# HIVE holder and trading assessment

Research date: **30 September 2026, approximately 02:21–02:23 UTC**.
Contract supplied: **`0xCdaE63D95D6dd4f89f6e508c77bD4388b4e5C8Ab`**.

## Answer

**My provisional judgment is a 30% chance of touching $1 million FDV during the next seven days, conditional on the accessible market snapshots being accurate, the reported market cap approximating FDV, and trading still being functional.** The forecast window ends **7 October 2026 at 02:23 UTC**. This is a subjective scenario estimate, not a probability measured from verified onchain activity or a fitted prediction model. A reasonable *judgmental sensitivity range* is **10–60%**, not a statistical confidence interval.

**An unconditional, evidence-calibrated percentage cannot be established from the data retrieved.** Current holders, supply, executable liquidity, and buy/sell flows could not be independently verified. The available evidence supports a speculative possibility, not a conclusion that $1m is likely. If those conditions fail, discard the 30% estimate rather than treating it as a live trading signal.

“Reach” means at least one genuine executed swap implying price × fully diluted supply of at least $1m in the principal trading pool. It does not mean sustaining that valuation, or that holders can liquidate at it. The pool and supply must still be established. Whether HIVE has *already* reached $1m is unanswered.

## Identity and evidence quality

The exact address appears as **Project Hive / HIVE** in a Pump market listing and a Robinhood-focused alert channel. Robinhood Chain is therefore a working identification, **not a verified deployment finding**. The address alone does not identify an EVM chain. Robinhood’s own documentation lists mainnet chain ID **4663**, its public RPC, and Blockscout explorer; it does not establish that this particular token is deployed there. [Pump listing A](https://pump.fun/explore?outputCurrency=8o9USCoLWJDvWKE7hyvvogSQgsWT1wZ8irViuujhpump&page=2), [alert source](https://telemetr.io/ar/channels/1835601798-villaninoushat), [official network documentation](https://docs.robinhood.com/chain/connecting/).

No raw token balances, contract bytecode, supply call, swap receipts, or block-pinned holder list were successfully retrieved. The numerical observations below are **what accessible indexed pages reported**, not independently certified chain facts. Search retrieval occurred on September 30; the market pages were labeled crawled “yesterday,” without a precise measurement timestamp. Opening those market pages directly failed. Thus **current trading activity remains unverified**; these are recent discoverable snapshots.

## Holders: what can and cannot be inferred

An early alert, identifying the exact address and token age as 5h33m, reported **167 holders**, **23.24% held by the top ten**, and, among the first 70 buyers, **5 holding/buying more, 6 partly sold, and 59 fully exited**. It also reported $43.6k market cap, $68.6k volume, and $19.1k liquidity. These are historical, unverified alert figures; the volume window and concentration exclusions are unspecified. [Alert record](https://telemetr.io/ar/channels/1835601798-villaninoushat).

**Inference:** 59/70 = **84.3%** reported early-buyer exits suggests turnover rather than strong early retention. Only 11/70 = **15.7%** reportedly retained any position. That could reduce remaining early-buyer selling pressure, but does not identify who subsequently accumulated. Top-ten concentration of 23.24% would matter, yet wallet splitting, common funding, and pool exclusions could change its meaning. These figures cannot describe today’s holders.

**Unknown:** current holder count or growth; largest beneficial owners; top-one/top-five concentration; deployer and related-wallet balances; LP, burn, treasury and router exclusions; whales’ net buying/selling; realized profits; and address clustering. No claim that “smart money” is holding is substantiated. Traders are not synonymous with holders or independent people.

## Trading: recent reported snapshots

| Field | Listing A | Listing B |
|---|---:|---:|
| Displayed token age | 1 day | 22 hours |
| Market cap, explicitly labeled Mcap | $577,280 | $359,770 |
| Displayed ATH | $665,000 | $611,000 |
| Transactions | 5,744 | 5,160 |
| 24-hour volume | $608,960 | $536,550 |
| Traders | 1,821 | 1,579 |
| Displayed 1h / 6h / 24h change | +40.9% / +162.9% / +2,851.2% | +29.5% / +9.6% / +7,091.4% |

Sources: [Pump listing A](https://pump.fun/explore?outputCurrency=8o9USCoLWJDvWKE7hyvvogSQgsWT1wZ8irViuujhpump&page=2), [Pump listing B](https://pump.fun/explore?outputCurrency=2cJoqyRJ7SGi2HEsmux7ghAc8uV5vzeLEvxLicyZpump&page=3). Both rows match the supplied address. They are different snapshots, not simultaneous quotes or independent corroboration. Transaction/trader measurement windows are not explicit in the retrieved headings. Do not subtract the counts to derive new traders or trades.

**Inference:** reported volume and positive changes are consistent with strong speculative attention. A’s volume/Mcap is approximately **1.055×**. Gross turnover does not establish net capital inflow, organic demand, or absence of wash trading. The inconsistent snapshots and missing pool data prevent a reliable present-tense momentum assessment.

## Distance to $1m and probability reasoning

FDV requires an explicit fully diluted supply assumption. Neither verified maximum supply nor price was retrieved; **market cap is not automatically FDV**. Assuming equality and unchanged supply only:

| Starting valuation | Multiple needed | Price rise needed |
|---|---:|---:|
| Listing A: $577,280 | 1.732× | 73.23% |
| Listing B: $359,770 | 2.780× | 177.96% |
| A’s reported ATH: $665,000 | 1.504× | 50.38% |

These are arithmetic scenarios, not confirmed distances from the current FDV. A $422,720 valuation increase from A does **not** mean $422,720 of buying is required. Without pool reserves, active liquidity, fees, token taxes and seller behavior, required inflow cannot be calculated reliably.

The 30% judgment uses the following transparent, deliberately coarse scenario allocation:

| Mutually exclusive seven-day outcome | Subjective weight |
|---|---:|
| Renewed demand produces a genuine $1m FDV touch | 30% |
| Trading continues but never touches $1m | 40% |
| Demand or liquidity deteriorates, without a prior $1m touch | 30% |

The weights are analyst assumptions, **not empirical frequencies**. Reported activity and the conditional 73% upside requirement make a touch plausible. Early-holder turnover, missing ownership checks, unknown liquidity and stale observations keep the estimate below 50%. There is no comparable-token cohort, backtest, volatility series or calibrated base rate; the evidence cannot distinguish 30% precisely from nearby estimates.

Under a favorable hypothetical update—verified starting FDV near $577k, persistent net buying from distinct funded owners, growing holder breadth and stable sellable liquidity—I would move toward **60%**. Under an adverse update—FDV nearer $360k or below, fading demand, whale distribution or disappearing liquidity—I would move toward **10% or lower**. These are sensitivity judgments, not additional observations.

## Unanswered questions that could change the answer

1. Which chain and trading pool correspond to this contract, and what is its block-pinned total/max supply? Can supply expand?
2. What are current price, FDV and historical maximum FDV? Has the target already been met?
3. What are the current holder distribution and 24-hour/7-day holder changes after excluding protocol addresses and clustering related wallets?
4. What are 1h, 6h and 24h buy/sell amounts, unique net buyers, and large-holder flows? Are repeated counterparties inflating volume?
5. What liquidity is executable on a sale? Who can remove it? Are transfers taxed, restricted, upgradeable or controlled by privileged accounts?

## Retrieval limits and audit trail

The official Robinhood RPC returned HTTP 403 on `eth_chainId`. Blockscout token metadata, holders, transfers and contract endpoints also returned HTTP 403. Their attempted URLs, UTC request times and errors are preserved in [evidence/](evidence/). DEX Screener’s token API returned HTTP 403 through the shell; browser access also failed. Explorer pages on Blockscout, RobinScan and Ethereum Etherscan, plus the candidate GMGN page and Pump coin page, were inaccessible through the browser tool. These failures describe this research environment, **not evidence of a missing contract, zero holders, halted trading or fraud**.

The indexed public listings are attributable leads, not a replacement for successful primary-chain verification. No independent reviewer certified this report. Local checks cover output structure and arithmetic only. A verified onchain probability assessment remains incomplete despite delivery of this bounded research report.
