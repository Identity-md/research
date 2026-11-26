# L-meta-2598 — Petersen-graph circuit lower bound

**The four results leave L-meta-2598 open.** None supplies a Lean 4 proof or a counterexample. They record neither a check of the completed theorem by another holder's machine nor a pull request from the proving contributor to `open-goat/pequalnp-proofs`. The closest proof attempt reduces the theorem to circuits in which just one or two gates read the distinguished input. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

## What must be proved

For ten Boolean inputs, let `P(x)` be true when both endpoints of at least one of the Petersen graph's 15 edges are true. The graph has outer cycle `0–1–2–3–4–0`, spokes from `i` to `i+5` for `i = 0,…,4`, and inner cycle `5–7–9–6–8–5`. Wires 0 through 9 carry the inputs, and wire 10 carries `¬x₀` for free. L-meta-2598 says that for **every** fan-in-two AND/OR/NOT circuit of at most 18 gates, **some** input makes its output differ from `P(x)`. Angle 1 reports that the posted statement elaborated in Lean 4.36.0. [Angle 4][a4] · [Angle 1][a1]

## Where the proof stops

Let `r` count gates that read wire 0 or wire 10. A gate counts once, and only the first input of a NOT gate counts. The following reductions are in the project snapshot at `e125f04`. [Angle 2][a2] · [Angle 3][a3]

| Reduction | Available ingredient | Missing ingredient |
| --- | --- | --- |
| `R_meta_2598_314` | `L_meta_3817` gives a 16-gate lower bound for the nine-vertex graph. The reduction handles `r = 0` and `r ≥ 3`. | `low_reads` must exhibit a mismatch when `1 ≤ r ≤ 2` and the circuit has at most 18 gates. Angle 2 checked the implication in Lean with the nine-vertex statement and `low_reads` as hypotheses. Its separate run on `L_meta_3817` timed out after 280 seconds. [Angle 2][a2] |
| `R_meta_2598_639` | `L_meta_5367` gives `15 + r ≤ C.size` for a correct circuit, excluding `r ≥ 4` at the proposed size. | `fewReaders` must give a mismatch for `r ≤ 3`. Angle 3 checked that these two hypotheses imply the target in Lean. [Angle 3][a3] |
| `R_meta_2598_704` | Angle 3 checked the composition with `R_meta_4085_317` in Lean, using the statements of `L_meta_4083` and `L_meta_5905` as hypotheses. | The residual hypothesis `few` is another lower bound for circuits with few readers. [Angle 3][a3] |

The difficulty in the first route is the restriction `x₀ = false`. Three eliminated gates would leave at most 15, contradicting the nine-vertex bound. Eliminating only one or two from an 18-gate circuit leaves 17 or 16, both compatible with that bound. A reader such as `x₀ OR h` becomes a copy of `h`, so eliminating it need not eliminate its consumers. The further splits for `low_reads` and `fewReaders` are conditional too. No matching proof was identified in the reported searches. One search of newer files inspected theorem statements in file tails and missed 98 statements too long to fit. [Angle 2][a2] · [Angle 3][a3]

Angles 1 and 2 also checked a reduction using ordinary ten-input circuits. Prepending `NOT [0]` produces exactly wire 10, preserves subsequent wire numbers and costs one gate. A 20-gate lower bound on ordinary circuits would therefore imply the requested 19-gate bound with the free wire. The searches found no such ordinary-circuit lower bound in the project. [Angle 1][a1] · [Angle 2][a2]

## What the circuit searches establish

Angle 1 reports a Lean kernel check over all 1,024 inputs of a **20-gate circuit**. Angle 4 checked a second construction by script. In the expression below, juxtaposition means AND and `+` means OR. Its six ANDs, nine ORs inside the terms and five ORs joining them give an upper bound of 20. Whether any circuit of size 18 or less works is still unresolved. [Angle 1][a1] · [Angle 4][a4]

```text
x1(x0+x2+x6) + x3(x2+x4+x8) + x4(x0+x9)
  + x5(x0+x7+x8) + x6(x8+x9) + x7(x2+x9)
```

Angle 4's 17-gate candidate also accepts inputs having at least two true vertices among the independent set `{0,2,8,9}`. It disagrees with the target on exactly 17 of 1,024 inputs. SAT searches for circuits of sizes 17 and 18 timed out, and the searches also missed the known 20-gate construction. They yielded no infeasibility certificate for the target. [Angle 4][a4] · [Angle 1][a1]

The reported SAT results on smaller graphs give minima of 4 and 5 gates for paths on four and five vertices, 7 and 8 for cycles on five and six vertices, and 8 and 9 for a five-cycle with one and two specified spokes. These match the edge count plus the minimum vertex-cover size minus one, which would give 20 on the Petersen graph. Extending that pattern to a lower bound on the full graph remains conjectural. Angle 4 used a minimum-circuit normal form, and its eight-vertex search also timed out. [Angle 1][a1] · [Angle 4][a4]

## Fitting a proof into the submission

The theorem file may import only `PEqualNP.Defs` and has a 524,288-byte cap. Inlining `L_meta_3817` and reduction 314 as written takes 510,618 + 48,668 = 559,286 bytes before proving `low_reads`. On route 639, `L_meta_5367` alone takes 523,825 bytes, leaving 463. Route 704 has the most documented room for a new proof. The reported sizes of its four ingredients sum to 332,321 bytes, leaving a nominal 191,967 bytes for `few` and the assembly. That route still depends on proving `few` before there is a theorem for a second holder to check. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3]

[a1]: ../../../.imd/reads/artifacts/item-angle-1 "angle-1/result.json · SHA-256 00455d22ba95b7f886e9bf71113224eafc9f6f5fe059a8656bde63c3959401d4"
[a2]: ../../../.imd/reads/artifacts/item-angle-2 "angle-2/result.json · SHA-256 5479f326d5c365058d00d231843bfcef926a08139b57ff91053b2dfc4beff6cb"
[a3]: ../../../.imd/reads/artifacts/item-angle-3 "angle-3/result.json · SHA-256 9c4e385b19a41856a82a394c26baa2fa61d9db9ad921978033abbfe5a5951783"
[a4]: ../../../.imd/reads/artifacts/item-angle-4 "angle-4/result.json · SHA-256 98ff614f413977d156e5242a24e13e37d4b6ccf725d8f2b4fca589c345c92e0a"
