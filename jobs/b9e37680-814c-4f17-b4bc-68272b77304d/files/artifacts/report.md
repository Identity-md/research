# Swarm Mining Farm: Economy Design, Simulation and Launch Spec

Date: 2026-10-10. Simulation: `sim/swarm_farm_sim.py` (Python 3, stdlib only, deterministic seed). Full output: `artifacts/simulation_output.md`. Reproduce with `python3 sim/swarm_farm_sim.py` (report) or `python3 sim/swarm_farm_sim.py --check` (acceptance test; currently `CHECK PASS`).

Evidence labels used in this report:
- **[F]** Fact from a cited source (source listed in §11).
- **[S]** Simulation output from this repo. It is only as good as the model's assumptions.
- **[A]** Assumption made because the input is unknown. Each one is listed in §10.
- **[I]** Inference or design judgment.

---

## 0. Executive summary

1. **Steady scenario target is met [S].** I define "positive returns" as: a pack bought on any day up to day 28 pays back in ETH within 60 days, counting sold tokens plus held tokens valued at the pool price. In the steady scenario the average payback is 27, 30, 34 and 37 days for players joining in weeks 1, 2, 3 and 4. The slowest pack bought up to day 28 pays back in 46 days. The reward pool never empties in any scenario. Emission is a fixed share of the pool, so it can only shrink geometrically. Even with zero new inflow, the day-35 pool takes another 43–58 days to fall to 10% of its peak.
2. **Hype stalls on day 13 and weak stalls on day 3 [S].** The stall rule is: a new pack no longer pays back within 60 days. Under hype, weeks 1 and 2 pay back (35 and 45 days on average). From week 3 most packs do not. In the weak scenario, almost nobody pays back within 60 days, whatever parameters are used. No parameter fixes a lack of new money; that is the structural limit (§4, §8).
3. **Hard ceiling [I].** All ETH that players can take out comes from the AMM. Real ETH reaches the AMM only from the 75% of pack ETH that buys tokens, plus the share of hook fees used for buybacks. Over the whole game, players as a group can therefore never recover more than about 75% of what they put into packs. Any individual player's profit is a transfer from later players and from swap volume. Every number below should be read with this in mind.
4. **Recommended changes from the starting point:**
   - Pack ETH split: change 50/25/15/10 to **65 reward / 10 burn / 15 team / 10 heartbeat**. In the steady scenario, weeks 1 and 4 payback improves from 32.6 and 45.8 days to 27.2 and 36.6 days. The hype stall moves from day 7 to day 13 [S].
   - **Pricing:** epoch-stepped pack price with a demand premium.
   - **Late joiners:** a +10% hashrate bonus per epoch on newly minted items.
   - **Sinks:** priced in "days of yield" from an on-chain reward-per-hash EMA, so they follow emission automatically.
5. **Chain: I recommend Robinhood Chain, with caveats [I].**
   - Gas cost is not the deciding factor. On 2026-10-10, Ethereum L1 was at 0.07 gwei, which is cheaper per action than Robinhood Chain's reported ~0.1 gwei. Robinhood Chain's median reached 0.511 gwei during the September 2026 congestion [F].
   - Robinhood Chain wins on: the retail audience already there, 100 ms blocks (fast pack reveals), and no exposure to L1 gas spikes. An L1 spike to 5 gwei makes a month of daily claims cost about $34 [S/F] (gas units estimated).
   - Caveat: on Robinhood Chain, `blockhash` is set by the sequencer and `block.number` returns an L1 estimate [F]. Randomness must use the ArbSys precompile, and Robinhood (the sequencer) must be trusted not to grind block hashes.

---

## 1. Parameter table (launch values)

Prices assume ETH = $2,505 (Etherscan, 2026-10-10) [F]. Every number below is what the simulation runs on, unless it is marked "spec only".

### 1.1 Packs and items

