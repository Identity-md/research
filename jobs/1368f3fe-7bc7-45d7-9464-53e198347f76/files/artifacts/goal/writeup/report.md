# L-meta-3241: consolidated proof-status report

The supplied results do **not establish the goal**. All four return `missing_lemma`; none supplies a Lean proof of L-meta-3241, and none reports a counterexample. The materials contain no evidence of another holder's verification of a completed theorem or of a pull request submitted from the proving contributor's account. This report consolidates the findings and the remaining proof obligation; it is not a theorem submission or a verification certificate. [S1–S4]

## Statement and mathematical content

The results interpret the step as follows. Let G be a bipartite graph with edge relation E and no 4-cycle. Its Boolean edge function is

`f_G(x) = OR_{uv ∈ E} (x_u AND x_v)`.

The project's `IsAO2` model permits only AND and OR gates, each reading exactly two earlier wires, with no constants or NOT gates. Circuit size counts gates. The requested conclusion is an exact star cover of E whose cost is at most the circuit size. Each star has a centre and a nonempty list of leaves; its contribution to the total construction is captured by

`cost = (sum of leaf counts) + (number of stars) - 1`.

For nonempty E the minimum cost is `|E| + τ(G) - 1`, where τ is the minimum vertex-cover size. The centres of any exact star cover cover E, and the leaf occurrences account for every edge; conversely, assigning each edge to a covering endpoint gives the matching upper bound. For bipartite G, König's theorem identifies τ with the maximum matching size ν. Thus the substantive target is the lower bound

`C.size ≥ |E| + ν(G) - 1`.

For empty E, the empty star list costs zero because subtraction is truncated in the natural numbers. The nonempty formula should not be read as ordinary integer subtraction in this case. [S1–S4]

S4 reports checking the interpretation against empty sides, isolated vertices, missing output wires, and output on an input wire, without finding a loophole that settles the general statement. These are reported observations, not a supplied formal proof. [S4]

## Remaining proof obligation and available reduction

S2 and S3 identify the following charge inequality as the central missing lemma:

> For `E M : Finset (Fin n × Fin m)`, if E is 4-cycle-free, C is an `IsAO2 (n+m)` circuit computing E's edge function, and `M ⊆ E` is a matching, then
> `E.card + M.card ≤ C.size + 1`.

S2 describes `R_meta_3241_917` as a reduction from two hypotheses: this `charge` inequality and a `stars` construction assigning edges to endpoints in a vertex cover. It also reports that the reduction already contains the needed matching/cover argument. S2 does not prove the stars helper itself. [S2]

S3 provides the more specific finding: in the project snapshot it identifies as `e125f04`, `L_meta_3519` already proves `stars`. It reports checking a conditional composition of the bodies of `L_meta_3519` and `R_meta_3241_917`, schematically:

```lean
-- Conditional composition reported by S3, not a complete theorem proof.
theorem chk (charge : ...) : <step statement> :=
  PEqualNP.Outside.R_meta_3241_917 charge PEqualNP.Outside.L_meta_3519
```

The ellipses above are explanatory notation, not executable Lean. S3 reports successful elaboration with axioms `propext`, `Classical.choice`, and `Quot.sound`. The result payload contains neither the scratch file nor its checking output. In particular, the composition assumes `charge`; it does not discharge it. [S3]

This resolves the apparent difference between S2's “charge plus stars” accounting and S3's “charge only” accounting: S3 identifies an existing stars proof that S2 did not supply. It does not resolve the mathematical lower bound. S1 and S4 approach the same obstacle directly rather than through the reduction. [S1–S4]

S3 also identifies restricted results: `L_meta_4897` under `IsReadK 1`, and `L_meta_7241` in a SimpleGraph/NoFourCycle formulation when every AND gate is false on each non-edge pair input. These restrictions do not cover arbitrary circuits. Its proposed bridge is that a size-minimal circuit has no “junk” AND gate, meaning one accepting a non-edge pair or a singleton input. That bridge is explicitly unproved. The theorem bodies and translations needed to apply these results are not supplied. [S3]

The results describe an original restriction to `PEqualNP.Defs`; S1 calls that module definitions-only, and S4 notes that auxiliary facts would have to be reproduced inside the submission under that restriction. Consequently, even accepting S3's conditional reduction as reported does not establish an admissible completed submission. [S1, S4]

## Reported finite-search evidence

The following preserves the scope of each source separately. The search programs, enumerated graph lists, and logs are not delivered in the result payloads. The counts are source reports, not reproduced results, and overlapping counts must not be added as independent evidence. [S1–S4]

| Source | Through seven vertices | Eight vertices | Additional detail |
|---|---|---|---|
| S1 | 40 graphs up to isomorphism without isolated vertices; minimum equals the bound in each case. For one seven-vertex graph, exclusion below the bound was combined with a star construction. | 52 graphs considered; 39 settled at the bound. For the remaining 13, all with parts of size four, only sizes through eight were excluded; target bounds were 10–12. | No counterexample reported. |
| S2 | All 40 graphs with at most seven vertices excluded smaller circuits; exact-size circuits were also found for all 21 graphs with at most six vertices. | Seven graphs with parts `(1,7)` or `(2,6)` fully checked. Of 20 with parts `(3,5)`, nine fully checked and 11 hit a node limit. Parts `(4,4)` were not run. | No smaller circuit found in the unfinished searches. |
| S3 | 21 graphs through six vertices and 19 on seven vertices settled at the bound. For one seven-edge graph on parts `(3,4)`, exclusion through size eight plus a star circuit establishes size nine. | 52 graphs; 39 settled and 13 unfinished, with bounds 10–12 and only sizes through eight excluded. | Reports enumerating all minimum circuits for 39 of the 40 graphs through seven vertices: 1,864 circuits up to gate order, none with a junk AND gate. The remaining graph's enumeration did not finish. |
| S4 | 21 isomorphism classes through six vertices settled exactly; 69 seven-vertex instances, including isomorphic repeats, excluded smaller circuits. | Only 109 tree instances with seven edges finished within a 400-second limit. The eight-cycle and the eight- and nine-edge graphs on parts `(4,4)` were not reached. | Reports agreement with unpruned searches through five vertices and with the ordering rule disabled at six vertices. |

