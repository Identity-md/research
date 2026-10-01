# Audit report

> What the contracts are for
>
> PepesFamily is a token launchpad on Robinhood Chain (chain ID 4663), built on Uniswap v4.
>
> Anyone can launch a token with a fixed supply of 1B, paired with ETH or IMD.
> At launch, the whole supply becomes single-sided liquidity in a new v4 pool. The launchpad contract owns that position and has no way to remove it, so liquidity is locked forever.
> The launchpad is also the pool's v4 hook. It takes 4% of the quote side of every swap, through any router: 1% to the protocol, and 3% to the token's holders pro rata, which they claim.
> Tokens have no mint, no owner (owner() returns 0x0 in v2) and no admin functions. Nothing is upgradeable.
> The launchpad owner can only change where the protocol fee goes and the starting price for future launches.
> Contracts
>
> v2 (current):
> PepesFamily.sol: launcher, hook, fee vault
> PadToken.sol: the launched ERC-20, with holder rewards and EIP-2612 permit
> PepesFamilyRouter.sol
> PepesFamilyEthRouter.sol: trades IMD pairs with ETH via the v4 IMD/ETH pool
> lib/SafeTransfer.sol
> deploy scripts
> v1 (still live with real liquidity): src/v1/PadTokenV1.sol, plus the v1 launchpad and routers at commit a549093. The main difference from v2: the v1 router can pull tokens without an allowance, but only from its own caller.
> About 1,340 lines of Solidity in total. Uniswap v4-core is out of scope.
> What to look at hardest
>
> Hook fee accounting: delta signs for exact-in and exact-out in both currency orders; the transient-storage handoff between beforeSwap and afterSwap; fees on partially filled swaps.
> Fee claims and payouts: fees are held as Uniswap claim balances and paid out by flush and collectProtocolFees. Anyone can call those while the pool manager is mid-transaction for another contract. Can that ever drain the pool manager or break our accounting?
> Launch liquidity math: rounding, both token orderings, extreme starting prices.
> Holder reward accounting: overflow bounds, the excluded-address list, reentrancy on claim, and that payouts can never exceed what was distributed.
> Permit and the routers: EIP-712 correctness, front-run handling, msg.value and refunds, the two-swap ETH route.
> The v1 router's approval shortcut: confirm nobody can move another holder's tokens. GoPlus flags v1 tokens as a honeypot because of it, and we believe that's a false positive.
> Invariants to verify
>
> Liquidity can never be removed.
> Every swap pays exactly 4%.
> Fee claims and reward payouts are always fully backed.
> Supply is fixed.
> Routers only spend the caller's funds.
> Nobody can block selling or claiming.
> The full list, the known accepted behaviour and the test instructions (38 tests, including mainnet fork tests) are in AUDIT.md.

| | |
|---|---|
| Repository | https://github.com/0xtenang/PepesFamily.git |
| Commit | `d1ad57886d66570471fa11e23cf2b62f3e5aa7e8` |
| Job | `a3e708e2-fb57-43ea-a163-d93b916694a2` |
| Judged | 2026-10-01 03:58 UTC |
| Findings | 1 medium · 3 low · 3 info |

Four agents audited the code as it is at `d1ad578`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Quote-specified swaps are charged 4% of the requested amount, so a partial fill at sqrtPriceLimitX96 pays up to ~100% of what actually traded (or reverts with Panic 0x11)

`contracts/src/PepesFamily.sol:310`

```
        uint256 fee = exactIn ? (amount * FEE_BPS) / BPS : (amount * FEE_BPS) / (BPS - FEE_BPS);
```

