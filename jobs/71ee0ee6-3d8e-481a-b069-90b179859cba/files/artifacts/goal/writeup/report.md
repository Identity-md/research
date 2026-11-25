# L-meta-2583 (pequalnp proof desk): write-up of the goal job

## Outcome

**Not delivered. Step L-meta-2583 is not proved, and this document is not a substitute for the proof.**

The goal asks for three things: one Lean 4 theorem proving L-meta-2583, a check of that proof on another holder's machine, and a pull request on `open-goat/pequalnp-proofs` from the account of the contributor whose machine proved it. None of the three exists:

| Required by the goal | State | Basis |
|---|---|---|
| Lean 4 proof of L-meta-2583 | **Absent** | All four results report `status: missing_lemma` and say no proof was produced (table below). |
| Check on another holder's machine | **Absent** | There is no proof file to check; no result contains checker output. |
| Pull request from the proving contributor's account | **Absent** | No result reports a pull request, a branch, a lease or a URL. |

The requester cannot use this report as the commissioned theorem contribution. What it does supply is the evidence for that verdict, the exact gap the four attempts hit, and the public state of the step at the time of writing, so the next attempt starts from the right place.

This write-up step received four result files and may write only this report. It did not attempt the proof, ran no Lean build, and opened no pull request.

## Results received

Four results were handed in. All four are present and non-empty, all four parse as JSON with the fields `status` and `notes`, and all four agree.

| Result | SHA-256 of the file | `status` | Proof file | Checker output |
|---|---|---|---|---|
| item-angle-1 | `0da349cc01d1982cff016353d289f5e5e7f9ef55a649d51a4907978540763a38` | `missing_lemma` | none | none |
| item-angle-2 | `51a84e88d83a40de186b675b7673d827b9d44d96542f91d12e24438a7c621098` | `missing_lemma` | none | none |
| item-angle-3 | `70871251c088e69a731035291280fb078afc7ec0893e3989734678f302eb6b5e` | `missing_lemma` | none | none |
| item-angle-4 | `ba2daf7534a96f6bbb00c9faf914b66f7f93aa7d583a4a2ee07b9e8a8e347c41` | `missing_lemma` | none | none |

Each result says in its own words that no proof exists:

- item-angle-1: "I could not establish the structural normalization or elaborate a proof, so I cannot claim this theorem proved."
- item-angle-2: "I therefore cannot report Lean acceptance or provide a proof file."
- item-angle-3: "No Lean proof was produced."
- item-angle-4: "I could not establish that lemma or elaborate a proof of the theorem; no Lean proof file is claimed."

## The step

The desk's published record for the step (source S1) gives:

- Title: "On a plane of order q, every fan-in-two AND/OR circuit for incidence can be replaced by a read-1 one with at most as many gates".
- Status: `conjecture`; `attempts`: empty; proposed 2026-11-24T09:00:08.316Z.
- Statement hash: `sha256:06ffc515bfe521dd0eb1a0ef05d2683255d714f1fa4a0abd5394e6a3e3923e1d`.
- Formal statement, copied from S1:

```lean
∀ (q N : ℕ) (I : Fin N → Fin N → Prop) [DecidableRel I] (C : PEqualNP.CircuitLowerBounds.Circuit), 2 ≤ q → N = q ^ 2 + q + 1 → (∀ l : Fin N, (Finset.univ.filter (fun p => I p l)).card = q + 1) → (∀ p p' : Fin N, p ≠ p' → ∃! l : Fin N, I p l ∧ I p' l) → PEqualNP.TopForm.IsAO2 (N + N) C → (∀ z : Fin (N + N) → Bool, PEqualNP.MetaComplexity.circuitFun (N + N) C z = decide (∃ p l : Fin N, I p l ∧ z (Fin.castAdd N p) = true ∧ z (Fin.natAdd N l) = true)) → ∃ D : PEqualNP.CircuitLowerBounds.Circuit, PEqualNP.TopForm.IsAO2 (N + N) D ∧ (∀ y : Fin (N + N) → Bool, PEqualNP.MetaComplexity.circuitFun (N + N) D y = decide (∃ p l : Fin N, I p l ∧ y (Fin.castAdd N p) = true ∧ y (Fin.natAdd N l) = true)) ∧ D.size ≤ C.size ∧ PEqualNP.ReadK.IsReadK (N + N) D 1
```

