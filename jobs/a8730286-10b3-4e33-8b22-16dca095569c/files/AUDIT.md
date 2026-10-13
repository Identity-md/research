# Audit report

> X: https://x.com/IMDBlackout
>
> Full pre-launch audit of BLACKOUT v3.13 before its five contract launches on Robinhood Chain (4663). Source: identity-md-launches/launch-1544-blackout-swarmdesk-bootstrap-robinhood at commit 24bfb1d, built with the repo foundry.toml (solc 0.8.26, optimizer 200, cancun, viaIR false, bytecode_hash none). Read-only: no deploy, no broadcast, no source changes.
>
> Goal: find now every finding that the IMD launch audit panel (audit_flow, audit_permissions, audit_economics, audit_math and the audit_judge) would raise as medium, high or critical in any of the launches, so all fixes land in one change before anything is deployed. The contracts authenticate each other by creation-code hash, so any later code change forces every launch to be repeated.
>
> Scope, by launch:
> - M1: SwarmDesk (oracle-only swarm role, EIP-712 attested IMD answers, bind via ProjectFactory proofs).
> - M2: EndowmentEscrow (ownerless, one forward to the authenticated RewardPool).
> - M3: V4Market (Uniswap v4 hook, fee 12500, ETH pair, stepped launch tax 90/50/25 for 30 min, then exactly 1% to rewards plus a progressive sell surcharge).
> - M4 job A: Params, GameRegistry, RewardPool, FarmRewards, FarmCore, FarmItems, PackSale, StarterClaim.
> - M7 job B: FeeRouter, GridOperator, Season, FarmEngine, Economy, Enhancement, Civic, Billboards.
> Plus shared libraries (src/lib, ModuleCode, SwarmCode), keeper/ and tools/ only where they define on-chain inputs.
>
> Review each contract the way the launch panel does: call flow and state transitions, every authority and caller check, custody of ETH and tokens, economics and exploit profitability, arithmetic, rounding and bounds, liveness (what can get stuck, what can be griefed), deployability under the factory (static constructors, no external calls, empty-chain constructor rehearsal, size limits).
>
> Known and accepted by the requester (report only if you find a worse variant):
> - M-2 twin front-run of SwarmDesk.bind (docs/m2-trust-assumption.md): griefing only, mitigated by binding right after job A.
> - 17 reserved Params keys with no reader (docs/params-keys-v313.md).
> - Import finding b2ccff16: a regulator answer with a cap announcement rolls back while the bound market reports initializedAt() == 0; unreachable because the Desk binds after the token launch and caps are only proposed at age >= 30 days.
> - Future-block randomness is sequencer-influenced; no VRF claim.
>
> Deliver report.md:
> 1. Every finding with severity (critical/high/medium/low/info), contract and line, a concrete reproduction (Foundry test or exact call sequence), and whether the launch judge would likely block on it.
> 2. For each medium or higher: the minimal fix, and exactly which creation-code pins it changes (which of SwarmDesk, EndowmentEscrow, V4Market, GameRegistry, Params, ModuleCode.launchHash(0..13)).
> 3. A recommended single fix set, ordered, that clears all blocking findings with the fewest pin changes.
> 4. A list of low/info items to accept as documented, with a one-line justification each, written so it can be pasted into the launch objectives.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1544-blackout-swarmdesk-bootstrap-robinhood.git |
| Commit | `24bfb1d700159042da4b08262927727d37170540` |
| Job | `a8730286-10b3-4e33-8b22-16dca095569c` |
| Judged | 2026-10-13 11:51 UTC |
| Findings | 1 high · 1 medium · 7 low · 4 info |

Four agents audited the code as it is at `24bfb1d`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: V4Market.quote ignores the pool's 1.25% LP fee, so FeeRouter.executeBuys cannot clear its 1.5% band at launch depth: reward ETH (1% share + 90/50/25% launch tax) is stuck in FeeRouter with no other ex

`src/V4Market.sol:296`

```
        uint256 netInput = ethAmount - ethAmount * PROJECT_BPS / 10000;
        return Math.mulDiv(netInput, twap(), 1 ether);
```

Merged from audit_economics 38b02812 and audit_math e02a8283 (same root cause, same fix). quote() (src/V4Market.sol:296-297) prices a system buy as (ethAmount - 1% hook share) x twap(), and quoteSell() (src/V4Market.sol:477-478) mirrors it. The pool itself charges POOL_FEE = 12500 ppm (1.25%) on the same input, so at spot == TWAP and zero price impact the real output is 0.9875 x quote. FeeRouter.executeBuys (src/FeeRouter.sol:295-296) requires minOut >= quote x (10000 - SlippageBps)/10000 with SlippageBps bounded to 150 (Params.bounds and FeeRouter.MAX_SLIPPAGE_BPS), executePotBuys and V4Market.sell/FeeRouter.executeSells use a literal 9850/10000. Only 0.25% (buys) / 0.15% (sells) is left for price impact plus spot-vs-TWAP deviation. The router refuses buys below min(rewardETH, 0.05 ETH) (src/FeeRouter.sol:291-292), and a 0.05 ETH exact-input buy has about 0.49% impact on a 10 ETH virtual reserve, so on the launch pool (10 ETH opening cap on 4663 per launch-v39.md line 184, poolBps 7000, i.e. roughly 7 ETH of virtual ETH depth) every executeBuys reverts InsufficientBalance (src/V4Market.sol:539-543) even in a perfectly calm market; it first clears above roughly 20 ETH of depth, and after that only while spot stays within about 0.2% of the 30-minute TWAP, i.e. never during a trend. rewardETH is decremented only by executeBuys (src/FeeRouter.sol:299); there is no owner, sweep or alternative path, and BuyBatch/MIN_BUY_AMOUNT are immutable, so the hook's 1% of every swap and the entire 90/50/25% launch tax (depositLaunchTax routes 100% to rewardETH) accumulate unconvertible from the first block. The regulator cannot widen the band (SlippageBps hi bound == current value 150; the sell side is a literal), and any regulator step below 125 bps makes buys impossible at every depth. Not an attacker finding: it is deterministic on the launch parameters, which is why it is rated high (certain occurrence, core reward flow dead, funds indefinitely stuck). The launch judge (audit_economics / audit_math) would block. Minimal fix (V4Market pin only, M3): in quote() apply netInput = netInput * (1_000_000 - poolFee) / 1_000_000 before the mulDiv, and in quoteSell() apply gross = gross * (1_000_000 - poolFee) / 1_000_000 before subtracting PROJECT_BPS, so SlippageBps covers only impact and deviation (verified: the attached proof fails on this code and passes with exactly the quote() change). Alternative (worse: changes ModuleCode.launchHash(6), Params and therefore every pin): raise MAX_SLIPPAGE_BPS and the SlippageBps bound to >= 300 and parameterise the 9850 literals. Recommended single fix set, ordered by pin cost: (1) this quote()/quoteSell() change [V4Market pin only]; (2) the SwarmDesk.bind market/token check from the next finding [SwarmDesk pin only]; (3) optionally batch the low module items (executeSells amount, retire caller check, lock walk bound, claimLottery lazy mint, vintage at) into one ModuleCode regeneration, or accept them as documented and leave every job A/B pin untouched.

