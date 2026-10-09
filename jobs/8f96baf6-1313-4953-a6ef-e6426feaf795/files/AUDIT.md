# Audit report

> Project: PepesFamily launchpad v5: creator-chosen split of the 3% fee
> Repo: github.com/0xtenang/PepesFamily (commit 6256451)
> Scope: contracts/src/PepesFamily.sol, contracts/src/PepesFamilyLens.sol, contracts/src/PepesFamilyRouter.sol (new launchWithSplit; launch uses the default split). PadToken.sol is unchanged from v4 (audits ec4e3ea7, b803125e, 348884ab, cbe092d6).
> Tests: contracts/test/PepesFamily.t.sol, contracts/test/Fork.t.sol
> Chain: Robinhood Chain (4663), Uniswap v4
>
> What changed from v4
> Every swap still pays 4%, with a fixed 1% protocol fee in IMD. The other 3% is split as the creator chose at launch: FeeSplit{creatorBps, holderBps, burnBps}, summing to 300, in steps of 50, with creator ≤ 200, immutable per token. Presets: 0/300/0 (default), 200/100/0, 0/0/300, or custom.
>
> IMD fee = (400 − burnBps) bps of the trader’s gross IMD: 100 protocol, creatorBps to pendingCreatorFees[token], holderBps to pendingHolderFees[token].
> Creator fees: collectCreatorFees(token) (anyone) pays creatorPayout[token]. setCreatorPayout can only be called by the current payout address.
> Burn = burnBps of the trader’s gross token amount, taken in the token and sent to 0x…dEaD via poolManager.take during the swap.
> Where each fee is charged: the specified currency’s fee in beforeSwap (positive specified delta), the unspecified currency’s fee in afterSwap (hook delta), so a swap can pay IMD fees and burn together. Transient slots FEE_SLOT / BURN_SLOT pass the before-swap amount to afterSwap.
> getTokenInfo / getTokens moved to PepesFamilyLens (deployed by the launchpad, lens()) to stay under the contract size limit. launch / launchFor were replaced by launchWithSplit / launchForWithSplit.
> Please check
>
> Fee math for all four swap kinds (exact-in/out × buy/sell) and both currency orders: protocol 1%, creator and holder shares of the gross IMD, burn share of the gross tokens. Is there any rounding or partial-fill case where a trader pays more or less than stated, or where toInt128 reverts unexpectedly?
> Is taking tokens to 0x…dEaD from inside beforeSwap / afterSwap always settled correctly? Consider swaps with a price limit that only partly fill, and very small or very large amounts.
> Claim backing: the launchpad’s ERC-6909 IMD claims must always equal pendingProtocolFees + Σ pendingHolderFees + Σ pendingCreatorFees.
> Creator fees: can anyone redirect or block them? Any reentrancy in collectCreatorFees or the unlock callback?
> Split validation: can a token end up with a split that breaks the rules, or a creator above 2%?
> Regressions: anything that breaks v4 guarantees (locked liquidity, 4% on every router, the flash-borrow guard, holder expiry, router compatibility, the ETH router’s hookData).

| | |
|---|---|
| Repository | https://github.com/0xtenang/PepesFamily.git |
| Commit | `625645162d0ce24946fd6c73316f8d9497452c76` |
| Job | `8f96baf6-1313-4953-a6ef-e6426feaf795` |
| Judged | 2026-10-09 03:28 UTC |
| Findings | 1 medium · 2 low · 4 info |

Four agents audited the code as it is at `6256451`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Specified-side fee and burn are computed on the requested amount in beforeSwap, so a partially filled swap (price limit reached) pays the full fee/burn of the request; exact-out partial fills below th

`contracts/src/PepesFamily.sol:346`

```
        uint256 fee = exactIn ? (amount * bps) / BPS : (amount * bps) / (BPS - bps);
```

