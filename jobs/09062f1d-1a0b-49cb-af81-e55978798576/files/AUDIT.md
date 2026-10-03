# Audit report

> IMD Ember World: targeted independent review of fifth-Audit four Low repairs.
>
> SUBJECT: unofficial TypeScript Cloudflare Worker/React World/Auth/Member M1. NO Solidity: inspect TypeScript/SQL/lifecycle, not invented contracts. If unsupported by the Audit tool, report unsupported/unknown scope. M1 persists public profiles; World is not wholly read-only.
>
> PIN: https://github.com/tungweb3/imd-ember-world-review/tree/445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703; parent 357668f37c75317f79ff2266795636597a707c04. Use immutable commit. Full local source 1cc61b68b2dc14af83bf5178c9fe057452ba9b46, parent 54410b2f8dece71bdb2fd999c94feea6454ecfcd. Private tree/history and 3D/textures/scenes/WorldApp/interior assets withheld. Check public fingerprints/masks; private provenance/full-suite counts are team evidence.
>
> Read R6/PRIOR_REVIEWS.md: fixed hashes/official sources for fifth Audit e137990d-8dbc-4153-ae11-cada783827ea and Report 0860e448-e960-43af-9a1c-5eed9019ef04 at parent pin. Acquire originals via those sources; four Audit Low need independent closure despite Report aggregate. Read README; R6/TEST_RESULTS.md, R6/BUILD_EVIDENCE.md, R6/PRODUCTION_DEPLOYMENT.json, R6/LIVE_MATCH.json; source/docs/security/R5_LOW_REMEDIATION.md and its sibling AUD4_REMEDIATION.md, AUD4_MEMBER_POLICY.md, AUD4_DISCOVERY.md. Old R4/R5 records are historical.
>
> TEAM EVIDENCE: 96 new cases (Auth 49, authority 36, cooldown 11); private and formal deploy gates each 1183/1183, zero skipped, tsc/Vite pass. Earlier dry-run exit 1: sandbox Wrangler path refusal after passed gates; isolated compiler retry exit 0, no upload. Preserve both. Parent 54410b2 fails four main Auth probes and backward-clock Member probe. Real Worker/routes/migrations + node:sqlite; generated EOA keys sign synthetic SIWE. Public subset/fixtures are separate from private counts/UI proof.
>
> PUBLIC: read R6/PUBLIC_SOURCE_VALIDATION.json and R6/TEST_RESULTS.md. Seven no-scene-stub files: 212/212 (96 new + 116 existing), not private 1183. Public tsc exit 2/16 diagnostics; full frontend withheld/unbuilt. First Worker compile denied; deeper layout differed 399B/133 labels; same-depth raw rebuild matches deployed 314447B/SHA. Empty ASSETS fixture, no normalization; arbitrary checkout/npm-ci layouts may differ.
>
> TEAM DEPLOYMENT: source 1cc61b68b2dc14af83bf5178c9fe057452ba9b46; record 20261003T214856Z-1cc61b6; Worker 5022cd62-6f1f-444c-af94-3b68ec359b94, 100% checked; 314447 bytes, SHA256 3977c6db6cbff23e9f6aec87092a236c603eac8bf64a7ce0c825d400dd1ad7dd. Five GETs UTC 2026-10-03T21:51:47.506Z-21:52:11.967Z: 5/5 200, four static hashes/24 headers match, session signedIn:false/no-store/no cookies. D1 pre/post metadata same: 0001-0006+0008, no new migration. Byte/GET comparison is partial, not repaired-flow/concurrency/wallet/UI proof; old R5 deployment is historical.
>
> METHOD: offline pinned source/local synthetic tests. Optional <=5 anonymous GETs, >=5s apart: https://imdember.com/, record-listed index JS, InteriorView JS, CSS, /api/auth/session. No cookies/credentials; record UTC/status/hash/headers; stop on denial, no bypass. No live login/signature/POST/PUT, transactions, scan/fuzz/flood, D1 changes or deploy. Local synthetic POST/PUT allowed.
>
> REQUIRED FOUR-LOW RETESTS, each with original counterexample and before/after/control:
> LOW-1 (R4-02/AUD4-06): A verify committed but recovery uncertain; shared jar now holds B/newer A plus pending flow. Account/provider switch must preserve them. Automatic cleanup uses retained nonce, otherwise displayed expectedAddress; no assertion means no automatic logout. Test stale A/failed read/switch C, pending-only replacement, pruned original and delayed same-address/expiry session. Session revocation needs token+nonce; address fallback needs live matching cookie and derives original flow. Pending-only needs NO token + original flow cookie + exact pending/unexpired nonce; any token forbids fallback. Missing/forged/dead/mismatch changes no rows/cookies; both assertions 400. Explicit /logout {} retains current-cookie semantics.
> LOW-2 (R4-02/AUD4-06): teardown during uncertain recovery must execute conditional cleanup while JS can run. Test failed verify/read, UNKNOWN idle/repeated reads, switches, stop/restart and late body/204. Old lifetime cannot update new UI/channel/hint/timer or rearm expiry. Accepted PRESENT clears responsibility: normal stop must not revoke it; ABSENT permits one new flow. Preserve newer session/pending challenge without cross-token revocation.
> LOW-3 (R4-02/AUD4-06/CORR-02): confirm only signedIn===false (optional boolean expired), or signedIn===true + valid address + positive safe-integer expiresAt. Missing/null/array/wrong type/bad address/expiry/NaN/infinity/truncated JSON and 429/503/network/timeout rejection stay UNKNOWN. Next click GETs first; one prompt/session while unknown. PRESENT restores without prompt; ABSENT permits one flow. Synthetic timeout rejection is not an auth deadline.
> LOW-4 (R4-08/AUD4-08): serverTime + monotonic performance.now() replaces Date.now(). Independent clocks: backward/forward wall jumps, early/late callbacks. Deadline GETs profile; only valid server confirmation unlocks. Failure stays cooling, positive 60s retry. Stop/switch/stale callback/response cannot affect new account. Simulated throttling is not real browser/OS suspension proof.
>
> R5-01..09 MATRIX (not nine findings): 01 account-switch preservation; 02 provider-switch session/challenge; 03 teardown cleanup; 04 malformed UNKNOWN; 05 invalid positive schema UNKNOWN; 06 GET before personal_sign; 07 no duplicate session/prompt; 08 backward clock; 09 timer server reconcile. Map Low/code/test file:line/outcome/gaps/verdict; separate four-Low closure matrix.
>
> REGRESSIONS: R4-01 display A/cookie B logout-all stays 409 before revocation; expectedAddress is assertion, cookie authority. Matching/absent/forged/expired cases must avoid false all-device success. R3-R1/AUD3/N/ADV/Enter/Home; M1-R2 old GET/new PUT version; atomic five-attempt quota, no-op/idempotency, bounded retention/probe cleanup, uncertain-save timeout/retry. Stored SIWE equality; house authority = session address + Ethereum mainnet ownerOf/eligibility, never names/roster/publicMemberId. Only eth_accounts, eth_requestAccounts, exact server-SIWE personal_sign. No Mint/Solidity/E1/0007/rewards/transactions/approval/Permit/typed-data/batching/delegation.
>
> KEEP LIMITS: R4-03 smart-wallet write policy partly; R4-09 availability partly; AUD3-05 partly; AUD3-09 review-limit. No A token after B replaces it means nonce cannot revoke A; A may live until authorized logout/expiry. Address-only fallback cannot distinguish same-wallet renewal. Already emitted old Set-Cookie clear may arrive after a new cookie; new session row is not revoked, readback withdraws stale owner. Cleanup is best effort in running JS, not guaranteed after termination/offline. Auth fetch still has no new bounded deadline. Production D1/bindings/WAF/limiter/upstream, real wallet/browser and withheld content are unknown unless actually checked.
>
> OUTPUT: independent four-Low verdict, R5 matrix, regression gaps: fixed locally/partly/open/unknown. Each issue: severity/blocking/prior ID, pinned file:line, preconditions/impact, reproduction/argument, event/time order, prompts/cookies, created/live/revoked sessions, pending/used/invalidated challenges, UI/channel/timers (explain N/A). Separate reviewer measurements, team logs/claims, inference, unavailable checks; record commands/failures/skips/shims. Seek any-severity regressions, not a no-Critical guarantee. Tests, Low labels or Completed/accepted do not certify approval/fund safety.

