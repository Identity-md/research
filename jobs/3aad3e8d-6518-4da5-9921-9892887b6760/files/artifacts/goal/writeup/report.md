# Step L-meta-6583 (outside proof desk pequalnp): write-up

## 1. Outcome

**The step was not proved. There is no Lean 4 theorem to deliver, so no pull request on
`open-goat/pequalnp-proofs` is proposed by this job, and nothing was handed to another holder's
machine to check.**

- All four results end with `"status": "missing_lemma"` and each says in its first lines that no proof
  exists: "NOT PROVED" [A1], "Not proved; no Lean file is delivered" [A2], "NOT PROVED; no Lean file is
  offered" [A3], "NOT PROVED AND NOT REFUTED" [A4].
- None of the four claims the statement is false, and none found a counterexample [A1][A2][A3][A4].
  [A4] adds "I believe it is true; nothing here proves it."
- The goal's condition "once another holder's machine has checked it" was therefore never reached. The
  Lean that three results did run was a scratch reduction on their own machines, explicitly not
  delivered ([A1] "scratch only, not delivered"; [A2] "a scratch file that is not submitted"; [A3] "not
  submitted, since it is not the step"). No result contains Lean source, so I could not re-run it and
  it is reported here on the results' word only.
- `missing_lemma` is one of the release reasons the repository's README lists for stopping without a
  proof ("`hypothesis_too_weak`, `missing_lemma`, `statement_seems_false`, `out_of_time` or `other`")
  [G1]. Whether a desk lease for this step is held, and by whom, is not in my inputs.

**One thing the four results do not mention, found while checking them against the public repository:**
a pull request titled "L-meta-6583: force ten positive transitions in one Petersen factor" (#22053, by
another contributor, `AndrewRegnier`) was merged into `open-goat/pequalnp-proofs` `main` on
2026-11-25T23:46:28Z by `pequalnp-intake[bot]` [G3]. It does not prove the step. It adds one file,
`lean/PEqualNP/Outside/R_meta_6583_317.lean`, a reduction that derives the step from two narrower
unproved cases (section 5) [G5]. A file `lean/PEqualNP/Outside/L_meta_6583.lean` did not exist on `main`
when I fetched it (HTTP 404) [G6]. So in the public repository the step is, as of this write-up,
reduced but not proved. Whether the desk still posts L-meta-6583 as an open gap I could not establish
(section 7).

## 2. The statement

None of the four results quotes the Lean statement; each paraphrases it. The desk's posted statement
was not among my inputs. The text below is the conclusion of the merged reduction
`R_meta_6583_317` [G5], which is the statement that reduction establishes from its two hypotheses.
I added line breaks only (a script confirmed the text is otherwise character-for-character the
file's, whitespace aside). It agrees with all four paraphrases. I did not compare it with the desk's
own posted text.

```lean
have x1 : (Fin (10 : ℕ) → Bool) → Bool := fun (x1 : Fin (10 : ℕ) → Bool) => x1 (0 : Fin (10 : ℕ)) && x1 (1 : Fin (10 : ℕ)) || x1 (1 : Fin (10 : ℕ)) && x1 (2 : Fin (10 : ℕ)) || x1 (2 : Fin (10 : ℕ)) && x1 (3 : Fin (10 : ℕ)) || x1 (3 : Fin (10 : ℕ)) && x1 (4 : Fin (10 : ℕ)) || x1 (4 : Fin (10 : ℕ)) && x1 (0 : Fin (10 : ℕ)) || x1 (0 : Fin (10 : ℕ)) && x1 (5 : Fin (10 : ℕ)) || x1 (1 : Fin (10 : ℕ)) && x1 (6 : Fin (10 : ℕ)) || x1 (2 : Fin (10 : ℕ)) && x1 (7 : Fin (10 : ℕ)) || x1 (3 : Fin (10 : ℕ)) && x1 (8 : Fin (10 : ℕ)) || x1 (4 : Fin (10 : ℕ)) && x1 (9 : Fin (10 : ℕ)) || x1 (5 : Fin (10 : ℕ)) && x1 (7 : Fin (10 : ℕ)) || x1 (7 : Fin (10 : ℕ)) && x1 (9 : Fin (10 : ℕ)) || x1 (9 : Fin (10 : ℕ)) && x1 (6 : Fin (10 : ℕ)) || x1 (6 : Fin (10 : ℕ)) && x1 (8 : Fin (10 : ℕ)) || x1 (8 : Fin (10 : ℕ)) && x1 (5 : Fin (10 : ℕ));
∀ (x2 : PEqualNP.CircuitLowerBounds.Circuit) (x3 x4 : Fin (28 : ℕ)),
  PEqualNP.MetaComplexity.FanInTwo x2 →
    x2.size = (18 : ℕ) →
      (15 : ℕ) ≤ List.countP (fun (x7 : PEqualNP.CircuitLowerBounds.Gate) => !x7.op.eval [Bool.false]) x2.gates →
        have x8 : (Fin (10 : ℕ) → Bool) → ℕ → Bool := fun (x8 : Fin (10 : ℕ) → Bool) (x9 : ℕ) => (x2.wires (List.ofFn x8)).getD x9 Bool.false;
        (∃ (x9 : Fin (10 : ℕ) → Bool), x8 x9 ↑x3 = Bool.true ∧ x8 x9 ↑x4 = Bool.false) → (∃ (x10 : Fin (10 : ℕ) → Bool), x8 x10 ↑x3 = Bool.false ∧ x8 x10 ↑x4 = Bool.true) → ¬∀ (x11 : Fin (10 : ℕ) → Bool), (x8 x11 ↑x3 && x8 x11 ↑x4) = x1 x11
```

In words, as the results read it, consistently with each other [A1][A2][A3][A4]:

- `x1` is the edge function of the Petersen graph: 10 inputs, 15 edges (outer cycle 0-1-2-3-4, spokes
  i to i+5, inner pentagram 5-7-9-6-8, as [A4] lists them).
- `x2` is a fan-in-two AND/OR/NOT circuit with exactly 18 gates. The predicate `!op.eval [false]` is
  true exactly for AND and OR and false for NOT, so the `countP` hypothesis says at least 15 gates are
  AND/OR, that is, at most 3 are NOT.
- `x3`, `x4` are two of its 28 wires (10 inputs, 18 gates), and the two existentials say the functions
  they compute are incomparable.
- Claim: the AND of those two wires is not the Petersen edge function on all inputs.

## 3. What the results established

Where a line names more than one result, those results agree on it.

| Finding | Results | Kind of evidence |
|---|---|---|
| The step is the case "top gate is an AND of two incomparable wires" of "x1 has no 19-gate circuit" ([A1]'s words). Appending `AND [x3, x4]` to the 18 gates, with output wire 28, gives a FanInTwo circuit of size 19 that evaluates to the AND of the two wires, with AND/OR count one higher | [A1] (lemma `extend`), [A2], [A3] (`step_of_no19`) | Elaborated in Lean 4.36.0 against the prebuilt project, "no error, no sorry", scratch only, not delivered. [A4] gives the same reading but wrote and elaborated no Lean |
| So the step would follow from "no FanInTwo circuit of 19 gates computes x1"; that derivation uses neither the incomparability hypotheses nor the count hypothesis | [A1], [A3] | Same scratch Lean |
| The count hypothesis `15 ≤ countP …` is redundant: given `L_meta_6581` (a fan-in-two circuit computing x1 has at least 16 AND/OR gates), it follows from the other hypotheses plus the negated conclusion | [A1], [A3] (`count_redundant`, with the statement of `L_meta_6581` taken as a hypothesis) | [A3]: scratch Lean. [A1]: argument |
| Incomparability implies neither wire alone computes the function; no further use for it was found | [A2] | Scratch Lean |
| The existing project bounds do not close the step. `L_meta_6581` (at least 16 AND/OR gates), `L_meta_4725` (15 + notCount ≤ size) and `L_meta_4332` (with input 9 false, no wire, plain or negated, of a circuit of at most 15 gates computes x1) all remain satisfied in every case the hypotheses allow | [A1], [A3] (all three bounds); [A2] (the first two) | Reading of the project files |
| The cases left open for the 18-gate circuit are (AND/OR, NOT) = (15,3), (16,2), (17,1), (18,0); equivalently 16 to 19 AND/OR gates and at most 3 NOT gates in the 19-gate circuit | [A1], [A2], [A3] | Arithmetic on the hypotheses |
| `L_meta_6581` counts binary gates in a signed model where complementation is free, so it cannot see the NOT budget and puts no condition on the output gate | [A2] | Reading of the project file |
| No theorem concluding the 18- or 19-gate bound was found in the project; such bounds appear only as hypotheses of reductions (`R_meta_1884_1`, `R_meta_4035_1` per [A3]; `R_meta_4727_1`, about circuits of size ≤ 19 with notCount between 1 and 4, per [A2]) | [A2], [A3] | Search of the project, incomplete (section 7) |

### The missing lemma

All four results name the same gap, in slightly different words:

- [A1]: "A bound that rules those four cases out when the top gate is an AND of incomparable wires."
- [A2]: "For each n in {0,1,2,3}: no fan-in-two circuit with n NOT gates and 19 - n AND/OR gates whose
  output gate is an AND of incomparable wires computes f." It notes that for n = 3 this is one AND/OR
  gate more than `L_meta_6581` gives, and for n = 0 it is a lower bound of 20 for monotone circuits of
  this shape; and that it would follow from "every fan-in-two circuit computing f with at most 3 NOT
  gates has at least 20 gates".
- [A3]: "a new lower bound of 20 gates for this circuit shape is needed, and that bound (or all of not
  HasCircuitSize 10 P 19) is the one lemma missing."
- [A4]: "A proof has to be a structural lower bound for circuits WITH up to 3 NOT gates on a girth-5
  graph: essentially the whole 20-gate lower bound for the top-AND case."

Why it was not produced: the step quantifies over every 18-gate circuit, so it is "far outside
decide/simp range" [A1], and `native_decide` is forbidden ([A4]; the rule is in [G1][G2]). The
neighbouring bounds in the project are machine-generated search certificates: `L_meta_6581` is 284540
bytes for the bound 16 and `L_meta_4332` is 520393 bytes for a 15-gate bound on the restriction
x9 = false [A1][A2][A3]. A proof of this step "would need a new search of that kind, one or more gates
deeper, compressed under the 524,288-byte file limit" [A2]; none of the runs designed or ran one
([A2]; [A3] "I could not build one for this shape in the 114 minutes of this run"; [A1] says the search
program behind the `L_meta_6581` certificate "is not in the workspace").

### Evidence on whether the statement is true (none of it is a proof)

- The size is tight: the star-cover circuit (a minimum vertex cover of size 6, one gate per edge, 5 ORs
  to join) has 20 gates and its top gate is an OR; it computes x1 on all 1024 inputs ([A1], [A3], each
  by script; [A4] gives the count as 20 = e + tau - 1 = 15 + 6 - 1). [A3] writes it out:
  `x0(x1|x4|x5) | x1(x2|x6) | x3(x2|x4|x8) | x7(x2|x5|x9) | x9(x4|x6) | x8(x6|x5)`.
- Putting an AND on top of that construction costs 21 gates: `(x0 | R) & ((x1|x4|x5) | R)`, R the
  other five stars, correct on all inputs [A3]; [A4] gives the same count for the same form by hand.
- x1 has 76 zeros, the independent sets; neither wire can be an input wire, because for every vertex
  some edge avoids it [A3] (script, not Lean).
- SAT exact synthesis on small cases [A4] (its own script, CaDiCaL 1.5.3 through python-sat; "computer
  checks, not Lean proofs"):
  - triangle, 4 gates, top AND: SAT, `(x0 or x1) and (x2 or x0 x1)`; C5 with 7 gates: SAT; C5 plus a
    pendant edge with 8 gates: SAT. So a top AND of incomparable wires at size e + tau - 1 does occur
    for some graphs.
  - C5 (e = 5, tau = 3): exactly 4, 5, 6 gates UNSAT; 7 gates with top AND UNSAT; 8 gates with top AND
    SAT.
  - C5 plus pendant edge 0-5 (e = 6, tau = 3): exactly 5, 6, 7 gates UNSAT.
  - C5 plus path 0-5-7-2 (e = 8, tau = 4), 10 gates, at most 3 NOTs: no answer in 240 s.
  - Petersen itself, no NOT, 19 gates, top AND: no answer in 420 s. The same solver also did not find
    the known 20-gate top-OR circuit in 420 s, "so this timeout is evidence of nothing" [A4].
- No result ran an exhaustive or SAT search that finished on the Petersen instance [A1][A2][A3][A4].
  No 19-gate circuit was found, and none of the results claims that none exists.

### Routes the results suggest (all unproved)

- Gate elimination: show that in such a 19-gate circuit some input, set to false, removes at least 4
  gates, then contradict the 16-gate bound for Petersen minus a vertex. Needs a restriction / dead-gate
  removal framework for `Circuit`, a transfer of `L_meta_4332` from vertex 9 to the other vertices by
  graph automorphism, and the structural argument itself, "which I do not have" [A1].
- Extending the signed live-wire search certificate of `L_meta_6581` from 16 binary gates to this case
  [A1].
- Split by the number of NOT gates, 0 to 3 (with 0 the circuit is monotone), and, as the desk did for
  the OR-top sibling (`L_meta_7479` with `R_meta_4938_1`), fix the first gate and cut on whether a
  second gate exists [A3].
- Split into (a) normalization (remove constants, copies, repeated inputs, dead gates and double NOTs
  without raising the size or the NOT count), (b) from the AND equation and incomparability: f ≤ g3,
  f ≤ g4, and on every independent set one of g3, g4 is 0, (c) a gate-elimination or AND/OR-counting
  bound; or post the 0-NOT version first [A4].

## 4. Where the results differ

No result contradicts another on a finding. The differences are these:

1. **Repository name.** The goal names `open-goat/pequalnp-proofs`. [A2] says the prebuilt project it
   read is "brilliant-hq/pequalnp-proofs at e125f04d". When I requested
   `https://github.com/brilliant-hq/pequalnp-proofs`, GitHub answered HTTP 301 to
   `https://github.com/open-goat/pequalnp-proofs` [G9], so the two names lead to the same repository
   today. I did not look up commit `e125f04d`.
2. **How the step relates to the 19-gate bound.** [A1] and [A3] say the step follows from the 19-gate
   bound; [A2] says the step "appears to be one top-gate case of that 19-gate bound rather than a
   consequence of it". These are compatible: the bound would imply the step, but the project does not
   have the bound as a theorem, only as a hypothesis of reductions, and this step looks like one case
   in a proof of it. That reconciliation is my reading.
3. **Wording of the target bound.** [A2] and [A3] ask for 20 gates for the whole circuit; [A4]'s item
   (c) asks for "at least 19 gates under such a top AND". I read the latter as 19 gates below the top
   AND, the same bound; [A4]'s own reading of the step ("no 19-gate ... circuit ... computes f")
   supports that, but the phrase is ambiguous.
4. **Which vertex cover.** [A3] uses stars at {0,1,3,7,8,9}; [A4] names the cover {1,3,4,5,6,7}. Both
   are vertex covers of size 6 (my recomputation, section 6), so both describe a valid 20-gate circuit.
5. **Tools available.** [A1]: "this machine has no SAT solver or C compiler". [A4] ran a SAT solver.
   Different runs, not a contradiction; only [A4] has SAT results.
6. **Access to the project's proofs.** [A1], [A2], [A3] read existing `Outside` files. [A4] could not:
   "after two early listings the source files of the prebuilt project could not be read here", so its
   statement that it knows no such lemma covers only Mathlib and `PEqualNP.Defs`, plus one bound it saw
   (`MetaComplexity.L115`, e + tau ≤ size + 1, assuming no NOT gate and girth at least 9).
7. **Coverage of the project search.** Only [A2] gives counts: 15 files contain the exact Petersen
   expression, all read; 174 files mention Petersen, of which it read the main statements of the first
   50 only.

## 5. The merged reduction of this step (not in the four results)

Read directly from GitHub during this write-up (machine date 2026-11-26); the file was downloaded and
read in full, the pull-request fields come from the GitHub API response.

- Pull request #22053, "L-meta-6583: force ten positive transitions in one Petersen factor", author
  `AndrewRegnier`, base `open-goat/pequalnp-proofs` `main`, head branch `R-meta-6583-317`, created
  2026-11-25T22:32:16Z, merged 2026-11-25T23:46:28Z by `pequalnp-intake[bot]`, 1 commit, 1 file, 59
  additions, 0 deletions, head `439da1b13e703a46e84357d87bdf71a872883f3e`, merge commit
  `4be8766b9982ab8e6e5c6e595001d2fb94a1ac0f` [G3]. The pull-request page, read through a summarizing
  fetch tool rather than by me directly, shows a bot comment "ACCEPTED (checker exit 0)" [G4].
- The file `lean/PEqualNP/Outside/R_meta_6583_317.lean` is 5618 bytes at the merge commit and identical
  on `main` (SHA-256 `f31810e93b2302b2d398f8a071866d0d1ac0cb321bfb7cba5af78100c8ea6996` for both
  downloads) [G5]. It contains no `sorry` and no `native_decide`; it uses `decide +kernel` once.
- What it proves: the statement of section 2, **assuming** two hypotheses `both` and `one`. Each is the
  step with extra premises about a property the file calls `sensitive`: wire `i` is sensitive when for
  every vertex `v` one of the five rows `[116,201,402,554,773]` has the wire false and turning input `v`
  on makes it true. `both` is the case where both wires are sensitive; `one` is the case where the
  first is and the second is not. The proof shows at least one wire is sensitive and dispatches by
  symmetry [G5]. The pull-request description says the rows are "the five maximum independent sets of
  the Petersen graph" [G3]; my script agrees (section 6).
- What it does not do: it does not prove `both` or `one`. Each is still a statement about every
  18-gate circuit, so in my reading the missing lemma of section 3 is narrowed, not supplied. The ids
  of the two child gaps, and whether either has been proved, I did not find.
- Consequence for the goal: `CONTRIBUTING.md` says "The gap must still be posted when the pull request
  is checked. If someone else's proof of the same gap was accepted earlier, the gap is closed." [G2].
  An accepted reduction is not a proof of the gap, and I could not tell from public pages whether the
  desk treats L-meta-6583 as still posted or as replaced by its two children. That is a question for
  the desk before any further attempt on this step.

Whether this reduction existed when the four results were written is not known: the results carry no
timestamps, and the only commit any of them names is `e125f04d` [A2], which I did not look up.

## 6. What I rechecked, and how

I did not run Lean: this job's inputs contain no Lean source to run. The following were recomputed or
re-read; none of it is a proof of the step.

By a small script of my own over all 1024 inputs (not delivered):

- 15 edges; 76 zeros of the function (the independent sets); minimum vertex cover size 6; no triangle
  and no 4-cycle; for every vertex some edge avoids it. Agrees with [A1][A3][A4].
- Both {0,1,3,7,8,9} and {1,3,4,5,6,7} are vertex covers. The six-star formula of [A3] has 20 gates,
  top gate OR, and is correct on all inputs. The form `(x0 | R) & ((x1|x4|x5) | R)` has 21 gates, is
  correct on all inputs, and its two top wires are incomparable. Agrees with [A1][A3][A4].
- The triangle formula of [A4], `(x0 or x1) and (x2 or x0 x1)`, computes the triangle edge function
  with incomparable factors. C5 has minimum vertex cover size 3.
- The rows 116, 201, 402, 554, 773 of the reduction are exactly the independent sets of size 4, the
  maximum, and there are 5 of them; for every pair of vertices one of these sets stays independent
  itself but gains an edge when either vertex is added (the `census` step of [G5]).

By reading the public repository `main` [G7][G8]:

- `L_meta_6581.lean` is 284540 bytes and `L_meta_4332.lean` is 520393 bytes, as [A1][A2][A3] state.
- The theorem statements of `L_meta_6581` (`(16 : ℕ) ≤ List.countP …` for a FanInTwo circuit with
  `circuitFun (10 : ℕ) x2 = x1`), `L_meta_4725` (`(15 : ℕ) + PEqualNP.NotBracket.notCount x2 ≤ x2.size`)
  and `L_meta_4332` (size ≤ 15, input 9 false, wire plain or negated) are as the results describe them.
  The header of `L_meta_6581.lean` says "The signed search counts binary gates with complementation
  available for free.", matching [A2].
- `R_meta_4727_1` has two hypotheses about FanInTwo circuits with `x2.size ≤ (19 : ℕ)` and notCount
  between 1 and 4 for the same function, matching [A2]. `L_meta_7479` and `R_meta_4938_1` exist and
  differ in whether a gate at index 1 exists, matching [A3]'s description of the OR-top sibling.
- `lean/lean-toolchain` reads `leanprover/lean4:v4.36.0`, matching the Lean 4.36.0 of [A1][A2][A3].
- `CONTRIBUTING.md` limits the file to "at most 512 KiB" (512 × 1024 = 524288 bytes, the limit
  [A1][A2] cite) and forbids `sorry`, `native_decide` and axioms beyond `propext`, `Classical.choice`,
  `Quot.sound` [G2].

## 7. Not found, not done, not verified

- No proof of the step, by anyone: not in the four results, and no `L_meta_6583.lean` on `main` [G6].
- No counterexample; no completed exhaustive or SAT search on the Petersen instance
  [A1][A2][A3][A4].
- The desk's own posted statement of L-meta-6583 and its current status (posted, leased, reduced,
  closed). I did not query the desk: its endpoint takes a GitHub handle and issues a lease [G1], which
  is not this write-up's to do. The site's front page, read through a summarizing fetch tool, did not
  mention the step [G10].
- The scratch Lean reductions of [A1][A2][A3]: not in my inputs, so not re-run.
- The SAT results of [A4]: not re-run.
- [A2]'s counts of 15 and 174 files, commit `e125f04d`, and the items `R_meta_1884_1`,
  `R_meta_4035_1`, `MetaComplexity.L115`, `HasCircuitSize`: not looked up.
- [A2] read the statements of only the first 50 of the 174 files mentioning Petersen, so, in its
  words, "a stronger bound stated in another encoding in the remaining files is not excluded".
- The ids and status of the two child gaps created by `R_meta_6583_317`.

## 8. What should happen next

1. Do not open a pull request for L-meta-6583 from this job: there is no proof file, and the
   repository's checker accepts nothing less ("No `sorry`, anywhere under the theorem" [G1]).
2. If a lease on the step is held, release it with reason `missing_lemma`, the status all four results
   report and a reason the README provides [G1].
3. Before spending more on this step, ask the desk whether L-meta-6583 is still posted now that
   `R_meta_6583_317` is merged. If the open work is now its two cases (`both`, `one`), any further
   attempt should start from those statements [G5], not from the original one.
4. Any further attempt needs the missing lower bound of section 3. The results agree it is a
   certificate-scale search or a new structural argument, not a short helper lemma; the routes they
   suggest are listed at the end of section 3.

## Sources

Results (inputs of this write-up, read as data):

- [A1] `artifacts/goal/items/angle-1/result.json`, SHA-256
  `5b474a48866961cc820267edf0881f2c6c3abb05a32b6a48f7e5d3e5a691391f`
- [A2] `artifacts/goal/items/angle-2/result.json`, SHA-256
  `fb21cd321003b5585737fae67d89291d431ecf16c1072dd19e1f9168434758cc`
- [A3] `artifacts/goal/items/angle-3/result.json`, SHA-256
  `b257f2f4517cb0f659548c7136f3baabda9594f7b5407a4f87ff7392865fca7f`
- [A4] `artifacts/goal/items/angle-4/result.json`, SHA-256
  `877b1a7cafb33a5a08359c7bb411e6da9ee1984df4d28250ce6c4f236286611e`

Public pages, fetched during this write-up (machine date 2026-11-26):

- [G1] https://raw.githubusercontent.com/open-goat/pequalnp-proofs/main/README.md
- [G2] https://raw.githubusercontent.com/open-goat/pequalnp-proofs/main/CONTRIBUTING.md
- [G3] https://api.github.com/repos/open-goat/pequalnp-proofs/pulls/22053
- [G4] https://github.com/open-goat/pequalnp-proofs/pull/22053 (read through a summarizing fetch tool)
- [G5] https://raw.githubusercontent.com/open-goat/pequalnp-proofs/4be8766b9982ab8e6e5c6e595001d2fb94a1ac0f/lean/PEqualNP/Outside/R_meta_6583_317.lean
  and the same path on `main`
- [G6] https://raw.githubusercontent.com/open-goat/pequalnp-proofs/main/lean/PEqualNP/Outside/L_meta_6583.lean
  (HTTP 404)
- [G7] `L_meta_6581.lean`, `L_meta_4332.lean`, `L_meta_4725.lean`, `L_meta_7479.lean`,
  `R_meta_4938_1.lean`, `R_meta_4727_1.lean` under
  https://raw.githubusercontent.com/open-goat/pequalnp-proofs/main/lean/PEqualNP/Outside/
- [G8] https://raw.githubusercontent.com/open-goat/pequalnp-proofs/main/lean/lean-toolchain
- [G9] https://github.com/brilliant-hq/pequalnp-proofs (HTTP 301 to
  https://github.com/open-goat/pequalnp-proofs)
- [G10] https://pequalnp.com (read through a summarizing fetch tool)
