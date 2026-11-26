# L-meta-6166 proof goal

The goal remains unmet. The four results supply no Lean 4 proof or refutation of L-meta-6166. They contain no record of another holder checking a proof and no pull request from a proving contributor. The best construction they report has 64 gates, one over the 63-gate budget. The revision reproduced that count and the row tests. [A1–A4](#supplied-results)

| Required milestone | Evidence available |
| --- | --- |
| Lean 4 proof of L-meta-6166 | A4 reports that the statement elaborated with `sorry` and that a reduction elaborated with the statement assumed as a hypothesis. The results supply no proof term discharging it. [A4](#supplied-results) |
| Check on another holder’s machine | No check of a completed proof was found in the supplied records. The local reproduction below tests the 64-gate circuit in Python. [A1–A4](#supplied-results) |
| Subsequent contributor PR to `open-goat/pequalnp-proofs` | No matching PR was found in the supplied records or in public GitHub searches for `L-meta-6166` and `L_meta_6166`. The dash-form hits changed files for other steps, and the repository’s default branch did not have `lean/PEqualNP/Outside/L_meta_6166.lean` at the time of the check. [A1–A4](#supplied-results), [dash-form search](https://api.github.com/search/issues?q=repo%3Aopen-goat%2Fpequalnp-proofs+is%3Apr+%22L-meta-6166%22), [underscore-form search](https://api.github.com/search/issues?q=repo%3Aopen-goat%2Fpequalnp-proofs+is%3Apr+%22L_meta_6166%22), [file lookup](https://api.github.com/repos/open-goat/pequalnp-proofs/contents/lean/PEqualNP/Outside/L_meta_6166.lean) |

## What the statement requires

Points and lines are indexed modulo 13. Point `p` lies on line `l` when `p + l` belongs to the difference set `{0,1,3,9}`. This presents the incidence graph of the projective plane PG(2,3). The Boolean function takes 26 input bits and returns true when a selected point lies on a selected line. Its 52 minimal true inputs each select a single incident point–line pair. The negative list takes each set `S` of at most three vertices on one side and pairs it with every vertex on the other side that misses `S`, in both orientations. The results report 704 distinct negative inputs, all of them maximal false inputs. Together the lists give 756 distinct rows. Every true input contains a minimal true input and every false input is contained in a maximal false input, so agreement on these rows determines the entire monotone function. [A1–A4](#supplied-results), [boundary theorem L-meta-3771](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/L_meta_3771.lean)

The target, reproduced as the `search` premise of `R_meta_3773_627`, chooses a first gate from `AND[0,13]`, `OR[0,1]`, `OR[0,13]`, and `OR[2,13]`. Point bits have indices 0–12 and line bits have indices 13–25. The first gate’s value is appended to each row as bit 26. The target then asks for `FormulaSat (enc 27 62 g rows)` on those packed rows, with `g` true on the incident pairs. The 62 slots come after the first gate, for a maximum of 63 gates. A1–A3 inspected the encoding and found no way for extra source or operation selectors, row packing, the output selector, or unused TRUE padding to circumvent the gate budget. [A1–A3](#supplied-results), [search premise](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/R_meta_3773_627.lean#L15), [CNF definition](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Defs/LratEncoding.lean)

A4 reports that Lean 4.36.0 elaborated `R_meta_3773_627 h L_meta_6168` with `h` having the type of L-meta-6166. This verifies the implication from the target to a circuit of size at most 63. In the public reduction, the proof extracts satisfiability from `search` and passes it to `reconstruct`. A4’s separate elaboration of the target used `sorry`. A1 reports no Lean elaboration, and A2 and A3 report no target elaboration or proof file. [A1–A4](#supplied-results), [reduction](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/R_meta_3773_627.lean), [reconstruction theorem](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/L_meta_6168.lean)

## The 64-gate construction

For each line, OR the four point bits incident to it using three binary OR gates, then AND the result with the line bit. OR the 13 terms using 12 more gates. The total is `13 × (3 + 1) + 12 = 64`. Line 0 contains points 0 and 1, so its term can start with the permitted `OR[0,1]`. Counting that gate separately still leaves **63 residual gates for 62 slots**. A1 also reports the dual construction centered at points. [A1–A4](#supplied-results)

A star cover needs at least 13 centers because the pairs `(p, -p)` form a perfect matching. Combining `k` star terms whose leaf counts sum to at least 52 costs at least `52 + k − 1` gates in the direct star construction. Any two vertices on the same side share only one neighbor, so distinct stars cannot reuse an OR of two shared leaves. This gives a 64-gate minimum for the star construction. The public project also has restricted lower bounds, including the no-nested-AND case under `IsAO2`, the `andPairs = 0` case under its stated hypotheses, and results requiring `HasLineDegree … 1`. Those hypotheses leave more general circuits to be considered. [A1–A4](#supplied-results), [cover bound L-meta-5077](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/L_meta_5077.lean), [L-meta-4803](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/L_meta_4803.lean), [L-meta-5158](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/L_meta_5158.lean), [L-meta-5254](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/L_meta_5254.lean), [L-meta-2420](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/L_meta_2420.lean), [L-meta-1500](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/L_meta_1500.lean), [L-meta-2145](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/L_meta_2145.lean)

## Search evidence

- A1 and A4 tried hand factorizations including pencil sums, mixed point–line ORs and products of sums. They report no saving over the star construction or unwanted positive inputs. A2 likewise reports no successful sharing or filtering of nonincident pairs. [A1, A2, A4](#supplied-results)
- All three SAT experiment reports agree on the 6-cycle: 8 gates were satisfiable and 7 were unsatisfiable. A2 reports further below-star UNSAT instances for paths with 3, 5 and 6 edges, a five-edge double star, a three-leg spider, a hexagon with a pendant edge, and a three-point line with an outside point joined to two of its points. Its two examples containing a 4-cycle beat the star count. A3 reports matching upper and lower results on paths P4 and P6 and the three-leg spider. A3 also cites a separate, constrained UNSAT theorem for a Petersen fragment and reports a vertex cover of size 5 for that fragment. [A2–A4](#supplied-results), [constrained SAT theorem L-meta-4314](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/L_meta_4314.lean)
- A2 and A3 report timeouts at the below-star budget on the 8-cycle. A4 found an 11-gate circuit there, with 10 gates undecided after 500 seconds. A2 also reports timeouts on two 4-by-4 graphs and on a satisfiable control. A3 reports a timeout on the three-leg theta graph at 11 gates. A4’s 500-second runs on the 10-cycle, K4 point/edge incidence, the Fano plane, and a row subset of PG(2,3) were inconclusive. [A2–A4](#supplied-results)

The formal outcomes differ in label. A1 used `hypothesis_too_weak` and suggested a conditional normalization statement. A2 used `statement_seems_false` as a judgment. A3 used `missing_lemma` for the missing circuit witness. A4 used `other` and reported neither proof nor refutation. No item establishes whether the required circuit exists. [A1–A4](#supplied-results)

## Proof obligations still open

A direct proof could give a circuit within the 62 residual slots and a satisfying assignment for the exact CNF, with a Lean proof of clause satisfaction. A2 and A3 describe using a circuit in normal form to assign the operation, source and row-value variables. The public `L_meta_5341` gives a circuit-to-satisfiability argument for a different width and budget. A4 cites `LinkN.lean` as a possible completeness reference. Its public encoding also includes NOT gates, so reuse would require a link to the exact monotone encoding used here. A3 reports over five million clauses in `fSrcEq` alone and favors structural clause proofs. No item supplies the required witness or assignment. [A1–A4](#supplied-results), [L-meta-5341](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/L_meta_5341.lean), [LinkN](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Library/LRAT/LinkN.lean)

A1 proposes adding an existence hypothesis for a 63-gate circuit, then using symmetry, elimination of first gates that are false on the tested rows, and encoding completeness. That proposal changes the posted theorem by making its existential claim conditional. The analogous `L_meta_5807` relies on the impossible premise `¬ (0 < 26)`. A3 and A4 point to `R_meta_3773_1`, whose `findCore` hypothesis asks for a circuit of at most 58 gates on the 24-input core and two exposed OR signals on false inputs. The reduction also has an `insertInputs` hypothesis. Neither source supplies the core witness. A checked UNSAT certificate for all allowed first-gate choices would instead refute the posted statement. [A1, A3, A4](#supplied-results), [L-meta-5807](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/L_meta_5807.lean), [core reduction](https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/R_meta_3773_1.lean)

## Revision check

The prior report and its cited line numbers were unavailable in the revision checkout. The four source files were present and their SHA-256 hashes matched the brief. The Python check below reproduced the row counts by enumerating the point masks. For each mask it found all lines missing it and tested whether the pair was closed by applying the same operation back to the line mask. It then evaluated an explicit binary star circuit on every listed row. The result was 52 positive rows, 704 maximal false rows, first gate `OR[0,1]`, and 64 gates with 63 remaining. This reproduces A3 and A4’s count and the reviewer’s budget objection. The Lean evidence is A4’s reported conditional elaboration. [A3, A4](#supplied-results)

```python
from itertools import combinations

n = 13
full = (1 << n) - 1
offsets = {0, 1, 3, 9}
neighbors = [
    sum(1 << line for line in range(n) if (point + line) % n in offsets)
    for point in range(n)
]

def misses(mask):
    hit = 0
    for vertex, adjacent in enumerate(neighbors):
        if mask & (1 << vertex):
            hit |= adjacent
    return full ^ hit

positive = {
    (1 << point, 1 << line)
    for point, adjacent in enumerate(neighbors)
    for line in range(n)
    if adjacent & (1 << line)
}
small = [
    sum(1 << vertex for vertex in subset)
    for size in range(4)
    for subset in combinations(range(n), size)
]
negative = {(mask, misses(mask)) for mask in small}
negative |= {(lines, points) for points, lines in negative}
closed = set()
for points in range(full + 1):
    lines = misses(points)
    if misses(lines) == points:
        closed.add((points, lines))

assert negative == closed
assert positive.isdisjoint(negative)
assert (len(positive), len(negative)) == (52, 704)

gates = []

def gate(op, left, right):
    gates.append((op, left, right))
    return 2 * n + len(gates) - 1

def disjunction(wires):
    result, *remaining = wires
    for wire in remaining:
        result = gate("OR", result, wire)
    return result

terms = []
for line in range(n):
    pencil = [p for p in range(n) if neighbors[p] & (1 << line)]
    terms.append(gate("AND", n + line, disjunction(pencil)))
output = disjunction(terms)

def evaluate(points, lines):
    wires = [(mask >> i) & 1 for mask in (points, lines) for i in range(n)]
    for op, left, right in gates:
        a, b = wires[left], wires[right]
        wires.append((a & b) if op == "AND" else (a | b))
    return wires[output]

assert gates[0] == ("OR", 0, 1)
assert len(gates) == 64 and len(gates) - 1 == 63 > 62
assert all(evaluate(*row) for row in positive)
assert all(not evaluate(*row) for row in negative)
```

## Supplied results

These identifiers refer to the JSON records under `.imd/reads/artifacts/`. The report preserves their findings and the evidentiary limits of their checks.

| Source | Record | SHA-256 |
| --- | --- | --- |
| A1 | `item-angle-1` | `035d2d1353afaed88160cd3d547a953f03f840a10780f298217a7d391dc3a9cd` |
| A2 | `item-angle-2` | `2073cd8f5a79cb0634addc1421e831a9f0856a8fb4ef5166266fa295ecf7cbe7` |
| A3 | `item-angle-3` | `3b6cbe6dc40108a96703e1f913ba9b03bee26480924f5119729180e64dc027d2` |
| A4 | `item-angle-4` | `23b1cf390f7419986f5d3c7b8025861ca162a76055549d2d73ec2bd5cbe36bcd` |
