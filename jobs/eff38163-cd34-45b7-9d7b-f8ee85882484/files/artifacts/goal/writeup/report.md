# L-meta-7368 — proof status and circuit evidence

**L-meta-7368 remains open in the four submitted results.** The requested theorem needs a circuit of at most 58 gates with both reserve wires. The explicit 58-gate circuit supplies only the first reserve. The explicit circuit with both reserves uses 60 gates. None of the results contains Lean source proving the original statement, a record of another holder checking such source, or a contributor-authored pull-request URL for `open-goat/pequalnp-proofs`. Three results record `statement_seems_false` and Angle 2 records `other`. All four leave open the existence of a different 58-gate circuit. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

## What the witness must compute

Point inputs 0 through 11 represent the elements of ℤ/13ℤ other than 9, in ascending order. Line inputs 12 through 23 represent line labels 1 through 12. Point label `p` and line label `l` are incident when `(p + l) mod 13` belongs to `{0, 1, 3, 9}`. The output `F` is true exactly when some incident point and line are both selected. The witness must be a monotone fan-in-two circuit starting with `OR(0, 1)`. On **every** assignment where `F` is false, designated wires must equal `P = x₀ ∨ x₁ ∨ x₃` and `Q = x₁₅ ∨ x₁₆ ∨ x₁₈`, respectively. [Angle 1][a1] · [Angle 3][a3] · [Angle 4][a4]

## Gate counts and the missing wire

For each line, OR its incident point inputs and AND that sum with the line input. OR the twelve products. Three lines have degree three and nine have degree four, for 45 incidences. The point sums cost 33 ORs, the products cost 12 ANDs, and combining the products costs 11 ORs. This accounts for all 56 gates of the incidence calculation. Centering the products on points gives the same count. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3]

| Line-centred construction, in gate order | Gates | First gate | Wires agreeing with P wherever F is false | Wires agreeing with Q wherever F is false |
|---|---:|---|---|---|
| Incidence calculation alone | 56 | OR(0, 2) | None | None |
| Prepend OR(0, 1) and OR(24, 3) | 58 | OR(0, 1) | 25 | None |
| Prepend OR(0, 1), OR(24, 3), OR(15, 16) and OR(26, 18) | 60 | OR(0, 1) | 25 | 27 |