beforeSwap computes the fee of the specified currency (the IMD fee when IMD is specified, the token burn when the token is specified) from params.amountSpecified, charges it immediately (_chargeFee mints claims / _burn takes tokens to 0x...dEaD) and returns it as a positive specified BeforeSwapDelta. v4-core subtracts that hook delta from the swapper's delta whatever the pool actually fills. afterSwap never reconciles it with the executed amount. When the swap stops early at sqrtPriceLimitX96 (any third-party router, aggregator or limit-order integration that passes a price limit; PepesFamily's own routers always pass the end-of-curve limit and are not affected) the trader pays the fee of the whole request on a small fill. The README already lists the IMD-fee half as an open medium inherited from v4; v5 adds the token burn in beforeSwap, which has the same shape, so burn tokens now over-burn on partial fills as well. Consequences: (1) exact-in buy: 4% (or 400-burnBps) of the requested IMD is charged although the pool consumed a fraction, effective fee up to ~97% of what the trader paid; (2) exact-in sell on a burn token: burnBps of the requested tokens are burned in beforeSwap, effective burn up to ~96% of tokens sold; (3) exact-out (sell with IMD specified, buy on a burn token): the fee is amount*bps/(BPS-bps) of the REQUESTED output; a partial fill delivering d < amount+fee gives the trader d-fee, i.e. an effective rate of fee/d (observed 3999 bps instead of 400); if d < fee the swapper's delta would flip sign (seller pays IMD / buyer owes tokens), which today is prevented only by accident: the Trade event's checked subtractions `poolQuote - fee` (line 416) and `poolToken - burned` (line 417) underflow and the swap reverts with Panic(0x11) wrapped by the PoolManager. Any refactor of that event silently re-enables the sign flip. The overcharge is booked into protocol/creator/holder fees or burned, so ERC-6909 claim backing stays exact; the loss is the trader's. Fix (minimal, preserves the design): refuse partial fills explicitly, e.g. in beforeSwap revert unless params.sqrtPriceLimitX96 is the end-of-curve limit (MIN_SQRT_PRICE+1 for zeroForOne, MAX_SQRT_PRICE-1 otherwise), or in afterSwap revert with a custom PartialFill() when the executed specified amount is smaller than requested minus fee; at minimum replace the accidental Panic with an explicit check. Charging the specified-side fee on the realised fill is not expressible in v4 (afterSwap can only return the unspecified delta) without re-denominating the fee. Merged from audit_flow, audit_math (two findings), audit_economics (two findings) and audit_permissions; all reproduced.

**Reproduction**

Foundry, local PoolManager, PepesFamily deployed at a mined hook address, start mcap 100 IMD, PoolSwapTest as the third-party router. (a) Token with FeeSplit(0,300,0), alice buys 20 IMD via PepesFamilyRouter; bob swaps exact-in -100e18 IMD with sqrtPriceLimitX96 = spot*0.999. Expected: fee ~4% of the IMD actually paid. Actual: bob pays 4.1212e18 IMD of which 4.0000e18 is fee (pendingProtocolFees+pendingHolderFees), 9705 bps of what he paid. (b) Token with FeeSplit(0,0,300): bob sells his whole balance exact-in with a limit 0.1% past spot. Actual: tokens paid 5.571e24, tokens burned 4.734e24 (8497 bps, expected 300). Both in Proof_476591b59783 (test/scratch), 2 failing tests; the audit_flow proof (limit one tick spacing away) fails the same way: fee 4e18 vs expected 0.2e18; burn 2.638e25 vs expected 8.2e23. (c) Exact-out: FeeSplit(0,300,0), bob buys 20 IMD, then exact-out sell of 1e18 IMD with limit = spot+1: reverts with WrappedError wrapping Panic(0x11) from afterSwap (data contains 4e487b71...11). With the limit set to the price reached by an exact-out sell of 0.1 IMD and a request of 1e18: pool delivers 0.104167e18 gross, fee charged 41,666,666,666,666,666 (=1e18*400/9600, on the REQUESTED amount), bob receives 62,500,000,000,000,000: 3999 bps effective fee. Scratch tests test_exactOutSell_partialFill_panics and test_exactOutSell_partialFill_overcharges (test/scratch/Edges.t.sol) pass as written, i.e. they confirm the defective behaviour.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {PoolSwapTest} from "v4-core/src/test/PoolSwapTest.sol";
import {StateLibrary} from "v4-core/src/libraries/StateLibrary.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {SwapParams} from "v4-core/src/types/PoolOperation.sol";

import {PepesFamily} from "src/PepesFamily.sol";
import {PepesFamilyRouter} from "src/PepesFamilyRouter.sol";
import {PadToken} from "src/PadToken.sol";
import {DeployLib} from "script/DeployLib.sol";

contract ProofIMD {
    string public name = "IMD";
    string public symbol = "IMD";
    uint8 public decimals = 18;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function mint(address to, uint256 amt) external {
        balanceOf[to] += amt;
    }

    function approve(address s, uint256 amt) external returns (bool) {
        allowance[msg.sender][s] = amt;
        return true;
    }

    function transfer(address to, uint256 amt) external returns (bool) {
        balanceOf[msg.sender] -= amt;
        balanceOf[to] += amt;
        return true;
    }

    function transferFrom(address f, address to, uint256 amt) external returns (bool) {
        if (allowance[f][msg.sender] != type(uint256).max) allowance[f][msg.sender] -= amt;
        balanceOf[f] -= amt;
        balanceOf[to] += amt;
        return true;
    }
}

