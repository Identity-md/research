# Fren Pet: the network cost of a Bonk

**A completed, direct two-transaction Bonk averaged 0.000002004183 ETH ($0.005363), equivalent to 2,004.183 Gwei in total network fees.** The gas-weighted L2 execution price was **0.00616689 Gwei per gas**. This result covers **3,475 matched Bonk Commit + Bonk Reveal pairs** at Base contract [`0x0e22B5f3E11944578b37ED04F5312Dfc246f443C`](https://base.blockscout.com/address/0x0e22B5f3E11944578b37ED04F5312Dfc246f443C). It is not the fee for just one transaction. [Computed results](summary.json), [every pair and its transaction hashes](bonks.csv).

**Observation window:** 24 September 2026 03:00:00 UTC through 25 September 2026 03:00:00 UTC, end-exclusive. This is the latest complete, half-hour-aligned 24 hours at the start of research (03:16 UTC on 25 September), deliberately omitting the unfinished interval after 03:00. It is a frozen historical snapshot, not a rolling “now minus 24 hours” value. Blocks **51,714,727–51,757,926**, inclusive; timestamps of the adjacent blocks establish both boundaries. [Query manifest](evidence/manifest.json), [boundary block responses](evidence/boundary-blocks.json).

## Results

| Included action | Transactions / Bonks | Mean network fee, ETH | Mean network fee, USD | Mean total fee, Gwei | Mean gas consumed |
|---|---:|---:|---:|---:|---:|
| Commit in matched pairs | 3,475 | 0.000001092598 | $0.002924 | 1,092.598 | 171,848.94 |
| Reveal in matched pairs | 3,475 | 0.000000911585 | $0.002439 | 911.585 | 148,078.92 |
| **One Bonk: Commit + Reveal** | **3,475** | **0.000002004183** | **$0.005363** | **2,004.183** | **319,927.86** |

Gas is a quantity of execution work; Gwei is a denomination of ETH. To avoid conflating them, the table gives **the total fee denominated in Gwei**, while the headline separately gives **Gwei per gas**. One ETH = 1 billion Gwei. Neither gas limits nor maximum fee caps are treated as amounts paid. The median Bonk fee was 0.000001973964 ETH ($0.005282); the empirical 95th percentile was 0.000002249279 ETH ($0.006019). [Receipt-derived transaction data](transactions.csv).

**USD convention:** all ETH costs are translated at **$2,675.835/ETH**, the [Coinbase ETH/USD spot endpoint](https://api.coinbase.com/v2/prices/ETH-USD/spot), retrieved **2026-09-25T03:20:10.546747+00:00**. This is a reporting-time valuation, not what ETH was worth at each transaction's timestamp, nor a claim about dollars actually paid. The exact response is [saved locally](evidence/usd-quote.json).

## Thirty-minute heatmap

![Average total fee per Bonk in 48 half-hour intervals, including sample counts](heatmap.svg)

[Open the standalone heatmap](heatmap.svg) · [Exact 48-bin values in CSV](intervals.csv).

Each cell is the arithmetic mean **combined Commit + Reveal fee** of pairs whose Reveal occurred in that half-hour. Both transactions must fall inside the overall 24-hour window; a Commit may lie in an earlier cell. Intervals are left-inclusive and right-exclusive. USD uses the same fixed quote as the overall average. Darker means more expensive, and `n` is the number of pairs. Empty intervals would be marked “No observations,” never zero. The overall average weights each Bonk equally; it is **not** an unweighted average of cell means.

## Evidence and method

1. **Enumerate activity.** Downloaded the [Blockscout transaction history for the fixed block range](https://base.blockscout.com/api?module=account&action=txlist&address=0x0e22B5f3E11944578b37ED04F5312Dfc246f443C&startblock=51714727&endblock=51757926&sort=asc), yielding 8,572 unique direct transactions. The initial full-window response omitted two calls; a fresh full-window response and two separate half-window queries agreed on exactly the same hash set. Both missing receipts were added before computing results, yielding one additional completed pair. The initial response is retained as `evidence/transactions-initial.json`. Also fetched **all 43,656 logs emitted by the contract** with `eth_getLogs` from [Base's public RPC](https://mainnet.base.org) in 22 contiguous block ranges. [Raw transaction history](evidence/transactions.json); individual log responses and queries are in `evidence/logs-*.json`.
2. **Identify the requested actions.** Filtered direct calls to the specified address by calldata selectors `0x3935a788` (Bonk Commit) and `0xa4333d91` (Bonk Reveal). Historical decoded examples establish the [Commit signature](https://basescan.org/tx/0x451bd1ad1f3d698d538f55255262fe892d498fa4baf8bb1b533ad802d77e083c) and [Reveal signature](https://basescan.org/tx/0x75405c56d5274315110da9e765f143e3d8f964fc0efed7d340e48d489aad64a7); those old transactions are **not** used in the fee sample. Downloaded a receipt for every one of the **7,130** matching current-window calls. Receipt status distinguishes success from reversion. Logs alone cannot supply fees or reveal reverted calls, so transaction inputs and receipts are necessary supplements.
3. **Infer and validate pairs.** In block/transaction order, matched each successful Reveal to the preceding unmatched successful Commit with the same sender and calldata attacker ID. All 3,475 successful Reveals matched; one successful Commit remained unmatched. Every successful direct call's contract event was reconciled with the independent log download, and all matched Reveals had **no intervening Commit event for that attacker anywhere in the contract logs**, including wrapped calls. Commit event payloads matched the first four calldata arguments. Reveal validation accepts both observed outcome topics; a successful transaction does not necessarily mean a winning game outcome. Full topic hashes and checks are in [the offline analysis](../scripts/analyze.py). Pairing is an explicit inference from ordered state activity, not a contract-provided unique Bonk transaction-pair ID or a cryptographic verification of the reveal preimage.
4. **Compute actual fees.** For each receipt, `fee_wei = gasUsed × effectiveGasPrice + l1Fee`. Sum the two fees per pair, then divide their total by 3,475. ETH = wei / 10^18; total Gwei = wei / 10^9; USD = ETH × the recorded quote. Gas-weighted execution price = total L2 execution fees / total gas used / 10^9. Base documents [L2 execution and L1 data/security fees](https://docs.base.org/specifications/transactions/network-fees). Three [saved explorer cross-checks](evidence/fee-crosschecks.json) agree exactly with this formula. No additional fee component is added; no separate operator fee appears in these receipts, and this matches the checked explorer totals. The L1 component accounts for **1.558%** of the matched-pair fees.

## What a player can take from this

**Observed:** the cheapest average interval was **2026-09-24 22:30:00 UTC**, at **$0.005019** per Bonk (113 pairs). The most expensive was **2026-09-24 08:00:00 UTC**, at **$0.010374** (33 pairs). Their difference is **$0.005355** per Bonk, or **106.7%** above the cheaper interval. This comparison describes this sample only; gas consumption, game state and player mix can also change a cell's average. It does not establish a recurring cheapest time of day.

**Observed:** 175 Commit calls and 4 Reveal calls reverted: **2.51% of direct Bonk-related calls**. They still consumed **0.000082717863 ETH ($0.221339)** in aggregate. These costs are excluded from the successful-pair headline. Spreading those failed-call costs across this window's completed pairs would add $0.000064 per Bonk, but this is a population-level overhead estimate, not an attribution of retries to individual pairs. One unmatched successful Commit is also excluded. [All successes and failures](transactions.csv).

**Inference for budgeting:** plan for two transaction fees and some possible failed-call overhead. Of the matched pairs, 3,472 revealed within one minute; the maximum observed delay was 184.5 minutes. That describes behavior, not a safe reveal deadline. This analysis did not establish the game's timing rules, and it does not recommend delaying a Reveal to chase a cheaper cell.

## Scope, uncertainty and unanswered questions

- **Scope matters:** the full log scan contains 18,953 Commit events and 18,952 events with the two observed Reveal-outcome topics. Most therefore occur outside the direct two-transaction sample. The headline answers the requested **direct Bonk Commit + Bonk Reveal flow**, not the average across every automated, batched or wrapped Bonk in the game. Allocating one wrapper transaction's fee among multiple actions would require a separate attribution model; no such all-game average is claimed.
- **Coverage and provider limits:** transaction enumeration comes from Blockscout, with split-query consistency checks; independent RPC logs corroborate successful selected actions. A full scan of every block's transactions was not performed, so a provider omission of a reverted transaction cannot be independently ruled out. Saved responses are attributable provider observations, not independently verified block proofs. Blocks were observed after inclusion, not accompanied by a finalized-L1 proof.
- **Excluded costs:** token transfers, game stakes/payments, approvals, funding or bridge transactions, and wallet/service charges outside these receipts. The estimate measures network fees, not the total economic cost or expected return of playing.
- **Unanswered:** historical transaction-time USD spending; fees allocated per Bonk inside wrappers; causes of individual reversions; whether this one day's timing pattern persists. No confidence interval or causal timing claim is inferred from the 48 descriptive means.

## Reproduce and inspect

From the repository root, run `python3 scripts/analyze.py` and `python3 scripts/write_report.py` with Python 3; no network or third-party packages are needed. The first script rebuilds the CSVs, JSON summary and SVG from delivered evidence and asserts receipt coverage, fees, event consistency, pairing, time boundaries and weighted-bin reconciliation. [Local check result](checks.txt). These checks were performed locally and are **not an independent audit**. [README](../README.md) describes files and limits.