| Parameter | Value | Reason / evidence |
|---|---|---|
| Pack price, epoch 1 | **0.010 ETH** (~$25) | Low enough for a casual 3-pack start (~$75). With 3 packs per new player it produces 4.5 ETH on day 1 in steady and 18.75 ETH in hype [S]. |
| Epoch length | **7 days** | Lines up with the weekly payback targets and with heartbeat review windows. |
| Price step per epoch | **−15%** (0.0100 → 0.0085 → 0.0072 → 0.0061 → 0.0060 floor) | Late-joiner fairness: a week-4 player pays 39% less per pack. With flat pricing and no epoch bonus, steady week-4 payback worsens from 36.6 to 43.3 days [S]. |
| Price floor | **0.006 ETH** | Below this, inflow per new player is too small to feed the reward pool. In the grid search, 0.005 lowered hype's stall day to 7 [S]. |
| Demand premium | price × (1 + min(0.5, 0.5·(packs₂₄h/1000 − 1))) | Takes extra ETH during hype, when buyers care least about price, and caps the premium at +50%. In hype, day 2 sold at 0.0144 ETH [S]. |
| Items per pack | **3** | Three reveals per pack give more feedback than one big item. The gas cost is a single reveal transaction. |
| Item type odds | GPU 60%, Cooling 20%, PSU 12%, Room 8% | GPUs are the yield. The rest are progression items that gate slot caps. |
| Rarity odds | Common 70%, Rare 22%, Epic 7%, Legendary 1% | About 1 Legendary per 33 packs (3 items each), so roughly one in every 11 three-pack starters sees one. |
| GPU hashrate | C 10 / R 28 / E 80 / L 250 | Each tier's expected hash contribution (7.0 / 6.2 / 5.6 / 2.5) is similar, so rarity is exciting without dominating. A Legendary is 25× a Common, but Legendaries make up only 12% of expected hash. **Expected raw hash per pack: 38.27** [S]. |
| Cooling | Farm-wide hash boost C 2% / R 5% / E 10% / L 20%; best unit per room counts. Rare or better = **heat-wave immune** | Gives cooling a reason to exist and a counter-play to heat waves. Expected boost per pack +2.04% [S]. |
| PSU | +1 / +2 / +3 / +4 GPU slots in its room (C/R/E/L) | Slot progression (spec only; folded into hash in the sim). |
| Room | Each room has 6 base GPU slots + 1 PSU + 1 cooling. Farm starts with 1 free room. | |
| **Farm caps (anti-whale)** | Max **4 rooms**, so at most 4 × (6 + 4) = **40 GPUs**. Max **20 packs per wallet per 24 h**. Soft cap: hash above **2% of global hash** counts at 50%. | Limits single-wallet share. Sybil wallets can bypass this; see §5. |
| Merge | 3 identical type+rarity items → 1 of the next rarity. Fee = 2 days of the result item's yield (via rpsEMA), burned. | Roughly hash-neutral (3 × 10 = 30 → 28), but frees 2 slots. That is valuable under the 40-GPU cap, and it is a sink. Sim: 2% of gross. |
| Epoch hash bonus | Items minted in epoch *w* get hash × (1 + 0.10·(w−1)), capped at +40% | Late-joiner fairness (§5). |

### 1.2 Emission and money flows

| Parameter | Value | Reason / evidence |
|---|---|---|
| Daily emission | **3.5% of the reward-pool token balance**, streamed per second and repriced each 12 h tick | Tied to pool size, so the pool cannot empty: its balance only shrinks geometrically. It tracks inflow automatically and needs no halvings. In the grid search, 3.5% beat 3% on early payback and beat 4–5% on late-week payback and runway [S]. |
| Halvings / epochs | No halvings; the pool-proportional rate is the decay. Epochs (7 d) drive price steps and the hash bonus only. | Halvings create cliff-edge dumps. Geometric decay is smooth. |
| Split of emission | Pro-rata by effective hash, inside 32 buckets (8 districts × cooling class × size class) whose weights are set by grid events | Events become exact, O(1)-per-tick reweightings (§7). |
| Pack ETH split | **65% buy→reward pool, 10% buy→burn, 15% team, 10% heartbeat treasury** | Moving 10 points from burn to rewards improved every steady cohort and pushed the hype stall from day 7 to day 13 [S]. Burn still comes mainly from in-game sinks: 32% of supply was burned by day 35 in steady [S]. |
| Reward/burn buy execution | Batched keeper buys: ≤0.5 ETH each, ≥10 min apart, minOut from a 30-min hook TWAP −2% | Avoids being sandwiched on large predictable buys (spec only). |
| Hook fee | **1% of the ETH leg of every swap** | [A]: IMD hook fee level not confirmed. |
| Hook fee split | **40% buyback & burn, 30% buy→reward pool, 20% team, 10% heartbeat** | Swap volume, including player sells, refills rewards. Team share stays below the pack team share. |
| Team token allocation | **0** (team earns ETH only) | As briefed. |

### 1.3 Sinks (all burned)

| Sink | Formula | Value | Reason |
|---|---|---|---|
| reward-per-hash EMA (`rpsEMA`) | rpsEMA ← 0.7·rpsEMA + 0.3·(tick emission ×2 / effective hash) | α = 0.3 per day | Prices every sink in "days of yield", so sinks scale with players and emission without manual retuning. |
| Electricity (upkeep) | per hash per day = **tariff × rpsEMA** | tariff **0.15** | Takes 15% of gross. At 0.40, steady stalls on day 7 [S]: upkeep is the sink that drives churn. |
| Durability / repair | Durability −2 points/day (100 max; efficiency = durability %). Repair cost per point = **0.025 × item daily yield** | Maintaining = **5%** of gross | Unattended farms decay. Repair is cheap only for active players. |
| Overclock upgrade | +10% hash per level, 5 levels. Cost to go from level k to k+1 = 0.10 × baseHash × rpsEMA × **15** × **1.4^k** | Upgrade payback 15, 21, 29, 41, 58 days | Early levels pay back inside the game window, later ones do not. Players reinvested 15% of net [A]. |
| Extra slot | +1 GPU slot per room, cost = 10 days of the average GPU yield × 1.5ⁿ, max +2 per room (inside the 40 cap) | spec only | |
| Merge fee | 2 days of the result item's yield | ~2% of gross [A] | |
| **Total sinks** | | **34–43% of emission** across scenarios/days [S] | Net emission stays at roughly 60% of gross. |

