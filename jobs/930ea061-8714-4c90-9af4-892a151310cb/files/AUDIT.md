# Audit report

> X: https://x.com/imdplace
> v3.2, follow-up to audit 85083c05. Full adversarial review before the token launch.
>
> 1. Build and test under both profiles: the protected foundry.toml (via_ir = true) and the launch profile (FOUNDRY_VIA_IR=false FOUNDRY_BYTECODE_HASH=none, optimizer 200 runs, solc 0.8.26, cancun). Confirm GACHA_RUNTIME_CODE_HASH 0x2db1143638494d63cd5b4b807bd3dfe333d590ea58e7204ab7fd0c5cf415c4cd matches BagGacha runtime code under the launch profile (testPinnedGachaRuntimeCodeHash).
> 2. Verify every 85083c05 fix: bindGacha preconditions against the deployed GoblinNFT (launch-1616: targetsSet, reserveTarget == vrfTarget == gacha, polTarget == gacha.polManager(), 7-day review ended, genesis().gacha()/oracle match); POL positive deltas; afterSwap PartialFill incl. exact-output rule realised == amount + fee; recorded liquidity min(current L, liquidityAt(30m)) and the genesisEthHeld bound; tokensForEth(GOLD) Math.min; genesisValueAndCap at the 4h TWAP; MIN_OUT_BPS 9475; exact-output gross fee; cancelRequest after 24h and its interaction with Curator pauses.
> 3. Hunt new issues from the changes: oracle/TWAP manipulation at minimum depth (MIN_LIQUIDITY 5 ETH, MIN_GENESIS_DEPTH 1 ETH, PAYOUT_CAP_BPS 500), payout above paid value, stuck funds, hook reentrancy, genesis lane griefing, VRF request/cancel races.
> 4. Check the manifest remainder path (paying wallet vs $contract:GoldHook) is valid for IMD.
>
> Report any medium or higher with a concrete fix. NO SOURCE CHANGES.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1545-goblin-gold.git |
| Commit | `8b769ee90e4d9189996578e1287fcd1ca32d752e` |
| Job | `930ea061-8714-4c90-9af4-892a151310cb` |
| Judged | 2026-10-14 07:03 UTC |
| Findings | 2 high · 3 medium · 1 low · 2 info |

Four agents audited the code as it is at `8b769ee`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: Genesis depth and payout cap treat concentrated liquidity as full-range: a narrow in-range position inflates both ~330x per ETH and bypasses MIN_GENESIS_DEPTH

`src/TwapOracle.sol:236`

```
        ethSide = genesisEthHeld(liquidity, sqrtPrice);
```

_checkGenesisPool bounds the liquidity term by min(current L, liquidityAt(30 min)) and converts it to ETH with genesisEthHeld(L, sqrtP) = L*2^96/sqrtP (integrated to tick 887220), i.e. the ETH a FULL-RANGE position of liquidity L holds. Uniswap v4 active liquidity is the sum of every position whose range contains the current tick, and GoldHook has no add-liquidity permission, so anyone can add a position one or two tick spacings wide through the PoolManager. Such a position carries about 1/(1-sqrt(1.0001^-120)) ~ 330x the liquidity per ETH of a full-range position while holding ~0.3% of the ETH the formula credits it with. The v3.2 recorded-liquidity rule only delays the attacker by one block plus 30 minutes (one swap in the next block records the new L; the position must still be active 30 minutes later, which the attacker ensures by keeping the price inside the range). Consequences: (1) PAYOUT_CAP_BPS (5% of ETH-side depth), the per-draw bound v3.1/v3.2 rely on against a manipulated GOLD TWAP (valueAndCap(GOLD) and genesisValueAndCap), is loosened to the tier maximum / 5% of the reserve with ~1 ETH of parked, fully recoverable capital; (2) MIN_GENESIS_DEPTH (1 ETH) is passed with ~0.03 ETH, so the Genesis lane and POL buys open on a pool whose TWAP costs almost nothing to move. Regular v3 pools are at least bounded by the pool's WETH balance (_liquidBalances); the v4 PoolManager is a singleton so no such bound exists for GOLD. Merged from two specialist reports of the same defect (audit_math, audit_permissions). Fix (keeps the design): make active liquidity equal full-range liquidity by giving GoldHook the BEFORE_ADD_LIQUIDITY permission (flags 0x30CC -> 0x38CC, re-mine the address) and reverting in beforeAddLiquidity unless params.tickLower == -887220 && params.tickUpper == 887220 (POLManager and the launch seed already use that range, so all existing depth math becomes exact). Alternative without a flag change: have TwapOracle read, via extsload of pools[id].positions[keccak256(abi.encodePacked(owner, int24(-887220), int24(887220), bytes32(0)))], the liquidity of the full-range positions of the trusted owners (POLManager and the launch seed holder) and use min(that, current L, liquidityAt(30 min)) in genesisEthHeld.

**Reproduction**

