# L-meta-2704: consolidated result and completion status

The supplied results do **not** establish L-meta-2704. All four return `missing_lemma`, offer no complete Lean theorem, and contain no independent holder’s check or contributor pull-request evidence. This report is the requested synthesis of those results, not a proof certificate or a claim that the public proof goal is complete. [S1–S4]

The goal supplied in the assignment is a Lean 4 theorem for L-meta-2704, checked on another holder’s machine and then opened as a pull request on `open-goat/pequalnp-proofs` by the proving contributor. None of those three completion artifacts can be recovered from these inputs. [Assignment; S1–S4]

## Sources and evidence limits

The source labels below refer to the supplied JSON results. Their original artifact paths and exact SHA-256 digests are recorded because the assignment says the input files are not delivered with this report. Links identify the supplied local sources; they are not public proof records.

| Label | Supplied source | Original artifact path | SHA-256 |
|---|---|---|---|
| S1 | [item-angle-1](../../../.imd/reads/artifacts/item-angle-1) | `artifacts/goal/items/angle-1/result.json` | `0743e76462e9effee1d008bb34a72122706f49e108c82414f335188f8f22f99e` |
| S2 | [item-angle-2](../../../.imd/reads/artifacts/item-angle-2) | `artifacts/goal/items/angle-2/result.json` | `e692f65bad46bd34c518093a512b2416f96ffe64c1dd62afb5e9ad6a9420d25d` |
| S3 | [item-angle-3](../../../.imd/reads/artifacts/item-angle-3) | `artifacts/goal/items/angle-3/result.json` | `3fc79868d17c822d2527858380b2b932aafc8ff14a2f3859a68a16185f93b2bc` |
| S4 | [item-angle-4](../../../.imd/reads/artifacts/item-angle-4) | `artifacts/goal/items/angle-4/result.json` | `874ff26511aca28bc0f1e11e5550d7291b3933b2dabe76cb8472f335d4e60b90` |

All four hashes were verified against the assignment, and each original-path copy matched its corresponding supplied input byte for byte. All four JSON documents parsed with status `missing_lemma`. These are local document-integrity checks, not independent verification of mathematics.

The sources describe repository lemmas, scratch Lean checks, enumeration, and unsuccessful searches. They supply neither the scratch proof files nor complete check transcripts. References below to project lemmas describe what the sources report; their implementations were not available in these inputs for re-elaboration. No public source URL for an actual theorem submission or check is supplied. [S1–S4]

## Mathematical content recovered

Use the sources’ notation: `U = Ustar G C`, `r = |U|`, `c = |centreless|`, `o = |orN \\ lam|`, `k = 2c + o`, `t = |tops \\ centreless|`, and `tau` the minimum vertex-cover size of `G.deleteEdges U`. Here `\\` denotes set difference. Let `HYP` abbreviate the stated graph, least-AO, top-form and size hypotheses, together with exactly two junk gates nested by `InCone`. [S1–S4]

The graph is on `Fin 11`, with edges

```text
(0,9), (0,10), (1,4), (1,8), (2,5), (2,10), (3,6), (3,7),
(4,8), (4,10), (5,8), (5,9), (6,7), (6,10), (7,9), (8,9).
```

This edge list is supplied in S3’s proposed `bill` statement. S2 and S4 report that it has 16 edges, no four-cycle, and vertex-cover number 7. Their cover construction uses `16 + 7 - 1 = 22` gates. These graph computations do not establish the required circuit lower bound. [S2, S3, S4]

The central shared reduction is:

```text
Requested conclusion, minimized over admissible x13:  5 + r <= tau + k
Available circuit/cover accounting under HYP:         tau + k <= 4 + r
```

The first inequality uses the relationship between the step’s `x13`, `x16`, `x17` expression and vertex covers. The second uses the size bound, two distinct junk gates, and a bound `tau <= t`. Together they contradict one another. Thus, conditional on the cited accounting and cover facts, the step is equivalent to the non-existence of a least top-form circuit of size at most 21 for this graph with exactly two nested junk gates. That equivalence is a reduction of the problem, not its solution. [S1, “CHECKED 3”; S2, “Why that is non-existence”; S3, “nec”; S4, item 2]

The sources cite different accounting lemmas: S1 and S2 cite `L_meta_7862`, S3 cites `L_meta_5781`, and S4 cites `L_meta_1491`. They report compatible inequalities, but this write-up does not certify those lemmas as interchangeable. S1–S3 report selected Lean checks with required project statements supplied as hypotheses; S4 explicitly calls its corresponding argument a paper derivation using enumeration. [S1–S4]

The common profile is

```text
r:     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
b(r):  0  0  2  4  5  7  8  9 11 12 13 14 16 17 18 19 21
```

S1 and S3 report that `L_meta_6103` and the cover construction suffice whenever `b(r) <= k`. The missing implication is that `HYP` cannot hold with `k < b(r)`. S3 calls the bound `b(r) <= k` under `HYP` the proposed lemma `bill`; it is unproved in that result. [S1, “CHECKED 1”; S3, “suff”]

S2 reports the minimum of `tau(G - U)` over edge sets with `|U| = r` as

```text
7, 6, 5, 4, 4, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 0.
```

S4 reports the corresponding maximum of `5 + r - tau(G - U)` as

```text
-2, 0, 2, 4, 5, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18, 19, 21.
```

These lists agree with `b(r)` for `r >= 1`. At `r = 0`, the profile entry 0 is weaker than the reported maximum -2; it is not an equality there. S4 reports zero mismatches between the cover number and the minimized step expression over 65,536 edge subsets. These are reported Python enumeration results, not delivered Lean certificates. [S2, “Graph facts”; S4, item 1]

