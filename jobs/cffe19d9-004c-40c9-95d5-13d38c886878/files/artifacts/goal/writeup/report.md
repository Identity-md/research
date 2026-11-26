# Step L-meta-5813 (proof desk pequalnp): write-up of four results

## Status: the goal is not met

**Step L-meta-5813 is not proved.** None of the four results contains a Lean proof of `PEqualNP.Outside.L_meta_5813`. Because there is no proof, no other holder's machine has checked one, and no pull request adding `lean/PEqualNP/Outside/L_meta_5813.lean` has been opened on `open-goat/pequalnp-proofs`. All three things the goal asks for are missing, and this write-up cannot supply them: it reports what the four results found, what I could confirm against the public repository, and what is still needed.

| The goal asks for | Delivered? | Evidence |
|---|---|---|
| One Lean 4 theorem proving the step | No | Results 1–3 report status `missing_lemma`; result 4 reports `out_of_time`. Each says in its first sentence that the step is not proved (records R1–R4 below). |
| A check of that proof on another holder's machine | No | There is no proof file to check. No result reports one. |
| A pull request from the proving contributor's account | No | No file `L_meta_5813.lean` on `main` at commit `7af82fd` (S1), and no pull request adding that file found (S6). |

Nobody claims the statement is false. Results 1, 2 and 3 say so explicitly, and result 4 opens with "Not proved and not refuted".

The rest of this report is evidence for a decision on what to do next. It is not a substitute for the proof.

## The step

This is the statement as it stands as the conclusion of the merged reduction file `R_meta_5813_73.lean` (S2). The desk's rules say a reduction's conclusion "is the step's statement exactly" (S8):

~~~~lean
(∀ (x1 : PEqualNP.CircuitLowerBounds.Circuit) (x2 x3 : Fin (13 : ℕ)) (x4 : Bool),   PEqualNP.MetaComplexity.Monotone2 x1 →     PEqualNP.MetaComplexity.NestedCover.ReadsBack (27 : ℕ) x1 →       (2 : ℕ) ≤ PEqualNP.TopForm.andPairs (27 : ℕ) x1 →         have x8 : Finset (Fin (13 : ℕ)) := {(0 : Fin (13 : ℕ)), (1 : Fin (13 : ℕ)), (3 : Fin (13 : ℕ)), (9 : Fin (13 : ℕ))};         have x9 : Finset (Fin (13 : ℕ)) → Finset (Fin (13 : ℕ)) → List Bool := fun (x9 x10 : Finset (Fin (13 : ℕ))) => ((List.ofFn fun (x11 : Fin (13 : ℕ)) => Decidable.decide (x11 ∈ x9)) ++ List.ofFn fun (x11 : Fin (13 : ℕ)) => Decidable.decide (x11 ∈ x10)) ++ [x4];         (∀ (x10 x11 : Fin (13 : ℕ)), x10 - x11 ∈ x8 → x10 ≠ x2 ∨ x11 ≠ x3 → x1.eval (x9 {x10} {x11}) = Bool.true) → (∀ (x11 : Finset (Fin (13 : ℕ))), x11.card = (4 : ℕ) → (∀ (x13 : Fin (13 : ℕ)), {x14 ∈ x11 | x14 - x13 ∈ x8}.card ≤ (2 : ℕ)) → x1.eval (x9 x11 {x14 : Fin (13 : ℕ) | ∀ x15 ∈ x11, x15 - x14 ∉ x8}) = Bool.false) → (∀ (x12 x13 x14 x15 : Fin (13 : ℕ)), x12 - x14 ∉ x8 → x12 - x15 ∉ x8 → x13 - x14 ∉ x8 → x13 - x15 ∉ x8 → x1.eval (x9 {x12, x13} {x14, x15}) = Bool.false) → (63 : ℕ) ≤ x1.size)
~~~~

In words: a circuit `x1` of AND and OR gates (`Monotone2`), satisfying `ReadsBack 27`, with at least two nested AND pairs (`2 ≤ andPairs 27 x1`), reads 13 point bits, 13 line bits and one spare bit `x4`. Point `a` lies on line `b` when `a - b ∈ {0, 1, 3, 9}` in `Fin 13`. If the circuit

1. accepts every incident point–line pair other than the one pair `(x2, x3)`,
2. rejects every input made of four points, no three on a line, together with the lines that miss all four, and
3. rejects every input of two points and two lines with no incidence among them,

then it has at least 63 gates.