In the two modes where the quote is the specified currency (exact-in buy, exact-out sell) `beforeSwap` derives the fee from `params.amountSpecified`, mints ERC-6909 claims for it in `_chargeFee` and returns it as the specified-side BeforeSwapDelta. v4 then swaps only `amount - fee` (exact-in) or asks the pool for `amount + fee` (exact-out), and in `Hooks.afterSwap` subtracts the full hook delta from the swapper regardless of how much executed. If the swap stops at the trader's `sqrtPriceLimitX96` before the requested amount is reached, the trader still pays 4% of the *requested* amount. `afterSwap` reads the fee back from FEE_SLOT and never compares the executed delta with the request. Measured: an exact-in buy of 1 ETH with a limit 0.1% below spot puts ~0.0017 ETH into the pool but pays 0.04 ETH of fee (96% of gross); 100 ETH with a limit 0.01% below spot pays 4.000 ETH for a 0.00025 ETH fill; an exact-out sell of 1 ETH with a limit 5% above spot receives 0.164 ETH gross and pays 0.041667 ETH (25%). When the exact-out partial fill is smaller than the pre-charged fee, the `Trade` event expression `poolQuote - fee` at line 350 underflows and the whole swap reverts with Panic(0x11) wrapped in HookCallFailed. That accidental revert is the only thing stopping the seller's quote delta from flipping negative (paying both tokens and quote), so any fix must not simply make line 350 saturating. This breaks AUDIT.md invariant 5.2 (`exactly 4% of the trader's gross quote amount`) and answers section 6.1: the overcharge is confined to the swap's own trader and the claim accounting stays consistent (minted claims == hook credit), but the loss is real for users of any router that passes a tight price limit as slippage protection (a documented v4 pattern): a front-runner who moves spot to the victim's limit forces the victim to pay the full fee for a near-zero fill, and the 3% holder share is then collected pro rata by holders including the front-runner. The project's routers and the Universal Router pass MIN/MAX limits and are only affected by the exact-out-sell revert at the end of the curve. The other two modes compute the fee from the pool's actual delta in `afterSwap` and are correct. Fix that keeps the design: in `afterSwap`, for the quote-specified branch, derive the executed specified amount from `delta` and revert with a dedicated error when it differs from `amount - fee` (exact-in) or `amount + fee` (exact-out), replacing the accidental Panic at line 350 with that explicit check; alternatively recompute the fee as 4% of the executed quote, burn the excess claims minted in `beforeSwap` and refund the difference to the swapper through the unspecified-side return delta (a hook cannot hand back specified currency from afterSwap). Merged from audit_economics 4a304d96, audit_permissions 18038b6d, audit_flow 00e8a3da and audit_math ae6142c5; all four proofs fail on the current code for this reason.

**Reproduction**

Launch an ETH-quoted token; bob buys 2 ETH through PepesFamilyRouter; p = slot0.sqrtPriceX96. (a) bob swaps through v4-core PoolSwapTest: SwapParams(zeroForOne=true, amountSpecified=-1 ether, sqrtPriceLimitX96=p - p/1000) with 1 ETH. Expected: fee <= 4% of the ETH bob actually spent (+2 wei). Actual: bob's balance drops by 0.0417 ETH, pendingProtocolFees(ETH)+pendingHolderFees(token) grow by exactly 0.04 ETH: 40000000000000000 > 1738077705176384 (the 4% bound). (b) bob swaps SwapParams(false, +1 ether, p + p/20): pool pays 0.164 ETH gross, fee 41666666666666666 wei charged vs bound 6568553689105052; bob receives 0.1225 ETH (25.4% fee). (c) bob swaps SwapParams(false, +1 ether, p + 1): pool delivers ~0 ETH < fee 0.041667 ETH, afterSwap reverts Panic(0x11) at `poolQuote - fee` (PoolManager surfaces WrappedError(hook, afterSwap.selector, Panic(0x11), HookCallFailed())). (d) with a limit one unit below spot and amountSpecified=-10 ether, the trader pays 400000000000000001 wei, receives 0 tokens, fee 0.4 ETH. Run: cd contracts && forge test --match-path test/scratch/Proof_18038b6d8bb1.t.sol (both tests fail on the current code).

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

