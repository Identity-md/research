# L-meta-9738: no proof was found. Report of the attempt

## Outcome

**The goal is not met.** Step L-meta-9738 was not proved, so there is no Lean 4 theorem to check and no pull request to open. This file is a report of four unsuccessful proof attempts and of what they established on the way. It is not the commissioned theorem contribution and must not be counted as one.

| What the goal asks for | State | Evidence |
|---|---|---|
| A Lean 4 proof of step L-meta-9738 | **Absent.** All four results have `status: missing_lemma`; none returns a Lean file. | A1 to A4 (inputs, listed under Sources) |
| A check of that proof by another holder's machine | **Did not happen.** There was no proof to check. | Follows from the row above |
| A pull request on open-goat/pequalnp-proofs from the proving contributor's account | **Does not exist.** No file whose path contains `9738` is in the repository tree, and a search of its issues and pull requests for `L-meta-9738` and `L_meta_9738` returns nothing. | W3, W4 (looked up 2026-11-25, about 23:07 UTC) |

What stands between the attempt and the goal is one lower-bound lemma that nobody in this job proved and that the public project does not hold without extra hypotheses (sections 5 and 6). The truth of the step is open: no proof and no counterexample were found.

A write-up step cannot supply the three missing things: the results it merges contain no proof, and writing one up as if it existed would be an invention. Section 10 says what would complete the goal.

## How to read the source marks

- **A1, A2, A3, A4**: the four results this report merges (`item-angle-1` to `item-angle-4`). A statement marked this way is the item's claim.
- **W1 to W6**: checks made in this write-up run, by a script or by reading the public repository at the commit the items name. They are listed under Sources, and the script is in the appendix so they can be repeated. They are this run's own checks and carry no independent authority.
- A statement with an A mark and no W mark was **not** re-checked here.

## 1. The step

The exact Lean text of the posted statement is not among this run's inputs; the description below is the items'.

The step is about a fixed list of 48 pairs on 25 vertices and the Boolean function "some listed pair has both ends true" (the edge function). It asserts that no `Monotone2` circuit (AND and OR gates of fan-in 2) of size at most 58 computes that function on 25 inputs. In the words of A1: "The step asserts 58 is impossible."

All four items identify the 48 pairs the same way (A1, A2, A3, A4):

- the pairs are `(a, 13 + j)` with `a < 13`, `j < 12` and `(j - a) mod 13` in `{3, 9, 11, 12}`;
- `{3, 9, 11, 12}` is a perfect difference set mod 13, so this is the point-line incidence graph of the projective plane of order 3, PG(2,3), with one line deleted: the line `j = 12`, through points 0, 1, 3, 9.

A3 and A4 write the same graph in the form "difference in `{0, 1, 3, 9}`" with a shifted line index. W1 confirms that the three written forms give the same 48 pairs.

Facts about the graph:

| Fact | Items | Re-checked here |
|---|---|---|
| 48 distinct pairs, 13 points and 12 line vertices, every vertex has an edge | A1, A2, A3, A4 | W1 |
| Points 0, 1, 3, 9 have degree 3; the other nine points have degree 4; all twelve lines have degree 4 | A1, A2, A3, A4 | W1 |
| No two vertices share two neighbours (no 4-cycle) | A1, A2, A3, A4 | W1 |
| Maximum matching 12 (A1, A3); minimum vertex cover 12 (A2, A3, A4) | as marked | W1 |
| The 12 line vertices are the only vertex cover of size 12 | A4 | W1 |

## 2. What each attempt returned

