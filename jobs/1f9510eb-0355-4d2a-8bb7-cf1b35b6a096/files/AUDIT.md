# Audit report

> X: https://x.com/imdplace
> v3.3, fixes for audit 930ea061 (commit 8b769ee). Full adversarial review before the token launch. Build and test under the launch profile (FOUNDRY_VIA_IR=false FOUNDRY_BYTECODE_HASH=none) and the protected profile; confirm GACHA_RUNTIME_CODE_HASH 0xbdb13664f85a03997922c0678be6c02e83716a9d7b24e0cd231ae51a3c8af1ad under the launch profile.
>
> 1. Verify every 930ea061 fix: full-range-only beforeAddLiquidity and flags 0x38CC; getHookPermissions matches REQUIRED_FLAGS; polTokensForEth (max) in POLManager vs min in GenesisVault; V3Depth (30-min harmonic L, band, first initialized tick, full-range-equivalent scaling); Genesis depth at max(spot, 4h) price and min(L now, 30m, 4h); seal refuses GOLD; bindCheck and CheckLaunch.s.sol; VRF ignored at or after requestedAt + CANCEL_DELAY; path A funding check.
> 2. Griefing: V3Depth stops at the first initialized tick. Can anyone, with a tiny position near the price, make a listed token unpriceable and so block spins, draws, payouts or cancellations for Bags holding it, or lock funds? Same question for the Genesis lane and full-range-only adds.
> 3. New issues from the changes: rounding in the band math, harmonic counter wrap, both token orders, oracle manipulation at minimum depth (MIN_LIQUIDITY 5 ETH, MIN_GENESIS_DEPTH 1 ETH, PAYOUT_CAP_BPS 500), payout above paid value, stuck funds, hook reentrancy, VRF races.
> 4. bindGacha against the deployed GoblinNFT (launch-1616): any remaining way to lock the reserve.
>
> Report any medium or higher with a concrete fix. NO SOURCE CHANGES.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1545-goblin-gold.git |
| Commit | `170070d52968fc43f73cf54c7a535917a31b78da` |
| Job | `1f9510eb-0355-4d2a-8bb7-cf1b35b6a096` |
| Judged | 2026-10-14 08:51 UTC |
| Findings | 1 high · 2 medium · 4 low |

Four agents audited the code as it is at `170070d`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: Empty-tier odds escalate upward: whoever controls the mature inventory wins every regular draw at 95% of value and drains the reserve

`src/BagGacha.sol:640`

```
            for (uint256 k = t + 1; k < 4 && !moved; ++k) {
                if (weights[k] > 0) {
                    eff[k] += odds[t];
                    moved = true;
                }
            }
```

_buildSnapshot moves the odds of every empty tier to the nearest lower non-empty tier, else to the nearest HIGHER one (README line 344 documents the rule but not its consequence). Inventory is permissionless and a kept draw pays the depositor 95% of the snapshot value from the reserve (finalize defaults to keep). Whoever is the only depositor with mature Bags therefore chooses the whole tier distribution: with one large-tier Bag (value in [2P,6P)) the small and medium tiers are empty, their 9300 bps move UP, req.odds becomes [0,0,10000,0] and every regular-lane draw pays that Bag. Per regular spin the reserve takes 88% of P = 0.0088 ETH and pays 0.95 * V with V up to min(5% of reserve, 70P, payout cap). The attacker spins against their own inventory: pays P + VRF fee (about 0.0105 ETH), receives 0.95 * 0.059 = 0.056 ETH as credit, pulls the tokens back with claimBag and re-seals them. Filling the 32 active slots (TooManyActive for everyone else) keeps the population controlled; the Genesis lane only reduces the regular share to 40% when available and is off for the first four hours and after any hour without a GOLD swap. At a 14 ETH reserve (jackpot on) a 0.7 ETH Bag pays 0.665 ETH per regular draw. Reproduced with the attached test: odds[2] == 10000, reserve 4.0 -> 3.95275 ETH and attacker credit 0.05605 ETH after one 0.0105 ETH spin. Fix (keeps the tiers and the keep/buyback economics): never move odds upward. When a tier is empty and no lower tier is non-empty (equivalently weights[0] == 0), treat the regular lane as empty for that request (regularEmpty = true: Genesis-only spin, or NothingToDraw when Genesis is unavailable) instead of concentrating the small/medium odds on a large or jackpot Bag; optionally also cap a tier's effective odds at odds[t] plus the odds of HIGHER empty tiers only.

