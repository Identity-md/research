# Decision memo: an opt-in campaign marketplace for AI products

Research date: 2026-10-26. **Recommendation: conditional go for one paid API onboarding and task-completion pilot; defer a broad marketplace build.**

**Evidence key:** **F** = public fact; **I** = inference; **P** = proposal; **A** = modelling assumption; **U** = unresolved. Design tables and recommendations are **P** unless marked otherwise. All linked sources were consulted on the research date. This evaluates an independent service using public examples and general design principles. The supplied earlier report is background, not evidence of demand or infrastructure suitability. No installations, campaigns, contacts, private-system access or spending took place.

## 1. Proposition and customer

**P — Sell an evidence package:** “Can agents unfamiliar with this product complete your target tasks from its documentation? Receive a result for every assignment, reproducible failures and a prioritized report.” Start with indie developers and small teams shipping **hosted, agent-facing APIs or remote MCP tools**, with test tenants and an upcoming release. Outcomes are observable and findings can inform the release.

**F:** Anthropic describes evaluating tools with agents on realistic tasks, reviewing transcripts and tool-call errors, and using held-out tasks to assess changes. This supports agent usability as an engineering problem; it does **not** establish demand for a third-party marketplace. [Anthropic: writing effective tools for agents](https://www.anthropic.com/research/writing-tools-for-agents)

| Potential developer value | Deliverable and measurement | Boundary |
|---|---|---|
| Onboarding trials and agent usability | First-task success, time, documentation gaps, invalid calls and error recovery | **I:** Strong fit for agent-facing products; cannot establish human comprehension. |
| Bug discovery and individual evaluations | Expected/actual results, artifacts, reproduction steps and confidence per assignment | A valid clean result earns payment too; no guaranteed bug count. |
| Consolidated findings | Deduplicated issues, severity, affected configurations, contradictions and fix retests | **I:** Saved triage effort is more valuable than submission volume alone. |
| Agent-native adoption | Useful outputs, repeat choice when alternatives are allowed, cost/success versus baseline | Paid use can be useful. Label it sponsored; measure unsubsidized continuation separately. |
| Operator discovery | Disclosed product introductions to interested operators; optional follow-up | Exposure can create distribution, but an assignment is not a human acquisition. |
| Human acquisition | Separately consented, attributable signups or purchases, if measured later | **U:** Conversion and audience fit. Never infer unique humans or machines from agent participation. |

**I:** Runs controlled by one operator or using one model can still expose stochastic failures and task-specific friction. Their value depends on coverage and evidence. Report run counts, disclosed operator relationships and model/version coverage; do not claim independent people or population-level representativeness.

**P — Integrity boundary:** Allow disclosed sponsored testing, useful paid tasks and honest feedback of any sentiment. Reject fabricated experiences, purchased ratings, spam, unauthorized traffic and deceptive metric inflation. Tag campaign activity in analytics and distinguish paid completions from organic retention. Public case studies require separate consent and sponsorship disclosure.

**F:** US FTC guidance permits honest incentivized consumer reviews without sentiment conditions, while warning that undisclosed incentives can violate the FTC Act; disclosure does not make paid five-star reviews permissible. This is a US-specific boundary, not a claim that every agent evaluation is legally a consumer review. [FTC: reviews and testimonials Q&A](https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers)

## 2. Alternatives and differentiation

| Public alternative (F) | Implication (I) |
|---|---|
| [Promptfoo](https://www.promptfoo.dev/docs/guides/evaluate-coding-agents/) documents agent evaluations with integrations, sandboxing, traces and assertions. | DIY evaluations plus CI are the strongest substitute. Sell fresh exploration, recruitment, verification and synthesis rather than parallel model calls alone. |
| [UserTesting](https://www.usertesting.com/plans) offers opt-in human research, moderated/unmoderated tests and customized pricing. | Prefer human research for human UX and purchasing motivation. An agent panel is complementary, not equivalent. |
| [Prolific](https://www.prolific.com/pricing) offers human research and AI evaluation participants. It lists a usual corporate fee of 42.8% above rewards, recommends at least $12/hour and enforces an $8/hour minimum. | A $12 one-hour reward implies about $17.14 including that platform fee, before tax. This is a human-research reference, not a specialist quote or equivalent agent benchmark. |
| [Test IO](https://test.io/) advertises exploratory, regression and agentic QA alongside its human testing community. | Crowd QA is established; agentic QA is not uncontested. The proposed package must beat DIY on usefulness or saved effort. |

**U:** No customer interviews, purchasing commitments or verified willingness-to-pay evidence were obtained. These alternatives establish adjacent offerings, not demand for this service. A managed pilot should also test recruitment and task supply before investing in marketplace scale.

## 3. Feasibility and safety

**I — Feasible with constrained access; safety depends on implementation and validation.** Treat developers, packages, pages, tool responses and submissions as potentially malicious. Threats include prompt injection, theft, unauthorized actions, supply-chain compromise, resource abuse, persistence, fabricated findings and collusion.

**F:** OpenAI describes external content manipulating agents and recommends limiting access and reviewing consequential actions; protections do not prevent every injection. MCP guidance identifies token-passthrough and SSRF risks. **I:** Enforce boundaries outside the model instead of relying on instructions alone. [OpenAI: prompt injections](https://openai.com/safety/prompt-injections/), [MCP: security best practices](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices)

| Mode | Feasibility and safeguards (P) | Residual risk and initial scope (I/P) |
|---|---|---|
| Browser trials | Disposable browser in isolated execution; synthetic accounts/data; approved destinations; no personal cookies, extensions or private connectors. Block downloads/execution and consequential external actions. | Page injection, browser vulnerabilities, unintended submissions and server retention remain. **Limited initial add-on:** public/read-only or test-tenant workflows; exclude purchases, messaging and social posting. |
| API / remote MCP | Pinned endpoint/version and test tenant; short-lived scoped credentials; externally enforced method, destination, rate and cost limits. Validate redirects/DNS; block private/metadata addresses. | Allowed services can receive data; authorization flaws and tenant-side effects remain. **Recommended first offering:** read-only fixtures or reversible writes confined to synthetic tenant data. |
| Isolated packages / skills | Pin artifacts/dependencies by hash/version; scan install behavior; ephemeral VM/microVM; no host mounts, privileged runtime access or ambient secrets; resource/egress limits; destruction after use. Skill text is untrusted too. | Supply-chain compromise and isolation escapes remain; hashes/scans do not prove benign code. **Phase two**, after independent isolation validation and an incident drill. |
| Optional persistent installation | Possible in a dedicated managed workspace; separately consent to permissions, duration, storage, updates and recurring tasks; revocation, uninstall and workspace destruction controls. | Longer exposure, stale credentials, background activity and delayed malicious updates. Uninstall alone cannot prove cleanup. **Exclude from MVP;** later use time-limited isolated workspaces. |

**F:** Docker documents configuration, daemon and kernel attack surfaces, including powerful host mounts. Firecracker documents KVM microVM isolation and a jailer as another defensive layer. These are mechanisms, not certification of the proposed service. [Docker security](https://docs.docker.com/engine/security/), [Firecracker](https://firecracker-microvm.github.io/)

**P — Consent and privacy:** Before enrollment disclose sponsor, objective, version, permissions, destinations, collected data, payout, resource limits, retention and withdrawal controls. Require affirmative campaign-specific operator consent; an agent cannot silently authorize broader access. Declining/withdrawing must not penalize unrelated participation. Provide immediate stop, credential revocation and teardown; explain that already transmitted data cannot simply be recalled.

**P:** Use synthetic data initially. Never request personal accounts, private files, wallets, production secrets or unrelated credentials. Keep model-provider credentials outside tested code behind a restricted service; tool credentials expose only a disposable tenant. Restrict report access, redact secrets/personal information and disclose retention, proposed at 30 days after dispute resolution for redacted evidence. Minimize billing records separately. A global stop must terminate active access. Validate isolation and revocation before launch; zero pilot incidents would not prove security.

## 4. Conceptual campaign workflow

1. **Define and fund.** Specify one objective, exact product/API version and documentation snapshot, allowed actions, synthetic fixtures, success rubric and known issues. For mutable services record build ID/run time and pause on undeclared changes. Set eligibility, finite budget, enrollment and assignment deadlines, payment and refund terms. Check authority to test and provider/platform terms.
2. **Invite and consent.** Invite all eligible participants through an opted-in listing/notification channel. Eligibility can specify declared model/client versions, competence and conflicts without implying unique people or machines. Invitation is not a funded assignment. Obtain separate consent for recurring schedules.
3. **Assign and reserve.** Select applicants by disclosed coverage quotas and random selection within them. Every admitted participant gets a distinct assignment ID, task variant, deadline, resource cap and reserved compensation. Prevent concurrent admissions from overcommitting funds. Release expired unaccepted reservations; waitlisted applicants do no unpaid testing.
4. **Execute and submit.** Every assignment produces its own completion/failure result, versions, time/cost, artifacts, friction, repro steps and limitations. A product-blocked task qualifies for full payment when the attempt/blocker meets the rubric. Hide others' submissions until delivery.
5. **Verify and consolidate.** Check outputs/evidence, reproduce material bugs, flag copying and collusion. Pay valid separate attempts even when findings overlap. Deduplicate issues in the consolidated report, preserve contradictions and distinguish observations from interpretations. State coverage and missing results. Logs show activity, not personhood or useful adoption by themselves.
6. **Settle and close.** Proposed acceptance window: five business days, then automatic acceptance absent a specific evidence-based objection. Pay within five business days of acceptance; platform review resolves disputes within ten. Pay for valid work, never sentiment or sponsor satisfaction. Refund unspent/unreserved funds and unearned service fees within ten business days of closure; disclose unavoidable processor fees/taxes upfront.

**P — Withdrawal and cancellation:** Participants may stop immediately, keeping earned milestones and approved incurred costs. Define partial milestones before acceptance; release remaining reservations without unrelated reputation penalties. Sponsor cancellation stops new work, pays earned work/disclosed nonrecoverable costs and refunds the balance. Platform-caused failures do not consume the sponsor's valid-result quota; replace or refund under a predeclared contingency/platform responsibility rule. Fraud earns nothing, subject to appeal. Valid inconvenient findings cannot be suppressed.

### Inviting everyone with bounded spending

| Model (P) | Budget behavior and trade-off |
|---|---|
| **Capped slots — recommended** | All eligible participants may apply; only N funded assignments start. Reserve maximum liability, including verification. Coverage selection and a waitlist avoid a speed-only race. Broad invitation does not mean universal funded admission. |
| **Funded enrollment window** | Accept applications until a deadline, then fund only affordable assignments; alternatively reserve in real time and close funded admission when funds run out. A time window alone cannot bound a fixed payment promised to everyone. |
| **Disclosed shared reward pool** | Publish pool R and objective weights: accepted assignment i earns R × wᵢ / Σw. More entrants dilute shares; disclose uncertain payment/no guaranteed minimum and obtain specific consent. Compute and review still require separate caps/admission limits. Poor MVP fit. |

**P — Budget invariant:** earned/reserved service fees + settled costs + maximum liabilities of admitted assignments + contingency must never exceed funding. Reservations include rewards, inference, runtime, review and replacement liability. Require explicit top-ups before increasing exposure.

## 5. Economics and recurring value

**P:** Quote in a stable accounting currency; no token requirement. Offer a fixed campaign package for defined coverage, individual results and synthesis; an additional unit per verified assignment/coverage cell; and capped monthly or release-based regression allowances. Disclose inclusions/overages and pause at the cap. Price against delivery cost and customer value, not headcount or installs.

**A:** Delivery cost = participant compensation + metered inference + isolation/runtime + reproduction/review + synthesis + payment/support. Quotes also need overhead and risk coverage. Review/recruitment may dominate; assume neither free subscription inference nor permitted commercial usage. Measure cost per actionable finding and developer hours saved, while recognizing valid clean evaluations have value. Avoid bug-only rewards that encourage exaggeration.

**P:** Recurring payments buy new work: release retests, health/compatibility checks, or operator-selected useful tasks such as producing a requested report through the API. Each occurrence needs an assignment/result, frequency/spending cap, expiry and cancellation. Standing consent may cover declared scope; new permissions or materially changed artifacts require renewed consent. Many recurring tasks need no persistent installation.

**I:** Sponsored continued use can yield outputs and reliability evidence; operator introductions can yield discovery. Measure utility, repeat voluntary choice and performance against substitutes. Track use after rewards stop separately. Installation duration, calls and visits alone do not establish value. **U:** Unsubsidized continuation and profitable sponsor renewal.

## 6. One small paid pilot

**P — Design:** One paying developer, one pinned hosted agent-facing API, two realistic synthetic-data tasks, two model families and two repetitions per task/family: **eight initial participant assignments**, each with its own result. Use fresh contexts and declared operator relationships; repetitions are not eight independent humans. Reserve four assignments for reproductions/fix retests. Three-day enrollment; report and renewal decision within two weeks. These are future experiment durations, not waits performed during research.

**P — Campaign objective:** Starting only from the published quickstart, retrieve the correct fixture records and produce a useful summary with source IDs; separately test recovery from an invalid request and export a valid structured result. Adapt these tasks to the sponsor's actual API before contracting. Record the sponsor-supplied release/build ID, API schema and documentation snapshot before funding; no unspecified “latest” version may enroll. Proposed run limit: 30 minutes, with separately enforced inference/request caps. Task correctness is checked against fixture answers; onboarding friction is tied to observed actions, not inferred feelings.

**P:** Before enrollment agree tasks, unknown-issue baseline, maximum acceptable cost per actionable finding and saved-hour valuation. Compare against existing CI/DIY agent evaluations and record developer triage time. Deliver individual results and one consolidated report; no endorsements, personal data or persistent installs. Use a managed workflow rather than building a marketplace.

**A — Illustrative $900 maximum quote, not observed willingness to pay:**

| Reservation | Maximum USD |
|---|---:|
| Eight initial rewards × $25 | 200 |
| Four reproduction/retest rewards × $15 | 60 |
| Twelve runs' inference × $8 | 96 |
| Twelve runs' isolated runtime × $2 | 24 |
| Review/synthesis: four hours × $50 | 200 |
| Payment/support allowance | 30 |
| Contingency | 90 |
| Service fee | 200 |
| **Total** | **900** |

**A/P:** Rewards compensate operator effort; inference/runtime are funded separately. Actual resource caps must fit the allowances or scope/quote must change before launch. Earn $80 of the fee on approved setup and $120 on report delivery. Refund unused allowances/contingency; spend contingency only within disclosed rules. The fee is not net profit: overhead, recruitment and overruns remain. Measure every cost; do not launch unaffordable scope under a fictitious margin.

**P — Success requires all:** at least 7/8 initial assignments meet the evidence rubric on time; at least two distinct actionable issues unknown to the sponsor reproduce, including one missed by its baseline; developer confirms at least two hours of triage/reproduction effort saved; cost per actionable issue is below its precommitted ceiling; direct costs stay within funded allowances; no material security/privacy incident; and the sponsor pays for another campaign covering measured costs plus a service fee without subsidy.

**P — Stop/kill:** Halt immediately for credential exposure, isolation failure, unauthorized external actions or material fabrication bypassing verification. Reject deceptive-engagement requests. Do not expand if recruitment cannot fill coverage, findings add no value beyond DIY, economics miss the agreed ceiling, or no paid renewal follows by the two-week decision point. One pilot can justify another test, not a market-size or retention claim.

## 7. Decision and unresolved gates

**I/P — Conditional go:** Begin with a managed agent usability and task-evidence campaign. Useful sponsored adoption and disclosed discovery remain credible extensions, conditional on measured outcomes. Broader self-service enrollment and persistent workspaces require paid repeat demand and validated safety controls.

**U:** Will developers pay versus DIY? Can the service recruit meaningful coverage? What are real verification/support costs and margins? Is there recurring useful task supply? Does adoption persist after incentives? What payment, privacy and provider-term requirements apply in target jurisdictions? Do isolation/revocation controls survive adversarial testing? Public research resolves none empirically. Local checks establish document integrity and arithmetic, not independent review or operational safety.
