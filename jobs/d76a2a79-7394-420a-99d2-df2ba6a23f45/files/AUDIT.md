# Audit report

> IMD Ember World — ninth offline audit / closure of the latest Audit8 findings (World / Member M1 only).
>
> Question: Does this exact candidate close the three Low and two Info findings from the latest eighth Audit, with bounded regression evidence? Seek new or reopened findings of any severity; do not promise a pass or zero findings.
> Period: latest Audit8 through the source-freeze and release measurement timestamps in this pinned snapshot, as of 2026-10-05. Length/format: Markdown finding table, precise reproductions and unlimited evidence appendix; preserve code, hashes and URLs.
>
> Exact public snapshot: https://github.com/tungweb3/imd-ember-world-review/tree/347268a7ecae700088547c2402db9a3eb07a6fd2
> Previous public: 88c130283efc45260f9e00da8d2d3055c38483bd
> Private source provenance: 8c3b60171a22b3ce71854f12282e629bbf5ca06f (not a public checkout URL).
> TEAM measured current Worker: 06cbc8fe-112f-4a11-b84f-42907179afff, 100% traffic; record 20261005T011008Z-8c3b601.
>
> Read Submission9/README.md, REVIEW_INPUTS.md, PRIOR_REVIEWS.md, FinalClosure/ closure/test/artifact/build/served/reviewer evidence, SERVED_EXPECTATIONS.json and manifests/submission9-published-source.json. Use this exact pin; older namespaces are historical.
>
> Unofficial TypeScript Cloudflare Worker/React SIWE; NO SOLIDITY. M1 writes persistent profiles. Scope Auth/server authority, ownership/index/budget/freshness and artifact/runner. Exclude Genesis/Mint, Ember Coin, Fren Pet, full 3D/scene/media/avatar/selfie and private backups. Public141 sources:125exact,16redacted/57masked lines; no private Git/full frontend. Unavailable full compilation is not a pass.
>
> Offline/local synthetic tests only. Public source/prior-document GETs and fresh dependency downloads are permitted. No live site/API tests or writes, real wallet signatures/logins, approvals, transfers, minting, payments, job submissions or deployments. Never request owner credentials/private databases.
>
> Fresh public checkout, Node 24.x, then in source/: npm ci --ignore-scripts; node scripts/review-tests.mjs --check; npm run test:review; node scripts/verify-artifact-closure.mjs. Use real locked viem 2.56.9 and all 23 selected test files. No missing-module stubs, private source selectors, substitute crypto/Worker/SQLite, omitted failing files, hidden skips or leaked outputs. Windows file-symlink controls require real capability; report actual environmental failures honestly. Artifact default creates no saved scheduler output; opt-in sanitized artifacts remain under the explicit private source/tmp policy.
>
> TEAM final exact-source measurements: Node 24.19.0; private full 1663/1663, supported runner on private source 613/613, fresh clean private-source checkout 613/613, real filesystem artifact suite 18/18, standalone and clean verifiers 13/13; all acceptance runs have zero fail/cancel/skip/todo. These are NOT a direct runtime rerun of the filtered public-byte checkout; selected-source correspondence is verified separately. Independently run the public runner. Historical failures and vulnerable-baseline expected exit 1 remain in TEST_RESULTS.json. Core 500 campaigns /428 distinct digests and additional 90 /54 are separate identities, not 590 unique proof cases or exhaustive state-machine proof.
>
> Latest Audit8 job7716c3f5-5d6c-4953-a643-141da678d051 reviewed public88c130..., completed2026-10-04T19:26:33.961Z, published19:26:58Z. Immutable original: https://github.com/Identity-md/research/blob/d7f6e26bf449d9c5ea3a1ecb6557ca3adbd23632/jobs/7716c3f5-5d6c-4953-a643-141da678d051/files/AUDIT.md ; SHA2568c9baaa6838e8b0137baa44282d1fcc2704834d68c92dafcd4426a882905bcfc. Earlier Report8 job38438c89-b34c-4d38-8ae8-027c9d175fb1 completed19:13:53.530Z and does not supersede the later Audit.
>
> Review the five mechanisms hardest, including reverse controls:
> 1. Post-D1 ownership proof expiry: strict proof age must be rechecked after all awaits. Test29999/30000/30001ms, sold seat, enrichment delay, refused/failed refresh lane, rollback/NaN/Infinity and latest recovery. Expired/unavailable is not complete-empty/not-owned authority. Do not extend producer checkedAt or renew authority on same-block deltas.
> 2. First locked-provider account event: CookieA + provider[] + first accountsChanged(B), without actual observedA, must not revoke sessionA. Cookie identity is not an earlier wallet observation. Genuine observedA-toB, A-lock-B, explicit selection/grant, passive replacement after observedA, restart/stop and delayed cleanup must retain correct context/nonce/address fencing.
> 3. Slow fresh overlap: twenty early joined same-context fresh requests with four pages at7475/7500ms share one admitted cycle/four pages/one budget/one proof/one epoch while that proof remains fresh. Different/late intent or changed roster re-evaluates after success/failure. Preserve strict proof TTL, original producer/index timestamp, bounded failure and later retry. This is not a global RPC ceiling or cross-isolate lock.
> 4. Dangling artifact final-link escape: exercise actual dangling/existing final file links, directory links, nonregular targets, parent/target substitution and safe hardlink replacement. No outside-root writes. Review lstat identities, exclusive regular sibling temp, fsync and validated replacement. Respect documented locally controlled private-root assumption; portable Node does not prove hostile concurrent ancestry-swap or SMB/NFS safety.
> 5. General diagnostic path redaction: actual persisted nested strings must mask arbitrary POSIX, Windows, UNC and file URLs, including spaces/parentheses, C://, D:/// and rooted backslash forms. Preserve network URLs, relative identifiers, structured actions/events/nonces and actual saved-trace replay. Assess conservative same-line masking policy without treating deliberately synthetic test paths as machine leaks.
>
> Only authenticated-address ownerOf grants ownership; index/roster/D1/name are candidates. Keep original Auth lifecycle cleanup and strict authority boundaries, retained verify/lock503/later-valid controls, nonce ownership, one primary cleanup plan per event and no old-flow cross-revocation. Do not infer production concurrency or real-wallet correctness from offline client/Worker/SQLite fixtures.
>
> For every finding give severity, blocker rationale, pinned location/prior link, exact event order, actual relevant database rows, prompt/challenge/verify/logout/hint/index/budget/RPC counts, reproduction/exit/hash or argument, fixed/partial/open/accepted limit/policy/unknown and what could not be checked. Separate fresh REVIEWER measurements, TEAM observations, inherited historical evidence, inference and unknowns.
>
> Request separate SOURCE-CLOSURE PASS/BLOCKED/UNKNOWN and RELEASE-READINESS PASS/BLOCKED/UNKNOWN verdicts. Production upload/build/record persistence and verification are distinct. Current stage-separated deployment consumed exact prior privileged local full-suite receipts; canonical npm run deploy was NOT invoked. The older canonical overall exit1 after successful upload remains historical. Deployment evidence is TEAM readback, not your authenticated production measurement. Completed/accepted and Low/Info labels do not certify approval, endorsement, zero vulnerabilities or fund safety.