/// @dev Hook fee on partially filled swaps whose specified currency is the quote.
///      `beforeSwap` computes the 4% fee on `params.amountSpecified` (the requested amount) and mints claims for it.
///      When the swap stops at `sqrtPriceLimitX96` before the requested amount is reached, the trader still pays the
///      full fee, so the fee is far more than 4% of what actually traded. Both tests fail on the current code and
///      pass once the hook either charges 4% of the executed quote amount or rejects partial fills.
contract PartialFillFeeTest is Test {
    using StateLibrary for IPoolManager;

    address constant FEE_RECIPIENT = 0x3c8A4d94B3219F6633F2cC94094f4765b30c691C;
    PoolManager pm;
    PepesFamily pad;
    PepesFamilyRouter router;
    PoolSwapTest extRouter; // third-party router: the trader picks the price limit
    PoolSwapTest.TestSettings settings = PoolSwapTest.TestSettings({takeClaims: false, settleUsingBurn: false});

    address alice = makeAddr("alice");
    address bob = makeAddr("bob");
    address owner = makeAddr("owner");

    function setUp() public {
        pm = new PoolManager(address(this));
        extRouter = new PoolSwapTest(pm);
        bytes memory initCode = abi.encodePacked(
            type(PepesFamily).creationCode,
            abi.encode(
                pm,
                address(0xBEEF), // IMD stand-in, unused here
                owner,
                FEE_RECIPIENT,
                DeployLib.startTickForMarketCap(1.5 ether),
                DeployLib.startTickForMarketCap(100e18),
                PepesFamily.ImdEthPool(10_000, 100, address(0))
            )
        );
        (bytes32 salt, address expected) = DeployLib.mineSalt(address(this), uint160(0x28CC), initCode, 0);
        address deployed;
        assembly {
            deployed := create2(0, add(initCode, 0x20), mload(initCode), salt)
        }
        require(deployed == expected, "hook address");
        pad = PepesFamily(deployed);
        router = PepesFamilyRouter(payable(pad.router()));
        vm.deal(alice, 100 ether);
        vm.deal(bob, 100 ether);
    }

    function _launchAndBuy() internal returns (PadToken t, PoolKey memory key) {
        vm.prank(alice);
        t = PadToken(payable(pad.launch("Test", "TST", "", address(0))));
        vm.prank(bob);
        router.buy{value: 2 ether}(address(t), 2 ether, 0, block.timestamp);
        key = pad.poolKey(address(t));
        vm.prank(bob);
        t.approve(address(extRouter), type(uint256).max);
    }

    function _pendingFees(PadToken t) internal view returns (uint256) {
        return pad.pendingProtocolFees(address(0)) + pad.pendingHolderFees(address(t));
    }

    /// Exact-in buy of 1 ETH with a price limit 0.1% below the current sqrt price: the pool only takes ~0.0015 ETH
    /// but the hook charges 0.04 ETH (fee on the requested 1 ETH): ~96% of what the trader paid.
    function test_exactInBuy_priceLimit_feeIsFourPercentOfExecuted() public {
        (PadToken t, PoolKey memory key) = _launchAndBuy();
        (uint160 p,,,) = IPoolManager(address(pm)).getSlot0(key.toId());
        uint256 ethBefore = bob.balance;
        uint256 feeBefore = _pendingFees(t);
        vm.prank(bob);
        try extRouter.swap{value: 1 ether}(key, SwapParams(true, -1 ether, p - p / 1000), settings, "") {
            uint256 paid = ethBefore - bob.balance; // gross quote the trader spent, fee included
            uint256 fee = _pendingFees(t) - feeBefore;
            assertLe(fee, (paid * 4) / 100 + 2, "fee exceeds 4% of the quote actually paid");
        } catch {
            // rejecting the partial fill is also a valid fix
        }
    }

    /// Exact-out sell of 1 ETH with a price limit 5% above the current sqrt price: the pool pays out ~0.164 ETH but
    /// the hook keeps 0.041667 ETH (fee on the requested 1 ETH): ~25% of what actually traded.
    function test_exactOutSell_priceLimit_feeIsFourPercentOfExecuted() public {
        (PadToken t, PoolKey memory key) = _launchAndBuy();
        (uint160 p,,,) = IPoolManager(address(pm)).getSlot0(key.toId());
        uint256 ethBefore = bob.balance;
        uint256 feeBefore = _pendingFees(t);
        vm.prank(bob);
        try extRouter.swap(key, SwapParams(false, int256(1 ether), p + p / 20), settings, "") {
            uint256 received = bob.balance - ethBefore;
            uint256 fee = _pendingFees(t) - feeBefore;
            uint256 gross = received + fee; // quote the pool actually paid out
            assertLe(fee, (gross * 4) / 100 + 2, "fee exceeds 4% of the quote actually received");
        } catch {
            // rejecting the partial fill is also a valid fix
        }
    }
}
```

### 2. Low: A zero-fill swap on a quote-empty pool moves the price to the end of the curve for free; marketCap(), getTokenInfo() and the Trade/Swap events then report ~0

`contracts/src/PepesFamily.sol:331`

```
        uint256 tokenAmount = uint256(int256(t < 0 ? -t : t));
