# Audit report

> Final check 3 for The Zero Person Billion Dollar Company ($COMPANY) on Robinhood Chain (4663), after IMD Swarm audit 78c00339, re-check f1d5def3, final check 363ab052 and final check 2 882666b4. AUDIT.md sections 4 to 7 map every finding to its fix and its test.
>
> What the contracts are for: CompanyToken is a fixed 1,000,000,000 supply ERC-20; its ownership is renounced in the constructor. CompanyHook owns the token's only Uniswap v4 pool, paired with IMD, with liquidity locked forever, and takes 4% of every swap in that pool: 1% to the protocol, 3% to holders. Holder fees are split 50% IMD and 10% each to NVDA, GOOGL, AAPL, GME and MSTR Robinhood stock tokens, bought IMD -> USDG -> stock at the start of every claim(), with each purchase checked against Chainlink. Only wallets holding at least 100,000 earn. If a wallet goes more than 7 days without claiming, buying, selling or sending, its unclaimed rewards older than 7 days expire.
>
> Changed since 882666b4; review these hardest:
> 1. Root-cause fix for the flash-borrow expiry bypass (findings 1 and 2): _transfer records in transient storage the $COMPANY each address received from the PoolManager in the current transaction (FROM_POOL_SEED; moved along when forwarded, reduced when returned), and expiredRewardsOf leaves that amount out of the weight used for "recent" rewards. Can a borrowed balance still count, through any path (forwarding chains, system accounts, transferFrom, routers, markActive)? Can the tag ever make a transfer revert, or expire rewards an honest holder earned in the last 7 days?
> 2. The IMD/USDG pool counts as empty while maxConvert() is below 1% of a full round (0.2 IMD), and the empty clock (imdPoolEmptySince) restarts unless re-confirmed within a day (imdPoolLastSeenEmpty).
> 3. feedLastGood: an unusable feed (revert, answer <= 0) is dead only after DEAD_AFTER without a usable answer.
>
> Please confirm these, check that nothing broke the solvency of the six reward assets, the flash-borrow guard, the 100,000 minimum, expiry or the scanner-relevant properties (no external calls in transfers), and report anything new.
>
> Tests: cd contracts; git submodule update --init --recursive; forge test. Fork test (live Chainlink feeds and pools): FORK_RPC=https://robinhood.drpc.org forge test --mc CompanyForkTest.

| | |
|---|---|
| Repository | https://github.com/imdmaxi/IMDINDEX.git |
| Commit | `3b09bc77b05166950f33681048e0fe2f0f59a854` |
| Job | `986abba2-68de-47d2-be7e-4c68f5525e3b` |
| Judged | 2026-10-07 13:53 UTC |
| Findings | 1 medium · 3 low |

Four agents audited the code as it is at `3b09bc7`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Empty IMD/USDG pool: a small position at a made-up price clears the 1% emptiness threshold and every round sells the stock reserves into it for dust

`contracts/src/CompanyToken.sol:680`

```
        if (roundCap < MAX_ROUND_IMD / 100) {
```

