# Bag Gacha: research and design report

ERC-20 "Bags" gacha on Ethereum mainnet, modeled on Fake World Assets (FWA), with a platform token handed out through Genesis Bags and a 0.001 ETH NFT mint that funds the launch.

Date: 2026-10-13. Scope: read-only research and design. Nothing was deployed and no transactions were sent.

**Labels used throughout:**
- **[F]** is a fact, with its source linked.
- **[I]** is my inference or a design choice.
- **[M]** is a model output from `sim/gacha_sim.py`, which is deterministic (seed 7). Reproduce it with `python3 sim/gacha_sim.py`.
- **[U]** is unverified or uncertain.

---

## 0. Summary of recommendations

| Item | Recommendation |
|---|---|
| Spin price | **0.01 ETH**, fixed. The Chainlink VRF fee is charged as a separate pass-through surcharge, as FWA does. |
| Tiers (multiple of spin price P, odds) | small 0.3–0.7×, 75.0% · medium 0.7–2×, 18.0% · large 2–6×, 6.5% · jackpot 6–70×, 0.5% |
| Spinner EV | Expected bag value is 0.944·P. After the best exit (dump at 2% slippage, or buyback), spinner EV is **≈92.5%** [M]. |
| Instant buyback | 88% of bag value, paid from the payout reserve. The Bag returns to the pool. |
| Depositor payout when a Bag is kept | 95% of bag value in ETH (5% fee) |
| Valuation | `min(30-min TWAP, 4-h TWAP)` from a Uniswap v3/v4 WETH pair. Pool liquidity must be at least 50 ETH per side, the quote must be fresher than 1 h, and the observation cardinality must cover the window. |
| Admission cap | A single Bag may not exceed 5% of the payout reserve. Jackpot bags are capped in absolute terms by reserve size. |
| Genesis discount band | Expected value **8% below** the pool price. Bounded range 5–12%, adjustable only by the oracle within the 10%/24h rule. |
| Genesis curve | `tokensPerBag = min((1−d)·P / TWAP, schedule)`. The schedule is linear over 540 days and decays 10% per day of being ahead of target (VRGDA-like). |
| Genesis spin ETH split | **40% protocol-owned liquidity (POL) · 30% payout reserve · 15% NFT holders · 15% team** |
| Regular spin ETH split | About 88% to the payout reserve (it funds payouts of about 0.86·P). The ~12% margin splits 4% platform-token buyback, 3% NFT holders, 2% POL, 3% team. |
| NFT mint | **10,000 at 0.001 ETH (10 ETH raise).** Funds sit in an ownerless escrow. Refunds open if no launch happens within 90 days. At release: 50% POL, 40% payout reserve, 10% VRF subscription. |
| 1% LP fee | Redirect it to the NFT revenue contract through `LaunchFactory.setRequester` [U: IMD interface not verified; see §5]. Split 50% NFT holders, 50% buy-and-burn. |
| Contracts | 7 immutable contracts (§5) |

---

## 1. Fake World Assets deep dive

