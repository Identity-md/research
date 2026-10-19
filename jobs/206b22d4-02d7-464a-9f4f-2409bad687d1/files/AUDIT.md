# Audit report

> Audit the contracts in AdamNakamoto/delivermail as they are.

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/delivermail.git |
| Commit | `3dad38cc3c9f89bee7fd740a7fa0a0984ecd93af` |
| Job | `206b22d4-02d7-464a-9f4f-2409bad687d1` |
| Judged | 2026-10-19 20:12 UTC |
| Findings | 1 medium · 2 low · 1 info |

Four agents audited the code as it is at `3dad38c`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Revoke window is attacker-timed: a root posted in the last second of a reward day is claimable one second later

`p2e/contracts/src/DeliveryRewards.sol:197`

```
        if (currentDay() <= postedOn[day]) revert NotOpenYet();
```

The fix for re-check finding 2 is supposed to give the owner time to revoke a bad root, especially one posted with a leaked poster key. The audit request says claims open 'the reward day after a root is posted (so the owner can always revoke a bad root first)'. postRoot records postedOn[day] = currentDay() (line 136), and _settle only requires currentDay() > postedOn[day]. So the window lasts until the next reward-day boundary, not for one full reward day. Whoever posts the root picks the timing. A leaked poster key can post at startTime + (N+1)*dayLength - 1, and the leaf accounts can claimNow one second later. Once one leaf is claimed, revokeRoot reverts AlreadyClaimedFrom, so the owner has no practical chance to react. The attacker can do this for every closed day that has no root yet, up to dailyBudget(day) per day (about 164,706 MAIL in era 0). The literal wording of AUDIT.md guarantee 7 ('for the rest of the day it was posted') still holds. The mitigation it promises does not hold in the leaked-key case it was built for. The precondition is a compromised poster key, which is the exact threat this control exists to handle. Fix, keeping the design: also store postedAt[day] = block.timestamp in postRoot, require block.timestamp >= postedAt[day] + dayLength in _settle, and make claimableFrom report the same time.

**Reproduction**

Setup: MailToken plus DeliveryRewards(dayLength 86400, initialDaily 16.8M/102, halving 51), with setMinter(rewards). Warp to startTime + 2*86400 - 1, the last second of day 1. The poster calls postRoot(0, leaf(alice,0,DAILY), DAILY), which sets postedOn[0] = 1. Warp forward 1 second, to day 2. Alice calls claimNow(0, DAILY, []). Expected: revert NotOpenYet, with the owner still able to revoke. Actual: the call succeeds 1 second after posting, alice is minted 80% of DAILY, 20% is burned, and revokeRoot(0) now reverts AlreadyClaimedFrom. The attached proof fails on this code with 'next call did not revert as expected' (run by this reviewer).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {MailToken} from "src/MailToken.sol";
import {DeliveryRewards} from "src/DeliveryRewards.sol";

/// The revoke window (AUDIT.md guarantee 7: "every root can be revoked for the rest of the day it was posted")
/// can be shrunk to one second: a root posted one second before a reward-day boundary is claimable one second later.
contract RevokeWindowTest is Test {
    MailToken mail;
    DeliveryRewards rewards;
    address owner = makeAddr("owner");
    address poster = makeAddr("poster");
    address alice = makeAddr("alice");
    uint256 constant DAY = 86_400;
    uint256 constant DAILY = uint256(16_800_000e18) / 102;

    function setUp() public {
        vm.warp(1_800_000_000);
        mail = new MailToken(makeAddr("liquidity"), owner);
        rewards = new DeliveryRewards(mail, owner, poster, DAY, DAILY, 51);
        vm.prank(owner);
        mail.setMinter(address(rewards));
    }

    function test_RootPostedOneSecondBeforeMidnightIsClaimableOneSecondLater() public {
        uint256 start = rewards.startTime();
        // Day 0 has closed; we are at the last second of day 1.
        vm.warp(start + 2 * DAY - 1);
        assertEq(rewards.currentDay(), 1);
        bytes32 root = rewards.leaf(alice, 0, DAILY); // one-leaf tree
        vm.prank(poster);
        rewards.postRoot(0, root, DAILY);

        // One second later the owner's revoke window is gone: the claim goes through.
        vm.warp(start + 2 * DAY);
        assertEq(block.timestamp - start - DAY - (DAY - 1), 1, "one second after posting");
        vm.prank(alice);
        // Expected (a guaranteed revoke window of at least one reward day): still NotOpenYet.
        vm.expectRevert(DeliveryRewards.NotOpenYet.selector);
        rewards.claimNow(0, DAILY, new bytes32[](0));
        assertEq(mail.balanceOf(alice), 0, "nothing minted from a root posted one second ago");
    }
}
```

### 2. Low: Claim flags are keyed by root only, so one root posted for two days lets the first claim block the second

`p2e/contracts/src/DeliveryRewards.sol:198`

```
        if (_claimedFor[d.root][account]) revert AlreadyClaimed();