Real vendored PoolManager, GoldHook etched at a 0x30CC-flagged address, real TwapOracle(goldHook). Seed 2 ETH + 2 GOLD full range (L = 2e18 at 1:1), write 4 h of ring history with two tiny swaps: oracle.payoutCap(GOLD) = 0.0999 ETH. Attacker adds liquidity 333e18 in [tick-60, tick+60] via PoolModifyLiquidityTest, spending 0.997 ETH (+ ~1 GOLD); swaps 0.0001 ETH in the next block; warps 30 minutes; swaps once more. Expected: cap <= 5% of the ~3.5 ETH the pool now holds (<= 0.185 ETH). Actual: payoutCap(GOLD) = 16.7499 ETH and genesisValueAndCap cap = 16.7499 ETH (reported depth ~335 ETH; attacker's funds remain withdrawable). Second test: a 0.5 ETH full-range seed reverts ThinPool as designed; after the attacker adds L = 5e18 in a 120-tick range for ~0.03 ETH and waits 30 minutes, valueInEth(GOLD, 1e18) no longer reverts. Run: FOUNDRY_VIA_IR=false FOUNDRY_BYTECODE_HASH=none forge test --match-path test/scratch/ConcentratedDepthB.t.sol -vv -> both tests fail on v3.2 (verified in this review under both profiles; a second specialist proof with a 100 ETH pool gives cap 21.65 ETH vs 5.05 ETH real).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {PoolManager} from "test/v4-core/PoolManager.sol";
import {IPoolManager} from "test/v4-core/interfaces/IPoolManager.sol";
import {IHooks} from "test/v4-core/interfaces/IHooks.sol";
import {Currency} from "test/v4-core/types/Currency.sol";
import {PoolKey as CoreKey} from "test/v4-core/types/PoolKey.sol";
import {SwapParams as CoreSwap, ModifyLiquidityParams as CoreModify} from "test/v4-core/types/PoolOperation.sol";
import {PoolSwapTest} from "test/v4-core/test/PoolSwapTest.sol";
import {PoolModifyLiquidityTest} from "test/v4-core/test/PoolModifyLiquidityTest.sol";
import {GoldHook} from "src/GoldHook.sol";
import {TwapOracle} from "src/TwapOracle.sol";

contract ScratchGold is ERC20 {
    constructor() ERC20("GOLD", "GOLD") {}

    function mint(address to, uint256 a) external {
        _mint(to, a);
    }
}

contract ScratchV3Factory {
    function getPool(address, address, uint24) external pure returns (address) {
        return address(0);
    }
}

/// @notice The genesis depth (`TwapOracle._checkGenesisPool` / `genesisEthHeld`) converts the pool's *active*
///         liquidity into ETH as if every unit of it were a full-range position. A narrow position (one tick spacing
///         wide) carries roughly 330x the liquidity per ETH of a full-range one, so 1 ETH parked in a 120-tick range
///         for 30 minutes makes the oracle report hundreds of ETH of depth and lifts the 5% payout cap accordingly.
///         The same trick makes a pool below MIN_GENESIS_DEPTH priceable.
contract ConcentratedDepthTest is Test {
    uint160 constant SQRT_PRICE_1_1 = 79228162514264337593543950336;
    address constant HOOK_ADDRESS = address((uint160(0x4A) << 152) | 0x30CC);
    address factoryEOA = address(0xFAC7);
    address attacker = address(0xA77);

    PoolManager manager;
    ScratchGold gold;
    GoldHook hook;
    TwapOracle oracle;
    PoolSwapTest swapRouter;
    PoolModifyLiquidityTest lpRouter;
    CoreKey key;

    receive() external payable {}

    function setUp() public {
        vm.warp(1_800_000_000);
        manager = new PoolManager(address(this));
        gold = new ScratchGold();
        GoldHook impl = new GoldHook(address(manager), address(gold), factoryEOA);
        vm.etch(HOOK_ADDRESS, address(impl).code);
        hook = GoldHook(payable(HOOK_ADDRESS));
        swapRouter = new PoolSwapTest(IPoolManager(address(manager)));
        lpRouter = new PoolModifyLiquidityTest(IPoolManager(address(manager)));
        key = CoreKey(Currency.wrap(address(0)), Currency.wrap(address(gold)), 12500, 60, IHooks(HOOK_ADDRESS));
        oracle = new TwapOracle(
            address(this), address(0x1111), address(new ScratchV3Factory()), address(gold), HOOK_ADDRESS
        );
        vm.deal(address(this), 10_000 ether);
        vm.deal(attacker, 10 ether);
        vm.prank(factoryEOA);
        manager.initialize(key, SQRT_PRICE_1_1);
    }

    /// @dev Returns false when the PoolManager (hook) refuses the position: a fix that only admits full-range
    ///      positions makes the attacker's add revert, which is the fixed behaviour.
    function _addLiquidity(address who, int24 lower, int24 upper, int256 liquidity, uint256 eth, uint256 tokens)
        internal
        returns (bool ok)
    {
        gold.mint(who, tokens);
        vm.startPrank(who);
        gold.approve(address(lpRouter), tokens);
        try lpRouter.modifyLiquidity{value: eth}(key, CoreModify(lower, upper, liquidity, bytes32(0)), "") {
            ok = true;
        } catch {
            ok = false;
        }
        vm.stopPrank();
    }

    function _tinySwap(bool zeroForOne) internal {
        uint160 limit = zeroForOne ? 4295128739 + 1 : 1461446703485210103287273052203988822378723970342 - 1;
        if (!zeroForOne) {
            gold.mint(address(this), 1 ether);
            gold.approve(address(swapRouter), type(uint256).max);
        }
        swapRouter.swap{value: zeroForOne ? 0.0001 ether : 0}(
            key, CoreSwap(zeroForOne, -0.0001 ether, limit), PoolSwapTest.TestSettings(false, false), ""
        );
    }

    /// @dev Honest launch: 2 ETH + 2 GOLD of full-range liquidity (L = 2e18 at 1:1), history older than 4 hours.
    function _honestPool() internal {
        assertTrue(_addLiquidity(address(this), -887220, 887220, 2e18, 2 ether + 1, 2 ether + 1));
        vm.warp(vm.getBlockTimestamp() + 1 hours);
        _tinySwap(true);
        vm.warp(vm.getBlockTimestamp() + 4 hours);
        _tinySwap(false);
    }

    function testNarrowPositionInflatesGenesisDepthAndPayoutCap() public {
        _honestPool();
        uint256 honestCap = oracle.payoutCap(address(gold));
        assertApproxEqRel(honestCap, 0.1 ether, 0.02e18, "5% of 2 ETH of full-range depth");

        // Attacker: ~1 ETH + ~1 GOLD in the 120-tick range around the price, liquidity 333e18 (vs 2e18 honest).
        (, int24 tick) = hook.slot0();
        int24 lower = (tick / 60) * 60 - 60;
        if (!_addLiquidity(attacker, lower, lower + 120, 333e18, 1.5 ether, 1.5 ether)) return; // narrow add refused: fixed
        uint256 attackerEthSpent = 10 ether - attacker.balance;
        assertLt(attackerEthSpent, 1.1 ether, "about one ETH of capital");

        // a swap in the next block records the liquidity; 30 minutes later the oracle counts it
        vm.warp(vm.getBlockTimestamp() + 1);
        _tinySwap(true);
        vm.warp(vm.getBlockTimestamp() + 30 minutes);
        _tinySwap(false);

        uint256 cap = oracle.payoutCap(address(gold));
        (, uint256 genesisCap) = oracle.genesisValueAndCap(1e18);
        emit log_named_decimal_uint("honest cap (ETH)", honestCap, 18);
        emit log_named_decimal_uint("attacker ETH spent", attackerEthSpent, 18);
        emit log_named_decimal_uint("cap after narrow position (ETH)", cap, 18);
        // Expected: the pool now holds about 3.5 ETH, so the cap should be at most 5% of that.
        // Actual: the oracle reports ~335 ETH of depth and a cap of ~16 ETH, ~150x the honest cap.
        assertLe(cap, (3.5 ether * oracle.PAYOUT_CAP_BPS()) / 10_000 + 0.01 ether, "cap bounded by the ETH the pool holds");
        assertLe(genesisCap, (3.5 ether * oracle.PAYOUT_CAP_BPS()) / 10_000 + 0.01 ether, "genesis cap too");
    }

    function testNarrowPositionMakesAPoolBelowMinimumDepthPriceable() public {
        // only 0.5 ETH of full-range depth: below MIN_GENESIS_DEPTH, GOLD must stay unpriceable
        assertTrue(_addLiquidity(address(this), -887220, 887220, 0.5e18, 0.5 ether + 1, 0.5 ether + 1));
        vm.warp(vm.getBlockTimestamp() + 1 hours);
        _tinySwap(true);
        vm.warp(vm.getBlockTimestamp() + 4 hours);
        _tinySwap(false);
        vm.expectRevert(abi.encodeWithSelector(TwapOracle.ThinPool.selector, HOOK_ADDRESS));
        oracle.valueInEth(address(gold), 1e18);

        // 0.02 ETH in a 120-tick range is enough liquidity to clear the 1 ETH bound
        (, int24 tick) = hook.slot0();
        int24 lower = (tick / 60) * 60 - 60;
        if (!_addLiquidity(attacker, lower, lower + 120, 5e18, 0.03 ether, 0.03 ether)) return; // refused: fixed
        vm.warp(vm.getBlockTimestamp() + 1);
        _tinySwap(true);
        vm.warp(vm.getBlockTimestamp() + 30 minutes);
        _tinySwap(false);
        // Expected: still ThinPool (the pool holds ~0.55 ETH). Actual: priced, depth reported above 1 ETH.
        vm.expectRevert(abi.encodeWithSelector(TwapOracle.ThinPool.selector, HOOK_ADDRESS));
        oracle.valueInEth(address(gold), 1e18);
    }
}
```

### 2. High: POLManager slippage floor inverted by the finding-5 change: tokensForEth(GOLD) now returns the smaller window quote, so a 30-minute pump lets buyAndBurn/addLiquidity buy GOLD at the pumped price

`src/POLManager.sol:122`

```
        return (oracle.tokensForEth(token, ethIn) * MIN_OUT_BPS) / 10_000;
```

v3.1 TwapOracle.tokensForEth(GOLD) returned the larger token amount of the 30-minute and 4-hour windows, which is the protective direction for a buyer's minimum-output floor (a pump of one window leaves the floor at the unpumped window and the buy reverts). The v3.2 fix for finding 5 changed it to Math.min (src/TwapOracle.sol:176-177) for the GenesisVault quote, where min is right (the vault sells GOLD). POLManager._minOut still derives its floor from the same function, and for a buyer the smaller token quote is the LESS protective one: when the 30-minute TWAP is pumped above the 4-hour TWAP the floor follows the pumped window and the permissionless buyAndBurn / addLiquidity (1 ETH / 2 ETH per call, repeatable until the budget is spent) execute at the pumped price with only the 5.25% allowance against the pumped mark. README states MIN_OUT_BPS makes these revert on 'a manipulated pool'; that now only holds for a pump shorter than 30 minutes. An attacker holding GOLD pumps for 31 minutes, then loops buyAndBurn/addLiquidity and sells into the POL's buys; the POL budgets (50% of the NFT escrow, hook reserve shares, spin POL shares) are spent at an inflated price. Fix: keep min for the vault but give POLManager a floor that follows the larger of the two window quotes, e.g. add TwapOracle.polTokensForEth(uint256 ethAmount) returning Math.max(short, long) for GOLD (the v3.1 behaviour) and call it from _minOut; or compute _minOut from the 4-hour tick of genesisValueAndCap.

**Reproduction**

Real vendored PoolManager, GoldHook at a flagged address, pool seeded 100 ETH / 100 GOLD (L = 100e18), real TwapOracle(goldHook) and POLManager(oracle). 1) warp 1 h, swap 0.001 ETH; warp 4 h, swap 0.001 GOLD: tokensForEth(GOLD, 0.1 ETH) ~ 0.1 GOLD. 2) Attacker buys with 30 ETH exact input, warp 31 minutes: 30-minute mean-tick quote = 0.0598 GOLD per 0.1 ETH, 4-hour quote = 0.0936. 3) pol.depositBurn{value: 1 ether}(); pol.buyAndBurn(0.1 ether). Expected (README, v3.1): revert Slippage because the pool pays < 4-hour quote * 0.9475 = 0.0887 GOLD. Actual on v3.2: minOut = 0.0566 GOLD and the burn executes at the pumped price (~35% fewer tokens than the 4-hour TWAP). Run: FOUNDRY_VIA_IR=false FOUNDRY_BYTECODE_HASH=none forge test --match-path test/scratch/PolFloorInverted.t.sol -> fails 'next call did not revert as expected' (verified under both profiles); passes with the GOLD branch of the POL floor restored to Math.max.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {Math} from "@openzeppelin/contracts/utils/math/Math.sol";
import {PoolManager} from "test/v4-core/PoolManager.sol";
import {IPoolManager} from "test/v4-core/interfaces/IPoolManager.sol";
import {IHooks} from "test/v4-core/interfaces/IHooks.sol";
import {Currency} from "test/v4-core/types/Currency.sol";
import {PoolKey as CoreKey} from "test/v4-core/types/PoolKey.sol";
import {SwapParams as CoreSwap, ModifyLiquidityParams as CoreModify} from "test/v4-core/types/PoolOperation.sol";
import {PoolSwapTest} from "test/v4-core/test/PoolSwapTest.sol";
import {PoolModifyLiquidityTest} from "test/v4-core/test/PoolModifyLiquidityTest.sol";
import {GoldHook} from "src/GoldHook.sol";
import {TwapOracle} from "src/TwapOracle.sol";
import {POLManager} from "src/POLManager.sol";
import {TickMath} from "src/TickMath.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ScratchGold is ERC20 {
    constructor() ERC20("GOLD", "GOLD") {}

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

contract ScratchV3Factory {
    function getPool(address, address, uint24) external pure returns (address) {
        return address(0);
    }
}

/// @notice v3.2 finding 5 changed `TwapOracle.tokensForEth(GOLD)` from the larger token amount of the two windows to
///         the smaller one, for the GenesisVault quote. POLManager uses the same function as its slippage floor
///         (`minOut = tokensForEth(GOLD, ethIn) * 9475 / 10000`), where the protective direction is the opposite:
///         the floor must follow the window that gives MORE tokens, otherwise a 30-minute pump of the GOLD price
///         lowers the floor and the permissionless `buyAndBurn` / `addLiquidity` buy GOLD at the pumped price.
///         This test fails on v3.2 (the buy goes through at ~60% of the 4-hour TWAP token amount) and passes once
///         POLManager's floor again follows the larger of the two window quotes.
contract PolFloorInvertedTest is Test {
    uint160 constant SQRT_PRICE_1_1 = 79228162514264337593543950336;
    address constant HOOK_ADDRESS = address((uint160(0x4A) << 152) | 0x30CC);
    address factoryEOA = address(0xFAC7);
    address trader = address(0x7A4D);

    PoolManager manager;
    ScratchGold gold;
    GoldHook hook;
    PoolSwapTest swapRouter;
    PoolModifyLiquidityTest lpRouter;
    CoreKey key;
    TwapOracle oracle;
    POLManager pol;

    receive() external payable {}

    function setUp() public {
        vm.warp(1_800_000_000);
        manager = new PoolManager(address(this));
        gold = new ScratchGold();
        GoldHook impl = new GoldHook(address(manager), address(gold), factoryEOA);
        vm.etch(HOOK_ADDRESS, address(impl).code);
        hook = GoldHook(payable(HOOK_ADDRESS));
        swapRouter = new PoolSwapTest(IPoolManager(address(manager)));
        lpRouter = new PoolModifyLiquidityTest(IPoolManager(address(manager)));
        key = CoreKey(Currency.wrap(address(0)), Currency.wrap(address(gold)), 12500, 60, IHooks(HOOK_ADDRESS));
        vm.deal(trader, 1000 ether);
        vm.deal(address(this), 10_000 ether);
        vm.prank(factoryEOA);
        manager.initialize(key, SQRT_PRICE_1_1);
        // seed 100 ETH / 100 GOLD full range (L = 100e18), as the launch would
        gold.mint(address(this), 100 ether);
        gold.approve(address(lpRouter), 100 ether);
        lpRouter.modifyLiquidity{value: 100 ether}(key, CoreModify(-887220, 887220, 100e18, bytes32(0)), "");

        oracle = new TwapOracle(address(this), address(0xBEEF), address(new ScratchV3Factory()), address(gold), HOOK_ADDRESS);
        pol = new POLManager(address(manager), address(gold), HOOK_ADDRESS, address(oracle), address(0xEEEE));
    }

    function _swap(bool zeroForOne, int256 amountSpecified) internal {
        uint160 limit = zeroForOne ? 4295128739 + 1 : 1461446703485210103287273052203988822378723970342 - 1;
        uint256 value;
        if (zeroForOne) {
            value = uint256(-amountSpecified);
        } else {
            gold.mint(trader, 1_000_000 ether);
            vm.prank(trader);
            gold.approve(address(swapRouter), type(uint256).max);
        }
        vm.prank(trader);
        swapRouter.swap{value: value}(
            key, CoreSwap(zeroForOne, amountSpecified, limit), PoolSwapTest.TestSettings(false, false), ""
        );
    }

    function _tokensAtTick(int24 tick, uint256 ethAmount) internal pure returns (uint256) {
        uint160 sqrtRatio = TickMath.sqrtPriceAtTick(tick);
        return Math.mulDiv(uint256(sqrtRatio) * sqrtRatio, ethAmount, 1 << 192);
    }

    function _meanTicks() internal view returns (int24 shortTick, int24 longTick) {
        uint32[] memory agos = new uint32[](3);
        agos[0] = 30 minutes;
        agos[1] = 4 hours;
        int56[] memory c = hook.observe(agos);
        shortTick = int24((c[2] - c[0]) / int56(uint56(30 minutes)));
        longTick = int24((c[2] - c[1]) / int56(uint56(4 hours)));
    }

    function testThirtyMinutePumpLowersThePolFloorAndTheBurnBuysAtThePumpedPrice() public {
        // GOLD priceable: a swap past the tax window records the seeded liquidity, 4 hours of ring history
        vm.warp(vm.getBlockTimestamp() + 1 hours);
        _swap(true, -0.001 ether);
        vm.warp(vm.getBlockTimestamp() + 4 hours);
        _swap(false, -0.001 ether);
        uint256 fair = oracle.tokensForEth(address(gold), 0.1 ether);
        assertApproxEqRel(fair, 0.1 ether, 0.01e18, "1:1 pool: 0.1 GOLD per 0.1 ETH");

        // attacker pumps GOLD: 30 ETH into a 100 ETH-deep pool, held for 31 minutes
        _swap(true, -30 ether);
        vm.warp(vm.getBlockTimestamp() + 31 minutes);
        (int24 s, int24 l) = _meanTicks();
        uint256 shortQuote = _tokensAtTick(s, 0.1 ether);
        uint256 longQuote = _tokensAtTick(l, 0.1 ether);
        assertLt(shortQuote, (longQuote * 70) / 100, "the 30-minute window is at the pumped price");
        assertGt(longQuote, (fair * 90) / 100, "the 4-hour window barely moved");

        // v3.2: the POL floor now follows the pumped window (fewer tokens), not the 4-hour one
        uint256 floorNow = (oracle.tokensForEth(address(gold), 0.1 ether) * pol.MIN_OUT_BPS()) / 10_000;
        uint256 floorProtective = (longQuote * pol.MIN_OUT_BPS()) / 10_000;
        emit log_named_uint("floor used by POLManager (GOLD per 0.1 ETH)", floorNow);
        emit log_named_uint("floor at the 4-hour TWAP               ", floorProtective);

        // a permissionless burn of POL money must NOT clear at the pumped price: the pool pays far less than the
        // 4-hour quote minus the 5.25% allowance, which is what MIN_OUT_BPS is documented to guarantee
        pol.depositBurn{value: 1 ether}();
        vm.expectRevert(POLManager.Slippage.selector);
        pol.buyAndBurn(0.1 ether);
    }
}
```

### 3. Medium: Finding-4 fix incomplete for regular (v3) tokens: the payout cap is read from the pool's current liquidity and raw WETH balance, so it is raised inside one transaction (JIT) and satisfiable with out-o

`src/TwapOracle.sol:261`

```
        uint128 liquidity = IUniswapV3PoolOracle(pool).liquidity();
```

The v3.2 fix for audit finding 4 bounds only the genesis (v4) pool by min(current L, liquidityAt(30 min)). _liquidBalances, which feeds valueAndCap/payoutCap and the MIN_LIQUIDITY check for every regular token, still uses pool.liquidity() and weth.balanceOf(pool) at call time. Two mechanisms follow, both in this function. (a) JIT: the cap is read in BagGacha._buildSnapshot during the spin request, so a depositor can in one transaction flash-loan WETH+token, mint a narrow v3 position around the current tick (liquidity() rises by orders of magnitude, the WETH balance by the deposit), call spin() so the snapshot commits uncapped amounts, then burn the position. A 0.7 ETH Bag of a token whose pool holds the 5 ETH minimum is then paid in one draw (0.665 ETH on keep) instead of being split at the 0.25 ETH cap, removing the per-draw bound the cap was introduced for. (b) Parked balances: wethSide = min(balanceOf(pool), virtual) counts WETH held by positions entirely out of range (and plain transfers), which cannot absorb a sale at the current price, so MIN_LIQUIDITY and a 0.25 ETH cap can be met persistently by ~5 WETH parked far above the price plus a one-spacing-wide in-range position of a few hundredths of an ETH. Merged from audit_flow (medium, JIT) and audit_math (low, out-of-range). Fix: mirror the genesis bound. v3 observe() also returns secondsPerLiquidityCumulativeX128; derive the harmonic-mean active liquidity over the 30-minute window and use min(current liquidity, 30-minute mean liquidity) (extend IUniswapV3PoolOracle.observe to decode the second array), and bound the ETH side by the amount the active liquidity actually holds within a fixed band around the price (e.g. up to the next initialized tick or +-5%) rather than the raw WETH balance.

**Reproduction**

test/scratch/V3JitCap.t.sol (mock v3 pool with the same interface the oracle reads): TwapOracle with pool(token, weth) listed via setPool; pool holds 5 WETH / 5 TOK with liquidity 5e18 -> payoutCap(token) = 0.25 ETH. In the same block and transaction mint 95 WETH + 95 TOK to the pool and set liquidity to 100e18 -> payoutCap(token) = 5 ETH. Expected (the finding-4 property the genesis pool now has, testJitPayoutCap): the cap does not move inside one transaction. Actual: forge test --match-path test/scratch/V3JitCap.t.sol fails with '5000000000000000000 != 250000000000000000'. For (b): a listed pool with 5 WETH in an out-of-range position above the price, 5 ETH of TOKEN below it, and an in-range one-spacing position holding 0.02 WETH whose L*2^96/sqrtP >= 5e18 passes validatePool (wethSide = min(5e18, virtual) = 5e18) instead of reverting ThinPool.

### 4. Medium: Genesis depth and payout cap are valued at the spot sqrtPrice: a GOLD pump raises the cap by sqrt(pump) and an in-transaction swap lifts a thin pool over MIN_GENESIS_DEPTH

`src/TwapOracle.sol:228`

```
        (uint160 sqrtPrice,) = goldHook.slot0();
```

ethSide = genesisEthHeld(min(L, liquidityAt(30m)), sqrtPrice) uses the current price from goldHook.slot0(). ETH is currency0, so buying GOLD lowers sqrtP and raises L*2^96/sqrtP by roughly the ETH put in. A price move changes no L, so the v3.2 recorded-liquidity bound does nothing against it. Two consequences. (1) 4-hour pump at minimum depth (the brief's 'TWAP manipulation at minimum depth' case): GOLD is sealable in regular Bags (isPriced(GOLD) is true once the pool is initialized) and is valued at min(30m, 4h) TWAP. With the pool at the 1 ETH minimum, pumping GOLD 10x costs about 2.16 ETH of recoverable ETH held in the pool for 4 hours plus ~0.1 ETH of fees; after 4 hours both windows are ~10x and the cap is 5% of genesisEthHeld(L, sqrtP/3.16) = 0.158 ETH instead of 0.05 ETH. A Bag of 0.03 GOLD sealed 24 h earlier (tier 1) is snapshotted at 0.3 ETH, capped at 0.158 ETH and split; a keep pays the depositor 95% = 0.150 ETH from the reserve for tokens worth 0.016 ETH pre-pump, and the spinner (same attacker) gets the tokens back. _splitBag leaves the remainder listed with its original listedAt, so it is drawable again on the next spin at the same pumped mark; the attacker loops spin -> draw -> keep while the pump lasts, each win paying up to min(cap, 5% of reserve). The Curator's only answer (pause GOLD) needs a 1-day IMD vote. (2) Same-transaction gate bypass: with recorded depth 0.5 ETH (ThinPool), two exact-input ETH->GOLD swaps of 0.3 ETH in one transaction move sqrtP so that genesisEthHeld ~ 1.08 ETH >= MIN_GENESIS_DEPTH, and BagGacha.spin() in the same transaction commits a Genesis quote; the attacker sells back afterwards. Merged from audit_flow (medium) and audit_economics (low). Fix: value the genesis depth and cap at a price the transaction cannot move and the pump must sustain beyond the pricing window, e.g. genesisEthHeld(L, max(sqrtPrice, sqrtPriceAtTick(longTick))) so the ETH-side figure can only go down, and bound L by liquidityAt(LONG_WINDOW) as well; and/or exclude the genesis token from seal() (keep it to the Genesis lane, whose value is bounded by (1-d)P), or raise MIN_GENESIS_DEPTH to a level at which a 4-hour pump costs more than 5% of the reserve. Independent of the concentrated-liquidity finding (different mechanism and fix); fixing one does not fix the other.

**Reproduction**

State: GOLD/ETH pool with recorded L giving genesisEthHeld = 1 ETH at price 1 (MIN_GENESIS_DEPTH), reserve 10 ETH, GenesisVault unfunded (regular lane 100%). Attacker seals Bag{GOLD, 0.03e18} (value 0.03 ETH, tier 1, below 5% of reserve) at T0. At T0+24h buys GOLD with 2.16 ETH (price x10, sqrtP / 3.16), waits 4 h with one tiny swap per hour (staleness). At T0+28h: valueInEth(GOLD, 0.03e18) ~ 0.3 ETH, payoutCap(GOLD) = 500/10000 * genesisEthHeld(L, sqrtP/3.16) ~ 0.158 ETH. spin(): bagPayout caps to 0.158 ETH and records the split; VRF word; draw() -> _splitBag; choose(keep) -> credits[attacker] += 0.150 ETH, reserve -= 0.150 ETH. Expected: the cap does not grow with the manipulator's own pump (0.05 ETH at 1 ETH depth). Actual: 0.158 ETH, repeatable each spin while the pump lasts. Gate case: pool with recorded depth 0.5 ETH, genesisValueAndCap reverts ThinPool; in one transaction swap 0.6 ETH exact-input ETH->GOLD (two 0.3 ETH swaps inside the buy cap), L unchanged, genesisEthHeld ~ 1.08 ETH, genesisValueAndCap/tokensForEth(GOLD) return values and spin() commits a Genesis quote. Expected: still ThinPool. Actual: priced.

### 5. Medium: bindGacha can be locked out forever: GoblinNFT.release() freezes the named targets, so a named set that fails any bindGacha check strands reserveAccrued (and, under path B, the whole GOLD remainder)

`src/GoldHook.sol:289`

```
        if (gacha_.codehash != gachaRuntimeCodeHash()) revert CodeMismatch();
```

bindGacha accepts only the set named through the deployed GoblinNFT's setLaunchTargets and then still requires the pinned runtime code hash and the vault/oracle wiring. The deployed GoblinNFT (src/GoblinNFT.sol:203-204, 221-230, runtime verified against the deployed address by the project's own tests) lets anyone call release() the moment the collection is sold out and the 7-day review has ended, and setLaunchTargets reverts AlreadyReleased afterwards. The README runbook orders bindGacha before release, but release is permissionless, so the order is not enforceable. If the named set fails the hook's own checks, the naming can never be corrected after release and bindGacha reverts forever. The most likely trigger is in the repository itself: the protected foundry.toml has via_ir = true while GACHA_RUNTIME_CODE_HASH is pinned for via_ir = false, bytecode_hash = none; a launch-2 BagGacha built with the repository profile has runtime hash 0x9796d137...dd361b and fails CodeMismatch. Consequences: reserveAccrued (half of every 1% hook fee plus all 90/50/25% launch taxes, held as currency-0 ERC6909 claims in the PoolManager) is never flushable and the hook has no other exit for it (no owner, no sweep, no second bind); under path B the GOLD launch remainder is stuck as well, the GenesisVault is never funded and the Genesis lane never opens. The gacha still receives the NFT escrow through pullMintEscrow, so the failure is silent. Fix (keeps the finding-1 design): (1) add a hook view bindCheck(address) returns (bytes4 reason) evaluating every bindGacha precondition except the review timer, and have the runbook require it to return zero (plus an eth_call of bindGacha after the review) before setLaunchTargets and before anyone can release; (2) pin the launch-2 build profile in the runbook/manifest and verify keccak256(extcodecopy(BagGacha)) == GACHA_RUNTIME_CODE_HASH on chain before naming; (3) optionally let bindGacha accept the named reserve/VRF target after nft.released() when only the code-hash check fails, since the owner naming plus holder review is then the authority the design relies on (document the trade-off).

**Reproduction**

State: NFT owner calls setLaunchTargets(polManager, gachaX, gachaX) where gachaX is a BagGacha whose extcodehash != 0x2db1...c4cd (any BagGacha built with the repository's foundry.toml via_ir = true: forge test --match-test testPinnedGachaRuntimeCodeHash -vv without FOUNDRY_VIA_IR=false prints 0x9796d1370679550f382780faab25b5d150ed263364ab04c5178a2c3741dd361b, verified in this review, versus the pinned 0x2db1143638494d63cd5b4b807bd3dfe333d590ea58e7204ab7fd0c5cf415c4cd), or whose GenesisVault.oracle() != gachaX.oracle(). Collection sells out, 7 days pass, anyone calls GoblinNFT.release(). Then GoldHook.bindGacha(gachaX) reverts CodeMismatch/GachaMismatch; GoblinNFT.setLaunchTargets(...) reverts AlreadyReleased; every later GoldHook.flush() pays holders only and reserveAccrued keeps growing with no function able to move it; IERC20(GOLD).balanceOf(hook) (path B) is immovable. Expected: a recoverable naming mistake, as the 7-day review is documented to provide. Actual: permanent loss of the reserve share and (path B) the genesis supply.

### 6. Low: cancelRequest is a free option once a VRF fulfilment is 24 h late: the spinner can front-run a visible losing word with cancelRequest and let a winning one land

`src/BagGacha.sol:668`

```
        if (block.timestamp < uint256(req.requestedAt) + CANCEL_DELAY) revert CancelNotDue();
```

After CANCEL_DELAY, cancelRequest() (anyone, full refund of P as credit, earmark released) and the wrapper's rawFulfillRandomWords are both valid in the same block. The fulfilment transaction carries the random word in public calldata and draw() is deterministic from it (lane via keccak(word,'lane'), tier and Bag via _select over the public snapshot()/currentRequest()). A spinner who sees a losing word pending cancels first (pending = false, vrfRequestId = 0, credits[spinner] += P), the word is ignored on arrival (id mismatch) and the spinner re-spins; a winning word is left to land. A third party can likewise cancel a visible winning fulfilment to grief the spinner. The VRF fee is the only cost of the option. Reachable only when a Chainlink fulfilment is more than 24 h late, hence low; it is the only ordering race the new cancel path introduces. Merged from three identical specialist reports. Fix: once the request is cancellable no fulfilment may count any more: in rawFulfillRandomWords add '|| block.timestamp >= uint256(req.requestedAt) + CANCEL_DELAY' to the ignore condition (after 24 h the only outcome is cancellation); alternatively make cancel two-step (announce, take effect a block later) or refund P minus a penalty so the option has a cost.

**Reproduction**

State: pending == true, req.fulfilled == false, block.timestamp == req.requestedAt + 24 h. The wrapper's rawFulfillRandomWords(id, [w]) is in the mempool with a w whose lane/tier selects a 0.3P Bag. The spinner submits cancelRequest() with a higher priority fee. Expected: the committed draw resolves with the word the VRF produced. Actual: cancel executes first (pending = false, vrfRequestId = 0, credits[spinner] += P), rawFulfillRandomWords returns early on the id mismatch (line 655), and the spinner spins again. With a jackpot word the spinner instead lets the fulfilment land and calls draw().

### 7. Info: bindGacha does not check the oracle's or POLManager's wiring as the README claims, and the NFT owner can re-run setLaunchTargets after binding

`src/GoldHook.sol:300`

```
        if (IHookGenesisVault(vault).oracle() != IHookGacha(gacha_).oracle()) revert GachaMismatch();
```

README launch 2 says 'vault, gacha and POLManager must share $contract:TwapOracle: bindGacha checks every one of these'. bindGacha only checks vault.oracle == gacha.oracle; it never checks that the oracle's genesisToken()/goldHook() equal this hook's token/address, nor that POLManager's oracle/token/hook match. Separately, the deployed GoblinNFT.setLaunchTargets only requires !released, so after bindGacha(G1) the owner can name G2 and release() sends the escrow to G2 while hook fees keep going to G1. Both depend on the NFT owner and the 7-day holder review (a trust assumption), so this is info. Fix: also require TwapOracle(gacha.oracle()).goldHook() == address(this) && genesisToken() == token and POLManager(gacha.polManager()).oracle()/hook()/token() to match, or correct the README claim; document the post-bind retarget as a trust assumption.

**Reproduction**

The owner names gacha G whose oracle is an arbitrary contract O (O.genesisToken() is not GOLD) with vault.oracle = O. After 7 days bindGacha(G) succeeds (lines 296-300 pass) although the README says the oracle is checked. Or: bind G1, then setLaunchTargets(pol, G2, G2) succeeds (GoblinNFT.sol:203-204 only checks !released) and release() credits G2.

### 8. Info: Manifest remainder path: path B validity cannot be verified from the tree, and path B depends on bindGacha ever succeeding; path A leaves the supply in wallet custody with no on-chain commitment

`README.md:365`

```
  - **Path B — hook custody (no wallet ever holds GOLD), if the manifest allows `remainderTo = $contract:GoldHook`:**
```

Brief item 4. The repository contains no IMD manifest grammar and the README itself conditions path B on 'if the manifest allows remainderTo = $contract:GoldHook', so whether a $contract: reference is accepted as remainder recipient is an IMD-side rule this review cannot confirm; it stays an open item for the requester. What the code guarantees: under path B the only exit for GOLD held by the hook is a successful bindGacha (see the bind lock-out finding), and genesisSupply must be <= the amount the hook forwards or GenesisVault.quote returns 0 forever (balanceOf(vault) < genesisSupply - withdrawn). Under path A the paying wallet (also the deployed GoblinNFT owner) custodies the whole genesis supply with no on-chain commitment to transfer it; the vault quotes nothing until it does. Recommendation: if IMD accepts $contract:GoldHook, prefer path B together with a bind pre-flight check before setLaunchTargets; otherwise record the path-A transfer as a runbook step with the exact genesisSupply and verify balanceOf(vault) == genesisSupply before setLaunchTargets.

**Reproduction**

Not a code defect; operational. State: launch 1 with remainderTo = $contract:GoldHook, then setLaunchTargets never called or called with polTarget != BagGacha.polManager(). Expected per README: GOLD reaches GenesisVault at bind. Actual: bindGacha reverts NotLaunchTarget and IERC20(GOLD).balanceOf(hook) stays at the full remainder with no function able to move it.

---

Judge's submission `95139b8ed4a140fefb281fd4b54b49c6d33d6ccc26efcc0b861508fa224e6e2e`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
