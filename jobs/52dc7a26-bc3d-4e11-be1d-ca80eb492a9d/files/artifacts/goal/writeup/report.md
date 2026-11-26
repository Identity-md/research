# Outside proof desk · L-meta-4817

**The four results leave L-meta-4817 unproved.** Each records `missing_lemma`. They supply a Lean-checked reduction and gate-count bounds. None supplies an unconditional Lean theorem, a second holder's check of that theorem, or a contributor-authored pull request carrying it. A continuation with 17 AND/OR gates and no NOT gates meets every counting bound below. Whether such a continuation computes the target is still the question. [Result 1][r1] · [Result 2][r2] · [Result 3][r3] · [Result 4][r4]

## The exact claim

Let `PET x` be true when the vertices selected by the ten Boolean inputs `x` contain an edge of the Petersen graph. The desk lists 15 edges. For each circuit `C` and index `k : Fin 12`, supply `C` with the list

```lean
let w := List.ofFn x ++ [x 0 && x 2]
w ++ [!w.getD k.val false]
```

Wire 10 carries the AND of two nonadjacent vertices. Wire 11 complements a primary input for `k < 10`, complements wire 10 for `k = 10`, and is true for `k = 11` because the lookup then defaults to false. The claim is that for **every** fan-in-two AND/OR/NOT circuit `C` of size at most 17 and **every** such `k`, some `x` makes its output differ from `PET x`. Size counts entries in `C.gates`. The two supplied wires are already present when the first entry executes. [Desk statement][reduction] · [FanInTwo and HasCircuitSize][meta] · [Circuit evaluation and size][circuit]

## What the Lean checks establish

Suppose a particular `C, k` agrees with PET on every input. Start on the ten primary inputs, prepend `AND[0,2]` and `NOT[k]` to the gate list of `C`, and keep its output index. Call this circuit `D`. Its first two gates produce exactly wires 10 and 11, including the default-read case. Every subsequent gate therefore sees the same wires as in `C`. The encoding theorem proves that `D` is a fan-in-two realization of PET with at most `17 + 2 = 19` gates. [L_meta_8079][encode] · [Result 2][r2]

Consequently, given `fullLower : ¬ HasCircuitSize 10 PET 19`, the Lean proof term for the step is `PEqualNP.Outside.R_meta_4817_1 fullLower PEqualNP.Outside.L_meta_8079`. The reduction takes two premises. The encoder discharges the second. The proof uses the first when it applies `fullLower` to the constructed circuit. Results 2–4 report checking this implication in Lean 4.36 with the encoding argument inlined. A lower bound just for circuits starting with those two gates would also suffice. [R_meta_4817_1][reduction] · [L_meta_8079][encode] · [Result 2][r2] · [Result 3][r3] · [Result 4][r4]

Write `s = C.size` and let `n` count its NOT gates. Then `D` has size `s + 2`, with `n + 1` NOT gates and `s − n + 1` AND/OR gates. The following deductions assume agreement with PET on every input.

| Published bound on `D` | Consequence for `C` | Evidence |
| --- | --- | --- |
| `15 + notCount D ≤ D.size` | `s − n ≥ 14`. Result 4 checked the desk statement with budget 13. | [L_meta_4725][lower15] · [Result 4][r4] |
| At least 16 gates of `D` have operation AND or OR | `s − n ≥ 15`. This rules out every `s ≤ 14` and permits at most two NOT gates when `s ≤ 17`. | [L_meta_6581][lower16] · [Result 1][r1] · [Result 3][r3] |

**A paper deduction narrows the remaining cases to three.** Set `x 0 = false`. Wire 10 becomes false, and wire 11 becomes a constant or a complemented primary input. In the signed circuit model, which allows constants and complements for free, the remaining nine-input function still needs 15 binary operations. This is the `nineFloor` certificate used in `L_meta_6581`. Its projection to the first 512 truth-table rows fixes vertex 0 to false. [Signed model and nine-input certificate][nine]