I did not obtain the desk's own posted text of the statement (the results refer to a `step.json` that is not among the inputs). I did confirm that the text above is character-for-character the statement of the two proved sibling steps with only the `andPairs` clause changed from `= 0` (L_meta_5809) or `= 1` (L_meta_5811) to `2 ≤` (S3, S4; my comparison).

## What the four results did

| | Result 1 | Result 2 | Result 3 | Result 4 |
|---|---|---|---|---|
| Status | `missing_lemma` | `missing_lemma` | `missing_lemma` | `out_of_time` |
| Proof file produced | No | No | No | No |
| Statement elaborated in Lean 4.36.0 | Yes, proof left open | Yes, placeholder body | Yes, placeholder proof | No Lean file written |
| Other machine checks | `andPairs = 2` for a 3-gate circuit, by `decide` | Cited project files byte-identical to prebuilt copies | None | Python model and SAT searches, not Lean |
| Counterexample found | No | No | No | No |

The Lean runs in results 1–3 confirm only that the statement parses and type-checks. A statement elaborated with a placeholder is not a proof, and under the repository's rules a file containing `sorry` is refused (S7).

## What the checks establish

Each row gives the claim, where it comes from, and whether I could confirm it independently. "Confirmed" means I re-derived it from the public repository at commit `7af82fd1b4e6fe6f792586b2c5aaddd8d264b377` or by direct computation; it does not mean checked in Lean.

| Claim | Source | Independent check |
|---|---|---|
| The step is the third branch of a split on `andPairs`: `flat` (`= 0`), `single` (`= 1`), `several` (`2 ≤`) | R2 | Confirmed: `R_meta_2341_417.lean` has hypotheses named `flat`, `single`, `several` with those clauses (S5). |
| The two sibling cases are proved in the project | R1–R4 | Confirmed present on `main`: `L_meta_5809.lean` and `L_meta_5811.lean` (S3, S4). The repository says a merged lemma is one the checker accepted (S7); I did not rebuild them. |
| Sibling sizes: 1799 lines and 84,084 bytes; 2528 lines and 121,756 bytes; 205,840 bytes together | R1, R2 | Confirmed (S3, S4). The sum is 84,084 + 121,756 = 205,840. |
| Both together fit under the 524,288-byte file limit | R2 | Confirmed: the limit is "at most 512 KiB" (S7), and 512 × 1024 = 524,288. |
| Both siblings import only `PEqualNP.Defs` | R2 | Confirmed: first line of each file (S3, S4). |
| Toolchain is Lean 4.36.0 | R1–R3 | Confirmed: `lean/lean-toolchain` reads `leanprover/lean4:v4.36.0` (S1). |
| 5809 rests on `no_and_cone`; 5811 opens `main_bound` with `unique_and_cone`, naming one pair `lo`, `hi` | R2, R4 | Confirmed: both names occur where described (S3, S4). |
| Lemma names cited from 5811 (`eval_Pure`, `eval_Mixed`, `quad_rect`, `rect_cover`, `common_le`, `cover_cost`, `count_gates`, `top_count`, `main_one_reach`, `plan_one_intersection`, `exception_plan`, `ordinary_root`, `leaf_count_bound`) | R1, R2 | Confirmed: every name occurs in `L_meta_5811.lean` (S4). I did not check that each lemma says what the results describe. |
| The third hypothesis is unused in both siblings | R1, R3 | Confirmed: both final theorems bind it to `_` and never use it (S3, S4). |
| 51 required incidences; degree 4; 51 + 13 − 1 = 63 | R1, R3 | Confirmed by computation: 52 incidences, 4 points per line and 4 lines per point, so 51 after removing one pair; at least ⌈51/4⌉ = 13 centres. |
| The incidence graph has no 4-cycle | R1, R3 | Confirmed by computation: any two points share exactly one line, any two lines exactly one point. |
| 2457 rejected input patterns | R4 | Confirmed by computation for a fixed spare bit: 234 four-point inputs plus 2223 two-by-two inputs. |
| Every single vertex, and every pair other than an incident point–line pair, lies inside a rejected input | R3, R4 | Confirmed by computation. The 234 four-point inputs alone already cover every such vertex and pair, as R3 states, and no incident pair lies in any rejected input. |
| `L_meta_8141` concerns a circuit of size ≤ 63 having an AND gate true on a rejected two-vertex input | R3 | Confirmed from its statement (S9); it is stated for 26 inputs and the full incidence function. |
| `R_meta_5164_2` is proved only from contradictory hypotheses | R2 | Confirmed: it takes a hypothesis `h` and its negation `hn`, and its proof is `exact absurd h hn` (S10). |
| A 3-gate circuit has `andPairs 27 = 2` | R1 | Not re-checked (no Lean toolchain used for this write-up). |
| The flat 63-gate circuit meets all hypotheses with `andPairs = 0`; one extra dead AND gate gives 64 gates with `andPairs = 2` | R4 (Python model); R2 gives a similar 64-gate example | Not re-checked. R4 states that none of it was checked in Lean. |
| Small-case SAT results (hexagon: 8 gates exist, 7 impossible; with nested pairs 8 impossible, 9 exists. Path with 5 edges: 7 exist, 6 impossible; with two or more nested pairs 7 impossible, 8 exists) | R4 | Not re-checked. |
| Searches on this instance at 60, 62 and 63 gates ran 330 s each with no answer | R4 | Not re-checked. R4 itself calls them inconclusive. |
| A surgery lemma exists for 26 inputs, when the inner AND is false on every four-point input, in `L_meta_2061` and `L_meta_5160` | R2 | Files present on `main` (74,568 and 74,301 bytes, S1); contents not read. |
| The step record has no sketch, no refutation and an empty dead list | R4 | Could not check: `step.json` is not among the inputs. |

