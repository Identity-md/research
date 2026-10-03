# Audit report

> IMD Ember World - fifth offline audit of R4/AUD4 and Member M1 (World only)
>
> Unofficial project; NO Solidity. TypeScript Cloudflare Worker/React SIWE; M1 writes persistent public profiles, so World is not wholly read-only. Offline source/local synthetic tests only: no live requests, real wallets/signatures, transactions, production writes/deploy.
>
> PIN: https://github.com/tungweb3/imd-ember-world-review at 357668f37c75317f79ff2266795636597a707c04; actual parent 6e307dea76e763936fc4ac86e54c9f5d558f58c4. Published baseline: 6e307dea76e763936fc4ac86e54c9f5d558f58c4. Use immutable history, not branch head. Private repair 54410b2f8dece71bdb2fd999c94feea6454ecfcd; private history withheld, provenance is a team claim.
>
> Read README, R5/TEST_RESULTS.md, R5/BUILD_EVIDENCE.md; source/docs/security/AUD4_REMEDIATION.md, AUD4_MEMBER_POLICY.md, AUD4_DISCOVERY.md. Old root docs remain historical. Read R5/PRIOR_AUDIT_f3e7cfc7.md (job f3e7cfc7-0b43-473a-9c0f-6931cf278c56) and R5/PRIOR_REPORT_1dbe2282.md (job 1dbe2282-d61a-42a8-9823-2b24e48d29c1). Eight Audit findings plus Report-only M1-R2 are NINE unique fixes; M1-R1 overlaps Audit #5. M1-R2 MUST have a separate verdict.
>
> TEAM/LOCAL: private 1087/1087, tsc/frontend build pass. Fresh local Wrangler D1 final 0008: five accepted, sixth trigger refused, recheck five; not production concurrency proof. Public tests (run/pass/fail): no-stub 239/235/4; FIRST with-stub 419/414/5. Failures: withheld geometry/preview/history plus first-run presence timing; timing-only 1/1 rerun does not erase first failure. Public tsc: 16 diagnostics/exit 2; no public full frontend build. Focused R3/AUD3/ADV 83/83, N 42/42, Enter 3/3, Member+AUD4 including M1-R2 111/111. Public/private Worker identical 309594 bytes, SHA256 c7d7c0fbe49ce601a187bafdf7480c40d64ceda7bcfde64b9aea3f63f809811c. Public source 100 = 16 masked + 84 exact against 54410b2; 3D/textures/scenes/WorldApp/interiors/history withheld. No full UI/browser proof; stubs are fixtures.
>
> TEAM deployment: Worker e491cb71-60ec-4cfe-9db7-b88e52d78ce9 (100% traffic checked); deployed source 54410b2f8dece71bdb2fd999c94feea6454ecfcd; record R5/BUILD_EVIDENCE.md (record 20261003T174551Z-54410b2); production migration status 0001-0006+0008 applied; six schema SQL definitions read back/matched; no 0007 (R5/PRODUCTION_D1.md); live comparison five GETs 200; four static hashes/24 headers match; anonymous signedIn:false/no-store; no Set-Cookie. No live Audit verification; old acdbb2bd/ddb10e2 records do not prove this repair deployed.
>
> NINE REQUIRED RETESTS; seek new regressions:
> 1. R4-01/AUD4-01/Audit #1: display A/shared cookie B logout-all must 409 ACCOUNT_CONTEXT_CHANGED before revoking either. Reread without false all-device success; matching/absent/forged/expired cookies retain session authority. expectedAddress is consistency, not authority.
> 2. R4-02/AUD4-06/Audit #6: verify cookie committed, body lost/truncated/malformed. Session unknown; readback before another personal_sign. Failed read stays unknown; confirmed absence permits new flow. Test switch/teardown and nonce/flow cleanup versus newer installed session AND pending challenge. Neither may be destroyed. Count prompts/sessions; late browser Set-Cookie remains a limit.
> 3. R4-03/AUD4-02/Audit #2: only server EOA AND ECDSA permits persistent bootstrap/PUT/GET last_login writes. CONTRACT/ERC1271/unknown fail closed (write 403 CONTRACT_WRITE_NOT_ENABLED); login/existing reads without touch remain. Test arbitrary-accepting and legitimate smart-wallet sessions; temporary restriction has usability cost, not complete contract authority.
> 4. R4-04/AUD4-05/Audit #5+M1-R1: 0008 trigger atomically caps five recorded attempts/member/rolling minute. Test 6/12/20 natural/controlled races: success, reserved-name refusal, cooldown, stale/locked, no-op. Outcome/mutation roll back together; fallback refusal recording returns 429/503 on quota/storage failure. Same-ID/same-payload retry at full quota adds no record/version/history/cooldown; changed payload conflicts. New same-name no-op consumes one attempt, no mutation, guarded against parallel rename/moderation. Separate recorded attempts from all HTTP/early-invalid/IP costs.
> 5. R4-05/AUD4-04/Audit #4: expired refusal rows cleaned without later rename. Requests 1 day/history 180 days are deletion eligibility, not hard deadlines. Indexed cron 200/table, write prune 10/table. Preserve unexpired retries/current profile; test backlog, missing 0008/indexes/errors. Probe cron bounded independently of M1 readiness.
> 6. R4-06/Report M1-R2 ONLY: GET(v0) starts -> SAVE(v1) accepted -> old GET(v0) arrives: client/DB retain v1. Test GET2-before-GET1, late 401/error, GET(v2) before PUT(v1) reply, account switch. Sequence/generation/highest accepted version prevent regression. Separate mandatory verdict; stale UI is not DB rollback.
> 7. R4-07/AUD4-07/Audit #7: committed PUT, lost/invalid/endless body. Fetch+body 15s deadline; retry once exact original ID/body. Both unknown: retain per-wallet operation, saving=false, reread, allow only original retry. Test early 401/429/503 and logout/switch/return; one mutation/history/cooldown. Refusal before outcome lookup does not prove original failure.
> 8. R4-08/AUD4-08/Audit #8: server-calibrated cooldown refresh/re-enable at expiry; switch/teardown cancel timers. Browser clock cannot bypass server.
> 9. R4-09/AUD4-03/Audit #3/AUD3-02: four sessions x20 refusals over 80 /24s at colo A then buyer B: zero admitted rows/index calls from refusals; B discovers. Bounded READY -> atomic separate probe -> limiter -> fresh-clock atomic admission -> index. Probe 30s backoff (/24,/64 one;/48 two), global 60/6s and 61-admission races; prune 2 opportunistic/200 cron. Test missing schema/index fail-closed, old released rows, slow/uncertain replies and refusal-counted/free models. Probes do not pollute admitted cap; no global probe-storage ceiling. Retain 10-versus-9 /24 local availability, shared networks, influx/cost/backlog.
>
> Recheck R3-R1/AUD3-01..09, N/ADV, Enter/Home; stored SIWE equality, nonce/session/cookies/logout. House authority remains session address plus Ethereum mainnet ownerOf/eligibility, never names/roster/candidates/publicMemberId. Only eth_accounts, eth_requestAccounts, exact server-SIWE personal_sign; verify no transactions, approvals, Permit/Permit2, typed data, delegated permissions, session keys or wallet batches. Out of scope: Genesis Mint, Solidity, Coin E1/0007, check-in/rewards/economy, withheld content.
>
> OUTPUT: nine-row verdict matrix, M1-R1 overlap and separate M1-R2. Classify fixed locally/partly/open/unknown; each finding severity, blocking, pinned file:line, prior ID, preconditions, player impact, reproduction/argument. Show event/timestamp order, DB rows/version/history/outcomes, client state, prompts and created/live/revoked sessions/cookie effects (N/A with reason). Record tests/failures/skips; separate measured fact, inference, team claim and unavailable checks. Preserve AUD3-05 partly, AUD3-09 review-limit, missing provider events, late shared-cookie responses, ERC1271 login truth, phishing/same-origin EOA writes, production D1/bindings/WAF/limiter/upstream and full-browser limits. Completed/accepted or Low/Info findings are not certification, approval, zero vulnerabilities or fund-safety proof.

