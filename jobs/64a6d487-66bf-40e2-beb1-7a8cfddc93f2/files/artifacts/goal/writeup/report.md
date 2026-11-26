# L-meta-5260 · The 63-gate lower bound

**The proof remains open in the supplied work.** All four results record `missing_lemma`. The strongest Lean result they report proves `63 ≤ C.size` **if** certain AND gates cover every incident point–line pair. The missing argument is why a circuit with at most 62 gates must have that coverage, or must otherwise be too large. No result contains a closed theorem `PEqualNP.Outside.L_meta_5260`, an acceptance of that theorem on another holder’s machine, or a contributor pull request submitting it. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

## What the theorem requires

The circuit has 26 inputs. The first 13 represent points and the next 13 represent lines. A point `p` lies on a line `l` when `p − l` modulo 13 belongs to `{0, 1, 3, 9}`. A **flag row** turns on just the two inputs of an incident pair. A **quadrangle row** turns on four points, no three collinear, and every line missing all four. There are 52 flag rows and 234 quadrangle rows. Each quadrangle row turns on seven inputs, four points and three lines. [Posted conclusion in the reduction][r731] · [Angle 3][a3] · [Angle 4][a4]

Let `a = x6` and `b = x7`. The circuit uses monotone AND and OR gates of fan-in at most two, each reading inputs or earlier wires. No AND gate lies in the input cone of another AND gate. Both wires must accept every flag. On every quadrangle at least one wire must reject. There must be a quadrangle on which only `a` accepts and one on which only `b` accepts. The conclusion counts gates already in this circuit. The known one-output flat bounds, 64 gates for all flags and 63 when one flag can be missed, require a wire that itself rejects every quadrangle. The strict witnesses rule that out for each wire here. Appending a final AND can put an existing AND in its input cone. [Target][r731] · [One-output bound][l1751] · [One-missing-flag bound][l7293] · [Angle 1][a1]

## Which Lean obligations remain

| Reduction at the source snapshot | Established in the results | Still required |
| --- | --- | --- |
| [R_meta_5260_731][r731] | [L_meta_6921][l6921] supplies `count`. Angles 1 and 2 report that the partial application elaborates. | `remaining` must supply a good AND gate for each flag under the small-circuit hypothesis. |
| [R_meta_5260_3][r3] | [L_meta_7967][l7967] supplies `sparse`. [L_meta_7969][l7969] supplies `extension`. Angle 1 reports checking both arguments together. | `bound` must prove the gate lower bound from the conditions on small accepted supports. |
| [R_meta_5260_17][r17] | The AND-gate count splits exhaustively into at most 12 and at least 13. | Both branches, `h1` and `h2`, need a proof of the lower bound. |

For the first route the exact term Angle 2 reports checking in Lean 4.36.0 is

```lean
fun rem => PEqualNP.Outside.R_meta_5260_731 PEqualNP.Outside.L_meta_6921 rem
```

Here `rem` is a proof input. Given a circuit of size below 63 that meets the structural and joint row conditions, it must produce, **for each flag**, a gate `j` with all of the following properties. Gate `j` is an AND. From `a` or `b` one can reach it by tracing back through OR gates (`OrReaches 26`). Its wire `26 + j` rejects every quadrangle row and accepts the given flag row. The stronger premise in route 731 omits the two strict witnesses. For the posted theorem it suffices to prove coverage with both strict witnesses available, since its hypotheses supply them. This narrower coverage obligation is also open. Angle 2 reports only the standard axioms `propext`, `Classical.choice` and `Quot.sound` for its conditional check. Angle 3 checked elaboration of the statement alone. Angle 4 reports script and paper checks. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4] · [Reduction source][r731]

The distinction between the two coverage statements can also be resolved within route 731. Suppose a circuit of size below 63 meets the joint row conditions but lacks a quadrangle on which only `a` accepts. Because the two wires never accept a quadrangle together, `a` must reject every quadrangle. Selecting `a` as the circuit output preserves its gate list, flatness and size. It accepts all flags, so the one-output theorem gives size at least 64, a contradiction. The same argument applies if the witness for `b` is missing. This discharges the cases without a strict witness and leaves the case with both witnesses as the substantive obligation. [One-output theorem][l1751] · [Route 731][r731]

**Why coverage would finish the proof.** A good AND that accepts a flag covers a star, meaning all flags it accepts share a point or all share a line. Let `A` be the set of such gates. Under full coverage their centres must cover the 13 disjoint flags `(i,i)`, so `|A| ≥ 13`. The formal count gives `|A| + |OrBot| ≥ 52`, where `OrBot` consists of OR gates in their input cones. It also gives `|OrTop| ≥ |A| − 2` for the OR gates joining them to the two wires. These three classes of gates are pairwise disjoint. Hence the circuit has at least `52 + (13 − 2) = 63` gates. The disjointness matters because both output wires may use the same gates. [Proof of main_bound][l6921] · [Angle 2][a2]

## Why the missing premise needs the size bound

There is a concrete circuit for which the two wires separate every required row, yet four flags have no good AND. For each point other than 0, OR its four incident lines, then AND that result with the point. Let `S` be the OR of those twelve stars. Take `a = S ∨ point₀` and `b = S ∨ (OR of the four lines through 0)`. The following count includes `S` once even though both outputs use it. [Angle 1][a1] · [Angle 3][a3] · [Angle 4][a4]

