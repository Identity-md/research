# L-meta-650: consolidated proof-desk handoff

**Outcome: the goal remains unachieved in the supplied evidence.** All four results say that they neither proved nor refuted the requested step and supplied no Lean file. None supplies a second-holder verification record or a contributor pull-request URL. This report is a synthesis of unsuccessful proof attempts, not a Lean theorem or a completed submission. [A1–A4]

The goal requires a Lean 4 theorem for L-meta-650, checked on another holder’s machine, followed by a pull request on `open-goat/pequalnp-proofs` from the proving contributor. That requirement comes from the assignment. The sources describe the mathematical target as a monotone binary circuit of at most **63 gates** for the function below. They provide a **64-gate** construction and a restricted lower-bound argument; neither meets that target. The exact Lean declaration and its dependencies are not included in the supplied results, so this report cannot certify their correspondence to the informal target. [A1–A4]

## Sources and evidence boundaries

These labels cite the `notes` and `status` fields of the four supplied JSON results. The hashes were recomputed locally and match the assignment’s pinned hashes. The links identify source locations; the substantive findings are preserved below because the input files are delivered separately from this report.

| Label | Supplied result | SHA-256 | Reported status |
| --- | --- | --- | --- |
| A1 | [item-angle-1](../../../.imd/reads/artifacts/item-angle-1) | `09eadf46582bf0a71b37787fc20c33dc3feacc56edc4d77ab3ddd1a7bfa014eb` | `statement_seems_false` |
| A2 | [item-angle-2](../../../.imd/reads/artifacts/item-angle-2) | `9e37a9711f8efb37aeb8f7fe2edbd10878de8986d961f0d79e5a2f9d57d4b3a7` | `other` |
| A3 | [item-angle-3](../../../.imd/reads/artifacts/item-angle-3) | `dbf23800eab574ecad4dbf284107c4eae9db3e52371db7ebca7e84845f2806eb` | `statement_seems_false` |
| A4 | [item-angle-4](../../../.imd/reads/artifacts/item-angle-4) | `9eea2065fc578d6e3a0a1997536cfb4ca8c35954c431c0bef398707870975615` | `other` |

A1 and A3 suspect that the statement is false, but explicitly do not prove that judgment. A2 and A4 report no proof in either direction. These positions are compatible: suspicion is not a refutation. No source contains Lean source code, solver certificates, executable search code, or raw check logs. Computational results below are therefore attributed reports, not independently rerun or certified computations. Agreement among these reports does not constitute another holder checking a particular Lean artifact. [A1–A4]

## Target and available construction

The sources identify the edge set as

`E = {(p, 13+l) : 0 ≤ p,l < 13 and (p+l) mod 13 ∈ {0,1,3,9}}`,

and the target as `f(x) = OR_{(p,13+l) ∈ E} (x_p AND x_{13+l})`. They identify this graph as the point-line incidence graph of the projective plane of order 3: 26 vertices, 52 edges, degree 4 at each vertex, and exactly one common neighbour for two distinct vertices on the same side. Consequently it has no 4-cycle. The reported minimum vertex-cover size is 13. [A1–A4]

For each of the 13 points, OR its four neighbouring line variables using three binary gates, then AND that sum with the point variable using one gate. OR the 13 resulting terms using 12 gates:

`13 × (3 + 1) + 12 = 39 + 13 + 12 = 64`.

Thus this witness exceeds the requested maximum by one gate. A1 reports checking it on the 52 edge inputs and 704 maximal false inputs. A2 reports those checks plus 200000 random inputs. A3 reports a bit-parallel check on all `2^26` inputs; A4 also reports exhaustive checking on all `2^26` inputs. These checks concern the 64-gate construction and are outside Lean. [A1–A4]

The reported graph has 704 maximal independent sets. A1 and A4 also report 38730 independent sets; A4 reports maximum independent-set size 13. A1 reports 11232 automorphisms including dualities, 54 independent-set orbits, and orbit counts by size 0 through 13 of `1,1,2,3,7,7,10,8,5,4,3,1,1,1`. A2 reports three unordered input-pair orbits: 52 incident point-line pairs, 117 non-incident point-line pairs, and 156 same-side pairs. A3 expresses the symmetry count as 5616 times duality. These are source-reported structural computations, not Lean lemmas supplied here. [A1, A2, A3, A4]

## What the lower-bound argument establishes—and leaves open

