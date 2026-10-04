# Audit report

> IMD Ember World - eighth Swarm audit / targeted Audit7 closure
>
> Question: Does this pinned candidate close the prior six Low and two Info findings, and what blocks SOURCE-CLOSURE or RELEASE-READINESS? Seek scoped regressions of any severity; no promised pass or zero-findings outcome.
> Period: 2026-10-05 pinned snapshot cutoff; captured prior records are comparison evidence.
> Length and format: Markdown finding table, reproductions and coverage appendix; preserve code/hashes/URLs.
>
> Exact public snapshot: https://github.com/tungweb3/imd-ember-world-review/tree/88c130283efc45260f9e00da8d2d3055c38483bd
> Previous public: 7215c5d89a96bc79113a85766c04868d54393f3c
> Frozen private source: bb7549e0a2576ba4da0ea7c4147c4aba1a7f577f
> TEAM deployed Worker: cdd3ef36-ca81-439a-8798-a64e30cf01d3
> Record: 20261004T180257Z-bb7549e
> Read Submission8/README.md and its closure matrix, test/reference, deployment/boundary, prior-original and REVIEW_INPUTS links; manifests/submission8-published-source.json; source/docs/security/AUDIT8_CLOSURE.md and AUDIT8_REVIEW_RUNNER.md. Cite actual pinned paths/lines. Older namespaces are historical.
>
> Unofficial TypeScript Cloudflare Worker/React SIWE; NO SOLIDITY. Persistent public names mean World is not wholly read-only. Scope: Auth/server authority, ownership discovery/proof/index/budget and related freshness/numbers. Exclude Genesis/Mint/Ember Coin/full 3D/scene/geometry/media/music/avatar/selfie/unrelated features. Supplied 140 source files: 124 exact, 16 preserved-redaction files/57 masked lines. No private history or full standalone frontend is supplied.
>
> Offline/local fixtures only. Public source/prior-document GETs and fresh dependency downloads are allowed. No live site/API test requests or writes, real wallets/signatures, transactions/approval/permit/delegation/bridging/mint, funding/payment/job submission, publication or deployment. Never request owner credentials/private databases. External deployment records are TEAM readbacks, not your live measurements; mark unavailable access unknown.
>
> Fresh checkout, Node 24, then in source/: npm ci --ignore-scripts; npm run test:review -- --check; npm run test:review. Require real locked viem 2.56.9/all 23 files. No stubs, omitted failing files, private source selectors/global crypto replacements or leaked outputs. Default persists no scheduler artifacts; opt-in sanitized/replayable output stays inside explicit source/tmp under the supplied policy.
>
> Provenance: public 574/574, core 500/500 (428 unique digests), additional 90/90 (54 unique) are inherited executions: all 140 public raw inputs/evaluator bytes remain unchanged for this candidate. Inheritance is not a fresh rerun; distinguish your own measurements. Private 1606/1606, TypeScript and Vite steps completed successfully. Overall canonical deploy exited1 at final local record-directory rename EPERM AFTER Wrangler exited0. The original nonzero receipt is retained; unchanged pending record restored; upload/live HTTP correspondence checked separately. Do not rewrite overall exit0, call it a test failure, or claim full public frontend build. Inspect BUILD_DEPLOYMENT.json for the operational limitation and point-in-time byte evidence.
>
> Eight causal fixes to test hardest, with baseline controls and actual effects:
> 1. Passive provider discovery must preserve cookie-restored/accepted session and selected page-used wallet. Test first/late announcements and reannouncements. Explicit provider selection and observed account changes remain genuine context changes with cleanup/fencing.
> 2. 20 overlapping ordinary AND fresh=1 home reads with advancing live clock share one index read, one chain-index budget charge and one proof per measured cohort. Re-read clock after queue/budget admission; stale request-start time cannot invalidate a newly completed index or amplify admission.
> 3. Same-account unlock after retained verify owner's first reconciliation503 must re-read canonically, preserve committed session and release lock responsibility. Lock is not logout. Provider/account/generation guards and later stop must not revive or cross-revoke another lifetime.
> 4. Ordinary valid canonical ABSENT/hint during an original same-click signature must not discard it solely because a read counter changed. Each click still needs its OWN preflight; PRESENT/UNKNOWN/context/expiry fence signing. Challenge lease uses finite nonnegative elapsed time from POST dispatch through completion; exact 5min/backward clock fails closed. SIWE clock tolerance and Worker nonce authority stay unchanged.
> 5. Queued independent roster/discovery intent re-evaluates after predecessor success OR failure503. Identical pending contexts share one bounded failure; failure stamps no proof epoch. Test later retry, changed roster, held proof crossing expiry/latest-block renewal and 512 active-address cap without live eviction.
> 6. Non-authority remote polling uses explicit 60000ms skew tolerance: test boundary/expiry/rollback/NaN/Infinity. Session/ownership/local-cache/write authority retain strict nonnegative ages/original TTL. floorUsd operands AND product finite/nonnegative; valid negative market changes remain valid.
> 7. Shared-copy warming preserves producer timestamps/source lineage instead of redating as now. Remote skew does not extend proof/session authority or conceal source age.
> 8. Default scheduler creates no sibling evidence/private-machine-path output. Opt-in source/tmp rejects symlink/junction escapes/nonregular files, sanitizes paths and preserves replay meaning. Real pinned dependencies/all 23 files/source-selector-clearing must remain active.
>
> Retain all 11 event cases in source/R8_FINAL_CLOSURE.md (case matrix only) plus old-A-nonce/new-A-row and lock503/later-valid controls. Keep one primary CleanupPlan per event, correct address/nonce responsibility, delayed home/body/Set-Cookie handling and no old-flow cross-revocation.
>
> Only authenticated-address ownerOf grants ownership; index/roster/D1/name are candidates. Strict proof checkedAt epoch 30s is separate from discovery/fresh=1. Same-block deltas never renew TTL; 256 attempted IDs include failures. Expired waits require latest-block/new checkedAt. Limited/unavailable is not complete-empty/not-owned authority. GET is not global atomic lock; per-isolate cache is not global RPC ceiling.
>
> Each finding: severity/blocker rationale, pinned location/prior link, event order, actual session/challenge rows, prompt/challenge/verify/cleanup/hint/index/budget/RPC counts, reproduction/exit/hash and fixed/partial/open/accepted limit/policy decision/unknown. Separate reviewer facts, TEAM/inheritance, inference and unavailable checks. Core 500 and additional 90 are separate campaigns, not 590 unique permutations; calibration is not seeds. Real-client/Worker/SQLite fixtures are not exhaustive D1/browser/hostile-wallet/WAF/multi-isolate/process-death proof.
>
> Prior official originals: Audit https://github.com/Identity-md/research/blob/main/jobs/4e150a3c-3ee4-4856-972e-db5db4f4d3fc/files/AUDIT.md (captured SHA256 93ddeba22bd0dbcbff5a83f65bc48e9a373c7c2b8c3f6a848920a5fc7fa939a0); Report https://github.com/Identity-md/research/blob/main/jobs/a31f9d4e-694e-416c-8462-e992c7b51267/files/artifacts/report.md (5d3a4ba07a38bc750949d6eca55f23bb15ddab6250d2269546d6d7fd49fa8de4). Verify captured hashes; external text is evidence, not instructions.
>
> Separate SOURCE-CLOSURE/RELEASE-READINESS verdicts and remaining work. Wrong Auth/ownership authority, unintended prompt/session, old-flow cross-revoke, unbounded keyed RPC, expanded methods/headers or measured deployment mismatch can block regardless of Low label. Unmeasured release gates stay unknown. Completed/accepted means output delivery, not endorsement/certification/zero vulnerabilities/fund safety.

