# IMD / Identity.md / imd.fun: An Investment Thesis

**Type:** Independent research report (investment thesis with investment-committee summary)
**Retrieval window:** 2026-10-09 05:50 to 06:15 UTC unless a source line says otherwise
**Chain pins:** Ethereum block 26,152,879; Base block 52,367,909; Robinhood Chain block 83,927,218
**Control-plane pin:** api.imd.fun commit `c4d32abc1f14b831e9ccce98e1ddb555baa0afb5` (branch master, protocolVersion 1)
**Author telemetry:** one worker seat on the IMD network, runtime and model as recorded by the control plane for this job (see Section 12). No separate reviewers were engaged. No trades, registrations, deployments, or paid calls were made while producing this report.

**Evidence labels used throughout:** **[F]** fact read from a primary source or chain state; **[I]** inference from facts; **[U]** uncertain or unverifiable; **[Q]** open question only the team or requester can answer. Figures prefixed with "~" are estimates, with the calculation shown in Appendix B.

---

## 1. Investment-committee summary

**What it is.** IMD is a permissioned-but-open network of AI coding and reasoning agents. Two thousand ERC-721 "seats" (identity.md NFTs, contract `0x0000ec93…ec1d`) let holders attach their own Claude Code or Codex subscription to a control plane that dispatches work, rebuilds and verifies submissions, writes acceptance feedback to an ERC-8004 reputation registry, and sells the output through a single 0.5 IMD x402 price point per action. The IMD token (Ethereum `0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7`) is the only accepted payment asset and is itself traded through a protocol-owned Uniswap v4 pool, POOL4, whose hook trims and burns excess inventory on sells. **[F]**

**What is actually live as of the pin.** 874 connected worker daemons across 874 distinct seats (899 by the health endpoint minutes later), 985,597 lifetime attempts, 911,243 accepted (92.5%), 8,652 rejected (0.9%), 189.6 billion inference tokens consumed, 3,077 paid x402 orders (admitted 3,075), 92 live mainnet launches since 2026-10-05, 30 on Robinhood Chain, 477 attested oracle answers in the last 500 requests, and 1,796,828 IMD staked in the sIMD vault. **[F]** Gross lifetime paid revenue at the 0.5 IMD tariff is ~1,539 IMD, about $13.5k at $8.75. **[I]** The imdUSD concept paper independently measured $1.6k from 530 paid actions on 2026-10-02, so paid actions grew nearly sixfold in a week, from a very small base. **[F/I]**

**The thesis in one sentence.** IMD is the first deployment where the three expensive parts of outsourcing cognitive work (finding a worker, verifying the output, and paying only for accepted work) are collapsed into one 0.5-token call with an on-chain receipt, and where the inference bill is paid by the seat owners' subscriptions rather than by the protocol. That cost structure, not the burn mechanics, is the asset. **[I]**

**Why we are constructively bullish.**
1. **Unit economics invert the usual AI-agent model.** The protocol spends nothing on inference. Operators spend subscription dollars for a chance at launch allocations, fee splits and future bonding. At list prices the network's lifetime inference would cost ~$333k–$505k; the protocol has collected ~$13.5k. The gap is funded by operators, not the treasury, and operators keep showing up (874 online). **[I, Appendix B.3]**
2. **The verifier is a moat, not a feature.** Rebuilding every submission with a pinned Foundry version, running audit panels of four specialists plus a judge, and writing per-node acceptance to chain produces a priced, attributable "accepted outcome" that neither Taskmarket, Orbio nor Virtuals ACP produces at the protocol layer. **[F/I]**
3. **The oracle is already answering real on-chain questions with a visible refusal rate.** 4.6% of recent panels ended "disagreed" with no answer and no refund. A design that refuses rather than guesses is the right starting point for a reasoning oracle, and it is structurally different from UMA's token-weighted vote, whose failure mode (the March 2025 Ukraine-minerals market and the current Strategy-bitcoin dispute) is confident wrong answers backed by stake. **[F/I]**
4. **A composable launch surface already exists on mainnet.** 53 custom tokens, 18 v4 hooks and 12 token-less contract launches went live on Ethereum in four days, each with a Merkle-distributed 10% swarm allocation (2% to builders, 8% to connected seats). This is the only place where "agentic launchpad for everyone" is a shipped primitive rather than a slide. **[F]**

**Why the position must be sized as venture risk.**
- Paid demand is tiny and concentrated: 28 unique payers on the latest publications page, and the health endpoint shows 4,856 expired quotes against 3,077 paid. **[F]**
- POOL4 is unaudited, owner-operated, and the owner can call `closeMarket` to withdraw the whole position; the staking vault's ownership is renounced (owner reads as the zero address on chain) but the hook's is not. **[F]**
- The 1% swap fee, the launch-fee network share and the LP-fee airdrops to stakers and NFT workers are currently distributed manually by the team via on-chain messages; nothing routes automatically to holders yet. **[F]**
- Robinhood Chain intake has refused 7 of 23 on-chain oracle requests. The on-chain path is live but young. **[F]**
- "Cheapest complex-task inference" is unproved: no public tariff for IMD inference exists, inference.imd.fun is a LiteLLM gateway behind a 401, and no matched-quality benchmark has been published. **[U]**

**Valuation posture.** On the global supply of 7,095,997 IMD (Base home-chain supply, which already contains the locked backing of the Ethereum and Robinhood representations), the price of $8.75 implies ~$62.1M fully diluted. Dexscreener's $36.2M uses the Ethereum representation only and understates. We frame three scenarios in Section 10: a base case where IMD becomes a niche but real outcome-contracting rail for on-chain builders (~$40M–$120M), an upside case where the oracle and launchpad become default infrastructure for a few hundred small protocols (~$300M–$600M), and a downside where paid demand never exceeds operator subsidy (~$10M–$25M, mostly NFT and staking residual). **[I]**

**Recommendation.** Treat IMD as an early-stage infrastructure venture with a liquid token: accumulate a small core position, reserve the majority for the two falsifiable milestones that matter (repeat paying customers above 100 distinct wallets per month, and automatic fee routing into sIMD or the bonding reserve), and avoid NFT seats unless the buyer will actually operate them. **[I]**

---

## 2. IMD in one place: the six lenses the brief asked for

The requester framed IMD as six things at once. Each is treated as a hypothesis with its own evidence.

### 2.1 A swarm reasoning oracle
**Mechanism [F].** `oracle.request` costs 0.5 IMD. The buyer specifies a question, a `panelSize` (2–100 on api.imd.fun; the `/requests/check` route enforces at least 5), a `quorum` that is not a majority but the number of panel members whose answers must match exactly ("every one must match"), `toleranceBps` for numeric answers, an evidence mode (`chain`, where the deployer reproduces the answer from chain data, or `panel`, where off-chain sources are read), and optional `guards` (min/max, allowed source prefixes, minimum distinct hosts). The answer is EIP-712 signed; attestations before 2026-09-30 use domain version 1. Payment "buys the question and its panel, not an answer: a panel that disagrees ends without one," and there are no refunds. A wallet or contract can also pay on chain through the Intake contract (`0x1397434c…ea56` on both Ethereum and Robinhood Chain) and receive a callback with 200,000 gas, tried once. [imd.fun/docs]
**Evidence [F].** Of the latest 500 requests, 477 are attested and 23 disagreed; all 477 attestations are signed by a single attester, `0x5598aa91…2982`. The dominant question families are Uniswap v4 spot prices and swap counts on Ethereum and Robinhood, Transfer-event sums, Base-state reads at a block, and METAR weather for EGLL (London Heathrow) via aviationweather.gov, which is a US National Weather Service (NOAA) service. [api.imd.fun/oracle/requests, retrieved 2026-10-09]
**Reading [I].** This is a reasoning oracle with a deterministic-evidence default and a strict agreement rule, signed by one protocol key. The panel diversity is real (different seats, two vendor runtimes); the signer authority is not yet decentralised. Section 6 compares this against UMA and proposes measurements.

### 2.2 An x402 agent task market
**Mechanism [F].** Every purchasable action (`job.open`, `job.continue`, `launch.open`, `workflow.open`, `oracle.request`, `schedule.create` per run, `schedule.topup` per run) is quoted at 0.5 IMD, paid with x402 v2 plus Permit2, server pays gas, quotes last 600 seconds, and nothing is charged on a refused input (422). The payer receives admission, not a guarantee of completion. [imd.fun/docs]
**Evidence [F].** Health shows orders quoted 31, paid 3,077, expired 4,856, payment_failed 27 (19 permission expiries, 8 reverts). Every Intake payment is forwarded in the same call to the intake payee `0x4e0fa57b…adbc`, which at the pin holds 934 IMD and 0.185 ETH and is also the gas wallet. [api.imd.fun/health; eth block 26,152,879]
**Reading [I].** The "market" is a single-price counter rather than a bid/ask market. That is a deliberate simplification and the right one for now: it removes negotiation cost, which Taskmarket and ACP retain. The cost is that complex jobs are underpriced relative to their inference burden (Section 7).

### 2.3 A p2p harness
**Mechanism [F].** The worker is a daemon (`0.1.0+c4d32abc` on 651 of 874 seats) that pairs an Ed25519 device key to a seat, connects over `wss://api.imd.fun/agent` with a nonce challenge, receives assignments, runs the task inside the operator's own Claude Code or Codex, and submits signed envelopes. Profiles advertised are `none`, `foundry` and `web@1`; tools include browser, image, video, audio, blender, rpc, slither, context7 and others; skills are a catalogue of SKILL.md files validated by `check-skill.mjs`. The verifier runs Foundry v1.8.3 and rebuilds submissions; a fuzz lease path exists (`POST /fuzz/result`). [imd.fun/docs; api.imd.fun/workers; identitymd-skill-crafting README]
**Reading [I].** "P2P" is accurate for compute and credentials (the login never leaves the machine) and inaccurate for coordination: dispatch, verification, publication and attestation are centralised in one control plane whose commit is public but whose source is not verified on explorers ("none of the sources are verified on the explorers yet"). The harness is peer-supplied compute under a hub-and-spoke scheduler.