### 1.4 Grid events (Swarm "Grid Operator")

| Parameter | Value | Reason |
|---|---|---|
| Frequency | 1 event per 12 h tick (2/day) | As briefed. The letter is published on chain with each tick. |
| Who chooses what | The swarm panel chooses the **event type** and writes the letter. **Which districts** are hit comes from the future block hash of the tick. | The swarm cannot target individual players. |
| Districts | 8; a farm's district = `uint256(keccak(farmOwner)) % 8`, fixed | |
| Odds (swarm guidance, contract-enforced bounds) | Surge 30% (bounds 20–40), Heat wave 25% (10–30), Blackout 20% (≤25), Tax audit 15% (≤20), Calm 10% | Positive events are the most common. |
| Bonus surge | 1 district gets weight ×1.5 for the tick, and tick emission +5% | |
| Heat wave | 2 districts: farms without Rare+ cooling get weight ×0.8 | Counter-play: buy or merge cooling. |
| Blackout | 1 district offline for 6 of 12 h (weight ×0.5). **The same district cannot be blacked out within 3 days (6 ticks).** | Most dramatic, so rate-limited. |
| Tax audit | Farms in the "large" class (effective hash ≥ 2,000 ≈ 50 packs) lose 5% of the tick's accrual (burned) | Hits whales, not newcomers. |
| Max single-tick loss | 50% of one tick, i.e. 25% of one day | Never zeroes a farm. |
| **Measured fairness [S]** | Over 28 days for 4,000 farms, income relative to no events is: p1 0.988, p5 0.994, median 1.015, p95 1.032 (with blackout cooldown). Without the cooldown, p1 is 0.984. | Dramatic per tick, but within ±3.5% over a month. |

### 1.5 Payback targets (average active player, ETH, sold + held-at-mark)

| Join week | Target | Steady sim | Hype sim | Weak sim |
|---|---|---|---|---|
| 1 | ≤ 28 d | **27.2** | 34.6 (10% never ≤120 d) | 103 (64% never) |
| 2 | ≤ 32 d | **30.3** | 44.8 (10% never) | 99 (53% never) |
| 3 | ≤ 35 d | **33.5** | 58.0 (38% never) | 86 (53% never) |
| 4 | ≤ 40 d | **36.6** | 73.8 (70% never) | 88 (39% never) |

---

## 2. Simulation model (what it does and does not model)

`sim/swarm_farm_sim.py`, 35 daily steps, each step containing two 12 h event ticks.

- **AMM [A]:** constant-product pool with 1 B tokens against a *virtual* 10 ETH. This stands in for an IMD launch curve whose parameters I did not have. The hook takes 1% of the ETH leg on sells.
- **Players [A]:** new players per day:
  - hype = 600·e^(−(d−1)/5) + 25
  - steady = 150/day for days 1–3, then 80/day
  - weak = 40·e^(−(d−1)/15) + 5

  Each new player buys 3 packs, scaled by (0.01/price)^0.7. 3% of active players buy one extra pack per day. Demand is also scaled by √(21 / perceived payback), capped at 1.
- **Each day:** pack ETH is routed (buys into the reward pool and into burn), emission is 3.5% of the pool, and events are drawn. Gross rewards minus sinks gives net. 15% of net goes to upgrades (burned, adds overclock levels), 65% of the rest is sold and 35% held. Hook fees are routed.
- **Churn:** 1.5%/day, plus up to 6% more when daily ROI on pack cost is below 2%.
- **Cohorts:** players are grouped by the day they bought packs. Payback is computed per *active* pack: sold ETH plus held tokens valued at the pool price. If a pack has not paid back by day 35, the payback is projected using the last-7-day decay of yield, out to 120 days.
- **Stall day:** the first day ≥ 3 on which a pack bought that day does not pay back within 60 days, or on which active farms fall below 25% of the running peak.
- **Not modelled:**
  - item-level variance (luck); the sim uses expected hash
  - the anti-whale soft cap
  - sybils and arbitrage bots
  - ETH/USD moves
  - gas cost (immaterial at the gas prices in §6)
  - pool-price manipulation

---

## 3. Simulation results per scenario [S]

Columns: price is ETH per 1 M tokens. Net yield is ETH per day for one base pack held by an active player, after sinks and reinvestment. Runway is the number of days for the pool to decay to 10% of its peak if all inflow stopped that day.

### 3.1 Hype

