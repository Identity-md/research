# L-meta-4087 remains open in the four submitted results

The requested Lean 4 theorem requires a circuit of **at most 18 gates**. The four workers supply one explicit **19-gate** construction and no proof that 18 gates suffice or are impossible. None of the four records contains an elaborated theorem, a successful check of that theorem on another holder’s machine, or a URL for a pull request opened by the proving contributor on `open-goat/pequalnp-proofs`. This status describes the submitted evidence. [1][worker-1] · [2][worker-2] · [3][worker-3] · [4][worker-4]

## The condition a witness must satisfy

Points and lines each have labels 0 through 12. Point `p` lies on line `l` when `(p − l) mod 13` belongs to `{0,1,3,9}`. A witness chooses nine entries, each centred at a point or a line, and a binary AND/OR circuit. The first 26 inputs encode the point set `P` and line set `L`. Each entry chooses a pairing of its four neighbours and supplies three helper bits, the OR of each pair and the OR of all four. The neighbours of a line centre are point bits and the neighbours of a point centre are line bits. For entry `j = 0,…,8`, the three-bit block starts at `26 + max(5j − 1, 0)`. The other 17 of the 70 inputs are unconstrained. [1][worker-1] · [3][worker-3] · [4][worker-4]

| Required output | Inputs imposing that output |
|---|---|
| True | `P = {p}` and `L = {l}` form an incident pair, and neither endpoint is a selected centre of its respective type. |
| False | No point of `P` lies on any line of `L`, every line contains at most two points of `P`, and every point lies on at most two lines of `L`. |

Both obligations apply for every assignment consistent with the helper bits. For the unconstrained bits, monotonicity makes all-false the hardest assignment to accept and all-true the hardest to reject. The construction below reads only the point and line bits. [1][worker-1] · [4][worker-4]

## The witness that fits 19 gates

Choose the entries `(true, j, 0)` for lines `j = 0,…,8`. For each remaining line, OR the first two point bits in its row, OR the last two, OR those two results, then AND with the line bit. OR the four row outputs with three more gates. The count is `4 × (3 OR + 1 AND) + 3 OR = 19`. The point labels below follow by adding `0,1,3,9` to the line label modulo 13. [2][worker-2] · [4][worker-4]

| Line | First pair | Second pair |
|---:|---:|---:|
| 9 | 9, 10 | 12, 5 |
| 10 | 10, 11 | 0, 6 |
| 11 | 11, 12 | 1, 7 |
| 12 | 12, 0 | 2, 8 |

A required singleton incidence makes its row true. Every true row identifies a selected line and a selected point on it, which rules out every required-false input. Worker 4 also evaluated the construction on all 16 required singleton incidences and all 12,234 required-false configurations. The following Python check reconstructs the gates and both sets of tests directly from the incidence rule. Its gate-count assertion makes the one-gate gap explicit. [1][worker-1] · [4][worker-4]

```python
D = (0, 1, 3, 9)
labels = range(13)
remaining = range(9, 13)
points_on = [sum(1 << ((l + d) % 13) for d in D) for l in labels]
lines_at = [sum(1 << ((p - d) % 13) for d in D) for p in labels]
gates = []

def gate(op, a, b):
    gates.append((op, a, b))
    return 70 + len(gates) - 1

rows = []
for l in remaining:
    a, b, c, d = [(l + offset) % 13 for offset in D]
    points = gate("or", gate("or", a, b), gate("or", c, d))
    rows.append(gate("and", 13 + l, points))
output = gate("or", gate("or", rows[0], rows[1]), gate("or", rows[2], rows[3]))

def evaluate(P, L):
    raw = P | (L << 13)
    wires = [(raw >> i) & 1 for i in range(26)] + [None] * 44
    for op, a, b in gates:
        x, y = wires[a], wires[b]
        wires.append((x | y) if op == "or" else (x & y))
    return wires[output]

def admissible(neighbourhoods):
    return [s for s in range(1 << 13)
            if all((s & n).bit_count() <= 2 for n in neighbourhoods)]

assert len(gates) == 19
yes = [(1 << p, 1 << l) for l in remaining for p in labels
       if (p - l) % 13 in D]
assert len(yes) == 16 and all(evaluate(P, L) == 1 for P, L in yes)
point_sets, line_sets = admissible(points_on), admissible(lines_at)
assert len(point_sets) == len(line_sets) == 560
rejected = 0
for P in point_sets:
    incident_lines = sum(1 << l for l in labels if P & points_on[l])
    for L in line_sets:
        if (L & incident_lines) == 0:
            assert evaluate(P, L) == 0
            rejected += 1
assert rejected == 12234
```

