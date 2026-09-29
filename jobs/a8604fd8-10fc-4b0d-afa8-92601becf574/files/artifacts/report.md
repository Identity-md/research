# Robinhood Chain: daily TVL and bridge inflows

Research date: **30 September 2026, Australia/Adelaide**. Retrieval began **29 September 2026, 22:04 UTC** (30 September, 07:34 ACST). All amounts below are USD.

**Answer:** DefiLlama’s latest retrieved midnight TVL snapshot is **$1,019,594,540 ($1.0196 billion), at 29 September 2026 00:00 UTC**. TVL fell **0.36% over one day**, rose **0.24% over three days**, and rose **2.52% over seven days**. Exact bridge inflows for matching periods could not be verified: the historical bridge API returned HTTP 402, and accessible indexed dashboard figures lack an exact observation time. This is a verified provider-data TVL calculation and a partial answer on bridge flows, not a complete flow measurement. [TVL source](https://api.llama.fi/v2/historicalChainTvl/Robinhood%20Chain).

## Windows and definitions

Use the last **completed UTC days**, ending at 29 September 00:00 UTC. The UTC day of 29 September was still in progress at retrieval, despite the local date being 30 September. These are not rolling windows ending at research time, nor Adelaide calendar days.

TVL means the provider’s chain DeFi TVL series, not Robinhood brokerage assets or canonical bridge custody. TVL is a stock: do not sum daily TVL to obtain a period total. “Daily close” below means the next midnight API snapshot, an explicit reporting convention rather than a claim about the provider’s underlying block selection. Source timestamps and raw values are preserved in [tvl.json](evidence/tvl.json).

For the requested bridge metric, **gross inflow** means USD value arriving on Robinhood Chain through tracked bridges. **Net flow = gross inflow − outflow**. A change in TVL is not a measurement of either: asset prices and movement into or out of DeFi can change TVL without bridging. Robinhood documents a canonical Ethereum bridge and multiple partner routes, so measuring only the canonical bridge would leave other routes out. [Official bridge documentation](https://docs.robinhood.com/chain/bridging/).

## Last 1, 3 and 7 completed days

Each interval includes its start and excludes its end; both boundaries are 00:00 UTC. TVL changes are calculated from the two boundary snapshots.

| Window | UTC boundaries | Starting TVL | Ending TVL | TVL change | Gross bridge inflow, same window |
| --- | --- | ---: | ---: | ---: | --- |
| 1 day(s) | 2026-09-28 → 2026-09-29 | $1,023,241,040 | $1,019,594,540 | $-3,646,500 (-0.36%) | Unverified |
| 3 day(s) | 2026-09-26 → 2026-09-29 | $1,017,195,976 | $1,019,594,540 | $+2,398,564 (+0.24%) | Unverified |
| 7 day(s) | 2026-09-22 → 2026-09-29 | $994,539,923 | $1,019,594,540 | $+25,054,617 (+2.52%) | Unverified |

## Day by day

Seven completed days, 22–28 September. The last one-day window is 28 September; the last three-day window is 26–28 September. All TVL cells come from the [DefiLlama historical chain API](https://api.llama.fi/v2/historicalChainTvl/Robinhood%20Chain); changes are derived, not additional observations.

| UTC day | Opening TVL | Next-midnight TVL | Daily change | Gross bridge inflow |
| --- | ---: | ---: | ---: | --- |
| 2026-09-22 | $994,539,923 | $1,009,130,116 | $+14,590,193 (+1.47%) | Unverified |
| 2026-09-23 | $1,009,130,116 | $996,432,450 | $-12,697,666 (-1.26%) | Unverified |
| 2026-09-24 | $996,432,450 | $1,001,738,252 | $+5,305,802 (+0.53%) | Unverified |
| 2026-09-25 | $1,001,738,252 | $1,017,195,976 | $+15,457,724 (+1.54%) | Unverified |
| 2026-09-26 | $1,017,195,976 | $1,025,491,399 | $+8,295,423 (+0.82%) | Unverified |
| 2026-09-27 | $1,025,491,399 | $1,023,241,040 | $-2,250,359 (-0.22%) | Unverified |
| 2026-09-28 | $1,023,241,040 | $1,019,594,540 | $-3,646,500 (-0.36%) | Unverified |

Machine-readable results: [daily-tvl.csv](daily-tvl.csv). Dollar precision reflects API output, not independently established valuation accuracy.

## What bridge evidence is available?

**Provider-reported, cached context only — not aligned with the TVL windows above.** The indexed investor dashboard, labelled “crawled 2 days ago” by the search tool, reported these Robinhood Chain values. Its actual measurement cutoff was not supplied. [DefiLlama bridge inflows by chain](https://investors.defillama.com/bridges/chains).

| Source’s window label | Gross deposits/inflows | Withdrawals/outflows | Net flow |
| --- | ---: | ---: | ---: |
| 24h | $46.09 million | $35.70 million | +$10.39 million |
| 3 days | Not supplied | Not supplied | Not supplied |
| 7d | $534.08 million | $466.72 million | +$67.36 million |

The public-domain version, labelled “crawled 4 days ago,” instead showed 24h deposits **$70.97m**, withdrawals **$49.31m**, net **+$21.67m**; and 7d deposits **$602.72m**, withdrawals **$515.07m**, net **+$87.65m**. These are distinct cached observations, not an uncertainty range or figures to combine. The $0.01m discrepancy in subtracting the displayed 24h numbers is consistent with rounding, but unrounded data were unavailable. [Public bridge inflows table](https://defillama.com/bridges/chains).

The chain overview also displayed a metric labelled “Inflows (24h)” of **$6.71m** in an indexed snapshot marked “crawled today.” Without matched deposit/outflow records and a cutoff, that label alone is insufficient to treat it as gross inflow or reconcile it to the tables. [Chain overview](https://investors.defillama.com/chain/robinhood-chain).

**Do not multiply a 24-hour number by three or divide a seven-day total to manufacture the missing three-day result.** Likewise, canonical bridge “Bridge Volume” and “Bridged TVL” are not substitutes for all-route directional inflow.

## Evidence, interpretation and remaining uncertainty

- **Observed facts:** The historical TVL endpoint returned HTTP 200 and dated numeric observations. The bridge-volume endpoint returned HTTP 402 Payment Required. Direct chain/bridge dashboard requests returned HTTP 403; web search exposed the cached provider figures above. See [retrieval log](evidence/retrieval.json) and [bridge observation notes](evidence/bridge-observations.md).
- **Calculated findings:** One-, three- and seven-day TVL changes are endpoint differences; percentages divide by starting TVL. TVL is higher over the week but lower on the final day. This says nothing by itself about fresh capital entering the chain.
- **Inference:** Different dashboard values plausibly reflect different cache times or windows. That explanation is not verified, and no preferred “current” flow total is selected.
- **Uncertainty:** DefiLlama is the primary publisher of these analytics, not an independent on-chain audit. This work did not validate its pricing, contract coverage, double-counting rules, revisions, or bridge adapter completeness. Midnight timestamp labels do not prove exact block-level valuation times.
- **Unanswered:** Daily gross inflow/outflow and exact 1/3/7-day sums for the defined UTC intervals; precise cutoffs and gross-versus-net meaning of the overview’s “Inflows” label; whether all official partner routes are indexed.

To close the flow gap requires timestamped directional bridge records or a dated daily export covering 22 September 00:00 through 29 September 00:00 UTC, with route coverage and USD valuation defined. Sum inbound daily values over 28 September, 26–28 September, and 22–28 September respectively; report outbound and net values separately. No missing value in this report means zero.

## Local checks

The offline check confirms eight consecutive midnight boundary observations, all seven daily rows, and the 1/3/7-day calculations against the saved response. It checks evidence consistency and file integrity, not the underlying economic truth. No independent review was performed.