At least one binary operation of the continuation can be removed on this restriction. To see why, compare the selected vertex sets `{1}` and `{0,1}`. PET changes because 01 is an edge. Wire 0 changes, as does wire 11 when `k = 0`. Every other input to the continuation stays fixed on this pair. Follow a changing wire back from the output, treating NOTs as free signs and unary gates as copies or complements. If no binary gate changed, the output would have to be a literal of vertex 0. PET also changes between `{0}` and `{0,1}`, which rules out that possibility. At the earliest changing binary gate, a changing operand must therefore be a literal of vertex 0. Fixing that vertex to false makes the operand constant, so this AND/OR simplifies to a constant or a copy. At most `s − n − 1` binary operations remain. The certificate gives `15 ≤ s − n − 1`. This application to the supplied wires is a paper argument. [Edge list][reduction] · [Gate semantics][circuit] · [Signed lower bound][nine]

With `s ≤ 17`, the resulting inequality `s − n ≥ 16` permits exactly `(s,n) = (16,0), (17,0), (17,1)`. Even in the zero-NOT cases the continuation receives wire 11. For example, `(17,0)` gives 17 AND/OR gates in `C` and 18 in `D`. Both the checked and the paper inequalities hold. None of the four results excludes agreement with PET throughout these cases. [L_meta_6581][lower16] · [Result 1][r1] · [Result 2][r2] · [Result 3][r3] · [Result 4][r4]

## What the 20-gate example shows

Result 4 gives a construction over the vertex cover `{0,2,3,5,6,9}`. Assign each PET edge once to an endpoint in the cover. The table gives one such assignment. Each row computes the AND of its center with the OR of its assigned neighbors. The OR of the six rows then computes PET. [Result 4][r4] · [Desk edge list][reduction]

| Center | Assigned neighbors | Gates in row |
| --- | --- | ---: |
| 0 | 1, 4, 5 | 3 |
| 2 | 1, 3, 7 | 3 |
| 3 | 4, 8 | 2 |
| 5 | 7, 8 | 2 |
| 6 | 1, 9, 8 | 3 |
| 9 | 4, 7 | 2 |

The rows use 15 gates, and joining their outputs takes five more. **All 20 gates belong to the continuation.** Its first gate writes wire 12, and no gate reads wire 10 or 11. It refutes the variant with continuation budget 20, and hence every larger budget. Sharpness at 17 and the variants with budgets 18 and 19 remain undecided by this example. [Result 4][r4] · [Circuit.size][circuit]

The following check reconstructs the gate list from the table and compares its output with the desk's edge list. It checked all 1,024 primary inputs for each of the 12 choices of `k`, with zero mismatches. The size test uses the same gate list that the evaluator executes. [Construction][r4] · [Desk edge list][reduction] · [Wire indexing][circuit]

```python
edges = [(0,1), (1,2), (2,3), (3,4), (4,0), (0,5), (1,6), (2,7),
         (3,8), (4,9), (5,7), (7,9), (9,6), (6,8), (8,5)]
stars = [(0,[1,4,5]), (2,[1,3,7]), (3,[4,8]), (5,[7,8]),
         (6,[1,9,8]), (9,[4,7])]
gates = []

def gate(op, a, b):
    wire = 12 + len(gates)
    gates.append((op, a, b))
    return wire

def join(wires):
    head, *tail = wires
    for w in tail:
        head = gate("or", head, w)
    return head

output = join([gate("and", c, join(neighbors)) for c, neighbors in stars])
assert len(gates) == 20 and not (len(gates) <= 18)
assert all(i not in (10, 11) for _, a, b in gates for i in (a, b))
mismatches = 0
for mask in range(1024):
    x = [bool(mask & (1 << i)) for i in range(10)]
    expected = any(x[a] and x[b] for a, b in edges)
    w = x + [x[0] and x[2]]
    for k in range(12):
        wires = w + [not (w[k] if k < len(w) else False)]
        for op, a, b in gates:
            wires.append((wires[a] and wires[b]) if op == "and"
                         else (wires[a] or wires[b]))
        mismatches += wires[output] != expected
assert mismatches == 0
```

