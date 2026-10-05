# Audit report

> IMD Ember World - tenth offline Audit9 source-closure audit (World/Member M1).
> Length/format: Markdown five-row closure matrix, concise summary and separate source/release verdicts; evidence appendix with commands, errors, reproductions and immutable source/line links.
>
> Question: Does this exact candidate close Audit9's 3 Low + 2 Info source blockers and the two adjacent counterexamples without reopening prior Auth/ownership/artifact boundaries? Seek any-severity findings within these mechanisms; do not assume a pass.
> Period: latest Audit9 completed 2026-10-05 04:30:23.485 UTC; candidate source frozen 10:07:04 UTC; frozen TEAM measurements completed 14:04:44 UTC that day. Earlier Report9's bounded pass does not overrule Audit9.
>
> Candidate: https://github.com/tungweb3/imd-ember-world-review/tree/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643
> Original Audit9: https://github.com/Identity-md/research/blob/911652a2b1a7ab7be7d16bc37d97ab9376028fe6/jobs/d76a2a79-7394-420a-99d2-df2ba6a23f45/files/AUDIT.md
> Read Submission10/REVIEW_INPUTS.md and FinalClosure/{CLOSURE_MATRIX.md,TEST_RESULTS.json,ARTIFACT_CLOSURE.json,SOURCE_MANIFEST.json}, plus manifests/submission10-published-source.json. FinalClosure paths are under Submission10/. Historical namespaces are context.
>
> Scope: unofficial TypeScript Cloudflare Worker/React SIWE World + Member M1; no Solidity. M1 persists public profiles, so World is not wholly read-only. Selected sources:143 (127 raw exact;16 historically masked files/57 lines). Exclude 3D/scene/media/avatar/selfie/UI/full frontend, private Git/backups/databases, Genesis/Mint, Ember Coin and Fren Pet. Missing full frontend inputs mean unavailable build evidence, not a pass.
>
> Offline/local synthetic tests only. Public repo/prior-report GETs and locked dependency downloads allowed. No production endpoint tests/writes, real wallets/login/signatures, asset actions, approvals, claims, bridges, payments, deployment or new jobs. Never request private credentials/databases.
> Fresh exact public checkout, Node24.x; in source/ run:
> npm ci --ignore-scripts
> node scripts/review-tests.mjs --check
> npm run test:review
> node scripts/verify-artifact-closure.mjs
> Use locked real viem2.56.9, actual AuthClient/Worker and migration-backed SQLite. Run all supported files; no private-source selector, global-module substitute, crypto/Worker/SQLite shim, dropped failing test or hidden skip. Record commands/exits/errors/skips/cancel/todo/retry reasons. Real Windows file-symlink EPERM is failure/unavailable evidence, never an assertion pass. Separate environmental failures from source defects.
>
> Review these five mechanisms and reverse controls:
> 1 Low1: use live post-await clocks for final eligibility and admitted/refused no-eligible lane. Test24h-1/24h/24h+1ms, D1 delays0/1/2/5000ms, both enrichment reads, refused/failed/successful refresh, strict ownership proof29999/30000/30001ms, sale, rollback/NaN/Infinity and later recovery. Preserve original proof.checkedAt/index/producer timestamps. Expired/unavailable cannot become complete-empty/not-owned authority; no index/budget/RPC amplification.
> 2 Low2: same-client stop/restart A-to-B, locked[] or no-provider clears stale public identity and reconciles first observation independently of cookie A; passive first observation must not logout. Retain actual B-to-A/current address cleanup, explicit grants, binding/account-event fences and passive provider replacement. Adjacent early-click: hold restarted eth_accounts(B) or[], restore cookie A, click before reply, release it. Prior-life A must not enable a stale same-session fast path; late[] must not erase a newer explicit grant.
> 3 Low3: B verify commits with response/nonce cleanup held; stop; other context installs cookie A; restart provider[]; restore A; first accountsChanged(C). B's old lifetime must not cause expectedAddress=A logout/A-row revocation. Preserve B's nonce-specific cleanup, actual current C-to-D cleanup and held-completion fencing. Separate A's live SQLite row from shared cookie after delayed clear-cookie headers; old callbacks cannot install B into new UI.
> 4 Info4: actual replay CLI --minimize uses validated artifact writer. Test dangling/existing final file links, nonregular outputs, unsafe parent links/junctions, outside-root/namespace attempts, safe regular replacement and default replay without persistence. Preserve input bytes. Adjacent input-parent junction alias: differently spelled input/output paths resolving to the same input must be rejected; safe separate output through that alias preserves both input views. For deliberate invalid HARNESS-CAUSAL witnesses, child exit1 alone proves neither rejection nor an Auth vulnerability: inspect ARTIFACT_REJECTED, bytes/existence/hashes. State locally controlled-root assumption; no hostile concurrent ancestor-swap or SMB/NFS guarantee.
> 5 Info5: read back persisted nested quoted/bare route-prefix filenames/suffix variants: /api/auth/session.log, /api/auth/verify.backup, /api/me/home.private.json must be masked. Preserve exact allowed routes/query/subroute tokens, network URLs, relative IDs, nonce/action/event identities and replay structure. Exact routes cannot exempt arbitrary filename prefixes. Synthetic filenames do not demonstrate production data leakage.
>
> TEAM claims to verify independently:25 supported files; review659/659; artifact28/28; verifier19/19; fresh private/public review659/659; private full1709/1709. Positive runs exit0, zero fail/cancel/skipped/todo. Same-evaluator vulnerable baseline64:40 pass/24 assertion fail; baseline verifier19:14 pass/5 assertion fail, exit1, no EPERM/setup failures. Prior EPERM/setup retries are documented. Use current TEST_RESULTS.json; historical613/613 and13/13 are not current totals. Tests are bounded, not exhaustive state-machine/global RPC/concurrency proof.
>
> For every finding and adjacent case: severity, exact source location/event order, expected/actual, relevant synthetic SQLite rows, prompt/connect/challenge/verify/logout/hint/broadcast/index/budget/RPC counts, command/exit/hash, and CLOSED/PARTIAL/OPEN/accepted-limit/UNKNOWN with rationale. Cite exact-pin sources/lines beside claims. Separate REVIEWER reproductions, TEAM measurements, history, inference and unavailable checks.
> Return separate SOURCE-CLOSURE and RELEASE-READINESS verdicts: PASS/BLOCKED/UNKNOWN. Release baseline remains UNKNOWN; this source was not deployed. Offline closure does not measure production Cloudflare/browser/provider/cookies/ERC1271/M1 authorization/D1/WAF/limiter/upstream/process-death/cross-isolate behavior. Bound accepted limits; UNKNOWN is not a demonstrated source defect. Completed/accepted, passing tests or Low/Info labels are not certification/endorsement/zero vulnerabilities/fund-safety proof.
>
> Publication provenance: private source a2e6aca828858730cfb6b60931abea20ba9b6ab6. Final pin directly extends official public347268a7ecae700088547c2402db9a3eb07a6fd2. All143 source bytes match tested local projection59dfc4a90a52de181c1420f0babe6170c1dc08d7; differences are docs/checksums only. Intermediate local Git history is private, not published. Privacy-gate receipt is private; publication checks are not independent source review.

