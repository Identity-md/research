# JSP-000550 — equal LCMs of disjoint integer blocks

**Outcome: partial.** As of 7 November 2026, I found no accepted proof or counterexample to the equal-length conjecture. The argument below gives a necessary condition for a collision, and the exact search covers a finite range. Neither settles the question.

## Exact statement and source

The task is [Erdős Problem #677](https://www.erdosproblems.com/677), not Erdős Problem #550. The catalogue states:

> Let $M(n,k)=[n+1,\ldots,n+k]$ be the least common multiple of $\{n+1,\ldots,n+k\}$. Is it true that for all $m\geq n+k$, $M(n,k)\neq M(m,k)$?

This wording is also transcribed in the [Erdős Problems research mirror](https://erdosproblems.ai/wiki/problems/integer_sequences/E0677). The condition $m\geq n+k$ makes the two blocks disjoint, including the adjacent case $m=n+k$. Here $k$ is a positive integer; the [Formal Conjectures statement](https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/ErdosProblems/677.lean) uses $n,m\in\mathbb N$ and $k>0$.

The historical source is Paul Erdős, [“Some Unconventional Problems in Number Theory,” *Mathematics Magazine* **52** (1979), 67–70, item 2 on p. 67](https://www.renyi.hu/~p_erdos/1979-22.pdf). Erdős also stated the same-length conjecture in a [separate paper with the same title in *Acta Mathematica Academiae Scientiarum Hungaricae* **33** (1979), §3, p. 78](https://combinatorica.hu/~p_erdos/1979-23.pdf). The searchable text of the *Mathematics Magazine* scan renders the separation condition as $m>n+k$, while the later catalogue uses $m\geq n+k$. This report addresses the catalogue's explicit, inclusive formulation; the distinction matters only for adjacent blocks. I have not independently resolved whether the scan's strict sign reflects the printed glyph or text extraction.

## Status check

The [JSP-000550 catalogue entry](https://github.com/TheJustinSunPrize/awards/blob/main/problems/catalog-0501-0600.md#jsp-000550--must-two-disjoint-equal-length-intervals-of-consecutive-integers-have-different-least-common-multiples) and [Bloom's Erdős #677 entry](https://www.erdosproblems.com/677) label the question **open**. The [research mirror's source inventory](https://erdosproblems.ai/wiki/problems/integer_sequences/E0677) likewise reports no proof or disproof, while expressly treating that as a bounded literature finding rather than a certificate that no solution exists.

The most recent directly relevant paper found was Payam Danesh and Raoul Bianchetti, [“Prime-Power Transport and a Three-Site Reduction,” *International Journal of Mathematics Trends and Technology* **72** (2026)](https://ijmttjournal.org/index.php/archive/IJMTT-V72I9P101), published 28 September 2026. Its abstract says that it excludes several restricted cases but leaves configurations with at least three active sites; the authors explicitly call it a reduction, **not a resolution**. The [Formal Conjectures Lean file](https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/ErdosProblems/677.lean) has the conjecture as a statement with `sorry`, so it is not a completed formal proof.

I also checked [arXiv for the phrase “Erdos problem 677”](https://arxiv.org/search/?query=%22Erdos+problem+677%22&searchtype=all); that query returned no results. Stijn Cambie's [arXiv:2410.09138, “Resolution of an Erdős' problem on least common multiples”](https://arxiv.org/abs/2410.09138) answers the neighboring *unequal-length inequality* question (#678), not the equal-length equality question here. A phrase search can miss papers that use different terminology, so this check does not establish that the literature is exhaustive.

**Status inference:** The checked catalogue, formal statement, arXiv result, and September 2026 paper support treating #677 as unresolved. I found no source justifying a “solved by X” report.

## Resolution attempt and rigorous partial result

Write $d=m-n$, so disjointness means $d\geq k$. A collision would satisfy the following necessary divisibility:

**Lemma.** If $k\geq1$, $d\geq k$, and $M(n,k)=M(n+d,k)$, then
\[
n+1\;\mid\;\prod_{i=0}^{k-1}(d+i).
\]
Consequently $n+1\leq\prod_{i=0}^{k-1}(d+i)$; for each fixed pair $(d,k)$ there are only finitely many possible $n$.

**Proof.** The first block contains $n+1$, so $n+1\mid M(n,k)$. Equality implies $n+1\mid M(n+d,k)$. The LCM of positive integers divides their product (at each prime, the maximum valuation is no larger than the sum), hence
\[
n+1\mid\prod_{j=1}^{k}(n+d+j).
\]
Modulo $n+1$, the factor $n+d+j$ is congruent to $d+j-1$. Therefore $n+1\mid\prod_{j=1}^{k}(d+j-1)$, as claimed. The product is positive, so a positive divisor of it cannot exceed it. $\square$

This observation is already recorded in the [#677 discussion summarized by the research mirror](https://erdosproblems.ai/wiki/problems/integer_sequences/E0677); no novelty is claimed. It does not provide a bound independent of $d$, which may grow with $n$.

The [#677 catalogue](https://www.erdosproblems.com/677) reports a stronger consequence of the Thue–Siegel theorem: only finitely many collisions for each fixed $k$, even with $d$ varying. I have not reproduced that theorem or its application here.

For completeness, $k=1$ is impossible because $M(n,1)=n+1$ increases strictly. For $k=2$, the two consecutive numbers are coprime, so $M(n,2)=(n+1)(n+2)$ also increases strictly. These arguments prove only the first two lengths.

The exact-integer [finite search](../search.py), run locally with `python3 search.py`, found no collision for $1\leq k\leq30$ and $0\leq n<m\leq5000$ subject to $m\geq n+k$. It computes every block LCM by repeated `gcd` and stores the earliest start for each value. Keeping only the earliest start is sufficient: if any prior block is disjoint from the current block, the earliest block is too. This is a finite check, not a proof for arbitrary parameters. The local run exited successfully with:

```text
No collision for 1 <= k <= 30 and 0 <= n < m <= 5000.
```

## Lean 4 + Mathlib code and proof boundary

The following is a **statement-only encoding** of the catalogue formulation, also in [JSP000550.lean](../JSP000550.lean):

```lean
import Mathlib

namespace JSP000550

def blockLCM (n k : ℕ) : ℕ :=
  (Finset.range k).lcm (fun i => n + i + 1)

def conjecture : Prop :=
  ∀ (m n k : ℕ), 0 < k → n + k ≤ m → blockLCM n k ≠ blockLCM m k

end JSP000550
```

`Finset.range k` runs through $0,\ldots,k-1$, so `blockLCM n k` takes the LCM of exactly $n+1,\ldots,n+k$. Mathlib documents [`Finset.lcm`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Algebra/GCDMonoid/Finset.html) with this argument order. No Lean toolchain or Mathlib checkout was available locally, so this file was not compiled. It proves nothing: there is no theorem, `sorry`, or new axiom in the delivered code. A full rigorous proof or counterexample of the original conjecture, and therefore a completed Lean formalization of it, remain unanswered.
