# SIMD TEST 2 jobs vault — how it works

Contract `0x7dD168b775ffbFaAB154D6bD3fD47c7d600538f6`, Robinhood Chain (4663). Source is unverified. Everything here comes from public RPC `rpc.mainnet.chain.robinhood.com` (bytecode, state, logs) at block ~111156971.

## Facts (on-chain)
- `token()` = `0xc8af…9550`, "SIMD TEST 2 - DO NOT BUY", 18 decimals. `MINIMUM_TOKENS()` = 1,000,000. `minimumHolding()` = 1e24 (1M tokens).
- `vault()` = `0xa9d4…813A`. Only the vault can call `setToken`, and only once (slot 0 must be empty).
- `stake(amount)` pulls tokens and emits `Staked`.
- Selector `0xb44b07eb(bytes)` requests a job. It reverts unless the caller's stake is at least `minimumHolding`, its per-caller cooldown has passed and the body is not empty. It then:
  - reads `priceOf("job.open@job-1", IMD)` from job market `0xa43e…de82`;
  - approves IMD (`0x5f7b…7127`) and calls the market's `request`;
  - resets the approval to 0;
  - sets both `lockedUntil` and the cooldown to now + 86400 (`0x015180`).
- `unstake` reverts while now < `lockedUntil`.
- Observed run: stake of 1e24 by `0xdfa1…8bc0` (tx `0xf727c3a3…`); job (tx `0x048f411a…`) paid 0.5 IMD, which the market forwarded to `0x4e0f…adbc`. `lockedUntil` = 1794428458, which is the job's timestamp + 86400.
- The contract holds 0.1737 IMD (less than one 0.5 IMD job).

## Inferences
- The IMD is paid from **this contract's own IMD balance**, not pulled from `0xa9d4` at job time. The vault (7-day `DISTRIBUTION_INTERVAL`, `distribute()`) probably tops it up.
- Each address gets one job per 24 h. Stake moved to a new address after unlock could get around this.

## Uncertainty / open questions
- Function names for `0xb44b07eb`, `0x40d7533d` and `0xac712640` are unresolved.
- What funds the IMD balance, and how often?
- The job price can change: the market owner sets it via `setPrice`.
- No admin can withdraw IMD from this contract (no withdraw selector found). Not fully traced.
