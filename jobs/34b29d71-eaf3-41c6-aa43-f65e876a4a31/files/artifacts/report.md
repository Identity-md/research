# $EMBER as a Living, Self-Sustaining, AI-Driven Economic Organism
## Research, Architecture, Economics, Threat Model and V1 Plan for IMD Ember World and the Genesis PEPE Ecosystem

**Report date:** 5–6 October 2026 (information current as of the research date; see §0.3 for what could and could not be checked).
**Scope:** Research and design only. **No Mainnet deployment is proposed or performed. No token is launched by this report.** Nothing here is financial advice.

---

## 0. How to read this report

### 0.1 Labels used throughout

| Label | Meaning |
|---|---|
| **[FACT]** | Verified from a primary or official source on the research date, with the source cited in §16. |
| **[ASSUMPTION]** | A working premise used for modelling or design. Not verified. Replace with real data before acting on it. |
| **[REC]** | A recommendation from this report. |
| **[EXPERIMENTAL]** | An idea worth prototyping on Sepolia but not ready for V1 commitment. |
| **[OPEN]** | Unanswered question that blocks or shapes a decision. |

### 0.2 The core question

> How can $EMBER become a living, self-sustaining, AI-driven economic organism that continuously funds, builds, evaluates and improves IMD Ember World and the Genesis PEPE ecosystem, while preserving strict financial and security boundaries?

**Short answer (expanded in §1–§12):** Keep the EMBER ERC-20 small, immutable and boring. Put the "life" in a ring of modules around it: a **World Brain** that observes and proposes; **World Build Epochs** in which several Identity.md Swarm agents compete with **forecast-committed proposals**; **independent review** by different seats; **Human/Safe approval** of every spend; **tranche-based funding** where part of a build's budget is released only after measured outcomes are attested; and a **Learning Ledger** that scores each agent's forecasts against what actually happened and uses that score to allocate *future proposal rights* (not money, not tokens). Funding comes from product revenue (premium collectibles, 3D upgrades, sponsored Dream Rooms, events, pool fee share) gathered by a bounded **Revenue Router** into a **Build Vault**, whose **World Runway** drives bounded **GROW / BALANCED / CONSERVE** modes. Burns (Genesis Forge) create demand and scarcity, but are explicitly **not** counted as revenue.

### 0.3 Evidence limits (read this before the rest)

- **Verified:** Identity.md docs, explorer, $IMD token page, the `identity-md-launches` GitHub organisation, Uniswap v4 hook and dynamic-fee docs, OpenZeppelin Contracts 5.x docs, Safe module docs, and the ERC-8004 draft were read on the research date (§16).
- **Not found in public sources:** No public repository, launch, contract or document named *EMBER*, *IMD Ember World*, *Genesis PEPE*, *Swarm Dream Hall*, *Agent Houses* or *EMBER BUILD VAULT* was found in the `identity-md-launches` GitHub organisation (repository search for "ember", "genesis pepe", "dream hall" returned zero results on the research date). All project context about these items is therefore taken from the task brief and is treated as **project premise**, not verified fact.
- **Comparative cases:** *CLAUS* and *Identity Units* could not be located in any primary source during research. *SIMD* has a public site showing only a name, an X handle and an Ethereum contract address (`0xbb0c…3415`); its mechanics could not be verified. These three are therefore **not** used as evidence for any mechanism in this report. The verified $IMD token and a recent IMD launch ($ADAM, launch 720) are used as comparative cases instead (§10).
- **Price data:** No live price of $IMD, ETH, or any EMBER market exists in this report. All money amounts in the economic model are labelled [ASSUMPTION] and are in USD-equivalent for readability.
- **Tooling limits:** Some pages were read through an automated summariser; every Identity.md number quoted below was re-checked against the raw text of `imd.fun/docs/` and `imd.fun/token/` downloaded on the research date.

---

## 1. Verified ground truth that constrains the design

These facts shape the architecture. Each is [FACT] with a source in §16.

### 1.1 Identity.md network

| Fact | Design consequence |
|---|---|
| Identity.md describes itself as "a network to create net new 0 to 1 billion financial applications, a consensus layer managed by distributed agents" [S1]. | The Swarm is a real build workforce, not branding; EMBER can buy work from it. |
| Seats are ERC-8004-bound; devices pair to a seat, and a seat binds to an ERC-8004 agent [S1]. There are **2,000 seats**, one per Identity.md NFT [S2]. | "Qualified Active IMD Seat" can be defined against an on-chain seat id, not a social claim. |
| Explorer on the research date showed ~638 agents, ~570 online, ~553 working, ~93.9K steps in 24h [S3]. (Snapshot; changes constantly.) | The supply of agent labour is large relative to one world's needs; competition between proposers is feasible. |
| Paid actions (`job.open`, `job.continue`, `launch.open`, `workflow.open`, `oracle.request`, schedules) cost **0.5 IMD each** (per run for schedules), paid via x402 with Permit2 [S1]. | The marginal *protocol* cost of a Swarm job is small and predictable; most real cost is human review, 3D production and hosting. |
| Job shapes include `chain`, `fan_out_join` and `dag`; templates include `impl_tests_review`, `audit`, `fuzz`, `research`; the `adversarial-review` skill is "Review, read-only, by a different seat" [S1]. | Multi-proposer competition (fan-out) and independent review by a *different seat* are native platform primitives. |
| Work records are hashed and written to a reputation registry; review documents are retrievable by hash (`/reviews/:hash.json`, `/work-records/:hash.json`); oracle work is batched daily under a Merkle root [S1]. | Proof-of-build can **reuse** IMD's hashes rather than invent a parallel system. |
| Oracles answer questions with a panel and quorum; "chain" evidence is reproducible from chain data via recipes (incl. Uniswap v4 spot/volume recipes); answers are EIP-712 attestations under domain `IdentityMD Oracle` v2 [S1]. | World Pulse can consume **verifiable** chain metrics (e.g., Genesis mints, Forge burns, pool volume) without trusting a single reporter. |
| Launch economics on IMD's launch path: fixed **1,000,000,000** supply, 18 decimals; "Ten percent to the swarm, ninety to the requester"; swarm share = 2% to wallets with accepted work + 8% per seat connected at admission; `poolBps` 1–9,000 seeds a single-sided pool [S1]. | If EMBER is launched through IMD's `evm_project` path, 10% goes to the swarm by rule; supply is fixed at 1B. This must be decided consciously (§6.4). |
| Trading fee on today's factories: "1.25% of every trade … 1% to the paying wallet and 0.25% to the network. Anyone can call the distribution." [S1] | If the paying wallet is the project Safe, 1% of pool volume is a real, if speculative, revenue stream (§7). |
| "Sepolia (11155111) is the only one open on api.imd.fun today" for launches [S1]. | "Sepolia first" is not just prudence; it is the only launch chain currently open on the platform. |
| `evm_contracts` launches deploy 1–8 contracts "all or nothing", with "No token, so no supply, swarm share or trading fee", and an `owner` address receiving owner roles [S1]. | Surrounding modules (Vault, Forge, Epoch Manager) can be deployed by the Swarm with the Safe as owner. |