```

The launch position covers [minUsableTick, start] (token is currency1) or [start, maxUsableTick] (token is currency0) and the pool is initialised exactly at `start`, where the position is not yet active. Whenever the pool holds no quote (every fresh launch without an initial buy, and any token whose buyers have all sold back) a sell-direction swap finds zero liquidity, so Pool.swap exchanges nothing and walks slot0 through empty tick words to the caller's `sqrtPriceLimitX96` (MAX_SQRT_PRICE-1 or MIN_SQRT_PRICE+1). The swapper's delta is 0/0, so the caller needs no tokens and no quote. The hook accepts it: `afterSwap` sees poolQuote == tokenAmount == 0, charges no fee and emits Trade(token, tx.origin, false, 0, 0, 0, sqrtPrice-at-limit); the PoolManager emits a Swap event with the same price. Afterwards `marketCap()` and `getTokenInfo().marketCap` return 0 for both orientations, the website's listing/ranking and chart show 0, and third-party charts built from Swap events show the token collapsing. Funds are not at risk: the next buy crosses the start tick (an initialized tick), re-activates the liquidity and trades at the correct price (confirmed: a following 1 ETH buy succeeds and marketCap recovers to ~4.05e18), so this is a free, repeatable griefing of every price surface the contracts expose. Minimal fix: in `afterSwap` revert when `tokenAmount == 0` (a swap on these pools that moves no tokens is never legitimate), optionally also clamping `marketCap()` to the start price when slot0 is outside the launch range. Merged from audit_economics 2acb80fc and audit_flow 4ef927c4.

**Reproduction**

Launch an ETH-paired token with no initial buy (start tick 203000; marketCap() = 1528490686780151368 wei). From an address holding zero tokens and sending no value, call PoolSwapTest.swap(key, SwapParams(zeroForOne=false, amountSpecified=-1, sqrtPriceLimitX96=MAX_SQRT_PRICE-1), settings, ""). Expected: revert or no price change. Actual: the call succeeds, caller balances unchanged, slot0.tick == 887271 (was 203000), sqrtPriceX96 == 1461446703485210103287273052203988822378723970341, pad.marketCap(token) == 0, a Trade event with all-zero amounts is emitted. Same on an IMD pool with the token as currency0 using zeroForOne=true and MIN_SQRT_PRICE+1. Run: cd contracts && forge test --match-path test/scratch/Proof_4ef927c4f0ae.t.sol (fails: 'pool tick moved by a zero-fill swap: 887271 != 203000').

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {PoolSwapTest} from "v4-core/src/test/PoolSwapTest.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {StateLibrary} from "v4-core/src/libraries/StateLibrary.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {SwapParams} from "v4-core/src/types/PoolOperation.sol";

import {PepesFamily} from "src/PepesFamily.sol";
import {PadToken} from "src/PadToken.sol";

contract MockIMD {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    function approve(address s, uint256 amt) external returns (bool) { allowance[msg.sender][s] = amt; return true; }
    function transfer(address to, uint256 amt) external returns (bool) { balanceOf[msg.sender] -= amt; balanceOf[to] += amt; return true; }
    function transferFrom(address f, address to, uint256 amt) external returns (bool) {
        if (allowance[f][msg.sender] != type(uint256).max) allowance[f][msg.sender] -= amt;
        balanceOf[f] -= amt; balanceOf[to] += amt; return true;
    }
}

/// @notice A swap on a pool that holds no quote fills nothing but still moves the pool price to the tick limit.
///         Anyone with zero tokens can do it; afterwards marketCap() reports 0 until the next buy.
contract ZeroCostPriceDisplacementTest is Test {
    using StateLibrary for IPoolManager;

    PoolManager pm;
    PepesFamily pad;
    PoolSwapTest ext;
    address alice = makeAddr("alice");
    address griefer = makeAddr("griefer");
    address owner = makeAddr("owner");

    function setUp() public {
        pm = new PoolManager(address(this));
        ext = new PoolSwapTest(pm);
        bytes memory initCode = abi.encodePacked(
            type(PepesFamily).creationCode,
            abi.encode(pm, address(new MockIMD()), owner, owner, int24(203000), int24(203000),
                PepesFamily.ImdEthPool(10_000, 100, address(0)))
        );
        bytes32 initHash = keccak256(initCode);
        for (uint256 i; i < 500_000; i++) {
            address h = address(uint160(uint256(keccak256(abi.encodePacked(bytes1(0xff), address(this), bytes32(i), initHash)))));
            if (uint160(h) & 0x3FFF == 0x28CC) {
                address deployed;
                assembly { deployed := create2(0, add(initCode, 0x20), mload(initCode), i) }
                require(deployed == h, "hook address");
                pad = PepesFamily(deployed);
                break;
            }
        }
        vm.deal(alice, 100 ether);
    }

    function test_quoteEmptyPoolPriceCannotBeDisplacedForFree() public {
        vm.prank(alice);
        PadToken t = PadToken(payable(pad.launch("T", "T", "", address(0))));
        PoolKey memory key = pad.poolKey(address(t));
        uint256 mcapBefore = pad.marketCap(address(t));
        (, int24 tickBefore,,) = IPoolManager(address(pm)).getSlot0(key.toId());
        assertEq(t.balanceOf(griefer), 0);

        // griefer "sells" 1 wei of a token they do not hold on a pool that holds no quote
        vm.prank(griefer);
        try ext.swap(key, SwapParams(false, -1, TickMath.MAX_SQRT_PRICE - 1), PoolSwapTest.TestSettings(false, false), "") {}
        catch {}

        (, int24 tickAfter,,) = IPoolManager(address(pm)).getSlot0(key.toId());
        // Expected: a zero-fill swap must not move the pool. Actual: tick jumps to 887271 and marketCap() is 0.
        assertEq(tickAfter, tickBefore, "pool tick moved by a zero-fill swap");
        assertEq(pad.marketCap(address(t)), mcapBefore, "marketCap changed by a zero-fill swap");
    }
}
```

