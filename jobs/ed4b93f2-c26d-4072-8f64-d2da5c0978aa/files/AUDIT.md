# Audit report

> Audit the contracts in 0xtenang/Runner as they are.

| | |
|---|---|
| Repository | https://github.com/0xtenang/Runner.git |
| Commit | `3ffb33f80479d0e616c46f1d9deb7c11188c721f` |
| Job | `ed4b93f2-c26d-4072-8f64-d2da5c0978aa` |
| Judged | 2026-10-25 10:07 UTC |
| Findings | 2 low · 8 info |

Four agents audited the code as it is at `3ffb33f`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Donations to the RUNNER/IMD pool are accepted: beforeDonate is never wired (BEFORE_DONATE flag not declared), so donated tokens are permanently lost

`contracts/RunnerHook.sol:196`

```
                beforeDonate: false,
```

RunnerHook defines beforeDonate()/afterDonate() overrides that revert HookNotAllowed (lines 555-569) and the comment above the block (lines 505-507) says everyone other than the hook is refused. But the Permissions struct passed to Hooks.validateHookPermissions sets beforeDonate: false and HOOK_FLAGS (line 90) does not include Hooks.BEFORE_DONATE_FLAG (1 << 5). v4-core only calls beforeDonate when that flag is set in the hook address (Hooks.beforeDonate: `if (self.hasPermission(BEFORE_DONATE_FLAG))`), so the revert is dead code and PoolManager.donate() on the RUNNER/IMD pool succeeds for anyone. Donated IMD or RUNNER is credited as fee growth to the only in-range position, which belongs to the hook; the hook never calls modifyLiquidity after launch and has no collect path, so the tokens are unrecoverable by anyone. No fee or reward accounting is affected. Fix: either set beforeDonate: true and add Hooks.BEFORE_DONATE_FLAG to HOOK_FLAGS (the mined hook address changes, so the deploy salt must be re-mined), or delete the unreachable beforeDonate/afterDonate/afterInitialize/afterAddLiquidity/beforeRemoveLiquidity/afterRemoveLiquidity overrides and correct the comment so the code states what is actually refused. Reported by the flow specialist; reproduced here.

**Reproduction**

State: pool opened as in contracts/test/RunnerHook.t.sol setUp; alice holds IMD and has approved a v4-core PoolDonateTest instance. Input: alice calls PoolDonateTest.donate(hook.poolKey(runner), imdIs0 ? 10e18 : 0, imdIs0 ? 0 : 10e18, ""). Expected (per the comment and the beforeDonate override): revert HookNotAllowed. Actual: the call succeeds; PoolManager's IMD balance rises by exactly 10e18 (scratch test test_donateAllowed, log 'pm imd gained: 10000000000000000000'); hook.pendingHolderFees and pendingProtocolFees are unchanged; no entry point in RunnerHook can withdraw the 10 IMD.

### 2. Low: RunnerDeployLib.sqrt returns 2 for input 2 (initial Babylonian guess is not an upper bound at x = 2)

`contracts/utils/RunnerDeployLib.sol:42`

```
        z = x;
        uint256 y = (x >> 1) + 1;
        while (y < z) {
```

The integer square root starts with z = x and y = x/2 + 1 and only iterates while y < z. For x = 2 the first guess y = 2 equals z, so the loop never runs and the function returns 2, although floor(sqrt(2)) = 1. Every other x in [0, 50) is correct (checked exhaustively), so the defect is confined to x = 2. In its only caller, startTickForMarketCap, the argument is supply * 2^192 / marketCap, which is astronomically larger than 2 for any sane market cap, so the deployed start tick (142,600 for 635 IMD, matching js/config.js and test_startTick_matchesAppConfig) is unaffected. It is still a wrong result from a pure helper that tests and deploy tooling rely on. Fix: use the standard form `z = (x >> 1) + 1; y = x; while (z < y) { y = z; z = (x / z + z) >> 1; } return y;` or special-case x <= 3 (return 1). Reported by the math specialist; reproduced here.