```

_settle reads and writes _claimedFor[d.root][account], and the day is not part of the key. postRoot accepts the same non-zero root for any number of days, each with its own total. Leaves encode the day, so one tree can legitimately hold an account's allocations for several days. If such a root is posted for days 0 and 1, the account's first claim sets the flag for the root, and its claim for the other day reverts AlreadyClaimed. That day's total stays unclaimed. The only recovery is for the owner to revoke the day, which is possible only while nothing has been claimed from it, and to re-post a different root. The precondition is a poster that batches days into one tree. The server builds one tree per day today. Fix: key the flag by day too, as mapping(uint256 day => mapping(bytes32 root => mapping(address => bool))), and update claimed() to match. This keeps the clean slate after a revoke that audit finding 2 asked for.

**Reproduction**

Build a two-leaf tree with leaf(alice,0,100e18) and leaf(alice,1,100e18), giving root R. At day 2 the poster calls postRoot(0,R,100e18) and postRoot(1,R,100e18); both are accepted. Warp to maturesAt(1). claim(alice,0,100e18,[leaf1]) mints 100e18. Then claim(alice,1,100e18,[leaf0]). Expected: another 100e18 minted. Actual: revert AlreadyClaimed(), and days_(1).claimed stays 0. The attached proof fails on this code with AlreadyClaimed() (run by this reviewer).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {MailToken} from "src/MailToken.sol";
import {DeliveryRewards} from "src/DeliveryRewards.sol";

/// Claim flags are keyed by root alone (`_claimedFor[root][account]`), not by (day, root). One Merkle tree that
/// holds an account's leaves for two different days has one root; posted for both days, the account's first
/// claim marks the flag for the root and the second day's claim reverts AlreadyClaimed.
contract RootReuseAcrossDaysTest is Test {
    MailToken mail;
    DeliveryRewards rewards;
    address alice = makeAddr("alice");

    function setUp() public {
        vm.warp(1_800_000_000);
        mail = new MailToken(makeAddr("pool"), address(this));
        rewards = new DeliveryRewards(mail, address(this), address(this), 1 days, 1_000e18, 51);
        mail.setMinter(address(rewards));
    }

    function test_SameRootForTwoDaysBlocksTheSecondClaim() public {
        uint256 amount = 100e18;
        bytes32 l0 = rewards.leaf(alice, 0, amount);
        bytes32 l1 = rewards.leaf(alice, 1, amount);
        bytes32 root = l0 < l1 ? keccak256(abi.encode(l0, l1)) : keccak256(abi.encode(l1, l0));

        vm.warp(block.timestamp + 2 days); // days 0 and 1 are closed
        rewards.postRoot(0, root, amount);
        rewards.postRoot(1, root, amount);

        vm.warp(rewards.maturesAt(1)); // both days matured and open for claims

        bytes32[] memory p0 = new bytes32[](1);
        p0[0] = l1;
        rewards.claim(alice, 0, amount, p0);
        assertEq(mail.balanceOf(alice), amount);

        // Expected: day 1 is a different day with its own posted total, so its proven leaf pays.
        // Actual: reverts AlreadyClaimed, because the flag is shared by every day that uses this root.
        bytes32[] memory p1 = new bytes32[](1);
        p1[0] = l0;
        rewards.claim(alice, 1, amount, p1);
        assertEq(mail.balanceOf(alice), 2 * amount);
        (, uint256 total1, uint256 claimed1) = rewards.days_(1);
        assertEq(claimed1, total1);
    }
}
```