| | |
|---|---|
| Repository | https://github.com/tungweb3/imd-ember-world-review.git |
| Commit | `357668f37c75317f79ff2266795636597a707c04` |
| Job | `e137990d-8dbc-4153-ae11-cada783827ea` |
| Judged | 2026-10-03 19:00 UTC |
| Findings | 4 low |

Four agents audited the code as it is at `357668f`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Account/provider-switch cleanup revokes a newer shared-cookie session and invalidates its pending challenge

`source/src/world/auth.ts:427`

```
    if(other||wasFlow){this.hint.set(null);this.sendLogout(ok=>{if(!ok){void this.restore();return;}this.loggedOut(g,ended);if(other)this.broadcast('signed-out');});}
```

R4-02 / AUD4-06 / prior Audit #6 remains partly fixed. accountChanged sends sendLogout without expectedNonce; providerChanged at line 217 does the same. During uncertain-verify readback the phase is still verifying, so a switch triggers plain logout. The real server's unbound branch (source/server/auth.ts:640-643) revokes the request's current cookie session, invalidates its current flow's pending challenges, and clears both cookies. Another tab can already have replaced both. This is request-time context confusion, distinct from late browser Set-Cookie responses. Player impact: the newer tab is logged out and loses its pending login; the abandoned original session remains live. Non-blocking Low for fund/house authority, but blocks closure of the required newer-session/newer-challenge preservation retest. Retain the active challenge nonce at client scope and use conditional abandoned-flow cleanup for both switches; preserve explicit logout behavior and reread on a context conflict. Merges audit_economics, audit_flow and audit_permissions reports of this mechanism. Independently reproduced offline at pin 357668f37c75317f79ff2266795636597a707c04 using the unchanged AuthClient/MemberClient, real session/logout/member handlers and migrations in in-memory SQLite. Node 22.11 required an in-memory adapter for numbered SQL parameters. Missing external crypto/ABI libraries were replaced by throwing import shims (address normalization only); challenge/signature/verify completion was a synthetic session fixture, not a cryptographic-verification test. No network, real signature, wallet or browser was used. Also reproduced outside an in-flight verify: a stale A display plus a failed session reread and account switch can revoke B. When no flow nonce is available, add an appropriate authenticated-session consistency assertion for automatic cleanup (expectedAddress can detect a different displayed wallet but is never authority).

