# L-meta-10006 (pequalnp outside proof desk): write-up of four results

## Outcome: the goal is NOT met

The goal is a Lean 4 theorem for step L-meta-10006, checked on another holder's machine and opened as a pull request on open-goat/pequalnp-proofs by the contributor whose machine proved it. **None of the four results has a proof, so I cannot supply any of those three things.** No Lean file exists, so no independent check took place and no pull request was opened. This write-up adds no proof of its own. The step is still open.

| Result | Status | Lean file |
|---|---|---|
| item-angle-1 [A1] | `other`: "could not prove the step, and I did not find it false" | none |
| item-angle-2 [A2] | `out_of_time`: "NOT PROVED and not refuted" | none |
| item-angle-3 [A3] | `missing_lemma`: "NOT PROVED" | none |
| item-angle-4 [A4] | `missing_lemma`: "NOT PROVED AND NOT REFUTED" | none |

## The statement

The step says the 775 zero entries of a 31x31 0/1 matrix cannot be covered by 15 all-zero rectangles, so any such cover needs at least 16 [A1, A3]. All four results identify the matrix as the circulant point-line incidence matrix of the projective plane of order 5, made of the cyclic shifts of 427073 = bits {0,6,10,15,17,18}. Every row and column has 6 ones, any two rows share exactly one 1, and the matrix has 775 zeros [A1–A4].

## What is known about the cover number (none of it proves the step)

| Bound | Value | Source | Status |
|---|---|---|---|
| Lower | no cover with at most 13 rectangles, so at least 14 | L_meta_10002 in the prebuilt project, as reported by [A1, A3] | in the project. I did not re-check it here. |
| Lower (required) | at least 16 | the step | **unproved** |
| Upper | 24 | L_meta_10013, as reported by [A3, A4] | in the project, as reported |
| Upper | 22 (explicit covers) | [A3, A4] | computational and re-checked by script, not formalised |

The cover number therefore lies somewhere from 14 to 22. The required bound of 16 is not established.

## Why the standard certificates stop short of 16 (all four results agree)

- **Area:** the largest all-zero rectangle has area 60 (6x10 or 10x6), and 775/60 = 12.92 gives only 13 [A1–A4].
- **Fooling set:** k(k-1)/2 ≤ 6k gives k ≤ 13 [A1–A4].
- **No weighting can do better:** there are 3100 zero rectangles of each maximal shape. Each zero lies in 240 rectangles of one shape [A2, A3], which is 480 of the 6200 counting both shapes [A4]. That gives a fractional cover of 12.92, so no LP-dual or entry-weighting argument can certify more than 13 [A2, A3, A4].
- **Row/column loads (the method of L_meta_10002):** the LP optimum is 7223/543 ≈ 13.3, which gives 14 [A4]. A column-wise branch and bound gives 31·14/33 = 13.15, which also gives 14 [A2].

## Partial results (not formalised)

- A spectral inequality, Q ≥ s²(1+36/(5K))/961. It reproves the bound of 13 and shows that a 15-cover would have to cover zeros three or more times, heavily (Σ(m-1)(m-2) > 97) [A4]. [A2] derives a similar condition independently.
- A 15-cover needs at least ten rectangles of area 40 or more [A3].
- The slack for 15 rectangles is 15·60 − 775 = 125 [A1, A2].

## Search evidence (heuristic only)

- Simulated annealing at 15 rectangles never covered all the zeros. The best runs left 93 [A1], 174 [A2], 90 [A3] and 90 [A4] zeros uncovered.
- SAT solvers did not decide any case. CaDiCaL ran for 270 s at K=10–15 [A1], and Kissat ran for 7 min at K=15–24 [A4].

## What is missing

The results name what a proof would need: a structural lemma that forces overlap among near-maximal rectangles [A1], or a bound on triple overlaps [A4], or an exhaustive search small enough for the Lean kernel to replay within the 524288-byte file limit, without native_decide [A1, A3]. None of these was found.

## Sources

- [A1]–[A4]: `.imd/reads/artifacts/item-angle-1` … `item-angle-4` (SHA-256 6b013d9e…, d430f585…, d6079bc4…, 4a3f0847…).
- I did not search GitHub in this run. No pull request is cited because the results give no proof to submit.