| day | new | active farms | packs | pack price | ETH in | emission | burned (cum) | supply | reward pool | price /1M | runway d | net yield/pack/day | sinks % |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 625 | 616 | 1875 | 0.0100 | 18.75 | 19.5M | 41.7M | 958.3M | 529.8M | 0.0556 | 65 | 0.000388 | 34% |
| 3 | 427 | 1331 | 1309 | 0.0100 | 13.09 | 23.4M | 79.0M | 921.0M | 652.2M | 0.1544 | 65 | 0.000557 | 41% |
| 7 | 206 | 2309 | 681 | 0.0100 | 6.81 | 23.5M | 133.9M | 866.1M | 653.3M | 0.3128 | 64 | 0.000610 | 43% |
| 14 | 70 | 2814 | 317 | 0.0085 | 2.70 | 19.8M | 202.7M | 797.3M | 552.1M | 0.3125 | 59 | 0.000393 | 39% |
| 21 | 36 | 2836 | 221 | 0.0072 | 1.60 | 16.8M | 253.6M | 746.4M | 454.6M | 0.2570 | 54 | 0.000247 | 36% |
| 28 | 28 | 2703 | 199 | 0.0061 | 1.22 | 13.8M | 294.9M | 705.1M | 375.0M | 0.2218 | 48 | 0.000161 | 35% |
| 35 | 23 | 2412 | 161 | 0.0060 | 0.97 | 11.2M | 328.8M | 671.2M | 312.3M | 0.2033 | 43 | 0.000117 | 35% |

- Payback by join week: 34.6, 44.8, 58.0 and 73.8 days. Week 5 has no payback within 120 days.
- Total pack ETH 135.5. Team 20.5 ETH, heartbeat 13.6 ETH.
- **Stall day 13.** Price peaks around day 10, then falls about 1–2% per day as sells exceed buys.

### 3.2 Steady

| day | new | active farms | packs | pack price | ETH in | emission | burned (cum) | supply | reward pool | price /1M | runway d | net yield/pack/day | sinks % |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 150 | 148 | 450 | 0.0100 | 4.50 | 8.1M | 28.8M | 971.2M | 218.3M | 0.0177 | 65 | 0.000209 | 34% |
| 3 | 108 | 343 | 331 | 0.0100 | 3.31 | 13.2M | 60.7M | 939.3M | 366.8M | 0.0313 | 65 | 0.000241 | 38% |
| 7 | 73 | 588 | 233 | 0.0100 | 2.33 | 15.9M | 104.0M | 896.0M | 442.8M | 0.0534 | 65 | 0.000274 | 40% |
| 14 | 80 | 1057 | 299 | 0.0085 | 2.54 | 16.9M | 172.6M | 827.4M | 471.2M | 0.1039 | 65 | 0.000272 | 40% |
| 21 | 80 | 1478 | 344 | 0.0072 | 2.48 | 16.3M | 230.1M | 769.9M | 441.2M | 0.1509 | 63 | 0.000241 | 37% |
| 28 | 80 | 1857 | 392 | 0.0061 | 2.41 | 14.6M | 279.5M | 720.5M | 397.2M | 0.1910 | 60 | 0.000189 | 37% |
| 35 | 80 | 2185 | 407 | 0.0060 | 2.44 | 12.7M | 322.2M | 677.8M | 354.6M | 0.2310 | 57 | 0.000149 | 36% |

- Payback by join week: **27.2, 30.3, 33.5 and 36.6 days**; week 5 (days 29–35) 58.2. No pack bought up to day 28 is projected to take more than 46 days.
- Total pack ETH 87.5. Team 13.2 ETH, heartbeat 8.8 ETH.
- **Stall day 33**, which is after the required day 28.
- Net yield per pack is positive every day.

### 3.3 Weak

| day | new | active farms | packs | pack price | ETH in | emission | burned (cum) | supply | reward pool | price /1M | runway d | net yield/pack/day | sinks % |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 45 | 44 | 135 | 0.0100 | 1.35 | 2.9M | 12.2M | 987.8M | 77.8M | 0.0121 | 65 | 0.000169 | 34% |
| 7 | 23 | 177 | 71 | 0.0100 | 0.71 | 8.2M | 54.3M | 945.7M | 228.8M | 0.0200 | 65 | 0.000182 | 37% |
| 14 | 18 | 292 | 66 | 0.0085 | 0.56 | 10.2M | 98.0M | 902.0M | 283.1M | 0.0283 | 65 | 0.000165 | 37% |
| 21 | 13 | 357 | 58 | 0.0072 | 0.42 | 10.4M | 135.3M | 864.7M | 281.3M | 0.0340 | 64 | 0.000146 | 36% |
| 28 | 10 | 380 | 51 | 0.0061 | 0.31 | 9.5M | 167.3M | 832.7M | 258.7M | 0.0373 | 62 | 0.000120 | 35% |
| 35 | 7 | 373 | 40 | 0.0060 | 0.24 | 8.3M | 194.2M | 805.8M | 230.1M | 0.0391 | 58 | 0.000098 | 35% |

- Payback by join week: 103, 99, 86 and 88 days, with 39–64% of packs never paying back within 120 days.
- **Stall day 3.**
- The reward pool never empties: the minimum after day 1 is 114.5 M tokens. Even so, the game never becomes profitable for most players. The weak case does not lose money quickly; it just never pays.

### 3.4 Sensitivity (all other parameters at launch values) [S]