**Reproduction**

At T=1790596800000 use A=0x1111111111111111111111111111111111111111 and B=0x2222222222222222222222222222222222222222. Start AuthClient, return signedIn:false from the real session route; issue exact-format SIWE fixture; count one personal_sign call; seed committed A session and install its cookie, but return HTTP 200 body '{' for verify. Hold the ensuing real GET /api/auth/session response. While held, install fixture session B in the same Browser jar, then seed B's new pending challenge and flow cookie. Emit accountsChanged([B]) or invoke the registered provider-change callback. Wait for logout before releasing the held GET. Measured outgoing logout body '{}'; A.revoked_at=NULL, B.revoked_at=T; pending B challenge.invalidated_at=T; both cookie names removed. Created/live/revoked sessions=2/1/1; client phase=idle, session=null, sessionKnown=false. Original flow prompts=1; B setup directly seeds its session (no additional prompt measured). Both switch variants reproduce. Pending-only controls (no B session, only B challenge) revoke A as intended but also invalidate B's challenge and clear its flow cookie: 1/0/1 sessions. Expected: nonce-bound cleanup must preserve the newer session/challenge and cookies (409 for a newer session; revoke only A for pending-only). M1 profiles/version/history/outcomes N/A: no member route is called. Additional measured stale-display control: complete synthetic A login; replace the shared cookie with B; return 429 on restore so the client still displays A with sessionKnown=false; emit accountsChanged([C]) where C=0x3333333333333333333333333333333333333333. The automatic logout again sends {}, revokes B, and leaves A live. No late cookie response is needed.

### 2. Low: Teardown during uncertain-verify reconciliation leaves the abandoned session live

`source/src/world/auth.ts:376`

```
    if(g!==this.gen)return;
```

R4-02 / AUD4-06 / prior Audit #6 remains partly fixed. Teardown increments gen while reconcileVerify awaits restore; the post-await generation check returns without nonce-bound revokeAbandoned. The stale read is discarded and signIn's finally releases its unsettled hold, so the client silently abandons a valid cookie-backed session. That EOA session retains persistent M1 write capability until revocation/expiry. Non-blocking Low for fund/house authority, but the required teardown cleanup retest cannot be closed. Carry the verified nonce through this cancellation boundary and conditionally clean up the abandoned session, preserving newer sessions and challenges. Merges audit_economics and audit_flow teardown findings. Independently reproduced offline at pin 357668f37c75317f79ff2266795636597a707c04 using the unchanged AuthClient/MemberClient, real session/logout/member handlers and migrations in in-memory SQLite. Node 22.11 required an in-memory adapter for numbered SQL parameters. Missing external crypto/ABI libraries were replaced by throwing import shims (address normalization only); challenge/signature/verify completion was a synthetic session fixture, not a cryptographic-verification test. No network, real signature, wallet or browser was used.

**Reproduction**

