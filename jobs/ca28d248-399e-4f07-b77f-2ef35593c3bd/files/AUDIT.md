# Audit report

> Courier ($STAMP), re-check of IMD Swarm audit ea514609 (that audit read commit 0a2ce30; this is commit 312f6a9). Read AUDIT.md first: section 6 maps every finding to its fix and the test that reproduces it, and section 1 describes the system as it is now.
>
> What it is: a game on Robinhood Chain (4663). Players put Courier NFTs on duty at post offices and earn $STAMP (21M cap), which trades in one Uniswap v4 pool against IMD; the hook takes 4% of the IMD side of every swap, rounded up, all to the protocol, and locks a 2.1M single-sided launch allocation forever. It launches in two stages from one wallet: stage 1 deploys the NFT for the mint; stage 2, only after the reveal, deploys the token, the pool and the post office, links them, and renounces every owner, so nothing has an owner afterwards.
>
> Scope: contracts/src/StampHook.sol, StampRouter.sol, StampEthRouter.sol, StampToken.sol, PostOffice.sol, CourierNFT.sol, lib/SafeTransfer.sol, contracts/script/DeployMainnet.s.sol, DeployCouriers.s.sol, DeployLib.sol. Out of scope: the view-only art (CourierRenderer, CourierSVG, CourierTraits), the dev scripts (Deploy.s.sol, DeployFork.s.sol) and web/.
>
> What changed, and what to look at hardest:
> 1. PostOffice has no owner (costs, rates and tiers fixed) and refuses to deploy before the couriers are revealed; reward debt is now kept unscaled (power x accRewardPerPower) so each stretch rounds down once. Check that total minted can never exceed totalEmitted, under any order of assign, unassign, levelUp on duty and claims, and that the new claimable() view matches claim().
> 2. Routers stop sells at the launch price (StampHook.sellPriceLimit); price() reports the launch price when the pool sits beyond it. Check both $STAMP/IMD orderings, partial sells, the ETH router's sell path, and that nothing else changed in the fee or settlement.
> 3. The fee rounds up (mulDivRoundingUp) in beforeSwap and afterSwap. Check the PartialFill accounting still holds in all four modes and that no trader pays more than 1 wei over 4%.
> 4. Start tick bounded to +-400,000 and launch to 21M: check that every accepted constructor input opens.
> 5. CourierNFT: Ownable2Step; renounceOwnership reverts until the couriers are revealed and the game is set; mint payments go straight to the treasury; reveal ends the sale itself. PostOffice office payments go straight to the treasury.
> 6. The deploy scripts: stage 2 must leave no owner on StampToken, StampHook, CourierRenderer or CourierNFT (it logs each), and must not be runnable before the reveal or from another wallet.
>
> Tests: cd contracts; git submodule update --init --recursive; forge test (86 tests; the hook suite runs with IMD as currency0 and as currency1). Fork: forge test --match-contract StampHookForkTest --fork-url https://robinhood.drpc.org. Both launch stages against a fork with the real settings: ./script/deploy-mainnet.sh rehearse.

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/courierworld.git |
| Commit | `d5a04ed5b1678b0ecc5d13fa14e95d55436ed7de` |
| Job | `ca28d248-399e-4f07-b77f-2ef35593c3bd` |
| Judged | 2026-10-08 21:48 UTC |
| Findings | 2 low · 2 info |

Four agents audited the code as it is at `d5a04ed`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: StampHook constructor accepts launch allocations below ~1.49e9 wei at \|startTick\| = 400,000, for which openPool always reverts (CannotUpdateEmptyPosition)

`contracts/src/StampHook.sol:144`

```
        if (launchSupply_ <= LIQUIDITY_BUFFER || launchSupply_ > MAX_LAUNCH_SUPPLY) revert BadToken();
```