| Variant | Steady wk1 / wk4 payback (d) | Steady stall | Hype stall | Weak stall |
|---|---|---|---|---|
| **Baseline** | **27.2 / 36.6** | **33** | **13** | 3 |
| AMM virtual ETH 3 (thinner launch) | 15.9 / 27.0 | 34 | 11 | 14 |
| AMM virtual ETH 30 (deeper launch) | 74.5 / 64.5 | 3 | 3 | 3 |
| Players sell 90% instead of 65% | 54.0 / 61.6 (14% never) | 6 | 4 | 3 |
| Emission 2.5%/day | 32.9 / 36.0 | none | 14 | 3 |
| Emission 5%/day | 23.2 / 42.1 | 31 | 12 | 3 |
| Original split 50/25/15/10 | 32.6 / 45.8 | 31 | 7 | 3 |
| Flat price, no epoch bonus | 22.2 / 43.3 | 33 | 12 | 9 |
| Tariff 40% | 43.8 / 50.9 | 7 | 4 | 3 |
| Churn ×2 | 24.9 / 26.3 | none | 32 | 3 |

Readings [I]:
1. **The launch liquidity depth is the single most sensitive input.** It is an IMD launch parameter that I do not know. Deep liquidity (30 ETH virtual) means pack buys barely move the price, and returns collapse.
2. **Player sell pressure is the second.** The game only works if players hold about a third of what they earn.
3. Higher churn *helps* the players who stay, because abandoned hash stops diluting them. That is a real but uncomfortable property of this design.

---

## 4. Failure modes and levers

The heartbeat (swarm) may only change the parameters listed here, only within the listed bounds, and by at most one step per 7-day epoch. Every change is announced in the tick letter. **The heartbeat can never change** the team share, the hook fee level, item hash tables, rarity odds, or mint rights.

| # | Failure mode | Early signal (on-chain) | Lever (bounds, max step/epoch) |
|---|---|---|---|
| 1 | **Inflow collapse** (weak case) | packs₂₄h < 25% of the 7-day average; net yield/pack < 1% of pack price per day | `epochPriceStep` 0–20% (±5 pp). `packPriceFloor` 0.004–0.010 ETH. `tariffRatio` down to 0.10. **Honest limit:** the sim shows no parameter set rescues the weak case (§3.4). The real fix is more players, not tuning. |
| 2 | **Sell-pressure spiral** (price −5%/day for 3 days) | hook TWAP slope | Hook split `burnShare` 30–60% (the reward share absorbs the difference, ±10 pp). `tariffRatio` 0.10–0.30 (±0.05). |
| 3 | **Hype overbuy, then crash** (hype stalls day 13) | packs₂₄h > 3× target | `surgePremiumCap` 0–100% (±25 pp). `surgeTargetPacks` 500–3000. |
| 4 | **Emission too fast or too slow** | runway < 30 d, or wk-N payback > target + 10 d | `emissionRate` 2.5–5.0%/day (±0.5 pp). |
| 5 | **Upkeep churn** (tariff 40% → stall day 7) | daily churn > 5% | `tariffRatio` 0.10–0.30. `repairPerPoint` 0.015–0.04 of daily yield. |
| 6 | **Event unfairness** | any district's 7-day income < 0.9 of the mean | Event odds within the bounds in §1.4. `blackoutCooldownTicks` ≥ 6 (can only be raised). `heatwavePenalty` 10–30%. |
| 7 | **Whale / sybil dominance** | top 10 wallets > 25% of hash | `softCapShare` 1–5%. `auditThreshold` 1,000–10,000 hash. Sybils remain possible [I]. |
| 8 | **MEV on reward-pool buys** | buy slippage > 2% | Keeper batch size 0.1–1 ETH. TWAP tolerance 1–3%. |
| 9 | **Late-joiner starvation** | wk-N payback > 45 d | `epochHashBonus` 0–15% per epoch (±5 pp; applies only to new mints). |
| 10 | **Reward pool emptying** | impossible by construction: the pool shrinks at most 5%/day | none needed |
| 11 | **Randomness abuse** | reveal rate < commit rate | Expired commits resolve as all-Common, so letting a bad roll expire never pays (§7). |

---

## 5. Late-joiner fairness and anti-whale

The four mechanisms below stack. Together they move steady week-4 payback from 43.3 days (flat price, no bonus) to 36.6 days [S].

1. **Cheaper packs per epoch.** The price drops 15% per epoch, so a week-4 pack costs 0.0061 ETH against 0.010 ETH in week 1.
2. **Epoch hash bonus.** Week-4 items get +30% hash. Combined with the cheaper price, a week-4 player gets about 2.1× the hash per ETH of a week-1 player.
3. **Durability decay.** Unattended early farms decay 2%/day and are not counted against newcomers.
4. **Pool-proportional emission.** Rewards follow inflow, not a schedule that front-loads everything into week 1.

**Anti-whale:**
- 20 packs per wallet per day
- 40 GPU slots per farm
- the soft cap at 2% of global hash
- tax audits on the large class

**What this cannot fix [I]:** early players still earn more per ETH, because they collect the high-yield days 1–14 that later players miss (§8).

