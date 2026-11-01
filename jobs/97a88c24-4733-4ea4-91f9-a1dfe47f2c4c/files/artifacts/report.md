# STRATOKS — Game Economy and Token Blueprint (Implementation Report)

Scope: specification and recommendations only. Nothing was deployed, no transactions were sent, no wallet secrets were used, and there were no writes to the live server.
Repository: https://github.com/kilicsln/stratoks at baseline `6304eaa8c3e5fa1cadbdc928898669aa5d4a9877` (commit dated 2026‑11‑01 12:53 UTC, 56 commits in history).
Live reference: https://stratoks.2-29-11-211.sslip.io, read only on 2026‑11‑01 through public GET endpoints.

**Evidence labels used throughout**
- **[F]** Fact: read in source or docs at the baseline commit, or observed on a live GET. The path is given.
- **[M]** Measured: numbers from the repo's own recorded runs, or from my live GET.
- **[I]** Inference: my reading of the evidence.
- **[A]** Assumption: an illustrative number, not measured.
- **[OD]** Owner decision: this report recommends but does not set it.
- **[U]** Unknown or inaccessible.

---

## 0. Sources and what was not accessible

| Source | Status |
|---|---|
| `docs/operations/LOCAL-MODEL-PILOT.md` | Read in full **[F]** |
| `server/src/expanse/{engine,chains,capabilities,terrain,persist,server,visitor-auth,cognition}.js`, `server/src/{world,wallet}.js`, `shared/stockpiles.js` | Read. The parts relevant to the economy were inspected; not every line was audited **[F]** |
| `docs/operations/{STORYBOOK,LOCAL-MODEL}-ROLLOUT-2026-11-01.md`, `server/README.md` | Read for the ledger offset, population and cutover facts **[F]** |
| Live `/healthz`, `/api/expanse/info`, `/api/expanse/cognition`, `/api/expanse/discoveries`, `/api/expanse/minimap`, `/api/auth/config` | Fetched once each **[M]** |
| VPS filesystem, snapshots, backups, `/opt/stratoks/compose.yml`, Ollama logs | **Inaccessible [U]**. Claims about them come only from the repo docs |
| The live world's per-unit provenance (where the +234 wood / +192 stone came from) | **Not available [U]**. No endpoint exposes it |
| IMD token: chain, contract, supply, governance | **Unknown [U]**. Nothing in the repo specifies it |
| Current L1/L2 gas prices, stablecoin availability per L2 | **Not measured in this run [U]**. The figures in §4 are assumptions |
| Legal or regulatory review of the token | **Not performed [U]**. Required before any sale or mainnet launch **[OD]** |

---

## 1. Source audit

### 1.1 Implemented [F]
- **Authoritative world server.** `server/src/expanse/server.js` ticks every `TICK_MS=1000` ms (`deploy/env.example:15`). Its only HTTP surface is read-only GETs: `/api/expanse/{frame,info,view,minimap,creature/:id,discoveries,cognition}` and `/healthz` (lines 42‑49).
- **Simulation** (`server/src/expanse/engine.js`, schema 5):
  - Needs: hunger, thirst, warmth, energy, health.
  - Reproduction and death: `lifecycle()` at line 1323 and `birth()`. Dead residents' inventories drop into ground piles, so items stay in the world.
  - Memories (`mind.known`, `mind.shelters`), relationships and leadership (an observed pattern, not an assigned role).
  - Learned signalling (`agency.js`) and a per-resident learned outcome model.
  - Recipes, `engine.js:20`: `flint+stick→hand_axe`, `stick+stone→stone_club`, `fiber+stick→bundle`, `bundle+fiber→fish_line`.
  - Tool wear, `engine.js:23`: fish_line 6 uses, hand_axe 40, stone_club 20.
  - Biome structures, `engine.js:25‑29`: temperate `timber_home` {wood 4, stone 2}, arid `desert_shade` {fiber 3, stick 2, stone 1}, cold `snow_refuge` {stone 4, wood 2}, coast `coast_hut` {wood 3, fiber 2}.
  - Crops (`capabilities.js` CROPS: berry, cactus_fruit), cooking and fires.