**Reproduction**

State: BagGacha with reserve 4 ETH (fundReserve), Genesis lane unavailable (vault quote 0 or GOLD stale), holder window over. Attacker seals one Bag of a listed token valued 0.059 ETH (large tier, under 5% of reserve), waits MATURATION (24 h), calls spin() paying spinPrice().total. Expected: the large tier keeps at most its 650 bps plus the jackpot tier's 50 bps; the empty small and medium tiers' 9300 bps do not become a certain win of the only Bag. Actual: currentRequest().odds == [0,0,10000,0]; any VRF word selects the attacker's Bag; after draw() and finalize() credits[attacker] == 0.05605 ETH, reserve 4.0 -> 3.95275 ETH, and claimBag returns the 59 tokens for re-sealing. test/scratch/OddsEscalation.t.sol (attached as proof) fails on this code with '10000 > 700'. Run: FOUNDRY_VIA_IR=false FOUNDRY_BYTECODE_HASH=none forge test --match-path test/scratch/OddsEscalation.t.sol -vv

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {BagGacha} from "src/BagGacha.sol";

contract DrainToken is ERC20 {
    constructor() ERC20("T", "T") {
        _mint(msg.sender, 1_000_000 ether);
    }
}

/// @dev Prices every token at 1 token = 1e-3 ETH, no payout cap.
contract DrainOracle {
    function isPriced(address) external pure returns (bool) {
        return true;
    }

    function valueInEth(address, uint256 a) external pure returns (uint256) {
        return a / 1000;
    }

    function valueAndCap(address, uint256 a) external pure returns (uint256, uint256) {
        return (a / 1000, type(uint256).max);
    }

    function genesisValueAndCap(uint256 a) external pure returns (uint256, uint256) {
        return (a / 1000, type(uint256).max);
    }
}

/// @dev Genesis lane unavailable (vault unfunded or GOLD stale): quote() == 0, so every spin is a regular draw.
contract DrainVault {
    address public immutable token;

    constructor(address t) {
        token = t;
    }

    function quote(bool) external pure returns (uint256) {
        return 0;
    }

    function commit(bool) external pure returns (uint256) {
        return 0;
    }

    function uncommit(uint256) external {}
    function deliver(address, uint256) external {}
    function setShares(address, uint256) external {}
}

contract DrainVRF {
    uint256 public last;

    function calculateRequestPriceNative(uint32, uint32) external pure returns (uint256) {
        return 0.0005 ether;
    }

    function requestRandomWordsInNative(uint32, uint16, uint32, bytes calldata) external payable returns (uint256) {
        last += 1;
        return last;
    }

    function fulfill(address consumer, uint256 id, uint256 word) external {
        uint256[] memory w = new uint256[](1);
        w[0] = word;
        BagGacha(payable(consumer)).rawFulfillRandomWords(id, w);
    }
}

contract Sink {
    function depositPOL() external payable {}
    function depositBurn() external payable {}
}