A2–A4 give an informal argument for circuits in which no AND gate has another AND gate below it; A1 gives the corresponding star argument. In that restricted class, each useful AND combines two OR-only variable sums. Every resulting pair must be an edge, and the absence of a 4-cycle forces the product to be a star. Its centres must cover the graph’s edges. OR gates combining at least two leaves cannot be shared between distinct centres, since two leaves determine at most one common centre. [A1–A4]

A3 makes the accounting explicit. Let `k` be the number of useful AND gates, `k₁` the number of singleton-leaf stars, and, for each centre `c`, let `m_c` count its other stars and `W_c` be their leaf union. The lower OR gates cost at least `Σ_c (|W_c| − m_c)`; joining the AND outputs costs at least `k − 1` further OR gates. Since `k = k₁ + Σ_c m_c`, `Σ_c |W_c| + k₁ ≥ 52`, and `k ≥ 13`, the total is at least `52 + 13 − 1 = 64`. A3 states the analogous restricted bound as `|E| + τ(G) − 1` for graphs without 4-cycles. This remains an informal proof in the supplied material. [A3, notes §3; A2, Cut A; A4, Cut 1]

**This is not a lower bound for unrestricted Monotone2 circuits.** A circuit with at most 63 gates, if one exists, must escape that argument by nesting AND gates and absorbing higher-degree products. No source proves that this cannot save a gate. The shared gap is precisely the unrestricted nested-AND case. [A1–A4]

## Search results and their limits

For a monotone circuit, the sources use the 52 edge inputs as positive tests and the 704 maximal independent sets as negative tests, a total of 756 rows. Every true input contains an edge and every false input lies inside a maximal independent set, giving the stated sufficiency by monotonicity. A2 also proposes gate replacements that preserve one of these boundary signatures while moving pointwise downward or upward, and uses these to prune gates. These are informal arguments, not supplied formal proofs. [A2, Cut B; A4, TEST SET]

| Source | Reported search | Result and limitation |
| --- | --- | --- |
| A1 | Kissat 4.0.1; 63 gates; 8.8M clauses; 20 seeds, 530 seconds each | Neither a model nor UNSAT. Control searches also failed to recover known 64-gate and 27-gate circuits. A1 explicitly says this supplies no evidence either way. |
| A2 | Kissat 4.0.2; 63 gates; 300 of 704 negative rows with refinement; 8 seeds, 420 seconds each | Undecided; known 64-gate and Fano 27-gate controls were not recovered. A later symmetry-breaking run timed out without output. |
| A4 | CaDiCaL 2.1.3; fix 12 point stars and their OR chain, totalling 59 gates and 85 available wires | Four additional gates reported UNSAT; five reported SAT. This excludes only that fixed-prefix completion, not all 63-gate circuits. No independent encoder check or proof certificate is supplied. |
| A4 | Free two stars: 54 fixed gates, nine free gates; point pairs `{11,12}`, `{0,12}`, `{5,12}` | Undecided after about nine minutes on 14, 4 and 4 runs respectively; eight-free-gate searches also undecided. |

All entries in this table are source-reported outcomes. A timeout is not an impossibility proof. A3 reports no successful witness for the target and instead contributes smaller-graph experiments. [A1–A4]

The small-case evidence must also retain its scope:

- A1, A2 and A4 report that a 6-cycle needs eight gates: seven UNSAT, eight SAT. A1 reports verifying the witness on all 64 inputs. [A1, A2, A4]
- A2 reports an 11-gate 8-cycle circuit. A4 reports 11 SAT and ten undecided. A3 lists its own 8-cycle run as unfinished. These are distinct search outcomes, not a shared exact lower bound. [A2, A3, A4]
- For the theta graph with three length-three paths, A2 reports 12 gates found and 11 undecided after six 420-second seeds. A4 reports 12 SAT and 11 undecided after about nine minutes on roughly 20 runs using two encodings. A3 also leaves this graph unfinished. [A2, A3, A4]
- A3 reports exact minima equal to `|E| + τ − 1` on 17 smaller graphs: paths P4–P8 `(4,5,7,8,10)`; C5–C7 `(7,8,10)`; spiders 2-2-2 and 2-2-2-1 `(8,10)`; C6 with one or two pendant edges `(9,11,11)`; C5 with one or two pendants `(8,9)`; theta(2,3,3) `(11)`; double star `(6)`. These are reported CaDiCaL/python-sat encoding results without supplied certificates. They do not settle the denser target graph. [A3, notes §5]
- A3 reports unfinished runs for C8, theta(3,3,3), and C6 with three pendants, with no circuit at at most nine gates and stated comparison bounds `(11,12,11)`. A2 leaves Fano at 26 gates undecided after eight 420-second seeds. A4 leaves subdivided K4 at 14 gates and Heawood at 26 undecided. [A2, A3, A4]

