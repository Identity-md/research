# Audit report

> The Zero Person Billion Dollar Company ($COMPANY): a pre-launch audit of one token on Robinhood Chain (4663). Read AUDIT.md first; it lists the guarantees and the known, accepted limits.
>
> What the contracts are for:
> - CompanyToken: a fixed 1,000,000,000 supply ERC-20 with permit. Ownership is renounced in the constructor; there is no mint and no upgrade.
> - CompanyHook: owns the token's only Uniswap v4 pool, paired with IMD. All liquidity is locked forever. It takes 4% of the IMD side of every swap: 1% to the protocol, 3% to holders.
> - CompanyRouter and CompanyEthRouter: buy and sell with IMD or ETH.
> - Holder fees are split 50% IMD and 10% each to NVDA, GOOGL, AAPL, AMC and MSTR Robinhood stock tokens. The stock share is bought IMD -> USDG -> stock at the start of every claim() (or by anyone calling convert()). Each round spends at most 0.25% of the IMD/USDG pool's depth, each stock converts at most once a minute, and each stock runs in an isolated self-call.
> - Only wallets holding at least 100,000 $COMPANY earn. Unclaimed rewards expire after 7 days of inactivity and go to the fee recipient.
>
> Look hardest at:
> 1. Solvency of all six reward assets: balances always cover what is owed and waiting to convert.
> 2. Reward capture with flash-borrowed pool tokens, or from one's own trade.
> 3. The conversion: can it be sandwiched profitably, pushed past its cap, or run more than once per stock in one block?
> 4. Stock tokens have blocklists: a blocked stock or holder must never block claims, trades or the other assets.
> 5. The 100,000 minimum: eligibleSupply must always equal the sum of weights, and crossing the line must never change rewards already earned.
> 6. Expiry: recycle must never move more than expiredRewardsOf, and only to the fee recipient.
> 7. Anything that would make a scanner flag a honeypot, hidden owner, owner-can-change-balance or a suspicious function.
>
> Tests: cd contracts; git submodule update --init --recursive; forge test. Fork test: FORK_RPC=https://robinhood.drpc.org forge test --mc CompanyForkTest.

| | |
|---|---|
| Repository | https://github.com/imdmaxi/IMDINDEX.git |
| Commit | `9fe5e93ea62d45be49fdbe9db13f91db8af17331` |
| Job | `78c00339-8764-4684-920c-0958d23472c0` |
| Judged | 2026-10-07 08:27 UTC |
| Findings | 1 high · 5 low · 3 info |

Four agents audited the code as it is at `9fe5e93`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: maxConvert() reads in-range liquidity at call time: just-in-time liquidity inflates the round cap and makes sandwiching convert() profitable

`contracts/src/CompanyToken.sol:595`

```
        uint256 liquidity = IPoolManager(poolManager).getLiquidity(id);
```

The only bound on how much IMD a conversion round sells is maxConvert(): 0.25% of the IMD/USDG pool's virtual IMD depth, derived from PoolManager.getLiquidity(id), i.e. the liquidity active at the current tick of a hookless, permissionless pool, read in the same transaction as the sale. Anyone can add a narrow position around the current tick with modifyLiquidity and remove it again in the same transaction, so the caller chooses the cap. AUDIT.md guarantee 4 ('sandwiching costs more in that pool's 0.9% fees than it can move the price') only holds while a round is really limited to 0.25% of the liquidity the attacker trades against. With the cap inflated, one round sells the entire pendingConvert of all five stocks (the 1-minute spacing and the self-call isolation do not help: it is one round), into the attacker's own position at a price the attacker pushed just before. The attack is one atomic transaction from a contract (swap, add liquidity, token.convert(), remove liquidity, swap back are separate unlocks; the isUnlocked() guard only blocks conversion inside a foreign unlock), carries no inventory risk, and is repeatable every CONVERT_INTERVAL while a reserve waits. Victims are all $COMPANY holders: the stock share of their fees is bought at the pushed price. On the fork (block ~26139145) the IMD/USDG pool has ~19,752 IMD of virtual depth, so the honest cap is 49.39 IMD per round (read from the fork test); the push-and-buy-back fee cost is ~0.9% x 2 of the push, so the attack pays once the five reserves together exceed roughly 1-2% of the pool's depth (~180 IMD, i.e. about $120k of trade volume since the last round; reserves only drain when someone claims or converts). Merged from audit_math, audit_permissions, audit_flow and audit_economics (same root cause, same line). Minimal fix that keeps the design: do not let a round be bounded only by state the caller can change in the same transaction. For example add an immutable absolute per-round ceiling (the attached proof passes with `if (cap > 50e18) cap = 50e18;` before dividing by five), and/or cap the round by min(current depth, depth recorded at the previous round in an earlier block) and skip the round when the IMD/USDG sqrtPrice has moved more than a small bound since the stored one. Reading liquidity from a previous block alone is not enough on a chain with sub-second blocks.

