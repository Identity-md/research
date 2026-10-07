# Audit report

> Audit the three Ponzinomics contracts in src/pimd: PimdToken, a fixed-supply ERC-20 of exactly 1,000,000,000 at 18 decimals with no owner, no mint and no burn; PimdHook, a Uniswap V4 hook that taxes every trade in IMD (2.4% on buys, 5.6% on sells) split 75% to holders and 25% to the team, taking fees as ERC-6909 claims on the quote currency; and PimdEngine, which pushes the holders' IMD into wallets weighted by balance times hold-streak across paged tally and pay calls. The hook is deployed by the IMD launch factory, which constructs it with only the pool manager and the token and opens the pool itself, so everything else is a source constant. Five things deserve the hardest look. First, beforeRemoveLiquidity is the entire safety case for letting the launch factory hold the liquidity position: it must refuse every negative liquidityDelta forever, from any caller including the position's owner and including the hook itself, while allowing a zero delta so the pool's own fee collection still works. If any path can withdraw liquidity, that is the finding that matters most. Second, beforeAddLiquidity must allow exactly one add, the factory's seed, and refuse every subsequent one; check for any way to slip a second through, including reentrancy and the hook calling itself. Third, beforeInitialize is the only gate on the pool's shape: confirm it cannot be bypassed and that every assumption the tax maths makes is actually enforced there, in particular that the quote currency is currency0, since every fee calculation depends on it and the token's address is no longer mined. Fourth, the fee accounting: that claims minted in beforeSwap and afterSwap always equal holdersOwed plus teamOwed, that nothing can be double counted or stranded, and that flush cannot pay out more than was taken. Fifth, the engine must never read holder weights while the PoolManager is unlocked, which is where a flash borrower would stand, and one holder who cannot receive IMD must not be able to stall a batch. Note also that the engine pulls from the hook inside a try/catch, which has already hidden one breakage from us: say whether that pattern is safe here. Report findings rather than fixing them, and do not propose changes to the economics, the tax rates, the split or the tier ladder.

| | |
|---|---|
| Repository | https://github.com/JJ-ME55/Ponzinomics.git |
| Commit | `1b073dfcce039c4b0e3e0072c8dc01f495ccc0ba` |
| Job | `ad23ef13-66b2-44ce-9cd3-172b051af105` |
| Judged | 2026-10-07 21:32 UTC |
| Findings | 1 high · 3 medium · 7 low · 5 info |

Four agents audited the code as it is at `1b073df`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: Paged tally weighs live balances, so one bag of PIMD moved between pages is counted once per registered wallet

`src/pimd/PimdEngine.sol:283`

```
            uint256 bal = IERC20Min(token).balanceOf(a);
```

tally() reads each registered holder's current balanceOf on the page that reaches it, compares it only with that holder's own lastBal, and tally is permissionless with a caller-chosen page size. Nothing ties the pages of one epoch to a single balance snapshot. One bag of PIMD can therefore register several wallets (register only needs the bag parked in the wallet at the moment of the call), and in every epoch the bag is parked in wallet A when the page containing A is tallied and moved to wallet B before the page containing B is tallied. Both wallets see bal == lastBal, so neither streak resets and neither blends; both are weighed at bag x tier. With N wallets the same tokens carry N times their weight, totalWeight is inflated, and every honest holder's mulDiv(total, w, tw) share in pay() shrinks accordingly. fire(), tally() and pay() are all permissionless, so the whole sequence can run in one transaction as soon as lastFire + minInterval has passed; no keeper race and no PoolManager unlock is involved, so the _requireLocked() guard does not see it. pay() is correctly frozen on epochQuote and totalWeight; tally is the only inconsistent read. Merged from audit_economics and audit_permissions, which reported the same mechanism. Fixing it means making one epoch's weights unmovable across pages: finish the tally in a single call, or weigh every page against balances fixed when the epoch fired (for example min(bal, lastBal) with increases counted from the next epoch, or a checkpointed read). This changes no rate, split or tier.

**Reproduction**

State: launched pool, engine bound and pot funded (100 IMD), tips set to 0 for clean numbers. Wallet A holds BAG = 1,000,000 PIMD and registers; the bag is sent to wallet B, B registers; the bag is sent back to A. Carol holds her own identical BAG and registers. Registration order [A, B, carol], 15 days pass. Calls: fire(); tally(1) (page ends after A, A weighed at BAG x 3); token.transfer(A -> B, BAG); tally(10) (B weighed at BAG x 3, carol at BAG x 3); pay(10). Expected: A + B together receive at most what carol receives, since they held one bag between them for exactly as long. Actual (test/scratch/PagingDoubleCount.t.sol, failing on this code): imd(A) + imd(B) = 41639116884859839266 wei, imd(carol) = 20819558442429919634 wei; the pair took two thirds of the epoch with the same bag carol held for one third. Repeatable every epoch by moving the bag back before the first page.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {IPoolManager} from "@uniswap/v4-core/src/interfaces/IPoolManager.sol";
import {PoolManager} from "@uniswap/v4-core/src/PoolManager.sol";
import {PoolModifyLiquidityTest} from "@uniswap/v4-core/src/test/PoolModifyLiquidityTest.sol";
import {PoolKey} from "@uniswap/v4-core/src/types/PoolKey.sol";
import {Currency} from "@uniswap/v4-core/src/types/Currency.sol";
import {ModifyLiquidityParams} from "@uniswap/v4-core/src/types/PoolOperation.sol";
import {TickMath} from "@uniswap/v4-core/src/libraries/TickMath.sol";
import {Hooks} from "@uniswap/v4-core/src/libraries/Hooks.sol";
import {IHooks} from "@uniswap/v4-core/src/interfaces/IHooks.sol";
import {LiquidityAmounts} from "v4-periphery/src/libraries/LiquidityAmounts.sol";
import {HookMiner} from "v4-periphery/test/shared/HookMiner.sol";
import {ERC20} from "solmate/src/tokens/ERC20.sol";
import {PimdToken} from "src/pimd/PimdToken.sol";
import {PimdHook} from "src/pimd/PimdHook.sol";
import {PimdEngine} from "src/pimd/PimdEngine.sol";

