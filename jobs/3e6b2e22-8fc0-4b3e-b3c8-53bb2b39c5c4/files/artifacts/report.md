# IMD Radar hackathon: all 78 submissions, swarm use and X activity

Research window: **October 22, 2026 UTC** (October 23 in Adelaide). Event-date analysis: **October 7–21, 2026 UTC**. This is an evidence review, not an organizer decision or an independent security audit.

## Answer

**The evidence does not support saying every submission used IMD Swarm or satisfied the launch requirements.** The public entry list contains 78 submissions. This review locates identifiable swarm-related records for **64**; their scope ranges from full contract builds to review-only work, website work, plain-token deployments and parked launch attempts. **11** remain supported only by entrant claims or insufficiently bound leads; **2** explicitly describe proposed/unbuilt IMD integrations; **1** does not explain its integration. “Record” therefore means evidence of some swarm-related work, not a qualifying working product.

The strongest transaction chains separately inspected in this review are **Ouroboros Press** (paid IMD chapter → delivered callback → bounty), **AskSwarm** (paid question → verified-answer path → market settlement → claim), **Pinky** (paid check → signed verdict → bond payout), and **Swarm Harvester** (custom batch claim of IMD launch rewards). They are examples of demonstrated functionality, **not a prize ranking or a finding that their entire submission packets pass**. Other projects may have equally strong evidence that this bounded review did not fully trace.

On X, **76 of 78 submitted project handles returned public profiles**. The direct profile-page sample contains **305 author-matched posts**, of which **240 fall within October 7–21**, spanning **69 accounts**. These are sampled observations, not all event posts. **56 entries name a personal handle; 22 omit one; 10 use the same handle for project and person.** The 56 personal declarations refer to 52 distinct handles, all resolving through the public account relay; their metadata is included per entry, but separate personal timelines were not sampled. Neither a handle in a form nor a public profile authenticates its controller or identifies the lead developer.

