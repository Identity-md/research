# Audit report

> Audit the Pepes token (0xE2C46c7068566740A33A4C93f5445B07BCfE5644, Robinhood Chain), an instance of contracts/src/PadToken.sol launched by the PepesFamily v1 launchpad (0x2d7689E48Fd71D9A0f225C673D7b8F8A693368CC). This branch is the v1 code exactly as deployed and verified.
>
> What it is: a fixed-supply (1B) token. The whole supply is locked as Uniswap v4 liquidity that can't be removed, and the launchpad's v4 hook takes 4% of every swap (1% protocol, 3% to holders). No mint, no owner, no admin functions.
>
> GoPlus/GMGN show three warnings. For each, tell us if it's a real risk or a false positive:
>
> Possible honeypot: can anyone block selling?
> Owner can change balance: can any privileged address change or move holders' balances?
> Has suspicious function: does any non-standard function give someone special power?
> Look hardest at:
> (1) PadToken.transferFrom skipping the allowance when msg.sender is the immutable v1 router. We think this triggers warnings 1 and 2. Confirm every router path (buy, sell, launch, unlockCallback) can only pull from its own caller.
> (2) Every non-standard token function (claim, distribute, isExcluded, the reward getters, receive). Confirm none is privileged, and identify which one scanners likely flag.
> (3) Whether any owner action or third-party call can make sells or claims revert.
> (4) Reward accounting never paying out more than was distributed.
>
> Full list of functions and details are in AUDIT.md.
>
> What's new in the branch's AUDIT.md:
>
> All three warnings listed, each with a request for a "real risk or false positive" verdict.
> Every non-standard function the token has, grouped and explained, with a request to confirm none is privileged and to say which one scanners likely flag:
> Holder rewards: claim, distribute and the read-only reward getters.
> Info: isExcluded, metadata, pad, router, poolManager, quote, creator.
> receive().
> A note that we believe one pattern triggers both the balance warning and the honeypot warning: the router's approval shortcut.
> The branch is now at commit 8c1869c. If the audit tool reads it at check time, it picks up this version automatically.

| | |
|---|---|
| Repository | https://github.com/0xtenang/PepesFamily.git |
| Commit | `8c1869c1af94cfea5b4b5c40bd2178c3b4c08a0c` |
| Job | `46a0c47b-d3ad-4c50-973e-369203a488ce` |
| Judged | 2026-10-01 07:35 UTC |
| Findings | 1 high · 1 medium · 3 low · 6 info |

Four agents audited the code as it is at `8c1869c`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: Anyone can flash-take the pool's tokens inside a PoolManager unlock and collect holder rewards without holding or paying anything

`contracts/src/PadToken.sol:148`

```
    function distribute() public returns (uint256 amount) {
```

distribute() spreads newly arrived quote over eligibleSupply as it stands at that instant (PadToken.sol:150-154). The PoolManager is on the exclusion list (line 141), so the tokens locked in the pool are meant to earn nothing. But Uniswap v4 flash accounting lets any address that calls poolManager.unlock() call poolManager.take(token, self, X) for the PoolManager's whole token balance, provided it is returned before the unlock ends. That take is a PoolManager -> caller ERC-20 transfer, so _transfer() adds X to eligibleSupply (line 132) and the caller is a dividend-eligible "holder" of roughly half the supply for the length of one call, with no swap, no 4% fee and no capital. A distribution can be triggered in that window by anyone, three ways: PadToken.distribute() is public; PepesFamily.flush() runs _flush() inline for any caller when poolManager.isUnlocked() (PepesFamily.sol:354); PadToken.claim() calls pad.flush() first (PadToken.sol:176) and then pays the caller. The caller then transfers the tokens back, settles, and keeps the quote. Merged from the audit_permissions specialist finding (a851bb53); no proof was attached there, the one here is mine.

