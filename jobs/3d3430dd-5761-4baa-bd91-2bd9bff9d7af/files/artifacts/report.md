# $HIVE (Project Hive): how likely is a $1M FDV, based on on-chain activity?

**Token:** `0xCdaE63D95D6dd4f89f6e508c77bD4388b4e5C8Ab` on **Robinhood Chain** (chain ID 4663, an Arbitrum Orbit L2)
**Data cut-off:** 2026-09-29 ~20:25 UTC (chain head ≈ block 75,940,4xx). The token was about 35 hours old at that point.
**Explorer:** <https://robinhoodchain.blockscout.com/token/0xCdaE63D95D6dd4f89f6e508c77bD4388b4e5C8Ab>
**Market page:** <https://dexscreener.com/robinhood/0x4674f978aab6c373c1634a6729771d9bd6b97bbf25fdfa70d601a81a339f6974>

---

## Answer

> **About a 15% chance of trading at or above $1M FDV within the next 30 days. My plausible range is 8–25%. The chance within 7 days is about 8%.**

This number is a **judgement (an inference)**. It is not a statistical model. Reaching $1M means the price has to rise about **5.8×** from the snapshot FDV of about **$173k**, or about **1.5×** above the all-time high of about **$662k** set roughly 11 hours before the snapshot.

- **Why the number isn't lower:** only a small amount of money is needed to move the price. The pool is thin, and roughly $26k of net buying took FDV from $55k to $662k. There are about 1,700 distinct buyers and 43 stakers who lock up 9.2% of supply.
- **Why the number isn't higher:**
  - Momentum has turned down: the price is −46% over 1 hour and about −74% from the peak.
  - Net buying across the whole life of the pool is close to zero.
  - The protocol's own fee contract holds about 5% of supply and sells it into the pool on a schedule.
  - A 6.5% fee on every trade makes each round trip cost about 13%.
  - Early bonding-curve buyers still hold about 18% of supply and are mostly in profit.

---

## 1. Facts (directly observed; each has a source)

