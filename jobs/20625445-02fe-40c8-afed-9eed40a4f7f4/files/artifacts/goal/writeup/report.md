**L-meta-2585 — synthesis of the supplied proof attempts**

**The commissioned proof contribution is not established by these results.** Each supplied result explicitly reports that no proof was completed or accepted. None contains a Lean theorem source, evidence of a successful check by another holder's machine, or a pull-request URL attributable to this goal's contributor. This report preserves the available findings; it does not certify that the proof, independent verification, or publication occurred. [1](#input-angle-1), [2](#input-angle-2), [3](#input-angle-3), [4](#input-angle-4)

The assignment's goal is a Lean 4 proof of L-meta-2585, followed by a successful check on another holder's machine and a contributor-opened pull request on [open-goat/pequalnp-proofs](https://github.com/open-goat/pequalnp-proofs). The table below distinguishes that requested outcome from the evidence actually supplied.

| Required outcome | Evidence in the supplied results | Assessment |
| --- | --- | --- |
| A theorem discharging L-meta-2585 | Inputs 1–3 report an unresolved normalization argument; input 4 supplies neither a proof nor a counterexample. | Not established. [1](#input-angle-1), [2](#input-angle-2), [3](#input-angle-3), [4](#input-angle-4) |
| Successful Lean checking | No input includes an accepted theorem or a successful checker transcript. Inputs 3 and 4 report failures before their candidate files were read. | No successful check documented. [1](#input-angle-1), [2](#input-angle-2), [3](#input-angle-3), [4](#input-angle-4) |
| A successful check on another holder's machine | No input identifies such a check or connects a successful checker result to theorem bytes. | Independent verification not documented. [1](#input-angle-1), [2](#input-angle-2), [3](#input-angle-3), [4](#input-angle-4) |
| A pull request opened by the contributor after that check | No input supplies a PR URL or publication record. | Publication and the required ordering are not documented. [1](#input-angle-1), [2](#input-angle-2), [3](#input-angle-3), [4](#input-angle-4) |

The inputs describe the target as a size-preserving conversion: given an arbitrary exact-fanin-two AND/OR circuit computing a C4-free bipartite edge function, construct an equivalent AO2 circuit whose size is no greater and which satisfies Read-1. Input 3 describes the Read-1 requirement in terms of prime-implicant proof trees. This is a paraphrase of the inputs, not a replacement for the exact desk statement, which the supplied JSON records do not include. [1](#input-angle-1), [2](#input-angle-2), [3](#input-angle-3)

The common mathematical gap is the proposed normalization through star blocks. Input 2 describes an OR of single-star blocks whose total cost must be bounded by the original gate count, followed by a proof of READ-1 for the construction. Inputs 1 and 4 identify the key missing inequality: each non-star block must cost at least a star cover of the edges it accepts. Input 4 locates this argument after the proposed reduction to ORs of blocks with no wire below the target function inside a block. None supplies a proof of that inequality or the resulting normalization. [1](#input-angle-1), [2](#input-angle-2), [4](#input-angle-4)

Input 3 makes the remaining obligation concrete: choosing `D = C` leaves `IsReadK` at read bound one unproved. Its cited reduction `R_meta_4478_271` assumes a `normalize` premise and a separate graph-cover bound, so using that reduction would still require establishing the missing premises. Input 1 likewise says `L_meta_7639` assumes that the original circuit is already Read-1. A theorem with that hypothesis does not supply the requested conversion for an arbitrary circuit. Input 2 reports that related outside modules were unavailable through the permitted `PEqualNP.Defs` import. These are distinct limitations; importing or citing a conditional result does not discharge its hypotheses. [1](#input-angle-1), [2](#input-angle-2), [3](#input-angle-3)

Input 4 reports no small counterexample in the boundary cases it considered: an empty incidence relation gives the false function, and a single edge has a one-gate read-1 AO2 representation. It supplies no search program, search range, or exhaustive enumeration. These observations are not a proof of the general normalization claim. Input 3 expressly says it has not established that the statement is false. There is no conflict among the mathematical conclusions of the four inputs: all leave the target unresolved, although input 4 uses status `other` while the others use `missing_lemma`. [1](#input-angle-1), [2](#input-angle-2), [3](#input-angle-3), [4](#input-angle-4)

The recorded Lean failures are operational reports, not successful elaboration or a counterexample. Input 3 reports `libInit_shared.so: cannot open shared object file`, then `error: failed to locate application` after a library-path change. Input 4 reports the shared-library error and says the library was absent from its prebuilt fetch tree. Both say the invocation stopped before reading the candidate. No raw checker log or accepted Lean artifact accompanies either record, and this write-up does not claim to have reproduced their toolchain failures. [3](#input-angle-3), [4](#input-angle-4)

A supplementary read-only review of the named public project on 2026-11-25 corroborated the limits of the related results. At repository revision `166b76053d283f2ffe2baa873ff81b4c586108d1`, the public declaration of `L_meta_7639` takes `IsReadK` as a hypothesis, and `R_meta_4478_271` explicitly takes both `normalize` and `charge` as arguments. Those declarations do not establish the missing normalization. [L_meta_7639 source](https://github.com/open-goat/pequalnp-proofs/blob/166b76053d283f2ffe2baa873ff81b4c586108d1/lean/PEqualNP/Outside/L_meta_7639.lean), [R_meta_4478_271 source](https://github.com/open-goat/pequalnp-proofs/blob/166b76053d283f2ffe2baa873ff81b4c586108d1/lean/PEqualNP/Outside/R_meta_4478_271.lean)

There is a public PR titled `L_meta_2585`, but its posted checker verdict is “REFUSED before any build: the file holds no theorem”. That PR cannot serve as evidence of a checked proof, and the supplied inputs do not attribute it to this goal's contributor. Its existence also means that the limited finding here must not be broadened into a claim that nobody has ever opened a PR for the step. [PR checker verdict](https://github.com/open-goat/pequalnp-proofs/pull/15212#issuecomment-7164565818), [1](#input-angle-1), [2](#input-angle-2), [3](#input-angle-3), [4](#input-angle-4)

The review finding's substantive concern therefore remains unresolved: the available results cannot substantiate delivery of the commissioned proof contribution. To establish that outcome would require the exact theorem source, successful checker evidence tied to that source from another holder's machine, and the contributor's subsequent PR URL. None can be supplied by treating the missing normalization as an assumption, counting a startup failure as verification, or attributing a public PR to the contributor without supporting evidence. The present evidence supports an incomplete outcome, without establishing that L-meta-2585 is false. [1](#input-angle-1), [2](#input-angle-2), [3](#input-angle-3), [4](#input-angle-4)

The following source records are embedded in full because the input files are not part of the delivered report. The original paths and SHA-256 values are those identified in the assignment; their bytes were checked against those hashes when preparing this report. Each JSON block preserves the original record, including its terminating newline. Claims about a worker's attempts are attributed to that worker's record; they are not independent proof-check certificates.

<a id="input-angle-1"></a>

**Input 1: item-angle-1.** Original result: `artifacts/goal/items/angle-1/result.json`; supplied read copy: `.imd/reads/artifacts/item-angle-1`. SHA-256: `01a1e1fc4c749bdd1e25c37ab45c4448038aeb79a64f1451f862fd8763f974d4`.

```json
{"status":"missing_lemma","notes":"I could not prove or elaborate the requested theorem. The target requires converting an arbitrary IsAO2 circuit for a C4-free bipartite edge function into an equivalent IsAO2 circuit of no greater size that is Read-1. The supplied desk sketch identifies the key missing lower bound: a non-star block must cost at least a star cover of its accepted edges. The available related project theorem L_meta_7639 instead assumes the original circuit is already Read-1, so it does not supply this conversion. No Lean file was accepted; the claimed conversion remains unproved here."}
```

<a id="input-angle-2"></a>

**Input 2: item-angle-2.** Original result: `artifacts/goal/items/angle-2/result.json`; supplied read copy: `.imd/reads/artifacts/item-angle-2`. SHA-256: `35cbbdd9c7722f5d63191af4b2cd68e99c54e86409b8af3e20f5bbb61833173b`.

```json
{"status":"missing_lemma","notes":"I could not prove the requested normalization theorem from the permitted import PEqualNP.Defs. The required helper is a size-preserving normalization for arbitrary exact-fanin-two AND/OR circuits computing a K2,2-free bipartite incidence function: it must turn the circuit into an OR of single-star blocks, with total block cost bounded by the original gate count, and then establish READ-1 for that construction. The posted sketch identifies the block-cost bound as the open part. Related material in the prebuilt project is in separate outside modules and is not available through the allowed imports; I did not establish the missing bound or produce a Lean file accepted without sorry."}
```

<a id="input-angle-3"></a>

**Input 3: item-angle-3.** Original result: `artifacts/goal/items/angle-3/result.json`; supplied read copy: `.imd/reads/artifacts/item-angle-3`. SHA-256: `f286097d43b9fb1c80af84db78581221df6a7bac2fe987dfadbbe92e17b290f6`.

```json
{"status":"missing_lemma","notes":"I did not complete a Lean proof. The decisive missing result is the normalization claim from the sketch: for a top-form AO2 circuit computing a C4-free bipartite edge function, construct an equivalent AO2 circuit of no greater size whose prime implicants have read-one proof trees. The fetched R_meta_4478_271 proof work isolates that claim as an explicit `normalize` premise and separately assumes a graph cover bound; it does not supply either premise as a theorem available through the permitted PEqualNP.Defs import. The straightforward candidate D = C leaves exactly the IsReadK obligation unproved. I attempted the required local elaboration, but the provided toolchain invocation failed before reading the candidate (`lean: error while loading shared libraries: libInit_shared.so: cannot open shared object file`); adding the toolchain library path then produced `error: failed to locate application`. No proof file was therefore accepted. I have not established that the statement is false."}
```

<a id="input-angle-4"></a>

**Input 4: item-angle-4.** Original result: `artifacts/goal/items/angle-4/result.json`; supplied read copy: `.imd/reads/artifacts/item-angle-4`. SHA-256: `3b29dd3f2d2e5608d684cd0a8096eb4c19f94c5a7881eb72c64b35ae8fd66b2c`.

```json
{"status":"other","notes":"No small counterexample was found in the boundary cases considered: empty incidence relations yield the false function, and a single edge has a one-gate read-1 AO2 representation. The supplied sketch identifies the substantive missing argument: after reducing to ORs of blocks with no wire below the target function inside a block, prove that each non-star block costs at least a star cover of the edges it accepts. I did not establish that lemma or a counterexample, so this is not a proof. I could not elaborate in the supplied project: the prescribed Lean invocation stopped before reading the scratch file with `libInit_shared.so: cannot open shared object file`, and that library is absent from the prebuilt fetch tree. No external sources were relied on."}
```