| | |
|---|---|
| Repository | https://github.com/tungweb3/imd-ember-world-review.git |
| Commit | `445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703` |
| Job | `09062f1d-1a0b-49cb-af81-e55978798576` |
| Judged | 2026-10-03 23:32 UTC |
| Findings | 4 low · 2 info |

Four agents audited the code as it is at `445747d`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: LOW-2 regression (new in R6): late house read after an accepted PRESENT recovery revokes the accepted session with the retained nonce

`source/src/world/auth.ts:419`

```
    if(g!==this.gen||life!==this.life){this.revokeAbandoned(g,life,nonce);return;}
```

Prior IDs: fifth-Audit LOW-2 / R4-02 / AUD4-06. Non-blocking for funds or house authority; blocks full LOW-2 closure. Merged from three specialists (economics #1, permissions #1, math #1), all on this line.

Mechanism: reconcileVerify runs after a committed verify whose 2xx body was unreadable. Its restore() -> readSession() accepts a valid PRESENT answer: line 263 releases this.flow (the retained cleanup responsibility), line 267 installs the session/hint/expiry timer, then line 268 awaits refreshHome. If the page's start() teardown runs while that /api/me/home response is still pending, teardown correctly finds no retained flow and sends nothing. When the house response settles, this line sees life/gen changed and unconditionally calls revokeAbandoned with the nonce it still holds in its closure. The browser still has the matching live cookie, so server logout() (token_hash + nonce match) returns 204, sets revoked_at and clears the session cookie. The remediation doc (R5_LOW_REMEDIATION.md row LOW-2) states 'a valid accepted read releases retained responsibility, so normal stop does not revoke an accepted session'; this path violates that.

Preconditions: committed verify with a malformed/truncated 2xx body (the exact AUD4-06 case), a successful PRESENT re-read, then a navigation/unmount while the follow-up house read is in flight. No attacker or cross-token authority needed; the user is simply signed out of a session they had just been shown as signed in.

Event order (measured, synthetic clock 1790596800000): GET session=200 -> POST challenge=200 -> personal_sign (1 prompt) -> POST verify=200 (cookie installed, body replaced by '{') -> GET session=200 PRESENT -> GET /api/me/home?fresh=1 held -> stop() [0 logouts] -> house released -> POST /api/auth/logout {expectedNonce: original nonce}=204 with one session-cookie clear. Sessions created/live/revoked 1/1/0 before stop, 1/0/1 after; challenge used=1 pending=0 invalidated=0; a following real GET session returns signedIn:false. UI/channel/timer: after stop no UI write and no broadcast occurred (life guard works), expiry timer cleared by stop; the defect is the server-side revocation, not UI mutation.

Classification: new in this repair. The identical test passes on parent 357668f (both the corrupt-body case and the control), so the R6 change introduced it.

Fix: track whether this particular uncertain flow was already resolved (e.g. reconcileVerify checks that this.flow for its g was released by an accepted read, or readSession records 'resolved' for that flow) and only call revokeAbandoned after the read when the flow is still unresolved. Keep the pre-read branch at line 413 and keep cleanup for a verify that remains uncertain.

**Reproduction**

Scratch copy of the pinned source with `npm ci` (locked deps), real Worker/routes/migrations over node:sqlite, in-memory EOA signing the exact server SIWE. Test F1 in tests/reviewer-r6.test.mjs (run: `node --test tests/reviewer-r6.test.mjs`). Steps: start AuthClient with provider for A and empty jar; signIn(); intercept the 200 verify response and return body '{' after the jar applied its Set-Cookie; let the recovery GET /api/auth/session return the real PRESENT; hold the following GET /api/me/home?fresh=1. At the gate assert sessionKnown=true, session=A, rows 1/1/0, prompts=1. Call the teardown returned by start() (0 logouts sent), release the house response, await signIn. Expected: no logout, rows stay 1/1/0, cookie kept, GET session signedIn:true. Actual: POST /api/auth/logout {expectedNonce}=204, rows 1/0/1, cookie gone, GET session signedIn:false. Control (same test, valid verify body, same held house read + stop): no logout, 1/1/0, cookie kept, GET signedIn:true. Parent 357668f: both cases pass.

### 2. Low: LOW-1 authority gap (retained): expectedNonce cleanup accepts a revoked or expired matching token, answers 204 and clears the session cookie

`source/server/auth.ts:632`

```
    const matches=token?await db.prepare(`SELECT 1 matched,
      (SELECT flow_hash FROM login_challenges WHERE nonce=?2) flow_hash FROM sessions WHERE token_hash=?1 AND nonce=?2`)
```

Prior IDs: fifth-Audit LOW-1 / R4-02 / AUD4-06; related dead-cookie invariant AUD3-06. Non-blocking for funds or house authority; blocks the required 'dead authority changes no rows/cookies' control for LOW-1. Merged from three specialists (economics #2, permissions #2, math #2), all on this line.

Mechanism: the expectedNonce branch selects the session by token_hash and nonce only, without `revoked_at IS NULL AND expires_at > now`. A dead cookie that still matches its own original nonce therefore reaches line 662-665: 204, `__Host-imd_session=; Max-Age=0` is emitted, and for an expired-but-unrevoked row revoked_at is newly written. The sibling expectedAddress branch (line 654) calls readSession and refuses dead tokens with 401 and no Set-Cookie; the session/home routes also refuse dead cookies without clearing (AUD3-06 comment at lines 607-610). The server comment at line 627 says 'revocation needs the matching session token', but a dead token is not a live authority.

Impact: because browsers apply Set-Cookie by arrival order, a delayed answer to such a request can delete a newer B session cookie installed meanwhile in the same jar, signing B out of that browser. B's session row and B's newer pending challenge are untouched (no cross-token DB revocation), so this is availability/context isolation, not authority escalation. This is distinct from the documented unavoidable race where A was still live when an authorized logout emitted its headers: here the server first authorizes the clear after A is already dead.

Measured (clock 1790596800000): revoked case: A signed in on b and on another device; the other device's /logout-all {expectedAddress:A} revokes both (2/0/2); b's GET session says signedIn:false; b POST /logout {expectedNonce:A nonce} -> 204 + session clear, rows unchanged 2/0/2. Expired case: A signed in, clock +7d, GET session false; same POST -> 204 + session clear, rows 1/0/0 -> 1/0/1 (revoked_at written on an expired row). In both, holding that response, signing in B on b and issuing B a pending challenge, then applying the held headers: jar loses the session cookie, keeps the flow cookie; GET session false; B row live (3/1/2 and 2/1/1), used challenges 3/2, pending 1, invalidated 0. No prompts/UI/timers involved (server-route probe). Existing auth-r5-authority.test.mjs covers dead tokens only with a different pending nonce, not a dead token with its own nonce.

Classification: retained from parent 357668f (same result there).

Fix: in the expectedNonce branch require a live matching session (`AND revoked_at IS NULL AND expires_at>?3`, or reuse readSession and compare its nonce), and refuse with 409/401 and no Set-Cookie otherwise; keep 'any token forbids pending-flow fallback' and explicit /logout {} semantics unchanged.

**Reproduction**

Test F2 in tests/reviewer-r6.test.mjs (`node --test tests/reviewer-r6.test.mjs`), real Worker over node:sqlite with all migrations. (1) b.signIn(A) -> 200; record A's challenge nonce. (2a) revoked: other.signIn(A), other POST /api/auth/logout-all {expectedAddress:A} -> 200. (2b) expired: clock.advance(7d). GET /api/auth/session on b -> signedIn:false in both. (3) b sends POST /api/auth/logout, content-type application/json, cookie = dead A token, body {expectedNonce:<A nonce>}. Expected: non-2xx, no Set-Cookie, no row change. Actual: 204 with `__Host-imd_session=; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age=0`; expired case also sets revoked_at. (4) Before applying that response, b.signIn(B) -> 200 and a B challenge; apply the held response: B's session cookie removed, GET session -> signedIn:false, B row still live, B pending challenge untouched. Controls in the same harness: expectedAddress with a dead token -> 401 without cookies (existing auth-r5-authority tests pass).

### 3. Low: LOW-2 partly fixed: a session read generated before verify committed releases the retained nonce, so teardown sends no cleanup while the verify body is pending

`source/src/world/auth.ts:263`

```
      if(this.flow?.uncertain&&this.flow.life===this.life)this.flow=null;
```

Prior IDs: fifth-Audit LOW-2 / R4-02 / AUD4-06 (flow specialist). Non-blocking for funds; blocks full closure of LOW-2's 'teardown during uncertain recovery must execute conditional cleanup while JS can run'. Distinct mechanism from the line-419 finding: there an accepted read is followed by a wrong late revocation; here a stale read wrongly releases responsibility and no cleanup happens at teardown.

Mechanism: readSession releases the retained uncertain flow on any valid response of the current generation, without checking that the read was issued after the in-flight verify committed. The channel listener at line 220 calls restore() on any tab message; during 'verifying' that read has the flow's gen and is the newest read, so it is applied. If the Worker answers it {signedIn:false} before verify commits, and the response is delivered after verify's Set-Cookie has arrived while verify's body is still pending (RC-1's stalled-body case), this line clears this.flow, line 274 sets session=null/sessionKnown=true. The teardown at lines 225-227 then finds no abandoned flow and sends nothing, although the browser holds the live cookie and JS is running. Cleanup only happens later at line 395 if/when the verify body settles; a body that never settles leaves the session live until expiry (7 days).

Impact: the page shows signed out (session null) while the browser carries a live EOA session cookie; the cookie still authorizes M1 writes (bootstrap/PUT profile) in that browser. Same-user, same-browser, so Low; it is a lost cleanup guarantee, not a bypass.

Measured (clock 1790596800000): order GET session=200 -> POST challenge=200 -> personal_sign (1) -> POST verify held before the Worker -> channel message -> GET session generated (signedIn:false) and held -> verify released, cookie applied, 200 headers returned with pending body -> session response delivered: sessionKnown=true, session=null, phase='verifying' -> stop(): 0 logouts, rows 1/1/0, cookie present, real GET session signedIn:true. Erroring the body afterwards: POST logout {expectedNonce}=204, rows 1/0/1. Control without the overlapping read: stop() sends the nonce logout at once (204) with the body still pending, rows 1/0/1. Challenge stays used=1, pending=0, invalidated=0; no post-stop UI writes, channel closed, no timers.

Classification: partly fixed vs parent 357668f (parent fails both the overlap case and the no-overlap control: no teardown cleanup at all).

Fix: do not release a verify's retained responsibility from a read that may predate its commit: e.g. record the sessionReads counter when the verify request is sent and only let reads begun after that (or reconcileVerify's own ordered read) release the flow; or have reconcileVerify/teardown treat flow release as valid only when the read observed signedIn:true for the flow's account. Keep accepted-PRESENT release and nonce-bound protection of newer sessions.