### 3. Low: setStartTick accepts ticks below about -349,200 for which every launch on that quote reverts with TickLiquidityOverflow (and far-positive ticks that price launches at a few wei)

`contracts/src/PepesFamily.sol:451`

```
        if (tick % TICK_SPACING != 0 || tick > limit || tick < -limit) revert BadTick();
```

`_setStartTick` only checks spacing alignment and |tick| <= maxUsableTick - 200 (887000). `_addLaunchLiquidity` derives liquidity from the fixed supply over the remaining curve: L = (TOTAL_SUPPLY - 1e9) * 2^96 / (sqrtPrice(tick) - sqrtPrice(minUsableTick)) for the token-is-currency1 orientation, mirrored for currency0. As the start tick falls the denominator shrinks and L passes v4's maxLiquidityPerTick for spacing 200 (type(uint128).max / 8873 ~= 3.83e34), so PoolManager.modifyLiquidity reverts TickLiquidityOverflow(-887200); further down `int256(liquidity)` no longer fits int128 either. Measured boundary: -349200 still launches (liquidity just under the cap, market cap 1.46e42 wei), -349400 computes 38614042292128989553118521597990787 > 38345995821606768476828330790147420 and reverts; everything from -349400 to -887000 (about 60% of the accepted negative range) is a dead zone for both ETH and IMD launches (6 of 6 IMD launches failed at -349400, both orientations). On the positive side the bound admits ticks where the starting market cap rounds to a few wei (tick 600000 gives 8 wei, 800000 gives 0). This is owner-only and reversible (existing pools are unaffected), so it is a trust/robustness issue rather than an exploit, but AUDIT.md section 3 describes the owner's tick as 'bounded' and says the owner cannot pause, while this is in effect a per-quote pause (or a mispricing of all future launches) that the bounds were meant to prevent; it answers section 6.3. Fix: in `_setStartTick` compute the launch liquidity for the relevant orientation(s) with the same formula as `_addLaunchLiquidity` and revert BadTick if it exceeds Pool.tickSpacingToMaxLiquidityPerTick(TICK_SPACING) (or simply require |tick| <= 340_000), optionally also bounding the implied market cap to a sane range. Merged from audit_economics 63aa4d95, audit_permissions d8cc7af0, audit_flow 09f3f2b8 and audit_math 0b7f85e2.

