# L-meta-5968 (pequalnp outside proof desk): not proved, nothing submitted

## 1. Outcome

**The goal was not met.** The goal asks for three things; none exists:

| Asked for | Delivered | Evidence |
|---|---|---|
| One Lean 4 theorem proving step L-meta-5968 | **No.** No Lean proof file was produced. | All four results carry `"status": "missing_lemma"` and say so in their first sentence (angle-1: "NOT PROVED; no Lean file"; angle-2: "Not proved; no file offered"; angle-3: "Not proved; no Lean file"; angle-4: "Not proved and not refuted"). |
| A check of that proof on another holder's machine | **No.** There is no proof to check. | Same four results; no check record is among the inputs. |
| A pull request on `open-goat/pequalnp-proofs` from the contributor's account | **No.** | No result reports opening one. Checked at source (section 2): `lean/PEqualNP/Outside/L_meta_5968.lean` does not exist on `main`, and no pull request with 5968 in its title proposes that file. |

This report does not close any of the three. It is a record of why four independent attempts stopped, which of their claims I could re-check at the public sources, what is still open, and what changed in the repository since they ran. Nothing here should be read as "L-meta-5968 is checked".

What the partial work does and does not show:

- The Lean fragments the results mention are scratch files on the workers' machines. None was handed to this step and none is a proof of the posted statement; angle-2 and angle-3 say outright that theirs could not be submitted.
- The graph figures (section 5) are finite calculations about one 11-vertex graph. I replayed them and they agree. They say nothing about circuits: the theorem quantifies over every circuit that meets the hypotheses, and no finite graph computation certifies that.

## 2. State of the step at the public sources

Read on 2026-11-26 (UTC) with `main` at commit `7372d00e842f3b1e5c91e109b0c8cc455cc61f04` (committed 2026-11-26T00:58:36Z).

| Fact | Value | Source |
|---|---|---|
| Desk state of L-meta-5968 | `"state": "leased"`, `"holders": 1`, `"since": "2026-11-26T00:53:22.780Z"`: held by someone, not closed | `https://pequalnp.com/desk/step?gap=L-meta-5968` |
| Proof file on `main` | absent (HTTP 404) | `https://raw.githubusercontent.com/open-goat/pequalnp-proofs/main/lean/PEqualNP/Outside/L_meta_5968.lean` |
| Files with 5968 in their name on `main` | two, both reductions: `R_meta_5968_71.lean` (5,111 bytes), `R_meta_5968_73.lean` (15,427 bytes) | git tree of `7372d00` |
| Pull requests with 5968 in the title | two, both merged reductions: #22201 "R-meta-5968-71" (merged 2026-11-25T23:43:21Z), #22179 "R-meta-5968-73" (merged 2026-11-25T23:47:14Z). A search for the phrase "L-meta-5968" returns 0 | `https://github.com/open-goat/pequalnp-proofs/pull/22201`, `https://github.com/open-goat/pequalnp-proofs/pull/22179`; GitHub issue search over the repository |
| Parent step L-meta-2262 | `"state": "leased"`, `"since": "2026-11-25T21:32:34.538Z"` | `https://pequalnp.com/desk/step?gap=L-meta-2262` |
| Toolchain pin | `leanprover/lean4:v4.36.0` (the results name Lean 4.36.0) | `lean/lean-toolchain` at `7372d00` |

Limits of these reads: the title search cannot see an open pull request whose title does not contain 5968, and I did not page through all open pull requests (the repository had more than 22,600 pull-request numbers at the time). The desk answer does not say who holds the lease.

One naming point. angle-4 says its prebuilt project came from `brilliant-hq/pequalnp-proofs` at `e125f04d0dc6fed67cee48a1d06692912e167c32`. The GitHub API answers that name with a redirect to repository id 1468025030, which is the id of `open-goat/pequalnp-proofs`, and that commit exists there (dated 2026-11-25T15:47:48Z). So it is the same repository under an earlier name. At that commit `lean/PEqualNP/Outside/` holds 5,592 files, the number angle-1 gives, and none has 5968 in its name. At `7372d00` it holds 8,918. The four results therefore predate the two reductions of section 6 or were built from a tree without them.

## 3. The step

L-meta-5968 is the `accounting` hypothesis of the repository's reduction `lean/PEqualNP/Outside/R_meta_2262_2.lean` (angle-1 §1, angle-4 §1). I confirmed this by reading that file at `7372d00`. The hypothesis there reads:

```lean
(accounting : ∀ (G : SimpleGraph (Fin 11)) [DecidableRel G.Adj] (C : Circuit) (d e : ℕ),
  G=edgeGraph 11 [(0,9),(0,10),(1,4),(1,8),(2,5),(2,10),(3,6),(3,7),(4,8),(4,10),(5,8),(5,9),(6,7),(6,10),(7,9),(8,9)] →
  IsLeastAO G C → TopForm G C → C.size<22 → junk G C={d,e} →
  let A := fun k => (gammaE G C k).filter (fun h => ∃ z∈wmax G C k, z∈h)
  let both := gammaE G C d ∩ gammaE G C e
  let safe := ∀ x, gateVal 11 C d x=true → gateVal 11 C e x=true → graphFun G ∅ x=true
  let U := Ustar G C
  ((A d).card≤7 ∧ (A e).card≤7 ∧ (safe → both.card≤8) ∧
  (safe ∨ (wmax G C d ∩ wmax G C e).Nonempty)) → (∀ h∈U, h∈A d ∨ h∈A e ∨ safe ∧ h∈both) →
  ∃ S : Finset (Fin 11), IsMinCover (G.deleteEdges ↑U) S ∧
    5+U.card ≤ S.card+2*(centreless G C).card+(orN G C \ lam G C).card)
```

