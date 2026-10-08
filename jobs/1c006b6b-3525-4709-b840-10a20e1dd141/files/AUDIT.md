# Audit report

> Audit the Sherwood Uniswap v4 hook (src/Sherwood.sol): a daily leaderboard game that takes a 5% pot fee on swaps, keeps points onchain, pays the daily top 3, handles Dice Protocol randomness for flips, referral earnings and a buyback reserve. Focus areas are in README.md under "Where we'd like the most scrutiny": swap delta accounting and the buyback unlockCallback, pot/prize/referral accounting including partial forfeits (ETH out can never exceed ETH in), the flip lifecycle, points and leader bookkeeping with negative scores, and anything that could block swaps, settlement or claims.

| | |
|---|---|
| Repository | https://github.com/MirakoolDev/sherwood.git |
| Commit | `1266778edc5697cb4b13442901e27bbe569a1e22` |
| Job | `1c006b6b-3525-4709-b840-10a20e1dd141` |
| Judged | 2026-10-08 11:09 UTC |
| Findings | 1 high · 3 medium · 4 low · 1 info |

Four agents audited the code as it is at `1266778`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: Points, pot fee and flip stake come from amountSpecified, not the ETH the pool consumed: a price-limited buy scores 100 points for 0.005 ETH, receives no $PFWA and escapes the holding rules

`src/Sherwood.sol:270`

```
        uint256 ethIn = uint256(-params.amountSpecified);
```

beforeSwap derives ethIn from params.amountSpecified (what the swapper offers) and plays the move before the pool runs (line 278: _play(day, tx.origin, ethIn, hookData)). A Uniswap v4 exact-input swap stops at sqrtPriceLimitX96 (or when in-range liquidity runs out) without reverting, so the pool can consume far less than offered; the unconsumed ETH never leaves the swapper. The hook still takes the 5% pot fee on the full offered amount and scores base = ethIn / 0.001 ETH (capped at 100), scales STEAL / ROBIN_HOOD shares by it and uses the scored amount as a FLIP stake. afterSwap only records bought[day][player] += delta.amount1(), which is the dust actually received. Consequences: (1) 100 points cost 0.005 ETH of fee plus a few wei instead of 0.1 ETH, with no price impact, no LP fee and no $PFWA exposure, so the daily 50/20/10% ETH prizes (other players' fees, plus fundPot seeds) can be taken for 1/20th of the honest cost; (2) bought is 0, so the settlement forfeit (balance < owed) and MustHoldToClaim never bind for such a player, bypassing the anti-dump mechanism entirely; (3) an honest buyer whose price limit is hit, or whose buy exhausts the one-sided $PFWA range, is overcharged: the 5% fee applies to ETH that was never swapped. The sell path is asymmetric and correct (afterSwap charges 5% of the realised delta.amount0()). Fix: score and record buys from realised amounts. Move _play for buys into afterSwap and use ethIn = uint256(-delta.amount0()) + fee (the delta passed to afterSwap is the pool's swap delta, net of the fee removed in beforeSwap), and require delta.amount1() > 0; or keep _play in beforeSwap but revert in afterSwap when -delta.amount0() + fee != ethIn so partially filled buys are rejected. Charge the fee on the filled amount. Merged from four specialist reports (audit_math, audit_economics, audit_flow, audit_permissions) that all describe this one root cause.

**Reproduction**