**Reproduction**

test/scratch/QuoteLpFee.t.sol (attached as proof; `forge test --match-path test/scratch/QuoteLpFee.t.sol`). State: real v4 PoolManager (vendor/v4-core), the production V4Market code (only the bind proof replaced by a direct setter), pool initialised at sqrtPriceX96 = 2^96, one full-range position with liquidity 10e18 (virtual reserves 10 ETH / 10 tokens), no trades, +60 minutes so twap() == spot(). Input: router.depositBaseFee{value: 0.1 ether}(); q = hook.quote(0.05 ether); router.executeBuys(0.05 ether, q * 9850 / 10000). Expected: the smallest allowed reward buy at the widest allowed slippage executes on a calm pool (received >= minOut, rewardETH 0.1 -> 0.05 ETH). Actual: revert InsufficientBalance from V4Market.unlockCallback (tokenDelta ~0.048644e18 < minOut 0.048757e18: 0.0495 ETH input x 0.9875 pool fee = 0.048881 ETH swapped into 10/10 reserves yields 10 x 0.048881 / 10.048881). rewardETH stays 0.1 ether with no other exit. Cross-check: test/V4Integration.t.sol passes the same call only because it seeds 1000 ETH of liquidity (impact 0.005%). With the one-line quote() fix the same test passes (verified by patching and restoring src/V4Market.sol).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;
import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {V4Market, IHookRouter, IHookParams} from "src/V4Market.sol";
import {FeeRouter} from "src/FeeRouter.sol";
import {RewardPool} from "src/RewardPool.sol";
import {Params} from "src/Params.sol";
import {IV4PoolManager, PoolKey, SwapParams} from "src/interfaces/IV4.sol";
import "src/lib/Errors.sol";

struct LiquidityParams {
    int24 tickLower;
    int24 tickUpper;
    int256 liquidityDelta;
    bytes32 salt;
}

interface RealManager is IV4PoolManager {
    function initialize(PoolKey memory, uint160) external returns (int24);
    function modifyLiquidity(PoolKey memory, LiquidityParams memory, bytes calldata) external returns (int256, int256);
    function sync(address) external;
}

contract QuoteToken is ERC20 {
    constructor() ERC20("T", "T") {
        _mint(msg.sender, 1e27);
    }
}

/// Minimal registry graph: token, params, market (the hook), FeeRouter as role 6, RewardPool as role 0.
contract QuoteRegistry {
    address public token;
    address public params;
    address public market;
    mapping(uint256 => address) public registeredModule;

    constructor(address t, address p, address m) {
        token = t;
        params = p;
        market = m;
    }

    function set(uint256 role, address a) external {
        registeredModule[role] = a;
    }

    function module(uint256 role) external view returns (address a) {
        a = registeredModule[role];
        require(a != address(0), "unset");
    }

    function launchTime() external view returns (uint256) {
        return block.timestamp - 1 days;
    }

    function freeRoot() external pure returns (bytes32) {
        return bytes32(uint256(1));
    }

    function starterRoot() external pure returns (bytes32) {
        return bytes32(uint256(1));
    }

    function snapshotBlock() external pure returns (uint256) {
        return 1;
    }

    function endowment() external pure returns (uint256) {
        return 0;
    }
}

/// The real hook with real flag validation; only the bind proof is replaced by a direct setter so the
/// test needs no Desk / ProjectFactory. quote(), buy() and unlockCallback() are the production code.
contract QuoteHook is V4Market {
    constructor(address manager_, address token_, address launcher_, address factory_, address desk_, bytes32 h)
        V4Market(manager_, token_, 12500, 60, launcher_, factory_, desk_, h)
    {}

    function bindForTest(address router, address p) external {
        fees = IHookRouter(router);
        params = IHookParams(p);
    }
}