/// @notice PepesFamily v5: fees taken in `beforeSwap` are computed on the amount the trader *requested*, not on
///         what the pool actually fills. A swap stopped early by `sqrtPriceLimitX96` (any third-party router that
///         sets one) therefore pays the full fee / burn of the requested amount on a tiny fill.
///         Expected: at most 4% IMD fee of the IMD actually paid, at most burnBps of the tokens actually sold /
///         received, or an explicit revert. Actual: fee is 97% of the IMD paid; burn is 85% of the tokens paid.
contract PartialFillProofTest is Test {
    using StateLibrary for IPoolManager;

    address constant DEAD = 0x000000000000000000000000000000000000dEaD;
    PoolManager pm;
    PepesFamily pad;
    PepesFamilyRouter router;
    ProofIMD imd;
    PoolSwapTest ext;
    PoolSwapTest.TestSettings settings = PoolSwapTest.TestSettings({takeClaims: false, settleUsingBurn: false});
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        imd = new ProofIMD();
        ext = new PoolSwapTest(pm);
        bytes memory initCode = abi.encodePacked(
            type(PepesFamily).creationCode,
            abi.encode(
                pm,
                address(imd),
                address(this),
                address(0xFEE),
                DeployLib.startTickForMarketCap(100e18),
                PepesFamily.ImdEthPool(10_000, 100, address(0))
            )
        );
        uint160 flags = uint160((1 << 13) | (1 << 11) | (1 << 7) | (1 << 6) | (1 << 3) | (1 << 2));
        (bytes32 salt, address expected) = DeployLib.mineSalt(address(this), flags, initCode, 0);
        address deployed;
        assembly {
            deployed := create2(0, add(initCode, 0x20), mload(initCode), salt)
        }
        require(deployed == expected, "hook address");
        pad = PepesFamily(deployed);
        router = PepesFamilyRouter(payable(pad.router()));
        address[2] memory users = [alice, bob];
        for (uint256 i; i < users.length; i++) {
            imd.mint(users[i], 1_000_000e18);
            vm.startPrank(users[i]);
            imd.approve(address(router), type(uint256).max);
            imd.approve(address(ext), type(uint256).max);
            vm.stopPrank();
        }
    }

    /// Launches with the given split, alice buys 20 IMD, bob is approved on the external router.
    function _launch(uint16 c, uint16 h, uint16 b) internal returns (PadToken t) {
        vm.prank(alice);
        t = PadToken(payable(pad.launchWithSplit("S", "S", "", address(imd), PepesFamily.FeeSplit(c, h, b))));
        vm.prank(alice);
        router.buy(address(t), 20e18, 0, block.timestamp);
        vm.prank(bob);
        t.approve(address(ext), type(uint256).max);
    }

    /// A price limit 0.1% (in sqrt price) past the current price: the swap can only fill a small amount.
    function _limit(PadToken t, bool zeroForOne) internal view returns (uint160) {
        (uint160 p,,,) = IPoolManager(address(pm)).getSlot0(pad.poolKey(address(t)).toId());
        return zeroForOne ? uint160(uint256(p) * 9_990 / 10_000) : uint160(uint256(p) * 10_010 / 10_000);
    }

    /// Exact-in buy of 100 IMD with a price limit: the pool takes ~0.12 IMD, the hook still charges 4 IMD.
    function test_exactInBuy_partialFill_feeIsAtMost4PercentOfPaid() public {
        PadToken t = _launch(0, 300, 0);
        (,,,, bool q0) = pad.launches(address(t));
        PoolKey memory key = pad.poolKey(address(t));
        bool zfo = q0; // buy: IMD in
        uint160 lim = _limit(t, zfo);
        uint256 before = imd.balanceOf(bob);
        uint256 p0 = pad.pendingProtocolFees(address(imd));
        uint256 h0 = pad.pendingHolderFees(address(t));
        vm.prank(bob);
        (bool ok,) = address(ext).call(abi.encodeCall(ext.swap, (key, SwapParams(zfo, -100e18, lim), settings, "")));
        if (!ok) return; // refusing a swap with a price limit is an acceptable fix
        uint256 paid = before - imd.balanceOf(bob);
        uint256 fee = (pad.pendingProtocolFees(address(imd)) - p0) + (pad.pendingHolderFees(address(t)) - h0);
        assertGt(paid, 0);
        assertLe(fee, paid * 400 / 10_000 + 1, "fee exceeds 4% of the IMD the trader actually paid");
    }

    /// Exact-in sell of all tokens on a 3%-burn token with a price limit: the burn is 3% of the requested amount,
    /// taken in `beforeSwap`, while the pool only takes a fraction.
    function test_exactInSell_partialFill_burnIsAtMost3PercentOfSold() public {
        PadToken t = _launch(0, 0, 300);
        (,,,, bool q0) = pad.launches(address(t));
        PoolKey memory key = pad.poolKey(address(t));
        bool zfo = !q0; // sell: token in
        uint256 bal = t.balanceOf(alice);
        vm.prank(alice);
        t.transfer(bob, bal);
        uint160 lim = _limit(t, zfo);
        uint256 tBefore = t.balanceOf(bob);
        uint256 dead0 = t.balanceOf(DEAD);
        vm.prank(bob);
        (bool ok,) = address(ext).call(abi.encodeCall(ext.swap, (key, SwapParams(zfo, -int256(bal), lim), settings, "")));
        if (!ok) return; // refusing a swap with a price limit is an acceptable fix
        uint256 paidTokens = tBefore - t.balanceOf(bob);
        uint256 burned = t.balanceOf(DEAD) - dead0;
        assertGt(paidTokens, 0);
        assertLe(burned, paidTokens * 300 / 10_000 + 1, "burn exceeds 3% of the tokens the trader actually sold");
    }
}
```

### 2. Low: Burn is taken from the PoolManager's token balance before the seller settles, so a single sell whose 3% burn exceeds the pool's remaining token inventory reverts (beforeSwap for exact-in sells, afterS

`contracts/src/PepesFamily.sol:443`

```
        poolManager.take(Currency.wrap(token), DEAD, amount);
