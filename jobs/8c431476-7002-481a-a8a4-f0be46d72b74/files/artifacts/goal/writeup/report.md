# L-meta-3773 — proof status

**The four results leave L-meta-3773 unresolved.** Their complete circuit passes every required evaluation and uses 64 gates. The theorem requires at most 63. Angle 1 elaborated the statement against `PEqualNP.Defs` using a placeholder proof body. None of the four results supplies a completed Lean 4 theorem, a check of that theorem on another holder’s machine, or a contributor-authored pull request submitting the proof to `open-goat/pequalnp-proofs`. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

## What the circuit must compute

Number the point wires 0 through 12 and the line wires 13 through 25. Point `p` lies on line `l` when `(p + l) mod 13` belongs to `{0, 1, 3, 9}`. The circuit must use AND and OR gates of fan-in at most two. Its first gate must be one of `AND [0,13]`, `OR [0,1]`, `OR [0,13]`, or `OR [2,13]`. [Angle 1][a1] · [Target statement in the Lean reduction][rows]

Each of the 52 incident pairs must be accepted with just its two wires set. For each set `S` of at most three indices, let `off(S)` be all indices incident to none of `S` on the opposite side. Both inputs `(S, off(S))` and `(off(S), S)` must be rejected. There are `1 + 13 + 78 + 286 = 378` choices of `S`, giving 756 listed rejection tests and **704 distinct rejecting inputs**. The check below removes duplicates only after generating both orientations. [Angle 1][a1] · [Angle 2][a2] · [Angle 4][a4] · [Row definition][rows]

These tests determine the answer on all inputs. An input containing an incidence contains an accepting pair. On an incidence-free input, at least one selected side has size at most three by L-meta-3771. Taking that side as `S` places the input inside the corresponding rejecting input. Monotonicity forces the output in both cases. Thus the circuit must compute the OR, over all incidences, of `point[p] AND line[l]`. [L-meta-3771][geometry] · [Angle 1][a1] · [Angle 3][a3]

## The one-gate gap

For each line, OR its four points using three gates, then AND the result with the line wire. Join the thirteen star outputs with twelve OR gates. Line 0 contains points 0, 1, 3 and 9, so the first gate can be `OR [0,1]`. A star fires exactly when its line and at least one incident point are selected. This gives the correct function with **13 × (3 + 1) + 12 = 64 gates**. Angles 2 and 3 evaluated this construction in Python. [Angle 2][a2] · [Angle 3][a3]

Reassigning the 52 edges to a partition of stars cannot save the gate. A star with `d` edges costs `d − 1` leaf ORs and one AND. Joining `k` stars costs another `k − 1`. Their centres must cover the 13 disjoint edges `(p, −p)`, hence `k ≥ 13`. Angle 2 found that an incidence-free set meeting both sides has at most 10 vertices. Taking complements gives a cover size of at least 16 **when the cover omits a vertex on each side**. The only covers of size 13 are all points or all lines. [Angle 2][a2] · [Angle 4][a4]

There are stronger results for circuits satisfying the project’s `ReadsBack 26` wiring hypothesis. L-meta-1751 gives a lower bound of 64 under its correctness tests when no AND lies in the input cone of another AND. L-meta-8141 shows that a correct circuit of size at most 63 must have an internal AND that fires on a pair rejected by the edge function. Those lemmas use `p − l` for incidence, which becomes `p + l` on renaming each line by its negative. R-meta-6140-102 still takes lower bounds for minimal circuits with such an AND on specified pairs as hypotheses. The unrestricted lower bound remains unproved in the four results. [Angle 2][a2] · [L-meta-1751][level] · [L-meta-8141][pair] · [R-meta-6140-102][lower]

## What the searches established