The entry census and submitted statements come from [Radar's public submission API](https://www.imdradar.site/api/launchpad?view=hackathon), the endpoint actually used by [the page's JavaScript](https://www.imdradar.site/hackathon.js?v=e721ffc9). Project-specific corroboration and uncertainties are linked in every entry review below.

## Scope, rules and evidence standard

The assignment is to **analyse the submissions**, treating the quoted launch requirements as the evaluation rubric. This report does not launch a token, send transactions or submit another entry.

The [announcement attributed to @surfcoderepeat, October 7](https://x.com/surfcoderepeat/status/2107939454396567581) describes submissions on October 7–21, Ethereum/Robinhood/Base launches, and results by October 23. Radar's [client code](https://www.imdradar.site/hackathon.js?v=e721ffc9) specifies closing at **October 21, 23:59 UTC**. That establishes the collection site's stated cutoff, not an independently recovered signed organizer ruleset. Its static HTML still contains the entry form; the client replaces it after closing. A cached “entries open” label should not override the dated announcement/code.

There is a prize-description discrepancy: the [entry page](https://www.imdradar.site/hackathon) describes a $10,000 pool, while the announcement advertises $15,000+ in rewards. This review neither reconciles the prize valuation nor assumes a payout occurred. Radar describes itself as a community tool unaffiliated with the identity.md team and says organizers set rules/dates.

The rubric asks for a working event-period launch on an approved network; an active custom hook or meaningful custom contract; a working IMD-dependent feature with code, addresses and invocation evidence; project and lead-developer X accounts; and a public reproducible repository, demo, problem/integration explanation, risks/admin permissions, receiving wallet and reused/event-work disclosure. **A standard ERC-20 plus the protocol's initialization guard is not an active custom swap hook. An address is not an invocation receipt. A completed job is not necessarily a deployed launch.**

Evidence labels used below:

| Label | Meaning | What it does not establish |
| --- | --- | --- |
| **Observation / fact** | A retrieved response, source function, transaction status or log directly supports the statement. | Universal correctness, ownership of accounts, demand, or safety. |
| **Entrant claim** | The public submission or project-authored post says it. | Independent verification of delivery, volume, tests or outcomes. |
| **Assessment / inference** | This report's interpretation of the evidence against the rubric. | An organizer ruling. |
| **Unknown / unanswered** | Evidence was absent, inaccessible, incomplete or not checked deeply enough. | That the claimed work certainly did not happen. |

Swarm use is separated into **development** (writing/adapting code or sites), **assurance** (tests/reviews), **release** (protocol deployment/hosting), and **runtime** (the product buys swarm work or relies on an IMD asset/NFT-specific mechanism). Review of imported code is not evidence that agents wrote the original implementation. Launch manifests, accepted nodes and audit counts are protocol-operator records; they are attributable primary records, not external certification. The [official IMD documentation](https://imd.fun/docs/) describes paid work, onchain Intake, oracle callbacks and result/signature validation; it also says payment buys admission rather than a guaranteed result.

## Census and what can be concluded

The API returned **count = 78** and 78 distinct entry IDs/handles. Submission timestamps range from **October 7, 22:02:32.938 UTC** to **October 21, 23:40:08.078 UTC**. **64 entries fill the contract field; 14 leave it blank.** Submitted chain labels total Ethereum 31, Robinhood 31 and Base 5; these are nonexclusive because imdLend lists three chains and IMD Offset lists two. They are entry metadata, not independent verification of all deployments.

Two paginated public IMD launch-index responses were collected: [latest, capped at 500](https://api.imd.fun/launches?limit=1000) and [older than launch 1166](https://api.imd.fun/launches?limit=500&before=1166), returning 500 and 403 records respectively, spanning launch numbers 2457 down to 9 with gaps. **39 submitted contract fields exactly match an artifact in those responses.** That is an observed match count in this snapshot, not proof the other 25 contract-field entries were not built by IMD: some are external deployments, helper contracts, later addresses, or contracts omitted from protocol artifacts. Additional matches were made only where the prose, repository or specific job supports the relationship. Similar names alone were not accepted as identity evidence.

The assessment categories are deliberately broader than eligibility. In particular:

- **Explicit delivery gaps:** STEPS reports a prototype and deployment pending; Proof of Silence proposes its IMD extension; After Market Club asks for development support; moneycanbuy.fun says the core protocol was still being deployed; PLEA says mainnet next. The LastSeen launch record is parked, although its work job is completed.
- **Plain-token traps:** EMBEO launch 944, FINCR launch 2311 and NEETHOME launch 1703 do not themselves deliver the applications described around them. EMBEO and NEETHOME manifests explicitly contain no custom application contracts. FINCR's auction/mining system needs separate deployment evidence.
- **Address/version traps:** the imdUSD entry field is INFER; Tithe's entry field is a hook; Pupate's entry-field address differs from its stated token; Stock DEX's swarm deployment differs from its entry field; several projects have multiple releases. PERK explicitly disclaims Ethereum launch 1663. A reused name or a protocol factory address must not silently substitute for the intended project.
- **Documentation gaps remain:** this review did not rebuild every repository, authenticate wallets, verify every admin's current state, watch every demo, or reconstruct every event-period diff. Consequently **no blanket “fully eligible” verdict is issued**, including for the four transaction-backed examples. Each entry below identifies the next project-specific evidence needed. All also retain the unresolved packet checks in the final section unless explicitly resolved.

## Transaction-backed examples

These are read-only explorer/API observations cross-checked with pinned source. Raw responses and a local integrity check are supplied with the research files. Explorer decoding can assign misleading parameter names to a shared event signature; source semantics take priority.

### Ouroboros Press — an actual contract customer of the swarm

[Launch 2408](https://api.imd.fun/launches/5cddd7dc-a9a2-4615-af12-41abc1092e52) records Robinhood deployment at **`0xfc65446d2c8a7ee6b173d62db710b76bd8bc978a`**, pinned to commit `3468a915f68531f4617dba0e7b29a8126e6cac6a`. The [source](https://github.com/identity-md-launches/launch-2408-ouroborospress/blob/3468a915f68531f4617dba0e7b29a8126e6cac6a/src/OuroborosPress.sol) pays Intake in `commission()`, accepts only its pending request from Intake in `_settle()`, records a chapter in `onResult()`, and attempts a 0.02 IMD commissioner bounty.

| Step | Observed evidence | Conclusion |
| --- | --- | --- |
| Commission chapter 1 | [Successful request transaction](https://robinhoodchain.blockscout.com/tx/0x8b010551056ecf944cbae1eb8f895889690f83bcacea52604d1de6f9632f5ea6), October 21. Intake request ID `0xc07fa2140543836a7a79bac068bb4a1706aa30b0893e7ee2122581ad697dc93d`. | A custom contract actually bought work; this was not just holding IMD. |
| Deliver and reward | [Successful completion transaction](https://robinhoodchain.blockscout.com/tx/0x41bb36518902c547cf2ec0d09e25e189f8329f83394e36e21d8f6e1b4e10eda0) contains the Press chapter log, IMD transfer of `20000000000000000` units, bounty event, and Intake `Completed` with `delivered=true`. | The result callback and 0.02 IMD bounty ran. The request/result hashes bind the steps. |
| Work provenance | [Chapter 1 job](https://explorer.imd.fun/jobs/f50efda3-a8ab-4172-852d-ce747f9f082b) identifies seat 1860; [chapter 2](https://explorer.imd.fun/jobs/c8207062-0178-478e-8056-088f993adaf4) identifies seat 766, with the Press as payer. | Different swarm workers produced identifiable paid outputs. |

**Limit/risk:** this proves delivery mechanics, not the truth or literary quality of the chapters. [The deployment review](https://explorer.imd.fun/jobs/f95cc590-c5c3-4fb5-b81d-7803a1eb4be1) reports a hardcoded 0.5 IMD price: an Intake price increase can strand funds in this ownerless contract. Reset can discard late answers. Its four sampled project X posts are dated October 22, after the collection deadline; that is distinct from the October 21 onchain execution.

### AskSwarm — the cited request needs three more transactions

[Launch 2223](https://api.imd.fun/launches/ffd8f76a-484d-4366-b1d6-a3100b9766e4) records the deployed contracts; the verified addresses are Registry **`0xf3a79f962ec1e75f0087af5491a69dee2a869012`** and Market **`0x6c95a84944b05e7de5000caef80a7c487aa57cb8`**. The [pinned Registry source](https://github.com/identity-md-launches/launch-2223-src-askswarmregistry-sol-src-swarmmarket/blob/712164b6f0121e093dfcd97b2925036becf6019b/src/AskSwarmRegistry.sol) checks Intake callbacks and oracle attestations.

| Step | Observed transaction | What it proves |
| --- | --- | --- |
| Market 3 requests resolution | [Entrant-cited `resolve(3)`](https://robinhoodchain.blockscout.com/tx/0xd0427fa2c2ec98eb53e2dc420856d3686ac5d9facbd5b0f000ee37e60c8b6b78), October 19, block 92,750,360. Intake receives 0.5 IMD; request ID `0x33f5c2eda0e50f1e5f7df2d82e9984202f9ccc8e562008b1a9d97af3dc0057cc`. | A paid question was opened. This one transaction does **not** prove settlement or claim. |
| Oracle callback | [Completion](https://robinhoodchain.blockscout.com/tx/0xcd1682a327b7170c63afc01d86ce5e5ac9b23b408829cce536aaf24631d71b71), block 92,751,060, links that request to oracle request `4f3a459d-5732-4229-8479-04c1249e5f76`; Registry answer logs and Intake delivery are present. | The paid request reached its answer-recording callback. |
| Settle | [Market 3 settlement](https://robinhoodchain.blockscout.com/tx/0xd67f3ca3912ad4aaf0f502df4b579f83c76835701fa0ab6c5f395eaac2aa9ccd) emits phase 3, two 0.1 IMD pools and a 0.002 IMD fee. | Market logic used the resolved path. |
| Claim | [Market 3 claim](https://robinhoodchain.blockscout.com/tx/0xfa833582590612abf77804120b44f1f73f5865ff3bdaafd21faf7dfe4ce15e79) emits a 0.198 IMD claim. | A participant exercised the payout path. |

**Assessment:** the expanded chain supports working runtime integration. It does not establish unique users, market demand or reliability for arbitrary questions. Registry logs also show later `body_refused` and `disagreed` failures; those are evidence of real failure handling, not grounds to portray every request as successful. The first cited transaction's question concerns Bitcoin's genesis date, a demonstration rather than proof of robust prediction-market adjudication.

### Pinky — paid oracle verdict changes bond distribution

[The launch and source linked in entry 69](#entry-69) identify PinkyVault **`0x3c81384aa1ca064316576a214e2fb30969992772`** on Robinhood. The [pinned source](https://github.com/identity-md-launches/launch-1166-pinkystaking-pinkyvault/blob/1476f8303d30a8d2178bee81a41a7b9c3c5c5326/src/PinkyVault.sol) verifies signed attestations, block window and quorum before choosing kept/broken.

For promise **2**, [the successful `ask`](https://robinhoodchain.blockscout.com/tx/0x155985f325e21c9ee41a98d979124febc31525309a4ce918fecbc08a475c3b1e), October 11, pays **0.5 IMD** and emits Intake request `0x22a03095f3a1665e0f469bf10b2afe45f06498761db3810519a18510ad4161fa`. [Completion](https://robinhoodchain.blockscout.com/tx/0xace6361ca31c9f30244c7c4e225f4956c9afe68ada0fd08e2d292b653ae3caa4) links it to oracle `48323d51-a3d8-47fd-a309-b17f8358067e`, emits `Verdict` with **kept=true**, **observedOut=0**, and successful delivery. [Payout](https://robinhoodchain.blockscout.com/tx/0x39907945b8a6d7c0d004d6ea896cce907d472f1bc7b5788ff3682ad3665b749f) distributes **4.5 IMD** back to the maker. The event has a generic signature that the explorer labels as match payouts; the pinned Pinky source names those fields `toMaker`, `bounty`, `toStakers`, `burned`.

**Limit/risk:** this demonstrates a kept promise, not the broken-promise watcher/staker/burn path. PinkyVault retains owner setters for protocol, signer and panel on future terms. The oracle and the contract's authorization assumptions still matter.

### Swarm Harvester — reward utility without pretending a token alone qualifies

[The build/review record](https://explorer.imd.fun/jobs/dc212460-0a28-4e3f-9485-2340b7051f1e) identifies SwarmHarvester **`0x390f407adad27a0f267479a8449d6a5c6daa93cf`**, SwarmSeller and the separate HARVEST token. The [pinned `claimMany` source](https://github.com/identity-md-launches/launch-1029-workflow-contract-stage-context/blob/388f84e9ee292e9a411c0d80c14e8f5f506640eb/src/SwarmHarvester.sol) loops over specified official-distributor-style claims, keeping tokens payable to each named account.

[The October 9 demo transaction](https://etherscan.io/tx/0x2e7e79ed757767e3e9d4ab3ed116912912954523b3d13dffdb80d64ba071526a) succeeded at block **26,152,645**, calls the entered harvester, and its input encodes **40 claim items**. All three log pages were collected: 120 logs include 40 harvester per-item results, all with success=true. This supports 40 successful claim calls through the custom batch function, rather than merely 40 submitted items. It does not prove that every item represents a distinct economic reward, or that a later sell/burn ran; the result counts were checked against the logs rather than inferred from the entry.

**Assessment:** the useful dependency is the swarm's reward-distribution system, even though HARVEST's own launch pool is native-ETH paired. The [job's accepted documentation](https://explorer.imd.fun/jobs/dc212460-0a28-4e3f-9485-2340b7051f1e) expressly corrects that pairing. Sending tokens to a sink and reducing ERC-20 `totalSupply` are different burn semantics and should be described accurately.

## X / Twitter activity

### Method and limits

Direct requests to `https://x.com/<submitted_handle>` returned profile HTML for 76 handles; two returned HTTP 404. The browsing tool separately refused some X pages, but direct public HTML retrieval succeeded. The extractor decodes embedded GraphQL JSON **without executing page scripts**, takes outer tweet objects, deduplicates IDs within each page, excludes quoted/retweeted objects authored by others, and filters by exact author handle and UTC date. Most pages expose only five original objects; pins and logged-out truncation make the sample incomplete. It is not a chronological export or a total post count for the event.

The separate public [FxTwitter relay](https://api.fxtwitter.com/imdradar) supplied profile metadata for 76 handles and individually linked posts for cross-checks. **Follower and lifetime-post numbers below are relayed metadata at acquisition**, not an authenticated X API export. Direct primary posts supply the event-sample observations. The mirror SSSTwitter returned some additional timelines and failures; these were retained as supplemental evidence but **not merged into the primary sample counts**, avoiding double counting or silent mixtures of sampling methods.

The period filter is October 7 00:00 UTC through October 21 23:59:59 UTC, a calendar-date interpretation of the announcement. It does not prove that material posted early on October 7 was built after the formal event opening. October 22 posts remain in the evidence files but are excluded from event counts. Engagement is a later snapshot of posts dated during the event, not engagement measured as of the deadline. Views are not unique viewers, summed views are not audience reach, and lifetime counts include pre-event/unrelated activity.

### Findings

**Observation:** the metadata median is **35.5 followers** among the 76 resolving handles; **27 have fewer than 10**. Existing personal/general accounts such as @tungweb3, @xmrscn and @stockroom carry substantial unrelated lifetime history. Comparing their lifetime post totals with newly created project accounts would misstate hackathon effort. @stepstoke and @pleaimd returned zero posts in the primary snapshot. @ouroborospress_ had four sampled posts, all on October 22; @heroboost_me's project explanation also appears after closing. A zero event sample is **not** proof an account was inactive or did not exist by the deadline.

| Attributable example | Observed activity | Assessment and limit |
| --- | --- | --- |
| [IMD6900 mint announcement, October 11](https://x.com/IMD6900/status/2109305368408993810) | 103 likes, 3 reposts, 45 replies, 8,620 displayed views. | Largest like count in the bounded primary entrant sample. It promotes Worker Frens, not the submitted LARP release; ecosystem attention must not substitute for evidence about that submission. |
| [imdLend explanation, October 17](https://x.com/sudeepb02/status/2111540462851088575) | 55 likes, 11 reposts, 4 replies, 9,144 views; followed by a [live announcement](https://x.com/sudeepb02/status/2111544514225844459) with 46 likes. | Specific product communication with an article/demo lead, more informative than a ticker mention. Engagement does not verify rental safety or deployment parity. |
| [IDM launch, October 20](https://x.com/theidmfun/status/2112578279937036723) | 57 likes, 5 reposts, 17 replies, 5,387 views; identifies the actual token and drum-machine hook. | Directly connects the public demo to the entered artifact. A [later feature post](https://x.com/theidmfun/status/2112942601573949760) distinguishes planned stations/subscriptions from the live sequencer. |
| [Pinky explanation, October 10](https://x.com/pinkybond_fun/status/2108878028814315521) | 56 likes, 3 reposts, 45 replies, 2,368 views. | Explains the oracle/bond problem in concrete terms; the receipt chain above independently supports a kept-promise example. Replies are not evidence of independent users or unique supporters. |
| [Radar switches its entry to IMD Vault, October 19](https://x.com/imdradar/status/2112201269800522173) | Publicly distinguishes its competition entry from the broader Radar site. | The host/curator is also an entrant. This is a disclosure/context fact; no claim of judging misconduct follows. Its curated homepage is not an impartial all-entry activity sample. |
| [moneycanbuy.fun token launch](https://x.com/moneycanbuy_fun/status/2112848871332118634) and [core protocol still building](https://x.com/moneycanbuy_fun/status/2112899516240478654), October 21 | Separate posts distinguish YOLO from the actual dares/escrow protocol. | Good evidence of development communication and its limit: a launched token does not prove the core product was ready. |
| [Hamster early-access promotion](https://x.com/hamsterhourgame/status/2111349317952999927) | Asks for a wallet and repost for early access. | An observable engagement incentive. This can inflate response metrics; it is not evidence of bots, fake accounts or misconduct. |
| [HeroBoost's supplied personal-account post](https://x.com/bezu0012/status/2112972101535883550) | A conditional-tip invitation, not a technical integration walkthrough. | The entry labels it a thread; the retrieved post alone does not substantiate the broader technical claims. |

**Inference:** the observable activity combines product demos, shipping/audit updates, community amplification, speculative promotion and incentives. Posts with a source/job/contract/receipt trail carry more technical information than engagement counts. **Unknown:** full posting cadence, deleted posts, impression histories, follower authenticity, paid promotion, conversion into independent users, and control of project/personal accounts. No bot, wash-engagement, fraud or plagiarism finding is made from these samples.

Radar's [published impact configuration](https://www.imdradar.site/tokens.js?v=739b938e) is dated **October 8**. Its [formula](https://www.imdradar.site/app.js?v=8c46c813) uses logarithmic 40% follower reach and 60% engagement, with interactions weighted as likes + 2×reposts + 2×replies. Those are a curator's dated, small-sample scores, not current all-submission rankings. The curated homepage tweet endpoint returned a single October 15 post in this acquisition, another reason not to infer ecosystem-wide activity from a “Today on X” label.

The following 78 entry reviews include each account's followers/lifetime posts and primary event-sample count. `0` is an observed zero in that returned sample; `unavailable` means the public profile could not be retrieved. The full rows and post-level URLs/text/timestamps are in `research/x-activity.csv` and `research/x-posts.json`.

## All submissions: individual evidence and gaps

Order follows the API, newest entry first. Each feature summary is the entrant's described mechanism unless the evidence paragraph or transaction section explicitly corroborates execution. **Record** denotes some corroborated swarm-related work; **Claim**, **Planned** and **Unclear** have the meanings given in the answer. Submitted contract/network fields and personal handles are attributed form data, not proof of ownership, chain approval or contract identity. “Deployment” links below prove the recorded release step only, not a live feature invocation.


<a id="entry-1"></a>

### 01. @imd_optmizer — Claim

Entry `0d13d5af0c4ba452` · submitted 2026-10-21T23:40:08.078Z.

**Submitted contract:** `0x61cef4f8ab5dc658189e95f1570031d3b50b09a6` · [ethereum explorer](https://etherscan.io/address/0x61cef4f8ab5dc658189e95f1570031d3b50b09a6).

**Swarm evidence and scope:** No matching optimizer job or launch was found for the submitted address; Sepolia tests and later swarm consensus are entrant claims.

**Described IMD feature:** MEV detection, arbitrage and IMD routing are described; swarm consensus is a future goal.

**Assessment / unanswered:** Provide the exact paid swarm job, deployed network and successful custom-logic receipt. The entry reports an X suspension; the submitted handle currently resolves through the relay.

**Sources / leads:** [submission census](https://www.imdradar.site/api/launchpad?view=hackathon).

**X:** [@imd_optmizer](https://x.com/imd_optmizer) · 5 followers; 8 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 3 dated in the event window. [Example sampled event post](https://x.com/Imd_Optmizer/status/2112164100071633016). Personal handle declared: [@buildercoin](https://x.com/buildercoin) (relay resolves: 13 followers, 73 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-2"></a>

### 02. @stepstoke — Record

Entry `999cc781297f6021` · submitted 2026-10-21T23:36:47.227Z.

**Submitted contract:** none in the contract field; additional prose/linked artifacts may supply one.

**Swarm evidence and scope:** The linked STEPS job records implementation and independent reviews of a release candidate.

**Described IMD feature:** A funded project relay would commission IMD work and reuse accepted checkpoints.

**Assessment / unanswered:** The entry explicitly says prototype only, gas-limit blocker, browser issues and deployment pending. Swarm development is supported; a working launch is not.

**Sources / leads:** [job 395064a3](https://explorer.imd.fun/jobs/395064a3-ae28-4477-89c2-9435e70bb7e8) · [entrant repository](https://github.com/identity-md-launches/launch-2393-prepare-steps-stepstoke-release-candidat).

**X:** [@stepstoke](https://x.com/stepstoke) · 1 followers; 0 lifetime posts (relay metadata). Direct profile sample: 0 authored posts, 0 dated in the event window. Personal handle declared: [@goderbug](https://x.com/goderbug) (relay resolves: 282 followers, 1,226 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-3"></a>

### 03. @swornbyswarm — Record

Entry `ad3581d8e84796bc` · submitted 2026-10-21T22:49:06.897Z.

**Submitted contract:** `0x0da2679000ea5380d1361cc3cca7d4e8c881f766` · [ethereum explorer](https://etherscan.io/address/0x0da2679000ea5380d1361cc3cca7d4e8c881f766).

**Swarm evidence and scope:** Launch 2404 matches the submitted Registry; the linked workflow records contract construction, reviews, deployment and site work.

**Described IMD feature:** Wallet traits combine chain reads with paid IMD oracle claims; cards and new specifications charge IMD.

**Assessment / unanswered:** Need a successful mint/oracle-claim receipt and fee/burn trace. This is an ERC-721 registry rather than a separate ERC-20 coin.

**Accepted worker assignments recorded:** implement seats #1345; integrate seats #463; review seats #2, #535, #1246, #1295 and others; tests seats #721. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2404 (live)](https://api.imd.fun/launches/1377d17c-3f09-49e8-87e7-20a07ad45ea9) · [source c4ff3238](https://github.com/identity-md-launches/launch-2404-renderer-composer-registry/tree/c4ff3238390fc51962fb67e86affc20cf418126e) · [deployment](https://etherscan.io/tx/0x2f65613f267fc2a5eb38efc3c1534fe47b184bd5f63f7bda975f6a17136016cf).

**X:** [@swornbyswarm](https://x.com/swornbyswarm) · 59 followers; 13 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 3 dated in the event window. [Example sampled event post](https://x.com/swornbyswarm/status/2111020470783074721). Personal handle declared: [@cryptokarlheinz](https://x.com/cryptokarlheinz) (relay resolves: 722 followers, 2,858 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-4"></a>

### 04. @requiem__dream — Record

Entry `c9af1cb619036513` · submitted 2026-10-21T21:56:08.280Z.

**Submitted contract:** none in the contract field; additional prose/linked artifacts may supply one.

**Swarm evidence and scope:** The Hooks Store has identifiable swarm development jobs. The specific listing-contract job inspected is dated October 22, after closing.

**Described IMD feature:** The entrant describes a paid IMD hook-building interface and an IMD-priced listing system.

**Assessment / unanswered:** Separate the pre-deadline working product from October 22 additions. No contract is in the entry; provide a user launch receipt and repository/version for judging.

**Accepted worker assignments recorded:** implement seats #712; integrate seats #410; review seats #912, #1183, #1836, #1875 and others; tests seats #222. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [job c2b72f7e](https://explorer.imd.fun/jobs/c2b72f7e-31f3-42e2-84b4-730165ce5310) · [job 7f951ad8](https://explorer.imd.fun/jobs/7f951ad8-ac62-41f0-b968-79737c96623e).

**X:** [@requiem__dream](https://x.com/requiem__dream) · 558 followers; 107 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/requiem__dream/status/2112620141242700226). Personal handle declared: [@requiem__dream](https://x.com/requiem__dream) (same handle as project) (relay resolves: 558 followers, 107 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-5"></a>

### 05. @Imdirectorb — Record

Entry `3bb7b68fdbfc823a` · submitted 2026-10-21T21:53:23.994Z.

**Submitted contract:** `0xecb5e7f3b9839eb083dda95099b8438ecebec16e` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0xecb5e7f3b9839eb083dda95099b8438ecebec16e).

**Swarm evidence and scope:** Launch 2418 and its audit/deployment job match Director and IMDPhysicalHook on Robinhood Chain.

**Described IMD feature:** Swap events are intended to trigger commands in a physical-device gateway.

**Assessment / unanswered:** The launch proves the hook was deployed, not that a device acted. The X demo is a project announcement with media, not an independently verified hardware execution trace.

**Accepted worker assignments recorded:** implement seats #822; integrate seats #1004; review seats #102, #544, #1176, #1357 and others; tests seats #740. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2418 (live)](https://api.imd.fun/launches/5992ada2-68e1-4af2-ad6d-47d67e09f703) · [source 41e3e33d](https://github.com/identity-md-launches/launch-2418-review-test-audit-launch/tree/41e3e33df7215df0845ff642c75fd0f6c8b32142) · [deployment](https://robinhoodchain.blockscout.com/tx/0xf6750d8919c43192add6432b7a68f395273563c6fb25c358a089280370aeeccd).

**X:** [@Imdirectorb](https://x.com/Imdirectorb) · 14 followers; 10 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 4 dated in the event window. [Example sampled event post](https://x.com/Imdirectorb/status/2113026769531842999). Personal handle declared: [@DmitryiBond](https://x.com/DmitryiBond) (relay resolves: 69 followers, 177 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-6"></a>

### 06. @byEugenVoyager — Planned

Entry `2ce5c904476bb29f` · submitted 2026-10-21T19:43:52.598Z.

**Submitted contract:** none in the contract field; additional prose/linked artifacts may supply one.

**Swarm evidence and scope:** The entrant explicitly calls the IMD integration a proposed extension, not a completed feature.

**Described IMD feature:** Paid IMD source research and claim review are planned for an existing editorial beta.

**Assessment / unanswered:** No contract, paid IMD work receipt or completed IMD-dependent path is supplied. Existing AI research alone cannot establish IMD use.

**Sources / leads:** [submission census](https://www.imdradar.site/api/launchpad?view=hackathon).

**X:** [@byEugenVoyager](https://x.com/byEugenVoyager) · 91 followers; 82 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 0 dated in the event window. Personal handle declared: [@byEugenVoyager](https://x.com/byEugenVoyager) (same handle as project) (relay resolves: 91 followers, 82 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-7"></a>

### 07. @ouroborospress_ — Record

Entry `8b7d12fddde3c2df` · submitted 2026-10-21T19:16:27.168Z.

**Submitted contract:** `0xfc65446d2c8a7ee6b173d62db710b76bd8bc978a` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0xfc65446d2c8a7ee6b173d62db710b76bd8bc978a).

**Swarm evidence and scope:** Launch 2408 records review and deployment of imported OuroborosPress code; chapter jobs identify separate swarm writers.

**Described IMD feature:** The contract pays Intake for chapters, records delivered hashes and pays a commissioner bounty.

**Assessment / unanswered:** A complete paid commission/callback/bounty cycle is corroborated below. Fixed Intake pricing and discarded late results are disclosed audit risks; project-account posts sampled here are after closing.

**Accepted worker assignments recorded:** integrate seats #1140; review seats #1905. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2408 (live)](https://api.imd.fun/launches/5cddd7dc-a9a2-4615-af12-41abc1092e52) · [source 3468a915](https://github.com/identity-md-launches/launch-2408-ouroborospress/tree/3468a915f68531f4617dba0e7b29a8126e6cac6a) · [deployment](https://robinhoodchain.blockscout.com/tx/0x43a78419b0ec1aef6284cfdc8e0e2e51ed00a89ceecb4dd418dfda8a1a8cef6f) · [entrant repository](https://github.com/AaroneGeorge/ouroboros-press).

**X:** [@ouroborospress_](https://x.com/ouroborospress_) · 8 followers; 4 lifetime posts (relay metadata). Direct profile sample: 4 authored posts, 0 dated in the event window. Personal handle declared: [@_aaronegeorge](https://x.com/_aaronegeorge) (relay resolves: 355 followers, 1,478 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-8"></a>

### 08. @LastSeenIMD — Record

Entry `2b6c5c3fcfb46c40` · submitted 2026-10-21T19:15:22.940Z.

**Submitted contract:** none in the contract field; additional prose/linked artifacts may supply one.

**Swarm evidence and scope:** An exact LastSeenRegistry deployment job exists and records swarm adaptation, tests and reviews.

**Described IMD feature:** An IMD oracle is intended to validate wallet accusations and bounty leads.

**Assessment / unanswered:** Its launch is parked despite the job being completed, with a reported lead-seat takeover blocker. Do not treat completed work as successful deployment or the entry's live-registry wording as established.

**Accepted worker assignments recorded:** implement seats #1368; integrate seats #1979; review seats #97, #358, #461, #658 and others; tests seats #1965. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [job 492fe9cf](https://explorer.imd.fun/jobs/492fe9cf-1f0a-453d-9a29-e88b442fed81) · [entrant repository](https://github.com/Alok-mad98/lastseenimd).

**X:** [@LastSeenIMD](https://x.com/LastSeenIMD) · 6 followers; 2 lifetime posts (relay metadata). Direct profile sample: 1 authored posts, 1 dated in the event window. [Example sampled event post](https://x.com/LastSeenIMD/status/2109321045547295012). Personal handle declared: [@AcayDr](https://x.com/AcayDr) (relay resolves: 697 followers, 6,798 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-9"></a>

### 09. @heroboost_me — Record

Entry `bf292a50b8643af9` · submitted 2026-10-21T18:58:23.337Z.

**Submitted contract:** `0x57ac054c81ac82b95fb8701c0ee2cd94a4df7b35` · [base explorer](https://basescan.org/address/0x57ac054c81ac82b95fb8701c0ee2cd94a4df7b35).

**Swarm evidence and scope:** The submitted oracle job has a signed answer, while the Base receipt reaches the entered Boost Diamond.

**Described IMD feature:** A Boost is described as binding an IMD yes/no result to conditional funding.

**Assessment / unanswered:** The oracle question checks HeroBoost's own feature description. The create transaction alone does not prove funds were released conditionally on that answer. Check cross-chain/result binding and proxy permissions.

**Sources / leads:** [job 2c6652c6](https://explorer.imd.fun/jobs/2c6652c6-7239-4d6c-b8ca-908bb1ecae75).

**X:** [@heroboost_me](https://x.com/heroboost_me) · 3 followers; 4 lifetime posts (relay metadata). Direct profile sample: 3 authored posts, 0 dated in the event window. Personal handle declared: [@bezu0012](https://x.com/bezu0012) (relay resolves: 90 followers, 144 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-10"></a>

### 10. @imdradar — Record

Entry `addf2a596f14a172` · submitted 2026-10-21T17:34:36.366Z.

**Submitted contract:** `0xdbaff609cd0500527a2a102f5cbbbbc70fd2ff5b` · [ethereum explorer](https://etherscan.io/address/0xdbaff609cd0500527a2a102f5cbbbbc70fd2ff5b).

**Swarm evidence and scope:** Launches 2244 and 2251 record audited VaultFactory deployments on Ethereum and Robinhood.

**Described IMD feature:** Projects pay IMD to create constrained treasury/vesting vaults; fees go to an immutable recipient.

**Assessment / unanswered:** A successful funded lock and permitted/blocked withdrawal receipt is still needed. The fee recipient is a trust boundary; source immutability does not prove how received fees are later spent. Personal handle is omitted.

**Accepted worker assignments recorded:** implement seats #559, #877; integrate seats #399, #1042; review seats #3, #368, #558, #581 and others; tests seats #286, #911. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2244 (live)](https://api.imd.fun/launches/d4303b9d-4c8d-4548-9dc4-a10e770c5d53) · [source ccfe47ac](https://github.com/identity-md-launches/launch-2244-audit-deploy-imd-vault/tree/ccfe47ac07f63b69ffa62313878343f4569b0756) · [deployment](https://etherscan.io/tx/0x7aa61ef647023da5d49b7fc0d18fd56cfe43b45f5c00719d37af4a0040e78d38) · [launch 2251 (live)](https://api.imd.fun/launches/76fe1985-1f08-416b-88da-6aa5a21eaa4e) · [source 1ba921a5](https://github.com/identity-md-launches/launch-2251-deploy-audited-imd-vault/tree/1ba921a5d3f218861bfd44e8f71cf7fd8398a64b) · [deployment](https://robinhoodchain.blockscout.com/tx/0xa8195965dc33e601c2568d809236152d5b83d2f67c5b6cbabd79d83ecce67703) · [entrant repository](https://github.com/Jamesjady/imd-vault).

**X:** [@imdradar](https://x.com/imdradar) · 991 followers; 208 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/imdradar/status/2110765083311689890). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-11"></a>

### 11. @SigmoidIMD — Claim

Entry `b34710a53d3eca3b` · submitted 2026-10-21T17:26:23.902Z.

**Submitted contract:** `0x51871f67273a56cdbdd8d9a936a98d3032cb60c8` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x51871f67273a56cdbdd8d9a936a98d3032cb60c8).

**Swarm evidence and scope:** The entry describes fork tests and a live FairLaunchpad, but the address did not match collected IMD launch artifacts and exact-name job searches found no matching build.

**Described IMD feature:** An IMD launch hook is said to impose dynamic anti-sniper fees, caps and a circuit breaker.

**Assessment / unanswered:** The referenced SWARMLER launch is the attack comparator, not proof Sigmoid used the swarm. Supply the FairOpenHook job, source pin and live swap/revert receipts.

**Sources / leads:** [project launch post](https://x.com/SigmoidIMD/status/2112969381550432719) · [linked repository](https://github.com/n0krayy/FairOpenHook).

**X:** [@SigmoidIMD](https://x.com/SigmoidIMD) · 20 followers; 18 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 4 dated in the event window. [Example sampled event post](https://x.com/SigmoidIMD/status/2112969381550432719). Personal handle declared: [@0drayne](https://x.com/0drayne) (relay resolves: 1,745 followers, 7,639 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-12"></a>

### 12. @pfwafun — Record

Entry `c8e5afcd23c5b3e4` · submitted 2026-10-21T15:32:46.103Z.

**Submitted contract:** none in the contract field; additional prose/linked artifacts may supply one.

**Swarm evidence and scope:** The linked Sherwood v2 audit/deployment job and launch 1389 are identifiable swarm work on Robinhood Chain.

**Described IMD feature:** An IMD trading pool drives a game pot, points, prizes and token purchases/burns.

**Assessment / unanswered:** The entry supplies a separate hook and pool, but no full settlement transaction. Match those to the launcher and prove the stated later live pool and payout/burn cycle.

**Accepted worker assignments recorded:** implement seats #1929; integrate seats #1614; review seats #130, #460, #560, #880 and others; tests seats #205. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1389 (live)](https://api.imd.fun/launches/50787239-e9b1-4891-b169-e0f0d38a850e) · [source bd9dc1dd](https://github.com/identity-md-launches/launch-1389-audit-deploy-sherwood-v2/tree/bd9dc1ddac3a7a192f4c2fb10adc79afe92fe117) · [deployment](https://robinhoodchain.blockscout.com/tx/0x8e328a10fb218f689e89d4f207c43700243b223fd733382e27b3ca0575da1d1b).

**X:** [@pfwafun](https://x.com/pfwafun) · 1,886 followers; 1,544 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 1 dated in the event window. [Example sampled event post](https://x.com/pfwafun/status/2108652156735623223). Personal handle declared: [@miracleotugo](https://x.com/miracleotugo) (relay resolves: 2,361 followers, 21,709 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-13"></a>

### 13. @tungweb3 — Record

Entry `532a35eda6957602` · submitted 2026-10-21T15:29:17.942Z.

**Submitted contract:** `0x2b82cdeb8477415d541799abb0cc48044c8ea5f3` · [ethereum explorer](https://etherscan.io/address/0x2b82cdeb8477415d541799abb0cc48044c8ea5f3).

**Swarm evidence and scope:** The entered EMBEO address matches launch 944, a standard token issuance by the swarm.

**Described IMD feature:** The entrant reports later audit work for a 3D world and plans holder/game benefits.

**Assessment / unanswered:** Launch 944 expressly deploys a plain ERC-20 with an initialization-only guard, not a custom swap hook or application. The token deployment alone fails the functionality requirement; later utility needs its own proof.

**Accepted worker assignments recorded:** implement seats #1434; integrate seats #1673; review seats #826, #1457, #1581, #1763 and others; tests seats #1654. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 944 (live)](https://api.imd.fun/launches/b81f8d6e-ebc0-4eb0-9307-d22cf765bea4) · [source cecf25b9](https://github.com/identity-md-launches/launch-944-emberevo-token-symbol-embeo/tree/cecf25b92d44568f8a0f81c34f4b634df905d1e5) · [deployment](https://etherscan.io/tx/0xd926c03bafe9e92252b37f44a0ea7bf1116f5c8a8cefb2aee7a3d28363d6aa09).

**X:** [@tungweb3](https://x.com/tungweb3) · 4,610 followers; 10,945 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 4 dated in the event window. [Example sampled event post](https://x.com/tungweb3/status/2112935852024471991). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-14"></a>

### 14. @inkandinference — Record

Entry `8a40f89998b5d0c6` · submitted 2026-10-21T15:29:10.793Z.

**Submitted contract:** `0x45d4cd12ced01d4316a6021387cfdee2fd9491a7` · [ethereum explorer](https://etherscan.io/address/0x45d4cd12ced01d4316a6021387cfdee2fd9491a7).

**Swarm evidence and scope:** INK launches 2321 and 2305 and the linked contract, hook, testnet, audit and site jobs corroborate extensive swarm work.

**Described IMD feature:** InkFeeRouter is described as routing IMD revenue to treasury and INK into liquidity, alongside seat-based portraits.

**Assessment / unanswered:** The entered router address is separate from the main launch artifacts. Verify its source and claimAndRoute receipt; NFT/liquidity contracts retain owner roles in the deployment manifest.

**Accepted worker assignments recorded:** implement seats #1030, #1925; integrate seats #180, #926; review seats #47, #358, #440, #461 and others; tests seats #39, #1274. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2321 (live)](https://api.imd.fun/launches/d545b1c4-f052-449e-81b4-06d9ed677af1) · [source 620960b3](https://github.com/identity-md-launches/launch-2321-src-inkhook-sol/tree/620960b344306b3469330eb0a6f9fb2a48c329a5) · [deployment](https://etherscan.io/tx/0xa4d254ca8affc1da17b3cb012175cf2193f02980bba0d1a1929f67767b58b354) · [launch 2305 (live)](https://api.imd.fun/launches/7833501f-1f99-4659-832a-290999ffc03f) · [source 57970230](https://github.com/identity-md-launches/launch-2305-deploy-nft-vault-liquidity/tree/579702304e4d69d564c94203113a782307375729) · [deployment](https://etherscan.io/tx/0x0d735a1cfa76baace8548e7b3310c527717fd29a819febd0370f756049a171c1) · [job 45527f4a](https://explorer.imd.fun/jobs/45527f4a-322a-441e-b653-67e01224d0e9).

**X:** [@inkandinference](https://x.com/inkandinference) · 103 followers; 37 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/inkandinference/status/2113012996289007659). Personal handle declared: [@edugrooves](https://x.com/edugrooves) (relay resolves: 3,064 followers, 56,702 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-15"></a>

### 15. @moneycanbuy_fun — Record

Entry `8b49a20f3479ceeb` · submitted 2026-10-21T14:56:57.996Z.

**Submitted contract:** `0x49e55a87aa4bb0d2fd58fdcf1a31c9612de015dc` · [ethereum explorer](https://etherscan.io/address/0x49e55a87aa4bb0d2fd58fdcf1a31c9612de015dc).

**Swarm evidence and scope:** The entered address matches YOLO launch 2364; the entry distinguishes token launch from still-pending core protocol deployment.

**Described IMD feature:** IMD bonds, paid swarm appeals and identity.md NFT voting are intended to adjudicate paid dares.

**Assessment / unanswered:** Do not substitute the YOLO launch for a live escrow/dispute cycle. The entry explicitly says core deployment was not finished at submission.

**Accepted worker assignments recorded:** implement seats #1576; integrate seats #225; review seats #11, #560, #1444, #1501 and others; tests seats #327. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2364 (live)](https://api.imd.fun/launches/a3cf5033-4522-4a83-bd9c-584be10351fc) · [source 0b50e441](https://github.com/identity-md-launches/launch-2364-launch-yolo-token-support/tree/0b50e441ed68cdf4176c79e8671018766bd48198) · [deployment](https://etherscan.io/tx/0x33b1f4491e7efebf713fc2a22b1a3916388c51994d929a927ae77967ee0c190e) · [entrant repository](https://github.com/sergey-mavr-agent/moneycanbuy.fun).

**X:** [@moneycanbuy_fun](https://x.com/moneycanbuy_fun) · 101 followers; 49 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 4 dated in the event window. [Example sampled event post](https://x.com/moneycanbuy_fun/status/2112848871332118634). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-16"></a>

### 16. @theimddaily — Record

Entry `3831923bea159e49` · submitted 2026-10-21T12:03:06.125Z.

**Submitted contract:** none in the contract field; additional prose/linked artifacts may supply one.

**Swarm evidence and scope:** The exact newspaper build/deploy job identifies swarm-written contracts and a hosted frontend.

**Described IMD feature:** ERC-1155 editions are described as mintable for IMD during a fixed 24-hour period.

**Assessment / unanswered:** The entry omits its contract field. Provide the edition contract, mint receipt and event-period publication record; confirm the publisher's powers and payment vault.

**Accepted worker assignments recorded:** implement seats #490; integrate seats #1299; review seats #92, #123, #130, #563 and others; tests seats #452. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [job ae8a24f3](https://explorer.imd.fun/jobs/ae8a24f3-a95d-4905-aff8-222404e085e6).

**X:** [@theimddaily](https://x.com/theimddaily) · 0 followers; 2 lifetime posts (relay metadata). Direct profile sample: 2 authored posts, 1 dated in the event window. [Example sampled event post](https://x.com/theimddaily/status/2112875471046390193). Personal handle declared: [@kilicsln](https://x.com/kilicsln) (relay resolves: 7,350 followers, 1,177 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-17"></a>

### 17. @imdgenesis — Record

Entry `3ec49c445a2e689a` · submitted 2026-10-21T06:41:12.025Z.

**Submitted contract:** `0x06f8ceff95e5d72887c575d2759e36230b711d06` · [ethereum explorer](https://etherscan.io/address/0x06f8ceff95e5d72887c575d2759e36230b711d06).

**Swarm evidence and scope:** The entered GenesisResearch address matches launch 2322 and a pinned source repository.

**Described IMD feature:** The entrant describes a paid IMD hypothesis proposal that feeds a deterministic experiment and public journal.

**Assessment / unanswered:** The judges/replay pages are entrant evidence. Independently link the proposal job, delivered artifact hash and engine input; a deployment receipt alone does not prove that end-to-end research cycle.

**Accepted worker assignments recorded:** implement seats #1646; integrate seats #1618; review seats #61, #420, #528, #1514 and others; tests seats #1966. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2322 (live)](https://api.imd.fun/launches/ba15aa1d-afc1-4274-862e-cd0614e3af29) · [source d5c4307c](https://github.com/identity-md-launches/launch-2322-genesisresearch/tree/d5c4307c5625c94b2106a861aac0646a5f4dc1e4) · [deployment](https://etherscan.io/tx/0x8549f90154b6e1b22c60a98ae71a3f78003640ca735cd9a5d7219f7eb21941b6).

**X:** [@imdgenesis](https://x.com/imdgenesis) · 9 followers; 3 lifetime posts (relay metadata). Direct profile sample: 2 authored posts, 2 dated in the event window. [Example sampled event post](https://x.com/imdgenesis/status/2112859539108508062). Personal handle declared: [@0maxxdev](https://x.com/0maxxdev) (relay resolves: 141 followers, 282 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-18"></a>

### 18. @visualimd — Record

Entry `7fa320b3743058ad` · submitted 2026-10-21T03:54:12.608Z.

**Submitted contract:** none in the contract field; additional prose/linked artifacts may supply one.

**Swarm evidence and scope:** The PERK site job explicitly uses the visual package, and a VisualIdentity.md community-entry job exists.

**Described IMD feature:** A reusable visual preset and proposed seat-holder art submission/voting mechanism are described.

**Assessment / unanswered:** Do not count PERK's separate deployment as VIMD's custom logic. Provide the voting contract, burn/vote receipt and package/event work attribution.

**Accepted worker assignments recorded:** implement seats #115, #646; integrate seats #687; review seats #249, #558, #606, #976 and others; tests seats #1614. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [job 8397b3aa](https://explorer.imd.fun/jobs/8397b3aa-732c-4cf9-80d5-a1ed917ccc0b) · [job a7227c55](https://explorer.imd.fun/jobs/a7227c55-15c6-473d-8584-898317adf043) · [entrant repository](https://github.com/blockmerchantlabs/vimd-family).

**X:** [@visualimd](https://x.com/visualimd) · 1 followers; 1 lifetime posts (relay metadata). Direct profile sample: 1 authored posts, 1 dated in the event window. [Example sampled event post](https://x.com/visualimd/status/2110116817670672568). Personal handle declared: [@Block_Merchant](https://x.com/Block_Merchant) (relay resolves: 3,594 followers, 20,435 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-19"></a>

### 19. @theidmfun — Record

Entry `2ad0aaf1b5a15930` · submitted 2026-10-20T21:39:11.529Z.

**Submitted contract:** `0x4fe9f3823791c8b187b81ab8b7398d793fed28f6` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x4fe9f3823791c8b187b81ab8b7398d793fed28f6).

**Swarm evidence and scope:** Launch 2303 matches the entered IDM token and records SequencerHook review/deployment.

**Described IMD feature:** Trades modify an onchain sequencer; the entrant describes a fee burn and a market-driven music interface.

**Assessment / unanswered:** The pool is IDM/ETH. Swarm-built creative logic is supported, but active swaps, the burn path and any IMD runtime demand need separate receipts; planned station subscriptions are not completed evidence.

**Accepted worker assignments recorded:** implement seats #32; integrate seats #963; review seats #1198, #1497, #1501, #1678 and others; tests seats #281. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2303 (live)](https://api.imd.fun/launches/8122e3ef-fedd-466b-b884-ac647119946f) · [source 79351314](https://github.com/identity-md-launches/launch-2303-review-launch-token-named/tree/793513141b37fa52419c18a1398070e462badd1b) · [deployment](https://robinhoodchain.blockscout.com/tx/0x0d8422d441fb766e74ce291f728745f08533767547ebf032215f1e417b43a13d).

**X:** [@theidmfun](https://x.com/theidmfun) · 213 followers; 70 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 1 dated in the event window. [Example sampled event post](https://x.com/theidmfun/status/2112578279937036723). Personal handle declared: [@badfriend](https://x.com/badfriend) (relay resolves: 1,936 followers, 4,316 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-20"></a>

### 20. @imdcontrol — Claim

Entry `bff51231456fda5e` · submitted 2026-10-20T21:26:16.778Z.

**Submitted contract:** `0xd7dc08c749d2581e1a2b84bad8b64d0575a06163` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0xd7dc08c749d2581e1a2b84bad8b64d0575a06163).

**Swarm evidence and scope:** The entry describes job.open/API use and a Robinhood recurring-request contract, but supplies no job, repository, contract or receipt.

**Described IMD feature:** A work-management interface coordinates paid IMD tasks and owner-controlled recurring oracle requests.

**Assessment / unanswered:** A resolving project account/site supports identity, not technical execution. Provide one actual request and callback plus the recurring contract's limits/admin controls.

**Sources / leads:** [submission census](https://www.imdradar.site/api/launchpad?view=hackathon).

**X:** [@imdcontrol](https://x.com/imdcontrol) · 2 followers; 1 lifetime posts (relay metadata). Direct profile sample: 1 authored posts, 1 dated in the event window. [Example sampled event post](https://x.com/imdcontrol/status/2112655125965951078). Personal handle declared: [@vedx02](https://x.com/vedx02) (relay resolves: 801 followers, 5,171 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-21"></a>

### 21. @HELPWANTED_imd — Record

Entry `ece3d42b7a2b271d` · submitted 2026-10-20T20:07:31.930Z.

**Submitted contract:** `0x730cb6c845d896e33283d3a4ed8967f8baa778d2` · [ethereum explorer](https://etherscan.io/address/0x730cb6c845d896e33283d3a4ed8967f8baa778d2).

**Swarm evidence and scope:** The entered WorkOrders contract matches launch 1573, with WorkProof, Doorbell and CrowdPots in the same deployment.

**Described IMD feature:** IMD work escrow pays against WorkRegistry receipt evidence and tips accepted workers' seat owners.

**Assessment / unanswered:** The claimed Doorbell/Rule hires need receipt-level settlement and tip checks. The no-token design may need organizer interpretation under the task's token-project wording.

**Accepted worker assignments recorded:** implement seats #1637; integrate seats #225; review seats #205, #286, #826, #963 and others; tests seats #507. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1573 (live)](https://api.imd.fun/launches/90de809f-6038-4f0c-9a1f-f3711ea865a9) · [source 99f4ab09](https://github.com/identity-md-launches/launch-1573-please-deploy-repository-contracts/tree/99f4ab0997bc8c9717f2203d8f3834f15d3220e1) · [deployment](https://etherscan.io/tx/0xfb28bef9c477cfe3777231d8c41f202e691673fc4cec98ecb8b07f1bfff7bf9c) · [entrant repository](https://github.com/OoJae/help-wanted).

**X:** [@HELPWANTED_imd](https://x.com/HELPWANTED_imd) · 1 followers; 10 lifetime posts (relay metadata). Direct profile sample: 3 authored posts, 3 dated in the event window. [Example sampled event post](https://x.com/HELPWANTED_imd/status/2112561163250610597). Personal handle declared: [@_OoJae](https://x.com/_OoJae) (relay resolves: 1,003 followers, 9,249 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-22"></a>

### 22. @imdfamily — Record

Entry `a1163391588a3f2b` · submitted 2026-10-20T19:44:46.655Z.

**Submitted contract:** `0x83204c01e8c0a795b1f0622b08c2ad2da91a96a4` · [ethereum explorer](https://etherscan.io/address/0x83204c01e8c0a795b1f0622b08c2ad2da91a96a4).

**Swarm evidence and scope:** The entered DAEMON address matches swarm launch 2335.

**Described IMD feature:** The entry describes a learning/community lab but specifies no concrete IMD-dependent application.

**Assessment / unanswered:** Inspect the actual custom mechanism and successful invocation; a lab description and protocol token launch are insufficient to establish the required feature.

**Accepted worker assignments recorded:** implement seats #162; integrate seats #1446; review seats #371, #660, #729, #852 and others; tests seats #595. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2335 (live)](https://api.imd.fun/launches/a3ddcd10-65d0-46d9-ad47-70acde6523a9) · [source 317dd1ae](https://github.com/identity-md-launches/launch-2335-launch-daemon-daemon-ethereum/tree/317dd1aeee7369413497aee884ae875b3512dae8) · [deployment](https://etherscan.io/tx/0x48566e0310ff589f2b792a5ddedaeacf01a9e044646c3b03e993c4009ebb42b7).

**X:** [@imdfamily](https://x.com/imdfamily) · 2 followers; 1 lifetime posts (relay metadata). Direct profile sample: 1 authored posts, 1 dated in the event window. [Example sampled event post](https://x.com/imdfamily/status/2112608398646579358). Personal handle declared: [@startoverai](https://x.com/startoverai) (relay resolves: 181 followers, 606 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-23"></a>

### 23. @curbhook — Record

Entry `830b102b59b1529e` · submitted 2026-10-20T18:33:28.612Z.

**Submitted contract:** `0xa4df8fbf3a1ab94795577c74ffae26e1d2083819` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0xa4df8fbf3a1ab94795577c74ffae26e1d2083819).

**Swarm evidence and scope:** Launch 2266 corroborates the custom CurbHook build/deployment, with a different CURB token address than the earlier entered address.

**Described IMD feature:** Price bands and halts constrain an IMD pool; a desk is described as paying IMD for halt analysis.

**Assessment / unanswered:** Bind the submitted desk/earlier address to the final hook and prove a swap plus oracle-assisted halt. The hook has an owner/configuration surface; backtest statistics are not live receipts.

**Sources / leads:** [entrant repository](https://github.com/RaYYeR220/curb).

**X:** [@curbhook](https://x.com/curbhook) · 1 followers; 6 lifetime posts (relay metadata). Direct profile sample: 1 authored posts, 1 dated in the event window. [Example sampled event post](https://x.com/curbhook/status/2112611035266101748). Personal handle declared: [@BazydloMis57623](https://x.com/BazydloMis57623) (relay resolves: 42 followers, 74 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-24"></a>

### 24. @imd_financier — Record

Entry `61f49883093874e9` · submitted 2026-10-20T18:06:54.287Z.

**Submitted contract:** `0x2f56d8fef9f0891c952b15c3b2a94fa4326c28b5` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x2f56d8fef9f0891c952b15c3b2a94fa4326c28b5).

**Swarm evidence and scope:** The entered FINCR token matches launch 2311, whose manifest deploys only an ERC-20 and standard protocol plumbing.

**Described IMD feature:** The entry describes an IMD Dutch auction, work-based mining and an acceptance-evidence publisher.

**Assessment / unanswered:** Those application contracts are not in launch 2311. Supply their addresses and a takeover/reward/request receipt. The trusted cross-chain publisher is a material dependency.

**Accepted worker assignments recorded:** implement seats #909; integrate seats #203; review seats #346, #527, #1309, #1430 and others; tests seats #1525. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2311 (live)](https://api.imd.fun/launches/37341c17-96e8-40c6-8651-4feec0ba99a3) · [source 39472276](https://github.com/identity-md-launches/launch-2311-launch-only-existing-src-fincr-sol/tree/39472276cea08cfbeffa9e949f483813605458de) · [deployment](https://robinhoodchain.blockscout.com/tx/0x51738f724d585bcc7fe377f7404afb63da1876388213332acbcc273f707ccced).

**X:** [@imd_financier](https://x.com/imd_financier) · 3 followers; 8 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/imd_financier/status/2112719136971481366). Personal handle declared: [@forkbearingbull](https://x.com/forkbearingbull) (relay resolves: 545 followers, 845 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-25"></a>

### 25. @SeerOnIMD — Claim

Entry `83254cb6ebf27588` · submitted 2026-10-20T15:57:58.648Z.

**Submitted contract:** none in the contract field; additional prose/linked artifacts may supply one.

**Swarm evidence and scope:** The entry supplies testnet adjudicator addresses and describes discovery, forecast and resolution panels.

**Described IMD feature:** IMD is intended to accept questions, price forecasts and judge Sooth markets.

**Assessment / unanswered:** Name-only Seer token jobs cannot be attributed to these adjudicators. The supplied contracts are Robinhood testnet; organizer approval and a matched completed oracle-to-settlement trace remain unestablished.

**Sources / leads:** [submission census](https://www.imdradar.site/api/launchpad?view=hackathon).

**X:** [@SeerOnIMD](https://x.com/SeerOnIMD) · 10 followers; 3 lifetime posts (relay metadata). Direct profile sample: 3 authored posts, 3 dated in the event window. [Example sampled event post](https://x.com/SeerOnIMD/status/2112596955654480338). Personal handle declared: [@danieltang](https://x.com/danieltang) (relay resolves: 49 followers, 22 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-26"></a>

### 26. @MailMessengerRH — Claim

Entry `c7dc56ea5036150d` · submitted 2026-10-20T15:14:21.668Z.

**Submitted contract:** `0xa46bb59e405d2bc3416ef11952cd6d64da570562` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0xa46bb59e405d2bc3416ef11952cd6d64da570562).

**Swarm evidence and scope:** The entry says six rounds of swarm audits, but no matching MailHook audit was located from the supplied evidence/searches.

**Described IMD feature:** A MAIL game uses delivery rewards and an ETH-side trading hook.

**Assessment / unanswered:** Same-name standard MAIL token/logo jobs are not proof of this game. Supply the six exact audit jobs, source pin and a successful delivery/claim/hook transaction tied to the entered address.

**Sources / leads:** [submission census](https://www.imdradar.site/api/launchpad?view=hackathon).

**X:** [@MailMessengerRH](https://x.com/MailMessengerRH) · 27 followers; 24 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/MailMessengerRH/status/2112561311586586920). Personal handle declared: [@GoatGPRO](https://x.com/GoatGPRO) (relay resolves: 28 followers, 40 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-27"></a>

### 27. @ConditionalsImd — Record

Entry `4ea0ee71b74725cc` · submitted 2026-10-20T14:32:53.787Z.

**Submitted contract:** `0xc8cc656b71dd77ae1e29b0bc7890edd110e73255` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0xc8cc656b71dd77ae1e29b0bc7890edd110e73255).

**Swarm evidence and scope:** Launch 2278 matches the entered Conditionals contract; pinned code includes Intake callback and settlement logic.

**Described IMD feature:** IMD stakes and two paid oracle answers resolve conditional outcome pools.

**Assessment / unanswered:** No settlement receipt was independently checked. The entry's no-admin wording needs qualification: source contains owner-only future oracle configuration and fee-recipient settings.

**Accepted worker assignments recorded:** implement seats #727; integrate seats #798; review seats #694, #1133, #1694, #1849 and others; tests seats #1327. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2278 (live)](https://api.imd.fun/launches/ec1d4b0d-2dc4-4827-a626-e24add58df22) · [source f6d35513](https://github.com/identity-md-launches/launch-2278-launch-conditionals-contract-repository/tree/f6d35513fe0076b05e62bb5de61fe6df01626d98) · [deployment](https://robinhoodchain.blockscout.com/tx/0x7baf02fbc322ef9c583b8d50008b0a19fcc0e405ec200e484130a36cdf60da40).

**X:** [@ConditionalsImd](https://x.com/ConditionalsImd) · 21 followers; 4 lifetime posts (relay metadata). Direct profile sample: 3 authored posts, 3 dated in the event window. [Example sampled event post](https://x.com/ConditionalsImd/status/2112589513394725084). Personal handle declared: [@0xmisturi](https://x.com/0xmisturi) (relay resolves: 710 followers, 933 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-28"></a>

### 28. @Gamma_imd — Record

Entry `2b78887e377e1536` · submitted 2026-10-20T14:21:49.982Z.

**Submitted contract:** `0xb333a22c2c3dd0fe29fd1bf184c5ff2282148535` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0xb333a22c2c3dd0fe29fd1bf184c5ff2282148535).

**Swarm evidence and scope:** Launch 2215 matches GammaGame and DrandBeacon; manifest records audited game logic.

**Described IMD feature:** Players spend IMD through the game; a hook and reserve distribute GAMMA rewards.

**Assessment / unanswered:** The game has an owner/configurator at launch. Prove energy purchase, beacon-driven epoch and payout, and link the separate token/hook deployment; description alone does not establish all runtime paths.

**Accepted worker assignments recorded:** implement seats #1160; integrate seats #462; review seats #142, #242, #290, #890 and others; tests seats #1612. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2215 (live)](https://api.imd.fun/launches/5d70e904-8bd6-4eb9-bed7-409e05b0439c) · [source ee52608f](https://github.com/identity-md-launches/launch-2215-src-drandbeacon-sol-src-gammagame-sol/tree/ee52608fdae69e50569b23845dc620f36f42d7b2) · [deployment](https://robinhoodchain.blockscout.com/tx/0x0678d297069eb555d9b4a4541650beee1903ef82a915eb6be2e4271ab16dbc6c).

**X:** [@Gamma_imd](https://x.com/Gamma_imd) · 13 followers; 2 lifetime posts (relay metadata). Direct profile sample: 1 authored posts, 1 dated in the event window. [Example sampled event post](https://x.com/Gamma_imd/status/2112549157835526200). Personal handle declared: [@0xresets](https://x.com/0xresets) (relay resolves: 37 followers, 194 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-29"></a>

### 29. @PixelFun — Record

Entry `8513ad43abfe4c2a` · submitted 2026-10-20T13:31:55.565Z.

**Submitted contract:** `0x30da521f63553ec3ea2dbb82c30581c00ccf9009` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x30da521f63553ec3ea2dbb82c30581c00ccf9009).

**Swarm evidence and scope:** Launch 2148 and its completed build job match PixelFun.

**Described IMD feature:** Deposited IMD buys pixel edits and is sent to the specified burn sink; epochs rank painters.

**Assessment / unanswered:** The manifest implements 32 colors, while the entry omits palette detail. Show deposit/paint/burn receipts. The submitted X handle could not be resolved by the account relay, so account existence is unverified.

**Accepted worker assignments recorded:** implement seats #1238; integrate seats #1403; review seats #205, #249, #641, #1173 and others; tests seats #1413. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2148 (live)](https://api.imd.fun/launches/328add1b-9584-461f-aa63-47549a03bde7) · [source e880bd59](https://github.com/identity-md-launches/launch-2148-dsa/tree/e880bd5931c48ca32e7de751471a4506bd25e6e4) · [deployment](https://robinhoodchain.blockscout.com/tx/0xd7c0e30bc98b22a71eff1aa35df2362f131a295cbc981c764c74fc0511b72523) · [entrant repository](https://github.com/NoMADless/pixelfun).

**X:** [@PixelFun](https://x.com/PixelFun) · Public project profile unavailable (HTTP 404 in this acquisition); no activity conclusion. Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-30"></a>

### 30. @supercolony_ai — Record

Entry `9bdfab768395ee0e` · submitted 2026-10-20T13:31:46.620Z.

**Submitted contract:** none in the contract field; additional prose/linked artifacts may supply one.

**Swarm evidence and scope:** A completed SuperColony website job identifies use of the swarm, while the entry links a public CLI repository.

**Described IMD feature:** The CLI is intended to interpret requests locally and submit paid IMD work.

**Assessment / unanswered:** A website build does not validate the CLI's payment or worker paths. No custom contract/token or invocation evidence is supplied; local wallet security claims were not audited here.

**Accepted worker assignments recorded:** implement seats #108; review seats #480. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [job e5548721](https://explorer.imd.fun/jobs/e5548721-e1d1-4654-a9bf-a0310096559c) · [entrant repository](https://github.com/Duggy-AI/supercolony).

**X:** [@supercolony_ai](https://x.com/supercolony_ai) · 1 followers; 1 lifetime posts (relay metadata). Direct profile sample: 1 authored posts, 1 dated in the event window. [Example sampled event post](https://x.com/supercolony_ai/status/2112393700764729599). Personal handle declared: [@tian7eth](https://x.com/tian7eth) (relay resolves: 2,263 followers, 3,284 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-31"></a>

### 31. @keptonchainn — Record

Entry `b586f6da0288c40f` · submitted 2026-10-20T09:55:38.759Z.

**Submitted contract:** `0x3152f9cbf64d0c1ac24ea7e101db3e4d8da86896` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x3152f9cbf64d0c1ac24ea7e101db3e4d8da86896).

**Swarm evidence and scope:** The entered KeptVault matches launch 2172; pinned code verifies oracle attestations and settles milestone tranches.

**Described IMD feature:** Paid IMD milestone checks release or burn locked project tokens.

**Assessment / unanswered:** The claim of two releases needs receipts. Source has owner-controlled protocol/panel settings, so disclose them; the separate fee-funding hook also needs a matched deployment and invocation.

**Accepted worker assignments recorded:** implement seats #1877; integrate seats #737; review seats #189, #694, #809, #939 and others; tests seats #1155. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2172 (live)](https://api.imd.fun/launches/790d256e-0949-4810-b23c-0ac8eb7fb2d4) · [source bbb7f7d1](https://github.com/identity-md-launches/launch-2172-deploy-only-src-keptvault-sol-repository/tree/bbb7f7d193af94838480bb6898c6d78dcc9b7f51) · [deployment](https://robinhoodchain.blockscout.com/tx/0xf808e9337d090cc5594e49d850ba4426b90cec1812f0efdd1d3eac1d6c8ee9a6).

**X:** [@keptonchainn](https://x.com/keptonchainn) · 5 followers; 25 lifetime posts (relay metadata). Direct profile sample: 4 authored posts, 3 dated in the event window. [Example sampled event post](https://x.com/keptonchainn/status/2112529108471042192). Personal handle declared: [@Modemolaa](https://x.com/Modemolaa) (relay resolves: 1,288 followers, 17,377 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-32"></a>

### 32. @hamsterhourgame — Record

Entry `54cd697974beb950` · submitted 2026-10-20T08:31:59.962Z.

**Submitted contract:** `0xe33ab493249a2df0d8c4a71ac54f46d1f7778367` · [ethereum explorer](https://etherscan.io/address/0xe33ab493249a2df0d8c4a71ac54f46d1f7778367).

**Swarm evidence and scope:** The entered HamsterHour contract matches launch 2260 with swarm deployment/source provenance.

**Described IMD feature:** IMD betting pools are intended to pay for swarm answers about a real hamster's recorded distance.

**Assessment / unanswered:** Verify the physical-data source, paid question, callback and payout for one hour. Sampled X promotion includes an early-access repost incentive, which can affect engagement comparisons.

**Accepted worker assignments recorded:** implement seats #1166; integrate seats #132; review seats #452, #1082, #1314, #1489 and others; tests seats #1503. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2260 (live)](https://api.imd.fun/launches/632979e3-2f01-425f-baf2-3bd4f7b7673a) · [source 49f53ca0](https://github.com/identity-md-launches/launch-2260-build-hamster-hour-v2/tree/49f53ca0f278fe4edf6431f68a51468552372af7) · [deployment](https://etherscan.io/tx/0xe22d3fc97a6940efd66987fd49f32cec14d9be4836bb1de146f580c60f357b4a).

**X:** [@hamsterhourgame](https://x.com/hamsterhourgame) · 107 followers; 42 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 4 dated in the event window. [Example sampled event post](https://x.com/hamsterhourgame/status/2112854458657124372). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-33"></a>

### 33. @Eval_Engine — Record

Entry `4ab3de91474bf687` · submitted 2026-10-20T06:48:14.163Z.

**Submitted contract:** `0xf3a79f962ec1e75f0087af5491a69dee2a869012` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0xf3a79f962ec1e75f0087af5491a69dee2a869012).

**Swarm evidence and scope:** Launch 2223 matches AskSwarmRegistry, SwarmMarket and SwarmWager; both pinned source and the cited request are inspectable.

**Described IMD feature:** Contracts buy IMD oracle answers and settle IMD markets/wagers after signature verification.

**Assessment / unanswered:** A full market-3 cycle is corroborated below after locating separate callback, settlement and claim transactions. Later logs also contain refusals/disagreements; successful examples do not prove universal availability.

**Accepted worker assignments recorded:** implement seats #363; integrate seats #77; review seats #11, #22, #293, #690 and others; tests seats #1682. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2223 (live)](https://api.imd.fun/launches/ffd8f76a-484d-4366-b1d6-a3100b9766e4) · [source 712164b6](https://github.com/identity-md-launches/launch-2223-src-askswarmregistry-sol-src-swarmmarket/tree/712164b6f0121e093dfcd97b2925036becf6019b) · [deployment](https://robinhoodchain.blockscout.com/tx/0xf3de97499688c53dffa1970fbd38a65d85413b985f91724f6332be3b4f291566) · [entrant repository](https://github.com/ChromiaAgents/askswarm).

**X:** [@Eval_Engine](https://x.com/Eval_Engine) · 1,901 followers; 315 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 2 dated in the event window. [Example sampled event post](https://x.com/Eval_Engine/status/2109634122964689168). Personal handle declared: [@superoo7](https://x.com/superoo7) (relay resolves: 9,778 followers, 5,520 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-34"></a>

### 34. @NotestotheW — Record

Entry `61eb85e009844400` · submitted 2026-10-19T23:56:08.741Z.

**Submitted contract:** `0x9550e4f888d1c084cb1c8e74677da54109723ee3` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x9550e4f888d1c084cb1c8e74677da54109723ee3).

**Swarm evidence and scope:** An exact gimogo/NTTW audit job and an address-specific settlement-integrity job corroborate swarm review.

**Described IMD feature:** The entry describes a custom wall/token lottery using Chainlink VRF and cross-chain relay delivery.

**Assessment / unanswered:** IMD protocol launch is claimed; prove the specific IMD dependency beyond token provenance. The one-ticket demo cannot establish lottery fairness; acknowledged audit issues and subscription/admin dependencies remain relevant.

**Accepted worker assignments recorded:** review seats #560, #641, #954, #1229 and others. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [job 16c65a39](https://explorer.imd.fun/jobs/16c65a39-24f4-47d6-a9f5-2140c70791c6) · [job 44df6543](https://explorer.imd.fun/jobs/44df6543-f9d6-4f44-9d69-40e0f7223b0c) · [entrant repository](https://github.com/gimogo/NTTW).

**X:** [@NotestotheW](https://x.com/NotestotheW) · 58 followers; 34 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 2 dated in the event window. [Example sampled event post](https://x.com/NotestotheW/status/2112331794670649637). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-35"></a>

### 35. @nightshiftimd — Record

Entry `35ac8064ad1f83af` · submitted 2026-10-19T20:16:46.902Z.

**Submitted contract:** `0xe5e58e53d0bb204aa62c995a6c8cc8a48e60c3ac` · [ethereum explorer](https://etherscan.io/address/0xe5e58e53d0bb204aa62c995a6c8cc8a48e60c3ac).

**Swarm evidence and scope:** The entered SHIFT address matches launch 2124 and a custom NightshiftHook.

**Described IMD feature:** Trading fees and swarm purchases are described as funding an IMD-based agent/product economy.

**Assessment / unanswered:** The manifest assigns Ownable roles to a developer wallet and initially gates trading. Separate deployed components from roadmap claims, and prove at least one IMD hire/payment and active hook transaction.

**Accepted worker assignments recorded:** implement seats #1411; integrate seats #544; review seats #27, #535, #810, #1059 and others; tests seats #1004. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2124 (live)](https://api.imd.fun/launches/ba3c2a45-99a6-446b-91ab-a839869a08a5) · [source 9f3e1600](https://github.com/identity-md-launches/launch-2124-launch-nightshift-shift-platform/tree/9f3e16007ca31848b48475b2a58d57b44b40077c) · [deployment](https://etherscan.io/tx/0x7066ea4c4d8f3a90b30f846925d41a989b851d9becc996065d69a2734a5766c1) · [entrant repository](https://github.com/RobertKodes/nightshift).

**X:** [@nightshiftimd](https://x.com/nightshiftimd) · 198 followers; 135 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/nightshiftimd/status/2112865377474535926). Personal handle declared: [@probert_mihai](https://x.com/probert_mihai) (relay resolves: 57 followers, 203 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-36"></a>

### 36. @imdpot — Record

Entry `36911e0d560f58e5` · submitted 2026-10-19T19:03:44.900Z.

**Submitted contract:** `0xa5ee8a1f2aa98f08755f80bb278528d789f1e8f3` · [ethereum explorer](https://etherscan.io/address/0xa5ee8a1f2aa98f08755f80bb278528d789f1e8f3).

**Swarm evidence and scope:** The entered jackpot contract matches launch 2183.

**Described IMD feature:** An IMD-only round allocates payouts, burns and loyalty balances.

**Assessment / unanswered:** Show a completed round and actual IMD transfers. Future-blockhash randomness, house fees and locked loyalty accounting need risk disclosure; a deployment record does not establish fair or reliable settlement.

**Accepted worker assignments recorded:** implement seats #1520; integrate seats #1687; review seats #94, #281, #468, #656 and others; tests seats #1906. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2183 (live)](https://api.imd.fun/launches/eb0cc821-2cbd-46ee-a720-014594db03e2) · [source b60026be](https://github.com/identity-md-launches/launch-2183-i-already-have-existing/tree/b60026be5455bdeed5a8adc224fe0ef57ffe68f4) · [deployment](https://etherscan.io/tx/0x3409199f4b2e8faa6a01fa2cada460fe93b6232df5b7b3b0151a3d33c21de738).

**X:** [@imdpot](https://x.com/imdpot) · 4 followers; 22 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/imdpot/status/2112815700389638549). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-37"></a>

### 37. @SuperFPET_eth — Claim

Entry `bd7a704b7f937181` · submitted 2026-10-19T18:51:36.580Z.

**Submitted contract:** none in the contract field; additional prose/linked artifacts may supply one.

**Swarm evidence and scope:** The entrant describes a bridge/keeper workflow; the entry has no contract, source or job link.

**Described IMD feature:** Trading fees are intended to bridge IMD into FP and stake it in a shared FrenPet.

**Assessment / unanswered:** Same-name launch jobs exist but were not bound to the submitted project by an address or payer. Provide the full fee, bridge receipt and staking transaction chain, including keeper permissions.

**Sources / leads:** [submission census](https://www.imdradar.site/api/launchpad?view=hackathon).

**X:** [@SuperFPET_eth](https://x.com/SuperFPET_eth) · 55 followers; 10 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 4 dated in the event window. [Example sampled event post](https://x.com/SuperFPET_eth/status/2112225192558678245). Personal handle declared: [@Atlasfreeman](https://x.com/Atlasfreeman) (relay resolves: 12,221 followers, 14,082 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-38"></a>

### 38. @sudeepb02 — Record

Entry `5fa4d624b80db4f8` · submitted 2026-10-19T18:32:59.406Z.

**Submitted contract:** `0x2008b60c94e97a0f5315fc90a0aafe9e3bd78f7d` · [ethereum explorer](https://etherscan.io/address/0x2008b60c94e97a0f5315fc90a0aafe9e3bd78f7d), [base explorer](https://basescan.org/address/0x2008b60c94e97a0f5315fc90a0aafe9e3bd78f7d), [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x2008b60c94e97a0f5315fc90a0aafe9e3bd78f7d).

**Swarm evidence and scope:** The exact linked imdLend audit corroborates a five-agent review of the named public contracts repository.

**Described IMD feature:** Seat owners rent capacity to operators for IMD, with vaults splitting work rewards.

**Assessment / unanswered:** The audit is not proof of every deployment or the first paired-seat job. Resolve findings against the deployed commit, inspect rental/return transactions and verify how worker authorization expires.

**Sources / leads:** [job d5b12e13](https://explorer.imd.fun/jobs/d5b12e13-efed-4950-b440-b544f6476fa3) · [entrant repository](https://github.com/sudeepb02/imdLend-contracts-public).

**X:** [@sudeepb02](https://x.com/sudeepb02) · 639 followers; 1,625 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 4 dated in the event window. [Example sampled event post](https://x.com/sudeepb02/status/2111540462851088575). Personal handle declared: [@sudeepb02](https://x.com/sudeepb02) (same handle as project) (relay resolves: 639 followers, 1,625 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-39"></a>

### 39. @robobet_fun — Record

Entry `dcd42434c88a2d60` · submitted 2026-10-19T17:37:04.723Z.

**Submitted contract:** none in the contract field; additional prose/linked artifacts may supply one.

**Swarm evidence and scope:** Launch 1791 matches the Ethereum USDCDepositClaim address in the entry's prose, supporting swarm-written claim logic.

**Described IMD feature:** The entrant describes paid IMD research selecting simulated high-leverage trades.

**Assessment / unanswered:** The claim contract itself has no demonstrated IMD dependency; it is owner-funded USDC distribution. Prove a specific research order-to-decision-to-claim connection and distinguish PaperTrade simulation from real market execution.

**Accepted worker assignments recorded:** implement seats #1020; integrate seats #143; review seats #422, #573, #1017, #1067 and others; tests seats #1510. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1791 (live)](https://api.imd.fun/launches/1f403228-7b27-432c-822a-c130ae716264) · [source b68dad2e](https://github.com/identity-md-launches/launch-1791-i-want-you-create/tree/b68dad2e0d690cd74f47e863773715f0f19f493b) · [deployment](https://etherscan.io/tx/0x4af5476bb33986e229336476a2239048a0861c7128aff0fc68773cf8b240cd79) · [job 1a03986b](https://explorer.imd.fun/jobs/1a03986b-3673-4b55-88c1-b5e529b2bd34).

**X:** [@robobet_fun](https://x.com/robobet_fun) · 297 followers; 25 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/robobet_fun/status/2112963650315334098). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-40"></a>

### 40. @chad_gotchi — Record

Entry `2d2b83984607f79b` · submitted 2026-10-19T07:54:54.649Z.

**Submitted contract:** none in the contract field; additional prose/linked artifacts may supply one.

**Swarm evidence and scope:** Identifiable OG Club jobs show ongoing swarm development, including an October 21 hook job.

**Described IMD feature:** The entry describes an NFT-avatar browser world without specifying an IMD-dependent contract feature.

**Assessment / unanswered:** No address or transaction is submitted. Later OG hook work cannot establish what this entry delivered by its earlier submission; bind the eligible version and demonstrate IMD seat/asset utility.

**Accepted worker assignments recorded:** implement seats #660; integrate seats #921; review seats #172, #205, #595, #1166 and others; tests seats #1446. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [job c2fbceb1](https://explorer.imd.fun/jobs/c2fbceb1-a54f-4c20-88c2-c4b9669d12bd).

**X:** [@chad_gotchi](https://x.com/chad_gotchi) · 295 followers; 535 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/chad_gotchi/status/2109951620817760297). Personal handle declared: [@chad_gotchi](https://x.com/chad_gotchi) (same handle as project) (relay resolves: 295 followers, 535 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-41"></a>

### 41. @TaskOnchainn — Record

Entry `3630478a1e8e7250` · submitted 2026-10-19T00:21:41.778Z.

**Submitted contract:** `0x2b79cc53d7f0f6458c44ce4f78e8d9adb1393b19` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x2b79cc53d7f0f6458c44ce4f78e8d9adb1393b19).

**Swarm evidence and scope:** Launch 2194 matches BountyBox and records an updated swarm deployment.

**Described IMD feature:** ETH escrow pays workers subject to creator approval or a human reviewer, with a timeout split.

**Assessment / unanswered:** The manifest's oracle is a reviewer EOA, not proof of an IMD agent oracle. Swarm development is supported; explain the continuing IMD dependency if claiming runtime integration. Admin may replace the reviewer after delay.

**Accepted worker assignments recorded:** implement seats #475; integrate seats #760; review seats #3, #650, #1457, #1616 and others; tests seats #715. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2194 (live)](https://api.imd.fun/launches/2844d117-8ac6-4d50-b205-1b4aa254b52b) · [source fd99ae4b](https://github.com/identity-md-launches/launch-2194-update-existing-bounty-box/tree/fd99ae4b0f44ca43cd91df7179150005ca6f1da5) · [deployment](https://robinhoodchain.blockscout.com/tx/0x231d887415a69557fe27872cd2ce70c06b2e9dde44cc8751ece7edff6fe29733).

**X:** [@TaskOnchainn](https://x.com/TaskOnchainn) · 7 followers; 6 lifetime posts (relay metadata). Direct profile sample: 2 authored posts, 2 dated in the event window. [Example sampled event post](https://x.com/TaskOnchainn/status/2112912220107755962). Personal handle declared: [@zyraxoo](https://x.com/zyraxoo) (relay resolves: 1,048 followers, 22,129 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-42"></a>

### 42. @pleaimd — Claim

Entry `6ba408eabebf9284` · submitted 2026-10-18T21:30:53.556Z.

**Submitted contract:** none in the contract field; additional prose/linked artifacts may supply one.

**Swarm evidence and scope:** The entry reports eight audits and seven Sepolia launches but supplies no exact job record or deployed address.

**Described IMD feature:** A paid IMD oracle panel would approve pleas to sell through an IMD-paired hook.

**Assessment / unanswered:** It explicitly says mainnet next. Need organizer-approved testnet status, source-bound audit jobs and a successful plea/verdict/sell receipt; test counts alone are insufficient.

**Sources / leads:** [entrant repository](https://github.com/khaed1/plea).

**X:** [@pleaimd](https://x.com/pleaimd) · 0 followers; 0 lifetime posts (relay metadata). Direct profile sample: 0 authored posts, 0 dated in the event window. Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-43"></a>

### 43. @UnlockBySwarm — Record

Entry `a1a233a85ff47d48` · submitted 2026-10-18T08:56:05.717Z.

**Submitted contract:** `0x99fa82b022be4575891a43b757bc770691e18fda` · [ethereum explorer](https://etherscan.io/address/0x99fa82b022be4575891a43b757bc770691e18fda).

**Swarm evidence and scope:** Launch 2071 matches UNLK and UnlkImdHook, recording a repaired swarm deployment.

**Described IMD feature:** The hooked IMD pool enforces sales quotas and collects IMD treasury fees.

**Assessment / unanswered:** The entry correctly says other pools/transfers bypass quotas. Prove a live swap/quota change and fee routing; an intended future NFT purchase is not an already-working IMD seat benefit.

**Accepted worker assignments recorded:** implement seats #701; integrate seats #1681; review seats #158, #172, #690, #1176 and others; tests seats #317. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 2071 (live)](https://api.imd.fun/launches/0528a007-5ec6-4acd-b9cc-b3ded6fe2929) · [source 40d70b7b](https://github.com/identity-md-launches/launch-2071-unlock/tree/40d70b7bd0853aedf84eac839a40a5f12e6ac341) · [deployment](https://etherscan.io/tx/0xa1b4e9ecc19fdc6cd663bc088ee636a3fbb2186b2bc6a51e37f8b48664fc301a).

**X:** [@UnlockBySwarm](https://x.com/UnlockBySwarm) · 9 followers; 16 lifetime posts (relay metadata). Direct profile sample: 2 authored posts, 2 dated in the event window. [Example sampled event post](https://x.com/UnlockBySwarm/status/2111555807175205274). Personal handle declared: [@kilicsln](https://x.com/kilicsln) (relay resolves: 7,350 followers, 1,177 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-44"></a>

### 44. @imd_offset — Claim

Entry `9a418bc5ddfb4f90` · submitted 2026-10-16T22:27:27.774Z.

**Submitted contract:** `0x87b525bc5ff6d7211f16291219c363e082ed4e9f` · [ethereum explorer](https://etherscan.io/address/0x87b525bc5ff6d7211f16291219c363e082ed4e9f), [base explorer](https://basescan.org/address/0x87b525bc5ff6d7211f16291219c363e082ed4e9f).

**Swarm evidence and scope:** The entry describes regenerative tools and a submitted token address; exact-address jobs were not found.

**Described IMD feature:** IMD compute offsets and trading-funded ecological contributions are proposed as the use case.

**Assessment / unanswered:** Similar IMD Offsets jobs surfaced, including testnet builds, but were not linked securely to this entered deployment. Need the actual receipt, credit retirement evidence and fee-routing code; avoid treating a contribution as verified offsetting.

**Sources / leads:** [submission census](https://www.imdradar.site/api/launchpad?view=hackathon).

**X:** [@imd_offset](https://x.com/imd_offset) · 136 followers; 101 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/imd_offset/status/2111173903808598255). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-45"></a>

### 45. @SinopiaMD — Record

Entry `757ee35b472f49c9` · submitted 2026-10-16T09:42:08.863Z.

**Submitted contract:** `0x0da78a50b3039f8ca719d01754988b23d7e70fe2` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x0da78a50b3039f8ca719d01754988b23d7e70fe2).

**Swarm evidence and scope:** Launch 1942 matches Sinopia and records swarm deployment of an IMD-funded commission auction.

**Described IMD feature:** Winning IMD bids buy a swarm image job; callbacks mint output and the remainder is burned.

**Assessment / unanswered:** A compelling runtime design, but no auction/job/mint/burn receipt was independently traced here. Verify output hash binding, failure refunds and accepted-code permissions.

**Accepted worker assignments recorded:** integrate seats #873; review seats #36. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1942 (live)](https://api.imd.fun/launches/60c0c715-ab5f-443c-9041-500301f8335d) · [source 2d7436e5](https://github.com/identity-md-launches/launch-1942-sinopia/tree/2d7436e57e6e90f8e5288ed6976e4d2d9a38fd26) · [deployment](https://robinhoodchain.blockscout.com/tx/0x7cd47ddce3a005e4fc632cf8107c46f2d46a74c014e20bc364e21ac6c71a246e) · [entrant repository](https://github.com/Timidan/sinopia.).

**X:** [@SinopiaMD](https://x.com/SinopiaMD) · 3 followers; 12 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/SinopiaMD/status/2110995740516372762). Personal handle declared: [@Timidan_x](https://x.com/Timidan_x) (relay resolves: 2,043 followers, 8,984 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-46"></a>

### 46. @IMDhongbao — Record

Entry `f493bc040796adeb` · submitted 2026-10-16T08:39:13.580Z.

**Submitted contract:** `0xc609565a5252c458609896b9ff4403b2a020c5d6` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0xc609565a5252c458609896b9ff4403b2a020c5d6).

**Swarm evidence and scope:** Launch 1815 and the linked workflow match HongbaoBox and corroborate build/test/review/deployment.

**Described IMD feature:** IMD packets use recipient-bound signatures, sharing logic and a fee burn.

**Assessment / unanswered:** The entry's abbreviated demo hash is not a usable full transaction reference. Retrieve the full packet open/grab/burn sequence; commit-reveal fallback and secret sharing need explicit limitations.

**Accepted worker assignments recorded:** implement seats #1637; integrate seats #704; review seats #531, #641, #1066, #1465 and others; tests seats #307. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1815 (live)](https://api.imd.fun/launches/618acce0-87e8-4831-b419-25e12dde5f8d) · [source 9689af00](https://github.com/identity-md-launches/launch-1815-workflow-contract-stage-context/tree/9689af00d42ca5dff84521a5c4d654dca44d292b) · [deployment](https://robinhoodchain.blockscout.com/tx/0x5fb76b7295111f8f45cc0400be08ef8feaea7fc286e38e0513e45fec2fe76d39).

**X:** [@IMDhongbao](https://x.com/IMDhongbao) · 0 followers; 4 lifetime posts (relay metadata). Direct profile sample: 3 authored posts, 3 dated in the event window. [Example sampled event post](https://x.com/IMDhongbao/status/2111013496288956486). Personal handle declared: [@nuantree](https://x.com/nuantree) (relay resolves: 181 followers, 2,157 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-47"></a>

### 47. @weirpay — Record

Entry `e498669a580a4d52` · submitted 2026-10-15T20:15:20.569Z.

**Submitted contract:** `0xde049547f1e55bb093e14d8f4545d1cc9b613f97` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0xde049547f1e55bb093e14d8f4545d1cc9b613f97).

**Swarm evidence and scope:** Launch 1869 matches ownerless Weir v2 and records source/deployment provenance.

**Described IMD feature:** ERC-20 payment streams can ask the IMD oracle to resolve disputes.

**Assessment / unanswered:** Provide a funded stream, dispute request, callback and final distribution. The entered application is distinct from the existing WEIR token used by its constructor.

**Accepted worker assignments recorded:** integrate seats #414; review seats #429, #539, #541, #1484 and others. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1869 (live)](https://api.imd.fun/launches/c107cc18-6ba3-4a66-a190-0f496e7c2d72) · [source 10866057](https://github.com/identity-md-launches/launch-1869-weir-v2-deploy-weir/tree/108660578606392f284fe2ad19bd8b576ece0bae) · [deployment](https://robinhoodchain.blockscout.com/tx/0x738bb84cdb93d459929c2fe63722dc009ca384ebbcc0aeaa768dc16eaa2e0e7f).

**X:** [@weirpay](https://x.com/weirpay) · 0 followers; 3 lifetime posts (relay metadata). Direct profile sample: 1 authored posts, 1 dated in the event window. [Example sampled event post](https://x.com/weirpay/status/2110827806611378510). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-48"></a>

### 48. @agentskill_imd — Record

Entry `c4dbb3e164264c55` · submitted 2026-10-15T13:15:34.374Z.

**Submitted contract:** `0xabec9774d66c640b64238dbd69758d31d10d54b1` · [ethereum explorer](https://etherscan.io/address/0xabec9774d66c640b64238dbd69758d31d10d54b1).

**Swarm evidence and scope:** Launch 1739 matches AgentSkill and its configured ERC-8004 reputation design.

**Described IMD feature:** Skills/endorsements and trusted reputation publishers are intended to rank IMD agents.

**Assessment / unanswered:** The manifest says no accepted-work adapter is included/deployed and ranking needs publisher configuration. Confirm current settings; ERC-8004 feedback is not automatically proof of accepted IMD jobs. Owner powers are material.

**Accepted worker assignments recorded:** implement seats #969; integrate seats #1299; review seats #346, #368, #442, #1457 and others; tests seats #900. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1739 (live)](https://api.imd.fun/launches/a7bba556-a4dd-4865-b573-4ff00dfa3ab7) · [source cae6d4dc](https://github.com/identity-md-launches/launch-1739-build-complete-polished-product/tree/cae6d4dcf66b14da9c8dadb25dac59f2697f3e92) · [deployment](https://etherscan.io/tx/0x9d5a14009178048eba37b29c3059e1baa146725dfcdf02cf1f90b41274761e21).

**X:** [@agentskill_imd](https://x.com/agentskill_imd) · 5 followers; 12 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/agentskill_imd/status/2111029438963982704). Personal handle declared: [@nemeremigweze](https://x.com/nemeremigweze) (relay resolves: 135 followers, 5,401 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-49"></a>

### 49. @IaMaDamIMD — Record

Entry `c7dc28300ef91486` · submitted 2026-10-15T13:06:28.817Z.

**Submitted contract:** `0x0eb84279eff71548ac5212ce17760b1e54692825` · [ethereum explorer](https://etherscan.io/address/0x0eb84279eff71548ac5212ce17760b1e54692825).

**Swarm evidence and scope:** An exact-address job explicitly identifies @IaMaDamIMD and records swarm website work.

**Described IMD feature:** The entry itself only supplies a slogan, so it does not explain a working IMD-dependent feature.

**Assessment / unanswered:** A website job corroborates swarm use, not custom contract behavior. Need technical mechanism, source, active invocation, demo and permission disclosure.

**Accepted worker assignments recorded:** implement seats #812. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [job 0fef589e](https://explorer.imd.fun/jobs/0fef589e-73d1-4e04-9e86-aca1ccb04180).

**X:** [@IaMaDamIMD](https://x.com/IaMaDamIMD) · 131 followers; 59 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/IaMaDamIMD/status/2112158775583125753). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-50"></a>

### 50. @IMDBlackout — Record

Entry `0e730668a808e9f2` · submitted 2026-10-15T05:46:17.202Z.

**Submitted contract:** `0x38b05971c79e738f64452be83c78ec3d66535b7a` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x38b05971c79e738f64452be83c78ec3d66535b7a).

**Swarm evidence and scope:** The entered BLACKOUT address matches swarm launch 1710.

**Described IMD feature:** The entry describes hardware-pack gameplay and a custom-fee hook across multiple releases.

**Assessment / unanswered:** One matched deployment does not verify all 20 contracts or four launches. Enumerate the set and demonstrate a paid pack, epoch and reward path; explain IMD's runtime role rather than only swarm authorship.

**Accepted worker assignments recorded:** implement seats #931; integrate seats #604; review seats #36, #671, #1295, #1561 and others; tests seats #1201. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1710 (live)](https://api.imd.fun/launches/74bf6327-bf09-44de-811c-9279e3dffe23) · [source 27c94e59](https://github.com/identity-md-launches/launch-1710-blackout/tree/27c94e597d39c5cb91813b2a73390e13d2b5a715) · [deployment](https://robinhoodchain.blockscout.com/tx/0x57bf8fbd6c612df0913662b433b6a1c1029375cfff2100d91556abecdbdb16b5).

**X:** [@IMDBlackout](https://x.com/IMDBlackout) · 65 followers; 45 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/IMDBlackout/status/2110365354077585628). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-51"></a>

### 51. @neethome_rh — Record

Entry `5bf997e11eba5d24` · submitted 2026-10-15T05:15:49.060Z.

**Submitted contract:** `0x66d0963f8a9af27b15028d84da8a1792999a840f` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x66d0963f8a9af27b15028d84da8a1792999a840f).

**Swarm evidence and scope:** Launch 1703 matches NEETHOME and explicitly records a fixed-supply ERC-20 with no application contracts or custom trading hook.

**Described IMD feature:** The entry plans to use fee revenue for a Solana purchase and burning.

**Assessment / unanswered:** This deployment alone is a plain-token launch and does not meet the meaningful-functionality requirement. The cross-chain plan needs independently deployed logic and transactions.

**Accepted worker assignments recorded:** implement seats #545; integrate seats #993; review seats #39, #475, #636, #727 and others; tests seats #1998. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1703 (live)](https://api.imd.fun/launches/06534dbc-d1f8-409e-9db3-a6b42b68bff6) · [source f58a01be](https://github.com/identity-md-launches/launch-1703-neetillions/tree/f58a01bee0385b21494d12eed32421b257709e85) · [deployment](https://robinhoodchain.blockscout.com/tx/0x0a3114644519ab11ec4764511959ce01a5cd957a30f9899cf035f3686bf5c3bf).

**X:** [@neethome_rh](https://x.com/neethome_rh) · 19 followers; 51 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/neethome_rh/status/2110601256200962169). Personal handle declared: [@neethome_rh](https://x.com/neethome_rh) (same handle as project) (relay resolves: 19 followers, 51 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-52"></a>

### 52. @PawnIMD — Record

Entry `e3c372ae9deed099` · submitted 2026-10-14T23:20:02.652Z.

**Submitted contract:** `0xf0d9300d7d891bc842da540cc4ddef050da9bcd4` · [ethereum explorer](https://etherscan.io/address/0xf0d9300d7d891bc842da540cc4ddef050da9bcd4).

**Swarm evidence and scope:** The entered PawnShop address matches launch 1139 and accompanying FloorRelay, LockDiscount and MilestoneBurn.

**Described IMD feature:** IMD oracle floor attestations price seat-backed ETH lending while authorization allows workers to continue.

**Assessment / unanswered:** Need a real collateral/loan/repayment or auction cycle and proof of continued worker authorization. Owner-controlled components and oracle/floor/liquidity risks must be disclosed.

**Accepted worker assignments recorded:** implement seats #976; integrate seats #429; review seats #12, #127, #560, #727 and others; tests seats #36. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1139 (live)](https://api.imd.fun/launches/1522cb0f-6fc1-4423-aea1-4569851a1856) · [source f6f7d1e5](https://github.com/identity-md-launches/launch-1139-deploy-audit-fixed-pawn-contracts/tree/f6f7d1e5b521a0490732b996bb2c54473bd5f68f) · [deployment](https://etherscan.io/tx/0x9a3354d2f181763c40663d24fc771f9d63c05fd6e873c470cc072002300ab6e3).

**X:** [@PawnIMD](https://x.com/PawnIMD) · 27 followers; 21 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/PawnIMD/status/2109353604976918807). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-53"></a>

### 53. @keelpad_imd — Record

Entry `2d09fca8599dbdc8` · submitted 2026-10-14T17:23:10.654Z.

**Submitted contract:** `0x324a7cc39764f3abac02cfc340228cd06042f064` · [ethereum explorer](https://etherscan.io/address/0x324a7cc39764f3abac02cfc340228cd06042f064).

**Swarm evidence and scope:** Keel Spin and Keel v2 build jobs corroborate swarm work for related products; project X explicitly describes those integrations.

**Described IMD feature:** The described launchpad routes IMD fees into further swarm-funded development and holder voting.

**Assessment / unanswered:** The submitted address was not matched. Do not substitute newer code-only Keel v2 or Keel Spin for the entered v1 deployment. Supply its precise factory/hook job, active pool receipt and paid follow-on build.

**Sources / leads:** [job 84e3719a](https://explorer.imd.fun/jobs/84e3719a-76be-40ed-92fb-c792d6490dba) · [job f4c6c94f](https://explorer.imd.fun/jobs/f4c6c94f-30c2-45be-8a4d-313ff9cf3b3d).

**X:** [@keelpad_imd](https://x.com/keelpad_imd) · 164 followers; 15 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/keelpad_imd/status/2112979327637676538). Personal handle declared: [@mrakold](https://x.com/mrakold) (relay resolves: 937 followers, 17,462 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-54"></a>

### 54. @perkshireimd — Record

Entry `294a0cbccb48c8f9` · submitted 2026-10-14T01:06:19.897Z.

**Submitted contract:** `0x2b2ed02698a82230f11d6285f3b147e3fd6df83a` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x2b2ed02698a82230f11d6285f3b147e3fd6df83a).

**Swarm evidence and scope:** Launch 1660 matches the Robinhood PERK address and custom hook/vault; launch 1663 is explicitly disclaimed by the entrant.

**Described IMD feature:** IMD trading fees fund a burn and redeemable float; a weekly call is intended to buy an IMD oracle answer.

**Assessment / unanswered:** Verify tender and paid-oracle transactions. Do not merge the Ethereum same-name launch into this project; the disclosed creator allocation and immutable-rule risks still matter.

**Accepted worker assignments recorded:** implement seats #1000; integrate seats #1572; review seats #3, #351, #1271, #1430 and others; tests seats #1782. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1660 (live)](https://api.imd.fun/launches/80a241f0-bb62-46ae-9712-2512f5e9f683) · [source 4329d97b](https://github.com/identity-md-launches/launch-1660-perkshire-imdway/tree/4329d97b05699e0d796c86ba4310d4df83e4381e) · [deployment](https://robinhoodchain.blockscout.com/tx/0x31ad7c183c844ccab6e3ca206e9a6e7bd7c5882269cf6fc0ea63360fe5b6c3d6).

**X:** [@perkshireimd](https://x.com/perkshireimd) · 2 followers; 1 lifetime posts (relay metadata). Direct profile sample: 1 authored posts, 1 dated in the event window. [Example sampled event post](https://x.com/perkshireimd/status/2110121862885937442). Personal handle declared: [@Block_Merchant](https://x.com/Block_Merchant) (relay resolves: 3,594 followers, 20,435 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-55"></a>

### 55. @imdusd — Record

Entry `bf04296330f66a63` · submitted 2026-10-13T21:45:11.599Z.

**Submitted contract:** `0x53d0ea0a685220718dc6a0a6e4617194c6f37921` · [ethereum explorer](https://etherscan.io/address/0x53d0ea0a685220718dc6a0a6e4617194c6f37921).

**Swarm evidence and scope:** The entered address matches INFER launch 1282, not the imdUSD stablecoin vault itself.

**Described IMD feature:** The entry describes IMD/sIMD-backed borrowing and signed swarm price/health inputs.

**Assessment / unanswered:** Identify the actual collateral vault, oracle adapter and stablecoin contracts and prove mint/redemption/liquidation. INFER's deployment alone does not demonstrate the stablecoin or peg; collateral and oracle risks remain.

**Accepted worker assignments recorded:** implement seats #410; integrate seats #1253; review seats #544, #1082, #1113, #1314 and others; tests seats #1070. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1282 (live)](https://api.imd.fun/launches/63f6d974-f5b8-4a84-b296-2219f5ab2c95) · [source 9b6cdbd4](https://github.com/identity-md-launches/launch-1282-launch-infer-repository-custom-token/tree/9b6cdbd4b3b3c8dfc3868310c72f1fda5cfa9d5f) · [deployment](https://etherscan.io/tx/0x9c319bb2dc4613a1be1c90b7f8d4559caefc941ca639a576fc5e831b976154e4).

**X:** [@imdusd](https://x.com/imdusd) · 774 followers; 35 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/imdusd/status/2112962501700645139). Personal handle declared: [@yadfarms](https://x.com/yadfarms) (relay resolves: 2,199 followers, 12,376 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-56"></a>

### 56. @xmrscn — Planned

Entry `e337c20e8ccd923e` · submitted 2026-10-13T16:14:59.823Z.

**Submitted contract:** `0x806b50f7e192697caf376d4e542153004baab28c` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x806b50f7e192697caf376d4e542153004baab28c).

**Swarm evidence and scope:** The entry says artwork exists but development/funding are still needed; no swarm job is supplied.

**Described IMD feature:** An IMD-priced NFT curve and reward system are a future vision.

**Assessment / unanswered:** No deployed custom logic or working IMD feature is established. Existing art and a social account do not meet the technical launch requirement.

**Sources / leads:** [submission census](https://www.imdradar.site/api/launchpad?view=hackathon).

**X:** [@xmrscn](https://x.com/xmrscn) · 2,159 followers; 15,703 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 1 dated in the event window. [Example sampled event post](https://x.com/XMrSCN/status/2111201682432643202). Personal handle declared: [@xmrscn](https://x.com/xmrscn) (same handle as project) (relay resolves: 2,159 followers, 15,703 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-57"></a>

### 57. @IMD6900 — Record

Entry `a0f703bc2d6e1ef8` · submitted 2026-10-13T15:18:22.426Z.

**Submitted contract:** `0x69000a4a9fa561dd6b313741bf1f79f4ade4adaf` · [ethereum explorer](https://etherscan.io/address/0x69000a4a9fa561dd6b313741bf1f79f4ade4adaf).

**Swarm evidence and scope:** The SDK page supplies the missing job link (its API returned 503); launch 1395 records nine accepted work nodes and independent review, but the deployment attempt is parked.

**Described IMD feature:** Seat-linked avatars, names, items and IMD oracle/burn fees are described.

**Assessment / unanswered:** The parked launch failed its manifest gate over a protocol-address argument. This supports swarm construction/review, not that the entered LARP address was deployed through it. The SDK links a separate deployment transaction; bind it to the final reviewed source.

**Sources / leads:** [launch 1395 (parked)](https://api.imd.fun/launches/46cd41c5-e332-451e-b0d0-6a8e3d7f1ebc) · [source 9aaf4380](https://github.com/identity-md-launches/launch-1395-larpburner-larp-imdnames-larplinks/tree/9aaf43805c39c44dfa79c209e226418b4235a30d) · [job 7e353f41](https://explorer.imd.fun/jobs/7e353f41-1fc4-4390-8e61-58d1c845db1c) · [entrant repository](https://github.com/magic0xfrens/imd6900-larp) · [SDK evidence page](https://imd6900.pages.dev/sdk/).

**X:** [@IMD6900](https://x.com/IMD6900) · 926 followers; 112 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 4 dated in the event window. [Example sampled event post](https://x.com/IMD6900/status/2109305368408993810). Personal handle declared: [@i0010110](https://x.com/i0010110) (relay resolves: 244 followers, 568 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-58"></a>

### 58. @stockroom — Record

Entry `5b41538fa6eecd90` · submitted 2026-10-13T09:57:17.924Z.

**Submitted contract:** `0xf66c6c7a09e741843d4ede8795ac4267e3823037` · [ethereum explorer](https://etherscan.io/address/0xf66c6c7a09e741843d4ede8795ac4267e3823037).

**Swarm evidence and scope:** Launch 1513 corroborates IMDStockDex at a different deployment address than the entry field; the named public repository is specific.

**Described IMD feature:** The DEX is designed to spend IMD on owner-listed stock-token routes and split an application fee.

**Assessment / unanswered:** The launch starts paused/unconfigured and permits extensive owner settings. Verify the entered-address relationship, actual unpause/configuration, liquidity and a purchase; listing does not establish stock backing or redemption.

**Accepted worker assignments recorded:** implement seats #286; integrate seats #535; review seats #225, #507, #694, #869 and others; tests seats #938. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1513 (live)](https://api.imd.fun/launches/42e04751-53a5-423d-9dfa-f44e3fece5e7) · [source 7933edf6](https://github.com/identity-md-launches/launch-1513-create-dex-buying-rwa/tree/7933edf6f604a63d8b4de3f6c4455bfecbe3f87d) · [deployment](https://etherscan.io/tx/0xf949886c0c836ae25a4eac0c7e8d98767091ec71da6f42ea04bfa408a96c7e21).

**X:** [@stockroom](https://x.com/stockroom) · 371 followers; 1,825 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 0 dated in the event window. Personal handle declared: [@jawaisme](https://x.com/jawaisme) (relay resolves: 479 followers, 10,192 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-59"></a>

### 59. @bunkervaultapp — Record

Entry `ad33c39d57cfdccb` · submitted 2026-10-13T06:14:28.971Z.

**Submitted contract:** `0x27f81fd932062fe67bca758e0e4cd8843cfaad41` · [ethereum explorer](https://etherscan.io/address/0x27f81fd932062fe67bca758e0e4cd8843cfaad41).

**Swarm evidence and scope:** An exact BunkerVault audit of the named source exists, corroborating specialist swarm review.

**Described IMD feature:** Vault operations require an additional ML-DSA signature; the entry says IMD registration fees mostly remain locked.

**Assessment / unanswered:** Bind audit commit to deployed bytecode, demonstrate registration plus withdrawal and quantify the actual IMD fee lock. Stronger vault authorization does not make the underlying chain post-quantum secure.

**Accepted worker assignments recorded:** review seats #184, #629, #1082, #1657 and others. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [job a8e78e5e](https://explorer.imd.fun/jobs/a8e78e5e-eda9-4f4a-baa4-5c3633422dd1).

**X:** [@bunkervaultapp](https://x.com/bunkervaultapp) · 5 followers; 2 lifetime posts (relay metadata). Direct profile sample: 2 authored posts, 2 dated in the event window. [Example sampled event post](https://x.com/bunkervaultapp/status/2109888279994663244). Personal handle declared: [@Byshot_](https://x.com/Byshot_) (relay resolves: 2,038 followers, 80 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-60"></a>

### 60. @pepe2pepe_fun — Record

Entry `c07e30858782884f` · submitted 2026-10-13T04:06:30.872Z.

**Submitted contract:** `0x54f97d8b32d8e90770d76b7d9eede1b77e28e3b8` · [ethereum explorer](https://etherscan.io/address/0x54f97d8b32d8e90770d76b7d9eede1b77e28e3b8).

**Swarm evidence and scope:** Address-specific oracle jobs reference the entered Pepe2Pepe market; named game-building jobs also exist.

**Described IMD feature:** The entry describes an IMD-powered game builder with optional token rewards, while Radar also describes an earlier prediction market.

**Assessment / unanswered:** Disambiguate the submitted market contract from the gaming launchpad. Prove the new paid build/reward path and backend replay/signing controls; avoid counting an earlier market's oracle use as proof of the new product.

**Accepted worker assignments recorded:** implement seats #1100. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [job 1c39fc17](https://explorer.imd.fun/jobs/1c39fc17-da54-453d-abbf-118e19f950ee) · [job 51e9d1f2](https://explorer.imd.fun/jobs/51e9d1f2-0b49-4361-b23d-8ef233275564).

**X:** [@pepe2pepe_fun](https://x.com/pepe2pepe_fun) · 190 followers; 47 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/pepe2pepe_fun/status/2111110603389501483). Personal handle declared: [@dani_who_daniel](https://x.com/dani_who_daniel) (relay resolves: 1,931 followers, 1,423 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-61"></a>

### 61. @pupateIMD — Record

Entry `6a97a6338288823e` · submitted 2026-10-12T18:22:07.894Z.

**Submitted contract:** `0x54993066369e57a49215f6fc2d9911a8e5a57a79` · [ethereum explorer](https://etherscan.io/address/0x54993066369e57a49215f6fc2d9911a8e5a57a79).

**Swarm evidence and scope:** Launch 1434 and its linked Pupate build/deployment job match the separately stated PUPATE token.

**Described IMD feature:** A custom hook funds a Cocoon vault intended to buy, operate and resell IMD seats using oracle prices.

**Assessment / unanswered:** The entry-field address is not the token address. Resolve the vault mapping and demonstrate a seat purchase/pairing/resale/burn path; operator and timelock controls are relevant.

**Accepted worker assignments recorded:** integrate seats #599; review seats #260, #330, #1113, #1725 and others. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1434 (live)](https://api.imd.fun/launches/71a4a0be-91c8-424c-bef2-0d332abaae57) · [source f405d2f4](https://github.com/identity-md-launches/launch-1434-pupate/tree/f405d2f40879b906abbe1824466e3fbc2f8d83b7) · [deployment](https://etherscan.io/tx/0xac7aff89cdf23f126631da73106cd3aef33c812fd39eace00fafb8e257e522b3).

**X:** [@pupateIMD](https://x.com/pupateIMD) · 28 followers; 31 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/pupateIMD/status/2111149696085557428). Personal handle declared: [@pupateIMD](https://x.com/pupateIMD) (same handle as project) (relay resolves: 28 followers, 31 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-62"></a>

### 62. @AgentCityrh — Record

Entry `845dc21c5a4d8f65` · submitted 2026-10-12T11:15:16.897Z.

**Submitted contract:** `0x878fbde429e1b21522735ed9dcf25e752a119284` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x878fbde429e1b21522735ed9dcf25e752a119284).

**Swarm evidence and scope:** Named AgentCity research, website and repository-specific audit jobs corroborate use for content, build support and review.

**Described IMD feature:** The entrant describes escrow-funded IMD work and an ERC-8004 town of agents.

**Assessment / unanswered:** The supplied POOL4 sell transaction is not proof of the town's job integration. Match a town-originated paid work order and delivered result; the entered token is not enough.

**Accepted worker assignments recorded:** implement seats #596; review seats #162, #822, #1030, #1489 and others. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [job 42b77bf7](https://explorer.imd.fun/jobs/42b77bf7-138d-44a1-861b-dd89ddb131f0) · [job d991bc96](https://explorer.imd.fun/jobs/d991bc96-0730-4861-a3fe-8a344d051617).

**X:** [@AgentCityrh](https://x.com/AgentCityrh) · 442 followers; 130 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 4 dated in the event window. [Example sampled event post](https://x.com/AgentCityrh/status/2112970430877200834). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-63"></a>

### 63. @marginalia_md — Record

Entry `ff93768fbb46b6a1` · submitted 2026-10-12T01:39:09.336Z.

**Submitted contract:** `0xf0457dd0cf526686190e4f057ba19db14d34a0cc` · [ethereum explorer](https://etherscan.io/address/0xf0457dd0cf526686190e4f057ba19db14d34a0cc).

**Swarm evidence and scope:** Launch 1283 matches MARG, MarginaliaHook and application contracts, supporting swarm launch provenance.

**Described IMD feature:** Bonded trade notes and paid IMD oracle rankings/identity attestations are described.

**Assessment / unanswered:** Need a note/observation/settlement and ranking-payout cycle. The source manifest includes admin-settable oracle/epoch configuration, so verify the current permission state rather than infer ownerlessness.

**Accepted worker assignments recorded:** implement seats #989; integrate seats #984; review seats #11, #351, #460, #727 and others; tests seats #551. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1283 (live)](https://api.imd.fun/launches/01771823-5250-4aaa-a55e-da5c1afe1146) · [source f99868c7](https://github.com/identity-md-launches/launch-1283-marginalia-x-com-marginalia-md-notes-mar/tree/f99868c781b4844b1e45837932ad73c790f7b288) · [deployment](https://etherscan.io/tx/0x6ba7149c648529bdc043dae985611f827fbbe18e47b5dfd9add56a5e17a74e48).

**X:** [@marginalia_md](https://x.com/marginalia_md) · 223 followers; 48 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 4 dated in the event window. [Example sampled event post](https://x.com/marginalia_md/status/2112767103988318244). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-64"></a>

### 64. @ArewaOS26 — Claim

Entry `d9ce31ca6261ada0` · submitted 2026-10-11T17:53:21.738Z.

**Submitted contract:** `0xaaa9ded4e50ca82e3c32444ea836940612a9fb96` · [base explorer](https://basescan.org/address/0xaaa9ded4e50ca82e3c32444ea836940612a9fb96).

**Swarm evidence and scope:** The entry describes a Base prediction scoreboard with IMD/NFT gating; no matched build/audit job was identified.

**Described IMD feature:** Reading IMD balances can enforce entry gates, which is more than passive holding if actually exercised.

**Assessment / unanswered:** A same-name Agent Duel token is not this Base contract. Verify source, an enabled gate and commit/reveal/result transaction; resolver trust and the no-token interpretation remain open.

**Sources / leads:** [project announcement](https://x.com/ArewaOS26/status/2109461424552501309) · [linked repository](https://github.com/0xzahra/agent-duel).

**X:** [@ArewaOS26](https://x.com/ArewaOS26) · 77 followers; 315 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 3 dated in the event window. [Example sampled event post](https://x.com/ArewaOS26/status/2109461424552501309). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-65"></a>

### 65. @Pixel_Pool — Record

Entry `aac8f6dddfa7fefc` · submitted 2026-10-11T04:32:47.308Z.

**Submitted contract:** `0xc280a6159698f73253274d2064c07f7aaeae122d` · [ethereum explorer](https://etherscan.io/address/0xc280a6159698f73253274d2064c07f7aaeae122d).

**Swarm evidence and scope:** Launch 1118 matches PIXEL and PixelPoolHook, supporting swarm-built custom swap logic.

**Described IMD feature:** IMD-paired trades are intended to update a persistent onchain canvas.

**Assessment / unanswered:** Show a swap receipt and corresponding pixel state change. Confirm the IMD pool and hook binding; an initialization-only protocol guard would not establish an active art hook.

**Accepted worker assignments recorded:** implement seats #1650; integrate seats #1542; review seats #61, #788, #1113, #1199 and others; tests seats #1781. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1118 (live)](https://api.imd.fun/launches/3ff2c26d-01fd-497a-8049-e2643075b77d) · [source 661f8bfd](https://github.com/identity-md-launches/launch-1118-pixel-pool/tree/661f8bfdeeeafeb31655a0d2714eafd232a7a67d) · [deployment](https://etherscan.io/tx/0x1e895591af81d6d27e89141b35e4872573d640c51274304056d66a74f79dd95e).

**X:** [@Pixel_Pool](https://x.com/Pixel_Pool) · 5 followers; 5 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/Pixel_Pool/status/2108365362710372496). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-66"></a>

### 66. @Musefren — Record

Entry `c5a7447f3e057a8d` · submitted 2026-10-11T02:26:10.403Z.

**Submitted contract:** `0x815de6ecfc1e0b24b7ae8a5dcc05ba8f5d8f20cc` · [ethereum explorer](https://etherscan.io/address/0x815de6ecfc1e0b24b7ae8a5dcc05ba8f5d8f20cc).

**Swarm evidence and scope:** Launch 1245 matches TitheHook and records a separate TitheToken.

**Described IMD feature:** Swap fees accrue to a configured identity.md seat and claims pay its current owner.

**Assessment / unanswered:** Demonstrate a swap accrual and claim to the then-current NFT owner. The manifest's demo default is seat 1; confirm this is intentional and distinguish the application hook address from its token.

**Accepted worker assignments recorded:** implement seats #368; integrate seats #1536; review seats #38, #225, #632, #1154 and others; tests seats #1081. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1245 (live)](https://api.imd.fun/launches/57e259f6-affc-4561-809b-78f18c35cb41) · [source 7219f0dc](https://github.com/identity-md-launches/launch-1245-tithehook/tree/7219f0dcf5d2609b75de0912c32668a201e9f617) · [deployment](https://etherscan.io/tx/0x7b2bdde1340e4c3f1621312a55f47a2deaf9e587ef9c7d0f0add1ddf97ce6a18).

**X:** [@Musefren](https://x.com/Musefren) · 179 followers; 1,029 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 2 dated in the event window. [Example sampled event post](https://x.com/Musefren/status/2113030116007960784). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-67"></a>

### 67. @Quantum_Canary — Record

Entry `8884b135d32d7214` · submitted 2026-10-10T18:41:53.558Z.

**Submitted contract:** none in the contract field; additional prose/linked artifacts may supply one.

**Swarm evidence and scope:** The specific QuantumCanary construction job and hook job link to live launches 1213 and 1235, supporting swarm build/review/deployment.

**Described IMD feature:** A trading hook is intended to fund an ownerless secp256k1 canary bounty.

**Assessment / unanswered:** The entry omits a contract field. X distinguishes the bounty address from the detector contract. Verify a hook fee transfer to that bounty and the cryptographic threat model; a same-name plain token is not this canary.

**Accepted worker assignments recorded:** implement seats #249, #1201; integrate seats #19, #1136; review seats #6, #88, #127, #153 and others; tests seats #604, #818. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1213 (live)](https://api.imd.fun/launches/5deffe44-44de-4867-98e6-4024ab572588) · [source d620a4c5](https://github.com/identity-md-launches/launch-1213-src-quantumcanary-sol/tree/d620a4c5747e5ed64ab2db2573ef69eb1b02652a) · [deployment](https://etherscan.io/tx/0x353a06e533091c2c31e72765a52f1198617cb9f88986b0a6d5a9c92fce12136f) · [launch 1235 (live)](https://api.imd.fun/launches/e3a73a59-a227-4cef-ae8d-f111c643b4b6) · [source e69c854c](https://github.com/identity-md-launches/launch-1235-src-quantumcanaryhook-sol/tree/e69c854c9ea623bc155f74a8edd8c85e857cf2ac) · [deployment](https://etherscan.io/tx/0x173200d4ef46fe34ebbfde548501a3a26d95b9801cad0d062d647153835bb541) · [job ffb47362](https://explorer.imd.fun/jobs/ffb47362-cdd3-498f-8c1c-911c27666c35) · [job 69561148](https://explorer.imd.fun/jobs/69561148-b678-420c-bf0b-3b6fb49af48f).

**X:** [@Quantum_Canary](https://x.com/Quantum_Canary) · 43 followers; 35 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/Quantum_Canary/status/2108992499654029337). Personal handle declared: [@BreakThePoint](https://x.com/BreakThePoint) (relay resolves: 289 followers, 120 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-68"></a>

### 68. @PlayCourierWld — Record

Entry `07966aa3eee6c40b` · submitted 2026-10-10T13:54:27.383Z.

**Submitted contract:** `0xbab43af01c32a952ff14b395d026cf1874932bc5` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0xbab43af01c32a952ff14b395d026cf1874932bc5).

**Swarm evidence and scope:** The exact linked Courier audit and repository-specific follow-up reviews corroborate swarm auditing.

**Described IMD feature:** A deployed game is described with NFT workers, STAMP emissions and burn-based upgrades.

**Assessment / unanswered:** Need an IMD-dependent live path beyond the audit and a delivery/claim/upgrade receipt. The audit job is a review of imported code, not proof that the swarm authored every game component.

**Sources / leads:** [job 19b34b9b](https://explorer.imd.fun/jobs/19b34b9b-94ef-4543-8d85-b05028860fcf) · [entrant repository](https://github.com/AdamNakamoto/courierworld).

**X:** [@PlayCourierWld](https://x.com/PlayCourierWld) · 378 followers; 234 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/PlayCourierWld/status/2112674842940211259). Personal handle declared: [@mineworldtoshi](https://x.com/mineworldtoshi) (relay resolves: 290 followers, 351 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-69"></a>

### 69. @pinkybond_fun — Record

Entry `65788b040281e2bf` · submitted 2026-10-10T06:25:30.335Z.

**Submitted contract:** `0xb125c461c00863aacad4cc99311d2f23d4342a6f` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0xb125c461c00863aacad4cc99311d2f23d4342a6f).

**Swarm evidence and scope:** Launch 1166 matches PINKY, PinkyVault and PinkyStaking; pinned source contains paid IMD oracle checks.

**Described IMD feature:** IMD-backed promises release or forfeit bonds after a signed transfer-count verdict.

**Assessment / unanswered:** A complete ask/verdict/payout cycle is corroborated below. PinkyVault has an immutable owner address with setters for future protocol/signer/panel terms; disclose that trust boundary.

**Accepted worker assignments recorded:** implement seats #939; integrate seats #687; review seats #131, #527, #1160, #1457 and others; tests seats #205. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1166 (live)](https://api.imd.fun/launches/6e9ac2a3-b5e4-4e2d-bf78-b61a8e2af6be) · [source 1476f830](https://github.com/identity-md-launches/launch-1166-pinkystaking-pinkyvault/tree/1476f8303d30a8d2178bee81a41a7b9c3c5c5326) · [deployment](https://robinhoodchain.blockscout.com/tx/0x4b71a9afc82e925c04588e0bc7eb12525ad47400aceaed479051bf5538e5d65f) · [entrant repository](https://github.com/hexysdev/pinky).

**X:** [@pinkybond_fun](https://x.com/pinkybond_fun) · 59 followers; 16 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/pinkybond_fun/status/2108878028814315521). Personal handle declared: [@hexysdev](https://x.com/hexysdev) (relay resolves: 25 followers, 369 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-70"></a>

### 70. @SovrnIMD — Record

Entry `2e665c8512ba93d5` · submitted 2026-10-09T22:41:56.381Z.

**Submitted contract:** `0x7f7e9b8e9f754c3076e514852552019cb571461b` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x7f7e9b8e9f754c3076e514852552019cb571461b).

**Swarm evidence and scope:** The entered SOVRN address matches swarm launch 1205.

**Described IMD feature:** The entry uses narrative language about trading fueling a listener, without defining its actual IMD-dependent operation.

**Assessment / unanswered:** Require the concrete hook/custom function, agent-work link and transaction. A protocol token record cannot validate the narrative's promised service.

**Accepted worker assignments recorded:** integrate seats #1646; review seats #346, #595, #690, #1357 and others. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1205 (live)](https://api.imd.fun/launches/e1df5b67-98d8-49af-af58-8d501b13cd86) · [source 20c673ed](https://github.com/identity-md-launches/launch-1205-sovrn-one-nine-characters-s-o-v-r-n-o-n/tree/20c673edbaae366464cf2a9568f74a8d11c0a288) · [deployment](https://robinhoodchain.blockscout.com/tx/0xe79cf0498085018330c11c6ac6183e2c03b4b5a3d0ee296326e178b8633f0303).

**X:** [@SovrnIMD](https://x.com/SovrnIMD) · 120 followers; 217 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 4 dated in the event window. [Example sampled event post](https://x.com/SovrnIMD/status/2110188321821311129). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-71"></a>

### 71. @HarvestIMD — Record

Entry `c2bd361f18036ea0` · submitted 2026-10-09T07:40:00.947Z.

**Submitted contract:** `0x390f407adad27a0f267479a8449d6a5c6daa93cf` · [ethereum explorer](https://etherscan.io/address/0x390f407adad27a0f267479a8449d6a5c6daa93cf).

**Swarm evidence and scope:** Launch 1029 and the exact linked job match SwarmHarvester and SwarmSeller; build, specialist reviews and tests are documented.

**Described IMD feature:** The harvester batches official IMD reward claims; seller code converts approved launch assets to IMD with a fee sink.

**Assessment / unanswered:** The cited batch-call receipt is corroborated below. Selling and fee burning need their own transaction evidence; the HARVEST launch pool is ETH-paired, not itself an IMD pair.

**Accepted worker assignments recorded:** implement seats #1080; integrate seats #921; review seats #250, #527, #863, #866 and others; tests seats #160. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1029 (live)](https://api.imd.fun/launches/e3c2f693-9f28-46d0-af84-865a8e9f995a) · [source 388f84e9](https://github.com/identity-md-launches/launch-1029-workflow-contract-stage-context/tree/388f84e9ee292e9a411c0d80c14e8f5f506640eb) · [deployment](https://etherscan.io/tx/0x3506bb74e03e294f3f24b2b390028c063f3ef6180db536e510039eff41620db1) · [job dc212460](https://explorer.imd.fun/jobs/dc212460-0a28-4e3f-9485-2340b7051f1e) · [entrant repository](https://github.com/Nuantree/swarm-harvester-site).

**X:** [@HarvestIMD](https://x.com/HarvestIMD) · 0 followers; 8 lifetime posts (relay metadata). Direct profile sample: 3 authored posts, 3 dated in the event window. [Example sampled event post](https://x.com/HarvestIMD/status/2108433918349434945). Personal handle declared: [@nuantree](https://x.com/nuantree) (relay resolves: 181 followers, 2,157 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-72"></a>

### 72. @swarmpepes — Record

Entry `68f6f994e5e55671` · submitted 2026-10-09T05:32:01.225Z.

**Submitted contract:** `0xce7eb1ad9e2e1c784ea05f7ea4a0fe625923d10a` · [ethereum explorer](https://etherscan.io/address/0xce7eb1ad9e2e1c784ea05f7ea4a0fe625923d10a).

**Swarm evidence and scope:** The entered Swarm Pepes address matches launch 1040 and swarm-deployed NFT/hook artifacts.

**Described IMD feature:** The entry describes onchain NFT art powered by a custom hook.

**Assessment / unanswered:** Explain the exact IMD-dependent feature and demonstrate the mint/trade/state change; the short entry alone does not show why this is more than an ecosystem-branded collection.

**Accepted worker assignments recorded:** implement seats #1528; integrate seats #1116; review seats #83, #976, #1246, #1309 and others; tests seats #905. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1040 (live)](https://api.imd.fun/launches/b2554377-536a-4903-af35-be2fdd674770) · [source 2b618def](https://github.com/identity-md-launches/launch-1040-og-symbol-og-the-launch-s-standard-token/tree/2b618def940c6686b92f10261a03eaca29e8f8ce) · [deployment](https://etherscan.io/tx/0x091cf7f8c7452403bba49c9e7922a51dc86537020a2f5da456b705c23cdfb946).

**X:** [@swarmpepes](https://x.com/swarmpepes) · 586 followers; 118 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/swarmpepes/status/2108177728054731138). Personal handle declared: [@swarmpepes](https://x.com/swarmpepes) (same handle as project) (relay resolves: 586 followers, 118 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-73"></a>

### 73. @jawaisme — Claim

Entry `5fb28c47d0890951` · submitted 2026-10-08T11:42:44.223Z.

**Submitted contract:** `0xa58de121670d27400823b1bb2544570806d4cdbc` · [ethereum explorer](https://etherscan.io/address/0xa58de121670d27400823b1bb2544570806d4cdbc).

**Swarm evidence and scope:** The entry describes ReputationToken and Reputation contracts but supplies no source repository or paid job.

**Described IMD feature:** IMD funds REP minting; REP spending records reputation against X accounts.

**Assessment / unanswered:** Verify the entered contract and a paid mint/reputation transaction. A costly signal does not establish account ownership or trustworthy reputation; the entry text appears cut off.

**Sources / leads:** [submission census](https://www.imdradar.site/api/launchpad?view=hackathon).

**X:** [@jawaisme](https://x.com/jawaisme) · 479 followers; 10,192 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 0 dated in the event window. Personal handle declared: [@jawaisme](https://x.com/jawaisme) (same handle as project) (relay resolves: 479 followers, 10,192 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-74"></a>

### 74. @imdplace — Record

Entry `0653ecb46bd6bf43` · submitted 2026-10-08T09:52:22.142Z.

**Submitted contract:** `0x9aa7bef88c90d237b19afe77c8883ff119b606e7` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x9aa7bef88c90d237b19afe77c8883ff119b606e7).

**Swarm evidence and scope:** Launch 1033 matches PlaceToken and PlaceHook; constructor-created canvas/game helpers are described by the manifest.

**Described IMD feature:** IMD trading earns paint and fees reward pixel ownership/season auctions.

**Assessment / unanswered:** Need buy/paint/revenue/season receipts. The entry appears truncated at the fair-launch detail, so confirm final economics and all helper permissions from deployed source.

**Accepted worker assignments recorded:** implement seats #625; integrate seats #525; review seats #131, #225, #586, #1497 and others; tests seats #1701. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [launch 1033 (live)](https://api.imd.fun/launches/704555aa-6447-4a2a-940d-ac87908e1b96) · [source 4ba07cc1](https://github.com/identity-md-launches/launch-1033-imd-place-symbol-i-p-if-the-launch-refus/tree/4ba07cc1aa427c5cf5ca67f6a0494adf57222ec4) · [deployment](https://robinhoodchain.blockscout.com/tx/0x6eff58ac7d7ca5f44831da053821934cf867bcde6afd2e389400a298099b4570).

**X:** [@imdplace](https://x.com/imdplace) · 20 followers; 22 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/imdplace/status/2110682563605848469). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-75"></a>

### 75. @Illuminatico — Unclear

Entry `69222611f5ae85f9` · submitted 2026-10-08T02:16:00.399Z.

**Submitted contract:** `0x6f035ba278e779ed6c50fff90ec7bfcd2152c969` · [base explorer](https://basescan.org/address/0x6f035ba278e779ed6c50fff90ec7bfcd2152c969).

**Swarm evidence and scope:** The entry supplies an art/meditation slogan and a Base address; no relevant swarm job or technical description was identified.

**Described IMD feature:** No concrete IMD-dependent feature is explained in the submitted text.

**Assessment / unanswered:** Provide an attributed repository, actual IMD work or fee path, deployed custom logic and invocation evidence. Public account/site presence cannot fill the technical gap.

**Sources / leads:** [submission census](https://www.imdradar.site/api/launchpad?view=hackathon).

**X:** [@Illuminatico](https://x.com/Illuminatico) · 398 followers; 3,032 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 3 dated in the event window. [Example sampled event post](https://x.com/illuminatico/status/2112958283891777756). Personal handle declared: not supplied. Ownership/lead identity unverified.

<a id="entry-76"></a>

### 76. @Numosimd — Claim

Entry `23a7fba21d6d968f` · submitted 2026-10-07T22:31:09.569Z.

**Submitted contract:** `0xe45f25c229a2cd274d2a99812858ec342db92ef5` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0xe45f25c229a2cd274d2a99812858ec342db92ef5).

**Swarm evidence and scope:** The entry describes a live number NFT collection but gives no direct swarm job or repository.

**Described IMD feature:** Choosing unique numbers is said to cost IMD; treasury balances and future games are described.

**Assessment / unanswered:** Same-name NUMOS ERC-20 launches are not this NFT collection. Supply the NFT source, mint receipt and IMD payment trace; future games/perks do not count as delivered functionality.

**Sources / leads:** [submission census](https://www.imdradar.site/api/launchpad?view=hackathon).

**X:** [@Numosimd](https://x.com/Numosimd) · 19 followers; 20 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 5 dated in the event window. [Example sampled event post](https://x.com/Numosimd/status/2107962799800426496). Personal handle declared: [@Numosimd](https://x.com/Numosimd) (same handle as project) (relay resolves: 19 followers, 20 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-77"></a>

### 77. @Pepesdotfamily — Record

Entry `968696ec0c926a95` · submitted 2026-10-07T22:20:50.741Z.

**Submitted contract:** `0xe2c46c7068566740a33a4c93f5445b07bcfe5644` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0xe2c46c7068566740a33a4c93f5445b07bcfe5644).

**Swarm evidence and scope:** Exact-address Pepes token audits and repository-specific launchpad reviews corroborate use of swarm security review.

**Described IMD feature:** IMD-paired launches and onchain holder fee distributions are described.

**Assessment / unanswered:** Verify deployed commit, a launch/swap/IMD-dividend cycle and upgrade/admin roles. Reported revenue and volume figures are entrant claims; the entry's assurance that the reward mechanism is risk-free is unsupported.

**Accepted worker assignments recorded:** review seats #2, #6, #420, #1731 and others. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [job 46a0c47b](https://explorer.imd.fun/jobs/46a0c47b-d3ad-4c50-973e-369203a488ce).

**X:** [@Pepesdotfamily](https://x.com/Pepesdotfamily) · 991 followers; 438 lifetime posts (relay metadata). Direct profile sample: 5 authored posts, 4 dated in the event window. [Example sampled event post](https://x.com/Pepesdotfamily/status/2112680103188799990). Personal handle declared: [@TradingTenang](https://x.com/TradingTenang) (relay resolves: 1,907 followers, 1,596 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

<a id="entry-78"></a>

### 78. @0xCompanyIMD — Record

Entry `1d3c41c724c379df` · submitted 2026-10-07T22:02:32.938Z.

**Submitted contract:** `0x5417eaece3885552e777fcf133254e641449ae73` · [robinhood explorer](https://robinhoodchain.blockscout.com/address/0x5417eaece3885552e777fcf133254e641449ae73).

**Swarm evidence and scope:** Specific Zero Person Company audit/recheck jobs corroborate swarm review of the named company repository.

**Described IMD feature:** The entry describes converting rewards to tokenized stocks and dividends.

**Assessment / unanswered:** Match audited commit to the entered contract and show conversion/distribution receipts, backing and admin roles. The submitted project X handle returned not found through the relay, so the account requirement remains unverified.

**Accepted worker assignments recorded:** review seats #36, #912, #1042, #1505 and others. Assignments attest the recorded work roles, not independent quality or original authorship.

**Sources / leads:** [job 4d037a63](https://explorer.imd.fun/jobs/4d037a63-766b-42d8-810a-2ddc7bad2299).

**X:** [@0xCompanyIMD](https://x.com/0xCompanyIMD) · Public project profile unavailable (HTTP 404 in this acquisition); no activity conclusion. Personal handle declared: [@0xCodeRepeat](https://x.com/0xCodeRepeat) (relay resolves: 56 followers, 69 lifetime posts; no separate event timeline collected). Ownership/lead identity unverified.

## Remaining decisions and a fair way to close the evidence gaps

These are **unanswered questions for judging**, not a request to interrupt this report or to supply deployment credentials:

1. **Version and timing:** which immutable commit, contracts and feature invocation constitute each entry at October 21, 23:59 UTC? Separate later fixes/releases from the event version. A submission timestamp, source creation time and deployment time prove different things. Code reused before the event needs an explicit attribution and event-work diff.
2. **Network and token scope:** are the specific testnets approved, and do NFT-only or no-new-token applications qualify under the quoted “token project” requirement? The announcement lists network families; it does not resolve every testnet or product-form question. Apply the same interpretation to all entries.
3. **Runtime proof:** require one minimal evidence chain per entry: exact chain and contract → successful custom function/hook invocation → meaningful state/event → IMD dependency. For oracle products, include the paid Intake request, request/consumer binding, signed answer or failure, settlement and actual transfer. Do not accept one deployment hash as all these steps.
4. **Reproduction:** pin the source commit, compiler/tool versions, vendored dependencies, build/test commands and any unavoidable RPC assumptions. This report inspected source/provenance and selected receipts; **it did not independently reproduce all project builds or rerun the entrants' claimed test totals**. A reproducible protocol bytecode attestation is useful evidence, but not a replacement for reviewers checking what the code does.
5. **Permissions and operational risks:** document owner, upgrade, pause, signer, oracle, pricing, keeper, relayer, callback, timeout, randomness and fee-recipient powers. “No owner” on a token says nothing about an owned hook, router, vault or offchain service. Conditionals, KEPT, Pinky, AgentSkill, NIGHTSHIFT and Stock DEX provide concrete examples where source/manifest settings need more nuance than headline copy.
6. **Identity and receiving wallet:** authenticate project and lead-developer accounts, resolving the 22 missing personal fields and 10 same-handle entries consistently. Obtain a project-authorized receiving wallet; **do not assume an automatically populated deployer is its beneficiary**. Many submissions explicitly distinguish their intended prize wallet from an IMD factory deployer. ENS names and addresses in entries are declarations, not proofs of wallet control. This review does not nominate payout destinations.
7. **Demo and disclosure packet:** verify a publicly accessible short demo, plain-language problem/integration explanation, known risks, reused-code licenses and an explicit list of work completed during the event. A landing page or SDK link can be useful without satisfying this entire packet. Where a field is absent from Radar, check the linked repository before treating it as absent everywhere.

**Assessment:** eligibility should follow the demonstrated product and documented deadline version. X engagement is useful context about communication and community response, but cannot repair missing integration, deployment, transaction or disclosure evidence. Conversely, low follower counts do not invalidate a technically demonstrated project.

## Source preservation, reproducibility and integrity checks

The repository README explains the deliverable and limits. `research/` contains the exact entry snapshot, the two launch indexes, analyst assessments, account/activity tables, post-level source URLs and source-acquisition metadata. The public response archive preserves inspected pages/API data/source text with acquisition timestamps and SHA-256 hashes; it includes negative results so failures are not silently reported as research completed.

The collection code uses only Python's standard library and performs public read requests. The offline checker reads the saved responses, validates hashes and census coverage, verifies the sampled-post date/account filters, and checks the selected transaction/log relationships. It does not send requests or transactions, install software, or certify the underlying research. The required Markdown report is an ordinary untracked output under `artifacts/report.md`; the supporting files are outside `artifacts/` so they can accompany the repository.

**Local-check authority:** these checks establish internal consistency and scope, not independent confirmation of claims, complete security review, or organizer approval. An independent review would still be needed for an authoritative award decision.