AUDIT.md section 1, guarantee 3 and the resolution of finding 11 state that every (start tick, launch allocation) the constructor accepts leads to a working openPool. The constructor bounds |startTick_| <= 400,000 and launchSupply_ <= 21M, but its lower bound only requires launchSupply_ > LIQUIDITY_BUFFER (1e9 wei). _addLaunchLiquidity (lines 214-217) computes the position's liquidity from launchSupply - 1e9 with floor division. At startTick = +400,000 the price factor across the launch range is about e^20 (4.85e8): with IMD as currency0 the range is [minUsableTick, 400000] and liquidity = amount * Q96 / (sqrtU - sqrtL) ~= amount / 4.85e8; with IMD as currency1 the pool tick is -400,000, the range is [-400000, maxUsableTick] and liquidity ~= amount * sqrtL / Q96 ~= amount * 2.06e-9. For any accepted allocation below about 1e9 + 4.85e8 wei the liquidity floors to 0, PoolManager.modifyLiquidity reverts CannotUpdateEmptyPosition, and openPool can never succeed for that hook. Because renounceOwnership requires a launched token, the hook also cannot be renounced; the allocation minted to it by StampToken is unrecoverable and the hook has to be redeployed. test_StartPriceIsBoundedSoOpenPoolAlwaysWorks only tries 2.1M and 21M as its 'smallest and largest' allocations, so the low end of the accepted range is untested. The real launch (2.1M $STAMP, launch.env) is unaffected, and a failing openPool is caught in the script simulation before broadcast, which keeps this low. This merges the three specialist reports (audit_math, audit_economics, audit_permissions), which describe the same mechanism at the same line. Fix: make the constructor's lower bound match what opens, for example require launchSupply_ >= LIQUIDITY_BUFFER + 1e18 (opens at every tick in range for both orderings), or compute the launch liquidity in the constructor and revert when it is 0; then add the minimum allocation to the corner test.

**Reproduction**

Deploy StampHook at a mined 0x28CC address with startTick_ = 400_000 and launchSupply_ = 1_400_000_000 wei (both pass the constructor: 400_000 % 200 == 0, |tick| <= 400_000, 1e9 < 1.4e9 <= 21M). Deploy StampToken(owner, hook, 1_400_000_000) so the hook holds the allocation, then call hook.openPool(token) as owner. Expected: the pool opens (the constructor accepted the inputs, AUDIT.md guarantee 3). Actual: liquidity = floor(4e8 * Q96 / (sqrtPriceAtTick(400000) - sqrtPriceAtTick(-887200))) = 0 with IMD as currency0, and floor(4e8 * (sqrtL*sqrtU/Q96) / (sqrtU - sqrtL)) = 0 with IMD as currency1; PoolManager.modifyLiquidity reverts CannotUpdateEmptyPosition() in both orderings. Same for launchSupply_ = 1e9 + 1. Verified: the three specialist proofs all fail with CannotUpdateEmptyPosition on this code (5 of their 6 cases; the one passing case used tick -400_000 with IMD as currency1, which is the opposite, liquidity-rich corner). The attached proof fails in all three cases on this code and passes once the constructor rejects the inputs (checked locally with a temporary minimum of LIQUIDITY_BUFFER + 1e18, then reverted).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {StampHook} from "src/StampHook.sol";
import {StampToken} from "src/StampToken.sol";

contract ImdStub {
    function balanceOf(address) external pure returns (uint256) {
        return 0;
    }
}