At T=1790596800000 start AuthClient for synthetic A with no cookie. Initial real session GET returns signedIn:false. After one counted personal_sign call, fixture verify completion creates A's session (expires_at=1791201600000) and installs its cookie; substitute HTTP 200 malformed body '{'. Hold the resulting real GET /api/auth/session after the handler generated signedIn:true. At the gate phase=verifying, sessionKnown=false, session=null, created/live/revoked=1/1/0. Invoke the stop function returned by start(), release the GET, await signIn. Measured route order: session -> challenge -> verify -> session, zero logout requests. Client ends idle/unknown/null; created/live/revoked remains 1/1/0 and session cookie remains. Direct real GET session reports signedIn:true. Expected: cleanup conditional on A's nonce revokes the matching abandoned session and clears its cookie, or an explicit accepted session replaces abandonment. No newer flow is needed to reproduce. M1 profile/version/history/outcomes N/A because no member route runs; no extra prompt occurs.

### 3. Low: Invalid session readback is treated as confirmed absence and permits another signature

`source/src/world/auth.ts:238`

```
      this.homeGen++;this.set({session:null,home:null,restored:true,sessionKnown:true,expired,ended:expired?'expired':held?'revoked':this.s.ended,checking:false});
```

R4-02 / AUD4-06 / prior Audit #6, CORR-02 remains partly fixed. readSession tests a positive shape but treats every other parsed non-null payload as confirmed sign-out. An invalid recovery response therefore sets sessionKnown=true with session=null despite an installed live cookie. The next click skips readback and requests another personal_sign, creating a second session while the original stays live. Requires malformed recovery response data in addition to uncertain verify; no production occurrence or authentication bypass is claimed. Non-blocking Low, but violates the mandatory failed-read-stays-unknown condition. Validate the two response variants strictly: absence only for signedIn===false; positive only for signedIn===true, valid address and finite valid expiry. All other schemas must leave sessionKnown=false. Merges audit_math and audit_flow schema findings. Independently reproduced offline at pin 357668f37c75317f79ff2266795636597a707c04 using the unchanged AuthClient/MemberClient, real session/logout/member handlers and migrations in in-memory SQLite. Node 22.11 required an in-memory adapter for numbered SQL parameters. Missing external crypto/ABI libraries were replaced by throwing import shims (address normalization only); challenge/signature/verify completion was a synthetic session fixture, not a cryptographic-verification test. No network, real signature, wallet or browser was used.

**Reproduction**

Freeze T=1790596800000. Start AuthClient with the real initial session GET returning signedIn:false. Count personal_sign; simulate committed verify by seeding one live EOA session and applying its Set-Cookie, then return HTTP 200 body '{'. Replace the following recovery GET's real signedIn:true response with HTTP 200 {}. Independently repeat with [] and {signedIn:true}. For all three, measured client session=null/sessionKnown=true with created/live/revoked=1/1/0 and prompts=1. Restore normal responses and call signIn again. Route order is session, challenge, verify, session, challenge, verify, home; no session read precedes the second signature. Prompts=2; created/live/revoked=2/2/0; second cookie replaces the first, leaving its session live. Expected invalid schema leaves unknown; next click reads the existing cookie and reuses it with one prompt/session. Profile/version/history/outcomes N/A: no M1 route is invoked.

### 4. Low: A backwards browser-clock correction extends the rename cooldown past server expiry

`source/src/world/member.ts:86`

```
  private serverNow(){return this.timeBase?this.timeBase.server+Math.max(0,this.now()-this.timeBase.local):this.now();}
```

R4-08 / AUD4-08 / prior Audit #8 is partly fixed. serverNow measures elapsed time with the wall clock Date.now and clamps negative deltas to zero. armCooldown's callback at line 96 rearms from that frozen estimate instead of reconciling with the server. A backwards clock step keeps the rename UI disabled after the real server deadline. Low, non-blocking client availability defect; it neither bypasses server cooldown nor changes profile/session authority. Use a monotonic elapsed clock anchored to serverTime or reconcile with the server at timer expiry. A 24-hour backward step can extend disabling by approximately 24 hours (inference from the timer arithmetic); the measured probe establishes the first missed expiry and rearm. Independently reproduced offline at pin 357668f37c75317f79ff2266795636597a707c04 using the unchanged AuthClient/MemberClient, real session/logout/member handlers and migrations in in-memory SQLite. Node 22.11 required an in-memory adapter for numbered SQL parameters. Missing external crypto/ABI libraries were replaced by throwing import shims (address normalization only); challenge/signature/verify completion was a synthetic session fixture, not a cryptographic-verification test. No network, real signature, wallet or browser was used.

**Reproduction**

At T=1790596800000 seed a synthetic EOA session, call real bootstrap and PUT ClockCat: profile version=1, history=1, profile_requests=1, deadline D=1791201600000. At D-1000 seed a fresh session and load real MemberClient with local clock L=D-1000; serverTime=D-1000, cooling=true, one GET. Move browser wall clock back 86400000ms; independently advance timer time and server time 1000ms. Fire the scheduled 1000ms callback. Measured serverNow=D-1000 (negative local delta clamped to zero), cooling=true, another 1000ms timer, GET count still 1. A direct real member GET at server D returns nextNameChangeAt=null. Expected deadline refresh and re-enabled rename. DB remains ClockCat/version1/history1/outcome1. The clock/timer operation creates/revokes zero sessions and has no Set-Cookie or wallet prompt; setup created two fixture sessions, first expired by D, so created/live/revoked=2/1/0. A reload recovers.

---

Judge's submission `b45aa8371d2248415df083f8be3ca4fb4a8c4522211e28f7d1b0f13627057c07`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