### 3. Low: Once-per-reward-day Messenger rule resets when MessengerNFT.office is changed, because the history is stored per office

`p2e/contracts/src/MailOffice.sol:165`

```
        if (lastAssignedDay[id] == dayPlusOne && lastWalletOf[id] != msg.sender) revert TooSoon();
```

Guarantee 8 says a Messenger plays for at most one wallet per reward day. The history that enforces it (lastAssignedDay, lastWalletOf) lives in each MailOffice instance, not on the token. When the NFT owner points MessengerNFT.office at a new MailOffice (the supported migration; re-check finding 8 keeps the old office able to unlock), the new office starts with empty history. On the migration day, a Messenger already played for wallet A at the old office can be unassigned, transferred and assigned to wallet B at the new office. The old office would reject this with TooSoon. One NFT then earns full stamina for two wallets that day. The precondition is an owner migration, and the effect is limited to that day. Fix: keep the per-token day and wallet history on MessengerNFT (for example, record them in setLocked, with the office passing the day), or have the new office consult a previousOffice's lastAssignedDay and lastWalletOf.

**Reproduction**

Alice and bob each open at office1 for 0.005 ETH. Alice owns Messenger #1 and calls office1.assign(1) on reward day 0. The owner deploys office2 and calls nft.setOffice(office2), and bob opens at office2. Alice calls office1.unassign() and transferFrom(alice,bob,1). bob's office1.assign(1) reverts TooSoon, as expected. bob's office2.assign(1) on the same day 0 should also revert TooSoon. Actual: it succeeds. The attached test fails on this code with 'next call did not revert as expected' at office2.assign (checked against the trace).

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

contract MigrationTest is Test {
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address poster = makeAddr("poster");
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");
    MailToken mail;
    MessengerNFT nft;
    DeliveryRewards rewards;
    MailOffice office1;
    MailOffice office2;

    function setUp() public {
        vm.startPrank(owner);
        mail = new MailToken(makeAddr("liquidity"), owner);
        nft = new MessengerNFT(owner, treasury, makeAddr("dev"), 0.01 ether, keccak256(abi.encode(bytes32("s"))), address(new DevTransferValidator()), "ipfs://m/");
        rewards = new DeliveryRewards(mail, owner, poster, 1 days, uint256(16_800_000e18) / 102, 51);
        office1 = new MailOffice(mail, nft, IRewardDay(address(rewards)), treasury, owner);
        office2 = new MailOffice(mail, nft, IRewardDay(address(rewards)), treasury, owner);
        mail.setMinter(address(rewards));
        nft.setOffice(address(office1));
        nft.ownerMint(alice, 1);
        vm.stopPrank();
        vm.deal(alice, 1 ether);
        vm.deal(bob, 1 ether);
    }

    function test_OfficeChangeResetsOncePerRewardDay() public {
        uint256 id = 1;
        assertEq(office1.openPrice(), 0.005 ether);
        assertEq(nft.ownerOf(id), alice);
        vm.prank(alice);
        office1.open{value: 0.005 ether}(address(0));
        vm.prank(bob);
        office1.open{value: 0.005 ether}(address(0));
        vm.prank(alice);
        office1.assign(id); // day 0: plays for alice

        vm.prank(owner);
        nft.setOffice(address(office2));
        vm.prank(bob);
        office2.open{value: 0.005 ether}(address(0));

        vm.startPrank(alice);
        office1.unassign();
        nft.transferFrom(alice, bob, id);
        vm.stopPrank();

        vm.prank(bob);
        vm.expectRevert(MailOffice.TooSoon.selector);
        office1.assign(id);

        assertEq(rewards.currentDay(), 0);
        // Same reward day, second wallet: guarantee 8 says TooSoon.
        vm.prank(bob);
        vm.expectRevert(MailOffice.TooSoon.selector);
        office2.assign(id);
    }
}
```

### 4. Info: Guarantee 17 ('hook ETH claims always equal pendingProtocolFees') fails: anyone can add ERC-6909 claims to the hook, and the excess is stranded

`p2e/contracts/src/MailHook.sol:313`

```
        poolManager.burn(address(this), Currency.wrap(quote).toId(), amount);
