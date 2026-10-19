# Audit report

> Audit the contracts in AdamNakamoto/delivermail as they are.

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/delivermail.git |
| Commit | `28bd579c5ee6ed62aebddf409ca81d9b4b9c3048` |
| Job | `df86f727-72f7-40ae-9e05-585361fc9f3a` |
| Judged | 2026-10-19 14:56 UTC |
| Findings | 1 high · 3 medium · 4 low · 3 info |

Four agents audited the code as it is at `28bd579`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: postRoot accepts root == bytes32(0): the once-per-day guard never fires, a day can be re-posted without limit and the stranded totalPosted bricks the 16.8M play allocation

`p2e/contracts/src/DeliveryRewards.sol:91`

```
        if (days_[day].root != bytes32(0)) revert RootExists();
```

postRoot decides 'already posted' from days_[day].root != 0 but never rejects root == bytes32(0). A zero-root post passes every check, adds total to totalPosted and writes days_[day] = Day(0, total, 0), yet the day still reads as unposted, so the same closed day can be posted again and again (guarantee 4 broken). days_[day].total keeps only the latest value, so revokeRoot(day) gives back only that one total; nothing else ever lowers totalPosted. One transaction from the poster key (a hot settlement key AUDIT.md expects can leak; its listed mitigations revokeRoot/pause/rotate all assume damage is revocable) can push totalPosted to ~16.8M with 102 posts of day 0, after which every honest postRoot with total > 0 reverts AllocationExhausted forever. MailToken.setMinter is one-shot, so a replacement DeliveryRewards cannot be wired: the play allocation can never be minted. Reported by three specialists (math, flow, economics); merged. Fix: in postRoot add `if (root == bytes32(0)) revert NoRoot();` (or track posting with a separate flag). The attached proof fails on this code and passes with that one line (verified against a patched copy).

**Reproduction**

Deploy as in test/P2E.t.sol (dayLength 1 day, DAILY = 16.8M/102, halvingDays 51); warp 3 days. As poster call postRoot(0, bytes32(0), DAILY) in a loop. Expected: the second call reverts RootExists. Actual: all 102 succeed, totalPosted = 16,799,999.99e18, the 103rd reverts AllocationExhausted. Owner calls revokeRoot(0): expected totalPosted back to 0, actual 16,635,294.1e18 (101 x DAILY stranded). Honest postRoot(0..2, leaf, DAILY) then fails with AllocationExhausted. Run: cd p2e/contracts && forge test --match-path test/scratch/ZeroRootRepost.t.sol -> FAIL 'revoking the only posted day must release everything it added: 16635294117647058823529388 != 0'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {MailToken} from "src/MailToken.sol";
import {DeliveryRewards} from "src/DeliveryRewards.sol";

