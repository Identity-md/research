# Audit report

> Audit the contracts in 0xtenang/Runner as they are.

| | |
|---|---|
| Repository | https://github.com/0xtenang/Runner.git |
| Commit | `f66eb5d430e156768c2253669d3c10e45c31bc7d` |
| Job | `d4297b4d-7c6d-4a0f-815f-2b0840ead21e` |
| Judged | 2026-10-24 14:42 UTC |
| Findings | 2 medium · 3 low · 1 info |

Four agents audited the code as it is at `f66eb5d`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Fee is fixed at 4% of the requested IMD in beforeSwap and never reconciled with the fill: partially filled exact-in buys and exact-out sells are overcharged, and large exact-out sells revert with a pa

`contracts/RunnerHook.sol:279`

```
        uint256 fee = exactIn ? (amount * FEE_BPS) / BPS : (amount * FEE_BPS) / (BPS - FEE_BPS);
```

Merged from audit_math (medium), audit_flow (low), audit_permissions (low) and audit_economics (medium), plus audit_math's separate low on the afterSwap underflow at line 320, which is the same defect's extreme case. For the two swap directions where IMD is the specified currency (exact-in buy, exact-out sell), beforeSwap computes the fee from params.amountSpecified, mints it to the hook as ERC-6909 claims via _chargeFee, and returns it as the specified-currency BeforeSwapDelta before the pool has swapped anything. afterSwap only reloads that number from FEE_SLOT (lines 303-307); it never compares it with the IMD delta the pool actually produced. Uniswap v4 does not revert on a partial fill: the pool delivers what the caller's sqrtPriceLimitX96 and the available liquidity allow. Since the hook's delta is fixed, the swapper's IMD delta becomes (filled amount) +/- (4% of the requested amount), so the effective fee is 4% of the request, not of the trade. The RUNNER/IMD pool is single-sided: its IMD reserve is only the net IMD bought so far, so an exact-out sell above the reserve is an ordinary early-market input through any v4 router that supports exact-output (the project's own RunnerRouter and RunnerEthRouter are exact-in only; the hook is documented to tax 'any v4 router'). The other two directions (exact-in sell, exact-out buy) compute the fee in afterSwap from the realised delta and are correct. When the fixed fee exceeds the IMD the pool paid out (request above ~24x the reserve), the Trade event argument `poolQuote - fee` at line 320 underflows and the whole swap reverts with Panic(0x11) wrapped in the PoolManager's WrappedError, so such sells cannot execute at all and the failure reason is opaque. Who loses: the trader, by up to the full 4% of an amount that did not trade (400 IMD on a 10,000 IMD exact-in order that fills 0.032 IMD). Fix that keeps the 4%-of-IMD design: in afterSwap, for the FEE_SLOT branch, compare the realised IMD delta with the amount the fee was computed from (exact-in buy: poolQuote must equal amount - fee; exact-out sell: poolQuote must equal amount + fee) and either revert with a clear PartialFill error or recompute the fee from the fill, burn the excess claims and return the difference through the after-swap hookDelta. Either way the subtraction in the Trade event can no longer underflow; if the revert option is chosen, also guard the event math explicitly.

**Reproduction**

