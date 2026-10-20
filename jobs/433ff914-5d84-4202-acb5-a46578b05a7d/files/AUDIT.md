# Audit report

> Audit the contracts in AdamNakamoto/delivermail as they are.

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/delivermail.git |
| Commit | `d5eeb4e003f05ce93d19e4eb2d3e46c6d97a19b0` |
| Job | `433ff914-5d84-4202-acb5-a46578b05a7d` |
| Judged | 2026-10-20 03:31 UTC |
| Findings | 3 low · 1 info |

Four agents audited the code as it is at `d5eeb4e`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: raiseLevel authorises against the current office only, while unlock honours lockedBy: after setOffice the old office can unassign a Messenger it holds but can no longer level it

`p2e/contracts/src/MessengerNFT.sol:260`

```
        if (msg.sender != office) revert NotOffice();
```

MessengerNFT.setLocked(id, false, ...) authorises the unlock against lockedBy[id] (line 250), which is what lets a Messenger locked by an old office keep working there after the owner calls setOffice(newOffice) (AUDIT.md guarantee 9, IMD finding 8). Its paired game hook raiseLevel (line 260) was not mirrored: it authorises against the current `office` only. After a migration the Messenger is still assigned at the old office (MailOffice.assignedBy[id] == holder), the new office refuses it (setLocked(true) reverts AlreadyLocked), so the old office is the only office allowed to touch it, yet MailOffice.levelUp there reverts NotOffice() at the raiseLevel call. The holder must unassign at the old office and re-assign at the new one before any level can be bought; a pending levelUp transaction sent before the migration reverts. No MAIL is lost (the whole levelUp reverts, so _spend is undone) and no unauthorised actor gains anything, so this is a low: an access asymmetry between the two writers of a locked Messenger's game state, which AUDIT.md describes as one trust surface. Fix: authorise raiseLevel against the office that holds the lock, `if (msg.sender != lockedBy[id]) revert NotOffice();`. This keeps the agreed design (only an office levels, only through MailOffice.levelUp, which already requires assignedBy[id] == msg.sender). If levelling unassigned Messengers by the current office is wanted, use `msg.sender != office && msg.sender != lockedBy[id]` instead. Reported by the permissions specialist; reproduced here.

**Reproduction**

State: nft.office == office1; alice opened office1 (open{value: 0.005 ether}), assigned Messenger 1 there (nft.locked(1) == true, nft.lockedBy(1) == office1, office1.assignedBy(1) == alice), approved office1 for MAIL and holds 10,000 MAIL; office1.levelUp(1, type(uint256).max) succeeded once (level 1). Then owner calls nft.setOffice(office2). Input: alice calls office1.levelUp(1, type(uint256).max). Expected: level 1 -> 2 (same call succeeded one transaction earlier; office2.assign(1) reverts AlreadyLocked and office1.unassign() succeeds, so office1 is the only office the NFT lets act on it). Actual: reverts NotOffice() from MessengerNFT.raiseLevel line 260 because msg.sender (office1) != office (office2). Verified: the attached test fails with NotOffice() on the current code (forge test --match-path test/scratch/Proof_5f2633d3ca08.t.sol).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {MailToken} from "src/MailToken.sol";
import {MessengerNFT} from "src/MessengerNFT.sol";
import {MailOffice, IRewardDay} from "src/MailOffice.sol";
import {DeliveryRewards} from "src/DeliveryRewards.sol";
import {DevTransferValidator} from "src/DevTransferValidator.sol";