/// Finding: postRoot treats root == bytes32(0) as "no root", so the RootExists guard never fires for a
/// zero root. The same day can be posted again and again, each call adding `total` to totalPosted while
/// days_[day].total only remembers the latest one. revokeRoot can give back only that latest total, so
/// the play allocation is consumed irreversibly and later honest roots revert with AllocationExhausted.
contract ZeroRootRepostTest is Test {
    MailToken mail;
    DeliveryRewards rewards;

    address owner = makeAddr("owner");
    address poster = makeAddr("poster");
    address liquidity = makeAddr("liquidity");
    address alice = makeAddr("alice");

    uint256 constant DAILY = uint256(16_800_000e18) / 102;
    uint256 constant HALVING_DAYS = 51;

    function setUp() public {
        vm.startPrank(owner);
        mail = new MailToken(liquidity);
        rewards = new DeliveryRewards(mail, owner, poster, 1 days, DAILY, HALVING_DAYS);
        mail.setMinter(address(rewards));
        vm.stopPrank();
    }

    function test_ZeroRootRepostExhaustsAllocationIrreversibly() public {
        vm.warp(block.timestamp + 3 days); // days 0, 1 and 2 are closed

        // The poster key posts day 0 with a zero root as often as it likes (one tx): each call passes
        // RootExists because days_[0].root stays zero. 102 x DAILY = 16,799,999.99 MAIL < 16.8M.
        uint256 posts;
        vm.startPrank(poster);
        for (uint256 i; i < 102; ++i) {
            try rewards.postRoot(0, bytes32(0), DAILY) {
                ++posts;
            } catch {
                break;
            }
        }
        vm.stopPrank();
        emit log_named_uint("zero-root posts of day 0 accepted", posts);

        // The owner revokes the bad day. Expected: totalPosted returns to 0 (only one day was ever posted
        // and it is now revoked). Actual: 101 x DAILY is stuck in totalPosted with nothing to revoke.
        vm.prank(owner);
        rewards.revokeRoot(0);
        assertEq(rewards.totalPosted(), 0, "revoking the only posted day must release everything it added");

        // Expected after the fix: honest roots for days 0, 1 and 2 post normally.
        vm.startPrank(poster);
        rewards.postRoot(0, rewards.leaf(alice, 0, DAILY), DAILY);
        rewards.postRoot(1, rewards.leaf(alice, 1, DAILY), DAILY);
        rewards.postRoot(2, rewards.leaf(alice, 2, DAILY), DAILY);
        vm.stopPrank();
        assertEq(rewards.totalPosted(), 3 * DAILY);
    }
}
```

### 2. Medium: revokeRoot gates on the claimed sum and keeps claimed[day][*] flags: a zero-amount leaf claimed from a bad root permanently blocks that account's honest claim for the day

`p2e/contracts/src/DeliveryRewards.sol:101`

```
        if (days_[day].claimed != 0) revert AlreadyClaimedFrom();
        totalPosted -= days_[day].total;
        delete days_[day];