## Why the step is open

The four results agree on the diagnosis. All of it below is their reasoning on paper, not Lean-checked.

**What the siblings do.** Both are direct gate counts. When no AND gate lies in the cone of another, each operand of an AND gate is an OR-tree of inputs. The four-point rejections force the two operand sets to span a complete bipartite piece of the incidence graph, which, with no 4-cycle, is a star. Counting star OR gates, AND gates and top OR gates gives 63 (R1, R3). The `andPairs = 1` proof handles its single nested pair by hand, in a case analysis that R3 puts at about 1300 lines.

**Why that stops at two or more nested pairs.** Nesting depth is unbounded. An AND gate inside another need not be false on rejected inputs: it can be true there and be filtered by the AND above it. An operand's set of accepted single inputs can arise as an intersection made by a lower AND gate. So the star lemma fails for such gates, and the OR-gate count behind the bound has no counterpart (R1, R2, R3). R4 adds that the sibling proofs depend structurally on there being exactly zero or exactly one nested pair.

**The obstruction, concretely (R2).** Take `i = (p1 ∨ p2 ∨ p3 ∨ p4) ∧ (l ∨ l')` with the `p_k` on `l`, and `j = i ∧ l`. Gate `i` is true on a rejected input. Replacing `i` by false loses the four pairs of `l`. Replacing it by its second operand makes `j` true on the single line `l`, which lies inside a rejected input. Only the first operand works here, and nothing guarantees one of the three replacements always works.

**The missing lemma.** Nobody proved it. The results state it in forms that amount to the same thing:

- *Descent* (R1 form A, R3 form B, R2's surgery lemma, R4's induction): from a circuit meeting the hypotheses with `andPairs ≥ 2`, build one that still meets them, is no larger, and has fewer nested pairs. R2's version allows smaller size, or equal size and fewer pairs. With the two siblings inlined as base cases this would close the step by strong induction.
- *Normal form* (R3 form A): reach `andPairs ≤ 1` directly, keeping the first two evaluation hypotheses.
- *Semantic charging* (R1 form B): replace the syntactic atom sets by single-input sets, charge each accepted edge to the lowest AND gate where it is a genuine minterm, and show each star's leaves still cost one OR gate apiece. R1 calls that last count the hard part.

Partial steps on paper (R3): a nested AND gate that is false on all 51 required inputs can be rewritten as an empty OR gate, keeping size and lowering `andPairs`; likewise an AND gate with one operand. What remains is a nested AND of two OR-sets, with no AND below it, that is true on some required incidence. R3 found no size-preserving rewrite for that case.

**Evidence that the statement is true, short of proof.** No result found a circuit of at most 62 gates meeting the hypotheses. The simplest nested shape costs one gate more than the one-level circuit for the same edges (R1). In R4's two exhaustive small cases the bound holds, and two or more nested pairs cost an extra gate. None of this proves anything about the 27-input instance.

## Where the results differ

