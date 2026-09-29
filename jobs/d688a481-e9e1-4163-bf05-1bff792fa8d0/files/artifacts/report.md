# Project Hive ($HIVE): holders, trading and the probability of $1 million FDV

**Assessment date: 29 September 2026, approximately 14:22–14:26 UTC.** Contract: `0xCdaE63D95D6dd4f89f6e508c77bD4388b4e5C8Ab`, **Robinhood Chain, chain ID 4663**. This is Project Hive, not the similarly named native Hive blockchain asset. The exact address matches both market APIs and the project's [published configuration](https://projecthive.fun/config.js); the network is documented by [Robinhood](https://docs.robinhood.com/chain/connecting/).

**My estimate is a 30% probability of reaching $1 million FDV within the next 30 days, with low confidence.** A reasonable subjective sensitivity range is **15–45%**. This is an analyst judgment informed by the observations below, **not a statistically calibrated forecast or a confidence interval**. There is no historical comparison cohort or validated predictive model behind it; onchain data cannot establish an objective percentage here.

For this report, “reach” means at least one completed hourly candle closing at or above **$0.001 per token** in the identified main pool, with supply remaining 1 billion. The horizon ends **29 October 2026 at 14:24 UTC**. This avoids counting a distorted quote in a dust pool. A brief intrahour touch is an easier event; maintaining that valuation for days is harder. Neither has been assigned the same probability. No investment suitability assessment is made.

## What is verified, and what is reported