Setup as in contracts/test/RunnerHook.t.sol (hook at the 635 IMD start tick, pool opened, alice holds IMD and 10M RUNNER, PoolSwapTest from v4-core as an external router). (A) Exact-out sell above the reserve: alice buys with 1,000e18 IMD through RunnerRouter, so the pool holds 960e18 IMD. alice then calls PoolSwapTest.swap(key, SwapParams(zeroForOne = RUNNER->IMD, amountSpecified = +2_000e18, sqrtPriceLimit = extreme), {false,false}, ""). Expected: fee at most 4% of the 960e18 IMD the pool paid out = 38.4e18, seller nets about 921.6e18, or the partial fill is refused. Actual: pendingProtocolFees+pendingHolderFees grow by 83_333_333_333_333_333_333 (2000e18*400/9600), the seller receives 876.67e18 IMD for RUNNER worth 960e18 (an 8.7% fee). (B) Exact-in buy with a price limit: from the fresh pool, alice calls PoolSwapTest.swap(key, SwapParams(zeroForOne = IMD->RUNNER, amountSpecified = -10_000e18, sqrtPriceLimit = current sqrtPrice +/- 0.05%)). Expected: fee about 0.0013e18 (4% of the 0.032e18 IMD the pool consumed). Actual: fee 400e18, alice's IMD balance drops by 400.032e18 for 49,999.99 RUNNER. (C) Same state as (A) with amountSpecified = +50_000e18: expected a clean partial fill or a clear revert; actual revert WrappedError(hook, afterSwap 0xb47b2fb1, Panic 0x11) from `poolQuote - fee`. The attached proof test/scratch/FeeOnRequestedAmount.t.sol fails on this code with 'fee is at most 4% of the IMD the pool paid out: 83333333333333333333 > 38400000000000000000' and 'fee is at most 4% of the IMD the pool took: 400000000000000000000 > 1283859551908474'. Because foundry.toml sets test = contracts/test, run it with: FOUNDRY_TEST=test/scratch forge test --match-path test/scratch/FeeOnRequestedAmount.t.sol

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
import {Currency} from "v4-core/src/types/Currency.sol";
import {SwapParams} from "v4-core/src/types/PoolOperation.sol";

import {RunnerHook} from "contracts/RunnerHook.sol";
import {RunnerRouter} from "contracts/RunnerRouter.sol";
import {RunnerDeployLib} from "contracts/utils/RunnerDeployLib.sol";

interface IRunner {
    function balanceOf(address) external view returns (uint256);
    function approve(address, uint256) external returns (bool);
    function transfer(address, uint256) external returns (bool);
}

