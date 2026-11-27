# Audit report

> Audit github.com/MirakoolDev/basketoor at commit 404e0ce, contracts/ only (scope and notes in contracts/AUDIT.md). This is a re-audit: you audited b14b3cc, and those fixes are in test/audit/. Look hardest at what changed since then:
>
> 1. Fee splits in DCAC._execute: the smart-buys premium (smartFeeBps) and shared baskets (createSharedPlan, creator gets creatorShareBps of each buy fee, paid via _pay). Can a creator, a copier or the owner take more than intended, block the keeper, or leave USDC stuck in the contract?
> 2. Budget math: _resize, setSmartBuys and updatePlan resizing deposits when the fee changes. Can a user underpay for their remaining buys or get back more than they put in?
> 3. PoolTwapFeed and TickMath: a 30-minute TWAP of Aerodrome Slipstream pools holding about $105k of USDC, used as the price check for stocks without Chainlink. How cheap is it to move, and what can an attacker get out of it?
> 4. AerodromeCLAdapter swap paths, and the gas budget (gasFor / InsufficientGas) with executeDue(3).
>
> The contract will run on Base mainnet with real USDC and Coinbase tokenized stocks (8 decimals, multiplier() about 1.0005).

| | |
|---|---|
| Repository | https://github.com/MirakoolDev/basketoor.git |
| Commit | `404e0ced4e2a4d92bfc99a46a539fc54e10c58ad` |
| Job | `2b372e3c-5c92-4c05-b62c-ebaaa402a9e2` |
| Judged | 2026-11-27 11:55 UTC |
| Findings | 1 high · 2 medium · 5 low · 3 info |

Four agents audited the code as it is at `404e0ce`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: PoolTwapFeed: one 30-minute arithmetic-mean tick with no outlier, spot or depth check; a few seconds at an extreme tick in a thin pool moves DCAC's only price bound for 24 TWAP-priced stocks by 10% or

`contracts/src/feeds/PoolTwapFeed.sol:68`

```
        return (1, int256(quote(twapTick())), block.timestamp, block.timestamp, 1);
```

Merged from audit_economics b574e845, audit_permissions bff4a26c, audit_flow e84470f8 and audit_math 92598271 (one mechanism). twapTick() (lines 56-64) is delta/window over a single observe([1800,0]), and latestRoundData() returns it with updatedAt = block.timestamp. So DCAC.priceOf always calls it fresh, maxStaleness never applies, and nothing limits how far one stretch of the window may sit from the rest. A displacement of D ticks held for t seconds moves the mean by D*t/1800 ticks. A swap that runs out of liquidity carries the tick to its price limit (MIN_TICK = -887272) at no extra cost, so one 2-second Base block there, from the ADBE market tick -8587, shifts the mean by about 976 ticks: the feed reports +10.3% for the next 30 minutes, after the pool is already back at the market price. For assets priced this way, DCAC._buyLeg (lines 659-660) sets minOut = amount/feedPrice*(1-1.5%) from this number, and it is the swap pool itself (AerodromeCLAdapter) that fills the buy. Pushed up, the bound accepts fills up to 1-0.985/shift below the market (about 10.7% after one far-tick block, 51% at a 2x shift). The attacker keeps the pool's token inventory they bought and sells it back to the keeper's buys as liquidity just inside the loosened bound, or sandwiches the keeper's buy. Pushed down, every leg in that token fails for 30 minutes: smart plans steer more of the buy into the failing leg, and mixed plans use up a buy (open finding 11). Live state I read on Base (block ~62,949,900, 2026-11-27): the ADBE/USDC pool 0x80997E42... holds 104,352 USDC at tick -8587 with in-range L = 1.58e12. The specialists' tick-bitmap reads put all real depth within about +/-2.5% of spot, with only a full-range dust position (L about 1e8) outside it. Moving the tick past the band then costs about the $105-120k of capital needed to buy out one side, held across a few blocks (no flash loan), plus about $110 of pool fees on the round trip. Plan schedules and amounts are public (getPlan, duePlans), so an attacker can time it to the buys due on a token. The contract comment ('someone willing to hold the pool price off for the whole window') understates this: the whole window is not needed, and depth is never checked. AUDIT.md invariant 3 (a leg fills only within maxSlippageBps of the oracle) does not hold for these assets. Fix, keeping the design: have the feed refuse to answer (revert, so DCAC skips the leg) when the window cannot be trusted. For example, read several sub-windows in one observe call ([1800,1500,...,0]) and use their median, or revert when the 5-minute mean and the 30-minute mean (or spot from slot0) differ by more than the slippage bound. Also require a minimum in-range pool.liquidity() at read time, and consider a per-asset slippage bound or a cap on USDC bought per window for TWAP-priced assets. A longer window alone only scales the seconds needed.

**Reproduction**

