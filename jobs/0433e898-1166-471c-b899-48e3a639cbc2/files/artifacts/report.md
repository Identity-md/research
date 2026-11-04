# ERL-100 for ETH on Papertrade: frozen settings, failed holdout

**Finding:** no positive edge survived the final holdout on any timeframe. **3m (180 seconds) is the single best of the four frozen development-selected settings**, meaning least negative: **−0.0643 R/trade, 82 trades, PF 0.9149** before added execution cost; **−0.1266 R/trade** with 1 bp adverse execution **on each side**. This is a research configuration, not evidence supporting profitable deployment. Keep the failed results visible beside the settings.

All headline results below use **2026-08-01 00:00 UTC inclusive to 2026-11-01 00:00 UTC exclusive**: 92 calendar days, 91 observed days. Parameters were frozen before holdout performance was read. Every timeframe exceeds the requested 60 completed holdout trades. No holdout result, sensitivity, or later development control was used to change the frozen parameters.

## Holdout results — the headline

| Timeframe | Trades | Win rate | Mean R | PF (R units) | Max DD, R | Bust rate | 1 bp/side mean R |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1m | 84 | 27.38% | -0.2362 | 0.6711 | 21.44 | 0.00% | -0.3607 |
| 3m | 82 | 24.39% | -0.0643 | 0.9149 | 24.04 | 0.00% | -0.1266 |
| 5m | 88 | 18.18% | -0.2238 | 0.6253 | 22.65 | 0.00% | -0.3195 |
| 15m | 106 | 22.64% | -0.1381 | 0.8215 | 32.65 | 0.00% | -0.1890 |

**Definitions:** a win has strictly positive settled modeled PnL; zero is not a win. `R = net PnL / original entry-to-stop cash risk`. Stops can gap past −1 R; full bust is the whole isolated margin. `profitFactor` in the settings and all search tables is **sum of positive R / absolute sum of negative R**. Drawdown is peak-to-trough cumulative closed-trade R starting at zero; it is not an intrabar equity drawdown or an account-return percentage. From/to are the fixed evaluation window, not the first/last trade timestamps. All modeled winning claims are assumed paid for accounting; actual paid cash was not observed.

| Timeframe | Conventional PF at equal isolated margin | Mean PnL / margin per trade | 7-day block-bootstrap 95% interval for mean R |
| --- | --- | --- | --- |
| 1m | 0.6595 | -3.48% | [-0.511, 0.033] |
| 3m | 0.9329 | -1.14% | [-0.457, 0.454] |
| 5m | 0.6699 | -2.99% | [-0.411, -0.025] |
| 15m | 0.8040 | -3.39% | [-0.416, 0.179] |

The second PF convention weights each trade by its modeled fixed-margin cash PnL rather than its stop-normalized R. It also stays below one on every timeframe. Intervals use 10,000 deterministic circular calendar-day block resamples, block length seven days, with daily trade counts retained in the ratio. They are descriptive, do not adjust for search or four-timeframe comparison, and cannot establish stationarity. The missing day contributes no invented trades; uncertainty across that unobserved day is not recovered by bootstrap.

### Holdout exit counts

| TF | STOP | TARGET | TIME | FRONTIER_FAIL | MANAGED_STOP | BUST | GAP_RISK | Unresolved |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1m | 60 | 16 | 8 | 0 | 0 | 0 | 0 | 0 |
| 3m | 62 | 20 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5m | 27 | 8 | 8 | 45 | 0 | 0 | 0 | 0 |
| 15m | 82 | 23 | 1 | 0 | 0 | 0 | 0 | 0 |

All selected configurations have zero unresolved positions at the end and zero entries rejected by the base fill assessment. `BUST_STRESS` is also zero. These zeros describe this data and hypothetical execution model; they do not imply guaranteed stop protection. No selected trade was exposed to the missing day. A position crossing a missing interval would receive a separately labeled `GAP_RISK` full-margin worst-case charge, not a fabricated observed liquidation.

## Data and attributable evidence

