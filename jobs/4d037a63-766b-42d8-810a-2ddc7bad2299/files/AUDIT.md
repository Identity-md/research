# Audit report

> Final check 5 for The Zero Person Billion Dollar Company ($COMPANY) on Robinhood Chain (4663), after IMD Swarm audit 78c00339, re-check f1d5def3 and final checks 363ab052, 882666b4, 986abba2 and dddb75ec. AUDIT.md sections 4 to 9 map every finding to its fix and its test.
>
> What the contracts are for: CompanyToken is a fixed 1,000,000,000 supply ERC-20; its ownership is renounced in the constructor. CompanyHook owns the token's only Uniswap v4 pool, paired with IMD, with liquidity locked forever, and takes 4% of every swap in that pool: 1% to the protocol, 3% to holders. Holder fees are split 50% IMD and 10% each to NVDA, GOOGL, AAPL, GME and MSTR Robinhood stock tokens, bought IMD -> USDG -> stock at the start of every claim(), each step checked against a reference price. Only wallets holding at least 100,000 earn. If a wallet goes more than 7 days without claiming, buying, selling or sending, its unclaimed rewards older than 7 days expire.
>
> Changed since dddb75ec; review these hardest:
> 1. Fallback size: every IMD fallback now pays min(pendingConvert, MAX_ROUND_IMD / 5), never a swap-clipped amount; a successful purchase below a tenth of a round doesn't reset the stuck clocks.
> 2. Stuck rule: failingSince[stock] is set on the first skipped or failed attempt since the last real purchase (stale feed, IMD/USDG pool unusable, PriceOff, dust purchase) and cleared by a real purchase; _skipOrFallBack pays as IMD only when waitingSince is more than DEAD_AFTER (30 days) old AND failingSince is at least a day old. Can a healthy stock still be paid as IMD early, or a broken one be kept from ever falling back?
> 3. IMD/USDG pool usability: usable only with maxConvert() >= 1% of a round AND its spot within IMD_TOLERANCE_BPS (10%) of IMD's reference (IMD/ETH pool + Chainlink ETH/USD and USDG/USD); stockRoundLimit prices USDG->IMD at that reference; an IMD/USDG-side fill failure reverts PriceOff (skip), so only stock-side failures fall back at once.
> 4. _swapFee: minUsdOut and minStockOut subtract the LP fee plus Uniswap's protocol fee for the swap's direction (0.1% is on for IMD/USDG and GME/USDG on Robinhood Chain).
>
> Please confirm these, check that nothing broke the solvency of the six reward assets, the flash-borrow guards, the 100,000 minimum, expiry or the scanner-relevant properties (no external calls in transfers), and report anything new.
>
> Tests: cd contracts; git submodule update --init --recursive; forge test. Fork test (live Chainlink feeds, pools and protocol fees): FORK_RPC=https://robinhood.drpc.org forge test --mc CompanyForkTest.

| | |
|---|---|
| Repository | https://github.com/imdmaxi/IMDINDEX.git |
| Commit | `08ff7970ce96f33f6dc9c1cdc2247550e80f1003` |
| Job | `4d037a63-766b-42d8-810a-2ddc7bad2299` |
| Judged | 2026-10-07 16:45 UTC |
| Findings | 1 medium · 3 low · 3 info |

Four agents audited the code as it is at `08ff797`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Dust-only stock purchases arm failingSince but the stuck rule is never evaluated on the success path, so a stock pool in the 0.04-0.4 IMD band throttles its reserve forever instead of falling back aft

`contracts/src/CompanyToken.sol:752`

```
            try this.convertStock{gas: CONVERT_GAS}(a, imdIn) returns (uint256 out) {
                stockOut[a] = out;
```