**Reproduction**

Call RunnerDeployLib.sqrt(2). Expected: 1. Actual: 2 (2*2 = 4 > 2). Scratch test test_sqrt_small asserts z*z <= x < (z+1)*(z+1) for x in 0..49 and only x = 2 violates it, returning z = 2.

### 3. Info: collectProtocolFees can be driven mid-unlock by any unlocker, unlike flush

`contracts/RunnerHook.sol:377`

```
        if (poolManager.isUnlocked()) _collect(quote);
```

flush() (lines 366-369) enforces the rule stated in its comment: while the PoolManager is unlocked, only the hook's own routers may distribute, because a third party's unlock callback is running with pool tokens it may have taken. collectProtocolFees() is the paired distribution function for the other half of the same fee, but its mid-unlock branch has no caller check: any contract that calls poolManager.unlock() can call hook.collectProtocolFees(IMD) from its unlockCallback and the hook burns its ERC-6909 claims and takes IMD to feeRecipient inside the stranger's unlock. Traced impact: the hook's own delta nets to zero (burn +amount, take -amount) and the IMD goes to the configured feeRecipient, so no funds are misdirected; the only effect is that the hook settles inside an untrusted caller's unlock, which the author chose to forbid for flush. Asymmetry between two paired functions, kept for consistency; no victim identified. Fix (preserves behaviour): mirror flush: `if (poolManager.isUnlocked()) { if (msg.sender == router || msg.sender == ethRouter) _collect(quote); } else poolManager.unlock(...)`, or drop the mid-unlock branch so protocol fees are always collected through the hook's own unlock. Reported by the permissions specialist; reproduced here.

**Reproduction**

State: pool open, alice buys 1,000 IMD of RUNNER through RunnerRouter, so pendingProtocolFees[IMD] = 20e18. Input: an unrelated contract (MidUnlockCollector) calls poolManager.unlock("") and, inside its unlockCallback, hook.collectProtocolFees(IMD). Expected (by the rule flush enforces): nothing happens mid-unlock for a non-router caller. Actual: the call succeeds, pendingProtocolFees[IMD] becomes 0 and feeRecipient receives 20e18 IMD while the stranger's unlock is still open (scratch test test_collect_midUnlock_stranger, logs 'pendingProtocolFees after stranger unlock: 0', 'feeRecipient IMD: 20000000000000000000').

### 4. Info: excludePool's pool check is satisfied by any contract exposing token0(), contrary to its NatSpec guarantee

`contracts/RunnerToken.sol:483`

```
        if (_poolToken(pool, 0x0dfe1681) != address(this) && _poolToken(pool, 0xd21220a7) != address(this)) revert NotAPool(); // token0(), token1()
```

The NatSpec (lines 478-479) says 'Only contracts that report RUNNER as token0 or token1 qualify, so a wallet (including a smart-contract wallet) can never be cut out this way.' The guard only requires a staticcall to token0() or token1() to return RUNNER's address; it does not check for any pool behaviour (reserves, factory, liquidity). A holder's smart-contract wallet, vault or any contract that exposes a token0() view returning RUNNER meets the test, so the owner can exclude it from holder rewards for every claimable day, and _exclude retroactively removes its weight from the unpaid days in the 7-day window. This is an owner-only action and the owner is trusted; the excluded account can still transfer freely. It is kept because the stated guarantee in the documentation and AUDIT.md ('Real RUNNER pools only') is stronger than what the code enforces, and because exclusion is irreversible (there is no includePool). Fix options that keep the design: document the actual rule, and/or add an include/revert path so a mistaken exclusion can be undone, or strengthen the check (e.g. require both token0() and token1() to resolve and a factory()/getReserves()-style surface), noting that no on-chain check can perfectly distinguish a pool from a wallet. Reported by the permissions specialist; reproduced here.

**Reproduction**