## What the searches settle

There are 52 incidences, and each of the nine centres can excuse at most four. At least 16 singleton pairs therefore need acceptance, even with repeated centres. Workers 1 and 3 report the following minima over distinct centres. Each count is the number of singleton inputs the circuit must accept. [1][worker-1] · [3][worker-3] · [4][worker-4]

| Number of line centres (other centres are points) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Minimum required pairs | 16 | 16 | 17 | 18 | 18 | 18 | 18 | 17 | 16 | 16 |

With gadget centres on lines 0–8, workers 2 and 3 report exact synthesis for smaller acceptance obligations. Line 9 alone took four gates, with three ruled out. Lines 9 and 10 took nine gates, with eight ruled out. Worker 2 used a restriction to the points on those two lines for the eight-gate exclusion. Worker 3 tested against 468 maximal required-false configurations and also excluded eight gates for lines 9 and 12. These results apply to the specified centres and target lines. [2][worker-2] · [3][worker-3]

The 18-gate searches targeting all required pairs timed out for the layouts tried. Worker 1 tried several point-centred layouts and a mixed layout with a 400-second limit. Worker 2 reports unfinished three- and four-line searches at 230 seconds each. Worker 3 reports nine-minute runs, and worker 4 also reports an unfinished search. Workers 1, 3 and 4 each had a control run that failed to find a known 19-gate solution within its limit. A timeout provides no lower bound. [1][worker-1] · [2][worker-2] · [3][worker-3] · [4][worker-4]

Two workers returned `statement_seems_false` (2 and 3), one returned `other` (1), and one returned `out_of_time` (4). The obstacle to a lower bound is specific. Two distinct lines meet in one point, so a helper pair on an excluded line cannot supply two neighbours of a remaining line. This explains why direct substitution fails. Counting each line’s OR gates separately would also require showing that a gate cannot serve multiple lines after later AND gates filter out unwanted pairs. The workers did not establish that claim. [1][worker-1] · [2][worker-2] · [3][worker-3] · [4][worker-4]

Workers 2–4 identify a conditional route in `PEqualNP/Outside/R_meta_4087_218.lean`. For centres on lines 0–8 it requires a circuit of at most 13 gates for lines 9–11 and a five-gate extension for line 12. The direct three-row construction costs `3 × 4 + 2 = 14`. The cited reduction assumes the smaller circuit, and the reported searches left its existence open. No supplied result discharges both hypotheses or provides a different witness meeting the original bound. [2][worker-2] · [3][worker-3] · [4][worker-4]

## Sources

Each number identifies one supplied worker record by its item path and SHA-256 digest.

| No. | Result | SHA-256 |
|---:|---|---|
| 1 | [item-angle-1](../items/angle-1/result.json) | `9aa4c6ba9b92ac73fc8183e90057c85c67b77f7850d5c423a73d1f4a9c21d7a6` |
| 2 | [item-angle-2](../items/angle-2/result.json) | `c0830bbf72df02420d499b1c89f4e021708c5016126b1b46c0c2f6ab10491fb1` |
| 3 | [item-angle-3](../items/angle-3/result.json) | `c501d3869879cbd45225679a9bab83f86fdb6f0d07d9ab58d88bb06e493159de` |
| 4 | [item-angle-4](../items/angle-4/result.json) | `3657e6d27cb71fa9ee6d57cfe41e6327e8b4da0832931fcadebde35d09df593c` |

[worker-1]: ../items/angle-1/result.json

[worker-2]: ../items/angle-2/result.json

[worker-3]: ../items/angle-3/result.json

[worker-4]: ../items/angle-4/result.json