- **Status.** Results 1–3 return `missing_lemma`; result 4 returns `out_of_time`. Result 4 nonetheless names the same missing lemma.
- **Is 63 attained in this case?** R4 raises an open question the others do not: the least size with `andPairs ≥ 2` is 63 or 64, and it found no 63-gate member. If none exists, the true bound for this case is 64. The step as posted asks only for 63, so this does not affect whether it holds.
- **Reusing the siblings.** R3 says a reduction would have to restate the siblings' core because neither may be imported and neither fits a 64,000-byte result. R2 says both can be inlined in the proof file, under the 524,288-byte limit. These concern different limits (the item result versus the repository file) and do not conflict. R1 agrees with R2 that copying is needed.
- **A search that is now out of date.** R2 reports that searching `Outside` for `2 ≤ andPairs 27` finds only `R_meta_2341_417`. At commit `7af82fd` the merged reduction `R_meta_5813_73.lean` also contains it (S2). R2's search presumably predates that merge.
- **An unnamed commit.** R2 says the cited files are byte-identical "at the cited commit" to the prebuilt copies, but names no commit. My size and line counts at commit `7af82fd` match R1's and R2's figures.

## Public state of the step when this was written

Read on 2026-11-26 between 01:45 and 01:48 UTC. This can change at any moment.

- **Repository.** `main` was at commit `7af82fd1b4e6fe6f792586b2c5aaddd8d264b377`. The tree has no `lean/PEqualNP/Outside/L_meta_5813.lean` (S1).
- **Desk.** The desk's record for the step returned `"state": "leased"`, `"holders": 1`, `"since": "2026-11-26T01:46:31.749Z"` (S11). So the step was still open and one holder had it. I do not know who.
- **Pull requests.** Searches for the step's name and number found six pull requests about it, all reductions (files named `R_meta_5813_*.lean`), none adding a proof file (S6). One was merged, one was open, and four were closed unmerged.
- **A merged reduction.** Pull request 22160 was merged on 2026-11-25 at 23:55:48 UTC and added `R_meta_5813_73.lean` (S2, S6). None of the four results mentions it. It derives the step from three smaller statements:

  | Hypothesis | Extra condition on top of the step's hypotheses |
  |---|---|
  | `hFull` | `2 ≤ andPairs` and the circuit also accepts the pair `(x2, x3)` |
  | `hPunctTwo` | `andPairs = 2` and the circuit rejects the pair `(x2, x3)` |
  | `hPunctMany` | `3 ≤ andPairs` and the circuit rejects the pair `(x2, x3)` |

  Its proof is a six-line case split. By the desk's rules, each hypothesis of an accepted reduction becomes a step, and the parent closes when all are proved (S8). I could not confirm from public sources that the desk recorded this reduction or posted the three children: the one bot comment I retrieved on that pull request reads `REJECTED (reduce-child)` for an earlier commit, yet the pull request shows as merged (S6). All three children still contain nested AND gates, so the missing lemma above is still needed for each.

## What is needed to meet the goal

1. **A proof.** Either the descent lemma (or one of its equivalents) for the 27-input instance, followed by the induction onto the two siblings; or, if the desk has posted the three children of `R_meta_5813_73`, proofs of those. Result 1 suggests the desk split the step further, with the descent lemma as its own step; results 2, 3 and 4 name the same lemma as what is missing.
2. **A file that passes the repository's rules** (S7): exactly one file, `lean/PEqualNP/Outside/L_meta_5813.lean`, one theorem with the posted statement unchanged, helpers in the module's namespace, no `sorry`, only the three standard axioms, at most 512 KiB.
3. **A check on another holder's machine**, then the pull request from the proving contributor's account. Neither can happen before item 1.

A solver-based attempt to refute the statement, or to settle R4's 63-versus-64 question, needs far more compute than the minutes R4 had; its runs at 60 to 63 gates returned nothing.

## What could not be found

- A proof of the step, in any of the four results or on `main`.
- The desk's posted text of the statement and its `step.json`. The statement above is taken from the merged reduction and matched against the siblings.
- Whether the desk recorded reduction `R_meta_5813_73` and which step ids its children have.
- Who held the lease at the time of reading.
- Independent confirmation of result 4's Python model and SAT runs, and of result 1's `decide` check.

## Sources

Repository files are pinned to commit `7af82fd1b4e6fe6f792586b2c5aaddd8d264b377`.