```

claim writes two coupled slots, claimed[day][account] = true and d.claimed += amount, and accepts amount == 0. revokeRoot decides 'nothing claimed yet' from d.claimed != 0 (an amount sum, not a claimant count) and deletes only days_[day]; the per-account flags survive. So a bad root with zero-amount leaves (exactly the leaked-poster-key case revokeRoot exists for, or a server export including 0-point players) lets anyone call the permissionless claim(victim, day, 0, proof) for each listed account: the flag is set, d.claimed stays 0, the owner's revoke still succeeds (contradicting guarantee 7), and once the corrected root is posted every flagged account reverts AlreadyClaimed for that day forever. Their earned MAIL for the day is never minted and there is no reset path. Reported by three specialists (math low, economics medium, permissions medium); merged. Fix: key the claim flag by root (mapping(bytes32 => mapping(address => bool))) or by a per-day version bumped in revokeRoot, and additionally reject amount == 0 in claim. The attached proof is fix-agnostic (the zero claim is a low-level call) and passes with the root-keyed mapping (verified against a patched copy).

**Reproduction**

Day 0 closed. 1) poster posts root R_bad built from leaf(alice,0,0) and leaf(bob,0,0), total 0. 2) griefer calls claim(alice, 0, 0, [leaf(bob,0,0)]) -> succeeds; claimed(0, alice) == true; days_(0).claimed == 0. 3) owner calls revokeRoot(0) -> succeeds. 4) poster posts honest root with leaf(alice,0,25_000e18), leaf(bob,0,15_000e18), total 40_000e18. 5) claim(alice, 0, 25_000e18, [leaf(bob,0,15_000e18)]). Expected: alice receives 25,000 MAIL. Actual: revert AlreadyClaimed(). Run: cd p2e/contracts && forge test --match-path test/scratch/RevokeKeepsClaimedFlags.t.sol -> FAIL AlreadyClaimed().

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {MailToken} from "src/MailToken.sol";
import {DeliveryRewards} from "src/DeliveryRewards.sol";

/// Finding: revokeRoot gates on the claimed SUM (days_[day].claimed != 0) and deletes only days_[day],
/// so a zero-amount leaf claimed from a bad root sets claimed[day][account] without blocking the revoke,
/// and the flag survives the re-post: the account can never claim the corrected root for that day.
/// Fix-agnostic: the zero claim is attempted with a low-level call (a fix may reject it), and the test
/// only asserts that after revoke + honest re-post the honest claim pays out.
contract RevokeKeepsClaimedFlagsTest is Test {
    MailToken mail;
    DeliveryRewards rewards;

    address owner = makeAddr("owner");
    address poster = makeAddr("poster");
    address liquidity = makeAddr("liquidity");
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");
    address griefer = makeAddr("griefer");

    uint256 constant DAILY = uint256(16_800_000e18) / 102;

    function setUp() public {
        vm.startPrank(owner);
        mail = new MailToken(liquidity);
        rewards = new DeliveryRewards(mail, owner, poster, 1 days, DAILY, 51);
        mail.setMinter(address(rewards));
        vm.stopPrank();
        vm.warp(block.timestamp + 1 days); // day 0 is closed
    }

    function _tree(address a, uint256 aAmt, address b, uint256 bAmt) internal view returns (bytes32 root, bytes32 la, bytes32 lb) {
        la = rewards.leaf(a, 0, aAmt);
        lb = rewards.leaf(b, 0, bAmt);
        root = la < lb ? keccak256(abi.encode(la, lb)) : keccak256(abi.encode(lb, la));
    }

    function test_HonestClaimSurvivesRevokeOfZeroLeafRoot() public {
        // 1. A bad root (leaked key or a server export with 0-point players) with zero-amount leaves.
        (bytes32 bad,, bytes32 lbBad) = _tree(alice, 0, bob, 0);
        vm.prank(poster);
        rewards.postRoot(0, bad, 0);

        // 2. Anyone claims the zero leaf for alice. On this code it succeeds and flags her.
        bytes32[] memory p = new bytes32[](1);
        p[0] = lbBad;
        vm.prank(griefer);
        (bool ok,) = address(rewards).call(abi.encodeCall(DeliveryRewards.claim, (alice, 0, 0, p)));
        emit log_named_uint("zero-amount claim accepted", ok ? 1 : 0);

        // 3. Owner withdraws the bad root (nothing was minted, so the revoke must be allowed or the
        //    zero claim must have been rejected; either way the honest flow below must work).
        vm.prank(owner);
        (bool revoked,) = address(rewards).call(abi.encodeCall(DeliveryRewards.revokeRoot, (0)));
        emit log_named_uint("revoke accepted", revoked ? 1 : 0);
        assertTrue(revoked, "revokeRoot must be possible when nothing was minted from the day");

        // 4. Poster posts the honest root for the same day.
        (bytes32 good,, bytes32 lbGood) = _tree(alice, 25_000e18, bob, 15_000e18);
        vm.prank(poster);
        rewards.postRoot(0, good, 40_000e18);

        // 5. Expected: alice receives 25,000 MAIL. Actual on this code: revert AlreadyClaimed().
        p[0] = lbGood;
        rewards.claim(alice, 0, 25_000e18, p);
        assertEq(mail.balanceOf(alice), 25_000e18, "honest allocation must be claimable after a revoke");
    }
}
```

### 3. Medium: Sliding 24h assign cooldown is not aligned to the reward day: one Messenger gives full stamina to two wallets in the same reward day, every day

`p2e/contracts/src/MailOffice.sol:141`

```
        if (last != 0 && block.timestamp < last + ASSIGN_COOLDOWN) revert TooSoon();
        lastAssignedAt[id] = block.timestamp;
```

