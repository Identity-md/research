# Audit report

> Courier ($STAMP), new contracts since launch: Courier Skins (CourierSkins.sol) and the golden stamp hunt (StampHunt.sol). The code is on branch audit-skins-hunt, commit 2cf3432 (https://github.com/AdamNakamoto/courierworld/tree/audit-skins-hunt); main does not have it yet. Read AUDIT.md section 9 first: it describes both contracts, what they must guarantee and what is accepted. Sections 1-8 cover the live game, audited in ea514609, ca28d248 and 19b34b9b; it is deployed, unchanged, and the new contracts only read from it.
>
> What it is: a game on Robinhood Chain (4663). CourierSkins is 999 cosmetic NFTs (16 designs) players wear in the game. Blind mint for ETH (0.004, up to 10 per transaction), paid straight to the treasury. A commit-reveal seed (secret mixed with blockhash at the reveal) keys a 4-round Feistel shuffle on 10 bits with cycle-walking, so each token gets a distinct card of a 999-card deck and a full mint matches every design's supply. Metadata is on-chain JSON (tokenURI and ERC-7572 contractURI); pictures come from an owner-set image base that can be frozen. The 5% royalty is enforced with ERC721-C: every transfer between two non-zero addresses calls OpenSea's StrictAuthorizedTransferSecurityRegistry (0xA000027A9B2802E1ddf7000061001e5c005A0000, live on Robinhood Chain). The rate is fixed; the validator can be replaced but never removed. StampHunt pays $STAMP from a pool the owner fills (it never mints) for golden stamps found in the game: the game server signs an EIP-712 voucher Finds(player, day, stamps, deadline), only wallets with an open post office can claim, and payouts are capped per wallet per day, per day in total, and by the pool.
>
> Scope: contracts/src/CourierSkins.sol, contracts/src/StampHunt.sol, contracts/script/DeploySkins.s.sol, contracts/script/DeployHunt.s.sol. Out of scope: contracts/script/DevTransferValidator.sol (local chains only), web/ and multiplayer/.
>
> What to check:
>
> Skins never exceed 999, every mint pays exactly price x quantity, and the payment reaches the treasury in the same call; nothing is ever left in the contract.
> Nobody, owner included, can know or influence any design before the reveal; designs never change after it; _shuffle is a bijection on 0..998 for every seed, so no design ever exceeds its supply.
> No path moves a skin between two non-zero addresses without calling the validator (transferFrom, both safeTransferFroms, anything reaching _update); the validator can't be set to zero or a non-contract; the royalty rate can't change from 5%; a holder can always move their own skin under the launch registry.
> tokenURI and contractURI always return valid base64 JSON, and designOf agrees with tokenURI.
> StampHunt pays only vouchers signed by signer for msg.sender, never pays a voucher beyond its count, never pays a wallet for more than maxStampsPerDay stamps in a day, never exceeds dailyLimit or the pool, pays only wallets with an open post office, and can't mint or touch any tokens but its own pool.
>
> Tests: cd contracts; git submodule update --init --recursive; forge test --match-contract "CourierSkinsTest|StampHuntTest" (28 tests). Fork: forge test --match-contract CourierSkinsForkTest --fork-url https://robinhood.drpc.org (against OpenSea's real registry: holder transfers pass, a marketplace without the fee check is refused). All 125 tests: forge test.

| | |
|---|---|
| Repository | https://github.com/AdamNakamoto/courierworld.git |
| Commit | `2cf3432693110c2fe40cc71e5bee2ca7f343c46e` |
| Job | `25e6a0b3-8bc8-422f-820c-d984e1517f57` |
| Judged | 2026-10-11 17:51 UTC |
| Findings | 1 medium · 2 low · 4 info |

Four agents audited the code as it is at `2cf3432`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: reveal() may run while the sale is open, so the seed is computable before it lands and the owner (or anyone who sees the secret in the pending reveal) can mint IDs whose designs it already knows

`contracts/src/CourierSkins.sol:126`

```
        uint256 s = uint256(keccak256(abi.encode(secret, blockhash(block.number - 1))));
```

Guarantee 2 (AUDIT.md section 9) and the NatSpec on reveal ('the owner can't pre-compute the designs either') say nobody, minter or owner, can know or influence a design before the reveal. The seed is keccak256(secret, blockhash(block.number - 1)). Both inputs are known before the reveal transaction executes: the secret is the owner's, and blockhash(block.number - 1) is already final when a transaction for the current block is built. Nothing forces minting to have stopped before that hash is fixed: reveal() closes the sale itself (line 122), and setSaleOpen(false) can be undone by setSaleOpen(true) until the reveal. So while the sale is open the owner can compute the exact seed a reveal would set now, run the public _shuffle/_designAt logic for IDs totalMinted+1 onward, mint exactly the IDs that land on Golden/Hologram Couriers or Moonwedges (10 per call, repeatable), and then reveal under the same hash; since mint payments go to the owner-set treasury the mints cost it only gas. On Robinhood Chain (Arbitrum Nitro, chain 4663) this needs no same-block bundle: block.number is the parent-chain (L1) block number and blockhash(block.number - 1) is ArbOS's deterministic value for that L1 block, identical for every L2 block of one L1 block. Observed live during this review: L2 blocks 86019789 and 86019829, four seconds apart, both report l1BlockNumber 26170803. Two ordinary transactions a few seconds apart therefore share the reveal entropy. A second, weaker actor exists: anyone who sees the reveal calldata before it is sequenced (the owner's RPC provider, the sequencer operator) learns the secret while the sale is still open and can mint the predicted IDs ahead of the reveal; Robinhood Chain has no public mempool, so that set is small. This is stronger than the 'Reveal timing' item in Known and accepted (the owner may wait for a blockhash it likes, which re-rolls the whole mapping): here the owner chooses which unminted deck slots it takes with certainty, so unminted legendaries are never really at stake for public minters once the sale slows. Minimal fix that keeps the design: refuse a reveal that can share its blockhash with an open sale. For example record saleClosedAt = block.number in setSaleOpen(false) (reset on reopen) and in reveal require !saleOpen && block.number > saleClosedAt, so the hash mixed in did not exist while anyone could still mint; document that on Arbitrum-family chains 'a later block' means a later L1 block. Alternatively make reveal() two-step: close and record the block, then draw the seed from blockhash(recorded + 1) once it exists (within 256 blocks). Merged from four specialist reports (audit_math, audit_flow, audit_economics, audit_permissions) describing the same mechanism.

**Reproduction**

State: sale open, tokens 1..5 minted by a player, secret S known to the owner, commit = keccak256(abi.encode(S)), block rolled forward 10 blocks. The owner computes s = keccak256(abi.encode(S, blockhash(block.number - 1))) (s == 0 -> 1) and predicted[i] = _designAt(_shuffle_s(5 + i)) for i = 0..9 (the designs tokens 6..15 will get), then in the same block calls mint{value: 0.04 ether}(10) and reveal(S). Expected (guarantee 2): the reveal is refused or designOf(6..15) does not match the prediction. Actual: both calls succeed, skins.seed() == s, and designOf(6 + i) == predicted[i] for all ten. Run: forge test --match-path test/scratch/Proof_d6a1e26c635c.t.sol fails with 'owner minted tokens whose designs it had already computed, then revealed'. The second specialist proof (Proof_9e47ecaacd12.t.sol, treasury == owner, 100 public mints, IDs 101..110) fails the same way. Both pass once reveal() reverts while the sale is open or in the block the sale was closed.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {CourierSkins} from "src/CourierSkins.sol";

contract PassValidator {
    function validateTransfer(address, address, address, uint256) external view {}
}

/// Guarantee 2 of AUDIT.md section 9: before `reveal` nobody, owner included, can know or influence any
/// token's design. The seed is keccak256(secret, blockhash(block.number - 1)), and both inputs are known to
/// the owner while the sale is still open (the sale is only closed inside `reveal` itself). So the owner can
/// compute the seed, predict the designs of the next unminted IDs, mint exactly those, and reveal in the same
/// block. This test fails on the current code (the prediction matches every minted token) and passes once
/// minting is impossible with the reveal entropy in hand (e.g. `reveal` requires the sale to have been closed
/// in an earlier block, or the seed is drawn from a block after the sale closed).
contract OwnerPredictsDesignsTest is Test {
    CourierSkins skins;
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");
    address alice = makeAddr("alice");
    uint256 constant PRICE = 0.004 ether;
    uint256 constant SECRET = 0x5EC12E7;

    function setUp() public {
        skins = new CourierSkins(owner, treasury, PRICE, keccak256(abi.encode(SECRET)), address(new PassValidator()), "x/");
        vm.prank(owner);
        skins.setSaleOpen(true);
        vm.deal(alice, 1 ether);
        vm.deal(owner, 1 ether);
        vm.prank(alice);
        skins.mint{value: PRICE * 5}(5); // the public sale: tokens 1..5
        vm.roll(block.number + 10);
    }

    // The owner's off-chain replica of the contract's shuffle, keyed by the seed it can already compute.
    function _shuffle(uint256 s, uint256 x) internal pure returns (uint256) {
        do {
            uint256 l = x >> 5;
            uint256 r = x & 31;
            for (uint256 i = 0; i < 4; i++) {
                (l, r) = (r, l ^ (uint256(keccak256(abi.encode(s, i, r))) & 31));
            }
            x = (l << 5) | r;
        } while (x >= 999);
        return x;
    }

    function _designAt(uint256 slot) internal view returns (uint256 design) {
        uint256 end;
        for (design = 0; design < 16; design++) {
            end += skins.supplyOf(design);
            if (slot < end) return design;
        }
        revert();
    }

    function test_OwnerCannotMintKnowingTheDesigns() public {
        // What the owner knows before anyone else: the secret, and this block's reveal entropy.
        uint256 s = uint256(keccak256(abi.encode(SECRET, blockhash(block.number - 1))));
        if (s == 0) s = 1;
        uint256 first = skins.totalMinted() + 1; // 6
        uint256[10] memory predicted;
        for (uint256 i = 0; i < 10; i++) predicted[i] = _designAt(_shuffle(s, first + i - 1));

        // The owner mints the next ten (paying its own treasury) and reveals in the same block.
        vm.startPrank(owner);
        (bool minted,) = address(skins).call{value: PRICE * 10}(abi.encodeCall(CourierSkins.mint, (10)));
        (bool revealed,) = address(skins).call(abi.encodeCall(CourierSkins.reveal, (SECRET)));
        vm.stopPrank();

        bool allMatch = minted && revealed && skins.seed() != 0;
        for (uint256 i = 0; allMatch && i < 10; i++) {
            if (skins.designOf(first + i) != predicted[i]) allMatch = false;
        }
        assertFalse(allMatch, "owner minted tokens whose designs it had already computed, then revealed");
    }
}
```

### 2. Low: DeployHunt narrows HUNT_MAX_PER_DAY to uint16 unchecked and validates none of its inputs; a cap of 0 is accepted by StampHunt and silently stops every payout

`contracts/script/DeployHunt.s.sol:29`

```
            uint16(vm.envOr("HUNT_MAX_PER_DAY", uint256(24))),
```

The per-wallet daily cap is read as uint256 from the environment and narrowed with a plain uint16() cast, which truncates instead of reverting: 70000 becomes 4464, 65560 becomes 24 (indistinguishable from the default), and any multiple of 65536 becomes 0. Neither the StampHunt constructor (contracts/src/StampHunt.sol:87) nor setLimits (line 171) rejects maxStampsPerDay == 0, and unlike dailyLimit, 0 does not mean 'no limit' there: claimable() computes cap = 0 and returns (0, 0), so every claim() reverts NothingToClaim however full the pool is. The two limits set in the same call thus have opposite zero semantics. The script also passes STAMP and OFFICE straight into immutables with no check that OFFICE has code and answers offices(address) with the nine-field tuple, or that it belongs to the given STAMP (deployments/robinhood.json holds the live pair but the script reads raw env), so a swapped pair deploys cleanly and every claim and deposit then reverts; the only remedy for either mistake in the immutables is to redeploy and repoint the signer and front end. Fix: in the script read the cap as uint256 and require 0 < v <= type(uint16).max before casting, require OFFICE.code.length > 0 (ideally PostOffice(OFFICE).stamp() == STAMP), and log the values the constructor receives; in StampHunt revert on maxStampsPerDay_ == 0 in the constructor and setLimits, or define 0 as 'no cap' consistently with dailyLimit. Merged from audit_math, audit_economics, audit_permissions and audit_flow reports on the same line.

**Reproduction**

Scratch test test/scratch/Probe.t.sol::test_DeployHuntTruncatesMaxPerDay: with STAMP, OFFICE, HUNT_SIGNER and HUNT_OWNER set, HUNT_MAX_PER_DAY=70000 -> new DeployHunt().run() returns a hunt with maxStampsPerDay() == 4464; HUNT_MAX_PER_DAY=65536 -> 0; HUNT_MAX_PER_DAY=65560 -> 24. Expected: the script refuses an out-of-range value. test_MaxPerDayZeroStopsEveryPayout: StampHunt deployed with maxStampsPerDay 0 and a 1000e18 pool; claimable(alice, today, 3) returns (0, 0) and a validly signed claim(today, 3, deadline, sig) from a wallet with an open office reverts NothingToClaim; the same state is reached on a live hunt by setLimits(0, 10_000e18). test_DeployHuntSwappedAddressesDeploys: STAMP and OFFICE swapped -> deployment succeeds with stamp() == the office address and the first claim reverts. All three pass on the current code.

### 3. Low: reveal() and setImageBase() rewrite every token's metadata but emit no ERC-4906 event, so marketplaces keep showing skins as sealed

`contracts/src/CourierSkins.sol:128`

```
        emit Revealed(seed);
```

Before the reveal tokenURI returns 'Courier Skin #n', status Sealed and mystery.png; after it, the design, rarity, type and picture. The reveal therefore changes the metadata of every minted token at once, and setImageBase changes every token's image. OpenSea and other marketplaces that cache tokenURI re-read it automatically only when the collection emits ERC-4906's MetadataUpdate(uint256) or BatchMetadataUpdate(uint256,uint256) and reports interface 0x49064906 in supportsInterface. CourierSkins emits only SaleOpen(false) and Revealed(seed) in reveal and ImageBaseSet plus ContractURIUpdated in setImageBase, and supportsInterface(0x49064906) is false. Listed skins keep the sealed name, mystery picture and no Design/Rarity traits until each holder refreshes manually, which is exactly when the traits drive pricing and the enforced royalty's value. Fix: emit BatchMetadataUpdate(1, totalMinted) in reveal (and in setImageBase when totalMinted > 0) and return true for 0x49064906 in supportsInterface. Reported by audit_flow; kept after reproduction.

**Reproduction**

Scratch test test/scratch/Probe.t.sol::test_NoMetadataUpdateEventOnReveal: mint 3 tokens, roll 5 blocks, vm.recordLogs(), reveal(secret), setImageBase('y/'). Expected: a BatchMetadataUpdate(1,3) or MetadataUpdate log and supportsInterface(0x49064906) == true. Actual: 4 logs, none with topic0 keccak256('MetadataUpdate(uint256)') or keccak256('BatchMetadataUpdate(uint256,uint256)'), tokenURI(1) differs from before the reveal, and supportsInterface(0x49064906) returns false. Passes on the current code.

### 4. Info: claim() reverts PoolEmpty when it is the day's dailyLimit, not the pool, that is exhausted

`contracts/src/StampHunt.sol:132`

```
            revert PoolEmpty();
```

claimable() returns count 0 for three reasons: the wallet already reached its per-day cap, the pool cannot cover one stamp, or dailyLimit - paidFor[day] cannot. claim() distinguishes only the first (NothingToClaim) and reports the other two as PoolEmpty, so a claim blocked by the day's global limit says the pool is empty while it may hold thousands of $STAMP. The accounting is correct (nothing is overpaid and the stamps stay claimable the next day or after setLimits), but the game client, support, or the owner reading the revert will act on the wrong cause: a deposit does not unblock the claim. Fix: add a DailyLimitReached error and choose it when dailyLimit != 0 && dailyLimit - paidFor[day] < rewardPerStamp before falling back to PoolEmpty. Merged from identical reports by all four specialists.

**Reproduction**

Scratch test test/scratch/Probe.t.sol::test_DailyLimitRevertsPoolEmpty: StampHunt with reward 10e18, maxStampsPerDay 24, dailyLimit 50e18, pool 1000e18, alice and bob with open offices. alice claims a valid 5-stamp voucher for today: paid 50e18, paidFor[today] == 50e18, pool 950e18. bob then calls claim with a valid 4-stamp voucher for today. Expected: a revert naming the daily limit. Actual: claimable(bob, today, 4) == (0, 0) and the claim reverts PoolEmpty() while pool() == 950e18. Passes on the current code.

### 5. Info: AUDIT.md says the owner can't mint for free, but setPrice(0) makes every mint free and owner mints at any price only pay the owner's own treasury

`contracts/src/CourierSkins.sol:330`

```
        price = price_;
```

Section 9 lists 'mint for free' among the things the owner can't do. setPrice has no floor and no timing restriction, and mint only checks msg.value == price * quantity, so the owner can set the price to 0, mint 10 per call as often as it likes, and restore the price, with PriceSet events as the only trace; while the price is 0 any other wallet can mint free too, so a buyer who paid 0.004 ETH cannot rely on every other skin having been paid for. Independently, every mint payment goes to the owner-controlled treasury, so the owner's mints cost it nothing even at full price. This is an owner power, not a bypass of any check, and the sale is blind, so it is reported as a trust-model statement that is too strong; it is also what makes the owner's knowledge-based mint in the medium finding free. Fix: either document the power as accepted, or add a minimum price (revert on price_ == 0) or a one-way price lock the owner sets before opening the sale. Merged from audit_economics, audit_permissions and audit_flow.

**Reproduction**

Scratch test test/scratch/Probe.t.sol::test_OwnerMintsFreeViaPriceZero: owner calls setPrice(0), mint{value: 0}(10); bob calls mint{value: 0}(10); owner calls setPrice(0.004 ether). Expected per AUDIT.md: the owner cannot mint for free. Actual: balanceOf(owner) == 10, balanceOf(bob) == 10, treasury.balance == 0, price back at 0.004 ether. Passes on the current code.

### 6. Info: ETH forced into CourierSkins can never leave it: mint forwards msg.value, not the balance, and there is no receive, fallback or sweep

`contracts/src/CourierSkins.sol:112`

```
        Address.sendValue(payable(treasury), msg.value);
```

Guarantee 1 says nothing is ever left in the contract. Mint payments are forwarded in full and there is no receive or fallback, so ordinary payments never accumulate. ETH can still be placed in the contract without calling it: SELFDESTRUCT of a contract created in the same transaction still transfers its balance after EIP-6780 (Cancun, the configured evm_version), and the deterministic address can be pre-funded before deployment. Such ETH is stuck forever; only the sender loses, so this is informational. A one-line change keeps the guarantee exactly: forward address(this).balance instead of msg.value in mint, or add an owner-only sweep to the treasury. Merged from audit_permissions and audit_flow.

**Reproduction**

Scratch test test/scratch/Probe.t.sol::test_ForcedEthIsStuck: deploy `contract Burner { constructor(address payable to) payable { selfdestruct(to); } }` with 1 ether and to = address(skins). Then alice mints 1 skin at 0.004 ether. Expected under guarantee 1: address(skins).balance == 0 afterwards. Actual: the treasury receives exactly 0.004 ether, address(skins).balance stays 1 ether, and a plain call with value to the contract reverts. Passes on the current code.

### 7. Info: Test gaps: no test reveals under the same blockhash as a mint, and several hunt and mint edges are unexercised

`contracts/test/CourierSkins.t.sol:55`

```
        vm.roll(block.number + 5);
```

Every reveal in the suite goes through _reveal(), which rolls five blocks first, so no test mints and reveals under one blockhash(block.number - 1), computes the seed off-chain before the reveal, or asserts anything about who can know a design before it; that is the edge the medium finding lives on. Bijectivity of _shuffle is asserted for a single seed (test_FullMintMatchesEverySupply); testFuzz_DifferentSeedsGiveAValidDeal only checks designOf < 16. The marketplace-authorized path is only exercised against the mock StrictValidator; the fork tests show a holder transfer passing and an unauthorized operator refused under OpenSea's live registry, but none shows an authorized sale through the registry's beforeAuthorizedTransfer flow succeeding, so the only evidence that marketplace sales work at all is the mock. Also untested: maxStampsPerDay == 0 and setLimits lowering the cap below a wallet's claimed count; dailyLimit or the pool not being a multiple of rewardPerStamp; a claim exactly at deadline and exactly at the UTC day rollover; safeTransferFrom with data through the validator; mint with price == 0. The suite passes (28 tests, and 125 in all), so none of this is a defect in the contracts; it is where the stated guarantees are assumed rather than checked. Merged from audit_math and audit_flow.

**Reproduction**

grep -n 'vm.roll' contracts/test/CourierSkins.t.sol shows the only roll is in _reveal() at line 55, and every reveal call site uses it; no test calls skins.reveal in the block of a mint. forge test --match-contract CourierSkinsTest -vvvv shows block.number at each reveal is setUp's number + 5 with no mint in that block. The scratch tests test/scratch/Proof_d6a1e26c635c.t.sol (mint and reveal in one block) and Probe.t.sol::test_BijectionSeveralSeeds (full deal checked for three seeds: every design count equals supplyOf) are the missing cases; the latter passes.

---

Judge's submission `4d9466c86b78225782e8e4dfc731fdf91054506692c86e309b13458def1b50f3`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
