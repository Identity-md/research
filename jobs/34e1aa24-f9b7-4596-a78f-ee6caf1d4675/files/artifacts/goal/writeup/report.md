# L-meta-7893 | Petersen circuit lower bound

**The goal remains open.** All four input records report `missing_lemma`. The records contain no Lean proof of `PEqualNP.Outside.L_meta_7893` under the posted hypotheses, no successful check of that proof on another holder’s machine, and no pull request from the proving contributor containing it. The desk row updated on 26 November 2026 lists the step under `gaps`, with empty `checked` and `pr_numbers` lists. [Desk statement and status][desk] · [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

## The exact gate limit

The desk quantifies over a circuit `C` with ten input bits, **16 ≤ C.size ≤ 18**, and a nonzero wire index `w < 10 + C.size`. Each gate is an AND or OR of exactly two earlier wires. No gate up to and including wire `w` reads input 0. Let `g(x)` be wire `w` evaluated with bit 0 cleared. The tested output is `H(x) = C(x₀ ∨ g(x), x₁, …, x₉)`. Given that `g` is false on the ten specified rows, the theorem says that `H` must miss a positive row or accept a negative row. [Desk statement][desk] · [Circuit model][model]

Regard each set bit as a vertex. The 15 positive masks are the edges of the Petersen graph. The 15 negative masks are all its maximal independent sets, ten of which omit vertex 0. The function `H` is monotone. If it accepts every edge, it accepts every set containing an edge. If it rejects every maximal independent set, it rejects every subset of one. Those cases cover all 1,024 assignments, so a circuit violating the conclusion would compute the Petersen edge function after substitution. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3]

Every input bit from 1 through 9 occurs in a negative mask omitting 0. Thus a wire false on all ten such masks must itself be a gate output, since `w ≠ 0`. Insert an OR of wire 0 and wire `w` immediately after `w`, shift the later wire numbers, and redirect later reads of 0 to the new wire. Apply the same wire mapping to the output index. The prefix through `w` already ignores bit 0. The resulting circuit `D` computes `H` with **17 to 19 gates**, and its inserted OR is the sole reader of input 0. It would suffice to prove that every such `D` with at most 19 gates disagrees with the Petersen function on at least one of the 30 listed rows. The insertion is a paper reduction in the item records. [Angle 1][a1] · [Angle 2][a2] · [Angle 4][a4]

## What the two pull requests establish

- **Merged PR #22077** declares `R_meta_7893_1`. Its arguments include `substOneGate` for the circuit insertion, `coverSixAnds` for six distinct AND gates, and `orAssemblyCost` for a size bound of `14 + t` given any `t` distinct AND gates. The proof calls all three and derives `20 ≤ D.size ≤ 19`. There is a concrete counterexample to the universally quantified `orAssemblyCost` argument below. [PR #22077][pr1] · [Lean declaration and proof][r1]
- **PR #21990** reduces the step to `plain`, `rename`, and `active`. These assume a lower bound for ordinary circuits, preservation of circuit and wire values under input relabeling, and a lower bound when the selected wire is true on edge mask 6 or 12. The public checker reported exit 0 for the commit containing that conditional declaration. The check therefore covers the reduction. [Lean declaration and proof][r2] · [Checker receipt][check]

## What the witnesses establish

Increasing the desk cap on **the original circuit** from 18 to 19 makes the statement false. Angles 1 and 4 supplied different 19-gate circuits satisfying the wire and row conditions. Both have output wire 28. Angle 1 reports a scratch Lean check using `native_decide` for the circuit predicate and row evaluations. Angle 4 reports a scratch Lean check using `decide +kernel`. The table gives the gate counts after making the substitution explicit. The replay below checks each substituted circuit on every assignment. [Angle 1][a1] · [Angle 4][a4] · [Wire evaluation and size][wires]

| Witness | Original gates | Selected wire | Explicit circuit gates | AND gates | OR gates |
|---|---:|---:|---:|---:|---:|
| [Angle 1][a1] | 19 | 11 | 20 | 6 | 14 |
| [Angle 4][a4] | 19 | 22 | 20 | 7 | 13 |

**Angle 4 refutes the counting premise of PR #22077.** In its explicit circuit, the zero-based gate indices `3, 9, 10, 12, 14, 16, 17` give an injective enumeration of seven AND gates. The circuit meets both row lists. Taking `t = 7` in `orAssemblyCost` would give `14 + 7 ≤ 20`. That premise has no size cap and applies to this circuit as written. The desk theorem caps the original circuit at 18. Both witnesses exceed that cap by one, so neither decides the theorem. [Angle 4 gate list][a4] · [Exact premise][r1] · [Gate indexing][gateAt] · [Desk statement][desk]

## Evidence at the requested cap

Angle 2 explains why the step entails a lower bound even for ordinary Petersen circuits. Given any such circuit with at most 17 gates, prepend enough copies of `x₂ ∧ x₃` to put its size in the allowed interval, with at least one copy. Select the first copy as `w`. When that wire fires, the input already contains edge {2,3}, so raising bit 0 preserves the correct positive answer. On an independent set the wire is false. This would satisfy the hypotheses and violate the conclusion. Angle 2 tested the construction on a larger circuit and obtained the expected row values. Its size exceeded the cap. [Angle 2][a2]

Setting bit 0 to false yields a circuit for the graph with vertex 0 deleted. Angle 4 gives a 16-gate upper bound for that restricted graph, which explains why the restriction alone cannot exclude the posted interval. Angle 3 derives the ten false values of `g` from the other row conditions. Each maximal independent set omitting 0 acquires an edge when 0 is added. If `g` fired there, the substitution would give the same output on those two rows, which require opposite answers. [Angle 3][a3] · [Angle 4][a4]