| Item | Status | Lean produced | Checked by the item | The item's missing lemma |
|---|---|---|---|---|
| A1 | `missing_lemma` | None returned. The posted statement elaborates with the proof left open (scratch only). | By script: the graph description, the relabeling into the 52-pair list, the 59-gate count. | `64 <= C.size` for every `Monotone2` circuit of the 26-vertex PG(2,3) edge function |
| A2 | `missing_lemma` | None written. | By script: the graph facts; the 59-gate circuit on all 2^25 inputs. | "claim (4)": every strict live DAG for this function has `totalSurplus >= 35`; "or equivalently the bound 64 for the full plane graph" |
| A3 | `missing_lemma` | A reduction "elaborated with the prebuilt toolchain, no error, no sorry, about 5 s; not delivered because the step itself is not proved". | By script: the graph facts; the 59-gate circuit on all 2^25 inputs. | `PG23LB` (section 5), the unrestricted 64-gate bound |
| A4 | `missing_lemma` | "No Lean file was written, so nothing was elaborated." | By script: the graph facts; the 59-gate circuit "in the project's wire semantics on all 2^25 inputs". | Either the direct bound `size >= 59` on 25 inputs, or `size >= 64` for the 52-edge plane function on `Fin 26` |

No item claims a proof and no item claims a refutation.

## 3. The upper bound: 59 gates suffice

For each of the 12 line vertices take 3 ORs over its 4 points and 1 AND with the line input; then 11 ORs join the 12 results. That is `12*4 + 11 = 59` gates (A1, A2, A3, A4), which equals edges + cover - 1 = `48 + 12 - 1` (A2, A4).

A2, A3 and A4 each report comparing this circuit with the edge function on all 2^25 inputs. W2 repeats it: the circuit has 59 gates (47 OR, 12 AND) and agrees with the edge function on all 2^25 inputs. W2 simulates a plain straight-line program (gate k reads two earlier wires, the last gate is the output); it did not load the project's `Circuit.eval`.

This is an upper bound only. It shows that the same statement with 59 in place of 58 would be false, so "58 is the last value that can hold" (A4). It says nothing about whether 58 gates are impossible, which is the whole content of the step.

## 4. Easy lower bounds fall far short

- Dependence on all 25 inputs gives 24 gates (A1).
- The vertex-cover bound `n + tau - 1` gives `25 + 12 - 1 = 36` here (A1, A3, A4). For the full 26-vertex plane the same kind of bound gives 38: `L_meta_1484` proves `38 <= C.size` for it (A4; W5 read the statement), and `MetaComplexity/L1478` reaches 38 from a hypothesis (A3; W5: its docstring ends "Conjecture, on paper").
- The cheap part of the Heawood scheme (eligible labels cover the edges and number at most the surplus) "gives only surplus >= 12, i.e. 36 gates" (A2).
- Fixing variables to false removes `fanout(v)` gates per deleted vertex, not the `deg(v)` or `deg(v) + 1` needed to reach 59 (A4); constant propagation guarantees 1 or 2 gates per vertex and "ends near n + cover - 1 = 36" (A3).

So the step needs 59 and the routine arguments stop at 36.

## 5. The reduction every attempt found, and its condition

Add the deleted line back as a 26th input: 3 ORs for `x0 OR x1 OR x3 OR x9`, 1 AND with the new input, 1 OR with the old output. That is 5 more gates. A circuit of size at most 58 for the step would therefore give a circuit of size at most 63 for the full PG(2,3) edge function on 26 inputs (A1, A2, A3, A4).

Hence the step **would follow from** the lemma A3 calls `PG23LB`:

> `PG23LB : forall C, Monotone2 C -> (forall y : Fin 26 -> Bool, C.eval (List.ofFn y) = true <-> exists u v : Fin 26, (u.val, v.val) in elFull and y u = true and y v = true) -> 64 <= C.size`

where `elFull` is the step's list followed by `(0,25), (1,25), (3,25), (9,25)` (A3).

State of this reduction:

- It is **conditional**. `PG23LB` is assumed, not proved. A conditional reduction is not a proof of the step.
- A3 reports it elaborated in Lean with no error and no `sorry`, adapted from `red13` of `L_meta_9730`: renumber every wire `i >= 25` to `i + 1`, then append `or[0,1], or[.,3], or[.,9], and[25,.], or[out,.]`. **The Lean source was not delivered** and is not among this run's inputs, so nobody outside A3's run has seen or checked it. A1, A2 and A4 worked the reduction by hand and script only.
- A1 and A4 give the relabeling that turns the step's graph plus its deleted line into the 52-pair list used by the project's rows `R_meta_972_733` and `R_meta_650_517`: point `a` stays, line vertex `13 + j` goes to `13 + ((12 - j) mod 13)`; the 4 pairs not hit are `(0,13), (1,13), (3,13), (9,13)`. W1 confirms the arithmetic, and W5 confirms that the list in both project rows is exactly the 52 pairs `(a, 13 + j)` with `(a + j) mod 13` in `{0, 1, 3, 9}`.
- W2 checked one instance of the construction: the 59-gate circuit, shifted and extended by those 5 gates, has 64 gates and computes the 52-edge function on all 2^26 inputs. That confirms the gate count and wiring of the re-addition on that circuit. It is not a check of A3's Lean lemma.

The pattern has a precedent in the project: `L_meta_9730` and `L_meta_9734` derive vertex-deleted Heawood graphs from the Heawood bound by re-adding stars (A1, A2, A3). W5 found `red13` in `L_meta_9730.lean` and `addStars_size : (addStars C).size = C.size + 8` in `L_meta_9734.lean`, matching A1's "two stars re-added for 8 gates".

## 6. The missing lemma, and where the public project stands on it

The missing lemma is the lower bound itself, in either form (A4):

1. direct: every `Monotone2` circuit computing this 25-input function has size at least 59; in A2's form, every strict live DAG computing it has `totalSurplus >= 35` (the star circuit has exactly `35 = 9*3 + 4*2`; W2 recomputed 35);
2. through the full plane: `PG23LB`, size at least 64 on 26 inputs.

A3 notes that the step is weaker than `PG23LB`, "so a direct proof might be easier, but I do not have one".

The items searched the project (A1 names it as "brilliant-hq/pequalnp-proofs at e125f04d") and found the bound 64 for PG(2,3) only under restrictions. W3 found that the GitHub API answers a request for `brilliant-hq/pequalnp-proofs` with a redirect to the repository `open-goat/pequalnp-proofs`, so the items read the repository the goal names. W5 read the statements below at commit `e125f04d0dc6fed67cee48a1d06692912e167c32`.

| Row | What it gives, per the items | Seen in the statement (W5) |
|---|---|---|
| `R_meta_972_733` | 64 from two assumed hypotheses, `normalize` and `lower` (A1) | Both hypotheses are arguments of the theorem; `lower` is `64 <= D.size` for `IsAO2 26` circuits |
| `L_meta_2143` | size at most 63 ruled out only under `HasLineDegree ... 1` (A1, A3) | `size <= 63` together with `HasLineDegree` at 1, under a negated existential |
| `L_meta_1500` | line degree 1, at most 63 gates refuted (A3) | Same shape: `C.size <= 63` and `HasLineDegree 26 (Finset.Ico 13 26) C 1` |
| `L_meta_8791` | 64 only under `IsLeastAO`, `TopForm` and `junk = empty` (A1) | The statement carries `TopForm.IsLeastAO`, `TopForm.TopForm` and `TopForm.junk ... = ∅` |
| `L_meta_2059` | "no AND gate in the cone of another AND" (A3) | The statement carries a `ReadsBack 26` hypothesis; the gloss is A3's |
| `L_meta_5158` | `andPairs = 0` (A3) | The statement carries `andPairs (26 : ℕ) x3 = (0 : ℕ)` |
| `L_meta_8141` | from a circuit of size at most 63, only a non-edge pair on which some AND gate fires, not a contradiction (A1) | Statement read in part only (it carries `ReadsBack` and is closed by `exists_bad_pair`); not checked in full |
| `R_meta_650_517` | the opposite side: a 61-gate circuit on 25 inputs with one exposed wire would give 63 gates for the plane (A1); conditional (A2, A4) | Both premises are hypotheses; the conclusion is a circuit with `C.size <= 63` for the 52-pair function |

