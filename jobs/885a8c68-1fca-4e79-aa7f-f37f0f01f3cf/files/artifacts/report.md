**BTC and ETH perpetuals at 100x: ten indicator setups, tested against Papertrade’s documented economics**

Research cutoff: 3 November 2026, 16:00 UTC. This report and `tuning.json` were generated from the bundled candles and trade ledger. All performance tables below use the held-out period only.

**Finding: none of the ten tuned indicators, or either tested combination, showed a positive pooled BTC/ETH net expectancy. Do not deploy these at 100x on this evidence.** TD Sequential was the least negative eligible result, at −0.020 R per trade over 59 trades, with a wide interval spanning losses and gains. A higher win rate did not establish an edge. “No demonstrated edge” describes this experiment; it is not proof that every possible version must fail.

**Scope and uncertainty.** This is a reproducible **current-rule, cross-venue price-proxy study**, not an exact historical Papertrade execution replay. The docs supply rounded impact parameters and an approximate bust buffer; public OHLCV does not supply block-level BBO, keeper ordering, historical owner settings, or LP state. Those gaps are not filled with invented data. The modeled payout equations, hard-bust treatment, explicit assumptions, and sensitivity results follow below. Exact contract rounding and actual historical fills remain unanswered.

**Out-of-sample ranking.** Test interval: **22 October 2026 16:00 to 3 November 2026 16:00 UTC**, 12 days. Rank by mean net R among setups with at least 30 pooled trades; fewer than 30 are placed last. This is a descriptive comparison, not a second validated selection step. Selecting a live winner from this table would require a fresh future test.

| Rank | Indicator | TF | Trades | Win rate | Mean R | PF | Max DD (R) | DD / initial equity | Bust rate | 95% block interval, mean R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TD Sequential | 1m | 59 | 57.6% | -0.020 | 0.903 | 3.70 | 0.92% | 0.00% | [-0.141, 0.159] |
| 2 | RSI | 1m | 1079 | 52.6% | -0.035 | 0.808 | 56.12 | 14.03% | 0.37% | [-0.080, 0.010] |
| 3 | Moving averages | 1m | 623 | 44.3% | -0.046 | 0.709 | 35.42 | 8.85% | 0.00% | [-0.091, -0.003] |
| 4 | Bollinger | 5m | 50 | 46.0% | -0.048 | 0.855 | 9.64 | 2.41% | 0.00% | [-0.284, 0.221] |
| 5 | MA ribbon | 1m | 540 | 45.2% | -0.067 | 0.647 | 43.23 | 10.81% | 0.19% | [-0.096, -0.039] |
| 6 | Stochastic | 5m | 157 | 43.3% | -0.102 | 0.730 | 23.56 | 5.89% | 0.00% | [-0.243, 0.027] |
| 7 | Volume | 15m | 76 | 35.5% | -0.139 | 0.762 | 17.99 | 4.50% | 0.00% | [-0.306, 0.026] |
| 8 | Ichimoku | 15m | 66 | 37.9% | -0.164 | 0.705 | 11.96 | 2.99% | 0.00% | [-0.362, 0.044] |
| 9 | MACD | 15m | 71 | 35.2% | -0.259 | 0.585 | 21.18 | 5.29% | 1.41% | [-0.481, 0.056] |
| 10 | SuperTrend | 1h | 27 | 33.3% | -0.094 | 0.859 | 9.24 | 2.31% | 0.00% | [-0.442, 0.530] |


The maximum drawdown here marks open positions at each one-minute close using the same net-close payout curve, plus realized PnL. It can miss intraminute equity peaks/troughs. Equity uses **fixed 0.25% of initial account equity per planned stop (1 R)**, no compounding, one position per asset, and simultaneous BTC/ETH trades. These are ten separate experiments; their returns must not be added as a portfolio. Realized-only drawdowns, side counts, and all unrounded statistics are in `tuning.json`.

R = net PnL / (notional × stop fraction). Win rate counts strictly positive net outcomes, zero as a non-win. PF = sum of positive net R / absolute sum of negative net R. A bust costs 1/(100 × stop fraction) R: 5 R at a 0.20% stop, 2.857 R at 0.35%, or 2 R at 0.50%. Thus a stop inside bust does not eliminate liquidation risk. The 95% intervals use 2,000 circular three-day block resamples of the 12 days, jointly across assets; they are descriptive, with few independent blocks and no multiple-testing adjustment. Zero observed busts is not a zero-risk claim.

