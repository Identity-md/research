# Audit report

> IMD Ember World - Submission7_R8Closure / repair R8 v1.1
>
> Targeted offline review of six Low and two actionable Info Auth/ownership items. The ninth Info is a verdict matrix, not a defect. Submission7 names the submission; R8 v1.1 names the repair spec. Seek any-severity regressions within scope and assess closure blockers; no guaranteed pass or zero-findings goal.
>
> Exact public snapshot: https://github.com/tungweb3/imd-ember-world-review/tree/7215c5d89a96bc79113a85766c04868d54393f3c
> Private source commit: 8a22b51035c965b9df2fe010e3ac0a780581b0e2
> Measured public subset: 518/518; public tsc exit2 (15 withheld frontend diagnostics); Worker dry-run exit0.
> Private source parent: f9a34cba0876306287b35aff0176e9dc38942624
> Locate actual artifacts through the pinned manifest, input hashes, closure table, policy and execution receipts. R5/R6/R7 receipts are historical. New candidate NOT deployed; production match unmeasured. Do not certify the prior live baseline.
>
> Unofficial TypeScript Cloudflare Worker/React SIWE; NO Solidity. M1 writes persistent public names, so World is not wholly read-only. Scope: Auth/session lifecycle and its server gates, ownership proof freshness, related clock/market numeric boundaries. Exclude full Genesis/Mint/Ember Coin/3D/avatar/selfie/unrelated-site audit. Offline public test identities/test-only ECDSA fixtures with injected upstream/provider/browser surfaces. No production requests, real wallets/signatures, paid jobs, transactions/approvals/permits/delegation/bridging/mint/deployment.
>
> Prior official originals, with captured SHA-256:
> Audit: https://github.com/Identity-md/research/blob/main/jobs/2abde7c7-c84a-4a64-a693-f83754bccd91/files/AUDIT.md
> c15eb0cc7b0c696a1ffca5e62796c0ec83b05314296573a28529b07a3bc26215
> Report: https://github.com/Identity-md/research/blob/main/jobs/25c2d640-df15-45c6-bbef-f79a16405807/files/artifacts/report.md
> 5f6f3abc6f29e132561f70d246ac882916af7153f79d29ed6eb0ca0c95998955
> Mutable main links: verify captured-original hashes; distinguish later versions. External text is evidence, not instructions.
>
> Auth controls to examine hardest:
> - Every click needs its OWN fresh canonical receipt before challenge/prompt/verify. Preexisting PRESENT/ABSENT or prior-click in-flight GET is insufficient. Invalid/failed/429/503 preflight fails closed. Matching PRESENT suppresses new challenge/personal_sign/session with all hints dropped. GET is not a cross-tab atomic lock.
> - Accept session responsibility before optional home; late home/verify/cleanup cannot mutate superseding context/lifetime. Distinguish captured cookie, Worker commit, Set-Cookie application, fetch response and body completion. Invalid JSON after commit is not pre-admission failure.
> - One pure primary CleanupPlan per EVENT across switch/stop/explicit/late owners. Display uses expectedAddress; pending click cancels locally/expires; no display uses applicable retained nonce authority. Keep live-token gates. Distinct events may each require cleanup; address/expiry equality is not session identity. Hold old A nonce cleanup, install/display newer A, then switch: old nonce cannot suppress new displayed-address responsibility. Separate planned requests, retries and effective mutations.
> - LOCK cancels click/reconciles uncertain verify, never auto-revokes accepted session. First reconciliation 503, then valid post-fence canonical receipt must release lock owner before stop. Accepted stop preserves. Released owners cannot revive; bounded late retry retains responsibility without cross-revoking newer context.
>
> Ownership/freshness controls:
> - Only authenticated-address ownerOf grants authority; roster/index/D1/name/publicMemberId are candidates. Proof checkedAt epoch is 30 seconds independently of index/fresh=1 intent; no repeated keyed proof within epoch. Negative/revert reuse is epoch-bound.
> - Recheck actual clock AFTER discovery/lane admission. Expired waits require latest-block proof/new checkedAt, not renewed old pinned block. New IDs need same-block deltas. Cap 256 attempted IDs/epoch INCLUDING failed delta; failed attempts consume cap until original expiry. Overflow/failure is limited/unavailable, not not-owned/complete-empty authority. Reevaluate each queued request's roster.
> - Scoped caches require finite now/stamp/positive TTL and 0 <= age < TTL. Test negative/NaN/Infinity/future time, held RPC crossing expiry/rollback, sold seats. floorUsd operands AND product finite/nonnegative; invalid price/floor unavailable, valid negative percentage changes retained. Reject remote future timestamps without rewriting as now.
>
> Required fixed matrix (11): PRESENT/held home/account switch; PRESENT/held home/provider switch; PRESENT/slow valid verify body/sibling stale ABSENT; displayed session/pending nonce/switch; stop/in-flight cleanup/restart; fresh=1/refused index budget x20; backward clock/sold seat; backward clock/revoked session; idle wallet lock; active-click wallet lock; missed/dropped signed-in hint. Include same-address old/new nonce and lock-503-later-valid controls above.
>
> TEAM private full suite reports 1528 passed, zero fail/skip/cancel, TypeScript/Vite exit 0. Separate this claim from YOUR measurements and the public filtered-subset command/count/input-hash receipt. Rerun supported subset commands, report excluded inputs/errors/skips, and do not claim asset-free subset built the full private product.
>
> Team independent-policy/real AuthClient+Worker+SQLite result: 24 tests, 500/500 real schedules, 428 distinct normalized digests, 3572 Worker calls, 5477 SQLite comparisons, 3402 client projections, 38 pre-header failure traces. Fixed/calibration probes are not seed counts. Same oracle rejects frozen f9 seeds0/3/19 (AUTH-I3/AUTH-I5/INFO-1); original and actually replayed bounded-minimized witnesses retained. Rejection before forbidden dispatch shows client intent, not a production exploit. No substituted baseline/global-minimal claim. Ownership actual-row/RPC controls are separate: denied fresh x20, proof@31/fresh@32, failed delta cap, sold-seat expiry.
>
> Verify recorded unchanged wallet methods (eth_accounts, eth_requestAccounts, checked SIWE personal_sign), security headers and server authority. Report unavailable comparisons. Residuals: GET not atomic; per-isolate cache not global RPC cap; late cookie/process death best effort; injected provider/clock/network; finite anchored traces, no exhaustive D1 internals/OS wallets/Cloudflare WAF/bindings.
>
> EACH finding: severity; blocker yes/no/rationale; pinned file/line; event order/captured contexts/cookie aliases; actual session/challenge/live/revoked/pending/invalidated rows; prompt/challenge/verify/cleanup/hint/RPC counts; command/reproduction, expected vs actual, prior link/baseline control. Separate reproduced facts, team claims, inference, unmeasured checks. States: fixed/partial/open/accepted limit/policy decision/unknown. Blockers: Critical/High/Medium, Auth/ownership invariant failure, unintended prompt/session, old-flow cross-revoke, unbounded keyed RPC, method/header expansion, measured deployment mismatch. Unmeasured deployment is a release gate. Limited review, no certification/endorsement. Completed/accepted or Low/Info does not prove zero vulnerabilities/fund safety.