convertStock (lines 807-814) classifies a purchase below a tenth of a round (imdIn < MAX_ROUND_IMD/5/10 = 0.4 IMD) as 'not a working stock': it arms failingSince and leaves waitingSince untouched, exactly as the dddb75ec finding 1 fix intends and as the failingSince NatSpec ('only dust bought') and the README describe. But the only code that pays a stuck stock as IMD is _skipOrFallBack, which _convertAll reaches on three skip paths only (IMD/USDG pool unusable, stale feed, PriceOff). A round whose stock pool allows between cap/100 (0.04 IMD with a full cap) and 0.4 IMD takes the try branch at line 752, succeeds with dust, and never reaches the stuck rule. The clocks are written but never read: waitingSince ages past DEAD_AFTER, failingSince stays armed, and no round is ever paid as IMD while the dust fills keep succeeding. A pool slightly emptier (limit < 0.04 IMD) pays a full 4 IMD round at once; a pool in the band above it throttles the reserve 10x-100x indefinitely, the exact throttle dddb75ec finding 1 rated Medium. The band is reachable on the live chain: for NVDA's 0.01% pool it is 800-8,000 USDG of in-range virtual depth, for GME's 1% pool 8-80 USDG (GME's live limit is 3.11 IMD on today's fork). Anyone can also keep an otherwise-empty stock pool in the band with one small position near Chainlink's price, turning the immediate fallback into an indefinite throttle. Holders lose nothing (IMD stays backed, solvency holds) but their stock share is delayed without bound while fee inflow exceeds the dust drain. The same root cause applies when the IMD/USDG pool is shallow (maxConvert between 0.2 and 2 IMD): all five stocks fill dust forever (see the info finding on the two thresholds). Merged from audit_flow and audit_economics (same mechanism, same fix). Minimal fix, verified: in _convertAll after clipping imdIn to poolLimit, `if (imdIn < MAX_ROUND_IMD/(ASSETS-1)/10 && pending >= MAX_ROUND_IMD/(ASSETS-1)/10) { _skipOrFallBack(a, fullRound); if (lastConvert[a] == block.timestamp) continue; }` then go on to buy the dust. With this patch the attached proof passes and all 65 existing tests still pass (checked).

**Reproduction**

Setup as test/Company.t.sol but the NVDA/USDG pool has 70e18 of full-range liquidity (stockRoundLimit(1) = 0.105 IMD: above cap/100 = 0.04, below a tenth of a round = 0.4). alice and bob each buy 1,000 IMD: pendingConvert(1) = 6 IMD, waitingSince(1) = T0. For 29 days: warp 1 day, refresh all feeds, arbitrage the NVDA pool back to tick 0, call convert(): out[1] > 0 every day (about 0.103 NVDA), failingSince(1) = T0 + 1 day and never cleared, waitingSince(1) still T0, pendingConvert(1) = 2.95 IMD. Day 31: warp 2 days, refresh feeds, call convert(). Expected (README, failingSince NatSpec, AUDIT.md 3.7): waited more than DEAD_AFTER without a real purchase and failing for 30 days, so min(pending, 4 IMD) = 2.95 IMD is credited to holders as IMD and ConversionFailed is emitted. Actual: another 0.105 IMD dust fill, owed(0) unchanged (30 IMD), no ConversionFailed; the same on every later day. Proof test/scratch/DustStockPoolNeverFallsBack.t.sol fails on this code with "a stuck stock's round is paid to holders as IMD: 0 <= 2000000000000000000" and passes with the fix above.

### 2. Low: failingSince never decays, so one isolated skip before a quiet month makes the first transient skip after it pay a healthy stock as IMD at once

`contracts/src/CompanyToken.sol:770`

```
        if (failingSince[asset] == 0) failingSince[asset] = block.timestamp;
```