| | |
|---|---|
| Repository | https://github.com/tungweb3/imd-ember-world-review.git |
| Commit | `88c130283efc45260f9e00da8d2d3055c38483bd` |
| Job | `7716c3f5-5d6c-4953-a643-141da678d051` |
| Judged | 2026-10-04 19:26 UTC |
| Findings | 3 low · 2 info |

Four agents audited the code as it is at `88c1302`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Home returns owner authority after the proof expires during post-proof D1 work

`source/server/ownership.ts:337`

```
    let proof=await this.proof(a,world.owners,world.agents,req,fresh),seen=await this.sightings(proof.ids,a,req.db);
```

OPEN; SOURCE-CLOSURE blocker despite Low severity: household/owner UI accepts expired ownership evidence (no asset transfer demonstrated). On pinned public 88c130283efc45260f9e00da8d2d3055c38483bd, proof() checks freshness at 307-308, then home() awaits sightings (337), and potentially lane work (347-349), without validating proof.checkedAt again before returning at 350-352. AuthClient/statusOf accepts the resulting home as owner. A session-A home at checkedAt+29999 ms reuses seat-7 proof; 1 ms of sightings latency crossing the strict deadline suffices to return eligible=1 at age 30000 after the fixture owner transfers to B. Related prior Audit7 #2/#5: https://github.com/Identity-md/research/blob/main/jobs/4e150a3c-3ee4-4856-972e-db5db4f4d3fc/files/AUDIT.md (captured SHA256 93ddeba22bd0dbcbff5a83f65bc48e9a373c7c2b8c3f6a848920a5fc7fa939a0, independently matched). This is an additional scoped path, not a failure of the exact supplied repair test. Recheck the live clock after all awaited enrichment/lane work, and reprove at latest or fail unavailable on expiry/rollback; do not return an expired fallback. This is an offline reviewer measurement, not live D1 evidence. The complete home() body was also byte-compared with the previous public 7215c5d89a96bc79113a85766c04868d54393f3c via its raw public source and is unchanged: this is pre-existing scoped behavior, not an asserted Submission8-introduced regression.

