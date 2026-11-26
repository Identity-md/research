**L-meta-5202: consolidated proof-attempt report**

The supplied results do **not establish the goal**. All four have status `missing_lemma`; none supplies a proof of L-meta-5202. They report useful constructions, reductions and unsuccessful searches, but provide neither the completed Lean theorem nor evidence of verification by another holder's machine or a contributor-authored pull request. This report records those results and their limits; it is not a proof submission. [S1–S4]

The requested goal is one Lean 4 theorem for step L-meta-5202 of the outside proof desk pequalnp, checked on another holder's machine and then opened as a pull request on `open-goat/pequalnp-proofs` from the account of the contributor whose machine proves it. That is the assignment's goal, not an outcome documented by the inputs. [Goal]

| Required outcome | Evidence in the supplied results |
| --- | --- |
| Proof of L-meta-5202 | All four explicitly report failure to prove it. Angles 2 and 3 explicitly offer no Lean file. [S1–S4] |
| A check of that proof by another holder's machine | No such attestation, machine-check record or checked theorem artifact is supplied. The reported checks concern auxiliary constructions and examples. [S1–S4] |
| A pull request from the proving contributor's account | No pull-request URL, author attribution or submission record is supplied. [S1–S4] |

Absence here means absence from these four inputs. It does not establish the current state of the public repository or whether work exists elsewhere.

**Sources and scope of evidence**

[Goal] denotes the assignment supplied with this report. [S1]–[S4] denote the four content-pinned JSON inputs below. Each contains a `status` and narrative `notes`; no proof file, enumeration script, SAT certificate, execution log or external verification record accompanies them. Their hashes were checked while preparing this report and match the assignment. Statements attributed to an angle remain that angle's reported findings, unless explicitly identified as arithmetic or a logical consequence below.

| ID | Input and original artifact name | SHA-256 |
| --- | --- | --- |
| [S1](../../../.imd/reads/artifacts/item-angle-1) | `item-angle-1`; `artifacts/goal/items/angle-1/result.json` | `7361f2626b78336526790d5068d1ea6bdda25735c73ef24ea995e5999fc0eb2b` |
| [S2](../../../.imd/reads/artifacts/item-angle-2) | `item-angle-2`; `artifacts/goal/items/angle-2/result.json` | `84721ee9275e48aa6cc60c5440989bbd3ea117d387c2034d2369b9cfd91d3d91` |
| [S3](../../../.imd/reads/artifacts/item-angle-3) | `item-angle-3`; `artifacts/goal/items/angle-3/result.json` | `555c76e136253a683ca10aa8f1e7319eaa4544b2878629089436d81c65b10502` |
| [S4](../../../.imd/reads/artifacts/item-angle-4) | `item-angle-4`; `artifacts/goal/items/angle-4/result.json` | `17060395aef2478798563203c733c10cc6f5499b43b3cb63f744a070dfbdb9fd` |

For a self-contained record of the common outcome, the inputs say:

- S1: “Not proved.” Its status is `missing_lemma`.
- S2: “NOT PROVED; no Lean file is offered.” Its status is `missing_lemma`.
- S3: “Not proved; no Lean file is offered.” Its status is `missing_lemma`.
- S4: “NOT PROVED, and no counterexample found.” Its status is `missing_lemma`.

The input paths above are source identifiers, not delivered Lean artifacts. No upstream source URLs are supplied in the JSON notes. The named project lemmas below therefore cite the angle that reports reading them; this report does not invent upstream file links or claim to have inspected them independently. S3 identifies its project state as commit `e125f04`, and S3 and S4 report using Lean 4.36. These are source-reported identifiers, not a newly reproduced build. [S1–S4]

**Statement being attempted**

The following is a mathematical synopsis, not a recovered exact Lean declaration. In the sources, `C` is a monotone AND/OR circuit with fan-in **at most** two (`Monotone2`) and backward wire references (`ReadsBack 26`). Its inputs represent the 13 points and 13 lines of the projective plane of order 3, using `singerLines3`. The designated wires `a` and `b` are valid circuit wires. [S1–S4]

The hypotheses require:

1. On every flag input consisting of one incident point and line, at least one of `a` and `b` is true. The sources count 52 such flags. [S1–S4]
2. On every input supported on a quadrangle `Q` and its missing lines `missLines Q`, both wires are false. The reported enumeration gives 234 quadrangles, each with four points and three missing lines. [S1, S2, S4]
3. One flag activates `a` alone, and another activates `b` alone. [S1–S4]
4. Three distinct AND gates each directly read an AND gate. Crucially, the reported statement does not require these gates to influence `a` or `b`. [S1–S4]

The conclusion is `63 ≤ C.size`. Unary gates and repeated operands matter to the padding arguments below; replacing this model with fan-in exactly two on distinct operands would require separate justification. [S1–S4]

**What the four attempts contribute**

| Angle | Main contribution | Limit |
| --- | --- | --- |
| 1 | Direct unfolding/library search; identification of the missing general counting argument; Python geometry and baseline-circuit checks; a description of flag-splitting AND gates. [S1] | The statement was elaborated with a placeholder proof, not proved. Its structural observations do not count enough gates. [S1] |
| 2 | Separation into bookkeeping, monotonicity, geometry and gate counting; analysis of signatures on inputs of weight at most two; a failed gate-elimination invariant. [S2] | The proposed count `52 + 13 - 2 = 63` remains unproved for general circuits. No theorem file was elaborated. [S2] |
| 3 | A reported Lean check that four added gates turn the target theorem into an unconditional lower bound of 59 for the same two-wire promise. [S3] | This is a conditional implication assuming the target, not a proof of the target. The scratch proof was not submitted. [S3] |
| 4 | Reported Lean evaluation of a 63-gate baseline and a 66-gate example satisfying all hypotheses; restricted-class analysis and small SAT searches. [S4] | No counterexample or general lower-bound proof was found; restricted searches do not settle the full problem. [S4] |

**Concrete constructions and consistency checks**

The reported baseline uses one term per line: `T_l = y_l AND (OR of the four points on l)`. Each four-input OR costs three binary OR gates. Across 13 lines, this gives 39 OR gates and 13 AND gates; combining the terms into two nonempty groups costs another 11 OR gates. Thus `39 + 13 + 11 = 63`. S1 and S2 describe the dual construction with point-centred terms, with the same total. [S1–S4]

S4 specifies one grouping as seven terms for `a` and six for `b`, with final wire indices 83 and 88. It reports evaluation using the project's `Circuit.wires`, `gateAt`, `singerLines3`, `IsQuadrangle` and `missLines`: the baseline has `Monotone2`, `ReadsBack 26`, flag coverage, rejection of every quadrangle input, both exclusive flags, and zero direct AND-over-AND gates. The checks cover all 52 flags and 234 quadrangles. This is reported Lean `#eval` evidence for the example, not a universal lower-bound theorem. [S4]

S4 then appends the unary gates `AND[65]`, `AND[66]`, `AND[67]`, copying three existing AND terms. The resulting 66-gate circuit reportedly satisfies the nesting requirement as well as the other hypotheses. S1 also reports a 66-gate construction, using a chain of three appended AND copies. Together these reports support consistency of the hypotheses. They do not show that 63 is attained with the nesting requirement, or rule out a qualifying circuit with at most 62 gates. [S1, S4]

**The central reduction, and the necessary/sufficient distinction**

For clarity, let `F` mean the target's circuit-validity, coverage, rejection and two exclusive-flag conditions, with only the three-nested-AND requirement omitted. Let `T` mean the desired theorem for circuits satisfying `F` plus that requirement. This notation only summarizes the hypotheses reported by the angles. [S1–S4]

The sources agree that unused gates can supply the nesting requirement while leaving the two designated wires unchanged. They give two versions:

- **Four-gate version.** S3 appends `AND[0,0]` and then three successive duplicate-operand AND copies. The last three gates directly read an AND gate. S3 reports checking in Lean that the old wire values, `Monotone2` and `ReadsBack 26` are preserved. Assuming `T` yields `63 ≤ C.size + 4`, hence `59 ≤ C.size` for every circuit satisfying `F`. This reportedly elaborated without warnings or `sorry`, but its source is absent. [S3]
- **Three-gate version.** S1, S2 and S4 argue that an `F` circuit must already contain an AND gate: a wire formed only from OR gates that accepts a flag would accept a singleton, whereas the designated wires reject singletons because those singleton supports extend to rejected quadrangle inputs. Appending three unary copies of an existing AND gate supplies the required three gates. Assuming `T` then yields `63 ≤ C.size + 3`, hence `60 ≤ C.size`. The general gate-existence/padding argument is reported reasoning, not a supplied Lean proof. [S1, S2, S4]