**Reproduction**

Owner calls setStartTick(address(0), -349400): accepted (multiple of 200, within +-887000). Any account then calls pad.launch("T","T","",address(0)) or PepesFamilyRouter.launch. Expected: a tick the owner is allowed to set yields a launchable configuration. Actual: revert TickLiquidityOverflow(-887200) from PoolManager.modifyLiquidity inside unlockCallback, for every launch until the tick is changed; setStartTick(address(0), -349200) followed by the same launch succeeds. setStartTick(address(imd), -349400) bricks IMD launches the same way. setStartTick(address(0), 600000) is accepted and the next launch reports marketCap() == 8 wei. Run: cd contracts && forge test --match-path test/scratch/StartTickBricksLaunch.t.sol (fails with TickLiquidityOverflow(-887200)).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";

import {PepesFamily} from "src/PepesFamily.sol";
import {DeployLib} from "script/DeployLib.sol";

contract MockIMD {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    function approve(address s, uint256 amt) external returns (bool) { allowance[msg.sender][s] = amt; return true; }
    function transfer(address to, uint256 amt) external returns (bool) { balanceOf[msg.sender] -= amt; balanceOf[to] += amt; return true; }
    function transferFrom(address f, address to, uint256 amt) external returns (bool) {
        if (allowance[f][msg.sender] != type(uint256).max) allowance[f][msg.sender] -= amt;
        balanceOf[f] -= amt; balanceOf[to] += amt; return true;
    }
}

/// @notice `_setStartTick` accepts every spacing-aligned tick inside +-887000, but for start ticks below about
///         -349200 the launch liquidity exceeds v4's per-tick cap and every launch on that quote reverts with
///         TickLiquidityOverflow. Fails on the current code (setStartTick(-349400) is accepted, then launch reverts);
///         passes once setStartTick rejects ticks at which a launch cannot succeed, or launches succeed there.
contract StartTickBricksLaunchTest is Test {
    PoolManager pm;
    PepesFamily pad;
    address owner = makeAddr("owner");
    address carol = makeAddr("carol");

    function setUp() public {
        pm = new PoolManager(address(this));
        bytes memory initCode = abi.encodePacked(
            type(PepesFamily).creationCode,
            abi.encode(
                pm,
                address(new MockIMD()),
                owner,
                owner,
                DeployLib.startTickForMarketCap(1.5 ether),
                DeployLib.startTickForMarketCap(100e18),
                PepesFamily.ImdEthPool(10_000, 100, address(0))
            )
        );
        (bytes32 salt, address expected) = DeployLib.mineSalt(address(this), uint160(0x28CC), initCode, 0);
        address deployed;
        assembly {
            deployed := create2(0, add(initCode, 0x20), mload(initCode), salt)
        }
        require(deployed == expected, "hook address");
        pad = PepesFamily(deployed);
    }

    function test_acceptedStartTickAllowsLaunch() public {
        vm.prank(owner);
        try pad.setStartTick(address(0), -349400) {}
        catch {
            return; // rejecting the tick at configuration time is the expected fix
        }
        // Expected: a tick the owner may set yields a launchable configuration.
        // Actual: PoolManager.modifyLiquidity reverts TickLiquidityOverflow(-887200) for every ETH launch.
        vm.prank(carol);
        pad.launch("T", "T", "", address(0));
    }
}
```

### 4. Low: sellWithPermit / sellForEthWithPermit only accept a permit signed for exactly tokenAmount, contradicting the documented `value >= tokenAmount`

`contracts/src/PepesFamilyRouter.sol:42`

```
        try IERC20Permit(token).permit(msg.sender, address(this), amount, deadline, v, r, s) {}