State: the project's test setup (game pool at SQRT_PRICE_1_1, liquidity 100e18 over ticks [-60000, 60000]). Input: alice reads slot0.sqrtPriceX96 = P and calls swapRouter.swap{value: 0.1 ether} with zeroForOne=true, amountSpecified=-0.1 ether, sqrtPriceLimitX96 = P - 1, hookData abi.encode(0). Expected: points proportional to the ETH that actually bought $PFWA (0 here, at most 5 for the 0.005 ETH that left the wallet), or the swap rejected. Actual (all four specialist proofs, run by the judge from test/scratch, fail identically): ETH spent 5000000000000002 wei, PFWA received 0, points(day, alice) == 100, bought(day, alice) == 0. Repeating per transaction buys 100 points per 0.005 ETH; at settlement owed == 0 so no forfeit applies and claim pays the full prize with a zero $PFWA balance. The attached proof fails with 'points scored on ETH that never entered the pool: 100 > 5' and passes either when points follow the consumed ETH or when partial fills are rejected.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {Deployers} from "v4-core/test/utils/Deployers.sol";
import {MockERC20} from "solmate/src/test/utils/mocks/MockERC20.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {Hooks} from "v4-core/src/libraries/Hooks.sol";
import {StateLibrary} from "v4-core/src/libraries/StateLibrary.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {PoolId} from "v4-core/src/types/PoolId.sol";
import {Currency, CurrencyLibrary} from "v4-core/src/types/Currency.sol";
import {ModifyLiquidityParams, SwapParams} from "v4-core/src/types/PoolOperation.sol";
import {PoolSwapTest} from "v4-core/src/test/PoolSwapTest.sol";
import {Sherwood, IDiceEntropy} from "src/Sherwood.sol";

/// Dice stand-in that accepts requests and never reveals.
contract QuietDice {
    function getFeeV2(address, uint32) external pure returns (uint128) {
        return 25_000_000_000_000;
    }

    function requestV2(address, bytes32, uint32) external payable returns (uint64) {
        return 1;
    }

    receive() external payable {}
}

/// Points, steal share and the holding record are all derived from `params.amountSpecified`
/// (the ETH the swapper *offered*), not from the ETH the pool actually consumed. A buyer who
/// sets `sqrtPriceLimitX96` one unit below the current price offers 0.1 ETH, the pool takes
/// ~1 wei of it, the hook keeps 0.005 ETH as pot fee, and the buyer scores the full 100
/// points with ~0 $PFWA recorded in `bought`.
contract PartialFillPointsTest is Test, Deployers {
    using StateLibrary for IPoolManager;

    Sherwood hook;
    MockERC20 pfwaToken;
    PoolKey gameKey;
    address owner = makeAddr("owner");
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");

    uint160 constant FLAGS = uint160(
        Hooks.BEFORE_INITIALIZE_FLAG | Hooks.BEFORE_SWAP_FLAG | Hooks.AFTER_SWAP_FLAG
            | Hooks.BEFORE_SWAP_RETURNS_DELTA_FLAG | Hooks.AFTER_SWAP_RETURNS_DELTA_FLAG
    );

    function setUp() public {
        vm.warp(1_760_000_000);
        deployFreshManagerAndRouters();
        pfwaToken = new MockERC20("PFWA", "PFWA", 18);
        pfwaToken.mint(address(this), 1e30);
        pfwaToken.approve(address(modifyLiquidityRouter), type(uint256).max);
        QuietDice dice = new QuietDice();

        address hookAddr = address(FLAGS | (uint160(0x4444) << 144));
        deployCodeTo(
            "Sherwood.sol:Sherwood",
            abi.encode(manager, Currency.wrap(address(pfwaToken)), IDiceEntropy(address(dice)), address(1), owner),
            hookAddr
        );
        hook = Sherwood(payable(hookAddr));
        vm.prank(owner);
        (gameKey,) = initPool(CurrencyLibrary.ADDRESS_ZERO, Currency.wrap(address(pfwaToken)), IHooks(hookAddr), 3000, SQRT_PRICE_1_1);
        vm.deal(address(this), 1_000 ether);
        modifyLiquidityRouter.modifyLiquidity{value: 500 ether}(
            gameKey, ModifyLiquidityParams({tickLower: -60000, tickUpper: 60000, liquidityDelta: 100e18, salt: 0}), ""
        );
    }

    function _swap(address who, uint256 amount, uint160 limit) internal returns (bool ok) {
        vm.deal(who, amount);
        vm.prank(who, who);
        (ok,) = address(swapRouter).call{value: amount}(
            abi.encodeCall(
                PoolSwapTest.swap,
                (
                    gameKey,
                    SwapParams({zeroForOne: true, amountSpecified: -int256(amount), sqrtPriceLimitX96: limit}),
                    PoolSwapTest.TestSettings({takeClaims: false, settleUsingBurn: false}),
                    abi.encode(uint256(Sherwood.Move.BUY))
                )
            )
        );
    }

    function test_pointsFollowEthActuallySwappedNotAmountOffered() public {
        uint256 day = hook.currentDay();

        // Alice buys honestly: 0.1 ETH leaves her, 100 points, ~0.095 PFWA recorded as bought.
        require(_swap(alice, 0.1 ether, MIN_PRICE_LIMIT), "honest swap failed");
        assertEq(hook.points(day, alice), 100);
        assertGt(hook.bought(day, alice), 0.09 ether);

        // Bob offers 0.1 ETH but caps the price one unit below spot, so the pool consumes ~1 wei.
        (uint160 sqrtP,,,) = manager.getSlot0(gameKey.toId());
        uint256 managerBefore = address(manager).balance;
        uint256 hookBefore = address(hook).balance;
        bool ok = _swap(bob, 0.1 ether, sqrtP - 1);
        if (!ok) return; // a fix that rejects partial fills is also acceptable

        uint256 paid = (address(manager).balance - managerBefore) + (address(hook).balance - hookBefore);
        // Bob parted with ~0.005 ETH (the 5% pot fee on 0.1) plus dust.
        assertLt(paid, 0.0051 ether, "bob paid more than the fee");
        assertLt(hook.bought(day, bob), 1e12, "bob's recorded buys should be dust");

        // Expected: points are earned per 0.001 ETH actually swapped, so at most paid/0.001.
        // Actual on this code: 100 points, the same as alice who really spent 0.1 ETH.
        assertLe(hook.points(day, bob), int256(paid / hook.POINT_UNIT()), "points scored on ETH that never entered the pool");
    }
}
```

### 2. Medium: Flip reveals and expiries still move points after batched settlement has started, so the recorded top-3 can disagree with the day's final points and a zero-score player can be paid

`src/Sherwood.sol:442`

```
        if (_results[f.day].settled) return; // revealed after its day was settled
