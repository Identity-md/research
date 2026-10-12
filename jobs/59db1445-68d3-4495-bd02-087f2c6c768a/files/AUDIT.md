# Audit report

> CourierPad: in-game token launchpad for Courier World on Robinhood Chain (4663). Players with an open post office (PostOffice 0x26D80804D0FA2F4598369E0062bFC9536d115D82) launch a PadToken (1B fixed supply, OpenZeppelin ERC20 + Permit, no owner) by burning a $STAMP fee (burnFrom, bounded by the launcher’s maxStampFee; permit variant). 5% of the supply goes to the treasury for drops; 95% is single-sided liquidity in a Uniswap v4 pool against IMD, owned by the pad, with no way to remove it. The pad is every pool’s hook: 4% of the IMD side of every swap to the fee recipient (StampHook’s audited fee code, keyed per pool), full fills only, and nobody else can create pools with the hook or add liquidity. StampRouter and StampEthRouter are reused unchanged.
>
> Please check: fee accounting across many pools and both currency orders, that launch liquidity can never be removed and no pool can be hijacked, the start-price bounds (liquidity overflow), the fee and permit handling at launch, that a launched token can’t be blocked from trading, and the owner’s powers.
>
> Source: contracts/src/CourierPad.sol and contracts/src/PadToken.sol; tests in contracts/test/CourierPad.t.sol and contracts/test/CourierPad.fork.t.sol. Commit 0b01b0c.

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/courierworld.git |
| Commit | `0b01b0c21c71ce2c8cb6b53b49c9bb5ff75cc3e1` |
| Job | `59db1445-68d3-4495-bd02-087f2c6c768a` |
| Judged | 2026-10-12 15:26 UTC |
| Findings | 4 low · 5 info |

Four agents audited the code as it is at `0b01b0c`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: A launch pins the $STAMP fee it agreed to but not the start price: an owner setStartTick sequenced before it reprices the launch with no way for the launcher to object

`contracts/src/CourierPad.sol:295`

```
        int24 st = startTick;
```

Merged from audit_math, audit_flow, audit_permissions and audit_economics (all four reported the same mechanism). _launch bounds one owner-settable launch parameter with a launcher-supplied value (`if (fee > maxStampFee) revert FeeChanged(fee);`, line 288, documented in setStampFee as protecting a pending launch) but reads the other, `startTick`, straight from storage with nothing from the launcher to pin it. The owner may move startTick anywhere in [-300000, 400000] on the 200 spacing, and the launch burns the $STAMP fee before it opens the pool at whatever tick is current, so a launcher who submitted against the configured ~635 IMD (5000 USD) start can burn 500 $STAMP and get a token whose entire 1B supply is worth 4 gwei of IMD (top of the range) or ~1e22 IMD (bottom), with the launch tick, sellPriceLimit and marketCap fixed at that value forever. Robinhood Chain has no public mempool (AUDIT.md), so no third party can exploit this; it is reachable only when the owner's own setStartTick is sequenced ahead of a player's pending launch (an honest retune while launches are in flight, or a compromised owner key). It is an owner power and not a permission bypass; it is reported because the contract already treats the launch as a commitment the launcher bounds (FeeChanged) and leaves the half that decides the launch's economics unbounded. Minimal fix that keeps the owner's power to retune future launches: add an `int24 expectedStartTick` (or min/max) parameter to launch and launchWithPermit and revert e.g. `StartTickChanged(st)` before burnFrom when `startTick` differs, mirroring FeeChanged. If this is accepted as a trust assumption instead, document it in the launch UX.

**Reproduction**

