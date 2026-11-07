# NP2 measurement before submission

**NP2 beats NP on mean simulated edge in the supplied fresh measurements:** pooling b0, b1, b2, b3, b4 and b6 gives the following paired results. The pool includes b3's recoverable measurements despite its delivery-blocked status; b5 contributes no observations. The reference block s0 is excluded from this fresh pool. These are calculations from each item's `pairs` sufficient statistics, not a new simulator run. [b0](../items/b0/result.json), [b1](../items/b1/result.json), [b2](../items/b2/result.json), [b3](../items/b3/result.json), [b4](../items/b4/result.json), [b6](../items/b6/result.json)

| Fresh paired comparison | n | Mean difference | SE | Approximate 95% interval |
|---|---:|---:|---:|---:|
| NP2 − NP | 12,000 | +0.109743499 | 0.006132022 | +0.097725 to +0.121762 |
| NP2 − CH | 12,000 | +0.572610259 | 0.011368815 | +0.550327 to +0.594893 |
| NP − CH | 12,000 | +0.462866760 | 0.009917774 | +0.443428 to +0.482306 |

The NP − CH check is consistent with the task's prior norm-phat result, **+0.464, SE 0.016**: the new estimate is 0.001133240 below that prior mean. The prior is supplied by the assignment, not independently recovered here. Likewise, the assignment's two-print-alone result **+0.248, SE 0.013 over CH** is background, not the measured incremental benefit on NP. The observed incremental gain on NP is the +0.109743499 above; the two standalone gains should not be added as a prediction for NP2. [Assignment: goal and seat results; fresh inputs linked above.]

The five worst reported fresh **NP2 − NP** seeds are below, using each block's `worst5_np2_np` values rather than subtracting coarsely rounded rows. The union of block bottom-five lists supplies the pooled bottom five for this comparison, conditional on those lists being correct. All values are rounded here to six decimals. [b0](../items/b0/result.json), [b1](../items/b1/result.json), [b3](../items/b3/result.json), [b4](../items/b4/result.json)

| Seed | Block | NP2 − NP |
|---|---|---:|
| 816920 | b3 | −46.743809 |
| 811849 | b0 | −11.724401 |
| 813120 | b1 | −3.769144 |
| 818614 | b4 | −3.586911 |
| 819923 | b4 | −3.284287 |

For **NP2 − CH**, the five worst *available rows* are seed 816920 (b3, −45.937617), 810864 (b0, approximately −5.97), 813382 (b1, approximately −4.6662), 819804 (b4, approximately −4.39), and 818614 (b4, approximately −4.05). These are row subtractions, with the precision available in the source. **A definitive pooled worst-five list for NP2 − CH cannot be established:** b2 omits its final 550 rows and supplies no NP2 − CH bottom-five list. An omitted seed could rank below these. For completeness, NP − CH's worst available row is seed 810864 in b0, approximately −6.07, with the same missing-row limitation. [b0 `per_seed`](../items/b0/result.json), [b1 `per_seed` and `per_seed_first_seed`](../items/b1/result.json), [b2 `per_seed_note`](../items/b2/result.json), [b3 decoded rows](../items/b3/result.json), [b4 `per_seed`](../items/b4/result.json), [b6 decoded rows](../items/b6/result.json)

The seeds **0..999** absolute edge results are:

| Strategy | n | Mean edge | SE |
|---|---:|---:|---:|
| CH | 1,000 | 525.5258821780834 | 2.7894264590251843 |
| NP | 1,000 | 526.0337302497851 | 2.7912248204542776 |
| NP2 | 1,000 | 526.1155722459862 | 2.7896004178197593 |

Source: [s0 `edge`, `n` and reference check](../items/s0/result.json). Its paired NP2 − NP result is +0.081841996, SE 0.016449792; NP2 − CH is +0.589690068, SE 0.027901253; NP − CH is +0.507848072, SE 0.024781688. These are reference-seed results, not extra fresh observations. The reported CH reference mean differs from the expected 525.525882178 by about 8.34e−11 and passes s0's stated 5e−10 tolerance. This checks numerical agreement with the supplied target, not the independent validity of that target.

## Block accounting and sensitivity

All numerical entries below come from the named item's `pairs`; the seed ranges are read from its metadata or rows. Each measured fresh block reports 2,000 paired observations. Means and SEs are rounded to six decimals in this table.

