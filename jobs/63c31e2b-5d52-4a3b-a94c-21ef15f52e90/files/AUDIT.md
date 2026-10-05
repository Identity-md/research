# Audit report

> IMD Ember World - Audit11 narrow source closure of Audit10 / Report10
>
> QUESTION
> Does this exact candidate close all six open Audit10/Report10 source issues (1 Low + 5 Info/test-reliability issues), including the same-invariant neighbor cases, without reopening prior Auth, ownership, artifact or Member M1 boundaries? Seek any-severity defects within these mechanisms. Do not assume PASS from local test counts.
>
> PERIOD AND SOURCES
> Review the latest Audit10/Report10 findings finalized 2026-10-05 and the remediation frozen 2026-10-06 Asia/Taipei. Use the submitted immutable pin and its recorded freeze/measurement times; historical namespaces are context, not current evidence.
> Candidate: https://github.com/tungweb3/imd-ember-world-review/tree/35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a
> Audit10: https://github.com/Identity-md/research/blob/d2bbc2713f0c15d7542bc8afa09bafc4bf12ef12/jobs/e817a62e-1b9f-4469-90d7-7a761579af81/files/AUDIT.md
> Report10: https://github.com/Identity-md/research/blob/7701ce0c6d860ba50616629d0a3a60e644135fe4/jobs/a3ec7191-f1ab-400e-bb5f-dfa858c6da65/files/artifacts/report.md
> Read README, Submission11/REVIEW_INPUTS.md, then Submission11/FinalClosure/{CLOSURE_MATRIX.md,TEST_RESULTS.json,ARTIFACT_CLOSURE.json,REVIEWER_EVIDENCE.json,LATEST_AUDIT_IDENTITY.md,FINAL_AUDIT_MAPPING.md}. Verify manifests/submission11-published-source.json and SHA256SUMS. Inspect the actual changed source, not just descriptions.
>
> SCOPE
> Unofficial TypeScript Cloudflare Worker / React SIWE World and Member M1; no Solidity. M1 writes persistent public profiles, so World is not wholly read-only. Review only the six mechanisms below and directly affected prior invariants. Exclude feature development, 3D/scene/media/avatar/selfie/full UI, Genesis/Mint, Ember Coin, Fren Pet, private databases/backups/credentials. Missing frontend inputs are unavailable build evidence, not a successful full-site build.
> Use local synthetic fixtures and locked real viem, actual AuthClient/Worker and migration-backed SQLite. Public repository reads and locked dependency downloads are allowed. No production endpoints or writes, real wallets/signatures, asset actions, approvals, claims, bridges, payment, deployment or new jobs. Do not request private credentials or databases.
>
> SIX CLOSURE ROWS
> 1. A10-L1 (Low): passive provider discovery must not replace stop/context-switch nonce cleanup with lock-reconcile. Reproduce held B verify, first nonce logout failure before Worker, stop/restart, discovery C, then late verify; also replacement cookie A and same-life genuine switch. Keep old-lifetime nonce responsibility and UI fencing; no expectedAddress=A logout from passive first observation. Preserve true current C-to-D cleanup and lock-to-stop promotion. Neighbor controls: repeated transport/503 uncertainty retains the owner without an immediate retry loop; later existing lifecycle trigger retries the same nonce; 2xx revokes or post-fence nonce 409 conclusively refuses, preserving foreign A. A fresh current-life canonical PRESENT may coexist with pending cleanup; old verify callbacks cannot install it. Separate database-row safety from delayed clear-cookie effects and preserve same-address newer sessions.
> 2. A10-I1 (Info): after awaited owner sightings, sample one live ranking clock before the 256-candidate cut/keepIndex. With 257 registered seats, seats 1..256 expire during the await while 257 remains eligible: 257 must be retained, eligible=1, size=s, still partial where required. Preserve index read_at and proof producer timestamps, ID tie-breaks, cap, RPC/index/budget limits.
> 3. A10-I2 (Info): public assets status uses a live display clock after all relevant awaited enrichment, including later character I/O. Test delays 0/1/2/5000ms around inclusive 24h boundaries; initial and subsequent responses agree. Preserve fetchedAt/presence producer data. No added index, budget or RPC requests. Public display hints are not verified ownership authority.
> 4. A10-I3 (Info): persisted nested/quoted/bare '/api/auth/session private.log', '/api/auth/session dir/file.ts' and '/api/auth/session (private)/x.ts' must be masked as local paths. Preserve complete allowed route/query/subroute tokens, real network URLs, relative test identifiers and nonce/action/event/replay structure. Read back persisted bytes; do not rely solely on an in-memory sanitizer result. Recheck prior replay writer containment and real symlink/junction controls.
> 5. R10-N1 (Info): NaN/Infinity/-Infinity must fail closed before lane/probe persistence, including clocks becoming invalid after awaits. Inspect actual index_lanes and index_lane_probes rows, not only HTTP status. No nonfinite durable values or stuck lane. An existing finite probe keeps its bounded 30-second backoff, without refund or timestamp refresh; finite requests recover at +10m/+60m. Include finite/rollback controls, no extra upstream/budget calls and no proof/producer timestamp renewal.
> 6. R10-N2 (Info/test reliability): the genuine B-to-A LOW2 regression waits for semantic logout completion and notification, not a fixed flush/sleep. Preserve all original response, SQLite, prompt, logout and broadcast assertions. Verify the recorded 50 targeted and 10 full stability runs; independently repeat where feasible and disclose exact repeats/unavailable checks. Do not replace failed tests or change the reference oracle to fit candidate behavior.
>
> VALIDATION
> Fresh exact public checkout, Node24.x; in source/:
> npm ci --ignore-scripts
> node scripts/review-tests.mjs --check
> npm run test:review
> node scripts/verify-artifact-closure.mjs
> Run all supported files with current dynamic totals. No private-source selector, shim, global module substitution, hidden skipped failure or copied node_modules. Distinguish real assertion failures from Windows symlink EPERM or setup failures; neither is an assertion PASS. Check causal same-evaluator baseline failures, positive regressions, reverse controls and unchanged original tests. Local TEAM author/reviewer checks are not external Swarm verdicts. Record commands, exits, totals, failures, cancellation/skips/todo, retries and reasons.
>
> LENGTH AND FORMAT
> Return Markdown: short summary, six-row closure matrix (ID/severity, exact-pin location, reproduction, measured fix/control result, CLOSED/PARTIAL/OPEN/UNKNOWN with rationale), then a concise evidence appendix. Cite immutable source/line links beside claims. Record key auth rows/nonces and prompt/connect/challenge/verify/logout/hint/broadcast/index/budget/RPC counts where relevant; no tokens or private secrets. Distinguish independent reproduction, TEAM evidence, historical results, inference and unavailable checks.
> Give separate SOURCE-CLOSURE and RELEASE-READINESS verdicts: PASS/BLOCKED/UNKNOWN. Source closure concerns this bounded candidate only; release readiness remains independently unmeasured. Offline tests do not establish production Cloudflare/browser/provider/cookie/ERC-1271/M1/D1/WAF/limiter/upstream/process-death/cross-isolate behavior or deployed source identity. Completed/accepted, passing counts and Low/Info labels are not certification, endorsement, zero vulnerabilities or fund-safety proof.

