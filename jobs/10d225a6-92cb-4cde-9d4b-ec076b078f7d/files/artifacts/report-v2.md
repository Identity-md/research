# BLACKOUT (Swarm Mining Farm) — v2 economy spec and simulation, Robinhood Chain

Date: 2026-10-10. This is the second research pass. It continues IMD job `b9e37680-814c-4f17-b4bc-68272b77304d`, whose accepted report I downloaded from `https://api.imd.fun/artifacts/dfbd6842…` (sha256 `dfbd6842bdf572b684b09c4e56d150483da21ccc8dfb14d05fb01409c4441c0b` matches the job record). I keep its parameter table, contract spec and model, and only add to or change them where stated.

- **New simulation:** `sim/blackout_sim_v2.py` (Python 3, stdlib only, deterministic seed).
  - `python3 sim/blackout_sim_v2.py` prints every table. The full output is in `artifacts/simulation_output_v2.md`.
  - `python3 sim/blackout_sim_v2.py --check` → `CHECK PASS`. The check confirms that:
    - with every new mechanic switched off, v2 reproduces v1 day by day (farms, pool, price, burns, yield, stall day, team ETH);
    - the steady scenario does not stall before day 28;
    - every steady pack bought up to day 28 pays back within 60 days;
    - the reward pool never empties;
    - team ETH stays within 12–20% of player ETH inflow;
    - the sell fee never exceeds its cap.
- **v1 model:** `sim/swarm_farm_sim.py` is unchanged and still passes its own check.

Evidence labels, as in v1:
- **[F]** fact from a cited source (§12)
- **[S]** simulation output, only as good as its assumptions
- **[A]** assumption (listed in §11)
- **[I]** inference or design judgment

---

## 0. Executive summary

1. **New fact that changes the launch picture [F]:** IMD's own launch policy is now public, and v1 did not have it.
   - **Token:** 1,000,000,000 tokens with plain transfers. 10% always goes to the swarm; the requester's 90% is split between the pool (`poolBps`, at least 1,000, at most 9,000) and `remainderTo`.
   - **Fee:** 1.25% on every trade: "1% to the paying wallet and 0.25% to the network".
   - **Opening:** the pool opens single-sided at a cap. For Robinhood Chain (4663) paired with ETH, the live `customCap` range is **1 to 1,000 ETH**.
   - **Effect on BLACKOUT [S]:**
     - The 0.25% network fee and the 90% pool barely matter.
     - The **swarm's 10% allocation** sits outside the game. If seat holders sell half of it in the first 14 days [A], the **hype case stalls on day 4 instead of day 31**. The steady case still holds (stall day 34).
     - This is the largest single effect found in this pass. It is outside the game's control.
2. **Steady target holds with everything added [S]:**
   - Steady stalls on **day 34** (v1: 33).
   - Payback by join week: **27.9 / 30.6 / 33.8 / 36.5 days** (v1: 27.2 / 30.3 / 33.5 / 36.6).
   - Every pack bought up to day 28 pays back within 60 days. The reward pool never empties.
   - Weak still stalls on day 3. No mechanic fixes missing demand.
3. **Team revenue [S]:**
   - The team receives **15.0% of all player ETH inflow** (packs, lobbying, hook fees, sell tax), **ETH only**.
   - Totals over 35 days: steady **13.8 ETH**, hype **21.5 ETH**, weak **2.7 ETH**. The weekly split is in §3.
   - Every team share is ≤ 20% per stream, so the aggregate can never exceed 20% (enforced by the contract, §9).
   - At the 20% maximum, steady still stalls on day 32, after day 28.
4. **What the new mechanics do [S], ranked by effect:**
   - **Swarm tariff controller** (largest positive): hype stall 13 → 32 on its own.
   - **Withdrawal tax plus in-game spending** (mixed):
     - Lowers the effective sold share from 65% to 52% and lifts the steady day-35 price by 23%.
     - But it **hurts late joiners**, because incumbents reinvest into more hash (steady week-4 payback 36.6 → 41.3 days on its own).
     - The mitigations in §1.2 (only 25% of in-game spending can buy packs, capped at 1 token-pack per wallet per day) keep it acceptable.
   - **Free NFT packs** are the costliest promotion:
     - Opened on day 1 at full hash, they cut the hype stall from 13 to 4.
     - Opened at hour 48 with 50% "Starter" hash, the hype stall is 7.
   - **Progressive sell tax:** almost no effect at daily resolution. It only bites intraday: a 5 ETH dump pays 10.9–12.6%. It is a dump brake, not an economy lever.
   - **Referrals:** cost about 2% extra emission and have a small effect.
   - **Lobbying:** a modest burn source.
   - **Beta caps:** only reshape the first 15 hours of hype.