| | |
|---|---|
| Repository | https://github.com/tungweb3/imd-ember-world-review.git |
| Commit | `c2f21a9ef9e1a093ed2c5808f8a99e4751fde643` |
| Job | `e817a62e-1b9f-4469-90d7-7a761579af81` |
| Judged | 2026-10-05 15:59 UTC |
| Findings | 1 low · 3 info |

Four agents audited the code as it is at `c2f21a9`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Passive discovery overwrites abandoned verify cleanup, leaving the cancelled session live

`source/src/world/auth.ts:309`

```
      if(abandoned||uncertain){this.gen++;this.lifecycle.cancel();this.cancelOwners('lock-reconcile');
```

OPEN; Audit9 Low3 is only PARTIAL. providerChanged('discovery') treats every retained owner as current uncertainty and calls cancelOwners('lock-reconcile'). AuthLifecycle.abandon unconditionally changes the reason even when already abandoned with stop/context-switch. The late verify then goes through reconcileLockedOwner and releases the owner without retrying its deferred nonce logout. A stopped or genuinely switched-away B session remains live after a transport-failed first cleanup. This violates preserved original-operation nonce responsibility; no signature bypass, cross-account privilege or foreign-session revocation demonstrated. Filter discovery to current-life owners and prevent passive lock reconciliation from downgrading an existing revoking disposition; preserve legitimate same-lifetime lock-to-stop promotion and cleanup retry/idempotence. Source chain: auth.ts:236,308-311,614-643; authLifecycle.ts:102-114; authCleanup.ts:19-20. Independently reproduced against c2f21a9 on Linux Node24.21.0, real viem2.56.9/AuthClient/Worker/migration-backed node:sqlite. Immutable source: https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/src/world/auth.ts#L309. Source SHA256 07afd30b8dcd8b1b1d74f3a8940f2f4d9a7037b06246911290ec8392f968275b.