No unrestricted row for the bound 64 was found by any item (A1, A2, A3, A4), and A1 found no row for this step's edge list. A1 adds: "The step's own context says the truth is not known to the desk."

## 7. Why the attempts did not close it

- **No finite check.** Unfolding the definitions leaves a statement over all lists of at most 58 AND/OR gates with arbitrary wire indices on 25 inputs; that is not a finite check of feasible size (A1). A kernel-replayed search over 58-gate circuits on 25 inputs is out of reach (A2); the certificate rows A3 saw (`L_meta_2427`, `L_meta_9781`) cover 13 to 16 gates.
- **The only known route is very large.** The one method in the project that reaches edges + cover - 1 on a plane is the Heawood proof `L_meta_971`: strict live binary DAGs, the surplus identity, carrier flow, cofactor restriction, then a case split over independent sets up to automorphism (A4). A2 gives its size as 472258 bytes and A4 gives `L_meta_9730` as 482,459 bytes; W4 confirms both file sizes. A2 describes about 6400 lines of mostly generic blocks followed by 14 closed cases (`elim_p7 .. elim_p13`); W5 found `normalize_strictLive`, `heawood_lb_27`, `elim_p7`, `elim_p13` and `totalSurplus` in the 9367-line file but did not count the cases.
- **Scaling that route is the open part.** For Heawood the claim was surplus at least 14 on 14 inputs; here it is surplus at least 35 on 25 inputs (A2, A4), with a new charging argument per case and Fano-specific cases replaced by order-3 geometry. A2: "I could not design that in this run and do not know whether the scheme extends." A4: it "probably does not fit one file without a new idea". A2 and A4 state a file limit of 524288 bytes; the repository's CONTRIBUTING.md says the file is "at most 512 KiB" (W6), which is the same number.
- **No shortcut to Heawood.** The order-3 plane has no Fano subplane, so restricting inputs does not lead to the Heawood rows (A2; not re-checked here).
- **Routine parts were not written.** A2 lists normalisation, the surplus identity, the graph facts by `decide` and the assembly as routine, and wrote no Lean for them "since without (4) there is no file to submit". With `n = 25`, the surplus identity `gates = n - 1 + totalSurplus` turns size at most 58 into `totalSurplus <= 34` (A2). A3 states the same count as input fanout plus gate surplus at least 60 over 25 inputs, against 28 over 14 for Heawood. W2 recomputed these on the star circuit: input fanouts sum to 60 and `24 + 35 = 59`.

## 8. Is the statement true?

Unknown. This is the items' own conclusion, and nothing here changes it.

- No circuit with at most 58 gates was found (A1, A3, A4). A2 did not search for one.
- A4 tried to refute the statement and failed: OR-sums cannot be shared between stars (two lines share one point, two points share at most one line), and four hand-built devices each cost at least as many gates as the star they replace. A4 calls this "Heuristic, not a proof." A3 tried shapes by hand and calls the result "not evidence either way".
- The formula edges + cover - 1 agrees with every merged bound of this family the items recomputed. A2 calls that "evidence, not proof".

| Row | Inputs | Edges | Cover | Formula | Merged lower bound | Items | Re-checked here (W5) |
|---|---|---|---|---|---|---|---|
| `L_meta_971` (Heawood) | 14 | 21 | 7 | 27 | 27 | A2, A3, A4 | 21 edges, cover 7, figure 27 in the statement |
| `L_meta_9730` | 13 | 18 | 6 | 23 | 23 | A2, A4 | 18 edges, cover 6, `C.size ≤ 22` refuted |
| `L_meta_9734` | 12 | 15 | 5 | 19 | 19 | A2 | 15 edges, cover 5, `C.size ≤ 18` refuted |
| `L_meta_9781` | 10 | 13 | 5 | 17 | 17 | A2 | 13 edges, cover 5, `C.size ≤ 16` refuted |
| this step | 25 | 48 | 12 | 59 | **not proved** | A1 to A4 | W1 |

