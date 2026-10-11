# BLACKOUT v3.3: independent pre-launch review

**Scope:** research only. I changed no code and deployed nothing.
**Reviewed snapshot:** `identity-md-launches/launch-1269-reports-v1-job-b9e37680-814c-4f17-b4bc-6`, branch `identitymd/job-46fe87c6` = `main` @ `b208e8397e62ef4224a4d9f12653b6689c204998` (v3.3). Demo: `playblackout.xyz` bundle `assets/index-DT46041E.js`, fetched 2026-10-11.
**Reviewer:** an outside reviewer who did not design the game. Being skeptical is the job here.

Every claim below carries one of these labels:

- **[F] Fact.** Read directly in code, docs or artifacts, with a file and line reference. Line numbers refer to the commit above, and `R/` is short for the repo root.
- **[M] Measured.** I re-ran the repo's own simulator (`sim/blackout_sim_v33.py`) unmodified. Where I subclassed only the arrival function for a stress case, I say so.
- **[I] Inference.** My reasoning from the facts.
- **[G] Guess.** Opinion or an outside estimate with no hard evidence behind it.
- **[?] Open question.** Something I could not verify.

Limits of this review are listed in section 11. Read them before you rely on any single number.

---

## 1. Verdict

**No. Do not launch as is. It could become "yes with changes" after the five blocking fixes in section 9 (#1–#5).** The reasons:

1. **The money only works for week-1 buyers.** [M] In the repo's own steady scenario, 60.6% of week-1 farms repay within 35 days, but only **7.3% of week-2** and **2.7% of week-3** farms do, and 0% of weeks 4–5. If new-player inflow drops to 10/day after day 14, even week-1 falls to 36.5% repaid and the price ends 80% below its peak.
2. **There is a player-funds bug.** [F] If nobody captures a pack's entropy within 256 L2 blocks, the pack mints three Common GPUs (`PackSale.sol:167,185`). Robinhood Chain blocks are reported at about 100 ms, so that window is roughly 26 seconds.
3. **There are three trust holes a player would call a rug.** [F]
   - Packs can be sold before the endowment is funded and before the fee router is bound (`PackSale.sol:126-134`).
   - The one-time hook bind accepts any look-alike router (`V4Market.sol:651-664`).
   - `activateEndowment` lets pool buybacks count toward the team's endowment transfer (`RewardPool.sol:70-74`).
4. **Launch protection is weaker than advertised.** [F] The max buy is per swap, not per wallet or block (`V4Market.sol:878`). The tax clock starts at pool initialization, which is permissionless in Uniswap v4. [I] The sniper simulation only models buys in minute 1, which is a straw man.
5. **The core is better engineered than most games in this category.** [F] There is no owner and no upgrade path, the epoch advance is O(1), Params moves are bounded, and the suite has 158 test functions. That makes the problems above fixable in days, not a redesign.

---

## 2. Player view

### First 10 minutes
- **What works.** [F] The demo pitch reads well: "Open packs. Mine the city. Pray the grid stays on." It has pixel art, dispatcher letters, combos and clear lock messages ("Equip at level 5"). The pack odds are published, including the rule that Mythic rolls turn into Common below level 10.
- **No reward on day 0.** [F/I] On chain, a pack bought during epoch *E* commits weight starting in *E+1* (`FarmRewards.sol:248-253`), and mining is only credited after *E+1* closes. So the first claimable reward arrives **6–12 hours after purchase**. A claim at age 0 is then taxed **20%** (`FarmRewards.sol:397-399`). The demo hides this with a fast clock. [G] This is the most likely quit point for players who came from X expecting something like a slot machine.
- **Inventory confusion.** [F] A pack needs three free inventory slots. Room 2 opens on day 3 (`FarmCore.sol:185`). A new player has 15 slots and one room of six, so after five packs they are already managing inventory.

### Day 1
- [F] Level is capped at 4 until farm age reaches 1 day, then 6 until day 3 and 9 until day 5 (`FarmCore.sol:140-147`). Rare items need level 3, Epic level 5 and Mythic level 10 (`FarmCore.sol:273`).
- [I] A day-1 buyer who pulls an Epic or Legendary item cannot use it, which feels like being punished for buying.
- [F] Packs bought before level 10 cannot roll Mythic at all (`PackSale.sol:151`, `ItemMath.sol:29`), at the same price. [G] Day-1 buyers will feel they got worse packs, and they did.
- **Catch-up friction.** [F] Any farm action settles at most 8 epochs (2 days). A player who is further behind gets `CatchUpRequired` and must first send extra `settle` transactions (`FarmCore.sol:215`, `FarmRewards.sol:16,289`).

### Day 7
- [F] A farm with no owner action for 12 epochs (3 days) leaves the denominator and earns nothing (`FarmRewards.sol:19,248`). The demo does warn about this ("Mining paused: no farm action for 3 days").
- [F] Season entry needs the whole week settled before week end + 7 days (`Season.sol:170-172,176`).
- [M] By day 7 of steady play, week-1 farms are on track. A player arriving on day 7 sits in a cohort where fewer than 1 in 13 repay by day 35.
- [G] Day-7 churn will be driven by the falling claim value. The simulated token price peaks around 9–10× opening and is 7× on day 35 in steady, but only 2.6× on day 35 in hype after a 94% drawdown.

### Where the demo contradicts the contracts
These mismatches will produce "you lied" posts on day 8. [F] All come from demo bundle strings compared with the `Season.sol`, `FarmRewards.sol` and `FarmCore.sol` lines cited.

| Topic | Demo says | Contract does |
|---|---|---|
| Best district | "ranked by average synced **mining** per active farm" | average **spend** per active farm (`Season.sol:126-159`) |
| Lottery prize | "3 farms win 20 tokens each" | 3 winners get a Rare (90%) or Epic **item** (`Season.sol:295-302`) |
| Best-farm prize | 50 tokens | **1% of every epoch's mining for the week** (`FarmRewards.sol:169-172`, `Season.sol:262`) |
| Supply drop | every district gets 5 tokens | 5% chance per active farm of a Common/Uncommon item, only when sales ≥ 2× target (`FarmRewards.sol:348-349`) |
| Overclock | per room | per item (`FarmCore.sol:365-373`) |
| "There are no team tokens" | — | the team wallet **holds 100–250M tokens** until it transfers them (`docs/launch-v31.md`, "Public enrollment" step 3) |

---

## 3. Economics

### Is the reward pool sustainable?
**Mechanically yes, economically no.**

- **Mechanically.** [F] Mining per epoch is `available × EmissionBps / 40000`, i.e. 3.5%/day of *released* tokens (`FarmRewards.sol:162`, `Params.sol:64`). The pool can never be overdrawn in tokens.
- **Economically.** [F] Launch liquidity is single-sided, with **zero real ETH** (`docs/simulation-assumptions.md`, "Opening supply and market"). [I] So the total ETH players can ever cash out is capped by the ETH that newcomers and speculators bring in:
  - **added:** about 88% of pack ETH plus the 1% swap fee, through buybacks;
  - **minus:** what contributor agents and earlier players extract first.

  The token endowment adds tokens, not ETH. This is a closed loop that relies on arrivals.

### Payback by join week
[M] All runs use 20% endowment, a 42-day drip, the 35-day horizon and the repo's deterministic seed. Whole-cohort median payback treats unrepaid farms as censored. My week-1 figures for steady, hype and weak exactly match the repo's `report.md` (22.5 d, 60.6%, 23.2%, 18.9%), which confirms the run reproduces.

| Scenario | Week-1 joiners: median / repaid by d35 | Week-2: median / repaid | Week-3: median / repaid | Weekly pack ETH, weeks 1→5 |
|---|---|---|---|---|
| steady (repo) | **22.5 d / 60.6%** | not reached / **7.3%** (est. 55 d) | not reached / **2.7%** (est. 57 d) | 22.6 / 18.1 / 16.9 / 13.1 / 12.8 |
| hype (repo) | not reached / 23.2% | not reached / 1.2% | not reached / 0% | 78.7 / 23.6 / 6.0 / 2.4 / 1.9 |
| weak (repo) | not reached / 18.9% | not reached / 6.6% | not reached / 0% | 6.2 / 4.0 / 2.5 / 1.5 / 1.2 |
| **Inflow slows** (mine): steady, then 10 new/day after d14 | not reached / **36.5%** | not reached / 1.3% | — / 0% | 22.6 / 18.1 / 1.5 / 1.0 / 0.9 |
| **Inflow stops** (mine): steady, then 2 new/day after d7 | not reached / **12.5%** | — | — | 22.6 / 0.4 / 0.3 / 0.3 / 0.1 |

"Est." is the repo's projected median (realized plus a constant-yield projection). It is not a realized result.

[I] Week 2 and week 3 have had 21–28 days to run, so some censoring applies. Even so, the gap against week 1 (60.6% repaid within 35 days) is large.

**Realistic payback answer:**
- Week-1 buyers: about 3–4 weeks if inflow holds.
- Week-2 and week-3 buyers: about 8 weeks at best (est. 55–57 d). Most will not break even if inflow decays, which is the normal case for crypto games [G].

### What happens when inflow slows
[M] With 10 new farms/day after day 14:
- the stall triggers on day 23;
- active farms fall from 1,901 to 1,044;
- the drawdown is 80% (price on day 35 is 1.97× opening, against a 9.5× peak);
- team ETH falls from 11.16 to 5.96.

With inflow stopped after day 7, the drawdown is 85% and the stall comes on day 19.25.

[F] The swarm can respond by cutting emission at most 10%/day, within 2–6%/day (`Params.sol:116,168`). That slows the fall but cannot create ETH.

### Is the team share fair?
- [F] The team gets 10% of pack, lobby and sell-surcharge ETH plus half of the 2% swap fee (`FeeRouter.sol:76-77,108`).
- [M] In steady, that is **11.16 ETH, about 13.4% of the 83.5 ETH of packs sold**, while 93% of week-2 buyers have not repaid by day 35.
- [G] 10% is within industry norms for a game with real operating work, and it fell from 13%. The fairness problem is timing, not size: the team is paid immediately on every pack, while players are paid only if later players arrive.
- [G] Recommendation: route the team's 10% pack share into a 30-day linear vesting escrow, or to the pool until the week-2 cohort's realized payback passes 50%.

### Biggest hidden assumption in the sims
**Exogenous, price-insensitive arrivals.** [F] Steady assumes 150 new paying farms/day for 3 days, then 80/day for all 35 days, regardless of price or drawdown. The only damping is `sqrt(21/forecast)` on payback (`sim/blackout_sim_v33.py:130-133,199-200`).

[M] Just changing the arrival line to 10/day after day 14 cuts week-1 repaid from 60.6% to 36.5%. Every headline number depends on that line.

Runner-up assumptions:
- **Referral adoption.** [F] The sim assumes 40% adoption at 5% (`blackout_sim_v33.py:298-299`). [I] Self-referral is free (finding M-4), so expect about 100% adoption among informed players.
- **Holder sales.** [F] Contributor agents sell 35%, 50% or 65% (steady, hype, weak) of 100M tokens over days 2–14 (`docs/simulation-assumptions.md`). That is **2.9–5.4M tokens/day**, compared with an endowment drip of 4.76M/day. [?] The real lock terms are unverified.
- **Externally funded volume.** [F] External round-trip volume is fixed at 50% of pack ETH, and it is what funds base fees.
- **One seed.** [F] Only one seed is used, and there is no MEV, ordering or concentrated-liquidity model (same doc, "Interpreting results").

---

## 4. Security review of the v3.3 contracts

The review was a manual read. [?] I could not run `forge` because it is not installed on this machine. The repo's own logs claim 159 passing tests.

Severity scale:
- **H:** players lose funds, or there is a trust break that can be exploited on day 1.
- **M:** value leakage or broken guarantees.
- **L:** griefing or UX.
- **I:** informational.

### H-1. Entropy expiry mints junk for paid packs
- **Where:** `src/PackSale.sol:160-171` (`_capture`), `:185`, and `src/lib/ChainClock.sol:16-21`.
- **What:** `ChainClock.hash` returns 0 once more than 256 L2 blocks have passed. `c.expired = true` then makes `(k,r)` stay `(0,0)`, so every item in a **paid** pack becomes a Common GPU.
- **Why it matters:** [F, external sources] Robinhood Chain mainnet (chain id 4663, matching `ChainClock.sol:12`) is reported to produce blocks about every 100 ms. One provider says "on demand, ~250 ms". 256 blocks is therefore **about 26–64 seconds**. [I] Capture depends on a 0.00001 ETH bounty bot or on the buyer's own frontend staying open. `StarterClaim` has the same pattern (`StarterClaim.sol:65-75`).
- **Fix:** do what `Season.rearm` already does. On an expired hash, set a new future target block, never mint a fallback. Make the purchase transaction plus a one-click "reveal" the default UX.

### H-2. Launch-protection clock is anchored to a permissionless event
- **Where:** `launch/V4Market.sol:715-725` (`afterInitialize` ignores `sender`) and `:820-841`.
- **What:** In Uniswap v4, anyone can call `PoolManager.initialize` for a valid key. If the IMD launcher does not initialize and seed liquidity **in one transaction**, an attacker can initialize early, or at a chosen price. That starts the 30-minute tax and 60-minute max-buy clocks before liquidity exists, which erases the protection. A wrong initial price can also hurt the launch position.
- **Separately:** [F] `GameRegistry.launchTime` is a hand-entered constructor argument (`docs/launch-v31.md`, "v3.3 changes" step 2), so PackSale's clock can drift from the hook's clock.
- **Open question:** [?] I could not verify whether the IMD launcher is atomic.
- **Fix:**
  - Require `sender ==` the platform launcher or the team in `afterInitialize`, or start the clock at the first liquidity add or first swap.
  - Have `PackSale` read `opensAt` from `hook.initializedAt()` rather than from a constructor input.

### H-3 (trust). Packs can be sold before the game is funded or wired
- **Where:** `src/PackSale.sol:126-134` and `src/RewardPool.sol:48-57`.
- **What:** `openPack` checks only `opensAt` and `paused`. It does not check `RewardPool.endowed()` or that the hook is bound to this FeeRouter. Before funding, `available()` is 0, so all mining is 0, yet 10% of every pack goes to `credit[team]` immediately (`FeeRouter.sol:113`). The launch doc only says to "verify funding before soliciting" (`docs/launch-v31.md`, step 5); nothing enforces it.
- **Fix:** add `require(pool.endowed() && IHook(market).fees() == address(feeRouter))` to `openPack` and `tokenPack`.

### H-4 (trust). `bindFeeRouter` accepts any look-alike router
- **Where:** `launch/V4Market.sol:651-664`.
- **What:** The check is only that `token()`, `market()` and `params()` return the expected values. A contract written by the team can return those values and receive every flushed stream: 100% of the launch tax, all sell surcharges and base fees (`:667-680`). It is a one-time action, but it is the single largest rug lever in the system.
- **Fix:** verify `router == IGameRegistry(router.registry()).module(6)`, that the registry's `market() == address(this)`, and that the registry's `factory` matches a constant pinned in the hook. Alternatively, pin `keccak256` of FeeRouter's creation code and re-derive the address through `factory.predictContract`, as `GameRegistry.register` already does (`GameRegistry.sol:71-77`).
- **Day-1 mitigation without code:** publish the bind transaction and a script anyone can run to prove `hook.fees() == registry.module(6)`.

### M-1. `activateEndowment` counts buybacks and donations as principal
- **Where:** `src/RewardPool.sol:70-74`.
- **What:** Activation checks `balance >= reserved + endowment`. Tokens already bought back by `executeBuys` before funding sit in the pool. The team can therefore transfer *endowment − buybacks* and still activate. The `Endowed` event (`:82`) emits the nominal amount, not what the team actually sent.
- **Fix:** remove `activateEndowment` and keep only `fundEndowment`, which measures the actual `transferFrom`. Alternatively, snapshot the balance at registration.

### M-2. Self-referral is free, a hidden 5% emission bonus
- **Where:** `src/FarmCore.sol:197-200` (`register` is callable by `p` itself, gas only), `:255-259`, `src/FarmRewards.sol:318-321,368-373`.
- **What:** A player registers wallet B (an empty farm), then sets B as the referrer of their main wallet A. B receives 5% of A's gross, paid *on top* from the 117% budget.
- **Effect:** [I] Informed players get +5%, uninformed players are diluted, and the sim's 40% adoption assumption is wrong.
- **Fix:** require the referrer to have `paid > 0`, a committed farm and a farm age of at least 1 day, plus a referee cap per referrer. Better still, fund referrals out of the house share (the tariff) rather than as extra emission.

### M-3. The "best farm" prize goes to the lowest-yield farm
- **Where:** `src/Season.sol:200-204`.
- **What:** Score is `spend / earned`. A farm that joins late in the week with 1 pack and 1 Common item, or one that runs near-broken items, has tiny `earned` and wins. The prize is **1% of every epoch's mining for the week** (`FarmRewards.sol:169-172`).
- **Size:** [G] roughly 0.3M+ tokens/week at the modeled steady drip, or about 0.03 ETH at day-7 prices. It is small but trivially farmable, and it contradicts the demo's "50 tokens".
- **Fix:** rank by capped absolute spend, require at least 20 active epochs, or split the prize pro rata over spend.

### M-4. Max buy is per swap only
- **Where:** `launch/V4Market.sol:878,943`.
- **What:** 10 swaps of 0.5 ETH in one transaction or block are allowed. The decay is linear, so the cheapest snipe window is minutes 25–30. Using `:824`, the tax is 2.25% + 87.75% × (30−t)/30, i.e. **about 17% at t=25 and 5% at t=29**.
- **Gap in the sim:** [I] The repo's sniper sim (`sim/run_v33.py`, `snipers`) only tests minute-1 buying.
- **Fix:** add a cumulative per-block cap (for example 1 ETH per block across all swaps) and a stepped curve that stays at 25% or more until minute 20. Re-simulate a sniper who buys at minutes 20–30.

### M-5. Pre-endowment and "stuck" reservations distort what players see
- **Where:** `src/FarmRewards.sol:341-344`, `src/RewardPool.sol:48-57`.
- **What:** Reservations of departed farms stay reserved until someone settles them. [M] That is **53.9M tokens (27% of the 200M endowment) at day 35 in steady**.
- **Assessment:** [I] Not a loss (the tokens are owed), but `available()` and the emission rate are lower than a naive reading of the pool balance. Expect "where did the pool go?" questions.
- **Fix:** have the dashboard show reserved, locked and available separately. The team or swarm can sponsor `settle` for departed farms to release the unused share.

### L-1. Lottery tickets are per farm-epoch
- **Where:** `src/Season.sol:181`.
- **What:** 100 cheap farms get 100× the tickets of one large farm. The prize is a Rare or Epic item. Combined with "every participant in the winning district gets a free guaranteed pack" (`:285-293`) and districts that can be ground from addresses (`keccak(addr) % 8`, `:87-89`), sybils can multiply free packs.
- **Fix:** weight tickets by committed hash with a sqrt or cap, and require `paid > 0` to claim district packs.

### L-2. District race can be griefed
- **Where:** `src/Season.sol:177-180,158`.
- **What:** Cheap active farms placed in a rival district raise its `activeFarms` denominator and lower its score. A district with fewer than 10 spending wallets scores 0 (the requester's decision is still open in `report.md`).
- **Fix:** count only farms with `paid > 0` in the denominator, and decide on the softer cap.

### L-3. Liveness depends on `advanceEpoch`
- **Where:** `FarmRewards.sol:136-138`, `FarmCore.sol:213`.
- **What:** Once the current epoch's end passes, every Core action and pack purchase reverts `TooEarly` until someone advances. The first advance pays 0 because the heartbeat starts empty.
- **Fix:** have the frontend bundle `advanceEpoch()` before user actions, and have the team run a funded bot from launch hour 0.

### L-4. Buyback slippage band is set by the caller
- **Where:** `FeeRouter.sol:162-176`.
- **What:** `minOut` must only be at least TWAP × 97%. There is no minimum interval, and `lastBuy` is written but never read (`:20,172`). A searcher can sandwich inside the 3% band.
- **Assessment:** [I] Low risk on an FCFS sequencer without a public mempool, but bots can still bundle a buy, `executeBuys` and a sell in one transaction. The 2.25% fee on each leg makes this mostly unprofitable at 0.5 ETH batches.
- **Fix:** lower `SlippageBps` toward 1% and add a minimum interval.

### L-5. Mythic eligibility is fixed at purchase
- **Where:** `PackSale.sol:151`.
- **What:** Disclose that pre-level-10 packs cannot roll Mythic, or snapshot level at reveal instead.

### I-1. Swarm powers are bounded but meaningful
- **Where:** `Params.sol:162-177`.
- **What:** Emission can go from 350 to 600 bps in about 6 daily steps (×1.1 per step), PriceCeiling can rise to 0.05 ETH, and PackSale can be paused 72 hours of every 144 (`PackSale.sol:38-45`). The swarm has no asset access.

### I-2. Inputs the registry trusts
- **Where:** `GameRegistry.sol:28-50`.
- **What:** `factory`, `launchTime`, `endowment` and `starterRoot` are constructor inputs. They must be checked publicly before anything else, because nothing can be replaced afterwards.

### I-3. FarmRewards lazy accounting and idle expiry look correct
- **What I checked:** bucket moves on re-commit (`:244-247`), the two-generation expiry roll (`:239-242,258-262`), claim re-commit only when caught up (`:435`), and the dust-close condition (`:341`). I found no double count. Lazy-vs-eager fuzzing is claimed but I did not run it.

---

## 5. Attacks and abuse, ranked by impact

| # | Vector | Impact | Evidence | Mitigation |
|---|---|---|---|---|
| 1 | **Contributor-agent sell pressure** | High | [F] 10% of supply; [F, sim assumption] 35–65% sold over days 2–14, i.e. 2.9–5.4M tokens/day, about the whole endowment drip | Publish the real lock terms. Ask IMD for a 14–30 day linear unlock. Start PackSale only after the claim lock ends. |
| 2 | **Entropy expiry and sequencer** | High | [F] H-1. The sequencer orders transactions and could in principle withhold blocks; future block hashes are not a VRF (`README.md`) | Rearm on expiry. Long term, a commit-reveal or VRF if one exists on chain [?] |
| 3 | **Launch snipers** | Med-High | [F] M-4, H-2 | Per-block cap, stepped tax, atomic initialization |
| 4 | **Self-referral and multi-accounts** | Medium | [F] M-2, L-1 | Paid-referrer rule, hash-weighted tickets |
| 5 | **Whales** | Medium | [F] No per-wallet caps (`PackSale.sol:115`). [M] 300 packs for 5.94 ETH gives a 4.04% emission share on day 1 and 2.11% on day 7 (`artifacts/v33/simulation.json`) | Already mitigated by age gates. [I] The real issue is the whale's 10% district cap and sell timing, not emission share. |
| 6 | **Prize farming** (best farm, district packs) | Low-Med | [F] M-3, L-1 | See fixes |
| 7 | **Keeper griefing and starvation** | Low-Med | [F] Advance bounty 0.001 ETH capped by heartbeat. [M] Weak-case minimum headroom 0.006 ETH (`artifacts/v33/simulation.json`) | Team-run backstop bot from block 0 |
| 8 | **MEV on buybacks** | Low | [F] L-4 | Tighter slippage, interval |
| 9 | **MEV on packs** | Low | [I] Pack price is VRGDA with a 1%/pack step (`Params.sol:66`). A bot can front-run large buys to sell nothing (items are soulbound). Back-running only raises the price. | None needed |
| 10 | **TWAP manipulation of token-pack price** | Low | [F] 30-minute TWAP (`V4Market.sol:753-758`). [I] Holding the price for 30 minutes costs more than the token-pack discount is worth | None needed |

---

## 6. Trust: what would make players call it a rug, and how to prove safety on day 1

**Rug triggers, most dangerous first:**
1. **The team holds 100–250M tokens** that are not yet in the pool, while the demo says "no team tokens". [F] `docs/launch-v31.md` admits "the token launch cannot cryptographically eliminate" this custody.
2. **Packs on sale before funding.** This is H-3, and it is the scenario an on-chain sleuth will screenshot.
3. **Hook bind to an unverified router.** H-4.
4. **Endowment counted with buybacks.** M-1.
5. **Swarm parameter changes** that look like nerfs. Emission, tariff and price can each move 10% per day, and pause is available.
6. **Contributor agents dumping** in the first two weeks. This is not the team, but players will not see the difference.

**Day-1 proof, in this order:**
1. Transfer the endowment through `approve` + `fundEndowment()` **before the token pool is initialized**, or at least before PackSale opens. Pin the `Endowed` event on X. The best version is to send the remainder directly to the RewardPool address at launch. [?] Check whether IMD's `remainderTo` can point to a contract address that is predicted in advance.
2. Bind the hook within minutes and publish a one-line verification command:
   `cast call hook "fees()" == cast call registry "module(uint256)" 6`.
3. Publish all 10 `Registered` events, the module code hashes and the Params defaults. Link a verified-source explorer page for each.
4. Run a public status page showing `endowed`, `lockedEndowment`, `available`, `reserved`, `heartbeatBalance`, `credit[team]`, the pause state and every `ParamChanged` letter.
5. Post an "everything the team can and cannot do" thread in 8 lines, with no adjectives.

---

## 7. Competition

[?] This section has the weakest evidence. A web search found **no competing on-chain mining or gacha game on Robinhood Chain** (mainnet launched 2026-07-01 according to [GetBlock](https://docs.getblock.io/api-reference/robinhood) and [eco.com](https://eco.com/support/en/articles/15859739)). That is a gap in my search, not proof that none exist.

**EVM and other comparables:**
- [GoMining Miner Wars](https://decrypt.co/315795/gomining-bitcoin-mining-game-miner-wars) (multi-chain). Backed by real BTC hashrate yield.
- [Hash Wars](https://eonar.substack.com/p/hash-wars-on-chain-nft-game-2e74048c198a). An on-chain hash game.
- [Mining Masters](https://opensea.io/de-DE/collection/miningmasters-miner/overview) (Ronin).
- Ethermax on Base. Its only source was a promotional page ([cointelegraph bonus page](https://cointelegraph.com/crypto-bonus/?p=763)), so treat it as unverified.
- [G] Plus the long history of BNB "miner" ROI dapps, which all collapsed when inflow slowed.

**What BLACKOUT does better** [F/I]:
- No owner and no upgrade path.
- Bounded and logged parameter changes.
- No farm loops, and O(1) idle expiry.
- Soulbound items, so there is no item-dump market.
- Withdrawal tax recycled to players.
- An unusually honest repo, with failures reported rather than buried.
- The event and combo layer gives real decisions, more than a "buy miner, wait" game.

**What it does worse** [I]:
- No real yield backing (GoMining has BTC).
- First reward arrives after 6–12 hours.
- Weak secondary value: soulbound items cannot be resold, so there is no exit except mining.
- Complexity: 12 item types, 4 rooms, combos, district politics, sync rules.
- Payback for later joiners is the same reflexive pattern as the miner dapps that failed.

---

## 8. Launch readiness: go/no-go checklist

**Owners:**
- **T** = team
- **S** = swarm (Params, pause)
- **B** = public or team-run bots
- **P** = IMD platform

| # | Step (in this order) | Owner | Go condition |
|---|---|---|---|
| 0 | Fix H-1…H-4 and M-1/M-2. Re-run pins, `forge test`, and an independent review of the diff | T | All pass; a reviewer other than the author signs off |
| 1 | Decide the open choices: district 10% cap rule, best-farm rule, team-share vesting | T (requester) | Written in the README |
| 2 | Confirm the IMD launcher initializes the pool and adds liquidity atomically, and confirm the contributor claim-lock terms | P → T | Written answer from the platform |
| 3 | Token + hook launch (`launch/V4Market.sol`, 5 arguments, flags `0x10cc`) | P | Hook address and initializedAt published |
| 4 | Application launch A (8 contracts) with `tokenLaunchTimestamp == initializedAt` | T/P | Constructor arguments published and checked by a third party |
| 5 | Application launch B (4 contracts) | T/P | — |
| 6 | Register all 10 roles; `registered()==10` | B (anyone) | Events published |
| 7 | `bindFeeRouter(registry.module(6))`, then `flushFees()` | T, then B | Verification command output posted |
| 8 | `approve` + `fundEndowment()`; `Endowed` event | T | Amount equals the remainder exactly; posted |
| 9 | Fund the IMD heartbeat schedule (70 IMD for 35 days) and top up a team gas float for the bot | T | Receipts posted |
| 10 | Start bots: `advanceEpoch`, entropy capture under 10 s, `executeBuys`, season finalize | B (team backstop) | 24 h dry run on testnet chain 46630 with about 100 ms blocks |
| 11 | First `advanceEpoch()`; check the Params defaults | B/S | Values match `docs/launch-v31.md` |
| 12 | PackSale opens. With H-3 fixed, the contract enforces the funding and binding gates | contract | `isOpen()` true **and** endowed **and** bound |
| 13 | Starter-claim window (hour 48 to day 16) | P/T | Merkle root published |
| 14 | Monitoring: status page, cohort payback dashboard, swarm letters | T/S | Live before step 12 |

**No-go triggers:**
- any H finding is open;
- endowment not funded at step 12;
- the platform cannot confirm atomic initialization;
- no bot is capturing entropy in under 10 s on testnet.

---

## 9. Top 10 changes, ranked by impact vs effort

| # | Change | Effort | Expected effect |
|---|---|---|---|
| 1 | Rearm on expired entropy instead of minting Commons (H-1) | S | Safety: removes the main player-funds loss path. [I] Without it, expected lost packs depend on bot uptime. |
| 2 | Gate `openPack`/`tokenPack` on `endowed && bound` (H-3) | S | Trust: removes the top rug narrative. No payback change. |
| 3 | Verify the router in `bindFeeRouter` against registry and factory (H-4) | S | Trust: binding becomes provably non-custodial |
| 4 | `fundEndowment` only (M-1); pre-fund before the pool opens | S | Trust, and the exact endowment can be proven |
| 5 | Per-block max buy, stepped tax, init-sender check, PackSale clock read from the hook (H-2, M-4) | S-M | Safety: [G] a smaller sniper share means less day-1 drawdown, though this is not simulated |
| 6 | Vest the team's 10% pack share (30-day linear), or route it to the pool until week-2 payback reaches 50% | S | Payback: [G] up to about 11 ETH more in buybacks in steady over 35 days. Mostly helps week-2/3 cohorts and trust. |
| 7 | Reshape emission to back-load rewards: lower the starting emission and extend the drip to 56 days (already allowed, `Params.sol:148`) | S (Params) | Payback: [I] moves yield from week-1 to week-2/3 joiners. Must be simulated before adoption; the repo's own levers show only modest gains. |
| 8 | Fix referral (paid referrer, funded from tariff) and the best-farm / lottery / district rules (M-2, M-3, L-1, L-2) | M | Fairness: removes about 5% hidden emission to informed players and stops sybil prize farming |
| 9 | Onboarding: credit a small "first epoch" reward or a starter Common so players see output within an hour, and have the frontend bundle advance and settle | M | Retention: [G] the largest lever on day-0 quits |
| 10 | Make the demo match the contracts (section 2 table) and add a public status page | S | Trust and clarity. Prevents "you lied" threads. |

**Also required (process):** a sim with inflow that responds to price, plus multiple seeds, before any payback claim is published.

---

## 10. Marketing angle

**One-line pitch:** *"Open packs, build a pixel mining farm, and survive a city where the grid fails every six hours, with no owner keys and every rule on chain."*

**The 3 strongest hooks for X:**
1. **The grid letters.** Daily "IMD Grid Dispatch" posts (outage, fire, theft, audit) with the combo that would have saved you. Shareable lore that brings people back each day.
2. **No admin keys.** "No owner, no upgrade, no withdraw. Here's the one-time bind tx and the endowment tx." Only post this after fixes #2–#4.
3. **District wars.** Eight districts, weekly season and free packs for the winning district. A social, team-based reason to recruit friends (fix the sybil holes first).

**What not to claim:**
- No payback, ROI, APY or "earn" figures. [M] 93% of week-2 joiners had not repaid by day 35 in the team's own *favorable* scenario.
- Not "no team tokens" until the endowment is in the pool on chain.
- Not "fair launch" or "bot-proof". The max buy is per swap (M-4).
- Not "provably fair randomness". It is sequencer-influenced block hashes, not a VRF (`README.md`).
- Not "audited". Only same-author reviews exist (`docs/review-v33.md` says so).
- No demo values (50-token best-farm prize, 20-token lottery, district ranked by mining) presented as launch rules.

---

## 11. Limits, uncertainties and unanswered questions

**What I did:**
- Read `src/` (FarmRewards, FeeRouter, PackSale, Season, GameRegistry, Params, RewardPool, the FarmCore actions), `launch/V4Market.sol`, `README.md`, `report.md`, `docs/launch-v31.md`, `docs/report-v32.md`, `docs/review-v33.md`, `docs/simulation-assumptions.md`, `regulator.md` and `artifacts/v33/simulation.json`.
- Re-ran the v3.3 simulator, standard library only, unmodified source. The two "inflow" rows use a subclass overriding only `demand()`.

**What I did not do:**
- Run `forge test`. Foundry is unavailable here, so the test claims are the repo's, not mine.
- Review `FarmEngine.sol`, `GridOperator.sol`, `FarmItems.sol`, `StarterClaim.sol` or `MarketFactory` / `StandardMarket` / `StandardAdapter` line by line.
- Play the demo interactively. I inspected its shipped JavaScript text and configuration (`chainId: 4663`, season and allocation constants) rather than clicking through it.
- Read X. `x.com/IMDBlackout` returned HTTP 402 to my fetcher, so the social and community state is unknown.
- Read the earlier jobs (9c938888, 14e753f9, 5ce56cbc, 80dc62dc and research b9e37680 / 10d225a6) except through the docs carried forward in this branch. `80dc62dc` has no branch on the remote; the branches are `job-14e753f9`, `job-46fe87c6`, `job-5ce56cbc`, `job-9c938888` and `result`.

**Uncertain:**
- Robinhood Chain block time. 100 ms is cited by most providers and about 250 ms on demand by one; this directly sizes H-1.
- Whether the IMD launcher initializes atomically (H-2).
- The contributor claim-lock terms.
- Whether `remainderTo` can be a contract.

**Unanswered questions for the requester:**
- Should the district 10% cap be the strict rule or the soft one?
- Is the team willing to vest its pack share?
- What is the launch date, relative to the contributor unlock?

**Sources:**
- Repo at the commit above (all `file:line` references).
- Demo bundle `https://playblackout.xyz/assets/index-DT46041E.js`.
- [GetBlock Robinhood docs](https://docs.getblock.io/api-reference/robinhood), [eco.com](https://eco.com/support/en/articles/15859739), [OrbitFlare](https://docs.orbitflare.com/robinhood-chain) and [NodeFlare](https://nodeflare.app/docs/endpoints/robinhood) for chain id and block time.
- Competitor links as given in section 7.