State: contract W with `address public token0 = RUNNER` holds 1,000,000 RUNNER received from the team wallet. Input: owner calls excludePool(W). Expected per NatSpec: revert NotAPool, since W is a wallet, not a pool. Actual: the call succeeds, excludedFromHolderRewards[W] = true, eligibleBalanceOn(W, today) = 0, and eligibleSupply drops by exactly 1,000,000e18 (scratch test test_excludePool_wallet).

### 5. Info: Trade event attributes non-router swaps to tx.origin

`contracts/RunnerHook.sol:340`

```
            (sender == router || sender == ethRouter) && hookData.length == 32 ? abi.decode(hookData, (address)) : tx.origin;
```

For swaps that do not come through RunnerRouter/RunnerEthRouter the hook records tx.origin as the trader. A smart-contract wallet (Safe, ERC-4337 account) trading through another v4 router, or a user whose transaction is relayed, is attributed to the relayer/bundler EOA. Nothing in the contracts or the repository's JS reads this field for rewards, fees or permissions, so the impact is limited to off-chain analytics and explorers. hookData is attacker-chosen for non-router senders, and the code correctly ignores it in that case. Suggested change: emit `sender` (the router contract) when the sender is not one of the hook's own routers, or emit both. Reported by the permissions specialist; reproduced here.

**Reproduction**

State: pool open. Input: relayer EOA R sends a transaction in which contract C calls a v4-core PoolSwapTest router to buy RUNNER with 1,000 IMD (vm.prank(C, R) in Foundry). Expected: Trade.trader identifies the trading account C or the router. Actual: the Trade log's indexed trader topic equals R, the tx.origin (scratch test test_tradeEvent_txOrigin, log 'trader: 0x011f44c6...8dB8' == makeAddr('relayer')).

### 6. Info: emissionSchedule() reports a superseded schedule as `current` once the pending one is in force

`contracts/RunnerToken.sol:458`

```
    function emissionSchedule() external view returns (Schedule memory current, Schedule memory next) {
        return (_schedule, _nextSchedule);
```

Schedule promotion is lazy: setEmissionSchedule() only copies _nextSchedule into _schedule on the owner's next call (line 529), while emissionOn()/claim() pick the pending schedule directly whenever day >= _nextSchedule.fromDay. The NatSpec says the view returns 'the schedule in force and the one waiting to start', but after the pending schedule's fromDay passes the view keeps returning the old schedule as `current` and the live one as `next`, even though nothing is waiting. Economic impact is nil (claim() and emissionOn() are correct); it is a view/write divergence that can mislead the app or an off-chain monitor reading current.dailyStart. Fix: in emissionSchedule(), return (_nextSchedule, empty) when _nextSchedule.fromDay != 0 && _today() >= _nextSchedule.fromDay, or promote eagerly in a small internal helper shared with setEmissionSchedule(). Reported by the economics specialist; reproduced here.

**Reproduction**

Owner: startEmission() on UTC day D, then setEmissionSchedule(5_000_000e18, 30, 100_000e18) on day D (next.fromDay = D+1). Warp to day D+1. emissionOn(D+1) == 5_000_000e18 (new schedule in force) but emissionSchedule() returns current.dailyStart == 10_000_000e18 and next.dailyStart == 5_000_000e18 with next.fromDay == D+1 == today. Expected: current == the 5M schedule, next == none. Scratch test test_emissionSchedule_view_stale (logs: current.dailyStart 1e25, next.dailyStart 5e24, next.fromDay 20501).

### 7. Info: RUNNER or IMD transferred to the hook after openPool is unrecoverable (no sweep path)

`contracts/RunnerHook.sol:275`

```
        token_.transferOut(DEAD, IRunnerToken(token_).balanceOf(address(this)));
```