The two definitions the results name are in the project's `Defs` modules:

- `IsReadK` (S5): "`C` is READ-k on `n` inputs: every prime implicant of the function it computes has a proof tree in `C` reading each of its variables at most `k` times." This matches item-angle-1's reading of it.
- `IsAO2` (S6): "The model: AND and OR gates only, each reading earlier wires, each reading exactly two wires. No constants, no NOT".

Per the repository's README (S3), the file for this step would be `lean/PEqualNP/Outside/L_meta_2583.lean`, declaring one theorem `PEqualNP.Outside.L_meta_2583`, with no `sorry` and only the axioms `propext`, `Classical.choice` and `Quot.sound`.

## What the four attempts found

**They agree on the gap; there is no disagreement to report.** Every result points at the same missing piece, which each says is identified by the sketch supplied with the step:

1. Starting from an arbitrary `IsAO2` circuit `C` for the incidence function, normalize it without increasing its size (item-angle-2 and item-angle-4 describe the move as taking wires that are below the function out of OR gates and moving them to the output).
2. Prove that each resulting block that is not a single star costs at least a star cover of the edges it accepts.

Step 2 is the lemma nobody could prove. Without it there is no way to exhibit a read-1 circuit `D` with `D.size ≤ C.size`, which is the theorem's conclusion (item-angle-3, item-angle-4).

Points made by only some of the results:

- **Where the lemma is not.** item-angle-1 and item-angle-2 report that the one project import allowed for the step, `PEqualNP.Defs`, supplies definitions and not this bound. item-angle-1 adds that it found related project results only with the normalization or a charging bound taken as an assumption. item-angle-3 reports the same of "the available prebuilt project".
- **No counterexample.** item-angle-4 looked for one and found none. It checked that the hypotheses are satisfiable at q = 2 (the Fano plane): N = 7, each line has 3 points, each pair of points lies on exactly one line. The arithmetic matches the statement: 2² + 2 + 1 = 7 and q + 1 = 3. This is evidence that the statement is not vacuous. It is not evidence that the statement is true.
- **Not a short assembly.** item-angle-2: "The incidence axioms and circuit definitions alone do not yield a short assembly proof; the central combinatorial bound remains unproved."

No result says the statement is false, and no result says a hypothesis is too weak. All four chose `missing_lemma`.

## Public state of the step when this was written

Read on 2026-11-25 between about 21:16 and 21:20 UTC. This was done for this write-up; it is not taken from the four results.

- **Still unproved at the desk.** The step's record has status `conjecture` (S1). The desk's board, updated 2026-11-25T21:16:31.289Z, lists it as an open step: level `hard`, kind `prove`, 232 points, held by 3 holders against a cap of 3, not offerable at that moment (S2).
- **No proof file on `main`.** `lean/PEqualNP/Outside/L_meta_2583.lean` returned HTTP 404 on branch `main` at commit `4888bfe559d847c71bbc9f232308fd337c3a2857` (S7).
- **No accepted pull request.** A GitHub issue search for `L-meta-2583` in the repository returned 7 pull requests, none merged (S8):
  - #13723 is open. The intake bot refused it three times with "REFUSED before any build: the theorem must stand at the top level, last, written with its full name" (S9; the rule is in S4). Its one file declares no top-level theorem. Its last lemma, `step_of_lower_bound`, reaches the step's conclusion only under an extra hypothesis `N * (q + 2) ≤ C.size + 1`, a lower bound on the size of `C` that the file does not prove (S10). I read the file and did not build it.
  - #5064, #6987, #7163, #9168, #10947 and #19757 are closed without merge. Five were offered as reductions; #19757 has only a lease line as its description. Each was closed with the message that the step is not open to reductions, for example "Closed: this step is not open to reductions (its row in the desk file does not say reductions: true), so this reduction will not be checked. A proof of the step is still welcome." (S11).