State: pad deployed with startTick 142600 (~635 IMD market cap, as in the tests), stampFee 500e18, bob has an open office and $STAMP approved. 1) owner: pad.setStartTick(400000) (in range, accepted). 2) bob: pad.launch("T","T","{}",500e18). Expected (from bob's side): a revert like FeeChanged, or a token at the advertised ~635 IMD start. Actual (test/scratch/Judge.t.sol::test_StartTickRace, both currency orders): launch succeeds, bob's $STAMP drops by 500000000000000000000, pad.launchTick(token) == 400000, pad.price(token) == 4 wei, pad.marketCap(token) == 3999999999 wei (4 gwei of IMD for the whole supply). 3) carol: router.buy(token, 1e9 /* 1 gwei IMD */, 1, now) returns 182253615583363540886102967 tokens (18% of the supply, more than 3x the treasury's 5% drop allocation) for 1 gwei of IMD. The same launch sequenced one slot earlier would have opened at ~635e18 wei market cap.

### 2. Low: setStampFee is unbounded and renounceOwnership has no payability guard, so a fee above what any wallet can hold halts every launch for good, contradicting the renounce NatSpec

`contracts/src/CourierPad.sol:481`

```
        stampFee = stampFee_;
```

Merged from audit_flow (low) and audit_permissions (trust-assumption item 1). setStampFee accepts any uint256; $STAMP is hard-capped at 21,000,000e18 with permanent burns, so any stampFee above the cap (or simply above the largest balance) makes launch and launchWithPermit revert for everyone, either with FeeChanged (maxStampFee below the fee) or inside burnFrom (ERC20InsufficientBalance). While an owner exists this is a reversible de facto launch pause, which is an owner power. The defect is that renounceOwnership (line 511) has no guard that the fee is payable, unlike StampHook's renounce which refuses before openPool, while its NatSpec on line 510 promises 'Launching keeps working'. After the renounce stampFee can never change, so a mistaken or hostile value set just before (or an owner-key compromise that sets fee then renounces) ends launching permanently. Trading of already-launched tokens is unaffected. Fix: bound stampFee_ in setStampFee (e.g. <= 21_000_000e18, StampToken.MAX_SUPPLY, or a protocol-chosen MAX_STAMP_FEE) and/or have renounceOwnership refuse while stampFee is unpayable, so a renounced pad really does keep launching.

**Reproduction**

State: pad deployed as in the tests. owner: pad.setStampFee(22_000_000e18); owner: pad.renounceOwnership(). bob (open office, max $STAMP approval): pad.launch("T","T","{}",22_000_000e18). Expected per the renounce NatSpec: launching keeps working. Actual (test/scratch/Judge.t.sol::test_StampFeeLocksLaunches, both orders): reverts inside burnFrom (no account can hold 22M $STAMP); with maxStampFee 500e18 it reverts FeeChanged(22000000000000000000000000). pad.owner() == address(0), setStampFee is onlyOwner, so nobody can ever lower it.

### 3. Low: TokenLaunched emits the pool-oriented tick, which is the negated launch tick whenever the token is currency0, so indexers derive the inverse start price for about half of all launches

`contracts/src/CourierPad.sol:316`

```
        emit TokenLaunched(token, msg.sender, name, symbol, metadata, id, tick, fee);
```

From audit_math. The `tick` emitted is the local `int24 tick = quoteIs0 ? st : -st;` (line 312), i.e. currency1-per-currency0 for the pool, while startTick, launchTick[token] and the setStartTick/StartTickSet documentation are all in tokens-per-IMD and store `st`. Whether a token is currency0 depends only on its address relative to IMD (0x5F7B... on mainnet, so roughly 37% of launches will have the token as currency0), so for those launches the only event that carries the launch tick carries the opposite sign of what launchTick(token) returns. An indexer or the game's own UI that reads the start price from the event gets a price of 1/p unless it also reads launches(token).quoteIsCurrency0 and flips the sign; the existing test suite never checks the event's tick. Fix: emit `st` (the documented tokens-per-IMD tick), or add a separately named pool-tick field and document the existing one as the pool tick.

**Reproduction**

Deploy the pad with IMD at an address above every PadToken's (test/scratch/Judge.t.sol JudgeImdHigh and JudgeImdMid, IMD at 2^160-0x1001 or 2^159) with startTick 142600 and call launch("T","T","{}",500e18) under vm.recordLogs. Expected: TokenLaunched.tick == launchTick(token) == 142600. Actual (test_EventTickSign): decoded event tick = -142600 while pad.launchTick(token) = 142600 and launches(token).quoteIsCurrency0 = false. With IMD at a low address (JudgeImdLow) the event and the mapping agree (142600).

### 4. Low: setFeeRecipient and setDropRecipient are single-step; after renounceOwnership a mistyped or non-receiving address permanently captures every future fee or drop

`contracts/src/CourierPad.sol:466`

```
        feeRecipient = feeRecipient_;
```

From audit_economics. Ownership deliberately moves in two steps ('so a typo can't lose the admin role', line 496), but the two value-receiving roles move in one step and only reject address(0). These are exactly the roles that must keep working after the owner is renounced (the design relies on the recipient moving itself if IMD's issuer blocks it). Once ownership is renounced the only account that can change feeRecipient is feeRecipient itself (line 464), so a wrong address set by the recipient (typo, a contract that cannot move IMD, a lost key) is final: collectProtocolFees sends every 4% fee from every pool there forever and nobody can redirect it. The same holds for dropRecipient (line 474): 5% of every future launch goes to the wrong address with no recovery. Note also that _collect pays whoever is feeRecipient at collection time, so a recipient change moves fees that accrued before it (collect is permissionless, so the outgoing recipient can flush first). Fix that keeps the recipient's post-renounce autonomy: pendingFeeRecipient/acceptFeeRecipient and the same for drops, so the new address proves it can act before it receives value. Reject address(this) and address(poolManager) as well (see the separate info finding).

**Reproduction**

1) owner: pad.renounceOwnership(). 2) feeRecipient: pad.setFeeRecipient(0x0000000000000000000000000000000000001234) succeeds. 3) feeRecipient: pad.setFeeRecipient(feeRecipient) reverts NotOwner; owner is 0 so nobody else can call it. 4) bob: router.buy(token, 1000e18, 1, now); anyone: pad.collectProtocolFees(IMD). Expected: a way to recover, as the two-step owner transfer gives the admin role. Actual (test/scratch/Judge.t.sol::test_FeeRecipientTypoIsFinal, both orders): IMD.balanceOf(0x1234) == 40e18 and every later fee goes there; treasury: setDropRecipient(0x1234) succeeds and setDropRecipient(treasury) then reverts NotOwner. Accrued-fee case (test_RecipientChangeMovesAccruedFees): 40e18 pending, owner setFeeRecipient(newR), collect: newR receives 40e18, the previous recipient 0.

