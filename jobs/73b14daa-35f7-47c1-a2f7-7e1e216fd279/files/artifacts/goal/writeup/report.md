# L-meta-4715 (pequalnp outside proof desk): write-up of four results

## 1. Outcome: the step is not proved, and nothing was opened

**The goal is not met.** The goal asks for one Lean 4 theorem proving step L-meta-4715, checked on another holder's machine, then opened as a pull request on `open-goat/pequalnp-proofs` from the proving contributor's account. None of the three exists:

| Goal requirement | State | Basis |
|---|---|---|
| Lean 4 proof of the posted statement of L-meta-4715 | **Missing** | All four results have `"status": "missing_lemma"` and each says in its first sentence that no proof was found (Appendix A). No result delivers a Lean file. |
| Check of that proof on another holder's machine | **Missing** | There is no proof to check. The Lean checks the workers report are of *other* statements (an equivalence and a conditional reduction), ran in their own scratch builds, and the scratch files were not delivered. |
| Pull request from the prover's account | **Not opened** | There is no prover. The pull requests that exist for this step are reductions by other accounts (section 5); none proves it. |

What the four results do deliver is a consistent negative finding: the step can only be true vacuously, so proving it means proving a circuit lower bound that the public repository does not have. That finding, the current state of the public desk, and what a future proof needs are below. This document cannot be merged in place of the theorem and should not be read as progress toward a merge beyond narrowing what is missing.

Markers used below: **[A1]–[A4]** a claim made by result item-angle-1 … item-angle-4 (verbatim in Appendix A); **[checked]** something I re-read or re-computed for this write-up on 2026-11-26, with its source in the Sources section; **[inference]** my own reasoning, not machine-checked.

## 2. The step

Desk record: <https://data.pequalnp.com/data/lemma/L-meta-4715.72c75318ae60.json> **[checked]**: HTTP 200; `"status":"conjecture"`; `"attempts":[]`; `"plain_statement":"Step 2 of 2 of a checked cut of L-meta-2384."`; `"statement_hash":"sha256:87a0264576c3201d65f4159d6ee50a37e038179cc28eff1e0301fcfad0322b80"`, which equals the SHA-256 of the record's `formal_statement` string as I computed it.