The emptiness test for the IMD/USDG pool (review item 2) uses maxConvert(), i.e. the pool's *virtual* IMD depth L/sqrtP at the current price. Once the real liquidity is gone at and below the current price, anyone can move the price anywhere for free (a swap through a pool with no in-range liquidity moves the price to the limit without exchanging tokens), then post a narrow position there. At a price where 1 IMD is worth ~1e-9 USDG, about 41 IMD of real capital gives a virtual depth of ~940 IMD, so maxConvert() reads 2.3 IMD (and with more capital up to the 20 IMD ceiling), the pool no longer counts as empty, imdPoolEmptySince is reset to 0, and the next round sells each stock's capped IMD into that position for dust USDG. The second hop then passes minStockOut because it is checked against usdOut, not against imdIn (AUDIT.md section 8 accepts that the IMD -> USDG hop has no oracle 'resting on the pool's depth'; here the depth is the attacker's). The attacker can call convert() every minute, so the five stock reserves (50% of every holder-fee distribution accrued while the real pool is empty) drain to the position's owner at up to 20 IMD per minute instead of either waiting or being paid to holders as IMD after DEAD_AFTER. This is the limit case of the accepted thin-pool sandwich, but it needs no sandwich and no price move within a transaction: the position just sits there. It also means the 30-day fallback for an abandoned pool (363ab052 finding 3, 882666b4 finding 3) can be both pre-empted and profited from. Precondition: no real IMD/USDG liquidity in range at and below the current price (an abandoned pool, or a concentrated LP whose range the price has left on the downside). Fix options that keep the design: (1) anchor the first hop: store the IMD/USDG rate of the last successful round (usdOut/imdIn) and skip (PriceOff-style, no fallback) a round whose rate is more than a bounded factor away, or derive an IMD/USD reference from the IMD/ETH pool and an ETH/USD feed; (2) in addition, define emptiness by in-range liquidity L against a floor fixed at deployment (e.g. 1% of the launch pool's L) rather than by virtual depth, since real capital for a given L explodes away from the honest price.

**Reproduction**

State: alice and bob each buy 1,000 IMD through CompanyRouter (pendingConvert = 6 IMD per stock); the IMD/USDG pool's only position (10,000 L, full range) is removed, so maxConvert() == 0 (pool counts as empty). Input, by the attacker: one swap of 1 wei with a price limit at tick +/-207,000 (price moves for free), then modifyLiquidity(lo = target - 900, hi = target + 900, L = 3e16): the position holds 41.24 IMD and 0.00000004 USDG. Now maxConvert() = 2.343 IMD (>= 0.2 IMD, no longer 'empty'). Warp 1 minute, refresh feeds, call convert(). Expected: the round waits (the pool has no usable liquidity at a sane price) or, after DEAD_AFTER, is paid to holders as IMD; the position's owner gains nothing. Actual: each stock round sells 0.4686 IMD (2.343 IMD total) for dust: NVDA bought = 474,156,573 wei (4.7e-10 NVDA) and credited to holders; pendingConvert(1) drops 6e18 -> 5.531e18 with owed(0) unchanged (assert '468613088435602910 != 0'); after removing the position the attacker holds 2.343 IMD more than before. Repeating convert() every minute drains the reserves. Proof: contracts/test/scratch/ProofEmptyPoolLp.t.sol (fails on this code; passes once the round is held, falls back to IMD, or the position is treated as empty).

### 2. Low: FROM_POOL tag also excludes the tagged tokens' share of distributions that ran later in the same transaction: a contract wallet that buys through a third-party router and claims in one transaction los

`contracts/src/CompanyToken.sol:575`

```
        uint256 weight = _weight(bal > tagged ? bal - tagged : 0);
```

Merged from audit_math, audit_flow, audit_economics and audit_permissions (same mechanism, same line; all four reproduce). expiredRewardsOf estimates 'recent' rewards as (magnifiedRewardPerShare - magAt(cutoff)) x weight and, since 882666b4, leaves every $COMPANY received from the PoolManager in this transaction out of that weight, on the assumption that those tokens 'earned nothing yet'. That holds only until a distribution runs in the same transaction after the receipt: claim() calls hook.flush() and _convertAll() (lines 531-532) before _recycle(msg.sender) (line 536), and both credit the holder's full balance (eligibleSupply includes the tagged tokens) while the expiry estimate still excludes them. The tagged tokens' share of that flush and of this round's stock credits is therefore classified as expired and sent to feeRecipient, seconds after it was credited. The same under-estimate applies to a send in that transaction after a flush (_forfeit in _transfer). Reachable only by an honest holder: a smart-contract wallet (its signer or bundler is tx.origin, so afterSwap's markActive does not make the wallet active) that has been inactive for more than 7 days, buys through a router other than CompanyRouter/CompanyEthRouter (no flush before the take) and claims in the same batched transaction. EOAs are marked active by the buy, the official routers flush before the take, and claiming in a later transaction avoids it. The flash-borrow attack this tag closes can never reach a distribution after the receipt (distribute/flush/convert are blocked inside a foreign unlock, claim and recycle revert there), so nothing on the attack side relies on the tag persisting past a distribution. Loss is bounded by the new tokens' pro-rata share of what was distributed in that transaction (mostly the wallet's own 3% fee, plus up to one stock round) and goes to the fee recipient. So the answer to review item 1's question 'can the tag expire rewards an honest holder earned in the last 7 days' is yes, in this one case. Fix that keeps 'no external call in transfers': in claim(), run _recycle(msg.sender) and set lastActive before flush() and _convertAll() (this transaction's credits then land on an active wallet; for every other holder credits at `now` are recent anyway), and for the send-after-flush case either bump a transient distribution epoch in _credit and ignore a tag older than the current epoch, or record the per-share level at each tagged receipt and add tagged x (mag_now - mag_at_receipt) / MAGNITUDE back into 'recent'.

