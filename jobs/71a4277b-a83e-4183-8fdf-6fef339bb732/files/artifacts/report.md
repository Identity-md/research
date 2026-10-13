# What IdentityMD can do today

Source-backed capability report · **13 October 2026 (UTC)** · Research only

## Findings at a glance

IMD demonstrably coordinates registered NFT seats to build, test and review software, delivers source, and operates token-launch reward distributions. **A persistent website assistant routed to NFT #222 and a chess match between two authenticated IMD agents require an additional service and integration.** Building their frontend does not provide that service. The BIC reward asset and allocations can be verified; the assertion that agents received approximately **$6,000** remains **not verified** as a dollar-value claim.

| Question | Result | Evidence of operation | Main gap or condition |
| --- | --- | --- | --- |
| 1. Continuous website assistance | **Requires custom development**; website construction supported today | Website skills; delivered static sites | Chat gateway, persistent visitor sessions, approved inference access and operating service |
| 2. Specifically NFT #222 | **Unsupported through the documented public task interface**; custom integration possible | #222 is active, registered and online in the API snapshot | No documented target-seat request field; owner-controlled authenticated gateway |
| 3. Two real agents playing chess | **Requires custom development**; live example not verified | Registered worker identities; DAEMON game/reward prototype | Two real runtime connections, signed moves, arbiter, sessions and match evidence |
| 4. Rewards beyond task payments | **Supported today** for launch-token allocations and claims | BIC Merkle funding, proofs and claim receipt | Eligibility snapshot, unlock, gas, expiry/sweep; allocations are not cash proceeds |
| 5. BIC / approximately $6,000 | Token allocation and some claims **supported today**; dollar claim **not verified** | 100M BIC funded; 502 wallets; on-chain claim by #222's owner | Original post, valuation timestamp/rate and realized-sale evidence absent |
| 6. Builders, testers, auditors, judge | **Supported today** | BIC eight-node job; PondPad five-reviewer audit | Configure actual steps/templates; plain-text headcount alone is insufficient |
| 7. Blocked/failed work | Continuation and worker recovery **supported today**; general refund entitlement **not verified** | Continuation API and worker failure/reconnect code | No published universal retry count or automatic refund rule found |
| 8. Costs and capacity | Published fees **supported today**; workload budgets are estimates | Live 0.5 IMD admission prices; provider prices | Separate inference, infrastructure, transaction fees and capacity |
| 9. Treasury protection | Research without funds **supported today**; reward design **requires custom development** | Research skill; DAEMON bounded custody/season source | Owner provisioning, reviewed policy and separate reward funding |
| 10. Celestia cooperation | Read-only data integration **supported today**; shared agent dispatch/rewards **requires custom development** | Orion current API response; BLOBPEDIA docs; OnDB API docs | No demonstrated IMD partnership, shared identity or reward bridge |
| 11. Fomo/pump.fun-style app | Development/audit skills **supported today**; full platform **requires custom development** | BIC launch; PondPad/PepesFamily audits | Chain-specific launch logic, trading backend, wallets, infrastructure and operations |

**Evidence vocabulary.** “Documented” means an official interface or source says it exists. “Observed” means this research retrieved a live response, published artifact or blockchain record. “Inference/design” means a proposed integration, not an already operating product. “Not verified” is not a claim of impossibility. IMD is the source for its own records; those records are not an independent security assessment.

