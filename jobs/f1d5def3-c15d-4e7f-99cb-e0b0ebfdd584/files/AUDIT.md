# Audit report

> Re-check of IMD Swarm audit 78c00339 (which audited commit 9fe5e93) for The Zero Person Billion Dollar Company ($COMPANY) on Robinhood Chain (4663). AUDIT.md section 4 maps each finding to its fix and its test.
>
> What the contracts are for: CompanyToken is a fixed 1,000,000,000 supply ERC-20; its ownership is renounced in the constructor. CompanyHook owns the token's only Uniswap v4 pool, paired with IMD, with liquidity locked forever, and takes 4% of every swap: 1% to the protocol, 3% to holders. CompanyRouter and CompanyEthRouter buy and sell with IMD or ETH. Holder fees are split 50% IMD and 10% each to NVDA, GOOGL, AAPL, AMC and MSTR stock tokens, bought IMD -> USDG -> stock at the start of every claim(). Only wallets holding at least 100,000 earn, and unclaimed rewards expire after 7 days.
>
> Fixes to verify:
> 1 (high) JIT liquidity inflating maxConvert(): fixed per-round ceiling MAX_ROUND_IMD = 20 IMD. Test: test_audit1_jitLiquidityCannotInflateRound replays your attack.
> 2 (low) USDG -> stock hop: per-stock limit stockRoundLimit(asset) = half the stock pool's fee x its virtual USDG depth, priced in IMD. Test: test_audit2_thinStockPoolLimitsItsRound.
> 3 (low) partial fills: CompanyHook.afterSwap reverts PartialFill unless an IMD-specified swap filled completely; the Trade event amount is clamped. Test: test_audit3_partialFillIsRejected_fullFillWorks.
> 4 (low) free timer reset: receipts from the PoolManager no longer count as activity. Test: test_audit4_poolManagerPingDoesNotResetTimer.
> 5 (low) releaseStuckReserve was removed: a failed stock purchase now credits that round's IMD to holders at once (_fallBackToImd), inside a self-call with a fixed gas budget (CONVERT_GAS); a claim with too little gas reverts with NotEnoughGas. Please review this new path hardest: can anyone force the fallback?
> 6 (low) and 7 (info): accepted and documented in the CompanyToken notice and README.
> 8 (info): refused expired rewards stay in recycledHeld until sendRecycled. Test: test_audit8_expiredStockHeldWhenFeeRecipientBlocked.
> 9 (info): the Trade event decodes the user for both routers. Test: test_audit9_ethRouterTradeLogsRealBuyer.
>
> Please confirm each fix and check that none of them broke the solvency of the six reward assets, the flash-borrow guard, the 100,000 minimum, expiry, or the scanner-relevant properties (no honeypot, hidden owner, owner-can-change-balance or suspicious function). Report anything new.
>
> Tests: cd contracts; git submodule update --init --recursive; forge test. Fork test: FORK_RPC=https://robinhood.drpc.org forge test --mc CompanyForkTest.

| | |
|---|---|
| Repository | https://github.com/imdmaxi/IMDINDEX.git |
| Commit | `ece5d4c9c599c4b56b2a1c1577b8032638b5b3a1` |
| Job | `f1d5def3-c15d-4e7f-99cb-e0b0ebfdd584` |
| Judged | 2026-10-07 09:50 UTC |
| Findings | 1 medium · 2 low · 2 info |

Four agents audited the code as it is at `ece5d4c`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Fix 2 bypass: stockRoundLimit reads same-transaction liquidity, so just-in-time liquidity lifts a thin stock pool's limit back to the full 4 IMD share and the stock hop can be sandwiched at a profit

`contracts/src/CompanyToken.sol:654`

```
        uint256 liquidity = IPoolManager(poolManager).getLiquidity(sk.toId());
```