## Limits of the other evidence

Deleting vertex 9 gives a 12-edge function that needs at least 16 gates. To contradict that bound starting from a 19-gate `D`, a restriction and simplification must leave at most 15 gates, a saving of four. The results establish no such saving for every pattern of readers of the supplied wires. The 17-gate lower bound for the 13-edge function with edges 01 and 12 deleted applies to a different target. Adding those edges back via `x 1 && (x 0 || x 2)` costs gates in the upper-bound direction. [Result 2][r2] · [Result 3][r3] · [L_meta_3817][minor9] · [L_meta_9818][minor13]

The ordinary ten-input problem is already contained in this step. A continuation can ignore both supplied wires. Shifting every index at least 10 up by two, including the output index, embeds an ordinary circuit of the same size and preserves out-of-range reads. Thus a proof of L-meta-4817 would also exclude every ordinary 17-gate PET circuit. Result 2 gives this argument on paper. Result 4 reports an exhaustive search for the five-cycle analogue, finding ordinary minimum size seven and excluding continuations of size at most five for every choice of the negated wire. That search covers a different graph. [Result 2][r2] · [Result 4][r4] · [Circuit evaluation][circuit]

Result 2 searched snapshot `e125f04`. Result 1 also searched upstream at `22af9c68`, examining only the final 9,000 bytes of each of 2,901 files newer than its snapshot. These searches support a claim about what the contributors found. The public PR record also distinguishes reductions from proofs of this step. PR #11268 merged `R_meta_4817_1`. PR #9645 bears the title “L-meta-4817”, but its sole file is another reduction, `R_meta_4817_633.lean`, with additional premises. Neither PR supplies the theorem and subsequent independent check required by the goal. [Result 1][r1] · [Result 2][r2] · [PR #11268][pr11268] · [PR #9645, files][pr9645]

[r1]: ../items/angle-1/result.json
[r2]: ../items/angle-2/result.json
[r3]: ../items/angle-3/result.json
[r4]: ../items/angle-4/result.json
[reduction]: https://github.com/open-goat/pequalnp-proofs/blob/22af9c68/lean/PEqualNP/Outside/R_meta_4817_1.lean
[encode]: https://github.com/open-goat/pequalnp-proofs/blob/22af9c68/lean/PEqualNP/Outside/L_meta_8079.lean
[meta]: https://github.com/open-goat/pequalnp-proofs/blob/22af9c68/lean/PEqualNP/Defs/MetaComplexity.lean
[circuit]: https://github.com/open-goat/pequalnp-proofs/blob/22af9c68/lean/PEqualNP/Defs/CircuitLowerBounds.lean#L51-L68
[lower15]: https://github.com/open-goat/pequalnp-proofs/blob/22af9c68/lean/PEqualNP/Outside/L_meta_4725.lean
[lower16]: https://github.com/open-goat/pequalnp-proofs/blob/22af9c68/lean/PEqualNP/Outside/L_meta_6581.lean
[nine]: https://github.com/open-goat/pequalnp-proofs/blob/22af9c68/lean/PEqualNP/Outside/L_meta_6581.lean#L4442-L4540
[minor9]: https://github.com/open-goat/pequalnp-proofs/blob/22af9c68/lean/PEqualNP/Outside/L_meta_3817.lean
[minor13]: https://github.com/open-goat/pequalnp-proofs/blob/22af9c68/lean/PEqualNP/Outside/L_meta_9818.lean
[pr11268]: https://github.com/open-goat/pequalnp-proofs/pull/11268
[pr9645]: https://github.com/open-goat/pequalnp-proofs/pull/9645/files
