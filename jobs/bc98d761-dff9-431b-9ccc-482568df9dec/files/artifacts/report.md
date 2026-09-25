# Fren Pet "diehard fans": pets 2+ years old, still alive, still playing

*Snapshot: indexer block 51763861 on Base (chainId 8453), block time 2026-09-25 06:17 UTC. Data source: live Ponder GraphQL `https://api.pet.game/graphql`. `api.frenpet.xyz` was not used.*

## Answer

- **60,379** of 83,955 indexed pets were created on or before 2024-09-25 06:17 UTC, so they are at least 730 days old.
- **753** of those are alive under the primary rule (`status == 0`, HAPPY). Another 34 were indexed as status 1-3 (alive but hungry, starving or dying), and 16 were indexed as the undocumented status 5. Both groups are left out of the ranking. 59,576 are dead (status 4).
- **753** alive pets pass the engagement floor (`fpSpent > 0 OR winQty >= 100 OR level >= 50`). **Every alive 2y+ pet passes it**, so the floor does not separate anyone. I therefore also report a stricter tier.
- **517** are **active diehards**: they pass the floor, have a starvation timer still in the future, and made an attack in the last 30 days. 99 of the top 100 are active diehards.
- These pets belong to only **123** distinct owner addresses (the top 100 belong to 52). A few wallets run many pets each (see [Owner concentration](#owner-concentration)). Counted by people, there are far fewer diehards than the pet count suggests.
- On-chain cross-check at Base block 51765491: every one of the 753 listed pets returned `isPetAlive == true` from the FrenPet diamond. All-listed-alive = `True`.

## Data provenance

| Item | Value |
|---|---|
| GraphQL endpoint | `https://api.pet.game/graphql` (Ponder) |
| `_meta` block | 51763861 @ 1790317069 (2026-09-25 06:17 UTC) |
| Fetch wall clock | 1790317070 → indexer lag ≈ **1s** |
| `asOfUnix` | 1790317069 (= `_meta` block timestamp) |
| Age cutoff | `createdAt <= 1727245069` (2024-09-25 06:17 UTC), i.e. asOf − 63,072,000 s |
| Completeness | Paginated `pets(where:{createdAt_lte}, limit:1000, after)` in id order and got 60,379 rows, equal to the server `totalCount`. The per-status `totalCount` queries sum to the same number (0: 753, 1: 5, 2: 9, 3: 20, 4: 59,576, 5: 16, 6: 0, 7: 0) |
| Relation counts | `attacks` (attackerId / targetId), `consumeds`, `gachas`, `wheelSpins`, `redeems` by petId, all-time and `createdAt_gte = asOf−30d`, from `totalCount` for every pet with indexed status 0-3 |
| On-chain check | `getStatus(uint256)` and `isPetAlive(uint256)` on diamond [`0x0e22b5f3e11944578b37ed04f5312dfc246f443c`](https://basescan.org/address/0x0e22b5f3e11944578b37ed04f5312dfc246f443c) at block 51765491 (2026-09-25 07:12 UTC) via `https://base-rpc.publicnode.com`, for all 803 pets with indexed status ≠ 4 |

## Status legend (with evidence)

FrenPet's docs list the V2 diamond at `0x0e22b5f3e11944578b37ed04f5312dfc246f443c` ([docs.frenpet.xyz/contracts](https://docs.frenpet.xyz/contracts/)). A verified facet build on Sourcify ([`0x47f634e78b1af81c0494763f18620e5ca3d7ad0a`](https://sourcify.dev/server/v2/contract/8453/0x47f634e78b1af81c0494763f18620e5ca3d7ad0a?fields=sources), `src/facets/FrenPetFacet.sol` lines 65-113) defines `getStatus()` through a commented enum `HAPPY, HUNGRY, STARVING, DYING, DEAD`. It returns 4 when `isPetAlive()` is false, meaning `timeUntilStarving == 0 || timeUntilStarving < block.timestamp`. Otherwise it picks 0-3 from the hours left until starving: more than 16, 12-16, 8-12, or under 8.

| status | meaning | 2y+ count |
|---|---|---|
| 0 | HAPPY - alive, >16h until starving (contract getStatus) | 753 |
| 1 | HUNGRY - alive, 12-16h until starving (contract getStatus) | 5 |
| 2 | STARVING - alive, 8-12h until starving (contract getStatus) | 9 |
| 3 | DYING - alive, <8h until starving (contract getStatus) | 20 |
| 4 | DEAD - isPetAlive()==false (timeUntilStarving passed); burned pets show owner 0x0 | 59,576 |
| 5 | UNDOCUMENTED - returned by the live (unverified) getStatus facet, absent from verified source; isPetAlive() is true, meaning unknown; excluded from alive | 16 |

**Contradiction found.** The diamond currently routes `getStatus`, `isPetAlive` and `getPetInfo` to facet [`0xe819c3445f505d2b8f47b8cc91d4a40b29ea4994`](https://basescan.org/address/0xe819c3445f505d2b8f47b8cc91d4a40b29ea4994) (checked with `facetAddress(bytes4)`). That facet is **not verified** on Sourcify or Blockscout, and it returns **5** for some pets (for example #450 and #29138) while also returning `isPetAlive == true`. Status 5 is not in the verified source, so its meaning is **unknown**. The 16 indexed status-5 pets all have `timeUntilStarving` 97-166 h ahead, which is beyond the documented 3-day feeding timer ([docs gameplay](https://docs.frenpet.xyz/gameplay/)). That suggests some special protected or paused state, but this is an inference and nothing documents it. Per the task, only status 0 counts as alive for ranking. Status 1-3 and 5 pets are listed separately in the JSON.

Every status-4 pet in the 2y+ set has owner `0x0` (0 have a non-zero owner). This fits the docs statement that dead pets are burned.

### Indexed status vs. live on-chain status

The indexer's `status` is recorded when an event touches the pet. The contract computes it from `block.timestamp` at call time. They therefore drift apart:

| indexed → on-chain getStatus (isPetAlive) | pets |
|---|---|
| 0->0 (alive=True) | 749 |
| 0->1 (alive=True) | 4 |
| 1->0 (alive=True) | 3 |
| 1->1 (alive=True) | 1 |
| 1->2 (alive=True) | 1 |
| 2->0 (alive=True) | 5 |
| 2->2 (alive=True) | 4 |
| 3->0 (alive=True) | 14 |
| 3->5 (alive=True) | 6 |
| 5->5 (alive=True) | 16 |

So 753 indexed-status-0 pets are all alive on-chain. The strict status-0 rule leaves out some pets that are alive on-chain (for example indexed 3 → on-chain 0 after being fed). A rule based only on `timeUntilStarving > asOf` would add 34 status 1-3 pets and 16 status 5 pets.

## Definitions used

1. **Age**: `createdAt <= cutoffUnix`, with `ageDays = (asOf − createdAt)/86400`. Alive 2y+ pets are 736.0-1050.2 days old (median 903.0).
2. **Alive**: `status == 0` (primary, as specified). Status 4 is never counted as alive.
3. **Still cared for**, reported as two separate filters:
   - `fedOk`: timeUntilStarving > asOfUnix → **753 / 753**
   - `attackedWithin30d`: lastAttackUsed >= 1787725069 (asOf - 30d) → **517 / 753**
   - both: 517; either: 753. Cross-checks: 517 alive pets have at least one indexed `attacks` event as attacker in the last 30 days, which matches the `lastAttackUsed` count. 420 have `oldestRelevantBonkTimer` within 30 days.
4. **Engagement floor**: `fpSpent > 0 OR winQty >= 100 OR level >= 50`. Among alive pets: fpSpent>0: 744, winQty≥100: 753, level≥50: 155.
   **Diehard** = alive ∧ 2y+ ∧ floor. **Active diehard** = diehard ∧ fedOk ∧ attackedWithin30d.
5. **Diehard score**: each component is log1p-transformed, then z-scored over all alive 2y+ pets (population SD). The score is the weighted sum of those z-scores.

| component | transform | weight | mean | sd |
|---|---|---|---|---|
| spend | `log1p(fpSpent/1e18)` | 0.3 | 4.726 | 0.663 |
| combat | `log1p(winQty+lossQty)` | 0.25 | 8.893 | 0.510 |
| level | `log1p(level)` | 0.2 | 3.648 | 0.676 |
| recent | `log1p(attacks made, createdAt >= asOf-30d)` | 0.15 | 3.453 | 2.720 |
| redeem | `log1p(totalRedeemFP/1e18)` | 0.1 | 2.647 | 1.755 |

Rationale: spending (FP) is the clearest sign of commitment. Combat volume and level reflect cumulative play. Attacks in the last 30 days reward continuing activity over past activity. Redeemed FP gets a small weight. `score` is left out because level is derived from it (`level = f(sqrt(score))` in the verified source). `petWins` is left out because it is nearly collinear with `winQty`. The weights are a judgement call. All component values are in the CSV, so the ranking can be recomputed with other weights.

## Counts

| population | pets |
|---|---|
| all indexed pets | 83,955 |
| 2y+ (createdAt ≤ cutoff) | 60,379 |
| 2y+ dead (status 4) | 59,576 |
| 2y+ alive (status 0) | 753 |
| 2y+ status 1-3 (alive on-chain, excluded) | 34 |
| 2y+ status 5 (undocumented, excluded) | 16 |
| diehards (alive + floor) | 753 |
| active diehards (+ fed + attacked ≤30d) | 517 |
| distinct owners of diehards | 123 |

## Top 25 diehards

`fpSpent` is shown in FP (wei / 1e18); the exact wei strings are in the JSON and CSV. `atk30d` counts indexed attacks made in the last 30 days. Owners are shortened here; full addresses are in the JSON and CSV.

| # | id | name | owner | ageDays | level | fpSpent (FP) | wins / losses | lastAttackUsed (UTC) | atk30d | score |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | Imagine✨️ | `0xc2Cd6C…0CC2` | 1050.2 | 298 | 14,590.6 | 15,206 / 7,149 | 2026-09-25 05:52:07 | 986 | 3.925 |
| 2 | 15907 | kitty | `0x6bA9aD…742a` | 941.3 | 339 | 4,040.7 | 9,890 / 2,794 | 2026-09-25 05:20:11 | 706 | 2.874 |
| 3 | 13670 | Lefty | `0xe6e077…cD67` | 1030.2 | 225 | 301.1 | 12,951 / 4,256 | 2026-09-25 06:16:13 | 938 | 1.867 |
| 4 | 13677 | Bully | `0xe6e077…cD67` | 1030.2 | 317 | 566.6 | 14,028 / 3,846 | 2026-09-25 06:16:13 | 940 | 1.832 |
| 5 | 15161 | Luckyshot27 | `0xbC8eD3…3488` | 969.6 | 91 | 803.2 | 12,550 / 8,728 | 2026-09-25 06:00:07 | 958 | 1.710 |
| 6 | 0 | #0 | `0x29ed68…a2ca` | 1050.2 | 468 | 109.0 | 15,675 / 5,186 | 2026-09-25 05:54:11 | 863 | 1.702 |
| 7 | 13678 | Scruffy | `0xe6e077…cD67` | 1030.2 | 239 | 190.6 | 13,016 / 4,433 | 2026-09-25 06:12:11 | 935 | 1.690 |
| 8 | 13680 | Lucky | `0xe6e077…cD67` | 1030.2 | 212 | 211.8 | 12,369 / 4,904 | 2026-09-25 04:12:11 | 962 | 1.640 |
| 9 | 13668 | Shorty | `0xe6e077…cD67` | 1030.2 | 196 | 206.0 | 12,190 / 4,661 | 2026-09-25 06:12:11 | 954 | 1.585 |
| 10 | 33566 | SeaSmoke | `0xd8500d…E02d` | 892.8 | 303 | 122.8 | 16,191 / 5,735 | 2026-09-25 06:11:45 | 853 | 1.509 |
| 11 | 8355 | Scrappy | `0xe6e077…cD67` | 1038.2 | 154 | 169.3 | 12,084 / 5,461 | 2026-09-25 06:14:11 | 953 | 1.495 |
| 12 | 13672 | Fluffy | `0xe6e077…cD67` | 1030.2 | 177 | 174.9 | 12,426 / 5,598 | 2026-09-25 03:14:11 | 943 | 1.476 |
| 13 | 15770 | sylvester | `0xd8500d…E02d` | 941.3 | 345 | 120.9 | 12,804 / 5,772 | 2026-09-25 05:12:39 | 850 | 1.474 |
| 14 | 18594 | Froomy 👨🏻‍🌾 | `0xe6e077…cD67` | 917.5 | 687 | 138.4 | 15,975 / 3,618 | 2026-09-25 06:16:13 | 946 | 1.471 |
| 15 | 24466 | Naruto | `0xbF60b8…F6d0` | 901.0 | 61 | 321.1 | 9,763 / 9,892 | 2026-09-25 05:22:11 | 689 | 1.468 |
| 16 | 11966 | SuperPleb | `0xd5DEfa…bb14` | 1037.2 | 144 | 109.1 | 11,589 / 5,916 | 2026-09-25 06:00:07 | 988 | 1.442 |
| 17 | 13667 | Frisky | `0xe6e077…cD67` | 1030.2 | 249 | 248.0 | 13,029 / 4,455 | 2026-09-25 05:52:07 | 947 | 1.378 |
| 18 | 73 | Rhynotic | `0xdE62c9…1a4E` | 1048.6 | 124 | 109.0 | 16,847 / 7,202 | 2026-09-24 15:28:13 | 947 | 1.332 |
| 19 | 13675 | Shaggy | `0xe6e077…cD67` | 1030.2 | 242 | 224.1 | 13,124 / 3,921 | 2026-09-25 06:00:07 | 961 | 1.312 |
| 20 | 13201 | hop0x | `0x68596C…B04B` | 1033.6 | 39 | 1,331.3 | 3,922 / 6,226 | 2026-09-25 06:02:11 | 694 | 1.311 |
| 21 | 13669 | Scooby | `0xe6e077…cD67` | 1030.2 | 233 | 181.1 | 13,741 / 5,678 | 2026-09-25 06:06:07 | 963 | 1.269 |
| 22 | 16306 | khaly0x_pet | `0x682294…F88D` | 941.3 | 33 | 1,329.8 | 3,587 / 6,182 | 2026-09-25 02:17:37 | 874 | 1.256 |
| 23 | 10558 | 🐕 Hachikō 🐕 | `0x25b85b…743a` | 1038.0 | 79 | 105.6 | 11,574 / 11,063 | 2026-09-25 06:04:11 | 984 | 1.199 |
| 24 | 15600 | Buddy | `0xe6e077…cD67` | 941.3 | 268 | 137.8 | 13,185 / 3,672 | 2026-09-25 05:56:11 | 961 | 1.118 |
| 25 | 23878 | Minato | `0xE7b27B…e098` | 902.8 | 120 | 115.9 | 8,821 / 9,196 | 2026-09-25 05:58:11 | 371 | 1.118 |

The full top 100 is in `FRENPET_DIEHARDS.json` → `top100`. All 753 alive 2y+ pets, with rank, component metrics and on-chain status, are in `FRENPET_DIEHARDS_alive.csv`.

## Owner concentration

| owner | diehard pets |
|---|---|
| `0x5b92d2b38ab372bff63f55113b98253adff62a74` | 107 |
| `0x040ba8d0e4870ac54e4560e18b2666e3bf0b055c` | 77 |
| `0xa3c1b8a95b937e78f8d6fb1d68a58c443946c795` | 75 |
| `0x74923fb137df52e0ac792772a34fc16817a17d40` | 41 |
| `0x2ecfe09e12d339710db74320ca74b70c3a2b41f2` | 40 |
| `0x29ed6881cb6698bffbf24bb3b8b3f20a8c51a2ca` | 30 |
| `0x5c9c892f1bf5a3763016952a1d6187bf5a13e65b` | 30 |
| `0x30e49549da679ec277301ffe4e66ac76aa1cc413` | 20 |
| `0x3239c9b3f8f584ef84c5defda7e3d88a64d05221` | 19 |
| `0x99ea608e28d1a13329d138b21cb67c7ed8b4302a` | 19 |

One wallet holding dozens of long-lived pets, together with near-identical `fpSpent` (297 of 753 alive pets are between 109.0 and 109.1 FP), points to automated or batch-managed play rather than one fan per pet. This is an **inference** from the data pattern. Nothing here identifies bots.

## Facts, inferences, uncertainty

**Facts** (read directly from the API or the chain at the stated block):
- The counts above, the status histogram (confirmed twice: page scan and per-status `totalCount`), and every listed pet's `createdAt ≤ cutoff` and indexed `status == 0` (the analyzer asserts these).
- On-chain `isPetAlive == true` for all 753 listed pets at block 51765491.
- The verified facet source defines statuses 0-4. The live facet is unverified and also returns 5.

**Inferences**:
- Status 5 is some special live state (possibly protected or paused) because those pets are alive with timers beyond 72 h. Its meaning is not established.
- `winQty + lossQty` is larger than `attacksMade` for 753 of 753 alive pets. This suggests `winQty`/`lossQty` include defensive outcomes (when the pet is bonked), so the combat component mixes offensive and defensive activity.
- Owner concentration suggests multi-pet operators, possibly automated.

**Uncertainty and caveats**:
- The "alive" rule uses the **indexed** status. That is a snapshot from the pet's last event, not a live value. A few pets drift between buckets within hours (see the drift table).
- The score weights are subjective. Rankings in the middle of the list are sensitive to them; the top handful stand out on every component.
- `fpSpent` and the other aggregates are computed by the Ponder indexer. They were not reconciled against raw FP token transfers.
- Relation counts use `totalCount` on filtered queries. Their completeness depends on the indexer.
- The data is a single snapshot. Rerun the scripts to refresh it.

**Unanswered**:
- The official meaning of status 5, and whether those pets should count as "alive" diehards.
- Whether the multi-pet owners are human fans or bots.
- The history of `fpSpent` over time. The API exposes only a cumulative value, so "sustained" spending over two years cannot be separated from an early burst without event-level spend data.

## Reproduce

```bash
python3 scripts/frenpet_diehards/fetch.py snapshot.json          # ~5 min, live GraphQL
python3 scripts/frenpet_diehards/verify_onchain.py snapshot.json onchain.json  # ~2 min, Base RPC
python3 scripts/frenpet_diehards/analyze.py snapshot.json artifacts onchain.json
python3 scripts/frenpet_diehards/report.py artifacts
```