The rule is documented as 'waited DEAD_AFTER AND been failing for at least a day, so a quiet month alone never pays a healthy stock as IMD' (failingSince NatSpec lines 222-225, README, AUDIT.md section 9 finding 2). failingSince is armed by the first skip and cleared only by a real purchase (convertStock), by the reserve emptying, or by distribute() refilling an empty reserve. The end of a transient condition clears nothing, because a quiet period produces no purchase. So the clock measures 'time since the first skip with no real purchase since', not 'continuously failing for a day'. One ordinary transient skip (a weekend-stale equity feed, a 5% gap between a stock's pool and Chainlink, the IMD/ETH vs IMD/USDG gap exceeding 10% after a large ETH-route buy, which arms all five stocks in one read) followed by 30 quiet days makes the next transient skip satisfy both conditions immediately: 4 IMD are paid as IMD at the first attempt, and every later due round pays another 4 IMD while the transient lasts. This answers request question 2: a healthy stock can still be paid as IMD early. Griefing variant: anyone can arm a stock's clock in the same transaction as a convert() by pushing its thin pool 3% off Chainlink (about $2 of fees on the live GME pool) or all five by pushing IMD/USDG 10% off its reference, but the 30 quiet days are not attacker-controllable, so this stays griefing. Impact is value-neutral for holders (IMD of equal value), hence low, matching the requester's rating of the parent finding. Merged from audit_permissions and audit_economics. Trade-off to decide (verified): the obvious fix, recording lastSkip[asset] and restarting failingSince when the previous skip is older than a window (for example 7 days), makes the attached reproduction pass but breaks five existing tests that pin the opposite expectation for a genuinely dead feed or empty pool seen once at day 5 and once at day 31 with no observation in between (test_final3_deadFeedFallsBackToImdAfter30Days, test_final3_emptyImdPoolFallsBackToImdAfter30Days, test_final2_4_unusableFeedHoldsUntilDeadAfter, test_final4_1a, test_final4_1b): without a daily keeper the contract cannot tell 'failed once, fine in between, failed again' from 'failing all month'. Either require the failing day to be observed by two skips within a window (and accept that a dead stock then needs two convert()/claim() calls a day apart after the 30 days), or keep the code and correct the NatSpec, README and AUDIT.md to the weaker semantics ('a stock skipped at least a day before and not bought since'). No proof is attached because the two legitimate resolutions lead to different outcomes.

**Reproduction**

Unit harness of test/Company.t.sol (all pools 1:1, feeds $1). 1) _buy(alice,1000e18); _buy(bob,1000e18): pendingConvert(1) = 6 IMD, failingSince(1) = 0. 2) warp +1 minute; feeds[0].set(0.95e8, now) (Chainlink says NVDA is 5% cheaper than its pool); convert(): NVDA reverts PriceOff and is skipped, pendingConvert(1) = 6e18, failingSince(1) = now (= T1). 3) feeds[0].set(1e8, now): the condition is over. Nobody claims or converts for 31 days. 4) warp +31 days; refresh all feeds; feeds[0].set(1e8, now - 4 days - 1) (a long weekend); convert(). Expected per the documented rule and test_final4_2a (which asserts exactly this without step 2): NVDA skipped, pendingConvert(1) == 6e18, owed(0) unchanged. Actual: _skipOrFallBack sees waitingSince T0 (> 30 days) and failingSince T1 (>= 1 day) and calls _fallBackToImd: pendingConvert(1) drops 6e18 -> 2e18 and owed(0) rises by 4e18; a convert() a minute later with the feed still stale pays the remaining 2e18. Reproduced in test/scratch/StaleFailingClock.t.sol: fails with 'healthy NVDA waits for its feed; nothing paid as IMD: 2000000000000000000 != 6000000000000000000' on this code; passes with a 7-day continuity window on failingSince (which in turn fails the five existing tests listed above).

### 3. Low: Zero in-range liquidity at the stock pool's current tick is treated as an empty pool and pays a full round as IMD at once, although the purchase would fill within the Chainlink tolerance

`contracts/src/CompanyToken.sol:739`

```
            if (poolLimit < cap / 100) {
                _fallBackToImd(a, fullRound);
```