The posted form, with fully qualified names and variables `x1 … x17`, is the conclusion of `R_meta_5968_71.lean` and `R_meta_5968_73.lean` (the desk rules require a reduction's conclusion to be "the step's statement exactly", `https://pequalnp.com/join.txt`, section REDUCTIONS). It is the same statement up to the names of bound variables; in it `x4, x5` are the two junk gates, `x11` is `A`, `x12` is `both`, `x13` is `safe`, `x14` is `U`.

In `R_meta_2262_2.lean` the hypothesis is used once: the proof starts `by_contra! small`, obtains `S` from `accounting`, and closes with `omega` against the caller's budget and cover hypotheses (angle-4 §1; confirmed in the file). The two bracketed premises of the step are the conclusions of two files already in the repository: `L_meta_5966.lean` (the four bounds; 77,120 bytes) and `L_meta_5964.lean` (the covering condition; 34,394 bytes) (angle-1 §1; statements confirmed at `7372d00`).

angle-1 and angle-2 report that Lean 4.36.0 with the prebuilt project accepts the statement as posted (a skeleton with a placeholder proof elaborates), and angle-3 says the obstacle is "not elaboration". angle-4 does not say either way. I did not run Lean.

Notation below: `U = Ustar`, `c = |centreless|`, `o = |orN \ lam|`, `t = |tops \ centreless|`, `τ(G − U)` = size of a minimum vertex cover after deleting the edges of `U`, `d, e` = the two junk gates (`x4, x5`).

## 4. Why the step was not proved: what all four results agree on

### 4.1 For d ≠ e the conclusion contradicts an inequality the repository already proves

All four results reach this independently.

- The library proves, for any graph with no 4-cycle and a nonempty edge set and any least top-form circuit: `|E| + t + 2c + |junk| + o ≤ size + |U| + 1`, and `|K| ≤ t` for every minimum cover `K` of `G − U`.
- Here `|E| = 16`. With `d ≠ e`, `|junk| = 2`; with `size ≤ 21` this gives `|K| + 2c + o ≤ 4 + |U|` for **every** minimum cover `K`.
- The step asks for some minimum cover `S` with `5 + |U| ≤ |S| + 2c + o`.

So when `d ≠ e`, no circuit that meets the hypotheses can satisfy the conclusion. The step is true only if its hypotheses are contradictory, which means proving it amounts to proving that no least top-form circuit with fewer than 22 gates has this two-junk-gate pattern. In the results' words it is "the 22-gate lower bound for this whole sub-case, not an unfolding" (angle-1 §3), "not a closing count" (angle-2 §1), "the whole branch" (angle-3 §1), "the whole two-junk-gate common-top case of the 22-gate lower bound" (angle-4 §2).

The results cite three different files for the library inequality. I read all three at `7372d00`; each carries the inequality as quoted:

| Result | File cited | What I found there |
|---|---|---|
| angle-1 §3, angle-4 §2 | `L_meta_5781.lean` (116,658 bytes) | top-level theorem, any `n`: hypotheses `NoFourCycle`, `edgeFinset.Nonempty`, `IsLeastAO`, `TopForm`; conclusion as above |
| angle-3 §1 | `L_meta_1491.lean` (115,624 bytes) | same statement, any `n` |
| angle-2 §1 | `L_meta_7247.lean` (149,767 bytes), "Ledger.main, any n" | the top-level theorem is about `Fin 26` only; the helper `Ledger.main` at line 2964 has the any-`n` statement, as angle-2 says |

Each result says it machine-checked the derivation "hypotheses + `d ≠ e` + conclusion ⟹ `False`" in a scratch Lean file that took the library statement as a hypothesis or loaded it. Those scratch files were not among my inputs and I did not re-run them. The arithmetic itself is `16 + t + 2c + 2 + o ≤ 21 + |U| + 1`, which I checked by hand. The caller's own budget hypothesis in `R_meta_2262_2.lean`, `17 + t + 2c + o ≤ size + |U|`, is the same inequality with `|E| = 16` and `|junk| = 2` put in.

### 4.2 The graph alone settles only |U| ≤ 1 and ten pairs

Figures from angle-1 §2, angle-2 §2, angle-3 (table `f`) and angle-4 §5, all replayed in section 5:

- `G` has 11 vertices and 16 edges; `τ(G) = 7`; no two vertices share two neighbours.
- The minimum of `τ(G − U)` over `|U| = k`, `k = 0..16`, is 7,6,5,4,4,3,3,3,2,2,2,2,1,1,1,1,0 (angle-1 §2).
- So `5 + |U| − τ(G − U)` reaches 0,2,4,5,7,8,9,11,12,13,14,16,17,18,19,21 for `k = 1..16` (angle-1 §2). With a leading 0 this is the table `f` = 0,0,2,4,5,7,8,9,11,12,13,14,16,17,18,19,21 indexed `0..16` (angle-3; it is the list in `L_meta_6103.lean` and in the `profile` premise of `R_meta_2704_2.lean`, both confirmed).
- Deleting one edge leaves the cover number at least 6. Of the 120 pairs of edges only 10 keep it at 7: the pairs inside {4-10, 5-8, 6-10, 7-9, 8-9} (angle-2 §2). Example of a pair that does not: `U = {0-9, 1-4}` gives 5 (angle-1 §2).

Consequence, as the results state it: the conclusion follows from the graph for `|U| ≤ 1` and for those 10 pairs. Everywhere else it needs a circuit-side lower bound `2c + o ≥ 5 + |U| − τ(G − U)`. The step's numeric hypotheses do not give one: they cap `|U|` and do not mention `centreless`, `orN` or `lam` (angle-1 §2, angle-2 §2, angle-3 §3).

### 4.3 Sub-cases closed with existing library lemmas (workers' Lean checks; not re-run by me)

- `|U| ≤ 1`: the conclusion holds, from the statement of `L_meta_6103` and the existence of a minimum cover (angle-4 §3; angle-3 §2a). Together with 4.1, no such circuit has `|U| ≤ 1` when `d ≠ e` (angle-4 §3).
- (a) `f(|U|) ≤ 2c + o`: closed by `L_meta_6103` (angle-3 §2a).
- (b) No gate of `centreless ∪ junk ∪ mixing` true at two edges of `U`: closed by `L_meta_6240` and (a), "since f(k) + 2 <= 2k for 1 <= k <= 16" (angle-3 §2b; the inequality on `f` replayed in section 5).
- (c) `2c + o ≤ 1` and `d ≠ e`: `L_meta_7895` gives the nested-cone structure, `L_meta_7897` then `|U| ≤ 3`, and `L_meta_5869`, `L_meta_5871`, `L_meta_2693` give a minimum cover of size at least `4 + |U|` (angle-3 §2c).

angle-3 reports each as Lean-checked with only the axioms `propext`, `Classical.choice`, `Quot.sound`, in a scratch file importing the named lemmas, and adds that none is submittable alone and none uses the step's two premises. I read the statements of `L_meta_6103`, `L_meta_6240`, `L_meta_7895`, `L_meta_7897` and `L_meta_2693` at `7372d00` and they have the shapes angle-3 relies on. I did not read `L_meta_5869` or `L_meta_5871` beyond confirming the files exist (45,560 and 18,629 bytes), and I did not re-run any of the Lean.

### 4.4 What is left, and the lemma that is missing

What remains after 4.3, for `d ≠ e` (angle-3 §3): `2c + o ≥ 2`, `f(|U|) > 2c + o` (so `|U| ≥ 3`), and some gate of `centreless ∪ junk ∪ mixing` true at two or more edges of `U`.

The missing lemma, in the results' words:

- "A bound that charges the U* edges lying in A_d ∪ A_e to centreless tops or to OR gates outside lam" (angle-1 §4).
- "A charging bound: each edge of U, routed through a junk gate … pays for a non-lam OR gate outside F or for a centreless top, so that 2c + o grows with |U|" (angle-2 §3).
- "a charge for the U edges inside, 5 + |U| - tau <= 2c + N" (angle-3 §3).
- "A lemma deriving False (or 22 ≤ size)" from the step's hypotheses with `d ≠ e` (angle-4 §6).

The nearest proved result, named by both angle-1 and angle-3, is `L_meta_7559`: `|U \ (A_d ∪ A_e)| ≤ 2 + o` when `|junk| = 2`. It charges only the edges of `U` outside `A_d ∪ A_e` and is silent when `U ⊆ A_d ∪ A_e` (angle-1 §4, angle-3 §3; statement confirmed at `7372d00`, 55,788 bytes).

angle-3 §3 adds that the missing bound is not a local fact and has to go through minimality (`IsLeastAO`, `size < 22`) by a replacement argument, and gives an example on this graph: `g = (x1 OR x4) AND (x8 OR x10)` is true at the non-edge {1,10}, `wmax g = {0,2,4,6,8}`, `A(g) = {1-8, 4-8, 4-10}`, and `a = g AND (x4 OR x8)` is below `F` and true at all three. The Boolean part of that example is replayed in section 5; `wmax` is a project definition I did not evaluate.

Scale, as the results give it: the proved neighbouring two-junk sub-cases are "412 to 512 KB of case analysis each" (`L_meta_2264`, `L_meta_4901`, `L_meta_5228`; angle-1 §4), and they use hypotheses this step does not have. The file sizes at `7372d00` are 507,709, 512,040 and 412,015 bytes. The contributor rules cap a proof file at 512 KiB (`CONTRIBUTING.md`).

### 4.5 The case d = e is also inside the statement and is not handled

The statement allows `x4 = x5`; the junk set is then one gate. The ledger then gives only `|K| + 2c + o ≤ 5 + |U|`: no contradiction, so "that case needs its own argument" (angle-1 §3). angle-4 §4 goes one step further: by the definition of junk, `safe` is then false, so `U ⊆ A(x4)`, and the conclusion needs equality `|S| + 2c + o = 5 + |U|` there; angle-4 marks this "Not handled; not checked in Lean". angle-3 §4 notes the same gap ("allows x4 = x5"). No result proves or refutes the `d = e` case.

One part of angle-4's reading can be corroborated: the merged file `R_meta_5968_73.lean` derives `d ≠ e` from `safe` by exactly that unfolding of `junk`.

### 4.6 The statement is wider than the case its premises came from

`L_meta_5966` proves the four bounds under `IsAO2`, `¬InCone d e`, `¬InCone e d` and a top with both gates in its cone. `R_meta_2262_2` also knows `d < e`, the routing of each `U` edge and the star shape of the tops. The step keeps none of these (angle-1 §5, angle-2 §4, angle-3 §4, angle-4 §6; hypothesis lists confirmed in the two files). angle-3 §4 suggests that adding them back and `d ≠ e` "should cost the parent nothing", and marks this as its reading, not checked.

### 4.7 Whether the statement is true

Not established in either direction, and every result says so. It fails only if a least top-form circuit of at most 21 gates with this junk pattern exists (angle-1, closing paragraph). No result has a counterexample. angle-4 §5 ran a SAT search for a 21-gate fan-in-two AND/OR circuit (rows: the 16 edge inputs and the 24 maximal independent sets): no answer in 100 seconds, and the same encoding did not return for 22, 23, 24 or 26 gates either, "so this is no evidence in either direction". The star circuit has `|E| + τ − 1 = 22` gates (angle-4 §5).

## 5. Replay of the graph figures (finite calculations only)

I recomputed every graph figure above by exhaustive enumeration over all 2^11 vertex sets and all 2^16 edge subsets of the edge list in section 3 (Python, not Lean). All agree with the results:

| Figure | Stated by | Replay |
|---|---|---|
| 11 vertices, 16 edges | angle-1, angle-2 | 16 distinct edges |
| No two vertices share two neighbours | angle-1 §2 | maximum number of common neighbours is 1 |
| `τ(G) = 7` | angle-1, angle-2, angle-4 | 7 |
| min `τ(G − U)` by `\|U\| = 0..16`: 7,6,5,4,4,3,3,3,2,2,2,2,1,1,1,1,0 | angle-1 §2 | identical |
| `5 + k − ` that minimum, `k = 1..16`: 0,2,4,5,7,8,9,11,12,13,14,16,17,18,19,21 | angle-1 §2 | identical; equals the table `f` on `0..16` |
| One deleted edge leaves `τ ≥ 6` | angle-2 §2 | values 6 and 7 occur |
| 120 pairs, 10 keep `τ = 7`, all inside {4-10, 5-8, 6-10, 7-9, 8-9} | angle-2 §2 | 120, 10, exactly those five edges |
| `τ(G − {0-9, 1-4}) = 5` | angle-1 §2 | 5 |
| `f(k) + 2 ≤ 2k` for `1 ≤ k ≤ 16` | angle-3 §2b | holds for all 16 values |
| 24 maximal independent sets | angle-4 §5 | 24 |
| Star circuit `\|E\| + τ − 1 = 22` | angle-4 §5 | 16 + 7 − 1 = 22 |
| `g` true at non-edge {1,10}; `g` true at edges 1-8, 4-8, 4-10; `a = g ∧ (x4 ∨ x8)` implies the graph function on all 2^11 inputs and is true at those three edges | angle-3 §3 | all confirmed; `N(1) ∪ N(10) = {0,2,4,6,8}`, the set angle-3 gives as `wmax g` |

From the same enumeration: the edge subsets with `5 + |U| ≤ τ(G − U)` number 27 = 1 + 16 + 10 (the empty set, the 16 single edges, the 10 pairs), which is angle-2's "only |U| ≤ 1 and those 10 pairs".

The enumeration, for anyone who wants to repeat it:

```python
E=[(0,9),(0,10),(1,4),(1,8),(2,5),(2,10),(3,6),(3,7),(4,8),(4,10),(5,8),(5,9),(6,7),(6,10),(7,9),(8,9)]
n=11; m=[(1<<u)|(1<<v) for u,v in E]; pc=lambda x: bin(x).count("1")
best=[99]*(1<<16)                       # best[U] = tau(G - U)
for S in range(1<<n):
    unc=sum(1<<i for i,e in enumerate(m) if not e&S)
    best[unc]=min(best[unc],pc(S))
for i in range(16):
    for U in range(1<<16):
        if U>>i&1: best[U]=min(best[U],best[U^(1<<i)])
mn=[min(best[U] for U in range(1<<16) if pc(U)==k) for k in range(17)]
print(mn, [5+k-mn[k] for k in range(1,17)])
print(sum(1 for U in range(1<<16) if pc(U)==2 and best[U]==7))
```

This replay checks arithmetic about one graph. It does not check any claim about circuits and is not a substitute for the Lean theorem.

## 6. What changed in the repository after the four results

Two reductions of L-meta-5968 were merged into `main` on 2026-11-25, after the commit angle-4 built from. Under the desk rules, "If accepted, each hypothesis becomes a step; the step closes when all are proved" (`https://pequalnp.com/join.txt`, REDUCTIONS). Neither closes L-meta-5968: the desk still shows it leased (section 2).

**`R_meta_5968_71.lean`** (pull request #22201, author `UnevenSpace`). Proves the step from two hypotheses:

- `profile`: for every `U ⊆ E` and every vertex cover `S` of `G − U`, `5 + |U| ≤ |S| + f(|U|)`. This has the content of `L_meta_6103.lean`, which is on `main` (the two write "vertex cover" differently: `IsVertexCover` against an explicit ∀). The desk reports L-meta-6103 as `not_open` ("it is checked already, or the fleet stood it down").
- `charge`: under the step's hypotheses and `2 ≤ |U|`, `f(|U|) ≤ 2c + o`. This is the charging bound that angle-1 §4, angle-2 §3 and angle-3 §3 name as missing. It is not proved in that file; it is assumed.

**`R_meta_5968_73.lean`** (pull request #22179, author `puplux`). Proves the step from three hypotheses, each with conclusion `False`:

- `smallU`: `|U| = 2`, a minimum cover `S` with `5 ≤ |S|`, `centreless = ∅`, `|S| + o ≤ 6`.
- `dirtyLarge`: `3 ≤ |U|`, a minimum cover with `7 ≤ |S| + |U|` and `|S| + 2c + o ≤ 4 + |U|`, an input where both junk gates are true and the graph function false, a common `wmax` vertex, `|A d| ≤ 7`, `|A e| ≤ 7`, `U ⊆ A d ∪ A e`.
- `safeLarge`: the same size conditions with `d ≠ e`, `safe`, `|both| ≤ 8`, `U ⊆ A d ∪ A e ∪ both`.

This is close to what three of the results recommended: split by `|U|` (angle-1 §5, angle-2 last paragraph) and state the remainder as `→ False` (angle-1 §5, angle-4 §6). The file's own proof of `7 ≤ |S| + |U|` uses the two triangles 1-4-8 and 3-6-7 and the 5-cycle 0-9-5-2-10, the decomposition angle-4 §5 gives for `τ(G) = 7`.

My reading of how the results bear on these new hypotheses (inference, not checked in Lean): angle-3's sub-case (c) is aimed at the same ground as `smallU` with `d ≠ e`, since `centreless = ∅` and `|S| + o ≤ 6` with `5 ≤ |S|` force `2c + o ≤ 1`. `smallU` with `d = e`, `dirtyLarge` and `safeLarge` are where the missing charging argument of 4.4 and the open case of 4.5 now sit.

Not found: the step ids the desk gave these five hypotheses, and whether any of them has been proved. The desk's `step` lookup answers `not_open` for `R-meta-5968-71` and `R-meta-5968-73` themselves and I did not find a public listing that maps hypotheses to steps.

## 7. Where the results differ

No two results contradict each other. The differences:

1. **Which file carries the ledger inequality**: `L_meta_5781` (angle-1, angle-4), `L_meta_7247` (angle-2), `L_meta_1491` (angle-3). All three carry it (table in 4.1).
2. **The cap on `|U|` from the numeric hypotheses**: "they only bound |U*| by 22, and G has 16 edges" (angle-1 §2); "up to 14 or 16" (angle-2 §2); "14, or 16 under x13" (angle-3 §3). These agree: 7 + 7 = 14 without `safe`; 7 + 7 + 8 = 22 with it, capped by the 16 edges.
3. **How far the partial cases go**: angle-1 and angle-4 close only `|U| ≤ 1`; angle-2 adds the 10 pairs from the graph; angle-3 closes more with library lemmas (4.3) and leaves `|U| ≥ 3`. angle-4 §3 says that at `|U| = 2` its two theorems give "only τ(G − U*) ≥ 5 and 2|centreless| + |orN \ lam| ≤ 1"; that is the entry condition of angle-3's sub-case (c), which uses three further lemmas. These are different depths, not a disagreement.
4. **Size of the neighbouring proofs**: angle-4 §6 says `L_meta_2264` and `L_meta_4901` are "about 490 kB of Lean each"; angle-1 §4 says 412 to 512 KB for three files; angle-2 §1 gives 512,040 bytes for `L_meta_4901`. The tree at `7372d00` has 507,709 and 512,040 bytes (about 496 and 500 KiB), so angle-4's figure is a rounding, slightly low.
5. **Coverage of the library**: angle-1 says it did not read all 5,592 files under `Outside` and "a lemma I missed may exist". No other result claims a complete search either.

Caveat on the workers' Lean checks: angle-2 and angle-3 both report that the Lean binary would not start in their sandbox as shipped and that they ran it with a small preloaded shim (angle-2: reads `/proc/self/exe`; angle-3: a `getpid` shim), with toolchain and project files otherwise the prebuilt ones. angle-4 could not import the `Outside` modules and took two theorem statements as hypotheses instead.

## 8. What is still owed for the goal

In order:

1. **A proof.** Either of
   - the charging bound (`charge` of `R_meta_5968_71`, with `profile` supplied by `L_meta_6103`), or
   - the three refutations `smallU`, `dirtyLarge`, `safeLarge` of `R_meta_5968_73`,
   
   as desk steps of their own, or a direct `L_meta_5968.lean`. Any route must cover both `d ≠ e` (where it has to refute every such circuit below 22 gates) and `d = e` (where equality is needed, 4.5). No result supplies the argument; angle-3 §3 expects it to be a replacement argument through minimality.
2. **A check on a second holder's machine** of whatever file results. None has happened because there is no file.
3. **A pull request** from the proving contributor's account that adds exactly the one named file (`CONTRIBUTING.md`: "It adds exactly one file and changes nothing else"; "The gap must still be posted when the pull request is checked"). None was opened by any of the four workers or by this write-up.

A decision for the requester: the step as originally scoped ("one Lean 4 theorem") did not fit in four attempts, and the repository has since accepted two alternative cuts of it, with two and three smaller hypotheses. Pointing the next attempt at one of those hypotheses, once their step ids are known, matches the repository's current state and the reposting advice in the results. All four results carry the status `missing_lemma`; for a step handed back with that reason the desk says "we post the smaller steps it needs" (`join.txt`). Whether the four workers released their leases at the desk is not recorded in the results.

## 9. Not checked, not found

- No Lean was run for this report. Every "Lean-checked" statement above is a worker's report about a scratch file I was not given.
- `wmax`, `gammaE`, `junk`, `TopForm`, `IsLeastAO` and the other project definitions under `PEqualNP/Defs` were not read; where a claim depends on them (for example `wmax g = {0,2,4,6,8}`) it stands on the result that made it.
- `L_meta_5869.lean`, `L_meta_5871.lean`, `L_meta_2264.lean`, `L_meta_4901.lean`, `L_meta_5228.lean` and `L_meta_4899.lean` were confirmed to exist with the stated sizes but their statements were not read.
- angle-4's SAT search and the brute-force scripts of angle-1 and angle-2 were not supplied; the graph figures were recomputed independently (section 5), the SAT search was not repeated.
- Who holds the current lease on L-meta-5968, and whether an open pull request for it exists under a title without "5968", could not be determined.
- angle-4 mentions a `sources.json` of its own; it was not among the inputs.

## 10. Sources

Inputs (read as data): `.imd/reads/artifacts/item-angle-1` (SHA-256 `892f865e…b628`), `item-angle-2` (`8b29a449…163d`), `item-angle-3` (`7dab40f1…fb57`), `item-angle-4` (`39dcc772…9314`). All four hashes matched the ones given with the task.

Public sources, all read at `main` = `7372d00e842f3b1e5c91e109b0c8cc455cc61f04` unless stated:

- Repository: `https://github.com/open-goat/pequalnp-proofs` (`README.md`, `CONTRIBUTING.md`, `lean/lean-toolchain`)
- Parent reduction: `https://github.com/open-goat/pequalnp-proofs/blob/7372d00e842f3b1e5c91e109b0c8cc455cc61f04/lean/PEqualNP/Outside/R_meta_2262_2.lean`
- Reductions of the step: `…/lean/PEqualNP/Outside/R_meta_5968_71.lean`, `…/R_meta_5968_73.lean` (same commit); pull requests `https://github.com/open-goat/pequalnp-proofs/pull/22201` and `https://github.com/open-goat/pequalnp-proofs/pull/22179`
- Library lemmas whose statements were read (same directory, same commit): `L_meta_5781.lean`, `L_meta_1491.lean`, `L_meta_7247.lean`, `L_meta_6103.lean`, `L_meta_7559.lean`, `L_meta_5966.lean`, `L_meta_5964.lean`, `L_meta_6240.lean`, `L_meta_7895.lean`, `L_meta_7897.lean`, `L_meta_2693.lean`, `R_meta_2704_2.lean`
- File sizes and counts: `https://api.github.com/repos/open-goat/pequalnp-proofs/git/trees/7372d00e842f3b1e5c91e109b0c8cc455cc61f04?recursive=1` and the same for `e125f04d0dc6fed67cee48a1d06692912e167c32`
- Absence of the proof file: `https://raw.githubusercontent.com/open-goat/pequalnp-proofs/main/lean/PEqualNP/Outside/L_meta_5968.lean` (404)
- Pull-request search (evidence of absence only): `https://api.github.com/search/issues?q=repo:open-goat/pequalnp-proofs+5968+in:title` (2 results, both reductions) and the same with the phrase `"L-meta-5968"` (0 results)
- Desk: `https://pequalnp.com/desk/step?gap=L-meta-5968` (also `gap=L-meta-2262`, `L-meta-6103`, `R-meta-5968-71`, `R-meta-5968-73`); rules: `https://pequalnp.com/join.txt`
- Earlier repository name: `https://api.github.com/repos/brilliant-hq/pequalnp-proofs` (301 to repository id 1468025030)
