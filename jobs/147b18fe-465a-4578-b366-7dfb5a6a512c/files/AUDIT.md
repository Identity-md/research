# Audit report

> TokenDrops re-check (Courier World, Robinhood Chain 4663), commit d59c2ab, after fixing audit 9755203f.
>
> The treasury (owner) funds drops of a launchpad token or $STAMP; players with an open post office claim coins they found with EIP-712 vouchers Finds(player, drop, day, coins, deadline) signed by the game server’s key. Since the last audit: dailyCoins is required and at least maxPerWallet (every player can collect each coin, as with golden stamps, so spots is coins placed, not a payout cap); claimMany skips expired or stale vouchers; withdraw while paused ends the drop; claimable respects pause and windows; endDrop(id, lastDay); sweep for stray tokens; SignerSet records the previous key; DROPS_OWNER required in the deploy script.
>
> Main question: if the server’s signing key leaks, what is the most an attacker can take, and can they touch anything outside the drops’ own balances? In particular, confirm they can’t pull tokens from the treasury wallet, move one drop’s tokens through another, exceed a drop’s daily cap per day (including the yesterday-plus-today window), or block the owner’s pause, setSigner and withdraw. Please also check the fixes above, the day edges, and that each drop’s tokens stay separate (held accounting).
>
> Source: contracts/src/TokenDrops.sol; tests in contracts/test/TokenDrops.t.sol.

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/courierworld.git |
| Commit | `d59c2ab5f2ba4f2f6bff570311198ff3f38ca26b` |
| Job | `147b18fe-465a-4578-b366-7dfb5a6a512c` |
| Judged | 2026-10-12 21:39 UTC |
| Findings | 2 low · 6 info |

Four agents audited the code as it is at `d59c2ab`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: dailyCoins has no upper bound, so the per-day cap that bounds a leaked key is only as tight as the value typed at createDrop

`contracts/src/TokenDrops.sol:290`

```
                || dailyCoins < maxPerWallet || days_ == 0 || days_ > MAX_DAYS || startDay < today()
```

Merged from three specialists (permissions, flow, economics). createDrop sanity-caps every other sizing input (spots 1..48, maxPerWallet 1..spots, days 1..365) but only lower-bounds dailyCoins (>= maxPerWallet). dailyCoins is a plain coin count sitting next to perCoin, a 1e18-scaled token amount, so a units slip (1000e18 instead of 1000) or type(uint256).max is accepted. With such a value _payable's dayLeft never binds and the only remaining limit on a day is the drop's `left`, which is exactly the state fix #1 of audit 9755203f closed for dailyCoins == 0. The main-question answer ('a leaked key takes at most dailyCoins*perCoin per drop per open day until pause') therefore rests on an unchecked owner parameter. This is an owner input, not a bypass, so it is a trust/limit gap rated low. Minimal fix that keeps the design: add a ceiling to the same BadDrop check, e.g. `dailyCoins > type(uint16).max` or a constant such as spots * 100, and state in the natspec/AUDIT.md trust note that dailyCoins * perCoin per open day is the loss bound a leak can reach. If uncapped drops are wanted, document that choice instead.

**Reproduction**

Scratch test test_UnboundedDailyCoins on d59c2ab (passes, i.e. the drain succeeds): treasury calls createDrop(coin, 1000e18, spots=10, maxPerWallet=5, dailyCoins=1000e18, today, 7, 100_000e18) -> accepted, drop.dailyCoins == 1e21 (expected: BadDrop or a bounded value). Then createDrop(coin, 1000e18, 10, 5, type(uint256).max, today, 7, 100_000e18) -> accepted. With the signer key, 20 wallets each with an open post office (0.005 ETH each) call claim(id, today, 5, deadline, voucher): total paid 100_000e18, drop.left == 0, paidCoins(id, today) == 100 in one block. Expected per the fix #1 rationale: a day's payout bounded well below the whole drop. Actual: the whole drop in one day; the yesterday-plus-today window adds nothing because the drop is already empty.

### 2. Low: withdraw while paused ends the drop at mining time (today()), so one mined after midnight leaves the emptied drop listed a day longer than meant, with no TooLate guard like endDrop

`contracts/src/TokenDrops.sol:343`

```
        _end(id, today());
```