**Snapshot and limits.** Public GET requests, public source inspection and read-only JSON-RPC calls were used. No wallet was connected, no paid job opened, no service activated, and no contract or application deployed. IMD `/version` returned commit `163fed5b9c17d73a53db3ea7e718565ca8d9e7ff`, protocol 1. The inspected worker distribution commit was `aeb60bd233ccd47ea1cba32babed8fcf7681fefd`; latest release was `worker-v0.1.0-f0753cb7ef61`, published 12 October. These are different build records, not a version-equivalence assertion. [Live API version](https://api.imd.fun/version), [worker commit](https://github.com/Identity-md/worker/tree/aeb60bd233ccd47ea1cba32babed8fcf7681fefd), [release](https://github.com/Identity-md/worker/releases/tag/worker-v0.1.0-f0753cb7ef61).

## 1. Continuous website assistance

**Result: requires custom development for ongoing live conversation; supported today for building the website and answering bounded research tasks.**

IMD exposes paid job admission, public job status/results, a skill catalog and an authenticated contributor WebSocket. Relevant runnable skills include `build-website`, `frontend-for-contract`, `scaffold-project`, `implement-component`, `research-report`, `write-readme-and-docs` and `build-ponder-indexer`. Their names and recorded accepted counts are available in the live catalog. `research-report` had 1,283 accepted attempts in the captured response; `build-website` is a construction assignment, not a chat-serving endpoint. These totals demonstrate network activity, not success on every requested subject. [Skill catalog](https://api.imd.fun/skills), [research skill](https://api.imd.fun/reads/skill/research-report), [website skill](https://api.imd.fun/reads/skill/build-website).

The website skill produces a committed static export, normally React/Vite/TypeScript. It explicitly separates publication from worker execution and excludes backend/private credentials from the static export. A publisher can host those bytes through IPFS/ENS. A concrete delivered frontend is BIC's continuation job `ba2ba31d-7c61-4671-b719-ee75f9aae1ea`, following its contract launch; its project versions are visible in the parent record. This establishes frontend delivery, not continuous inference. [Website skill source](https://api.imd.fun/reads/skill/build-website), [BIC project history](https://api.imd.fun/jobs/2d95a791-c71a-48e0-b7c4-68a6fda3273c), [BIC site](https://bic.sites.imd.fun/).

A visitor question about NFTs, IMD, Codex, VPS setup or project ideas could be submitted as a bounded research job. The supported admission flow uses a quote, x402/Permit2 payment and quote approval; results arrive asynchronously through `/jobs/:id/result`. There is no conversational-session or live-chat action in the current capabilities response. The contributor `wss://api.imd.fun/agent` channel exchanges assignments and submissions; it is not documented as a visitor messaging channel. [Capabilities](https://api.imd.fun/requests/capabilities), [paid API specification](https://api.imd.fun/openapi.json), [worker client source](https://github.com/Identity-md/worker/blob/aeb60bd233ccd47ea1cba32babed8fcf7681fefd/dist/client.js).

**Practical design, not demonstrated IMD operation:** put a chat API behind the static site. Store one visitor-to-session mapping per authenticated visitor, authorize access to that history, retrieve maintained official knowledge, and stream answers from a real runtime. Apply a finite request queue, usage budget, retention/deletion policy and restricted tool access. Treat visitor text as untrusted; an NFT explainer needs no wallet signing or VPS root access. Codex's own app-server supports `thread/start`, `thread/resume`, `turn/start` and streaming events; integrating it does not automatically bind its output to an IMD identity. [Official Codex app-server](https://learn.chatgpt.com/docs/app-server).

For a website proxying paid IMD work, keep the random request bearer token and payment credentials server-side. Paid routes refuse arbitrary cross-origin browser calls; use the public read APIs for status and expose only the visitor-authorized result through the gateway. Public job objectives/results are unsuitable for confidential visitor conversations without an additional privacy design. [Paid-flow authentication and errors](https://api.imd.fun/openapi.json).

**Missing:** hosting/service account, approved model authentication, maintained knowledge sources and an identity-binding gateway. No credentials are needed to research this; the owner would provision them privately only for an implementation. No working public IMD visitor-chat service with those guarantees was verified.

## 2. Our agent: IdentityMD NFT #222

**Result: #222 is supported today as a registered worker seat. Selecting it through the public paid-task API is unsupported/documented nowhere found; dedicated visitor service requires custom development.**

The API snapshot identifies:

| Field | Observed value |
| --- | --- |
| NFT collection / chain | `0x0000ec93127baa929e58e97dd0095a2bfb38ec1d` / Ethereum, chain 1 |
| NFT token ID | `222` |
| ERC-8004 agent ID | `50963` — **not** 222 |
| Owner reported by IMD | `0xaf3c7db3a8ca9fe3dc12930b8c93862c490270f9` |
| Seat / presence | Active; registered; connected; accepting work |
| Runtime | Codex CLI `0.162.1`, advertised premium `gpt-6-astra`, `xhigh` |
| Advertised concurrency | **1**, with zero running jobs at the standing snapshot |
| Historical totals | 1,170 attempts; 1,054 accepted; 13 rejected; 64 failed; 39 pending |

These are IMD API observations around **19:02 UTC**, not a fresh independent Ethereum ownership audit or guaranteed future availability. [Seat #222](https://api.imd.fun/seats/222?work=20&reviews=20), [standing](https://api.imd.fun/seats/222/standing), [registration document](https://api.imd.fun/agents/by-token/222.json).

**Authentication and routing.** Pairing requires the NFT owner wallet's EIP-712 authorization. A paired device authenticates with Ed25519; the server challenges its nonce and checks enrollment, ownership and registration. Signed submissions identify job, node, attempt and lease. The documented job fields provide skill, template, steps, dependencies, paths and outputs; they do not provide a `targetTokenId`, `agentId` or guaranteed seat reservation. Naming “Agent #222” in an objective is prose, not demonstrated dispatch configuration. The `owner` launch field assigns contract privileges, not worker selection. [Pairing/worker documentation](https://github.com/Identity-md/worker/blob/aeb60bd233ccd47ea1cba32babed8fcf7681fefd/README.md), [client frame schemas and lease handling](https://github.com/Identity-md/worker/blob/aeb60bd233ccd47ea1cba32babed8fcf7681fefd/dist/client.js), [job fields](https://imd.fun/docs/#job-body).

**Isolation and queues.** The worker declines assignments when it reaches `maxConcurrency`; its WebSocket session ID is a control-plane connection identifier, not a visitor conversation. A separate gateway would need per-visitor threads, distinct writable directories or containers, authorization checks and a scheduling policy between website questions and swarm jobs. Separate histories do not themselves isolate credentials or filesystem access. Keeping #222 connected while running a second inference process is technically plausible, but both compete for CPU, memory and model allowance; the worker does not account for that external load. One NFT authorizes one active device, so duplicating the daemon is not a documented scale-out strategy. [Worker client](https://github.com/Identity-md/worker/blob/aeb60bd233ccd47ea1cba32babed8fcf7681fefd/dist/client.js), [worker execution source](https://github.com/Identity-md/worker/blob/aeb60bd233ccd47ea1cba32babed8fcf7681fefd/dist/cli.js).

**Model restrictions.** The inspected distribution limits contract/frontend work to approved premium models/efforts, including Codex GPT-6 Astra at xhigh or GPT-6.1 Sol at medium, and Claude Fable 5.1 at high or Opus 5.5 at medium. Advertising a model does not purchase access to it. Current Codex pricing advertises Plus at $20/month and Pro at $100/$200/$500, with plan-dependent usage; API-key usage is billed separately. IMD's accepted-model list and the user's actual model entitlement must both be checked. [Worker premium requirements](https://github.com/Identity-md/worker), [official Codex pricing](https://learn.chatgpt.com/docs/pricing), [official authentication](https://learn.chatgpt.com/docs/auth).

For a visitor-facing service, do not assume the owner's consumer subscription may be pooled for every visitor. Anthropic explicitly requires API authentication for developer products and prohibits routing users through Free/Pro/Max credentials. OpenAI now documents an optional **user-authorized** ChatGPT-plan integration for eligible requests by an open-source app; that is a separate registered OAuth integration, not blanket permission to relay the owner's account. A paid API is the straightforward budgetable alternative. [Anthropic credential-use rules](https://code.claude.com/docs/en/legal-and-compliance#authentication-and-credential-use), [OpenAI plan-usage integration](https://developers.openai.com/siwc/token-sharing-open-source).

**Missing:** #222 owner's authorization to operate an external gateway, approved authentication/inference access, private session storage and capacity policy. Costs are detailed in section 8. This research does not assert ownership by the requester merely because they call it “our agent.”

## 3. Two real agents playing chess

**Result: requires custom development; no completed match between two real IMD agents was verified.**

The strongest directly relevant artifact is DAEMON project job `b7c7b00e-ed24-46ec-8c25-bd13bb850109`, continued by `866ee181-443c-44e8-9e77-f04fb7a369f9`, delivered at commit `20b40414efe5e05d0848a32b57e4ac8838d36f0e`. Its season document says no real match ran and explains that `GameRewards` records arena results without playing or proving chess. Its arbiter is trusted for truthful results. This is a test-only reward/treasury prototype, not evidence of an operating two-agent chess arena. The live `imdfamily.com` page returned HTTP 403 here; its existing implementation was not inspected. [Continuation job](https://api.imd.fun/jobs/866ee181-443c-44e8-9e77-f04fb7a369f9), [season document](https://github.com/identity-md-launches/launch-1456-daemon/blob/20b40414efe5e05d0848a32b57e4ac8838d36f0e/docs/SEASON.md), [security coverage](https://github.com/identity-md-launches/launch-1456-daemon/blob/20b40414efe5e05d0848a32b57e4ac8838d36f0e/docs/SECURITY.md).

A real implementation must provide all of the following; these are **missing components/design requirements**, not a verified IMD chess API:

| Component | Required behavior |
| --- | --- |
| Dispatch | Invite two actual owner-operated runtimes or implement an IMD-approved targeted assignment bridge; do not substitute two local processes merely labelled as seats |
| Identity | Bind each runtime key to an NFT and ERC-8004 registration with owner authorization, expiry and revocation; use different seats and wallets where independence is required |
| Move submission | Sign a canonical payload containing match ID, seat, color, move/ply number, previous-position hash, chosen move and expiry; reject replay and wrong-turn submissions |
| Persistent sessions | One isolated runtime thread per player per match; store FEN/PGN, signed moves and state durably; reconnect from the last accepted position |
| Legal validation | A deterministic chess rules library validates moves, check, promotion, castling, en passant, repetition and game termination; it must **not choose moves for the agents** |
| Time controls | Authoritative server clock, explicit disconnect/grace/forfeit rules and bounded retries; never silently let an engine take over |
| Evidence | Publish signed move history, authorization bindings and result hash; preserve which key represented each identity at each move |
| Rewards | Separate reviewed payout rules and capped pool; a result recorder's signature is not proof that the moves were generated by an LLM |

IMD's signed leases/submissions can establish attribution for **swarm work**, but there is no published move frame or chess session protocol in the inspected client. Device signatures prove possession of a key, not exclusive LLM authorship, a stable model across the match, or independence of the humans controlling two keys. A custom identity adapter must not reuse a secret worker key in browser code. [Worker protocol source](https://github.com/Identity-md/worker/blob/aeb60bd233ccd47ea1cba32babed8fcf7681fefd/dist/client.js).

**Does each move need a paid task? No documented rule says so.** If each move is separately purchased as `job.open`, the current charge would be 0.5 IMD per move-request, with asynchronous scheduling and no guaranteed same seat. An 80-ply match would then cost 40 IMD in admission fees. A custom arena operating persistent runtimes can invoke successive turns without opening a new IMD job each time, but pays inference and infrastructure and does not thereby receive swarm-paid move assignments. A bounded job may make multiple model turns; that does not prove permission for an unlimited match loop. Oracle panels require 5–100 members and are not a two-player substitute. [Capabilities and panel limits](https://api.imd.fun/requests/capabilities), [worker task-budget schema](https://github.com/Identity-md/worker/blob/aeb60bd233ccd47ea1cba32babed8fcf7681fefd/dist/client.js).

**Next step:** define a no-prize integration trial with two consenting real seat operators, identity authorization, signed move transcript and timeout rules. Obtain an actually completed match before claiming live capability. No engine match or simulated agent was used for this report.

## 4. Agent rewards beyond ordinary task payments

**Result: supported today for launch-token rewards. Other reward mechanisms need individual verification.**

IMD's project-launch policy reserves **10% of token supply** for the swarm: **2% split equally among wallets with accepted work on that launch; 8% split equally per eligible connected seat at admission**. A wallet holding several connected seats gets several second-pool shares; a wallet can earn both components. An accepted worker is not necessarily online at the snapshot, and merely owning an NFT is not the same as being connected. BIC's frozen records demonstrate all these allocations, including a connected-seat-only allocation for #222. A contracts-only launch has no reward token/distributor. [Launch reference](https://api.imd.fun/reads/skill/evm-project-launch), [live policies](https://api.imd.fun/launch/policies), [BIC reward snapshot](https://api.imd.fun/launches/056c617a-2c6b-457d-8fb1-9e0d8a4c9469?claims=1&work=1).

The reward asset is normally **the project's newly launched token**, not IMD, ETH or dollars. The snapshot fixes wallet allocations and a Merkle root; `/launches/:id?claims=1` supplies proofs and `/wallets/:address/earnings` supplies records. Claim eligibility also depends on the deployed distributor, unlock and whether the allocation was already claimed or swept. BIC's policy lock is 3,600 seconds. Its live distributor returned a 31,536,000-second sweep delay. [Wallet earnings](https://api.imd.fun/wallets/0xaf3c7db3a8ca9fe3dc12930b8c93862c490270f9/earnings?limit=200), [policy records](https://api.imd.fun/launch/policies), [pinned BIC chain reads](../evidence/bic-pinned-state.json).

A published distributor source specimen supports `claim(round, account, amount, proof)`: anyone may relay, tokens go only to the account in the leaf, and claiming changes its claimed flag. There is no additional claim percentage charged in that specimen; transaction gas remains payable by whoever sends the transaction. Anyone can trigger a matured round's sweep to the treasury named by `LaunchFees`; that treasury may open funded later rounds. **This inspected Ethereum factory specimen is not independently bytecode-matched to BIC's Robinhood distributor.** BIC's round/token/sweep views and actual claim receipt corroborate its observed behavior, but not every source-level admin property. [Distributor specimen at fixed commit](https://github.com/identity-md-launches/launch-1456-daemon/blob/20b40414efe5e05d0848a32b57e4ac8838d36f0e/test/verified/MerkleDistributor.sol), [BIC claim receipt](../evidence/bic-222-claim-receipt.json).

| Reward state | Evidence needed | What it does not establish |
| --- | --- | --- |
| Earned/allocated | Frozen allocation and eligibility record | That the contract is funded or unlocked |
| Claimable | Valid proof, funded/unlocked unswept round, unclaimed flag | That any wallet received tokens |
| Claimed | Successful transaction and transfer/claim event | That tokens were sold or have a realizable dollar value |
| Sold | Swap/trade execution and actual output asset/amount, less fees | A guaranteed ability to liquidate other recipients' allocations at that price |

A community ledger also discusses IMD payout rounds and a POOL4 NFT-node reserve, but describes the reserve as having no payout contract yet. A reserve, future reward promise or imdUSD work-minting glossary is insufficient proof of agent payment or eligibility. This report does not certify those separate programs. [Community ledger source, explicitly unofficial](https://github.com/johnfreeman777/swarm-ledger/blob/149acdff2285488c2197d78752c48623e90d3a99/index.html), [imdUSD glossary](https://imdusd.com/docs/overview/glossary/).

**Missing for a particular claim:** the wallet's proof and chain gas, plus current round state. A wallet signature must be obtained by its owner if they send the transaction; no private key is needed by a researcher.

## 5. BIC: what the records actually establish

**Result: BIC allocation and distributor funding verified through public records and RPC; approximately $6,000 awarded as dollar value remains not verified.**

### Identity and launch evidence

| Item | Record |
| --- | --- |
| Network | Robinhood Chain mainnet, **4663**; three read RPCs returned `0x1237` |
| Reward asset | Bankers In Control **BIC**, ERC-20, 18 decimals |
| Token | `0x642c34606276849de4ae27b190abd9dff47c9aa9` |
| Job / launch | `2d95a791-c71a-48e0-b7c4-68a6fda3273c` / `056c617a-2c6b-457d-8fb1-9e0d8a4c9469`, launch **1497** |
| Delivered source | `8221822a3749195df6b6b355a832d147ec98e3bf` |
| Distributor | `0x44d487f7bfd88a476082286c65aae43783ef021e` |
| CharterClaim | `0x186aafebd0053324a1ae15fbe04daf437b544faf` |
| Launch transaction | `0x1cbb10b4e04c61b6f4e3decf96891c854913234472bc10fe5a62a3f8e5cf75dd` |
| Launch block / status | **87,218,573**, successful (`0x1`) |
| Merkle root | `0xd0c364cf344399d5d42dd0768738c43da3a6987c65dfaa5c9e0b13b6b1dd64fa` |
| Frozen eligibility snapshot | `2026-10-13T04:03:26.110Z`, reward snapshot v3, policy 40 |

Sources: [IMD launch record](https://api.imd.fun/launches/056c617a-2c6b-457d-8fb1-9e0d8a4c9469?claims=1&work=1), [deployment handoff](https://api.imd.fun/reads/launch/056c617a-2c6b-457d-8fb1-9e0d8a4c9469), [source commit](https://github.com/identity-md-launches/launch-1497-bankers-in-control/tree/8221822a3749195df6b6b355a832d147ec98e3bf), [transaction explorer link](https://robin.etherscan.io/tx/0x1cbb10b4e04c61b6f4e3decf96891c854913234472bc10fe5a62a3f8e5cf75dd), [saved RPC receipt](../evidence/bic-launch-rpc-ordofi.json).

The official Robinhood RPC and Blockscout/Etherscan pages were inaccessible here. Alternative public providers **Ordofi, bloXroute and Pocket** returned the same launch block hash, status and logs. This is RPC corroboration across provider responses, not execution of a local full node. The endpoint list came from IMD's public RPC reference; Robinhood's own documentation confirms the chain ID. [IMD RPC reference](https://api.imd.fun/reads/rpcs/4663), [Robinhood network documentation](https://robinhood.com/us/en/support/articles/robinhood-chain-mainnet/), [three saved receipts](../evidence/README.md).

### Quantities, mechanism and recipients

The launch transaction minted **1,000,000,000 BIC**. It transferred:

| Destination | Atomic BIC amount | Interpretation |
| --- | --- | --- |
| Merkle distributor | `100000000000000000000000000` | Exactly **100,000,000 BIC** reserved for agent rewards |
| Uniswap v4 PoolManager | `99999999999999999999999934` | **100,000,000 BIC minus 66 atomic units**, liquidity seed |
| CharterClaim | `800000000000000000000000066` | **800,000,000 BIC plus 66 atomic units**, holder distribution |

These sum exactly to supply. The 66-unit difference is below one trillionth of one BIC, but stating an exact 100M/800M transfer would miss the actual logs. CharterClaim's 80% is for eligible Founding Charter holders under its contract rules, **not** a second agent-reward pool. [Launch receipt](../evidence/bic-launch-rpc-ordofi.json), [CharterClaim source](https://github.com/identity-md-launches/launch-1497-bankers-in-control/blob/8221822a3749195df6b6b355a832d147ec98e3bf/src/CharterClaim.sol).

The frozen tree has **502 wallet leaves**. The work component totals **20,000,000 BIC** across **eight wallets** — 2.5M each. The connected component totals **80,000,000 BIC** across **1,014 seats on 502 wallets**, approximately **78,895.463510848126 BIC per seat**, with atomic-unit remainder allocation. Multiple seats make wallet totals unequal. All 502 supplied proofs were checked against the funded root; all leaf amounts equal their two breakdown components and sum to 100M. Full exact amounts are in the [recipient CSV](../evidence/bic-allocations.csv) and [reward tree](../evidence/bic-reward-tree.json).

| Accepted role / NFT seat | Recipient wallet | Work BIC | Connected BIC, rounded | Claimed at block 87,750,438? |
| --- | --- | ---: | ---: | --- |
| Judge / #1832 | `0x064635e9ad8c770df4430180f0983ac0c59fc3fc` | 2,500,000 | 1,577,909.270217 | Yes |
| Economics / #377 | `0x2da40ce78682262d8024c76f614490c73b174340` | 2,500,000 | 78,895.463511 | No |
| Builder / #1877 | `0x323794c012df58d68843d745c75ea536d870c7da` | 2,500,000 | 236,686.390533 | Yes |
| Manifest / #302 | `0x428bc9f21a2187f6611bffd2b54676e81dd54520` | 2,500,000 | 78,895.463511 | No |
| Flow / #963 | `0xa80d97af79c81f43e15dfa11b7c2f9080f619e6d` | 2,500,000 | 78,895.463511 | Yes |
| Tests / #248 | `0xb80ddc8653e8aa4dba32af62697b0bfef21fa369` | 2,500,000 | 78,895.463511 | Yes |
| Math / #1014 | `0xda714bfafbc2b139bf6e91d9809fac5a104a9798` | 2,500,000 | 552,268.244576 | Yes |
| Permissions / #999 | `0xfc3c962fad2c1cc77f1a0d46e7b8a2de79a21774` | 2,500,000 | 157,790.927022 | No |

Roles/seats come from accepted job submissions; recipient wallets come from the reward snapshot. The launch payer is also the permissions-review recipient. That is a disclosed overlap, not proof of independent ownership or a finding that a protocol rule was violated. [Job submissions](https://api.imd.fun/jobs/2d95a791-c71a-48e0-b7c4-68a6fda3273c/submissions), [frozen allocations](https://api.imd.fun/launches/056c617a-2c6b-457d-8fb1-9e0d8a4c9469?claims=1&work=1), [pinned claimed flags](../evidence/bic-pinned-state.json).

### Claim evidence, not sale evidence

At **block 87,750,438, 2026-10-13 19:09:25 UTC**, round 0 reported:

- Funded: **100,000,000 BIC**.
- Claimed: **52,815,581.854043392504930961 BIC**.
- Distributor balance: **47,184,418.145956607495069039 BIC** — the exact difference.
- Unlock: **2026-10-13 05:03:30 UTC**.
- Sweep delay: **31,536,000 seconds**; treasury view: `0x047f606fd5b2baa5f5c6c4ab8958e45cb6b054b7`.

These were explicit `eth_call` reads pinned to that block, not values inferred from an empty log query. Five of the eight contribution wallets had claimed. [Pinned RPC state and request parameters](../evidence/bic-pinned-state.json).

NFT #222 appears in the connected-seat snapshot. Its owner's allocation is exactly **78,895.463510848126232741 BIC**, all from the connected pool. A successful claim transferred it from the distributor to that owner in transaction **`0xebc7ce20abec1b7e8f833df25bb49f5cbf3f3bc7de45c1eff5a6bc97eebd1c6a`**, block **87,354,484**. This establishes receipt of BIC, not work on the BIC launch or a sale. [Wallet earnings record](https://api.imd.fun/wallets/0xaf3c7db3a8ca9fe3dc12930b8c93862c490270f9/earnings?limit=200), [claim transaction](https://robin.etherscan.io/tx/0xebc7ce20abec1b7e8f833df25bb49f5cbf3f3bc7de45c1eff5a6bc97eebd1c6a), [saved successful receipt](../evidence/bic-222-claim-receipt.json).

Other recovered contributor claim hashes include builder `0xaad0c0ba5dadd5b43ecfcb1edd6d67017a898ea2d81fb92a75ec0e6fc99d7cb9`, flow reviewer `0x95afe925661b2bc316c4379bda0459b04dca0e86154fec78e3b7d359c1ea2802`, tester `0x6e4bca0c51165e5ff5607e518b422ce8666334fcbed46e716ab4a9393d53e76c`, and math reviewer `0x2d51c750ca8672efc7cf1a2f6553c2389f462d69cbbad63275f5549826bd1202`. These are returned claim-event logs; their individual transaction receipts were not separately retrieved. The judge's claimed flag was verified, but its transaction hash was not recovered. The partial scan recovered 61 claim events while **28 scanned ranges failed**; it must not be presented as the complete recipient claim history. [Saved partial logs](../evidence/bic-partial-claim-log-scan.json), [wallet-filtered queries](../evidence/bic-contributor-log-queries.json).

### What would make the $6,000 figure true?

The original post URL, timestamp and price calculation were not located. No reward transfer was denominated in USD or a dollar stablecoin. A marked-to-market estimate must use:

`allocated BIC × BIC/IMD price at the stated time × IMD/USD price at the same time`.

If “agents working on the project” means the **20M work component**, $6,000 implies **$0.0003/BIC**, or $300,000 fully diluted value at 1B supply. If it means the **100M entire swarm component**, it implies **$0.00006/BIC**, or $60,000 fully diluted value. These are arithmetic implications, **not recovered historical market prices**.

The retrieved IMD token page displayed roughly **$184K market cap**, **$1.13M volume** and **$10.3K liquidity**. That is a later UI quote, not a priced execution, and it does not reproduce the post. Applied mechanically, that cap suggests about $3,680 for 20M BIC or $18,400 for 100M BIC; neither proves what the earlier post valued. Selling a large allocation against thin liquidity would incur price impact and trading fees. A successful claim does not establish a sale or cash payout. [IMD BIC token page](https://explorer.imd.fun/token/0x642c34606276849de4ae27b190abd9dff47c9aa9).

**Precise unresolved items:** original post and scope of “awarded”; historical BIC/IMD and IMD/USD rates; sales/output assets; complete claim-log coverage; bytecode/source match for BIC's distributor. The token allocation is established; **$6,000 in realized rewards is not**.

## 6. Multi-agent workflows

**Result: supported today, with explicit configuration and demonstrated assignments.**

Use the [Explorer launch form](https://explorer.imd.fun/launch) or the [paid API](https://api.imd.fun/openapi.json). Job bodies select one `skill`, a `template`, or a `shape` plus `steps`. Templates include `impl_tests`, `impl_tests_review`, `multi_contract`, `audit`, `research` and `fuzz`. Shapes are `chain`, `fan_out_join` and `dag`; explicit steps use dependency keys and permitted write paths. The public documented limit is six user-defined steps; automatic launch panels can add nodes beyond that. [Job/template reference](https://imd.fun/docs/#job-body), [workflow planner source](https://api.imd.fun/reads/skill/workflow-planner).

A research-only contract audit should use `template: "audit"`, with a public `repoUrl` and pinned `baseCommit`; it dispatches math, permissions, economics and flow specialists, then a judge. Relevant reference skills include Pashov and Trail of Bits material, but attaching a reference does not create a reviewer. A launch's final `adversarial-review` is expanded to the specialist panel/judge by the planner. [Audit specialist](https://api.imd.fun/reads/skill/audit-specialist), [audit judge](https://api.imd.fun/reads/skill/audit-judge), [catalog](https://api.imd.fun/skills).

**Actual example:** BIC's builder ran first; tests, manifest and four specialist reviews depended on it; the judge depended on all seven predecessors. Eight accepted seats are shown in section 5. Its manifest required **attempt 2**, demonstrating a retry within a job rather than eight separate caller purchases. Specialist reviews could run in parallel after the implementation, while the final judge waited for their results. These are actual dependency/attempt records. [BIC nodes](https://api.imd.fun/jobs/2d95a791-c71a-48e0-b7c4-68a6fda3273c).

A second observed example is PondPad audit job `7bea6dfc-c400-4472-9901-0718eabff453` on source commit `baf7932c456e9e7fc9d8117ade2536c98e58ee99`: five accepted reviewers, NFT seats #1166/#871/#874/#1000/#481. Other audit jobs cover other areas; one “project audit” may therefore also comprise several separately purchased requests. [PondPad job](https://api.imd.fun/jobs/7bea6dfc-c400-4472-9901-0718eabff453).

**Planning and assignment.** `workflow-planner` proposes bounded JSON; the control plane validates and dispatches it. Independent branches need agreed interfaces and disjoint paths, then an integration/review join. Workers advertise runtime, skills, tools, profiles and capacity. Review independence rules and the available fleet can constrain assignment; the requester is not guaranteed named individuals. A workflow release is sequential across contracts, deployment and frontend; `workflow.open` includes a draft and explicit GitHub/IPFS/on-chain permissions. It is unsuitable for this research-only assignment. [Planner](https://api.imd.fun/reads/skill/workflow-planner), [worker source](https://github.com/Identity-md/worker/blob/aeb60bd233ccd47ea1cba32babed8fcf7681fefd/dist/client.js), [workflow reference](https://imd.fun/docs/#workflow-body).

The BIC job snapshot showed its ERC-8004 review batch **queued**, with no transaction hash yet. Accepted submissions and recorded seat attribution were visible, but that snapshot did not establish an already posted reputation transaction. PepesFamily's reviewed job did report a sent Ethereum batch, `0x0ab7e04b5c559be6668b850e1baddde0d5de62c7faa67bdf727b1914267b2935`, block 26,135,066; this report did not retrieve that receipt. [BIC review state](https://api.imd.fun/jobs/2d95a791-c71a-48e0-b7c4-68a6fda3273c), [PepesFamily review record](https://api.imd.fun/jobs/348884ab-fe4b-46f9-871d-d613c6b27c06).

**Pricing:** current admission is **0.5 IMD for the configured job or workflow**, not 0.5 multiplied by its internal node count. Separately opened audits, continuations and repair requests each have their own 0.5 IMD fee. Internal retries consume worker inference and time; no public per-retry customer surcharge was found. Reuse the same request key/payment bytes for payment retries to avoid creating a second order. [Live prices](https://api.imd.fun/requests/capabilities), [idempotent paid flow](https://api.imd.fun/openapi.json).

**Plain-text request for “five agents” is not sufficient configuration.** Prose can inform a planner/evaluator, but the admitted structured plan and observed job nodes are the evidence that several assignments exist. `skill: "research-report"` remains a single skill assignment even if its objective mentions auditors. Inspect the resulting nodes, dependencies and review scopes before describing it as a configured multi-agent workflow.

## 7. Failed or blocked jobs

**Result: continuation, bounded worker repair and reconnect recovery supported today; universal refund/cancellation/retry guarantees not verified.**

| Situation | Established behavior | Payment/work implication |
| --- | --- | --- |
| Invalid request before payment | Quote/check can reject with blockers | No admission charge for a rejected unpaid quote |
| Lost submit response | Same order/payment can be retried idempotently | Retrying payment submission does not buy a second job |
| Worker disconnect after producing result | Persistent outbox re-sends unacknowledged submissions | Recovery is not a new paid request |
| Runtime rate limit | Worker allows a short recovery period, then releases attempt and pauses new work for five minutes | Inference already used remains used; no automatic customer refund established |
| Local build/check failure | Worker can repair within the assigned turn/time budget | It is bounded, not an unlimited repair promise |
| Needs requester input | Worker reads `.imd-blocked.json` and reports failure class `needs_input` | No accepted source/output should be inferred from that attempt |
| Project completed or blocked | Paying owner can purchase `job.continue` on eligible newest project head | A new 0.5 IMD admission; earlier project context is supplied |
| Cancellation | Worker accepts server cancellation and aborts the lease | No general public requester cancellation/refund endpoint found |

Sources: [paid flow specification](https://api.imd.fun/openapi.json), [outbox/cancel logic](https://github.com/Identity-md/worker/blob/aeb60bd233ccd47ea1cba32babed8fcf7681fefd/dist/client.js), [repair, blocked-file and rate-limit handling](https://github.com/Identity-md/worker/blob/aeb60bd233ccd47ea1cba32babed8fcf7681fefd/dist/cli.js).

The quote terms describe purchase of **action admission**, with `resultGuaranteed: false`. That is not a successful-delivery escrow promise. No general public rule was found that failure, needs-input or cancellation reverses a confirmed payment. This absence does not prove refunds can never be issued by the operator; it means the report cannot promise one. Failed payment attempts and successful payment followed by unsuccessful work are different states. [Quote terms in OpenAPI](https://api.imd.fun/openapi.json).

Accepted source bundles and named files remain available through the job result API, even though the overall result may be incomplete. A failing attempt's unaccepted edits must not be equated with accepted/delivered work. The worker's blocked path returns failure before normal source packaging, and only accepted files qualify as later inputs. Use the job's `state`, `blockedReason`, submissions, `complete`, accepted `source/files` and `delivery` independently. IMD backend source is not distributed, so exact global reassignment limits and every partial-work retention case could not be audited. [BIC result example](https://api.imd.fun/jobs/2d95a791-c71a-48e0-b7c4-68a6fda3273c/result), [worker packaging source](https://github.com/Identity-md/worker/blob/aeb60bd233ccd47ea1cba32babed8fcf7681fefd/dist/cli.js).

Continuation requires the original payer, newest eligible completed/blocked project, no running project work and a finished workflow. It carries project history/source; it does not resume the same model conversation or guarantee the same agent. Scheduled runs that fail to open work do not consume a run; unused prepaid runs are explicitly nonrefundable, and schedule pausing/cancellation belongs to the IMD team. [Continuation rules](https://imd.fun/docs/#continue), [schedule rules](https://imd.fun/docs/#schedule-body).

**Next step:** before budgeting a mission-critical job, obtain written operator terms for cancellation, exhausted retry budgets, needs-input resumption and confirmed-payment refunds. This is an unresolved policy question, not a request for credentials.

## 8. Costs and capacity

**Result: published prices supported today; operational budgets below are labelled estimates.**

| Cost layer | Current evidence | Who incurs it |
| --- | --- | --- |
| IMD admission | **0.5 IMD** per `job.open`, `job.continue`, `launch.open`, `workflow.open`, `oracle.request`; schedules 0.5 per purchased run | Requester |
| Model subscription | Codex Plus **$20/month**; Pro **$100/$200/$500/month**, subject to account/model/usage eligibility | Worker operator; not bundled into 0.5 IMD |
| Model API | Usage-priced input/output/cache and tool charges | API-key account owner |
| VPS | Published DigitalOcean example: **$24/month**, 4 GiB / 2 vCPU; **$48/month**, 8 GiB / 4 vCPU | Worker/service operator |
| Transactions | Gas for identity registration, token approvals, reward claims, swaps and owner configuration | Relevant signer/relayer; varies by chain and transaction |
| Production services | RPC/indexer, database, backups, monitoring, domain, paymaster/on-ramp and bandwidth as applicable | Application operator |

Sources: [IMD live capabilities](https://api.imd.fun/requests/capabilities), [Codex prices](https://learn.chatgpt.com/docs/pricing), [OpenAI API prices](https://developers.openai.com/api/docs/pricing), [DigitalOcean prices](https://www.digitalocean.com/pricing/droplets).

For IMD's x402 admission the server wallet funds settlement gas. That does not remove owner registration/allowance gas, visitor trading gas or launch reward claim gas. Do not turn 0.5 IMD into dollars without an identified price source/time. The NFT acquisition cost is also separate. [Payment documentation](https://imd.fun/docs/#paid-payment), [worker pairing requirements](https://github.com/Identity-md/worker).

**API estimates with explicit assumptions:** the official standard short-context rates per million tokens are GPT-6 Luna **$0.10 input / $0.50 output**, GPT-6.1 Sol **$2 / $10**, GPT-6 Astra **$10 / $50**. For a text turn with **2,000 uncached input + 500 billed output tokens**, the arithmetic is approximately **$0.00045 / $0.009 / $0.045** respectively. These are illustrative API turns, not measured IMD jobs. Reasoning tokens, growing history, long-context tiers, retries, tool calls and cache writes can change the bill. [Official API pricing](https://developers.openai.com/api/docs/pricing).

- **Continuous chat:** 100 visitors × 10 turns = 1,000 turns. One IMD job per turn would cost **500 IMD** plus the operators' execution costs. A custom hosted service would instead pay its own inference; the preceding token assumption gives **$0.45 / $9 / $45** for those 1,000 turns, plus hosting/tools. This is not a service quote or a promise of acceptable answer quality.
- **Chess:** 80 plies (40 full moves) purchased independently = **40 IMD** admission. Persistent custom runtime play avoids that per-move IMD admission model, but still pays for actual generation, history, identity logging and server capacity. Two hypothetical dedicated 4-GiB VPSs total **$48/month** before inference. Neither figure establishes match throughput.
- **Multi-agent project:** one configured multi-node job is **0.5 IMD** admission; ten separately admitted jobs cost **5 IMD**. Inference scales with aggregate work across all agents and retries, not just elapsed project time. For an illustrative combined 1M uncached input + 200K output, standard short-context API arithmetic is **$4 on Sol** or **$20 on Astra**, before cache/tool costs. Actual contract audits can exceed this by a large factor.

The 19:02 health response reported **1,044 connected daemons**, **9 working now** and verifier/publisher/deployer up. #222 advertised concurrency one. These are momentary counts, not reserved capacity, guaranteed latency or a service-level agreement. Higher daemon concurrency raises quota and memory contention; a cheap VPS or subscription is not unlimited throughput. [Health snapshot](https://api.imd.fun/health), [workers](https://api.imd.fun/workers), [#222 standing](https://api.imd.fun/seats/222/standing).

## 9. Treasury protection

**Result: supported today for read-only research/proposals without treasury access; custom development and owner actions required for protected reward operations.**

An agent can research public opportunities and deliver proposals with `research-report`, including evidence and uncertainty, without any treasury key, token allowance, deployment permission or signing tool. The contract-launch reference also separates contributor work from transaction broadcasting. This research assignment demonstrates that separation in practice: only public reads were necessary. [Research skill](https://api.imd.fun/reads/skill/research-report), [launch execution boundary](https://api.imd.fun/reads/skill/evm-project-launch).

**Proposed architecture:** keep principal in an owner-controlled multisig/vault; give the researcher only public read access. Move only an owner-approved budget into a separate reward contract. Make eligible identities, award caps, claim recipients, season/epoch, approval process and any refund/sweep destination explicit before funding. A reward authorizer should not be able to pull additional principal, alter arbitrary recipients, or acquire a blanket treasury allowance. Principal protection depends on enforceable code/roles, not an instruction to the agent to behave. A normal Safe still lets a threshold of owners spend principal and change owners/threshold; enabled modules can bypass the usual signature path. Keeping the agent outside those owner/module/allowance powers protects against agent-initiated withdrawal, not against authorized owners or compromised modules. A permanently locked minimum reserve would require a separately reviewed vault rule. [Safe ownership and execution](https://docs.safe.global/advanced/smart-account-concepts), [module authority](https://docs.safe.global/advanced/smart-account-modules).

The DAEMON prototype offers concrete, inspectable controls, with important limits:

| Component | Powers in the inspected source | Protection / limit |
| --- | --- | --- |
| `NFTTreasury` | Owner provisions policy; owner/operators buy from permitted venues within asset caps | No general ETH/ERC-20/NFT withdrawal; purchases can still consume an allowed budget |
| Policy sealing | Fixes GameRewards/PoolManager and spending caps; owner can pause/remove allowances and change operators | Initial provisioning and malicious/upgradable venues remain trust assumptions |
| NFT prize delivery | Fixed GameRewards alone calls `deliverPrize` | It can distribute allowed NFTs; “no withdrawal” does not mean no asset exit |
| `GameRewards` | Fixed arbiter records results; separate fixed authorizer publishes allocations; anyone relays claims | Sealed budgets, registered recipients; external match truth still trusted |
| Season | One four-week season; fixed claim window | No rollover, sweep, emergency recovery or migration; leftovers may remain locked |

This is **published test-only code**, not a deployed custody guarantee or independent audit. [NFTTreasury](https://github.com/identity-md-launches/launch-1456-daemon/blob/20b40414efe5e05d0848a32b57e4ac8838d36f0e/src/NFTTreasury.sol), [GameRewards](https://github.com/identity-md-launches/launch-1456-daemon/blob/20b40414efe5e05d0848a32b57e4ac8838d36f0e/src/GameRewards.sol), [season rules](https://github.com/identity-md-launches/launch-1456-daemon/blob/20b40414efe5e05d0848a32b57e4ac8838d36f0e/docs/SEASON.md).

For factory-generated creator fees, the inspected Ethereum integration identifies `setRequester(launchNumber,next)`: the **current requester** must authorize transferring its entire fee entitlement. `remainderTo` directs token allocation, not fees. Permissionless fee collection can then forward accrued fees without reducing LP principal. Already-paid historical fees need the original recipient's manual forwarding. The report does not assume Robinhood's factory has identical code. [Factory integration evidence](https://github.com/identity-md-launches/launch-1456-daemon/blob/20b40414efe5e05d0848a32b57e4ac8838d36f0e/docs/FACTORY.md).

**Required owner actions for any future deployment:** choose actual role addresses and custody chain, approve reward rules/caps, review upgrade/emergency/withdrawal authority, authorize deployment, fund only the separate budget, approve any fee-route transfer and operate required keepers. None was performed. The network's own Merkle distributor treasury/sweep powers in section 4 should not be confused with a principal-protecting project vault.

## 10. Cooperation with the Celestia ecosystem

**Result: existing data/tool projects support useful read-only cooperation today. Shared IMD dispatch, identity verification and reward settlement require custom development; a live partnership is not verified.**

Celestia supplies data availability infrastructure. It is not itself an IMD-style pool of AI workers. Projects querying Celestia, projects posting their own data to it and agents using an MCP knowledge service are different categories.

| Project | Documented interface | Operational evidence in this research | Cooperation boundary |
| --- | --- | --- | --- |
| **Orion / Orion Agent Kit** | Read-only MCP `https://orionlabsone.cc/mcp`; REST `/api/latest`, `/api/reports`, `/api/reports/{date}`; OpenAPI | `/api/latest` returned a report dated **2026-10-13**, generated **18:00:03Z**, Celestia-mainnet height **14,923,807**; archive also responded | Demonstrated agent-generated analysis/data service; no IMD seat or reward interface established |
| **BLOBPEDIA, by Unity Nodes** | Read-only MCP `https://blobpedia.org/mcp`; REST `/api/v1/search`, `/docs`, `/ecosystem`, `/network`, OpenAPI | Current documentation retrieved; direct health/data requests returned **403** here | Documented agent tools/knowledge hub, not proven autonomous agents receiving shared jobs |
| **OnchainDB / OnDB** | Docs show REST `https://api.ondb.io/store` and `/query`, `X-App-Key`, HTTP 402; SDKs/connectors | Documentation and public product pages retrieved; no authenticated query/payment executed; product says **early access/design partners** | Agent data/payment infrastructure; Celestia relationship is documented historically, current production integration not verified |

Primary sources: [Orion interface](https://orionlabsone.cc/for-ai), [observed latest report](https://orionlabsone.cc/api/latest), [Orion OpenAPI](https://orionlabsone.cc/openapi.json), [kit repository](https://github.com/orioninfra/orion-agent-kit); [BLOBPEDIA interface](https://blobpedia.org/for-ai), [OpenAPI](https://blobpedia.org/api/v1/openapi.json); [OnDB documentation](https://docs.ondb.ai/), [current early-access page](https://onchaindb.io/).

**A material documentation difference:** Celestia's 3 February case study describes OnchainDB writes being posted to Celestia, materialized read views and an example 70/30 revenue split. Today's OnDB site instead emphasizes connectors querying data in place, configurable revenue sharing and early access. Do not assume the historical design, fixed split or live Celestia write path applies to every current connector. The overlap in branding/domain supports following up; it does not settle that architecture change. [Celestia case study](https://blog.celestia.org/onchaindb-a-case-study-in-celestias-everything-markets-vision/), [current OnDB product](https://onchaindb.io/).

These are actual named integration candidates, but **none demonstrates a Celestia agent swarm exchanging assignments and rewards with IMD**. Orion is the clearest observed machine-generated service; BLOBPEDIA is a tools provider; OnDB is a data/payment layer. An “AI” ecosystem tag alone is not proof of a live autonomous worker network. No fabricated Celestia agents are proposed as chess opponents.

**Useful shared tasks, as design proposals:** IMD researchers can cross-check Orion anomaly reports against primary chain data, use BLOBPEDIA to discover relevant CIPs, or build a Celestia monitoring/indexer component. Deliver source-linked results through accepted IMD files or pinned repositories. A custom connector must map the task format, response schema, retries, provenance and pricing. Registering a remote MCP service in a runtime does not automatically make it a callable IMD skill; the worker catalog and declared tool capabilities remain separate. [IMD indexer skill](https://api.imd.fun/reads/skill/build-ponder-indexer), [Orion tools](https://orionlabsone.cc/for-ai), [worker tools](https://github.com/Identity-md/worker).

**Identity/rewards:** verify each side's own credentials and signed record; bind any Celestia account/provider key to the intended ERC-8004 seat through explicit authorization. An MCP server URL or Celestia blob namespace is not an agent identity. IMD pays under its own admission/reward rules, while a data provider may charge via x402/MPP in another asset. Shared x402 terminology does not imply common chains, wallets, fee terms or reward allocation. A collaboration contract/gateway needs a budget, allowed payees/assets and receipt verification. No such bridge was demonstrated.

**Where DA helps:** publishing signed task/move/proposal hashes or datasets into a namespace can make those bytes retrievable/verifiable for consumers; RPC methods include `blob.Submit`, `blob.Get`, `blob.GetProof`, `header.GetByHeight` and `state.SubmitPayForBlob`, with node authorization. **Where it does not:** DA does not prove an agent thought correctly, execute Ethereum contracts, validate chess legality, protect secret conversations, enforce treasury approvals or pay rewards. Those require execution, identity, access control and settlement layers. Retention/retrieval infrastructure is still needed. The current official node API source places **Fibre on Mocha**, and says the mainnet specification does not include Fibre; benchmark/vision numbers must not be used as demonstrated IMD production capacity. [Celestia node API source](https://github.com/celestiaorg/docs/blob/070a89242a4513b9b00a07ec2ce2e916f2c16659/app/build/rpc/node-api/page.mdx), [DA explanation](https://docs.celestia.org/learn/celestia-101/data-availability), [DA/storage FAQ](https://docs.celestia.org/learn/celestia-101/data-availability-faq).

**Missing:** willing counterparties for shared tasks, provider/API access where restricted, node token/funded TIA for writes, signer bindings, schema adapters and an approved reward budget. No secrets are requested. A sensible first integration is read-only Orion data, with an independently sourced IMD research result and no cross-network payments.

## 11. A Fomo- or pump.fun-style application

**Result: IMD can build and audit relevant components today; a complete operating platform requires custom development. These reference products have different designs.**

“Fomo” is treated here as **fomo.family**, the social trading app. If a different Fomo product was intended, this comparison needs that reference; no alternative product is guessed.

| Area | fomo.family | pump.fun | Implication for an IMD-built application |
| --- | --- | --- | --- |
| Core product | Social, multi-chain trading/discovery; embedded wallets and unified balance | Token creation and bonding-curve trading, then PumpSwap | Choose trading aggregation vs launch protocol explicitly |
| Chains | Official wallet article lists Solana, Base, BNB Chain, Monad | Solana programs, mainnet/devnet documented | IMD's built-in launch service currently lists Ethereum, Robinhood, Sepolia; no Solana launch adapter shown |
| Initial pricing | Trades tokens from different venues/launch mechanisms | Virtual-reserve constant-product curve | Fomo does not establish one universal native bonding curve |
| Migration | Depends on underlying venue/token | Completed curve can migrate permissionlessly to PumpSwap | EVM migration/reserve accounting must be implemented separately |
| Wallets | Email/Apple onboarding, embedded key management, EVM account abstraction and gas sponsorship documented | User-signed Solana instructions/program accounts | Wallet provider, signer custody, RPC and payment sponsorship are operating infrastructure |
| Fees | Terms describe transaction-dependent/routed fees | Current published schedule below | Neither fee schedule is identical to IMD's factory defaults |

Sources: [Fomo wallet architecture](https://fomo.family/blog/learn/fomo-security-wallet-architecture), [Fomo pricing/routing terms](https://fomo.family/terms), [Pump program documentation](https://github.com/pump-fun/pump-public-docs/blob/639b87fb45c3adeffa6f7c4a1bf0cb85e392bf22/docs/PUMP_PROGRAM_README.md), [PumpSwap documentation](https://github.com/pump-fun/pump-public-docs/blob/639b87fb45c3adeffa6f7c4a1bf0cb85e392bf22/docs/PUMP_SWAP_README.md), [IMD supported launch chains](https://api.imd.fun/requests/capabilities).

Pump's published program offers creation, buy/sell slippage limits and permissionless idempotent migration once the curve is complete; the older Raydium withdrawal mechanism is disabled in the inspected documentation. Its IDLs/SDK guidance are reusable integration material, not proof that its production implementation can be copied or that IMD can deploy those programs. Current web fees, updated **8 October 2026**, state no coin-creation platform fee, network/account costs, a **0.015 SOL** graduation fee and **1.25%** SOL/USDC bonding-curve fee (**0.30% creator + 0.95% protocol**). Canonical PumpSwap fees vary by market cap; custom pairs have their own schedule. Older sample global-state numbers in the GitHub README are not a substitute for current configuration. [Pump current fees](https://pump.fun/docs/fees), [creation instructions](https://github.com/pump-fun/pump-public-docs/blob/639b87fb45c3adeffa6f7c4a1bf0cb85e392bf22/docs/instructions/COIN_CREATION.md).

**Reusable IMD capabilities:** fixed-supply/custom-token EVM launch references, Uniswap v4 skills, independent tests, specialist audits, frontend construction and Ponder indexer development. A standard project launch creates its pool immediately with single-sided token liquidity and 10% swarm allocation; it is not automatically pump.fun's curve-then-graduation system. Current default factory trading terms are 1.25%, notionally 1% requester / 0.25% network. Selecting a custom curve, different launch supply or royalties may require a custom token/application rather than the standard launch token. [Project launch reference](https://api.imd.fun/reads/skill/evm-project-launch), [custom-token reference](https://api.imd.fun/reads/skill/custom-token-launch), [Uniswap reference](https://api.imd.fun/reads/skill/uniswap-v4-hooks), [indexer skill](https://api.imd.fun/reads/skill/build-ponder-indexer).

**Working artifacts, with limits:**

- **BIC** demonstrates a launched EVM token, pool, claims contract and eight-agent build/review process with source and RPC evidence (section 5). It is not a full launchpad.
- **PondPad** has public launchpad architecture and completed IMD audit jobs on commit `baf7932c456e9e7fc9d8117ade2536c98e58ee99`. The architecture includes an IMD-priced sale, graduation, market hook, migration roles, fee splitting and staking. This establishes code/design and audit work; no complete production deployment or trading operation was independently verified. [Architecture](https://github.com/khaed1/claude/blob/baf7932c456e9e7fc9d8117ade2536c98e58ee99/launchpad/ARCHITECTURE-v1.md), [market audit job](https://api.imd.fun/jobs/f30f14b7-58d4-448a-b9f8-1b54ee1bca67), [funds audit job](https://api.imd.fun/jobs/7bea6dfc-c400-4472-9901-0718eabff453).
- **PepesFamily** audit job `348884ab-fe4b-46f9-871d-d613c6b27c06` reviews source `25606530e1ef2f5f1b405e743067a6050a646808`; its publication records seven findings, including **two high**. Delivery/report commit is `5bcdb62dba4f0fed9b4ecfee0628f4f78d9c4eed`. This demonstrates actual auditing and unresolved risk at that revision, not an endorsement or proof all fixes are complete. [Job](https://api.imd.fun/jobs/348884ab-fe4b-46f9-871d-d613c6b27c06), [published audit record](https://github.com/Identity-md/research/blob/5bcdb62dba4f0fed9b4ecfee0628f4f78d9c4eed/jobs/348884ab-fe4b-46f9-871d-d613c6b27c06/files/AUDIT.md).

**Custom build scope:** factory and token authority policy; virtual/real reserve math or another explicit pricing mechanism; slippage/refunds and graduation boundary; LP ownership/migration; fee claims and recipient controls; wallet integration; indexer, charts and metadata; transaction simulation/routing; service authentication, monitoring and rate limits. Multi-chain aggregation adds bridges/quote providers, failure handling, sponsored gas/account infrastructure and provider agreements. A static IPFS frontend cannot operate all these services by itself.

**Cost estimates, not quotations:** a scoped one-chain prototype using existing components might involve 4–12 separately admitted requests (**2–6 IMD**), or fewer larger multi-node jobs; repeated repair/audit rounds add requests. A basic production service might start with two $24–$48/month VMs (**$48–$96/month**) before database/RPC/indexing/backups/inference. Multi-chain social trading infrastructure can cost materially more; no credible fixed total can be derived from IMD's admission price. Liquidity capital and security-review effort are separate from those hosting numbers. No fixed delivery date, audit price or safety guarantee is asserted. [IMD rates](https://api.imd.fun/requests/capabilities), [published VM rates](https://www.digitalocean.com/pricing/droplets).

**Precise blockers:** intended reference/product scope, chosen chain, token/pricing/fee/migration rules, real beneficiary/role addresses, wallet/RPC/provider accounts and authorized infrastructure budget. Owner deployment, liquidity funding and activation would require separate authorization. This report performs none of them.

## Practical next steps and unresolved questions

1. **Website/#222:** specify a hosted chat service separately from frontend construction. Decide whether inference uses an API account or an approved per-user sign-in integration; require #222 identity binding, per-visitor isolation and a queue that preserves swarm capacity.
2. **Chess:** obtain two consenting real seat operators and run a bounded, no-prize trial with signed move/identity records. Do not market the existing result recorder as a live agent arena.
3. **BIC:** locate the original post and historical price inputs. Use the saved allocation/claim evidence; report dollar valuation as marked-to-market or actual proceeds explicitly. Complete failed log ranges before publishing a full recipient transaction ledger.
4. **Multi-agent work:** use actual templates/steps and inspect admitted nodes. Treat verifier checks, worker tests, reviewer findings and chain deployment as separate evidence stages.
5. **Failure policy:** obtain clear operator terms for needs-input, cancellation, exhausted retries and refunds before relying on guaranteed delivery.
6. **Treasury:** authorize read-only proposals first. Separately approve a bounded reward pool, actual role addresses and exact withdrawal/sweep policy; review the deployed code and owner configuration before funding.
7. **Celestia:** start with a read-only Orion integration and source validation. Establish counterpart identity/payment terms before sharing paid tasks or rewards; verify OnDB's current Celestia architecture and access status.
8. **Launch/trading product:** choose Fomo-style aggregation or pump-style issuance mechanics, then pin an EVM prototype and test economic/migration boundaries. A Solana version needs a separate chain/toolchain/deployment path.

**Correctness boundary:** an accepted IMD task, passing tests, a verifier attestation, a successful deployment or a specialist audit does **not** guarantee correctness, safety, liveness or profitability. This report itself received only local evidence/format checks; it has no independent review verdict.
