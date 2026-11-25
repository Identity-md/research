# Step L-meta-5012 (desk pequalnp): write-up of four attempts

**Bottom line: none of the four attempts proved step L-meta-5012.** None produced a Lean 4 proof of it. So no second holder had a proof to check, and no pull request was opened on open-goat/pequalnp-proofs. What is delivered below is a record of what was found: where each attempt got stuck, the evidence checked by machine, and the lemmas that are still missing. A write-up cannot supply a proof that none of its source results contain, and this one does not claim one.

## Sources (inputs to this write-up)

| id | path | SHA-256 | status |
|---|---|---|---|
| angle-1 | `.imd/reads/artifacts/item-angle-1` (= `artifacts/goal/items/angle-1/result.json`) | `104dfde63bfd8b82bf3c370ab8c0d1fd60c987857bea67ca0a31f719e6428a40` | `out_of_time` |
| angle-2 | `.imd/reads/artifacts/item-angle-2` (= `artifacts/goal/items/angle-2/result.json`) | `d63a42ba03876b8a2d66ff45a6097766d7153841517c69b075707667c693ff06` | `missing_lemma` |
| angle-3 | `.imd/reads/artifacts/item-angle-3` (= `artifacts/goal/items/angle-3/result.json`) | `ea531e96cbbe904f37151d34e643b710dde926cc8ca525e668b6cb6564b1faf8` | `missing_lemma` |
| angle-4 | `.imd/reads/artifacts/item-angle-4` (= `artifacts/goal/items/angle-4/result.json`) | `b470f43fdd7cc300fbc111c70852bd1255607282af6b6e00660d5bbf284b026b` | `missing_lemma` |

These input files come from the job and are not part of this repository's Git history. Each one is a JSON object with a `status` field and a `notes` field. Every statement below names the attempt it comes from.

## 1. What the step says

- The hypothesis is "rung 1": if G is bipartite with no 4-cycle (NoFourCycle) and C satisfies IsLeastAO, then `(junk G C).card ≠ 1`. The conclusion is the same statement with 2 in place of 1: `(junk G C).card ≠ 2` (angle-1 §1, angle-2 §2, angle-3, angle-4 §1).
- `junk G C` is the set of AND gates (indices `j < C.gates.length`) that are true at some input where `graphFun G ∅` is false. `IsLeastAO` means three things: C satisfies IsAO2 (AND/OR gates only, each reading exactly two earlier wires), C computes `graphFun G ∅`, and C has least size in that model (angle-1 §2, angle-2 §1).
- The hypothesis is already a theorem in the project: `PEqualNP.Outside.L_meta_3760` (513,510 bytes), restated as `L_meta_8725` (all four attempts). angle-2 and angle-4 each elaborated L_meta_3760 with the prebuilt toolchain, with exit 0 and no sorry. angle-4 also checked in Lean that `(hypothesis → conclusion) ↔ conclusion`. **Consequence:** the hypothesis cannot be refuted to make the step true vacuously. The step is exactly as hard as proving the two-junk rung with no assumption.

## 2. Evidence checked by machine (none of it proves the step)

- **angle-3, a Lean frame.** angle-3 built a frame of 102,957 bytes (the limit is 524,288) under Lean 4.36.0: exit 0, no sorry, and only the axioms propext, Classical.choice and Quot.sound. The frame derives the step's conclusion from rung 1 plus **two missing lemmas, A and B**. It inlines three pieces:
  - L_meta_3760 lines 6–1039 (thm_1501: TopForm normalisation);
  - L_meta_7895 lines 4–1082 (the dichotomy lemma);
  - `empty_graph_size_zero` (L_meta_3760 lines 6183–6209).
  
  The frame was not delivered, because a result carries Lean only when it is a full proof.
- **angle-3, text search.** A text search of the 5,592 Outside files at commit e125f04 found no proof of the two-junk claim.
- **Exhaustive searches by small-case enumeration.** These are C programs, not Lean, so they are evidence and not proof:
  - **angle-1** covered bipartite 4-cycle-free graphs **without isolated vertices**: on at most 5 vertices (9 graphs), and 8 of the 11 such graphs on 6 vertices. It found least sizes from 1 to 6 and 288 function sets, all with 0 junk. Runs for P6 and one spider (least size 7) stopped at the time cap, with all sets found having 0 junk. The 6-cycle run did not finish size 7.
  - **angle-2** covered graphs **without isolated vertices** on 2 to 6 vertices: 20 graphs up to isomorphism, every least circuit with 0 junk. For P4 the least size is 4, with 5 circuits; for C6 the least size is 8, with 54 circuits. Partial runs up to size 8 on P7, a spider and a caterpillar found 0 junk.
  - **angle-4** covered every *labelled* bipartite 4-cycle-free graph **with at least one edge** (isolated vertices allowed) on n ≤ 7 vertices. For n = 2 to 7 that is 1, 6, 37, 290, 2991 and 39900 labelled graphs, with 38 isomorphism classes at n = 7. It went up to circuit size 9, which reaches the least size of every one of these graphs. In every least circuit the junk count is 0. Its limit: every such graph is a forest or has a single 6-cycle. The first graph with two cycles needs about 12 gates and was out of reach.
  - The populations differ: "with an edge" (angle-4) is not the same as "without isolated vertex" (angle-1, angle-2), so the counts are not comparable across attempts.
- No attempt found a counterexample, and no attempt claims the statement is false.

## 3. Missing lemmas, which is where every attempt stopped

The route the attempts agree on is: no edge ⇒ size 0 ⇒ no junk. Otherwise, apply L_meta_1501 to reach TopForm, then L_meta_7895 to split into two cases (angle-1 §3, angle-3, angle-4 §4):

- **Lemma A (counting branch).** The case `2 ≤ 2·|centreless G C| + |orN G C \ lam G C|`. Here one needs a D in the model that computes F and either is strictly smaller than C, or has size ≤ C.size and exactly one junk gate. angle-3 calls this "nearly the whole problem". The "mutual kill" top, `(OR(S1) ∨ g) ∧ (OR(S2) ∨ h)`, falls inside this case (angle-1, angle-2 L7, angle-3).
- **Lemma B (nested shape).** The case `junk = {a,b}`, `InCone a b`, `centreless = ∅`, `readers a = {b}`, `readers b = {m}`, `orN \ lam = {m}`, with both junk gates true on every U\* edge (angle-3).
- Partial results in the project hold only for special shapes under `Core.IsLiftFixedPoint`: L_meta_5138, L_meta_5391 and L_meta_5412 (angle-1, angle-2, angle-3).
- angle-4 §5 describes what is needed: a bound on U\* edges for two junk gates that is strong enough against the inequality of L_meta_1491. It says this is of the order of the rung-1 development, not a short lemma.
- One reported pitfall: an exchange that cleans both junk gates without saving a gate gives no contradiction, because rung 1 says nothing about card = 0 (angle-2 L3, angle-3).
- angle-3 suggests proving B first, then splitting A by mutual versus independent position.

## 4. Outcome against the goal

| Required by goal | Status |
|---|---|
| Lean 4 theorem proving L-meta-5012 | **Not produced** (all four attempts) |
| Check by another holder's machine | **Not done**: there was nothing to check |
| PR on open-goat/pequalnp-proofs | **Not opened** |

The step is still open. Doing the next attempt along the route in §3 should work.
