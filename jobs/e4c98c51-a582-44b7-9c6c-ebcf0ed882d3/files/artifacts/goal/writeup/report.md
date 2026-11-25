# Proof status of L-meta-2341

**L-meta-2341 remains unproved in the four supplied results.** All four record `missing_lemma`. The Lean reduction reaches the requested statement once a lower bound for circuits with at least two nested AND pairs is supplied. The only reported attempt to assemble the theorem used `sorry` for that bound. The results supply neither a check of a complete proof by another holder nor a pull-request URL for a submission by the proving contributor to `open-goat/pequalnp-proofs`. [Direct proof attempt][a1] · [Helper lemmas][a2] · [Gate-elimination attempt][a3] · [Lean composition and counterexample search][a4]

## The bound and a circuit attaining it

Points and lines each have labels modulo 13. A point `p` and line `l` form a *flag* when `(p − l) mod 13` belongs to `{0, 1, 3, 9}`. The circuit has 13 point inputs, 13 line inputs and a fixed bit `x4`. It uses fan-in-two AND and OR gates with backward wire references. It must accept the point-plus-line input of every flag except possibly the designated pair `(x2, x3)`. For every quadrangle (four points with no three collinear), it must reject the input consisting of those points and the lines missing all four. The claim is `63 ≤ C.size`. [Direct proof attempt][a1] · [Helper lemmas][a2] · [Lean composition and counterexample search][a4]

The enumeration found 52 flags and 234 quadrangles, each with three missing lines. When the designated pair is a flag, omit it from the incidence relation. For each line, OR its remaining incident points and AND that result with the line input. OR the 13 results. The 51 retained incidences require `51 − 13 = 38` point ORs, 13 line ANDs and 12 final ORs, totaling **63 gates**. On a quadrangle input, each active line misses every active point, so every line AND is false. Two items report simulating the construction for all 52 choices of freed flag and both values of `x4`. When the designated pair is nonincident, all flags remain required and the same construction uses 64 gates. [Direct proof attempt][a1] · [Gate-elimination attempt][a3] · [Counterexample search][a4]

## Where the Lean proof stops

In the project snapshot identified as `e125f04d0dc6fed67cee48a1d06692912e167c32`, the reduction `R_meta_2341_417` splits on `TopForm.andPairs 27 C`. This counts ordered pairs of AND gates in which one lies strictly inside the other's input cone. An indirect dependency counts. [Helper lemmas][a2] · [Lean composition][a4]

| Nested AND pairs | Evidence for the 63-gate lower bound |
| --- | --- |
| Zero | `L_meta_5809` supplies the 27-input case. [Helper lemmas][a2] · [Lean composition][a4] |
| Exactly one | `L_meta_5811` supplies the one-pair case. Angle 3 lists `single` as open. Angle 4 reports compiling the application of the reduction with this lemma in that argument position. [Gate-elimination attempt][a3] · [Lean composition][a4] |
| At least two | The premise named `several` remains open in the results. Angle 4 reports compiling the reduction with the two lemmas above and an admitted proof of this premise. The resulting axiom list included `sorryAx`. [Direct proof attempt][a1] · [Helper lemmas][a2] · [Lean composition][a4] |

Specifically, `several` assumes `Monotone2 C`, `NestedCover.ReadsBack 27 C`, and `2 ≤ TopForm.andPairs 27 C`. It retains the required flag acceptances and quadrangle rejections. It also assumes rejection of every input consisting of two points and two lines with all four cross-pairs nonincident. The direct enumeration found that each such input lies inside a quadrangle negative, which explains this extra rejection hypothesis by monotonicity. Under these assumptions the missing conclusion is still `63 ≤ C.size`. [Direct proof attempt][a1] · [Lean composition][a4]

Two other reductions in the snapshot give context for the missing case. `R_meta_2341_1` translates the designated flag. `R_meta_2341_214` recasts the problem as a search over at most 61 new columns on 285 tests. Angle 2 also identifies the premise `dirty` of `R_meta_4732_639` as another route. After simplification, it would suffice to rule out a minimum separator of size below 63 that has a nested AND pair and in which each such inner AND accepts some quadrangle negative. The items supply neither that exclusion nor a completed search. [Direct proof attempt][a1] · [Helper lemmas][a2] · [Gate-elimination attempt][a3]

## What the counting argument establishes

In the incidence graph, two distinct points cannot share two lines. Consequently every complete bipartite subgraph with an edge is a star. After one flag is freed, the remaining graph still has a perfect matching of size 13, so covering its edges by stars needs at least 13 centers. This explains the count `51 + 13 − 1 = 63` for the star construction. In a general circuit an inner AND can accept an unwanted pair, and a later AND can remove that pair while preserving required flags. Counting the output stars leaves the cost of those shared intermediate gates unresolved. [Direct proof attempt][a1] · [Helper lemmas][a2] · [Gate-elimination attempt][a3]

Angles 1 and 3 propose a lower bound of `|E| + τ(E) − 1` for restricted flag sets, where `τ(E)` is the minimum vertex-cover size. Their induction needs to show that deleting a variable saves its incident-edge count plus the decrease in cover size. Neither derives that saving in the presence of sharing. Angle 3 reports that all 26 one-flag deletions tested on six small configurations matched the proposed count. Angle 4 found a four-vertex path where a nested AND attains the star count, so even an optimal circuit can contain nesting. The searches supply no circuit with 62 or fewer gates for the full instance and no exhaustive exclusion at that size. [Direct proof attempt][a1] · [Gate-elimination attempt][a3] · [Counterexample search][a4]

[a1]: ../items/angle-1/result.json
[a2]: ../items/angle-2/result.json
[a3]: ../items/angle-3/result.json
[a4]: ../items/angle-4/result.json