- **Biomes.** `terrain.js:16` defines temperate, arid, cold and coast. Coast includes "open sea with islands… wadeable shallows" (`terrain.js:80`). Forest is a tile type inside temperate, not a separate biome.
- **Migration and exploration.** `chains.js:152‑171` tracks explore `started/found/returned/settled/failed` with origin, farthest distance and ticks. This is the hook for a verified expedition outcome.
- **Discoveries.** `engine.discover()` (line 1166) records `{tick, what, by, firstInWorld, selfFound}`, visible at `/api/expanse/discoveries`.
- **Conservation ledger.** `holdings()` and `expectedHoldings(totals)` (`engine.js:1378,1420`). Seeded runs report exact ledgers (`docs/chains/VALIDATION.md`, `docs/maintenance/revision/VALIDATION.md`).
- **Durable persistence.** `persist.js` writes atomic gzip snapshots with a sha256 manifest, keeps generations for rollback, provides backup and restore, and runs forward-only migrations 1→5. It refuses newer schemas (line 96).
- **Visitor wallet sign-in.** `server/src/expanse/visitor-auth.js` verifies EIP‑191 signatures with no private keys (`server/src/wallet.js`). Live `/api/auth/config` returns `chains:[1]`, `transport:"memory-bearer"`, `sessionsSurviveRestart:false` **[M]**. Role is `visitor` only.
- **Legacy intervention ledger.** `server/src/world.js:437` holds idempotent intervention records with `payment: null`. `server/README.md:9` says there are no tokens, NFTs, contracts, pools or payments in this phase.
- **Local Qwen adviser.** `cognition.js` plus `LOCAL-MODEL-PILOT.md`:
  - At most 3 adult residents, one inference per minute.
  - A valid suggestion adds +0.5 utility to an existing candidate only.
  - Replies expire after 120 ticks; container limit is 2 GiB.
  - Live: `pilots:[6941,6996,7180]`, 58 requested, 56 accepted, 1 rejected, 1 failed, last latency 23.3 s **[M]**.

### 1.2 Incomplete [F/I]
- **Ground and store accumulation is unbounded in behaviour.** `STORYBOOK-ROLLOUT-2026-11-01.md:19` says plainly: "This does NOT establish bounded ground accumulation." Seed 7 reached 134 piles by tick 9000 **[M, repo]**.
  - Live: `stored: 7153` units, 299 shelters (208 standing, 91 ruins), 56 unfinished sites — for **17 residents** **[M]**.
  - [I] Stock per resident is very large and does not reflect present productive capacity. Most of it is inherited from dead residents and abandoned stores.
- **Historical ledger offset.** The live world carries **+234 wood and +192 stone** relative to its historical counters (`STORYBOOK-ROLLOUT-2026-11-01.md:27`, `LOCAL-MODEL-ROLLOUT-2026-11-01.md:12`). It is preserved and documented, not explained, and its per-unit origin is **[U]**.
- **Population collapse in progress.**
  - [M, repo] 181 residents at cutover tick 433110 → 44 at tick 437871.
  - [M, live] 17 at tick 442032 (temperate 11, arid 1, cold 5, coast 0). Lifetime births 6612, deaths 6653.
  - [I] Extinction is plausible within days at this rate. The repo has no recovery or reseeding policy for the live world.
- **Visitor sessions** are in memory and lost on restart; mainnet is the only chain allowed.
- **Adviser** has no controlled evaluation. The pilot doc states no improvement is established.

### 1.3 Absent [F, by search of `server/src`]
- Player accounts with inventories.
- Player-owned infrastructure.
- Expeditions, a market or orders, settlement, escrow or refunds.
- Token, vesting or treasury contracts.
- Any write API for players.
- Chain indexer or reconciliation.
- A test economy.

The only player-adjacent write paths are the legacy developer interventions (`server/src/world.js`, `actions.js`).