Merged from audit_permissions (low), audit_economics (medium, part a) and audit_math (low); all three reproduce. stockRoundLimit(asset) sizes a stock's round as fee/2 x the USDG/stock pool's virtual USDG depth, where the depth is getLiquidity() at the current tick read in the same transaction as the round. That is exactly the read finding 1 (high) showed to be inflatable: fix 1 added the fixed MAX_ROUND_IMD ceiling for the IMD/USDG hop, but the stock hop got only this manipulable read and no ceiling in the stock pool's own fee terms. An attacker who (1) pushes the stock pool's price in the direction the round moves it, (2) mints a narrow, large position around the pushed tick, (3) calls convert() (or lets any claim() run the round), (4) removes the position and (5) swaps back, makes stockRoundLimit read far above the 4 IMD share, so _convertAll sells the full min(pending, MAX_ROUND_IMD/5) = 4 IMD into the attacker's position with no minimum output (_swapExactIn sets none; convertStock only rejects stockOut == 0). The guarantee the fix claims (contract notice: 'A sandwich of that hop then costs more in the pool's fee than it can move the price'; AUDIT.md section 3 item 4) does not hold in the thin-pool scenario the fix was written for, which is the scenario test_audit2_thinStockPoolLimitsItsRound models. Loss is bounded by the 4 IMD share per stock per CONVERT_INTERVAL, about 85% of it extractable, and repeatable every minute while that stock's reserve has IMD; the attack transaction can check the pool and revert when it is deep, so trying it every minute costs only gas. Not exploitable on today's mainnet state: on the fork (block of 2026-10-07) stockRoundLimit reads 680-1,667 IMD, far above the 4 IMD share, and pushing through the market makers' hundreds of thousands of USDG of in-range liquidity costs more in pool fees than a 4 IMD round is worth. It becomes profitable whenever a stock pool's real in-range depth falls below roughly (4 IMD in USDG) / pool fee: about $400k of depth for NVDA (0.01%), $40k for AMC (0.1%), $16k for MSTR (0.25%), $13k for GOOGL and AAPL (0.3%) at $10 per IMD, including the moments when market makers withdraw and re-place their positions. AUDIT.md section 5 covers an LP forcing the IMD fallback, not this: here the round succeeds and holders receive stock worth a small fraction of the IMD spent. Fix that preserves the design: do not price a round from state the same transaction can set. Record each stock pool's sqrtPriceX96 at deployment and after every successful round, and skip (do not fall back) a round whose current price deviates from that reference by more than a few percent, so a same-transaction push can never be the execution price (a manipulation then has to persist across a full CONVERT_INTERVAL, exposed to arbitrage); or enforce a minimum output per round derived from that reference price. This patch, together with the one for the zero-liquidity case, was applied locally: the attached proof passes and the project's 37 tests still pass. A fixed per-stock ceiling scaled to the pool fee alone (share x fee/9000) only bounds the loss; in the thin pool it stays profitable.

**Reproduction**

Local suite setup (IMD/USDG 1:1 with 10,000 depth; USDG/NVDA fee 0.3%, spacing 60). alice and bob each buy for 1,000 IMD, so 6 IMD waits per stock. The NVDA pool's LP removes 999,990e18 of its 1,000,000e18 liquidity, exactly as test_audit2_thinStockPoolLimitsItsRound does: stockRoundLimit(1) = 0.015 IMD. Warp 1 minute. Attacker (100,000 USDG, 100,000 NVDA): (1) swaps 30 USDG for NVDA through PoolSwapTest (the price moves to roughly 0.1 NVDA per USDG); (2) mints L = 50,000e18 over 180 ticks around the new tick: stockRoundLimit(1) now reads 299.38 IMD; (3) token.convert(): pendingConvert(1) drops by 4e18 and the contract receives 0.248 NVDA (about 3.95 at the honest price); (4) removes the position; (5) sells the NVDA from the push back. Expected (fix 2): the NVDA round spends at most 0.015 IMD and the attacker's USDG+NVDA (valued 1:1) does not grow. Actual: the round spends 4 IMD and the attacker ends 3.6019 USDG+NVDA richer (200,003.6019e18 vs 200,000e18). Run: cd contracts; forge test --match-path test/scratch/JitStockLimit.t.sol -vv. Fails on this code with 'sandwich of the stock hop is profitable: 200003601874124907240677 > 200000000000000000000000'; passes with a reference-price check as described.

### 2. Low: Fix 2/5: a stockRoundLimit of zero (no liquidity at the current tick) removes the per-stock limit instead of skipping; the v4 swap crosses the gap and the whole 4 IMD round fills at the next resting p

`contracts/src/CompanyToken.sol:555`

```
            if (imdIn > poolLimit) imdIn = poolLimit == 0 ? imdIn : poolLimit; // an empty pool fails below -> IMD
```

