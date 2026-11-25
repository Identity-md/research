**L-meta-2583: merged results and revision assessment**

**The proof goal remains incomplete.** None of the four supplied results contains a Lean proof of `PEqualNP.Outside.L_meta_2583`, an independent holder's successful check of that proof, or a qualifying pull request. Three results report `missing_lemma`; the fourth reports `other` and also says it could not establish the theorem. This report preserves those results and identifies the missing argument. It does not claim to complete the commissioned proof or submission. [A1](#a1), [A2](#a2), [A3](#a3), [A4](#a4)

The assignment's completion conditions and the available evidence are:

| Required outcome | Evidence in the supplied results | Assessment |
| --- | --- | --- |
| The full Lean theorem, including `D.size ≤ C.size` under the original incidence and circuit hypotheses | All four workers explicitly decline to claim a proof. | Missing. |
| A successful check of that completed theorem by another holder's machine | No input supplies a checker identity, checked proof revision, or successful check record. | Missing. |
| A completed-proof PR on `open-goat/pequalnp-proofs` from the proving contributor, after that check | No input supplies such a PR URL or submission record. | Missing. |

These are conclusions about the evidence supplied to this write-up, not assertions that no proof could exist elsewhere. The source records are reproduced below so that the report can be reviewed without the original input mounts. [A1](#a1), [A2](#a2), [A3](#a3), [A4](#a4)

**The requested mathematical statement.** For natural numbers `q, N` and a decidable incidence relation `I : Fin N → Fin N → Prop`, the hypotheses are `2 ≤ q`, `N = q^2 + q + 1`, exactly `q + 1` points on each line, and a unique common line for every pair of distinct points. Let `F_I` accept an assignment exactly when some incident point and line both have true input bits. An arbitrary circuit `C` satisfying `IsAO2 (N + N) C` and computing `F_I` must admit a circuit `D` satisfying all four conclusions: `IsAO2 (N + N) D`, computation of `F_I` on every assignment, `D.size ≤ C.size`, and `ReadK.IsReadK (N + N) D 1`. The desk names `lean/PEqualNP/Outside/L_meta_2583.lean` and the project import `PEqualNP.Defs`. [Desk row](https://pequalnp-desk.pequalnp.workers.dev/desk/row?gap=L-meta-2583)

Here the repository's `IsReadK` predicate concerns an appropriate proof tree for each prime implicant, with each variable read at most `k` times in that tree. It does not impose a global single-occurrence condition on every input wire. [Pinned definition, lines 160–163](https://raw.githubusercontent.com/open-goat/pequalnp-proofs/c5d2253c0f2e5208c74ad41fcc94eba07da7c1ee/lean/PEqualNP/Defs/ReadK.lean)

**What the four results establish about the attempted approach.** A1 found local read-1 facts for a separating AND gate, but no reusable size-preserving transformation through the permitted definitions import. A2 reports a canonical line-star construction with the required function and read-1 property and with

```text
D.size + 1 = N * (q + 2).
```

A4 reports the point-star count `Nq + 2N - 1`. These expressions agree by elementary algebra. The existence of the reported construction does not establish the comparison with an arbitrary input circuit. For that fixed-size construction, the desired comparison is equivalent to

```text
N * (q + 2) ≤ C.size + 1.
```

This equivalence follows by substituting the reported size equality and cancelling the added unit. Establishing this lower bound for every eligible `C` would therefore complete the size comparison for the canonical construction. The inputs do not establish the lower bound. Nor do they establish that this particular construction is the only possible route to the existential desk theorem. [A1](#a1), [A2](#a2), [A4](#a4)

The apparent difference between A1's failure to find a reusable construction through `PEqualNP.Defs` and A2's description of a construction in the prebuilt project is not evidence of a completed proof: A2 expressly says nearby prebuilt results cannot be imported under the file's rules. A4 likewise identifies related work, including `L_meta_2581`, without supplying the requested normalization. These are accounts of available ingredients and import limitations, not verified proofs attached to the merged results. [A1](#a1), [A2](#a2), [A4](#a4)

A3 reports that Lean failed before elaboration because it could not load `libInit_shared.so`. A4 reports the same initial failure and a later `failed to locate application` error after changing library paths. Those are historical worker observations; this report does not turn either into a successful Lean check. A1 and A2's missing mathematical argument remains a separate obstacle. A4's observation that `q = 2` has a consistent Fano-plane incidence pattern supplies no counterexample and no general proof. [A1](#a1), [A2](#a2), [A3](#a3), [A4](#a4)

**The remaining proof obligations.** The desk labels the step `hard` and asks for smaller statements. Its sketch suggests extracting suitable wires to obtain an OR of blocks, then bounding the cost of blocks that are not single stars. [Desk row](https://pequalnp-desk.pequalnp.workers.dev/desk/row?gap=L-meta-2583)

For the route described by the workers, a useful decomposition is:

1. Formalize the transformation from an arbitrary eligible circuit to suitable blocks, proving that the function is preserved and the gate count does not increase.
2. Prove the missing block-cost comparison from the original circuit and incidence hypotheses. Any summation over blocks must account for shared gates without charging them more often than the original circuit's budget permits.
3. Construct the replacement stars and combine their verified costs to obtain an AO2 read-1 circuit no larger than `C`.

This is an outline of obligations, not a proof of them. The first and second obligations are not supplied as Lean proofs in the inputs; the second is the common substantive gap they identify. The need to account for shared gates is the accounting condition required for the proposed sum to bound the actual circuit size. A conditional arithmetic lemma that assumes the partition, charges, cover, and budget inequalities cannot establish those structural conditions. A successful check of such an implication would leave this gap open. [A1](#a1), [A2](#a2), [A3](#a3), [A4](#a4)

**Reproduction of the review finding.** Finding `1790a6139210d463d46abc7b7446fad801bc9a14e4ce83081f78a0dad17c1992` correctly identifies the absence of the original goal's three outcomes in the supplied evidence. The previous report cited in the finding was not present at the named output path when this revision began, so its line numbers and claimed local arithmetic check could not be independently inspected. The following public-source checks do reproduce the substantive issue:

| Source checked | Observation | What it supports |
| --- | --- | --- |
| [Desk row](https://pequalnp-desk.pequalnp.workers.dev/desk/row?gap=L-meta-2583), HTTP response dated 2026-11-25 at 21:22:03 UTC | `updated_at: 2026-11-25T21:19:38.541Z`; `checked: []`; for `L-meta-2583`, `pr_open: 0` and `pr_numbers: []`. | This desk snapshot records no checked proof or listed open PR for the step. |
| [Repository tree at `c5d2253c0f2e5208c74ad41fcc94eba07da7c1ee`](https://api.github.com/repos/open-goat/pequalnp-proofs/git/trees/c5d2253c0f2e5208c74ad41fcc94eba07da7c1ee?recursive=1) | The response has `truncated: false`; the exact path `lean/PEqualNP/Outside/L_meta_2583.lean` is absent. | That revision does not contain the requested file. This is a finding about the pinned tree, not every branch or later revision. |
| [PR source at `33aa02599ab1cb165b4333b9f4ce39a5fe15a6b2`](https://raw.githubusercontent.com/open-goat/pequalnp-proofs/33aa02599ab1cb165b4333b9f4ce39a5fe15a6b2/lean/PEqualNP/Outside/L_meta_2583.lean), especially lines 639–657 | `no_larger_of_size` assumes `hsize : N * (q + 2) ≤ C.size + 1`; `step_of_lower_bound` also adds that inequality as a premise. | The cited source supplies a conditional route, not the unconditional desk theorem. |
| [Checker comment on PR #13723](https://github.com/open-goat/pequalnp-proofs/pull/13723#issuecomment-7166760455) | The comment says “REFUSED before any build” and identifies the theorem's placement and full-name requirement as the reason. | This is not a successful build or independent validation of the requested proof. The refusal itself does not adjudicate the mathematical argument. |
| [Checker comment on PR #19757](https://github.com/open-goat/pequalnp-proofs/pull/19757#issuecomment-7171739256) | The reduction was closed without checking because the step does not accept reductions; a proof remains welcome. | A reduction or proposed cut does not satisfy the completed-proof submission requirement. |

The tree and desk requests returned HTTP 200. The pinned Lean file and both specific comment records were also fetched successfully; the comments were verified through the [first comment API record](https://api.github.com/repos/open-goat/pequalnp-proofs/issues/comments/7166760455) and [second comment API record](https://api.github.com/repos/open-goat/pequalnp-proofs/issues/comments/7171739256). The desk's `pr_open` field must be read as a desk record: the existence of the linked GitHub PRs means it cannot be used to claim that no related PR has ever existed.

The finding's factual premise is therefore upheld, and the original goal's failure remains **unresolved**. The revision response disputes the requested remedy's scope: this bounded assignment is to write up the four merged results, which contain no completed theorem or independent check to document. This report supplies an evidence-based account of that failure. It neither resolves nor disputes the missing theorem, independent check, and qualifying PR.

**Preserved input evidence.** Each original input's SHA-256 was recomputed and matched the hash supplied in the assignment. Its corresponding `artifacts/goal/items/angle-*/result.json` copy also matched byte for byte. The hashes below identify the original input bytes; the JSON is presented with formatting for readability. All original fields and values are retained.

<a id="a1"></a>
**A1 — item-angle-1**

Source: `.imd/reads/artifacts/item-angle-1`, also supplied as `artifacts/goal/items/angle-1/result.json`.

SHA-256: `1baddd53e8dc80dd09de7cf439d7919ad5ef32784ab5c6e57e1e63987aa830bf`.

```json
{
  "status": "missing_lemma",
  "notes": "The requested conclusion is a size-preserving transformation from an arbitrary IsAO2 circuit for the projective-plane incidence function to a circuit satisfying ReadK.IsReadK ... 1. The permitted project import is only PEqualNP.Defs; inspection found local READ-1 facts for a selected separating AND gate, but no reusable construction theorem. The pinned desk sketch itself identifies the open step: proving a lower bound for blocks that are not single stars, needed to show the transformed circuit has size at most C.size. I could not prove that block-cost lemma or complete a Lean proof, so no Lean file is claimed."
}
```

<a id="a2"></a>
**A2 — item-angle-2**

Source: `.imd/reads/artifacts/item-angle-2`, also supplied as `artifacts/goal/items/angle-2/result.json`.

SHA-256: `60783c720a32f772f87e434640f5a1151d1e022db52cb40a7cb84eed7ade1e12`.

```json
{
  "status": "missing_lemma",
  "notes": "The canonical line-star construction in the prebuilt project supplies an AO2 circuit D for the incidence function with IsReadK (N + N) D 1 and D.size + 1 = N * (q + 2). The required comparison D.size ≤ C.size therefore needs the general lower bound N * (q + 2) ≤ C.size + 1 for every AO2 circuit C computing this function under the incidence hypotheses. The desk sketch identifies the same open issue: reducing an arbitrary circuit to blocks and showing non-star blocks cost at least a star cover of their accepted edges. I found no such lemma among the definitions imported by PEqualNP.Defs. The nearby prebuilt results establish weaker lower bounds or special cases and cannot be imported under this file's rules. I have not established the missing bound or found a counterexample, so no Lean proof is claimed."
}
```

<a id="a3"></a>
**A3 — item-angle-3**

Source: `.imd/reads/artifacts/item-angle-3`, also supplied as `artifacts/goal/items/angle-3/result.json`.

SHA-256: `1523a0c227d96721ad14c0d12b3214e648f05162ee4fc5a65b1366e95cf0b599`.

```json
{
  "status": "other",
  "notes": "I could not establish the theorem. The required Lean command failed before elaboration with `lean: error while loading shared libraries: libInit_shared.so: cannot open shared object file: No such file or directory` (the named file is present in the supplied toolchain directory). The imported definitions provide circuit and read-k predicates, but I found no proved size lower bound handling non-star blocks. That bound is the missing mathematical step in the desk sketch, so I cannot responsibly report a proof without elaboration."
}
```

<a id="a4"></a>
**A4 — item-angle-4**

Source: `.imd/reads/artifacts/item-angle-4`, also supplied as `artifacts/goal/items/angle-4/result.json`.

SHA-256: `887ec828d0f2212c945be8997d64e4a1675d8af8737bcaaea01316ed0a7d749d`.

```json
{
  "status": "missing_lemma",
  "notes": "No counterexample was found: q = 2 gives the consistent Fano-plane incidence pattern, so the small admissible case does not refute the statement. The direct point-star construction computes the target and is ReadK 1, but its gate count is Nq + 2N - 1; the hypotheses do not by themselves give that bound on C.size by an elementary counting argument. The missing step is the desk sketch's structural lemma: for arbitrary IsAO2 circuits computing this incidence edge function, decompose the circuit into blocks and prove that every nonsingle-star block costs at least a star cover of its accepted edges. The repository contains related incidence lower-bound work (including L_meta_2581) but not this size-preserving normalization. I could not validate a proof with Lean: the documented command first failed to load libInit_shared.so; adding the toolchain lib directories changed the error to 'failed to locate application'."
}
```