- **S1** Repository tree and toolchain: https://github.com/open-goat/pequalnp-proofs/tree/7af82fd1b4e6fe6f792586b2c5aaddd8d264b377/lean/PEqualNP/Outside and https://github.com/open-goat/pequalnp-proofs/blob/7af82fd1b4e6fe6f792586b2c5aaddd8d264b377/lean/lean-toolchain
- **S2** Merged reduction (4,653 bytes, SHA-256 `485f52bff5cfa788f1749ed0caaa8be4b3b0cb28b6fa02cf17eedb762d483500`): https://github.com/open-goat/pequalnp-proofs/blob/7af82fd1b4e6fe6f792586b2c5aaddd8d264b377/lean/PEqualNP/Outside/R_meta_5813_73.lean
- **S3** Sibling `andPairs = 0` (SHA-256 `09bd8f0e5213720b7b7c6c4fa94150a055d35fd656d7bdb1182b2b0a8ce2a2f3`): https://github.com/open-goat/pequalnp-proofs/blob/7af82fd1b4e6fe6f792586b2c5aaddd8d264b377/lean/PEqualNP/Outside/L_meta_5809.lean
- **S4** Sibling `andPairs = 1` (SHA-256 `c3519a1fc1c97c9b3978763e8bbee38b5c59eead7d73026426f7324dbebf2764`): https://github.com/open-goat/pequalnp-proofs/blob/7af82fd1b4e6fe6f792586b2c5aaddd8d264b377/lean/PEqualNP/Outside/L_meta_5811.lean
- **S5** Three-way split: https://github.com/open-goat/pequalnp-proofs/blob/7af82fd1b4e6fe6f792586b2c5aaddd8d264b377/lean/PEqualNP/Outside/R_meta_2341_417.lean
- **S6** Pull requests naming the step: https://github.com/open-goat/pequalnp-proofs/pull/22160 (merged), https://github.com/open-goat/pequalnp-proofs/pull/22529 (open), https://github.com/open-goat/pequalnp-proofs/pull/22319, https://github.com/open-goat/pequalnp-proofs/pull/13084, https://github.com/open-goat/pequalnp-proofs/pull/18429 and https://github.com/open-goat/pequalnp-proofs/pull/22414 (closed unmerged). Found with the GitHub issue search for `L-meta-5813` and `5813` in this repository. Pull request 22414 is titled `R-meta-5813-1` and appeared only in the second search.
- **S7** Repository rules: https://github.com/open-goat/pequalnp-proofs/blob/7af82fd1b4e6fe6f792586b2c5aaddd8d264b377/CONTRIBUTING.md and https://github.com/open-goat/pequalnp-proofs/blob/7af82fd1b4e6fe6f792586b2c5aaddd8d264b377/README.md
- **S8** Desk rules on reductions: https://pequalnp.com/join.txt (section "REDUCTIONS")
- **S9** https://github.com/open-goat/pequalnp-proofs/blob/7af82fd1b4e6fe6f792586b2c5aaddd8d264b377/lean/PEqualNP/Outside/L_meta_8141.lean
- **S10** https://github.com/open-goat/pequalnp-proofs/blob/7af82fd1b4e6fe6f792586b2c5aaddd8d264b377/lean/PEqualNP/Outside/R_meta_5164_2.lean
- **S11** Desk record: https://pequalnp.com/desk/step?gap=L-meta-5813
- **R1–R4** The four results, reproduced in full below.

## Source records

The `notes` field of each result, unchanged, with the SHA-256 of the input file it came from.

### R1: item-angle-1

Status: `missing_lemma`. Input SHA-256: `cd424fa40aef43c54eb99cebdbfa52db903335f76ef5ba07f6050476a1500a8c`.

~~~~text
NOT PROVED. No proof file was produced. I do not claim the statement is false.

Checked by machine (prebuilt Lean 4.36.0 + project, about 5 s per run): (1) the posted statement elaborates unchanged as theorem PEqualNP.Outside.L_meta_5813 after `import Mathlib` / `import PEqualNP.Defs`, with the proof left open, so this only confirms it parses and type-checks; (2) the andPairs hypothesis is satisfiable: the 3-gate circuit and[0,1], and[27,2], and[27,3] has PEqualNP.TopForm.andPairs 27 = 2, by `decide`.

Where the step sits. The prebuilt project already holds the two sibling steps with the same hypotheses and conclusion: PEqualNP/Outside/L_meta_5809.lean (andPairs = 0, 1799 lines) and L_meta_5811.lean (andPairs = 1, 2528 lines). This step, 2 <= andPairs, is the whole remaining general case: arbitrary nesting of AND gates. The bound 63 is tight (51 edges + 13 stars - 1 for the one-level circuit), so a cruder argument has no slack.