```

settle(day, maxPlayers) copies each scanned player's points into r.top/r.topPoints and advances r.cursor, but r.settled only becomes true after the last batch. _entropyCallback (line 442) and expireFlip (line 456) only check settled, so while r.cursor > 0 and the day is not yet settled they still _credit/_debit points[day]. A change to an already-scanned player is ignored (their stored topPoints stay), while a change to an unscanned player (e.g. the flip's `previous`, who receives a lost stake) is counted. The ranking therefore mixes pre- and post-reveal scores: a player who lost their flip after being scanned stays in the top 3 at 0 or below (breaking the 'only players above zero can place' rule), and a player credited after being scanned is under-ranked. Precondition: a flip for the day is still unrevealed at (day+1) 00:15, which the code explicitly plans for (requestV2 try/catch, FLIP_TIMEOUT); settle is permissionless so anyone can call settle(day, 1) to freeze the first entries before a known reveal or expiry, and anyone can time expireFlip after an index has been scanned. The mismatch is permanent (AlreadySettled) and prizes are paid on it. Fix: treat a day as closed once settlement has begun, i.e. have _entropyCallback and expireFlip return (only deleting the flip) when _results[f.day].cursor != 0 || settled; or keep a per-day pending-flip counter and have settle revert while it is non-zero so pending flips must be expired first. Merged from audit_math, audit_economics, audit_flow and audit_permissions.

**Reproduction**

State: day D, alice BUY 0.1 ETH (players[0], 100), bob BUY 0.06 ETH (players[1], 60), alice FLIP 0.1 ETH (stake 100, previous bob, Dice sequence 1 pending). Warp to (D+1)*1 days + 15 minutes. Input: settle(D, 1) returns false (alice scanned at 100); Dice reveals sequence 1 as odd: points(D, alice) == 0, points(D, bob) == 160; settle(D, 1) returns true. Expected: bob places #1 and alice, at 0 points, gets no prize. Actual (judge test test_A_batchedSettleRanksStalePoints): result(D).top == [bob, alice], topPoints[1] == 100, prize[1] == 2595000000000000 wei (20% of the pot) for alice.

### 3. Medium: Robin Hood can pay the mover: _lowestRecent excludes only the leader, so the move becomes a cheap, repeatable transfer from the leader to the caller

`src/Sherwood.sol:519`

```
            if (a == leader) continue;
