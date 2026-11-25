# L-meta-3527 (pequalnp outside proof desk): write-up of four results

## Outcome

**Step L-meta-3527 is not proved.** None of the four results has a Lean 4 proof. All four have status `missing_lemma`. So there is no Lean declaration to check and no revision another holder's machine could have checked. **No pull request was opened on open-goat/pequalnp-proofs, and no PR URL exists.** The goal asked for a proved theorem, an independent check and a PR. This deliverable gives none of the three. It records what the four attempts established and the one lemma they all lack.

## Sources

The four results are the only sources. None of them relied on a web source. They are cited by their item name and their SHA-256. They are not committed to Git, so each claim below quotes the result's own words where it matters.

| Item | Path | SHA-256 | status |
|---|---|---|---|
| angle-1 | `artifacts/goal/items/angle-1/result.json` | `50e98de5b1f39bc43a389349cb85528b2ace3d11f5050fef84276292a21d983b` | missing_lemma |
| angle-2 | `artifacts/goal/items/angle-2/result.json` | `fd2591a160c912fe8a4357728bdd066e4fc4ee28f1c3694dc718e7d7ca1539e7` | missing_lemma |
| angle-3 | `artifacts/goal/items/angle-3/result.json` | `c1a5d73071f31c5876c758b20f6251d3fb537a9b4fb5b4ffe0b72840f6777549` | missing_lemma |
| angle-4 | `artifacts/goal/items/angle-4/result.json` | `634e32d9359833d11b2118e12edea514238739d0d1f8f7fc04f6d2da746a6cc8` | missing_lemma |

## What the step says

All four results agree on this reading. x3 = E is the edge set of a bipartite graph on Fin x1 + Fin x2. That graph has no 4-cycle and has a cycle. x4 = M is a matching inside E. x5 = C is an `IsAO2` circuit (AND/OR gates only, each with exactly two inputs) computing f_E, the OR over edges of x_p AND x_l. Let L(H) be the least size of an IsAO2 circuit for f_H. The step is then equivalent to this statement: **for every such E and every such M, some e in E \ M has L(E − e) < L(E).**

- angle-1: "Taking x5 of least size, the step is exactly: for every C4-free bipartite G with a cycle and every matching M in G there is an edge e not in M with L(G-e) < L(G)."
- angle-4: "(Take C minimal for one direction; C.size >= L(E) for the other.) A cycle is not inside a matching, so E \ M is never empty."

How the statement elaborates:

- angle-2 says the statement elaborates on Lean 4.36.0 with Mathlib and PEqualNP.Defs, with the proof replaced by `sorry`.
- angle-1 says it needed `Mathlib.Combinatorics.SimpleGraph.Acyclic` as an extra import ("PEqualNP.Defs alone lacks IsAcyclic").

The two reports differ on the import list. Neither one is a proof.

## Shared argument

**Upper bound (routine).** Cover H with τ(H) stars, where τ is the least vertex cover. This gives L(H) ≤ |H| + τ(H) − 1. By Kőnig's theorem, τ equals the matching number ν on bipartite graphs, which is how angle-1 writes it. The bound drops by at least 1 under any edge deletion. Sources: angle-1, angle-2, angle-3, angle-4.

**Leaf case (elementary).** Suppose some edge outside M has an endpoint of degree 1. Pinning that input to false then gives f_{E−e} and removes at least one gate. Sources: angle-2, angle-3, angle-4.

**Missing lemma (all four results).** A matching lower bound is needed:

> L(E) ≥ |E| + τ(E) − 1 for C4-free bipartite E (with a cycle).

The four results phrase it as follows:

- angle-1 states it as (LB) with ν.
- angle-2 gives a sufficient per-edge form: |E| + τ(E∖e) − 1 ≤ C.size.
- angle-3 and angle-4 narrow the open core to the **leafless / matched-leaves case**. angle-4 states it as "C4-free bipartite E containing a cycle in which every pendant edge lies in the matching M".

**Why local rewriting fails.** Pinning x_u to false deletes deg(u) edges. Restoring deg(u) − 1 of them costs deg(u) gates, so the pin would have to save deg(u) + 1 gates. Nothing forces that. Circuits that are not of star shape also exist with the same size. Examples: angle-3 gives (a∨c)(b∨cd); angle-4 gives (a+c)(b+d)(b+c).

**Prior conditional files.** The repository holds three conditional files for this statement: PEqualNP/Outside/R_meta_3527_615, _642 and _927. Each one assumes the missing part as a hypothesis, so none of them closes the step. Sources: angle-2, angle-3, angle-4. angle-1 reports that it could not read their source on its machine.

## Computational evidence (not Lean, not checked by another holder)

Each result ran its own computation. angle-1, angle-2 and angle-3 ran exhaustive C/C++ searches. angle-4 ran SAT synthesis with python-sat. The table shows what each reported.

| Graph | Least size L | Sources |
|---|---|---|
| 6-path (5 edges) | 7 (none with ≤ 6 gates) | angle-1, angle-2, angle-3, angle-4 |
| 6-cycle | 8 (none with ≤ 7 gates) | angle-1, angle-2, angle-3, angle-4 |
| 6-cycle + one pendant edge | 9 (none with ≤ 8 gates); every one-edge deletion has an 8-gate circuit | angle-1, angle-2, angle-3, angle-4 |
| 6-cycle + two pendant edges at one vertex; 6-cycle + pendants at two cycle vertices at distance 2 | 10 (9 UNSAT); every G−e has a 9-gate circuit | angle-4 only |
| The other five 8-vertex instances (τ = 4, incl. 8-cycle, theta graph) | undecided at 500 s | angle-4 only |
| 17 connected 9-vertex instances | undecided at 240 s | angle-4 only |

Further figures from the results:

- angle-3 reports 19,277,086 search nodes for the 6-cycle at 7 gates. Without the gate-order cut it reports 256,012,381.
- angle-3 reports 1,032,944,354 nodes for the 6-cycle plus a pendant edge at 8 gates.
- angle-2 found 21 normal-form 7-gate circuits for the 6-path and 29 8-gate circuits for the 6-cycle.
- angle-1 and angle-4 say the 6-cycle and the 6-cycle plus a pendant edge are the only connected instances on at most 7 vertices. On that basis, the step holds for x1 + x2 ≤ 7 and every M.

Where the results overlap, they agree. No counterexample was found, and none of the results claims the step is false.

## What a next attempt needs

1. A proof of the lower bound, or of the leafless case of R_meta_3527_615 as its own step (angle-2, angle-3). angle-3 suggests proving the 6-cycle instance (L(C6) ≥ 8) as a smaller checkable lemma first.
2. The routine pieces, formalised: wire/eval bookkeeping, pin-to-false, and the star (cover) circuit (angle-1, angle-2).
3. After that, a check on another holder's machine and the PR from the proving contributor. Neither can happen until a proof exists.