Every row is sourced to its corresponding item. The differing eight-vertex coverage is not a contradiction: the sources describe differently bounded searches. Likewise, S4's 69 seven-vertex instances include repeats and are not a claim of 69 isomorphism classes. S1 and S3 give matching headline totals, but the supplied material does not establish independent reproduction. Finite searches cannot prove the unrestricted theorem or the proposed minimal-circuit bridge. [S1–S4]

## Obstacles and useful examples

- **The 4-cycle-free condition matters.** S1 gives `K_{2,2}` as a counterexample to dropping it: `(u1 OR u2) AND (v1 OR v2)` uses three gates, whereas its star-cover cost is `4 + 2 - 1 = 5`. This is not a counterexample to the requested theorem. [S1]
- **A minimum circuit need not have star form.** For the path with edges `ab, bc, cd`, `(a OR c) AND (b OR (c AND d))` uses four gates, equal to the target, while nesting an AND beneath another AND's input cone. Normalizing all circuits to stars therefore requires a size-preservation argument; merely assuming the desired form is insufficient. [S1, S3]
- **Junk gates can occur in nonminimal circuits.** S3 gives `(a1 OR a2) AND (b1 OR b2) AND (a2 OR b1)` for the path `a1-b1-a2-b2`. It uses five gates against a bound of four. This motivates a claim about minimal circuits rather than all circuits. [S3]
- **Essential-input counting is weaker.** The sources obtain the elementary bound `C.size ≥ n' - 1`, with n' the number of non-isolated vertices. The desired improvement is `|E| + τ(G) - n'`; counting inputs alone does not supply it. [S1, S2]
- **Simple deletion need not recover the whole target decrement.** S4's eight-gate six-cycle circuit is `v1(u1 OR u2) OR v2(u2 OR u3) OR v3(u3 OR u1)`. Setting `u1 = 0` removes two gates by direct simplification, while the resulting path has target cost five, three below eight. Further restructuring is needed for this induction strategy. [S4]

S1, S2, and S4 report that their limited literature searches found no proof of the exact bound; this does not establish that no proof exists. S1 and S2 mention Jukna's *Disproving the single level conjecture*, ECCC TR05-021, as a caution about general quadratic functions. Their payloads do not include the cited source passages or URLs, so that literature claim is not used here as an independently verified premise. [S1, S2, S4]

S3 reports that its upstream snapshot, identified as `bf7e3efb` on 2026-11-25, had no `L_meta_3241`. It further reports examining 2,400 Outside files newer than the prebuilt tree: one mentioned `IsAO2` (`L_meta_5857`, for a fixed 11-vertex graph), and none had the shape of `charge`. This is an attributed snapshot observation, not a current repository audit. The named public repository is [open-goat/pequalnp-proofs](https://github.com/open-goat/pequalnp-proofs). [S3]

## What remains to complete the goal

A complete Lean proof of `charge`, or another argument establishing the same unrestricted lower bound, is still needed. S3's proposed minimal-circuit lemma and S1's suggested narrower forest or block subproblems are possible research directions, not proven substitutes for L-meta-3241. The reported reduction and star helper may support a future proof, subject to the actual submission constraints. [S1–S3]

The requested delivery sequence also remains unsupported: there is no completed theorem artifact, independent holder verification record, or submitted pull-request URL in any input. No contributor-account attribution can be established from these results. Accordingly, the defensible disposition is **unproved / missing lemma**, not proved, refuted, independently checked, or submitted. [S1–S4; task goal]

## Source record

The four inputs each contain a `status` and a prose `notes` field. Their SHA-256 hashes were checked against the task-supplied hashes when preparing this report and matched. The records below identify the evidence even if the input files are not included with the delivered report; the substantive findings needed to understand the outcome are retained above. Repository claims, search counts, and prior checking claims remain attributed to these records.

| ID | Supplied input | Logical result path | SHA-256 |
|---|---|---|---|
| S1 | `.imd/reads/artifacts/item-angle-1` | `artifacts/goal/items/angle-1/result.json` | `52051376e1d876eb1d4f059b121b78b75237a3e752ea9bae138f9c8b2605e900` |
| S2 | `.imd/reads/artifacts/item-angle-2` | `artifacts/goal/items/angle-2/result.json` | `84c7b01a9d474de6bd1e69399346277d155852b6bda5ac25548d03fc149a2baf` |
| S3 | `.imd/reads/artifacts/item-angle-3` | `artifacts/goal/items/angle-3/result.json` | `0f0e0d629569595513069eeb944f6af128f249e2991f936aa134f0f9b25d58f8` |
| S4 | `.imd/reads/artifacts/item-angle-4` | `artifacts/goal/items/angle-4/result.json` | `11f862532e60321b1a47bdafcfdc2c78f857cb75ace0787736335c55100d3755` |

No external page, Lean source, search implementation, or pull request was supplied as part of these four JSON records. This write-up validates the supplied records' integrity and synthesizes their content; it does not independently certify their mathematical or computational claims.