```

_lowestRecent(day, leader) scans the last-10 ring and skips only the leader. The player making the ROBIN_HOOD move is in the ring whenever they played earlier that day (_pushRecent runs after every play), and a mover who is the lowest non-leader entry (always in a two-player game; after a lost flip; or arranged by filling the ring with ten 0.001 ETH buys from the same wallet) receives the leader's 10-33% themself. The README and NatSpec describe the move as redistribution to the lowest of the last 10 players; in practice it is a steal from the leader that STEAL cannot match (STEAL only reaches the previous player), repeatable as long as the mover stays below the leader. Impact is to points, which decide the daily ETH prizes. Fix: pass the mover into _lowestRecent and skip a == player as well as the leader; optionally skip duplicate entries so one wallet cannot fill the ring, and skip players with points <= 0 if the intent is to help a trailing positive player. Merged from audit_math (low) and audit_permissions (medium).

**Reproduction**

State: alice BUY 0.1 ETH (100, leader); bob BUY 0.001 ETH (1); recent ring = [alice, bob]. Input: bob plays ROBIN_HOOD with 0.05 ETH. Expected: bob ends at 51 and the leader's share goes to another player or nobody. Actual (judge test test_C_robinHoodPaysMover): target == bob, moved = 100 * 2150 / 10000 = 21, points(day, alice) == 79, points(day, bob) == 72. Repeat variant (test_C2_robinHoodSelfRepeat): alice 100, carol 50, then ten ROBIN_HOOD buys of 0.001 ETH by bob (0.01 ETH total) leave alice 49, bob 57, carol 54: the leader lost half their score to a 0.01 ETH spend.

### 4. Medium: The Dice fee paid from the pot is uncapped: a provider fee increase lets any FLIP send the whole day's pot to Dice

`src/Sherwood.sol:415`

```
        if (pot[day] < diceFee) return false;
```

_requestFlip pays whatever dice.getFeeV2 quotes as long as pot[day] covers it (lines 410-423). Dice is a Pyth Entropy fork whose provider sets its own fee at any time: the live Dice contract at 0xd8A0680e7699526B57140ED4EAfdCc7219Dc0A0c exposes setProviderFee(uint128) and setProviderFeeAsFeeManager(address,uint128) (the judge verified both selectors in its bytecode and read the current quote of 25000000000000 wei over RPC). The only guard is the solvency check, so after a fee change the next FLIP by any player drains the pot, which is every player's accumulated 5% fees plus fundPot seeds, up to its full size. FLIP is a permissionless move and the contract cannot distinguish a 0.000025 ETH quote from a 1 ETH quote. This is a third-party trust dependency rather than a bug in the hook's own arithmetic, but the README asks for scrutiny of 'the Dice fee taken from the pot' and the pot is the game's ETH. Fix: cap the fee accepted from the pot (an absolute constant such as MAX_DICE_FEE, or a small fraction of pot[day]) and fall back to a plain BUY when the quote exceeds it, exactly as already done when the pot cannot cover it. Reported by audit_permissions.

**Reproduction**

State: pot[day] = 1 ETH (fundPot seed); the Dice provider fee is 1 ETH (mock setFee). Input: bob swaps 0.02 ETH with hookData abi.encode(3) (FLIP). Expected: an out-of-range quote is refused and the move scores as a BUY; the pot stays 1.001 ETH. Actual (judge test test_E_diceFeeDrainsPot): pot(day) == 0.001 ETH and the Dice contract's balance == 1 ETH.

### 5. Low: Flip win multiplier scales with the bonus-inflated stake instead of base points, so holder and welcome bonuses count twice

`src/Sherwood.sol:445`

```
        uint256 amount = won ? (uint256(f.stake) * scaledBps(FLIP_WIN_BPS_MIN, FLIP_WIN_BPS_MAX, f.stake)) / 10_000 : f.stake;
