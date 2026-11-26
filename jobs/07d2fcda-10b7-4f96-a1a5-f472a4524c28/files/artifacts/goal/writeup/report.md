# L-meta-3039: consolidated proof status

The supplied results do **not** complete the goal. Each has status `missing_lemma`. None delivers a Lean theorem proving L-meta-3039 without an additional unproved hypothesis, a successful check of that theorem by another holder, or a pull-request URL. This report records the partial work and its limits; it is not a proof submission. [S1–S4]

The requested outcome is a Lean 4 theorem for L-meta-3039, checked on another holder’s machine and opened as a pull request on `open-goat/pequalnp-proofs` from the proving contributor’s account. The supplied evidence does not establish any of those completion milestones. A conditional derivation or successful elaboration of a statement is insufficient. [Task; S1–S4]

## Sources and evidence limits

The sources are the four supplied JSON results. Citations below refer to their `notes` fields unless expressly referring to `status`. Their SHA-256 digests were checked against the task’s supplied digests. The original scratch Lean files and their compiler logs are not included in those results; reported checks below are contributor reports, not independently rerun checks or certification by another holder. [S1–S4]

| Citation | Supplied source | SHA-256 |
| --- | --- | --- |
| S1 | `.imd/reads/artifacts/item-angle-1`, designated `artifacts/goal/items/angle-1/result.json` | `504e1f2ea1ff2dd50ce3ea984bab3c1468e3349dc4153f4a38ee6dd3d9c3b938` |
| S2 | `.imd/reads/artifacts/item-angle-2`, designated `artifacts/goal/items/angle-2/result.json` | `ea4436e63f97d0002e20537dbc890d1caadeb3b80fce75a10de2959604aa0cf4` |
| S3 | `.imd/reads/artifacts/item-angle-3`, designated `artifacts/goal/items/angle-3/result.json` | `ed3d1e061229146dfb64022e8b382580a57a9d0a4431ea5d4acc4e0f44eea55f` |
| S4 | `.imd/reads/artifacts/item-angle-4`, designated `artifacts/goal/items/angle-4/result.json` | `fa3d1e8efa8873afce619f4c4b3c41dcc3a171d72bc02b7d0160631624fb5f6c` |

Representative exact source passages make the lack of a proof explicit:

- S1: “I could neither prove nor refute `dense`.”
- S2: “Not proved; no Lean file is returned.”
- S3: “Not proved: one lemma is missing, and no Lean file is delivered.”
- S4: “No Lean file is offered.”

Repository file names and historical branch observations below are attributed to these results. This write-up does not establish their current availability. The project URL supplied by the task is https://github.com/open-goat/pequalnp-proofs ; no current upstream status is needed to establish what the supplied results contain.

## Statement and outstanding obligation

Using the sources’ notation, let `q` be the projective-plane order and `N = q² + q + 1`. The circuit `C` is a minimal monotone fan-in-two AND/OR circuit on point and line inputs. It rejects the specified inputs with at most `q` selected lines and no selected incident point-line pair. The pruned circuit `D` replaces each two-input AND whose inputs both have positive line-degree by false. Let `E` be the incident pairs accepted by `C` but rejected by `D`, and let `A` be the gates false on the all-false input and true on at least one pair in `E`. The target inequality is `|E| ≤ 44 |A|`. This is a summary of the statement reported by the contributors, not a replacement for its exact Lean definition. [S1, S2, S4]

S1 reports that the following conditional term elaborated against the step’s exact statement, without errors or `sorry`, under Lean 4.36:

```lean
PEqualNP.Outside.R_meta_3039_317 PEqualNP.Outside.L_meta_3487 dense
```

Here `dense` is an unresolved proof argument. As described in S1, it must bound `|E|` by `44 * C.size` for the reduction’s circuit and incidence hypotheses when `q ≥ 87`, both evidence supports have cardinality greater than `7656`, and `44 * (P + L - 1) < |E|`, where `P` and `L` count evidence points and lines. S1 identifies this as the outstanding L-meta-3489 obligation. The reduction is therefore not a closed theorem for L-meta-3039. [S1]

S1 reports that L-meta-3487 supplies the reduction’s small-support assumption. S4 independently reports elaborating the reduction with its `small` and `dense` assumptions, but only numerically sampled the small-support bound itself. These are different evidence levels: S4’s sampling is not a proof, and S1’s reported reuse of L-meta-3487 does not prove `dense`. [S1, S4]

## Findings retained from each angle

**Angle 1 — reduction route.** Besides the conditional term above, S1 reports an alternative route through `R_meta_3039_8` and `L_meta_4659`, explicitly leaving a `sorry` for the other branch. It identifies a sparse-support threshold of `1893` and a vacuous dense branch for `q ≤ 43` through L-meta-6428. With its reported L-meta-3487 route, it says the target is settled for `q ≤ 86`. These are partial reductions, not a completed general proof. [S1]