The only code that ever moves an ERC-20 balance held directly by the hook is this line inside _addLaunchLiquidity, which runs exactly once in openPool (AlreadyLaunched blocks a second run). All later fee flows use ERC-6909 claims inside the PoolManager (mint/burn/take), never the hook's own ERC-20 balance. So any RUNNER or IMD sent to the hook address after launch (a user pasting the wrong address, or IMD sent to the 'pool' address shown in explorers) is frozen forever. The comment on setFeeRecipient (line 423) acknowledges the IMD case; the RUNNER case is not documented. The hook is excluded from holder rewards, so there is no dilution; this is a loss-of-user-funds note, not a protocol defect. Fix (optional, preserves the locked-liquidity design because it must never touch PoolManager positions or claims): an owner-only sweep that transfers the hook's direct ERC-20 balance of a given asset to a recipient, or document that the hook address must not receive tokens. Reported by the economics specialist; reproduced here.

**Reproduction**

After openPool: team calls runner.transfer(address(hook), 1e18). runner.balanceOf(hook) == 1e18; openPool(token) reverts AlreadyLaunched (scratch test test_tokensStuckInHook); by inspection flush/collectProtocolFees only burn claims and take from the PoolManager, and no other function in RunnerHook calls transfer/transferOut on an ERC-20. Expected: a recovery path or an explicit warning; actual: permanently stuck.

### 8. Info: Launch 'rounding dust' is not bounded by LIQUIDITY_BUFFER at extreme (but accepted) start ticks: ~0.87 RUNNER burned at startTick 887,000

`contracts/RunnerHook.sol:95`

```
    /// @dev Kept out of the liquidity calculation so rounding can never ask for more than the allocation; burned.
```

_launchRange floors the liquidity L = (100M - 1e9) * Q96 / (sqrtU - sqrtL) (or the currency0 mirror). The RUNNER actually pulled by modifyLiquidity for that floored L is smaller than the allocation by up to one liquidity unit's worth of token, i.e. (sqrtU - sqrtL)/Q96 wei for RUNNER-as-currency1 or roughly Q96/sqrtL wei for RUNNER-as-currency0. At the configured tick 142,600 that is ~170 wei (measured 1,000,000,170 wei burned including the buffer), so the comment and the existing test (assertLe(balanceOf(DEAD), 2e9)) hold. But the constructor accepts any tick up to maxUsableTick - 200 = 887,000, and there the floored-liquidity remainder is ~8.7e17 wei: 870,828,554,575,458,962 wei end up at DEAD instead of in the pool. Nothing reverts and the amount (0.87 RUNNER of 100M) is economically negligible, so this is informational: the buffer comment is accurate in the safe direction, but 'only rounding dust burned' is only true near the production tick. If a different launch price is ever chosen, re-check the burned amount, or compute the exact owed amount via LiquidityAmounts/SqrtPriceMath and transfer that instead of the whole hook balance. Reported by the math specialist; reproduced here for the RUNNER-as-currency1 ordering (the specialist also measured 874,638,813,332,944,459 wei for the other ordering).

**Reproduction**

