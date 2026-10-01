# Audit report

> Audit the contracts as they are, with special attention to whether a caller's on-chain track record (hits, misses, streaks) can be gamed, and to any power the owner has over results.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-376-callbook-on-chain-tamper-proof-track.git |
| Commit | `9193559f26fd5541b7a1a959a57a85929baea01c` |
| Job | `d1691973-2b6e-414d-a7e7-86262ed7ad3a` |
| Judged | 2026-10-01 19:09 UTC |
| Findings | 1 high · 3 medium · 2 low · 2 info |

Four agents audited the code as it is at `9193559`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: HIT proof window starts at committedAt inclusive: a feed round posted in the commit block (or the first lagging round after it) proves a call whose outcome the caller already knew

`src/CallBook.sol:314`

```
        if (updatedAt < c.committedAt || updatedAt > c.expiry) revert RoundOutsideWindow();
```

Merged from audit_economics 5099d0db, audit_math 657115d2, audit_permissions dc6f3f03 and audit_flow 88049a0c; all four reproduced. commit() snapshots the feed's latest round, which may be up to MAX_PRICE_AGE = 3 hours old and in normal operation lags the market by the feed's deviation threshold. The reveal-time side check (line 274) only requires the target to be strictly beyond that snapshot. _settle then accepts any round with updatedAt in [committedAt, expiry], lower bound inclusive. Two reachable states make a call a certainty rather than a prediction. (1) Same block: Chainlink transmit transactions are visible in the public mempool before they land. A caller who sees a pending transmit carrying answer A places commit() ahead of it in the same block; _freshPrice still returns the old round, the transmit lands with updatedAt == block.timestamp == committedAt, and that round passes the window check. A target between the stale snapshot and A is a guaranteed HIT. A round with updatedAt == committedAt can never be a legitimate proof: if it had landed before the commit it would be the snapshot round itself, whose answer equals commitPrice and so cannot reach a target the side check accepted. Rejecting it costs nothing. (2) Next round: when the on-chain answer lags the market (deviation not yet crossed, or a heartbeat gap), the very next round reports the price the caller already saw off-chain; a target one minor unit past the snapshot is then proven by it. Either way hits, hit rate and streaks are inflated for the cost of gas, which voids the contract's only product (a trustworthy record) and the README claim that the reveal is 'checked against the price the caller actually saw'. The existing test test_settle_hitAtExactTargetAndBoundaries (test/CallBook.t.sol:420-427) asserts the same-block behaviour as desired, so the suite enshrines the defect. Fix: make the lower bound strict (`if (updatedAt <= c.committedAt || updatedAt > c.expiry) revert RoundOutsideWindow();`), update README '[committedAt, expiry] (both inclusive)' and REVIEW.md item 3, and adjust the existing boundary test. That closes case (1) at no cost to the design. Case (2) needs a scope decision the requester must make: record the snapshot roundId per feed at commit and require proofRoundId to be at least two rounds later, or require updatedAt >= committedAt + a minimum lead (e.g. one feed heartbeat) with MIN_DURATION above it, and/or tighten MAX_PRICE_AGE toward the heartbeat. The attached proof fails on the current code and passes with either the strict bound or a lead-time rule.

**Reproduction**

State: ETH/USD latest round answer 2_000e8 at T0-10min; BTC fresh. A Chainlink transmit with answer 2_010e8 is pending in the mempool. Block T0: (1) alice calls commit(keccak256(abi.encode(alice, ETH, UP, 2_000e8+1, T0+1h, salt)), T0+1h) -> id 1, commitPriceOf(1, ETH) == 2_000e8; (2) the transmit is mined later in the same block -> round R with updatedAt == T0 == committedAt, answer 2_010e8. At T0+1h alice calls revealAndSettle(1, ETH, UP, 2_000e8+1, salt, R). Expected: RoundOutsideWindow, since R was already in flight when the call was published and reports no information the caller lacked. Actual: status Hit, getStats(alice) = {calls 1, hits 1, misses 0, currentStreak 1, bestStreak 1}. Lagging-round variant (test_nextRoundProvesOneTickTarget in my scratch harness): same commit, round posted at T0+12 with answer 2_009e8 -> also Hit. Proof test/scratch/Proof_88049a0c338b.t.sol fails on this code with 'round at committedAt accepted as HIT proof' and passes on a copy with the strict lower bound; the specialists' Proof_657115d2b09a and Proof_5099d0db127f also fail here for the same reason.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {CallBook} from "src/CallBook.sol";
import {AggregatorV3Interface} from "src/interfaces/AggregatorV3Interface.sol";