Inputs occupy wires 0 through 23. Gate `k`, counted from zero, produces wire `24 + k`. The table uses Angle 3's ascending line and point order, folding each product into the output as it is built. The exhaustive check below reproduces the table and Angle 2's count of **20,978 false assignments**. [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

Three assignments suffice to see the defect in the 58-gate candidate. Turn on just line input 15, just 16, or just 18. Each time, all points are off, so `F = 0` and `Q = 1`. Every gate of this candidate is false on all three assignments, including the two gates for P. Each input wire is true on at most one of the three. Hence no choice of wire index can supply Q in this circuit. [Angle 3][a3] · [Angle 4][a4]

Angle 3 reports that its Lean proof of the **60-gate variant** elaborated without `sorry`, with axioms `propext`, `Classical.choice`, and `Quot.sound`. Restoring 58 in the same file made the size obligation fail. This is the worker's account of a local Lean run. The supplied result contains the gate specification and proof notes, with no attached Lean file or second-holder attestation. [Angle 3][a3]

## How far the obstruction goes

The incidence graph has no 4-cycle. A product of a sum of points and a sum of lines can therefore cover only a star if every pair it generates must be incident. The star centres cover the edges, and a matching of size 12 forces at least 12 centres. In the star-cover calculation the cost is at least 45 incidences plus 12 stars minus one, or 56 gates. No remaining line contains two of the three P points, and no remaining point lies on two of the three Q lines. The usual sums for those stars therefore share no two-input OR with the reserve sums. The workers' counting argument gives 60 for this restricted construction. [Angle 1][a1] · [Angle 2][a2] · [Angle 4][a4]

The unrestricted theorem allows nested ANDs. It also constrains each reserve only on false outputs. For example, monotonicity and the three singleton point assignments force a candidate P wire `w` to satisfy `P ≤ w` everywhere. Agreement on false outputs gives `w ≤ P ∨ F`. The same reasoning applies to Q. The counts above do not exclude a circuit that uses this freedom. Angle 3's searches on a six-cycle and a six-vertex path, and Angle 4's searches on disjoint pairs and a six-cycle, concern smaller graphs. None establishes the lower bound of 59 needed to refute this step. [Angle 1][a1] · [Angle 3][a3] · [Angle 4][a4]

The two-gate gap also matters downstream. Angle 2 describes a five-gate extension restoring deleted point 9 and line 0. With reserve wires `wP` and `wQ`, its output is `F ∨ (line₀ ∧ wP) ∨ (point₉ ∧ (line₀ ∨ wQ))`. When F is false the reserves enumerate the missing incidences, including the deleted point–line pair. When F is true the extension is already true. A witness meeting 58 would thus give at most 63 gates for the full plane. The workers cite a 64-gate lower bound in `L_meta_4803` under the hypothesis that no AND feeds another AND, even indirectly. The additional lemmas cited by Angle 1 also have structural or minimality hypotheses. These results leave the general nested case unresolved. [Angle 1][a1] · [Angle 2][a2]

## Reproducing the circuit comparison

This check runs with Python 3.10 or later. For each point mask it evaluates all line masks in parallel. It compares the output with the incidence definition, then tests **every** input and gate wire for reserve agreement on false assignments. It covers all `2^24` inputs for each listed circuit. [Incidence definition and false-input count][a2] · [Gate order][a3] · [Three constructions][a4]

```python
from functools import reduce
from operator import or_

points = [p for p in range(13) if p != 9]
rows = [[i for i, p in enumerate(points) if (p + line) % 13 in {0, 1, 3, 9}]
        for line in range(1, 13)]

def build(prefix):
    gates = list(prefix)
    def add(op, a, b):
        gates.append((op, a, b))
        return 23 + len(gates)

    out = None
    for line, row in enumerate(rows, 12):
        point_sum = row[0]
        for point in row[1:]:
            point_sum = add("or", point_sum, point)
        product = add("and", point_sum, line)
        out = product if out is None else add("or", out, product)
    return gates, out

reserve_gates = [("or", 0, 1), ("or", 24, 3), ("or", 15, 16), ("or", 26, 18)]
mask_count = 1 << 12
ones = (1 << mask_count) - 1
line_bits = [sum(1 << m for m in range(mask_count) if (m >> l) & 1)
             for l in range(12)]

for prefix_size, expected_p, expected_q in [(0, [], []), (2, [25], []), (4, [25], [27])]:
    gates, output = build(reserve_gates[:prefix_size])
    candidates = [set(range(24 + len(gates))) for _ in range(2)]
    false_count = 0
    for m in range(mask_count):
        wires = [ones if (m >> p) & 1 else 0 for p in range(12)] + line_bits
        expected = reduce(or_, (line_bits[l] for l, row in enumerate(rows)
                                if any((m >> p) & 1 for p in row)), 0)
        for op, a, b in gates:
            wires.append((wires[a] | wires[b]) if op == "or" else (wires[a] & wires[b]))
        assert wires[output] == expected
        off = ones ^ expected
        false_count += off.bit_count()
        for k, indices in enumerate([(0, 1, 3), (15, 16, 18)]):
            reserve = reduce(or_, (wires[i] for i in indices))
            candidates[k] = {i for i in candidates[k] if ((wires[i] ^ reserve) & off) == 0}
    assert false_count == 20978
    assert len(gates) == 56 + prefix_size
    assert [sorted(c) for c in candidates] == [expected_p, expected_q]
    print(len(gates), output, expected_p, expected_q, false_count)
```

[a1]: ../items/angle-1/result.json
[a2]: ../items/angle-2/result.json
[a3]: ../items/angle-3/result.json
[a4]: ../items/angle-4/result.json