**Reproduction**

Fresh pinned checkout, Node v24.21.0, npm ci --ignore-scripts with real locked viem 2.56.9. Run the following from source/ with node --input-type=module via stdin. It asserts actual defective behavior and exits 0. At added sightings latency 0/1/2 ms: HTTP 200, proof age 29999/30000/30001, eligible=1, status=owner, index/budget/proof RPC=1/1/1, session rows created/live/revoked=1/1/0, challenge rows total/used/pending/invalidated=1/1/0/0. Setup challenge/verify=1/1; measured RPC methods contain only the ownership eth_call, no eth_getCode; UI prompts/cleanup/hints=0. For the expired cases the next request returns eligible=0 and total proof RPC=2. Expected at age >=30000: latest reproof returning zero or OWNERSHIP_UNAVAILABLE, never expired owner authority. Reproduction JavaScript SHA256 (UTF-8, including final newline): 0f0ee4f1cad69bac80881b67f9e575d2f969b24f14ff4d6676361d5fffe7e4e1.

import assert from 'node:assert/strict';
import {setup,newAccount,fakeChain,fakeImd} from './tests/wallet-harness.mjs';
import {MULTICALL3,ALCHEMY_NFTS_URL} from './server/ownership.ts';
import {INITIAL,statusOf} from './src/world/auth.ts';
for(const delay of [0,1,2]){
 const account=newAccount(),a=account.address.toLowerCase(),owners=[];owners[7]=a;
 const chain=fakeChain({owners:{7:a}}),w=setup({chain,imd:fakeImd({seats:{7:'707'},owners,online:[7]})}),b=w.browser();
 let budget=0;w.env.CHAIN_LIMITER={limit:async({key})=>{if(key==='chain:index')budget++;return {success:true};}};
 assert.equal((await b.signIn(account)).verify.status,200);
 const initial=await (await b.get('/api/me/home')).json();assert.equal(initial.eligible,1);
 w.clock.advance(29999);
 const prepare=w.db.prepare.bind(w.db);let held=true;
 w.db.prepare=sql=>{const wrap=s=>({...s,bind:(...args)=>wrap(s.bind(...args)),all:async()=>{
   if(held&&sql.startsWith('SELECT token_id,last_online_at')){held=false;chain.state.owners[7]='0x'+'2'.repeat(40);w.clock.advance(delay);}
   return s.all();}});return wrap(prepare(sql));};
 const r=await b.get('/api/me/home'),home=await r.json();
 const status=statusOf({...INITIAL,session:{address:a,expiresAt:w.clock.now()+600000},sessionKnown:true,home},w.clock.now());
 const rpc=()=>chain.state.calls.filter(c=>c.body&&JSON.parse(c.body).method==='eth_call'&&JSON.parse(c.body).params[0].to===MULTICALL3).length;
 console.log(JSON.stringify({delay,age:w.clock.now()-home.checkedAt,http:r.status,eligible:home.eligible,status,proofRpc:rpc(),rpcMethods:chain.state.calls.filter(c=>c.body).map(c=>JSON.parse(c.body).method),
 index:chain.state.calls.filter(c=>c.url.startsWith(ALCHEMY_NFTS_URL+'?')).length,budget,
 sessions:w.db.raw.prepare('SELECT count(*) created,sum(revoked_at IS NULL) live,sum(revoked_at IS NOT NULL) revoked FROM sessions').get(),
 challenges:w.db.raw.prepare('SELECT count(*) total,sum(used_at IS NOT NULL) used,sum(used_at IS NULL AND invalidated_at IS NULL) pending,sum(invalidated_at IS NOT NULL) invalidated FROM login_challenges').get()}));
 assert.equal(home.checkedAt,initial.checkedAt);assert.equal(home.eligible,1);assert.equal(status,'owner');
 if(delay){const next=await (await b.get('/api/me/home')).json();assert.equal(next.eligible,0);assert.equal(rpc(),2);
 console.log(JSON.stringify({delay,control:'next request',eligible:next.eligible,proofRpc:rpc()}));}
}