Why the direct angle does not close it. Mathlib has nothing on these circuits; the content is a tight monotone-circuit lower bound for the incidence graph of the 13-point plane. The siblings' method does not carry over as it stands:
- Both describe a wire w by `atoms C bit w`, the inputs reached from w through OR gates only (orIn / OrReaches). For an AND gate OR-reachable from the output whose operands reach no AND gate, each operand evaluates exactly as `hit (atoms ..)` (5811: eval_Pure); the quadrangle rejections force atoms a x atoms b to be a rectangle of incidences (quad_rect), which with no 4-cycle is a star (rect_cover, common_le). The count is cover_cost (covered edges <= roots + OR gates building the leaves), count_gates (ANDs + top ORs + root ORs <= size) and top_count (top ANDs <= top ORs + 1).
- 5811 handles its single nested pair (lo, hi) by hand: eval_Mixed, main_one_reach, plan_one_intersection, exception_plan (at most 2 roots). Each takes uniqueness of the nested pair as a hypothesis (hu, from unique_and_cone), and eval_Pure uses it to exclude any AND below an operand.
- With 2 or more nested pairs the nesting depth is unbounded, so an operand of a live AND gate is an arbitrary monotone function of lower AND gates. The single-input set of an AND gate is the intersection of those of its operands, so the leaves of a star need not be the OR-atoms of one wire, and the OR-gate count behind cover_cost (leaf_count_bound, which walks OR gates only) has no counterpart. A case analysis of the 5811 kind does not terminate.

The missing lemma, in either of two forms (my reading, not established):
(A) Normalisation: for C satisfying Monotone2, ReadsBack 27 and the three evaluation hypotheses with andPairs 27 C >= 2, there is C' satisfying the same hypotheses with C'.size <= C.size and andPairs 27 C' < andPairs 27 C. With 5809 and 5811 as base cases this gives the step by strong induction (both files would have to be copied into the helper namespace, since only PEqualNP.Defs may be used from the project).
(B) Semantic charging: replace atoms by S(w) = the inputs i such that w is true when only i (and the fixed bit) is set; S(and) = S(a) inter S(b), S(or) = S(a) union S(b); charge each accepted edge {p,l} to the lowest AND gate where it is a genuine minterm (p in S(a) \ S(b), l in S(b) \ S(a)); then show the leaves of each star still cost one OR gate apiece although they may arise through intersections. That last count is the hard part and is not in the siblings.

A hand check that supports truth but proves nothing: the simplest nested shape (OR of A /\ OR of B) /\ (c \/ d) accepts only a double star on an edge (c,d) and costs |A|+|B|+1 gates for |A|+|B|-1 edges, one more than the one-level circuit for those edges.

The third hypothesis (two points and two lines with no incidence are rejected) is unused in both siblings; this step may need it.

Suggestion to the desk: split further, e.g. (A) as its own step. No external sources were used; all references are to files of the prebuilt project.
~~~~

### R2: item-angle-2

Status: `missing_lemma`. Input SHA-256: `32df864664f258186b702aabbefaef989ea687f178298d8faaac6fd8ae667f8d`.