| | |
|---|---|
| Repository | https://github.com/tungweb3/imd-ember-world-review.git |
| Commit | `347268a7ecae700088547c2402db9a3eb07a6fd2` |
| Job | `d76a2a79-7394-420a-99d2-df2ba6a23f45` |
| Judged | 2026-10-05 04:30 UTC |
| Findings | 3 low · 2 info |

Four agents audited the code as it is at `347268a`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Post-await household eligibility uses request-start time and counts sightings older than 24 hours

`source/server/ownership.ts:355`

```
    const seats=proof.ids.map(id=>this.status(id,world.agents.get(id),seen.get(id),req.now)),eligible=seats.filter(s=>s.counts).length;
```

OPEN new scoped temporal counterexample adjacent to latest Audit8 #1 (https://github.com/Identity-md/research/blob/d7f6e26bf449d9c5ea3a1ecb6557ca3adbd23632/jobs/7716c3f5-5d6c-4953-a643-141da678d051/files/AUDIT.md). The strict 30-second proof recheck at line 354 fixes the prior sold-seat reproduction, but the final eligibility computation and the no-eligible-seat lane predicate at line 349 still use req.now from before awaits. A registered offline seat whose owner-specific D1 sighting expires during enrichment still grants eligible=1/size=s. Low: inaccurate household authority; no forged ownerOf, asset transfer or unauthorized M1 mutation demonstrated. SOURCE-CLOSURE blocker for current eligibility. Evaluate the final counting/lane predicate at the live post-wait clock while preserving the inclusive 24-hour comparator and original proof/index timestamps. This is scoped pre-existing behavior, not asserted to have been introduced by this patch. Independently reproduced on public 347268a7ecae700088547c2402db9a3eb07a6fd2, Linux Node v24.21.0, real locked viem 2.56.9, actual Worker and migration-backed node:sqlite; production D1 timing, full frontend and real wallets remain unmeasured. Exact source SHA256: db7c60509de363c925c938c44ba7e40721a1271f6e558e62e2022abbb2b3c317. The immutable prior Audit8 document was independently fetched: 32883 bytes, SHA256 8c9baaa6838e8b0137baa44282d1fcc2704834d68c92dafcd4426a882905bcfc.

