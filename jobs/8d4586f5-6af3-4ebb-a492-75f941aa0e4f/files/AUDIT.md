# Audit report

> Audit the contracts in 0xtenang/Runner as they are.

| | |
|---|---|
| Repository | https://github.com/0xtenang/Runner.git |
| Commit | `15a66e930ceed9549d636c41182bd06a51128d42` |
| Job | `8d4586f5-6af3-4ebb-a492-75f941aa0e4f` |
| Judged | 2026-10-25 07:51 UTC |
| Findings | 4 low · 5 info |

Four agents audited the code as it is at `15a66e9`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Any sell beyond the pool's IMD reserve (or a zero-value sell when the reserve is empty) parks the pool price at the tick limit for free: marketCap()/getTokenInfo() read 0 and Trade reports an extreme

`contracts/RunnerHook.sol:454`

```
        (uint160 sqrtP,,,) = poolManager.getSlot0(poolKey(t).toId());
```

Merged from audit_economics (RunnerHook.sol:329) and audit_flow (RunnerHook.sol:454); both describe the same mechanism. The launch position is single-sided, [minUsableTick, startTick] with RUNNER as currency1 (mirrored otherwise), so there is no liquidity above the start price. A sell whose RUNNER input is worth more than the IMD the pool holds drains the reserve back to startTick and then keeps stepping through empty ticks up to the caller's sqrtPriceLimitX96; both official routers (RunnerRouter.sol:99, RunnerEthRouter.sol:162) and any generic v4 router pass the extreme limit. v4 swaps nothing in that region, the hook charges 4% only of the IMD actually paid and the routers pull only the RUNNER actually consumed, so no funds are lost. But afterSwap accepts a swap that moved nothing (the exact-in sell direction has IMD as the unspecified side, so it goes to the else branch, computes fee = 0 and _chargeFee returns early; nothing requires poolQuote > 0 or tokenAmount > 0), and the views read slot0 raw: marketCap() returns 0, getTokenInfo().sqrtPriceX96/marketCap are at the limit, and the Trade event for that swap carries fee 0, amounts 0 and sqrtPriceX96 = MAX_SQRT_PRICE-1 (or MIN when RUNNER is currency0). Right after openPool the reserve is 0 IMD, so an account holding no RUNNER and no IMD can do this with a 1-wei exact-in sell through PoolSwapTest or the universal router (RunnerRouter refuses only because out == 0 trips its own Slippage check). It can be repeated after every time sellers return all the IMD. The next genuine buy steps down ~745,000 empty ticks before reaching liquidity (about 83k extra gas measured) and fills at the launch price, so the pool itself is never damaged. Integrity problem for the app, indexers and PepesFamily-style tooling that reads this interface, not a fund-safety one. Fix (preserves the design): in afterSwap revert when the swap moved nothing (`if (poolQuote == 0 || tokenAmount == 0) revert PartialFill();` before the fee branch), and in marketCap()/getTokenInfo() clamp sqrtP to the launch price when the current tick is outside the position (tick > startTick when quoteIsCurrency0, tick < -startTick otherwise), emitting the clamped price in Trade; optionally have the routers use TickMath.getSqrtPriceAtTick(launch tick) as the sell-side price limit so official-router sells stop exactly at the reserve boundary.

**Reproduction**

Reproduced on this commit with contracts/test/scratch/Judge.t.sol (setup identical to contracts/test/RunnerHook.t.sol: pool opened at startTick 142600, IMD is currency0). Case A, zero reserve: griefer with 0 RUNNER and 0 IMD calls PoolSwapTest.swap(key, SwapParams(zeroForOne = !imdIs0, amountSpecified = -1, sqrtPriceLimitX96 = MAX_SQRT_PRICE-1)). Expected: refused, or price stays at the reserve boundary (tick 142600, marketCap 641.6e18). Actual: swap succeeds, slot0 tick 142600 -> 887271, hook.marketCap(runner) 641608811066259581626 -> 0, griefer's RUNNER balance still 0. A following router.buy(100 IMD) still fills and marketCap returns above 600e18, at 512,984 gas versus 429,745 for the same buy without the push. Case B, official router: alice buys with 1,000 IMD (pool holds 960 IMD), team sends her 5,000,000 RUNNER more, alice calls router.sell(runner, got + 5,000,000e18, 0, deadline). Actual: she receives 921.6 IMD, only 93,735,273.2e18 RUNNER is pulled (not the full amount), marketCap == 0 afterwards; bob's router.buy(1,000 IMD) restores marketCap to exactly its post-alice-buy value, showing the pool was not damaged.

### 2. Low: setProtocolWallet accepts the PoolManager and the hook: swept holder IMD is then skimmable by anyone (PoolManager) or stuck forever (hook)