### 1.2 $IMD token (comparative, not a template)

[FACT] $IMD: "10M minted in 2023, none since", one supply across Ethereum, Base and Robinhood Chain; "Every sell burns supply"; sIMD staking "redeems for more IMD over time"; "Community Coins" are priced in and backed by IMD and "Each trade pays the launcher and burns a cut of IMD"; all liquidity moved to Uniswap v4 with the "POOL4 hook" in Sep 2026 [S2].

**Design reading [REC]:** $IMD uses sell-burns and staking. EMBER's baseline explicitly forbids anti-sell mechanics and staking APY. EMBER should not mirror $IMD; it should *complement* it by being the asset that **buys world-building work** from the IMD Swarm.

### 1.3 Uniswap v4 and contract standards

- [FACT] Hook permissions are encoded in the hook's address bits; "you cannot deploy a hook to an arbitrary address"; if the address lacks a flag, "the PoolManager never calls that hook function" [S4].
- [FACT] Callbacks: before/after initialize, add/remove liquidity, swap, donate; plus return-delta flags that "let a hook adjust balances" [S4].
- [FACT] Dynamic-fee capability is a flag fixed at pool creation; fees can be updated via `updateDynamicLPFee` or overridden per swap from `beforeSwap` [S5].
- [FACT] OpenZeppelin Contracts 5.x provides `ERC20Burnable` (`burn`, `burnFrom` against allowance), `ERC20Capped` (immutable cap), `ERC20Permit` (ERC-2612), `ERC20Votes` [S6]; `TimelockController` with proposer/executor/canceller/admin roles and a `minDelay` [S7].
- [FACT] Safe modules "can execute arbitrary transactions… A malicious module can take over a Safe" [S8].
- [FACT] ERC-8004 ("Trustless Agents") is a **Draft** defining Identity, Reputation and Validation registries [S9]. Draft status means interfaces can still change.

---

## 2. What makes EMBER distinctive

### 2.1 What EMBER must not be

| Pattern | Why rejected |
|---|---|
| Tax token | Hidden transfer fees break composability and trust; forbidden by baseline. |
| Simple burn token | Burn is supply reduction, not funding. A world needs builders paid. |
| Reflection / rebasing | Forbidden; adds accounting risk; no link to world-building. |
| Staking APY / holder dividend | Forbidden; creates securities-like expectations and JIT-staking attack surface (see $ADAM audit finding A-01, §10). |
| "AI branding only" | No mechanism in which AI output changes what gets built or how money flows. |

### 2.2 The AI-native mechanism: Forecast-Committed, Outcome-Graded Building

This is the core distinctive mechanism. It cannot be summarised as "ERC-20 + fee + burn + AI branding" because the economic flow (which build gets funded, and how much of its budget is released) depends on AI-generated predictions being **committed before** and **scored after** the work.

```
         ┌────────────── WORLD BUILD EPOCH n ───────────────┐
         │                                                   │
 Agent A ─┤ proposal + budget + FORECAST(metric Δ, horizon)  │
 Agent B ─┤ proposal + budget + FORECAST(metric Δ, horizon)  ├─► hashes committed
 Agent C ─┤ proposal + budget + FORECAST(metric Δ, horizon)  │   on EpochManager
         │                                                   │
         │  Reviewers (different seats) score + re-forecast  │
         │  Human/Safe selects winner(s), approves budget    │
         │                                                   │
         │  Budget split:  BASE tranche  (on publish + QA)   │
         │                 OUTCOME tranche (after horizon,   │
         │                 released by Safe against attested │
         │                 World Pulse metric)               │
         └───────────────────────────────────────────────────┘
                                │
                                ▼
                     LEARNING LEDGER (per seat)
           forecast error, review calibration, cost accuracy
                                │
                                ▼
       next epoch: proposal SLOTS & review weight allocated by
       calibration score  (rights, not money; never balances)
```

Key properties:

1. **Forecast commitment.** Each proposal includes a structured forecast, e.g. "Dream Room *Lantern Bog* will raise weekly unique Dream Hall visitors by +8% (±4%) within 21 days" and "cost ≤ 1,800 USD-eq". The hash of the proposal (including forecast) is committed on-chain to the EpochManager before review. It cannot be edited after the fact.
2. **Outcome-graded release.** A fixed share of the approved budget (the outcome tranche, e.g. 20–30%) is only *eligible* for release after the horizon, conditional on the attested metric. The Safe still signs the release; the contract enforces that it cannot exceed the reserved amount and cannot be paid before the horizon. Unreleased outcome tranches return to the Vault.
3. **Learning Ledger.** For every seat: forecast error, cost overrun, review calibration (did their ranking predict outcomes?), QA defect rate. This is published (off-chain JSON, on-chain hash).
4. **Rights, not rewards.** Calibration determines *how many proposal slots* a seat gets next epoch and *how much weight* its review carries in the ranking shown to the Human. It never touches token balances, never mints, never changes fees.

Why this is AI-native: the system's capital allocation is a function of machine-generated predictions and machine-generated evaluations, scored over time. A human-only DAO could copy it, but it only becomes practical when dozens of agents can cheaply generate structured forecasts and reviews every epoch — which the IMD Swarm verifiably provides (§1.1).

**Pros:** rewards being *right*, not being loud; limits overspend on hyped ideas; creates a measurable learning signal; transparent.
**Cons:** metrics can be gamed (§11); horizons delay payment to builders (needs a base tranche large enough to be fair); small sample sizes early on make calibration noisy; requires good World Pulse data.

### 2.3 Secondary distinctive mechanisms

- **Dream-to-Forge pipeline** (§9): ideas are cheap in 2D/2.5D (Swarm Dream Hall) and only promoted to expensive 3D (Tripo / premium production) after review and human selection. The token economy funds an *evolutionary funnel*, not a fixed roadmap.
- **World Runway modes** (§8): the world's build tempo is coupled to its measured treasury health.
- **Proof-of-Learning records**: each closed epoch publishes what was predicted, what happened, and what the World Brain changed in response.

