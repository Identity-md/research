# L-meta-5126: consolidated proof-attempt report

The supplied results do **not** establish L-meta-5126. They contain no completed Lean theorem source, no record of another holder’s machine checking a completed source, and no subsequent pull-request URL. Three results report `missing_lemma`; the fourth reports `other` and explicitly says “Not proved, and not refuted.” This report records the work and its limits; it is not a completed proof or evidence that the overall goal was achieved. [S1–S4]

## Sources and evidence boundary

The sources are the four supplied JSON results, identified below by their logical artifact paths and SHA-256 digests. Their bytes were checked against the digests in the assignment. The public-project findings, Lean runs, and enumeration results below are attributed to those results; their underlying proof files, programs, and execution logs were not supplied. No independent Lean check, enumeration rerun, or public-repository audit is claimed here. The logical links identify the input artifacts even if the report is distributed without those files.

| ID | Supplied result | SHA-256 |
|---|---|---|
| S1 | [angle-1/result.json](../items/angle-1/result.json), read from `.imd/reads/artifacts/item-angle-1` | `4b7e58ea12e3a9250eb61ebe815a79515a09d2b5b85ebfe8f1f1836d67ecd5d6` |
| S2 | [angle-2/result.json](../items/angle-2/result.json), read from `.imd/reads/artifacts/item-angle-2` | `5e7b92599391da2f21732a1ca0a6adc24bc23ddd0b0f7406e069571f1e16d38f` |
| S3 | [angle-3/result.json](../items/angle-3/result.json), read from `.imd/reads/artifacts/item-angle-3` | `0026eb2c2ee4b89e8df6bdcff1b94a650d528ff577ace9453905f04359f5f26f` |
| S4 | [angle-4/result.json](../items/angle-4/result.json), read from `.imd/reads/artifacts/item-angle-4` | `ffbb04de4dea7004fa85c411a8898258201d3f8d9bbd3e6b29278b3aa3e0deac` |

S3 identifies its project snapshot as commit `e125f04`. S1 says the public copies it read matched its prebuilt copies byte for byte, but its supplied JSON contains no URL list. The inputs do not establish a single common revision for all four investigations. Repository identifiers below therefore describe the workers’ reported findings, not a verified current repository state. [S1, S3]

## What was established, and what remains missing

The goal requires a Lean 4 theorem proving step L-meta-5126, checked on another holder’s machine, followed by a pull request to `open-goat/pequalnp-proofs` from the proving contributor’s account. The assignment supplies that goal; the following outcome assessment comes from S1–S4.

| Required outcome | Evidence in the supplied results |
|---|---|
| Completed theorem | None. S1 and S3 offer no Lean file. S2 describes a draft with one `sorry` for the central claim and explicitly says it is not a proof and is not submitted. S4 supplies computational observations. |
| Another holder’s check of that exact theorem | No completed source or corresponding independent check record is included. The reported Lean elaboration and computational searches are not this check. |
| Pull request from the proving contributor after that check | No PR URL, submission record, or account attribution is included. |

These are absences in the supplied evidence, not a claim that no relevant proof or PR could exist elsewhere. [S1–S4]

## The mathematical obligation

As described by the workers, the step concerns a bipartite graph with `NoFourCycle` and a least AND/OR circuit computing its graph function. Its first-rung hypothesis excludes a least circuit with exactly one junk AND gate; its conclusion excludes exactly two junk AND gates when every junk gate is false at every one-hot input. The results identify `PEqualNP.Outside.L_meta_3760` as an existing proof of the first rung, with the same statement also appearing in `L_meta_8725`. Thus the unresolved mathematical content is the two-junk-gate exclusion under the extra one-hot condition. The exact posted Lean statement is not reproduced in any supplied result, so this is a paraphrase rather than a substitute theorem declaration. [S1–S3]

S1 reports that the posted header and introduction of hypotheses elaborate under Lean 4.36.0, without closing the body. S2 reports, under the same Lean version, a `junk_pair` lemma extracting ordered gates `g1 < g2` from junk cardinality two, and a `step_of_core` reduction to a `CoreClaim`. That core says that bipartiteness, `NoFourCycle`, `IsLeastAO G C`, `g1 < g2`, `junk G C = {g1, g2}`, and both gates being false on every `unitInput` imply `False`. The draft’s one `sorry` admits precisely this core claim. S3 expressly says nothing in its run was Lean-checked. [S1–S3]