### 5. Info: setDropRecipient accepts the pad itself or the PoolManager: the 5% drop of every later launch is burned or stranded instead of reaching the treasury

`contracts/src/CourierPad.sol:473`

```
        if (dropRecipient_ == address(0)) revert ZeroAddress();
```

From audit_economics. _launch transfers TOTAL_SUPPLY - POOL_SUPPLY to dropRecipient and _addLaunchLiquidity then burns whatever balance of that token the pad still holds (line 340). If dropRecipient is the pad, the 5% lands back in the pad and is burned with the rounding buffer; if it is the PoolManager, the tokens sit in the PoolManager with no delta and no claim and are unrecoverable. Only the owner or the current drop recipient can set it, so this is a misconfiguration guard, not an attack, and the launch gives no error. Fix: reject dropRecipient_ == address(this) and == address(poolManager) in setDropRecipient and the constructor (optionally DEAD too).

**Reproduction**

1) owner: pad.setDropRecipient(address(pad)) succeeds. 2) bob: pad.launch(...). Expected: 50,000,000e18 tokens at the treasury. Actual (test/scratch/Judge.t.sol::test_DropRecipientIsPad): PadToken.balanceOf(DEAD) == 50000000000000001000000304 (the 5% plus the buffer), pad balance 0, treasury 0. With setDropRecipient(address(poolManager)): the next launch leaves PoolManager holding 999999999999999998999999704 wei of the token (the pool position plus the stranded 5%).

### 6. Info: An exact-in IMD buy of 1 wei executes a zero-amount pool swap: the rounded-up fee consumes the whole input and the full-fill check still passes

`contracts/src/CourierPad.sol:360`

```
            ? FullMath.mulDivRoundingUp(amount, FEE_BPS, BPS)
```