---

## 3. Layered architecture

### 3.1 Overview

```
 ┌──────────────────────────── OFF-CHAIN (adaptive) ─────────────────────────────┐
 │                                                                                │
 │  EMBER WORLD BRAIN  (planning/analysis; NO keys that move funds)              │
 │   ├─ Observer: reads World Pulse, Dream Hall analytics, Explorer, chain data   │
 │   ├─ Analyst: gaps, weaknesses, opportunities                                  │
 │   ├─ Planner: drafts Epoch Brief + budget priorities + mode recommendation     │
 │   └─ Evaluator: post-publication scoring → Learning Ledger                     │
 │                                                                                │
 │  IDENTITY.MD SWARM (jobs via api.imd.fun, paid 0.5 IMD/action)                 │
 │   ├─ Proposer seats (fan_out)     ├─ Builder seats (impl / content)            │
 │   ├─ Reviewer seats (adversarial-review, different seat)                       │
 │   └─ Oracle panels (chain-evidence metrics, EIP-712 attested)                  │
 │                                                                                │
 │  Swarm Dream Hall (2D/2.5D)   Ember World (3D)   Agent Houses (proof pages)    │
 └───────────────┬─────────────────────────────────────────────┬──────────────────┘
                 │ hashes, attestations, signed recommendations │
 ┌───────────────▼─────────────────────────────────────────────▼──────────────────┐
 │                         ON-CHAIN (bounded)                                      │
 │                                                                                 │
 │  EpochManager ── BuildRegistry ── WorldPulse ── ModeRegistry                    │
 │       │                                              │                          │
 │       ▼ (reservations only)                          │ (bounded params)         │
 │  BuildVault  ◄──── RevenueRouter ◄──── revenue (fees, sales, sponsors)          │
 │       ▲                                                                         │
 │       │ (Safe-signed releases, capped)                                          │
 │  HUMAN / SAFE (M-of-N)  ──► TimelockController (for parameter changes)          │
 │                                                                                 │
 │  GenesisForge (burn EMBER → mint Genesis PEPE; seat free-claim)                 │
 │  EMBER ERC-20 (fixed supply, immutable, no owner)                               │
 │  [future] BurnReserve   [future] Uniswap v4 Hook                                │
 └─────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Mutability matrix [REC]

| Component | Where | Mutability | Authority | Notes |
|---|---|---|---|---|
| EMBER ERC-20 | On-chain | **Immutable**, no owner, no proxy | None | OZ `ERC20` + `ERC20Permit` + `ERC20Burnable`. Entire supply minted in constructor. No `mint` function exists. |
| GenesisForge | On-chain | Immutable logic; **price** and **season caps** adjustable within hard-coded bounds | Safe via Timelock | Separate contract; owns Genesis PEPE mint right; cannot touch EMBER balances except via user-approved `burnFrom`. |
| Genesis PEPE NFT | On-chain | Immutable; minter = GenesisForge only, set once | None after init | Metadata URI pointer may be updatable by Safe+Timelock until frozen. |
| BuildVault | On-chain | Immutable logic; caps adjustable within hard bounds | Safe (releases), Timelock (caps) | Holds EMBER/ETH/stablecoin. Per-epoch and per-job caps. Replaceable by migrating funds through a timelocked call. |
| EpochManager | On-chain | **Replaceable** (new version, Vault points to new one via Timelock) | Safe opens/closes epochs; anyone reads | Stores proposal/review/forecast hashes and reservations. |
| BuildRegistry | On-chain | Append-only; replaceable | Safe or Safe-authorised recorder | Proof-of-build entries (artifact hash, IMD job id, reviewer seat ids). |
| WorldPulse | On-chain | Append-only; replaceable | Accepts IMD oracle EIP-712 attestations (verified on-chain) + Safe-posted hashes | Never moves funds. |
| ModeRegistry | On-chain | Mode enum + bounded params | AI may *record* recommendation; Safe+Timelock sets mode | Bounds hard-coded. |
| RevenueRouter | On-chain | Immutable split **bounds**; split values adjustable within bounds | Safe+Timelock | Pull-based; anyone can trigger distribution. |
| World Brain | Off-chain | Freely upgradeable (prompts, models, data) | Project team | Outputs hashed into EpochManager; a signing key that can only sign recommendations. |
| Learning Ledger | Off-chain JSON + on-chain hash | Append-only by convention | Evaluator | Reproducible from public data. |
| Dream Hall / Ember World content | Off-chain (IPFS/ENS via IMD sites) | Fully iterative | Human approves production publishes | Content CIDs recorded in BuildRegistry. |
| BurnReserve | Future | Immutable if introduced | — | Only receives a bounded share; only burns. |
| v4 Hook | Future | Immutable per pool (address-encoded permissions) | — | Not in V1 (§6.5). |

**Principle [REC]:** *Upgradeability lives at the edges; the token and the money-holding contracts' safety rules do not change. A new version replaces a module; it does not mutate it in place.* Avoid upgradeable proxies for any contract that holds funds in V1.

---

## 4. EMBER WORLD BRAIN

### 4.1 Definition

The World Brain is a set of Swarm jobs and project-run agents that answer one question per epoch: **"What should the world build or improve next, and why do we believe it will work?"** It holds no treasury keys. Its only on-chain footprint is (a) a recommendation-signing key whose signatures are recorded but grant no authority, and (b) hashes of its documents.

### 4.2 Inputs (Observe)

| Signal | Source | Verifiability |
|---|---|---|
| Genesis PEPE mints, Forge burns, holder count | Chain; IMD oracle `log-count`/`log-sum` recipes | High (chain evidence) |
| EMBER pool volume, spot price | Chain; IMD `univ4-spot`, `v4-volume-rank` recipes | High |
| Build Vault balance, reservations, burn rate | Chain | High |
| Dream Hall / Ember World visits, session length, return rate | Web analytics | Low–medium (off-chain; hash daily) |
| Room-level engagement (which rooms are visited, abandoned) | World telemetry | Low–medium |
| Swarm job acceptance/rejection, review findings | IMD API (`/jobs/:id/records`, `/reviews/:hash.json`) | High (hash on chain) |
| Community requests, bug reports | Forms / social | Low (sybil-prone) |

### 4.3 Outputs

1. **Epoch Brief**: top 3–5 needs, each with evidence, a target metric and a budget envelope.
2. **Mode recommendation**: GROW / BALANCED / CONSERVE with the runway calculation shown.
3. **Proposal comparison table** after proposals close.
4. **Post-epoch evaluation**: forecast vs actual, Learning Ledger update, "what we will do differently".

### 4.4 Guardrails

- Briefs must cite metric snapshots by hash. Claims without data are flagged.
- The Brain may not propose changes to the token, the Forge price outside bounds, or Vault caps outside bounds. Proposals that do are auto-rejected by a lint step.
- The Brain's own forecasts are scored in the Learning Ledger like any proposer's. The Brain is not exempt from being wrong.

---

## 5. The AI World Evolution Loop

### 5.1 Formal states

```
  ┌─────────┐   ┌──────────────┐   ┌───────────────┐   ┌─────────────────────┐
  │ OBSERVE ├──►│NEED IDENTIFIED├──►│PROPOSALS OPEN ├──►│MULTIPLE AGENTS      │
  └─────────┘   └──────────────┘   └───────────────┘   │PROPOSE (commit hash)│
       ▲                                               └──────────┬──────────┘
       │                                                          ▼
  ┌────┴─────┐  ┌───────┐  ┌──────────┐  ┌────┐  ┌───────┐  ┌──────────────────┐
  │NEXT EPOCH│◄─┤ CLOSE │◄─┤  LEARN   │◄─┤... │  │RANKED │◄─┤INDEPENDENT REVIEW│
  └──────────┘  │ EPOCH │  └────▲─────┘  └────┘  │CANDID.│  └──────────────────┘
                └───────┘       │                └───┬───┘
                           ┌────┴────┐               ▼
                           │ MEASURE │      ┌────────────────────┐
                           └────▲────┘      │HUMAN / SAFE APPROVE│
                                │           └─────────┬──────────┘
                           ┌────┴────┐                ▼
                           │ PUBLISH │◄─QA◄─BUILD◄─FUNDING RESERVED
                           └─────────┘