/// @dev Minimal 18-decimal IMD stand-in (RunnerToken is compiled with 0.8.24, so it is deployed via deployCode).
contract ScratchIMD {
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

/// @notice When IMD is the specified currency (exact-in buy, exact-out sell) RunnerHook.beforeSwap fixes the
///         fee at 4% of the *requested* amount and afterSwap never reconciles it with the amount the pool
///         actually moved. A partial fill (price limit, or an exact-out sell above the pool's IMD reserve)
///         is therefore charged far more than 4% of the IMD that was swapped. Both tests fail on the current
///         code; they pass if the hook either refuses the partial fill or re-derives the fee from the fill.
contract FeeOnRequestedAmountTest is Test {
    using StateLibrary for IPoolManager;

    uint256 constant DAY = 1 days;
    uint256 constant SUPPLY = 1_000_000_000e18;

    PoolManager pm;
    ScratchIMD imd;
    RunnerHook hook;
    IRunner runner;
    RunnerRouter router;
    PoolSwapTest extRouter;
    PoolSwapTest.TestSettings settings = PoolSwapTest.TestSettings({takeClaims: false, settleUsingBurn: false});

    address owner = makeAddr("owner");
    address feeRecipient = makeAddr("feeRecipient");
    address team = makeAddr("team");
    address alice = makeAddr("alice");

    function setUp() public {
        vm.warp(20_500 * DAY + 3600);
        pm = new PoolManager(address(this));
        imd = new ScratchIMD();
        extRouter = new PoolSwapTest(pm);

        bytes memory initCode = abi.encodePacked(
            type(RunnerHook).creationCode,
            abi.encode(
                pm,
                address(imd),
                owner,
                feeRecipient,
                RunnerDeployLib.startTickForMarketCap(635e18, SUPPLY),
                RunnerHook.ImdEthPool(10_000, 100, address(0))
            )
        );
        (bytes32 salt, address expected) = RunnerDeployLib.mineSalt(address(this), uint160(hook_flags()), initCode, 0);
        address deployed;
        assembly {
            deployed := create2(0, add(initCode, 0x20), mload(initCode), salt)
        }
        require(deployed == expected, "hook address");
        hook = RunnerHook(deployed);
        router = RunnerRouter(hook.router());

        runner = IRunner(deployCode("RunnerToken.sol:RunnerToken", abi.encode(owner, address(hook), team, address(imd), address(pm))));
        vm.prank(owner);
        hook.openPool(address(runner));

        imd.mint(alice, 1_000_000e18);
        vm.prank(team);
        runner.transfer(alice, 10_000_000e18); // RUNNER to sell with
        vm.startPrank(alice);
        imd.approve(address(router), type(uint256).max);
        imd.approve(address(extRouter), type(uint256).max);
        runner.approve(address(extRouter), type(uint256).max);
        vm.stopPrank();
    }

    function hook_flags() internal pure returns (uint256) {
        return (1 << 13) | (1 << 11) | (1 << 7) | (1 << 6) | (1 << 3) | (1 << 2);
    }

    function _fees() internal view returns (uint256) {
        return hook.pendingProtocolFees(address(imd)) + hook.pendingHolderFees(address(runner));
    }

    /// Exact-out sell for more IMD than the pool holds: fee must be at most 4% of the IMD actually paid out.
    function test_exactOutSell_feeIsAtMost4PercentOfWhatThePoolPaid() public {
        // The pool holds exactly the IMD one buy brought in: 1,000 IMD paid, 40 fee, 960 IMD in the pool.
        vm.prank(alice);
        router.buy(address(runner), 1_000e18, 0, block.timestamp);

        PoolKey memory key = hook.poolKey(address(runner));
        bool imdIs0 = Currency.unwrap(key.currency0) == address(imd);

        uint256 imdBefore = imd.balanceOf(alice);
        uint256 runnerBefore = runner.balanceOf(alice);
        uint256 feesBefore = _fees();

        // Exact-out sell: ask for 2,000 IMD out (the pool only has 960). Sell direction = RUNNER in.
        bool zeroForOne = !imdIs0;
        uint160 limit = zeroForOne ? TickMath.MIN_SQRT_PRICE + 1 : TickMath.MAX_SQRT_PRICE - 1;
        vm.prank(alice);
        try extRouter.swap(key, SwapParams(zeroForOne, int256(2_000e18), limit), settings, "") {
            uint256 imdAfter = imd.balanceOf(alice);
            uint256 feeCharged = _fees() - feesBefore;
            assertLt(runner.balanceOf(alice), runnerBefore, "seller paid RUNNER");
            assertGt(imdAfter, imdBefore, "a sell must pay the seller IMD, never cost IMD");
            uint256 gross = (imdAfter - imdBefore) + feeCharged;
            assertLe(feeCharged, (gross * hook.FEE_BPS()) / hook.BPS() + 1, "fee is at most 4% of the IMD the pool paid out");
        } catch {
            // Refusing a partial exact-out fill is also an acceptable outcome.
        }
    }

    /// Exact-in buy stopped early by the caller's price limit: fee must be at most 4% of the IMD the pool took.
    function test_exactInBuy_priceLimit_feeIsAtMost4PercentOfWhatThePoolTook() public {
        PoolKey memory key = hook.poolKey(address(runner));
        bool imdIs0 = Currency.unwrap(key.currency0) == address(imd);
        (uint160 sqrtP,,,) = IPoolManager(address(pm)).getSlot0(key.toId());
        // A limit 0.05% away from the current price: the pool fills only a sliver of the 10,000 IMD order.
        uint160 limit = imdIs0 ? uint160(uint256(sqrtP) * 9995 / 10000) : uint160(uint256(sqrtP) * 10005 / 10000);

        uint256 imdBefore = imd.balanceOf(alice);
        uint256 feesBefore = _fees();
        vm.prank(alice);
        try extRouter.swap(key, SwapParams(imdIs0, -10_000e18, limit), settings, "") {
            uint256 feeCharged = _fees() - feesBefore;
            uint256 paid = imdBefore - imd.balanceOf(alice);
            uint256 toPool = paid - feeCharged;
            assertLe(feeCharged, (toPool * hook.FEE_BPS()) / hook.BPS() + 1, "fee is at most 4% of the IMD the pool took");
        } catch {
            // Refusing a partial fill is also an acceptable outcome.
        }
    }
}
```

### 2. Medium: openPool requires the hook's RUNNER balance and the token supply to be exactly 100M / 1B, so 1 wei transferred to the hook or burned before launch bricks the launch and strands the 100M liquidity allo

`contracts/RunnerHook.sol:216`

```
                || t.balanceOf(address(this)) != LIQUIDITY_ALLOCATION || t.totalSupply() != TOTAL_SUPPLY
```

Merged from audit_flow (medium) and audit_permissions (medium). openPool, the only function that sets `token` and moves the hook's RUNNER into the pool, reverts BadToken unless the hook's balance equals LIQUIDITY_ALLOCATION and totalSupply equals TOTAL_SUPPLY with strict equality. Both values are controlled by third parties between RunnerToken's deployment and openPool: the constructor mints 100M transferable RUNNER to the team wallet (a different address from the owner), and RunnerToken has public transfer() and burn(). Any holder can transfer 1 wei to the hook, or burn 1 wei, and from then on every openPool call reverts. The hook has no function that moves RUNNER out except _addLaunchLiquidity, which is only reachable after this check, and hook, startTick and RunnerToken.hook are all immutable, so the 100,000,000 RUNNER allocation is stranded and both contracts must be redeployed (new token address, existing holders orphaned). The README's deploy order (hook, token, then open the pool) leaves this window open in normal operation, and startEmission() before openPool widens the set of holders to every claimant. The strictness buys nothing: the wiring is already proven by t.hook() == address(this), and _addLaunchLiquidity burns whatever the hook holds beyond `owed` to DEAD (line 261), so a surplus is harmless. Fix: replace the two equalities with t.balanceOf(address(this)) >= LIQUIDITY_ALLOCATION (or drop both checks, since the token mints exactly 100M to its immutable hook), keeping the burn of the remainder.

**Reproduction**

Deploy RunnerHook (startTick 142_600) and RunnerToken(owner, hook, team, imd, poolManager); the hook holds exactly 100_000_000e18 and the team 100_000_000e18. Before the owner calls openPool: vm.prank(team); runner.transfer(address(hook), 1); (or vm.prank(team); runner.burn(1);). Then vm.prank(owner); hook.openPool(address(runner)). Expected: the pool opens, hook.token() == runner, about 100M RUNNER in the PoolManager and the extra wei burned with the rounding dust. Actual: revert BadToken() on this and every later call; runner.balanceOf(hook) stays 100_000_000e18 + 1 with no path out. The attached proof (both tests) fails with BadToken() on this code. Because foundry.toml sets test = contracts/test, run it with: FOUNDRY_TEST=test/scratch forge test --match-path test/scratch/OpenPoolBrick.t.sol

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {RunnerHook} from "contracts/RunnerHook.sol";
import {RunnerDeployLib} from "contracts/utils/RunnerDeployLib.sol";

interface IRunner {
    function balanceOf(address) external view returns (uint256);
    function transfer(address, uint256) external returns (bool);
    function burn(uint256) external;
}

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

/// RunnerHook.openPool requires the hook's RUNNER balance to be exactly 100,000,000e18 and the token's
/// totalSupply to be exactly 1e27. Between the token's deployment and openPool, the team wallet (and anyone
/// it pays) holds RUNNER and can send 1 wei to the hook or burn 1 wei. After that openPool reverts BadToken
/// forever and the hook has no way to move its 100M RUNNER: the pool can never open.
contract OpenPoolBrickTest is Test {
    PoolManager pm;
    MockIMD imd;
    RunnerHook hook;
    IRunner runner;
    address owner = makeAddr("owner");
    address team = makeAddr("team");

    function setUp() public {
        vm.warp(20_500 days + 3600);
        pm = new PoolManager(address(this));
        imd = new MockIMD();
        bytes memory initCode = abi.encodePacked(
            type(RunnerHook).creationCode,
            abi.encode(pm, address(imd), owner, makeAddr("feeRecipient"), int24(142_600), RunnerHook.ImdEthPool(10_000, 100, address(0)))
        );
        uint160 flags = uint160((1 << 13) | (1 << 11) | (1 << 7) | (1 << 6) | (1 << 3) | (1 << 2));
        (bytes32 salt, address expected) = RunnerDeployLib.mineSalt(address(this), flags, initCode, 0);
        address deployed;
        assembly { deployed := create2(0, add(initCode, 0x20), mload(initCode), salt) }
        require(deployed == expected, "hook address");
        hook = RunnerHook(deployed);
        runner = IRunner(deployCode("RunnerToken.sol:RunnerToken", abi.encode(owner, address(hook), team, address(imd), address(pm))));
    }

    /// 1 wei of RUNNER sent to the hook before openPool must not stop the launch.
    function test_openPool_survivesDustSentToHook() public {
        vm.prank(team);
        runner.transfer(address(hook), 1);
        vm.prank(owner);
        hook.openPool(address(runner)); // reverts BadToken on the current code
        assertEq(hook.token(), address(runner), "pool opened");
        assertGe(runner.balanceOf(address(pm)), 99_999_999e18, "liquidity allocation is in the pool");
    }

    /// 1 wei of RUNNER burned by any holder before openPool must not stop the launch either.
    function test_openPool_survivesPreLaunchBurn() public {
        vm.prank(team);
        runner.burn(1);
        vm.prank(owner);
        hook.openPool(address(runner)); // reverts BadToken on the current code
        assertEq(hook.token(), address(runner), "pool opened");
    }
}
```

### 3. Low: Constructor accepts start ticks beyond roughly +/-395,000 for which openPool always reverts TickLiquidityOverflow, stranding the 100M allocation

`contracts/RunnerHook.sol:175`

```
        if (startTick_ % TICK_SPACING != 0 || startTick_ > limit || startTick_ < -limit) revert BadTick();
```

From audit_math (low), reproduced. The constructor only checks that startTick_ is a multiple of 200 and within +/-887,000. _addLaunchLiquidity then derives liquidity = amount * 2^96 / (sqrtU - sqrtL) (or the currency0 mirror) for a range running from the start tick to the extreme usable tick. Far from zero that range is so narrow in sqrt-price space that the liquidity exceeds v4's maximum liquidity per tick for spacing 200 (about 3.83e34), and PoolManager.modifyLiquidity reverts TickLiquidityOverflow. openPool is the only path that moves the hook's RUNNER, and the hook address, startTick and RunnerToken.hook are immutable, so the allocation is unrecoverable and both contracts must be redeployed. The documented launch tick (142,600, liquidity about 8e22) is well inside the safe band, so the live configuration is not affected; the defect is that the guard admits inputs that brick the launch only after the token has been minted to the hook. Fix: compute the launch liquidity in the constructor and require it to be <= Pool.tickSpacingToMaxLiquidityPerTick(TICK_SPACING) (and <= type(int128).max), or bound |startTick_| accordingly, so a misconfigured deployment fails at construction.

**Reproduction**

Deploy RunnerHook via CREATE2 with startTick_ = -400_000 (a multiple of 200, |tick| <= 887,000, so BadTick does not fire). Deploy RunnerToken(owner, hook, team, imd, poolManager); the hook holds 100_000_000e18 RUNNER. Call hook.openPool(token) as owner. Expected: the pool opens and the allocation is locked in it. Actual: revert data 0xb8e3c385fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff27660 = TickLiquidityOverflow(int24 -887200); token.balanceOf(hook) stays 100_000_000e18 with no way to move it. Reproduced in test/scratch/Leads.t.sol::test_startTick_minus400000_bricksOpenPool (the mirror case +400,000 with RUNNER as currency0 gives the same liquidity by symmetry).

### 4. Low: claimable() returns a cap-clamped amount that claim() with the same signed totalEarned rejects with DailyCapReached / PoolEmpty

`contracts/RunnerToken.sol:353`

```
        if (amount > leftToday) amount = leftToday;
```

Merged from audit_math (low) and audit_permissions (low), reproduced. claimable(account, totalEarned) clamps totalEarned - claimed[account] to what is left of today's emission (line 353) and to rewardsRemaining() (line 355), implying a partial payout. claim() is all-or-nothing: line 380 reverts DailyCapReached whenever claimedOnDay[day] + amount > emissionOn(day), and line 381 reverts PoolEmpty when the pool is short. So for any account whose unpaid earnings exceed today's remaining emission, the view reports a positive, payable-looking amount while the write with the same signature reverts. Wallets and integrators that read claimable() before submitting a signed claim will show a balance and send a failing transaction; the server would have to sign a smaller totalEarned (done + leftToday) to realise the reported number. Fix: either make claimable return 0 when the full difference does not fit (mirroring claim), or make claim pay min(amount, leftToday, pool) and set claimed[account] = done + paid so the remainder is claimable later (which changes the signed-total semantics and needs the server to agree); update the doc comment to match.

**Reproduction**

owner calls setSigner(S) and startEmission() (emissionOn(today) = 10_000_000e18). Bob submits a valid locked claim for totalEarned = 9_500_000e18, so claimedOnDay[today] = 9_500_000e18. claimed[alice] = 0. runner.claimable(alice, 1_000_000e18) returns 500_000e18. alice calls claim(alice, 1_000_000e18, block.timestamp + 1 hours, v, r, s, false) with S's valid signature over (alice, 1_000_000e18, deadline, false). Expected: either claimable returns 0, or claim pays the 500_000e18 the view promised. Actual: claim reverts DailyCapReached(). Reproduced in test/scratch/Leads.t.sol::test_claimable_vs_claim.

### 5. Low: transferFrom accepts from = address(0) with value 0 and emits Transfer(0x0, to, 0), a mint-looking event anyone can forge

`contracts/RunnerToken.sol:225`

```
    function transferFrom(address from, address to, uint256 value) external returns (bool) {
```

From audit_economics (low), reproduced. _transfer only rejects to == address(0); nothing rejects from == address(0). With value = 0, _spendAllowance passes (allowance[0][caller] = 0 and 0 < 0 is false) and _move passes (balanceOf[0] = 0 >= 0, _track returns early because the balance is unchanged), so the call returns true and emits Transfer(address(0), to, 0). On an ERC-20, a Transfer from the zero address is the mint signal explorers, indexers and token scanners key on, so any address can make the event log show 'mints' to any wallet at no cost. Supply and balances are untouched, so this is a logging and indexing defect rather than a loss of funds. OpenZeppelin's ERC20 reverts ERC20InvalidSender for this input. Fix: revert in _move or _transfer when from == address(0).

**Reproduction**

Deploy RunnerToken(owner, hook, team, rewardToken, poolManager) with any non-zero addresses. From any EOA call transferFrom(address(0), <any address>, 0). Expected: revert (transfer from the zero address is invalid). Actual: returns true and emits Transfer(from = 0x0000000000000000000000000000000000000000, to = <any address>, value = 0); totalSupply stays 1_000_000_000e18. Reproduced in test/scratch/Leads.t.sol::test_transferFrom_fromZero with vm.expectEmit on Transfer(address(0), bob, 0).

### 6. Info: Trust assumption: the token owner's setSigner and setEmissionSchedule powers can move up to 20M RUNNER/day out of the run-reward pool, bounded only by the daily cap

`contracts/RunnerToken.sol:499`

```
    function setSigner(address newSigner) external onlyOwner {
```

From audit_permissions (info), verified; recorded as a trust assumption, not a permission bypass. Access-control inventory checked on every path: RunnerToken owner: setSigner (any address, no delay), setClaimsPaused, startEmission (once), setEmissionSchedule (from the next UTC day, <= 20M/day, >= 7-day halving), excludePool (only contracts whose token0()/token1() is RUNNER), setProtocolWallet, two-step ownership. RunnerHook owner: openPool (once), setFeeRecipient, two-step ownership; flush is gated to the hook's routers mid-unlock, collectProtocolFees is ungated but only pays feeRecipient; hook callbacks and unlockCallback are PoolManager-only; nobody can remove the launch liquidity. Material assumption: a compromised token-owner key calls setSigner(attacker) and claims the whole of the day's emission (10M RUNNER on launch day, 8M paid plus 2M burned for an instant claim), then setEmissionSchedule(20M, 7, 20M) raises that to 20M/day from the next day. The code documents this and the requester states ownership moves to a multisig before launch. No unprivileged amplifier was found.

**Reproduction**

Owner calls setSigner(S) then startEmission(). S signs (bob, 10_000_000e18, deadline, instant = true); bob calls claim(...). Result: bob receives 8_000_000e18 and 2_000_000e18 is burned. Owner calls setEmissionSchedule(20_000_000e18, 7, 20_000_000e18); emissionOn(today + 1) returns 20_000_000e18. Reproduced in test/scratch/Leads.t.sol::test_owner_setSigner_drains_day. Expected per design: the owner is a multisig; the code permits exactly this and nothing beyond DailyCapReached.

---

Judge's submission `77b0faa12a4ce3c3fe988facb1e1eb20fa4978168896b53ae38bec31906e2863`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
