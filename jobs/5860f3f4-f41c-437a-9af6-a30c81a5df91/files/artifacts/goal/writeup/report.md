# L-meta-4297 remains open in the four submitted results

All four source results report `missing_lemma`. None supplied a closed Lean 4 proof of `PEqualNP.Outside.L_meta_4297`. Angle 4 checked two ways to apply existing reductions to the requested statement. Lean accepted each application with one proof obligation still open. The results contain no record of another holder checking a completed theorem and no pull request from a proving contributor containing it. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

The reviewer's pinned repository tree at `d03458b7bedbd651aca853929f2a5c0e005c72c9` contains three Lean filenames for this step. Each declares a theorem beginning with `R_meta_4297_` and takes two hypotheses. PR #8663 contributed the rectangle reduction, #9178 the circuit normalization reduction, and #8803 the wire-pair reduction. None of those PRs contains `L_meta_4297.lean`. [Pinned recursive tree][tree] · [#8663 files][pr1] · [#9178 files][pr271] · [#8803 files][pr284]

## The statement to prove

Let `F` be the edge function of a four-cycle-free bipartite graph. It is true when both endpoints of some edge are true. The circuit `C` computes `F`, uses binary AND and OR gates, and has a valid output wire. A wire is *below the output* when every input that makes the wire true also makes the output true. The lift hypothesis requires that if either operand of an OR gate is a gate wire below the output, the other operand is below it as well. [Target statement in the wire-pair reduction][r284]

The conclusion asks for a list of nonempty stars covering exactly the edges, with total leaf count plus number of stars minus one at most `C.size`. For a nonempty edge set `E`, the least possible cost is `|E| + τ − 1`, where `τ` is the minimum vertex-cover size. Each edge needs a leaf occurrence, and the centers cover all edges. Conversely, assign each edge to one endpoint in a minimum cover and group the edges by that endpoint. This uses one leaf per edge and at most `τ` stars. For an empty edge set the empty list has cost zero under Lean's natural-number subtraction. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

## What Lean checked and what would close the goal

Angle 4 reports compiling scratch copies of the project files and applying each reduction to the statement copied from the step. The two rows are independent routes. A proof of **either** remaining obligation would suffice. [Angle 4][a4]

| Application accepted by Lean in angle 4 | Remaining obligation |
| --- | --- |
| `refine PEqualNP.Outside.R_meta_4297_271 PEqualNP.Outside.L_meta_7649 ?_` | **`h2`**. Construct a binary AND/OR circuit computing the same function, of size at most the original size, in which every gate outside the part below the output is an OR whose operands are also outside that part. The obligation does not assume the original output-index bound. [Reduction][r271] · [Proved counting lemma][l7649] |
| `refine PEqualNP.Outside.R_meta_4297_284 PEqualNP.Outside.L_meta_7372 ?_` | **`hProducts`**. Suppose every gate of a binary AND/OR circuit `D` can be true on some input where `F` is false. Let `B` be a list of wire pairs of `D` such that `F` is exactly the OR of their pairwise ANDs. For a four-cycle-free graph, construct an exact star cover of cost at most `D.size + 2 * B.length − 1`. The proved separation lemma gives `D.size + 2 * B.length ≤ C.size + 1`. [Reduction][r284] · [Proved separation lemma][l7372] |

Angle 3 left the first route's counting lemma as a paper argument. Angle 2 identified both available helpers by reading their statements, and angle 4's applications confirm those matches. Angle 4 also identified `L_meta_8725`, which rules out exactly one AND outside the part below the output under its least-circuit hypotheses. That result leaves the case of two or more such ANDs unresolved. [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4] · [L_meta_8725][l8725]

## Why the gap matters

An individual input wire is true on its singleton assignment, where `F` is false. The lift condition for OR and the semantics of AND then imply that a gate outside the part below the output reads only wires outside it. This permits the separation used by `L_meta_7372`. The cost of converting the resulting wire products to stars is the outstanding issue. [Angle 1][a1] · [Angle 2][a2] · [Wire-pair reduction][r284]

The three-edge path shows why counting one star per AND below the output fails. Form `r = (x₁ ∨ x₂) ∧ (y₁ ∨ y₂)` and take `r ∧ (x₁ ∨ y₁)` as output. The first AND accepts all four cross pairs. The last AND removes the nonedge `x₂y₂`, leaving edges `x₁y₁, x₁y₂, x₂y₁`. The resulting five-gate circuit satisfies the lift hypothesis and has just one AND below the output. Covering the path requires two stars, of minimum cost four. Angle 1 also notes that setting an input to false can change which wires are below the output, so induction by restriction would need to reestablish the lift condition. [Angle 1][a1] · [Angle 3][a3]