/// Asymmetry between MessengerNFT.setLocked (unlock honours `lockedBy[id]`, so the office that locked a Messenger
/// keeps working after `setOffice`) and MessengerNFT.raiseLevel (honours only the current `office`). After a
/// migration the holder of a Messenger still locked by the old office can unassign there but cannot level it there,
/// although the old office is the only one that may touch it (the new office reverts AlreadyLocked on assign).
contract OfficeMigrationLevelUpTest is Test {
    uint256 constant DAILY = uint256(16_800_000e18) / 102;
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address poster = makeAddr("poster");
    address alice = makeAddr("alice");

    MailToken mail;
    MessengerNFT nft;
    DeliveryRewards rewards;
    MailOffice office1;
    MailOffice office2;

    function setUp() public {
        vm.startPrank(owner);
        mail = new MailToken(makeAddr("liquidity"), owner);
        nft = new MessengerNFT(
            owner, treasury, makeAddr("dev"), 0.01 ether, bytes32(uint256(1)), address(new DevTransferValidator()), ""
        );
        rewards = new DeliveryRewards(mail, owner, poster, 1 days, DAILY, 51);
        office1 = new MailOffice(mail, nft, IRewardDay(address(rewards)), treasury, owner);
        office2 = new MailOffice(mail, nft, IRewardDay(address(rewards)), treasury, owner);
        mail.setMinter(address(rewards));
        nft.setOffice(address(office1));
        nft.ownerMint(alice, 1);
        vm.stopPrank();
        vm.deal(alice, 1 ether);
        vm.prank(address(rewards));
        mail.mint(alice, 10_000e18);
    }

    function test_OldOfficeCanUnlockButNotLevelAfterMigration() public {
        vm.startPrank(alice);
        office1.open{value: 0.005 ether}(address(0));
        office1.assign(1);
        mail.approve(address(office1), type(uint256).max);
        office1.levelUp(1, type(uint256).max); // works before the migration
        vm.stopPrank();
        assertEq(nft.levelOf(1), 1);
        assertEq(nft.lockedBy(1), address(office1));

        vm.prank(owner);
        nft.setOffice(address(office2));

        // The Messenger is still locked by office1 and assigned to alice there; office2 can't take it.
        vm.startPrank(alice);
        office2.open{value: 0.005 ether}(address(0));
        vm.expectRevert(MessengerNFT.AlreadyLocked.selector);
        office2.assign(1);

        // Same wallet, same assignment, same approval: the level-up that worked a moment ago now reverts, while
        // the mirror operation (unassign through the same office) is still accepted by the NFT.
        office1.levelUp(1, type(uint256).max);
        vm.stopPrank();
        assertEq(nft.levelOf(1), 2, "the office holding the lock can still level its Messenger");
    }
}
```

### 2. Low: Batched claims are all-or-nothing: one already-claimed day, which anyone can trigger after maturity, reverts the account's whole claimMany/claimNowMany

`p2e/contracts/src/DeliveryRewards.sol:196`

```
        for (uint256 i; i < dayList.length; ++i) claimNow(dayList[i], amounts[i], proofs[i]);