Merged from audit_permissions (medium) and audit_economics (medium, part b); reproduces. _convertAll treats stockRoundLimit(a) == 0, which stockRoundLimit returns when getLiquidity() is 0 at the stock pool's current tick, as 'empty pool, the swap will fail and the round falls back to IMD', and keeps imdIn at the full per-stock cap (4 IMD). That is not how a Uniswap v4 swap behaves: Pool.swap steps across a zero-liquidity range to the next initialized tick, crosses it and fills there (lib/v4-core/src/libraries/Pool.sol swap loop; only a pool with no position anywhere leaves the input unfilled, which _swapExactIn then rejects with Slippage). With no minimum output anywhere on the path, whoever owns the next initialized position sells the whole capped round at the price that position sets, with no capital at risk beyond resting an order, and can collect up to 4 IMD of that stock's reserve every CONVERT_INTERVAL from every claim() or convert() until the reserve is gone. The limit added for finding 2 is removed in exactly the state the pool is most exposed, and the code comment, the contract notice ('Zero for a pool with no liquidity (the round then falls back to IMD)') and AUDIT.md section 5 ('holders still receive its full value in IMD') all describe a fallback that does not happen. maxConvert() handles the same reading the other way (zero depth gives a cap of 0 and no round runs). Reachability today is limited: every live stock pool holds a dust full-range position, so getLiquidity() at the current tick is small but not zero (then the limit is tiny and binds), and an attacker cannot empty a full-range position alone; the state arises when those dust LPs withdraw and the market makers' concentrated positions are out of range or being re-placed. Fix: never widen a round on a zero reading: `if (imdIn > poolLimit) imdIn = poolLimit;` so a zero limit skips the stock this round (or call _fallBackToImd directly without swapping, if the IMD fallback is preferred). With that one-line change the attached proof passes and the project's 37 tests still pass.

**Reproduction**

Local suite setup. alice and bob each buy for 1,000 IMD, so 6 IMD waits per stock. (1) The NVDA pool's LP removes all 1,000,000e18 of its liquidity: pm.getLiquidity(poolId) == 0 and token.stockRoundLimit(1) == 0. Warp 1 minute. (2) The attacker mints one position of L = 2,000e18 at ticks [-46080, -46020] when USDG is currency0 (mirrored, [46020, 46080], otherwise), about 100x the fair NVDA price on the side the purchase moves toward; it holds about 0.6 NVDA and no USDG; stockRoundLimit(1) still reads 0. (3) Anyone calls token.convert(). Expected (code comment, contract notice, AUDIT.md section 5): the round is skipped or its 4 IMD is credited to holders as IMD. Actual: pendingConvert(1) drops by 4e18, no ConversionFailed, owed(0) unchanged, and the contract receives 0.0396 NVDA for 4 IMD (fair about 3.95). (4) The attacker removes the position and ends 3.92 USDG+NVDA richer (2,003.9228e18 vs 2,000e18). Run: cd contracts; forge test --match-path test/scratch/ZeroLiquidityGap.t.sol -vv. Fails on this code with 'resting position sold the whole round at its own price: 2003922797156961323124 > 2000000000000000000000'; passes with `imdIn = poolLimit`.

### 3. Low: Fix 5 side effect: the gas a claim() needs jumps by about 1.07M per due stock while the gas it uses does not, so a claim sent with the limit from an estimate made before a round became due reverts wit

`contracts/src/CompanyToken.sol:559`

```
            if (gasleft() < (CONVERT_GAS * 64) / 63 + 50_000) revert NotEnoughGas();
```

From audit_flow (low); reproduces. The new path is sound in what it prevents: the self-call always receives exactly CONVERT_GAS, so a caller cannot starve a purchase into _fallBackToImd, and a short claim reverts without state change (test_lowGasClaim_isRefused_notTurnedIntoImd). Its side effect is that the gas a claim needs is a step function of state the caller does not control. For every stock with pendingConvert > 0 whose minute has elapsed, the loop demands gasleft() >= 1,065,873 at that point, although the purchase then consumes 100k-300k. A claim with nothing due uses about 479k gas; the same claim one minute later uses about 975k but needs a limit well above 1.07M at the first due stock, and a further 1M-plus headroom at each later due stock whose predecessor used little. Wallets set the gas limit from eth_estimateGas plus a 10-50% margin, so any claim estimated while the last round was less than a minute old and included after the minute boundary reverts with NotEnoughGas, and the holder pays for a failed transaction; with reserves waiting, rounds are due every minute, so this window recurs every minute. The same state can be created by anyone: when every reserve is fully converted (estimation sees no conversion at all), a dust swap through any router (1e15 wei of IMD, fee 4e13 wei) leaves holder fees in the hook; the victim's claim flushes them, every pendingConvert becomes nonzero, and the claim reverts for the same reason. A purchase that fails by exhausting its budget (a swap made to cross many initialized ticks) also consumes the full 1M, so the gas needed grows by that much more than the estimate. No funds are at risk; the effect is failed claims and wasted gas. Fix that keeps the starvation protection: when gasleft() is below the headroom, `continue` instead of reverting. A skipped stock is neither bought nor fallen back, so a low-gas caller still cannot turn stock into IMD, and anyone can run convert() later. Alternatively keep the revert and document that claim() must be sent with a fixed limit (about 5 x 1.1M plus payouts) so front-ends do not size it from an estimate.

