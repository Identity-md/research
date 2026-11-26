# Exact integer kernels — local results for subnet 66

**Verified board takeovers: 0.** On three held-out seeds, the frozen entry tied former champion 50 on RV32IM. Its score was 0.03175–0.03456% higher on Cortex-M0+ and 0.01587–0.01728% higher overall. Lower is better. The reigning sources were withheld, so eligibility against the actual champions is **undetermined on all three boards**. The candidate passed the full-domain output checks for all three functions on the host and all three target architectures. The work involved no hotkey registration, signing, competition submission or TAO spending.

**Delivered source.** `entry.c` is the 166,756-byte, single-file C11 implementation of `eik_sigmoid`, `eik_tanh` and `eik_exp`. The goal repository is `identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io`. Its final merged commit is **`c5e3f91274b1f0c409127e8cfc14aa5ac8f392da`**. The root file and delivery copy both have SHA-256 `593e2420f5363dcb5d4fe429dd486f23b88ed9e917c22864c6c1b3e7ec0c5f6b`. The archive includes the exact public base, experiment sources and full check logs. [Download entry.c](https://raw.githubusercontent.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/entry.c) · [Repository at the final commit](https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/tree/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da) · [Download source and evidence archive](https://codeload.github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/tar.gz/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da) · [Delivery inventory][inventory]

## Same-input board comparison

The 2026-11-26 11:42:15 UTC snapshot resolved RV32IM promotion **59** to submission **52**, Thumbv6-M promotion **60** to submission **53**, and overall promotion **61** to submission **56**. A second public check at 12:22:43 UTC confirmed the same holders. Each source endpoint returned HTTP 403 `SOURCE_WITHHELD`. The API supplied no absolute champion S. In the table, `null` means the denominator for that seed is unavailable. A takeover requires candidate/champion ≤ 0.970 on identical fresh inputs. On the validator's historical inputs, submissions 53 and 56 scored 0.968439× and 0.968152× former 50 on their respective boards. RV32IM's previous reference could not be tied to a public source. The historical inputs differ from the held-out sets below, and the kit's default incumbent is a separate implementation. [Board snapshot][boards] · [Packaging refresh and HTTP records][refresh] · [Competition boards API](https://conjectures.io/v1/competitions/exact-integer-kernels/boards)

| Held-out seed | Board | Candidate S | Former 50 S | Candidate / 50 | Reigning submission | Champion S | Candidate / champion |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 849230117 | RV32IM | 28.335213 | 28.335213 | 1.000000000 | 52 | null | null |
| 849230117 | Thumbv6-M | 40.152571 | 40.139826 | 1.000317524 | 53 | null | null |
| 849230117 | Overall | 33.730278 | 33.724924 | 1.000158749 | 56 | null | null |
| 2715043869 | RV32IM | 28.395532 | 28.395532 | 1.000000000 | 52 | null | null |
| 2715043869 | Thumbv6-M | 40.299878 | 40.286226 | 1.000338856 | 53 | null | null |
| 2715043869 | Overall | 33.828043 | 33.822313 | 1.000169414 | 56 | null | null |
| 396172055 | RV32IM | 28.381597 | 28.381597 | 1.000000000 | 52 | null | null |
| 396172055 | Thumbv6-M | 40.333895 | 40.319962 | 1.000345557 | 53 | null | null |
| 396172055 | Overall | 33.834012 | 33.828168 | 1.000172764 | 56 | null | null |

Each former-50 measurement used the candidate's seed, input digest, fresh hard pool and evaluator fingerprint. S combines retired-instruction means for 2,000 typical, 1,000 wide, 300 hard and 1,000 uniform inputs per function, with weights 55%, 30%, 10% and 5%. The scorer applies a hard-tail penalty and a code-and-table-size penalty. Overall is the geometric mean of the two scored target scores for the **same entry**. Thumbv7E-M contributes to correctness testing only. The table rounds S to six decimals and computes ratios before rounding. [Full-precision CSV][csv] · [Input digests and raw score references][scores] · [Pinned competition rules](https://github.com/conjectures-io/exact-integer-kernels-miner/blob/5a32428ad4aa23bce737d50a738ace24ddeeed2e/RULES.md)

| Held-out run | Evaluation record |
| --- | --- |
| 849230117 | Candidate and former 50 both completed `eik evaluate --quick --json` in about 168 seconds each. The historical comparison explicitly mapped all three boards to former 50. [Run 1 logs][run1] |
| 2715043869 | Earlier attempts timed out. Standalone paired measures and quick host checks completed. The coordinator's candidate evaluate then exited 0 in 287.730 seconds. [Run 2 logs][run2] |
| 396172055 | The evaluate command timed out during kit-incumbent comparison at 600 seconds, exit 124. Standalone `eik measure` supplied both absolute scores on the same populations. Per-function quick fullchecks passed. [Run 3 logs][run3] |

All three runs recorded zero wrong scored outputs and zero mismatches in the 98,304 stratified words per target and source. Each quick host check covered 134,217,728 words per function. The exhaustive counts below come from separate runs. [Check summary][checks]

## Public baseline selection

The workers ran `python -m eik setup` with upstream kit commit `5a32428ad4aa23bce737d50a738ace24ddeeed2e`, then checked and evaluated the five hash-matched public sources on two common seeds. The recorded environment was Linux x86-64, Python 3.12.3, GCC 13.3.0, Zig 0.17.1 / Clang 22.1.8 and QEMU 7.2.22. The measurement fingerprint is `2c8fd1f3a6711f0639685319fb25262b02bfecf4c6589c52cb58928270a46322`, and the verifier fingerprint is `ebbf9d5cac596a718532b34798dc452e4050d6940594005c44f9a729c699c5a8`. [Setup and provenance][provenance] · [Detailed fingerprint][fingerprint]

Each cell lists **RV32IM / Thumbv6-M / overall S**. Submission 50 had the lowest S on every board on both seeds. Its exact source, SHA-256 `88617bb49e36a06cabd7d84ce6fe504ee337f8f41ad7c55bc72f696db94060c3`, became the base for all eight trials. [Former-50 source][source50] · [Baseline command logs and reports][bases]

| Public submission | Seed 180434352 | Seed 2851275305 |
| ---: | --- | --- |
| 50 | 28.501406 / 40.430641 / 33.945988 | 28.623919 / 40.575572 / 34.079787 |
| 48 | 29.279218 / 43.272489 / 35.594728 | 29.384764 / 43.430226 / 35.723759 |
| 46 | 30.047304 / 45.718455 / 37.063679 | 30.124699 / 46.141665 / 37.282755 |
| 42 | 30.866819 / 47.590187 / 38.326984 | 30.864147 / 47.669166 / 38.357113 |
| 37 | 32.126463 / 48.590736 / 39.510106 | 32.076136 / 48.722956 / 39.532824 |

| Source | Tables, reduction and fast paths |
| ---: | --- |
| 50 | RV exp uses a split 256-entry table on the ln(2)/256 grid, a quadratic residual and dedicated negative-exp cells. RV activations use cubic cells, with linear or degree-five odd approximations for small arguments. Thumb uses 16-byte interleaved rows, a 512-step exp grid and split products. Guard bits decide when refinement is needed. |
| 48 | RV exp reduces to the ln(2)/256 grid and uses a split high-word/low-halfword table with a degree-three Q32 residual. Exponent and mantissa bits select cubic activation cells. Tiny and saturating inputs return early. Cold paths use extra table precision or division. Thumb shares exp and activation coefficients in one four-word-row table. |
| 46 | RV exp uses odd anchors on a 1/1024 grid and a 256-entry split table. Much of negative exp and the activation ranges use cubic cells backed by high-half multiplication. Thumb uses 16-bit limbs and quadratic/cubic rows. Guard windows send near-midpoint values to a higher-precision tier with sparse corrections. |
| 42 | RV exp combines a 256-entry odd-anchor table and quadratic residual with negative-domain cubic and quartic cells. Small activations use odd series up to degree seven. Thumb packs activation coefficients and exp high words into 728 rows and uses a 512-entry low table. Tiny-input and saturation branches avoid interpolation. Ambiguous results use midpoint tests, including a final mask for difficult Thumb exp words. |
| 37 | Sign and exponent classification lead to tiny-input, saturation or ordinary-cell paths. Ln(2)-scaled exp reduction uses paired 256-entry tables. Activations use 32/64-cell tables and cubic approximations. Guard windows select integer midpoint refinement or sparse input-specific corrections. RV uses widening products and Thumb uses 16-bit limbs. |

All five public sources select their compiled arithmetic paths through wide-character signedness. Host and RV use one path, Thumb the other. The compiler folds the selector after preprocessing. The trials preserved the common entry tokens required by the kit, which rejects dependence on predefined architecture macros. [Source 37 analysis][analysis-37] · [Source 42 analysis][analysis-42] · [Source 46 analysis][analysis-46] · [Source 48 analysis][analysis-48] · [Source 50 analysis][analysis-50]

## What changed in the frozen entry

The only edit from former 50 is in the Thumb tanh path for biased exponent 119. With `r = t_z mod 2^23`, the old fast return required `r ≥ 262144`. The new guard accepts `r ≥ 253952`, retaining the same returned word and the original refinement for smaller remainders. The diff contains one changed condition.

```diff
-  if (((t_z << 9) >> 27) != 0u)
+  if (((t_z << 9) >> 22) >= 31u)
```

The integer certificate bounds the residual over 32,767 affected cells after the first, separately handled cell. In Q54 units the residual lies in [−250889, −33522]. Even at the new cutoff the exact correction clears the lower rounding midpoint by 3,063 units and stays strictly below the upper midpoint. This admits **5,632 additional fast returns per sign**. On M0+ the new guard introduced literal loads, masking and a comparison. On the first selection seed the mean Thumb tanh wide cost rose from 20.731 to 20.788 instructions and the hard p99.9 stayed at 117. The Thumbv6-M image grew by eight bytes. RV32IM emitted identical scored code and read-only data. [Exact base-to-entry diff][diff] · [Rounding certificate and derivation][proof] · [Class measurements and stack][tanh-cost]

## Experiment log

The selection seeds were drawn after baselining. All eight main trials changed one technique from former 50 and used the same inputs as the control on each seed. Each numeric cell lists **RV32IM / Thumbv6-M / overall S**. A dash denotes an unmeasured second seed. The reviewed ledger also retains the full-precision ratios, per-class statistics in the cited raw logs, and unsuccessful evaluator attempts. [Experiment log][log] · [Machine-readable trial and variant ledger][ledger]

| Trial | Seed 1874435642 | Seed 1947282751 | Change and observed cost |
| --- | --- | --- | --- |
| `id50` | 28.522714 / 40.515261 / 33.994194 | 28.517414 / 40.303039 / 33.901895 | Unchanged public control. |
| `rv-exp-interval` | 32.896202 / 40.515261 / 36.507509 | 32.836443 / 40.303039 / 36.378681 | Dispatch early on one unsigned interval of negative exp inputs. Two branches disappeared, but the compiler outlined the cell evaluation and set up a stack frame on the common path. |
| `rv-exp-loads` | 28.995332 / 40.515261 / 34.274677 | 28.993483 / 40.303039 / 34.183702 | Use typed row indices for positive exp reduction. RV code and tables grew by 128 bytes. |
| `rv-tanh-quadratic` | 30.692301 / 40.515261 / 35.263389 | 30.738936 / 40.303039 / 35.197621 | Try a guarded quadratic before the cubic on 28 tanh rows. Typical RV tanh rose from 25.8 to 34.8 instructions per call. |
| `m0-exp-layout` | 28.522714 / 42.118337 / 34.660198 | 28.517414 / 41.903767 / 34.568585 | Copy 512 interleaved exp high words into a contiguous table. Other readers still needed the original rows. The M0+ image grew by 2,084 bytes. |
| `m0-exp-reduction` | 28.522714 / 41.117854 / 34.246062 | 28.517414 / 40.919484 / 34.160180 | Specialize negative exp row 10 with a rotated index and the same residual. The new addressing increased M0+ S on both seeds. |
| `m0-sigmoid-cell` | 28.522714 / 42.187310 / 34.688565 | 28.517414 / 41.979863 / 34.599959 | Expose narrow coefficients for 91 negative sigmoid cells. Two narrow loads saved extractions but lost the grouped word load. The M0+ image grew by 1,584 bytes. |
| `m0-tanh-refine` | 28.522714 / 40.530569 / 34.000615 | 28.517414 / 40.316224 / 33.907440 | Lower the rounding cutoff for exponent 119. The extra guard instructions cost more than the saved refinements. Selected fallback. |
| `shared-small-sigmoid` | 30.745566 / 45.476042 / 37.392334 | 30.820392 / 45.345929 / 37.384212 | Add an affine fast path for magnitudes below 2⁻⁷ before dispatch. Every call pays the new test, including calls already cheaper on RV. |
| `shared-small-sigmoid v2` | 31.108405 / 43.638988 / 36.844800 | — | Limit the affine guard to biased exponents 90–114 and omit the table. One-seed measurement only. |
| `shared-small-sigmoid v3` | 30.912174 / 43.404485 / 36.629592 | — | Narrow v2 to biased exponents 103–114. One-seed measurement only. |

The freeze ranked each eligible source by its best board's worse-of-two-seeds ratio, breaking ties by the worse overall ratio. Seven eligible trials tied at 1.0 on their best board. `m0-tanh-refine` had the smallest overall regression of those seven, with a worst ratio of 1.000188903. None of the eight trials beat former 50 on any board on either seed, so the freeze retained this single change. The independent review located 36 affected-range target shards for `shared-small-sigmoid` outside its packet index. Those runs passed and the trial still ranked last. The two additional sigmoid variants had only single-seed measures and target samples. For trials where default incumbent remeasurement timed out or evaluate was skipped, the ledger uses the pinned measurement and quick-fullcheck stages and preserves the unsuccessful attempts separately. [Freeze and selection][freeze] · [Independent review][review]

## Correctness and source checks

The frozen file passed `eik check` and the static gate. The linked objects exported the three entry points, used integer arithmetic and had zero writable allocated bytes. The review checked signed zeros, infinities, positive and negative NaNs with payload preservation and quieting, and exp boundary words on all three targets. For example, exp returned `0x7f7fff84` for `0x42b17217` and positive infinity for the next word. The post-normalization source digest, `adf3a5a8074ffcca8e58ea852f58143a20a00aa6a74df8f14c1b742fa21a03c8`, differs from each of the five public sources. Duplicate status against withheld sources remains unknown. [Static check and gate logs][checklogs] · [Compiled special-value and normalization probes][probes]

| Target | Code and tables, bytes | Static stack bound, bytes |
| --- | ---: | ---: |
| RV32IM | 18,960 | 176 |
| Thumbv6-M | 20,508 | 312 |
| Thumbv7E-M | 21,254 | 280 |
| Limit on each target | 65,536 | 8,192 |

Each linked **Pass** below is the selected full report for one runtime and one function. Each covers all 4,096 chunks of 2²⁰ binary32 words, the half-open range `[0,4096)`, against the pinned correctly rounded reference. All recorded **4,294,967,296 words and zero mismatches per cell**. The three host reports also recorded zero sanitizer failures.

| Runtime | eik_sigmoid | eik_tanh | eik_exp |
| --- | --- | --- | --- |
| GCC ASan + UBSan | [Pass · rerun][raw-host-sigmoid] | [Pass · rerun][raw-host-tanh] | [Pass · reused][raw-host-exp] |
| QEMU RV32IM | [Pass · rerun][raw-rv32im-sigmoid] | [Pass · rerun][raw-rv32im-tanh] | [Pass · rerun][raw-rv32im-exp] |
| QEMU Thumbv6-M | [Pass · rerun][raw-thumbv6m-sigmoid] | [Pass · rerun][raw-thumbv6m-tanh] | [Pass · rerun][raw-thumbv6m-exp] |
| QEMU Thumbv7E-M | [Pass · rerun][raw-thumbv7em-sigmoid] | [Pass · rerun][raw-thumbv7em-tanh] | [Pass · rerun][raw-thumbv7em-exp] |

The pinned `eik merge` required `rv32im,thumbv6m,thumbv7em` and exited 0 with empty stderr and verdict `passed`. The twelve reports sum to **49,152 runtime/function/chunk combinations and 51,539,607,552 function evaluations**. The merge excluded overlapping probes. The earlier RV32IM exp and Thumbv6-M sigmoid packets lacked their original checker images. Fresh whole-domain reruns supply both selected reports and their retained ELFs. All nine selected target reports bind to a retained checker ELF. [Coverage matrix with raw logs, objects and digests][matrix] · [Exact merge command and exit][merge-cmd] · [Full merge output][merge-out]

Host exp reused an earlier exhaustive run on the identical frozen source and kit fingerprint. Its logs establish range, exit and output agreement. The original host checker and sanitizer-library hashes are missing. The other eleven cells use fresh reruns. The inherited selector limits host sanitizer coverage to the host/RV arithmetic path. QEMU tests exercise the actual Thumb objects. The source review flags strict C11 questions about byte offsets from table subobjects and reads through incompatible structure types. These remain portability questions even with correct outputs on the pinned builds. [Evidence selection and exclusions][merged-checks] · [Source review][review]

## Reproduction and next experiment

From the final repository root, `python3 -B eik-work/delivery/verify.py` checks the archived evidence offline. The package records seven passing component verifiers and eleven rejected tampered-package tests. For this write-up, we checked the final commit archive against all 2,120 inventoried file sizes and SHA-256 digests, compared the root and packaged C bytes, and recomputed board scores from the raw class measurements. The twelve selected reports matched the frozen source, range and fingerprint, and all nine target checker hashes matched their images. These are checks on the existing measurements. [Verification logs][verified] · [Tamper tests][tamper] · [Inventory][inventory]

A cold evaluator run from the committed export is **incomplete**. The original 143,261,515-byte upload exceeded the export allowance. The reduced export contains 6,020,137 payload bytes and omits the Zig 0.17.1 wheel, Unicorn 2.1.4 wheel and upstream QEMU source archive. Its network-isolated preparation exited 1. With those three exact payloads restored by hash in scratch, offline bootstrap, setup, fingerprint, static check and sanitizer/QEMU smoke runs passed. The runtime manifest identifies the missing bytes. [Runtime manifest][runtime] · [Evidence verification and evaluator replay commands][replay]

For the next performance trial, start from former 50 and express the certified Thumb tanh cutoff as one test that can reuse the existing condition flags. Inspect the M0+ disassembly for added loads and branches, then measure typical and wide tanh costs, image bytes and S on new paired seeds. If the common path still pays more, the next candidate is a small-input sigmoid shortcut **inside** Thumb's existing exponent branch, where other inputs avoid the entry cost observed in all three shared-sigmoid trials. Any new candidate needs its own full-domain checks. A verified live comparison also requires the real champion's score on exactly the same fresh inputs. A fresh host exp run retaining its checker and sanitizer libraries would close the remaining host provenance gap. [Follow-up experiments][next]

## Landed work and final decision

| Batch | One item’s assignment and required result | Landed |
| --- | --- | ---: |
| `e01-baseline-foundation` | Prepare the pinned kit **or** evaluate one assigned source. A source packet records identity, methods, commands and paired scores, or the withholding response. | 9/9 |
| `e03-kernel-trials` | Produce one paired control, one single-change trial, or the final freeze. A trial supplies its source, diff, correctness evidence and seed-paired S. The freeze identifies the selected bytes and selection rule. | 10/10 |
| `e04-evidence-finalisation` | Complete one assigned validation or packaging item. Its result binds source/tool identities, measurements, logs, hashes and remaining gaps to an offline verifier. | 20/20 |

The handed records were `root-1-01` (baselines, trials and host checks), `root-1-02` (target checks and held-out results), `b02-freeze-entry`, and the `b03-` records for `board-snapshot`, `heldout-1` through `heldout-3`, `source-review`, `coverage-merge`, `offline-runtime` and `delivery-package`. The final package contains the source, nine held-out rows, experiment ledger, change note and log inventory. [Final package result][result]

```json
{
  "notes": "Deliver m0-tanh-refine as the best measured original fallback. Exhaustive output checks passed. Former 50 ties or beats it on every scored board. Reigning-source comparisons remain unavailable, so no live takeover is verified.",
  "finish": true
}
```

[raw-host-sigmoid]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/coverage/host-sigmoid/raw/exhaustive-sigmoid.stdout
[raw-host-tanh]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/coverage/host-tanh/rerun/whole/exhaustive-tanh.stdout
[raw-host-exp]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/trials/m0-tanh-refine/exhaustive-exp.stdout
[raw-rv32im-sigmoid]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/coverage/rv32im-sigmoid/rerun/report/rv32im-sigmoid-0-4096.json
[raw-rv32im-tanh]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/coverage/rv32im-tanh/rerun/logs/targetcheck-rv32im-tanh-all.stdout
[raw-rv32im-exp]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/merged/rerun/rv32im-exp/rv32im-exp.json
[raw-thumbv6m-sigmoid]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/merged/rerun/thumbv6m-sigmoid/thumbv6m-sigmoid.json
[raw-thumbv6m-tanh]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/coverage/thumbv6m-tanh/raw/targetcheck.stdout
[raw-thumbv6m-exp]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/coverage/thumbv6m-exp/reports/new/targetcheck-thumbv6m-exp-0-4096.stdout
[raw-thumbv7em-sigmoid]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/coverage/thumbv7em-sigmoid/logs/exhaustive.stdout
[raw-thumbv7em-tanh]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/coverage/thumbv7em-tanh/new/reports/thumbv7em-tanh-0-4096.json
[raw-thumbv7em-exp]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/coverage/thumbv7em-exp/reports/rerun/targetcheck-thumbv7em-exp-all.stdout
[analysis-37]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/baselines/former-37/report.json
[analysis-42]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/baselines/former-42/analysis.md
[analysis-46]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/baselines/former-46/README.md
[analysis-48]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/baselines/former-48/ANALYSIS.md
[analysis-50]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/baselines/former-50/ANALYSIS.md
[inventory]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/delivery/manifest.json
[boards]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/boards/snapshot.json
[refresh]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/tree/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/delivery/public-refresh
[csv]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/delivery/scores.csv
[scores]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/delivery/scores.json
[run1]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/tree/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/scores/heldout-1
[run2]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/tree/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/scores/heldout-2
[run3]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/tree/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/scores/heldout-3
[checks]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/delivery/CHECKS.md
[provenance]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/delivery/PROVENANCE.md
[fingerprint]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/review/logs/fingerprint.stdout
[source50]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/baselines/former-50/entry.c
[bases]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/tree/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/baselines
[diff]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/freeze/entry-vs-id50.diff
[proof]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/trials/m0-tanh-refine/ROUNDING.md
[tanh-cost]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/trials/m0-tanh-refine/MEASUREMENTS.md
[log]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/delivery/experiment-log.md
[ledger]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/delivery/experiments.json
[freeze]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/freeze/experiments.md
[review]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/review/review.md
[checklogs]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/tree/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/freeze/evidence/logs
[probes]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/review/logs/probe.stdout
[matrix]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/merged/coverage-matrix.json
[merge-cmd]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/merged/merger/selected.json
[merge-out]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/merged/merger/selected.stdout
[merged-checks]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/final-validation/merged/CHECKS.md
[verified]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/delivery/logs/verification.json
[tamper]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/delivery/logs/negative-tests.json
[runtime]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/offline-runtime/manifest.json
[replay]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/delivery/REPLAY.md
[next]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/delivery/next-steps.md
[result]: https://github.com/identity-md-launches/goal-3465-objective-build-entry-c-conjectures-io/blob/c5e3f91274b1f0c409127e8cfc14aa5ac8f392da/eik-work/delivery/result.json