/// V4Market.quote() prices a system buy at TWAP minus only the hook's 1% share and ignores the pool's own
/// 12500 ppm (1.25%) LP fee. FeeRouter.executeBuys allows at most SlippageBps = 150 below the quote, so at a
/// flat price only 0.25% is left for price impact: the smallest allowed reward buy (0.05 ETH) reverts on a
/// pool of the launch's depth (10 ETH opening cap on 4663). Expected: a calm pool with spot == TWAP converts
/// reward ETH inside the documented 1.5% band. Actual: InsufficientBalance from the hook's unlockCallback,
/// and rewardETH has no other exit. Passes once quote() nets the pool fee out of the input.
contract QuoteLpFeeTest is Test {
    RealManager internal manager;
    QuoteHook internal hook;
    FeeRouter internal router;
    QuoteToken internal token;
    RewardPool internal pool;

    function setUp() public {
        vm.warp(1_800_000_000);
        vm.deal(address(this), 10000 ether);
        manager = RealManager(address(new PoolManager(address(this))));
        token = new QuoteToken();
        Params params = new Params(address(this), 200, 1 ether);
        bytes32 h = keccak256("config");
        bytes memory code = abi.encodePacked(
            type(QuoteHook).creationCode,
            abi.encode(address(manager), address(token), address(this), address(0xf), address(0xd), h)
        );
        bytes32 codeHash = keccak256(code);
        bytes32 salt;
        for (uint256 i;; ++i) {
            salt = bytes32(i);
            address target = vm.computeCreate2Address(salt, codeHash, address(this));
            if (uint160(target) & 0x3fff == 0x10cc) break;
        }
        hook = new QuoteHook{salt: salt}(address(manager), address(token), address(this), address(0xf), address(0xd), h);
        QuoteRegistry registry = new QuoteRegistry(address(token), address(params), address(hook));
        router = new FeeRouter(address(registry));
        pool = new RewardPool(address(registry));
        registry.set(0, address(pool));
        registry.set(2, address(this));
        registry.set(4, address(this));
        registry.set(6, address(router));
        hook.bindForTest(address(router), address(params));
        manager.initialize(hook.key(), uint160(1 << 96));
        // Full-range position with virtual reserves of 10 ETH and 10 tokens (price 1:1), the launch's scale.
        manager.unlock(abi.encode(uint8(0), uint256(10 ether)));
        vm.warp(vm.getBlockTimestamp() + 60 minutes);
    }

    receive() external payable {}

    function unlockCallback(bytes calldata data) external returns (bytes memory) {
        require(msg.sender == address(manager));
        (uint8 action, uint256 amount) = abi.decode(data, (uint8, uint256));
        int256 delta;
        if (action == 0) {
            (delta,) =
                manager.modifyLiquidity(hook.key(), LiquidityParams(-887220, 887220, int256(amount), bytes32(0)), "");
        } else {
            delta = manager.swap(
                hook.key(),
                SwapParams(
                    action == 1,
                    -int256(amount),
                    action == 1 ? 4295128740 : 1461446703485210103287273052203988822378723970341
                ),
                ""
            );
        }
        int128 a = int128(delta >> 128);
        int128 b = int128(delta);
        if (a < 0) manager.settle{value: uint256(-int256(a))}();
        else if (a > 0) manager.take(address(0), address(this), uint256(uint128(a)));
        if (b < 0) {
            manager.sync(address(token));
            token.transfer(address(manager), uint256(-int256(b)));
            manager.settle();
        } else if (b > 0) {
            manager.take(address(token), address(this), uint256(uint128(b)));
        }
        return abi.encode(delta);
    }

    /// The smallest reward buy the router accepts (MIN_BUY_AMOUNT) at the widest slippage the router allows.
    function testMinimumRewardBuyClearsAtFlatPriceOnLaunchDepth() public {
        router.depositBaseFee{value: 0.1 ether}();
        assertEq(hook.twap(), hook.spot(), "calm pool: TWAP equals spot");
        uint256 q = hook.quote(0.05 ether);
        uint256 minOut = q * (10000 - 150) / 10000;
        uint256 before_ = token.balanceOf(address(pool));
        uint256 received = router.executeBuys(0.05 ether, minOut);
        assertGe(received, minOut);
        assertEq(token.balanceOf(address(pool)) - before_, received);
        assertEq(router.rewardETH(), 0.05 ether);
    }
}
```

### 2. Medium: SwarmDesk.bind never checks registry.market()/registry.token(): a pinned-code twin registry naming a foreign market or token captures the Desk and permanently freezes the hook's ETH fees or the escrow

`src/SwarmDesk.sol:201`

```
        if (_predictRegistry(r, p, registryLaunch, registryIndex, registryCode) != candidate) revert InvalidProof();