| | |
|---|---|
| Repository | https://github.com/tungweb3/imd-ember-world-review.git |
| Commit | `35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a` |
| Job | `63c31e2b-5d52-4a3b-a94c-21ef15f52e90` |
| Judged | 2026-10-05 19:28 UTC |
| Findings | 1 low · 1 info |

Four agents audited the code as it is at `35ace95`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: R10-N1 neighbor: nonfinite scheduled clock sample reaches presence housekeeping and deletes every live session and challenge

`source/server/presence.ts:59`

```
  const housekeeping=[db.prepare(PRUNE_CHALLENGES).bind(now-DAY_MS,now-UNUSED_CHALLENGE_KEEP_MS),db.prepare(PRUNE_SESSIONS).bind(now-DAY_MS)];
```

R10-N1 requires NaN/Infinity/-Infinity temporal authority to fail closed before durable persistence, and the candidate adds that guard only on the request lane path (server/auth.ts lane closure and reserveIndexProbe). The Worker scheduled entry point (source/worker/app.ts:150-158) samples now() three times with no finite check and passes the first sample straight into recordPresence(). recordPresence binds now-DAY_MS into PRUNE_SESSIONS ('DELETE FROM sessions WHERE expires_at<?1') and PRUNE_CHALLENGES without validating now. SQLite evaluates every finite expires_at < Infinity as true, so a single Infinity sample deletes every live session and every login challenge, and writes a non-finite updated_at (stored as NULL by node:sqlite) into seat_presence. A signed-in browser's cookie then points at a deleted row and GET /api/auth/session answers signedIn:false. This is the same invalid-clock class as the R10-N1 request-side fix and the probe-prune neighbor, but with an Auth-boundary effect (mass session revocation) instead of a 30-second backoff refund. Production reachability is not demonstrated: Date.now() ordinarily returns a finite value and no remote clock control exists; this is a synthetic robustness defect against the stated fail-closed requirement. NaN happens to fail closed because the comparisons are false and the presence batch rejects (the waitUntil promise for recordPresence has no catch); -Infinity deletes nothing but still writes a NULL updated_at. The second unguarded sample has the same shape: pruneMemberRecords(db,Infinity) (server/member.ts:42-50, called at worker/app.ts:153) deleted one unexpired profile_requests row and one unexpired profile_history row (expires_at t+1d and t+30d) in a direct helper run, while t, NaN and -Infinity deleted 0 (M1 boundary, bounded by MEMBER_CLEANUP_MAX_ROWS per run). Fix: reject non-finite now at the scheduled entry (one guard before all three waitUntil calls) or at the top of recordPresence/pruneMemberRecords/pruneIndexProbes, logging a fixed 'unavailable' status, and add a scheduled-path regression asserting sessions/login_challenges/seat_presence rows are byte-identical after an Infinity/NaN/-Infinity cron sample. Keep ordinary finite expiry pruning unchanged.

