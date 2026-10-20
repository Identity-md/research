# Audit report

> Audit the contracts in AdamNakamoto/delivermail as they are.

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/delivermail.git |
| Commit | `29767796f5d58f1054eb1693a1bc5622b907120f` |
| Job | `ed98e0c7-d552-4c11-844c-8a8395e43fb5` |
| Judged | 2026-10-20 04:25 UTC |
| Findings | 1 low · 3 info |

Four agents audited the code as it is at `2976779`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: MessengerNFT.setOffice moves the lock but not the office tiers players paid for in MAIL, nor the ETH gate

`p2e/contracts/src/MailOffice.sol:49`

```
    mapping(address => uint8) public tierOf;
```

Messenger levels are stored on MessengerNFT (levelOf) and survive a change of office, but office tiers live only in the MailOffice instance that sold them (tierOf, lastUpgradeAt), as does the 0.005 ETH open gate. A fresh MailOffice installed with MessengerNFT.setOffice starts every wallet at tier 0: staminaOf, apprenticeStaminaOf and capacityOf read 0, assign reverts NotOpen, and the wallet must pay openPrice again and re-buy the whole ladder (up to 168,000 MAIL, 75% burned) at full price while the old office keeps the ETH and the burned MAIL is gone. The owner is trusted and the migration is an owner action, so this is a trust-gap rather than a permission bypass, but AUDIT.md describes setOffice only as 'changing the office never strands a Messenger' and lists what the office owner can't do ('move anyone's NFT or MAIL'); it does not say that a migration voids every paid tier and re-charges the gate. Reproduced by the judge (test/scratch/Judge.t.sol::test_OfficeMigrationLosesPaidTiers, passes on this code, i.e. the loss happens). Merged from the permissions specialist; the economics specialist reported nothing on this path. Fix options that keep the design: document the loss as a trust assumption, or let a new office import tierOf/lastUpgradeAt once per wallet from a `previousOffice`, or keep tierOf on the NFT next to levelOf.

**Reproduction**

State: alice has Messenger #1, 100,000 MAIL and an approval for the office. alice: office.open{value: 0.005 ether}(0); office.upgrade(7_000e18); office.assign(1). Now office.tierOf(alice)==2 and office.staminaOf(alice)==14. Owner: office2 = new MailOffice(mail, nft, rewards, treasury, owner); nft.setOffice(office2). Expected (per AUDIT.md's description of setOffice): the wallet's paid state follows the player. Actual: office2.tierOf(alice)==0, office2.staminaOf(alice)==0, office2.apprenticeStaminaOf(alice)==0, office2.capacityOf(alice)==0, office2.assign(1) reverts NotOpen; after office.unassign() and office2.open{value: 0.005 ether}(0) the wallet is at tier 1 and office2.upgradeCost(2)==7_000e18 is due again; address(office).balance still holds the first 0.005 ETH and mail.totalSupply() shows the 5,250 MAIL burned by the first upgrade is not restored.

### 2. Info: Privileged setters that change where value goes or who may lock emit no event

`p2e/contracts/src/MessengerNFT.sol:248`

```
    function setOffice(address office_) external onlyOwner {
```

MessengerNFT.setOffice (the contract allowed to lock any Messenger and raise levels), MessengerNFT.setTreasury (mint payments), MailOffice.setTreasury (25% of every MAIL spend plus withdrawn ETH), MailOffice.setOpenPrice (the sybil gate) and Wardrobe.setTreasury write storage with no event, while the sibling setters in the same contracts (setPrice, setMaxLevel, setTransferValidator, setUpgradeCost, setLevelCost, openTiers, list) all emit. AUDIT.md relies on the office change being 'visible on-chain', but nothing indexable marks it: a player, the game server or a monitor cannot subscribe to the change and has to poll storage. Reproduced by the judge (test/scratch/Judge.t.sol::test_SettersEmitNoEvent). Fix: emit OfficeSet(address), TreasurySet(address) and OpenPriceSet(uint256) from each setter.