```

From audit_permissions 08cbad44, reproduced. bind (src/SwarmDesk.sol:194-202) proves the candidate's creation code, factory, keccak(starterRoot, freeRoot, snapshotBlock, endowment) and Params, and _predictRegistry (src/SwarmDesk.sol:223-226) only feeds r.token() and r.market() into the CREATE2 prediction: whatever token and market the twin was constructed with are accepted. docs/m2-trust-assumption.md section 3 row "Change the token or the pool: No ... The twin has to reuse them" is therefore not what the code enforces, and the accepted M-2 (griefing only, funds stay under pinned game rules) has two strictly worse variants with identical preconditions (a paid factory launch of the pinned Params + GameRegistry with the public roots after job A, and winning the race to bind). (a) Foreign market: the Desk binds a registry whose market is an attacker address. V4Market.bindFeeRouter then can never succeed for any router, because _routerMarketValid (src/V4Market.sol:142, 210-212) needs r.market() == hook while _canonical (src/V4Market.sol:152, 189-191) needs Desk.registry() == r; flushFees (src/V4Market.sol:195) reverts NotConfigured forever and every wei of heldBase/heldSellTax/heldLaunchTax (including the whole 90/50/25% launch-window tax) is frozen in the ownerless hook, whose receive() only accepts the manager. The bound game's GameRegistry.launchTime(), PackSale readiness and FeeRouter.market() (zapBuy sends player ETH to it, executeSells approves tokens to it) are attacker-controlled. (b) Foreign token: EndowmentEscrow.forward reads r.token() of the bound registry (src/EndowmentEscrow.sol:84-86), sees balance 0 and reverts InsufficientBalance; since the Desk is bound (AlreadyDone) no other registry can ever be forwarded, so the full 200,000,000e18 endowment (20% of supply) is locked in the ownerless escrow forever and the hook cannot bind either (r.token() != token). Severity: same low likelihood as the accepted M-2 (sequencer chain, keeper binds right after job A) but the impact changes from griefing to permanent loss of the endowment / fee stream, and the fix is one check on the only pin not yet launched, so the launch judge is likely to block. Minimal fix (SwarmDesk pin only, M1): after proving r in bind, require that r.market() is a launch hook of this Desk and that its token is the registry's token: `IBoundHook h = IBoundHook(r.market()); if (h.desk() != address(this) || h.token() != r.token() || h.gameConfigHash() != binding.gameConfigHash) revert InvalidProof();` (V4Market already exposes desk(), token() and gameConfigHash() as immutables; an EOA market reverts on the staticcall, which is the desired outcome). Pins changed: SwarmDesk only; EndowmentEscrow, V4Market, GameRegistry, Params and ModuleCode.launchHash(0..13) untouched. Also correct the "Change the token or the pool" row of docs/m2-trust-assumption.md. Pin impact of any module (job A/B) source fix: tools/pin_module_code.py regenerates ModuleCode.launchHash(role); ModuleCode is compiled into GameRegistry and EndowmentEscrow, so the GameRegistry creation hash (SwarmCode.REGISTRY_*) changes, which changes SwarmDesk and EndowmentEscrow (SwarmCode) and V4Market (embeds type(GameRegistry).creationCode). A module fix therefore regenerates every pin (M1..M7). A fix confined to SwarmDesk changes only the SwarmDesk pin (M1; the Escrow and hook take the Desk as an address, not code). A fix confined to V4Market changes only the V4Market pin (M3; nothing pins the hook code).

**Reproduction**

test/scratch/Proof_08cbad446c1c.t.sol (attached; `forge test --match-path test/scratch/Proof_08cbad446c1c.t.sol`): both tests fail on this code with "next call did not revert as expected". State: SwarmDesk deployed with factory F and gameConfigHash H = keccak(starterRoot, freeRoot, 23_000_000, 200_000_000e18); Params deployed through F at (1,0) with (desk, 200, 1e18). Input 1: attacker deploys through F at (1,1) the pinned GameRegistry creation code with constructor (realToken, params, market = attacker EOA, roots/snapshot/endowment matching H, F) and calls desk.bind(twin, GameRegistry.creationCode, Params.creationCode, 1, 1, 1, 0). Expected: revert (InvalidProof or a failed hook probe). Actual: bind succeeds, desk.registry() == twin, Bound emitted. Input 2: same with token = foreign ERC20 and the escrow holding 200,000,000e18 real tokens; bind succeeds; with a pinned RewardPool registered at (1,2), escrow.forward(twin, 1, 1, registryCode, 1, 2, poolCode) reverts InsufficientBalance and the escrow balance stays 200,000,000e18 with no remaining exit.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {SwarmDesk} from "src/SwarmDesk.sol";
import {Params} from "src/Params.sol";
import {GameRegistry} from "src/GameRegistry.sol";
import {EndowmentEscrow} from "src/EndowmentEscrow.sol";
import {RewardPool} from "src/RewardPool.sol";
import "src/lib/Errors.sol";

/// @dev Minimal stand-in for the IMD ProjectFactory: CREATE2 over (launchNumber, index) with a launch record.
contract ScratchFactory {
    mapping(uint64 => bool) public isRecorded;

    function predictContract(uint64 launchNumber, uint256 index, bytes calldata initCode)
        external
        view
        returns (address)
    {
        return address(
            uint160(
                uint256(
                    keccak256(
                        abi.encodePacked(
                            bytes1(0xff), address(this), keccak256(abi.encode(launchNumber, index)), keccak256(initCode)
                        )
                    )
                )
            )
        );
    }

    function deploy(uint64 launchNumber, uint256 index, bytes memory initCode) external returns (address result) {
        isRecorded[launchNumber] = true;
        bytes32 salt = keccak256(abi.encode(launchNumber, index));
        assembly ("memory-safe") {
            result := create2(0, add(initCode, 32), mload(initCode), salt)
        }
        require(result != address(0), "create2");
    }
}

contract ScratchToken {
    mapping(address => uint256) public balanceOf;
    uint256 public totalSupply;

    function mint(address to, uint256 amount) external {
        balanceOf[to] += amount;
        totalSupply += amount;
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        return true;
    }
}

/// @notice SwarmDesk.bind proves the registry's code, factory, roots, snapshot, endowment and Params, but never
/// looks at `registry.market()` or `registry.token()`. A byte-identical "twin" registry that names a foreign
/// market (or token) therefore captures the Desk. The launch hook (V4Market) can then never bind a FeeRouter
/// (`_routerMarketValid` / `_canonical` cannot both hold), so every ETH fee it collects is frozen, and with a
/// foreign token the EndowmentEscrow can never forward the endowment. Both tests expect `bind` to reject such a
/// registry; they fail on the current code and pass once `bind` checks the market/token against the hook.
contract DeskBindForeignMarketTest is Test {
    ScratchFactory internal factory;
    ScratchToken internal realToken;
    SwarmDesk internal desk;
    Params internal params;
    bytes32 internal constant STARTER_ROOT = keccak256("starter root");
    bytes32 internal constant FREE_ROOT = keccak256("free root");
    uint256 internal constant SNAPSHOT = 23_000_000;
    uint256 internal constant ENDOWMENT = 200_000_000 ether;
    address internal attacker = makeAddr("attacker");

    function setUp() public {
        vm.warp(1_800_000_000);
        factory = new ScratchFactory();
        realToken = new ScratchToken();
        uint256 policyWord = uint256(1) | (uint256(100) << 32) | (uint256(200) << 80) | (uint256(0.5 ether) << 128)
            | (uint256(200) << 224);
        desk = new SwarmDesk(
            makeAddr("intake"),
            makeAddr("delivery"),
            vm.addr(0x123456),
            address(realToken),
            bytes32("oracle.request@oracle-1"),
            policyWord,
            keccak256("event question"),
            keccak256("regulator question"),
            keccak256("event body"),
            keccak256("regulator body"),
            address(factory),
            keccak256(abi.encode(STARTER_ROOT, FREE_ROOT, SNAPSHOT, ENDOWMENT))
        );
        params = Params(
            factory.deploy(
                1, 0, bytes.concat(type(Params).creationCode, abi.encode(address(desk), uint256(200), uint256(1 ether)))
            )
        );
    }

    function _twin(address token, address market) internal returns (GameRegistry) {
        bytes memory args =
            abi.encode(token, address(params), market, STARTER_ROOT, FREE_ROOT, SNAPSHOT, ENDOWMENT, address(factory));
        return GameRegistry(factory.deploy(1, 1, bytes.concat(type(GameRegistry).creationCode, args)));
    }

    /// @dev A registry whose `market` is an attacker EOA, not the launch hook pinned to this Desk, must be rejected.
    function testBindRejectsRegistryWithForeignMarket() public {
        GameRegistry twin = _twin(address(realToken), attacker);
        vm.prank(attacker);
        // Any revert is acceptable: InvalidProof, or the failed hook probe on an address that is not the hook.
        vm.expectRevert();
        desk.bind(address(twin), type(GameRegistry).creationCode, type(Params).creationCode, 1, 1, 1, 0);
        assertEq(address(desk.registry()), address(0), "desk must stay unbound");
    }

    /// @dev A registry naming a foreign token must be rejected: once bound, the escrow holding the real
    /// endowment can never forward (its only exit reads `registry.token()`), freezing 20% of supply forever.
    function testBindRejectsRegistryWithForeignToken() public {
        ScratchToken foreign = new ScratchToken();
        GameRegistry twin = _twin(address(foreign), attacker);
        EndowmentEscrow escrow = new EndowmentEscrow(address(factory), address(factory), address(desk));
        realToken.mint(address(escrow), ENDOWMENT);

        vm.prank(attacker);
        // Any revert is acceptable: InvalidProof, or the failed hook probe on an address that is not the hook.
        vm.expectRevert();
        desk.bind(address(twin), type(GameRegistry).creationCode, type(Params).creationCode, 1, 1, 1, 0);

        // On the current code the bind above succeeds; the lines below then document the freeze.
        if (address(desk.registry()) == address(twin)) {
            address pool = factory.deploy(1, 2, bytes.concat(type(RewardPool).creationCode, abi.encode(address(twin))));
            twin.register(0, 1, 2, type(RewardPool).creationCode);
            vm.expectRevert(InsufficientBalance.selector);
            escrow.forward(
                address(twin), 1, 1, type(GameRegistry).creationCode, 1, 2, type(RewardPool).creationCode
            );
            assertEq(realToken.balanceOf(address(escrow)), ENDOWMENT, "endowment frozen in escrow");
            assertEq(realToken.balanceOf(pool), 0);
        }
    }
}
```