~~~~text
Not proved; no sorry-free file exists, so none is given. WHAT THE STEP IS. The third branch of a three-way split on andPairs for the 27-input punctured PG(2,3) incidence problem: R_meta_2341_417 takes hypotheses flat (andPairs = 0), single (= 1) and several (2 <= andPairs), and several is this statement. The other two are proved in the project: L_meta_5809 (84,084 bytes) and L_meta_5811 (121,756 bytes). Since those cover 0 and 1, this step is equivalent to the unconditional bound 63 <= size for every Monotone2/ReadsBack circuit meeting the accept/reject hypotheses: it carries all circuits with arbitrarily deep AND nesting. WHY THE SIBLING PROOFS DO NOT EXTEND. Both are direct gate counts, not reductions. 5809 turns andPairs = 0 into 'no AND in the cone of an AND' (no_and_cone). 5811 extracts the unique pair (lo, hi) with unique_and_cone, shows every other AND that OR-reaches the output is false on quadrangle inputs and hence one star root (ordinary_root), covers the pairs accepted at hi by at most 2 roots (exception_plan, a long case split on the atom sets of the operands), and closes with count_gates / cover_cost / top_count: ANDs + ORs OR-reachable from the output + ORs inside star sums <= size. With 2 or more pairs the nesting depth is unbounded, unique_and_cone has no analogue, and the accounting breaks: OR gates combining stars strictly inside the cone of an AND are neither top ORs nor star-sum ORs. Example of the obstacle (not a counterexample): the flat 63-gate circuit with output wire x plus one gate AND(x, x) meets every hypothesis, has andPairs >= 2 and a single top AND whose accepted pairs need 13 roots. A general proof needs a new invariant for wires that are true on rejected inputs and only become valid after a later AND. REDUCTION ROUTE AND THE MISSING LEMMA. One could inline 5809 and 5811 (205,840 bytes together, under the 524,288 limit, both using only PEqualNP.Defs) and argue by strong induction on (size, andPairs), given a surgery lemma: from a circuit meeting the hypotheses with a nested AND pair, build one still meeting them with smaller size, or equal size and fewer andPairs. The project has this only for 26 inputs and only when the inner AND is false on every quadrangle input (L_meta_2061, L_meta_5160), not for 27 inputs with the punctured pair, the spare bit and the 2x2 reject family. For an inner AND that is true on some rejected input I found no lemma: the 26-input analogue appears only as a reduction between hypotheses (R_meta_5164_1), and R_meta_5164_2 is proved only from contradictory hypotheses. Searching Outside for 2 <= andPairs 27 finds only R_meta_2341_417, as a hypothesis. No uniform local replacement works: take i = (p1 or p2 or p3 or p4) AND (l or l') with the p_k on l, and j = i AND l. Then i is true on the rejected input {p_k, l'}; replacing i by false loses the four pairs of l; replacing i by its second operand makes j = l, true on the single line l, which lies inside a rejected input; only the first operand works here, and nothing guarantees one of the three always does. So the missing lemma is: in a size-minimal, then andPairs-minimal circuit meeting the hypotheses, no AND that is true on a rejected input lies in the cone of another AND (or a direct count for that case). I could not prove it in the time available. TRUTH. I found no counterexample. One would be a circuit of at most 62 gates meeting the hypotheses; the inputs the hypotheses leave free (three collinear points, three concurrent lines, five or more points, four or more lines, the punctured pair) gave no saving in any construction I tried. I have no evidence the statement is false and no proof that it is true. CHECKED HERE. The posted statement elaborates as a theorem header under the prebuilt Lean 4.36.0 toolchain with PEqualNP.Defs (placeholder body, only to check that it parses). The cited project files are byte-identical at the cited commit to the prebuilt copies on this machine.
~~~~

### R3: item-angle-3

Status: `missing_lemma`. Input SHA-256: `a6f7731e26a950da1cce221c88e28013345a9778cfbde3b4d08088bd985b232e`.

~~~~text
NOT PROVED; no file is offered. Checked here: Lean 4.36.0 with the prebuilt project elaborates the posted statement as written (with a placeholder proof), so it is well formed. Everything below marked 'on paper' was not Lean-checked.

Where the step sits. It is the general case of a split on TopForm.andPairs 27 C. The two sibling cases are in the project with the same hypotheses and the same conclusion 63 <= size: L_meta_5809 (andPairs = 0, 84 KB) and L_meta_5811 (andPairs = 1, 122 KB). Neither may be imported here (only PEqualNP.Defs) and neither fits a 64000-byte result, so even a reduction to them would have to restate their core.

Why their method stops. With no AND gate inside the cone of another AND gate, each operand of an AND gate is an OR-tree of inputs, and every AND gate the output reaches through OR gates is below the output, hence false on every quadrangle input. Any two vertices that are not an incident point-line pair lie together in some quadrangle input, so the two operand sets span a complete bipartite subgraph of the incidence graph of PG(2,3); that graph has no 4-cycle, so the gate is a star. Counting the OR gates of the stars, the AND gates and the top OR gates gives 51 + 13 - 1 = 63 (51 required incidences, degree at most 4, so at least 13 centres). 5811 handles its single nested pair by a case analysis of about 1300 lines. With andPairs >= 2 an AND gate strictly inside another AND gate need not be below the output: it may be true on quadrangle inputs and be filtered by the AND above it, and an operand may obtain its set of accepted single inputs as an intersection made by an AND gate. The star lemma fails for such gates and I found no charging of gates to incidences that survives it. Both sibling proofs discard the third hypothesis (rejection of two points and two lines with no incidence), so it is presumably meant for exactly this case.

On paper:
1. Owner gate. For each required incidence e = (p,l), the first gate that is true on input e and false on both one-vertex inputs {p} and {l} is an AND gate with two operands a, b, where a is true on {p} and not on {l}, and b is true on {l} and not on {p} (or swapped). With nesting that gate need not be below the output.
2. Dead nested AND. If an AND gate i in the cone of another AND gate is false on all 51 required inputs, rewriting it as an OR gate with no input keeps the size, every required acceptance (same wire values on those inputs) and every rejection (the function only decreases), and lowers andPairs. Likewise an AND gate with exactly one operand, or with the 27th input as an operand when x4 = true, can be rewritten as a one-input OR gate.
3. What remains: a nested AND gate i = OR(S0) AND OR(S1) with no AND gate below it that is true on some required incidence. If it is false on all quadrangle inputs it is a star sitting under a filter; otherwise S0 x S1 contains a pair that is not an incidence. I found no size-preserving rewrite for either.