The searches produced no certificate at the relevant sizes. Angle 3 reports that the single-OR-reader instance at 19 gates was undecided after 430 seconds on each of five solvers. Angle 4 searched the original 18-gate instance with 20 processes for 500 seconds, then 26 processes for 450 seconds. Neither run returned a model or an UNSAT result. Its size-19 runs also timed out despite a known witness at that size. What is still needed is a proof excluding all original circuits of sizes 16 through 18 under the wire condition, followed by another holder’s successful check of the same theorem and a contributor PR containing that proof. [Angle 3][a3] · [Angle 4][a4] · [Desk statement][desk]

## Replaying the boundary witnesses

The following Python 3 code uses the two gate lists verbatim in wire order, with `|` for OR and `&` for AND. It checks the desk masks, the selected wire, both circuit evaluations, and the AND indices used above. This finite calculation can be reproduced independently of the authors’ scratch Lean checks. [Gate list 1][a1] · [Gate list 4][a4] · [Desk masks][desk] · [Circuit evaluation][wires]

```python
edges = [3, 6, 12, 17, 24, 33, 66, 132, 160, 264, 288, 320, 528, 576, 640]
negative = [50, 69, 104, 116, 138, 201, 208, 276, 385, 402, 521, 548, 554, 770, 773]
zero_free = [50, 104, 116, 138, 208, 276, 402, 548, 554, 770]
rows = range(1 << 10)
petersen = [any(mask & edge == edge for edge in edges) for mask in rows]
assert negative == [
    m for m in rows if not petersen[m] and
    all(petersen[m | (1 << i)] for i in range(10) if not (m >> i) & 1)
]
assert zero_free == [m for m in negative if not m & 1]

witnesses = [
    (11, """|2,6 &1,10 |1,4 |12,5 &0,13 |2,4 |15,8 &3,16 |2,5 |18,9
            &7,19 |5,6 &8,21 |4,6 &9,23 |14,17 |25,20 |26,22 |27,24"""),
    (22, """|3,7 |8,9 |1,5 &10,11 |4,12 |7,8 |1,11 |3,9 |1,10 &2,18
            &13,15 |4,20 &5,15 &6,16 |19,23 &17,21 &0,14 |25,26 |24,27"""),
]

def evaluate(gates, mask):
    wires = [(mask >> i) & 1 for i in range(10)]
    for op, a, b in gates:
        assert op in ("&", "|") and 0 <= a < len(wires) and 0 <= b < len(wires)
        wires.append(wires[a] & wires[b] if op == "&" else wires[a] | wires[b])
    return wires

for w, listing in witnesses:
    circuit = []
    for token in listing.split():
        a, b = map(int, token[1:].split(","))
        circuit.append((token[0], a, b))
    prefix_length = w - 10 + 1
    assert len(circuit) == 19
    assert all(0 not in (a, b) for _, a, b in circuit[:prefix_length])
    helper = [evaluate(circuit, m & ~1)[w] for m in rows]
    assert all(helper[m] == 0 for m in zero_free)
    assert [evaluate(circuit, m | helper[m])[28] for m in rows] == petersen

    def redirect(i):
        if i == 0:
            return w + 1
        return i + 1 if i > w else i

    explicit = circuit[:prefix_length] + [("|", 0, w)]
    explicit.extend((op, redirect(a), redirect(b))
                    for op, a, b in circuit[prefix_length:])
    assert sum(0 in (a, b) for _, a, b in explicit) == 1
    assert [evaluate(explicit, m)[29] for m in rows] == petersen
    ands = [j for j, (op, _, _) in enumerate(explicit) if op == "&"]
    assert len(explicit) == 20
    if w == 22:
        assert ands == [3, 9, 10, 12, 14, 16, 17]
        assert 14 + len(ands) > len(explicit)
    print(w, len(circuit), len(explicit), len(ands), len(explicit) - len(ands))
```

[desk]: https://pequalnp-desk.pequalnp.workers.dev/desk/row?gap=L-meta-7893
[a1]: ../items/angle-1/result.json
[a2]: ../items/angle-2/result.json
[a3]: ../items/angle-3/result.json
[a4]: ../items/angle-4/result.json
[pr1]: https://github.com/open-goat/pequalnp-proofs/pull/22077
[r1]: https://github.com/open-goat/pequalnp-proofs/blob/0138f0621c49674293d925bcc959c0cef16a8536/lean/PEqualNP/Outside/R_meta_7893_1.lean#L40-L58
[r2]: https://github.com/open-goat/pequalnp-proofs/blob/cc744f5e6a5a005c89f150780def289405b2a079/lean/PEqualNP/Outside/R_meta_7893_1.lean#L5-L24
[check]: https://github.com/open-goat/pequalnp-proofs/pull/21990#issuecomment-7177603201
[model]: https://github.com/open-goat/pequalnp-proofs/blob/0138f0621c49674293d925bcc959c0cef16a8536/lean/PEqualNP/Defs/TopForm.lean#L80-L85
[wires]: https://github.com/open-goat/pequalnp-proofs/blob/0138f0621c49674293d925bcc959c0cef16a8536/lean/PEqualNP/Defs/CircuitLowerBounds.lean#L44-L68
[gateAt]: https://github.com/open-goat/pequalnp-proofs/blob/0138f0621c49674293d925bcc959c0cef16a8536/lean/PEqualNP/Defs/NestedCoverCircuit.lean#L107-L109
