# Prediction Market challenge: measured improvements and remaining handoff gap

The best reported eligible results across the two merges are **s1-queue, s2-stock, s3-flow and s4-flow**. Their quarter-weighted gains imply **+1.615075** overall mean edge, calculated from the reported rounded differences; this is not a measured combined strategy or a new leaderboard result. Exact executable implementations of these four selections are **not available in the supplied merges**. This report is a results write-up, not a submission-ready strategy handoff. [M1 §4–5; M2 §1, §3.1, §6]

## Sources and scope

- **[M1](https://api.imd.fun/artifacts/5201f7d9326a763a76f7bcae9a2cb4a627bc496dbc1f007ae8c520ec8d2eadfd)**: Merge 01, supplied as `.imd/reads/artifacts/merge-01`; 20 items. Its HTTP body was retrieved and its SHA-256 matched the full identifier in this link.
- **[M2](https://api.imd.fun/artifacts/53ce6cd623c486ae2dbbc3c31c4ad8bc617f03ba9c6daf8c8706bdd662fbe664)**: Merge 02, supplied as `.imd/reads/artifacts/merge-02`; 12 items. Its HTTP body was retrieved and its SHA-256 matched the full identifier in this link.
- **B (assignment brief)**: the requester's dated standings, scoring description, disjoint-spread rule and earlier-seat measurements. These are supplied context, not independently refreshed leaderboard observations.
- **[Base](https://api.imd.fun/artifacts/41fa8829432f502a00c5302c0e2200b475c5c2e100a2a16b086aaab0ce62a395)**: the original public strategy JSON. Retrieval succeeded; the SHA-256 of its UTF-8 `code` field was `dcf68e0c9a7b06f90cf70a833357b60e2208b5b3e2971e7dddf02986d4747076`, confirming the reviewer's original-base observation. It does not supply the selected improvements.

Bracketed M1/M2 references below identify sections of these immutable sources. Item names identify the underlying seats as reported by the merges; individual item JSONs were not supplied. No simulations were rerun for this write-up. No code is included, as the brief requests.

## Goal and interpretation

On **2026-11-06**, the network stands **3rd of 186 at 106.80**, comprising **129.22** retail edge and **22.42** lost to the arbitrageur. First is **109.59 (130.77, 21.18)**; second is **109.43 (127.73, 18.31)**. The challenge scores mean edge over **200 simulations**. The base reads the rival's first-step spread as `self.s`; spreads **1 to 4** each occur in a quarter of runs. The brief's approximate unseen means are **35, 84, 123 and 154** for those spreads. These contextual numbers come from B, not the merges' holdout sample. [B]

The merges use unseen seeds **60000–67999**, filtered by spread. M1 reports base means **41.78494849744236**, **75.37891657984132**, **118.8166859338749**, **163.47813945343543**, on **1969**, **1987**, **2035**, **2009** runs respectively. Their difference from B's approximate means reflects different unseen sets. M1 says spread 4's base is not cross-checked within that merge; M2 subsequently reports agreement among its spread-4 seats. [M1 §3; M2 §1]

A candidate must gain on unseen runs, have no simulation failures, preserve other spreads run by run, and be no slower than the base. Separate spread gains add because their branches are disjoint; gains within a spread need joint testing. Positive arbitrage difference below means reduced arbitrage loss. Component figures are independently rounded and need not sum to the displayed total. [B; M1 introduction, §4–5; M2 introduction, §4]

## One row per item

Values are copied at the precision supplied by the merges. “NR” means not reported in the supplied merge, not zero. Times are seconds, **base → returned file**; CPU timings are marked. “900” means reported identical on 900 other-spread runs. “Base” means unchanged code, hence identical by construction; an executed check is distinguished where supplied. The final column cites the evidence and records eligibility caveats.

| Spread / part (item) | Unseen mean difference (SE) | Retail difference | Arbitrage difference | Other spreads identical? | Seconds: base → file | Source / status |
|---|---:|---:|---:|---|---|---|
| 1 / asks (s1-asks) | NR (NR); base unchanged | NR | NR | Base; check NR | NR | M1 §1–2: only 16 unseen runs; no gain |
| 1 / bids (s1-bids) | +0.4361 (0.129) | -0.611 | +1.047 | Yes, 900 | 90.81 → 90.33 | M1 §4: eligible |
| 1 / clock (s1-clock) | NR (NR); base unchanged | NR | NR | Base; 0 runs checked | NR | M1 §1–2: 249 unseen seeds; no gain |
| 1 / flow (s1-flow) | +1.2750 (0.229) | +0.955 | +0.320 | Yes, 900 | 97.14 → 95.32 | M1 §4: eligible |
| 1 / free (s1-free) | +0.2590 (0.057) | +0.265 | -0.006 | Yes, 900 | 96.77 → 96.61 | M1 §4: eligible |
| 1 / middle (s1-middle) | +0.0683 (0.0065) | -0.023 | +0.091 | Yes, 900 | 198.93 → 168.60 (CPU) | M1 §4: eligible; scorer drift, §1 |
| 1 / queue (s1-queue) | +2.2637 (0.354) | +2.208 | +0.056 | Yes, 900 | 210.61 → 206.80 | M1 §4: selected |
| 1 / stock (s1-stock) | NR (NR) | NR | NR | NR | NR | M1 §4: no purchase control passed validation |
| 2 / asks (s2-asks) | Not measured | Not measured | Not measured | Not checked | Not timed | M1 §2: blocked; zeros were placeholders |
| 2 / bids (s2-bids) | +0.2860 (0.081) | -0.167 | +0.453 | Yes, 900 | 85.64 → 85.01 | M1 §4: eligible |
| 2 / clock (s2-clock) | -0.294 (0.503) | NR | NR | NR | NR | M1 §4: failed holdout gain |
| 2 / flow (s2-flow) | +0.6075 (0.183) | +0.290 | +0.318 | Yes, 900 | 152.27 → 154.76 | M1 §4: slower, ineligible |
| 2 / free (s2-free) | +0.6075 (0.183) | +0.290 | +0.318 | Yes, 900 | 515.33 → 503.38 | M1 §4: eligible; same reported policy as stock |
| 2 / middle (s2-middle) | NR (NR); below base | NR | NR | NR | NR | M1 §4: failed holdout gain |
| 2 / queue (s2-queue) | +0.4851 (0.347) | +1.601 | -1.116 | Yes, 900 | 71.89 → 72.65 | M1 §4: slower, ineligible |
| 2 / stock (s2-stock) | +0.6075 (0.183) | +0.290 | +0.318 | Yes, 900 | 147.27 → 146.75 | M1 §4: selected |
| 3 / asks (s3-asks) | +0.8625 (0.335) | +1.094 | -0.231 | Yes, 900 | 119.96 → 119.36 | M1 §4: eligible, superseded by flow |
| 3 / bids (s3-bids) | -0.0163 (0.1135) | NR | NR | NR | NR | M1 §4: failed holdout gain |
| 3 / stock (s3-stock) | Not measured | Not measured | Not measured | Not checked | Not timed | M1 §2: blocked; no Python interpreter |
| 3 / flow (s3-flow) | +2.445 (0.665) | -1.280 | +3.725 | Yes, 900 | 209.90 → 207.19 | M2 §1: selected; 0 failures |
| 3 / free (s3-free) | +0.946 (0.207) | +0.934 | +0.013 | Yes, 900 | 106.24 → 106.81 | M2 §1, §3.2: slower in primary timing |
| 3 / clock (s3-clock) | +0.258 (0.067) | -0.139 | +0.397 | Yes, 900 | 131.23 → 130.13 | M2 §1: eligible; 0 failures |
| 3 / middle (s3-middle) | 0 (NR) | 0 | 0 | Base; 0 runs checked | same file; seconds NR | M2 §1, §3.4: no gain; no unseen scoring |
| 3 / queue (s3-queue) | 0 (NR) | 0 | 0 | Base | 313.10 → 301.44 (same file, CPU) | M2 §1, §3.5: returned base; rejected policy lost |
| 4 / flow (s4-flow) | +1.1441 (0.340) | -0.596 | +1.740 | Yes, 900 | 334.60 → 333.71 (CPU) | M1 §4: selected |
| 4 / bids (s4-bids) | +0.606 (0.084) | -0.231 | +0.837 | Yes, 900 | 163.13 → 159.97 | M2 §1: eligible; 0 failures |
| 4 / asks (s4-asks) | +0.330 (0.077) | +0.427 | -0.097 | Yes, 900 | 39.87 → 39.79 | M2 §1: eligible; 0 failures |
| 4 / queue (s4-queue) | +0.278 (0.070) | +0.585 | -0.308 | Yes, 900 | 164.65 → 163.91 | M2 §1: eligible; 0 failures |
| 4 / middle (s4-middle) | +0.258 (0.136) | -1.616 | +1.874 | Yes, 900 | 46.31 → 46.45 | M2 §1: slower, ineligible |
| 4 / free (s4-free) | +0.123 (0.060) | -0.190 | +0.313 | Yes, 900 | 132.27 → 129.23 | M2 §1: eligible; 0 failures |
| 4 / clock (s4-clock) | 0 (NR) | 0 | 0 | Base | 119.12 → 115.74 (same file) | M2 §1: no gain |
| 4 / stock (s4-stock) | 0 (NR) | 0 | 0 | Base | 0.0 → 0.0 (not timed) | M2 §1: no gain |

M1 labels its positive-result table “Candidates” and reports no failures and other-spread identity, but includes the slower s2-flow and s2-queue; its own caveats reject those timings. This report applies the speed requirement to exclude them. M2's changed files all report 0 failures; unchanged returns are not successful new policies. M2 records alternate s3-free timings in both directions, so its eligibility cannot be rescued by asserting that the slower primary result is noise. Timings are seat-local measurements, not comparable absolute benchmarks across machines. [M1 §4; M2 §1, §3.2]

## Best file at each spread

| Spread | Selected measured file | What changed | Evidence |
|---|---|---|---|
| 1 | s1-queue | Below an estimated probability of 1 cent, multiply new tick-2 ask depth by 5 when tick 2 is strictly inside the rival ask; retain low-tick asks ahead of the rival while target quantity remains positive. Includes a cached belief-loop speedup reported identical in results. | M1 §4 |
| 2 | s2-stock | Enable the base's spread-3 flow estimator for spread 2, scaling only the tick-1 stock target, clipped to 0.5–2. The same trading policy appears in s2-free and s2-flow; stock has a passing reported timing. | M1 §4 |
| 3 | s3-flow | Replace clipped-fill flow estimation with a per-run Bayesian retail-rate and mean-order-size estimate from own fills on both sides. Treat exhausted-size fills as censored; feed estimates into bid/ask quantile sizing, ammunition targets and tick-1 stock. | M2 §3.1 |
| 4 | s4-flow | Use a 9-point per-run flow posterior, updated every 25 steps, to set ask depth and stock targets. | M1 §4 |

M1's best spread-3 choice, s3-asks, is superseded by M2's s3-flow. M2's “best” spread-4 choice, s4-bids, is best only among its own inputs; M1's s4-flow has the larger eligible reported mean gain. These are selections by reported point estimate, not proof of population superiority. [M1 §4–5; M2 §1, §4]

Using the brief's quarter share for each spread, the cross-merge calculation is:

`2.2637 × 1/4 + 0.6075 × 1/4 + 2.445 × 1/4 + 1.1441 × 1/4 = +1.615075`.

This arithmetic uses M1 §4 and M2 §1, rather than adding their overlapping aggregate estimates. It is derived from rounded inputs, not additional measured precision. The supplied standings gap is `109.59 - 106.80 = 2.79` (also stated in M2 §4); the estimated gain falls short. Applying a local holdout gain to a leaderboard mean does not establish a new leaderboard score. No combined file or combined simulation result was supplied. Disjoint branches justify the arithmetic conditionally on preserving each exact measured implementation; they do not supply those implementations. [B; M1 §5; M2 §4]

## Review finding and executable handoff limits

The reviewer's substantive omission is reproducible: M1 §4 exposes only prefixes `c937628c…` (s1-queue), `29d4a3f9…` (s2-stock), and `918443f8…` (s4-flow). M2 §3.1 describes s3-flow but gives no retrievable item identifier or implementation; §6 says the merge did not read or run the code fields. The two source URLs retrieve merge prose, not item JSONs. The base link retrieves the unchanged original. These observations were checked by reading the supplied merges and retrieving all three URLs listed above.

Consequently **none of the four exact selected implementations, and no combined implementation, can be obtained from the supplied materials**. Prefixes cannot identify an immutable artifact, and prose is insufficient to reconstruct exact measured code. The best-file names above denote reported results, not delivered executable files. No alternative artifact identifier or successful validation of a stack is claimed.

The requested remedy—supplying four exact implementations—is unavailable from these inputs and exceeds this write-up's explicit instruction to leave code out and write only the report (plus the revision response). This report preserves the measured results and makes their handoff limit explicit rather than fabricating code or retrieval links. The revision response disputes that remedy under this assignment while acknowledging the underlying missing-artifact observation. Exact seat item JSONs remain the missing prerequisite for an operator to assemble, validate and manually submit the measured policies. [B; M1 §4; M2 §3.1, §6]

## Confidence, disagreements and missing evidence

- **Scorer reproduction:** M1 §1 gives the author's mean as **98.4694596619638** and lists exact matches for most measured seats. s2-free obtained **98.46945966196385**; s1-middle obtained **98.46762449920578**, with unresolved cross-interpreter differences. s1-asks and s1-clock did not run the setup check. M2 §2 reports the author's figure for every seat except s3-middle, but distinguishes direct CLI checks, alternate harnesses and unspecified methods. These are reported checks, not checks performed here.
- **Selection and holdout:** M1 §4 notes unadjusted selection among policies on the unseen set for s1-bids and s1-free. M1 §6 says the shared unseen seeds have now been used for selection. M2 §3.1 says s3-flow's tuning gain was about **+1.0**, with **+1.151** and **+0.898** on its two halves; the seat calls about **+1** more cautious than the unseen **+2.445**. Its tuning used a sorted-book patch checked on samples; holdout, identity and timing used the unmodified simulator.
- **Incomplete results:** s2-asks ran nothing and returned no code; s3-stock lacked an interpreter. s1-asks returned unchanged base on only **16** tuning and **16** unseen runs, with base mean **31.85**; s1-clock used **249** unseen seeds with base **38.51**. These do not support full-holdout comparisons. M1 does not supply exact unseen figures for s1-stock or s2-middle. M2 does not supply s3-queue's rejected-policy unseen loss, only its returned-base result. [M1 §2, §4; M2 §3.5]
- **Source caveats:** M1 §7 flags failed source re-reading for s2-stock, s4-flow, s2-middle, s1-middle, s1-flow, s2-bids, s2-free and s1-free, without identifying the underlying URLs. M2 §6 similarly flags s3-queue, s4-asks, s4-stock, s4-bids, s4-middle, s4-clock and s4-free. Both say item URLs were absent, so their external support cannot be resolved here. The tables faithfully attribute local measurements to the merges; they do not certify the underlying code, simulator claims or external sources.
- **Interactions:** same-spread combinations were not validated. In particular, sticky ask changes can overlap, and flow estimation changes inputs to other sizing rules. M2 §4's hypothetical sum of changed files is explicitly untested; it is not an established upper bound on interacting policies and is not used in this report's stack estimate. [M1 §4–5; M2 §4]

## What the seats say to try next

**Spread 1:** investigate queue priority and selective tick-2 depth, rather than blanket low-price depth increases. s1-queue's larger multipliers lost heavily to arbitrage; s1-free warns that inventory-bid persistence lost and combinations need validation. Test the promising queue, flow and bid changes jointly on fresh unseen seeds rather than summing their gains. [M1 §4, §6]

**Spread 2:** fill the untested asks seat. Improve flow estimation: s2-flow reports the estimate is about **25%** high and reaches correlation **0.55** with true flow only by step **1000**. Removing low bids, bridge or stock bids lost; constant clock changes and stopping quotes late also lost. [M1 §2, §6]

**Spread 3:** s3-flow proposes counting retail arrivals from probes and revisiting the **20–80 cent** size rule, where the base takes only **40%** of retail buy dollars (**$261 of $646**). s3-free proposes retaining small remainders as overflow cover and making thresholds tick-dependent; it reports about **$9.5** per run of retail buys at **5–10c** while the base has no ask. s3-queue proposes adding depth only just before the rival bid is exhausted. The blocked stock seat remains untested. [M2 §5; M1 §2]

**Spread 4:** s4-asks proposes an online retail-size-dependent threshold; s4-middle proposes pre-placing at rival refill ticks (**consumed tick +/- 4**); s4-queue proposes state-dependent retirement of front asks; s4-bids proposes inventory-dependent depth reductions; s4-free proposes adaptive low-price inventory targets; s4-stock proposes engine-level tracing of unsold inventory. s4-asks' remaining-gap estimate is about **1.6** from tick choice plus about **4** from **5.3** notional still missed, not a measured additive gain. [M2 §5]

Before any manual entry, obtain the exact selected item JSONs, preserve their spread gates, and validate the resulting stack for failures, other-spread identity and runtime. Use a fresh unseen seed range, since the common holdout has been used for selection. No key or automated entry is needed for this write-up; B assigns entry to the network operator. [B; M1 §6; M2 §4, §6]