S3 isolates a sufficient replacement-circuit lemma, denoted (M): under the step’s two-junk-gate assumptions, construct `D` such that

```text
IsAO2 n D
circuitFun n D = graphFun G ∅
and either
  D.size < C.size
or
  D.size = C.size and (junk G D).card = 1.
```

The smaller-size alternative contradicts leastness. In the equal-size alternative, `D` is itself least and contradicts the first rung. This is a proposed reduction, not a proved lemma; S3 states that no part of (M) was proved in its attempt. [S3]

S1 supplies an unformalized argument for a restricted case. Let `h` be the higher-index junk gate, and let `E_h` be the graph edges whose edge inputs stop being accepted when `h` is forced false. If `E_h` is contained in a single edge `uv` on whose input `h` is true, replace `h` by `AND(x_u, x_v)`. S1 argues that this preserves the computed graph function and size, leaves the lower junk gate untouched, and makes the junk count one. It explicitly lacks an argument when the higher gate is needed by two or more edges. This paper argument is not reported as checked in Lean. [S1]

## Obstacles and available partial results

**Normalization.** `L_meta_1501` and its use within `L_meta_3760` preserve size and junk count while producing `TopForm`; the reported exported statements do not preserve the one-hot falseness hypothesis. S3 suggests carrying that invariant through the induction, using `V2_gateval` from `L_meta_1499` and falseness of the graph function on unit inputs, but did not prove it. S1 also names `L_meta_5779` among the normalization rows. [S1–S3]

**Gate shapes and nesting.** S2 reasons that in top form the lower junk gate has no AND gate in its cone, so its operands are ORs of input sets; one-hot falseness would force those sets to be disjoint. The same argument for the upper gate requires the lower gate to be outside its cone. S2 identifies the need to establish the existing partial rows’ additional conditions, including lift fixed points, output-cone membership, and restrictions on AND operands, while preserving the two-junk and one-hot hypotheses. These are proposed proof steps, not completed formal results from this attempt. [S2]

The workers report the following nearby rows, none of which they successfully combine into the requested theorem:

| Row | Reported relevance and limitation |
|---|---|
| `L_meta_5391` | A nested configuration where junk gate `T` reads junk gate `g`, with another operand `OR(Cs)` and additional fixed-point and reader conditions. S1 describes a construction removing two junk gates; S2 describes the resulting size inequality counting lost edges and stresses that it does not conclude `False`. The descriptions do not establish an unconditional reduction. [S1, S2] |
| `L_meta_5412` | Excludes a specified two-flag configuration at a lift fixed point, with operands drawn from specified neighborhoods and sides of size at least two. [S1, S2] |
| `L_meta_5138` | Excludes a specified path configuration with two-by-two sides and further conditions. S1 calls it a five-vertex path core; S2 describes a path `d-z-w-z0-b-a`. The inputs do not resolve that descriptive discrepancy; neither claims a general theorem. [S1, S2] |
| `L_meta_7895` | Under `TopForm` and junk cardinality two, gives a counting alternative or a chain `g → h → m`. [S1] |
| `L_meta_8305` | Concerns a junk gate needed by one edge in the `Monotone2` model. [S1] |
| `L_meta_1491` | A general counting inequality for arbitrary junk count. [S3] |
| `L_meta_5242` | A covering bound under top form, two junk gates, a nested cone condition, and girth at least five; not a contradiction. [S3] |

S3’s broad statement that it found no proof of junk cardinality unequal to two “under any hypothesis” must be read as a limit of its search: S1 and S2 identify restricted impossibility rows. S1 reports reading final statements of 162 Outside rows mentioning junk. S2 reports pattern searches in a folder of 5,592 files and reading about 25 statements, not their proofs. None establishes exhaustive absence of a suitable proof. [S1–S3]

All three proof-oriented results identify the desk’s unresolved cases as two flags with no overlap, rectangles beyond two by two, and factors with variables on both sides. S2 and S3 did not have the underlying ten-case split to inspect. Their reports therefore cannot certify its completeness or close its gaps. [S1–S3]

The results also report a submission constraint: only `PEqualNP.Defs` may be imported from the project and the file cap is 524,288 bytes. S2 reports `L_meta_5412` at 448,991 bytes and `L_meta_5138` at 99,932 bytes. Their sum is 548,923 bytes, exceeding the reported cap even before missing cases are added. S1 gives 610,427 bytes for those two rows plus `L_meta_5391`. This obstructs verbatim inlining of those files, not every possible compressed or different proof. [S1, S2; sum calculated from S2]

