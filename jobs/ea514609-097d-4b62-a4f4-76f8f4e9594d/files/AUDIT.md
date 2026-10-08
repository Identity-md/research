# Audit report

> Courier is a game on Robinhood Chain (4663). Players buy post offices with ETH, put Courier NFTs on duty and earn $STAMP, which trades in one Uniswap v4 pool against IMD. Read AUDIT.md first: it describes the system, the guarantees, every admin power and the known, accepted limits.
>
> Contracts (contracts/src):
> - StampHook: pool owner and v4 hook. openPool (owner, once) locks a 2.1M $STAMP single-sided launch allocation that can never be removed; every swap in the pool pays 4% of its IMD side to the protocol through return deltas, held as ERC-6909 claims until collectProtocolFees.
> - StampRouter, StampEthRouter: buy/sell with IMD (permit sells), or with ETH through the hookless IMD/ETH pool.
> - StampToken: $STAMP, 21M cap, only PostOffice mints, ownership renounced at deploy.
> - PostOffice: offices, couriers on duty, reward-per-power emissions with halvings, levels, $STAMP spending (75% burned), referrals.
> - CourierNFT: 3,333 NFTs minted for ETH, commit-reveal traits, couriers locked while on duty.
> - Deploy: contracts/script/DeployMainnet.s.sol, DeployLib.sol.
> Out of scope: the view-only art contracts (CourierRenderer, CourierSVG, CourierTraits), DeployFork.s.sol (dev only) and web/.
>
> Look hardest at:
> 1. The fee: exactly 4% on every swap in the pool, through any router, direction and exact-in/out mode; never skipped, never overcharged; partial fills; the hook's IMD claims always equal pendingProtocolFees.
> 2. Locked liquidity: nobody can remove it, add liquidity, open another pool on the hook, or block openPool.
> 3. Supply: $STAMP can never exceed 21M; nothing can change balances, the minter or transfers after deploy.
> 4. PostOffice accounting: never pays more than was emitted, or for time a courier wasn't on duty, including across halvings.
> 5. Couriers: one on duty can't be transferred; traits can't be learned or influenced before the mint ends.
> 6. Routers move only the caller's tokens and enforce deadlines and minimum outputs; no admin power reaches user funds (scanner flags: honeypot, hidden owner, owner can change balance).
>
> Tests: cd contracts; git submodule update --init --recursive; forge test (43 tests). Fork test: forge test --match-contract StampHookForkTest --fork-url https://robinhood.drpc.org

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/courierworld.git |
| Commit | `0a2ce30357882180a87365514d7e9e6800700537` |
| Job | `ea514609-097d-4b62-a4f4-76f8f4e9594d` |
| Judged | 2026-10-08 14:31 UTC |
| Findings | 1 medium · 4 low · 7 info |

Four agents audited the code as it is at `0a2ce30`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: PostOffice: owner can change $STAMP costs between a player's quote and execution; levelUp/upgradeOffice pull the live cost up to the player's allowance

`contracts/src/PostOffice.sol:221`

```
        _spend(cost);
```

levelUp pulls levelCost(lvl) and upgradeOffice pulls tiers[next].upgradeCost from msg.sender at execution time, with no caller-supplied maximum. The owner can rewrite both bases at any moment with setLevelCostBase (line 316) and setTierUpgradeCost (line 306): no cap, no delay. The web client (web/chain.js ensureAllowance) approves the office for type(uint256).max, so whatever the cost is when the call lands is taken: burnBps burned, the rest to the treasury the owner also sets. AUDIT.md guarantee 8 and section 5 state that no admin power can move a player's $STAMP and that owner-set costs 'never' reach balances; this path does. The ETH-paid actions already have the right guard (openOffice and CourierNFT.mint require msg.value == price * qty, so a price change makes the player's call revert); the $STAMP-paid actions lack the equivalent. The owner is a single EOA until the planned multisig move, and a compromised owner key could combine setTreasury + setBurnBps(0) + setLevelCostBase(huge) to take every in-flight levelUp caller's whole approved balance. Reported by audit_economics (medium) and audit_permissions (low); merged. Fix, keeping the owner powers: add a maxCost argument to levelUp and upgradeOffice and revert if the live cost exceeds it (mirroring WrongPayment), or apply cost changes only after a delay.

