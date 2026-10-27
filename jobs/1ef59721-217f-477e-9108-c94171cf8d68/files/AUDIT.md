# Audit report

> Weir Townies: AUDIT ONLY, ROUND 2 (round 1 findings fixed: royalty follows the treasury and is capped, renounceOwnership reverts, cap arithmetic widened, zero withdraw reverts, freezeMetadata, endSale + owner sweeps). Review src/WeirTownies.sol from this repository as it arrives (do not edit src/, test/, foundry.toml or lib/) and report findings; do NOT deploy anything, do NOT create a token, pool, distributor or website. The owner deploys from script/Deploy.s.sol with their own key after findings at medium or above are fixed. Context: an ERC-721 (OpenZeppelin v5.5.0: ERC721, ERC721Enumerable, ERC2981, Ownable2Step, MerkleProof, ReentrancyGuard) for 3,333 tokens on Robinhood Chain (chainId 4663, Arbitrum Orbit, cancun). Token ids are laid out by the owner before the sale (setLayout, sealPools): an owner-minted reserve, then role pools each with its own Merkle root and a one-claim-per-wallet rule, then the general range sold first to a Merkle allowlist and then publicly at an ETH price with a per-wallet cap of 3. Metadata is off-chain at baseURI + id and the contract emits ERC-4906 events from an updater address. Money: msg.value must equal price x qty; withdraw() sends the balance to the treasury and anyone may call it. Please look hardest at: the id layout arithmetic (ranges never overlap, never exceed MAX_SUPPLY, no id minted twice), the Merkle leaf encoding (double keccak of abi.encode(address)) and proof misuse across pools, the per-wallet caps, reentrancy through _safeMint receivers, owner powers after the sale (nothing should touch sold tokens), and the withdraw path. Build: forge build && forge test (20 tests incl. fuzz and a reentrant receiver). Report any finding at medium or above and block on high or critical. Do not claim an independent audit.

| | |
|---|---|
| Repository | https://github.com/weircool/townies-contracts.git |
| Commit | `1a2dc1f02f008a53bb7a3dc65c240b4c833d9552` |
| Job | `1ef59721-217f-477e-9108-c94171cf8d68` |
| Judged | 2026-10-27 02:20 UTC |
| Findings | 1 medium · 2 low · 1 info |

Four agents audited the code as it is at `1a2dc1f`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Reserve ids left unminted at endSale() are stranded forever: ownerMint is closed by saleEnded and no sweep covers the reserve range

`src/WeirTownies.sol:186`

```
        if (saleEnded) revert SaleIsOver();
```

endSale() is one-way and its NatSpec (lines 235-236) and the README ('After the sale') promise that afterwards the owner can sweep what nobody claimed 'so the collection can still reach its full size'. That holds for the role pools (sweepPool) and the general range (sweepGeneral) but not for the reserve [1 .. reserveSize]: ownerMint is the only function that mints reserve ids, it reverts SaleIsOver once saleEnded is true (line 186), and both sweeps start at generalStart or p.start, which are always > reserveSize. saleEnded has no setter that clears it, setPhase is blocked after it, and ownership cannot bypass it. So every reserve id with index > reserveMinted at the moment endSale() runs can never be minted, totalSupply can never reach MAX_SUPPLY, and the provenance-committed 1/1s at those ids never exist. Trigger is owner sequencing only (no unprivileged actor), but the loss is irreversible and the runbook (README step 5, Configure.s.sol: 'reserve' and 'endsale' are independent actions with no ordering check) does not prevent it; the existing test test_endSaleAndSweep asserts the revert, so the consequence for the reserve was not followed through. Rated medium because a documented guarantee is false and the resulting state is permanent; the owner must either keep the reserve completable or refuse to end the sale with it incomplete. Reported by three specialists (permissions, flow, economics) and merged here. Minimal fix preserving the design, any one of: (a) remove the saleEnded check from ownerMint (it is owner-only and bounded by reserveSize, so it does not reopen the public sale); (b) make endSale revert while reserveMinted < reserveSize; (c) add a sweepReserve mirroring sweepGeneral. The attached proof accepts (a) or (b).

**Reproduction**

MAX_SUPPLY=100. Owner: setLayout(5, [2], [anyRoot]) (reserve 1..5, pool 6..7, general 8..100); sealPools(); ownerMint(owner, 2) -> ids 1,2, reserveMinted=2. Owner: endSale(). Owner: ownerMint(owner, 3) -> expected: ids 3,4,5 minted so the collection can reach 100 as endSale's NatSpec states; actual: revert SaleIsOver(). Owner: sweepPool(0, owner, 2) mints 6,7; sweepGeneral(owner, 93) mints 8..100; further sweepGeneral reverts SoldOut and sweepPool reverts PoolExhausted. End state: totalSupply()=97, reserveMinted=2, reserveSize=5, ownerOf(3) reverts, and no function can ever mint ids 3..5. Verified with test/scratch/Judge.t.sol::test_A_reserveStrandedAfterEndSale (passes on this code, i.e. the stranded state is reachable) and the attached proof test/scratch/ReserveStrandedAfterEndSale.t.sol, which fails on this code with SaleIsOver().

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {WeirTownies} from "src/WeirTownies.sol";