---

## 6. Chain choice: Ethereum L1 vs Robinhood Chain

**Evidence [F]:**
- **Ethereum L1:** Etherscan gas tracker on 2026-10-10 17:37 UTC showed 0.07 gwei and ETH at $2,505.12. Secondary sources put typical early-2026 L1 base fees at 0.1–0.5 gwei after the Fusaka upgrade.
- **Robinhood Chain:**
  - Arbitrum Orbit chain, chain ID 4663, gas paid in ETH, ~100 ms blocks.
  - Minimum gas price 0.02 gwei.
  - Median gas reached 0.511 gwei on 2026-09-03 during a memecoin surge (Bitquery). L1 data price is set to zero, so a transfer costs exactly 21,000 gas.
  - Robinhood's gas subsidy ended 2026-09-29.
  - About 0.098 gwei reported in October 2026. This comes from a search-engine summary that I could not open directly, so treat it as unverified.
- Uniswap v4 PoolManager is deployed on both chains (L1 `0x000000000004444c5dc75cB358380D2e3dE08A90`, Robinhood `0x8366a39cc670b4001a1121b8f6a443a643e40951`).

**Cost per action** [S, using gas units *estimated* for the spec'd contracts; these are not measured, so ±40%]:

| Action | gas (est.) | L1 @0.07 gwei | L1 @0.5 | L1 @5 (stress) | RH @0.02 (floor) | RH @0.1 (Oct) | RH @0.5 (Sep peak) |
|---|---:|---:|---:|---:|---:|---:|---:|
| openPack (commit) | 95,000 | $0.017 | $0.119 | $1.19 | $0.005 | $0.023 | $0.122 |
| revealPack (mint 3) | 165,000 | $0.029 | $0.207 | $2.07 | $0.008 | $0.041 | $0.211 |
| claim (settles upkeep+repair) | 90,000 | $0.016 | $0.113 | $1.13 | $0.005 | $0.022 | $0.115 |
| upgrade | 65,000 | $0.011 | $0.081 | $0.81 | $0.003 | $0.016 | $0.083 |
| pay upkeep only | 50,000 | $0.009 | $0.063 | $0.63 | $0.003 | $0.012 | $0.064 |
| merge 3→1 | 110,000 | $0.019 | $0.138 | $1.38 | $0.006 | $0.027 | $0.141 |
| 30 daily claims | 2.7 M | $0.47 | $3.38 | $33.82 | $0.14 | $0.66 | $3.46 |

**Recommendation: Robinhood Chain [I].**
- **Gas:** at today's prices both chains are cheap. One pack open (commit + reveal, 260k gas) costs about $0.046 on L1 at 0.07 gwei and $0.064 on Robinhood Chain at 0.1 gwei, against a $25 pack. Gas does not decide the choice. The risk is an L1 spike: at 5 gwei one claim ($1.13 ≈ 0.00045 ETH) costs about 2.4 days of one pack's net yield on day 28 of the steady scenario (0.000189 ETH/day). Robinhood Chain's worst observed level was 0.5 gwei.
- **Audience and speed:** Robinhood Chain has the retail and memecoin audience (daily fee records in September 2026). Its 100 ms blocks let a pack reveal follow the commit within about a second.
- **Implementation consequences** (Arbitrum docs):
  - `block.number` returns an L1 estimate. Use `ArbSys(0x64).arbBlockNumber()` and `arbBlockHash()` for commit/reveal.
  - `blockhash` is "cryptographically insecure". The sequencer (Robinhood) could in principle grind, but players cannot. State this in the game's disclosures.
  - On L1, use `blockhash(commitBlock + 2)`. A validator would have to give up a block reward (≫ the value of a $25 pack) to bias it.
- **Choose Ethereum L1 instead** if the requester values trust-minimised randomness over audience. The economics are unchanged.

---

## 7. Implementation-ready contract spec (fits one IMD launch prompt)

**Constants:**
- 1e18 fixed point
- `DAY` = 86,400 s, `TICK` = 43,200 s, `EPOCH` = 7 days from `launchTime`
- `blockNum()` = `block.number` on L1, `ArbSys.arbBlockNumber()` on Robinhood; `bhash(n)` likewise
- All tunables live in `Params` with the min/max bounds from §4. Only `heartbeat` (the IMD oracle) may set them, and changes are clamped to bounds and one step per epoch.
- `owner` sets `teamWallet` and `heartbeatTreasury` once at deploy (owner-settable; no hard-coded addresses).

**Contracts**

1. **`FarmItems` (ERC-1155)**
   - `id = type*4 + rarity` (type: 0 GPU, 1 Cooling, 2 PSU, 3 Room; rarity 0–3).
   - Per-token metadata: `mintEpoch` is encoded as a separate id range, `id + 16*epoch` (epochs 1–5; later epochs reuse 5). The hash bonus is therefore readable from the id alone.
   - `mint`/`burn` are restricted to `PackSale` and `FarmCore`.
   - Items placed in a farm are held by `FarmCore` (escrow) and are not transferable while placed.

2. **`PackSale`**
   - State: `commits[id] = {player, n, revealBlock, price, resolved}`, `packs24h` (rolling count, 1-hour buckets), `ethForReward`, `ethForBurn`.
   - `price() = max(floor, base·(1−step)^(epoch−1)) · (1 + min(cap, max(0, 0.5·(packs24h/target − 1))))`
   - `openPack(n≤20−walletPacks24h) payable`: requires `msg.value == n·price()`. Splits 65/10/15/10 into internal balances, team and heartbeat (pull payments). Stores `revealBlock = blockNum()+2`. Emits `PackCommitted(id, player, n, price, revealBlock)`.
   - `reveal(id)` (callable by anyone):
     - If `blockNum() ≤ revealBlock`: revert.
     - Seed: `h = bhash(revealBlock)`. If `h == 0` (more than 256 blocks old), the commit resolves as all-Common.
     - Each item: `r = keccak(h, id, i)`, then `type = pick(r>>0)`, `rarity = pick(r>>64)`, minted to the player with the current epoch.
     - Emits `PackRevealed(id, ids[])`.
   - `executeBuys(maxEth, minOut)` (keeper/heartbeat): ≤0.5 ETH per call, ≥10 min apart, swaps via v4 PoolManager. Tokens go to `RewardPool` or are burned (`burn()` if the IMD token supports it, otherwise sent to a no-withdraw `BurnVault`). Emits `Bought(kind, eth, tokens)`.

3. **`FarmCore`** (emission, farms, sinks)
   - State:
     - `buckets[32]` = {hash, acc} with bucket = district(0–7)·4 + strongCooling·2 + large
     - `farms[a]` = {bucket, rawHash, effHash, durability, lastSettle, rewardDebt, pending, overclock[], rooms, debt}
     - `rpsEMA`, `emissionRate`, `tariff`, `repairPerPoint`, `weights[32]` (current tick, 1e4 = 1.0)
   - Hash:
     - `effHash = min(raw, cap) + 0.5·max(0, raw − cap)`, with `cap = softCapShare · totalHash`
     - `raw = Σ gpuHash[r]·(1+0.1·(epoch−1)) · (1+0.1·oc) · (1+bestCooling[room])`
   - Tick accrual (in `tick()` and lazily per block):
     - `E = emissionRate · RewardPool.balance · dt / DAY`
     - For every bucket b: `acc_b += E · w_b / Σ_j(w_j · H_j)`
     - `rpsEMA` is updated once per day from `E_day / ΣH`.
   - `settle(a)`:
     - `gross = effHash·(acc_b − rewardDebt)`
     - `avgDur = durability − 1·elapsedDays` (linear decay, floored at 0). Credit is `gross·avgDur/100`; the rest returns to the pool.
     - `upkeep = tariff · rpsEMA · effHash · elapsedDays`, burned.
     - If `gross < upkeep`, the farm goes offline (hash removed from its bucket) and `debt += shortfall`.
     - Durability drops 2/day.
   - Functions:
     - `place(ids, room)` / `unplace(...)`: settle first, then rebucket.
     - `claim()`: settle, then transfer `pending` to the player. Emits `Claimed(a, gross, upkeep, net)`.
     - `repair(points)`: cost `points · repairPerPoint · rawHash · rpsEMA`, burned.
     - `overclock(gpuSlot)`: cost `0.1 · baseHash · rpsEMA · 15 · 1.4^k`, burned, max 5 levels.
     - `buySlot(room)`: cost `10 · avgGpuYield · 1.5^n`, max +2 per room.
     - `merge(id, 3)`: burns 3 items, mints 1 of the next rarity, fee `2 · yield(result)` burned.
     - `poke(a)`: permissionless settle for stale farms.
   - Events: `Placed`, `Unplaced`, `Settled`, `Claimed`, `Repaired`, `Overclocked`, `Merged`, `FarmOffline`, `Burned(source, amount)`.

4. **`GridOperator`**
   - `publishTick(tickId, eventType, letterHash, letterURI)`: only `heartbeat`, at most once per `TICK`.
   - The contract computes the affected districts from `bhash(blockNum()−1)` and applies the cooldown and bounds. It sets `weights[32]`:
     - surge: ×1.5 on district d, and E×1.05
     - heat wave: ×0.8 on weak-cooling buckets of 2 districts
     - blackout: ×0.5, district not hit in the last 6 ticks
     - audit: `large` buckets ×0.95, the difference burned
   - If the heartbeat misses a tick for more than 1 h, anyone may call `calmTick()`, which sets weights to 1.0.
   - Emits `GridEvent(tickId, type, districts, letterHash, letterURI)`.

5. **`RewardPool`**: holds tokens and only releases them to `FarmCore` through the accrual formula. It has no owner withdrawal.

6. **IMD v4 hook** (existing IMD component, configured):
   - 1% fee on the ETH leg, split 40% burn-buy / 30% reward-buy / 20% team / 10% heartbeat (accrued to `PackSale` balances).
   - Records a 30-min TWAP used for `minOut`.

7. **`Params`**: getters and setters with bounds, step limits, and `ParamChanged(name, old, new, tickId)`.

**Invariants to test:**
- Pool emission ≤ 5%/day.
- Σ claims ≤ RewardPool inflow.
- No player-controlled input affects the item seed.
- A heartbeat cannot exceed the bounds.
- Team ETH comes only from the pack and hook splits.

---

## 8. Risk note for players (publish as-is)

Swarm Mining Farm is a game, not an investment.
- All token rewards are bought with ETH from other players' pack purchases and from swap fees. As a group, players can never take out more ETH than they put in: about a quarter of pack ETH goes to the team and the swarm treasury.
- Early players earn more than later ones. In our own simulation, with steady growth, a week-1 pack paid back in about 27 days and a week-4 pack in about 37 days. With fast hype that fades, packs bought from week 3 onward mostly did not pay back. With weak demand, almost nobody broke even.
- Rewards fall as soon as new players and swap volume slow down.
- The token price can drop sharply when players sell.
- The swarm's grid events, and the sequencer of the chain the game runs on, can affect your income.
- Only spend what you would spend on a game you expect to lose money on.

---

## 9. Facts, inferences, uncertainty, open questions

**Facts [F]** (see §11):
- L1 gas was 0.07 gwei and ETH $2,505 on 2026-10-10.
- Robinhood Chain: Arbitrum Orbit, chain ID 4663, 0.02 gwei floor, 0.511 gwei median on 2026-09-03, L1 data priced at zero, subsidy ended 2026-09-29.
- On Arbitrum chains, `blockhash` is insecure and `block.number` is an L1 estimate; the ArbSys precompile is at `0x64`.
- Uniswap v4 is deployed on both chains.

**Simulation results [S]:** all tables in §1.5 and §3, the event fairness figures and the sensitivity runs. They are deterministic and reproducible.

**Inferences [I]:**
- the ~75% collective ETH ceiling
- the chain recommendation
- that liquidity depth and sell share dominate
- that sybils can bypass per-wallet caps

**Uncertainty:**
- Player behaviour parameters (packs per player, sell share, churn, demand elasticity) are guesses, not measured from comparable games.
- Gas units are estimates, not measured from compiled contracts.
- Robinhood Chain's October gas level (0.098 gwei) is unverified.
- The simulation uses expected values, so individual luck (for example a Legendary pull) is not shown.

**Open questions for the requester:**
1. IMD launch curve and initial liquidity. This is the most sensitive input (§3.4); the sim assumes a 10 ETH virtual reserve.
2. The IMD hook's fee level and whether its split is configurable.
3. Whether the IMD token supports `burn()`.
4. Team and heartbeat treasury addresses (owner-settable at deploy).
5. Final chain choice: trust in the sequencer versus audience.

## 10. Assumptions [A]

- 1 B token supply, all in a constant-product pool with 10 ETH virtual reserve.
- Hook fee 1%.
- 3 packs per new player.
- 3% of active players buy one pack per day.
- Players reinvest 15% of net, sell 65% of the remainder and hold the rest.
- Churn 1.5–7.5%/day.
- Merge fees 2% of gross.
- The top 10% of farms hold 35% of hash (used for audits).
- 55% of farms have Rare+ cooling (used in the event Monte Carlo).
- ETH/USD fixed at $2,505.

## 11. Sources

- Etherscan Gas Tracker (fetched 2026-10-10 17:37 UTC): https://etherscan.io/gastracker
- Bitquery, "Robinhood Chain Gas Fees: 25x in 11 Days, $4.5M a Day" (2026-09-04): https://bitquery.io/investigations/robinhood-chain-gas-price-25x
- Gokhshtein, "Robinhood Chain Goes Live on Arbitrum: Free Gas Through Sept. 29" (2026-09-07): https://gokhshtein.com/news/2026-09-07-robinhood-chain-goes-live-on-arbitrum-free-gas-through-sept
- crypto.news, Robinhood Chain fees and subsidy (2026-09-04): https://crypto.news/robinhood-chain-flipped-solana-revenue-gas-subsidy-expires/
- Arbitrum docs, Solidity support (blockhash, block.number): https://docs.arbitrum.io/build-decentralized-apps/arbitrum-vs-ethereum/solidity-support
- Arbitrum docs, precompiles reference (ArbSys `0x64`, `arbBlockNumber`, `arbBlockHash`): https://docs.arbitrum.io/build-decentralized-apps/precompiles/reference
- Uniswap v4 deployments: https://developers.uniswap.org/docs/protocols/v4/deployments
- Bitquery, Uniswap v4 hooks on Robinhood Chain: https://bitquery.io/investigations/uniswap-v4-hooks-robinhood-chain
- Secondary, not independently verified: DEXTools 2026 gas guide (post-Fusaka 0.1–0.5 gwei typical): https://www.dextools.io/tutorials/what-is-gas-price-gwei-ethereum-fees-guide-2026-de ; Robinhood Chain October gas ~0.098 gwei from a search summary that cited gwei.wtf / robinscan.io, neither of which could be fetched.