A4 also cites `L_meta_3525` for all forests; W5 read its statement, `edgeSet.ncard + x2 ≤ size + 1` for acyclic graphs with every vertex cover of size at least `x2`.

If the statement were false, the reduction of section 5 would run the other way: "a 58-gate circuit for this step would give a 63-gate circuit for the plane, so the opposite row of this step would refute that bound of 64" (A1).

## 9. Where the results differ

The four results agree on the status, the graph, the 59-gate circuit, the reduction and the missing lemma. They differ in these points, none of which changes the outcome:

- **Lean use.** A3 says the conditional reduction was elaborated in Lean; A1 elaborated only the open statement; A2 and A4 elaborated nothing. A1 describes the reduction as "by hand and script; not elaborated in Lean", which is about A1's own run and does not contradict A3.
- **Search for a counterexample.** A3 and A4 tried by hand; A1 reports finding none without describing a search; A2 says plainly it did not search.
- **Which rows are cited.** A1 and A3 list different restricted rows for the bound 64 (they share `L_meta_2143`). The lists are compatible; section 6 gives their union.
- **The 38 bound.** A3 says `L1478` reaches 38 "from a hypothesis"; A4 says `L_meta_1484` instantiates the general bound to get 38. These are two different rows and both descriptions hold (W5).
- **How the Heawood bound is written.** A3 writes `27 = 21 + 6`; A2 and A4 write edges + cover - 1 with cover 7. Same number.
- **Form of the missing lemma.** A2 prefers the direct surplus form, A1 and A3 the full-plane form, A4 lists both. A2 calls the two "equivalent"; A3 says the step is weaker than `PG23LB`. Only the direction "`PG23LB` implies the step" is supported by the reduction; the converse is not shown by any item.
- **Where the deleted line is put back.** A3 adds it as vertex 25 with no relabeling; A1 and A4 relabel into the project's 52-pair list, where the re-added star sits at vertex 13. W1 confirms A1's and A4's relabelings give the same image.

## 10. What is missing, and what would complete the goal

Missing, in order:

1. **A proof of the lower bound.** Either the direct bound on 25 inputs or `PG23LB` on 26 inputs. This is new mathematics relative to the public project as the items read it, not a formalisation of something already on file.
2. **The Lean file** for the step. Per the repository's CONTRIBUTING.md (W6) a pull request proves one posted gap with one file `lean/PEqualNP/Outside/L_<gap>.lean`, with no `sorry`.
3. **The check on another holder's machine**, which needs item 2.
4. **The pull request** from the proving contributor's account, which needs items 2 and 3. Per CONTRIBUTING.md (W6), credit goes to the author of the pull request.

Suggestions from the items for whoever continues:

- Post `PG23LB` (26 vertices, at most 63 gates refuted) as its own row; with it, the 5-gate star re-addition closes L-meta-9738 "and, by the symmetry of the plane, every other one-line-deleted relabelling" (A3). A1 gives the same plan: adapt the `addStars` part of `L_meta_9734` to one star of 4 points (5 gates) with the relabeling of section 5.
- A port of `L_meta_971` needs order-3 geometry in place of its Fano cases; the map `u -> 3u mod 13` fixes the deleted line and so acts on this graph (A4).
- A3's elaborated reduction should be delivered as a file if that run can be repeated; at present it exists only as a description.

## 11. What this run could not find or did not check

- The exact posted Lean statement of L-meta-9738 and the desk's public list were not among the inputs and were not read.
- A3's Lean reduction: not delivered, not seen, not re-elaborated. No Lean toolchain was run in this write-up.
- Whether an unrestricted PG(2,3) bound landed in the repository after commit `e125f04d`: not checked. The repository moves quickly (its head at lookup time was `9e532759798dcaf311fd642150f58b2219256376`, committed 2026-11-25T23:04:07Z). The tree at that head has no path containing `9738` (W4), but other new rows were not read.
- The items' statements about the proofs inside the large rows (the 14 cases, carrier flow, the absence of a Fano subplane, A1's reading of the step's context) were not re-checked beyond what section 6 and section 7 mark with W.
- The repository search (W3) is a point-in-time lookup and covers issues and pull requests only.

