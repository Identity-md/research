# Audit report

> Courier ($STAMP), final check after IMD Swarm re-check ca28d248 (which read commit d5a04ed; this is commit ca016a4). Read AUDIT.md first: section 7 maps each re-check finding to its fix and test, section 6 does the same for the first audit ea514609, and section 1 describes the system.
>
> What it is: a game on Robinhood Chain (4663). Players put Courier NFTs on duty at post offices and earn $STAMP (21M cap), which trades in one Uniswap v4 pool against IMD; the hook takes 4% of the IMD side of every swap, rounded up, all to the protocol, and locks a single-sided launch allocation forever. Two launch stages from one wallet: stage 1 deploys the NFT for the mint; stage 2, only after the reveal, deploys the token, pool and post office, links them, freezes the art and renounces every owner.
>
> Scope: contracts/src/StampHook.sol, StampRouter.sol, StampEthRouter.sol, StampToken.sol, PostOffice.sol, CourierNFT.sol, lib/SafeTransfer.sol, contracts/script/DeployMainnet.s.sol, DeployCouriers.s.sol, DeployLib.sol. Out of scope: the view-only art (CourierRenderer, CourierSVG, CourierTraits), the dev scripts (Deploy.s.sol, DeployFork.s.sol) and web/.
>
> Changes in this round, and what to check:
> 1. StampHook: launch allocation must be at least 1 $STAMP (MIN_LAUNCH_SUPPLY) and at most 21M, start tick within +-400,000. Check that every input the constructor accepts gives a nonzero launch liquidity within v4's per-tick cap, so openPool always succeeds, in both $STAMP/IMD orderings.
> 2. Stage 2 (_deployGame) requires the NFT's current renderer and DeployMainnet reads it from the NFT. Check that stage 2 can never leave a renderer, the NFT, the token or the hook with an owner, or freeze a renderer it didn't link.
> 3. CourierNFT.setTreasury moves the ERC-2981 receiver along with mint payments (rate unchanged); renounceOwnership now also requires rendererFrozen. Check no ordering of owner calls before renouncing leaves funds or royalties pointing somewhere unintended, or the collection unrevealed, unlinked or unfrozen.
> 4. Confirm the earlier fixes still hold: total minted never exceeds totalEmitted, the fee is never below 4% nor more than 1 wei over it in all four modes, sells stop at the launch price, and no admin power reaches user funds.
>
> Tests: cd contracts; git submodule update --init --recursive; forge test (88 tests; the hook suite runs in both orderings). Fork: forge test --match-contract "StampHookForkTest|LaunchStagesForkTest" --fork-url https://robinhood.drpc.org (the second runs the real stage 2 after a renderer swap). Both launch stages with the real settings: ./script/deploy-mainnet.sh rehearse.

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/courierworld.git |
| Commit | `633ab97b01461431f5ee449d98e9a43662744675` |
| Job | `19b34b9b-94ef-4543-8d85-b05028860fcf` |
| Judged | 2026-10-08 22:44 UTC |
| Findings | 3 low · 2 info |

Four agents audited the code as it is at `633ab97`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: CourierNFT.freezeRenderer freezes whatever `renderer` holds, including address(0), a codeless or foreign-owned contract: the collection can be frozen with no on-chain art, which still satisfies renoun

`contracts/src/CourierNFT.sol:180`

```
    function freezeRenderer() external onlyOwner {
        rendererFrozen = true;
        emit RendererFrozen();
    }
```

