# L-meta-1884 — Petersen circuit lower bound

**L-meta-1884 remains unproved in the four worker results.** The missing lemma would rule out every fan-in-two circuit of at most 18 gates for the Petersen edge function even when the complement of one input is free. The public Lean reduction takes this lemma as its argument `lower` on line 14. The workers supply neither a proof nor a counterexample. There is no second-holder check of a completed proof or qualifying contributor pull request in the handoff. [Angle 1](#angle-1) · [Angle 2](#angle-2) · [Angle 3](#angle-3) · [Angle 4](#angle-4) · [Lean declaration][cut]

## The proof obligation

Let `P x` be true when both endpoints of some Petersen edge are true in `x`. The desk numbers the vertices 0 through 9. The outer cycle is 0–1–2–3–4–0, the spokes are 0–5, 1–6, 2–7, 3–8, 4–9, and the inner cycle is 5–7–9–6–8–5. The circuit model allows AND, OR and NOT with at most two input wires per gate. NOT reads its first input. Size counts every gate, including NOT, and input wires are free. [Edge list][edges] · [FanInTwo][fan] · [Gate evaluation and size][eval]

The original step quantifies over every circuit `C`, every input map `σ : Fin 10 → Fin 10` and every unary function `u : Bool → Bool`. A circuit with fan-in at most two and size at most 18 must disagree with `P x` on some `x` when evaluated on `List.ofFn (x ∘ σ) ++ [u (x 0)]`. After normalizing the inputs, the remaining proposition has the following Lean form. [Original statement and normalized hypothesis][cut]

```lean
∀ C : Circuit, FanInTwo C → C.size ≤ 18 →
  ∃ x : Fin 10 → Bool, C.eval (List.ofFn x ++ [!x 0]) ≠ P x
```

Angle 2 reports a Lean 4.36.0 check of equivalence in both directions. Specializing the original statement to `σ = id` and `u = Bool.not` gives the displayed proposition. In the other direction, `L_meta_2594` absorbs any input map at equal gate count, including a non-injective map. `L_meta_2596` replaces the unary input by the free complement without increasing size when the output is not the appended wire. `R_meta_1884_773` handles that output-wire case and uses `lower` for the remaining circuits. This locates the relabeling lemma that Angle 1 could not find. Angle 3 separately checked that the statement elaborates with a `sorry` body. [Angle 1](#angle-1) · [Angle 2](#angle-2) · [Angle 3](#angle-3) · [Relabeling][relabel] · [Normalization][normalize] · [Reduction proof][cut-proof]

Angle 1 checked an evaluation identity that explains the link to the parent problem. Prepending a NOT of wire 0 to a circuit on ten ordinary inputs produces precisely the eleven starting wire values in the displayed proposition. Thus a counterexample using at most 18 gates would give an ordinary circuit of at most 19 gates beginning with that NOT. L-meta-1884 handles the unary first-gate branch of L-meta-651. The parent reduction also has binary first-gate branches. [Angle 1](#angle-1) · [Parent reduction][parent]

## What is known at the 18-gate budget

| Result | Consequence for a hypothetical circuit computing `P` |
|---|---|
| `L_meta_5367` | If `k` gates read wire 0 or wire 10, then `15 + k ≤ C.size`. Count a gate once and inspect only the first input of a NOT. At most three gates can read either wire within the budget. A contradiction would still require ruling out those cases. [Lean statement][reads] · [Angle 2](#angle-2) |
| `L_meta_6194` | An ordinary circuit for `P` needs at least 15 gates other than NOT. Applied after prepending the NOT above, this leaves at most three NOT gates **among the original 18**. Angle 1 gives this last deduction as a paper inference. [Lean statement][nonnot] · [Angle 1](#angle-1) |
| `L_meta_4332` | At size at most 15 on ten ordinary inputs, every wire, with either choice of output polarity, disagrees with `P` somewhere on the slice `x 9 = false`. Its budget and input model leave the displayed proposition open. [Lean statement][slice] · [Angle 1](#angle-1) |

Two other reductions also retain hypotheses. `R_meta_1884_1` assumes the ordinary Petersen bound at 18 gates, the vertex-deleted bound at 15 gates and restrictions on reads of wires 0 and 10. `R_meta_1884_412` assumes a circuit bound called `core` involving monotonicity, symmetry and pivotal variables. Angle 2 counted input reads after pruning unused gates. A circuit of size `s` with `N` NOT gates then has at most `2s − N` effective input slots. At least `s − 1` slots connect gates, leaving at most `s − N + 1` reads of input wires. A variable read only once still leaves possible circuits. [First reduction][first] · [Symmetry reduction][sym] · [Angle 2](#angle-2)

**An explicit upper bound is 20 gates.** Angle 2 gives the circuit below, where juxtaposition is AND and `+` is OR. Each parenthesized group uses one AND at its center and enough binary ORs to combine its neighbors. The six groups cost 3, 3, 2, 3, 2 and 2 gates, followed by five ORs. Expanding the groups gives the 15 edges listed above. Angle 2 checked all 1024 assignments, and the circuit ignores the extra wire. Angle 4 independently reports a 20-gate construction using the vertex cover `{0,1,3,7,8,9}` and an enumeration excluding a cover of size five. These are upper-bound witnesses for circuit size. [Angle 2](#angle-2) · [Angle 4](#angle-4) · [Edge list][edges]

```text
x1(x0+x2+x6) + x3(x2+x4+x8) + x4(x0+x9)
             + x5(x0+x7+x8) + x7(x2+x9) + x6(x9+x8)
```

## Which graphs the proposed induction covers

Angle 3 proposes a stronger lemma **for induced subgraphs of the Petersen graph**. Choose a vertex subset, retain every Petersen edge between the chosen vertices, and let `τ(G)` be its minimum vertex-cover size. The conjectured lower bounds for its edge function are `|E(G)| + τ(G) − 1` ordinary gates and `|E(G)| + τ(G) − 2` gates when the complement of one chosen vertex input is free. On the full graph the second expression is `15 + 6 − 2 = 19`, which would settle the step. The induction remains conjectural even for this restricted family. [Angle 3](#angle-3) · [Angle 4](#angle-4)

On the four-cycle 0–1–2–3–0 the two disjoint edges 01 and 23 require two cover vertices, and `{0,2}` covers every edge. The two proposed bounds would therefore be 5 and 4. The circuit `(x0 OR x2) AND (x1 OR x3)` uses three gates in either model. Its four cross terms are exactly the four edges, so it agrees on all 16 assignments. Opposite vertices of a four-cycle have two common neighbors. In the Petersen edge list every pair has at most one, so this example lies outside the proposed family. [Angle 3](#angle-3) · [Petersen edge list][edges] · [Finite checks](#finite-checks)

Restricting a Petersen input illustrates the missing induction step. Setting `x0 = false` leaves nine vertices, 12 edges and minimum cover size five. Angle 3 checked a 16-gate construction on all 512 remaining assignments. To exclude an 18-gate circuit this way would require a **lower** bound of 16 on the restriction and the elimination of at least three gates. A variable that feeds only ORs can cost just one gate per bypass. Setting `x0 = true` leaves `x1 OR x4 OR x5` together with the edge function of the cycle 2–3–8–6–9–7–2, joined by OR. Angle 3 reports an 11-gate construction there. Even a matching lower bound would require eliminating eight gates. [Angle 3](#angle-3)

## Exact-synthesis results

Each entry is a worker's solver verdict at the stated gate count. In the last two columns the extra wire is the free complemented input used in that worker's instance. A dash means the record gives no verdict for that cell. Angle 3 used normalized gates and the last gate as output. Angle 4 reports checking returned circuits on every input. Neither record supplies a checked UNSAT certificate. [Angle 3](#angle-3) · [Angle 4](#angle-4)

| Graph | Ordinary, Angle 3 | Ordinary, Angle 4 | Free complement, Angle 3 | Free complement, Angle 4 |
|---|---|---|---|---|
| Path on four vertices | 3 UNSAT, 4 SAT | 3 UNSAT, 4 SAT | 2 UNSAT | — |
| Three-leaf star | — | 2 UNSAT, 3 SAT | — | — |
| Five-cycle | 6 UNSAT, 7 SAT | 6 UNSAT, 7 SAT | 5 UNSAT | 6 UNSAT |
| Six-cycle | 7 UNSAT, 8 SAT | 7 UNSAT, 8 SAT | 6 UNSAT | 7 UNSAT |
| Five-cycle with one pendant edge | 7 UNSAT, 8 SAT | 8 SAT | 6 UNSAT | 7 UNSAT |
| Five-cycle with pendant edges at two adjacent vertices (induced on 0–6 in Angle 3) | 8 UNSAT, 9 SAT | 9 SAT | 7 UNSAT | 8 UNSAT |
| Spider with three legs of length two | — | 8 SAT | — | 7 UNSAT, center complemented |

On the graph induced by vertices 0–7, Angle 3 reports no verdict in 200 seconds for 12 or 11 ordinary gates, or for 10 gates with the free complement. Angle 4 reports that two solvers left the seven-cycle at nine gates with a free complement undecided after about nine minutes. Petersen minus `{0,1,2}` at ten gates also remained undecided after about nine minutes. The record leaves its extra-input setting unspecified. [Angle 3](#angle-3) · [Angle 4](#angle-4)

For the full Petersen graph at **18 gates**, Angle 4 tried five searches. One used ordinary monotone circuits. Three supplied the free complement and respectively allowed exactly one NOT, exactly two NOTs or at least three NOTs in the circuit. The fifth used Glucose 4 without gate-type restrictions. Each ended after about nine minutes without a verdict. A calibration run at 20 monotone gates also timed out despite the explicit witness above. The 18-gate question therefore remains unanswered by these searches. [Angle 4](#angle-4)

## Finite checks

This Python check uses the public edge list, Angle 2's upper-bound circuit and the four-cycle example. The assertions cover the 20-gate count, the Petersen truth table, its minimum cover size, exclusion of four-cycles, and the three-gate truth table on the four-cycle. [Edge list][edges] · [Angle 2](#angle-2) · [Angle 4](#angle-4)

```python
from itertools import combinations, product

edges = [(0,1), (1,2), (2,3), (3,4), (4,0), (0,5), (1,6), (2,7),
         (3,8), (4,9), (5,7), (7,9), (9,6), (6,8), (8,5)]
stars = {1: (0,2,6), 3: (2,4,8), 4: (0,9),
         5: (0,7,8), 7: (2,9), 6: (9,8)}

def edge_value(x, graph):
    return any(x[a] and x[b] for a, b in graph)

def is_cover(vertices):
    return all(a in vertices or b in vertices for a, b in edges)

assert sum(map(len, stars.values())) + len(stars) - 1 == 20
for x in product((False, True), repeat=10):
    value = any(x[c] and any(x[j] for j in leaves) for c, leaves in stars.items())
    assert value == edge_value(x, edges)
assert is_cover({0, 1, 3, 7, 8, 9})
assert not any(is_cover(vs) for vs in combinations(range(10), 5))

neighbors = [set() for _ in range(10)]
for a, b in edges:
    neighbors[a].add(b)
    neighbors[b].add(a)
assert all(len(a & b) <= 1 for a, b in combinations(neighbors, 2))

four_cycle = [(0,1), (1,2), (2,3), (3,0)]
for x in product((False, True), repeat=4):
    assert ((x[0] or x[2]) and (x[1] or x[3])) == edge_value(x, four_cycle)
```

## Worker evidence

The passages below come from the `notes` field of each supplied JSON record. The identifiers and SHA-256 digests refer to the original files. The SAT verdicts, time limits and Lean check descriptions are the workers' accounts. The supplied records contain no solver certificates or completed proof file.

[cut]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/R_meta_1884_773.lean#L14-L16
[cut-proof]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/R_meta_1884_773.lean#L17-L53
[edges]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/R_meta_1884_412.lean#L21-L26
[fan]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Defs/MetaComplexity.lean#L27-L31
[eval]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Defs/CircuitLowerBounds.lean#L37-L68
[relabel]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/L_meta_2594.lean#L93
[normalize]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/L_meta_2596.lean#L528
[parent]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/R_meta_651_1.lean#L8-L23
[reads]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/L_meta_5367.lean#L7205
[nonnot]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/L_meta_6194.lean#L3245
[slice]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/L_meta_4332.lean#L6973
[first]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/R_meta_1884_1.lean#L5-L22
[sym]: https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/lean/PEqualNP/Outside/R_meta_1884_412.lean#L9-L17

### Angle 1

Input `item-angle-1` · Status `missing_lemma` · SHA-256 `271f0133dc70652efb3eff0a6db5c81057f5dad86bfa7a7611c5e4071deee229`

> Not proved; no Lean file is offered. Angle 1 (unfold and close with Mathlib lemmas) does not reach it: after unfolding Circuit.eval, Circuit.wires and FanInTwo the statement is a bare gate-count lower bound, and nothing in Mathlib or PEqualNP.Defs carries one. The lemma that is missing is the core below.
>
> I did not find relabel among the proved files, but it is routine. lower is the whole difficulty. CHECKED HERE in Lean 4.36.0 with the prebuilt project (scratch file, no error): for every circuit C and x : Fin 10 → Bool, C.eval (List.ofFn x ++ [!x 0]) = (Circuit.mk (⟨GateOp.not, [0]⟩ :: C.gates) C.output).eval (List.ofFn x), by simp [Circuit.eval, Circuit.wires, GateOp.eval, List.getD_eq_getElem?_getD]. So a counterexample to lower is the same thing as a FanInTwo circuit with at most 19 gates for the Petersen function on 10 inputs whose first gate is NOT of wire 0.
>
> I scanned the final theorem of all 3937 L_* files under PEqualNP/Outside: none states lower. Five state something about List.ofFn x ++ [!x 0] on ten variables, all partial. The relevant proved fragments: (a) L_meta_5367, 523825 bytes: if C is FanInTwo and computes Petersen from x ++ [!x 0], then 15 + (number of gates reading wire 0 or wire 10, a NOT counting only its first input) ≤ C.size; hence in a counterexample at most 3 gates touch x0 or its negation. (b) L_meta_6194, 148848 bytes: a FanInTwo circuit whose circuitFun 10 is Petersen has at least 15 gates that are not NOT; applied to the circuit with the prepended NOT (my inference, not formalised) a counterexample has at most 3 NOT gates. (c) L_meta_4332, 520393 bytes: for a FanInTwo circuit with at most 15 gates on ten inputs, no wire and no negated wire agrees with Petersen on all inputs with x 9 = false. The two other checked cuts of this step, R_meta_1884_1 (97622 bytes; leaves ¬HasCircuitSize 10 Petersen 18, a 15-gate bound for the 9-vertex graph, and two cases about which gates read wires 0 and 10) and R_meta_1884_412 (leaves core, the same bound for a monotone automorphism-invariant F), also leave the bound itself open.
>
> The residual case, 18 gates with at most 3 NOT gates and at most 3 gates on x0 or ¬x0, is decided by none of the proved fragments.

### Angle 2

Input `item-angle-2` · Status `missing_lemma` · SHA-256 `6669675d843676b600e3f4d2f05ea6f4bb7fa3123f1bb1dec189fb71a3813496`

> NOT PROVED; no Lean file is offered. The step is exactly as hard as one bare lower bound, and that bound is the missing lemma.
>
> MISSING LEMMA (LOWER): ∀ C : Circuit, FanInTwo C → C.size ≤ 18 → ∃ x : Fin 10 → Bool, C.eval (List.ofFn x ++ [!x 0]) ≠ P x, with P the Petersen edge function of the step. In words: no AND/OR/NOT fan-in-two circuit with at most 18 gates computes P, even with the negation of x0 as a free input. This is the 19-gate lower bound that the desk's own sketch calls open.
>
> CHECKED IN LEAN (4.36.0, prebuilt project, scratch file; axioms propext, Classical.choice, Quot.sound): LOWER ↔ the step's statement. (→) is the project's R_meta_1884_773 applied to L_meta_2594 (relabel the inputs along any σ at equal size) and L_meta_2596 (replace the extra wire u (x i) by !x i without growing the circuit); I re-elaborated those three files and they pass. (←) is the instance x2 := id, x3 := not, closed by exact. So the split into helper lemmas (my angle) is: H1 relabel, proved (L_meta_2594); H2 normalize, proved (L_meta_2596); H3 the case output = wire 10, proved inside R_meta_1884_773; H4 LOWER, open. Nothing smaller than H4 is left: any further cut has to cut H4.
>
> LOOKED FOR, NOT FOUND in the prebuilt project: a proved statement of LOWER, or a complete set of proved hypotheses for any of the three checked reductions of this step it ships (R_meta_1884_1, _412, _773). Each keeps an unproved core: _1 assumes ¬HasCircuitSize 10 P 18 and a 9-vertex analogue at 15, among others; _412 assumes its hypothesis core; _773 assumes LOWER. The proved Petersen steps with a size bound near 18 that I found cover only degenerate circuits: output an input wire (L_meta_9037), gates reading input wires only (L_meta_9039), at most one gate (L_meta_6024, L_meta_9031), non-surjective rewiring (L_meta_4015).
>
> CLOSEST PROVED FACT: L_meta_5367: if a FanInTwo circuit computes P from List.ofFn x ++ [!x 0], then 15 + (number of gates reading wire 0 or wire 10) ≤ size. So a counterexample to LOWER has at most 3 gates touching x0 or its negation. That is 15 + k, not 19; I found no way to force k ≥ 4.
>
> WHERE A DIRECT ARGUMENT STALLS (paper reasoning, not checked in Lean): (1) Wire counting: after deleting unread gates, s gates of which N are NOT offer at most 2s − N input slots and gate wires use at least s − 1 of them, so input wires are read at most s − N + 1 ≤ 19 times; hence one of the ten variables is read exactly once. The 20-gate circuit is a formula with 21 reads, so this is one read short of a contradiction and gives none alone. (2) Gate elimination: x_v := 0 removes at least 2 gates unless x_v feeds a single OR gate, where it removes 1; the known circuit spends 15 + 6 − 1 (edges + vertex cover − 1), so a star centre would have to be shown to cost 3 to 4 gates, and x_v := 1 leaves the class of graph functions. Deleting vertices at 2 gates each cannot reach 19, since the last few vertices carry no edge. I did not find the invariant that closes this, and did not try to formalise a partial bound below 19, which would not prove the step.
>
> NOT CLAIMED FALSE: I have no circuit with at most 18 gates and ran no exhaustive or SAT search (18 gates over 11 wires does not fit in this run), so I give no evidence of falsity. One sanity check: the star-cover circuit x1(x0+x2+x6) + x3(x2+x4+x8) + x4(x0+x9) + x5(x0+x7+x8) + x7(x2+x9) + x6(x9+x8) has 20 gates and agrees with P on all 1024 inputs for either value of the extra wire, under the Circuit.eval semantics (checked by a Python script, not in Lean).
>
> SUGGESTED NEXT CUT OF H4 (unverified): apply L_meta_5367 at every vertex, transporting by H1 and a Petersen automorphism; the free negation then costs one extra NOT gate, which should give size ≥ 14 + reads(x_v) for v ≠ 0. Combine with count (1) to pin down the read profile of a putative 18-gate circuit, then case on the variable read once.

### Angle 3

Input `item-angle-3` · Status `missing_lemma` · SHA-256 `36000ca6fe9e0fccaf172865d3081b9224003af1155bf40edd5adeee008b5ebd`

> NOT PROVED. No Lean file: I have no proof, only an analysis and bounded computations.
>
> WHAT THE STEP IS. It is the hypothesis `unary` of the checked cut R_meta_651_1 (the first gate of a 19-gate circuit reads one wire or none). With x2 = id and x3 = not it says: no fan-in-two AND/OR/NOT circuit with 18 gates computes the Petersen edge function F, even when NOT x0 is given free as an 11th input. So it implies size(F) >= 19 in the project's model (every gate counted, NOT included), while the best circuit known has 20. This branch is therefore not easier than the parent: it is the parent's conjecture one gate lower. x3 constant or id adds nothing; a non-injective x2 only removes inputs.
>
> WHERE THE CONTEXT ROUTE STOPS (gate elimination by restricting x0).
> - x0 := false turns F into the edge function of Petersen minus a vertex (9 vertices, 12 edges, minimum vertex cover 5). That function has a 16-gate circuit (built here and checked on all 512 inputs). So this route needs BOTH (a) the restriction removes at least 3 of the 18 gates, and (b) the exact bound that Petersen minus a vertex needs 16 gates. The standard argument does not give (a): if x0 is read only by OR gates they are merely bypassed, one gate each. And (b) is a tight bound of the same kind as the step, with no slack to induct on.
> - x0 := true leaves x1 or x4 or x5 or (the 6-cycle on 2,3,8,6,9,7) (identity checked on all 1024 inputs), which has an 11-gate circuit; that route would need 8 gates removed.
> So an induction on vertices needs the exact value |E| + tau - 1 (tau = minimum vertex cover: 20 for Petersen, 16 minus a vertex, 8 for the 6-cycle) at every level, against circuits with NOT gates. I know no technique that proves this and found none.
>
> THE MISSING LEMMA (stated as the target, not proved). For every induced subgraph G of the Petersen graph, every FanInTwo circuit computing the edge function of G has at least |E(G)| + tau(G) - 1 gates, and at least |E(G)| + tau(G) - 2 gates when NOT x_v is given as one free extra input. With G the Petersen graph the second half is this step (19 > 18).
>
> COMPUTED EVIDENCE for that lemma. My own exact-synthesis SAT encoding, Glucose4 through python-sat 1.9.dev25; gates are AND/OR of two distinct earlier wires or NOT of one, the last gate is the output. Computed in this run, NOT checked by Lean or by a proof checker:
> - path on 0,1,2,3 (value 4): 4 gates SAT, 3 UNSAT; 2 with free NOT x0 UNSAT.
> - 5-cycle on 0..4 (value 7): 7 SAT, 6 UNSAT; 5 with free NOT x0 UNSAT.
> - 6-cycle on 2,3,8,6,9,7 (value 8): 8 SAT, 7 UNSAT; 6 with free NOT x0 UNSAT.
> - 5-cycle plus pendant vertex 5 (value 8): 8 SAT, 7 UNSAT; 6 with free NOT x0 UNSAT.
> - induced on 0..6 (7 edges, tau 3, value 9): 9 SAT, 8 UNSAT (MapleChrono); 7 with free NOT x0 UNSAT.
> - induced on 0..7 (9 edges, tau 4, value 12): 12, 11, and 10 with free NOT x0 all undecided in 200 s.
> So the small analogue of this step (value minus 2 gates, NOT x0 free) held wherever the solver finished, and NOT gates saved nothing. Several optimal circuits found are not single-level, e.g. the path as (x1 or x3) and (x2 or (x0 and x1)), so a proof cannot assume the star-cover shape. The step itself (18 gates, 1024 rows) is far beyond this search: the 8-vertex 12-gate instance was not even found satisfiable in 200 s. No 18-gate circuit was found and I have no reason to call the statement false.
>
> LEAN. The statement as posted elaborates against PEqualNP.Defs with the prebuilt toolchain (body sorry, only to confirm the statement and the setup; nothing else was elaborated).

### Angle 4

Input `item-angle-4` · Status `other` · SHA-256 `edd7411665a0e0751078191b8d821330c98b60fab3ccfc252eb0c258d8d92791`

> Not proved and not refuted. No Lean file is offered.
>
> SEARCH FOR A REFUTATION (my angle). I wrote an exact-synthesis SAT encoder (python-sat 1.9.dev25, CaDiCaL 1.5.3 and Glucose 4; normalised AND2/OR2/NOT1 gates, CEGAR over truth-table rows). Every circuit it returned was re-evaluated on all inputs. Its UNSAT answers are solver verdicts only: no proof certificate was checked.
> Small cases, minimum gate count for the edge function OR_{ij in E} x_i x_j:
> - path on 4 vertices: 3 gates UNSAT, 4 SAT
> - star K_{1,3}: 2 UNSAT, 3 SAT
> - C5: 6 UNSAT (also with a free NOT x0), 7 SAT
> - C6 (= Petersen minus a closed neighbourhood): 7 UNSAT (also with free NOT x0), 8 SAT
> - C5 plus a pendant edge at vertex 0: 7 UNSAT with free NOT x0, 8 SAT
> - spider, a centre with three legs of length 2 (induced in Petersen): 7 UNSAT with free NOT of the centre, 8 SAT
> - C5 plus pendant edges at two adjacent vertices: 8 UNSAT with free NOT x0, 9 SAT
> In all seven the minimum equals |E| + tau - 1 (tau = vertex cover number), the cost of the star-cover circuit, and neither NOT gates nor the free negated input saved a gate. For Petersen that formula gives 15 + 6 - 1 = 20: I checked by enumeration that no vertex cover of size 5 exists, and built and verified on all 1024 inputs a 20-gate circuit from the cover {0,1,3,7,8,9}, matching the desk's known bound.
> Full size: five runs for Petersen at 18 gates, each cut off after about 9 minutes with no answer (monotone on plain inputs; free NOT x0 with exactly 1 NOT gate, exactly 2, at least 3; unrestricted with Glucose 4). A calibration run asking for the known 20-gate monotone circuit also did not finish in that time, so these timeouts are no evidence either way. Also undecided after about 9 minutes: C7 at 9 gates with free NOT x0 (two solvers) and Petersen minus {0,1,2} at 10 gates.
> So no counterexample was found, and the small cases give no hint of one, but 18 gates on 11 wires was not searched to completion.
>
> WHY NO PROOF. The lower bound itself is the open part. The one-variable gate-elimination argument I tried removes two gates per fixed variable and then needs bounds for the restrictions (Petersen minus a vertex, or x_a OR x_b OR x_c OR C6), which it does not supply; it falls well short of 18. A brute-force kernel proof is out of reach under the file rules (no native_decide, 524288 bytes): the solver could not settle even 10 gates on 7 variables here. The prebuilt project holds three conditional reductions of this exact statement (R_meta_1884_1, R_meta_1884_412, R_meta_1884_773) and no unconditional proof; each leaves hypotheses of the same difficulty, e.g. _773 leaves the free-NOT-x0 lower bound itself, and _1 leaves that Petersen has no 18-gate circuit and Petersen minus a vertex no 15-gate circuit.
>
> WHAT WOULD MOVE IT. A solver certificate (DRAT/LRAT) for the free-NOT-x0 instance at 18 gates would settle truth but would still not fit a Lean file under these rules; a human-style case analysis, as the desk's reductions attempt, seems to be the only route to a checked proof.
