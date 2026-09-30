# Audit report

> IMD Ember World (https://imdember.com) - re-audit of wallet sign-in, sessions and home authorization after the fixes for audit 519db624 (World only)
>
> Please read this first: this repository contains NO Solidity and no smart contract. It is a TypeScript Cloudflare Worker (the server) and the TypeScript/React client code for wallet sign-in (SIWE, EIP-4361). The site never asks a wallet for a transaction, a token/NFT approval, a Permit/Permit2 or typed-data signature; the only signature is personal_sign of a server-built SIWE text. The team states there is no "loss of funds" path by design (please verify rather than assume it). Rate findings by what an attacker could do to a player through this code: sign in as an address without its key, keep or revive a session after revocation, end another address's sessions, get owner rights for seats or a house that are not theirs, make the page ask the wallet to sign anything other than the site's own sign-in text, leak data, or deny sign-in (availability is in scope). If your checklist is Solidity-only, say which parts you could not apply rather than forcing them.
>
> Repository: the public review snapshot pinned at the commit shown when "Read" was clicked: the newest commit, whose parent is b6e986be6d1c85a720a3b8231feb3adf1ab2b780 (the version audit 519db624 reviewed; c2a8c33 before it). Code is in source/. Root docs are in Traditional Chinese and are the team's claims; the code is the reference. README.md maps each earlier finding (A-1..A-8 of audit 519db624, W-1..W-3/S-1/S-2 of Report e48d0a96) to what changed and what remains; none of these fix statuses has been re-reviewed.
>
> Facts you cannot check without network (team statements, from the deploy record and read-only GETs on 2026-09-30):
> - Live: Cloudflare Worker "imd-world" version 1a0dd495-35e7-4052-ba84-332e787f864d, built from private commit 4321bb4da3826276919ed60ecc2018139dcaeacc (source/ is taken from a later commit that differs only in one doc and one test, plus two added evidence pages).
> - Rebuilding the Worker from source/ alone (wrangler deploy --dry-run) gives SHA-256 1018f02a98ccb7de5b91434613d5e38047925a463df8d892b6cd9439d9a2078c (274,961 bytes), equal to the deploy record (manifests/).
> - D1 migrations 0001-0004 applied (0004_index_candidates before this code); rate-limit bindings as in source/wrangler.jsonc; an edge rule blocks an IP sending over 20 /api/ requests in 10 s.
>
> Entry points: source/worker/app.ts routes /api/* to server/auth.ts handleAccountApi (line 473), then server/world-api.ts, else static assets.
> - POST /api/auth/challenge (challenge, auth.ts:339; INSERT_CHALLENGE :129), POST /api/auth/verify (verify :365; verifySignature :290), POST /api/auth/logout (:438) and /api/auth/logout-all (:451), GET /api/auth/session (:431; readSession :326).
> - GET /api/me/home (owner data from the session's address only; server/ownership.ts class Ownership :191, ownerOf via Multicall3), GET /api/wallet/:address/assets (public), GET /api/world/* (public data; server/gateway.ts now also keeps a shared copy of the upstream snapshot in the Cache API, worker/app.ts:40-58).
> - Cron: server/presence.ts (presence rows, cleanup, and the new index_candidates prune).
> - Client: src/world/auth.ts (AuthClient; statusOf :54), siwe.ts (checkSignInMessage :16 before personal_sign at auth.ts:247), homeEntry.ts (enterGate :11, enterableHome :21), walletView.ts / WalletPanel.tsx, moves.ts.
>
> What changed since b6e986b (please verify each fix, then look for what the fix itself broke):
> - A-1: a contract address whose per-address ERC-1271 share is spent still gets one check a minute per network (CLAIM_LANE auth.ts:154, key chain:erc1271:lane). Can junk from a few networks still hold a real Safe owner out? Can the lane be used to exceed the chain:erc1271 budgets?
> - A-2: the last NFT-index answer per address is kept in D1 (migrations/0004, ownership.ts KEEP_INDEX :153, keptIndex :166) and reused as candidates when chain:index is refused or fails; ownerOf proves every one. Can a kept row grant or leak seats, be written for another address, or replace a newer answer?
> - A-3: the client keeps only the latest /api/me/home read (src/world/auth.ts around :190). Any ordering left where an older answer restores owner mode or Enter?
> - A-4: candidates ranked (seats that can count first, ownership.ts :138, :212) and a cut list reported as partial, never as "owns nothing" (:232).
> - A-5: challenge and verify read the clock only after the body has arrived (clock :245, readJson :247); there is no separate body timeout, and the per-IP limiter is still asked at request start (stated trade-off). Can a slow body still date a check into an earlier minute or past its challenge's window?
> - A-6: the per-(address, network) challenge cooldown is gone; one address asked from many networks writes audit lines (ADDRESS_SURGE). Does removing it open a new cost or lock-out path?
> - A-7: 20 of the global 60-per-6-s valve are kept for networks with no challenge in the last minute (INSERT_CHALLENGE, FRESH_NETWORK_RESERVE :118). Can a few networks still close sign-in for everyone?
> - A-8: the page says the chain check could not be completed instead of "no seat" (walletView.ts).
> - Report follow-ups: W-1 owner mode, move and Enter end at the session's expiresAt on the device clock; the old SIWE statement allowance removed; undici pinned (package.json overrides).
>
> Please look hardest at, as before: signature verification (message re-read from D1 only; domain, URI, chain id 1, version, statement, Issued At, Expiration Time equal to the stored row; ERC-6492 refused; ERC-1271 needs code and exactly the magic word; one check per challenge; burns on failure except 503/409 as SIWE.md states), session issuance and revocation (one session per nonce, token stored as SHA-256, __Host- cookies, 7-day expiry, logout-all only by a live session), limiters failing closed (permit :239, LimiterMissing), ownership only from ownerOf and the session address, and the page-side check (nothing but this site's exact 11-line message for this account and nonce reaches personal_sign; it does not stop injected script or a phishing page: known limit).
>
> Tests: source/tests (node --test; TESTS/README.md: copy source/ into its own git repo, npm ci, add the two stubs from TESTS/stubs). Real handler, migrations on node:sqlite, synthetic keys; only npm ci needs network. Recorded outputs are in TESTS/. Snapshot run: 171 tests, 167 pass, 4 fail: three need withheld house geometry or interior code, one (tests/deploy-evidence.test.mjs) needs the team's git history. The three "group 5" Enter-gate tests pass. The A-n and W-n tests are named after the finding ids.
>
> Out of scope: Genesis Mint (no Mint code here; a future Mint page on this origin will be reviewed separately; see source/docs/security/MINT_BOUNDARY.md), withheld files (3D world, art, music, house placement, interior rendering, WorldApp.tsx; listed by hash in manifests/).
>
> Report each finding with severity, file:line, the attacker's preconditions and the impact on a player, and a reproduction or a clear argument; say which earlier finding it relates to, and list what you could not check. This is a code review record, not a certification: please do not call the site safe, secure, audited or certified.

| | |
|---|---|
| Repository | https://github.com/tungweb3/imd-ember-world-review.git |
| Commit | `ae1d41a30363ad04711083465501680469400d2f` |
| Job | `8c3aea2e-26bc-4bff-bf5d-52d10f79ec9b` |
| Judged | 2026-09-30 13:45 UTC |
| Findings | 6 low · 1 info |

Four agents audited the code as it is at `ae1d41a`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: An older session response erases owner state established by a newer restore

`source/src/world/auth.ts:178`

```
      const v=await r.json() as {signedIn:boolean;address?:string;expiresAt?:number};if(g!==this.gen)return;
```

Related to A-3. Overlapping restore() calls share gen and have no session-read sequence guard. A page-load read can overlap the restore started by a signed-in BroadcastChannel message from another tab. If the old signedIn:false body arrives last, it clears the session and home already obtained by the newer read. Owner mode, Enter and move controls disappear despite a live cookie. sessionKnown remains true, and visible() and refreshHome() do not restore a missing session; the next sign-in click can request an unnecessary signature. No attacker privilege is needed: ordinary cross-tab sign-in and delayed delivery suffice. Add a session-read sequence counter checked after fetch, body parsing and in failure handling.

**Reproduction**

Executed Node v24.21.0 importing the unmodified AuthClient and statusOf. Inject clock T=2026-09-30T12:00:00Z, inert timers, a memory hint store and controlled fetch. Start restore R1 and hold json() for {signedIn:false}. Start R2 and return {signedIn:true,address:'0x1111111111111111111111111111111111111111',expiresAt:T+86400000}; return a home for that address with eligible:1,size:'s',one counting seat,checkedAt:T,presence:'fresh'. Await R2: statusOf is owner. Resolve R1's body and await R1. Expected: R1 is superseded and owner state remains. Actual, asserted: session=null, home=null, sessionKnown=true, statusOf=visitor. This models a successful sign-in in another tab between the two session reads.

### 2. Low: A cancelled sign-in still asks the old account to sign when the challenge body arrives late

`source/src/world/auth.ts:240`

```
      const {nonce,message}=await c.json() as {nonce:string;message:string};
```

Related to A-3 and F-7a. The generation check runs before awaiting the challenge body, with no check after that await or immediately before personal_sign. An account/provider switch or sign-out during body delivery cancels the flow, but the old continuation validates against its captured account and prompts its captured provider anyway. This creates an unwanted wallet prompt for the abandoned account and can interfere with a replacement flow. The prompt still contains this site's SIWE text, and the later generation check prevents verification; this is not arbitrary signing or an authentication bypass. Recheck generation and the active account/provider after c.json() and before updating signing state or prompting.

**Reproduction**

Executed the unmodified AuthClient in Node v24.21.0 at T=2026-09-30T12:00:00Z. Restore signedIn:false, accountChanged(A), and call signIn(), where A='0x1111111111111111111111111111111111111111'. Return successful challenge headers but hold json(). Call accountChanged(B), B='0x2222222222222222222222222222222222222222', and answer its logout with 204. Release the challenge body: nonce='a'.repeat(32), and the exact 11-line message naming imdember.com, A, exported SIWE_STATEMENT, URI https://imdember.com/, Version 1, Chain ID 1, that nonce, Issued At T, Expiration Time T+300000. Expected: zero wallet prompts from the cancelled flow. Actual, asserted: one personal_sign with params[1]=A while client.state.account=B. Returning '0x12' sends no verify because the subsequent generation guard rejects it.

### 3. Low: The candidate cap drops an owned seat that still qualifies through recent presence

`source/server/ownership.ts:212`

```
    const order=(id:string)=>rank(agents.get(id)),best=(ids:Iterable<string>)=>[...ids].sort((x,y)=>order(x)-order(y)||compareIds(x,y)).slice(0,CANDIDATE_CAP);
```

Residual A-4, also affecting the candidates persisted by A-2. rank() considers registration and current online status, but not the owner-bound 24-hour sightings that status() uses for eligibility. Sightings are read only after truncation. Thus 256 lower-numbered registered offline seats with no recent sighting displace a higher-numbered seat that still counts. An attacker must transfer enough real registered seat NFTs to cross this boundary: one additional NFT suffices for an owner already holding 255 non-counting lower IDs and one qualifying higher ID. The response correctly says partial, but eligible=0 removes owner mode, Enter and move access; repeating the check chooses the same wrong subset. Use the same owner-specific recent-presence predicate before truncating, and continue proving each selected candidate with ownerOf. This does not forge ownership or transfer funds.

**Reproduction**

Executed unmodified Ownership with real viem ABI encoding, ReadGateway, all four migrations on node:sqlite and wallet-harness fakeImd/fakeChain fixtures. At T=1790769600000 (2026-09-30T12:00:00Z), A=0x1111111111111111111111111111111111111111 owns IDs 0..254 and 1000. Give each a distinct numeric agentId; fresh complete workers is empty. Insert seat_presence(1000,A,T-3600000,T-3600000); no other sighting exists. Both candidate sources and ownerOf agree on these 256 IDs, and chain:index is allowed. First home(A) returns eligible=1,size='s'. Transfer registered offline #255 to A and update roster/index/ownerOf consistently. Read using a new Ownership/ReadGateway at the same T. Expected: recently seen #1000 remains selected and eligibility remains at least 1. Actual, asserted: seats are 0..255, #1000 absent, eligible=0,size=null,recheck='partial'; statusOf changes from owner to ownershipUnavailable. The two specialist reports of this issue are merged here.

### 4. Low: A-1's fallback lane counts the owner's earlier pool check and blocks its retry

`source/server/auth.ts:156`

```
 AND NOT EXISTS(SELECT 1 FROM login_challenges WHERE net=?3 AND called_at>?4 AND +address=?6)`;
```

Related to A-1/F-3; includes the overlapping same-network residual reported by the economics specialist. CLAIM_LANE counts every called_at row, including a legitimate earlier shared-pool attempt or successful sign-in. After that attempt, one invalid verify from any other network consumes the address's remaining shared slot, and the owner has no fallback lane for a retry or second device for the remainder of the rolling minute. Preconditions: known contract address, an owner attempt within the last minute, and one attacker challenge plus garbage verify from another network; no owner key is needed. A neighbour in the same /24 or /48 can also consume both slots with two garbage verifies and deny the owner's first attempt, an already documented residual rather than a separate finding. Track lane usage separately from pool usage, or reserve a carefully bounded additional retry, charging it to the existing lane budget and retaining network/global bounds.

**Reproduction**

Executed the real Worker handler, four real migrations on node:sqlite, real viem encoding and fakeChain ERC-1271 callback for C=0x5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a (accepts only synthetic signature 0xaa, rejects 0x12), with AUTH=20,API=180,CHAIN=20,SEAT=60 per-minute limiters. Owner 198.51.100.20 verifies 0x12 ->401; attacker 203.0.113.9 verifies 0x12 ->401; owner retries 0xaa ->429 CHAIN_BUSY, reason address. After 61000 ms: owner signs in with 0xaa ->200; attacker garbage ->401; second device 198.51.100.21 with 0xaa ->429, reason address. Expected: the fallback reserve remains usable for an owner retry after the shared slots are spent. Actual: the earlier owner pool check satisfies NOT EXISTS's disqualifying predicate. Also reproduced two garbage verifies from 198.51.100.77 denying the owner's next valid check. Control: two garbage verifies from different foreign /24s, with no earlier owner attempt, leave an owner lane check and return 200.

### 5. Low: IPv6 /48 aggregation lets separate subscriber networks exhaust one another's smart-wallet sign-ins

`source/worker/app.ts:77`

```
  return k.startsWith('ip6:')?'net6:'+k.slice(4).split(':').slice(0,3).join(':')+'::/48':'net:'+k.slice(3);
```

Related to A-6/F-3/F-5 availability. The per-IP limiter distinguishes IPv6 /64s, but all /64s within a /48 share D1's three contract checks, ten code claims and thirty challenges per minute. Where distinct subscribers are assigned prefixes within one /48, one subscriber can consume the three contract checks and prevent unrelated subscribers signing in with other smart-wallet addresses. Four ordinary concurrent smart-wallet users also trigger the refusal without an attacker. This is conditional on actual address allocation; carrier prevalence and production user distribution were not established. Use an allocation-appropriate prefix and scaled budgets, while preserving protection against host-address rotation. No signature or ownership bypass results.

**Reproduction**

Executed the real Worker with all four migrations on node:sqlite, real viem encoding and production-shaped AUTH=20,API=180,CHAIN=20,SEAT=60 per-minute limiters. In one minute, clients at 2001:db8:1:a::1, 2001:db8:1:b::2, 2001:db8:1:c::3 and 2001:db8:1:d::4 each request and verify a challenge for a different deployed synthetic contract address (0x1111...1111 through 0x4444...4444); each callback accepts its test signature with the exact ERC-1271 magic word. Expected under the separate-subscriber precondition: independent sign-ins. Actual, asserted statuses: 200,200,200,429 CHAIN_BUSY, with reason network_contract. All four networkKey outputs equal net6:2001:db8:1::/48, while rateLimitKey distinguishes them. The same effect permits an attacker controlling one subscriber prefix and three contract addresses to exclude another subscriber's wallet.

### 6. Low: One IP can consume all NFT-index discovery capacity and deny newly indexed owners home access

`source/server/ownership.ts:219`

```
          if(!req.budget||!await req.budget())throw new Limited();
```

Related to H1/F-3 and the remaining A-2 availability limitation; this is the substantiated subset of the economics specialist's report. Any newly generated EOA can obtain a session and spend one unit of the shared chain:index budget. One IP's allowed 20 sign-ins per minute is enough to consume all 20 discovery reads at its Cloudflare location. A legitimate owner whose NFT appears only in the index, with no candidate yet kept in D1, then receives eligible=0,recheck=limited and loses owner mode/Enter/move access even though ownerOf would confirm the NFT. A-2 preserves previously discovered candidates but cannot help this first discovery. Preconditions: attacker traffic reaches the victim's location and spends the budget before the victim's read; the public roster still omits the buyer and D1 has no candidates for that buyer. Denial lasts while those conditions persist. Add per-network shares or a discovery reserve that one network cannot consume; retain ownerOf as the authority. Upstream billing-plan exhaustion and a resulting sitewide RPC outage were not demonstrated and are not claimed.

**Reproduction**

Executed the real Worker and AuthClient, all four migrations on node:sqlite, real viem-generated EOA signatures and Multicall ABI encoding, with fixture upstreams. Use wallet-harness START, AUTH=20,API=180,CHAIN=20,SEAT=60 per-minute windowLimiters. Victim V owns online registered #361 (agent 51320) according to fakeChain and its NFT index, but fakeImd swarm.owners[361] still names 0x2222222222222222222222222222222222222222 and V has no index_candidates row. Sign V in from 198.51.100.20 without reading home. At each of three minute boundaries, one IP 203.0.113.7 performs 20 fresh-key challenge/sign/verify/home sequences, spaced 2500 ms apart. All sign-ins and home reads are 200: 60 index reads total, none for V. This is 60 HTTP requests/minute, at most 15 in any 10-second interval with this spacing. After each batch, V restores or calls refreshHome(true,true). Expected: a single other network cannot prevent V's seat discovery repeatedly. Actual, asserted for all three minutes: eligible=0,recheck='limited',statusOf='ownershipUnavailable',enterGate='sign-in'. At the fourth minute, stop attacker traffic and refresh V with otherwise identical roster and chain state: eligible=1,statusOf='owner',enterGate='ok'. The attached specialist JavaScript proof (despite its .t.sol filename) was also executed unchanged in memory: both of its tests passed, but its forced upstream outage does not prove real quota exhaustion.

### 7. Info: Remote revocation is incorrectly displayed as session expiry

`source/src/world/auth.ts:205`

```
      if(r.status===401){this.hint.set(null);this.set({session:null,home:null,expired:c==='SESSION_EXPIRED'||!!this.s.session,checking:false});return;}
```

Related to F-4 and W-1. refreshHome marks every 401 received while holding a session as expired. The server returns AUTH_REQUIRED for a revoked session, so logout-all on another device makes this page say 'Session expired'. readSession explicitly distinguishes remote revocation from expiry. Authorization is removed correctly; the defect is misleading status text. Set expired only for SESSION_EXPIRED or when the held session has actually reached expiresAt.

**Reproduction**

Executed the unmodified AuthClient and statusOf at T=2026-09-30T12:00:00Z with a session for 0x1111111111111111111111111111111111111111 expiring T+86400000 and a home with eligible:1. Assert initial status owner. Make the next refreshHome(true) return HTTP 401 {error:'AUTH_REQUIRED'}, the response readSession produces for revoked_at != null. Expected: signed out with expired=false because expiry is still one day away. Actual, asserted: session=null, home=null, expired=true and statusOf=expired. Additionally reproduced end-to-end with a synthetic EOA owning online seat #361: two browsers sign in, browser 2 logout-all returns revoked:2, and the real handler's next home response makes browser 1's AuthClient enter expired.

---

Judge's submission `fda9a5cd337cafee4e453b98ccc3ef7581c3a0680eda6b9484a7c3e79c2acaa4`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