### 2. Low: First accountsChanged observation from a locked wallet revokes the cookie-restored session

`source/src/world/auth.ts:583`

```
    const other=!!a&&!!this.s.session&&this.s.session.address!==a;
```

PARTIAL Audit7 #1; SOURCE-CLOSURE blocker for unintended session revocation. Passive bind/discovery at lines 280-285 correctly requires a previously observed wallet account before cleanup. accountChanged instead compares the first observed account only against the displayed cookie session. With a restored session A, initially locked provider eth_accounts=[], no click and no retained owner, accountsChanged([B]) is treated as an A-to-B switch even though the page never observed account A. Lines 593-597 select displayed-session cleanup: POST /api/auth/logout with expectedAddress A revokes the live row and broadcasts signed-out. The same first account B observed by passive discovery preserves A and shows mismatch. Require an established prior account or active flow context before classifying first unlock as an account switch; preserve cleanup for a proven A-to-B change. Pinned public 88c130283efc45260f9e00da8d2d3055c38483bd. Prior: https://github.com/Identity-md/research/blob/main/jobs/4e150a3c-3ee4-4856-972e-db5db4f4d3fc/files/AUDIT.md (#1; SHA256 93ddeba22bd0dbcbff5a83f65bc48e9a373c7c2b8c3f6a848920a5fc7fa939a0 independently verified). Real AuthClient/Worker/SQLite offline reproduction; no real extension claim.

**Reproduction**

Node v24.21.0 and genuine locked viem 2.56.9 installed via npm ci --ignore-scripts. Run below from source/ with node --input-type=module on stdin (exit 0 asserting defective behavior). unlock-first: session created/live/revoked goes 1/1/0 -> 1/0/1, challenge total/used/pending/invalidated remains 1/1/0/0, one address-conditional logout 204, zero nonce cleanup, plan account-switch:displayed-session, one signed-out broadcast. No post-setup prompts/challenge/verify; setup challenge/verify=1/1. Discovery-first control preserves 1/1/0, no cleanup or broadcast. Observed-switch control first binds A then emits B and correctly revokes once. Default empty-world fixture needs no ownerOf proof (no seat candidates). Expected first-unlock behavior matches discovery-first, while genuine observed switch remains fenced. Additional measured upstream counts: one index fetch before the event, no RPC methods, unchanged after the event. Thus the event adds zero index/budget/proof RPC work; emitted hint/broadcast count is one for unlock-first and observed-switch, zero for discovery-first. Reproduction JavaScript SHA256 (UTF-8, including final newline): fb0c6cf88a50c39000fb01a037499bd866b9226c083dc079e9d19d4b3635342a.

import assert from 'node:assert/strict';
import {setup,newAccount,provider,tab,until,flush,rows,logouts,routeEvents,prompts} from './tests/auth-r7-fixtures.mjs';
for(const mode of ['unlock-first','discovery-first','observed-switch']){
 const w=setup(),A=newAccount(),B=newAccount(),b=w.browser(),p=provider(mode==='observed-switch'?A:null);
 assert.equal((await b.signIn(A)).verify.status,200);
 let chosen=mode==='discovery-first'?null:p;
 const q=tab(w,b,p,{getProvider:()=>chosen});
 await until(()=>q.c.state.restored&&q.c.state.session&&!q.c.state.checking);
 if(mode!=='observed-switch')assert.equal(q.c.state.account,null);
 const before=rows(w).counts;
 const beforeCalls=w.chain.state.calls.length;
 if(mode==='discovery-first'){chosen=provider(B);q.notifyProvider('discovery');}else p.switchTo(B);
 await flush(40);
 const result={mode,before,after:rows(w).counts,sessionRetained:!!q.c.state.session,
   plans:q.c.lifecycleSnapshot.cleanupPlans,logouts:logouts(q).map(e=>({address:e.addressAssertion,nonce:e.nonceAssertion,status:e.status})),
   broadcast:q.channels.flatMap(c=>c.messages),prompts:prompts([p]),challenge:routeEvents(q,'/api/auth/challenge').length,
   verify:routeEvents(q,'/api/auth/verify').length,
 upstreamCallsBeforeEvent:beforeCalls,upstreamCallsAfterEvent:w.chain.state.calls.length,
 rpcMethods:w.chain.state.calls.filter(c=>c.body).map(c=>JSON.parse(c.body).method),indexFetches:w.chain.state.calls.filter(c=>c.url.includes('getNFTsForOwner?')).length};
 console.log(JSON.stringify(result));
 assert.equal(rows(w).counts.live,mode==='discovery-first'?1:0);
 assert.equal(logouts(q).length,mode==='discovery-first'?0:1);q.stop();
}