5. **Launch recommendation for IMD on Robinhood Chain [I/S]:**
   - Pair with **ETH**, **`poolBps` = 9000** (all of the requester's 90% in the pool, so **no team tokens**).
   - **Opening cap ≈ 5.6 ETH**. That equals a 5 ETH virtual reserve on the 900 M pooled tokens, about $14k at $2,505/ETH.
   - With the defaults and 65% sell intent:
     - **5 ETH:** steady never stalls in 35 days; hype stalls on day 7.
     - **3 ETH:** steady stalls on day 35 and is the most robust at 90% sell intent (27 vs 14).
     - **10 and 20 ETH:** both are worse.
   - No setting survives 90% sell intent everywhere.

---

## 1. Updated parameter table

v1 values (§1.1–1.5 of the previous report) all still apply unless changed here. Changed values are marked **(changed)**.

### 1.1 Kept from v1 (summary)

| Parameter | Value |
|---|---|
| Pack price | 0.010 ETH, −15%/epoch (7 d), 0.006 floor, surge premium ≤ +50% |
| Pack ETH split | 65 buy→reward pool / 10 buy→burn / 15 team / 10 heartbeat |
| Items per pack and odds | 3 items. GPU 60 / Cooling 20 / PSU 12 / Room 8. Rarity C 70 / R 22 / E 7 / L 1 |
| GPU hash | C 10 / R 28 / E 80 / L 250. Expected 38.27 hash per pack |
| Emission | 3.5% of the reward pool per day, streamed |
| Sinks | Tariff × rpsEMA (starts at 0.15), repair 5%, merge 2%, overclock 15 days of yield × 1.4^k (5 levels), slots |
| Grid events | 2 per day. Odds and effects as in v1. Blackout cooldown 6 ticks. The swarm picks the type; the future block hash picks districts |
| Anti-whale | 20 packs/wallet/24 h after beta, 40 GPUs, soft cap 2% of hash, audits |

### 1.2 New mechanics

| # | Parameter | Value | Reason / evidence |
|---|---|---|---|
| 1 | **Base swap fee** (changed) | **1.25% of the ETH leg**, IMD policy: 1.00% to the paying wallet (= BLACKOUT `FeeRouter`, split 40 burn / 30 reward / 20 team / 10 heartbeat) and 0.25% to the IMD network | [F] imd.fun/docs. Buys pay only this. |
| 1 | Progressive sell fee | `fee = min(15% − 0.25%, 1% + 5%·s1h + 4%·s24h + 0.5·min(dev, 10%))`, plus the 0.25% network fee, so **total ≤ 15.00%** | Max of the formula = 1 + 5 + 4 + 5 = 15%. The hard cap is an immutable constant, so the token is never a honeypot. |
| 1 | `s1h`, `s24h` | `max(0, (S − B)/(S + B + V0))` over the last 1 h (12 × 5-min buckets) and 24 h (24 × 1 h buckets). S/B = ETH value of sells/buys. **V0 = 0.5 ETH (1 h), 2 ETH (24 h)** | V0 damps thin-volume noise: a lone 0.05 ETH sell cannot trip the tax. |
| 1 | `dev` | `max(0, 1 − spot_after / TWAP30)` | Measured *after* the swap (fee taken in `afterSwap` on the ETH output), so a single-block dump cannot dodge the fee. The stress test shows the earlier `beforeSwap` version charged a one-block 5 ETH dump only 1% [S]. |
| 1 | Update and decay | Recomputed on **every sell**. It rises at once. The stored fee falls by at most **1 pp per 10 min** toward the target. The 1 h term clears within 1 h, the 24 h term within 24 h. | Stress [S]: after a 5 ETH dump the fee peaks at 12.5%, is 4% after 2 h, 2–3% while the 24 h window holds the dump, and back to base after ~25 h. |
| 1 | Sell-tax routing (excess over 1%) | **35% buy & burn / 40% buy → reward pool / 15% team / 10% heartbeat** | Most of it goes back to the players who stay, as rewards. Team ≤ 20% per stream. |
| 2 | Withdrawal tax | `wtax(age) = max(5%, 20% − 15%·age/7 d)`, where age = token-weighted time since the reward accrued (FIFO "vintage" buckets per day) | As briefed. The 7-day decay rewards patience without trapping funds. |
| 2 | Redistribution | Tax tokens are added to the next tick's accrual, **pro-rata by effective hash** across all farms | Goes to "players who stay"; no extra emission. |
| 2 | In-game spending of unclaimed rewards | **0% tax and +5% purchasing power** on upgrades, repairs, electricity prepay, lobbying (token lobby is burned) and token-paid packs | As briefed. |
| 2 | **Token-paid packs** | Price = pack ETH price / TWAP30 × (1/1.05). **Max 1 per wallet per day.** Tokens: 70% back to the reward pool, 30% burned. **No team cut** (team is ETH only). | Without the cap, incumbents compound hash: in a v2 run without the IMD-policy flag, 50% of in-game spending on packs moved the hype stall from 31 to 20 (scratch run, reproducible with `token_pack_share=0.5, imd_policy=False`) [S]. The sim models the cap as 25% of in-game spending. |
| 2 | Behaviour response [A] | Share of sell intent moved in game = 1.5 × average withdrawal tax (13.6%) = 20%. Share deferred (held) = 1.0 × (sell fee − 1%) | Effective sold share 65% → **51.8%** (steady) [S]. |
| 3 | Referrals | Inviter earns **5% of the referee's mining rewards**, paid **on top from the reward pool**, one level. `referrer` is set once on the first action (pack, claim or place), must be ≠ self and must already have a farm. Unreferred players pay nothing extra. | Extra emission = 5% × referred share (40% assumed) = **+2.0% of emission**: steady 9.6 M tokens over 35 days [S]. |
| 4 | IMD NFT starter pack | One per tokenId of the Identity MD collection (**1,999 items, ~820 owners** on OpenSea [F]). Merkle root of `(tokenId, owner)` at a **fixed Ethereum block chosen by the owner and set once** before launch. Claim window: **hour 48 to day 16**. 3 items, rarity floor Rare (C→R, L→E: R 92% / E 8%). **"Starter" edition: non-transferable, 50% hash until the claimer opens one paid pack** | Opening on day 1 at full hash cut the hype stall from 13 to 4 [S]. Hour-48 start with 50% hash gives 7. Expected starter hash at full rate: 57.9 vs 38.3 for a paid pack. |
| 4 | Claim rate [A] | **35%** (700 packs). Sensitivity 10–60%. | Token airdrops see ~63–64% claimed (Arbitrum after day 1, Anchor) [F]. A ~$25 game pack on another chain, needing bridged gas, should claim lower [I]. Cost: 6.5–6.7 ETH of forgone list price plus dilution [S]. |
| 5 | Lobbying | Players pay ETH for their district: **85% buy & burn, 10% team, 5% heartbeat**. Per-district lobby `L_d` decays with a 3-day half-life. Blackout selection weight `w_d = max(0.40, 1/(1 + 0.5·L_d/max(L̄, 0.05 ETH)))` | At most −60% weight, so never a guarantee. At 4× the mean lobby, a district's blackout odds fall from 12.5% to ~6.8–7.5% [S]. Unlobbied districts rise to ~15–18%. The cooldown still applies. |
| 5 | Lobby volume [A] | 0.00004 ETH per active farm per day (~$0.10) | The rational value is small: blackouts cost ~1.25% of income [I]. So lobbying is a social burn, not an economic lever. |
| 5 | Electricity tariff | Set **daily by the swarm**, **±10%/day**, bounds **0.10–0.30** of rpsEMA | v1 found tariff the strongest churn lever. The sim policy: lower it when a new pack's projected payback is > 35 d, raise it when < 25 d and the price is falling. |
| 5 | Weekly inspection bonus | Score = 7-day burned spend ÷ 7-day gross accrual, for farms ≥ 100 hash. Top farm wins **1% of the week's emission** (paid from the pool, half sold [A]). Permissionless: during a 24 h window anyone submits a candidate and the contract keeps the max. | O(1) on chain. The swarm does not pick the winner. |
| 6 | Beta caps (no admin) | Per wallet per rolling 24 h: **3 packs (h 0–12), 6 (h 12–24), 10 (h 24–48), then 20**. Global per hour: **75 (h 0–6), 150 (h 6–24), 300 (h 24–48), then uncapped**. All derived from `block.timestamp − launchTime`. | Hype: first-hour demand of ~293 packs queues up to 757 packs, cleared by hour 15. No daily total changes [S]. Steady and weak never queue. |
| — | Team share per stream | Packs 15%, base fee 20%, sell tax 15%, lobby 10%; **each ≤ 20%** (contract-enforced) | Aggregate 15.0% in all scenarios [S]. |

---

## 2. Simulation model changes

Unchanged from v1:
- the AMM is constant product with a virtual ETH reserve
- daily steps with two event ticks
- cohorts by purchase day, with payback per active pack
- projection to 120 days
- the stall rule: the first day ≥ 3 on which a new pack does not pay back within 60 days, or farms fall below 25% of peak

Added, each switchable for the ablation:
- **IMD policy:**
  - 900 M tokens in the pool.
  - A 0.25% network fee on every swap.
  - The swarm's 100 M tokens: 50% sold evenly over days 1–14 [A].
- **Sell fee:**
  - In the 35-day run, the daily imbalance is net sells against system buys (pack buys, lobby burns, fee buybacks) plus external buys.
  - The 1 h term is taken as 1.25× the 24 h term [A]. TWAP deviation is taken as half of the day's price drop [A].
  - The exact 5-minute formula is exercised separately in the stress test (§3.6).
- **External traders [A]:** round-trip volume of 0.5 × the day's pack ETH. They pay the base fee on the buy and the dynamic fee on the sell.
- **Claims:**
  - Claims are spread by age: 40% claimed on day 0, 30% on day 3, 30% on day 7 [A]. This gives an average withdrawal tax of 13.6%.
  - Tokens reach the AMM with that delay. For per-cohort accounting they are valued at the day's execution price (approximation).
  - Unclaimed holdings are valued at the pool price × 0.95.
- **Free NFT packs** are separate zero-cost cohorts. They are excluded from payback and stall but included in hash and active farms.
- **Not modelled:** see §10.

---

## 3. Results per scenario [S] (recommended defaults, 10 ETH virtual reserve for comparability with v1)

Notes on the tables:
- Price is in ETH per 1 M tokens.
- "Sell fee" is the day's average effective fee rate, excluding the 0.25% network fee.
- "Runway" is the number of days for the pool to fall to 10% of its peak with zero inflow.
- The table carries both the reward pool and the burned/supply figures. Supply = 1 B − burned.

### 3.1 Hype

| day | active farms | packs | pack price | pack ETH | lobby ETH | burned (cum) | supply | reward pool | price ETH/1M | runway d | net yield/pack/day ETH | sell fee | tariff | team ETH (cum) | heartbeat ETH (cum) | events |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 616 | 1875 | 0.0100 | 18.75 | 0.025 | 40.4M | 959.6M | 477.6M | 0.0632 | 65 | 0.000441 | 1.0% | 0.150 | 2.85 | 1.90 | heatwave/surge |
| 2 | 927 | 769 | 0.0144 | 11.05 | 0.038 | 60.1M | 939.9M | 545.1M | 0.1108 | 65 | 0.000542 | 1.0% | 0.150 | 4.54 | 3.01 | blackout/surge |
| 3 | 1382 | 1309 | 0.0100 | 13.09 | 0.056 | 78.3M | 921.7M | 584.7M | 0.1817 | 65 | 0.000560 | 1.0% | 0.150 | 6.54 | 4.34 | heatwave/heatwave |
| 5 | 2069 | 936 | 0.0100 | 9.37 | 0.084 | 109.1M | 890.9M | 597.3M | 0.3007 | 65 | 0.000596 | 1.0% | 0.150 | 9.74 | 6.47 | surge/heatwave |
| 7 | 2475 | 686 | 0.0100 | 6.86 | 0.100 | 135.8M | 864.2M | 580.4M | 0.3652 | 64 | 0.000547 | 1.0% | 0.150 | 12.03 | 7.98 | heatwave/audit |
| 10 | 2833 | 500 | 0.0085 | 4.25 | 0.115 | 170.6M | 829.4M | 543.7M | 0.3696 | 62 | 0.000426 | 1.8% | 0.165 | 14.33 | 9.50 | blackout/heatwave |
| 14 | 3051 | 324 | 0.0085 | 2.76 | 0.124 | 214.0M | 786.0M | 489.8M | 0.3287 | 59 | 0.000272 | 2.9% | 0.200 | 16.41 | 10.87 | heatwave/audit |
| 17 | 3101 | 279 | 0.0072 | 2.02 | 0.126 | 242.5M | 757.5M | 451.3M | 0.3292 | 57 | 0.000241 | 1.4% | 0.200 | 17.45 | 11.55 | heatwave/surge |
| 21 | 3065 | 228 | 0.0072 | 1.65 | 0.125 | 276.3M | 723.7M | 402.1M | 0.3204 | 54 | 0.000202 | 2.1% | 0.162 | 18.60 | 12.31 | heatwave/surge |
| 24 | 3011 | 222 | 0.0061 | 1.36 | 0.123 | 297.8M | 702.2M | 369.3M | 0.3123 | 51 | 0.000170 | 1.9% | 0.146 | 19.29 | 12.76 | heatwave/audit |
| 28 | 2916 | 205 | 0.0061 | 1.26 | 0.119 | 322.4M | 677.6M | 328.7M | 0.3005 | 48 | 0.000155 | 2.3% | 0.100 | 20.15 | 13.32 | surge/heatwave |
| 31 | 2818 | 199 | 0.0060 | 1.20 | 0.115 | 338.5M | 661.5M | 302.7M | 0.2949 | 46 | 0.000132 | 1.6% | 0.100 | 20.75 | 13.71 | audit/heatwave |
| 35 | 2656 | 179 | 0.0060 | 1.07 | 0.109 | 357.9M | 642.1M | 271.2M | 0.2874 | 42 | 0.000113 | 2.1% | 0.100 | 21.49 | 14.20 | heatwave/blackout |

| join week | avg pack price ETH | paid back by day 35 | avg payback days (incl. projected) | projected never (<=120 d) |
|---:|---:|---:|---:|---:|
| 1 | 0.0107 | 25% | 50.8 | 10% |
| 2 | 0.0085 | 0% | 56.4 | 21% |
| 3 | 0.0072 | 0% | 58.8 | 52% |
| 4 | 0.0061 | 0% | 72.8 | 70% |
| 5 | 0.0060 | 0% | n/a | 100% |

| week | pack ETH | lobby ETH | base hook fees ETH | sell tax ETH | team ETH | team % of inflow | heartbeat ETH | withdrawal tax redistributed (M tok) | avg sell fee |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 78.69 | 0.468 | 0.908 | 0.001 | 12.03 | 15.0% | 7.98 | 6.5 | 1.0% |
| 2 | 27.56 | 0.818 | 0.523 | 0.382 | 4.38 | 14.9% | 2.89 | 6.0 | 2.0% |
| 3 | 13.57 | 0.878 | 0.253 | 0.092 | 2.19 | 14.8% | 1.44 | 5.0 | 1.5% |
| 4 | 9.38 | 0.851 | 0.190 | 0.131 | 1.55 | 14.7% | 1.01 | 4.5 | 1.9% |
| 5 | 8.13 | 0.795 | 0.162 | 0.090 | 1.35 | 14.7% | 0.88 | 3.9 | 1.7% |

- Player ETH inflow: packs 137.34 + lobbying 3.81 + base hook fees 2.03 + progressive sell tax 0.70 = **143.88 ETH**
- Team ETH **21.49** (= 14.9% of inflow: packs 20.60, base fee 0.41, sell tax 0.10, lobby 0.38); heartbeat ETH 14.20
- Withdrawal tax redistributed to staying farms: 25.9M tokens (~7.84 ETH at the day's price)
- Referral emission 11.2M tokens; inspection bonuses 5.61M; packs bought with tokens 494
- Free NFT packs claimed 700 (forgone pack ETH at list price 6.67)
- Effective share of free tokens sold: 51.5% (intent 65%), moved in game 13.2%
- Peak active farms 3101; day-35 farms 2656; min reward pool after day 1 271.2M; day-35 runway 42 d
- **Stall day: 4**

### 3.2 Steady

| day | active farms | packs | pack price | pack ETH | lobby ETH | burned (cum) | supply | reward pool | price ETH/1M | runway d | net yield/pack/day ETH | sell fee | tariff | team ETH (cum) | heartbeat ETH (cum) | events |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 148 | 450 | 0.0100 | 4.50 | 0.006 | 27.6M | 972.4M | 197.1M | 0.0197 | 65 | 0.000198 | 1.0% | 0.135 | 0.68 | 0.45 | heatwave/surge |
| 2 | 241 | 292 | 0.0100 | 2.92 | 0.010 | 43.8M | 956.2M | 271.7M | 0.0264 | 65 | 0.000216 | 1.0% | 0.122 | 1.13 | 0.75 | blackout/surge |
| 3 | 393 | 337 | 0.0100 | 3.37 | 0.016 | 59.6M | 940.4M | 332.7M | 0.0352 | 65 | 0.000215 | 1.0% | 0.109 | 1.64 | 1.09 | heatwave/heatwave |
| 5 | 605 | 219 | 0.0100 | 2.19 | 0.025 | 82.2M | 917.8M | 374.0M | 0.0468 | 65 | 0.000219 | 1.0% | 0.100 | 2.30 | 1.52 | surge/heatwave |
| 7 | 751 | 235 | 0.0100 | 2.35 | 0.031 | 104.1M | 895.9M | 400.4M | 0.0603 | 65 | 0.000231 | 1.0% | 0.100 | 3.01 | 2.00 | heatwave/audit |
| 10 | 989 | 296 | 0.0085 | 2.52 | 0.040 | 135.2M | 864.8M | 422.9M | 0.0826 | 65 | 0.000233 | 1.0% | 0.100 | 4.16 | 2.76 | blackout/heatwave |
| 14 | 1291 | 305 | 0.0085 | 2.60 | 0.052 | 174.0M | 826.0M | 426.8M | 0.1113 | 65 | 0.000226 | 1.0% | 0.100 | 5.75 | 3.81 | heatwave/audit |
| 17 | 1492 | 344 | 0.0072 | 2.49 | 0.061 | 200.5M | 799.5M | 418.9M | 0.1396 | 64 | 0.000224 | 1.0% | 0.100 | 6.90 | 4.57 | heatwave/surge |
| 21 | 1713 | 351 | 0.0072 | 2.54 | 0.070 | 233.0M | 767.0M | 399.1M | 0.1765 | 63 | 0.000216 | 1.0% | 0.100 | 8.46 | 5.60 | heatwave/surge |
| 24 | 1869 | 392 | 0.0061 | 2.41 | 0.076 | 255.5M | 744.5M | 381.4M | 0.2023 | 61 | 0.000190 | 1.0% | 0.100 | 9.58 | 6.34 | heatwave/audit |
| 28 | 2068 | 398 | 0.0061 | 2.45 | 0.084 | 283.4M | 716.6M | 355.3M | 0.2348 | 59 | 0.000176 | 1.0% | 0.100 | 11.10 | 7.35 | surge/heatwave |
| 31 | 2209 | 408 | 0.0060 | 2.45 | 0.090 | 302.7M | 697.3M | 336.9M | 0.2605 | 58 | 0.000155 | 1.0% | 0.100 | 12.25 | 8.10 | audit/heatwave |
| 35 | 2382 | 413 | 0.0060 | 2.48 | 0.097 | 326.5M | 673.5M | 312.6M | 0.2934 | 56 | 0.000141 | 1.0% | 0.100 | 13.80 | 9.12 | heatwave/blackout |

| join week | avg pack price ETH | paid back by day 35 | avg payback days (incl. projected) | projected never (<=120 d) |
|---:|---:|---:|---:|---:|
| 1 | 0.0100 | 88% | 27.9 | 0% |
| 2 | 0.0085 | 28% | 30.6 | 0% |
| 3 | 0.0072 | 0% | 33.8 | 0% |
| 4 | 0.0061 | 0% | 36.5 | 0% |
| 5 | 0.0060 | 0% | 57.2 | 0% |

| week | pack ETH | lobby ETH | base hook fees ETH | sell tax ETH | team ETH | team % of inflow | heartbeat ETH | withdrawal tax redistributed (M tok) | avg sell fee |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 19.67 | 0.135 | 0.213 | 0.000 | 3.01 | 15.0% | 2.00 | 4.2 | 1.0% |
| 2 | 17.76 | 0.303 | 0.230 | 0.000 | 2.74 | 15.0% | 1.81 | 5.5 | 1.0% |
| 3 | 17.49 | 0.439 | 0.228 | 0.000 | 2.71 | 14.9% | 1.79 | 5.5 | 1.0% |
| 4 | 16.92 | 0.545 | 0.240 | 0.000 | 2.64 | 14.9% | 1.74 | 4.9 | 1.0% |
| 5 | 17.19 | 0.640 | 0.252 | 0.000 | 2.69 | 14.9% | 1.78 | 4.3 | 1.0% |

- Player ETH inflow: packs 89.04 + lobbying 2.06 + base hook fees 1.16 + progressive sell tax 0.00 = **92.27 ETH**
- Team ETH **13.80** (= 15.0% of inflow: packs 13.36, base fee 0.23, sell tax 0.00, lobby 0.21); heartbeat ETH 9.12
- Withdrawal tax redistributed to staying farms: 24.4M tokens (~3.69 ETH at the day's price)
- Referral emission 9.6M tokens; inspection bonuses 4.79M; packs bought with tokens 246
- Free NFT packs claimed 700 (forgone pack ETH at list price 6.49)
- Effective share of free tokens sold: 51.8% (intent 65%), moved in game 13.2%
- Peak active farms 2382; day-35 farms 2382; min reward pool after day 1 271.7M; day-35 runway 56 d
- **Stall day: 34**

### 3.3 Weak

| day | active farms | packs | pack price | pack ETH | lobby ETH | burned (cum) | supply | reward pool | price ETH/1M | runway d | net yield/pack/day ETH | sell fee | tariff | team ETH (cum) | heartbeat ETH (cum) | events |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 44 | 135 | 0.0100 | 1.35 | 0.002 | 11.7M | 988.3M | 70.3M | 0.0134 | 65 | 0.000146 | 1.0% | 0.135 | 0.21 | 0.14 | heatwave/surge |
| 2 | 68 | 80 | 0.0100 | 0.80 | 0.003 | 19.2M | 980.8M | 103.9M | 0.0148 | 65 | 0.000154 | 1.0% | 0.122 | 0.33 | 0.22 | blackout/surge |
| 3 | 137 | 80 | 0.0100 | 0.80 | 0.006 | 26.8M | 973.2M | 133.1M | 0.0162 | 65 | 0.000115 | 1.0% | 0.109 | 0.45 | 0.30 | heatwave/heatwave |
| 5 | 260 | 74 | 0.0100 | 0.74 | 0.011 | 41.6M | 958.4M | 177.0M | 0.0189 | 65 | 0.000105 | 1.0% | 0.100 | 0.68 | 0.45 | surge/heatwave |
| 7 | 302 | 66 | 0.0100 | 0.66 | 0.013 | 55.6M | 944.4M | 205.9M | 0.0214 | 65 | 0.000115 | 1.0% | 0.100 | 0.89 | 0.59 | heatwave/audit |
| 10 | 363 | 72 | 0.0085 | 0.61 | 0.015 | 75.7M | 924.3M | 235.3M | 0.0249 | 65 | 0.000119 | 1.0% | 0.100 | 1.19 | 0.79 | blackout/heatwave |
| 14 | 423 | 60 | 0.0085 | 0.51 | 0.018 | 101.0M | 899.0M | 251.2M | 0.0284 | 65 | 0.000114 | 1.0% | 0.100 | 1.53 | 1.01 | heatwave/audit |
| 17 | 452 | 65 | 0.0072 | 0.47 | 0.019 | 118.8M | 881.2M | 255.3M | 0.0317 | 65 | 0.000115 | 1.0% | 0.100 | 1.76 | 1.17 | heatwave/surge |
| 21 | 450 | 55 | 0.0072 | 0.40 | 0.019 | 140.7M | 859.3M | 250.5M | 0.0352 | 64 | 0.000114 | 1.0% | 0.100 | 2.03 | 1.34 | heatwave/surge |
| 24 | 450 | 60 | 0.0061 | 0.37 | 0.019 | 156.2M | 843.8M | 244.2M | 0.0375 | 63 | 0.000103 | 1.0% | 0.100 | 2.21 | 1.46 | heatwave/audit |
| 28 | 444 | 51 | 0.0061 | 0.31 | 0.018 | 175.3M | 824.7M | 231.2M | 0.0399 | 62 | 0.000099 | 1.0% | 0.100 | 2.42 | 1.60 | surge/heatwave |
| 31 | 435 | 48 | 0.0060 | 0.29 | 0.018 | 188.6M | 811.4M | 221.0M | 0.0415 | 61 | 0.000089 | 1.0% | 0.100 | 2.56 | 1.69 | audit/heatwave |
| 35 | 418 | 41 | 0.0060 | 0.25 | 0.017 | 204.8M | 795.2M | 205.9M | 0.0431 | 59 | 0.000084 | 1.0% | 0.100 | 2.73 | 1.80 | heatwave/blackout |

| join week | avg pack price ETH | paid back by day 35 | avg payback days (incl. projected) | projected never (<=120 d) |
|---:|---:|---:|---:|---:|
| 1 | 0.0100 | 0% | n/a | 100% |
| 2 | 0.0085 | 0% | n/a | 100% |
| 3 | 0.0072 | 0% | 103.9 | 53% |
| 4 | 0.0061 | 0% | 96.8 | 39% |
| 5 | 0.0060 | 0% | n/a | 100% |

| week | pack ETH | lobby ETH | base hook fees ETH | sell tax ETH | team ETH | team % of inflow | heartbeat ETH | withdrawal tax redistributed (M tok) | avg sell fee |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 5.83 | 0.054 | 0.063 | 0.000 | 0.89 | 15.0% | 0.59 | 1.9 | 1.0% |
| 2 | 4.11 | 0.110 | 0.052 | 0.000 | 0.64 | 14.9% | 0.42 | 3.2 | 1.0% |
| 3 | 3.17 | 0.130 | 0.039 | 0.000 | 0.50 | 14.9% | 0.33 | 3.4 | 1.0% |
| 4 | 2.48 | 0.129 | 0.033 | 0.000 | 0.39 | 14.8% | 0.26 | 3.2 | 1.0% |
| 5 | 1.93 | 0.124 | 0.028 | 0.000 | 0.31 | 14.8% | 0.20 | 2.9 | 1.0% |

- Player ETH inflow: packs 17.52 + lobbying 0.55 + base hook fees 0.21 + progressive sell tax 0.00 = **18.28 ETH**
- Team ETH **2.73** (= 14.9% of inflow: packs 2.63, base fee 0.04, sell tax 0.00, lobby 0.05); heartbeat ETH 1.80
- Withdrawal tax redistributed to staying farms: 14.7M tokens (~0.47 ETH at the day's price)
- Referral emission 5.6M tokens; inspection bonuses 2.81M; packs bought with tokens 32
- Free NFT packs claimed 700 (forgone pack ETH at list price 6.49)
- Effective share of free tokens sold: 51.8% (intent 65%), moved in game 13.2%
- Peak active farms 453; day-35 farms 418; min reward pool after day 1 103.9M; day-35 runway 59 d
- **Stall day: 3**

### 3.4 Per-week team and heartbeat ETH

These are in the weekly tables above. Summary:

| Scenario | Inflow (35 d) | Team ETH | Team % | Heartbeat ETH | Sell tax collected (excess over base) | Withdrawal tax redistributed |
|---|---:|---:|---:|---:|---:|---:|
| hype | 143.88 | 21.49 | 14.9% | 14.20 | 0.70 ETH | 25.9 M tok (~7.84 ETH) |
| steady | 92.27 | 13.80 | 15.0% | 9.12 | 0.00 ETH | 24.4 M tok (~3.69 ETH) |
| weak | 18.28 | 2.73 | 14.9% | 1.80 | 0.00 ETH | 14.7 M tok (~0.47 ETH) |

The sell tax raises little in this model. The daily-average fee only exceeds the base in hype (max 2.9%), because system buys from packs offset player sells most days [S]. In practice, revenue from the sell tax will come from intraday dumps, which a daily model cannot see. Team income is driven by packs: 97% in steady.

### 3.5 Beta caps, lobbying, fairness

**Beta caps** (packs per day without → with caps)

- hype: day 1 1875 -> 1875; day 2 769 -> 769; day 3 1309 -> 1309
- steady: day 1 450 -> 450; day 2 292 -> 292; day 3 337 -> 337
- weak: day 1 135 -> 135; day 2 80 -> 80; day 3 80 -> 80
  - hype hourly queue: first-hour demand 293 packs vs cap 75/h; max queue 757 packs; queue cleared at hour 15
  - steady hourly queue: first-hour demand 70 packs vs cap 75/h; max queue 0 packs; queue cleared at hour never queued
  - weak hourly queue: first-hour demand 21 packs vs cap 75/h; max queue 0 packs; queue cleared at hour never queued

**Lobbying curve**

| district lobby vs district mean | selection weight | blackout odds if only this district lobbies (8 districts) | change vs 12.5% |
|---:|---:|---:|---:|
| 0x | 1.00 | 18.3% | +47% |
| 0.5x | 0.80 | 14.9% | +19% |
| 1x | 0.67 | 12.5% | +0% |
| 2x | 0.50 | 9.3% | -26% |
| 4x | 0.40 | 6.8% | -45% |
| 8x | 0.40 | 5.4% | -57% |
| 32x | 0.40 | 5.4% | -57% |

Long-run blackout share per district with the 6-tick cooldown, lobby profile [4,4,1,1,0.25,0.25,0.25,0.25] x mean: 7.5%, 7.4%, 12.4%, 12.5%, 15.1%, 15.0%, 15.0%, 15.0%

**Event fairness** (28 days, 4,000 farms; 1.00 = income with no events)

| setting | p1 | p5 | median | p95 | p99 |
|---|---:|---:|---:|---:|---:|
| cooldown, no lobbying (v1) | 0.996 | 0.997 | 1.013 | 1.030 | 1.030 |
| cooldown + lobbying profile | 0.990 | 0.997 | 1.016 | 1.030 | 1.030 |

### 3.6 Sell-fee stress test (exact on-chain rule, 5-minute steps) [S]

Setup:
- The pool holds 30 ETH virtual against 120 M tokens.
- Background flow: 0.02 ETH buys and 0.02 ETH sells every 5 minutes.
- At minute 60, one wallet dumps tokens.

| case | dumper's avg sell fee | peak fee | fee back within 0.5 pp of base at minute |
|---|---:|---:|---:|
| 1.5 ETH dump over 30 min, pool 30 ETH real-equivalent | 6.13% | 8.11% | 1005 |
| 5 ETH dump over 30 min | 10.88% | 12.52% | 1520 |
| 5 ETH dump in one 5-min block | 12.59% | 12.59% | 1505 |
| 20 ETH dump over 30 min (extreme) | 13.26% | 13.88% | 1525 |

Fee path, 5 ETH dump over 30 min (minute: fee): 60: 1.0%, 65: 6.9%, 70: 10.3%, 80: 11.9%, 90: 12.5%, 100: 12.0%, 120: 10.0%, 150: 7.0%, 180: 4.0%, 240: 3.1%, 360: 2.9%, 720: 2.4%, 1440: 2.0%, 1500: 2.0%, 1560: 1.0%, 1800: 1.0%

Max daily-average sell fee in the 35-day runs: hype 2.9%, steady 1.0%, weak 1.0%

Readings:
- A dumper pays 6–13% on the dump.
- The cap is never reached.
- Normal sellers who arrive in the next ~2 h pay elevated fees (10% → 4%). For ~24 h they pay 2–3%, because the 24 h term remembers the dump.

This is a deliberate trade-off. To shorten the tail, the heartbeat may lower `a24h` (bounds in §5).

---

## 4. Comparison with the previous report [S]

"v1 model" is the v1 simulation reproduced exactly by v2 with every new flag off. Each "+" row adds one mechanic to v1. Each "v2 minus" row removes one mechanic from the full v2.

| variant | steady wk1 / wk4 payback d | steady stall | hype wk1 / wk3 payback d | hype stall | weak stall | steady team ETH (% inflow) | hype team ETH (% inflow) | steady day-35 price /1M |
|---|---|---|---|---|---|---|---|---|
| **v1 model (all new mechanics off)** | 27.2 / 36.6 | 33 | 34.6 / 58.0 | 13 | 3 | 13.2 (15.0%) | 20.5 (15.0%) | 0.231 |
| + progressive sell tax | 27.2 / 36.6 | 33 | 41.5 / 53.6 | 13 | 3 | 13.2 (15.0%) | 20.6 (15.0%) | 0.231 |
| + withdrawal tax / in-game bonus | 26.9 / 41.3 | 32 | 35.7 / 53.1 | 13 | 3 | 13.2 (15.0%) | 20.5 (15.0%) | 0.284 |
| + referrals 5% | 27.0 / 36.9 | 33 | 34.6 / 61.9 | 13 | 3 | 13.2 (15.0%) | 20.4 (15.0%) | 0.228 |
| + free NFT packs | 30.8 / 37.9 | 34 | 39.5 / 55.1 | 7 | 3 | 13.3 (15.0%) | 20.6 (15.0%) | 0.234 |
| + lobbying | 26.8 / 34.9 | 34 | 35.8 / 53.7 | 14 | 3 | 13.4 (14.9%) | 20.8 (14.9%) | 0.241 |
| + swarm tariff controller | 25.9 / 34.9 | 34 | 36.5 / 47.0 | 32 | 3 | 13.3 (15.0%) | 20.5 (15.0%) | 0.218 |
| + inspection bonus | 27.5 / 37.5 | 33 | 36.3 / 62.0 | 12 | 3 | 13.2 (15.0%) | 20.4 (15.0%) | 0.228 |
| + 48 h beta caps | 27.2 / 36.6 | 33 | 34.6 / 58.0 | 13 | 3 | 13.2 (15.0%) | 20.5 (15.0%) | 0.231 |
| + external trader volume | 26.6 / 35.0 | 34 | 35.9 / 54.0 | 13 | 3 | 13.4 (15.1%) | 20.7 (15.1%) | 0.235 |
| + IMD launch policy (90% pool, 0.25% network fee, swarm sells 5%) | 29.1 / 36.6 | 34 | 55.6 / 69.8 | 4 | 3 | 13.1 (15.0%) | 20.4 (15.0%) | 0.237 |
| **v2: all mechanics on** | 27.9 / 36.5 | 34 | 50.8 / 58.8 | 4 | 3 | 13.8 (15.0%) | 21.5 (14.9%) | 0.293 |
| v2 minus sell tax | 27.9 / 36.5 | 34 | 52.4 / 58.8 | 4 | 3 | 13.8 (15.0%) | 21.4 (14.9%) | 0.293 |
| v2 minus withdrawal tax | 28.8 / 33.0 | none | 52.4 / 69.3 | 4 | 3 | 13.8 (15.0%) | 21.4 (14.9%) | 0.237 |
| v2 minus referrals | 28.6 / 36.3 | 34 | 51.5 / 67.5 | 4 | 3 | 13.8 (15.0%) | 21.5 (14.9%) | 0.296 |
| v2 minus external trader volume | 29.0 / 38.0 | 33 | 52.3 / 63.0 | 4 | 3 | 13.6 (14.9%) | 21.2 (14.9%) | 0.289 |
| v2 minus IMD policy (1 B in pool, no network fee, no swarm sells) | 26.7 / 36.9 | 33 | 31.9 / 44.4 | 31 | 3 | 13.8 (15.0%) | 21.5 (14.9%) | 0.286 |

What each mechanic changed, in order of mechanics briefed:

| Mechanic | Effect in the sim | Interpretation [I] |
|---|---|---|
| 1. Progressive sell tax | Alone: steady unchanged, hype week-3 payback 58 → 54 d. In v2: ≈ 0 effect at daily resolution. | It is a dump brake and price-stability feature, not a revenue or payback lever. Its value is intraday (§3.6), which this daily model understates. |
| 2. Withdrawal tax + in-game bonus | Sold share 65% → 52%. Steady day-35 price +23%. 24–26 M tokens redistributed per scenario. Steady week-4 payback 36.6 → 41.3 d on its own; removing it from v2 moves steady stall 34 → none. | Holding works, but reinvested rewards become hash and dilute newcomers. That is why token-paid packs are capped. It is a trade between price support and late-joiner fairness. |
| 3. Referrals 5% | +2% emission; small negative effect on payback (hype week-3 58 → 62 d). | Cheap growth tool. The effect on demand (more players) is not modelled, so this is cost only. |
| 4. Free NFT packs | Alone (hour 48, 50% hash): steady week-1 payback 27 → 31 d, hype stall 13 → 7. | A large dilution relative to early inflow. Mitigation: hour-48 start and 50% Starter hash. Keep it as a marketing cost and be honest about it. |
| 5a. Lobbying | 2.06 ETH of lobby ETH in steady (1.75 ETH bought and burned); small positive effect. At 5× volume, steady never stalls. | A good sink if players like it. |
| 5b. Swarm tariff (±10%/d) | Hype stall 13 → 32 on its own, the strongest new lever. | The tariff falls to its 0.10 floor in steady and weak, so its power is used up early. |
| 5c. Inspection bonus | ≈ 0 (1% of weekly emission). | Engagement, not economics. |
| 6. Beta caps | No daily change; smooths hours 0–15 of hype. | A safety feature only. |
| IMD launch policy | Hype stall 13 → 4 in v1. In v2, removing it moves hype 4 → 31. | The swarm's 10% unlock is the main external risk. |

---

## 5. Failure modes and heartbeat parameters

The heartbeat may change **only** these parameters, within bounds, at most **one step per epoch (7 d)** unless stated. Every change is emitted in the tick letter.

The heartbeat can **never** change:
- team shares
- the 15% sell-fee cap
- the base fee (IMD policy)
- item tables, rarity odds or NFT terms
- the referral rate
- mint rights

| # | Failure mode | Early signal | Lever (bounds; max step) |
|---|---|---|---|
| 1 | Inflow collapse (weak) | packs₂₄h < 25% of the 7-day average | `epochPriceStep` 0–20% (±5 pp). `packPriceFloor` 0.004–0.010. `tariff` toward 0.10. **The weak case still stalls on day 3. There is no parameter fix.** |
| 2 | Sell spiral / swarm unlock dump | spot < 0.9 × 24 h TWAP | `a1h` 2–6% (±1 pp/day). `a24h` 0–5% (±1 pp/day). `kTwap` 0.2–0.5 (±0.1/day). Max total stays 15%. `sellTaxSplit.burn` 20–50% (±10 pp; reward takes the difference). |
| 3 | Hype overbuy | packs₂₄h > 3× target | `surgePremiumCap` 0–100% (±25 pp). `surgeTargetPacks` 500–3000. |
| 4 | Emission speed | runway < 30 d | `emissionRate` 2.5–5.0%/day (±0.5 pp). |
| 5 | Upkeep churn | daily churn > 5% | **`tariff` 0.10–0.30, ±10% per day** (daily, new). `repairPerPoint` 0.015–0.04. |
| 6 | Reinvest dilution of newcomers | week-N payback > target + 10 d | `ingameBonus` 0–10% (±2.5 pp). `tokenPacksPerWalletDay` 0–2 (±1). `tokenPackRecycle` 50–90% (±10 pp). |
| 7 | Withdrawal tax too punitive | claims/day < 20% of accrual for 3 days, or churn spike | `wtaxDay0` 10–25% (±5 pp). `wtaxFloor` 0–5% (±2.5 pp; may only be lowered). `wtaxDecayDays` 3–14 (±2). |
| 8 | Referral farming (sybil inviters) | > 30% of referrers with ≥ 10 referees that each have < 1 paid pack | `referralMinPaidPacks` 0–3 (the referee must open N paid packs before the inviter earns). The rate itself is fixed. |
| 9 | Lobby capture | one district > 40% of 7-day lobby | `lobbyK` 0.25–1.0 (±0.25). `lobbyMinWeight` 0.40–0.70 (may only be raised). |
| 10 | Event unfairness | district 7-day income < 0.9 × mean | Event odds within v1 bounds. Cooldown ≥ 6 ticks (may only be raised). |
| 11 | Beta overload | n/a | No lever. Caps lift by time only. |
| 12 | Inspection gaming (wash burns) | winner score > 3× the median | `inspectionShare` 0–2% (±0.5 pp). `inspectionMinHash` 100–2,000. |
| 13 | MEV on buybacks | slippage > 2% | Keeper batch 0.1–1 ETH. TWAP tolerance 1–3%. |
| 14 | Pool emptying | impossible: pool-proportional emission plus ≤ 2% referral top-up and ≤ 1%/week inspection | none |

---

## 6. Liquidity and launch: sensitivity with the new mechanics [S]

Virtual ETH here means the ETH-equivalent depth of the single-sided pool at open. For a range from price P₀ to ∞, the virtual ETH reserve equals P₀ × pooled tokens [I]. So virtual ETH = opening cap × `poolBps`/10,000. Payback figures are in days.

| virtual ETH | sell intent | steady wk1 / wk4 payback | steady stall | hype stall | weak stall | steady team % | steady effective sold share | steady day-35 price /1M |
|---:|---:|---|---|---|---|---:|---:|---:|
| 3 | 50% | 15.1 / 18.3 (never 0%) | none | none | 28 | 15.0% | 39.8% | 0.490 |
| 3 | 65% | 18.6 / 26.5 (never 0%) | 35 | 7 | 5 | 15.0% | 51.8% | 0.380 |
| 3 | 90% | 31.8 / 51.3 (never 0%) | 27 | 4 | 3 | 15.0% | 71.6% | 0.256 |
| 5 | 50% | 18.0 / 21.5 (never 0%) | none | none | 5 | 15.0% | 39.8% | 0.443 |
| 5 | 65% | 21.8 / 28.3 (never 0%) | none | 7 | 3 | 15.0% | 51.8% | 0.350 |
| 5 | 90% | 40.2 / 53.9 (never 29%) | 14 | 4 | 3 | 15.0% | 71.7% | 0.244 |
| 10 | 50% | 22.9 / 27.5 (never 0%) | none | none | 3 | 14.9% | 39.8% | 0.345 |
| 10 | 65% | 27.9 / 36.5 (never 0%) | 34 | 4 | 3 | 15.0% | 51.8% | 0.293 |
| 10 | 90% | 67.1 / 64.9 (never 29%) | 4 | 3 | 3 | 15.0% | 71.7% | 0.225 |
| 20 | 50% | 33.2 / 39.3 (never 0%) | 35 | 7 | 3 | 14.9% | 39.8% | 0.259 |
| 20 | 65% | 46.0 / 50.1 (never 0%) | 7 | 4 | 3 | 15.0% | 51.8% | 0.231 |
| 20 | 90% | 101.2 / 83.8 (never 28%) | 3 | 3 | 3 | 15.0% | 71.7% | 0.189 |

Readings:
1. **Thinner is better for players, up to a point.**
   - 3–5 ETH give the best paybacks and stall days.
   - 3 ETH is the most robust if players sell 90% (steady stalls on day 27 vs 14 at 5 ETH).
   - But 3 ETH amplifies every price move. The day-35 price is 1.3× that of 10 ETH, and the launch is more exposed to snipers and a swarm unlock.
2. **20 ETH breaks the design** at 65% sell intent: steady stalls on day 7.
3. **Sell intent still dominates.** At 90%, every depth fails the hype case and most fail steady. The withdrawal tax lowers the effective sold share to ~72% at 90% intent, which is not enough.

**Recommended IMD launch settings (Robinhood Chain, chain 4663) [I]:**
- `pairWith = eth`.
- `poolBps = 9000`: all of the requester's 90% seeds the pool. `remainderTo` receives nothing, so there are no team tokens.
- **Opening cap 5.6 ETH**: within the live 1–1,000 ETH `customCap` range [F]. With 900 M pooled tokens, this is the 5 ETH virtual reserve.
  - Alternative: 3.3 ETH cap (3 ETH virtual) if the requester prefers robustness to heavy selling over price stability.
- The hook kind is `univ4_hook`, with the BLACKOUT FeeRouter as the "paying wallet".
- **Open question:** whether an IMD hook launch lets a project-defined hook add the progressive sell fee on top of the policy fee. The docs show hook launches but do not say so.
- **Swarm allocation:** BLACKOUT cannot lock the swarm's 10%. Publish the risk. The sell tax also applies to those sells.

Other sensitivity (v2 defaults):

| variant | steady wk1 / wk4 payback d | steady stall | hype wk1 / wk3 payback d | hype stall | weak stall | steady team ETH (% inflow) | hype team ETH (% inflow) | steady day-35 price /1M |
|---|---|---|---|---|---|---|---|---|
| baseline v2 | 27.9 / 36.5 | 34 | 50.8 / 58.8 | 4 | 3 | 13.8 (15.0%) | 21.5 (14.9%) | 0.293 |
| team 0% everywhere (shares to reward) | 22.4 / 25.9 | none | 28.7 / 36.9 | none | 3 | 0.0 (0.0%) | 0.0 (0.0%) | 0.379 |
| team 20% everywhere (max allowed) | 31.9 / 42.2 | 32 | 45.7 / 69.7 | 4 | 3 | 18.1 (20.0%) | 28.4 (20.0%) | 0.267 |
| no behavioural response to taxes | 28.4 / 34.2 | 35 | 49.9 / 68.0 | 4 | 3 | 13.8 (15.0%) | 21.5 (14.9%) | 0.250 |
| withdrawal tax flat 20% (no decay), all claim day 0 | 30.4 / 37.0 | 34 | 54.7 / 59.4 | 4 | 3 | 13.8 (14.9%) | 21.5 (14.9%) | 0.329 |
| sell-tax cap 8% | 27.9 / 36.5 | 34 | 50.8 / 58.8 | 4 | 3 | 13.8 (15.0%) | 21.5 (14.9%) | 0.293 |
| referred share 80% | 27.8 / 36.6 | 33 | 51.4 / 60.7 | 4 | 3 | 13.8 (15.0%) | 21.5 (14.9%) | 0.291 |
| NFT claim rate 10% | 26.7 / 35.6 | 33 | 45.4 / 65.5 | 4 | 3 | 13.7 (15.0%) | 21.3 (14.9%) | 0.289 |
| NFT claim rate 60% | 29.9 / 37.0 | 34 | 49.3 / 62.1 | 4 | 3 | 13.9 (14.9%) | 21.7 (14.9%) | 0.298 |
| lobbying x5 | 25.3 / 29.5 | none | 34.2 / 37.9 | 34 | 3 | 14.6 (14.5%) | 23.0 (14.5%) | 0.348 |
| no external traders | 29.0 / 38.0 | 33 | 52.3 / 63.0 | 4 | 3 | 13.6 (14.9%) | 21.2 (14.9%) | 0.289 |
| external traders 2x pack ETH | 26.6 / 32.5 | 35 | 37.2 / 54.1 | 13 | 3 | 14.4 (15.1%) | 22.9 (15.1%) | 0.307 |
| emission 3.0%/day | 30.1 / 35.5 | 35 | 50.8 / 64.7 | 4 | 3 | 13.4 (15.0%) | 21.2 (14.9%) | 0.301 |
| swarm sells all 10% in 14 d | 29.4 / 35.9 | 34 | 48.5 / 73.8 | 4 | 3 | 13.7 (15.0%) | 21.4 (14.9%) | 0.273 |
| swarm sells nothing | 26.7 / 36.9 | 33 | 31.9 / 44.7 | 31 | 3 | 13.8 (15.0%) | 21.5 (14.9%) | 0.318 |
| churn x2 | 26.1 / 26.6 | none | 34.9 / 34.0 | none | 3 | 13.6 (15.0%) | 20.9 (15.0%) | 0.283 |

Notes:
- **Team share:** at 0% team, steady payback improves by ~6 days and hype never stalls. That is the price of team revenue. At the allowed maximum of 20%, steady stalls on day 32, which still meets the day-28 rule.
- **External traders:** volume helps (2× → hype stall 13), because fees on both legs feed the reward pool.

---

## 7. Updated contract spec (sized for one IMD launch prompt)

Everything in v1 §7 still applies. Additions and changes:

**A. `BlackoutHook` (Uniswap v4 hook; permissions: `afterSwap`, `afterSwapReturnDelta`, `beforeSwap`, `beforeSwapReturnDelta`)**
- Pool: ETH/BLACKOUT.
- The IMD policy fee (1.25%: 1% to the paying wallet = `FeeRouter`, 0.25% to the network) is applied as IMD configures it.
- **Buys** (ETH in, exact-input): no extra fee.
- **Sells** (token → ETH):
  - In `afterSwap`, compute `fee` per §1.2 using the windows *including* this swap and `spot_after`.
  - Take `extra = ethOut · (fee − 1%)` with `poolManager.take(ETH, FeeRouter, extra)` and return it as the unspecified delta. Exact-input sells take it from the ETH output; exact-output sells take it from the token input converted at spot.
  - `require(totalFee ≤ 1500 bps)` is an immutable constant.
- **Whitelist:** `PackSale`, `LobbyBurner` and `FeeRouter` buys pay no extra fee. They also do not count as "buys" in B, so system buybacks cannot be used to wash the imbalance. Note: the sim counted system buys in B, so this rule is stricter than what was simulated.
- State:
  - `uint128[12] sell5m, buy5m` (ring buffer)
  - `uint128[24] sell1h, buy1h`
  - `uint32 lastBucket`
  - `uint16 storedFeeBps`, `uint32 feeTs`
  - TWAP: 30-min ring buffer of `(ts, cumulativePrice)`, 12 slots
- Events: `SellFee(account, ethOut, feeBps, s1hBps, s24hBps, devBps)`.
- Reference facts [F]:
  - Hooks charge their own fees through return deltas plus `poolManager.take`.
  - LP-fee overrides (`OVERRIDE_FEE_FLAG`, max 1,000,000 = 100%) go to LPs and are *not* used here.

**B. `FeeRouter`** (the "paying wallet" in IMD terms)
- Receives the 1% base fee and the sell-tax excess.
- Splits are constants: base 40 burn / 30 reward / 20 team / 10 heartbeat; sell tax 35 / 40 / 15 / 10.
- **`require(teamShare ≤ 2000)` for every stream.**
- Burn and reward portions queue for `executeBuys` (v1 batching rules).
- Burn = transfer to a no-withdraw `BurnVault`, because the IMD token is fixed with plain transfers and no `burn()` [F].

**C. `FarmCore` additions**
- `claim(amount)`:
  - Settle, then consume pending in FIFO daily vintages.
  - `tax = Σ amount_i · wtax(now − day_i)`, sent to `redistribution` and added to the next tick's `E`.
  - Transfer `amount − tax`. Emits `Claimed(a, gross, tax)`.
- `spend(kind, amount)`:
  - Kinds: upgrade, repair, electricity, lobby, tokenPack.
  - Pays from the unclaimed balance with ×1.05 purchasing power and 0 tax.
  - tokenPack is limited to 1 per wallet per day: 70% to `RewardPool`, 30% to `BurnVault`. It mints a normal pack via `PackSale.mintFor`.
- `setReferrer(r)`:
  - Called once, inside the first action.
  - `r ≠ msg.sender` and `r` already has a farm.
  - At settle: `pool.release(r, 5% · gross)` on top.
- Inspection:
  - `submitInspection(farm)` is open during [epochEnd, epochEnd + 24 h]. It keeps the max score.
  - `finalizeInspection()` pays `1% · weekEmission` from the pool.
- `tariff` is set by the heartbeat through `Params`, at most once per 24 h, `|Δ| ≤ 10%`, bounds 0.10–0.30.

**D. `GridOperator` additions**
- `lobby(district) payable`:
  - 85% to `LobbyBurner` (buy & burn), 10% team, 5% heartbeat.
  - `L_d` is stored as `(amount, ts)` and decayed lazily: `L·2^(−Δt/3 d)`.
  - Token lobbying through `spend(lobby)` burns tokens and counts at TWAP value.
- Blackout district:
  - `r = uint256(bhash(arbBlockNumber − 1)) % Σw` over the eligible districts (cooldown).
  - `w_d` as in §1.2, fixed-point 1e4.
  - The swarm still picks only the event type.

**E. `StarterClaim`** (Robinhood Chain)
- `bytes32 immutable root` of `keccak256(abi.encode(tokenId, holder))`, from an Ethereum snapshot at block `snapshotBlock`.
  - The root and the block are set once by the owner before `launchTime`. Both are values only the requester can provide, so they are placeholders in this spec.
- `claim(tokenId, proof)`:
  - Requires `msg.sender == holder` and `!claimed[tokenId]`.
  - Requires `launchTime + 48 h ≤ now < launchTime + 16 d`.
  - Verifies with OpenZeppelin `MerkleProof`.
  - Mints 3 Starter items (rarity table R 92% / E 8%, non-transferable, `starter` flag = 50% hash until `paidPacks[holder] ≥ 1`).
- Seed: same commit/reveal as packs.
- The snapshot ties a claim to the snapshot holder, so later NFT sales do not carry the claim. Say so in the UI.

**F. `PackSale` additions**
- Beta caps computed from `t = now − launchTime`:
  - per wallet, rolling 24 h: `t < 12 h ? 3 : t < 24 h ? 6 : t < 48 h ? 10 : 20`
  - global per hour: `t < 6 h ? 75 : t < 24 h ? 150 : t < 48 h ? 300 : ∞`
- No setter exists.

**Invariants to test (new):**
- `totalSellFee ≤ 15%` for any state.
- A single-swap dump pays the elevated fee.
- `Σ teamShare_stream ≤ 20%`.
- Withdrawal tax plus redistribution conserves tokens.
- A referral cannot be changed or self-assigned.
- Each NFT tokenId claims once; nothing can be claimed outside the window.
- Beta caps are monotone non-decreasing in time.
- Lobby weight is ≥ 0.40.

---

## 8. Risk note for players (publish as-is)

BLACKOUT is a game, not an investment.
- **Where rewards come from:** all token rewards are bought with ETH from other players' packs and from trading fees. As a group, players cannot take out more ETH than they put in. About 15% of all player ETH goes to the team and about 10% to the swarm treasury.
- **Early players earn more than later ones.** In our simulation:
  - With steady growth, packs paid back in about 28 days (week 1) to 37 days (week 4).
  - With fast hype that fades, packs often took 50–60+ days.
  - With weak demand, almost nobody broke even.
- **Taxes:**
  - Claiming rewards to your wallet costs 20%, falling to 5% after 7 days. Spending them in game costs nothing.
  - Selling the token costs 1.25% normally and up to 15% when many people are selling at once. The 15% cap cannot be changed.
- **The swarm:** the IMD swarm holds 10% of the token supply and can sell it. That can push the price down, especially in the first weeks.
- **Events:** grid events, lobbying by other districts and the chain's sequencer can affect your income. Lobbying lowers your blackout odds but never removes them.
- **Free NFT starter packs:** these mine at half speed until you open a paid pack.
- Only spend what you would spend on a game you expect to lose money on.

---

## 9. Facts, inferences, uncertainty, unanswered questions

**Facts [F]:**
- **IMD launch policy:** 1 B fixed supply with plain transfers; swarm 10%; 1.25% fee (1% to the paying wallet, 0.25% to the network); single-sided pool opening at a cap; Robinhood Chain 4663 ETH `customCap` 1–1,000 ETH (live API, 2026-10-10).
- **Identity MD collection:** 1,999 items and ~820 owners (OpenSea, 2026-10-10).
- **Uniswap v4:** hook fees via return deltas and `take`; `MAX_LP_FEE` 1,000,000 = 100%; `OVERRIDE_FEE_FLAG` for LP fees.
- **Airdrop claim rates:** Arbitrum ~63% of tokens claimed in the first days; Anchor 64.4%.
- **Chain and gas:** all v1 chain and gas facts still stand (v1 §11).

**Simulation results [S]:** everything in §3, §4 and §6. They are deterministic and reproducible.

**Inferences [I]:**
- equivalence of virtual ETH and cap × pool share
- the launch recommendation
- that the sell tax is an intraday brake, not a revenue source
- the lower NFT claim rate
- that lobbying is a social sink
- the v1 collective ceiling (players as a group recover at most ~75% of pack ETH), now slightly lower after the 0.25% network fee

**Uncertainty:**
- All behaviour parameters are guesses: sell intent, response to taxes, claim-age mix, referral share, NFT claim rate, lobby spend, trader volume, swarm sell-off.
- The daily model cannot see intraday sell-tax dynamics.
- The stall day is knife-edge in the hype case. Small changes move it by 10+ days (for example 4 vs 7 vs 31 across rows), so read stall days as ranges.
- The 7-day decay projection used for payback is sensitive to the last week's events.

**Unanswered questions for the requester:**
1. Can an IMD `univ4_hook` launch carry this progressive sell fee on top of the policy fee?
2. Opening cap: 5.6 ETH (recommended) or 3.3 ETH?
3. Ethereum snapshot block for the NFT merkle root, and confirmation of the Identity MD contract address.
4. Team and heartbeat treasury addresses. These are owner-settable; no values are guessed here.
5. Is the "Starter" 50%-hash rule acceptable? The alternative is full hash with a lower hype stall day.
6. Will IMD swarm seat holders be asked to lock or vest the 10% swarm allocation?

---

## 10. Not modelled

- Item luck
- Sybils and referral farming
- Intraday price paths (except in the stress test)
- ETH/USD moves
- Gas cost (immaterial per v1 §6)
- Demand uplift from referrals, NFT holders converting to buyers, or lobbying
- Per-wallet beta caps (aggregate demand per player is below the caps)

## 11. Assumptions [A]

- **Carried from v1:** all v1 assumptions §10.
- **Sell behaviour:**
  - Sell intent 65% of free tokens.
  - In-game redirect = 1.5 × average withdrawal tax (cap 60%). Deferral = 1.0 × excess sell fee.
  - Claim-age mix 40/30/30 at 0/3/7 days.
  - Token-pack share of in-game spending 25%.
- **Referrals and NFT packs:**
  - Referred share of hash 40%.
  - NFT claim rate 35%, with 50% of claims in the first 3 days of the window.
- **Other flows:**
  - Lobby 0.00004 ETH per farm per day.
  - External round-trip volume 0.5 × pack ETH.
  - Swarm sells 50% of its 10% over 14 days.
- **Sell-fee inputs:** 1 h imbalance = 1.25 × 24 h imbalance. TWAP deviation = half the day's price drop.
- **Pool:** 900 M tokens in the pool.

## 12. Sources

- Previous accepted report and sim, IMD job b9e37680: https://api.imd.fun/jobs/b9e37680-814c-4f17-b4bc-68272b77304d/result (artifact sha256 dfbd6842…c0b); repo copy `sim/swarm_farm_sim.py`
- IMD docs (launch policy, fee, supply, poolBps, chains), fetched 2026-10-10: https://imd.fun/docs/
- IMD live capabilities API (Robinhood Chain 4663 ETH customCap 1–1000 ETH), fetched 2026-10-10: https://api.imd.fun/requests/capabilities
- Identity MD on OpenSea (1,999 items, 820 owners), fetched 2026-10-10: https://opensea.io/collection/identitymd
- Uniswap v4 `LPFeeLibrary.sol` (DYNAMIC_FEE_FLAG, OVERRIDE_FEE_FLAG, MAX_LP_FEE): https://github.com/Uniswap/v4-core/blob/main/src/libraries/LPFeeLibrary.sol
- Uniswap v4 docs, dynamic fees: https://developers.uniswap.org/docs/protocols/v4/concepts/dynamic-fees
- Uniswap v4 docs, custom accounting (hook fees with return deltas and `poolManager.take`): https://developers.uniswap.org/docs/protocols/v4/guides/custom-accounting
- CoinDesk, Arbitrum airdrop: 37% unclaimed after day one (2023-03-23): https://www.coindesk.com/business/2023/03/23/after-frenzied-arbitrum-airdrop-day-37-of-eligible-wallets-still-havent-claimed-their-arb/
- Anchor airdrop analysis (64.4% claimed): https://amusing-sky-b53.notion.site/Anchor-Airdrop-Analysis-9dca9fe7d5b747d680b802212758d7b7 (secondary)
- Arbitrum docs: blockhash and ArbSys (as in v1): https://docs.arbitrum.io/build-decentralized-apps/arbitrum-vs-ethereum/solidity-support
- OpenZeppelin MerkleProof: https://docs.openzeppelin.com/contracts/5.x/api/utils#MerkleProof (standard library; cited for the API, not fetched in this pass)
