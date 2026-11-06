# ETH perps plus PAPER: buy-side research decision

**As of 6 November 2026, approximately 05:54–06:10 UTC. Recommendation: preserve cash, observe, and stake already-owned PAPER only if its custody and claim path are acceptable. Do not deliberately manufacture losses. No tested ETH configuration establishes a robust positive expected return on total account economics.** Some directional comparators have positive sample means, especially BTC, but none clears uncertainty and execution stress. This is a research deliverable, not a trading deployment. `strategy.json` hard-disables execution; recurring IMD reviews can update bounded shadow parameters and evidence, but cannot enable transactions in this version.

A $1 liquidation loss currently creates about **10.18 PAPER**, not $1 of redeemable value. Our explicitly judgmental dividend model values its next 90 days of distributions at **$0.0205 mean, $0 p10, $0.0170 median and $0.0421 p90**. A same-entry 20× long/short pair closed on its first bust needs **$0.132 per dollar lost** merely to recover trading friction. A managed close just before bust needs approximately **$0.126 per dollar of effective mint basis**. Neither clears that hurdle at recent dividend rates. Future PAPER sale proceeds are assigned zero: launch tokens cannot be transferred, and no transfer-enablement date or market price is assumed.

**Evidence labels:** **Observed** means a saved primary API/RPC response, not an audit; **documented** means current official documentation; **derived** means our arithmetic; **scenario/design** means assumptions or proposed rules; **unknown** means evidence was not obtained. Quantiles of scenarios are not calibrated probability forecasts. Negative or inconclusive results are retained.

## 1. What was verified, and what was not