/// Finding: endSale() closes ownerMint, and neither sweep covers the reserve range, so any reserve id the owner has
/// not minted before endSale can never be minted. The NatSpec on endSale promises "the collection can still reach its
/// full size" after it. This test fails on the current code (ownerMint reverts SaleIsOver) and passes once the owner
/// can complete the reserve after the sale is over: either ownerMint stays open after endSale, or endSale refuses to
/// run while the reserve is incomplete (both branches are accepted below).
contract ReserveStrandedAfterEndSaleTest is Test {
    WeirTownies t;
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");

    function setUp() public {
        t = new WeirTownies(owner, treasury, 100, keccak256("prov"), 0, 0.001 ether);
        uint32[] memory sizes = new uint32[](1);
        sizes[0] = 2;
        bytes32[] memory roots = new bytes32[](1);
        roots[0] = keccak256("any");
        vm.startPrank(owner);
        t.setLayout(5, sizes, roots); // reserve 1..5, pool 6..7, general 8..100
        t.sealPools();
        t.setPhase(WeirTownies.Phase.Public);
        vm.stopPrank();
    }

    function test_reserveCanBeCompletedAfterEndSale() public {
        vm.prank(owner);
        t.ownerMint(owner, 2); // ids 1,2 minted; 3,4,5 still unminted when the sale ends
        assertEq(t.reserveMinted(), 2);

        vm.prank(owner);
        try t.endSale() {} catch {
            // acceptable fix: endSale refuses while the reserve is incomplete; finish it, then end the sale
            vm.prank(owner);
            t.ownerMint(owner, 3);
            vm.prank(owner);
            t.endSale();
        }
        assertTrue(t.saleEnded());

        if (t.reserveMinted() < t.reserveSize()) {
            // acceptable fix: the owner may still mint the reserve after endSale
            vm.prank(owner);
            t.ownerMint(owner, 3); // current code: reverts SaleIsOver, ids 3..5 are stranded forever
        }

        // sweeps cover the pool and the general range, never the reserve
        vm.prank(owner);
        t.sweepPool(0, owner, 2);
        vm.prank(owner);
        t.sweepGeneral(owner, 93);

        assertEq(t.reserveMinted(), 5);
        assertEq(t.ownerOf(3), owner);
        assertEq(t.ownerOf(5), owner);
        assertEq(t.totalSupply(), 100); // the collection reaches its full size
    }
}
```

### 2. Low: endSale, sweepGeneral and sweepPool do not require poolsSealed: a sweep on an unsealed layout followed by setLayout strands ids, underflows generalRemaining and wedges the sweep cursor

`src/WeirTownies.sol:237`

```
    function endSale() external onlyOwner {
        if (saleEnded) revert SaleIsOver();
        saleEnded = true;
```

sealPools' NatSpec (line 144) states 'Minting of any kind needs this', and ownerMint (line 184), mintRole (line 196) and _mintGeneral (line 223) each enforce poolsSealed; that is what makes the id ranges immutable once any id exists. endSale (line 237), sweepGeneral (line 246) and sweepPool (line 256) only check saleEnded, so the owner can end the sale on an unsealed layout and both sweeps then mint from ranges that are still mutable. setLayout (line 128) refuses only when poolsSealed is true, so after such a sweep the owner can replace the layout; setLayout rebuilds _pools (resetting each pool's minted counter) but never touches generalMinted, and the sweeps resume at newGeneralStart + generalMinted or p.start + p.minted. Consequences verified: (a) if the new general range is smaller than generalMinted, generalRemaining() (line 177) reverts with Panic(0x11) for every caller including the mint page and every sweepGeneral reverts SoldOut although ids remain unminted; (b) if the new generalStart is lower, the cursor lands on an id minted under the old layout and every sweepGeneral reverts inside ERC721._mint with ERC721InvalidSender(0) for good while generalRemaining() still reports ids as available; (c) ids below the resumed cursor can never be minted by any path because ownerMint, mintRole and mint* are closed by saleEnded. No id is ever minted twice (ERC721's existence check rejects it) and totalSupply never exceeds MAX_SUPPLY, so the core invariants hold; the defect is that the sealed-layout invariant the rest of the contract relies on has three unguarded paths and the failure is unrecoverable. Owner-only and contrary to the documented layout -> seal -> sale -> endSale order, hence low. Reported by all four specialists and merged here. Minimal fix: add `if (!poolsSealed) revert PoolsNotSealed();` to endSale (the single choke point, since both sweeps already require saleEnded), or to both sweeps.

**Reproduction**

Case (a): MAX_SUPPLY=100. Owner: setLayout(0, [], []) (general 1..100), do NOT seal. Owner: endSale() -> expected per the seal rule: revert PoolsNotSealed; actual: succeeds. Owner: sweepGeneral(owner, 50) -> expected: revert PoolsNotSealed as every other mint path; actual: mints ids 1..50, generalMinted=50. Owner: setLayout(90, [], []) -> succeeds, generalStart=91, generalSize=10; sealPools(). Now generalRemaining() reverts Panic(0x11) (10 - 50); sweepGeneral(owner, 1) reverts SoldOut; ownerMint(owner, 1) reverts SaleIsOver; totalSupply stays 50 and ids 51..100 are unmintable forever. Case (b): setLayout(5, [], []) unsealed; endSale(); sweepGeneral(owner, 10) mints 6..15; setLayout(0, [], []); sealPools(); generalRemaining() returns 90 but sweepGeneral(owner, 1) computes first = 1 + 10 = 11 and reverts ERC721InvalidSender(0x0) on every future call; totalSupply stays 10. Verified with test/scratch/Judge.t.sol::test_B_sweepBeforeSealThenRelayout_underflowAndWedge and ::test_B_sweepBeforeSealThenRelayout_cursorOnMintedId (both pass on this code, i.e. the broken states are reachable) and the attached proof test/scratch/SweepBeforeSeal.t.sol, which fails on this code because neither endSale nor sweepGeneral is blocked on an unsealed layout.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {WeirTownies} from "src/WeirTownies.sol";

/// Finding: endSale, sweepGeneral and sweepPool do not require poolsSealed, while every other mint path does. With an
/// unsealed layout the owner can sweep general ids and then call setLayout again, which moves generalStart under a
/// non-zero generalMinted: the sweep cursor now points at ids that were already minted, every further sweep reverts
/// with ERC721InvalidSender, generalRemaining() underflows, and the ids below the old cursor can never be minted.
/// The test fails on the current code (the sequence runs) and passes once endSale or the sweeps require the seal.
contract SweepBeforeSealTest is Test {
    WeirTownies t;
    address owner = makeAddr("owner");
    address treasury = makeAddr("treasury");

    function setUp() public {
        t = new WeirTownies(owner, treasury, 100, keccak256("prov"), 0, 0.001 ether);
        uint32[] memory sizes = new uint32[](1);
        sizes[0] = 3;
        bytes32[] memory roots = new bytes32[](1);
        roots[0] = keccak256("any");
        vm.prank(owner);
        t.setLayout(5, sizes, roots); // reserve 1..5, pool 6..8, general 9..100 ; NOT sealed
    }

    function test_sweepRequiresSealedLayout() public {
        assertFalse(t.poolsSealed());
        bool blocked;
        vm.prank(owner);
        try t.endSale() {} catch { blocked = true; }
        if (!blocked) {
            vm.prank(owner);
            try t.sweepGeneral(owner, 10) {} catch { blocked = true; }
        }
        assertTrue(blocked, "minting through a sweep must not be possible on an unsealed layout");
    }
}
```

### 3. Low: setRenderer accepts a codeless or reverting renderer and freezeMetadata does not check it: freezing with a dead renderer makes tokenURI revert permanently for every token

`src/WeirTownies.sol:317`

```
    function freezeMetadata() external onlyOwner {
        metadataFrozen = true;
        emit MetadataFrozen();
    }
```

tokenURI (line 276) performs an external call renderer.tokenURI(tokenId) whenever renderer is non-zero. setRenderer (line 324) accepts any address, including one with no code (an EOA, a typo, a not-yet-deployed address): the call then returns empty data and the ABI decoder reverts, so tokenURI reverts for every id. The owner can normally repair this with setRenderer(address(0)), but freezeMetadata (line 317) is one-way and performs no validation of the current renderer, after which setRenderer and setBaseURI both revert MetadataIsFrozen and no marketplace can ever display any Townie. Two owner transactions are needed, both against documented intent, so low; reported because the result is irreversible and cheap to guard against. Merged from the math, flow and economics specialists. Minimal fix: in setRenderer require `r == address(0) || r.code.length > 0`; in freezeMetadata, when renderer != 0 and totalSupply() > 0, require that renderer.tokenURI(tokenByIndex(0)) succeeds (try/catch). Also document that freezing pins the pointer, not the content: a renderer with its own admin or upgrade path, or an HTTP base URI, can still change what sold tokens resolve to after the freeze.

**Reproduction**

Owner: setLayout(1, [], []); sealPools(); setBaseURI('https://x/'); ownerMint(owner, 1); tokenURI(1) == 'https://x/1'. Owner: setRenderer(0x000000000000000000000000000000000000dEaD) (no code) -> expected: revert or refuse; actual: succeeds. tokenURI(1) -> reverts (empty return data cannot be decoded as string). Owner: freezeMetadata() -> expected: revert because the renderer does not answer; actual: succeeds. Owner: setRenderer(address(0)) -> revert MetadataIsFrozen; setBaseURI('https://y/') -> revert MetadataIsFrozen. tokenURI(1) now reverts for the lifetime of the contract. Verified with test/scratch/Judge.t.sol::test_C_rendererWithoutCodeThenFreeze (passes on this code).

### 4. Info: Owner trust assumptions that survive the sale (documented, not bypasses): roots, prices, royalty, treasury, renderer and sweeps stay owner-mutable; Merkle leaf binds only the address

`src/WeirTownies.sol:153`

```
    function setPoolRoot(uint256 poolIndex, bytes32 root) external onlyOwner {
        Pool storage p = _pools[poolIndex];
        p.root = root;
        emit PoolSet(poolIndex, p.start, p.size, root);
    }
```

Recorded for the trust model the brief asked to be checked ('owner powers after the sale'); none of these moves, burns or re-mints a sold token, and all are consistent with the README. (1) setPoolRoot (line 153) and setAllowlistRoot (line 305) have no phase, seal or saleEnded gate: before endSale the owner can replace a root with a one-leaf tree of their own wallet and claim unclaimed pool ids or free allowlist ids. (2) setPrices (line 299) is ungated; strict msg.value == price*qty (line 228) means a change can only make a pending user transaction revert, never overcharge it. (3) setRoyalty (line 342) can raise ERC-2981 royalties on already-sold tokens from 5% to the 10% cap at any time, and setTreasury (line 335) redirects both withdrawals and royalties; withdraw is callable by anyone, so proceeds land at whichever treasury is current, and if the treasury is a contract whose receive reverts every withdraw() reverts TransferFailed until setTreasury is changed. (4) endSale may be called at any moment, after which sweepGeneral/sweepPool hand every unsold id to an owner-chosen address. (5) freezeMetadata pins only the pointer: an upgradeable renderer or an HTTP base URI can still change content afterwards. (6) The Merkle leaf is keccak256(bytes.concat(keccak256(abi.encode(address)))) with no pool index, contract or chain id; the double hash correctly prevents an interior node from being passed as a leaf and a proof for one root is rejected by a pool with a different root, but if two pools (or a pool and the general allowlist) are given the same root, one wallet claims from each with the same proof, since roleClaimed is keyed by pool index. That is a requirement on the app's root-building step rather than a contract defect; optionally include the pool index in the leaf. Checked and found clean in this review: layout arithmetic (ranges tile with no gaps, next - 1 <= MAX_SUPPLY, generalSize >= 0, cursors strictly increasing per range, OpenZeppelin _mint rejects any existing id so no id is minted twice); the per-pool claim flag and the shared WALLET_CAP across allowlist and public with widened arithmetic; nonReentrant on every _safeMint path and on withdraw with counters advanced before the receiver callback (a receiver re-entering withdraw or mintPublic is blocked, test/scratch/Judge.t.sol::test_clean_reentrancyBlocked); withdraw pays only the current treasury, reverts on zero, and there is no receive/fallback; renounceOwnership reverts and ownership moves in two steps.

**Reproduction**

Owner: setLayout(0, [1, 1], [R, R]) with R = keccak256(bytes.concat(keccak256(abi.encode(w)))) for a wallet w (single-leaf tree), sealPools(), setAllowlistRoot(R), setPhase(Allowlist). From w with an empty proof: mintRole(0, []) mints id 1, mintRole(1, []) mints id 2, mintAllowlist(3, []) mints 3..5 -> balanceOf(w) == 5 where a reader of 'one per wallet' expects fewer. royaltyInfo(1, 1 ether) returns (treasury, 0.05 ether); after endSale() the owner calls setRoyalty(1000) and royaltyInfo(1, 1 ether) returns 0.1 ether on an already-sold token. Both permitted by design. Verified with test/scratch/Judge.t.sol::test_D_royaltyRaisedAfterSaleAndSharedRootAcrossPools.

---

Judge's submission `9ebc773d35e7304c17703519df2af19cd834a287c3b3b992999800e17d47e7b9`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