**Data and selection.** The dataset contains 90,720 confirmed native one-minute candles per asset from **1 September 2026 16:00 through 3 November 2026 15:59 UTC**, 63 complete days. Instruments are OKX **BTC-USDT-SWAP** and **ETH-USDT-SWAP**, not spot. Prices are in USDT; volume is in base-asset units. There are no missing or duplicate minutes, no unconfirmed rows, and OHLC bounds passed validation. Public source: [OKX history-candles](https://www.okx.com/api/v5/market/history-candles), with [official field and pagination definitions](https://www.okx.com/docs-v5/en/#rest-api-market-data-get-candlesticks-history).

The older BTC and ETH [Hyperliquid candleSnapshot](https://api.hyperliquid.xyz/info) probes returned empty arrays. Its [API documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint) limits candle history to the most recent 5,000 candles, insufficient for 60 days of one-minute bars. The fallback and exact request/response probes are saved in `sources/hyperliquid-probe.json`; Binance was reachable in a preliminary probe but was not used in the dataset. No venue series were spliced.

Five-minute, 15-minute, and one-hour series are UTC-aligned aggregates of the same one-minute history, with 18,144 / 6,048 / 1,512 bars per asset respectively. Open = first open, high/low = extremes, close = last close, volume = sum. Eighteen sampled comparisons against native OKX higher-timeframe candles all matched. The compressed native and derived datasets, checksums, and audit responses are bundled under `data/` and `sources/`. Every stop and target uses one-minute execution candles, regardless of signal timeframe.

The held-out input sample per asset is 17,280 one-minute bars, 3,456 five-minute bars, 1,152 fifteen-minute bars, and 288 hourly bars. The trade counts in the result tables are the executed subset after triggers, filters and position-overlap rules; bars and trades are not independent observations.

| Stage | Start inclusive, UTC | End exclusive, UTC | Purpose |
| --- | --- | --- | --- |
| Warm-up | 2026-09-01 16:00 | 2026-09-08 16:00 | 7 days; no scored entries |
| Training | 2026-09-08 16:00 | 2026-10-10 16:00 | 32 days; candidate ranking |
| Validation | 2026-10-10 16:00 | 2026-10-22 16:00 | 12 days; choose among top five |
| Test | 2026-10-22 16:00 | 2026-11-03 16:00 | 12 days; report once after selection |


For each family, the search is 3 indicator variants × 4 timeframes (1m/5m/15m/1h) × trend filter on/off × 3 exit packages = **72 candidates, 720 total**. Exit packages are (stop, target, time): (0.20%, 0.40%, 6 bars), (0.35%, 0.70%, 12 bars), (0.50%, 1.00%, 24 bars). Both sides and assets share one selected configuration; there is no per-asset hindsight tuning. The objective is pooled mean net R minus 0.5 × sample SD(R)/√n, with ≥40 training trades and ≥15 validation trades, plus at least max(3, floor(minimum/5)) trades per asset. Top five training candidates proceed to validation; highest validation objective wins, ties resolved by training score. All ten selected configurations met these count requirements. A selected configuration may still have negative expectancy; selection is not an instruction to trade.

The full grid is in `research/search-design.json`, every candidate’s training record and finalist validation record in `research/search-audit.json`, and the frozen choices in `research/selection-lock.json` (SHA-256 recorded in the tuning file). The script writes the lock before computing any test results. No signal, threshold, or timeframe was changed after observing test performance. The continuous-stop sensitivity was added as an execution audit after the initial run; it did not change selection. Indicators may use preceding training/validation candles as past context; positions never carry across split boundaries and are force-closed at a boundary. This is a single chronological train/validation/test experiment, not repeated walk-forward validation.

**What Papertrade actually charges.** The current docs describe synthetic positions against the LP, with entry and close priced at Hyperliquid BBO mid. There is no notional trading fee, spread, funding, or user-paid gas. Impact acts on **winning PnL**, not the entry price; papertrade.xyz names no builder, so the base scenario has no builder fee. [Architecture](https://docs.papertrade.xyz/how/architecture/), [BBO pricing](https://docs.papertrade.xyz/how/pricing-bbo/), [trades and pricing](https://docs.papertrade.xyz/learn/trades-pricing/).

For directional price return d = side × (exit/entry − 1), a non-bust loss is not scaled and carries no extra trader charge. For a win, remove a 0.2 bp price deadband and the active holdback, then apply the documented impact scale and 2% win fee. [Asymmetric impact](https://docs.papertrade.xyz/how/asymmetric-impact/), [wins and losses](https://docs.papertrade.xyz/learn/wins-losses/).

```text
m = max(0, d − 0.00002 − holdback)
net PnL / notional = m × (1 − b) / (1 + 1/(m×r) + Nref/(10^6×m×p)) × 0.98
(set result to zero when m = 0)
b = 0.10; r = 15000; Nref = 100000
pBTC = 814.598; pETH = 483.979

Within the relevant raw-move band only:
u = (d − band_start) / width
standard: holdback = 3.597 × width × u² × (1−u)²; band 0.75–6 bp
off-hours: holdback = 6.085 × width × u² × (1−u)³; band 0.3–10 bp
Otherwise holdback = 0.
```

These are the documented launch values held fixed throughout this counterfactual. The owner can change fee/impact settings; the off-hours keeper chooses the curve on an unpublished schedule. Headline results assume the standard curve for every close; an all-off-hours scenario tests the other endpoint. Neither is claimed to be the actual historical schedule. [Risk and operator powers](https://docs.papertrade.xyz/how/risk/).

The user brief’s “about 1%, less after impact” is corrected by the current liquidation documentation: the early bust comes from a **fixed price buffer**, not entry slippage. At 100x, the docs place the hard trigger near a **0.95% adverse move** (1% zero-equity move less about 0.05% price buffer). Crossing it, including on a voluntary close, loses **the full isolated margin**, rather than only 95% of margin. Main tests use 0.95%; 0.90% and 1.00% are sensitivity assumptions because the page gives no exact fixed-point formula. All proposed stops are ≤0.50%, inside every tested threshold. The exact displayed live bust must be checked before use. [Liquidations](https://docs.papertrade.xyz/learn/liquidations/).

Contract set 2 is documented as live since **21 October 2026**; the production launch is documented as 7 October. The 63-day data therefore cannot be represented as 63 days of realized Papertrade trading. We apply current rules to older prices for fitting, with test dates after the documented upgrade. An attempt to obtain the linked implementation’s verified source encountered an unverified contract page; byte-exact bust and payout arithmetic was not independently established. [Protocol change history](https://docs.papertrade.xyz/dev/protocol-changes/), [documented deployment](https://docs.papertrade.xyz/dev/contract-addresses/), [implementation explorer](https://hyperevmscan.io/address/0x0A44049dBbb6b4762a6ba37aa0f7548c0B4A3723#code).

PAPER is not counted as recoverable trading income. It is emitted on eligible **losses and liquidations**, and the docs say it is non-transferable at launch. The implemented state-dependent formula is `supply × expm1(c × (g + (m−1) × g_below0))`, with `m=1+4u(2−u)`, `u=min(1, insolvent_seconds/259200)`, and `g_below0=min(LP credit, LP deficit)`. The documented c is approximately 1.101e−9 per dollar. A solvent, queue-empty USD losing close without a builder generally uses 98% of loss as mint basis; a liquidation uses full lost margin. The required historical supply, exact c, queue/funding state and insolvency clock are unavailable, so **token quantities and token-valued returns are unknown**, not fabricated zero-valued measurements. No staking yield is credited. [Mint curve](https://docs.papertrade.xyz/how/mint-curve/), [PAPER emissions](https://docs.papertrade.xyz/learn/paper-emissions/).

Profitable accounting credits are also not guaranteed immediate cash withdrawals: LP insolvency can queue claims. The backtest measures modeled PnL claims, assumes no rejected opens, and does not model payout waiting time, retirement, caps or relayer outages. These missing states can make live experience worse. [LP solvency and payout queue](https://docs.papertrade.xyz/how/solvency-queue/), [risk](https://docs.papertrade.xyz/how/risk/).

**Execution convention for every setup.** Signal t confirms only at its candle close; enter at candle t+1’s open, using that minute’s OKX open as a BBO proxy. Skip if entry differs from signal close by more than 0.10% in either direction. A long stop is entry×(1−s), short stop entry×(1+s); targets reverse those signs. Exit full size at the first stop, target, bust, or time stop. Count the entry candle as holding bar 1; a six-bar limit on 5m means 30 minutes. There are no trailing stops, partial closes, or stop widening. New signals, including opposite signals, are ignored while a position in that asset is open. BTC and ETH can each hold one position. No session filter is used.

At a minute open, a gap beyond bust loses full margin, an adverse gap through stop fills at that open, and a favorable gap through target is credited only at target. Within a minute, bust takes priority if touched while still open; otherwise stop precedes target when both are touched. This is a **conservative ambiguity convention**, not knowledge of the price path or a claim that every candle touching bust causes a real bust before a working stop. The ideal continuous-stop scenario assumes stop execution before a later intraminute bust touch; the delay scenario executes a stop/target-triggered close at the next minute open. Actual block latency and intraminute BBO may lie outside these simplified cases.

The documentation describes full-position closes through the relayer, but does not establish native guaranteed stop or target orders. The setup therefore requires monitored/automated close intents; a chart line alone cannot protect margin. For operational use, skip missing or unfinished data, rejected/paused markets, unreliable close submission, and any entry where the actual displayed bust is inside the planned stop. Those live checks were not backtest filters. [Trading workflow](https://docs.papertrade.xyz/learn/trades-pricing/), [architecture](https://docs.papertrade.xyz/how/architecture/).

**The ten unambiguous specifications.** These are the selected research setups for both assets; none is recommended for live 100x deployment on the evidence above. “Trend filter” always means close > rising EMA100 for a long, or close < falling EMA100 for a short, on the selected timeframe. Strict rising/falling compares with the preceding completed bar. Every row inherits the execution and skip rules above.

**1. Bollinger — 5m.** Parameters: `{"period":20,"sd":2.0,"local":5,"reentry":true}`.

**Long:** Current low ≤ SMA20 − 2×population SD20 and is the minimum low of this bar and the preceding four; close > lower band and close > open. **Short:** Current high ≥ SMA20 + 2×population SD20 and is the maximum high of this bar and the preceding four; close < upper band and close < open.

Confirm at the completed signal bar; enter next open under the common assumption. **Stop 0.20% of entry; target 0.40%; time stop 6 bars (30 minutes).** Apply the EMA100 trend filter on both sides. No session filter or trailing rule. Do not enter on the touch alone, on a doji, or before the close returns inside the touched band.

Selection sample: 165 training and 66 validation trades for the final configuration (not headline performance). Test sample: 50 trades; 26 long / 24 short. Time stops ended 32 trades; forced close at the test boundary ended 0.

| Asset | Side | Trades | Win rate | Mean R | PF | Realized max DD (R) | Bust rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BTC | long | 14 | 50.0% | -0.146 | 0.583 | 2.44 | 0.00% |
| BTC | short | 12 | 41.7% | -0.118 | 0.712 | 4.15 | 0.00% |
| ETH | long | 12 | 41.7% | 0.179 | 1.890 | 1.83 | 0.00% |
| ETH | short | 12 | 50.0% | -0.091 | 0.754 | 4.38 | 0.00% |


Assessment: **no demonstrated edge at 100x after tuning**; pooled mean -0.048 R and PF 0.855. A positive asset or side subgroup is exploratory and too small to rescue the pooled result.

**2. Moving averages — 1m.** Parameters: `{"fast":5,"middle":20,"slow":50,"width":0.0005,"duration":5}`.

**Long:** For at least five consecutive completed bars, (max(EMA5,EMA20,EMA50) − min(...))/close ≤ 0.0005. On the current bar it becomes > 0.0005, EMA5 > EMA50, EMA5 rises and EMA50 rises versus the prior bar. **Short:** The same five-bar compression ends with width > 0.0005, EMA5 < EMA50, EMA5 falls and EMA50 falls versus the prior bar.

Confirm at the completed signal bar; enter next open under the common assumption. **Stop 0.35% of entry; target 0.70%; time stop 12 bars (12 minutes).** Apply the EMA100 trend filter on both sides. No session filter or trailing rule. No entry while still compressed, after a release without five immediately preceding compressed bars, or when the two EMA slopes disagree.

Selection sample: 1521 training and 541 validation trades for the final configuration (not headline performance). Test sample: 623 trades; 287 long / 336 short. Time stops ended 604 trades; forced close at the test boundary ended 0.

| Asset | Side | Trades | Win rate | Mean R | PF | Realized max DD (R) | Bust rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BTC | long | 157 | 45.9% | -0.019 | 0.854 | 9.66 | 0.00% |
| BTC | short | 180 | 44.4% | -0.054 | 0.628 | 9.87 | 0.00% |
| ETH | long | 130 | 47.7% | -0.035 | 0.800 | 10.69 | 0.00% |
| ETH | short | 156 | 39.7% | -0.073 | 0.607 | 11.92 | 0.00% |


Assessment: **no demonstrated edge at 100x after tuning**; pooled mean -0.046 R and PF 0.709. Its selected validation mean was already nonpositive; do not interpret the mechanical selection as evidence of an edge.

**3. MA ribbon — 1m.** Parameters: `{"fast":[3,5,8,10,12,15],"slow":[30,35,40,45,50,60],"mode":"cross"}`.

**Long:** The arithmetic mean of EMA3/5/8/10/12/15 crosses strictly above the mean of EMA30/35/40/45/50/60; on the previous bar the fast mean was ≤ the slow mean. **Short:** The same fast mean crosses strictly below the slow mean; on the previous bar it was ≥ the slow mean.

Confirm at the completed signal bar; enter next open under the common assumption. **Stop 0.50% of entry; target 1.00%; time stop 24 bars (24 minutes).** Apply the EMA100 trend filter on both sides. No session filter or trailing rule. An already aligned ribbon is not a new entry. Do not trade an intrabar crossover that disappears at the close.

Selection sample: 1454 training and 522 validation trades for the final configuration (not headline performance). Test sample: 540 trades; 295 long / 245 short. Time stops ended 504 trades; forced close at the test boundary ended 0.

| Asset | Side | Trades | Win rate | Mean R | PF | Realized max DD (R) | Bust rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BTC | long | 140 | 40.7% | -0.060 | 0.624 | 11.05 | 0.00% |
| BTC | short | 116 | 52.6% | -0.027 | 0.804 | 5.64 | 0.00% |
| ETH | long | 155 | 44.5% | -0.072 | 0.664 | 15.07 | 0.65% |
| ETH | short | 129 | 44.2% | -0.103 | 0.561 | 13.74 | 0.00% |


Assessment: **no demonstrated edge at 100x after tuning**; pooled mean -0.067 R and PF 0.647. Its selected validation mean was already nonpositive; do not interpret the mechanical selection as evidence of an edge.

**4. SuperTrend — 1h.** Parameters: `{"atr":7,"mult":2.0,"smoothing":"sma"}`.

**Long:** SuperTrend with SMA ATR7 × 2 on hl2 flips from down to up when the close is strictly above the current final upper band. **Short:** The same SuperTrend flips from up to down when the close is strictly below the current final lower band.

Confirm at the completed signal bar; enter next open under the common assumption. **Stop 0.50% of entry; target 1.00%; time stop 24 bars (1440 minutes).** No extra trend filter. No session filter or trailing rule. Do not enter on a wick through the band or merely because the trend remains up/down. Exact recursive bands are specified below.

Selection sample: 65 training and 24 validation trades for the final configuration (not headline performance). Test sample: 27 trades; 14 long / 13 short. Time stops ended 0 trades; forced close at the test boundary ended 0.

| Asset | Side | Trades | Win rate | Mean R | PF | Realized max DD (R) | Bust rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BTC | long | 6 | 33.3% | -0.091 | 0.864 | 2.27 | 0.00% |
| BTC | short | 6 | 16.7% | -0.545 | 0.346 | 5.00 | 0.00% |
| ETH | long | 8 | 37.5% | 0.018 | 1.028 | 5.00 | 0.00% |
| ETH | short | 7 | 42.9% | 0.163 | 1.285 | 3.00 | 0.00% |


Assessment: **no demonstrated edge at 100x after tuning**; pooled mean -0.094 R and PF 0.859. Only 27 trades pooled (12 BTC / 15 ETH): strongly underpowered.

**5. Ichimoku — 15m.** Parameters: `{"tenkan":6,"kijun":18,"span_b":36,"displacement":18,"mode":"break"}`.

**Long:** With tenkan/kijun/span-B = 6/18/36 and displacement 18, close is above the displayed cloud top and the previous close was ≤ the previous displayed cloud top; current tenkan > kijun. **Short:** Close is below the displayed cloud bottom and the previous close was ≥ the previous displayed cloud bottom; current tenkan < kijun.

Confirm at the completed signal bar; enter next open under the common assumption. **Stop 0.50% of entry; target 1.00%; time stop 24 bars (360 minutes).** No extra trend filter. No session filter or trailing rule. No inside-cloud entries or breaks against tenkan/kijun alignment. Use the cloud calculated 18 bars ago, not today’s forward projection.

Selection sample: 162 training and 67 validation trades for the final configuration (not headline performance). Test sample: 66 trades; 29 long / 37 short. Time stops ended 19 trades; forced close at the test boundary ended 0.

| Asset | Side | Trades | Win rate | Mean R | PF | Realized max DD (R) | Bust rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BTC | long | 13 | 46.2% | -0.090 | 0.739 | 3.37 | 0.00% |
| BTC | short | 15 | 46.7% | 0.053 | 1.121 | 2.01 | 0.00% |
| ETH | long | 16 | 25.0% | -0.488 | 0.335 | 7.80 | 0.00% |
| ETH | short | 22 | 36.4% | -0.121 | 0.811 | 5.23 | 0.00% |


Assessment: **no demonstrated edge at 100x after tuning**; pooled mean -0.164 R and PF 0.705.

**6. TD Sequential — 1m.** Parameters: `{"setup":9,"countdown":13,"mode":"setup_reversal","perfect":true}`.

**Long:** Exactly the ninth consecutive close < close four bars earlier; min(low on setup bars 8,9) ≤ min(low on setup bars 6,7), and the ninth candle is green (close > open). **Short:** Exactly the ninth consecutive close > close four bars earlier; max(high on setup bars 8,9) ≥ max(high on setup bars 6,7), and the ninth candle is red (close < open).

Confirm at the completed signal bar; enter next open under the common assumption. **Stop 0.50% of entry; target 1.00%; time stop 24 bars (24 minutes).** Apply the EMA100 trend filter on both sides. No session filter or trailing rule. Do not anticipate bar 9, backdate a later perfection, or enter on countdown 13 for this selected setup. Equality in the four-bar comparison resets that setup count.

Selection sample: 161 training and 39 validation trades for the final configuration (not headline performance). Test sample: 59 trades; 22 long / 37 short. Time stops ended 52 trades; forced close at the test boundary ended 0.

| Asset | Side | Trades | Win rate | Mean R | PF | Realized max DD (R) | Bust rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BTC | long | 11 | 63.6% | 0.044 | 1.512 | 0.88 | 0.00% |
| BTC | short | 19 | 57.9% | -0.003 | 0.976 | 2.12 | 0.00% |
| ETH | long | 11 | 54.5% | -0.122 | 0.555 | 2.97 | 0.00% |
| ETH | short | 18 | 55.6% | -0.013 | 0.955 | 2.85 | 0.00% |


Assessment: **no demonstrated edge at 100x after tuning**; pooled mean -0.020 R and PF 0.903. A positive asset or side subgroup is exploratory and too small to rescue the pooled result.

**7. RSI — 1m.** Parameters: `{"period":7,"lower":30,"upper":70,"mode":"recross"}`.

**Long:** Wilder RSI7 was < 30 on the prior bar and is ≥ 30 now, with current close > open. **Short:** Wilder RSI7 was > 70 on the prior bar and is ≤ 70 now, with current close < open.

Confirm at the completed signal bar; enter next open under the common assumption. **Stop 0.50% of entry; target 1.00%; time stop 24 bars (24 minutes).** No extra trend filter. No session filter or trailing rule. No entry merely because RSI remains oversold/overbought; require the threshold recross and candle color. No trend or session filter was selected.

Selection sample: 2844 training and 1057 validation trades for the final configuration (not headline performance). Test sample: 1079 trades; 563 long / 516 short. Time stops ended 973 trades; forced close at the test boundary ended 2.

| Asset | Side | Trades | Win rate | Mean R | PF | Realized max DD (R) | Bust rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BTC | long | 278 | 51.4% | -0.044 | 0.721 | 16.55 | 0.00% |
| BTC | short | 255 | 52.5% | -0.024 | 0.833 | 10.97 | 0.00% |
| ETH | long | 285 | 54.4% | -0.043 | 0.821 | 23.31 | 1.40% |
| ETH | short | 261 | 52.1% | -0.028 | 0.850 | 11.90 | 0.00% |


Assessment: **no demonstrated edge at 100x after tuning**; pooled mean -0.035 R and PF 0.808. Its selected validation mean was already nonpositive; do not interpret the mechanical selection as evidence of an edge.

**8. MACD — 15m.** Parameters: `{"fast":12,"slow":26,"signal":9}`.

**Long:** MACD = EMA12 − EMA26; signal = EMA9 of MACD. Histogram is > 0 now and was ≤ 0 on the prior bar. **Short:** The same histogram is < 0 now and was ≥ 0 on the prior bar.

Confirm at the completed signal bar; enter next open under the common assumption. **Stop 0.50% of entry; target 1.00%; time stop 24 bars (360 minutes).** Apply the EMA100 trend filter on both sides. No session filter or trailing rule. Do not treat a change in histogram slope as a zero crossing or act before the bar closes.

Selection sample: 187 training and 60 validation trades for the final configuration (not headline performance). Test sample: 71 trades; 25 long / 46 short. Time stops ended 15 trades; forced close at the test boundary ended 1.

| Asset | Side | Trades | Win rate | Mean R | PF | Realized max DD (R) | Bust rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BTC | long | 11 | 27.3% | -0.528 | 0.273 | 6.54 | 0.00% |
| BTC | short | 24 | 33.3% | -0.221 | 0.600 | 5.65 | 0.00% |
| ETH | long | 14 | 35.7% | -0.402 | 0.438 | 6.29 | 7.14% |
| ETH | short | 22 | 40.9% | -0.075 | 0.873 | 8.09 | 0.00% |


Assessment: **no demonstrated edge at 100x after tuning**; pooled mean -0.259 R and PF 0.585.

**9. Stochastic — 5m.** Parameters: `{"k":9,"d":3,"lower":30,"upper":70}`.

**Long:** Raw %K9 = 100×(close − lowest low9)/(highest high9 − lowest low9), %D = SMA3(%K). K > D now, K ≤ D previously, and current K < 30. **Short:** K < D now, K ≥ D previously, and current K > 70.

Confirm at the completed signal bar; enter next open under the common assumption. **Stop 0.35% of entry; target 0.70%; time stop 12 bars (60 minutes).** Apply the EMA100 trend filter on both sides. No session filter or trailing rule. No signal if the crossing occurs outside the specified K zone. A zero nine-bar range is assigned K = 50 and provides no extreme-zone signal.

Selection sample: 434 training and 172 validation trades for the final configuration (not headline performance). Test sample: 157 trades; 81 long / 76 short. Time stops ended 101 trades; forced close at the test boundary ended 0.

| Asset | Side | Trades | Win rate | Mean R | PF | Realized max DD (R) | Bust rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BTC | long | 38 | 52.6% | 0.021 | 1.085 | 4.80 | 0.00% |
| BTC | short | 35 | 42.9% | -0.092 | 0.765 | 7.70 | 0.00% |
| ETH | long | 43 | 46.5% | -0.028 | 0.907 | 4.89 | 0.00% |
| ETH | short | 41 | 31.7% | -0.302 | 0.471 | 13.09 | 0.00% |


Assessment: **no demonstrated edge at 100x after tuning**; pooled mean -0.102 R and PF 0.730. Its selected validation mean was already nonpositive; do not interpret the mechanical selection as evidence of an edge.

**10. Volume — 15m.** Parameters: `{"vma":30,"multiple":2.0,"move":0.002,"mode":"breakout"}`.

**Long:** Base-asset volume is > 2×SMA30(volume), including the signal bar, and close/open − 1 > 0.002. **Short:** Volume is > 2×SMA30(volume), including the signal bar, and close/open − 1 < −0.002.

Confirm at the completed signal bar; enter next open under the common assumption. **Stop 0.50% of entry; target 1.00%; time stop 24 bars (360 minutes).** Apply the EMA100 trend filter on both sides. No session filter or trailing rule. A high-volume doji or spike without the required signed 0.20% body move is not a trade. Do not use dollar volume in place of the tested base-asset volume.

Selection sample: 214 training and 79 validation trades for the final configuration (not headline performance). Test sample: 76 trades; 33 long / 43 short. Time stops ended 16 trades; forced close at the test boundary ended 1.

| Asset | Side | Trades | Win rate | Mean R | PF | Realized max DD (R) | Bust rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BTC | long | 14 | 28.6% | -0.437 | 0.245 | 6.73 | 0.00% |
| BTC | short | 16 | 43.8% | -0.012 | 0.977 | 3.70 | 0.00% |
| ETH | long | 19 | 31.6% | -0.269 | 0.561 | 6.83 | 0.00% |
| ETH | short | 27 | 37.0% | 0.033 | 1.055 | 5.53 | 0.00% |


Assessment: **no demonstrated edge at 100x after tuning**; pooled mean -0.139 R and PF 0.762.

**Baseline results and interpretation.** The brief supplies no baseline timeframe, stop, target or holding period. To make it tradable without optimizing on the test set, all baseline signals use a common fixed 0.35% stop / 0.70% target / 12-bar time stop, the same next-open and gap conventions, and no EMA100 filter. They are evaluated separately on all four requested timeframes below. This wrapper is an experimental assumption, not an original baseline parameter. Compare tuned and baseline at the same timeframe as well as the common 5m reference; changes in exits and timeframe prevent attributing improvement solely to an indicator parameter.

| Baseline | TF | Trades | Win rate | Mean R | PF | Realized max DD (R) | Bust rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Bollinger | 1m | 2448 | 50.8% | -0.053 | 0.737 | 133.99 | 0.20% |
| Bollinger | 5m | 657 | 47.2% | -0.073 | 0.828 | 79.54 | 0.61% |
| Bollinger | 15m | 320 | 40.0% | -0.104 | 0.817 | 47.27 | 0.62% |
| Bollinger | 1h | 125 | 31.2% | -0.176 | 0.742 | 31.66 | 0.00% |
| Moving averages | 1m | 0 | — | — | — | — | — |
| Moving averages | 5m | 0 | — | — | — | — | — |
| Moving averages | 15m | 2 | 50.0% | 0.346 | 1.693 | 1.00 | 0.00% |
| Moving averages | 1h | 2 | 0.0% | -1.000 | 0.000 | 2.00 | 0.00% |
| MA ribbon | 1m | 0 | — | — | — | — | — |
| MA ribbon | 5m | 0 | — | — | — | — | — |
| MA ribbon | 15m | 0 | — | — | — | — | — |
| MA ribbon | 1h | 0 | — | — | — | — | — |
| SuperTrend | 1m | 1136 | 50.6% | -0.020 | 0.870 | 37.88 | 0.00% |
| SuperTrend | 5m | 209 | 43.5% | -0.055 | 0.848 | 14.42 | 0.00% |
| SuperTrend | 15m | 62 | 43.5% | -0.033 | 0.941 | 11.28 | 0.00% |
| SuperTrend | 1h | 13 | 53.8% | 0.385 | 1.835 | 3.00 | 0.00% |
| Ichimoku | 1m | 1461 | 46.7% | -0.057 | 0.693 | 92.56 | 0.00% |
| Ichimoku | 5m | 349 | 45.3% | -0.094 | 0.757 | 37.72 | 0.00% |
| Ichimoku | 15m | 140 | 39.3% | -0.024 | 0.954 | 19.09 | 0.00% |
| Ichimoku | 1h | 47 | 31.9% | -0.183 | 0.731 | 11.01 | 0.00% |
| TD Sequential | 1m | 1029 | 54.6% | -0.031 | 0.827 | 40.10 | 0.00% |
| TD Sequential | 5m | 183 | 50.8% | -0.002 | 0.993 | 16.66 | 0.00% |
| TD Sequential | 15m | 71 | 33.8% | -0.237 | 0.601 | 20.79 | 1.41% |
| TD Sequential | 1h | 16 | 37.5% | 0.015 | 1.024 | 5.00 | 0.00% |
| RSI | 1m | 488 | 57.0% | -0.000 | 0.997 | 10.27 | 0.00% |
| RSI | 5m | 96 | 41.7% | -0.191 | 0.651 | 23.87 | 2.08% |
| RSI | 15m | 34 | 38.2% | -0.029 | 0.950 | 6.07 | 0.00% |
| RSI | 1h | 10 | 60.0% | 0.622 | 2.554 | 3.00 | 0.00% |
| MACD | 1m | 1629 | 50.0% | -0.031 | 0.818 | 62.55 | 0.00% |
| MACD | 5m | 373 | 42.9% | -0.153 | 0.628 | 60.33 | 0.00% |
| MACD | 15m | 150 | 42.0% | -0.034 | 0.933 | 23.11 | 0.00% |
| MACD | 1h | 46 | 32.6% | -0.119 | 0.824 | 15.80 | 0.00% |
| Stochastic | 1m | 1492 | 51.1% | -0.028 | 0.843 | 51.01 | 0.07% |
| Stochastic | 5m | 264 | 47.3% | -0.045 | 0.875 | 21.46 | 0.38% |
| Stochastic | 15m | 79 | 39.2% | -0.041 | 0.924 | 18.19 | 0.00% |
| Stochastic | 1h | 15 | 60.0% | 0.622 | 2.556 | 3.00 | 0.00% |
| Volume | 1m | 0 | — | — | — | — | — |
| Volume | 5m | 1 | 0.0% | -1.000 | 0.000 | 1.00 | 0.00% |
| Volume | 15m | 1 | 0.0% | -1.000 | 0.000 | 1.00 | 0.00% |
| Volume | 1h | 2 | 0.0% | -1.000 | 0.000 | 2.00 | 0.00% |


Positive baseline cells are not hidden: 1h SuperTrend made +0.385 R over 13 trades, 1h RSI +0.622 R over 10, 1h stochastic +0.622 R over 15, 1h TD +0.015 R over 16, and 15m moving averages +0.346 R over just two. All are very small samples among 40 baseline comparisons; selecting them after seeing this table would spend the holdout. They are not demonstrated edges. The 1m baseline RSI was close to flat (PF 0.997) and better than the selected tuned RSI; tuning did not reliably improve results, and several selected versions performed worse than their same-timeframe baselines.

An em dash is undefined, not a zero win rate or zero risk. The original ribbon has **no entry signals**, so its baseline correctly has zero trades on every timeframe; tuning adds a new entry rule. The MA baseline uses an explicit release above 3% EMA width following at least five bars at/below it; zero or very few trades reflect this definition and cannot establish profitability. For volume, only the directional BREAKOUT/BREAKDOWN labels create baseline orders; undirected spikes and exhaustion annotations do not specify a side and are not silently converted into trades.

Other necessary baseline interpretations: Bollinger’s five-bar local extreme means a trailing window including the current bar, not a hindsight-centered pivot. Its population SD uses the latest 15 closes. STRONG labels are included with the same risk as ordinary entries; colors and SD buckets are display annotations. Ichimoku takes the union of tenkan/kijun crosses and displayed-cloud breaks, without filtering out weak grades; simultaneous opposite signals cancel. RSI retains its asymmetric 30/80 thresholds and candle-color requirement. Stochastic tests the current K against the stated zone. Volume’s move means close/open−1, and its VMA includes the current candle.

TD Sequential is an explicit reproducible variant of the description, not a claim to reproduce unavailable licensed chart code: setup counts close versus four bars back, resetting on failure; the ninth bar triggers. The baseline also permits nonconsecutive countdown 13 (close ≤ low two back for buys; close ≥ high two back for sells), beginning on setup completion. A new setup restarts the countdown, the opposite setup cancels/replaces it, and a close through the active setup’s TDST extreme cancels it (buy above setup-high resistance, sell below setup-low support). The 13th qualifying count is deferred until buy low ≤ countdown-8 close, or sell high ≥ it. Perfection tests setup bars 8/9 versus 6/7 without backdating. The selected tuned version uses perfected setup 9 with reversal candle and EMA100 filter, not countdown entries. These choices matter to attribution; alternative TD recycling/TDST definitions need a new study.

SMA uses a full trailing window; EMA is seeded by its first full-window SMA and then α=2/(n+1); Wilder RSI uses α=1/n on positive/negative close differences. Flat RSI is 50. For SuperTrend, basic bands are hl2±multiplier×SMA(true range); final upper is the current basic upper if it is lower than the prior final upper or prior close exceeded that upper, otherwise the prior upper. Final lower is the current basic lower if higher than the prior lower or prior close was below that lower, otherwise the prior lower. Seed direction is up after ATR warm-up, then flip on close crossing the opposite final band. Ichimoku midpoints use rolling high/low ranges, with both cloud spans shifted from the past by the configured displacement. All variants passed prefix-invariance checks: appending future candles did not change earlier signals.

**Execution sensitivity, with selected parameters frozen.** Each number is OOS mean R. These scenarios assess assumptions; they are not new choices selected for headline performance.

| Indicator | Standard | All off-hours | Next-minute triggered exit | Ideal stop first | Bust 0.90% | Bust 1.00% |
| --- | --- | --- | --- | --- | --- | --- |
| Bollinger | -0.048 | -0.053 | -0.053 | -0.048 | -0.048 | -0.048 |
| Moving averages | -0.046 | -0.049 | -0.053 | -0.046 | -0.046 | -0.046 |
| MA ribbon | -0.067 | -0.069 | -0.070 | -0.065 | -0.067 | -0.065 |
| SuperTrend | -0.094 | -0.094 | -0.063 | -0.094 | -0.094 | -0.094 |
| Ichimoku | -0.164 | -0.164 | -0.151 | -0.164 | -0.164 | -0.164 |
| TD Sequential | -0.020 | -0.023 | -0.005 | -0.020 | -0.020 | -0.020 |
| RSI | -0.035 | -0.037 | -0.033 | -0.031 | -0.036 | -0.034 |
| MACD | -0.259 | -0.259 | -0.259 | -0.245 | -0.273 | -0.259 |
| Stochastic | -0.102 | -0.104 | -0.095 | -0.102 | -0.102 | -0.102 |
| Volume | -0.139 | -0.139 | -0.125 | -0.139 | -0.139 | -0.139 |


A delayed exit can occasionally improve a particular losing path; it is not uniformly worse and is not a fitted benefit. Both fee schedules are known formulas, but the live schedule is unknown. Neither candle execution convention proves the actual bust rate. The bundled JSON contains trade counts, drawdowns and bust rates for every sensitivity, not just mean R.

For scale, these are **analytical payout calculations**, not observed strategy results. A gross 2R target pays less than 2R after impact. Breakeven win rates below assume every trade is exactly a target or a −1R stop, with no time exits, gaps, or busts:

| Stop | Target | BTC net target R | ETH net target R | BTC breakeven win rate | ETH breakeven win rate |
| --- | --- | --- | --- | --- | --- |
| 0.20% | 0.40% | 1.675 | 1.642 | 37.4% | 37.8% |
| 0.35% | 0.70% | 1.712 | 1.693 | 36.9% | 37.1% |
| 0.50% | 1.00% | 1.728 | 1.714 | 36.7% | 36.9% |


**Combinations.** Two combinations were specified in the selection lock before their OOS evaluation; no combination grid was searched. They inherit their parent’s train/validation-selected timeframe, exits and filter. These are the two proposals evaluated, not profitable recommendations.

1. **Bollinger + RSI recovery:** the selected 5m Bollinger re-entry and EMA100 filter, further requiring RSI7 rising and below 50 for a long, or falling and above 50 for a short, on the same completed signal candle. Entry next open; stop 0.20%, target 0.40%, time stop six bars. This is the less-negative tested combination, suitable only as a clearly labeled future observation candidate; it did not improve on the parent in this test.

2. **MACD + ribbon alignment:** the selected 15m MACD zero cross and EMA100 filter, further requiring the mean of fast EMAs 3/5/8/10/12/15 above the mean of slow EMAs 30/35/40/45/50/60 for a long, below for a short. Alignment, not a simultaneous ribbon cross, is required. Entry next open; stop 0.50%, target 1.00%, time stop 24 bars. It performed worse than its parent and is rejected for live deployment.

| Combination | Trades | Win rate | Mean R | PF | Max DD (R) | Bust rate | 95% block interval |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MACD + ribbon alignment | 57 | 36.8% | -0.287 | 0.547 | 19.97 | 1.75% | [-0.576, 0.074] |
| Bollinger + RSI recovery | 45 | 42.2% | -0.076 | 0.782 | 10.35 | 0.00% | [-0.304, 0.195] |


The most defensible trading decision from these measurements is to remain flat. TD Sequential plus the selected EMA100 filter is the least-negative standalone package, but its 59-trade pooled sample and interval do not justify promoting it to an edge. Dropping losing assets or directions after seeing their test table would be additional overfitting. New combinations involving it would need an untouched future sample, rather than another optimization on these 12 days.

**Facts, inferences, and remaining questions.** Facts supported by retained inputs are the API responses, candle timestamps/counts, documented equations and stated protocol version. Backtest statistics are computations under the specified model. The inference is that these selected strategies have no demonstrated positive 100x edge over this test window. Uncertainty includes cross-venue/USDT basis, BBO versus trade-price candles, execution ordering, rounded contract constants, few independent test days, correlated assets, and the 720-candidate search. Unknown live fee settings, precise bust arithmetic, off-hours history, guaranteed stop support/latency, queue liquidity, and realizable PAPER value remain unresolved. Neither documentation nor this local check is an independent audit of the deployed contracts.

**Reproduction and local checks.** No third-party runtime packages are required: Python 3.10+ standard library suffices. From the repository root run `python3 research/backtest.py`, `python3 research/write_report.py`, then `python3 research/check.py`. All analysis inputs are included and these commands use no network. `research/fetch.py` and `research/validate_sources.py` are optional online acquisition tools, not needed to reproduce the results. The checks cover input hashes and minute continuity, OHLC validity, timeframe aggregation, no future-dependent signals across all variants, entry timing, both-touch/gap/hard-bust behavior, win/loss economics, holdback monotonicity, emissions with supplied state, split separation, nonoverlap, trade-ledger reconciliation, and the selection lock. Check output is in `research/check-results.txt`; native cross-check output is in `research/source-check-results.txt`. These are author-run checks, not independent certification.

Required outputs are `artifacts/report.md` and `artifacts/tuning.json`. Supporting deliverables are outside `artifacts/`: `README.md`, `research/`, `data/`, and `sources/`. Documentation provenance records identify retrieval time, raw-page hashes and short excerpts in `sources/manifest.json`; full articles are not redistributed. Native candle files identify retrieval time and hashes in `data/manifest.json`. No annualized return, Sharpe ratio, token price, or live execution claim is inferred from this short study.