Angle 1 proposed two inequalities for the wire-pair route. If `k = B.length` and `M` is a maximum matching, they are `#OR(D) + k ≥ |E|` and `#AND(D) + k ≥ |M|`. Adding them would give the required budget because `|M| = τ` for a bipartite graph. Both inequalities remain conjectural. [Angle 1][a1]

The third reduction, `R_meta_4297_1`, has a different defect. Angle 2 identified `L_meta_6172` for its rectangle-to-star hypothesis. Its other hypothesis, `hRectangles`, demands the rectangle cost bound for **all** bipartite relations. Angle 1 exhibited the half graph with edge `aᵢbⱼ` exactly when `i ≤ j`. With four vertices on each side, prefix ORs give a lifted circuit of size 10, but the minimum sum of rectangle side sizes is 12, requiring `12 − 1 ≤ 10`. With five vertices on each side the corresponding figures are 13 and 16. Enumerating all bicliques and minimizing their total side sizes over covers reproduced both minima during this write-up. These graphs contain a four-cycle, which explains how they refute this auxiliary hypothesis while leaving the target open. [Angle 1][a1] · [Angle 2][a2] · [Rectangle reduction][r1] · [L_meta_6172][l6172]

## Extent of the computational evidence

| Result | Search reported by its contributor |
| --- | --- |
| [Angle 1][a1] | Every bipartition and every nonempty four-cycle-free graph for 2–3 vertices through 6 gates, and for 4–6 vertices through 5 gates. The six-vertex search reports 1,691,918,298 circuits. No qualifying circuit violated the bound. |
| [Angle 2][a2] | Ruled out sizes up to 3 for the three-edge path and up to 7 for the six-cycle. For the six-cycle with a pendant edge, ruled out sizes through 7. Size 8 hit the 90-second limit. |
| [Angle 3][a3] | Completed the lower-bound search for connected cases through 7 vertices, including size 8 for the six-cycle with a pendant edge, and for 8-vertex cases of bound at most 9. For five 8-vertex graphs of bound 10, ruled out sizes through 8. Size 9 timed out. |
| [Angle 4][a4] | Without requiring lift, found no smaller circuit for all 40 four-cycle-free bipartite graphs without isolated vertices on 2–7 vertices up to isomorphism, and for 39 of 52 on 8 vertices. The other 13, with bounds 10–12, were outside the completed search. The same program found a three-gate circuit for the excluded four-cycle. |

The pendant-edge results agree where the searches overlap. Angle 3 reached the next size after angle 2 timed out. All four results support the bound in their tested ranges. The general step still needs a closed Lean proof before another holder can check that proof and the proving contributor can submit it. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

[a1]: ../items/angle-1/result.json
[a2]: ../items/angle-2/result.json
[a3]: ../items/angle-3/result.json
[a4]: ../items/angle-4/result.json
[tree]: https://api.github.com/repos/open-goat/pequalnp-proofs/git/trees/d03458b7bedbd651aca853929f2a5c0e005c72c9?recursive=1
[pr1]: https://github.com/open-goat/pequalnp-proofs/pull/8663/files
[pr271]: https://github.com/open-goat/pequalnp-proofs/pull/9178/files
[pr284]: https://github.com/open-goat/pequalnp-proofs/pull/8803/files
[r1]: https://github.com/open-goat/pequalnp-proofs/blob/d03458b7bedbd651aca853929f2a5c0e005c72c9/lean/PEqualNP/Outside/R_meta_4297_1.lean
[r271]: https://github.com/open-goat/pequalnp-proofs/blob/d03458b7bedbd651aca853929f2a5c0e005c72c9/lean/PEqualNP/Outside/R_meta_4297_271.lean
[r284]: https://github.com/open-goat/pequalnp-proofs/blob/d03458b7bedbd651aca853929f2a5c0e005c72c9/lean/PEqualNP/Outside/R_meta_4297_284.lean
[l6172]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d/lean/PEqualNP/Outside/L_meta_6172.lean
[l7372]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d/lean/PEqualNP/Outside/L_meta_7372.lean
[l7649]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d/lean/PEqualNP/Outside/L_meta_7649.lean
[l8725]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d/lean/PEqualNP/Outside/L_meta_8725.lean