| Block and source | Available seed range | NP2 − NP (SE) | NP2 − CH (SE) | NP − CH (SE) | Status |
|---|---|---:|---:|---:|---|
| [b0](../items/b0/result.json) | 810000..811999 | +0.110379 (0.012930) | +0.601815 (0.044046) | +0.491437 (0.042832) | Complete |
| [b1](../items/b1/result.json) | 812000..813999 | +0.120307 (0.011146) | +0.546053 (0.018018) | +0.425746 (0.014900) | Complete |
| [b2](../items/b2/result.json) | 814000..815999 intended; rows through 815449 | +0.125147 (0.011580) | +0.604007 (0.028516) | +0.478860 (0.026870) | Complete flag; row export truncated |
| [b3](../items/b3/result.json) | 816000..817999 | +0.092253 (0.025981) | +0.531808 (0.029523) | +0.439555 (0.015422) | Delivery blocked; measurements recovered |
| [b4](../items/b4/result.json) | 818000..819999 | +0.099670 (0.011559) | +0.578486 (0.019354) | +0.478815 (0.016835) | Complete |
| [b5](../items/b5/result.json) | No measured seeds | — | — | — | Setup blocked |
| [b6](../items/b6/result.json) | 822000..823999 | +0.110705 (0.010940) | +0.573493 (0.018133) | +0.462787 (0.015527) | Complete; compressed rows |

The blocked items are:

- **b3:** `complete=false`, top-level `n=0`; `blocked.step=serialize_per_seed`. It reports that all simulations succeeded, but the literal six-decimal row array would make the result 85,576 bytes, above its 64,000-byte limit. Its `measured_n=2000` and all three `pairs.*.n=2000` distinguish measurement count from delivery status. I decoded its gzip/base64 rows, found 2,000 contiguous seeds, and verified the decoded SHA-256 against its embedded digest. Rounded rows reproduce its paired means and SEs to rounding precision. Including its measured data avoids dropping the unusually bad seed 816920 because of an export failure. [b3](../items/b3/result.json)
- **b5:** `complete=false`, `n=0`; its setup platform preflight exited with code 3 and output `BLOCKED platform`. The result says the Linux x86_64 and `/proc/self/exe` preflight failed, no simulation ran, and strategy hashes were not checked. Its null edges and zero pair counts supply no performance evidence. The input does not identify which preflight condition caused the failure. [b5](../items/b5/result.json)

Excluding b3 strictly by completion status leaves **10,000** fresh pairs: NP2 − NP **+0.113241647, SE 0.005210504**; NP2 − CH **+0.580770774, SE 0.012297702**; NP − CH **+0.467529127, SE 0.011494422**. Thus the sign of the incremental improvement does not depend on admitting b3. [Calculated from b0, b1, b2, b4 and b6 `pairs`, linked in the table.]

## Interpretation and evidence limits

The supplied measurements support using NP2 over NP for **expected edge under this simulator setup**: the pooled approximate interval for NP2 − NP is positive, and every measured fresh block has a positive mean. This is not a per-seed dominance claim: seed 816920 loses about 46.74 against NP. Nor is this evidence of a live challenge score or a completed submission. The challenge is the assignment's [Paradigm AMM fee challenge](https://www.paradigm.xyz/puzzles/amm); no submission is recorded in these inputs.

The assignment identifies CH as ChengHua926's public retune of jiayaoqijia's YQ, NP as CH plus seat 356's norm-phat, and NP2 as NP plus seat 377's two-print. These provenance labels and the historical seat estimates come from the assignment. The result files report matching CH/NP/NP2 hashes across all measured items; b5 provides none. They therefore identify consistent reported strategy artifacts, but strategy source code was not supplied as part of these eight JSON results for an independent implementation audit. [s0](../items/s0/result.json), [b0](../items/b0/result.json), [b1](../items/b1/result.json), [b2](../items/b2/result.json), [b3](../items/b3/result.json), [b4](../items/b4/result.json), [b5](../items/b5/result.json), [b6](../items/b6/result.json)