```

claimMany (line 172) and claimNowMany (line 196) loop over the public single-day functions and revert as a whole if any entry fails in _settle (AlreadyClaimed at line 204, OverTotal at line 206). Because claim(account, ...) is open to anyone once a day has matured (lines 158-164), a third party can settle one of the days in an account's pending batch (the tokens go to the account, so this costs the griefer only gas) and the account's claimNowMany / claimMany transaction then reverts with AlreadyClaimed, delivering nothing for the other days in the batch. The same happens when the batch includes a day whose total was exhausted by earlier claimants (OverTotal). There is no partial-success path, so a wallet claiming several days at once must detect the failure off-chain and resubmit without the offending day, and a griefer can repeat this each time a new matured day is included; a relayer paying gas for players loses the gas of every reverted batch. No funds are lost. Fix: in claimMany/claimNowMany skip days whose flag _claimedFor[day][days_[day].root][account] is already set (continue instead of revert), keeping the single-day functions strict. Reported by the economics specialist; reproduced here.

**Reproduction**

State: DeliveryRewards(dayLength 1 days, initialDaily 164_705e18, halving 51); poster posts day 0 with a two-leaf tree containing (A, 0, 100e18) and day 1 with one containing (A, 1, 100e18), both at startTime + 2 days; warp to maturesAt(1) (past both claimableFrom values). Inputs: (1) relayer R calls claim(A, 0, 100e18, proof0): succeeds, A receives 100e18. (2) A calls claimNowMany([0,1], [100e18,100e18], [proof0,proof1]). Expected (a batch entry point usable for several days): A is paid day 1 (balance 200e18) and day 0 is skipped as already claimed. Actual: the call reverts with AlreadyClaimed() from _settle on day 0; A receives nothing for day 1 in that transaction. Same revert with claimMany(A, [0,1], ...). Verified: the attached test fails with AlreadyClaimed() on the current code (forge test --match-path test/scratch/Proof_5b3226fce876.t.sol).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {MailToken} from "src/MailToken.sol";
import {DeliveryRewards} from "src/DeliveryRewards.sol";

/// A third party settles one matured day of A's batch with `claim`; A's `claimNowMany` for [0,1] then reverts
/// as a whole and pays nothing for day 1.
contract BatchClaimTest is Test {
    MailToken mail;
    DeliveryRewards rewards;
    address owner = address(0xA11CE);
    address poster = address(0xB0B);
    address A = address(0xAAAA);
    address relayer = address(0xCAFE);

    function setUp() public {
        mail = new MailToken(address(0xDEAD), address(this));
        rewards = new DeliveryRewards(mail, owner, poster, 1 days, 164_705e18, 51);
        mail.setMinter(address(rewards));
    }

    function _leaf(address a, uint256 day, uint256 amt) internal pure returns (bytes32) {
        return keccak256(bytes.concat(keccak256(abi.encode(a, day, amt))));
    }

    function _hash(bytes32 x, bytes32 y) internal pure returns (bytes32) {
        return x < y ? keccak256(abi.encodePacked(x, y)) : keccak256(abi.encodePacked(y, x));
    }

    function test_batchClaimSurvivesAThirdPartySingleClaim() public {
        // two-leaf trees per day: A and a filler account
        bytes32 l0 = _leaf(A, 0, 100e18);
        bytes32 f0 = _leaf(address(0xF111), 0, 1e18);
        bytes32 root0 = _hash(l0, f0);
        bytes32 l1 = _leaf(A, 1, 100e18);
        bytes32 f1 = _leaf(address(0xF111), 1, 1e18);
        bytes32 root1 = _hash(l1, f1);

        vm.warp(rewards.startTime() + 2 days);
        vm.startPrank(poster);
        rewards.postRoot(0, root0, 101e18);
        rewards.postRoot(1, root1, 101e18);
        vm.stopPrank();

        vm.warp(rewards.maturesAt(1));

        bytes32[] memory p0 = new bytes32[](1);
        p0[0] = f0;
        bytes32[] memory p1 = new bytes32[](1);
        p1[0] = f1;

        // anyone settles day 0 for A
        vm.prank(relayer);
        rewards.claim(A, 0, 100e18, p0);
        assertEq(mail.balanceOf(A), 100e18);

        uint256[] memory dayList = new uint256[](2);
        dayList[0] = 0;
        dayList[1] = 1;
        uint256[] memory amounts = new uint256[](2);
        amounts[0] = 100e18;
        amounts[1] = 100e18;
        bytes32[][] memory proofs = new bytes32[][](2);
        proofs[0] = p0;
        proofs[1] = p1;

        // Expected: day 1 is paid (day 0 skipped). Actual on current code: the whole batch reverts.
        vm.prank(A);
        rewards.claimNowMany(dayList, amounts, proofs);
        assertEq(mail.balanceOf(A), 200e18, "day 1 was not paid by the batch");
    }
}
```

### 3. Low: setFeeRecipient is one-step after the renounce: one wrong address strands every future 4% fee with no recovery path

`p2e/contracts/src/MailHook.sol:355`

```
        if (msg.sender != owner && msg.sender != feeRecipient) revert NotOwner();
```

MailHook is renounced at deploy (Deploy.s.sol line 107), after which the only party able to redirect the pool's fees is the current feeRecipient, through a one-step setter (line 354-359). Ownership of the same contract is deliberately two-step ('so a typo can't lose the admin role', line 361), but the fee recipient, the only privileged role left after launch, has no such protection. If the recipient names an address that cannot itself call setFeeRecipient (the hook itself, a plain vault or splitter contract, a mistyped EOA whose key nobody holds), then every future swap still mints 4% into the hook's ETH claims, _collect pays only feeRecipient so collection either reverts forever (no receive) or pays an address nobody controls, and owner is address(0), so nobody can repoint it. The 4% of all future trading volume is lost or frozen permanently. AUDIT.md's accepted limit ('a fee recipient that can't receive ETH ... can point its fees at another address') assumes the recipient can still act, which is exactly what one wrong call removes. Fix that preserves the design (renounced hook, only the recipient moves its own fees): make the change two-step, pendingFeeRecipient set by the current recipient and acceptFeeRecipient callable only by the pending address, so the new recipient proves it can act before it becomes the only key to the fees. Reported by the flow specialist; reproduced here.

**Reproduction**

State: PoolManager, MailHook at a mined 0x28EC address with owner, feeRecipient, 4.2M launch supply; MailToken minted to the hook; owner calls openPool(mail) then renounceOwnership() (as Deploy.s.sol does). 1) feeRecipient calls hook.setFeeRecipient(address(hook)). 2) alice calls router.buy{value: 1 ether}(mail, 1, block.timestamp): pendingProtocolFees(address(0)) == 0.04 ether. 3) anyone calls hook.collectProtocolFees(address(0)). Expected: the fee reaches an address somebody controls. Actual: reverts inside PoolManager.take (the hook has no receive; NativeTransferFailed wrapped by the unlock), and the 0.04 ETH stays in the hook's claims. 4) the old feeRecipient calls hook.setFeeRecipient(feeRecipient). Expected: a way back. Actual: reverts NotOwner(), and hook.owner() == address(0) so no one else can either. 5) a second 1 ether buy raises pendingProtocolFees to 0.08 ether, all stranded. Verified with test/scratch/FeeRecipient.t.sol (passes: the stranding state is reachable) and the attached test, which fails on the current code at step 3.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {MailHook} from "src/MailHook.sol";
import {MailRouter} from "src/MailRouter.sol";
import {MailToken} from "src/MailToken.sol";
import {DeployLib} from "script/DeployLib.sol";