**Direct onchain facts:** read-only calls to the official [Robinhood RPC](https://rpc.mainnet.chain.robinhood.com) returned chain ID 4663, token decimals of 18 and total supply of **1,000,000,000 HIVE**. Holder balance checks use block **75,725,118**, timestamp **2026-09-29 14:23:44 UTC**, hash `0x041d30789f35ceb1990e4202f459c00a225f1ae544e8381d08ce0b85588a13d2`. Requests and responses are saved in [rpc-pinned.json](evidence/rpc-pinned.json). This verifies supply at that block, not that future minting is impossible.

**Indexer observations:** DEX Screener and GeckoTerminal provide prices, pool statistics and holder summaries. These are provider calculations from indexed activity, not independently reconstructed swap logs. They were fetched within minutes but are not synchronized to the RPC block. Saved HTTP responses preserve the evidence even if the live links change.

## Holders: concentration is real, but contracts are not individual whales

[RobinScan's token page](https://robin.etherscan.io/token/0xCdaE63D95D6dd4f89f6e508c77bD4388b4e5C8Ab) reported **781 holders**, while [GeckoTerminal's token-info API](https://api.geckoterminal.com/api/v2/networks/robinhood/tokens/0xCdaE63D95D6dd4f89f6e508c77bD4388b4e5C8Ab/info) reported **792**, last updated **14:19:30 UTC**. Treat this as approximately **780–790 addresses**, not people. The disagreement could reflect indexing timing or methodology; it does not establish holder growth or decline.

I extracted the first 25 addresses from the [RobinScan holder table](https://robin.etherscan.io/token/generic-tokenholders2?a=0xCdaE63D95D6dd4f89f6e508c77bD4388b4e5C8Ab&s=1000000000000000000000000000&p=1) and checked their balances at the block above:

| Explorer rank | Address | HIVE at pinned block | Supply share | Attribution and limit |
|---|---|---:|---:|---|
| 1 | `0x4a56860781f90cd4d9d9883b33c2b9be94e88695` | 104,667,902 | 10.47% | Project config identifies `hiveStaking`; RPC confirms contract code. Beneficial owners and withdrawal terms not audited. |
| 2 | `0x8366a39cc670b4001a1121b8f6a443a643e40951` | 86,217,044 | 8.62% | RobinScan labels it Uniswap Pool Manager. Infrastructure balance, not an individual investor. |
| 3 | `0x267444d099b10fb5ed7c3cc7b7c767adca574952` | 81,632,653 | 8.16% | RPC confirms contract code; purpose, controller and restrictions unresolved. |
| 4 | `0xe5e702641ea86f4ae6cc3cdaed2b886f976be044` | 55,487,695 | 5.55% | RobinScan and project config identify Pons Meme Hook. Economic ownership/release rights unresolved. |
| 5 | `0x653c6c4859c69e5df0f86184f3203aeb2b3a3773` | 27,048,299 | 2.70% | Unattributed address. |

The sampled first ten hold **46.20%** and the first 25 **63.11%** of total supply. These are the explorer-selected addresses checked at one block, not a full independently reconstructed ranking. GeckoTerminal independently reports raw top-ten concentration of **46.12%**, and its cohort percentages imply **74.99% in the top 50**. [Saved holder data and RPC evidence](evidence/holders-parsed.json).

Subtracting staking, Pool Manager and Meme Hook from the sampled first ten leaves **21.57% of total supply in the other seven addresses**. This is a descriptive residual, **not an adjusted “top ten whale” statistic**: it neither replaces excluded addresses with the next ranks nor attributes staked balances to their owners. In particular, the unidentified 8.16% contract is material. Calling all 46% insider ownership would be unjustified; assuming the staking and hook balances can never create selling pressure would also be unjustified.

GeckoTerminal reports **0% at its identified developer address**, but this does not rule out related wallets. Its embedded pool-page security data also reports a different top-ten figure, **32.59%**, without a reconciled methodology. I use the transparent raw balance calculation rather than treating that adjusted-looking figure as verified. No funding-cluster analysis, beneficial-owner analysis, retention series, insider acquisition-cost analysis or holder-growth time series was completed. [Token-info API](https://api.geckoterminal.com/api/v2/networks/robinhood/tokens/0xCdaE63D95D6dd4f89f6e508c77bD4388b4e5C8Ab/info); [saved pool page](evidence/details.json).

## Current trading: strong turnover, weakening momentum

The reference pool is `0x4674f978aab6c373c1634a6729771d9bd6b97bbf25fdfa70d601a81a339f6974`, paired with native ETH (called WETH by GeckoTerminal). DEX Screener labels it Uniswap v4; GeckoTerminal labels the same pool Pons V2 Dex. The identifiers match, so these are not treated as separate pools.

| Main-pool measure | DEX Screener snapshot |
|---|---:|
| Price / FDV | $0.0003520 / $352,056 |
| Reported liquidity | $57,239.67 |
| 24-hour volume | $614,604.16 |
| 6-hour / 1-hour volume | $146,119.68 / $13,352.99 |
| 24-hour buys / sells | 2,539 / 2,037 |
| 6-hour buys / sells | 497 / 345 |
| 1-hour buys / sells | 56 / 46 |
| Price change: 24h / 6h / 1h | +541% / −23.95% / −6.03% |

Source: [DEX Screener exact-token API](https://api.dexscreener.com/latest/dex/tokens/0xCdaE63D95D6dd4f89f6e508c77bD4388b4e5C8Ab), saved in [http-attempts.json](evidence/http-attempts.json), record `dexscreener`. Pool creation was **28 September at 15:11:58 UTC**, so its “24-hour” statistics cover less than a full day of pool life.

**Calculated interpretation:** buys are **55.49% of trade count**; volume is **10.74× reported liquidity** and **1.75× FDV**. The latest hour's volume is **45.17% below** the preceding six-hour window's hourly average, which includes that latest hour. Activity is substantial relative to the pool's size, but turnover is slowing. More buys than sells do not demonstrate positive dollar net inflow: trade sizes differ, and arbitrage or repeated wallet activity can inflate counts.

[GeckoTerminal's same-pool API](https://api.geckoterminal.com/api/v2/networks/robinhood/pools/0x4674f978aab6c373c1634a6729771d9bd6b97bbf25fdfa70d601a81a339f6974) broadly corroborates ~$352,246 FDV and ~$613,514 volume. It reports **726 buyers and 648 sellers** over its 24-hour window, with overlap unknown; these cannot be added into a unique-trader total. Its ~$59,871 pool reserve differs from DEX Screener's ~$57,240. More substantially, its token endpoint reports only ~$31,777 total reserves, less than this pool alone. The reserve discrepancy is unresolved; no precise execution-depth estimate is justified.

DEX Screener returned 15 pools; the main pool accounts for **93.90% of their reported dollar liquidity**. One low-activity pool has an absurd price near $9.16×10^41, no reported liquidity and no FDV. It is excluded from valuation. Pool volumes are not summed as unique user demand. The main pool's [hourly OHLCV](https://api.geckoterminal.com/api/v2/networks/robinhood/pools/0x4674f978aab6c373c1634a6729771d9bd6b97bbf25fdfa70d601a81a339f6974/ohlcv/hour?aggregate=1&limit=100) contains 24 candles, with a highest observed price of **$0.000664747**, equivalent to about **$664,747 FDV**. Current price is roughly **47% below** that high. This history does not show $1 million reached in this pool; it does not establish an all-venue lifetime high.

## Why 30%, and what could change it?

At verified supply, **$1,000,000 / 1,000,000,000 = $0.001 per HIVE**. Relative to $352,056 FDV, the target requires **2.8405×**, or **+184.05%**. This is a price hurdle, not a requirement for $647,944 of new cash: FDV is a marginal-price valuation, not money deposited or realizable liquidation proceeds. Pool liquidity is not interchangeable with executable buy-side depth.

The **positive inference** is that hundreds of buying addresses, substantial turnover and a previous observed ~$665k valuation make another speculative expansion plausible. Project-identified staking holds 10.47% of supply, but absent withdrawal analysis I give it no credit as permanently removed supply.

The **negative inference** is stronger in the immediate snapshot: falling hourly and six-hour prices, slower volume, concentration in a small set of addresses, unresolved contract control and only about 23 hours of main-pool history. No repeatable revenue or staking-payout stream has been verified. The [project website](https://projecthive.fun/) describes using trading fees to operate AI-agent seats and reward stakers; that is a project claim, not demonstrated earnings in this analysis.

**30% is a deliberately coarse, below-even-odds judgment balancing those factors.** The 15–45% range represents how much the judgment could change with plausible answers to the unresolved questions, not measured statistical error. It would be false precision to claim that trade counts alone mathematically produce 30%. A calibrated percentage remains unanswered without a comparable-token cohort and out-of-sample validation.

I would move toward the upper end if subsequent observations showed increasing independent buyers, recovery above the observed ~$665k high with stable liquidity, and verified restrictions on large contract balances. I would move toward the lower end if turnover and holder participation contracted, major addresses sent tokens into selling routes, or liquidity became removable or disappeared. These are conditional monitoring criteria, not findings that those events have occurred.

## Uncertainty, unanswered questions and reproducibility

- **Ownership and selling risk:** who controls the 8.16% contract and the other large balances? How concentrated are underlying staking depositors? What are withdrawal, vesting and hook permissions?
- **Liquidity and contract risk:** liquidity locking is unverified. GeckoTerminal's lock percentage is null and its page flag is false; neither substitutes for inspecting positions and permissions. Token minting, upgrade, blacklist and fee powers were not audited. Automated “not a honeypot” output is not a guarantee.
- **Organic activity:** no swap-by-swap wash-trading, funding-link or MEV analysis was completed. Indexed buyers are addresses, not independent people. Buy/sell dollar flow and executable slippage remain unknown.
- **Historical context:** no reliable holder-change series, complete launch/bonding-curve history or comparable-token success base rate is available in this report. Cached search results were not used as current readings.
- **Source access:** initial requests failed; retrying public GETs succeeded. Blockscout endpoints returned 403, and its alternative API required a key/payment (402). RobinScan and read-only RPC supplied the holder evidence instead. Requests, failures and timestamps are retained; failures are not treated as zero activity.

Run `python3 artifacts/check.py` offline to recompute supply, sampled concentration, target multiples and market ratios from the saved responses. [Calculated results](evidence/calculations.json) and [README](README.md) describe the evidence package. These checks validate arithmetic and file consistency; they do not independently certify providers, contract safety or the forecast.