**Reproduction**

Independent reproduction at exact pin 35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a, Linux, Node v24.21.0, npm ci --ignore-scripts with locked viem 2.56.9, real createWorker and migration-backed node:sqlite via tests/wallet-harness.mjs; no production endpoints or real wallets. From source/ run with node --input-type=module (or save as a .mjs file in source/):

import {setup,newAccount,fakeImd,fakeChain} from './tests/wallet-harness.mjs';
import {createWorker} from './worker/app.ts';
const t=1790596800000;
for(const first of [t+1,Infinity,NaN,-Infinity]){
  const account=newAccount(),A=account.address.toLowerCase(),owners=[];owners[7]=A;
  const w=setup({chain:fakeChain({owners:{7:A}}),imd:fakeImd({seats:{7:'707'},owners,online:[7]})});w.clock.set(t);
  const b=w.browser();const v=(await b.signIn(account)).verify.status;
  const rows=()=>({sessions:w.db.raw.prepare('SELECT count(*) n FROM sessions').get().n,challenges:w.db.raw.prepare('SELECT count(*) n FROM login_challenges').get().n,presence:w.db.raw.prepare('SELECT token_id,last_online_at,updated_at FROM seat_presence').all()});
  const before=rows();let samples=0;
  const sched=createWorker(w.gateway,w.chain.fetcher,()=>{samples++;return samples===1?first:t+1;},[]);
  const pending=[];const saved=console.log;console.log=()=>{};
  try{await sched.scheduled({scheduledTime:t+1,cron:'*/15 * * * *'},w.env,{waitUntil:p=>pending.push(p)});await Promise.allSettled(pending);}finally{console.log=saved;}
  const after=rows();const s=await b.get('/api/auth/session');
  console.log(JSON.stringify({first:String(first),verify:v,before,after,sessionAfter:s.status,body:await s.json()}));
}

Only the first now() sample (the one recordPresence receives) is replaced; the member and probe cleanups receive finite t+1. Measured output (exit 0):
- first=t+1 (finite control): verify 200; before {sessions:1,challenges:1}; after {sessions:1,challenges:1, presence:[{token_id:7,last_online_at:t,updated_at:t+1}]}; /api/auth/session 200 signedIn:true.
- first=Infinity: verify 200; before {sessions:1,challenges:1}; after {sessions:0,challenges:0, presence:[{token_id:7,last_online_at:t,updated_at:null}]}; /api/auth/session 200 {signedIn:false}. The cron log still reports presence {written:1,...}.
- first=NaN: rows unchanged, no presence row written, no presence log line (the recordPresence promise rejected inside waitUntil).
- first=-Infinity: sessions/challenges unchanged; presence row written with updated_at:null.
Expected under R10-N1: an invalid scheduled clock sample must not delete or write any durable row; the live session must remain readable (signedIn:true) and seat_presence.updated_at must stay finite. Actual: Infinity revokes all sessions and challenges and both infinities persist a non-finite updated_at. Same-evaluator finite control passes, so this is a real assertion-level difference, not a setup failure.

### 2. Info: R10-N1 neighbor: nonfinite scheduled prune refunds an unexpired 30-second index-probe backoff

`source/server/auth.ts:284`

```
  try{return {status:'cleaned',deleted:(await db.prepare(INDEX_PROBE_PRUNE).bind(now,cap).run()).meta.changes??0};}
```