**Reproduction**

forge test --match-path test/scratch/ConvertCapJit.t.sol (run from contracts/). Setup identical to test/Company.t.sol: IMD/USDG full-range at 1:1 with 10,000 IMD of virtual depth (honest maxConvert() = 25 IMD). alice buys 1,000 IMD, bob buys 10 x 3,333 IMD through CompanyRouter: 514.95 IMD waits in the five reserves. Warp 60 s. Attacker holding 1,000,000 IMD + 1,000,000 USDG, no $COMPANY: (1) PoolSwapTest exact-in 10,000 IMD -> USDG on IMD/USDG; (2) PoolModifyLiquidityTest adds 2,000,000e18 liquidity over 3 tick spacings around the new tick; maxConvert() now returns 10,004.77 IMD; (3) token.convert(): imd.balanceOf(token) drops by 514.95 IMD (every stock's whole reserve, 20x the honest cap, sold at ~0.25 USDG/IMD); (4) remove the position; (5) swap all USDG gained back to IMD. Expected: the round sells at most 25 IMD and the attacker's IMD+USDG (valued 1:1) after <= before. Actual: the test fails with 'sandwiching the conversion must not be profitable: 2000249.54e18 > 2000000e18' (attacker +249.54 IMD-equivalent after all fees; holders' 514.95 IMD became ~130 USDG worth of stock). With a 50 IMD absolute cap patched into _convertAll the same test passes (round sells 50 IMD, attacker ends -97.5).

### 2. Low: Second hop (USDG -> stock) is sized only by the IMD/USDG pool: a stock pool thinner than ~round/fee is sandwichable, and nothing on-chain enforces that

`contracts/src/CompanyToken.sol:559`

```
        uint256 stockOut = _swapExactIn(_key(usd, assets[asset], stockPools[asset]), usd, usdOut);
```

Each stock's share of a round is maxConvert()/5 and its USDG output is swapped into the fixed USDG/stock pool with no minimum output and no cap related to that pool's depth or fee. The 'fees exceed price impact' argument needs stockDepth > perStockRound / fee; for the deployed tiers (USDG/NVDA 0.01%, AMC 0.1%, MSTR 0.25%, GOOGL/AAPL 0.3%) that means the NVDA pool must stay at least ~5x deeper than IMD/USDG. On the fork the stock pools are $8M-$170M deep against ~$198k for IMD/USDG, so the attack is not profitable today (audit_permissions' fork simulation: a $2k-$200k push loses 0.5-50 USDG); it becomes profitable whenever IMD/USDG liquidity grows or a stock pool's liquidity leaves, both permissionless, and the routes cannot be changed. Merged from audit_flow (medium) and audit_permissions (info); kept as low because the exploit needs third-party liquidity to change first. Fix: bound each stock's round by its own pool too, e.g. min(cap/5, fee_bps/BPS x that pool's virtual USDG depth), or skip the stock when its pool price moved more than a small bound since the previous round. An absolute per-round ceiling (the fix for the high finding) also bounds this leg.

**Reproduction**

forge test --match-path test/scratch/StockHop.t.sol (passes, i.e. the sandwich is profitable). IMD/USDG at 1:1 with 1,000,000e18 liquidity (per-stock round 500 IMD), USDG/NVDA at 1:1 with the deployed tier (fee 100, spacing 1) and 20,000e18 liquidity; alice buys 1,000 IMD, bob 5 x 3,500 IMD: 55.5 IMD waits for NVDA. Attacker: buy NVDA with 5,000 USDG, call token.convert(), sell the NVDA back. Expected (AUDIT.md guarantee 4): unprofitable. Actual: the round buys 35.12 NVDA for holders instead of 54.84 (-36%) and the attacker ends +18.91 USDG.

### 3. Low: Hook fee on IMD-specified swaps is charged on the requested amount: partial fills at a price limit overpay, and an exact-out sell can Panic inside the hook

`contracts/src/CompanyHook.sol:279`

```
        uint256 fee = exactIn ? (amount * FEE_BPS) / BPS : (amount * FEE_BPS) / (BPS - FEE_BPS);
```

When IMD is the specified currency (exact-in buy, exact-out sell) beforeSwap computes the fee from params.amountSpecified, charges it and stores it in FEE_SLOT; afterSwap reads it back unchanged. Uniswap v4 fills a swap only up to sqrtPriceLimitX96 (or the end of liquidity) without reverting, so when the pool delivers less than requested the swapper still pays 4%/96% of the full request, far more than 4% of what traded. The IMD-unspecified cases are correct because afterSwap uses the realised delta. Second effect at line 319: the Trade event computes `poolQuote - fee`, which underflows (Panic 0x11, surfaced as Wrap__FailedHookCall) when a partially filled exact-out sell delivers less IMD than the pre-computed fee, so the swap fails with an opaque error. CompanyRouter and CompanyEthRouter use exact-in with extreme limits and are unaffected on buys; third-party routers (Universal Router exact-out, any integrator passing a real price limit) reach it. Loss is bounded by the user's own parameters. Merged from audit_math and audit_permissions. Fix: in afterSwap compare the provisional fee with 4% of the IMD the pool actually moved and either revert with a clear PartialFill error or charge only the realised fee and credit the difference back; and compute the event's quoteAmount without an unchecked-looking subtraction (e.g. clamp).

**Reproduction**

forge test --match-path test/scratch/Leads.t.sol --match-test exactOutSellPartialFill (both pass, demonstrating the behaviour). Setup as test/Company.t.sol; alice and bob each buy 1,000 IMD (pool holds 1,920 IMD). alice via PoolSwapTest sells $COMPANY exact-out 3,000 IMD (amountSpecified = +3000e18) with sqrtPriceLimitX96 2,000 ticks from the current tick. Expected: fee = 4% of the IMD actually paid out. Actual: pendingHolderFees+pendingProtocolFees grow by exactly 125 IMD (3000e18*400/9600) while alice receives 86.74 IMD: 5,903 bps of the gross delivered. With a limit 40 ticks away the swap reverts with Wrap__FailedHookCall wrapping Panic(0x11) (revert data contains 4e487b71...11) because poolQuote < fee at line 319.

### 4. Low: Anyone can reset any wallet's 7-day expiry timer for free by moving 1 wei out of the PoolManager with take()

`contracts/src/CompanyToken.sol:328`

```
            if (!toSystem && (msg.sender == to || from == poolManager || lastActive[to] == 0)) {
```

A transfer whose `from` is the PoolManager is treated as a buy and refreshes lastActive[to]. The contract notice and AUDIT.md section 4 assume this costs the buyer the 4% fee. It does not: inside a plain PoolManager.unlock anyone can take(COMPANY, victim, 1), then sync + transfer(1) + settle from their own balance. No swap, no hook, no fee: the recipient's timer is reset by a stranger for gas. After the ping expiredRewardsOf(victim) is 0, so recycle() and the strict claim move nothing to feeRecipient; a keeper (or the inactive holder's second wallet) can keep every wallet 'active' forever, voiding the expiry stream that AUDIT.md guarantee 6 describes. Nobody's tokens are at risk. Merged from audit_permissions and audit_economics. Fix: count a receipt from the PoolManager as activity only when it is part of a swap through this token's pool (e.g. the hook records the buyer in afterSwap in a transient slot the token checks), or drop the from == poolManager rule and rely on msg.sender == to / router delivery; and correct the documented assumption.

**Reproduction**

forge test --match-path test/scratch/Leads.t.sol --match-test freeTimerReset (passes, demonstrating the behaviour). alice and bob buy 1,000 IMD each; bob sends 1 wei $COMPANY to contract P. Warp 8 days: expiredRewardsOf(alice, 0) > 0. P calls poolManager.unlock and in its callback does take(COMPANY, alice, 1); sync(COMPANY); transfer(poolManager, 1); settle(). Expected (per the notice): a stranger cannot refresh alice's timer without paying the 4% buy fee. Actual: lastActive[alice] == block.timestamp, expiredRewardsOf(alice, 0) == 0, pendingHolderFees and pendingProtocolFees unchanged, recycle(alice) returns 0.

### 5. Low: releaseStuckReserve treats an idle stock as stuck: lastConvert is not refreshed when nothing is waiting, so a healthy stock's fresh reserve can be diverted to IMD by anyone

`contracts/src/CompanyToken.sol:606`

```
        if (block.timestamp <= lastConvert[asset] + STUCK_PERIOD) revert TooSoon();
```

lastConvert[a] is set at deployment and advances only on a successful convertStock or a release. _convertAll skips a stock with nothing waiting (`if (imdIn == 0) continue;`) without touching it, and reserves drain to zero within a few rounds whenever pendingConvert < cap. After any 30-day window without a successful conversion of stock a (simply no trades, or no reserve), the first fee arrival makes releaseStuckReserve(a) succeed immediately for anyone, in the same block as the trade and before any conversion was attempted. The notice says this path is for 'a stock that can't be bought for 30 days'; here it fires on a stock that converts fine in the same block. The promised asset mix for that batch is broken at a third party's choice (IMD instead of stock), and it hands a large holder immediately claimable IMD instead of a stream of later rounds. Merged from audit_permissions and audit_flow. Fix: measure stuckness from failed attempts, e.g. also stamp lastConvert[a] = block.timestamp when a round finds nothing to convert for a, or record when the reserve became non-zero and require STUCK_PERIOD since max(that, lastConvert[a]).

**Reproduction**

forge test --match-path test/scratch/Leads.t.sol --match-test releaseHealthyIdleStock (passes, demonstrating the behaviour). alice and bob buy 1,000 IMD each (6 IMD reserved per stock); warp 1 min, convert(); warp 1 min, convert(): all reserves are 0. Warp 31 days with no trades. carol buys 1,000 IMD: pendingConvert(1) == 3e18; a snapshot shows convert() buys NVDA normally. Expected: releaseStuckReserve(1) reverts TooSoon. Actual: it returns 3e18, pendingConvert(1) becomes 0 and owed[0] grows by 3e18.

### 6. Low: The stock half of each fee is credited to holders at conversion time, not when the fee was paid, so whoever holds during an attacker-timed convert() takes the accumulated reserve

`contracts/src/CompanyToken.sol:550`

```
        distributeStock(asset);
```

distribute() credits the IMD half of a holder fee to the holders of that moment, but the five stock reserves are credited only in convertStock -> distributeStock, pro rata to eligibleSupply at conversion time, which can be minutes to days after the fees were paid and which anyone triggers with the public convert() once per minute. This contradicts the comment at line 317 ('Rewards stay with whoever held the tokens when they were earned, for every asset'): a holder who sold between fee arrival and conversion gets no stock, and a buyer who arrives after the fees were paid does. Unlike the accepted 'dividend sniping around large trades' (AUDIT.md section 4), the sniper chooses the moment and the prize is the whole accumulated reserve paid out at maxConvert() per round; with the 4% fee each way it pays whenever reserve >> 8% of the position cost, which at the planned 306 IMD launch market cap is a few hundred IMD of reserve. From audit_economics. Fix (design choice): keep a per-share index of 'IMD reserved' at distribution time and credit each stock pro rata to that index, or convert on every distributing trade so the timing is not attacker-chosen; otherwise document it next to the accepted sniping limit.

**Reproduction**

forge test --match-path test/scratch/Leads.t.sol --match-test stockCreditedToHoldersAtConversionTime (passes, demonstrating the behaviour). alice buys 1,000 IMD and is the only eligible holder while bob buys and sells 3,333 IMD ten times (NVDA reserve > 100 IMD, all from fees paid while only alice held). carol then buys 4,000 IMD (19.3% of eligible weight), warp 1 min, carol calls convert(). Expected (per the line-317 comment): the stock bought with those fees is alice's. Actual: carol is credited 0.955 NVDA and alice 3.983, exactly carol's current weight share of every round.

### 7. Info: Stock already bought and owed to holders has no fallback if the stock token blocklists the token contract: the 30-day release covers only the unconverted IMD reserve

`contracts/src/CompanyToken.sol:608`

```
        amount = pendingConvert[asset];
```

AUDIT.md guarantee 7 says a stock blocked for 30 days 'can be released to IMD holders'. releaseStuckReserve moves only pendingConvert. Stock bought by earlier rounds sits in owed[asset]; if the stock token later blocks this contract as a sender, every _tryTransfer of that asset fails: claim() keeps it claimable forever, _recycle cannot move it to feeRecipient either, and no path converts or releases it. The contract cannot move tokens it is blocked from sending, so no in-contract fix exists; the gap is in the stated guarantee. From audit_flow. Fix: document that already-converted stock is unrecoverable after a blocklisting of the contract (the release only covers the IMD reserve), or hold converted stock in a separate per-stock escrow contract so a blocklisting of one address does not freeze all of it.

**Reproduction**

forge test --match-path test/scratch/Leads.t.sol --match-test owedStockFrozenWhenTokenBlocked (passes, demonstrating the behaviour). alice and bob buy 1,000 IMD; warp 1 min; convert(): owed[1] = 4.94 NVDA. MockStock NVDA blocks address(token). alice.claim(): paid[1] == 0 (PayoutFailed). Warp 8 days, recycle(alice): expired[1] == 0 (refused). Warp 30 days, releaseStuckReserve(1) moves only the 1 IMD still pending. Expected: a way to redirect the unpayable stock after 30 days. Actual: owed[1] stays 4.94 NVDA and the contract still holds it, with no function able to move it.

### 8. Info: Expired stock rewards are paid to the claimer when the stock token blocks feeRecipient

`contracts/src/CompanyToken.sol:504`

```
                withdrawnRewards[a][holder] -= amount;
```

claim() first runs _recycle(msg.sender); if the stock token refuses the transfer to feeRecipient the expired amount is put back into the holder's withdrawable balance, and the same claim then pays it to the claimer and resets the timer. The notice says expired rewards 'go to the protocol address'; a feeRecipient that a stock token blocks (plausible given US-person restrictions, and the hook owner can point it anywhere) silently turns strict expiry into no expiry for that stock. No user loses funds. From audit_permissions. Fix if strictness matters: keep refused expired amounts in a separate per-holder bucket that only a later recycle can move, instead of re-adding them to the claimable balance.

**Reproduction**

forge test --match-path test/scratch/Leads.t.sol --match-test blockedFeeRecipient_expiredStockGoesToClaimer (passes, demonstrating the behaviour). alice and bob buy 1,000 IMD; warp 1 min; convert(); alice's NVDA = 4.34. Warp 8 days: expiredRewardsOf(alice, 1) == 4.34. MockStock NVDA blocks FEE_RECIPIENT. alice.claim(). Expected: paid[1] == 0 (expired, stays for a later recycle). Actual: paid[0] == 0 (expired IMD went to the fee recipient) but paid[1] >= 4.34 NVDA was paid to alice.

### 9. Info: Trade event attributes CompanyEthRouter trades to tx.origin: the hookData carrying the real buyer is only decoded for CompanyRouter

`contracts/src/CompanyHook.sol:317`

```
        address trader = sender == router && hookData.length == 32 ? abi.decode(hookData, (address)) : tx.origin;
```

CompanyEthRouter passes abi.encode(r.user) as hookData on the token-pool swap ('so the hook credits the right buyer'), but afterSwap decodes hookData only when sender == router. For ethRouter trades the event names tx.origin, which differs from the user for smart-contract wallets, relayers and batched calls; third-party routers' trades are attributed to tx.origin as well. Event-only, no accounting depends on trader. Note also that tx.origin in the hook is a pattern some scanners flag; it is harmless here. Merged from audit_permissions and audit_flow. Fix: `(sender == router || sender == ethRouter) && hookData.length == 32`.

**Reproduction**

forge test --match-path test/scratch/Leads.t.sol --match-test tradeEventTxOriginForEthRouter (passes, demonstrating the behaviour). A contract wallet W calls ethRouter.buyWithEth{value: 1 ether}(token, 0, deadline) from a transaction whose tx.origin is alice. Expected: Trade.trader == W. Actual: Trade.trader == alice.

---

Judge's submission `a1223f180c24a6aae6982ff54de7078802186c677477b4c4a7c4f7726e95fb9f`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