### 3. Low: FeeRouter.executeSells demands amount == min(total, maxSellBatch()) at inclusion time, so any pool movement between quote and inclusion reverts the keeper's team/heartbeat token sale (griefable by dus

`src/FeeRouter.sol:204`

```
        if (amount == 0 || amount != Math.min(total, m.maxSellBatch())) revert InvalidValue();
```

Merged from audit_flow e270020b (medium) and audit_math 05f18ede (info); reproduced, rated low. executeSells only accepts amount == min(teamTokens + heartbeatTokens, market.maxSellBatch()). On V4Market, maxSellBatch() = min(liquidity x sqrtPrice / 2^96 / 1000, twap() / 10) (src/V4Market.sol:482-488). Whenever virtual ETH reserves are below 100 ETH (true for the whole launch) the depth term binds and changes with every swap, so a keeper transaction built from sellBatchQuote() (keeper/keeper.mjs:240-241 does exactly quote-then-send) reverts InvalidValue if anyone moves the pool by one wei before inclusion; a third party can keep doing that with dust swaps for gas plus 2.25% of dust, stalling conversion of the team's 10% and the heartbeat-bounty token share. Why low and not medium: no funds are at risk, lastSell is not consumed by the revert so no cadence is lost, only team/heartbeat tokens are affected, and the keeper can defeat it without a code change by calling sellBatchQuote() and executeSells() from one contract in the same transaction. The launch judge is unlikely to block. Fix if desired (FeeRouter: ModuleCode.launchHash(6), cascading to every pin, so only worth batching with another module change): replace line 204 with `amount = Math.min(total, m.maxSellBatch()); if (amount == 0) revert InvalidValue();` and keep the minOut check against quoteSell(amount) (verified: the attached proof fails now with InvalidValue and passes with this change). Accept-as-documented wording otherwise: "executeSells must be quoted and executed against the same pool state (bundle both calls in one transaction); a mismatch reverts harmlessly and the keeper retries." Pin impact of any module (job A/B) source fix: tools/pin_module_code.py regenerates ModuleCode.launchHash(role); ModuleCode is compiled into GameRegistry and EndowmentEscrow, so the GameRegistry creation hash (SwarmCode.REGISTRY_*) changes, which changes SwarmDesk and EndowmentEscrow (SwarmCode) and V4Market (embeds type(GameRegistry).creationCode). A module fix therefore regenerates every pin (M1..M7). A fix confined to SwarmDesk changes only the SwarmDesk pin (M1; the Escrow and hook take the Desk as an address, not code). A fix confined to V4Market changes only the V4Market pin (M3; nothing pins the hook code).

**Reproduction**

test/scratch/Proof_e270020b696f.t.sol (attached; `forge test --match-path test/scratch/Proof_e270020b696f.t.sol`) fails on this code with InvalidValue(). State: FeeRouter wired to a minimal registry, Params (this, 200, 1e18), RewardPool, and a market whose maxSellBatch() = depth / 1000 like V4Market. Route 2,000,000e18 tokens (teamTokens = 200,000e18 > cap 1,000e18). (amount, minimum) = sellBatchQuote() -> amount == 1,000e18. Reduce depth by 1000 wei (one dust swap). executeSells(amount, minimum): expected the best available batch is sold; actual revert InvalidValue at src/FeeRouter.sol:204.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;
import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {FeeRouter} from "src/FeeRouter.sol";
import {RewardPool} from "src/RewardPool.sol";
import {Params} from "src/Params.sol";

contract GriefToken is ERC20 {
    constructor() ERC20("T", "T") {
        _mint(msg.sender, 1e27);
    }
}

/// Minimal registry graph: token, params, market, FeeRouter as role 6, RewardPool as role 0, this test as PackSale (4).
contract GriefRegistry {
    address public token;
    address public params;
    address public market;
    mapping(uint256 => address) public registeredModule;

    constructor(address t, address p, address m) {
        token = t;
        params = p;
        market = m;
    }

    function set(uint256 role, address a) external {
        registeredModule[role] = a;
    }

    function module(uint256 role) external view returns (address a) {
        a = registeredModule[role];
        require(a != address(0), "unset");
    }

    function launchTime() external view returns (uint256) {
        return block.timestamp - 1 days;
    }

    function freeRoot() external pure returns (bytes32) {
        return bytes32(uint256(1));
    }

    function starterRoot() external pure returns (bytes32) {
        return bytes32(uint256(1));
    }

    function snapshotBlock() external pure returns (uint256) {
        return 1;
    }

    function endowment() external pure returns (uint256) {
        return 0;
    }
}

/// Market whose sell batch cap depends on live pool depth, as V4Market.maxSellBatch does.
contract GriefMarket {
    IERC20 public token;
    uint256 public depth = 1_000_000 ether;
    uint256 public constant rate = 1_000_000 ether; // tokens per ETH

    constructor(address t) {
        token = IERC20(t);
    }

    function setDepth(uint256 v) external {
        depth = v;
    }

    function maxSellBatch() external view returns (uint256) {
        return depth / 1000;
    }

    function quoteSell(uint256 amount) public pure returns (uint256) {
        return amount * 1 ether / rate;
    }

    function quote(uint256 ethAmount) external pure returns (uint256) {
        return ethAmount * rate / 1 ether;
    }

    function buy(uint256, address) external payable returns (uint256) {
        return 0;
    }

    function sell(uint256 amount, uint256 minimum, address recipient) external returns (uint256 received) {
        token.transferFrom(msg.sender, address(this), amount);
        received = quoteSell(amount);
        require(received >= minimum, "minimum");
        (bool ok,) = recipient.call{value: received}("");
        require(ok);
    }

    receive() external payable {}
}

contract ExecuteSellsGriefTest is Test {
    GriefToken token;
    GriefMarket market;
    GriefRegistry registry;
    FeeRouter fees;

    function setUp() public {
        vm.warp(1_800_000_000);
        token = new GriefToken();
        market = new GriefMarket(address(token));
        vm.deal(address(market), 100 ether);
        Params params = new Params(address(this), 200, 1 ether);
        registry = new GriefRegistry(address(token), address(params), address(market));
        fees = new FeeRouter(address(registry));
        RewardPool pool = new RewardPool(address(registry));
        registry.set(0, address(pool));
        registry.set(2, address(this));
        registry.set(4, address(this)); // this test acts as PackSale
        registry.set(6, address(fees));
    }

    /// A keeper quotes the batch, then one dust trade moves pool depth before inclusion.
    /// Expected: the sale still executes for the best batch available at inclusion time.
    /// Actual on current code: executeSells reverts InvalidValue because amount must equal the live cap exactly.
    function testKeeperSaleSurvivesDepthNudge() public {
        token.transfer(address(fees), 2_000_000 ether);
        fees.routeTokens(2_000_000 ether); // teamTokens = 200,000e18 > maxSellBatch = 1,000e18
        (uint256 amount, uint256 minimum) = fees.sellBatchQuote();
        assertEq(amount, market.maxSellBatch());
        market.setDepth(market.depth() - 1000); // dust swap / LP change by a third party
        uint256 received = fees.executeSells(amount, minimum);
        assertGt(received, 0);
        assertGt(fees.credit(fees.team()), 0);
    }
}
```

### 4. Low: RewardPool.fundEndowment needs the immutable principal from unrecorded inflows only: a one-wei shortfall in the escrow remainder leaves available() == 0 forever and donate() cannot close it (only an u

`src/RewardPool.sol:68`

```
        if (balance < otherInflow || balance - otherInflow < principal) revert InsufficientBalance();