### 3. Low: Slow paginated fresh home cohort serializes into repeated index admissions and proof epochs

`source/server/ownership.ts:266`

```
          const indexed=await this.candidates.get(address,current(),fresh?OWNERSHIP_TTL_MS:CANDIDATES_TTL_MS,async()=>{
```

PARTIAL Audit7 #2; blocks an all-eight-fixed SOURCE-CLOSURE verdict under the specified overlapping fresh=1 cohort requirement. Successful waiters recurse at 234-237. Candidate cache entry at 202 and index at 268 are dated before completion; the fresh keep predicate at 284 rejects the just-completed index when discovery plus proof consumes >=30000 ms. Twenty already-overlapping same-address fresh requests then each admit a new index cycle and start a new proof epoch. This is achievable within configured timeouts: four 7500-ms pages each below CHAIN_TIMEOUT_MS=10000, within NFT_PAGE_CAP=5, total 30000 ms; no single 30-second network fetch is needed. Measured 20 index cycles, 80 page fetches, 20 chain:index charges, 20 owner-proof RPCs and 20 checkedAt epochs, 602600 ms injected elapsed. It is bounded by existing request/admission controls; this does NOT demonstrate an unbounded/global RPC bypass or exhaustion of the 20-per-minute limiter (the measured slow cohort spans minutes). Preserve index producer age and strict proof TTL, while recognizing the completed discovery flight as satisfying waiters that joined that cohort, instead of recursively re-admitting them solely because its start timestamp aged. Prior #2: https://github.com/Identity-md/research/blob/main/jobs/4e150a3c-3ee4-4856-972e-db5db4f4d3fc/files/AUDIT.md (SHA256 93ddeba22bd0dbcbff5a83f65bc48e9a373c7c2b8c3f6a848920a5fc7fa939a0). Pinned public 88c130283efc45260f9e00da8d2d3055c38483bd. Offline injected-clock measurement, not production latency.

**Reproduction**

Run below in source/ on Node v24.21.0 with locked genuine viem 2.56.9, via node --input-type=module stdin. Exit 0 asserting observed behavior. Gate first page until all 20 Ownership.home(A, req(START+i), fresh) calls have entered. Budget advances live clock by 30 ms, each page by pageMs, each proof by 100 ms. Four-page fresh controls at 7475 and 7500 ms/page give budget/indexCycles/pageFetches/RPC/epochs = 20/20/80/20/20, elapsed 600600/602600 ms, all eligible=1/complete. Same four-page ordinary cohort gives 1/1/4/1/1 and 30130 ms. A 200-ms single-page fresh cohort gives 1/1/1/1/1 and 330 ms. Expected: one shared discovery admission/cycle and proof for the already-overlapping fresh cohort too (four network pages for one cycle). Direct Ownership fixture: no session/challenge rows, prompts/challenge/verify/cleanup/hints all zero; address A and ownerOf are fixture inputs, not an auth bypass. Reproduction JavaScript SHA256 (UTF-8, including final newline): b27ee42b60115e8e6f062b264d062c14a31e634b504966456ec791dc141876dc.

