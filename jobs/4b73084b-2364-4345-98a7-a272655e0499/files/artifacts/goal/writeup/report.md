# Eight missing-list theorems in Lean 4

**Casorati–Weierstrass is a candidate for a first Lean formalization.** The proof establishes density in the entire complex plane on every punctured disc about an essential singularity. Seven other catalogue entries also have complete proofs. Independent reviewers recompiled ten proof files unchanged with Lean 4.36.0 and prebuilt Mathlib, checked the statements, and obtained only `propext`, `Classical.choice`, and `Quot.sound` for every main declaration. Searches found earlier Lean proofs of parts of Pompeiu and Midy. Global priority is **UNVERIFIED** for every entry. [Missing list](https://leanprover-community.github.io/1000-missing.html) · [Completed list](https://leanprover-community.github.io/1000.html)

The public repository reached `7f9e6fe9271561d22465648a652278c486acde1f`. It contains the Lake project, catalogue snapshot and audit. Its only committed Lean file is the library root. The integration wave that would have added the proofs was refused. The clean-clone audit therefore correctly recorded **FAIL — files absent** at parent `5fff4405e5b89976ab98ba3ca43215b47368b4e2`. This report supplies the exact sources from the accepted proof records. [Extract all proof files and logs](#source-appendix) · [Rebuild instructions](#build-and-axiom-evidence) · [Final tree](https://github.com/identity-md-launches/goal-3470-objective-produce-first-lean/tree/7f9e6fe9271561d22465648a652278c486acde1f/formalization) · [Index][index] · [Independent checkout review][audit] · [Checkout log][auditlog]

## Catalogue triage

**Dataset `catalogue-triage-v1` has 956 rows.** Download the full table below. Each row contains the exact catalogue key, Wikidata mapping, name, area, statement, standard proof, estimated length, existing Mathlib support, missing lemmas, feasibility grade, prior work, evidence, and status. The extra `_item` column identifies the original report and its source list. The CSV SHA-256 is `5b7d9d858949ffdace92cf67b74c1786a50be4d836700d18d3d2c7cdbf8cfd56`. I checked both export digests against the manifest, matched the records to the originals, and compared their keys to the frozen catalogue. [Full triage table (CSV)][csv] · [Full triage table (JSONL)][jsonl] · [Manifest][dataset] · [Original reports and source lists][items]

A means the worker expected a proof within a few hundred Lean lines using existing theory. B needs additional definitions. C needs substantial theory. C/SKIP and UNVERIFIED preserve hard exclusions and unresolved identifications. Grades estimate effort. A row can receive A and still identify an earlier proof. Suffixes distinguish entries sharing a parent entity, including `Q4724004A` and `Q4724004B`. Sources in shards 03, 06 and 20 were flagged on recheck. Their affected claims remain UNVERIFIED where corroboration is missing. For some shard-20 rows the available evidence supports only a catalogue title. Those statements and feasibility estimates remain UNVERIFIED. The dossiers distinguish Mathlib and Loogle/Moogle findings from failed queries. [Selection and search log][selection] · [Merged reviews][m1] [2][m2] [3][m3] [4][m4] [5][m5]

All eight shortlisted entries had a worker grade of A and a proof route from existing definitions. The selection review graded Schwenk, Balinski and Ford C because they respectively need a tour-splicing construction, polytope edge-path theory and a sieve argument for totient multiplicities. It found existing projective work on Brianchon and external work on Platonic classification. Gauss–Markov was held for comparison with a reported BLUE covariance result. The angle-bisector reserve still needed a benchmark and converse check. Cartan–Brauer–Hua still needed a division-subring API and prior-work check. Neither reserve produced a Lean file. Every selected target reached a full proof. Two distinct routes landed for Gomory and Lambek–Moser, one apiece for the others. [Selection, dependencies, estimates and reserve dossiers][selection]

## Statements, proofs and fidelity

**Weierstrass–Casorati · Q2226962.** Let a complex function be holomorphic on the disc of radius R about c with c removed, and have an essential singularity at c. For each 0 < r ≤ R its image on the punctured r-disc is dense in ℂ. Lean expresses essentiality as `¬ MeromorphicAt f c`. A meromorphic punctured holomorphic germ has a removable singularity or a pole, independently of the assigned value at c. If the image misses an ε-ball about w, set H(z) = (z−c)²/(f(z)−w). Its difference quotient at c has norm at most |z−c|/ε, so H extends holomorphically with derivative zero there. Then f agrees on the puncture with w+(z−c)²/H(z), a meromorphic germ, a contradiction. The reviewer checked the germ and radius quantifiers. Mathlib PR 29588 concerns residues and supplied no density theorem. [Author][a06] · [Verification][v06] · [Related PR](https://github.com/leanprover-community/mathlib4/pull/29588)

**Infinite monkey theorem · Q487132.** For iid measurable letters on any probability space, over any finite alphabet with every letter of positive probability, almost surely every finite word occurs as a consecutive block beyond every cutoff. Fix a nonempty word with probability q > 0. Starting after a chosen cutoff, disjoint blocks spell it independently. The probability that the first m blocks miss it is (1−q)ᵐ, which tends to zero. A countable intersection handles all lengths, words and cutoffs simultaneously. The empty word also satisfies the conclusion. The reviewer checked that the almost-everywhere quantifier comes first and that no uniform distribution is assumed. Searches found the Borel–Cantelli machinery and no earlier Lean proof of this statement. [Author][a02] · [Verification and search][v02]

**Gomory’s theorem · Q2916568.** Remove any black square and any white square from an ordinary 8×8 chessboard. Exactly 31 dominoes can cover the rest. Route A numbers the board along a closed edge tour. Removing opposite colours leaves two even runs, including a possibly empty run. Pair their successive squares. A bijection from `Fin 31 × Fin 2` to the surviving squares proves exact coverage, with ordinary edge adjacency excluding wrap-around. Route B pairs opposite colours within 2×2 blocks and moves the designated hole-pair along a path of adjacent blocks by swaps. It also returns the partner involution. Earlier Lean work proves impossibility for two same-colour corners. The searches found no prior proof of arbitrary opposite-colour existence. [Tour][a01] · [Tour review][v01] · [Block proof][a01b] · [Block review][v01b] · [Earlier corner proof](https://gist.github.com/avigad/1080e327ad6806884c9c5091f5c449bd)

**Pappus’s area theorem · Q3527044.** On AB and AC of a noncollinear triangle erect arbitrary outward parallelograms. The extensions of their far sides meet at a unique H. Using the vector from H to A on BC gives an outward parallelogram with area equal to the sum of the first two. The determinant of B−A and C−A is nonzero and yields H. The two strict opposite-side tests give opposite signs to the two signed determinants. The third determinant is their difference, so its absolute value is the sum of their absolute values. The Lean conclusion equates Lebesgue measures of the translated closed parallelograms and proves the outward side condition. The known Lean file for Pappus’s hexagon concerns collinearity. [Author][a03] · [Verification and comparison][v03]

**Lambek–Moser · Q6481192.** For nondecreasing f,g : ℕ → ℕ, the relation f(i) ≤ j ↔ i < g(j) holds for every i,j exactly when the ranges of i+f(i) and j+g(j) are disjoint and cover ℕ. Every ordered partition into two infinite parts determines a unique such pair. Both shifted sequences are strictly increasing. Route A compares the rank of one sequence below a term of the other and fills each gap. Route B pairs indices i and n−1−i at every cutoff n. Exactly n shifted terms fall below n. Comparing successive counts proves coverage, and `Nat.nth` gives unique increasing enumerations of the prescribed sets. Shifting the domain and ranges by one recovers the positive-index convention. For example f(i)=i and g(j)=j+1 yield evens and odds. The count proof puts the statement and ID in its module docstring. The rank proof also documents the main declaration. Review found special Beatty partitions and related enumeration machinery. [Rank proof][a04] · [Rank review][v04] · [Count proof][a04b] · [Count review][v04b]

**Pompeiu · Q3534036.** Let a,b,c be the distances from any point P to the vertices of a nondegenerate equilateral triangle in the Euclidean plane, modeled by ℂ. They form the side lengths of a possibly degenerate triangle. All three triangle inequalities are strict exactly off the circumcircle, and one is an equality exactly on it, including at the vertices. Normalize the triangle by a similarity. The Heron product (a+b+c)(b+c−a)(c+a−b)(a+b−c) equals 3(PO²−R²)² for circumcentre O and radius R. Its sign and zeros give all three conclusions. Earlier Lean code already proves the weak inequalities. The circumcircle equivalences are the extension for which the searches found no proof. [Author][a05] · [Review][v05] · [Earlier proof](https://github.com/rjwalters/lean-genius/pull/25024)

**Midy · Q856158.** Expand a/p in base b ≥ 2, with p prime, p ∤ b and 0 < a < p. If the least period is 2k, the two k-digit blocks sum to bᵏ−1, corresponding digits sum to b−1, and the full block has value a(b^(2k)−1)/p. For 1/7 in base ten, 142+857=999. Leading zeroes retain their positions. The Lean lemmas connect the digit recurrence to actual long division and identify the least digit period with the multiplicative order of b modulo p. Then bᵏ is the nonidentity square root of one in the residue field, hence −1. The second half starts at remainder p−a, and complementary remainders generate complementary digits. The earlier Lean reciprocal case treats a=1 and the block sum. This proof also covers every admissible numerator, the individual digits and the least-period bridge. [Author][a07] · [Review][v07] · [Earlier proof](https://github.com/rjwalters/lean-genius/pull/25071)

**Le Cam · Q3154003.** For a finite independent family of Bernoulli trials on any probability space, let S be their sum, pᵢ their success probabilities and λ=Σpᵢ. The absolute errors |P(S=k)−exp(−λ)λᵏ/k!| form a summable series over all k ≥ 0, of sum at most 2Σpᵢ². A single trial contributes exactly 2p(1−exp(−p)) ≤ 2p². Convolution with a probability law contracts the sum of absolute errors. Independence gives convolution for the trial sums, Poisson rates add under convolution, and induction adds the one-trial bounds. The reviewer checked the ℓ¹ normalization, the explicit summability claim, unequal probabilities, pᵢ=0 or 1, and the empty family. Mathlib’s pointwise binomial-to-Poisson limit has a different conclusion. [Author][a08] · [Review][v08] · [Le Cam’s paper](https://msp.org/pjm/1960/10-4/pjm-v10-n4-p11-p.pdf)

**Prior-work verdict, 26 November 2026.** Six targets had no prior Lean formalization found in the searches listed. The two earlier results above establish prior work on Pompeiu and Midy. I repeated the open Mathlib PR searches by theorem name and found no matching open PR. The linked reviews give the actual GitHub queries, Mathlib snapshots, public Zulip coverage and related proofs. Authenticated global code search, exhaustive Zulip history, and priority over unnamed equivalents remain **UNVERIFIED**. The network also flagged some source checks in the proof and review batches. Passing compiler checks authenticate proof terms within the specified foundations and say nothing about priority. [Community database](https://github.com/leanprover-community/mathlib4/blob/master/docs/1000.yaml) · [Open PRs](https://github.com/leanprover-community/mathlib4/pulls) · [Public Zulip archive](https://leanprover-community.github.io/archive/)

## Build and axiom evidence

The pin is Lean `v4.36.0` (commit `611c117bfaf7b7ae1cfcf246ce6fba31e8f509e9`) and Mathlib `fc4f59e577feb1a4956671bc04ac18aaaf8cd842` (release `v4.36.0`, the current stable release on 26 November 2026). Every author and independent reviewer used prebuilt dependencies and compiled the same UTF-8 source. Each verifier record linked above includes `lean_source`, `source_sha256`, `build_output`, `fidelity_review` and `prior_work`. I checked each author/verifier pair for byte equality, checked the hashes of the public records, and scanned every source for proof holes, new axioms and native proof shortcuts. [Mathlib release](https://github.com/leanprover-community/mathlib4/releases/tag/v4.36.0) · [Foundation][foundation] · [Runtime tests and limitations][harness]

Each independent build ran `lean -DautoImplicit=false FILE.lean` in a fresh directory and exited 0. The rank proof of Lambek–Moser emitted two unused-variable linter warnings for `hd` and `hu` at line 143. The count proof ran without warnings. The following lines are the reviewers’ main-declaration outputs, with identical lines from second routes printed once.

```text
'Complex.casorati_weierstrass' depends on axioms: [propext, Classical.choice, Quot.sound]
'ProbabilityTheory.infinite_monkey' depends on axioms: [propext, Classical.choice, Quot.sound]
'Gomory.exists_domino_tiling' depends on axioms: [propext, Classical.choice, Quot.sound]
'EuclideanGeometry.pappus_area' depends on axioms: [propext, Classical.choice, Quot.sound]
'LambekMoser.inverse_iff_partition' depends on axioms: [propext, Classical.choice, Quot.sound]
'EuclideanGeometry.pompeiu' depends on axioms: [propext, Classical.choice, Quot.sound]
'Nat.midy' depends on axioms: [propext, Classical.choice, Quot.sound]
'ProbabilityTheory.le_cam' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The goal records a different agent for each author/verifier pair. The count-route verifier also printed the same three axioms for `LambekMoser.inverse_ranges_disjoint` and `LambekMoser.existsUnique_monotone_pair`. The Midy reviewer separately checked `Nat.longDivDigit_minPeriod_iff`. The two proofs of Gomory share a public declaration name, as do the two proofs of Lambek–Moser. For a single importing module select one route per theorem. The extractor adds an import file, `MissingTheorems.Selected`, using Gomory A and Lambek–Moser B. Import that module to use all eight main theorems together.

**Reconstructed project, PASS.** In a fresh clone of the final revision I installed the recovered proof sources, matched both prebuilt archive hashes and checked the directly imported Mathlib sources against the pin. The default `lake build` passed after building each primary module. A fresh Lean process imported `MissingTheorems.Selected` and printed the same three axioms for all eight main declarations and the uniqueness and least-period lemmas. The package linter reported module-header and style warnings. The two alternates ship in `AlternateProofs/` and passed independent direct Lean checks. I reproduced both direct passes. The alternate Lambek–Moser rank proof’s linter-enabled Lake build remains **UNVERIFIED** here after two timeouts. The bare commit lacks the proofs and dependency payload. An offline build from that commit alone and compatibility with newer Mathlib master remain **UNVERIFIED**.

Clone the pinned tree and check out its revision before running the source-appendix extractor. The bootstrap below uses the two matching Linux x64 bundles. The foundation exercised `lake exe cache get` during online preparation. The proof replay uses already-built Mathlib objects throughout. [Prebuilt release and checksums](https://github.com/Identity-md/lean-bundles/releases/download/pequalnp-e125f04d0dc6/fetch.json)

```sh
set -eu
timeout 540 git clone https://github.com/identity-md-launches/goal-3470-objective-produce-first-lean.git proofs
git -C proofs checkout --detach 7f9e6fe9271561d22465648a652278c486acde1f
```

Run the [source extractor](#source-appendix) to populate the checkout. It can also recover the project files into an empty directory. Then, in the directory containing `proofs/`, prepare the prebuilt runtime and build the modules.

```sh
set -eu
bundle=https://github.com/Identity-md/lean-bundles/releases/download/pequalnp-e125f04d0dc6
mkdir -p runtime/lean runtime/pk
curl -fLsS --max-time 540 "$bundle/lean-4.36.0-linux.tar.zst" -o runtime/lean.tar.zst
curl -fLsS --max-time 540 "$bundle/pequalnp-e125f04d0dc6-packages-lean-4.36.0-linux-x64.tar.zst" -o runtime/pk.tar.zst
sha256sum -c <<'SUMS'
2b7ab1ed8b92d2e6abfaf41344823b510064dbc9c0260cac73eb496ab2dea6eb  runtime/lean.tar.zst
69b68c745d0bd8dba3ab21966f8cdb14f9373bd4f1df1d17680f4b80dad98a88  runtime/pk.tar.zst
SUMS
timeout 540 tar --no-same-owner -xf runtime/lean.tar.zst -C runtime/lean
timeout 540 tar --no-same-owner -xf runtime/pk.tar.zst -C runtime/pk
export PATH="$PWD/runtime/lean/lean-4.36.0-linux/bin:$PATH"
mkdir -p proofs/formalization/vendor
cp runtime/pk/mathlib/LICENSE proofs/formalization/LICENSE
ln -sfnT "$PWD/runtime/pk" proofs/formalization/vendor/src
cd proofs/formalization
timeout 540 lake --no-build build +Mathlib:irArts
# Build one target at a time in this prepared checkout.
for f in MissingTheorems/Target*/Route*/*.lean; do
  LEAN_NUM_THREADS=2 timeout 540 lake build "$f" || exit 1
done
LEAN_NUM_THREADS=2 timeout 540 lake build
```

The standalone command for the rank proof is `LEAN_NUM_THREADS=2 timeout 540 lake env lean -DautoImplicit=false AlternateProofs/Target04/RouteA/LambekMoser.lean`.

## Entries for the 1000+ database

These YAML replacements use the existing catalogue keys and titles. The external-project `url` leads to a public verified source record. The `comment` identifies the file and declaration inside it. For a single file, `jq -j .lean_source review.json` emits its exact Lean bytes. This form applies before Mathlib imports the modules. A future in-Mathlib entry can use `decl` or `decls` directly. The replacements passed the pinned Mathlib YAML checker. These are unsubmitted entries. [Field definitions](https://github.com/leanprover-community/mathlib4/blob/fc4f59e577feb1a4956671bc04ac18aaaf8cd842/scripts/yaml_check.py)

```yaml
Q2226962:
  title: Weierstrass–Casorati theorem
  url: https://api.imd.fun/artifacts/b75b7c00d41506624bdb039c70f33d06e6c7db63211ddb661a0d3f46c7786bb5
  comment: "Complex.casorati_weierstrass in CasoratiWeierstrass.lean (lean_source)."
Q487132:
  title: Infinite monkey theorem
  url: https://api.imd.fun/artifacts/c28ab14eec3a4f7338701bc401b4341d91ee13ea3d2fa7a402c4a60d7f1ede77
  comment: "ProbabilityTheory.infinite_monkey in InfiniteMonkey.lean (lean_source)."
Q2916568:
  title: Gomory's theorem
  url: https://api.imd.fun/artifacts/8922ac00b3f75a9f46f8065d3b363d4aaa96cafefd71bdb4bfab740b6b8d94e6
  comment: "Gomory.exists_domino_tiling in Gomory.lean (lean_source)."
Q3527044:
  title: Pappus's area theorem
  url: https://api.imd.fun/artifacts/75f002c5a12171db9f44574684eeac2c622643742583ea4137ea949ee4ace12e
  comment: "EuclideanGeometry.pappus_area in PappusArea.lean (lean_source)."
Q6481192:
  title: Lambek–Moser theorem
  url: https://api.imd.fun/artifacts/76a75b291f55d3623372e7a644b55e1171696137a24f7d4a913bdc3209e4a72b
  comment: "LambekMoser.inverse_iff_partition and LambekMoser.existsUnique_monotone_pair in LambekMoser.lean (lean_source)."
Q3534036:
  title: Pompeiu's theorem
  url: https://api.imd.fun/artifacts/aaf98529fbe64c3d99249714bd440cd140c2fd72048da671e5c8989b9b5e9e44
  comment: "EuclideanGeometry.pompeiu in Pompeiu.lean (lean_source)."
Q856158:
  title: Midy's theorem
  url: https://api.imd.fun/artifacts/3b9c88d60ff8c3ed7d4d3a0417e77cb973621bfebec84eec94bfd19299c7ae25
  comment: "Nat.midy in Midy.lean (lean_source)."
Q3154003:
  title: Le Cam's theorem
  url: https://api.imd.fun/artifacts/cc405c5f79a5867fd3a23d867cb7557e3cd5a5e5605ad0eaecf03cdf18978b00
  comment: "ProbabilityTheory.le_cam in LeCam.lean (lean_source)."
```

## Source appendix

The ten proof files and the pinned Lake configuration are recoverable offline from this Markdown. The extractor also saves the reviewers’ build and axiom logs under `reports/TargetNN/RouteX/`. The complete lead proof is readable inline. From a directory containing `report.md` and the clone `proofs/`, run the following Python 3 snippet.

```sh
python3 - report.md proofs/formalization <<'PYTHON'
import base64, hashlib, json, lzma, re, sys
from pathlib import Path

report = Path(sys.argv[1]).read_text(encoding="utf-8")
root = Path(sys.argv[2])
plain = dict(re.findall(r"^#### `([^\n`]+\.lean)`\n\n```lean\n(.*?)^```$", report, re.M | re.S))
data = re.search(r"^```base85\n(.*?)^```$", report, re.M | re.S)
archive = json.loads(lzma.decompress(base64.b85decode("".join(data[1].split()))))
sources = archive["lean"]
sources.update(plain)
manifest = dict((path, digest) for digest, path in
                re.findall(r"^([a-f0-9]{64})  ((?:MissingTheorems|AlternateProofs)/\S+\.lean)$", report, re.M))
assert set(sources) == set(manifest) and len(sources) == 10
def save(out, raw):
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and out.read_bytes() != raw:
        raise FileExistsError(out)
    out.write_bytes(raw)

for name in ("lakefile.toml", "lake-manifest.json", "lean-toolchain", "MissingTheorems.lean", "NOTICE"):
    save(root / name, archive["project"][name].encode("utf-8"))

save(root / "MissingTheorems/Selected.lean", archive["selected"].encode("utf-8"))

for path, source in sources.items():
    assert re.fullmatch(r"(?:MissingTheorems|AlternateProofs)/Target0[1-8]/Route[AB]/[A-Za-z]+\.lean", path)
    raw = source.encode("utf-8")
    assert hashlib.sha256(raw).hexdigest() == manifest[path]
    save(root / path, raw)

    log = archive["verification"][path]
    dest = root / "reports" / Path(*Path(path).parts[1:-1])
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "build.log").write_text(log, encoding="utf-8")
    lines = [line for line in log.splitlines() if "depends on axioms:" in line]
    (dest / "axioms.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
PYTHON
```

Each checksum covers a single Lean file. Paths are relative to `formalization/` in the reconstructed checkout.

```text
43423e847a6364653c4c81f0fef90a57addd19b96647a2f755506c3a91a8ca8b  AlternateProofs/Target01/RouteB/Gomory.lean
b5610ca2b1f88cbb68eb30617025992020cd41abc70c9f5d2f23c80420e525e0  AlternateProofs/Target04/RouteA/LambekMoser.lean
6a4d847db1e61f61267ce8f12de4118e9df7d46879aaad1d540492917bebecd2  MissingTheorems/Target01/RouteA/Gomory.lean
32a3a686681be51647b115fdca9f116b22eaf0a126ed3bf3085a045fccb979f7  MissingTheorems/Target02/RouteB/InfiniteMonkey.lean
df91feb8e09b6802a4329513feb2b54389961533558cc0f2bc23e54218e0a3eb  MissingTheorems/Target03/RouteA/PappusArea.lean
0cbf6a40a48464ad96acfe824cc3c38a11e5a19a48c7883c7df866bfa310bd9b  MissingTheorems/Target04/RouteB/LambekMoser.lean
8b4912e3dfbe84664275a39e0a84d5a10bb3920cbf68af3231e11352610c364a  MissingTheorems/Target05/RouteB/Pompeiu.lean
32f7dc3209cc721457470f4746500f4c8f997550f4cfe8ee0665f2fe325c2154  MissingTheorems/Target06/RouteB/CasoratiWeierstrass.lean
919c77a7eeab3c615464741eb08694461f2a90d8fa037cdfaf0bd6b9d971c6bf  MissingTheorems/Target07/RouteB/Midy.lean
deef382e175aeeca7c37e7d6bafddfde0d110d5a44272d94b7a9dd316c67d2b7  MissingTheorems/Target08/RouteA/LeCam.lean
```

#### `MissingTheorems/Target06/RouteB/CasoratiWeierstrass.lean`

```lean
import Mathlib.Analysis.Complex.CauchyIntegral
import Mathlib.Analysis.Meromorphic.Basic

open Filter Metric Set
open scoped Topology

namespace Complex

/-- **Casorati–Weierstrass theorem** (Wikidata Q2226962).
"If a function is holomorphic on a punctured disc and has an essential singularity at its
center, its image on every concentric punctured disc of positive radius at most the original
radius is dense in the complex plane."

For a holomorphic punctured germ, being meromorphic at the center means it is removable or
has a pole. Indeed, after multiplication by a sufficiently large power of `z - c` the germ
extends analytically. Its power series is either zero or has a first nonzero term. Subtracting
the exponent of the multiplier from the order of this term gives a nonnegative order in the
removable case and a negative order in the pole case. Conversely an analytic extension or a
pole can be made analytic by such multiplication. This condition depends only on the germ
away from the center. -/
theorem casorati_weierstrass {f : ℂ → ℂ} {c : ℂ} {R r : ℝ}
    (hf : DifferentiableOn ℂ f (ball c R \ {c})) (hess : ¬ MeromorphicAt f c)
    (hr : 0 < r) (hrR : r ≤ R) :
    Dense (f '' (ball c r \ {c})) := by
  rw [Metric.dense_iff]
  intro w ε hε
  by_contra hmiss
  have hbound (z : ℂ) (hz : z ∈ ball c r \ {c}) : ε ≤ ‖f z - w‖ := by
    by_contra! hlt
    exact hmiss ⟨f z, by simpa only [mem_ball, dist_eq_norm] using hlt, mem_image_of_mem f hz⟩
  have hne (z : ℂ) (hz : z ∈ ball c r \ {c}) : f z - w ≠ 0 := by
    intro heq
    simpa [heq, not_le.mpr hε] using hbound z hz
  let H (z : ℂ) := (z - c) ^ 2 / (f z - w)
  have hHc : H c = 0 := by simp [H]
  have hderiv : HasDerivAt H 0 c := by
    rw [hasDerivAt_iff_tendsto_slope, Metric.tendsto_nhdsWithin_nhds]
    intro δ hδ
    refine ⟨min r (δ * ε), lt_min hr (mul_pos hδ hε), ?_⟩
    intro z hz hzc
    have hzr : z ∈ ball c r \ {c} :=
      ⟨(lt_min_iff.mp hzc).1, hz⟩
    have hsub : z - c ≠ 0 := sub_ne_zero.mpr hz
    have hslope : slope H c z = (z - c) / (f z - w) := by
      rw [slope_def_field, hHc, sub_zero]
      dsimp [H]
      field_simp [hsub, hne z hzr]
    rw [hslope, dist_zero_right, norm_div, div_lt_iff₀ (hε.trans_le (hbound z hzr))]
    rw [dist_eq_norm] at hzc
    exact (lt_min_iff.mp hzc).2.trans_le (mul_le_mul_of_nonneg_left (hbound z hzr) hδ.le)
  have hdiff : DifferentiableOn ℂ H (ball c r) := by
    intro z hz
    by_cases hzc : z = c
    · subst z
      exact hderiv.differentiableAt.differentiableWithinAt
    · have hzf : z ∈ ball c R \ {c} := ⟨ball_subset_ball hrR hz, hzc⟩
      have hfz : DifferentiableAt ℂ f z :=
        hf.differentiableAt ((isOpen_ball.sdiff isClosed_singleton).mem_nhds hzf)
      exact (((differentiableAt_id.sub_const c).pow 2).div
        (hfz.sub_const w) (hne z ⟨hz, hzc⟩)).differentiableWithinAt
  have hHa : AnalyticAt ℂ H c := hdiff.analyticAt (ball_mem_nhds c hr)
  have hnum : AnalyticAt ℂ (fun z : ℂ ↦ (z - c) ^ 2) c := by fun_prop
  have hm : MeromorphicAt (fun z ↦ w + (z - c) ^ 2 / H z) c :=
    (MeromorphicAt.const w c).add (hnum.meromorphicAt.div hHa.meromorphicAt)
  apply hess (hm.congr ?_)
  filter_upwards [mem_nhdsWithin_of_mem_nhds (ball_mem_nhds c hr),
    self_mem_nhdsWithin] with z hzr hzc
  have hsub : z - c ≠ 0 := sub_ne_zero.mpr hzc
  have hden : f z - w ≠ 0 := hne z ⟨hzr, hzc⟩
  dsimp [H]
  field_simp
  ring

end Complex

#print axioms Complex.casorati_weierstrass
```

<details>
<summary>Lake project files, remaining proofs and all verifier logs (XZ, Base85)</summary>

```base85
{Wp48S^xk9=GL@E0stWa8~^|S5YJf5;i39u{9OP&h>3=iwq)Fx#@vUq>w^=^(&U#Prp6^Q8jwVk8AM-l79PhICf;<@%wHz~WxWYJBRRl2Q-
AsfWzHhiQxOaKREe{_LX#f8M(q-
u6H(cEgYx4uADDH~DuhG)Lq%%066)#p{NLz{Kj2*@%ZL5`JnYxvJFH88Jp9rS*sfVXTD8j3qLW|6QEtx|H4K?Jw<abbH6_Zh%L~|=6Q~galcD<Ng
*m8l)=l;Ijp4x<veI9AIWf$N?}PKlDS9DAAE3uVvsH_`y0+IaKrw<5u0HM#?T+f*L6m4*y*%ztT)P5is=V2HClk+0(iMOh$Y#}D%Yiz`UcIR}>8O
ig^8pkv|K=SrCLOrp@uH{Z=O65x63r~^ujDG|{I{aCE2Vz0jKUbuKWn}dwslKOKZ5GuR>%;@nIhzSBg3hXE>G5xAiIosVJqYT@KO1(4QXgg)~U6B
lr@LKbme<LMaJ%<8I7s%t=?G?HaM?_)FD&&r0-
xQXzyY=_*$|I_uqVc!SxIH$rH`_{pDihw<OW@{JLIL)E*5>r#nEbc@&EST$s4ZpZnb~Z46w;kTwwf^HL1HrMZ;hd?`EOw&|)l&#a4}=yibx9e36@
Dz4PGJX?SB%J^1=rL2~5-
t~`zXmWr>(%o_FQkFjJ=y^lI!+lg@Gkg9F@I|qE4M2g>jj<J#9>)A)$SCZj;sb3ZiC(#pocw!&qno}=&sHXa)`Qf1umjtOAL2SM$DVK7d%MkRJ-
O-)0LS}@+cfcg_jnbF733ynfQ^}h90bRF`hD#ps+M8OT;DhlT;2-xDf--ng>fUTE(j@q@w9qY&eqNkRid5S1{H}O#W)qH^f)1?Qi9h%iE~|kU%83
mDYhBE6)TQPDCJRbo0c@j#)A`+Qm5K#Z_(a>pAQ!7Djy-`c_-3Wx$B~!oR^E5QeE9^<=alc8S&RUc$9V(#9MSnUcl{6Xo-WVs^NiO3IA-Gmy~5~D
%`X;@@7OXyD|5uU~o*R7#3EjE2{KS7Az@(k`i3Ac}m#Ed}T8Xvr4yUiab_YPL2p<i9;$m#+0?JKT9ZjA_D`SpzUYA{85rxQIm<ODm;Diw!pNXCw!
P#ERJ9^eW>|Qex6nb1l%-bRnPP$#?=j6OsIBArAmAd7-Sl*fhczVc>$sFcY-i7rK2H-
3$8y8pZi<90)Fnn$&J%&7Z3Ku*g!!ywQkR4jdzld&i!zVqHq<|0XdD}Er~FDpi9$}iibC#lnzwZ)a3?-
?SB?}9!et~O%5p`{^lEN$&YCeY^8UVIQFiuO$?&RMuDplIWyo{Wn@iF-~&!FQNq{4DqEEn&M-zG-
+k6^EWT{quFJ|L+($9vhD|i)ISq*cT`4{SIi>F8Y|*&_g*SS2a6}eF5dJHsBdmji$g-
<K$`EGH(qAXPMvdw&>?{8ot`2;6bCk`EMtlTKvRABSRo|`4+R&KVAR58}Q=PUFZK*L}3DnSHHvRSk7S4sBi;pcP=G(pu^8T;~i?{Wv89~`amc<%i
7}XD>A`6eH$ENKvUdC+3XJcM|$_$yIF?|vkDNf0Y3jT8=<otU}l*UhC5?HSHVm^QM^M3XE?A!AFpU8Xj$h>U1v|TncSc|$}>3p~2XUNTe|Gt9nGO
#f*90&cAL%Cu>uEsN10LN{xb}n}V^I3IkqNDho55_DI4X;!wQ1xb-
c!4>>S2<gpFs;%Mb^9`{w23i#Z}~EAbqwtn46iRc8IBLUtxH%GVp>jEp%xp)?0(XyVHK$iGXFmB0cd7HYI!1nX=_>yx*Q&F=u6%UABw(aR+%AEMd
m!cb}mG9)!>`l^p|8u>Q#KpfM=O&3}3BFB+(-
$QEifg<{GMye7W;;0^9+II94+zbVJ)@n+_G2sODx1$WCL@AJ*(6Di0z&4C=6=X|c!{cJsK084tg;h#K%xnc@NJQNpN+)7CyCE^~oQEvT2Gg8#J#8
Crux<x1(f%d4W6fq$`1ZT6*)SNrHNb|w(9-;(dhIy*B;kZKZn|3N<_o_S1xmO*432I-
Ds8H5l8C9w`{x91i8&|mYog)qwZjC^VY?siW))hpFfQPk8ltBg>D-IIjd#zo?jzQ7s{^~fMQ6wEU4z-CN}k0z1L-
!F{cLc1B!5G=Z?(5*;#mp>Mn&R<RG413q>eKIdA5n#H!M=Zr6Eqr1PD(t2=p~dnaA|8|Hi89ho$;TYB#-dpEK%55Ymk-
Q{K_aq+jw8BDH%E%AXZbSJ$B}RVdi75<(-
rlXepnZ>gx!d2sBnpU_{^cBDw|_qOg@@TX$2uZhA%e!HEo|r1r=(u14q+$QU1I+p*S3rL;2zAlHCId#>5V3j%bFMB`=py=<m5#BIrkZ7n=em0iZK
ak4?#kCT+_+U_0=bem%W-
G6CI_T_`Kt!SM_>sE98+3}MNDTK6r>ZW4MUfrtUb<AH4M+VJIbsNm{2r;o7Z&5ce7Fi$C({3$MfyU2!UnsVk4TrJ!iZkO4y7fet1c=+hnyZFZ|U|
qV>Lf6b+fZ%BLJS^ovelLuF3Lj#tl_mqDh6w?^-
D#ugN3$f?5p!tw5++4)NY#wYGNzw2V;Dg514%QxMa0)I9G0B@bZb+OEuW7(QHl|nuPONJDE{(<x>>?;;*Sw!nq^TFRL@{~_m1(2|26ABTwK6N_kg
<_RBD7lcGz2Sl?lXtyPSQm{3$OYtT8X<dRQTp>ZCJsM7F!B3F9i7mgqQy+QLMlLNx}-y(~yk<-
kNfsz{4;(=1=*x!S!*k6PioXFyiv?*~H+*S3?p^4~cxm2g5wxC=i4pYN)dtdR6M0`2dGtPz+f*k_#p0UUYFWHMp!|5u}#8H$l2kN*S+l@NqK_L(^
nhFCORtbhgbxtDdQW+8q@CGg5hTKcPrFb5oxRYEdTh)rW|Wl|CM%dkayI~5(hc#Lg=UMh?}aOGjYMBxRR^&r;2_f|})Ysj6I@YL(RufpXZ_Kt@Jt
D`MDH7iTwt23{{fCwfLQ=E=f$u{yxo!v~!6!}v32QF(GwogLa(Dc;8&!Xi(Tu0FpZ)CW8B~!RvIK(+{s+&r>xLD8c%5x|4eMu_Itm#>Pv@e5C`IU
+}QS<lIWUWFH|0k|yr+y~s%poa3InQI`i0ef~3rN0=s7>H6A9S<pUF($~LFfzW?DUDgs~ovFapAOC8iMhRzAW4*F2T#AR|O)_5C)|W6Z1<T>6{M&
jqv#=vz1J3q<O>ES5e>l3h(rQ!uE^3WTkodfPB(&{TD*%nF(HVx690JC4Lh%#@wj?n1ZU^v7-k2Ytt?@O}jB-xz8$bx>WaZN;42c*ZkF9oha6n(m
Dy+;3A7b%m!=Fn<r3$I>4F4-$bL<oiD)^r<-TTMeW%^2bUCB9<6^P_v_##BTjC`AR0EAHt}kIYn6IEOg0P`u8x7CQKjqW&r&^Ib~3V-
dxi?o$+0^xL|Z#tfgdjzZ8thbv=92QB}RWTe4{V<WYn>~kuO_?P;j8i)mrXp%$H5~HbpOOUOKcS8f6O}8MM7HFLEQ2FaUi60XJ(@x`Ec#kwZ+QBJ
{ppfvS6?4)varuht%{WiE<k{NT+uQ>--
<+r=Xw?hzIbu@HJe14GJ>o|sxf19e&g7ah*E=P?uEg@AATQl1L;A*H3|vFt54cNSh*mXSCZKTwyPA33co$h`p;7-
K;&Q|x3WV>u3<hC$sARjqMa5#bzUc2}o)6hSdB<B?_E2D&h;fQ9p0)OvNKH_kFy`8PJ-9JjiCRgjf`S#Ya=4QPoQud_K03||orX1P_?tIeb-Ch6s
7`vKCtH<FqJ_Ay^4Gb}Xb?h6FkAuW)E;X8{sZ%dkl1<gu2tp7|xS`2ozTsEHm$)1&dK4_RwMAS_)*%i^^(ql%MKa{@3-
%1;89yTkGx)U&kJ!DS&5|Z+OhMbO#c~G3{WI-4$cQ6#u$8U=!;pwqmg+v`9{RjtU-
D2`GLiaD<4L#8<wEX9sXwgU?@h0B)!20c=b@;nr)w%UcCb}=*g^pLb>2rfLTq#$R>Adt#z^xUk03G_~=SEKpM~&svmp)tvQ6675#c>2tNZdoY{1)
n=O0)iIrwb>H?4|sRB18`FdR@r{!_hZ|Vq#vhft(78rtT1Uc7bBzM*c&@YhmqehY;fK>(($Fb-
g;JvCU|OS8!F<$o;oE;(}APC8Y&BE&C3jrnwXU{O!Bvql)VtC*DLTgGs<Db7AEE{+BP%wvGW=ndrORBU#(A6$9OFV!);6XNkMPn2JwCCtgtyTkm|
)0Gj|Pkj+9ptT0W$RqLH?Kd!+S1jK%D7Im5IR%g@?fv)0`p@&^Ij%(w$5oit;ZXmU`)LyUf$b0BlVI;tyxXg6GG+oAq3u;(8u^&si&^$PB(^Tb^K
tr1=cGrfjstyzlPiN1glfFyi_r)rZ2Zim9B@-1HYS9T?v+C-8vi@mf6e$d-oWEje;xn;ec&CncWX<PVyqchGpPLL8ubBy+GIsB-J!+RR-
MFb6aiK7-4rCG>wb<tTgew@T1$#*F^bb#PRyy6@*DwMpcyo%lvMilL+{xyo1dzlu2ADBVP8jdOOH;hLs(((3PIXKO1m9h^n5n6gm$!6@439rM-WP
Pz%}=z8nVGmM0M3Sa_hzF^{S#;6wt5t&m2`X=8<nPe809fy$n%|mtv`bq*8qb9gMz8@946~_h=9leOfYy!%OBYW2-&c-<ujH@8wS-
`;S1LEPq>y+28ZNGOo{DVi(wS??bT6E10}XB*mRuLG4`?a>@|BYdYXvYwkbjUv>jq}%o#0G#z&@OqDmL&Thv3&b?R**0O0SKK-
x*54bpEdxXhkaI>dBf!Z0$&=#@Ao#M%@YYyl}><qi<Az3D}<vrm!ncTPDYzGbV*TN{wd^^T_I*K}X*cz&ho$!bolIzvTmDtFTuPo*nKg+l8_L^8A
@MRTg~l_B*na}a&(WA?=+W*U}mj<^o|EdqAdXMf>0#)hg7oAA;F%9Y7`y3ccqD0miUl>Nn>n13`}wJti~K(2*zvO>D|p>ih>_s$Iv2Jjy)On?T_*
m;ACcd*xddR$nL{?|lpjAejkAO*aavEtLGBn}k4c7K0^+8VRub;M3U{(+cn`=F-Q2yR4?bxuAT?=>|-kc@mtH<Nw-
;8@g2T+eQ}UYsHHM^`Uu4=h#N+3`a$bo?!XS>SW0Ao^@z%eP`NuV^+E;2a|UkobeiSdB@Zi3|zQ|Gz=a@(V8M8V9$>i0&y4^JakTbJd64r<fmW^I
7kR?>skomDGLC#~hQi1R0P@brQ6slQeAdVQc!KK7-h246D{RGFdE5riK=O6KAufO&Iz{G^edDz5y&%=-aWEPi3+_grZv6yn%4I-
l1vi+b`%F<pdY#pMuxw@49Ke%)ZoJ7=a3A5laTFWSH^X4(j0iIK+llB_P7A0hgnRhL=J7dCO2%wwDBhr?H!H#eCuth_3>rU<}R7_F29`Yq{ENrm4
H7S&uo9LsbkbD}G?!+MbYHlb;bFePAEHIWlLP_<<pR_@gfrL1p3v`ab#=mSGG#Kmr7BYXk&Z%-
cY%KUBGIiq10U1bA{^3am?*r^Y^rz3xy5FY~LD$)I5U158H1$nzU0nFmuX=c|zbLm(@sBrW0=+kXDS$u#?))gC3o?F9VY+>xiN-
u9@QwbpwqzkzH&4>kEPqn~C_u_PBFU&XlKNu>I|;G#1X%v*@_E$m<7*188e<@FLkB!E`W>*()KVOp=y<Mp|+`D`FJ4-
37$nlb}vU;Xn4=2dQZ@98@EJ0-Omzdmky?i(m0zodQCoC_*lfNoZ}P1awXn^`{->V|es1wVsbvNu0Ptkr1aC<mbXA0qFTY!@TQYDA2d>h-
y&RKs9zq3>-3l+aw1$=boVH_O1S&Bro)fg}5WSBK${No`plnhfRkGtEvZ)Gw$QThL+jPR*hBmdF}V>MeHevEzT83G|p<;F<LQ4qH?Ia~o@*uSky-
Td<?NEbb5t9K8)~Wo%S)QtAzo4#hcfInw5<B-!m<MOb*^l;c-Cqm@2#{UJ;qcy0Zktp~o+?afXjE{vT~>?yfacwG26N5?yo+rve*>-
CFZAn(%W&XU0y#*AhSFYE;f-
3U~$aXo8?;M4x9M(gi{acp#zMY6;cIxToZs?|}v?{4LI2SAb99anI5mw$G;`c3jY@ntoz@|T67wfy#iz&UeB+mTtGUAl%u9e{D_Bd1=c!VYc_u_?
+Ww+w?P`!({?#a1)o+aWNaf@uX-
%g8&CUEu!|%L5wjSSBLpoS;c~Pd~hmS6>S?0%wAw%s9;(f&){hj|&Of)fOqbk!*Q~=(V2H&`deEHr}ZrOVUpG5{`9GAk-
C7G~LIL7)(7)#_f{`cPUG#rk4&ng2wku^#%M`A4Y821U-}(^eq6}u;dJ2aZ_@?<Sbmap3o-!Id$V)6F_sNy{u7Rq{9-
W11T~T`)W`9HyAEhv@QpIIFi<}K6shjhmT{n97flPqFa15?8B^54JzsitijCwy$LNvHZvJ>wRxiq*#j2ekew01-
uLAUp~Y&s$<s04N$$XuM38+UiNk@(?>5h!T`<9H80o;b<i+mpyMAnhn-
1ktlcQ<I76PQ^DK66vUA59}dbI81Y!MOJYZd`Sc|>S8xKbA!c9KMEFEzbG$N!9<+yvVo07G0PTM9WF_+;x(r9pX0a41QEq$qe-
h3+Tum0=GJVxC^Bx|s$VJ&e-
YGMCR1QjYW5OnWwi13j{yg)&79kzpl0QL0X0jv{kgUMSlFtJFWzF~fZLbjakexY)>j27k^G2u6iII~{t_l0LB4D$Aqm{XB%bC%2<mv*RRA2X$eI)
=B4F+&_TZtP0ZO^AG{GcuK$_9`NptFw429z>`S48zl`g8oefk<1~85E6tih@m=Dg)9RsJIBy;V%;+zNyQKR-ims?^KfG&*Xe-u&L#-Z^-
4`rcnDv46XEReZbyh%T?md;pzZR<qF;eiE#k#K>YcJ+}cHI5#yRjvsN4RiRRK~Tzbv(~%H!~?-
UdP$&NP;QooZFco6<j>5LeMLLlP2>PT8|*aMAlwZ`IRN@bIcithc6enAd?Yp_B;wVD(+;8%zO1eHLHhzraaM$O%47cT)G>uaP7iuXTDrm^tJLPKx
)Z)XRv_kXrOjoEl5uSi7wqRhL#<Xv!{hlQ-i>UmcV-
`h{AmA{le}nna3snmcRX$&J28Ms*g*++NsERpU~*>Gx}>y8KhPAsv2Z^BJd`vyBH!IcA99l5}w3=fqM0`$S8->#-~Lx+9`bLdIsi<-
A!xdVTp97BU?;~*&2GKB$vbfw|lB|Loefhj3(z0H90sDljb%kwB!fXs37?TT&}0^DQu3S5i}HDGIV#Z(u&qB^7I;`Wi^o7n2-
y+@SA63e%Sy=3MM%1R#CiJdDGoLBovuGraq(r(aMG2Tv~pB-lK8apHz{uU2$GfIgSnDIUST<3w)~G%LX#`(41-
Go1OkS9z9@UVYj~2eM^W$_U^UVe1cTMla0-k2*a$?5p4+2xL}B5Uxlf6YVE3~tu@E=DoDf%`m5=ang-
=@PCF_Evn^NPa(@6y10y5D_YNG(06BkJpTR!X<3NJICOjC|xK~_ht+~#{y&*IrY}0%B+54@fGr!75h@k;92Gu<_FMOI21w|S`aAs7E<Vm<XUMXTO
WHnsesvyOT`Kyo!?35~%ZPn+@9;+*IJe`}%mTd*ea5mttLXa%GSaQU%`o$%uZ3_Uom?>9=8BlUHjJznG=X#~7C+bOD0)qaUZePFYG&AqT`|0p9TW
%PEG1U5QgM^%|UlTaEdY#a+*zHw;76qmDq`y?Wo;sV}71JAS3oHO#=|KVrC+4k53*NtGNAPUR`QT|>!0b=RYhaT8eVd*xqY{DC29<7JTXE;{s10k
znjl0J65{@Zs>e>D0j-N^8x2`A#E3UQI{TUw)ghH6-2iqtF5yDgw~un?5vMCIo1ES?C`^U2QL8)D<kwt%edC~&9ZFk-
N;rf|%UJNpIK`z{aAOQ>KZ79P<meh0%?X!tA2KmgS3fMHjj(M4lU|<0a*0?9cSmjSA?#h`F~u1dvamF8H&ycfzz2as<$(S9t=;&F>E@)EuH~Y_pL
AWFnU=|@pFvy+PwaqicRiJ3av~Y=G(q<%hdqPpE9+ft)O}Idm?Ax~Rr&AWEf*TKJ(5Ar?lGEYp=V9c64t2v%4fbH7N_jzxW0z?QWJ{Hl?-
bcnr9HoGkYdI=JC#LNQfPO=+uTNDbvdv5hc1vx#MtdB9im>T62$==Hs;fAAUJxo>*wfeGgsjJn0>&3uA?d;v9=`48su`c&<LJ*1|1BKwApn1Bcnk
G5I&sSLTL*E=BCetHvOK=CfMO`Duw)%0T>~Ukkpu_B2&C50jZwe`w&$rP0fzZNB`zEf!4}C$1P_d{|d7=ZLWJ!JV&t>~AbF48E2l{Xd!do!b1yE%
73WJLnI|+Xae1v>EDD8irzyd6`h&fu{L@qZkDz2v>pKgk@|-M;i5QSrgApH|PV*cu34W7Y{iJ9XMNVeM+01$l9UoA-
16LjgFK%rtDZl+I>mYGj!RPO|Noq8nIW)r#~8Z_P_Zt70cFbva^{NOyJYn+Hf1D>opE-@At5uWxg@?mp(}-
Ek1v84&6%q!yC@<=by{0rm3%K0Q31w>b=}B@;`xRY}<3i{v&`##x4bF{KOjXk=bktRJC$tH%o>PzvNC!Ga`_RvVoM7BYa3|p9{VT5Uqw2#uH$}P6
Cyg`&6%UQRnQYU-{L(80EnyIeCkjlpzA3ofTgig9suAg!mc<$_uSlHqyr!nGbwNm5i||8`Rd`Z!@_CZpo|bZ2k@Z*+qze-bmhP##{{=pBELK$QUI
=6$85qCY<T(b!>0*1etweb`=8iO;UHuOH@>ZpgVGpF{{Ng?5eHef$cVDyxUeQe9iR$x(NZ5<q+g7WmPY!I2N#pJq#g-
D7}NJe(FJSQhkQ0Rs<V_Le@NJF@Hnby1^~jk+jIPD^8xq3FlteH?(|Z+(^rT&Du_aXQnTx-ne<`+ZC7JKb0nXfzyl;*Qgbd)T28}DR<a(#eb}^)M
Ho><F$k1mS)d{KeJ%Qz!O#)8FZW~L|WS%XPKQ#kQ~N+IkB(YIIkuPU|C0QV5{!Eld+%Y=N|<L{5;d=ZPZKKKoPt=P)wm@-
}&|5(UvTOFOqSVZV5sTAE&H7G{c(-oGnSz%ABK68_Q<X&%-WfjOdR}OV1eAH<<$54{-
{e6mjY;EeZcZ!EuH#CP8^zFtrdfe*&+SvH_1<(J^D(WpOi-
W9r1a;BC}NaV90lfuhHMwAaQ1;S+7pYEmtqGfYeYDk?$smZ58tneyrPZGf0`?5yRYd(cv)z3F^i{qvn`Q6MlCqi-zZqU5i`gz$3#B46K<X=9gi!C
ax0+Y|J!Y)H9+st7F=b@BvP1Fv6;$KBHO-;CJVVG~?!J|8);mS6m(lfB(T=XX>Kn<W&Z`bOXg-*OsZN7dcla-
d42qvnxtpD(GPe2xgtu%gfIio{e`CiZ*dac@fvu4<O7dhn|WzkohSm`&LAEafk)UW1kn-_q=Cj&%3|t{Bhz0_?^wOaHvDr9V)4if>)@PClnXi@y7
g9|{B%OGG%$%zWq(VgW*@gi<WM0jpC%vy2s@%-
_JZ6m?n*@KuCrU7mr8YgA6Z)WP%;2x5ct48;*TjnoqP(4PI{_ubuU8kN6RF>~mrD^<lvweD(e9@k1!nw3C_vw-
4>pt)YNu8zG_ooBN~79Q)C_H2IZE#l9iD&QnX4X%9Q9spt|&&N?mnz;Kb^9r(YLcS;rf{_KnF0Z9ny;Q})%{#I7{^uDnH7Rf(lbQ4<YZ^m+?Wu-U
B_1Bnbex`48GP0}k{NxJv537j@A&YCkIkz5*vAD9<~@6aOj3%5hCFoIlqH}jfv5Q-
@vSdAMI}A4&w2Z!#PNRK(9q3>wwe_M78ZQJ%L?^^<sKdcO*xM?tin4i;&DsrmLGqkf4c%i9NC9^e3gPkcGZ!}Zrs;8lm&4$w7$MC@QjJ8m(;6-
QmEc^_3X+GUWnM)fG!UMpg#_>99(y`!ns;|-gDX6U*t!&*-
t6OoA%fdxWR^HFn0J*5MH78tb1vt+EJjKM$Aa!>Of_Q5=e)z_4s1Mr%*iUo~8+U{arlTOXR-`LaJdt%qskJao-
V=qqUgI;N_6L%CO|iHSp4|xi;0Yw}@laqwycI9uvarV1(psu|4WCA$E2S_Kk_cH;FhBx7(OFPe~{zO<ZRSt{HLSJRR86>pnU~FfM{n<q|bxSe|HK
Y37N;7ogTc$r(UXNkW!QRe`#qxv3|?cRc%?tg3WkU>@8ala&--ag!2UKj2v+fw*Agb9D}JN52*^0Y@QsC=yGq&Q$i=W_s2>iaD6B-
e6pYVo}GR7w`R<PF}LUBMOE6@Z(#q!TNi<eM5V>&#G!TocO5B@>DD;tlS=_v6<>Cz-
1G<>t&oRVR)TmrVg*p@hk5lUL&F$RB!YbX|qV$*@%!3rdsZFlI;!t>7#2tq5sZ8A#|hsuNWd!IX2;jd*nB`9v2Ks(M^J6f>xl^A7(_5{sj`bWp7P
sPW#E$p_<21BK7X_p*H3C_l+%sx}hfRUgNNzy`p&?gpF27=@hARuZnJ5dLH#qnOg3;2ZoM=mm+NK-
gHfVvLgQ8gyJ-`vS+72u`^%nvsv_YQ9b`$lO1Dd!(vE?L@pwvnf$eb7jyxl-AX5~rsS7RNM_Zc@5rFi56d5~djGfH>q;;xUhBVior*|G2?l((DCZ
T6lVHq3A0s~B!Om0D_?}VOkBB=kfHAN~1)lG^Tfq=ukQgj&X%nMUo<G)Z-r?4sqX@2sVEy+vldfB!vR}~Qx-x@|gVHB-
@feGRzg4mrIar^%`A?_=n%cJ~qmYc0D-o!0TJF-
0VC)PtpbNo4*{b5V{5q72{(oz(1%=rVnZYre@vq6Cj>~<S35PdF5)H6$kc{6=qb5T^NpIjTB<&Su6tqF`#sDjU6yK)W6?oDr7kZHu%TkKUR=Z(UD
)(qr`LCew4(e6H9dz8}cH4~@&KamlCxIYdBo5($tIQ#)J~7yXrMa6?s_5Uny0D1L6`1F63zt->`9WD|$LRcK-ndXDos}T38)$?gAE}QsX)}$yMUX
UP!IJOZL9P#hI4b@FLUxrN6^a@%6>W@9xOg`%oYU=LrotU$sv4Z1t~FWLid_G?7+g0gIntyMk=@0QQ2WJ60HG3LFEc`!P%B(WXCFkYhObf;)lbuv
`=LH(I4zn<wv)|qmy<lHGNBG|@si0<&oFApgG?gi>mOXy=&uXwM^rEd$L;(HKY)kglFXMmRkX)dP@d~J%weO$j-
#Gg1AM;GL6TIr1Vt65N@O?@v|fA*`=K7zcN;c>Zv$VuL0&>Z-8H}MfK?1=)Jv6-
5kzbJghs8Y11Wgw#3e5hnI&K@OcX?z{jYB<;<2L3^QAZXGx`xdaZ)o`P<%{tjrODNvN#HS%T^LxO(!a?r1^jr6txj)qFLi*Wt|Z<qbnoAX1QfgEf
Z$AT|O+KryO(X_;VR}!e$3Gxebrrx_T2C2dCX(>8nlDMvJvR94#?dqiQWtOia?!t<vx>KQ;SH=5GeI^f58mI!X|)%dlRW!b1rXEJ;^&bmq#uWul>
tIos{O?H*qvB1<lwuFg)~@E14>JlunFMOki_N3ZbQ%S7j#<JzGL#xzy5?eixdG<d304_N-(1t`O=MHSEN?vE~&bJ!df*)q2W48l>9f6!P5^-
SiitNtpOlM(4p((+LdX6hpupd2zBI)BZdAwoEtJViXOfi#b*WXB8;`z$O8RdPsOJ8xIgw3|5+&sYGjYm2I31NV~A>SQY1spXf1+2;`=1AYM0zTM6
m!q!z+mH)Zy6Xs_-BL?tPtvU0;P*Ev_qxOxsuT!cSv&lDH7=g5^@~5(A7ARubN_v49pjY!pmOym<G-
}%U(4^kW2DpfwF<O?jp2?@ig!gO^okEKeFObPQQEu(Qfhq}<5k{b)26fE<lpI^Je3)Lt36>T@L~;r4??zK*WXN>L484EIs(+g!33c9|Es}0S^U1x
Kjhp$IdZ=crn$U2?EY*R+jd%S3t6Io)<lfCI>1**NmYI7k9|-DZFy=U02AiBE6cLYYB)@^Q7O(f^OGXipgF+hC^-_<P*DxQ{DJ${8DVSi-kDq&zV
GC`Mj&H|&cYpk}ykh!!3;-
fzEbMxPJ}Z%$`^3Am%K<HWrmy4vDzV@v3#x`m_$CA+W*eU>I;L=@aOwnkl)gZZ5TP25x#u#*m31pb`pccin6n*?nbx77Eif%Eq48B~vC>K9MMf=}
8~=5dboH%MB7xm1JX`O57q%JEc8J(F2|MUC=UwHHr01SqJFny`ks+9H2%$W_#I6i9xG86O*xv`Xm&b|02TjuKtVkDHQbA>zUwhbSuXTk%an(9z#^
Ufrtr#Qo|I!PwKprJ`oAp>Av?O&tA}BSLp;!X2b<zhqka~<83t=J+y*Qkc`dgpj?fVj1Ja^u4x43T6#D#auv;}uRy*h_7eBvOYajdX5&S{URIUA+
G<wMqsRIb1+N$^(X6S?cAK4Yrwz9ucVuR;T!9xQ8B*%(J8aFxpmAwh<755#`Vi>pC;4?+;*24mCjgM){8KhZ_^gPC8~rdy~yD@lSc*boD3K6EF{g
$zz+7PDG;zuC<+SCv9RYWW6YGme!e9f6hG<?$d&<G5E5js{>Zpr~ej?feD;#ON`SD=jOyJtS?ptUY7JlfcJ*Sw2QKhZ#H!#CbTjd&?>MWun}}vXT
(kS-
#<ft(Tte+Qzd03kR+vH*q$Ltxy=KbErQwBlSiWw6PTCHO)cpeUCwZIf*?>XLv$_H&F~WgdsdBu*RWjU>D0S*E7{#qdBpD*fVh{6P$l3KKVsZqlfj
G?zskU$Ym?31Ub1`I(Tyg%IvoH!IP9Y><u0Q71+imm9C-
B5jtBM?zhMkOsfg>HTlxQa9TAFgQx;YI;=u;=16@EXQL`r(z2UE!90D^Hn9sq6NmQY&T|*3DhoM@r$ZC;$5?P08ja$v{CgsP0`s$y=4I70Af}!8^
a*eN)N*Y3=_3`4IKgCi?SogAUUlYT;dvl91#iRUX`e~qtIJmGwJt}}V;l5q;(rX5>j3|0FG=8kp>@y>6PragUL20>2`jkkgDr%+naa*5?d_*|OQ7
ge0m<GS-^kRIf>u_b^-@02Mj_1sv%iCL(Au0Mx#4SI>}zb2Y$-
8nLwf&n=XMr?OoP%VaC>8d9~_Ty@HmIPPF7Rr&9J2Pt7t`U8rh_x&tm4SNbaidv0=$kxrjH8>;fceWi5Cl$;v@+rZb3Jaj2QRPyhrG)iYwfEg7J*
A$s{HHvP{mV`@~U9J-)iQ^}eUYSxd=likXy_AMSr<aN9iJA5(Ej33N5%pz|lf?%D2+@lk7E)ORAyAf$S7;d@pcrdF1oqbSV-ma)O3S5Ie$pGo>H@
Z6$ePAm!a`fp*P{))+ldX7rdNV#OVKu1d&C2ThItPY~p+xmM!hYJA7*xs>6vA}eCsA+r?gN}oeY!)bF7dnzk#XGAr*l3={od%W{yr(pFphY#xi3*
q>gJYT13he#Va-118oP!!U-
F9Sc!G)OC`h#wOLo1s9vt_W(U#2XImXYDp4E1KzAl9ceTdg^N4+;3yQ<AVNQXrt0KH*>OCdETs~0)3UCNf<G{sLe$lG&eyu~GscQi;KlIweO7sN!
P-
odT|G`(gbsVrI^>C<8d<fHw~tcv>VcxbCq;_j6&2a=M*pH%88^7g^|ZUKad`;I~Qsh7OuXq<55uYyqKtI`O^vI@B^Ze_Sqa;l^Ab8%hHaOyps$N{
~Ky=#(mahYUjw?~-Ys?hnqKi3i+Kx~sxJb^==?0J(;V}p*HkCDY87dc$2v3Awez#9)hmfTn#9pSkc!~~L)M85b(C_}6fU<mE;Tks*u(JW@_@;-
xr%H=mw-_2$%R`^RYj2Z=>Xbc>%;d@oAB5yB`HF(_-
lzR#NK8`c*!iSb3f>6xQWf;}*<9|3bQ_gCv2U#Nc=vTG(aTFLKZ5qtxnI_u2vX1|eB*Y1Jqq5nxN5yU;s4zEI)&>m?%PPL?JNuTKx2k8g{*>uXIA
fKUpoGJgIe2us=>gk^Y^!Prh8IM~Y839w!iLbraFPIeTUF)h6-
<UT=%SF19vT!6puJi}<_F6F@d9?NmWTv168=a4!k4DR@c#A$jJtknb`RoOzG+d{nt|WRI`_UJlb6>Flw<&mB7kYYg5YXkn;P@IBJ-faSu;hEc|hf
O9HGWmt>&vhFX=XtA>r|i?CR&>@e9zJPIFil>l}eb9m%~>)Y>!H^$<Cvo2k+iPLjX&m}!Pidmx3$+BDV}xO>c+-
B;M>12qr*z+?n23Nvg=a9J7HEhWY56k(l`*b>!l-vE3QRk_jh3<`8aR_kfq&9%HQr)hOfoh_DWfS`|CNSo<SlrCzox3X%+mdl2iF}I5ds3-
OcGS9b@Uz^i%w}i!PBu(@UO$yFkq(oNb>7uHb8hOeZdO7EEKD3NqM63nj1_kegFCe)yGz4;jdUT`4?KHCMozL@#S~i@*K<ppx;D^DZFy-
1<6K<^w$2%P;d#<4FKjaEew&$L#=K2Og*z@y3#+WW8!yb4`#Mkvb+7;0bs7(3U;y2huR;!biwx_y6*arp;%upwqVsmD>?HKr-^-
*<4r}ANiM+>l3muq{A^#1!yQbSM}#{lh#I-=wRoFvy&F_O;-
!V70|pgY`#aMal1_ZPOjWri`PHul*=MoPXyZL<6yq0K<X5rnQ5eVKo2?S2G$@c*6g3u2p6C-
;i=47MHLSF9ovGf)E&rh#i^9TqmxYS!;@p=0Ogz;N`vG<TiH`Y+%ROgmQs{8qM&mIW^ncBszCrCdSv31mNAl#te{JOXMTiLD!rhKfTO5uP-
`CK39td~x(V>52n7%S?aX^E^Ryzowyh(q|5wNsbrHjxK`7zMhsYA-
C!C#6b69IMAZRZ5%8+vqH&e2~efz)Hqa@+z))fy(kKp&4aO)JR+1?s;TDhL}oOS{y`n+7fn&if@4CnX3LPo_ZcaMI<1cXea6Id;)nfb!-
&aY0;bL$@H3C8E{U{&YzFn=BwxNDWKARe$xpc}AcGbaU$p=d>WW^c#10|AzeFD{z;rUC{)PN0AJ)|P$D{uEztSi9y1}XfvshBayhBGNb7_Mg^tl+
P+F}h<OtMEc<yt1Q+tGF@^*qa`h1_JU9i~}gArZXt9iF6dLxZr>mBCwgennbt^1J@?+XxmkVlk2$f#L$P0kpt)^jGoNnsZwJByyInk6?3dpYz*jr
95?$=OGHl*Y6k1BIME=*)W^`Z7A7>`P;kRQ(WZP*sLb7XOQJO{64FIlP1!;7>Oqb+&c+o)^p%BSjp1sfCn#Le(8=(1FmBBp1xt?n8LeFrW~oba$S
o{#;md_{+G>lhp9axCFdc|rjOzMA5w*fN7Ri2pspfXJe=Nv6`Lq{C4@1-kaqcw0HiRuO1_Uw?KwUQd^dy}%KK>vr77fcnRR*lkuDzcfup-
q%7=oJgI%qou##J;u`%HfLy3APN71Nm=SXyS)+PWG)$Si0;}(}p0Wr2$;>oFeT3^YdkGBtcyY0$j;T#-OP~3Gz;j{-
VFRO;@{~dGPc4Y~t*IiAW2iLqB8yRd*>iJ+4p^GFb>F8FSBUqPWHWm=WMCh`R&N>_I-HW_nnRP`!A0BVjt*Xb7zmo&(F>^D>evJp|O{^&sE6vdKz
m)y%9cJd*4EEmC$+9rNe$1O6k?vDwRnOaf^n(AP?Kf)?sbwh{Fn_8C->$!-Al-
~=zG4yn+S<9uiqYvfMnm;5(vJyARcO!mi>AOekbB+POC9apIkG5^yvK$}E@y-&_*<MAEkOU4;4I6sM+S-
${s4FMENI7xTpk)r%CAp^rZ0d0kGzSu@I!>KrCNYZ2OV2rK3{Sa_ZbuwWijgK6%Gd@*jT}G%34j3sB~sIaX=2_3F7v*rU!CU)C+)Mx}s{7_i5^MU
(EhYbcYDJz?nUq#pSB~U(dcMJ`yE)t2GQ8QE{btm9K_17@?|B(?qOlMs?s4Sz|$iV$gLky%8B*CCmm%j3y*Y2DR?ds^XP<u3F9~DrcB2o5D(Wmn{
1rLNl)@vXWX(!l~y>mzg#siv29`M~;y}NKUAva{ZB`ak&%~uv^yEpZ#-
In+@?PyzM$Md1`3YFNv;{x(#@J0jAM$#KM@D7X~kTDO}to*#k8N5D@+@DblToc>UW*8GW-pl)T`s>dtrWa>-
B_cNWZyW0+Cavs&6>MvySPovGj%2USEF?MaoihHrZ>X6g8G9=203dbpeLn%3Q#%ZO6#Qnj39Cdkwg;Q|T;k$Sy(iAzOL%fba{*nn)+bf(i(QgE1+
VQtkkGlO`Sh2c#^B{ac$LG#cc4-
gCYtK_1Yt&Bl&?AxpWJ}FcGb12KkWm1PyS5u*(675)Yrt(m30*S$pudUs{BD5)46NZ$kStp1PoL2wR>8HLFXZY*h!^j5KFteQ@CER>>f0kR8TdLT
?z(~V)kSA)FSP~ZBvc`M&msEFNwBC$-ar;aaUNP6hU%p&CY*g{Y<M6yOA)TLi7bA!T&+vI+hS1WbJ&}8(qgY}hZy)Nh&1sCu`YODA*#khY;uWt-a
Q#l1&Pmn)GP{kBntqD3nK~FNVARKI9aGKLR%6yT58k1H0=f*Ll|1($&sDC{Y}M~It$&(w70J-
&Xyw6JBULrL8@et@jelEPOtaV?F?#NztI0d(Q`f2oZGgQ1y7aXsC>Qy6SPdBeTL&@iF_&D_VHX<?K$X#EmG-
97vaMX)CR$5^HQdm(uU7n_%bPvHJ7FL<Zy{AJ--dY8o)-_FI+#xux9do#B@YfDU8d5*M~1eJ%FT3NPR8!#>>-GCtzeGyqOi-dJ)AV!>grCLEafP{
)j5n=9mz``|0T3#!XW^LAl|M^humj6UxRl<{G6Q%E7Kh<X07uSMf$`Hf(a&yJG8VN{L7W`GS?g7Xsr)PyHD?=2L?J-
FtuP@xJ$4AM3kV<dZJ>(*)7pP)2d#}MHP+o3IbA^{gXK3+8#^saLJJ>zg5uhHVzc#TcM?^lw5t;0MZZq6C<4se!=9o0&bFM)pvz-
<9$uO(d)r$bU@IX^k&dmp^?tUJZ&xASr2Xii0r_46WC{_$32>BNfDA6aMC+pfu6CksebA_RfbUN&>DA?7!d<-PA<oo7m;tndZ-
Cw`6sWIf4pU(_^#AGS-uf{A%Xuu)bmLh4jn^M=-
Xd6q8`j|$9oJlR0#A#jOMLV1f{pgNXcf6&M1^SC;^|aOXUZlS8_bWBlGb+uZR`@Xpog^;uQ(qiRy2}&htrfbW#twNp+-
whMismg{&5f+N650gD(%!@~8_A5Tgvg8GrNqqdJr2%^w+c5u8|13Zm>36^l~DQzcf4wNU0MyZT3!UeWRmPCpwm%0}e{Ki%3#!DT3NCxrigrwNg9(
n9o?9F#P|Xi|P@?+)N9URbIr9wfej7Jysqg0lDi3+5Y%CgSf6G@`yVD;#vo(tx2jHtW*fRo-8;Z}_PjNv^)s9*~F~GWrnX=@dbQ-Eodg#(Di15+F
_R#C@NstB7wmNbY!mx_E(=FWv=@`Zwdv`!r=di6*+vKpl@$1i^1zS6a%_%{)XQxa5i=fFh$C&r%9)(gJ{(4oU+MxH)SprGx{LgYgmhfD7lL@iz#E
KDLH#H19S^z+Y+uFy9!z(zd*3QroLp@Mt}>m%e0;?pLSq4$A{6brMcM4#s5s-HlIEC%I>t4_M-=cAUqz1QCx%Ar6=Dr%WD6a2a8m&ddL?txnS5g-
erj+wg&*y^}}u92>xsh0nT;gyFe|R&%MdEW<R6j-
L)F&u3Lp95fgGmg{yBG?%+A%upO3LOmg@>@RchLk9FG!PH7^Ft!<p3E~yDVqTF*40BCB%Jk5(@7fSX)`E^giG^kxk$pImo!inv|NFGJW6_tBT;T~
MnlNNE^8ao-$`_1O{198*sh<bj%MFf=Z`QM8n|iu(rx3Ws|HowH3!3^~BmQ9-
umOYXhgLVpwVapNrT3XL0+A2=F*ispjuPt|q_?Wmx`RlTm(HdI!h2~*wqFxHJ-
e(OMI0E2q2q05k7q>*NT#>MQ>D%lSkS2sR3jX2;Yt%PBD7BhLstH39X70L;nn~YNamMOqr@qG=@KsVR_$3O$**Fx^RiNiK&ASye5BvS$!b3hT7~U
QFO+iLDxf4?<KGg~`Ky^aKP#EE*D^PLV;L^?ABb$ZzRtn1`(=#zXf5HK>*9>LM}Fm<lB;2rUM=QI2kJ4o-
U!MH#AVv$((C5Q%1LAvp)co6+P5zPyi~j6vzE<cRy8~q2oJIOzc^_Iemi~a@{?>?w7UK8AQdtS(=FCUXymW)hv8h%=F!NkxmE6VbcV*FOk~qhGA<
6Yr;#A(e(7>d*V!~goMh+3xT*(Zr{}z-Hl}kQ!xah{vO>Q7{!*CdVrL41aI%P6!O%;O0<Y`FnB8%ms?@>v+xFV9mt-eRT(IDFjf|q-
xmy^~ZvwE{!goV!smW#&$-
(xKJ3$GSfK#tVLTHp&+y9`KMMG<%F{F!T0$A@@m??A&ZgnJ8xby{`4oWXkF(&QZstg0~kKfWR%jM&7LZGY~XhcL1o?5i9K}xx|LaeJ&rF5`X<$Kp
fUq9zggAr^WG}8X?6v%%fz(0RmJ61v7;10&C--asFCP1m6AW{f6(+iEjTAB2iloHZ-
3z)$a@FtYb;qqawyT}>HX|j82J!^J@uEoDS)f8#9FI;`2v9F<?+X*&;RCx^WTDD|nh?cx5`<%17ivIi_2$yd(i`Z{UHorQ}h!sH+0;X(|!#&+<HL
YKkfryI=dWX~RFAn`}wU~9BWQ99&dR`3SY{Bu(A&x-
ac)e^0rK)`8aTG&YX5k6VZ4~TrH7tI95q(t|YXurw@#toS9u?wMMBHhxPRc;BRi_yI;`@7?m3_+Bfmg+@2Gtai-@U3JVdPHWcSdOBnSQ3Z-
IJrmPRlM($RnuWime>##T4a>=)YSu*4ecn6U3L+hm!Be^F+{MrAyWkt^R~zkB3Bhcu)8t^HHF%`cIHBoqzq`aiWsHw5(_cFVMC!V#nVb*cTXP9m`
p$Wa~qQ74U!zP7`{s>?p|;_YIB)20M&;mO-<nC!=~DR!l+ettsQ%Nv9~<-Oo)oeaX^+uTd!p;&QpU#?X0O;q_W-I_Eg1+@w~!yg9sLl&+dBckB|x
Bl2Jf%S+jAzW!*`V>gd2MRv(!rL?RhQnum+C0_%Mx7Y6-
mfFmXkE|%o#7EX2wFaQo?F<K>>EB0|xg$E4WCM}p5Hek8l<5ym87yh(R+v9b+2reGPs{pseKXC|$Y#F2z%WoySm-lxovP1gKj<A^PFNNB-
zt$dWU-oh#SxqMGQrmE3J~7q?Cl@YaSVKSRU|nT08H-@bF!Q)yY|D`M-
RXc<FO&R1u%`CDK9=>HoJdPx5!$Z&qqos0DSZ%VIy^<GrmDbC97~ei>sb9>zfsQ<a-
8YEUs%4Z4_mOde7<Ut}3G!la}K!;huF$b*Svx<Rs1yVJr<X8;J&e7aw22FxY>8!{c5>S!F0j@Tkqhpr6_q^hsWXPzxm)1PPRc43Wr3^aa>h{v60W
v9)32oP%4MF|WVk8QMxi^7nhvp4J{;7(sJ7-
vC(WIqLrOy1#7R;tG^@L>n1c@dmDhs2c!c7nQ77a9yO);|bGA;vvh@L1@c%rtqkP&)@aOR^jcJe2`G?LTy7*q;aXiCFF2){$6uK)DgT?khCWoM$g
{^i{Bs@C6*C2S_xB@yIN23##pdy$kwN-OX=^T2r=s)Bz|w;(I8~`u$-}b)+!R306rnX{gH;=PixdWfEg(a>idW@Lb{^#$}cyyNaO85s@%a}6v@7-
#$6ArM_sHxzj@mAHgBVwBA{l9--
$!g7+p&Fx}o8yLw;K~jS|`P(PBR1wc9YJ(#*ZZJI_MvCza?n;j(mQ<Zcg#UDr^y@BE$}uEJ7ONH{$|ibuL_kI06Vk-q{-
_38oCh2I%UFaUX(GxIv}RUO`4;PWxRhcpWB@X;vBMyN;WsehW_PaiGVmy<5~M3UWwi$9*kTQz41G94e`Jzt%g+ubJ6a~PSpCI@9wU^QlYsPo85hH
Sgpl?MHhUAC|Nfcz9=vD&_=?X~F?+=%zq=sHYC*#f8GiWhtSFq(ppQDaBtG0MJ65Jz{P5UaX~ySoBe41e77p8f?4;pUX8y27muq#%f_R9o*u;KMD
QimrLsz1Ax@6#r%mqVSSCgytxfPge|SE{0iKlFxlnL3k0SYHAXccyA!|y;b8hvWH(f9vxC5JJj_d0m40*68@7-
lD`g%x)yx6X(zcz?8tMCCwM^{LXJVIpTP(6ax_p|9#RtmSbv_NtVcNHFjt_BLFN;Z64huJO4;}s1_;T~iI`T61!|6DvNbyY--c7gO^A>YLN5Wfa-
yGs_>T}F!b9yn<6V~+hM{$oOfO4LAp)#kJ6(<ogm-(RNAI9E-
FHtp<J*Mr+|qeHXUBL68|iv}jV)VQzF_AFr@rnex%97)$H%eLPqaZXk$;sjx?1z{L!$gi=2FMFI#r_Xt0B2*u6jQt4=@738<SDoc4y<fmXWH<vM;
a9{gX|h4rEl<Gs>R*7G@{D3NAzfzuT^*{{OL%@d{47TaFzdB;7oHrdK!mfZNB&MzG{J)Q4t~fUbRNwCo6N6<}z=CqzoZE|%K~erp>NF(zhJJ{iJ5
WbKaF<3<xnqp7nyA|8Rf@IZRz!t+*vQu_g=G5?qIiwMfS_P{_{_GQQoj3MHD2YVN{ELq^XI&6T?_$h8vLD8E?)lP=mjs5-F0U{-
8Cx980fQ@S!D#1AZ()K)2D%@$xdNVPV8Li%1(3DzN$z@Rj4m<K%V29RqRwt8jJT?$(HZ?#H(rqS%-
QRXM3;ohwgVgsx*5y|<2q0wY>J8BP$3l(&d4*g&hT3MKTM(BPpaksP5vvZN(|B)MbVj%hy3;NAL{mg2_Zi?lQy+ga{;enREDTx_fcZJUBn2T&MVs
;fGUAQj(MF>X`mqw*rv~M-
zc8sH^;ffp6Nxh%{<w{V3J@`;Tr?zJl!rf(MgvMy?`CViN$a~FrOe`Nu^?dJXSiP28;odzDqf4Ga4+fgvo?`34s*%C!cEqmd-
z@o6arfmB;(SAO9!R3hsMax9dn&{`~{=+8-;-dYf-@QCucTNOXCx76<N3EqynyrfW9cGCFCMEdsp-
Q;3d<@c!(i}T^dT1h{>bG?{`tfhPjWh!ZuAD<dv#?u(BJ<=W}~3L<d_%R`Nuza*|iY>Wzy5v9KpOppu254rTLy1;Ber5Sf7>;FLr$GLq6^jcsi)Z
pbr9MR|IN09T!}I;MHlT6yqpZxRA|FgA~fNXao72uG!c?CFy}Bk2w@rDZe$^bT|YC6*C=?1}B28ZS1XsBPEuTG#zNO72`GXQfUS^)%P<5!*0f(d5
N80%7>i%O!Pm6GuJ~U~aBh-kCeoqpP_u8W37-LtPA-)`|C7-Iy@h#EhsV6E0k&z>}f)?RN-MR*_GeMU)i_yWQr&U$Hq_7?E#8*ztn!e_O?c*^jkL
!<#Ny%gI9|53A^WefXf~d0u-
shus<tn1?)aQq=W!Nyqag!C=z%w&a1wX#D(zpGW_s)G3Hwq=aAt2*37~2yAMaPQ)1~yuXv1&c7sxd!+cBC^)vsFT4}`<*9K7Us>r{>;?ZM57jiP7
BrXU?i9d6KJ!`{OMDyrA2{ty3C?qr9r=m2W_u)m$>;zs-
P<JArh<Wu&%cNI04fj5=x_9)Hi=DXmMN?F!F0~heYl$|8%Gbii14!ZBj8xUS8b=HHEtiuR4(^HcQ8R!Bjey?45cYg#i4;v=OrrZ*Vrb@o}FVSM$+
OvjEEk3XO=rZWn<zlByHY@^AATn(J*fJ*OW{sl_#Kf6PORO;J!66(zEYcT)iEl-FjW)>~vE4WHb~WvvOP+^D;-yMNs-UkKd3*it{(VbGn?H4ezu|
=B~=8#x~1cqvn1Xqm5w}jD+WUUR}qxra;)|ig&$B&)eApKI|#Xu6{IqHXpf%De;C{^L%Uyd)X@gmaeN=;sqwR)@@^o+Cn_wGG5y}wLwo-
3E6+Me*HddfQ(D{J-Cn%b~Llb!#hQq+Y@;Izubt?J%=}I1c+vh&F}sy+}iz-pW`2`Sj)+nbVl3qB+*(Sbj>&hno1?`ku)_~Qs9>n&7Ntet57Su4)
xCt$jz49zw>za4t}R5qHyVXL*C2M-<3(0+^l{ejYm8YPvaaLPupLgfvKb#-
cziBv;%<Uq$Xkw5lR;zL@Zlmsj?9noa!3*O74Q+nFHginBhP07mtb?%^|7Qfq{75R!B`xc5@p-W$r-
zIofVSxUS}3cYU*?{Xrm|g3s)B|K9oc1CT`2?JJ%mEP$`$W=@;gMO4LQFHW^1L|412bkIisgyd0~r&pEMP~+^(zdjMBu!C&wHWU-
=r?T#fl3oa6DwH@=Eft%BP~nws_Q`$kSI=66vi8+qV&%;s5e$x2dlPSwu?3M@T?ukQEcD5K!{fgE4RtgJza&u~m7Z+fAFoDrn?Ut7@xu!|>^Xh&r
oYh(D$Bv%g=z6p0iR(i3Eij%)_k1d+j;8Kr`yJNN%82ghRhsRSi;{<Ddn?bHhXG++ha%#<ISxgtJ2An(_WIYZz%?zE;W7S2PA6iSZI1oLb_XP#4G
PD4>Xc5ne8c)7{KKS5#T@>%eX{w%DZ}tX#o7RR;o9qLNmB}L3E2=rXv^WSDQX*^$yGda6#+EtFc9F4Z;vx;-etQ+#R`by++jcLwGzjcA~dJ-
L2!J{KPSuqOrmnbwt52s_B!4XEO0G%OT>L!7l{&%#@g_`5S$m(@=98(*!G0SD7bIAD=ZH@G0Y&8tT6tRhFO-
Lm}zHLC88W{}c6==QG;S6%J!7IX8dY-Mg1XUUOFHa*yh)Pf82}E5@t3!slFyODO68ij1*Yq5Mx1g(vRf;fCgva#CW$xUUOsi0EG3Oia4GK>708&}
|ecLX7;}+GJF}L7-)z*2G29u0@Q|q(yxAC<Ha$;Vr5G%>d?v4IoNB+l-
+%R>9Y?ggn(!>t=Ad9cHsac!7VIe;^|KdldW*8YU7aXs&7*eh@*5_ku(JkDQRmnecM7*dZ(s(rnW}E>+$<82%5#{F7`;^PR6U`!H73R`Ck)%W|jy
*0-aFS_3^|%6nIq%~S)5y@pANx+$Y~Fp+XXq3%_b(|NPKHMsxdFx%n>8~W0$Y@W5-
23}!(dbc_u^r#2^zB#V(93~U@5#$o3Uw`lrPRwtx+uFs8wHEpnJ_Pn=WJyruP-
r(zj)a!3lpSJM#K8<zcgdaVP0M0i%S*AQ)x2w2X>=DHzVBY+m8Y_x3@9UJ`*R}}-RCXZ#M-MTG#Y=~E6pz_kl|-Nr_|-
Dng0Y1D2x82L|=4_md>nArf-
f!+EQ#LW0J%NW>NAOq94GWM>~dGc$)aOwYo=qA4E#RDKAIZ?ZW6;Z1CiHwPCxKm83niEKY*w8qhN3O9g0Cq{%F7fvqpm3~vJ*?rFN>7vKLXZ&uve
i+fyKkjH`)JKiXr5fP$1w$|c1zEub@zfux9XM7>Fx>MQND(*e6UHPIq`mV!yUBpbqa)PMv2BETE^wFh-OI2VcHPt+3bb<aY0qh?NDq_V!yB&tQ3$
n}|J+$ft94R6#Vgoof>Wsu5xkq{zy8H);GP{TSL#Y0Nh=2RtviYSX45?-
A1xA57+2W~}rJipZo<1{4i&&wI^MF#$LpB;_W<P0ReV_9pVdcygdHI5Zzj>+@Oy1_WkfS?=2#Scs2eHgf`K0vJrE2AG<`qVdX~e;Z=strGEL<ns+
m59R36||!Sz^ASO7FI~tz0#2IOf4bH)`z|S(N&K(lMppaVftvA8i;Bv3_;_y{BTf!&8@_><v3lS#tHK*2Ij<Pre{mD_p*bzd1cQlrJL5FLs^&DId
1=Hv{Tsh(izvA|b$hebzhmttxoiND^lD=hEjd<fgQsURn_ZjLSCEt^h9pd%%qW0~AYN3;!RujAjewmsxh>%4U%eaTJ7Yd~K>SBm`qWZ_L^XYv}Fq
z)SPO?=E@y${c}^T0y`vuoi@Smip>KRu_49R;qkoHQ>?ycKZl7r=XN9FB~OLx^0$IaRN#A6%(Li4!>31V>jk>mx+b(P6TaoT<{jF>rxeX$_6}On1
lt|Or3PBsd<i~9B;9SMjlh1t`4B7a4rrQlGo)?2dwLK1@`xs$;sWJPqam$u3yl4>)haIp<Xp3tDI2fcP6+<NRtK~X8@~VWzU}I>STh6^C^&0A;I1
qWbXUm%e3~XnW`pTCzkd#Nyols0f)!V;2!vV(Zhyyak%Q{leuDd6QJzY)zOk91b@wk3Ii9F`+yKI=sY>C^<LK}YyT1dAH2Q;Ma*~0EfXO4`U8zzr
pyNJjJa4VCy2>WJJV+!ikX3T(KcepQ#}S|7AZmWc7yN8tY(eo7Z}?<<4H88tM##x_&*!#dooFi#7VHao-
|9w(=4=*rD<+HVkg<4v2I5c$fSR+jB(<&P=EkF&`qC)v-MHCIb-
X#ljA=%^ZjJ4)J{o=iBY$@?JMT8jJFB1f;@e4suXfP^S4@j9A{(c#pj1xX^y(_n{H!(D)pT%aVLCEy+X0n)b$;r8HsAO@NA&iwhK()*zec&*HWA1
4!VewxMmB7SM)kVGy>V{$NEG>uCtt+q-
2C{p@ug;^3OeD$y;`9_56x@Wo)a;rH!1TqXaShrH>av7tsDhn^)tS2O_np#kxhBB;h|M&0DU_go9g_Q4Ff2qP-m1eY-
;b0S|6K1C0rTfz6j*%$MbWL~e}t*2CIr9@He9XF&augI~U79}u7R@f`B1-9x3oER-
!@ol|%e`LQA6M1hac2sWF&t?!^WHU`{E1IjnNu%jC&mVZi56*NQudo<N-
!K#eQI2{h;<+X<dTN10zrH%PrHnny>pbq&MDAdl980DQGhW0L2vX|SAv}M@SF-smG?#~FwPq4R#)8OoxM9BejDF?*b()`bi0}=#nO2!9=^qFS`d)
c>@owC?|fFP8Fv{<FAK(EL(@O5)iCz`z~4Qc?F`5AxiC4;CH+P4?a{lhelRd4lv(TzGf@})j?8x*8m+kq&kpMxf0ysGae>0iNaPEu*jyF8?xG_4m
IiR{Nu20@4aMFr4jz4|^bn|_Nn9rZ<@(<n726;SC?1UA75YH;hDmn>S|J0npTm(Wa>!;(A+N|t!x7QfC)mYCG?JlDYI*vS@b?X!3_530%>qvS%4m
G^?uuf<nxx!69UE3oa=ak0A<<#>oQ#%V(CrQgED1`FA(Ek8xB&I;l!^yJSP0BRaCvm&zBZIN{?azF<hY5FjPk&UcQ`*eRL-tn6kZje!O$CUm^<H|
dKWlh?YQ;c@=4?9bX3rF-~Tdh1|Ohg$Hq~mw|?-E9Y((cu*^w@;j0ya~B_K9gw*|Dwim}%eq1r|?-
&}hI6+#=&DcuJVXr|+`f`Mov$p_QXUR`)(purq-z-hv@2%Rm`oaI?dkGru=Pd|U`cgMb0<+u##$_&SZmcy(0mWYlz3iJQAT%d-
e9p=(q=Md+f%LThKzNJ!U=`SG^c{oX-
|UzgkaUP+h=7W_`_%|S`N7s=(hY`mr0^4jU@RK^%r1c~$!j}OK9js}XrsZ|bV$}@0FMNZ#d4PfJ|CpqY^csk2~fJgW(HihYuI!@ieX`tW9B6#yI>
7{rfwv1o-qj;79evk~<P8dgyo!p!L(5~5Eno#VE{Onv-
X6PpPHd>3%#OrA}49a9F!oPecY=mchMoN{z=`BNfnm}99TC|NtR5DWy9sn)8wq4>HvFmFZVnWv<gU%oK1A(EKAQL|E)$Lt!kOOuXl~^ps*EYUJr~
<jd<8*aQu9`M_yOC#T<9tRWXs7D{6gY{K1gCQihex`ktm9=QpIn}_i_6E|jNHW&Uz7tx>0?|We1vn|7ss)ZYOq|)QID4_cB$AKczHE5HlJO02D8q
F+5XtnV#4JWZ&V95;JBS~-k}{|O(`LjDcSO$CF+C@)RRNMgrPtE@m{5ZcMRt%YaX8Z#)F{Mm;D&!)8v*$0AaFdov7(Of0-
>~p~N1H@&8hEUBnna2(HtR-VF>Oa%XGhg39xTp%2B<iv{xRJ8LEKA@$5hCg7qMCD<CzG34+aL0WevJ1{bTyC|IV7uL+e*N#!q(AH@%;8_5xoxsmf
ryllpM1#qTdH~!I-m#W|32ei-Oc~G<v)pV2UQ7~sLH$h}78oqK(+J@{te$-
dU#=?Bh1jh)O5<$2CIrzs7J4w7Q0~z=_oS;rRY&fI0kf>k{t=k#kzGjAgcxG=JZLY$XdqZNgXg&SK<|2UklDs$qFl^-
JwXkeuNZ>*z_WGT4u$T5Qy`LL;eNM(7+Bn=-
pRy0y_}yeZ*8l|&h^GZQ+%p_Sbj1TZ23+`;uRiZ1>EoQ*+U>l1^HI($X+M<BI)4=M=;on9h{9;lU<c>7JdQ8*A)mS2yeO+DFPaSm#~N7#NC1McCo
MF73O4TEY`0S-<TCN+aihD7nt<@z!caV4XQG4Ho4|!XHas53FtFlv-_Vc+2Caqh6~ozqG1v7Fy(RTVM;hrX7NL%`gt#-
tAI7Iwm|8$8MMGsYGTeY5i>7CkoLq)<}?if=R8lDuon~=JyvuX8urZ6X@Y9VK^)WJR+b#>iIECh@#I=`1X&8lX(9b;QdX|}IoE1H%7dePz-
k(l5Dj4ClrV0nQzT{x)7SdnC|S((4OSxaVOV(YGXob-e@;XeaoJ$q$ThL61$9|MLyCF?C;-
~j{5k!He9}3%tyXLTEInIl?5|RQis`z6!ZeRYOK=G}*~EsO?@RRJ7~41Ja3@Hc?mOCZUXSs>j4QNYPe-oowOV0qlNC3<B>+J%YDGX^q)iLWImpC@
t{cwAalyU>ryL__|Acuv;*A4*fOpYwfl34WT>8;*{=Uh*Ua9tBvAL~V24<G3ZkE^-
Bs_lo$kg1X9n`ve>=>vcuCank6_!sOY@O_$^BY~9(tTs$_vl&z5Ij@zajovt9km9U?=OQ=)K>mUhUOFXcaKkdKWaGtP|^vrPSXQ9Lvd+r4c!J5m6
%1IAzG6ot-VZjtb*H}Y$8ZLCp_;82dq0aa`Yn(jP1zgSyJ0;wW+ywU4>M!_z@^NvDkF_<ZWl7KCrYd_JqWMyu(`Kp0c&=KVjE1Lf?Ei%R7mAS({8
CugDSYw!d9YVc?andxIb9kOXEUhj?&gmZKiFi7n&mCv#EcdI}IFJeM?jVtT){&_bUrzY4c9=|#yJ+D(0};w%MlIP^X97r?8;#r}qkuZC-drtbMlf
=(?>DeQpK<h8hSmXYLXD?|Y`d&`B4j%YCMy^4}3Ay{gG>ZiarRdJp^Ac(?xUh_VU*qr-++ANkMkC8JvOKLy{(LeU{mMKk?wXFAQSwOH=kHt2Iy-
X!3vDR5Qr!WJ0FL@hUi4#|37Zw;VdJ+E=Yd+D9wV!=2PctSbPmBqruz<dIvnrUogLf(ga7!=NY6A>dkbD!a9FQv|^<k(%szWh$X~S~_Ps#oL!2-
|R_CJ!7G@`zY*QWW?2Rbg<yXj|JI`e;!4WSdQAy>iTvhc7lR`GGPhJzr<84pNgQg};%9guXy$RWkj(7Nk?Ti8`m>0rkX%~3B3d^tQiYg*2XRl2L<
{O)^eNC)Ia5~82)O4bjVU!I`{F=AwHoPf3C@0u{S+S#tvJ-BeURGMb4S+KESvB?|DHbnUGH33dtLV6Uo+Njh*b5>gzTMc`ULnX$YQ(~AII+ZF0nf
A&Kw=L-
Eh?ENgTeye<srOemAXv8#GYfEB_Jy4>82dIN(bv3(wv$D}@`#;a?6Eg}Xr`IH>&YeVz*e(cr@Zs@f;zmo+zU)KBI~xPi)y;RiSI243!5e11rOdTS
?^7Wrz+mpw>!H}F=AUXzHbiw@75yvk)Z7w?T1ez3n6Z>rxS1E7#{)4!|?8J9<-
>0AZ69+@1kT_LQQNhydW*rT6_UJEddNpWoc1u%S#6#<D*7EQW%S!I*Z;Vv{n7%9%5m#j7N=GJZZ`mW5i{Rk2=kh+KN!BuBpaSY-uyRuo3I?pw*5W
Vwos@4_ml^C=OXo`2&$2Z`?Ufk$H^|iX2gM#NrrXH%x8|(z7*LM1kWEm!EVp-!@cX+%5Ze+o+&!(486j8u|$HU5R-
G4Z}spS)8U(%MKM)Nst%Ju0{ItwQ+C;+lXiuF#;Bk`4(4;Vj=aTeI&>vkLVv+@!hxUq6~>nyz2j*2TalwN5?K6O}rWj=Q6FWfO|H^S!_%XB)G~M+
6D0<9vM|@<1g#{St~UA-|bs<iZxC)g$lSP@LUw(tc-p_09)SSRu9`V?sINfhM>ZuJ4c#H=??K0LcJ5|QI?qV5$3Zm0INnIx#TSFAw;c6QPhZexeo
xihdefFcpGDx=gs5oJU(Fq+DaXzVMN?necVQY1pv6b%ScPb3E3n(#^@JTs;Yf7cksA<NRvV1kh4w!1Mmw7v^I-vjWG-BFQL>q%~wWyCs)>)Uq1Dm
Zqf<#pm+UJQ~96?Cr;$@x%2`KO~*P#HMM~}H`5A;{c|RFFmxo*MA_QzIXfhCvcBJRU3h)iF^!l{+Bhtc6#;BB82Vr!Zc@%OV9uE1AG{&>6q>EdL}
Or>^}Gaae7`(i4>~Lyf)J;(lE%*@TGCd$B*FhpE~*2q+J{t+{MRpHA%v5yly5ehxugKQUz5g<O%0ana{a?cST3Y|Hj^E-
7O&UgrQq`nhNSsTC8+{yEwnI57%{HVW~CAN^YT0kX&9B!)545v#rCOc{R-!oWJDFYK=qXUhtY>(toRX)4`qo#ooapTghF$^Dac>>NrGD^Z-
&&VdwkR8rnEz?WoVmKIxN;m%+tcX>3{iW-cIe?qLi2OjEFk&=%a~k5#>Krf#Hc)7iJ04!Bbtq-
`@HmqLq4wyAgGkfuxgZx`<d*mxz>DHlnW8XK6#4!A5{@1p^Ocn^9dbv0Op}O9E|5upg2o4%sDDJwE3E3eS&*h$6=H+mHgP`)t@!2v=zQ`J*!|u#E
hWh#TRj=BTun3zUZ_3iM5M#MUh!J3TKy@acfKx?S<GT~rC!ps_QEt-
=>n$7QLvr4uT3xbgK<&t>}_2K{#a1u%)YTDs9>mxwi18#IgY5l4my6A<RAM&(LtMXioqQZJMqr`zGUL{^(#q3g$nnF0oHY|farTYwHw2nI@Q{gwp
_n!LZnT(gpHH+gnfKT`WB8xQr90JIC3KLX+n(^)NlqNWAkLRfe_hZi*m%T$NuT<_0ViF(dFMz_l8=w7hZh`d%mv}b-
98I(<Z5OSv<&?LJ0kmU)2=;1Cu0ecN|x!63xjeKv8?Pu~b!k|m#-
)$srW6`i4J<uRMb7Ok4oHRy@JX;uLswPvhmHo~xa)66@V^%F89qOYMcAFXmWuZ|&BGmVLEjMM;Va;O{c*XZ}ToYf3Pkd$MwqdDfw$#K%<y{y(pqx
biCT3fL(CyAk^N*L~JUu$gP0GwzKT+9$Kx>!7s-
x*4N%L=4+=5Ufg_6o64J_kfH{0oOa`APoVS?NVqr%wR+TEA;=*TTF^xEBt!`gppT8uih6>lKZFx4Aho~X<i7cWA^&crgPYd?{olUI=)X=c;*z*kU
TwtWj;eTr=#O8n=)a;HR_h?9Av)pR_EXdhd}2d7D5GQbw)<>W78D$i!E?iKs?x!TE**fqscKeicrP5{&Us}+JvGO+L(bqV9EdU4BgIwH11CCnyHJ
X8Z^`pn%NhEmr&?<OvlnXt1UA<Ra|z*K%Xc&NkuCfmVa7L}U8^YX58rjKm#nxi%*FOiJUg1Z4FWtwaCV7W8*MP};~hvp~Y!!imKNY+~7xUYCQSRm
G*2LN?V)qsqTA5{0MZ)1oe83h&Ivo|O{_rvWBZF`Y#VO~}}=tsCleP~rVl*gCs6@ZwgxKEyDNouuG$g~5_Fa^#ZnL6YYkh~wO8G3&iZyvj8K5ZmY
C+vb(ik&uZT0E+Vsi)KU^?)0b&162Yz#y46nVto`$a5xmG(RDtFKjPF$e|ORD?!G;+7p$e7-
`{r5Ff`SG9birG@&|16wj!qT9O`9upl%6)NQ7a$j-DyLcikb{5M*1)!LDNDeIjGiN27qeZkDgk?1q-
_$e(==$@%HUPDLdjjmvTCh%5o8O;<3J^b~13%Y=D`WK7B{B+0LR?PH}Ogo!na3*p{Obq=OKJ^%zZLnLju)>k(K*2Y~WchC-
7p<eI>%7)lFr4{0$KH#boOcBCrC!1t5iG!6YugHu4BIV6qEgDhft7y43OGCdYM#+PikVHTsx}(nJX6F>{HZ8}nVxF!68yNUHyvqh_~IJg^9N_3&Z
<!~;g)wCGclLJQo>*<351#Dk-j74t+Ko|3XSQ;vgo~9`olLE@}9z3XT~!v@RY|8rA{gKwu$nR*l)MA_xM8UML;u8sLsYAl;(^arE;(Dt9j(Z;*-
t5>|a5LiAC!BaKfH&6_q(+V1Y^$yG7tQ8HyJ=-
%DU5&vo8oZ8GDL_dknc&5_Sf4=~mh4<!X~fC3{X#`QgWn#DN?OGEu67_Qa47aO>BbX@Ee!m47DGLe@#Rj?_63P<_ZM651n3F8=Aq)?9VH6#du=7H
LCxwigQA!9X;`6IES#}96WL?7oReQVIO$J2Js?yM}7(Q6k~v8SzXZLnwCkO@{Iw4clTcE`bLpNgI*!u=acGUdj4G5Eu)y^MOV=h5UU5~1zZr5>_6
?ebY$X^HHE8Q9aTzL}2Wg_M&+S%OywuAL%)X#g@XPCB{RPNp9FWM^SIAftZim_iS4xiobM_f07AmSjw!<qU;f=YGZjECvv*d;%#c+28JEh-
P%PE4{TNjbIblmdf`ANB>l_LYC^hNNr?cBmCDbie^!x@p}f}6;;)izaIC*AO`SmcbZCdYhkuOWT`g|`_4P<kUvys0vThm$h~gXqPE<rSlj^39@6I
P?rVc3N>uKCDptr%@FkXn!bi{KBbp|#sh?pFYL8fDlgL2}r+l9|%;e^`F1?4<1`!Kj4kYX=Jj$s24_(4+RPYVD=x$ksskKC6$!L%k7tV+1>46$tl
a0=<Bq=LhS21s(O1bgv^qcmNtg}YsA7rm_US%KL_}kPL_e=7h;eFMS!S68}7<InLyPGBwj>KER`hp!~KVUp7J*V`?QXlzG&x}$3%c*s1bJBFlSv*
?21mp78+K83jHKNw{+*B(2FAzGyc&rtn0*7c_&t?roLiX5L5`ige?n?RtX1^7NNyKaf#>zIym90saf(}yQ1sCRwbGVC9W3SEIS2@sBXrnq!>ZF{X
VHp|v?$ns*a*kBpXT02nj%T7|8Iku0XE5>b(z0b&FTQ2JfTw3|Tb~CB19pD5NJglA>h~07wJ%@s_?rcPm-
dRRq~G;aQ(T3xq&wCp4^>VH2qKGY9AQEF(>qXnRbt_N&@ytCt6l_;Pw>0u(p@M3-BAc-bd;Bo2yynb*E?J$ah4Qi{%&%dFwRQJBver%%53@Pnd%U
Fb6K-
))LkKChuwL2lTKeO1k|*Yv@l2AN>Et=rG(IPO9<LtryO_Hlj_;fIS}X_mz<WRT$jh#Xq8jjup>F49aC6E6*8L!aRt|9ZInRuxl~Ycazc@!N;K2Po
5Qwoh*WTM4E<k+EI)`yJ#(JgRP9;oN~ruIm5aO0{>L-Q+BEhr%vQ$9wr7K$ENJj@1c@N$(|4uAnFSj+bDnSP)ue%9Y`A40QNCL#I`@XE@R-
Q)bMW)8YTm*Zk|y1Dx2$KT?cIA>rUrhg&@%#rBPo=ou&FYY`YL5cpy8FG6D^o$Jx`I?t}KD^%c>(P!2x<@C<msLdHm<A!5tnx_`5`h*^yBEW;?7)
v<0DueNyj$#&<YMGo#um3z;V;h#L_TnQwJ75Nu3$=gDAjhqw@=ruoXAe(GNQ8MgboVyh$AT6$!~;Wq#BhJoJ1Rvxw%Dj9ylM0~A#ONzUI=q0cMiN
AobV#c^IA}r2!f#dYHOK%tnSvw-!dOjYY$(uU=us@B)NO~S)(w!>06+eFa8deR=GfavlGfU}=f1?2q>kK-v+N+@WA9wX?-
&^54yMM!STXUM+dN6w5TAJrXK_q%Ewwbk;0hr^KtAJ7Fs**jTrZso=#jQH(Zx&jN4+p-+>$}R`*2)MKBH;st5z`o*R#$0c(EI(5@B!-
9*w@X1lS|jP+%AR3c>coR+$Op8qK$PI1R#60AB=Flr=ow^X4zAktqcBw(BaATNyEjI-
N%!C*$$?jUy%1IXb1PYk_ciTPjapTL8gw`;8*q(Z4GMgIvbb8LVouqtsmwC&v78KvikSDcuyC5g3g=(k$}zGUt6a9_JL3=+Ua^4dq}dLJ_OoaB!c
Z<5la{lC<ee^2^fGk5t|;=1;!kD%k#gr;t_Ks+dEL>uBVEZIL?@i%49+&SX)VNWlFdd_?a#wAfyb9GI}v2Jp(B+A^??*S~5{)dq<U}^Fu=3Q|Ybt
?Q46FfwK$GYXp#|9HJhNuKa;-U=`TUEYp6fHy*0S<_Q&l%@{HR^i$~z$gL-hO|c4v5aC3!7pzspg?tv{`#~O+bz}~AdDg-QfXWe5=fu@&?5FpKwk
UxYW&H2e|ATlcd+}mA;TXdF9198}Y*fRROJ4g6o1(K@{XzM__#+(8v}t^-
F6+ha>#TA9KX=~dPRAiUHB^r1<wfm87eX~H=vki}?8H^;&g|00>?&W3uMx+&)8yc@bYD;<n{}CYYu!mlr(@;m7;=n-egYmZwZDnNbVehnFe(8a&-
LeQ>oyx4T(Vl+=khcGBT@#|ZPWM7J!+o3+4@zAC7NLcYS4BXDAqt>{<UmIKs&rW%rE(}L}IE2hPr~6V``s_^<~iING^X96~fo9eM#87r2JCLxGsb
zIM|gw4S!L>arI5<R#447$fJU-
R71Z<zg@@OG@`3y$KDx!XVr?TilrwWDy)#>ItY;e?pWuAA~k@dDLY_rFHN7g#b0aq6bcrW55(U^20R5<Mz4AO{<)&xK8G$t9ujV4LO4g=NjPQ~rU
SG0<Tk=Rcm(Zsx_cYJAjM-
v#SLK<NENVsoIG#k*|}xnl?U0u1oOlY1P5<&78>4pXxxx6hX#YW;2oMEezN9=Qc>rVE1R^fX(F^EM+rOkEUp65>}ER-
$9UM6)b_hYub4X@2s0*<b+o$B^;g_?&88)Uugbx>V>1e9g8ZM3PIqM<Q5)^F6h0BJ2Mw^!)wR0Oo68B1K#NM7ZbWN9>G+R1C>Hf>Tqw?cZFs5zbi
qE=v&g4E;z!#f({9|o`0Lek)RUY^p_%)yIrQPHTng8R?I;K^Zyd|4PQXS&ux9M4n}wz$sE^|9mkAb!=wv5)mUC&5Gi`<`=BqYB5q})gCiaQxh}ja
FQUVhVwoXE>tYS~~@#!4Se)q*R#6+q5wYuyWb7G`$u<!A<7!@jw!b#+~PLu!u<Wd6_2p6V|00EfF0sF%SWolfRvBYQl0ssI200dcD
```

</details>

[index]: https://github.com/identity-md-launches/goal-3470-objective-produce-first-lean/blob/7f9e6fe9271561d22465648a652278c486acde1f/formalization/THEOREMS.md
[audit]: https://github.com/identity-md-launches/goal-3470-objective-produce-first-lean/blob/7f9e6fe9271561d22465648a652278c486acde1f/formalization/reports/trunk-check-v5/CHECK.md
[auditlog]: https://github.com/identity-md-launches/goal-3470-objective-produce-first-lean/blob/7f9e6fe9271561d22465648a652278c486acde1f/formalization/reports/trunk-check-v5/check.log
[dataset]: https://api.imd.fun/goals/4b73084b-2364-4345-98a7-a272655e0499/datasets/catalogue-triage-v1
[csv]: https://api.imd.fun/goals/4b73084b-2364-4345-98a7-a272655e0499/datasets/catalogue-triage-v1?format=csv
[jsonl]: https://api.imd.fun/goals/4b73084b-2364-4345-98a7-a272655e0499/datasets/catalogue-triage-v1?format=jsonl
[items]: https://api.imd.fun/goals/4b73084b-2364-4345-98a7-a272655e0499/items?batch=catalogue-triage-v1
[selection]: https://api.imd.fun/artifacts/05b7da72b4e4ff3e4839de85722ae595dbc2f498bbfad4019e4dd536e3395052
[foundation]: https://api.imd.fun/artifacts/5058151b32fda29f8e71221f75b708d6cb2d1c8d12eaa3e7879d51925182e25a
[harness]: https://api.imd.fun/artifacts/0b80111ae88982a976750cb3a1ec6751854b71367cf212378271db74b90b8b4e
[m1]: https://api.imd.fun/artifacts/2fb506f007887838c120ecb23cca792a0aadafb8c93648b53409c79148b980be
[m2]: https://api.imd.fun/artifacts/cf518e27ff3202e6e7fe661e4a1856ac271506a9e8ecdfe66b3a1da1e5f3a42c
[m3]: https://api.imd.fun/artifacts/34be11b9ae40bb632f6c0b4cc9e2d1f2ea98177faea2180cd509963158ad7330
[m4]: https://api.imd.fun/artifacts/d761551268ee81d0cfb044c639ef2c8cf7460634a48a1c53a0369014e3e1348c
[m5]: https://api.imd.fun/artifacts/e4ecf115455b47768b9057dabaf0155d6cb5a72c27616405b26e43d94f73be29
[a02]: https://api.imd.fun/artifacts/6e4fae65aef04d85944ab4a137b25818c8aefcfdf780efc03f9a49e047f73500
[v02]: https://api.imd.fun/artifacts/c28ab14eec3a4f7338701bc401b4341d91ee13ea3d2fa7a402c4a60d7f1ede77
[a05]: https://api.imd.fun/artifacts/eea7cb18dd8155989186e507f9ad8a8b243bc2eea25130ff2f42987cd03985c9
[v05]: https://api.imd.fun/artifacts/aaf98529fbe64c3d99249714bd440cd140c2fd72048da671e5c8989b9b5e9e44
[a06]: https://api.imd.fun/artifacts/aa23db96f70c2449d513ac3df89f629ff172370f84111764e38195fc4a82c3df
[v06]: https://api.imd.fun/artifacts/b75b7c00d41506624bdb039c70f33d06e6c7db63211ddb661a0d3f46c7786bb5
[a07]: https://api.imd.fun/artifacts/72384986dfb362aa002859615e8ed1d2a1a552b4657455e83d524cc37ee43035
[v07]: https://api.imd.fun/artifacts/3b9c88d60ff8c3ed7d4d3a0417e77cb973621bfebec84eec94bfd19299c7ae25
[a01]: https://api.imd.fun/artifacts/7f4f625037269466291ff1fe35c1299090331f4c79dd9d9a45e69446f2662ac6
[v01]: https://api.imd.fun/artifacts/8922ac00b3f75a9f46f8065d3b363d4aaa96cafefd71bdb4bfab740b6b8d94e6
[a03]: https://api.imd.fun/artifacts/9a9bdc991ff88b23a040c6ba8f7c859c2c60c060358967bc0bb4b036312a253a
[v03]: https://api.imd.fun/artifacts/75f002c5a12171db9f44574684eeac2c622643742583ea4137ea949ee4ace12e
[a04]: https://api.imd.fun/artifacts/07a707712063915f64961c304f6261102ef78ae1fe7e8ba83ad4fd616b4b6c13
[v04]: https://api.imd.fun/artifacts/57c6ec355be459a10c5834707130f1bea509b2b7922c671637158bcac301625f
[a08]: https://api.imd.fun/artifacts/3c401ed75fd3d299715f20e497c597668496c5a97583763c1d31e0b91ea28a03
[v08]: https://api.imd.fun/artifacts/cc405c5f79a5867fd3a23d867cb7557e3cd5a5e5605ad0eaecf03cdf18978b00
[a01b]: https://api.imd.fun/artifacts/aa7606f5f9af082a6218f2295e28b623b4362c06386c4f2747d7dbe225ddf093
[v01b]: https://api.imd.fun/artifacts/079b5bd784087c5a0534c04916dab6558694c0cc0f9afbbcbb267daedd7b1eb1
[a04b]: https://api.imd.fun/artifacts/2f7f10d81a993b3eb438d1efce5fe35cda18eb438b215670fdeca028bc94c4cb
[v04b]: https://api.imd.fun/artifacts/76a75b291f55d3623372e7a644b55e1171696137a24f7d4a913bdc3209e4a72b
