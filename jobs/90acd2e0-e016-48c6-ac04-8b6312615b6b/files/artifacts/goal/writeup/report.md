# Proof status of L-meta-6752

**The goal remains open in the four supplied results.** All four return `missing_lemma`. The contributors report Lean checks of the counting argument and of restricted cases. None supplies a Lean proof of the posted theorem, a check of that proof by another holder, or a pull request opened by the proving contributor after that check. The public reductions for this step also have premises that still need proofs. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4] · [Public reduction][r643]

## The inequality to prove

Fix the step's 11-vertex, 16-edge graph `G` and a circuit `C` satisfying `C.size ≤ 21`, `IsLeastAO G C`, and `TopForm G C`. Write `U = Ustar G C` for the residual edges, `J = junk G C` for the junk gates, and `S = x9` for the nonempty subset of `U` in the statement. Let `u = |U|`, `j = |J| ≥ 2`, `c = |centreless G C|`, and `o = |orN G C ∖ lam G C|`. For each junk gate `g`, its edge set is `γ(g) = gammaE G C g`. [Posted conclusion in the public reduction][r643] · [Angle 2][a2]

Let `d = |U ∖ S|`, let `j₀` count the junk gates whose edge sets are disjoint from `S`, and let `jₛ` count the others. The hypotheses give `d ≤ j₀`, every edge in `U` belongs to some `γ(g)` for `g ∈ J`, and no `S ∩ γ(g)` has exactly one edge. The requested conclusion is **`|S| ≤ 2c + (j − d) + o`**. Since `d ≤ j₀ ≤ j`, natural-number subtraction is exact. Adding `d` to both sides and using `|S| + d = u` gives the equivalent obligation **`u ≤ 2c + j + o`**, under the same hypotheses. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

Angle 2 reports that the following helper elaborated in Lean 4.36.0. Take `K` to be the filter of junk gates disjoint from `S`. The proof uses only the subset and cardinality hypotheses once it has `charge`. [Angle 2][a2]

```lean
theorem assemble {α β : Type} [DecidableEq α] [DecidableEq β]
    (U S : Finset α) (J K : Finset β) (c O : ℕ)
    (hS : S ⊆ U) (hK : K ⊆ J) (h : (U \ S).card ≤ K.card)
    (charge : U.card ≤ 2 * c + J.card + O) :
    S.card ≤ 2 * c + (J.card - (U \ S).card) + O := by
  have h1 : (U \ S).card + S.card = U.card :=
    Finset.card_sdiff_add_card_eq_card hS
  have h2 : K.card ≤ J.card := Finset.card_le_card hK
  omega
```

## Cases covered

| Sufficient condition | Reason the requested inequality follows |
|---|---|
| `u ≤ j + 1` | Since `S` is nonempty, so is `U`. The connection lemma gives `1 ≤ 2c + o`. This covers every `u ≤ 3` because `j ≥ 2`. [Angle 3][a3] · [Angle 4][a4] |
| `u ≤ 4` | For `j ≥ 3`, the preceding row suffices. For `j = 2`, `L_meta_7895` gives either `2 ≤ 2c + o`, enough for four edges, or a nested configuration of the two junk gates. In that configuration `L_meta_7897` gives `u ≤ 3` under the size hypothesis. Angle 3 reports checking the combined argument in Lean. [Angle 3][a3] · [Dichotomy][l7895] · [Nested case][l7897] |
| `S.card ≤ jₛ + 1` | Adding `d ≤ j₀` gives `u ≤ jₛ + j₀ + 1 = j + 1`. Coverage gives `jₛ ≥ 1`, so this includes `S.card ≤ 2`. It includes `S.card = 3` if at least two junk gates meet `S`. [Angle 1][a1] |

There is a further restriction on a possible failure with **exactly two junk gates**. Let `D` be the union, over junk gates `g`, of the edges in `γ(g)` with an endpoint in `wmax G C g`. The proved lemma `L_meta_7559` gives `|U ∖ D| ≤ 2 + o`. Thus whenever `|U ∩ D| ≤ 2c`, adding the two cardinalities gives `u ≤ 2 + o + 2c`, exactly the required bound for `j = 2`. This deduction applies for any `u`. The inputs supply no general bound of `2c` on the intersection. [Angle 2][a2] · [Statement of L_meta_7559][l7559]

## The remaining proof obligation

It suffices to prove `u ≤ 2c + j + o` for **`u ≥ 5` and `u ≥ j + 2`** with all the original circuit hypotheses. In that range `|S| = u − d ≥ jₛ + 2`. A failure with `j = 2` would additionally require `2c + o ≥ 2` by the nested-case argument, and `|U ∩ D| > 2c` by the preceding paragraph. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3]

