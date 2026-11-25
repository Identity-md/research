# L-meta-2373 (desk pequalnp): write-up of four results

## Outcome

**This job did not prove L-meta-2373.** None of the four results contains a Lean 4 proof. So there is no checked theorem, nobody else's machine checked anything, and this job opened no pull request on open-goat/pequalnp-proofs. Rewording this report cannot change that. Two things could: a new proving round that produces the theorem, or the requester deciding to stand the step down.

| Deliverable the goal asks for | Status | Source |
|---|---|---|
| Lean 4 theorem for L-meta-2373 | Not produced | item-angle-1..4 (each says no proof was produced) |
| Check by another holder's machine | Not done (nothing to check) | follows from the row above |
| Pull request from the prover's account | Not opened | follows from the row above |

An independent reviewer reported two public facts in its finding on the earlier revision. I did not fetch either of them again for this revision:
- On pull request #15214 the intake bot said the step "has been stood down: the attack no longer needs it".
- The desk status list still shows L-meta-2373 as an open gap.

## What the results establish

- **The reduction (item-angle-1, item-angle-4).** Suppose the conclusion fails. Then the hypotheses force the OR of the two selected wires of x2 to equal the Petersen-graph edge predicate on the 10 input bits:
  - the OR is false on every independent set, and
  - it is true on every assignment that contains an edge.
- **The gate count (item-angle-1, item-angle-4).** That OR gives a circuit for the edge predicate with at most 19 gates:
  - 1 preprocessing gate (x1),
  - at most 17 gates (x2),
  - 1 final OR gate.
- **What is missing (all four results).** The step therefore needs a lower bound: the Petersen edge predicate has no AND/OR/NOT circuit of at most 19 gates in this form. No such lemma is available from the permitted import `PEqualNP.Defs`.
- **The desk's own case split (item-angle-2, item-angle-4).**
  - item-angle-2: the prebuilt project's reduction splits on whether the first gate is AND, OR or NOT, but the results for those cases are assumptions there, not lemmas.
  - item-angle-4: the desk sketch says its five-case search did not decide the 19-gate case.
- **No counterexample (item-angle-1, -2, -4).** None of these found a counterexample, so the statement is neither shown false nor proved.
- **Toolchain failure (item-angle-3).** Lean failed to start:
  - first a `libInit_shared.so` load failure;
  - then, after setting `LD_LIBRARY_PATH`, `error: failed to locate application`.

  This item produced no check.

## What could not be found

- A proof of the 19-gate lower bound, or a counterexample to it.
- Any Lean file for this step that has been checked.

## Sources

The four results, as received (SHA-256 of each file):
- item-angle-1: `2c5adf59de8e1504a5327f4c61b03d4ac72aa6c1506f169a0ab06240b09c2c57`, status `missing_lemma`
- item-angle-2: `c08d0b04cb6add4176e1310f575c3e5f7963fe9d8d650932da55edbbd21d72ff`, status `missing_lemma`
- item-angle-3: `28400b6e835137c67bb328be2f8a0487d59cf9d3cec1ac087bcc9774b44b4ebb`, status `other`
- item-angle-4: `f9b5681e2f2d49b23e87e315e3cbf613251d284e5c5b7148f389c62f630eb83a`, status `missing_lemma`
