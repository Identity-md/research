# Conjectures.io proof search

**No target was solved.** Zero of 278 targets yielded a proof or refutation. No solution Main.lean, build log, axiom output or successful-attempt chat exists. Five lemmas about quintic collisions passed a fresh rebuild. The official #324 scaffold still prints `[propext, sorryAx]` for `Bounty.target`. No contributor submitted to the subnet, created an account, bought credits or spent TAO for this work. [Replay][replay]

The 2026-11-26 snapshot (09:19:45–09:19:56 UTC) matched 556 modes to 278 submission-open targets among 321 catalog records. Terms v13 require exact statement identity, clean kernel dependencies and the original producing chats. An established prior solution disqualifies even a first formalization. Actual intake and the meaning of a test-only site notice are **UNVERIFIED**. [Rules](https://conjectures.io/how-it-works) · [Submission terms](https://conjectures.io/submission-terms) · [Inventory][inv]

The code wave reached `3d3f3a09d60c67992738413746463076008eb894` in **identity-md-launches/goal-3467-objective-settle-least-one**. Exact inputs are in `catalog/targets/<slug>/{formalized,counterexample}/Challenge.lean`. This revision matched both digests and each expanded type to `metadata.json`. The trunk contains the inventory and harness. Proof work is in the result records. [Repository at commit](https://github.com/identity-md-launches/goal-3467-objective-settle-least-one/tree/3d3f3a09d60c67992738413746463076008eb894) · [Inventory][inv]

## Ten priority leads

All search windows below are ordinary program results, **UNVERIFIED** as Lean coverage certificates. These ten include all seven original a/b leads, two finite decision problems and #49, where one chain certifies a refutation. The workers returned 19 records on 14 targets, including triage-only #982. Only #366, #617 and #647 had repeat worker assignments. Four leads received their first bounded tests during this revision. The new checks share one author. The ten-target multi-agent requirement remains unmet.

|Target|Work performed and strongest reusable result|What remains|
|---|---|---|
|#647|Sieve n=360360j>24 by τ(n−h)≤h+2 with a divisor cap. Two 10⁹-multiplier windows left 73+22 survivors. All 95 have kernel-checked violating shifts among 108 declarations.|Full coverage is **UNVERIFIED** in Lean. Other windows remain open. [Early work][root1] · [after-e647][tri]|
|#617|On 170 vertices, the frozen affine core failed to extend to a balanced 13-coloring. Unrestricted search returned UNKNOWN. Six certificate lemmas and ten stability lemmas include `at_most_one_pure_color`.|Mixed color classes survive the counting inequalities. Forum certificates at fixed r leave the universal statement open. [I7][tri] · [Stability][stability]|
|#366|Squarefull n **before** cubefull n+1. No forward hit through 10¹⁰. Valuations eliminated the last 59 Pell candidates at B,D≤300. Of 3,797 Mordell parameter pairs, 339 remained unsettled. Lean checked `no_witness_le_300` and `target_iff_mordell`.|Reverse pairs pass the controls. No bound covers all curves or heights. Conditional abc finiteness alone cannot answer existence. [Pell, continuation and Mordell records][root1]|
|#49 primes-maximal|The strict φ-LIS matched π(N) for 2≤N≤3,000,000. Reconstructing the final chain gave **216,811 prime indices and five composites** (6,8,9,25,121), length 216,816. The original `nonprime_indices` counted primes. Three Lean facts concern φ(1), φ(2) and φ(p).|The strict-LIS upper bound is required at every endpoint. An asymptotic equality allows pointwise excess. [Scan and prior log][e49]|
|#723 eq-12|Order 12 gives 157 points and 157 lines. Enumerating binary incidence matrices and checking plane axioms terminates. Sixteen Lean helpers bridge incidence tables and grids. The five McKay squares and the product seed lack a common transversal. A two-square prefix leaves 48 point pairs uncovered.|These exclusions are seed-specific. Exhausting 2^(157²) labeled matrices without major reductions is impractical. [after-e723][tri]|
|Math30 source16|The 47 slots for 4×4 multiplication over ℂ give 2,256 variables and 4,096 polynomial identities over ℤ. A Gröbner basis over ℚ decides unit-ideal membership, equivalent by field extension and Nullstellensatz to no complex solution. The worker verified the rational 48-term algorithm, tried all 48 deletions and proportional merges, and tested a naive mod-4 lift of an F₂ seed.|No 47-term solution, unit-ideal certificate or Lean build. The full elimination was not run. Exact finite decision can be prohibitively expensive. [after-m16][tri]|
|#373 Surányi|Factorial lookup and falling products agree through n=450 on a single triple, (10,7,6). For a=n−2, cancellation gives b!=n(n−1). Exact roots of 4b!+1 excluded every 2≤b≤4,000 on this slice, including 1,921 with b!>10³⁰⁰⁰(10³⁰⁰⁰+1).|Habsieger excludes a huge initial range. A general proof must also cover a<n−2. [Habsieger](https://arxiv.org/abs/1903.08370)|
|#386 two|For a consecutive-prime product P, test whether 8P+1 is square. Enumerating intervals and factoring triangular numbers agreed through n=10⁶. Hits were 4,6,15,21,715. A multi-prime interval starting above 10⁶ exceeds the cap, and a triangular number at n≥4 is composite.|The target fixes k=2 and requires infinitely many n. Martins's restrictions and conditional finiteness do not settle either direction. [Problem and examples](https://www.erdosproblems.com/386) · [Claim](https://www.erdosproblems.com/forum/thread/386/proof-claims)|
|#398|Rolling factorials and integer square roots through n=2,000 returned 4,5,7. Separately, all 100,000 n from 1,000,000,001 through 1,000,100,000 had a nonsquare residue n!+1 modulo a prime q=n+i, i≤1,100. Wilson gives n!≡(−1)^i/((i−1)!) mod q.|Naciri's 7-free restriction on a neighbor does not cover all roots. A modular exclusion covers only its finite window. [Source](https://www.erdosproblems.com/398)|
|#672|For coprime 1≤n,d≤250, factor the AP terms. A gcd >1 of their accumulated prime exponents detects every perfect power. No hit in 418,517 tests at 4≤k≤14, or **1,483,833** at 35≤k≤73, beyond the k≤34 theorem. A prime with exponent one rules out every power exponent ≥2.|No bound on starts, steps or lengths. Negative entries in a published example violate positivity. [Győry–Hajdu–Pintér and later results](https://www.erdosproblems.com/672)|

## Other landed work

- **#324 quintic.** At b−d=1, 10,184,165 exact tests for selected a,b≤30 million found no equal sums. Five `Quintic324` lemmas reduce any refutation to a primitive nested collision and constrain residues mod 11. The search leaves other differences and unbounded heights open. [Original Lean source][e324] · [Fresh replay][replay]
- **#677.** Enumerated runs of divisors of a lower block lcm and screened disjoint blocks by prime-power fingerprints. No collision. Nineteen declarations include `fixed_lower_finite_check` and exclusion of k≤2. There is no joint bound on starts and length. [I1][tri]
- **#686 twenty-five.** Bracketed the upper block in Pₖ(m)=25Pₖ(n). The worker screened 88,202,323 (k,n) pairs with no witness. Seventeen declarations include `length_bound` and exclusions at k=2,4,6. Starts and k remain unbounded. [I2][tri]
- **#1082(i).** Exact cyclotomic counts met the half-cardinality threshold for the admissible Harborth samples and deletions. Seven lemmas include `harborth_squared_codes`. The sharp bound for all sets with no three collinear remains open. [I5][tri]
- **#373 maximal.** Used valuations of the factors of n!/(n−2)! seeking solutions above 16 with several factorials. No candidate or compiled lemma. The reported exp(80) exclusion for this variant is **UNVERIFIED**. [I6][tri]
- **#982.** Triage only. No search or compiled lemma. A single convex vertex must see floor(n/2) distances. Published linear lower bounds and the more recent claimed improvement have smaller coefficient. [I8][tri]
- **#364.** Direct search through 10⁸ found ten consecutive powerful pairs and zero triples. Pell search tested 3,064 neighbors of 1,532 pairs with 79 unresolved. Fifteen helpers include `triple_mod_thirtysix`. No cutoff on the kernels. [after-e364][tri]
- **#458.** Near 10²⁵ and 10³⁶, 365,069 and 120,785 higher powers respectively gave no apparent hit. Endpoints were probable primes. The sparse square-plus-cube argument leaves two squares or three powers in a gap open. The original seven source declarations were missing. Reconstructed controls and bounds are included below. [Original report][e458]

## Rebuilding the partial proofs

Use Lean v4.35.0-rc2 and the manifest (Mathlib `065356127b1dc0016f66b7283ce0ce2c4055aa55`). To reconstruct audited Formal Conjectures `6adcbe13652f4e7c69ad02a783465ae2a99d5cb3`, check out upstream `7d1a8c9912747679d0093f6d1216420c33ee5ffa` and apply the [tasks audit patch][patch] (SHA-256 `352280407fbbe83e636aa07a5c090aab15c6353c7cd77c0491284cd40df51275`). The trunk harness tries to fetch the derived commit directly. The replay gives commit reconstruction, package pins, commands and logs. [Replay][replay]

For #324, save the validator's [TaskSupport.lean][support], the trunk's counterexample Challenge and I4's UTF-8 `files["Lemmas.lean"]` at the **audited Lake package root**. Save the replay JSON as replay.json. Register the three modules before building.

```sh
cat >> lakefile.toml <<'TOML'

[[lean_lib]]
name = "TaskSupport"
[[lean_lib]]
name = "Challenge"
[[lean_lib]]
name = "Lemmas"
TOML
lake exe cache get
lake build FormalConjectures/ErdosProblems/324.lean TaskSupport Lemmas Challenge
for k in axiom_probe_source probe_source; do
  jq -r --arg k "$k" '.commands[$k]' replay.json > "$k.lean"
  lake env lean "$k.lean"
done
```

The two residue lemmas print only propext. The nested, scaling and primitive reductions print propext, Classical.choice and Quot.sound. All six original steps exited 0. This revision rebuilt the three modules and reproduced both axiom audits. Distinct author/verifier identities are **UNVERIFIED**. Episode 5 separately replayed 18 files within the axiom allowlist, substituting Challenge's three imports for #49's `import Challenge`. Extract source from b03's literal `compiled_lemmas`/partial `main_lean`, b06/b07/b08's `files["Lemmas.lean"]`, after-e723's `source_utf8`, and the base64/XZ file entries in after-e364 and after-e647. b05-e366 contains the search continuation only. [First merge][root1] · [Second merge][root2] · [Per-target records][tri]

In the same project, build `FormalConjectures/ErdosProblems/458.lean` and TaskSupport. Save the next block as `Partial.lean` and run `lake env lean Partial.lean`. These are reconstructed proofs of the seven reported controls and inequalities. The cluster inequality follows by taking sixth powers and comparing 32p⁵ with p⁶. The missing original text prevents a byte comparison.

```lean
import Mathlib
import FormalConjectures.ErdosProblems.«458»
import TaskSupport

namespace Bounty
open Erdos458

theorem control_lcm_seven : lcm_upto 7 = 420 := by decide
theorem control_lcm_ten : lcm_upto 10 = 2520 := by decide
theorem control_ratio_7_11 : lcm_upto 10 / lcm_upto 7 = 6 := by
  rw [control_lcm_ten, control_lcm_seven]
theorem control_gap_7_11 : lcm_upto 10 < 7 * lcm_upto 7 := by
  rw [control_lcm_ten, control_lcm_seven]
  decide
theorem control_k_three :
    lcm_upto (Nat.nth Prime (3 + 1) - 1) <
      Nat.nth Prime 3 * lcm_upto (Nat.nth Prime 3) := by
  have h : (Prime : ℕ → Prop) = Nat.Prime := by
    funext n
    exact propext Nat.prime_iff.symm
  rw [h, Nat.nth_prime_three_eq_seven, Nat.nth_prime_four_eq_eleven]
  exact control_gap_7_11

theorem sparse_product_bound {p a b : ℕ} (hp : 32 < p)
    (ha : a^2 ≤ 2*p) (hb : b^3 ≤ 2*p) : a*b < p := by
  have h : (a*b)^6 < p^6 := calc
    (a*b)^6 = (a^2)^3 * (b^3)^2 := by ring
    _ ≤ (2*p)^3 * (2*p)^2 := by gcongr
    _ = 32*p^5 := by ring
    _ < p*p^5 := Nat.mul_lt_mul_of_pos_right hp (pow_pos (by omega) 5)
    _ = p^6 := by ring
  by_contra! hn
  exact (not_lt_of_ge (Nat.pow_le_pow_left hn 6)) h

theorem sparse_gap_shape {p q a b : ℕ} (hp : 32 < p) (hq : q < 2*p)
    (ha : a^2 < q) (hb : b^3 < q) : a*b < p :=
  sparse_product_bound hp (by omega) (by omega)
end Bounty
#print axioms Bounty.control_lcm_seven
#print axioms Bounty.control_lcm_ten
#print axioms Bounty.control_ratio_7_11
#print axioms Bounty.control_gap_7_11
#print axioms Bounty.control_k_three
#print axioms Bounty.sparse_product_bound
#print axioms Bounty.sparse_gap_shape
```

Both revision files exited 0. All seven #458 declarations printed [propext, Classical.choice, Quot.sound]. Save the next block as `Leads.lean` and run `lake env lean Leads.lean`. The Surányi cancellation uses propext alone. The other three use the same three axioms as #458. These establish reductions used by the searches.

```lean
module
public import Mathlib

public section

namespace Leads

theorem suranyi_two_step {a b : ℕ}
    (h : (a+2).factorial = a.factorial * b.factorial) :
    b.factorial = (a+1)*(a+2) := by
  rw [Nat.factorial_succ, Nat.factorial_succ] at h
  exact Nat.eq_of_mul_eq_mul_left (Nat.factorial_pos a)
    (h.symm.trans (by ring))

theorem triangular_discriminant (n : ℕ) :
    8 * n.choose 2 + 1 = (2*n - 1)^2 ∨ n = 0 := by
  cases n with
  | zero => exact Or.inr rfl
  | succ n =>
    left
    have h : 2 * (n+1).choose 2 = n*(n+1) := by
      induction n with
      | zero => decide
      | succ n ih =>
        rw [Nat.choose_succ_succ (n+1) 1, Nat.choose_one_right]
        nlinarith
    have a : 2*(n+1)-1 = 2*n+1 := by omega
    rw [a]
    nlinarith

theorem brocard_neighbors {m n : ℕ} :
    n.factorial + 1 = (m+1)^2 ↔ n.factorial = m*(m+2) := by
  constructor <;> intro h <;> nlinarith

theorem simple_prime_blocks_power {p v q l : ℕ}
    (hp : p.Prime) (hv : p ∣ v) (hs : ¬ p^2 ∣ v) (hl : 2 ≤ l) :
    v ≠ q^l := by
  rintro rfl
  have hq := hp.dvd_of_dvd_pow hv
  exact hs ((pow_dvd_pow_of_dvd hq 2).trans (pow_dvd_pow q hl))

end Leads
#print axioms Leads.suranyi_two_step
#print axioms Leads.triangular_discriminant
#print axioms Leads.brocard_neighbors
#print axioms Leads.simple_prime_blocks_power
```

## Inventory and individual triage

Each row gives the exact catalog slug. For its full Lean type look up its slug in the [pinned inventory][inv]. The source for an Erdős slug is its **own number** at `https://www.erdosproblems.com/N`; a key such as GHP09 identifies a reference on that page. E followed by a number names a problem page directly. W means the slug's original Wikipedia problem URL in the inventory. An arXiv number, including a bare YYMM.NNNNN, resolves at `arxiv.org/abs/<id>`. Attempts/bounty codes give the observed attempt count followed by the USD quote at 09:19 UTC: A = $2,957.83 (256 rows), B = $2,574.51 (18), C = $2,196.46 (3), D = $2,218.04 (1). Five rows had one attempt, the other 273 zero.

**a** denotes a finite decision or a concrete one-sided search, **b** a specialized formulation, **c** a short identified gap, **d** a hard target with no promising bounded route. Classes are primary routes, and a finite witness may exist for a d row. Revised counts are 30 a, 1 b, 0 c and 247 d. Chance is a subjective percentage for reaching an eligible complete theorem in one focused session. ≈0 is rounded. For the 194 previously unestimated rows, the revision uses bounds below 0.1% for a concrete unresolved reduction, below 0.01% for a major missing theorem or unbounded classification, and below 0.001% for searches already excluded to an extreme frontier. The other 84 estimates come from the workers with heterogeneous horizons. None is calibrated.

The original run used 45 of 50 items. Its specialist reviews cover rows 20,21,39,45,78,83,86,92,103,105,106,127,134,142,153,154,158,163,164,168,171,193,228,266. The remaining 254 received slice screens then individual editorial review here. The revision compared all 278 pinned types with their problem records, read the numbered source pages, discussions and claims, and queried 2023–2026 arXiv title/abstract metadata via DataCite by problem number or subject. Some paper comparisons relied on abstracts or bibliographic records. Number searches miss unnumbered papers and can return unrelated hits. For every row, the reviewed sources yielded no established proof with matching hypotheses. **Wider novelty is UNVERIFIED.** The report records relevant special cases and named claims where they change the route. One distinct reviewer per slug was beyond the historical allocation. I1–I8 and after-* resolve via `reference_legend`. For original plans and sources download the [triage record][tri] and run `jq -r .data result.json | base64 -d | xz -dc > triage.tsv` (206,168 bytes, SHA-256 `af8f724cf8e2710870daaba425cce0c9d8e3a1f9722c4069a0a8e2504e518a66`).

|#|Slug|Source|Class|Chance %|Attempts / bounty|Statement, route and obstruction|
|--:|---|---|:-:|--:|:-:|---|
|0|artinprimitiverootsconjecture-artin-primitive-roots-parts-i|W/arXiv 1112.4816|d|<1|0A|Sieve failures of primitive-root generation. Hooley's positive-density argument needs GRH for its field-degree tail.|
|1|borsuk-borsuk-conjecture-four|W/arXiv 2608.12561|d|<1|0A|Seek a 4D diameter graph needing six colors. Projection of a high-dimensional example loses diameter edges.|
|2|brocard-brocard-conjecture|W/arXiv 2307.08725|d|<0.5|0A|Count primes between consecutive prime squares. Four must occur even across the narrowest spacings.|
|3|bunyakovsky-bunyakovsky-conjecture|W|d|<0.5|0A|Sieve values after removing fixed divisors. Even X²+1 requires a prime-producing quadratic sieve.|
|4|carmichaeltotient-charmichaeltotient|W/arXiv 2610.34808|d|<0.5|0A|Invert φ(m) by branching on p−1 dividing the target value. The 2p^s fiber classification leaves general m.|
|5|classnumberproblem-class-number-problem|W|d|<0.5|0A|Test principality in small-regulator quadratic fields. For class number one the family must be infinite.|
|6|dickson-dickson-conjecture|W/arXiv 0906.3850|d|<0.5|0A|Sieve admissible linear tuples. Even simultaneous primality of X and X+2 remains open.|
|7|erdos10-erdos-10|E10 Ga75|d|<1|0A|Cover Gallagher's exceptional integers by extra binary summands. The number added must be uniform.|
|8|erdos100-erdos-100|E100 GuKa15|d|<1|0A|Count unit-separated *distance values*. Guth–Katz gives diameter ≫n/log n. Need a linear bound.|
|9|erdos1003-erdos-1003|E1003 EPS87|d|<0.5|1A|Match factorizations of n,n+1 giving equal φ. EPS's upper count supplies no infinite family.|
|10|erdos102-erdos-102|E102 Er92e|d|<1|0A|Bound four-rich lines assuming bounded collinearity. Even forcing five collinear points is open.|
|11|erdos103-erdos-103|E103 Er94b|d|<1|0A|Deform an optimal separated packing at its boundary. Need unboundedly many incongruent optima at each large n.|
|12|erdos104-erdos-104|E104 HaMe86|d|<1|0A|Discount shared pairs among triple-rich unit circles. Pair counting gives O(n²), short of little-o.|
|13|erdos1049-erdos-1049|E1049 Er48|d|<1|1A|Clear denominators for t=a/b in the Lambert series. Erdős's integer-base proof loses control of b-powers.|
|14|erdos1056-erdos-1056|E1056 Ma83|d|<1|0A|Find k+1 equal factorial residues mod p and divide neighbors. Makowski's k=3 example has fixed length.|
|15|erdos1060-erdos-1060-parts-ii|E1060 Gu04|d|<1|0A|Sieve k ∣ n by σ(k)=n/k. The divisor bound on fiber size exceeds the required polylogarithm.|
|16|erdos107-erdos-107|E107 Su17|d|<0.5|0A|Extend cups and caps in finite order types. Suk's exponent leaves the exact 2^(n−2)+1 upper bound.|
|17|erdos1072-erdos-1072-parts-i|E1072 HaSu02|d|<1|0A|Fix the Wilson hit at p−1 and sieve all earlier hits of −1. Need infinitely many surviving primes.|
|18|erdos1072-erdos-1072-parts-ii|E1072 HaSu02|d|<1|0A|Estimate primes whose first hit exceeds εp. Density zero at every ε would yield a density-one diagonal.|
|19|erdos1073-erdos-1073|E1073 HaSu02|d|<1|0A|For composite u ∣ n!+1, minFac(u)>n. Count such u by n and factor size to seek x^o(1).|
|20|erdos1082-erdos-1082-parts-i|E1082 Fi02|a|0.5|0A|Count distinct squared distances with no collinear triple. Harborth controls attain half, while the general Szemerédi argument yields a third.|
|21|erdos1085-erdos-1085-variants-upper-d3|E1085 Sw09|d|≈0|0A|Adapt Zahl's point–sphere incidences to control rich surfaces. The exponent 295/197+ε still exceeds the conjectured 4/3 with log-log factor.|
|22|erdos1094-erdos-1094|E1094 Se77|d|<1|0A|Split exceptional binomials at n=k². A smallest-factor threshold for fixed k must be uniformized.|
|23|erdos1095-erdos-1095-variants-log-istheta|E1095 SSW20|d|<1|0A|Bound the threshold for small binomial factors from both sides. The exponential upper bound loses log k.|
|24|erdos1095-erdos-1095-variants-lower-conjecture|E1095 SSW20|d|<1|0A|Construct carry patterns avoiding small binomial factors up to exp(c k/log k) at every large k.|
|25|erdos11-erdos-11|E11 He24b|d|<0.5|0A|Sieve n−2^j against square divisors. Hercher covers 2^50. A uniform argument must survive the tail.|
|26|erdos1101-erdos-1101-parts-i|E1101 Er81h|d|<1|0A|Try u_i=p_i². Polynomial growth and summable reciprocals hold. The sharp gap bound remains.|
|27|erdos1106-erdos-1106-parts-ii|E1106 On00|d|<1|0A|Bound the first partition number divisible by each prime. Ono's eventual occurrence gives no >n count by n.|
|28|erdos1107-erdos-1107|E1107 He88|d|<1|0A|Extend Heath-Brown's squarefull circle method to r+1 r-full terms. Need minor-arc control for r≥3.|
|29|erdos1108-erdos-1108-parts-i|E1108 BrEr91|d|<1|0A|Isolate the largest factorial in a subset sum and sieve kth powers. Even squares of form n!+1 remain.|
|30|erdos1113-erdos-1113-variants-filaseta-finch-kozek|E1113 FFK08|d|<1|0A|Use orders of 2 at prime factors of k2^n+1. For nonpowers k, finiteness of a covering subfamily is open.|
|31|erdos1135-erdos-1135|E1135 La10|d|≈0|0A|Seek strict descent in every positive Collatz orbit. Almost-everywhere descent allows an exception.|
|32|erdos1137-erdos-1137|E1137 Va99|d|<1|0A|Bound products of consecutive prime gaps relative to the squared record. Separate bounds miss adjacency.|
|33|erdos1142-erdos-1142|E1142 MiWe69|d|<1|0A|Cover n by composite offsets n−2^k. Seven survive through 2^44. Vaughan's upper bound allows infinitude.|
|34|erdos1175-erdos-1175|E1175 Va99|d|<1|0A|Thin a graph to a triangle-free subgraph of chromatic κ. Shelah's fixed-cardinal case leaves ∃μ.|
|35|erdos1192-erdos-1192|E1192 Ru90|d|1|0A|Repair missing sums in the Erdős–Rényi construction. Ruzsa handles r=2. For r>2 energy must stay O(x).|
|36|erdos120-erdos-120|E120 JLM24|d|<0.5|0A|Reduce to a sequence decreasing to zero. Delete neighborhoods of its affine copies, retaining positive measure.|
|37|erdos1203-erdos-1203|E1203 Er80|d|<1|0A|Force many primes into n+k at low cost log k/log log k. The normalized lower bound near one must diverge.|
|38|erdos1209-erdos-1209-parts-iii-d|[E1209](https://www.erdosproblems.com/forum/thread/1209) Er80|d|<0.5|0A|Sieve squares along n+2^(2^k) for one fixed n. Excluding an always-prime translate uses a repeated divisor and leaves infinite squarefreeness open.|
|39|erdos124-erdos124-ne-zero|E124 Me04|d|1|0A|Extend positive-cutoff power-sum interval certificates. BEGL handles some bases. Uniform boundary cases remain.|
|40|erdos126-erdos-126-variants-islittleo|E126 ErTu34|d|<1|0A|Choose n numbers whose pair sums use o(n/log n) primes. The published √n lower bound settles a different limit.|
|41|erdos128-erdos-128|E128 Ra22|a|1|0A|Perturb a triangle-free C₅ blowup to increase every half-set minimum. The unperturbed example is tight.|
|42|erdos137-erdos-137-variants-multiple-powerful-factors|E137 ErGr80|d|<1|0A|Force k exponent-one primes in each long consecutive product. Excluding perfect powers gives less.|
|43|erdos141-erdos-141-variants-eleven|E141 GrTa08|a|<1|0A|Sieve admissible eleven-term APs, checking primality and every intervening integer. Green–Tao supplies no control on intervening primes.|
|44|erdos145-erdos-145|E145 Ch23c|d|<1|0A|Integrate the tail of squarefree gaps against t^(α−1). Chan reaches α=3.75. Higher moments need sharper tails.|
|45|erdos151-erdos-151|E151 EGT92|d|1|0B|Use an independent set to save vertices of a clique transversal. Small-order checks leave the sharp Ramsey term.|
|46|erdos153-erdos-153|E153 ESS94|d|<1|0A|Lower-bound squared gaps of A+A by Sidon energy. Cauchy–Schwarz gives a constant. Need divergence.|
|47|erdos155-erdos-155|E155 ESS94|d|<1|0A|Delete new points from a largest Sidon set on [1,N+k]. Eventually all but one loss must be recoverable.|
|48|erdos158-erdos-158|E158 ESS94|d|<1|0A|Extend the dyadic Sidon count to B₂[2]. Doubled representations obstruct the square-root zero-liminf bound.|
|49|erdos159-erdos-159|E159 EFRS78|d|<1|0B|Expand neighborhoods in C₄-free graphs. The Ramsey upper bound must save a power of n beyond a log saving.|
|50|erdos168-erdos-168-parts-ii|E168 GSW77|d|<1|0A|Use GSW's 3-smooth reciprocal series for the non-ternary density. Prevent rational cancellation in the tail.|
|51|erdos17-erdos-17|E17 El03|d|<0.5|1A|Cover all required even differences to construct cluster primes. Elsholtz's upper count permits finiteness.|
|52|erdos19-erdos-19|E19 HoTu90|d|<0.5|0A|Enumerate EFL configurations below the large-n coloring theorem. Need a usable cutoff and every small order.|
|53|erdos200-erdos-200|E200 ErGr79|d|<0.5|0A|Sieve a long prime AP by small primes. Primorial growth gives a log scale but no uniform little-o.|
|54|erdos208-erdos-208-variants-log-bound|E208 Gr98|d|<0.5|0A|Bound intervals covered by distinct prime squares. Moment bounds allow exceptional superlogarithmic gaps.|
|55|erdos212-erdos-212|E212 ABT20|d|<0.5|0A|Intersect rational-distance loci while adding points. Need an available point in every open disk.|
|56|erdos213-erdos-213|E213 GIP24|d|<0.01|0A|Extend integral-distance sets without three collinear or four concyclic. Kreisel–Kurz reaches seven.|
|57|erdos218-erdos-218-variants-ge|E218 Ba23|d|<0.01|0A|Count nonincreasing adjacent gaps. Banks's conditional spacings would give half. Need unconditional frequencies.|
|58|erdos218-erdos-218-variants-infinite-equal-prime-gap|E218 Ba23|d|<0.01|0A|Force three consecutive primes in AP infinitely often. An intervening prime spoils a Green–Tao progression.|
|59|erdos218-erdos-218-variants-le|E218 Ba23|d|<0.01|0A|Count nondecreasing gaps. Both ties and orientation bias matter. Infinite increases give no frequency.|
|60|erdos23-erdos-23|E23 BCL21|a|<0.01|0A|Sharpen triangle-free max-cut deletion from 1.064n² to n² on 5n vertices. C₅ blowups give equality.|
|61|erdos233-erdos-233|E233 Se43|d|<0.01|0A|Sum the squared-gap tail by dyadic size. PNT gives the lower N log² N scale. Large gaps govern the upper side.|
|62|erdos234-erdos-234|E234 Er55c|d|<0.1|0A|Prove tightness and a unique continuous gap/log n distribution. Limit points alone give no frequencies.|
|63|erdos236-erdos-236|E236 Er55c|d|<0.1|0A|Sieve the O(log n) shifts n−2^j together. A saving must hold even for exceptional odd n.|
|64|erdos238-erdos-238|E238 Er55c|d|<0.01|0A|Construct prime runs with gaps >c₂. Erdős's small-c₁ regime leaves arbitrary c₁ log x lengths.|
|65|erdos241-erdos-241-variants-generalization|[E241](https://www.erdosproblems.com/241) BoCh62|d|<0.1|0A|Compare B_r multisets using Bose–Chowla for the lower construction. For r=3 Green's upper constant already exceeds one.|
|66|erdos242-erdos-242-variants-schinzel-generalization|E242 ElPl20|d|<0.01|0A|Build congruence classes with three distinct unit fractions for a/n. Each a must cover all large n.|
|67|erdos243-erdos-243|E243 Du01|d|<0.01|0A|Clear rational tails to force Sylvester's recurrence. Duverney needs summable relative error, beyond convergence to zero.|
|68|erdos244-erdos-244|E244 Di25|d|<0.01|0A|Bound the second moment of p+floor(C^j). Ding's almost-every-base result leaves exceptional C>1.|
|69|erdos247-erdos-247|E247 ErGr80|d|<0.01|0A|Approximate by binary truncations. Unbounded n_k/k does not ensure the superpolynomial gaps in Erdős's theorem.|
|70|erdos249-erdos-249|E249 ErGr80|d|<0.01|0A|Expand φ by divisor convolution. Exclude eventual binary periodicity after all carries are included.|
|71|erdos25-erdos-25|E25 Er95|d|<0.01|0A|Truncate delayed residue exclusions to finite unions. Need uniform logarithmic-weight control of the tail.|
|72|erdos251-erdos-251|E251 Er58b|d|<0.01|0A|Seek carry-free blocks in Σp_n/2^n. The conditional normality claim needs uniform Hardy–Littlewood estimates.|
|73|erdos257-erdos-257|E257 TaTe25|d|<0.01|0A|Expand by A-divisors and seek binary gaps. Prime and prime-power cases leave arbitrary infinite A.|
|74|erdos263-erdos-263-parts-i|E263 KoTa24|d|<0.1|0A|Bound rational tails at critical squaring growth. The folklore criterion needs faster denominators.|
|75|erdos264-erdos-264-parts-ii|E264 KoTa24|d|<0.01|0A|Clear bounded offsets of factorial denominators. Offsets destroy nesting, and exponential examples grow too slowly.|
|76|erdos274-herzog-schonheim|E274 Su04|d|<0.01|0A|Pass to a finite quotient via subgroup cores. Sun's subnormal result leaves nonsubnormal coset partitions.|
|77|erdos28-erdos-28|E28 ErTu41|d|<0.01|0A|Estimate the convolution energy of an additive basis. Cofiniteness must force unbounded representation counts.|
|78|erdos287-erdos-287|E287 ErGr80|d|≈0|0A|Clear the unit sum and force two consecutive missing denominators. The needed prime pairs remain conditional.|
|79|erdos291-erdos-291-parts-i|E291 WuYa22|d|<0.01|0A|Use base-p leading digits to track harmonic numerator cancellation. Need infinite simultaneous avoidance.|
|80|erdos291-erdos-291-variants-shiu-heuristic-density-zero|E291 WuYa22|d|<0.1|0A|Combine leading-digit obstructions for many primes. One density saving must be amplified to density zero.|
|81|erdos295-erdos-295|E295 ErSt71b|d|<0.01|0B|Improve the harmonic bound on unit-fraction set size. Bounded deficit leaves divergence of the excess open.|
|82|erdos30-erdos-30|E30 CHO25|d|<0.01|0A|Transfer dense Sidon designs to nearby lengths. N^(1/4)-scale errors exceed N^ε for small ε.|
|83|erdos307-erdos-307|E307 Ba76|d|≈0|0A|Clear reciprocal sums and search disjoint supports. A witness needs ≥59 primes. Congruences alone allow solutions.|
|84|erdos311-erdos-311|E311 ErGr80|d|<0.01|0B|Bound subset-sum error via the lcm denominator. Match exponential rates at a limit strictly between 0 and 1.|
|85|erdos313-erdos-313-variants-primary-pseudoperfect-are-infinite|E313 ErGr80|d|<0.01|0A|Extend a primary pseudoperfect prime support, preserving its reciprocal identity. No iteration is known.|
|86|erdos317-erdos-317-variants-claim2|E317 ErGr80|d|≈0|0A|Clear signed harmonic sums to integers. Primes above n/2 rule out ±1 locally. Need an obstruction eventually.|
|87|erdos32-erdos-32|E32 2610.14127|d|<0.01|0A|Thin the O(log² N) complement while covering every large n. The new Ω(log N log log N) still permits little-o(log² N).|
|88|erdos322-erdos-322|E322 Ma36|d|<0.01|0B|Parameterize k-term equal-power sums with many representations. Mahler's cubes leave degrees k≥4.|
|89|erdos323-erdos-323-parts-i|E323 ErGr80|d|<0.01|0A|Bound collisions of k-term kth-power sums by mean values. Landau's squares leave higher-degree support.|
|90|erdos323-erdos-323-parts-ii|E323 ErGr80|d|<0.01|0A|Count collisions of m-term kth-power sums to retain order x^(m/k). Single powers do not handle all m<k.|
|91|erdos323-erdos-323-variants-k-gt-2|E323 ErGr80|d|<0.01|0A|Sieve values of k kth powers for zero density. Landau's two-square argument uses a special factorization.|
|92|erdos324-erdos-324-variants-quintic|E324 Ru01b|a|0.01|0A|Reduce fifth-power collisions to primitive nested pairs. Mod 11 prunes the search without bounding heights.|
|93|erdos325-erdos-325|E325 Wo15|d|<0.01|0A|Bound collisions of three kth powers. Wooley's cubic exponent falls short of positive density.|
|94|erdos340-erdos-340|E340 ErGr80|d|<0.01|0A|Count greedy Sidon exclusions by old differences. Cubic counting gives 1/3 in place of nearly 1/2.|
|95|erdos340-erdos-340-variants-sub-hasposdensity|E340 ErGr80|d|<0.1|0A|Track Mian–Chowla differences over whole intervals. Individual hits give neither convergence nor positive density.|
|96|erdos357-erdos-357-parts-i|E357 He86|d|<0.1|0A|Count distinct interval sums to bound sequence length. The reported linear saving still misses little-o.|
|97|erdos357-erdos-357-variants-infinite-set-density|E357 He86|d|<0.01|0A|Control every dense prefix of an increasing sequence with unique block sums. Zero lower density leaves spikes.|
|98|erdos357-erdos-357-variants-infinite-set-sum|E357 He86|d|<0.01|0A|Sum block contributions to the reciprocal series under distinct interval sums. Sparsity alone allows divergence.|
|99|erdos357-erdos-357-variants-monotone-parts-i|E357 He86|d|<0.1|0A|Singleton sums force distinct entries. Bound the increasing extremal length uniformly by o(n).|
|100|erdos359-erdos-359-parts-i|E359 Po77|d|<0.01|0A|Count skipped MacMahon terms as consecutive sums. Need enough skipped values to force A(k)/k→∞.|
|101|erdos359-erdos-359-parts-ii|E359 Po77|d|<0.01|0A|Bound runs of represented integers after each greedy term. A small subsequence misses the uniform o(k^(1+c)).|
|102|erdos359-erdos-359-variants-isgoodfor-1-asymptotic|E359 An75|d|<0.01|0A|Count overlaps of block sums to match Andrews's k log k/log log k with leading constant one.|
|103|erdos364-erdos-364|E364 Sh25|a|0.01|0A|Test both neighbors of powerful Pell pairs. Neither kernel sizes nor solution heights are bounded.|
|104|erdos364-erdos-364-variants-strong|E364 Sh25|d|<0.1|0A|Count a²b³ in short intervals. A positive power saving on every second-neighbor gap requires excluding triples.|
|105|erdos366-erdos-366|E366 Go70|a|≈0|0A|Stream cubefull C=a³b⁴c⁵ and test C−1 for squarefullness. The known Pell controls have reversed order.|
|106|erdos373-erdos-373-variants-maximal-solution|E373 Er76d|a|0.01|0A|Seek n>16 with n! a nontrivial product of factorials. Largest term (n−2)! forces consecutive smooth factors.|
|107|erdos373-erdos-373-variants-suranyi|E373 Ha19|a|<0.001|0A|Test whether n!/a! is a factorial b! with b≤a. Habsieger excludes new two-factor triples to extreme heights.|
|108|erdos375-erdos-375|E375 LaSh06|d|<0.1|0A|Apply Hall to the factor sets of consecutive composites. A deficient subblock would refute Grimm.|
|109|erdos376-erdos-376|E376 EGRS75|d|<0.1|0A|Avoid Kummer carries in bases 3,5,7. The two-base construction must preserve its restrictions in the third.|
|110|erdos383-erdos-383|E383 ErGr80|d|<0.01|0A|Sieve p²+i for p-smoothness simultaneously at 0≤i≤k. For each k this must recur at prime square starts.|
|111|erdos385-erdos-385-parts-i|E385 Er79d|d|<0.1|0A|Cover large n by an earlier composite m with m+minFac(m)>n. Primorials defeat a fixed list of least factors.|
|112|erdos386-erdos-386-variants-two|E386 ErGr80|b|<0.01|0A|Test 8P+1 for squareness over consecutive-prime products P. Five triangular hits leave infinitude open.|
|113|erdos388-erdos-388|E388 Er76d|d|<0.1|0B|Equate factorial quotients of disjoint blocks longer than three. Fixed-length curve bounds lack uniformity.|
|114|erdos389-erdos-389|E389 ErGr80|d|<0.1|0B|Compare adjacent block products prime by prime. Every start needs one length meeting all valuations.|
|115|erdos39-erdos-39|E39 Ru98|d|<0.01|0A|Glue finite Sidon sets. Avoid cross-sum collisions without falling below N^(1/2−ε) between scales.|
|116|erdos396-erdos-396|E396 Po14|d|<0.1|0A|Force Kummer carries for a central binomial at all primes of a falling factorial of length k+1.|
|117|erdos398-erdos-398|E398 Na25|a|<0.001|0A|Test n!+1 for a square and split n!=(m−1)(m+1). Naciri's 7-free neighbor case leaves other roots.|
|118|erdos400-erdos-400-parts-i|E400 2606.23661|d|<0.1|0A|Sum factorial carry excesses. The density-one log n lower bound leaves the mean coefficient undetermined.|
|119|erdos406-erdos-406-variants-one-two|E406 La09|a|<0.1|0A|Search beyond 2^15 for powers with only ternary digits 1,2. Proving maximality requires a tail bound.|
|120|erdos409-erdos-409-variants-sigma-termination|E409 ErGr80|d|<0.1|0A|Track composite σ(n)−1 orbits. A forward-invariant composite family would refute eventual primality.|
|121|erdos41-erdos-41|E41 Ch96b|d|<0.01|0A|Count repeated differences of triple sums. The Sidon zero-liminf argument falls short at the cube-root scale.|
|122|erdos410-erdos-410|E410 ErGr80|d|<0.01|0A|Sum log(σ(m)/m) over each orbit. Divergent kth roots require growth beyond every fixed exponential.|
|123|erdos412-erdos-412|E412 Er79d|d|<0.01|0A|Match factorizations of later σ-iterates to merge orbits. Finite delays cannot certify disjoint tails.|
|124|erdos413-erdos-413-parts-i|E413 La26|d|<0.1|0A|Maximize m+ω(m) over m<n. Need infinitely many barriers controlling every earlier offset.|
|125|erdos414-erdos-414|E414 2609.22298|d|<0.01|0A|Join n+τ(n) orbits in crossing windows. Finite frontier certificates leave all later starts (2609.22298).|
|126|erdos422-erdos-422|E422 ErGr80|d|<0.1|0B|Track missed values of the positive Hofstadter Q recurrence. Even well-definedness at every index is open.|
|127|erdos423-erdos-423|E423 Cu25|d|1|0B|Bound omissions in the greedy block-sum sequence. Tang's logarithmic-iterated excess allows density one.|
|128|erdos428-erdos-428|E428 ErGr80|d|<0.01|0A|Build A near successive prime translates. Its lower relative density must persist between good endpoints.|
|129|erdos430-erdos-430|E430 ErGr80|d|<0.1|0B|Sieve composites m<n for minFac(m)>n−m. Need success even in exceptional short intervals.|
|130|erdos44-erdos-44|E44 Er84b|d|<0.01|0A|Translate near-optimal Sidon designs beyond a fixed seed. Cross-collisions must cost o(√M) points.|
|131|erdos445-erdos-445|E445 He00|d|<0.1|0A|Bound incomplete Kloosterman sums for inverse pairs in one interval. Heath-Brown reaches c>3/4, target c>1/2.|
|132|erdos454-erdos-454|E454 Po79|d|<0.01|0A|Force p_(n+i)+p_(n−i) far above 2p_n for every 0<i<n. Pomerance gets a fixed excess only.|
|133|erdos455-erdos-455|E455 Ri76|d|<0.01|0A|Bound equal-gap runs in convex prime sequences. Even a larger constant times n² falls short of divergence.|
|134|erdos458-erdos-458|E458 ErGr80|a|0.1|0A|Group prime powers by gap and bound their base product. The sparse square-plus-cube case holds for p>32.|
|135|erdos461-erdos-461|E461 ErGr80|d|<0.1|0B|Count distinct t-smooth parts in t consecutive integers. Repetitions cost a log in the known lower bound.|
|136|erdos463-erdos-463|E463 ErGr80|d|<0.1|0A|Find composite n+h with minFac(n+h)>h. Need h growing at every sufficiently large start.|
|137|erdos467-erdos-467|E467 ErGr80|d|<0.1|0B|Partition primes ≤x into two residue covers of [0,x). Fixed-x SAT leaves eventual existence open.|
|138|erdos472-erdos-472|E472 ErGr80|d|<0.1|0B|Choose a seed extending the least-prime recurrence forever. Each next step needs a prime in a changing list.|
|139|erdos478-erdos-478|E478 GSSV24|d|<0.01|0B|Count collisions of k! mod p. Fraction 1−1/e requires joint statistics beyond a power lower bound.|
|140|erdos479-erdos-479|E479 ErGr80|d|<0.01|0A|Preserve 2^n≡k mod n when enlarging n. Need infinitely many exponents for each integer k≠1.|
|141|erdos483-erdos-483|E483 He17|d|<0.1|0B|Bound the Schur-number recursion by a constant factor per color. The usual factorial upper bound exceeds C^k.|
|142|erdos49-erdos-49-variants-primes-maximal|E49 Ta24d|a|0.1|0A|Seek a strict totient chain longer than π(N). Tao's asymptotic allows excess at a single endpoint.|
|143|erdos495-erdos-495|E495 Er61|d|<0.01|0A|Approximate two reals jointly via lattices. Need arbitrarily small n times their two errors for every pair.|
|144|erdos5-erdos-5|E5 Me20|d|<0.01|0A|Construct gaps/log n approaching each C≥0. Known intervals of limit points leave possible holes.|
|145|erdos50-erdos-50|E50 Er95|d|<0.01|0A|Bound local φ(n)/n distribution increments. Singularity leaves possible positive derivatives at exceptional points.|
|146|erdos51-erdos-51|E51 Er95|d|<0.1|0A|Force small prime factors in *every* preimage of a totient value, making its least-preimage ratio diverge.|
|147|erdos517-erdos-517|E517 Po29|d|<0.01|0A|Apply value-distribution bounds to entire Fabry series. Fejér needs reciprocal summability beyond n_k/k→∞.|
|148|erdos52-erdos-52|E52 BSSZ26|d|<0.01|0A|Iterate integer sum-product expansion. A fixed gain above exponent one still misses all 2−ε.|
|149|erdos545-erdos-545|E545 Su11|d|<0.1|0B|Compress Ramsey extremizers to a clique plus one vertex. Exact comparison is needed at every large edge count.|
|150|erdos59-erdos-59-variants-big-o|E59 MoSa16|d|<0.1|0A|Use containers with entropy O(ex(n,H)). For bipartite cyclic H the constant-factor exponent remains open.|
|151|erdos600-erdos-600-parts-i|E600 RuSz78|d|<0.01|0A|Separate adjacent triangle-book thresholds additively. Ruzsa–Szemerédi's o(n²) bound on each allows near ties.|
|152|erdos61-erdos-61|E61 NSS26|d|<0.01|0A|Decompose forbidden H by substitution. Prime patterns still need polynomial homogeneous sets.|
|153|erdos617-erdos-617|E617 ErGy99|a|0.2|0A|Extend an affine plane to a balanced coloring. A frozen core fails. Mixed classes survive the counting bounds.|
|154|erdos647-erdos-647|E647 Er79|a|0.1|0A|Sieve n=360360j by τ(n−h)≤h+2. A single violating shift eliminates n. No survivor passed all shifts.|
|155|erdos65-erdos-65-parts-ii|E65 LiMo20|d|<0.1|0A|Sum reciprocal cycle lengths at fixed size and order. Log lower bounds omit exact bipartite extremality.|
|156|erdos66-erdos-66|E66 Ho07|d|<0.01|0A|Build a thin random basis and repair exceptional sums. Need every count asymptotic to c log n, c≠0.|
|157|erdos672-erdos-672|E672 GHP09|a|<0.01|0A|Factor coprime APs and take the gcd of prime exponents. Search k≥35 beyond proven short lengths.|
|158|erdos677-erdos-677|E677 Er79|a|0.1|0A|Enumerate disjoint runs of divisors of the lower lcm. Fixed-k finiteness permits isolated equalities.|
|159|erdos68-erdos-68|E68 Er68d|d|<0.01|0A|Expand 1/(n!−1) geometrically. Bound carries from higher factorial powers after clearing denominators.|
|160|erdos680-erdos-680-parts-i|E680 Gr95|d|<0.1|0A|Sieve offsets with minFac(n+k)>k²+1. Prime-tuple heuristics leave unconditional uniformity in n open.|
|161|erdos680-erdos-680-parts-ii|E680 Gr95|d|<0.1|0A|Block offsets with large least prime factor. CRT handles a prefix but leaves the exponential-threshold tail.|
|162|erdos681-erdos-681|E681 Er79d|d|<0.1|0A|Seek a rough composite n+k with minFac>k². Nearby primes fail the compositeness guard.|
|163|erdos686-erdos-686-variants-four|E686 Er79d|a|1|0A|Bracket disjoint blocks at ratio four. Small-length exclusions leave an unbounded family of curves.|
|164|erdos686-erdos-686-variants-twenty-five|E686 Er79d|a|0.5|0A|Bound k² by 24(n+k), then bracket the ratio-25 upper start. Excluding k=2,4,6 leaves an infinite tail.|
|165|erdos688-erdos-688-parts-ii|E688 Er79d|d|<0.1|0A|Sieve covers of [1,n] by primes >n^ε. Need to exclude every fixed positive ε eventually.|
|166|erdos695-erdos-695|E695 FKL10|d|<0.01|0A|Use the even multipliers of a prime chain. Doubling forces only exponential growth. Need divergent kth roots.|
|167|erdos695-erdos-695-variants-upperbound|E695 FKL10|d|<0.01|0A|Build a chain by least primes in progressions. Linnik bounds grow too fast for exp(k log^(1+o(1)) k).|
|168|erdos699-erdos-699|E699 ErSz78|d|1|0A|Use Lucas residues for a common factor ≥i. Accepted cases j≤3i/2 or n=2j leave an interior range.|
|169|erdos7-erdos-7|E7 HoNi19|a|<0.01|0A|Search distinct odd moduli by lcm-cover certificates. A lower bound on the lcm gives no global exclusion.|
|170|erdos70-erdos-70|E70 Er87|d|<0.01|0A|Extend red ordinals in a triple coloring. Erdős–Rado's ω+m versus four leaves the ω·2 limit step.|
|171|erdos723-erdos-723-variants-eq-12|E723 BrRy49|a|0.01|0A|Search 157×157 incidence matrices up to relabeling. Seed obstructions leave arbitrary planes untested.|
|172|erdos749-erdos-749|E749 Er94b|d|<0.1|0A|Glue sets with bounded sum representations. Keep A+A dense between blocks to force *lower* density near one.|
|173|erdos770-erdos-770-parts-i|E770 Er74b|d|<0.01|0A|Express h(n)=p via gcds of i^n−1. Truncating to periodic order tests leaves a prime tail in the density.|
|174|erdos770-erdos-770-variants-three|E770 Er74b|d|<0.1|1A|Sieve exponents for gcd(2^n−1,3^n−1)=1. Need infinitely many for h(n)=3.|
|175|erdos774-erdos-774|E774 NRS24|d|<0.1|0A|Color by dissociated sets using compactness. Proportional dissociativity must bound the colors uniformly.|
|176|erdos779-erdos-779|E779 Gu83|a|<0.1|0A|For primorial P test p,P+p between the stated endpoints. Success for each n needs a uniform pair bound.|
|177|erdos78-erdos-78|E78 Li23b|d|<0.01|0A|Derandomize a Ramsey graph on unary input. Li's explicit bound still exceeds O(log n).|
|178|erdos789-erdos-789-variants-sq|E789 St66|d|<0.1|0A|Project unequal-size subset sums apart. A claimed √(n log log n/log n) lower bound leaves a log loss.|
|179|erdos80-erdos-80-parts-ii|E80 FoLo12|d|<0.01|0A|Force one large triangle book by density increments. Regularity gives divergence with no Ω(log n) rate.|
|180|erdos812-erdos-812-parts-i|E812 BEFS89|d|<0.01|0A|Extend optimal diagonal Ramsey colorings by a fixed fraction. Additive gain 4n−8 is insufficient.|
|181|erdos82-erdos-82|E82 FMRS95|d|<0.01|0A|Extract induced regular subgraphs larger than every C log n. Ramsey alone gives one fixed C.|
|182|erdos828-erdos-828|E828 Er83|d|<0.1|0A|Construct infinite families with φ(n) ∣ n+a. Prime powers serve selected offsets, leaving arbitrary signed a.|
|183|erdos828-erdos-828-variants-lehmer-conjecture|E828 Er83|d|<0.01|0A|Sieve odd squarefree composites for φ(n) ∣ n−1. Primes satisfy the equivalence. Composites remain.|
|184|erdos829-erdos-829|E829 St08|d|<0.1|0A|Factor x³+y³ to count cube sums. Divisor bounds must improve to a fixed power of log n.|
|185|erdos835-erdos-835|E835 Er74d|a|<0.1|0A|Seek a large set of Steiner systems at prime k+1. Composite exclusions leave infinitely many k to try.|
|186|erdos849-erdos-849|E849 MRSTT22|d|<0.01|0A|Engineer a binomial hit then enumerate its entire half-row multiplicity. Need examples for every t.|
|187|erdos85-erdos-85|E85 Er93|d|<0.1|0A|Extend an extremal C₄-free graph without losing minimum degree. Asymptotic bounds allow late drops.|
|188|erdos853-erdos-853-parts-i|E853 Er85c|d|<0.01|0A|Realize each even gap between *consecutive* primes. Bounded-gap theorems leave its value unspecified.|
|189|erdos853-erdos-853-parts-ii|E853 Er85c|d|<0.1|0A|Force all even gaps up to A log n by index n. Mere occurrence gives no uniform appearance time.|
|190|erdos86-erdos-86|E86 Ba12b|d|<0.1|0A|Count cube four-cycles via smaller subcubes. The half-density construction needs a matching upper bound.|
|191|erdos87-erdos-87-parts-i|E87 FaMc93|d|<0.01|0A|Transfer clique Ramsey colorings to k-chromatic graphs with subexponential loss. Fixed-base exponential bounds fall short.|
|192|erdos873-erdos-873|E873 Er92c|d|<0.1|0A|Bound consecutive blocks with small lcm via prime powers. Longer blocks must give arbitrarily small counting exponents.|
|193|erdos885-erdos-885|E885 Br19|d|≈0|0A|Extend rational square grids using d²+4N square for each shared difference. Bremner reaches k=4.|
|194|erdos886-erdos-886|E886 ErRo97|d|<0.1|0A|Count near-square factor pairs. The n^(1/4) interval bound leaves wider intervals n^(1/2−ε).|
|195|erdos889-erdos-889|E889 ErSe67|d|<0.1|0A|Force many fresh primes >k into one n+k. The known two-prime bound leaves growth open.|
|196|erdos889-erdos-889-variants-general|E889 ErSe67|d|<0.1|0A|Force the same fresh-prime gain after an arbitrary prescribed minimum shift l. Fixed l=0 gives less.|
|197|erdos89-erdos-89|E89 GuKa15|d|<0.01|0A|Improve Guth–Katz's n/log n by √log n. The square grid matches the conjectured distance scale.|
|198|erdos890-erdos-890-parts-a|E890 ErSe67|d|<0.1|0A|Construct infinitely many k-blocks with ≤k large primes counted termwise. Pólya's k−1 bound limits candidates.|
|199|erdos890-erdos-890-parts-b|E890 ErSe67|d|<0.01|0A|Use primorials for the lower block-ω limsup. Individual maximal-order upper bounds lose a factor k.|
|200|erdos891-erdos-891|E891 Po18|d|<0.1|0A|Find >k distinct factors in each late primorial-length interval. The forced primorial multiple can be smooth.|
|201|erdos893-erdos-893|E893 KoLu25|d|<0.01|0A|Compare Mersenne divisor totals at 2n and n. Kovač–Luca give unbounded ratios only on a subsequence.|
|202|erdos9-erdos-9|E9 Pa11|d|<0.1|0A|Exclude p+2^i+2^j on a positive upper proportion of odds. Crocker's infinite exceptions can have zero density.|
|203|erdos91-erdos-91|E91 Ko24c|d|<0.1|0A|Deform a distinct-distance minimizer preserving optimality. Need two inequivalent optima for every large size.|
|204|erdos912-erdos-912|E912 Er82c|d|<0.1|0A|Group valuations of n! by prime intervals. The √(n/log n) order leaves the limiting coefficient open.|
|205|erdos912-erdos-912-variants-tao|E912 Er82c|d|<0.01|0A|Match Tao's √(2π) coefficient by bounding gap correlations in n!'s valuations. The Cramér model is heuristic.|
|206|erdos913-erdos-913-variants-infinite-many-8p-sq-sub-one-primes|E913 Er82c|d|<0.1|0A|Sieve p and 8p²−1 together. Admissibility leaves the infinitude of simultaneous primes open.|
|207|erdos930-erdos-930|E930 ErSe75|d|<0.1|0A|Isolate a valuation across r disjoint long intervals. Exponents from different blocks can cancel modulo l.|
|208|erdos931-erdos-931|E931 Er76d|d|<0.1|0A|Match prime supports of disjoint blocks, longer first. The known infinite (3,4) family has reversed lengths.|
|209|erdos932-erdos-932|E932 Er76d|d|<0.1|0A|Construct two gap-smooth integers in infinitely many prime gaps. Density zero for even one permits infinitude.|
|210|erdos933-erdos-933|E933 Er76d|d|<0.1|0A|Vary n=2^(3^r) to exceed every multiple of n log n in the 2,3-valuation product. This family gives a constant.|
|211|erdos936-erdos-936-variants-factorial-add-one|E936 Cr20|d|<0.1|0A|Force an exponent-one prime in n!+1, necessarily >n. Known radical estimates are conditional on abc.|
|212|erdos936-erdos-936-variants-factorial-sub-one|E936 Cr20|d|<0.1|0A|Sieve n!−1 for a simple prime divisor eventually. Coprimality with n! removes all small candidate primes.|
|213|erdos936-erdos-936-variants-two-pow-add-one|E936 Cr20|d|<0.1|0A|Factor 2^n+1 cyclotomically. A primitive prime can occur squared, so its first appearance is insufficient.|
|214|erdos936-erdos-936-variants-two-pow-sub-one|E936 Cr20|d|<0.1|0A|Lift valuations in 2^n−1. Wieferich primes obstruct the step from primitive divisibility to exponent one.|
|215|erdos942-erdos-942|E942 DLS05|d|<0.1|0A|Count a²b³ between squares and match both log exponents. Divergent limsup alone gives no shared exponent.|
|216|erdos943-erdos-943|E943 Er76d|d|<0.1|0A|Count n=a²b³+c²d³ with squarefree kernels. Summing over all kernels must preserve a subpower bound.|
|217|erdos945-erdos-945|E945 ErMi52|d|<0.1|0A|Bound runs of distinct τ-values by short-interval divisibility. Subexponential bounds exceed the polylog target.|
|218|erdos949-erdos-949|E949 Er77c|d|<0.1|0A|Recursively avoid S and S−a for a sum-free S. Continuum-sized S can exhaust the choices for new points.|
|219|erdos950-erdos-950-parts-i|[E950](https://www.erdosproblems.com/latex/950) Er77c|d|<0.01|0A|For f(n)=Σ_{p<n prime}1/(n−p), the mean gives liminf≤1. Need f(n)≥1−ε eventually for each ε.|
|220|erdos950-erdos-950-parts-ii|[E950](https://www.erdosproblems.com/latex/950) Er77c|d|<0.1|0A|Construct prime clusters below n with unbounded reciprocal mass. Bounded gaps alone contribute finitely much per pair.|
|221|erdos950-erdos-950-parts-iii|[E950](https://www.erdosproblems.com/latex/950) Er77c|d|<0.1|0A|Sum reciprocal prime mass in dyadic shells. Uniform savings must hold even at exceptional n for o(log log n).|
|222|erdos951-erdos-951|E951 Er69|d|<0.1|0A|Compare a separated Beurling system with π(x). Refutation needs excess at unbounded x in one system.|
|223|erdos962-erdos-962|E962 Er65|d|<0.01|0A|Bound blocks whose terms each have a prime factor exceeding the block length. The √n ceiling misses the log exponent.|
|224|erdos972-erdos-972|E972 Vi48|d|<1|0A|Sieve p and floor(αp) jointly. Vinogradov equidistribution alone leaves primality of the second value open.|
|225|erdos975-erdos-975|E975 Mc99|d|<1|0A|Switch divisors in τ(f(n)). Known x log x order lacks a leading constant for general degree ≥3.|
|226|erdos979-erdos-979|E979 Er65b|d|<0.01|0A|Seek repeated k-prime sums of kth powers. The square and cube cases leave unbounded multiplicity for k≥4.|
|227|erdos98-erdos-98|E98 EFPR93|d|<0.01|0A|Count equal-distance incidences in general position. Even a linear lower bound misses superlinear growth.|
|228|erdos982-erdos-982|E982 NPPZ13|d|≈0|0A|Count isosceles triangles at one convex vertex. The 13/36-scale result misses half, attained by regular polygons.|
|229|erdos99-erdos-99|E99 BeFo99|d|<0.01|0A|Perturb an optimal separated packing without a unit equilateral triple. Lattice density gives no exact triangle.|
|230|fermat-infinite-fermat-primes|W|d|<0.01|0A|Sieve Fermat numbers by factor orders. Pépin tests one index. Infinitude needs unbounded prime indices.|
|231|fulloldproblemscatalog-bergefulkerson-conjecture|arXiv 2607.29511|d|<0.01|0A|Round a fractional matching cover of a bridgeless cubic multigraph to six matchings, each edge occurring twice.|
|232|fulloldproblemscatalog-chvataltoughness-conjecture|arXiv 2506.12684|d|<0.01|0A|Extract a small cut from a longest nonspanning cycle. Need one toughness ceiling for all non-Hamiltonian graphs.|
|233|fulloldproblemscatalog-erdospurdydegeneratequadruples-conjecture|E1087 ErPu71|d|<0.01|0A|Bound quadruples with a repeated distance. Count equal incident edges and equal disjoint edges separately.|
|234|fulloldproblemscatalog-hajoscycledecomposition-conjecture|arXiv 2610.07840v2|d|<0.01|0A|Remove long cycles while charging vertices. The new O(n) cycle decomposition misses the floor((n−1)/2) bound.|
|235|fulloldproblemscatalog-kotzigperfectfactorization-conjecture|arXiv 2607.09459|d|<0.01|0A|Repair the o(n) exceptional matchings in the asymptotic factorization while preserving every Hamilton union.|
|236|fulloldproblemscatalog-lovaszhamiltonpath-conjecture|arXiv 2609.38135v2|d|<0.01|0A|Lift paths from vertex-transitive quotients. A path on n^(1−o(1)) vertices still need not span.|
|237|fulloldproblemscatalog-marcusblockpermanent-conjecture|arXiv 2611.22058|d|<0.1|0A|Extend symmetric-web positivity beyond four blocks. Five small blocks and unrestricted equality cases need checking.|
|238|fulloldproblemscatalog-marcusdeoliveira-conjecture|[DOI](https://doi.org/10.3390/math13050711)|d|<0.1|0A|Vary the relative eigenbases of normal A,B. Commuting matrices give vertices of the proposed determinant hull.|
|239|fulloldproblemscatalog-minkowskiinhomogeneousproduct-conjecture|[DOI](https://doi.org/10.1112/S0025579300000863)|d|<0.01|0A|Reduce lattices by diagonal scaling to bound the inhomogeneous product. Low-dimensional covers need uniform extension.|
|240|fulloldproblemscatalog-riddellerdosprogressionratio-conjecture|E201 KSS75|d|<0.01|0A|Embed finite integer sets into intervals preserving k-APs. The extremal ratio requires o(1) relative loss.|
|241|fulloldproblemscatalog-sidonsubsetasymptotic-conjecture|E530 AlEr85|d|<0.1|0A|Sample N reals and delete Sidon collisions. The guaranteed subset needs leading constant one at scale √N.|
|242|fulloldproblemscatalog-tuttefiveflow-conjecture|[source](https://dwest.web.illinois.edu/openp/tut5flow.html)|d|<0.01|0A|Modify a six-flow by circulations to obtain a five-flow. Keep every edge nonzero across small cuts.|
|243|fulloldproblemscatalog-tuttethreeflow-conjecture|arXiv 2609.08377|d|<0.01|0A|Join modulo-three orientations across small cuts. Six-edge-connected results omit four- and five-edge cuts.|
|244|fulloldproblemscatalog-vizingindependence-conjecture|arXiv 1805.05996|d|<0.01|0A|Charge independent vertices to neighbors using Δ-criticality. Need half-density even at small minimum degree.|
|245|fulloldproblemscatalog-wanghadamardpermanentnonvanishing-conjecture|[DOI](https://doi.org/10.1007/BF02760844)|a|<0.1|0A|Compute permanents of Hadamard matrices by orbit sums to seek zero. Sylvester formulas cover a restricted family.|
|246|gausscircleproblem-error-isbigo|W/arXiv 2305.03549|d|<1|0A|Bound oscillatory disk-boundary sums pointwise. Mean-square cancellation leaves the r^(1/2+o(1)) error open.|
|247|goldbachconjecture-goldbach|W|d|<0.01|0A|Sieve p,n−p at even n. Chen permits an almost-prime. Finite Goldbach checks leave unbounded exceptions.|
|248|goormaghtigh-goormaghtigh-conjecture|[source](https://math.colgate.edu/~integers/y98/y98.pdf)|a|<1|0A|Compare repunits in distinct bases. Fixed-base uniqueness leaves both bases unbounded, including composite repunits.|
|249|hadamard-hadamardconjecture|W|d|<0.01|0A|Fill missing Hadamard orders by products and designs. A single new 4k construction leaves the universal claim open.|
|250|hardylittlewood-first-hardy-littlewood-conjecture|W|d|<0.01|0A|Control the prime-tuple error around the singular series. The two-shift case already demands twin-prime asymptotics.|
|251|hardylittlewood-second-hardy-littlewood-conjecture|W|d|<0.01|0A|Search for an interval denser than its initial counterpart. Hensley–Richards relies on the unproved tuple conjecture.|
|252|hilbertcatalog-borgerdesmitquestion4-conjecture|arXiv 1809.02295|d|<0.01|1C|Construct compatible Frobenius lifts for one field other than ℚ or an imaginary quadratic. Need its full abelian closure.|
|253|hilbertcatalog-hilbert12lambdageometric-conjecture|arXiv 1809.02295|d|<0.01|0C|Extend toric and CM constructions to arbitrary number fields. The lifts must generate all abelian layers.|
|254|hilbertcatalog-hilbert13-conjecture|[source](https://www.math.uchicago.edu/~farb/papers/RD.pdf)|d|<0.01|0B|Obstruct two-parameter resolvents for the general septic. Three parameters give the upper bound only.|
|255|hilbertcatalog-hilbert16quinticsurfaces-conjecture|[source](https://mathcs.clarku.edu/~djoyce/hilbert/problems.html#prob16)|a|<0.1|0D|Patchwork smooth real quintics and certify topology. A 24-component surface beats the known 23 example.|
|256|hilbertcatalog-hilbert6vlasovpoissonlimit-conjecture|arXiv 1502.04608|d|<1|0C|Control close Coulomb pairs to remove the cutoff in mean-field convergence. Smooth VP existence alone is insufficient.|
|257|hilbertcatalog-rankoneabelianstark-conjecture|[source](https://math.berkeley.edu/~hhao/notes/Rank-one%20abelian%20Stark%20conjecture.pdf)|d|<0.01|0B|Build the rank-one Stark unit from an L-derivative. Finite-place results leave archimedean equivariance.|
|258|inscribedsquare-inscribed-square-problem|W/arXiv 2005.09193|d|<0.01|0A|Approximate Jordan curves by smooth ones with squares. Prevent collapse to a point when taking limits.|
|259|inversegalois-inverse-galois-problem|W/arXiv math/9809211|d|<0.01|0A|Construct a rigid G-cover over ℚ(t) and specialize by Hilbert irreducibility. Shafarevich covers solvable G. No general nonsolvable construction.|
|260|irrational-irrational-eulermascheroniconstant|W/arXiv math/0209070|d|<0.01|0A|Use Sondow's small linear forms for γ. arXiv 2312.00295 claims irrationality. Its decisive error bound is UNVERIFIED.|
|261|kummervandiver-kummer-vandiver|W/arXiv 1605.02398|a|<1|0A|Sieve irregular p and test the real class number. Hart–Harvey–Ong verify p<2³¹. Need the tail.|
|262|legendreconjecture-legendre-conjecture|W|d|<0.01|0A|Seek an effective prime bound at x=n². Ferreira claims the large-n case. Validity and cutoff are UNVERIFIED.|
|263|lehmermahlermeasureproblem-lehmer-mahler-measure-problem|W|d|<0.01|0A|Strip cyclotomic factors and bound Mahler measure. Degree-dependent gaps above one decay with degree.|
|264|lehmertotient-lehmer-totient|W/arXiv 2409.17076|a|<0.1|0A|Sieve odd squarefree composites with φ(n) ∣ n−1. Spoof factorizations need actual prime factors.|
|265|lemoine-lemoine-conjecture|W/arXiv 2304.00024|d|<0.01|0A|Count n=p+2q by a binary sieve for each odd n≥7. Verification through 10¹³ still leaves the tail.|
|266|math30catalog-source16|[source](https://epoch.ai/frontiermath/open-problems/matrix-multiplication)|a|≈0|0A|Test the 4,096 tensor equations for rank ≤47 over ℂ. A failed lift omits other initial tensors.|
|267|math30catalog-source20|arXiv 2005.00566v2|d|<0.01|0A|Seek a fixed saving in Huang's quadratic sensitivity bound in terms of real degree. Uniformity in dimension matters.|
|268|math30catalog-source21|[source](https://eccc.weizmann.ac.il/report/2026/010/)|d|<0.1|0A|Constrain disjoint sensitive blocks by sensitive edges. The quartic degree-based bound misses cubic growth.|
|269|mersenne-catalans-mersenne-conjecture|W|a|<0.01|0A|Seek factors of Catalan–Mersenne iterates via modular powers. The first untested iterate already defies direct testing.|
|270|mersenne-infinitely-many-mersenne-primes|W|d|<0.01|0A|Sieve Mersenne exponents by possible factor orders. Lucas–Lehmer decides each p but gives no infinite supply.|
|271|normalnumber-pi-normal-base-ten|W|d|<0.01|0A|Bound exponential sums along 10^jπ mod 1. Normality needs all decimal block frequencies in the limit.|
|272|oppermann-oppermann-conjecture|W|d|<0.01|0A|Sieve on both sides of x² separately. Legendre between squares fails to specify both required half intervals.|
|273|perfectnumbers-odd-perfect-number-conjecture|W/arXiv 2607.04365|d|<0.01|0A|Close σ(N)=2N factor chains for odd N. A 2026 minimal-prime branch certificate was withdrawn (2607.04365).|
|274|pollocksconjecture-pollock-tetrahedral|W|d|<1|0A|Convolve five tetrahedral sequences with zero allowed. Four-term tables still need a uniform five-term covering.|
|275|primesandperfectsquares-infinite-prime-sq-add-one|W|d|<0.01|0A|Sieve n²+1 at square-root level. The x²+y⁴ prime theorem allows varying y, while here y=1.|
|276|regularprimes-regularprime-conjecture|W/arXiv 1605.02398|d|<1|0A|Test regularity by Bernoulli numerators. Infinitely many irregular primes leave regular-prime infinitude open.|
|277|twinprimes-twin-primes|W|d|<0.01|0A|Sieve p and p+2. Bounded prime gaps leave the difference unspecified. The parity barrier survives at two.|

[inv]: https://raw.githubusercontent.com/identity-md-launches/goal-3467-objective-settle-least-one/3d3f3a09d60c67992738413746463076008eb894/catalog/inventory.json
[tri]: https://api.imd.fun/artifacts/d5172e566c7d8638a9ec8787f655482e792ce75b525253ee24f36c774b8775dc
[replay]: https://api.imd.fun/artifacts/8e24fdb29b0ffe17f11d807863232013017e4cdf8cab52594ca7e47c083b4ac5
[root1]: https://api.imd.fun/artifacts/4e00cbd672d6bf02e6883504d921f60a3e4506bfb1c229274c914fd8f655b04d
[root2]: https://api.imd.fun/artifacts/686a010feb867406567a8dd9044058a60ed72e27af93aa440b6d74a5205b3919
[stability]: https://api.imd.fun/artifacts/3301187f24541418906fe5aeb08e01c5ec80d7a1c499b51313147a1cb846f9e1
[support]: https://raw.githubusercontent.com/conjectures-io/conjectures-validator/57c969e87cad845b60908cef474c8d1c0b6e43c5/lean/TaskSupport.lean
[patch]: https://raw.githubusercontent.com/conjectures-io/conjectures-tasks/f5dab9b843c460bf946e0ec7b0e6ad2f2f739eb8/tiers/tier-1/formal-conjectures-audit-fixes.patch
[e49]: https://api.imd.fun/artifacts/604fec89f9a5c83f138036d9532d83dc92d036ad17b6a158b45c19e0e0728976
[e458]: https://api.imd.fun/artifacts/a8941ccecef07aaec7c3aec4551798975a2d20cc83fc8748862373b314999d77
[e324]: https://api.imd.fun/artifacts/7679572c40018e639445d2ee0f4d29edeb08630653be59ab60365718d65807e6