/// @notice A depositor who controls the mature inventory gets the odds of every empty tier moved UP to its own
///         bag: one large-tier Bag receives 100% of the regular-lane odds, so every regular draw pays it 95% of its
///         value from the reserve for a 0.01 ETH spin.
contract OddsEscalationDrainTest is Test {
    BagGacha gacha;
    DrainToken token;
    DrainVRF vrf;
    address attacker = address(0xA11CE);

    function setUp() public {
        vm.warp(1_000_000);
        token = new DrainToken();
        vrf = new DrainVRF();
        DrainVault vault = new DrainVault(address(0xB0B)); // GOLD is some other address
        gacha = new BagGacha(
            address(new DrainOracle()),
            address(vault),
            address(0xCAFE), // nft: never called on this path
            address(vrf),
            address(new Sink()),
            address(0x7EA0),
            block.timestamp,
            address(this)
        );
        vm.deal(address(this), 100 ether);
        gacha.fundReserve{value: 4 ether}();
        token.transfer(attacker, 1000 ether);
        vm.deal(attacker, 10 ether);
        vm.warp(block.timestamp + gacha.HOLDER_WINDOW());
    }

    function testEmptyTierOddsMustNotEscalateToTheOnlyBag() public {
        // one large-tier Bag: 59 tokens = 0.059 ETH (large tier is [2P, 6P)), under 5% of the 4 ETH reserve
        address[] memory toks = new address[](1);
        toks[0] = address(token);
        uint256[] memory amts = new uint256[](1);
        amts[0] = 59 ether;
        vm.startPrank(attacker);
        token.approve(address(gacha), type(uint256).max);
        gacha.seal(toks, amts);
        vm.warp(block.timestamp + gacha.MATURATION());

        uint256 reserveBefore = gacha.reserve();
        (uint256 price,) = gacha.spinPrice();
        uint256 id = gacha.spin{value: price}();
        vm.stopPrank();

        (,,,, uint256[4] memory odds,) = gacha.currentRequest();
        emit log_named_uint("effective odds of the only (large) tier", odds[2]);

        // Drive the draw to the end to show the flow: every word selects the attacker's Bag.
        vrf.fulfill(address(gacha), id, uint256(keccak256("any word")));
        uint256 alloc = gacha.draw();
        vm.warp(block.timestamp + gacha.CHOICE_WINDOW());
        gacha.finalize(alloc);
        emit log_named_uint("reserve before", reserveBefore);
        emit log_named_uint("reserve after one spin", gacha.reserve());
        emit log_named_uint("attacker credit after paying 0.0105 ETH", gacha.credits(attacker));

        // The large tier's base odds are 650 bps; it may absorb the jackpot tier's 50 bps moving DOWN, but the
        // small and medium tiers' 9300 bps must never move UP into it.
        assertLe(odds[2], 650 + 50, "empty lower tiers' odds escalated to the only bag");
    }
}
```

### 2. Medium: V3Depth stops at the first initialized tick: a 1-wei position within one spacing of the price, or a swap parked exactly on an initialized tick, makes a listed token unpriceable (ThinPool) at gas cost

`src/v3/V3Depth.sol:74`

```
            if (bitmap != 0) return price;
