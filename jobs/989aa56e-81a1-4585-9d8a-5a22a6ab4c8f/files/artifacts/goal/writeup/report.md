# IMD goal write-up: Erdős #647, #366, #364, #324 quintic, #723 eq-12 (continuation of goal 58bb39f6)

## Outcome: nothing is solved

**None of the five targets is solved.** No proof or refutation of any official `Challenge.lean` statement was found, so there is no `Main.lean`, no successful attempt, no success chat log and no second-agent re-check (re-checking only applies to a solved target). Nothing was submitted to conjectures.io. No accounts were created, no credits were bought and no TAO was spent. This report is meant for the requester only; it does not publish the sources anywhere else.

What is delivered instead, per target: the compiled partial lemmas as **full Lean source** (in the embedded bundle at the end, with a sha256 for every file), the build and `#print axioms` evidence that exists, and where each proof is stuck. Each build or axiom claim below says which run produced it:

- the **item run**: the worker run that produced that target's result;
- a **prior job**, linked;
- **this write-up run**.

Anything not reproduced is marked **UNVERIFIED**.

Common pins: Lean `4.35.0-rc2` (commit `11acb17ec6b07a8f9e9173e6845197929540936b`), Mathlib `065356127b1dc0016f66b7283ce0ce2c4055aa55`, Formal Conjectures `6adcbe13652f4e7c69ad02a783465ae2a99d5cb3`.