**Observed:** downloaded Binance **USD-M perpetual ETHUSDT 1m klines**, January–October 2026, on 2026-11-04 UTC. There are **436,320 validated one-minute rows**, or 303 observed days in a 304-day calendar span. Each downloaded ZIP matched its published SHA-256 checksum. Binance identifies USD-M archive klines as `/fapi/v1/klines` data and supplies companion checksum files in its [public-data documentation](https://github.com/binance/binance-public-data#futures). The [January archive](https://data.binance.vision/data/futures/um/monthly/klines/ETHUSDT/1m/ETHUSDT-1m-2026-01.zip) through the [October archive](https://data.binance.vision/data/futures/um/monthly/klines/ETHUSDT/1m/ETHUSDT-1m-2026-10.zip) are the actual sources; all ten exact URLs and digests are retained in `research/data/manifest.json`, and the normalized CSV is included losslessly as `research/data/eth-1m.csv.xz` for offline reproduction. Redundant source ZIPs are omitted to fit the upload limit. The offline verifier checks the decompressed CSV against its recorded SHA-256 and validates every candle and monthly coverage; it cannot independently recheck the omitted ZIP bytes or their derivation. `research/download.py` can reacquire and verify those original archives online.

Normalized CSV SHA-256: `45a21af41c42117761652e5bdc020b351442885ea8987bcfe9c96e41a2c666a2`.

**Observed access limits:** Hyperliquid candleSnapshot returned recent candles but could not supply the requested 120-day one-minute history; its [API documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint#candle-snapshot) limits availability to the most recent 5,000 candles, about 3.47 days at 1m. OKX history-candles returned HTTP 403 here. Binance was the usable historical fallback. This is not a claim that Binance candles equal Papertrade execution prices.

**Observed data limitation:** October 28 is missing from the October archive; the corresponding daily archive request returned 404. The gap runs from the last open at 2026-10-27 23:59 to the next at 2026-10-29 00:00. No interpolation, carry-forward, or replacement feed was used. Duplicate timestamps, invalid OHLC, and incomplete aggregate buckets are rejected. Missing intervals reset candle/ledger history. 3m, 5m and 15m OHLCV are aggregated from complete one-minute groups aligned to UTC epoch boundaries: first open, highest high, lowest low, last close, summed volume. The normalized timestamps are bar opens in Unix seconds. No BTC confirmation was used.

**Economics/specification source:** the supplied [papertradeResearch artifact](https://api.imd.fun/artifacts/6e8652275deb7261fcc223d0cbcb13342ab70f0f84d1a3063dff85857a9af858), sections 2, 4 and 5. Its exact bytes are retained as `research/papertrade-research-input.md`; SHA-256 `6e8652275deb7261fcc223d0cbcb13342ab70f0f84d1a3063dff85857a9af858`. Direct attempts to re-read the current Papertrade docs returned HTTP 403/access errors. Therefore economics are the **supplied documented scenario**, not an onchain verification or a current executable quote. Relevant primary pages are [impact](https://docs.papertrade.xyz/how/asymmetric-impact/), [fees](https://docs.papertrade.xyz/learn/wins-losses/), [liquidations](https://docs.papertrade.xyz/learn/liquidations/), and [position restrictions](https://docs.papertrade.xyz/learn/trades-pricing/). Those claims below are attributed to the supplied research transcription of these pages, not a successful new fetch.

The requester’s OKX reference runs (1m −0.126 R; 5m −0.174 R) are reported inputs, not independently reproduced results. This project implements section 4 independently; the earlier reference source code was not supplied. The independent default comparison below uses the same Binance dates and this engine, with default numerical thresholds and the entry-timeframe policy extended to 3m/15m as required here, so differences from the requester’s runs cannot be attributed solely to tuning.

## Economics and execution assumptions

Leverage is exactly **100×** throughout. With isolated margin M, notional is 100M. For favorable fractional move p, the model computes the following per-notional payout, then multiplies by 100 to obtain profit / margin:

```text
H = k*(z-a)*u^2*(1-u)^n inside a < p < z, else 0
u = (p-a)/(z-a)
standard (a,z,k,n) = (0.000075,0.0006,3.597,2)
off-hours          = (0.00003,0.001,6.085,3)
q = max(0,p-0.00002-H)
S = 0.9 / (1 + 1/(q*15000) + 100000/(1e6*q*483.979))
G_mode = q*S*(1-0.02-builderFee), or 0 when q=0
G = min(G_standard,G_offHours)
```

Use the worse curve **at every planned target and realized winning exit**, not a guessed off-hours schedule. The primary papertrade.xyz scenario uses 2% win fee after impact, builder fee zero; an additional 0.5% builder sensitivity is reported. Losses are full signed 100× price moves, without profit impact or a loss fee. No exchange funding or Binance transaction fee is added because Binance supplies proxy prices, not the execution venue. No PAPER value, dividends, or queue-discount income is credited. Economic constants are documentation defaults; actual active parameters, fixed-point rounding and builder attribution remain unverified.

Approximate historical bust is a **0.0095 adverse fraction of entry** on either side and costs 100% of margin. A voluntary execution at/past that boundary also busts. Entry requires the stop to remain more than 0.003 of entry inside this approximate bust boundary. Operational eligibility must instead use the actual position/quote `bustPrice`; approximate history is not a contract invariant.

Entries are attempted only at the next timeframe bar open after the confirmation closes. Reference entry is the confirmation close. Reject more than 0.0002 absolute relative entry drift, entry at/past stop, or any re-evaluated risk/coverage/netRR/ERL failure. Keep the raw stop fixed; recompute stop fraction, target, upper coverage and payout gates using actual modeled fill and the **frozen confirmation-time ledger**. The stop pad uses the reference close, not a later price. A 0.0002 latency reserve enters the entry risk budget; it is not a cash fee subtracted again from every realized trade.

Exit checks use the underlying **1m** bars for all signal timeframes. Process gaps at the minute open first; a bust gap overrides a stop, a stop gap exits at the adverse open, and favorable target gaps receive only the target price. A previously requested structural/time market exit fills at the next timeframe open, subject to bust/stop checks. Within each minute, use stop-first if stop and target are both touched. The main result assumes a functioning hypothetical standing stop before a deeper intraminute bust; the full-bust sensitivity replaces a stop with full bust when that minute can reach bust. Unknown ordering inside one minute, relayer failure, and basis spikes remain unresolved.

The required execution sensitivity fills entry at `open*(1+s*0.0001)` and exit at `exitLevel*(1-s*0.0001)`, with s=+1 long and −1 short. It reruns fill eligibility and cooldown, so it can skip/change subsequent trades. Builder-fee sensitivity changes realized winning payouts on otherwise frozen opportunities; it does not optimize a new gate profile. Open trades at a window end are censored and counted unresolved, never force-closed favorably; each fold starts flat with historical warmup allowed.

## Exact selected parameters

All four choices retain the **24 pre-sweep bars and 12-bar closing frontier**. Price-distance fields are fractions, never percent: 0.001 = 10 bps. Window/hold/cooldown fields are integers, targetRiskMultiple/netRR/budget are dimensionless, and support/obstacle thresholds are coverage fractions. `erl-eth-settings.json` contains exactly the requested parameter field names, no added aliases. Its `best` is the string `"180"`, usable as a key into `timeframes`.

| Parameter | 1m / 60 | 3m / 180 | 5m / 300 | 15m / 900 |
| --- | --- | --- | --- | --- |
| ledgerBars | 24 | 24 | 24 | 24 |
| frontierBars | 12 | 12 | 12 | 12 |
| sweepMin | 0.0003 | 0.0003 | 5e-05 | 0.0001 |
| sweepMax | 0.0015 | 0.006 | 0.0015 | 0.006 |
| reclaimBuffer | 5e-05 | 5e-05 | 0.0 | 0.0001 |
| confirmMin | 0.0 | 0.0 | 5e-05 | 0.0 |
| stopPad | 0.0003 | 0.0005 | 0.0005 | 0.0002 |
| riskMin | 0.0003 | 0.0005 | 0.0003 | 0.001 |
| riskMax | 0.002 | 0.006 | 0.0045 | 0.0035 |
| rangeMax | 0.003 | 0.003 | 0.008 | 0.008 |
| targetRiskMultiple | 4.0 | 4.0 | 5.0 | 4.0 |
| targetMin | 0.0015 | 0.0015 | 0.003 | 0.0015 |
| targetMax | 0.004 | 0.008 | 0.006 | 0.008 |
| supportMin | 0.2 | 0.05 | 0.3 | 0.2 |
| obstacleMax | 0.2 | 0.7 | 0.7 | 0.9 |
| netRRMin | 1.2 | 1.8 | 2.2 | 1.5 |
| budgetMin | 0.05 | 0.2 | 0.6 | 0.1 |
| latencyReserve | 0.0002 | 0.0002 | 0.0002 | 0.0002 |
| maxHoldBars | 48 | 96 | 24 | 96 |
| cooldownBars | 6 | 3 | 6 | 3 |

### Exact long and short entry rules shared by all four

At closed confirmation i, sweep j=i−1, evaluate each permitted side s. Transform prices as `O=s*open`, `C=s*close`, `L=min(s*low,s*high)`, `U=max(...)`. Positive raw close is always the distance denominator, including shorts. Set `F=min(C[k], k=j−12..j−1)`. Require:

1. `sweepMin <= (F−L[j])/close[j] <= sweepMax`; `C[j] >= F + reclaimBuffer*close[j]`; sweep range / close[j] <= rangeMax.
2. `L[i] > L[j]` strictly; `C[i] >= C[j] + confirmMin*close[i]`; `C[i] >= F + reclaimBuffer*close[i]`; confirmation range / close[i] <= rangeMax. A zero confirmation threshold allows equality in close progress, not retouch of the sweep extreme.
3. For each of the 24 bars strictly before j, form lower/upper wick intervals. Subtract every later candle **body** through i; preserve all surviving pieces. Give the oldest cohort bar weight 1/24 and newest 1. Density at each price is the **maximum**, not sum, of surviving weights. Integrate exactly over interval endpoints. `J` is lower-density coverage over `[L[j],F]`; the sweep itself supplies no prior support.
4. At reference E=close[i], set `Sx=L[j]−stopPad*E`, `r=(s*E−Sx)/E`, `p=clamp(targetRiskMultiple*r,targetMin,targetMax)`, `Tx=s*E+p*E`. Raw stop/target are s*Sx and s*Tx. `A` is upper-density coverage over `[s*E,Tx]`.
5. `netRR=G(p)/(r+latencyReserve)` (100× cancels), `ERL=J*(1−A)*netRR`. Require inclusive risk bounds, J>=supportMin, A<=obstacleMax, netRR>=netRRMin, ERL>=budgetMin, plus the filters below. Both sides qualifying is ambiguous and produces no entry. Reassess at next open as described above; a failed setup cannot revive later without a new preceding sweep.

**Long interpretation:** sweep a prior minimum-close frontier with a lower low, reclaim it, then confirm with a strictly higher low and sufficient close progress; stop below that sweep low, target above fill. **Short interpretation:** mirror every condition: sweep above the prior maximum-close frontier, close back below it, confirm a strictly lower high and sufficient downward close progress; stop above the sweep high, target below fill. No future bars enter ledger construction, gates, trend or volatility ranks. Forming bars cannot confirm signals or erase past evidence.

| TF | Allowed long | Allowed short | Decision-time UTC hour | Trend filter | ATR percentile | Closed-bar structural failure |
| --- | --- | --- | --- | --- | --- | --- |
| 1m | Yes | Disabled | 08:00 inclusive–16:00 exclusive | None | 0.10–0.90 inclusive | Disabled (addition) |
| 3m | Disabled | Yes | 08:00 inclusive–16:00 exclusive | Closed 1h close < EMA20 | None | Disabled (addition) |
| 5m | If trend passes | If trend passes | 08:00 inclusive–16:00 exclusive | Long: 1h close > EMA20; short: < | None | Enabled (original) |
| 15m | If trend passes | If trend passes | All hours | Long: 1h close > EMA20; short: < | 0.00–0.75 inclusive | Disabled (addition) |

**Filter additions, exact:** the hour is the UTC hour at **confirmation close**, not the sweep/open or future fill. The hourly filter uses the latest fully closed UTC 1h candle with end <= decision time, age strictly below one hour. EMA20 has alpha 2/21, seeded at the first segment close, includes that latest closed hour, and requires 21 consecutive closed hourly bars; equality/insufficient history rejects. ATR14 is Wilder recursion alpha 1/14, seeded at first segment true range; TR=max(high−low, abs(high−previousClose), abs(low−previousClose)), with high−low on segment start. Compare current ATR14/close against the **previous** up-to-240 bars’ ATR14/close; percentile is count <= current divided by available count. No future/global percentile normalization is used. Reset on gaps. The JSON includes these definitions and numerical thresholds.

Direction/hour/ATR/trend restrictions were candidates on development data only. In 1m, selected long-only earned +0.1485 development R versus +0.0963 both-side and +0.0528 short-only controls. In 3m, short-only +0.1396 was slightly below both-side +0.1448 in raw mean, but window-mean dispersion was 0.1119 versus 0.1581; the declared mean/dispersion/count rank was 0.06668 versus 0.06492. This is weak training justification for a direction restriction, not evidence that ETH structurally favors that direction. Controls were diagnostic and did not cause post-holdout changes.

### Exact exits and additions

One open position per symbol, no pyramiding, no entry/reversal on an exit bar. Freeze raw stop, actual-fill target, frontier and sweep extreme at entry. Stop/target are full closes under the hypothetical execution assumptions above. **None of the four selected settings uses break-even, trailing or partial profit-taking.**

For **5m only**, retain the original structural rule: after any holding bar h closes, if `s*close[h] < F` **or** `s*close[h] <= L[j]`, request full exit for the next bar open. Strict frontier failure and non-strict sweep failure have no extra buffer. This takes precedence over a time request. For **1m, 3m, 15m**, the added exit variant disables **both** structural tests; fixed stop, target and time exit remain. JSON `exits=null` on 5m means inherited original exit rules; other values explicitly state the structural-exit removal.

Time stops request full exit after respectively **48, 96, 24, 96 completed holding bars** on 1m/3m/5m/15m, filled at the following open. Holding bar 1 is the entry bar. This is at most 48 minutes, 288 minutes, 120 minutes, or 1,440 minutes before the next-open request, excluding execution delay. After the exit bar, require respectively **6, 3, 6, 3 full cooldown bars**; earliest new confirmation index is exit index+cooldownBars+1, with fill one bar later. Do not hold past an observed bust to seek token emissions.

Enabling 3m and 15m entry policies at 100× is an explicit extension of the research defaults, which originally allowed 1m/5m. A consumer must enable all four provided timeframe keys rather than retain the old allowed-timeframe guard. The parameter JSON does not introduce an unsupported `allowedEntryTf` parameter.

## Development search and three-fold walk-forward

The chronological development period is **2026-01-01 to 2026-08-01** (212 calendar days). Initial training is Jan–Feb (59 days). Fold 1 trains Jan–Feb and tests Mar–Apr (61 days); fold 2 trains Jan–Apr and tests May–Jun (61 days); fold 3 trains Jan–Jun and tests July (31 days). Each test begins flat; warmup uses earlier observations, and trades extending past the test boundary are unresolved rather than realized by hindsight. Candidate outcomes outside the requested window are never included in selection.

Per timeframe, a deterministic 1,169-configuration broad search includes the reference baseline; a 144-member holding/target/management/failure grid; and 1,024 seeded mixed parameter designs. The broad search varies every requested search field: maxHoldBars, cooldownBars, targetRiskMultiple, targetMin/Max, riskMin/Max, stopPad, sweepMin/Max, reclaimBuffer, confirmMin, rangeMax, supportMin, obstacleMax, netRRMin, budgetMin, ledgerBars and frontierBars. The 2 bp latency reserve stays fixed. Exact designs/seeds are in `research/search.py` and `research/params-*.csv`; this is a finite search, not a claimed global optimum.

Holding options: 4/6/12/24/48/96 bars; cooldown 0/1/3/6/12; targets 1.5–5 times stop with 0.001–0.003 floors and 0.004–0.008 caps; stop bounds up to 0.006, also subject to the 30 bp bust-safety gate. Ledger/frontier pairs include 24/12, 20/10, 28/14, 24/8 and 24/16. Filters include no filter, UTC 00–08/08–16/16–24, hourly trend, ATR rank ranges and permitted direction. Other exact value sets are retained in the design source rather than inferred from winning settings.

Search management variants are: unchanged stop; move stop to original fill only after a closed bar closes at >=+1 original raw-stop R; or trail after that same +1R close, using `stop=max_direction(oldStop, close−s*originalRiskFraction*entry)` after each qualifying close. A new managed stop applies only from the next bar and never widens. Structural exits were tested on/off. These are additions, not part of the core ledger. None won final selection.

A 50% take-profit at 1R and 1.5R was additionally evaluated as a **non-deployable two-leg research control**, with the remainder using the same stop/target/time rules and each leg paying its own winning curve. The supplied platform restrictions prohibit partial closes of a position; it was excluded from eligible site settings rather than pretending it is supported. Its fills use the same stop-first priority, and it never improves the selected configuration’s pooled development mean in these controls. Two-leg controls are additions and are not evidence of a Papertrade partial-close feature.

For each training prefix, require >=max(40,0.9*trainingDays) completed trades and >=10 in each constituent development window. Rank broad candidates by `pooledMeanR − 0.35*SD(windowMeanR) − 0.5/sqrt(trades)`; retain eight leaders. For each leader, perturb each nonzero eligible numerical parameter separately: ±10%, windows ±2 bars, hold/cooldown about ±20%; invalid bounds and duplicate rounded values are skipped, latency reserve/filters/management held fixed. Rank centres by `0.6*neighbourMedianMeanR + 0.4*neighbourQ25MeanR − 0.15*SD(centreWindowMeanR)`. The same two-stage rule is rerun on **each fold’s training prefix only**, then once on all development data to freeze the final setting. Final-neighbourhood results are not holdout performance.

There were 1m: 1,881, 3m: 1,844, 5m: 2,042, 15m: 1,956 distinct design rows across broad search and the union of walk-forward/final neighbourhood checks, **7,723 across timeframes**, plus diagnostic controls. Rows can be economically identical where a gate is inactive; these are not independent trials. Searching thresholds, exits, filters and four timeframes introduces substantial multiple-testing/selection bias. No adjusted significance claim is made, and attractive training plateaus cannot repair a failed holdout.

### Actual walk-forward results (setting reselected before each test)

| TF | Fold | Training-selected ID | Test trades | Win rate | Mean R | PF (R) | Max DD, R | Bust rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1m | 1 | rand0233 | 82 | 43.90% | -0.0783 | 0.8574 | 9.65 | 0.0% |
| 1m | 2 | rand0080 | 69 | 50.72% | 0.1033 | 1.2097 | 12.48 | 0.0% |
| 1m | 3 | rand0474 | 34 | 35.29% | 0.0058 | 1.0092 | 11.83 | 0.0% |
| 3m | 1 | rand0300 | 164 | 33.54% | -0.0013 | 0.9975 | 16.61 | 0.0% |
| 3m | 2 | rand0141 | 141 | 28.37% | -0.0011 | 0.9982 | 15.46 | 0.0% |
| 3m | 3 | rand0155 | 28 | 35.71% | -0.1009 | 0.8359 | 8.09 | 0.0% |
| 5m | 1 | rand0113 | 75 | 44.00% | -0.0711 | 0.8713 | 12.09 | 0.0% |
| 5m | 2 | rand0860 | 85 | 21.18% | -0.1090 | 0.8183 | 20.00 | 0.0% |
| 5m | 3 | rand0359 | 28 | 17.86% | -0.1250 | 0.8111 | 10.33 | 0.0% |
| 15m | 1 | rand0838 | 76 | 30.26% | 0.2132 | 1.3058 | 10.00 | 0.0% |
| 15m | 2 | rand0774 | 81 | 28.40% | -0.1187 | 0.8252 | 15.31 | 0.0% |
| 15m | 3 | rand0747 | 37 | 29.73% | 0.1673 | 1.2380 | 9.17 | 0.0% |

Fold IDs and all rejected alternatives remain in `research/results/search-*.csv`; `selection-frozen.json` retains the exact training windows, selected IDs, scores, centre metrics and neighbourhood summaries. The walk-forward rows above evaluate the actual prefix-selected settings, not a retrospective run of the final winner relabeled as out-of-sample.

### Final chosen settings on development data only

| TF | Final ID | Trades | Mean R | Jan–Feb / Mar–Apr / May–Jun / July means | Neighbours | Median mean R | Q25 mean R | Positive neighbours |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1m | rand0474 | 223 | 0.1485 | 0.039/0.248/0.214/0.006 | 36 | 0.1485 | 0.1309 | 100% |
| 3m | rand0934 | 219 | 0.1396 | -0.024/0.174/0.283/0.097 | 35 | 0.1396 | 0.1352 | 100% |
| 5m | rand0359 | 197 | 0.1533 | 0.226/0.374/0.059/-0.125 | 36 | 0.1533 | 0.1474 | 100% |
| 15m | rand0747 | 208 | 0.2253 | 0.263/0.204/0.255/0.167 | 36 | 0.2253 | 0.2253 | 100% |

All final centres kept 24/12 despite permitting alternative windows. Neighbourhood plateaus were positive in development and failed to transfer to holdout. This is evidence of selection/regime sensitivity, not robustness sufficient for deployment. The final centres’ four window means above are selection data, not four independent tests.

## Sensitivities and default comparison

| TF | Scenario | Trades | Win rate | Mean R | PF (R) | Max DD, R | Bust rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1m | Base | 84 | 27.38% | -0.2362 | 0.6711 | 21.44 | 0.0% |
| 1m | 1 bp adverse each side | 76 | 25.00% | -0.3607 | 0.5457 | 27.41 | 0.0% |
| 1m | +0.5% builder fee | 84 | 27.38% | -0.2387 | 0.6677 | 21.62 | 0.0% |
| 1m | Intraminute full-bust stress | 84 | 27.38% | -0.2362 | 0.6711 | 21.44 | 0.0% |
| 3m | Base | 82 | 24.39% | -0.0643 | 0.9149 | 24.04 | 0.0% |
| 3m | 1 bp adverse each side | 82 | 24.39% | -0.1266 | 0.8401 | 26.83 | 0.0% |
| 3m | +0.5% builder fee | 82 | 24.39% | -0.0679 | 0.9103 | 24.10 | 0.0% |
| 3m | Intraminute full-bust stress | 82 | 24.39% | -0.0643 | 0.9149 | 24.04 | 0.0% |
| 5m | Base | 88 | 18.18% | -0.2238 | 0.6253 | 22.65 | 0.0% |
| 5m | 1 bp adverse each side | 81 | 18.52% | -0.3195 | 0.5184 | 26.29 | 0.0% |
| 5m | +0.5% builder fee | 88 | 18.18% | -0.2257 | 0.6221 | 22.73 | 0.0% |
| 5m | Intraminute full-bust stress | 88 | 18.18% | -0.2238 | 0.6253 | 22.65 | 0.0% |
| 15m | Base | 106 | 22.64% | -0.1381 | 0.8215 | 32.65 | 0.0% |
| 15m | 1 bp adverse each side | 102 | 23.53% | -0.1890 | 0.7643 | 33.07 | 0.0% |
| 15m | +0.5% builder fee | 106 | 22.64% | -0.1413 | 0.8173 | 32.83 | 0.0% |
| 15m | Intraminute full-bust stress | 106 | 22.64% | -0.1381 | 0.8215 | 32.65 | 0.0% |

The intraminute bust stress equals base because none of these selected exposures reached the approximate bust boundary inside a minute before modeled exit. It does **not** simulate a prolonged stop-service outage. The 1 bp stress is already materially harmful; untested larger basis/latency errors can be worse.

| TF | Same-feed default trades | Default holdout mean R | Default PF (R) | Selected minus default mean R |
| --- | --- | --- | --- | --- |
| 1m | 706 | -0.1036 | 0.7186 | -0.1326 |
| 3m | 514 | -0.0950 | 0.7687 | 0.0307 |
| 5m | 295 | -0.0742 | 0.8192 | -0.1496 |
| 15m | 65 | -0.2912 | 0.4396 | 0.1531 |

The selected 1m and 5m configurations are worse than this independent default on holdout; 3m and 15m are less negative. Do not replace the frozen setting with whichever baseline looked better after viewing holdout—that would consume the holdout for tuning. The 15m baseline has one unresolved boundary position excluded from completed-trade metrics; all selected configurations have none. There is no claim that every tuned setting improved the baseline out of sample.

Development-only holding controls on the final geometry, pooled over the four development windows:

| TF | 6 bars | 12 bars | 24 bars | 48 bars | 96 bars |
| --- | --- | --- | --- | --- | --- |
| 1m | -0.0613 | -0.0047 | 0.0932 | 0.1485 | 0.1837 |
| 3m | -0.0801 | -0.0739 | 0.0074 | 0.0793 | 0.1396 |
| 5m | 0.0021 | 0.0475 | 0.1533 | 0.2348 | 0.2639 |
| 15m | 0.0810 | 0.1457 | 0.1838 | 0.2305 | 0.2253 |

These controls support investigating longer holds in this development sample, including 5m, but do not justify another holdout-driven search. In the final holdout 1m time exits fall to 8/84 and 3m to 0/82, yet stop losses dominate. Removing premature time exits alone did not create an edge. The supplied exploratory 1m 48-bar lead was treated as a candidate, not as validation.

## Live liquidation-map veto and site use

Keep the complete section-5 veto **live only**, on the latest completed candidate within its one-bar entry expiry. No historical liquidation maps or protocol-summary archive were supplied or reconstructed, so **all backtests are candle-only**. The delivered filters carry the numerical live policy; it may only veto a fresh current candidate, never increase ERL, rewrite a historical marker or improve a reported holdout trade. Runtime reads must validate the response; configuration text is not a deployed map validator.

Use matching ETH/range, default rangePct=1 (percent units), exactly 150 contiguous positive-width buckets spanning finite from<to, nonnegative finite amounts/counts, and endpoint tolerance `1e−8*max(abs(from),abs(to),1)`. Normalize timestamps to seconds once. Map and summary must be <=15 seconds old, no more than 2 seconds in the future. Map midpoint must be within 0.0005 of planned entry; the entire stop-target interval must fit in range, otherwise widen or report RANGE INSUFFICIENT. Never fabricate inside-range levels for the above/below totals.

Estimate each bucket’s mass by overlap fraction (uniform-within-bucket approximation). For a long, Ad is long USD from stop to entry, Fav is short USD from entry to target, Near is long USD in the adverse 0.0005 entry band clipped to stop. Reverse the sides for shorts. Material amount is `max(10000,0.01*summary.marginUsd)`; veto if `(Ad>=material AND Ad/(Ad+Fav)>=0.75) OR Near>=material`. Zero total mass produces NO MAP EVIDENCE, not safety. A fresh valid summary with queueUsd>0 or lpUsd<=0 blocks new entries; positive LP/zero queue still leaves LP accounting unverified.

Missing/stale/malformed/mismatched map or summary preserves the core historical candidate but makes live eligibility UNKNOWN with no actionable entry. The map never changes an existing stop or target. Actual bust-price, economics and execution-service eligibility remain separate checks. Without live inputs a site can display labeled candle-only research, not silently claim that these holdout metrics include the veto. The original read-only nature of the indicator does not implement protective onchain orders.

## Evidence, uncertainty and deliverables

**Measured facts in this experiment:** public data hashes and coverage; the deterministic trade counts and modeled outcomes; positive selected development neighbourhoods; negative final holdout means and PF below one on all four timeframes. **Inference:** training gains likely reflect selection and/or a regime that did not persist; no surviving edge is established. **Unknown:** the distribution of future returns, Papertrade BBO versus Binance basis, real relayer/stop delay, actual bust rounding, current owner-adjustable economic parameters, historical queue cash payment, and historical live-veto impact. These unknowns must not be replaced by synthetic liquidity or a fabricated execution record.

A single best setting per timeframe is supplied because the assignment requires one even when negative. “Best” means selected under this finite predeclared development rule; 3m is the least-negative member of those four on holdout and under 1 bp stress. Comparing the four holdouts to name one overall also introduces selection; a genuinely new prospective evaluation would be needed for a positive performance claim. No statistically or operationally demonstrated edge survives here.

`artifacts/erl-eth-settings.json` has the exact requested top-level/parameter schema and uses proportions for win/bust rates. `research/` contains the standard-library C++17 simulator, deterministic Python search/selection/rendering scripts, all offline candle files, independent payoff/metric reconciliation, selected and baseline trade logs for all four holdout scenarios, and full search/controls tables. It needs no installed Python packages or network for verification. See root `README.md` for commands.

Settings frozen at `2026-11-04T05:04:03.279235+00:00`. Frozen-selection SHA-256 used by evaluation: `9c1fd32b6f6c63cb917239475d0ede5eb310d873bf6e424a8246d076c9e7c41a`. The freeze records a causal parameter decision, not an independent audit or preregistration before collecting the data.

Local checks cover the hand-computable surviving-interval example; randomized numerical integration/translation/partition checks; payoff table and monotonicity; long/short exits; next-open entry and structural/time fills; drift rejection; gap/bust/stop-first handling; break-even/trailing activation; partial-control accounting; cooldown; censored positions; gap aggregation; and prefix-causality on generated histories. Independent Python code reconstructs payout and reconciles every selected holdout R and reported summary against raw trade logs. Dataset and output schema checks are included. These are self-checks of implementation consistency, **not independent certification of the model or strategy profitability**.