```

_edge returns the sqrt price of the first initialized tick in each direction and balances() counts only the liquidity released between the spot price and that tick, scaled by the fixed band factor upper/(upper - sqrtP) = 21 and capped at the virtual reserve. Anyone can initialize a tick next to the price by minting a position with liquidityDelta 1 (1 wei of each token, about 300k gas). A boundary within one tick spacing (60 ticks = 0.3% of sqrt price) caps the measured side at about 0.3% * 21 = 6.3% of the virtual reserve, so every pool with under about 79 ETH of virtual reserve per side (at spacing 60; under 160 ETH when the price sits mid-bucket, at spacing 10 almost every pool) fails MIN_LIQUIDITY and TwapOracle reverts ThinPool for that token. Worse, the downward mask at line 61 includes the current compressed tick and the upward search returns a price equal to sqrtPrice: after a zeroForOne swap with sqrtPriceLimitX96 == sqrtPriceAtTick(T) for an initialized T, v3 leaves slot0 = (sqrtPriceAtTick(T), T-1) and the measured token0 side is exactly 0 (symmetrically (sqrtPriceAtTick(T), T) after oneForZero zeroes the token1 side). That state needs no position at all and can be placed in front of a specific request. Consequences on this tree: seal() of the token reverts BadBag/ValueOutOfRange; _buildSnapshot skips every Bag holding it (try/catch) so those Bags are not drawable, which also tilts draws toward the attacker's own Bags; withdraw() waives the 0.5% exit fee because bagValue reverts; a Curator pool proposal fails at execute() (setPool -> validatePool -> ThinPool) for its whole validity; 32 such Bags held by one actor squat every active slot (TooManyActive for everyone, regularEmpty for every request, NothingToDraw when Genesis is unavailable). draw(), choose/finalize, claimBag and cancelRequest never read the oracle, so no ETH is locked and depositors exit after maturation; hence Medium. README lines 137-139 document the limitation as a curation matter, but the state is created after listing, by anyone, at any time. Fix (keeps the no-raw-balance design and the JIT bound): inside the fixed band walk a bounded number of initialized ticks (e.g. 8 per direction) reading IUniswapV3Pool.ticks(t).liquidityNet, carry L' = L +/- liquidityNet across each crossing and use min(L, L') for the next segment, so a dust tick releases the same amounts while liquidity that only appears after a crossing is never credited; and start each search strictly beyond a tick whose price equals sqrtPrice (treat it as already crossed, as the v3 swap loop does).

**Reproduction**

Merged from four specialist reports; all reproduced. V3Depth.balances(pool, sqrtPrice = 2^96 (tick 0), tick 0, L = 100e18) on a spacing-60 pool with no initialized ticks inside the band returns about 100 ETH on both sides. (a) Initialize tick 60 (a 1-wei position [60,120]): expected token0 side still near 100 ETH; actual amount0 = 6.290245407412639953 ETH, so any pool under about 79 ETH per side reports under MIN_LIQUIDITY 5 ETH and TwapOracle._liquidBalances reverts ThinPool. (b) Initialize tick 0 with the price at 2^96 (MockV3Pool from test/mocks/CuratorMocks.sol, liquidity = history = 1000e18, setInitializedTick(0, true)): balances returns (999999999999999999987, 0) and oracle.payoutCap(token) reverts ThinPool(pool) for a 1000 ETH pool. (c) slot0 = (sqrtPriceAtTick(60), 59), the exact state v3 leaves after a zeroForOne swap limited at tick 60: amount0 == 0. test/scratch/DustTick.t.sol (attached) fails on this code with those values. Run: FOUNDRY_VIA_IR=false FOUNDRY_BYTECODE_HASH=none forge test --match-path test/scratch/DustTick.t.sol -vv

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {V3Depth} from "src/v3/V3Depth.sol";
import {TickMath} from "src/TickMath.sol";

/// @dev A v3 pool's tick bitmap and tick table, enough for V3Depth (and for a fix that walks liquidityNet).
contract DustPool {
    int24 public tickSpacing = 60;
    mapping(int16 => uint256) public tickBitmap;
    mapping(int24 => int128) public liquidityNetOf;

    function initTick(int24 tick, int128 net) external {
        int24 compressed = tick / tickSpacing;
        tickBitmap[int16(compressed >> 8)] |= 1 << uint8(uint24(compressed));
        liquidityNetOf[tick] = net;
    }

    function ticks(int24 tick)
        external
        view
        returns (uint128 liquidityGross, int128 liquidityNet, uint256, uint256, int56, uint160, uint32, bool)
    {
        int128 net = liquidityNetOf[tick];
        return (uint128(net < 0 ? -net : net), net, 0, 0, 0, 0, 0, net != 0);
    }
}

contract DepthHarness {
    function balances(address pool, uint160 price, int24 tick, uint128 l) external view returns (uint256, uint256) {
        return V3Depth.balances(pool, price, tick, l);
    }
}

/// @notice A 1-wei-liquidity position whose tick is within one spacing of the price caps the measured depth at a
///         sliver of the real depth; a swap that stops exactly at an initialized tick measures zero.
contract DustTickDepthTest is Test {
    DustPool pool;
    DepthHarness depth;
    uint160 constant P = 1 << 96; // price 1, tick 0
    uint128 constant L = 100 ether; // 100 ETH virtual reserve on each side

    function setUp() public {
        pool = new DustPool();
        depth = new DepthHarness();
    }

    function testOneDustTickWithinOneSpacingMakesA100EthPoolThin() public {
        (uint256 a0, uint256 a1) = depth.balances(address(pool), P, 0, L);
        assertApproxEqRel(a0, 100 ether, 1e15);
        assertApproxEqRel(a1, 100 ether, 1e15);

        // Attacker: position [60, 120] with 1 wei of liquidity (dust of both tokens, left forever).
        pool.initTick(60, 1);
        pool.initTick(120, -1);
        (a0, a1) = depth.balances(address(pool), P, 0, L);
        emit log_named_decimal_uint("token0 depth seen with one dust tick at +60", a0, 18);
        // A 1-wei position changes the pool's real depth by nothing; the measured ETH side must not drop below
        // half of the 100 ETH the active liquidity really backs across the band.
        assertGe(a0, 50 ether, "one dust tick made the pool unpriceable");
    }

    function testSwapParkedExactlyAtAnInitializedTickMeasuresZero() public {
        pool.initTick(60, 1);
        pool.initTick(120, -1);
        // A zeroForOne swap with sqrtPriceLimitX96 == sqrtPriceAtTick(60) ends with slot0 = (price(60), tick 59).
        uint160 pinned = TickMath.sqrtPriceAtTick(60);
        (uint256 a0,) = depth.balances(address(pool), pinned, 59, L);
        emit log_named_uint("token0 depth seen when parked at tick 60", a0);
        assertGt(a0, 0, "parked at the tick: zero depth, every quote reverts ThinPool");
    }
}
```