### 1.4 Module mapping (proposed)
| New capability | Where it attaches |
|---|---|
| Commons/player ledger split | New `server/src/economy/ledger.js`. The `engine.js` world ledger stays the **commons** ledger, untouched |
| Player installations as world objects | New `economy/installations.js`, placed through additive schema‑6 fields in chunk state (`persist.js` migration 5→6) |
| Expedition caches | Render as ordinary stores (`STORABLE`, `storeCapacity: 40`). Residents use the existing `retrieve` affordance |
| Outcome verification | Subscribe to the `chains.js` explore log and `engine.discover()` events |
| Orders, settlement and indexer | New `economy/market.js` and `economy/chainwatch.js`. Separate process; it must never block ticks |
| API | New `/api/economy/*` behind `visitor-auth.js` sessions (upgraded to persistent sessions) |
| UI | `web/src/expanse/` with new panels for Expedition, Workshop, Market and History |

### 1.5 Release blockers
- **B1.** Population collapse (17 live). There must be no economy that depends on residents until a stable or recovering population is demonstrated.
- **B2.** Unexplained ledger offset and the size of the accumulated stock. These need a forensic report before any value is assigned.
- **B3.** Unbounded pile and store growth.
- **B4.** No persistent auth sessions and no account model.
- **B5.** No contracts, no audit, no testnet.
- **B6.** Host budget: 2 CPU / ~4 GB shared with Ollama (`LOCAL-MODEL-PILOT.md`). The indexer and database must fit, or move to a separate host **[OD]**.
- **B7.** Legal review **[U/OD]**.

### 1.6 Non-destructive migration
1. Take a full snapshot backup with `deploy/backup.sh` and keep an offsite copy.
2. Schema 5→6 adds only **new** fields: `economy:{epoch, installations:[], caches:[]}` and `provenance:"legacy"` on every existing stock.
3. **Every existing unit is tagged `legacy-commons` and is permanently non-redeemable.** It can never enter a player inventory. Residents keep using it exactly as today.
4. Player ledgers start empty. Value only enters through §2 rules and only from economy epoch 1 onward.
5. Rehearse on a copied volume, following the pattern in the rollout docs: compare normalized state, keep the old image, and roll back by restoring the previous generation.
6. The world ID, residents, memories, relationships, brains and backups stay unchanged.

---

## 2. The initial playable loop

**Time:** 1 tick = 1 s; 1 day = 1200 ticks (`dayLength`). The economy runs on **testnet/valueless first** (see §8).

### 2.1 Two ledgers (survival protection)
- **Commons ledger [F, existing].** Nodes, ground piles, resident inventories, shelter stores and crops. Residents survive on it.
  - Players can **donate into** it.
  - Players can **never withdraw** from it: no API path, enforced by a type-level separation and tests.
- **Player ledger [new].** Account-bound offchain balances of player goods, with an append-only journal.
  - Goods come only from player installations, crafting, purchases and verified-outcome records.
- **Commons floor.** An installation that harvests a world node on its plot (woodlot, quarry, garden) may harvest only if the chunk's commons food plus that node keeps:
  `reserve_b = residents_in_biome_b × 3 days × 1.5 food units/day` [A].
  It also must never take a node below 50 % of its maximum. A failed check pauses harvest; it does not take from residents.

### 2.2 Three connected production chains
Inputs and outputs use existing item names where possible. Jobs run in the player's installation, not by resident labour.

| Chain | Biome need | Installation (plot) | Step | Time | In → Out | Failure |
|---|---|---|---|---|---|---|
| A Cordage | Coast/islands need nets and lines | Fiber Bed (temperate/coast grass) | harvest | 300 ticks | plot node → 4 fiber | node <50 % or floor → paused |
| | | Rope Walk | twist | 60 | 3 fiber → 1 cordage | none (deterministic) |
| | | Rope Walk | net | 120 | 2 cordage + 1 stick → **Shore Net** (6 uses) | inputs stay reserved until done |
| B Timber/Stone | Cold needs insulated warmth caches | Woodlot (forest) / Quarry (cold, arid) | harvest | 300 | → 3 wood / 2 stone (+1 stick per wood harvest) | as above |
| | | Lodge Workshop | cache | 120 | 2 wood + 2 stone → **Cold Cache** (warmth store; 1 per cold expedition) | |
| C Water | Arid needs water | Cactus Garden (arid; mirrors CROPS cactus_fruit: 8 checks × 50 = 400 ticks, yield 2) | harvest | 400 | → 2 cactus_fruit | withers after 8 stress checks (seed lost) |
| | | Lodge Workshop | gourd | 80 | 2 cactus_fruit + 1 fiber → **Water Gourd** | |