## Sources

Inputs merged (read as data; SHA-256 computed in this run and equal to the values the task gives):

- **A1** `item-angle-1` (`artifacts/goal/items/angle-1/result.json`), SHA-256 `5ba379f755489980d0ded9a202647879f302fc29684502f2a1464b8fef561688`
- **A2** `item-angle-2` (`artifacts/goal/items/angle-2/result.json`), SHA-256 `731e2b4f4351427f7a40c45de11893c570ee50dd76d93961bdc66dc0a4e379d1`
- **A3** `item-angle-3` (`artifacts/goal/items/angle-3/result.json`), SHA-256 `8b1887b4707630b4d2f9e12fdbaa36f568961404dfa0b4701436086f8544da8e`
- **A4** `item-angle-4` (`artifacts/goal/items/angle-4/result.json`), SHA-256 `2e0f5b93895e8ec6b2d7cc12ea79c0bb4ff093c8eb911fe9dd076ad8520ff043`

Checks made in this run (2026-11-25, about 23:05 to 23:15 UTC):

- **W1** Script, appendix part 1: the pair list, the difference set, degrees, common neighbours, matching, covers, the relabeling.
- **W2** Script, appendix part 2: the 59-gate circuit against the edge function on all 2^25 inputs; fanout and surplus counts; the 64-gate extension against the 52-edge function on all 2^26 inputs.
- **W3** GitHub API. `https://api.github.com/repos/brilliant-hq/pequalnp-proofs` answers 301 and, followed, returns `open-goat/pequalnp-proofs`. `https://api.github.com/search/issues?q=repo:open-goat/pequalnp-proofs+%22L-meta-9738%22+in:title` and the same search for `%22L_meta_9738%22` return `total_count` 0. For comparison the same title search finds the merged siblings: <https://github.com/open-goat/pequalnp-proofs/pull/14574> (`L-meta-9730`, merged 2026-11-25T13:29:40Z) and <https://github.com/open-goat/pequalnp-proofs/pull/15192> (`L-meta-9734`, merged 2026-11-25T14:07:36Z).
- **W4** Repository tree at head `9e532759798dcaf311fd642150f58b2219256376` (`https://api.github.com/repos/open-goat/pequalnp-proofs/git/trees/main?recursive=1`, 9883 entries, not truncated): no path contains `9738`; sizes `L_meta_971.lean` 472258, `L_meta_9730.lean` 482459, `L_meta_9734.lean` 449005, `L_meta_9781.lean` 517117 bytes. Commit `e125f04d` resolves to `e125f04d0dc6fed67cee48a1d06692912e167c32` (2026-11-25T15:47:48Z).
- **W5** Files read at that commit, each at `https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/<path>`:
  `lean/PEqualNP/Outside/L_meta_971.lean`, `L_meta_9730.lean`, `L_meta_9734.lean`, `L_meta_9781.lean`, `R_meta_972_733.lean`, `R_meta_650_517.lean`, `L_meta_2143.lean`, `L_meta_1500.lean`, `L_meta_8791.lean`, `L_meta_2059.lean`, `L_meta_5158.lean`, `L_meta_8141.lean`, `L_meta_1484.lean`, `L_meta_3525.lean` (all under `lean/PEqualNP/Outside/`) and `lean/PEqualNP/MetaComplexity/L1478.lean`. Edge counts and cover numbers in section 8 were computed from the lists in the final theorem statements.
- **W6** <https://github.com/open-goat/pequalnp-proofs/blob/e125f04d0dc6fed67cee48a1d06692912e167c32/CONTRIBUTING.md>: "One pull request proves one posted gap."; "It is a plain text file in UTF-8, at most 512 KiB."; "No `sorry`."; "Credit goes to the author of the pull request."

## Appendix: the check script (W1, W2)

Python 3, standard library only, about 2 seconds. Expected output is given after it.