The `6adcbe13` commit object is not public: the GitHub commit API answers "No commit found" (item results #364 and #723). It was therefore reconstructed in the way the target metadata describes:

1. Check out upstream base `7d1a8c9912747679d0093f6d1216420c33ee5ffa`.
2. Apply the [audit patch](https://raw.githubusercontent.com/conjectures-io/conjectures-tasks/f5dab9b843c460bf946e0ec7b0e6ad2f2f739eb8/tiers/tier-1/formal-conjectures-audit-fixes.patch) (sha256 `352280407fbbe83e636aa07a5c090aab15c6353c7cd77c0491284cd40df51275`).
3. Add [TaskSupport.lean](https://raw.githubusercontent.com/conjectures-io/conjectures-validator/57c969e87cad845b60908cef474c8d1c0b6e43c5/lean/TaskSupport.lean) (sha256 `58a80a223dbd7383d92eb2a57b1ec207c0991131a1a1bf24585a4452777c257e`).

**This write-up run reproduced that reconstruction on its own:**

- the patch and TaskSupport downloads matched both sha256 values;
- `git write-tree` after applying the patch gave tree `0766488c915be93b33c98aae256543800ee2a84c`, the same as the #647 item and the #723 prior job;
- the patch contains no hunk for `ErdosProblems/324.lean`, `364.lean` or `723.lean`, so for those three targets the pinned statement is the base-commit text;
- the manifest pins Mathlib `065356127b1d…`, and `lake exe cache get` fetched 8915 files;
- `lake build '+FormalConjectures.ErdosProblems.«364»' '+…«324»' '+…«723»'` with the native aarch64 Lean 4.35.0-rc2 build finished with **"Build completed successfully (9200 jobs)", exit 0** (`this-run/fc-modules-build.log`).

The official Challenge files fetched from the [goal-named repo at 3d3f3a09](https://github.com/identity-md-launches/goal-3467-objective-settle-least-one/tree/3d3f3a09d60c67992738413746463076008eb894/catalog/targets) hash as follows:

| Challenge | sha256 | Match |
|---|---|---|
| #364 | `0608e0e2a751e8156341b50347548b168730106e6f4230abdf041bc49cf52219` | matches the hash recorded by the #364 item |
| #723 | `61851a3cc2d776cd91d4fcd75686ed7b8538ab30832356be34dca776964a7c0b` | matches the #723 item |
| #324 | `6e1d6cdc1d601aef3c91c4a52dc918c5b4502bf04dff2985eb07940fbc81b232` | none recorded to compare |

**This run's own lemma compilation did not finish.** Nine `lake env lean <file>.lean` runs were started in parallel against that tree: the new #364 and #324 files, the four #723 files, and the three unmodified Challenge stubs as a control. **All nine were killed by a 520 s timeout (exit 124)**, the Challenge stubs included. A Challenge stub only imports Mathlib, FC and TaskSupport and then hits `sorry`, so the timeout comes from the environment (loading Mathlib nine times at once on this machine), not from the proofs. The logs are `this-run/*.log`.

An earlier single run of the #324 file at a search bound of 40 also hit the 10-minute tool limit. That bound was then cut to 15.

So **no lemma compile or `#print axioms` result from this write-up run is claimed.** The compile evidence below comes from the item runs and the prior jobs, and it is labelled that way.

| Target | Solved | Lemma source delivered | Compiled & axioms (who) | Pinned FC + official Challenge |
|---|---|---|---|---|
| #647 | No | `647/Extension.lean` (11 new theorems) | Item run: Lake exit 0, 9212 jobs, all 11 `[propext, Classical.choice, Quot.sound]`; condensed log included | Yes (reconstructed tree 0766488c) |
| #366 | No | `366/Partial366.lean` (9 new theorems) | Item run: "Build completed successfully (9207 jobs)", axioms standard | Yes (item reports tree `33f872f2…`, see §366) |
| #364 | No | `364/Erdos364Partial.lean` (compiled, vendored defs) + `364/Erdos364Official.lean` (official defs, **not compiled**) | Item run: 8932 jobs, standard axioms, vendored defs only | Vendored in the item run; this run showed the defs match FC (see §364) |
| #324 quintic | No | `324/Erdos324Partial.lean` (new, **not compiled**) | None | Statement verified at the pinned base (this run) |
| #723 eq-12 | No | `723/{IncidenceBridge,GridBridge,McKayObstruction,ProductObstruction}.lean` | Prior job only (axiom outputs included); this run's recompile timed out | Prior job: tree 0766488c |

---

## Erdős #647

**Status: UNSOLVED.**

Target type: `True ↔ ∃ n > 24, (⨆ m : Fin n, (m : ℕ) + σ 0 m) ≤ n + 2`. The counterexample Challenge is its negation. Sources: [positive Challenge](https://raw.githubusercontent.com/identity-md-launches/goal-3467-objective-settle-least-one/3d3f3a09d60c67992738413746463076008eb894/catalog/targets/erdos647-erdos-647/formalized/Challenge.lean), [counterexample Challenge](https://raw.githubusercontent.com/conjectures-io/conjectures-tasks/f5dab9b843c460bf946e0ec7b0e6ad2f2f739eb8/versions/fc-v2-erdos647-erdos-647-18af8d4ee1176a6aaf75cb6b-counterexample/Challenge.lean).

**Rebuilt prior lemmas (item run).** `Early.lean` (18 declarations), `Lemmas.lean` (28) and `WitnessReview.lean` (108) all passed with standard axioms. They come from the [early attack](https://api.imd.fun/artifacts/f5453ec0b62391aee0c76de9c7ba4b021caf360f8c976a6705cc044822fe838b), the [continuation](https://api.imd.fun/artifacts/4344c7021d19a9b6093d2f0640ace2b23976014adbc1c45dc72260791f94be7e) and the [witness review](https://api.imd.fun/artifacts/3d284b15746fdadb318f22a55d82f51ccab0e0b5144e1dfdb4b3ef6be9bf6fb9). Those artifacts hold the *prior* modules. The *new* lemmas are not in them; they are in `647/Extension.lean` (sha256 `66c91cbc3f81d8888d018dcaad52feaa9169f9cffe33ed1fc6654f1d337f058d`, 16,920 bytes; `import Lemmas`, `import Challenge`).

**New theorems in `Extension.lean`** (namespace `Bounty`):

- `prime_of_sigma_lt_three`, `prime_of_sigma_lt_four`;
- `prime_cofactor_of_dvd`, `prime_at_shift_one`;
- `required_prime_cofactors`: for `n > 97368`, `n−1` and `n/k−1` (k = 2, 3, 4, 6, 12) are prime;
- `no_budgets_through_1770`: 141 overlapping intervals;
- `no_budgets_through_97368`: with the 2520 rule this forces `360360 ∣ n`;
- `prime_cofactor_at_shift_eight`, `prime_cofactor_at_shift_five`;
- `challenge_prime_reduction`: an equivalence for the official type, with only shifts where `k+2 < 2⌊√n⌋` checked;
- `reject_36036000416802347161200`.

**Build (item run).** The item reports Lean 4.35.0-rc2 and Mathlib `06535612`, on the tree reconstructed from base `7d1a8c99` plus the audit patch (tree `0766488c`). The command was `lake build FormalConjectures/ErdosProblems/647.lean TaskSupport Challenge Early Lemmas WitnessReview Extension PositiveChallenge` plus `lake env lean ReviewAudit.lean`. The log ends "Build completed successfully (9212 jobs)", and each of the 11 new `#print axioms` gives `[propext, Classical.choice, Quot.sound]`.

The full item log (`final-build.log`, 102,342 bytes, sha256 `4ffb2fd781737b7d50cba5dd37e5613f9ff34116af1d510b2cd911810304b46c`) is mostly copyright-linter warnings. It is delivered condensed as `647/final-build.condensed.log` (37 lines: every `info:` axiom line, the `sorry` warnings of the two Challenge stubs, and the final line). Re-running it in this write-up run: **UNVERIFIED**, because the compile timeouts described above apply.

**Bounded search (item run, Python/C++ sieve; UNVERIFIED in Lean).** Window `j = n/360360 ∈ [100000001000000000, 100000001999999999]`. Pipeline counts, as given in the item result:

| Stage | Count |
|---|---|
| Wheel residues (wheel modulus 861764) | 37908 |
| After the wheel | 43,988,844 |
| After the prime sieve (sieving primes 17–997 dividing `n−k` at any tested shift) | 17,689 |
| After the 361 lift | 17,594 |

The survivor row is **cumulative over that pre-sieved set**, testing only shifts 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 24 in that order:

```text
shift        1    2   3   4   5  6  8  9  10  12  24
survivors 4198  996 240  56  17  7  3  1   0   0   0
```

Shift 7 is **not** a tested shift. So "the one candidate reaching shift 10", n = 36036000416802347161200 (j = 100000001156627670), only passed the tested shifts. This run checked that `n−7 = 7·47·3274070147·33454358411`, which has 16 divisors and is over the budget of 9. That kills it independently.

This run also checked two multipliers a reviewer found to pass every shift 1–9: j = 100000001742999244 and j = 100000001938020751. For both, `n−10` is divisible by a sieving prime (19 and 17 respectively), so the pre-sieve removed them correctly, and both fail at shift 10. The counts are therefore not raw survivor counts over all 10⁹ multipliers. On that raw basis the reviewer reports about 1.0·10⁸ surviving shift 1 (UNVERIFIED here).

The conclusion is unchanged: no multiplier in the window passes the tested shifts through 10. This bounded result is UNVERIFIED in Lean beyond the single `reject_…` theorem.

**Where it is stuck.** One would need either a multiplier `j` meeting every budget `τ(360360j − k) ≤ k+2`, or a proof that every eligible `j` has an over-budget shift. The required window of shifts grows with the candidate, so no fixed finite sieve closes the case.

**Literature.** Two external sources were flagged as not re-established, and the reviewer reports both are reachable and say what is attributed to them:

- [Mian–Siddique, arXiv 2608.17880](https://arxiv.org/abs/2608.17880): a kernel-checked exclusion through 10⁹.
- [Tölö README](https://raw.githubusercontent.com/fjordmindlabs/math/main/erdos647-sparse/README.md): kernel-checked `2520 ∣ n (n > 1800)` and `360360 ∣ n (n > 10^5)`, and an exclusion to 10¹³.

This write-up run did not re-fetch them, so their content is **UNVERIFIED here**. If they read as quoted, then the residue reductions (`no_budgets_through_1770`/`97368`, `360360 ∣ n`) **restate published results** and are not new. The new content would then be limited to the prime-cofactor lemmas and `challenge_prime_reduction`, whose novelty is UNVERIFIED.

Other sources cited by the item: [Erdős Problems #647](https://www.erdosproblems.com/647) (n = 24 and Schinzel's Hypothesis H; that site refuses automated fetches, see §364, so this is **UNVERIFIED**), [Hughes](https://raw.githubusercontent.com/scottdhughes/erdos647-proof-chain/main/README.md) and [Veljjanoski](https://raw.githubusercontent.com/veljjanoski/erdos647/main/README.md) (a GPU scan to 10²², UNVERIFIED).

---

## Erdős #366

**Status: UNSOLVED.**

Positive Challenge: `True ↔ ∃ n > 0, Nat.Full 2 n ∧ Nat.Full 3 (n + 1)`. Sources: [positive](https://raw.githubusercontent.com/conjectures-io/conjectures-tasks/f5dab9b843c460bf946e0ec7b0e6ad2f2f739eb8/versions/fc-v2-erdos366-erdos-366-d0f03abf2067a02de9e6ce2f-formalized/Challenge.lean), [counterexample](https://raw.githubusercontent.com/conjectures-io/conjectures-tasks/f5dab9b843c460bf946e0ec7b0e6ad2f2f739eb8/versions/fc-v2-erdos366-erdos-366-36250ff6331dcba94150a949-counterexample/Challenge.lean), [metadata](https://raw.githubusercontent.com/identity-md-launches/goal-3467-objective-settle-least-one/3d3f3a09d60c67992738413746463076008eb894/catalog/targets/erdos366-erdos-366/metadata.json).

**Prior modules rebuilt (item run).**

- `PriorPell.lean`: `.compiled_lemmas` of the [Pell artifact](https://api.imd.fun/artifacts/8bcea98184ef00b3f4a21c9aa486ab213d51b8ca7a24f0b0235c4768c0f0a080).
- `PriorMordell.lean`: `.files["Lemmas.lean"]` of the [Mordell artifact](https://api.imd.fun/artifacts/2b6296cdb25a1c9237c102cc1bbe379d58016819e9f5c67e18cc7b89bfbd5e0c).
- See also the [prior merge](https://api.imd.fun/artifacts/4e00cbd672d6bf02e6883504d921f60a3e4506bfb1c229274c914fd8f655b04d) and the [Pell continuation](https://api.imd.fun/artifacts/3c5010e126048eb34991ff36947ae5eea8e33f38cf00303a66d3ef25896c5631).

The Pell continuation's rejection of 59 candidates and the Mordell search's 339 unsettled pairs are **UNVERIFIED**.

**New theorems** in `366/Partial366.lean` (sha256 `5ee10b1edb833829c1cb47968c558a3dace049bdf94114a700a9325cb5bbb4c2`; `import PriorMordell`, `import TaskSupport`; namespace `Erdos366Extension`):

- `squarefull_normal_form`, `cubefull_normal_form`;
- `target_iff_normal_form`, `target_iff_normalized_mordell`: the target is equivalent to a point on `Y² + q²B³ = X³` with `q = b⁴c⁵` and the stated coprimality and divisibility conditions;
- `negative_B_isSquare_mod`;
- `no_witness_le_1000000`: kernel `decide` over a normal-form table;
- `atlas_endpoint_excluded`: `10^25+1` has 11-adic valuation 1;
- `pell_successor_not_full`;
- `official_iff_above_checked_bound`: the official type ↔ ∃ n > 1,000,000 ….

**Build (item run).** `lake build Challenge PriorPell PriorMordell Partial366` ended "Build completed successfully (9207 jobs)". `#print axioms`: `Bounty.mordell_of_rep` gives `[propext]`; all nine new theorems and twenty prior ones give `[propext, Classical.choice, Quot.sound]`. The item gives a log excerpt only, and the full log was not supplied. The item reports tree `33f872f26b34e6043650c6a699ea6519039cf8b5` after applying the same patch to `7d1a8c99`. That differs from the `0766488c` found by #647, #723 and this run. The likely cause is the extra files staged before `write-tree`, but this is **UNVERIFIED**.

**Where it is stuck.** One needs either an admissible Mordell point giving n > 10⁶, or a uniform exclusion over unbounded (B, b, c).

**Literature (item).**

- [Erdős Problems #366](https://www.erdosproblems.com/366): the pairs (8, 9) and (12167, 12168), and abc-conditional finiteness. The site returns HTTP 403 to automated fetches (see §364), so this reading is **UNVERIFIED**.
- Conditional bound: [theofilxeff Challenge](https://raw.githubusercontent.com/theofilxeff/erdos_366/866c5c5e21589b55808f7b8ad1ec6e4ebf9dc346/Challenge.lean).
- [Atlas sweep](https://raw.githubusercontent.com/techno-optimist/erdos-frontier-atlas/165f845a061c73c104a639efa9dce0a531b7d602/certificates/erdos-366/RESULT.json): no hit below 10²⁵ (UNVERIFIED).
- [Chan, arXiv 2503.21485](https://arxiv.org/abs/2503.21485): a special case only.

---

## Erdős #364

**Status: UNSOLVED.** Target: `¬ ∃ n, n.Powerful ∧ (n+1).Powerful ∧ (n+2).Powerful` ([Challenge](https://raw.githubusercontent.com/identity-md-launches/goal-3467-objective-settle-least-one/3d3f3a09d60c67992738413746463076008eb894/catalog/targets/erdos364-erdos-364/formalized/Challenge.lean), [metadata](https://raw.githubusercontent.com/identity-md-launches/goal-3467-objective-settle-least-one/3d3f3a09d60c67992738413746463076008eb894/catalog/targets/erdos364-erdos-364/metadata.json)). The prior job had no partial lemmas for #364. They were written in the item run.

**Compiled lemmas (item run, vendored definitions).** `364/Erdos364Partial.lean` (sha256 `c076ca85917e8060f7e876aa29d880b79d7d86b96c7d603d366fc0d581304d5c`) contains:

- `Powerful.sq_dvd`, `powerful_zero`, `not_powerful_of_witness`;
- `Powerful.mul`, `Powerful.of_mul_coprime`;
- `triple_mod_four`, `triple_mod_nine`;
- `triple_mod_36`: n % 36 ∈ {7, 27, 35}, Beckon's condition, formalised;
- `triple_mod_prime_sq`;
- `triple_iff_sq_sub_one`: a triple exists ⇔ an even powerful x > 0 exists with x² − 1 powerful;
- the sound checkers `isPrimeB_sound` and `findW_sound`;
- `no_triple_below`: no triple with n < 2000, by `decide +kernel`;
- `counterexample_constraints`.

Build (item run): "Build completed successfully (8932 jobs)", exit 0. `#print axioms` for the five headline theorems gives `[propext, Classical.choice, Quot.sound]`. The item tried and dropped a bound of 10000 after more than 10 minutes.

**Why the definitions were vendored, and what this run checked.** The item run could not fetch commit `6adcbe13` and did not use the base-plus-patch route that #647 and #366 used. It copied `Nat.Full` and `Nat.Powerful` into the namespace `Vendored` and did not compile the official Challenge. That was a choice made by that worker, not a property of this target. This write-up run applied the route to #364:

- the patch has no hunk for `ErdosProblems/364.lean`;
- `FormalConjectures.ErdosProblems.«364»` built (exit 0, see above);
- the pinned `FormalConjecturesForMathlib/Data/Nat/Full.lean` defines `def Full (k : ℕ) (n : ℕ) : Prop := ∀ p ∈ n.primeFactors, p^k ∣ n` and `abbrev Powerful : ℕ → Prop := (2).Full`;
- `364.lean` states `theorem erdos_364 : ¬ ∃ (n : ℕ), Powerful n ∧ Powerful (n + 1) ∧ Powerful (n + 2)` under `open Nat`.

The vendored `Full` is textually identical, and the vendored `Powerful := Full 2` is the same abbreviation.

**Extension (this run, NOT compiled).** `364/Erdos364Official.lean` (sha256 `ba981eb9d7aed73398279b7c4f57e17cc407e98c081c75e56f34156e9032c97f`) is the same file with these changes:

- it imports `FormalConjectures.ErdosProblems.«364»` and `TaskSupport`;
- it sets `abbrev Powerful := Nat.Powerful` (the official predicate);
- it adds `powerful_iff_official` (`Iff.rfl`);
- it adds `official_iff_no_large_triple`: `fcTypeOfName% "Erdos364.erdos_364" ↔ ¬ ∃ n, 2000 ≤ n ∧ n % 36 ∈ {7,27,35} ∧ …`.

Its compile hit the 520 s timeout, so it is **UNVERIFIED Lean source**.

**Where it is stuck.** The statement `∀ x even, Powerful x → Powerful (x²−1) → x = 0` is equivalent to the conjecture. Local conditions mod p² leave the residues {0, p²−1, p²−2} for every prime p, so by CRT no finite set of congruences rules it out. A global Diophantine input is needed: abc gives only conditional finiteness.

**Literature (item).**

- Wikipedia (Powerful number): open, the Erdős–Mollin–Walsh conjecture.
- Beckon, Rose-Hulman UMJ 20(2): the mod-36 condition.
- [Chan, arXiv 2503.21485](https://arxiv.org/abs/2503.21485): the cube-middle case only.

The item says erdosproblems.com/364 returned **HTTP 403**, so its status there is **UNVERIFIED**. The pinned FC file tags `erdos_364` `@[category research open, AMS 11]` (checked in this run). One #364 source was flagged as not re-established on re-read. It is most likely the Beckon citation, which the item gives without a URL, so the mod-36 attribution rests on the Lean proof `triple_mod_36` and not on that source.

---

## Erdős #324, quintic

**Status: UNSOLVED.**

**Statement verified in this run.** The patch has no hunk for `ErdosProblems/324.lean`, and the built pinned base gives, at line 43:

```lean
@[category research open, AMS 11]
theorem erdos_324.variants.quintic : {(a, b) : ℕ × ℕ | a < b}.InjOn fun (a, b) => a ^ 5 + b ^ 5
```

This is the text the item quoted from `main`. Its "pinned text UNVERIFIED" caveat is therefore resolved. The official [Challenge](https://raw.githubusercontent.com/identity-md-launches/goal-3467-objective-settle-least-one/3d3f3a09d60c67992738413746463076008eb894/catalog/targets/erdos324-erdos-324-variants-quintic/formalized/Challenge.lean) is `theorem target : fcTypeOfName% "Erdos324.erdos_324.variants.quintic"`.

**Item run.** That worker's machine had no Lean, and the prior job had no partial lemmas for #324, so no lemma was compiled. A Python search over all 4,498,500 pairs 0 ≤ a < b < 3000 found **0 collisions** of a⁵ + b⁵ (no script was supplied; it is consistent with the conjecture and is not a proof).

**New lemma source (this run, NOT compiled).** `324/Erdos324Partial.lean` (sha256 `425b927c301bff5e11173a24aa2ddf16e8612bdede19ca3cc16e35e5eabecf6e`; imports Mathlib, `FormalConjectures.ErdosProblems.«324»` and `TaskSupport`; namespace `E324`):

- `official_type_eq`: by `rfl`, the official type is the InjOn statement;
- `pow5_strictMono`, `pow5_inj`;
- `collision_shared`: a collision sharing any entry is trivial;
- `collision_interleave`: if b < d then c < a, so a nontrivial collision has c < a < b < d;
- `pow5_mod_11`: x⁵ mod 11 ∈ {0, 1, 10};
- `pow5_mod_25`: x⁵ mod 25 depends only on x mod 5;
- `sum_pow5_mod_11`;
- `injOn_below_15`: a kernel `decide` on the nodup of 105 sums.

Its compile hit the timeout (a first run at bound 40 hit the 10-minute limit), so it is **UNVERIFIED Lean source**.

**Where it is stuck.** A refutation needs an explicit a⁵ + b⁵ = c⁵ + d⁵, and none is known. A proof means showing that x⁵ + y⁵ = z⁵ + w⁵ has no nontrivial solutions in ℕ, which is open (Lander–Parkin–Selfridge would imply it).

**Literature (item).** The item quotes [Erdős Problems #324](https://www.erdosproblems.com/324) as "Probably f(x)=x^5 should work". That site returns 403 to automated fetches (§364), so the quote is **UNVERIFIED**. The open status rests on the pinned FC tag `category research open` (checked in this run). The item also cites Ruzsa (x⁵ + ⌊cx⁴⌋ is Sidon) and Dubickas–Novikas (cubics fail). Both are UNVERIFIED, and no URLs were given.

---

## Erdős #723, eq-12

**Status: UNSOLVED.** Target ([Challenge](https://raw.githubusercontent.com/identity-md-launches/goal-3467-objective-settle-least-one/3d3f3a09d60c67992738413746463076008eb894/catalog/targets/erdos723-erdos-723-variants-eq-12/formalized/Challenge.lean), sha256 `61851a3c…`): `True ↔` a finite projective plane of order 12 exists. The existence direction needs such a plane, and the refutation needs nonexistence of every such plane.

**Lemma sources.** This write-up run fetched the four files from `compiled_lemmas[].source_utf8` of the [prior attack artifact](https://api.imd.fun/artifacts/d7449350c296802dc4b0cb65c6f98d2ed4ea32bc363fe40aaca4c1404d5f2a8c). Each matched the artifact's own byte count and sha256 (all import Mathlib, `FormalConjectures.ErdosProblems.«723»` and `TaskSupport`):

| File | Bytes | sha256 | Declarations (prior job, axioms `[propext, Classical.choice, Quot.sound]`) |
|---|---|---|---|
| `IncidenceBridge.lean` | 2978 | `854f019b…43cbcc` | `formalized_shape`, `counterexample_shape`, `planeOfIncidence`, `order_twelve_of_line_card`, `order_twelve_sizes` |
| `GridBridge.lean` | 6287 | `6873b0e0…116d54a` | `Grid.toPlane`, `Grid.toPlane_order`, `Grid.order_three_control` |
| `McKayObstruction.lean` | 4516 | `bc52c2a5…9fdf93` | `McKay.no_common_transversal_through_pair`, `search_complete`, `pair_compatible`, `no_transversal_through_pair` |
| `ProductObstruction.lean` | 2202 | `09ae85e6…bdce129f` | `no_product_transversal` |

The prior job's per-file `print_axioms_output` and its build-log excerpt are delivered as `723/prior-axioms-and-build.txt`. The prior job ran x86_64 Lean 4.35.0-rc2, tree `0766488c`, Mathlib `06535612`, and `lake build +FormalConjectures.ErdosProblems.«723»` ending at `[9198/9198]`.

**Rebuild status.** The item run's replay failed with `Exec format error`: it had downloaded the x86_64 Lean archive on an aarch64 machine. This write-up run used the aarch64 build, built `FormalConjectures.ErdosProblems.«723»` (exit 0), and ran `lake env lean` on the four files. All four hit the 520 s timeout together with the control Challenge stubs. **The compile and axioms in this job are UNVERIFIED**, and the evidence is historical (prior job).

**Extension.** The item proposed `ProductMultiplicity.lean`: bijective column/first/second maps on `Fin 3 × Fin m` with the stated relations force `3 ∣ m`. The source was not passed on in the item result, so it is **not delivered** and remains UNVERIFIED. The item's Python `check_seed.py` and `seed-check.json` (384 common transversals, 48 unjoinable pairs including (0, 61)) were not passed on either. Those counts match the prior report according to the item and are **UNVERIFIED** here.

**Where it is stuck.** For existence, one must give all 13 orthogonal coordinate directions on 144 cells (via `GridBridge`), or raw incidence data. The fixed McKay seed cannot be completed, and the product seed is obstructed under its projection hypotheses. For nonexistence, the argument must cover every order-12 plane, including planes without these seeds and with trivial collineation group. No reduction to the tested seeds exists.

**Literature.**

- The open status rests on the [pinned base FC file](https://raw.githubusercontent.com/google-deepmind/formal-conjectures/7d1a8c9912747679d0093f6d1216420c33ee5ffa/FormalConjectures/ErdosProblems/723.lean), which tags `erdos_723.variants.eq_12` `category research open`.
- The item's claim that [erdosproblems.com/723](https://www.erdosproblems.com/723) was "fetched in this run" is the source that did not re-verify. That site returns HTTP 403 to automated fetches, so the claim is **UNVERIFIED**.
- Akiyama–Suetake–Tanaka ([Crossref record](https://api.crossref.org/works/10.1002/jcd.21869)): no collineation group of order 4. This is a symmetry restriction only, and the full text is UNVERIFIED.

---

## Deliverable bundle (requester only)

All Lean sources and logs named above are in a gzip tar archive, base64 encoded below:

- bundle sha256 `8cd91f6de334ff0016ca21bc7a02032afffac8a69959e3ca6a21172853d2d145`;
- 21,078 bytes, holding 25 files plus `SHA256SUMS`;
- `this-run/` holds the official Challenge files and TaskSupport as fetched, plus the tail of every compile log from this run.

To unpack and check it:

```sh
awk '/^```base64$/{p=1;next} p && /^```$/{exit} p{print}' report.md | base64 -d > bundle.tgz
sha256sum bundle.tgz && mkdir b && tar -xzf bundle.tgz -C b && cd b && sha256sum -c SHA256SUMS
```

To rebuild, start from the FC base `7d1a8c99` with the audit patch applied (`git write-tree` = `0766488c…`). Run `lake exe cache get`, copy in `TaskSupport.lean` and compile it to `.lake/build/lib/lean/TaskSupport.olean`, then run `lake env lean <file>.lean` per file. #647 additionally needs `Early.lean`, `Lemmas.lean` and `WitnessReview.lean` from the three #647 artifacts, extracted as the item result describes. #366 needs `PriorMordell.lean` from the Mordell artifact. Build the #647 modules separately from the #366 modules, because they share the `Bounty` namespace.

`SHA256SUMS`:

```text
425b927c301bff5e11173a24aa2ddf16e8612bdede19ca3cc16e35e5eabecf6e  ./324/Erdos324Partial.lean
ba981eb9d7aed73398279b7c4f57e17cc407e98c081c75e56f34156e9032c97f  ./364/Erdos364Official.lean
c076ca85917e8060f7e876aa29d880b79d7d86b96c7d603d366fc0d581304d5c  ./364/Erdos364Partial.lean
5ee10b1edb833829c1cb47968c558a3dace049bdf94114a700a9325cb5bbb4c2  ./366/Partial366.lean
66c91cbc3f81d8888d018dcaad52feaa9169f9cffe33ed1fc6654f1d337f058d  ./647/Extension.lean
4da1a2984ec525b5da8b5d3d4e3d17919649fe965aae36f9a16c2e02ab531b09  ./647/final-build.condensed.log
6873b0e04468dd90ae66825206e3104ded7d0f53ac2873f918f29d8c4116d54a  ./723/GridBridge.lean
854f019b1804a259b5af12178b04053ecbaa07f77e5f0398e0b74ecf9443cbcc  ./723/IncidenceBridge.lean
bc52c2a5b7ebc55184ae7fffef8b71ddbe8831b68463d0ac816ffe37239fdf93  ./723/McKayObstruction.lean
09ae85e6e0e132185bc6f2324692a21d36a027c4df0cd168e913a7b1bdce129f  ./723/ProductObstruction.lean
a29e883ac1c12c5098e8765fb61a6371626f89c08c39ce2e5ea82d59735d531f  ./723/prior-axioms-and-build.txt
a1b53f2d4cef5450035d929140f0db633dd961204fe0bde424134a27b053188c  ./SHA256SUMS
8920db22050198de5e0aa52e9f86acaba556c325a44a2e0659c042a57de1dc98  ./this-run/Challenge324.log
76d344c08c1b71b608169122a49489e852e21ce2b66a7ac6282323732e0493f0  ./this-run/Challenge364.log
0ab3124f0efd05122ac497d3caf5dab4a17049b7d9dbf90df380cce9b3b23fd5  ./this-run/Challenge723.log
4478e6183293c9189f3cf5bfe1bb52d6817fe4ead0582fddd2d96ff485a8ab4a  ./this-run/Erdos324Partial.log
4ce742ab4e48426507c5177abfa9e6f0d1f0765c291871cb47a9504b8ea22bae  ./this-run/Erdos364Official.log
ba7e8e277a38f6b1f5245ad75df3e5e270801e78bc6563dc765e6cf4bf70df7f  ./this-run/GridBridge.log
1ce63acbbdc1149674cfb9457da08065647421e6ff418021b999aa22bdb6b7c4  ./this-run/IncidenceBridge.log
281db4bc888c53f6945655ee384970520688fdd74daf0ed01214dee370772aac  ./this-run/McKayObstruction.log
8edefe928c078163a895585e4307b2c2861890f6111decbea7a6c8afef87854c  ./this-run/ProductObstruction.log
58a80a223dbd7383d92eb2a57b1ec207c0991131a1a1bf24585a4452777c257e  ./this-run/TaskSupport.lean
6e1d6cdc1d601aef3c91c4a52dc918c5b4502bf04dff2985eb07940fbc81b232  ./this-run/erdos324-erdos-324-variants-quintic.Challenge.lean
0608e0e2a751e8156341b50347548b168730106e6f4230abdf041bc49cf52219  ./this-run/erdos364-erdos-364.Challenge.lean
61851a3cc2d776cd91d4fcd75686ed7b8538ab30832356be34dca776964a7c0b  ./this-run/erdos723-erdos-723-variants-eq-12.Challenge.lean
b0adb4ac6a0fd3437b636f50323bdd797bf8a1ce5eb21cf19d7292f621b41ed4  ./this-run/fc-modules-build.log
```

```base64
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
```
