# Audit report

> Audit github.com/MirakoolDev/basketoor at commit b14b3cc4facaa197c319db2ed6596f537b7eebd1. Scope: contracts/src/Basketoor.sol and contracts/src/adapters/AerodromeCLAdapter.sol (mocks, scripts, keeper and web are out of scope). Read contracts/AUDIT.md first: it has the roles, intended invariants and known limitations. Look hardest at: (1) escrow and ERC-4626 savings-vault accounting: principal vs idle vs shares, yield fee on withdraw/cancel, and whether the contract's loose USDC can drift from zero; (2) updatePlan resizing the budget (pull vs refund) and fee snapshots per plan; (3) executeDue/executeMany: Chainlink staleness and price bounds, the minOut derivation for 8-decimal stock tokens vs 18-decimal crypto, skipped legs, and fees charged only on USDC actually spent; (4) AerodromeCLAdapter: the uniswapV3SwapCallback can only be paid by the active pool (transient storage), partial fills, and the sqrt price limits; (5) owner powers (adapter, feeds, vault) and whether a plan owner can always cancel and exit without the keeper or owner.

| | |
|---|---|
| Repository | https://github.com/MirakoolDev/basketoor.git |
| Commit | `b14b3cc4facaa197c319db2ed6596f537b7eebd1` |
| Job | `9a020ffc-afdb-41b8-b89d-89c302c28bce` |
| Judged | 2026-11-25 09:33 UTC |
| Findings | 5 medium · 7 low · 3 info |

Four agents audited the code as it is at `b14b3cc`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Savings plans are funded to the exact wei, so ERC-4626 rounding closes them without making the last funded buy (or reverts the whole keeper batch)

`contracts/src/Basketoor.sol:402`

```
if (_value(p) < per + _feeFor(per, p.feeBps, p.minFee)) {
```

Where: Basketoor._execute budget check (line 402) with _value (551-555), _take (558-566), _put (569-577), createPlan (182-185) and updatePlan (214-227). createPlan/updatePlan fund exactly (perBuy + fee) x buys. For a savings plan that amount goes through vault.deposit (shares rounded down), _value reads it back with previewRedeem (rounded down), each run calls vault.withdraw twice (shares burned rounded up) and re-deposits the USDC of skipped legs. At any share price other than exactly 1 each step can cost the plan 1 wei and nothing in the budget pays for it; only yield accrued in the meantime hides it. Two outcomes on the last funded buy. (a) value is short by dust: the check on line 402 is true and the run calls _close(id,false) instead of buying. The user is refunded, but the buy they paid for never happens; a one-buy savings plan (first buy is due at creation, before any yield) never buys at all. Intended invariants 1 (planValue >= principal absent vault losses) and 5 (the budget funds exactly the remaining buys) do not hold: planValue is principal - 1 right after createPlan with no loss. (b) value equals the budget exactly: the check passes, _take(p, per) burns rounded-up shares and _take(p, fee) on line 421 then asks the vault for more than the plan has left; the vault reverts and with it executeDue for every plan in the batch. AUDIT.md known issue 4 names this revert "e.g. after a vault loss"; no loss is needed and any user can open such a plan. Fix that keeps the budget rule and fees: make the last-buy path tolerant of share rounding. For example require only value >= per before buying and charge fee = min(fee, what the plan still holds), and in _take use redeem(min(p.shares, previewWithdraw(amount))) and account the assets actually returned; or add a few wei of rounding allowance per remaining withdraw when sizing a savings plan's deposit.

**Reproduction**