import assert from 'node:assert/strict';
import {decodeFunctionData,encodeFunctionResult,encodeAbiParameters,multicall3Abi} from 'viem';
import {Ownership,ALCHEMY_RPC_URL,ALCHEMY_NFTS_URL,MULTICALL3} from './server/ownership.ts';
import {SEAT_COLLECTION} from './src/world/market.ts';
const A='0x'+'1'.repeat(40),START=Date.UTC(2026,9,4,12),BLOCK=21000000n;
const abi=[{type:'function',name:'ownerOf',stateMutability:'view',inputs:[{name:'tokenId',type:'uint256'}],outputs:[{name:'',type:'address'}]}];
const defer=()=>{let resolve;return {promise:new Promise(r=>resolve=r),resolve};},tick=()=>new Promise(r=>setImmediate(r));
for(const [fresh,pageMs,pages] of [[false,7500,4],[true,200,1],[true,7475,4],[true,7500,4]]){
 const s={live:START,budget:0,index:0,pageFetches:0,rpc:0},gate=defer(),entered=defer();
 const gateway={async source(name){const owners=[];owners[7]=A;return {state:'fresh',fetchedAt:s.live,url:'fixture://'+name,
 data:name==='swarm'?{at:1,seats:{7:{tokenId:7,agentId:'707'}},owners}:{count:1,workers:[{seat:{tokenId:'7',agentId:'707'},working:0,runtimes:[],lastHeartbeatAt:'2026-10-04T11:59:00Z'}]}};}};
 const fetcher=async(input,init={})=>{
  if(String(input).startsWith(ALCHEMY_NFTS_URL+'?')){
   const page=Number(new URL(input).searchParams.get('pageKey')??0);if(page===0)s.index++;s.pageFetches++;s.live+=pageMs;
   if(s.pageFetches===1){entered.resolve();await gate.promise;}
   return Response.json({ownedNfts:[{contract:{address:SEAT_COLLECTION},tokenId:'7'}],pageKey:page+1<pages?String(page+1):null});
  }
  assert.equal(String(input),ALCHEMY_RPC_URL);s.rpc++;s.live+=100;
  const calls=decodeFunctionData({abi:multicall3Abi,data:JSON.parse(init.body).params[0].data}).args[0];
  return Response.json({jsonrpc:'2.0',id:1,result:encodeFunctionResult({abi:multicall3Abi,functionName:'aggregate3',result:calls.map(c=>
   c.target===MULTICALL3?{success:true,returnData:encodeAbiParameters([{type:'uint256'}],[BLOCK])}:{success:true,returnData:encodeFunctionResult({abi,functionName:'ownerOf',result:A})})})});
 };
 const o=new Ownership(gateway,[]),req=i=>({chain:{key:'offline-fixture',fetch:fetcher},now:START+i,clock:()=>s.live,budget:async()=>{s.budget++;s.live+=30;await tick();return true;}});
 const promises=Array.from({length:20},(_,i)=>o.home(A,req(i),fresh));
 await entered.promise;await tick();gate.resolve();
 const views=await Promise.all(promises),epochs=new Set(views.map(v=>v.checkedAt)).size;
 const expected=fresh&&pageMs*pages>=29900?20:1;
 console.log(JSON.stringify({fresh,pageMs,pages,budget:s.budget,indexCycles:s.index,pageFetches:s.pageFetches,rpc:s.rpc,epochs,elapsed:s.live-START,
 allEligible:views.every(v=>v.eligible===1),allComplete:views.every(v=>!v.recheck)}));
 assert.deepEqual([s.budget,s.index,s.rpc,epochs],[expected,expected,expected,expected]);
}

### 4. Info: Dangling scheduler output symlink bypasses source/tmp containment

`source/tests/auth-artifacts.mjs:28`

```
    validate();const path=join(directory,name);if(existsSync(path)&&(!lstatSync(path).isFile()||lstatSync(path).isSymbolicLink()))throw new Error('artifact output is not a regular file');return path;
```

PARTIAL Audit7 #8. existsSync follows the link and returns false when its target is absent, so file() does not lstat the existing symlink entry. writeFileSync at 32 then follows it and creates the target outside the permitted source/tmp. Directory validation does not inspect this final component. A deterministic preplanted dangling core500-RESULT.json symlink defeats the documented output containment without any race. Default-disabled output still works; no remote wallet/Worker authority is affected. Info severity reflects local opt-in artifact hygiene and a preexisting hostile filesystem entry. It prevents declaring the artifact-containment requirement fully closed. Use lstat independently of target existence and a no-follow/exclusive safe open strategy, checking directory components too. Pinned public 88c130283efc45260f9e00da8d2d3055c38483bd; policy source/docs/security/AUDIT8_REVIEW_RUNNER.md. Prior #8: https://github.com/Identity-md/research/blob/main/jobs/4e150a3c-3ee4-4856-972e-db5db4f4d3fc/files/AUDIT.md (SHA256 93ddeba22bd0dbcbff5a83f65bc48e9a373c7c2b8c3f6a848920a5fc7fa939a0). Duplicate flow/math reports merged.

**Reproduction**