| Part of the circuit | Gates |
| --- | ---: |
| Twelve stars, three ORs and one AND each | 48 |
| OR of the twelve stars | 11 |
| Join the point input to `S` for `a` | 1 |
| OR the four lines and join the result to `S` for `b` | 4 |
| **Total** | **64** |

Every star is false on every quadrangle row. On those rows `a` accepts exactly when the quadrangle contains point 0, and `b` accepts exactly when it does not. On a flag at 0, `S` is false, yet the point input makes `a` true and its incident line makes `b` true. These four flags witness failure of coverage if the size restriction is removed. The example puts an upper bound of 64 on the minimum admissible size. Refuting the posted bound would require an example of size at most 62. None of the four results found one. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

Angle 2 gives a second circuit of 68 gates. It shares the stars at the other eleven points, exposes points 0 and 1 directly on one wire, and uses two products on the other. For point 0 the product is the OR of its four lines ANDed with the OR of point 0 and a line through 1 that misses 0. The other product interchanges 0 and 1. All eight flags at those two points lack a good AND, so the uncovered flags need not share a centre. Local Python re-enumeration reproduced both circuits’ sizes, fan-in, backwards reads, flatness, flag acceptance, joint quadrangle rejection, both strict witnesses and uncovered flag sets. These checks concern two specified circuits. [Angle 2][a2]

## What the alternative count has to explain

In the second route, `sparse` gives an accepted subrow on at most two inputs whenever a wire accepts. Call an accepted subrow of this size that fits in a quadrangle an *extra*. Each wire has an extra by its strict witness. An extra from each wire cannot fit together in one quadrangle, since then both wires would accept it. Their union has at most four inputs. The extension criterion decides exactly when such a union fits. It must contain no flag, at most three lines, no three collinear points and no three concurrent lines. The reported enumeration tested all 17,902 subsets of size at most four with zero mismatches, which local enumeration reproduced. Angle 1 also identifies the Lean proof of this criterion. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Extension theorem][l7969] · [Reduction using it][r3]

The unresolved case is a flag accepted using a direct input or a non-star product on one side, with the other wire still accepting the flag. For example, if direct inputs from both wires witness such flags, every cross-pair of those inputs must be incident: a single input or a nonincident pair would fit in a quadrangle. The resulting complete bipartite subgraph can only be a star, since the incidence graph has no four-cycle. A product of two ORs can cover many flags at once and also accept extra subrows. Counting its two input disjunctions independently of the rest of the circuit can charge shared OR gates twice. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

Angle 2 proposes keeping track of the uncovered flag set `M`, the number `k` of diagonal flags in it, the exposed AND gates `B` that accept a quadrangle, and the number `λ` of exposed inputs. Here “exposed” means reachable from either output by tracing back only through ORs. In the proposed count, the additional charges `2|B| + λ` plus ORs below those ANDs would have to pay for `|M| + k`, with an adjustment for shared gates. The 64-gate example already has `|M| = 4`, `k = 1`, `|B| = 0` and `λ = 5`. The proposed inequality and overlap adjustment remain unproved. A complete count also has to admit fan-in zero and one. The hand searches over merged stars, point and line constructions, and shared subtrees did not exhaust those possibilities. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

## Independent check and pull request

At upstream commit `9e9fd9cdf7fbb8d2e2533028c23741517e634da7`, the repository lookup for `lean/PEqualNP/Outside/L_meta_5260.lean` returned HTTP 404. The issue and pull-request search for `"L-meta-5260"` returned two merged PRs. **#10451** adds only `R_meta_5260_731.lean`. **#11800** adds only `R_meta_5260_17.lean`. Neither submits the requested theorem. The first PR also records the distinction between checking its counting child and leaving coverage open. [Pinned path lookup][lookup] · [PR search][search] · [#10451 changed files][pr731] · [#11800 changed files][pr17] · [#10451 discussion][discussion]

The four inputs supply no completed proof for another holder to check. Consequently there is no theorem acceptance or subsequent proof PR to cite for this goal. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4] · [Project acceptance criteria][readme]

[a1]: ../items/angle-1/result.json
[a2]: ../items/angle-2/result.json
[a3]: ../items/angle-3/result.json
[a4]: ../items/angle-4/result.json
[r731]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/R_meta_5260_731.lean
[r3]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/R_meta_5260_3.lean
[r17]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/R_meta_5260_17.lean
[l6921]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/L_meta_6921.lean
[l7967]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/L_meta_7967.lean
[l7969]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/L_meta_7969.lean
[l1751]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/L_meta_1751.lean
[l7293]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/L_meta_7293.lean
[lookup]: https://api.github.com/repos/open-goat/pequalnp-proofs/contents/lean/PEqualNP/Outside/L_meta_5260.lean?ref=9e9fd9cdf7fbb8d2e2533028c23741517e634da7
[search]: https://api.github.com/search/issues?q=repo%3Aopen-goat%2Fpequalnp-proofs+%22L-meta-5260%22
[pr731]: https://github.com/open-goat/pequalnp-proofs/pull/10451/files
[pr17]: https://github.com/open-goat/pequalnp-proofs/pull/11800/files
[discussion]: https://github.com/open-goat/pequalnp-proofs/pull/10451
[readme]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/README.md