From audit_math. For amountSpecified = -1 the fee rounds up to 1, so Hooks.beforeSwap computes amountToSwap = -1 + 1 = 0; v4's HookDeltaExceedsSwapAmount only rejects amountToSwap > 0 for exact input, and PoolManager's SwapAmountCannotBeZero ran on the original params before the hook, so Pool.swap runs with amountSpecified 0 and a (0,0) delta. afterSwap sees poolQuote = 0 and passes the full-fill test on line 394 because 0 + 1 == 1, emits Trade with tokenAmount 0, and the hook keeps the 1 wei. For 2..25 wei the same rounding charges 1 wei (50% down to 4%), which is the documented 'never less than 4%' behaviour. Economic impact is 1 wei per call, so informational; recorded because the invariant 'a fee is charged on a swap the pool actually performed' has a zero-swap exception. If wanted, revert in beforeSwap when fee >= amount for exact-in.

**Reproduction**

Launch any token; through PoolSwapTest call swap(key, SwapParams(zeroForOne = quoteIsCurrency0, amountSpecified = -1, limit = MIN_SQRT_PRICE+1 or MAX_SQRT_PRICE-1), settings(false,false), ""). Expected: revert (SwapAmountCannotBeZero or PartialFill), since the pool cannot swap 0. Actual (test/scratch/Judge.t.sol::test_OneWeiBuy, all three IMD placements): the call succeeds, the buyer's IMD balance drops by 1, token balance unchanged, pendingProtocolFees[IMD] increases by 1; a 2-wei buy then charges another 1 wei (fee 1, swap 1).

### 7. Info: price() has 1-wei-per-token resolution, so near the top of the allowed start ticks the reported price and marketCap are several percent low

`contracts/src/CourierPad.sol:559`

```
            ? FullMath.mulDiv(FullMath.mulDiv(1e18, Q96, sqrtP), Q96, sqrtP)
```

From audit_math. price() returns IMD wei per whole token as an integer. At MAX_START_TICK (400000) the true value is 1.0001^-400000 * 1e18 = 4.248 wei, which truncates to 4; marketCap multiplies the truncated figure by the supply so the error does not average out. The intermediate mulDiv values do not overflow or vanish anywhere in [-300000, 400000] in either currency order (price at -300000 is 1.067e31 wei, at 400000 it is 4). View only; nothing on-chain consumes price() or marketCap(). If off-chain consumers need accuracy near the top of the range, return the price scaled by a larger constant (e.g. 1e36) or expose sqrtPriceX96.

**Reproduction**

owner: setStartTick(400000); bob: launch. Expected: marketCap about 4.248e9 wei (1e9 tokens x 4.248 wei). Actual (test/scratch/Judge.t.sol::test_PriceResolutionAtMaxTick, both orders): pad.price(token) = 4, pad.marketCap(token) = 3999999999, a 5.8% understatement. At -300000: price = 10670457952892911130929611517541, marketCap = 1.067e40 wei, no overflow.

### 8. Info: Test gap: no suite runs a pad holding pools of both currency orders (what mainnet will have), and the burned-dust bound only holds near the configured start tick

`contracts/test/CourierPad.t.sol:211`

```
        assertLt(token.balanceOf(DEAD), 1.1e9);
```

Merged from audit_flow, audit_permissions and audit_economics. CourierPadImdFirstTest pins the mock IMD at 0x1000 and CourierPadImdSecondTest at 2^160-0x1001, so within one suite every PadToken lands on the same side of IMD. On Robinhood Chain IMD (0x5F7B...) sits mid-range, so one pad will hold pools of both orders sharing one pendingProtocolFees[IMD] ledger, one FEE_SLOT transient slot and one ERC-6909 IMD claim balance; that state is never exercised. It was checked here and the accounting is correct (see reproduction), so this is a coverage note, not a defect. Separately, the 1.1e9 bound on the burned remainder is only true near the default tick: at MAX_START_TICK one unit of liquidity is worth ~4.85e8 wei of token, so flooring the liquidity leaves ~1.46e9 wei to burn; the invariant the code guarantees (pool + DEAD == 95% of supply, pad balance 0) still holds. Suggest a mid-range IMD fixture with launches of both orders, and asserting the conservation equation rather than a tick-specific dust bound.

**Reproduction**