```

The README and the constant comments say Steal, Robin Hood and the flip win scale linearly with the buy's base points, and STEAL / ROBIN_HOOD do pass `base` to scaledBps (test_holderBonusDoesNotRaiseStealShare checks that intent). A flip win instead passes f.stake, and stake is `scored`, i.e. base already multiplied by the holder bonus (+25%) and/or welcome bonus (+10%). The bonus therefore raises both the stake and the multiplier, reaching the 3x cap at an 0.08 ETH buy for a holder-bonus player. Fix: store base in PendingFlip (or derive it) and pass it to scaledBps. Merged from audit_economics and audit_flow.

**Reproduction**

State: alice buys 0.01 ETH on day D and still holds it on D+1 (holderBonusActive true). Input: on D+1 alice FLIPs 0.08 ETH: base 80, flips(1).stake == 100; Dice reveals even (win). Expected per spec: 100 * scaledBps(20000, 30000, 80) / 10000 = 100 * 28000 / 10000 = 280 points. Actual (judge test test_B_flipWinMultiplierUsesInflatedStake): scaledBps(..., 100) = 30000, points(D+1, alice) == 300.

### 6. Low: Claim window is anchored to the day's end, not to settlement: a day settled more than 7 days late has prizes that are instantly unclaimable and sweepable

`src/Sherwood.sol:597`

```
        if (block.timestamp > (day + 1) * 1 days + CLAIM_WINDOW) revert ClaimWindowClosed();
```

settle has no upper time bound and is permissionless, but claim rejects any call after (day+1)*1 days + CLAIM_WINDOW and sweepUnclaimed (line 630) opens at that same instant. If a day is settled later than 7 days after it ended (nobody called settle, or a large day's batches were never finished), r.prize[] is populated but no winner can ever claim: claim reverts ClaimWindowClosed and the first sweepUnclaimed moves the full prizes into the current pot. The winners lose ETH they were entitled to while the README promises 7 days to claim. The trigger is unprivileged inaction rather than an attack, but the outcome is irreversible. Fix: record a settlement timestamp in Result and measure CLAIM_WINDOW (and sweep eligibility) from max(dayEnd, settledAt); or refuse to settle once the claim window would already be closed and roll such a day over explicitly. Merged from audit_math and audit_permissions.

**Reproduction**

State: day D, alice BUY 0.1 ETH (only player). Nobody settles. Input: warp to (D+1)*1 days + 7 days + 1; settle(D, 100) returns true with result(D).prize[0] > 0; alice calls claim(D); anyone calls sweepUnclaimed(D). Expected: alice has a window to claim. Actual (judge test test_D_lateSettlementUnclaimable): claim reverts ClaimWindowClosed, sweepUnclaimed succeeds immediately and pot[currentDay()] grows by prize[0].

### 7. Low: Leader cache freezes for the rest of the day once stale with more than MAX_LEADER_SCAN players; Robin Hood then keeps draining a non-leader

`src/Sherwood.sol:490`

```
        if (n > MAX_LEADER_SCAN) return _leader[day]; // too big to rescan inside a swap; keep the cached one
```

_debit sets _leaderStale[day] whenever the cached leader loses points. _currentLeader clears the flag only by rescanning and skips the rescan without clearing it when _players[day].length > 1500 (line 490), while _credit (line 473) refuses to update the cache while the flag is set. So after one debit of the leader on a day with more than 1500 joined players the leader address is frozen until midnight: every later ROBIN_HOOD move debits the stale address (who may already have been wiped by a sell, in which case the move silently does nothing), the actual leader is immune, and the leader(day) view used by the site is wrong. The README accepts a bounded rescan, but the incremental tracking does not need to stop with it. Reaching the state costs 1501 distinct 0.001 ETH buys (about 0.075 ETH of fees; the $PFWA is kept) plus gas for the wallets, or simply a busy day. Fix: in _credit keep comparing against the cached leader even when stale (if (leader == address(0) || updated > points[day][leader]) _leader[day] = player;), and/or have _currentLeader return address(0) when the rescan is skipped so Robin Hood does nothing rather than hitting a known-stale target. Reported by audit_permissions as medium; kept at low for the >1500-player precondition.

**Reproduction**

State: alice BUY 0.1 ETH (100, leader); 1501 distinct wallets each BUY 0.001 ETH (playerCount == 1502); carol ROBIN_HOOD 0.01 ETH (alice 88, cache stale); bob BUY 0.1 ETH (bob 100 is now the top score). Input: dave plays ROBIN_HOOD 0.1 ETH. Expected: alice, no longer the leader, keeps 88 and the move targets bob or nobody. Actual (judge test test_F_leaderFreezes): leader(day) still returns alice, points(day, alice) == 59, points(day, bob) == 100.

### 8. Low: ETH refunded by Dice outside refundDiceRequest is dropped by receive() and stuck in the contract

`src/Sherwood.sol:220`

```
        if (msg.sender != address(poolManager) && msg.sender != address(dice)) _seed(currentDay(), msg.value);