The assignment pins the [simulator commit](https://github.com/benedictbrady/amm-challenge/tree/6b6921f8d463314aa7c96234e1be25a25245f704). s0, b0 and b6 explicitly name that commit in their metadata. Their reported setup uses a 30 bps normalizer; s0 and b6 describe 10,000 steps, price seed equal to seed, and retail seed equal to seed+1. Pairing means comparing CH, NP and NP2 on the same seed, each against the normalizer, not a direct NP2-versus-NP pool match. These are producer-reported methods, not an independent rerun here. [s0 `check_ch_0_999.method`](../items/s0/result.json), [b0 `method`](../items/b0/result.json), [b6 `method`](../items/b6/result.json)

**Source-validation flags:** the assignment says one cited source failed revalidation for each of **s0, b0, b3 and b6**. It does not identify the failed URLs or passages, and these JSON inputs contain no citation lists identifying them. I therefore do not treat any external page, reference target, strategy-provenance assertion or claimed simulator setup from those items as independently verified. In particular, s0's absolute scores remain reported measurements, and its reference check cannot validate the external provenance of its target. b0, b3 and b6 remain included as numerical artifacts, with that qualification; their external-source flags are not proof their numbers are wrong. The local hashes, decoded rows and arithmetic checks validate artifact integrity/internal consistency only.

As a conservative sensitivity calculation, omitting all flagged fresh items (b0, b3, b6) leaves **b1, b2 and b4, n=6,000**: NP2 − NP **+0.115041380, SE 0.006599597**; NP2 − CH **+0.576181957, SE 0.012964545**; NP − CH **+0.461140576, SE 0.011680717**. This supports the same directional conclusion without those items, but does not certify the remaining items' external sources or restore b2's missing rows. [Calculated from b1, b2 and b4 `pairs`, linked above.]

Row-level audit limits also matter. b0 and b4 export two-decimal scores; b1 exports four-decimal scores with implicit consecutive seeds. b2 exports only 1,450 six-decimal rows although its aggregates cover 2,000. b3 and b6 preserve all 2,000 six-decimal rows through compression. I successfully decoded both; their decoded digests match their metadata, and row-derived paired means/SEs agree with their reported aggregates within rounding precision. Pooling uses reported `sum_d` and `sum_d2`, not rounded row subtractions. b2's sufficient statistics are themselves rounded, so extra displayed pooled digits are arithmetic precision rather than a claim of full underlying accuracy. [Each item's serialization metadata and `pairs`.]

## Calculation and provenance record

For each comparison let N be the sum of `pairs.*.n`, S the sum of `sum_d`, and Q the sum of `sum_d2` across included blocks. I used mean = S/N and SE = sqrt((Q − S²/N)/(N(N−1))). This is the sample SD of paired seed differences divided by sqrt(N); intervals above use mean ± 1.96 SE, assuming independent seed observations. They do not include model error, strategy-selection effects or uncertainty in the historical seat estimates.

For the main pool the sufficient statistics are:

| Comparison | N | S | Q |
|---|---:|---:|---:|
| NP2 − NP | 12000 | 1316.9219892051988 | 5558.716577411536 |
| NP2 − CH | 12000 | 6871.323107289809 | 22545.03139986164 |
| NP − CH | 12000 | 5554.40111908461 | 16733.93002879188 |

Source: sums of the six measured fresh items' `pairs` fields, linked above. s0 and repeated CH reference checks are excluded; b5's zero counts add nothing.

All eight supplied inputs were present and parsed. Their bytes matched the assignment's SHA-256 values. For traceability, the following identifies the exact local input artifacts used; links elsewhere in this report refer to their named result paths. These inputs are source artifacts, not additional report outputs.

| Item | Read artifact | SHA-256 |
|---|---|---|
| s0 | `.imd/reads/artifacts/item-s0` | `c2d9acdc92f381f1a1146325a4ff5c31a7c2474ea6414ebeb1070ef7e7685747` |
| b0 | `.imd/reads/artifacts/item-b0` | `68a15ddc9fe6d5481028564695a145adbb19e47e3b40b58e5434eac38b561040` |
| b1 | `.imd/reads/artifacts/item-b1` | `7cc80553b57c26178e0e9a5a827304d50a7784e006db04321a92b06593e4158a` |
| b2 | `.imd/reads/artifacts/item-b2` | `668459c0e303b8023e3aecaad1e4550fa61461220eedda2e0718eda2d46ad0a2` |
| b3 | `.imd/reads/artifacts/item-b3` | `1d8e883efa5c10f44ee0a208790e767777dcaed992e07b0bfddfa614e3c368c1` |
| b4 | `.imd/reads/artifacts/item-b4` | `e0f160ba22f928769849acab06edfb8bb17156e00646cfc89c5a665cb3bba8d0` |
| b5 | `.imd/reads/artifacts/item-b5` | `0aae35ad3466d8b1074f56eabccc900e72ebb2fdfc1cec9eecddcfff2c39fc21` |
| b6 | `.imd/reads/artifacts/item-b6` | `7f03521c6c940a9fa110951fea2c3c4bd8da2dd0935ae22c8731455222a2b3a7` |

Reported strategy SHA-256 identifiers, normalized across the inputs' capitalization:

| Strategy | SHA-256 |
|---|---|
| CH | `6dd68f77a70900319460215374143dbd5d924198450a46d9f5f91f6b1e3d35c3` |
| NP | `f1ea5b95c853ef28399a0b22ec222773525dba18c92282c04993170c97b57c83` |
| NP2 | `51f1c1a9d4999ee460eb8bbc66880da8074b173399a4f5d71f96671482e18ac0` |

Source: measured items' `shas` fields. The goal is answered by the supplied evidence, with a positive incremental mean for NP2, a reproduced norm-phat gain near the prior estimate, and an unresolved tail-risk and provenance qualification rather than an unqualified submission guarantee.