/// After the renounce (done at deploy), setFeeRecipient is one-step. One call naming an address that cannot call
/// setFeeRecipient back (here: the hook itself, which has no receive) strands every future 4% fee: collection
/// reverts, the old recipient is no longer allowed to repoint, and owner is address(0).
/// Fails on the current code (collectProtocolFees reverts). Passes once the change is two-step (the recipient stays
/// `feeRecipient` until the new address accepts), because collection then still pays the controllable address.
contract FeeRecipientProofTest is Test {
    PoolManager pm;
    MailHook hook;
    MailToken mail;
    MailRouter router;

    address owner = makeAddr("owner");
    address feeRecipient = makeAddr("feeRecipient");
    address alice = makeAddr("alice");
    address constant ETH = address(0);
    uint256 constant LAUNCH = 4_200_000e18;

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        bytes memory initCode = abi.encodePacked(
            type(MailHook).creationCode,
            abi.encode(pm, owner, feeRecipient, DeployLib.startTickForMarketCap(20 ether, 21_000_000e18), LAUNCH)
        );
        (bytes32 salt, address expected) = DeployLib.mineSalt(address(this), uint160(0x28EC), initCode, 0);
        address h;
        assembly {
            h := create2(0, add(initCode, 0x20), mload(initCode), salt)
        }
        require(h == expected, "hook address");
        hook = MailHook(h);
        router = MailRouter(payable(hook.router()));
        mail = new MailToken(address(hook), owner);
        vm.startPrank(owner);
        hook.openPool(address(mail));
        hook.renounceOwnership(); // as Deploy.s.sol does
        vm.stopPrank();
        vm.deal(alice, 10 ether);
    }

    function test_MistakenFeeRecipientDoesNotStrandTheFees() public {
        // The recipient names an address that can never call setFeeRecipient (the hook has no receive either).
        vm.prank(feeRecipient);
        hook.setFeeRecipient(address(hook));

        vm.prank(alice);
        router.buy{value: 1 ether}(address(mail), 1, block.timestamp);
        assertEq(hook.pendingProtocolFees(ETH), 0.04 ether);

        // Expected: the fees are still collectable to an address somebody controls.
        // Actual on the current code: reverts (the hook cannot receive ETH), and nobody can repoint the recipient.
        hook.collectProtocolFees(ETH);
        assertEq(feeRecipient.balance, 0.04 ether, "fees reached a controllable address");
    }
}
```

### 4. Info: The one-character rule is per office contract: after setOffice a wallet can hold two locked, assigned Messengers, one in each office

`p2e/contracts/src/MailOffice.sol:157`

```
        if (characterOf[msg.sender] != 0) revert HasCharacter();