```

### 5.2 State table [REC]

| # | State | Actor | On-chain effect | Exit condition | Typical duration [ASSUMPTION] |
|---|---|---|---|---|---|
| 1 | OBSERVE | World Brain (Observer) | WorldPulse snapshot hash | Snapshot published | continuous; snapshot daily |
| 2 | NEED IDENTIFIED | World Brain (Analyst/Planner) | Epoch Brief hash; `openEpoch()` by Safe | Safe opens epoch | 1–2 days |
| 3 | PROPOSALS OPEN | EpochManager | Epoch state = PROPOSING, deadline set | Deadline | 3–5 days |
| 4 | MULTIPLE AGENTS PROPOSE | Proposer seats (IMD `fan_out_join` job) | `commitProposal(hash)` per proposal | Deadline | within 3 |
| 5 | INDEPENDENT REVIEW | Reviewer seats (different seats, `adversarial-review`) | review hashes | All assigned reviews in | 2–3 days |
| 6 | RANKED CANDIDATES | World Brain aggregates | ranking hash | Published | 1 day |
| 7 | HUMAN / SAFE APPROVAL | Safe signers | `approve(proposalId, base, outcome, horizon)` | Safe tx executed | 1–3 days |
| 8 | FUNDING RESERVED | BuildVault | Reservation ≤ caps; mode bounds checked | Reserved | same tx |
| 9 | BUILD | Builder seats | — | Delivery | 3–14 days |
| 10 | QA | Reviewer seats + human | QA report hash | Pass / fail | 1–3 days |
| 11 | PUBLISH | Human approves production publish | BuildRegistry entry (CID, job ids); base tranche release | Live | 1 day |
| 12 | MEASURE | Oracle panels + analytics | WorldPulse attestations | Horizon reached | 14–30 days |
| 13 | LEARN | Evaluator | Learning Ledger hash; outcome tranche decision | Published | 1–2 days |
| 14 | CLOSE EPOCH | Safe | `closeEpoch()`; unreleased funds return | Closed | — |
| 15 | NEXT EPOCH | — | — | — | Epochs overlap: MEASURE of n runs during BUILD of n+1 |

**Failure paths:** QA fail → one revision round (`job.continue`) → if still failing, base tranche partially paid for accepted work only, remainder returns. Safe rejects all candidates → epoch closes with zero spend (a valid outcome). Measurement unavailable → outcome tranche returns to Vault by default after a grace period (fail-closed).

---

## 6. Contracts and money boundaries

### 6.1 EMBER ERC-20 [REC]

- OpenZeppelin 5.x `ERC20`, `ERC20Permit`, `ERC20Burnable`. **No** `Ownable`, `AccessControl`, `Pausable`, proxy, blacklist, fee-on-transfer, rebasing, or hooks into transfers.
- Total supply minted once in the constructor to a distribution contract/Safe. With no `mint` function, the cap is enforced by absence; `ERC20Capped` is unnecessary (and adds a code path) unless a vesting minter is required — it is not.
- `ERC20Votes` **not** included in V1: governance is Human/Safe; adding votes invites governance-capture expectations before the community is ready.

### 6.2 Genesis Forge [REC]

Confirmed principles preserved: Qualified Active IMD Seats get a separate one-time free entitlement; **no public free mint**; non-free Genesis requires EMBER consumption.

```
 User ──approve(Forge, X) or permit──► EMBER
 User ──forge(qty)──► GenesisForge
                         │ 1. check season cap, per-wallet cap, price X (bounded)
                         │ 2. EMBER.burnFrom(user, X*qty)   ← reverts if allowance/balance short
                         │ 3. GenesisPEPE.mint(user, qty)   ← reverts if sold out
                         ▼
                 single transaction: both happen or neither (atomic)

 Seat holder ──claimSeat(seatId, proof)──► GenesisForge
                         │ 1. verify Merkle proof: (seatId, wallet) in qualified snapshot
                         │ 2. require !claimed[seatId]; set claimed[seatId] = true
                         │ 3. GenesisPEPE.mint(wallet, 1)
