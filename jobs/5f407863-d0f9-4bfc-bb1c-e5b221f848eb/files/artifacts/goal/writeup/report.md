# pequalnp outside proof desk · L-meta-17964

**The step remains open.** All four results report `does_not_elaborate`. Lean 4.36.0 cannot form the posted proposition because two names in its statement are undefined in the prebuilt project. The results contain no Lean proof, no record of another holder checking a proof, and no contributor pull request to `open-goat/pequalnp-proofs`. The desk lists the mathematical claim as “Truth unknown.” [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

## Where Lean stops

Each result describes elaborating the exact posted statement after `import PEqualNP.Defs`. Lean reported exactly two errors, both before the proof body. The circuit type, the representation predicate and the list expressions resolved. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

| Column | Lean diagnostic |
| ---: | --- |
| 262 | Unknown identifier `PEqualNP.FoldExtra.IsFolded` |
| 573 | Unknown identifier `PEqualNP.FoldExtra.circuitExtra` |

The column positions come from [Angle 1][a1]. Searches of the imported Lean environment, project sources and compiled library found neither name in the prebuilt revision `e125f04d0dc6fed67cee48a1d06692912e167c32`. [Angle 1][a1] · [Angle 2][a2] · [Angle 4][a4] · [Prebuilt revision][prebuilt]

The reported upstream check on 2026-11-26 reached the same result at `b7a6d9a7980b25e884d3b70cee2f628d2b6ca7e1`. The only added import in the definitions root was `PEqualNP.Defs.BranchingProgram`. The similarly named `FoldCircuit.lean` and `FoldProg.lean` were helpers outside that root and defined neither identifier. Angle 4 also reports that issue and pull-request searches returned zero results for both `FoldExtra` and `L-meta-17964`. [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4] · [Upstream definitions root][upstream]

## Why the definitions matter

The proposed bound says that for a folded circuit representing the path graph, the sum of `length - 3` over the paths is at most `8 * circuitExtra n C + 2`. Angle 4 mechanically checked the path hypotheses for `n = m = 3` and `ps = [[0,3,1,4,2,5]]`. This alternating path has six distinct vertices and contributes 3. For a natural-number measure the bound would then require every folded circuit representing this graph to have `circuitExtra n C ≥ 1`. The calculation checks the path data alone. Deciding the circuit claim requires both missing definitions. The desk reports computation up to 16 vertices and gives no refutation. [Angle 1][a1] · [Angle 4][a4]

Angle 1 made the remaining statement elaborate using parameters of types `Nat → Circuit → Prop` and `Nat → Circuit → Nat`, respectively. These are compatible signatures. They supply neither the folding criterion nor the rule for computing EXTRA that the proposed induction needs when it zeros a row or column. The checker reads the recorded statement against Mathlib and `PEqualNP.Defs`, and local helpers must live in `PEqualNP.Outside.L_meta_17964`. A proof-file helper therefore cannot supply either missing name to the recorded statement. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3]

## What would unblock the proof

The desk can publish its definitions of `PEqualNP.FoldExtra.IsFolded` and `PEqualNP.FoldExtra.circuitExtra` through `PEqualNP.Defs` and rebuild the prebuilt project from that revision. Alternatively, it can restate the step using definitions already exported by that root. Either repair would make it possible to attempt the theorem. A completed proof would still need another holder’s machine check before the proving contributor opens the pull request. [Angle 1][a1] · [Angle 2][a2] · [Angle 3][a3] · [Angle 4][a4]

[a1]: ../items/angle-1/result.json
[a2]: ../items/angle-2/result.json
[a3]: ../items/angle-3/result.json
[a4]: ../items/angle-4/result.json
[prebuilt]: https://github.com/brilliant-hq/pequalnp-proofs/tree/e125f04d0dc6fed67cee48a1d06692912e167c32
[upstream]: https://github.com/open-goat/pequalnp-proofs/blob/b7a6d9a7980b25e884d3b70cee2f628d2b6ca7e1/lean/PEqualNP/Defs.lean