```

`PermitHelper.permit` always calls `permit(msg.sender, address(this), amount, ...)` with `amount == tokenAmount`. The EIP-712 digest includes `value`, so a signature the holder produced for any other value (a larger or max allowance, as the NatSpec on PepesFamilyRouter.sol:118 invites with '`value` >= `tokenAmount`') does not recover to the holder and PadToken.permit reverts InvalidSignature; the catch branch then requires an *existing* allowance >= tokenAmount, which a user relying on permit does not have, so the sale reverts PermitFailed. The front-run tolerance likewise only works when the front-runner replays the identical signature. Users or integrators who sign one larger permit (the common pattern) cannot sell through the permit entry points; the website signs exactly `amount` so it is unaffected, and no funds are at risk. Fix: either add a `permitValue` parameter and pass it to `permit` (keeping the `allowance >= tokenAmount` fallback), or correct the NatSpec on PepesFamilyRouter.sol:118 and PepesFamilyEthRouter.sol:99 to say the permit must be signed for exactly `tokenAmount`. From audit_permissions eb8d0da8.

**Reproduction**

Holder dan buys 1 ETH of an ETH-quoted token (balance bal). dan signs a valid EIP-2612 permit for spender = router, value = 2*bal, nonce 0, deadline = now. dan calls router.sellWithPermit(token, bal, 1, now, v, r, s). Expected per NatSpec: the sale goes through because the signed value >= tokenAmount. Actual: reverts PermitFailed() (test_permitLargerValueRejected in test/scratch/JudgeChecks.t.sol, expectRevert(PermitHelper.PermitFailed.selector) passes).

### 5. Info: Trade event attributes third-party-router swaps to tx.origin, misattributing trades made through contract wallets, bundlers, aggregators and the project's own ETH router

`contracts/src/PepesFamily.sol:348`

```
        address trader = sender == router && hookData.length == 32 ? abi.decode(hookData, (address)) : tx.origin;