Merged from three identical specialist findings (audit_math, audit_permissions, audit_economics); each was independently re-executed here and reproduces. The candidate's R10-N1 fix rejects non-finite clock samples in the request lane (server/auth.ts lane closure sample() and reserveIndexProbe's Number.isFinite(now) guard), but the other writer of index_lane_probes, pruneIndexProbes(), validates only the deletion limit and binds the unchecked now into INDEX_PROBE_PRUNE ('... WHERE expires_at<=?1 ...'). The real Worker scheduled handler calls it with an unguarded now() at source/worker/app.ts:157. With now=Infinity every finite expires_at satisfies the predicate, so a still-live finite probe is deleted (up to the 200-row cap), refunding the mandatory 30-second backoff that the request path promised. The next finite request then calls the local 'chain:index:lane' limiter again and replaces the original probed_at/expires_at before the original deadline. This violates the scoped R10-N1 invariant that an existing finite probe keeps its bounded backoff without refund or timestamp refresh. The request-side admission defect from Report10 is fixed; this is a surviving same-table temporal neighbor and the unguarded helper is also present in the prior public source c2f21a9 (unclosed neighbor, not a new regression). No production clock control or ownership bypass is demonstrated; Date.now() is ordinarily finite. Fix: return early (no DELETE) when !Number.isFinite(now) in pruneIndexProbes, keep the existing 0-200 cap and finite expiry pruning, and add a scheduled-path regression asserting the live probe row and the subsequent lane-limiter count are unchanged after Infinity/NaN/-Infinity cron samples.

**Reproduction**

Independent reproduction at exact pin 35ace952824ebf711fd9fa6cb7ea1cc83b75cd6a, Linux, Node v24.21.0, locked viem 2.56.9, real createWorker and migration-backed node:sqlite; no production endpoints or real wallets. (1) Minimal helper-level assertion, run from source/ with node --input-type=module: import assert from 'node:assert/strict'; import {openD1} from './tests/d1-sqlite.mjs'; import {pruneIndexProbes} from './server/auth.ts'; const t=1790596800000; for(const now of [t+1,NaN,-Infinity,Infinity]){const db=openD1(); db.raw.prepare('INSERT INTO index_lane_probes(scope_key,net,sub,probed_at,expires_at) VALUES(?,?,NULL,?,?)').run('net:unknown|','net:unknown',t,t+30000); const r=await pruneIndexProbes(db,now); console.log(String(now),JSON.stringify(r),db.raw.prepare('SELECT count(*) n FROM index_lane_probes').get().n);} Measured: t+1 -> {cleaned,deleted:0} remaining 1; NaN -> deleted 0, remaining 1; -Infinity -> deleted 0, remaining 1; Infinity -> deleted 1, remaining 0. Asserting remaining===1 for Infinity fails with ERR_ASSERTION (actual 0, expected 1). (2) End-to-end through the real scheduled entry point: sign in a synthetic EOA A owning offline seat 7 (fakeChain owners {7:A}, fakeImd seats {7:'707'}, owners[7]=A, online []), insert seat_presence(7,A,t-ONLINE_WINDOW_MS-1,t-ONLINE_WINDOW_MS-1) at t=1790596800000, set env.CHAIN_LIMITER.limit to record keys and return {success:false}. GET /api/me/home -> 200 recheck:'limited'; work {index:0,rpc:1,budget:1,lane:1}; index_lanes []; index_lane_probes [{scope_key:'net:unknown|',probed_at:1790596800000,expires_at:1790596830000}]. Build createWorker(w.gateway,w.chain.fetcher,clock,[]) with clock returning t+1,t+1,THIRD for the handler's three samples, call scheduled({scheduledTime:t+1,cron:'*/15 * * * *'},w.env,{waitUntil:p=>pending.push(p)}) and await Promise.allSettled(pending). Then set the request clock to t+1 and GET /api/me/home again. Measured: THIRD=t+1, NaN, -Infinity: cron log index_probe_cleanup {cleaned,deleted:0}; probe row unchanged after cron and after the second request; lane-limiter calls total 1; second response 200 limited. THIRD=Infinity: cron log index_probe_cleanup {cleaned,deleted:1}; probe rows [] after cron; second request 200 limited re-inserts {probed_at:1790596800001,expires_at:1790596830001}; lane-limiter calls total 2 within 1 ms; index requests 0, budget calls 1, ownerOf RPC 1 across both requests, no admitted lane, session unrevoked. Expected: the original row retained at t/t+30000 and only 1 lane-limiter call before t+30000. All runs exit 0 with no setup/EPERM failures; the invariant check printed INVARIANT VIOLATED only for Infinity.

---

Judge's submission `5b89f643d041f9b8bf008bbcd3a227eb910941e149ae93ec99e69999871500e2`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