A4’s statement that no case beyond the 6-cycle was proved tight describes its own results. It should not erase A3’s stronger reported small-case results, nor upgrade A3’s unprovided certificates into checked proofs. [A3, A4]

## Proposed routes, not completed proofs

A2’s signature pruning and the three pair orbits leave four proposed first-gate cases: AND of an incident pair; OR of an incident pair; OR of a non-incident point-line pair; and OR of two points. A1 reports that the project already has a first-gate symmetry reduction, `R_meta_650_1`, as well as `R_meta_650_713` and `R_meta_650_517` (the latter deleting point 0). Their source and exact declarations are not supplied, so they cannot serve as checked dependencies here. [A1, A2]

A1 suggests normalizing to a strict live binary DAG and using the identity `totalSurplus + n = size + 1`. At `n = 26`, a circuit of at most 63 gates would have surplus at most 38, whereas the star circuit has 39. A4 gives the equivalent excess `s − 25`. This accounting motivates searching for saved repeated reads; it does not itself forbid nested circuits. [A1, A4]

A1 proposes dividing cases by the independent set `I` of ineligible inputs and its 54 symmetry orbits. It reports that any four points miss at most three lines, hence such an independent set has at most three points or at most three lines. A proposed charge `4|I| − |N(I)|` would give 39 when `I` is all points or all lines, but remains unproved and leaves small or empty `I` unresolved. A1 explicitly notes that the Heawood counting argument does not transfer directly: 26 eligible labels fit within a surplus allowance of 38. [A1]

A3 proposes a lower bound for straight-line union/intersection programs on signatures recording singleton and pair inputs, with target `(empty, E)` on `26 + 325` positions. It reports that testing only inputs with at most two ones already refutes size bound-minus-one on 11 of its smaller graphs. Its general lemma `(L)` for graphs without 4-cycles is explicitly missing. Proving it would refute the requested upper bound, rather than provide the requested witness. [A3, notes §6]

A2–A4 suggest formalizing the restricted lower bound and resolving the theta(3,3,3) case before attempting a general nesting theorem. A4 also suggests freeing more stars in the constrained search. A2 records failed algebraic attempts: shared sums create non-edge cross terms; a global point/line guard costs 25 gates; and `(x_p OR K)(L_p OR K) = x_p L_p OR K`, with `K` below the target, costs one gate more than its plain form. None is a successful 63-gate construction. [A2–A4]

A1 reports an existing Heawood theorem `L_meta_971` with bound 27 and general normalization machinery, and says the project’s `R_meta_972_*` reductions conclude the conflicting lower bound 64 for the same list. It reports no `L_meta_972` file in its snapshot. These are unverified project descriptions, not evidence that the general target lower bound has been proved. A3 explicitly did not rely on the project files it could not inspect. [A1, A3]

## Revision finding and outstanding handoff

Finding `90646e79b9fef7ee5a44afc1dbca7d099a4bb52ab024fb0a227cfb0bfd03bf74` correctly identifies the substantive evidence gap: no requested Lean theorem, no second-holder check, and no contributor PR. Its arithmetic and qualification of the lower bound agree with A1–A4. The earlier report and its cited lines were absent from this revision checkout; the supplied artifacts were four JSON results and their matching copies, not two copies of a Markdown report. That portion of the stated reproduction could not be repeated. [A1–A4; local inventory and hash comparison for this revision]

This revision supplies the bounded write-up requested by the assignment and records the finding separately. It does **not** repair the missing mathematical proof or claim completion of the larger goal. Supplying invented Lean code, a check record, or a PR URL would contradict the source requirement. The demand to create those missing artifacts is disputed as a requirement of this synthesis task, while its factual observation that the larger goal is incomplete is accepted.

The outstanding evidence is a Lean source proving the exact L-meta-650 declaration, a successful check of that same source by another holder, and a PR URL attributable to the proving contributor after that check. None can be recovered from these four results. Alternatively, a proof of the suspected unrestricted lower bound would establish that the requested witness is impossible, but no such proof is supplied either. [Assignment goal; A1–A4]