| Instance | Reported solver outcome | Source |
| --- | --- | --- |
| Full plane, 63 gates, allowed first gate | Seven runs in Angle 1 were undecided. Its unrestricted search also missed the known 64-gate circuit. Angles 2 and 4 did not run the full instance. | [Angle 1][a1] · [Angle 2][a2] · [Angle 4][a4] |
| Twelve fixed point stars and their fixed OR chain | The prefix uses 59 gates. With that wiring frozen, four free gates gave UNSAT and five gave SAT. The solver conclusion applies to the encoded layout. | [Angle 1][a1] |
| More of the plane left free | With two stars left free, ten free gates gave SAT and nine were undecided. Runs with three or four stars free, with the joining chain free, and with all thirteen line sums fixed and 24 gates free were also undecided. | [Angle 1][a1] · [Angle 3][a3] |
| Smaller cycles | For the 6-cycle, seven gates gave UNSAT and eight gave SAT. For the 8-cycle, Angle 1 left ten gates undecided, while Angles 3 and 4 reported UNSAT at ten and SAT at eleven. For the 10-cycle, thirteen remained undecided and Angle 3 reported SAT at fourteen. | [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4] |
| Other small graphs | Angle 3 reports UNSAT one gate below the star count on paths of six through eight vertices, a three-legged spider, a double star, two point stars sharing a leaf, and a 6-cycle with one or two pendant edges. | [Angle 3][a3] · [Angle 4][a4] |
| Fano plane | For three collinear points at ten gates, Angle 3 left cases undecided. Angle 4 reported UNSAT at ten and SAT at eleven for both collinear and non-collinear triples. Its UNSAT runs for the triples and the 8-cycle used one solver and a gate-ordering restriction whose soundness the author did not prove. The full Fano plane remained undecided at 26 gates, and searches missed its known 27-gate circuit. | [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4] |

SAT and UNSAT in the table are solver reports for the indicated instances. None of the items supplies a Lean certificate of non-existence for the target. Angles 1–3 returned `other`. Angles 2 and 3 suspected the witness might not exist, and Angle 4 returned `statement_seems_false` while explicitly leaving the general case open. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

### Why the ordering of a star matters to the search

Take the twelve line stars with centres 0 through 11, OR each line’s points in increasing order, then join the star outputs in order. Wires 26, 27 and 28 in the first star successively compute `p0 ∨ p1`, `w26 ∨ p3` and `w27 ∨ p9`. Change just the last two to `p3 ∨ p9` and `w26 ∨ w27`. Both prefixes start with the allowed first gate, use 59 gates, and agree at their outputs on all 52 accepting and 704 distinct rejecting rows. Both miss the four incidences on line 12. **None of the 85 original wires** has the new wire 27’s column of values. A suffix may read that column. The row check below reproduces the reviewer’s example from the incidence rule. [Angle 1, fixed-prefix search][a1] · [Row definition][rows]

### A counting argument for arbitrary groupings of those twelve stars

For this specific family, there is a separate hand proof that five suffix gates are necessary. Fix twelve complete line stars built from their own incident point inputs and join their outputs with ORs. Allow any grouping within the stars and in the join, and let the suffix read **any** input or prefix wire. The argument uses the incidence function above and the fact that two distinct lines meet in exactly one point. [Angle 1, prefix construction][a1] · [Angle 2, incidence geometry][a2]

1. Let `m` be the omitted line. Set the other line inputs and all points outside `m` to false. The required output now depends on five independent bits, namely the bit for `m` and the four points on it. Every available wire restricts to zero or to a single one of those bits. In particular, an OR within a covered star sees at most one surviving point. Every covered line bit, star output and OR of star outputs vanishes.
2. In the dependency graph leading to one output, `g` suffix gates of fan-in at most two can read at most `g + 1` distinct external wires. With `b` external wires this connected graph has at least `g + b − 1` edges and at most `2g`. Thus four gates have room for at most five external wires.
3. All five would have to carry different surviving bits. Before restriction, each wire that survives is either the omitted line bit or a function of point inputs alone. The suffix could therefore never respond to a covered line bit, even on an unrestricted input. Selecting one incident point and toggling its covered line, with every other line false, requires the output to change. This rules out a four-gate suffix.

Five gates suffice by forming the omitted four-point OR, gating it with its line and ORing it into the prefix output. Exchanging points and lines gives the same conclusion for point stars. This argument allows regrouping and intermediate-wire access throughout the specified prefix family. Circuits that build a different prefix remain candidates for L-meta-3773. [Angle 1][a1] · [Angle 3][a3]

## What the public reductions supply

R-meta-3773-791 reduces the theorem to a gate list of length at most 63 with a permitted head and the correct bit-packed output, together with a transfer hypothesis relating list evaluation to Lean circuit evaluation. Public PR #12068 concerns that reduction. The search hypothesis still asks for the missing gate list. Another reduction, R-meta-3773-1, would use a 24-input core of at most 58 gates after deleting point 9 and line 0, two specified reserve wires and a five-gate suffix. Angle 1’s direct star core costs 56 gates plus four to construct the two reserves. Neither route yielded a witness in the handoff. [Angle 1][a1] · [Angle 3][a3] · [Bit-parallel reduction][rows] · [Reduction PR #12068](https://github.com/open-goat/pequalnp-proofs/pull/12068) · [Core reduction][core]

