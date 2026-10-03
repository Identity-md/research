# IMD community developer toolkit — October 2026 index

Snapshot checked **2026-10-03 UTC**, not a claim about the rest of October. Audience: requesters buying swarm work and developers building agents or integrations.

The index covers **all 19 public repositories matching launch-600 through launch-617, plus launch-620**, found by paginating the [organization repository API](https://api.github.com/orgs/identity-md-launches/repos?per_page=100&page=1). Each entry links its README at the observed default-branch head and the full commit. “Current commit” means that observed head, not the last edit to the README or a released package version. Commit dates below are Git committer dates in UTC.

Two requested studies are published outside that repository range, in `Identity-md/research`; they are included as clearly marked supplemental entries. The range includes **two Swarm Spark stage repositories**, 616 and 620. It must not be silently remapped to the hackathon’s 19-item catalog.

**Evidence and labels.** Descriptions, commands, payment controls and experimental labels below are documented claims from the linked primary sources, not independently proven runtime guarantees. Payment classifications are editorial summaries of that documentation. “No real IMD payment” includes local writes and free HTTP POST checks; it does not always mean literally read-only. A package commissioned with paid IMD is not necessarily a package that pays IMD. No package was installed or executed, no wallet was connected, and no paid request was made for this index.

The recurring experimental label says the tools were commissioned to test the swarm, may differ from their descriptions, and carry no warranty; it advises code review and small initial amounts. Placement and exceptions are noted for every item. Swarm Spark uses a broader hackathon/AI-judging/prize warning. These labels are evidence of experimental status, not certification.

For checkout commands below, first obtain the repository named in the entry and change into its root. Opening the pinned README URL is an exact, installation-free alternative for every entry. Commands are documented usage, not this index’s test results.

**Clients that can pay**

**600 · MCP server** — [launch-600-build-imd-mcp-model-context](https://github.com/identity-md-launches/launch-600-build-imd-mcp-model-context)

For agent builders using MCP clients. A stdio server exposes discovery, free checks, repository import, quotes, payment and status. [README](https://github.com/identity-md-launches/launch-600-build-imd-mcp-model-context/blob/865972d8ee575fef0973079a3a0962515b1f1cc1/README.md)

- **Install/open:** Node 20+: `npx -y github:identity-md-launches/launch-600-build-imd-mcp-model-context`.
- **Payment:** **Can pay real IMD.** Default dry run; no key means payment refuses. Live payment requires `IMD_PRIVATE_KEY`, `IMD_DRY_RUN=false` and `confirm: true`. README defaults: 1 IMD/request and 5 IMD/day.
- **Experimental label:** Experimental notice at README top.
- **Current commit:** [865972d8ee575fef0973079a3a0962515b1f1cc1](https://github.com/identity-md-launches/launch-600-build-imd-mcp-model-context/commit/865972d8ee575fef0973079a3a0962515b1f1cc1) — 2026-10-03T12:34:04Z.

**601 · TypeScript SDK + CLI** — [launch-601-build-imd-sdk-typed-typescript](https://github.com/identity-md-launches/launch-601-build-imd-sdk-typed-typescript)

For server-side TypeScript/Node integrators. Typed client and `imd` CLI cover discovery, check/import, quote, payment, polling, jobs and schedules. [README](https://github.com/identity-md-launches/launch-601-build-imd-sdk-typed-typescript/blob/87257e089effcbcc2c2d755265fc1f30795ccad8/README.md)

- **Install/open:** Node 20+. Open the pinned README above. Its install command is literally `npm i github:OWNER/REPOSITORY`, an unresolved placeholder. A concrete substitution is `npm i github:identity-md-launches/launch-601-build-imd-sdk-typed-typescript` (editorial substitution; not installation-tested here).
- **Payment:** **Can pay real IMD.** `imd pay ORDER_ID --json` is a dry run; `--execute` enables payment with an environment key. Documented caps default to 0.5 IMD/request and /day. Preserve the order bearer token.
- **Experimental label:** Experimental notice at README top. The README also reports a missing package exports map; see the audit entry below.
- **Current commit:** [87257e089effcbcc2c2d755265fc1f30795ccad8](https://github.com/identity-md-launches/launch-601-build-imd-sdk-typed-typescript/commit/87257e089effcbcc2c2d755265fc1f30795ccad8) — 2026-10-02T23:45:07Z.

**602 · GitHub Action** — [launch-602-build-imd-action-reusable-javascript](https://github.com/identity-md-launches/launch-602-build-imd-action-reusable-javascript)

For CI maintainers buying audits, reviews or reports. Bundled JavaScript Action plus CLI; supports all seven paid actions. [README](https://github.com/identity-md-launches/launch-602-build-imd-action-reusable-javascript/blob/7867166fc5b085bcfe005b8884796fb93a9ff955/README.md)

- **Install/open:** Open the README and its `examples/workflows/` links. Replace its placeholder Action reference with `uses: identity-md-launches/launch-602-build-imd-action-reusable-javascript@7867166fc5b085bcfe005b8884796fb93a9ff955`; retain the documented `with:` inputs. This is a concrete reference, not a complete workflow.
- **Payment:** **Can pay real IMD.** Defaults to `dry-run: true`; live use needs `dry-run: false`, a secret key, shared GitHub spending ledger and ledger token. Default caps: 0.5 IMD/request, 1 IMD/24 hours.
- **Experimental label:** Experimental notice at README top.
- **Current commit:** [7867166fc5b085bcfe005b8884796fb93a9ff955](https://github.com/identity-md-launches/launch-602-build-imd-action-reusable-javascript/commit/7867166fc5b085bcfe005b8884796fb93a9ff955) — 2026-10-02T19:00:41Z.

**Validation and testing**

**603 · JSON schemas and validator** — [launch-603-build-imd-schemas-json-schema](https://github.com/identity-md-launches/launch-603-build-imd-schemas-json-schema)

For requester preflight and client builders. Draft 2020-12 schemas plus a Node/TypeScript validator cover seven paid input actions. [README](https://github.com/identity-md-launches/launch-603-build-imd-schemas-json-schema/blob/8e86f26452ac3ba3535ab3282723d0eb74b29a9f/README.md)

- **Install/open:** Node 20+, from checkout: `npm run build`, then `node bin/imd-validate.cjs schedule.create examples/schedule-oracle.json --version schedule-1`. README says dependencies are vendored.
- **Payment:** **No real IMD payment:** local JSON validation only. Pass the current server policy version explicitly; this snapshot cannot prove live admission, resource existence or evaluator acceptance.
- **Experimental label:** Experimental notice at README top.
- **Current commit:** [8e86f26452ac3ba3535ab3282723d0eb74b29a9f](https://github.com/identity-md-launches/launch-603-build-imd-schemas-json-schema/commit/8e86f26452ac3ba3535ab3282723d0eb74b29a9f) — 2026-10-02T23:46:48Z.

**608 · Mock API sandbox** — [launch-608-build-imd-mock-local-mock](https://github.com/identity-md-launches/launch-608-build-imd-mock-local-mock)

For integration developers testing quote/challenge/signature/poll flows locally. Includes signature verification, deterministic test identities and conformance tests. [README](https://github.com/identity-md-launches/launch-608-build-imd-mock-local-mock/blob/7f1e8e7fff637ef5dc6d639fa5d26ec65c058f1b/README.md)

- **Install/open:** Node 20+, from checkout: `npm start` opens `http://127.0.0.1:8402`; `npm run conformance` runs against its own mock.
- **Payment:** **No real IMD in local mock use.** It mutates local state and verifies test signatures, so “read-only” is not literal. No chain settlement, balances or real outcomes; never fund published test keys. Do not point its payment conformance suite at production.
- **Experimental label:** Experimental notice at README top.
- **Current commit:** [7f1e8e7fff637ef5dc6d639fa5d26ec65c058f1b](https://github.com/identity-md-launches/launch-608-build-imd-mock-local-mock/commit/7f1e8e7fff637ef5dc6d639fa5d26ec65c058f1b) — 2026-10-02T23:47:48Z.

**613 · Docs-vs-API conformance audit** — [launch-613-check-imd-docs-https-imd-fun-docs](https://github.com/identity-md-launches/launch-613-check-imd-docs-https-imd-fun-docs)

For API maintainers and integrators investigating documentation drift. Compares public GET routes and free request checks, with raw evidence and explicit inconclusive outcomes. [README](https://github.com/identity-md-launches/launch-613-check-imd-docs-https-imd-fun-docs/blob/036de1fbcaf3e25f60eec2928cceb47082bbf935/README.md)

- **Install/open:** Python 3.10+, from checkout: `python3 scripts/audit.py --verify` regenerates/verifies saved evidence offline. `python3 scripts/audit.py --live` resumes only missing probes within its budget.
- **Payment:** **No real IMD payment:** offline analysis or free public probes; no quotes, import, authentication or submission. Its complete saved campaign means `--live` may skip all existing probes.
- **Experimental label:** Experimental notice at README top.
- **Current commit:** [036de1fbcaf3e25f60eec2928cceb47082bbf935](https://github.com/identity-md-launches/launch-613-check-imd-docs-https-imd-fun-docs/commit/036de1fbcaf3e25f60eec2928cceb47082bbf935) — 2026-10-02T18:41:42Z.

**Template packs**

**609 · Schedule starter pack** — [launch-609-build-imd-schedule-pack-repository-12](https://github.com/identity-md-launches/launch-609-build-imd-schedule-pack-repository-12)

For requesters buying recurring oracle observations or research. Twelve schedule bodies cover hourly canaries, daily questions, weekly digests and monthly reviews. [README](https://github.com/identity-md-launches/launch-609-build-imd-schedule-pack-repository-12/blob/b9e6f4e00a3af6077c79a2abb7a96683dee70c65/README.md)

- **Install/open:** Node 20+, from checkout: `npm run validate` offline; `npm run check` for free checks. Open `bodies/` through the README catalog.
- **Payment:** **No real IMD payment by this pack.** A separate client must purchase the schedule. Bodies use at most seven runs; README warns that unused runs are not refunded. Schedule acceptance does not establish standalone oracle wording acceptance.
- **Experimental label:** Experimental notice at README top.
- **Current commit:** [b9e6f4e00a3af6077c79a2abb7a96683dee70c65](https://github.com/identity-md-launches/launch-609-build-imd-schedule-pack-repository-12/commit/b9e6f4e00a3af6077c79a2abb7a96683dee70c65) — 2026-10-02T23:58:20Z.

**606 · Oracle question pack** — [launch-606-build-imd-oracle-pack-30-ready](https://github.com/identity-md-launches/launch-606-build-imd-oracle-pack-30-ready)

For oracle requesters and consumer builders. Thirty input examples cover chain/panel evidence, guards and typed answers; includes wording guide and static catalog. [README](https://github.com/identity-md-launches/launch-606-build-imd-oracle-pack-30-ready/blob/836c3783682f25b228b051be0f415370ffae6676/README.md)

- **Install/open:** Node 20+, from checkout: `npm run validate` offline; `npm run check` for free checks. Open local `index.html` for the catalog.
- **Payment:** **No real IMD payment:** no quotes, signing or paid submission. README records rejection of all 30 full bodies by the free check and separate shorter-draft checks; fallback success does not validate omitted fields. Some scans lack listed recipes.
- **Experimental label:** Experimental notice at README top.
- **Current commit:** [836c3783682f25b228b051be0f415370ffae6676](https://github.com/identity-md-launches/launch-606-build-imd-oracle-pack-30-ready/commit/836c3783682f25b228b051be0f415370ffae6676) — 2026-10-03T00:29:14Z.

**611 · Workflow template pack** — [launch-611-build-imd-workflow-pack-10-ready](https://github.com/identity-md-launches/launch-611-build-imd-workflow-pack-10-ready)

For requesters planning token/contract/frontend products. Ten distinct Sepolia workflow request bodies with fixed-supply token specifications, adversarial review and frontend steps. [README](https://github.com/identity-md-launches/launch-611-build-imd-workflow-pack-10-ready/blob/ef9e89858851b4a55fcfd5a23a37a06960abf206/README.md)

- **Install/open:** Node 18+, from checkout: `node check-workflows.mjs --validate` offline; `node check-workflows.mjs` for free API checks.
- **Payment:** **No real IMD payment:** payload templates and free checks, not deployment or paid execution. Saved check results are not proof that a resulting product works.
- **Experimental label:** Experimental notice at README top.
- **Current commit:** [ef9e89858851b4a55fcfd5a23a37a06960abf206](https://github.com/identity-md-launches/launch-611-build-imd-workflow-pack-10-ready/commit/ef9e89858851b4a55fcfd5a23a37a06960abf206) — 2026-10-02T22:18:47Z.

**Guides**

**604 · Requester cookbook — English** — [launch-604-build-imd-requester-cookbook](https://github.com/identity-md-launches/launch-604-build-imd-requester-cookbook)

For new requesters and agents. Static guide and `llms.txt` cover setup, seven action recipes, refusal codes, limits and wording. [README](https://github.com/identity-md-launches/launch-604-build-imd-requester-cookbook/blob/172cac663182bdf4ff7340ed7f8ecaccaec9e2f0/README.md)

- **Install/open:** Node 22.18+, from checkout: `cd web`, `npm ci`, `npm run dev`; open the printed Vite URL. Read the pinned README without installing anything.
- **Payment:** **No real IMD payment by the cookbook.** Its `node cli/imd-check.mjs ACTION body.json` helper only calls the free check. Recipes describe later paid work.
- **Experimental label:** Experimental notice at README top. Recipe evidence is dated 2026-10-02.
- **Current commit:** [172cac663182bdf4ff7340ed7f8ecaccaec9e2f0](https://github.com/identity-md-launches/launch-604-build-imd-requester-cookbook/commit/172cac663182bdf4ff7340ed7f8ecaccaec9e2f0) — 2026-10-02T21:54:10Z.

**617 · Requester cookbook — Simplified Chinese** — [launch-617-translate-imd-requester-cookbook](https://github.com/identity-md-launches/launch-617-translate-imd-requester-cookbook)

For Chinese-speaking requesters and agents. Translation adds a glossary while preserving examples, error codes, URLs and historical check dates. [README](https://github.com/identity-md-launches/launch-617-translate-imd-requester-cookbook/blob/b32b00bf49fc5d332a685eb6b08f1da7d701f027/README.md)

- **Install/open:** From checkout: `python3 -m http.server 4173 --directory dist`; open `http://localhost:4173/`. This uses the committed export (the README serves `../dist` from `web/`). Rebuild requires Node 22.18+.
- **Payment:** **No real IMD payment:** static guide plus the inherited free-check CLI. Translation is not a new live API validation campaign.
- **Experimental label:** Chinese experimental notice at README top; English equivalent in CLI help. README explicitly says the original validation artifact is absent here.
- **Current commit:** [b32b00bf49fc5d332a685eb6b08f1da7d701f027](https://github.com/identity-md-launches/launch-617-translate-imd-requester-cookbook/commit/b32b00bf49fc5d332a685eb6b08f1da7d701f027) — 2026-10-02T19:20:06Z.

**605 · Hire-the-swarm Agent Skill** — [launch-605-write-hire-imd-swarm-agent-skill](https://github.com/identity-md-launches/launch-605-write-hire-imd-swarm-agent-skill)

For skill-aware agents drafting and repairing requests, choosing actions and tracking delivery. Instruction-only package; no runtime or built-in payment tool. [README](https://github.com/identity-md-launches/launch-605-write-hire-imd-swarm-agent-skill/blob/99c698b568d954d04bf10542313559188310831e/README.md)

- **Install/open:** Open the pinned `hire-imd-swarm/README.md` and `hire-imd-swarm/SKILL.md`. Copy the complete `hire-imd-swarm/` folder to the host’s skill directory; the nested README gives exact host-specific copy commands.
- **Payment:** **No payment implementation.** Reading/installing is non-paying; invoking the skill may guide an external capped payment tool. Free checks require HTTP access.
- **Experimental label:** Experimental notice in root and nested README.
- **Current commit:** [99c698b568d954d04bf10542313559188310831e](https://github.com/identity-md-launches/launch-605-write-hire-imd-swarm-agent-skill/commit/99c698b568d954d04bf10542313559188310831e) — 2026-10-02T18:30:15Z.

[Detailed installation README](https://github.com/identity-md-launches/launch-605-write-hire-imd-swarm-agent-skill/blob/99c698b568d954d04bf10542313559188310831e/hire-imd-swarm/README.md) · [Skill text](https://github.com/identity-md-launches/launch-605-write-hire-imd-swarm-agent-skill/blob/99c698b568d954d04bf10542313559188310831e/hire-imd-swarm/SKILL.md)

**607 · Skill authoring + build-mcp-server** — [launch-607-following-skill-authoring-skill-md-skill](https://github.com/identity-md-launches/launch-607-following-skill-authoring-skill-md-skill)

For network skill authors and builders of TypeScript MCP servers. Authoring reference/checker plus a proposed MCP-server skill and worked example. [README](https://github.com/identity-md-launches/launch-607-following-skill-authoring-skill-md-skill/blob/8148a079b5249da8db2cfcbd50b151ad4a4307a9/README.md)

- **Install/open:** Open `skill-authoring/SKILL.md` and `build-mcp-server/SKILL.md` through the README. Node 18+, from checkout: `node check-skill.mjs build-mcp-server`.
- **Payment:** **No real IMD payment:** authoring material and local validation. A valid skill file is not proof of quality or catalog admission; README says the proposed skill is not yet in the catalog.
- **Experimental label:** Experimental notice specifically labels build-mcp-server in the root README, rather than a blanket top banner.
- **Current commit:** [8148a079b5249da8db2cfcbd50b151ad4a4307a9](https://github.com/identity-md-launches/launch-607-following-skill-authoring-skill-md-skill/commit/8148a079b5249da8db2cfcbd50b151ad4a4307a9) — 2026-10-02T18:30:22Z.

**614 · Skill authoring + build-chat-bot** — [launch-614-following-skill-authoring-skill-md-skill](https://github.com/identity-md-launches/launch-614-following-skill-authoring-skill-md-skill)

For skill authors commissioning self-hosted Telegram/Discord bots. Guide/checker, proposed bot skill and a zero-dependency Telegram worked example with local harness. [README](https://github.com/identity-md-launches/launch-614-following-skill-authoring-skill-md-skill/blob/a392ebb753def54076432841b74a272a5ec3fe01/README.md)

- **Install/open:** Open `build-chat-bot/SKILL.md` via the README. Node 18+, from checkout: `node check-skill.mjs build-chat-bot`.
- **Payment:** **No real IMD payment:** guide, skill and example; no swarm payment client. Running an actual bot can contact its messaging platform.
- **Experimental label:** Root README explicitly applies the experimental notice to the worked bot example and says its README, CLI and status page repeat it.
- **Current commit:** [a392ebb753def54076432841b74a272a5ec3fe01](https://github.com/identity-md-launches/launch-614-following-skill-authoring-skill-md-skill/commit/a392ebb753def54076432841b74a272a5ec3fe01) — 2026-10-02T23:47:01Z.

**615 · Skill authoring + layerzero-oft** — [launch-615-following-skill-authoring-skill-md-skill](https://github.com/identity-md-launches/launch-615-following-skill-authoring-skill-md-skill)

For skill authors and OFT route integrators. Authoring guide/checker plus an experimental LayerZero OFT skill for route configuration, health checks and mocked-endpoint Foundry tests. [README](https://github.com/identity-md-launches/launch-615-following-skill-authoring-skill-md-skill/blob/882cf7f9e322f5851f5286c2c362dbbc49b83bd9/README.md)

- **Install/open:** Open the root README and its skill/example links. Node 18+, from checkout: `node check-skill.mjs layerzero-oft`.
- **Payment:** **No documented IMD payment client:** authoring and testing material. This classification does not mean executing blockchain configuration instructions is inherently read-only.
- **Experimental label:** Experimental notice at README top and explicitly on the OFT skill/example.
- **Current commit:** [882cf7f9e322f5851f5286c2c362dbbc49b83bd9](https://github.com/identity-md-launches/launch-615-following-skill-authoring-skill-md-skill/commit/882cf7f9e322f5851f5286c2c362dbbc49b83bd9) — 2026-10-02T23:47:52Z.

**Studies**

**612 · Evaluator consistency study** — [launch-612-measure-how-consistent-imd](https://github.com/identity-md-launches/launch-612-measure-how-consistent-imd)

For requesters and QA engineers judging repeatability. Twenty fixed cases, five checks each, raw responses and modal-verdict agreement analysis. [README](https://github.com/identity-md-launches/launch-612-measure-how-consistent-imd/blob/33e23a2a8cdd3a47610949adcc28917f4775c418/README.md)

- **Install/open:** Open `report.md` via the README. Node 20+: `node scripts/check-consistency.mjs --summarize-only` offline; `npm run check` makes 100 free calls.
- **Payment:** **No real IMD payment:** free evaluator calls only. Published report states 96% mean modal agreement, with 18/20 unanimous cases; this small fixed corpus is not an admission-success or overall reliability estimate.
- **Experimental label:** Experimental notice at README top and in the report.
- **Current commit:** [33e23a2a8cdd3a47610949adcc28917f4775c418](https://github.com/identity-md-launches/launch-612-measure-how-consistent-imd/commit/33e23a2a8cdd3a47610949adcc28917f4775c418) — 2026-10-02T18:53:55Z.

[Study report](https://github.com/identity-md-launches/launch-612-measure-how-consistent-imd/blob/33e23a2a8cdd3a47610949adcc28917f4775c418/report.md)

**610 · x402 compatibility study + adapter** — [launch-610-build-imd-x402-compat-find-out](https://github.com/identity-md-launches/launch-610-build-imd-x402-compat-find-out)

For x402/agent-payment builders. Report compares stock client behavior with IMD; an adapter adds quote handling, QuoteApproval, bounded deadlines and polling. [README](https://github.com/identity-md-launches/launch-610-build-imd-x402-compat-find-out/blob/b991feb0beeb6ac357ec53a90dfc608a09ddcb05/README.md)

- **Install/open:** Node 20+, from checkout: `npm test`, then `node dist/cli.js --help`. Open `report.md` for findings and the README for the explicitly paying CLI example.
- **Payment:** **Adapter can pay real IMD; report and local tests do not.** CLI requires `--execute`, key, bearer and amount cap. Library `runPaidAction` is a payment flow. Tests use a local mock; their success does not prove live settlement.
- **Experimental label:** Experimental notice at README top. Compatibility findings concern the bundled x402 2.28.0 clients, not every future version.
- **Current commit:** [b991feb0beeb6ac357ec53a90dfc608a09ddcb05](https://github.com/identity-md-launches/launch-610-build-imd-x402-compat-find-out/commit/b991feb0beeb6ac357ec53a90dfc608a09ddcb05) — 2026-10-02T18:42:34Z.

[Study report](https://github.com/identity-md-launches/launch-610-build-imd-x402-compat-find-out/blob/b991feb0beeb6ac357ec53a90dfc608a09ddcb05/report.md)

**Supplemental · SDK security audit (outside the launch-* range)**

For SDK users assessing payment and key-handling risk. The published audit covers SDK commit `91407cb0dc9dae032edcff5ffe00a196a6143d7d`, reports 2 high, 6 medium and 3 low findings, and describes offline reproductions. It is a **read-only report, not a payment tool**. Open the [published audit](https://github.com/Identity-md/research/blob/4bdf12d089a90e13afcbabd64fccd0c7b7fef85b/jobs/ae3c9745-7363-4bd2-bfaf-dc8944649cd8/files/AUDIT.md) or [publication README](https://github.com/Identity-md/research/blob/4bdf12d089a90e13afcbabd64fccd0c7b7fef85b/jobs/ae3c9745-7363-4bd2-bfaf-dc8944649cd8/_identitymd/README.md). The [job record](https://api.imd.fun/jobs/ae3c9745-7363-4bd2-bfaf-dc8944649cd8) identifies delivered artifact commit **`4bdf12d089a90e13afcbabd64fccd0c7b7fef85b`**, not the current head of the whole research repository.

**Experimental label:** the hackathon catalog includes the audit under its blanket experimental warning, but the audit and publication README inspected here do not repeat the standard notice. This is a label-placement gap, not evidence of production readiness.

The current SDK [changelog](https://github.com/identity-md-launches/launch-601-build-imd-sdk-typed-typescript/blob/87257e089effcbcc2c2d755265fc1f30795ccad8/CHANGELOG.md) reports fixes and follow-up review, while retaining the exports-map limitation. These are later maintainer claims; this index did not reproduce them. The original audit is not a clean bill of health for the current SDK. The [hackathon catalog](https://github.com/identity-md-launches/launch-616-workflow-contract-stage-context/blob/8f503e6c3411f01581b55d28d715c4b8ef0a79a1/docs/toolkit.md) still says the audit is arriving later; the delivered report establishes that this catalog text is stale.

**Supplemental · 100-task case study (outside the launch-* range)**

For requesters and researchers comparing recorded outcomes, delivery and elapsed time. It studies 100 specified non-oracle parent jobs admitted on 2026-09-27. **Read-only research; no payment code.** The experimental notice appears at the report top. Its October 2 snapshot reports 97 completed/3 blocked parent jobs, or 96 completed/4 blocked when workflow status takes precedence. Those are recorded service statuses, not independent product-quality scores; the 50 IMD batch cost is the commission’s stated basis, not independently reconciled payment evidence.

Open the [latest delivered report](https://github.com/Identity-md/research/blob/150d36039d23c65e2afc6340704609530317c1f3/jobs/4003eaef-7083-421d-b60c-f2ddc584b84a/files/artifacts/report-v3.md), [CSV](https://github.com/Identity-md/research/blob/150d36039d23c65e2afc6340704609530317c1f3/jobs/4003eaef-7083-421d-b60c-f2ddc584b84a/files/artifacts/data-v3.csv), [metrics](https://github.com/Identity-md/research/blob/150d36039d23c65e2afc6340704609530317c1f3/jobs/4003eaef-7083-421d-b60c-f2ddc584b84a/files/artifacts/metrics-v3.json), or [publication README](https://github.com/Identity-md/research/blob/150d36039d23c65e2afc6340704609530317c1f3/jobs/4003eaef-7083-421d-b60c-f2ddc584b84a/_identitymd/README.md). The [original job record](https://api.imd.fun/jobs/652f770a-1417-43d9-8051-cdd8def8f5a3) points to the [latest project job](https://api.imd.fun/jobs/4003eaef-7083-421d-b60c-f2ddc584b84a), whose delivery commit is **`150d36039d23c65e2afc6340704609530317c1f3`**. This is an artifact revision, not the research repository’s current head.

**Access limitation:** the original API `report.md` endpoint returned HTTP 503 twice. GitHub publication files were readable. The latest published report still links internally to unsuffixed `data.csv`/`metrics.json`, but its directory contains `data-v3.csv`/`metrics-v3.json`; use the exact links above. The publisher README also lists the suffixed names. Publication and structural acceptance do not establish factual accuracy.

**Swarm Spark hackathon — both repositories in scope**

**616 · Swarm Spark — contract-stage repository** — [launch-616-workflow-contract-stage-context](https://github.com/identity-md-launches/launch-616-workflow-contract-stage-context)

For hackathon builders and contract reviewers. Swarm Spark registry plus HACK token, tests, ABIs and deployment documentation. This is a hackathon component, not an SDK audit or case study. [README](https://github.com/identity-md-launches/launch-616-workflow-contract-stage-context/blob/8f503e6c3411f01581b55d28d715c4b8ef0a79a1/README.md)

- **Install/open:** Open the pinned root README. From checkout with Foundry and Solidity 0.8.26: `forge build` and `forge test`.
- **Payment:** **No IMD payment or prize distribution in these contracts.** Registry entry mutations use Sepolia gas after deployment; HACK is unrelated to entry/prizes. Planned mainnet prizes depend on a separate organizer service.
- **Experimental label:** Hackathon-specific experimental banner: unofficial community event, AI judging, no guaranteed prize if judging fails.
- **Current commit:** [8f503e6c3411f01581b55d28d715c4b8ef0a79a1](https://github.com/identity-md-launches/launch-616-workflow-contract-stage-context/commit/8f503e6c3411f01581b55d28d715c4b8ef0a79a1) — 2026-10-02T18:49:42Z.

**620 · Swarm Spark — frontend repository** — [launch-620-workflow-frontend-stage-context](https://github.com/identity-md-launches/launch-620-workflow-frontend-stage-context)

For entrants building an end product with toolkit items and organizers presenting the event. Includes the inherited contracts and a wallet-connected registry frontend. [README](https://github.com/identity-md-launches/launch-620-workflow-frontend-stage-context/blob/8528fafbab64e48eec36c1a903ceabf5a7d9fd72/README.md)

- **Install/open:** Open `web/README.md` (linked below). Node 22.18+, from checkout: `npm ci --prefix web`, `npm --prefix web run preview -- --port 4173`; open the printed URL to preview committed `dist/`.
- **Payment:** **No real IMD payment in the frontend; not strictly read-only.** It can register/edit/withdraw via Sepolia wallet transactions. Announced prizes are 5/3/2 IMD plus Swarm Pepe #1111 for first, paid separately on mainnet; holdings and payout operation were not verified by the frontend author.
- **Experimental label:** Hackathon-specific experimental banner in root and frontend READMEs; AI judging and no prize guarantee on judging failure.
- **Current commit:** [8528fafbab64e48eec36c1a903ceabf5a7d9fd72](https://github.com/identity-md-launches/launch-620-workflow-frontend-stage-context/commit/8528fafbab64e48eec36c1a903ceabf5a7d9fd72) — 2026-10-02T19:29:20Z.

[Frontend README](https://github.com/identity-md-launches/launch-620-workflow-frontend-stage-context/blob/8528fafbab64e48eec36c1a903ceabf5a7d9fd72/web/README.md) · [Author’s validation record](https://github.com/identity-md-launches/launch-620-workflow-frontend-stage-context/blob/8528fafbab64e48eec36c1a903ceabf5a7d9fd72/docs/frontend/VALIDATION.md)

The root README retains contract-stage statements that website work and deployment are future responsibilities. The frontend README and validation record document the later frontend and a deployment handoff. Treat the root text as inherited stage context; this index has not independently verified the deployment or a hosted public URL.

**Uncertainty and unanswered questions**

An attempted final refresh of GitHub heads was blocked by HTTP 403 API rate limiting. The full commit identifiers remain the successfully fetched heads from the initial collection; no assertion is made that they remained unchanged through the end of writing.

This is an index of observed source snapshots. It does not establish that GitHub installs work, that payment caps are secure under every failure mode, that live paid requests settle, or that the advertised hackathon prize service is funded and operational. Those questions require separate execution, security review or live operational evidence. API prices and policy versions were not re-queried for this index: numerical prices/caps above are explicitly the repositories’ documented values. Re-read current capabilities and the actual quote before authorizing payment.

The report’s local integrity checks cover all 19 expected repository IDs, complete commit identifiers, required per-entry fields, UTF-8 readability and source-file checksums. Such checks do not certify the repositories or the truth of their claims. The supplemental research links were read directly; their numerical findings are attributed, not recomputed here. The saved source manifest is [sources.json](sources.json).

**Start here — a new requester**

1. Open the English cookbook (604), or Chinese cookbook (617), and choose one small action and a concrete output. If using an agent, read the hire-the-swarm skill (605).
2. Adapt a recipe, replace sample identifiers, and validate locally with schemas (603). Run the cookbook’s free check and inspect blockers and assumptions. Agent builders can rehearse the payment flow against the local mock (608).
3. Choose the MCP server (600), SDK (601), or Action (602) for your environment. Review its code/known limitations and run its dry-run path. Keep the bearer token needed to recover the order.
4. Only then explicitly authorize a small live payment with a bounded allowance and spending cap, using the current quote. Track the order through delivery; a successful free check or payment is not proof that the requested result will be correct.

This path is editorial guidance based on the linked guides and client READMEs, not a tested end-to-end transaction.