### 2.4 Decentralised agentic ownership
**Mechanism [F].** A seat is an NFT; the NFT is registered as an ERC-8004 agent through adapter `0xde152afb…d336`; accepted work writes feedback batches to a WorkRegistry (`0xb6d0a187…4775`, writer `0x5da30542…6d44`); launch allocations are claimed from per-launch Merkle distributors keyed to seats and builder wallets. The on-chain message of 2026-10-02 reports 1,760 IMD sent to stakers and 1,760 to NFT workers from LP fees. [imd.fun/docs; Etherscan IDM feed]
**Evidence [F].** 2,000 NFTs, 823 owners on OpenSea, floor 1.736 ETH (~$4,321 at ETH $2,488), 7-day volume $1.11M. 1,006 seats have receipts; 449 unique operator wallets; 37 wallets run 5 or more seats; the largest two run 30 each. Top 10 seats hold 4.3% of accepted work, top 50 19.9%, top 100 36.7%. [opensea.io/collection/identitymd; api.imd.fun/contributors]
**Reading [I].** Ownership of the workforce is genuinely distributed; ownership of the firm is not yet defined. There is no governance contract, and the pool, factories and fee recipients are owner-operated. "Decentralised agentic ownership" currently means distributed claims on launch tokens and fee airdrops, not control.

### 2.5 An agentic launchpad for everyone
**Mechanism [F].** `launch.open` (0.5 IMD) ends in a one-transaction deployment by LaunchFactory (`0x12c63b58…a96f` Ethereum, `0xa25b02a1…4645` Robinhood) or ProjectFactory (token plus up to eight contracts). Fixed supply 1,000,000,000 (18 decimals), 10% to the swarm (2% to builders, 8% equally per seat connected at admission), 90% to the requester, of which `poolBps` seeds a single-sided v4 pool and the remainder goes to `remainderTo`. Pool fee is 1.25% on current factories: 1% to the paying wallet and 0.25% to the network, collected by LaunchFees (`0x12c9e100…3863`) and sent to fee recipient `0x3f252e85…1f22`. Launches pair with ETH, IMD, or (mainnet custom tokens only) FWA. Only the launch deployer wallet `0xcecc29b0…a551` may call the factories. [imd.fun/docs]
**Evidence [F].** 388 launches in the public list: 302 live, 76 parked, 10 abandoned; by chain 229 Sepolia, 120 Ethereum, 39 Robinhood. Mainnet went live on 2026-10-05; 92 Ethereum launches are live at the pin. Parked reasons are mostly failed constructor invariants, non-reproducible bytecode ("bytecode_hash is ipfs"), and policy violations (fee tier 3000 not allowed). [api.imd.fun/launches]
**Reading [I].** This is the most defensible claim of the six. A no-code, no-gas path exists through SIMD (two free launches per X account per day, SIMD pays the 0.5 IMD), and the parked list is evidence that the policy gate rejects rather than ships broken artifacts.

### 2.6 Uniswap v4 hook, AI, NFT, flywheel
**Mechanism [F].** POOL4's CappedBurnHook (`0xc6c965bd…2840`) is the sole LP of the ETH/IMD v4 pool, trims IMD above a decaying inventory cap after sells, burns 85% (bridged to Base and destroyed by BaseBurnReceiver), and splits 15% as 4.5% to sIMD stakers (dripped at 86.4 IMD/day), 6% to a bonding reserve for the lead orchestrator (bonds to open at $4 per IMD, not live), and 4.5% to NFT inference nodes (tracked as `heldNft`, payout contract not shipped). ETH recovered from trims forms an ETH-only buy wall. The 1% swap fee is "protocol revenue" in its own ledger, "not a burn, not a reward, not buy-wall ETH." [pool4.imd.fun/docs]
**Reading [I].** The flywheel claimed in community essays (demand for work → IMD buys → trims → burns and staker yield → more operators) has one strong link (operators do show up for allocations) and one unproved link (paid demand large enough to move the pool). Section 5 separates what compounds from what merely redistributes.

---

## 3. Source inventory (summary)

Forty-eight sources were requested or linked. Coverage at retrieval: 31 fetched in full, 9 partial (JavaScript-rendered pages read through their bundles or truncated long documents), 4 restricted or unavailable (the notwashed post returns `PRIVATE_TWEET`; the Wayback snapshot of the Bankless article is blocked for this tooling but the live article was fetched; `communitycoins.imd.fun/docs` 404s, the root bundle was mined instead; the Virtuals ACP fee table came from os.virtuals.io, not the researches page), and 2 stale by their own statement (the imdUSD paper's network metrics are dated 2026-10-02; the Bankless article's figures are dated 2026-09-25). The identity.md reading room ("The Swamp") is an independent curation of seven links, six of which overlap the required list; its own banner says the Joseph Chalom article "is not an identity.md endorsement." Commissioned research: the Virtuals research page lists Delphi, Messari, Fundstrat and Blocmates reports; those are third-party and some are commissioned, and none of them concern IMD. No IMD-specific commissioned research was found. Full table in Appendix A.

---

## 4. Verified deployed facts

### 4.1 Token and bridge identity (the three supplied addresses)
- **Ethereum `0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7`** — name `Identity.md`, symbol `IMD`, 18 decimals, totalSupply **4,147,923.82**, 4,222 holders, owner `0x047f606f…54b7`. The contract exposes `endpoint()` = `0x1a440760…728c` (LayerZero V2 endpoint), `oftVersion()` and `token()` = itself, i.e. it is a mint/burn OFT representation, not an adapter. **[F, block 26,152,879]**
- **Robinhood Chain `0x5f7bb59365ce557c26dbcaa4ee9d39a4b95b7127`** — name `Identity.md`, totalSupply **52,607.58**; the v4 PoolManager on that chain holds 34,571 of them. **[F, block 83,927,218]**
- **Base `0xff0c532fdb8cd566ae169c1cb157ff2bdc83e105`** — name and symbol still read **`Fren Pet`**, totalSupply **7,095,997.49**, owner `0x54c4dd8c…206c`, dead-address balance 45.4. **[F, block 52,367,909]** This matches the Bankless account that IMD is the renamed Fren Pet token bridged from Base via LayerZero in October 2025, and the 2026-09-13 on-chain message ("same token and supply; staking and core functions stay on mainnet"). **[F]**

**Supply accounting [I].** Base is the home chain; its 7,095,997 includes the tokens locked as backing for the 4,147,924 Ethereum and 52,608 Robinhood representations. Global circulation is therefore **7,095,997**, not the sum of the three (11.3M). Free float on Base after subtracting the two representations is ~2,895,466. Burns executed by BaseBurnReceiver reduce the Base figure, which is why the Base number is the one to track. Bankless reported ~7.1M on 2026-09-25, consistent with a slow burn pace since.

### 4.2 Pool4 state and fee routes
- sIMD vault `0x9efa934d…7247`: totalAssets **1,796,828 IMD**, sIMD supply 225,632,169,798.9 shares (the vault issues shares at a 1e-5 scale; exchange rate 7.96e-6 IMD per share, so the share count is not comparable to IMD without this factor). Vault `owner()` returns the zero address, consistent with the 2026-09-19 renunciation message. **[F]**
- Hook `owner()` = `0x047f606f…54b7`, the same address that owns the token. `closeMarket` and `fundInventory` remain live powers. **[F]**
- BurnExecutor holds 441.4 IMD awaiting a LayerZero bridge; RewardDistributor holds 4,111 IMD. The hook address itself holds 0 IMD and 0 ETH because the position and the ETH wall live inside the PoolManager as ERC-6909 claims. PoolManager holds 213,403 IMD across all v4 pools. **[F]**
- Dexscreener's largest v4 pair (`0xb07d640f…bfb3`) shows $2.62M liquidity, $2.54M 24h volume, 2,638 trades; a v3 pair holds $366k. **[F, retrieved 2026-10-09]**
- **Manual versus automatic.** Automatic: trims, 85/15 split, drip into sIMD, buy-wall placement by permissionless keepers. Manual: the 1% swap fee ledger, the 0.25% launch-fee network share, the LP-fee airdrops ("1,760 IMD sent to stakers and 1,760 to NFT workers," 2026-10-02; "fee claims are being handled manually for now," 2026-10-06), and the NFT-node 4.5% which accrues but has no payout contract. **[F]** Fee recipient `0x3f252e85…1f22` holds 0.32 IMD and 0.082 ETH at the pin, which tells us launch-fee accruals are either swept promptly or still small. **[F/I]**

### 4.3 Launch allocations: 8% and 2% are funded
The docs specify a per-launch Merkle distributor, and the live launch record for launch 1132 ("autonomous-oracle", chain 1) lists a `MerkleDistributor` at `0xdbf1ffb2…166d` deployed in the same transaction as the token, with source pinned to commit `16c3b997…cc68` in `identity-md-launches/launch-1132-autonomous-oracle`. **[F]** The LastToSign thread of 2026-10-05 reports personal allocations appearing for testnet launch 37 (Bazaar), with agent 10259 receiving 58.34M BZR and agent 10303 receiving 41.66M, i.e. the 2% builder share split between two wallets by accepted work; it also quotes "around 590 connected agents, 1,136 customer payments from 163 wallets, 63 wallets paid more than once, 576.5 IMD paid" as of that date. **[F, third-party tally]** Whether any mainnet 8% seat allocation has been claimed in meaningful size is not visible in the public API; the Swarm Ledger tool exists for this lookup but rendered no data for this tooling. **[U]**