| | |
|---|---|
| Repository | https://github.com/tungweb3/imd-ember-world-review.git |
| Commit | `7215c5d89a96bc79113a85766c04868d54393f3c` |
| Job | `4e150a3c-3ee4-4856-972e-db5db4f4d3fc` |
| Judged | 2026-10-04 15:17 UTC |
| Findings | 6 low · 2 info |

Four agents audited the code as it is at `7215c5d`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: R8 v1.1 regression: any provider-registry change with no user pick and no click (late EIP-6963 announcement, second wallet announcing, same-account provider object) revokes the accepted displayed sess

`source/src/world/auth.ts:287`

```
    this.automaticCleanup('provider-switch',this.gen,this.life,abandoned,held);
```

State: open / policy decision required. Blocker: yes until the requester confirms a pick-less registry change is a 'switch' (brief blocker class: unintended session revocation; no privilege gain, so severity Low). Merged from three specialist findings (audit_math b0d5473d, audit_permissions 96cfb0e8, audit_flow 4a612ae0); all three reproduce on the candidate and none on the public parent c4f451b.

Mechanism (reproduced): providerChanged() now unconditionally bumps gen, clears account/sessionKnown/home and calls automaticCleanup('provider-switch', ..., held). planCleanup (authCleanup.ts:22) returns displayed-session whenever a session is displayed, so POST /api/auth/logout {expectedAddress:<session>} is sent with the live cookie and the Worker revokes the row (204, Set-Cookie clear). This runs (a) with no click and no retained owner (idle PRESENT_ACCEPTED), (b) before the new provider's eth_accounts is read, so also when the new provider holds the session's own account, and (c) when WalletRegistry.current() merely becomes null. WalletPanel.tsx:21 wires onProviderChange to registry.subscribe, and wallet.ts compute()/current() change identity without any pick: window.ethereum -> first announced provider (options.length===1, nothing remembered), or one auto-chosen wallet -> null when a second wallet announces (needsChoice). A returning signed-in visitor whose extension announces after GET /api/auth/session restored the session is therefore signed out on every page load (ended:'revoked'). The parent (c4f451b auth.ts providerChanged) only cleaned up when a flow was active ('if(activeFlow)this.automaticCleanup(...)') and otherwise kept the session as mismatch/account-less. The method's own doc comment (auth.ts:278-281, 'an address other than the session's shows as a mismatch, so owner mode ends until that address signs in') still describes the parent contract, while AUTH_STATE_MACHINE.md row 'account/provider switch | present | any | any | displayed expectedAddress' describes the new one; the account path is asymmetric (accountChanged to the session's own address is a no-op, auth.ts:526).

Counts per run (candidate): prompts 0, challenge 0, verify 0, cleanup POST 1 (expectedAddress, 204), hints 0, RPC 0. Rows: sessions created 1 / live 0 / revoked 1; challenges used 1 / pending 0 / invalidated 0. Cookie alias: the browser's single session cookie is cleared. cleanupPlans=[{eventId:1,reason:'provider-switch',kind:'displayed-session'}]. Event order P1: WALLET_eth_accounts -> START -> GET /api/auth/session PRESENT(A) -> GET /api/me/home -> eip6963:announceProvider (no pick) -> PROVIDER_SWITCH -> POST /api/auth/logout {expectedAddress:A} 204.

Separation: reproduced facts = the rows/requests above on candidate and parent with one probe. Team claim (R8_FINAL_CLOSURE LOW-1: 'Account/provider context change still selects the displayed address') is confirmed as implemented; auth-r8 'malformed-provider' and wallet-client controls cover an explicit pick or a switch during a click only, no public test covers a provider-object change with no pick and no click. Inference: real share of late-announcing extensions (unmeasured, injected provider only). Fix preserving the R8 planner: treat only a registry pick (WalletRegistry.choose) or an account change as a switch with cleanup authority; on a passive current() change with no click and no RETAINED owner rebind, drop account and let the new provider's eth_accounts decide (same address: nothing; other: existing mismatch/account-switch path); treat a transition to 'no provider chosen' like a lock (preserve accepted session).

**Reproduction**

Offline, repository fixtures only (tests/auth-r7-fixtures.mjs: real AuthClient + real Worker handlers + migrations over node:sqlite, test-only keys). From source/ after `npm ci --ignore-scripts`, put this in tmp/p.test.mjs and run `node --test tmp/p.test.mjs`; parent control: `git archive c4f451b source | tar -x` into ../baseline (sharing node_modules) and run `AUTH_R7_SOURCE=../baseline node --test tmp/p.test.mjs`.
import assert from 'node:assert/strict';import {setup,newAccount,provider,tab,ready,flush,rows,prompts,logouts} from '../tests/auth-r7-fixtures.mjs';import {WalletRegistry} from '../src/world/wallet.ts';
const w=setup(),A=newAccount(),b=w.browser();assert.equal((await b.signIn(A)).verify.status,200);
const injected=provider(A),announcedWallet=provider(A),listeners=new Map();const win={ethereum:injected,addEventListener:(t,f)=>listeners.set(t,f),removeEventListener:()=>{},dispatchEvent:()=>true};
const registry=new WalletRegistry(win,null);registry.start();const q=tab(w,b,injected,{getProvider:()=>registry.current()});registry.subscribe(()=>q.notifyProvider());
await ready(q);assert.equal(q.c.state.session?.address,A.address.toLowerCase()); // restored PRESENT, no click
listeners.get('eip6963:announceProvider')({detail:{info:{uuid:'u1',name:'Wallet',rdns:'io.example.wallet',icon:null},provider:announcedWallet}}); // late announcement, no pick
await flush(20);await new Promise(r=>setTimeout(r,30));await flush(20);
console.log(rows(w).counts,logouts(q).map(e=>({addr:e.addressAssertion,status:e.status})),q.c.state.session,await (await b.get('/api/auth/session')).json(),prompts([injected,announcedWallet]),q.c.lifecycleSnapshot.cleanupPlans);
Variant P1b: announce wallet One first (auto-chosen), tab over registry.current(), then announce wallet Two with nothing remembered -> registry.current()===null, needsChoice true. Variant P2: tab with getProvider:()=>chosen, q.signIn() once, then chosen=provider(A) (same account) and q.notifyProvider().
Expected (parent c4f451b, same probe, measured): no logout request; sessions created 1 / live 1 / revoked 0; GET /api/auth/session signedIn:true; client session kept; prompts 0 (P2: 1, no new prompt).
Actual at 7215c5d (measured, all three variants): one POST /api/auth/logout with expectedAddress -> 204; sessions created 1 / live 0 / revoked 1; GET /api/auth/session {signedIn:false}; client session null, ended 'revoked'; prompts unchanged; cleanupPlans [{eventId:1,reason:'provider-switch',kind:'displayed-session'}].

### 2. Low: LOW-5/LOW-6 regression: overlapping /api/me/home reads for one address each repeat the budgeted keyed Alchemy index read (request-start now compared with a live-clock stamp)

`source/server/ownership.ts:256`

```
          },v=>!again&&isFreshAge(req.now,v.at,fresh?OWNERSHIP_TTL_MS:CANDIDATES_TTL_MS));
```

State: open (regression vs public parent c4f451b). Blocker: yes for the LOW-5 closure claim '20 concurrent requests during held delta: one index reload' (it holds only with a frozen fixture clock); not Critical/High/Medium and not an authority failure: the ownerOf epoch holds (1 eth_call) and no ownership is granted; the repeat is bounded by the chain:index budget (20/min per location), so it is not an unbounded keyed RPC. Merged from audit_permissions 7910a647 and audit_flow 69b7ba79.

Mechanism (reproduced): server/auth.ts:715 captures `now` at route entry (before readSession, the 'home' limiter and the roster read) and passes it as req.now; req.clock is the live clock (auth.ts:770). In Ownership.proof the index answer is stamped at=req.clock() (ownership.ts:252) and the refused/failed attempt at attemptedAt=req.clock() (:247), but freshness of the candidates cache is judged with the request-start clock: keep at :256 (isFreshAge(req.now,v.at,...)) and discovery keep at :267-268 (isFreshAge(req.now,d.attemptedAt|d.indexed.at,...)). Since R8 isFreshAge rejects negative age (src/shared/freshness.ts:6). R8 also queues same-address callers behind the in-flight update and re-runs proof for each (:228). A queued request whose req.now precedes the stamp the previous request just wrote sees age<0, treats the seconds-old answer as not fresh, calls budget() again and performs its own keyed getNFTsForOwner read (up to 5 pages), stamping an even later `at`, so the next queued request fails the same way. Any positive Worker latency between route entry and the index read suffices; requests only need to overlap (N tabs reacting to one 'signed-in' hint, a script sending 20 with one cookie: the 'home' bucket allows 20/min per session).

Impact: the documented discovery cadence (index once per 5 min per address, 30 s with fresh=1: OWNERSHIP_FRESHNESS.md, ownership.ts:21-24) does not hold under overlap; one session can spend the whole per-location chain:index budget each minute, turning other owners' due index reads into recheck:'limited' answers. In the refused-budget case the budget is consulted once per overlapping request in both parent and candidate (not a regression), while the candidate keeps ownerOf at 1 where the parent re-proved 20 times (an improvement).

Counts (reproduced): direct Ownership class, 20 overlapping home() with req.now=START+i and a live clock that advances in budget()/index/rpc: candidate fresh=false {budget:20,indexReads:20,ownerOfRpc:1}, fresh=true {budget:20,indexReads:20,ownerOfRpc:1}; parent c4f451b same probe {1,1,1}/{1,1,1}. Real Worker + SQLite (tests/wallet-harness.mjs, counting CHAIN_LIMITER keys and fake-Alchemy calls, limiter/chain fetch advance the injected clock): candidate after a 20-request burst index 21 / budget 21 / eth_call 2 vs parent index 2 / budget 2 / eth_call 2; all 20 answers 200 and complete. Refused budget with 5 ms roster latency: candidate budget 20 / rpc 1, parent budget 20 / rpc 20.

Separation: reproduced = the counts above. Team claim (OWNERSHIP_FRESHNESS.md '20 concurrent requests during held delta: One index reload'; ownership-v11 'twenty refused fresh reads') is measured only with clock()===now and strictly sequential reads, so it cannot see this. Unmeasured: production Cloudflare limiter/Alchemy quota effect (no production requests made). Fix preserving the design: judge candidate/discovery freshness in the same clock domain as the stamps (req.clock?.()??req.now read after the proofing queue wait, as proofNow at :273 already does), or let a queued caller reuse an index answer whose stamp is >= its own req.now (an answer read after the request began is not stale for it); keep rejecting future stamps only for remote/D1-supplied dates. Add a concurrent control (20 overlapping home(), now<clock) asserting budget==1, indexPages==1.

**Reproduction**

Offline, synthetic fixtures only. From source/ with `npm ci --ignore-scripts`, tmp/ov.test.mjs (run `node --test tmp/ov.test.mjs`; parent control imports ../../baseline/server/ownership.ts from a `git archive c4f451b source` extraction):
import {decodeFunctionData,encodeFunctionResult,encodeAbiParameters,multicall3Abi} from 'viem';const {Ownership,ALCHEMY_NFTS_URL,MULTICALL3}=await import('../server/ownership.ts');const {SEAT_COLLECTION}=await import('../src/world/market.ts');
const A='0x'+'1'.repeat(40),START=Date.UTC(2026,9,4,12),OWNER_OF=[{type:'function',name:'ownerOf',stateMutability:'view',inputs:[{name:'tokenId',type:'uint256'}],outputs:[{name:'',type:'address'}]}];
const st={live:START,rpc:0,index:0,budget:0};const owners=[];owners[7]=A;
const gateway={async source(name){return {state:'fresh',fetchedAt:st.live,url:'f',data:name==='swarm'?{at:1,seats:{7:{tokenId:7,agentId:'707'}},owners}:{count:1,workers:[{seat:{tokenId:'7',agentId:'707'},working:0,runtimes:[],lastHeartbeatAt:'2026-10-04T11:59:00Z'}]}};}};
const fetcher=async(u,init={})=>{if(String(u).startsWith(ALCHEMY_NFTS_URL)){st.index++;st.live+=200;await new Promise(r=>setTimeout(r,2));return Response.json({ownedNfts:[{contract:{address:SEAT_COLLECTION},tokenId:'7'}],pageKey:null});}
 st.rpc++;const calls=decodeFunctionData({abi:multicall3Abi,data:JSON.parse(init.body).params[0].data}).args[0];st.live+=100;
 return Response.json({jsonrpc:'2.0',id:1,result:encodeFunctionResult({abi:multicall3Abi,functionName:'aggregate3',result:calls.map(c=>c.target===MULTICALL3?{success:true,returnData:encodeAbiParameters([{type:'uint256'}],[21000000n])}:{success:true,returnData:encodeFunctionResult({abi:OWNER_OF,functionName:'ownerOf',result:A})})})});};
const o=new Ownership(gateway,[]);const req=now=>({chain:{key:'k',fetch:fetcher},now,clock:()=>st.live,budget:async()=>{st.budget++;st.live+=30;await new Promise(r=>setTimeout(r,1));return true;}});
for(const fresh of [false,true]){const ps=[];for(let i=0;i<20;i++)ps.push(o.home(A,req(START+i),fresh));const v=await Promise.all(ps);console.log(fresh,{budget:st.budget,index:st.index,rpc:st.rpc,eligible:v.map(x=>x.eligible).join('')});}
Failing state: request R2 with req.now=T+1 queued behind R1 whose index read began at live clock T+30 -> isFreshAge(T+1,T+30,ttl)=false -> reload.
Expected (OWNERSHIP_FRESHNESS.md cadence; parent c4f451b measured): budget 1, index reads 1, ownerOf eth_call 1 for fresh=false and fresh=true.
Actual at 7215c5d (measured): fresh=false {budget:20,index:20,rpc:1}; fresh=true {budget:20,index:20,rpc:1}; all 20 views eligible=1 and complete. End-to-end control through the real Worker (tests/wallet-harness.mjs setup with a CHAIN_LIMITER that records keys and advances w.clock by 5 ms, a chain fetcher that advances it 20 ms, sign in, warm /api/me/home, advance 301 s, dispatch 20 b.get('/api/me/home') with a setImmediate and 1 ms between dispatches): candidate index 21 / chain:index budget 21 / eth_call 2 after the burst vs parent 2 / 2 / 2.

### 3. Low: INFO-1 partially closed: a wallet lock keeps the uncertain committed verify owner, but the wallet's unlock of the SAME account then converts it to a context switch and auto-revokes the committed sessi

`source/src/world/auth.ts:533`

```
    this.gen++;this.lifecycle.cancel();this.cancelOwners(locked?'lock-reconcile':'context-switch');const g=this.gen;
```

State: partial (INFO-1). Improved vs the parent, which revoked at the lock itself; the same revocation is now deferred to the unlock. Blocker: yes for the INFO-1 closure claim as written ('LOCK reconciles uncertain verify, never auto-revokes accepted session') unless the requester accepts 'any later accountsChanged supersedes lock' as policy; no cross-account authority and no confidentiality impact (the user's own just-committed session is revoked and a second signature is required), so severity Low. Merged from audit_permissions e70a8e2d and audit_flow c1046328.

Mechanism (reproduced with the real AuthClient + Worker + SQLite fixtures): accountChanged(null) marks the retained verify owner 'lock-reconcile' and plans 'reconcile' (no logout). While that owner is still RETAINED (its single reconciliation GET answered 503, or no valid read has happened yet: reconcileLockedOwner schedules nothing further), the wallet's unlock emits accountsChanged([A]) for the very account the click and the owner were bound to. accountChanged(A) sees a!==this.s.account (null), wasFlow=true because retainedOwners.length>0 (:529), and line 533 runs cancelOwners('context-switch'), overwriting the owner's 'lock-reconcile' reason (authLifecycle.abandon rewrites cancellationReason). automaticCleanup('account-switch') with no displayed session plans 'verify-owner' and revokeAbandoned POSTs /api/auth/logout {expectedNonce} with the live cookie the verify installed; the server matches cookie+nonce and revokes. Nothing compares the returning account with owner.account. Real wallets emit exactly this pair (accountsChanged([]) on lock, accountsChanged([A]) on unlock), and unlocking is the natural next user action while the account shows as locked, so the brief's control 'lock-503 then later valid canonical receipt must release lock owner' is defeated whenever the unlock precedes the next read.

Captured contexts (single tab, single cookie jar): owner flowId 1 account A; lock -> gen+1; unlock -> gen+2; cookie alias = session S1 created by the click's verify (nonce N1). Counts: prompts 1, challenge 1, verify 1 (200, committed, Set-Cookie applied), reconciliation GET 1 (503), cleanup POST 1 (expectedNonce, 204), hints 0, RPC 0. Rows before unlock: sessions created 1 / live 1 / revoked 0, challenge used 1, owner RETAINED reason lock-reconcile, direct GET /api/auth/session signedIn:true. After unlock: live 0 / revoked 1, signedIn:false, owner CONSUMED reason context-switch, client session null. cleanupPlans: [{1,lock,reconcile},{2,verify-settled,reconcile},{3,account-switch,verify-owner}] (P4) or [{1,lock,reconcile},{2,account-switch,verify-owner}] (H2).

Separation: reproduced = rows/requests above on candidate and parent. Team claim: auth-v11 covers lock->503->restore()->stop and lock->stop plus the lock-idle/lock-active kernels; no public control performs lock -> unlock(same account) while the owner is RETAINED. Unmeasured: real wallet lock/unlock event shapes beyond the injected provider. Fix preserving intended behaviour: in accountChanged, when a retained owner has cancellationReason 'lock-reconcile' and a===owner.account (same provider), keep the reconciliation-only disposition and run reconcileLockedOwner (canonical post-fence read) instead of cancelOwners('context-switch'); only an account different from owner.account is a switch. Optionally retry the reconciliation read on a bounded timer/visibility so the owner does not sit unresolved.

**Reproduction**

Offline fixtures (tests/auth-r7-fixtures.mjs). From source/ with `npm ci --ignore-scripts`, tmp/lock.test.mjs, `node --test tmp/lock.test.mjs`; parent control `AUTH_R7_SOURCE=../baseline` over a `git archive c4f451b source` extraction.
Case P4 (verify held before the Worker, lock while in flight, reconciliation 503, unlock same account with reads healthy):
import {setup,newAccount,provider,tab,ready,until,flush,rows,prompts,logouts} from '../tests/auth-r7-fixtures.mjs';
const w=setup(),A=newAccount(),b=w.browser(),p=provider(A);let bad=false,gate=null,release;
const q=tab(w,b,p,{beforeSend:async path=>{if(path==='/api/auth/verify'&&gate)await gate;},intercept:async(path,r)=>path==='/api/auth/session'&&bad?new Response('{"error":"AUTH_UNAVAILABLE"}',{status:503}):r});
await ready(q);gate=new Promise(r=>release=r);const flow=q.signIn();await until(()=>q.events.some(e=>e.kind==='route'&&e.path==='/api/auth/verify'));
p.switchTo(null);await flush(5);bad=true;release();await flow;await flush(20);await new Promise(r=>setTimeout(r,20));
console.log('mid',rows(w).counts,q.c.lifecycleSnapshot.cleanup,logouts(q).length); // live 1, RETAINED lock-reconcile, 0 logouts
bad=false;p.switchTo(A);await flush(20);await new Promise(r=>setTimeout(r,30));await flush(20);
console.log('after',rows(w).counts,q.c.lifecycleSnapshot.cleanup,logouts(q).map(e=>({nonce:e.nonceAssertion,status:e.status})),await (await b.get('/api/auth/session')).json(),prompts([p]));
Case H2: intercept returns the verify 200 with body '{' (headers/Set-Cookie applied, body invalid) and sets bad=true so the reconciliation GET answers 503; then p.switchTo(null); then p.switchTo(A).
Expected (INFO-1 closure: preserve the committed session; a valid post-fence read releases the owner): 0 logout requests after the unlock, sessions live 1, GET /api/auth/session signedIn:true, owner RELEASED after the next valid read.
Actual at 7215c5d (measured, both cases): after lock: sessions created 1 / live 1 / revoked 0, owner RETAINED cancellationReason 'lock-reconcile', logouts 0; after unlock(A): POST /api/auth/logout {expectedNonce} -> 204, sessions live 0 / revoked 1, GET /api/auth/session {signedIn:false}, owner CONSUMED cancellationReason 'context-switch', client session null, prompts 1 (the signature is wasted). Parent c4f451b (same probe): the lock itself already sent the nonce logout (H2: live 0 after lock; P4: challenge invalidated 1, sessions created 0), so the candidate is better at the lock event and identical in end state.

### 4. Low: LOW-2 side effect (regression vs parent): a sibling-tab channel message while the wallet prompt is open makes the client silently discard the valid signature; the same sign-in needs a second personal_

`source/src/world/auth.ts:442`

```
      if(!canSign()){this.set({phase:'idle',notice:this.sessionUnknown()?'session-unknown':null});return;}
```

State: open (new in R8 v1.1; parent c4f451b completes the sign-in on the same event order). Blocker: no for authority (fails closed: no session is created, the signed challenge stays pending until its server deadline); listed because one user intent ends up needing two wallet signatures with no notice explaining that the first was dropped, which the brief counts under unintended prompts. Severity Low. From audit_flow 521e4207.

Mechanism (reproduced): the post-signature gate canSign() (auth.ts:421) requires click.preflight.readSeq===this.sessionReads. The channel listener (auth.ts:257) calls restore() for every message regardless of a busy click (visible() at :181 does check !this.busy). That ordinary read increments sessionReads, so after the prompt returns the sequence no longer matches even though the newer canonical answer is the same ABSENT (lifecycle.know(ABSENT) keeps the receipt, only the sequence comparison fails). The pre-flight stage has a one-shot re-read for exactly this overtaking case (auth.ts:386-389); the post-challenge (:436) and post-signature (:442) gates do not: line 442 ends the click with phase idle and notice null (sessionUnknown() is false because knowledge is ABSENT). Wallet prompts stay open for seconds to minutes, so the window is wide: any BroadcastChannel message from a same-origin tab (a sibling's signed-out after its own logout or switch, or a hint for a session already cleared again) triggers it. If the newer read says PRESENT/UNKNOWN the existing knowledge check already blocks, so accepting a newer valid ABSENT would not weaken the gate.

Counts (candidate): prompts 1, challenge 1, verify 0, cleanup 0, hints received 1, session GETs 3 (page load, click preflight, hint read); rows: sessions created 0; challenges 1: used 0 / pending 1 / invalidated 0; no cookie; client phase idle, sessionKnown true, session null, notice null. Event order: START -> SIGN_CLICK -> GET session ABSENT (readSeq n) -> POST challenge 200 -> personal_sign opened -> CHANNEL_MESSAGE -> GET session ABSENT (readSeq n+1) -> signature returned -> canSign() false -> click ends. Parent: prompts 1, verify 1 (200), sessions created 1 / live 1, challenge used 1.

Separation: reproduced = the above on candidate and parent. Team claim: AUTH_STATE_MACHINE.md line 11 ('A newer ordinary read invalidates a receipt by read ordering; a valid superseding read permits at most one new per-click GET') is implemented only before the challenge. Unmeasured: real browser BroadcastChannel timing. Fix direction: mirror the pre-flight rule after the prompt (accept a superseding read whose knowledge is valid ABSENT as the click's receipt, or perform the one per-click re-read before verify), or skip/defer the channel-triggered restore while a click is busy as visible() does; if the click must still end, set a notice (e.g. session-unknown/challenge-lost) so the discarded signature is not silent.

**Reproduction**

Offline fixtures (tests/auth-r7-fixtures.mjs; real AuthClient + real Worker + node:sqlite). From source/ with `npm ci --ignore-scripts`, tmp/hint.test.mjs, `node --test tmp/hint.test.mjs`; parent control `AUTH_R7_SOURCE=../baseline` over a `git archive c4f451b source` extraction.
import {setup,newAccount,provider,tab,ready,flush,rows,prompts} from '../tests/auth-r7-fixtures.mjs';
const w=setup(),A=newAccount(),b=w.browser();let release,opened;const held=new Promise(r=>release=r),open=new Promise(r=>opened=r);
const p=provider(A,{beforePrompt:async()=>{opened();await held;}});const q=tab(w,b,p);await ready(q);
const flow=q.signIn();await open; // personal_sign is open
q.channels.at(-1).message(); // sibling hint; canonical state is still signed out
await flush(20);await new Promise(r=>setTimeout(r,20));await flush(20);release();await flow;await flush(20);
console.log(rows(w).counts,prompts([p]),q.events.filter(e=>e.kind==='route'&&e.path==='/api/auth/verify').length,{phase:q.c.state.phase,notice:q.c.state.notice,session:q.c.state.session},await (await b.get('/api/auth/session')).json());
Expected (parent c4f451b measured): POST /api/auth/verify 200, sessions created 1 / live 1, challenge used 1, client signed in, prompts 1.
Actual at 7215c5d (measured): no verify request; sessions created 0; challenges 1 pending / 0 used; phase 'idle', notice null, session null; GET /api/auth/session signedIn:false; prompts 1 spent; a second click issues a new challenge and a second personal_sign.

### 5. Low: Ownership request queued behind a failing proof inherits that failure instead of re-evaluating with its own proof (pre-existing, contradicts OWNERSHIP_FRESHNESS.md serialisation rule)

`source/server/ownership.ts:228`

```
    if(pending)return pending.then(()=>this.proof(address,owners,agents,req,fresh,again));
```

State: open, not a regression (identical on public parent c4f451b). Blocker: no. It is fail-closed (503 OWNERSHIP_UNAVAILABLE, never an empty complete home), grants no authority and expands no method or header, so it is an availability defect, not an Auth/ownership invariant failure. From audit_economics 57507b65.

Mechanism (reproduced): proof() serialises per-address updates by chaining a waiting caller on the in-flight update with pending.then(onFulfilled) only. When the in-flight update rejects (a first or expired-epoch proof whose Multicall3 ownerOf eth_call failed, or a proof completing at/after its 30 s deadline, :292), the rejection propagates through .then() to every caller queued behind it. The queued caller never runs its own update(): no ownerOf RPC is attempted for it even if the node has recovered, and its own captured roster and fresh intent are not re-evaluated. This contradicts OWNERSHIP_FRESHNESS.md line 20 ('A caller waiting behind another request re-evaluates its own captured roster and fresh intent') and the stated availability design ('First/expired proof failures ... their retries remain unavailable and are bounded by existing request limiters'): the waiter is refused without any retry. The existing ownership-v11 controls queue callers only behind successful updates.

Counts (reproduced): index reads 1, ownerOf RPC 1 (the failed one), lane calls 0; first request rejects OWNERSHIP_UNAVAILABLE (correct), second (queued, node healthy) also rejects OWNERSHIP_UNAVAILABLE with no RPC of its own; a third request afterwards succeeds (eligible 1, RPC 2). Parent c4f451b: identical.

Separation: reproduced = the above. Team claim: the serialisation rule in OWNERSHIP_FRESHNESS.md is only partially implemented. Minimal fix preserving the serialisation design: chain on settlement rather than fulfilment, e.g. `return pending.then(()=>this.proof(...),()=>this.proof(...))` (or `pending.catch(()=>{}).then(()=>this.proof(...))`), so the waiter performs its own epoch evaluation and proof after the predecessor settles; a re-run still passes the same budget/lane/limiter gates, so the bounded-RPC argument is unchanged.

**Reproduction**

Offline, synthetic fixtures only. From source/ with `npm ci --ignore-scripts`, tmp/oq.test.mjs, `node --test tmp/oq.test.mjs` (same gateway/fetcher scaffold as the overlap probe, plus a hold gate and a fail flag on the eth_call):
const deferred=()=>{let resolve;return {promise:new Promise(r=>resolve=r),resolve};};const st={live:START,rpc:0,failRpc:false,holdRpc:null};
// in the eth_call branch of the fetcher: st.rpc++; const willFail=st.failRpc; if(st.holdRpc){const g=st.holdRpc;st.holdRpc=null;g.started.resolve();await g.release.promise;} if(willFail)return new Response('{}',{status:502}); ...normal aggregate3 answer...
const gate={started:deferred(),release:deferred()};st.holdRpc=gate;st.failRpc=true;
const first=o.home(A,req(START),false);await gate.started.promise; // first proof's RPC is held
const second=o.home(A,req(st.live),false); // queued behind the held first proof
st.failRpc=false; // node healthy again before the first failure is observed
gate.release.resolve();
await first.catch(e=>console.log('first',e.message)); await second.then(v=>console.log('second ok',v.eligible),e=>console.log('second',e.message,'rpc',st.rpc));
console.log('third',(await o.home(A,req(st.live),false)).eligible,'rpc',st.rpc);
Expected (OWNERSHIP_FRESHNESS.md): the queued second request performs its own proof after the first settles: RPC count 2, second request resolves with eligible 1.
Actual at 7215c5d (measured): first OWNERSHIP_UNAVAILABLE; second OWNERSHIP_UNAVAILABLE with rpc still 1 (no RPC of its own); third succeeds (eligible 1, rpc 2). Parent c4f451b: identical output.

### 6. Low: LOW-6 side effect (regression vs parent): a good world snapshot whose Worker fetchedAt is ahead of the browser clock is classified as a failed read (retry ladder, permanently 120 s for a lagging clock

`source/src/world/cadence.ts:62`

```
    if(core.some(s=>s.fetchedAt===null||!isFreshAge(now,s.fetchedAt,Number.MAX_VALUE)))return false;
```

State: policy decision with an unmeasured load/UX side effect; open. Blocker: no (not an authority issue; load and display only). Merged from audit_math c5dd4210 and audit_permissions b7888aae.

Mechanism (reproduced): worldReadResult() compares the Worker's epoch fetchedAt (server/gateway.ts:212, fetchedAt=this.now()-ageMs, Cloudflare's clock) with the browser's Date.now() through isFreshAge, which returns false for any negative age (src/shared/freshness.ts:6). A client whose wall clock is behind the stamp by more than the response latency sees a state:'fresh' sample as 'future' and worldReadResult returns false, the same value as a transport failure. startPoll() (cadence.ts:98-103) then increments failures and schedules nextDelay(false,...): 5 s, 15 s, 30 s, 60 s, then 120 s for ever, instead of REFRESH_MS=900 s after a good read, while the valid data it just received is displayed. The effect is transient when the lag is smaller than the sample's age at the next retry (one or a few extra reads) and persistent for a device whose clock lags by more than the gateway sample age (up to UPSTREAM_TTL_MS, 5 min): that client polls /api/world/snapshot every 120 s (7.5x the designed rate) for the whole session. The same comparison in marketView (market.ts:112) and floorView (market.ts:93) labels a Worker-fallback quote 'stale' (weather 'unknown', floor null) for the same skewed client. Before R8 (c4f451b cadence.ts:59) a future stamp counted as a good read ('behind'/true). FRESHNESS_BOUNDARIES.md records the intent ('invalid/future source fetchedAt cannot count as a good read') and tests/freshness-v11.test.mjs pins fetchedAt 1001 vs now 1000 => false, but neither considers that 'not good' is mapped onto the failure retry ladder rather than onto 'behind' (one bounded follow-up) or a success-for-scheduling. Clock skew of seconds on consumer devices is routine (siwe.ts allows 10 minutes of skew for the sign-in message for that reason).

Separation: reproduced = the probe below on candidate and parent. Team claim: FRESHNESS_BOUNDARIES.md policy as stated is implemented. Inference/unmeasured: the share of real visitors with negative skew; WorldApp.tsx (withheld) is assumed to feed worldReadResult into startWorldPoll as the public fixture comments describe. Fix that keeps future stamps untrusted: keep refusing to label a future-dated sample fresh, but return 'behind' (or true) for the scheduler when the samples are fresh and the only defect is a bounded negative age (e.g. up to FOLLOW_UP_MS or the SIWE skew allowance), and allow the same bounded skew for remote stamps in marketView/floorView, never rewriting the stamp.

**Reproduction**

From source/ (no fixtures needed): node --test tmp/cd.test.mjs with
const {worldReadResult,nextDelay,FIRST_RETRY_MS,REFRESH_MS,startPoll}=await import('../src/world/cadence.ts');const {marketView}=await import('../src/world/market.ts');
const now=1_000_000,s=at=>({state:'fresh',data:{seats:{}},url:'x',fetchedAt:at});
console.log(worldReadResult({swarm:s(now+1),workers:s(now)},now),worldReadResult({swarm:s(now),workers:s(now)},now)); // client 1 ms behind vs control
const delays=[];let t=now;const env={set:(fn,ms)=>{delays.push(ms);return {};},clear:()=>{},hidden:()=>false,now:()=>t,onVisible:()=>()=>{}};
const poll=startPoll(async()=>worldReadResult({swarm:s(t+2000),workers:s(t+2000)},t),env,{retryMs:FIRST_RETRY_MS}); // clock persistently 2 s behind
for(let i=0;i<7;i++){await new Promise(r=>setImmediate(r));await new Promise(r=>setImmediate(r));t+=delays.at(-1);poll.poke();}await new Promise(r=>setTimeout(r,5));console.log(delays,poll.failures,REFRESH_MS);
const T=1_000_000_000,sample={state:'fresh',url:'x',fetchedAt:T,data:{priceUsd:8,change24h:-30,priceNative:.003,pairUrl:'https://dexscreener.com/ethereum/x',provider:'DEX Screener'},extras:{floorEnabled:true,floor:{floorEth:2.5,marketplace:'OpenSea',fetchedAt:T}}};
const v=marketView(sample,T-2000);console.log(v.state,v.weather,v.floor);
Expected (parent c4f451b measured): true,true; delays [900000 x8], failures 0; market 'fresh' 'thunderstorm' floor {floorEth:2.5,floorUsd:6666.67}.
Actual at 7215c5d (measured): false,true (a 1 ms-ahead stamp is classified like a transport failure); delays [5000,15000,30000,60000,120000,120000,120000,120000], failures 8; market 'stale' 'unknown' floor null.

### 7. Info: Gateway shared-copy warm accepts a record dated up to 60 s in the future and rewrites its fetchedAt to now, contrary to the frozen freshness policy ('never synthesize a future stamp', 'reject remote f

`source/server/gateway.ts:256`

```
      const fetchedAt=Math.min(record.fetchedAt,at);
```

State: accepted limit / unchanged since the public parent (gateway.ts is not in the R8 change set); reported because the task's freshness controls require rejecting remote future timestamps without rewriting them as now and FRESHNESS_BOUNDARIES.md states 'never synthesize a future stamp'. Blocker: no. From audit_math d6cd077d.

Mechanism (reproduced): ReadGateway.warm() (gateway.ts:253-259) seeds a cold isolate from the per-colo Cache API copy written by another isolate. Line 254 tolerates age>=-60_000 (a record dated up to one minute ahead of this isolate's clock) and line 256 stores fetchedAt=Math.min(record.fetchedAt,at), re-dating a future record as read 'now', then validUntil=max(entry.validUntil,fetchedAt+ttl) gives it a full UPSTREAM_TTL_MS from this clock and labels it 'fresh' to clients and to the ownership roster read (Ownership.world() uses gateway.source('swarm')). Impact is bounded: the writer is another isolate of the same Worker in the same Cloudflare location, so the skew is Cloudflare's own inter-isolate clock skew, and the roster only names candidates (ownerOf still proves them). It is a documented-policy inconsistency rather than an authority defect, and the exact boundary (age===-60_000 accepted) is untested.

Separation: reproduced = probe below (candidate and parent identical). Unmeasured: real inter-isolate skew. Fix if the policy is to be uniform: reject age<0 as isFreshAge does elsewhere, or keep the record's own fetchedAt unmodified and let label()/servable() judge it.

**Reproduction**

From source/ (offline, injected fetch and clock): node --test tmp/gw.test.mjs with
const {ReadGateway,SHARED_SHAPE}=await import('../server/gateway.ts');let t=1_000_000;const urls=[];
const g=new ReadGateway(async u=>{urls.push(String(u));return new Response(JSON.stringify({seats:{},owners:[],count:0,workers:[]}),{status:200});},()=>t,{sharedWaitMs:50});
const shared={async get(k){return k==='swarm'?{v:1,shape:SHARED_SHAPE,key:k,data:{seats:{},owners:[],at:1},fetchedAt:t+59_000}:undefined;},async put(){}};
const s1=await g.source('swarm',undefined,shared);console.log(s1.state,s1.fetchedAt,t);t+=4*60_000;const s2=await g.source('swarm',undefined,shared);console.log(s2.state,s2.fetchedAt,t,urls.filter(u=>u.includes('/swarm')).length);
Expected under the stated policy: a shared record dated 59 s in the future is not usable as current data (ignored, or kept with its own future fetchedAt so downstream freshness gates reject it).
Actual at 7215c5d (measured): prints fresh 1000000 1000000 (accepted and re-dated to this isolate's now) and at +4 min still fresh with fetchedAt 1000000; parent c4f451b identical.

### 8. Info: Public scheduler test writes evidence artifacts outside source/ into the review repository root, embedding an absolute local path and a non-reproducible run id

`source/tests/auth-reference-scheduler.test.mjs:9`

```
const artifactRoot=resolve(import.meta.dirname,'../../evidence/reference-scheduler');
```

State: open (hygiene). Blocker: no. From audit_economics 553671b9.

The recorded public filtered-subset command (Submission7_R8Closure/TEST_RESULTS.json) includes tests/auth-reference-scheduler.test.mjs, whose save() helper (line 18) writes into resolve(import.meta.dirname,'../../evidence/reference-scheduler'), i.e. <repository>/evidence/reference-scheduler, one level above the published source/ tree. A reviewer who runs the exact recorded command from source/ ends up with untracked JSON files in the review repository root (fixed-<seed>-<kernel>.json, focused-<seed>.json, gate-<timestamp>-<uuid>-RESULT.json, LATEST.json). Each fixed/focused file embeds provenance().sourceRoot, an absolute local path, and the gate file name contains a wall-clock timestamp and random UUID, so the artifacts are not byte-reproducible and are easy to commit by accident into a package whose manifests (submission7-r8closure-published-source.json, SHA256SUMS, BOUNDARY_CHECK.json) do not cover them; TEST_RESULTS.json's sourceUnchangedDuringRun receipt only speaks for source/.

Reproduced fact: after the recorded command in a scratch copy of source/, the sibling directory evidence/reference-scheduler held 18 JSON files (13 fixed-*, 3 focused-*, 1 gate-*-RESULT.json, LATEST.json) and fixed-0-lost-hint.json contains "sourceRoot": "<absolute path of the machine that ran it>". Minimal fix: write artifacts under a path inside source/ that .gitignore already excludes (source/.gitignore ignores tmp/), or honour an explicit output environment variable and skip persistence when it is unset; record the artifact location in TEST_RESULTS.json if artifacts are meant to be part of the receipt.

**Reproduction**

From a clean checkout of commit 7215c5d: `cd source && npm ci --ignore-scripts && node --test --test-reporter=tap --test-concurrency=3 tests/auth-reference-scheduler.test.mjs` then `cd .. && git status --short && ls evidence/reference-scheduler | wc -l && grep -o '"sourceRoot": "[^"]*"' evidence/reference-scheduler/fixed-0-lost-hint.json`.
Expected: no files created outside source/ (or only under an ignored path).
Actual (measured on a scratch copy): the directory evidence/reference-scheduler is created beside source/ with 18 JSON files, the fixed/focused files carry the absolute sourceRoot of the running machine, and the gate RESULT file name carries a timestamp and UUID; in the repository this appears as `?? evidence/` in git status.

---

Judge's submission `29cb6677d8353bccc33f288d1e6489354d49c953c9a0d67abba57655f1c5ce0f`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
