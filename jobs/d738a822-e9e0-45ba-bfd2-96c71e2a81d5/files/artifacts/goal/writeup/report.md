# L-meta-2584 — proof status

**The four results leave L-meta-2584 unresolved.** Each reports `missing_lemma`. None supplies Lean source proving `PEqualNP.Outside.L_meta_2584`, a successful check of that source revision on another holder's machine before submission, or the proving contributor's pull request containing it. The Lean checks reported below concern reductions and individual circuits. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

The public pull request titled *L-meta-2584*, #12013, describes a reduction. At commit `83d1576e60371dd69010f709c01fd70a178a8624`, the declaration is `PEqualNP.Outside.R_meta_2584_1`. Its hypothesis `h1` supplies a circuit of the required size computing the same function, with the required read bound on every edge. Its hypothesis `h2` turns that per-edge bound into `IsReadK`. The proof takes its witness directly from `h1` and applies `h2`. The PR was closed and lists no reviews. [Lean declaration and body][lean] · [PR #12013][pr]

## What remains to prove

Let the points and lines form a bipartite incidence graph with no four-cycle. Its Boolean function is true exactly when the input selects both endpoints of some edge. Given **any** binary AND/OR circuit `C` computing this function, the goal asks for a binary AND/OR circuit `D` computing it with `D.size ≤ C.size` and `IsReadK (P + L) D 2`. Any true input contains an incident point–line pair, and the pair alone suffices. The prime implicants are precisely those pairs. Thus each edge needs a proof tree reading each endpoint at most twice. Different edges may use different trees in the same circuit. [Angle 1][a1] · [Angle 3][a3] · [Angle 4][a4] · [Formal conclusion][lean]

Angle 1 reports a scratch Lean check of this reduction. For an edge `(p,l)`, the project's `setList` orders the wires as `[p, P+l]`. With no edges, there are no prime implicants and `D := C` suffices. Otherwise one can minimize circuit size first. **The missing implication** is that among the least circuits there exists one with a bounded tree for every edge. Starting from such a circuit would meet the size bound for every input `C`. [Angle 1][a1] · [Angle 3][a3]

The choice of least circuit matters. Angle 4 gives a four-cycle-free graph with edges `(0,0), (0,1), (0,2), (1,0), (2,1)`. It reports Lean evaluations of two circuits of size 7 for that graph. In one, the only count vector for edge `(1,0)` is `[2,3]`, which fails read-2. The other is read-1. The minimum size of 7 comes from a separate exhaustive search. Angle 2 reports the same obstruction with the point labels permuted and checks both of its circuits on all 64 inputs. The example refutes the claim that *every* least circuit is read-2 while providing a witness for the requested existential statement on that graph. [Angle 4, example 2][a4] · [Angle 2, dead route][a2]

## Two routes identified by the results

| Route | What the results supply | Outstanding obligation |
| --- | --- | --- |
| Count the gates needed to cover the edges by stars | For a nonempty edge set `E`, choose a minimum vertex cover of size `t` and assign each edge to one of its covered endpoints. A center with `m` assigned edges uses `m−1` OR gates and one AND gate. Joining the stars gives a read-1 circuit of size `card(E) + t − 1`. | Prove that every circuit computing the function has at least that size under the four-cycle hypothesis. The cited `L_meta_4897` gives a cover bound under a read-1 hypothesis. To use the read-1 construction of `L_meta_7684` in Lean one also needs the read-1 to read-2 implication for the capped count vectors, or a direct read-2 check. [Angle 1][a1] · [Angle 2][a2] · [Angle 4][a4] |
| Prove the read bound in a selected least circuit | Angle 3 reports a scratch Lean reduction using `L_meta_4543`. It selects a least circuit in top form minimizing the number of edges in `Ustar`, the edges outside `starEdges`. Every prime implicant lands in one of those two sets. | For a star edge, lemma `N1` needs to carry the two unit reads through OR gates to the output. The argument is on paper. For an edge in `Ustar`, lemma `M` must supply a bounded tree in the selected circuit. Neither lemma has a submitted proof in the result. [Angle 3][a3] |

Both routes encounter AND gates inside a block. Angle 2 describes moving a wire whose truth implies the output function from an internal OR to a new output OR. It reports testing size and function preservation and a termination measure over 12086 moves on 60000 random circuits. The resulting form can still nest ANDs. Angle 3 observes that a three-leaf tree using both endpoints reads each at most twice. A four-leaf tree can already read `u,u,u,v`. Narrowing an operand to remove a repeated read can lose other edges. No result shows how to pay for those edges within the original gate budget or how to choose bounded trees for all of them. [Angle 2, C1–C3][a2] · [Angle 3, analysis of M][a3]

## Extent of the finite checks

| Source and method | Reported result |
| --- | --- |
| [Angle 1][a1], exact synthesis by SAT | The six-cycle has a circuit of size 8 and none of size 7. Adding one pendant edge gives size 9 and no circuit of size 8. On the eight-cycle at 10 gates the search returned no answer within 200 seconds. |
| [Angle 2][a2], enumeration up to graph isomorphism | For all 40 graphs examined with `P ≤ L`, `P + L ≤ 7`, no isolated vertex and no four-cycle, minimum size equalled the star-cover size. On 33 graphs it classified 2289 least circuits up to gate order and operand swap. Their smallest read bounds were 1 for 1983 circuits, 2 for 302 and 3 for 4. On the 21 graphs with `P + L ≤ 6`, all 535 least circuits became ORs of stars in at most two moves. |
| [Angle 4][a4], exhaustive circuit search | All 15 graphs examined attained the star-cover size. The spider example had 642 least circuits with smallest read bound 1, 828 with bound 2 and 20 with bound 3 under this enumeration. It treats each gate's inputs as unordered. Angle 2 also quotients by gate order, so its counts cannot be pooled with these. |

The finite searches support a least read-1 witness in the cases examined. A proof of L-meta-2584 could use the weaker conclusion that a least read-2 witness always exists. That universal implication is where the submitted evidence ends. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

## Pinned input records

| Result | SHA-256 of the supplied JSON |
| --- | --- |
| [item-angle-1][a1] | `8b406f17e89c8fb947692337607784aaad9598fbf3f546bc694ff01ae628114c` |
| [item-angle-2][a2] | `c39ed172b24e011f620757eabcefec99b3b77a3e5ab39e3ff3a66b6159e089f1` |
| [item-angle-3][a3] | `b2399d74adbd1f8bf059a7f97101ebddf7b7da6c2efbe117ee65536713d674c5` |
| [item-angle-4][a4] | `f699d09b0ec12d6c7ad8c9e542967d465eaeb5dfbd3d362753eeaeb5cebe1ef4` |

[a1]: ../items/angle-1/result.json
[a2]: ../items/angle-2/result.json
[a3]: ../items/angle-3/result.json
[a4]: ../items/angle-4/result.json
[pr]: https://github.com/open-goat/pequalnp-proofs/pull/12013
[lean]: https://raw.githubusercontent.com/open-goat/pequalnp-proofs/83d1576e60371dd69010f709c01fd70a178a8624/lean/PEqualNP/Outside/R_meta_2584_1.lean
