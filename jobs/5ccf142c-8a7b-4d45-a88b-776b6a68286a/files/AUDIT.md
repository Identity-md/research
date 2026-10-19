# Audit report

> Audit the contracts in AdamNakamoto/delivermail as they are.

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/delivermail.git |
| Commit | `5c2987cc935597a0cfa7e26b7f6dccbdd8019b25` |
| Job | `5ccf142c-8a7b-4d45-a88b-776b6a68286a` |
| Judged | 2026-10-19 15:52 UTC |
| Findings | 1 medium · 3 low · 4 info |

Four agents audited the code as it is at `5c2987c`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: One Messenger NFT plays for two wallets in the same reward day: assign() keys the once-per-day rule on the join day only and unassign() records nothing

`p2e/contracts/src/MailOffice.sol:159`

```
        if (lastAssignedDay[id] == dayPlusOne) revert TooSoon();
```

MailOffice.assign stores lastAssignedDay[id] = currentDay()+1 and rejects a join only when that value equals today's stamp. unassign() deletes characterOf/assignedBy and unlocks the token but never records that the Messenger served a wallet today. A Messenger assigned on day D is wallet A's character through day D+1 (staminaOf(A) returns its full 12 + tier stamina), and when A unassigns during D+1 and transfers it, wallet B's assign(id) sees lastAssignedDay[id] == D+1 != D+2 and succeeds, so B also gets staminaOf(B) == 12 in day D+1. The game server meters paid deliveries per (wallet, day) from profileOf (p2e/server/src/game.js pay: entry.paid < p.stamina + p.apprenticeStamina), so one 12-stamina Messenger backs 24 full-point paid deliveries in one reward day, and alternating the two wallets repeats it every day (confirmed for 5 consecutive days). Each day's budget is split pro rata by points, so every honest player is diluted by the doubled share; the cost to the sybil is one extra office (0.005 ETH) and three transactions a day. This is the hole IMD finding 3 meant to close (contract doc lines 23-25: 'so one NFT can't be passed around to play for several wallets in a day'; AUDIT.md guarantee 8); the fix only moved the window to the join day, and test_F3 covers only the case where A re-assigns on day D+1 (which re-stamps it). Merged from audit_economics b7252a98 and audit_math 1c36ea7c (same mechanism, same line). Fix (verified: both supplied proofs pass and all 39 existing tests still pass): in unassign() write lastAssignedDay[id] = clock.currentDay() + 1, add mapping(uint256 => address) lastWalletOf set in assign(), and relax the check to `if (lastAssignedDay[id] == dayPlusOne && lastWalletOf[id] != msg.sender) revert TooSoon();` so the same wallet may re-assign on the same day (as test_F3 expects) but a different wallet must wait for the next reward day.

**Reproduction**

Setup as test/P2E.t.sol (dayLength 1 day); alice and bob each open an office, alice owns Messenger #1. t = startTime + 12h (day 0): alice.assign(1). t = startTime + 1 day + 12h (day 1): rewards.currentDay() == 1 and office.staminaOf(alice) == 12 (alice is credited the Messenger's stamina for day 1). Then alice.unassign(); nft.transferFrom(alice, bob, 1); bob.assign(1). Expected: revert TooSoon (#1 already served a wallet in reward day 1). Actual: succeeds, office.characterOf(bob) == 1 and office.staminaOf(bob) == 12 in the same reward day. Repeating with roles swapped on days 2..5 succeeds each day. Run: forge test --match-path test/scratch/Proof_b7252a982bea.t.sol (both tests fail on the current code: 'next call did not revert as expected' and 'a second wallet got the Messenger's stamina in the same reward day'; both pass with the fix above).

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

/// One Messenger NFT is the character of two wallets within the same reward day, every day.
/// `assign` only limits how often a Messenger JOINS a wallet per reward day; it ignores that the
/// Messenger was already another wallet's character earlier in that same day (assigned on an
/// earlier day and held across the day boundary). The game server meters paid deliveries per
/// (wallet, day), so each wallet gets the Messenger's full stamina: 24 paid deliveries a day from
/// a 12-stamina Messenger.
contract MessengerDoublePlayTest is Test {
    MailToken mail;
    MessengerNFT nft;
    MailOffice office;
    DeliveryRewards rewards;

    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address liquidity = makeAddr("liquidity");
    address poster = makeAddr("poster");
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");

    uint256 constant DAILY = uint256(16_800_000e18) / 102;

    function setUp() public {
        vm.startPrank(owner);
        mail = new MailToken(liquidity, owner);
        nft = new MessengerNFT(
            owner, treasury, owner, 0.01 ether, keccak256(abi.encode(keccak256("s"))), address(new DevTransferValidator()), "ipfs://m/"
        );
        rewards = new DeliveryRewards(mail, owner, poster, 1 days, DAILY, 51);
        office = new MailOffice(mail, nft, IRewardDay(address(rewards)), treasury, owner);
        mail.setMinter(address(rewards));
        nft.setOffice(address(office));
        nft.ownerMint(alice, 1);
        vm.stopPrank();
        vm.deal(alice, 1 ether);
        vm.deal(bob, 1 ether);
        vm.prank(alice);
        office.open{value: 0.005 ether}(address(0));
        vm.prank(bob);
        office.open{value: 0.005 ether}(address(0));
    }

    /// Day 0: alice assigns. Day 1 (mid-day): alice has already had the Messenger's stamina for day 1,
    /// hands it to bob, and bob assigns it in the same reward day: two wallets, one Messenger, one day.
    function test_OneMessengerIsTwoWalletsCharacterInOneRewardDay() public {
        uint256 t0 = rewards.startTime();
        vm.warp(t0 + 12 hours);
        vm.prank(alice);
        office.assign(1);
        assertEq(office.staminaOf(alice), 12);

        vm.warp(t0 + 1 days + 12 hours); // reward day 1; alice is still playing Messenger #1
        assertEq(rewards.currentDay(), 1);
        assertEq(office.characterOf(alice), 1);
        assertEq(office.staminaOf(alice), 12); // alice's day-1 stamina comes from #1

        vm.startPrank(alice);
        office.unassign();
        nft.transferFrom(alice, bob, 1);
        vm.stopPrank();

        // Expected: #1 already served a wallet in reward day 1, so it can't serve a second one today.
        vm.prank(bob);
        vm.expectRevert();
        office.assign(1);
    }

    /// The pattern repeats indefinitely: every reward day the Messenger serves the wallet that held it
    /// overnight and then a second wallet, so a 12-stamina Messenger backs 24 paid deliveries a day.
    function test_DoublePlayRepeatsEveryDay() public {
        uint256 t0 = rewards.startTime();
        vm.warp(t0 + 12 hours);
        vm.prank(alice);
        office.assign(1);

        address holder = alice;
        address next = bob;
        for (uint256 day = 1; day <= 5; ++day) {
            vm.warp(t0 + day * 1 days + 12 hours);
            // `holder` has had the Messenger's stamina for this reward day.
            assertEq(office.staminaOf(holder), 12);
            vm.startPrank(holder);
            office.unassign();
            nft.transferFrom(holder, next, 1);
            vm.stopPrank();
            vm.prank(next);
            (bool ok,) = address(office).call(abi.encodeCall(MailOffice.assign, (1)));
            // Expected: the second wallet of the day can't take the Messenger's stamina too.
            assertFalse(ok, "a second wallet got the Messenger's stamina in the same reward day");
            if (!ok) return;
            (holder, next) = (next, holder);
        }
    }
}
```

### 2. Low: revokeRoot has no window: a root can be posted and claimed from in the same transaction, so the documented 'withdraw a bad root before anyone has claimed' mitigation can never be relied on

`p2e/contracts/src/DeliveryRewards.sol:130`

```
        if (days_[day].claimed != 0) revert AlreadyClaimedFrom();
```

revokeRoot reverts AlreadyClaimedFrom once days_[day].claimed != 0, and claimNow (line 157) has no delay after postRoot: the only time gate is maturesAt on the full claim, while the early path pays 80% at once. AUDIT.md lists 'revokeRoot before claims' as a mitigation for a wrong or malicious root and the NatSpec says it 'withdraws a bad root before anyone has claimed from it (e.g. a leaked key)', but there is no state in which that holds against an adversary: (a) whoever holds the poster key can drive it from a contract that calls postRoot and then claimNow in one transaction, so 80% of the day's budget (131,764.7 MAIL at launch, per closed day without a root) is minted to the poster's leaf before the owner can act and revokeRoot/postRoot for that day revert AlreadyClaimedFrom/RootExists for good; (b) in the honest case, a root the server posted with a wrong split is locked in by the first over-allocated player who claims in the next block, and the under-allocated players' share of that day is lost. The accepted limit in AUDIT.md ('until the owner pauses and rotates it') assumes a reaction window that does not exist. Merged from audit_economics 38c2a707 and audit_permissions e6ca794d (same mechanism, same line). Fix options, both design changes the requester must decide: record the posting day in Day and have _settle revert while currentDay() <= postedDay (or until a short dispute window has passed), which gives every root at least one reward day in which revokeRoot works (verified: the supplied proof passes, but 4 existing tests that claimNow right after posting then need a one-day warp); or let the owner revoke a root while paused even after claims, subtracting what was already claimed; or drop the claim from the mitigation list and state that a root is final once posted.

**Reproduction**

State: DeliveryRewards with poster = a contract (any leaked EOA key can deploy and drive one), day 0 closed (block.timestamp >= startTime + 1 days). Input: the poster contract calls postRoot(0, leaf(poster, 0, dailyBudget(0)), dailyBudget(0)) and claimNow(0, dailyBudget(0), []) in one transaction. Expected (NatSpec, AUDIT.md): the owner can revokeRoot(0) before any claim and nothing is minted from the bad root. Actual: 131,764.7 MAIL (80% of 164,705.9) is minted to the poster in the posting transaction, 20% burned, and revokeRoot(0) reverts AlreadyClaimedFrom. Honest-poster variant (test/scratch/Judge.t.sol test_RevokeBlockedByImmediateClaim): poster EOA posts a single-leaf root for alice, alice calls claimNow in the same block, then revokeRoot(0) reverts AlreadyClaimedFrom and postRoot(0, ...) reverts RootExists. Run: forge test --match-path test/scratch/Proof_e6ca794da741.t.sol (fails on the current code with AlreadyClaimedFrom()).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {MailToken} from "src/MailToken.sol";
import {DeliveryRewards} from "src/DeliveryRewards.sol";

/// The poster can post a root and claim from it in the same transaction, so there is no moment at which
/// `revokeRoot` ("withdraws a bad root before anyone has claimed from it, e.g. a leaked key") can run.
contract RoguePoster {
    DeliveryRewards immutable rewards;

    constructor(DeliveryRewards r) {
        rewards = r;
    }

    /// Posts a root paying the whole budget to this contract and claims it at once (80% paid, 20% burned).
    function postAndClaim(uint256 day, uint256 total) external {
        bytes32 root = rewards.leaf(address(this), day, total); // single-leaf tree: root == leaf
        rewards.postRoot(day, root, total);
        bytes32[] memory proof = new bytes32[](0);
        // Low-level so the test also passes if the fix makes an immediate claim revert.
        address(rewards).call(abi.encodeWithSelector(DeliveryRewards.claimNow.selector, day, total, proof));
    }
}

contract AtomicPostAndClaimTest is Test {
    MailToken mail;
    DeliveryRewards rewards;
    RoguePoster poster;
    address owner = makeAddr("owner");
    address liquidity = makeAddr("liquidity");
    uint256 constant DAILY = uint256(16_800_000e18) / 102;

    function setUp() public {
        mail = new MailToken(liquidity, owner);
        // The poster key is held by a contract (any leaked EOA key can deploy one and drive it the same way).
        address posterAddr = vm.computeCreateAddress(address(this), vm.getNonce(address(this)) + 1);
        rewards = new DeliveryRewards(mail, owner, posterAddr, 1 days, DAILY, 51);
        poster = new RoguePoster(rewards);
        assertEq(address(poster), posterAddr);
        vm.prank(owner);
        mail.setMinter(address(rewards));
    }

    function test_OwnerCanStillRevokeARootRightAfterItWasPosted() public {
        vm.warp(rewards.startTime() + 1 days + 1); // day 0 has closed
        poster.postAndClaim(0, DAILY);

        // Expected: the owner, reacting to the bad root, can withdraw it and nothing was minted from it.
        // Actual: the claim already went through in the posting transaction and `revokeRoot` reverts
        // AlreadyClaimedFrom; 80% of the day's budget is in the poster's hands.
        vm.prank(owner);
        rewards.revokeRoot(0);
        assertEq(mail.balanceOf(address(poster)), 0, "nothing may be claimed before the owner could react");
    }
}
```

### 3. Low: setSaleOpen(false) on a sale that never opened stamps saleClosedAt, so reveal() passes its 'a sale opened and closed' gate and ends all minting with zero tokens sold

`p2e/contracts/src/MessengerNFT.sol:144`

```
        if (!open) saleClosedAt = block.number;
```

reveal (line 169) treats saleClosedAt != 0 as proof that a sale opened and later closed (comment at line 168: 'saleClosedAt is 0 until a sale has opened and closed'), but setSaleOpen(false) writes saleClosedAt = block.number unconditionally, including when saleOpen is already false and no sale ever opened. One owner call that is a no-op on saleOpen therefore satisfies the gate, and reveal in the next block fixes the seed; after that ownerMint and setSaleOpen(true) revert AlreadyRevealed forever with totalMinted == 0, so none of the 3,333 Messengers can ever be minted and the office/levels economy has no supply. This contradicts AUDIT.md guarantee 13 and is the state the IMD finding-7 fix (RevealTooEarly) was meant to exclude; test_F7_NoRevealBeforeASale only covers reveal with saleClosedAt still 0. Owner-only trigger (a defensive 'close' before launch, or two admin calls in the wrong order), so a bricking footgun rather than an attack path. Merged from audit_flow e29512c6, audit_math dcaf75da and audit_permissions 30c485f0. Fix: stamp the close only when a sale is actually being closed, `if (!open && saleOpen) saleClosedAt = block.number;` evaluated before `saleOpen = open;` (verified: the supplied proof passes and all 39 existing tests still pass); optionally also require totalMinted != 0 in reveal.

**Reproduction**

Fresh MessengerNFT (saleOpen false, saleClosedAt 0, totalMinted 0). Owner calls setSaleOpen(false): actual saleClosedAt == block.number (expected: no-op or revert, the sale was never open). vm.roll(+1). Owner calls reveal(SECRET) with the committed secret. Expected: revert RevealTooEarly (guarantee 13). Actual: succeeds, seed != 0; afterwards setSaleOpen(true) and ownerMint(owner, 1) revert AlreadyRevealed and totalMinted stays 0 forever. Run: forge test --match-path test/scratch/Proof_e29512c6f268.t.sol (fails on the current code with 'next call did not revert as expected'; passes with the one-line guard).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {MessengerNFT} from "src/MessengerNFT.sol";
import {DevTransferValidator} from "src/DevTransferValidator.sol";

/// Guarantee 13 (AUDIT.md): "the reveal needs a sale that opened and closed". The inline comment at
/// MessengerNFT.sol:168 says saleClosedAt is 0 until a sale has opened and closed. Neither holds:
/// setSaleOpen(false) on a sale that was never open stamps saleClosedAt, so reveal() succeeds with
/// no sale ever opened, and from then on nothing can be minted (sale can't reopen, ownerMint reverts).
contract RevealWithoutSaleTest is Test {
    MessengerNFT nft;
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    bytes32 constant SECRET = keccak256("messenger reveal secret");

    function setUp() public {
        vm.prank(owner);
        nft = new MessengerNFT(owner, treasury, makeAddr("dev"), 0.01 ether, keccak256(abi.encode(SECRET)), address(new DevTransferValidator()), "ipfs://m/");
    }

    function test_RevealNeedsASaleThatOpenedAndClosed() public {
        vm.startPrank(owner);
        assertFalse(nft.saleOpen());
        nft.setSaleOpen(false); // the sale was never open; this must not count as "opened and closed"
        vm.roll(block.number + 1);
        // Expected (guarantee 13): RevealTooEarly, since no sale has ever opened.
        // Actual on the current code: reveal succeeds and the collection can never be minted.
        vm.expectRevert(MessengerNFT.RevealTooEarly.selector);
        nft.reveal(SECRET);
        vm.stopPrank();
        assertEq(nft.seed(), 0);
    }
}
```

### 4. Low: Treasury setters (and the MessengerNFT/Wardrobe constructors) accept address(0): withdraw() and mint() then burn ETH to the zero address and every MAIL spend reverts

`p2e/contracts/src/MailOffice.sol:263`

```
        treasury = t;
```

MailOffice's constructor reverts ZeroAddress on a zero treasury (line 86), but MailOffice.setTreasury stores any value, and MessengerNFT.setTreasury (line 153), the MessengerNFT constructor (line 114), Wardrobe.setTreasury (line 82) and the Wardrobe constructor (line 42) check nothing. DeliveryRewards.setPoster (line 192) likewise accepts address(0) although its constructor rejects it, which silently disables postRoot. Consequences once treasury == address(0): (1) MailOffice.withdraw executes address(0).call{value: balance}(''), which succeeds and irrecoverably burns all collected office-opening ETH; MessengerNFT.mint forwards every buyer's msg.value to address(0) and the mint still succeeds, so the public sale's proceeds are burned while buyers receive tokens (guarantee 12 'forwards it to the treasury' not met). (2) MailOffice._spend and Wardrobe.buy call mail.transferFrom(payer, treasury, amount - burnPart), which OpenZeppelin's ERC20 rejects with ERC20InvalidReceiver(address(0)), so every upgrade, levelUp and buy reverts until the treasury is re-set (liveness only, recoverable). Owner-only trigger (one wrong argument), so hardening; reported because the project already guards the same value in one constructor and the ETH loss is permanent. Merged from audit_flow 4f7f0242, audit_economics 58f68b2c, audit_math b9b66f1d and audit_permissions b5b593a1. Fix: `if (t == address(0)) revert ZeroAddress();` in MailOffice.setTreasury, MessengerNFT.setTreasury, Wardrobe.setTreasury (add the error to Wardrobe), the MessengerNFT and Wardrobe constructors, and DeliveryRewards.setPoster.

**Reproduction**

Setup as test/P2E.t.sol; alice has an open office (office holds 0.005 ETH), 200,000 MAIL and an unlimited approval; wardrobe item 1 listed at 100 MAIL. (a) owner: office.setTreasury(address(0)) succeeds; alice: office.upgrade(7_000e18) -> expected tier 2, actual revert ERC20InvalidReceiver(0x0). (b) owner: office.withdraw() -> ok, office balance 0, address(0).balance grows by 0.005 ether. (c) owner: wardrobe.setTreasury(address(0)); alice: buy(1,1,100e18) -> revert ERC20InvalidReceiver(0x0). (d) owner: nft.setTreasury(address(0)); setSaleOpen(true); bob: mint{value: 0.01 ether}(1) succeeds, bob owns token 3, address(0).balance grows by 0.01 ether. (e) new MessengerNFT(..., treasury_ = address(0), ...) and new Wardrobe(mail, address(0), ...) deploy; rewards.setPoster(address(0)) succeeds and poster() == 0. All five observed in test/scratch/Judge.t.sol (test_ZeroTreasury_*, test_SetPosterZeroAccepted). Proof: forge test --match-path test/scratch/ZeroTreasury.t.sol (3 tests expecting the setters to reject address(0) fail on the current code with 'next call did not revert as expected' and pass with the zero checks added).

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
import {Wardrobe} from "src/Wardrobe.sol";

/// The treasury setters accept address(0) although MailOffice's constructor rejects it. With a zero
/// treasury, MailOffice.withdraw and MessengerNFT.mint forward ETH to address(0) (a successful call that
/// burns the funds) and every MAIL spend (upgrade, levelUp, Wardrobe.buy) reverts in the ERC20 with
/// ERC20InvalidReceiver. Expected: each setter rejects address(0), as the constructor does.
contract ZeroTreasuryTest is Test {
    MailToken mail;
    MessengerNFT nft;
    MailOffice office;
    DeliveryRewards rewards;
    Wardrobe wardrobe;

    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address liquidity = makeAddr("liquidity");
    address poster = makeAddr("poster");
    uint256 constant DAILY = uint256(16_800_000e18) / 102;

    function setUp() public {
        vm.startPrank(owner);
        mail = new MailToken(liquidity, owner);
        nft = new MessengerNFT(owner, treasury, owner, 0.01 ether, keccak256(abi.encode(keccak256("s"))), address(new DevTransferValidator()), "ipfs://m/");
        rewards = new DeliveryRewards(mail, owner, poster, 1 days, DAILY, 51);
        office = new MailOffice(mail, nft, IRewardDay(address(rewards)), treasury, owner);
        wardrobe = new Wardrobe(mail, treasury, owner, "ipfs://w/{id}.json");
        vm.stopPrank();
    }

    function test_OfficeSetTreasuryRejectsZero() public {
        vm.prank(owner);
        vm.expectRevert();
        office.setTreasury(address(0));
        assertEq(office.treasury(), treasury);
    }

    function test_NftSetTreasuryRejectsZero() public {
        vm.prank(owner);
        vm.expectRevert();
        nft.setTreasury(address(0));
        assertEq(nft.treasury(), treasury);
    }

    function test_WardrobeSetTreasuryRejectsZero() public {
        vm.prank(owner);
        vm.expectRevert();
        wardrobe.setTreasury(address(0));
        assertEq(wardrobe.treasury(), treasury);
    }
}
```

### 5. Info: Owner can compute the reveal seed before calling reveal() and ownerMint ids with chosen traits in the same block, wider than the documented 'choose among a few candidate seeds'

`p2e/contracts/src/MessengerNFT.sol:136`

```
        if (seed != 0) revert AlreadyRevealed(); // traits are knowable after reveal: no more minting
```

Trust-assumption note, not a bypass. reveal derives the seed from the owner's secret and blockhash(block.number - 1), both known to the owner at the start of the reveal block, and ownerMint is still allowed in that block because it only blocks once seed != 0. After closing the sale the owner can compute the exact seed, scan ids totalMinted+1..3333 for the rarest traits (the 2% Golden Letter unlocks every job type on the game server), ownerMint exactly up to that id and reveal in the same block or bundle. AUDIT.md's accepted limit only says the owner 'could choose among a few candidate seeds'; it does not say the owner can mint tokens with known traits after the sale. Buyers still cannot influence or predict the seed, so guarantee 13 holds for them. If this power is not intended, a minimal fix that keeps giveaways is to forbid ownerMint once saleClosedAt != 0, or to bind the seed to a block fixed at close time (blockhash(saleClosedAt + 1), revealed within 256 blocks) so no minting can happen after the seed is determined; otherwise widen the AUDIT.md wording. From audit_flow 7eab2195.

**Reproduction**

Setup as test/P2E.t.sol (2 tokens owner-minted to alice). Owner: setSaleOpen(true); setSaleOpen(false); roll 10 blocks. Compute predicted = keccak256(abi.encode(SECRET, blockhash(block.number - 1))) | 1; find the first id > totalMinted with (keccak256(abi.encode(predicted, id)) >> 64) % 1000 >= 980; ownerMint(owner, id - totalMinted); reveal(SECRET). Result: nft.seed() == predicted and nft.traitsOf(id).carry == 4 (Golden Letter), chosen before the on-chain reveal. Observed in test/scratch/Judge.t.sol test_OwnerPredictsSeedAndMintsGoldenLetter.

### 6. Info: renounceOwnership() is reachable on every Ownable2Step contract; on MailOffice it strands collected office ETH because withdraw() is onlyOwner

`p2e/contracts/src/MailOffice.sol:266`

```
    function withdraw() external onlyOwner {
```

Ownable2Step (OpenZeppelin 5.4) keeps Ownable.renounceOwnership as a single-step call; none of the five contracts override it and no test exercises it. On MailOffice the only way ETH leaves is withdraw(), which is onlyOwner, so a renounce (accidental, or by a compromised owner key) permanently locks every 0.005 ETH office fee collected since the last withdraw and freezes costs, tiers and the treasury address. On DeliveryRewards a renounce removes pause/unpause, revokeRoot and poster rotation, which AUDIT.md lists as the mitigations for a leaked poster key. Owner footgun, not a user-facing bypass. Fix: override renounceOwnership to revert, or make withdraw() permissionless since it already pays only the treasury. From audit_flow 8a16e550.

**Reproduction**

Office holds 0.005 ETH from alice's open(). Owner calls office.renounceOwnership(): succeeds, owner() == address(0). Owner (or anyone) then calls office.withdraw(): reverts OwnableUnauthorizedAccount; setTreasury/setOpenPrice/openTiers revert the same way, so the ETH is stuck. Owner calls rewards.renounceOwnership() then rewards.pause(): reverts OwnableUnauthorizedAccount. Expected: an ownerless office can still pay the treasury, or renounce is impossible. Observed in test/scratch/Judge.t.sol test_RenounceStrandsOfficeEth.

### 7. Info: After unassign(), the same wallet cannot re-assign its own Messenger until the next reward day (TooSoon), because the rule is keyed on the token only

`p2e/contracts/src/MailOffice.sol:168`

```
    function unassign() external nonReentrant {
```

The once-per-reward-day rule exists so one NFT cannot play for two wallets in one day, but it is keyed only on the token, not on who last assigned it. unassign clears characterOf/assignedBy and unlocks, yet leaves lastAssignedDay, so the same wallet's assign on the same day reverts TooSoon. A player who unassigns by mistake, or briefly to let the Apprentice play, loses the Messenger's stamina for the rest of the day; the server-side per-wallet paid counter already prevents any extra stamina from re-assigning. Distinct from the medium double-play finding (that one is too lax across wallets; this one is too strict within a wallet) but the same root cause and the same fix resolves both: record lastWalletOf[id] in assign and only reject a different wallet on the same day (verified: with that fix this scenario succeeds while bob is still rejected the same day). If the strictness is intended, document it in AUDIT.md guarantee 8, which is worded as an anti-pass-around rule. From audit_permissions f49bf6f4.

**Reproduction**

alice has an open office and owns Messenger 1; t = startTime + 12h (day 0). alice calls assign(1), unassign(), assign(1) in the same reward day. Expected (anti-pass-around rule only): the second assign succeeds. Actual: the second assign reverts TooSoon. Observed in test/scratch/Judge.t.sol test_SameWalletReassignSameDayTooSoon.

### 8. Info: The current office can unlock Messengers locked by a previous office, wider than the documented 'unlock the ones it locked', and that strands the old office's assignment

`p2e/contracts/src/MessengerNFT.sol:220`

```
            if (msg.sender != office && msg.sender != lockedBy[id]) revert NotOffice();
```

The lock branch records lockedBy[id] = msg.sender; the unlock branch accepts either the locking office or whatever office currently is. AUDIT.md's trust assumption says a malicious office 'could lock or level any Messenger (and unlock the ones it locked)'; actually a newly set office can unlock any locked token, which deletes lockedBy while the old MailOffice still has characterOf[wallet] = id and assignedBy[id] = wallet. The token becomes transferable while the old office still reports it as that wallet's character (staminaOf), and once the holder sells it the old wallet can no longer unassign (the old office is neither office nor lockedBy, so setLocked(id, false) reverts NotOffice), leaving it with a characterOf it does not own and unable to assign another Messenger in that office. Requires the NFT owner to point office at a contract that unlocks tokens it did not lock, so this is a trust assumption rather than a bypass; the honest MailOffice only unlocks its own characterOf. Fix: tighten the unlock branch to msg.sender == lockedBy[id] (the current office never needs to unlock a token it did not lock), or correct the AUDIT.md wording. From audit_permissions ddff43bc.

**Reproduction**

alice opens an office and assigns token 1 (lockedBy[1] == office). Owner calls nft.setOffice(U) where U is any contract that calls messengers.setLocked(1, false). U.unlock(1): expected per AUDIT.md NotOffice; actual succeeds, locked[1] false, lockedBy[1] == 0, while office.characterOf(alice) == 1 and office.staminaOf(alice) == 12. alice transfers token 1 to bob (succeeds, no longer locked), then alice calls office.unassign(): reverts NotOffice; office.characterOf(alice) stays 1. Observed in test/scratch/Judge.t.sol test_NewOfficeUnlocksOldOfficeLock.

---

Judge's submission `bea714c1822eb5bd6d123fc6ffdd8ec8fb41e2a5837f46acca738ff7013e2c3c`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