Ran the attached proof (from audit_flow, unchanged): forge test --match-path test/scratch/TwapSpike.t.sol in contracts/. It uses a pool mock that integrates tickCumulative the way the Slipstream oracle does, with USDC as token0, the stock at tick -8587 (~$236) for 1800 s, and PoolTwapFeed(window 1800). Input: the tick is set to -887272 at the end of one block, 2 s pass, and the tick is set back to -8587. Expected: the feed still reports ~$236.00 (within 1.5%) or refuses. Actual: 260.21868383e8 (+10.26%); test_oneBlockSpikeMovesTwapPrice fails with '26021868383 > 23953890980'. In test_spikeLoosensBuyBound the venue fills 8% above the market. Before the spike, bob's $1,000 buy is refused (bob receives 0). After the spike, alice's identical buy is accepted and she receives about 7.6% less stock than $1,000 buys at the market; it fails with 'buy filled more than 1.5% under the market price'. Both pass with a median-of-sub-windows or short-vs-long-mean check, because the feed then refuses and DCAC skips the leg. Also confirmed: the other specialists' proofs fail on this commit the same way (held tick: 1.9708 instead of >= 4.11 tokens for $1,000; HOOD parked +20%: 83.795e8 against 69.83e8).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {DCAC} from "src/DCAC.sol";
import {ISwapAdapter} from "src/interfaces/ISwapAdapter.sol";
import {PoolTwapFeed, ICLPoolOracle} from "src/feeds/PoolTwapFeed.sol";
import {MockUSDC, MockStock, MockFeed, MockSwapAdapter} from "src/mocks/Mocks.sol";

/// Minimal Slipstream / Uniswap-v3 style oracle: tickCumulative grows by tick * seconds, an observation is
/// written when the tick changes, and observe() interpolates between observations like the real Oracle library.
contract OraclePool {
    address public immutable token0;
    address public immutable token1;
    int24 public tick;
    uint32[] internal times;
    int56[] internal cums;

    constructor(address t0, address t1, int24 tick_) {
        token0 = t0;
        token1 = t1;
        tick = tick_;
        times.push(uint32(block.timestamp));
        cums.push(0);
    }

    /// A swap that leaves the pool at `newTick`.
    function setTick(int24 newTick) external {
        uint32 last = times[times.length - 1];
        if (block.timestamp > last) {
            cums.push(cums[cums.length - 1] + int56(tick) * int56(uint56(block.timestamp - last)));
            times.push(uint32(block.timestamp));
        }
        tick = newTick;
    }

    function _cumAt(uint32 when) internal view returns (int56) {
        uint256 n = times.length;
        uint32 last = times[n - 1];
        if (when >= last) return cums[n - 1] + int56(tick) * int56(uint56(when - last));
        for (uint256 i = n - 1; i > 0; --i) {
            if (times[i - 1] <= when) {
                int56 slope = (cums[i] - cums[i - 1]) / int56(uint56(times[i] - times[i - 1]));
                return cums[i - 1] + slope * int56(uint56(when - times[i - 1]));
            }
        }
        revert("OLD");
    }

    function observe(uint32[] calldata ago) external view returns (int56[] memory c, uint160[] memory s) {
        c = new int56[](ago.length);
        s = new uint160[](ago.length);
        for (uint256 i; i < ago.length; ++i) {
            c[i] = _cumAt(uint32(block.timestamp) - ago[i]);
        }
    }
}

