# IdentityMD Hackathon Entries — How Each Project Uses IMD

**Question:** Research the listed IdentityMD (IMD) hackathon entries and how each uses IMD.

**Date of research:** 2026-10-28

## Method and evidence grades

Each finding below is tagged with its evidence:

- **[ENTRY]** — the project's own text on the official entry form. Self-reported by the entrant; attributable but not independent.
- **[CHAIN]** — checked independently against Ethereum mainnet and Robinhood Chain via archive reads (`eth_call` `name()`/`symbol()`, contract-code probing, ERC-20 `Transfer` log scans).
- **[SITE]** — the project's own site, fetched live on 2026-10-28.
- **[3P]** — third-party source (DexScreener, Nitter/X mirror, published audit).

**Primary source for the entry list:** the frozen entries file behind the official entry page at `imdradar.site/hackathon` — `https://www.imdradar.site/data/hackathon-entries.json` (78 entries, frozen after the 2026-10-21 23:59 UTC deadline; the page's own JS confirms it serves this static file post-deadline). All 15 handles in the brief are present in it.

## Background (verified)

- IMD (IdentityMD) is "a network to create net new 0 to 1 billion financial applications, a consensus layer managed by distributed agents that pairs itself … with smart contracts and blockchains" — [3P] `imd.fun/docs/llms.txt`.
- The official IMD token on Ethereum mainnet is `0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7`; on Robinhood Chain IMD is `0x5F7Bb59365ce557C26dbcAa4EE9d39A4b95B7127` — [3P] imd.fun docs and the published SOVRN.ONE audit (`api.imd.fun/jobs/165186a0-9696-443d-8524-caca2ea94b45/report.md`).
- The event is the **first Identity MD Hackathon**, community-funded and organised ($10,000–$15,000+ reported prize pool), submissions 7–21 Oct 2026, judged by IMD agents (places 6–15) and a human jury (top 5) — [3P] imdradar.site/hackathon and the organiser's announcement mirrored on nitter (`nitter.cf/surfcoderepeat/status/2107939454396567581`).
- Entry rules required building "through the IMD protocol: a Uniswap v4 hook or a custom contract that really uses IMD," launching via `explorer.imd.fun/launch`, a dedicated X account, and submission through IMD Radar — [3P] same sources.
- Paying IMD to the network opens work: `job.open`, `launch.open`, `oracle.request` etc. are priced at **0.5 IMD** per action — [3P] `imd.fun/docs/llms.txt`. This matches the 0.5-IMD-per-question figures cited by several entries.

**Recurring IMD-usage patterns across the 15 entries:** (a) token launched through `explorer.imd.fun/launch` and paired with IMD in a Uniswap v4 pool; (b) IMD oracle panels (`oracle.request`, ~0.5 IMD/question) settling markets or attesting facts, often paid on-chain via the "IMD Intake" contract; (c) IMD as the unit of account (stakes, mint prices, fees, bonds); (d) IMD burned via the "BurnExecutor"; (e) the swarm itself building/auditing the code. Items (d) and (e) are self-reported except where noted.

---

## The 15 entries

### 1. swornbyswarm — "Sworn" wallet-fact registry (Ethereum)
Submitted 2026-10-21 22:49 UTC by @cryptokarlheinz. Contract `0x0da2679000ea5380d1361cc3cca7d4e8c881f766`. [ENTRY]

- **What:** an ownerless Ethereum registry of 25 facts about 19,522 wallets (`WhitelistCurator.sol`); an ERC-721 "card" (0.1 IMD to mint) shows a wallet's facts; other contracts can gate on `hasTrait(wallet, id)`. [ENTRY]
- **IMD usage:** IMD is the fee currency — 0.1 IMD per card, 0.5 IMD per oracle fact (one IMD oracle request each), 6.9 IMD to add a community spec with its first claim; card/spec fees go to the IMD BurnExecutor for bridging/burning on Base. Built in one swarm "workflow" (launch #2404). [ENTRY]
- **Checked:** contract exists and `name()="Sworn"`, `symbol()="SWORN"` — consistent with the ERC-721 card. [CHAIN] Site `swornbyswarm.sites.imd.fun` live; linked GitHub repo and explorer.imd.fun job page both return 200. [SITE]

### 2. Imdirectorb — "IMDirector" device-control gateway (Robinhood)
Submitted 2026-10-21 21:53 UTC by @DmitryiBond. Contract `0xecb5e7f3b9839eb083dda95099b8438ecebec16e`. [ENTRY]

- **What:** infrastructure connecting the IMD token to physical devices — a gateway turns IMD transfers and contract events into on/off commands for appliances; a live show is planned where viewers use IMD to control lights. [ENTRY]
- **IMD usage:** IMDirector token plus a Uniswap v4 hook for the Director/IMD pool on Robinhood; buys/sells are linked to switching a device. Built through an IMD job (`explorer.imd.fun/jobs/432eeaaf-…`, page live). [ENTRY][SITE]
- **Checked:** contract verified on Robinhood — `name()="IMDirector"`, `symbol()="Director"`. [CHAIN] `imdirector.live` and `imdirector.live/docs.html` live; demo linked to an X status. [SITE]

### 3. tungweb3 — "EmberEVO" / Ember World (Ethereum)
Submitted 2026-10-21 15:29 UTC. Contract `0x2b82cdeb8477415d541799abb0cc48044c8ea5f3`; deployer `0xff03410d0fe5fa8f7f59f743de35e333d9857120`. [ENTRY]

- **What:** EmberEVO, an "IMD-inspired" ecosystem around Ember World (`imdember.com`), an explorable 3D social town; planned staking of $EMBEO, off-chain GOLD credits usable for AI-market research, Genesis NFTs and multiplayer games. [ENTRY]
- **IMD usage:** the entry states only "we use IMD Swarm for code reviews and security audits." No IMD payment, oracle, pairing or contract-level use is claimed. This is the **lightest IMD integration** among entries that shipped a contract. [ENTRY — self-reported]
- **Checked:** token verified on Ethereum — `name()="EmberEVO"`, `symbol()="EMBEO"`. [CHAIN] `imdember.com` live (a WebGL world boot page). [SITE]

### 4. inkandinference — "Ink & Inference" portraits + INK (Ethereum)
Submitted 2026-10-21 15:29 UTC by @edugrooves. Router `0x45d4cd12ced01d4316a6021387cfdee2fd9491a7`. [ENTRY]

- **What:** 2,000 generative portraits (one per identity.md seat) plus an INK token on a Uniswap v4 hook pool paired with IMD (1.25% fee, launch 2321). The entered contract, InkFeeRouter, receives the launch's trading-fee share; `claimAndRoute()` sends IMD to the treasury and adds INK as liquidity. [ENTRY]
- **IMD usage:** IMD pair on the v4 pool; IMD-denominated fee flow routed on-chain; five separate swarm jobs cited (audit, Sepolia, contracts, hook, site). [ENTRY]
- **Checked:** INK token verified (`name/symbol "INK"`); Portraits NFT verified (`"Ink & Inference"/"INKINF"`); the InkFeeRouter address holds code (reverts `name()` as expected for a non-token). [CHAIN] Site live. [SITE]

### 5. moneycanbuy_fun — "moneycanbuy.fun" paid-dare board (Ethereum)
Submitted 2026-10-21 14:56 UTC. Contract `0x49e55a87aa4bb0d2fd58fdcf1a31c9612de015dc` (this is the $YOLO token); deployer `0xff03…7120`. [ENTRY]

- **What:** a board of paid yes/no dares. Posters escrow rewards in ETH/USDC/IMD/YOLO; doers submit public proof; a 24 h dispute window precedes payout. [ENTRY]
- **IMD usage:** every appeal is a paid IMD oracle job (0.5 IMD/question) whose EIP-712 verdict moves the money; doer and dispute bonds carry 0.5 IMD; rewards payable in IMD; $YOLO paired with IMD (swarm launch #2364); identity.md NFT holders act as a first court, 1 NFT = 1 vote. [ENTRY]
- **Checked:** YOLO token verified on Ethereum (`name/symbol "YOLO"`). [CHAIN] Site and GitHub repo live. [SITE] **Caveat:** the entry itself admits "core contracts deploy via the IMD swarm: slower than planned, almost done" — the full system may not have been deployed by the deadline. [ENTRY]

### 6. theimddaily — "The IMD Daily" newspaper (Ethereum, no contract on file)
Submitted 2026-10-21 12:03 UTC by @kilicsln. No contract in the entry. [ENTRY]

- **What:** a free newspaper and collectible history of the IMD ecosystem — PDF reading, searchable archive, and ERC-1155 editions. [ENTRY]
- **IMD usage:** each issue collectable for **0.1 IMD** during a contract-enforced 24 h window, then minting closes permanently; payments go to a dedicated on-chain vault; publisher dashboard with wallet login and content-hash verification. Described as giving "IMD a practical use beyond trading." [ENTRY]
- **Checked:** site `the-imd-daily-free-to-read-colle.sites.imd.fun` live (JS-rendered shell confirmed). [SITE] Claims of being "live on Ethereum" not independently verified — no contract address was submitted. [unverified]

### 7. imdgenesis — "GENESIS" experiment-lab game (Ethereum)
Submitted 2026-10-21 06:41 UTC by @0maxxdev. Contract `0x06f8ceff95e5d72887c575d2759e36230b711d06` (GenesisResearch); deployer `0xff03…7120`. [ENTRY]

- **What:** a playable laboratory where players spend a limited experiment budget to infer the rules of a synthetic ecosystem; an optional IMD agent can assess a hypothesis and choose the next experiment. [ENTRY]
- **IMD usage:** one preserved paid IMD cycle — hypothesis → IMD proposal → hash-checked artefact → engine experiment → public journal; GenesisResearch deployed through IMD launch #2322. [ENTRY]
- **Checked:** contract code exists on Ethereum (non-token; reverts `name()`). [CHAIN] `imdgenesis.xyz`, `/judges` and `/replay` live. [SITE]

### 8. SeerOnIMD — "Seer" swarm-judged prediction markets (Robinhood **testnet**)
Submitted 2026-10-20 15:57 UTC by @danieltang. No contract in the contract field; three adjudicator addresses listed in text. [ENTRY]

- **What:** prediction markets judged by the IMD swarm: a question becomes a market; after its deadline an IMD oracle panel answers and the signed outcome settles the market on-chain. Includes agent question-acceptance, up-to-9-agent forecast panels that set opening prices, 9-agent question "discovery," and post-settlement Brier/peer scoring with a leaderboard. [ENTRY]
- **IMD usage:** every step is paid in IMD from the user's wallet ("0.5 IMD per agent step" per the site); the app pays IMD to the IMD Intake on Robinhood at `0xa43e6f75ee006411f79ac1c84120606c2330de82`. [ENTRY][SITE]
- **Checked:** `seer.zone` and `app.seer.zone` live and describe the same three use cases, all marked "live on testnet." [SITE] The listed contracts are on Robinhood **testnet**, so they could not be confirmed with mainnet-chain reads. [unverified]

### 9. ConditionalsImd — "Conditionals" conditional prediction markets (Robinhood)
Submitted 2026-10-20 14:32 UTC by @0xmisturi. Contract `0xc8cc656b71dd77ae1e29b0bc7890edd110e73255`. [ENTRY]

- **What:** markets of the form "if X happens, will Y?" — each opens two worlds (X happens / X doesn't), each with YES/NO pools; comparing prices isolates X's effect on Y. [ENTRY]
- **IMD usage:** the IMD oracle settles every market — the contract pays the Intake for two questions (condition and outcome) and verifies the panel's signed answers on-chain; IMD is the only currency (stakes, payouts, deposits, oracle fees); 2% of every settled pot is burned; built/audited/deployed by the swarm (launch 2278); claimed no admin/pause/upgrade. [ENTRY]
- **Checked:** contract code exists on Robinhood. [CHAIN] Remaining mechanics are self-reported. [ENTRY]

### 10. hamsterhourgame — "Hamster Hour" hourly betting game (Ethereum)
Submitted 2026-10-20 08:31 UTC. Contract `0xe33ab493249a2df0d8c4a71ac54f46d1f7778367`; deployer `0xff03…7120`. [ENTRY]

- **What:** bets on how far a real hamster runs each hour — OVER/UNDER, SNOOZE, and an EXACT jackpot (5 IMD ticket). Pari-mutuel, claimed ownerless; 5% to stakers, 2% to jackpot, 1% to oracle. [ENTRY]
- **IMD usage:** every bet is in IMD; each hour is settled by an IMD oracle panel; the contract buys its own oracle requests through IMD Intake (no backend); review, contracts (3 audit rounds), site and an agent skill all swarm-built. [ENTRY]
- **Checked:** contract exists on Ethereum. An ERC-20 `Transfer` scan of official IMD (`0xd34a…63b7`) over the last ~100 k blocks found **22 transfers involving the contract** — bets in, payouts out — including an outgoing transfer of exactly **0.5 IMD**, matching the stated per-request oracle price. This independently corroborates live IMD-denominated activity. [CHAIN] `hamsterhour.fun` live. [SITE] Whether the wheel data is a real running hamster is not verifiable on-chain. [unverified]

### 11. chad_gotchi — "OG Club World" NFT social world (no contract on file)
Submitted 2026-10-19 07:54 UTC. No contract, no chain listed. [ENTRY]

- **What:** a pixel-art browser world where NFTs you hold (Swarm Pepe, FrenPet, Aavegotchi incl. borrowed) are your character and pass; free to look around as a guest. [ENTRY]
- **IMD usage:** the entry text states **no direct IMD integration**. The connection is community-level: it serves the Swarm Pepe / OG Club community (Swarm Pepes being, per their own entry, "the first NFT collection powered by a Uniswap v4 hook built by the $IMD swarm"). The site additionally mentions burning a "$SWARM" token to build in-world — a different token, not IMD. [ENTRY][SITE]
- **Checked:** `world.ogclub.online` live and matches the description. [SITE] **Unanswered:** whether the project qualifies under the "really uses IMD" rule is a judging question, not resolvable from the entry.

### 12. marginalia_md — "Marginalia" bonded trade theses (Ethereum)
Submitted 2026-10-12 01:39 UTC. Contract `0xf0457dd0cf526686190e4f057ba19db14d34a0cc` (the v4 hook); deployer `0x12c6…a96f` (the same address that deployed other swarm launches, e.g. Pixel_Pool, swarmpepes, Musefren — consistent with "deployed by the IMD factory"). [ENTRY]

- **What:** "notes in the margin of every trade" — buying MARG through the router with a note attached posts a bonded call (side, target, deadline) on any token; the chain settles it from permissionless observations; right returns the bond, wrong forfeits it to writers' pools. Explicitly "not a perp DEX, not a prediction market." [ENTRY]
- **IMD usage:** hook paired with IMD on Ethereum (launch #1283); weekly ranking of theses by an **IMD oracle panel** on reasoning and citations (never outcome), paid from the pools; sealed notes for the author's key holders; handle claims in the key market attested by the IMD oracle. Tokenomics: 85% to pool, 10% to the swarm, deployer's 5% burned. [ENTRY]
- **Checked:** contract code exists on Ethereum. [CHAIN]

### 13. pinkybond_fun — "Pinky" bonded no-dump promises (Robinhood)
Submitted 2026-10-10 06:25 UTC by @hexysdev. Token `0xb125c461c00863aacad4cc99311d2f23d4342a6f`; PinkyVault `0x3c81384aa1ca064316576a214e2fb30969992772`. [ENTRY]

- **What:** a deployer bonds IMD behind the promise "my wallet won't move more than N of this token before the deadline." At expiry, PinkyVault pays the IdentityMD oracle on-chain, out of the bond, to sum the wallet's transfers over the exact block range; within the limit the bond returns, over it 10% goes to the first watcher and the rest is split between PINKY stakers and a burn. [ENTRY]
- **IMD usage:** "IMD is the bond, the oracle fee and the pair"; built from the team's repo, then audited/fixed/deployed by the swarm (launch #1166, Robinhood). [ENTRY]
- **Checked:** PINKY token verified on Robinhood (`name="Pinky"`, `symbol="PINKY"`); PinkyVault holds code. [CHAIN] Site and GitHub repo live. [SITE] **Caveat:** a ~300 k-block scan of Robinhood IMD `Transfer` logs found no transfers to the vault, so the claim "first promise already settled on chain" is unconfirmed — the settlement may predate the scanned window or use a path that doesn't emit the scanned event. [CHAIN — inconclusive]

### 14. SovrnIMD — "SOVRN.ONE" / Solomon voice agent (Robinhood)
Submitted 2026-10-09 22:41 UTC. Contract `0x7f7e9b8e9f754c3076e514852552019cb571461b`. [ENTRY]

- **What:** the entry text is pure lore for "Solomon," an AI voice agent; the mechanics come from the project's site and its published swarm audit. [ENTRY][SITE][3P]
- **IMD usage:** SVO launched through the IMD launchpad — 80% of the fixed 1 B supply into a **SVO/IMD Uniswap v4 pool**, 10% swarm allocation, 10% operations. Every trading fee is paid **in IMD** to an immutable `LifeForceVault`: 70% funds Solomon's operation, 30% SVO buybacks; overflow IMD streams to SVO stakers. Contracts audited by the IMD swarm (full audit report public at `api.imd.fun/jobs/165186a0-…/report.md`). [SITE][3P]
- **Checked:** token verified on Robinhood — `name()="SOVRN.ONE"`, `symbol()="SVO"`. [CHAIN] DexScreener shows a live SVO/IMD v4 pair (~$15 K liquidity, ~$20 K mcap at fetch time). [3P] `sovrn.one` live, including an on-chain accounting page. [SITE]

### 15. NightShiftImd — "NIGHTSHIFT" agent-economy company (Ethereum)
Submitted 2026-10-19 20:16 UTC by @probert_mihai (entry handle filed as `nightshiftimd`). Contract `0xe5e58e53d0bb204aa62c995a6c8cc8a48e60c3ac`; deployer `0x12c6…a96f` (IMD factory). [ENTRY]

- **What:** an "AI company" stack that buys products, sites and audits from the swarm in IMD and sells for USDC: $SHIFT (launch #2124, v4 hook), 500 on-chain NIGHT FROGS, GameEscrow (real-money chess/pinball), BetPool, and an Agent Arena where ERC-8004 agents and IMD seats play for Elo. [ENTRY]
- **IMD usage:** v4-hook fees burn IMD at the BurnExecutor; 10% to the swarm; agent discovery via `agents.md`, MCP and x402 so external agents can find, register, play, sell and hire the swarm with every job settling in IMD; IMD seats get first-class profiles; claims to have reported IMD Intake/RPC outages and to be building an IMD watchtower/SDK. [ENTRY]
- **Checked:** SHIFT token verified on Ethereum (`name()="NIGHTSHIFT"`, `symbol()="SHIFT"`). [CHAIN] GitHub repo live. [SITE]

---

## Summary table

| # | Handle | Project | Chain | Contract verified? | Core IMD usage |
|---|--------|---------|-------|--------------------|----------------|
| 1 | swornbyswarm | Sworn wallet-fact registry + NFT card | ETH | Yes — SWORN NFT | IMD mint/fact/spec fees; IMD oracle facts; BurnExecutor |
| 2 | Imdirectorb | IMD→device gateway | RH | Yes — Director token | Director/IMD v4 hook drives physical devices |
| 3 | tungweb3 | EmberEVO / Ember World | ETH | Yes — EMBEO | Swarm audits only (weakest stated use) |
| 4 | inkandinference | Ink & Inference + INK | ETH | Yes — INK + INKINF + router code | INK/IMD v4 pool; IMD fee routing |
| 5 | moneycanbuy_fun | Paid-dare board | ETH | Yes — YOLO | IMD oracle appeals; IMD bonds/rewards; YOLO/IMD pair |
| 6 | theimddaily | IMD Daily newspaper | ETH | No contract filed | 0.1 IMD collectible editions; IMD vault |
| 7 | imdgenesis | GENESIS lab game | ETH | Code present | Paid IMD hypothesis→experiment cycle |
| 8 | SeerOnIMD | Seer prediction markets | RH testnet | Not checkable (testnet) | IMD-paid agent panels settle/price/discover markets |
| 9 | ConditionalsImd | Conditional markets | RH | Code present | IMD-only currency; IMD oracle settlement; 2% burn |
| 10 | hamsterhourgame | Hamster racing bets | ETH | Code present + live IMD flows | IMD bets; IMD Intake-bought oracle settlement |
| 11 | chad_gotchi | OG Club World | — | None filed | Community tie-in only; no stated direct use |
| 12 | marginalia_md | Marginalia bonded theses | ETH | Code present (hook) | MARG/IMD v4 hook; IMD oracle ranks theses, attests claims |
| 13 | pinkybond_fun | Pinky bonded promises | RH | Yes — PINKY + vault code | IMD bond + oracle fee + pair; oracle sums transfers |
| 14 | SovrnIMD | SOVRN.ONE / Solomon | RH | Yes — SVO | SVO/IMD v4 pool; IMD fees to vault, streamed to stakers |
| 15 | NightShiftImd | NIGHTSHIFT agent economy | ETH | Yes — SHIFT | IMD-fee-burning hook; every job settles in IMD; x402/MCP |

## Facts, inferences, uncertainty

**Established facts (independently checked):**
- All 15 handles appear in the official frozen entry list (78 entries total) with the submission times, chains, and contract addresses cited above. [ENTRY file]
- Every submitted contract address that was checked holds code on the claimed chain; all token contracts return the names/symbols matching the projects. [CHAIN]
- The Hamster Hour contract has real IMD transfers in both directions within the last ~100 k Ethereum blocks, including an exact 0.5 IMD outgoing payment consistent with the documented oracle-request price. [CHAIN]
- All cited project sites returned HTTP 200 on 2026-10-28; the Sovrn audit report and all four linked GitHub repos resolve. [SITE]
- Two deployer addresses recur across entries — `0xff03410d…7120` (tungweb3, moneycanbuy_fun, imdgenesis, hamsterhourgame) and `0x12c63b58…a96f` (marginalia_md, NightShiftImd, plus other entries like Pixel_Pool, swarmpepes, Musefren). Several entries state the IMD factory deployed their contracts, consistent with shared deployer addresses. [ENTRY][CHAIN]

**Inferences (reasoned, not directly proven):**
- The exact-0.5-IMD outgoing transfer from Hamster Hour is likely an oracle-request fee, matching the documented price — but the counterparty's role was not independently confirmed.
- Non-token contracts that revert `name()` were treated as deployed code because an EOA returns `0x` rather than reverting; this proves code exists, not that it implements the described logic.
- "Deployed by the IMD factory" is inferred from shared deployer addresses plus entry statements, not from factory records.

**Uncertainty / self-reported only:**
- All mechanism descriptions (oracle panels settling markets, fee splits, burn paths, "no admin") come from entrants' own text and sites; except where noted, the contract internals were not audited here.
- Pinky's claim that a first promise already settled on-chain was not confirmed by the scanned transfer window.
- The IMD Daily's claimed Ethereum contracts could not be checked (no address filed).
- Seer's contracts are on Robinhood **testnet**; mainnet tooling cannot confirm them.
- Whether OG Club World (chad_gotchi) and EmberEVO (tungweb3) satisfy the "really uses IMD" entry rule is unclear — their entries assert community ties and swarm audits rather than on-chain IMD mechanics.

**Unanswered questions:**
- Final judging results/prizes: the hackathon page still shows "judges are reviewing them all" as of the fetch; winners were to be announced ~23 Oct but were not located.
- Whether Hamster Hour's wheel data is generated by a real animal.
- The identity of recurring deployer addresses (factory vs. shared entrant wallets) beyond entries' own statements.
- Whether any entries were disqualified or removed post-freeze; the static file reflects the state at deadline.

## Sources

- `https://www.imdradar.site/hackathon` and `https://www.imdradar.site/data/hackathon-entries.json` (frozen entry list)
- `https://imd.fun/docs/llms.txt` (IMD protocol actions/pricing; official mainnet token)
- `https://nitter.cf/surfcoderepeat/status/2107939454396567581` (organiser announcement)
- `https://api.imd.fun/jobs/165186a0-9696-443d-8524-caca2ea94b45/report.md` (SOVRN.ONE swarm audit; Robinhood IMD address)
- `https://dexscreener.com/robinhood/0x9e585c98778fe782fdeae2662751900407f15696b69ff6156dfa40d53a1de46a` (SVO/IMD pair)
- Project sites: swornbyswarm.sites.imd.fun, imdirector.live, imdember.com, ink-and-inference.sites.imd.fun, moneycanbuy.fun, the-imd-daily-free-to-read-colle.sites.imd.fun, imdgenesis.xyz, seer.zone / app.seer.zone, hamsterhour.fun, world.ogclub.online, pinkybond.fun, sovrn.one
- On-chain reads: Ethereum mainnet and Robinhood Chain via archive RPC (name/symbol calls, code-existence probes, IMD ERC-20 `Transfer` scans) executed 2026-10-28.