Mixed order (test/scratch/Judge.t.sol JudgeImdMid::test_MixedOrderFees, IMD etched at 2^159): 12 launches give 5 pools with IMD as currency0 and 7 with IMD as currency1; in each pool an exact-in router buy of 1000e18*(i+1) adds exactly 40e18*(i+1), an exact-out buy, a router sell and an exact-out sell each add at least 4% rounded up; afterwards pendingProtocolFees(IMD) == poolManager.balanceOf(pad, uint160(IMD)) and collectProtocolFees(IMD) pays exactly that to feeRecipient. Dust (test_DustAtEdges): at startTick 400000 token.balanceOf(DEAD) is 1462478968 (IMD as currency0) or 1467510800 (IMD as currency1), above the 1.1e9 asserted at line 211 for the default tick (1000000296 / 1000000304), while balanceOf(pm) + balanceOf(DEAD) == 950000000e18 at every tick tried (-300000, 0, 142600, 400000).

### 9. Info: Owner and recipient powers (trust assumptions, for the record): unbounded stampFee, start price anywhere in a ~1e31x range, one-step recipient redirection, no timelock; none reach launched tokens, poo

`contracts/src/CourierPad.sol:464`

```
        if (msg.sender != owner && msg.sender != feeRecipient) revert NotOwner();
```

Merged from audit_flow, audit_permissions and audit_economics. Powers that exist by design and were verified to be the only ones: (1) setStampFee, any value (a de facto launch pause; see the separate low on the renounce), 0 makes launches free; (2) setStartTick within [-300000, 400000] on the 200 spacing, future launches only (every tick in the range opens: liquidity ~3.1e33 at -300000 against the per-tick cap ~3.8e34, ~1.96e18 at 400000); (3) setFeeRecipient by the owner or the current fee recipient, and setDropRecipient by the owner or the current drop recipient, effective immediately and forever, including after the renounce; a recipient change also moves fees that accrued before it; (4) two-step ownership transfer and an unguarded renounce. Verified limits: no function removes or modifies the launch position (the only modifyLiquidity call is the positive one in _addLaunchLiquidity, reachable only from _launch through the pad's own unlock; unlockCallback is onlyPoolManager and the PoolManager only calls back the unlocker); nothing touches tokenOfPool, launches, launchTick, a PadToken's balances (no owner, mint, tax or blocklist) or the pad's ERC-6909 claims beyond collectProtocolFees sending exactly pendingProtocolFees to feeRecipient; beforeInitialize and beforeAddLiquidity revert for every caller (the pad's own calls skip the hook via v4's noSelfCall), so no second pool on this hook with any fee or spacing, and no outside liquidity; there is no pause on swaps. Consequences for the deployer: FEE_RECIPIENT and TREASURY are the same key in launch.env (0x7221...D566), so a compromise of it redirects 100% of future fees and 5% of every future launch with no recovery after the renounce; the treasury's 5% can be sold into a pool as soon as the first buyer has put IMD in; Trade.trader is tx.origin for swaps that do not come through the two routers; postOffice is immutable, so a migrated PostOffice would need a new pad. Nothing to fix for the design as commissioned; listed so the requester can decide on a fee cap, a timelock, or a multisig behind the recipient keys.

**Reproduction**

test/scratch/Judge.t.sol: test_NoHijack (both orders): pm.initialize of a second pool (same pair, fee 3000, spacing 60, hooks = pad) reverts; PoolModifyLiquidityTest.modifyLiquidity on the launch pool reverts; pad.unlockCallback from a non-PoolManager caller reverts NotPoolManager. After renounceOwnership: prank(feeRecipient) setFeeRecipient(x) and prank(treasury) setDropRecipient(x) succeed and cannot be undone (test_FeeRecipientTypoIsFinal; the project's own test_RecipientsCanMoveTheirOwn asserts the same as intended). setStampFee(22_000_000e18) stops every launch (test_StampFeeLocksLaunches). 40e18 pending, setFeeRecipient(newR), collect: newR gets 40e18 (test_RecipientChangeMovesAccruedFees).

---

Judge's submission `894791a4b2f5d3484fe3c72d34adec039123652da5bca5d1b966c62af671a75a`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