Merged from the math specialist (low) and the permissions specialist's note. Fix #5 of audit 9755203f gave endDrop(id, lastDay) an explicit last day and `if (lastDay < today()) revert TooLate()` so a transaction mined after midnight cannot run a drop a day longer than intended. The paused-withdraw path added by fix #3 has the same midnight race and no guard: it calls _end(id, today()) with today() read at mining time. A withdraw sent at 23:59:50 on day D and mined at 00:00:05 on D+1 sets endDay = D+1. The drop then has left == 0 but activeDrops(D+1) still lists it, so the room (multiplayer/src/index.js dropsOn/layDrops reads only activeDrops and spots) lays its coins out for all of D+1; every voucher for them pays nothing (claim reverts NothingToClaim, claimMany skips it), and the owner cannot shorten it afterwards because endDrop(id, D) now reverts TooLate. No tokens are at risk; the impact is a day of players collecting coins that cannot pay, for a drop the owner meant to stop, which is the state fix #3 was meant to prevent. Minimal fix preserving the design: give withdraw the intended last day exactly as endDrop has it, e.g. withdraw(uint256 id, address to, uint32 lastDay) with `if (lastDay < today()) revert TooLate();` and `_end(id, lastDay);` (a finished or cancelled drop is unaffected since _end only shrinks endDay). Alternatively have the admin UI send endDrop(id, today) first and withdraw only after it is mined.

**Reproduction**

Scratch test test_WithdrawPausedMinedAfterMidnight on d59c2ab (passes, showing the behaviour): createDrop(coin, 1000e18, 10, 5, 100, D=30, 30 days, 100_000e18) so endDay = 59. setPaused(true) at timestamp 31*86400-10 (23:59:50 on day 30); withdraw(id, treasury) mined at 31*86400+5 (00:00:05 on day 31); setPaused(false). Expected (the intent endDrop enforces): endDay == 30, or the transaction reverts TooLate. Actual: drop(id).endDay == 31, activeDrops(31) == [id], drop(id).left == 0, endDrop(id, 30) reverts TooLate, and alice with a valid voucher Finds(alice, id, 31, 3, deadline) gets NothingToClaim.

### 3. Info: claimable() quotes a full payout for a wallet with no post office, where claim() reverts NoOffice

`contracts/src/TokenDrops.sol:167`

```
        if (id >= _drops.length || paused) return (0, 0);
```

Merged from the economics specialist and the flow specialist's test-gap item. Fix #4 of audit 9755203f made claimable() return (0, 0) where a claim would fail: paused, outside the drop's days, outside the two-day window. One guard of claim() is still missing from the view: _checkClaimer requires postOffice.offices(msg.sender).open, but claimable(id, player, day, coins) never reads the post office, so it quotes the full amount for a wallet that cannot claim. It is a view, so no funds are at risk; the effect is a misleading quote in the front end and an incomplete 'claimable quotes nothing where a claim would fail' guarantee in AUDIT.md line 459. Fix: in claimable(), read postOffice.offices(player) and return (0, 0) when the office is not open, or document the exception.

**Reproduction**

Scratch test test_ClaimableNoOffice on d59c2ab: createDrop(coin, 1000e18, 10, 5, 100, today, 7, 100_000e18); carol has no post office. claimable(0, carol, today, 3) -> expected (0, 0); actual (3, 3000e18). carol calling claim(0, today, 3, deadline, validVoucherForCarol) reverts NoOffice().

### 4. Info: Leaked signer key: bounded to the drops' own balances and per-day caps as designed, but the short-term worst case is three day-caps per drop within one second at midnight, not the two days the AUDIT.m

`contracts/src/TokenDrops.sol:243`

```
        else if (now_ >= day + CLAIM_DAYS) stale = TooLate.selector;
```

Merged from the permissions and math specialists; this is the answer to the main question, with one documentation discrepancy. Confirmed against the code and by test: the only token-moving path a key holder reaches is _claim, which pays msg.sender (a wallet with an open office) at most maxPerWallet - claimed per (drop, day, wallet), at most dailyCoins - paidCoins per (drop, day) across everyone, and only from that drop's own `left` (left and held[token] decrement together before the transfer, so no drop pays from another's tokens or from strays, and sweep only moves balanceOf - held). _pull is reached only from the owner-only createDrop/topUp and always pulls from msg.sender, so the treasury's standing allowance cannot be spent by anyone else. setPaused, setSigner, endDrop and withdraw make no call a claimer controls and read nothing a claimer can write (PadToken/StampToken have no hooks), so the owner cannot be blocked; a claimer can at most front-run the pause for the caps already open. Per-day caps hold: an extra wallet on a filled day gets NothingToClaim. The discrepancy: AUDIT.md lines 471-472 say a leaked key can claim 'up to each drop's dailyCoins a day (for today and yesterday)'. Because yesterday stays open until 23:59:59 and the new day opens at 00:00:00, an attacker timing the drain at the day edge fills D-1, D and D+1 within one second, i.e. up to 3 * dailyCoins * perCoin per running drop (bounded by left) before any owner reaction, then dailyCoins per further day until pause. Each day's drain needs ceil(dailyCoins / maxPerWallet) office wallets at 0.005 ETH each. No contract change is required by the agreed design; the fix is to state the 3-day edge bound in the trust note and alert on Claimed volume so the owner can pause quickly.

