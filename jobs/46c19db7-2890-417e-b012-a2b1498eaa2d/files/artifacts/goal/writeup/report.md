# L-meta-9763: write-up of the four supplied results

**Disposition: unsolved.** The four supplied results contain no Lean 4 proof of L-meta-9763. None reports a successful check by another holder's machine or identifies a pull request from the proving contributor. This report therefore documents a tight **upper bound** and the missing lower bound; it does not claim that the goal job has been completed. [A1–A4]

## Statement and established calculation

The results describe L-meta-9763 as asserting that the specified 25-input Boolean edge function has **no** fan-in-two AND/OR/NOT circuit of at most 58 gates, with NOT gates counted. They do not supply the exact posted Lean declaration, so this is a description of the statement, not a replacement for it. [A1–A4]

Write the point inputs as `x0` through `x12` and the retained line inputs as `x13` through `x24`. For `0 ≤ j < 12`, point `i` is incident to line `13+j` when `(j-i) mod 13` belongs to `{3, 9, 11, 12}`. The function is the OR of `x_i AND x_(13+j)` over these incidences. The thirteenth line, `j=12`, is omitted. This is the order-three projective-plane incidence graph with one line removed. [A1–A4]

| Property | Result | Sources |
| --- | --- | --- |
| Vertices and terms | 13 point inputs, 12 line inputs, 48 distinct edges/products | [A1–A4] |
| Degrees | Each retained line has degree 4; points 0, 1, 3, and 9 have degree 3; the other nine points have degree 4 | [A1–A4] |
| Short cycles | Two retained lines share exactly one point; there is no four-cycle and six-cycles exist | [A1–A4] |
| Matching and cover | Maximum matching and minimum vertex cover both have size 12 | [A1–A4] |

The cover claim also follows directly from the described graph: all 12 line vertices cover every edge, and a matching of 12 edges forces any cover to contain at least 12 vertices. The four results report these quantities; I independently recalculated the edge count, degrees, line intersections, and matching from the incidence rule for this write-up. [A1–A4]

**A 59-gate circuit exists.** For each of the 12 retained lines, OR its four incident point inputs using three binary OR gates, then AND that result with the line input using one gate. OR the 12 line terms with 11 further binary OR gates. Thus the count is `12 × (3 + 1) + 11 = 59`, also `48 + 12 − 1`. All four contributors report checking that this circuit computes the stated function on all `2^25` assignments. That is their reported exhaustive check, not a Lean kernel check of a lower bound. [A1–A4]

Consequently the proposed theorem is tight **if true**: it must exclude every circuit with at most 58 gates, including circuits that share intermediate computations across terms and circuits using NOT. The 59-gate construction cannot establish that exclusion. [A1–A4]

## Why the supplied arguments stop short

**Single-level star circuits.** A circuit formed by assigning edges to covering vertices, computing one star at each selected centre, and ORing the stars costs at least `|E| + τ(G) − 1 = 59` gates. The contributors also reason that the absence of four-cycles prevents useful sharing of an OR of two leaves between distinct stars. This only addresses that restricted circuit shape. It does not rule out deeper sharing, absorbed terms, or NOT-using circuits, so it is not the required lower bound. [A1, A2, A3, A4]

**Restriction or gate elimination.** Fixing a line input to false removes four graph edges and can reduce the cover number from 12 to 11. Relative to the `|E| + τ − 1` target, an induction through such a restriction needs five gates to disappear. Fixing a point removes three or four edges while the cover may remain 12. The workers found no lemma ensuring the needed gate loss for *every* AND/OR/NOT circuit: a variable can feed a single gate, and the ordinary local argument they considered gives only about one or two gates. Angle 3 states the needed stronger elimination claim as an **unproved candidate**, not an established theorem. [A1–A4]

**Available precedents.** The workers report that the general lower-bound tools they examined have hypotheses that do not cover this graph: the forest result L104, the high-girth and separated-high-degree result L204, and the maximum-degree-three/peeling route discussed with L658. Angle 3 mentions L532's `Peelable` condition but could not read its definition, so whether it applies was **not checked**. Angle 2 reports monotone-circuit results for smaller Heawood-related graphs, L_meta_971 and L_meta_9730, but those do not settle a statement allowing counted NOT gates; it also reports that the NOT-removal result L113 needs larger girth. These are contributors' readings of project material, not a formal derivation for L-meta-9763. [A1, A2, A3]

**Finite certificates and related instances.** The workers found no 58-gate counterexample and no exhaustive lower-bound certificate for 25 inputs and 58 gates. They describe existing fixed-graph certificate examples on roughly 9–11 inputs and much smaller bounds as already close to a one-file size limit; no result supplies a certificate that scales to this step. Angle 4 reports small-case SAT synthesis and several unfinished searches, all explicitly non-decisive for this graph. Angle 2 suggests deriving the result from a stronger full-plane statement, but reports no such result in the general circuit model. Angle 1 reports a survey of small fixed-graph rows as suggestive evidence only. None of these observations proves or refutes L-meta-9763. [A1–A4]

## Verification and disagreements in the inputs

| Question | What the supplied results establish | Sources |
| --- | --- | --- |
| Lean theorem file | No contributor supplied one | [A1–A4] |
| Lean elaboration | Angle 1 says the bare statement skeleton elaborated; angle 2 says no proof candidate was elaborated; angle 3 says Lean could not be run in that session. No result reports elaboration of a proof. | [A1, A2, A3] |
| Independent holder check | No successful check of a proof is reported | [A1–A4] |
| Contributor pull request | No PR for a proved and checked L-meta-9763 is identified | [A1–A4] |
| Existing certificate size | The sources disagree on the byte size of L_meta_9818: angle 1 says 522,167 bytes, while angle 4 says 515,811 bytes. No exact size is used as a conclusion here. | [A1, A4] |

The reported 59-gate upper bound is useful progress, but the goal requires a Lean theorem excluding 58 gates, an independent check of that theorem, and then the specified contributor PR. The four supplied results establish none of those three deliverables. The exact Lean statement, a proof file, a check record, a PR link, and a contributor account are not present in the supplied results; this write-up cannot identify or manufacture them. [A1–A4; goal brief]

## Source key

All four inputs were supplied as JSON result files under `.imd/reads/artifacts/`. Citations above refer to those records, not to a Lean proof. The SHA-256 values identify the exact supplied content. [A1–A4]

- **A1:** `.imd/reads/artifacts/item-angle-1` (`artifacts/goal/items/angle-1/result.json`), SHA-256 `1f34ea100ba2f64f54c8e8a8482fcf71d27ffcf82057ec04a25e099e61ef4a0d`.
- **A2:** `.imd/reads/artifacts/item-angle-2` (`artifacts/goal/items/angle-2/result.json`), SHA-256 `0196b66c1875f5759284eeaabd89fc1c7258a4a9bd720bdb7d3575370af1cdbf`.
- **A3:** `.imd/reads/artifacts/item-angle-3` (`artifacts/goal/items/angle-3/result.json`), SHA-256 `f8e1c213263caaac498bb7a7eeb88e1537af8298b34ff337d7eb32a8014fe89d`.
- **A4:** `.imd/reads/artifacts/item-angle-4` (`artifacts/goal/items/angle-4/result.json`), SHA-256 `54a8dbc018dd21f6869bcab76652cc7cf000da5a5438843f29a5fe4a95bf2175`.