One sufficient structural lemma would bound **`|S| ≤ jₛ + 2c + o`**. Adding `d ≤ j₀` would then prove the result. The difficulty is accounting for several edges covered by the same gate. Angle 1 derives junk-gate coverage already from leastness and top form. Angle 2 traces an edge to a junk gate and a gate reading its output, but several edges can give the same pair. Counting available operand slots bounds the number of gates reached. A proof still has to bound the number of distinct residual edges that pass through them. [Angle 1][a1] · [Angle 2][a2]

Two checks explain why the distinction matters.

- In angle 4's abstract set example, `S = U` has four edges and both junk gates cover all four. With `c = 0` and `o = 1`, coverage, the disjoint-gate budget, and the no-singleton condition all hold, yet the desired inequality reads `4 ≤ 3`. This example makes no claim to realize a least circuit. Angle 3's nested-case argument settles precisely the four-edge issue for actual circuits. The stronger bound `2u ≤ 2c + j + o` from `L_meta_6240` requires at most one residual edge per centreless, junk, or mixing gate. A junk gate meeting `S` here covers at least two. [Angle 1][a1] · [Angle 3][a3] · [Angle 4][a4]
- Writing `t = |tops ∖ centreless|`, the size ledger gives `16 + t + 2c + j + o ≤ C.size + u + 1`, hence `t + 2c + j + o ≤ 6 + u`. This upper bound is compatible with a shortfall in `2c + j + o`. The graph has a vertex cover of size seven, namely `{4,5,6,7,8,9,10}`. The disjoint triangles on `{1,4,8}` and `{3,6,7}` each require two vertices, and the disjoint cycle `0–9–5–2–10–0` requires three, proving minimality of that cover. The star construction therefore uses `16 + 7 − 1 = 22` gates. A lower bound of 22 for every eligible circuit would rule out the size hypothesis, but the results give such lower bounds only with extra assumptions. Angle 4's SAT search on a 22-gate instance did not finish within 400 seconds and produced no certificate or counterexample. [Angle 1][a1] · [Angle 3][a3] · [Angle 4][a4] · [Graph edge list][r643]

## What the public pull requests establish

At revision `252e69c`, angle 3 identified three reductions. `R_meta_6752_452` assumes a bound on a minimal remaining edge set. `R_meta_6752_859` splits according to whether one gate carries two vertex-disjoint edges. `R_meta_6752_643` further separates the pairwise-intersecting case into common-vertex and triangle cases. Each reduction takes the corresponding counting bounds as premises. [Angle 3][a3] · [Minimal-set reduction][r452] · [Disjoint-edge split][r859] · [Common-vertex and triangle split][r643]

The file changes in PRs #22237 and #22164 are the `_643` and `_859` reductions respectively. PR #22548 also carries the step name, but its theorem `R_meta_6752_1` takes the active-gate estimate above as an explicit `fiberCharge` premise. These records explain why a PR title matching L-meta-6752 cannot establish completion. The four job results stop before a full proof was available for another holder to check and for the proving contributor to submit. [PR #22237][pr643] · [PR #22164][pr859] · [PR #22548][pr1] · [Premises of R_meta_6752_1][r1] · [Angle 2][a2] · [Angle 4][a4]

[a1]: ../items/angle-1/result.json
[a2]: ../items/angle-2/result.json
[a3]: ../items/angle-3/result.json
[a4]: ../items/angle-4/result.json
[r452]: https://github.com/open-goat/pequalnp-proofs/blob/252e69c/lean/PEqualNP/Outside/R_meta_6752_452.lean
[r643]: https://github.com/open-goat/pequalnp-proofs/blob/252e69c/lean/PEqualNP/Outside/R_meta_6752_643.lean
[r859]: https://github.com/open-goat/pequalnp-proofs/blob/252e69c/lean/PEqualNP/Outside/R_meta_6752_859.lean
[l7559]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04/lean/PEqualNP/Outside/L_meta_7559.lean
[l7895]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04/lean/PEqualNP/Outside/L_meta_7895.lean
[l7897]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04/lean/PEqualNP/Outside/L_meta_7897.lean
[pr643]: https://github.com/open-goat/pequalnp-proofs/pull/22237/files
[pr859]: https://github.com/open-goat/pequalnp-proofs/pull/22164/files
[pr1]: https://github.com/open-goat/pequalnp-proofs/pull/22548/files
[r1]: https://github.com/open-goat/pequalnp-proofs/blob/310f0df531bc06c53c819f9950070f1f32535cd7/lean/PEqualNP/Outside/R_meta_6752_1.lean