The missing lemma (either form closes the step with the sibling arguments):
(A) Normal form. For Monotone2 C with ReadsBack 27 C and the three evaluation hypotheses there is C' with Monotone2 C', ReadsBack 27 C', C'.size <= C.size, andPairs 27 C' <= 1, and the first two evaluation hypotheses (same x4, some x2 x3).
(B) Descent. In configuration 3 there is C' with the same three hypotheses, C'.size <= C.size and andPairs 27 C' < andPairs 27 C.
This is the single-level question for this 4-cycle-free graph under the promise. I know no proof of it. The later project step L_meta_8141 (a circuit of size <= 63 computing the full incidence function has an AND gate true on a rejected two-vertex input) is about the same obstruction.

Not claimed false. The bound is met by 13 stars when (x2,x3) is an incidence, and I found no circuit in which nested AND gates save a gate; no machine search was run (62 gates on 27 inputs is beyond enumeration).
~~~~

### R4: item-angle-4

Status: `out_of_time`. Input SHA-256: `9e9ef1a38580fa839aebc7dfd68e8cdab68d2c3f0b53cb90cf3880379a6810e3`.

~~~~text
Not proved and not refuted; no Lean file was written, so nothing was elaborated.

WHAT THE STEP IS. The last of three cases of one bound. The project already holds L_meta_5809 (andPairs = 0) and L_meta_5811 (andPairs = 1) with the same hypotheses and conclusion; this step is 2 <= andPairs, i.e. AND gates nested arbitrarily. step.json gives no sketch, no refutation and an empty dead list.

CHECKS THAT IT CAN HOLD (my own Python model of Circuit.wires/eval, cones, andPairs and ReadsBack; none of this was checked in Lean):
1. Not vacuous, and nearly tight. With (x2,x3) = (0,0): the single-level circuit for the other 51 incidences (per line an OR of its points ANDed with the line, then an OR chain) has 63 gates, andPairs = 0, and meets all three hypotheses for x4 false and true (51 accepted inputs, 2457 rejected input patterns enumerated). One extra dead AND gate reading two of the line ANDs gives 64 gates, andPairs = 2, hypotheses still met. So the least size in this step's class is 63 or 64. I found no 63-gate member.
2. No loophole in the encoding. Every single vertex and every pair of vertices other than an incident point-line pair lies inside a rejected input (checked by enumeration), so a counterexample must produce the incidence graph exactly on inputs of weight <= 2 with at most 62 gates. Inputs it may freely accept (three collinear points, three concurrent lines, five or more points, four or more lines) gave no saving in the constructions I tried by hand: OR sets shared between lines and filtered by a later AND, products of mixed point/line sets, grid intersections, absorbing one line term into the next. Each costs at least as much as the single-level circuit. This is not a proof.
3. Small cases, exhaustive SAT search (fan-in two; accept every edge, reject every non-edge pair). Hexagon C6: 8 gates = edges + cover - 1 exist, 7 impossible; with one or more nested AND pairs 8 is impossible and 9 exists. Path with 5 edges: 7 exist, 6 impossible; with two or more nested pairs 7 is impossible and 8 exists (one nested pair is possible at 7). So the bound holds there, and two nested pairs cost a gate more, which matches 64 here.
4. Inconclusive runs. The same search on the Fano analogue (7, {0,1,3}) at 22 to 27 gates, on C8 and C10, and on this instance at 60, 62 and 63 gates ran 330 s each with no answer, including sizes where a circuit is known to exist. They say nothing either way.

WHY NO PROOF. L_meta_5811 rests on there being exactly one nested pair: main_bound opens with unique_and_cone, which names the single pair lo, hi, and several hundred lines of case analysis on that one gate follow. L_meta_5809 rests on there being none (no_and_cone). Neither extends to several or deeper nestings. I found no size-preserving way to remove a nested pair: turning the inner AND into false can lose incidences that reach the output only through the outer AND, and turning it into an OR can make a rejected input accepted. A proof needs a new lemma for arbitrary nesting, for instance an induction on andPairs that rewires the lowest nested AND without adding gates (then the 5809 argument closes it), or a count showing each nested pair costs a gate. I did not get either in the time.

OPEN. Whether 63 is attained with andPairs >= 2 (if not, the true bound for this case is 64). A solver-based refutation attempt needs far more than the minutes available here.
~~~~