## Reproducing the construction and the wire comparison

This Python check builds the two prefixes gate by gate. One bit of a wire’s integer value represents one test row. It also evaluates the full 64-gate construction and checks the first gate and size separately. Its inputs are the incidence rule, star construction and row families above. [Angle 2][a2] · [Angle 3][a3] · [Row definition][rows]

```python
from itertools import combinations

indices = range(13)
offsets = {0, 1, 3, 9}
points = [tuple(p for p in indices if (p + l) % 13 in offsets) for l in indices]
accept = [(1 << p) | (1 << (13 + l)) for l in indices for p in points[l]]
reject = []
for size in range(4):
    for side in combinations(indices, size):
        selected = sum(1 << i for i in side)
        opposite = sum(1 << l for l in indices if set(side).isdisjoint(points[l]))
        reject.extend([selected | (opposite << 13), opposite | (selected << 13)])

rows = accept + sorted(set(reject))
assert (len(accept), len(reject), len(set(reject))) == (52, 756, 704)
assert len(rows) == len(set(rows))

def stars(centres):
    gates, heads = [], []

    def gate(op, a, b):
        wire = 26 + len(gates)
        gates.append((op, a, b))
        return wire

    for l in centres:
        a, *rest = points[l]
        for b in rest:
            a = gate("or", a, b)
        heads.append(gate("and", a, 13 + l))
    output = heads[0]
    for head in heads[1:]:
        output = gate("or", output, head)
    return gates

def columns(gates):
    wires = [sum(((r >> i) & 1) << j for j, r in enumerate(rows)) for i in range(26)]
    for op, a, b in gates:
        assert op in {"and", "or"} and 0 <= a < len(wires) and 0 <= b < len(wires)
        wires.append(wires[a] & wires[b] if op == "and" else wires[a] | wires[b])
    return wires

full = stars(indices)
assert full[0] == ("or", 0, 1) and len(full) == 64
assert columns(full)[-1] == (1 << len(accept)) - 1

original = stars(range(12))
regrouped = original.copy()
regrouped[1:3] = [("or", 3, 9), ("or", 26, 27)]
before, after = columns(original), columns(regrouped)
assert original[0] == regrouped[0] == ("or", 0, 1)
assert len(original) == len(regrouped) == 59 and len(before) == 85
assert before[-1] == after[-1] and after[27] not in before
```

## Supplied result records

| Source | SHA-256 of the supplied JSON |
| --- | --- |
| [Angle 1][a1] | `960a4149d20348f7b7d8034fe7c95299e0ae739e90992c07139831472a8a752a` |
| [Angle 2][a2] | `89e8a525e96acd8a839b9f0d59f08c730574bfd8d20af9805dfbb2dc8db90e3c` |
| [Angle 3][a3] | `6aed3d4f49cba166d45cae6f81dafccf48bc19608e3dfce616e392054a2b73be` |
| [Angle 4][a4] | `cd5d149f0155269b134f9d65c13fbb547d852790d70efcfd319746152eef24cf` |

[a1]: ../items/angle-1/result.json
[a2]: ../items/angle-2/result.json
[a3]: ../items/angle-3/result.json
[a4]: ../items/angle-4/result.json
[geometry]: https://github.com/open-goat/pequalnp-proofs/blob/7c39871d38bf01918abd73c4d5ae36c424d30d78/lean/PEqualNP/Outside/L_meta_3771.lean
[rows]: https://github.com/open-goat/pequalnp-proofs/blob/7c39871d38bf01918abd73c4d5ae36c424d30d78/lean/PEqualNP/Outside/R_meta_3773_791.lean
[level]: https://github.com/open-goat/pequalnp-proofs/blob/7c39871d38bf01918abd73c4d5ae36c424d30d78/lean/PEqualNP/Outside/L_meta_1751.lean
[pair]: https://github.com/open-goat/pequalnp-proofs/blob/7c39871d38bf01918abd73c4d5ae36c424d30d78/lean/PEqualNP/Outside/L_meta_8141.lean
[lower]: https://github.com/open-goat/pequalnp-proofs/blob/7c39871d38bf01918abd73c4d5ae36c424d30d78/lean/PEqualNP/Outside/R_meta_6140_102.lean
[core]: https://github.com/open-goat/pequalnp-proofs/blob/7c39871d38bf01918abd73c4d5ae36c424d30d78/lean/PEqualNP/Outside/R_meta_3773_1.lean