/// AUDIT.md guarantee 3 / finding 11: every (startTick, launchSupply) the StampHook constructor accepts must open.
/// Today the constructor accepts startTick = 400_000 with launchSupply = 1.4e9 wei, and openPool reverts
/// CannotUpdateEmptyPosition because the launch liquidity floors to 0. The test passes once the constructor
/// rejects such inputs (a higher minimum, or a liquidity check) or openPool handles them.
contract AcceptedLaunchOpensTest is Test {
    PoolManager pm;
    address owner = makeAddr("owner");

    function setUp() public {
        pm = new PoolManager(address(this));
    }

    /// Deploys the hook at a mined 0x28CC address. Returns address(0) if the constructor rejects the inputs.
    function _hook(address imd, int24 tick, uint256 launch) internal returns (address h) {
        bytes memory initCode = abi.encodePacked(
            type(StampHook).creationCode,
            abi.encode(pm, imd, owner, owner, tick, launch, StampHook.ImdEthPool(10_000, 100, address(0)))
        );
        bytes32 hash = keccak256(initCode);
        bytes32 salt;
        for (uint256 i;; i++) {
            address a = address(uint160(uint256(keccak256(abi.encodePacked(bytes1(0xff), address(this), bytes32(i), hash)))));
            if (uint160(a) & 0x3FFF == 0x28CC) {
                salt = bytes32(i);
                break;
            }
        }
        assembly {
            h := create2(0, add(initCode, 0x20), mload(initCode), salt)
        }
    }

    function _check(address imdAddr, int24 tick, uint256 launch) internal {
        vm.etch(imdAddr, address(new ImdStub()).code);
        address h = _hook(imdAddr, tick, launch);
        if (h == address(0)) return; // rejected by the constructor: nothing to open
        StampToken s = new StampToken(owner, h, launch);
        vm.prank(owner);
        StampHook(h).openPool(address(s)); // accepted by the constructor, so this must work
        assertEq(StampHook(h).token(), address(s));
        assertEq(s.balanceOf(h), 0);
    }

    function test_AcceptedSmallLaunchAtTopTickOpens_ImdFirst() public {
        _check(address(0x1000), 400_000, 1_400_000_000);
    }

    function test_AcceptedSmallLaunchAtTopTickOpens_ImdSecond() public {
        _check(address(uint160(type(uint160).max) - 0x1000), 400_000, 1_400_000_000);
    }

    function test_AcceptedSmallestLaunchAtTopTickOpens_ImdFirst() public {
        _check(address(0x1000), 400_000, 1_000_000_001);
    }
}
```

### 2. Low: Stage 2 links, renounces and logs the renderer recorded in robinhood-couriers.json / RENDERER, not the renderer the NFT actually uses, so a renderer swapped between the stages keeps its owner and neve

`contracts/script/DeployMainnet.s.sol:118`

```
        CourierRenderer(c.renderer).setOffice(ICourierDuty(address(office)));
        CourierRenderer(c.renderer).renounceOwnership();
```

_deployGame calls setOffice and renounceOwnership on c.renderer, which comes from deployments/robinhood-couriers.json (written by stage 1) or the RENDERER env var, and then calls CourierNFT.freezeRenderer(), which freezes whatever CourierNFT.renderer() is at that moment. Nothing checks that the two are the same contract. AUDIT.md section 4 lists setRenderer (until frozen) as an admin power the NFT owner keeps between stage 1 and stage 2, e.g. to fix the art. If the owner uses it and does not also edit the JSON, stage 2 runs to completion: the detached renderer R1 gets the office link and is renounced, while the renderer R2 the NFT is now frozen on keeps the deployer as owner and has office == 0, so tokenURI never shows level or ON DUTY. _log prints CourierRenderer(c.renderer).owner(), i.e. R1's, so it reports 0x0 and the operator sees nothing wrong. This breaks the brief's requirement that stage 2 leave no owner on CourierRenderer and guarantee 8 (no contract has an owner after launch); R2's owner can still call setOffice once, which is the only remaining power (and R2 is used by a frozen, ownerless NFT). The precondition is an operator action (a renderer swap without updating the JSON), so this is low. Fix: in _deployGame derive the renderer from the NFT, c.renderer = address(CourierNFT(c.nft).renderer()), or require(address(CourierNFT(c.nft).renderer()) == c.renderer, ...) before linking, and have _log read the owner of CourierNFT(c.nft).renderer().

**Reproduction**

Verified with contracts/test/scratch/DeployRenderer.t.sol, which inherits CourierDeployer and runs the real _deployGame with a PoolManager and a stub IMD deployed at the script's hard-coded mainnet addresses. Stage 1: c = _deployCouriers(deployer, deployer, 0.003 ether, commit) gives NFT N and renderer R1. Between stages the owner deploys R2 = new CourierRenderer(N, new CourierSVG(), deployer), calls N.setRenderer(R2), then N.reveal(secret). Stage 2: _deployGame(deployer, deployer, deployer, 3000e18, 2_100_000e18, 0.005 ether, 1100, c) with c.renderer still R1 does not revert. Expected: the renderer the NFT is frozen on has owner 0 and office == PostOffice. Actual: N.rendererFrozen() == true, N.renderer() == R2, R1.owner() == 0 (what _log prints as 'Owner: Renderer'), but R2.owner() == deployer (0x7FA9385bE102ac3EAc297483Dd6233D62b3e1496 in the test) and R2.office() == 0. Test output: '[FAIL: the live renderer should be renounced: 0x7FA9...1496 != 0x0000...0000]'.

### 3. Info: CourierNFT.setTreasury moves mint revenue but leaves the ERC-2981 royalty receiver on the old treasury

`contracts/src/CourierNFT.sol:192`

```
    function setTreasury(address treasury_) external onlyOwner {
        if (treasury_ == address(0)) revert ZeroAddress();
        treasury = treasury_;
    }