## Case coverage and remaining gap

| Case | Strongest supported status | Source |
|---|---|---|
| `r <= 1` | Profile sufficiency is reported checked conditionally; counting also excludes these circuit cases. | S1, CHECKED 1; S2; S4, item 3 |
| `r = 2`, `k < b(r)` | Reported reduction to `k = 1`, size 21, `t = tau = 5`, and `c = 0`. S1 still lacks two bridges into `L_meta_5226`: disjointness of the two Ustar edges and a top-operand OR-reachability witness to the specified gate. | S1, missing case (a); S2; S4 |
| `r = 3` | S1 reports a Lean-checked contradiction conditional on copied statements of `L_meta_6103`, `7862`, `1490`, `5228`, `8005`, and `inCone_lt`. Other sources leave side hypotheses to be derived. No complete proof file is supplied. | S1, CHECKED 2; S2–S4 |
| `r >= 4`, `k = 1` | Sources report exclusion using the rigid shape from `L_meta_7895` and the bound `r <= 3` from `L_meta_7897`. No assembled proof is delivered. | S1–S4 |
| `r >= 4`, `2 <= k < b(r)` | Open in all four results. For `r = 4`, `b(4) = 5`, so `k = 2, 3, 4` remain within this range. | S1, missing case (b); S2–S4 |

The difference over `r = 3` is evidence granularity: S1 claims a conditional assembly check beyond the statement-level observations of the others. It cannot be promoted into an independently checked, complete theorem. S1 also explicitly labels its discussion of the remaining cases as not Lean-checked. [S1–S4]

For the large case, the reported available bounds include `t + k <= 4 + r` and `t >= tau >= 5 + r - b(r)`. At `r = 4`, `k = 2`, these merely allow `4 <= tau <= t <= 6`. They do not yield a contradiction. This arithmetic illustrates the proof gap; it does not exhibit a circuit satisfying `HYP`. [Derived from S1’s stated bounds and profile]

S2–S4 report unresolved hypotheses in nearby reductions, including `large_uncovered` in `R_meta_5182_1`, `many` in `R_meta_2260_2`, and `budget`/`larger` in `R_meta_5184_376`. S1 notes that `L_meta_4899`, `4901`, and `5966` instead assume non-nested junk gates. S4 says `L_meta_5242` requires girth at least 5, whereas this graph has triangles `(1,4,8)`, `(3,6,7)`, and `(5,8,9)`. These observations describe limits of the searches, not an exhaustive proof that no suitable lemma exists anywhere. [S1–S4]

## Other results and limitations

S1–S3 report scratch checks using Lean 4.36.0, without `sorry`; S3 additionally reports only `propext`, `Classical.choice`, and `Quot.sound` as axioms. Those checks concerned reductions and conditional implications, not a completed L-meta-2704. The scratch artifacts are expressly not delivered. S1 and S2 also report tool-startup difficulties; this supplies no additional mathematical evidence. [S1–S3]

The sources describe an original proof-file restriction to importing `PEqualNP.Defs` and a 524,288-byte limit. S2 reports that copying `L_meta_5228` (412,015 bytes), `L_meta_7862` (89,712 bytes), and `L_meta_7895` (49,816 bytes) already exceeds that limit. S3 reports the same obstacle for a different collection. This establishes the reported obstacle to those particular assembly strategies, not impossibility of a shorter proof. S2 and S3 suggest splitting the missing lemma into separate desk steps or allowing imports of proved modules; these are proposals, not approved changes or completed work. [S2, S3; S4 corroborates the assembly concern]

S4 reports SAT synthesis searches for 21-gate circuits, with and without nested-junk/top-form constraints, timing out at 330 seconds using `cadical153` and `glucose4`. A known-satisfiable 22-gate control also timed out. The encoding reportedly used 16 edge inputs and 24 maximal independent sets. These runs are inconclusive: no UNSAT certificate, circuit witness, or Lean proof is supplied. All four sources report neither a proof nor a counterexample; failure to find a proof is not evidence that the statement is false. [S1–S4]

## Revision finding and goal status

Finding `79599553439fa7d674ae18933d77d80c9f3bb592cc9ac98a5400a6ccc3f66c1c` correctly identifies missing goal outcomes. Its exact references to the previous report’s lines cannot be reproduced because that report was absent from the supplied checkout. Its substantive mathematical witness does reproduce: `r = 4`, `k = 2` satisfies `r >= 4` and `2 <= k < b(4) = 5`, the range S1–S4 leave unresolved. The supplied artifact directories contain the four JSON results and their copies, not a complete theorem or verification/submission record. [Local inventory and arithmetic check; S1–S4]

| Required goal outcome | Evidence in the supplied results |
|---|---|
| Complete Lean 4 theorem for L-meta-2704 | Absent; every result has status `missing_lemma`. [S1–S4] |
| Another holder’s check of that complete theorem | No check record supplied. Reported partial scratch checks do not meet this requirement. [S1–S4] |
| Ensuing contributor pull request on `open-goat/pequalnp-proofs` | No pull-request URL, contributor submission record, or checked theorem supplied. [S1–S4] |

This revision makes the incompleteness explicit. The assignment authorizes a write-up from supplied results; it does not provide the missing proof, independent-holder check, or submission evidence. Those outcomes cannot truthfully be manufactured in a synthesis. The underlying proof goal remains unfinished, and no claim of its completion is made.
