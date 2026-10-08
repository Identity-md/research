# PAPER farming for Swarm Pepe / OG holders

Research snapshot: **8 October 2026**, approximately 15:32–15:40 UTC. Research only; no trades, deposits, deployments, signatures, or keys were used.

**Recommendation:** prepare a non-custodial holder frontend, but do not accept farming deposits until the published deployment and relayer integration pass the gates below. Model equal-notional BTC long/short positions at modest leverage, close voluntarily after a meaningful move, and stake with a separate wallet signature. A 1% BTC move costs approximately **$0.001389/PAPER** before external costs and staking rebates under the documented initial mint rate, assuming both legs execute as modeled and the winner is paid. A 3% move lowers that to $0.001267, but takes more time and exposes the position to a longer path and execution risk. This is acquisition of an illiquid revenue claim, not a guaranteed profitable trade.

**Availability finding:** the primary website still displayed “trade coming soon”; every Papertrade deployment address was TBA. The docs describe third-party signed intents through the relayer, but provide no public endpoint, schema, or onboarding procedure. Therefore an independently usable “send ETH and farm” product is **not presently verified**. This report supplies a concrete implementation specification and release gates, not a claim that an integration already works. [Website](https://papertrade.xyz/), [addresses](https://docs.papertrade.xyz/#/dev/contract-addresses), [frontend FAQ](https://docs.papertrade.xyz/#/intro/faq).

## Evidence and scope

Labels used throughout:

- **Documented:** stated in Papertrade's official documentation; not verified against deployed code because addresses/source were unavailable.
- **Source-verified:** inspected verified contract source, with its provenance specified; this is not an audit.
- **Derived:** calculation or inference from documented mechanics.
- **Proposed / unknown:** design choice or unanswered integration issue, never a claim of current functionality.

The requested `research-report` skill was absent from the available skill catalog and filesystem search. Research proceeded using the task's evidence requirements. All **23 navigation pages** were read from the official client bundle, including Quick start; normal web extraction returned only the empty application shell. The exact bundle was [index-Crm0Tgz1.js](https://docs.papertrade.xyz/assets/index-Crm0Tgz1.js), SHA-256 `7be94652a6c1a0600a7081717f708505f085bec74653d313e660b0b1bdc3fd4f`. The page inventory is at the end. The linked Martingaler PDF was downloaded but not independently analyzed; the docs' Martingaler summary was read. No claim of a whitepaper or protocol audit is made.

Searches covered Papertrade relayer/API, contract repositories, audit references, EIP-1271, and the supplied distributor. No authenticated Papertrade ABI, deployed address set, relayer API specification, public farming policy, or audit report was located. Same-name PAPER tokens on other chains were excluded because the official docs did not authenticate them. Missing public integration information is a research result; it is not filled with invented addresses.

A [mirror of the project's launch announcement](https://www30.twstalker.com/papertrade_xyz) reports predeposits on October 8, frontend-only trading October 10, followed by open contracts, builder codes, and eventual token transfers. **Secondary evidence only:** direct X access failed. Treat this as a launch-access warning, not proof of the current contract configuration. It conflicts with the docs' broad third-party-frontend wording; obtain a primary relayer-access confirmation before release.

## 1. Exact mechanics, with unresolved details explicit

### Pricing, impact and fees

**Documented:** Papertrade is synthetic; its positions do not execute perps on HyperCore. HyperEVM chain ID is 999. `PriceOracle` reads BBO precompile `0x000000000000000000000000000000000000080e`, with BTC asset index 0 and ETH 1, and uses `(bid + ask)/2`. Zero or crossed quotes revert. There is no independent deviation, TWAP, or lookback breaker. No funding, spread, notional fee, or user-paid trading gas is documented. The relayer pays execution gas. “Zero market impact” on the landing page means no execution-book impact; **winning PnL still suffers an impact haircut**. [BBO pricing](https://docs.papertrade.xyz/#/how/pricing-bbo), [trading](https://docs.papertrade.xyz/#/learn/trades-pricing).

For a winning price move `m = abs(exit-entry)/entry`, define `d = 1/50000 = 0.00002`, i.e. **0.2 bps = 0.002%**. Remove this deadband first: `x = max(m-d,0)`. For notional `N`, the documented floating-point approximation is:

```text
raw gain after deadband = N*x
scale = (1-baseRate) / (1 + 1/(x*rateMultiplier)
                         + referenceNotional/(10^6*x*positionMultiplier))
adjusted gain A = N*x*scale
trader win W = 0.98*A
```

At `x=0`, payout is zero; do not divide by zero. Launch parameters: `baseRate=0.10`, `rateMultiplier=15000`, `referenceNotional=$100,000`, `positionMultiplier=814.598` for BTC and `483.979` for ETH. The move inside the implementation's impact curve uses the deadband-adjusted exit. The reference notional is fixed per instrument, not the trader's position size. The 2% win fee is applied **after** impact. Integer rounding and exact directional boundary behavior require the real implementation. [Asymmetric impact](https://docs.papertrade.xyz/#/how/asymmetric-impact).

For an ordinary losing close, raw loss `L=N*m` is charged without an added trader fee. If the queue is empty and the loss fee applies, 2% is carved from the LP gain: PAPER basis is `0.98L`. With an active queue the loss fee is waived and basis is `L`. **Liquidation mints on the full lost margin `M` even when a 2% LP-side liquidation fee is charged.** Liquidation forfeits the full isolated margin, not merely the loss at the trigger. Its approximate price buffer is 5 bps before zero equity: around 9.95% adverse at 10x, 0.95% at 100x, and the docs give about **0.052% at 1000x**. Never implement exact bust prices from the approximate `1/leverage - 0.0005` heuristic. [Mint basis](https://docs.papertrade.xyz/#/how/mint-curve), [liquidation](https://docs.papertrade.xyz/#/learn/liquidations).

### Mint rate

**Documented:** the initial flat region pays 100 PAPER/$ of eligible loss basis while tracked LP is below $2M, including underwater. The tail uses:

```text
r(H) = 100 * (S/(S+H))^2,   S = $120,000,000
H = tailProgressUsd, a non-decreasing cumulative tail-progress high-water mark
```

`H` is not current LP balance. Staker drains reduce tracked LP but do not unwind tail progress. Examples: `H=$0 → 100`, `$30M → 64`, `$100M → 29.7521`, `$120M → 25 PAPER/$`. At 25 PAPER/$ every cost/PAPER in the flat-rate tables is multiplied by four. [Mint curve](https://docs.papertrade.xyz/#/how/mint-curve).

**Unknown:** the docs simultaneously describe a below-threshold flat branch and permanent rate decay after tail advancement. They do not fully disambiguate a later fall below $2M after tail progress. Do not model rate restoration by draining LP. Nor assume a trade crossing the threshold gets its opening marginal rate for the whole loss. If loss basis advanced `H` one-for-one, the integral over `[H0,H1]` would be `100*S^2*(1/(S+H0)-1/(S+H1))`; that is a mathematical illustration, **not verified contract mint logic**. All tables use losses fully inside the initial flat region.

### LP, queue and revenue

**Documented:** tracked LP is tokenomics accounting, not total deposits or treasury USDC. LP starts without seed capital; users cannot directly deposit to LP. Available user balances, open margin and accrued fees are liabilities, not free LP bankroll. With an active FIFO queue, `lpBankrollAvailable()` is zero for new winners. Losses park in `sideBucket`, and `harvest(maxEntries)` pays existing claims in order, debiting that bucket first. Residual sideBucket becomes ordinary LP cash when the queue clears. The keeper normally calls `harvest(32)`; permissionless callers receive no documented bounty. [Queue mechanics](https://docs.papertrade.xyz/#/how/solvency-queue), [LP overview](https://docs.papertrade.xyz/#/learn/lp-queue).

A USD-funded winning close returns its margin immediately; only unpaid profit queues. A losing close returns remaining margin. A debt-funded position consumes an existing queued claim; its **entire surviving claim**, including collateral, can queue again. Losing such a position destroys part of the claim and can mint PAPER, net of any applicable loss fee. A queue promise is not a guaranteed repayment date: payment requires future backing cash. The docs' language that winners eventually get paid is conditional on replenishment. [Settlement](https://docs.papertrade.xyz/#/how/solvency-queue).

Stakers receive half of each 2% trading fee: equivalently **1% of adjusted winning PnL**, or 1% of raw losing PnL / lost liquidation margin when fees are actually funded. “1% of PnL” does not mean 1% of notional, nor 1% of pre-impact winning profit. The other half goes to the dev recipient. Fees do not get paid ahead of queue claims. LP excess above **$5M tracked LP** is also sweepable to stakers. `Exchange.pushStakerFees()` is public; distribution uses keeper-signed `distributeBySig` through the relayer. Rewards accrue by stake share at distribution, not automatically as cash in a holder's wallet at each trade. [Dividends](https://docs.papertrade.xyz/#/learn/staking-dividends), [staking mechanics](https://docs.papertrade.xyz/#/paper/staking).

### Limits, authorizations and money routes

- **Limits:** up to 1000x and $10M notional per position; independent configurable long/short OI caps. Default keeper policy targets current OI plus $5M headroom per side, resetting outside $4.5M–$5.5M headroom. This is not a $5M total OI cap. Minimum margin and minimum notional are keeper-set; **numeric current minima are unpublished**, and the 10 USDC deposit minimum is not a trade-margin minimum. Positions cannot be topped up, partially closed, or resized. [Risk](https://docs.papertrade.xyz/#/how/risk), [trades](https://docs.papertrade.xyz/#/learn/trades-pricing).
- **Session keys:** 30-day lifetime; trade intents valid one hour. Open/close only, potentially using available or queued balances. Registration goes through the relayer. Stake, unstake, claim and withdrawal need the real wallet's signature. Direct `revokeSessionKey` needs HyperEVM HYPE gas and cancels queued key-signed trades. A compromised key can lose the account balance despite being unable to withdraw it. [Session keys](https://docs.papertrade.xyz/#/learn/session-keys).
- **Execution:** configured relayers alone submit to BatchExecutor; its intents settle independently. A batch is not evidence of all-or-nothing paired trading. Opens, closes, session registration, proxy deployment and staking are gated. Direct `withdrawToCore` is wallet-callable; anyone can relay `withdrawToCoreBySig` with the real wallet signature. [Architecture](https://docs.papertrade.xyz/#/how/architecture), [risk](https://docs.papertrade.xyz/#/how/risk).
- **Deposits:** USDC routes from HyperCore, HyperEVM, Ethereum, Arbitrum and Solana; USDG via Across from Robinhood Chain. At least 10 USDC must arrive after route costs, with a one-time 1 USDC account activation charge. Frontend quotes must settle the exact first-deposit minimum. Withdrawals minimum 10 USDC, limited to available balance. ETH requires an additional swap into USDC; Papertrade is not an ETH deposit contract. [Deposits/withdrawals](https://docs.papertrade.xyz/#/learn/deposits-withdrawals).
- **CREATE2:** register the owner's deterministic proxy address with the relayer before sending. CCTP/HyperCore routes land on its Core account. HyperEVM native USDC uses CoreDepositWallet; an ERC-20 transfer straight to the proxy is not monitored as a deposit. Only relayer keys deploy proxies; `requestSweep(user)` and `finalizeSweep(user)` are public. Overlapping deposits can obscure the balance-decrease check and require owner reconciliation, so send one deposit and await credit before the next. No factory, salt encoding or init-code hash was published here. A deterministic deposit address does not prove contract-wallet trading support. [CREATE2 deposits](https://docs.papertrade.xyz/#/how/deposits).

## 2. Farming economics

### Comparable cost definition

**Derived:** equal-notional long and short positions with matched entry and exit prices have one raw loss `L=N*m` and one win `W` after deadband, impact and fee. They do not have perfectly equal realized PnL. Use:

```text
PAPER Q = r * b * N*m            b=0.98 solvent voluntary close; b=1 active queue
Economic pair cost C = N*m-W
Acquisition cost c = (C + external costs - received rebates)/Q
Cash reduction while winner remains queued = N*m + external costs
Discounted cost if recovery fraction is q = (N*m-q*W+external costs-rebates)/Q
```

`q` incorporates default and time-value discounts; it is not inferred from queue length alone. No PAPER sale proceeds are counted. Both legs' margin is capital committed, **not** an extra acquisition expense. At zero realized loss there is no mint and cost/PAPER is undefined. Flat-rate cost does not improve by splitting size across wallets or raising leverage: size cancels in `C/Q`.

The following table is generated by the accompanying offline `calculations.py`. It assumes no liquidation, matched fills, full eventual recovery, no route costs, unchanged launch parameters and no staking rebate. The active-queue column is an economic accrual value, **not immediately withdrawable USDC**.

| Move | BTC win / raw loss | BTC $/PAPER, empty | ETH $/PAPER, empty | BTC $/PAPER, active* |
|---:|---:|---:|---:|---:|
| 0.05% | 60.71% | 0.004009 | 0.004699 | 0.003929 |
| 0.1% | 72.43% | 0.002813 | 0.003307 | 0.002757 |
| 0.25% | 81.29% | 0.001910 | 0.002162 | 0.001871 |
| 0.5% | 84.63% | 0.001569 | 0.001706 | 0.001537 |
| 1% | 86.38% | 0.001389 | 0.001461 | 0.001362 |
| 2% | 87.28% | 0.001298 | 0.001334 | 0.001272 |
| 3% | 87.59% | 0.001267 | 0.001291 | 0.001241 |

BTC retains more of a win at any fixed move because its larger positionMultiplier reduces the denominator. ETH could nevertheless reach a target move sooner; no observed volatility sample or return-per-day forecast was collected. As moves become very large, the theoretical flat-rate solvent limit is `(1-0.98*0.9)/98 = $0.00120408/PAPER`. This is a limiting curve, not an achievable guaranteed floor: margin, time, path and queue risk intervene.

### Leverage versus move

Cells below show the losing leg's raw loss as a percentage of its own margin, `100*leverage*move`. BUST means the approximate trigger is passed, invalidating voluntary-close economics. NEAR is unsafe boundary proximity; at 1000x the docs' approximately 0.052% trigger makes a 0.05% target precarious. Actual onchain bust values and execution delay override this table.

| Move | 10x | 25x | 50x | 100x | 250x | 500x | 1000x |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.05% | 0.5% | 1.2% | 2.5% | 5.0% | 12.5% | 25.0% | NEAR |
| 0.1% | 1.0% | 2.5% | 5.0% | 10.0% | 25.0% | 50.0% | BUST |
| 0.25% | 2.5% | 6.2% | 12.5% | 25.0% | 62.5% | BUST | BUST |
| 0.5% | 5.0% | 12.5% | 25.0% | 50.0% | BUST | BUST | BUST |
| 1% | 10.0% | 25.0% | 50.0% | BUST | BUST | BUST | BUST |
| 2% | 20.0% | 50.0% | BUST | BUST | BUST | BUST | BUST |
| 3% | 30.0% | 75.0% | BUST | BUST | BUST | BUST | BUST |

The hedge is only hedged while both legs remain alive and appropriately matched. After one liquidates, the remaining leg is directional. A subsequent reversal can lose its margin too. Smaller leverage lowers mint throughput per unit of margin but leaves room to reach larger, cheaper moves. **Proposed default: 25x, 1% absolute move**, 80% of available trading balance allocated equally to the two margins, 20% held in reserve. This is a design starting point, not an optimal leverage proven by historical testing. At a 1% move the loser consumes 25% of its margin, well below the roughly 3.95% bust distance.

### Worked pair and liquidation comparison

With $400 margin per leg at 25x, `N=$10,000`, a 1% BTC move produces `L=$100`, `A=$88.146917`, `W=$86.383978`, `Q=9,800 PAPER` and economic cost **$13.616022**. If the winner is unpaid, immediate cash is lower by $100 and there is an $86.383978 queue claim. At 50% recovery value, cost is `$56.808011/9800 = $0.005797/PAPER`; at zero recovery, `$0.010204/PAPER`. A small nominal acquisition price can conceal a much larger cash commitment.

At 1000x and $10,000 notional, margin is $10. At the docs' approximate 0.052% bust move, voluntary loss immediately before the trigger is about $5.20, while liquidation burns **$10**, minting 1,000 PAPER. The opposite BTC win at that move is about $3.19831. Liquidation pair cost is therefore about `$6.80169/1000 = $0.006802/PAPER`; a voluntary pair just below the trigger would be around $0.0039/PAPER with roughly 510 PAPER. Boundary timing is not dependable. At 100x and a roughly 0.95% trigger, the liquidation pair costs about $0.0018/PAPER, still worse than the corresponding voluntary close. The full-margin mint basis gives liquidation only a 2.04% token advantage over voluntarily losing the *same dollars* solvently; the early hard-bust loss is usually more significant. [Liquidation evidence](https://docs.papertrade.xyz/#/learn/liquidations).

### Close order and timing

**Queue empty, adequately funded:** loser-first contributes roughly `0.98L` before the winner asks for `W` plus its fee. At documented launch parameters that contribution exceeds the paired adjusted win, improving payment availability. Prefer this for normal operation, but confirm settlement before submitting the next dependent close and measure residual exposure. It does not reserve liquidity against unrelated intervening winners.

**Queue empty, LP near zero:** winner-first may put your own win at the queue head; loser-second may waive its loss fee and supply enough sideBucket to pay that claim on harvest. This can improve Q from `98L` to `100L` (2.04% more) and is a non-obvious legitimate accounting consequence. It is **not an atomic or guaranteed loop**: other claims, relayer ordering, price drift, and liquidations can intervene. Loser-first is the more conservative default; winner-first is an experimental mode only after simulation and policy confirmation.

**Queue already active:** neither close order bypasses older creditors. Loser-first can fund other users while your later win joins the tail. Winner-first may secure an earlier place for your claim before contributing the loss, but the claim still follows existing debt. Model queue reduction, arrival rates and eventual recovery independently; a 2% mint-basis improvement does not compensate for an indefinite payout wait. Do not sell this as risk-free self-funding.

**Timing:** the early flat-rate window is the cheapest emission regime, but LP near zero has the most payout uncertainty. The attractive compromise is a funded, empty queue while the initial flat window remains. Volatility shortens the time to a target but increases legging, reversal, liquidation and intent-delay risks. Sideways tiny-move cycling is expensive. No measured time-to-target, execution-latency distribution or annualized yield is available.

### Early staking rebate: 1%, 5%, 20%

For stake share `s` already present at distribution, with solvent fees funded and no overflow:

```text
pair staker fee pool F = 0.01*L + 0.01*A
own rebate R = s*F
net cost/PAPER = (L-W-R)/Q
```

For the $10,000-per-leg, 1% BTC example, `F=$1.881469`:

| Existing stake share | Rebate, 1% BTC move / $10k per leg | Net $/PAPER |
|---:|---:|---:|
| 1% | $0.018815 | 0.001387 |
| 5% | $0.094073 | 0.001380 |
| 20% | $0.376294 | 0.001351 |

This small self-rebate is not a 1%, 5% or 20% refund of the deposit or total loss. At an active queue use zero paid fee rebate until actual distributable revenue exists. Freshly minted PAPER earns only after it is staked and included in a later distribution; a session key cannot do that. If the holder stakes between losing and winning closes, the loser-fee capture depends on distribution timing. Existing stakers' shares dilute as others stake. Stake/unstake has no cooldown, so just-in-time competition for distributions can dilute projected early share. Do not assume a persistent 20% share or privately preferred relayer sequencing. [Distribution rules](https://docs.papertrade.xyz/#/paper/staking).

Above $5M, add `s*D` for actual distributed LP excess `D`; do not assume every dollar of trading volume becomes excess. At higher tail progress lower emissions can dominate the rebate. Repeated farming may increase ownership, but it continually spends cash and has no assured break-even date.

### Ranked strategy set

Costs below use initial emissions, before route costs. Ranking prioritizes credible acquisition economics and controllable risk; USDC-only methods are separately identified because they mint no new PAPER.

| Rank / approach | Indicative $/PAPER or USDC economics | Main constraint / risk |
|---|---|---|
| 1. Modest-leverage BTC pair, voluntary close, 1–3% move | $0.001267–$0.001389 if fully paid | Execution mismatch, price path, payout liquidity; requires time |
| 2. Same pair with an existing stake | 1% example $0.001351 at 20% stake | Future stake share and fee distribution not guaranteed |
| 3. ETH pair at 1–3% | $0.001291–$0.001461 | Slightly worse fixed-move economics; may have different time-to-target |
| 4. Small-move BTC pairing, 0.05–0.1% | $0.002813–$0.004009 | More cycles; tempting high leverage causes hard-bust exposure |
| 5. Directional trading one already intends to do | Losing-close basis $0.010204/PAPER solvent; $0.010000 queue-active | Mint is a rebate, not protection against directional losses |
| 6. Deliberate liquidation | Standalone $0.010000/PAPER; pair depends on bust move, about $0.006802 at 1000x example | Full-margin loss and unhedged surviving leg; avoid as default |
| Conditional. External hedge against a Papertrade position | `(PT loss - external net gain + other costs)/Q` on a losing outcome | Basis, funding, fees, two liquidations, independent custody and adverse other outcomes |
| Conditional. Consume already queued claims as collateral | Claim value destroyed / newly minted PAPER; no new cash required for that margin | Sacrifices repayment rights; surviving debt requeues; not free PAPER |
| USDC only. Stake existing PAPER and wait | `s*(funded fees + LP excess)` | No mint; queue, dilution and protocol profitability risk |
| USDC only, future. Builder-originated revenue | Planned `0.01 * eligible LP-revenue carve` | Not live, base and settlement API unfinalized |
| No direct reward. Harvest, sweep, fee pushing | No documented keeper bounty for public caller | Gas expense; may accelerate one's own recovery |
| Not available at launch. Buy/borrow PAPER or LP deposit | No verified route | PAPER transfers disabled; no direct LP deposits |

**Directional rebate valuation:** with token value `v` dollars/PAPER, a solvent realized loss has effective cost `L*(1-98v)` before external costs. Cash loss is still `L`; `v` is uncertain and cannot be a realized market exit at launch. For symmetric ±m outcomes with win probability `p`, expected marked value is `p*W -(1-p)*L +(1-p)*98L*v - external costs`. At `p=0.5`, ignoring external costs, break-even `v` equals the corresponding pair cost/PAPER. Thus the mint does not create USDC-positive expectancy by itself.

**External hedge:** a Papertrade losing outcome can be offset by an external winning position, apparently acquiring PAPER for only external fees. The reverse outcome produces an external full loss against a haircutted Papertrade win and no PAPER. With symmetric outcomes and ideal linear hedging, averaging both outcomes returns the same haircut burden as an internal pair, before additional external costs. There is no evidence here for predictive selection that reliably forces only the favorable branch.

**Debt recycling:** a queued claim economically worth fraction `q` of face value could be burned into PAPER at roughly `q/r` per PAPER before fees. The cheaper number at small `q` reflects surrender of an impaired asset, not new arbitrage. No transferable claim market or ability to buy other users' debt was verified. Do not recursively count face-value queue winnings as newly available cash.

**Excluded claims:** no documented NFT-holder PAPER multiplier, referral mint, airdrop, direct LP yield deposit, keeper bounty, or risk-free oracle strategy was found. Holder status can gate our product or distribute our revenue; it does not alter Papertrade's tokenomics. No BBO manipulation or sybil evasion is recommended.

## 3. A holder product that can actually be built

### Feasibility comparison

| Design | Works now? | Launch / later status | Who holds the assets? | Build estimate, excluding protocol wait |
|---|---|---|---|---|
| A. Non-custodial guided frontend | Independent submission not verified; landing page not trading | Docs permit compatible relayer intents in principle; launch admission must be confirmed | Holder controls wallet and withdrawal signature; Papertrade contracts/Core accounts hold trading cash; browser holds trade key | 2–4 engineer-weeks after real ABI/API access, plus 1–2 weeks testing/security review |
| B. Pooled vault, one Papertrade account | No verified contract-account compatibility | Conditional on EIP-1271 or explicit contract-call support, relayer admission and contract-account withdrawal path; not proven at launch | Vault collectively owns cash and PAPER; its trader/keeper controls risk within policy | 6–10 engineer-weeks plus independent audit and bridge testing, realistically 8–12+ calendar weeks |
| C. Builder frontend → holder rewards | Builder codes explicitly not live | Future and undated; not a launch revenue assumption | Builder receiver holds earned USDC until bridged/distributed | 2–4 additional weeks after final builder API, plus contract review |

These are planning estimates, not quotes. None of these designs can promise an immediate Ethereum round trip while a Papertrade winning claim is queued. “Never” applies to specific incompatible paths: an external receiver cannot call the present hook-only OGDistributor funding methods; arbitrary PAPER transfers cannot work while transfer restrictions remain. Contract vaults are **unverified**, not inherently impossible forever.

### A. Recommended first: holder-owned account, guided execution

**Proposed transaction path, not just a calculator:**

1. Connect the holder's Ethereum EOA. Verify Pepe ownership or OG balance read-only against authenticated token/collection addresses; offer holder eligibility without asking the user to send an NFT or OG token. Eligibility is a product gate, not a Papertrade privilege.
2. Quote ETH→native Ethereum USDC, source gas, CCTP/forwarding, and minimum amount received. Keep gas reserve outside the amount to swap. User approves/signs through an established swap router. The frontend never receives custody of their ETH.
3. Register the holder's predicted Papertrade proxy with its official relayer. Derive and compare the address from the real factory, salt and init-code hash. Route USDC via the supported CCTP forwarding path to that proxy's **HyperCore** account. Alternatively CCTP to the holder on HyperEVM, then the documented CoreDepositWallet deposit-for path to the verified proxy, if supported by the current integration. Await bridge delivery, proxy deployment, sweep and Exchange credit; no trade before credit is confirmed.
4. Generate a browser session key, obtain the holder's wallet authorization and relayer registration. The key signs only opens/closes. Display that it can lose the trading balance, its expiry, and revocation instructions. No server-side session-key upload. Prefer memory-only key storage; encrypted persistence requires a separate security review.
5. Read actual margin minima, OI headroom, leverage limits, queue, LP accounting and mint state. Show a maximum loss budget and total margin. Default to available-balance collateral only, no queued-debt funding. With user consent to the risk budget, one UI action starts equal-notional BTC long/short intents at proposed 25x sizing. Match **actual asset quantities and executed entries**, not merely nominal form inputs.
6. Track both execution receipts. If only one leg opens, cancel the unfilled intent and flatten the live leg when possible. Never report a hedged state until both fills are known. Stop opening additional pairs after a partial failure; do not automatically scale up to recover a loss.
7. Monitor live BBO, actual bust prices, queue, and target economics. At a 1% target under normal funded conditions, close loser then winner, confirming results. An emergency close threshold uses bust distance and observed relayer latency, not just the target. A UI stop request cancels unsubmitted work but must also cancel accepted pending intents through the real API where supported.
8. Show minted PAPER, available USDC and queued USDC separately. Request a **new real-wallet signature** for `stakeBySig`; stake is not achievable using the trade session key. Show `pendingReward(holder)` and request wallet-signed claims. No promise of fully unattended staking.
9. For exit, close outstanding positions, claim rewards, withdraw available USDC to the holder's HyperCore account using the holder's real-wallet signature. Use the verified USDC Core→EVM path, CCTP back to Ethereum and optional USDC→ETH swap. Persist queue claims as outstanding assets; do not label them returned principal.

**Needed contracts:** authenticated deployed Exchange, BatchExecutor, SessionKeyManager, DepositProxyFactory/proxy, PriceOracle, PaperToken, PaperTokenomics and PaperStaking; Circle TokenMessengerV2/MessageTransmitterV2 and supported forwarding/CoreDepositWallet contracts; existing vetted swap router. No new custody contract is needed for v1. Product configuration must refuse missing addresses; it must not substitute a zero, burn or testing address.

**Relayer feasibility gate:** the docs explicitly say another frontend can produce the same signed intents and send them through the relayer. That establishes intended architecture, **not a working public API**. The absent items are base URL and access policy; CORS/authentication and rate limits; EIP-712 domains, type hashes and nonce/deadline rules; status/cancel/idempotency behavior; account/proxy registration; allowed paired trading; session registration; stake/claim payloads; per-leg ordering and execution guarantees. None was located in the 23 pages or site assets. Obtain official schemas and captured test vectors; do not guess paths such as `/trade`, bypass gating, or infer private endpoints from launch promises. [Frontend support](https://docs.papertrade.xyz/#/intro/faq), [architecture](https://docs.papertrade.xyz/#/how/architecture).

**Launch fallback:** if independent frontend access is not allowed, offer the same research, read-only monitoring and a handoff to the official UI once operational. That is a useful assisted flow but **does not satisfy one-click automated farming**; label it accordingly and leave execution disabled. A polished UI is not evidence of backend availability.

### Bridge details and real cost model

**Primary-source bridge facts:** Circle supports Ethereum and HyperEVM for CCTP, with domain IDs **0 and 19**, which differ from EVM chain IDs **1 and 999**. Its CoreDepositWallet source exposes `deposit` and `depositFor` for HyperCore delivery. Papertrade specifically documents CCTP deposits landing on the Core side of its proxy. Use the USDC-specific contracts; generic token system-address instructions are insufficient to prove the correct USDC route. [Circle domains](https://developers.circle.com/cctp/concepts/supported-chains-and-domains), [Circle CoreDepositWallet source](https://github.com/circlefin/hyperevm-circle-contracts/blob/master/src/CoreDepositWallet.sol), [Papertrade route](https://docs.papertrade.xyz/#/how/deposits).

Circle's fee page lists standard CCTP protocol transfers as free and Ethereum-source fast transfers at 1 bp at this snapshot. That does **not** remove Ethereum gas, swaps, destination execution, forwarding or return-route costs. The CoreDepositWallet source contains a configurable default forwarding-fee initialization of 0.2 USDC; it is not a verified current route quote. Fetch current fees and contract settings before signing. The return path must first withdraw actual available Papertrade cash to Core and use the supported USDC Core→EVM mechanism before burning for Ethereum. [CCTP fees](https://developers.circle.com/cctp/concepts/fees), [CoreDepositWallet](https://github.com/circlefin/hyperevm-circle-contracts/blob/master/src/CoreDepositWallet.sol), [HyperEVM onboarding](https://hyperliquid.gitbook.io/hyperliquid-docs/onboarding/how-to-use-the-hyperevm).

**Derived general estimate:** let `E` be ETH deposited, `P` the actual ETH/USDC swap execution price, `Cin` all inbound swap/bridge/gas costs in USDC-equivalent, `Cout` eventual return costs, and `a=1 USDC` for first activation (zero thereafter). Net trading balance is `B=E*P-Cin-a`. For the proposed 80%-allocated, 25x, 1%-move BTC pair:

```text
margin per leg = 0.4B; N = 10B
L = 0.1B; W = 0.0863839783842B
Q = 9.8B PAPER
pair cost = 0.0136160216158B
all-in $/PAPER = 0.001389389961 + (Cin+a+Cout-received rebate)/(9.8B)
```

For 0.1, 1, and 10 ETH, substitute `B=0.1P-Cin-a`, `P-Cin-a`, and `10P-Cin-a`. This is the usable estimate with live quotes. **No truthful fixed expected dollar cost is possible without the quote, recovery assumption and realized move.** No price forecast or fake live ETH quote is supplied.

For scale illustration only, set **scenario** `P=$3,000/ETH`, inbound external costs $5, activation $1 and return external costs $5. These are hypothetical sensitivity inputs, not observed costs or requester-specific deployment values. One completed cycle, no rebates, funded queue, no application fee:

| ETH deposit | Gross USDC at scenario price | Trading balance B | PAPER | Pair loss | All-in $/PAPER |
|---:|---:|---:|---:|---:|---:|
| 0.1 | $300 | $294 | 2,881.2 | $4.0031 | 0.005207 |
| 1 | $3,000 | $2,994 | 29,341.2 | $40.7664 | 0.001764 |
| 10 | $30,000 | $29,994 | 293,941.2 | $408.3990 | 0.001427 |

The smaller deposit suffers most from fixed bridge costs. Every extra $10 of external cost, holding Q fixed, adds approximately $0.003471, $0.000341 and $0.000034/PAPER respectively. Multiple cycles can amortize the route cost, but repeat losses shrink B and each cycle adds risk; do not multiply first-cycle emissions indefinitely. A holder starting and finishing in HyperCore USDC avoids most external routing costs.

**B pooled comparison at the same exposure:** the trading curve is size-independent, so pooling itself offers no PAPER price advantage. Write `B_i=E_i*P-Cin_i-allocated activation` and use the same formula, then add allocated vault gas, audit/operating fees and return costs. A single pooled account can amortize activation and outbound batch costs; deposits still need origin routing. With no pooling savings or extra fees, the illustrative A table is also the B baseline. Since pool size, batch count and management fees are unspecified, there is no defensible separate fixed pooled quote. Each $1/holder of net savings lowers cost by `1/Q_i`; each $1 extra expense raises it likewise. Any wrapper fee must be disclosed, not assumed zero in a production quote.

**C builder comparison:** holders executing the same guided pair have A's costs. Builder revenue mints **zero additional PAPER**, so a standalone builder $/PAPER is undefined. An activated Pepe's later ETH reward can offset their total economic cost, but only by the amount actually received; there is no fixed discount attributable to a 0.1, 1 or 10 ETH deposit because reward weights and originating volume differ.

### B. Pooled vault: possible architecture, unresolved hard dependencies

A smart contract can implement [ERC-1271 signature validation](https://eips.ethereum.org/EIPS/eip-1271), but that does not make a verifier call it. If Papertrade uses only ECDSA recovery equal to the account address for wallet intents, a vault cannot sign as itself. An EOA keeper does not solve this: registering its session key must first be authorized by the **vault account**, and staking/withdrawal still need account-level authorization. The Papertrade docs do not say whether EIP-1271 is supported. No source or bytecode was available to settle it.

The follow-up must verify EIP-1271 in session registration, staking, claim, withdrawal and any direct wallet intent; registration acceptance by the relayer; CREATE2 proxy derivation for a contract user; contract HyperCore account activation; CoreWriter withdrawal/bridging; and whether direct contract calls are supported after gates change. A contract-origin caller and a contract-signature account are distinct capabilities. A successful EOA deposit is not a valid vault compatibility test.

**Conditional build design:** an Ethereum ingress router accepts the holder's ETH with a receipt identifier and minimum USDC output, swaps to USDC, then CCTP delivers to a HyperEVM vault. Shares are minted only after destination receipt and credit reconciliation, not from an unauthenticated browser message. The vault owns one Papertrade account, uses a budget-constrained trading signer/keeper, holds and stakes PAPER, and keeps a reserve. An asynchronous withdrawal request claims a pro-rata share of available USDC after settlement; a funded bridge request returns USDC to Ethereum, optionally swaps to ETH and pays the receipt owner. Contracts needed: ingress/receipt router, vault and shares/accounting, signature validator and trading policy, bridge adapter, asynchronous redemption escrow, and optionally a separately audited reward distributor. Protocol contract addresses remain required configuration, not guessed placeholders.

**PAPER restriction:** vault-earned PAPER remains in the vault's own account/staking balance. A vault cannot allocate actual PAPER transfers to depositors at launch. A share represents an economic interest in cashflow and locked PAPER, not a redeemable PAPER unit. Deposit/exit valuation must not let an exiting investor take all liquid USDC while leaving illiquid PAPER/queue losses to remaining holders. Prefer closed cohorts or explicit segregated illiquid claims and asynchronous redemptions; generic instant ERC-4626 redemption assumptions are unsafe here. A permission to transfer vault shares also must not be presumed acceptable to Papertrade's launch policy. [PAPER transfer restriction](https://docs.papertrade.xyz/#/paper/overview).

Paying investor assets “to activated Pepes” is not interchangeable with pro-rata redemption. Use pro-rata capital accounts for depositor principal and their agreed returns. A separate, explicitly disclosed operator-fee or builder-revenue stream can fund Pepe rewards. Do not divert depositor principal to non-depositing holders. An EOA acting as pooled account owner would give its key direct withdrawal control: that is a custodial manager, not a non-custodial vault.

### C. Builder codes and the supplied OGDistributor

**Documented:** builder codes are planned, not live, with no firm date, no registration ABI, no tagging schema and no claim API. The docs describe **1% of the LP-revenue carve**, without an additional user fee. Do not interpret this as 1% of deposited ETH or notional volume; a mirrored launch post uses different frontend-fee wording. Let `Religible` be the eventual contract-defined base: builder revenue would be `0.01*Religible`, subject to final settlement rules. [Builder codes](https://docs.papertrade.xyz/#/how/builder-codes).

**Source-verified on Ethereum chain 1:** Sourcify returns a creation/runtime match for **OGDistributor `0xd450ea80aec46b8bffdf0c4f44d3964489b613f2`**, deployed at Ethereum block **26,147,432** (metadata, not a current balance snapshot). Its immutable hook is `0x22fded8abce0d93979ebb2a04cfc37c110abe0cc`; the matching OGHook source creates this distributor. Collection is `0x999ce0ce8c5f7661e0c74a568ffe27ceb9177bdb`, OG token is `0xce7eb1ad9e2e1c784ea05f7ea4a0fe625923d10a`. [Verified distributor source/ABI](https://sourcify.dev/server/v2/contract/1/0xd450ea80aec46b8bffdf0c4f44d3964489b613f2?fields=all), [verified hook source/ABI](https://sourcify.dev/server/v2/contract/1/0x22fded8abce0d93979ebb2a04cfc37c110abe0cc?fields=all).

The source imposes material constraints:

- `receiveFees(normal,surplus)` accepts native ETH and only the immutable hook; `receiveFeeClaims` and `fundFeeClaims` are hook-only too. No general donation or ERC-20 reward-credit method exists. Plain ETH forwarding has no public receive handler in this distributor, and forcing ETH in would not update reward accounting.
- Activation levels 1/2/3 have weights 1/2/4 and cumulative OG burn costs 50,000/150,000/400,000 tokens. `activateWithETH` buys the required OG through its specified pool and burns it, with price/deadline controls; **it does not farm PAPER**.
- Normal fees are credited by weight; surplus enters a 30-day stream. When no weight is active, amounts backlog until activation. No standalone claim method appears in this implementation. `exit(id)` after a 24-hour activation lock pays accrued ETH **and moves the NFT to OGAuction**. A holder must not be told this is an ordinary harmless reward claim.

**Can builder revenue use this exact distributor?** Not by simply setting it as recipient or by a new adapter calling `receiveFees`: the immutable sender check rejects that. The immutable OGHook also has no external donation-forwarding method; its native-ETH receive only accepts PoolManager. A normal OG swap through that hook does generate legitimate distributor fees: after launch decay, the hook's gross-ETH fee is 3.5%, split 2.5% normal holder rewards and 1% team; its pool additionally uses the 12,500 fee tier. During the first hour, buy fees decay from 50% toward 3.5%, with surplus streamed. These facts come from the inspected source, not from a swap quote. [OGHook source](https://sourcify.dev/server/v2/contract/1/0x22fded8abce0d93979ebb2a04cfc37c110abe0cc?fields=all).

Thus a revenue-funded OG purchase can direct **the fee slice** through this exact OGDistributor, but cannot efficiently distribute all builder proceeds, and changes assets into OG. Cycling trades only to create fees adds spread, price impact, LP fees and team leakage. It is not recommended as the main holder payout route.

**Recommended future route:** builder USDC receiver on the actual payout ledger → claim/withdraw → supported USDC bridge to Ethereum → optional USDC/ETH swap → a **new** `PaperHolderRewards` contract with public funding, explicit snapshot epochs, non-replayable claims and no NFT exit requirement. Use OGDistributor's real `level`, `weight`, and collection ownership at a finalized snapshot to assign activated-Pepe weights. A proposed epoch model fixes entitled addresses at the snapshot, handles later NFT transfers explicitly, and prevents duplicate claims. If using Merkle roots, publish inputs and disclose the root publisher's trust; keep earned funds separate from trader deposits. This references the existing distributor for eligibility but **does not pay through it**. If “through that exact address” is mandatory, only the verified hook fee route is presently demonstrated; a full-value direct route is incompatible with the inspected immutable interfaces.

Revenue example: if final eligible carve were $10,000, builder revenue would be $100 before bridge/swap/claim costs. With 100 activated weight units and a holder of weight 4, that epoch's gross entitlement would be $4, not 4% of trading deposits. These are scenarios, not projected revenues. No PAPER needs to transfer for this cash distribution.

## 4. Follow-up build specification and release criteria

Build A first with a thin read-only backend and a holder-owned browser execution client. The following is an actionable specification, not authorization to trade in this research job.

**Modules:** wallet/eligibility; authenticated protocol configuration; exact fixed-point pricing and mint preview; quote/deposit tracker; browser signing; relayer adapter; persistent public intent/position status store; hedge state machine; queue/reward dashboard; wallet-controlled withdrawal. A state record contains chain/account, official configuration version, deposit transaction/message IDs, position IDs, actual quantities/entries, intent IDs/nonces/deadlines and current phase. It never contains a private key.

**State machine:** `eligible → quoted → depositPending → credited → sessionAuthorized → opening → paired → closingLoser → closingWinner → settledOrQueued → stakeAwaitingWallet → staked`. Partial fills enter `repairRequired`; rejected signatures return to a safe waiting phase. Reloads reconcile authoritative status before signing anything new. An uncertain submission is queried, not resent with a fresh nonce. A stale quote expires before funds move. Browser shutdown means no ongoing browser automation; disclose this and restore monitoring on return. Reliable unattended execution would need separately approved signing infrastructure or supported protocol conditional intents, not a hidden server key.

**Execution policy:** proposed default 25x, 1% move, 80% margin allocation, one pair at a time. Enforce the smaller of real onchain limits and holder-authorized budgets. Refuse new opens if deployed params cannot be fetched, queue risk exceeds the holder's limit, available funds are insufficient, session validity is too short, either side lacks OI headroom, or close latency breaches the tested margin safety envelope. Adjust quantity matching from receipts. Display close-order mode and recovery assumption. Stake requires an explicit wallet action. Never automatically reuse queue debt, increase leverage after losses or promise atomic two-leg execution.

**Required evidence before money flows:**

1. Official addresses and verified implementation/ABI, proxy administrator and live settings, independently tied to the canonical domain. Record chain 999 and block hash. Inspect mint branching/rounding, bust formula, wallet validation and batch failure semantics.
2. Official relayer access, schemas and terms allowing our frontend and intended paired strategy. Demonstrate EOA session registration, proxy tracking, open/close/cancel/status, staking and direct recovery path. Resolve the launch frontend-only conflict. Missing API access means disabled execution, not trial-and-error bypass.
3. Rehearsed end-to-end route in an authorized test environment or read-only fork with HyperCore behavior modeled accurately: Ethereum swap → CCTP → Core credit → PAPER mint → wallet-signed stake → claim → Core withdrawal → Ethereum return. Publish all quoted costs. A local EVM mock alone cannot prove CoreWriter settlement or relayer admission.
4. Failure cases: one-leg rejection, delayed second fill, market retirement, queue activation between closes, duplicate/replayed/expired intents, wallet rejection, key revocation, bridge delay, overlapping deposits, sweeper reconciliation, zero stakers, tail transition and no token transfers. Test no false “withdrawable” label for queue claims.
5. Security review of key handling, origin isolation, dependency supply chain, transaction target verification and withdrawal destination. No application admin may redirect holder funds. User-visible emergency instructions cover direct withdrawal and session revocation, including HYPE gas.

**Deliverable acceptance for that build:** a holder can use their own wallet to fund a verified account from ETH, open and monitor a pair, handle partial execution, close, sign a stake, see claims and return available proceeds, with no custodial key. Testnet receipts and a published integration checklist must establish this. Research does not certify it today. For the vault, add contract-account EIP-1271 and bridge compatibility, asynchronous NAV accounting and an independent audit before any pooled funds.

## 5. Risks that change the answer

| Risk | Practical consequence | Mitigation / remaining limitation |
|---|---|---|
| Queue while LP is near zero | Winner is debt while loser spends real cash; wait can be indefinite | Prefer funded empty queue; quote cash-at-risk and discounted recovery, not just nominal net cost |
| Upgradeable proxies / owner | Owner can tune fees, change relayers, reconcile credits and replace implementations; practical powers exceed the initial code | Inspect admin/timelock/multisig when published; no such governance assurance verified |
| BBO manipulation | Uncrossed nonzero manipulated quotes can pass and damage traders/LP | Monitor, size conservatively; deadband and impact do not prove safety; no manipulation strategy proposed |
| Non-transferable PAPER | No ordinary sale, bridge or payout of minted tokens to another owner at launch | Value as uncertain future cashflow; guided accounts retain own tokens; vault claims must be explicit |
| Relayer and launch gating | Delay, censorship, reordered legs, unavailable closes/stakes; no guaranteed atomic hedge | Authorized API, receipt-based state machine, direct available-balance withdrawal; direct withdrawal does not close positions |
| Hard-bust / path dependence | One side loses full margin before linear zero equity; reversal can kill the other | Avoid 1000x default, use actual bust values and tested latency budget |
| Session compromise / custody | Trade key can destroy holder balances; pooled manager may withdraw if it owns account | Browser key isolation; no server key; a pooled EOA is custodial |
| Bridge / sweeper | Wrong token/ledger/proxy strands money; overlapping credit may require owner help | Authenticated routes, serialized deposit reconciliation, minimum-output and fee limits |
| Emission/stake dilution | Rates and stake shares decline; self-rebate forecasts overstate returns | Read current curve, actual distribution shares and rewards; no fixed APY |
| Anti-sybil / wash rules | Farming may be restricted by relayer policy despite contract arithmetic | No specific published rules were found; absence is not permission. Obtain confirmation; no identity splitting or access evasion |
| OG payout mismatch | Supplied distributor is hook-only; its reward exit auctions the NFT | New reward distributor or explicitly limited hook-fee route; do not send funds blindly |

The owner can upgrade proxied implementations; the pause guardian can permanently retire an instrument and freeze its closing BBO, while a global opens gate does not freeze prices. The keeper changes OI caps and minimums. These are documented powers, not guesses about an unknown multisig. [Admin powers and manipulation](https://docs.papertrade.xyz/#/how/risk), [retirement pricing](https://docs.papertrade.xyz/#/how/pricing-bbo).

## 6. Live state and reproducibility

A read-only call to the [official HyperEVM RPC](https://rpc.hyperliquid.xyz/evm) returned block **48,003,987**, hex `0x2dc7b93`. `eth_getBlockByNumber` gave timestamp **2026-10-08 15:34:01 UTC**, hash `0x452cdc4eff84f7177af92dfe855a94f684d6ed96788b8ac16b7831351ef23f93`. This establishes a chain reference, **not a Papertrade state snapshot**. The [official onboarding page](https://hyperliquid.gitbook.io/hyperliquid-docs/onboarding/how-to-use-the-hyperevm) identifies that RPC and chain ID.

| Requested value | Verified live result at that block | Reason |
|---|---|---|
| tracked LP | **Unavailable, not zero** | PaperTokenomics/Exchange addresses TBA |
| Queue entry count / total queued USDC | **Unavailable, not zero** | Exchange address and ABI TBA |
| PAPER total supply | **Unavailable, not zero** | PaperToken address TBA; zero is a documented launch initial condition only |
| Total PAPER staked | **Unavailable, not zero** | PaperStaking address and getter ABI TBA |
| Tail progress, fees, minima, OI caps, admin | **Unavailable** | No authenticated deployment to inspect |

All eight contracts on the official address page remained TBA. Site JavaScript contained no 40-byte hexadecimal contract addresses. Search hits for namesake Ethereum/Solana tokens were not accepted as the HyperEVM deployment. A genuine future snapshot must pin every `eth_call` to the same block, use verified ABI methods, distinguish queue entries from USDC debt, record token decimals and implementation/admin addresses, and attach raw results. Do not guess getter selectors for contracts not yet identified. [Address registry](https://docs.papertrade.xyz/#/dev/contract-addresses).

**Other source provenance:** OGDistributor Sourcify response SHA-256 `28f93903e9582549b0c080c75ce1164bf72e755a74ea6e9570a5f732a323fbd2`; OGHook response `d592d01bff2df7960b01d15bb7fc1d011c4dd9fd4a7cbc30ddab0505bf4f75c5`. Sourcify reported verified creation and runtime matches for the distributor, verified at `2026-10-08T11:55:03Z`. Its deployment block is Ethereum's, not the HyperEVM block above. Full JSON hashes reflect the retrieved responses; APIs can subsequently add metadata. Explorer access to the supplied address was blocked, so verified source was retrieved through Sourcify v2 instead.

**Local verification:** `python3 artifacts/calculations.py` regenerates all four tables using only the Python standard library. Checks cover deadband zero payout, scale invariance across notionals, BTC/ETH ordering, queue-basis scaling and the 1% worked result. These validate the report's floating-point arithmetic, not unknown deployed Solidity rounding or operational integration. Documents were checked for required sections, table insertion and identical report aliases. No independent reviewer or behavioral certification was used.

### Documentation coverage: every navigation page

| Group | Pages read |
|---|---|
| Introduction | [What is Papertrade](https://docs.papertrade.xyz/#/intro/what-is-papertrade); [FAQ](https://docs.papertrade.xyz/#/intro/faq); [Quick start](https://docs.papertrade.xyz/#/intro/quick-start) |
| How it works | [Trades/pricing](https://docs.papertrade.xyz/#/learn/trades-pricing); [Wins/losses](https://docs.papertrade.xyz/#/learn/wins-losses); [Liquidations](https://docs.papertrade.xyz/#/learn/liquidations); [LP/queue](https://docs.papertrade.xyz/#/learn/lp-queue); [Emissions](https://docs.papertrade.xyz/#/learn/paper-emissions); [Dividends](https://docs.papertrade.xyz/#/learn/staking-dividends); [Deposits/withdrawals](https://docs.papertrade.xyz/#/learn/deposits-withdrawals); [Session keys](https://docs.papertrade.xyz/#/learn/session-keys) |
| Technical | [Architecture](https://docs.papertrade.xyz/#/how/architecture); [BBO](https://docs.papertrade.xyz/#/how/pricing-bbo); [Impact](https://docs.papertrade.xyz/#/how/asymmetric-impact); [Solvency/queue](https://docs.papertrade.xyz/#/how/solvency-queue); [Mint curve](https://docs.papertrade.xyz/#/how/mint-curve); [CREATE2 deposits](https://docs.papertrade.xyz/#/how/deposits); [Builder codes](https://docs.papertrade.xyz/#/how/builder-codes); [Risk](https://docs.papertrade.xyz/#/how/risk) |
| Remaining | [Martingaler LP](https://docs.papertrade.xyz/#/martingaler/overview); [PAPER overview](https://docs.papertrade.xyz/#/paper/overview); [Staking/claims](https://docs.papertrade.xyz/#/paper/staking); [Contract addresses](https://docs.papertrade.xyz/#/dev/contract-addresses) |

### Unanswered questions that must not be hidden

Official deployment/ABIs and exact minima; public relayer credentials/access and launch restrictions; paired-trading policy; EIP-1271 across all account actions; atomicity/cancel semantics; mint integration and post-tail below-threshold behavior; bridge contracts/route quotes; actual LP/queue/supply/stake and admin governance; final builder revenue base and claim ledger. These do not require inventing requester-owned keys or recipients to complete a research report, but they block a claim of production readiness.

## One-screen TL;DR

- **Best modeled strategy:** equal-notional **BTC long + short**, modest leverage, voluntary close after a meaningful move. Start the build with 25x / 1% target, not 1000x liquidation farming. Prefer a funded, empty payout queue during the initial flat-rate window.
- **Cost:** approximately **$0.001389/PAPER at 1%**, **$0.001267 at 3%**, versus **$0.004009 at 0.05%**, before bridges/rebates and assuming full winner recovery. At 1% with no winner recovery the solvent model costs **$0.010204/PAPER**. No launch market price or guaranteed profit exists.
- **Holder solution:** build the **holder-owned guided frontend first**: ETH→USDC→registered Core deposit proxy, browser trade key, paired-intent state machine, real-wallet stake/claim/withdrawal. Contract addresses are TBA and relayer API access is unverified, so execution must remain disabled until proven. Pooled vault compatibility is unresolved.
- **Swarm/OG revenue:** builder codes are future, not current income. The supplied OGDistributor only accepts reward credit from its hook; direct builder donations do not work. Prefer a separate activated-Pepe rewards contract. Existing `exit` auctions the NFT.
- **Top three risks:** **(1)** queued wins can remain unpaid, **(2)** relayer delays and hard liquidation can break the hedge, **(3)** upgrade/admin and BBO-oracle exposure can change or impair settlement. PAPER's launch non-transferability makes all three harder to exit.