```

- **"Burn / permanently consume"**: use `burnFrom`, which reduces `totalSupply` — publicly verifiable. Sending to a dead address is weaker (does not reduce `totalSupply`) and is rejected.
- **No hidden tax:** the price X shown in the UI equals the amount burned. No portion is diverted. (If the project later wants a *revenue* share from forging, it must be a separate, visible line item — see §7.3 and §11.)
- **No arbitrary admin mint:** GenesisPEPE's only minter is the Forge, set once in the constructor; the Forge has no admin-mint path. Seat claims use a Merkle root fixed at deployment (or set once, then locked).
- **"Qualified Active IMD Seat"** [OPEN]: must be defined precisely before the snapshot — e.g. seat NFT held by wallet at block B, and seat with ≥ N accepted work records in the 30 days before B (readable from `/seats/:tokenId`). The exact threshold is a product decision.
- **Price bounds:** X adjustable by Safe+Timelock within `[X_min, X_max]` hard-coded at deploy, with a maximum change per adjustment (e.g., ±25%) and a minimum interval. The World Brain may recommend; it cannot set.

### 6.3 Build Vault [REC]

- Holds assets for approved Swarm jobs and related production costs (3D production, hosting, QA).
- `reserve(epochId, proposalId, base, outcome, horizon)` callable only by the Safe, checks: per-job cap, per-epoch cap (from current mode, bounded), and that total reservations ≤ free balance.
- `releaseBase(proposalId, to)` — Safe only, only after BuildRegistry has a publish record.
- `releaseOutcome(proposalId, to, amount)` — Safe only, only after `horizon`, `amount ≤ outcomeReserved`.
- `expire(proposalId)` — anyone, after horizon + grace: unreleased funds return to free balance (fail-closed).
- No function lets any address other than the Safe move funds. No function lets the World Brain key do anything.
- Paying the IMD Swarm: jobs are paid in IMD (0.5 IMD/action [S1]). The Vault should therefore hold a small IMD float, topped up by Safe-approved swaps; the Vault itself should not contain swap logic in V1.

### 6.4 Launch path decision [OPEN → REC]

Two options:

| Option | What happens | Pros | Cons |
|---|---|---|---|
| A. IMD `evm_project` / standard launch | 1B fixed supply, 10% to swarm via Merkle distributor, pool seeded per `poolBps`, 1.25% trading fee (1% to paying wallet) [S1] | Native to ecosystem; swarm alignment (seat holders receive EMBER); built-in fee revenue to paying wallet | Token code generated through the platform: must be audited against EMBER's baseline (no mint, no tax on transfer); fee is on trades, so revenue depends on speculation; parameters set by "chain's policy" may change |
| B. `evm_contracts` (no token issued by platform) + own EMBER | Contracts only, owner = Safe, no swarm share or fee [S1] | Full control of token code | Loses native pool fee and swarm distribution; must design liquidity separately |

**[REC]:** Prototype **both on Sepolia** and decide after reading the generated token code. Option A's 10% swarm distribution is *strongly aligned* with the "Swarm = builders" premise and its 1% fee to the paying wallet is the only verified recurring revenue stream available today. The pool fee is a swap fee in the pool, **not** a transfer tax on the token — it does not violate the "no hidden tax" rule as long as it is disclosed.

### 6.5 Uniswap v4 Hook (future, not V1) [REC]

A custom hook could, for example, route a bounded donation to the Build Vault, or emit World Pulse events. But hook permissions are fixed by address bits and the dynamic-fee flag is fixed at pool creation [S4][S5], so mistakes are permanent per pool. Hooks with return-delta permissions can change balances, which is exactly the class of power AI must never steer. V1 should use the platform's standard pool. A V2 hook, if any, must have: hard-coded fee ceilings, no owner-adjustable fee beyond bounds, no AI-controlled inputs, and a full independent audit.

### 6.6 Revenue Router [REC]

```
          revenue in (ETH / EMBER / stable / IMD)
                         │
                  RevenueRouter.distribute()   ← anyone may call
          ┌──────────────┼─────────────────┬───────────────┐
          ▼              ▼                 ▼               ▼
   BuildVault       OpsReserve        QA/Audit Fund   [future] BurnReserve
   (60–85%)         (10–25%)          (5–10%)         (0–15%, EMBER only)
