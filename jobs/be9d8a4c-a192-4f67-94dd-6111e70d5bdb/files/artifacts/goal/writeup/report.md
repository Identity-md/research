**UNVERIFIED — Conjectures.io: final Step 0 report, 23 November 2026**

**Decision: `stop-literature-barred`.** The program appears active, but its reported current rules exclude the goal's main strategy: claiming an open-problem bounty by formalizing an already-published complete solution of the exact target. Terms v13, effective 11 November 2026, state: “An independent rediscovery, a different argument, or a first Lean formalization does not restore eligibility.” This triggers the requester's instruction to stop at Step 0. The decision concerns bounty eligibility; it does not invalidate such a Lean proof. [Versioned terms v13, Reward review](https://raw.githubusercontent.com/conjectures-io/conjectures-validator/main/docs/policies/submission-terms-v13.md). Evidence: R2, R5 and episode 2 notes.

We therefore did not undertake the full candidate inventory, per-problem literature search, ranking, or five Lean proofs. There are no candidate payout estimates, compilation logs, or submission-ready proofs to deliver. Nothing was submitted and no verification fee was paid. The report supplies the Step 0 findings and the exact reason those later deliverables are absent.

This is not a claim that all use of published mathematics is ineligible. Supporting lemmas, weaker results, or special cases may support an original argument that closes the remaining gap. Whether a particular reduction or corollary already constitutes a complete prior solution remains unresolved. No such candidate was assessed after the stop decision. [Review v4, Prior publication and attribution](https://raw.githubusercontent.com/conjectures-io/conjectures-validator/main/docs/MANUAL_REVIEW_CRITERIA.md). Evidence: R2, R5.

All findings, figures, policy interpretations and examples below remain **UNVERIFIED**. R1–R5 identify the five supplied results in the provenance table below. Their observations span 2026-11-23 08:38:29–08:45:00 UTC; one underlying treasury snapshot is dated 08:38:00 UTC. The writer reread the official live terms, versioned v13 terms, review manual, status page and how-it-works page. These corroborate the stop condition, advertised activity, short toolchain pins and advertised fee. The writer did not re-enumerate the catalogue, replay a payout, or compile a proof. Browser access to the metadata and system-status API URLs returned “not accessible via this tool”; API figures below retain their supplied observation dates.

**Step 0 — program activity and governing rules.**

The status page reports submissions open and service OK. R1, R4 and R5 also report `submissions_open=true`; R4 records a latest payout on 19 November 2026. These support an active-program finding. A hidden catalogue label reported by R1 says “Test only · submissions disabled”; its meaning is unresolved and cannot be silently dismissed. The stop decision is based on the novelty rule, not an inactivity finding. [Official status](https://conjectures.io/status), [system-status API cited by the workers](https://conjectures.io/v1/system/status), [public results](https://conjectures.io/results).

The live contract identifies **submission terms v13**, effective **2026-11-11**, and **review policy v4**; R2 dates review v4 to **2026-10-12**. The versions recorded at paid acceptance govern a submission. Earlier submissions retain their recorded contracts. The generic repository `SUBMISSION_TERMS.md` was reported as v7, so it should not replace the versioned v13 document for this snapshot. [Live submission terms, In force and Changes](https://conjectures.io/submission-terms), [generic repository terms](https://raw.githubusercontent.com/conjectures-io/conjectures-validator/main/docs/SUBMISSION_TERMS.md). Evidence: R2, R4, R5.

**Step 0 — what counts as settling a problem.**

The mathematical artifact is a Lean proof of the exact published proposition, or a proof of its exact logical negation through the counterexample task. An informal argument or an unproved computational counterexample is insufficient. Original AI chat logs that produced the proof accompany the artifact. Proof and refutation compete for the same target reward. [FAQ, Submitting](https://conjectures.io/faq). Evidence: R3, R5.

The authoritative target is the task's digest-bound `Challenge.lean`, together with its machine contract. Production acceptance checks statement equality through Comparator, permitted dependencies, the transitive axiom closure, and kernel replay in the production sandbox. A successful local `lake build` does not establish official acceptance or payment. The reported production axiom allowlist is exactly `propext`, `Classical.choice`, and `Quot.sound`, subject to any stricter task contract. Neither direct nor transitive admitted results are permitted. [Validator security policy, Production acceptance contract and Permitted production axioms](https://github.com/conjectures-io/conjectures-validator/blob/main/SECURITY.md). Evidence: R3; its source-check flag is preserved below.

The submitted `Main.lean` supplies declarations between the task's trusted header and footer. Those supply imports and namespace. R3 reports scanner restrictions including `sorry`, `admit`, new axioms, `native_decide`, `set_option`, user imports and source-theorem references. A theorem that already has the target statement cannot simply be imported as the solution. The exact task contract remains controlling. [Miner README, Your first submission](https://github.com/conjectures-io/conjectures-miner/blob/main/README.md). No scanner or production verifier was run for this goal.

Verification, reward approval and payment are separate states. A proof can pass Lean and still be refused a bounty. A material mismatch between the published Lean target and the intended informal problem can instead qualify for a formalization-defect award, capped at the lesser of the locked bounty and USD 750 equivalent, paid in Subnet 66 Alpha, provided no disqualification applies. This is not a full settlement of the intended problem. [Live terms, Reward review](https://conjectures.io/submission-terms). Evidence: R4.

The requested `#print axioms` outputs and `lake build` logs do not exist: proof construction was not started. No unattempted build is described here as failed or stuck.

**Step 0 — Lean and Mathlib versions.**

| Component | Reported pin at the observation date | Evidence and precision |
| --- | --- | --- |
| Lean 4 | `leanprover/lean4:v4.35.0-rc2` | R3, R4, R5; official status reread |
| Mathlib | `065356127b1dc0016f66b7283ce0ce2c4055aa55` | Full commit reported by R4/R5; status shows `065356127b1d` |
| Formal Conjectures | `6adcbe13652f4e7c69ad02a783465ae2a99d5cb3` | Full commit reported by R4/R5; status shows `6adcbe13652f` |
| Task repository | `85cfaba5faee` | Abbreviated revision only; no full commit supplied |
| Comparator | `32bd61da1d68` | Abbreviated revision in R3 and status |

Sources: [pinned toolchain status](https://conjectures.io/status), [catalogue metadata cited by R4/R5](https://conjectures.io/v1/catalog/meta). R5 reports the next weekly rotation window as 24 November 2026, 02:00–06:00 UTC. These are dated observations, not a promise that a later task uses the same environment. Existing submissions retain their recorded task version. No toolchain or dependency checkout was created for this goal.

**Step 0 — prize per problem and payment token.**

The bounty is paid in **Subnet 66 Alpha (`α`, netuid 66)**. The attempt fee is denominated in **TAO**; these are different assets. There is no universal fixed prize per problem. R4 reports that a target's precise quote is `bounty.amount_rao / 1,000,000,000` Alpha, read with `available`, `reason`, `as_of`, `locked` and `policy_version` from its catalogue detail. [Public API, catalogue bounty pricing](https://raw.githubusercontent.com/conjectures-io/conjectures-validator/main/docs/PUBLIC_API.md), [catalogue metadata](https://conjectures.io/v1/catalog/meta).

For new targets, the opening share is 1/40 of the available treasury and grows linearly to 1/8 over 15 days. R4 gives the integer-rao formula:

```text
floor(B * (c + (1/8 - c) * min(max(age_seconds / 1296000, 0), 1)))
```

Here `B` is treasury balance after subtracting outstanding locks; `c` is the target's stored opening share, 1/40 for new targets. Older targets retain their original opening share. Fresh intake conditionally locks the quote; it grants neither priority nor entitlement. Pre-V012 submissions retain their earlier payout-time pricing. [Validator README, Dynamic bounty pricing](https://raw.githubusercontent.com/conjectures-io/conjectures-validator/main/README.md), [versioned terms v13, Reward review and Chat logs](https://raw.githubusercontent.com/conjectures-io/conjectures-validator/main/docs/policies/submission-terms-v13.md). Evidence: R4.

The following amounts illustrate the reported units and timing only. Neither entry is a selected candidate or a forecast of this goal's earnings.

| Record | Reported amount | Meaning and source |
| --- | --- | --- |
| Artin primitive roots, part i; slug `artinprimitiverootsconjecture-artin-primitive-roots-parts-i` | **7,324.173719427 Alpha**, from `7324173719427` Alpha rao | R4's unlocked quote at about 08:39 UTC on 23 November 2026; [target detail API](https://conjectures.io/v1/catalog/conjectures/artinprimitiverootsconjecture-artin-primitive-roots-parts-i). No solvability or eligibility assessment was made. |
| Erdős 624, submission `6f349986-c876-4902-8b27-52f19652d5cb` | **9,459.928336837 Alpha**, from `9459928336837` Alpha rao | R4 reports payment at 2026-11-19 15:47:48 UTC; [public result API](https://conjectures.io/v1/results/6f349986-c876-4902-8b27-52f19652d5cb). The cited transfer was not independently replayed. |

**Expected payout for the intended route:** under the reported novelty rule, a fresh claim for an exact target already completely proved in established public literature before intake is ineligible for the full open-problem bounty: **0 Alpha from that bounty**. This is a conditional policy implication, not an observed payment or a per-candidate valuation. No eligible candidates were selected, so their expected payouts are **not assessed**. Separate contribution, historical chat-log, prize or defect programs do not establish a payable claim for this goal. Evidence: R2, R4, R5.

**Step 0 — verification fee.**

The dated live metadata reported by R1/R4/R5 gives `credit_price_rao=250000000` and `credits_per_attempt=1`: **0.25 TAO per admitted verification attempt**. The how-it-works page also advertises 0.25 TAO. Free preflight precedes paid intake; a Lean rejection consumes the attempt. [Catalogue metadata](https://conjectures.io/v1/catalog/meta), [how it works, Per attempt and Check, then submit](https://conjectures.io/how-it-works).

R3 found a conflicting **0.5 TAO** amount in validator documentation, also recorded by R4 in the [validator miner guide](https://raw.githubusercontent.com/conjectures-io/conjectures-validator/main/docs/MINER.md). This report uses the dated live-price observation and preserves the discrepancy. R4 reports credit restoration for an attempt that never ran or could not run for an operator-side reason; ordinary failed proofs do not qualify. Additional chain/processor charges and cash refund treatment for a consumed direct transfer remain unconfirmed. No credit was bought or spent.

**Step 0 — published solutions, prior formalizations and exceptions.**

The governing test is a complete, established public proof of the **same direct mathematical problem** predating paid acceptance. It covers conventional and computer-assisted mathematics. Attribution, permission, independent discovery, a different argument or being first to formalize it in Lean does not restore eligibility. [Versioned v13 terms, Reward review](https://raw.githubusercontent.com/conjectures-io/conjectures-validator/main/docs/policies/submission-terms-v13.md). Evidence: R2 and R5 independently reached this conclusion; episode 2 reread the policy.

Review must identify an inspectable proof, reliable public chronology, matching hypotheses and scope, and a basis for treating the proof as complete. Peer review is not a prerequisite. An unsupported announcement, inaccessible assertion, related theorem or stronger-assumption special case is insufficient. Publication first occurring after paid acceptance does not itself disqualify the claim. A completed, dated external formalization can separately trigger `PRIOR_EXTERNAL_FORMALIZATION`; misattribution is a different ground. [Review v4, Prior publication and attribution; Ambiguous external-formalization evidence](https://raw.githubusercontent.com/conjectures-io/conjectures-validator/main/docs/MANUAL_REVIEW_CRITERIA.md).

Historical cases in the supplied evidence explain why older successes do not authorize a new literature-only claim:

| Precedent | Reported outcome and relevance | Direct source |
| --- | --- | --- |
| Wilf, embedding dimension four, 12 October 2026 | R2 reports Lean verification but withdrawal of approval and cancellation of an unsigned payout for `NOT_NOVEL`, following evidence of a complete earlier computer-assisted proof. No payment. The individual correction was expressly authorized; it is not evidence that every earlier contract had v4 wording. | [Public result](https://conjectures.io/results/487cb5cc-804d-4a17-963a-c938408637a5), [dated decision](https://raw.githubusercontent.com/conjectures-io/conjectures-validator/main/docs/review-decisions/2026-10-12-wilf-e4.md) |
| Wilf, `c ≤ 4m` | R2 reports approval under v3 on 12 October and payment on 14 October 2026: earlier `c ≤ 3m` and special families did not cover the full target. This illustrates the distinction between partial prior work and a complete prior solution. | [Public result](https://conjectures.io/results/fd12daa7-2b0e-460f-a805-f9ba6d9fede4) |
| Erdős 859 | R2 reports approval with credited PNT+ code and Ford estimates as supporting work; no complete earlier solution of the exact target was established. | [Public result and review](https://conjectures.io/results/e060355f-a728-4b06-af11-6302b5780d19) |
| Erdős 10, Grechuk variant | R2 reports historical v1 approval despite a parity implication of Crocker's result. The supporting review document is explicitly a draft; first-entry payment was unconfirmed. That older novelty rule does not govern fresh claims. | [Dated draft decision](https://raw.githubusercontent.com/conjectures-io/conjectures-validator/main/docs/review-decisions/2026-08-06-erdos-10-grechuk.md), [task retirements](https://raw.githubusercontent.com/conjectures-io/conjectures-tasks/main/tiers/tier-1/RETIREMENTS.md) |
| Erdős 624 | R4 reports a case-specific exception involving possession of the exact working proof before self-disclosure and a corrected filing. It is not general permission to submit already-published solutions. | [Public result and review](https://conjectures.io/v1/results/6f349986-c876-4902-8b27-52f19652d5cb) |

These are policy precedents, not a ranked shortlist. The evidence does not establish that every problem close to a known result is barred; the stop decision follows the explicit gate for the main already-solved-in-the-literature strategy.

**Step 0 — eligibility and KYC.**

R2/R4 report an account, attempt credit and original AI chat logs as requirements for new submissions. Browser sign-in supports password, Google, email link or a supported wallet. A Bittensor rewards coldkey is required to receive Alpha and may be set after proof acceptance. The CLI route requires the paying/signing coldkey to be linked to the account; its documentation says a registered hotkey is unnecessary. [How it works, Create an account and Your payout wallet](https://conjectures.io/how-it-works), [miner CLI README](https://raw.githubusercontent.com/conjectures-io/conjectures-miner/main/README.md).

**KYC and jurisdictional eligibility are unknown.** R2/R4 found no express public rule establishing government-ID checks, age, nationality, residence, tax or academic-affiliation restrictions. This absence is not proof that KYC is unnecessary or that every entrant is eligible. Signed-in checkout, payment-provider screening and jurisdiction-specific conditions were not observed. [Terms of service](https://conjectures.io/terms), [privacy policy](https://conjectures.io/privacy). No account was created and no transactional route was tested.

**Step 0 — submission process and competing claims.**

The documented sequence below is descriptive; no step involving filing or payment was performed:

1. Select the exact target and direction, checking submission availability, the task ID, digest, `Challenge.lean` and machine contract. Prepare the declaration-only Lean artifact in the pinned environment. Evidence: R3/R4; [miner workflow](https://github.com/conjectures-io/conjectures-miner/blob/main/README.md).
2. At the [submission page](https://conjectures.io/submit), select the file and run the free preflight. R4 reports optional explanatory PDFs and public attribution fields.
3. Deposit the original AI chat-log ZIP, binding it to the task and exact proof hash, before filing the matching proof. R4 reports a **24-hour initial deposit-to-proof window** from `deposit_hours=24`. The separate waiver of claim/correction deadlines is not treated here as a verified waiver of that intake window. The interaction was not transactionally tested. [Trajectory package rules](https://conjectures.io/trajectory-bonus), [trajectory-offer API](https://conjectures.io/v1/trajectory-offer).
4. Submit through the browser using one credit, or use the official CLI's sealed proof bundle and payment-reference flow. R4 reports that pre-admission refusal leaves an unused payment reference reusable, whereas a changed proof after a consumed attempt needs a new attempt and matching logs. [Miner CLI, What costs money and Your first submission](https://raw.githubusercontent.com/conjectures-io/conjectures-miner/main/README.md).
5. Production verification precedes human reward review and any payout. Required logs must be authentic; R4 reports up to three original-log versions for corrections, without a correction deadline. Accepted logs are private but licensed for use, sale and sublicensing. [Chat-log terms v6](https://raw.githubusercontent.com/conjectures-io/conjectures-validator/main/docs/trajectories/chat-log-terms-v6.md).
6. Track the submission in the account or CLI and the public [results](https://conjectures.io/results). Approved proof bytes are exposed through the result's solution endpoint; payment requires a rewards destination. Evidence: R4; [public API, Results and publication](https://raw.githubusercontent.com/conjectures-io/conjectures-validator/main/docs/PUBLIC_API.md).

An earlier eligible claim can defeat a later submission. Proof/refutation and source repins share one stable target reward, while independently formalized parts and variants can be separate targets. A paid attempt does not reserve the target, and a conditional bounty lock does not reserve it either. The phrase “first accepted” should therefore not be read as “first fee paid.” Review-pending targets may still accept submissions; no per-candidate competing-filings search was carried out. [Versioned terms v13, Reward review](https://raw.githubusercontent.com/conjectures-io/conjectures-validator/main/docs/policies/submission-terms-v13.md). Evidence: R2, R4.

**Step 0 — open versus settled counts.**

R1 reports counting four API pages with `limit=100` and offsets **0, 100, 200, 300**, with 26 records on the last page and 326 unique slug/problem-ID/reward-target values. The counting unit is one formal proposition, not one Erdős number and not one attempt. Proof and counterexample are directions for the same proposition. [First catalogue page](https://conjectures.io/v1/catalog/conjectures?limit=100&offset=0). The following is the worker's dated enumeration, not an independently reproduced dataset.

| Catalogue status | Reported count | Accepting claims? | Interpretation |
| --- | ---: | --- | --- |
| `open` | 283 | Yes | Open bounty target |
| `in_review` | 3 | Yes | Earlier proof is under review; competing claim risk remains |
| `solved` | 36 | No | Catalogue labels these solved |
| `solved_documentation_pending` | 3 | No | Closure with documentation pending; R1 says not yet rewarded |
| `formalization_defect` | 1 | No | Closure does not establish settlement of the intended conjecture |
| **All current bounty targets** | **326** | **286 yes; 40 no** | **283 + 3 + 36 + 3 + 1** |

Thus **286 were open for claims**, including three in review; **40 were closed to submissions**. It would be inaccurate to call all 40 successfully settled mathematical problems. The most direct solved-status count is **36**, with three further documentation-pending records and one defect kept separate. The request's approximate **274** open count was not reproduced; the evidence does not establish exactly when or why it differed. Evidence: R1, R5.

The other reported totals refer to different populations:

| Total | What it counts | Why it differs |
| --- | --- | --- |
| 329 website entries | Current bounty catalogue plus three Hilbert research entries | 326 + 3; those extra entries are not separate bounty targets |
| 43 historically rewarded targets | Public results across current and retired targets | R1 reports six rewarded targets absent from the current catalogue; one of the remaining 37 is now the defect record |
| 74 submissions | Attempts across 60 distinct slugs | 60 Lean-verified and 14 Lean-rejected; attempts are not target counts |
| 652 task bundles | Task repository's reported snapshot | Two directions for 326 propositions |
| 572 tasks | Worker-reported `/v1/tasks` response | Not reconciled with 652; although 572 = 2 × 286, that equality alone does not establish the endpoint's filtering rule |

Sources: R1; [website catalogue](https://conjectures.io/problems), [results](https://conjectures.io/results), [task repository](https://github.com/conjectures-io/conjectures-tasks), [tasks endpoint](https://conjectures.io/v1/tasks). R1 also reports metadata `open_conjectures=326` and `is_open=true` on closed records. Its interpretation that those fields describe source classification rather than bounty availability is an inference. The 286 figure instead uses the reported submission-availability fields. The status queue's seven awaiting review versus 21 unreviewed results remains another unresolved difference.

**Coverage of the requested deliverable.**

| Requested work | Delivered status | Exact stopping point or limitation |
| --- | --- | --- |
| Step 0: rules, activity, versions, payouts, fees, eligibility, submission, counts | Reported above, all UNVERIFIED | Novelty rule triggered the explicit stop condition; KYC and listed discrepancies remain unknown |
| Step 1: every open ID, statement, source, prize and Lean-statement locator | Not produced | The rules worker counted catalogue records, but the separate exhaustive inventory stage was never run |
| Step 2: literature search for every open target and statement mismatches | Not attempted | No coverage claim for arXiv, bibliographic references, Erdős threads/comments, MathOverflow, Lean Zulip or Formal Conjectures per target |
| Step 3: ranking by solution strength, formalization effort and prior filings | Not attempted | No candidate shortlist; policy precedents and a pricing example above are not candidates |
| Step 4: five exact Lean proofs, `lake build`, no admitted results and `#print axioms` | Not attempted | No proof files, Lake project, build logs, axiom output, failed goals or compiler diagnostics exist |
| Expected payout for each candidate | Not assessed | No candidates selected; the 0-Alpha statement is only the policy implication for the barred class |
| Goal code repository and final merged commit | None | Supplied goal record has `trunk: null`; no code wave was created |
| Submissions or payments | None | No proof filed, fee paid, logs uploaded or reward claimed |

The missing later-stage artifacts result from the required Step 0 stop, not a claim that a full inventory or five proofs were completed, nor a time, memory or build failure.

**Batch and decision audit.**

The goal record reports five used items out of 50, over two episodes. All three batches are settled. The first batch has four accepted research results, and the verdict batch has one. The inventory batch shows one failed item, but its dependency record and episode notes identify this as automatic cancellation because `decision` was not `proceed`; it is not a failed inventory investigation. No code trunk or child-job output was handed over.

| Batch | One item's bounded assignment | Required result visible in the supplied brief | Outcome |
| --- | --- | --- | --- |
| `program-rules` | Answer one substituted Step 0 question: activity/counts, literature/eligibility, settlement/Lean, or payout/submission | One JSON object with `status: unverified`, `question`, `as_of_utc`, `findings`, `sources`, `unresolved`; precise source locations and short evidence excerpts | Four accepted items, R1–R4 |
| `step-zero-verdict` | Make one Step 0 decision from the four rules results and resolve official-source discrepancies | One JSON object with `status`, `as_of_utc`, `decision`, `reason`, `rules`, `unresolved`; controlled decision values | R5 returned `stop-literature-barred` |
| `open-id-inventory` | Build one exhaustive index of official open problem IDs, conditional on a `proceed` verdict | Exhaustive official IDs with observation interval, stable enumeration and official record locators | Automatically not run |

The stored briefs are abbreviated with ellipses. Their visible text supports the one-item/one-piece structure above, but does not permit certification of every omitted instruction or the inventory's complete output schema. No batches were added or amended during this write-up.

The following is a reconstruction of the final decision from the episode 2 notes, using the reference's single-object `notes`/`finish` shape. It is embedded because this assignment expressly permits only `report.md`; no separate decisions file is created. This records the decision without claiming to deliver an additional file under the generic decisions-file criterion.

```json
{
  "notes": "UNVERIFIED. Final decision: stop-literature-barred. Terms v13 and review v4 exclude a fresh open-problem bounty claim when an established complete public proof of the exact problem predates paid acceptance, including a first Lean formalization. Activity indicators support an operating program. The requester's Step 0 stop condition applies to the main literature-only strategy. Report all five research results and unresolved discrepancies. Steps 1-4 were not undertaken; the gated inventory was cancelled before running. No candidates, Lean project, builds, trunk repository or merged commit exist. No submission or fee was made. No new batches are needed.",
  "finish": true
}
```

**Evidence provenance and remaining limitations.**

All five handed JSON files parsed successfully and matched their supplied SHA-256 digests in this write-up's local check. Hash agreement confirms which input was read; it does not certify the input's claims. Result identifiers and digests are recorded here because the temporary inputs are removed before delivery. The findings needed to understand the decision are included in this report, with direct primary-source links above.

| Label | Handed input / logical result | Observation UTC on 2026-11-23 | Source-check status in goal record |
| --- | --- | --- | --- |
| R1 | `b01-activity-and-counts` / `program-rules/activity-and-counts` | 08:39:08 | Flagged; reason not supplied |
| R2 | `b01-literature-and-eligibility` / `program-rules/literature-and-eligibility` | 08:41:07 | Not flagged |
| R3 | `b01-settlement-and-lean` / `program-rules/settlement-and-lean` | 08:38:29 | Flagged; reason not supplied |
| R4 | `b01-payout-and-submission` / `program-rules/payout-and-submission` | 08:39:21 | Not flagged |
| R5 | `b02-bounty-program` / `step-zero-verdict/bounty-program` | 08:45:00 | Not flagged; synthesizes R1–R4 and is not a wholly independent measurement |

| Input | SHA-256, matched locally |
| --- | --- |
| R1 | `61fe7d51218e74188be3958a3f85db7fd5fff56aa02b388fe1b84508309db628` |
| R2 | `16440bb4f98596089683f7969f77e556166cf45af0eb7efa73d898a85714b7cc` |
| R3 | `9ef9938d045fb6864d1e377f81c1091874d6f14d9282f536600d84bb6f14b97f` |
| R4 | `7fe8d316e6bbe85225e641a060170f46fd89d380bfbbdd4b533c22f701096df6` |
| R5 | `a683a915bc683e008a10dbc3fc5a5e0a6de4b960e4e7b303c9264e544fbeb566` |

R1–R4 originated at `artifacts/goal/batches/program-rules/items/<item-key>/result.json`; R5 at `artifacts/goal/batches/step-zero-verdict/items/bounty-program/result.json`. They were supplied as the named `.imd/reads/artifacts/` inputs, not as deliverable files. R4 refers to an auxiliary `sources.json` that was not handed over; its inline URL/location/evidence tuples were used instead. The final notes and batch metadata came from the supplied `.imd/reads/goal.json`.

The source-check flags on R1 and R3 are retained without inventing a reason or treating acceptance as independent validation. R2/R3 reported inaccessible API reads or HTTP 403 responses, while R4/R5 reported successful anonymous reads of selected endpoints. This difference in access is not resolved. Numeric catalogue evidence is a reported count without the complete underlying rows in the handed files; it is not a replicated dataset. The hidden test label, 572/652 task discrepancy, queue discrepancy, KYC conditions, exact corollary boundary and transactional deposit-window behavior remain open limitations. Source URLs on `main` can change; their policy versions and observation date matter.

Local document checks passed: all five input hashes matched, the inputs and embedded decision object parsed, the stated count arithmetic and token-unit conversions agreed, and this UTF-8 report is below 64,000 bytes. The report remains untracked; no tracked file was changed or staged. It is the only output created. These checks do not independently certify mathematics, production behavior, reward eligibility or chain payments. **Every substantive result remains UNVERIFIED.**
