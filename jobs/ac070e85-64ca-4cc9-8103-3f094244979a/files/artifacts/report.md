# BTC-USD PaperTrade scalp decision — 2026-10-12 07:54 UTC

## Decision (the required output)

```json
{"direction":"long","leverage":500,"take_profit_bp":8,"take_profit_price":84023.67,"bust_distance_bp":15.2,"bust_price_estimate":83828.89,"expected_net_return_on_margin_pct":27.68,"max_hold_minutes":30,"confidence":0.52,"regime":"ranging","key_levels":{"support":83927,"resistance":84020},"entry_mid":83956.5,"data_time_utc":"2026-10-12T07:54:15Z","reasoning":"BTC is up about 120 bp over 24h and the 15m EMA9 (84000) is above the EMA21 (83926). After a rejection from 84315, price is sitting on the 6h 5m-VWAP (83932) and the 1h lows (83927-83935), which held several times. The perp mid is 2.9-3.6 bp below the oracle price, so convergence would favor longs. Current 1m ATR is only about 3.5 bp in quiet Monday early-European trade, so 500x (15.2 bp bust) keeps the bust beyond the hour's range. An 8 bp target (84024, the recent 1m spike high near 84020) keeps about 69% of the gain after the haircut and should be reachable inside 30 minutes.","risks":"Losing the 83927 support could set off a continuation of the pullback from 84315 toward the 83740-83840 area of earlier 15m closes, which would cross the 83829 bust. A sudden volatility burst (15m ATR is about 26 bp) could do the same."}
```

## Evidence (facts: measured from Hyperliquid's public `info` API at 07:53:29 and 07:54:15 UTC)

All data comes from POSTs to `https://api.hyperliquid.xyz/info`: `l2Book` (nSigFigs 5), `candleSnapshot` 1m/60 min, 5m/6 h and 15m/24 h, `metaAndAssetCtxs`, `fundingHistory` (24 h) and `recentTrades`.

| Item | Value |
|---|---|
| Best bid / ask (07:54:15 refetch) | 83956.0 / 83957.0 → **entry mid 83956.5** |
| First fetch mid (07:53:29) | 83955.5 |
| Mark / oracle (refetch) | 83956.0 / 83981.0; premium −0.000286 (perp is ~3 bp below the oracle) |
| Funding (hourly) | +0.0000098; it stayed between +0.0000037 and +0.0000125 for the last 8 hours (small, longs pay) |
| Open interest / 24h notional | 38,423 BTC / $1.60B; prevDayPx 82970 |
| 1m (60 bars) | ATR14 29.7 = **3.5 bp**; high 84315, low 83927; VWAP 84130; EMA9 83965 < EMA21 83978; change over the hour −4 bp |
| 5m (6 h) | ATR14 100 = 11.9 bp; VWAP 83932; EMA9 ≈ EMA21 ≈ 84003; change +59 bp |
| 15m (24 h) | ATR14 215 = **25.6 bp**; range 82916–84315; VWAP 83713; EMA9 84000 > EMA21 83926; change +120 bp |
| Book top-20 depth | First fetch: bid 37 / ask 108 BTC. Refetch 46 s later: bid 77 / ask 30 BTC. The imbalance flipped, so I treat it as noise. |
| Recent 1m closes | 83954, 83935, 83935, 83949, 83955, 83943, 83941, 83945, 84020, 83949, 83984, 83964 |

## Payoff arithmetic (computed with the brief's haircut formula)

At 500x, net return on margin if the take-profit hits, along with a **driftless random-walk** probability of hitting the TP before the 15.2 bp bust (P = bust / (bust + TP)):

| TP bp | Net RoM | Keep share | P(TP first), no edge | EV per unit margin, no edge |
|---|---|---|---|---|
| 5 | 15.2% | 61% | 0.75 | −0.13 |
| 8 | **27.7%** | 69% | 0.66 | −0.16 |
| 10 | 36.2% | 72% | 0.60 | −0.18 |
| 12 | 44.8% | 75% | 0.56 | −0.19 |

Higher leverage is worse under the same model. At 1000x, a 5 bp TP gives P ≈ 0.51 and EV ≈ −0.34.

## Inferences (my judgment, not measured)

- **Regime: ranging.** The higher timeframes trend up, but the last hour is a pullback that is consolidating on VWAP support.
- **Why long:** the 24h and 15m trend is up, price is holding at the 6h VWAP and the 1h lows, and the perp trades at a discount to the oracle, which tends to mean-revert. The case for short is real: the rejection from 84315, price below the 1h VWAP, and a 1m EMA9 below its EMA21. That is why confidence is barely above a coin flip.
- **Why 500x / 8 bp / 30 min:** the minimum leverage gives the widest bust distance (15.2 bp, about 4× the current 1m ATR). 8 bp is a reasonable balance between the haircut (69% kept) and how reachable the target is, and it lines up with the 84020 spike high. 30 minutes is about one to two 15m ATRs of time. A longer hold mostly adds bust risk.

## Uncertainty and open questions

- **Structural negative expectancy.** Under a no-edge random walk, every allowed combination of leverage and TP has negative expected value, because the bust forfeits 100% of margin while wins are haircut. The trade is profitable in expectation only if the directional read is right well above ~66% of the time at these settings. My confidence of 0.52 does not reach that. The user should know that the trade is likely to lose money in expectation.
- The time-limit exit outcome (neither TP nor bust inside 30 minutes) is not modelled.
- I had no liquidation-heatmap or cross-exchange order-flow data. The `recentTrades` sample was only 10 prints over about 2 seconds, which is not informative.
- **Macro (web search, secondary sources, not verified against primary):** today is Columbus Day, so the US bond market is closed ([thriveinmarkets](https://thriveinmarkets.com/calendar/2026-10-12/)). US CPI is reportedly due Wed 2026-10-14 at 08:30 ET ([fedratecalc](https://fedratecalc.com/us-economic-calendar/october-2026/), [investinglive](https://investinglive.com/news/week-ahead-us-inflation-and-retail-sales-lead-a-busy-economic-calendar-be-aware/)), and the FOMC meets Oct 27–28. Nothing is scheduled inside the holding window. I found no reliable BTC news for today. One aggregator item described early October as range-bound between 83.5k and 86.6k ([Pluang](https://pluang.com/en/news-feed/prediksi-harga-bitcoin-enam-dari-delapan-oktober-naik)), which is consistent with the API data but unverified.
- The data is a snapshot. If entry happens more than a minute or two after 07:54:15 UTC, the levels above should be recomputed.