**Reproduction**

With owner as caller: vm.recordLogs(); nft.setOffice(address(office2)); nft.setTreasury(alice); office.setTreasury(alice); office.setOpenPrice(1); wardrobe.setTreasury(alice); vm.getRecordedLogs().length. Expected: one event per privileged state change, as the other owner setters in these contracts do. Actual: 0 logs for all five calls, while nft.office()==office2 and office.openPrice()==1 confirm the state did change.

### 3. Info: Guarantee 6 'claims for a day never exceed that day's total' (OverTotal) and the AllocationExhausted cap have no test

`p2e/contracts/src/DeliveryRewards.sol:214`

```
        if (d.claimed + amount > d.total) revert OverTotal();
```

The 107-test suite never reaches the OverTotal revert nor AllocationExhausted (line 136): grep for either name in p2e/contracts/test returns nothing. These are the two caps that bound minting when the poster under-declares a day's total or posts more than the 16.8M play allocation. Both are correct on this code: an early 80% claim books the full `amount` into d.claimed, so a 20% burn cannot be used to overdraw a day. But nothing pins them, so a future change to _settle or claimNow (for instance booking only the paid 80%) would silently drop a stated guarantee. Reproduced by the judge: test/scratch/Judge.t.sol::test_OverTotalReachable_EarlyClaimsCountFull passes on the current code and would be the missing test. Fix: add that scenario and a postRoot sequence that exhausts PLAY_ALLOCATION to the suite.

**Reproduction**

Deploy DeliveryRewards(mail, owner, poster, 1 days, 16_800_000e18/102, 51) as minter; warp to startTime + 1 day. Two-leaf tree: leaf(alice, 0, 100e18), leaf(bob, 0, 100e18); poster: postRoot(0, root, 150e18) (total below the leaf sum). Warp to claimableFrom(0). alice.claimNow(0, 100e18, proofA): alice receives 80e18 and days_(0).claimed == 100e18 (the full amount, not 80e18). bob.claimNow(0, 100e18, proofB): expected and actual revert OverTotal(). Covered by the existing suite: no.

### 4. Info: Guarantee 17 'partial fills are rejected in every direction and mode' is only tested for exact-in buys; the exact-out sell branch is untested

`p2e/contracts/src/MailHook.sol:281`

```
            if (exactIn ? poolQuote + fee != requested : poolQuote != requested + fee) revert PartialFill();
```

test_PartialFillIsRejected in test/MailHook.t.sol exercises only the exactIn == true branch of this line (an exact-in buy stopped by a price limit). The exact-out sell branch (ETH is the specified output and the seller asks for more ETH than the pool holds) is the one where an unrejected partial fill would matter most: beforeSwap already charged ceil(Y/24) on the requested Y, so a short fill would pay a fee above 4% of what the pool actually delivered. The branch is correct on this code, reproduced by the judge (test/scratch/Judge.t.sol::test_ExactOutSellPartialFillReverts passes), but nothing in the suite pins it. Fix: add that scenario next to test_PartialFillIsRejected.

**Reproduction**

Open the pool as in test/MailHook.t.sol setUp (START_MCAP 20 ether, LAUNCH 4.2M). alice: router.buy{value: 1 ether}(mail, 1, now) -> pool holds 0.96 ETH, pendingProtocolFees(ETH) == 0.04 ether. alice via PoolSwapTest: swap(key, SwapParams(zeroForOne=false, amountSpecified=+2e18, MAX_SQRT_PRICE-1)). Expected and actual: revert (MailHook.PartialFill wrapped by the PoolManager); pendingProtocolFees unchanged at 0.04 ether. Then swap(key, SwapParams(false, +0.5e18, MAX_SQRT_PRICE-1)): alice.balance rises by exactly 0.5 ether and pendingProtocolFees rises by (0.5e18 + 23) / 24.

---

Judge's submission `d3974c4ae37c6dd189637e3743778b5be19038294f62513bd7167369296731fc`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