Run from contracts/: forge test --match-path test/scratch/ProofSavingsRounding.t.sol (the attached file; both tests fail on this commit). State: the savings vault (OpenZeppelin ERC4626, the repo's MockSavingsVault) holds a third party's 1,000 USDC and has received accrueAmount(111_111_111), share price 1.111111. Default fees. Input 1: alice createPlan("p", [stock], [10e6], 1 days, maxBuys=1, savings=true) pulls 10,100,000; keeper executeDue(10) in the same block. Expected: one 10 USDC buy, buysDone = 1, stock delivered. Actual: plan closed, buysDone = 0, no stock ("the one funded buy never ran: 0 != 1"). Input 2: same vault, maxBuys=3, runs at t0, t0+1d, t0+2d with fresh prices and no vault yield in between. Expected buysDone = 3. Actual 2 ("last funded buy was dropped: 2 != 3"). Case (b), run separately as a local Foundry test: a third party deposits 1,999,999 wei of USDC and 1,000,000 wei of yield arrives (share price exactly 1.5); bob opens a non-savings plan, alice a one-buy savings plan of [10e6, 10e6] (planValue = 20,100,000 exactly); keeper executeDue(50). Expected: both plans run. Actual: revert ERC4626ExceededMaxWithdraw(basketoor, 100000, 99999) (selector 0xfe9cceec) from _take(p, fee); bob's buysDone stays 0.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {IERC4626} from "@openzeppelin/contracts/interfaces/IERC4626.sol";

import {Basketoor} from "src/Basketoor.sol";
import {ISwapAdapter} from "src/interfaces/ISwapAdapter.sol";
import {MockUSDC, MockStock, MockFeed, MockSwapAdapter, MockSavingsVault} from "src/mocks/Mocks.sol";

/// Savings plans: ERC-4626 share rounding leaves planValue 1 wei under the budget, so the budget check in
/// _execute closes the plan ("ran out of budget") instead of doing the buy the user paid for.
contract ProofSavingsRounding is Test {
    Basketoor b;
    MockUSDC usdc;
    MockSwapAdapter venue;
    MockSavingsVault vault;
    MockStock stock;
    MockFeed feed;

    address admin = makeAddr("admin");
    address treasury = makeAddr("treasury");
    address keeper = makeAddr("keeper");
    address alice = makeAddr("alice");
    uint256 t0 = 1_760_000_000;

    function setUp() public {
        vm.warp(t0);
        vm.startPrank(admin);
        usdc = new MockUSDC();
        venue = new MockSwapAdapter(admin);
        b = new Basketoor(usdc, ISwapAdapter(address(venue)), treasury, admin);
        vault = new MockSavingsVault(usdc);
        stock = new MockStock("Apple", "AAPLc", 8, admin);
        feed = new MockFeed(8, 180e8, admin);
        stock.setMinter(address(venue));
        venue.setFeed(address(stock), feed);
        b.setAsset(address(stock), feed, true);
        b.setKeeper(keeper, true);
        b.setSavingsVault(IERC4626(address(vault)));
        vm.stopPrank();

        // The vault already has another depositor and has earned yield: share price 1.111111, not 1.
        usdc.mint(address(this), 1000e6);
        usdc.approve(address(vault), 1000e6);
        vault.deposit(1000e6, address(this));
        vault.accrueAmount(111_111_111);

        usdc.mint(alice, 10_000e6);
        vm.prank(alice);
        usdc.approve(address(b), type(uint256).max);
    }

    function _create(uint32 buys) internal returns (uint256) {
        address[] memory tokens = new address[](1);
        tokens[0] = address(stock);
        uint256[] memory amounts = new uint256[](1);
        amounts[0] = 10e6;
        vm.prank(alice);
        return b.createPlan("p", tokens, amounts, 1 days, buys, true);
    }

    function test_singleBuySavingsPlanActuallyBuys() public {
        uint256 id = _create(1); // pulls 10.10 USDC: one $10 buy + $0.10 fee
        vm.prank(keeper);
        b.executeDue(10);
        (Basketoor.Plan memory p,) = b.getPlan(id);
        assertEq(p.buysDone, 1, "the one funded buy never ran");
        assertGt(stock.balanceOf(alice), 0, "no stock delivered");
    }

    function test_threeBuySavingsPlanDoesAllThreeBuys() public {
        uint256 id = _create(3); // pulls 30.30 USDC
        for (uint256 k; k < 3; ++k) {
            vm.warp(t0 + k * 1 days);
            vm.prank(admin);
            feed.setPrice(180e8);
            vm.prank(keeper);
            b.executeDue(10);
        }
        (Basketoor.Plan memory p,) = b.getPlan(id);
        assertEq(p.buysDone, 3, "last funded buy was dropped");
    }
}
```

### 2. Medium: Vault calls are made bare in the keeper loop and in close: a savings vault that cannot pay out (or take deposits) reverts the whole batch, non-savings plans included, and blocks cancelPlan

`contracts/src/Basketoor.sol:561`

```
uint256 burned = p.vault.withdraw(amount, address(this), address(this));
```

Where: Basketoor._take (line 561, vault.withdraw), _put (line 573, vault.deposit, reached from line 417 when a leg was skipped) and _close (line 482, vault.redeem), reached from _execute, updatePlan and cancelPlan. None of these calls is isolated. (1) If the plan's ERC-4626 vault refuses the withdrawal (paused, or a lending vault at full utilisation: maxWithdraw < amount), _execute reverts and with it the whole executeDue/executeMany transaction. duePlans() returns that plan again on every call, so plans that never opted into savings stop being executed until the keeper switches to hand-built executeMany lists. (2) _execute withdraws the whole buy before pricing any leg and re-deposits what was skipped; if the vault is not taking deposits (maxDeposit = 0, cap full) while withdrawals are open, any run of a savings plan with one skipped leg (routine: a stale stock price) reverts the batch the same way. (3) cancelPlan and updatePlan's refund go through the same vault calls, so a savings plan owner cannot exit while the vault is illiquid. AUDIT.md says a plan owner "can always cancel and receive everything unspent ... No dependency on the keeper or the owner to exit"; for savings plans that holds only while the owner-chosen vault is liquid, and p.vault is fixed for the life of the plan (setSavingsVault affects new plans only). This is a batch-revert trigger beside known issues 4 and 5 that needs only ordinary vault state. Fix that keeps the design: isolate each plan in the keeper loop (external self-call in try/catch, or check maxWithdraw/maxDeposit first and skip the plan with an event); when a re-deposit fails keep the remainder as p.idle (_value and _close already sum idle + shares, _take would need to draw idle first); on cancel, if redeem is not possible, pay out p.idle and transfer the plan's vault shares to the owner.

**Reproduction**

Run from contracts/: forge test --match-path test/scratch/ProofVaultBlocksBatch.t.sol (attached; fails with "no liquidity"). State: bob has a savings plan createPlan("p", [stock], [10e6], 1 days, 2, savings=true), alice the same plan with savings=false; both due. The vault then refuses withdrawals (IlliquidVault.setFrozen(true)). Input: keeper executeDue(10). Expected: bob's plan is skipped or deferred and alice's plain-escrow plan buys (buysDone = 1). Actual: the call reverts with the vault's error and alice's buysDone stays 0. Also run as local Foundry tests on an OpenZeppelin ERC4626 vault: (deposit side) alice has a savings plan [AAPLc 100e6] x5, bob a non-savings plan [WETH 100e6] x5; 27 hours later AAPLc's price is stale, WETH's is fresh and the vault's maxDeposit returns 0: executeDue(25) reverts with ERC4626ExceededMaxDeposit(basketoor, 100000000, 0) (0x79012fb2) from the _put on line 417 and bob's buy does not run. (exit side) with maxRedeem/maxWithdraw returning 0, alice.cancelPlan(id) reverts with ERC4626ExceededMaxRedeem(basketoor, 502500000, 0) (0xb94abeec) and updatePlan down to one buy reverts as well; the plan stays active.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {IERC4626} from "@openzeppelin/contracts/interfaces/IERC4626.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC4626} from "@openzeppelin/contracts/token/ERC20/extensions/ERC4626.sol";

import {Basketoor} from "src/Basketoor.sol";
import {ISwapAdapter} from "src/interfaces/ISwapAdapter.sol";
import {MockUSDC, MockStock, MockFeed, MockSwapAdapter} from "src/mocks/Mocks.sol";

/// An ERC-4626 vault that can refuse withdrawals (paused, or all liquidity lent out), as real ones do.
contract IlliquidVault is ERC4626 {
    bool public frozen;

    constructor(IERC20 a) ERC20("v", "v") ERC4626(a) {}

    function setFrozen(bool f) external {
        frozen = f;
    }

    function _withdraw(address c, address r, address o, uint256 a, uint256 s) internal override {
        require(!frozen, "no liquidity");
        super._withdraw(c, r, o, a, s);
    }
}

/// One savings plan whose vault cannot pay out must not stop plans that never opted into savings.
contract ProofVaultBlocksBatch is Test {
    Basketoor b;
    MockUSDC usdc;
    IlliquidVault vault;
    MockStock stock;
    MockFeed feed;

    address admin = makeAddr("admin");
    address treasury = makeAddr("treasury");
    address keeper = makeAddr("keeper");
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");

    function setUp() public {
        vm.warp(1_760_000_000);
        vm.startPrank(admin);
        usdc = new MockUSDC();
        MockSwapAdapter venue = new MockSwapAdapter(admin);
        b = new Basketoor(usdc, ISwapAdapter(address(venue)), treasury, admin);
        vault = new IlliquidVault(usdc);
        stock = new MockStock("Apple", "AAPLc", 8, admin);
        feed = new MockFeed(8, 180e8, admin);
        stock.setMinter(address(venue));
        venue.setFeed(address(stock), feed);
        b.setAsset(address(stock), feed, true);
        b.setKeeper(keeper, true);
        b.setSavingsVault(IERC4626(address(vault)));
        vm.stopPrank();
        usdc.mint(alice, 1_000e6);
        usdc.mint(bob, 1_000e6);
        vm.prank(alice);
        usdc.approve(address(b), type(uint256).max);
        vm.prank(bob);
        usdc.approve(address(b), type(uint256).max);
    }

    function _create(address who, bool savings) internal returns (uint256) {
        address[] memory tokens = new address[](1);
        tokens[0] = address(stock);
        uint256[] memory amounts = new uint256[](1);
        amounts[0] = 10e6;
        vm.prank(who);
        return b.createPlan("p", tokens, amounts, 1 days, 2, savings);
    }

    function test_nonSavingsPlanStillRunsWhenVaultCannotPay() public {
        _create(bob, true); // savings plan, first in the active list
        uint256 aliceId = _create(alice, false); // plain escrow, no vault involved
        vault.setFrozen(true);

        vm.prank(keeper);
        b.executeDue(10); // reverts today: bob's vault.withdraw bubbles up

        (Basketoor.Plan memory p,) = b.getPlan(aliceId);
        assertEq(p.buysDone, 1, "alice's non-savings plan was blocked by the vault");
    }
}
```

### 3. Medium: skippedRuns is a lifetime counter that a successful buy never resets, so ordinary market-closed skips add up and force-close healthy plans

`contracts/src/Basketoor.sol:429`

```
++p.skippedRuns;
```

Where: Basketoor._execute, the increment on line 429 and the close condition on line 437. p.skippedRuns is incremented on every run where all legs were skipped and is never cleared: not in the spent > 0 branch (lines 419-427) and not by updatePlan. Line 437 closes the plan when the lifetime total reaches the live global maxSkippedRuns (60), and it is evaluated after successful runs too. AUDIT.md (note 8) describes the limit as retiring plans that can no longer buy; for that the counter has to measure consecutive failures (the app describes it as "Refunds the basket if it can't buy for that long", web/src/About.tsx:177). Fully skipped runs are routine for stock legs: the live Base NVDAc feed 0x04689a41629776563E6822F76f2e57D148d28513 (read through https://mainnet.base.org, getRoundData over the last 450 rounds) had one gap longer than 26h, 49.3h from 2026-11-20 23:42:40Z to 2026-11-23 01:00:41Z, so with maxStaleness = 26h its price is unusable for about 23 hours every weekend. With default settings an hourly all-stock plan collects about 23 skips per weekend and is closed in its third weekend whatever maxBuys says; a daily plan loses one run each weekend and is closed at its 60th. Because the limit is read live, the owner lowering maxSkippedRuns also closes plans retroactively. No funds are lost (the remainder is refunded), but the plan the user funded for N buys stops early and must be re-created at the fees then in force. Fix: set p.skippedRuns = 0 in the spent > 0 branch so the limit means consecutive fully skipped runs, and evaluate it only in the skipped branch.

**Reproduction**

Run from contracts/: forge test --match-path test/scratch/ProofSkippedRuns.t.sol (attached; fails on this commit). State: owner setExecutionParams(150, 26 hours, 3) (the default rule scaled from 60 to 3 to keep the run short). alice createPlan("daily", [stock], [10e6], 1 days, maxBuys=100, savings=false). The keeper calls executeDue(10) once a day for 20 days; the price is 2 days old on days 5, 12 and 19 and fresh on every other day. Expected: the plan is still active after day 19, since it filled six times between each skip (17 fills, 83 buys still funded). Actual: on day 19 the third lifetime skip closes it: active = false ("plan was closed although it never missed two runs in a row"). With the default limit, also run as a local Foundry test: createPlan([AAPLc], [10e6], 1 hours, 1000, false); price stale for hours 0-38, fresh for hours 39-88 (50 fills), stale again from hour 89: the plan is closed at hour 109 with buysDone = 50, skippedRuns = 60 and 950 funded buys left.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";

import {Basketoor} from "src/Basketoor.sol";
import {ISwapAdapter} from "src/interfaces/ISwapAdapter.sol";
import {MockUSDC, MockStock, MockFeed, MockSwapAdapter} from "src/mocks/Mocks.sol";

/// skippedRuns is only ever incremented. A plan that fills six runs between every fully skipped run is
/// still closed once its lifetime total of skipped runs reaches maxSkippedRuns.
contract ProofSkippedRunsNeverReset is Test {
    Basketoor b;
    MockUSDC usdc;
    MockStock stock;
    MockFeed feed;

    address admin = makeAddr("admin");
    address treasury = makeAddr("treasury");
    address keeper = makeAddr("keeper");
    address alice = makeAddr("alice");
    uint256 t0 = 1_760_000_000;

    function setUp() public {
        vm.warp(t0);
        vm.startPrank(admin);
        usdc = new MockUSDC();
        MockSwapAdapter venue = new MockSwapAdapter(admin);
        b = new Basketoor(usdc, ISwapAdapter(address(venue)), treasury, admin);
        stock = new MockStock("Apple", "AAPLc", 8, admin);
        feed = new MockFeed(8, 200e8, admin);
        stock.setMinter(address(venue));
        venue.setFeed(address(stock), feed);
        b.setAsset(address(stock), feed, true);
        b.setKeeper(keeper, true);
        // Same rule as the default (60), scaled down so the test stays short.
        b.setExecutionParams(150, 26 hours, 3);
        vm.stopPrank();
        usdc.mint(alice, 10_000e6);
        vm.prank(alice);
        usdc.approve(address(b), type(uint256).max);
    }

    function test_isolatedSkipsDoNotCloseAHealthyPlan() public {
        address[] memory tokens = new address[](1);
        tokens[0] = address(stock);
        uint256[] memory amounts = new uint256[](1);
        amounts[0] = 10e6;
        vm.prank(alice);
        uint256 id = b.createPlan("daily", tokens, amounts, 1 days, 100, false);

        // One run a day for 20 days. The price is too old on days 5, 12 and 19 only.
        for (uint256 day; day < 20; ++day) {
            vm.warp(t0 + day * 1 days);
            bool stale = (day == 5 || day == 12 || day == 19);
            vm.prank(admin);
            feed.setUpdatedAt(stale ? block.timestamp - 2 days : block.timestamp);
            vm.prank(keeper);
            b.executeDue(10);
        }

        (Basketoor.Plan memory p,) = b.getPlan(id);
        assertTrue(p.active, "plan was closed although it never missed two runs in a row");
    }
}
```

### 4. Medium: A fully skipped run pushes nextRun out by a whole interval with no retry, so a weekly plan opened while the market is closed never buys

`contracts/src/Basketoor.sol:432`

```
uint64 next = p.nextRun + p.interval;
```

Where: Basketoor._execute, lines 428-434. nextRun is advanced by a full interval after every run, including one where every leg was skipped and nothing was bought. The schedule is anchored to the previous nextRun (line 432), and the first run is due at creation (line 170), so the plan keeps the phase it was created with. If a plan is opened while its feeds are older than maxStaleness (the market-closed case the contract is built to skip) and its interval is a multiple of 7 days, every attempt lands on the same closed-market moment: every run is skipped, nothing is ever bought, and the budget sits in the plan until the owner cancels or 60 skips close it (60 weeks for a weekly plan). On the live NVDAc feed the unusable window is about Sunday 01:42Z to Monday 01:00Z each week (gap of 49.3h measured 2026-11-20 23:42:40Z to 2026-11-23 01:00:41Z, maxStaleness 26h), so any weekly/14/21/28-day stock plan created in that window is affected. The same rule makes one transient failure expensive on long intervals: a single run of a 30-day plan that meets a stale price, a thin pool or a price outside the 1.5% bound delays that buy by 30 days, and the keeper chooses the moment within the due window. Expected: a run that bought nothing is retried once the price is usable again (the app tells users "Buys during market closures are skipped and retried", web/src/PlanForm.tsx:242). Actual: it is scheduled like a completed buy. Fix that keeps the cadence of successful buys: when spent == 0 leave the plan due, or set nextRun = block.timestamp + a short owner-set retry delay capped at the interval, and keep counting the run in skippedRuns so a dead plan still closes.

**Reproduction**

Run from contracts/: forge test --match-path test/scratch/ProofNoRetry.t.sol (attached; fails on this commit). State: the stock feed was last updated 27 hours ago (maxStaleness is 26h). Input: alice createPlan("weekly", [stock], [20e6], 7 days, maxBuys=10, savings=false). The keeper calls executeDue(10) every 6 hours for 28 days; on days 1-5 of each week the price is fresh, on days 0 and 6 it is 27h old. The plan is attempted at t = 0, 168h, 336h, 504h and 672h, each time on a stale price: LegSkipped(reason 1), nextRun moves 168h on. Expected: at least one buy during the 20 days with a usable price. Actual: buysDone = 0 ("no buy in four weeks although the price was usable on 20 of the 28 days: 0 <= 0").

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";

import {Basketoor} from "src/Basketoor.sol";
import {ISwapAdapter} from "src/interfaces/ISwapAdapter.sol";
import {MockUSDC, MockStock, MockFeed, MockSwapAdapter} from "src/mocks/Mocks.sol";

/// A run where every leg is skipped moves nextRun a whole interval on, exactly like a completed buy.
/// A weekly plan opened while the market is closed is therefore attempted at the same closed-market
/// moment every week and never buys, although the price is usable on five days out of seven.
contract ProofSkippedRunIsNotRetried is Test {
    Basketoor b;
    MockUSDC usdc;
    MockStock stock;
    MockFeed feed;

    address admin = makeAddr("admin");
    address treasury = makeAddr("treasury");
    address keeper = makeAddr("keeper");
    address alice = makeAddr("alice");
    uint256 t0 = 1_760_000_000;

    function setUp() public {
        vm.warp(t0);
        vm.startPrank(admin);
        usdc = new MockUSDC();
        MockSwapAdapter venue = new MockSwapAdapter(admin);
        b = new Basketoor(usdc, ISwapAdapter(address(venue)), treasury, admin);
        stock = new MockStock("Apple", "AAPLc", 8, admin);
        feed = new MockFeed(8, 200e8, admin);
        stock.setMinter(address(venue));
        venue.setFeed(address(stock), feed);
        b.setAsset(address(stock), feed, true);
        b.setKeeper(keeper, true);
        vm.stopPrank();
        usdc.mint(alice, 10_000e6);
        vm.prank(alice);
        usdc.approve(address(b), type(uint256).max);
    }

    function test_weeklyPlanOpenedOnAClosedMarketDayEventuallyBuys() public {
        // The plan is opened on a closed-market day: the last price is 27 hours old (> maxStaleness of 26h).
        vm.prank(admin);
        feed.setUpdatedAt(t0 - 27 hours);

        address[] memory tokens = new address[](1);
        tokens[0] = address(stock);
        uint256[] memory amounts = new uint256[](1);
        amounts[0] = 20e6;
        vm.prank(alice);
        uint256 id = b.createPlan("weekly", tokens, amounts, 7 days, 10, false);

        // The keeper calls executeDue every 6 hours for four weeks. Day 0 and day 6 of each week are
        // closed-market days (price 27h old); on days 1-5 the price is fresh.
        for (uint256 k; k <= 28 * 4; ++k) {
            uint256 t = t0 + k * 6 hours;
            vm.warp(t);
            uint256 dow = ((t - t0) / 1 days) % 7;
            vm.prank(admin);
            feed.setUpdatedAt(dow >= 1 && dow <= 5 ? t : t - 27 hours);
            vm.prank(keeper);
            b.executeDue(10);
        }

        (Basketoor.Plan memory p,) = b.getPlan(id);
        assertGt(p.buysDone, 0, "no buy in four weeks although the price was usable on 20 of the 28 days");
    }
}
```

### 5. Medium: GAS_PER_RUN (900,000) is well below what a plan costs on the mainnet venue, and the gas guard returns success after one plan at the lowest passing gas limit

`contracts/src/Basketoor.sol:36`

```
uint256 public constant GAS_PER_RUN = 900_000;
```

Where: the constant on line 36 ("Gas a keeper should budget per plan (5 legs, savings on)") and the guards that use it on lines 244 and 252. (1) Measured against live Base mainnet state (block 62,042,869, eth_call with state overrides: Basketoor and AerodromeCLAdapter deployed inside the call, real Slipstream pools and Chainlink feeds, one non-savings plan, 10 USDC per leg, all legs filled), executeDue for a single due plan used 516,660 gas with 1 leg (NVDAc), 898,634 with 2 (NVDAc, AAPLc), 1,203,832 with 3 (+WETH) and 1,496,667 with 4 (+cbBTC). These are lower bounds (the setup in the same call had already warmed the pool, token and feed addresses) and exclude the vault. So the documented budget for "5 legs, savings on" is already exceeded by 3 legs with no vault. Consequences: a caller that budgets by the constant, as the comment says (the repository keeper sends 300k + 900k per run), cannot execute a lone due plan with 4 or more legs: the call runs out of gas and reverts every time, the plan stays due, and since neither a buy nor a skipped run is recorded it is never closed either. For i > 0 the guard admits a plan with 900k left that can need 1.5M or more; it runs out of gas mid-plan, and the whole transaction, including the plans already completed in it, reverts and repeats on retry. (2) The guard breaks and returns normally, so at the lowest gas limit at which the call does not revert (what eth_estimateGas, and so a generic scheduler doing "Read dueCount() -> Write executeDue(25)", sends) the call succeeds having run one plan and leaves the rest due with no event; the comment on line 243 covers only the ran-nothing case. Fix that keeps the design: size the guard from the plan (a per-leg allowance of at least ~450k for active legs plus a vault allowance when p.savings), check it before every plan including the first with an explicit revert reason for the first, expose it as a view so keepers budget from the contract, and emit or return how many due plans were left (or revert unless the caller allows partial work).

**Reproduction**

(1) Base mainnet at block 62,042,869 through https://mainnet.base.org, read-only eth_call with a state override placing a probe contract (and 1,000 USDC) at an unused address. The probe deploys AerodromeCLAdapter and Basketoor, calls setPool(USDC, token, pool) and setAsset(token, feed, true) for NVDAc 0xb20000000000000000000078ee7ce2fE4908108C (pool 0xF668e21993f0ACd7ab00BB1cFbAeD0df28A3C8EC, feed 0x04689a41629776563E6822F76f2e57D148d28513), AAPLc 0xb200000000000000000000C2e324d24d7eEcd1fb (pool 0xF5FCB9CDAFcE67d50AfEf298F88E709d2B946BA6, feed 0x787f13dEa48Db0897CbCDD985de77809D837F988), WETH 0x4200000000000000000000000000000000000006 (pool 0xb2cc224c1c9feE385f8ad6a55b4d94E92359DC59, feed 0x71041dddad3595F9CEd3DcCFBe3D1F4b0a16Bb70) and cbBTC 0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf (pool 0x4e962BB3889Bf030368F56810A9c96B83CB3E778, feed 0x64c911996D3c6aC71f9b455B1E8E7266BcbD848F), then createPlan("p", tokens, [10e6 each], 1 days, 3, false) and executeDue(25). Input: executeDue(25) forwarded 1,200,000 gas (one GAS_PER_RUN plus the keeper's 300k). Expected: the plan runs inside the documented budget. Actual: with 4 legs, and with 3 legs, the call reverts (out of gas); with unlimited gas the same call succeeds with ran = 1, totalSpent = 40e6 / 30e6 and uses 1,496,667 / 1,203,832 gas. (2) Local Foundry test, mock venue: four non-savings plans of two 10 USDC legs, all due; binary search for the lowest gas limit at which keeper executeDue(10) does not revert gives 497,109. Expected at a limit that succeeds: all four run, or a revert. Actual: success with ran = 1 and dueCount() still 3 (with 5,000,000 gas ran = 4).

### 6. Low: yieldFeeBps is read at close, not snapshotted per plan: a fee change applies to yield existing plans have already earned

`contracts/src/Basketoor.sol:486`

```
uint256 yieldFee = yieldEarned * yieldFeeBps / BPS;
```

Where: Basketoor._close line 486, against createPlan lines 173-174 and setFees lines 362-369. createPlan snapshots feeBps and minFee into the plan; the setFees comment says "Fees are snapshotted per plan, so changes only affect new plans" and AUDIT.md lists the owner's fees as "bounded; snapshotted per plan". The yield fee is the exception: _close reads the global yieldFeeBps when the plan closes, on both cancelPlan and the keeper's automatic close. setFees(.., .., 3000) therefore changes what every open savings plan pays on yield accrued before the change, up to MAX_YIELD_FEE_BPS (30% of yield, three times the default the user opened the plan under). It is owner-only and bounded, so it is a broken stated guarantee about an owner power rather than a permission bypass. Fix: add uint16 yieldFeeBps to Plan (it fits beside minFee and vault in the existing slot), set it in createPlan next to feeBps/minFee, and use p.yieldFeeBps in _close.

**Reproduction**

Ran the specialist's Foundry test against this commit. State: yieldFeeBps = 1000. alice createPlan("tech", [NVDAc, TSLAc], [500e6, 500e6], 1 days, maxBuys=5, savings=true) deposits 5,025 USDC into the vault; 100e6 USDC of yield arrives in the vault (planValue - principal = 99,999,999). Input: owner setFees(50, 100_000, 3_000); alice cancelPlan(id). Expected: the treasury receives 10% of the yield, 9,999,999. Actual: it receives 29,999,999, taken from alice's refund (test fails with "yield fee changed retroactively: 29999999 !~= 9999999").

### 7. Low: The automatic close pushes the refund to the plan owner inside the keeper batch: one owner USDC will not pay makes every executeDue that reaches the plan revert

`contracts/src/Basketoor.sol:499`

```
if (refund > 0) usdc.safeTransfer(p.owner, refund);
```

Where: Basketoor._close line 499, reached from _execute (lines 403 and 437) and cancelPlan; updatePlan's refund on line 226 has the same push. When the keeper closes a plan (last buy with leftover, out of budget, or the skipped-runs limit) the remainder is transferred to p.owner in the keeper's transaction. USDC on Base has an issuer blocklist and reverts transfers to a blocked address. For such an owner the close reverts and takes the whole batch with it. The plan stays active and due: only its owner may cancel it, and cancelPlan hits the same transfer, so nobody can remove it. duePlans() returns it on every call, so executeDue(maxRuns) reverts each time until the keeper falls back to executeMany without that id (the repository keeper only calls executeDue), and the plan never leaves _active. It needs refund > 0 at close, which is the case for any plan that had a leg skipped, any savings plan with yield, and every close through maxSkippedRuns. Same effect as known issues 4 and 5, different trigger. Fix: do not let the refund decide the batch. Record it as claimable by the owner (always, or as the fallback when the transfer fails in a try/catch) with a claim function, and/or isolate each plan's execution in a try/catch self-call.

**Reproduction**

Local Foundry test, USDC stand-in whose transfers revert for a blocked sender or recipient. State: alice createPlan("p", [AAPLc, WETH], [100e6, 1e6], 1 days, maxBuys=1, false); bob createPlan("p", [WETH], [100e6], 1 days, 5, false). 27 hours later AAPLc's price is stale and WETH's is fresh; the token blocks alice. Input: keeper executeDue(25). Alice's run fills WETH, skips AAPLc, reaches buysDone == maxBuys and calls _close with a 100.5 USDC refund. Expected: bob's buy executes (buysDone = 1) whatever happens to alice's refund. Actual: executeDue reverts with "Blacklistable: account is blacklisted", bob's buysDone stays 0, alice's cancelPlan reverts with the same error, and executeDue reverts again a day later. Only executeMany([bobId]) gets bob's plan run.

### 8. Low: Exit depends on the treasury: the yield-fee push in _close reverts cancelPlan when the treasury cannot receive USDC, and the constructor accepts a zero treasury that setTreasury rejects

`contracts/src/Basketoor.sol:497`

```
if (yieldFee > 0) usdc.safeTransfer(treasury, yieldFee);
```

Where: Basketoor._close line 497 and _execute line 422 (fee pushes to the treasury), setTreasury line 357 and the constructor line 145. AUDIT.md states the plan owner can always cancel with "No dependency on the keeper or the owner to exit". _close transfers the yield fee to the owner-set treasury before refunding the user; _execute pushes the per-buy fee the same way. If that transfer reverts (treasury address on the USDC blocklist, or address(0), which the constructor stores unchecked although setTreasury rejects it), then every savings plan whose yield fee is non-zero cannot be cancelled or auto-closed, and every keeper run that fills at least one leg reverts for all plans, until the owner calls setTreasury. Non-savings plans can still cancel (no yield fee). The owner can repair it, but until then savings exits depend on the owner, which the stated trust model excludes. Fix: reject address(0) in the constructor as setTreasury does, and make user paths independent of the fee recipient: accrue buy and yield fees to a counter the treasury withdraws with its own call (or fall back to accruing when the push fails).

**Reproduction**

Local Foundry tests. (1) Blocked treasury: alice createPlan("p", [AAPLc], [100e6], 1 days, 10, savings=true); 100e6 USDC of yield arrives in the vault; the USDC stand-in blocks the treasury address. alice cancelPlan(id). Expected: alice receives her 1,005 USDC plus yield less the fee. Actual: revert "Blacklistable: account is blacklisted" from line 497; keeper executeDue(25) reverts the same way at line 422; bob's non-savings cancelPlan succeeds. (2) Zero treasury: new Basketoor(usdc, adapter, address(0), admin) succeeds while setTreasury(address(0)) on it reverts BadConfig; alice createPlan("x", [AAPLc], [10e6], 1 days, 2, false) succeeds and pulls 20.2 USDC; keeper executeDue(10) reverts on the fee transfer to address(0).

### 9. Low: updatePlan changes the interval but not nextRun, so a new frequency only takes effect after the old schedule's next run

`contracts/src/Basketoor.sol:211`

```
p.interval = interval;
```

Where: Basketoor.updatePlan line 211; nextRun is written only in createPlan (line 170) and _execute (line 434). updatePlan is documented as "change the frequency", but it stores the new interval and leaves nextRun as computed from the old one at the last run; no user function can move nextRun. Shortening the interval has no effect until the old, longer period is over (a monthly plan switched to hourly waits up to 30 days for its next buy); lengthening it still lets one more buy fire on the old, shorter schedule. The budget is resized at once for the new shape, so funds are escrowed (or spent) on a schedule the user no longer asked for. Fix: when the interval changes, re-anchor the schedule: derive the last run as nextRun - oldInterval before the write, then nextRun = min(nextRun, block.timestamp + interval) when shortening and lastRun + interval (clamped to now) when lengthening.

**Reproduction**

Local Foundry test. alice createPlan("p", [AAPLc], [100e6], interval = 30 days, maxBuys = 10, false) at T; the keeper runs the first buy at T, so nextRun = T + 30 days. Input: at T + 1 hour alice calls updatePlan(id, "p", [AAPLc], [100e6], 1 hours, 10). Expected: next buy about an hour after the change. Actual: getPlan(id).interval is 1 hours but nextRun is still T + 30 days; at T + 2 days with a fresh price executeDue(50) returns 0 (nothing due).

### 10. Low: _put accepts whatever the vault mints, including zero shares: on a near-empty vault a donation makes a new savings plan worth nothing

`contracts/src/Basketoor.sol:573`

```
p.shares += p.vault.deposit(amount, address(this));
```

Where: Basketoor._put line 573 with createPlan line 185 and setSavingsVault line 351. _put adds the return value of vault.deposit to p.shares without checking it, and createPlan records the full deposit as principal. If the savings vault has almost no supply and no share-decimals offset (a plain OpenZeppelin ERC4626, which is what the repository's MockSavingsVault is), anyone can deposit 1 wei, transfer USDC straight to the vault and make the next deposit round to zero shares. The plan is then recorded with principal = deposit and shares = 0: planValue is 0 and cancelPlan refunds nothing. OpenZeppelin's virtual share makes this unprofitable for the attacker, so it is griefing rather than theft, and it needs the owner to have pointed savingsVault at a vault in that state (setSavingsVault checks only asset()); an established vault or one with a decimals offset is not exposed. The contract can verify the assumption itself. Fix: in _put revert when the minted shares are zero or when vault.previewRedeem(minted) is below the amount by more than a wei or two, so createPlan/updatePlan fail instead of escrowing into a manipulated vault; optionally have setSavingsVault refuse a vault with no supply.

**Reproduction**

Local Foundry test, fresh OpenZeppelin ERC4626 vault (totalSupply 0) set as savingsVault. mallory: vault.deposit(1, mallory), then usdc.transfer(vault, 50e6). alice: createPlan("p", [AAPLc, WETH], [10e6, 10e6], 1 days, 1, savings=true) pulls 20,100,000. Expected: the plan holds shares worth about 20.1 USDC, or createPlan reverts. Actual: p.shares = 0, p.principal = 20,100,000, planValue = 0; alice's cancelPlan returns 0, so she is 20.1 USDC down. mallory's redeem(1) returns 35,050,001 of her 50,000,001 (she loses 14.95 USDC).

### 11. Low: A run that fills only some legs uses up a whole buy for every leg: in a stock + crypto basket the stock leg loses its closed-market buys for good and the run pays the fee floor

`contracts/src/Basketoor.sol:423`

```
p.buysDone = buyIndex;
```

Where: Basketoor._execute lines 419-427 and 437. buysDone advances whenever spent > 0 and the plan closes at buysDone >= maxBuys. A leg skipped in such a run is not retried: its USDC for that slot stays in the plan and is refunded at close. For a basket that mixes stocks with crypto this happens every weekend: the crypto feed is fresh while the stock feed is older than maxStaleness for about 23 hours (NVDAc gap 2026-11-20 23:42:40Z to 2026-11-23 01:00:41Z), so each run in that window buys only the crypto leg and still counts as a full buy. The fee on those runs is max(spent x feeBps, minFee) on the small filled leg, i.e. the floor: 0.10 USDC on 1 USDC spent with the defaults. The Plan struct documents buysDone as "buys where at least one leg filled", so this is the coded rule, but its effect is that the plan does not buy what was funded per leg (a daily stock + crypto plan invests about 6/7 of its stock budget; an hourly one can burn all its buys in a weekend). No USDC is lost beyond the floor fees. Fixing it is a design decision: count buys per leg (close when every active leg has done maxBuys), or do not consume a buy slot when a leg was skipped for reason 1 (stale price), or state the rule to users.

**Reproduction**

Local Foundry test. Input: alice createPlan("p", [AAPLc, WETH], [100e6, 1e6], interval 1 hours, maxBuys 24, false) deposits 2,433.60 USDC. From 27 hours later AAPLc's price is older than 26h while WETH's is refreshed each hour; the keeper calls executeDue(50) hourly for 24 hours. Expected: the stock leg's 24 buys are still available when its price is usable again. Actual: buysDone = 24 and the plan is closed as completed with AAPLc bought = 0, totalSpent = 24 USDC, totalFees = 2.40 USDC (10% of what was spent, against feeBps = 0.5%), refund = 2,409.72 USDC.

### 12. Low: createPlan takes no maximum deposit, so a fee change that lands first is pulled from the allowance and snapshotted into the plan

`contracts/src/Basketoor.sol:182`

```
uint256 deposit = _required(_perBuy(id), p.feeBps, p.minFee, maxBuys);
```

Where: Basketoor.createPlan lines 173-174 and 182-183. The deposit is computed from the global feeBps/minFee at execution time and pulled with safeTransferFrom; the caller passes no expected deposit or fee bound. A setFees transaction mined between the user's quoteDeposit and their createPlan changes both the amount pulled (up to the allowance and balance; wallets commonly approve more than one plan's worth) and the fee terms snapshotted into the plan for its life. The first buy is due at once, so one buy can be charged at the new fee before the user reacts; the rest is recoverable by cancelling. Owner-triggered and bounded by MAX_FEE_BPS and the 5 USDC minFee cap. Fix: add a maxDeposit (or expected feeBps/minFee) argument to createPlan and revert when it is exceeded.

**Reproduction**

Local Foundry test. State: feeBps 50, minFee 0.10 USDC; quoteDeposit(10e6, 520) = 5,252.00 USDC. Owner setFees(200, 5e6, 1000) is mined first. alice (allowance to Basketoor above 7,800 USDC) calls createPlan("p", [AAPLc], [10e6], 7 days, 520, false). Expected: revert, or at most 5,252.00 USDC pulled. Actual: 7,800.00 USDC is pulled and the plan is fixed at a 5 USDC fee per 10 USDC buy.

### 13. Info: updatePlan is a second deposit path without createPlan's gates: it ignores createPaused and funds any new budget at the plan's creation-time fees

`contracts/src/Basketoor.sol:214`

```
uint256 required = _required(_perBuy(id), p.feeBps, p.minFee, maxBuys - p.buysDone);
```

Where: Basketoor.updatePlan lines 204-221 against createPlan lines 160 and 173-174. updatePlan pulls new USDC, can add stocks and raise maxBuys to any uint32, but has no pause check and prices everything with the fee snapshot taken when the plan was opened. AUDIT.md describes the pause as "pause of new plans" and fees as "snapshotted per plan", so this matches the documented rules; it is listed because of what follows from them. (1) When the owner pauses creation because the adapter, a feed or the vault is misbehaving, existing plans can still be topped up without limit, and for savings plans that USDC goes into the vault. (2) Since a plan can be resized freely, a minimal plan opened under a low fee schedule keeps that schedule for unlimited later volume. No user funds are at risk; the cost is fee revenue and a pause that does less than an operator may expect. Decision needed: revert on createPaused when updatePlan would pull USDC (always allow refunds), and decide whether a budget increase re-snapshots feeBps/minFee.

**Reproduction**

Local Foundry test. Owner setFees(0, 0, 0); alice createPlan("p", [AAPLc, WETH], [1e6, 1e6], 1 days, maxBuys=1, false) deposits 2e6. Owner setFees(200, 5e6, 3000) and setCreatePaused(true). alice updatePlan(id, "x", [AAPLc, WETH], [1000e6, 1000e6], 1 hours, 4). Expected (if the pause and current fees applied): CreatePaused, or 8,160e6 pulled. Actual: the call succeeds and pulls 7,998,000,000 (zero fee) while bob's createPlan reverts CreatePaused; the next keeper run spends 2,000e6 and the treasury receives 0.

### 14. Info: setSwapAdapter (and the constructor) accept any address: a zero or code-less adapter makes every keeper batch revert instead of skipping legs

`contracts/src/Basketoor.sol:345`

```
swapAdapter = adapter;
```

Where: Basketoor.setSwapAdapter line 345, constructor line 144, _buyLeg lines 457-461. setTreasury rejects address(0) and setSavingsVault checks asset(), but the adapter address is stored unchecked. The try/catch in _buyLeg only catches a revert inside the adapter: with address(0) the preceding forceApprove reverts, and with any other address without code the high-level call's code-size check reverts in Basketoor, so executeDue/executeMany revert for every plan rather than recording skipped legs. Cancels and updates are unaffected, so users can still exit; this is an owner-mistake hazard listed to complete the owner-powers review. Other owner settings that act on already-open plans at once and are not snapshotted: maxSlippageBps (up to 10%), maxStaleness and maxSkippedRuns via setExecutionParams. Fix: require adapter code length != 0 in setSwapAdapter and the constructor.

**Reproduction**

Local Foundry test. alice has a due plan (one 100e6 AAPLc leg). Owner setSwapAdapter(address(0)); keeper executeDue(10). Expected: the leg is skipped with LegSkipped(id, token, 2) and the USDC stays in the plan, as for any failing venue. Actual: the whole transaction reverts. Same with setSwapAdapter(address(0xdead)) (no code).

### 15. Info: AerodromeCLAdapter has its own single-step owner who chooses the pools, a trust root AUDIT.md does not list; setPool only checks token0/token1

`contracts/src/adapters/AerodromeCLAdapter.sol:50`

```
pools[tokenIn][tokenOut] = pool;
```

Where: AerodromeCLAdapter line 23 (Ownable, single-step) and setPool lines 45-53. No defect was found in the swap path: swap only pulls from msg.sender; the callback pays only the pool held in transient storage for the swap in progress; a partial fill reverts with nothing stranded; the limits are MIN_SQRT_RATIO + 1 / MAX_SQRT_RATIO - 1 and the result is bounded by minOut and re-checked at the recipient by Basketoor. What is missing from the documented roles: the adapter's owner need not be Basketoor's owner and can point pools[USDC][token] at any contract that returns the right token0()/token1(); setPool does not check the address against the Slipstream factory. Such a contract is bounded like a malicious adapter (known issue 1): it can keep up to maxSlippageBps of every leg by delivering exactly minOut, or make every batch revert by reporting a fill it did not deliver (UnderDelivered, known issue 5). It cannot take more, because Basketoor measures the fill at the recipient. Fix: document the adapter owner as part of the trust surface, use Ownable2Step with the same key policy as Basketoor, and have setPool verify the pool with the Slipstream factory.

**Reproduction**

Local Foundry tests with a mock pool contract (not a Slipstream pool) exposing token0()/token1() and a v3-style swap that calls the callback. setPool(USDC, AAPLc, mock) is accepted. With AAPLc at 200 USD (8 decimals) a 100e6 USDC leg expects 50,000,000 units; a pool paying exactly 1.5% less fills and the plan owner receives 49,250,000 (the bound), while a pool paying 2% less, or taking only half the input, reverts in the adapter (Slippage / PartialFill), the leg is skipped and all 402e6 USDC is back in the plan with 0 left in the adapter. Callback checks: a direct call by a stranger, and a call from the configured pool outside a swap, both revert UnexpectedCallback with 5e6 stray USDC sitting in the adapter, and a stranger's own swap leaves that 5e6 untouched. An 18-decimal leg (WETH at 3,000 USD) for 100e6 USDC delivered 0.033166 WETH against the same bound.

---

Judge's submission `b8d82083748c90fc0d4076393076f5b15d29745b621620edbb29804c76971c62`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