```

receive deliberately ignores ETH from Dice because refundDiceRequest measures the balance change itself. But the live Dice contract exposes refundRequest(address,uint64) as a public function (selector 0x361e02a7 is present in its bytecode; the project's own MockDice lets anyone call it). If a refund for one of the hook's sequences is triggered by any path other than the operator's refundDiceRequest (a third party, a keeper, or Dice's own expiry logic), the ETH arrives through receive with msg.sender == dice, is neither seeded into the pot nor added to buybackReserve, and a later refundDiceRequest for the same sequence finds nothing to credit. The ETH stays in the contract with no path out. The amount is one Dice fee per request (0.000025 ETH today; see the uncapped-fee finding for how large it can become). Whether Dice allows a non-requester to trigger the refund could not be verified (no verified source is published for chain 4663), so the third-party trigger is a plausible but unconfirmed precondition; the dropping of Dice ETH in receive is confirmed. Fix: credit ETH received from Dice in receive (to buybackReserve, matching refundDiceRequest) instead of ignoring it, and have refundDiceRequest rely on that path rather than a balance diff. Reported by audit_permissions.

**Reproduction**

State: alice plays FLIP 0.02 ETH; the pot pays 0.000025 ETH to Dice for sequence 1. Input: any address calls dice.refundRequest(provider, 1) directly and Dice sends the fee back to the hook. Expected: the refunded 0.000025 ETH is accounted (buybackReserve or pot). Actual (judge test test_G_diceRefundOutsideOperatorPathIsUnaccounted): address(hook).balance grows by 25000000000000 wei while pot(day) and buybackReserve are unchanged; the operator's refundDiceRequest(1) afterwards credits nothing.

### 9. Info: Trust assumption: the owner can route the buyback reserve to themself via setBuybackPool plus minPfwaOut = 0, contrary to the README's 'cannot' column

`src/Sherwood.sol:694`

```
        if (PoolId.unwrap(key.toId()) == PoolId.unwrap(poolId) || address(key.hooks) == address(this)) {
```

The README's roles table says the owner cannot touch funds and the operator cannot send reserve ETH anywhere but the buyback swap. In code, setBuybackPool accepts any ETH/$PFWA pool whose hook is not Sherwood and whose id is not the game pool, and buybackAndBurn lets the caller pick minPfwaOut (0 allowed). An owner-created pool with a hook that returns a beforeSwapDelta claiming almost the whole specified ETH and takes it makes unlockCallback settle ethPaid == amount while pfwaOut is dust, which passes minOut 0; independently, minPfwaOut = 0 lets the operator sandwich their own buyback in the holder pool. This is a privileged-actor power, not a permission bypass, and is reported so the roles table can be corrected or the power narrowed. Possible narrowing that keeps the design: pin the buyback pool once (set-once like poolId) or restrict its hook to address(0) or an allow-list, and enforce a minimum output derived from the holder pool's price. Reported by audit_permissions.

**Reproduction**

Code trace: setBuybackPool (lines 690-699) checks only currency0 == ETH, currency1 == pfwa, id != poolId and hooks != this; buybackAndBurn (line 646) accepts minPfwaOut == 0 and unlockCallback (lines 655-668) uses the returned swap delta as ethPaid/pfwaOut with no external price check. Input: owner calls setBuybackPool(key) with key.hooks a hook returning toBeforeSwapDelta(int128(amount - 1), 0) that takes amount - 1 ETH, then buybackAndBurn(R, 0). Expected per README: reserve ETH can only be swapped for $PFWA and burned. Actual: ethPaid == R is settled to the PoolManager, which credits R - 1 to the owner's hook; BuybackBurned is emitted with a dust burn. Not executed as a test (info-level trust assumption).

---

Judge's submission `334b2a757958b206e83e253dcc451557ed30eec8a02f5ac0db59078943d2200c`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
