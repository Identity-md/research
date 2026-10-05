# Audit report

> IMD Ember World - Audit12 source closure, World only
>
> Exact immutable review snapshot: https://github.com/tungweb3/imd-ember-world-review/tree/2f21b74cf61fe8fed9e3700d082b2dab38904b33
> Public parent: 35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a. Private TEAM source pin: 3a1ea7d0cabd40aaf1bd171d64fa64edeb6a2548 (not a request for private access).
> Period: this fixed snapshot prepared October 6, 2026 Taiwan time, compared with the latest completed Audit11/Report11.
>
> Question: Are the two remaining Audit11 scheduled-clock findings closed in this exact source without regressions in the previously closed Auth, ownership, Member M1, artifact or request-lane boundaries?
>
> Unofficial community project; NO Solidity in scope. TypeScript Cloudflare Worker / React SIWE; Member M1 writes persistent public profiles, so World is not wholly read-only. Genesis mint/contracts, Ember Coin functionality, 3D models/media/full frontend and live deployment are excluded. Use source/ and Submission12/FinalClosure/ as delivered; do not infer withheld runtime configuration or production state.
>
> Current closure matrix: exactly two rows.
> 1. A11-L1 (Low): scheduled non-finite clock reaching destructive housekeeping. Check NaN, +Infinity and -Infinity at EACH of the three sampled positions. All three samples must be finite before any DB helper, SQL or waitUntil work starts. Verify sessions, challenges, presence, member requests/history, probes/lanes/candidates and total DB changes unchanged; signed cookie stays readable after return to finite time. No partial cleanup may occur before a later invalid sample.
> 2. A11-I1 (Info): non-finite clock deleting a live 30-second probe, refunding backoff and admitting another lane request. Verify probe timestamps, budget, lane acquisitions and RPC calls at t+1ms remain unchanged after invalid scheduled input. Trace refused-lane probe retention as well as successful work. Confirm finite recovery at +10m/+60m.
>
> Only worker/app.ts changes production behavior. tests/scheduled-audit11.test.mjs is added; review runner registration/count tests are updated. Helpers, SQL/schema/migrations, dependencies, Auth lifecycle, ownership and request-lane implementation are unchanged. The previous six issues are previously closed unchanged context; challenge any regression you reproduce, regardless of severity.
>
> Finite controls must preserve three distinct advancing clock inputs, strict presence vs inclusive member/probe expiry boundaries, independent 200-row cleanup caps, independent missing-schema jobs, and no-DB no-clock behavior. A single shared finite timestamp would change existing helper inputs and is not equivalent.
>
> Sources: README.md, Submission12/REVIEW_INPUTS.md, Submission12/BOUNDARY_CHECK.json, Submission12/FinalClosure/CLOSURE_MATRIX.md, TEST_RESULTS.json, REVIEWER_EVIDENCE.json, SOURCE_MANIFEST.json, BUILD_DEPLOYMENT.json, SERVED_READBACK.json, and manifests/submission12-published-source.json; resolve these at the exact containing pin above. Prior final Audit11: https://github.com/Identity-md/research/blob/e7c4bb596a725863a8c23992926f6d2c59040005/jobs/63c31e2b-5d52-4a3b-a94c-21ef15f52e90/files/AUDIT.md
> Prior Report11: https://github.com/Identity-md/research/blob/193d49fca202162f17206af81aa8db6f1f7bda48/jobs/260746ad-ac5f-4013-89e1-2d70eb6dfc47/files/artifacts/report.md
>
> Reproduce offline from a clean exact checkout using real Node24.x, locked viem2.56.9 and migration-backed node:sqlite. In source/: npm ci --ignore-scripts; node scripts/review-tests.mjs --check; node --test --test-reporter=tap tests/scheduled-audit11.test.mjs; npm run test:review; node scripts/verify-artifact-closure.mjs. Supported runner selects29 files and clears inherited *_SOURCE selectors. Real Windows symlink permission is needed; EPERM is a failed/unavailable prerequisite, not a PASS. Do not replace crypto/Worker/SQLite, remove assertions, hide skips or insert arbitrary waits.
>
> TEAM measurements, not reviewer reproduction: target13/13; supported review728/728; private full1778/1778; artifact20/20; fresh private728/728+20/20; typecheck exit0. Final committed public checkout was freshly installed and measured preflight29, target13/13, review728/728, artifact20/20; zero failed/skipped/cancelled/todo. Public commit/object/content privacy passed316 text files,315 checksums,147 selected sources (131 exact,16 masked files,57 preserved mask lines), zero private commit intersection and zero unreachable stored objects. Raw private receipts are withheld. Public metadata records the earlier nine-stage phase; later same-pin public tests are additional TEAM records, not self-certifying committed verdicts.
>
> Calibration: identical published13-test evaluator on the unpatched baseline produced4 passes and9 actual assertion failures. A separate private offline-probe control produced1 candidate pass and1 baseline assertion failure, measuring old third-Infinity probe deletion/lane reacquisition. The combined fixture has an online owned seat for presence observability, which can mask extra baseline lane admission; do not conflate it with that separate private control or claim all its bytes were published.
>
> Native cleanup provider still reports BLOCK on manual-only update-coverage REVIEW, with sync-unconfigured and README-version NOT_CHECKED; no native FAIL. This is explicitly retained as a bounded source-only exception, not provider PASS or release approval. No production deployment/readback occurred; full frontend/browser/production D1, secrets, bindings, WAF, limiter and upstream behavior remain unmeasured release gates. Do not contact production, request private data, use real wallets/signatures, transact, pay, deploy or create jobs. Public repository/report reads and locked dependency downloads are permitted.
>
> Output: concise English Markdown, roughly1200-1800 words plus exactly two current closure rows and an evidence appendix. Rank any reproduced regression. For each row cite containing-pin source lines, reproduction/order, expected/actual mutations, SQL/tasks/RPC/budget/lane counts and residual bounded impact. Record commands/exits/errors/skips/shims and checks you could not run. Give SOURCE-CLOSURE and RELEASE-READINESS separately as PASS/BLOCKED/UNKNOWN with rationale. Separate reviewer measurements, TEAM claims, inference and unknowns. Completed/accepted means output delivery; tests, Low/Info labels and acceptance do not certify safety, endorsement, zero vulnerabilities or fund security.

| | |
|---|---|
| Repository | https://github.com/tungweb3/imd-ember-world-review.git |
| Commit | `2f21b74cf61fe8fed9e3700d082b2dab38904b33` |
| Job | `3ffb2bf9-fe8c-4433-aa15-333f218775bb` |
| Judged | 2026-10-05 20:59 UTC |
| Findings | none kept |

Four agents audited the code as it is at `2f21b74`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

The judge kept no findings: every specialist finding it could not reproduce was dropped. What it checked is below.

---

Judge's submission `33d044b5b6f3aebd2a3644abbc01635cb14cbb942b0222d2af370588bb35cab7`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
