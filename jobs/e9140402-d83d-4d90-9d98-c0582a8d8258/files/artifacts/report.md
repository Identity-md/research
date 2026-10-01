# Dynamic LP Fees in Live Uniswap v4 Hooks: Arrakis Pro Hook, StablePair Hook, Angstrom

**Scope:** Three hooks currently deployed and operating on Uniswap v4 that set per-swap LP
fees/compensation dynamically, rather than a fixed pool fee. For each: the rule it uses, what
it defends against, and its documented or inferred weaknesses, with sources.

As of this writing (checked October 2026): Arrakis Pro Hook and the Uniswap StablePair Hook
have been live since 2025 and September 2026 respectively; Angstrom has been live on mainnet
since July 2025 and continues active development. All three facts are marked **[fact]** below
when drawn directly from a primary source, **[inference]** when reasoned from primary sources
without a direct quote, and **[uncertain]** where sources disagree or are silent.

---

## 1. Arrakis Pro Hook (Arrakis Finance)

**What it is [fact]:** A Uniswap v4 hook built for token issuers acting as a single LP (the
issuer or a whale LP), announced as "the first whitelisted Hook with dynamic fees" on v4.
Source: [Arrakis — "The Arrakis Pro Hook: Dynamic Fees for Token Issuers on Uniswap V4"](https://arrakis.finance/blog/the-arrakis-pro-hook-dynamic-fees-for-token-issuers-on-uniswap-v4).

**The rule [fact]:** The hook's `beforeSwap` callback adjusts the fee on two axes each swap:
- **Volatility →** fees rise as the pool price deviates from the reference (CEX) price, making
  it more costly to arbitrage the pool as the mispricing grows.
- **Inventory imbalance →** fees fall for trades that rebalance the pool back toward a 50:50
  token ratio, and rise for trades that worsen the imbalance.

Quote: *"Putting a price on volatility disincentivizes arbitrage attacks because the cost of
arbing the pool increases as the price deviates from the CEX price... fees decrease when the
inventory is more imbalanced [i.e., for rebalancing trades]."*
Source: [Arrakis Pro Hook blog post](https://arrakis.finance/blog/the-arrakis-pro-hook-dynamic-fees-for-token-issuers-on-uniswap-v4); related mechanism description in [Arrakis — "DEX Liquidity Design 101"](https://arrakis.finance/blog/dex-liquidity-101).

**What it protects against [fact]:** Arbitrage-driven MEV and loss-versus-rebalancing (LVR)
against the token-issuer LP — the scenario where a stale on-chain price gets picked off by
faster traders reacting to CEX price moves.

**Known weaknesses:**
- **Oracle/price-feed dependency [inference]:** the rule requires a live read of "the CEX
  price" to price volatility; the public blog post does not disclose the oracle or
  price-discovery source, update frequency, or staleness handling, so manipulation or lag in
  that feed is an unaddressed attack surface in the public materials.
- **Single-LP centralization [fact]:** deposits into the Pro/"Private Hook" pool are
  restricted to one LP, "usually the Token Issuer or a whale liquidity provider" — a design
  choice, not a flaw, but it concentrates custody/key risk rather than distributing it.
  Source: [Arrakis Pro Hook blog post](https://arrakis.finance/blog/the-arrakis-pro-hook-dynamic-fees-for-token-issuers-on-uniswap-v4).
- **Independent audit findings on the adjacent Arrakis V4 module [fact]:** ChainSecurity's
  audit of Arrakis's Uniswap v4 module (the vault/management layer the Pro Hook plugs into,
  not the fee-pricing logic itself) found a fee-related bug ("manager fee collected multiple
  times"), rounding errors, and a risk that privileged "executor" roles could extract small
  amounts of liquidity at discrete intervals; the auditors concluded security "depends on the
  correct usage by trusted accounts" rather than being trust-minimized.
  Source: [ChainSecurity — Arrakis Uniswap V4 Module audit](https://www.chainsecurity.com/security-audit/arrakis-uniswap-v4-module).
  **[uncertain]** whether these specific findings apply to the Pro Hook's fee contract itself,
  since the audit page does not fully disambiguate module vs. hook scope from the summary
  available.
- No public post-mortem or incident involving the Pro Hook's dynamic-fee logic was found
  **[unanswered]** — absence of evidence is not evidence of absence here.

---

## 2. Uniswap StablePair Hook (Uniswap Labs)

**What it is [fact]:** Uniswap Labs' own dynamic-fee hook for stablecoin-to-stablecoin pairs,
launched September 10, 2026 with initial pools for USDC/USDT and USDC/USDG on Ethereum
mainnet. Uniswap Labs describes it as its "first upgradeable dynamic-fee hook."
Source: [Uniswap blog — "StablePair Hook: A Fee That Moves with the Market"](https://blog.uniswap.org/stablepair-hook-a-fee-that-moves-with-the-market); [Uniswap developer docs — Dynamic Fees](https://developers.uniswap.org/docs/protocols/v4/concepts/dynamic-fees).

**The rule [fact]:** Fee is a function of how far the pool's price has drifted from a
configured reference rate, and of which direction a given swap pushes the price:
- **Inside a narrow band around the reference rate:** the fee is set each swap to reproduce a
  fixed, narrow bid/ask spread around that rate — i.e., quoting behavior similar to a
  market-maker spread rather than a flat percentage.
- **Outside the band, trades that widen the deviation:** charged zero fee (they are, in
  effect, offering the pool a better price, so the pool doesn't need to discourage them).
- **Outside the band, trades that correct the deviation back toward the reference rate:**
  priced via a **Dutch auction** — the fee starts high and decays block-by-block until a
  trader accepts it, so LPs capture most of the value of the price reversion instead of
  ceding it to the first arbitrageur.

Quote: *"The fee starts high, then drops each block until someone takes it. LPs keep the
difference."*
Source: [Uniswap blog post](https://blog.uniswap.org/stablepair-hook-a-fee-that-moves-with-the-market).

Mechanically, the hook computes the fee in `beforeSwap` and calls `updateDynamicLPFee` on the
`PoolManager`, following v4's native dynamic-fee path (pools must be created with the dynamic-fee
flag, which is immutable at creation). Source: [Uniswap developer docs — Dynamic Fees](https://developers.uniswap.org/docs/protocols/v4/concepts/dynamic-fees).

**What it protects against [fact]:** Depeg/arbitrage value leakage on stablecoin pairs — the
case where a stablecoin pair's on-chain price drifts from its true 1:1 (or near-1:1) rate and
arbitrageurs extract the correction for free. Uniswap frames the business motivation as
capturing a larger share of the ~$43.4B/quarter stablecoin-swap market by giving LPs a "CEX-like"
tight-spread experience while still recapturing reversion value.
Source: [Uniswap blog post](https://blog.uniswap.org/stablepair-hook-a-fee-that-moves-with-the-market).

**Known weaknesses:**
- **Reference-rate source and update cadence undisclosed in public materials [unanswered]:**
  the blog post and available docs state that fee depends on deviation from "a configured
  reference rate" but do not specify how that rate is computed, by whom, or how often it is
  refreshed — a stale or manipulable reference rate would misprice the whole mechanism (e.g.,
  during a real depeg, a reference rate that doesn't update could keep charging arbitrageurs
  who are providing a correct price, or fail to charge them when it should).
- **Governance upgrade risk [fact → inference]:** parameters and fee logic are explicitly
  upgradeable "through Uniswap Governance." This is a deliberate design choice (Uniswap Labs'
  first *upgradeable* dynamic-fee hook) but it reintroduces a governance/trust dependency that
  immutable hooks don't have — a successful governance attack or a bad parameter change could
  alter LP economics for live pools.
- **Newly launched [fact]:** live for under a month as of this report; no independent audit
  report, post-mortem, or adversarial review was found in public sources during this research,
  so its real-world robustness under stress (e.g., an actual stablecoin depeg event) is
  **[unanswered]**.

---

## 3. Angstrom (Sorella Labs)

**What it is [fact]:** An MEV-protection DEX layer built as a Uniswap v4 hook, live on Ethereum
mainnet since around July 25, 2025, backed by Paradigm and supported by the Uniswap Foundation's
Hook Design Lab; it secures its off-chain node network via EigenLayer restaking.
Sources: [Uniswap Foundation — Builder Update 31](https://www.uniswapfoundation.org/blog/builder-update-31-angstrom-oz-hook-library-eth-nyc); [Angstrom docs](https://docs.angstrom.xyz/); [Sorella Labs GitHub](https://github.com/SorellaLabs/angstrom/blob/main/contracts/docs/overview.md).

**Framing note [inference]:** Angstrom does not price LP compensation as a simple percentage
fee the way the other two do. It is included here because it is one of the most prominent live
v4 hooks that dynamically determines how much value LPs receive per swap/per block — the
mechanism is an **auction-priced** fee/tax rather than a formula-priced one, which is a
meaningfully different "rule" worth contrasting against the other two.

**The rule [fact], two variants:**
- **L1 (mainnet) — two auctions per block:** (1) An **arbitrage auction**: at the start of each
  block, arbitrageurs bid in an English auction for the exclusive right to execute a fee-free
  trade that realigns the pool price to the external (CEX) market; the winning bid is
  distributed pro rata to LPs. (2) A **batch auction**: all other user orders for that block are
  then matched at a single uniform clearing price derived from the (now-rebalanced) AMM
  curve plus off-chain limit orders, so every trade in the block settles at the same price.
  Sources: [Angstrom docs — Arbitrage Auction](https://docs.angstrom.xyz/l2/arbitrage-auction); [Angstrom docs — Batch Auction](https://docs.angstrom.xyz/l1/core-mechanisms/batch-auction).
- **L2 variant — deterministic priority-fee tax:** since L2 sequencers don't support the
  off-chain auction design, `AngstromL2.beforeSwap` reads the swap's attached priority fee
  (sequencer tip) and charges a deterministic "MEV tax" proportional to it; `afterSwap` splits
  that tax between LPs, the pool creator, and the protocol, crediting LPs via a "Compensation
  Price Finder" so that, in aggregate, LPs are compensated as if they had traded at a fairer
  price. Source reported via secondary summary of Angstrom L2 docs (primary docs.angstrom.xyz
  page describing this exact flow was not independently re-fetched in this research —
  **[uncertain, secondary-sourced]**).

**What it protects against [fact]:** Loss-versus-rebalancing (LVR) and sandwich attacks. By
forcing arbitrage rights to be auctioned (rather than free-for-all), the value that would
normally leak from LPs to the fastest searcher/validator is instead captured and paid back to
LPs; uniform per-block clearing prices remove the incentive to front-run or reorder within a
block.

**Known weaknesses:**
- **Decentralized-trust (not trustless) model [fact]:** Angstrom's own documentation states it
  is not fully trustless: *"one must trust that a majority of well incentivized actors is
  operating in their best interest."* Security relies on validators being "sufficiently
  staked" such that even a worst-case malicious bundle, run for the maximum possible time
  before detection, can be covered by slashing — i.e., it is an economic/game-theoretic
  guarantee, not a cryptographic one. Source: [Sorella Labs — Angstrom contracts overview.md](https://github.com/SorellaLabs/angstrom/blob/main/contracts/docs/overview.md).
- **Leader/searcher collusion window [inference]:** each block's bundle is built by a randomly
  selected leader and only verified by other validators *after* submission; misbehavior is
  punished post hoc via slashing, not prevented up front. This leaves a window in which a
  colluding leader and searcher could misorder a bundle before being caught, bounded only by
  the economic cost of slashing. Source: synthesized from [Sorella Labs overview.md](https://github.com/SorellaLabs/angstrom/blob/main/contracts/docs/overview.md) and [EigenLayer's own framework distinguishing provable vs. decentralized-trust AVS guarantees](https://blog.eigencloud.xyz/the-three-dimensions-of-programmable-trust/).
- **Dependent on router behavior [fact]:** the docs flag that liquidity-reward distribution
  assumes "well-behaving routers," since a malicious router could steal rewards paid out in
  the `beforeRemoveLiquidity` hook — i.e., a third-party integration mistake outside Angstrom's
  own contracts can still cause LPs to lose their accrued compensation.
- **Proposer-decentralization externality [inference, third-party view]:** an independent
  analysis argues that if many apps impose Angstrom-style sequencing constraints on block
  proposers, this could, in aggregate, pressure validator/proposer decentralization — a
  systemic risk rather than a protocol bug. Source: [auditless.com — "Angstrom and the Arrival
  of Application-Specific Sequencing"](https://research.auditless.com/p/angstrom-and-the-arrival-of-application).
- Audit coverage exists (Spearbit review plus a Cantina public audit competition) but the
  **specific list of unresolved findings** from those reviews was not retrieved in this
  research — **[unanswered]**.

---

## Comparison

| | Arrakis Pro Hook | Uniswap StablePair Hook | Angstrom |
|---|---|---|---|
| Live since | 2025 (exact date not found) | 2026-09-10 | 2025-07-25 (L1) |
| Fee rule | Volatility- and inventory-based formula | Deviation-from-reference-rate + Dutch auction | Block-level English/batch auction (L1) or priority-fee tax (L2) |
| Target market | Single-LP / token-issuer pools | Stablecoin pairs | General pools, LVR/MEV-sensitive |
| Protects against | Arbitrage MEV, LVR, inventory risk | Depeg arbitrage leakage | LVR, sandwich attacks |
| Core dependency | Off-chain CEX price feed (undisclosed) | Governance-set reference rate (mechanics undisclosed) | Honest-majority, sufficiently-staked validator set |
| Documented/observed weakness | Oracle opacity; single-LP concentration; adjacent-module audit findings | Governance upgrade risk; untested at scale/under depeg stress | Decentralized-trust (not trustless); leader-collusion window; router-integration risk |

---

## A directly relevant cautionary case (not one of the three "live" hooks)

**Bunni v2** was, until September 2025, the largest Uniswap v4 hook by trading volume and a
widely cited example of a dynamic-fee design (a TWAP-based volatility fee plus an exponential
"surge fee" after liquidity-density-function shifts, intended to resist sandwiching during
autonomous rebalancing). **It is not included as one of the three "live" hooks above because it
is no longer live**: on 2025-09-02 an attacker exploited a rounding-direction bug in
`BunniHubLogic::withdraw()` — 44 small withdrawals compounded a rounding error that let the
attacker drain ~85.7% of a pool's active balance while burning minimal shares — stealing a
combined $8.3–8.4M across Ethereum and Unichain. Trail of Bits and Cyfrin had both audited the
contracts beforehand without catching it; it is widely described as a logic-level flaw rather
than an implementation typo. Bunni permanently shut down on 2025-10-27, citing an inability to
afford the six-to-seven-figure cost of a secure relaunch, and relicensed its contracts from BUSL
to MIT.
Sources: [QuillAudits — Bunni V2 Exploit: $8.3M Drained via Liquidity Flaw](https://www.quillaudits.com/blog/hack-analysis/bunni-v2-exploit); [The Block — "Bunni DEX shuts down after $8.4 million exploit, citing lack of funds"](https://www.theblock.co/post/375813/bunni-dex-shuts-down); [Bunni's shutdown announcement](https://x.com/bunni_xyz/status/1981160279871558114); [Bunni v2 docs — Overview](https://docs.bunni.xyz/docs/v2/overview/).

This is relevant to the comparison above because the two currently-live hooks with
formula-based dynamic fees (Arrakis Pro Hook, StablePair Hook) both depend on custom,
unaudited-in-public-detail arithmetic for fee/price calculation — the same general risk class
(precision/rounding bugs in bespoke fee or rebalancing math) that ended Bunni. This is offered
as an **[inference]**/analogy, not a claim that either hook shares Bunni's specific bug.

## A claim found and rejected during research

One secondary source (a 2026 "guide" article on dextools.io) asserted that an "Atrium Dynamic
Fee" hook is "the most widely adopted" dynamic-fee hook, scaling fees from 0.30% to 1.50% with
volatility. This could not be corroborated: "Atrium" appears in reliable sources only as the
name of the **Uniswap Hook Incubator program**, under which several *unrelated, independent*
hackathon/prototype dynamic-fee hooks (e.g., "Autopilot Hook," a Spearbit-incubator-adjacent
0.30%+volatility-premium prototype) were built by third parties — none of which is a single
named, live, widely-adopted "Atrium Dynamic Fee" product. This claim was excluded as likely
conflated/unreliable rather than used as a third example.
Sources: [dextools.io guide (the unverified claim)](https://www.dextools.io/tutorials/what-is-uniswap-v4-hooks-customizable-amm-guide-2026); contrast with [RegisGraptin/autopilot-hook — "Built during the Atrium academy"](https://github.com/RegisGraptin/autopilot-hook).

---

## Limitations of this report

- Research relied on public blog posts, developer docs, one GitHub `overview.md`, one
  third-party audit summary page, and secondary news/analysis coverage, fetched via web
  search/fetch tools in October 2026. Primary smart-contract source code for the three hooks
  was **not directly read** in this research; fee-logic descriptions above are as stated by the
  protocols' own documentation/blog posts, not independently verified against deployed
  bytecode.
- Exact launch date for the Arrakis Pro Hook, the precise reference-rate mechanism for
  StablePair, and the specific unresolved findings from Angstrom's Spearbit/Cantina audits were
  **not found** and are marked unanswered above rather than guessed.
- "Live" is assessed as of 2026-10-01 based on the most recent sources found; protocol status
  (especially for newly launched StablePair Hook) can change quickly.
