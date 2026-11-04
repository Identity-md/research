# Second-pass BTC / ETH indicator tuning at exactly 100x

Research cutoff: **4 November 2026, 00:00 UTC**. Source retrieval and author-run checks occurred later that day. Both assets always use **100x**; no result relies on lowering leverage.

**No setup establishes a robust positive edge at 100x in this study.** The tables below give a single initial-training-selected setting for each of the ten indicators, including losing results. “Best” means the bounded search winner under the declared training objective, not a globally optimal setting. The highest eligible observed OOS mean is **SuperTrend: 0.009 R over 157 trades**. Choosing that family now is exploratory selection from the holdout.

The SuperTrend gain has a **95% block interval of −0.134 to +0.166 R**, turns **−0.038 R at 1bp adverse execution per side**, and its next indicator variant loses **−0.184 R**. Rolling refits lose **−0.076 R**. This is a narrow indicator-parameter result with modest evidence (37–42 trades per fold), despite mild stability under small exit perturbations.

**Evidence labels.** Documented facts describe primary-source pages, not a contract audit. Measured results are calculations on the included candles under explicit execution assumptions. Interpretation and risk limits are inferences/design choices. Unknown live settlement, rounding, queue and execution states are identified below.

## Headline: chronological out-of-sample results

| Setup | TF | OOS trades | Win | Mean net R | PF | Realized max DD R | Bust | Eligible |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| SuperTrend | 60m | 157 | 45.9% | 0.009 | 1.028 | 16.87 | 0.00% | yes |
| TD Sequential | 3m | 275 | 48.0% | -0.023 | 0.915 | 12.29 | 0.36% | yes |
| MA ribbon | 3m | 162 | 50.6% | -0.031 | 0.908 | 11.88 | 0.62% | yes |
| Volume | 3m | 187 | 41.7% | -0.034 | 0.897 | 13.74 | 0.00% | yes |
| Stochastic | 15m | 353 | 51.6% | -0.058 | 0.793 | 25.43 | 0.28% | yes |
| Moving averages | 5m | 166 | 45.8% | -0.063 | 0.810 | 18.24 | 0.00% | yes |
| Bollinger | 1m | 284 | 44.4% | -0.093 | 0.701 | 31.86 | 0.00% | yes |
| RSI | 1m | 230 | 45.2% | -0.117 | 0.629 | 29.24 | 0.00% | yes |
| Ichimoku | 3m | 429 | 43.6% | -0.120 | 0.641 | 57.66 | 0.47% | yes |
| MACD | 15m | 278 | 41.7% | -0.137 | 0.556 | 40.77 | 0.00% | yes |

Headline period: **12 August–4 November 2026**, 84 days, four nonoverlapping 21-day blocks. Configurations above were selected only on **17 June–12 August**, after 14 days of warm-up. Eligibility requires at least **100 pooled OOS trades and 15 in every fold**. Tables include both BTC and ETH, both directions, without hindsight asset/side exclusions. All statistics aggregate a two-leg exit as one strategy trade.

R = net modeled PnL / (initial total notional × raw stop fraction). A normal un-slipped stop is −1 R; full bust is −0.01/stop R. Win means strictly positive PnL. PF = positive R sum / absolute negative R sum, undefined without losses. Drawdown is **realized-only**, chronological exit equity, with zero starting equity included; BTC is booked first on tied exit minutes. For dual-position exits, these realized-only tables book aggregate PnL at the last leg’s close; the marked paths below credit each leg at its own exit. Realized-only drawdown understates floating/intraminute risk and is not a cash-withdrawal drawdown. Zero observed busts is not proof of safety.

Separate survival rankings among eligible standalone indicators:

| Rank | Lowest observed bust rate (ties: mean R) | Bust | Smallest realized DD | DD R |
|---:|---|---:|---|---:|
| 1 | SuperTrend | 0.00% | MA ribbon | 11.88 |
| 2 | Volume | 0.00% | TD Sequential | 12.29 |
| 3 | Moving averages | 0.00% | Volume | 13.74 |
| 4 | Bollinger | 0.00% | SuperTrend | 16.87 |
| 5 | RSI | 0.00% | Moving averages | 18.24 |
| 6 | MACD | 0.00% | Stochastic | 25.43 |
| 7 | Stochastic | 0.28% | RSI | 29.24 |
| 8 | TD Sequential | 0.36% | Bollinger | 31.86 |
| 9 | Ichimoku | 0.47% | MACD | 40.77 |
| 10 | MA ribbon | 0.62% | Ichimoku | 57.66 |

Low DD can simply reflect fewer trades or a different R denominator. With zero busts, the rough independent-trade 95% upper bound is 3/n; clustered BTC/ETH events make even that approximation optimistic. These ranks must not be combined into a claimed portfolio return.

One-minute net-close drawdown, including remaining-position PnL, gives the more relevant survival comparison:

| Rank | Setup | Mark-to-close DD R | DD as % initial cash at 0.10% margin/trade |
|---:|---|---:|---:|
| 1 | MA ribbon | 12.25 | 0.466% |
| 2 | TD Sequential | 13.02 | 0.495% |
| 3 | Volume | 14.59 | 0.555% |
| 4 | SuperTrend | 18.67 | 0.709% |
| 5 | Moving averages | 19.35 | 0.735% |
| 6 | Stochastic | 26.35 | 1.001% |
| 7 | RSI | 30.52 | 1.160% |
| 8 | Bollinger | 32.40 | 1.231% |
| 9 | MACD | 41.79 | 1.588% |
| 10 | Ichimoku | 58.16 | 2.210% |

Each minute marks surviving legs to a hypothetical net close; realized partial closes remain credited. These equity paths reconcile exactly to final trade-ledger PnL and are retained under `research/results/equity-family-*.csv.xz`. They still omit intraminute equity extrema, actual liquidity/queue haircuts and policy trade caps. Account percentages use fixed initial margin, no compounding; they are separate experiments.

## Data, attribution and the first pass