```

Two specialist findings are merged here: one used PoolManager.mint(hook,...) and the other used ERC-6909 transfer to the hook. Both are the same mechanism. Any party can credit ERC-6909 ETH claims to the hook, either by calling poolManager.mint(hook, 0, x) inside its own unlock or by calling poolManager.transfer(hook, 0, x). _collect burns and takes only pendingProtocolFees, and collectProtocolFees returns early when that is 0. No path ever burns the surplus, and the hook is renounced. Only the donor loses value; fee collection and user funds are not affected. The stated invariant is still false, and the stray value cannot be recovered. Fix: either restate the invariant as claims >= pendingProtocolFees, or have _collect burn and take poolManager.balanceOf(address(this), id) and pay it to feeRecipient.

**Reproduction**

After openPool, a Donor contract calls poolManager.unlock. In unlockCallback it calls poolManager.mint(hook, 0, 1) and then poolManager.settle{value: 1}(). Expected per guarantee 17: poolManager.balanceOf(hook,0) == hook.pendingProtocolFees(address(0)). Actual: 1 != 0, and collectProtocolFees(address(0)) returns without moving the 1 wei. The attached test fails on this code with 'assertion failed: 1 != 0'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {IUnlockCallback} from "v4-core/src/interfaces/callback/IUnlockCallback.sol";
import {MailHook} from "src/MailHook.sol";
import {MailToken} from "src/MailToken.sol";
import {DeployLib} from "script/DeployLib.sol";

contract Donor is IUnlockCallback {
    IPoolManager pm;
    address hook;
    constructor(IPoolManager pm_, address hook_) { pm = pm_; hook = hook_; }
    function go() external payable { pm.unlock(""); }
    function unlockCallback(bytes calldata) external returns (bytes memory) {
        pm.mint(hook, 0, 1);
        pm.settle{value: 1}();
        return "";
    }
}

contract ClaimsTest is Test {
    PoolManager pm;
    MailHook hook;
    MailToken mail;
    address owner = makeAddr("owner");
    address feeRecipient = makeAddr("feeRecipient");

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        bytes memory initCode = abi.encodePacked(
            type(MailHook).creationCode,
            abi.encode(pm, owner, feeRecipient, DeployLib.startTickForMarketCap(20 ether, 21_000_000e18), uint256(4_200_000e18))
        );
        (bytes32 salt, address expected) = DeployLib.mineSalt(address(this), uint160(0x28CC), initCode, 0);
        address h;
        assembly { h := create2(0, add(initCode, 0x20), mload(initCode), salt) }
        require(h == expected, "hook address");
        hook = MailHook(h);
        mail = new MailToken(address(hook), owner);
        vm.prank(owner);
        hook.openPool(address(mail));
    }

    function test_DonatedClaimsBreakInvariant() public {
        Donor d = new Donor(pm, address(hook));
        d.go{value: 1}();
        // Guarantee 17: the hook's ETH claims always equal pendingProtocolFees.
        assertEq(pm.balanceOf(address(hook), 0), hook.pendingProtocolFees(address(0)));
    }
}
```

---

Judge's submission `1b020f612ddeeb59baf6a83f29d468c52c38997c99a804f9d914c6703f87e3c1`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