The 59 and 60 figures therefore come from different padding constructions and different reported verification levels. They are not conflicting measurements of the target threshold. Both observations explain why a nesting condition permitting irrelevant gates does not by itself restrict the useful circuit computing `a` and `b`. [S1–S4]

The useful logical directions are:

| Statement | Relationship to the target |
| --- | --- |
| Every circuit satisfying `F` has at least 59 gates | A necessary consequence of `T`, via S3's reported four-gate reduction. [S3] |
| Every circuit satisfying `F` has at least 60 gates | A necessary consequence of `T`, via the three-gate argument and existence of an AND gate. [S1, S2, S4] |
| Every circuit satisfying `F` has at least 63 gates | Sufficient for `T`, by applying that bound directly to its hypotheses. [S2, S3] |
| Every corresponding single-output flag/quadrangle separator has at least 64 gates | Sufficient for `T`: append `OR(a,b)` to obtain a single-output circuit with one additional gate, then subtract one from the bound. [S1, S4] |

Some closing suggestions in S1 and S4 list an unconditional 60-gate bound as though it would immediately finish the step. Their padding arguments establish the reverse implication: the target would imply that bound. A lower bound of 60 alone does not supply the missing argument excluding sizes 60, 61 and 62 for circuits meeting the full target hypotheses. No such additional argument is supplied. The stronger sufficient bounds above also remain unproved in the inputs. [S1–S4; logical comparison of their stated reductions]

**Reported project results and the remaining gap**

The angles report the following existing results. The side conditions are essential; these entries are not claims that the target follows from them.

| Named result | Reported content and limitation |
| --- | --- |
| `L_meta_5158` | Single-output lower bound 64 with `andPairs = 0`; S1–S3 report it does not cover the general case here. S2 and S3 describe the flat-case development as 1468 lines. [S1–S3] |
| `L_meta_5162` | Single-output lower bound 64 for a size-minimal circuit with `andPairs = 1`; not a theorem for arbitrary two-wire circuits with several nested ANDs. S2 and S3 report 4429 lines. [S1–S4] |
| `L_meta_7293` | Lower bound 63 when one flag may be omitted and no AND lies in the cone of another AND; its structural restriction does not cover the target. [S1, S3, S4] |
| `L_meta_5160` | Surgery on a pair of AND gates in a cone, when the first rejects all quadrangle inputs, producing a smaller circuit or one of equal size with fewer `andPairs`. S3 identifies the missing applicability when an intermediate AND accepts some quadrangle input. [S3] |
| `L_meta_5272` | S1 reports only a bound of 38 without the relevant side condition, in the fan-in-exactly-two model `IsAO2`. No reduction from that result to the desired bound is given. [S1] |
| `R_meta_5202_7` | Normalization of the two exclusive flags by a collineation; retains a hypothesis named `canonical` carrying the bound. [S1–S3] |
| `R_meta_5202_73` | Reduction to a frontier count, retaining `hCount`. [S1–S3] |
| `R_meta_5202_701` | Establishes `26 ≤ a`, `26 ≤ b`, and `a ≠ b`, then splits by the operations at those wires; retains `hAA`, `hAO` and `hOO`. [S1–S3] |

S2 also reports that sibling steps 5198 and 5200 are present only as conditional `R_` files; S3 identifies `R_meta_5200_1` as retaining the exactly-two branch as a hypothesis. These reports give no completed alternative route. S4 says `PEqualNP.Defs` contains definitions only and reports a restriction against using the cited modules in the candidate file; the exact allowed-import specification is not supplied, so compatibility with it cannot be certified here. [S2–S4]

The substantive obstacle is counting useful gates through multiple AND layers. S1 describes descending from a flag accepted at a designated wire to an AND gate whose operands separate the point and line singleton inputs. Such an intermediate gate may accept quadrangle inputs that a later AND filters out. Consequently, a proof cannot simply assume every such intermediate gate computes a star, or apply a flat-circuit count to all of them. [S1, S3]

**Geometry, counting attempts and counterexample searches**