**Reproduction**

Test F3 in tests/reviewer-r6.test.mjs (`node --test tests/reviewer-r6.test.mjs`), real Worker over node:sqlite, injected channel. Steps: start with no cookie; signIn(); hold POST /api/auth/verify before it reaches the Worker; fire the registered channel 'message' listener; let the real GET /api/auth/session answer {signedIn:false} and hold its delivery; release verify, let the jar apply its Set-Cookie, return a 200 Response whose ReadableStream body never closes; deliver the held session response; call the teardown from start(). Expected: one POST /api/auth/logout {expectedNonce} at teardown, rows 1/0/1, cookie cleared. Actual: zero logouts, rows 1/1/0, cookie present, GET /api/auth/session signedIn:true; only after erroring the verify body does the late branch send the logout (204, 1/0/1). Control 'control-no-overlap' in the same test: teardown sends the logout immediately with the body still pending.

### 4. Low: Account switch does not cancel a sign-in click that is still waiting for its session read; the click then prompts for the new account

`source/src/world/auth.ts:469`

```
    if(!wasFlow&&!other){this.set({account:a});return;}
```

Prior IDs: retained N-2 / R3-R1 / ADV lifecycle contract, related to R4-02 (permissions specialist #3). Low: a stale click opens a personal_sign prompt for an account the user did not click for. The wallet still displays and must approve B's SIWE, so this is not a signature or account-authorization bypass.

Mechanism: signIn() sets busy=true and awaits wait()/restore() while phase stays 'idle', session=null, flow=null. accountChanged(B) computes wasFlow=false and other=false and takes this early return, which neither bumps gen nor clears busy. The waiting click therefore stays live; when the read confirms absence it reads this.s.account (now B), requests a challenge for B and prompts personal_sign for B. providerChanged() handles the same busy preflight by cancelling it (`if(flow||this.busy){this.gen++;this.busy=false;...}`), and the file's own contract says a click 'still waiting for a session read when one of them [a switch, a sign-out or the page's teardown] happens is ended by it too' (lines 310-311, 330), so this branch violates the stated invariant.

Measured: provider for A, initial GET /api/auth/session held; once account=A, signIn() (events: 1 GET, phase idle); accountsChanged([B]); release the GET. Order: GET session=200 -> POST challenge {address:B}=200 -> personal_sign for B (1 prompt) -> POST verify=200 -> GET /api/me/home=200. Rows 1/1/0 for B, challenge used=1; session cookie installed, 'signed-in' broadcast, expiry timer armed for B. Expected: no challenge, no prompt until a new explicit click. Control: with B selected from the start, the same sequence yields only the GET and no prompt.

Classification: retained (same result on parent 357668f).

Fix: before this early return, if this.busy (a preflight click is waiting) and the account changed to a different non-null account, bump gen and clear busy (as providerChanged does) without sending any automatic logout, since there is neither a retained nonce nor a displayed session.

**Reproduction**

Test F4 in tests/reviewer-r6.test.mjs (`node --test tests/reviewer-r6.test.mjs`). Steps: AuthClient.start() with a provider whose eth_accounts returns A and no cookie; hold the first GET /api/auth/session; wait until state.account===A; call signIn(); after a few ticks assert events.length===1 and phase idle; emit accountsChanged([B]) (state.account becomes B); release the held GET; await signIn(). Expected: no POST /api/auth/challenge, 0 personal_sign calls. Actual: POST /api/auth/challenge {address:B}, 1 personal_sign for B, a B session row created and shown as signed in.

### 5. Info: Public-name cache compares wall-clock ages, so a backward clock correction keeps a stale name for the size of the jump

`source/src/world/member.ts:194`

```
  const hit=names.get(a);if(hit&&now-hit.at<NAME_TTL_MS)return hit.name;
```

Not one of the four Low items and not a regression of this repair (math specialist #3; same code on parent 357668f). Presentation-only: names never authorize houses, writes or assets. Reported because LOW-4 moved the rename cooldown off Date.now subtraction for exactly this reason, and this sibling one-minute cache (publicName, and lookupName at line 209 which uses the same comparison) still uses it. A negative age stays below NAME_TTL_MS, so after a backward wall-clock correction a renamed or moderated profile keeps showing its old name in house panels until wall time passes the old timestamp + 60 s, until the entry is evicted (256-entry cap) or the page reloads. Realistic corrections are small (seconds), so the practical window is short; large jumps only occur with a badly wrong clock being corrected.

Fix: compute the cache age from a monotonic source (performance.now, as the member client now does), or treat a negative age as expired.

**Reproduction**

Test F5 in tests/reviewer-r6.test.mjs (`node --test tests/reviewer-r6.test.mjs`), unmodified publicName with an injected get. address=0xabab...ab, t0=1790000000000: publicName(address,t0,get) with get -> {name:'PriorName'} returns 'PriorName' (1 GET). Change get to return {name:'NewName'}. publicName(address,t0-259200000+60001,get) (wall clock corrected 3 days back, then 60.001 s elapsed). Expected: cache older than 60 s refreshes -> 'NewName' (2 GETs). Actual: 'PriorName', still 1 GET (age = -259139999 ms < 60000). Control: publicName(address,t0+60000,get) -> 'NewName' and the GET count becomes 2.

### 6. Info: Sixth-review verdict matrix: four-Low closure, R5-01..09 map, regression status and review limits

`source/docs/security/R5_LOW_REMEDIATION.md:15`

```
| LOW-1 — switch cleanup affects newer shared-cookie context | Retain the original flow nonce; automatic cleanup sends `expectedNonce`, or `expectedAddress` when only a displayed session is available. No assertion means no automatic logout. Nonce/address are consistency assertions, not authority. The server requires the matching token for revocation and preserves a different current pending flow. Successful or refused cleanup reconciles the cookie when needed; identical address/expiry is not treated as session identity. | Account/provider switches with newer B, newer same-wallet A, pending-only replacement; wrong/missing/forged/dead authority; pruned original challenge; original-flow-only cancellation; delayed completion with a new same-address/expiry session. |
```

Not a defect; the review verdict the task requires, anchored to the remediation table. Pinned public commit 445747d6a4d4fb6fa4eaa9c67b74e3e2bd9c1703, parent 357668f. Subject is TypeScript Worker/React; no Solidity, so the Solidity reference checklists were applied only as generic failure-mode prompts (access control per entry point, replay/nonce consumption, time/ordering, tests not covering edges). Private source 1cc61b68, 1183-case private suite, production D1/WAF/limiter, real wallets/browsers and withheld assets were not checked and remain team claims.

FOUR-LOW VERDICT (reviewer measurements):
- LOW-1 (R4-02/AUD4-06): PARTLY. Account/provider switch preservation of newer B / same-wallet A / pending-only, no-assertion-no-logout, pruned original, same-address/expiry delayed completion: pass (project tests auth-r5.test.mjs and auth-r5-authority.test.mjs re-run, 102/102). Open: expectedNonce accepts a revoked/expired matching token (finding at server/auth.ts:632).
- LOW-2 (R4-02/AUD4-06): PARTLY. Teardown during a held/failed uncertain read now sends nonce-bound cleanup (control measured: 1 logout at stop, 1/0/1); life guard stops old-lifetime UI/channel/timer writes (measured: no post-stop UI or broadcast). Open: pre-commit overlapping read releases responsibility (auth.ts:263); accepted PRESENT + stop during house read gets revoked by the late branch (auth.ts:419, new regression).
- LOW-3 (R4-02/AUD4-06/CORR-02): FIXED LOCALLY. readSession lines 261-262 accept only signedIn===false (expired undefined/boolean) or signedIn===true + address + positive safe-integer expiresAt; non-2xx/network/parse failures leave sessionKnown=false; signIn re-reads first (line 329) and refuses with 'session-unknown' while unknown (line 337). Project LOW-3 table tests pass. No deadline on the auth fetch remains (known limit).
- LOW-4 (R4-08/AUD4-08): FIXED LOCALLY. member.ts serverNow() = timeBase.server + max(0, monotonicNow - timeBase.elapsed); timer only schedules load(), cooling derives from server deadline vs serverTime; failed refresh retries after PROFILE_COOLDOWN_RETRY_MS=60000; run/gen guards on callbacks. member-r5 tests pass. Simulated throttling is not OS-suspension proof.

R5-01..09 MATRIX: 01 account-switch preservation: pass (auth-r5 LOW-1 account cases) but see auth.ts:469 for a busy-preflight click not cancelled. 02 provider-switch: pass. 03 teardown cleanup: partly (auth.ts:263, :419). 04 malformed UNKNOWN: pass. 05 invalid positive schema UNKNOWN: pass. 06 GET before personal_sign: pass (line 329/337). 07 no duplicate session/prompt: pass in measured cases (1 prompt each). 08 backward clock: pass for the cooldown; sibling name cache still wall-clock (member.ts:194, info). 09 timer server reconcile: pass.

REGRESSIONS CHECKED: R4-01 logout-all requires live cookie address == expectedAddress, 409 on mismatch before revocation, 401 dead cookie without Set-Cookie (server/auth.ts:673-688; project tests pass). AUD3-06 dead cookie refused-not-cleared holds for session/home/logout-all/expectedAddress, broken only for expectedNonce (finding). Explicit /logout {} keeps current-cookie semantics (test passes). Wallet methods remain eth_accounts/eth_requestAccounts/personal_sign (provider fixture throws on anything else; none seen). No Solidity/Mint/transactions present.

PUBLIC SUITE: `npm test` in a scratch npm-ci copy: 343 run, 332 pass; failures = 6 reviewer assertions, 3 files unloadable (withheld src/world/households.ts: home-entry, ownership, wallet-client), 2 deploy-evidence tests needing a git checkout. Team's 212/212 seven-file no-stub figure was not reproduced as such; the project's auth/authority/aud4 files gave 102/102.

NOT DONE: no live GETs to imdember.com, no Worker rebuild/byte comparison, no production D1 check; the fifth Audit/Report originals were not fetched (offline review), their hashes in R6/PRIOR_REVIEWS.md are team records.

**Reproduction**

Commands run in /tmp scratch copy of source/ (repo tree unchanged): `npm ci --ignore-scripts`; `node --test tests/auth-r5.test.mjs tests/auth-r5-authority.test.mjs tests/aud4-auth.test.mjs` (102/102); `node --test tests/reviewer-r6.test.mjs` (8 cases: F1 corrupt FAIL/valid PASS, F2 revoked FAIL/expired FAIL, F3 overlap FAIL/control PASS, F4 FAIL, F5 FAIL); same file against `git archive 357668f` (F1 both PASS, F2 FAIL x2, F3 FAIL x2, F4 FAIL, F5 FAIL); `npm test` (343/332). Node v24.21.0, npm 11.19.0, no shims: native TS type stripping, node:sqlite, viem from the lockfile.

---

Judge's submission `2ee49d656abb43c155aaabefe088979d2f00a69aa6ccf7d3b98ce52dc34aa53e`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