- **Whether any of these comes from this goal's contributor could not be established.** The four results name no GitHub account, lease or pull request, so none of the 7 can be attributed to this job. None of them is a checked proof in any case.

The public attempts stop at the same place as the four results. The description of #5064 calls its unproved child `blockCost` "the open part named in the sketch" (S8), and #13723 leaves a size lower bound as a hypothesis (S10). These are other contributors' statements about their own files; the checker accepted none of them.

## What could not be found or was not done

- **A Lean proof of L-meta-2583.** Not in any result, not on `main`, not in any accepted pull request.
- **Checker output.** No `ACCEPTED` or `REJECTED` line for a proof of this step from this job. No result reports running the checker.
- **A second holder's check.** Not possible without a proof file; none is reported.
- **A pull request URL from the contributor.** None in the results.
- **The contributor's GitHub account and any desk lease id.** Not in the results.
- **Whether a lease was released at the desk.** `missing_lemma` is one of the desk's release reasons (S3), but no result says a lease was held or released with it.
- **The step's sketch.** All four results refer to "the supplied sketch"; none quotes it, and the public record S1 does not carry it. Its content is known here only through the results' paraphrases above.
- **Independent verification of the mathematics.** This write-up did not test the missing lemma, search for a counterexample, or build any Lean file.

## What a further attempt would need

These are my reading of the results and sources, not instructions from the desk.

- The proving items need to be run again with the missing lemma as the explicit target: the block-cost bound in step 2 above, or any other route to `D.size ≤ C.size`. A write-up cannot close the goal; only a proof file can.
- A reduction is not a way through. The desk closes reductions on this step (S11), so the bound has to be proved inside the one file.
- The board rates the step `hard` (S2). The README describes `--hard` steps as "an open problem the attack is stuck on" (S3). Four independent attempts and seven public pull requests have not produced a checked proof, which is consistent with that rating.
- If the contributor still holds a lease and will not continue, the README's stated way to stop is to release it with the reason that fits; `missing_lemma` is what all four results support (S3).

## Sources

| # | Source | Used for |
|---|---|---|
| S1 | https://data.pequalnp.com/data/lemma/L-meta-2583.567fbafe0560.json | Title, formal statement, statement hash, status `conjecture`, empty `attempts`, proposal time |
| S2 | https://pequalnp.com/desk/board | Board entry for L-meta-2583: level, kind, points, holders, cap, `updated_at` |
| S3 | https://github.com/open-goat/pequalnp-proofs/blob/main/README.md | File path and theorem name rules, checker requirements, release reasons, `--hard` |
| S4 | https://github.com/open-goat/pequalnp-proofs/blob/main/CONTRIBUTING.md | Rule that the theorem stands outside the namespace block, last, with its full name |
| S5 | https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Defs/ReadK.lean | Definition of `IsReadK` (lines 160-163 at the commit in S7) |
| S6 | https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Defs/TopForm.lean | Definition of `IsAO2` (lines 80-83 at the commit in S7) |
| S7 | https://raw.githubusercontent.com/open-goat/pequalnp-proofs/main/lean/PEqualNP/Outside/L_meta_2583.lean and https://api.github.com/repos/open-goat/pequalnp-proofs/commits/main | 404 for the step's file; commit of `main` when read |
| S8 | https://api.github.com/search/issues?q=L-meta-2583+repo:open-goat/pequalnp-proofs | The 7 pull requests, their state, `merged_at: null`, their descriptions |
| S9 | https://github.com/open-goat/pequalnp-proofs/pull/13723 | Open pull request and the bot's three refusals |
| S10 | https://github.com/open-goat/pequalnp-proofs/pull/13723.diff | The file's content: no top-level theorem, `step_of_lower_bound` with the extra size hypothesis |
| S11 | https://github.com/open-goat/pequalnp-proofs/pull/10947 (same message on #7163, #9168, #19757; authors' own closing notes on #5064, #6987) | Reductions are not accepted on this step |
| Results | `.imd/reads/artifacts/item-angle-1` to `item-angle-4`, identified by the SHA-256 values above | Every statement attributed to a result |
