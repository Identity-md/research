# L-pcx-167 (desk pequalnp): write-up of four results

## Outcome

**Not proved. The goal is not met.** None of the four results contains a Lean theorem. So there is nothing for another holder to check and no pull request to open on open-goat/pequalnp-proofs. All four results have `"status": "other"` and say "No Lean file is offered" (item-angle-1, -2, -3, -4). None of them shows that the statement is false either.

The statement asks for a list π with `IsRefutation (PHP 5 4) π` and `π.length ≤ 139` (formal statement: https://data.pequalnp.com/data/lemma/L-pcx-167.b3805b76f7db.json, as cited by the review of the previous submission).

## Sources

The four inputs were handed to this write-up as files under `.imd/reads/artifacts/`. They are not in Git, so the reader cannot open them from this repository. Their SHA-256 hashes are:

- item-angle-1: `5857d5b78ac4588a96503f48b5b5bdc18e39b5761e0beb47c4999d74ba0fe78d`
- item-angle-2: `7193beaad99528f32295c2bdd999dabc1a851f3bcc6c11c2ce37802a4a1b58b9`
- item-angle-3: `358bc5e3f1c91d0f70f15bdcd972b62fb4d4a8fe7a937d7b3cd0d08b63df2765`
- item-angle-4: `287adfe30ae522331001d94193b324e31c75eb1fe8e593f2881f895a726286c0`

Every figure below is quoted from these files, and the note after each figure names the file it comes from. The scripts, search logs and the 156-line list that the results describe were **not delivered**. Angle-1 says "scripts not delivered". So the computations cannot be re-run from this write-up.

## Findings the results agree on

- **The proof system is plain resolution.** `IsRefutation` uses exact resolvents and has no weakening rule. The length counts every line, axioms included (angles 1–4).
- **All 45 axioms must appear, which caps the resolvents at 94.** PHP 5 4 has 45 clauses: 5 pigeon clauses and 40 hole clauses. The formula is minimally unsatisfiable, so every refutation lists all 45 axioms. A refutation of at most 139 lines therefore has at most 94 resolvents (angles 1–4).
- **The textbook construction is 18 lines too long.** The standard subset dynamic-programming refutation uses 112 resolvents, which gives 45 + 112 = 157 lines (angles 1–4).
- **Small cases:**
  - PHP 3 2 has a proven minimum of 19 lines, since 9 resolvents is UNSAT and 10 is SAT (angle-1 with CaDiCaL, angle-4 with CP-SAT).
  - On PHP 4 3, the exhaustive runs returned no answer (angles 1 and 4).
  - Local searches on PHP 4 3 never went below the 58-line baseline (angles 2 and 3).

## Best result found: 156 lines (unverified here)

- Angle-2 reports 156 lines (111 resolvents) from simulated annealing over the branching policies of a DPLL procedure with clause caching. It says the result was "re-checked ... line by line" by a separate script, "not run through Lean".
- Angle-3 reports the same count, 111 steps = 156 lines, reached in ten of twelve runs. It says "an independent checker confirmed" it, and it explains the one-step saving by hand (its trick (3)).
- Neither result includes the list, so this write-up cannot inspect it. 156 is 17 lines more than the 139 the statement allows.

## Bounds already in the project (as reported)

- `PEqualNP/Outside/L_pcx_171.lean` proves at most 159 lines for this formula and system, using the chkR / axPHP / `decide +kernel` checker pattern (angles 1–4).
- `L_pcx_173` proves at most 169 lines (angle-2).
- `L_pcx_158` proves that no refutation has at most 89 lines, i.e. a lower bound of 90 (angles 3 and 4).
- `L_pcx_199` proves at most 140 lines, but for **Res(2)**: its lines are 2-DNFs, not clauses (angles 2–4). The step's sketch mentions linear clauses and weakening, which are Res(lin) features (angles 1, 2 and 4). Angles 3 and 4 suggest that the desk's figure of 140 may come from one of those stronger systems. They offer this as a guess, not a finding.

## What is missing

1. A plain-resolution refutation of PHP 5 4 with at most 139 lines. None was found, and none of the results claims to have one.
2. As a result, there is also no Lean theorem, no check by another holder and no pull request.

If such a list is ever supplied, the results say the Lean side is routine: reuse the L_pcx_171 checker pattern (angles 1–4). A provable statement within reach of this work is a bound of 156 lines (angle-2), but that is not this step.