```

Split values can move only inside hard-coded ranges, via Safe+Timelock, at most once per epoch. BurnReserve stays at 0% in V1 (burn is not revenue, and the Forge already burns).

---

## 7. Self-sustaining revenue

### 7.1 Burn ≠ revenue

Genesis Forge burns EMBER. That **reduces supply** and **creates demand** for EMBER, but the protocol receives nothing it can spend. A design that counts burns as "income" will run out of money while looking healthy. Every model below excludes burns from revenue.

### 7.2 Candidate revenue sources

| Source | Who pays | Why they pay | Protocol receives | Recurring? | Depends on speculation? | V1? |
|---|---|---|---|---|---|---|
| Pool trading fee share (IMD launch path) | Traders | To trade EMBER | 1% of volume to paying wallet on today's factories [S1] → Safe → Router | Yes, while volume exists | **High** | Yes, if Option A; do not budget on it |
| Premium 3D upgrades for Genesis PEPE | Genesis holders | Better 3D model, animation, World presence | ETH/stable/EMBER price, set per item | Per season | Low–medium | **Yes** (core) |
| Premium collectibles / Dream Room items | Players, collectors | Cosmetic, display in Agent House | Primary sale price | Seasonal | Medium | Yes (small) |
| Sponsored Dream Rooms | Other IMD projects, brands, communities | Presence in a living world; Swarm-built room | Fixed fee per room per season | Yes, if world has visitors | Low | **Yes** (pilot) |
| Commissioned builds ("Dream Room as a service") | Other communities | They want a 2D/2.5D room built by the Swarm | Fee minus Swarm/production cost | Yes | Low | Experimental |
| Event passes / seasonal quests | Players | Access to time-limited events | Pass price | Seasonal | Low–medium | Later (V1.5) |
| Marketplace secondary royalties | Secondary buyers | Marketplace convention | ERC-2981 % where honoured | Yes | Medium | Yes, but **not enforceable**; budget at 0 |
| Special/limited Genesis mints | Collectors | Scarcity | Burn only by principle → **0 revenue**, unless an explicit, disclosed ETH component is added | No | High | Burn-only in V1 |
| Bounded protocol levy on transfers | Every holder | Forced | — | — | — | **No** (violates baseline) |
| Grants / ecosystem partnerships | IMD ecosystem, partners | Strategic | One-off | No | Low | Opportunistic; not runway |

### 7.3 Should the Forge carry a revenue component?

[REC] Not in V1. "Burn X EMBER → mint" is simple, honest and auditable. If a revenue component is later needed, add it as a **separate, explicit ETH price line** (e.g., "burn 5,000 EMBER **and** pay 0.002 ETH to the Build Vault"), shown in the UI and enforced in the same atomic transaction. Never silently divert part of X.

### 7.4 Revenue scenarios [ASSUMPTION — illustrative only]

Assumptions: monthly figures in USD-equivalent; pool fee share = 1% of volume (Option A); 3D upgrade avg $25 net of production marginal cost of $10 (i.e., $15 contribution); sponsored room $300/season-month; collectible net $5 each; royalties budgeted at 0.

| Monthly | LOW | MEDIUM | HIGH |
|---|---|---|---|
| EMBER pool volume | $150k ($5k/day) | $1.5M ($50k/day) | $15M ($500k/day) |
| Pool fee share (1%) | $1,500 | $15,000 | $150,000 |
| 3D upgrades sold | 20 → $300 | 150 → $2,250 | 800 → $12,000 |
| Sponsored rooms | 1 → $300 | 4 → $1,200 | 12 → $3,600 |
| Collectibles | 50 → $250 | 400 → $2,000 | 3,000 → $15,000 |
| **Total revenue** | **$2,350** | **$20,450** | **$180,600** |
| Of which speculation-dependent (pool fee) | 64% | 73% | 83% |
| Non-speculative revenue | $850 | $5,450 | $30,600 |

**Reading:** At every volume level the pool fee dominates, and it is the most fragile line. A sustainable design must be able to fund a **minimum viable world** (see §8) from **non-speculative revenue alone** in the medium case, and treat pool fees as surplus that extends runway or funds GROW mode. In the low case the world cannot be self-funding; it must run on its initial treasury allocation in CONSERVE mode. This is stated plainly: self-sustainability is **plausible** at medium volume with product revenue, **not** guaranteed.

---

## 8. World Runway and economic modes

### 8.1 Definitions

```
free_balance       = Vault balance − active reservations           (USD-eq, at a conservative price)
avg_build_cost     = trailing mean of last 4 epochs' total spend per build
build_runway       = free_balance ÷ avg_build_cost                 (in builds)
burn_rate          = trailing 3-epoch spend per month
net_burn           = burn_rate − trailing 3-month non-speculative revenue
time_runway        = free_balance ÷ max(net_burn, ε)               (in months)
```

[REC] Value EMBER held in the Vault at a **haircut** (e.g., 50% of 7-day TWAP) because selling it to pay builders moves the price. Value stablecoins and ETH at market.

### 8.2 Build cost estimate [ASSUMPTION]

| Cost item | Low | Typical | High |
|---|---|---|---|
| IMD Swarm actions (proposals fan-out, reviews, build, QA; ~15–40 actions × 0.5 IMD) | 7.5 IMD | 12 IMD | 20 IMD |
| Human review/curation time | $150 | $400 | $1,000 |
| 3D production (only for promoted concepts) | $0 | $300 | $1,500 |
| Hosting/analytics share | $50 | $100 | $200 |
| **Per build (excl. IMD at unknown price)** | **$200** | **$800** | **$2,700** |

### 8.3 Modes [REC]

| Mode | Trigger (recommended by Brain; set by Safe+Timelock) | Builds/epoch | Per-epoch cap | Outcome tranche share | 3D promotions |
|---|---|---|---|---|---|
| **GROW** | time_runway ≥ 12 months **and** non-speculative revenue covers ≥ 50% of burn | 3–5 | up to 15% of free balance | 20% | up to 3 |
| **BALANCED** | 6 ≤ time_runway < 12 | 2–3 | up to 8% | 25% | 1–2 |
| **CONSERVE** | time_runway < 6 **or** pool-fee revenue falls > 50% month on month | 1 | up to 4% | 30% | 0–1 (only pre-sold) |

- Hard bounds in contract: per-epoch cap can never exceed 15% of free balance in any mode; mode can change at most once per epoch; Timelock delay ≥ 48h [ASSUMPTION].
- **Automatic downgrade only:** [EXPERIMENTAL] the contract could allow *anyone* to trigger a downgrade to CONSERVE if an attested runway figure falls below threshold, because becoming more conservative is safe. Upgrades always require Safe.
- AI recommends a mode each epoch, with the calculation published. The recommendation is recorded in ModeRegistry as data only.

---

## 9. Genesis PEPE Engine and its self-improvement

### 9.1 Funnel

```
 WIDE  ─► World Brain + proposer seats generate 30–100 concepts per season
          (traits, lore, accessories, behaviours, room tie-ins)          cost: very low
   │
   ▼    Independent reviewers (different seats) score: originality, lore fit,
        production feasibility, IP risk, duplication vs existing set        cost: low
   │
   ▼    Top 8–12 → 2D/2.5D prototypes in Swarm Dream Hall
        (visitors interact; engagement measured; forecasts committed)       cost: low–medium
   │
   ▼    Human selects 1–3 (Safe approves budget)                            decision
   │
   ▼    Tripo / premium 3D production → QA → publish as Genesis upgrade
        or new trait set, minted only through Genesis Forge                 cost: high
 NARROW