contract MockIMD is ERC20("Identity.md", "IMD", 18) {
    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

/// The production hook writes the engine and team into its source; this only points them at test doubles.
contract HookHarness is PimdHook {
    address private immutable _engine;
    address private immutable _team;

    constructor(IPoolManager pm, address token_, address engine_, address team_) PimdHook(pm, token_) {
        _engine = engine_;
        _team = team_;
    }

    function engine() public view override returns (address) {
        return _engine;
    }

    function team() public view override returns (address) {
        return _team;
    }
}

/// tally() reads each holder's live balanceOf on the page that reaches it, and tally is permissionless with a
/// caller-chosen page size. Nothing ties the pages of one epoch to a single snapshot, so one bag of PIMD moved
/// between two registered wallets between two pages is weighed twice. Expected: two wallets that together hold
/// one bag are paid no more than a third wallet holding the same bag. Actual: they are paid twice as much.
contract PagingDoubleCountTest is Test {
    uint160 constant HOOK_FLAGS = uint160(
        Hooks.BEFORE_INITIALIZE_FLAG | Hooks.AFTER_INITIALIZE_FLAG | Hooks.BEFORE_SWAP_FLAG | Hooks.AFTER_SWAP_FLAG
            | Hooks.BEFORE_SWAP_RETURNS_DELTA_FLAG | Hooks.AFTER_SWAP_RETURNS_DELTA_FLAG | Hooks.BEFORE_ADD_LIQUIDITY_FLAG
            | Hooks.BEFORE_REMOVE_LIQUIDITY_FLAG
    );
    int24 constant START_TICK = 129_000;
    int24 constant TICK_LOWER = 82_980;
    uint256 constant BAG = 1_000_000e18;

    IPoolManager manager;
    PoolModifyLiquidityTest lpRouter;
    MockIMD imd;
    PimdToken token;
    PimdHook hook;
    PimdEngine engine;
    PoolKey key;

    address team = makeAddr("team");
    address walletA = makeAddr("walletA");
    address walletB = makeAddr("walletB");
    address carol = makeAddr("carol");

    function setUp() public {
        manager = IPoolManager(address(new PoolManager(address(this))));
        lpRouter = new PoolModifyLiquidityTest(manager);
        imd = new MockIMD();

        engine = new PimdEngine(
            PimdEngine.Config({
                poolManager: address(manager),
                imd: address(imd),
                team: team,
                binder: address(this),
                dripBpsPerPeriod: 400,
                minInterval: 2 minutes,
                minBalance: 100_000e18,
                fireTip: 0,
                tipPerHolder: 0,
                maxCatchup: 6 hours
            })
        );

        token = PimdToken(_deployTokenAbove(address(imd)));

        bytes memory args = abi.encode(manager, address(token), address(engine), team);
        (address hookAddr, bytes32 salt) =
            HookMiner.find(address(this), HOOK_FLAGS, type(HookHarness).creationCode, args);
        hook = PimdHook(payable(address(new HookHarness{salt: salt}(manager, address(token), address(engine), team))));
        require(address(hook) == hookAddr, "hook addr");

        key = PoolKey({
            currency0: Currency.wrap(address(imd)),
            currency1: Currency.wrap(address(token)),
            fee: 12_500,
            tickSpacing: 60,
            hooks: IHooks(address(hook))
        });
        manager.initialize(key, TickMath.getSqrtPriceAtTick(START_TICK));
        uint256 amount = token.balanceOf(address(this)) * 9 / 10;
        uint128 liquidity = LiquidityAmounts.getLiquidityForAmount1(
            TickMath.getSqrtPriceAtTick(TICK_LOWER), TickMath.getSqrtPriceAtTick(START_TICK), amount
        );
        token.approve(address(lpRouter), type(uint256).max);
        lpRouter.modifyLiquidity(
            key,
            ModifyLiquidityParams({
                tickLower: TICK_LOWER,
                tickUpper: START_TICK,
                liquidityDelta: int256(uint256(liquidity)),
                salt: 0
            }),
            ""
        );
        engine.bind(address(token), address(hook));

        // The pot is funded directly so the payout maths is the only thing under test.
        imd.mint(address(this), 100e18);
        imd.approve(address(engine), type(uint256).max);
        engine.seed(100e18);
    }

    function test_one_bag_moved_between_pages_is_not_weighed_twice() public {
        // One bag registers two wallets: register A holding it, pass it to B, register B, pass it back to A.
        // Carol holds an identical bag of her own. Registration order is [A, B, carol].
        token.transfer(walletA, BAG);
        _register(walletA);
        vm.prank(walletA);
        token.transfer(walletB, BAG);
        _register(walletB);
        vm.prank(walletB);
        token.transfer(walletA, BAG);
        token.transfer(carol, BAG);
        _register(carol);
        assertEq(engine.holderCount(), 3, "three registered");

        vm.warp(block.timestamp + 15 days); // everyone is in the same tier

        engine.fire();
        assertEq(uint8(engine.phase()), uint8(PimdEngine.Phase.Tally), "epoch open");

        // Page 1 weighs A with the bag, then the bag moves to B before page 2 weighs B with the same bag.
        engine.tally(1);
        vm.prank(walletA);
        token.transfer(walletB, BAG);
        if (engine.phase() == PimdEngine.Phase.Tally) engine.tally(10);
        assertEq(uint8(engine.phase()), uint8(PimdEngine.Phase.Pay), "tallied");
        engine.pay(10);
        assertEq(uint8(engine.phase()), uint8(PimdEngine.Phase.Idle), "paid");

        uint256 pair = imd.balanceOf(walletA) + imd.balanceOf(walletB);
        uint256 honest = imd.balanceOf(carol);
        assertGt(honest, 0, "carol was paid");
        // A and B held exactly one bag between them, for exactly as long as carol held hers.
        assertLe(pair, honest + 1, "one bag must not be paid twice: A+B took more than carol");
    }

    function _register(address who) internal {
        address[] memory a = new address[](1);
        a[0] = who;
        engine.register(a);
    }

    function _deployTokenAbove(address floor) internal returns (address) {
        bytes32 initHash = keccak256(type(PimdToken).creationCode);
        for (uint256 i; i < 100_000; ++i) {
            bytes32 salt = bytes32(i);
            address predicted = vm.computeCreate2Address(salt, initHash, address(this));
            if (uint160(predicted) > uint160(floor)) {
                PimdToken t = new PimdToken{salt: salt}();
                require(address(t) == predicted, "create2");
                return address(t);
            }
        }
        revert("no salt");
    }
}
```

### 2. Medium: beforeInitialize never checks that currency0 is IMD, so any ERC-20 sorting below PIMD can be bound as the quote forever

`src/pimd/PimdHook.sol:217`

```
        if (c0 == address(token) || c0 == address(0)) revert BadCurrencyOrder();
```

The gate requires currency1 == PIMD and currency0 != PIMD and != address(0), then records quote = currency0 and sets launched for good. It never compares currency0 with IMD, although the engine at ENGINE_ADDRESS pays out its immutable imd and nothing else, every claim is minted against quoteId, flush take()s quote, and _book() reads imd.balanceOf. The brief's point that every fee calculation depends on the quote being currency0 is satisfied (c1 is pinned to PIMD so c0 is the quote), but which token the quote is remains unchecked. PoolManager.initialize is permissionless and the sender argument is discarded, so the first caller after the hook has code decides the quote. Preconditions: the factory's own initialize does not land in the same transaction as the hook's deployment (a window the launch factory code, which is not in this tree, would have to close), or the factory passes a wrong currency0 by mistake. Consequences: the factory's IMD pool is refused with AlreadyLaunched and the hook is spent; if trading ever happens on the foreign-quote pool, flush pushes the foreign token to the engine, which books only IMD, so the holders' 75% is stranded with no sweep and the team is paid in the foreign token. Four specialists reported this (one as high, three as medium); merged here as medium because reachability depends on the factory window. The hook already knows engine(), and the engine exposes imd() as a public immutable, so a one-line check (revert unless c0 == PimdEngine(engine()).imd()) pins the quote and also fails loudly on a chain where ENGINE_ADDRESS has no code. Checking the sender against the deployer is an alternative that also covers the seed.

**Reproduction**

State: a freshly deployed, unlaunched PimdHook for PIMD; junk = any other ERC-20 whose address sorts below PIMD. Input: any address calls manager.initialize(PoolKey{currency0: junk, currency1: PIMD, fee: 12500, tickSpacing: 60, hooks: hook}, TickMath.getSqrtPriceAtTick(129000)). Expected: the hook reverts, launched() stays false, and a later initialize with currency0 = IMD succeeds. Actual (test/scratch/P1_WrongQuote.t.sol, the audit_economics proof, failing on this code with 'next call did not revert as expected'): the call succeeds, hook.launched() == true, hook.quote() == junk, and the IMD initialize then reverts AlreadyLaunched. The audit_math proof (test/scratch/P3_InitFrontRun.t.sol) reproduces the same from a non-factory sender.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {IPoolManager} from "@uniswap/v4-core/src/interfaces/IPoolManager.sol";
import {PoolManager} from "@uniswap/v4-core/src/PoolManager.sol";
import {PoolKey} from "@uniswap/v4-core/src/types/PoolKey.sol";
import {Currency} from "@uniswap/v4-core/src/types/Currency.sol";
import {TickMath} from "@uniswap/v4-core/src/libraries/TickMath.sol";
import {Hooks} from "@uniswap/v4-core/src/libraries/Hooks.sol";
import {IHooks} from "@uniswap/v4-core/src/interfaces/IHooks.sol";
import {HookMiner} from "v4-periphery/test/shared/HookMiner.sol";
import {ERC20} from "solmate/src/tokens/ERC20.sol";
import {PimdToken} from "src/pimd/PimdToken.sol";
import {PimdHook} from "src/pimd/PimdHook.sol";
import {PimdEngine} from "src/pimd/PimdEngine.sol";

contract MockIMD is ERC20("Identity.md", "IMD", 18) {
    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

contract HookHarness is PimdHook {
    address private immutable _engine;
    address private immutable _team;

    constructor(IPoolManager pm, address token_, address engine_, address team_) PimdHook(pm, token_) {
        _engine = engine_;
        _team = team_;
    }

    function engine() public view override returns (address) {
        return _engine;
    }

    function team() public view override returns (address) {
        return _team;
    }
}

/// The hook's tax, its claims, its flush and the engine's payout all assume currency0 is IMD, the asset the engine
/// was built for. beforeInitialize only checks that currency1 is PIMD, so any ERC-20 that sorts below PIMD is
/// accepted as the quote. PoolManager.initialize is permissionless, so whoever calls it first with a junk
/// currency0 spends the hook's single launch, and the real IMD pool can never open on this hook.
contract WrongQuoteTest is Test {
    uint160 constant HOOK_FLAGS = uint160(
        Hooks.BEFORE_INITIALIZE_FLAG | Hooks.AFTER_INITIALIZE_FLAG | Hooks.BEFORE_SWAP_FLAG | Hooks.AFTER_SWAP_FLAG
            | Hooks.BEFORE_SWAP_RETURNS_DELTA_FLAG | Hooks.AFTER_SWAP_RETURNS_DELTA_FLAG | Hooks.BEFORE_ADD_LIQUIDITY_FLAG
            | Hooks.BEFORE_REMOVE_LIQUIDITY_FLAG
    );
    int24 constant START_TICK = 129_000;

    IPoolManager manager;
    MockIMD imd;
    MockIMD junk;
    PimdToken token;
    PimdHook hook;
    PimdEngine engine;

    address team = makeAddr("team");
    address attacker = makeAddr("attacker");

    function setUp() public {
        manager = IPoolManager(address(new PoolManager(address(this))));
        imd = new MockIMD();
        junk = new MockIMD(); // any other ERC-20 that sorts below PIMD

        engine = new PimdEngine(
            PimdEngine.Config({
                poolManager: address(manager),
                imd: address(imd),
                team: team,
                binder: address(this),
                dripBpsPerPeriod: 400,
                minInterval: 2 minutes,
                minBalance: 100_000e18,
                fireTip: 0.02e18,
                tipPerHolder: 0.0005e18,
                maxCatchup: 6 hours
            })
        );

        address floor = uint160(address(imd)) > uint160(address(junk)) ? address(imd) : address(junk);
        token = PimdToken(_deployTokenAbove(floor));

        bytes memory args = abi.encode(manager, address(token), address(engine), team);
        (address hookAddr, bytes32 salt) =
            HookMiner.find(address(this), HOOK_FLAGS, type(HookHarness).creationCode, args);
        hook = PimdHook(payable(address(new HookHarness{salt: salt}(manager, address(token), address(engine), team))));
        require(address(hook) == hookAddr, "hook addr");
    }

    function test_initialize_refuses_a_quote_that_is_not_imd() public {
        PoolKey memory bad = PoolKey({
            currency0: Currency.wrap(address(junk)),
            currency1: Currency.wrap(address(token)),
            fee: 12_500,
            tickSpacing: 60,
            hooks: IHooks(address(hook))
        });

        // The hook must refuse a pool whose quote is not the asset the engine pays out.
        vm.prank(attacker);
        vm.expectRevert();
        manager.initialize(bad, TickMath.getSqrtPriceAtTick(START_TICK));

        // And the real pool still opens afterwards.
        PoolKey memory good = PoolKey({
            currency0: Currency.wrap(address(imd)),
            currency1: Currency.wrap(address(token)),
            fee: 12_500,
            tickSpacing: 60,
            hooks: IHooks(address(hook))
        });
        manager.initialize(good, TickMath.getSqrtPriceAtTick(START_TICK));
        assertTrue(hook.launched(), "launched on IMD");
        assertEq(Currency.unwrap(hook.quote()), address(imd), "the quote is IMD");
    }

    function _deployTokenAbove(address floor) internal returns (address) {
        bytes32 initHash = keccak256(type(PimdToken).creationCode);
        for (uint256 i; i < 100_000; ++i) {
            bytes32 salt = bytes32(i);
            address predicted = vm.computeCreate2Address(salt, initHash, address(this));
            if (uint160(predicted) > uint160(floor)) {
                PimdToken t = new PimdToken{salt: salt}();
                require(address(t) == predicted, "create2");
                return address(t);
            }
        }
        revert("no salt");
    }
}
```

### 3. Medium: beforeAddLiquidity gives the single permitted add to whoever is first, so a stranger's dust add locks the factory out of its seed

`src/pimd/PimdHook.sol:306`

```
        if (seeded) revert LiquidityIsLocked();
```

The one-add rule is a boolean flipped on the first beforeAddLiquidity with no check of the sender, the range, the side or the size. Between PoolManager.initialize and the factory's modifyLiquidity, any address can add dust liquidity through any router: a range strictly above the opening tick needs only IMD, which anyone holds. seeded flips to true, the factory's real single-sided seed of 90% of the supply reverts LiquidityIsLocked, and since nothing resets seeded or launched the pool stays essentially empty and the launch must be redone with a new hook. The reentrancy and self-call routes the brief asks about are closed: seeded is written before the hook returns and beforeAddLiquidity makes no external call; the hook has no code path that calls modifyLiquidity, so the Hooks.noSelfCall skip is unreachable; unlockCallback only knows ACTION_FLUSH; and a reverting add reverts the flag with it. The only remaining way to slip a wrong add through is this ordering one, and it exists only if the factory's initialize and seed are not in one transaction (or a reverted seed leaves the pool initialized but unseeded). Three specialists reported it; merged as medium. Fixing it means tying the one add to the pool's opener (record the sender passed to beforeInitialize and require beforeAddLiquidity's sender to match) or requiring the add in initBlock; both keep the single-seed design.

**Reproduction**

State: pool initialized by the factory stand-in (hook.launched() == true, hook.seeded() == false), seed not yet sent. Input: a stranger holding 1e18 IMD calls PoolModifyLiquidityTest.modifyLiquidity(key, {tickLower: 129060, tickUpper: 129120, liquidityDelta: 1e6, salt: 0}). Expected: refused; hook.seeded() stays false and the factory's seed succeeds. Actual (test/scratch/P2_FrontRunSeed.t.sol, the audit_economics proof, failing on this code with 'next call did not revert as expected'): the dust add succeeds, hook.seeded() == true, and the factory's seed of ~900M PIMD then reverts LiquidityIsLocked. The audit_math proof (test/scratch/P3_InitFrontRun.t.sol) shows the same with liquidityDelta = 1 in the factory's own range.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {IPoolManager} from "@uniswap/v4-core/src/interfaces/IPoolManager.sol";
import {IUnlockCallback} from "@uniswap/v4-core/src/interfaces/callback/IUnlockCallback.sol";
import {PoolManager} from "@uniswap/v4-core/src/PoolManager.sol";
import {PoolModifyLiquidityTest} from "@uniswap/v4-core/src/test/PoolModifyLiquidityTest.sol";
import {PoolKey} from "@uniswap/v4-core/src/types/PoolKey.sol";
import {Currency} from "@uniswap/v4-core/src/types/Currency.sol";
import {BalanceDelta} from "@uniswap/v4-core/src/types/BalanceDelta.sol";
import {ModifyLiquidityParams} from "@uniswap/v4-core/src/types/PoolOperation.sol";
import {TickMath} from "@uniswap/v4-core/src/libraries/TickMath.sol";
import {Hooks} from "@uniswap/v4-core/src/libraries/Hooks.sol";
import {IHooks} from "@uniswap/v4-core/src/interfaces/IHooks.sol";
import {LiquidityAmounts} from "v4-periphery/src/libraries/LiquidityAmounts.sol";
import {HookMiner} from "v4-periphery/test/shared/HookMiner.sol";
import {ERC20} from "solmate/src/tokens/ERC20.sol";
import {PimdToken} from "src/pimd/PimdToken.sol";
import {PimdHook} from "src/pimd/PimdHook.sol";
import {PimdEngine} from "src/pimd/PimdEngine.sol";

contract MockIMD is ERC20("Identity.md", "IMD", 18) {
    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

contract HookHarness is PimdHook {
    address private immutable _engine;
    address private immutable _team;

    constructor(IPoolManager pm, address token_, address engine_, address team_) PimdHook(pm, token_) {
        _engine = engine_;
        _team = team_;
    }

    function engine() public view override returns (address) {
        return _engine;
    }

    function team() public view override returns (address) {
        return _team;
    }
}

/// A stand-in for the launch factory: holds the supply, initializes the pool and seeds it itself, as the real
/// factory does, so the hook sees the same `sender` for both calls.
contract MiniFactory is IUnlockCallback {
    IPoolManager immutable pm;

    constructor(IPoolManager pm_) {
        pm = pm_;
    }

    function open(PoolKey memory key, uint160 sqrtPriceX96) external {
        pm.initialize(key, sqrtPriceX96);
    }

    function seed(PoolKey memory key, ModifyLiquidityParams memory p) external {
        pm.unlock(abi.encode(key, p));
    }

    function unlockCallback(bytes calldata data) external returns (bytes memory) {
        require(msg.sender == address(pm), "pm");
        (PoolKey memory key, ModifyLiquidityParams memory p) = abi.decode(data, (PoolKey, ModifyLiquidityParams));
        (BalanceDelta delta,) = pm.modifyLiquidity(key, p, "");
        if (delta.amount0() < 0) _settle(key.currency0, uint256(uint128(-delta.amount0())));
        if (delta.amount1() < 0) _settle(key.currency1, uint256(uint128(-delta.amount1())));
        return "";
    }

    function _settle(Currency c, uint256 amount) internal {
        pm.sync(c);
        ERC20(Currency.unwrap(c)).transfer(address(pm), amount);
        pm.settle();
    }
}

/// beforeAddLiquidity accepts whichever add comes first, from anyone, in any range, of any size. If the factory's
/// initialize and seed are not in one transaction, a stranger's dust add between them takes the only slot, the
/// factory's seed is refused forever, and the hook, which can launch only once, is spent on an empty pool.
contract FrontRunSeedTest is Test {
    uint160 constant HOOK_FLAGS = uint160(
        Hooks.BEFORE_INITIALIZE_FLAG | Hooks.AFTER_INITIALIZE_FLAG | Hooks.BEFORE_SWAP_FLAG | Hooks.AFTER_SWAP_FLAG
            | Hooks.BEFORE_SWAP_RETURNS_DELTA_FLAG | Hooks.AFTER_SWAP_RETURNS_DELTA_FLAG | Hooks.BEFORE_ADD_LIQUIDITY_FLAG
            | Hooks.BEFORE_REMOVE_LIQUIDITY_FLAG
    );
    int24 constant START_TICK = 129_000;
    int24 constant TICK_LOWER = 82_980;

    IPoolManager manager;
    MockIMD imd;
    PimdToken token;
    PimdHook hook;
    PimdEngine engine;
    MiniFactory factory;
    PoolKey key;

    address team = makeAddr("team");
    address attacker = makeAddr("attacker");

    function setUp() public {
        manager = IPoolManager(address(new PoolManager(address(this))));
        imd = new MockIMD();
        factory = new MiniFactory(manager);

        engine = new PimdEngine(
            PimdEngine.Config({
                poolManager: address(manager),
                imd: address(imd),
                team: team,
                binder: address(this),
                dripBpsPerPeriod: 400,
                minInterval: 2 minutes,
                minBalance: 100_000e18,
                fireTip: 0.02e18,
                tipPerHolder: 0.0005e18,
                maxCatchup: 6 hours
            })
        );

        token = PimdToken(_deployTokenAbove(address(imd)));
        token.transfer(address(factory), token.balanceOf(address(this))); // the factory holds the supply

        bytes memory args = abi.encode(manager, address(token), address(engine), team);
        (address hookAddr, bytes32 salt) =
            HookMiner.find(address(this), HOOK_FLAGS, type(HookHarness).creationCode, args);
        hook = PimdHook(payable(address(new HookHarness{salt: salt}(manager, address(token), address(engine), team))));
        require(address(hook) == hookAddr, "hook addr");

        key = PoolKey({
            currency0: Currency.wrap(address(imd)),
            currency1: Currency.wrap(address(token)),
            fee: 12_500,
            tickSpacing: 60,
            hooks: IHooks(address(hook))
        });
        factory.open(key, TickMath.getSqrtPriceAtTick(START_TICK));
        assertTrue(hook.launched(), "pool open, not yet seeded");
        assertFalse(hook.seeded(), "not yet seeded");
    }

    function test_a_stranger_cannot_take_the_factory_seed_slot() public {
        // A range strictly above the opening tick needs only IMD, which anyone has. Dust is enough.
        imd.mint(attacker, 1e18);
        PoolModifyLiquidityTest attackerRouter = new PoolModifyLiquidityTest(manager);
        vm.startPrank(attacker);
        imd.approve(address(attackerRouter), type(uint256).max);
        vm.expectRevert();
        attackerRouter.modifyLiquidity(
            key,
            ModifyLiquidityParams({tickLower: START_TICK + 60, tickUpper: START_TICK + 120, liquidityDelta: 1e6, salt: 0}),
            ""
        );
        vm.stopPrank();

        // The factory's own single-sided seed must still go through.
        uint256 amount = token.balanceOf(address(factory)) * 9 / 10;
        uint128 liquidity = LiquidityAmounts.getLiquidityForAmount1(
            TickMath.getSqrtPriceAtTick(TICK_LOWER), TickMath.getSqrtPriceAtTick(START_TICK), amount
        );
        factory.seed(
            key,
            ModifyLiquidityParams({
                tickLower: TICK_LOWER,
                tickUpper: START_TICK,
                liquidityDelta: int256(uint256(liquidity)),
                salt: 0
            })
        );
        assertTrue(hook.seeded(), "the factory seeded");
        assertGt(token.balanceOf(address(manager)), 800_000_000e18, "the supply is in the pool");
    }

    function _deployTokenAbove(address floor) internal returns (address) {
        bytes32 initHash = keccak256(type(PimdToken).creationCode);
        for (uint256 i; i < 100_000; ++i) {
            bytes32 salt = bytes32(i);
            address predicted = vm.computeCreate2Address(salt, initHash, address(this));
            if (uint160(predicted) > uint160(floor)) {
                PimdToken t = new PimdToken{salt: salt}();
                require(address(t) == predicted, "create2");
                return address(t);
            }
        }
        revert("no salt");
    }
}
```

### 4. Medium: Tax is charged on the specified amount, not the filled one: a partially filled exact-in buy or exact-out sell pays tax on IMD that never traded

`src/pimd/PimdHook.sol:253`

```
            fee = params.amountSpecified < 0 ? amt * bps / BPS : amt * bps / (BPS - bps);
```

For the two cases where IMD is the specified side (exact-in buy, exact-out sell) beforeSwap computes the fee from params.amountSpecified and mints that many claims before the pool has decided how much it can fill. A V4 swap stops at sqrtPriceLimitX96 or when the range runs out and returns the smaller delta, but the hook's BeforeSwapDelta of +fee is charged to the swapper in full and afterSwap books the whole fee into holdersOwed and teamOwed. The claims == holdersOwed + teamOwed invariant still holds, so the ledger is consistent, but the stated economics (2.4% of a buy, 5.6% of a sell) are not: with a tight price limit a 1000 IMD offer that fills a sliver pays the full 24 IMD, and an exact-out sell asking for more IMD than the pool holds pays 5.6%/94.4% of the ask while receiving only what the pool has; had the pool held less than the fee the seller's IMD delta would have gone negative. The two unspecified cases (exact-out buy, exact-in sell) are unaffected because their fee is computed in afterSwap from delta.amount0(). This is reachable by ordinary users through any router that allows partial fills, and is most likely exactly at the ends of the single range. Two specialists reported it; merged as medium. Fixing it within the existing economics means computing the fee for all four cases in afterSwap from the executed IMD amount, returning it as the hook delta on the specified side; the rates and split are unchanged.

**Reproduction**

State: launched and seeded pool, past the init block and the launch-cap window. Buy case: alice holds 1000 IMD and swaps zeroForOne, amountSpecified = -1000e18, sqrtPriceLimitX96 = spot - spot/20000. Expected: tax within 5% of 2.4% of the IMD that actually traded. Actual (test/scratch/PartialFillTax.t.sol, failing on this code): hook.totalTaxed() grew by 24000000000000000000 while only 3113002299885281 wei of IMD traded. Sell case: after a 100 IMD buy the pool holds about 97 IMD; bob holds PIMD and swaps oneForZero, amountSpecified = +1000e18, limit MAX_SQRT_PRICE - 1. Expected: tax within 5% of 5.6% of the IMD the pool paid out. Actual: tax 59322033898305084745 wei against about 96.4 IMD paid out, 5.6% of which would be 5397279999999999999 wei.

### 5. Low: flush is all-or-nothing across engine, team and tipper, so IMD refusing the fixed team wallet strands the holders' slice at the hook

`src/pimd/PimdHook.sol:389`

```
            _payOut(team(), toTeam);
```

The engine deliberately survives one refused IMD recipient (gas-capped _send, failure logged, share back to the pot). The hook does not: unlockCallback burns claims and take()s to the engine, the team wallet and the caller in one unlock, and take() does a plain ERC-20 transfer, so a revert on any one leg reverts the whole flush and holdersOwed and teamOwed are restored. TEAM_WALLET and ENGINE_ADDRESS are source constants with no setter. IMD is a third party's token whose owner powers the engine's own comments call unknown; if it ever refuses transfers to the team wallet, every flush from every caller reverts, holdersOwed grows forever as claims the hook can never burn, and fire() swallows the failure (next finding) and keeps dripping only from an unfed pot. The tipper leg is harmless because the caller picks themself. Three specialists reported it; merged as low because it needs IMD to refuse a fixed address. A fix that keeps the split: pay the holders' and team's legs independently, or make the team leg best-effort and leave teamOwed in place on failure, so the holders' path never depends on the team address being transferable.

**Reproduction**

State: launched pool, one 100 IMD buy so holdersOwed = 1.8 IMD and teamOwed = 0.6 IMD; vm.mockCallRevert(imd, abi.encodeWithSignature('transfer(address,uint256)', team), 'blacklisted') stands in for IMD refusing the team wallet. Input: keeper calls hook.flush(). Expected: the holders' 1.8 IMD reaches the engine. Actual (test/scratch/Leads.t.sol::test_flush_is_all_or_nothing, passing as a demonstration): flush reverts, hook.holdersOwed() stays 1.8e18; two days later engine.fire() succeeds with imd.balanceOf(engine) == 0, pot == 0, holdersOwed unchanged, and exactly one engine event (Fired) emitted.

### 6. Low: fire()'s empty catch around hook.flush() is safe for funds but hides every pull failure, and still tips the keeper

`src/pimd/PimdEngine.sol:247`

```
            try hook.flush() {} catch {}
```

Assessment of the pattern, as the brief asks. It is safe against value extraction: flush() is nonReentrant and its take() path makes no callback into the engine; fire() is nonReentrant and _requireLocked; the engine's ledger is only updated by _book() from the real IMD balance, so a failed or partial pull can never be booked as income; and the 63/64 gas trick is not practical because the work fire() still has to do after flush() needs far less gas than flush() itself. It is not safe operationally, which is exactly how it already masked one breakage: the catch is empty, so a flush that reverts on every epoch (a hook whose ENGINE_ADDRESS is a different engine, IMD refusing the team wallet, a wrong quote) is indistinguishable on chain from a quiet market; fire() proceeds, lastFire advances, the drip is computed from a pot that never grows, and the keeper's fireTip is still paid from that pot for an epoch whose income never arrived. Two edges besides: hook.holdersOwed() on the line above sits outside the try, so a hook whose view reverted would block fire() entirely (the opposite of the stated intent; not reachable with this hook), and Solidity does not route return-data decoding failures of flush() into the catch, so a hook returning malformed data would also revert fire(). Four specialists reported this; merged as low. Minimal fix without changing behaviour: catch (bytes memory reason) and emit an event carrying it and the pending amount, and decide deliberately whether fireTip should be paid when the pull failed.

**Reproduction**

State: launched pool, alice bought 200 IMD so hook.holdersOwed() > 0, alice registered two days ago, pot seeded with 10 IMD; vm.mockCallRevert(hook, PimdHook.flush.selector, 'broken') stands in for any deterministic revert. Input: keeper calls engine.fire(). Expected: a revert or an on-chain signal that income could not be pulled. Actual (test/scratch/Leads.t.sol::test_fire_hides_a_broken_flush_and_still_tips, passing as a demonstration): fire() succeeds, hook.holdersOwed() is unchanged, phase == Tally, imd.balanceOf(keeper) == fireTip (0.02 IMD), and the engine emitted exactly one event (Fired), no failure event.

### 7. Low: The unlock guard only sees the Uniswap V4 PoolManager; a PIMD balance borrowed from any other lender is tallied as weight

`src/pimd/PimdEngine.sol:426`

```
        if (IExttload(address(poolManager)).exttload(IS_UNLOCKED_SLOT) != bytes32(0)) revert PoolUnlocked();
```

fire, tally and pay refuse to run while the PoolManager's transient unlock flag is set, which closes the V4 flash path the design notes name, and the three existing tests confirm it from inside a real unlock. The comment 'Outside an unlock the borrow cannot exist' is not true in general: PIMD is a plain ERC-20, and a V3 pool with flash(), an ERC-3156 lender or a money market listing PIMD never touches the PoolManager's lock. A registered holder that is a contract can borrow inside such a callback, call tally(), and repay. The size blend dampens but does not neutralise it: with lastBal = 3.5M and 38.7M borrowed, a 15-day holder's blended age falls to about 1.24 days (tier 1x), so the weight is 42.2M instead of the honest 10.5M (3.5M x 3x), a 4x boost paid out of the other holders' share of that epoch. The borrower's own streak resets at the next tally (bal < last), so this is one epoch per address, repeatable by rotating addresses. Precondition not present in this tree: a third-party PIMD lender with a large bag, which is why this is low. The guard is correct for what it covers; the finding is that the engine's safety claim rests on an assumption about the whole chain, not about the PoolManager. Mitigations that keep the economics overlap with the paging finding: weigh on min(bal, lastBal) with increases counted from the next epoch, or snapshot balances one block earlier.

**Reproduction**

State: engine bound and pot funded (100 IMD); lender contract L holds 38,700,000 PIMD; alice and contract holder B hold 3,500,000 PIMD each, both registered 15 days ago; fire() called so phase == Tally. Input: B calls L.flash(B, 38.7M, cb) where cb runs engine.tally(100) and then repays. Expected: tally refuses or ignores the borrowed balance; B's weight == 3.5M x 3 = 10.5M. Actual (test/scratch/Leads.t.sol::test_lender_outside_v4_is_tallied_as_weight, passing as a demonstration): tally completes inside the callback, holderInfo(B).lastBal == 42,200,000e18, totalWeight - aliceWeight == 42.2M against alice's 10.5M, and pay(100) sends B 50015347226027093464 wei against alice's 12444328101262665435 wei for an equal honest bag.

### 8. Low: A sell followed by a re-buy to at least lastBal before the next tally keeps the full hold streak, contrary to the documented rule

`src/pimd/PimdEngine.sol:285`

```
            if (bal < last) {
```

The streak is maintained from balance snapshots taken at tally time, not from transfers. The restart fires only when the balance at this tally is below the balance at the previous one. A holder who sells (or sends out) any amount and restores at least the same token count before the next tally is seen as bal >= last: if exactly equal nothing changes, if slightly above the blend touches only the difference. The README and the engine's NatSpec promise 'selling or sending tokens out restarts your streak'; the engine cannot see a round trip that completes between two tallies, and the window is the keeper cadence (15 minutes by policy, unbounded if the keeper is down). The round trip costs the 5.6% and 2.4% taxes plus pool fees, so it is not a farming move, but a 14-day 3x holder can take profit at a local top and re-enter without losing the tier, which is the behaviour the streak was designed to penalise. Two specialists reported it; merged as low. No code fix is proposed because the stronger rule needs per-transfer tracking the token deliberately omits; the finding is that the documented guarantee and the enforced one differ, and the documents should state the enforced one.

**Reproduction**

State: alice bought 100 IMD of PIMD (bag), registered, 15 days pass, an epoch runs; holderInfo(alice).tierBps == 30000 and lastBal == bag. Input: alice sells 90% of the bag exact-in, then buys back exact-out so that balanceOf(alice) == bag again; 3 minutes later fire/tally/pay run. Expected per the documented rule: tier 0 (clock restarted by the sale). Actual (test/scratch/Leads.t.sol::test_sell_and_rebuy_keeps_the_streak, passing as a demonstration): holderInfo(alice).tierBps == 30000 after the second epoch; the tally saw bal == last and kept streakStart.

### 9. Low: bind() does not check that the hook pays this engine, in this IMD, on this PoolManager

`src/pimd/PimdEngine.sol:181`

```
        hook = IPimdHookLike(hook_);
```

The hook's payout target is the compile-time constant ENGINE_ADDRESS and its quote is whatever currency0 the pool opened with. bind() accepts any non-zero hook address and verifies none of hook.engine() == address(this), hook.quote() == imd, hook.poolManager() == poolManager or hook.launched(). The deploy script prints the engine address and relies on a human to write it into the hook source before the launch request goes out; if the bound engine is not the one baked into the hook, the engine binds fine, fires fine, and never receives income: flush moves the holders' slice to the constant address and the bound engine receives only the flush callerTip paid to it as msg.sender. Combined with the empty catch in fire(), nothing reverts and nothing is logged, which matches the breakage the brief says was already hidden once. A PoolManager mismatch would additionally make _requireLocked read the wrong contract's lock and silently disable the flash guard. Fix: have bind() read the hook's public engine(), quote() and poolManager() views and revert on mismatch.

**Reproduction**

State: launched protocol whose hook's engine() returns E1 (the bound engine). Input: deploy a second engine E2 with the same config and call E2.bind(token, hook); alice buys 100 IMD (holdersOwed = 1.8 IMD); 3 minutes later the keeper calls E2.fire(). Expected: bind reverts because hook.engine() != E2. Actual (test/scratch/Leads.t.sol::test_bind_accepts_a_hook_that_pays_another_engine, passing as a demonstration): bind succeeds, E2.fire() succeeds, hook.holdersOwed() == 0, imd.balanceOf(E1) == 1.8e18, and 0 < E2.pot() <= callerTip (0.01 IMD): E2 looks alive while receiving no holder income.

### 10. Low: register() lets one minBalance bag register unlimited addresses, growing every epoch's tally and pay cost

`src/pimd/PimdEngine.sol:209`

```
            if (bal < minBalance || _isPool(a)) continue;
```

register() checks only that the address holds minBalance at the instant of the call; the balance does not have to stay, there is no caller restriction or bond, and it is the one state-changing entry without _requireLocked(), so PIMD taken from the PoolManager inside an unlock would also do. One bag of exactly minBalance (100,000 PIMD, 0.01% of supply) transferred through N fresh addresses registers each. Every registered address is then visited by tally (balanceOf call plus storage writes) and pay (storage read) in every epoch until someone pays to prune it, and prune() is a separate paid step after which the same bag re-registers for the price of gas. The keeper tip budget (5% of each drip) does not scale with holder count. Griefing only, bounded by the griefer's gas, hence low. The same openness means any contract holding PIMD that is not a V2-style pair (a treasury, a vesting contract, the factory) can be registered by anyone and pushed IMD it may never be able to move; that is a launch-policy question recorded here for the requester. Mitigations that keep the economics: self-registration only (msg.sender == account) plus _requireLocked on register, and/or letting tally drop entries below minBalance.

**Reproduction**

State: launched pool, alice registered; a griefer holds exactly minBalance (100,000e18) PIMD. Input: 50 times, transfer the bag to a fresh address and call engine.register([that address]). Expected: registration is bounded by real holdings. Actual (test/scratch/Leads.t.sol::test_register_bloat_with_one_bag, passing as a demonstration): holderCount() == 51 while token.balanceOf(last address) == minBalance is the only bag that ever existed; the next epoch's tally(100) costs 833031 gas against about 20k for the one real holder.

### 11. Low: fire() pays fireTip from the pot even when no epoch opens because nobody is registered

`src/pimd/PimdEngine.sol:268`

```
        _tip(fireTip);
```

tipBudget is set to 5% of the computed drip before the `drip != 0 && n != 0` check, and _tip(fireTip) runs unconditionally after it. While holders.length == 0 (before anyone registers) the pot is not released and lastFire still advances, so the slice is deferred rather than lost, but the caller is paid fireTip out of the pot for a no-op, and can repeat it every minInterval until registration happens. Bounded by min(fireTip, 5% of the would-be drip) per call, so a small leak of holders' money rather than a drain; the comment 'tips never exceed 5% of an epoch's drip' assumes an epoch. Two specialists reported it (info and low); merged as low. If intended, document it; otherwise set tipBudget only when an epoch actually opens.

**Reproduction**

State: bound engine, holderCount() == 0, pot seeded with 100 IMD, fireTip = 0.02 IMD, dripBps = 400. Input: keeper calls fire() 2 minutes after bind, then again 2 minutes later. Expected: nothing to do, nothing paid. Actual (test/scratch/Leads.t.sol::test_fire_tip_is_paid_with_no_holders, passing as a demonstration): phase stays Idle, no epoch opens, imd.balanceOf(keeper) == 0.02e18 after the first call and more after the second, pot == 100e18 - 0.02e18 after the first call.

### 12. Info: _INSWAP_SLOT is never written, so the early returns in beforeSwap and afterSwap are dead code

`src/pimd/PimdHook.sol:244`

```
        if (_tload(_INSWAP_SLOT) == 1) return (IHooks.beforeSwap.selector, toBeforeSwapDelta(0, 0), 0);
```

The inswap transient flag was the guard for the removed v1 burn self-swap. No code path calls _tstore(_INSWAP_SLOT, ...) any more, so the checks at lines 244 and 265 can never be true and the fee is always taken. Not exploitable; it is audit surface that reads as an untaxed swap path (and, because afterSwap also returns early, a launch-cap bypass) waiting for a future change to arm it. Hooks.noSelfCall would skip the hook on a self-swap anyway, and the hook never calls swap, modifyLiquidity or initialize on the PoolManager, so the self-call exemption cannot be used to bypass beforeInitialize, beforeAddLiquidity or beforeRemoveLiquidity. Four specialists reported it; merged. Remove the constant and both branches, or pin them unreachable with a test.

**Reproduction**

grep -n _INSWAP_SLOT src/pimd/PimdHook.sol shows one declaration (line 81) and two _tload reads (lines 244, 265) and no _tstore. For any swap, _tload(_INSWAP_SLOT) == 0, so the branch is never taken; every existing swap test pays the tax.

### 13. Info: LAUNCH_CAP_MAX_SECONDS can never be the binding bound because launchCapSeconds (600) is already smaller than it (3600)

`src/pimd/PimdHook.sol:287`

```
                    && block.timestamp < uint256(launchStart) + LAUNCH_CAP_MAX_SECONDS
```

The comment describes LAUNCH_CAP_MAX_SECONDS as a fail-open bound on the block-based launch cap in case ArbSys stops answering. The window is the conjunction of three conditions, and the time condition using launchCapSeconds (600 s) always expires before the one using LAUNCH_CAP_MAX_SECONDS (3600 s), so the third conjunct is dead in both afterSwap and inLaunchCapWindow. Not a vulnerability; it misstates what protects against a stuck cap (launchCapSeconds does), which matters if launchCapSeconds is ever raised above an hour expecting the max to hold.

**Reproduction**

For any timestamp t: t < launchStart + 600 implies t < launchStart + 3600, so removing the third conjunct changes no evaluation. test/scratch/Leads.t.sol::test_launch_cap_max_is_dead asserts launchCapSeconds() < LAUNCH_CAP_MAX_SECONDS() on the deployed constants.

### 14. Info: README and contract NatSpec describe a different economy from the code (3%/7%, 60/20/20 with a burn, a launcher role)

`README.md:6`

```
- **3% on buys, 7% on sells**, taken in IMD by the hook
```

The code taxes 2.4% on buys and 5.6% on sells (BUY_TAX_BPS = 240, SELL_TAX_BPS = 560), splits 75/25 between holders and the team (HOLDERS_BPS = 7_500) with no burn slice, has no launcher role or launch() function, and the engine's NatSpec at PimdEngine.sol line 26 still calls the holders' share 60%. The README also says the token mints to the hook and that the deploy script mines the token's salt and opens the pool, all superseded by the factory launch. Since this review was briefed on 2.4/5.6/75/25 as the agreed design, the code is taken as correct and the documents as stale; an auditor or user reading them will check the wrong invariants.

**Reproduction**

Compare README.md lines 6-7 and 28 and src/pimd/PimdHook.sol lines 30-35 with src/pimd/PimdHook.sol lines 57-59 (BUY_TAX_BPS = 240, SELL_TAX_BPS = 560, HOLDERS_BPS = 7_500) and src/pimd/PimdEngine.sol line 26 ('the holders' 60%'). The existing test test_tax_splits_seventy_five_twenty_five passes against the code, not the README.

### 15. Info: totalBurned and circulatingSupply ignore PIMD sent to address(0), which solmate's ERC20 allows

`src/pimd/PimdToken.sol:40`

```
        return balanceOf[DEAD];
```

solmate's ERC20.transfer has no zero-address check, so PIMD can be sent to address(0) and is as unspendable as at DEAD, but the site's burn counter and circulatingSupply only count DEAD. The engine already treats both addresses as excluded. Harmless to funds; the published scarcity numbers can understate burns.

**Reproduction**

Input: a holder calls token.transfer(address(0), 1e18). Expected: totalBurned() includes it. Actual (test/scratch/Leads.t.sol::test_total_burned_ignores_address_zero, passing as a demonstration): balanceOf(address(0)) == 1e18 and totalBurned() is unchanged.

### 16. Info: The tax applies only to this pool: a second PIMD pool without the hook trades untaxed

`src/pimd/PimdHook.sol:30`

```
/// @notice The Ponzinomics ($PIMD) hook. PIMD is paired with **IMD**, and every trade pays a tax **in IMD**:
```

PimdToken is a plain ERC-20 with no transfer tax and PoolManager.initialize is permissionless, so anyone can open PIMD/IMD (or PIMD/anything) with hooks = address(0) or another hook, add liquidity bought from the taxed pool, and route trades there with no 2.4%/5.6% tax and no contribution to holders. The engine excludes the PoolManager from drips and _isPool() filters V2-style pairs, so such a pool does not farm the pot, but the 'every trade pays a tax' guarantee holds only for this one pool. Recorded as a design limitation of a hook-based tax on a free token, not as a change request.

**Reproduction**

Input: manager.initialize(PoolKey{currency0: IMD, currency1: PIMD, fee: 3000, tickSpacing: 60, hooks: IHooks(address(0))}, anyPrice); add liquidity; swap. Expected per the header: the trade is taxed. Actual: no beforeSwap/afterSwap runs for that pool and PimdHook.totalTaxed() is unchanged; by construction, since the PoolManager only calls the hook named in the key.

---

Judge's submission `fdd3c5d961775cf5cb2e74e52cdbaad3ffa74200652321bf8c751bbf04c9ed6d`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