**Reproduction**

From source/ in a fresh exact public checkout, after npm ci --ignore-scripts, run the JavaScript below with node --input-type=module on stdin. REVIEWER exit 1 at the final expected-behavior assertion (actual 1, expected 0); earlier assertions verify the boundary controls. Request starts t=1790596800000 with seat 7/agent707 offline, ownerOf=A, last_online_at=t-86400000+1. Delay the real sightings read by advancing the injected clock 2ms. Actual HTTP200/eligible1/counts=true/size=s at sighting age86400001ms, with proof age2ms and checkedAt=t/block21000000. Immediate second request returns eligible0 without another index/budget/RPC. Delays0/1/2/5000ms yield ages86399999/86400000/86400001/86404999, first eligible1/1/1/1 and next1/1/0/0. Each run has setup challenge/verify1/1; home2; prompt/logout/hint0/0/0; index/budget/ownerOf eth_call1/1/1 and no eth_getCode. Actual 2ms SQLite rows: seat_presence=(7,0x19e7e376e7c213b7e7e7e46cc70a5dd086daff2a,1790510400001,1790510400001); session nonce=c4f58a8e817fd3b8cbc4dfa8e5e5e118,address=A,expires_at=1791201600000,revoked_at=NULL; matching challenge used_at=1790596800000,invalidated_at=NULL. Counts created/live/revoked1/1/0; challenges total/used/pending/invalidated1/1/0/0. Nonces vary on rerun. No member writes.

import assert from 'node:assert/strict';
import {privateKeyToAccount} from 'viem/accounts';
import {setup,fakeChain,fakeImd,rows} from './tests/auth-r7-fixtures.mjs';
const A=privateKeyToAccount('0x'+'11'.repeat(32)),a=A.address.toLowerCase();
const observed=[];
for(const delay of [0,1,2,5000]){
  const owners=[];owners[7]=a;
  const w=setup({chain:fakeChain({owners:{7:a}}),imd:fakeImd({seats:{7:'707'},owners,online:[]})}),b=w.browser();
  let budget=0;w.env.CHAIN_LIMITER={limit:async({key})=>{if(key==='chain:index')budget++;return {success:true};}};
  assert.equal((await b.signIn(A)).verify.status,200);
  const t=w.clock.now(),seen=t-86400000+1;
  w.db.raw.prepare('INSERT INTO seat_presence(token_id,owner,last_online_at,updated_at) VALUES(7,?,?,?)').run(a,seen,seen);
  const prepare=w.db.prepare.bind(w.db);let once=true;
  w.db.prepare=sql=>{const wrap=s=>({...s,bind:(...args)=>wrap(s.bind(...args)),all:async()=>{
    if(once&&sql.startsWith('SELECT token_id,last_online_at')){once=false;w.clock.advance(delay);}return s.all();
  }});return wrap(prepare(sql));};
  const response=await b.get('/api/me/home'),home=await response.json();
  const next=await(await b.get('/api/me/home')).json();
  const result={delay,http:response.status,now:w.clock.now(),sightingAge:w.clock.now()-seen,home,next,
    rows:rows(w),presence:w.db.raw.prepare('SELECT * FROM seat_presence').all(),
    counts:{setupChallenge:1,setupVerify:1,home:2,prompt:0,logout:0,hint:0,
      index:w.chain.state.calls.filter(c=>!c.body).length,budget,rpc:w.chain.state.calls.filter(c=>c.body).length},
    rpcMethods:w.chain.state.calls.filter(c=>c.body).map(c=>JSON.parse(c.body).method)};
  console.log(JSON.stringify(result));observed.push(result);
  assert.equal(home.eligible,1);assert.equal(next.eligible,delay<=1?1:0);
  assert.equal(home.checkedAt,t);assert.equal(budget,1);
}
assert.equal(observed[2].home.eligible,0,'offline sighting older than 24h must not count after D1 await');


Reproduction JavaScript SHA256 (UTF-8 including final newline): 4e684e1f923761730153a3354954c00f810297dddf655632be4024489fad1634.

### 2. Low: Restarted AuthClient retains a prior wallet account instead of its current eth_accounts reply

`source/src/world/auth.ts:290`

```
      }else if(a){this.observedAccount=a;if(!this.s.account){this.lifecycle.discovered(p,a);this.set({account:a});}}
```

