# JSP-000340

Exact statement (Erdős #413): let \(\omega(m)\) denote the number of distinct prime divisors of the positive integer \(m\). Are there infinitely many positive integers \(n\) satisfying
\[
\forall m\in\mathbb Z_{\ge1},\quad m<n\implies m+\omega(m)\le n?
\]
The second question asks whether there exists a real \(\epsilon>0\) such that infinitely many positive integers \(n\) satisfy
\[
\forall m\in\mathbb Z_{\ge1},\quad m<n\implies m+\epsilon\omega(m)\le n.
\]
Source: [Erdős Problems #413](https://www.erdosproblems.com/413). The second quantifier is **some** positive multiplier, rather than **every** positive multiplier in the catalog paraphrase. The [catalog entry](https://github.com/TheJustinSunPrize/awards/blob/main/problems/catalog-0301-0400.md#JSP-000340) is the selected JSP record; its number is not the Erdős problem number.

Status check, 2026-11-07: the problem page lists the main question as open, credits Lau with resolving the second question, and displays zero proof claims. [Lau, arXiv:2604.15042v3, revised 13 October 2026](https://arxiv.org/html/2604.15042v3), retains the main question as Conjecture 2. Its Theorem 1.3 and Corollary 1.5 give a logarithmic bound and the desired bound for all distances above a fixed threshold, respectively. These do not settle the main question. Targeted arXiv searches for “413”, “barriers”, and “omega” found no complete resolution; this search is not evidence that no such work exists.

Open repository issues and PRs were searched through the GitHub API for JSP-000340, the equivalent catalog entry JSP-000551, 413, and barrier terminology. No active complete-solution claim for this problem was found. The relevant [open PR #625](https://github.com/TheJustinSunPrize/awards/pull/625) corrects infinitude quantifiers and explicitly makes no proof claim. [Reproducible search for the selected ID](https://github.com/TheJustinSunPrize/awards/issues?q=is%3Aopen%20%22JSP-000340%22); [search for the equivalent entry](https://github.com/TheJustinSunPrize/awards/issues?q=is%3Aopen%20%22JSP-000551%22). These findings concern the inspected public records, not a guarantee of availability.

Outcome: **no result** — no complete proof or counterexample obtained; proof sketch and Lean file: none, and no Lean compilation or axiom audit is claimed.