_stockRoundLimit reads getLiquidity(id), the liquidity active at the pool's exact current tick, and returns 0 when it is zero. In a concentrated pool this is the state whenever the price sits in a gap between positions, which an ordinary sell produces: the swap exhausts the active position and the price lands at the seller's price limit just outside it. The token's own purchase direction (USDG -> stock) re-enters that position at once at a price below Chainlink's, so the round could be bought and would pass minStockOut by a wide margin. _convertAll instead classifies poolLimit < cap/100 as 'no liquidity at the price' and calls _fallBackToImd(a, fullRound): 4 IMD are credited to holders as IMD without a swap, and every following due round (one per minute, on every claim) does the same until some other trade moves the price back inside a position. The zero-limit shortcut predates the Chainlink check (it was added for f1d5def3 finding 2, a far resting position); with minStockOut now guarding the price, a far position is already rejected as PriceOff, so the shortcut only converts a transient, fillable state into an immediate IMD payout, contradicting AUDIT.md guarantee 7's intent that pool-state problems wait for the 30-day rule. It costs nothing to cause (one sell with a price limit, or the natural result of a trade that exhausts a range) and holders receive IMD of equal value, hence low. On the live chain the five stock pools and IMD/USDG all have several positions near their current ticks today (fork probe), so the state needs a trade that crosses the whole active range; GME's thin 1% pool (3.11 IMD round limit today) is the most exposed. Fix options, both of which change behaviour the requester's tests currently pin (test_recheck2_zeroLiquidityRoundPaidAsImd_noSwap and test_final4_dustPositionCountsAsEmpty fail with either): route poolLimit < cap/100 through _skipOrFallBack (a truly empty pool then falls back through the 30-day rule, which guarantee 7 promises for pool-state problems), or attempt the purchase and let minStockOut and Slippage decide. The requester should decide which rule they want and update AUDIT.md section 1 ('a stock pool with no liquidity at its price has the round credited as IMD without a swap') to match. No proof attached for that reason.

**Reproduction**

