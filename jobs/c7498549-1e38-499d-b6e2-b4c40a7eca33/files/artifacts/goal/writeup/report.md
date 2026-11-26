# L-meta-4649 — proof outstanding

All four results report `missing_lemma`. The strongest construction reaches the target in **28 gates**. The required theorem says **every allowed circuit with at most 27 gates misses the target**. That claim remains unproved in the supplied results. The records contain no completed Lean 4 theorem, no check of such a theorem by another holder, and no contributor pull request for `open-goat/pequalnp-proofs`. Angles 1 and 2 report that Lean accepted the statement with a placeholder proof. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

## The claim a proof must establish

The 14 input wires represent the seven points and seven lines of the Fano plane. Call the point inputs `x_0` through `x_6` and the line inputs `y_7` through `y_13`. In point order, the triples of incident line indices are `(7,11,13) (7,8,12) (8,9,13) (7,9,10) (8,10,11) (9,11,12) (10,12,13)`. Bits 0–20 test the 21 incident pairs. Bits 21–57 test the 37 maximal independent sets of the incidence graph. The target has value `2097151`, with just bits 0–20 set. Monotonicity forces the output on every assignment. An assignment containing an edge contains a tested positive pair. An assignment containing no edge lies inside a tested negative set. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3]

Bits 58 and 59 evaluate a wire with only input 0 or only input 7 on, respectively. Bit 60 tracks input 7 at the first assignment, and bit 61 tracks input 0 at the second. In each pair `(58,60)` and `(59,61)`, write the bits as `(v,d)`. OR acts componentwise. AND takes operands `(v,d)` and `(w,e)` to `(v AND w, (v AND e) OR (d AND w))`. The target requires zero in all four positions. Gates use distinct earlier wires, and the first gate is an OR. The obligation applies to **any gate** in a list of at most 27 gates. Whenever it matches the target on bits 0–59, bit 60 or bit 61 must be set. [Angle 1][a1] · [Angle 3][a3] · [Angle 4][a4]

## What the circuit evaluations establish

| Construction | Gates | Output compared with the target | Source |
|---|---:|---|---|
| One star per point, or one per line | 27 | Each orientation matches bits 0–59. Both have bits 60 and 61 set. | [Angle 3][a3] |
| Point stars with the term for point 0 combined with the term for point 2 as described below | 28 | Matches all 62 bits. | [Angle 4][a4] |
| Duplicate the final OR of a star circuit and AND the two output wires | 29 | Matches all 62 bits. | [Angle 2][a2] |

For the point-star construction, let `s_i` be the OR of the three lines incident to point `i`, and let `g_i = x_i AND s_i`. Computing the seven sums costs 14 OR gates, forming the seven terms costs seven AND gates, and joining them costs six OR gates. The 28-gate witness replaces the two gates that form `g_2` and join it to `g_0` with three gates computing `(x_2 OR g_0) AND (s_2 OR g_0)`. On ordinary bits this equals `g_2 OR g_0`. At bits 58 and 59 both operands of the new AND are zero, so its product rule clears bits 60 and 61. Joining the other five stars yields the target. [Angle 2][a2] · [Angle 4][a4]

The full witness is given below in wire order, 14 through 41. Each token gives the operation (`o` for OR, `a` for AND) and its two operand indices. Replaying this list with the rule above gives `2097151` at wire 41. This settles the 28-gate existence question left open by the earlier angles. It gives an upper bound on the minimum. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

```text
o7,11  o14,13  o7,8   o16,12  o8,9   o18,13  o7,9
o20,10 o8,10   o22,11 o9,11   o24,12 o10,12  o26,13
a0,15  a1,17   a3,21  a4,23   a5,25  a6,27   o2,28
o19,28 a34,35  o36,29 o37,30  o38,31 o39,32  o40,33
```

## Where the proof stops

The reduction `R_meta_4649_517` isolates a hypothesis named `fano`. For every allowed list of at most 27 gates on the first 60 bits, take any gate with value `2097151`. One must exhibit a path to that gate either from input 7 with the other operand of every AND on the path set at bit 58, or from input 0 with those operands set at bit 59. Such a path carries bit 60 or 61 to the gate by the product rule. The reduction also takes a reachability hypothesis named `paths`. The reported reductions by final gate (`R_meta_4649_671`) and first OR (`R_meta_4649_1`) also leave cases to prove. [Angle 1][a1] · [Angle 3][a3] · [Angle 4][a4]

Angle 3 reports that `L_meta_971` proves a 27-gate lower bound for the **ordinary** Boolean function under a different labelling. Transferring it would exclude a target computed using at most 26 gates. Angle 3 also reports that `L_meta_3793` covers circuits with at most 27 gates and no repeated gate reference. For each edge, at least one endpoint is read at most once. The proposed route would use this property for edge (0,7) to obtain a path. If all 27 gates feed the output, the 26 other gates each occupy at least one of the 54 slots, leaving at most 28 input reads. A shared gate uses another slot. Proving that at least 28 input reads are necessary would rule out sharing and allow the tree-case argument to apply. That lower bound on reads is a proposed lemma. Neither the counting identity nor the two star examples establish it. [Angle 2][a2] · [Angle 3][a3]

Angle 3 tested 124800 two-gate extensions of one fixed 26-gate prefix and found that all missed the target. Angle 4 reports unsatisfiability after fixing all 14 gates for the neighbour sums and either six particular star products or one of two particular sets of five. Those exclusions depend on the fixed gates. Angle 4’s unrestricted 27-gate search returned no answer. Angle 2 also reports timeouts at sizes for which witnesses are known. [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

## Source records

The four supplied JSON records are identified by their SHA-256 digests.

| Record | SHA-256 |
|---|---|
| [Angle 1][a1] | `c2da6758a2b7c519e3b733be5cc23af8804c67fb60443235f7570c1b7074689a` |
| [Angle 2][a2] | `dfd9d899ad813b0cb3523ce40516449dfe00835c64b2efc61cc30568dd99e559` |
| [Angle 3][a3] | `6ebc5f87680f6707263f247452014b02a8eb05eaeacd7b8a7a4701a4dbd8b2c9` |
| [Angle 4][a4] | `73fb6b35a79e570d21a1018979711d79ff84afd944f82d7f15627f50f6a4ef0d` |

[a1]: ../items/angle-1/result.json
[a2]: ../items/angle-2/result.json
[a3]: ../items/angle-3/result.json
[a4]: ../items/angle-4/result.json