**Reproduction**

Scratch test test_ThreeCapsAtMidnight on d59c2ab (passes): createDrop(coin, perCoin=1e18, spots=10, maxPerWallet=5, dailyCoins=20, startDay=today, 30 days, 1_000_000e18) and a second same-token drop of 1_000e18. Warp to 23:59:59 on D = start+1. Four office wallets claim day D-1 with coins=65535 and four claim day D: paid 40e18, paidCoins(id, D-1) == paidCoins(id, D) == 20; a fifth wallet's claim for D or D-1 reverts NothingToClaim (cap holds). Warp 1 second to 00:00:00 of D+1: four fresh wallets claim D+1: total paid 60e18, three day-caps in one second; a claim for D-1 now reverts TooLate. The other drop's left is still 1_000e18, held(coin) == balanceOf(drops) == 1_001_000e18 - 60e18, the treasury balance only dropped by what it funded. Afterwards setPaused(true), setSigner(new), withdraw(both drops) all succeed and return 1_001_000e18 - 60e18 to the treasury. Expected per AUDIT.md: at most 2 x dailyCoins before the next day. Actual: 3 x dailyCoins reachable at the day edge.

### 5. Info: withdraw panics (0x11) instead of reverting StillRunning for a drop whose endDay is within CLAIM_DAYS of uint32 max

`contracts/src/TokenDrops.sol:342`

```
        if (!paused && !cancelled && today() < d.endDay + CLAIM_DAYS) revert StillRunning();
```

From the flow specialist, reproduced. `d.endDay + CLAIM_DAYS` is a checked uint32 addition and createDrop only requires startDay >= today() and days_ <= 365, so the owner can create a drop with startDay = type(uint32).max - 1, days_ = 1 (endDay = 4294967294). A non-paused, non-cancelled withdraw on it hits an arithmetic overflow panic rather than StillRunning. Tokens are not stuck: endDrop(id, today()) cancels it (the `cancelled` short-circuit skips the addition) and withdraw then succeeds; pausing also skips it. _open and _claim are safe because day <= now_ is checked before day + CLAIM_DAYS. Day 4294967294 is millions of years away, so this is a misconfiguration edge only, reported for completeness of the day-edge review. Minimal fix: bound startDay in createDrop (e.g. startDay <= today() + MAX_DAYS), which also stops a drop being scheduled absurdly far ahead by mistake, or compare without the addition.

**Reproduction**

Scratch test test_WithdrawOverflowNearMaxDay on d59c2ab: treasury calls createDrop(coin, 1e18, 10, 5, 10, type(uint32).max - 1, 1, 1e18), then withdraw(id, treasury) with paused == false. Expected: revert StillRunning. Actual: revert Panic(0x11) from `d.endDay + CLAIM_DAYS`. Recovery: endDrop(id, today()) then withdraw(id, treasury) succeeds, left == 0. createDrop with startDay = type(uint32).max also reverts with Panic(0x11) (from `startDay + days_ - 1` on line 294) rather than BadDrop.

### 6. Info: A malformed voucher signature (wrong length, high-s) reverts claim/claimMany with OpenZeppelin ECDSA errors rather than BadSignature

`contracts/src/TokenDrops.sol:238`

```
        if (ECDSA.recover(digest, signature) != signer) revert BadSignature();
```

From the flow specialist, reproduced. OpenZeppelin v5 ECDSA.recover(bytes32, bytes) reverts itself with ECDSAInvalidSignatureLength, ECDSAInvalidSignatureS or ECDSAInvalidSignature for a signature that is not 65 bytes, has a high s, or recovers to zero; only a well-formed signature by the wrong key reaches the BadSignature branch. The security outcome is correct (nothing is paid, the batch reverts as documented for a forged voucher, and a caller can only break their own batch), so this is cosmetic: the error the front end sees differs from the one the natspec and test_RejectsForgedOrChangedVouchers describe, and no test covers malformed signatures. Minimal fix: use ECDSA.tryRecover and treat any error or a non-signer address as BadSignature, or document the OZ errors as possible.