In the notation the workers share: G is the graph on 11 vertices with the 16 edges 0-9, 0-10, 1-4, 1-8, 2-5, 2-10, 3-6, 3-7, 4-8, 4-10, 5-8, 5-9, 6-7, 6-10, 7-9, 8-9; `blocks` is a fixed list of 23 numbers read as vertex bitmasks. For a circuit C write U = `Ustar G C`, B = 2·|`centreless`| + |`junk`| + |`orN \ lam`| (the record's `x9`), t = |`tops \ centreless`|. The statement is:

> for every circuit C with `C.size ≤ 21`, `IsLeastAO G C`, `TopForm G C`, `2 ≤ |junk|`, `|U| ≤ B`, `B < 2·|U|` and `B − |U| < 7`: there is a minimum vertex cover K of `G.deleteEdges U` such that every pairwise-disjoint list P of blocks avoiding K has weight Σ ⌈|b|/2⌉ ≤ B − |U|.

(The exact Lean text is the `formal_statement` field of the record above; the paraphrase is mine.)

## 3. What the four results establish

All four agree on the following; none contradicts another on any of it.

1. **The conclusion is false whenever the hypotheses hold, so the step is equivalent to "no circuit satisfies the hypotheses".** [A1 point 1, A2 (1), A3 points 1–2, A4 (1)]. The argument, the same in all four:
   - G has 16 edges and no 4-cycle, and every vertex cover of G has at least 7 vertices.
   - The repository's general inequality for least top-form circuits on a graph with no 4-cycle gives 16 + t + B ≤ `C.size` + |U| + 1, and |K| ≤ t for every minimum cover K of `G.deleteEdges U`. With `C.size ≤ 21`: t + B ≤ 6 + |U|.
   - `L_meta_4713`, applied at K, gives a pairwise-disjoint list P of blocks avoiding K and a set X with K ∪ X a vertex cover of G and |X| ≤ weight(P).
   - If the conclusion held for K then 7 ≤ |K| + |X| ≤ t + (B − |U|) ≤ 6. Contradiction.
   
   Each worker reports having this elaborated by Lean in a scratch build (Lean 4.36 / Mathlib / prebuilt `PEqualNP.Defs`), with no error and no `sorry`. A1 and A2 took the cited repository theorems as hypotheses copied from their statements (A2 adds that the source files of its three elaborate unchanged under the prebuilt toolchain); A3 and A4 compiled the repository's `L_meta_5781.lean` and `L_meta_4713.lean` and used them as lemmas, and report the axioms `propext`, `Classical.choice`, `Quot.sound` only. **None of these scratch files was delivered, and I did not re-run Lean**, so these are the workers' reports, not something this write-up certifies.

2. **Some hypotheses of the step are redundant.** A1: `2 ≤ |junk|`, `B < 2|U|` and `B − |U| < 7` are not used in the contradiction of point 1. A2: `x9 − |U*| < 7` "then holds automatically". A4 (2), the strongest form: `B < 2·|U|` and `B − |U| < 7` follow from `C.size ≤ 21`, `IsLeastAO` and `TopForm` alone.

3. **The first merged reduction, `R_meta_4715_12`, does not shrink the problem.** [A1 point 3, A2 (2), A3 point 3, A4 (3)]. Its "cheap" branch (a set X meeting every U-edge with |X| ≤ B − |U|) cannot occur under the hypotheses, for the same reason as point 1, so its premise named `hard` carries the whole step.

4. **What is missing is a lower bound, not a certificate.** Stated three ways across the results, each sufficient:
   - *Regime emptiness* [A2, A3 "L\*", A4 "R"]: no circuit C with `C.size ≤ 21`, `IsLeastAO G C`, `TopForm G C`, at least two junk gates and `|U| ≤ B < 2|U|` exists (A4's form R omits `B < 2|U|` as derivable). A2 and A4 describe it as a 22-gate lower bound for this graph in this regime.
   - *Charging lemma on U* [A1 "M", A3 4(b)]: for such C there is X meeting every U-edge with |X| + |U| ≤ B. A1 reports Lean accepting "`L_meta_7862` and M imply the exact posted statement".
   - *Charging lemma on G* [A4]: for such C there is a vertex cover X of G with |X| + |U| ≤ t + B. The repository has exactly this conclusion for `|junk| = 1` in `L_meta_8103` [A1, A3, A4; statement **[checked]**, section 6]. No result found it for two or more junk gates.
   
   A possible starting point named by two results: by the contrapositive of `L_meta_6240`, `B < 2|U|` forces some gate of `centreless ∪ junk ∪ mixing` to have two U-edges in its `gammaE` [A1 point 4, A3 4(a)]. A4 names `L_meta_8005` as another possible input.

5. **Counting alone does not close it.** [A2, A3 4(c)]. Edge sets U and values of B survive every numeric constraint the workers derived; the smallest are two-edge matchings such as U = {0-9, 1-4} with B = 3 and cover number 5 for G − U. A3 counts 26196 surviving edge sets with |U| ≤ 7 and 16 surviving two-edge matchings; larger U were not enumerated.

6. **No evidence the step is false.** All four say so explicitly and none claims it is true either. It is false exactly if a least top-form circuit with at most 21 gates exists in the regime; nobody found one or excluded one. A4 adds an exhaustive search with its own program on six small graphs (triangle 4 gates, path on 4 vertices 4, triangle with a pendant 5, bull 6, triangle with a 2-edge tail 7, 5-cycle 7), each equal to edges + cover number − 1, the analogue of 16 + 7 − 1 = 22 for G. That is an analogy, not a proof.

## 4. Where the results differ

No two results conflict on a fact. They differ in these ways:

- **Which repository theorem supplies the inequality.** A1 cites `L_meta_7862`; A2, A3, A4 cite `L_meta_5781`. Both exist, and **[checked]** their final statements have the same conclusion; `L_meta_7862` is stated with `x2.edgeSet.ncard` and the hypothesis `∃ x6 x7, x2.Adj x6 x7`, `L_meta_5781` with `x2.edgeFinset.card` and `x2.edgeFinset.Nonempty`. This also accounts for A1 proving `16 ≤ G.edgeSet.ncard` where A4 proves `G.edgeFinset.card = 16`.
- **Which hypotheses the equivalent statement keeps.** A3's L\* keeps `B < 2|U|`; A4's R drops it and `B − |U| < 7` as derivable (point 2 above). These are compatible: A4's claim is the stronger one and A3 does not deny it.
- **Form of the missing lemma.** Three forms (point 4 above). A1's M as written has no `C.size ≤ 21` premise and no window, so it is a stronger claim than the step needs; A1 notes it may be weakened by adding them. Whether the unweakened M is true is not addressed by any result.
- **How the cover bound was checked.** A1: `omega` on 11 edge constraints after splitting G into two triangles and a 5-cycle, plus a script; A3 and A4: `decide` over all 2048 subsets; A2: the repository's `L_meta_2693`.
- **Repository files read for sub-cases.** A2 lists `L_meta_2264, 4899, 4901, 5228, 5966, 7465, 7467, 7559, 7897`; A3 describes `L_meta_7467` and `L_meta_5855`. Both conclude the proved sub-cases carry extra hypotheses and do not cover the regime.
- **Suggested next step.** A2 gives a helper split (a)–(d); A3 and A4 suggest re-posting the step as L\*/R or as the charging lemma. A4 states that 4715 then follows "in about 15 lines" and that it has that proof elaborated; the proof text is not in the result.

## 5. State of the public repository and desk (read 2026-11-26)

The workers read the repository at commit `e125f04d` **[checked: this is `e125f04d0dc6fed67cee48a1d06692912e167c32`, committed 2026-11-25T15:47:48Z; the name `brilliant-hq/pequalnp-proofs` that A2 uses answers HTTP 301 to `open-goat/pequalnp-proofs`]**. The repository has moved since. When I read it, the head of `main` was `5a44ec9d26fd1819460df66718a6353124ccba50` (2026-11-26T00:27:14Z). **[checked]**:

- **No proof file.** `lean/PEqualNP/Outside/L_meta_4715.lean`, `L_meta_17395.lean` and `L_meta_17397.lean` all answer HTTP 404 on `main`. (Proved steps are stored as `lean/PEqualNP/Outside/L_meta_<n>.lean` with a theorem `PEqualNP.Outside.L_meta_<n>`, e.g. `L_meta_8103.lean` line 2827, so the expected theorem is `PEqualNP.Outside.L_meta_4715`.)
- **Pull requests whose title names L-meta-4715** (GitHub search, 5 hits). All five add a file named `R_meta_4715_<k>.lean`, i.e. a reduction; none adds `L_meta_4715.lean`:

  | PR | Author | State | File added |
  |---|---|---|---|
  | [#9486](https://github.com/open-goat/pequalnp-proofs/pull/9486) | yaboijbigs | merged 2026-11-25T03:24:11Z, commit `356d54f4…` | `R_meta_4715_12.lean` (113 lines) |
  | [#22148](https://github.com/open-goat/pequalnp-proofs/pull/22148) | scarbain | merged 2026-11-25T23:13:02Z, commit `789af578134b855a76a37ea7f50757657b1ad1aa` | `R_meta_4715_619.lean` (1905 lines) |
  | [#9132](https://github.com/open-goat/pequalnp-proofs/pull/9132), [#11882](https://github.com/open-goat/pequalnp-proofs/pull/11882) | gperdigao | closed, not merged | `R_meta_4715_421.lean` (36 lines) |
  | [#9596](https://github.com/open-goat/pequalnp-proofs/pull/9596) | 0xshuzo | closed, not merged | `R_meta_4715_215.lean` (42 lines) |

  The three unmerged ones carry an automatic comment that the checker accepted the reduction but did not record it because the author already had five open reductions.
- **`R_meta_4715_619` is conditional.** At the merge commit ([file](https://github.com/open-goat/pequalnp-proofs/blob/789af578134b855a76a37ea7f50757657b1ad1aa/lean/PEqualNP/Outside/R_meta_4715_619.lean), 100710 bytes, SHA-256 `04bfd65b2ce371909c446863de9999fdcc79350884ef36837012bbd3c5c42d00`, no occurrence of `sorry`) the theorem takes two premises, `twoJunk` (lines 9–19, `(junk G C).card = 2`) and `manyJunk` (lines 20–30, `3 ≤ (junk G C).card`), and its proof calls them at lines 1878 and 1886. From the lines I read (1–45 and 1795–1905), the reduction itself discharges the cheap branch, the case `orN \ lam = ∅` and the case `centreless = ∅ ∧ |orN \ lam| ≤ 1`, and hands the rest to the two premises. I did not read lines 46–1794 and did not compile the file.
- **Its two premises are posted as steps and are unproved.** <https://data.pequalnp.com/data/lemma/L-meta-17395.98a51e5013ca.json> ("Step 1 of 2 of a checked cut of L-meta-4715.") and <https://data.pequalnp.com/data/lemma/L-meta-17397.bbdd1c6cc369.json> ("Step 2 of 2 of a checked cut of L-meta-4715.") both answer HTTP 200 with `"status":"conjecture"`, `"attempts":[]`, `"proposed_at":"2026-11-25T23:12:53.820Z"`. A title search for either id in the repository's pull requests returns 0.
- **This cut postdates the workers' reading.** `e125f04d` is from 15:47 UTC on 2026-11-25 and #22148 merged at 23:13 UTC, so none of the four results mentions `R_meta_4715_619` or the two new steps; their remarks about "the repository's reduction" are about `R_meta_4715_12`.

**[inference]** The workers' point-1 argument applies unchanged to both new steps. Each asks, for a circuit C with `C.size ≤ 21`, `IsLeastAO`, `TopForm` and `|U| ≤ B`, for a minimum cover K of `G.deleteEdges U` and a set X with K ∪ X a vertex cover of G and |X| ≤ B − |U|. Then |K ∪ X| ≤ t + (B − |U|) ≤ 6, against the cover number 7. So L-meta-17395 and L-meta-17397 are again true only vacuously: they are the regime-emptiness statement of section 3 point 4, split by `|junk| = 2` / `|junk| ≥ 3`, with the three sub-cases above removed. The second cut removes cases but leaves the same kind of lower bound open. I did not check this in Lean.

## 6. Figures re-checked for this write-up

| Figure or claim | From | Re-check |
|---|---|---|
| G has 11 vertices and 16 distinct edges | A1–A4 | **[checked]** by script from the edge list in the desk record |
| G has no 4-cycle | A1–A4 | **[checked]**: no two vertices have two common neighbours |
| Every vertex cover of G has ≥ 7 vertices; {1,3,5,6,8,9,10} is a cover of size 7 | A1 (A2–A4 for the bound) | **[checked]** by exhaustive search over vertex subsets |
| Triangles {1,4,8}, {3,6,7} and 5-cycle 0-9-5-2-10 | A1 | **[checked]** against the edge list; the three vertex sets partition the 11 vertices |
| The block list has 23 entries | (statement) | **[checked]** |
| 26196 edge sets with \|U\| ≤ 7 pass max(\|U\|,3) ≤ B ≤ min(2\|U\| − 1, 6 + \|U\| − τ(G − U)); the smallest are 16 two-edge matchings, e.g. {0-9, 1-4}, with τ(G − U) = 5 | A3 (example also A2) | **[checked]**: my own enumeration under exactly that constraint gives 26196 in total and 16 of size 2, all matchings, all with τ(G − U) = 5, {0-9, 1-4} among them |
| 16 + 7 − 1 = 22 | A4 | arithmetic |
| Six small graphs: least circuit size = edges + cover number − 1 | A4 | **Not reproduced.** I only confirmed that the six stated sizes equal edges + cover number − 1 for the named graphs |
| `L_meta_4901.lean` is 512040 bytes | A3 | **[checked]** on `main` |
| Sub-case files "run up to about 9400 lines" | A2 | **[checked]**: `L_meta_4901.lean` 9374 lines, `L_meta_2264.lean` 9323 |
| A proof file may be at most 524288 bytes and may import only `PEqualNP.Defs` | A2, A3 | **Not verified**; I did not find or read the desk's submission rules |
| `L_meta_8103` assumes `(junk).card = 1` | A1, A3, A4 | **[checked]**: line 2827 ff.; its conclusion is `∃ x11, IsVertexCover x2 x11 ∧ x11.card + (Ustar).card ≤` t + B, for a least top-form circuit on any graph with no 4-cycle, at least one edge and `Ustar` nonempty |
| Statements of `L_meta_5781`, `L_meta_7862`, `L_meta_4713`, `L_meta_2693`, `L_meta_6240` are as the workers paraphrase them | A1–A4 | **[checked]** by reading each final theorem statement on `main`; none of the five files contains `sorry`. Not compiled |
| A2's table f = [0,0,2,4,5,7,8,9,11,12,13,14,16,17,18,19,21] and bounds 2 ≤ \|U\*\|, 3 ≤ x9 from `L_meta_6103`, `L_meta_6838` | A2 | **Not verified** (both files exist on `main`; I did not read their statements) |
| Every Lean elaboration the workers report | A1–A4 | **Not reproduced**: no Lean was run for this write-up and the scratch files were not delivered |

## 7. What could not be found

- A proof of L-meta-4715, of regime emptiness, or of either charging lemma for two or more junk gates: in no result, and not on `main` under the file names above.
- A circuit with at most 21 gates in the regime (which would refute the step): in no result.
- Any record of a check by a second holder, and any pull request by a prover: neither exists because no proof exists.
- The desk record of the parent L-meta-2384: I do not have its content-addressed URL, and the un-suffixed URL `https://data.pequalnp.com/data/lemma/L-meta-2384.json` answers 404, so I state nothing about its status. `lean/PEqualNP/Outside/L_meta_2384.lean` answers 404 on `main`.
- The workers' scratch Lean files and the texts of their conditional proofs: reported, not delivered.

## 8. Hand-off for whoever continues

1. Do not look for a witness. No choice of K and no packing certificate proves the step (section 3 point 1). A proof must derive `False` from the circuit hypotheses.
2. The live targets on the desk are now L-meta-17395 (`|junk| = 2`) and L-meta-17397 (`|junk| ≥ 3`). If both are proved, `R_meta_4715_619` yields L-meta-4715; the final `L_meta_4715.lean` would still have to be written, checked on a second holder's machine and opened as a pull request by its prover.
3. For each of the two, it is enough to prove one of: `22 ≤ C.size` in that case; a set X meeting every U-edge with |X| + |U| ≤ B (this directly contradicts the premise both new steps carry, that every such X has |X| > B − |U|); or a vertex cover X of G with |X| + |U| ≤ t + B, the conclusion `L_meta_8103` has for one junk gate.
4. Starting facts the results point to: `L_meta_6240` (some gate of `centreless ∪ junk ∪ mixing` carries two U-edges), `L_meta_8005`, `L_meta_8103` as a template, and the existing two-junk sub-case files listed in section 4. The smallest numerically surviving case is |U| = 2, B = 3, t = 5, size 21 [A2].

## Sources

Read on 2026-11-26. Repository files other than `R_meta_4715_619.lean` were read from branch `main` (head `5a44ec9d26fd1819460df66718a6353124ccba50` when I read it).

- Desk records: <https://data.pequalnp.com/data/lemma/L-meta-4715.72c75318ae60.json>, <https://data.pequalnp.com/data/lemma/L-meta-17395.98a51e5013ca.json>, <https://data.pequalnp.com/data/lemma/L-meta-17397.bbdd1c6cc369.json>
- Pull requests: <https://github.com/open-goat/pequalnp-proofs/pull/22148>, <https://github.com/open-goat/pequalnp-proofs/pull/9486>, <https://github.com/open-goat/pequalnp-proofs/pull/9132>, <https://github.com/open-goat/pequalnp-proofs/pull/11882>, <https://github.com/open-goat/pequalnp-proofs/pull/9596>
- Reductions: <https://github.com/open-goat/pequalnp-proofs/blob/789af578134b855a76a37ea7f50757657b1ad1aa/lean/PEqualNP/Outside/R_meta_4715_619.lean>, <https://github.com/open-goat/pequalnp-proofs/blob/main/lean/PEqualNP/Outside/R_meta_4715_12.lean> (9204 bytes, SHA-256 `dbd0918d82e0182df54cf777187bf82460faa661eb6792e96f6b416f28d85904`)
- Proved steps cited by the workers, under <https://github.com/open-goat/pequalnp-proofs/tree/main/lean/PEqualNP/Outside>: `L_meta_5781.lean`, `L_meta_7862.lean`, `L_meta_4713.lean`, `L_meta_2693.lean`, `L_meta_6240.lean`, `L_meta_8103.lean` (statements read); `L_meta_4901.lean`, `L_meta_2264.lean` (size and line count only); `L_meta_6103.lean`, `L_meta_6838.lean`, `L_meta_8005.lean`, `L_meta_4899.lean`, `L_meta_5228.lean`, `L_meta_5966.lean`, `L_meta_7465.lean`, `L_meta_7467.lean`, `L_meta_7559.lean`, `L_meta_7897.lean`, `L_meta_5855.lean` (existence only)
- Commit the workers read: <https://github.com/open-goat/pequalnp-proofs/commit/e125f04d0dc6fed67cee48a1d06692912e167c32>
- The four results, Appendix A.

## Appendix A. The four results, verbatim

Each result is a JSON object with the two fields `status` and `notes`. The `notes` string is reproduced with its JSON escapes decoded and nothing else changed. The SHA-256 is of the input file as handed to this step.

### A1. item-angle-1 (`artifacts/goal/items/angle-1/result.json`)

- SHA-256: `d012393212b6cfd5ac4e38fb6a0d8c9c002d8a7388e51457732591afce0434cd`
- `status`: `missing_lemma`
- `notes`:

~~~~text
NOT PROVED; no Lean file is offered. What I established, each point elaborated with the prebuilt Lean 4.36 / Mathlib / PEqualNP.Defs in a scratch file (no error, no sorry). The Outside modules are not prebuilt, so the statements of the repo's L_meta_7862 and L_meta_4713 were copied verbatim as hypotheses; their proofs were not re-elaborated here.

Notation: G the posted graph, U = Ustar G C, t = |tops \ centreless|, B = 2*|centreless| + |junk| + |orN \ lam| (the posted x9).

1. Under the step's own hypotheses the conclusion is false, so the step holds iff its hypotheses are inconsistent.
 - Every vertex cover of G has at least 7 vertices: the triangles {1,4,8} and {3,6,7} need 2 each and the 5-cycle 0-9-5-2-10 needs 3 (Lean: omega on 11 edge constraints). {1,3,5,6,8,9,10} is a cover of size 7 and no 6-set covers (script). G has 16 edges and NoFourCycle G holds (decide +kernel).
 - L_meta_7862 gives 16 + t + B <= C.size + |U| + 1 and |K| <= t for every IsMinCover K of G.deleteEdges U.
 - If K is as in the conclusion, L_meta_4713 at K gives a list P of disjoint blocks avoiding K and a set x5 with K ∪ x5 a vertex cover of G and |x5| <= value(P) <= B - |U|. With C.size <= 21 and |U| <= B: 7 <= |K| + |x5| <= t + B - |U| <= 6.
 Lean accepted: (h7862) (h4713) : ∀ C, C.size ≤ 21 → IsLeastAO G C → TopForm G C → U.card ≤ B → ¬ ∃ K, IsMinCover (G.deleteEdges ↑U) K ∧ ∀ P, (pairwise disjoint, in the block list, avoiding K) → value P ≤ B - U.card. The premises 2 ≤ junk, B < 2|U| and B - |U| < 7 are not used.

2. So the step is exactly the lower-bound claim: no IsLeastAO, TopForm circuit with at most 21 gates for G has at least 2 junk gates and |U| <= B < 2|U|. A direct proof (unfold the definitions, find the Mathlib lemma) cannot exist in the sense of my angle: the existential in the conclusion can never be witnessed, and any proof must derive False from the circuit hypotheses. That is circuit-structure work of the kind the repo does in L_meta_8103 (one junk gate) and in its long two-junk-gate files; Defs and Mathlib alone do not carry it and I did not get there.

3. In the repo's reduction R_meta_4715_12 the cheap branch (some X covering U with |X| <= B - |U|) is contradictory for the same reason as point 1, so all the content of the step sits in its hypothesis named hard.

4. The missing lemma, sufficient and machine-checked as such. M: ∀ C, IsLeastAO G C → TopForm G C → 2 ≤ (junk G C).card → ∃ X : Finset (Fin 11), (∀ u v, s(u, v) ∈ Ustar G C → u ∈ X ∨ v ∈ X) ∧ X.card + (Ustar G C).card ≤ B. This is the analogue for 2 or more junk gates of L_meta_8103, which assumes (junk).card = 1. Lean accepted: (h7862) (hM : M) : the exact posted statement. Proof: take a minimum cover K of G.deleteEdges U (Nat.find); K ∪ X covers G; 7 <= |K| + |X| <= t + B - |U| <= 6; False. M may also be weakened by adding the window |U| <= B < 2|U| and C.size <= 21 to its premises. By L_meta_6240 (read, not re-elaborated), B < 2|U| forces some gate of centreless ∪ junk ∪ mixing to have two U-edges in its gammaE; a proof of M on the window would start there.

5. Not established: whether the step is true. It is false exactly if a least, TopForm circuit with at most 21 gates exists in the window. I found neither such a circuit nor a proof that none exists, so I do not claim statement_seems_false.

Scratch theorems that Lean accepted: nf (NoFourCycle G), tau (cover ≥ 7), ecard (16 ≤ G.edgeSet.ncard), contra (point 1), cond (point 4).
~~~~

### A2. item-angle-2 (`artifacts/goal/items/angle-2/result.json`)

- SHA-256: `b553bbb3cd93bd16b948ec989d785811eb76d398d0b66dee1d7c213d35329af5`
- `status`: `missing_lemma`
- `notes`:

~~~~text
Not proved. The step is true if and only if its hypotheses are contradictory, and that contradiction is a lemma the repository does not have.

Checked with the prebuilt Lean 4.36.0 and Mathlib (scratch files outside the workspace, no error, no sorry; not delivered):

(1) Equivalence. With the posted statements of three repository theorems as hypotheses, the step's statement implies the same statement with its conclusion replaced by False; the converse is False.elim. The three are L_meta_5781 (NoFourCycle graph, least top-form circuit: |E| + |tops\centreless| + 2|centreless| + |junk| + |orN\lam| <= size + |U*| + 1, and every min cover K of G minus U* has |K| <= |tops\centreless|), L_meta_4713 (this graph and block list: for every S there are a pairwise-disjoint list P of blocks avoiding S and a set T with S u T a vertex cover of G and |T| <= weight of P) and L_meta_2693 (a vertex cover of G minus X has at least 7 - |X| vertices). Argument: |E| >= 16 and size <= 21 give |tops\centreless| + (x9 - |U*|) <= 6; the witness x13 = K has |K| <= |tops\centreless|; L_meta_4713 at S = K gives P, T with |T| <= weight(P) <= x9 - |U*| by the step's own conclusion; so K u T covers G with at most 6 vertices, against 7. NoFourCycle for this graph goes by decide, 16 <= |E| by an explicit 16-edge subset. The three source files elaborate unchanged under the prebuilt toolchain (only PEqualNP.Defs is prebuilt; Outside files are source only).

(2) Narrowing. With L_meta_5781, L_meta_2693, L_meta_6103 and L_meta_6838 as hypotheses (those two files also elaborate unchanged), the step's hypotheses force: 2 <= |U*|; 3 <= x9; x9 <= 1 + f(|U*|) with f = [0,0,2,4,5,7,8,9,11,12,13,14,16,17,18,19,21]; |tops\centreless| + x9 <= 6 + |U*|; and every vertex set X meeting all edges of U* has |X| > x9 - |U*|. A min cover of G minus U* is obtained by Nat.find. The last item means the cheap branch of the repository's reduction R_meta_4715_12 never occurs under the hypotheses, so its premise named hard is the whole step.

Missing lemma: for this 11-vertex, 16-edge graph there is no circuit C with C.size <= 21, IsLeastAO, TopForm, at least two junk AND gates and |U*| <= x9 < 2|U*| (x9 - |U*| < 7 then holds automatically). That is a 22-gate lower bound in this regime. Given it, the step follows in one line.

Why counting does not close it: a brute-force check over edge sets (python, this run) finds values passing every inequality above, the first being U* = {0-9, 1-4} with cover number 5 for G minus U* (cover number 2 for U*), x9 = 3, |tops\centreless| = 5, size 21. So each surviving (|U*|, x9) case needs structural analysis of the junk gates. The repository's results on this graph that I read (L_meta_2264, L_meta_4899, L_meta_4901, L_meta_5228, L_meta_5966, L_meta_7465, L_meta_7467, L_meta_7559, L_meta_7897) each carry extra hypotheses (junk = {a, b} with a fixed cone relation, a given shape of the U*-edges, fixed cardinalities), run up to about 9400 lines for one sub-case, and do not together cover the regime; a search of the Outside tree found no unconditional 22 <= size theorem for this graph. A from-scratch proof of that bound was not attempted: it is out of reach of this run and of one 524288-byte file built only on PEqualNP.Defs.

Helper split for whoever continues (the angle asked for): (a) the L_meta_5781 instance for this graph, (b) existence of a min cover of G minus U*, (c) the numeric narrowing in (2), all checked as above; (d) the missing regime-emptiness lemma; then the theorem is False.elim.

I found no evidence that the statement is false: that would need a least circuit of size <= 21 for this graph in this regime, and I have neither such a circuit nor a proof that none exists. Sources quote the repository files at the commit the prebuilt project names (brilliant-hq/pequalnp-proofs e125f04d).
~~~~

### A3. item-angle-3 (`artifacts/goal/items/angle-3/result.json`)

- SHA-256: `94fe13802cbb9bc8d020eeb9fb52754285dc31fc80b45ddc2eb78b8d97cd9890`
- `status`: `missing_lemma`
- `notes`:

~~~~text
Not proved. The step gave no sketch, context or dead list, so I worked from the definitions and the steps already proved in the repository. Result: the posted conclusion can never hold under the posted hypotheses, so the step is exactly one missing lemma, which I could not prove. Points 1, 2 and 4a were checked in Lean 4.36 in a scratch build (L_meta_5781, L_meta_4713, L_meta_6240 compiled from the prebuilt project sources and brought in; axioms propext, Classical.choice, Quot.sound only). Those scratch files are not a submittable proof file and are not delivered.

Write G for the 11-vertex graph, U = Ustar G C, B = 2*|centreless| + |junk| + |orN \ lam|, t = |tops \ centreless|.

1. Equivalence (Lean-checked: step <-> L*). L*: for every circuit C with C.size <= 21, IsLeastAO G C, TopForm G C, 2 <= |junk|, |U| <= B and B < 2*|U|: False. So the step says precisely that no least top-form circuit of size <= 21 with at least two junk gates has |U| <= B < 2|U|. No choice of the minimum cover x13 and no packing certificate proves it; only refuting the hypotheses does.

2. Why the conclusion is unsatisfiable (Lean-checked). (a) G has no 4-cycle and 16 edges (decide), so L_meta_5781 gives 16 + t + B <= C.size + |U| + 1 and |K| <= t for every minimum cover K of G.deleteEdges U; with size <= 21 this is t + B <= 6 + |U|. (b) L_meta_4713 at x3 := K gives a packing P of blocks avoiding K and a set X with K ∪ X a vertex cover of G and |X| <= weight(P). (c) every vertex cover of G has at least 7 vertices (decide over the 2048 subsets). Hence weight(P) >= 7 - |K| >= 7 - t >= B - |U| + 1, so the required bound weight <= B - |U| fails for every minimum cover K. Proof script: obtain the two parts of L_meta_5781 11 G C; obtain P, X from L_meta_4713 K; apply (c) to K ∪ X; Finset.card_union_le; omega. The hypothesis x9 - x8.card < 7 is redundant (B - |U| <= 6 - t).

3. Consequence for R_meta_4715_12. Its cheap branch (a set X meeting every U-edge with |X| <= B - |U|) cannot occur under the hypotheses either: K ∪ X would cover G with at most t + B - |U| <= 6 < 7 vertices. Its hypothesis `hard` keeps the same unsatisfiable conclusion, so that reduction does not shrink the problem: what is left is L* itself.

4. What L* needs. (a) By the contrapositive of L_meta_6240 (Lean-checked), B < 2|U| forces a gate g in centreless ∪ junk ∪ mixing with at least two U-edges in gammaE g. (b) The missing content is a charging bound for that situation: |U| + tau(U) <= B, where tau(U) is the least number of vertices meeting every U-edge (then K ∪ X has at most 6 vertices, contradiction), or directly 22 <= C.size. L_meta_8103 gives the analogous bound only for |junk| = 1. (c) Numbers alone do not close it. Using B >= 3 (two junk gates plus L_meta_6838, not re-checked by me) the constraints are max(|U|,3) <= B <= min(2|U| - 1, 6 + |U| - tau(G - U)). My own enumeration over edge sets with |U| <= 7 finds 26196 sets U that pass; the smallest are 16 two-edge matchings such as {0-9, 1-4} with B = 3 and tau(G - U) = 5. Larger U were not enumerated.

5. Why I stopped. The repository's case steps for this graph that I read (L_meta_7467: size <= 21, |U| = 3, 5 tops, no centreless, 3 junk, one gate in orN \ lam, a minimum cover of size 5 -> False; L_meta_5855: |U| = 2, t >= 5, 3 <= |junk| and further side conditions -> 22 <= size) each assume structure that is not derivable from this step's hypotheses, and I found no set of proved steps that covers L*. They also cannot be carried in one file: L_meta_4901 alone is 512040 bytes of the 524288 allowed, and a proof file may bring in only PEqualNP.Defs. I have no circuit of size <= 21 for this graph, so I do not claim the statement is false.

Suggested re-posting: replace this step by L* (or by 22 <= C.size under the same hypotheses) and split it by the heavy gate of 4a (centreless, junk or mixing) and by how its U-edges meet.
~~~~

### A4. item-angle-4 (`artifacts/goal/items/angle-4/result.json`)

- SHA-256: `bbb1188e710a466704e64ef719a1146ad8efa65ffa6d417ac8e137ba6d327d64`
- `status`: `missing_lemma`
- `notes`:

~~~~text
Neither proved nor refuted. Verdict for this angle: the statement can hold only vacuously; proving it is the same as proving that no circuit meets its hypotheses.

CHECKED IN LEAN (scratch directory, prebuilt Lean 4.36 / Mathlib / PEqualNP.Defs; I compiled the desk's own L_meta_5781.lean and L_meta_4713.lean unchanged and used them as lemmas; my scratch theorems depend only on propext, Classical.choice, Quot.sound). Write G for the step's graph x1, U = Ustar G C, B = 2*(centreless G C).card + (junk G C).card + (orN G C \ lam G C).card.
(1) The posted statement, verbatim, is equivalent to
  R: ∀ C, C.size ≤ 21 → IsLeastAO G C → TopForm G C → 2 ≤ (junk G C).card → U.card ≤ B → False.
(2) From C.size ≤ 21, IsLeastAO and TopForm alone: B < 2*U.card and B - U.card < 7. Those two hypotheses of the step are redundant.
(3) Under the step's hypotheses every X that meets all edges of U has B - U.card < X.card. So the `hard` child of the earlier reduction R_meta_4715_12 adds a hypothesis that is already implied: that child is again equivalent to R, no easier.

WHY (1). L_meta_5781 (NoFourCycle G by decide; G.edgeFinset.card = 16 by decide +kernel) gives 16 + t + B ≤ C.size + U.card + 1, and K.card ≤ t for every minimum cover K of G.deleteEdges U, where t = (tops G C \ centreless G C).card. With size ≤ 21: K.card + (B - U.card) ≤ 6. L_meta_4713 at x3 = K gives a list P of pairwise disjoint blocks avoiding K and a set X with K ∪ X a vertex cover of G and X.card ≤ weight(P). Every vertex cover of G has at least 7 vertices (all 2048 subsets, decide +kernel). So weight(P) ≥ 7 - K.card > B - U.card: for every minimum cover K an admissible packing breaks the bound, i.e. the conclusion is false whenever the hypotheses hold. The converse is ex falso.

CAN IT BE FALSE? Only if R fails, which needs an AND/OR circuit with exactly two inputs per gate computing the edge function of G with at most 21 gates. The cover construction gives 16 + 7 - 1 = 22. I cannot search 21 gates on 11 inputs. Small cases, exhaustive search over all such circuits with my own C program: triangle 4 gates, path on 4 vertices 4, triangle with a pendant 5, bull 6, triangle with a 2-edge tail 7, 5-cycle 7; each is exactly edges + cover number - 1, so in these analogues 'least and one gate below the cover construction' is unsatisfiable. No counterexample found and no evidence the step is false; I do not claim it is true either.

WHAT IS MISSING. R is the 22-gate lower bound for least top-form circuits with at least two junk gates. By L_meta_5781 it would follow from a charging lemma: for such C there is a vertex cover X of G with X.card + U.card ≤ t + B. The desk has this for (junk G C).card = 1 (L_meta_8103); I found no proved file in lean/PEqualNP/Outside at this commit that gives it for two or more junk gates. A possible input is L_meta_8005 (every U edge meets both sides of some junk gate). I did not prove that lemma: it needs a new argument about how junk gates pay for U edges, not a finite check.

SUGGESTION. Post R, or the charging lemma, as the step. 4715 then follows in about 15 lines from L_meta_5781 and L_meta_4713 (I have that proof elaborated), and its parent 2384 with it. Splitting 4715 further on K or on covers of U, as R_meta_4715_12 does, cannot help, because of (3).
~~~~