The angles' reported geometry is consistent: 234 quadrangles, each missing three lines; every point and every line occurs in an appropriate rejected support. S2 and S4 additionally report that every pair of points, every pair of lines and every non-incident point-line pair extends to a rejected support, while incident pairs do not. S1 and S2 attribute their checks to Python enumeration, not Lean proofs; S4 reports enumeration and the baseline's Lean evaluation. [S1, S2, S4]

S2 uses monotonicity and this geometry to characterize the designated wires on inputs of weight at most two: no constant or linear contribution, with their accepted pairs jointly equal to the incidence graph. It reports 52 edges, no 4-cycle, a maximum matching of 13 and a vertex-cover number of 13. These facts motivate the proposed gate count `52 + 13 - 2 = 63`; S2 explicitly identifies deriving that circuit bound as the missing step. The graph figures themselves do not supply that derivation. [S2]

The unsuccessful approaches provide useful limits:

- **Gate elimination.** S2 tried an invariant based on edges plus vertex-cover number. Deleting a line from the baseline removes four OR gates, while the proposed invariant drops by five; the remaining matching has size 12. That mismatch defeats the proposed induction as stated. No stronger invariant was obtained. [S2]
- **Flat star covers.** S3 reports a hand argument, not a Lean proof, that a bottom AND of an OR of points and an OR of lines must be a star if it rejects all quadrangle inputs. S4 reports that 52 flags require at least 13 stars and that a 13-star cover cannot mix point and line stars. It concludes optimality of the 63-gate baseline within the described OR-of-AND-of-OR class. This restricted-class argument does not address intermediate gates whose unwanted values are filtered above. [S3, S4]
- **Other supports.** S4 reports enumeration up to size five of minimal flag-free supports contained in no quadrangle input: 52 collinear point triples, 52 concurrent line triples and 234 quadrilaterals of four lines. It found no saving from products of three OR factors built on such supports, observing that they accept no two-variable flag. These are reported search findings, not a general exclusion of other circuit constructions. [S4]
- **Small exact synthesis.** S4 reports CaDiCaL searches for a monotone binary AND/OR circuit with one output for the eight flags of two lines, and separately of two points, using flags plus restricted quadrangle tests. Eight gates was reported UNSAT and nine gates SAT, including when all 26 inputs could be read. For three lines or three points, the baseline was 14 gates; runs at 12, 13 and 14 gates did not finish within 500 seconds each. Those unfinished runs establish no SAT or UNSAT result, and no full-instance conclusion follows. No solver files or certificates are supplied. [S4]
- **Manual searches.** S1 found no circuit of at most 62 gates meeting all hypotheses. S2 found no improvement by hand using products from biclique-cover constructions. S3 explicitly did not run a machine counterexample search. None of the four reports a counterexample, and none proves that one cannot exist. [S1–S4]

The verification distinctions matter. S1's target-statement elaboration used a placeholder. S2 reports a successful Lean `decide` check that `{p, p+1, p+2, p+5}` is a quadrangle for every point `p`, while explicitly saying it elaborated no proof file for the target. S3's reported Lean check assumes the target as a hypothesis. S4's `#eval` checks particular circuits. None is evidence that Lean has checked L-meta-5202 itself. [S1–S4]

**What remains before the goal can be claimed**

The missing mathematical deliverable is a proof of the original 63-gate statement. The inputs identify sufficient possible routes: a general two-wire lower bound of 63, a corresponding single-output lower bound of 64, or a direct argument that genuinely exploits the target hypotheses and handles filtering through nested ANDs. They supply none of those proofs. [S1–S4]

S2 proposes studying signatures on inputs of weight at most two or proving a cleaning lemma that removes unary and directly nested AND gates without increasing size. S3 proposes tying the nested gates to the designated wires or imposing minimality so that circuit surgery can apply. These are research suggestions, not established lemmas. Changing the statement's hypotheses would also change the assigned theorem and would need justification against the original goal. [S2, S3; Goal]

After the mathematical gap is closed, the goal still requires an actual Lean theorem artifact, its check on another holder's machine, and the specified contributor-authored pull request. No proof source, independent-check attestation, contributor identity or pull-request record is available in the supplied results. The supported outcome of this write-up is therefore an unresolved proof attempt with explicit partial evidence, not a completed public proof contribution. [Goal; S1–S4]