Node v24.21.0, pinned clean checkout. Run the script below from source/ with node --input-type=module stdin (exit 0). It creates a synthetic source S under the real source/tmp/reviewer-artifact-probe, links S/tmp/store/core500-RESULT.json to ../../escaped.json while the target is absent, and invokes createArtifactStore({sourceDir:S,requestedDir:'tmp/store'}).write(...). Expected: reject nonregular output and create nothing outside S/tmp. Actual: wrote=true, S/escaped.json created outside allowed S/tmp, output remains symlink, JSON trace unchanged. Control: second write through the same link is rejected once its target exists. All physical writes remain in the real source/tmp and are removed in finally. No session/challenge rows or prompt/challenge/verify/cleanup/hint/index/budget/RPC activity. Reproduction JavaScript SHA256 (UTF-8, including final newline): b688b0d47f181b6366fd38ca9ef4ab9596a3c15a13fe10480ed1d3a44d28b1a6.

import assert from 'node:assert/strict';
import {mkdirSync,symlinkSync,existsSync,readFileSync,rmSync,lstatSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {createArtifactStore,sanitizeArtifact} from './tests/auth-artifacts.mjs';
const root=resolve('tmp/reviewer-artifact-probe');assert.equal(existsSync(root),false);
try{
 const dir=join(root,'tmp/store'),escaped=join(root,'escaped.json');mkdirSync(dir,{recursive:true});
 const output=join(dir,'core500-RESULT.json');symlinkSync('../../escaped.json',output);
 assert.equal(existsSync(output),false);assert.equal(lstatSync(output).isSymbolicLink(),true);
 const store=createArtifactStore({sourceDir:root,requestedDir:'tmp/store'});
 const wrote=store.write('core500-RESULT.json',{status:'PASS',trace:{actions:[{type:'start',tab:'a'}]}});
 console.log(JSON.stringify({wrote,escapedCreated:existsSync(escaped),outsideAllowedTmp:!escaped.startsWith(join(root,'tmp')+'/'),
 outputStillSymlink:lstatSync(output).isSymbolicLink(),escaped:JSON.parse(readFileSync(escaped,'utf8'))}));
 assert.equal(wrote,true);assert.equal(existsSync(escaped),true);
 assert.throws(()=>store.write('core500-RESULT.json',{status:'FAIL'}),/not a regular file/);
 console.log('existing-symlink control rejected');
 for(const p of ['/home/ci/source/x.mjs','/root/work/source/x.mjs','/var/lib/ci/source/x.mjs','/opt/build/x.mjs','/srv/jobs/x.mjs','/workspace/source/x.mjs','/Volumes/Work/source/x.mjs','/dev/shm/x.mjs','/mnt/c/Users/u/x.mjs']){
   console.log(JSON.stringify({input:p,output:sanitizeArtifact({message:'Cannot find module '+p})}));
 }
 const next=createArtifactStore({sourceDir:root,requestedDir:'tmp/clean'});
 next.write('core500-RESULT.json',{message:'Cannot find module /root/private-project/source/x.mjs',sourceRoot:'/root/private-project/source',trace:{actions:[{type:'start',tab:'a'}]}});
 const v=JSON.parse(readFileSync(join(root,'tmp/clean/core500-RESULT.json'),'utf8'));
 assert.equal(v.message,'Cannot find module /root/private-project/source/x.mjs');assert.equal(v.sourceRoot,undefined);
 assert.deepEqual(v.trace.actions,[{type:'start',tab:'a'}]);console.log(JSON.stringify({persisted:v}));
}finally{rmSync(root,{recursive:true,force:true});}

### 5. Info: Artifact sanitizer leaves absolute machine paths under common POSIX roots unmasked

`source/tests/auth-artifacts.mjs:10`

```
  if(typeof value==='string')return value.replace(/(?:[A-Za-z]:[\\/]|\/(?:Users|home|tmp)\/)[^\s"'<>|]+/g,'[local-path]');
```

PARTIAL Audit7 #8, separate mechanism from symlink containment. The string sanitizer enumerates only Windows drive prefixes and /Users/, /home/, /tmp/. Error/detail strings containing /root, /var/lib, /srv, /opt, /workspace, /Volumes or /dev/shm paths persist verbatim through createArtifactStore.write. WSL /mnt/c/Users/... is only partly removed. Hidden-key deletion works but does not cover arbitrary failure.message/detail strings. Info: a concrete sanitizer/output-contract failure and defense-in-depth gap; no current production secret leak or naturally emitted private-path failure is claimed. Default scheduler output remains disabled. Mask the actual checkout/machine roots or recognize absolute filesystem path tokens without altering replay action values. Pinned public 88c130283efc45260f9e00da8d2d3055c38483bd. Prior #8: https://github.com/Identity-md/research/blob/main/jobs/4e150a3c-3ee4-4856-972e-db5db4f4d3fc/files/AUDIT.md (SHA256 93ddeba22bd0dbcbff5a83f65bc48e9a373c7c2b8c3f6a848920a5fc7fa939a0). Duplicate flow/permissions reports merged. Non-authority issue; prevents the absolute no-private-path guarantee but not independently a remote release exploit.

**Reproduction**

Run the shared artifact probe below from source/ on Node v24.21.0, node --input-type=module stdin (exit 0). sanitizeArtifact({message:'Cannot find module /root/work/source/x.mjs'}) returns the same path; /home/ci/source/x.mjs becomes [local-path]. /var/lib, /opt, /srv, /workspace, /Volumes and /dev/shm controls remain unmasked; /mnt/c/Users/u/x.mjs becomes /mnt/c[local-path]. createArtifactStore.write persists {message:'Cannot find module /root/private-project/source/x.mjs'} unchanged, while removing sourceRoot and preserving trace.actions exactly. Expected: no absolute machine path in persisted message. Strings are synthetic, not actual disclosed private paths. Temporary fixture is removed. No session/challenge rows; all auth/index/budget/RPC counts zero. Reproduction JavaScript SHA256 (UTF-8, including final newline): b688b0d47f181b6366fd38ca9ef4ab9596a3c15a13fe10480ed1d3a44d28b1a6.

import assert from 'node:assert/strict';
import {mkdirSync,symlinkSync,existsSync,readFileSync,rmSync,lstatSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {createArtifactStore,sanitizeArtifact} from './tests/auth-artifacts.mjs';
const root=resolve('tmp/reviewer-artifact-probe');assert.equal(existsSync(root),false);
try{
 const dir=join(root,'tmp/store'),escaped=join(root,'escaped.json');mkdirSync(dir,{recursive:true});
 const output=join(dir,'core500-RESULT.json');symlinkSync('../../escaped.json',output);
 assert.equal(existsSync(output),false);assert.equal(lstatSync(output).isSymbolicLink(),true);
 const store=createArtifactStore({sourceDir:root,requestedDir:'tmp/store'});
 const wrote=store.write('core500-RESULT.json',{status:'PASS',trace:{actions:[{type:'start',tab:'a'}]}});
 console.log(JSON.stringify({wrote,escapedCreated:existsSync(escaped),outsideAllowedTmp:!escaped.startsWith(join(root,'tmp')+'/'),
 outputStillSymlink:lstatSync(output).isSymbolicLink(),escaped:JSON.parse(readFileSync(escaped,'utf8'))}));
 assert.equal(wrote,true);assert.equal(existsSync(escaped),true);
 assert.throws(()=>store.write('core500-RESULT.json',{status:'FAIL'}),/not a regular file/);
 console.log('existing-symlink control rejected');
 for(const p of ['/home/ci/source/x.mjs','/root/work/source/x.mjs','/var/lib/ci/source/x.mjs','/opt/build/x.mjs','/srv/jobs/x.mjs','/workspace/source/x.mjs','/Volumes/Work/source/x.mjs','/dev/shm/x.mjs','/mnt/c/Users/u/x.mjs']){
   console.log(JSON.stringify({input:p,output:sanitizeArtifact({message:'Cannot find module '+p})}));
 }
 const next=createArtifactStore({sourceDir:root,requestedDir:'tmp/clean'});
 next.write('core500-RESULT.json',{message:'Cannot find module /root/private-project/source/x.mjs',sourceRoot:'/root/private-project/source',trace:{actions:[{type:'start',tab:'a'}]}});
 const v=JSON.parse(readFileSync(join(root,'tmp/clean/core500-RESULT.json'),'utf8'));
 assert.equal(v.message,'Cannot find module /root/private-project/source/x.mjs');assert.equal(v.sourceRoot,undefined);
 assert.deepEqual(v.trace.actions,[{type:'start',tab:'a'}]);console.log(JSON.stringify({persisted:v}));
}finally{rmSync(root,{recursive:true,force:true});}

---

Judge's submission `63293e0212a0e1bda71739653d1573ad98998d56f78aad4114e9602db9f9cfb1`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