### 1.1 Token and launch
| Item | Value | Source |
|---|---|---|
| Name / symbol / decimals | "Project Hive" / HIVE / 18 | `name()`, `decimals()` eth_call on the token over `https://rpc.mainnet.chain.robinhood.com` |
| Total supply | 1,000,000,000 HIVE (0x033b2e3c9fd0803ce8000000 wei) | `totalSupply()` eth_call |
| Mint | All 1B was minted to `0x27929453…f890` at block 74,688,116 (2026-09-28 ~09:25 UTC) | tx [`0x0ee2b071…5b5e`](https://robinhoodchain.blockscout.com/tx/0x0ee2b07178d2fe9d2548ee057fb665afbf57632bc986851ff343dde2c0975b5e). The tx sender was EOA `0xead2f747…e7a9`, calling `0x7ed598bc…ec7e` |
| Bonding-curve phase | From 09:25 to 15:12 UTC on 09-28, 445 addresses received HIVE from the minter contract `0x2792…` before any Uniswap pool existed | Transfer logs, blocks 74,688,116–74,895,207 |
| Graduation to Uniswap v4 | Block 74,895,208 (2026-09-28 15:11:58 UTC): `0x7ed598…` moved 285.7M HIVE. 204.08M went into the v4 PoolManager and 81.63M went to `0x267444d0…4952`. The pool was initialized with hook `0xe5e70264…e044` and tickSpacing 200 | tx [`0x28e587a2…c85e`](https://robinhoodchain.blockscout.com/tx/0x28e587a2fb8c20f9e574c18c5a1cd7431c2a92252b7d86cab53a1bfaacf4c85e), `Initialize` event on PoolManager `0x8366a39c…0951` |
| Graduation caller | `0x2c2572da…4a49` received 6.26M HIVE in the graduation tx and sold all of it in three equal swaps within about 5 minutes | Transfer logs, blocks 74,898,180 / 74,898,778 / 74,899,378 |
| Project claims (not verified on-chain) | 6.5% fee on every buy and sell, split: 5.5% buys identity.md agent seats, 0.5% team, 0.2% running costs, 0.3% Pons launchpad. Stakers receive the IMD the seats earn. There is a 1×→2× loyalty multiplier over 90 days. The site says "No admin keys" | <https://projecthive.fun/> (fetched 2026-09-29) |

### 1.2 Market snapshot (DexScreener API, 2026-09-29 20:25 UTC)
Saved as `artifacts/data/dexscreener_snapshot_20260929T2025Z.json`. Main pool: HIVE/ETH, Uniswap v4, id `0x4674f978…6974`.

| Metric | Value |
|---|---|
| Price | $0.0001733 |
| FDV (= market cap, because the whole supply is liquid) | **$173,387** |
| Liquidity | **$40.1k** (7.85 ETH + 109.2M HIVE) |
| 24h volume | $479k. 24h txns: 1,559 buys / 1,157 sells |
| Price change | 5m −20%, 1h −46%, 6h −51%, 24h −32% |
| Other pools | 6 small pools (ETH and USDG), each with less than $1k liquidity |

An earlier snapshot at 20:21 UTC showed FDV $217k. That is a −20% move in 4 minutes, which shows how volatile the price is.

### 1.3 Holders (reconstructed from every `Transfer` log: 20,315 events, blocks 72.3M → head)
Full table: `artifacts/data/top100_holders.csv`.

- **776 addresses hold more than 0 HIVE.** 2,181 addresses have ever received HIVE, so about 64% of addresses that ever held HIVE have since exited.
- Only 130 holders have more than 1M HIVE (about $170 at the snapshot price). 18 holders have more than 10M.
- **Protocol and infrastructure holdings** (identified by bytecode, events and selectors):

| Address | HIVE | % supply | What it is |
|---|---|---|---|
| `0x8366a39c…0951` | 110.3M | 11.03% | Uniswap v4 **PoolManager**. This is pool liquidity: it emits `Initialize` and `Swap` for the HIVE pools |
| `0x4a568607…8695` | 92.0M | 9.20% | **Staking contract**. `totalStaked()` = 92,043,469.97. Its bytecode contains `stake(uint256)` / `unstake(uint256)` / `claim()` selectors. **43 unique depositors** |
| `0x267444d0…4952` | 81.6M | 8.16% | Contract that received 81.63M at graduation and has never sent any. `owner()` = Safe `0x263ed295…19dd`. It has an ERC-721 receiver function |
| `0xe5e70264…e044` | 50.6M | 5.06% | **Main-pool v4 hook**, also owned by Safe `0x263ed295…`. It received 132.3M HIVE across 2,776 inflows and sent 81.7M to the PoolManager in 28 outflows |

- **All other addresses** hold 66.5% of supply:
  - Top 10 of these hold 20.7%. Top 25 hold 33.9%.
  - The largest single wallets hold 2.7%, 2.7%, 2.4%, 2.4% and 2.1%.
  - Many large wallets are EIP-7702 delegated EOAs (their code starts with `0xef0100…`).
- **Early holders:** 76 of the 445 bonding-phase recipients still hold HIVE. Together they hold **18.3%** of supply.
- **Size buckets** at $0.000217, all addresses except the four above:

| Holding value | Addresses | % of supply |
|---|---|---|
| < $10 | 305 | 0.4% |
| $10–100 | 254 | 4.4% |
| $100–1k | 184 | 25.8% |
| $1k–5k | 25 | 25.9% |
| > $5k | 4 | 10.2% |

### 1.4 Trading activity (decoded v4 `Swap` events from the three largest pools)
Full hourly table: `artifacts/data/hourly_trading_utc.csv`.

- **7,138 swaps** from graduation to the snapshot (about 29 hours): 3,909 buys and 3,229 sells.
- A buy is a swap where ETH goes into the pool. I checked this sign convention: every one of the 2,821 main-pool swaps of that type that moved the price moved it up.
- **Gross ETH in from buys ≈ $379k. Gross ETH out on sells ≈ $372k. Net inflow over the pool's whole life ≈ +$7.5k.**
- FDV path (main pool; converted with a constant ETH price):

| Time (UTC) | FDV | Note |
|---|---|---|
| 09-28 15:12 | ~$55k | graduation |
| 09-28 22:00 | ~$320k | |
| 09-29 05:00 | ~$615k | busiest hour: $44k of buys |
| 09-29 09:00 | **$662k** | ATH, tx [`0x3b68936a…7003`](https://robinhoodchain.blockscout.com/tx/0x3b68936a827a3d21ddecdc430dcaa5d4b24e1956f7f77566017a49e1b8597003) |
| 09-29 20:22 | **~$167k** | at the cut-off |

- **Since the ATH**, 8 of 11 hours had net selling. The last hour was about $1k of buys against about $10.5k of sells.
- **Hourly activity** has fallen from 300–500 swaps per hour at the peak to about 90–230 per hour.
- **Traders** (heuristic: the final HIVE recipient of each swap tx, or the first sender):
  - about 1,709 distinct buy-side addresses
  - about 1,301 distinct sell-side addresses
  - about 1,172 addresses did both

---

## 2. Inferences (my reasoning from the facts; could be wrong)

1. **Reaching $1M needs little capital, but it needs continued net demand.**
   - At the snapshot the pool held about 7.85 ETH against 109M HIVE, roughly balanced at about $20k per side.
   - If the liquidity behaves roughly like a full-range pool, a 5.8× price move needs about 7.85 × (√5.8 − 1) ≈ **11 ETH (~$30k) of net buying**, or about $32k once the 6.5% fee is included.
   - The pool's own history supports this. About **$26k of cumulative net buying** took FDV from $55k to $662k (12×).
   - So this is a question about demand, not about liquidity.
2. **There is built-in, recurring sell pressure.**
   - The hook keeps part of the fee in HIVE. It has already sold 81.7M HIVE into the pool in 28 tranches. That matches the site's description: fees are converted to buy agent seats.
   - It still holds 50.6M HIVE (about $8.8k at the snapshot price), and it takes in more with every trade.
   - Any rally therefore has to absorb these conversions, as well as profit-taking by the 18% held by early bonding-curve buyers.
3. **The 6.5% fee** makes each round trip cost about 13%. This discourages the fast momentum and bot trading that usually drives small-cap spikes. It also makes arbitrage between the seven pools slower.
4. **Holder quality is mixed.**
   - *Positive:* 9.2% of supply is staked by 43 wallets. Given the 90-day multiplier, these look like longer-horizon holders. No single non-infrastructure wallet holds more than 2.7%.
   - *Negative:* 64% of addresses that ever held HIVE have left. The 776 remaining holders are a small base. About 51% of supply sits in 29 wallets worth $1k or more, so a few exits can move the price 20–40% in minutes, as the snapshot showed.
5. **Momentum.** The ATH was set on a clear volume spike (05:00–09:00 UTC). Since then there has been a lower high and then a sharp drop. The typical pattern for launchpad tokens after a first peak is a long decline. A second, higher peak usually needs a new catalyst, such as a listing, partnership or visible agent-seat purchases. I found no on-chain sign of one yet.
6. **Probability estimate.**
   - I started from a low prior. From general experience, which I have not measured, most launchpad tokens that fail to hold their first-day peak don't later exceed 1.5× that peak.
   - I raised it for the low capital requirement and the staking and fee-to-yield narrative.
   - I lowered it for the fee-contract selling and the current downtrend.
   - Result: **about 15% within 30 days (range 8–25%) and about 8% within 7 days.**

## 3. Uncertainty and caveats
- **USD values** in the hourly data and the FDV path use a single ETH price of ~$2,691, derived from DexScreener's priceUsd/priceNative. ETH moves over 29 hours add error of a few percent.
- **Pool shape:** the capital estimate assumes roughly full-range liquidity. I did not read the v4 position ticks. If the liquidity is concentrated, the capital needed could be meaningfully higher or lower.
- **Trader counts** come from a heuristic that follows transfer chains inside each swap tx. Routers and smart-account wallets could inflate or deflate them.
- **Scope:** swaps were decoded only for the three largest pools. The four others together hold less than $1k of liquidity and were ignored.
- **Labels** for the staking contract, the LP-holding contract and the hook are **inferred** from bytecode selectors, events and flows. None of them has a verified source code label that I could read.
- **Data access:** the Blockscout API was behind a Cloudflare challenge. All holder data was therefore rebuilt from raw RPC logs, not taken from an indexer. Mistakes in log paging would change the holder numbers. Checks done: the first log is the 1B mint, there are no burn transfers, and the PoolManager's 110.3M HIVE is consistent with DexScreener's 109.2M in the main pool plus the small pools. There was no independent holder count to compare against.
- **The probability is subjective** and very sensitive to off-chain factors that I did not measure: social attention, a CEX or aggregator listing, team actions, and the broader market.

## 4. Unanswered questions
1. **Can Safe `0x263ed295…19dd` withdraw the 81.6M HIVE (8.16%) or the LP position** held by `0x267444d0…`? Can it change the hook's fee or its selling behaviour? The owner functions exist, but I did not review their powers. This bears directly on the site's "No admin keys" claim.
2. **When and how does the hook sell its HIVE** (threshold, schedule, price cap)? The site says buying is "price-capped". What that means for sell size is unverified.
3. **Who are the large EIP-7702 wallets?** Several share the same delegate implementations (`0xe6cae83b…`, `0x63c0c19a…`). I did not determine whether they are linked to each other or to the deployer `0xead2f747…`.
4. **Are agent seats actually being bought and earning IMD?** If so, how much yield does that give stakers? This is the fundamental demand driver, and I did not check it on-chain.
5. **Did the price keep falling after the cut-off?** The token was at −20% over 5 minutes at the snapshot, so this report ages within hours.

## 5. Method (reproducible)
1. DexScreener token API: `https://api.dexscreener.com/latest/dex/tokens/0xCdaE63D95D6dd4f89f6e508c77bD4388b4e5C8Ab`.
2. Public RPC `https://rpc.mainnet.chain.robinhood.com`:
   - `eth_getLogs` for ERC-20 `Transfer` on the token, from block 72,324,358 to the head.
   - v4 `Swap` (`0x40e9cecb…`) and `Initialize` (`0xdd466e67…`) on PoolManager `0x8366a39c…0951`, filtered by pool id.
   - `eth_call` / `eth_getCode` for token metadata, contract classification, `owner()` and `totalStaked()`.
3. Scripts: `artifacts/scripts/` (logs.py → hold.py → swaps.py → ana.py → ana2.py → ana3.py). They were run in a scratch directory, and the large intermediate JSON files (about 20 MB of raw logs) are not committed. Re-running the scripts regenerates them. Expect different numbers, because the chain keeps moving.

*This is not financial advice. The probability is an analytical estimate from on-chain data at a single point in time.*