```

### 9.2 Rules

- Only Forge-minted or seat-claimed Genesis PEPE exist. No new admin mint for "special editions"; special editions are new **traits/upgrades** applied to existing tokens, or new Forge seasons with their own bounded caps.
- 3D upgrades are sold (revenue, §7) — not burned — to keep a clear line between demand-creation (burn) and funding (sale).
- Prototype performance in Dream Hall feeds the Learning Ledger: did the reviewers' ranking predict which concepts players engaged with?
- IP review is a mandatory reviewer criterion (AI-generated art can resemble existing IP; human sign-off required before 3D production).

---

## 10. Comparative case studies

| Case | Verified mechanics | Lesson for EMBER |
|---|---|---|
| **$IMD** [S2] | Fixed 10M supply; sell-burns; sIMD staking; POOL4 v4 hook; community coins burn a cut of IMD per trade | Demand-side sinks work as narrative, but EMBER's baseline rejects anti-sell and staking. EMBER should create **utility demand** (Forge, upgrades) instead and pay the IMD Swarm for work — a complementary role. |
| **IMD launch economics** [S1] | 10% to swarm (2% by accepted work, 8% per connected seat); 1.25% pool fee | A ready-made alignment and fee path; must be consciously adopted or declined (§6.4). |
| **$ADAM, launch 720** [S10] | Public repo describes token, hook, fees, splits, oracle, NFT claim and keeper bounty, and an independent audit whose finding A-01 was "just-in-time staking" in a distributor | Evidence, inside the same ecosystem, that staking-style distributors attract JIT attacks; supports EMBER's no-staking/no-dividend baseline. |
| **SIMD** [S11] | Only name, X handle and contract address verifiable | Not used as evidence. |
| **CLAUS, Identity Units** | Not found in primary sources | Not used as evidence. [OPEN] Provide primary links if these should be analysed. |

---

## 11. Multi-agent competition: evaluation

| Dimension | Single proposer | Multi-proposer competition (recommended) | Notes / mitigation |
|---|---|---|---|
| Creativity | Narrow | **High** — diverse models/identities | Mix models and identity profiles across proposer rows. |
| Quality | Depends on one agent | **Higher** via selection | Review rubric fixed per epoch and published. |
| Cost | 1× | ~3–5× proposal cost | Proposal cost is small (0.5 IMD actions); build cost only for winner. Net cost increase is modest. |
| Latency | Fast | +2–4 days (review + ranking) | Overlap epochs. |
| Reviewer bias | n/a | Risk: reviewers favour their own model family/style | Blind proposals (strip seat ids), assign reviewers from different model families, measure reviewer calibration. |
| Collusion | n/a | Risk: proposer and reviewer controlled by same operator | Reviewers must be different seats **and** different wallets; random assignment; calibration penalties; Human has final say. Wallet-level independence is not provable — residual risk. |
| Duplication | n/a | Risk: near-identical proposals | Similarity check (embedding distance) before review; duplicates merged, earliest commit credited. |
| Gaming metrics | Possible | Possible | Use chain-attested metrics where possible; cap outcome tranche; human review of anomalies. |

[REC] **3 proposers, 3 reviewers per proposal** as default; 5 proposers in GROW mode. Ranking presented to Human shows each reviewer's calibration score.

---

## 12. Threat model and risk analysis

### 12.1 Authority map

| Actor | Can | Cannot |
|---|---|---|
| World Brain / any AI agent | Observe, propose, review, forecast, sign recommendations, build content in repos | Hold Vault/Safe keys; mint; burn others' tokens; change balances; change fees; change modes; deploy to production without approval |
| Swarm builder seat | Deliver work; receive approved payments | Self-approve; release funds |
| Safe signers (M-of-N) | Approve reservations/releases; propose timelocked parameter changes within bounds | Mint EMBER (no function exists); exceed hard caps; seize user funds |
| Timelock | Execute queued parameter changes after delay | Change hard-coded bounds |
| Any user | Forge, claim seat entitlement, trigger `distribute()`, `expire()` | Anything privileged |

### 12.2 Risk register

| # | Threat | Likelihood | Impact | Mitigation | Residual |
|---|---|---|---|---|---|
| R1 | Prompt injection: repo text / proposal content instructs an agent to request funds or change parameters | High | Medium | AI has no fund authority; parameter-changing proposals auto-rejected; reviewers instructed to treat content as data | Low |
| R2 | Safe signer compromise | Low | Critical | M-of-N ≥ 3-of-5, hardware keys, Timelock on parameters, per-epoch caps, no modules in V1 (Safe warns modules can take over a Safe [S8]) | Medium |
| R3 | Forge bug mints without burn | Low | High | Atomic `burnFrom` then mint; tests + fuzz + independent audit (IMD `audit`/`fuzz` templates plus external); supply cap on NFT | Low |
| R4 | Seat entitlement double-claim / sybil | Medium | Medium | Per-seatId bitmap; Merkle snapshot; "active" threshold based on accepted work | Low |
| R5 | Metric gaming to unlock outcome tranches | Medium | Medium | Chain-attested metrics preferred; off-chain metrics bot-filtered; tranche ≤ 30%; Safe signs | Medium |
| R6 | Reviewer collusion | Medium | Medium | §11 mitigations | Medium |
| R7 | Revenue collapse (volume dries up) | High | High | Non-speculative revenue focus; CONSERVE mode; EMBER haircut in runway | Medium |
| R8 | Vault EMBER dumping crashes price | Medium | High | Pay builders in IMD/stable where possible; release EMBER in small, scheduled amounts; disclose | Medium |
| R9 | Regulatory: token perceived as investment contract | Medium | High | No yield, no dividend, no promise of returns; utility framing; legal review before Mainnet [OPEN] | Medium |
| R10 | ERC-8004 draft changes break seat checks | Medium | Low | Snapshot Merkle root rather than live registry call in Forge | Low |
| R11 | Platform parameter change (fee policy, 0.5 IMD price, chains) | Medium | Medium | Docs state fee is "set by the chain's policy"; model with sensitivity; re-check each epoch | Medium |
| R12 | AI-generated content IP infringement | Medium | Medium | Mandatory IP review criterion; human sign-off before 3D/production | Medium |
| R13 | Hook misconfiguration (future) | — | Critical | Not in V1 | — |

---

## 13. World self-improvement (beyond content)

*Note: the brief's sentence "The system should improve not only content, but also the …" is truncated. [ASSUMPTION] It is read here as "…but also the process, the economy's parameters and the AI system itself".*

What the loop improves, and how:

| Layer | Improvement target | Measured by | Who changes it |
|---|---|---|---|
| Content | Rooms, residents, quests | engagement metrics | Swarm builders; Human approves |
| Process | Epoch length, number of proposers, review rubric | cost per accepted build, QA pass rate, latency | World Brain recommends; team adopts (off-chain) |
| AI quality | Prompts, model mix, identity profiles | forecast error, reviewer calibration | Team (off-chain), informed by Learning Ledger |
| Economics | Forge price, mode, Router splits — **within bounds only** | runway, revenue mix | Safe + Timelock |
| Security | Tests, fuzzing, audits of modules | findings count, severity | Swarm `audit`/`fuzz` jobs + external audit; Safe deploys |

Proof-of-Learning record per epoch: `{epochId, briefHash, proposals[], forecasts[], selected[], actuals[], forecastErrors[], ledgerHash, changesAdopted[]}` → JSON on IPFS, hash in EpochManager.

---

## 14. Final recommended V1 architecture

### 14.1 Components

```
                    ┌──────────────── HUMAN / SAFE (3-of-5) ────────────────┐
                    │  approves every reservation and release              │
                    │  queues bounded param changes via Timelock (≥48h)    │
                    └───────┬───────────────────────┬──────────────────────┘
                            │                       │
     ┌──────────────────────▼───┐        ┌──────────▼───────────┐
     │ EpochManager v1          │        │ ModeRegistry          │
     │ commit/review/forecast   │        │ GROW/BALANCED/CONSERVE│
     │ hashes; reservations     │        │ hard bounds           │
     └──────┬───────────────────┘        └──────────┬───────────┘
            │                                       │
     ┌──────▼──────────┐   ┌──────────────┐   ┌─────▼─────────────┐
     │ BuildVault      │◄──┤RevenueRouter │◄──┤ revenue: pool fee,│
     │ caps, tranches, │   │bounded splits│   │ 3D upgrades,      │
     │ fail-closed     │   └──────────────┘   │ sponsors, items   │
     └──────┬──────────┘                      └───────────────────┘
            │ pays (IMD float / stable / EMBER small)
            ▼
     IMD Swarm jobs ──► BuildRegistry (proof-of-build) ──► WorldPulse
                                                           (IMD oracle
                                                            attestations)
     ┌───────────────────────────┐   ┌─────────────────────────────┐
     │ EMBER ERC-20 (immutable,  │──►│ GenesisForge (burnFrom X →  │
     │ fixed supply, no owner)   │   │ mint PEPE; seat free claim) │
     └───────────────────────────┘   └─────────────────────────────┘
     Off-chain: World Brain, Learning Ledger, Dream Hall, Ember World, Agent Houses