`contracts/RunnerToken.sol:492`

```
        if (wallet == address(this)) revert BadAddress(); // swept IMD would stay here and be re-booked
```

Merged from audit_permissions (PoolManager and hook cases) and audit_flow (hook case), same line and same guard gap. setProtocolWallet refuses only address(0) and the token itself, although the token already holds the two other protocol addresses as immutables (`poolManager`, `hook`) and IMD sent to either is lost to the protocol. sweepExpired() is permissionless and pays protocolWallet with a plain IMD transfer. If protocolWallet is the Uniswap v4 PoolManager, the IMD enters the PoolManager outside settle accounting; in v4 whoever called sync(IMD) before such a transfer and settle() after it is credited the difference, so an unprivileged caller wraps sweepExpired() in their own unlock and takes the whole swept amount. If protocolWallet is the hook, the IMD sits as a raw ERC-20 balance in RunnerHook, which only ever moves ERC-6909 claims (collectProtocolFees burns claims and takes; nothing transfers raw IMD), so it is unrecoverable. Owner misconfiguration rather than a bypass, but it is the same guard class the team already closed for the token address itself (second audit #4), and the PoolManager case has an unprivileged amplifier. Fix: also revert when `wallet == poolManager || wallet == hook` (both immutables on this contract), mirroring the existing address(this) check.

**Reproduction**

Reproduced on this commit (contracts/test/scratch/Judge.t.sol, test_G_protocolWalletPoolManager_anyoneSkimsSweep and test_G_protocolWalletHook_sweptImdStuck). State: pool open, alice buys 10,000 IMD of RUNNER via RunnerRouter (200 IMD booked as today's holder rewards). Owner calls setProtocolWallet(address(poolManager)). Expected: revert like the address(this) case. Actual: accepted. Warp 9 days. An attacker contract calls poolManager.unlock(); in unlockCallback it calls poolManager.sync(IMD), RunnerToken.sweepExpired(30) (transfers 200 IMD from the token to protocolWallet = PoolManager), poolManager.settle() (credited 200e18), poolManager.take(IMD, attacker, 200e18). Result: attacker holds 200 IMD, imd.balanceOf(poolManager) unchanged, protocol receives nothing. Variant: setProtocolWallet(address(hook)) is accepted; after sweepExpired(30), imd.balanceOf(hook) == 200e18 and collectProtocolFees(IMD) leaves it at 200e18.

### 3. Low: setFeeRecipient accepts the PoolManager: protocol fees are then burned into unaccounted PoolManager surplus by anyone calling collectProtocolFees

`contracts/RunnerHook.sol:413`

```
        if (feeRecipient_ == address(0) || feeRecipient_ == address(this)) revert ZeroAddress(); // IMD sent here would be stuck
```

Mirror of the token-side guard gap. The hook rejects itself as fee recipient because IMD would be stuck, but accepts its own immutable `poolManager`. collectProtocolFees() is permissionless; _collect burns the hook's ERC-6909 IMD claims and calls poolManager.take(IMD, feeRecipient, amount). With feeRecipient == poolManager, take() debits the hook's delta and performs an IMD transfer from the PoolManager to itself, so the IMD never leaves the PoolManager and no account is credited: the claims are gone, pendingProtocolFees is zeroed, and the fee becomes surplus inside the PoolManager that nobody (including the protocol) can withdraw. Owner misconfiguration, but the burn is triggered by anyone the moment the setter lands, and it costs the whole pending protocol fee plus every fee collected until the recipient is corrected. Fix: `if (feeRecipient_ == address(0) || feeRecipient_ == address(this) || feeRecipient_ == address(poolManager)) revert ZeroAddress();`.

**Reproduction**

Reproduced on this commit (contracts/test/scratch/Judge.t.sol, test_H_feeRecipientPoolManager_burnsProtocolFees). State: pool open, alice buys 10,000 IMD of RUNNER (pendingProtocolFees[IMD] == 200e18, hook holds 200e18 IMD claims). Owner calls setFeeRecipient(address(poolManager)). Expected: revert like the address(this) case. Actual: accepted. Anyone calls collectProtocolFees(IMD). Expected: 200 IMD delivered to a recipient. Actual: pendingProtocolFees[IMD] == 0, the hook's ERC-6909 IMD claim balance dropped by exactly 200e18, imd.balanceOf(poolManager) unchanged; the 200 IMD are unaccounted inside the PoolManager.

### 4. Low: Run-reward backlog larger than the day's emission can never be claimed with its true total (all-or-nothing cap, no carry-over)

`contracts/RunnerToken.sol:379`

```
        if (claimedOnDay[day] + amount > emissionOn(day)) revert DailyCapReached();
```

claim() pays the full difference totalEarned - claimed[account] or nothing, compares it with the whole day's emission, and the emission is not carried over between days. Once the schedule has halved down to the floor (100,000 RUNNER/day after seven halvings, ~210 days with the default schedule), any runner whose unclaimed backlog exceeds the day's emission is refused on every day, forever, even when nobody else claimed that day. claimable() correctly returns 0 for the same input, so the app shows nothing to claim. The only way out is off-chain: the server must sign staged intermediate totals (the contract allows it, but nothing documents it), or the owner raises the schedule protocol-wide. Invariant 'a valid signed total is eventually payable' breaks exactly where amount > emissionOn(day), persistently. Fix options: let claim() pay min(amount, emission left today) and record claimed[account] += paid (the signature stays reusable until exhausted, safe because claimed[] only grows), or document that the server must sign staged totals <= today's remaining emission.

**Reproduction**

Reproduced on this commit (contracts/test/scratch/Judge.t.sol, test_C_backlogAboveDailyEmission_neverClaimable). State: owner sets a signer and calls startEmission(); warp 210 days so emissionOn(today) == 100_000e18 (10M >> 7 = 78,125 < floor). Input: a valid signer signature for (alice, totalEarned = 100_000e18 + 1, deadline, instant = false), claimed[alice] == 0, claimedOnDay[today] == 0. Expected: the earned amount is claimable over time. Actual: claim() reverts DailyCapReached; the same signature one day later reverts DailyCapReached again; claimable(alice, total) returns 0. A signature for exactly 100_000e18 succeeds and sets claimed[alice] = 100_000e18.

### 5. Info: Trust assumption: every official-router trade and every holder claim depends on the IMD token's issuer-controlled blocklist and transfer switch

`contracts/RunnerRouter.sol:114`

```
        pad.flush(d.token);
```

Not a code defect in Runner; recorded as a counterparty trust assumption the launch documentation should state. Both routers call pad.flush on every trade; because the same swap just charged the 4% fee, pendingHolderFees[token] > 0 at that point, so _flush runs unconditionally: poolManager.burn + poolManager.take(IMD, RunnerToken, amount) (an IMD.transfer to the token contract) followed by RunnerToken.syncHolderRewards(). The live IMD on Robinhood Chain is an owner-controlled token exposing blocked(address) and a transfer switch (per the economics specialist's probe; its exact blocklist semantics are unverified because the explorer source could not be fetched). If the IMD issuer blocks the RunnerToken address (or the PoolManager, or disables transfers), every RunnerRouter.buy/sell and RunnerEthRouter.buyWithEth/sellForEth reverts inside _flush, while swaps through any other v4 router keep working and keep accumulating ERC-6909 fee claims in the hook that flush() can no longer deliver; claimHolderRewards() and sweepExpired() revert in _sendReward, freezing all holder IMD inside RunnerToken; collectProtocolFees reverts if feeRecipient is blocked (owner-fixable via setFeeRecipient). If the team wants trading to survive a reward-token freeze, the routers could flush in a try/catch (leaving the holder share pending) so only reward delivery, not trading, depends on IMD's policy; that is a design decision.

**Reproduction**

Reproduced on this commit against a mock with the same blocklist shape (contracts/test/scratch/Judge.t.sol, JudgeTrustTest.test_B_rewardTokenBlocklist_freezesOfficialRoutersAndClaims): deploy the system with a reward token whose transfer() reverts when sender or recipient is blocked. alice's router.buy(1,000 IMD) succeeds. Mark RunnerToken as blocked. Expected per the design text ('every trade pays 4%, 2% to holders'): trades keep working. Actual: router.buy(runner, 1,000e18, 0, deadline) reverts; PoolSwapTest.swap of 1,000 IMD on the same pool succeeds and raises pendingHolderFees by 20e18; hook.flush(runner) reverts; after 9 days sweepExpired(30) reverts TransferFailed. Not reproducible against the live IMD without a fork; the live token's selectors are what the specialist verified.

### 6. Info: marketCap() prices the fixed 1,000,000,000 constant, not the live totalSupply, so it overstates the cap after burns

`contracts/RunnerHook.sol:456`

```
            ? FullMath.mulDiv(FullMath.mulDiv(TOTAL_SUPPLY, Q96, sqrtP), Q96, sqrtP)
```

RunnerToken has no mint but does burn: every instant claim burns 20% of the amount (INSTANT_BURN_BPS), releaseEarly burns 20% of unfinished locks, and holders can burn(). totalSupply therefore only falls, while marketCap() (and getTokenInfo().marketCap, which tools read) multiplies the hard-coded TOTAL_SUPPLY constant by the pool price, so the reported figure drifts above the real fully-diluted cap by the burned fraction. View-only; no on-chain logic depends on it. The hook already has IRunnerToken.totalSupply() in its interface. Fix: use IRunnerToken(t).totalSupply() in place of TOTAL_SUPPLY in marketCap (keep the constant for openPool's checks).

**Reproduction**

Reproduced on this commit (contracts/test/scratch/Judge.t.sol, test_F_marketCapIgnoresBurns). State: pool open at the launch price, marketCap == 641608811066259581626. Team burns 50,000,000 RUNNER; totalSupply() == 950_000_000e18. Expected: marketCap falls 5% to ~609.5e18. Actual: marketCap unchanged at 641608811066259581626.

### 7. Info: Hook fee truncates to zero for IMD legs below 25 wei (exact-in) / 24 wei (exact-out)

`contracts/RunnerHook.sol:292`

```
        uint256 fee = exactIn ? (amount * FEE_BPS) / BPS : (amount * FEE_BPS) / (BPS - FEE_BPS);
```

Fees round down. For an exact-in buy, amount * 400 / 10000 == 0 for every amount <= 24 wei of IMD; for an exact-out sell, amount * 400 / 9600 == 0 for amount <= 23 wei; the mirrored formulas in afterSwap (line 329) behave the same on the unspecified side. Such trades pay no fee at all. With 18-decimal IMD the fee-free amount is 2.4e-17 IMD per swap and gas dwarfs it by many orders of magnitude, so there is no economic leak; recorded so the 'exactly 4%' statements in comments and docs are read as 'floor of 4%'. Fix if wanted: round the fee up (`(amount * FEE_BPS + BPS - 1) / BPS`), which keeps the PartialFill equality checks valid since they reuse the same `fee` value.

**Reproduction**

Reproduced on this commit (contracts/test/scratch/Judge.t.sol, test_E_tinyBuyPaysNoFee). Input: PoolSwapTest exact-in buy with amountSpecified = -24 (IMD specified). Expected per docs: fee = 4% of 24 wei. Actual: pendingProtocolFees + pendingHolderFees unchanged (fee = 24 * 400 / 10000 = 0, _chargeFee returned early, the swap went through). The same swap with amountSpecified = -25 raises the pending total by exactly 1 wei.

### 8. Info: sweepExpired(type(uint256).max) reverts on the end-bound addition instead of meaning 'all'

`contracts/RunnerToken.sol:275`

```
        uint256 end = d + maxDays;
```

The end bound is computed as nextSweepDay + maxDays in checked arithmetic. A caller passing type(uint256).max (the idiomatic 'no limit') reverts with an arithmetic panic rather than sweeping everything. No funds are affected; every smaller value works and the sweep is permissionless and resumable, so this is a usability edge only. Fix: `uint256 end = maxDays > type(uint256).max - d ? type(uint256).max : d + maxDays;` or loop on a counter.

**Reproduction**

Reproduced on this commit (contracts/test/scratch/Judge.t.sol, test_D_sweepExpiredMax_overflows). State: nextSweepDay == 20500 (the deploy day). Input: sweepExpired(type(uint256).max). Expected: sweep all expired days. Actual: Panic(0x11) arithmetic overflow at `d + maxDays`; sweepExpired(type(uint256).max - nextSweepDay) succeeds.

### 9. Info: burnFrom(address(0), 0) emits a Transfer(0x0, 0x0, 0) event (same class as third audit #5)

`contracts/RunnerToken.sol:236`

```
    function burnFrom(address from, uint256 value) external {
```

The third audit's finding 5 removed the forged mint event from transferFrom(address(0), to, 0) by adding a zero-address check in _transfer. burnFrom and burn do not go through _transfer: _spendAllowance(address(0), 0) passes (allowance 0 is not less than value 0), _burn(address(0), 0) passes its balance check, and `emit Transfer(from, address(0), value)` fires with from == address(0). No balance or supply changes, so the impact is limited to indexers and explorers that treat Transfer-from-zero as a mint. Fix: revert ZeroAddress in _burn when `from == address(0)` (or in burnFrom), matching _transfer.

**Reproduction**

Reproduced on this commit (contracts/test/scratch/Judge.t.sol, test_I_burnFromZero_emitsEvent). Any caller invokes RunnerToken.burnFrom(address(0), 0). Expected: revert ZeroAddress, as transferFrom(address(0), to, 0) now does. Actual: the call succeeds and emits Transfer(address(0), address(0), 0) (checked with vm.expectEmit on the token address).

---

Judge's submission `b6cdf21065f81c36d7e0d0902f44529c35e1d1130aa89aaf41f7a164f0654cd6`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
