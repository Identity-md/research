# L-meta-2571 goal-job write-up

## Disposition

The requested proof contribution is **not established by the four supplied results**.  No result supplies a 45-gate witness circuit or a Lean theorem file; consequently the supplied material cannot supply an accepted Lean check, a check by a second holder, or a pull request from the proving contributor. This is an evidence-based non-completion report, not a claim that the theorem is false. [A1](#a1-item-angle-1), [A2](#a2-item-angle-2), [A3](#a3-item-angle-3), [A4](#a4-item-angle-4)

The revision finding is substantively reproduced: all four records describe unsuccessful construction/search work, while the best concrete circuit they report uses 46 gates against the requested 45-gate bound. The previous report named in the finding is not present in this workspace, so its quoted line range and SHA-256 could not be independently rerun here; the conclusion below is based only on the supplied current records. [A1](#a1-item-angle-1), [A2](#a2-item-angle-2), [A3](#a3-item-angle-3), [A4](#a4-item-angle-4)

## Required outcome

| Goal outcome | Evidence in the supplied records | Result |
| --- | --- | --- |
| A Lean 4 theorem proving step L-meta-2571 | Every record says that no Lean file was produced because no witness circuit was found. [A1](#a1-item-angle-1), [A2](#a2-item-angle-2), [A3](#a3-item-angle-3), [A4](#a4-item-angle-4) | Missing |
| An accepted check of that theorem | No theorem file, check transcript, accepted check, or solution commit is supplied. This follows for the theorem file from A1--A4; the remaining evidence is absent from all four supplied records. [A1](#a1-item-angle-1), [A2](#a2-item-angle-2), [A3](#a3-item-angle-3), [A4](#a4-item-angle-4) | Missing from supplied evidence |
| Check by another holder's machine | No record identifies another holder, a solution commit, or that holder's check. [A1](#a1-item-angle-1), [A2](#a2-item-angle-2), [A3](#a3-item-angle-3), [A4](#a4-item-angle-4) | Missing from supplied evidence |
| Pull request to `open-goat/pequalnp-proofs` from the proving contributor | No record gives a pull-request URL/number, contributor account, branch, or commit. [A1](#a1-item-angle-1), [A2](#a2-item-angle-2), [A3](#a3-item-angle-3), [A4](#a4-item-angle-4) | Missing from supplied evidence |

Absence from the supplied records does not prove that a check or pull request does not exist elsewhere. It does mean the stated goal cannot be verified from these results.

## What the records do establish

All four records analyze the same reduced Boolean-circuit problem: nine retained point inputs, twelve line inputs numbered 13 through 24, and the three-line target `x13 OR x15 OR x21`. They identify lines 13, 15, and 21 as a parallel class in the affine plane of order 3, and give 36 point-line incidences. [A1](#a1-item-angle-1), [A2](#a2-item-angle-2), [A3](#a3-item-angle-3), [A4](#a4-item-angle-4)

They report the same straightforward construction: for each of the nine points, form an OR of its four incident lines (three OR gates) and AND it with the point; then OR the nine terms together (eight OR gates). That computes the incidence function in 44 gates. Two additional OR gates compute `x13 OR x15 OR x21`, for 46 gates total. A1 reports bit-parallel verification on all `2^25` inputs; A4 reports exhaustive verification on all `2^21` assignments to the live inputs. [A1](#a1-item-angle-1), [A4](#a4-item-angle-4)

Thus the documented construction exceeds the requested 45-gate limit by one gate. The records do not derive a 45-gate construction or a lower bound proving that one cannot exist. A1 explicitly classifies its result as `other`; A3 as `missing_lemma`; A2 and A4 as `statement_seems_false`, while both of the latter explicitly say that they did not prove a refutation. [A1](#a1-item-angle-1), [A2](#a2-item-angle-2), [A3](#a3-item-angle-3), [A4](#a4-item-angle-4)

The search evidence is limited and should not be overstated. A2, A3, and A4 report exact-synthesis searches on smaller analogues and/or restricted bank forms, including some UNSAT results; they also report that the real 45-gate/full search or relevant larger cases were unresolved or timed out. A1 reports small-analogue exhaustive searches and failed manual variants. None claims that these searches cover every 45-gate circuit for the real instance. [A1](#a1-item-angle-1), [A2](#a2-item-angle-2), [A3](#a3-item-angle-3), [A4](#a4-item-angle-4)

## Relation to the stated proof path

A1, A2, and A4 report that the desk reductions `R_meta_2571_417` and `R_meta_2571_911` leave the required circuit/bank as an open hypothesis: the former needs a 28-gate bank and the latter a 45-gate circuit on 21 inputs. A3 likewise describes the 28-gate bank as the missing lemma, with the naive bank costing 29 gates. These are reports about the supplied project analysis, not proofs that no alternative Lean proof exists. [A1](#a1-item-angle-1), [A2](#a2-item-angle-2), [A3](#a3-item-angle-3), [A4](#a4-item-angle-4)

## What is needed before the goal can be claimed complete

1. A concrete 45-gate (or smaller) witness satisfying the step's output and promised-wire conditions, or another proof route that proves the Lean theorem.
2. A Lean source file containing the theorem and a successful elaboration/check tied to an identifiable solution commit.
3. A successful check of that same commit on another holder's machine.
4. A pull request from the proving contributor's account to `open-goat/pequalnp-proofs` that submits the checked commit.

These are completion requirements derived from the goal statement. They are not present in A1--A4.

## Source register

The sources are the four supplied merged-result files. Their SHA-256 values were checked against the hashes provided with this task.

### A1 — item-angle-1

- File: `.imd/reads/artifacts/item-angle-1`
- SHA-256: `38f1955a551c2fc48d68817097957c4017eb7d800b2907d90c9e15534abaa5ac`
- Status recorded by source: `other`
- Relevant source statement: “NOT PROVED: no witness circuit found, so there is no Lean file to elaborate.”

### A2 — item-angle-2

- File: `.imd/reads/artifacts/item-angle-2`
- SHA-256: `579ca71ac3fd78f252f7657961c58bacd88167185f9b8dbdf70beeb4d8ccbac6`
- Status recorded by source: `statement_seems_false`
- Relevant source statement: “Not proved. I think the bound 45 is one gate too small, but I have no proof of that.”

### A3 — item-angle-3

- File: `.imd/reads/artifacts/item-angle-3`
- SHA-256: `280ecfae50c868d4eb91ef659285d76cde8b98e440a2826b2299b219946d915a`
- Status recorded by source: `missing_lemma`
- Relevant source statement: “Not proved, so no Lean file. I could not construct the circuit and I have no disproof.”

### A4 — item-angle-4

- File: `.imd/reads/artifacts/item-angle-4`
- SHA-256: `b431a5b4753bd60d2c8f27df8e84d9b59f4ce6590d814cfb592822ff1e0dc7bc`
- Status recorded by source: `statement_seems_false`
- Relevant source statement: “NOT PROVED and NOT REFUTED; the evidence points to false. No Lean file was written because no witness circuit was found.”