```

For any swap not sent by `PepesFamilyRouter` with a 32-byte hookData (including the project's own PepesFamilyEthRouter, which passes empty hookData, Universal Router, aggregators, ERC-4337 bundlers and Safe/EIP-7702 wallets) `trader` is `tx.origin`: the relayer or EOA that signed the outer transaction, not the account whose funds moved. The website's trade list and any analytics built on the event therefore show the wrong address for those trades; a relayer submitting many users' trades appears as one whale. No funds are affected; only the event is wrong. Fix: fall back to `sender` (the locker) when hookData carries no trader, and have PepesFamilyEthRouter pass abi.encode(r.user) as hookData and be recognised like `router`. From audit_permissions 58e4b03b.

**Reproduction**

vm.prank(bob, carol) (msg.sender bob, tx.origin carol); bob swaps 1 ETH exact-in through PoolSwapTest on an ETH-quoted pool. Expected: Trade.trader == bob (or the router contract). Actual: Trade.trader == carol (test_tradeEventTxOrigin in test/scratch/JudgeChecks.t.sol: expectEmit with trader = carol passes).

### 6. Info: The 4% fee and holder rewards only bind swaps in the hooked pool; any second pool for the same token trades fee-free (design boundary, should be stated as accepted)

`contracts/src/PepesFamily.sol:521`

```
    function beforeInitialize(address, PoolKey calldata, uint160) external pure returns (bytes4) {
```

`beforeInitialize` only blocks pool keys whose hook is PepesFamily; PadToken is a plain ERC-20 with no transfer hooks, so holders can supply it as liquidity to any other venue: a v4 pool with a different fee/tickSpacing/hook, or a v2/v3 pool. Swaps there pay nothing to the protocol or to holders, and once such a pool has depth aggregators will route around the 4%. AUDIT.md invariant 5.2 is stated for launched pools only, so this is a design boundary rather than a code bug, but the docs advertise '4% of every swap, through any router' and this caps those economics. No code fix is possible without changing the token (transfer-level fees), which the design rejects; recommend listing it under section 8 as accepted behaviour. From audit_economics 48737709.

**Reproduction**

ETH-paired launch; bob buys 5 ETH through the router. Anyone initialises PoolKey{currency0: ETH, currency1: token, fee: 3000, tickSpacing: 60, hooks: 0} at the current price (succeeds: no hook is consulted) and bob adds full-range liquidity with PoolModifyLiquidityTest (2 ETH + tokens). carol swaps 0.5 ETH exact-in in that pool through PoolSwapTest. Expected per the docs: 0.02 ETH of fees. Actual: carol receives tokens; pendingProtocolFees(ETH) and pendingHolderFees(token) are unchanged (test_secondPoolNoFee in test/scratch/JudgeChecks.t.sol passes).

### 7. Info: v1 router allowance exemption confirmed safe: no path lets the v1 router move tokens from anyone but its own msg.sender (GoPlus honeypot flag is a false positive)

`contracts/src/v1/PadTokenV1.sol:105`

```
        if (msg.sender != router) {
```

Not a defect; recorded because AUDIT.md section 6.6 asks for an independent opinion. Reviewed against the v1 PepesFamilyRouter at commit a549093. The only `transferFrom` the router issues is in `unlockCallback`: `Currency.unwrap(cIn).transferFrom(d.user, address(poolManager), owed)`, and `d.user` is always `msg.sender` of `sell`/`buy`/`launch` because the router builds `SwapData` itself in `_swap` and the PoolManager only calls `unlockCallback` on the contract that called `unlock`, passing that contract's own bytes back. `unlockCallback` checks `msg.sender == poolManager`; the router has no fallback or receive and makes no calls to attacker-supplied contracts, so there is no confused-deputy path; `launch`/`launchFor` and `buy` never pull a PadToken. The pulled currency is `cIn` from `pad.poolKey(token)` (reverts UnknownToken for anything not launched), so a crafted key cannot redirect it. The v1 ETH router is a separate contract, is not the exempt `router`, and needs a normal approval. Conclusion: the exemption lets the v1 router spend only the caller's own tokens, only inside the caller's own sell; nobody can move another holder's balance and selling is never blocked, so GoPlus's `owner_change_balance` / `is_honeypot` classification matches the pattern, not the behaviour. v2 removed the exemption (PadToken.sol:155-157), which is the right call for scanner compatibility. Merged from audit_economics 2e0ad245 and audit_permissions d2227b6e.

**Reproduction**

PadTokenV1 deployed with router = R: carol.transferFrom(bob, carol, 1) reverts InsufficientAllowance; only msg.sender == R skips the check (test_v1Exemption in test/scratch/JudgeChecks.t.sol). Against the a549093 router: carol calls router.sell(token, bobBalance, 0, deadline) -> transferFrom(carol, poolManager, bobBalance) -> InsufficientBalance, bob unchanged; carol calls router.unlockCallback(abi.encode(SwapData{user: bob,...})) directly -> NotPoolManager; carol calls poolManager.unlock(...) -> the PoolManager calls carol's own unlockCallback, not the router's. No other external function on the router reaches transferFrom.

---

Judge's submission `78c90a43bb866b9041081865ac7bbee72d7b65c14bb46fc8fbef02c14730b2e1`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