Read first: the supplied [first-pass report](https://api.imd.fun/artifacts/9192786bee06cc298914a72245224d5c1a6445d025c51db37a89f3de12e6da7a), [machine-readable tuning](https://api.imd.fun/artifacts/f1c8591e30a2e8945ec176d7a162156e4ac4737aff45749110a99828fa401d11), and [mechanics research](https://api.imd.fun/artifacts/6e8652275deb7261fcc223d0cbcb13342ab70f0f84d1a3063dff85857a9af858). Their byte-identical copies and hashes are retained in `sources/inputs/`. The earlier TD −0.020 R/59 and RSI −0.035 R/1,079 figures refer to a different 12-day test and different exits. The new results are not a paired proof that tuning improved performance.

**Fresh acquisition:** 221,760 confirmed native one-minute candles per asset, **3 June–4 November 2026**, 154 complete UTC days. Instruments are **OKX BTC-USDT-SWAP and ETH-USDT-SWAP**, perpetuals, prices USDT, volume base units. No missing/duplicate minutes; all OHLC and nonnegative-volume checks passed. Source: [OKX history-candles](https://www.okx.com/api/v5/market/history-candles), with [official field/pagination definitions](https://www.okx.com/docs-v5/en/#rest-api-market-data-get-candlesticks-history). The optional fetcher retries failed batches, rejects incomplete windows and does not splice venues.

The old-range [Hyperliquid candleSnapshot](https://api.hyperliquid.xyz/info) probe returned an empty array (HTTP 200), retained in `sources/hyperliquid-probe.json`; this could not supply 120 days, so the specified OKX fallback was used. Hyperliquid documents only the [most recent 5,000 candles](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#candle-snapshot), which is insufficient at 1m.

UTC-aligned OHLCV aggregation builds 1m/3m/5m/15m/1h bars: **221,760 / 73,920 / 44,352 / 14,784 / 3,696 per asset**. Open first, high/low extrema, close last, base-volume sum. All executions remain one-minute resolution. Native higher-timeframe API cross-checks: **24/24** matched within stated numeric tolerance; raw sampled rows and requests are in `sources/native-bar-checks.json`. Native inputs are bundled losslessly as delta-coded integer columns in `data/*.delta.xz`, with compressed and original CSV SHA-256 hashes and decimal scales. `research/run.py derive` rebuilds all five timeframes from those inputs without network access; redundant derived copies are omitted from the source bundle.

**Independence limit:** this 84-day period is OOS with respect to this study’s fitting, but **not an untouched independent replication of the first pass**. That input already exposed September–November candles and October 22–November 3 outcomes. Most new history was added backwards, not prospectively. The JSON separately reports OOS entries before the first-pass data begins, inside its span, and after its cutoff. There are only eight newly observed hours after its cutoff here; that cannot validate a live edge.

## Economics and execution model

Documented Papertrade positions settle against the LP at Hyperliquid BBO midpoint; OKX traded OHLC is therefore a **cross-venue proxy**, not an execution replay. There is no notional fee, funding, spread charge or user gas fee. Winning PnL is discounted and then charged 2%; losses are taken in full. The main frontend names no builder. [Pricing](https://docs.papertrade.xyz/how/pricing-bbo/), [trades](https://docs.papertrade.xyz/learn/trades-pricing/), [wins/losses](https://docs.papertrade.xyz/learn/wins-losses/).

For directional fractional return d = side × (exit/entry − 1), d <= 0 pays d × notional unless bust. For d > 0 use the documented reconstruction:

```text
a=.000075, z=.0006, k=3.597, exponent=2  (standard)
a=.00003,  z=.001,  k=6.085, exponent=3  (off-hours)
u=(d-a)/(z-a)
hold=k*(z-a)*u^2*(1-u)^exponent inside (a,z), otherwise 0
q=max(0,d-.00002-hold)
net/notional = q*.90/(1+1/(q*15000)+.1/(q*p))*.98; 0 if q=0
pBTC=814.598, pETH=483.979
```

These are rounded, owner-adjustable documentation defaults, held constant counterfactually throughout all historical prices. Active curve-switch history is unknown; headline uses standard, sensitivity all off-hours. Target prices numerically invert this function to earn net 1/2/3 R per target leg, compensating asymmetric impact instead of assuming gross 2:1 means net 2:1. The impact×1.25 stress multiplies base rate and both denominator-friction terms; it is a modeled stress, not a published parameter setting. [Asymmetric impact](https://docs.papertrade.xyz/how/asymmetric-impact/), [operator powers](https://docs.papertrade.xyz/how/risk/).

Approximate 100x bust distance is **0.95%**, reflecting a roughly 5bp buffer before the 1% zero-equity move; crossing it forfeits full isolated margin even on voluntary close. Test 0.90%/1.00% as uncertainty scenarios. Stops use 15%, 25%, 40% or 60% of the baseline bust distance: **0.1425%, 0.2375%, 0.3800%, 0.5700%**. Exact displayed bust price overrides this approximation operationally. [Liquidations](https://docs.papertrade.xyz/learn/liquidations/).

The docs permit **full-size closes only**. Scale-out is modeled as two separately opened positions with half of total margin each, closed independently. Payout fractions are size-independent under the documented curve, so splitting alone creates no economic advantage. Simultaneous successful opens/closes, sufficient position minimums and reliable close automation are assumptions; a chart stop is not a guaranteed native order. [Position mechanics](https://docs.papertrade.xyz/learn/trades-pricing/).

**Causal execution:** signal bar i confirms at its close; entry is the immediately following one-minute open (baseline zero extra basis/slippage). Reject drift >0.10% from signal close. One trade per asset; signals while open are discarded, no pyramiding or reversal. Opening beyond bust loses all margin; adverse stop gaps fill at the open; favorable gaps through target get only target. The TTL exit occurs at its minute open, before that minute’s extremes. During ordinary holding minutes, bust takes priority if its level is reachable; otherwise stop precedes target if both touched. This deliberately pessimistic OHLC ordering does not establish what happened intraminute. An ideal-stop-first stress gives the other endpoint. Stops/trails inferred from completed one-minute closes apply next minute only; no high-water mark from an unfinished bar is used.

Entries too near each split end to complete their maximum holding period are excluded in advance; no cross-fold positions or favorable boundary marks. In delayed scenarios, a triggered close waits one/two minutes, with bust monitoring while pending; time stops still execute at their preset open. Slippage scenarios worsen both entry and exit by 1/2/5/10bp; entry drift veto is based on the observed open, so stressed fills can violate that operational limit intentionally. Price-loss-plus-slippage at bust is capped at full margin.

No PAPER income or staking return is credited. Quantities and realizable dollar value are unknown. Measured positive PnL represents a claim, not necessarily immediately paid cash: historical LP cash, queue priority and protocol state are absent. The current contract set is documented from 21 October 2026; earlier price windows are **current-rule counterfactuals**, not realized Papertrade results. [Queue accounting](https://docs.papertrade.xyz/how/solvency-queue/), [protocol changes](https://docs.papertrade.xyz/dev/protocol-changes/).

## Search and rolling robustness design

The grid contains **34,560 configurations per training window**: 16 families (ten standalone, three pairs, three triples) × 3 parameter variants × 5 timeframes × 12 filter profiles × 12 exit designs. Every raw training score is retained in four compressed audit files. Four rolling searches total **138,240 configuration-window comparisons**; neither this nor the prior 720-candidate study is a single hypothesis.

| Fold | Rolling training, UTC [start,end) | OOS, UTC [start,end) |
|---:|---|---|
| 1 | 2026-06-17 → 2026-08-12 | 2026-08-12 → 2026-09-02 |
| 2 | 2026-07-08 → 2026-09-02 | 2026-09-02 → 2026-09-23 |
| 3 | 2026-07-29 → 2026-09-23 | 2026-09-23 → 2026-10-14 |
| 4 | 2026-08-19 → 2026-10-14 | 2026-10-14 → 2026-11-04 |

Selection uses training mean R − 0.5 × SD(R)/sqrt(n), ≥100 pooled trades and ≥20 per asset, deterministic grid order breaking ties. This mild iid penalty is a ranking heuristic, not confidence. The first fold’s winner is the single fixed setting reported per family; rolling refits choose from their own preceding 56 days. Decisions for all windows were written to `research/results/selection-lock.json` before OOS scoring; its hash is in the JSON. No test score changes a frozen setting.

Filters cover hourly EMA100 slope/direction, local ADX14 and EMA50 alignment, ATR percentile, ATR-based excursion proxy, weekday/weekend and UTC Asia/Europe/US hour cohorts, other-asset 15m EMA50 confirmation, and own 15m plus hourly confluence. They are a bounded profile grid, not an exhaustive per-hour search. The volatility veto uses **3 × ATR14(1m) <= stop**, with ATR percentile 10–80 against the preceding 480 observations. ATR is a heuristic excursion proxy, not an estimated probability that adverse excursion stays below stop. High-volatility tail protection is therefore unproven. Exact selected profiles appear below; entry-hour/day attribution is in the JSON and never used for post-hoc entry deletion.

Exit designs jointly test fixed net targets, very short 3/8/20/45 minute limits, break-even stops, close-based ratcheting trails, and two-position 50/50 take-profit emulation. The JSON retains the complete exit vector. All stop fractions are inside even the 0.90% bust stress.

Indicator definitions: full-window SMA/population SD; EMA seeded at the first full finite-window SMA, alpha 2/(n+1); RSI/ATR/ADX use Wilder alpha 1/n. RSI is 50 on a flat series; stochastic K is 50 for a zero range. Ichimoku displayed spans are shifted **from past bars** by displacement, never a future cloud. Midpoints are (rolling high + rolling low)/2. SuperTrend uses hl2 ± multiplier×Wilder ATR, final upper resets down or after prior close above it; final lower resets up or after prior close below it; initial direction up, then close crosses final bands. TD is a transparent setup-count/perfection variant, with strict close-versus-four-back counts and no countdown entries; it does not claim licensed Sequential equivalence. Moving averages use ordinary EMA crosses in this pass, rather than the prior compression-release family.

## Exact settings and fold-by-fold results

Every rule below inherits the confirmation, execution, R, overlap and do-not-trade conventions above. Equality is accepted only where written. All signals use their stated completed timeframe; all protective monitoring is one-minute. A missing/NaN required feature means no entry. Stops are entry-price percentages, never widened.

### 1. Bollinger — 1m

**Parameters:** `{"period":20,"population_sd_multiple":2.0}`.

**Long:** Low <= SMA20 - 2.0 × population SD20; close > that lower band and close > open. **Short:** High >= SMA20 + 2.0 × population SD20; close < that upper band and close < open.

**Confirmation/entry:** Completed signal bar i; enter at the next one-minute open at the signal bar start timestamp plus its full timeframe. Never enter within signal bar. **Filters:** Monday-Friday, entry UTC hour 08 through 11 inclusive. Latest completed UTC 1h close > its EMA100 and that EMA100 > its value five hourly bars earlier for long; both inequalities reversed for short. One-minute ATR14/entry open, calculated through the previous minute, × 3 <= initial stop fraction; current ATR fraction percentile in [10%,80%] against the preceding 480 ATR fractions (strictly lower ranks / 480). This is a volatility proxy, not a measured adverse-excursion bound.

**Initial stop:** 0.3800% of entry = 40% of approximate bust distance. Long E×(1−0.0038000); short E×(1+0.0038000). **Main target:** net 3 R per target leg; gross price move **BTC 1.313190%, ETH 1.321291%**, favorable direction from entry. After a completed one-minute close reaches +1 initial stop, raise the stop to entry from the next minute. Never lower it. No trailing or partial exits.

**Time stop:** 45 minutes, at open after exactly that many complete one-minute holding candles. **Do not trade:** Skip non-confirmed or missing candles, NaN required features, absent trigger/filter, entry open >0.10% away from signal close, an already open position in that asset, or insufficient complete execution horizon before a split. Operational veto: stale BBO, changed payout settings, unavailable/rejected close service, paused/retired market, queue/cash uncertainty, or actual displayed bust inside planned stop. Operational vetoes were not backtested.

**Pooled OOS:** 284 trades; win 44.4%; mean -0.093 R; PF 0.701; realized DD 31.86 R; bust 0.00%. Initial-training winner: 195 trades, mean 0.094 R (not headline). **BTC:** 132 trades; win 46.2%; mean -0.063 R; PF 0.778; realized DD 9.44 R; bust 0.00%. **ETH:** 152 trades; win 42.8%; mean -0.120 R; PF 0.645; realized DD 22.53 R; bust 0.00%.

| Fold | Fixed trades | Win | Mean R | PF | DD R | Bust | Rolling-selected mean R (trades) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 63 | 38.1% | -0.058 | 0.827 | 8.99 | 0.00% | -0.058 (63) |
| 2 | 75 | 46.7% | -0.033 | 0.892 | 8.84 | 0.00% | -0.051 (51) |
| 3 | 69 | 47.8% | -0.130 | 0.568 | 10.81 | 0.00% | -0.155 (29) |
| 4 | 77 | 44.2% | -0.148 | 0.522 | 11.42 | 0.00% | -0.092 (55) |

Three-day joint-asset bootstrap 95% interval for mean: **[-0.187, 0.004] R**. Bonferroni/HAC lower bound -0.331 R; adjusted one-sided p=1.000. 
Continuous neighborhood: 0/6 eligible ±10% variants positive; median -0.090 R, worst -0.109 R. **No positive plateau demonstrated; fragile or persistently nonpositive.**

### 2. Moving averages — 5m

**Parameters:** `{"ema_fast":12,"ema_slow":50}`.

**Long:** EMA12 > EMA50 now and EMA12 <= EMA50 on the previous bar. **Short:** EMA12 < EMA50 now and EMA12 >= EMA50 on the previous bar.

**Confirmation/entry:** Completed signal bar i; enter at the next one-minute open at the signal bar start timestamp plus its full timeframe. Never enter within signal bar. **Filters:** Signal-timeframe Wilder ADX14 >= 25; signal close > EMA50 for long, < EMA50 for short.

**Initial stop:** 0.3800% of entry = 40% of approximate bust distance. Long E×(1−0.0038000); short E×(1+0.0038000). **Main target:** net 3 R per target leg; gross price move **BTC 1.313190%, ETH 1.321291%**, favorable direction from entry. After a completed one-minute close reaches +1 initial stop, raise the stop to entry from the next minute. Never lower it. No trailing or partial exits.

**Time stop:** 45 minutes, at open after exactly that many complete one-minute holding candles. **Do not trade:** Skip non-confirmed or missing candles, NaN required features, absent trigger/filter, entry open >0.10% away from signal close, an already open position in that asset, or insufficient complete execution horizon before a split. Operational veto: stale BBO, changed payout settings, unavailable/rejected close service, paused/retired market, queue/cash uncertainty, or actual displayed bust inside planned stop. Operational vetoes were not backtested.

**Pooled OOS:** 166 trades; win 45.8%; mean -0.063 R; PF 0.810; realized DD 18.24 R; bust 0.00%. Initial-training winner: 133 trades, mean 0.087 R (not headline). **BTC:** 94 trades; win 40.4%; mean -0.135 R; PF 0.609; realized DD 14.24 R; bust 0.00%. **ETH:** 72 trades; win 52.8%; mean 0.032 R; PF 1.103; realized DD 6.26 R; bust 0.00%.

| Fold | Fixed trades | Win | Mean R | PF | DD R | Bust | Rolling-selected mean R (trades) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 46 | 41.3% | -0.084 | 0.682 | 8.24 | 0.00% | -0.084 (46) |
| 2 | 30 | 50.0% | 0.035 | 1.129 | 3.36 | 0.00% | -0.001 (44) |
| 3 | 42 | 45.2% | -0.152 | 0.577 | 9.24 | 0.00% | 0.013 (59) |
| 4 | 48 | 47.9% | -0.025 | 0.938 | 9.40 | 0.00% | -0.098 (50) |

Three-day joint-asset bootstrap 95% interval for mean: **[-0.189, 0.060] R**. Bonferroni/HAC lower bound -0.384 R; adjusted one-sided p=1.000. 
Continuous neighborhood: 0/6 eligible ±10% variants positive; median -0.060 R, worst -0.068 R. **No positive plateau demonstrated; fragile or persistently nonpositive.**

### 3. MA ribbon — 3m

**Parameters:** `{"fast_emas":[8,13,21],"slow_emas":[34,55,89]}`.

**Long:** Mean of EMAs [8, 13, 21] crosses strictly above mean of EMAs [34, 55, 89]; previous fast mean <= slow mean. **Short:** Mean of EMAs [8, 13, 21] crosses strictly below mean of EMAs [34, 55, 89]; previous fast mean >= slow mean.

**Confirmation/entry:** Completed signal bar i; enter at the next one-minute open at the signal bar start timestamp plus its full timeframe. Never enter within signal bar. **Filters:** Monday-Friday, entry UTC hour 12 through 19 inclusive. One-minute ATR14/entry open, calculated through the previous minute, × 3 <= initial stop fraction; current ATR fraction percentile in [10%,80%] against the preceding 480 ATR fractions (strictly lower ranks / 480). This is a volatility proxy, not a measured adverse-excursion bound.

**Initial stop:** 0.3800% of entry = 40% of approximate bust distance. Long E×(1−0.0038000); short E×(1+0.0038000). **Main target:** net 3 R per target leg; gross price move **BTC 1.313190%, ETH 1.321291%**, favorable direction from entry. Open two independent positions simultaneously with 50% of total margin each. First target earns net 1 initial R on that leg; second target earns net 3 initial R on that leg. For either surviving leg, a completed one-minute close at +1 initial stop raises stop to entry next minute; at +1.5 stops raises it to close minus 0.75 initial stop next minute. Never lower a stop. This emulates scale-out; no native partial close is assumed.

Half-margin first-leg targets: BTC 0.451015%, ETH 0.458624% favorable move; headline main target is the second leg.

**Time stop:** 45 minutes, at open after exactly that many complete one-minute holding candles. **Do not trade:** Skip non-confirmed or missing candles, NaN required features, absent trigger/filter, entry open >0.10% away from signal close, an already open position in that asset, or insufficient complete execution horizon before a split. Operational veto: stale BBO, changed payout settings, unavailable/rejected close service, paused/retired market, queue/cash uncertainty, or actual displayed bust inside planned stop. Operational vetoes were not backtested.

**Pooled OOS:** 162 trades; win 50.6%; mean -0.031 R; PF 0.908; realized DD 11.88 R; bust 0.62%. Initial-training winner: 108 trades, mean 0.068 R (not headline). **BTC:** 78 trades; win 47.4%; mean -0.057 R; PF 0.816; realized DD 7.80 R; bust 0.00%. **ETH:** 84 trades; win 53.6%; mean -0.007 R; PF 0.981; realized DD 7.17 R; bust 1.19%.

| Fold | Fixed trades | Win | Mean R | PF | DD R | Bust | Rolling-selected mean R (trades) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 31 | 58.1% | 0.012 | 1.035 | 4.18 | 0.00% | 0.012 (31) |
| 2 | 48 | 41.7% | -0.095 | 0.758 | 9.78 | 0.00% | -0.114 (65) |
| 3 | 42 | 54.8% | 0.088 | 1.374 | 3.36 | 0.00% | 0.006 (62) |
| 4 | 41 | 51.2% | -0.111 | 0.710 | 6.70 | 2.44% | 0.182 (46) |

Three-day joint-asset bootstrap 95% interval for mean: **[-0.201, 0.121] R**. Bonferroni/HAC lower bound -0.438 R; adjusted one-sided p=1.000. 
Continuous neighborhood: 1/6 eligible ±10% variants positive; median -0.028 R, worst -0.060 R. **No positive plateau demonstrated; fragile or persistently nonpositive.**

### 4. SuperTrend — 60m

**Parameters:** `{"wilder_atr":7,"multiplier":2.0}`.

**Long:** SuperTrend direction flips from down to up on a completed close strictly above the current final upper band. **Short:** SuperTrend direction flips from up to down on a completed close strictly below the current final lower band.

**Confirmation/entry:** Completed signal bar i; enter at the next one-minute open at the signal bar start timestamp plus its full timeframe. Never enter within signal bar. **Filters:** None; all UTC hours and weekdays eligible.

**Initial stop:** 0.3800% of entry = 40% of approximate bust distance. Long E×(1−0.0038000); short E×(1+0.0038000). **Main target:** net 3 R per target leg; gross price move **BTC 1.313190%, ETH 1.321291%**, favorable direction from entry. After a completed one-minute close reaches +1.5 initial stops, raise the stop to that close minus 0.75 initial stop in directional-return coordinates; effective next minute. Never lower it. No partial exits.

**Time stop:** 45 minutes, at open after exactly that many complete one-minute holding candles. **Do not trade:** Skip non-confirmed or missing candles, NaN required features, absent trigger/filter, entry open >0.10% away from signal close, an already open position in that asset, or insufficient complete execution horizon before a split. Operational veto: stale BBO, changed payout settings, unavailable/rejected close service, paused/retired market, queue/cash uncertainty, or actual displayed bust inside planned stop. Operational vetoes were not backtested.

**Pooled OOS:** 157 trades; win 45.9%; mean 0.009 R; PF 1.028; realized DD 16.87 R; bust 0.00%. Initial-training winner: 105 trades, mean 0.080 R (not headline). **BTC:** 79 trades; win 46.8%; mean -0.023 R; PF 0.923; realized DD 8.08 R; bust 0.00%. **ETH:** 78 trades; win 44.9%; mean 0.042 R; PF 1.117; realized DD 8.79 R; bust 0.00%.

| Fold | Fixed trades | Win | Mean R | PF | DD R | Bust | Rolling-selected mean R (trades) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 37 | 48.6% | 0.042 | 1.134 | 3.57 | 0.00% | 0.042 (37) |
| 2 | 38 | 31.6% | -0.160 | 0.602 | 10.90 | 0.00% | -0.101 (86) |
| 3 | 42 | 40.5% | -0.075 | 0.753 | 8.76 | 0.00% | -0.084 (39) |
| 4 | 40 | 62.5% | 0.227 | 1.766 | 2.00 | 0.00% | -0.125 (39) |

Three-day joint-asset bootstrap 95% interval for mean: **[-0.134, 0.166] R**. Bonferroni/HAC lower bound -0.378 R; adjusted one-sided p=1.000. 
Continuous neighborhood: 4/6 eligible ±10% variants positive; median 0.003 R, worst -0.011 R. **Observed positive plateau; still exploratory.**

### 5. Ichimoku — 3m

**Parameters:** `{"tenkan":6,"kijun":18,"span_b":36,"displacement":18}`.

**Long:** Close breaks strictly above displayed cloud top (previous close <= previous cloud top), and tenkan > kijun. **Short:** Close breaks strictly below displayed cloud bottom (previous close >= previous cloud bottom), and tenkan < kijun.

**Confirmation/entry:** Completed signal bar i; enter at the next one-minute open at the signal bar start timestamp plus its full timeframe. Never enter within signal bar. **Filters:** Signal-timeframe Wilder ADX14 >= 25; signal close > EMA50 for long, < EMA50 for short.

**Initial stop:** 0.3800% of entry = 40% of approximate bust distance. Long E×(1−0.0038000); short E×(1+0.0038000). **Main target:** net 3 R per target leg; gross price move **BTC 1.313190%, ETH 1.321291%**, favorable direction from entry. After a completed one-minute close reaches +1 initial stop, raise the stop to entry from the next minute. Never lower it. No trailing or partial exits.

**Time stop:** 45 minutes, at open after exactly that many complete one-minute holding candles. **Do not trade:** Skip non-confirmed or missing candles, NaN required features, absent trigger/filter, entry open >0.10% away from signal close, an already open position in that asset, or insufficient complete execution horizon before a split. Operational veto: stale BBO, changed payout settings, unavailable/rejected close service, paused/retired market, queue/cash uncertainty, or actual displayed bust inside planned stop. Operational vetoes were not backtested.

**Pooled OOS:** 429 trades; win 43.6%; mean -0.120 R; PF 0.641; realized DD 57.66 R; bust 0.47%. Initial-training winner: 313 trades, mean 0.069 R (not headline). **BTC:** 219 trades; win 47.0%; mean -0.094 R; PF 0.679; realized DD 25.67 R; bust 0.46%. **ETH:** 210 trades; win 40.0%; mean -0.147 R; PF 0.610; realized DD 34.60 R; bust 0.48%.

| Fold | Fixed trades | Win | Mean R | PF | DD R | Bust | Rolling-selected mean R (trades) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 111 | 35.1% | -0.165 | 0.587 | 23.28 | 0.00% | -0.165 (111) |
| 2 | 110 | 49.1% | -0.089 | 0.710 | 16.23 | 1.82% | -0.042 (62) |
| 3 | 103 | 41.7% | -0.124 | 0.617 | 15.97 | 0.00% | -0.072 (35) |
| 4 | 105 | 48.6% | -0.101 | 0.667 | 17.40 | 0.00% | -0.034 (32) |

Three-day joint-asset bootstrap 95% interval for mean: **[-0.198, -0.040] R**. Bonferroni/HAC lower bound -0.321 R; adjusted one-sided p=1.000. 
Continuous neighborhood: 0/6 eligible ±10% variants positive; median -0.115 R, worst -0.121 R. **No positive plateau demonstrated; fragile or persistently nonpositive.**

### 6. TD Sequential — 3m

**Parameters:** `{"setup_count":9,"comparison_lag":4,"perfection":true,"countdown_entries":false}`.

**Long:** Exactly 9 consecutive closes strictly below close four bars earlier; close > open; min(current low, previous low) <= min(lows two and three bars earlier). **Short:** Exactly 9 consecutive closes strictly above close four bars earlier; close < open; max(current high, previous high) >= max(highs two and three bars earlier).

**Confirmation/entry:** Completed signal bar i; enter at the next one-minute open at the signal bar start timestamp plus its full timeframe. Never enter within signal bar. **Filters:** Latest completed UTC 1h close > its EMA100 and that EMA100 > its value five hourly bars earlier for long; both inequalities reversed for short.

**Initial stop:** 0.3800% of entry = 40% of approximate bust distance. Long E×(1−0.0038000); short E×(1+0.0038000). **Main target:** net 3 R per target leg; gross price move **BTC 1.313190%, ETH 1.321291%**, favorable direction from entry. After a completed one-minute close reaches +1 initial stop, raise the stop to entry from the next minute. Never lower it. No trailing or partial exits.

**Time stop:** 45 minutes, at open after exactly that many complete one-minute holding candles. **Do not trade:** Skip non-confirmed or missing candles, NaN required features, absent trigger/filter, entry open >0.10% away from signal close, an already open position in that asset, or insufficient complete execution horizon before a split. Operational veto: stale BBO, changed payout settings, unavailable/rejected close service, paused/retired market, queue/cash uncertainty, or actual displayed bust inside planned stop. Operational vetoes were not backtested.

**Pooled OOS:** 275 trades; win 48.0%; mean -0.023 R; PF 0.915; realized DD 12.29 R; bust 0.36%. Initial-training winner: 198 trades, mean 0.073 R (not headline). **BTC:** 130 trades; win 50.8%; mean 0.002 R; PF 1.010; realized DD 7.32 R; bust 0.00%. **ETH:** 145 trades; win 45.5%; mean -0.046 R; PF 0.849; realized DD 12.07 R; bust 0.69%.

| Fold | Fixed trades | Win | Mean R | PF | DD R | Bust | Rolling-selected mean R (trades) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 62 | 48.4% | -0.026 | 0.912 | 8.51 | 1.61% | -0.026 (62) |
| 2 | 67 | 49.3% | -0.003 | 0.991 | 5.47 | 0.00% | -0.086 (32) |
| 3 | 82 | 50.0% | -0.038 | 0.844 | 6.33 | 0.00% | 0.132 (32) |
| 4 | 64 | 43.8% | -0.023 | 0.917 | 7.60 | 0.00% | -0.184 (51) |

Three-day joint-asset bootstrap 95% interval for mean: **[-0.094, 0.045] R**. Bonferroni/HAC lower bound -0.197 R; adjusted one-sided p=1.000. 
Continuous neighborhood: 0/6 eligible ±10% variants positive; median -0.023 R, worst -0.038 R. **No positive plateau demonstrated; fragile or persistently nonpositive.**

### 7. RSI — 1m

**Parameters:** `{"wilder_rsi":7,"lower":25,"upper":75}`.

**Long:** Previous RSI7 < 25, current RSI >= 25, close > open. **Short:** Previous RSI7 > 75, current RSI <= 75, close < open.

**Confirmation/entry:** Completed signal bar i; enter at the next one-minute open at the signal bar start timestamp plus its full timeframe. Never enter within signal bar. **Filters:** Monday-Friday, entry UTC hour 08 through 11 inclusive. Latest completed UTC 1h close > its EMA100 and that EMA100 > its value five hourly bars earlier for long; both inequalities reversed for short. One-minute ATR14/entry open, calculated through the previous minute, × 3 <= initial stop fraction; current ATR fraction percentile in [10%,80%] against the preceding 480 ATR fractions (strictly lower ranks / 480). This is a volatility proxy, not a measured adverse-excursion bound.

**Initial stop:** 0.3800% of entry = 40% of approximate bust distance. Long E×(1−0.0038000); short E×(1+0.0038000). **Main target:** net 3 R per target leg; gross price move **BTC 1.313190%, ETH 1.321291%**, favorable direction from entry. After a completed one-minute close reaches +1 initial stop, raise the stop to entry from the next minute. Never lower it. No trailing or partial exits.

**Time stop:** 45 minutes, at open after exactly that many complete one-minute holding candles. **Do not trade:** Skip non-confirmed or missing candles, NaN required features, absent trigger/filter, entry open >0.10% away from signal close, an already open position in that asset, or insufficient complete execution horizon before a split. Operational veto: stale BBO, changed payout settings, unavailable/rejected close service, paused/retired market, queue/cash uncertainty, or actual displayed bust inside planned stop. Operational vetoes were not backtested.

**Pooled OOS:** 230 trades; win 45.2%; mean -0.117 R; PF 0.629; realized DD 29.24 R; bust 0.00%. Initial-training winner: 142 trades, mean 0.050 R (not headline). **BTC:** 120 trades; win 42.5%; mean -0.131 R; PF 0.574; realized DD 16.17 R; bust 0.00%. **ETH:** 110 trades; win 48.2%; mean -0.101 R; PF 0.686; realized DD 14.00 R; bust 0.00%.

| Fold | Fixed trades | Win | Mean R | PF | DD R | Bust | Rolling-selected mean R (trades) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 62 | 46.8% | -0.045 | 0.851 | 5.92 | 0.00% | -0.045 (62) |
| 2 | 49 | 46.9% | -0.053 | 0.790 | 6.06 | 0.00% | 0.149 (46) |
| 3 | 57 | 42.1% | -0.249 | 0.330 | 14.18 | 0.00% | -0.134 (74) |
| 4 | 62 | 45.2% | -0.117 | 0.638 | 7.37 | 0.00% | -0.099 (58) |

Three-day joint-asset bootstrap 95% interval for mean: **[-0.204, -0.029] R**. Bonferroni/HAC lower bound -0.335 R; adjusted one-sided p=1.000. 
Continuous neighborhood: 0/6 eligible ±10% variants positive; median -0.114 R, worst -0.130 R. **No positive plateau demonstrated; fragile or persistently nonpositive.**

### 8. MACD — 15m

**Parameters:** `{"fast_ema":12,"slow_ema":26,"signal_ema":9}`.

**Long:** (EMA12-EMA26) minus its EMA9 crosses strictly above zero; previous histogram <= 0. **Short:** (EMA12-EMA26) minus its EMA9 crosses strictly below zero; previous histogram >= 0.

**Confirmation/entry:** Completed signal bar i; enter at the next one-minute open at the signal bar start timestamp plus its full timeframe. Never enter within signal bar. **Filters:** All weekdays, entry UTC hour 00 through 07 inclusive. One-minute ATR14/entry open, calculated through the previous minute, × 3 <= initial stop fraction; current ATR fraction percentile in [10%,80%] against the preceding 480 ATR fractions (strictly lower ranks / 480). This is a volatility proxy, not a measured adverse-excursion bound.

**Initial stop:** 0.3800% of entry = 40% of approximate bust distance. Long E×(1−0.0038000); short E×(1+0.0038000). **Main target:** net 3 R per target leg; gross price move **BTC 1.313190%, ETH 1.321291%**, favorable direction from entry. After a completed one-minute close reaches +1 initial stop, raise the stop to entry from the next minute. Never lower it. No trailing or partial exits.

**Time stop:** 45 minutes, at open after exactly that many complete one-minute holding candles. **Do not trade:** Skip non-confirmed or missing candles, NaN required features, absent trigger/filter, entry open >0.10% away from signal close, an already open position in that asset, or insufficient complete execution horizon before a split. Operational veto: stale BBO, changed payout settings, unavailable/rejected close service, paused/retired market, queue/cash uncertainty, or actual displayed bust inside planned stop. Operational vetoes were not backtested.

**Pooled OOS:** 278 trades; win 41.7%; mean -0.137 R; PF 0.556; realized DD 40.77 R; bust 0.00%. Initial-training winner: 186 trades, mean 0.034 R (not headline). **BTC:** 147 trades; win 42.2%; mean -0.122 R; PF 0.576; realized DD 20.57 R; bust 0.00%. **ETH:** 131 trades; win 41.2%; mean -0.155 R; PF 0.536; realized DD 24.20 R; bust 0.00%.

| Fold | Fixed trades | Win | Mean R | PF | DD R | Bust | Rolling-selected mean R (trades) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 64 | 43.8% | -0.027 | 0.897 | 4.16 | 0.00% | -0.027 (64) |
| 2 | 70 | 31.4% | -0.291 | 0.311 | 20.36 | 0.00% | -0.215 (47) |
| 3 | 83 | 38.6% | -0.166 | 0.483 | 17.94 | 0.00% | 0.026 (64) |
| 4 | 61 | 55.7% | -0.038 | 0.819 | 3.22 | 0.00% | 0.008 (56) |

Three-day joint-asset bootstrap 95% interval for mean: **[-0.213, -0.062] R**. Bonferroni/HAC lower bound -0.326 R; adjusted one-sided p=1.000. 
Continuous neighborhood: 0/6 eligible ±10% variants positive; median -0.136 R, worst -0.171 R. **No positive plateau demonstrated; fragile or persistently nonpositive.**

### 9. Stochastic — 15m

**Parameters:** `{"raw_k_period":9,"d_sma":3,"lower":30,"upper":70}`.

**Long:** Raw %K crosses strictly above SMA3(%K), previous K <= previous D, and current K < 30. **Short:** Raw %K crosses strictly below SMA3(%K), previous K >= previous D, and current K > 70.

**Confirmation/entry:** Completed signal bar i; enter at the next one-minute open at the signal bar start timestamp plus its full timeframe. Never enter within signal bar. **Filters:** Other asset latest completed 15m close > its EMA50 for long, < EMA50 for short (BTC checks ETH and ETH checks BTC).

**Initial stop:** 0.3800% of entry = 40% of approximate bust distance. Long E×(1−0.0038000); short E×(1+0.0038000). **Main target:** net 3 R per target leg; gross price move **BTC 1.313190%, ETH 1.321291%**, favorable direction from entry. Open two independent positions simultaneously with 50% of total margin each. First target earns net 1 initial R on that leg; second target earns net 3 initial R on that leg. For either surviving leg, a completed one-minute close at +1 initial stop raises stop to entry next minute; at +1.5 stops raises it to close minus 0.75 initial stop next minute. Never lower a stop. This emulates scale-out; no native partial close is assumed.

Half-margin first-leg targets: BTC 0.451015%, ETH 0.458624% favorable move; headline main target is the second leg.

**Time stop:** 45 minutes, at open after exactly that many complete one-minute holding candles. **Do not trade:** Skip non-confirmed or missing candles, NaN required features, absent trigger/filter, entry open >0.10% away from signal close, an already open position in that asset, or insufficient complete execution horizon before a split. Operational veto: stale BBO, changed payout settings, unavailable/rejected close service, paused/retired market, queue/cash uncertainty, or actual displayed bust inside planned stop. Operational vetoes were not backtested.

**Pooled OOS:** 353 trades; win 51.6%; mean -0.058 R; PF 0.793; realized DD 25.43 R; bust 0.28%. Initial-training winner: 246 trades, mean 0.059 R (not headline). **BTC:** 186 trades; win 54.3%; mean -0.014 R; PF 0.939; realized DD 5.32 R; bust 0.00%. **ETH:** 167 trades; win 48.5%; mean -0.108 R; PF 0.686; realized DD 20.30 R; bust 0.60%.

| Fold | Fixed trades | Win | Mean R | PF | DD R | Bust | Rolling-selected mean R (trades) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 84 | 52.4% | -0.107 | 0.690 | 12.89 | 1.19% | -0.107 (84) |
| 2 | 73 | 54.8% | -0.029 | 0.884 | 7.28 | 0.00% | -0.071 (77) |
| 3 | 103 | 48.5% | -0.069 | 0.743 | 8.47 | 0.00% | -0.046 (203) |
| 4 | 93 | 51.6% | -0.026 | 0.902 | 10.63 | 0.00% | 0.061 (32) |

Three-day joint-asset bootstrap 95% interval for mean: **[-0.122, 0.006] R**. Bonferroni/HAC lower bound -0.221 R; adjusted one-sided p=1.000. 
Continuous neighborhood: 0/6 eligible ±10% variants positive; median -0.058 R, worst -0.074 R. **No positive plateau demonstrated; fragile or persistently nonpositive.**

### 10. Volume — 3m

**Parameters:** `{"volume_sma":30,"volume_multiple":1.5,"body_return_threshold":0.0005}`.

**Long:** Base-asset volume > 1.5 × SMA30(volume), including current bar; close/open - 1 > 0.0005. **Short:** Base-asset volume > 1.5 × SMA30(volume), including current bar; close/open - 1 < -0.0005.

**Confirmation/entry:** Completed signal bar i; enter at the next one-minute open at the signal bar start timestamp plus its full timeframe. Never enter within signal bar. **Filters:** Monday-Friday, entry UTC hour 08 through 11 inclusive. Latest completed UTC 1h close > its EMA100 and that EMA100 > its value five hourly bars earlier for long; both inequalities reversed for short. One-minute ATR14/entry open, calculated through the previous minute, × 3 <= initial stop fraction; current ATR fraction percentile in [10%,80%] against the preceding 480 ATR fractions (strictly lower ranks / 480). This is a volatility proxy, not a measured adverse-excursion bound.

**Initial stop:** 0.3800% of entry = 40% of approximate bust distance. Long E×(1−0.0038000); short E×(1+0.0038000). **Main target:** net 3 R per target leg; gross price move **BTC 1.313190%, ETH 1.321291%**, favorable direction from entry. After a completed one-minute close reaches +1 initial stop, raise the stop to entry from the next minute. Never lower it. No trailing or partial exits.

**Time stop:** 45 minutes, at open after exactly that many complete one-minute holding candles. **Do not trade:** Skip non-confirmed or missing candles, NaN required features, absent trigger/filter, entry open >0.10% away from signal close, an already open position in that asset, or insufficient complete execution horizon before a split. Operational veto: stale BBO, changed payout settings, unavailable/rejected close service, paused/retired market, queue/cash uncertainty, or actual displayed bust inside planned stop. Operational vetoes were not backtested.

**Pooled OOS:** 187 trades; win 41.7%; mean -0.034 R; PF 0.897; realized DD 13.74 R; bust 0.00%. Initial-training winner: 143 trades, mean 0.060 R (not headline). **BTC:** 93 trades; win 39.8%; mean -0.074 R; PF 0.755; realized DD 8.83 R; bust 0.00%. **ETH:** 94 trades; win 43.6%; mean 0.004 R; PF 1.012; realized DD 10.75 R; bust 0.00%.

| Fold | Fixed trades | Win | Mean R | PF | DD R | Bust | Rolling-selected mean R (trades) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 45 | 40.0% | 0.002 | 1.005 | 5.31 | 0.00% | 0.002 (45) |
| 2 | 50 | 48.0% | 0.100 | 1.336 | 8.70 | 0.00% | -0.165 (50) |
| 3 | 45 | 48.9% | 0.020 | 1.073 | 3.88 | 0.00% | -0.028 (53) |
| 4 | 47 | 29.8% | -0.264 | 0.388 | 13.06 | 0.00% | -0.035 (41) |

Three-day joint-asset bootstrap 95% interval for mean: **[-0.170, 0.112] R**. Bonferroni/HAC lower bound -0.393 R; adjusted one-sided p=1.000. 
Continuous neighborhood: 0/6 eligible ±10% variants positive; median -0.037 R, worst -0.063 R. **No positive plateau demonstrated; fragile or persistently nonpositive.**

Coarse parameter-spike checks (same filter and remaining settings; adjacent parameter variant changes a prescribed parameter bundle):

| Setup | Neighbor parameter / TF / exit means R | Narrow positive indicator spike? |
|---|---|---|
| Bollinger | k=0, TF=1m, exit=7: -0.132 (374 trades); k=2, TF=1m, exit=7: -0.100 (204 trades); k=1, TF=3m, exit=7: 0.015 (129 trades); k=1, TF=1m, exit=6: -0.107 (334 trades); k=1, TF=1m, exit=8: -0.107 (334 trades) | no positive spike identified |
| Moving averages | k=1, TF=5m, exit=7: -0.094 (253 trades); k=2, TF=3m, exit=7: 0.014 (273 trades); k=2, TF=15m, exit=7: 0.071 (72 trades); k=2, TF=5m, exit=6: -0.149 (170 trades); k=2, TF=5m, exit=8: -0.155 (170 trades) | no positive spike identified |
| MA ribbon | k=1, TF=3m, exit=11: -0.090 (239 trades); k=2, TF=1m, exit=11: -0.109 (430 trades); k=2, TF=5m, exit=11: -0.158 (93 trades); k=2, TF=3m, exit=10: -0.107 (130 trades) | no positive spike identified |
| SuperTrend | k=1, TF=60m, exit=9: -0.184 (128 trades); k=0, TF=15m, exit=9: -0.060 (697 trades); k=0, TF=60m, exit=8: -0.053 (157 trades); k=0, TF=60m, exit=10: -0.059 (157 trades) | YES |
| Ichimoku | k=1, TF=3m, exit=7: -0.080 (292 trades); k=0, TF=1m, exit=7: -0.089 (1100 trades); k=0, TF=5m, exit=7: -0.122 (279 trades); k=0, TF=3m, exit=6: -0.108 (456 trades); k=0, TF=3m, exit=8: -0.123 (455 trades) | no positive spike identified |
| TD Sequential | k=0, TF=3m, exit=7: -0.026 (490 trades); k=2, TF=3m, exit=7: -0.032 (156 trades); k=1, TF=1m, exit=7: -0.033 (765 trades); k=1, TF=5m, exit=7: -0.078 (141 trades); k=1, TF=3m, exit=6: -0.037 (279 trades); k=1, TF=3m, exit=8: -0.037 (279 trades) | no positive spike identified |
| RSI | k=1, TF=1m, exit=7: -0.098 (120 trades); k=0, TF=3m, exit=7: 0.021 (93 trades); k=0, TF=1m, exit=6: -0.170 (266 trades); k=0, TF=1m, exit=8: -0.171 (265 trades) | no positive spike identified |
| MACD | k=1, TF=15m, exit=7: -0.117 (420 trades); k=2, TF=5m, exit=7: -0.078 (657 trades); k=2, TF=60m, exit=7: -0.028 (64 trades); k=2, TF=15m, exit=6: -0.139 (270 trades); k=2, TF=15m, exit=8: -0.134 (270 trades) | no positive spike identified |
| Stochastic | k=1, TF=15m, exit=11: -0.064 (292 trades); k=0, TF=5m, exit=11: -0.040 (1438 trades); k=0, TF=60m, exit=11: -0.188 (32 trades); k=0, TF=15m, exit=10: -0.055 (391 trades) | no positive spike identified |
| Volume | k=1, TF=3m, exit=7: 0.016 (88 trades); k=0, TF=1m, exit=7: -0.034 (317 trades); k=0, TF=5m, exit=7: 0.103 (115 trades); k=0, TF=3m, exit=6: 0.067 (181 trades); k=0, TF=3m, exit=8: 0.053 (181 trades) | no positive spike identified |
| SuperTrend + Stochastic | k=0, TF=15m, exit=8: -0.077 (129 trades); k=2, TF=15m, exit=8: -0.096 (172 trades); k=1, TF=5m, exit=8: -0.024 (382 trades); k=1, TF=60m, exit=8: -0.084 (39 trades); k=1, TF=15m, exit=7: -0.084 (179 trades); k=1, TF=15m, exit=9: -0.088 (179 trades) | no positive spike identified |
| Ichimoku + MACD | k=0, TF=3m, exit=7: -0.187 (329 trades); k=2, TF=3m, exit=7: -0.179 (162 trades); k=1, TF=1m, exit=7: -0.151 (504 trades); k=1, TF=5m, exit=7: -0.171 (169 trades); k=1, TF=3m, exit=6: -0.185 (210 trades); k=1, TF=3m, exit=8: -0.184 (210 trades) | no positive spike identified |
| Bollinger + RSI + Volume | k=1, TF=3m, exit=5: -0.053 (440 trades); k=2, TF=1m, exit=5: -0.069 (753 trades); k=2, TF=5m, exit=5: -0.056 (116 trades); k=2, TF=3m, exit=4: -0.044 (236 trades); k=2, TF=3m, exit=6: -0.078 (239 trades) | no positive spike identified |

In particular, SuperTrend’s ATR10 × 2.5 adjacent variant loses −0.184 R; its 15m counterpart and neighboring exit packages also lose. Its mild exit-only plateau is not broad parameter robustness. Positive neighbors such as Volume 5m (+0.103 R/115 trades) are post-hoc observations, not replacements for the frozen setting; promoting them would spend the same holdout again. Their full fold eligibility, execution sensitivity and multiplicity-adjusted evidence were not established here.

## Combinations and selectivity

| Setup | TF | OOS trades | Win | Mean net R | PF | Realized max DD R | Bust | Eligible |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| SuperTrend + Stochastic | 15m | 172 | 41.9% | -0.125 | 0.523 | 24.43 | 0.00% | yes |
| Ichimoku + MACD | 3m | 256 | 39.1% | -0.200 | 0.508 | 54.44 | 0.00% | yes |
| Bollinger + RSI + Volume | 3m | 226 | 54.4% | -0.043 | 0.805 | 17.20 | 0.88% | yes |

**SuperTrend + Stochastic (15m):** long: SuperTrend is up, AND Raw %K crosses strictly above SMA3(%K), previous K <= previous D, and current K < 30. Short: SuperTrend is down, AND Raw %K crosses strictly below SMA3(%K), previous K >= previous D, and current K > 70. Parameters `{"direction":{"wilder_atr":10,"multiplier":2.5},"timing":{"raw_k_period":14,"d_sma":3,"lower":30,"upper":70}}`. Filter: One-minute ATR14/entry open, calculated through the previous minute, × 3 <= initial stop fraction; current ATR fraction percentile in [10%,80%] against the preceding 480 ATR fractions (strictly lower ranks / 480). This is a volatility proxy, not a measured adverse-excursion bound. Stop 0.2375%; main targets BTC 0.828341%, ETH 0.836285%; time 20 minutes. After a completed one-minute close reaches +1.5 initial stops, raise the stop to that close minus 0.75 initial stop in directional-return coordinates; effective next minute. Never lower it. No partial exits. Same next-open and veto conventions apply.

Fold results: F1 32 trades; win 50.0%; mean 0.067 R; PF 1.397; realized DD 2.00 R; bust 0.00%; F2 47 trades; win 40.4%; mean -0.096 R; PF 0.627; realized DD 4.59 R; bust 0.00%; F3 45 trades; win 37.8%; mean -0.218 R; PF 0.323; realized DD 10.76 R; bust 0.00%; F4 48 trades; win 41.7%; mean -0.192 R; PF 0.283; realized DD 9.93 R; bust 0.00%.

**Ichimoku + MACD (3m):** long: Tenkan > kijun and close > displayed cloud top, AND (EMA8-EMA21) minus its EMA5 crosses strictly above zero; previous histogram <= 0. Short: Tenkan < kijun and close < displayed cloud bottom, AND (EMA8-EMA21) minus its EMA5 crosses strictly below zero; previous histogram >= 0. Parameters `{"direction":{"tenkan":9,"kijun":26,"span_b":52,"displacement":26},"timing":{"fast_ema":8,"slow_ema":21,"signal_ema":5}}`. Filter: Monday-Friday, entry UTC hour 12 through 19 inclusive. One-minute ATR14/entry open, calculated through the previous minute, × 3 <= initial stop fraction; current ATR fraction percentile in [10%,80%] against the preceding 480 ATR fractions (strictly lower ranks / 480). This is a volatility proxy, not a measured adverse-excursion bound. Stop 0.3800%; main targets BTC 1.313190%, ETH 1.321291%; time 45 minutes. After a completed one-minute close reaches +1 initial stop, raise the stop to entry from the next minute. Never lower it. No trailing or partial exits. Same next-open and veto conventions apply.

Fold results: F1 55 trades; win 38.2%; mean -0.208 R; PF 0.492; realized DD 14.45 R; bust 0.00%; F2 66 trades; win 39.4%; mean -0.108 R; PF 0.696; realized DD 11.95 R; bust 0.00%; F3 64 trades; win 45.3%; mean -0.122 R; PF 0.669; realized DD 8.14 R; bust 0.00%; F4 71 trades; win 33.8%; mean -0.349 R; PF 0.276; realized DD 26.27 R; bust 0.00%.

**Bollinger + RSI + Volume (3m):** long: Low <= SMA28 - 2.3 × population SD28; close > that lower band and close > open. RSI21 is rising and < 50; volume > 2.5 × SMA30(volume). Short: High >= SMA28 + 2.3 × population SD28; close < that upper band and close < open. RSI21 is falling and > 50; volume > 2.5 × SMA30(volume). Parameters `{"bollinger":{"period":28,"population_sd_multiple":2.3},"rsi":{"wilder_rsi":21,"lower":35,"upper":65},"volume":{"sma":30,"multiple":2.5}}`. Filter: Latest completed UTC 1h close > its EMA100 and that EMA100 > its value five hourly bars earlier for long; both inequalities reversed for short. Stop 0.5700%; main targets BTC 1.959537%, ETH 1.967730%; time 45 minutes. No break-even, trailing or partial exits. Same next-open and veto conventions apply.

Fold results: F1 50 trades; win 46.0%; mean -0.154 R; PF 0.469; realized DD 8.19 R; bust 2.00%; F2 62 trades; win 54.8%; mean -0.083 R; PF 0.713; realized DD 9.18 R; bust 1.61%; F3 58 trades; win 53.4%; mean -0.045 R; PF 0.730; realized DD 5.03 R; bust 0.00%; F4 56 trades; win 62.5%; mean 0.102 R; PF 1.715; realized DD 4.32 R; bust 0.00%.

All three pairs and all three triples were searched, including **EMA + RSI**, **SuperTrend + Stochastic**, **Ichimoku + MACD**, **Bollinger + RSI + Volume**, **Ribbon + RSI + Volume**, and **EMA + TD + Volume**. A family absent from the table had no first-fold candidate meeting ≥100 training trades and ≥20 per asset; it has no eligible fixed setting, not a fabricated zero-return result. Best-case sparse examples remain in the training audit. Selectivity can make a training spike look strong with little evidence. These combinations are not additions to the ten standalone return series.

## Stability, costs and multiple testing

Continuous neighborhood tests perturb one exit dimension at a time: stop fraction ±10%, net target multiple ±10%, and TTL ±10% rounded to minutes (so a 3-minute TTL can map back to itself). All other rules stay frozen. Coarse adjacent indicator variants, timeframes and exit packages are separately retained. A positive plateau label requires at least four eligible continuous neighbors, with ≥2/3 positive; it is a descriptive criterion, not a selection-adjusted discovery test. The playbook prefers agreement across exit and indicator neighborhoods; where none qualifies it identifies the raw best result explicitly as fragile. [Neighborhood heatmap](../research/robustness.svg).

| Setup | Base | Off hours | 1bp/side | 2bp/side | 5bp/side | 10bp/side | Delay 1m | Delay 2m | Impact ×1.25 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Bollinger | -0.093 | -0.095 | -0.142 | -0.197 | -0.330 | -0.581 | -0.087 | -0.092 | -0.103 |
| Moving averages | -0.063 | -0.065 | -0.106 | -0.161 | -0.301 | -0.577 | -0.076 | -0.067 | -0.074 |
| MA ribbon | -0.031 | -0.032 | -0.080 | -0.132 | -0.294 | -0.558 | -0.027 | -0.034 | -0.045 |
| SuperTrend | 0.009 | 0.007 | -0.038 | -0.089 | -0.239 | -0.478 | 0.010 | 0.019 | -0.004 |
| Ichimoku | -0.120 | -0.122 | -0.164 | -0.215 | -0.353 | -0.591 | -0.117 | -0.115 | -0.130 |
| TD Sequential | -0.023 | -0.025 | -0.088 | -0.137 | -0.277 | -0.543 | -0.023 | -0.016 | -0.034 |
| RSI | -0.117 | -0.118 | -0.166 | -0.223 | -0.360 | -0.589 | -0.112 | -0.104 | -0.126 |
| MACD | -0.137 | -0.139 | -0.185 | -0.241 | -0.388 | -0.630 | -0.128 | -0.125 | -0.146 |
| Stochastic | -0.058 | -0.061 | -0.104 | -0.157 | -0.303 | -0.530 | -0.054 | -0.047 | -0.069 |
| Volume | -0.034 | -0.036 | -0.080 | -0.123 | -0.265 | -0.530 | -0.026 | -0.014 | -0.047 |
| SuperTrend + Stochastic | -0.125 | -0.130 | -0.195 | -0.263 | -0.514 | -0.917 | -0.135 | -0.134 | -0.132 |
| Ichimoku + MACD | -0.200 | -0.201 | -0.242 | -0.281 | -0.432 | -0.652 | -0.210 | -0.193 | -0.209 |
| Bollinger + RSI + Volume | -0.043 | -0.045 | -0.072 | -0.105 | -0.195 | -0.349 | -0.039 | -0.042 | -0.051 |

Cells are mean net R per trade; exact counts, PF, DD and bust rates for every scenario are in the JSON, including builder 0.5%, bust 0.90/1.00%, and ideal-stop-first. Stressed target levels remain baseline targets; they are not retuned to restore profitability. Delay can improve an individual sample by chance; it is not a promised execution advantage.

Uncertainty uses 2,500 seeded circular three-day block resamples of the 84 OOS days, resampling BTC/ETH jointly with random trade-count denominator. This addresses some intraday and cross-asset dependence, not regime changes. The multiple-testing view uses daily centered PnL/count estimating functions, Newey-West lag 2 standard error, a normal one-sided tail, and Bonferroni over **138,240** configuration-window comparisons. The familywise lower bound is mean minus the corresponding normal critical value × HAC SE. Correlated trials do not invalidate Bonferroni’s union bound if individual tests are valid, but **normal/HAC calibration here is approximate**, and the repeated prior study/meta-search is not fully quantifiable. This is a multiple-testing-aware diagnostic, not a formal proof or a deflated-Sharpe claim.

Rolling-refit pooled means versus fixed settings:

| Setup | Fixed mean R | Rolling mean R | Rolling trades |
|---|---:|---:|---:|
| Bollinger | -0.093 | -0.080 | 198 |
| Moving averages | -0.063 | -0.040 | 199 |
| MA ribbon | -0.031 | 0.008 | 204 |
| SuperTrend | 0.009 | -0.076 | 201 |
| Ichimoku | -0.120 | -0.102 | 240 |
| TD Sequential | -0.023 | -0.054 | 177 |
| RSI | -0.117 | -0.048 | 240 |
| MACD | -0.137 | -0.042 | 231 |
| Stochastic | -0.058 | -0.055 | 396 |
| Volume | -0.034 | -0.059 | 189 |
| SuperTrend + Stochastic | -0.125 | -0.046 | 151 |
| Ichimoku + MACD | -0.200 | -0.079 | 242 |
| Bollinger + RSI + Volume | -0.043 | -0.102 | 189 |

The rolling numbers assess the fitting procedure, not the final fixed setting. Full per-fold configs and statistics are in `best-settings.json`; no last-fold setting is represented as having been known in earlier folds. Changing rules again based on these results requires fresh future data.

## Mandatory-100x playbook

**Research-only observation candidates:** **SuperTrend** (60m, 0.009 R/trade). These are the best observed eligible candidates after checking continuous and indicator neighborhoods; none clears the broad-robustness gates; they are not certified profitable trades. Use only their exact rules above / in the JSON. Do not combine signals into a new untested rule. If both assets signal simultaneously, choose the earliest timestamp and BTC on a tie; this is a declared risk policy, not a backtested portfolio.

**Sizing:** total isolated margin per strategy trade = **0.10% of initial spendable cash account equity**, always exactly 100x. Notional = 10% of that equity. For two-position emulated scale-out, each leg gets 0.05% equity margin, not 0.10% each. A normal stop risks 100×stop×0.10% equity (0.01425–0.05700% for the tested stop menu); a full bust loses the entire 0.10%. At most one strategy trade open across both assets; never reuse queued claims as cash equity, add margin, average down, or increase size after losses. If venue minimums make this size impossible, skip; do not silently upscale.

**Frequency:** at most **two trades per asset per UTC day, four total**, only during the selected setup’s eligible hours. Trade both BTC and ETH when their own valid signals occur; there is no assumed obligation to force a signal every day. Required market participation without any valid signal is outside the tested playbook. Observed uncapped frequencies: SuperTrend 1.87 pooled trades/day.

**Loss limits and stopping:** stop new entries and close remaining risk at a **0.30% day-start cash-equity loss**, including open marked loss; stop for the week at **1% cash-equity loss**. These are loss-trigger actions, not guaranteed caps through gaps/outages. An unexpected bust, rejected/delayed close, stale BBO, payout/bust-setting change, retirement, or uncertain cash/queue status triggers an immediate halt and execution audit. Pause for prospective review if the last 20 trades average below −0.10 R, or the last 50 average <=0. Those monitoring cutoffs are design judgments; they are not calibrated significance tests. **Do not increase trade count or size to recover losses.**

The daily caps, one-asset rule, sizing and monitoring policy are **not backtested together**; their performance cannot be inferred from the unconstrained per-setup tables. They limit the amount put at risk under a requirement to use 100x. No setup establishes a robust positive edge at 100x in this study. Confidence is materially stronger in the limitations of this test than in any positive raw cell. Only prospective, timestamped Papertrade BBO/intent/fill/queue records with frozen rules could resolve the execution and independence gaps.

## Unanswered questions and checks

Unknown: exact live per-market payout constants and rounding, short bust formula, curve-mode history, builder attribution changes, BBO/trade-feed basis during stress, relayer latency and guaranteed protective-close support, rejected opens, historical queue/cash state, minimum position sizes, and realizable PAPER value. Public OHLC cannot recover these. An exchange or relayer outage can make actual losses much worse than a planned stop; our assumed hard-bust cap is isolated-margin economics, not a guarantee against custody/protocol failure.

No trade was sent. No account, key or requester-specific address was needed. Source pages were re-fetched successfully by the acquisition script; page hashes/status/timestamps are in `sources/documentation-manifest.json`. Local tests check native hashes/continuity, aggregation, payout examples and monotonicity, target inversion, prefix invariance, both-side stop/gap/bust handling, pending-close timing and split boundaries. Further ledger checks reconcile trade counts, cash R and drawdowns to the named outputs. **Author-run checks have no independent authority; path/byte verification does not validate this research.**

**Compact offline runtime:** the original numerical search used NumPy/Numba. Its source is retained as historical reference; the delivered executable runtime uses only Python standard-library scalar operations. Exact original CSV bytes, all 138,240 training records, the selection lock, trade ledger and one-minute equity paths are preserved. `check` tests payout and causal engine behavior, `verify` reconciles the records, and `replay` recomputes every frozen baseline choice and marked drawdown. `search` recomputes all training scores without network access but is substantially slower than the original accelerated run. Frozen sensitivity/bootstrap records remain original measured outputs; they are not newly independently validated by this packaging repair.

Offline reproduction and limits are in [README](../README.md). Supporting code, losslessly packed data, search audits, frozen choices and trade ledger are ordinary repository files outside `artifacts/`. The deliverables are this report and `artifacts/best-settings.json`.