The contract header, README and AUDIT.md guarantee 8 rely on 'a Messenger can join a wallet at most once per 24 h, so one NFT can't play for several wallets in a day'. The cooldown is a sliding window from lastAssignedAt[id], while the reward day the server meters stamina against (DeliveryRewards.currentDay, fixed windows from startTime; server game.js reads profileOf at sign-in and ledger.js counts entry.paid per wallet per day) is a fixed window. A Messenger assigned to wallet A at startTime + 12h gives A its full staminaOf for every reward day; at +36h (mid reward day 1, after A used its 12 paid deliveries) it can be unassigned, transferred and assigned to wallet B, who signs in with a fresh stamina of 12 and paid == 0 for the same reward day. Repeated daily (A <-> B alternating) one NFT yields two wallets' worth of full-point paid deliveries per reward day for the one-time cost of a second 0.005 ETH office, and since the day's budget is split by points the surplus comes out of every other player's share. Fix preserving the design: in assign, also reject a token that already joined any wallet during the current reward day (store lastAssignedDay[id] computed from the rewards contract's startTime/dayLength, or an owner-set day anchor), so a token joins at most one wallet per reward day.

**Reproduction**

Deploy as in test/P2E.t.sol; t0 = rewards.startTime(). vm.warp(t0 + 12 hours): alice opens an office and assign(1); bob opens an office. vm.warp(t0 + 36 hours): rewards.currentDay() == 1 and office.staminaOf(alice) == 12. alice calls unassign(), transferFrom(alice, bob, 1); bob calls assign(1). Expected: TooSoon (the token already played for a wallet in reward day 1). Actual: succeeds (36h - 12h == ASSIGN_COOLDOWN), rewards.currentDay() still 1, office.staminaOf(bob) == 12, office.staminaOf(alice) == 0. Run: cd p2e/contracts && forge test --match-path test/scratch/Judge.t.sol --match-test test_OneMessengerTwoWalletsSameRewardDay (passes on this code, asserting the exploit state).

### 4. Medium: DeliveryRewards constructor accepts dayLength == 0 or halvingDays == 0: the immutable divisors make every postRoot and the budget views panic forever, and the one-shot minter cannot be re-pointed

`p2e/contracts/src/DeliveryRewards.sol:63`

```
        dayLength = dayLength_;
        initialDaily = initialDaily_;
        halvingDays = halvingDays_;
```

dayLength and halvingDays are immutable and used as divisors in currentDay() ((block.timestamp - startTime) / dayLength) and dailyBudget() (day / halvingDays); initialDaily == 0 silently makes every budget 0. The constructor checks none of them. With a zero value every postRoot reverts with panic 0x12 and there is no setter. Because MailToken.setMinter works once and only for the deployer, a launch that wires such a DeliveryRewards as the minter permanently strands the 16.8M play allocation. AUDIT.md says there is no mainnet deploy script yet, so these parameters are typed by hand. Likelihood is operator error only, impact is an unrecoverable launch. Fix: in the constructor revert when dayLength_ == 0, halvingDays_ == 0 or initialDaily_ == 0 (custom error); zero runtime cost. The attached specialist proof fails on this code with the panic and passes once the constructor reverts.

**Reproduction**

new DeliveryRewards(mail, owner, poster, 1 days, DAILY, 0) deploys. Warp 1 day; as poster call postRoot(0, bytes32(uint256(1)), 1). Expected: a constructor revert. Actual: panic: division or modulo by zero (0x12) from dailyBudget(0); dailyBudget(anyDay) view panics too. Same with dayLength_ = 0 from currentDay(). Run: cd p2e/contracts && forge test --match-path test/scratch/CtorBounds.t.sol -> both tests FAIL with panic 0x12.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {MailToken} from "src/MailToken.sol";
import {DeliveryRewards} from "src/DeliveryRewards.sol";

/// Finding: the DeliveryRewards constructor accepts dayLength == 0 and halvingDays == 0. Both are
/// immutable divisors, so currentDay() / dailyBudget() panic with division by zero and postRoot can never
/// succeed. Because MailToken.setMinter is one-shot, wiring such a deployment as the minter strands the
/// whole 16.8M play allocation with no admin path to recover.
contract RewardsConstructorBoundsTest is Test {
    MailToken mail;
    address owner = makeAddr("owner");
    address poster = makeAddr("poster");
    address liquidity = makeAddr("liquidity");

    uint256 constant DAILY = uint256(16_800_000e18) / 102;

    function setUp() public {
        vm.prank(owner);
        mail = new MailToken(liquidity);
    }

    function test_ZeroHalvingDaysIsRejectedAtDeploy() public {
        // Expected: the constructor refuses a zero halving period. Actual: it deploys, and every
        // postRoot (and dailyBudget view) reverts with a division-by-zero panic forever.
        vm.prank(owner);
        try new DeliveryRewards(mail, owner, poster, 1 days, DAILY, 0) returns (DeliveryRewards r) {
            vm.warp(block.timestamp + 1 days);
            vm.prank(poster);
            r.postRoot(0, bytes32(uint256(1)), 1); // panics: day / halvingDays with halvingDays == 0
            fail("deployment with halvingDays == 0 must not be accepted");
        } catch {}
    }

    function test_ZeroDayLengthIsRejectedAtDeploy() public {
        vm.prank(owner);
        try new DeliveryRewards(mail, owner, poster, 0, DAILY, 51) returns (DeliveryRewards r) {
            vm.warp(block.timestamp + 1 days);
            vm.prank(poster);
            r.postRoot(0, bytes32(uint256(1)), 1); // panics: (now - start) / dayLength with dayLength == 0
            fail("deployment with dayLength == 0 must not be accepted");
        } catch {}
    }
}
```

### 5. Low: upgrade(), levelUp() and Wardrobe.buy() charge whatever the owner-adjustable cost is at execution time, with no caller-supplied maximum

`p2e/contracts/src/MailOffice.sol:126`

```
        uint256 cost = upgradeCost[tier + 1];
        _spend(msg.sender, cost);
```

AUDIT.md says costs are owner-adjustable so the ladder can track a dollar target as the price moves, i.e. setUpgradeCost / setLevelCost / Wardrobe.list are routine operations while players transact. upgrade() reads upgradeCost[tier + 1], levelUp() reads levelCost[next] (line 164) and Wardrobe.buy reads it.price (Wardrobe.sol:51) at execution, and none takes a maximum the caller agreed to, while MessengerNFT.mint pins msg.value == price * quantity. The project's own tests approve type(uint256).max to the office, so a player who signed upgrade() at 7,000 MAIL pays whatever a retune mined first set, and 75% of the overpayment is burned irreversibly. No malice is needed; ordinary retune timing suffices. Reported by three specialists; merged. Fix: add a maxCost parameter to upgrade, levelUp and buy and revert when the current cost exceeds it (or make cost changes take effect after a delay).

**Reproduction**

alice has an open office, 100,000 MAIL and approve(office, type(uint256).max); upgradeCost(2) == 7_000e18. Owner calls setUpgradeCost(2, 70_000e18); then alice's upgrade() executes. Expected: revert or a charge of at most 7,000e18. Actual: balanceOf(alice) drops by 70_000e18 (52,500 burned, 17,500 to treasury), tierOf(alice) == 2. Run: cd p2e/contracts && forge test --match-path test/scratch/Judge.t.sol --match-test test_UpgradeChargesRetunedPrice (asserts alice is left with 30,000e18 and treasury has 17,500e18 on this code). Same sequence with setLevelCost before levelUp and list() before buy().

### 6. Low: The 75% burn rounds down in MailOffice._spend and Wardrobe.buy: costs not divisible by 4 wei burn less than 75% and the treasury receives the remainder

`p2e/contracts/src/MailOffice.sol:252`

```
        uint256 burnPart = amount * BURN_BPS / 10_000;
        mail.burnFrom(from, burnPart);
        mail.transferFrom(from, treasury, amount - burnPart);
```

Guarantees 11 and 16 say every MAIL spend burns exactly 75%. burnPart = amount * 7500 / 10_000 truncates and the treasury gets amount - burnPart, so rounding always favours the treasury over the burn; the same formula is at Wardrobe.sol:52. setUpgradeCost, setLevelCost and Wardrobe.list only forbid zero, not amounts that are not multiples of 4 wei. The launch ladder (whole e18 values) is exact; the deviation appears as soon as a cost is retuned to a dollar target or an item is priced in odd wei. The amount is at most 3 wei per spend, so the economic effect is nil, but the stated invariant does not hold and a 1 wei price burns nothing. Reported by two specialists (math low, economics info); merged. Fix: round the burn up ((amount * BURN_BPS + 9_999) / 10_000) or require amount % 4 == 0 in the setters.

**Reproduction**

Owner calls office.setUpgradeCost(2, 3); alice opens an office, approves, calls upgrade(). Expected: 75% of 3 burned. Actual: totalSupply drops by 2, treasury receives 1 (66.7% burned). Owner calls wardrobe.list(1, 1, 0); alice buys 1. Expected 75% burned; actual 0 burned, 1 wei to treasury. Run: cd p2e/contracts && forge test --match-path test/scratch/Judge.t.sol --match-test test_BurnRoundsDown (asserts those values on this code).

### 7. Low: reveal() succeeds when the sale never opened (saleClosedAt == 0), after which no Messenger can ever be minted

`p2e/contracts/src/MessengerNFT.sol:163`

```
        if (saleOpen || block.number <= saleClosedAt) revert RevealTooEarly();
```

saleClosedAt is only written by setSaleOpen(false), so before the sale was ever opened it is 0 and block.number <= 0 is false for every real block: reveal passes with no sale having happened. Once seed != 0, setSaleOpen(true) and ownerMint revert AlreadyRevealed by design, so a reveal sent out of order by the launch operator leaves the collection at its pre-sale count (0, or whatever was owner-minted) forever, with no recovery short of redeploying the NFT, the office and every integration. AUDIT.md accepts 'unsold NFTs stay unminted' after a closed sale; the never-opened case is a degenerate boundary, not a stated intent. Fix: require that a sale took place, e.g. `if (saleClosedAt == 0) revert RevealTooEarly();`.

**Reproduction**

Deploy MessengerNFT with any commit; never call setSaleOpen(true); advance one block; owner calls reveal(secret). Expected: RevealTooEarly. Actual: success, seed != 0; afterwards setSaleOpen(true) and ownerMint(owner, 1) both revert AlreadyRevealed and totalMinted stays at its pre-reveal value permanently. Run: cd p2e/contracts && forge test --match-path test/scratch/Judge.t.sol --match-test test_RevealBeforeSaleOpened (asserts this on the current code).

### 8. Low: setOffice strands every Messenger locked by the previous office: unassign on the old office reverts NotOffice and the token cannot move until the holder pays for a second office

`p2e/contracts/src/MessengerNFT.sol:201`

```
        office = office_;
    }
