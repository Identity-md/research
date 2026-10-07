# Audit report

> Adversarial review of the IMDO flywheel contracts at the given commit of github.com/ToknWrks/imdo (Foundry; Solidity 0.8.26, via_ir, bytecode_hash = "none"; vendored lib/ with Uniswap v4-core, v4-periphery, permit2, OpenZeppelin, solmate, forge-std). This tree is the accepted output of IMD swarm job 948f8b1b-a4bd-4689-a346-2536b218e486 (build, tests, manifest and four specialist reviews accepted; judge accepted with seven findings) plus two commits by the project that apply the judge's findings 1-3. Review the whole tree as it stands; weigh the two commits hardest.
>
> Contracts (src/): IMDOToken (LaunchToken alias, fixed 1,000,000,000e18 supply, no owner), ImdoHook (Uniswap v4 hook on one ETH/IMDO pool: ETH-side fee 20% at the first filled swap decaying linearly over 30 minutes to 1.5%, owner can only lower; fees paid to the treasury inside the swap, or minted as ERC-6909 claims redeemable only to the treasury when the PoolManager lacks ETH), ImdoTreasury (no owner, no withdrawal; anyone calls process() at most every 600 s for a 50 bps bounty; the rest splits 1000/2500/2500/4000 bps to opsWallet, offsetsSafe, REGEN (held in staking, withdrawable by regenSafe never beyond what was notified) and an on-chain IMD buy on the ETH/IMD v4 pool fee 10000 spacing 200 pushed to staking; REGEN leg capped per 7-day epoch, 0.5 ETH default, settable by regenSafe within 0.05-5 ETH, overflow to IMD; IMD buy min-out = max(spot, checkpoint * 7d/(7d+age)) fee-adjusted minus 300 bps; after a buy the checkpoint is refreshed to clamp(postSwapSpot, floorNow, floorNow * 1.02) and CheckpointRefreshed is emitted; failed legs halve the retry cap), ImdoStaking (stake IMDO, 24-hour lock reset on every stake, pro-rata IMD rewards, lifetime REGEN credit in ETH that never decreases, stakeFor only by the immutable claim contract), ImdoClaim (identity.md seat holders and a Merkle holder list claim IMDO in daily tranches after launch; unclaimed burns to 0xdead after the deadline; launch_ >= block.timestamp enforced). script/DeployImdo.s.sol deploys all of it from one EOA with the claim address predicted from the deployer nonce and requires launch >= now + MIN_LAUNCH_LEAD (1 hour).
>
> The two project commits to scrutinise: (1) src/ImdoTreasury.sol _refreshCheckpoint / _checkpointFloor / MAX_CHECKPOINT_RISE_BPS = 200 and test/unit/CheckpointRefresh.t.sol (the judge's sandwich proof plus an inflated-dust-buy case): is the clamp sound in both directions, can the floor still be ratcheted or pinned, does any honest market move now stall the IMD leg longer than the 7-day decay implies, does the choice of 200 bps leave a cheaper attack; (2) script/DeployImdo.s.sol MIN_LAUNCH_LEAD and test/unit/ImdoDeploy.t.sol: is the lead sufficient given that staking and claim are separate broadcast transactions. Also confirm the parent judge's informational findings 4-7 are still as described and whether any deserves a fix before mainnet.
>
> Rules: read-only review; do not modify src/, script/, foundry.toml, lib/ or launch.json; scratch tests may be added under test/scratch/ only. Every finding needs severity, exact file:line, a concrete reproduction and, where possible, a Foundry proof that fails on this code. Run the default suite (101 tests) and forge fmt --check and report the result. Do not claim an audit; this is a review by the IMD swarm. Mainnet dependencies for fork tests: IMD 0xD34a99Bc0f67aE1bbd63C660e6d0b0dd03E263B7, PoolManager 0x000000000004444c5dc75cB358380D2e3dE08A90.

| | |
|---|---|
| Repository | https://github.com/ToknWrks/imdo.git |
| Commit | `d980fdd621007e27cd318881d9410a37657f8e83` |
| Job | `37ac5d94-da10-4a27-84d9-246c17a2c3f7` |
| Judged | 2026-10-07 03:53 UTC |
| Findings | 5 low · 4 info |

Four agents audited the code as it is at `d980fdd`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: MAX_CHECKPOINT_RISE_BPS bounds one refresh, not the sum: repeated sandwiched dust buys lift the floor above market and stall the IMD leg for days

`src/ImdoTreasury.sol:359`

```
        uint256 ceilNow = FullMath.mulDiv(floorNow, BPS + MAX_CHECKPOINT_RISE_BPS, BPS);
```

Commit e28a1f9 clamps each post-buy refresh to floorNow * 1.02 (sqrt-price), but floorNow is the previous checkpoint decayed by only 7d/(7d+600s) = 0.099% per cooldown and the refresh resets checkpointAt, so successive buys compound: after N cooldowns the checkpoint can sit at market * (1.02 * 0.999)^N. The ceiling is independent of ethIn, so a buy of ~1 gwei (receive() is open; 3 gwei sent to the treasury puts ~1.2 gwei in the IMD leg, above MIN_ETH_PER_BUY) moves it by the full step. Anyone who is the keeper each cooldown can therefore sell IMD until the sqrt-price clears the next ceiling, call process() so the dust buy fills there, and buy back, inside one transaction. After 12 rounds (2 h) the checkpoint is 1.2557x market and 144 consecutive process() calls over the next 24 h all fail with InsufficientOutput; after 20 rounds (3.3 h) it is 1.4596x market and the leg is stalled for 264,600 s (3.06 days). README.md:35 and launch.json say a dust buy 'cannot pin the floor above spot for longer than that decay takes to close a 2% gap (under an hour)' / 'cannot pin it above spot for days'; both hold only for a single buy. Cost is round-trip pool fees and impact only: 17.17 ETH-equivalent for 20 rounds at the 200 ETH test depth (about 2.8x that at the mainnet pool's ~564-692 ETH virtual depth). No funds are lost: pending IMD ETH waits, the retry cap halves, and the other legs continue, so this is a paid grief of the 40% leg, not extraction. It also answers the brief: 200 bps is not what leaves the cheaper path, any per-buy step larger than the ~10 bps per-cooldown decay is ratchetable. Merged from audit_flow, audit_economics and audit_math (three equivalent reports). Minimal fix inside the design: scale the permitted rise with the buy, riseBps = MAX_CHECKPOINT_RISE_BPS * ethIn / maxEthPerBuy (a pin then requires full-size buys at the pushed price, each handing the treasury IMD at a discount), and/or bound the rise by elapsed time since the last upward refresh; correct the README/launch.json wording either way.

**Reproduction**

Fixture of test/unit/CheckpointRefresh.t.sol (200 ETH full-range ETH/IMD pool, script constants). (1) fund 1 ETH, process(): checkpoint = market. (2) Repeat 12 times: warp +600 s; sell IMD (oneForZero) with sqrtPriceLimit = floorNow * 1.03; send 3 gwei to the treasury; process() (pending becomes 0, CheckpointRefreshed to floorNow * 1.02); buy IMD back to market. (3) warp +600 s, fund 0.01 ETH, process(), repeat 144 times. Expected per README: IMD bought within the hour. Actual (test/scratch run of the attached proof): checkpoint/market = 12557 bps, 144 failed calls, 0 IMD bought in 24 h. With 20 rounds (test/scratch/Residual.t.sol::test_cumulativePinCost): checkpoint/market = 14596 bps, 264,600 s stalled, round-trip cost 17,166,091,265,848,883,922 wei.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "@uniswap/v4-core/src/PoolManager.sol";
import {IPoolManager} from "@uniswap/v4-core/src/interfaces/IPoolManager.sol";
import {IHooks} from "@uniswap/v4-core/src/interfaces/IHooks.sol";
import {PoolKey} from "@uniswap/v4-core/src/types/PoolKey.sol";
import {PoolIdLibrary} from "@uniswap/v4-core/src/types/PoolId.sol";
import {Currency, CurrencyLibrary} from "@uniswap/v4-core/src/types/Currency.sol";
import {SwapParams, ModifyLiquidityParams} from "@uniswap/v4-core/src/types/PoolOperation.sol";
import {TickMath} from "@uniswap/v4-core/src/libraries/TickMath.sol";
import {StateLibrary} from "@uniswap/v4-core/src/libraries/StateLibrary.sol";
import {FullMath} from "@uniswap/v4-core/src/libraries/FullMath.sol";
import {PoolSwapTest} from "@uniswap/v4-core/src/test/PoolSwapTest.sol";
import {PoolModifyLiquidityTest} from "@uniswap/v4-core/src/test/PoolModifyLiquidityTest.sol";
import {LiquidityAmounts} from "@uniswap/v4-periphery/src/libraries/LiquidityAmounts.sol";
import {MockERC20} from "solmate/src/test/utils/mocks/MockERC20.sol";
import {IMDOToken} from "src/IMDOToken.sol";
import {ImdoStaking} from "src/ImdoStaking.sol";
import {ImdoTreasury} from "src/ImdoTreasury.sol";

/// @notice The MAX_CHECKPOINT_RISE_BPS ceiling is applied per successful buy, relative to the floor that buy
/// enforced, and independent of how much ETH the buy spent. A 1-gwei buy at a pushed price therefore lifts the
/// checkpoint by the full 2% (sqrt), and repeating it every cooldown compounds: after N pins the floor is
/// ~1.02^N * 0.999^N of market. The decay only closes 0.1% per 600 s, so the stall after N pins is about
/// 7d * (1.02^N / 1.0153 - 1): 12 dust pins (2 hours of attacker time) stall the IMD leg for about 1.6 days,
/// not the "under an hour" one pin is documented to cost. The test asserts the leg recovers within a day.
contract RepeatedPinsTest is Test {
    using PoolIdLibrary for PoolKey;
    using StateLibrary for IPoolManager;

    PoolManager manager;
    PoolSwapTest swapRouter;
    PoolModifyLiquidityTest lpRouter;
    MockERC20 imd;
    IMDOToken imdo;
    ImdoStaking staking;
    ImdoTreasury treasury;
    PoolKey imdKey;
    address alice = makeAddr("alice");

    receive() external payable {}

    function setUp() public {
        vm.warp(1_800_000_000);
        manager = new PoolManager(address(this));
        swapRouter = new PoolSwapTest(manager);
        lpRouter = new PoolModifyLiquidityTest(manager);
        vm.deal(address(this), 100_000 ether);
        imd = new MockERC20("Identity.md", "IMD", 18);
        imd.mint(address(this), 1e36);
        imd.approve(address(lpRouter), type(uint256).max);
        imd.approve(address(swapRouter), type(uint256).max);
        imdKey = PoolKey(CurrencyLibrary.ADDRESS_ZERO, Currency.wrap(address(imd)), 10000, 200, IHooks(address(0)));
        uint160 sqrtP = TickMath.getSqrtPriceAtTick(54000);
        manager.initialize(imdKey, sqrtP);
        uint128 liquidity = LiquidityAmounts.getLiquidityForAmounts(
            sqrtP,
            TickMath.getSqrtPriceAtTick(-887200),
            TickMath.getSqrtPriceAtTick(887200),
            200 ether,
            type(uint128).max
        );
        lpRouter.modifyLiquidity{value: 200 ether}(
            imdKey, ModifyLiquidityParams(-887200, 887200, int256(uint256(liquidity)), 0), ""
        );
        imdo = new IMDOToken();
        staking =
            new ImdoStaking(address(imdo), address(imd), address(manager), makeAddr("claim"), makeAddr("regenSafe"));
        treasury = new ImdoTreasury(
            address(staking),
            makeAddr("ops"),
            makeAddr("offsets"),
            makeAddr("regenSafe"),
            address(manager),
            address(imd),
            10000,
            200,
            address(0),
            1 ether,
            300,
            600,
            0.5 ether,
            0.05 ether,
            5 ether
        );
        imdo.transfer(alice, 1e18);
        vm.startPrank(alice);
        imdo.approve(address(staking), type(uint256).max);
        staking.stake(1e18);
        vm.stopPrank();
    }

    function _spot() internal view returns (uint160 p) {
        (p,,,) = IPoolManager(address(manager)).getSlot0(imdKey.toId());
    }

    function _limitSwap(bool zeroForOne, uint160 limit, uint256 ethValue) internal {
        swapRouter.swap{value: ethValue}(
            imdKey,
            SwapParams({zeroForOne: zeroForOne, amountSpecified: -int256(1e30), sqrtPriceLimitX96: limit}),
            PoolSwapTest.TestSettings({takeClaims: false, settleUsingBurn: false}),
            ""
        );
    }

    function _fund(uint256 amount) internal {
        (bool ok,) = address(treasury).call{value: amount}("");
        require(ok);
    }

    function _floorNow() internal view returns (uint256) {
        ImdoTreasury.Leg memory l = treasury.leg(0);
        return FullMath.mulDiv(l.checkpointSqrtPriceX96, 7 days, 7 days + vm.getBlockTimestamp() - l.checkpointAt);
    }

    function test_repeatedDustPinsRatchetTheFloorAboveSpotForDays() public {
        _fund(1 ether);
        treasury.process(); // honest buy anchors the checkpoint at market
        uint160 market = _spot();
        uint256 cp0 = treasury.leg(0).checkpointSqrtPriceX96;
        // twelve cooldowns: sell IMD until the sqrt-price clears the next ceiling, let the treasury buy ~1 gwei
        // there, buy back to market. Each pin lifts the checkpoint by the full MAX_CHECKPOINT_RISE_BPS step.
        for (uint256 r; r < 12; ++r) {
            vm.warp(vm.getBlockTimestamp() + 600);
            uint160 target = uint160(_floorNow() * 103 / 100);
            if (target > _spot()) _limitSwap(false, target, 0);
            _fund(3 gwei);
            treasury.process();
            assertEq(treasury.leg(0).pending, 0, "dust buy fills at the pushed price");
            _limitSwap(true, market, 5000 ether);
        }
        uint256 cp = treasury.leg(0).checkpointSqrtPriceX96;
        emit log_named_uint("checkpoint / original checkpoint (bps)", cp * 10_000 / cp0);
        emit log_named_uint("checkpoint / market (bps)", cp * 10_000 / market);
        // the pool is back at market; the IMD leg must be live again within a day
        uint256 failed;
        bool bought;
        for (uint256 i; i < 144 && !bought; ++i) {
            vm.warp(vm.getBlockTimestamp() + 600);
            _fund(0.01 ether);
            uint256 before = imd.balanceOf(address(staking));
            treasury.process();
            if (imd.balanceOf(address(staking)) > before) bought = true;
            else ++failed;
        }
        emit log_named_uint("failed process() calls before recovery", failed);
        assertTrue(bought, "IMD leg stalled for more than a day after twelve dust pins");
    }
}
```

### 2. Low: Refresh clamps the treasury's own price impact out of the checkpoint: without counter-flow the IMD leg stalls after four max-size buys (regression vs 8f2430e)

`src/ImdoTreasury.sol:362`

```
        if (next < floorNow) next = floorNow;
```

Before e28a1f9 the refresh copied the post-swap spot, so the sqrt-price drop caused by the treasury's own buy was absorbed into the next floor. Now next = max(post, floorNow), so each 1 ETH buy's own impact (0.39% of sqrt-price at the 200 ETH test depth, ~0.14-0.18% at the mainnet pool's depth) must be covered by the decay (0.099% per 600 s) plus the 300 bps slippage slack (~1.5% of sqrt-price). When the ETH/IMD pool is the market and nobody arbitrages the price back between cooldowns, floor/spot grows ~0.3% per round and the fifth buy fails InsufficientOutput; the cap halves, a half buy fills, and the leg degrades to roughly the decay rate. Over 24 rounds of maximum inflow (2.5126 ETH per cooldown) 11 of 24 IMD legs fail and 30.5 ETH sits pending; on the parent commit 8f2430e the identical test fills all 24 (14.5 ETH pending, the per-buy cap alone). The same mechanism follows any honest downward sqrt-price drift (IMD rallying) faster than ~10 bps per cooldown, although every single step is far inside the 3% slippage band: the leg then follows the market only at the decay rate. This answers the brief's question: no honest move stalls the leg longer than the 7-day decay implies, but the treasury's own demand is now charged against that decay budget, which the comment at line 355 ('Genuine moves still pass through') does not say. Delay only; no ETH is lost. Merged from audit_flow, audit_economics and audit_permissions. Fix options that keep the sandwich bound: allow the refresh to absorb the buy's own measured impact, next = max(post, floorNow * post / pre) only when the pre-swap spot pre >= floorNow (an unsandwiched buy; a front-run that lowers pre below floorNow gets no allowance), or shorten CHECKPOINT_DECAY; otherwise document the ~0.1%/cooldown tracking limit in README 'Operational risks'.

**Reproduction**

Fixture of test/unit/CheckpointRefresh.t.sol. Loop 24 times: warp +600 s; send 2.5126 ETH to the treasury; process(); do nothing else to the pool. Expected (design: 1 ETH buy every cooldown while pending >= 1 ETH): 24 LegBought. Actual on this tree: floor/spot after rounds 1-4 = 10039, 10078, 10118, 10157 bps; round 5 emits LegFailed(InsufficientOutput) and retryCap = 0.5 ETH; 11 of 24 rounds fail; pending = 30.5 ETH. Same test on a worktree of 8f2430e: 0 of 24 fail. Attached proof test/scratch/OwnImpact.t.sol fails here with '11 != 0'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "@uniswap/v4-core/src/PoolManager.sol";
import {IPoolManager} from "@uniswap/v4-core/src/interfaces/IPoolManager.sol";
import {IHooks} from "@uniswap/v4-core/src/interfaces/IHooks.sol";
import {PoolKey} from "@uniswap/v4-core/src/types/PoolKey.sol";
import {PoolIdLibrary} from "@uniswap/v4-core/src/types/PoolId.sol";
import {Currency, CurrencyLibrary} from "@uniswap/v4-core/src/types/Currency.sol";
import {ModifyLiquidityParams} from "@uniswap/v4-core/src/types/PoolOperation.sol";
import {TickMath} from "@uniswap/v4-core/src/libraries/TickMath.sol";
import {StateLibrary} from "@uniswap/v4-core/src/libraries/StateLibrary.sol";
import {PoolModifyLiquidityTest} from "@uniswap/v4-core/src/test/PoolModifyLiquidityTest.sol";
import {LiquidityAmounts} from "@uniswap/v4-periphery/src/libraries/LiquidityAmounts.sol";
import {MockERC20} from "solmate/src/test/utils/mocks/MockERC20.sol";
import {IMDOToken} from "src/IMDOToken.sol";
import {ImdoStaking} from "src/ImdoStaking.sol";
import {ImdoTreasury} from "src/ImdoTreasury.sol";

/// Regression of commit e28a1f9: the refresh clamps the treasury's own price impact out of the checkpoint, so a run
/// of max-size buys with no counter-flow drifts the pool under the floor and the IMD leg starts failing. On the parent
/// commit (refresh = post-swap spot) all 24 rounds fill.
contract OwnImpactProof is Test {
    using PoolIdLibrary for PoolKey;
    using StateLibrary for IPoolManager;

    PoolManager manager;
    PoolModifyLiquidityTest lpRouter;
    MockERC20 imd;
    IMDOToken imdo;
    ImdoStaking staking;
    ImdoTreasury treasury;
    PoolKey imdKey;
    address alice = makeAddr("alice");

    receive() external payable {}

    function setUp() public {
        vm.warp(1_800_000_000);
        manager = new PoolManager(address(this));
        lpRouter = new PoolModifyLiquidityTest(manager);
        vm.deal(address(this), 100_000 ether);
        imd = new MockERC20("Identity.md", "IMD", 18);
        imd.mint(address(this), 1e36);
        imd.approve(address(lpRouter), type(uint256).max);
        imdKey = PoolKey(CurrencyLibrary.ADDRESS_ZERO, Currency.wrap(address(imd)), 10000, 200, IHooks(address(0)));
        uint160 sqrtP = TickMath.getSqrtPriceAtTick(54000);
        manager.initialize(imdKey, sqrtP);
        uint128 liquidity = LiquidityAmounts.getLiquidityForAmounts(
            sqrtP,
            TickMath.getSqrtPriceAtTick(-887200),
            TickMath.getSqrtPriceAtTick(887200),
            200 ether,
            type(uint128).max
        );
        lpRouter.modifyLiquidity{value: 200 ether}(
            imdKey, ModifyLiquidityParams(-887200, 887200, int256(uint256(liquidity)), 0), ""
        );
        imdo = new IMDOToken();
        staking =
            new ImdoStaking(address(imdo), address(imd), address(manager), makeAddr("claim"), makeAddr("regenSafe"));
        treasury = new ImdoTreasury(
            address(staking),
            makeAddr("ops"),
            makeAddr("offsets"),
            makeAddr("regenSafe"),
            address(manager),
            address(imd),
            10000,
            200,
            address(0),
            1 ether,
            300,
            600,
            0.5 ether,
            0.05 ether,
            5 ether
        );
        imdo.transfer(alice, 1e18);
        vm.startPrank(alice);
        imdo.approve(address(staking), type(uint256).max);
        staking.stake(1e18);
        vm.stopPrank();
    }

    function test_maxRateInflowWithoutCounterflowKeepsBuying() public {
        uint256 failed;
        for (uint256 r; r < 24; ++r) {
            vm.warp(vm.getBlockTimestamp() + 600);
            (bool ok,) = address(treasury).call{value: 2.5126 ether}("");
            require(ok);
            uint256 before = imd.balanceOf(address(staking));
            treasury.process(); // nobody else trades the pool between cooldowns
            if (imd.balanceOf(address(staking)) == before) ++failed;
        }
        emit log_named_uint("failed IMD legs out of 24", failed);
        emit log_named_uint("pending ETH", treasury.leg(0).pending);
        assertEq(failed, 0, "treasury's own impact stalled the IMD leg with no adverse flow");
    }
}
```

### 3. Low: Floor-clamped refresh resets the decay anchor, so under repeated sandwiched buys the floor decays geometrically, below the documented 7-day hyperbola

`src/ImdoTreasury.sol:365`

```
        l.checkpointAt = uint64(block.timestamp);
```

When the post-swap price is under the floor, _refreshCheckpoint writes checkpointSqrtPriceX96 = floorNow and unconditionally checkpointAt = block.timestamp. The current floor is unchanged, but its future slope steepens from -floorNow/(7d+age) to -floorNow/7d: after N sandwiched buys spaced dt apart the enforced floor is cp0 * (7d/(7d+dt))^N instead of the cp0 * 7d/(7d+N*dt) that README.md and the function comment ('downward via the 7-day decay') describe. For dt = 600 s: N = 20 gives 0.9803 vs 0.9806 (why CheckpointRefresh.t.sol cannot see it), N = 432 (3 days) 0.651 vs 0.700, N = 1008 (7 days) 0.368 vs 0.500 of cp0 in sqrt-price, i.e. the bound on how far a persistent sandwicher can push the treasury's accepted price widens faster than stated (7.4x fewer IMD per ETH at a week versus the documented 4x). Stakers receive the shortfall; it is bounded by pool depth and round-trip fees as described in the sandwich finding below. From audit_math; reproduced with the attached proof. Fix: when the clamp lands on floorNow (no genuine upward move) leave checkpointSqrtPriceX96 and checkpointAt untouched so the floor continues from the original anchor; only advance the anchor when next > floorNow. The judge's two CheckpointRefresh tests remain valid under that change.

**Reproduction**

Fixture of test/unit/CheckpointRefresh.t.sol. One honest 1 ETH process() anchors cp0 at t0. Then 432 rounds: warp +600 s, fund 1 ETH, buy IMD until spot = 0.991 * floorNow, process() (fills), sell back to market. Expected: enforced floor >= cp0 * 7d / (7d + 259200 s) = 0.6999 cp0. Actual: 0.6515 cp0 (768036953006014633935250631937 vs 824289157495641637278626311288). Attached proof fails on this tree with 'floor fell below cp0 * 7d / (7d + elapsed)'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "@uniswap/v4-core/src/PoolManager.sol";
import {IPoolManager} from "@uniswap/v4-core/src/interfaces/IPoolManager.sol";
import {IHooks} from "@uniswap/v4-core/src/interfaces/IHooks.sol";
import {PoolKey} from "@uniswap/v4-core/src/types/PoolKey.sol";
import {PoolIdLibrary} from "@uniswap/v4-core/src/types/PoolId.sol";
import {Currency, CurrencyLibrary} from "@uniswap/v4-core/src/types/Currency.sol";
import {SwapParams, ModifyLiquidityParams} from "@uniswap/v4-core/src/types/PoolOperation.sol";
import {TickMath} from "@uniswap/v4-core/src/libraries/TickMath.sol";
import {StateLibrary} from "@uniswap/v4-core/src/libraries/StateLibrary.sol";
import {FullMath} from "@uniswap/v4-core/src/libraries/FullMath.sol";
import {PoolSwapTest} from "@uniswap/v4-core/src/test/PoolSwapTest.sol";
import {PoolModifyLiquidityTest} from "@uniswap/v4-core/src/test/PoolModifyLiquidityTest.sol";
import {LiquidityAmounts} from "@uniswap/v4-periphery/src/libraries/LiquidityAmounts.sol";
import {MockERC20} from "solmate/src/test/utils/mocks/MockERC20.sol";
import {IMDOToken} from "src/IMDOToken.sol";
import {ImdoStaking} from "src/ImdoStaking.sol";
import {ImdoTreasury} from "src/ImdoTreasury.sol";

/// @notice `_refreshCheckpoint` writes `checkpointSqrtPriceX96 = floorNow` and `checkpointAt = now` whenever the
/// post-swap price sits under the floor. Each refresh therefore restarts the 7-day hyperbola from a lower anchor:
/// after N sandwiched buys spaced dt apart the enforced floor is cp0 * prod(7d / (7d + dt)) = cp0 * (7d/(7d+dt))^N,
/// a geometric decay, instead of the documented cp0 * 7d / (7d + N*dt). Three days of 600 s rounds give 0.651 vs
/// 0.700 of the original checkpoint (sqrt price), i.e. the treasury accepts ~15% fewer IMD per ETH than the stated
/// decay allows. The test asserts the floor never falls under the documented hyperbola.
contract FloorCompoundsTest is Test {
    using PoolIdLibrary for PoolKey;
    using StateLibrary for IPoolManager;

    PoolManager manager;
    PoolSwapTest swapRouter;
    PoolModifyLiquidityTest lpRouter;
    MockERC20 imd;
    IMDOToken imdo;
    ImdoStaking staking;
    ImdoTreasury treasury;
    PoolKey imdKey;
    address alice = makeAddr("alice");

    receive() external payable {}

    function setUp() public {
        vm.warp(1_800_000_000);
        manager = new PoolManager(address(this));
        swapRouter = new PoolSwapTest(manager);
        lpRouter = new PoolModifyLiquidityTest(manager);
        vm.deal(address(this), 100_000 ether);
        imd = new MockERC20("Identity.md", "IMD", 18);
        imd.mint(address(this), 1e36);
        imd.approve(address(lpRouter), type(uint256).max);
        imd.approve(address(swapRouter), type(uint256).max);
        imdKey = PoolKey(CurrencyLibrary.ADDRESS_ZERO, Currency.wrap(address(imd)), 10000, 200, IHooks(address(0)));
        uint160 sqrtP = TickMath.getSqrtPriceAtTick(54000);
        manager.initialize(imdKey, sqrtP);
        uint128 liquidity = LiquidityAmounts.getLiquidityForAmounts(
            sqrtP,
            TickMath.getSqrtPriceAtTick(-887200),
            TickMath.getSqrtPriceAtTick(887200),
            200 ether,
            type(uint128).max
        );
        lpRouter.modifyLiquidity{value: 200 ether}(
            imdKey, ModifyLiquidityParams(-887200, 887200, int256(uint256(liquidity)), 0), ""
        );
        imdo = new IMDOToken();
        staking =
            new ImdoStaking(address(imdo), address(imd), address(manager), makeAddr("claim"), makeAddr("regenSafe"));
        treasury = new ImdoTreasury(
            address(staking),
            makeAddr("ops"),
            makeAddr("offsets"),
            makeAddr("regenSafe"),
            address(manager),
            address(imd),
            10000,
            200,
            address(0),
            1 ether,
            300,
            600,
            0.5 ether,
            0.05 ether,
            5 ether
        );
        imdo.transfer(alice, 1e18);
        vm.startPrank(alice);
        imdo.approve(address(staking), type(uint256).max);
        staking.stake(1e18);
        vm.stopPrank();
    }

    function _spot() internal view returns (uint160 p) {
        (p,,,) = IPoolManager(address(manager)).getSlot0(imdKey.toId());
    }

    function _limitSwap(bool zeroForOne, uint160 limit, uint256 ethValue) internal {
        swapRouter.swap{value: ethValue}(
            imdKey,
            SwapParams({zeroForOne: zeroForOne, amountSpecified: -int256(1e30), sqrtPriceLimitX96: limit}),
            PoolSwapTest.TestSettings({takeClaims: false, settleUsingBurn: false}),
            ""
        );
    }

    function _fund(uint256 amount) internal {
        (bool ok,) = address(treasury).call{value: amount}("");
        require(ok);
    }

    function _floorNow() internal view returns (uint256) {
        ImdoTreasury.Leg memory l = treasury.leg(0);
        return FullMath.mulDiv(l.checkpointSqrtPriceX96, 7 days, 7 days + vm.getBlockTimestamp() - l.checkpointAt);
    }

    function test_sandwichedRefreshesCompoundTheDecayBelowTheDocumentedHyperbola() public {
        _fund(1 ether);
        treasury.process(); // honest buy: the checkpoint is anchored at (cp0, t0)
        uint160 market = _spot();
        uint256 cp0 = treasury.leg(0).checkpointSqrtPriceX96;
        uint256 t0 = vm.getBlockTimestamp();
        // three days of cooldown-spaced buys, each pushed 0.9% under the floor the treasury enforces
        for (uint256 r; r < 432; ++r) {
            vm.warp(vm.getBlockTimestamp() + 600);
            _fund(1 ether);
            uint160 target = uint160(_floorNow() * 991 / 1000);
            if (target < _spot()) _limitSwap(true, target, 5000 ether);
            treasury.process();
            assertEq(treasury.leg(0).pending, 0, "treasury buy must still fill");
            _limitSwap(false, market, 0);
        }
        uint256 elapsed = vm.getBlockTimestamp() - t0;
        uint256 documented = FullMath.mulDiv(cp0, 7 days, 7 days + elapsed); // cp0 * 7d / (7d + 3d) = 0.700 cp0
        uint256 enforced = _floorNow();
        emit log_named_uint("elapsed seconds", elapsed);
        emit log_named_uint("documented floor / cp0 (bps)", documented * 10_000 / cp0);
        emit log_named_uint("enforced floor / cp0 (bps)", enforced * 10_000 / cp0);
        // The 7-day decay is the stated bound on how far a sandwich may lower the floor. Allow 0.1% rounding.
        assertGe(enforced, documented * 999 / 1000, "floor fell below cp0 * 7d / (7d + elapsed)");
    }
}
```

### 4. Low: Anti-snipe fee clock starts at any first swap, including a 1 wei buy that pays no fee, so the 20% launch fee can be bypassed before the announced launch

`src/ImdoHook.sol:174`

```
        if (launchTimestamp == 0) {
```

beforeSwap records launchTimestamp on the first swap regardless of size. A 1 wei exact-input buy computes fee = 1 * 2000 / 10000 = 0, takes nothing, and starts the 30-minute linear decay (the project's own test helper LocalV4.warpPastDecay relies on exactly this). script/DeployImdo.s.sol initializes and seeds the ETH/IMDO pool at deployment, at least MIN_LAUNCH_LEAD (1 hour) before the claim `launch`, and nothing gates swaps before `launch`. A bot watching the deployer can therefore start the clock in the pool-creation block and 30 minutes later buy at the 150 bps steady fee, before the claim window the project announces opens, so the 20% launch fee never applies to the trades it was meant to tax. Nothing is lost by the contracts; the treasury forgoes the anti-snipe premium and the documented schedule ('20.00% at the first filled swap' in the contract header) does not describe what happens. From audit_flow; reproduced with the attached proof on a fresh pool. Minimal fix that keeps the schedule: anchor the decay to an immutable launch timestamp passed to the hook (the same `launch` the claim uses), with swaps before it paying LAUNCH_FEE_BPS flat; or require the clock-starting swap to carry at least a minimum ETH amount.

**Reproduction**

Fresh PoolManager, ImdoHook mined with flags 0x20cc, ETH/IMDO pool at tick 177240 seeded with 890M IMDO single-sided (the script's layout), launchTimestamp == 0, currentFeeBps() == 2000. Swap zeroForOne exact input 1 wei: fees taken (treasury balance + deferred ERC-6909 claims) unchanged at 0, launchTimestamp == block.timestamp. Warp +30 minutes: currentFeeBps() == 150. Buy with 10 ETH. Expected under the documented schedule: 2 ETH fee. Actual: 0.15 ETH (150000000000000000 wei). Attached proof test/scratch/HookClockProof.t.sol fails with '150000000000000000 != 2000000000000000000'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "@uniswap/v4-core/src/PoolManager.sol";
import {IPoolManager} from "@uniswap/v4-core/src/interfaces/IPoolManager.sol";
import {IHooks} from "@uniswap/v4-core/src/interfaces/IHooks.sol";
import {PoolKey} from "@uniswap/v4-core/src/types/PoolKey.sol";
import {Currency, CurrencyLibrary} from "@uniswap/v4-core/src/types/Currency.sol";
import {SwapParams, ModifyLiquidityParams} from "@uniswap/v4-core/src/types/PoolOperation.sol";
import {TickMath} from "@uniswap/v4-core/src/libraries/TickMath.sol";
import {PoolSwapTest} from "@uniswap/v4-core/src/test/PoolSwapTest.sol";
import {PoolModifyLiquidityTest} from "@uniswap/v4-core/src/test/PoolModifyLiquidityTest.sol";
import {LiquidityAmounts} from "@uniswap/v4-periphery/src/libraries/LiquidityAmounts.sol";
import {IMDOToken} from "src/IMDOToken.sol";
import {ImdoHook} from "src/ImdoHook.sol";
import {HookMiner} from "script/utils/HookMiner.sol";

/// The anti-snipe clock starts at any first swap, including a 1 wei buy whose fee rounds to zero.
contract HookClockProof is Test {
    PoolManager poolManager;
    PoolSwapTest swapRouter;
    PoolModifyLiquidityTest lpRouter;
    IMDOToken imdo;
    ImdoHook hook;
    PoolKey key;
    address hookOwner = makeAddr("hookOwner");
    address treasury = makeAddr("treasury");

    receive() external payable {}

    function setUp() public {
        vm.warp(1_800_000_000);
        poolManager = new PoolManager(address(this));
        swapRouter = new PoolSwapTest(poolManager);
        lpRouter = new PoolModifyLiquidityTest(poolManager);
        vm.deal(address(this), 10_000 ether);
        imdo = new IMDOToken();
        bytes memory args = abi.encode(address(poolManager), address(imdo), treasury, hookOwner);
        (, bytes32 salt) = HookMiner.find(address(this), 0x20cc, type(ImdoHook).creationCode, args);
        hook = new ImdoHook{salt: salt}(poolManager, address(imdo), treasury, hookOwner);
        key = PoolKey(CurrencyLibrary.ADDRESS_ZERO, Currency.wrap(address(imdo)), 0, 60, IHooks(address(hook)));
        vm.prank(hookOwner);
        poolManager.initialize(key, TickMath.getSqrtPriceAtTick(177240));
        uint128 liquidity = LiquidityAmounts.getLiquidityForAmount1(
            TickMath.getSqrtPriceAtTick(108180), TickMath.getSqrtPriceAtTick(177240), 890_000_000e18
        );
        imdo.approve(address(lpRouter), type(uint256).max);
        lpRouter.modifyLiquidity(key, ModifyLiquidityParams(108180, 177240, int256(uint256(liquidity)), 0), "");
    }

    function _buy(uint256 ethIn) internal {
        swapRouter.swap{value: ethIn}(
            key,
            SwapParams({zeroForOne: true, amountSpecified: -int256(ethIn), sqrtPriceLimitX96: TickMath.MIN_SQRT_PRICE + 1}),
            PoolSwapTest.TestSettings({takeClaims: false, settleUsingBurn: false}),
            ""
        );
    }

    /// Fees paid directly to the treasury plus fees deferred as ERC-6909 claims (fresh manager without ETH).
    function _feesTaken() internal view returns (uint256) {
        return treasury.balance + poolManager.balanceOf(address(hook), 0);
    }

    function test_oneWeiSwapStartsDecayAndFirstRealBuyerPaysSteadyFee() public {
        assertEq(hook.launchTimestamp(), 0);
        assertEq(hook.currentFeeBps(), 2000);
        _buy(1); // fee = 1 * 2000 / 10000 = 0; nothing is taken or deferred
        assertEq(_feesTaken(), 0, "no fee taken by the clock-starting swap");
        assertEq(hook.launchTimestamp(), vm.getBlockTimestamp(), "decay clock started by a fee-less swap");
        vm.warp(vm.getBlockTimestamp() + 30 minutes);
        assertEq(hook.currentFeeBps(), 150);
        _buy(10 ether);
        emit log_named_uint("fee paid by the first real buyer (wei)", _feesTaken());
        // Documented schedule: 20% at the first filled swap. The first real buyer should pay 2 ETH.
        assertEq(_feesTaken(), 2 ether, "first real buy paid the steady 1.5% fee instead of the 20% launch fee");
    }
}
```

### 5. Low: forge fmt --check fails on test/unit/CheckpointRefresh.t.sol (added by e28a1f9); docs/REVIEW.md verification table is stale

`test/unit/CheckpointRefresh.t.sol:59`

```
            sqrtP, TickMath.getSqrtPriceAtTick(-887200), TickMath.getSqrtPriceAtTick(887200), 200 ether, type(uint128).max
```

README.md 'Verification' and test/TESTING.md make `forge fmt --check` with the unchanged configuration part of the required gate, and docs/REVIEW.md:36 records it as 'Passed'. On this tree it exits 1: line 59 is 122 characters (foundry.toml [fmt] line_length = 120), so the getLiquidityForAmounts argument list must be split one argument per line (lines 58-60), and the ImdoStaking construction at lines 65-67 must collapse onto a single continuation line. Both statements were introduced by e28a1f9; src/, script/ and every other test file are clean. docs/REVIEW.md:35 also still reports '83 passed ... across 14 local suites' while the default suite now runs 101 tests in 19 suites. Reported identically by all four specialists; merged. Fix: `forge fmt test/unit/CheckpointRefresh.t.sol` (whitespace only) and refresh the counts in docs/REVIEW.md.

**Reproduction**

Run `forge fmt --check` at the repository root with forge 1.8.3. Expected: exit 0. Actual: exit 1 with 'Diff in test/unit/CheckpointRefresh.t.sol' showing two hunks (lines 58-60 and 65-67). `forge test` on the same tree: 101 passed, 0 failed, 0 skipped across 19 suites.

### 6. Info: Persistent sandwiching still holds the floor below market after an honest IMD drop: the refresh never rises while every buy is front-run to the floor (inherited; improved vs parent; fee-bounded at mai

`src/ImdoTreasury.sol:285`

```
        if (sqrtPriceX96 < checkpointFloor) sqrtPriceX96 = uint160(checkpointFloor);
```

After a move that leaves spot above the floor (an honest IMD sale, or the floor's own decay during a pause), the checkpoint only rises when a buy's post-swap price exceeds floorNow. A front-runner who buys IMD down to just under the floor before each process() makes the treasury quote at the floor and leaves post < floorNow, so the refresh writes floorNow every time and the gap never closes (it widens 0.1% per cooldown). The treasury then pays the whole honest gap plus the 300 bps band on every sandwiched buy, for as long as the sandwicher is willing to be the keeper. This is not a regression: the parent additionally ratcheted the floor down (same test on 8f2430e: checkpoint 75.5% of market and 3187 bps average shortfall, versus 89.8% and 2041 bps here), and it is bounded by pool depth: moving the sqrt-price by a gap g costs ~2 * 1.1% * g * depth in round-trip fees against ~2 * g * ethIn of extraction, so with maxEthPerBuy = 1 ETH it is unprofitable while in-range virtual ETH depth exceeds ~90-110 ETH (564-692 ETH on the mainnet pool at blocks 26,137,698-26,137,750 per the specialists' reads), unless the attacker owns most of the in-range liquidity. Merged from audit_flow, audit_economics and audit_permissions. Keep maxEthPerBuy small relative to pool depth, state the depth assumption in README next to the existing manipulation caveat, and monitor CheckpointRefreshed for repeated post < checkpoint rounds. A design-level option is to let the rise bound scale with cooldowns elapsed since the last upward refresh, so honest gaps close faster when buys are infrequent.

**Reproduction**

test/scratch/Residual.t.sol::test_sandwichedBuysNeverLiftStaleFloor (passes; demonstrates the behaviour). Fixture of CheckpointRefresh.t.sol: honest 1 ETH buy (cp0); third party sells IMD until sqrt-price = 1.10 cp0 (market). 12 rounds: warp +600 s, fund 2.5126 ETH, buy IMD with limit floor * 0.99, process() (fills), sell back to market. Expected by the commit comment ('upward in bounded steps per buy'): checkpoint rises up to 2% per filled buy toward market. Actual: checkpoint/cp0 = 9881 bps, checkpoint/market = 8983 bps, average IMD shortfall vs the market quote 2041 bps per buy. On 8f2430e: 8300 / 7546 / 3187 bps.

### 7. Info: Checkpoint seed at construction (and at first process()) is an unclamped spot read: a sandwiched treasury creation pins the floor above market for 7d x (push - 1)

`src/ImdoTreasury.sol:151`

```
            (_imdLeg.checkpointSqrtPriceX96,,,) = poolManager.getSlot0(_imdLeg.key.toId());
```

_refreshCheckpoint bounds every later move, but the initial reference copies slot0 with no bound, both in the constructor (line 151) and in _ensurePool (line 384) when the pool did not exist at construction. DeployImdo creates the treasury as the fourth broadcast transaction with calldata visible in the public mempool; a seller who pushes the sqrt-price up by a factor g around that block and buys back leaves checkpointSqrtPriceX96 = g x market, so every IMD buy fails until the decay closes the gap: about 7 d x (g - 1): 3.4 h for g = 1.02, 1.4 d for 1.2, 3.5 d for 1.5. Pure griefing (ETH stays pending; cost is round-trip fees on (g - 1) x the pool's reserve, ~2.5 ETH for g = 1.2 at mainnet depth). Merged from audit_math and audit_permissions. Mitigation: deploy through a private relay, or give the constructor an operator-reviewed expected sqrt-price and revert (or clamp to +/-2%) when slot0 is outside it, or seed with checkpointAt pre-aged so the first days enforce spot only. A lazy seed at first process() does not help because that call is equally sandwichable. No proof attached: a fix needs a constructor argument the current signature lacks.

**Reproduction**

test/scratch/Residual.t.sol::test_constructionSeedIsUnclampedSpot (fails on this tree with '183 >= 6'). Fixture of CheckpointRefresh.t.sol: sell IMD with sqrtPriceLimit = spot x 1.2; construct ImdoTreasury with the script's arguments; buy IMD back to the original spot; leg(0).checkpointSqrtPriceX96 / market = 11999 bps. Then fund 0.01 ETH and process() every 600 s. Expected: a fresh treasury buys at market within an hour. Actual: 183 consecutive failed calls (30 h) before the first LegBought.

### 8. Info: MIN_LAUNCH_LEAD is checked only at simulation time: a claim creation mined after `launch` still burns the predicted address; the Permit2 expiry and LP-mint deadline share the same one-hour horizon; no

`script/DeployImdo.s.sol:153`

```
                || c.seatNFT.code.length == 0 || c.launch < block.timestamp + MIN_LAUNCH_LEAD
```

The lead removes the hazard the parent judge named (a launch at or just after simulation time) and test_scriptRequiresLaunchLeadBeforeAnyCreation proves the boundary. It is a minimum, not a guarantee: preflight runs on the simulation block while token, staking and claim are three separate broadcast transactions. If the claim creation is mined at or after `launch` (hardware-wallet signing of ~14 transactions, under-priced gas, an RPC stall, an operator pausing between dry run and --broadcast, or --resume after a gap, which does not re-run preflight), ImdoClaim's constructor reverts on `launch_ < block.timestamp` (src/ImdoClaim.sol:56), the nonce is consumed, and ImdoStaking.claimContract points at an address that can never receive code, so token and staking must be redeployed (docs/DEPLOYMENT.md says so). Lines 129 and 137 give the Permit2 allowance and modifyLiquidities a deadline of simulation block.timestamp + 1 hours, so a stall of an hour also breaks the sequence at transactions 8/9, recoverably. There is also no upper bound on `launch`: a value years ahead passes preflight and locks the 110M claim funding until then. Answer to the brief: the lead is sufficient for an uninterrupted broadcast and the residual is operational. Merged from all four specialists. Options: raise MIN_LAUNCH_LEAD together with the two deadlines (or derive both from c.launch), add a sanity upper bound, and state in DEPLOYMENT.md: re-simulate immediately before broadcasting and never --resume across a gap. Structural alternatives are design changes for the requester: drop the constructor's launch_ < block.timestamp check (preflight already enforces the lead) or create staking and claim from one factory in a single transaction.

**Reproduction**

test/scratch/DeployLead.t.sol::test_claimMinedAfterLaunchBurnsPredictedAddress (passes; demonstrates the boundary). T = 1_800_000_000, launch = T + 1 hours (exactly what preflight accepts). tx1 from deployer: new IMDOToken(). tx2: new ImdoStaking(token, imd, pm, computeCreateAddress(deployer, nonce + 1), regenSafe). Warp to launch + 1 and send tx3: new ImdoClaim(token, staking, seatNFT, 2000, 0, launch). Actual: tx3 reverts InvalidConfiguration; staking.claimContract() == expectedClaim with code.length == 0; a retry with launch + 1 days lands at a different address. Also: ImdoDeployTest passes with c.launch = now + 100 years (no upper bound).

### 9. Info: Hook CREATE2 through the permissionless deterministic deployer can be replayed ahead of the operator: the identical hook lands first and the operator's transaction reverts, halting the broadcast

`script/DeployImdo.s.sol:115`

```
            new ImdoHook{salt: salt}(IPoolManager(c.poolManager), address(d.token), address(d.treasury), c.deployer);
```

Under broadcast this creation is a call to 0x4e59b44847b379578588920cA78FbF26c0B4956C with salt ++ initcode, visible in the mempool; the factory binds no sender, so anyone can send the same calldata first. The replayed hook is byte-identical (owner = c.deployer, same treasury and token), so no authority is lost, but the operator's transaction 5 then reverts (the factory reverts when CREATE2 returns zero on a collision, consuming the forwarded gas) and Foundry stops the sequence with token, staking, claim and treasury already live. A fresh `forge script` run starts over with new nonces and a new treasury address, abandoning the first four contracts; HookMiner.find (script/utils/HookMiner.sol:39) only returns salts whose address has no code, so a re-simulation silently mines the next salt and never shows the on-chain revert. Gas-only impact before any public trading. From audit_permissions; reproduced. Mitigation: send the sequence through a private relay/bundle, or use a sender-bound CREATE2 factory (salt prefixed with the deployer address) so a replay from another account lands elsewhere; at minimum document the recovery (the pre-landed hook is usable as-is if the operator continues the sequence manually with it).

**Reproduction**

test/scratch/DeployLead.t.sol::test_hookCreate2CanBeReplayedAheadOfTheOperator (passes; demonstrates the behaviour). Etch the canonical deterministic-deployer runtime at 0x4e59...956C; from the deployer's pending nonce compute token = createAddress(nonce), treasury = createAddress(nonce + 3), (expectedHook, salt) = HookMiner.find(factory, 0x20cc, creationCode, abi.encode(pm, token, treasury, deployer)). A griefer calls the factory with salt ++ creationCode ++ args first: expectedHook has code, owner() == deployer, treasury() == the intended treasury. A subsequent script.run(c) deploys a hook at a different address (HookMiner skipped the occupied one) while the operator's original calldata replayed from the deployer with 3M gas fails (CREATE2 collision).

---

Judge's submission `a41c0a18803d6a07851d0403d8d3a65b2b8b54951788547763e00d9b88bffb90`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
