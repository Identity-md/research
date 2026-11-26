# L-meta-5373 write-up

## Result

The four supplied records do not contain a complete Lean proof of L-meta-5373. No theorem file, second-holder check, or contributor pull request is supplied. I therefore do not claim that the requested proof effort is complete.

This conclusion is consistent across all four records:

- `item-angle-1` reports `status: missing_lemma`, says that the step is reduced to the unproved `residual` hypothesis, and explicitly says “NOT PROVED; no Lean file”.
- `item-angle-2` reports `status: missing_lemma`, says that the reduction needs the unproved `countShared` lemma, and offers no Lean file.
- `item-angle-3` reports `status: missing_lemma`, identifies a sharper unproved `CORE` lemma, and says no inlined proof was built.
- `item-angle-4` reports `status: missing_lemma`; its exhaustive checks found no counterexample in the tested cases, but it describes the needed lower-bound argument as unavailable.

Sources: `.imd/reads/artifacts/item-angle-1`, `.imd/reads/artifacts/item-angle-2`, `.imd/reads/artifacts/item-angle-3`, and `.imd/reads/artifacts/item-angle-4` (the same records are also present under `artifacts/goal/items/angle-{1,2,3,4}/result.json`).

## What was checked

The cited reduction file is [R_meta_5373_1.lean at commit 9d8e016](https://github.com/open-goat/pequalnp-proofs/blob/9d8e016ba61d1af5796eb469e56ad3a895470e3c/lean/PEqualNP/Outside/R_meta_5373_1.lean). Its declaration has two explicit premises, `construct` and `core` (lines 296–312), and its proof invokes `core` at lines 391–394. Thus the reduction is not itself a proof of L-meta-5373: supplying `construct` does not discharge `core`.

The records report the following verified partial routes on the pinned project:

1. The `R_meta_5373_376` route can use the already proved `normalize` (`L_meta_8567`), `countLocalized` (`L_meta_8933`), and `compileStars` (`L_meta_5785`), but still requires `countShared`.
2. The `R_meta_5373_951` route can use the proved high case (`L_meta_8179`), but still requires `residual` for the complementary case.
3. The sharper assembled route reduces the target to `CORE`, which includes the non-high condition and a shared junk-AND case; `CORE` was not proved.

Sources: `item-angle-2` and `item-angle-3` for the named reductions and compilation checks; `item-angle-1` and `item-angle-4` for the high/residual split and its interpretation.

## Empirical evidence (not a Lean proof)

The supplied searches report no counterexample in the cases they decided. In particular, `item-angle-4` reports an exhaustive result of size 8 for the 6-cycle and size 7 after any tested single-edge deletion, and reports the tested pendant-edge examples matching the star-cover upper bound. It also states that C8 and several larger cases were not decided. These experiments support plausibility only and cannot replace `CORE`, `residual`, or `countShared`.

Source: `.imd/reads/artifacts/item-angle-4`.

## Completion status

The requested theorem cannot be honestly presented as complete from the supplied material. The missing mathematical deliverable is a proof of the residual/CORE obligation (equivalently, the shared-junk lower-bound case), followed by an independent holder check and a contributor PR. None of those is present in the four records, so no PR number, contributor identity, second-holder result, or completed theorem is stated here.