```

_burn calls poolManager.take(token, DEAD, amount), a real ERC-20 transfer out of the PoolManager, from inside the swap. For sells the seller's tokens arrive only after the swap (every router, including PepesFamilyRouter, PepesFamilyEthRouter and Uniswap's, settles the input after swap returns), so at that moment the PoolManager holds only the pool's remaining inventory. If burnBps*amountIn/BPS (exact-in, beforeSwap) or burnBps*poolToken/(BPS-burnBps) (exact-out, afterSwap) exceeds that balance, PadToken.transfer reverts with InsufficientBalance and the whole sell fails. Reached once more than ~97% of the supply (for burnBps=300) is outside the pool and one holder sells more than pool/0.03 in a single swap. The seller can split the sale, so funds are not stuck, but v4's 'everyone can exit in one trade' (test_everyoneCanExit) regresses for burn tokens at high market caps, and the failure surfaces as an opaque wrapped revert. Fix: do not move real token balances mid-swap: mint the burn as ERC-6909 claims to the hook during the swap (as the IMD fee is) and convert claims to tokens at 0x...dEaD outside the swap path (e.g. in flush or a separate burnPending(token)); this also removes the sync-ordering regression reported separately. Merged from audit_math and audit_economics; audit_permissions anchored a different mechanism at this line (kept separately).

**Reproduction**

FeeSplit(0,0,300) token with IMD as currency0, start mcap 100 IMD. bob buys with 5,000e18 IMD through PepesFamilyRouter: bob holds 950,432,978.447e18 tokens, the PoolManager holds 20,172,187.167e18. bob approves the router and calls router.sell(token, 950,432,978.447e18, 0, now). Expected: the sale executes. Actual: revert; trace shows PepesFamily.beforeSwap -> PoolManager.take(token, 0xdEaD, 28,512,989.353e18) -> PadToken.transfer -> InsufficientBalance(). Selling the same balance in two halves succeeds and claims stay backed. afterSwap variant: same state, PoolSwapTest exact-out sell of 4,880e18 IMD (oneForZero, end-of-curve limit): afterSwap -> take(token, 0xdEaD, 25,080,902.628e18) -> InsufficientBalance(); an exact-out sell of 1,220e18 IMD succeeds. Scratch tests test_hugeSell_burnExceedsPoolBalance_reverts and test_exactOutSell_burnInAfterSwap_exceedsPoolBalance_reverts in test/scratch/Edges.t.sol.

### 3. Low: Burn moves real tokens out of the PoolManager mid-swap, so routers that sync the input token before calling swap revert with CurrencyNotSettled on burn tokens (worked on every v4 token)

`contracts/src/PepesFamily.sol:443`

```
        poolManager.take(Currency.wrap(token), DEAD, amount);
