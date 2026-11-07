# Silence-handling variants of BS: results write-up

**Goal:** measure four silence-handling variants (V1–V4) of BS before it goes to Paradigm's AMM fee challenge (paradigm.xyz/puzzles/amm). BS = stack-b (seat 827) + silence-a (seat 534) from goal 052122ee. That goal reported BS at +0.736 (se 0.018) over NP2. Each variant moves BS's silence settings (cap on silent steps, per-step keep factor, damping) toward silence-b's (seat 494). Simulator: github.com/benedictbrady/amm-challenge @ `6b6921f8d463314aa7c96234e1be25a25245f704`. Opponent: 30 bps Vanilla. Each block ran NP2, BS and one VAR separately on the same 2,000 fresh seeds.

All figures below come from the eight result files, `item-v1a` … `item-v4b`. Their SHA-256s were checked against the brief and all matched. Pooled figures are my own. For each variant I added up the blocks' reported `n`, `sum_d` and `sum_d2`, then took mean = Σd/n and se = sample sd/√n. That is the same se definition the blocks use: I recomputed every block's se from its own sums and each one matched the value it reported.

## Headline: pooled gain per variant, best first

| Rank | Variant | VAR SHA-256 | Blocks used | n | VAR − BS mean | se | VAR − NP2 mean | se |
|---|---|---|---|---|---|---|---|---|
| 1 | **V4** | `b7b8902636547df00d92258a946b00141be5822ef15818b74eb6f0357c1ae243` | v4a (full), v4b (partial, 512 seeds) | 2512 | **+0.0786** | 0.0074 | +0.8131 | 0.0162 |
| 2 | V2 | `28417e116f57f1029fdd1803832e852574902c1ae7253c05657f317db76da4ab` | v2a, v2b | 4000 | +0.0623 | 0.0045 | +0.8329 | 0.0119 |
| 3 | V1 | `a06cef7692a41fddddc2c9709a30a2f06d08a6ecea38ea7d94eb2aac576471e8` | v1a, v1b | 4000 | +0.0599 | 0.0068 | +0.7977 | 0.0133 |
| 4 | V3 | `357d9b5ada279be132765650dab59638e254386ffc749139e423a84e4bd526e7` | v3b only (v3a blocked) | 2000 | **−0.3239** | 0.0174 | +0.4311 | 0.0245 |

V4 using only its complete block (v4a, n 2000): VAR − BS +0.0722 (se 0.0081), VAR − NP2 +0.8154 (se 0.0179).

The ranking uses VAR − BS. That is the direct paired comparison against the file we would otherwise submit, measured on the same seeds within each block. Ranked by VAR − NP2 instead, V2 comes ahead of V4 (+0.833 vs +0.813). That reversal comes from block-to-block noise in BS − NP2: v2b's BS − NP2 was +0.792, the highest of any block. It does not mean V2 is better relative to BS.

### Check: BS − NP2 against the +0.736 baseline

| Pool | n | BS − NP2 mean | se |
|---|---|---|---|
| All blocks with data (v1a, v1b, v2a, v2b, v3b, v4a, v4b) | 12512 | +0.7504 | 0.0069 |
| Complete 2,000-seed blocks only (excludes v4b) | 12000 | +0.7525 | 0.0070 |

Every block ran the same BS (`a9830b417dd43806c144e8b4a217cda1317850bb52578b18a3237307cf8dfa16`) and NP2 (`51f1c1a9d4999ee460eb8bbc66880da8074b173399a4f5d71f96671482e18ac0`). The pooled +0.750 is about 0.015 above the goal's +0.736. With the earlier se of 0.018, that is within one se, so the baseline holds. Per block, BS − NP2 ranged from +0.701 (v4b, n 512) to +0.792 (v2b).

## Best variant

**V4 is the best measured variant:** SHA-256 `b7b8902636547df00d92258a946b00141be5822ef15818b74eb6f0357c1ae243`. It gains +0.0786 (se 0.0074, n 2512) over BS and +0.8131 (se 0.0162) over NP2.

Caveats:
- **V4's lead over V2 and V1 is not yet decisive.** V4 − V2 on VAR − BS is about +0.016, with a combined se of about 0.009 (≈1.9 se). The two were run on different seed blocks, so this is not a paired comparison. V1, V2 and V4 all beat BS clearly: each is more than 8 se above zero.
- V4 has 2,512 seeds, not the planned 4,000, because v4b only finished 512 seeds (see below).
- On the plus side, neither V4 block (v4a, v4b) is among the results whose sources failed to re-verify (see the last section).

**V3 should not be used.** It loses −0.324 (se 0.017) to BS. Its worst seeds lose roughly 3.6–4.3 edge each, for example seed 3210459 at −4.27 (v3b). Whatever V3 changes in the silence settings hurts the stacked file.