**Reproduction**

REVIEWER command: node /tmp/imd-a10-probe-auth.mjs; exit 1 ERR_ASSERTION actual lock-reconcile expected stop. Script SHA256 3ca70d941a7e1b9b0805f57de3fb6a48c919978d56015394c540c092b3ff96cf. Use tests/auth-r7-fixtures.mjs setup/provider/tab and synthetic privateKeyToAccount('0x'+'22'.repeat(32)) for B, 11 for A, 33 for C. ready -> signIn B; hold verify in intercept after Worker commit and cookie headers. stop (or same-life accountsChanged C); fail the first nonce logout in beforeSend with TypeError, before Worker dispatch; wait cleanup RETAINED/not inFlight. For stop variants lock provider while stopped, optionally browser.signIn A, then restart and restore the cookie. Replace provider with C and notifyProvider('discovery'); release held verify. Actual stop changes to lock-reconcile, owner RELEASED, no second logout. B row expires_at=1791201600000, revoked_at=NULL; B challenge used_at=1790596800000, invalidated_at=NULL. With no discovery the second expectedNonce logout is 204 and B.revoked_at=1790596800000 (owner CONSUMED). In replacement-A control second logout is 409 and A stays live; discovery attempts no second logout. Same-life switch produces the same lost cleanup. All six runs prompt/connect/challenge/verify=1/0/1/1, address logouts=0. Broadcast=0 except same-life discovery emits one signed-in hint; its session/home/hint/index/budget/RPC counts=3/1/1/1/1/0 versus control 3/0/0/0/0/0. Stop-B control/discovery sessionGET=4/4, homeGET=1/1, hint=2/2, index/budget/RPC=1/1/0; nonce logouts=2/1. No member writes. Full reproducible script:
import assert from 'node:assert/strict';
import {privateKeyToAccount} from '/tmp/imd-audit10-review/source/node_modules/viem/_esm/accounts/index.js';
import {setup,provider,tab,ready,defer,until,flush,rows,logouts,prompts,connects,routeEvents,statusOf} from '/tmp/imd-audit10-review/source/tests/auth-r7-fixtures.mjs';
const A=privateKeyToAccount('0x'+'11'.repeat(32)),B=privateKeyToAccount('0x'+'22'.repeat(32)),C=privateKeyToAccount('0x'+'33'.repeat(32));
const addr=x=>x.address.toLowerCase(),results=[];
for(const mode of ['stop-B','stop-A','switch'])for(const discovery of [false,true]){
 const w=setup(),b=w.browser(),p=provider(B),gate=defer();let chosen=p,committed=false,failed=false,budget=0,hint=0;
 w.env.CHAIN_LIMITER={limit:async({key})=>{if(key==='chain:index')budget++;return {success:true};}};
 const q=tab(w,b,p,{getProvider:()=>chosen,beforeSend:async(path,init)=>{
   if(path==='/api/auth/logout'&&JSON.parse(init.body).expectedNonce&&!failed){failed=true;throw new TypeError('synthetic transport failure before Worker');}
 },intercept:async(path,r)=>{if(path==='/api/auth/verify'){committed=true;await gate.promise;}return r;}});
 const set=q.c.deps.hint.set;q.c.deps.hint.set=v=>{hint++;set(v);};
 await ready(q);const flow=q.signIn();await until(()=>committed);
 if(mode==='switch')p.switchTo(C);else q.stop();
 await until(()=>failed&&!q.c.lifecycleSnapshot.cleanup.inFlight);
 const before=q.c.lifecycleSnapshot;
 if(mode!=='switch'){
   p.switchTo(null);
   if(mode==='stop-A')assert.equal((await b.signIn(A)).verify.status,200);
   q.restart();await until(()=>q.c.state.session?.address===addr(mode==='stop-A'?A:B)&&!q.c.state.checking);await flush();
 }
 const next=provider(C);
 if(discovery){chosen=next;q.observeProvider(next);q.notifyProvider('discovery');await flush(20);}
 const afterDiscovery=q.c.lifecycleSnapshot;
 gate.resolve();await flow;await flush(40);
 const final=q.c.lifecycleSnapshot,db=rows(w),client={account:q.c.state.account,session:q.c.state.session?.address??null,status:statusOf(q.c.state,w.clock.now())};
 const counts={prompt:prompts([p,next]),connect:connects([p,next]),challenge:routeEvents(q,'/api/auth/challenge').length,verify:routeEvents(q,'/api/auth/verify').length,
 session:routeEvents(q,'/api/auth/session').length,home:q.events.filter(e=>e.kind==='route'&&e.path.startsWith('/api/me/home')).length,
 logout:logouts(q).length,nonce:logouts(q).filter(e=>e.nonceAssertion).

### 2. Info: Candidate-cap ranking uses the stale request clock and omits a still-eligible seat

`source/server/ownership.ts:262`

```
        const order=(id:string)=>rank(agents.get(id),sightings.get(id),req.now);
```

OPEN adjacent temporal consistency defect. best() awaits owner-specific sightings but ranks with req.now, although home() now correctly counts at the live clock. With over 256 registered candidates, seats expiring during the wait tie with the still-recent seat and lower IDs crowd it out. Both keepIndex at line273 and the proof cut at line295 inherit the stale ranking. The result is partial/unavailable, not false complete-empty or forged ownership. Info: extreme-household availability/selection inconsistency; no additional RPC amplification or unauthorized owner rights. Sample current() once after the sightings await for the ranking, preserving original index/proof producer timestamps and all caps. Exact c2f21a9, real Worker/viem2.56.9/SQLite, synthetic offline fixtures. Immutable source: https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/server/ownership.ts#L262. Source SHA256 858cdfc9eec304e2c15b7f7b1ae66f846a9677c87a91c4333f56dd607abce207.

**Reproduction**

REVIEWER command node /tmp/imd-a10-probe-ownership.mjs cap; exit1 ERR_ASSERTION cap must prioritize the still-counting seat (false !== true). At t=1790596800000, A owns registered offline seats1..257 in roster and chain; seat_presence1..256=(A,last_online_at=t-86400000,updated_at=same);257=(A,t-1000,t-1000). First actual SQLite sightings completion advances injected clock by1ms (also5000). GET /api/me/home -> HTTP200 eligible0 size:null recheck:partial, 256 seats,257 absent; index_candidates.ids also1..256, read_at=t. Expected seat257 prioritized over expired1..256, eligible1 size:s (still partial). Delay0 control correctly counts256 with id tie-break. checkedAt=t+delay, unrenewed index t. Session A expires_at1791201600000 revoked_atNULL; auth rows unchanged; setup challenge/verify1/1, home1, sightings2, index/budget/RPC1/1/2, prompt/connect/logout/hint/broadcast0. No M1 writes. Script SHA256 837138d0f4b9c3e533c4bbece3874715834c0653c1a9a23ea32b6f3e256189e8. Full script (imports may be adjusted to the exact checkout location):
import assert from 'node:assert/strict';
import {privateKeyToAccount} from '/tmp/imd-audit10-review/source/node_modules/viem/_esm/accounts/index.js';
import {setup,fakeImd,fakeChain} from '/tmp/imd-audit10-review/source/tests/wallet-harness.mjs';
const A=privateKeyToAccount('0x'+'11'.repeat(32)),a=A.address.toLowerCase(),W=86400000,results=[];
function delayFirst(w,delay){const prepare=w.db.prepare.bind(w.db);let reads=0;
 w.db.prepare=sql=>{const wrap=s=>({...s,bind:(...args)=>wrap(s.bind(...args)),all:async()=>{const r=await s.all();if(sql.startsWith('SELECT token_id,last_online_at')){reads++;if(reads===1)w.clock.advance(delay);}return r;}});return wrap(prepare(sql));};return ()=>reads;
}
for(const delay of (process.argv[2]==='cap'?[]:[0,1,2,5000])){
 const owners=[];owners[7]=a;
 const w=setup({chain:fakeChain({owners:{7:a}}),imd:fakeImd({seats:{7:'707'},owners,online:[]})}),b=w.browser();let budget=0;
 w.env.CHAIN_LIMITER={limit:async()=>{budget++;return {success:true};}};
 const t=w.clock.now(),seen=t-W+1;w.db.raw.prepare('INSERT INTO seat_presence(token_id,owner,last_online_at,updated_at) VALUES(7,?,?,?)').run(a,seen,seen);
 const reads=delayFirst(w,delay),r=await b.get('/api/wallet/'+a+'/assets'),first=await r.json(),next=await(await b.get('/api/wallet/'+a+'/assets')).json();
 const result={mode:'assets',delay,t,now:w.clock.now(),first,next,cache:r.headers.get('cache-control'),expected:delay<=1,counts:{assets:2,sightings:reads(),index:w.chain.state.calls.filter(c=>!c.body).length,budget,rpc:w.chain.state.calls.filter(c=>c.body).length},sessions:w.db.raw.prepare('SELECT * FROM sessions').all(),presence:w.db.raw.prepare('SELECT * FROM seat_presence').all()};
 results.push(result);console.log(JSON.stringify(result));
}
for(const delay of [0,1,5000]){
 const owners=[],seats={},onchain={};for(let id=1;id<=257;id++){owners[id]=a;seats[id]=String(id+700);onchain[id]=a;}
 const w=setup({chain:fakeChain({owners:onchain}),imd:fakeImd({seats,owners,online:[]})}),b=w.browser();let budget=0;
 w.env.CHAIN_LIMITER={limit:async()=>{budget++;return {success:true};}};
 assert.equal((await b.signIn(A)).verify.status,200);
 const t=w.clock.now(),insert=w.db.raw.prepare('INSERT INTO seat_presence(token_id,owner,last_online_at,updated_at) VALUES(?,?,?,?)');
 for(let id=1;id<=257;id++){const seen=id===257?t-1000:t-W;insert.run(id,a,seen,seen);}
 const reads=delayFirst(w,delay),r=await b.get('/api/me/home'),home=await r.json();await Promise.all(w.kept);
 const result={mode:'cap',delay,t,now:w.clock.now(),status:r.status,eligible:home.eligible,size:home.size,recheck:home.recheck,checkedAt:home.checkedAt,seats:home.seats?.length,has257:home.seats?.some(s=>s.tokenId==='257'),countingIds:home.seats?.filter(s=>s.counts).map(s=>s.tokenId),indexRows:w.db.raw.prepare('SELECT * FROM index_candidates').all(),sessions:w.db.raw.prepare('SELECT address,expires_at,revoked_at FROM sessions').all(),counts:{challenge:1,verify:1,home:1,sig

### 3. Info: Public assets counts expired sightings using request-entry time after D1 await

`source/server/ownership.ts:371`

```
      seats:ids.map(id=>({...this.status(id,world.agents.get(id),seen.get(id),req.now),image:null})),
```

OPEN adjacent display consistency gap; the original Audit9 Low1 final household authority and lane fixes remain effective. assets() awaits world/sightings then passes req.now to status; its Worker caller server/auth.ts:735 supplies no live clock. Sighting expiry during D1 yields counts:true in this public unverified roster while the next request is false. Info only: public max-age=300 display hints, not owner authority; no index/budget/RPC amplification. Thread the live clock from the route and sample after awaited enrichment (account for later character I/O if enabled), without changing fetchedAt or the inclusive comparator. Synthetic D1 delays do not establish production effects. Immutable source: https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/server/ownership.ts#L371. Source SHA256 858cdfc9eec304e2c15b7f7b1ae66f846a9677c87a91c4333f56dd607abce207.

**Reproduction**

REVIEWER command node /tmp/imd-a10-probe-ownership.mjs; exit1 ERR_ASSERTION assets must count at the post-await clock (true !== false). At t=1790596800000 put seat7/agent707 offline, roster owner A=0x19e7e376e7c213b7e7e7e46cc70a5dd086daff2a; insert seat_presence(7,A,1790510400001,1790510400001). After first real SELECT token_id,last_online_at completes advance clock D in0/1/2/5000ms. Two GET /api/wallet/A/assets. First counts=true for all four; expected true,true,false,false at ages86399999/86400000/86400001/86404999. Immediate second counts=true,true,false,false, with offline-24h reason on expired cases. Original presence row unchanged; sessions empty; fetchedAt=t. Each run assetsGET2/sightings2, index/budget/RPC0/0/0, prompt/connect/challenge/verify/logout/hint/broadcast0. No M1 writes. Script SHA256 837138d0f4b9c3e533c4bbece3874715834c0653c1a9a23ea32b6f3e256189e8. Full script (imports may be adjusted to the exact checkout location):
import assert from 'node:assert/strict';
import {privateKeyToAccount} from '/tmp/imd-audit10-review/source/node_modules/viem/_esm/accounts/index.js';
import {setup,fakeImd,fakeChain} from '/tmp/imd-audit10-review/source/tests/wallet-harness.mjs';
const A=privateKeyToAccount('0x'+'11'.repeat(32)),a=A.address.toLowerCase(),W=86400000,results=[];
function delayFirst(w,delay){const prepare=w.db.prepare.bind(w.db);let reads=0;
 w.db.prepare=sql=>{const wrap=s=>({...s,bind:(...args)=>wrap(s.bind(...args)),all:async()=>{const r=await s.all();if(sql.startsWith('SELECT token_id,last_online_at')){reads++;if(reads===1)w.clock.advance(delay);}return r;}});return wrap(prepare(sql));};return ()=>reads;
}
for(const delay of (process.argv[2]==='cap'?[]:[0,1,2,5000])){
 const owners=[];owners[7]=a;
 const w=setup({chain:fakeChain({owners:{7:a}}),imd:fakeImd({seats:{7:'707'},owners,online:[]})}),b=w.browser();let budget=0;
 w.env.CHAIN_LIMITER={limit:async()=>{budget++;return {success:true};}};
 const t=w.clock.now(),seen=t-W+1;w.db.raw.prepare('INSERT INTO seat_presence(token_id,owner,last_online_at,updated_at) VALUES(7,?,?,?)').run(a,seen,seen);
 const reads=delayFirst(w,delay),r=await b.get('/api/wallet/'+a+'/assets'),first=await r.json(),next=await(await b.get('/api/wallet/'+a+'/assets')).json();
 const result={mode:'assets',delay,t,now:w.clock.now(),first,next,cache:r.headers.get('cache-control'),expected:delay<=1,counts:{assets:2,sightings:reads(),index:w.chain.state.calls.filter(c=>!c.body).length,budget,rpc:w.chain.state.calls.filter(c=>c.body).length},sessions:w.db.raw.prepare('SELECT * FROM sessions').all(),presence:w.db.raw.prepare('SELECT * FROM seat_presence').all()};
 results.push(result);console.log(JSON.stringify(result));
}
for(const delay of [0,1,5000]){
 const owners=[],seats={},onchain={};for(let id=1;id<=257;id++){owners[id]=a;seats[id]=String(id+700);onchain[id]=a;}
 const w=setup({chain:fakeChain({owners:onchain}),imd:fakeImd({seats,owners,online:[]})}),b=w.browser();let budget=0;
 w.env.CHAIN_LIMITER={limit:async()=>{budget++;return {success:true};}};
 assert.equal((await b.signIn(A)).verify.status,200);
 const t=w.clock.now(),insert=w.db.raw.prepare('INSERT INTO seat_presence(token_id,owner,last_online_at,updated_at) VALUES(?,?,?,?)');
 for(let id=1;id<=257;id++){const seen=id===257?t-1000:t-W;insert.run(id,a,seen,seen);}
 const reads=delayFirst(w,delay),r=await b.get('/api/me/home'),home=await r.json();await Promise.all(w.kept);
 const result={mode:'cap',delay,t,now:w.clock.now(),status:r.status,eligible:home.eligible,size:home.size,recheck:home.recheck,checkedAt:home.checkedAt,seats:home.seats?.length,has257:home.seats?.some(s=>s.tokenId==='257'),countingIds:home.seats?.filter(s=>s.counts).map(s=>s.tokenId),indexRows:w.db.raw.prepare('SELECT * FROM index_candidates').all(),sessions:w.db.raw.prepare('SELECT address,expires_at,revoked_at FROM sessions').all(),counts:{challenge:1,verify:1,home:1,sightings:reads(),index:w.chain.state.calls.filter(c=>!c.body).length,budget,rpc:w.chain.state.

### 4. Info: Bare route-prefix filenames containing spaces survive persisted artifact redaction

`source/tests/auth-artifacts.mjs:17`

```
    const route=[...routeIds].find(id=>chunk.startsWith(id,match.index)&&/^(?:$|[ \t]|[,;|)"'<>](?=[ \t]|$))/.test(chunk.slice(match.index+id.length)));
```

PARTIAL Audit9 Info5: dot/suffix filenames are fixed, but the route-prefix exemption treats whitespace as a route terminator. A bare local filename whose initial segments spell an allowed route bypasses the conservative remainder-of-line masking rule. Quoted paths mask correctly. This is an opt-in diagnostic redaction policy gap, not demonstrated production leakage or an Auth vulnerability. Require an unambiguous complete route token before exempting it, or explicitly narrow the claimed spaced-path guarantee and accept that limit. Preserve exact route/query/subroute identifiers, URLs, relative identifiers and replay structure. Reproduced by reading the actual file written by createArtifactStore, on exact c2f21a9 with Node24.21.0. Immutable source: https://github.com/tungweb3/imd-ember-world-review/blob/c2f21a9ef9e1a093ed2c5808f8a99e4751fde643/source/tests/auth-artifacts.mjs#L17. Source SHA256 af7e838ffa6cbd835a118c1e62b085ed15d5d2475d4e7663ce23668503db0d50.

**Reproduction**

REVIEWER command node /tmp/imd-a10-probe-redaction.mjs; exit1 ERR_ASSERTION expected Error at [local-path], actual Error at /api/auth/session private.log. Script SHA256 aca91d15f68e018510291981baa1a5bdc622dd79c2ff4624f4e718ab2d372488. Write core500-RESULT.json through createArtifactStore under a synthetic source/tmp/artifacts with nested messages [Error at /api/auth/session private.log, Cannot read /api/auth/session (private)/x.ts, /api/auth/session dir/file.ts]. Read back: first/third unchanged; second becomes Cannot read /api/auth/session (private)[local-path]. Expected full absolute filename masking in all three. Quoted same path and non-route spaced path mask; /api/auth/session.log, /api/auth/verify.backup and /api/me/home.private.json mask; exact routes/query/subroute, network URL, relative ID, n1 nonce, actions/events remain byte-equivalent. Persisted output830 bytes SHA25609be431559624b3f6920191eae4172376da683d5ece76510b9c9978cac259dbf. No DB rows or prompt/connect/challenge/verify/logout/hint/broadcast/index/budget/RPC calls. Full script:
import assert from 'node:assert/strict';
import {mkdirSync,readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {createArtifactStore,sanitizeArtifact} from '/tmp/imd-audit10-review/source/tests/auth-artifacts.mjs';
const root='/tmp/imd-a10-redaction-fixture';mkdirSync(root,{recursive:true});
const store=createArtifactStore({sourceDir:root,requestedDir:'tmp/artifacts'});
const messages=['Error at /api/auth/session private.log','Cannot read /api/auth/session (private)/x.ts','/api/auth/session dir/file.ts','Cannot read "/api/auth/session private.log"','Error at /root/private directory/project.ts'];
const controls={routes:['/api/auth/session','/api/auth/verify','/api/me/home','/api/me/home?fresh=1','/api/me/home/refresh'],url:'https://example.com/api/auth/session.log',relative:'tests/auth-artifacts.test.mjs',nonce:'n1',actions:[{type:'start',tab:'a'}],events:[{index:0,type:'headers',id:'r1'}]};
const filenames=['/api/auth/session.log','/api/auth/verify.backup','/api/me/home.private.json'];
store.write('core500-RESULT.json',{nested:{errors:messages},filenames,controls});
const bytes=readFileSync(store.directory+'/core500-RESULT.json'),saved=JSON.parse(bytes);
assert.deepEqual(saved.controls,controls);assert.deepEqual(saved.filenames,filenames.map(()=>'[local-path]'));
assert.equal(saved.nested.errors[3],'Cannot read "[local-path]"');assert.equal(saved.nested.errors[4],'Error at [local-path]');
console.log(JSON.stringify({messages,saved,bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex')}));
for(const text of ['Loaded module.file:///root/reviewer/private/project.ts','see x-file:///root/reviewer/private/project.ts','https://example.com/a,/root/reviewer/private/project.ts','at file:///root/reviewer/private/project.ts:12:3','node:internal/modules/esm/resolve:272'])console.log(JSON.stringify({input:text,actual:sanitizeArtifact(text)}));
assert.equal(saved.nested.errors[0],'Error at [local-path]','persisted bare route-prefix filename with spaces must be masked');

---

Judge's submission `fca579e45543c94ad3690021b52023d9bd739a3d50e1883aa318572ac4b6c97f`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