## Computational evidence and its limits

All search results below are worker-reported computations outside Lean. The search code and logs are not included, so their exhaustiveness and minimality claims are not independently certified by this write-up. They provide no substitute for the universal theorem. [S1, S3, S4]

| Source | Reported search coverage and outcome |
|---|---|
| S1 | Enumerated least circuits for `P3`, `P4`, `2K2`, `K1,3`, `P5`, the fork with edges `0-1,1-2,2-3,2-4`, `P3+K2`, and `K1,4`; respective least sizes `2, 4, 3, 3, 5, 5, 4, 4`. Every least circuit found had zero junk gates. |
| S3 | Every bipartite, four-cycle-free graph without isolated vertices on two through six vertices: respective graph counts `1, 1, 3, 4, 11`, totaling `20`; `569` least circuits and least sizes `1` through `8`. All had empty junk. |
| S4 | Reports all bipartite, four-cycle-free graphs on at most five vertices with isolates allowed, and all `11` six-vertex graphs without isolates (`6` trees, `4` forests, and `C6`), with no junk in least circuits. Its method is stated for graphs with an edge; handling of edgeless graphs is not detailed. Specific results: `P6` size `7`, `13` least circuits; `C6` size `8`, `6` least circuits. |
| S4 | On seven vertices without isolates, completed `17` of `18` graphs: `11` trees and `6` forests, all with empty junk in least circuits. `P7` has reported size `8` and `3` least circuits. `C6` with a pendant edge remained unfinished: size `8` was exhausted, while size `9` was too long. |

S4’s method uses truth tables and iterative deepening, pruning circuits that admit deletions or rewiring, and selecting representatives under reordering of independent gates. These pruning and symmetry claims are part of its unverified computational account. The overlapping S1/S3/S4 searches are not disjoint datasets and their circuit counts must not be added. S4’s closing phrase suggesting no two-junk least circuit exists “up to 7 vertices” overstates its completed coverage; the seven-vertex pendant-cycle case remains unresolved in its own results. [S1, S3, S4]

S4 also reports a useful example outside the bipartite hypotheses: the bull graph with edges `0-1, 0-2, 1-2, 0-4, 1-3`. It reports least size `6`, after exhausting size `5`, and `13` least circuits, including:

```text
g0 = OR(x0, x1)
g1 = OR(x0, x3)
g2 = OR(x1, x4)
g3 = AND(g1, g2)
g4 = OR(x2, g3)
g5 = AND(g0, g4)
output = g5
```

S4 expands the output to the graph function `x0x2 ∨ x1x2 ∨ x0x1 ∨ x0x4 ∨ x1x3`. Gate `g3` accepts the non-edge input `{3,4}` and is false at every one-hot input. The claimed leastness depends on the undelivered enumeration. The graph has a triangle, so this is not a counterexample to L-meta-5126; it illustrates why the first rung cannot simply discard bipartiteness. S4 reports this as the only graph with a junk gate among its completed searches without isolates on at most five vertices, with `K5` unfinished. Its suggestion that a proof must use coloring at one particular shared-OR configuration is a proposed explanation, not a demonstrated necessity for every proof strategy. [S4]

## Revision finding and disposition

Finding `831ac437336e0a79751295b9174320a95e2a4c61915adacc591e372532f2f9e0` says the prior report did not deliver the proved theorem, second-holder check, or PR. The underlying evidence gap is confirmed by S1–S4. However, the cited prior report was absent from this revision checkout, so its exact wording, line numbers, and reported SHA-256 were not reproduced. The finding’s public-repository checks are reviewer assertions and were not independently rerun here.

The finding is disputed as a demand to repair those missing goal outcomes within this bounded write-up assignment. The assignment requires synthesis of the four supplied results into this report and requires that unavailable evidence be identified. None of those results provides the completed theorem that could be checked and submitted. Treating their admitted core claim as a proof, attributing a check to another holder without a record, or inventing a PR would misrepresent the sources. The overall proof goal remains unfulfilled on the supplied evidence. [Assignment; S1–S4]

For that overall goal to be established, the evidence still needed is a completed sorry-free source for the posted statement, a second-holder check tied to that exact source, and the resulting contributor PR URL. The inputs’ proposed next mathematical work is a formal gate-replacement lemma, normalization preserving one-hot falseness or a route avoiding it, and proofs of the remaining multi-edge cases. Those are outstanding proof tasks, not completed deliverables of these results. [Goal and revision finding; S1–S3]
