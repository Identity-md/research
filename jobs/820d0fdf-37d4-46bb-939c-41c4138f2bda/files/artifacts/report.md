# Security review: UpToken, EmissionVault, BatchPay

**Code reviewed:** bundle `1bd4969b…4859`, commit `9bf1b6b4bab490543e8f41bd8dbc68a860d97269` (branch `imd-submission`).
**Files in scope:**

| File | sha256 |
| --- | --- |
| `src/UpToken.sol` | `05aec06fca260fd87592724fe6d710e1eb4543e5958a3f7811b80bec02528e79` |
| `src/EmissionVault.sol` | `5d693748bd4b960b2a62b2e1f8f861d3096ced3ed5d6d9ebecc9cf82c3943c02` |
| `src/BatchPay.sol` | `cb78308ee18caae8312f47f2e9dfeb77b5338d2e6af5ff97ab1d237682bd3b9b` |

`src/UpHook.sol` and `src/HookFlags.sol` were not reviewed, as requested. I read `script/Deploy.s.sol` and `README.md` only to learn how the in-scope contracts are deployed. I did not review them.

**How claims are marked**

- **[FACT-code]**: read directly from the cited line.
- **[FACT-test]**: reproduced by a Foundry test that I wrote and ran (forge 1.8.3, solc 0.8.30, `via_ir`, optimizer 200, the repo's `foundry.toml`). The harness is in `artifacts/Audit.t.sol` and has 18 tests, all passing. Fuzz tests ran 2000 times each.
- **[INFERENCE]**: reasoning from code or documentation that I did not execute.
- **[UNVERIFIED]**: not established. The reason is given.

Line numbers are relative to each file.

---

## Summary

| # | Severity | Title | Location |
| --- | --- | --- | --- |
| M-1 | Medium | `startTime` is not validated. A backdated start vests up to ~684M UP at deployment. | `EmissionVault.sol:21-25` |
| M-2 | Medium | A compromised distributor can take the whole vested-but-unreleased backlog in one call. 94% of lifetime emissions vest in year one. | `EmissionVault.sol:52-57` |
| L-1 | Low | "BatchPay holds no funds between calls" can be broken by anyone sending tokens to it directly. Those tokens can never be recovered. | `BatchPay.sol:15-30` |
| L-2 | Low | A token that charges a fee only on the outbound leg short-pays recipients without reverting. | `BatchPay.sol:26-29` |
| I-1 | Info | About 16M UP stay in the vault forever: the halving series sums to 683,999,999.99…9974 UP. | `EmissionVault.sol:29,39-43` |
| I-2 | Info | The halving shift is exact for 24 halvings, rounds down after that, reaches 0 at halving 82, and never reverts. | `EmissionVault.sol:29` |
| I-3 | Info | Epoch boundaries depend on the L2 sequencer's `block.timestamp`. On Arbitrum Nitro it may run up to 1 h ahead. | `EmissionVault.sol:35-36` |
| I-4 | Info | `release` accepts recipients where tokens get stuck, such as the token contract or BatchPay. | `EmissionVault.sol:54` |
| I-5 | Info | Nothing on-chain links `UpToken` to an `EmissionVault`. The 70/30 split is only as good as the constructor argument. | `UpToken.sol:19-22` |
| I-6 | Info | 400 recipients use about 10.8M execution gas. One reverting recipient blocks the whole batch. | `BatchPay.sol:18-28` |

No critical or high findings. I found no call sequence that mints, pulls from a third party's approval, or releases more than the schedule allows **once `startTime` is set correctly**.

---

## Invariant verdicts

### Invariant 1: fixed supply of 1e27, split 700M/300M, no mint, no admin. **Holds in code, with one deployment caveat (I-5).**

- [FACT-code] `totalSupply` is a `constant` (`UpToken.sol:9`), so no code can change it.
- [FACT-code] Balances are credited in exactly two places:
  - the constructor (`UpToken.sol:21-22`: `700_000_000e18 + 300_000_000e18 = 1e27`);
  - `_transfer` (`UpToken.sol:48-52`), which subtracts `amount` from `from` and adds the same `amount` to `to`.

  The contract has no other function that writes `balanceOf`. The pragma is `^0.8.26` and the files contain no `unchecked` blocks, so overflow and underflow revert. The sum of balances therefore stays at 1e27.
- [FACT-code] The contract has no owner, pause, blacklist, `delegatecall`, `assembly`, `selfdestruct` or proxy. Its only functions are `approve`, `transfer`, `transferFrom` and the constant getters.
- [FACT-test] `test_supplyConservedIncludingSelfTransferAndZero`: self-transfers and transfers to `address(0)` keep the sum of balances equal to `totalSupply`. Tokens sent to `address(0)` stay counted in `totalSupply`, as the NatSpec on line 4 documents.
- Caveat: the constructor writes 700M to whatever `vault` address it is given. See I-5.

### Invariant 2: schedule-only release, distributor only, no other exit. **Holds in code if `startTime` is correct (see M-1).**

- [FACT-code] Only `release` moves tokens out (`EmissionVault.sol:52-59`). The contract has no `approve`, sweep, `receive`/`fallback`, setter or upgrade path. `token`, `distributor` and `startTime` are `immutable` (lines 10-12). `EPOCH` and `HALVING_PERIOD` are `constant` (lines 13-14).
- [FACT-code] Line 53 reverts unless `msg.sender == distributor`. [FACT-test] `test_onlyDistributor` fuzzes the caller 2000 times.
- [FACT-code] Line 55 requires `amount <= cumulativeBudget() - totalReleased`, and line 56 adds `amount` to `totalReleased` before the transfer on line 57. So `totalReleased <= cumulativeBudget()` after every call.
  - [INFERENCE] `cumulativeBudget` never decreases as time advances, and Arbitrum timestamps are monotonic ([Arbitrum docs](https://docs.arbitrum.io/build-decentralized-apps/arbitrum-vs-ethereum/block-numbers-and-time)). Given both, the subtraction on lines 47 and 55 cannot underflow.
  - Reentrancy from the token cannot bypass this, because state is updated before the transfer. UP also has no transfer hooks.
- [FACT-test] `cumulativeBudget()` equals `Σ_{e < epochs} epochBudget(e)` computed naively. `testFuzz_cumulativeMatchesReference` checked this for every `dt` in `[0, 2^32)` seconds, which is about 136 years and 552 halving groups, well past saturation.
- [FACT-test] `test_boundaries`:
  - `t < startTime` gives 0.
  - `t == startTime` gives 0.
  - `t == startTime + 1 day - 1` gives 0, and a release of 1 wei reverts with `ScheduleExceeded`.
  - `t == startTime + 1 day` gives 3,800,000e18.

  "Elapsed" therefore means *completed* epochs, which matches the NatSpec on line 32.

### Invariant 3: BatchPay holds no funds, has no owner, and reverts on a length mismatch. **The length and owner parts hold. "Holds no funds" is only true for funds that pass through `pay` (see L-1).**

- [FACT-code] Line 16 reverts with `LengthMismatch` when `to.length != amount.length`. The existing test `test_mismatchedLengthsRevertWithoutMovingFunds` covers this.
- [FACT-code] BatchPay has no owner or admin. The only state is OpenZeppelin v5.1 `ReentrancyGuard`'s status slot.
- [FACT-code] For honest tokens, line 29 enforces that BatchPay's balance after `pay` equals its balance before `pay`, so `pay` never leaves value behind. [FACT-test] `test_batch_donationStuck` shows that a plain `transfer` to BatchPay leaves it holding tokens.

---

## Findings

### M-1: `startTime` is not validated, so a backdated start vests almost everything at deployment. Medium.

**Where:** `src/EmissionVault.sol:21-25` (the constructor stores `startTime_` without checking it).

**Why it matters:** combined with the compromised-distributor assumption, one bad deployment argument lets the distributor withdraw ~684M UP in one transaction instead of over 20 years.

**Evidence:**
- [FACT-test] `test_backdatedStartVestsImmediately` deploys with `startTime = 0` and sets `block.timestamp = 1_800_000_000`. `cumulativeBudget()` then returns `683999999999999999999997480`, the whole lifetime budget, immediately.
- [FACT-test] `test_futureStartForever` shows that `startTime = type(uint256).max` locks everything permanently.
- [INFERENCE] `script/Deploy.s.sol:58` rejects `startTime < block.timestamp`, but only in the script at simulation time. That is off-chain tooling and does not protect any other deployer. The on-chain contract provides no guarantee.

**Fix:** in the constructor, add:

```solidity
if (startTime_ < block.timestamp || startTime_ > block.timestamp + 30 days) revert InvalidStart();
```

Pick an upper bound that fits the launch plan.

### M-2: a compromised distributor takes the entire unreleased backlog at once. Medium, a design risk under the stated threat model.

**Where:** `src/EmissionVault.sol:52-57`. `release` checks only the cumulative cap. It has no per-call or per-period limit and no recipient restriction.

**Why it matters:** the schedule is front-loaded, so a key compromise after even a few months of unreleased emissions hands the attacker most of the 700M.

**Evidence:**
- [FACT-test] `test_compromisedDistributorBacklog`: if nothing is released for 365 days, one `release(attacker, 642_437_500e18)` succeeds. That is 93.9% of lifetime emissions. The next 1-wei release reverts.
- [INFERENCE] Even with daily releases, the distributor normally receives the tokens itself before using BatchPay (README: "release and batch payment are separate transactions"). A compromised key can therefore also take whatever it holds between those two steps.
- This does **not** break invariant 2. Nothing is released early. The risk is how much is exposed.

**Fix:** any of the following, strongest first:
1. Deploy `distributor` as a multisig or timelock contract, not an EOA. It is immutable, so this must be decided before deployment.
2. Cap each release, e.g. `amount <= epochBudget(currentEpoch) * K` per `EPOCH`, so a stolen key yields at most K days of emissions per day.
3. Fix the recipient to an immutable distribution contract, such as a Merkle distributor.

### L-1: donations break "BatchPay holds no funds" and cannot be recovered. Low.

**Where:** `src/BatchPay.sol:15-30`. The contract has no withdrawal path by design.

**Why it matters:** a plain `transfer` to BatchPay, or a `release(to = BatchPay)` from the vault (see I-4), leaves tokens there permanently. Off-chain monitoring that asserts a BatchPay balance of 0 will fire.

**Evidence:**
- [FACT-test] `test_batch_donationStuck`.
- [FACT-code] Line 29 compares against `beforeBalance`, not zero, so donated tokens cannot be taken by later callers. The existing test `test_selfRecipientRejectedAndAccidentalDepositsCannotBeStolen` confirms this.

**Fix:** restate the invariant as "retains no funds from `pay`". Adding a sweep would contradict "no owner", so do not add one. If the balance must be literally zero, have `pay` require `beforeBalance == 0`. Note that anyone could then block `pay` for a token by donating 1 wei of it, so documenting the limitation is the better option.

### L-2: an outbound-only fee token silently short-pays recipients. Low.

**Where:** `src/BatchPay.sol:26-29`. Only BatchPay's own balance is checked, never the recipients'.

**Why it matters:** payees can receive less than `amount[i]` while `pay` succeeds. The NatSpec says fee-on-transfer tokens are "unsupported", but the code only rejects some of them.

**Evidence:**
- [FACT-test] `test_batch_outboundOnlyFeeNotDetected`: a token that charges 1% only when the sender is a contract. The inbound pull is fee-free, so line 25 passes. The recipient gets 99e18 of 100e18, BatchPay ends at 0, so line 29 passes, and the call succeeds.
- [FACT-test] `test_batch_feeOnTransferRejected`: an ordinary fee-on-transfer token (fee on every transfer) reverts at line 25 with `UnsupportedToken`, as intended.
- [INFERENCE] A token that charges the sender an extra fee on the outbound leg makes line 29 revert, so it cannot drain donated balances.
- UP has no fees, so this does not affect UP.

**Fix:** for guaranteed delivery, record `balanceOf(to[i])` before and after each transfer and require a delta of `amount[i]`. That costs about 2 extra `balanceOf` calls per recipient. Otherwise, reword the NatSpec to say "recipient-side fees are not detected".

### I-1: about 16M UP are permanently locked in the vault. Informational.

**Where:** `EmissionVault.sol:29`, `39-43`.

**Evidence:**
- [FACT-test] `test_lifetimeSumAndLockedRemainder` gives:
  - lifetime `cumulativeBudget() = 683,999,999,999,999,999,999,997,480` wei;
  - `700M − lifetime = 16,000,000,000,000,000,000,002,520` wei (≈ 16.0M UP, 2.29%).
- After a full release, `releasable() == 0` and any further release reverts.
- [INFERENCE] Any UP sent to the vault later, such as hook fee shares or deploy dust, adds to the locked balance because the budget ignores the balance. The README acknowledges this.

**Fix:** none needed if intended. Otherwise publish "≈684M distributable" instead of "70% distributed".

### I-2: halving-shift truncation, behaviour after 20+ halvings, and reverts. Informational. Nothing breaks.

**Where:** `EmissionVault.sol:29`: `3_800_000e18 >> (epoch / 90)`.

**Evidence:**
- [FACT-code] `3.8e24 = 2^24 · 19 · 5^23`, so the first 24 halvings are exact. [FACT-test] `3.8e24 % 2^24 == 0` and `% 2^25 != 0`.
- [FACT-test] Budgets at selected halvings:
  - after 20 halvings: `3,623,962,402,343,750,000` wei per day (exact);
  - after 24 halvings: `226,497,650,146,484,375`;
  - after 25 halvings: `113,248,825,073,242,187` (first floor);
  - after 81 halvings: `1` wei;
  - after 82 halvings (epoch ≥ 7380, ≈ 20.2 years): `0`.
- [FACT-test] `epochBudget(type(uint256).max) == 0` with no revert. `testFuzz_epochBudgetNeverReverts` ran over the full `uint256` range. EVM `SHR` by ≥ 256 returns 0.
- [FACT-code] The only divisors are the constants `EPOCH` and `90`, so division by zero is impossible.
- [FACT-code] The loop on line 39 ends when `rate == 0`, so it runs at most 82 iterations. [FACT-test] That costs 22,094 gas at `block.timestamp = type(uint256).max`.
- [FACT-code] `rate >>= 1` applied repeatedly equals `B0 >> i`, because floor(floor(x/2)/2) = floor(x/4). The fuzz test agrees.
- Rounding always goes down, which favours the vault.

**Fix:** none.

### I-3: the sequencer controls epoch boundaries. Informational. Neither front-running nor acceleration is possible for the distributor alone.

**Where:** `EmissionVault.sol:35-36`.

**Evidence:**
- [FACT-code] The distributor can influence only `to` and `amount`. Everything else is immutable, so the distributor cannot accelerate the schedule. Racing to be first to call at an epoch boundary gains nothing, because only the distributor can call.
- [INFERENCE] Chain 4663 is Robinhood Chain, an Arbitrum Orbit rollup ([Chainstack](https://docs.chainstack.com/reference/robinhood-getting-started), [QuickNode](https://www.quicknode.com/guides/robinhood/what-is-robinhood-chain); secondary sources). Arbitrum Nitro lets the sequencer set `block.timestamp` up to 24 h behind and 1 h ahead of real time, and keeps it monotonic ([Arbitrum docs](https://docs.arbitrum.io/build-decentralized-apps/arbitrum-vs-ethereum/block-numbers-and-time)).
- A sequencer that colludes with the distributor could therefore vest an epoch up to about 1 h early. That is at most one day's budget earlier, and the total is still capped.
- [UNVERIFIED] Whether Robinhood Chain uses the default Orbit bounds.

**Fix:** none at contract level. Document the trust in the sequencer.

### I-4: `release` accepts recipients where funds get stuck. Informational.

**Where:** `EmissionVault.sol:54`. The check blocks only `address(0)` and the vault itself.

**Evidence:** [INFERENCE] `release(to = address(token))` or `release(to = BatchPay)` succeeds, and those tokens become unrecoverable (see L-1). This needs a distributor mistake, and the budget is still enforced.

**Fix:** optionally also reject `to == address(token)`. Using BatchPay correctly is an operational matter.

### I-5: the 700M allocation is not bound to an EmissionVault on-chain. Informational.

**Where:** `UpToken.sol:19-22`.

**Evidence:**
- [FACT-code] The token does not store `vault` and cannot check that it is an `EmissionVault` whose `token()` points back to it.
- [FACT-test] `test_constructorVaultEqualsDeployer`: with `vault == msg.sender`, the deployer holds all 1e27 (the `+=` on line 22 adds the 300M to the same address).
- [FACT-code] `Deploy.s.sol:80-82` builds the vault against a predicted token address and reverts on a mismatch. Only this deployment path gives the binding.

**Fix:** after deployment, verify:
- the two constructor `Transfer` events;
- `vault.token() == token`;
- the vault's code hash.

Optionally, deploy the vault from the token's constructor with `new EmissionVault(address(this), …)` so the link holds by construction.

### I-6: gas at 400 recipients, loops, `unchecked`, and batch atomicity. Informational.

**Where:** `BatchPay.sol:18-28`.

**Evidence:**
- [FACT-test] `test_batch_400Gas_fresh_vs_warm_and_worst` with UP:

  | Batch | Execution gas |
  | --- | --- |
  | 400 fresh (zero-balance) recipients | 10,789,075 |
  | 400 recipients with existing balances, same tx | 3,942,836 |
  | 1000 fresh recipients | 26,856,684 |

  A fresh recipient costs about 26.9k gas, so at about 16.7M gas (the Ethereum-L1 per-transaction cap, EIP-7825) the practical limit is roughly 600 fresh recipients.
- [INFERENCE] The 400-entry calldata is 25,764 bytes. I did not measure the intrinsic calldata gas or the L1 data fee.
- [FACT-code] The loops are bounded by caller-supplied arrays. The caller pays, and nothing is stored between calls, so there is no griefing vector.
- [FACT-code] No `unchecked` blocks exist in the three files. `total += amount[i]` (line 20) is checked. [FACT-test] `test_batch_overflowTotalReverts`: `[max, 1]` panics.
- [INFERENCE] One recipient that reverts (for example a token-level blocklist or a transfer hook) reverts the whole batch. This is atomic by design, but a single bad address can hold up payouts. UP has no hooks or blocklist.

**Fix:** keep batches ≤ 400. Estimate gas with `eth_estimateGas` on chain 4663 before sending.

---

## Specific checks requested

- **Reentrancy through a malicious ERC-20 in BatchPay.** [FACT-code] Line 24 always pulls from `msg.sender`, and BatchPay never approves anyone.
  - [FACT-test] `test_batch_reentrancyBlocked`: re-entering `pay` from `transfer` is rejected by `nonReentrant`.
  - [FACT-test] `test_batch_cannotPullVictimApproval`:
    - A victim gives BatchPay unlimited approval for UP.
    - A malicious token's `transferFrom` calls `pay(UP, …)`. This fails.
    - The attacker calls `pay(UP, [attacker], [victimBalance])` directly. This reverts, first with `InsufficientAllowance` and then, after the attacker approves, with `InsufficientBalance`, because the pull comes from the attacker.
    - The victim's balance is unchanged.
  - [INFERENCE] A lying token can fake the balance checks on lines 25 and 29, but only for itself. `asset` is fixed per call, so BatchPay cannot be made to move a different token.
- **Partial or fee-on-transfer tokens.** An inbound fee reverts at line 25. An outbound-only fee is not detected (L-2). A token that returns `false` reverts via SafeERC20. A token with no return value is accepted. A token address with no code reverts in `_callOptionalReturn`.
- **Timestamp at and before `startTime`.** Both give 0 with no underflow, because of the guard on line 35. See Invariant 2.
- **Distributor front-running or acceleration.** Not possible beyond the sequencer's timestamp tolerance (I-3). The real exposure is the backlog (M-2) and the deployment `startTime` (M-1).

---

## What I could NOT verify, and why

1. **Deployed bytecode and parameters.** Nothing has been deployed. The README says no transactions were broadcast. Every verdict applies to source at the commit above, compiled locally. The actual `startTime`, `distributor` type (EOA or multisig) and vault/token binding can only be checked after launch.
2. **Robinhood Chain limits.** I did not query the chain. The per-transaction and per-block gas limits, the L1 data fee for a 25.7 KB batch, and the sequencer timestamp bounds (I-3) are not measured. The Orbit/Arbitrum facts come from documentation, and the chain details from secondary sources.
3. **Integrity of vendored OpenZeppelin.** I read the `ReentrancyGuard` (v5.1.0 header) and `SafeERC20` code that is actually compiled. I did not diff `lib/openzeppelin-contracts` against upstream commit `acd4ff74…`.
4. **Formal proof.** The conservation and schedule arguments come from reading the code plus fuzzing (2000 runs per property, full timestamp range up to 2^32 s). I did not run an SMT or formal verifier. `cumulativeBudget` for timestamps above 2^32 s past start was checked only at `type(uint256).max`.
5. **Compiler correctness.** I assume solc 0.8.30 with `via_ir` compiles these contracts correctly. I did not inspect the generated bytecode.
6. **Interaction with `UpHook`.** It is out of scope. [INFERENCE] The vault has no approvals and no callable exit except `release`, so the hook cannot remove vault funds. Hook deposits change only the vault's balance, not its budget. I did not read the hook to confirm how it behaves.