The chains connect: chain A's fiber is needed in chain C, and chain B's sticks are needed in chain A. Every recipe is server-side and deterministic. The LLM plays no part.

### 2.3 The loop: prepare → explore → verify → craft → sell or use
1. **Prepare.** Player P owns a Waystation (a store object) at the frontier. P loads an **Expedition Cache** with a biome kit (for example, cold: 1 Cold Cache + 4 cooked food bought from players) and sets a target chunk the world has not yet explored.
   - Loading **reserves** the items in P's ledger as `state=staged`.
   - P can withdraw them freely until the first resident retrieval.
2. **Autonomous exploration.** The cache appears to residents as an ordinary stocked store. Whether any resident retrieves from it, and where it then goes, is decided by its own circuit and planner.
   - The server never issues commands. Adviser nudges stay capped at +0.5, three pilots, and never mention caches.
   - Each retrieved unit moves **one way** to the commons, with provenance `cache:<id>` (extending `mind.prov` and `foodSources`).
3. **Verified outcome.** A *Survey Record* is created only when all of these hold:
   - an explore chain event `found`, `returned` or `settled` (`chains.js:171`);
   - the resident is carrying or has consumed ≥1 unit with `cache:<id>` provenance;
   - it entered a chunk with no prior visit in this economy epoch.
   The record key is `(worldId, epoch, cx, cy)`.
4. **Craft.** P combines Survey Record + 2 cordage + 1 wood (60 ticks) into a **Route Chart (cx,cy)**. Each chunk issues at most 3 charts, which are its plot rights. These can only be minted from the record.
5. **Buy or use.** Player Q buys the chart on the market and consumes it to place a Quarry or Garden in chunk (cx,cy). That installation feeds chains B and C. Q can also buy Shore Nets and Water Gourds for their own caches.

**Rules for the loop**
- **Ownership.** Installations and player goods belong to accounts. Residents, commons stock and world nodes belong to nobody.
- **Consumption.**
  - Nets: 6 uses. Gourds and Cold Caches: consumed once when a resident uses them.
  - Charts: burned when used to place an installation.
  - Installations decay 0.5 %/day unless maintained with 1 wood/day [A].
- **Discovery uniqueness and duplicate claims.**
  - Each key is unique in the database.
  - The first record is ordered by (tick, event seq), so it is deterministic.
  - Several sponsors' provisions on the same trip: credit is split pro rata by provisioned units consumed.
  - A later claim returns `409 already_recorded` with the winning record ID.
  - Every claim carries an idempotency key, and a replay returns the original result.
- **Failure.**
  - If the resident dies, provisions drop into commons piles (existing `lifecycle`) and P gets a receipt "expedition failed: death at tick t".
  - If the cache goes unused for 20 000 ticks [A], staged items return to P. Food loses 25 % [A, spoilage].
- **Recovery.** Consumed provisions are not refunded: they fed real residents. The UI must say this before loading.
- **No resident-free fallback.** If population is 0, no records can be created; see the extinction scenario in §5.

---

