# Step L-meta-3456 (pequalnp-proofs) — status report

**Goal as stated:** produce a completed Lean 4 theorem for step `L-meta-3456` of the
`pequalnp` proof desk, have it checked by a second contributor's machine, and open the
proving contributor's pull request on `open-goat/pequalnp-proofs`.

**Result: the goal is not reached.** None of the four independent research angles
merged below produced a finished Lean proof, so there is nothing for a second holder
to check and no PR to open. Reporting that gap honestly, rather than inventing a proof,
a check, or a PR URL, is the only accurate thing this write-up can do with the inputs
it was given: a write-up step merges research results, it does not do new mathematics
on its own authority, and the task's own rules forbid filling an acceptance gap with
any stand-in. All four source records are reproduced and summarized below so the next
contributor (or the next angle) does not have to redo this work.

## What the four angles agree on

All four results — `item-angle-1`, `item-angle-2`, `item-angle-3`, `item-angle-4`
(each `artifacts/goal/items/angle-N/result.json`) — report
`"status": "missing_lemma"`, independently, using different proof strategies and
different exhaustive-search code. None reports `statement_seems_false`. All four
converge on the same obstruction, which is restated per-angle below. No Lean file,
`.lean` source, or `sorry`-free completed theorem is attached in any of the four
records; angle 1 states this explicitly ("no Lean file is offered"), and angle 3
states explicitly that its ~830-line scratch file is "not attached, since the lean
field is for a full proof" — i.e. it is a partial reduction, not a completed proof.

The target statement (as elaborated by all four against `PEqualNP.Defs`,
Lean 4.36.0, prebuilt project) is equivalent to: for every `K22`-free / `C4`-free
incidence structure `I`, the minimum-size `Monotone2`, `ReadsBack` circuit computing
the associated function `f_I` can be chosen so that none of its `AND` gates evaluates
to `true` on any single one-hot input ("no bad AND gate"). This equivalence itself
elaborates without error in all four reports' Lean environments.

## Source records (verbatim status per angle)