### 3. Medium: bindCheck and CheckLaunch verify neither POLManager.mintEscrow nor POLManager.poolManager: a mis-wired POLManager passes preflight and binding, then release() freezes the 50% POL escrow for good

`src/GoldHook.sol:370`

```
                || _readAddress(pol, IHookPOL.oracle.selector) != oracle_
                || _readAddress(pol, IHookPOL.hook.selector) != address(this)
                || _readAddress(pol, IHookPOL.token.selector) != token
```

The 930ea061 repair of findings 5 and 7 made bindCheck the single wiring gate (every wire except the review timer) and CheckLaunch.s.sol the operator preflight. bindCheck checks pol.oracle, pol.hook and pol.token but not pol.mintEscrow (must equal NFT) or pol.poolManager (must equal the hook's poolManager), both immutables of POLManager that the hook can verify. CheckLaunch checks only the runtime hash, flags, vault funding, bindCheck and a simulated bindGacha. GoblinNFT.claimRelease pays polOwed only to msg.sender == polTarget, and POLManager reaches it only through pullMintEscrow, which reads its own mintEscrow. So a POLManager deployed with the wrong mintEscrow passes CheckLaunch, is named polTarget, passes bindCheck and bindGacha; once release() runs (permissionless after the 7-day review) polOwed = liveSupply * PRICE / 2 (5 ETH at sellout) is unclaimable by anyone, forever: nothing can retarget after release and POLManager has no rescue. A wrong poolManager is caught by no check either and makes every buyAndBurn/addLiquidity revert, stranding all POL and burn budget ETH (40%+2%/4% of every spin). This is the same lock-out class the shared bindCheck was meant to close. Fix: declare mintEscrow() and poolManager() on IHookPOL and add to the GachaMismatch clause `|| _readAddress(pol, IHookPOL.mintEscrow.selector) != NFT || _readAddress(pol, IHookPOL.poolManager.selector) != address(poolManager)`; mirror both in CheckLaunch.s.sol and extend testBindCheckChecksEveryWireWithoutWaitingForReview with the two selectors.

**Reproduction**

test/scratch/MintEscrowWire.t.sol (Audit930Fixture): deploy POLManager(manager, GOLD, hook, oracle, mintEscrow = address(vault), i.e. any contract other than the NFT), a GenesisVault and a BagGacha pointing at that POLManager, fund the vault exactly. Expected: CheckLaunch.run reverts BindNotReady and bindCheck returns GachaMismatch. Actual: CheckLaunch.run(hook, gacha2) passes; nft.setLaunchTargets(badPol, gacha2, gacha2); bindCheck(gacha2) == bytes4(0); after 500 holders mint 20 each and 7 days pass, bindGacha(gacha2) succeeds and nft.release() sets polOwed = 5 ETH; badPol.pullMintEscrow() reverts, nft.claimRelease() from any other caller reverts NothingOwed, gacha2.pullMintEscrow() works for its own shares and polOwed stays 5 ETH. The test passes on this code (it asserts the defect). Run: FOUNDRY_VIA_IR=false FOUNDRY_BYTECODE_HASH=none forge test --match-path test/scratch/MintEscrowWire.t.sol -vv

### 4. Low: Full-range-equivalent scaling counts a band-only (about +/-10%) v3 position at 20x its capital: 0.25 ETH per side passes the documented 5 ETH per side policy and the cap equals all the WETH in the ban

`src/v3/V3Depth.sol:36`

```
                    Math.min(Math.mulDiv(liquidity, Q96, sqrtPrice), Math.mulDiv(released, upper, upper - sqrtPrice));
```

The amounts released inside the +/-5% sqrt band are multiplied by upper/(upper - sqrtPrice) = 21, i.e. to the virtual reserve L*2^96/sqrtP of a full-range position with the same L. For a position that spans exactly the band this is 20x the tokens it holds. TwapOracle compares the scaled figure with MIN_LIQUIDITY and takes PAYOUT_CAP_BPS of it, while README lines 40 and 128 and the Curator policy string (src/Curator.sol line 302: at least 5 ETH value per side) describe a capital figure. The slippage semantics are consistent (a 5% payout against liquidity L moves the price about 10% whether L is full-range or band-only, and the band covers that move), so this is a policy mismatch plus a 20x reduction of the capital an LP who controls a token needs to make its pool pass the on-chain gate (about 0.3 ETH instead of 5 ETH, recoverable in both cases); the Curator panel remains the gate against listing such a pool, and README lines 139-141 state the design. Fix: either state in the policy string and README that the gate is a liquidity-equivalent (L) bound, not capital, so panel reviewers measure the quantity the contract does, or additionally require the unscaled WETH released inside the band to be at least a fraction of MIN_LIQUIDITY (e.g. 1 ETH) and bound the payout cap by a multiple of that released amount.

**Reproduction**

test/scratch/BandScale.t.sol: spacing-60 pool with initialized ticks -1020 and 1020 only, spot tick 0 (sqrtPrice 2^96), L = 5e18. V3Depth.balances returns amount0 = 4.999999999999999995e18 and amount1 = 4.999999999999999994e18 (L = 5.0001e18 clears MIN_LIQUIDITY); the position really holds token0 = 0.248594532077046411e18 and WETH = 0.248594532077046411e18; payoutCap = 0.249999999999999999e18, more than the 0.2486 ETH of WETH the band contains. Expected under the policy text: rejected as under 5 ETH value per side. Actual: passes validatePool/_checkPool.

### 5. Low: Genesis lane liveness depends on swap cadence: dark until the first post-seed swap plus 4 hours, and again after any hour without a GOLD swap

`src/GoldHook.sol:241`

```
        observations[0] = Observation(uint32(block.timestamp), 0, true, 0); // no liquidity exists yet
```

Observations are written only in beforeSwap. afterInitialize stores one entry with liquidity 0 and the factory seed (same transaction) is not recorded until the first swap in a later block (T1). TwapOracle._checkGenesisPool takes min(current L, liquidityAt(30m), liquidityAt(4h)); for targets before T0 liquidityAt reverts OldObservation and for T0 <= target < T1 it returns 0, so the oracle reverts ThinPool until T1 + 4h regardless of how long ago the pool was seeded. Separately, _checkGenesisPool reverts StalePool after 3600 s without a swap because staleness measures time since the last trade although observe() extrapolates correctly. In both states BagGacha._commitGenesis returns (0,0): freeSpin reverts NothingToDraw, paid spins are regular-lane only (NothingToDraw with no mature Bags, and 100% regular odds, which amplifies the odds-escalation finding), and POLManager.buyAndBurn/addLiquidity revert through polTokensForEth. Anyone can refresh the ring with a dust swap, so this is liveness, not a lock, and the 4-hour seasoning is stated in README lines 142-143; it is reported because startTime relative to the first swap is a launch input and day-one free spins fail if startTime is within 4 h of the first swap. Fix options: write an observation in an afterAddLiquidity callback (flag 1<<10) so the seed is recorded in the factory transaction, or document that startTime must be at least 4 h after the first swap and that a keeper should trade at least hourly.

**Reproduction**

test/scratch/GenesisDark.t.sol (Audit930Fixture, 100 ETH seed at T0): first swap at T1 = T0 + 1h, dust swaps every 59 min keep the ring fresh. At T1 + 4h - 1s: hook.liquidityAt(4 hours) == 0, oracle.genesisValueAndCap(1e18) and oracle.polTokensForEth(1e17) revert ThinPool(hook), gacha.spin{value: spinPrice().total}() reverts NothingToDraw. At T1 + 4h the same calls succeed. Expected (operationally): the lane opens 4 h after seeding. Actual: 4 h after the first swap. Staleness: with a seasoned ring and no swap for 3601 s, valueInEth(GOLD), polTokensForEth and genesisValueAndCap revert StalePool(hook) (the existing TwapOracle staleness tests cover that mechanism).

### 6. Low: CheckLaunch requires exact vault funding, so 1 wei of GOLD sent to the vault by anyone makes the preflight revert forever

`script/CheckLaunch.s.sol:25`

```
        if (IERC20(hook.token()).balanceOf(address(vault)) != vault.genesisSupply()) revert WrongFunding();
```

The runbook (path A) requires the preflight to pass before the NFT owner names targets. The check demands balanceOf(vault) == genesisSupply, but any holder can transfer GOLD to the vault and nothing can remove it (the vault only pays claims and dividends). GenesisVault.quote needs only balanceOf >= genesisSupply - withdrawn, so a surplus is harmless on chain while the script refuses on every later run and operators must edit it under time pressure. Fix: revert only on balanceOf < genesisSupply and log any surplus.

**Reproduction**

Existing test test/audit930ea061/GenesisAndBinding.t.sol::testPathAFundingAndPreflightBeforeOwnerNamesTargets shows it: vault funded with exactly genesisSupply, then gold.mint(address(vault), 1) makes CheckLaunch.run revert WrongFunding; the test has to prank the vault to send the wei back before the script passes, which nobody can do on chain. Expected: a vault holding at least what it owes passes. Actual: WrongFunding on every run.

### 7. Low: CheckLaunch does not exercise the gacha VRF wrapper or its other constructor words: a wrong vrf address passes preflight, then every spin reverts and the reserve is stranded after release

`script/CheckLaunch.s.sol:30`

```
        bytes4 reason = hook.bindCheck(gachaAddress);
        if (reason != bytes4(0)) revert BindNotReady(reason);
```

The pinned runtime hash fixes BagGacha code but not the storage its constructor sets: vrf, team, curator, startTime. bindCheck cannot know the right wrapper and CheckLaunch never calls gacha.spinPrice() or vrf.calculateRequestPriceNative. If vrf is the VRF coordinator, a wrapper of another chain or a stale wrapper, _paidSpin and freeSpin revert on the price call forever; the gacha's 40% escrow share (up to 4 ETH), every hook reserve flush (including the 90/50/25% early buy tax) and donations become unspendable, with no admin, no rescue and no rebinding (AlreadyBound). Fix: in CheckLaunch after the funding check add `(uint256 total, uint256 fee) = gacha.spinPrice(); if (fee == 0 || total <= fee) revert WrongWiring();`, assert gacha.curator() == vault.curator() and gacha.startTime() within the intended window, and compare address(gacha.vrf()) with the chain-table wrapper passed as a script argument.

**Reproduction**

By inspection of script/CheckLaunch.s.sol lines 19-35 and src/BagGacha.sol lines 377-380, 496 and 504: deploy BagGacha with vrfWrapper_ = any contract without calculateRequestPriceNative (e.g. the VRF coordinator). CheckLaunch.run passes every check (the hash is unchanged; bindCheck reads only oracle, genesis, nft and polManager) and bindGacha succeeds; afterwards gacha.spin{value: x}() reverts inside vrf.calculateRequestPriceNative for every caller and the reserve plus flushed hook share can never be paid out. Expected: preflight fails.

---

Judge's submission `788bee624dc7ad417c257c2d1856125f4a903afc77018d40e03c05a52f7ce1c3`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