## 3. Legitimate player income (who pays, and why)
| Source | Payer | Why they pay | Guards |
|---|---|---|---|
| Useful goods (nets, gourds, caches, cordage, food) | Another player | Needed for their own expeditions and installations | Goods are consumed in use. Self-trades between linked accounts are excluded from any metric. No volume rewards |
| Route Charts (validated discoveries) | Players wanting plots | Plot rights in newly surveyed chunks are scarce (3 per chunk) | Uniqueness per key; issuance only from verified records |
| Discovery bounty (optional) | Reward budget (treasury, capped) | Funds frontier exploration | Paid per unique key, not per account. Fixed weekly cap. 0 when the budget is exhausted |
| Creator cosmetics (waystation skins, banners; never residents' bodies) | Players | Aesthetic expression | Moderation review; creator share 80 % [A]; no gameplay power |
| Funded work orders ("deliver 20 Water Gourds to waystation X by day D") | Requesting player or a funded sponsor | Wants goods without producing them | Full escrow at posting; paid on server-verified delivery; refunded on expiry |

**Excluded:**
- Rewards for trading volume, number of wallets, referrals or logins.
- Liquidity mining beyond the funded budget.
- Lotteries, loot boxes or randomized cash prizes.
- Unlimited farming. Every output needs a finite plot node, time and inputs, and the number of plots per account is capped [A: 6].

**Disasters.** Paid disasters are **not recommended**. If a world event (storm, drought) exists, it is world-driven and seed-determined. It can only damage installations to a maintenance-repairable state; it never deletes purchased goods and is never purchasable against another player's property.

---

## 4. Token, chain and fee recommendations (recommendations, not approved parameters)

### 4.1 Chain [OD]
Mainnet is evaluated here as a reference point; no new chain is chosen silently.

**Assumptions [A]**
- A market settlement transaction uses about 120k gas; an ERC‑20 transfer about 50k.
- ETH price is $3,000.
- These are not live figures; check current fees before deciding.

**Settlement cost per trade**
- At 1 gwei: 120k gas ≈ **$0.36**. At 20 gwei: ≈ **$7.20**.
- For a $3 trade, a 5 % fee is $0.15, which is **smaller than gas** at either price.

**Assessment**
- [I] Ethereum mainnet is unsuitable for per-trade settlement of small items. It would only work with offchain batching, which is a larger trust burden.
- An EVM L2 typically costs cents or less per transaction [A, unverified this run]. That is economically suitable, but it brings sequencer and bridge trust assumptions.
- Today's sign-in is chain 1 only (`/api/auth/config`).

**Recommendation:** choose one established EVM L2 as the owner's choice. Keep mainnet sign-in, and add the L2 chain ID only after the owner decides.

### 4.2 Settlement currency [OD]
- **Recommended:** a single gameplay settlement currency, **STRATOKS on the chosen L2**. Prices are fixed in STRATOKS at listing and shown with an informational fiat estimate.
- **Alternative:** a stablecoin. It protects players from volatility but leaves STRATOKS with little transactional role. Owner choice.
- **IMD's role:** optional. A buyer holding IMD may route IMD→STRATOKS through a DEX swap inside the same purchase transaction. Only one payment reaches the seller, and the seller receives STRATOKS. IMD is never required, and no fee is charged in both currencies.
- IMD's contract and chain are **[U]**. If IMD is on another chain, this route needs a bridge and is deferred.

### 4.3 Supply, allocation and vesting (illustrative)
- Fixed supply **1,000,000,000 STRATOKS**.
- All tokens minted once at genesis into vesting, treasury and liquidity contracts.
- The minter role is renounced in the same deployment script.

| Bucket | % | Vesting / control |
|---|---|---|
| Player reward budget | 20 | Emission contract. Y1 80M, Y2 60M, Y3 40M, Y4 20M. Hard weekly caps, Y1 ≈ 1.54M/week |
| Treasury | 30 | Multisig + 48 h timelock. Spending is public: audits, hosting, security bounties, art grants |
| Liquidity | 10 | Paired with **owner-supplied** quote asset. See below |
| Team/operator | 15 | 12-month cliff, then 36-month linear |
| Contributors (IMD network) | 10 | 6-month cliff, 24-month linear |
| Creator grants | 10 | Released per approved grant from the treasury multisig |
| Locked reserve | 5 | 24-month lock; release only by timelocked governance |

**Liquidity example:** 100M tokens + $20,000 quote asset gives an implied initial price of $0.0002 and a fully diluted value of $200k. **These are not approved values.**

Burns, team allocations and treasury balances are **not revenue**.

### 4.4 Fees (hypotheses)
- **Marketplace fee:** f = 5 % **(hypothesis)**, to be tested against 2 % and 8 % on testnet. Fee revenue = f × V_settled, where V_settled excludes cancelled or refunded orders.
- **Work-order fee:** 5 % (hypothesis) of the escrow paid out.
- **Cosmetics:** operator takes 20 % [A].
- **Accounting:**
  - Gross revenue R = fees + cosmetics share.
  - Costs C = hosting + RPC + audit amortization + support + gas sponsorship.
  - Profit = R − C. Neither players nor the operator are guaranteed profit.

---

## 5. Cash-flow and resource-flow tables (ALL ILLUSTRATIVE [A]; nothing measured except where marked [M])

### 5.1 Monthly operator cash flow (USD equivalent; 4.33 weeks/month)
| Line | Low | Base | High |
|---|---|---|---|
| Trades/week × avg value | 200 × $2 | 3,000 × $3 | 40,000 × $4 |
| Settled volume V | 1,732 | 38,970 | 692,800 |
| Market fee 5 % | 86.6 | 1,948.5 | 34,640 |
| Cosmetics sales → 20 % op. share | 100 → 20 | 3,000 → 600 | 30,000 → 6,000 |
| Work orders → 5 % | 200 → 10 | 5,000 → 250 | 50,000 → 2,500 |
| **Gross revenue R** | **116.6** | **2,798.5** | **43,140** |
| Hosting/RPC | 30 | 150 | 1,500 |
| Audit $30k ÷ 24 months | 1,250 | 1,250 | 1,250 |
| Support/moderation | 0 (owner time unpaid) | 1,000 | 8,000 |
| Gas sponsorship (L2) | 0 | 100 | 1,000 |
| **Costs C** | 1,280 | 2,500 | 11,750 |
| **Profit R − C** | **−1,163.4** | **+298.5** | **+31,390** |

### 5.2 Stress scenarios
Each scenario is applied to the Base row.

| Scenario | Mechanism | Effect |
|---|---|---|
| Token price −80 %, prices sticky in token | R in USD × 0.2 | 559.7 − 2,500 = **−1,940.3/mo**. Treasury must cover costs or fees must be repriced |
| No new buyers | Only existing holders trade; reward recipients sell into a fixed pool | Volume falls toward Low. **Rule:** emissions pause automatically if pool depth < 2 × weekly emission value [A] |
| Reward budget exhausted | Bounty = 0 | Income only from goods, charts, cosmetics and work orders. R unchanged (rewards were never revenue); player income falls by the former bounty share |
| Bot farming (1,000 accounts) | Bounty is per unique chunk key and capped weekly; plots are capped per account and every output needs time and inputs | Total payout unchanged (≤ weekly cap). Bots only compete; per-account caps and the cache-sponsorship cost bound it. Sybil detection is still needed for cosmetics and voting |
| Stock hoarding | One player holds all gourds | Prices rise. Arid expeditions pause and residents are unaffected, because commons food is not tradable. Inventory caps [A: 200 units/item/account] and decay limit hoarding |
| World extinction (pop 0) | No verified outcomes can occur | Survey and Route Chart issuance stop. Existing goods keep their in-game use value only for installations. The UI must show "no residents". Recovery needs an owner-approved, publicly logged founder repopulation as a world event, **never paid and never minting player value** |
| Recovery | Population re-grows | Issuance resumes in a new economy epoch; earlier records stay valid |

### 5.3 Resource flow per player-day (Base, one of each installation [A])
| Flow | Wood | Stone | Fiber | Cactus | Product |
|---|---|---|---|---|---|
| Harvest (1200 ticks/day ÷ 300 = 4 cycles/day; ÷ 400 = 3 for cactus) | +12 | +8 | +16 | +6 | sticks +4 |
| Cold Cache ×2 | −4 | −4 | | | +2 Cold Cache |
| Gourd ×3 | | | −3 | −6 | +3 Water Gourd |
| Cordage ×4 → Net ×2 | | | −12 | | +2 Shore Net (−2 sticks) |
| Maintenance | −1 | | | | |
| **Net surplus to sell** | +7 | +4 | +1 | 0 | sticks +2 |

Commons flows are measured only by the existing ledger. Live counts at tick 442032 **[M]**: stored 7,153, fishCaught 4,871, births 6,612, deaths 6,653.

---

## 6. Onchain/offchain boundary and trust

| Element | Location | Notes |
|---|---|---|
| STRATOKS ERC‑20, vesting, emission caps, treasury multisig/timelock | Onchain (L2) | Fixed supply, no mint after genesis |
| Market escrow `Settlement.sol` | Onchain | Buyer deposits STRATOKS against `orderId`. Release needs a server delivery attestation (EIP‑712), otherwise the buyer can refund after a timeout |
| Player goods, installations, records, charts | **Offchain**, authoritative server DB with an append-only journal | Simulation-coupled; NFTs not needed (see below) |
| Cosmetics | Offchain by default; an optional ERC‑1155 is justified only if creators need portability [OD] | |

**Atomicity.**
1. The server **reserves** the item (`state=reserved`, 30-minute TTL [A]) and returns a signed order quote: `{orderId, item, price, expiry, nonce}`.
2. The buyer calls `escrow(orderId)`.
3. After N L2 confirmations [A: finalized], the indexer sees the deposit and transfers the item in one DB transaction while signing a delivery attestation.
4. Anyone may submit the attestation to release funds to the seller minus the fee.
5. If there is no attestation by the deadline, `refund(orderId)` returns the funds.

Item delivery and fund release cannot be one atomic transaction across offchain state. The escrow plus timeout bounds the loss to the server failing to deliver, and in that case the buyer can always reclaim.

**Integrity rules**
- **Replay and duplicates.** `orderId` is used once onchain and is unique in the DB. Quotes are nonce-bound and expire. Client requests carry idempotency keys, following the pattern of the existing intervention IDs (`server/src/world.js`).
- **Reorgs.** Deliver only after finality. On a detected reorg before finality, un-deliver a reserved item; finalized-only processing avoids this case.
- **Crash reconciliation.** On start, rescan from the last finalized block checkpoint. For every escrow without a delivery: deliver if the item is still reserved, or let the refund path run. A journal-versus-chain diff job runs hourly and halts the market on any mismatch.
- **Cancellation.** The seller can cancel only reservations that have not been escrowed. Escrowed orders can only be completed or refunded.
- **Restricted issuance.**
  - Only deterministic server rules create player goods.
  - The attestation key is held by the operator, ideally in an HSM, and is limited to delivery attestations. It can never mint tokens.
  - The **LLM has no access to the economy module and cannot authorize funds or create assets.** This is enforced by import boundaries and tests.
- **Server unavailable.** All escrows stay refundable. Tokens stay with their holders. Offchain goods are frozen, and their balances are protected by the snapshot and backup regime (`persist.js`).
- **Honest trust statement.** Players must trust the operator for offchain items and world rules. Onchain contracts guarantee only token custody, refunds and caps.

**Are NFTs needed?**
- Resource goods: **no**. They are fungible and simulation-bound.
- Installations: **no**. They are tied to world state.
- Route Charts: **no**. They are offchain, unique and consumed.
- Residents: **never**. They are not assets.
- Cosmetics: optional.

---

## 7. UX and art requirements
- Keep the existing isometric renderer (`web/src/expanse/worldRenderer.ts`, `ART-DIRECTION.md`) and the original yellow residents. New sprites must be original; none may be copied.
- Each of the four biomes needs distinct ground, flora and structures. These already exist per `STRUCTURES` and must extend to the new installations, which need a readable working or idle state.
- Use exact pile size classes (`shared/stockpiles.js:pileSizeClass`) and aggregate by zoom level so 7k units do not carpet the map. **No repeated log or house tiling.**
- Every displayed counter must come from an API field. Previews are labelled "recorded" or "preview" (the existing storybook practice).
- **Panels:**
  - Expedition: kit checklist per biome, staged items, live status from real explore events, failure receipts.
  - Workshop: job queue with timers and reserved inputs.
  - Market: listings, quote expiry, escrow state machine.
  - History: journal entries with transaction hashes and refund buttons.
- Viewing stays walletless. A wallet is requested only at purchase.

---

## 8. Dependency-ordered backlog (each brief < 5,000 characters)

**J0 — Forensics: ledger offset and accumulation (blocker B2/B3)**
- Scope: read-only analysis of a copied live snapshot.
  - Attribute the +234 wood and +192 stone to counters and migrations.
  - Report stock by age, origin and owner state.
  - Measure pile growth and its causes.
- Interface: `server/bin/economy-forensics.js --snapshot <path> --out report.json`.
- Acceptance: the report reproduces the documented offsets exactly, and makes no writes (hash of input unchanged).
- Rollback: none needed (read only).

**J1 — Population stability study (B1)**
- Scope: seeded control runs from a copy of the live state, measuring time to extinction. Propose engine fixes reviewed against resident autonomy.
- Acceptance: 10 seeds × 50k ticks from the copy, with documented median survival. Fixes adopted only if they do not regress the 270-test backend suite.
- Rollback: previous image plus snapshot generation.

**J2 — Schema 6 and commons/player ledger split**
- Scope: additive migration that tags existing stock `legacy-commons`; new `economy/ledger.js` with an append-only journal.
- Acceptance:
  - normalized v5 fields are byte-equal after migration;
  - property test: no API path withdraws from the commons;
  - the commons-floor check is tested per biome.
- Rollback: restore the previous generation; the v5 server refuses v6 (`persist.js:96`).

**J3 — Installations, recipes and caches (valueless test economy, internal points only)**
- Scope: chains A, B and C; caches as stores; provenance tag `cache:<id>`.
- Acceptance:
  - exact conservation in both ledgers over 3 seeds × 9k ticks;
  - zero commands issued to residents;
  - unchanged results when the economy is off.
- Rollback: feature flag `ECONOMY_ENABLED=false`.

**J4 — Verified outcomes, records and charts**
- Scope: Survey Record from explore and provenance events; unique keys; pro-rata split; 409 duplicates.
- Acceptance: concurrent duplicate claims produce exactly one record; a replay returns the same response.
- Rollback: flag off; records retained read-only.

**J5 — Accounts and persistent sessions**
- Scope: persist visitor sessions or switch to short JWTs bound to world ID; per-account caps.
- Acceptance: sessions survive a restart test; cross-origin protections pass the existing browser tests.
- Rollback: revert to memory sessions.

**J6 — Offchain market (valueless points)**
- Scope: reservation with TTL, quotes, cancel and refund, history.
- Acceptance: no double-sell under 100 concurrent buyers; reconciliation after a forced crash.
- Rollback: flag off; open reservations released.

**J7 — Contracts on testnet**
- Scope: ERC‑20 fixed supply, vesting, emission caps, timelock multisig treasury, `Settlement.sol` escrow with attestation, refund and timeout.
- Acceptance: Foundry tests including fuzzing for replay, double release and refund after release; minter renounced; testnet deploy script with no secrets in the repo.
- Rollback: redeploy (testnet).

**J8 — Indexer and reconciliation on testnet**
- Scope: `economy/chainwatch.js` with finality-only processing, a checkpoint, an hourly diff and a market halt.
- Acceptance: simulated reorg, crash and RPC outage tests; memory < 300 MB on ARM64.
- Rollback: halt market; escrows refundable.

**J9 — UX panels**
- Scope: §7.
- Acceptance: Chromium checks at 1440/390 px; every counter traced to an API field.
- Rollback: hide panels.

**J10 — Independent security and economic review, then fixes**
- Scope: external audit of J7/J8; economic review of the §5 assumptions against testnet measurements.
- Acceptance: all high and medium findings fixed and re-reviewed.

**J11 — Owner-operated deployment artifacts**
- Scope: `deploy/economy/compose.yml` (world, economy, indexer, Postgres or SQLite), backup and restore extension, runbook.
- IMD hosts only the static client (`server/README.md:9`), so the backend runs on the owner's VPS.
- Acceptance: dry-run on a copied volume.
- Rollback: previous compose file and volume snapshot.

**J12 — Gated mainnet (or chosen L2 production) rollout**
- Gate: J0–J11 done, owner approvals (§9), legal review.
- Scope:
  - Phase 1: market fee 0 and caps at 10 %.
  - Phase 2: raise caps after 30 days without reconciliation mismatches.
- Kill switch: market halt with refunds kept open.

---

## 9. Owner decisions and open questions
- **[OD]** L2 choice.
- **[OD]** STRATOKS versus stablecoin settlement.
- **[OD]** Supply, allocation and liquidity quote-asset amount.
- **[OD]** Fee level after testnet.
- **[OD]** Whether a discovery bounty exists.
- **[OD]** Founder repopulation policy if extinction occurs.
- **[OD]** Hosting split versus the 4 GB VPS.
- **[U]** IMD token details.
- **[U]** Origin of the ledger offset (J0).
- **[U]** Live gas prices.
- **[U]** Whether the live population (17) survives.
- **[U]** Legal classification of the token.