**Reproduction**

Scratch test (contracts/test/scratch/GasEstimate.t.sol, run with forge test --match-path, removed after the review) on the repo's own setup. Scenario 1: alice buys 1,000 IMD, bob buys 10,000 IMD (the reserve stays > 0 after a round), warp 1 minute, convert(). alice's claim() with nothing due uses 479,448 gas and succeeds. Warp 1 minute; the same claim sent with 1.5 x 479,448 = 719,172 gas: expected (from the estimate) success; actual: revert with selector NotEnoughGas. Sent with 5M gas it succeeds and uses 975,114. Scenario 2: alice buys 1,000 IMD, bob buys 100 IMD, convert() empties all five reserves (pendingConvert == 0); a claim now uses 550,691 gas; the attacker swaps 1e15 wei of IMD through PoolSwapTest; alice's claim sent with 2 x 550,691 = 1,101,382 gas reverts with NotEnoughGas. Expected: a claim whose estimate was valid seconds earlier succeeds; actual: it reverts whenever a round became due or a dust fee arrived in between.

### 4. Info: README still describes the removed 30-day release (finding 5) and an outdated test count

`README.md:127`

```
- **Fixed routes.** The conversion pools can't be changed after deployment. If liquidity leaves them, conversion slows or stops, and the 30-day release applies.
```

From audit_flow (info); confirmed. Finding 5's resolution removed releaseStuckReserve and the 30-day release entirely; the contract now falls back to IMD one capped round at a time (_fallBackToImd), as AUDIT.md section 4 and the contract notice say. README.md line 127 ('the 30-day release applies') and line 82 ('blocked holders and blocked stocks, including the 30-day release') still describe the old mechanism, and line 73 says 'forge test # 31 unit, attack and fuzz tests' while the suite has 37. A reader of the public README, the document scanners and holders are pointed to, is told that a reserve stuck by a drained pool is released after 30 days; in the shipped code it is paid out as IMD, at most 4 IMD per stock per minute, as soon as a purchase fails. Fix: replace both 30-day sentences with the IMD-fallback description already used in the 'IMD fallback' bullet, and update the count.

**Reproduction**

grep -n '30-day' README.md returns lines 82 and 127; grep -rn 'releaseStuck\|30 days' contracts/src returns nothing (the only time constants in CompanyToken.sol are INACTIVITY_PERIOD = 7 days and CONVERT_INTERVAL = 1 minutes). cd contracts; forge test reports 37 tests in Company.t.sol against the README's 31 on line 73.

### 5. Info: AUDIT.md section 5 still lists 'a router buy resets the recipient's expiry timer' as accepted behaviour, which fix 4 made false

`AUDIT.md:57`

```
- A buy delivered by a router to another address resets that address's expiry timer (costs the buyer 4%).
```

Merged from audit_economics (info) and audit_math (info); confirmed. After fix 4, CompanyToken._transfer (lines 338-341) records activity for the recipient only when the recipient initiated the transfer (msg.sender == to) or on its first receipt (lastActive[to] == 0). Tokens delivered by the PoolManager, which is how both routers deliver a buy (poolManager.take(cOut, d.user, out)), no longer touch an existing holder's lastActive; test_expiry_giftsAndBuysDontResetTimer_claimDoes asserts that a buy is not activity, and the contract notice and README say 'buying alone does not count: claim at least weekly'. Section 5 of the brief still describes the pre-fix behaviour as a known and accepted way to reset another wallet's timer at a 4% cost, so a reviewer or holder reading the brief expects a buy to keep a wallet's rewards alive when it does not. Fix: delete the bullet or reword it (a buy delivered to a wallet that has never held $COMPANY sets its first lastActive; a buy to an existing holder changes nothing).

**Reproduction**

contracts/test/Company.t.sol, test_expiry_giftsAndBuysDontResetTimer_claimDoes: alice holds and is 8 days inactive; _buy(alice, 1e18) through CompanyRouter delivers tokens from the PoolManager to alice; expiredRewardsOf(alice, 0) stays > 0 and lastActive(alice) is unchanged. test_audit4_poolManagerPingDoesNotResetTimer shows the same for a direct PoolManager delivery. Expected per AUDIT.md line 57: the timer is reset. Actual: no reset.

---

Judge's submission `60b43c7582e74763252818ed3bd0457e34f61bd214598d6510432001d5c10cd8`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