Re-check ca28d248 finding 4 made renounceOwnership require rendererFrozen so an ownership mistake cannot leave the art changeable. freezeRenderer itself validates nothing: it raises the flag for whatever `renderer` currently holds. setRenderer accepts any value, including address(0) (the documented fallback to baseURI), so the owner can freeze an empty renderer. From then on setRenderer reverts RendererIsFrozen forever, so the CourierRenderer from stage 1 can never be re-attached and tokenURI stays on the off-chain baseURI/unrevealedURI strings. Stage 2 can never run against the collection: DeployMainnet reads nft.renderer() (address(0)), the equality require in _deployGame passes trivially, and `CourierRenderer(address(0)).setOffice(...)` reverts on the code-less target (DeployMainnet.s.sol:121), so the game can only be launched by hand with the art permanently off-chain. Meanwhile the three renounce conditions (seed != 0, game != 0, rendererFrozen) are all satisfiable, so the owner can still reveal, setGame and renounce: the collection reads as 'art final' with no art linked. Variants reproduced the same way: a renderer with no code (tokenURI reverts forever once frozen), a renderer owned by someone else (stage 2's setOffice reverts OwnableUnauthorizedAccount and the renderer cannot be swapped), a renderer already linked (OfficeAlreadySet). This is the mirror of the mistake the re-check guarded against: frozen on the wrong thing instead of not frozen. The project's own CourierFixture never attaches a renderer, so test_RenounceOnlyOnceRevealedLinkedAndFrozen and test_GameRunsWithNobodyInCharge freeze and renounce with renderer == 0 and would not catch it. Reported independently by four specialists (permissions, flow, math, economics); merged here. Minimal fix that keeps the design: in freezeRenderer, `if (address(renderer) == address(0)) revert ZeroAddress();` (optionally also require address(renderer).code.length > 0, and in _deployGame check CourierRenderer(c.renderer).owner() == deployer and .nft() == c.nft before deploying anything). With the guard, the two fixture tests above need the fixture to attach a renderer before freezing, as DeployCouriers does.

**Reproduction**

State: CourierNFT after stage 1 (renderer attached), revealed. Owner calls nft.setRenderer(ICourierRenderer(address(0))) then nft.freezeRenderer(). Expected: freezeRenderer reverts because there is nothing to freeze. Actual: it succeeds; rendererFrozen() == true, renderer() == address(0); nft.setRenderer(realRenderer) now reverts RendererIsFrozen; CourierDeployer._deployGame with Couriers{nft, renderer: nft.renderer()} (what DeployMainnet._couriers builds) reverts at CourierRenderer(address(0)).setOffice (verified on a Robinhood Chain fork: test_Fork_StageTwoRevertsWhenRendererFrozenAtZero); nft.setGame(x); nft.renounceOwnership() then succeed with owner() == 0. The attached proof fails on this commit with 'next call did not revert as expected' and passes once freezeRenderer refuses an unset renderer. Variant checked locally: setRenderer(rendererOwnedByStranger); freezeRenderer(); stranger-owned setOffice from the deployer reverts OwnableUnauthorizedAccount(owner) and setRenderer reverts RendererIsFrozen, yet setGame + renounceOwnership succeed.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {CourierNFT, ICourierRenderer} from "src/CourierNFT.sol";
import {CourierSVG} from "src/CourierSVG.sol";
import {CourierRenderer, ICourierSeed} from "src/CourierRenderer.sol";

/// freezeRenderer() must refuse to freeze when no renderer is attached: otherwise the 'art is frozen' flag is set
/// with no art, renounceOwnership's rendererFrozen guard is satisfied, no renderer can ever be attached again, and
/// stage 2 (which calls setOffice on nft.renderer()) can never run against this collection.
contract FreezeWithoutRendererProof is Test {
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    uint256 constant SECRET = 7;

    function test_FreezeWithNoRendererIsRefused() public {
        vm.startPrank(owner);
        CourierNFT nft = new CourierNFT(owner, treasury, 0.003 ether, keccak256(abi.encode(SECRET)));
        CourierRenderer renderer = new CourierRenderer(ICourierSeed(address(nft)), new CourierSVG(), owner);
        nft.setRenderer(ICourierRenderer(address(renderer))); // stage 1 attaches the art
        nft.reveal(SECRET);

        // Owner mistake between the stages: detach the art, then try to freeze it.
        nft.setRenderer(ICourierRenderer(address(0)));
        vm.expectRevert();
        nft.freezeRenderer();
        assertFalse(nft.rendererFrozen());

        // With the art attached again, freezing works and the renounce guard is meaningful.
        nft.setRenderer(ICourierRenderer(address(renderer)));
        nft.freezeRenderer();
        assertTrue(nft.rendererFrozen());
        assertEq(address(nft.renderer()), address(renderer));
        vm.stopPrank();
    }
}
```

### 2. Low: CourierNFT.setTreasury unconditionally overwrites the ERC-2981 receiver, so setRoyalty(artist, bps) followed by setTreasury(x) silently redirects royalties from the artist to x, permanently after reno

`contracts/src/CourierNFT.sol:198`

```
        _setDefaultRoyalty(treasury_, uint96(bps));
```

Re-check ca28d248 finding 3 made setTreasury move the default royalty receiver to the new treasury at the existing rate. The NFT also exposes setRoyalty(receiver, bps), which can deliberately point royalties at an address that is not the treasury (an artist, a splitter). Both setters write the same ERC2981 default-royalty slot, and setTreasury does so without checking whether the current receiver is the treasury being replaced. So the ordering setRoyalty(artist, bps) then setTreasury(newTreasury) ends with royalties at newTreasury and nothing naming the artist in the call, no event and no revert, while the opposite ordering keeps them on the artist. After the stage-2 renounceOwnership this cannot be corrected. This is exactly the ordering class this round asked about ('no ordering of owner calls before renouncing leaves funds or royalties pointing somewhere unintended'). The NatSpec on setTreasury does say both follow the treasury, so it is partly a design coupling, but setRoyalty's receiver parameter contradicts it. Reported by the permissions and economics specialists; merged. Minimal fix that preserves the re-check behaviour: in setTreasury, move the receiver only when it currently equals the old treasury: `(address receiver, uint256 bps) = royaltyInfo(0, _feeDenominator()); if (receiver == treasury) _setDefaultRoyalty(treasury_, uint96(bps)); treasury = treasury_;`. Alternatively drop the receiver parameter from setRoyalty and document that the treasury is the only receiver.

**Reproduction**

Owner calls nft.setRoyalty(artist, 700) then nft.setTreasury(safe). Expected: royaltyInfo(1, 1 ether) == (artist, 0.07 ether) and mint payments go to safe. Actual: royaltyInfo(1, 1 ether) == (safe, 0.07 ether). In the other order (setTreasury(safe) then setRoyalty(artist, 700)) the artist keeps the royalties, and a later setTreasury(safe2) moves them again to safe2 (checked locally). The attached proof's test_SetTreasuryKeepsADeliberateRoyaltyReceiver fails on this commit (receiver == safe, not artist) and passes with the fix; its second test shows the re-check-3 behaviour is preserved.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {CourierNFT} from "src/CourierNFT.sol";

/// setRoyalty(receiver, bps) lets the owner give royalties to an address that is not the treasury (an artist).
/// setTreasury(newTreasury) then silently rewrites that receiver to the new treasury. After renounceOwnership
/// the artist's royalties are permanently redirected. Fails on the current code; passes once setTreasury only
/// moves the royalty receiver when it still points at the treasury being replaced.
contract TreasuryClobbersRoyaltyTest is Test {
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address artist = makeAddr("artist");
    address safe = makeAddr("safe");
    uint256 constant SECRET = 7;

    function test_SetTreasuryKeepsADeliberateRoyaltyReceiver() public {
        CourierNFT nft = new CourierNFT(owner, treasury, 0.003 ether, keccak256(abi.encode(SECRET)));
        vm.startPrank(owner);
        nft.setRoyalty(artist, 700); // royalties deliberately to the artist, 7%
        nft.setTreasury(safe); // mint payments move to a Safe
        vm.stopPrank();

        (address receiver, uint256 amount) = nft.royaltyInfo(1, 1 ether);
        assertEq(amount, 0.07 ether, "rate kept");
        // Expected: royalties still go to the artist. Actual (current code): they now go to the Safe.
        assertEq(receiver, artist, "royalty receiver silently moved by setTreasury");
    }

    function test_SetTreasuryStillMovesRoyaltiesThatFollowedTheTreasury() public {
        CourierNFT nft = new CourierNFT(owner, treasury, 0.003 ether, keccak256(abi.encode(SECRET)));
        vm.startPrank(owner);
        nft.setRoyalty(treasury, 300);
        nft.setTreasury(safe);
        vm.stopPrank();
        (address receiver, uint256 amount) = nft.royaltyInfo(1, 1 ether);
        assertEq(receiver, safe);
        assertEq(amount, 0.03 ether);
    }
}
```

### 3. Low: IMD is an owner-controlled token with a blocklist; once the hook is renounced the only fee destination, feeRecipient, is immutable, so a block on that address strands every protocol fee until lifted

`contracts/src/StampHook.sol:327`

```
        poolManager.take(Currency.wrap(quote), feeRecipient, amount);
```

Trust-gap between an external admin and an immutable setting. The live IMD at 0x5F7Bb59365ce557C26dbcAa4EE9d39A4b95B7127 on Robinhood Chain (chain 4663) is not a plain ERC-20: it is owned by the EOA 0x047F606fD5b2BaA5f5C6c4aB8958E45CB6B054B7 and exposes blocked(address), setBlocked(address,bool) (eth_call from the owner succeeds, from any other address reverts OwnableUnauthorizedAccount), transfersEnabled(), enableTransfers() and setV4Config(address,address,bool). Its transfer reverts 'BridgedFP: blocked' when the recipient is blocked, including the transfer the PoolManager makes in take(). StampHook.collectProtocolFees is the only path by which fees leave the PoolManager and it can only send to feeRecipient, which becomes final when stage 2 calls renounceOwnership. If the IMD owner blocks feeRecipient (deliberately or by mistake), _collect reverts for everyone: swaps keep working and keep minting ERC-6909 IMD claims to the hook (the fee path never transfers ERC-20 IMD), pendingProtocolFees keeps growing, and nothing can redirect it. The fees are recoverable only if the IMD owner unblocks the address. AUDIT.md sections 3.2 and 5 do not mention this dependency. Not a Courier permission bypass, but guarantee 2 ('collectProtocolFees sends exactly that to feeRecipient') depends on a third party's admin key, and the launch wallet is both FEE_RECIPIENT and TREASURY. Suggested handling: document it as a trust assumption in section 5, and consider a recovery path that does not reintroduce an owner, e.g. let the current feeRecipient rotate itself (`function setFeeRecipient(address) external { if (msg.sender != feeRecipient) revert NotOwner(); ... }` once owner == 0), or let collectProtocolFees take a destination only when called by feeRecipient. Open item: setV4Config(address,address,bool)/poolManager() on IMD (currently zero) may let the IMD owner apply special rules to PoolManager transfers; worth asking the IMD team before launch. Side observation, the token's policy rather than a Courier defect: a blocked user cannot buy or sell through StampRouter (take/transferFrom to a blocked address reverts) but can still trade through StampEthRouter, since IMD never leaves the PoolManager on that path. Reported by the permissions specialist; reproduced on a fork.

**Reproduction**

On a Robinhood Chain fork (forge test --fork-url https://robinhood.drpc.org): deploy the hook as StampHookForkTest does with feeRecipient = F, deploy StampToken (2.1M to the hook), openPool, renounceOwnership. 1) alice buyWithEth{0.01 ether}; collectProtocolFees(IMD) succeeds and F receives 124496871883179848 wei IMD (sanity). 2) alice buys again; pendingProtocolFees(IMD) > 0; vm.prank(IMD.owner()); IMD.setBlocked(F, true). 3) collectProtocolFees(IMD): expected per guarantee 2 to send the pending amount to F; actual: reverts with v4 WrappedError(0x90bfb865) wrapping IMD.transfer's 'BridgedFP: blocked', pendingProtocolFees unchanged, owner() == 0 so no function can change feeRecipient. 4) further buys succeed and pendingProtocolFees keeps rising. 5) IMD.setBlocked(F, false): collection works again, showing the harm is exactly the stranding while blocked. Also observed: a blocked user's StampEthRouter.buyWithEth succeeds (20421934974834588368535 wei STAMP for 0.01 ETH) while their StampRouter.sell reverts.

### 4. Info: Stage 2 takes the post office treasury from the TREASURY env and never reconciles it with the NFT's treasury, so mint payments and royalties can end up at one final address and office sales and the 25

`contracts/script/DeployMainnet.s.sol:201`

```
        address treasury = vm.envOr("TREASURY", feeRecipient);
```

launch.env documents one TREASURY that 'Receives NFT mint and post office sales, and 25% of $STAMP spent in the game'. The NFT's treasury (mint payments and, since this round, the ERC-2981 receiver) is fixed in stage 1 from that run's TREASURY (default FEE_RECIPIENT) and is mutable through setTreasury until renounce; PostOffice.treasury is immutable and set in stage 2 from the TREASURY env of that run. Nothing compares the two: _deployGame neither requires CourierNFT(c.nft).treasury() == treasury nor calls setTreasury before freezeRenderer/renounceOwnership, and _log prints neither treasury. If the value differs between the runs (launch.env edited, TREASURY unset in one run so it fell back to a changed FEE_RECIPIENT, or the owner moved the NFT treasury to a Safe between the stages), the game's 25% spend share and office sales go to the stage-2 address forever while royalties on every secondary sale go to the stage-1 address forever; deployments/robinhood.json records only the stage-2 one. Re-check finding 2 was fixed by making stage 2 read the renderer from the NFT rather than trusting an input; the treasury has the same shape. Reported by the flow and math specialists; merged. Minimal fix: in DeployMainnet.run (or _deployGame) `require(CourierNFT(c.nft).treasury() == treasury, "treasury differs from the couriers'")`, or default `treasury` to CourierNFT(c.nft).treasury() when TREASURY is unset, and print both treasuries in _log.

**Reproduction**

Stage 1 with treasury A: _deployCouriers(deployer, A, 0.003 ether, commit); reveal. Stage 2 with treasury B: _deployGame(deployer, feeRecipient, B, 3_000e18, 2_100_000e18, 0.005 ether, 1_100, c) (what DeployMainnet.run does with TREASURY=B). Expected: one treasury for the whole system, or a refusal. Actual (Robinhood Chain fork, test_Fork_StageTwoTreasuryCanDivergeFromTheNfts): PostOffice(g.office).treasury() == B, nft.treasury() == A, royaltyInfo(1, 1 ether) receiver == A, nft.owner() == address(0): both are final and differ.

### 5. Info: CourierNFT.setGame is one-shot and accepts any nonzero address, so a mistaken call before stage 2 permanently prevents the collection from being linked to the real post office, while renounceOwnership

`contracts/src/CourierNFT.sol:136`

```
        if (game != address(0)) revert GameAlreadySet();
```

Guarantee 6 says the collection cannot be left unlinked by an ownership mistake, and renounceOwnership refuses while game == address(0). But setGame can be called once with any nonzero address and never corrected. If the owner calls it by hand with a wrong address (an EOA, an old PostOffice from a dev run, a PostOffice whose `couriers` is a different NFT), stage 2 reverts GameAlreadySet at _deployGame's nft.setGame(office) (DeployMainnet.s.sol:120) every time, so no scripted launch can ever link this collection; couriers can never go on duty (setLocked reverts NotGame for the real office) and the only remedy is a new collection and a new mint. The renounce guard does not help: game != 0 is satisfied by the wrong address. The one-shot gives no protection while an owner exists (the owner is trusted until renounce anyway), so a minimal fix within the design is to allow setGame to be re-set until ownership is renounced, or at least to require `game_.code.length > 0` and `PostOffice(game_).couriers() == this`. Reported by the flow specialist.

**Reproduction**

State: stage 1 done, revealed. Owner calls nft.setGame(0xEOA) by mistake. Then nft.setGame(realOffice): expected a way to point the NFT at the real office before renouncing; actual: revert GameAlreadySet, game stays 0xEOA. vm.prank(realOffice); nft.setLocked(1, true) reverts NotGame, so office.assign(tokenId) can never succeed; nft.freezeRenderer(); nft.renounceOwnership() still succeed (seed != 0, game != 0, frozen). Checked locally (test_SetGameWrongAddressIsFinal).

---

Judge's submission `126726f34a15ad2f299330a86b88e08c070924b1d64be5854adcf10e35fe1d4d`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