**Reproduction**

Reproduced with the attached test (forge test --match-path test/scratch/Proof_cf80b5135a67.t.sol). State: tiers as in DeployMainnet; alice has an office, one revealed courier, ~10,000 $STAMP claimed and has approved PostOffice for type(uint256).max. office.levelCost(0) == 25e18. Owner calls setLevelCostBase(alice's balance). Alice calls levelUp(1). Expected: alice pays 25 $STAMP or the call reverts. Actual: _spend burns 75% and sends 25% of alice's whole balance to the treasury; her balance is 0. Test fails: 'player paid more than the cost they signed for: 9999999999999999999999 > 25000000000000000000'. Same with setTierUpgradeCost(1, balance) then upgradeOffice() (quoted 100e18).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {StampToken} from "src/StampToken.sol";
import {CourierNFT} from "src/CourierNFT.sol";
import {PostOffice} from "src/PostOffice.sol";

/// PostOffice owner can change STAMP-denominated costs at any time, and `levelUp` / `upgradeOffice`
/// carry no caller-side bound: a call a player sent for "25 STAMP" pulls whatever the cost is when it
/// executes, up to the player's allowance (the web client approves type(uint256).max).
///
/// Fails on the current code. Passes with either fix: a `maxCost` argument on the two spend functions
/// (the test then calls the bounded variant with the quoted cost and expects it to revert or charge at
/// most that), or cost changes that only take effect after a delay.
contract OwnerCostPullTest is Test {
    StampToken stamp;
    CourierNFT nft;
    PostOffice office;

    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address alice = makeAddr("alice");

    uint256 constant SECRET = 0xC0FFEE;

    function setUp() public {
        vm.roll(100);
        vm.warp(1_800_000_000);
        vm.startPrank(owner);
        stamp = new StampToken(owner, address(0), 0);
        nft = new CourierNFT(owner, treasury, 0.003 ether, keccak256(abi.encode(SECRET)));
        office = new PostOffice(stamp, nft, 1000, 2.5e18, 0.005 ether, treasury, owner);
        stamp.setMinter(address(office));
        nft.setGame(address(office));
        office.addTier(2, 3, 0);
        office.addTier(4, 7, 100e18);
        nft.setSaleOpen(true);
        vm.stopPrank();
        vm.deal(alice, 10 ether);

        vm.prank(alice);
        nft.mint{value: 0.003 ether}(1);
        vm.startPrank(owner);
        nft.setSaleOpen(false);
        nft.reveal(SECRET);
        vm.stopPrank();

        vm.prank(alice);
        office.openOffice{value: 0.005 ether}(address(0));
        // alice earns ~10,000 STAMP and, like the web client, approves the office for max.
        vm.warp(1_800_000_000 + 4000);
        vm.startPrank(alice);
        office.claim();
        stamp.approve(address(office), type(uint256).max);
        vm.stopPrank();
    }

    function _callBounded(bytes memory unbounded, bytes memory bounded) internal {
        vm.startPrank(alice);
        (bool ok,) = address(office).call(unbounded);
        if (!ok) {
            // Signature changed by the fix: the bounded call must revert or charge at most the quoted cost.
            (ok,) = address(office).call(bounded);
        }
        vm.stopPrank();
    }

    /// Expected: a level-up costs levelCost(0) = 25 STAMP, the amount shown to alice when she sends it.
    /// Actual: the owner raises levelCostBase before alice's call executes and the same `levelUp(1)`
    /// pulls alice's whole balance (75% burned, 25% to the treasury).
    function test_OwnerCanDrainPlayerStampThroughLevelUp() public {
        uint256 balanceBefore = stamp.balanceOf(alice);
        uint256 quoted = office.levelCost(0);
        assertEq(quoted, 25e18, "quoted cost");

        vm.prank(owner);
        office.setLevelCostBase(balanceBefore);

        _callBounded(
            abi.encodeWithSignature("levelUp(uint256)", 1),
            abi.encodeWithSignature("levelUp(uint256,uint256)", 1, quoted)
        );

        uint256 paid = balanceBefore - stamp.balanceOf(alice);
        assertLe(paid, quoted, "player paid more than the cost they signed for");
    }

    /// Same with the office tier upgrade cost.
    function test_OwnerCanDrainPlayerStampThroughUpgradeOffice() public {
        uint256 balanceBefore = stamp.balanceOf(alice);
        (,, uint256 quoted) = office.tiers(1);
        assertEq(quoted, 100e18, "quoted cost");

        vm.prank(owner);
        office.setTierUpgradeCost(1, balanceBefore);

        _callBounded(
            abi.encodeWithSignature("upgradeOffice()"),
            abi.encodeWithSignature("upgradeOffice(uint256)", quoted)
        );

        uint256 paid = balanceBefore - stamp.balanceOf(alice);
        assertLe(paid, quoted, "player paid more than the cost they signed for");
    }
}
```

### 2. Low: PostOffice: total claimed can exceed totalEmitted by dust because every power change re-floors rewardDebt in the office's favour

`contracts/src/PostOffice.sol:381`

```
            o.pending += o.power * accRewardPerPower / PRECISION - o.rewardDebt;
```

AUDIT.md guarantee 5 says total claimed <= totalEmitted and that no rounding lets a claim exceed what was earned. _checkpoint credits floor(power * acc / 1e18) - rewardDebt and _addPower/_removePower (lines 358, 365) then reset rewardDebt = floor(power_new * acc / 1e18). The fraction discarded by that floor is recovered by the office at its next checkpoint, so an office gains up to 1 wei above its exact share per power change (assign, unassign, levelUp on duty), while constant-power offices only lose fractions. After a few changes the sum of claims lands above totalEmitted. The 21M cap still holds (claim clamps to MAX_SUPPLY - totalMinted and StampToken.mint reverts past it), so the impact is a few wei of over-emission and a broken stated invariant; the repo's testFuzz_ClaimsNeverExceedEmission does not vary power so it never hits it. Fix: keep the debt in undivided units (rewardDebt = power * acc; credit (power * acc - rewardDebt) / PRECISION) so each segment is floored once, or track totalClaimed and clamp claims to totalEmitted - totalClaimed.

**Reproduction**

Reproduced with the attached test (forge test --match-path test/scratch/Proof_7ce0d47618c0.t.sol). blockTimeMs 1000, initialReward 2.25e18, one tier. t0: alice opens an office (60), bob opens one and assigns an On Foot courier (160); totalPower 220. +2 blocks: bob unassigns foot, assigns a Skateboard (220); totalPower 280. +2 blocks: bob swaps back to foot; totalPower 220. +2 blocks: both claim. Expected: stamp.totalMinted() <= office.totalEmitted() == 13.5e18. Actual: totalMinted == 13500000000000000001. Test fails 'claimed more than emitted: 13500000000000000001 > 13500000000000000000'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {StampToken} from "src/StampToken.sol";
import {CourierNFT} from "src/CourierNFT.sol";
import {PostOffice} from "src/PostOffice.sol";

/// PostOffice: total claimed can exceed totalEmitted. Each power change re-floors rewardDebt, so an office can gain
/// up to 1 wei per change on top of its exact share, while nothing offsets it. The brief's guarantee
/// "total claimed <= totalEmitted" (AUDIT.md section 3.5) does not hold.
contract RewardRoundingTest is Test {
    StampToken stamp;
    CourierNFT nft;
    PostOffice office;

    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");

    uint256 constant SECRET = 0xC0FFEE;
    uint256 constant T0 = 1_800_000_000;

    function setUp() public {
        vm.roll(100);
        vm.warp(T0);
        vm.startPrank(owner);
        stamp = new StampToken(owner, address(0), 0);
        nft = new CourierNFT(owner, treasury, 0, keccak256(abi.encode(SECRET)));
        // 1 virtual block per second, 2.25 $STAMP per block (mainnet initialReward).
        office = new PostOffice(stamp, nft, 1000, 2.25e18, 0, treasury, owner);
        stamp.setMinter(address(office));
        nft.setGame(address(office));
        office.addTier(2, 3, 0); // Kiosk
        nft.setSaleOpen(true);
        vm.stopPrank();
        for (uint256 i = 0; i < 4; i++) {
            vm.prank(bob);
            nft.mint(10);
        }
        vm.startPrank(owner);
        nft.setSaleOpen(false);
        nft.reveal(SECRET);
        vm.stopPrank();
    }

    function _find(address who, uint8 ride) internal view returns (uint256) {
        for (uint256 id = 1; id <= nft.totalMinted(); id++) {
            if (nft.ownerOf(id) == who && nft.rideOf(id) == ride) return id;
        }
        revert("no courier with that ride");
    }

    function test_ClaimsExceedTotalEmitted() public {
        uint256 foot = _find(bob, 0); // 100 power
        uint256 skate = _find(bob, 1); // 160 power

        // t0: alice 60 (trainee), bob 60 + foot = 160. totalPower 220.
        vm.prank(alice);
        office.openOffice(address(0));
        vm.startPrank(bob);
        office.openOffice(address(0));
        office.assign(foot);
        vm.stopPrank();

        // 2 blocks, then bob swaps foot for skate: 220. totalPower 280.
        vm.warp(T0 + 2);
        vm.startPrank(bob);
        office.unassign(foot);
        office.assign(skate);
        vm.stopPrank();

        // 2 blocks, then bob swaps back to foot: 160. totalPower 220.
        vm.warp(T0 + 4);
        vm.startPrank(bob);
        office.unassign(skate);
        office.assign(foot);
        vm.stopPrank();

        // 2 blocks, then everyone claims.
        vm.warp(T0 + 6);
        vm.prank(alice);
        office.claim();
        vm.prank(bob);
        office.claim();

        // 6 blocks x 2.25 = 13.5 $STAMP emitted; 13.5 $STAMP + 1 wei minted.
        assertEq(office.totalEmitted(), 13.5e18);
        assertLe(stamp.totalMinted(), office.totalEmitted(), "claimed more than emitted");
    }
}
```

### 3. Low: StampHook.price()/marketCap() read 0 after a sell outruns the pool's IMD: the swap walks empty ticks to the router's price limit

`contracts/src/StampHook.sol:375`

```
    function price(address t) public view returns (uint256) {
```

All liquidity sits on one side of the start tick. An exact-in sell asking for more IMD than the pool holds takes everything the position can pay, then keeps iterating through zero-liquidity ticks until sqrtPriceLimitX96. Both project routers pass MIN_SQRT_PRICE + 1 / MAX_SQRT_PRICE - 1 (StampRouter.sol:127, StampEthRouter.sol:177), so slot0 ends at the extreme tick. The trade itself is fine (the seller only gives up the $STAMP the pool paid for, the fee is 4% of the real output), but afterwards price() evaluates 1e18 * Q96^2 / sqrtP^2 with sqrtP at the limit and returns 0, marketCap() returns 0, and the Trade event logs the limit price, until the next buy walks the same empty ticks back (about 16 extra bitmap words of gas). Because the launch is single-sided and players mint $STAMP in the game, sells larger than the pool's IMD are the normal early state and anyone can trigger it for free; the deploy script and web/ read these views. Verified in both currency orderings (sqrtP ends at 1461446703485210103287273052203988822378723970341 with IMD as currency0, 4295128740 with IMD as currency1). Fix: cap the sell-side price limit in the routers at the launch sqrt price (nothing beyond the locked range can fill), and/or clamp price() to the launch price when slot0 is past the start tick on the empty side.

**Reproduction**

Reproduced with the attached test (forge test --match-path test/scratch/Proof_9f0c8d1e6c9c.t.sol). Fresh pool at a 330 IMD market cap (price() == 15737769455531). alice buys with 1e18 IMD through StampRouter (pool holds 0.96e18 IMD), then sells 10x the $STAMP she got with minQuoteOut 1: the call succeeds and returns 0.9216e18 IMD. Expected: price() == 15737769455531, marketCap() == 330493158566151000000. Actual: slot0.sqrtPriceX96 == MAX_SQRT_PRICE - 1, price() == 0, marketCap() == 0. Test fails 'price() after the sell: 0 != 15737769455531'. The same happens through a generic v4 router (PoolSwapTest) selling into the untouched pool.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";

import {StampHook} from "src/StampHook.sol";
import {StampRouter} from "src/StampRouter.sol";
import {StampToken} from "src/StampToken.sol";
import {DeployLib} from "script/DeployLib.sol";

contract MockIMD3 {
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

/// A sell that outruns the pool's IMD keeps walking the price through empty ticks to the router's limit. Afterwards
/// StampHook.price() / marketCap() report 0 (and the Trade event logs the limit price) until the next buy, although
/// the only liquidity sits at the launch price.
contract PriceWalkTest is Test {
    PoolManager pm;
    MockIMD3 imd;
    StampHook hook;
    StampToken stamp;
    StampRouter router;

    address owner = makeAddr("owner");
    address feeRecipient = makeAddr("feeRecipient");
    address alice = makeAddr("alice");

    uint256 constant LAUNCH = 2_100_000e18;
    uint256 constant START_MCAP = 330e18;

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        imd = new MockIMD3();

        bytes memory initCode = abi.encodePacked(
            type(StampHook).creationCode,
            abi.encode(
                pm, address(imd), owner, feeRecipient, DeployLib.startTickForMarketCap(START_MCAP, 21_000_000e18), LAUNCH,
                StampHook.ImdEthPool(10_000, 100, address(0))
            )
        );
        (bytes32 salt, address expected) = DeployLib.mineSalt(address(this), 0x28CC, initCode, 0);
        address deployed;
        assembly {
            deployed := create2(0, add(initCode, 0x20), mload(initCode), salt)
        }
        require(deployed == expected, "hook address");
        hook = StampHook(deployed);
        router = StampRouter(hook.router());

        stamp = new StampToken(owner, address(hook), LAUNCH);
        vm.prank(owner);
        hook.openPool(address(stamp));

        imd.mint(alice, 1_000e18);
        vm.startPrank(alice);
        imd.approve(address(router), type(uint256).max);
        stamp.approve(address(router), type(uint256).max);
        vm.stopPrank();
    }

    function test_SellPastThePoolsImdKeepsThePrice() public {
        uint256 launchPrice = hook.price(address(stamp));
        uint256 launchMcap = hook.marketCap(address(stamp));
        assertGt(launchPrice, 0);

        // One small buy puts 0.96 IMD in the pool.
        vm.prank(alice);
        uint256 got = router.buy(address(stamp), 1e18, 1, block.timestamp);

        // A player sells more $STAMP than that IMD covers: the pool takes what it can pay for ...
        deal(address(stamp), alice, got * 10);
        vm.prank(alice);
        uint256 imdOut = router.sell(address(stamp), got * 10, 1, block.timestamp);
        assertEq(imdOut, 0.96e18 * 96 / 100);

        // ... and the only liquidity left is the launch allocation at the launch price, so that is the price.
        assertEq(hook.price(address(stamp)), launchPrice, "price() after the sell");
        assertEq(hook.marketCap(address(stamp)), launchMcap, "marketCap() after the sell");
    }
}
```

### 4. Low: CourierNFT uses single-step Ownable (with renounceOwnership) while the owner-only, one-shot reveal() unlocks every courier mechanic

`contracts/src/CourierNFT.sol:19`

```
contract CourierNFT is ERC721, ERC2981, Ownable {
```

StampHook implements a two-step owner transfer 'so a typo can't lose the admin role' and PostOffice inherits Ownable2Step, but CourierNFT inherits plain Ownable: transferOwnership takes effect immediately and renounceOwnership is exposed. Losing this owner before reveal() is not merely losing settings: reveal is the only writer of seed, rideOf() reverts NotRevealed while seed == 0, and PostOffice.assign, unassign and levelUp all call rideOf, so no courier can ever go on duty or be levelled; the 3,333 NFTs sold for ETH are useless in the game, and setGame/setRenderer/withdraw (the mint ETH) are lost too. The launch plan moves ownership to a multisig after the mint, which is exactly the window in which reveal has not yet been called. This is an operational-hardening asymmetry rather than a bypass (the owner is trusted), but its blast radius is the whole game. Reported by audit_flow and audit_permissions; merged. Fix that preserves the design: inherit Ownable2Step as PostOffice does; optionally block renounceOwnership while seed == 0, or add a permissionless fallback reveal after a long deadline.

**Reproduction**

Scratch test (test/scratch/JudgeGame.t.sol, test_NftOwnershipTypoBricksReveal): sale closed, seed == 0, one token minted to alice. Owner calls nft.transferOwnership(address(1)). Expected (per the design goal stated for the other two contracts): pending until accepted; the deployer can still reveal. Actual: ownership moves immediately; the deployer's nft.reveal(SECRET) reverts OwnableUnauthorizedAccount(owner); alice's office.assign(1) reverts CourierNFT.NotRevealed() and nobody can ever change that. renounceOwnership() before reveal gives the same state.

### 5. Low: sellWithPermit / sellForEthWithPermit reject a permit signed for value > tokenAmount, contrary to their NatSpec

`contracts/src/StampRouter.sol:34`

```
        try IERC20Permit(token).permit(msg.sender, address(this), amount, deadline, v, r, s) {}
```

PermitHelper.permit always submits the permit with value == amount (the tokenAmount being sold). The NatSpec on sellWithPermit (StampRouter.sol:91, '`value` >= `tokenAmount`') and the mirrored sellForEthWithPermit (StampEthRouter.sol:99-111) promise that a permit signed for a larger value is acceptable. It is not: the EIP-712 digest includes value, so OZ ERC20Permit reverts ERC2612InvalidSigner, the catch branch finds allowance < amount and the sell reverts PermitFailed. A front end that signs a 'max' or rounded-up permit, or a user who signs once for their balance and sells in parts, has every sell fail. No funds at risk; the front-run case (same signature already consumed) is handled correctly. Reported by audit_flow (low) and audit_permissions (info); merged. Fix: add a permitValue parameter passed to permit() (keep the allowance >= tokenAmount fallback), or change the NatSpec on both routers to say the permit must be signed for exactly tokenAmount.

**Reproduction**

Scratch test (test/scratch/JudgeHook.t.sol, test_PermitLargerValueFails, both currency orderings): signer holds G $STAMP, allowance(signer, router) == 0, signs an EIP-2612 permit (owner=signer, spender=router, value=2*G, nonce=nonces(signer), deadline=now+100) and calls router.sellWithPermit(stamp, G, 1, deadline, v, r, s). Expected per NatSpec: the sell succeeds. Actual: revert PermitFailed(). The same call with a permit signed for exactly G succeeds.

### 6. Info: StampHook: the 4% fee rounds down, so swaps whose IMD side is under 25 wei pay no fee

`contracts/src/StampHook.sol:242`

```
        uint256 fee = exactIn ? (amount * FEE_BPS) / BPS : (amount * FEE_BPS) / (BPS - FEE_BPS);
```

Both fee formulas (here and on poolQuote at line 279) use floor division, so an IMD leg below 25 wei (24 wei for exact-out sells) pays 0 and _chargeFee returns early; larger swaps pay up to 1 wei under 4%, never over. AUDIT.md guarantee 1 says rounding never skips the fee; it does for dust. Economically irrelevant (splitting a trade into 24-wei pieces costs far more gas than the fee saved). Reported by audit_economics and audit_math; merged. Verified independently that the fee is otherwise exactly 4% in all four modes (exact-in/out, buy/sell), both currency orderings, and that the hook's ERC-6909 claims equal pendingProtocolFees after every swap (1,000-run fuzz, test/scratch/JudgeHook.t.sol). If exactness matters, round up with FullMath.mulDivRoundingUp (over-charge of at most 1 wei).

**Reproduction**

Scratch test test_DustFeeIsZero (both orderings): after one buy, an exact-in buy of 24 wei IMD through PoolSwapTest. Expected per guarantee 1: a nonzero fee. Actual: pendingProtocolFees unchanged (fee 0); the same swap with 25 wei charges 1 wei.

### 7. Info: StampHook: ERC-6909 IMD claims pushed to the hook by third parties are unrecoverable, so claims can exceed pendingProtocolFees

`contracts/src/StampHook.sol:312`

```
        uint256 amount = pendingProtocolFees[quote];
```

_collect burns and takes exactly pendingProtocolFees[quote], never the hook's actual ERC-6909 balance. Anyone can poolManager.transfer(hook, imdId, x) or mint x to the hook inside their own unlock, after which the hook holds pending + x and x is stuck forever (no function burns more than pending). Guarantee 2 states equality; the invariant that holds is claims >= pending, so the fee flow is never under-backed and no user or protocol funds are at risk. Reported by audit_economics and audit_flow; merged. If the equality is wanted, _collect can sweep poolManager.balanceOf(address(this), id).

**Reproduction**

Scratch test test_DonatedClaimsAreStuck (both orderings): after a 1,000 IMD exact-in buy pending == 40e18 and claims == 40e18. A contract unlocks, syncs IMD, transfers 5e18 to the PoolManager, settles and mints 5e18 claims to the hook. Now claims == 45e18, pending == 40e18. collectProtocolFees(IMD) sends 40e18 to feeRecipient; claims == 5e18 remain and no call can move them.

### 8. Info: PostOffice.pendingRewards reports the gross amount; claim mints less (referral cut, supply-cap clamp)

`contracts/src/PostOffice.sol:286`

```
        return o.pending + o.power * acc / PRECISION - o.rewardDebt;
```

The view the web client shows players omits two things claim applies: the referrer's referralBps share (2.5% default, up to 10%) and the clamp to MAX_SUPPLY - totalMinted, after which o.pending is zeroed and the excess dropped. Players see more than they receive. Either document the view as pre-referral or add a claimable(address) view mirroring claim.

**Reproduction**

Scratch test test_PendingViewVsClaimWithReferralChange and the repo's test_ReferrerGetsTwoAndAHalfPercent: bob opens an office, alice opens one with referrer bob, warp; pendingRewards(alice) == P. alice claims. Expected per the view: P to alice. Actual: P - P*referralBps/10000 to alice, the rest to bob.

### 9. Info: PostOffice: referral and burn rates are applied at claim/spend time, so a rate change re-splits rewards already accrued

`contracts/src/PostOffice.sol:259`

```
            refAmount = amount * referralBps / BPS;
```

Rewards accrue into o.pending with no record of the rate in force; claim applies the current referralBps to the whole pending amount and _spend applies the current burnBps. An owner call to setReferralBps (max 10%) changes the split of value other users already earned but have not claimed; the delta goes to the referrer, not the owner. Bounded and admin-triggered, so informational: document it, or settle pending at the old rate before changing it.

**Reproduction**

Scratch test test_PendingViewVsClaimWithReferralChange: alice's office referred by bob, referralBps 250, warp until pendingRewards(alice) == P. Owner calls setReferralBps(1000). alice claims. Expected if rates were snapshotted at accrual: bob gets P*250/10000. Actual: bob gets P*1000/10000 and alice P*9000/10000.

### 10. Info: PostOffice: the emission clock starts at deployment, so trainee-only offices collect the full block reward until the reveal

`contracts/src/PostOffice.sol:128`

```
        startTime = block.timestamp;
```

Era 0 (2.25 $STAMP per 1.1 s virtual block) begins when PostOffice is deployed, which DeployMainnet does in the same run that opens the pool, before the NFT sale and reveal. assign calls rideOf, which reverts until the reveal, so until then only trainees (60 power per 0.005 ETH office) earn and the whole block reward goes to whoever opened offices first: about 176,700 $STAMP per day in total regardless of how many offices exist, immediately sellable into the pool. A 14-day mint and reveal would distribute roughly 2.47M $STAMP (13% of the 18.9M emission budget) this way. A design consequence rather than a code defect; reported so the launch sequence can be confirmed (for example deploying PostOffice, or adding its first tier, only after the reveal).

**Reproduction**

Scratch test test_TraineeEarnsEverythingBeforeReveal (blockTimeMs 1100, initialReward 2.25e18): one player opens an office right after deployment, nobody else does; warp 1 day (78,545 virtual blocks). pendingRewards(player) == 176726250000000000000000 (176,726 $STAMP), claimable, while office.assign(1) reverts NotRevealed.

### 11. Info: StampHook constructor accepts start ticks for which openPool always reverts (liquidity overflow), stranding the launch allocation

`contracts/src/StampHook.sol:139`

```
        if (startTick_ % TICK_SPACING != 0 || startTick_ > limit || startTick_ < -limit) revert BadTick();
```

The BadTick guard only checks spacing and the usable-tick bound. For very negative start ticks the liquidity computed in _addLaunchLiquidity exceeds int128 or tickSpacingToMaxLiquidityPerTick(200), so poolManager.modifyLiquidity reverts and openPool can never succeed; the 2.1M $STAMP minted to the hook by StampToken's constructor has no other way out. Reaching it needs a grossly wrong START_MCAP input (about 1e20 IMD per $STAMP) and the forge simulation would fail before broadcasting, so informational. Fix: compute the launch liquidity in the constructor and revert BadTick if it overflows, or tighten the limit to |startTick| <= 400_000.

**Reproduction**

Scratch test JudgeBadTick.test_Sweep: deploy StampHook with startTick in {-887000, -700000, -500000} (constructor accepts), deploy StampToken(owner, hook, 2.1M), call openPool as owner. Expected: pool opened. Actual: openPool reverts for all three (TickLiquidityOverflow / SafeCastOverflow); -400000, 110600 and 887000 succeed.

### 12. Info: Test suite never exercises the $STAMP-as-currency0 ordering, exact fee equality for three of four swap modes, PartialFill, permit sells or collection during a foreign unlock

`contracts/test/StampHook.t.sol:105`

```
        stamp = new StampToken(owner, address(hook), LAUNCH);
```

Whether IMD or $STAMP is currency0 on mainnet depends on the deployer's nonce-derived StampToken address versus 0x5F7B...7127 and is unknown until deploy. In the suite MockIMD lands at 0x2e23...470b and StampToken at 0xD6Bb...FBfF, so only the IMD-as-currency0 branch of _addLaunchLiquidity (the mulDiv(sqrtL, sqrtU, Q96) formula, the [tick, maxUsableTick] range) and the mirrored sign handling in the hook and routers run. test_EveryRouteAndDirectionIsTaxed asserts exact equality only for the exact-in buy (assertGt elsewhere). No test triggers PartialFill, exercises sellWithPermit / sellForEthWithPermit, or collects fees inside another contract's unlock. I re-ran these in both orderings (test/scratch/JudgeHook.t.sol: 1,000-run fuzz of exact fee equality in all four modes, PartialFill, permit) and they pass, so this is a coverage gap, not a defect. Fix: vm.etch a mock IMD at a low and a high address and run the hook/router suite as two contracts; replace assertGt with the exact formulas.

**Reproduction**

forge test --match-contract StampHookTest -vvvv shows MockIMD at 0x2e234DAe75C793f67A35089C9d99245E1C58470b and StampToken at 0xD6BbDE9174b1CdAa358d2Cf4D57D1a9F7178FBfF in every run, so IMD is always currency0. Etching the mock IMD at address(type(uint160).max) flips the ordering and the branch at StampHook.sol:213 runs with no assertion in the repo covering it.

---

Judge's submission `54062dd39a90d3bd9924d3b73bce1c746b0c19db9eca81cfca67cb2bca931a53`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