/// One 2-second block with the pool parked at the far end of the tick range moves the 30-minute TWAP price by
/// about 10%, and DCAC's buy bound moves with it.
contract TwapSpikeTest is Test {
    int24 constant MARKET_TICK = -8587; // USDC is token0, an 8-decimal stock at about $236 (ADBEc pool on Base)
    int24 constant FAR_TICK = -887272; // TickMath.MIN_TICK: where a swap ends once it runs out of liquidity

    DCAC b;
    MockUSDC usdc;
    MockStock stock;
    MockSwapAdapter venue;
    MockFeed spot; // the price the venue fills at: the pool's spot price
    OraclePool pool;
    PoolTwapFeed feed;

    address admin = makeAddr("admin");
    address treasury = makeAddr("treasury");
    address keeper = makeAddr("keeper");
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");

    function setUp() public {
        vm.warp(1_760_000_000);
        vm.startPrank(admin);
        usdc = new MockUSDC();
        stock = new MockStock("Adobe", "ADBE", 8, admin);
        pool = new OraclePool(address(usdc), address(stock), MARKET_TICK);
        feed = new PoolTwapFeed(ICLPoolOracle(address(pool)), address(stock), address(usdc), 8, 6, 1800);
        venue = new MockSwapAdapter(admin);
        spot = new MockFeed(8, 1, admin);
        venue.setFeed(address(stock), spot);
        stock.setMinter(address(venue));
        b = new DCAC(usdc, ISwapAdapter(address(venue)), treasury, admin);
        b.setAsset(address(stock), feed, true);
        b.setKeeper(keeper, true);
        vm.stopPrank();
        usdc.mint(alice, 10_000e6);
        usdc.mint(bob, 10_000e6);
        vm.prank(alice);
        usdc.approve(address(b), type(uint256).max);
        vm.prank(bob);
        usdc.approve(address(b), type(uint256).max);
        vm.warp(block.timestamp + 1800); // a quiet half hour at the market price
    }

    function _price() internal view returns (bool ok, uint256 price) {
        try feed.latestRoundData() returns (uint80, int256 answer, uint256, uint256, uint80) {
            return (true, uint256(answer));
        } catch {
            return (false, 0);
        }
    }

    function _spike() internal {
        pool.setTick(FAR_TICK); // last transaction of block N
        vm.warp(block.timestamp + 2); // one Base block
        pool.setTick(MARKET_TICK); // first transaction of block N+1: the pool is back at the market price
    }

    function _open(address who) internal returns (uint256) {
        address[] memory t = new address[](1);
        t[0] = address(stock);
        uint256[] memory a = new uint256[](1);
        a[0] = 1_000e6;
        vm.prank(who);
        return b.createPlan("adbe", t, a, 1 days, 1, false, false, type(uint256).max);
    }

    /// A 2-second excursion must not move the reported price past DCAC's 1.5% bound (or the feed must refuse).
    function test_oneBlockSpikeMovesTwapPrice() public {
        (, uint256 fair) = _price();
        assertApproxEqRel(fair, 236e8, 0.01e18);
        _spike();
        (bool ok, uint256 spiked) = _price();
        if (ok) assertLe(spiked, fair * 10_150 / 10_000, "one block at the far tick moved the 30-minute TWAP");
    }

    /// With the pool's spot held 8% over the market, a buy is refused. After the one-block spike the same buy
    /// goes through and the user gets about 7.6% less stock than their USDC is worth.
    function test_spikeLoosensBuyBound() public {
        (, uint256 fair) = _price();
        vm.prank(admin);
        spot.setPrice(int256(fair * 108 / 100)); // what the pool sells at while the attacker holds it up

        _open(bob);
        vm.prank(keeper);
        b.executeDue(3);
        assertEq(stock.balanceOf(bob), 0, "control: an 8% overpriced fill is refused against the honest TWAP");

        _spike();
        _open(alice);
        vm.prank(keeper);
        b.executeDue(3);
        uint256 fairOut = 1_000e6 * 1e16 / (fair * 1e6);
        uint256 got = stock.balanceOf(alice);
        assertTrue(got == 0 || got >= fairOut * 9_850 / 10_000, "buy filled more than 1.5% under the market price");
    }
}
```

### 2. Medium: createSharedPlan: the 'no creator when sharing with yourself' rule is one address comparison, so any user takes back creatorShareBps (50%) of their own buy fees by naming a second address

`contracts/src/DCAC.sol:255`

```
        if (creator != address(0) && creator != msg.sender) {
```

Merged from audit_economics 9ea86b29, audit_permissions 4b0cf02a, audit_flow 6faf7680 and audit_math fba1f6e5. The NatSpec on createSharedPlan says 'Sharing with yourself counts as no creator', and SharedBaskets.t.sol tests exactly that. But creator is any caller-supplied address other than msg.sender. Nothing ties it to a basket that was shared, a registered creator or a signature. A user who names a second wallet (or a contract they control, or a wallet front end naming its own address for all its users) receives creatorShareBps of every buy fee on their own plan: half with the default 5,000, all of it if the owner ever sets 10,000. The share is snapshotted for the life of the plan. The effective fee drops from 0.5% to 0.25% (0.375% with smart buys, $0.05 instead of the $0.10 floor), and the treasury loses that share. Deposit and total fee look the same as for a genuine shared plan, so it cannot be told apart on-chain. A stricter comparison cannot close this; it needs a scope decision. Either recognise creators by something the copier cannot mint for free (an owner-kept registry, an on-chain basket id whose legs must match, or a creator-signed basket hash checked in createSharedPlan), or accept the cut openly as a referral rebate and price creatorShareBps accordingly.

**Reproduction**

Ran the attached proof (from audit_economics, unchanged): forge test --match-path test/scratch/CreatorSelfRebate.t.sol. Alice calls createSharedPlan(creator = makeAddr('alice second wallet'), 'mine', [NVDA], [100e6], 1 days, 10, false, false, max), then the keeper calls executeDue(3). One $100 buy is charged a 500,000 fee. Expected: treasury 500,000, second address 0. Actual: treasury 250,000, alice2 250,000 (creatorEarned[alice2] = 250,000). The test fails with 'the plan owner rebated half the fee to themselves: 250000 != 0'. Over 10 buys Alice gets $2.50 of her $5.00 in fees back. The test passes once an unknown creator earns nothing or the call reverts.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";

import {DCAC} from "src/DCAC.sol";
import {ISwapAdapter} from "src/interfaces/ISwapAdapter.sol";
import {MockUSDC, MockStock, MockFeed, MockSwapAdapter} from "src/mocks/Mocks.sol";

abstract contract Base is Test {
    DCAC b;
    MockUSDC usdc;
    MockSwapAdapter venue;
    MockStock nvda;
    MockStock aapl;
    MockFeed nvdaFeed;
    MockFeed aaplFeed;

    address admin = makeAddr("admin");
    address treasury = makeAddr("treasury");
    address keeper = makeAddr("keeper");
    address alice = makeAddr("alice");

    function setUp() public virtual {
        vm.warp(1_795_000_000);
        vm.startPrank(admin);
        usdc = new MockUSDC();
        venue = new MockSwapAdapter(admin);
        b = new DCAC(usdc, ISwapAdapter(address(venue)), treasury, admin);
        nvda = new MockStock("NVIDIA", "NVDA", 8, admin);
        aapl = new MockStock("Apple", "AAPL", 8, admin);
        nvdaFeed = new MockFeed(8, 100e8, admin);
        aaplFeed = new MockFeed(8, 100e8, admin);
        nvda.setMinter(address(venue));
        aapl.setMinter(address(venue));
        venue.setFeed(address(nvda), nvdaFeed);
        venue.setFeed(address(aapl), aaplFeed);
        b.setAsset(address(nvda), nvdaFeed, true);
        b.setAsset(address(aapl), aaplFeed, true);
        b.setKeeper(keeper, true);
        vm.stopPrank();
        usdc.mint(alice, 10_000e6);
        vm.prank(alice);
        usdc.approve(address(b), type(uint256).max);
    }

    function _one(address token, uint256 amount) internal pure returns (address[] memory t, uint256[] memory a) {
        t = new address[](1);
        t[0] = token;
        a = new uint256[](1);
        a[0] = amount;
    }
}

/// A copier names a second address of their own as the basket's "creator" and gets half of every buy fee back.
contract CreatorSelfRebateTest is Base {
    function test_copierCannotRebateTheFeeToTheirOwnSecondAddress() public {
        address alice2 = makeAddr("alice second wallet"); // never shared anything, registered nowhere
        (address[] memory t, uint256[] memory a) = _one(address(nvda), 100e6);
        vm.prank(alice);
        try b.createSharedPlan(alice2, "mine", t, a, 1 days, 10, false, false, type(uint256).max) {}
        catch {
            return; // refusing a creator the protocol doesn't know is a fix
        }
        vm.prank(keeper);
        b.executeDue(3);

        // One $100 buy: the fee is $0.50. Expected: all of it reaches the treasury, since no basket was shared.
        // Actual: treasury $0.25, Alice's second address $0.25.
        assertEq(usdc.balanceOf(alice2) + b.owed(alice2), 0, "the plan owner rebated half the fee to themselves");
        assertEq(usdc.balanceOf(treasury), 0.5e6, "treasury short");
    }
}
```

### 3. Medium: executeDue always scans _active from the front, and runs that buy nothing are free and come back due after 1 hour: 180 refundable $1.10 plans on a stale-feed stock starve every later plan

`contracts/src/DCAC.sol:481`

```
            if (_plans[id].nextRun <= block.timestamp) ids[n++] = id;
```

Merged from audit_economics 46fe3dd2 and audit_permissions c9f4c783. duePlans(maxRuns) returns the first maxRuns due plans in _active order and starts at index 0 on every call. A run where every leg is skipped charges no fee (line 606), and _skipRun (line 638) makes the plan due again RETRY_DELAY = 1 hour later, up to maxSkippedRuns = 168 times in a row. The shipped keeper (keeper/index.mjs) calls executeDue(3) every 60 s, which is 180 runs an hour. Once 180 plans near the front of _active are in the skip-retry state, each comes back due exactly when the keeper gets round to it again. No plan behind them is ever reached: no first buy and no scheduled buy, for up to 7 days per retrying plan. The keeper meanwhile pays gas for runs that earn nothing. It costs an attacker 180 x $1.10 = $198 of deposits, all refunded by cancelPlan since a skipped run is never charged, plus creation gas. The skipping leg can be any market-hours Chainlink stock once its feed is older than maxStaleness (26 h, so about Saturday evening to Monday's open every weekend), a disabled asset, or a TWAP-priced token whose feed reverts. It also happens with no attacker: on a weekend, 180 older ordinary stock-only plans starve the newer ETH, cbBTC, 24/7-feed and TWAP-priced plans, which are exactly the ones that could buy. This is different from AUDIT.md known issue 6, which covers the gas of the O(n) scan, not its fixed order. Fix, keeping fees and retries: make the scan fair. Keep a storage cursor so each executeDue resumes after the last plan it served (wrapping around), or move a skipped plan to the back of _active, or serve never-skipped due plans first. Backing the retry off (1 h, 2 h, 4 h...) also stops failing plans from taking the whole batch.

**Reproduction**

Ran the attached test (mine): forge test --match-path test/scratch/RetryQueueStarvation.t.sol. State: the AAPL feed's updatedAt = now - 27 h (stale). Mallory creates 180 plans, each createPlan('junk', [AAPL], [1e6], 30 days, 1, false, false, max) (1.1e6 each). Alice then creates createPlan('nvda', [NVDA], [100e6], 1 hours, 10, ...), due at once. The keeper calls executeDue(3) every 60 s for 6 hours (360 calls), with the NVDA feed refreshed before each call. Expected: Alice's plan, due with a usable price the whole time, buys at least once. Actual: every call runs three of Mallory's plans, which skip and become due again 1 h later; Alice's buysDone stays 0. The test fails with 'plan starved behind plans that never buy: 0 < 1'. It passes with a round-robin cursor. Note for whoever reruns it: under via_ir, block.timestamp is cached inside the test function, so the warps use literal timestamps.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {IERC4626} from "@openzeppelin/contracts/interfaces/IERC4626.sol";

import {DCAC} from "src/DCAC.sol";
import {ISwapAdapter} from "src/interfaces/ISwapAdapter.sol";
import {MockUSDC, MockStock, MockFeed, MockSwapAdapter, MockSavingsVault} from "src/mocks/Mocks.sol";

/// Runs that buy nothing are free and come back to the front of the scan every hour, so 180 refundable $1.10
/// plans on a stock whose feed is stale keep a due plan with a fresh price from ever running.
contract RetryQueueStarvationTest is Test {
    DCAC b;
    MockUSDC usdc;
    MockSwapAdapter venue;
    MockStock nvda;
    MockStock aapl;
    MockFeed nvdaFeed;
    MockFeed aaplFeed;
    MockSavingsVault vault;

    address admin = makeAddr("admin");
    address treasury = makeAddr("treasury");
    address keeper = makeAddr("keeper");
    address alice = makeAddr("alice");
    address mallory = makeAddr("mallory");

    function setUp() public {
        vm.warp(1_795_000_000);
        vm.startPrank(admin);
        usdc = new MockUSDC();
        venue = new MockSwapAdapter(admin);
        b = new DCAC(usdc, ISwapAdapter(address(venue)), treasury, admin);
        nvda = new MockStock("NVIDIA", "NVDA", 8, admin);
        aapl = new MockStock("Apple", "AAPL", 8, admin);
        nvdaFeed = new MockFeed(8, 100e8, admin);
        aaplFeed = new MockFeed(8, 100e8, admin);
        nvda.setMinter(address(venue));
        aapl.setMinter(address(venue));
        venue.setFeed(address(nvda), nvdaFeed);
        venue.setFeed(address(aapl), aaplFeed);
        b.setAsset(address(nvda), nvdaFeed, true);
        b.setAsset(address(aapl), aaplFeed, true);
        b.setKeeper(keeper, true);
        vault = new MockSavingsVault(usdc);
        b.setSavingsVault(IERC4626(address(vault)));
        vm.stopPrank();
        for (uint256 i; i < 2; ++i) {
            address who = i == 0 ? alice : mallory;
            usdc.mint(who, 100_000e6);
            vm.prank(who);
            usdc.approve(address(b), type(uint256).max);
        }
    }

    function _one(address token, uint256 amount) internal pure returns (address[] memory t, uint256[] memory a) {
        t = new address[](1);
        t[0] = token;
        a = new uint256[](1);
        a[0] = amount;
    }

    function _two(uint256 x, uint256 y) internal view returns (address[] memory t, uint256[] memory a) {
        t = new address[](2);
        t[0] = address(nvda);
        t[1] = address(aapl);
        a = new uint256[](2);
        a[0] = x;
        a[1] = y;
    }

    function _plan(uint256 id) internal view returns (DCAC.Plan memory p) {
        (p,) = b.getPlan(id);
    }

    // Plans that only skip re-queue hourly at the front of _active and starve later plans.
    function test_retryQueueStarvation() public {
        vm.prank(admin);
        aaplFeed.setUpdatedAt(block.timestamp - 27 hours); // stale (maxStaleness 26h)
        (address[] memory t, uint256[] memory a) = _one(address(aapl), 1e6);
        for (uint256 i; i < 180; ++i) {
            vm.prank(mallory);
            b.createPlan("junk", t, a, 30 days, 1, false, false, type(uint256).max);
        }
        (t, a) = _one(address(nvda), 100e6);
        vm.prank(alice);
        uint256 id = b.createPlan("nvda", t, a, 1 hours, 10, false, false, type(uint256).max);
        for (uint256 i; i < 360; ++i) {
            vm.prank(admin);
            nvdaFeed.setPrice(100e8);
            vm.prank(keeper);
            b.executeDue(3);
            vm.warp(1_795_000_000 + 60 * (i + 1)); // literal: via-IR caches block.timestamp in tests
        }
        assertGe(_plan(id).buysDone, 1, "plan starved behind plans that never buy");
    }

}
```

### 4. Low: Shared plan with creator = the DCAC contract: the creator's cut is 'paid' from DCAC to itself and stranded for good (no sweep; loose balance no longer equals totalOwed)

`contracts/src/DCAC.sol:613`

```
            _pay(p.creator, cut);
```

Merged from audit_economics d1e3c8e2, audit_permissions 75ec3458, audit_flow 0015058d and audit_math 92019cf2. _createPlan accepts any creator other than address(0) and msg.sender. With creator = address(this), _pay calls usdc.transfer(DCAC, cut), which succeeds, so nothing is recorded in owed. The cut stays in DCAC's balance, belongs to no plan's idle or shares, and no function can move it out. That breaks AUDIT.md invariant 2 (loose USDC == totalOwed). creatorEarned[DCAC] meanwhile reports earnings nobody received. The same happens through the owed path for a creator that can never receive USDC or call claim: the USDC token address (Circle blacklists it as a recipient) leaves owed[USDC] forever. The specialists also note setTreasury(address(this)) strands every fee in the same way; that one is owner-only. The caller gains nothing, so this is the stuck-USDC case rather than theft: the treasury loses creatorShareBps of every fee on that plan. Fix: in _createPlan, treat creator == address(this) (and address(usdc)) like no creator, or revert; reject treasury_ == address(this) in setTreasury.

**Reproduction**

Ran my repro (test/scratch/Repro.t.sol test_creatorIsDcacStrandsUsdc). Alice calls createSharedPlan(address(dcac), 'copy', [NVDA], [100e6], 1 days, 1, false, false, max), then the keeper calls executeDue(3). The single buy is charged a 500,000 fee and the plan closes. Expected: no active plans, totalOwed 0, usdc.balanceOf(dcac) 0, treasury 500,000. Actual: activePlans().length == 0 and totalOwed == 0, but usdc.balanceOf(dcac) == 250,000, and the treasury received 250,000. It fails with 'USDC stranded in DCAC: 250000 != 0'.

### 5. Low: Smart-buys premium (smartFeeBps) is charged on runs where _allocate fell back to the plain leg amounts

`contracts/src/DCAC.sol:609`

```
        uint256 fee = _take(p, _feeFor(spent, _bps(p), p.minFee));
```

Merged from audit_economics dfb07e0a, audit_permissions ad9fd6a5, audit_flow c2527ea2 and audit_math 89e1cbbe. _allocate returns the plain leg amounts whenever any active leg lacks a usable price (line 706: if (!smart || !allPriced) return (prices, allocs)). The fee is still computed with _bps(p), which adds smartFeeBps whenever p.smart is set, so the plan pays the premium for a run that did no rebalancing. For the baskets the app offers this is the normal weekend case: a smart basket that mixes a market-hours Chainlink stock with ETH, cbBTC, a 24/7-feed stock or a TWAP-priced stock falls back on every run while the stock feed is stale. A creator, if set, takes creatorShareBps of the extra. The header's wording ('plus smartFeeBps while smart buys are on') literally matches what happens, but the user pays for a service that was not delivered. Fix: have _allocate report whether the smart split was applied, and charge p.feeBps alone when it was not. The budget is already sized for the higher rate, so the unused premium stays in the plan and is refunded by the next resize or at close.

**Reproduction**

Ran my repro (test/scratch/Repro.t.sol test_smartPremiumOnFallback): createPlan('smart', [NVDA, AAPL], [60e6, 40e6], 1 days, 2, false, smart = true, max), then the AAPL feed's updatedAt is set to now - 27 h and the keeper calls executeDue(3). NVDA buys its plain 60e6 (totalSpent = 60,000,000) and AAPL is skipped. Expected fee for a plain run: max(60e6 x 50 / 10,000, 100,000) = 300,000. Actual: totalFees = 450,000 (75 bps); it fails with '450000 != 300000'.

### 6. Low: PoolTwapFeed does not check that the pool keeps a window's worth of observations: the live ADBE and HOOD pools have observationCardinality 900 (next 900), so one write per 2-second block makes observe

`contracts/src/feeds/PoolTwapFeed.sol:59`

```
        (int56[] memory cumulatives,) = pool.observe(ago);
```

Merged from audit_economics faf9747b, audit_permissions 223a66b4, audit_flow 4edd521f and audit_math 7b23d9d5. A Slipstream pool (Uniswap v3 Oracle library) keeps observationCardinality observations, writes at most one per block (on a swap, or a mint/burn in range), and observe() reverts 'OLD' when now - window is older than the oldest stored observation. The constructor (line 40) checks the pair and window >= 5 min but never the pool's capacity, and nothing calls increaseObservationCardinalityNext. I read slot0 on Base at block ~62,949,900: ADBE 0x80997E42... cardinality 900, next 900; HOOD 0x25B45fF2... 900, next 900; KO 0x59C7a81E... 900, next 2000. The math specialist reports that 17 of the 24 TWAP pools are at 900. At 2-second blocks, 900 observations written in consecutive blocks span 1,798 s, two seconds short of the 1,800 s window. If the pool was written in each of the last 900 blocks (busy trading, a griefer paying gas for one dust swap or in-range mint per block, or an earlier buy of the same token in the same keeper batch), the read reverts. DCAC.priceOf then returns (0, 0, false) and every leg in that token is skipped (LegSkipped reason 1). Single-token plans retry hourly and close after maxSkippedRuns; mixed plans use up buys without the leg; smart plans fall back and still pay the premium. No funds are lost. Fix: at deployment call pool.increaseObservationCardinalityNext (permissionless) to well above window / block time (e.g. 3,600), and have the constructor require observationCardinalityNext to be at least that and call observe([window,0]) once, so a pool that cannot answer is rejected.

**Reproduction**

State: PoolTwapFeed(window = 1800) over the ADBE pool (cardinality 900, next 900; read with cast call slot0() on Base at block ~62,949,900). Input: one observation-writing action in each of 900 consecutive 2-second blocks, the last one earlier in the keeper's block, so the oldest stored observation is at T-1798. Then latestRoundData() runs observe([1800, 0]) with target T-1800, older than the oldest observation. Expected: a price. Actual: the pool reverts 'OLD', DCAC.priceOf(ADBE) returns (0, 0, false), and executeDue emits LegSkipped(id, ADBE, 1) for every plan holding it, for as long as the writes continue. This follows from the pool's Oracle.observe rule plus the live cardinality. It was not executed on a fork: the stock tokens are B20 precompiles that Foundry forks cannot run.

### 7. Low: No yield fee when vault.redeem fails at close; the plan owner chooses when to cancel, and the share value was knowable via previewRedeem

`contracts/src/DCAC.sol:757`

```
        uint256 yieldEarned = sharesOut == 0 && assetsOut > p.principal ? assetsOut - p.principal : 0;
```

Merged from audit_economics 44453f04 and audit_math 78ea8873. When vault.redeem reverts in _close, the owner is handed all the plan's vault shares and yieldEarned is forced to 0, so the treasury's yieldFeeBps (10% by default) is never charged on that yield. cancelPlan is the owner's call and the owner picks the moment: a Morpho/MetaMorpho vault reverts redeem whenever its markets' free liquidity is short. That happens at high utilisation, and a contract owner can create it for one transaction (borrow the free liquidity, cancel, repay). The comment's reason ('what they are worth isn't known here') does not hold: previewRedeem / convertToAssets values the shares without needing liquidity, and _valueOf already relies on it. The loss is bounded by yieldFeeBps of one plan's yield. Fix: when redeem fails, value the shares with previewRedeem (in a try), and transfer yieldFee worth of shares (shares x yieldFee / value) to the treasury before handing the owner the rest. Keep today's behaviour only if previewRedeem also fails.

**Reproduction**

Ran my repro (test/scratch/Repro.t.sol test_frozenVaultCloseSkipsYieldFee), with an ERC-4626 whose _withdraw reverts while frozen (the same as AuditFixes.t.sol's FreezableVault). Savings plan [NVDA] [100e6], 10 buys: deposit 1,005e6. 100.5e6 of yield is added to the vault (+10%). The vault is frozen, Alice calls cancelPlan, the vault is unfrozen, and Alice redeems the shares she was handed. Expected: the treasury receives about 10.05e6 (10% of the yield). Actual: PlanClosed reports yieldEarned 0 and yieldFee 0, Alice redeems everything (about 1,105.5e6), and the treasury balance stays 0; it fails with 'no yield fee taken: 0 < 10000000'.

### 8. Low: A sub-cent budget top-up into a savings plan reverts with BadVaultDeposit (the 0.01% allowance is 0 below 10,000 units while ERC-4626 rounding loses 1 unit), so setSmartBuys and small updatePlan chang

`contracts/src/DCAC.sol:895`

```
            if (strict && (minted == 0 || vault.previewRedeem(minted) + amount / 10_000 < amount)) {
```

From audit_math e4b43bcf. For new money, _put requires previewRedeem(minted) + amount/10_000 >= amount. Below 10,000 units ($0.01) the allowance is 0. Meanwhile any ERC-4626 whose share price is not exactly 1 values a fresh deposit one unit short, because deposit rounds shares down and previewRedeem rounds assets down. The specialist read previewRedeem(previewDeposit(5000)) = 4999 on Gauntlet USDC Prime. _resize pulls exactly the difference in required budget, which is often tiny near the fee floor. For example, turning smart buys on for a $13.40-per-buy basket changes each buy's fee by 500 units. The user then cannot turn the feature on, or make that small amount change, on a savings plan, and the error blames the vault. Fix: allow for one or two units of vault rounding on top of the 0.01%, e.g. vault.previewRedeem(minted) + amount / 10_000 + 2 < amount. The donation-inflation guard from the previous audit (finding 10) still rejects materially short mints.

**Reproduction**

Ran my repro (test/scratch/Repro.t.sol test_smallTopUpReverts) with the project's MockSavingsVault (OZ ERC4626). createPlan('s', [NVDA], [13,400,000], 1 days, 10, savings = true, smart = false, max) deposits 10 x (13.4e6 + 100,000). vault.accrue(100) raises the share price to 1.01. Then Alice calls setSmartBuys(id, true, max): required rises by 10 x 500 = 5,000 units, which are pulled and deposited strictly. Expected: smart buys on, 5,000 units pulled. Actual: previewRedeem(minted) = 4,999 and 4,999 + 0 < 5,000, so it reverts with BadVaultDeposit().

### 9. Info: The minimum fee absorbs the smart-buys premium: baskets up to $13.33 per buy get smart buys for free, and up to $20 for less than the premium

`contracts/src/DCAC.sol:833`

```
        return Math.max(spent * bps / BPS, floor);
```

From audit_math d4a9584c. The premium is added to the rate before the floor is applied: fee = max(spent x (feeBps + smartFeeBps) / 10,000, minFee). For spent <= 13,333,333 the fee is the 100,000 floor with or without smart buys, so the premium is 0, and setSmartBuys resizes the budget by 0. Between $13.33 and $20 only part of the premium is charged. If the premium is meant to apply to every smart buy, use max(spent x feeBps / 10,000, minFee) + spent x smartFeeBps / 10,000, and size _required the same way. Otherwise, document that the premium is free under the floor.

**Reproduction**

Ran my repro (test/scratch/Repro.t.sol test_minFeeSwallowsPremium): createPlan([NVDA], [13e6], 1 days, 10) with smart = false deposits 131,000,000, and the same plan with smart = true also deposits 131,000,000. Every buy pays 100,000 either way. The assertion that the smart plan pays more fails: '131000000 <= 131000000'.

### 10. Info: AerodromeCLAdapter.MAX_SQRT_RATIO is not the pool's constant (40 digits instead of 49): token1-to-token0 swaps get a price limit at about tick 472,800

`contracts/src/adapters/AerodromeCLAdapter.sol:35`

```
    uint160 internal constant MAX_SQRT_RATIO = 1461446703485210103287233237081398096342;
```

Merged from audit_flow 7aa483e6 and audit_math 7dee64eb. The Uniswap v3 / Slipstream maximum is 1461446703485210103287273052203988822378723970342, which is what this repository's TickMath.getSqrtPriceAtTick(887272) returns. The adapter's value is about 1e9 times smaller and is passed as MAX_SQRT_RATIO - 1 for every zeroForOne = false swap (line 81). It has no effect at today's prices: only WETH/USDC has USDC as token1, at sqrtPriceX96 of about 3e24, and stock tokens and cbBTC sort above USDC and use the correct MIN_SQRT_RATIO + 1. A pair priced above about tick 472,800 could not be bought, because the pool rejects a limit that is not above the current price. Fix: use 1461446703485210103287273052203988822378723970342.

**Reproduction**

Ran my repro (test/scratch/Repro.t.sol test_maxSqrtRatioConstant). TickMath.getSqrtPriceAtTick(887272) == 1461446703485210103287273052203988822378723970342, while the adapter constant is 1461446703485210103287233237081398096342, so the comparison fails. Failing input: a factory pool with tokenIn = token1 and slot0.sqrtPriceX96 >= 1461446703485210103287233237081398096341; adapter.swap reverts on the pool's price-limit check and DCAC records LegSkipped(reason 2).

### 11. Info: GAS_VAULT (400k) is below what the mainnet savings vault costs (one previewRedeem is ~300k): gasFor is a floor, not an upper bound, for savings plans

`contracts/src/DCAC.sol:53`

```
    uint256 public constant GAS_VAULT = 400_000;
```

Merged from audit_permissions 7afe1634 and audit_math 4d1858e4. One savings run calls previewRedeem (_valueOf), previewWithdraw + redeem (the buy), previewWithdraw + redeem (the fee), deposit when a leg was skipped, and redeem again at close. On Gauntlet USDC Prime a single cold previewRedeem is about 300k gas, so a 1-leg savings plan can pass the gasleft() >= gasFor(id) = 1,350,000 check and then run out of gas. I checked the harmful version, where a try/catch swallows an out-of-gas vault or swap call and the run 'succeeds' with work skipped. After such a failure only 1/64 of the forwarded gas is left, too little for the storage writes, transfers and re-deposit that follow, so the whole transaction reverts, and the lowest gas limit that passes does all the work. The keeper sizes its transactions by simulation, so nothing breaks today. Only a keeper that derived its gas limit from gasFor would revert every time. Fix: raise GAS_VAULT to the measured worst case for the vault in use (about 1.2M per the math specialist), or make it an owner-set per-vault value.

**Reproduction**

cast estimate 0xeE8F4eC5672F09119b96Ab6fB59C27E1b7e44b61 'previewRedeem(uint256)' 1000000000000000000000 --rpc-url https://mainnet.base.org returned 320588 (about 300k after the 21k intrinsic) on 2026-11-27. Expected from GAS_VAULT: all vault work of one run within 400,000. Actual: one view call uses about 300k, and a run makes at least five vault calls. Not run end to end: the stock tokens are B20 precompiles a Foundry fork cannot execute.

---

Judge's submission `19f19e6b4595618410227e3dca68d8de00f6ec5cec975b36beeabb153f640387`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