### Angle 1 — `artifacts/goal/items/angle-1/result.json`
Status: `missing_lemma`. Confirms the statement's setup and unfolding elaborate
correctly, but the body is open. Gives a paper-only (not Lean-checked) sketch for the
"unshared OR cone" case and identifies the missing piece as the "shared OR cone"
case: it shows by explicit example that the natural shortcut ("replace the AND by one
of its operands") is *unsound* in general. Ran an exhaustive search (not a proof) over
all 21 `K22`-free structures with ≤ 6 non-isolated vertices and 18 of 19 such
structures with 7 vertices, up to size 8 gates: found no counterexample to the "no bad
AND" claim. One structure at 7 vertices was not decided (needs > 8 gates).

### Angle 2 — `artifacts/goal/items/angle-2/result.json`
Status: `missing_lemma`. Builds and elaborates in Lean (no `sorry`, axioms
`propext`, `Classical.choice`, `Quot.sound`) a reduction of the full statement to one
"RAISE-STEP" lemma, via strong induction on circuit size plus a secondary measure.
Proves auxiliary Lean lemmas (`first_bad`, `circuitMono`/sandwich argument) and handles
three of four first-bad-gate shapes (gates with 0 or 1 input) completely in Lean. The
fourth shape — a bad AND gate with two distinct earlier OR-gate inputs — is left open;
the angle narrows this to two sub-cases (`d2`, `d3`) and states it has no exchange
argument for either, and performed no counterexample search in the time available.

### Angle 3 — `artifacts/goal/items/angle-3/result.json`
Status: `missing_lemma`. Elaborates (no `sorry`) a longer Lean reduction of the full
statement to a single open lemma it calls `CORE`. Proves four Lean lemmas (constants,
copy, lower, shape) covering every case of a first bad gate except one specific shape
(an AND of two earlier OR gates agreeing at one input `v`), which is exactly `CORE`.
Gives a non-vacuous witness showing `CORE`'s hypotheses are satisfiable. Reports
exhaustive-search (C program, not Lean) evidence: for 26 connected `C4`-free bipartite
graphs up to 7 vertices, minimum circuit size always equals the minimum size restricted
to circuits with no bad AND gate; for 25 of those 26, no minimum-size circuit has a bad
AND gate at all (the 26th, minimum size 9, was not decided — too slow). Flags a
stronger conjecture ("any circuit satisfying `CORE`'s hypotheses is not of minimum
size") as worth trying but unproven.

### Angle 4 — `artifacts/goal/items/angle-4/result.json`
Status: `missing_lemma`. Took a search/bound-based angle rather than a Lean
reduction. Exhaustively verified (C search, not Lean) the "no bad AND gate" property
for all nonempty `C4`-free incidence classes at `N ≤ 3` (1 + 4 + 15 classes) and for 43
of 58 such classes at `N = 4` (15 undecided — search budget of 4×10⁹ nodes exhausted on
classes needing ≥ 9 gates). For all settled cases it additionally enumerated *every*
minimum circuit (not just one) and found none with a bad AND gate. Observed that in
every settled case, minimum circuit size equals `e + t − 1` (`e` = number of incidences,
`t` = minimum vertex cover of the incidence graph), and proposes this bound, if proved,
as an alternative route that bypasses the open core lemma entirely (`(3')` in its notes)
— but states this bound itself is currently only numerically supported, not proved.

## Where the proof stops

Every angle isolates the same open point: a minimum circuit may contain an `AND` gate
`g = a AND b` where `a` and `b` are themselves `OR` gates that both evaluate `true` on
one shared single-input (one-hot) vector. No angle found a way to eliminate such a gate
without either (a) growing the circuit, (b) changing the function it computes, or
(c) assuming the `C4`/`K22`-free hypothesis is used in some way none of the four could
complete. Angle 3's `CORE` and angle 2's unresolved case `d2`/`d3` are the same
obstruction stated two different ways; angle 1's "shared OR cone" case and angle 4's
general undecided classes are the same obstruction again, approached by direct search.
No published reference resolving this exact case was found by any angle (angle 4 notes
one related but strictly different result on single-level circuits as background only).

## Deliverables requested vs. what exists

| Requested | Status |
|---|---|
| Completed Lean 4 theorem for `L-meta-3456` | **Not produced.** All four angles report an open core lemma; no `.lean` source or `sorry`-free proof term for the full statement is attached anywhere in the four records. |
| Second holder's check of that proof | **Not applicable.** There is no completed proof to check. |
| Contributor's pull request on `open-goat/pequalnp-proofs` | **Not opened.** No PR URL, branch, or commit is present in any of the four records, and none can be fabricated per this task's rules. |

## Figures stated in this report

Every numeric figure above is quoted from its source record and is not independently
re-derived here:
- Angle 1: 21 `K22`-free structures (≤6 vertices, all decided to size 8), 19 structures
  at 7 vertices (18 decided).
- Angle 3: 26 connected `C4`-free bipartite graphs ≤7 vertices (25 of 26 decided);
  13 graphs ≤6 vertices containing a 4-cycle (control group).
- Angle 4: 1 / 4 / 15 nonempty classes at `N = 1,2,3` (all decided); 58 nonempty
  classes at `N = 4` (43 decided, 15 undecided); search budget 4×10⁹ nodes per class;
  bound `e + t − 1` observed in all settled cases.

No other figures (timings, dates, author identities, commit hashes, PR numbers) are
stated anywhere in the four source records, so none are repeated here.

## Conclusion

The honest write-up of these four results is that step `L-meta-3456` remains **open**.
The three outputs the goal calls for — a completed theorem, a second-holder check, and
a contributor PR — do not exist in the material handed to this write-up step, and
cannot be produced without either (a) solving the shared-OR-cone core lemma identified
independently by all four angles, or (b) proving the alternative `e + t − 1` minimum-size
bound flagged by angle 4, either of which is original mathematical research outside the
scope of merging and reporting on existing results. The next useful step is a fifth
angle targeting specifically the shared-OR-cone case (`CORE` / `d2`/`d3`) or the
`e + t − 1` lower bound, not another write-up of the same four inputs.
