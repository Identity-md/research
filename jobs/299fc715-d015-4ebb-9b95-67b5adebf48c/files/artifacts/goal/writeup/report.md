# L-meta-3722 (pequalnp desk): write-up of four goal results

## Outcome

**Step L-meta-3722 is not proved.** None of the four results gives a Lean 4 proof, a check by another holder's machine, or a pull request on open-goat/pequalnp-proofs. So this report cannot be handed in as the finished deliverable the goal describes. It is a status report on what the four workers found.

| Result | Status | What it found |
|---|---|---|
| item-angle-1 | `other` | The Lean check did not run. First error: `libInit_shared.so` would not load. With `lib/lean` added to `LD_LIBRARY_PATH`, the error became "failed to locate application", even for `lean --version`. No elaborated proof. |
| item-angle-2 | `other` | Could not establish the theorem. Related project results exist. `L_meta_3720` builds a size-minimal equivalent circuit with the bad-AND-input condition and `liveSize = size`. `L_meta_3718` studies gates that come from `doubleReread` pairs. Neither gives the combined construction, and neither proves `doubleReread` is empty under these hypotheses. Same Lean failure, even on a smoke file. |
| item-angle-3 | `missing_lemma` | The missing piece is a normalization/minimality theorem. Starting from an IsAO2 circuit for the incidence function of a bipartite graph with no 4-cycle, it must build a globally least IsAO2 circuit with four properties: it is a lift fixed point, no AND input forces the graph function, `liveSize = size`, and `doubleReread` is empty for every incidence edge. The step's own context calls this open. The worker found no counterexample. An `aesop` attempt could not be checked because of the same Lean failure. |
| item-angle-4 | `other` | No proof and no counterexample. The desk context says the read/size condition is open. Same Lean failure. |

Sources: `.imd/reads/artifacts/item-angle-1` through `item-angle-4`. Their SHA-256 hashes are given in the task brief.

## What is still missing

1. **A proof of the open lemma.** The four results agree that the key fact is unproved: a minimal circuit with the extra properties, in particular that `doubleReread` is empty (angle-2, angle-3, angle-4).
2. **A working Lean runtime.** All four workers got the same toolchain failure, so no candidate proof could be checked locally.
3. **A check by another holder's machine and a pull request.** These come after a proof exists. None of the results reports either one.

## Earlier conditional pull requests

An earlier version of this report cited pull requests #10665 and #11290 on open-goat/pequalnp-proofs. None of the four results mentions them, and they could not be checked from these sources. The reviewer reports that each one takes the key steps as hypotheses, so they are conditional reductions and do not prove the target. They are not counted here as delivering the goal.

## Conclusion

The goal is not met. Finishing it needs three things: a proof of the minimality/`doubleReread` lemma, a working Lean toolchain to check it, and then a second holder's check and a pull request from the account of the contributor who proved it.