OPEN, merged duplicate restart claims from math/economics/permissions/flow. Related to latest Audit8 #2 (https://github.com/Identity-md/research/blob/d7f6e26bf449d9c5ea3a1ecb6557ca3adbd23632/jobs/7716c3f5-5d6c-4953-a643-141da678d051/files/AUDIT.md). start()/stop() reset observedAccount but preserve s.account. The non-discovery bind reply records B internally but only updates the public/lifecycle account when the old public account is falsy; an empty reply is ignored. After observing A, stopping, changing to B while unsubscribed and restarting the same instance, account remains A and statusOf/ownerAddress reports owner for cookie A. An explicit signIn takes the stale same-session fast path. A fresh instance correctly shows B/mismatch and preserves A. Low: incorrect wallet context/owner UI, no server authentication bypass, funds or unauthorized profile mutation demonstrated. SOURCE-CLOSURE blocker for requested restart/context controls. Reconcile public/lifecycle account with the first fenced reply of each lifetime, including empty replies, without deriving automatic logout authority from cookie/prior-lifetime A. Preserve binds/accountEvents and nonce cleanup fences. Existing auth-audit8.test.mjs same-client-restart emits an extra accountsChanged([]) after restart, masking the missing initial update. This scoped behavior predates the patch. REVIEWER Linux Node v24.21.0/viem2.56.9/actual AuthClient, Worker and SQLite at public347268a7ecae700088547c2402db9a3eb07a6fd2; actual production React remount/browser/provider scheduling is unknown. Independently reproduced a second consequence of the same split identity: after another context installs cookie B while stopped, restart observes B internally but leaves public A; a subsequent genuine B-to-A event returns at accountChanged line584 (a===s.account), suppressing B's required conditional cleanup. This is merged here because reconciling the binding account fixes both symptoms. Exact source SHA256: e8b6b2433fb2b8bc64f4ec8e03a2c5049d02cba42ea15ff5556a923846d12829. The immutable prior Audit8 document was independently fetched: 32883 bytes, SHA256 8c9baaa6838e8b0137baa44282d1fcc2704834d68c92dafcd4426a882905bcfc.

**Reproduction**

Run the following stdin with node --input-type=module from source/ after fresh locked npm ci --ignore-scripts. REVIEWER exit1: expected B, actual A. Order: local A login; observe A/seat7 owner; stop; switch provider B; restart same instance; await its eth_accounts(B)/cookie restoration; explicit signIn. Actual A/owner before and after click; fresh-client control B/mismatch. With provider locked while stopped, restarted account likewise remains A instead of null. Actual B-case before/after SQLite session=(noncec66d01ab1e646725c8f7a0c7dcdcfbb8,address0x19e7e376e7c213b7e7e7e46cc70a5dd086daff2a,expires_at1791201600000,revoked_atNULL), challenge=(same nonce,used_at1790596800000,invalidated_atNULL). Created/live/revoked1/1/0 and challenges total/used/pending/invalidated1/1/0/0 remain unchanged. Setup challenge/verify1/1. Measured client prompt/connect/challenge/verify/logout/broadcast0/0/0/0/0/0; sessionGET3/homeGET2 after click; hint writes2 at restart,3 including click; index/budget/ownerOfRPC1/1/1. The locked variant has sessionGET2/homeGET1/hint writes2, otherwise same counts. Cleanup plan stop:none. Synthetic identities only; no member writes.