```

v4's hook only minted ERC-6909 claims during a swap, which changes no ERC-20 balance, so any legal sync/transfer/settle ordering worked. v5's _burn lowers the PoolManager's token balance inside beforeSwap/afterSwap. PoolManager._settle credits balanceOf(PoolManager) - syncedReserves, so an integrator whose unlock does sync(tokenIn) -> swap -> transfer(owed) -> settle is credited owed - burn against a debt of owed, leaving a -burn delta and the unlock reverts with CurrencyNotSettled(). The same router works on tokens with burnBps = 0. PepesFamily's two routers, PoolSwapTest and Uniswap's V4Router/Universal Router sync after the swap and are unaffected, so this is an integration regression for third-party routers and pre-funding patterns rather than a loss of funds. Fix: as for the inventory-limit finding, hold the burn as claims during the swap and take the tokens to 0x...dEaD outside the swap; or document that integrators of burn tokens must sync after the swap. Merged from audit_math, audit_economics and audit_permissions.

**Reproduction**

Minimal router R whose unlockCallback does pm.sync(tokenIn); delta = pm.swap(key, exact-in 1e18 tokens, end-of-curve limit); token.transferFrom(user, pm, -delta.in); pm.settle(); pm.take(IMD, user, delta.out). Launch a FeeSplit(0,300,0) token and a FeeSplit(0,0,300) token (both with IMD as currency0), bob buys 10 IMD of each through PepesFamilyRouter and approves R. R.swapExactIn(keyA, false, 1e18) on the 0/300/0 token succeeds. R.swapExactIn(keyB, false, 1e18) on the 0/0/300 token reverts with IPoolManager.CurrencyNotSettled(): beforeSwap took 0.03e18 tokens to 0xdEaD after the sync, so settle credits 0.97e18 against a 1e18 debt. Scratch test test_syncBeforeSwapRouter_breaksWithBurn in test/scratch/Edges.t.sol.

### 4. Info: Rounding remainder of the IMD fee is booked to pendingHolderFees even when holderBps is 0, so the routers flush and distribute 1-wei amounts on such tokens

`contracts/src/PepesFamily.sol:435`

```
        uint256 holderFee = fee - protocolFee - creatorFee;
```

_chargeFee rounds protocolFee and creatorFee down and assigns the remainder to holders. For splits with holderBps == 0 and creatorBps > 0 (200/0/100, 150/0/150, 100/0/200, 50/0/250) the remainder is 1 wei on most trades, so pendingHolderFees[token] becomes non-zero although the creator chose no holder share. PepesFamilyRouter and the ETH router then call flush on the next trade, which burns 1 wei of claims, takes 1 wei of IMD to the token, runs PadToken.distribute (storage writes, checkpoint push, events) and emits HolderFeesFlushed(token, 1). Accounting and claim backing stay exact; the cost is gas on every trade of such tokens and misleading events for a token advertised as paying holders nothing. Fix: compute holderFee = fee * holderBps / qBps and let the protocol (or creator) share absorb the remainder. Merged from audit_math, audit_economics and audit_permissions.

**Reproduction**

Launch FeeSplit(200, 0, 100). Exact-in buy of 1034 wei IMD through PoolSwapTest: fee = 1034*300/10000 = 31; protocolFee = 31*100/300 = 10; creatorFee = 31*200/300 = 20; holderFee = 1. Expected: pendingHolderFees[token] == 0. Actual: pendingProtocolFees == 10, pendingCreatorFees == 20, pendingHolderFees == 1; the next router.buy flushes it (pendingHolderFees back to 0, imd.balanceOf(token) == 1). Scratch test test_holderDust_whenHolderBpsZero in test/scratch/Edges.t.sol.

### 5. Info: PepesFamilyLens.getTokens(offset, limit) reverts with Panic(0x11) when offset + limit overflows instead of returning the tail of the list

`contracts/src/PepesFamilyLens.sol:96`

```
        uint256 end = offset + limit > n ? n : offset + limit;