S1 reports that its snapshot at `e125f04d` and its branch searches on 2026-11-26 contained reductions but no `L_meta_3039.lean` or `L_meta_3489.lean`. This is a historical search report, not a fresh assertion about the remote repository. Its informal circuit analysis compares the problem to lower bounds for disjoint Boolean sums, but finds neither a usable replacement argument across line sets nor a counterexample. Its small-case observations include the nonempty-evidence active-output argument and a hand-constructed nonvacuous circuit with two evidence pairs. Those observations were not formalized in the supplied result. [S1]

**Angle 2 — helper lemmas.** S2 reports scratch elaboration under Lean 4.36.0, without errors or `sorry`, of helper facts for wire lengths, preservation of input wires, monotonicity, existence of an active output gate, and tracing a changed wire to a replaced gate that was true in `C`. It reports assembling the empty-evidence case and the case `|E| ≤ 44`. The scratch proofs are not delivered. [S2]

Its remaining obstacle is quantitative: assigning an evidence pair to an active or replaced gate does not bound how many pairs use that gate. In particular, the output gate can be active on every evidence pair. S2 supplies a hand argument for a minimal circuit with one evidence pair and two active gates, showing why it cannot close the theorem by claiming the hypotheses contradictory. It found no counterexample and did not consult the literature; its statements about missing library support must not be read as an exhaustive impossibility result. [S2]

**Angle 3 — support-count decomposition.** S3 reports a scratch conditional derivation using helpers from L-meta-4659 plus a new `glue2` lemma. Its low-density branch uses `P + L ≤ |A| + 1`: if `|E| ≤ 44(P + L - 1)`, the goal follows. A second branch covers one support of size at most `1893`. The remaining branch has both supports at least `1894`, `q ≥ 44`, and `44(P + L - 1) < |E|`; S3 names its required hypothesis `DENSE`. Neither completed branch uses minimality or the pruned circuit, according to S3. [S3]

S3 illustrates the gap with the conditional example `q = 89`: `N = 8011` and all `8011 * 90 = 720990` incidences as evidence would require at least `16387` active gates, whereas the support count supplies only `16021`. This is an arithmetic illustration, not a constructed circuit meeting every hypothesis. S3 associates its missing argument with the L-meta-4661 reduction route and reports unsuccessful searches through related reductions, including those for L-meta-3686 and L-meta-5220. It could not make a first-AND-gate charging argument work: one gate may serve a rectangle of pairs, while rejection of nonincident pairs must be enforced elsewhere. Its suggested circuit replacement argument remains a proposal. [S3]

**Angle 4 — counterexample and small cases.** S4 reports statement elaboration with an open proof body and reduction elaboration without errors; only the latter is a completed conditional check. Its hand argument obtains `P + L ≤ 2|A|` and then `|E| ≤ (q + 1)|A|`, proving the desired factor for `q ≤ 43` if those arguments are formalized. It says a counterexample would consequently need `q ≥ 44` and at least `3962` inputs; accepting the small-support reduction would push the search to `q ≥ 87` with more than `7656` points and lines in evidence. [S4]

S4’s numerical sampling supports, but does not prove, the small-support extremal inequality. It found no counterexample among the informal circuit families discussed and could not certify minimality for a dense candidate. It describes the dense problem as a superlinear monotone circuit lower bound and warns that counting one level of AND gates is inadequate. Its mention of a Jukna source has no URL or passage in the supplied JSON, so no external literature theorem is adopted here on that basis. [S4]

## Reconciliation and completion status

The different cutoffs do not describe conflicting full proofs. The `43` cutoff belongs to the elementary or sparse route; the `86` cutoff is reported using the stronger small-support result L-meta-3487. S4’s lack of a proof of `small` is a limit of that angle, while S1 reports an existing theorem that discharges it. Likewise, S3’s `DENSE` for orders at least `44` and S1’s L-meta-3489 obligation for orders at least `87` belong to different reductions and must not be silently identified as identical Lean statements. Both routes leave a dense lower-bound obligation. [S1, S3, S4]

All four agree on the essential limit: no unconditional proof is supplied, and no counterexample is established. “Missing” here describes the supplied work; it does not establish that the theorem is false or globally unproved. Reported local elaborations of helpers or conditional reductions do not demonstrate independent verification of a completed theorem. [S1–S4]

The reviewer’s substantive finding is supported by these inputs: the requested theorem, independent check, and pull request are absent. The prior report quoted in the finding was not present in this revision checkout, so its exact line references could not be reproduced. This write-up cannot truthfully close that finding by relabeling the conditional term as a theorem. Completion requires a proof of the outstanding obligation (or another unconditional proof of the exact target), the other-holder check, and the requested pull request. None of their artifacts or identifiers can be recovered from the supplied results. [Task; S1–S4]
