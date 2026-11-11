# SIMD TEST 3 vault set: how it works (Robinhood Chain, 4663)

Source: read-only JSON-RPC calls on chain 4663 at block 111,297,819 (ts 1794357088). There was no verified source, so names come from 4byte/openchain selector lookups.

## Facts (on chain)
- Both contracts' `NOTICE()`: *"TEST ONLY. SIMD TEST 3 vault set. Not the real SIMD. Do not buy."* Stake token `0x583c…cc46` ("SIMDTEST3"). Reward token `IMD()` = `0x5f7b…7127` ("Identity.md").
- **StakeRewards** `0xDD1D…7F7A`: `DURATION()` = 604800 (7 days). JobsVault `minimumStake()` = 1e24 (1,000,000 tokens). `totalStaked` = 1e24 from one staker, `0xdfa1…8bc0` (tx `0xb262a8d2…`).
- **Vault** `0x8fe1…ff21`: `distribute()` (tx `0xaf7d19a0…`) split 1.95 IMD: 0.78 to StakeRewards, 0.50154 to JobsVault, and 0.33423 each to DEV and MARKETING (both `0xdfa1…`). StakeRewards then set `rewardRate` × 7 days = 0.78 IMD, with `periodFinish` = 1794961758.
- **JobsVault** `0x6672…7C7F`: `COOLDOWN()` = 86400. Job tx `0x2d597dbe…` emitted `Locked(user, 1794443380)`, which is the job time + 86400. The same tx moved 0.5 IMD **from JobsVault's own balance** to `0x4e0f…adbc`, using an approval to `INTAKE()` `0xa43e…de82`. The user sent no IMD.
- Simulations (eth_call): `withdraw`/`exit` revert with `StakeLocked(1794443380)`, but `claim()` succeeds. Calling the job again reverts with `TooSoon(1794443380)`. A non-staker gets `InsufficientStake()`. Any caller other than JobsVault gets an error when it calls `lock()`.

## Inferences
- The weekly IMD comes from the vault's `distribute()` and is streamed linearly over 7 days, Synthetix-style.
- "Paid in IMD" means JobsVault pays the job price out of its vault-funded IMD. The job fails if that balance (now 0.00154 IMD) is below the price.

## Uncertain / unanswered
- Where the vault gets its IMD (the receipt suggests pool fees from position #3195) and how the split ratios are set.
- What `0x74a38b6a()` = 1,000,000 means, and how `priceOf` is set.