The results do not record which silence settings (cap on silent steps, keep factor, damping) each variant actually uses. They give only file SHA-256s, so this report cannot say which setting change explains V4's lead or V3's loss.

## Per-block results

| Block | Variant | Seeds | n | NP2 0..999 check | VAR − BS (se) | VAR − NP2 (se) | BS − NP2 (se) |
|---|---|---|---|---|---|---|---|
| v1a | V1 | 3200000–3201999 (stated) | 2000 | 526.1155722459862 | +0.0516 (0.0097) | +0.7848 (0.0183) | +0.7332 (0.0173) |
| v1b | V1 | 3202000–3203999 (inferred, not stated) | 2000 | passed, exact | +0.0683 (0.0094) | +0.8105 (0.0193) | +0.7423 (0.0182) |
| v2a | V2 | 3204000–3205999 (inferred, not stated) | 2000 | 526.1155722459862 | +0.0597 (0.0064) | +0.8093 (0.0169) | +0.7496 (0.0169) |
| v2b | V2 | 3206000–3207999 (stated) | 2000 | passed, exact | +0.0650 (0.0065) | +0.8566 (0.0168) | +0.7916 (0.0169) |
| v3a | V3 | 3208000–3209999 (planned) | 0 | **failed** (526.115573224169) | — | — | — |
| v3b | V3 | 3210000–3211999 (stated) | 2000 | passed, exact | −0.3239 (0.0174) | +0.4311 (0.0245) | +0.7550 (0.0170) |
| v4a | V4 | 3212000–3213999 (inferred, not stated) | 2000 | passed, exact | +0.0722 (0.0081) | +0.8154 (0.0179) | +0.7432 (0.0172) |
| v4b | V4 | 3214000–3214511 of 3214000–3215999 | 512 | 526.1155722459862 | +0.1033 (0.0177) | +0.8041 (0.0373) | +0.7008 (0.0334) |

The "inferred" seed ranges come from the seeds in each block's `worst5_var_bs` list, which all fall inside the range shown. Those blocks do not state their range in a `method` field. Every 2,000-seed block reports its sample sizes as n = 2000 for all three pairs.

## Blocks that blocked or did not complete

- **v3a (V3): blocked, n = 0.** The NP2 reproduction check on seeds 0..999 gave mean edge 526.115573224169 against the expected 526.1155722459862. The difference is 9.782e-07, about 2e-9 relative. Under the brief's rule a mismatch blocks the item, so V3, BS and NP2 were not run on seeds 3208000..3209999. According to the block's own account, all three file SHA-256s matched. That machine built the simulator from the pinned commit's source tarball on macOS aarch64 (rustc 1.99.1, Python 3.12), and the block attributes the gap to platform floating-point (libm) differences. That diagnosis is its own explanation and was not independently confirmed. The block suggests either running on linux x86_64 or allowing a tolerance such as |diff| < 1e-5. As a result V3 rests on one block (v3b, n 2000). The other seven blocks reproduced the check value 526.1155722459862 exactly.
- **v4b (V4): incomplete, not blocked (`blocked: null`, `complete: false`).** Only seeds 3214000..3214511 (n 512) of 3214000..3215999 finished in the time budget, at about 1.38 s per simulation. It used `n_workers=16` instead of 8, and its notes say worker count does not affect per-seed results. Its 512 paired seeds are included in V4's pooled figure. V4 using v4a alone is shown above.

## Weight of sources that did not re-verify

The brief says some results cite sources that failed to re-verify when their machines read them again: v1a (2 sources), v1b (1), v2a (2), v2b (1), v3a (1). The result files handed to this write-up contain no source lists or URLs, so I cannot tell which claims those sources backed. What this means for the findings:

- **V1 (v1a, v1b) and V2 (v2a, v2b):** every block behind these two variants is flagged. Their simulated figures are internally consistent: each reported se and mean matches its own sums, and each block's NP2 check reproduced 526.1155722459862 exactly. But any claim in them that rests on an external source, such as the simulator page or the challenge rules, should be treated as unconfirmed.
- **V3:** v3a is flagged, so its explanation of the block (the platform and libm account) carries less weight. v3b, the only block with V3 data, is not flagged.
- **V4:** neither v4a nor v4b is flagged, so the best variant's figures rest on blocks with no failed sources.

## What could not be determined

- The actual silence settings (cap, keep factor, damping) of V1–V4. They are not in the results.
- Seed ranges for v1b, v2a and v4a are inferred, not stated.
- A paired, same-seed comparison between V4 and V2 was not run. Running V4 and V2 together on one fresh 2,000-seed block, and finishing v4b's remaining 1,488 seeds, would settle the ranking.
- Mean edges against Vanilla are only partly reported: v2b gives NP2 523.816 / BS 524.608 / VAR 524.673, v3b gives 523.253 / 524.008 / 523.684, and v4b gives 525.868 / 526.569 / 526.672. The other blocks report only differences.