```

The paging helper adds offset and limit with checked arithmetic before clamping to n. A caller passing limit = type(uint256).max (the common 'everything from offset' idiom) with 0 < offset < tokenCount gets an arithmetic panic rather than the remaining tokens. View-only, no funds. Fix: `uint256 end = limit > n - offset ? n : offset + limit;`. From audit_math.

**Reproduction**

Launch two tokens so pad.tokenCount() == 2, then staticcall PepesFamilyLens(pad.lens()).getTokens(1, type(uint256).max). Expected: a one-element array holding the second token. Actual: revert with selector 0x4e487b71 and code 0x11. Scratch test test_lens_getTokens_limitOverflow in test/scratch/Edges.t.sol.

### 6. Info: marketCap (and the Lens) multiply the price by the constant TOTAL_SUPPLY, so tokens burned to 0x...dEaD by burn-share tokens are still counted

`contracts/src/PepesFamily.sol:597`

```
            ? FullMath.mulDiv(FullMath.mulDiv(TOTAL_SUPPLY, Q96, sqrtP), Q96, sqrtP) // price = tokens per quote
```

marketCap is documented as the fully diluted market cap. PadToken.totalSupply is a constant 1e27 and the burned tokens sit at 0x...dEaD, so price x 1e27 is literally 'fully diluted'; but for v5 burn tokens those tokens are irrecoverable and the site sorts tokens by this value (commit 48cb09c), so a heavily traded burn token is ranked above a non-burn token at the same price. Cosmetic / product decision rather than a security defect. Fix if wanted: use TOTAL_SUPPLY - token.balanceOf(DEAD) (or - totalBurned[token]) in marketCap, or expose totalBurned in TokenInfo so the front end can choose. From audit_economics.

**Reproduction**

FeeSplit(0,0,300) token (start mcap 100 IMD, IMD currency0): bob buys with 50e18 IMD through PepesFamilyRouter and sells his whole balance back. totalBurned[token] = 19,321,629.866e18. marketCap(token) = 105.963240689025969032e18 IMD. Excluding the dead balance: 103.915858172946660784e18 IMD (2% higher). Scratch test test_marketCap_countsBurnedTokens in test/scratch/Edges.t.sol.

### 7. Info: Trust assumptions: single-step creator payout handover (a typo loses all future creator fees), owner/feeRecipient powers, tx.origin attribution on third-party routers

`contracts/src/PepesFamily.sol:482`

```
        creatorPayout[token] = payout;
```

Documented for completeness, not permission bypasses. (1) setCreatorPayout is a single-step handover with only a zero-address check, unlike the launchpad's two-step ownership transfer; the payout address that sends the role to a wrong address loses every future creator fee of that token irrevocably, because collectCreatorFees (permissionless) always pays creatorPayout[token] and nobody else can change it. A two-step accept, or at least an event-driven UI confirmation, would mirror the owner flow. (2) owner (two-step transfer) can repoint feeRecipient, which receives the 1% protocol fee and all expired holder rewards (PadToken.recycle reads feeRecipient() at call time), and can change startTick for future launches; a compromised owner key redirects those flows but cannot touch liquidity, the 3% split, pendingHolderFees/pendingCreatorFees or any existing token. (3) For buys through routers other than the two PepesFamily routers the hook records tx.origin as the active buyer (v4 behaviour): contract wallets buying through aggregators are not marked and should claim weekly. Inventory of the other state-changing entry points found correctly guarded: launchForWithSplit (router only), hook callbacks and unlockCallback (PoolManager only; the pad's unlockCallback only runs from its own unlock payloads), beforeInitialize/beforeAddLiquidity/donate hooks revert for everyone but the hook itself, flush mid-unlock only for the two routers, collectProtocolFees/collectCreatorFees permissionless but paying fixed recipients, split validation (sum 300, 0.5% steps, creator <= 200) enforced on both launch paths and written once, ERC-6909 claims equal pendingProtocolFees + sum(pendingHolderFees) + sum(pendingCreatorFees) on every path (each mint/burn matches the pending update). From audit_permissions.

**Reproduction**

State: alice launches a FeeSplit(200,100,0) token, bob buys 100 IMD (pendingCreatorFees = 2e18). alice calls setCreatorPayout(token, 0x...typo). Expected: a way to recover or confirm. Actual: creatorPayout[token] is the typo forever; alice's later setCreatorPayout reverts NotCreator (test_split_creatorFeesCollectAndPayout shows the old address losing the role), and every collectCreatorFees(token) pays the typo address. State: owner key compromised -> setFeeRecipient(attacker) redirects all future protocol fees and all future expired rewards of every token; nothing else.

---

Judge's submission `5530411083da71da2c94cf9b5a3f45c2642253a3dcf75c86291d3ca0a5e10032`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