**Reproduction**

State (test/scratch/ProofTagSameTx.t.sol): a contract wallet W buys 20 IMD worth of $COMPANY through PoolSwapTest (a plain v4 router) and is active by first receipt; bob buys 20 IMD (W earns); warp 8 days; bob buys 10 IMD (one distribution inside W's last 7 days). expiredRewardsOf(W, 0) = 0.3 IMD. Input, one transaction from W with tx.origin = its signer: [1] PoolSwapTest.swap buying with 1,000 IMD (W receives ~631M tagged tokens, the hook marks the signer active, 30 IMD of holder fees wait in the hook), [2] token.claim(). Expected: at most the 0.3 IMD that had expired before the transaction goes to the fee recipient and W is paid the rest, including its share of the 15 IMD the claim's flush credits. Actual: totalRecycled(0) and imd.balanceOf(FEE_RECIPIENT) grow by 12.649 IMD (assert '12649389304807710912 > 300000000000000000'): the tagged tokens' share of the flush, credited seconds earlier in the same claim, is treated as expired. The suite's own test_final2_* tests do not cover a distribution after a tagged receipt.

### 3. Low: feedLastGood is written only when a stock's round actually reaches its purchase, so after 30 days without a round one unusable read declares the feed dead at once

`contracts/src/CompanyToken.sol:715`

```
            feedLastGood[usdFeed] = block.timestamp;
```

Merged from audit_math, audit_flow, audit_economics and audit_permissions (same root cause; all reproduce). Review item 3 states that an unusable feed (revert, no data, answer <= 0) is dead only after DEAD_AFTER (30 days) without a usable answer. The only memory of usable answers is feedLastGood, written in the constructor and at lines 715-716, i.e. only when that stock's round is due (CONVERT_INTERVAL), has IMD waiting, the IMD/USDG pool is not in its 'empty' branch (early return at line 685), stockRoundLimit >= cap/100 and both feeds read fresh. While any of those gates is closed (no trades for a while, that stock's reserve already drained, the IMD/USDG pool below the emptiness threshold, a weekend-stale feed), feedLastGood stays frozen although the feed answers correctly on every claim. When the feed is then unusable for even one call, _feedAge falls back to _sinceGood, which is measured from that stale timestamp: once it exceeds 30 days, _feedsDead is true immediately and _fallBackToImd credits that round's stock share (up to MAX_ROUND_IMD/5 = 4 IMD per stock, one round per minute while the glitch lasts) to holders as IMD. For the shared USDG/USD feed this hits all five stocks (20 IMD per round). Holders keep the value as IMD instead of stock, so the impact is bounded to the accepted 'one capped round' outcome per unusable call, but the property 882666b4 finding 4 was fixed to provide does not hold. Fix: record a usable answer whenever one is observed, independently of whether a round runs: at the top of _convertAll (before the IMD-pool early return and the per-stock gates) read the USDG feed and each stock feed with _readFeed and set feedLastGood[feed] = block.timestamp when ok; or replace _sinceGood with a feedUnusableSince[feed] set on the first unusable observation and cleared by a usable one, dead only when block.timestamp > feedUnusableSince + DEAD_AFTER.