The [protocol summary](https://exchange.papertrade.xyz/query/protocol/summary), observed at source block **50,515,757**, reported:

| Metric | Observed value |
|---|---:|
| TVL | $24,387,352.34 |
| Locked margin | $3,121,722.34 |
| LP | $4,994,092.84 |
| Payout queue | $0 |
| Open positions | 1,016 |
| Lifetime volume | $1.54045 trillion |
| PAPER supply | 9,248,373,226.96 |
| PAPER staked | 9,183,730,026.73; 99.301% of supply |
| Global reward accumulator, normalized | $0.01474282943 per PAPER |
| `rebateC36 / 1e36` | 1.10100176626 × 10⁻⁹ per effective USD |

All monetary API integers above use 18-decimal accounting units. This does not assert the collateral ERC-20 has 18 decimals. TVL, LP cash, tracked LP, unpaid debt and the staking reward reserve are different quantities. Lifetime volume is turnover, not organic revenue or liquid backing. The API's `fees.lifetime` is approximately $65.0M and matches the historical staking-reward series; it is **not** used as a win-fee-only revenue estimate.

The [address register](https://docs.papertrade.xyz/dev/contract-addresses/) identifies chain **999**, PAPER `0xe40f17915DAa230324030003A197cdAEf2261C0e`, staking `0xAAd6c7b0CC3014FC80FfEDAe0Ed7Ce5967b0F016`, Exchange `0x6cd5661646289FB6E65EA5C032310fDEd797D0a2`, and tokenomics `0x75174549dbBD44497D31a47E2E2D7406408d63D9`. Current `totalSupply()` and `totalStaked()` RPC reads agree with the summary. The documented governance is a 24-hour timelock controlled by a 2-of-3 multisig; this was not independently audited onchain.

**Important correction to the brief:** dividends are not funded exclusively by winning closes. [Staking Dividends](https://docs.papertrade.xyz/learn/staking-dividends/) describes half of the 2% fees on wins **and LP-side fees on losses/liquidations**, plus sweepable tracked-LP surplus above $5M. Loss-side fees come out of the LP's receipt, not an additional trader debit. Debt-funded liquidations are exempt. Distribution depends on an empty queue and sufficient backing. Thus even accurately forecasting win fees alone would understate some revenues, while applying the fee to notional would grossly overstate them.

**Concurrent opposite positions are possible.** Beyond isolated-position documentation, saved [trade history for public account `0xa7c49e836c4ba1982f02d4c20319260baff8af8f`](https://exchange.papertrade.xyz/query/accounts/0xa7c49e836c4ba1982f02d4c20319260baff8af8f/trades?filter=all&limit=75) includes opposite-side, same-market positions **1552069 and 1579171** whose holding intervals overlap. The two close receipts are `0x4879fbbe6c2ea0b3e20388ae300fd1be2d92b88843eefaff7ec9e772b285152d` and `0x77432fd6eaa30d13792bc2871056177cfda5af486c476fd661fe95d19550b5b1`.

The attached [papertradeResearch](https://api.imd.fun/artifacts/6e8652275deb7261fcc223d0cbcb13342ab70f0f84d1a3063dff85857a9af858) was read and is preserved in `research/data/reference-papertrade-research.md`. Its documented equations were independently recomputed. [Prior research](https://api.imd.fun/artifacts/81acf7737c587e44372da89b2bdcaec4055a56c63d7300938e8e5bc77524f7ee) and its [structured results](https://api.imd.fun/artifacts/1a8c2558532925032d1575a28382d71aa8540e0760830ab341d33e0ce2e08681) are background, not extra independent trades in our tests. Their best 100× SuperTrend mean of +0.009R had a confidence interval spanning zero and failed small execution stress.

### Historical evidence quality

The supplied RPC rejected log ranges above 1,000 blocks and rate-limited a broad scan. More seriously, requests for `totalSupply()` at **block 1**, a pre-deployment block, returned the same positive value as today. Historical accumulator and stake calls also returned today's state. **Those calls cannot support historical measurements and were excluded.** This is a reproducible inconsistency, not proof about its underlying cause.

We instead obtained actual logs through another public HyperEVM RPC, `https://rpc.hypurrscan.io`, checked event blocks against requested ranges, and cross-checked current values. Thirty of 32 daily 1,000-block sample requests succeeded: **138 distribution events and 8,726 mint Transfer events** were decoded. Two requests failed (`invalid block range`; response >1MiB); samples are not a complete event census. `keccak256("Distributed(uint256,uint256,uint256,uint256)")` matches topic `0xf7576d8c2653e9d07af5ef229acf59b339e327d4e0eaddb4a96615534cf148f8`. Its fourth data word, divided by 10²⁷, matches the current accumulator and advances monotonically in these samples. Other event-word meanings are not assumed from an unverified ABI.

For exact weekly comparisons we located UTC boundary blocks by timestamp and fetched the preceding 6,000 blocks of distribution logs. This produces these boundary accumulators:

| Boundary UTC | Last block before boundary | Accumulator USDC/PAPER |
|---|---:|---:|
| 23 Oct 00:00 | 49,264,541 | 0.01398443349546 |
| 30 Oct 00:00 | 49,879,366 | 0.01449278017603 |
| 6 Nov 00:00 | 50,494,189 | 0.01473372456402 |

Boundary events are before their cutoffs, not after. The last endpoint distribution receipt is [0x0016b98bd536839cf970b24a6905337a771a5d69be611a3b654667c3027ef259](https://hyperevmscan.io/tx/0x0016b98bd536839cf970b24a6905337a771a5d69be611a3b654667c3027ef259). Raw requests and responses are in `research/data/anchor_rpc_requests.json`; sampled logs and derived results are also shipped. These are RPC observations, not independently certified receipts or a full contract-source audit. Explorer implementation pages returned unverified source.

## 2. PAPER economics

### Issuance per dollar of loss

The [mint curve](https://docs.papertrade.xyz/how/mint-curve/) defines `K = S × expm1(c × G_eff)`. Normal solvent no-builder losing closes use **0.98 × raw loss** as basis; liquidations use the **entire lost margin**. Queue-active cash losses have full basis. For the part refilling negative tracked LP, the multiplier is `1 + 4u(2−u)`, with `u = min(1, underwaterSeconds/259200)`; only that deficit-refilling part receives the bonus. There is no current bonus in our positive-LP snapshot. `c` is fixed after activation in this implementation, but an implementation upgrade remains a risk.

At current supply, the marginal rates are **10.18248 PAPER per effective basis dollar**, **9.97883 per dollar of normal solvent close loss**, and **10.18248 per dollar liquidated**. For a finite loss use the exponential, not the marginal approximation. An effective $1M loss would mint approximately 10.188M PAPER and dilute existing holders; new tokens are not a stable dollar claim.

Selected-wallet API evidence, deduplicated by receipt and position ID:

| Date UTC | Branch | Observations | PAPER / raw loss dollar, loss-weighted | Basis / raw loss |
|---|---|---:|---:|---:|
| 12 Oct | Close, older contract set | 1 | 26.8033 | 0.98 |
| 16 Oct | Close, older set | 5 | 12.6055 | 0.98 |
| 22 Oct | Close, set 2 | 3 | 9.6462 | 0.98 |
| 24 Oct | Liquidation | 1 | 9.8756 | 1.00 |
| 29 Oct | Liquidation | 2 | 10.0139 | 1.00 |
| 2 Nov | Close | 8 | 9.8859 | 0.98 |
| 5 Nov | Close | 62 | 9.9641 | 0.98 |
| 5 Nov | Liquidation | 4 | 10.1549 | 1.00 |
| 6 Nov, partial day | Close | 42 | 9.9777 | 0.98 |

Sources are the saved public-account trade endpoints listed in the manifest, including [the small account](https://exchange.papertrade.xyz/query/accounts/0xc6c6f0dbef8706085ef363e70bfd4749c4cd664a/trades?filter=all&limit=75) and [another sampled trader](https://exchange.papertrade.xyz/query/accounts/0xd76232f7b8b9b789bdf03bcb6a9258656a990922/trades?filter=all&limit=75). This is a convenience sample from recent mints and leaderboards, not an unbiased account sample. API close histories are capped; we do not claim complete lifetime losses. The old declining issuance schedule must not be fitted with today's increasing-supply formula: [contract set 2 changed the mint rule on 21 October](https://docs.papertrade.xyz/dev/protocol-changes/). A wallet's cumulative 17 PAPER/$ or a large staker's lifetime $261,855 of rewards is therefore not today's marginal mint rate or an investment APY.

### Dividends per PAPER and their trend

From event accumulator differences, one continuously staked PAPER earned:

| Measurement window | USDC/PAPER/day |
|---|---:|
| 23–30 Oct, exact UTC boundaries | **0.00007262095** |
| 30 Oct–6 Nov, exact UTC boundaries | **0.00003442063** |
| Change between those weeks | **−52.60%** |
| Sampled 22 Oct–6 Nov, 14.757 days | 0.00005917038 |

Independent [daily protocol history](https://exchange.papertrade.xyz/query/protocol/history?interval=1d) gives revenue divided by each day's ending staked supply of 0.00007252981 and 0.00003434384 for the same completed weeks, close to the event result. This ending-stake method is approximate during intraday staking changes; event accumulator differences are preferred. Completed 22 Oct–5 Nov daily revenue was **$7.827M / 15 days**, about **$521,803/day**; last seven days were **$2.194M**, about **$313,362/day**. Median last-seven daily yield was only **0.000009439/PAPER/day**: payments are lumpy. Excluding bootstrap, the 26 completed days 11 Oct–5 Nov average approximately 0.000203494/day using end-stake denominators, strongly above recent rates.

**30-day request:** the daily API covers the launch period and shows zero rewards/supply through 9 October, followed by a **$23.975M** bootstrap-era revenue day on 10 October. The 7 Oct–6 Nov 30-calendar-day accumulator increment is approximately **0.014733725 USDC/PAPER**, or **0.000491124/day**, using a zero pre-reward accumulator anchor inferred from the daily zero-reward/zero-supply records. That start anchor is not a successful archive-state read. It is a protocol accumulator statistic, not a yield that a newly minted token could actually have earned throughout that window. Late minters could not capture distributions before their stake existed. Bootstrap concentration makes this unsuitable for forecasting.

**90-day request: unavailable, not zero.** The documented production launch was 7 October local/date convention; summary genesis is **6 Oct 22:42 UTC**. Ninety days of protocol economics do not exist. A zero-padded 90-day “APY” would misrepresent an inactive pre-launch system. Current-rule history is only approximately 16 days. We do not fabricate 90-day dividends, loss rates, liquidation maps or queue observations.

### Queue-empty uptime

[House history](https://exchange.papertrade.xyz/query/house/history?interval=1d) reports **30/30 daily snapshots empty**, the [hourly history](https://exchange.papertrade.xyz/query/house/history?interval=1h) **168/168 empty**, and the [minute history](https://exchange.papertrade.xyz/query/house/history?interval=1m) **1,440/1,440 empty**, all without declared gaps. The current [queue summary](https://exchange.papertrade.xyz/query/protocol/queue-summary) is empty. Thus **sampled empty uptime is 100% at all three resolutions**. True time-weighted uptime, especially sub-minute queues and older intraday outages, is unknown; correlated snapshots cannot justify a binomial confidence interval. Distribution gaps also need not mean a queue: no eligible revenue or keeper delay can cause them. Do not multiply historical realized dividends by another assumed historical uptime factor; that would double-discount them.

### Forward dividend value and payback

For loss basis settled now, new stake `K` earns `V_H = Σ[D_t × K/(T_t + K)]`, where `T_t` is other staked PAPER. Normal close loss has 0.98 basis per dollar; liquidation has 1. Tokens have **zero terminal cash value** here. This measures dividends, before subtracting the loss itself. Inflation of PAPER supply is dilution, not USDC income.

**Scenario distribution:** 12,000 paths, seed 20261106. Joint three-day circular blocks resample the seven completed daily **USDC revenues and corresponding supply log growth** from 30 Oct–5 Nov. Start at today's staked supply, hold its fraction of circulating supply constant, and dilute by resampled growth. Four deliberately judgmental regimes: **20% permanent revenue collapse; 40% revenue half-life 45 days; 30% constant recent revenue; 10% twice recent revenue**. These probabilities are stress weights, not fitted estimates. No additional queue factor is applied to already-realized baseline revenue; collapse/decay represent future demand, queue or parameter failure. No discount rate is charged, favoring the farm.

| Horizon after $1 liquidation loss | Mean dividends | p10 | Median | p90 |
|---|---:|---:|---:|---:|
| 30 days | $0.00829 | $0 | $0.00835 | $0.01435 |
| 90 days | **$0.02051** | **$0** | **$0.01703** | **$0.04214** |
| 180 days | **$0.03349** | **$0** | **$0.02019** | **$0.08409** |
| 730 days | $0.07155 | $0 | $0.02100 | $0.23268 |

Multiply approximately by 0.98 for $1 of normal no-builder solvent close loss. “Effective basis dollar” uses the liquidation row. Insolvency-bonus basis can be higher, but hunting it while dividends are suppressed and claims queue is not an approved strategy. Costs and bonus cannot be mixed between incompatible solvent/insolvent branches. As a deliberately generous conditional upper scenario, a full 5× bonus followed by immediate recovery multiplies the 90-day mean to about $0.1025 and p90 to $0.2107 per cash dollar lost; the 180-day mean would be about $0.1674. Some such recovery scenarios can beat low-leverage farm costs. Today neither negative tracked LP nor a mature insolvency clock was observed, and queued winning claims plus suppressed dividends make assuming immediate recovery unjustified. We do not rule out every future parameter/state configuration; we reject allocating to an unavailable bonus or an unverified recovery.

No path repaid the **entire $1 lost** within 730 days. That is conditional on these assumptions, not a universal impossibility theorem. Under constant recent dollar revenue and daily dilution ~0.219%, the infinite-horizon dividend value is only **$0.159 per liquidation dollar**; under the completed set-2 average with ~0.252% daily dilution it is **$0.230**. Neither has finite full-loss payback. Without any dilution or decay, today's recent rate would take roughly **2,870 days** to repay $1; ignoring dilution is economically material.

A hedge only needs to repay its **net pair cost**, not the losing leg's whole dollar. This distinction is essential. Constant recent revenue and dilution would repay ideal 5×/10×/20× bust-pair friction after about **664/709/815 days after minting**, respectively. Add the time waiting for the first bust and any claim delay. A 100× bust pair never repays even over an infinite horizon in that constant-recent scenario. A sufficiently persistent revenue recovery can make a lower-leverage farm conditionally positive over long horizons; it is not supported at a 30/90/180-day conservative hurdle today.


The same scenario distribution gives these ideal bust-farm payback probabilities, measured **after minting**, excluding the wait to reach the barrier and settlement delays. They are subjective-model CDF values, not observed success frequencies.

| Leverage | Repaid by 90 days | By 180 days | By 730 days |
|---|---:|---:|---:|
| 5× | 0.00% | 0.14% | 35.88% |
| 10× | 0.00% | 0.06% | 28.54% |
| 20× | 0.00% | 0.00% | 12.96% |
| 100× | 0.00% | 0.00% | 10.17% |

Every listed farm has median payback beyond 730 days in this mixture; a conditional constant-revenue payback is not the unconditional median.

## 3. Hedged-pair farm: full account arithmetic

Let each equal-leverage leg have margin `M`, leverage `L`, notional `N=LM`, same entry, and common exit price. For absolute move `p`, let `W(N,p)` be the winning **profit**, not returned principal. Using [documented asymmetric impact](https://docs.papertrade.xyz/how/asymmetric-impact/):

```
q = max(0, p − 0.00002 − holdback(p))
W = N q × 0.9 / (1 + 1/(15000q) + 100000/(1e6 q × positionMultiplier)) × 0.98
ETH positionMultiplier = 483.979; BTC = 814.598
standard holdback = 3.597 width u²(1−u)², band [0.000075,0.0006]
off-hours holdback = 6.085 width u²(1−u)³, band [0.00003,0.001]
```

Outside its band holdback is zero. `u` normalizes the move within that band. The 2% fee follows impact; a builder would reduce retention to 97.5%, so the base case assumes canonical no-builder execution. Losses remain linear until hard bust. These equations are floating-point reconstructions using documented defaults, not exact Solidity rounding or a live execution quote.

Before either bust, the **exact accounting identity conditional on the quoted payout function** is:

`pair cash PnL = W(N,p) − Np; basis = 0.98 Np` in the solvent no-builder close branch.

Raw directional PnL cancels, but discounted wins do not cancel full losses. Unequal leverage with **equal notionals** preserves that negative identity until a bust; it only changes margin requirements and which barrier arrives first. Equal margins with unequal leverage instead create directional exposure `ΔN=N_long−N_short`.

The [liquidation documentation](https://docs.papertrade.xyz/learn/liquidations/) describes full-margin forfeiture at a trigger about 5 bps before zero equity, including voluntary closes executed past that trigger. Approximate bust move is `b≈1/L−0.0005`; actual position `bustPrice` and integer price ticks must replace it operationally. At first bust, with the survivor closed immediately at that price:

`pair cash PnL = W(N,b) − M; minted basis = M; total committed margin = 2M`.

### Ideal one-to-bust versus managed close

| Equal leverage | Approx. move to bust | Winner profit / its M | Bust cost / total 2M | Managed pre-bust cost / 2M | Bust cost / dollar lost |
|---|---:|---:|---:|---:|---:|
| 5× | 19.95% | 0.87850 | 6.075% | 5.950% | $0.12150 |
| 10× | 9.95% | 0.87501 | 6.250% | 6.000% | $0.12499 |
| 20× | 4.95% | 0.86803 | 6.598% | 6.098% | $0.13197 |
| 50× | 1.95% | 0.84718 | 7.641% | 6.391% | $0.15282 |
| 100× | 0.95% | 0.81271 | 9.365% | 6.865% | $0.18729 |
| 200× | 0.45% | 0.74484 | 12.758% | 7.758% | $0.25516 |
| 500× | 0.15% | 0.55095 | 22.453% | 9.953% | $0.44905 |
| 1000× | ~0.05% | 0.23571 | 38.215% | 13.215% | $0.76429 |

Managed columns are the mathematical limit just **before** the approximate barrier; no real execution can rely on reaching that exact price safely. At 1000× the off-hours curve increases bust-pair cost to about **43.41% of total margin**. Small changes in actual buffer/ticks matter greatly there. At low leverage, reaching a 10–20% move can take much longer than one review cycle.

At 100×, deliberate bust destroys an extra **0.05M** relative to a just-before-bust close, increasing effective basis from **0.931M to 1M**. The extra 0.069M basis is worth only about **0.00142M** in our mean 90-day dividends. Extra minting does not justify that extra destruction. The same comparison is even more damaging at very high leverage. At 5× the slight advantage of full liquidation basis in cost-per-basis arithmetic is tiny and does not clear the dividend hurdle either.

A just-before-bust managed 20× pair has cost **0.12197M**, basis **0.9702M**. Mean 90-day dividends are only **0.01990M**, leaving **−0.10207M**, or **−5.10% of total pair margin**. A 20× bust pair leaves **−5.57% of total margin** after mean 90-day dividends; at p90 it still leaves **−4.49%**. The 180-day p90 liquidation-dividend credit is below the 20× farm's break-even requirement too.

**Sensitivity:** with constant recent dilution, an ideal 20× bust farm needs about **$1.457M/day** of sustained protocol distributions for 90-day payback, or **$800k/day** for 180-day payback, versus the recent **$313k/day**. Set-2 historical mean is about $522k/day. These are distribution thresholds, not volume thresholds. For managed closes, divide cost by their smaller basis; reducing leverage cannot remove the roughly 12% large-move payout wedge per loss-basis dollar.

### Exits, timing and alternative constructions

- **Time exits:** simulate closing both after 12 or 24 hours. Low leverage reduces daily losses and mints less. Turnover does not turn a negative cost-per-basis into positive value.
- **Volatility/move exits:** simulate first ±0.25%, ±0.5%, ±1% move or first bust, with a 24-hour timeout. The full grid is shipped. Tiny moves suffer the strongest holdback/impact; wider exits approach the lower large-move wedge but take longer.
- **Unequal leverage:** equal-notional long 10×/short 100× allocates margin 10:1. On a +0.95% move the short loses 0.1 unit and long earns about 0.08127, a cost of 0.01873 across 1.1 margin units. Its cost per high-leverage leg dollar lost is still approximately $0.1873. On the opposite large move the accounting branch differs; there is no uniform improvement.
- **Staggered entries:** a long opened first and a short opened an hour later carry real unhedged exposure during the hour. A favorable entry spread may lock a raw gain, but earning that spread is a timing bet. It is not a free hedge farm. We simulate a first-leg bust before the second entry as a loss and abort the second leg.
- **Keep the survivor:** holding a winner after the loser busts is a one-sided trade. A reversal can bust both isolated legs, losing **100% of total pair margin**. Its expected value needs directional alpha, not just a dividend story.
- **Rebalancing:** [positions cannot be topped up, resized, or partially closed](https://docs.papertrade.xyz/learn/trades-pricing/). Close fully and reopen smaller if needed. Four fills, extra latency and new state replace an imagined partial-close hedge. Splitting a position does not defeat size-independent impact.

A recurring daily swarm alone cannot keep a survivor hedged at a 0.05–0.95% barrier. A separate continuous, receipt-aware guard would be necessary even for a future approved version; it is not supplied or presumed available here.

### Capacity and endogenous rewards

For cumulative basis `G`, new token share of staked supply is `S expm1(cG)/(T+S expm1(cG))`. At today's stake fraction, a **0.1% share** corresponds to roughly **$902,370 of effective loss basis**, before external dilution. This is a cumulative issuance illustration, not an allowed loss budget. Per-dollar issuance rises with supply, while ownership of each already-minted cohort falls; both effects must be represented.

[Risk documentation](https://docs.papertrade.xyz/how/risk/) describes directional OI caps with launch policy targeting **$1B of additional headroom per side**, recalibrated outside a $900M–$1.1B band. That is **not a fixed $1B total OI cap**. Single-position documented notional cap is $10M. Current live side caps/minimum order size were not independently verified; therefore executable capacity is unknown and any live entry must be refused until actual headroom is read. Policy limits own notional to 0.5% of observed side OI and 5% of verified free headroom, with small equity-based limits usually binding first.

Our fees and LP surplus cannot be treated as independent external yield. If our current stake share is α, redistributing one of our own cost dollars returns at most approximately α dollars under a fully distributable branch. At the 0.1% share cap this feedback is negligible. Increasing α does not create system profit; it requires more losses and changes dilution, LP state and other users' returns. The small-account simulations exclude incremental self-funded distribution changes; at their $1 research margin scale this is immaterial. Large-scale extrapolation is invalid.

## 4. Public-candle backtest and directional evidence

### Data, chronology and execution assumptions

We retrieved ETH and BTC from the primary [Hyperliquid info API](https://api.hyperliquid.xyz/info), request type `candleSnapshot`, interval `1h`. The [official API reference](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint) documents these requests. There are **3,744 complete hourly bars per asset**, **3 June–5 November 2026 inclusive, 156 days**, plus the **6 November 00:00 open** used only as a terminal execution price. Timestamp uniqueness, one-hour continuity, OHLC inequalities and positive prices were checked. There are zero missing hours or duplicate timestamps within this downloaded window. Raw responses, request bodies, source timestamps and SHA-256 manifest are included. These are trade candles, not a BBO execution archive.

Initial **60 calendar days** (3 June–1 August) select parameters; the next **96 days** (2 August–5 November) are holdout. Four days warm up lagged signals. Within each asset, **65 base settings** were examined: 16 equal-leverage pairs; 12 move-triggered pairs; 32 directional variants; four tilted pairs; one always-long control. Selection of the directional winner uses only training mean net PnL/calendar day, with at least 20 trades. All settings and results are retained; no claim of an externally preregistered trial is made. The confidence intervals are **1,500 circular seven-calendar-day block resamples**, with idle days retained, not independent-trade normal intervals. They are conditional on this historical sample and do not correct for every model-selection decision.

The candle proxy is deliberately simple: prior 24h and 72h returns must agree; trade their sign for trend, or the opposite for reversion. Enter at the next UTC 00:00 hourly open; at most one daily decision, ATR is the prior 24-hour mean true range, with an hourly ATR/price gate of 0.1–2%. Test leverage 10/20/50/100×, hold 12/24h, with either no managed stop or a 1-ATR stop and 2-ATR target. This is a **proxy test**, not a backtest of unavailable historical swarm judgments or liquidation maps.

Current documented payout curves are applied counterfactually to the whole candle history, including dates before Papertrade launched. Base case uses standard payout weekdays and off-hours weekends; other quiet-hour switching is unknown. Winning gains incur impact, holdback, deadband and 2% fee; losses are full and busts lose all isolated margin. No funding is charged on Papertrade. Gap opens are processed before stops. Directional bars touching both stop and target use stop-first; a bust-first stress is also retained. Execution stress applies 1 or 5 bp adverse drift **per side**, not a fictitious venue notional fee. One-hour delayed entries are separately evaluated.

Pair base cases close the survivor at the first touched bust level and can therefore be **optimistic about continuous monitoring and atomicity**. If both barriers are reachable in an hour, the default chooses an adverse branch; a separate stress loses both legs. At 1000× the holding-time result of zero hours means “inside the entry hour,” not instantaneous riskless execution. Losses and dividends must not be inferred from trade-candle closing direction alone. The time-exit boundary open is available; no favorable forced terminal mark is substituted.

### Holdout trading results, excluding dividends

All means below are **USD/day per $1 total margin budget committed per decision**, with idle days included. Drawdowns use 1% current account equity per group/trade and realized cash PnL, before proposed risk gates. A pair's denominator includes **both** margins.

| Configuration | OOS decisions | Training mean/day | OOS mean/day | 95% block interval for OOS mean/day | Historical account drawdown |
|---|---:|---:|---:|---:|---:|
| ETH equal pair 10×, 24h | 96 | −0.01169 | −0.01112 | [−0.01413, −0.00857] | 1.06% |
| ETH equal pair 20×, 24h | 96 | −0.02439 | −0.02220 | [−0.02719, −0.01733] | 2.11% |
| ETH equal pair 100×, 24h | 96 | −0.08590 | −0.08990 | [−0.09293, −0.08617] | 8.27% |
| ETH equal pair 1000×, 24h | 96 | −0.37052 | −0.39675 | [−0.39784, −0.39567] | 31.73% |
| **ETH training winner: reversion 100×, 12h, no stop** | 63 | +0.19849 | **−0.01793** | [−0.13208, +0.08562] | 7.13% |
| ETH training winner within ≤20×: reversion 20×, 12h | 63 | +0.03997 | **−0.01054** | [−0.03772, +0.01386] | 1.73% |
| ETH trend 20×, 24h, 1-ATR stop | 63 | −0.03649 | +0.00027 | [−0.02588, +0.02731] | 1.39% |
| ETH always-long 20×, 24h control | 96 | +0.01465 | +0.02045 | [−0.07339, +0.14891] | 4.86% |
| **BTC training winner: reversion 50×, 12h, no stop** | 65 | +0.06853 | **+0.02617** | [−0.04114, +0.08423] | 3.04% |
| BTC training winner within ≤20×: reversion 20×, 12h | 65 | +0.03115 | +0.00484 | [−0.03554, +0.03384] | 1.79% |

The ETH selected rule wins **50.8%** of trades and still loses money: this is why win rate is not the objective. At 100×, its mean falls to **−0.04258/day** with 1 bp adverse drift per side and **−0.08621/day** at 5 bp. Its first/second/third 32-day OOS blocks are **+0.09233, +0.04763, −0.19375/day**. BTC's selected 50× mean is **+0.02040/day** at 1 bp and **−0.01554/day** at 5 bp; its blocks are **−0.03442, +0.04881, +0.06412/day**. Neither positive mean is robust evidence of executable alpha. A one-hour delay happens to improve both selected means, illustrating timing sensitivity rather than validating delay optimization.

An equal-notional leverage/timing extension, same 96-day ETH holdout, also loses before dividends:

| Long/short leverage | Second-leg delay | PnL/day per $1 planned total margin |
|---|---:|---:|
| 10× / 20× | simultaneous | −0.01454 |
| 20× / 10× | simultaneous | −0.01509 |
| 10× / 100× | simultaneous | −0.01762 |
| 100× / 10× | simultaneous | −0.01865 |
| 10× / 10× | 1 hour | −0.01031 |
| 20× / 20× | 1 hour | −0.02064 |
| 100× / 100× | 1 hour | −0.08446 |

These extensions use all daily entries without the ATR gate, so differences from the primary grid are not a clean timing-only ablation. Their seven-day block confidence intervals all remain below zero. Full results include move-trigger exits, both-bust stress and the negative tilted-pair results, not merely table winners.

### Combined cash economics and rankings

We also simulate **8,000 90-day account paths per candidate**, seed 831. Historical seven-day blocks jointly resample each candidate's daily cash PnL and effective mint basis; future USDC revenue/supply growth use the same three-day blocks and regime weights as Section 2. New losses accumulate stake over time, its share dilutes, and only distributions earned **within the same 90-day account window** are counted. A new loss on the last day gets no 90-day forward token mark. Supply growth increases newly minted token counts as well as diluting previous cohorts; the implementation works in relative stake shares. Fees carved from LP proceeds are not charged twice. Trading is assumed cash-paid in these base simulations; future queue-activation loss of profit cash is an additional downside outside them.

| Candidate | Mean total USD/day/$margin | p10 | p90 | Economic conclusion |
|---|---:|---:|---:|---|
| Cash / observe | **0** | 0 | 0 | Recommended risk-adjusted choice; external USDC yield excluded |
| BTC reversion 50×, 12h | +0.02729 | −0.01592 | +0.06823 | Highest selected-rule sample mean; outside approved shadow leverage cap and execution-fragile |
| BTC reversion 20×, 12h | +0.00533 | −0.01857 | +0.02716 | Best bounded candidate mean; no positive lower-tail evidence |
| ETH trend 20×, managed 24h | +0.00087 | −0.01752 | +0.01948 | Positive sample mean after dividends, selected descriptively from holdout; training lost |
| ETH reversion 20×, 12h | −0.01028 | −0.02769 | +0.00625 | Training-selected bounded ETH rule fails |
| ETH pair 10×, 24h | −0.01032 | −0.01234 | −0.00840 | Lower farm loss, not positive carry |
| ETH pair 20×, 24h | −0.02063 | −0.02424 | −0.01704 | Dividend credit does not repair pair costs |
| ETH tilted pair 20× | −0.04035 | −0.06149 | −0.01884 | Bias proxy worsens hedge economics |
| ETH pair 100×, 24h | −0.08530 | −0.09022 | −0.07928 | Reject |
| ETH pair 1000×, 24h | −0.39196 | −0.39657 | −0.38704 | Reject decisively |

Here p10/p90 describe a **90-day average daily account outcome distribution**, combining empirical resampling and judgmental dividend regimes. They are neither single-trade return quantiles nor 95% confidence intervals for the true mean. `strategy.json` uses exactly this convention. Its `maxDrawdown` is the historical 1%-allocation metric above, not a prediction or maximum possible loss.

Ranking by sample expected value is not the same as capital allocation: BTC's fragile point estimate cannot dominate cash with confidence. Ranking by downside for the bounded set is cash first, then small protected ETH trend / BTC 20× / ETH 20× reversion (their relative tail ordering depends on stress), then farming 10×, farming 20×, and tilted farming. Directional candidates have wider uncertainty; pairs have more certain negative carry. Keep those two kinds of downside distinct. High-leverage farms rank last. Existing PAPER staking may earn positive incremental cash with no new trading loss, but the existing stake and claim rights belong in the baseline, not as an alpha credit for a new farm.

## 5. Daily bias oracle and conditional directional overlay

This is a proposed management design, **not an empirically validated predictive factor**. Funding on another venue is information about positioning, not Papertrade carry. No historical Papertrade map archive, point-in-time panel answers or complete 24h OI changes were available; their predictive contribution can only be measured prospectively. Current public [Hyperliquid market contexts](https://api.hyperliquid.xyz/info), funding history and [OKX funding](https://www.okx.com/api/v5/public/funding-rate?instId=ETH-USDT-SWAP) were saved as examples. A current OI level is not an OI change.

At daily cutoff, compute the following from evidence known then, clipping each signed component to [−1,1]:

1. **Trend T (50%)**: 0.5 times the clipped 24h log return divided by twice prior 24h realized volatility, plus 0.3 times the 72h return divided by `2√3 × RV24`, plus 0.2 times the 168h return divided by `2√7 × RV24`. RV24 is the square root of the sum of the last 24 closed hourly squared log returns. Reject zero/invalid denominators. This rewards persistent direction without treating a quiet-market tiny return as certain.
2. **Funding F (20%)**: negative of mean funding across Hyperliquid and OKX normalized to an 8h period, divided by **0.0003**, clipped. Use the prior 24h average of known realized rates. Hyperliquid hourly rates are multiplied by eight; divide OKX payment by its actual payment interval then multiply by eight hours. Positive crowded long funding is a contrarian bearish component. Do not use a predicted rate as realized history.
3. **OI O (20%)**: `sign(24h return) × clip(mean venue 24h proportional OI change / 0.10)`. Rising OI confirms direction in this hypothesis; falling OI fades it. Snapshot each venue at exactly matching cutoffs and consistent units; missing yesterday's OI invalidates this component. Do not reconstruct it from today's map or volume.
4. **Papertrade Q (10%)**: `(short exposure above spot − long exposure below spot)/(their sum)` within ±5%, using all 150 buckets and prorating any bucket crossing spot. Exclude outside-range totals from this local score; validate both outside totals separately. If local total is zero, mark Q unavailable. This is a positioning proxy, not a claim that synthetic liquidations create forced Hyperliquid market buys/sells.

For volatility multiplier `v`, rank RV24 against trailing 90 completed daily RV24 observations: **v=0.5 above p90, v=0.75 below p10, otherwise v=1**. Insufficient history or extreme data discontinuity invalidates the answer. Bias is `round(100 v (0.5T+0.2F+0.2O+0.1Q))`, clipped to [−100,100]; rounding ties goes away from zero. No renormalization silently hides missing components. ETH's observed ±5% snapshot reports about **$5.223M long versus $3.314M short bucket exposure**, naive skew **−0.224**. Those are reported exposure units, not verified margin-loss amounts or an actionable prediction. The full score was not manufactured from this single snapshot.

**Exact oracle question** (also in `strategy.json`):

> Using only public evidence timestamped at or before {asOfUtc}, what is the directional pressure on ETH over the next 24 hours on a scale from -100 (strong short) through 0 (neutral) to +100 (strong long)? Apply the fixed trend, funding, open-interest and Papertrade liquidation-map rubric and volatility multiplier in report.md. Report an int256 integer in [-100,100], without units, prose or JSON. Publish the required timestamped evidence packet separately. This score predicts price pressure, not a guaranteed profitable Papertrade trade.

Use at least three independent panel responses; median integer is the candidate answer. **Tolerance is ±10 score points**, not dollars or basis points; require panel max−min ≤20 and reproduced formula within 10. Any required evidence missing, invalid or stale means **INVALID and no entry**, not “neutral 0.” A valid zero means actual neutral evidence. Market snapshots must be at most 60 seconds old at cutoff; panel returns before 01:00 UTC and expires for entries after two hours. Each packet records source URL, timestamp, raw-response hash, formulas, all four components, volatility percentile and disagreement. If BTC is used, ask the same question explicitly replacing ETH and collect BTC evidence; never reuse the ETH integer implicitly.

**Tilt and timing, if a future policy version is ever enabled:**

- `|bias|<20`: no directional overlay. A neutral pair may be shadowed, but may be traded only if its conservative total economics independently clears the farm hurdle; it currently does not.
- `20≤|bias|<70`: equal leverage, `w_long=0.5+maxTiltFraction×bias/100`, `w_short=1−w_long`. Default maximum tilt is 0.10; absolute allowed maximum is 0.25. Unequal sizes intentionally create net delta. Check the net-notional limit after rounding/minimum-order constraints; do not change leverage to obscure the exposure.
- `|bias|≥70`: shadow a one-sided trade in the bias direction, **10–20×**, only at the next confirmed hourly open after the evidence packet. Require the prior 24h/72h candle trend to agree with the oracle for this continuation design. A disagreeing/reversion comparator remains research, not an automatic override. The proposed execution slot is 01:00 UTC; backtested comparators use 00:00 UTC, which is recorded separately in candidate parameters. Refresh the execution BBO, queue and headroom immediately before any order; the daily evidence cutoff and bias packet remain unchanged.
- Reject entry if price moved >1 bp from the approved BBO snapshot, hourly ATR is outside [0.1%,2%], or a 1-ATR stop is closer than four stop distances to actual bust. Use a 2-ATR target and maximum 12h hold by default; full exits only. At a 24h boundary require a fresh oracle, never roll blindly.
- Submit paired legs only with a receipt-aware execution service. If the second leg is not confirmed within two seconds, request a full close of the first and stop. There is no assertion that this latency is attainable. Separate 1–5-second guard heartbeats are a prerequisite, not a property of recurring swarm runs.

These gates seek safer future experiments; their combined performance has **not** been backtested. The protected ETH trend comparator is related but does not include the full panel or every proposed risk gate. Prospective records must include every eligible decision, abstention and failure, not only executed winners. Obtain at least 60 days of live shadow observations and 100 executable opportunities, and positive conservative total-value evidence after basis/latency stress, before proposing a new execution-enabled policy. This is a research gate, not a promise that 100 observations establish significance.

## 6. Portfolio risk and adversarial review

**Sizing design:** cash equity excludes nontransferable PAPER and marks queue claims at zero for new-risk sizing. Count open losses conservatively, with isolated full margin as stress loss. Keep at least **98% free cash** by default, preferably outside protocol custody; future total open margin ≤1% equity, pair margin ≤0.5% equity **combined**, directional margin ≤0.25%, one correlated group at a time. Absolute schema ceilings are 2%, 1%, 0.5% respectively; they cannot be used to bypass the tighter gross/net notional limits. All ETH and BTC exposure belongs to one correlated risk bucket.

For an illustrative $100,000 account, defaults mean $500 combined margin ($250/leg at equal leverage) or $250 one-sided, never $500 on each pair leg. At 20× the pair's total gross notional is $10,000. A both-bust pair loses at most the group's $500 trading margin before counterparty/custody failures; a one-leg loss is not a daily-loss estimate. Hypothetical account size is an illustration, not a supplied owner balance or an executable allocation.

Daily loss stop **1% equity**, trailing seven-day loss stop **3%**, peak-equity drawdown kill **6%**; hard ceilings 2%/5%/8%. Daily threshold resets at 00:00 UTC; weekly uses a rolling seven-day window. Use start-period equity adjusted for external flows, net cash trading PnL plus earned dividends without double counting, and current adverse open-position marks. Receipt and keeper failures may exceed stop levels. No martingale, debt-funded position, margin top-up or partial close. Future dividends receive **zero sizing credit**, even when a forward valuation is displayed.

**Risk of ruin:** historical drawdowns are not ruin estimates. In the 8,000-path 90-day seven-day-block cash-price simulation with **1% equity per trade**, before enforcing any kills, no bounded ≤20× candidate reached a 20% drawdown; the naive binomial “rule of three” would be 0.0375%, but dependence and model misspecification make that unsuitable as a real-world bound. Their simulated p90 drawdowns ranged roughly 1.2–5.8%, highest for the tilted pair. The 100× pair hit 8% drawdown in about 6.0% of paths; the 1000× pair hit 20% in **100%**. For comparison, 96 consecutive full-margin losses at a 1% fractional allocation leave only 0.99^96 ≈38.1% of starting cash, a 61.9% drawdown; the both-bust stress can be much worse than a paired-close backtest. These simulations omit unseen crises, unbounded queue delay and loss of custody. A finite fractional isolated-margin loss does not mathematically bankrupt a continuously resized account, but repeated negative carry can make it uneconomic.

The actual recommended **zero-new-trade allocation has zero trading-model ruin probability**. It does not eliminate USDC, protocol or key/custody risk on assets already held there. Protocol failure can impair 100% of venue-held cash and accrued reward claims, regardless of a 0.5% trading margin limit. No defensible numerical probability of that event is available.

| Failure mode | Economic effect / desk response |
|---|---|
| Queue activates | Profit becomes an unpaid claim while losses are cash; dividends stop or slow. Halt new entries; segregate claim NAV and aging. Do not count a queued gain as earned cash. |
| Dividend collapse or growth in supply | New cohorts earn less; old claims dilute. Revalue at zero revenue and faster issuance; no averaging into a farm to rescue it. |
| Owner upgrade/parameter change | Changes payout or claim economics; docs describe proxy upgrade power and timelock, not permanent guarantees. Halt on material scheduling and compare implementation/config fingerprints. |
| Relayer/keeper outage or legging | The “hedge” can become a naked leg; both legs can bust across a reversal. No entries without confirmed guard and actual exit receipts. |
| BBO distortion, gaps, retirement | Candles are not executable mids; retirement can freeze an instrument's close reference. Require fresh market state and full-close contingency. |
| High LP surplus used as “free yield” | Surplus depends on other traders losing; protocol growth or circular self-generated fees may not persist. Isolate fee share from sweeps when event evidence permits. |
| Claim/withdrawal path failure | Accumulator accrual is not external USDC cash. Track pending, claimed-to-Exchange and externally withdrawn amounts separately. |
| Source inconsistency | Archive RPC state failed sanity checks; docs and frontend deployment data disagree on collateral address. No live deployment until active collateral and implementations are independently resolved. |

The [solvency model](https://docs.papertrade.xyz/how/solvency-queue/) prioritizes queued winners ahead of fees and separates LP cash, side bucket and debt. FIFO ordering is not a finite repayment guarantee if future backing cash does not arrive. Our adverse reviewer rejects any report that treats zero queue in current samples as proof of future liquidity, assumes the insolvency bonus and full dividends simultaneously, or capitalizes bootstrap rewards into a transferable PAPER price.

## 7. Strict management interface and recurring review

`artifacts/strategy.json` has the requested `version`, `recommended`, `bounds`, `candidates`, `oracleBiasQuestion`, `reviewInputs`, `reviewOutputs`, and `killConditions`. It additionally includes the full `parameterSchema` and metric definitions, so the separately uploaded JSON is self-describing. `strategy-parameters.schema.json` is the same parameter schema as a source file. Every parameter is numeric, finite and required, with an explicit hard minimum and maximum; identifiers/modes are integer codes with meanings in the JSON. `additionalProperties:false` rejects unrecognized fields. In this version **executionEnabled has min=max=0**, and debt funding, partial closing and future-dividend sizing credit are also pinned to zero. Recommended bias 0 is a neutral research default, not a fabricated live oracle answer.

A review may patch **only `recommended`**, within the trusted schema and cross-field policy. It must not edit bounds, candidates, oracle wording, schema or kill conditions. The future bot must pin the reviewed policy/schema hash outside the editable review document and reject a changed policy or stale expected-version hash. Validating a changed JSON against its own changed `bounds` is not a security boundary. This repository includes an offline fail-closed validator and adversarial input checks; it is not a signer or a production transaction executor.

Cross-field validation also requires daily loss limit ≤ weekly ≤ drawdown kill; pair/directional margin ≤ total open margin; neutral threshold < directional threshold; minimum ATR < maximum ATR; nonzero target ATR ≥ stop ATR; used margin plus free-cash minimum ≤1; maximum net notional ≤ gross; and single-group limits. Market minimums and actual per-side OI headroom are additional runtime gates. No field silently clamps invalid data into validity. An out-of-bounds value or unsupported version halts review ingestion.

The review must read **our complete reconciled trade/intent receipts**, actual loss basis and PAPER mint Transfers, supply/stake history, our staked balance, `pendingReward(address)` (selector `0xf40f0f52`), reward accumulator changes, distribution/claim receipts, withdrawals, queue claims and all external flows. It must separately report trading cash PnL, minted PAPER quantity, dividends accrued, dividends claimed to the Exchange, and cash actually withdrawn. A claim is not a second dividend. Do not add an ambiguous API portfolio `pnl` column to `stakingRewards` without reconciling the equity bridge: the [portfolio history API](https://exchange.papertrade.xyz/query/accounts/0xd76232f7b8b9b789bdf03bcb6a9258656a990922/portfolio-history?range=all) is sampled and declares incomplete coverage for this account.

The accounting objective is:

`net external-flow-adjusted cash economics = independently summed net trading settlements + USDC dividends earned/received`,

with pending/queued amounts shown in separate ledgers and no PAPER sale mark. For trade history, establish whether positive `adjustedPnlRaw` is pre-user-fee and subtract the recorded winning fee once; negative raw losses are not reduced again for LP-side fee carving. Retain separate settlement, claim and withdrawal dates. New strategy performance is incremental to a cash-plus-existing-stake baseline. Deposits and withdrawals are flows, not alpha.

Each daily review outputs a strict recommended-only patch with prior policy hash, timestamp and expiry; the integer oracle plus evidence packet; updated dividend distributions; rolling cash-equity/mint reconciliation; candidate mean/p10/p90 and limits; and an adversarial pass/fail for every kill condition. This version must output **an empty transaction list**. The PM owns allocation, researcher owns frozen comparisons, risk manager enforces gates, and adversarial reviewer challenges dependence, survivorship, self-funded rewards, latency and mismatched data windows. The same model filling four roles is not independent validation.

### Remaining unknowns and falsification targets

- **Not measured:** full 90-day protocol history; exact continuous queue uptime; per-recipient fee-versus-surplus attribution over the whole month; future dividend demand; an unbiased population loss sample; historical complete OI and liquidation maps; full swarm-oracle performance.
- **Not verified:** active market impact parameters, exact fixed-point bust/rounding at each historical trade, real quiet-hour schedule, current side caps/minimums, reliable signing/relayer latency, audited implementation source, active collateral address discrepancy and withdrawal liveness. Documentation defaults are not live guarantees.
- **Can falsify the no-farm conclusion:** a sustained, independently measured increase in dollar distributions sufficient to clear the cost-per-basis hurdle after dilution, with positive conservative 90/180-day value and reliable paired exits. A single high dividend day or a survivor wallet cannot do this.
- **Can qualify a directional candidate:** point-in-time public-data packets, locked rules, realistic executable BBO fills and costs, independent future holdouts across regimes, adequate trade counts and positive lower-tail total economics. Any proposed activation requires a new reviewed policy, not a recurring patch that raises risk because PAPER was minted.

## 8. Reproduction and checks

All delivered calculations run **offline with Python 3 standard library**, without packages or network. Run `python3 research/check.py` for data, arithmetic, interface and adversarial checks. `research/README.md` describes optional full regeneration; fetch scripts are read-only provenance tools and are never required for verification. Raw primary responses, failed requests, request metadata, SHA-256 manifest, formulas, full backtest grid, trade-level simulations and projection/combined results are source files under `research/`. Nothing depends on the disposable `test/scratch/` directory.

Checks establish reproducibility and internal consistency, not profitable execution or truth of remote data. No order, wallet signature, stake, claim, approval, contract deployment or live trade was submitted. The useful deliverable is a quantitative **no-new-risk verdict**, explicit conditional economics, and a bounded observation/review specification that can gather the evidence needed to change that verdict.