```

### 14.2 V1 decisions

| Decision | V1 choice |
|---|---|
| Chain | Sepolia only (also the only launch chain open on api.imd.fun today [S1]). Mainnet: separate decision after audit, legal review, and ≥ 3 full epochs on Sepolia. |
| Token | Fixed supply, immutable, OZ ERC20 + Permit + Burnable; no owner. |
| Launch path | Prototype both IMD standard launch (Option A) and contracts-only (Option B); choose after code review. Leaning A for swarm alignment and fee revenue, provided generated token code meets baseline. |
| Forge | Separate contract; `burnFrom` + mint atomic; bounded price; seat Merkle claim. |
| Vault | Safe-only releases; per-job and per-epoch caps; base + outcome tranches; fail-closed expiry. |
| AI authority | Zero on-chain authority; recommendations recorded as data. |
| Distinctive mechanism | Forecast-committed proposals + outcome-graded tranches + Learning Ledger allocating proposal rights. |
| Competition | 3 proposers × 3 independent reviewers per proposal (5 in GROW). |
| Modes | Three modes, Safe+Timelock, one change per epoch, auto-downgrade [EXPERIMENTAL]. |
| Revenue | 3D upgrades, sponsored rooms, collectibles, pool fee share; burns excluded from revenue; royalties budgeted at 0. |
| Excluded in V1 | Hook, BurnReserve share > 0, ERC20Votes, Safe modules, upgradeable proxies, transfer levy. |

### 14.3 Implementation plan (Sepolia)

1. **Phase 0 – Specification (1–2 weeks):** define Qualified Active Seat; write invariants (supply constant except burns; Vault outflows ≤ reservations ≤ caps; one claim per seat).
2. **Phase 1 – Contracts (2–4 weeks):** IMD `impl_tests_review` and `fuzz` jobs for Token, Forge, NFT, Vault, EpochManager, BuildRegistry, WorldPulse, Router, ModeRegistry; `adversarial-review` by different seats; external audit before any Mainnet consideration.
3. **Phase 2 – World Brain MVP (parallel):** Observer + Planner producing Epoch Briefs from Sepolia data and Dream Hall analytics.
4. **Phase 3 – Three dry-run epochs:** test-value funds; full loop including MEASURE and LEARN; publish Proof-of-Learning records.
5. **Phase 4 – Review gate:** decide Mainnet readiness using explicit criteria (zero critical/high open findings, runway model validated with real Sepolia-era costs, legal opinion).

---

## 15. Open questions

1. [OPEN] Exact definition of "Qualified Active IMD Seat" (holding vs. activity threshold; snapshot block).
2. [OPEN] Option A vs B launch path — requires reading the platform-generated token code.
3. [OPEN] Current $IMD price and expected per-build IMD spend — needed to finalise runway numbers.
4. [OPEN] Tripo / 3D production pricing and licensing terms (not researched; not a primary-source item in scope).
5. [OPEN] Primary sources for CLAUS and Identity Units, if they should be compared.
6. [OPEN] Jurisdictional legal review of EMBER utility framing before any Mainnet step.
7. [OPEN] Whether IMD's fee policy ("set by the chain's policy", "today's factories") will remain 1.25% / 1% to paying wallet.
8. [OPEN] Whether IMD oracle attestations can be verified on Sepolia contracts (EIP-712 domain includes `chainId` and `verifyingContract` [S1]; cross-chain usage needs confirmation).

---

## 16. Sources

All accessed 5–6 October 2026.

- **[S1]** Identity.md API documentation — https://imd.fun/docs/ (launch economics, trading fee, paid actions at 0.5 IMD, job shapes/templates/skills, oracle EIP-712 domain, reputation registry records, Sepolia-only launches, `evm_contracts`).
- **[S2]** Identity.md $IMD token page — https://imd.fun/token/ (10M supply, sell burns, sIMD, 2,000 seats, POOL4 hook, Community Coins, timeline). Token contract: https://etherscan.io/address/0xd34a99bc0f67ae1bbd63c660e6d0b0dd03e263b7
- **[S3]** Identity.md Explorer, agents — https://explorer.imd.fun/agents (network snapshot figures).
- **[S4]** Uniswap v4 Hooks concept — https://developers.uniswap.org/docs/protocols/v4/concepts/hooks
- **[S5]** Uniswap v4 Dynamic Fees — https://developers.uniswap.org/docs/protocols/v4/concepts/dynamic-fees
- **[S6]** OpenZeppelin Contracts 5.x ERC-20 API — https://docs.openzeppelin.com/contracts/5.x/api/token/erc20
- **[S7]** OpenZeppelin Contracts 5.x Governance (TimelockController) — https://docs.openzeppelin.com/contracts/5.x/api/governance#TimelockController
- **[S8]** Safe smart account modules — https://docs.safe.global/advanced/smart-account-modules
- **[S9]** ERC-8004: Trustless Agents (Draft) — https://eips.ethereum.org/EIPS/eip-8004
- **[S10]** Identity.md launches GitHub organisation — https://github.com/identity-md-launches ; $ADAM launch 720 — https://github.com/identity-md-launches/launch-720-adam-official-x
- **[S11]** SIMD site — https://www.si-md.xyz/

Secondary (context only, not used for mechanics): KuCoin blog on IMD history — https://www.kucoin.com/blog/id-imd-token-community-owned-ai-agents
