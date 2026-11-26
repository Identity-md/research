# L-meta-9809: merged status

## Result and goal status

The supplied results do **not** establish the requested step. No result contains a
Lean 4 theorem proving `HasCircuitSize 14 f 24`; no result contains an independent
check by another holder's machine; and no result contains a pull-request URL on
`open-goat/pequalnp-proofs`. Consequently this report does not claim that the goal
has been completed. (Sources: `item-angle-1`, `item-angle-2`, `item-angle-3`, and
`item-angle-4`.)

The reported finding that these three deliverables remain absent is reproducible
from the supplied material. The results consistently say that no 24-gate circuit
was found and that the question was not settled. In particular, item-angle-1
explicitly says that it has no 24-gate witness or refutation; item-angle-2 says
that whether one exists stays open; item-angle-3 says neither direction was
proved; and item-angle-4 calls its evidence heuristic rather than a proof.

## Function and established figures

The target is described as the edge function of a bipartite graph with inputs
`0..6` on one side and `7..13` on the other. It has 19 edges, no 4-cycle (girth
6), and minimum vertex-cover size 7. The graph is described as the Heawood/Fano
incidence graph with edges `0-7` and `1-9` removed. These structural facts are
reported by all four items, with item-angle-1 additionally giving the two
minimum covers as the two sides of the bipartition. (Sources: `item-angle-1`,
`item-angle-2`, `item-angle-3`, `item-angle-4`.)

The requested bound is 24 gates. The available construction has 25 gates, namely
`19 + 7 - 1 = 25`. Item-angle-1 and item-angle-3 report that the explicit
25-gate construction was checked in Lean in scratch work; item-angle-2 and
item-angle-4 report exhaustive truth-table agreement for the construction. This
is an upper bound of 25, not the requested 24-gate result. (Sources:
`item-angle-1`, `item-angle-2`, `item-angle-3`, `item-angle-4`.)

The explicit 25-gate sequence reported by item-angle-1 is, in gate order,
`or(8,10)`, `and(0,14)`, `or(7,13)`, `and(1,16)`, `or(8,12)`,
`or(18,13)`, `and(2,19)`, `or(7,11)`, `or(21,12)`, `and(3,22)`,
`or(10,11)`, `or(24,13)`, `and(4,25)`, `or(9,10)`, `or(27,12)`,
`and(5,28)`, `or(8,9)`, `or(30,11)`, `and(6,31)`, `or(15,17)`,
`or(33,20)`, `or(34,23)`, `or(35,26)`, `or(36,29)`, `or(37,32)`,
with output wire 38. Item-angle-3 gives the same sequence in bracket notation.
Item-angle-1 and item-angle-3 say this was checked in Lean scratch work, whereas
item-angle-2 says its 25-gate construction was not put through Lean; this is a
difference in the reported checking scope, not evidence of a 24-gate proof.
(Sources: `item-angle-1`, `item-angle-2`, `item-angle-3`.)

The truth table has `2^14 = 16384` inputs. Item-angle-4 reports 552 false inputs
for the target function. That figure is not evidence for either the 24-gate
claim or its negation. (Source: `item-angle-4`.)

## Search and proof evidence

The supplied searches did not produce a 24-gate circuit. They include SAT and
heuristic searches, but their negative outcomes are explicitly described as
inconclusive: some controls failed to rediscover known circuits, some runs timed
out, and circuits with NOT gates were not covered by all searches. Item-angle-4
reports 64 random and 51 one-gate-removed anneals without an exact 24-gate
result, while noting that this cannot exclude a rare circuit. (Sources:
`item-angle-2`, `item-angle-3`, `item-angle-4`.)

The single-level star-count argument reaches 25 gates because the graph has no
4-cycle and cover size 7. The items agree that this argument covers only that
restricted circuit shape; they do not formalize the required reduction from all
fan-in-two AND/OR/NOT circuits to that shape. Therefore it is not a lower-bound
proof for the target. (Sources: `item-angle-1`, `item-angle-3`, `item-angle-4`.)

The project the items inspected contains related lower-bound theorems, but the
reported scans do not contain a theorem deciding this 14-input, 24-gate case.
The cited related results and their applicability limits are evidence about
context only, not a proof of L-meta-9809. (Sources: `item-angle-1`,
`item-angle-2`, `item-angle-3`, `item-angle-4`.)

## Missing commissioned deliverables

The merged results provide no Lean source file for a 24-gate witness, no checked
negation/lower-bound certificate, no independent second-holder verification, and
no contributor-account pull-request URL. The only Lean evidence reported is
scratch verification of the 25-gate upper bound (items 1 and 3). The requested
proof contribution, independent check, and PR therefore remain unresolved; the
available evidence should not be presented as completion of the public proof
effort. (Sources: `item-angle-1`, `item-angle-2`, `item-angle-3`, `item-angle-4`.)

## Source record

All claims above are merged from the four supplied result records, not from web
pages or an independently inspected repository:

- `artifacts/goal/items/angle-1/result.json` (`item-angle-1`)
- `artifacts/goal/items/angle-2/result.json` (`item-angle-2`)
- `artifacts/goal/items/angle-3/result.json` (`item-angle-3`)
- `artifacts/goal/items/angle-4/result.json` (`item-angle-4`)