```

IMD re-check 206b22d4 finding 3 moved the once-per-reward-day record (lastPlayedDay, lastPlayer) onto MessengerNFT so that setOffice cannot reset it. The one-character-per-wallet rule (AUDIT.md guarantee 8: 'at most one Messenger assigned (characterOf)') was not moved: characterOf (checked at line 157) and assignedBy are still per MailOffice instance, and MessengerNFT.setLocked(true) checks nothing about the player's other locked Messengers. After the owner points the NFT at a new office, a wallet whose Messenger is still locked by the old office can open the new office and assign a second Messenger there. Both offices then report the wallet as playing a Messenger with full stamina, both tokens are locked, and lastPlayer of both is the same wallet. Whether this yields extra points depends on which office the game server reads (out of scope); on chain the guarantee as stated no longer holds across a migration, any consumer reading the old office sees two active characters for one wallet, and the holder cannot sell the first Messenger until they unassign it at the old office. Informational: it needs the owner's documented migration action, and the server is the economic guard. Fixes that keep the design: keep the wallet -> locked Messenger record on the NFT (mapping(address => uint256) characterOf written in setLocked, with setLocked(true) reverting when the player already holds a locked Messenger), or have MailOffice.assign refuse wallets that still have a character at the previous office. Reported by both the permissions and the flow specialists (merged); reproduced here.

**Reproduction**

State: nft.office == office1; alice holds Messengers 1 and 2. 1) alice: office1.open{value: 0.005 ether}(address(0)); office1.assign(1) (nft.locked(1) == true, nft.lockedBy(1) == office1). 2) owner: nft.setOffice(address(office2)), office2 a fresh MailOffice on the same token, NFT and clock. 3) alice: office2.open{value: 0.005 ether}(address(0)); office2.assign(2). Expected under guarantee 8: step 3 reverts (HasCharacter or AlreadyLocked) while the wallet still has a character. Actual: it succeeds; office1.characterOf(alice) == 1, office2.characterOf(alice) == 2, nft.locked(1) && nft.locked(2), nft.lastPlayer(1) == nft.lastPlayer(2) == alice, office1.staminaOf(alice) == 12 and office2.staminaOf(alice) == 12 (test/scratch/TwoCharacters.t.sol::test_StateAfterSecondAssign passes). The attached test, which expects the second assign to revert, fails on the current code.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {MailToken} from "src/MailToken.sol";
import {MessengerNFT} from "src/MessengerNFT.sol";
import {MailOffice, IRewardDay} from "src/MailOffice.sol";
import {DeliveryRewards} from "src/DeliveryRewards.sol";
import {DevTransferValidator} from "src/DevTransferValidator.sol";

/// The one-character-per-wallet rule lives in each MailOffice (characterOf), while the lock lives on the NFT.
/// After setOffice, a wallet whose Messenger is still locked by the old office can assign a second one at the new
/// office: two locked, assigned Messengers for one wallet. Fails on the current code (the second assign succeeds);
/// passes once the NFT (or the new office) refuses a wallet that already plays a locked Messenger.
contract TwoCharactersProofTest is Test {
    uint256 constant DAILY = uint256(16_800_000e18) / 102;
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address poster = makeAddr("poster");
    address alice = makeAddr("alice");

    MailToken mail;
    MessengerNFT nft;
    DeliveryRewards rewards;
    MailOffice office1;
    MailOffice office2;

    function setUp() public {
        vm.startPrank(owner);
        mail = new MailToken(makeAddr("liquidity"), owner);
        nft = new MessengerNFT(
            owner, treasury, makeAddr("dev"), 0.01 ether, bytes32(uint256(1)), address(new DevTransferValidator()), ""
        );
        rewards = new DeliveryRewards(mail, owner, poster, 1 days, DAILY, 51);
        office1 = new MailOffice(mail, nft, IRewardDay(address(rewards)), treasury, owner);
        office2 = new MailOffice(mail, nft, IRewardDay(address(rewards)), treasury, owner);
        mail.setMinter(address(rewards));
        nft.setOffice(address(office1));
        nft.ownerMint(alice, 2);
        vm.stopPrank();
        vm.deal(alice, 1 ether);
    }

    function test_OneWalletCannotPlayTwoMessengersAcrossOffices() public {
        vm.startPrank(alice);
        office1.open{value: 0.005 ether}(address(0));
        office1.assign(1);
        vm.stopPrank();
        assertTrue(nft.locked(1));

        vm.prank(owner);
        nft.setOffice(address(office2));

        vm.startPrank(alice);
        office2.open{value: 0.005 ether}(address(0));
        // Expected under guarantee 8 (one character per wallet): refused while Messenger 1 is still alice's character.
        // Actual on the current code: succeeds; both offices report alice playing, both tokens are locked.
        vm.expectRevert();
        office2.assign(2);
        vm.stopPrank();
    }
}
```

---

Judge's submission `37598f4972df230248087c2d36acfeb402216dfe6537c1ae31a64ee1830732f4`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