```

setLocked is gated on msg.sender == office, a single mutable slot, and nothing records which office locked a token. After an honest office migration (new ladder, bug fix) every assigned Messenger stays locked: unassign() on the old office reverts NotOffice from setLocked, transferFrom reverts IsLocked, and the new office has no record of the assignment. The holder's only escape is to pay 0.005 ETH for an office in the new contract and assign then unassign there (or the owner toggles the office slot back and forth). This contradicts guarantee 9 ('unassign unlocks it') for every holder at migration time. Fix: record the locker (lockedBy[id]) and let the current office or the recorded locker clear a lock, or let setOffice refuse while tokens are locked, or add an owner-only unlock.

**Reproduction**

alice owns Messenger #1, opened an office, called assign(1); nft.locked(1) == true. Owner deploys office2 and calls nft.setOffice(office2). alice calls office.unassign(). Expected: locked(1) == false. Actual: revert NotOffice(); locked(1) stays true; nft.transferFrom(alice, bob, 1) reverts IsLocked(). Only office2.open{value: 0.005 ether}(0); office2.assign(1); office2.unassign() unlocks it. Run: cd p2e/contracts && forge test --match-path test/scratch/Judge.t.sol --match-test test_SetOfficeStrandsLocked (asserts the stranded state and the paid recovery on this code).

### 9. Info: setMinter's one-shot guard is keyed on the zero sentinel: setMinter(address(0)) succeeds and leaves the function callable

`p2e/contracts/src/MailToken.sol:36`

```
        if (minter != address(0)) revert MinterAlreadySet();