```

Merged from audit_flow ff821413 and audit_economics 448ac11f (same mechanism); reproduced. GameRegistry.endowment is immutable (200,000,000e18 for this launch, committed in the hook's and Desk's gameConfigHash before the token launch), and fundEndowment requires balance - otherInflow >= endowment. Every in-protocol inflow (donate, routeTokens, FarmCore charges, executeBuys before endowed) is added to otherInflow (src/RewardPool.sol:75, 92) and excluded, so if EndowmentEscrow.forward delivers less than the committed principal by any amount (platform split change, pool seeding different from the rehearsal), available() returns 0 for ever (src/RewardPool.sol:56), advanceEpoch reserves nothing and PackSale readiness fails; no in-protocol path repairs it. The only recovery is a plain ERC20 transfer of the shortfall to the pool, which the runbook does not mention. A launch-input risk rather than a code defect: launch-v39.md line 109-111 shows the fork remainder at +0.056% above principal. Judge unlikely to block. Accept-as-documented wording: "remainderTo must deliver >= 200,000,000e18; a shortfall is repaired by a plain token transfer to the RewardPool (not donate), after which fundEndowment is called." Code alternative (RewardPool: ModuleCode.launchHash(0), cascading): record the escrow-sourced amount in a dedicated path. Pin impact of any module (job A/B) source fix: tools/pin_module_code.py regenerates ModuleCode.launchHash(role); ModuleCode is compiled into GameRegistry and EndowmentEscrow, so the GameRegistry creation hash (SwarmCode.REGISTRY_*) changes, which changes SwarmDesk and EndowmentEscrow (SwarmCode) and V4Market (embeds type(GameRegistry).creationCode). A module fix therefore regenerates every pin (M1..M7). A fix confined to SwarmDesk changes only the SwarmDesk pin (M1; the Escrow and hook take the Desk as an address, not code). A fix confined to V4Market changes only the V4Market pin (M3; nothing pins the hook code).

**Reproduction**

test/scratch/JudgeChecks.t.sol testEndowmentShortfallCannotBeClosedByDonate (passes, i.e. the behaviour is observed). State: MockGameRegistry with endowment 200,000,000e18, fresh RewardPool. Transfer 200,000,000e18 - 1 to the pool. fundEndowment() -> InsufficientBalance. donate(1) succeeds but counts in otherInflow; fundEndowment() -> InsufficientBalance again; available() == 0. token.transfer(pool, 1) from any wallet -> fundEndowment() succeeds. Expected: a documented funding path for any shortfall; actual: only the raw transfer works.

### 5. Low: FarmCore.retire(address) has no caller check: anyone can retire another player's empty farm from the roster and force its re-commit

`src/FarmCore.sol:401`

```
    function retire(address p) external nonReentrant {
        _prepare(p);
```

From audit_flow f44deaf5, reproduced. retire takes an arbitrary player address, runs _prepare(p) (settle + roll + sync, i.e. a fresh re-commitment of p's configured weight) and removes p from the players enumeration; every other owner action in FarmCore is msg.sender-scoped. The on-chain game never iterates players (count/playerAt serve the UI and keepers), so the impact is a third party removing idle players from the public roster and the re-added-on-next-place churn; funds are unaffected. Judge unlikely to block. Fix (FarmCore: ModuleCode.launchHash(2), cascading to every pin; batch only): `if (msg.sender != p) revert Unauthorized();` at the top of retire. Accept-as-documented wording: "retire(p) is permissionless for empty farms; the roster is advisory and a retired player re-enters on the next place()." Pin impact of any module (job A/B) source fix: tools/pin_module_code.py regenerates ModuleCode.launchHash(role); ModuleCode is compiled into GameRegistry and EndowmentEscrow, so the GameRegistry creation hash (SwarmCode.REGISTRY_*) changes, which changes SwarmDesk and EndowmentEscrow (SwarmCode) and V4Market (embeds type(GameRegistry).creationCode). A module fix therefore regenerates every pin (M1..M7). A fix confined to SwarmDesk changes only the SwarmDesk pin (M1; the Escrow and hook take the Desk as an address, not code). A fix confined to V4Market changes only the V4Market pin (M3; nothing pins the hook code).

**Reproduction**

test/scratch/JudgeChecks.t.sol testAnyoneCanRetireAnotherFarm (passes, i.e. observed). BaseTest fixture: alice places one item and unplaces it (alice is in players, count == 1), advance one epoch. bob calls d.farm.retire(alice). Expected: Unauthorized. Actual: succeeds, d.farm.count() goes 1 -> 0 and Retired(alice) is emitted by bob's call.

### 6. Low: SwarmDesk._regulate clamps an out-of-range regulator key onto RepairHours instead of skipping it

`src/SwarmDesk.sol:416`

```
            Params.Key k = Params.Key(_clamp(key, 1, 45) - 1);
```

From audit_permissions ab4b472e, verified against the code. The regulator answer packs a key in the top byte of v[1..8]; key 0 means no change (line 414). Any key above 45 is clamped to 45 and decoded as Params.Key(44), which is RepairHours (the 45th and last enum member, src/Params.sol:52); the value bits are then clamped into the RepairHours bounds (4e18..8e18) and the +/-10% band and applied through params.set. A malformed or future key (e.g. a new recipe key added before the Params enum grows) silently moves the repair-cost parameter by up to 10% per day instead of being ignored. Attester-trusted and bounded, so low; judge unlikely to block. Fix (SwarmDesk pin only): `if (key == 0 || key > 45) continue;`. Accept-as-documented wording: "Out-of-range regulator keys clamp to RepairHours; the attester recipe emits only keys 1..45."

**Reproduction**

Call sequence: store a valid regulator-stream attestation (stream 1) whose v[1] = (uint256(0xff) << 248) | 8 ether, with Params.RepairHours at its default 6e18 and lastChanged more than 1 day old; call execute(1, answer). Expected: the unknown key 255 is ignored and RepairHours stays 6e18. Actual: _clamp(255, 1, 45) - 1 = 44 = Params.Key.RepairHours; target = _clamp(_clamp(8e18, 4e18, 8e18), 5.4e18, 6.6e18) = 6.6e18; params.set(RepairHours, 6.6e18, notice) executes and ParamChanged is emitted (arithmetic from src/SwarmDesk.sol:413-421 and src/Params.sol:140, 165-179).

### 7. Low: Economy._insert walks the district's sorted lock list without a bound: a district can be filled with ascending locks so that later locks of equal or smaller amount cost +4.5k gas per existing node

`src/Economy.sol:176`

```
        while (cursor != address(0) && locks[cursor].amount >= locks[p].amount) {
```

From audit_economics d8b7bf18, reproduced (the specialist's "descending" wording is inverted: ascending amounts give the attacker O(1) inserts because each new lock is larger than the head). lock() inserts the caller into a descending linked list by walking until a smaller lock is found. An attacker in fresh wallets of the target district (district = keccak(address) % 8) locking amounts A, A+1, A+2, ... pays a constant insert each time; a victim locking <= A then walks all N nodes at about 4,525 gas each (measured: 653,885 gas for an empty district vs 2,011,393 after 300 larger locks), so roughly 7,000 nodes exceed a 32M block. Cost to the attacker: N x lock minimum (farmDaily x 5 at 7 days) refundable after 7 days plus gas; the victim can bypass by locking more than the attacker's largest amount; only the optional lock/boost feature (Civic feature 4, disabled at launch) is affected. Judge unlikely to block. Fix (Economy: ModuleCode.launchHash(10), cascading; batch only): bound the walk (e.g. 32 steps then revert with a hint, or accept a caller-supplied insertion hint checked against both neighbours); districtStake reads only the top ten so a bounded prefix suffices. Accept-as-documented wording: "Lock insertion is unbounded per district; a flooded district can be bypassed by locking above the flood amount." Pin impact of any module (job A/B) source fix: tools/pin_module_code.py regenerates ModuleCode.launchHash(role); ModuleCode is compiled into GameRegistry and EndowmentEscrow, so the GameRegistry creation hash (SwarmCode.REGISTRY_*) changes, which changes SwarmDesk and EndowmentEscrow (SwarmCode) and V4Market (embeds type(GameRegistry).creationCode). A module fix therefore regenerates every pin (M1..M7). A fix confined to SwarmDesk changes only the SwarmDesk pin (M1; the Escrow and hook take the Desk as an address, not code). A fix confined to V4Market changes only the V4Market pin (M3; nothing pins the hook code).

**Reproduction**

test/scratch/JudgeChecks.t.sol testLockInsertionWalkGrowsWithEqualOrLargerLocks (passes, i.e. observed). BaseTest fixture with feature 4 enabled: one lock(15_000e18, 7) in an empty district costs 653,885 gas; after 300 wallets in alice's district each lock(15_000e18 + i, 7) in ascending order, alice's lock(15_000e18, 7) costs 2,011,393 gas. Expected: lock cost independent of other users' locks. Actual: +4,525 gas per existing equal-or-larger lock, unbounded.

### 8. Low: Season.claimLottery couples the 10% pot payout to an item mint that reverts when the winner's inventory is full, so the token share is blocked and forfeits to rollover after the claim window

`src/Season.sol:369`

```
        id = items().mint(msg.sender, k, r, true);
```

From audit_economics 3e388933, verified against the code. claimLottery pays the token share with _payPot and then calls FarmItems.mint in the same transaction; mint reverts InvalidValue when inventory[p] >= capacity(p) = 15 + 5 x expansions (src/FarmItems.sol:95), so a winner with a full inventory cannot collect the token share either until they free a slot or expand, and after the claim deadline rollover() moves the unclaimed 10% to the current pot. claimDistrict is unaffected (rewardPack commits a lazy receipt). Judge unlikely to block. Fix (Season: ModuleCode.launchHash(8), cascading; batch only): commit the item through PackSale.rewardPack like claimDistrict, or make the mint best-effort. Accept-as-documented wording: "A lottery winner must have inventory space to claim; the claim window is four weeks." Pin impact of any module (job A/B) source fix: tools/pin_module_code.py regenerates ModuleCode.launchHash(role); ModuleCode is compiled into GameRegistry and EndowmentEscrow, so the GameRegistry creation hash (SwarmCode.REGISTRY_*) changes, which changes SwarmDesk and EndowmentEscrow (SwarmCode) and V4Market (embeds type(GameRegistry).creationCode). A module fix therefore regenerates every pin (M1..M7). A fix confined to SwarmDesk changes only the SwarmDesk pin (M1; the Escrow and hook take the Desk as an address, not code). A fix confined to V4Market changes only the V4Market pin (M3; nothing pins the hook code).

**Reproduction**

Call sequence: winner w with inventory == capacity (15 items, no expansions) after finalize(week) set lotteryWon[week][w]; w calls claimLottery(week). Expected: pot[week] x 10 / 100 is paid regardless of inventory. Actual: revert InvalidValue from FarmItems.mint at src/FarmItems.sol:95 (the whole call reverts, lotteryClaimed stays false, potRemaining unchanged); after scrapping or unequipping one item the same call succeeds.

### 9. Low: FarmRewards._credit lets a later same-epoch scrap/award credit push the whole vintage slot's maturity timestamp forward, over-taxing the earlier credit by up to 6 hours of decay

`src/FarmRewards.sol:486`

```
        if (at > v.at || v.amount == 0) v.at = uint64(at);
```

From audit_math b6ce9ea5, verified against the code. One Vintage per epoch slot (e % 32) keeps a single `at`. Settlement credits use at = epoch end and never disagree, but scrap() (line 561) and award() (line 575) credit the current epoch with at = block.timestamp, so a second such credit in the same 6-hour epoch overwrites `at` with the later timestamp and the earlier amount's 7-day decay (20% -> 5%, taxBps line 491-493) restarts from it. Bounded to 6 hours of decay, i.e. at most about 54 bps extra claim tax on the earlier amount, only for players who scrap or win awards more than once per epoch. Judge unlikely to block. Fix (FarmRewards: ModuleCode.launchHash(1), cascading; batch only): keep the earlier timestamp (`if (v.amount == 0 || at < v.at) v.at = uint64(at)`), or key the slot by (epoch, kind). Accept-as-documented wording: "Scrap/award credits within one epoch share a vintage; the earlier credit matures up to 6 hours late (<= 54 bps extra claim tax)." Pin impact of any module (job A/B) source fix: tools/pin_module_code.py regenerates ModuleCode.launchHash(role); ModuleCode is compiled into GameRegistry and EndowmentEscrow, so the GameRegistry creation hash (SwarmCode.REGISTRY_*) changes, which changes SwarmDesk and EndowmentEscrow (SwarmCode) and V4Market (embeds type(GameRegistry).creationCode). A module fix therefore regenerates every pin (M1..M7). A fix confined to SwarmDesk changes only the SwarmDesk pin (M1; the Escrow and hook take the Desk as an address, not code). A fix confined to V4Market changes only the V4Market pin (M3; nothing pins the hook code).

**Reproduction**

Arithmetic from the code: farm p with pending == 0 in epoch E; at time T core.scrap() credits A = 1000e18 via _credit(p, A, E, T): slot E % 32 gets at = T. At T + 5h (still E) a second scrap credits B = 1e18: at > v.at so v.at = T + 5h, amount = A + B. At T + 7d the player claims A. Expected: A is 7 days old, taxBps = 500, tax = 50e18. Actual: the sweep at line 503 does not mature the slot (T + 7d < T + 5h + 7d); line 520 charges taxBps(7d - 5h) = 2000 - 1500 x 163h / 168h = 545 bps, tax = 54.5e18; the player receives 4.5e18 less than the documented schedule.

### 10. Info: V4Market rejects every exact-output swap (amountSpecified >= 0) in beforeSwap and afterSwap; undocumented for integrators

`src/V4Market.sol:410`

```
        if (p.amountSpecified >= 0) revert InvalidValue();
```

From audit_flow 35091f46, verified against the code (lines 410 and 433). The pool supports exact-input swaps only, for all users; the system buy/sell paths are exact-input too. Deliberate (the BeforeSwapDelta is taken from the specified ETH input) and asserted by test/Market.t.sol, but not stated in launch-v38.md, docs/api-v35.md or the launch objective, and wallets or aggregators that quote "buy exactly N tokens" fail against the launch pool. No code change recommended. Accept-as-documented wording: "The launch pool accepts exact-input swaps only; exact-output swaps revert InvalidValue."

**Reproduction**

Call PoolManager.swap on the launch pool with SwapParams(zeroForOne = true, amountSpecified = +1e18, sqrtPriceLimitX96 = MIN + 1) via any router: beforeSwap reverts InvalidValue at src/V4Market.sol:410; oneForZero exact-output is rejected the same way (afterSwap, line 433). Expected by an integrator: a quoted exact-output buy; actual: revert.

### 11. Info: spot() hard-reverts outside (0, 1e40], which would freeze every swap and the TWAP if the pool price ever reached those bounds (unreachable for this launch)

`src/V4Market.sol:243`

```
        if (price == 0 || price > 1e40) revert InvalidValue();
```

From audit_math 7cdcbcd2, verified against the code. spot() is called from beforeSwap, afterSwap and both unlock callbacks, so a price above 1e22 tokens per ETH or below 1e-18 tokens per ETH makes every swap revert, including the one that would move the price back. With a 1e9 token supply and full-range liquidity the upper bound needs less than 1e5 wei of ETH in the pool, which the 1.25% LP fee and the sell surcharge make unreachable; the lower bound is likewise unreachable. No pin change recommended. Accept-as-documented wording: "spot() refuses prices outside (1e-18, 1e22] tokens/ETH; unreachable for a 1e9-supply pool with full-range liquidity."

**Reproduction**

With test/mocks/MockV4Manager.sol: manager.setSqrt(uint160((1 << 96) * 1e11)) gives price 1e40 and spot() returns it; manager.setSqrt(uint160((1 << 96) * 1e11 + (1 << 96) / 1e11)) gives price > 1e40 and spot() reverts InvalidValue, after which manager.invokeBefore(hook, SwapParams(true, -1 ether, 0)) reverts InvalidValue for any swap.

### 12. Info: Trust assumption to document: the Desk's oracle signer, intake and delivery addresses are fixed at construction with no rotation path

`src/SwarmDesk.sol:137`

```
    ) OracleAttestationConsumer(signer_) {
```

From audit_permissions 25ec9ccc, verified: OracleAttestationConsumer offers _setOracleSigner (src/oracle/OracleAttestation.sol:179) but SwarmDesk never calls it, and config.intake / config.delivery are written only in the constructor. If the IMD attester key is rotated or the Intake contract replaced, every submit() fails BadSignature and every delivery fails Unauthorized for the life of the game: no plans (GridOperator falls back to its fixed table), no Params changes, no feature notices, no pack pauses. A deliberate ownerless design, not a bypass; it belongs in the launch objectives as a platform dependency. If resilience is wanted, point signer_ at the oracle's ERC-1271 signer registry instead of a bare key (no code change).

**Reproduction**

Sign a valid attestation for the Desk's domain with any key other than oracleSigner and call submit(a, sig): reverts BadSignature. Grep src/SwarmDesk.sol for _setOracleSigner: no call site; no function writes config.intake or config.delivery. Expected if rotation were intended: an update path; actual: none, by design.

### 13. Info: Between job A and job B every SwarmDesk.execute reverts NotConfigured (roles 7/10/11/12 unregistered), so attested answers accepted in that window are consumed but never executable

`src/SwarmDesk.sol:393`

```
        GridOperator grid = GridOperator(registry.module(7));
```

From audit_permissions c7b99644, verified against the code. The runbook binds the Desk right after job A. Until job B registers GridOperator (7), Economy (10), Enhancement (11) and Civic (12), _event reverts at registry.module(7) (GameRegistry.module reverts NotConfigured for an empty role, src/GameRegistry.sol:62-65) and _regulate at module(12)/(11)/(10); _accept has already consumed the attestation's requestId and marked the slot accepted, and once the slot ends execute returns AnswerIgnored. No funds at risk and the game cannot start before job B. Accept-as-documented wording: "Attested answers accepted between job A and job B are not executable; job B is launched in the same session."

**Reproduction**

State: Desk bound to a registry with roles 0..5 registered only. Store any valid event-stream attestation via submit, then call execute(0, answer). Expected per design: a plan submitted for epochs base+1..base+2. Actual: revert NotConfigured from registry.module(7) inside _event (src/SwarmDesk.sol:393); the requestId is already consumed, and after the 6-hour slot execute emits AnswerIgnored(…, 2).

---

Judge's submission `6bad4d42d4bdeb3b85bed704c5c0c8ed71496cf43a6043901eb0fb5f9bddfee8`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