import assert from 'node:assert/strict';
import {privateKeyToAccount} from 'viem/accounts';
import {setup,provider,tab,ready,until,flush,rows,logouts,prompts,routeEvents,fakeImd,fakeChain,statusOf} from './tests/auth-r7-fixtures.mjs';
const A=privateKeyToAccount('0x'+'11'.repeat(32)),B=privateKeyToAccount('0x'+'22'.repeat(32));
const a=A.address.toLowerCase(),bb=B.address.toLowerCase(),results=[];
for(const next of [B,null]){
 const owners=[];owners[7]=a;
 const w=setup({chain:fakeChain({owners:{7:a}}),imd:fakeImd({seats:{7:'707'},owners,online:[7]})}),b=w.browser(),p=provider(A);
 let budget=0;w.env.CHAIN_LIMITER={limit:async({key})=>{if(key==='chain:index')budget++;return {success:true};}};
 assert.equal((await b.signIn(A)).verify.status,200);
 const q=tab(w,b,p);let hintWrites=0;const set=q.c.deps.hint.set;q.c.deps.hint.set=v=>{hintWrites++;set(v);};
 try{
  await ready(q);assert.equal(statusOf(q.c.state,w.clock.now()),'owner');
  const before=rows(w);q.stop();p.switchTo(next);q.restart();await until(()=>routeEvents(q,'/api/auth/session').filter(e=>e.finished).length===2&&!q.c.state.checking);await flush();
  const restored={account:q.c.state.account,session:q.c.state.session?.address,status:statusOf(q.c.state,w.clock.now())};
  const hintsAtRestart=hintWrites;
  if(next){await q.signIn();await flush(20);}
  const counts={setupChallenge:1,setupVerify:1,prompt:prompts([p]),connect:p.calls.filter(x=>x==='eth_requestAccounts').length,
   session:routeEvents(q,'/api/auth/session').length,home:q.events.filter(e=>e.kind==='route'&&e.path.startsWith('/api/me/home')).length,
   challenge:routeEvents(q,'/api/auth/challenge').length,verify:routeEvents(q,'/api/auth/verify').length,
   logout:logouts(q).length,broadcast:q.channels.flatMap(c=>c.messages).length,hintWrites,hintsAtRestart,
   index:w.chain.state.calls.filter(c=>!c.body).length,budget,rpc:w.chain.state.calls.filter(c=>c.body).length};
  const fresh=tab(w,b,p);await until(()=>fresh.c.state.restored&&!fresh.c.state.checking);await flush();
  const control={account:fresh.c.state.account,status:statusOf(fresh.c.state,w.clock.now())};fresh.stop();
  assert.equal(control.account,next?bb:null);if(next)assert.equal(control.status,'mismatch');
  assert.deepEqual(rows(w),before);assert.equal(logouts(q).length,0);
  const result={provider:next?bb:null,before,after:rows(w),restored,afterClick:statusOf(q.c.state,w.clock.now()),counts,control,plans:q.c.lifecycleSnapshot.cleanupPlans};
  results.push(result);console.log(JSON.stringify(result));
 }finally{q.stop();}
}
assert.equal(results[0].restored.account,bb,'restart must adopt the current binding account');
assert.equal(results[0].restored.status,'mismatch');
assert.equal(results[1].restored.account,null);