### 1.1 What it is
- **[F]** FWA is a "pool-based NFT acquisition product": buy "a randomly selected NFT from the pool". It is operated by Token Workshop, Inc. under the TokenWorks brand. Pools show rarity tiers, backing and odds per item. A visited pool showed Common at 99.8%. The site shows 76,367 purchase requests and 5,539.6 Ξ of volume. ([fwa.fun](https://www.fwa.fun/), fetched 2026-10-13)
- **[F]** A depositor lists an NFT with an ETH "backing" held in escrow. Drawers pay a flat price per pull, most recently 0.117 ETH, and Chainlink VRF picks the NFT. The drawer keeps the NFT or returns it for 85% of backing in ETH or $FWA. Higher backing means a lower chance of being pulled. ([blocmates, 2026-07-29](https://www.blocmates.com/articles/what-happened-to-fake-world-assets))
- **[F]** blocmates estimates that drawers pay about 1.1× average backing and receive about 0.85× on cashback, a "21% haircut per pull". (same source)

### 1.2 Contracts (Ethereum mainnet, V1, from the official deployments page)
[F] ([fwa.fun/docs/deployments](https://www.fwa.fun/docs/deployments)):

| Contract | Role | Address |
|---|---|---|
| FWA | V1 main pool | `0xB276F62DB0ce8CA2Ca5bc522695bE604521eAc1c` |
| FWARewards | Emissions and reward routing | `0x6a1a1C0CfB3D3C538e13D36d608a5bcaa992fc78` |
| FWAVRFService | VRF subscription coverage and processing | `0xa084c33Fb7a467307452898b8D58165ebd2E5D9f` |
| FWAToken | $FWA ERC-20 | `0xa0Df17B5aC76ABaBA36E1450E2cbCd18A620C845` |
| FWAERC20Wrapper | **Wraps ERC-20s into FWA-compatible NFT packs** (the closest existing analogue to "Bags") | `0x727C739F07A89f11E883FE0F34937c55e4c3d74A` |
| FWAERC20PackRenderer | Pack SVG and metadata | `0x69Cc9c633867eEE71b17142BBBc2c6aaf14c61a4` |
| FWATokenWrapper | Block-locked $FWA packs as ERC-721 | `0x470879Abd61FdCA91436fE27ed87dB2c8650f3e7` |
| FWATokenHook | Uniswap v4 hook for the $FWA pool | `0x2C67ebA8A50AF0dB5Fba55F725247a75CbDA6444` |
| OwnerSplitter | Recipient of hook trading fees | `0x7400824eec17F86Cc74385862810710F9c46Ec04` |
| FWAClaim | Merkle snapshot distribution | `0xd4085d38855F17EdF0B1CCBFad7B3846fb305655` |
| FWAWhitelistAuthority | Collection curation and FWAIR activation | `0x54B641aC97A9e9375665934b8e7a7D0b2C0E898B` |
| FWAIRLaunchManager | FWAIR launch registry | `0x900252d9A8F9AcC3DD1014C594c91fC33e5A6AAf` |

- **[F]** The homepage links a "verified contract" at `0x958c41181182e76f221331b2755b77d9e1426a98`. The page does not label it [U: probably the V2 main pool].
- **[U]** I did not pull transaction examples from Etherscan in this run. Concrete purchase, fulfil and settle transactions are an **open item**. They can be found from the FWA V1 address above (`requestRandomWords` and fulfilment calls through FWAVRFService).

### 1.3 Flow and parameters
**V1** [F] ([fwa.fun/docs/v1](https://www.fwa.fun/docs/v1)):
- **Price and fees.** The price is a 2.5% acquisition surcharge over weighted expected backing, split between depositor fees and a purchaser FWA allowance. A crown tithe of 1% of the fee goes to the top depositor. The protocol takes 1% of the purchase fee, plus a 1% settlement cut when the NFT is kept.
- **Depositor bid.** The purchaser receives 90% and 10% is retained.
- **Routing.** 100% of protocol cuts go to the FWA buyback reserve. Bought-back FWA is routed 60% to purchasers, 20% to depositors and 20% burned.
- **VRF.** Chainlink VRF uses 3 confirmations and a 30-block selection timeout. The VRF service fee is "800k gas / 30% / 0 flat". If randomness is missing or price drift is excessive, the fee becomes a refund credit.
- **Timing.** The settlement window is 1 h (purchaser exclusive). After a 24 h finalize window anyone may finalize. Positive and negative slippage caps are 10%.
- **Limits and queueing.** Minimum backing is 0.025 ETH. Requests process in order, and deposits and withdrawals stage while acquisitions are unresolved.

**V2** [F] ([fwa.fun/docs/v2](https://www.fwa.fun/docs/v2)):
- **Allocation.** Lower-backed positions are drawn more often, and active positions share acquisition fees equally.
- **Oracle.** Backing may not exceed oracle ask + premium (default 10%). Quotes can be challenged by escrowing an NFT plus a 90% bid. Maximum quote age is 7 days. **The owner can set a trusted manual quote.**
- **Cold windows.** No purchases at 11:45–12:00 and 23:45–00:00 UTC. During these windows anyone can remove a listing whose backing exceeds the oracle ceiling.
- **Crown.** Exiting the crown within 12 h costs 1%.
- **Cashout.** 90% in ETH or 92.5% as FWA, adjustable from 80% to 95%.
- **Rewards.** Depositors earn through a sqrt(backing) accumulator, and purchasers share daily epochs. Emissions last 15 days and are funded from existing FWA.

### 1.4 Economics, controversy and results after emissions
- **[F]** The 15-day program distributed 1% of supply per day each to drawers and depositors, 30% in total. It ended on 2026-08-04. FWA relaunched on 2026-07-20. ([cryptonews/The Defiant, 2026-08-04](https://cryptonews.net/news/altcoins/33247357/); [blocmates](https://www.blocmates.com/articles/what-happened-to-fake-world-assets))
- **[F]** Fees were about $3.2M (1,735 ETH) in the first two weeks and $8.8M over 30 days (DefiLlama via The Defiant). TVL was $5M.
- **[F]** Researcher Kunal Doshi estimated about $300k per day of incentives against about $100k per day of revenue. In other words, **emissions paid users about 3× what the protocol earned**. (same source)
- **[F]** The token rose more than 35,000% to a peak market cap of about $38M on 2026-07-26 ($0.03856). By 2026-08-04 it was at $0.0083, after an all-time low of $0.0066, down 78% from the peak.
- **[F]** Holders learned that launch revenue had not gone to buybacks. TokenWorks then reversed course twice in under 24 h:
  - 50% of the team's fee share would go to buybacks, and the purchase fee would drop from 5% to 2.5%.
  - Then up to 80% of fees would go to buybacks.
  - Then a 327 ETH reserve buy would run over 30 days.

  ([The Defiant](https://thedefiant.io/news/nfts-and-web3/fake-world-assets-boosts-buybacks-to-80-of-fees-after-token-crashes-to-record-low); [Crypto Briefing, 2026-08-04](https://cryptobriefing.com/fake-world-assets-revises-buyback-program-backlash/))
- **[F, secondary]** A search-result summary of The Defiant coverage says fee income fell more than 98% from peak after emissions ended, and TVL fell to $3.14M. **[U]** I could not open the primary page for the 98% figure. The cryptonews reprint does not contain it.
- **[F]** Blockworks noted that buybacks were disabled and key parameters were centrally controlled. ([Blockworks 0xResearch](https://blockworks.com/newsletter/0xresearch/issue/post_a770e2c9-fad6-4dc2-807f-3032b36ceae9), via search summary)
- **[F]** FWAir lets an approved creator price each NFT of a new collection. Backers fund pieces with ETH and are refunded if the collection does not fill. ([The Defiant tag page](https://thedefiant.io/tag/token-works))
- **Exploits and farming.**
  - **[U]** I found no public report of a contract exploit.
  - **[I]** Farming is evident from the numbers: incentives were 3× revenue, so drawing was profitable while emissions lasted and activity collapsed when they stopped.
  - **[I]** The V2 additions (cold windows, oracle ceilings, drift removal, crown commitment fee) read as responses to two problems: over-backed listings (depositors inflating backing to extract ETH) and crown sniping.

### 1.5 Lessons applied to this design [I]
1. **Do not pay more in emissions than the protocol earns.** Genesis Bags are priced so the spinner loses about 8% versus the market. Distribution is paid for by spinners, not given away.
2. **Fix fee routing on-chain at deploy and publish it.** No later "reversals" should be possible.
3. **FWA's oracle depends on an owner manual quote.** Here valuation is TWAP-only and there is no owner.
4. **FWA had over-backing extraction** (backing above market). Here a Bag's value is never chosen by the depositor. It is computed at draw time.

---

## 2. Mechanism spec

### 2.1 Deposit (regular Bag)
- `seal(tokens[], amounts[], lockDays)`:
  - Allows 1–4 whitelisted tokens.
  - Tokens are pulled with `transferFrom`, and the **received balance delta** is recorded. Fee-on-transfer tokens get no credit beyond what actually arrived, and are delisted anyway (§4).
  - Mints an ERC-721 Bag to the BagVault, with `depositor` recorded.
- **Admission check at deposit:**
  - The current value must be at least 0.3·P.
  - It must be at most `min(70·P, 5% of payout reserve)`.
  - Every token must be listed and unpaused.
- **Activation delay.** The Bag enters the drawable set at the **next epoch boundary (1 h) after a 1-h delay**. This blocks front-running a pending VRF request (§4).
- **Lockup and withdrawal.**
  - The minimum lock is 24 h. During the lock the depositor cannot withdraw.
  - After the lock the depositor may `unseal` and withdraw, but only when no request referencing the Bag is pending. A 0.5% exit fee goes to the reserve; it discourages rotating out of falling tokens.
  - Dividends stop on withdrawal.

### 2.2 Valuation
- **Source.** A Uniswap v3 pool for token/WETH at the curated fee tier, or a v4 pool. The tokens/pools mapping is set by the curator oracle.
- **Price.** `price = min(TWAP_30m, TWAP_4h)` for deposit admission and buyback. At settlement, a depositor payout uses the same min.
  - Using the min means short-term pumps cannot inflate value.
  - Long-TWAP lag after a crash is handled by also checking `|TWAP_30m/TWAP_4h − 1| ≤ 15%`. If that check fails, the token is in **cooldown**: its Bags are not drawable, and the draw redraws in the same tier.
- **Minimum liquidity.** In-range liquidity worth at least 50 ETH on the WETH side, and the observation cardinality must cover 4 h. Otherwise the token counts as stale.
- **Staleness.** If the latest observation is older than 1 h, cooldown applies. This is checked at draw fulfilment.
- **Valuation time.** Value is computed when VRF fulfils (draw time), as the brief requires. Tier membership is updated lazily: `poke(bagId)` lets anyone re-tier a Bag, and fulfilment re-tiers the drawn Bag.

### 2.3 Tiers and draw weighting
Tier bounds are in multiples of P: small [0.3, 0.7), medium [0.7, 2), large [2, 6), jackpot [6, 70].

Each draw works in two stages:
1. **Lane.** With probability `g`, the draw is from the Genesis lane; otherwise it is regular. `g` starts at 60% and is bounded to 20–90%. If the regular pool is empty, `g` is 1.
2. **Regular lane.** Pick a tier by odds (75/18/6.5/0.5, each bounded ±50% of its initial value). Within the tier, weight each Bag ∝ `1/sqrt(value)`, so cheaper Bags are drawn more often, as in FWA. Use a Fenwick tree per tier for O(log n) selection.
   - If the chosen tier is empty, take the nearest non-empty lower tier.
   - The EV shortfall goes to the reserve and the spinner is told. [I: alternative is a refund. Refunds are simpler to reason about, but they leak information.]

**Bounded parameter changes.** Odds and `g` change only via the oracle, and by at most **10% relative per 24 h**. On-chain constants also set:
- hard floors and ceilings for each parameter;
- that small-tier odds stay at least 60%;
- that the EV implied by tier means stays within 0.88–0.95·P, checked on-chain using tier midpoints.

### 2.4 Keep vs buyback
After fulfilment, the spinner has 24 h to choose:
- **Keep.** The Bag NFT is transferred to the spinner. The depositor is paid `0.95·V` in ETH from the reserve, and the 5% fee stays in the reserve. The spinner may hold the sealed Bag, trade it, or `open()` it to receive the tokens.
- **Buyback.** The reserve pays the spinner `0.88·V`. The Bag stays in the pool, still owned by its depositor and still earning, and gets a 6-h redraw cooldown.

The default after 24 h is Keep. This mirrors FWA's finalize window [F, §1.3]. Settlement uses `min(V_draw, V_settle)`, which caps drift in the spinner's favour.

### 2.5 Payout reserve
- **Funding:**
  - 88% of every regular spin;
  - 30% of every Genesis spin;
  - 40% of the mint escrow;
  - 5% depositor fees and 0.5% exit fees.
- **Admission cap.** A Bag must be ≤5% of the reserve. With this cap, a run of large Bags cannot drain the reserve in one streak [M §3.2].
- **Solvency guard.** If the reserve falls below 20 × the max jackpot, the jackpot tier is disabled until it recovers. If it falls below 2·P × open requests, new spins revert.

### 2.6 Genesis Bags and curve
- **Supply.** About 80% of the token supply is held by GenesisVault. Each Genesis Bag is virtual and only minted as an NFT when drawn.
- **Tokens per bag:**
  - `T_twap = (1 − d)·P / min(TWAP_30m, TWAP_4h)` with d = 0.08.
  - `T_sched = T_twap · 0.9^(daysAhead)`, where `daysAhead = (emitted − target(t))/dailyTarget` and target(t) is linear over 540 days.
  - `T = min(T_twap, T_sched, remaining)`. This is VRGDA-like: when demand runs ahead of schedule, tokens per bag shrink exponentially.
- **Early holder window.** For the first 48 h after the gacha launches, Genesis spins are NFT-holder-only. The discount is d = 0.03 for holders, so their EV is about 97%, still below the market. Each NFT may spin up to 5 times in this window.
- **Free spins.** Each NFT gets **2 free Genesis spins**, funded by the 10% mint VRF/reward allocation plus a token allotment from GenesisVault. Per-NFT claims are tracked by tokenId.

### 2.7 Fee split
- **Genesis spin (100% of P is margin):** 40% POL · 30% payout reserve · 15% NFT holders · 15% team.
- **Regular spin:** 88% reserve; the margin of about 12% splits 4% platform-token buy-and-burn, 3% NFT holders, 2% POL, 3% team.
- **Depositors** earn platform-token dividends (§2.8), not ETH fees. Their ETH comes from the payout on Keep.

### 2.8 Dividend accounting (sealed Bags and depositors)
- **Emission budget.** 2% of supply (taken from the Genesis 80%), streamed linearly over 540 days to a MasterChef-style accumulator `accPerShare`.
- **Shares:**
  - A regular Bag in the pool has `shares = sqrt(V_lastPoke)` with value in wei. The square root dampens whale share, as in FWA V2 [F §1.3].
  - A sealed Bag held by a winner keeps the same shares.
  - A Genesis Bag held by a winner gets shares = sqrt(P·(1−d)).
- **Payout.** Shares are paid to the current NFT owner, with checkpoints on transfer, and `claim` is callable.
- **Opening.** `open()` settles pending rewards, burns the Bag and sets its shares to 0.
- **Anti-wash.** Shares accrue only after a Bag has been sealed or held for at least 24 h. A regular Bag's shares are refreshed only by `poke`, rate-limited to once per 24 h.

### 2.9 Mint escrow release and refund
- **MintEscrow** holds ETH and has no owner.
- `release()` is callable by anyone once both conditions hold:
  - `token` is the address of the IMD-launched token, verified because its `totalSupply` is in GenesisVault ≥ 75%;
  - the token/WETH pool exists.

  [I: the token address must be known at gacha deploy. Since constructors cannot make external calls, the token address is a static constructor argument, and `release()` performs the checks.]
- **Release split.** 50% to POL (buy-and-add via the router; the LP position is locked forever in POLManager), 40% to PayoutReserve, 10% to fund the VRF subscription.
- **Refund.** If `block.timestamp > deadline` (mint end + 90 days) and the escrow was never released, each tokenId can `refund()` once and receive 0.001 ETH. The NFT is burned.

---

## 3. Economic simulation (`sim/gacha_sim.py`)

### 3.1 Spinner EV and tiers [M]
| Tier | Odds | Mean value (×P) | EV contribution (×P) |
|---|---|---|---|
| small | 75.0% | 0.47 | 0.354 |
| medium | 18.0% | 1.24 | 0.223 |
| large | 6.5% | 3.64 | 0.237 |
| jackpot | 0.5% | 26.05 | 0.130 |
| **Total** | | | **0.944** |

- **Spinner EV.** After the best exit (keep and dump at 2% cost, vs. 88% buyback), EV is **0.925·P (92.5%)**, inside the 90–93% target. Genesis spins are 92% by construction (d = 8%).
- **Protocol margin.** About 10.3% per regular spin on the Keep path, before the VRF surcharge.
- **Depositor return [I].** A depositor effectively sells tokens at 95% of the TWAP value when drawn, or keeps them if never drawn. Their upside is the dividend:
  - In the steady scenario, 2% of supply over 540 d is about 0.004%/day of supply, shared by sqrt-weight.
  - At the steady-case token FDV (about 4,000 ETH, [M] below), this is about 0.15 ETH/day across all Bags.
  - Against an assumed 50 ETH of deposited value, that is roughly 100%+ APR early, decaying as the pool grows. This is an inference with high uncertainty.

### 3.2 Reserve solvency [M]
The model runs 20,000 regular spins, 400 runs each. The reserve pays 0.95·V (Keep) or 0.88·V (Buyback).

| Start reserve | Inflow share | Crash | Admission cap | Ruin | 1st-pct minimum | Median final |
|---|---|---|---|---|---|---|
| 4 ETH | 88% | – | 5% | 0% | 3.67 | 11.0 |
| 4 ETH | 86% | – | 5% | 0% | 3.55 | 9.3 |
| 4 ETH | 82% | – | 5% | 0% | 3.05 | 5.6 |
| 1 ETH | 88% | – | 5% | 0% | 0.93 | 10.5 |
| 4 ETH | 88% | 50% at spin 5,000 | 5% | 0% | 3.67 | 71.8 |
| **4 ETH** | 88% | – | **none** | 0% | **0.00** | 1.44 |

- **The cap matters.** Without the admission cap, the 1st-percentile path touches zero: one 70·P jackpot equals 0.7 ETH when the reserve is small.
- **What the cap does.** It makes solvency robust because early jackpots are naturally small (5% of a 4 ETH reserve is 0.2 ETH, i.e. 20·P).
- **Crash case.** A 50% token crash *helps* the reserve mechanically, because payouts are on TWAP value. The model holds demand constant, so that row is optimistic. [I] The real crash risk is TWAP lag (§4.1) and demand collapse. Both are handled by `min(TWAP_30m, TWAP_4h)` with the divergence cooldown, and by spins simply stopping.

### 3.3 Bot arbitrage vs Genesis discount [M]
Spot/TWAP lag is modelled as lognormal with sd = σ·sqrt(0.5 h/72 h). The exit cost is 2%.

| d | σ=15%/day: share of time profitable | σ=40%/day: share of time profitable (mean edge) |
|---|---|---|
| 0% | 5.3% | 27.4% (2.1%) |
| 3% | ~0% | 6.5% (1.4%) |
| 5% | 0% | 1.6% (1.2%) |
| **8%** | 0% | **0.09% (0.8%)** |
| 12% | 0% | 0% |

**Recommendation:** use a band of 5–12% and start at 8%. Below 5%, a volatile memecoin gives bots repeated positive-EV windows. Above 12%, Genesis spins become unattractive and distribution stalls. The `min(TWAP)` rule further removes upward-lag edge, because valuation never exceeds the shorter TWAP.

### 3.4 Genesis distribution and price path [M]
Setup: 1B supply, 80% Genesis. The LP starts with 100M tokens and 5 ETH of mint POL. Spinners dump 60% of their tokens immediately. 40% of Genesis ETH goes to POL.

| Spins/day (ETH/day) | Day 1 FDV | Day 30 FDV | Day 180 FDV | Day 540 FDV | Pool ETH day 540 | Distributed day 30 / 180 / 540 |
|---|---|---|---|---|---|---|
| 200 (2) weak | 47 ETH | 172 | 387 | 437 | 256 | 9.7% / 35.5% / 100% |
| 2,000 (20) steady | 88 | 1,510 | 3,831 | 4,361 | 2,566 | 10.5% / 35.5% / 100% |
| 20,000 (200) hype | 527 | 14,670 | 38,466 | 43,636 | 25,749 | 11.6% / 35.5% / 100% |

- **Front-loading.** Day 1 front-loads distribution when the price is tiny: 2.4–10% of Genesis supply goes out at FDV under 530 ETH. After that, the VRGDA schedule pins distribution to the 540-day line.
- **Where price comes from.** The price path is set by demand. Steady growth comes from POL plus the 40% of tokens kept.
- **Limitations [I].** The model has no external buyers or sellers and dumper behaviour is fixed. The hype row is not a forecast.
- **Recommendation [I].** Day-1 front-loading is a fairness risk. Cap the first 7 days at the schedule plus 3 days. This is included in the spec as a `maxAheadDays = 3` hard cap.

### 3.5 Mint raise and liquidity at launch
- **Raise.** 10,000 × 0.001 ETH = **10 ETH**. That gives 5 ETH of POL, 4 ETH of initial reserve and 1 ETH of VRF.
- **Pool depth.** The IMD launch pool has 10% of supply plus whatever ETH the IMD launch type pairs [U]. With the 5 ETH of POL, the initial FDV is about 50 ETH in the model.
- **[I]** 10 ETH is small. A 4 ETH reserve caps the largest admissible Bag at 0.2 ETH (20·P), so the jackpot tier is effectively 6–20·P at first.
- **Option.** If the requester wants bigger day-1 jackpots, raise supply to 20,000 or the price to 0.002 ETH. I kept 0.001 × 10,000 as briefed.

### 3.6 NFT holder yield (ETH share only, excluding the LP fee) [M]
| Scenario | Spins/day (Genesis share) | NFT pot | Per NFT per year | Multiple of mint price |
|---|---|---|---|---|
| weak | 200 (70%) | 0.23 ETH/day | 0.0083 ETH | 8× |
| steady | 2,000 (50%) | 1.80 ETH/day | 0.066 ETH | 66× |
| hype | 20,000 (40%) | 15.6 ETH/day | 0.57 ETH | 570× |

- **[I]** Because the mint is so cheap, even weak volume pays 8× the mint price per year. Expect the NFT to reprice on the secondary market immediately. This strongly increases its security-like character (§6).
- **Option [I].** Reduce the Genesis NFT share to 10% if the requester wants a smaller yield. The model shows the reserve does not need it.

### 3.7 Recommended parameter set
- **Spin and VRF:** P = 0.01 ETH, plus a VRF surcharge quoted on-chain from the coordinator (`calculateRequestPriceNative`).
- **Tiers:** as in §3.1.
- **Payouts:** buyback 88%, depositor fee 5%, exit fee 0.5%.
- **Valuation:** TWAP 30m/4h with min; minimum liquidity 50 ETH; staleness 1 h.
- **Reserve:** admission cap 5% of reserve.
- **Genesis:** `g` = 60%, d = 8% (band 5–12%), holder d = 3% for 48 h, schedule 540 days, `maxAheadDays` = 3.
- **Splits:** Genesis 40/30/15/15; regular 88/4/3/2/3.
- **Dividends:** 2% of supply over 540 d.
- **Mint:** 10,000 at 0.001 ETH, 90-day deadline, 2 free spins per NFT.

---

## 4. Attack analysis

| Attack | Mechanism | Mitigation |
|---|---|---|
| TWAP manipulation | Pump a thin pool so a Bag is over-valued at payout | Use `min(30m, 4h)` TWAP. Require ≥50 ETH in-range WETH liquidity and full observation cardinality. Value at draw is `min(V_draw, V_settle)`. A Bag is capped at 5% of the reserve. [I] Moving a 30-min TWAP on a 50 ETH pool by 10% costs about the pool depth × 10% held for 30 min. That is about 5 ETH at risk to win at most 5% of the reserve, and it also needs the specific Bag to be drawn. |
| Fee-on-transfer, rebasing, blacklist, pausable, upgradeable tokens | Value accounted differs from tokens held. Transfers can be frozen. | The curator oracle question requires token-safety checks (§5.4). Seal records the balance delta. Open uses `try transfer` per token: if one token fails, the others still release and the failed token stays claimable. Pause a single token's Bags via the oracle. Bags whose token is delisted are removed from draws and can be withdrawn by the depositor without fee. |
| Adverse selection (depositors dump falling tokens) | Deposit tokens expected to fall, get paid at TWAP | 24 h lock and 1 h activation. The min-TWAP and divergence cooldown blocks falling tokens. Odds weight 1/sqrt(V). 0.5% exit fee. Delist on a liquidity drop. [I] Residual: slow bleeders still get paid near market. This is the spinner's loss and is priced into the ~92% EV. |
| VRF timing and request griefing | Re-roll by reverting the callback, or wait for favourable states | `fulfillRandomWords` only stores the word and the snapshot index. It never reverts and uses less than 200k gas. Selection is computed in a separate `settle()` against the epoch snapshot taken at request time. Requests are only accepted while the reserve is sufficient. A per-address request cap limits spam. A request that is unfulfilled after 24 h is refunded to the spinner (as FWA V1 does [F]). |
| Reentrancy via token callbacks (ERC-777, hooks) | Callback during open/seal or payout | Checks-effects-interactions, `nonReentrant` on all external entry points, and pull-payments for ETH. ERC-777 and other hook-bearing tokens fail the curator safety check. |
| Front-running deposits before draws | Deposit a Bag when a request is pending | Draw-set snapshots are per epoch, and a new Bag joins only after epoch boundary + 1 h. Withdrawals block while a pending request references the snapshot. |
| Wash spinning to farm dividends | Spin, keep sealed Bags, collect dividends | Dividend shares are small (sqrt) and accrue only after 24 h of holding. Each spin costs about 8% EV, versus dividends worth a fraction of that unless the emission rate is set too high. [I] Constraint: daily dividend value must stay below the expected spinner loss. At the steady case, the spinner loss is about 1.5 ETH/day and the dividend budget is about 0.15 ETH/day. |
| Mint sybils | Many wallets mint for the free spins and NFT share | The mint is open by design, so sybils just pay 0.001 ETH each. Free spins are per NFT, so sybils are equivalent to buyers. Cap at 20 NFTs per transaction to limit gas wars. Holder-window spins are capped per NFT, so they scale linearly. [I] This is acceptable: there is no free value per wallet, only per paid NFT. |
| Oracle capture | Malicious oracle answer whitelists a scam token | On-chain bounds: 10%/24h on parameters, minimum pool liquidity is checked on-chain regardless of the oracle, and new tokens start with a 7-day 0.5% pool-weight ramp. If the oracle stops, the last settings stand. |

---

## 5. Contract architecture (IMD limits: at most 8 contracts, at most 16 static constructor words, no owner, no proxy, no external constructor calls)

### 5.1 Contracts (7)
| # | Contract | Responsibility | Key storage | Constructor arguments (words) |
|---|---|---|---|---|
| 1 | **BagNFT** | ERC-721 for regular and Genesis Bags, contents registry, `open()` | `bag[id] → {depositor, tokens[≤4], amounts[≤4], kind, sealedAt}` | vault (1) |
| 2 | **BagVault** | Seal and unseal, the drawable set (Fenwick tree per tier), settle Keep/Buyback, depositor payouts | per-tier trees, epoch snapshots, pending requests | nft, reserve, oracleAdapter, curator, priceLib params (≈6) |
| 3 | **GenesisVault** | Holds about 80% of supply. VRGDA-like curve, holder window, free spins. Named recipient of the IMD launch remainder. | emitted, startTime, schedule constants | token, vault, mintNFT, startTime, scheduleDays, d (6) |
| 4 | **SpinRouter** | Takes ETH, requests VRF (v2.5, native payment), receives randomness, applies the fee split | requests, subId | coordinator, keyHash, vault, genesis, revenue, pol, team (7) |
| 5 | **PayoutReserve + POLManager** | Reserve accounting, admission cap; buy-and-add LP held forever; buy-and-burn | reserve balance, LP position id | router, positionManager, weth, token (4) |
| 6 | **Curator** | Reads attested IMD oracle answers. Enforces bounds and the 10%/24h rule. Token list, per-token pause, odds, `g`, d. | params, lastChange timestamps, token registry | oracle address, question ids (≤6) |
| 7 | **MintNFT + Escrow + Revenue** | 0.001 ETH mint, refund after deadline, permissionless `release()`. Per-NFT ETH revenue accumulator (spin share and LP fee via setRequester). Dividend accumulator for Bags. | `accEthPerNFT`, claimed[], deadline | price, supply, deadline, token, reserve, pol (6) |

**Wiring [I].** Contract addresses are needed in a cycle (Vault ↔ Router). Two options:
- precompute addresses with CREATE2 (deterministic deploy order), passing them as static arguments; or
- use a one-shot `wire()` callable by anyone that sets immutable-in-practice storage only once and verifies `msg.sender` is the deploy batch.

Use CREATE2 if IMD evm_contracts supports it [U].

### 5.2 Events
- `BagSealed(id, depositor, tokens, amounts)`
- `BagActivated(id, tier)`
- `SpinRequested(reqId, spinner, lane, price, vrfFee)`
- `SpinFulfilled(reqId, word)`
- `BagDrawn(reqId, id, value, tier)`
- `Kept(id, spinner, depositorPaid)`
- `BoughtBack(id, spinner, paid)`
- `BagOpened(id, owner)`
- `GenesisMinted(id, tokens, twap)`
- `DividendClaimed(owner, amount)`
- `ParamChanged(key, old, new, oracleAnswerId)`
- `TokenListed / Delisted / Paused(token)`
- `EscrowReleased(pol, reserve, vrf)`
- `Refunded(tokenId)`
- `RevenueAccrued(source, amount)`

### 5.3 VRF without an admin key [I, based on Chainlink VRF v2.5 docs, not re-verified this run [U]]
- **Subscription.** SpinRouter calls `createSubscription()` in a one-shot permissionless `initVRF()`, not in the constructor. That makes SpinRouter the subscription owner, and it adds itself as consumer. There is no human owner, and nobody can cancel the subscription because only SpinRouter can, and it exposes no cancel.
- **Funding.**
  - Every spin forwards its VRF surcharge via `fundSubscriptionWithNative`.
  - The mint escrow seeds 1 ETH.
  - Anyone can top up.
- **Alternative.** VRF direct funding (`VRFV2PlusWrapper`) avoids subscriptions entirely and charges per request. It is simpler, at roughly 10–20% higher cost [U].
- **Verify before deploy:** the mainnet coordinator address, the keyHash gas lanes, and that `fundSubscriptionWithNative` is callable by non-owners.

### 5.4 Curator oracle questions (IMD attested answers) [I]
1. `TOKEN_LIST(token)` returns `{listed: bool, pool: address, feeTier}`. Criteria:
   - verified source, no transfer fee, non-rebasing, no blacklist or pause, not upgradeable (or a timelocked proxy is excluded);
   - at least 50 ETH WETH liquidity;
   - at least 30 days of history;
   - no honeypot sell tax.
2. `TOKEN_PAUSE(token)` returns bool. Use it for an exploit, depeg, or a liquidity drop below 30 ETH.
3. `TIER_ODDS()` returns 4 values in bps. The contract clamps them to ±10% per 24 h, enforces hard bounds, and requires the sum to equal 10,000.
4. `GENESIS_WEIGHT()` returns `g` in bps, clamped.
5. `GENESIS_DISCOUNT()` returns d in bps, clamped to 500–1200 and to ±10% relative per 24 h.

Every answer must carry the IMD attestation and its timestamp. If an answer is older than 7 days it is ignored, and the current settings persist.

### 5.5 Gas estimates [I, order-of-magnitude, not measured]
| Operation | Gas |
|---|---|
| spin request | ~120k |
| VRF callback | ~60k, paid via subscription |
| settle Keep | ~150–250k (TWAP reads ~15k per token, NFT transfer, ETH payout) |
| settle Buyback | ~120k |
| seal | 150k + 60k per token |
| open | 40k + 35k per token |
| mint | ~60k for the first, ~25k each after (ERC721A-style) |

At 1 gwei, a spin round-trip of about 400k gas is roughly 0.0004 ETH, which is about 4% of P. [U: ETH gas prices in Oct 2026 not checked.]

---

## 6. Launch plan through IMD

**IMD-specific caveat [U].** The facts I use about IMD come only from the task brief and were not verified against IMD documentation in this run:
- the evm_project launch type;
- 10% LP and 10% swarm;
- the LaunchFactory 1% pool fee paid to the requester, and `setRequester`;
- the evm_contracts limits.

The open questions are:
- whether `setRequester` is callable by the current requester or only by the factory;
- whether the launch transaction can name an arbitrary recipient contract for the remainder;
- whether the remainder recipient must exist before the token launches.

Order:
1. **NFT mint (week 0).** Deploy MintNFT+Escrow (contract 7) via evm_contracts. The token address is unknown at this point, so the escrow takes `release()` arguments that are validated against GenesisVault once it is deployed:
   - **[I]** This needs a second small "Binder" step: store the GenesisVault address set once by a permissionless call that verifies GenesisVault's immutable `mintNFT == address(this)`.
   - Deadline: mint close + 90 days.
   - Art: 10,000 pixel-art bags at 24×24, on IPFS. The swarm should draw:
     - **Material traits:** burlap, leather, silk, chrome, gold.
     - **Contents peeking out:** coins, gems, scrolls, a tiny ETH diamond.
     - **Tie/seal:** rope, wax seal, padlock.
     - **Backgrounds:** by tier color.
     - **Rarity:** common 60%, uncommon 25%, rare 10%, epic 4%, legendary 1% (gold bag with a glowing seal).
     - Rarity is cosmetic only, with equal revenue per NFT. That avoids extra security-like tiering.
   - Cost: deploy gas only.
2. **Token launch (about week 2–6).** IMD evm_project:
   - 10% to the LP and 10% to the swarm;
   - **remainder (~80%) to `GenesisVault`** in the launch transaction. GenesisVault must be deployed first, which implies a deploy order of contracts before the token, with the token address precomputed or bound once [U: depends on IMD].
   - Call `setRequester(Revenue)` so the 1% pool fee flows to NFT holders [U].
3. **Gacha contracts.** Deploy the remaining contracts in the same batch (7 ≤ 8). Then:
   - call `initVRF()`;
   - call `release()` on the escrow, which seeds POL, the reserve and VRF;
   - open the 48-h holder-only Genesis window, then public spins.
4. **Website.** A static site (IPFS) reading on-chain state. It should show the odds, the TWAP values, the reserve balance and the EV disclosure.

**Costs [I].** Deployment for 7 contracts is about 15–25M gas. VRF runs about 0.0002–0.0005 ETH per request.

**Timing.** Mint 1–2 weeks, then launch within the 90-day deadline.

**Key risks:**
- low volume after the novelty fades (the FWA precedent [F]);
- a token-curation failure;
- IMD interface unknowns [U];
- a thin initial reserve, which limits jackpots.

**Legal (high level only, not legal advice) [I]:**
- **Gambling.** Paying ETH for a randomized prize of variable value has the hallmarks of gambling (consideration, chance, prize) in many jurisdictions. It may also fall under loot-box rules. Geofencing the website, age gating, and odds and EV disclosure reduce exposure but do not remove it.
- **Securities.** NFTs that share protocol ETH revenue and the 1% LP fee look like profit-sharing instruments, and the §3.6 yields make this acute. Options are to drop the revenue share or to seek counsel before mint.
- **Platform token.** The token's value depends on team-built mechanics.
- **Sanctions/AML.** There is a mixing-like value transfer between depositors and spinners.
- **Next step.** Get counsel in the team's jurisdiction before the mint.

---

## 7. Unanswered questions and limits
- I collected no FWA transaction hashes. Pull them from the V1 pool address on Etherscan.
- The primary source for "fees fell more than 98% after emissions" is unverified, and I found no post-August-2026 FWA status.
- None of the IMD-specific mechanics (§6 caveat) were verified.
- The Chainlink VRF v2.5 mainnet addresses and the fee figures were not re-checked.
- Gas numbers are estimates. No contracts were written or compiled.
- The simulation is stylised: fixed demand, no external traders, lognormal TWAP lag. Use it for relative comparisons, not forecasts.