```python
import itertools
D = {3, 9, 11, 12}
E = [(a, 13 + j) for a in range(13) for j in range(12) if (j - a) % 13 in D]
nb = {v: set() for v in range(25)}
for u, v in E: nb[u].add(v); nb[v].add(u)
# part 1: the graph
print("pairs", len(set(E)), "difference set", sorted((x - y) % 13 for x in D for y in D if x != y) == list(range(1, 13)))
E4 = {(u, 12 + l) for u in range(13) for l in range(1, 13) if (u - l) % 13 in {0, 1, 3, 9}}
E3 = {(p, 12 + w) for p in range(13) for w in range(1, 13) if (p - w) % 13 in {0, 1, 3, 9}}
print("same list in A3 and A4 form", E3 == set(E), E4 == set(E))
print("degrees", [len(nb[v]) for v in range(25)])
print("max common neighbours", max(len(nb[x] & nb[y]) for x in range(25) for y in range(x)))
match = {}
def aug(a, seen):
    for l in nb[a]:
        if l not in seen:
            seen.add(l)
            if l not in match or aug(match[l], seen): match[l] = a; return True
    return False
print("matching", sum(aug(a, set()) for a in range(13)))
M = [(a, l) for l, a in match.items()]   # a cover of size 12 takes one end of each matching edge
cov = {frozenset(M[i][b] for i, b in enumerate(bits)) for bits in itertools.product((0, 1), repeat=12)}
cov = {c for c in cov if all(u in c or v in c for u, v in E)}
print("covers of size 12", len(cov), cov == {frozenset(range(13, 25))})
F = {(a, 13 + j) for a in range(13) for j in range(13) if (a + j) % 13 in {0, 1, 3, 9}}
img = {(a, 13 + (12 - (v - 13)) % 13) for a, v in E}
print("relabeling", len(F), img <= F, sorted(F - img))
# part 2: circuits; a truth table over all 2^n inputs is one integer
def var(i, n):
    t, w = ((1 << (1 << i)) - 1) << (1 << i), 1 << (i + 1)
    while w < (1 << n): t |= t << w; w *= 2
    return t
def run(n, gates):          # gate k is wire n + k, reads two earlier wires; the last gate is the output
    W = [var(i, n) for i in range(n)]
    for op, a, b in gates: W.append(W[a] | W[b] if op == "or" else W[a] & W[b])
    return W
def edge_fn(W, edges):
    f = 0
    for u, v in edges: f |= W[u] & W[v]
    return f
g, outs = [], []
for l in range(13, 25):
    p = sorted(nb[l]); w = p[0]
    for q in p[1:]: g.append(("or", w, q)); w = 24 + len(g)
    g.append(("and", l, w)); outs.append(24 + len(g))
w = outs[0]
for o in outs[1:]: g.append(("or", w, o)); w = 24 + len(g)
W = run(25, g)
print("gates", len(g), "equal on 2^25 inputs", W[-1] == edge_fn(W, E))
fan = [0] * (25 + len(g))
for _, a, b in g: fan[a] += 1; fan[b] += 1
print("input fanout", sum(fan[:25]), "surplus", sum(f - 1 for f in fan[:-1]))
g2 = [(op, a + (a >= 25), b + (b >= 25)) for op, a, b in g]
o = 25 + len(g2)
g2 += [("or", 0, 1), ("or", o + 1, 3), ("or", o + 2, 9), ("and", 25, o + 3), ("or", o, o + 4)]
W2 = run(26, g2)
print("gates", len(g2), "equal on 2^26 inputs", W2[-1] == edge_fn(W2, E + [(0, 25), (1, 25), (3, 25), (9, 25)]))
```

Expected output:

```
pairs 48 difference set True
same list in A3 and A4 form True True
degrees [3, 3, 4, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
max common neighbours 1
matching 12
covers of size 12 1 True
relabeling 52 True [(0, 13), (1, 13), (3, 13), (9, 13)]
gates 59 equal on 2^25 inputs True
input fanout 60 surplus 35
gates 64 equal on 2^26 inputs True
```
