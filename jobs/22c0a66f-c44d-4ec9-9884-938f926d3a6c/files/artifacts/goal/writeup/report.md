# L-meta-5373 (pequalnp outside proof desk): write-up

## Outcome

**Not proved. No Lean theorem, no second-holder check, and no pull request exist for L-meta-5373.** All four merged results (A1–A4) report `status: "missing_lemma"`. None of them submits a proof or a Lean file. Nothing in the results backs a PR on open-goat/pequalnp-proofs, and a write-up can't create a proof, so the goal's deliverable (a checked theorem opened as a PR from the proving contributor's account) is still outstanding. This report records where the step stands. It does not stand in for the proof.

## Sources

The four results, each a JSON object `{status, notes}`. Their full text is reproduced **verbatim** in the Appendix, so this report can be checked without access to the original paths.

| id | path | SHA-256 |
|---|---|---|
| A1 | artifacts/goal/items/angle-1/result.json | `ccd97603b53f0aced82507e5ea1d17f7542a35d835acf39739abfb70abfbcfd0` |
| A2 | artifacts/goal/items/angle-2/result.json | `20cb0af2d13247a6fc35419acaeea26ae7769908b51a6818f1ca751d61b84071` |
| A3 | artifacts/goal/items/angle-3/result.json | `0cf13417bcd19fca88f49375f2101150b3ece72625f6d7ed38580a01a3911ef8` |
| A4 | artifacts/goal/items/angle-4/result.json | `fa02746eae1d9151bcabd1eb292eda81ea665afb28985d9b94e65ff9e16af4ea` |

## What the step says (A1–A4 agree)

E = x3 is a bipartite edge set with no 4-cycle whose graph has a cycle. M = x4 is a matching inside E that contains every pendant edge. C = x5 is an IsAO2 circuit (AND/OR gates, each reading two earlier wires) for f_E. The claim is that some e in E \ M has an IsAO2 circuit for f_{E\e} with fewer gates than C. C may be a least circuit, so the claim amounts to min(E−e) < min(E): a tight circuit lower bound (A1, A2, A3 (1), A4).

## Reductions in the project (checked by workers, not by this write-up)

- **R_meta_5373_951**: the step follows from `highCase` + `residual`. `highCase` is proved as L_meta_8179. A1 reports that `R_meta_5373_951 L_meta_8179` elaborates in Lean 4.36.0, which leaves only `residual` (A1 (1); A3 (4)).
- **R_meta_5373_376**: the step follows from normalize + countLocalized + countShared + compileStars. countLocalized is L_meta_8933. The two workers who supplied the other two pieces disagree on how:
  - A1 wrote its own glue: normalize from L_meta_8385 plus a Nat.find least-size choice, and compileStars from L_meta_2874 by splitting the cover. A1 does not include that glue source.
  - A4 reports that the project already has normalize = L_meta_8567 and compileStars = L_meta_5785, and that `R_meta_5373_376 L_meta_8567 L_meta_8933 countShared L_meta_5785` elaborates.
  
  Both conclude that the step follows from `countShared` alone. A4 gives the full statement of countShared (see the Appendix).
- **R_meta_5373_666** only drops the leaf hypothesis. It needs coreWeak, which is as strong as the step (A2, A3, A4).
- None of the workers found a proved form of `residual` or `countShared` (A1, A3, A4). A2 notes that its search was not exhaustive. A4 also scanned 2810 newer L_ files in the public repository at commit 283aa4af and did not find L_meta_5373 there.

## Small-case evidence (workers' own computations, no Lean proofs)

| Instance | Least gates | Source |
|---|---|---|
| C6 (x1=x2=3) | 8 (7 impossible) | A2 (Node exhaustive search), A3 (MiniSat via logic-solver), A4 (CaDiCaL 1.5.3 via PySAT) |
| C6 minus an edge (6-path) | 7 (6 impossible) | A2, A4; A3 shows a 7-gate star circuit exists |
| C6 plus one pendant edge | 9 (8 impossible) | A4 only |
| C8, theta(3,3,3), C6+2 pendants, 7-edge path | not settled | A3 (ran out of memory), A4 (no answer in 9-minute runs) |

The step holds on every instance that was settled. No worker found a counterexample. **Limitation:** no worker delivered the search scripts, the SAT encodings, or UNSAT certificates (for example DRAT proofs). The "7 gates impossible" result for C6 therefore rests on three independent searches agreeing, and this report cannot re-check it.

## What could not be found or done

- No proof of `residual` or `countShared`. No worker had one, and A3 says it knows of no published proof that star circuits are optimal for every 4-cycle-free bipartite graph.
- No Lean source for the glue A1 describes, and no runnable search or certificate for the small-case minima.
- No second-holder check and no pull request, because there is no proof to check.

## Next step (as the workers propose)

Post `countShared` (A4's statement T) or `residual` (A3, A2 (d)) as its own step. If one of them is proved, the A1 and A4 notes describe how to assemble the file: about 170 KB according to A4, under the 524288-byte limit according to A1.

## Appendix: full verbatim text of each result's `notes` field

### A1 (status: `missing_lemma`)

````text
Not proved. The direct angle (unfold the definitions, find Mathlib lemmas) cannot close this step: it is not a consequence of the definitions plus library facts, it is the inductive step of a circuit lower bound.
Reading of the statement: x3=E is the edge set of a bipartite graph on Fin x1 + Fin x2 with no 4-cycle and with a cycle, x4=M is a matching inside E containing every pendant edge, x5=C is an IsAO2 circuit (AND/OR, exactly two earlier wires per gate) computing f_E(x) = OR over (a,b) in E of x_a AND x_b. Claim: some e in E outside M has a strictly smaller IsAO2 circuit for f_{E minus e}. C is arbitrary, so this says minsize(f_{E-e}) < minsize(f_E) for some non-matching edge. Pinning one input to false (the sibling L-meta-5371) deletes all edges at a vertex; the only edges that are alone at a vertex are pendant and those are in M, so pinning alone never yields an allowed e. One needs an exact lower bound of the shape |E| + (vertex cover) <= size + 1.
What I checked with the prebuilt Lean 4.36.0 / Mathlib (scratch files only, each elaborated with no error and no sorry, axioms reported: propext, Classical.choice, Quot.sound):
(1) The project snapshot (commit e125f04) already records R_meta_5373_951: step <= highCase + residual, and L_meta_8179 proves highCase. Concatenating the two files (imports Mathlib, PEqualNP.Defs) and adding `PEqualNP.Outside.R_meta_5373_951 PEqualNP.Outside.L_meta_8179` elaborates: the step follows from `residual` alone.
(2) It also records R_meta_5373_376: step <= normalize + countLocalized + countShared + compileStars, and L_meta_8933 proves countLocalized. `fun normalize countShared compileStars => PEqualNP.Outside.R_meta_5373_376 normalize PEqualNP.Outside.L_meta_8933 countShared compileStars` elaborates.
(3) I wrote the glue for the other two hypotheses of R_meta_5373_376: normalize from L_meta_8385 plus a least-size choice (Nat.find), compileStars from L_meta_2874 by splitting the cover T into its left and right parts. With them `fun countShared => R_meta_5373_376 normalize L_meta_8933 countShared compileStars` elaborates: the step follows from `countShared` alone.
What is missing: one of two lemmas, neither proved in the snapshot and neither proved by me.
- residual (R_meta_5373_951): the step when no vertex v of degree d >= 2 has more than d reader gates, nor exactly d with an AND reader that is itself read by a gate not reading v.
- countShared (R_meta_5373_376): for a bipartite, non-acyclic, 4-cycle-free G and a least top-form circuit C containing an AND gate not below F that is true at the pair inputs of two different edges ab, cd with readsAtMost C n [a,b] 1 = false and readsAtMost C n [c,d] 1 = false, there is a vertex cover T with |E| + |T| <= C.size + 1.
I searched Outside/ and MetaComplexity/ of the snapshot for a theorem stating either (patterns `readers (0 : N)`, `IsBipartite`, the doubled `readsAtMost ... = false`) and found only the reductions themselves and L_meta_8179 / L_meta_8933. The nearest proved bounds are restricted: L_meta_7241 (every AND gate false on non-edge pair inputs), L_meta_6369 and L_meta_2237 (read-once circuits), MetaComplexity.L115 (girth >= 9, vertices of degree >= 3 far apart). I found no counterexample and computed no exact minimum for any instance, so I do not claim the statement false; its hypotheses are satisfiable (the 6-cycle with x1 = x2 = 3 and M empty), so it is not vacuous.
For whoever continues: a submitted file may use only Mathlib and PEqualNP.Defs, so route (1) must inline L_meta_8179 (27 KB) and R_meta_5373_951 (4 KB) next to a proof of residual; route (2) must inline L_meta_8933 (72 KB), L_meta_8385 (39 KB), L_meta_2874 (33 KB) and R_meta_5373_376 (11 KB) next to a proof of countShared. Both fit in 524288 bytes.
Machine note: here `lean <file>` stopped with `failed to locate application` (/proc/<pid>/exe is not readable); I ran it with a small preload answering that one lookup from /proc/self/exe. Toolchain and project were not changed.
````

### A2 (status: `missing_lemma`)

````text
NOT PROVED. Angle: helper lemmas. Notation: E=x3 (edges), M=x4 (matching), C=x5, f_F = the OR over (a,b) in F of x_a AND y_b, L(F) = least size of an IsAO2 circuit for f_F.
WHAT THE STEP IS. C is an arbitrary correct circuit, so it may be a least one; the step is therefore exactly: some e in E\M has L(E-e) < L(E). That is a strict edge-deletion drop of exact circuit size for every 4-cycle-free bipartite graph with a cycle. I found no way to get it by transforming a given circuit; it needs a lower-bound lemma that the pinned project does not have.
THE SPLIT, AND WHERE EACH PIECE STANDS.
(a) E\M is nonempty and every e in E\M has both endpoints of degree >= 2. Elementary: a cycle is not a matching, and the leaf hypothesis puts every pendant edge in M (E.erase e is nonempty since E has a cycle). Not written in Lean.
(b) Pin an input to false: the sibling L-meta-5371 (proved in the project; would have to be inlined) gives an IsAO2 circuit for the pinned function, STRICTLY smaller when the function depends on that input. It guarantees one gate saved, no more.
(c) Re-attach: for e=(u,w) with deg(u)=d>=2, f_{E-e} = f_{E-u} OR (x_u AND OR(N(u)\{w})), at most d new gates (d-2 OR, 1 AND, 1 OR) appended to a circuit for f_{E-u}. Elementary gate appending. Not written in Lean.
(d) MISSING LEMMA: there is a vertex u with an edge outside M such that pinning x_u removes at least deg(u)+1 gates of C (or C is not least). (a)+(b)+(c)+(d) give the step. With (b) alone, pin-then-re-attach changes the size by up to +(d-1), so it loses. In a star circuit (d) holds exactly when u is a star centre (its d-1 ORs, its AND and one joining OR die); for an arbitrary AND/OR circuit I see no proof, and it looks as strong as the bound |E| + |T| <= size + 1 for a vertex cover T.
SAME GAP IN THE PROJECT. The three reductions of this step at the pinned commit all stop at it: R_meta_5373_951 leaves `residual` (no vertex with more readers than its degree) and `highCase`; R_meta_5373_376 leaves countLocalized and countShared (the vertex-cover bound above) plus normalize and compileStars; R_meta_5373_666 only drops the leaf hypothesis. I found no L_ file proving any of these hypotheses (searched the project for IsVertexCover and IsAcyclic statements); that search is not exhaustive.
TRIED TO REFUTE, FAILED. Smallest instance: E = the 6-cycle on 3+3 vertices (M empty or a perfect matching; every E-e is the 6-path). Exhaustive search by my own Node script, NOT checked in Lean, over fan-in-2 AND/OR circuits without constants on 6 inputs: 6-cycle has no circuit with 5, 6 or 7 gates and has one with 8; 6-path has none with 5 or 6 and has one with 7. So 8 -> 7 and the step holds there. Search assumptions (each without loss for a least circuit): the two operands differ, no two wires compute the same function, every input is read, every gate but the output is read. Larger instances were not searched. I do not claim the statement false, nor true.
NO SHORTCUT IN THE DEFINITIONS. size is the number of gates; IsAO2 = AND/OR only, each gate reads exactly two earlier wires (no constants, no missing wires); an out-of-range output reads false, but f_{E-e} is never constant here (a cycle in a 4-cycle-free bipartite graph has >= 6 edges). The hypotheses are satisfiable (6-cycle): no vacuous proof.
LEAN. The file skeleton (import Mathlib, import PEqualNP.Defs, the theorem exactly as posted, proof sorry) elaborates with Lean 4.36.0 with the sorry warning only, so the statement is well-typed. No Lean file is delivered: there is no proof. On this machine lean would not start as given (error: failed to locate application; /proc/<pid>/exe names another process inside the sandbox); I ran it with an LD_PRELOAD shim redirecting that lookup to /proc/self/exe.
NEXT CUT I WOULD POST: (d) as its own step, in two cases as R_meta_5373_951 does: a vertex with more than deg readers (pin + re-attach closes it), and the residual case, which is the real open problem.
````

### A3 (status: `missing_lemma`)

````text
Not proved; no Lean file is offered. Status missing_lemma: the lemma that is missing is named in (4).

Reading. E=x3, M=x4, C=x5. E is a bipartite edge set with no 4-cycle whose graph has a cycle, C is an IsAO2 circuit for f_E (true iff both ends of some edge of E are true), M is a matching inside E that contains every pendant edge. Wanted: e in E\M and an IsAO2 circuit for f_{E\e} with fewer gates than C.

(1) Strength. The step is as strong as the exact bound |E|+|M| <= C.size+1 of its ancestor L-meta-2872 on graphs with a cycle. R_meta_2872_3 gets that bound from this peel by induction on E; conversely R_meta_5373_376 gets the peel from a bound |E|+|T| <= C.size+1 (T a vertex cover) plus a star circuit for E\e with |E|+|T|-2 gates. C may be a least circuit, so nothing weaker than a tight lower bound for every such graph can prove the step. In the prebuilt project the text `x3.card + x4.card ≤ x5.size` occurs only in R_ reductions, never in a proved L_ theorem.

(2) Routes that fail.
- Pinning an input to false (sibling L_meta_5371, proved) gives a strictly smaller circuit, but it yields f_{E\e} only when an end of e has degree 1, and the step's last hypothesis puts exactly those edges in M (E.erase e is nonempty because E has a cycle). So the cheap route never gives an admissible e: that hypothesis makes the step harder, not easier.
- For e=(a,b) with deg a = d >= 2, f_{E\e} is no restriction of f_E. Pinning x_a and OR-ing back x_a AND (OR of the other d-1 neighbours) costs d gates, so pinning must remove d+1. That is guaranteed only when x_a has more than d readers, or d readers and an AND reader that is read outside them: the `highCase` of R_meta_5373_951, which the project already proves as L_meta_8179 (same statement up to let/have).
- Substituting x_a := x_a AND y_b' (d=2) gives f_{E\e} but adds a gate.

(3) The existence half is easy and is inside R_meta_5373_376: if E\M were empty every vertex would have degree <= 1 and the graph would be acyclic.

(4) The missing lemma is the `residual` hypothesis of R_meta_5373_951: the same conclusion when NO vertex v of degree d >= 2 has more than d readers (nor d readers with an AND reader read outside them). With L_meta_8179 for the other case, R_meta_5373_951 then gives this step verbatim. I found no proved form of it in the project (L_meta_8179 is the only L_ file that speaks of `readers (0 : ℕ)`), and I could not prove it: the optimal star circuits (one AND per cover vertex, each other vertex read once per incident edge) all lie in this case, so it is the generic case and still carries the whole lower bound. The other two reductions leave the same gap: _376 needs countLocalized and countShared (the bound itself), _666 needs coreWeak (this step without the pendant hypothesis). I know of no published proof that star (single-level) circuits are optimal for every 4-cycle-free bipartite graph, and did not look for one on the web.

(5) A check that the statement is not false on its smallest instance (my own computation, not a proof). Exact synthesis by SAT (MiniSat through the npm package logic-solver; rows = the edges and the maximal independent sets, which fix a monotone function; every gate an AND or OR of two distinct earlier wires, every wire read, last gate the output): for the 6-cycle (x1 = x2 = 3, 6 edges, matching number 3) there is no circuit with 1 to 7 gates and there is one with 8, verified on all 64 inputs. So a least circuit has 8 = |E|+|M|-1 gates, while the 6-cycle minus any edge is a path with a 7-gate star circuit: the step holds there. The same runs for the 8-cycle, the 6-cycle with a pendant edge and the theta graph of three paths of length 3 ran out of solver memory and decided nothing.

I do not say statement_seems_false: I have no counterexample. One would have to be a 4-cycle-free bipartite graph with a cycle and a circuit of at most |E|+|M|-2 gates.
````

### A4 (status: `missing_lemma`)

````text
NOT PROVED, NO COUNTEREXAMPLE: it holds in every small case I could settle and is one lemma short of a proof.

WHAT IT SAYS. E = x3 is a bipartite graph with a cycle and no 4-cycle, C = x5 any AO2 circuit for its edge function, M = x4 a matching holding every pendant edge. Claim: some e in E \ M has an AO2 circuit for E - e with fewer gates than C, that is min(E - e) < min(E). E \ M is never empty (a cycle does not fit in a matching), so all the content is a lower bound on the size of C.

SMALL CASES. My own exact search, not a citation: SAT encoding of 'k gates, each AND/OR of two earlier wires, repeats allowed, last gate equals the edge function on all 2^n inputs', PySAT with CaDiCaL 1.5.3. A smaller circuit pads with copy gates, so UNSAT at k excludes every size <= k. Each circuit found was re-evaluated on all inputs outside the solver.
- C6, the smallest graph meeting the hypotheses (x1 = x2 = 3): 7 gates impossible (UNSAT with and without symmetry breaking), 8 possible. C6 minus an edge: 6 impossible, 7 possible. All edges of C6 are alike, so it holds on C6 for every M.
- C6 plus one pendant edge (7 inputs, 7 edges): 8 gates impossible, 9 possible. Removing any edge leaves 6 edges covered by 3 vertices, and one star per cover vertex costs at most 6 + 3 - 1 = 8 < 9. Holds for every M.
- Both minima equal |E| + tau - 1, tau the least vertex cover.
- Not settled (no answer in 9 minute runs): C8, C6 plus two pendant edges, the 7-edge path, theta(3,3,3).

WHERE THE PROOF STANDS. The repository has a checked reduction of this exact statement, lean/PEqualNP/Outside/R_meta_5373_376.lean, from four hypotheses: normalize, countLocalized, countShared, compileStars. Three are already proved there as steps: normalize = L_meta_8567, countLocalized = L_meta_8933, compileStars = L_meta_5785. Checked in Lean 4.36.0 against the prebuilt project: those four files pasted into one scratch file, followed by
theorem t (countShared : T) : <the step as posted> := PEqualNP.Outside.R_meta_5373_376 PEqualNP.Outside.L_meta_8567 PEqualNP.Outside.L_meta_8933 countShared PEqualNP.Outside.L_meta_5785
elaborate with no error and no sorry. So the step follows from the single statement T, which no file proves: it occurs only as that hypothesis, in my snapshot and in the public repository at commit 283aa4af (I scanned the statements of its 2810 newer L_ files; L_meta_5373 is not there). T, with PEqualNP.TopForm, ReadK, EdgeOwnership and MetaComplexity.NestedCover open:
∀ (n : ℕ) (G : SimpleGraph (Fin n)) [DecidableRel G.Adj] (C : Circuit), G.IsBipartite → ¬ G.IsAcyclic → NoFourCycle G → IsLeastAO G C → TopForm G C → (∃ j < C.size, (gateAt C j).op = .and ∧ ¬ BelowF G C j ∧ ∃ a b c d : Fin n, G.Adj a b ∧ G.Adj c d ∧ s(a,b) ≠ s(c,d) ∧ readsAtMost C n [a.val,b.val] 1 = false ∧ readsAtMost C n [c.val,d.val] 1 = false ∧ gateVal n C j (pairInput a b) = true ∧ gateVal n C j (pairInput c d) = true) → ∃ T : Finset (Fin n), G.IsVertexCover ↑T ∧ G.edgeFinset.card + T.card ≤ C.size + 1
In words: |E| + tau <= size + 1 for a least top-form circuit that has an AND gate not below F which is true on two different edges, each with an endpoint read more than once. I did not prove it: it is the lower bound itself where a junk AND gate is shared between edges; L_meta_8933 covers only circuits without one. The small cases agree with its conclusion (6 + 3 = 8 + 1; 7 + 3 = 9 + 1); I did not check whether their least circuits meet its hypothesis.

The other reductions of this step there (R_meta_5373_666, R_meta_5373_951) leave hypotheses as strong as the step.

NEXT. R_meta_5373_376 never uses x4 ⊆ x3 or the pendant-edge hypothesis: given the bound, every e in E \ M works; a counterexample to the step needs a circuit of at most |E| + tau - 2 gates. Post T as its own step; with it the file is the helpers of L_meta_8567, L_meta_8933, L_meta_5785 plus the body of R_meta_5373_376, about 170 KB.
````