Setup as test/Company.t.sol but the NVDA/USDG pool has one position [-600, 600] of liquidity 1e24 instead of full range; alice and bob each buy 1,000 IMD (6 IMD pending per stock). Sell 200,000 NVDA into the pool with a price limit at tick 660 (-660 when NVDA is currency0): the price lands at the limit, pm.getLiquidity(pool) == 0, token.stockRoundLimit(1) == 0. In a snapshot, a direct 3.964 USDG -> NVDA swap at this moment returns more than token.minStockOut(1, 3.964e18) (the pool fills from the position at a price better than Chainlink's). Warp 1 minute, call convert(). Expected: NVDA bought, or the round skipped and retried (30-day rule). Actual: owed(0) rises from 30e18 to 34e18 and pendingConvert(1) drops from 6e18 to 2e18, the NVDA round is paid as IMD immediately, and each later minute pays another round while the price stays outside the position. Reproduced in test/scratch/OutOfRangePoolPaysImdAtOnce.t.sol: fails with 'a fillable pool must not be paid as IMD at once: 34000000000000000000 != 30000000000000000000' on this code and passes when the zero-limit branch calls _skipOrFallBack instead.

### 4. Low: A stock-hop swap that cannot fill the whole round because the price is near the edge of a thin position is treated as a stock failure and pays the full round as IMD at once

`contracts/src/CompanyToken.sol:761`

```
                // The stock side failed (its token refuses this contract, its pool can't fill): pay as IMD.
                _fallBackToImd(a, fullRound);
```

_stockRoundLimit sizes the round from the virtual depth at the current tick (half the fee times depth), which says nothing about how far that depth extends in the purchase direction. When the price sits inside a position but within the round's price move of its edge, with no liquidity beyond, the v4 swap runs out of liquidity, fills only part of the input, _swapExactIn reverts Slippage (second hop), and the catch branch at line 761 calls _fallBackToImd(a, fullRound) at once: a healthy pool that agrees with Chainlink and would fill a smaller purchase is paid as IMD, 4 IMD per minute, until the price moves away from the edge. The token's own purchases walk the price toward that edge. This contradicts AUDIT.md guarantee 7 (pool-state problems wait 30 days) and the request's framing that only stock-side refusals fall back at once; here nothing refused. Holders receive IMD of equal value and the state is not attacker-profitable, hence low. On the live GME/USDG pool (1% fee, tick spacing 200, round clipped to 3.11 IMD today, so a round moves its price about 1%) the next liquidity edge in the purchase direction is 643 ticks above the current tick on today's fork, so the state is not present now but one trade or a few rounds can produce it; the other four stock pools have deeper neighbouring positions. Minimal fix, verified: treat a Slippage revert from the stock hop like PriceOff, i.e. `if (reason.length >= 4 && (bytes4(reason) == PriceOff.selector || bytes4(reason) == Slippage.selector)) { _skipOrFallBack(a, fullRound); continue; }` so a pool that cannot fill the round is retried and only falls back through the 30-day rule (a token that refuses the contract still reverts with its own error and falls back at once). With this patch the attached proof passes and all 65 existing tests still pass (checked). Alternatively size imdIn to the depth available up to the next initialized tick before giving up on the round.

**Reproduction**

Setup as test/Company.t.sol but the NVDA/USDG pool has one position [-600, 600] with liquidity 3,000e18 (about 3,000 USDG of virtual depth; stockRoundLimit(1) = 4.5 IMD, above the 4 IMD round). alice and bob each buy 1,000 IMD. Buy NVDA with USDG up to tick -590 (590 when NVDA is currency0), 10 ticks (0.1%) before the position's edge in the purchase direction, and set the NVDA feed to the pool price (1.0608e8). In a snapshot, a direct 1 USDG -> NVDA swap returns more than token.minStockOut(1, 1e18), so a quarter-size purchase is fine. Warp 1 minute, call convert(). Expected: stock bought (smaller size) or the round skipped and retried. Actual: the 3.964 USDG swap needs a 0.26% move but only 0.1% of range remains, _swapExactIn reverts Slippage, and owed(0) rises from 30e18 to 34e18 with pendingConvert(1) = 2e18: the full round is paid as IMD at once. Proof test/scratch/NearEdgePartialFillPaysImdAtOnce.t.sol fails on this code with 'a healthy pool must not be paid as IMD at once: 34000000000000000000 != 30000000000000000000' and passes once a Slippage revert from the stock hop is skipped instead of falling back.

### 5. Info: IMD/USDG usability (1% of a full round) and 'real purchase' (10% of a stock's round) thresholds disagree: with 80-800 IMD of IMD/USDG depth every successful purchase counts as failing

`contracts/src/CompanyToken.sol:721`

```
            refOk && roundCap >= MAX_ROUND_IMD / 100 && _within(_imdUsdSpot(), refUsdPerImd, IMD_TOLERANCE_BPS);
```

_convertAll declares the IMD/USDG pool usable when maxConvert() >= MAX_ROUND_IMD/100 (0.2 IMD) and then spends cap = maxConvert()/5 per stock, while convertStock counts a purchase as real (resetting waitingSince and failingSince) only when imdIn >= MAX_ROUND_IMD/5/10 = 0.4 IMD, a fixed number that does not scale with the round actually allowed. Whenever maxConvert() is between 0.2 and 2 IMD (IMD/USDG virtual in-range depth between 80 and 800 IMD; the live pool holds about 8,550), every round is both executed and classified as dust: failingSince is set by the first purchase, waitingSince stays at the time the reserve filled, and because the reserve refills from trading it never empties, so the clocks never clear. From then on the first transient skip after 30 days (a weekend feed gap, an IMD/ETH drift, a momentary PriceOff) pays a full 4 IMD round as IMD, then 4 IMD per due round while the skip lasts, for stocks whose own pools are fine; and (per the medium finding above) with no skip the stuck rule never fires at all, so the dust state persists. Whether that is a defect depends on the rule the requester wants: the task statement says a purchase below a tenth of a round must not count, and an IMD/USDG pool that shallow is far below the ~2,200 IMD the sandwich argument needs, so paying as IMD after 30 days is defensible; but then the pool should not be called usable at 1% of a round. The two thresholds should agree: either require maxConvert() >= MAX_ROUND_IMD/10 for usability (every unclipped purchase is then at least 0.4 IMD, and a dust IMD/USDG position still counts as empty), or judge a real purchase against the round actually allowed (imdIn >= cap/10) with an absolute floor that keeps the 882666b4 finding 3 protection. Reported as info: value-neutral for holders and a consistency decision rather than a bug on its own.

**Reproduction**

Setup as test/Company.t.sol but the IMD/USDG full-range liquidity is 400e18 instead of 10,000e18. maxConvert() == 1e18 (0.25% of 400), which is >= MAX_ROUND_IMD/100, so the pool is usable; cap = 0.2 IMD per stock. alice and bob each buy 1,000 IMD; warp 1 minute; convert(): out[1] > 0 (NVDA bought), pendingConvert(1) == 5.8e18 (0.2 IMD spent), yet failingSince(1) != 0 and waitingSince(1) is unchanged: the successful purchase counts as failing. Reproduced in test/scratch/ShallowImdPoolProbe.t.sol (passes, i.e. confirms the state). Continuing daily for 31 days and then skipping once with a 4-day-old NVDA feed pays 4 IMD as IMD (audit_math's reproduction, consistent with the finding above).

### 6. Info: README still says a failed purchase moves only 'one round's capped amount' to IMD; the code moves min(pending, 4 IMD) regardless of the cap or pool limit

`README.md:134`

```
- **IMD fallback.** Only one round's capped amount moves to IMD per failed purchase. Someone able to make a purchase fail on purpose (for example, a liquidity provider who pulls liquidity from a stock's pool in the same transaction) can turn that round's stock share into IMD. Holders still receive the full value, in IMD.
```

Since the dddb75ec finding 1 fix, every fallback (_fallBackToImd from a stock-side failure, an empty or dust stock pool, or _skipOrFallBack) pays fullRound = min(pendingConvert[a], MAX_ROUND_IMD/5) = up to 4 IMD (CompanyToken.sol lines 727-729), explicitly never a swap-clipped amount. The README's 'Known and accepted' bullet still describes the old behaviour, which understates what a deliberately failed purchase moves: on the live GME/USDG pool a successful round is clipped to 3.11 IMD (fork today) and with IMD/USDG depth below 8,000 IMD the per-stock cap drops below 4 IMD, yet a forced failure still moves the full 4 IMD. Documentation fix only: state that a failed purchase moves min(reserve, 4 IMD), independent of maxConvert() and stockRoundLimit().

**Reproduction**

Unit harness: _buy(alice,1000e18); _buy(bob,1000e18) (6 IMD reserved per stock). Remove the IMD/USDG full-range liquidity and re-add 4,000e18 so maxConvert() = 10 IMD and the per-stock cap = 2 IMD; block GME for the token contract (stocks[3].setBlocked(address(token), true)); warp +1 minute; convert(). The README wording predicts 2 IMD moving to IMD for GME; actual: pendingConvert(4) goes 6e18 -> 2e18 and owed(0) rises by 4e18 (fullRound), as test_final4_1b also shows for a dust stock pool ('4 IMD paid, not the 0.045 the pool allows').

### 7. Info: _swapFee NatSpec says Uniswap's protocol fee is on only for IMD/USDG and GME/USDG; on the live chain all six route pools have it on (code reads it correctly)

`contracts/src/CompanyToken.sol:933`

```
    ///      it is switched on (0.1% on IMD/USDG and GME/USDG on Robinhood Chain; audit dddb75ec, finding 4).
```

_swapFee reads protocolFee from slot0 and picks the direction's 12 bits (lower for 0->1, upper for 1->0), then combines it with the LP fee as v4 does (pf + lp - pf*lp/1e6), so minUsdOut and minStockOut subtract the fee actually charged whatever the pool: request item 4 is confirmed correct. The comment is incomplete, though: on a fork of Robinhood Chain today the protocol fee is on for every route pool, not only the two named: IMD/USDG 0.1% each way, GME/USDG 0.1%, NVDA/USDG 0.0025%, GOOGL/USDG 0.05%, AAPL/USDG 0.05%, MSTR/USDG 0.04%. Nothing to fix in code; the NatSpec and README ('0.1% where it is on') should say the fee is read per pool and direction and is on for all six.

**Reproduction**

On a fork (FORK_RPC=https://robinhood.drpc.org) read getSlot0 of each pool returned by token.routeOf(1..5): protocolFee raw 4097000 (0x3E8|0x3E8<<12: 1000 ppm each way) for IMD/USDG and GME/USDG, 102425 (25 each way) for NVDA, 2048500 (500) for GOOGL and AAPL, 1638800 (400) for MSTR; test_final4_4 covers the arithmetic. Probe test/scratch/ForkProbe.t.sol logs these values.

---

Judge's submission `30e1f10a4c65789541a5d0255158337c3d8bd9f43f69174859a35285af05444c`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