Deploy RunnerHook with startTick_ = 887000 (passes the constructor's BadTick check), deploy RunnerToken against it, call openPool. Expected (per comment/test): RUNNER at 0xdEaD approximately equals LIQUIDITY_BUFFER = 1e9 wei. Actual: 870,828,554,575,458,962 wei burned (scratch test test_dust_extremeTick, log 'burned at DEAD (tick 887000): 870828554575458962'); the same procedure at startTick 142,600 burns 1,000,000,170 wei (test_dust_productionTick), within the documented bound.

### 9. Info: Run-reward daily cap is per UTC day, so two full-cap claims can be paid seconds apart across midnight (header comment says 'per day')

`contracts/RunnerToken.sol:379`

```
        if (claimedOnDay[day] + amount > emissionOn(day)) revert DailyCapReached();
```

The cap is keyed on block.timestamp / 1 days and resets exactly at 00:00:00 UTC. The contract header (lines 49-50) states 'even a stolen owner key can move at most 2.5% of the pool per day'. That is true per calendar day, but the rate limit it implies over any rolling 24h window does not hold at the boundary: a signer (or compromised owner who rotates the signer) can have emissionOn(D) claimed at 23:59:59 and emissionOn(D+1) claimed at 00:00:00, i.e. up to 2 * 20,000,000 RUNNER = 40M (5% of the 800M pool) within two consecutive blocks, then nothing more until the next midnight. No invariant of the contract is broken and this is inherent to the chosen day-bucket design, so it is recorded as a design note rather than a defect; it quantifies the worst case of the owner-key trust assumption recorded separately. If a true rolling limit is wanted, track a sliding window instead of a per-day counter; otherwise adjust the comment to 'per UTC day'. Reported by the math specialist; reproduced here.

**Reproduction**

State: signer set, startEmission() on day D (default schedule, emissionOn(D) = 10M), claimedOnDay[D] = 0. At timestamp (D+1)*86400 - 1 call claim(alice, totalEarned = 10M, deadline, v, r, s, false) -> succeeds, claimedOnDay[D] = 10M. At timestamp (D+1)*86400 call claim(alice, totalEarned = 20M, ...) -> succeeds because claimedOnDay[D+1] is 0. Expected from the header comment: at most one day's emission per 24h. Actual: claimed[alice] == 20,000,000e18 within 1 second (scratch test test_cap_acrossMidnight, log 'claimed within 1 second: 20000000000000000000000000').

### 10. Info: Privileged-role trust assumptions (documented, by design)

`contracts/RunnerToken.sol:499`

```
    function setSigner(address newSigner) external onlyOwner {
```

Not a defect; recorded separately as the assignment asks so the requester can see the full owner surface. RunnerToken owner: setSigner (chooses who can authorise run-reward claims) combined with setEmissionSchedule (up to MAX_DAILY_EMISSION = 20M/day, effective next UTC day) lets a compromised owner key sign claims to itself for up to 20M RUNNER per UTC day from the run-reward pool, indefinitely until the key is recovered (see the midnight-boundary note for the 40M-in-two-blocks worst case); setClaimsPaused halts claims (locks and holder rewards unaffected); setProtocolWallet redirects the protocol share and expired holder rewards (pending sweeps go to the new wallet); excludePool is irreversible. RunnerHook owner: openPool (once), setFeeRecipient (pending, uncollected protocol fees go to the new recipient; may be set to the RunnerToken, which would reclassify protocol fees as holder rewards on the next sync). RunnerGenesis owner: setTransferValidator accepts any address including one without code, in which case every transferFrom/safeTransferFrom reverts (Solidity's high-level call to a function with no return value checks extcodesize) until the owner resets it; setTreasury to a reverting receiver halts minting. Fee constants, liquidity lock, total supply and the 20M/day ceiling are not changeable by anyone. All of these are consistent with the intended design and the README/AUDIT.md statements; the mitigation already planned (multisig owner before launch) is the right one. Reported by the permissions specialist; the claim-cap arithmetic was verified by the midnight-boundary test and the rest by code reading.

**Reproduction**

Concrete state for the largest power: owner key compromised on day D after startEmission. Owner calls setSigner(attackerKey) and setEmissionSchedule(20_000_000e18, 7, 20_000_000e18). From day D+1 the attacker signs Claim(attacker, totalEarned = 20M*k, deadline, false) each day and claim() pays 20M RUNNER/day (claimedOnDay[D+1] + 20M <= emissionOn(D+1) = 20M). Expected: bounded by the daily cap, which it is; nothing above 20M per UTC day is possible (scratch test test_cap_acrossMidnight shows the cap is enforced per day bucket). For the NFT: owner calls setTransferValidator(0x1234) (no code); any holder's transferFrom then reverts until setTransferValidator(address(0)).

---

Judge's submission `c4efd7c7e3a42811cb4ade000ee66314fdf7d5f755453dcde43d388927f41432`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