Additional merged cleanup reproduction (same environment, node --input-type=module stdin

### 3. Low: A stopped lifetime's retained verify owner authorizes revocation on the new lifetime's first wallet observation

`source/src/world/auth.ts:589`

```
    const other=!!a&&!!this.s.session&&this.s.session.address!==a&&(wasFlow||changed);
```

PARTIAL/REOPENED latest Audit8 #2 (https://github.com/Identity-md/research/blob/d7f6e26bf449d9c5ea3a1ecb6557ca3adbd23632/jobs/7716c3f5-5d6c-4953-a643-141da678d051/files/AUDIT.md). wasFlow at line587 treats every retained owner as current account-change intent, including detached cleanup from a stopped lifetime. After cookie A is restored with no observed account in the restarted lifetime, first accountsChanged(C) acquires displayed-session cleanup authority from the old B owner. planCleanup then prioritizes displayed A and sends expectedAddress=A, revoking A instead of preserving it as mismatch. The Worker correctly enforces the assertion; the client should not issue it. This reproduces with public account=null before the event, independent of the separate stale-account finding. Low: unintended logout/old-flow cross-context authority, no signature bypass or fund loss demonstrated. SOURCE-CLOSURE blocker under the specified no-old-flow-cross-revocation requirement. Separate current lifetime/click switch authority from old retained nonce-cleanup responsibility, retaining B's conditional cleanup and binding/generation guards. Fresh REVIEWER Linux Nodev24.21.0, real locked viem2.56.9, actual AuthClient/Worker/node:sqlite at public347268a7ecae700088547c2402db9a3eb07a6fd2; real extension/browser/D1/production scheduling remains unknown. Exact source SHA256: e8b6b2433fb2b8bc64f4ec8e03a2c5049d02cba42ea15ff5556a923846d12829. The immutable prior Audit8 document was independently fetched: 32883 bytes, SHA256 8c9baaa6838e8b0137baa44282d1fcc2704834d68c92dafcd4426a882905bcfc.

**Reproduction**

From source/ of the fresh pin after npm ci --ignore-scripts, run the following stdin with node --input-type=module. REVIEWER exit1 at expected A.revoked_at=NULL, actual1790596800000; a no-event control passes. Order: client B verify commits and sets cookie B but its fetch result is held; lock; stop, holding nonce-B cleanup before Worker execution; direct local other-context A login sets the shared cookie; restart with eth_accounts=[]; canonical A/home complete with account=null; deliver first accountsChanged(C). Expected preserve A/mismatch, no new logout/hint, B cleanup remains nonce-specific. Actual new expectedAddress=A logout204 with cookie clear, signed-out broadcast, A row revoked. Event-case actual rows before/after: B=(nonce dd435a8374693913f7e1f63e0c9f1401,address0x1563915e194d8cfba1943570603f7606a3115508,expires_at1791201600000,revoked_atNULL unchanged); A=(nonce0c89a82516064a909f02854db4035d41,address0x19e7e376e7c213b7e7e7e46cc70a5dd086daff2a,expires_at1791201600000,revoked_atNULL ->1790596800000). Both challenges retain used_at1790596800000/invalidated_atNULL. Sessions created/live/revoked2/2/0 ->2/1/1; challenges total/used/pending/invalidated2/2/0/0 unchanged. Before releasing old gates: prompt/client challenge/client verify1/1/1 plus direct A challenge/verify1/1; sessionGET3/homeGET1; logout2 (old pending nonce+new completed address) versus control1; broadcasts1 versus0; hint writes2 versus1; index/budget/RPC1/1/0, event adds none. No M1 rows touched. All identities/signatures are offline synthetic.

import assert from 'node:assert/strict';
import {privateKeyToAccount} from 'viem/accounts';
import {setup,provider,tab,ready,defer,until,flush,rows,logouts,prompts,routeEvents} from './tests/auth-r7-fixtures.mjs';
const A=privateKeyToAccount('0x'+'11'.repeat(32)),B=privateKeyToAccount('0x'+'22'.repeat(32)),C=privateKeyToAccount('0x'+'33'.repeat(32));
const results=[];
for(const emit of [false,true]){
 const w=setup(),b=w.browser(),p=provider(B),v=defer(),d=defer();let committed=false,held=false,budget=0;
 w.env.CHAIN_LIMITER={limit:async({key})=>{if(key==='chain:index')budget++;return {success:true};}};
 const q=tab(w,b,p,{beforeSend:async(path,init)=>{
   if(path==='/api/auth/logout'&&JSON.parse(init.body).expectedNonce){held=true;await d.promise;}
  },intercept:async(path,r)=>{if(path==='/api/auth/verify'){committed=true;await v.promise;}return r;}});
 let hintWrites=0;const set=q.c.deps.hint.set;q.c.deps.hint.set=x=>{hintWrites++;set(x);};
 await ready(q);const flow=q.signIn();await until(()=>committed);
 p.switchTo(null);q.stop();await until(()=>held);
 assert.equal((await b.signIn(A)).verify.status,200);
 q.restart();await until(()=>q.c.state.session?.address===A.address.toLowerCase()&&!q.c.state.checking);
 assert.equal(q.c.state.account,null);
 const before=rows(w),chainBefore=w.chain.state.calls.length,hintsBefore=hintWrites;
 if(emit){p.switchTo(C);await until(()=>logouts(q).some(e=>e.addressAssertion&&e.finished));}
 await flush(30);
 const after=rows(w),a=after.sessions.find(s=>s.address===A.address.toLowerCase());
 assert.equal(a.revoked_at,emit?w.clock.now():null);
 assert.equal(logouts(q).filter(e=>e.addressAssertion).length,emit?1:0);
 assert.equal(w.chain.state.calls.length,chainBefore);
 const result={emit,before,after,client:{account:q.c.state.account,session:q.c.state.session?.address??null},
  counts:{prompt:prompts([p]),challenge:routeEvents(q,'/api/auth/challenge').length,verify:routeEvents(q,'/api/auth/verify').length,
   directChallenge:1,directVerify:1,logout:logouts(q).length,hintWrites,hintsBefore,
   session:routeEvents(q,'/api/auth/session').length,home:q.events.filter(e=>e.kind==='route'&&e.path.startsWith('/api/me/home')).length,
   budget,index:w.chain.state.calls.filter(c=>!c.body).length,rpc:w.chain.state.calls.filter(c=>c.body).length},
  logout:logouts(q).map(({assertedNonce,...e})=>e),broadcast:q.channels.flatMap(c=>c.messages),plans:q.c.lifecycleSnapshot.cleanupPlans};
 console.

### 4. Info: Replay CLI minimization bypasses the artifact store and follows a dangling output symlink

`source/scripts/replay-auth-trace.mjs:13`

```
    const minimized=await (audit8?minimizeAudit8Failure:minimizeFailure)(error.schedulerTrace??trace,error.invariant);writeFileSync(out,JSON.stringify(sanitizeArtifact({invariant:error.invariant,trace:minimized}),null,2)+'\n');}
```

OPEN additional sink counterexample related to latest Audit8 #4 (https://github.com/Identity-md/research/blob/d7f6e26bf449d9c5ea3a1ecb6557ca3adbd23632/jobs/7716c3f5-5d6c-4953-a643-141da678d051/files/AUDIT.md). createArtifactStore now rejects dangling/existing final links, but the supported replay CLI imports only its sanitizer and writes --minimize directly with writeFileSync(out,...). A preplanted dangling minimized-output symlink is followed and its outside target created. This bypasses final-entry validation, source/tmp containment, exclusive sibling temp/fsync and validated replacement. Info: local opt-in artifact hygiene, not a remote Worker/wallet exploit; default scheduler persistence remains disabled. SOURCE-CLOSURE blocker for complete artifact/runner containment. Use the validated artifact-store writer for CLI minimization, preserving separate replay input and rejecting nonregular/linked outputs. Assumes the same pre-existing link case as Audit8; no hostile concurrent ancestry-swap or SMB/NFS claim. Fresh REVIEWER real Linux file-symlink reproduction, Nodev24.21.0/locked viem2.56.9 at public347268a7ecae700088547c2402db9a3eb07a6fd2. All physical probe files remain beneath the actual checkout source/tmp and are removed; a nested synthetic source models the prohibited destination. Exact source SHA256: 6559bd435d66d275dbea845fd14ef1cd20ab75a30aa2fd9c185843442c2888db. The immutable prior Audit8 document was independently fetched: 32883 bytes, SHA256 8c9baaa6838e8b0137baa44282d1fcc2704834d68c92dafcd4426a882905bcfc.

**Reproduction**

After fresh locked npm ci --ignore-scripts, run the following via node --input-type=module stdin from source/. REVIEWER outer exit1 at expected outside-target-absent assertion; replay child exit1 is the deliberately triggered HARNESS-CAUSAL invariant, not an environmental failure. Generate real runSeed(0) trace (46 actions/10 Worker calls); append duplicate completed worker action (47 actions) to reach failure/minimization; save original through real store. In synthetic source S, preplant S/tmp/store/core500-failure-minimized.json -> S/outside.json, target absent. Same createArtifactStore rejects it with 'not a regular file'. CLI --replay S/tmp/store/core500-failure-original.json --minimize S/tmp/store/core500-failure-minimized.json creates S/outside.json and leaves output symlink intact. Saved invariant HARNESS-CAUSAL; minimization.reproduced=true,attempts14,invalid5,originalEvents47. Measured saved bytes SHA256683ba5e0d06c1c86ee74dbe1dfcc357010d271a72282d922e058550f594c2b2d. Expected reject link without target write. This intentionally invalid trace establishes sink reachability, not an Auth regression. Filesystem mechanism has no database authority or prompt/challenge/verify/logout/hint/index/budget/RPC requests; replay internally uses fresh synthetic Worker/SQLite fixtures (10 Worker calls in original trace), no persistent M1/production rows, and those internal route counts do not establish this filesystem defect. No naturally occurring Auth failure or Windows-specific CLI exploit measured.

import assert from 'node:assert/strict';
import {mkdirSync,mkdtempSync,symlinkSync,readFileSync,existsSync,lstatSync,rmSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {runSeed} from './tests/auth-scheduler-driver.mjs';
import {createArtifactStore} from './tests/auth-artifacts.mjs';
mkdirSync('tmp',{recursive:true});const root=mkdtempSync(resolve('tmp/reviewer-replay-'));let escaped;
try{
 const trace=await runSeed(0,{retainTrace:true});assert.ok(trace.metrics.workerCalls>=2);
 trace.actions.push({type:'worker',id:trace.actions.find(a=>a.type==='worker').id});
 const store=createArtifactStore({sourceDir:root,requestedDir:'tmp/store'});
 store.write('core500-failure-original.json',{trace});
 const input=join(store.directory,'core500-failure-original.json'),out=join(store.directory,'core500-failure-minimized.json'),outside=join(root,'outside.json');
 symlinkSync(outside,out,'file');assert.equal(existsSync(outside),false);
 assert.throws(()=>store.write('core500-failure-minimized.json',{}),/not a regular file/);
 const cli=spawnSync(process.execPath,['scripts/replay-auth-trace.mjs','--replay',input,'--minimize',out],{encoding:'utf8'});
 assert.equal(cli.status,1);escaped=existsSync(outside);assert.equal(escaped,true);assert.ok(lstatSync(out).isSymbolicLink());
 const bytes=readFileSync(outside),saved=JSON.parse(bytes);
 console.log(JSON.stringify({exit:cli.status,stderr:cli.stderr.trim(),createdOutsideConfiguredStore:escaped,outputStillSymlink:true,
  invariant:saved.invariant,workerCalls:trace.metrics.workerCalls,actions:trace.actions.length,minimized:saved.trace.minimization,
  savedSha256:createHash('sha256').update(bytes).digest('hex')}));
}finally{rmSync(root,{recursive:true,force:true});}
assert.equal(escaped,false,'minimization must reject a dangling final link without creating its outside target');


Reproduction JavaScript SHA256 (UTF-8 including final newline): 42470cc0493f2a290d3744912a48c1e79e38f14ceb197f4805fdb33ac00c66d5.

### 5. Info: Route-prefix exemptions leave absolute filenames unmasked in persisted diagnostics

`source/tests/auth-artifacts.mjs:15`

```
    const route=[...routeIds].find(id=>chunk.startsWith(id,match.index)&&/^(?:$|[\s.,;|)"'<>])/.test(chunk.slice(match.index+id.length)));
```

PARTIAL/OPEN latest Audit8 #5 (https://github.com/Identity-md/research/blob/d7f6e26bf449d9c5ea3a1ecb6557ca3adbd23632/jobs/7716c3f5-5d6c-4953-a643-141da678d051/files/AUDIT.md). The bare-path route exception accepts a route prefix followed by a dot, so absolute filenames such as /api/auth/session.log survive nested persisted diagnostics although they are not routeIds. The general arbitrary-root path-redaction guarantee is incomplete. Info: opt-in local artifact hygiene only; these deliberately synthetic filenames are not evidence of actual machine-data disclosure or an Auth bypass. Restrict exemptions to exact/unambiguous complete route identifiers, preserving exact route IDs, network URLs, relative identifiers and replay structure. SOURCE-CLOSURE blocker for complete redaction closure, separate from filesystem containment. Fresh REVIEWER Linux Nodev24.21.0 measurement against public347268a7ecae700088547c2402db9a3eb07a6fd2; module SHA25669b9d2023fde69ec2b2b1719c721f0f99d5b0d7274aef5a548d75a96ec2fe2d7. Supplied suite613/613 and verifier13/13 still pass. Windows runtime and naturally emitted production diagnostics are unmeasured; conservative same-line masking itself is an accepted documented policy. Exact source SHA256: 69b9d2023fde69ec2b2b1719c721f0f99d5b0d7274aef5a548d75a96ec2fe2d7. The immutable prior Audit8 document was independently fetched: 32883 bytes, SHA256 8c9baaa6838e8b0137baa44282d1fcc2704834d68c92dafcd4426a882905bcfc.

**Reproduction**

Run the following with node --input-type=module on stdin from source/ after fresh locked npm ci --ignore-scripts. REVIEWER exit1 at the expected masked-message assertion. createArtifactStore persists nested 'Cannot read /api/auth/session.log', 'Error at /api/auth/verify.backup', and 'Error at /api/me/home.private.json' verbatim. Expected all three absolute filenames masked; actual unchanged. Control /var/private/session.log masks to [local-path]; exact /api/auth/session, https://example.com/root/project.ts, tests/auth-artifacts.test.mjs, structured action start/tab a and nonce n1 survive. Persisted JSON SHA256372f303933cdb0b337824d911a3215eb44cb0364e86e532b1b99b844e2b75c24. Actual file is read back before deletion under a synthetic source/tmp root. No outside-root writes; no database rows; prompt/challenge/verify/logout/hint/index/budget/RPC all0.

import assert from 'node:assert/strict';
import {mkdirSync,readFileSync,rmSync,existsSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {createHash} from 'node:crypto';
import {createArtifactStore} from './tests/auth-artifacts.mjs';
const root=resolve('tmp/reviewer-route-prefix');assert.equal(existsSync(root),false);mkdirSync(root,{recursive:true});
let saved;
try{
 const store=createArtifactStore({sourceDir:root,requestedDir:'tmp/artifacts'});
 const input={nested:{message:'Cannot read /api/auth/session.log',errors:['Error at /api/auth/verify.backup','Error at /api/me/home.private.json']},
  control:'Cannot read /var/private/session.log',route:'/api/auth/session',relative:'tests/auth-artifacts.test.mjs',
  url:'https://example.com/root/project.ts',trace:{actions:[{type:'start',tab:'a'}],nonce:'n1'}};
 store.write('core500-RESULT.json',input);
 const bytes=readFileSync(join(store.directory,'core500-RESULT.json'));saved=JSON.parse(bytes);
 assert.equal(saved.nested.message,input.nested.message);assert.deepEqual(saved.nested.errors,input.nested.errors);
 assert.equal(saved.control,'Cannot read [local-path]');assert.equal(saved.route,input.route);
 assert.equal(saved.url,input.url);assert.equal(saved.relative,input.relative);assert.deepEqual(saved.trace,input.trace);
 console.log(JSON.stringify({saved,sha256:createHash('sha256').update(bytes).digest('hex'),noOutsideWrite:true}));
}finally{rmSync(root,{recursive:true,force:true});}
assert.equal(saved.nested.message,'Cannot read [local-path]','route-prefix filenames must be masked');


Reproduction JavaScript SHA256 (UTF-8 including final newline): 628b43ae42b5fb454ee28051d2b288d9dba48aa4b21a920616fc1fd3dc97ad4d.

---

Judge's submission `73463325b9200243ae7bc76d4ee79e7ee7d478a7b98a33f740762078451ecf87`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