**Reproduction**

Scratch test test_MalformedSignatureError on d59c2ab: alice (open office) calls claimMany with one Claim{drop: 0, day: today, coins: 1, deadline: type(uint64).max, signature: hex"00"} on a running drop. Expected per natspec: revert BadSignature(). Actual: revert ECDSAInvalidSignatureLength(1).

### 7. Info: A running drop emptied by claims stays in activeDrops until endDay, so its coins keep going out and pay nothing (asymmetric with the withdraw-ends-the-drop fix)

`contracts/src/TokenDrops.sol:189`

```
        // As many as the drop's tokens, and the day's coins, can cover; the rest stays claimable if they grow.
```

From the permissions specialist, reproduced; a documented design trade-off rather than a defect, recorded because the requester asked to check fix #3. Fix #3 ends a drop that withdraw empties while paused so its coins stop going out. The same state reached through claims (running drop, left < perCoin) does not end it: activeDrops(day) still lists it for every day to endDay, the room lays its coins out (dropsOn/layDrops read only activeDrops and spots), players collect them and every voucher pays 0 (claim reverts NothingToClaim, claimMany skips). The comment on this line shows the intent: a topUp can revive the finds. No funds are at risk. Options that keep the design: have the room treat left < perCoin as not running (read left/perCoin in dropsOn), or have the owner endDrop or topUp promptly on a Claimed-volume alert.

**Reproduction**

Scratch test test_EmptiedDropStaysActive on d59c2ab: createDrop(coin, perCoin=1e18, spots=10, maxPerWallet=10, dailyCoins=1000, startDay=today, 7 days, amount=1e18). alice claims 10 coins on day start: pays 1e18, drop.left == 0. activeDrops(start+3) returns [id] and, on day start+3, claimable(id, alice, start+3, 1) returns (0, 0). Expected by the rationale of fix #3: a drop with nothing to pay stops putting coins out. Actual: listed until endDay = start+6.

### 8. Info: Test suite gaps around the edges this re-check asked about: leaked-key bound across midnight with many wallets, held invariant under mixed operations, claimable for a non-office, malformed signatures,

`contracts/test/TokenDrops.t.sol:641`

```
    function testFuzz_NeverOverpays(uint16[6] memory finds, uint8 daily) public {
```

Merged from all four specialists' test-coverage notes. The 33 tests (all passing on d59c2ab) cover each fix from audit 9755203f and the day edges to the second, but the question this re-check asks has no test: nothing claims yesterday's and today's finds from more than two wallets on one calendar day, nothing crosses a midnight with claims on both sides, and the fuzz runs one drop, one day and two wallets, so paidCoins of two days never coexist and the `held == sum(left)` accounting is never fuzzed through interleaved createDrop, topUp, claim, endDrop, paused withdraw, stray transfer and sweep. Also untested: claimable() for a wallet without an office (it quotes a payout, see the separate note); a 1- or 64-byte signature in a batch; claimMany reverting the whole batch with UnknownDrop next to a valid voucher (stated in the natspec); endDrop(id, lastDay > endDay) being a no-op (a drop cannot be extended); topUp on a cancelled or finished drop followed by withdraw returning held to 0; endDrop(id, today) then withdraw at 23:59:59 of D+1 (StillRunning) and 00:00:00 of D+2 (allowed); withdraw while paused mined after midnight (see the low finding). All of these were exercised in scratch tests during this review and behave as documented except the two reported above. Adding them, plus a multi-day multi-wallet invariant (sum of Claimed per (drop, day) <= dailyCoins, held[token] == sum of left over that token's drops, balanceOf >= held), would turn the AUDIT.md section 13 trust statement into a tested property.

**Reproduction**

Run `forge test --match-path test/TokenDrops.t.sol` (33 pass) and grep the file: no test warps to uint256(day+1)*1 days - 1 and claims both day-1 and day from more than two office wallets asserting paidCoins per day; no `hex"` or `ECDSAInvalid`; no claimMany with a drop id >= dropCount; no topUp after endDrop or withdraw; no assertion that drops.held(token) equals the sum of drop(i).left after a topUp + paused withdraw + sweep sequence; claimable is never called for carol. Expected: coverage of the stated leaked-key bound and held invariant; actual: single-day fuzz with two wallets and no invariant handler.

---

Judge's submission `a8562c9ba5284774912e8a6b38bcc226d2ef21b1c15eff5b0a0492c452556941`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
