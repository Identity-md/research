# Justin Sun Prize · Lean formalization survey

**289 in-range problems met the bank filter. Zero cleared the prior-work screen.** Neither attempted proof closed. No claim or PR was submitted. At the 23 November 2026 pin `7782c2aa02df745da60d53e61718b714f8685a98`, all matches read **Solved / Lean No / Eligible No / Solver Unavailable / Lean Unavailable**. None had Lean Pending. Counts by hundred were 15, 20, 22, 28, 31, 28, 42, 30, 37, 27 and 9 through 001022. The last catalog extends through 001072. Its three additional matches bring the total to 292 among 1,072 entries, 396 solved. [Pinned index](https://github.com/TheJustinSunPrize/awards/blob/7782c2aa02df745da60d53e61718b714f8685a98/problems/README.md)

## Shortlist under the exclusion rule

**288 of 289 in-range IDs appear by exact ID in an open Lean submission.** I checked all 12 pages (1,146 open PRs). Each hit gives a PR number at `TheJustinSunPrize/awards/pull/<number>`. A registration suffices to establish overlap. **000036** has closed partial submissions and overlapping semistable modularity work. Whether anyone is formalizing its full universal theorem remains unresolved. [Open PR register](https://github.com/TheJustinSunPrize/awards/pulls?q=is%3Apr+is%3Aopen) · [000036 submission](https://github.com/TheJustinSunPrize/awards/pull/3878) · [FLT blueprint](https://imperialcollegelondon.github.io/FLT/blueprint/sect0001.html)

The initial shortlist (000173, 000198, 000108, 000121, 000139) came from a rate-limited search that missed public registrations for all five. The re-screen examined 36 in range. The audit examined the other 253, originally grading 226 as matches and flagging 27. The final selector found no backups. Searches covered awards and other GitHub repos, Mathlib, Erdős Problems, Formal Conjectures and the Lean Zulip archive. Some Erdős pages returned 403. Negative searches cannot establish priority. [Formal Conjectures](https://github.com/google-deepmind/formal-conjectures) · [Zulip archive](https://leanprover-community.github.io/archive/)

### Five exclusions ordered by estimated proof effort

|Order|JSP|Mathematical task and screening outcome|
|---|---|---|
|1|000301|Consecutive powerful nonsquares include 12167=23³, 12168=2³·3²·13², both between 110² and 111². One paragraph of arithmetic, same witness already formalized. [PR 1197](https://github.com/TheJustinSunPrize/awards/pull/1197)|
|2|001018|Two distinct contiguous blocks in a sufficiently long increasing sequence with bounded gaps and fixed first term have equal sums. Hegyvári’s 1–2 page pigeonhole argument already has competing proofs. [PR 1622](https://github.com/TheJustinSunPrize/awards/pull/1622)|
|3|000605|In any uncountably chromatic graph, ∃ edge e, ∃ N, ∀ n≥N, ∃ an n-cycle through e. Thomassen’s two-page proof uses infinite graphs. The unrestricted helper already proves it. [Lean theorem](https://github.com/plby/lean-proofs/blob/8822f7ddef30fadbd92e1c6ab4ed897af356af5e/src/latest/ErdosProblems/Erdos737.lean#L1181)|
|4|000198|Classify empty convex polygon thresholds. Finite certificates offer a route for hexagons, but a same-ID classification is already under review. The attempted endpoint used `sorryAx`. [PR 726](https://github.com/TheJustinSunPrize/awards/pull/726)|
|5|000036|Realize every elliptic curve over ℚ by a weight-two modular form. One-curve and semistable results leave the general lifting argument open in Lean. The attempted endpoint used `sorryAx`. [Semistable work](https://tianyipeng.github.io/fermats-last-theorem/route/s4.html)|

For the three supplemental rows, 001067 and 001070 have same-ID PRs. For 001058 the quintic Liénard result and Hilbert 16 statement request overlap the topic. Full degree-uniform Lean coverage remains unverified. [Formal Conjectures issue](https://github.com/google-deepmind/formal-conjectures/issues/1805)

## Two unsuccessful builds

No code trunk or merged commit was created. The declarations and logs come from the two workers. Both ran `lake update`, fetched the Mathlib cache and ran `lake build` (exit 0) on Lean `v4.37.0-rc1`, Mathlib `90e6eec9fe53b02d431c90718e4a1d22d67a204e`. Both later slots returned no target. No independent replay ran. [Mathlib pin](https://github.com/leanprover-community/mathlib4/tree/90e6eec9fe53b02d431c90718e4a1d22d67a204e)

### JSP-000198 · exact hexagon threshold

`b09-slot-1` stopped at the whole conjunction. Emptiness is relative to S. Forcing quantifies over all cardinalities ≥N, while counterexamples have each exact cardinality M.

```lean
import Mathlib

open Finset Set

namespace JSP198

abbrev Point := Fin 2 → ℝ

def orient (a b c : Point) : ℝ :=
  (b 0 - a 0) * (c 1 - a 1) - (b 1 - a 1) * (c 0 - a 0)

def GeneralPosition (S : Finset Point) : Prop :=
  ∀ a ∈ S, ∀ b ∈ S, ∀ c ∈ S,
    a ≠ b → a ≠ c → b ≠ c → orient a b c ≠ 0

noncomputable def Hole (S : Finset Point) (k : ℕ) : Prop := by
  classical
  exact ∃ V : Finset Point, V ⊆ S ∧ V.card = k ∧
    (∀ v ∈ V, v ∉ convexHull ℝ ((V.erase v : Finset Point) : Set Point)) ∧
    (∀ p ∈ S \ V, p ∉ convexHull ℝ (V : Set Point))

def Force (N k : ℕ) : Prop :=
  ∀ S : Finset Point, GeneralPosition S → N ≤ S.card → Hole S k

theorem empty_polygon_threshold_classification :
    (∀ N : ℕ, Force N 3 ↔ 3 ≤ N) ∧
    (∀ N : ℕ, Force N 4 ↔ 5 ≤ N) ∧
    (∀ N : ℕ, Force N 5 ↔ 10 ≤ N) ∧
    (∀ N : ℕ, Force N 6 ↔ 30 ≤ N) ∧
    (∀ k : ℕ, 7 ≤ k → ∀ M : ℕ, ∃ S : Finset Point,
      S.card = M ∧ GeneralPosition S ∧ ¬ Hole S k) := by
  sorry

end JSP198

#print axioms JSP198.empty_polygon_threshold_classification
```

```text
⚠ [18295/18297] Built JSP198 (58s)
warning: JSP198.lean:33:8: declaration uses `sorry`
info: JSP198.lean:44:0: 'JSP198.empty_polygon_threshold_classification' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
Build completed successfully (18297 jobs).
```

`JSP198.FinalAssembly.erdos216_classification` supplies 3, 5 and 10 for k=3,4,5, plus exact-size Horton counterexamples for every k≥7. Reuse requires translating its pair coordinates, general position and holes to the hull model above, then rebuilding. Its fourth branch gives a finite least g₆. Proving **g₆=30** requires the 29-point witness and sharp upper bound. The public sharp theorem’s axiom record includes `Geo.unsat_6hole_cnf`, `mathlibSorry` and `Lean.ofReduceBool`. Its geometry-to-CNF reduction and UNSAT certificate need kernel verification within the axiom limit. [Reusable classification](https://github.com/peilinliu66-dev/jsp-000198-lean/blob/0202e2902bbe51bcf202dc117075b2869e76a355/FinalClassification.lean) · [Sharp theorem](https://github.com/bsubercaseaux/EmptyHexagonLean/blob/3073981d2aa5aa1e399b382e605c0ed12a0b69af/Lean/Geo.lean)

### JSP-000036 · universal eigenform witness

These are the local definitions and exact type from `b09-slot-2`, with the theorem body shortened to the unresolved placeholder. Equality covers every positive coefficient, including bad factors.

```lean
module

public import Mathlib.AlgebraicGeometry.EllipticCurve.LFunction
public import Mathlib.NumberTheory.ModularForms.QExpansion

public section

open scoped UpperHalfPlane BigOperators MatrixGroups
open UpperHalfPlane

namespace JSP36

def scalePoint (p : ℕ) (hp : 0 < p) (z : ℍ) : ℍ :=
  ⟨(p : ℂ) * (z : ℂ), by
    simp only [Complex.mul_im, Complex.natCast_re, Complex.natCast_im, zero_mul, add_zero]
    exact mul_pos (by exact_mod_cast hp) z.im_pos⟩

noncomputable def cosetPoint (p : ℕ) (hp : 0 < p) (j : ℕ) (z : ℍ) : ℍ :=
  ⟨((z : ℂ) + (j : ℂ)) / (p : ℂ), by
    rw [Complex.div_natCast_im]
    simp only [Complex.add_im, Complex.natCast_im, add_zero]
    exact div_pos z.im_pos (by exact_mod_cast hp)⟩

noncomputable def primeHecke (N p : ℕ) (hp : p.Prime) (f : ℍ → ℂ) (z : ℍ) : ℂ :=
  (if p ∣ N then 0 else (p : ℂ) * f (scalePoint p hp.pos z)) +
    (∑ j ∈ Finset.range p, f (cosetPoint p hp.pos j z)) / (p : ℂ)

def IsPrimeEigenform (N : ℕ) (f : ℍ → ℂ) : Prop :=
  ∀ (p : ℕ) (hp : p.Prime), ∃ eigenvalue : ℂ,
    ∀ z : ℍ, primeHecke N p hp f z = eigenvalue * f z

open CongruenceSubgroup

theorem modularity (W : WeierstrassCurve ℚ) [W.IsElliptic] :
    ∃ (N : ℕ) (_ : 0 < N) (f : CuspForm (Gamma0 N : Subgroup (GL (Fin 2) ℝ)) 2),
      IsPrimeEigenform N f ∧
      (UpperHalfPlane.qExpansion 1 f).coeff 1 = 1 ∧
      ∀ n : ℕ, 0 < n → (UpperHalfPlane.qExpansion 1 f).coeff n = (W.LFunction n : ℂ) := by
  sorry

end JSP36
#print axioms JSP36.modularity
```

```text
⚠ [7385/7387] Built JSP36 (4.7s)
info: JSP36.lean:239:2: W : WeierstrassCurve ℚ
inst✝ : W.IsElliptic
⊢ ∃ N,
    ∃ (_ : 0 < N),
      ∃ f, IsPrimeEigenform N ⇑f ∧ ∀ (n : ℕ), 0 < n → (PowerSeries.coeff n) (qExpansion 1 ⇑f) = ↑(W.LFunction n)
warning: JSP36.lean:227:8: declaration uses `sorry`
info: JSP36.lean:253:0: 'JSP36.modularity' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
Build completed successfully (7387 jobs).
```

In the actual proof `curveLFunction_at_one` reduced normalization to coefficient equality. Removing the placeholder and running `lake env lean JSP36OpenGoal.lean` exited 1 at the displayed existential. Nine auxiliary axiom checks printed only `[propext, Classical.choice, Quot.sound]`. Constructing the witness still requires residual modularity, wild deformation, lifting and local-factor comparison for arbitrary W. Conductor minimality and identification with the analytic Euler product were not checked. [BCDT, Theorem A][s1] · [E₁₁ at 2, 3, 5](https://github.com/CreizyLabs/bounty_solves/blob/4495135202f5f9d2882d881861c85f59c738f276/BountySolves/ModularityTheorem.lean)

## Amount and claim procedure

Intersecting all 292 IDs with the 50 pilot IDs gives **zero**. All inventory rows use the **legacy route**. For Tier II (Breakthrough), III (Landmark), IV (Advance) and V (Contribution), the Academic Committee sets and publishes the gross allocation upon review. Lean alone receives **30% of that allocation**, solver 70%, both roles 100%. No row has a verified dollar award. Tier I fixes $1 million gross. MathDB publishes separate pilot caps. [Register](https://github.com/TheJustinSunPrize/awards/blob/7782c2aa02df745da60d53e61718b714f8685a98/problems/mathdb-pilot.md) · [Rules][s2] · [Pilot caps](https://www.hejustinsun.com/prize/mathdb)

1. Search open, merged and closed submissions by JSP ID and role. Publish the Lean proof with traceable history. Priority depends on the earliest valid public proof. The rules cover achievements from 1 January 2026. Per-role application of the cutoff to older solutions remains unclear.
2. Ordinarily, fork `TheJustinSunPrize/awards`, edit the catalog entry and PR to `main`. Link the mathematical solution, solver and Lean credits, original external source repo, branch and full SHA, statement path and theorem name. Match definitions, hypotheses, quantifiers and cases. Give pinned toolchain and manifest, clean build commands and actual `#print axioms` output. Maintainers review the mathematics, reproduce the proof and compare priority. [PR template](https://github.com/TheJustinSunPrize/awards/blob/7782c2aa02df745da60d53e61718b714f8685a98/.github/PULL_REQUEST_TEMPLATE.md)
3. **Peer-verified registration.** If the Lean formalization is publicly released and broadly recognized by community consensus as peer-verified, §4.1 waives re-verification. Submit a registration application in place of the verification PR. Entry follows verification of its traceable timestamp. The rules leave the form and its interaction with the ordinary issue template unspecified. [Rules §4.1][s2]
4. On the ordinary route, after merge open your own `[Award claim] JSP-xxxxxx` issue for the Lean role. Link the catalog, merged PR and proof repo. Send identity verification privately by email as directed. Candidate publication starts 14 days of public review. Recipient confirmation and KYC precede TRC-20 USDT or ERC-20 USDC payment. [Legacy process](https://github.com/TheJustinSunPrize/awards/blob/7782c2aa02df745da60d53e61718b714f8685a98/docs/award-process.md) · [Claim form](https://github.com/TheJustinSunPrize/awards/issues/new?template=claim-award.yml)

## Scope checks

- **000027.** The bank’s 8 October review and PR 4970 credit infinitude for every admissible base. Density remains outside the solved assertion. The bank records independent review of the manuscript as pending. [PR 4970](https://github.com/TheJustinSunPrize/awards/pull/4970)
- **000126.** K₆ plus countably many isolated vertices forces a monochromatic triangle by R(3,3)=6 and has no K₇. The ordinal theorem negates an implication whose red alternative is a copy of the entire order type. It does not settle the symmetric graph formulation. [Erdos118.lean](https://github.com/plby/lean-proofs/blob/8822f7ddef30fadbd92e1c6ab4ed897af356af5e/src/latest/ErdosProblems/Erdos118.lean#L724)
- **000554.** The gap (23,29) has length 6, but 24 through 28 have least prime factors 2,5,2,3,2. Gafni–Tao and `erdos_682` prove density one, allowing exceptions. Open PR 1116 also tackles the universal wording.
- **000622.** At n=1,…,19 the reported maxima are 1,1,2,2,3,3,3,3,4,4,4,4,5,5,5,6,6,6,6. `erdos_758` gives only z(12)=4. For z(15)≤5, remove a homogeneous triple by R(3,3)=6 and use the 12-vertex bound. A 15-vertex induced subgraph of Paley(17) has no homogeneous four-set, giving z(15)≥5. ¹The n=12 Lean file spans 3,046 lines plus certificate imports. [Erdos758.lean](https://github.com/plby/lean-proofs/blob/8822f7ddef30fadbd92e1c6ab4ed897af356af5e/src/latest/ErdosProblems/Erdos758.lean#L3039)
- **000895.** Glock’s k=5 case disproves the universal 1/6 limit in `not_erdos_1076`. The approximate Steiner construction concerns simultaneous local sparsity. [Steiner paper](https://arxiv.org/abs/1808.01065)
- **000589 and 000933.** The former row links Hunter’s lower bound, Schoen’s historical upper bound and Bloom–Sisask for the sharper Roth-based upper bound. The latter links Just–Krawczyk for CH isomorphism, Farah Cor. 3.4.4 for nonisomorphism under OCA+MA, and Abraham–Rubin–Shelah for consistency. The audit compared MeowLean’s relative-independence theorem, while plby's theorem has hypothesis CH. [MeowLean submission](https://github.com/TheJustinSunPrize/awards/pull/5614)

## Inventory

Six-digit IDs carry the JSP prefix. Each Erdős number links a solution or its source discussion. “Paper” means no Erdős number. Lengths are approximate pages, article or manuscript envelopes (a, m), or the indicated units. Proof dependencies may add work.

C = audit or corrected source match, S = re-screen source match to the published resolution, N = partial or scope-sensitive, E = competing effort, G = failed target with overlap. The in-range counts are **225 C, 30 S, 29 N, 3 E, 2 G**. No public proof was independently rebuilt or axiom-checked. Sources include b02, b07–08 and b10–12. Checks flagged parts of scans 301–500 and 1001–1022, screen 401–500, second selection, both attempts and audit 471–600. [Pinned Lean collection](https://github.com/plby/lean-proofs/tree/8822f7ddef30fadbd92e1c6ab4ed897af356af5e/src/latest/ErdosProblems)

Area codes denote G SimpleGraph, HG hypergraphs, R Ramsey, F Finset, P probability, As asymptotics, D density, Pr primes, Div divisors, Siv sieve, Add additive combinatorics, APs progressions, Geo geometry, Conv convexity, Poly polynomials, CA complex analysis, Meas measure, Four Fourier, Top topology, Ord ordinals, Card cardinals, EC elliptic curves, MF modular forms, Grp groups, Col colorings.

|JSP|Erdős / solution|Question or resolution|Length|Areas|Lean|Open PR|
|---|---|---|---|---|---|---|
|000018|[paper](https://arxiv.org/abs/2411.19826)|Maximal area of a sofa that can turn a unit-width right angle?|119|Conv Geo|C|4441|
|000027|[paper](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Primitive-roots-for-every-admissible-integer-base-October-4-2026/primitive-roots-all-integer-bases.pdf)|Infinitely many primes with primitive root a for each nonsquare a≠−1.|92m|ZMod Pr|C|4970|
|000035|[paper](https://doi.org/10.1515/crll.2004.048)|Are 8 and 9 the only consecutive proper powers in ℕ⁺?|29a|NumberTheory.Cyclotomic|C|5058|
|000036|[paper][s1]|Does each elliptic curve over ℚ arise from a weight-two modular form?|97+lifting inputs|EC MF|G|—|
|000045|[4](https://arxiv.org/abs/1408.5110)|Are prime gaps unbounded multiples of the Erdős–Rankin scale?|18 (Maynard)/FGKT ~40a|Siv Pr|C|5499|
|000060|[27](https://doi.org/10.1090/s0894-0347-06-00549-2)|Can distinct moduli in [N,CN] cover almost all integers?|23a|P Siv|C|5498|
|000076|[54][s3]|How sparse can a Ramsey 2-complete set of integers be?|part of 75a|Add As|C|5497|
|000077|[55][s3]|How sparse can a Ramsey r-complete set be for r>2 colors?|part of 75a|Add As|C|5496|
|000078|[58](https://doi.org/10.1016/0012-365x%2892%2990037-g)|Bound chromatic number from the number of distinct odd cycle lengths.|8a|G|C|5495|
|000085|[67](https://www.erdosproblems.com/bibs/Ta16)|Are the sums of any ±1 sequence on finite homogeneous APs unbounded?|29|P Four|C|5494|
|000087|[69](https://arxiv.org/abs/2512.01739)|Is the series Σ ω(n)/2ⁿ irrational?|part of 61a|Siv Div|C|5493|
|000089|[72](https://doi.org/10.1002/jgt.20072)|Can a zero-density cycle-length set meet every graph of large average degree?|17a (Ve05)|G D|C|5492|
|000090|[73](https://www.erdosproblems.com/73)|If α(H)≥(∣H∣−k)/2 for every subgraph H, can Oₖ(1) deletions make G bipartite?|30a|G|C|5491|
|000093|[76](https://arxiv.org/abs/2008.05311)|Guaranteed edge-disjoint monochromatic triangles in a 2-colored Kₙ?|31 (37 incl. app.)|G|N|5490|
|000096|[79](https://arxiv.org/abs/2409.05931)|Characterize minimal graphs whose Ramsey numbers fail to be size-linear.|2|G R|N|5489|
|000104|[88](https://arxiv.org/abs/2208.02874)|How many distinct induced edge counts occur in a C-Ramsey graph?|60a|G P|S|5488|
|000108|[92](https://www.erdosproblems.com/forum/thread/92#post-6542)|Is planar minimum favorite-distance degree nᵒ⁽¹⁾?|~1–2 given unit-distance counterexample|G Geo|S|1492|
|000121|[110](https://arxiv.org/abs/1902.08177)|Uniform size bound on k-chromatic subgraphs in uncountably chromatic graphs?|10m|Ord G|S|5487|
|000126|[118 · ordinal](https://www.erdosproblems.com/latex/118)|Does G→(K₃,K₃) imply G→(Kₙ,Kₙ) for every finite n in infinite graphs?|1 ¶ graph/21 ordinal|G R|N|5486|
|000139|[133](https://doi.org/10.1002/jgt.3190180103)|Minimum Δ in an n-vertex triangle-free graph of diameter ≤2?|14 Füredi–Seress|G As|S|5485|
|000140|[136](https://arxiv.org/abs/2207.02920)|Colors needed in Kₙ if each K₄ uses ≥5 colors?|35m|G R|S|5484|
|000155|[157](https://arxiv.org/abs/2303.09659)|Can triple sums from an infinite Sidon set cover all large integers?|15m|Poly Add|S|5483|
|000161|[163](https://arxiv.org/abs/1505.04773)|Is R(G)=O(n) at bounded degeneracy?|35m|G R|S|5482|
|000163|[166](https://arxiv.org/abs/2306.04007)|Growth of R(4,t) as t→∞?|24m|G R|S|5481|
|000168|[172](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Monochromatic-finite-sums-and-products-in-the-positive-integers-September-23-2026/paper.pdf)|Simultaneous monochromatic finite sums and products in every finite coloring of ℕ⁺?|70m|R dynamics|S|5075|
|000173|[179](https://arxiv.org/abs/1908.09905)|How many short APs can a set avoiding a longer AP contain?|7m|APs Add|S|5480|
|000175|[181](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-hypercube-Ramsey-number-has-linear-order-September-23-2026/paper.pdf)|Is R(Qₙ)=O(2ⁿ) for the hypercube?|172m|G R|S|4967|
|000176|[182](https://arxiv.org/abs/2411.11785)|Maximum edges without a regular subgraph of specified degree?|16m|G P|S|5479|
|000179|[186](https://arxiv.org/abs/2410.14624)|Largest subset of [1,n] with no element the average of some others?|20m|Add As|S|5478|
|000182|[190](https://arxiv.org/abs/2604.20588)|Interval length forcing a monochromatic or rainbow AP of prescribed size?|10m|R P|S|5477|
|000183|[193](https://arxiv.org/abs/2609.01766)|Must an infinite walk in ℝ³ with finite step set visit three collinear points?|2m|Geo|C|1474|
|000192|[207](https://arxiv.org/abs/2201.04554)|Can Steiner triple systems have arbitrarily large girth?|54m|HG P|S|5475|
|000194|[210](https://arxiv.org/abs/1208.4714)|Minimum ordinary-line count for n noncollinear planar points?|72m|Geo Add|S|5474|
|000195|[211 · Beck](https://doi.org/10.1007/bf02579184) [Sz.–Tr.][s4]|How many lines do n planar points determine if at most n−k are collinear?|17 Beck/12 Sz.–Tr.|affine geometry incidences|S|5473|
|000198|[216](https://arxiv.org/abs/2403.00737)|What minimum size forces an empty convex k-gon in planar general position?|3 Horton+23 hexagon+SAT|Conv SAT|G|726|
|000202|[223](https://arxiv.org/abs/0707.0213)|Maximum number of diameter pairs among n points in ℝᵈ?|19–21|G Geo|N|5471|
|000203|[225](https://doi.org/10.1112/jlms/s2-9.1.16)|Is ∫₀²π ∣P(eⁱᵗ)∣dt≤4 for real-rooted P of unit-circle sup norm 1?|≤7|Poly|C|1420|
|000204|[227](https://doi.org/10.1007/BF02807433)|Attainable limits of maximum term / maximum modulus for transcendental entire functions?|≤44|CA series|N|846|
|000205|[232](https://arxiv.org/abs/2207.14179)|Can a measurable 1-avoiding planar set have upper density >1/4?|~18–22|Geo Four|S|5469|
|000208|[235](https://publi.math.unideb.hu/paper/2953)|Continuous limiting law for normalized gaps between primorial totatives?|~9–10|Pr F|C|5468|
|000211|[240](https://www.numdam.org/item/CM_1973__26_3_319_0.pdf)|Can gaps of integers supported on an infinite prime set tend to ∞?|~2–3+deps|Pr Div|C|5467|
|000216|[245](https://www.erdosproblems.com/bibs/Fr73)|For infinite density-zero A, is limsup (A+A)(x)/A(x)≥3?|≤108 Freiman book|Add D|C|1505|
|000242|[284][s5]|Maximal least denominator among k distinct unit fractions summing to 1?|~17 partial result|As F|C|5464|
|000243|[286][s5]|Minimum width of k distinct denominators with reciprocal sum 1?|~17 interval result|Siv F|S|5463|
|000248|[292](https://arxiv.org/abs/math/9811112)|Attainable largest denominators in distinct Egyptian fraction expansions of 1?|~3+lemmas|Pr Div|C|5462|
|000250|[294][s6]|First forbidden least denominator of a distinct Egyptian expansion of 1 with denominators ≤N?|~2+§§2–4 lemmas|Four Pr|N|5461|
|000252|[297](https://arxiv.org/abs/2404.16016)|Count subsets of [1,N] with reciprocal sum 1.|~10–11|Pr As|C|5460|
|000256|[305][s6]|Bound the smallest maximum denominator in a distinct Egyptian expansion of a/b.|~1+§§2–4 lemmas|Four Pr|C|5459|
|000259|[308](https://ecroot.math.gatech.edu/erdos_graham.pdf)|Which integers are sums of distinct reciprocals from 1,1/2,…,1/N?|~10–13|As F|N|1266|
|000264|[318](https://www.erdosproblems.com/318)|Zero signed reciprocal subsum for nonconstant signings of APs, dense sets or squares?|~5–9 squares/≤6 AP article|Pr APs|C|5458|
|000266|[320](https://www.erdosproblems.com/forum/thread/320/proof-claims#proof-claim-55)|Count distinct subsums of 1,1/2,…,1/N.|~3–6 upper/≤12 lower|Pr Div|C|5457|
|000267|[321](https://arxiv.org/abs/2509.10030)|Largest subset of [1,N] whose reciprocal subsums are all distinct?|~8–12+#320 upper bound|Pr F|C|1267|
|000281|[339](https://doi.org/10.1515/crll.2003.055)|Positive lower density of restricted r-fold sums of an order-r basis?|≤22|Add D|C|5456|
|000285|[343][s7]|Do subset sums of positive-lower-density multisets contain an infinite AP?|~4+finite theorem|Add D|N|5455|
|000286|[344][s7]|Does A(N)≥c√N eventually force an infinite AP among finite subset sums?|~4+~24 inputs|APs Add|C|5454|
|000288|[346](https://www.erdosproblems.com/forum/thread/346/proof-claims#proof-claim-59)|Must ratios ≥1+ε in a minimal stably complete sequence converge to φ?|~1,260 words, exposition #5609|As F|C|5609|
|000298|[360][s3]|Colors needed on [1,n−1] to avoid a monochromatic distinct-element sum of n?|~12–20+common lemmas|APs As|C|5453|
|000301|[365](https://www.erdosproblems.com/latex/365)|Can consecutive powerful integers both be nonsquares?|1 ¶|Pr Div|C|1197|
|000307|[372](https://doi.org/10.1556/SSCMATH.38.2001.1-4.3)|Is P(n)>P(n+1)>P(n+2) infinitely often for the largest prime factor P?|≤6|Siv Pr|C|5452|
|000313|[378](https://dms.umontreal.ca/~andrew/PDF/ramare.pdf)|Density of Pascal rows with exactly r squarefree entries?|≤35 incl. lemmas|D|N|2228|
|000314|[380](https://arxiv.org/html/2603.27990)|Density of consecutive products whose largest prime factor repeats?|1 major section+preliminaries|Siv Pr|S|5450|
|000315|[381](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/4E3B60B2BC31651C55D01FFC9ECB4497/S0008414X00053037a.pdf/repartition_des_nombres_hautement_composes_de_ramanujan.pdf)|Estimate the counting function of highly composite numbers.|~15|Pr Div|N|5449|
|000320|[387](https://arxiv.org/html/2605.21221)|Must a binomial coefficient have a divisor close to the upper parameter?|3 major sections+outline|Siv Div|N|5448|
|000331|[402](https://matwbn.icm.edu.pl/ksiazki/aa/aa75/aa7511.pdf)|How small a pairwise gcd must occur in a large finite integer set?|~38|Pr F|C|5446|
|000334|[407](https://arxiv.org/pdf/2308.05162)|Bound the number of representations n=2ᵃ+3ᵇ+2ᶜ3ᵈ.|~38|Pr Div|C|5527|
|000346|[421](https://www.erdosproblems.com/static/421-Pratt.pdf)|Density-one sequence with all contiguous-block products distinct?|~16|Siv Pr|C|5444|
|000356|[437](https://terrytao.wordpress.com/2024/08/09/a-result-of-bui-pratt-zaharescu-and-erdos-problem-437/)|How often can prefix products of an increasing integer sequence be squares?|~2–4|Div As|S|5442|
|000357|[438](https://archive.dimacs.rutgers.edu/TechnicalReports/TechReports/2000/2000-39.ps.gz)|Largest subset of [1,n] in which no two elements sum to a square?|~13|Four D|C|5440|
|000358|[439](https://doi.org/10.1017/S0963548305007169)|Is a monochromatic pair summing to a perfect power forced by any finite coloring?|≤15|Poly Div|C|5438|
|000359|[440](https://www.renyi.hu/~p_erdos/1980-15.pdf)|How often can adjacent terms of an increasing sequence have lcm ≤x?|1 ¶ O(√x)/≤4 sharp|series As|C|2208|
|000360|[441](https://matwbn.icm.edu.pl/ksiazki/aa/aa84/aa8416.pdf)|Largest positive integer set of pairwise lcm ≤x?|~25|Div As|C|5435|
|000361|[444](https://www.renyi.hu/~p_erdos/1980-40.pdf)|How many divisors of one integer can lie in a given infinite set?|≤22+1 ¶|Div As|C|3839|
|000363|[446](https://www.ford126.web.illinois.edu/wwwpapers/hxyz.pdf)|Density of integers having a divisor in (y,2y]?|~60 incl. lemmas|Siv Div|C|5432|
|000364|[449](https://www.erdosproblems.com/forum/thread/449)|What fraction of divisors can be paired with another of comparable size?|1 ¶ given the dyadic occupancy theorem|Div D|C|5431|
|000377|[465](https://www.mathnet.ru/php/getFT.phtml?jrnid=mzm&paperid=691&what=fullt)|Bound planar set size when distances avoid integers by given margins.|≤4|Geo Four|C|5427|
|000378|[466](https://real-j.mtak.hu/5461/1/StudScientMath_11.pdf)|Arbitrarily large planar sets with all distances uniformly away from ℤ?|~5|Geo As|C|5424|
|000383|[471](https://www.erdosproblems.com/forum/thread/471)|Can iterated prime sums of three distinct primes from a finite seed grow forever?|1–2¶+Vinogradov’s theorem|Pr F|C|5419|
|000385|[473](https://www.erdosproblems.com/forum/thread/473)|Is there a permutation of ℕ⁺ whose adjacent sums are prime?|~1+bounded prime gaps and Dirichlet|G Pr|C|5011|
|000388|[477](https://www.erdosproblems.com/forum/thread/477)|Can a polynomial image have a unique-representation additive complement?|~2–3+determinant-method estimates|Poly As|C|5416|
|000391|[482](https://www.impan.pl/shop/en/publication/transaction/download/product/83728)|Can digits from the given floor recurrence represent an algebraic number?|~6 Stoll’s main proof section|Real.sqrt|C|1520|
|000393|[485](https://ems.press/content/serial-article-files/39657?nt=1)|Compare numbers of nonzero coefficients of a polynomial and its square.|~4+cited lemmas|Poly F|S|5445|
|000397|[491](https://www.erdosproblems.com/forum/thread/491)|Are additive functions with bounded first differences close to logarithmic?|≤13|Pr As|C|5443|
|000398|[492](https://users.renyi.hu/~p_erdos/1963-01.pdf)|Equidistribution of scaled integers in sequence gaps when successive ratios tend to 1?|~7+a¶|Meas As|C|5441|
|000399|[494](https://msp.org/pjm/1962/12-1/pjm-v12-n1-p17-s.pdf)|Do the k-element subset sums with multiplicities determine a finite set?|1 ¶ disproof/~2–3+reductions (unique eventually)|Poly F|N|1466|
|000400|[496](https://www.impan.pl/shop/en/publication/transaction/download/product/106367)|Can u²+v² approximate αw² arbitrarily closely for irrational α>0?|~1 ¶+≤11|Quadratic forms|C|1684|
|000402|[501](https://drive.google.com/file/d/12f4eP2EJQO7tYGHXkFyPjNcjWfkvm1lF/view)|Do outer-measure bounds on a set mapping force a free set of the given size?|8m|forcing Card|C|5437|
|000404|[504](https://www.erdosproblems.com/504)|Largest angle forced among n planar points?|≤4a|Conv Geo|E|5592|
|000410|[511](https://arxiv.org/html/2509.11597)|Bound the number of large-diameter components of {∣P∣≤1}.|~3–6 of argument|Poly Top|C|5436|
|000413|[515](https://www.erdosproblems.com/515)|Path to ∞ integrating ∣f∣⁻λ for all λ>0 for transcendental entire f?|≤11a|Meas|C|5434|
|000415|[518](https://arxiv.org/html/2409.03623)|For an edge-colored Kₙ, how few paths of one color cover its vertices?|~8–15|G F|C|5433|
|000419|[523](https://www.erdosproblems.com/523)|Typical maximum modulus on the unit circle of a random sign polynomial?|≤9a|P Poly|C|5430|
|000421|[525](https://www.erdosproblems.com/525)|Typical minimum modulus on the unit circle of a random sign polynomial?|≤46a|P Poly|C|5429|
|000422|[526](https://www.erdosproblems.com/526)|Which random arc lengths give almost-sure full circle coverage?|≤18a|Geo P|C|5428|
|000423|[527](https://arxiv.org/html/2509.02729)|Does a random-sign power series converge somewhere on the unit circle?|~15–30 incl. lemmas|P series|C|5425|
|000428|[534](https://doi.org/10.4064/aa-75-3-259-276)|Largest pairwise noncoprime subset of [1,n] containing a prescribed integer?|≤18a|Pr F|C|5422|
|000433|[542](https://www.erdosproblems.com/542)|How large is Σ1/a for A⊆[1,n] with pairwise lcm >n?|≤9a|F|C|5420|
|000434|[543](https://github.com/QuanyuTang/erdos-problem-543/blob/main/On_Erdos_Problem_543_Revised_and_Verified.pdf)|In abelian G of order N, do log₂N+o(log log N) random elements' subset sums cover G with probability ≥½?|10m|Grp P|C|5417|
|000437|[546](https://www.erdosproblems.com/546)|Is R(G)≤2^(C√m) for m edges and no isolated vertices?|≤9a|G R|C|5414|
|000440|[549](https://arxiv.org/html/1605.03612)|Ramsey number of a tree with bipartition sizes k and 2k?|~4–8 lower|G R|C|5412|
|000444|[553](https://doi.org/10.1007/s00493-005-0011-9)|Growth of the three-color clique Ramsey number R(3,3,n)?|≤17a|G R|C|5411|
|000450|[559](https://www.erdosproblems.com/559)|Do bounded-degree graphs have linear size-Ramsey numbers?|≤6a|G R|C|5410|
|000455|[565](https://arxiv.org/html/2509.22629)|Is the induced Ramsey number at most exponential in graph order?|~40–70|HG G|C|5408|
|000460|[570](https://arxiv.org/html/2601.10238)|Bound R(Cₖ,H) in terms of k and the edge count of H.|~8–15 new odd-cycle cases|G R|C|5406|
|000464|[574](https://doi.org/10.1006/jctb.1994.1020)|Extremal edge count forbidding odd and even cycles of adjacent lengths?|≤6a|G As|C|5404|
|000465|[575](https://cdn.openai.com/pdf/ten-proofs-oai.pdf)|Is a bipartite-containing forbidden family's extremal number comparable to one member's?|1 ¶ literal/~5 stronger cyclic version|G Geo|C|1528|
|000467|[577](https://doi.org/10.1007/s00373-010-0948-3)|Which minimum degree forces a spanning C₄-factor?|≤45a|G F|C|5398|
|000468|[578](https://doi.org/10.1017/s0963548399004150)|When does G(2ᵈ,p) contain a spanning hypercube with high probability?|≤24a|G P|C|5395|
|000471|[581](https://doi.org/10.1007/bf01261315)|Largest guaranteed bipartite subgraph of a triangle-free graph with m edges?|≤11a|G P|C|5392|
|000475|[586](https://www.erdosproblems.com/586)|Can finite covering congruences have pairwise nondividing moduli?|≤38a|P Siv|C|5390|
|000476|[587](https://doi.org/10.1007/978-3-642-14444-8_14)|Largest subset of [1,n] with no square among its nonempty subset sums?|≤34a|APs Add|C|5388|
|000479|[591](https://www.erdosproblems.com/591)|Does ω^(ω²) → (ω^(ω²),3)² hold?|≤21a|Ord R|C|5386|
|000486|[599](https://doi.org/10.1007/s00222-008-0157-3)|Infinite A–B Menger theorem with a separator choosing one vertex per path.|≤62a|Card G|C|5426|
|000490|[603](https://www.erdosproblems.com/603)|Uniform color bound for countable-edge families with intersections never of size two?|1 proof¶+Erdős–Rado theorem|Card R|C|5423|
|000492|[605](https://doi.org/10.1080/00029890.1989.11972243)|Can n spherical points determine superlinearly many equal-distance pairs?|≤7a|Geo As|C|5418|
|000493|[606](https://doi.org/10.4153/cmb-1988-020-2)|Which line counts are attainable by n planar points?|≤10a|Geo F|C|5415|
|000494|[607][s4]|Count possible sets of line multiplicities for n planar points.|≤12a|Geo As|C|5413|
|000503|[622](https://arxiv.org/abs/2503.01826v2)|Count cycle vertex sets of (n+1)-regular graphs on 2n vertices.|14–15|G P|C|5409|
|000506|[625](https://arxiv.org/abs/2608.30604v2)|How far below χ is the cochromatic number of G(n,1/2)?|~30|G P|C|5596|
|000511|[630](https://web.math.princeton.edu/~nalon/PDFS/chrom3.pdf)|Is every planar bipartite graph 3-choosable?|~7–8|G Poly|N|4712|
|000512|[631](https://doi.org/10.1006/jctb.1994.1062)|Find the optimal list size for coloring planar graphs.|~4–7|G|N|922|
|000513|[632](https://arxiv.org/abs/1806.03880v2)|Does multiplying list and demand sizes preserve multichoosability?|~7|G F|C|5399|
|000514|[633](https://arxiv.org/abs/2604.03609v4)|Which triangles can be dissected into congruent triangles only when their number is a square?|~20|Geo|C|5396|
|000517|[636](https://arxiv.org/abs/1712.05656)|How many induced (order,size) pairs in a C-Ramsey graph?|~20|G P|C|5393|
|000518|[637](https://people.math.ethz.ch/~sudakovb/distinct-degrees.pdf)|How many distinct degrees can a large induced subgraph of a Ramsey graph attain?|~5|Conv G|C|5391|
|000521|[641](https://arxiv.org/abs/2410.02437)|Does high chromatic number force edge-disjoint cycles on the same vertices?|~3|G|C|5389|
|000527|[651](https://arxiv.org/abs/2208.04878v1)|For fixed d≥3, can the convex-position threshold ES_d(n) grow exponentially in n?|~11–13|Conv Geo|N|5385|
|000528|[652](https://arxiv.org/abs/1912.01883)|Bound the kth smallest pinned distinct-distance count among n planar points.|~5|Geo|C|5383|
|000532|[656](https://arxiv.org/abs/2206.12377)|Can one translate all distinct pair sums of infinite B⊆A into A of positive density?|~12|Meas Top|C|5381|
|000539|[664][s8]|Can partial designs have transversals with bounded intersection per block?|~1.5|P F|C|5378|
|000547|[673](https://users.renyi.hu/~p_erdos/1982-33.pdf)|Does the sum of adjacent divisor ratios diverge on a density-one set?|~1 for divergence|P Pr|C|5377|
|000554|[682](https://arxiv.org/abs/2508.06463)|Rough integer in every prime gap, with least prime factor ≥ gap length? Density one is proved.|1 ¶ universal/~6 density one|Siv Pr|N|1116|
|000562|[690](https://arxiv.org/abs/2501.10333)|Are the limiting prime-factor densities at the kth ordered position unimodal?|~1–2+exact computations|Pr F|N|4526|
|000568|[697](https://doi.org/10.1016/0022-314X%2892%2990096-8)|Find the density threshold for divisors ≡1 mod m below exp(mᵅ).|≤7a|Div D|C|5371|
|000572|[702](https://doi.org/10.1017/S0004972700025521)|When must two k-sets in a uniform family meet in exactly one point?|~9|F|C|5369|
|000573|[703](https://doi.org/10.1090/S0002-9947-1987-0871675-6)|Largest family of subsets avoiding an intersection of size r?|~7 fixed r/~5–7 more via Long for bulk|P F|N|5366|
|000575|[705](https://www.erdosproblems.com/705)|Is girth bounded in 4-chromatic unit-distance graphs in ℝ²?|~20a|G Geo|C|5364|
|000584|[715](https://www.mathnet.ru/eng/mzm5870)|Does every simple 4-regular graph contain a 3-regular subgraph?|~21 Russian|G|C|5362|
|000585|[717](https://arxiv.org/abs/1107.1920)|Relate chromatic number to the largest complete subdivision on n vertices.|~9–11|G R|C|1686|
|000586|[718](https://doi.org/10.1017/S096354830000184X)|What average degree forces a subdivision of Kᵣ?|~4 via Bollobás–Thomason (1998)/12a in the bank-listed Komlós–Szemerédi proof|G F|C|5403|
|000588|[720](https://doi.org/10.1002/jgt.3190070115)|Growth of the size-Ramsey numbers of paths and cycles?|~11–12 via a common proof|G P|C|5400|
|000589|[721 · upper](https://arxiv.org/abs/2006.02877) [lower](https://arxiv.org/abs/2111.01099) [Roth](https://arxiv.org/abs/2309.02353)|Bound W(3,k), forcing a red 3-AP or a blue k-AP.|24 lower/8 historical upper+Roth|P Four|C|5397|
|000590|[722](https://arxiv.org/abs/1401.3665)|Do divisibility tests suffice for large Steiner systems?|~50|HG P|C|5394|
|000598|[730](https://www.overleaf.com/read/gpttrsmhbhbk#a7cfdf)|Equal prime supports for distinct central binomial coefficients?|~1,800 words of reconstructed proof notes|Div|C|5387|
|000600|[732][s8]|Which block-size lists admit a pairwise balanced design of index 1?|~1–2 the two counting bounds|As F|N|5384|
|000601|[733](https://trotter.math.gatech.edu/papers/38.pdf)|Count feasible sorted line-size lists for n planar points.|~2+~7 of incidence machinery|Geo As|C|5382|
|000603|[735](https://math.haifa.ac.il/ackerman/publications/magic-socg07.pdf)|Which planar sets admit positive weights giving each determined line equal mass?|~9|Geo|C|5380|
|000605|[737](https://doi.org/10.1007/BF02579349)|In an uncountably chromatic graph, ∃ edge e, ∀ large n, ∃ n-cycle through e.|≤2|Ord Card|C|1615|
|000612|[744](https://www.sciencedirect.com/science/article/pii/0095895685900668)|How many edges must be deleted from a chromatic-critical graph to make it bipartite?|≤10|G F|C|5376|
|000613|[745](https://escholarship.org/content/qt5s77j58b/qt5s77j58b_noSplash_2827d3aa70ed7a526db5fb6e9bf213b0.pdf)|Limiting size of the second-largest component in the random graph critical window?|~10|G P|C|5374|
|000614|[746](https://www.sciencedirect.com/science/article/pii/0012365X83900213)|Hamiltonicity threshold in G(n,m)?|≤9|G P|C|5372|
|000615|[747](https://arxiv.org/pdf/1909.06834)|Perfect-matching threshold in a random 3-uniform hypergraph?|~24|G P|C|5370|
|000616|[748](https://arxiv.org/pdf/math/0304058)|How many sum-free subsets does [1,n] have?|~10|Four Add|C|5368|
|000619|[752](https://arxiv.org/pdf/0707.2117)|How many cycle lengths are forced by a minimum degree and girth bound?|~3|G|C|5367|
|000620|[754](https://arxiv.org/pdf/1108.4817)|Largest minimum favorite-distance degree among n points in ℝ⁴?|~1–2+unit-distance bound|G Geo|N|1647|
|000622|[758](https://www.erdosproblems.com/758)|Maximum cochromatic number z(n) for each 1≤n≤19?|6 Gimbel+enumeration at 12¹|G Col|N|5363|
|000623|[759](https://citeseerx.ist.psu.edu/document?doi=0dc3be9d7387f7334e4c66f6588310d70fcf8115&repid=rep1&type=pdf)|How does the minimum number of clique or independent-set parts for graphs on a surface grow with the surface's complexity?|~1+deps|G Geo|C|5361|
|000625|[763](https://upload.wikimedia.org/wikipedia/commons/b/b7/On_a_problem_of_additive_number_theory%2C_by_P._Erdos%2C_H._W._J._Fuchs.pdf)|Can cumulative two-term additive representation counts grow linearly with bounded error?|~5–9|Four Add|C|5360|
|000626|[764](https://pure.psu.edu/en/publications/on-the-addition-of-sequences-of-integers/)|Can cumulative three-term additive representation counts grow linearly with bounded error?|~8|Four Add|C|5359|
|000628|[767](https://onlinelibrary.wiley.com/doi/10.1002/jgt.10179)|How many edges can a graph have if no vertex of a cycle is incident to several specified chords?|≤3|G F|C|5358|
|000632|[771](https://web.math.princeton.edu/~nalon/PDFS/Publications/On%20sums%20of%20subsets%20of%20a%20set%20of%20integers.pdf)|How large a subset of an arbitrary finite integer set can have every subset sum avoid a given target?|~3+~2 of lemmas|Add As|C|5357|
|000633|[772](https://web.math.princeton.edu/~nalon/PDFS/Publications2/An%20application%20of%20graph%20theory%20to%20additive%20number%20theory.pdf)|If two-term representation counts are bounded, how large a Sidon subset is guaranteed?|~1|P Add|C|5356|
|000637|[777](https://web.math.princeton.edu/~nalon/PDFS/compairs4.pdf)|How many edges can the containment graph of a set family have?|~7 first question+separate arguments|G As|C|5355|
|000640|[780](https://web.math.princeton.edu/~nalon/PDFS/Publications/The%20chromatic%20number%20of%20Kneser%20hypergraphs.pdf)|What size of a multicolored uniform hypergraph forces a given number of disjoint edges of one color?|~8 with deps|Top F|C|5354|
|000641|[781](https://web.math.princeton.edu/~nalon/PDFS/Publications1/Ascending%20waves.pdf)|Exact 2-color threshold for a fixed-length monochromatic increasing sequence with nonincreasing gaps. Is the quadratic prediction correct?|~6|P Add|C|1687|
|000643|[783](https://terrytao.wordpress.com/wp-content/uploads/2026/02/erdos783-3.pdf)|Maximal multiples density of coprime sets with bounded reciprocal sum?|~7+Hildebrand's prime case|Pr As|C|1687|
|000644|[784](https://arxiv.org/abs/2310.13038)|Bound the density avoiding all multiples of A given its reciprocal sum.|~3+~20 of sieve input|Div As|C|5352|
|000653|[795](https://arxiv.org/pdf/2501.02695)|Largest subset of [1,n] with distinct subset products?|~11|G Pr|C|5347|
|000655|[797](https://web.math.princeton.edu/~nalon/PDFS/Publications2/Acyclic%20colouring%20of%20graphs.pdf)|Acyclic chromatic number of graphs of maximum degree Δ?|~5|G P|C|5345|
|000656|[799](https://web.math.princeton.edu/~nalon/PDFS/colaks9.pdf)|Is the list chromatic number of a random graph sublinear?|~10|G P|C|5343|
|000657|[800](https://web.math.princeton.edu/~nalon/PDFS/rams.pdf)|Is R(G) linear in order if its high-degree vertices are independent?|~3+Ramsey lemma|G F|C|5340|
|000658|[801](https://web.math.princeton.edu/~nalon/PDFS/indrams1.pdf)|Does small independence number force a small dense subgraph?|~2+independence lemma|G P|C|5337|
|000660|[803](https://web.math.princeton.edu/~nalon/PDFS/extremalII1.pdf)|Must a dense graph contain a dense subgraph with comparable degrees?|~3|G P|C|5334|
|000661|[804](https://web.math.princeton.edu/~nalon/PDFS/erdoshajnal4.pdf)|Bound independence number from local independence numbers.|~4–6|G P|C|5332|
|000663|[806](https://web.math.princeton.edu/~nalon/PDFS/dkakeya2.pdf)|Can each A⊆[1,n] of size ≤√n lie in B+B with ∣B∣=o(√n)?|~2+~2 of universal-set tools|Add As|C|2540|
|000664|[807](https://web.math.princeton.edu/~nalon/PDFS/biclique4.pdf)|Typical biclique partition number in G(n,1/2)?|~5|G P|C|5328|
|000665|[808](https://arxiv.org/pdf/1802.06405)|How small can sum and product sets both be along edges of a dense integer graph?|~1–2 counterexample|G Div|C|1687|
|000671|[814](https://arxiv.org/pdf/1705.09979)|Which edge count forces a small subgraph of minimum degree k?|~29|G F|C|5324|
|000672|[815](https://arxiv.org/pdf/1408.5289)|Must large degree-3-critical graphs contain every prescribed cycle length?|~5|G|C|5351|
|000673|[816](https://arxiv.org/pdf/2503.19569)|In dense odd-order graphs, must a 3-edge path have equal-degree endpoints?|~4 via Liu–Zeng/~9 via Chen–Ma|G F|C|5349|
|000678|[822](https://arxiv.org/pdf/2306.16035)|Does {n+φ(n)} have positive lower density?|~10|Meas As|C|5348|
|000679|[823](https://www.pollack-math.net/preimages-maier3.pdf)|Are ratios m/n with σ(m)=σ(n) dense in ℝ⁺?|~3+bounded-gap prime machinery|Top Pr|C|5346|
|000688|[832](https://web.math.princeton.edu/~nalon/PDFS/Publications/Hypergraphs%20with%20high%20chromatic%20number.pdf)|Minimum edges of a uniform hypergraph of specified chromatic number?|~2+Turán design bound|P As|C|5339|
|000689|[833](https://users.renyi.hu/~p_erdos/1975-34.pdf)|Must a 3-chromatic r-graph have maximum degree exponential in r?|~1–2|P F|C|1542|
|000690|[834](https://arxiv.org/pdf/2512.24850)|Can a critically 3-chromatic 3-uniform hypergraph have minimum degree ≥7?|~4 or shorter via a checked finite certificate|F|C|5336|
|000698|[842](https://doi.org/10.1016/0012-365X%2892%2990588-7)|Is a Hamilton cycle together with disjoint triangles always 3-colorable?|~3|G Poly|C|1325|
|000699|[843](https://arxiv.org/pdf/2104.14766)|Do monochromatic distinct-square sums in every 2-coloring cover all large integers?|~10–20 including supporting lemmas|P Add|C|5321|
|000704|[851](https://www.erdosproblems.com/forum/discuss/851)|Can 2ᵃ plus an almost-prime represent a density-one set?|~5–15|Siv Div|C|5317|
|000711|[858](https://www.ulam.ai/research/erdos858-asymptotic.pdf)|Bound reciprocal sums under the prescribed prime-divisibility exclusions.|~8|Pr F|C|5310|
|000714|[861](https://arxiv.org/pdf/1204.6595)|Count Sidon subsets of [1,n].|~13 sharper bounds|Add As|S|5307|
|000715|[863](https://boonsuan.github.io/erdos863.pdf)|Compare maximal sizes under bounded sum vs. difference multiplicities.|~7|As F|C|1545|
|000720|[869](https://arxiv.org/pdf/2603.03472)|Does the union of two disjoint order-two bases contain a minimal such basis?|~5|Add As|C|5299|
|000725|[874](https://www.numdam.org/item/AST_1999__258__141_0.pdf)|Largest A⊆[1,n] avoiding equal subset sums of unequal lengths?|~7+prior structure theorem|APs Add|S|5289|
|000728|[877](https://arxiv.org/pdf/1502.07605)|Count maximal sum-free subsets of [1,n].|~17+deps|As F|S|5285|
|000731|[880](https://www.cmls.polytechnique.fr/perso/plagne/Erdos-Burr.pdf)|Does the restricted sumset of an additive basis have bounded gaps?|~2–3|Add As|C|1222|
|000733|[882](https://doi.org/10.1016/S0012-365X%2898%2900385-9)|Largest A⊆[1,n] with subset sums avoiding the given divisibilities?|~1–3 leading asymptotic|F|S|5283|
|000745|[894](https://arxiv.org/pdf/0706.0223)|Can a finite coloring avoid same-color differences in a given sparse set?|~3–5|G P|C|1271|
|000746|[895](https://www.erdosproblems.com/895)|Must every triangle-free graph on the integers contain independent x,y,x+y?|1 ¶+SAT on [1,18]|SAT G|C|5270|
|000747|[896](https://www.ulam.ai/research/erdos896.pdf)|Bound the number of uniquely represented products from two integer sets.|~5+Ford's estimates|P Pr|C|5268|
|000748|[900](https://doi.org/10.1007/BF02579172)|How long a path occurs just above the random-graph giant-component threshold?|~8–11|G P|C|1688|
|000751|[903](https://users.renyi.hu/~p_erdos/1985-22.pdf)|Gaps in block counts of pairwise balanced designs near projective planes?|~2–3|F|C|5264|
|000753|[908](https://doi.org/10.1007/BF01896840)|Measurable differences: decompose f into measurable, additive and a.e.-zero-increment parts.|19a|Meas|S|5261|
|000754|[909](https://www.jstor.org/stable/2035444)|Can a space and its square have the same positive finite dimension?|≤5a|Geo Top|C|5259|
|000755|[910](https://bibliotekanauki.pl/articles/1382985.pdf)|Which distinct connected homeomorphism types must a connected Euclidean set contain?|~10a|Top|E|5344|
|000759|[915](https://doi.org/10.1007/BF02018594)|Which edge count forces k internally disjoint paths with common endpoints?|≤4a|G|C|5341|
|000760|[916](https://doi.org/10.1007/BF01238666)|Does linear edge density force a cycle with an outside vertex adjacent to three cycle vertices?|~4 original/~4–7 alternate|G|C|5338|
|000764|[920](https://arxiv.org/pdf/2605.28793v3)|Largest χ of a Kᵣ-free n-vertex graph?|~½ reduction/≥20 of Ramsey input|G R|C|5335|
|000765|[921](https://trotter.math.gatech.edu/papers/45.pdf)|Largest odd girth given graph order and chromatic number?|~1–3+lower-bound construction|G As|C|5331|
|000766|[922](https://arxiv.org/pdf/1907.11429v2)|Do nearly half-size independent sets in finite subgraphs bound chromatic number?|~4–5|G|C|5329|
|000767|[924](https://www.sciencedirect.com/science/article/pii/0095895676900150)|Can a Kₛ-free graph force a smaller monochromatic clique in every r-edge-coloring?|≤7+specialization|G R|C|5325|
|000768|[925](https://web.math.princeton.edu/~nalon/PDFS/arodl4.pdf)|Does a triangle-avoiding edge 2-coloring force a large independent set?|~6|G P|C|1388|
|000769|[926](https://people.math.ethz.ch/~sudakovb/bipartite-turan-numbers.pdf)|Bound edges excluding the given complete subdivision with a common center.|~3–5+lower-bound construction|G Geo|C|5320|
|000782|[941](https://www.impan.pl/shop/en/publication/transaction/download/product/83021)|Are all large integers sums of three positive powerful integers?|~2 §5/~18 with inputs|Pr Div|E|5316|
|000787|[946](https://msp.org/pjm/1987/129-2/pjm-v129-n2-p06-p.pdf)|Is τ(n)=τ(n+1) infinitely often?|~12|Siv Pr|C|1389|
|000788|[948](https://www.erdosproblems.com/forum/discuss/948)|Can subset sums of a sparse sequence omit a color in any finite coloring?|~2–5|F|C|5311|
|000797|[957](https://adriandumitrescu.org/product-ineq.pdf)|Bound the product of shortest- and longest-distance multiplicities.|~10–11|Conv G|C|5308|
|000799|[960](https://arxiv.org/pdf/2604.06609)|Do many two-point lines force a large subset with all joins ordinary?|~5–6+elliptic-curve facts|EC G|C|5305|
|000810|[977](https://arxiv.org/abs/1008.1274)|How fast can the largest prime factor of 2ⁿ−1 grow relative to n?|12|Poly Pr|C|5303|
|000813|[980](https://doi.org/10.4064/aa-13-2-131-149)|Average least kth-power nonresidue over primes?|19+corrigendum|Pr As|N|5301|
|000814|[981](https://doi.org/10.1016/1385-7258%2869%2990006-7)|Average initial interval for quadratic residues and nonresidues to balance?|8a|Siv As|C|5298|
|000817|[984](https://www.erdosproblems.com/forum/thread/984#post-37)|Can monochromatic APs starting at a all have length Oε(aᵋ) in a 2-coloring?|~1+a major input|APs As|C|5295|
|000819|[986](https://arxiv.org/abs/2605.28793v3)|Lower bounds on R(s,t) as t grows with s fixed?|9+external inputs|G R|C|5293|
|000821|[988](https://doi.org/10.1007/BF01418774)|Is spherical cap discrepancy unbounded as the number of points grows?|~8+parallel argument|Geo Meas|C|5288|
|000822|[989](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6400-11511_2006_Article_BF02392553.pdf)|Minimal disk counting discrepancy of an infinite discrete planar set?|~30|Geo Four|S|5286|
|000824|[991](https://arxiv.org/abs/1907.04814)|Do spherical maximizers of the distance product equidistribute?|~22|Geo Meas|C|5281|
|000825|[992](https://doi.org/10.1112/jlms/50.3.454)|Discrepancy of {αaₙ} for almost every α?|11a|P Four|C|1395|
|000827|[994](https://doi.org/10.1112/plms/s3-21.3.540)|Does an irrational rotation visit a measurable set with frequency its measure?|17a|Meas dynamics|C|1444|
|000831|[998](https://doi.org/10.4064/aa-12-2-193-212)|Which interval lengths give bounded discrepancy under irrational rotation?|20a|AddCircle|S|5277|
|000832|[999](https://arxiv.org/abs/1907.04593)|Almost-everywhere criterion for reduced rational approximation with variable error?|~40–45|Meas Pr|C|5275|
|000833|[1001](https://doi.org/10.4064/aa125-2-3)|Limiting measure of Farey approximation intervals over a denominator range?|~10|Meas|N|5273|
|000837|[1005](https://arxiv.org/abs/2607.23302v1)|Maximum length of a Farey run with numerators and denominators co-monotone?|~14|As|C|5271|
|000838|[1006](https://www.researchgate.net/publication/239285245_On_a_probabilistic_graph-theoretical_method)|Does every girth-≥5 graph admit an acyclic orientation with no dependent arc?|5a|G P|C|5269|
|000839|[1009](https://www.erdosproblems.com/forum/thread/1009)|Edge-disjoint triangles forced above the bipartite Turán threshold?|10 ch.|G|C|5266|
|000840|[1010](https://www.renyi.hu/~miki/LovSimBirk.pdf)|Minimum triangle count above the bipartite Turán threshold?|~35 via the sequel|G F|C|5263|
|000842|[1012](https://doi.org/10.1112/plms/s3-24.4.739)|Which edge density forces a cycle covering almost all vertices?|17a|G|C|5258|
|000845|[1015](https://www.renyi.hu/~p_erdos/1975-35.pdf)|Fewest vertices left by disjoint monochromatic cliques in a colored Kₙ?|~2+lemmas|G R|C|1553|
|000848|[1018](https://doi.org/10.1007/BF02122555)|Does superlinear edge count force a bounded-order nonplanar subgraph?|4+standard planarity fact|G|C|5256|
|000849|[1019](https://www.erdosproblems.com/forum/thread/1019)|Do ⌊n²/4⌋+⌊(n+1)/2⌋ edges force a triangulation on >3 vertices?|~1,875 words, exposition #5594|G|N|5594|
|000851|[1021](https://arxiv.org/abs/1809.00468)|Maximum edges excluding the 1-subdivision of a fixed clique?|~4|G As|C|5252|
|000852|[1024](https://combinatorialpress.com/ars/vol21/)|Bound the independence number of a linear 3-uniform hypergraph.|6a|HG P|C|5251|
|000853|[1025](https://arxiv.org/abs/1507.00547)|Bound free-set size for the given set mapping on pairs.|~2+lower-bound argument|HG P|C|5327|
|000854|[1027](https://www.erdosproblems.com/forum/thread/1027#post-661)|Count subsets meeting every hyperedge and containing none in full.|~1–2+Beck’s theorem|HG G|C|5544|
|000857|[1031](https://doi.org/10.1006/jcta.1999.2972)|Does a Ramsey graph have a nontrivial regular induced subgraph?|6a|G R|C|5323|
|000865|[1042](https://arxiv.org/abs/2312.13673)|Bound polynomial sublevel components by transfinite diameter of the zero set.|~8+inputs|Poly|C|5319|
|000868|[1046](https://doi.org/10.1307/mmj/1028998227)|Must connected {∣P∣≤1} for monic P fit inside a radius-two disk?|5a|Poly|C|5315|
|000870|[1050](https://www.cecm.sfu.ca/~pborwein/PAPERS/P59.pdf)|Is Σ 1/(2ⁿ−3) irrational?|~4|F|C|1221|
|000878|[1058](https://doi.org/10.1090/S0025-5718-00-01178-9)|Can n!+1 have only the next two primes as factors infinitely often?|4a|Pr|C|5312|
|000884|[1064](https://www.impan.pl/shop/publication/transaction/download/product/87975)|Compare φ(n) and φ(n−φ(n)).|20a|Pr Div|C|1956|
|000888|[1069](https://doi.org/10.1007/BF02579194)|Bound the number of k-rich lines among n planar points.|~8|Geo As|C|5306|
|000895|[1076 · Glock](https://doi.org/10.1112/blms.12224)|Forbidding k−2 triples on ≤k vertices gives (1/5+o(1))n² at k=5, refuting universal 1/6.|6 Glock|HG designs|S|1562|
|000896|[1078](https://page.mi.fu-berlin.de/szabo/PDF/oddtransversal.pdf)|Minimum degree forcing a transversal clique in a balanced multipartite graph?|~17+even-case input|G|C|5302|
|000897|[1079](https://doi.org/10.1016/S0095-8956%2881%2980016-0)|At Turán density, must some vertex neighborhood induce many edges?|4|G|C|5300|
|000898|[1081](https://www.impan.pl/shop/publication/transaction/download/product/103069)|Asymptotic count of sums of two powerful numbers?|17 disproof|As|C|5297|
|000900|[1083](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-higher-dimensional-Erdos-distinct-distances-conjecture-September-23-2026/paper.pdf)|Minimum distinct distances among n points in fixed higher dimension?|~100|Geo Poly|C|4994|
|000906|[1089](https://arxiv.org/abs/2601.22401)|How many points in fixed dimension force k distinct distances?|~2–3+upper bound/≤8–9 total|Geo Poly|C|5294|
|000907|[1091](https://www.sciencedirect.com/science/article/pii/0095895682900041)|Must a 4-chromatic graph contain an odd cycle with prescribed chords?|~7 counterexample/≤22 more positive|G|N|5113|
|000912|[1099](https://www.sciencedirect.com/science/article/pii/0022314X84901070)|Bound sums of powers of consecutive-divisor ratios minus one.|≤6 Vose or ~14–17 for Tenenbaum|Div As|C|5290|
|000916|[1105](https://arxiv.org/abs/2102.00807)|Most edge colors avoiding a given rainbow path or cycle?|~7–8 paths/≤12 for cycles|G F|C|5287|
|000925|[1114](https://www.erdosproblems.com/bibs/Ba60b)|Are gaps of critical points monotone for polynomials with equally spaced roots?|≤8|Poly F|C|5284|
|000926|[1115](https://www.mathnet.ru/eng/sm2401)|Shortest escape path for a transcendental entire function?|~7 both counterexamples|CA|C|1565|
|000927|[1116](https://www.acadsci.fi/mathematica/Vol02/vol02pp565-572.pdf)|Extremal value-count ratios for the specified meromorphic functions?|~3–7|CA As|C|5282|
|000929|[1118](https://www.mathnet.ru/eng/smj3876)|Growth of an entire function with a finite-area superlevel set?|~6|CA Meas|C|5280|
|000930|[1119](https://home.iitk.ac.in/~krashu/efwso.pdf)|Size of a family of entire functions with restricted pointwise ranges?|~1 for positive model+~15–24 for countermodel|forcing CA|C|5278|
|000933|[1123 · CH](https://doi.org/10.1090/S0002-9947-1984-0748847-1) [OCA+MA](https://doi.org/10.1090/memo/0702) [model](https://shelah.logic.at/papers/153/)|Is ℘(ℕ) modulo natural-density zero isomorphic to its log-density analogue?|~10–15 CH+Farah/forcing|Boolean algebras forcing|C|5614|
|000934|[1124](https://doi.org/10.1515/crll.1990.404.77)|Can equal-area squares and disks be finitely equidecomposed?|~25–40|Geo Meas|C|5274|
|000935|[1127](https://doi.org/10.1017/s0305004100067426)|Countable Euclidean coloring with all pairwise distances distinct in each color?|≤5 Kunen direction/a¶ for converse|Geo|N|5272|
|000936|[1129][s9]|Which interpolation nodes minimize the Lebesgue constant?|~10–15|Poly|C|5267|
|000937|[1130][s9]|Which nodes maximize the smallest local Lebesgue maximum?|~10–15|Poly As|C|1566|
|000945|[1140](https://rms.unibuc.ro/bulletin/pdf/53-3/GicaEpure.pdf)|Can n−2x² be prime for every permitted smaller square?|~4+class-number theorems|Pr|C|5262|
|000952|[1147](https://arxiv.org/abs/1504.02410)|For irrational α, do integers with αn² close to ℤ form a basis of order two?|~3–5 √2/~10–14 incl. metric generalization|Meas D|C|5257|
|000954|[1149](https://arxiv.org/abs/1611.08044)|Density of n coprime to ⌊nᶜ⌋ for fixed nonintegral c?|~20–23|Pr D|C|5255|
|000958|[1153](https://arxiv.org/abs/2603.21453)|Logarithmic lower bound on interpolation amplification on every fixed subinterval?|~30–35|CA Poly|C|5253|
|000966|[1161](https://arxiv.org/abs/2510.11698)|Most frequent element order in Sₙ?|~6–7|P As|N|4695|
|000969|[1164](https://doi.org/10.4007/annals.2004.160.433)|Growth of the centered disk covered by a planar random walk?|~4–6 §5+inputs|P|N|5250|
|000970|[1165](https://arxiv.org/abs/2409.00995)|Probability of a tie for favorite site of planar random walk?|~19–25|P As|C|5249|
|000971|[1166](https://www.erdosproblems.com/1166)|Count distinct past favorite sites of planar random walk.|<1+two results|P As|C|5248|
|000984|[1179](https://users.renyi.hu/~p_erdos/1976-34.pdf)|Random subset sums needed for near-uniform counts on a finite abelian group?|~6–7|P Add|C|5247|
|000985|[1180](https://doi.org/10.1007/s00013-002-8269-2)|Can boundedly many sums of modular inverses of small integers cover ℤ/p?|≤4 original proof/≤12 for improvement|Add|C|5246|
|000990|[1185](https://www.erdosproblems.com/bibs/Fu81)|Long APs in dense sets with step in a prescribed difference set?|~2+recurrence-to-density conversion|dynamics APs|C|5245|
|000992|[1187](https://doi.org/10.4007/annals.2008.167.481)|Monochromatic APs in primes, or with prime step, under finite coloring?|~1 ¶+Green–Tao/~55–67 including that theorem|Pr APs|C|5244|
|001000|[1195](https://boonsuan.github.io/erdos1195.pdf)|Growth of measurable sets avoiding integer ratios between distinct elements?|~5–7 both variants|Meas|C|5243|
|001003|[1198](https://www.sciencedirect.com/science/article/pii/0097316595900292)|Monochromatic sums of products over disjoint blocks of an infinite set in a 2-coloring?|few lines+18 Smith|R F|C|5242|
|001007|[1202](https://www.overleaf.com/read/qyhdmrchqnvb#5e76b8)|Can deleting (p−1)/2 classes at k small primes always leave ≤εn in [1,n]?|~1–2+prime counts|Pr As|C|5241|
|001010|[1205](https://www.erdosproblems.com/1205)|Maximum uniform coverage of [1,x] with one class per modulus ≤x?|~1–2|P As|C|5240|
|001016|[1211](https://arxiv.org/abs/2105.15195)|In every 2-partition of ℕ⁺, do one cell's finite sums have lower log density ≥c>0?|<1 for counterexample|As F|C|5239|
|001018|[1213](https://doi.org/10.1007/BF01949064)|Do increasing integer sequences of bounded gaps force equal sums on distinct contiguous blocks?|~1–2|F|C|1622|
|001019|[1214](https://blogs.mat.ucm.es/ccorrale/wp-content/uploads/sites/60/2021/05/support.pdf)|If xⁿ−1 and yⁿ−1 have equal prime supports for every n≥1, must x=y?|~3+standard deps|Galois Pr|C|5238|
|001020|[1215](https://doi.org/10.1307/mmj/1028989918)|Bound escape length in {∣P∣<1} from 0 to the unit circle for P(0)=1 with unit roots.|≤2 note|Geo CA|C|5237|
|001021|[1216](https://doi.org/10.1016/S0021-9800%2870%2980061-8)|Must every n-tournament have a transitive subtournament of order ⌊log₂ n⌋+1?|~10 the case analysis|F|N|1196|
|001022|[1217](https://arxiv.org/abs/2605.00301)|Divisibility chains of prescribed log-log growth in sets of positive lower log density?|~2 direct+inputs|P Div|C|5235|

### Additional matches beyond JSP-001022

|JSP|Erdős / solution|Question or resolution|Length|Areas|Lean|Open PR|
|---|---|---|---|---|---|---|
|001058|[paper](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/uniform-bounds-for-planar-polynomial-limit-cycles-September-24-2026/uniform-bounds-for-planar-polynomial-limit-cycles-September-24-2026.pdf) [2](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/two-limit-cycles-for-quintic-lienard-systems-September-24-2026/two-limit-cycles-for-quintic-lienard-systems-September-24-2026.pdf)|Degree-dependent bound on isolated periodic orbits of planar polynomial vector fields.|160+40|ODEs Poly|E|—|
|001067|[paper](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Uniform-excess-charge-for-Coulomb-molecules-and-the-outer-radius-of-neutral-atoms-September-24-2026/paper.pdf) [2](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Generalized-ionization-energies-for-full-Coulomb-atoms-September-24-2026/paper.pdf) [3](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Generalized-outer-electron-radii-of-neutral-Coulomb-atoms-September-24-2026/paper.pdf)|Full two-spin Coulomb model: universal two-sided first-ionization and half-electron radius bounds, with Thomas–Fermi generalized removal-energy asymptotics.|84+33+17|spectral theory PDEs|E|5063|
|001070|[paper](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/The-Grothendieck-homotopy-hypothesis-via-elementary-expansions-September-24-2026/paper.pdf)|Do weak ∞-groupoids of every Ara–Henry Grothendieck coherator model spaces?|26|category theory homotopy|E|5068|

[s1]: https://virtualmath1.stanford.edu/~conrad/papers/tswfinal.pdf
[s2]: https://www.hejustinsun.com/prize/rules
[s3]: https://arxiv.org/abs/2104.14766
[s4]: https://doi.org/10.1007/bf02579194
[s5]: https://arxiv.org/abs/math/9904181
[s6]: https://arxiv.org/abs/2404.07113
[s7]: https://arxiv.org/abs/math/0507539
[s8]: https://web.math.princeton.edu/~nalon/PDFS/remark191.pdf
[s9]: https://pinkus.net.technion.ac.il/files/2021/02/conj.pdf