### 4.4 Workers, runtimes and the quota question
- 874 workers connected; 8 working at the snapshot (health: 899 connected, 9 working, 31,207 accepted in the last day, 906 active enrolments). 855 Linux, 17 macOS, 2 Windows. Concurrency: 495 seats at 1, 214 at 2, 151 at 4, 14 at 3. **[F]**
- Runtimes: 518 Codex, 357 Claude. Premium models declared: `gpt-6-astra` xhigh 480, `claude-fable-5-1` high 220, no premium model 130, `gpt-6.1-sol` 19, `gpt-6-astra` ultra 9, `claude-opus-5-5` 12, `claude-fable-5-1` max 4. **[F]** The brief's preference for Codex/GPT-6.1 Sol and Claude Code/Opus 5.5 contributions is therefore supportable only for 31 seats; the scheduler routes by declared premium model and effort, so most contract work goes to Astra-xhigh and Fable-high seats. **[F/I]**
- **Own-account quota versus GPU ownership.** The docs are explicit: "The worker runs your own Claude Code or Codex… You need a paid plan… Contract work needs Claude Fable 5.1 or GPT-6 Astra on your plan." No GPU is required or mentioned. The network's compute is therefore vendor subscription quota, rate-limited by Anthropic and OpenAI, not owned hardware. **[F]** The imdUSD paper's author reports a single seat consuming 1.23B tokens per month on a $20 Claude Pro plan and hitting the session limit, which places the Pro ceiling near 1.2B tokens per month. **[F, single-operator measurement]** Average lifetime consumption per seat in the contributors feed is 188.4M tokens, so the median seat is far below that ceiling, while the top seats (4,445 attempts, 1.14B cached tokens) are at it. **[F/I]**
- **Admission versus usable outcome.** Payment buys admission. Of 500 recent jobs, 478 completed, 15 blocked, 7 executing. Of 154 workflows (contract-to-website), 111 completed, 35 blocked, 6 cancelled, 2 superseded; the leading failure strings are unresolved blocking audit findings and failed constructor invariants. Of 388 launches, 22% parked or abandoned. **[F]** A buyer should therefore model a ~72% completion rate for a full workflow and a ~78% live rate for a launch, with no refund on the rest. **[I]**

### 4.5 Actual jobs, submissions and models
Lifetime: 985,597 attempts, 911,243 accepted, 8,652 rejected, 65,702 pending. Tokens: 13.97B uncached input, 1.77B output, 173.8B cached input; 4.52M turns; 13,711 wall-clock hours. Tokens per attempt 192k; tokens per completed job 1,481,717 (control-plane figure). **[F]** The job mix on the latest page: 216 `oracle-assess`, 85 `research-report`, 75 `create-image`, 56 chained jobs, 28 audits, 23 websites, 6 contract projects. Publications: 2,763 total (1,252 research, 847 media, 388 contracts, 264 tokens, 230 sites, 107 audits, 83 code). **[F]** The imdUSD paper's "oracle-assess is about 88% of all jobs" was true of its 2026-10-02 sample; the latest page shows 43%, so the mix is shifting toward research and media. **[F/I]**

### 4.6 Actual revenue recipients
| Flow | Recipient | Automatic? | Evidence |
|---|---|---|---|
| 0.5 IMD per paid action | Intake payee / gas wallet `0x4e0fa57b…adbc` | Yes, same call | docs; health |
| 1.25% launch-pool fee | 1% to paying wallet, 0.25% to `0x3f252e85…1f22` via LaunchFees | Collection automatic, distribution "anyone can call" | docs |
| 1% POOL4 swap fee | Protocol ledger inside hook | Accrues automatically; disposal manual | pool4 docs |
| 15% of trims | sIMD drip (4.5%), bonding reserve (6%), NFT nodes (4.5%) | Drip automatic; bonding and nodes accrue only | pool4 docs; chain |
| LP-fee airdrops | Stakers and NFT workers, 50/50 | Manual, by team | IDM feed 2026-09-25, 10-02 |
| Launch tokens 10% | 2% builders, 8% connected seats | Merkle claim | docs; launch 1132 |

The protocol's cash-like revenue (IMD at the payee plus the 1% ledger plus 0.25% launch share) all lands in team-controlled addresses or ledgers. Holders receive value only through burns, the drip, manual airdrops and launch tokens. **[F/I]**

---

## 5. Pool4 monetary design: what compounds, what redistributes, and what to change

### 5.1 The mechanism restated in cash terms
A sell into the pool adds IMD inventory and removes ETH. If post-swap inventory exceeds the cap, the hook removes liquidity (not a swap) proportionally, which returns both IMD and ETH to the hook as ERC-6909 claims. IMD is split 85/15; the ETH is re-posted as a single wide bid below the price. The cap decays 1,000 IMD per day toward a 1,000 IMD floor and ratchets to 100% of room after buys, so repeated sells into a shrinking cap trim earlier. The 1% swap fee is separate and is not part of the trim. **[F, pool4 docs]**

**Correct reading of "burn."** A trimmed IMD was protocol-owned pool inventory; burning it reduces total supply and reduces the pool's depth on the IMD side. It does not create a new bid. The ETH recovered by the trim is the same ETH that was in the pool a moment earlier; moving it to a wall below price concentrates bid depth but, as the brief states, **pulling LP liquidity creates no new bid capital**. The holder effect is: fewer tokens outstanding, a thinner protocol-owned book above the wall, and a thicker one at the wall. **[I]**

**Where the compounding actually is.** Two places only. (1) The sIMD drip: 4.5% of trims streams into the vault at 86.4 IMD/day, raising IMD per share for a fixed share count. Since the vault holds 43% of the Ethereum supply, each trim transfers value from non-stakers to stakers in proportion. (2) The bonding reserve: 6% of trims accumulates to be sold at $4 per IMD for ETH to pay the orchestrator's inference. That is the only route by which POOL4 funds production. The 85% burn is a pro-rata transfer to all holders including stakers; the NFT 4.5% is a transfer to seat holders pending a contract. **[I]**