**Reproduction**

State (test/scratch/ProofFeedLastGood.t.sol): fresh deployment (feedLastGood = T0); for 31 days nobody trades, every feed is refreshed daily with answer 1e8 and convert() is called daily (nothing pending, so line 715 never runs). Then alice and bob buy 1,000 IMD each (pendingConvert[1] = 6 IMD); warp 1 minute; refresh all feeds; make the NVDA feed's latestRoundData revert for this one call; call convert(). Expected (contract notice, AUDIT.md section 7 finding 4): the NVDA round is held, pendingConvert(1) stays 6e18, owed(0) unchanged. Actual: _sinceGood(NVDA) = 31 days + 1 minute > DEAD_AFTER, so _feedsDead(1) is true and _fallBackToImd(1, 4e18) runs: pendingConvert(1) == 2e18 and owed(0) grows by 4e18 (assert '2000000000000000000 != 6000000000000000000'). The existing test_final2_4_unusableFeedHoldsUntilDeadAfter passes only because a good round ran a minute earlier.

### 4. Low: The empty-pool clock restarts unless convert()/claim() runs every day, so the 30-day IMD fallback for an abandoned IMD/USDG pool needs a daily keeper for 30 consecutive days

`contracts/src/CompanyToken.sol:681`

```
            if (imdPoolEmptySince == 0 || block.timestamp > imdPoolLastSeenEmpty + 1 days) {
```

Merged from audit_flow, audit_economics and audit_permissions (same mechanism; all reproduce). The fix for 882666b4 finding 6 restarts imdPoolEmptySince whenever the previous emptiness observation (imdPoolLastSeenEmpty) is more than one day old. Observations happen only inside _convertAll, i.e. on claim() or convert(). With the IMD/USDG pool genuinely without liquidity nothing can be bought, claims pay only IMD and nothing makes anyone call daily; any single gap over 24 hours in the 30 days resets the clock to zero, and after the dead state is reached the same branch runs first, so one missed day stops the fallback rounds and restarts the 30-day wait. The DEAD_AFTER fallback introduced for 363ab052 finding 3 (medium: an empty pool locks the five stock reserves, 50% of every holder-fee distribution, forever) is therefore conditional on off-chain liveness that neither the contract nor the documentation provides ('no keeper needed'), in exactly the scenario where claims are rarest. The else-branch already resets the clock whenever the pool is seen with liquidity, so the daily re-confirmation only guards against liquidity that came and went unobserved between two calls, whose cost is one 20 IMD round paid as IMD (holders keep the value) versus reserves locked for good. Fix that keeps the finding-6 intent: widen the re-confirmation window so a normal claim cadence suffices (e.g. 7 days = INACTIVITY_PERIOD), or count confirmations at least a day apart instead of requiring an unbroken daily chain, and document whatever cadence remains.

**Reproduction**

State (test/scratch/ProofEmptyClock.t.sol): alice and bob each buy 1,000 IMD (6 IMD pending per stock); the IMD/USDG pool's only position is removed, maxConvert() == 0. Input: convert() is called every 2 days, feeds refreshed each time, for 90 days (45 confirmations of an uninterrupted empty pool). Expected (contract notice: 'after DEAD_AFTER of confirmed emptiness every stock's rounds are paid to holders as IMD'): from day 31 each call credits 5 x 4 IMD to holders as IMD, so pendingConvert(1) < 6e18. Actual: on every call block.timestamp > imdPoolLastSeenEmpty + 1 days, imdPoolEmptySince restarts, no ConversionFailed event, pendingConvert(1) is still 6e18 after 90 days (assert '6000000000000000000 >= 6000000000000000000'). The existing test_final3_emptyImdPoolFallsBackToImdAfter30Days passes only because it calls convert() every single day.

---

Judge's submission `ffece18c9a8470ff5a4208fd9fbcceef2f126aa1046a23818c76acad116a7880`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