```

The constructor couples the two destinations: it stores treasury for mint payments and calls _setDefaultRoyalty(treasury_, 500) for secondary-sale royalties. setTreasury only updates the first. An owner who changes the treasury before stage 2 (the only window in which the setter works, since the game deploy renounces the NFT) ends up with mint ETH going to the new address while marketplaces keep paying royalties to the old one unless they also remember to call setRoyalty. No funds are lost and no third party can trigger it; it is an asymmetry between the constructor and its setter, pre-launch only. Fix: have setTreasury also call _setDefaultRoyalty(treasury_, <current bps>), or document that setRoyalty must be called alongside it. (Reported by audit_flow; reproduced.)

**Reproduction**

Deploy CourierNFT(owner, T1, 0.003 ether, commit); owner calls setSaleOpen(true) and setTreasury(T2); alice calls mint{value: 0.003 ether}(1); then royaltyInfo(1, 1 ether). Expected: mint ETH and royalties both go to T2, or a documented need to call setRoyalty. Actual: T2.balance == 0.003 ether while royaltyInfo returns (T1, 0.05 ether). Verified in contracts/test/scratch/NftAdmin.t.sol::test_SetTreasuryLeavesRoyaltyReceiverBehind (passes, asserting the mismatch).

### 4. Info: CourierNFT.renounceOwnership does not require the renderer to be frozen, so rendererFrozen can read false forever on an ownerless collection

`contracts/src/CourierNFT.sol:174`

```
        if (seed == 0 || game == address(0)) revert NotFinished();
```

The guard added for audit finding 4 checks the reveal and the game link but not the renderer freeze. If the owner renounces without first calling freezeRenderer(), nobody can call setRenderer or freezeRenderer any more (both onlyOwner), so the art is in fact final, but the public rendererFrozen() flag that AUDIT.md section 1 presents as the signal that 'the art can never be changed again' reads false permanently. The mainnet script (_deployGame) calls freezeRenderer() immediately before renounceOwnership(), so the shipped flow is correct; the guard just does not enforce the invariant the flag advertises, and a manual or partial stage 2 could leave it unset. Fix: add `|| !rendererFrozen` to the NotFinished check, or set rendererFrozen inside renounceOwnership. (Reported by audit_flow; reproduced.)

**Reproduction**

Owner: reveal(secret); setGame(office); renounceOwnership() without freezeRenderer(). Expected: NotFinished, or the renderer frozen as part of renouncing. Actual: owner() == address(0), rendererFrozen() == false, and both freezeRenderer() and setRenderer() now revert OwnableUnauthorizedAccount for everyone. Verified in contracts/test/scratch/NftAdmin.t.sol::test_RenounceWithoutFreezeLeavesFlagFalse (passes, asserting the stuck flag).

---

Judge's submission `1bda366afbb9555d0558436367abb2e88c01a11d73cf1dad8b6d85eb8176be54`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