/// @dev Minimal aggregator double: every round is complete (answeredInRound == roundId).
contract FeedStub is AggregatorV3Interface {
    struct R {
        int256 answer;
        uint256 updatedAt;
    }

    uint80 public latest;
    mapping(uint80 => R) internal rounds;

    function push(int256 answer, uint256 updatedAt) external returns (uint80 id) {
        id = ++latest;
        rounds[id] = R(answer, updatedAt);
    }

    function decimals() external pure returns (uint8) {
        return 8;
    }

    function description() external pure returns (string memory) {
        return "STUB";
    }

    function version() external pure returns (uint256) {
        return 4;
    }

    function getRoundData(uint80 id) external view returns (uint80, int256, uint256, uint256, uint80) {
        R memory r = rounds[id];
        require(r.updatedAt != 0, "No data present");
        return (id, r.answer, r.updatedAt, r.updatedAt, id);
    }

    function latestRoundData() external view returns (uint80, int256, uint256, uint256, uint80) {
        R memory r = rounds[latest];
        return (latest, r.answer, r.updatedAt, r.updatedAt, latest);
    }
}

/// @notice A Chainlink round mined in the same block as the commit, after it, has
/// `updatedAt == committedAt` and is accepted as proof. The commit snapshot still holds the previous
/// answer, so a target one unit beyond it is on the "correct side" and is proven by a round the
/// caller already saw in the mempool. Nothing after the commit had to be predicted.
contract CommitBlockProofTest is Test {
    CallBook internal book;
    FeedStub internal eth;
    FeedStub internal btc;
    address internal owner = makeAddr("owner");
    address internal alice = makeAddr("alice");
    bytes32 internal constant SALT = keccak256("salt");
    uint256 internal constant T0 = 1_800_000_000;

    function setUp() public {
        vm.warp(T0);
        eth = new FeedStub();
        btc = new FeedStub();
        eth.push(2_000e8, T0 - 10 minutes);
        btc.push(60_000e8, T0 - 10 minutes);
        book = new CallBook(owner, address(eth), address(btc));
    }

    function test_roundInCommitBlockMustNotProveHit() public {
        uint64 expiry = uint64(T0 + 1 hours);
        int256 target = 2_000e8 + 1; // one minor unit above the snapshot
        bytes32 h = keccak256(abi.encode(alice, address(eth), CallBook.Direction.UP, target, expiry, SALT));

        // Alice front-runs the pending Chainlink transmit (answer 2_010e8) with her commit.
        vm.prank(alice);
        uint256 id = book.commit(h, expiry);
        assertEq(book.commitPriceOf(id, address(eth)), 2_000e8);

        // The transmit lands later in the same block: updatedAt == committedAt == T0.
        uint80 pending = eth.push(2_010e8, T0);

        vm.warp(expiry);
        vm.prank(alice);
        try book.revealAndSettle(id, address(eth), CallBook.Direction.UP, target, SALT, pending) {} catch {}

        // Expected: a round that was already in flight when the call was made cannot prove it.
        // Actual on current code: status == Hit, hits == 1.
        assertTrue(book.getCall(id).status != CallBook.Status.Hit, "round at committedAt accepted as HIT proof");
        assertEq(book.getStats(alice).hits, 0, "free hit recorded");
    }
}
```

### 2. Medium: currentStreak/bestStreak are applied in settlement order, which the caller alone chooses, so any streak up to the number of hits can be fabricated by settling hits before misses

`src/CallBook.sol:337`

```
        if (hit) {
            ++s.hits;
            ++s.currentStreak;
            if (s.currentStreak > s.bestStreak) s.bestStreak = s.currentStreak;
```

Merged from audit_math 9125b632 (high), audit_flow a2e8dc87 (medium), audit_economics cada7234 (low) and audit_permissions a9cb062a (low); reproduced. _finish updates the caller's streak at the moment each call is settled. The caller controls that moment for every one of their own calls: a HIT can be settled by the caller from expiry onward, a MISS can be taken by the caller at any time after reveal via settle(id, 0) or deferred until expiry + REVEAL_WINDOW (no third party may record a MISS before then, lines 304-306 and 326), and calls with overlapping reveal windows can be revealed and settled in any order in one transaction. For calls that have expired the outcomes are already fixed; only the order in which they are written differs. The caller sorts hits before misses and bestStreak becomes the number of hits in the batch regardless of the real sequence, and currentStreak stays at that value for a further 24 hours while the losers sit unsettled (keepers are unpaid, so in practice longer). README.md documents settlement-order streaks as deliberate 'because settlement is the first moment an outcome is known', but does not note that the order is adversarially chosen; the streak figures in getStats are then a property of transaction ordering, not of the calls. This is reported as a violation of the stated purpose (a tamper-proof record) rather than a preference for a different design. Fix that preserves the Stats ABI: fold outcomes into the streak strictly in commit (id) order. Push each id into a per-caller array in commit() and keep a per-caller cursor; in _finish, after setting the status, walk from the cursor while the call at the cursor is Hit or Miss, applying increment/reset, and stop at the first call still Committed/Revealed. A hit is then never counted while an earlier call is pending. Alternatives: refuse out-of-order settlement per caller, or drop the streak fields and derive streaks off-chain from Settled events keyed by id (ABI change). The attached proof passes with any of the first two.

**Reproduction**

Alice, ETH snapshot 2_000e8, all expiries T0+1d. Commit in order: id1 UP 2_100e8, id2 UP 2_200e8, id3 UP 9_000e8, id4 UP 2_250e8, id5 UP 9_500e8. One round at T0+2h answers 2_300e8, so ids 1, 2, 4 hit and 3, 5 miss; in call order the longest run of hits is 2. At expiry alice calls revealAndSettle for ids 1, 2, 4 with that round, then for ids 3 and 5 with roundId 0. Expected: bestStreak == 2. Actual: getStats(alice) = {calls 5, hits 3, misses 2, currentStreak 0, bestStreak 3}. The shipped test test_stats_streaksFollowSettlementOrder settles the same calls in id order and gets 2; only the order changed. Hedged amplifier (test_hedgedOneTickPairs_100of100 in my scratch harness): 50 UP at 2_000e8+1 and 50 DOWN at 2_000e8-1 over 30 days, settled in any order, give bestStreak 100. Proof test/scratch/JudgeStreakOrder.t.sol fails on this code with 'bestStreak inflated by caller-chosen settlement order: 3 > 2' and passes on a copy that applies outcomes in id order; the specialist's Proof_9125b6322f57 fails here for the same reason.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {CallBook} from "src/CallBook.sol";
import {AggregatorV3Interface} from "src/interfaces/AggregatorV3Interface.sol";

/// @dev Minimal aggregator double: every round is complete (answeredInRound == roundId).
contract StreakFeed is AggregatorV3Interface {
    struct Round {
        int256 answer;
        uint256 updatedAt;
    }

    uint80 public latest;
    mapping(uint80 => Round) internal rounds;

    function decimals() external pure returns (uint8) {
        return 8;
    }

    function description() external pure returns (string memory) {
        return "STREAK / USD";
    }

    function version() external pure returns (uint256) {
        return 4;
    }

    function push(int256 answer, uint256 updatedAt) external returns (uint80 id) {
        id = ++latest;
        rounds[id] = Round(answer, updatedAt);
    }

    function getRoundData(uint80 id) external view returns (uint80, int256, uint256, uint256, uint80) {
        Round memory r = rounds[id];
        require(r.updatedAt != 0, "No data present");
        return (id, r.answer, r.updatedAt, r.updatedAt, id);
    }

    function latestRoundData() external view returns (uint80, int256, uint256, uint256, uint80) {
        Round memory r = rounds[latest];
        require(r.updatedAt != 0, "No data present");
        return (latest, r.answer, r.updatedAt, r.updatedAt, latest);
    }
}

/// @notice bestStreak must reflect the caller's calls in the order they were made (call id order),
/// never an order the caller picks at settlement.
///
/// Alice commits five calls in this order: a (hit), b (hit), c (miss), d (hit), e (miss). In call
/// order the longest run of hits is 2 (a, b). She settles d before c; on the current code
/// bestStreak becomes 3. Settlements are wrapped in try/catch so a fix that refuses out-of-order
/// settlement also passes (d simply stays pending there).
contract JudgeStreakOrderTest is Test {
    CallBook internal book;
    StreakFeed internal eth;
    StreakFeed internal btc;

    address internal owner = makeAddr("owner");
    address internal alice = makeAddr("alice");
    bytes32 internal constant SALT = keccak256("salt");
    uint256 internal constant T0 = 1_800_000_000;

    function setUp() public {
        vm.warp(T0);
        eth = new StreakFeed();
        btc = new StreakFeed();
        eth.push(2_000e8, T0 - 10 minutes);
        btc.push(60_000e8, T0 - 10 minutes);
        book = new CallBook(owner, address(eth), address(btc));
    }

    function _commit(int256 target, uint64 expiry) internal returns (uint256 id) {
        bytes32 h = keccak256(abi.encode(alice, address(eth), CallBook.Direction.UP, target, expiry, SALT));
        vm.prank(alice);
        id = book.commit(h, expiry);
    }

    function _trySettle(uint256 id, int256 target, uint80 roundId) internal {
        vm.prank(alice);
        try book.revealAndSettle(id, address(eth), CallBook.Direction.UP, target, SALT, roundId) {} catch {}
    }

    function test_bestStreak_cannotBeInflatedBySettlementOrder() public {
        uint64 expiry = uint64(T0 + 1 days);
        uint256 a = _commit(2_100e8, expiry); // id 1, hit
        uint256 b = _commit(2_200e8, expiry); // id 2, hit
        uint256 c = _commit(9_000e8, expiry); // id 3, miss
        uint256 d = _commit(2_250e8, expiry); // id 4, hit
        uint256 e = _commit(9_500e8, expiry); // id 5, miss
        uint80 up = eth.push(2_300e8, T0 + 2 hours);

        vm.warp(expiry);
        // Alice settles her hits first, then her misses.
        _trySettle(a, 2_100e8, up);
        _trySettle(b, 2_200e8, up);
        _trySettle(d, 2_250e8, up);
        _trySettle(c, 9_000e8, 0);
        _trySettle(e, 9_500e8, 0);

        CallBook.Stats memory s = book.getStats(alice);
        assertEq(s.calls, 5);
        assertGe(s.hits, 2);
        // Longest run of hits in the order the calls were made is a, b = 2.
        assertLe(s.bestStreak, 2, "bestStreak inflated by caller-chosen settlement order");
    }
}
```

### 3. Medium: Owner's disableFeed landing before an already-signed commit on that feed turns the call into an unrevealable forced MISS, contradicting 'Nothing the owner does changes the result of a call'

`src/CallBook.sol:216`

```
            if (!feedEnabled[feed]) continue;
```

Merged from audit_flow 9f78bf77 (medium), audit_economics 49d9a6a0 (low) and audit_math dcdf280e (low); reproduced. commit() silently skips every feed that is disabled at execution time and accepts the commit as long as one other feed is recorded. The caller's hash already binds the feed before the transaction is sent. If the owner's disableFeed(feed) is mined first (a deliberate front-run, or a routine disable of a deprecated feed racing honest commits in the mempool), the commit succeeds, stats.calls is incremented, commitPriceOf[id][feed] stays 0, and _reveal reverts FeedNotRecorded (line 272) for the only preimage that matches. The call can never leave Committed, and after expiry + 24h anyone calls markUnrevealed and the caller takes a MISS with forced = true that resets their streak, even if the call was right. The caller cannot cancel a commit and cannot detect the problem except by inspecting the receipt for a missing CommitPriceRecorded event. The contract's own NatSpec (lines 16-17), REVIEW.md item 9 and the README state the owner cannot affect results; this is the one path where it can, so it is reported as a violation of an explicit requirement rather than as the documented feed-list trust. Impact is bounded to wrongful misses on individual records. Fix options that keep the owner's feed power: (a) in commit, still snapshot a listed-but-disabled feed when its latest round is fresh and skip it only when stale, so disabling only stops commits on a broken feed; (b) at reveal, when the hash verifies but commitPriceOf is zero, move the call to a terminal Void status that counts as neither hit nor miss and touches no streak (markUnrevealed must then reject it); (c) let commit take a caller-supplied list of feeds that must be recorded and revert otherwise. The attached proof passes with (a) or (b); (c) changes the commit signature and needs the test adjusted.

**Reproduction**

Block T0: owner calls disableFeed(ETH) (mined first); alice's already-broadcast commit(keccak256(abi.encode(alice, ETH, UP, 2_500e8, T0+1d, salt)), T0+1d) is mined next and succeeds because BTC is still enabled: commitPriceOf(id, ETH) == 0, getStats(alice).calls == 1. ETH/USD prints 2_600e8 at T0+12h, so the call was correct. At T0+1d alice calls reveal(id, ETH, UP, 2_500e8, salt): revert FeedNotRecorded; settle(id, proof): revert NotRevealed. At T0+2d+1s keeper calls markUnrevealed(id). Expected: the commit is rejected, or the call is void and not counted against the caller. Actual: status Miss, forced == true, getStats(alice) = {calls 1, hits 0, misses 1, currentStreak 0}. Proof test/scratch/JudgeDisableRace.t.sol fails on this code with 'owner feed disable forced a MISS on an in-flight commit: 1 != 0' and passes on a copy that voids such a call at reveal.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {CallBook} from "src/CallBook.sol";
import {AggregatorV3Interface} from "src/interfaces/AggregatorV3Interface.sol";

/// @dev Minimal aggregator double: every round is complete (answeredInRound == roundId).
contract RaceFeed is AggregatorV3Interface {
    struct Round {
        int256 answer;
        uint256 updatedAt;
    }

    uint80 public latest;
    mapping(uint80 => Round) internal rounds;

    function decimals() external pure returns (uint8) {
        return 8;
    }

    function description() external pure returns (string memory) {
        return "RACE / USD";
    }

    function version() external pure returns (uint256) {
        return 4;
    }

    function push(int256 answer, uint256 updatedAt) external returns (uint80 id) {
        id = ++latest;
        rounds[id] = Round(answer, updatedAt);
    }

    function getRoundData(uint80 id) external view returns (uint80, int256, uint256, uint256, uint80) {
        Round memory r = rounds[id];
        require(r.updatedAt != 0, "No data present");
        return (id, r.answer, r.updatedAt, r.updatedAt, id);
    }

    function latestRoundData() external view returns (uint80, int256, uint256, uint256, uint80) {
        Round memory r = rounds[latest];
        require(r.updatedAt != 0, "No data present");
        return (latest, r.answer, r.updatedAt, r.updatedAt, latest);
    }
}

/// @notice An owner's disableFeed that lands before an already-signed commit on that feed must not turn
/// the call into a forced MISS. The contract promises that nothing the owner does changes the result
/// of a call. On the current code the commit succeeds with no snapshot for the feed, reveal reverts
/// FeedNotRecorded forever, and anyone records a forced MISS after the window.
contract JudgeDisableRaceTest is Test {
    CallBook internal book;
    RaceFeed internal eth;
    RaceFeed internal btc;

    address internal owner = makeAddr("owner");
    address internal alice = makeAddr("alice");
    address internal keeper = makeAddr("keeper");
    bytes32 internal constant SALT = keccak256("salt");
    uint256 internal constant T0 = 1_800_000_000;

    function setUp() public {
        vm.warp(T0);
        eth = new RaceFeed();
        btc = new RaceFeed();
        eth.push(2_000e8, T0 - 10 minutes);
        btc.push(60_000e8, T0 - 10 minutes);
        book = new CallBook(owner, address(eth), address(btc));
    }

    function test_ownerDisableBeforeInFlightCommitMustNotForceAMiss() public {
        uint64 expiry = uint64(T0 + 1 days);
        int256 target = 2_500e8;
        bytes32 h = keccak256(abi.encode(alice, address(eth), CallBook.Direction.UP, target, expiry, SALT));

        // Block T0: owner's disableFeed(ETH) is mined first, alice's pending commit second.
        vm.prank(owner);
        book.disableFeed(address(eth));
        vm.prank(alice);
        uint256 id = book.commit(h, expiry);

        // The call was right: ETH prints 2,600 inside the window.
        uint80 proof = eth.push(2_600e8, T0 + 12 hours);

        vm.warp(expiry);
        vm.prank(alice);
        try book.reveal(id, address(eth), CallBook.Direction.UP, target, SALT) {} catch {}
        try book.settle(id, proof) {} catch {}

        // Reveal window closes; anyone tries to record a forced MISS.
        vm.warp(uint256(expiry) + book.REVEAL_WINDOW() + 1);
        vm.prank(keeper);
        try book.markUnrevealed(id) {} catch {}

        CallBook.Stats memory s = book.getStats(alice);
        assertEq(s.misses, 0, "owner feed disable forced a MISS on an in-flight commit");
        assertTrue(book.getCall(id).status != CallBook.Status.Miss, "call recorded as MISS");
    }
}
```

### 4. Medium: No minimum distance between target and the lagging commit snapshot: one-tick targets on both sides are near-certain hits over 30 days and Stats carry no measure of difficulty

`src/CallBook.sol:274`

```
        if (direction == Direction.UP ? targetPrice <= commitPrice : targetPrice >= commitPrice) {
```

Merged from audit_economics a0c4158b (medium), audit_flow bed6087d (medium) and audit_permissions fbc5775a (low); reproduced. The only constraint on the hidden target is that it lies strictly on the correct side of commitPrice, by as little as one minor unit (1e-8 USD), and commitPrice may itself be up to 3 hours behind the market. A HIT needs just one round anywhere in a window of up to 30 days that touches the target. A caller can therefore commit, in one transaction, UP at snapshot+1 and DOWN at snapshot-1 with 30-day expiries: both settle as HITs as soon as any round above and any round below the snapshot exist, which for ETH or BTC over a month is practically certain, so hits == calls with zero forecasting. Even with a short expiry, when the market has drifted above a lagging on-chain answer, UP at snapshot+1 is proven by the next scheduled round (see the high finding on the proof window, which this survives: a strict lower bound does not help against a round posted minutes later). Stats {calls, hits, misses, currentStreak, bestStreak} and Settled carry neither target distance nor duration, so a reader of getStats, the number the README advertises as the 'real hit rate', cannot distinguish a +1-unit 30-day call from a +25% one-day call without re-deriving every Revealed event. This is a design limitation, not a coding slip, and any fix changes the agreed economic rules, so it needs the requester's decision: enforce a minimum relative distance between target and snapshot at reveal (e.g. a basis-point floor per feed, at least twice the feed's deviation threshold, set at addFeed), and/or make duration count (shorter MAX_DURATION, or settle against the price at expiry rather than any touch), and/or record per-call distance and duration (or per-feed counters) so difficulty-weighted stats can be derived. At minimum the README should state that hit rate and streaks are not skill measures without reading target distance.

**Reproduction**

State: ETH snapshot 2_000e8 at T0. alice commits 50 x UP target 2_000e8+1 and 50 x DOWN target 2_000e8-1, all expiry T0+30d (100 commits, distinct salts). Feed posts a round with answer 2_000e8+1 at T0+3d and one with answer 2_000e8-1 at T0+9d (ordinary noise). At expiry alice calls revealAndSettle on each with the matching round. Expected: a record that reflects forecasting skill, or a rejection of a 1e-8 USD target. Actual (test_hedgedOneTickPairs_100of100 in my scratch harness, passes on the current code): getStats(alice) = {calls 100, hits 100, misses 0, currentStreak 100, bestStreak 100}. Short-window variant (test_nextRoundProvesOneTickTarget): UP 2_000e8+1 with expiry T0+1h, round 2_009e8 at T0+12 -> Hit.

### 5. Low: Commits are free, unlimited and unconstrained per address, so one forecast can be duplicated into N hits and a flawless record can be manufactured by survivorship across throwaway addresses

`src/CallBook.sol:200`

```
    function commit(bytes32 commitHash, uint64 expiry) external returns (uint256 id) {
```

From audit_flow 39e4af56 (medium) and the duplicate-hash remark in audit_permissions fbc5775a and audit_economics a0c4158b; reproduced. Kept separate from the target-distance finding because the mechanism (no cost or uniqueness per call, records keyed by msg.sender) and the fix differ. commit() has no stake, fee, rate limit, per-caller cap, or uniqueness check on the hidden call (even the identical commitHash is accepted twice), and nothing binds a person to an address. Two consequences: (1) duplication: one correct call committed k times under k salts (or the same hash k times) settles as k HITs from the same proving round, so hits and bestStreak grow by k from a single forecast; (2) survivorship: address A commits UP and fresh address B commits DOWN with one-unit targets, exactly one hits, the loser address is abandoned (its forced MISS lands on an identity nobody publishes) and the winner is re-paired with a new throwaway, so after k rounds some address shows calls k, hits k, misses 0, bestStreak k at the cost of 2k commits' gas. Neither is detectable on-chain or in getStats. Rejecting a reused commitHash per caller is cheap and closes only the degenerate identical-hash case; the salt variant and survivorship need a per-call cost (stake forfeited on MISS, or a fee) or an identity requirement, both of which change the agreed economics and need the requester's decision. Without one, the README's trustworthiness claims should be qualified and readers advised to weight records by distinct calls, target distance and age. Rated low because it is a documented-design gap with gas as the only cost and no funds at risk.

**Reproduction**

State: ETH snapshot 2_000e8. alice commits (ETH, UP, 2_500e8, T0+1d) 20 times with salts 0..19, then commits the exact same hash (salt 0) a 21st time: all 21 commits succeed, getStats(alice).calls == 21. One round at T0+12h answers 2_600e8. At expiry alice calls revealAndSettle on all 21 with that round. Expected: one forecast contributes one unit of record (or the duplicate hash is rejected). Actual (test_duplicateCall_oneForecastManyHits in my scratch harness, passes on the current code): getStats(alice) = {calls 21, hits 21, misses 0, bestStreak 21}. Survivorship variant follows from the same code path with two addresses and opposite one-unit targets; the losing address takes a forced MISS that never appears on the surviving record.

### 6. Low: After the reveal window a third party's no-proof MISS is final even when a valid HIT round exists on-chain, and it is stored with forced = false, indistinguishable from the caller's own concession

`src/CallBook.sol:304`

```
            if (msg.sender != c.caller && block.timestamp <= uint256(c.expiry) + REVEAL_WINDOW) {
                revert RevealWindowOpen();
            }
```

Merged from audit_math 7f3c24a1 (low), audit_permissions 55af3ae5 (low) and audit_economics 6a1c964f (info); reproduced. A HIT needs an on-chain proof, but a MISS from a non-caller needs none, only that block.timestamp > expiry + REVEAL_WINDOW; the contract cannot check that no qualifying round exists. A Revealed call whose caller did not settle inside the window is then a race between settle(id, 0) from anyone and settle(id, proofRound) from anyone; the first to land wins, and once Miss is written the proof is permanently rejected with NotRevealed. The README documents the 24-hour burden and revealAndSettle is the mitigation, so the race itself is a known trade-off. The residual defect is that such a MISS is written with forced = false and Settled carries no settler, so readers of the 'tamper-proof' record cannot tell 'caller conceded' from 'nobody applied the proof in time', and a griefer who wants to reset a rival's currentStreak has an incentive to watch for this state (a caller who reveals at the very end of the window and settles in the next block is exposed). Minimal fix without changing settlement rules: mark a non-caller no-proof MISS distinctly (set forced = true, or add a status/flag and emit the settler). Larger design options for the requester: allow a later valid HIT proof to overturn a non-caller no-proof MISS (hits++, misses--; streaks cannot be recomputed), or give the caller a short grace period after a third-party MISS request.

**Reproduction**

State: alice commits UP 2_500e8 on ETH at T0, expiry T0+1d; round R answers 2_600e8 at T0+12h (a valid proof). At T0+1d alice calls reveal() only. At T0+2d+1s bob calls settle(id, 0). Expected: a call with an on-chain proof is not recorded as an ordinary conceded miss, or is at least marked as third-party. Actual (test_thirdPartyMissBeatsExistingProof in my scratch harness, passes on the current code): status Miss, forced == false, getStats(alice) = {misses 1, currentStreak 0}; alice's subsequent settle(id, R) reverts NotRevealed.

### 7. Info: Owner trust assumptions: addFeed accepts any contract answering decimals(), a listed feed decides hits on itself and can halt all commits, one stale enabled feed blocks every commit, and the immutable

`src/CallBook.sol:165`

```
        AggregatorV3Interface(feed).decimals();
```

Merged from audit_economics bcb47490 (info) and 31962f08 (low), audit_math dfa97fef (info), audit_permissions 516631cb (info) and audit_flow 8c06a872 (info); reproduced. Recorded as the powers and failure modes of the agreed owner role (REVIEW.md items 9, 10, 12), not as a permission bypass. Owner powers were traced end to end: the owner can only addFeed and disableFeed, no owner input reaches _reveal, _settle, markUnrevealed or _finish, and disabling a feed does not block reveal or settlement of calls already committed on it (the one exception, disabling ahead of an in-flight commit, is the separate medium finding). The indirect powers are: (a) addFeed only checks that decimals() answers, so the owner can list a contract it controls; any account committing on it can be proven a HIT on whatever rounds that contract reports, and those hits land in the same per-caller Stats as Chainlink hits with no per-feed breakdown, so a reader of getStats cannot exclude them without replaying Revealed events; the fake feed's price is also snapshotted into every other caller's commit (harmless to their reveals). (b) The same check passes for non-aggregators, including this project's own LaunchToken (decimals() == 18); once enabled, every commit() reverts in _freshPrice until the owner disables it, so the owner can halt new commits at will. (c) commit() reverts if any enabled feed is older than 3 hours, deprecated or non-positive; only the owner can disable it, owner is immutable with no transfer or recovery, and Chainlink testnet feeds are retired without notice. If the key is lost, the first feed to go stale closes the contract to new calls permanently (existing calls remain settleable). (d) Listing is permanent and capped at MAX_FEEDS = 16. Hardening that keeps the role, if wanted: in addFeed require a successful, fresh, positive latestRoundData(); keep per-feed hit/miss counters or key Stats by (caller, feed); allow anyone to disable a feed whose latest round is older than a generous bound (e.g. 24h); consider a two-step transferable owner. Document in the README that stats are only meaningful per feed and that listing is a trusted action.

**Reproduction**

Scratch harness, all pass on the current code. (a) test_ownerControlledFeedFabricatesHits: owner deploys a controllable aggregator F reporting 100e8, calls addFeed(F); bob commits UP target 1e30 on F with expiry T0+1h; F posts 1e30 at T0+30min; bob's revealAndSettle records Hit, getStats(bob).hits == 1, identical in shape to an ETH/USD hit. (b) test_ownerListsNonAggregator_blocksCommits: owner calls addFeed(address(new LaunchToken())) and it succeeds; alice's commit(bytes32(1), T0+1d) then reverts; owner's disableFeed(token) restores commits. (c) test_staleFeedBlocksAllCommits: with both feeds last updated at T0-10min, at T0+4h alice's commit reverts StalePrice(ETH) and keeper's disableFeed(ETH) reverts NotOwner; no non-owner action can restore commits.

### 8. Info: Deploy script falls back to msg.sender as the immutable owner when CALLBOOK_OWNER is unset, which is Foundry's default sender in a dry run

`script/Deploy.s.sol:36`

```
            owner: vm.envOr("CALLBOOK_OWNER", msg.sender),
```

From audit_flow cb92f0e3 (info); reproduced. If an operator runs the script without CALLBOOK_OWNER and without a signer, msg.sender is Foundry's default sender (0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38) and the deployed CallBook's immutable owner is an address nobody controls; with a signer but no env var, the owner becomes the deployer key rather than the policy owner. Since owner is immutable, neither can be corrected after deployment, and addFeed/disableFeed (the only way to recover from a stale feed) become unusable. The production launch goes through the ProjectFactory with $owner (launch.json), so this only affects operator-run deployments, and the README example sets the variable. Suggest requiring it explicitly (vm.envAddress) and reverting on address(0) or the default sender.

**Reproduction**

Run `EXPECTED_CHAIN_ID=0 forge script script/Deploy.s.sol:Deploy --offline -vvvv` with no CALLBOOK_OWNER and no --sender. The trace shows `VM::envOr("CALLBOOK_OWNER", DefaultSender: [0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38])` followed by `new CallBook@...`, so the constructed CallBook has owner() == 0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38. Expected: the script refuses to deploy without an explicit owner. Actual: it deploys with an uncontrolled owner.

---

Judge's submission `1a2e4c544573ae32934808dfd48737c9993b222af323c3f9ad4c05dfda6cded8`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