What can be taken: (a) pendingHolderFees[token], i.e. the 3% holder share of every swap that did not go through PepesFamilyRouter/PepesFamilyEthRouter (Universal Router, aggregators, trading bots); AUDIT.md lists "fees from trades through other routers reach holders at the next flush" as known behaviour, and this is what makes that window exploitable; (b) any quote sitting in the token contract above accountedBalance (first-buy fee waiting for eligibleSupply >= 1 token, donations); (c) a trader's own fee: a trader who swaps inside its own unlock gets most of its own 3% holder fee straight back, so the effective fee is about 1.5% instead of 4%, against the README statement (line 22) that a trader does not earn from their own trade and against AUDIT.md's "dividend sniping costs 4% in and 4% out". Who loses: every real holder, pro rata. What is not affected: token balances, the ability to sell, already-accrued (accounted) rewards (the receiver's correction at line 131 cancels past accrual), and the protocol 1%. It is not an owner or privileged power; it is permissionless. Live state read with cast call at about Robinhood Chain block 77197460: the PoolManager held 481,186,191.98 Pepes against eligibleSupply 518,813,808.02, so a flash-take gets 48.1% of whatever is distributed, and pad.pendingHolderFees(Pepes) was 2.454178224066759594 IMD un-flushed, i.e. about 1.18 IMD capturable in a single call at that moment, recurring with every third-party-router trade. I did not run the attack against the chain or a fork; the reproduction is local.

Fix that keeps the design: do not let a distribution happen while the PoolManager is unlocked by an untrusted caller. For example, PepesFamily.flush() runs _flush() inline only when msg.sender is a trusted router and otherwise leaves the fees pending, and PadToken.distribute() returns 0 when msg.sender != pad and the PoolManager is unlocked. I applied exactly that as a temporary local patch: both proof tests and the 25 existing tests pass with it (sources restored afterwards). PepesFamilyEthRouter would need to be on the trusted list to keep its inline flush. The deployed v1 token and pad are immutable, so for Pepes itself the only mitigation is operational: keep pendingHolderFees at zero by calling pad.flush(token) outside an unlock promptly after third-party trades (anyone can), which leaves nothing to capture; that does not close variant (c).

**Reproduction**

Local PoolManager, IMD-quoted launch (start cap 100 IMD), run from contracts/: forge test --match-path test/scratch/FlashDividendSnipe.t.sol -vv. Test 1: bob buys 10 IMD twice through PepesFamilyRouter (only real holder, nothing waiting); carol buys 100 IMD through PoolSwapTest (stand-in for a third-party v4 router), so pad.pendingHolderFees(token) == 3e18. Attacker contract holds 0 tokens and 0 IMD. It calls poolManager.unlock(); in unlockCallback: poolManager.take(token, attacker, token.balanceOf(poolManager)); token.claim(); poolManager.sync(token); token.transfer(poolManager, same amount); poolManager.settle(). Expected: attacker ends with 0 IMD and bob+carol's withdrawable rises by 3e18. Actual: attacker ends with 1408165773704161705 wei IMD (1.408 of the 3 IMD, 47%) and still 0 tokens; the test fails with "a non-holder with no capital captured holder rewards: 1408165773704161705 != 0". Test 2: bob makes one 10 IMD router buy, so 0.3e18 IMD waits un-accounted in the token; the attacker does take -> token.distribute() -> return inside its unlock, then token.claim() afterwards. Expected 0; actual 274172264672444690 wei IMD (91% of the 0.3 IMD that belonged to bob). Variant (c), separate scratch test: a contract buys 100 IMD inside its own unlock, takes the PoolManager's whole token balance, calls claim(), returns the flash-borrowed part: it gets 2524391587445605893 wei IMD back in the same transaction (84% of its own 3 IMD holder fee); bob, the only prior holder, receives 475608412554394107 wei instead of 3e18.

### 2. Medium: Hook fee on quote-specified swaps (exact-in buy, exact-out sell) is computed from the requested amount, so a partially filled swap pays far more than 4% or reverts

`contracts/src/PepesFamily.sol:294`

```
        uint256 fee = exactIn ? (amount * FEE_BPS) / BPS : (amount * FEE_BPS) / (BPS - FEE_BPS);
```

Merged from three specialist findings on this line (audit_math c29230d5, audit_permissions 1d1e2d36, audit_economics 616601b3); both attached proofs were run and fail for the stated reason. When the quote asset is the swap's specified currency, beforeSwap computes the fee from params.amountSpecified, books it immediately (_chargeFee mints claims and raises pendingProtocolFees/pendingHolderFees) and returns it as the BeforeSwapDelta. Uniswap v4 does not revert a swap that stops at sqrtPriceLimitX96 or runs out of liquidity; it fills what it can, and the full hook delta is still applied to the trader. afterSwap reads the fee back from the transient slot (lines 318-322) without comparing it with the quote that actually moved, so the trader pays requested*400/10000 (buy) or requested*400/9600 (sell) on quote that never changed hands. If the fee exceeds the delivered quote on an exact-out sell, `poolQuote - fee` at line 334 underflows and the swap reverts. The documented rule (4% of the quote side of every swap) and the Trade event are wrong for these swaps. Reach: swaps through any router that passes a real price limit or an exact-out request larger than the pool's quote reserve (PoolSwapTest in this repo, custom v4 integrations). PepesFamilyRouter and PepesFamilyEthRouter only do exact-in with the extreme limits, so the app's own paths are affected only in the unreachable case of a buy that runs to the end of the curve. The excess goes to holders (3/4) and the protocol (1/4), not to an attacker directly, although whoever moves the price up to a victim's limit first would hold tokens and share in the excess (reasoned, not tested). It does not block ordinary sells: exact-in sells are charged in afterSwap from the real output. Severity medium: direct loss for the trader, up to most of the proceeds, but only on trader-chosen parameters outside the project's routers. Fix that keeps the design: in afterSwap, in the quote-specified branch, require the actual quote delta to equal what beforeSwap assumed (requested - fee for exact-in, requested + fee for exact-out) and revert otherwise (e.g. PartialFill()). I applied that locally as a temporary patch: all three proof tests pass and the 25 existing tests still pass.

**Reproduction**

ETH-quoted launch at the test start tick; bob buys 1 ETH through PepesFamilyRouter (pool holds 0.96 ETH). Run from contracts/: forge test --match-path test/scratch/PartialFillFee.t.sol -vv (the audit_math proof with the DeployLib helpers inlined so the file is self-contained; logic unchanged). Case A, exact-out sell via PoolSwapTest: zeroForOne=false, amountSpecified=+10e18, sqrtPriceLimitX96 half-way back to the launch price. Pool pays out 594713003907107236 wei. Expected fee: 4% of that = 23788520156284289 wei. Actual fee: 416666666666666666 wei (10e18*400/9600, 70% of the gross); bob receives 178046337240440570 wei. Test fails: "fee exceeds 4% of the gross the pool actually paid: 416666666666666666 > 23788520156284290". Case B, exact-in buy: zeroForOne=true, amountSpecified=-10e18 with 10 ETH attached and a limit a little past the current price. Bob pays 1539233323399973647 wei in total. Expected fee: 61569332935998946 wei. Actual: 400000000000000000 wei (26%). Test fails: "fee exceeds 4% of the gross the buyer actually paid: 400000000000000000 > 61569332935998946". The audit_economics proof (2 ETH exact-out, limit 200 ticks short of launch) also fails as stated: fee 83333333333333333 > 37823967403430027.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {PoolSwapTest} from "v4-core/src/test/PoolSwapTest.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {FullMath} from "v4-core/src/libraries/FullMath.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {SwapParams} from "v4-core/src/types/PoolOperation.sol";

import {PepesFamily} from "src/PepesFamily.sol";
import {PepesFamilyRouter} from "src/PepesFamilyRouter.sol";
import {PadToken} from "src/PadToken.sol";

/// @notice When the quote asset is the swap's *specified* currency (exact-in buy, exact-out sell) the hook computes
///         its fee in `beforeSwap` from `params.amountSpecified`, the amount the trader *asked* for. If the pool
///         fills only part of that amount (price limit reached, or the pool's quote reserve exhausted) the fee is
///         still taken in full, so the trader pays far more than 4% of the quote that actually moved.
///         Both tests fail on the current code. They pass once the hook either charges 4% of the actual gross or
///         rejects partially filled swaps of these two kinds.
contract ExactOutSellFeeTest is Test {
    PoolManager pm;
    PepesFamily pad;
    PepesFamilyRouter router;
    PoolSwapTest extRouter;
    PoolSwapTest.TestSettings settings = PoolSwapTest.TestSettings({takeClaims: false, settleUsingBurn: false});

    address alice = makeAddr("alice");
    address bob = makeAddr("bob");
    address owner = makeAddr("owner");
    address feeRecipient = makeAddr("feeRecipient");
    address imd = makeAddr("imd"); // never touched: the pool under test is ETH-quoted

    PadToken t;
    PoolKey key;
    uint160 sqrtStart; // launch price = top of the pool's single-sided range (quote is currency0)

    function setUp() public {
        pm = new PoolManager(address(this));
        extRouter = new PoolSwapTest(pm);
        int24 ethStartTick = _startTickForMarketCap(1.5 ether);
        bytes memory initCode = abi.encodePacked(
            type(PepesFamily).creationCode,
            abi.encode(pm, imd, owner, feeRecipient, ethStartTick, _startTickForMarketCap(100e18))
        );
        (bytes32 salt, address expected) = _mineSalt(address(this), _flags(), initCode);
        address deployed;
        assembly {
            deployed := create2(0, add(initCode, 0x20), mload(initCode), salt)
        }
        require(deployed == expected, "hook address");
        pad = PepesFamily(deployed);
        router = PepesFamilyRouter(payable(pad.router()));
        vm.deal(bob, 100 ether);

        vm.prank(alice);
        t = PadToken(payable(pad.launch("Test", "TST", "", address(0))));
        key = pad.poolKey(address(t));
        sqrtStart = TickMath.getSqrtPriceAtTick(ethStartTick); // ETH is currency0, so the tick is not flipped

        // bob buys with 1 ETH through the native router: 0.96 ETH enters the pool, 0.04 ETH is fee.
        vm.prank(bob);
        router.buy{value: 1 ether}(address(t), 1 ether, 0, block.timestamp);
        vm.prank(bob);
        t.approve(address(extRouter), type(uint256).max);
    }

    function _flags() internal pure returns (uint160) {
        return uint160((1 << 13) | (1 << 11) | (1 << 7) | (1 << 6) | (1 << 3) | (1 << 2));
    }

    function _fees() internal view returns (uint256) {
        return pad.pendingProtocolFees(address(0)) + pad.pendingHolderFees(address(t));
    }

    /// @dev A price limit half-way back to the launch price: the pool can return roughly half of its 0.96 ETH.
    function _halfWayLimit() internal view returns (uint160) {
        uint160 sqrtP = pad.getTokenInfo(address(t)).sqrtPriceX96;
        return sqrtP + (sqrtStart - sqrtP) / 2;
    }

    /// @notice Exact-output sell: bob asks for 10 ETH, the pool stops at the price limit after paying ~0.5 ETH.
    ///         `beforeSwap` charged 10e18 * 400 / 9600 = 0.4167 ETH, so bob keeps ~0.08 ETH of the ~0.5 ETH gross.
    function test_exactOutSell_partialFill_feeIsFourPercentOfActualGross() public {
        uint160 limit = _halfWayLimit();
        uint256 ethBefore = bob.balance;
        uint256 feeBefore = _fees();
        vm.prank(bob);
        try extRouter.swap(key, SwapParams(false, int256(10 ether), limit), settings, "") {
            uint256 received = bob.balance - ethBefore;
            uint256 fee = _fees() - feeBefore;
            uint256 grossPaidByPool = received + fee;
            emit log_named_uint("gross the pool paid out (wei)", grossPaidByPool);
            emit log_named_uint("fee taken (wei)", fee);
            emit log_named_uint("seller received (wei)", received);
            assertLe(fee, (grossPaidByPool * 4) / 100 + 1, "fee exceeds 4% of the gross the pool actually paid");
        } catch {
            // Rejecting the partially filled swap is an acceptable fix: the 4% rule is then never broken.
        }
    }

    /// @notice Exact-input buy: bob offers 10 ETH with a price limit; the pool takes only ~1.1 ETH more but
    ///         `beforeSwap` charged 10e18 * 400 / 10000 = 0.4 ETH, so bob pays ~1.5 ETH for ~1.1 ETH of tokens.
    function test_exactInBuy_partialFill_feeIsFourPercentOfActualGross() public {
        // Limit: a price a little further along the curve than the current one (buying moves the price down).
        uint160 sqrtP = pad.getTokenInfo(address(t)).sqrtPriceX96;
        uint160 limit = sqrtP - (sqrtStart - sqrtP) / 2;
        uint256 ethBefore = bob.balance;
        uint256 feeBefore = _fees();
        vm.prank(bob);
        try extRouter.swap{value: 10 ether}(key, SwapParams(true, -int256(10 ether), limit), settings, "") {
            uint256 paid = ethBefore - bob.balance; // PoolSwapTest refunds what the pool did not take
            uint256 fee = _fees() - feeBefore;
            emit log_named_uint("gross the buyer paid (wei)", paid);
            emit log_named_uint("fee taken (wei)", fee);
            assertLe(fee, (paid * 4) / 100 + 1, "fee exceeds 4% of the gross the buyer actually paid");
        } catch {
            // Rejecting the partially filled swap is an acceptable fix.
        }
    }

    // ------------------------------------------------------------ helpers (inlined copies of the deploy-script helpers)

    function _startTickForMarketCap(uint256 marketCap) internal pure returns (int24 tick) {
        uint256 sqrtPriceX96 = _sqrt(FullMath.mulDiv(1_000_000_000e18, 1 << 192, marketCap));
        tick = TickMath.getTickAtSqrtPrice(uint160(sqrtPriceX96));
        int24 rem = tick % 200;
        tick -= rem < 0 ? rem + 200 : rem;
    }

    function _mineSalt(address deployer, uint160 flags, bytes memory initCode)
        internal
        pure
        returns (bytes32 salt, address hook)
    {
        bytes32 h = keccak256(initCode);
        for (uint256 i = 0; i < 500_000; i++) {
            hook = address(uint160(uint256(keccak256(abi.encodePacked(bytes1(0xff), deployer, bytes32(i), h)))));
            if (uint160(hook) & 0x3FFF == flags) return (bytes32(i), hook);
        }
        revert("no salt");
    }

    function _sqrt(uint256 x) internal pure returns (uint256 z) {
        if (x == 0) return 0;
        z = x;
        uint256 y = (x >> 1) + 1;
        while (y < z) {
            z = y;
            y = (x / y + y) >> 1;
        }
    }
}
```

### 3. Low: claim() does not distribute quote already waiting in the token when no hook fees are pending

`contracts/src/PadToken.sol:176`

```
        IPadFlush(pad).flush(address(this));
```

claim() relies on PepesFamily.flush(token) to reach distribute(), but flush returns at once when pendingHolderFees[token] == 0 (PepesFamily.sol:353) and claim() never calls distribute() itself. Quote already in the token contract above accountedBalance is therefore not credited by a claim. That state arises in the normal flow: the router flushes before the first buyer receives tokens, eligibleSupply is 0 < MIN_ELIGIBLE_SUPPLY, distribute() returns 0 and the 3% waits; the same holds for donations. Nothing is lost: the next flush with pending fees, or anyone calling distribute(), credits it to the holders at that moment. Effect: withdrawableDividendOf and claim() under-report until then, and the waiting amount is exposed to the flash-take in the high finding for longer. Fix: call distribute() in claim() after the flush (subject to the guard the high finding needs).

**Reproduction**

Run in a scratch test on this tree: ETH-quoted launch; bob buys 1 ETH through PepesFamilyRouter. After it, token balance minus accountedBalance = 30000000000000000 wei and pad.pendingHolderFees(token) == 0. Send 1 ETH to the token. bob calls claim(). Expected: 1.03 ETH (he is the only holder). Actual: returns 0. Anyone calls distribute(); bob calls claim() again: returns 1029999999999999999 wei.

### 4. Low: Zero-value transferFrom from the zero address succeeds and emits a mint-shaped Transfer event

`contracts/src/PadToken.sol:119`

```
        if (to == address(0)) revert InvalidRecipient();
```

_transfer rejects to == address(0) but not from == address(0), and with amount == 0 the allowance check in transferFrom passes for any caller (0 < 0 is false, line 108). Anyone can call transferFrom(address(0), X, 0) and the token emits Transfer(0x0, X, 0), which indexers and scanners read as a mint event on a token that advertises no mint. No balance, supply or reward value changes (all deltas are 0), so there is no fund impact. Zero-value transferFrom between two real addresses without allowance also succeeds, but that matches ERC-20 and OpenZeppelin behaviour and is not a defect. Fix: `if (from == address(0)) revert` in _transfer (OpenZeppelin's ERC20InvalidSender); no effect on fees, rewards or the router shortcut. Deployed tokens cannot be changed; relevant for v2.

**Reproduction**

Scratch test on this tree: carol (no tokens, no allowance) calls token.transferFrom(address(0), bob, 0). Expected: revert. Actual: returns true and emits Transfer(from=0x0000000000000000000000000000000000000000, to=bob, value=0) from the token (checked with vm.expectEmit). Control: token.transferFrom(bob, carol, 1) by carol reverts InsufficientAllowance.

### 5. Low: test_everyoneCanExit compares marketCap with itself, so the sell-out price check can never fail

`contracts/test/PepesFamily.t.sol:361`

```
        assertApproxEqRel(pad.marketCap(address(t)), pad.marketCap(address(t)), 0);
```

Both arguments of the assertion are the same view call evaluated against the same state, so it passes for any pool price. This is the suite's only check of the state where every holder has left and the price is back at the edge of the single-sided range. Fix: read `uint256 mc0 = pad.marketCap(address(t));` before the buys and assert the post-exit value against mc0 with a small tolerance. Edges the suite does not cover at all and that this review exercised with throwaway tests: distribution triggered while pool tokens are flash-taken (the high finding), partially filled quote-specified swaps (the medium finding), re-entry from a seller during the router's ETH payout, a feeRecipient that rejects ETH, zero-value transferFrom from the zero address.

**Reproduction**

Read contracts/test/PepesFamily.t.sol:361: assertApproxEqRel(pad.marketCap(address(t)), pad.marketCap(address(t)), 0). Left and right are the same expression, so for any price P the assertion evaluates P == P. Expected: a check that fails if the exits leave the price away from the launch price. Actual: cannot fail; the test passes on this tree and would pass with any afterSwap or liquidity change that shifted the final price.

### 6. Info: Verdict, "owner can change balance": false positive. The only allowance-free spender is the immutable router, and it can only pull from its own caller

`contracts/src/PadToken.sol:105`

```
        if (msg.sender != router) {
```

Merged from audit_flow 34ed83a8 and audit_economics 6bc72e1c. The token has no owner. The only way a balance moves without the holder's own call or allowance is transferFrom when msg.sender == router (immutable; on chain Pepes.router() returns 0xA73604EA3C393B47573986ff9Ce5A9EAb61883dC, equal to pad.router()). Router paths: buy, sell and launch all reach _swap, which sets SwapData.user = msg.sender (PepesFamilyRouter.sol:105) and passes it to poolManager.unlock (line 112). The router has exactly one transferFrom site (line 142) and it pulls from d.user. unlockCallback is gated to the PoolManager (line 119), and the PoolManager only calls back the address that called unlock with the bytes that address supplied, so d.user is always the router's own caller. A nested unlock reverts, so re-entry during the ETH payout cannot start a second swap. The currency pulled comes from pad.poolKey(token), which reverts UnknownToken for anything the launchpad did not deploy, so a crafted token or key cannot redirect the pull. launch() passes msg.sender as creator and then uses the same _swap. The router has no owner, no setter, no delegatecall and no arbitrary call. The launchpad, its owner, the PoolManager, the creator and PepesFamilyEthRouter (line 137 there) all need a normal allowance. This is very likely what triggers both the balance warning and the honeypot warning: a transferFrom branch keyed on a fixed address that skips the allowance. Trust assumption to state publicly: the router bytecode is a permanent allowance-free spender for every PadToken; it is 150 lines, immutable and reviewed here, and nobody can change it.

**Reproduction**

Scratch test on this tree (test_routerCanOnlyPullFromItsCaller): bob and carol hold tokens. (a) alice, with no tokens, calls router.sell(token, bobBalance, 0, deadline): reverts, bob's balance unchanged. (b) vm.prank as the pad, the PoolManager, the pad owner and the token creator, each calling token.transferFrom(bob, self, 1): all revert InsufficientAllowance. (c) router.unlockCallback called directly: reverts NotPoolManager. (d) a seller contract that, while receiving ETH inside the router's unlock, calls router.unlockCallback(SwapData{user: bob,...}), poolManager.unlock(...) and router.sell(...): all three revert, bob's balance unchanged, the seller's own sale completes. Expected: nobody but the holder moves the holder's tokens without allowance. Actual: same. Existing test_attack_cannotSellSomeoneElsesTokens also passes.

### 7. Info: Verdict, "possible honeypot": false positive. No owner action, third-party call or reachable state makes a sell or a claim revert

`contracts/src/PepesFamilyRouter.sol:148`

```
        pad.flush(d.token);
```

Merged from audit_flow 6eaffad9 and audit_economics 79ceaf98. Sell path dependencies: PadToken._transfer checks only to != 0 and balance; there is no pause, blacklist, max-tx or cooldown and the exclusion list has no setter. The hook charges 4% of the real quote output of an exact-in sell in afterSwap; its only revert is a SafeCast on a fee above 2^127. Router sells then call pad.flush (this line), which burns the pad's own ERC-6909 claims (mint and burn amounts match one to one, nobody else can move them), takes quote to the token and calls distribute(), which returns 0 instead of reverting when the balance is at or below accountedBalance or eligibleSupply is under 1 token. Arithmetic bounds: `magnifiedDividendPerShare * amount` in _transfer reverts only above 2^255 = 5.79e76; on chain Pepes has magnifiedDividendPerShare = 8.687e31, so a transfer of the whole 1e27 supply gives 8.7e58; reaching the bound needs about 1.7e29 wei of cumulative quote distributed at the 1-token eligibility floor, against an IMD totalSupply on this chain of 3.657e22 wei. Owner powers (setFeeRecipient, setStartTick, two-step ownership) are not on the sell or claim path; a feeRecipient that rejects ETH only makes collectProtocolFees revert. Sells through other v4 routers never call flush. Why scanners flag it: the only liquidity is a Uniswap v4 pool behind a hook, which a honeypot simulator generally cannot route a sell through, plus the router branch in transferFrom. Caveats that are not honeypot behaviour: router sells with zero quote output revert Slippage by design; the fix for the high finding must keep flush non-reverting on the router path; IMD is an external LayerZero OFT with an owner, and its deployed bytecode contains none of the pause/paused/unpause/blacklist selectors I searched for (0x8456cb59, 0x5c975abb, 0x3f4ba83a, 0xf9f92be4, 0xfe575a87), so IMD transfers cannot be frozen by the code as deployed today, but IMD is out of scope here.

**Reproduction**

Scratch test on this tree (test_ownerAndThirdPartiesCannotBlockSellOrClaim), one ETH-quoted and one IMD-quoted token, bob and carol holding both: the owner sets feeRecipient to a contract that reverts on ETH, sets both start ticks to extreme values and starts an ownership transfer; a third party sends ETH to the ETH-quoted token, IMD to the IMD-quoted token and to the pad, and calls distribute() and flush() on both. Then bob and carol each claim on both tokens and sell 100% of both through PepesFamilyRouter. Expected: all sells and claims succeed. Actual: all succeed, final balances 0; only collectProtocolFees(ETH) reverts while the bad feeRecipient is set. Existing test_everyoneCanExit and test_attack_distributeNeverBlocksTradesOrClaims pass. Live values quoted above were read with cast call at about block 77197460.

### 8. Info: Verdict, "has suspicious function": false positive as to privilege. No non-standard function gives any address special power; claim() is the one scanners most likely flag

`contracts/src/PadToken.sol:173`

```
    function claim() external returns (uint256 amount) {
```

Merged from audit_flow d9e40c99 and audit_economics 70df85b0. State-changing externals on the token: transfer, approve, transferFrom, distribute, claim, receive. The only msg.sender comparison in the contract is the router check in transferFrom (line 105); there is no owner, role, initializer, setter, delegatecall, selfdestruct or proxy slot. claim() pays only msg.sender's own withdrawableDividendOf, debits withdrawnDividends and accountedBalance before the transfer and is guarded by _locked. distribute() is permissionless and only converts quote already in the contract into per-share accrual. isExcluded is a comparison against six fixed addresses with no storage. pad, router, poolManager, quote, creator are immutable; name, symbol, metadata are written once in the constructor. receive() reverts for Pepes because its quote is IMD. The getters are views. Most likely flagged: claim(), a non-ERC-20 external function that calls another contract and sends ETH or a token out to the caller (it pattern-matches a hidden withdraw); distribute() second; the transferFrom router branch is covered by the balance warning. Reward accounting (brief item 4): the sum of holders' withdrawable amounts never exceeded accountedBalance, which never exceeded the quote balance, and total claims never exceeded totalDividendsDistributed. One qualification: "not privileged" does not mean "not abusable". Because claim() and distribute() are callable by anyone while the PoolManager is unlocked, a non-holder can redirect rewards that are waiting to be distributed (the high finding). That moves rewards between addresses; it never pays out more than was distributed and never touches balances.

**Reproduction**

Scratch tests on this tree: a stranger with no tokens calls claim(): returns 0, nothing moves. IMD-quoted token: sending 1 wei of ETH reverts (EthNotAccepted). testFuzz_claimsNeverExceedDistributed, 256 runs of three random buys, a random partial transfer and a full sell: eligibleSupply == sum of holder balances; sum(withdrawableDividendOf) <= accountedBalance <= token quote balance; the three claims pay exactly the sum of withdrawable and no more than totalDividendsDistributed. Existing testFuzz_buySellFeesAndSolvency (256 runs) passes. Expected: no special power behind any non-standard function and no over-payment. Actual: same.

### 9. Info: First buyer of a launch gets their own 3% holder fee back at the next distribution

`contracts/src/PadToken.sol:152`

```
        if (bal <= accountedBalance || eligible < MIN_ELIGIBLE_SUPPLY) return 0;
```

The router flushes before the buyer receives tokens so a trader does not share in their own fee. On the first buy eligibleSupply is 0, distribute() returns here and the 3% waits in the token; the buyer is then the only eligible holder and the next distribution credits the whole waiting amount to them. Effective fee on the first buy (normally the creator's initial buy through router.launch) is 1%, not 4%; the same applies whenever every holder has exited. Nobody is diluted, so this is a documentation gap against the README and the router comment at PepesFamilyRouter.sol:147, not a loss. Changing it is a design decision (for example routing the waiting amount to the protocol or holding it until a second holder exists).

**Reproduction**

Scratch test on this tree: alice calls router.launch{value: 1 ether}("A","A","", address(0), 1 ether, 1). Expected per README line 22 ("a trader doesn't earn from their own trade"): nothing from her own trade. Actual: the token holds 30000000000000000 wei with withdrawableDividendOf(alice) == 0; after bob buys 0.1 ETH through the router, withdrawableDividendOf(alice) == 32999999999999999 wei: her own 0.03 ETH plus 3% of bob's buy.

### 10. Info: setStartTick accepts -887000, at which every later launch for that quote reverts (owner-only, future launches only)

`contracts/src/PepesFamily.sol:435`

```
        if (tick % TICK_SPACING != 0 || tick > limit || tick < -limit) revert BadTick();
```

Trust assumption, not an exploit. The accepted range includes the negative edge value, where the launch range in _addLaunchLiquidity is a single 200-tick band at the end of the curve and the computed liquidity does not fit what the PoolManager accepts, so launch() and launchFor() for that quote revert until the owner sets a workable tick. Already-launched tokens such as Pepes, their pools, holders and rewards are unaffected: startTick is read only in _launch. The positive edge (+887000) launches normally. If the owner role is meant to be unable to halt launches, bound the tick to a range where the liquidity fits (or to a market-cap window).

**Reproduction**

Scratch test on this tree: owner calls setStartTick(IMD, -887000) (accepted: multiple of 200, within the limit); anyone calls pad.launch("X","X","",IMD): reverts. Same for setStartTick(ETH, -887000) and an ETH launch. Owner sets the IMD tick back to the 100 IMD market-cap tick: launch succeeds. Expected per the docs ("sets the starting market cap for future launches"): a launch at an extreme price. Actual: launches blocked while the value is set.

### 11. Info: Fee rounds down to zero for quote amounts below 25 wei (exact-in) or 24 wei (exact-out)

`contracts/src/PepesFamily.sol:294`

```
        uint256 fee = exactIn ? (amount * FEE_BPS) / BPS : (amount * FEE_BPS) / (BPS - FEE_BPS);
```

Both fee formulas round down (here and at line 326), so a swap whose quote side is under 25 wei pays no fee. Not exploitable: each such swap moves a few wei of value and costs a full transaction. Recorded only as the one place besides the medium finding where the 4% rule is not exact; no change recommended.

**Reproduction**

Scratch test on this tree: ETH-quoted launch, bob has bought. bob swaps through PoolSwapTest with zeroForOne=true, amountSpecified=-24 and 24 wei attached. Expected under a strict 4% rule: a non-zero fee. Actual: pendingProtocolFees(ETH) and pendingHolderFees(token) unchanged; bob receives 5923821984 token wei.

---

Judge's submission `b6eebc8c6ac6367a6b3ba803aeac1c8713a1772a85d4126ab47ede177f21c6fd`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