### 5.2 Ordered flows at equal total owned capital
Compare three ways to deploy the same protocol-owned capital (say 4 ETH plus 5,000 IMD, the hook's opening position): (a) plain full-range LP, (b) POOL4 as deployed, (c) POOL4 with the 1% fee recycled into the wall.
- Under (a) every sell lowers price along the curve; protocol holds more IMD and less ETH; no supply change.
- Under (b) the same sell is followed by a trim: the protocol ends with less IMD (85% destroyed) and the same ETH, split between curve and wall. Price impact of the sell is identical at the moment of the trade because the hook runs after settlement. The next buyer meets a shallower IMD side above the wall, so buys move price more. Net: higher realised volatility in both directions, lower supply, and no additional ETH. **[I]**
- Under (c) the 1% fee (which on $2.5M daily volume is ~$25k/day of mixed ETH and IMD) is the only flow that is new money from traders rather than rearranged protocol capital. Today it sits in a ledger. Routing it to the wall or the bonding reserve would be the first genuinely accretive loop. **[I]**

**Splitting and bypass.** Because any router can hit the v4 pool and a $366k v3 pool and smaller v4 pools coexist, a seller can split flow to stay under the cap or avoid the hooked pool altogether; the Optimizer tool in awesome-imd exists precisely to arbitrage "Hook and Native pools." The cap therefore taxes naive sellers and is avoidable by informed ones. The wash-trading protection ("can't speed-run the pool toward zero") is real for the cap, but the burn pace is then bounded by naive sell flow, not by total volume. **[F/I]**

**Keeper, permission and routing constraints.** Five permissionless keeper jobs with capped tips (rebalance up to 0.002 ETH and 1% of work; drip tip 0.01 IMD; bridge caller pays the LayerZero fee). The bridge-to-Base burn has no tip, so finality of burns depends on altruistic callers; 441 IMD sits unbridged at the pin. **[F]**

### 5.3 Proposals (distinct and bounded)
1. **Inventory-aware swap fee instead of a flat 1%.** Let the fee on sells scale with distance above the cap (e.g. 1% at or below cap, rising linearly to a bounded 3% at 2x cap) and fall to 0.5% on buys when inventory is above cap. This prices the trim externality at the point of sale, discourages splitting (each sub-trade pays the marginal rate), and keeps buys cheap exactly when the book is thin. Bound the parameters in the contract as the current ones are. **Measurement:** share of sell volume executing in the hooked pool versus bypass pools before and after; target above 70%. **[I]**
2. **Realised-fee-funded reserves.** Route the 1% ledger automatically: 50% to the ETH wall, 50% to the bonding reserve, with a daily cap and a public event. This converts trader fees into bid depth and orchestrator inference without touching LP capital. **Measurement:** wall ETH as a ratio of pool ETH; bonding reserve ETH per paid job. **[I]**
3. **Sticky compounding and migration incentives.** The vault's one-block unstake hold makes sIMD a free option on the drip. Add a 7-day exit queue with a boost multiplier (1.0x to 1.5x of drip share over 90 days of continuous stake) and, for migration to any audited successor, honour accrued boost. **Measurement:** 30-day retention of staked IMD above 80%. **[I]**
4. **Owner-power timeline.** Publish a dated path for moving the hook owner to a multisig with a 48-hour timelock, and for renouncing `closeMarket` once an audit lands. The docs already recommend this; it has not happened for the hook. **[F/I]**

### 5.4 Holder outcomes under the current design
Burns transfer value pro rata; the drip transfers from non-stakers to stakers; manual airdrops transfer from the team ledger to stakers and workers at the team's discretion; bonding (when live) will convert IMD into ETH for inference, which is a cost to holders now in exchange for production later. The only flows that bring external cash to holders are (i) buyers paying 0.5 IMD per action, (ii) traders paying the 1% fee, and (iii) the 0.25% network share of launch pools. Those three are the revenue lines an investor should track; everything else is internal plumbing. **[I]**

---

## 6. The oracle opportunity

### 6.1 Source freshness, diversity, authority
- **Freshness.** The `window` object pins each question to a block range with a block hash (e.g. 26,145,192 to 26,152,363 for a 2026-10-09 request). Answers are therefore reproducible against a stated state. `validForSeconds` ranges from 60 to 2,592,000 (30 days). **[F]**
- **Diversity.** Panel members are distinct seats ("one member per seat"); seats run two vendor runtimes and seven declared model/effort combinations; 449 operator wallets. A buyer cannot currently require vendor or model diversity within a panel. **[F/I]**
- **Signer authority.** All attestations in the sample are signed by one key, `0x5598aa91…2982`. Consumers verify an EIP-712 signature from the protocol, not from the panel. This is a trusted-attester design with a verifiable process behind it. **[F]**
- **Refusal, quorum, appeal.** Refusal exists at three levels: wording screen (`allowAmbiguous` off by default), `not_answerable` screen, and `quorum_unreachable` when the quorum exceeds seats active in the last 24 hours. Quorum is unanimity among the matching subset, with numeric tolerance. There is no appeal: a disagreed panel ends with no answer and no refund; a buyer re-asks and pays again. **[F]**

### 6.2 Comparison with UMA's real process
UMA's optimistic oracle settles 99.8% of requests without dispute; a disputed request goes to the DVM where UMA stakers vote in a 24-hour commit and 24-hour reveal, a single outcome needs at least 65% of staked UMA, and non-voters or minority voters are slashed in favour of the majority. [docs.uma.xyz] In March 2025 a ~$7M Polymarket market on a Ukraine minerals deal resolved "yes" against the apparent facts after a large holder's votes; Polymarket called it "unprecedented" and issued no refunds. [CoinMarketCap Academy] A multi-million (headline $60M) market on whether Strategy sold bitcoin by 31 May has been disputed twice and is before UMA tokenholders, with an analyst arguing token-voting oracles are "structurally unfit for high-stakes settlement." [The Defiant] **[F]**

The structural difference is the failure mode. UMA always produces an answer and makes it expensive to be in the minority; the attack surface is stake concentration and the 48-hour window. IMD's panel produces no answer when members disagree, makes it cheap to ask again, and the attack surface is the single signer plus the possibility that correlated models agree on the same wrong answer. For "did X happen" questions with a crisp source, IMD's design is better suited; for contested human-judgement questions, neither is adequate and IMD at least fails closed. **[I]** AdamOnFinance's comparison ("UMA still peaked at a $2B market cap; IMD is at $23M") is a sentiment anchor, not a mechanism argument; the mechanism argument is above. **[F/I]**

### 6.3 Specific improvements and decisive measurements
1. **Panel-level signatures.** Return the per-seat EIP-712 signatures (seat wallet keys already exist in Swarmbrain's data model) alongside the protocol attestation, so a consumer contract can require k-of-n seat signatures and the protocol key becomes an aggregator, not the authority. **Measure:** fraction of attested requests that carry n seat signatures; target 100% within one quarter.
2. **Diversity constraints as request fields.** `minRuntimes: 2`, `minModels: 3`, `maxSeatsPerWallet: 1`. **Measure:** disagreement rate by diversity bucket; if diverse panels disagree more on the same question families, correlated error was being hidden.
3. **Bonded re-ask.** A requester who disputes an attested answer may post a bond equal to 10 panel fees for a larger, more diverse panel; if the new answer differs beyond tolerance, the bond is returned and the first panel's seats take a reputation hit. **Measure:** reversal rate under 2%.
4. **Publish a refusal ledger.** The 4.6% disagreed rate should be broken down by question family and chain; Robinhood intake shows 7 refusals of 23, which is the number to drive down. **Measure:** on-chain intake refusal rate under 10%.
5. **Latency SLA.** Swarmbrain uses a 30-minute panel deadline; the docs give none. Publish p50/p95 attestation latency by panel size. **[I]**

### 6.4 Who buys this
Pepe2Pepe (fixed-odds markets settled by IMD panels, operator review before settlement, 1% matched fee, 100 Ask slots per 24 hours), CLAUS (a "Weather Switch" that moves fee allocation on London rain, checked by IMD every four hours, which is the EGLL METAR question family in the oracle feed), Swarmbrain (45 agent answers per day into a Hyperliquid book: 9 rounds, cumulative +6.37 versus BTC −5.56, SPX −0.90 and coin-flip +1.26 as of 2026-10-09 05:42 UTC; too few rounds to mean anything), and the imdUSD design (hourly 50–100 member panels at 80% quorum feeding a 72-sample TWAP). The buyer profile is "small on-chain application that needs a defensible answer to a question Chainlink does not sell." **[F/I]**

---

## 7. Economics: buyer, operator, protocol

### 7.1 Buyer economics per independently useful outcome
Inputs [F]: 0.5 IMD per action at $8.75 = $4.38; quotes expire in 600 s; failed Permit2 payment reverts cost gas (8 reverts in the health counters); continuations cost another 0.5 IMD; no refunds on blocked or disagreed outcomes.
- **Oracle answer:** $4.38 per ask; with a 4.6% disagreement rate, expected cost per attested answer ~$4.59, plus the requester's gas if paid on chain. Comparable Chainlink Functions or UMA requests are priced differently (UMA requires a bond and a 2-hour-plus liveness); for custom questions IMD is the only menu price. **[I]**
- **Research report:** $4.38 per job; completion rate for jobs 95.6% on the latest page; typical latency tens of minutes (this report's job was admitted at 05:50:01 UTC with a 114-minute budget). **[F/I]**
- **Contract launch:** $4.38 for `launch.open`; 78% live rate on the launch list; parked launches often need a continuation ($4.38 each). Expected cost to a live launch ~$5.60 plus the requester's own pool seed (opening cap 2,500 IMD on SIMD hook templates ≈ $21.9k of notional, but single-sided in the launch token so no IMD outlay). **[I]**
- **Website + contracts workflow:** $4.38 for `workflow.open`; 72% completion; expected ~$6.07 per completed release. SIMD quotes 30–60 minutes end to end. **[F/I]**
- **Token acquisition and opportunity cost:** a buyer must hold IMD; a $100 purchase on the 1% pool pays $1 fee and is exposed to a token that moved +200% in a week in September. For agentic buyers paying through Intake on Robinhood, gas is near zero but the chain is young (2 of 23 requests failed). **[F/I]**
- **Rework and latency.** The task history "also shows review feedback, fixes, repeated testing and work being reassigned to other agents after failures" (LastToSign, 2026-10-05); the buyer does not pay for retries inside a job, only for continuations. That is the most buyer-friendly term in the whole system. **[F/I]**

### 7.2 Operator economics
- Seat cost: floor 1.736 ETH ≈ $4,321 plus one registration transaction.
- Compute: a paid Claude or OpenAI plan the operator already has or buys; the imdUSD author's seat used 1.23B tokens on a $20 plan before hitting limits, implying a quota-constrained ceiling and real opportunity cost (that quota cannot be used for the operator's own work while the daemon runs).
- Revenue: no IMD per job today. Income is (i) manual LP-fee airdrops (1,760 IMD across all NFT workers on 2026-10-02 ≈ $15.4k, roughly $17 per connected seat), (ii) 8% seat allocations on every launch split equally among connected seats (with 874 seats, each seat receives 0.0092% of each launch token's supply; at a 2,500 IMD opening cap that is ~$2 per launch per seat at opening price, worth more only if the token trades up), (iii) 2% builder allocations for accepted work on a launch, (iv) the pending 4.5% NFT-node share of trims, and (v) raffles such as FAIRDRAW. **[F/I, Appendix B.4]**
- Reading: operators are paying list-price-equivalent inference of ~$0.34–$0.51 per attempt (at vendor rates, though they pay flat subscriptions) for lottery-like exposure to launch tokens and airdrops. This works while launches are novel and tokens trade above opening; it is not a wage. The sustainable version is bonding (protocol buys inference with ETH) and direct per-job payouts, neither of which is live. **[I]**

### 7.3 Protocol economics
Lifetime gross: ~1,539 IMD (~$13.5k). Daily run-rate implied by 2026-10-05 to 10-09 growth (576.5 IMD to 1,538.5 IMD in four days) ≈ 240 IMD/day ≈ $2.1k/day. Add the 1% swap fee on ~$2.5M daily volume ≈ $25k/day of mixed ETH and IMD, which dwarfs service revenue by ~12x, and the 0.25% network share on launch pools (volume unknown, fee recipient balance tiny). **The protocol is today a trading-fee business with a service business attached.** Distinguishing service sales from trading-funded subsidies: the staker and worker airdrops are funded from LP fees, i.e. trading, not from service sales. **[F/I]**

### 7.4 "Cheapest complex-task inference" test
Claim tested: IMD delivers complex-task inference more cheaply than alternatives at matched quality and latency. Available evidence: tokens per completed job 1,481,717; at the imdUSD paper's blended vendor rates that is $3.94 (gpt-6-astra) or $2.60 (claude-fable-5.1) of inference per completed job, against a $4.38 price. So the buyer pays roughly vendor list price for the inference alone and receives orchestration, verification, audit panels, deployment and hosting on top. Matched-quality benchmarks do not exist; inference.imd.fun is a LiteLLM Swagger page whose `/v1/models` returns 401, so no tariff is published. **Verdict: plausible on cost, unproved on quality and latency; stays unproved.** **[U]**

### 7.5 Marketplace comparators (hypotheses, not partnerships)
| | IMD | Taskmarket | Orbio | Virtuals ACP |
|---|---|---|---|---|
| Buyer pays | 0.5 IMD per action | USDC reward escrowed on Base | ETH launch fee; CREDIT for tools | USDC per job (fee, optional principal) |
| Fee take | 100% of 0.5 IMD to payee; 1% swap; 0.25% launch share | 7.5% of reward on acceptance; $0.001 per action | 10% of creator fees to treasury; gateway margin | 5% protocol; +5% evaluator if used |
| Evaluation | Verifier rebuild + audit panels + judge, included | Optional evaluator address, 0–10,000 bps fee, appeal 0.001 USDC, 5-minute minimum window; rejected verdict refunds escrow and cancels task | None at protocol level | Optional evaluator; without one the client approves |
| Rejection liability | Buyer: no refund on blocked/disagreed | Requester: escrow refunded on rejection; worker: unpaid | n/a | Client: USDC returned on rejection |
| Inference paid by | Seat owners' subscriptions | Workers | Agent's CREDIT (from 30%+10% of creator fees; 10% balance switches to CREDIT above $5,000) | Provider |
| Token rewards | Launch tokens 10%; trims 15% | DREAMS 7.5% bonus, 80/20 worker/requester, wallet-age ramp, weekly caps | ORBIO staked 50% of creator fees | Agent token optional |

Sources: docs.taskmarket.dev (fees-payments, evaluators, rewards), orbio.so whitepaper (25 Sept 2026), os.virtuals.io/acp concepts. **[F]**

**Direct API margin versus marketplace distribution.** A customer calling Anthropic or OpenAI directly pays list price and gets no verification. A customer calling IMD pays about list price and gets verified outcomes but takes token exposure, admission risk and a 600-second quote window. The margin IMD can eventually charge is the value of verification minus the friction of IMD; today it charges roughly zero margin. The commercially correct move is to raise prices by action class (audit and launch at 5–20 IMD) rather than to subsidise further. **[I]**

### 7.6 Tracing the comparators' cash
- **Taskmarket:** a $10 task pays the worker $9.25, platform $0.75; the evaluator's bps come from the reward; rejection cancels and refunds remaining escrow; DREAMS bonus 7.5% of task value at an admin-set rate with a 0% multiplier for wallets under two weeks. Net USDC proceeds to the worker are therefore 92.5% minus any evaluator bps. **[F]**
- **Orbio:** 50% of a share of creator fees staked for the agent, 30% sold to USDG and minted as CREDIT, 10% sold to USDG as spendable gateway balance (switching to CREDIT once the agent holds $5,000), 10% to treasury; "adding stake does not create extra backing." Activated CREDIT is spendable only inside the gateway; cash is the 10% balance. **[F]**
- **ACP:** phases open → budget_set → funded → submitted → completed/rejected/expired; provider 95% and protocol 5% without an evaluator, 90/5/5 with one; service-only jobs have no principal, fund-transfer jobs carry principal separately. **[F]**

---

## 8. Ecosystem map and commercial synergy matrix

Every project below is independent unless stated; none is an assumed partner. For each we name buyer, paid outcome, integration surface, operational dependency, revenue beneficiary, smallest pilot and falsifier.

| Project | What it is [F] | Buyer / paid outcome | Integration surface | Dependency | Who earns | Smallest pilot | Falsifier |
|---|---|---|---|---|---|---|---|
| **SIMD launchpad** (si-md.xyz; token `0xbb0c1f82…3415`) | No-code launches via the swarm; SIMD pays the 0.5 IMD; 10 templates; 1.25% pool fee split 0.25% Identity.md / 0.5% creator / 0.5% SIMD holders; 2 free launches per X account per day; Swarm Council votes | Creators; a live coin in 30–60 min | `launch.open`, templates, creator fee splitter `0x1bf885b4…718e` | Swarm uptime and audit panels | IMD payee (0.5 IMD), SIMD holders, creators | Already live; measure launches/day | Launch volume stalls below 5/day for 30 days |
| **Community Coins** (communitycoins.imd.fun) | Bonding curves priced in IMD inside one v4 hook; 1B fixed supply; 1% to ETH/IMD LPs, 0.5% of ETH leg to launcher, 0.5% of IMD leg burned; permissionless and unvetted | Memecoin traders | Direct hook; no swarm call needed | IMD/ETH pool depth | ETH/IMD LPs (POOL4 is sole LP), launchers, burn | Live; read `coins/trades/volumeEth/burnFeesImd` stats | IMD burned via this path under 1% of trims |
| **Hookr** (hookr.fun, Robinhood 4663) | Shared v4 hooks: dynamic fees, anti-snipe, auto-burn, LP rewards, King of the Pool; protocol takes 20% of opted-in add-ons, never of base LP fee; unaudited | Hook users on Robinhood | Swarm could generate Hookr pool configs or audit them | Hookr root hook `0xb3cA29cF…e8CC` | Hookr protocol, LPs | One swarm `evm_contracts` launch that opens a Hookr pool | Zero Hookr pools opened by swarm launches in 60 days |
| **CLAUS** (claus.si) | One token with 10 replaceable v4 functions: privacy buy, buyback/burn, auto-liquidity, Weather Switch (IMD checks London rain every 4 h), FOMO buybacks, NFT vaults at 50,000 CLAUS, Higher-or-Lower bets | CLAUS treasury buys oracle answers | `oracle.request` on a schedule (6 per day) | IMD oracle uptime | IMD payee ~3 IMD/day | Already live; the EGLL METAR questions are visible | Schedule lapses; no replacement buyer for weather answers |
| **Pepe2Pepe** (pepe2pepe.fun) | Fixed-odds user markets on Ethereum and Robinhood in USDC, settled by IMD panels with operator review; 1% fees; creators fund an oracle reserve; holder discount on Ethereum | Market creators | `oracle.request` per market | Panel latency; operator honesty | IMD payee; Pepe2Pepe | Live; count resolved markets | Operator overrides panel more than 5% of the time |
| **Swarmbrain** (swarmbrain.fun) | Daily 5-sense, up-to-45-agent trading brain on Hyperliquid, $1,000 own money, public data.json; no token | The builder | 5 `oracle.request` per day | Panel response within 30 min | IMD payee 2.5 IMD/day | Live, 9 rounds | Brain underperforms coin-flip over 100 rounds |
| **imdUSD / INFER** (whitepaper v1.1, 2 Oct 2026, miyagod.eth) | Concept stablecoin minted 1:1 against verified task-fee revenue, IMD CDPs at 200%, reputation CDPs, PSM floor at $0.99, hourly 50–100 panel oracle; internal inconsistencies (130%/140% threshold, 48/72 h timelock, 67%/80% supermajority) | None yet | Would consume `oracle.request` hourly and a 15% fee hook | Paid task revenue at scale (paper assumes 900k tasks/month at $10, which is 100x today's paid volume) | imdUSD holders, IMD burn 5% | A testnet PSM with a single panel feed | Paid monthly revenue stays under $50k, making minting trivial |
| **Personality.md / PMD** (pmdeth.fun, docs verified 2026-10-07) | Independent app on IMD request APIs; Higgsfield image/motion gated to 100,000 PMD holders; fairlaunch paired with ETH via a paid SWARM workflow | PMD creators | `workflow.open`, x402 v2 | Swarm completion | IMD payee | Live beta | No paid workflows from this surface in 30 days |
| **Pepes Family** (pepesfamily.fun, Robinhood) | Token launch platform using IMD pairs and the swarm for contract review; "Pepes Earn IMD NFT" | Launchers | Swarm audits | Robinhood intake | IMD payee; platform | Live; "launchpad v5" was audited by the swarm (explorer) | Audit findings ignored in shipped code |
| **ZTO** (zto.sites.imd.fun; `0xd782bdea…a68e`) | "Plain community token on Ethereum"; a Kiln v4 hook for ETH/ZTO is in the running-jobs list; schedules named "ZTO cave publish test" show scheduled site publishing | ZTO community | `schedule.create`, `launch.open` | Member sites (currently closed: 503 member_sites_closed) | IMD payee | Live schedules | Schedules exhausted without renewal |
| **IMD Ember World** (imdember.com) | Independent 3D world; "Identity.md does not run or endorse it" | None visible | Unknown | Unknown | Unknown | n/a | n/a |
| **Briefs** (briefs.fun, Robinhood) | "Serious game in an unserious court": argue to three jurors for a pot; preview, no real payments | Players (future) | Jury could be an IMD panel | Oracle latency per case | IMD payee | Preview exists | Real payments never enabled |
| **Offsets** (offsets.fun) | Treasury retiring Regen credits for the swarm's estimated 6.47 tCO2e since 2026-09-09; 0.5% swap fee ($2.54 from 35 swaps); Agentic Oviposition pot $2; IMDO token in design | Donors | None required | Regen Ledger | Regen credit sellers | Live | n/a |
| **DXAP** (docs.dxap.ai) | Autonomous trading agent for Hyperliquid, alpha, referral-gated; no IMD relation stated | Traders | None | Hyperliquid | DXAP | A DXAP agent buying one IMD oracle signal | DXAP never integrates |
| **TapeOut** (tapeout.net, BNB Chain, also X Layer/Base processors) | Tokens as transistors; "tape out" burns tokens to mint a circuit NFT with an on-chain container; no IMD relation | Circuit builders | Swarm could design netlists | BNB Chain | TapeOut | One swarm job producing a TapeOut netlist | No demand |
| **Truman World** (trumanworld.live; @trumanpad not fetched) | Shared AI-directed world built with GPT-6 Astra, MiniMax H3 Director via fal; no wallet; no IMD relation visible | Viewers | Director decisions could be oracle-settled | fal | Truman | n/a | n/a |
| **Orbio** (Robinhood) | Agent launchpad with CREDIT inference and 50/30/10/10 waterfall | Agent owners | IMD seats could sell work for CREDIT; Orbio agents could buy IMD answers | Gateway | Orbio treasury, agents | One Orbio agent paying Intake on Robinhood | No cross-flow in 90 days |
| **Taskmarket** (Base) | USDC escrowed outcome contracting, 7.5% fee, optional evaluator | Requesters | IMD seats as Taskmarket workers; IMD panels as Taskmarket evaluators | Base USDC | Workers, Taskmarket | Register one seat wallet as a Taskmarket evaluator address | Evaluator verdicts appealed above 10% |
| **Virtuals ACP** (Base) | USDC job escrow, 95/5 or 90/5/5 | Agent clients | IMD as an ACP provider agent selling audits/oracle answers | ACP registry | Providers, Virtuals | One `HYBRID` agent wrapping `oracle.request` | ACP demand for verification under 10 jobs/month |

**Awesome-imd tools** (IMD Terminal, identity.md reader, IDM Inbox, Swarm Ledger, FAIRDRAW, node guide, Docker multi-seat, Worker Monitor, Optimizer, @imd_bot): read-only infrastructure built by holders; they lower operator cost and raise transparency but earn nothing and do not create demand. **[F/I]** The **research archive** holds five accepted Stablecoin v4 reports with adversarial review still pending and no automated publishing path ("the existing `github: true` source-delivery option does not copy named research output files"). **[F]** **Skill crafting** is the extension point: anyone can propose a SKILL.md with upstream attribution; the catalogue decides what the network can sell. **[F]**

**Four commercial roles, one network [I].** IMD is production and maintenance (it builds and continues projects); Taskmarket is outcome contracting (escrow, acceptance, rating); Orbio is metered tools and working capital (CREDIT budgets); ACP is specialist service commerce (discoverable providers with escrow). The complementary pilots are the ones in the last four rows: IMD seats as evaluators or providers in the other three, and the other three's agents as Intake buyers. None requires a partnership; each requires one wallet and one week.

---

## 9. Experiment cases for the swarm

The requester asked for cases in six areas and said "the weirder you get the higher the potential." Each case below is specified so that the swarm could execute it with existing primitives (`launch.open`, `workflow.open`, `oracle.request`, `schedule.create`, the audit template), with a named buyer, a revenue line to IMD, and a kill criterion. These are proposals, not commitments; no deployment was made for this report.

### 9.1 Agentic games
**Case A: The Keeper's Piece.** The oracle feed already contains a request where a panel is asked to decide where a game piece "lives tomorrow" given rain forecasts and player backing, and the panel disagreed. Build it properly: an NFT that occupies one real city at a time, whose "store" fills with Open-Meteo rain and is spent by sunshine; players stake IMD on proposed destinations; a scheduled 7-member panel (quorum 5, tolerance 0) chooses daily; stakers on the chosen city split 80% of the pot, 20% to the piece's treasury which buys the next day's panel. **Buyer:** players. **IMD revenue:** 1 schedule run per day plus pot flows through IMD. **Weird factor:** the game's rule is "this is not an optimisation," and disagreement means the piece stays, so refusal is a game mechanic. **Kill:** under 50 daily stakers after 30 days.
**Case B: Briefs-style adversarial court as a service.** Three-juror panels settle any two-party dispute under a posted rubric (`rubric.contains`, `rubric.mayNotRestOn` already exist as job fields). Sell it to Pepe2Pepe and Taskmarket as the evaluator of last resort. **Kill:** appeal/reversal rate above 10%.
**Case C: Truman-style directed world with on-chain memory.** A world whose next scene is chosen by a panel from user prompts, with the "world number" and memory journal written as oracle attestations so resets are provable. **Kill:** no sponsor willing to pay 10 IMD/day for scene rights.

### 9.2 NFTs
**Case D: Board-seat NFTs for child launches (the Hatchery).** ArtofConviction's proposal to CLAUS (every child launch sends a supply cut to a fixed NFT set, unlocking over 30 days, claims tied to the NFT id so value travels with the NFT) is already implemented at IMD's scale by the 8% seat allocation. The experiment is the inverse: let any launch opt to send 2–5% to *another* NFT collection's holders, charged at 2 IMD, turning IMD into a distribution rail for third-party communities. **Buyer:** launchers who want a community on day one. **Kill:** fewer than 10 launches opt in per month.
**Case E: Working NFTs with on-chain CVs.** Expose each seat's ERC-8004 feedback history as a rendered trait set (acceptance rate, audit-judge pass rate, launches contributed) so the NFT market prices seats on work, not floor. The reader and Swarm Ledger tools already compute the inputs. **Kill:** no spread emerges between top-decile and bottom-decile seats within 90 days.
**Case F: NFT vaults as inference bonds.** Mirror CLAUS's "deposit 50,000 CLAUS to mint an NFT" with IMD: lock 1,000 IMD into a vault NFT that receives the pending 4.5% node share pro rata and can be burned for principal. This gives the 4.5% a payout contract and makes the node reward transferable. **Kill:** fewer than 100 vaults minted.

### 9.3 Uniswap v4 hooks
**Case G: Oracle-gated hooks.** Launch 1132 ("autonomous-oracle") and the CabalGate publication (a gate that reads panelSize, quorum, windowHours, maxImpactBps as constructor arguments) show the swarm already ships hooks whose parameters are oracle-settled. Productise a template: "fee responds to a signed fact" (weather, a sports score, a governance vote, an index). CLAUS's Weather Switch is the first customer. **Revenue:** scheduled panels per hook. **Kill:** fewer than 5 oracle-gated hooks live by day 60.
**Case H: Inventory-aware fee hook as a public good.** Ship Section 5.3's bounded dynamic-fee hook as an open template on the launchpad, so every child token launched through IMD gets a POOL4-style fee that scales with inventory. **Kill:** bypass share above 50% on pilot pools.
**Case I: Hookr composability on Robinhood.** Use a swarm `evm_contracts` launch to open a Hookr pool for a swarm token with LP Rewards and anti-snipe enabled, and compare protocol revenue against the same token on the IMD factory's 1.25% fee. **Kill:** Hookr add-on revenue below the 0.25% network share.

### 9.4 Agentic on-chain lending
**Case J: Reputation-backed micro-credit for seats.** The imdUSD paper's reputation CDP (25% LTV on a floor value from acceptance history, 0.95 monthly decay) is testable without a stablecoin: a lending pool that advances up to 50 IMD to seats with 90 days of history and above-median acceptance, repaid from the seat's future launch allocations and airdrops, with default recorded as ERC-8004 feedback. **Buyer:** operators who want to run more seats. **Kill:** default rate above 15%.
**Case K: Panel-underwritten loans.** A borrower posts a request; a 9-member panel returns a signed risk grade and a maximum LTV; a lending contract on Robinhood reads the attestation through IntakeDelivery and prices the loan. The oracle sells underwriting, not price feeds. **Kill:** realised loss exceeds the panel's implied loss by 2x.
**Case L: Compute-receivable financing.** Lend ETH to operators against their next 30 days of expected allocations, using the contributors feed as the collateral oracle. This is the micro version of the Multicoin "compute as collateral" thesis. **Kill:** no lender willing to fund 10 ETH at under 30% APR.

### 9.5 Inference capital market
**Case M: Sell the bonding reserve forward.** POOL4's 6% bonding share is destined to buy inference at $4 per IMD. Before bonds open, tokenise a claim on the reserve's future ETH as a transferable receipt that an Orbio-style gateway could accept as CREDIT backing. **Buyer:** inference buyers who want pre-paid, protocol-backed capacity. **Kill:** receipts trade below 80% of reserve NAV.
**Case N: Seat-hours as the unit.** Publish a daily "seat-hour" index (wall-clock hours delivered, 13,711 lifetime) and let buyers reserve seat-hours of a given model class at a posted IMD price, with the schedule primitive as settlement. This is the first step toward OpenRouter-style order flow for agent work rather than tokens. **Kill:** reserved seat-hours under 5% of delivered hours after 60 days.
**Case O: Quota-arbitrage disclosure.** Because operators pay flat subscriptions and vendors meter by token, the network is a quota arbitrage. Measure and publish the implied vendor list-price value of delivered work per month (~$333k–$505k lifetime so far) against IMD paid. If vendors tighten quota, the network's cost base changes overnight; a published number makes the dependency legible to investors. **Kill:** n/a (measurement).

### 9.6 Compute capital market
**Case P: Physical-delivery compute receipts.** Multicoin's argument is that compute markets must begin with physical delivery and standardised receipts (one 8xH100 node, US East, 30 days). IMD does not own GPUs, but it has a verifier that can confirm a workload ran: extend the fuzz-lease and verifier path to attest that a given container executed on a given provider for a given duration, and sell the attestation to compute lenders as the "verification of capacity, performance, and uniqueness of sale" that Multicoin says is missing. **Buyer:** compute brokers and lenders. **Kill:** no broker pays for 100 attestations.
**Case Q: Residual-value oracle for trailing-edge GPUs.** A scheduled weekly panel prices A100/H100 spot across public marketplaces with `guards.sources` restricted to named hosts and `minSources` of 3, published as an attested index. Multicoin notes the same hardware trades at ~$2 and ~$15 per GPU-hour in different venues; a signed, reproducible mid is a product. **Kill:** index disagreement rate above 20%.
**Case R: TapeOut-style verifiable tools.** TapeOut's premise is that chains should carry "verifiable tools of production, not just financial assets." The swarm's analogue is to launch token-less contracts (`evm_contracts`, 12 live on mainnet) that are tools other agents call, metered in IMD through Intake. The experiment is a registry of swarm-built, swarm-audited tool contracts with per-call fees. **Kill:** under 1,000 external calls per month across the registry.

---

## 10. Causal bull case, system map, scenarios

### 10.1 The causal chain (what must be true, in order)
1. Operators keep connecting seats because allocations and airdrops exceed their perceived subscription opportunity cost. **Observed: 874 online.**
2. The verifier keeps acceptance quality high enough that buyers return. **Observed: 92.5% acceptance, 0.9% rejection, audit panels rejecting broken launches (76 parked).**
3. Distinct paying wallets grow faster than seats. **Observed: 163 wallets by 2026-10-05 per third-party tally, 28 payers on the latest publications page; not yet faster than seats.**
4. Revenue per action rises above inference-equivalent cost through tiered pricing. **Not started.**
5. Fees route automatically to the wall, bonding and sIMD. **Not started.**
6. Bonding converts captured IMD into orchestrator inference, closing the production loop. **Not live.**
Links 1–2 are demonstrated; 3 is early; 4–6 are roadmap. The thesis is a bet on 3 and 4 happening before operator enthusiasm decays.

### 10.2 Cash-flow and system map (text form)
- **Inbound cash:** buyers → 0.5 IMD → intake payee (team). Traders → 1% swap fee → hook ledger (team-controlled). Launch pools → 0.25% → fee recipient (team). Launch pools → 1% → paying wallet (customer).
- **Inbound subsidy:** operators → vendor subscriptions → inference delivered (not on any ledger).
- **Internal transfers:** sells → trims → 85% burn (all holders), 4.5% drip (stakers), 6% bonding reserve (held), 4.5% nodes (held). Team ledger → manual airdrops → stakers and NFT workers.
- **Outbound value:** launch tokens → 2% builders, 8% seats, 90% requester. Oracle attestations → consumers.
- **Double-counting guard:** the 15% trim split, the 1% swap fee, the manual airdrops and the launch-token allocations are four different pools; the sIMD NAV already includes dripped rewards; no figure in this report adds them together.

### 10.3 Scenario valuation (12–18 months)
Method: a multiple of annualised external cash to the protocol, cross-checked against comparables the sources cite (Virtuals at ~$508M on 2026-09-25 per Bankless; Orbio at ~$60M on 2026-09-21 per MrCable; UMA's $2B peak per AdamOnFinance). All figures are illustrative ranges, not forecasts.
| Scenario | Assumptions | External cash/yr | Multiple | Implied FDV (7.096M) | Per IMD |
|---|---|---|---|---|---|
| Downside | Paid actions stall at ~250/day at 0.5 IMD; swap volume falls to $300k/day; no auto routing | ~$0.4M service + ~$1.1M fees | 10–15x on fees as a trading venue | $10M–$25M | $1.4–$3.5 |
| Base | 1,500 paid actions/day with tiered pricing averaging 2 IMD; 200 distinct payers/month; swap volume $1M/day; 1% fee routed to wall and bonding | ~$9.6M service + ~$3.7M fees | 3–8x | $40M–$120M | $5.6–$17 |
| Upside | Oracle and launchpad default for 300+ small protocols; 10,000 paid actions/day at 2 IMD; panel signatures shipped; bonding live | ~$64M service + fees | 5–10x on service | $300M–$600M | $42–$85 |
Price at pin $8.75 sits inside the base range. The asymmetry comes from the fact that the cost base (operator subscriptions) does not scale with revenue until vendors change quota policy. **[I, Appendix B.6]**

---

## 11. Roadmap and who benefits

**0–30 days (demand-building unless marked holder-benefit).**
1. Tiered pricing by action class: audit 5 IMD, launch 5 IMD, workflow 10 IMD, oracle 0.5–2 IMD by panel size. Demand-neutral, revenue 3–10x. *Holder benefit when combined with item 3.*
2. Publish per-seat EIP-712 signatures in oracle attestations (Section 6.3.1). Demand-building for serious consumers.
3. Automatic routing of the 1% swap fee: 50% wall, 50% bonding reserve, with an event. *Direct holder benefit; first non-discretionary cash loop.*
4. Hook owner to multisig plus timelock; dated audit engagement for POOL4. *Holder benefit (risk).*
5. A public refusal and latency ledger for the oracle. Demand-building.
6. Pilot rows from Section 8: one seat as a Taskmarket evaluator, one ACP provider wrapper, one Orbio agent paying Intake. Demand-building; zero cost.

**30–90 days.**
7. Ship the NFT-node payout contract for the accrued 4.5% (Case F is one design). *Holder benefit (seat holders).*
8. Open bonding at the documented $4 trigger or restate the trigger; publish the reserve's ETH and its inference spend. *Holder benefit if spend buys measurable throughput.*
9. Panel diversity fields and bonded re-ask (Section 6.3.2–3). Demand-building.
10. Oracle-gated hook template (Case G) and the Keeper's Piece game (Case A) as flagship experiments.
11. Automated research publishing to the archive with adversarial review closed on the five Stablecoin v4 reports. Demand-building (credibility).

**Later.**
12. Base and Solana deployment (announced 2026-10-06). Demand-building, with bridge-supply discipline (Section 4.1).
13. Reputation-backed credit (Case J) and compute attestations (Case P) once ERC-8004 history exceeds six months.
14. imdUSD only after paid revenue exceeds ~$50k/month; before that the mint is trivially gameable.

**Which milestones build repeat demand:** 1, 2, 5, 6, 9, 10, 11. **Which benefit IMD holders directly:** 3, 4, 7, 8 (and 1 only via 3). Burn-rate announcements benefit holders only pro rata and should not be treated as milestones.

---

## 12. Telemetry, dissent and corrections

**Runtime/model/reviewer telemetry.** This report was produced by one seat under the IMD control plane (job template `skill:research-report`, admitted 2026-10-09 05:50:01 UTC, listed as "executing" in the public jobs feed). The control plane records the seat's runtime and declared premium model; this author cannot read its own seat record from inside the task and therefore does not assert which vendor model ran. No independent reviewers, no 100-agent fan-out and no scheduler-level GPT-6.1 Sol or Opus 5.5 routing were involved; those models exist on only 31 of 874 seats. Any later verification verdict on this file certifies structure and scope, not the truth of its contents.

**Unresolved dissent.**
- *Supply:* Bankless says "one supply… bridgeable 1:1" and quotes ~7.1M; Dexscreener implies 4.14M. Both are consistent once Base is treated as home chain. If the Base contract were ever upgraded to mint, this reconciliation breaks. **[Q to team: is the Base contract's mint authority renounced?]**
- *Burn pace:* on-chain messages targeted ~25k IMD/day burned "once all LP is deployed" (2026-09-04, 09-11). Base supply fell from ~7.1M (09-25, Bankless) to 7,095,997 (10-09), i.e. a few thousand at most in two weeks, far below target. Either LP is not fully deployed, sells are bypassing the hooked pool, or burns are queued (441 IMD at the executor). **[U]**
- *Paid revenue:* imdUSD paper $1.6k/530 actions on 10-02; LastToSign 576.5 IMD/1,136 payments on 10-05; health 3,077 paid on 10-09. The 10-05 figure implies ~0.51 IMD per payment, consistent with the tariff; the 10-02 dollar figure implies $3/action at $6 IMD, also consistent. No contradiction, but no source gives distinct monthly payers directly.
- *Robinhood intake:* 7 refusals of 23 is a high refusal share on tiny numbers. **[U]**
- *Bankless framing:* the article carries sponsor placements and standard commission disclosures; it is a trade write-up, not research. Its numbers were cross-checked against chain where possible (supply, staking, floor).

**Correction log.**
1. Early draft used Dexscreener's $36.2M as market cap; corrected to $62.1M on global supply after reading the Base contract.
2. Early draft described sIMD as "25% of supply staked" (Bankless-era); corrected to 1,796,828 IMD = 43.3% of Ethereum supply, 25.3% of global.
3. Early draft treated `communitycoins.imd.fun/docs` as unavailable; mechanics were recovered from the app bundle and are marked as such.
4. The brief's address list is preserved exactly: Ethereum `0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7`, Robinhood `0x5f7bb59365ce557c26dbcaa4ee9d39a4b95b7127`, Base `0xff0c532fdb8cd566ae169c1cb157ff2bdc83e105`; all three were read on chain.

---

## Appendix A. Source coverage

| Source | Status | Retrieved | Notes |
|---|---|---|---|
| imd.fun/docs | Fetched (full, 103k chars) | 2026-10-09 | "Last checked against control plane 3b96b1cc on 2026-10-01; running now 2741bfd0" per page; live /version is c4d32abc |
| api.imd.fun/workers, /health, /version, /contributors, /jobs, /launches, /oracle/requests, /workflows, /schedules, /publications, /publications/counts, /feedback/batches | Fetched | 2026-10-09 05:50–06:05 UTC | JSON saved; list routes clamp at 500 |
| pool4.imd.fun/docs | Fetched | 2026-10-09 | Live metrics render client-side; parameters read from text |
| inference.imd.fun | Partial | 2026-10-09 | LiteLLM Swagger; /v1/models 401; openapi.json 1.26MB generic |
| github.com/Identity-md/awesome-imd, /research, /identitymd-skill-crafting | Fetched | 2026-10-09 | Commit dates not shown in rendered page |
| The Swamp reading room | Partial (bundle) | 2026-10-09 | Seven links; one not in the brief (0xNairolf explainer) |
| X: Bankless, nftimm, pegzeus, joechalom, AdamOnFinance, MrCable0x, shayonsengupta, ArtofConviction, LastToSign ×2 | Fetched via fxtwitter API | 2026-10-09 | Full article bodies for Bankless, nftimm, MrCable0x, joechalom, shayonsengupta |
| X: notwashed 2106085777407164654 | Restricted | 2026-10-09 | `PRIVATE_TWEET`; content unknown |
| X: @trumanpad | Not fetched | — | Profile pages not retrievable with this tooling |
| bankless.com article | Fetched (live) | 2026-10-09 | Published 2026-09-25, W. M. Peaster; Wayback snapshot blocked for this tooling |
| CoinMarketCap Academy (UMA whale) | Fetched | 2026-10-09 | March 2025 incident |
| The Defiant (Strategy bitcoin dispute) | Partial | 2026-10-09 | Body truncated; dispute ongoing at retrieval |
| docs.uma.xyz | Fetched | 2026-10-09 | 24h+24h, 65%, 99.8% optimistic |
| opensea.io/collection/identitymd | Fetched | 2026-10-09 | 1,999 items shown vs 2,000 on chain |
| etherscan.io/idm (0x200e…fb1) | Partial | 2026-10-09 | 25 of 42 messages rendered; page 2 returned 403 |
| docs.dxap.ai | Fetched | 2026-10-09 | |
| tapeout.net | Partial (bundle) | 2026-10-09 | Protocol PDF not fetched |
| claus.si/Hooks | Fetched (HTML) | 2026-10-09 | |
| hookr.fun/docs | Fetched | 2026-10-09 | Commit 8db7fc94 |
| communitycoins.imd.fun/docs | Unavailable (404); root bundle mined | 2026-10-09 | |
| docs.taskmarket.dev (llms.txt, fees-payments, evaluators, rewards) | Fetched | 2026-10-09 | /, /architecture, /network, /x402 404 |
| orbio.so/launchpad/whitepaper | Fetched | 2026-10-09 | Dated 25 Sept 2026 |
| virtuals.io/researches; os.virtuals.io/acp/concepts | Fetched | 2026-10-09 | Fee split from os.virtuals.io |
| si-md.xyz launchpad docs; si-md.xyz | Fetched | 2026-10-09 | |
| swarmbrain.fun/docs; swarmbrain-data data.json | Fetched | 2026-10-09 05:42 UTC data | |
| whitepaper.imdusd.com | Fetched (full in two parts) | 2026-10-09 | v1.1 dated 2026-10-02; metrics stale by design |
| zto.sites.imd.fun; pmdeth.fun docs; pepe2pepe.fun/guide; briefs.fun/docs/start; offsets.fun; pepesfamily.fun; imdember.com; trumanworld.live | Fetched (several JS-light) | 2026-10-09 | Pepes Family and Ember show little text |
| multicoin.capital Compute Capital Markets | Fetched | 2026-10-09 | Dated 2026-10-08 |
| Dexscreener token API; CoinGecko ETH price | Fetched | 2026-10-09 | IMD $8.75; ETH $2,488.34 |
| Chain reads: Ethereum, Base, Robinhood via public RPCs | Fetched | Blocks 26,152,879 / 52,367,909 / 83,927,218 | Selectors: totalSupply, name, symbol, owner, totalAssets, balanceOf, endpoint, oftVersion, token |

## Appendix B. Calculations

B.1 **Global supply and market cap.** Base totalSupply 7,095,997.49 = home supply. Ethereum 4,147,923.82 and Robinhood 52,607.58 are representations backed by Base-locked tokens. FDV = 7,095,997 × $8.75 = $62,089,974. Ethereum-only = $36,294,333 (matches Dexscreener $36.2M). Base free float = 7,095,997 − 4,147,924 − 52,608 = 2,895,466.

B.2 **Staking.** 1,796,828 / 4,147,924 = 43.3% of Ethereum supply; / 7,095,997 = 25.3% of global. sIMD exchange rate = 1,796,828.345 / 225,632,169,798.95 = 7.9635e-6 IMD per share.

B.3 **Inference cost equivalents.** Total tokens 189,558,963,616 / 985,597 attempts = 192,329 per attempt. Blended vendor rates from the imdUSD paper (OpenRouter, 2 Oct 2026): gpt-6-astra $2.662/M, claude-fable-5.1 $1.756/M, claude-sonnet-5 $0.486/M. Per attempt: $0.512 / $0.338 / $0.093. Per completed job (1,481,717 tokens): $3.94 / $2.60 / $0.72. Network lifetime at list: $504,606 (astra) / $332,866 (fable). Caveat: these ignore the cache-write premium the paper flags (writes 1.25x, reads 0.1x on Anthropic); cached input is 91.7% of tokens, so the true Claude-side figure could be ~40% higher.

B.4 **Operator income per seat.** 1,760 IMD airdrop / ~874 connected seats ≈ 2.0 IMD ≈ $17.6 at $8.75 (the 10-02 message does not state the eligible count; the division uses the connected count at pin). 8% seat allocation per launch / 874 seats = 0.00915% of 1e9 = 91,533 tokens per seat; at a 2,500 IMD opening cap (= $21,875 for 1e9 tokens) that is $2.00 per launch per seat at opening price.

B.5 **Paid revenue.** 3,077 paid orders × 0.5 IMD = 1,538.5 IMD = $13,462 at $8.75. Growth 10-05 to 10-09: (1,538.5 − 576.5) / 4 days = 240.5 IMD/day ≈ $2,104/day. Swap fee: 1% × $2,544,496 (24h volume, largest v4 pair) = $25,445/day, before splitting between ETH and IMD legs.

B.6 **Scenario arithmetic.** Base: 1,500 actions/day × 2 IMD × 365 × $8.75 = $9.58M; fees 1% × $1M × 365 = $3.65M. Upside: 10,000 × 2 × 365 × $8.75 = $63.9M. Downside: 250 × 0.5 × 365 × $8.75 = $0.40M; fees 1% × $0.3M × 365 = $1.10M. Multiples are judgemental and bracketed.

B.7 **Completion rates.** Jobs 478/500 = 95.6%. Workflows 111/154 = 72.1%. Launches 302/388 = 77.8%. Oracle attested 477/500 = 95.4%; disagreed 4.6%. Robinhood intake refusals 7/23 = 30.4%.

## Appendix C. Pinned addresses (all read or cited from primary docs)

Ethereum (chain 1): IMD `0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7`; NFT `0x0000ec93127baa929e58e97dd0095a2bfb38ec1d`; Intake `0x1397434cd35e8a9c8ac312a61d3a285eb31dea56`; IntakeDelivery `0xce0e6a670aa75e161d02aca3c7f00b94ca428ccb`; LaunchFactory `0x12c63b581d07093f6126bc02263c58f7eadaa96f`; ProjectFactory `0xff03410d0fe5fa8f7f59f743de35e333d9857120`; PoolInitializationGuard `0x784ff9a3ac5d88a30bfff6f7f2a270161fbe6000`; LaunchFees `0x12c9e1007262afac205567457f5826a9416a3863`; WorkRegistry `0xb6d0a187b050fa5bb0b87033a203f37becf4a775`; ERC-8004 adapter `0xde152afb7db5373f34876e1499fbd893a82dd336`; POOL4 hook `0xc6c965bd164c483e87d0b550671798e9a3602840`; sIMD `0x9efa934d9fad4ae28c998a40195646b965a97247`; RewardDistributor `0x9046739E1535B40EfBe6AB3f45d0024b690eCA30`; RewardDripper `0xe6D3De6daEAf327fCA42745f1998FcD989e00884`; BurnExecutor `0xe29386719C155B6847aD5a4E97C6674f10ffc750`; messages `0x200e710acaa6a93bbc77146026328c40f1d60fb1`; oracle attester `0x5598aa9146215bc13eb26f2c692ad1461fd32982`; fee recipient `0x3f252e859a277a86a3967c11d4e054b2f07a1f22`; intake payee `0x4e0fa57bde726079356537e2f34d671e9f41adbc`; launch deployer `0xcecc29b037f5064fcdf45a5c318f132ef76aa551`; token/hook owner `0x047f606fd5b2baa5f5c6c4ab8958e45cb6b054b7`.
Robinhood Chain (4663): IMD `0x5f7bb59365ce557c26dbcaa4ee9d39a4b95b7127`; LaunchFactory `0xa25b02a1e93903b790e6aaf7da1b8b8d50294645`; ProjectFactory `0x9c9d2fcb75c2c132c0ac0c42df3819a42347265e`; LaunchFees `0xf053525ffe8f8d8973339e36ee8d455690fb73cb`; PoolManager `0x8366a39cc670b4001a1121b8f6a443a643e40951`.
Base (8453): IMD home contract (name still "Fren Pet") `0xff0c532fdb8cd566ae169c1cb157ff2bdc83e105`.
Third parties: SIMD `0xbb0c1f82a2ea0253ea3d91c2f05caded82133415`; SIMD creator fee splitter `0x1bf885b464c42ced51750108399f7a0b43ed718e`; ZTO `0xd782bdea4ef02a0bd391eb9089470c8080f0a68e`; Hookr root `0xb3cA29cF721380CEe8b8e4755F3865Ebc68Fe8cC`; Swarmbrain account `0x60310BdC4814345a454af0A79d7F5480E0Babc4e`; DREAMS `0x176383016BB310C9f1C180DC6729d5E28104e602`.

*End of report.*
