# IMD Ember World: Report12 source-closure evidence review (World only)

**SOURCE-CLOSURE: PASS (bounded). RELEASE-READINESS: UNKNOWN.**

**Short answer.** Yes, within the bounded offline scope. At the exact public pin `2f21b74cf61fe8fed9e3700d082b2dab38904b33`, A11-L1 and A11-I1 are closed. One entry guard in `worker/app.ts` takes three clock samples and checks that all of them are finite before any helper, SQL statement or `waitUntil` task can start. I reproduced this independently, and I calibrated it against the unpatched parent `35ace95`. I found no regression in the previously closed Auth, ownership, Member M1, artifact or request-lane boundaries. The evidence supports bounded source closure only. Release readiness is unmeasured: there was no deployment, no production readback and no full frontend build.

"Accepted" or "completed" means this output was finished. It is not certification, endorsement, a claim of zero vulnerabilities, or proof that funds are safe.

Evidence labels used below:
- **[R]** reviewer reproduction, done by me in this review.
- **[T]** TEAM record. Raw private receipts are withheld.
- **[H]** historical official report.
- **[I]** my inference.
- **[U]** unavailable or unchecked.

Base URL for source links: `B = https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/`

## What changed

- **Production behavior.** Only `source/worker/app.ts` changes, at lines 152–163 ([B/source/worker/app.ts#L150-L164](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/source/worker/app.ts#L150-L164)) **[R]**, checked with `git diff --stat 35ace95 2f21b74`. The handler:
  - keeps the early `if(!env.DB)return;` (L151), so the no-DB path still samples no clock;
  - takes three samples, `presenceNow`, `memberNow` and `probeNow` (L153);
  - if any sample fails `Number.isFinite`, logs one fixed line, `scheduled {"status":"invalid_clock"}`, and returns (L154–156);
  - otherwise passes each helper its own sample (L157, L158, L162).
- **Everything else in `source/`.** The other changes are test and runner files: `tests/scheduled-audit11.test.mjs` is new, and `scripts/review-tests.mjs` (lines 13–14) and `tests/review-runner.test.mjs` (count 28→29, `SCHEDULED_AUDIT11_SOURCE` selector) are updated **[R]**.
- **Unchanged.** `git diff 35ace95 2f21b74 -- source/server source/migrations source/src source/package.json source/package-lock.json` is empty **[R]**. Helpers, SQL, schema, migrations, dependencies, Auth lifecycle, ownership and request-lane code are byte-identical to the parent. This matches the TEAM claim in [BOUNDARY_CHECK.json](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/Submission12/BOUNDARY_CHECK.json) (`helperChange:false`, `schemaChange:false`, `dependencyUpgrade:false`) **[T]**.
- **Where the old damage happened** (helper sinks, unchanged):
  - `PRUNE_SESSIONS`/`PRUNE_CHALLENGES` bound at [server/presence.ts#L36-L37, L59](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/source/server/presence.ts#L36-L59);
  - inclusive `expires_at<=?1` member prune at [server/member.ts#L42-L50](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/source/server/member.ts#L42-L50);
  - `INDEX_PROBE_PRUNE` at [server/auth.ts#L269-L285](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/source/server/auth.ts#L269-L285).

  None of these helpers validates `now` itself. They are now protected only because their single scheduled call site is guarded **[R][I]**.

## Current closure matrix (exactly two rows)

| ID / severity | Exact-pin location | Reproduction and order | Expected vs actual at pin | Verdict |
|---|---|---|---|---|
| **A11-L1 / Low**: a non-finite scheduled clock reached destructive housekeeping ([H] [Audit11 §1](https://github.com/Identity-md/research/blob/e7c4bb596a725863a8c23992926f6d2c59040005/jobs/63c31e2b-5d52-4a3b-a94c-21ef15f52e90/files/AUDIT.md)) | Guard at [app.ts#L153-L156](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/source/worker/app.ts#L153-L156); sinks are unchanged helpers | **[R]** Committed evaluator, 9 cases (NaN, +Inf, −Inf × sample 1, 2, 3); the other samples finite (T+1, T+2, T+3). **[R]** My separate probe: offline seat, refused limiter, the same 9 cases plus finite controls, run on both candidate and baseline. | **Expected:** every invalid sample position does zero work. **Actual [R]:** in all 9 cases, `sampled:3, tasks:0, sql:0, batches:0, rejected:0`. `total_changes()` delta is 0. Full row snapshots of sessions (2), login_challenges (2), seat_presence (1), profile_requests (2), profile_history (2), index_lane_probes (2), index_lanes (1) and index_candidates (1) are byte-identical. Upstream calls: 0. `/api/auth/session` returns 200 `signedIn:true`. Recovery at +10m and +60m sees SQL > 0, no rejections, still signed in, and only finite timestamps. **Baseline [R]:** an Infinity at sample 1 deleted the session (1→0), so `/api/auth/session` returned `signedIn:false` and `/api/me/home` returned 401. No later invalid sample can cause partial cleanup, because no task is registered until all three samples are checked (L154 comes before L157). | **CLOSED (bounded source)** |
| **A11-I1 / Info**: a non-finite clock deleted a live 30 s probe, refunding the backoff ([H] Audit11 §2) | Same guard, which now covers `pruneIndexProbes(env.DB, probeNow)` at [app.ts#L162](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/source/worker/app.ts#L162) | **[R]** Same 9 committed cases. Then a request at T+1 ms against a refused `chain:index:lane` limiter. **[R]** Offline control without an online seat (this keeps presence work from masking lane admission). | **Expected:** probe stays at (T, T+30000); lane/budget/RPC unchanged at +1 ms. **Actual [R]:** `probeAfterRequest` stays `{probed_at:T, expires_at:T+30000}`. Work stays `{index:0, rpc:1, budget:1, lane:1}` before and after, response 200 `recheck:"limited"`. The expired-probe row is also retained in the invalid cycle. Finite recovery at +10m and +60m prunes the old probe and writes a new one at `later`/`later+30000`, for cumulative `{index:0, rpc:3, budget:3, lane:3}`. **Baseline offline control [R]:** with Infinity at sample 3, the probe was deleted after cron, re-inserted at (T+1, T+30001), and lane calls went **1→2**. NaN and −Inf did not delete it. **Candidate [R]:** unchanged lane count of 1 in all 9 cases. | **CLOSED (bounded source)** |

The six Audit10/Report10 issues are context only and were closed previously. Their tests (auth-audit10, ownership-audit10, artifacts-audit10, auth-audit9 and so on) are part of the 728-test supported run, which passed with no failures **[R]**. I did not reproduce any regression in them.

## Finite-control equivalence

- **Distinct, advancing inputs.** The committed finite control passes samples T+10, T+20 and T+30 and checks that each helper gets its own value [tests/scheduled-audit11.test.mjs#L120-L141](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/source/tests/scheduled-audit11.test.mjs#L120-L141) **[R]**. It verifies:
  - the strict presence cutoff: the exact-boundary session and unused challenge are kept, and `updated_at` is T+10;
  - inclusive member expiry at T+20: entries at T+15 and T+20 are deleted, T+21 is kept;
  - inclusive probe expiry at T+30: entries at T+25 and T+30 are deleted, T+31 is kept.

  A single shared timestamp would fail these assertions.
- **Independent 200-row caps.** The 201-row backlog drains as 200 rows and then 1, separately for each job (L143–153).
- **Independent missing-schema jobs** (L155–172) and **no-DB: no clock sample, no SQL, no task** (L174–180) both pass **[R]**.
- **One equivalence nuance [I].** The baseline interleaved each `now()` with the synchronous prefix of the previous helper. The candidate takes the three samples back-to-back. With real `Date.now()`, the three values may now be equal, where before they could differ by a few milliseconds. That is harmless for these cutoff semantics, but it is a minor timing difference, not strict identity.

## Remaining limitations (not relabelled as fixes)

1. **Defense in depth [R][I].** The helpers still accept non-finite `now`. Closure depends on the one guarded call site. A future direct caller would reintroduce the risk. As a side probe, I checked the request-path opportunistic `pruneMemberRecords` ([member.ts#L176, L214](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/source/server/member.ts#L170-L214)) under a NaN, +Inf or −Inf request clock on bootstrap. It deleted nothing: +Inf returned 401 before the prune, and NaN and −Inf deleted 0 rows. This was outside the two rows and was not tested exhaustively.
2. **Liveness [I].** A persistently non-finite clock now skips all housekeeping, failing safe rather than destroying data. Expired rows then build up until the clock is finite again. This is by design and is unmeasured in production.
3. **Calibration scope [R].** The committed evaluator's 9 baseline failures all hit the first assertion (the full row snapshot). Some of that difference is the baseline's finite helpers doing legitimate cleanup in the same cycle, on top of the non-finite damage. The combined fixture also uses an online owned seat. So the decisive causal evidence for A11-I1 lane refund is my separate offline control, which reproduces the TEAM's private 1/1 control **[T]** in kind. I did not obtain the private bytes.
4. **Native cleanup provider [T].** It reports BLOCK on manual-only `update-coverage` REVIEW, with `sync-unconfigured` and `release-doc-version-missing` NOT_CHECKED ([BOUNDARY_CHECK.json](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/Submission12/BOUNDARY_CHECK.json)). This is a bounded source-only exception, not a provider PASS.
5. **Release gates [U].** These are all unmeasured: [BUILD_DEPLOYMENT.json](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/Submission12/FinalClosure/BUILD_DEPLOYMENT.json) records `newDeployment:false`, and [SERVED_READBACK.json](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/Submission12/FinalClosure/SERVED_READBACK.json) records `status:"UNKNOWN"`.
   - real Cloudflare cron and `waitUntil` semantics;
   - production D1;
   - secrets and bindings;
   - WAF, limiter and upstream behavior;
   - browser, provider and cookie behavior, including ERC-1271;
   - M1 production write authorization;
   - process-death and cross-isolate behavior;
   - deployed source identity.
6. **Public typecheck [R].** `tsc --noEmit` in the public checkout exits 2. The four errors are all missing modules for excluded frontend files (`households.ts`, `content-hash.ts`, `terrainField.ts`, `terrainBake.ts`). The TEAM typecheck exit 0 is private **[T]**. Its public replay is unavailable, and that is not a source defect.
7. **Windows [U].** I ran on Linux. Windows symlink/junction permission was not exercised, so it is neither PASS nor EPERM.

## Verdicts

- **SOURCE-CLOSURE: PASS (bounded).**
  - Both rows close at the exact pin under reviewer reproduction.
  - Same-evaluator baseline calibration reproduced 4 passes and 9 failures.
  - An independent offline control shows lane admission at 1→2 on the baseline and 1→1 at the pin.
  - No regression reproduced: 728/728, artifact checks 20/20.
- **RELEASE-READINESS: UNKNOWN.**
  - There was no deployment or readback, and no full frontend build.
  - The native provider reports BLOCK.
  - The production gates listed above are unmeasured.

  I chose UNKNOWN rather than BLOCKED because I have no evidence of a release defect, only no evidence either way.

---

## Evidence appendix

### Identity and integrity [R]
- `git rev-parse HEAD` = `2f21b74cf61fe8fed9e3700d082b2dab38904b33`; parent `35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a`. The private source pin `3a1ea7d…` is provenance only [T]. I did not access it.
- `sha256sum -c SHA256SUMS`: 315/315 OK.
- [manifests/submission12-published-source.json](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/manifests/submission12-published-source.json): 147/147 source hashes match. The manifest's own SHA-256 is `194c8f03…0c42`, which matches [CLOSURE_MATRIX.md](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/Submission12/FinalClosure/CLOSURE_MATRIX.md).
- Downloaded Audit11 SHA-256 `af016f6e…42cc` and Report11 `cc483912…7290` match [LATEST_AUDIT_IDENTITY.md](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/Submission12/FinalClosure/LATEST_AUDIT_IDENTITY.md).
- Checksums prove byte integrity, not behavior.

### Commands (Linux 6.8, Node v24.21.0, npm 11.19.0, run in `source/` of a fresh clone at the pin)

| Command | Exit | Result |
|---|---|---|
| `npm ci --ignore-scripts` | 0 | Locked install, 0 vulnerabilities reported; viem 2.56.9 |
| `node scripts/review-tests.mjs --check` | 0 | `{"node":"v24.21.0","viem":"2.56.9","testFiles":29}` |
| `node --test --test-reporter=tap tests/scheduled-audit11.test.mjs` | 0 | 13/13 pass; fail, cancelled, skipped, todo all 0 |
| `npm run test:review` (×4) | 0 each time | 728/728 each run; fail, cancelled, skipped, todo all 0; about 6 s per run |
| `node scripts/verify-artifact-closure.mjs` | 0 | `status:PASS`, 20/20, 0 skipped; real Linux file and directory symlinks; no EPERM |
| `SCHEDULED_AUDIT11_SOURCE=<git archive 35ace95>/source node --test … scheduled-audit11.test.mjs` | 1 | Baseline: 4 pass, 9 fail. All 9 are real assertion failures at "an invalid sample anywhere forbids every durable housekeeping mutation". Finite, cap, missing-schema and no-DB controls pass |
| Reviewer offline probe (scratch script; real `createWorker`, `wallet-harness`, migration-backed `node:sqlite`) on candidate and baseline | 0 / 0 | Candidate: all 9 invalid cases have probe (0, 30000), lane 1, sessions 1→1, signed in. Baseline: sample-1 Infinity gives sessions 1→0 and 401; sample-3 Infinity gives probe `[]` → (1, 30001), lane 2 |
| Reviewer request-path member probe (bootstrap under NaN, ±Inf) | 0 | profile_requests and history 1→1 in every case; status NaN 200, +Inf 401, −Inf 200 |
| `node node_modules/typescript/bin/tsc --noEmit` | 2 | Missing excluded frontend modules only; reported as unavailable |

**Shims and deviations.**
- For the baseline run only, `node_modules` in the scratch archive of `35ace95` was a symlink to the candidate's locked install. The lockfiles are identical.
- No crypto, Worker or SQLite substitution, no removed assertions, no inserted waits and no hidden skips. The supported runner cleared the `*_SOURCE` selectors. The baseline selector was used only for a direct `node --test` call.
- There were no failures other than those listed above.

### TEAM records (not reproduced by me unless stated) [T]
- From [TEST_RESULTS.json](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/Submission12/FinalClosure/TEST_RESULTS.json) and the [README](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/README.md):
  - I matched these publicly: targeted 13/13, supported 728/728, artifact 20/20, baseline 4 passes and 9 failures.
  - Private only: full suite 1778/1778, fresh private 728/728 + 20/20, typecheck exit 0.
- [REVIEWER_EVIDENCE.json](https://github.com/tungweb3/imd-ember-world-review/blob/2f21b74cf61fe8fed9e3700d082b2dab38904b33/Submission12/FinalClosure/REVIEWER_EVIDENCE.json): a private offline probe, 1/1 on the candidate and 1 failure on the baseline, lane 1→2. It is labelled "independent agents within TEAM, not external Swarm review".
- Public-commit privacy checks (316 text files, 0 private commit intersection, 0 unreachable objects) are TEAM records that I did not repeat. Raw private receipts are withheld.

### Historical claims [H]
- Audit11 (judged 2026-10-05 19:28 UTC) found 1 Low and 1 Info against `35ace95`. It noted that production reachability was not demonstrated, because `Date.now()` is ordinarily finite.
- Report11 gave a bounded source PASS for the six Audit10 issues. It is superseded on the scheduled path by Audit11.

### Unanswered questions [U]
- Whether Cloudflare's cron runtime can ever supply a non-finite `Date.now()`. A11-L1 and A11-I1 remain synthetic robustness findings.
- Production D1 behavior of `Infinity` and `NaN` bindings compared with `node:sqlite`.
- Windows link semantics.
- The identity of the deployed build, and every release gate above.