```

Guarantee 2 says setMinter 'works once'. The guard is minter != address(0), so a call with address(0) passes, writes nothing useful and the function stays callable until a non-zero address is given. Only the deployer can trigger it and no third party gains access, so this is a correctness note on the stated guarantee rather than a bypass. Fix: add a bool minterSet or revert on minter_ == address(0).

**Reproduction**

deployer: new MailToken(liq); setMinter(address(0)) -> succeeds (expected: revert or consume the one shot); setMinter(address(0)) -> succeeds again; setMinter(0xBEEF) -> succeeds, minter() == 0xBEEF. Run: cd p2e/contracts && forge test --match-path test/scratch/Judge.t.sol --match-test test_SetMinterZero.

### 10. Info: Only the constructor's msg.sender can ever call setMinter: a factory or helper-contract deployment that does not wire the minter in-flight leaves the play allocation unmintable

`p2e/contracts/src/MailToken.sol:29`

```
        _deployer = msg.sender;
```

_deployer is the immutable msg.sender of the constructor, there is no owner and setMinter has no other caller. The repository has no mainnet deploy script, and the IMD launch path creates everything in one factory transaction. If MailToken is created by a factory or deployment helper, _deployer is that contract, and unless it calls setMinter(rewards) in the same flow the minter is unset forever: DeliveryRewards.claim reverts NotMinter on every call while the 4.2M liquidity mint has already happened. Nothing is lost to a third party; the risk is an irrecoverable launch. Fix: take the minter (or a one-time admin) as a constructor argument, or have the deploy script assert minter() == address(rewards) before anything else is handed out.

**Reproduction**

A contract F runs new MailToken(liq) then new DeliveryRewards(mail, owner, poster, 86400, DAILY, 51) and returns without calling mail.setMinter. The EOA owner then calls mail.setMinter(rewards). Expected (per deploy wiring): minter becomes rewards. Actual: revert NotMinter() because msg.sender != F; minter() stays address(0). Run: cd p2e/contracts && forge test --match-path test/scratch/Judge.t.sol --match-test test_FactoryDeployCannotSetMinter.

### 11. Info: Test suite does not exercise the edges where the defects above live: zero root, repeated postRoot for one day, revokeRoot accounting and claim flags, claimMany, reward-day boundaries around assign, co

`p2e/contracts/test/P2E.t.sol:466`

```
    function test_PauseAndRevoke() public {
```

The 25 tests cover happy paths and documented reverts but never: post bytes32(0) or post the same day twice (RootExists is never hit); assert totalPosted after revokeRoot when more than one post touched the day; claim a zero-amount leaf or re-claim after a revoke and re-post; call claimMany at all; place assign/unassign across a DeliveryRewards day boundary (office tests use an arbitrary block.timestamp and never read rewards.currentDay()); call upgrade()/levelUp()/buy() after a cost change; call reveal() with saleClosedAt == 0; construct DeliveryRewards with zero parameters. Adding these cases pins guarantees 4, 5, 7 and 8 and would have caught the high and medium findings above.

**Reproduction**

forge test --match-test 'test_PauseAndRevoke|test_ClaimFlow|test_DailyBudgetCap': none posts bytes32(0), none posts a day twice, none asserts totalPosted after a second post. Missing assertion: after postRoot(0, 0x0, DAILY) twice and revokeRoot(0), totalPosted should be 0 (actual on this code: DAILY). Missing assertion: with t0 = rewards.startTime(), assign at t0 + 12h then at t0 + 36h unassign/transfer/assign by a second wallet should fail if one Messenger may play for only one wallet per reward day (actual: succeeds).

---

Judge's submission `b8f38d463b51580d7ac8b03cd5bd4670474c7bd79558a98821d176d3246048a2`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
