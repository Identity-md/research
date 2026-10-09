# Audit report

> Audit the Pawn contracts at github.com/identity-md-launches/launch-1031-workflow-frontend-stage-context (main): PawnShop, CollateralVault, LendingPool, LockDiscount, MilestoneBurn and FloorRelay. Focus: can anyone take pool ETH or vault NFTs; oracle verification and the relay (replay, wrong signer, stale answers); the ERC-1271 worker-authorization scope on seats; auction math and the shortfall reserve; lock commitments and release; owner powers and their delays. Rank findings by severity with a concrete fix for each.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1031-workflow-frontend-stage-context.git |
| Commit | `5086b570d5b31c6b1bb783c6dacca178ab2f79bf` |
| Job | `e4a761c2-59b8-4c34-84fc-54fade5f665a` |
| Judged | 2026-10-09 02:30 UTC |
| Findings | 2 medium · 10 low · 4 info |

Four agents audited the code as it is at `5086b57`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: startAuction freezes a stale floor and buyAuction may follow in the same transaction, so a defaulted seat can be taken atomically at an outdated price

`src/PawnShop.sol:396`

```
        loan.auctionFloor = floors[loan.collection].price;
```

pawn() and extend() refuse a floor older than FLOOR_MAX_AGE (26 h), but startAuction() copies floors[collection].price with no freshness check and buyAuction() can be called in the same transaction at elapsed == 0, i.e. at 100% of that stored number. Floors only change when someone pays for a new oracle answer, so after a quiet month the stored price can sit far below the market. Whoever notices this can, strictly after due + GRACE, call startAuction and buyAuction back to back and take the seat at the stale price with no block of public visibility. The borrower loses the surplus a current floor would have returned (surplus = price - principal), and when the stale floor is below principal the pool books the gap as a loss. The README says the auction 'freezes the last stored floor, even if stale', but the shop's own lending rule treats that number as unusable, and the consequence is an instant third-party arbitrage against the borrower. Merged from audit_permissions. Fix (design-preserving): add `if (!floorFresh(loan.collection)) revert StaleFloor();` to startAuction, so a default is priced from a floor the shop would lend against; anyone can refresh it for the existing 0.001 ETH floor bounty. Trade-off: auctions then depend on oracle liveness; if the requester prefers no such dependency, open at max(stored floor, principal * 10000 / ltv) when the floor is stale and forbid buyAuction in the block that started the auction.

**Reproduction**

Lender deposits 5 ETH; floor 1 ETH signed; alice pawns seat #1 at term 0 (principal 0.4 ETH, credited 0.388 ETH). One day later a 0.5 ETH floor is posted and nobody refreshes afterwards. At due + 3 days + 1 s floorFresh() is false (floor is 29 days old). Attacker calls startAuction(id) then buyAuction{value: 0.5 ether}(id, attacker) in one transaction. Expected: startAuction reverts StaleFloor until a fresh floor is posted; with a fresh 1 ETH floor the auction opens at 1 ETH and alice is credited 0.6 ETH surplus. Actual: auctionPrice is 0.5 ETH at elapsed 0, the attacker receives the seat, the pool recovers 0.4 ETH and alice is credited only 0.1 ETH. Reproduced with test/scratch/Proof_fba9bc1cb98d.t.sol (fails: 'next call did not revert as expected').

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {PawnShop} from "src/PawnShop.sol";
import {LendingPool} from "src/LendingPool.sol";
import {LaunchToken} from "src/LaunchToken.sol";
import {OracleAttestation} from "src/OracleAttestation.sol";

contract StaleWETH is ERC20 {
    constructor() ERC20("Wrapped Ether", "WETH") {}

    function deposit() external payable {
        _mint(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external {
        _burn(msg.sender, amount);
        (bool ok,) = msg.sender.call{value: amount}("");
        require(ok);
    }
}

contract StaleSeat is ERC721 {
    constructor() ERC721("Seat", "SEAT") {}

    function mint(address to, uint256 id) external {
        _mint(to, id);
    }
}

/// Atomic start-and-buy of a defaulted seat at a stale stored floor.
contract StaleFloorAuctionTest is Test {
    uint256 constant KEY = 0xA11CE;
    bytes32 constant Q = keccak256("floor question");
    address owner = makeAddr("owner");
    address alice = makeAddr("borrower");
    address bob = makeAddr("lender");
    address attacker = makeAddr("attacker");
    LaunchToken token;
    StaleWETH weth;
    PawnShop shop;
    LendingPool pool;
    StaleSeat nft;
    uint256 nonce;

    function setUp() public {
        vm.chainId(1);
        vm.warp(1_800_000_000);
        vm.deal(alice, 10 ether);
        vm.deal(bob, 10 ether);
        vm.deal(attacker, 10 ether);
        token = new LaunchToken();
        weth = new StaleWETH();
        shop = new PawnShop(owner, address(token), address(weth), vm.addr(KEY));
        pool = shop.lendingPool();
        StaleSeat template = new StaleSeat();
        vm.etch(shop.IDENTITY_COLLECTION(), address(template).code);
        nft = StaleSeat(shop.IDENTITY_COLLECTION());
        vm.startPrank(owner);
        shop.setQuestionHashOnce(address(nft), Q);
        shop.setNewLoansPaused(false);
        vm.stopPrank();
        vm.prank(bob);
        pool.depositETH{value: 5 ether}(bob);
    }

    function _floor(uint256 price) internal {
        OracleAttestation.Attestation memory a;
        a.requestId = keccak256(abi.encode("floor", ++nonce));
        a.chainId = 1;
        a.questionHash = Q;
        a.answerType = 3;
        a.answer = abi.encode(price);
        a.panelSize = 5;
        a.quorum = 4;
        a.agreed = 4;
        a.issuedAt = uint64(vm.getBlockTimestamp());
        a.expiresAt = uint64(vm.getBlockTimestamp() + 26 hours);
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(KEY, shop.attestationDigest(a));
        shop.submitFloor(address(nft), a, abi.encodePacked(r, s, v));
    }

    function test_defaultedSeatCannotBeSeizedAtStaleFloor() public {
        _floor(1 ether);
        nft.mint(alice, 1);
        vm.startPrank(alice);
        nft.approve(address(shop), 1);
        uint256 id = shop.pawn(address(nft), 1, 0); // principal 0.4 ETH against a 1 ETH floor
        vm.stopPrank();

        // A legitimate dip is posted the next day, then nobody refreshes the floor for a month.
        vm.warp(vm.getBlockTimestamp() + 1 days);
        _floor(0.5 ether);
        vm.warp(shop.getLoan(id).due + 3 days + 1);
        assertFalse(shop.floorFresh(address(nft)), "stored floor is 29 days old");

        // Expected: a default cannot be priced from a floor the shop itself refuses to lend
        // against. Actual: anyone starts the auction at the stale 0.5 ETH and buys the seat in
        // the same transaction, leaving the borrower 0.1 ETH instead of the 0.6 ETH a current
        // 1 ETH floor would return.
        vm.startPrank(attacker);
        vm.expectRevert(PawnShop.StaleFloor.selector);
        shop.startAuction(id);
        vm.stopPrank();

        // Once a fresh floor is posted the auction opens at the current valuation.
        _floor(1 ether);
        vm.startPrank(attacker);
        shop.startAuction(id);
        assertEq(shop.auctionPrice(id), 1 ether);
        shop.buyAuction{value: 1 ether}(id, attacker);
        vm.stopPrank();
        assertEq(nft.ownerOf(1), attacker);
        assertEq(shop.claimable(alice), 0.388 ether + 0.6 ether);
    }
}
```

### 2. Medium: Unsold collateral is never re-priced: the auction holds at 50% of the floor captured at auction start forever, including after write-off

`src/PawnShop.sol:415`

```
        return Math.mulDiv(floor, 5000, 10000, Math.Rounding.Ceil);
```

auctionPrice() reads loan.auctionFloor, which startAuction sets once from floors[collection].price (no freshness requirement) and nothing ever updates. After ten days the price is pinned at half of that number for the rest of time. writeOffAuction clears the debt but leaves status = Auction and the same auctionFloor, and the vault only releases through buyAuction, so if the collection's market falls more than 50% after the auction starts (or the captured floor was already stale and high) no rational buyer ever appears: the pool realises 100% of the principal as loss (reserve first, then cumulativeLoss), the PAWN commitment is released, and a seat that still has real market value sits in its vault with no path to liquidity and no owner rescue. Only a floor drop after default is needed; no admin action. Merged from audit_economics and audit_permissions. The README documents the 50% terminal level and 'remains for sale at the original auction curve' but not that the combination can strand recoverable value permanently. Fix (both options change economics and need a scope decision): (a) after writeOffAuction, or once an auction has sat at the terminal price for N days, let anyone call restartAuction(id), which requires floorFresh(loan.collection), sets auctionStarted = block.timestamp and auctionFloor = floors[collection].price, and re-runs the same curve, with proceeds still flowing through receiveRecovery / borrower surplus; or (b) keep declining past day ten (e.g. linearly to 0 by day 40) so the terminal price cannot sit above any market forever.

**Reproduction**

PawnTestBase setup (bob 5 ETH). Submit floor 10 ETH, alice pawns token 1 at term 1 (principal 4 ETH). Warp to due + 3 days + 1 and startAuction (auctionFloor = 10 ETH, fresh at that moment). Submit floor 1 ETH. Warp 40 days and writeOffAuction: cumulativeLoss = 4 ETH. Observed in test/scratch/Judge.t.sol::test_strandedAt50pct: shop.auctionPrice(id) = 5 ETH immediately after write-off and still 5 ETH one year later; nft.ownerOf(1) is still the vault; buyAuction{value: 1 ether} (the real market price) reverts IncorrectPayment. Expected: after write-off the pool can still realise the roughly 1 ETH the seat is worth. Actual: the seat is unsellable forever and the pool recovers nothing.

### 3. Low: Zero-price auction 'sale' while ownerOf misreports permanently strands the seat in its vault and books the full principal as loss

`src/PawnShop.sol:405`

```
        if (!CollateralVault(payable(loan.vault)).holdsCollateral()) return 0;
```

auctionPrice() returns 0 whenever CollateralVault.holdsCollateral() is false at that instant (ownerOf reverts or reports another address). buyAuction() then accepts msg.value = 0 from anyone, sets status = Sold, settles the whole principal as a loss, releases the PAWN commitment and calls vault.release(), which sets released = true and skips delivery. release() is one-shot, the loan is no longer in Auction, and the vault has no other exit path, so if the collection's ownership report was only transiently wrong (a revocation later reversed, a paused or upgrading proxy whose ownerOf reverts for a few blocks, a seizure returned to the holder) the seat comes back to a vault that can never release it. The borrower loses all surplus, the pool books the full principal although the collateral exists again, and the seat is bricked. The README documents zero-price settlement for missing collateral and lists collection ownership reporting as a trust assumption, and the live identity collection has no seizure path, so this is rated low: it needs a collection that can misreport, e.g. an owner-listed collection or a future upgrade. writeOffAuction() already provides the financial settlement path for missing collateral without finalising custody, so the zero-price purchase is not needed for liveness. Fix: in buyAuction revert when !vault.holdsCollateral() (equivalently when price == 0 because collateral is missing); keep writeOffAuction as the immediate financial settlement for missing collateral, so a later return of the seat can still be sold on the original curve and recovered via receiveRecovery. test_seizedNFTZeroPriceBooksGapWithoutPayingIssuer would then use writeOffAuction.

**Reproduction**

Floor 1 ETH, pool 5 ETH from bob. alice pawns seat #1 (term 0, principal 0.4 ETH). Warp due + 3 days + 1 s; startAuction(1). Collection reports ownerOf(1) = issuer (seize). griefer calls buyAuction(1, griefer) with 0 ETH: succeeds, emits CollateralUnavailable, pool records loss 0.4 ETH, loan status Sold, vault.released = true. Collection then reports ownerOf(1) = vault again. Expected: the seat is still saleable on the curve (auctionPrice(1) > 0; a buyer paying it receives the NFT and the pool recovers 0.4 ETH). Actual: auctionPrice(1) reverts NotAuctioning(), buyAuction reverts, and the NFT is held forever by a released vault. Reproduced with test/scratch/Proof_037673e06f2f.t.sol (fails: NotAuctioning()). Note for the fixer: this proof starts its auction 33 days after the last floor; if the stale-floor fix (fresh floor required by startAuction) is applied first, post a fresh floor before startAuction in the fixture, since the proof targets this finding's fix only.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {LaunchToken} from "src/LaunchToken.sol";
import {PawnShop} from "src/PawnShop.sol";
import {LendingPool} from "src/LendingPool.sol";
import {OracleAttestation} from "src/OracleAttestation.sol";

contract ZWETH is ERC20 {
    constructor() ERC20("Wrapped Ether", "WETH") {}

    function deposit() external payable {
        _mint(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external {
        _burn(msg.sender, amount);
        (bool ok,) = msg.sender.call{value: amount}("");
        require(ok);
    }
}

/// Seat collection whose issuer can temporarily reassign (e.g. a revocation later reversed).
contract ZSeat is ERC721 {
    constructor() ERC721("Seat", "SEAT") {}

    function mint(address to, uint256 id) external {
        _mint(to, id);
    }

    function seize(uint256 id, address to) external {
        _update(to, id, address(0));
    }
}

contract ZeroPriceStrandTest is Test {
    uint256 internal constant KEY = 0xA11CE;
    bytes32 internal constant Q = keccak256("floor question");
    address internal owner = makeAddr("owner");
    address internal alice = makeAddr("alice");
    address internal bob = makeAddr("bob");
    address internal griefer = makeAddr("griefer");
    address internal buyer = makeAddr("buyer");
    address internal issuer = makeAddr("issuer");
    PawnShop internal shop;
    LendingPool internal pool;
    ZSeat internal nft;

    function setUp() public {
        vm.chainId(1);
        vm.warp(1_800_000_000);
        vm.deal(bob, 100 ether);
        vm.deal(buyer, 100 ether);
        LaunchToken token = new LaunchToken();
        ZWETH weth = new ZWETH();
        shop = new PawnShop(owner, address(token), address(weth), vm.addr(KEY));
        pool = shop.lendingPool();
        vm.etch(shop.IDENTITY_COLLECTION(), address(new ZSeat()).code);
        nft = ZSeat(shop.IDENTITY_COLLECTION());
        vm.prank(owner);
        shop.setQuestionHashOnce(address(nft), Q);
        OracleAttestation.Attestation memory a;
        a.requestId = keccak256("r1");
        a.chainId = 1;
        a.questionHash = Q;
        a.answerType = 3;
        a.answer = abi.encode(uint256(1 ether));
        a.panelSize = 5;
        a.quorum = 4;
        a.agreed = 4;
        a.issuedAt = uint64(block.timestamp);
        a.expiresAt = uint64(block.timestamp + 26 hours);
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(KEY, shop.attestationDigest(a));
        shop.submitFloor(address(nft), a, abi.encodePacked(r, s, v));
        vm.prank(owner);
        shop.setNewLoansPaused(false);
        vm.prank(bob);
        pool.depositETH{value: 5 ether}(bob);
    }

    function test_transientlyUnreportedSeatCanStillBeAuctionedOnceItReturns() public {
        nft.mint(alice, 1);
        vm.startPrank(alice);
        nft.approve(address(shop), 1);
        uint256 id = shop.pawn(address(nft), 1, 0);
        vm.stopPrank();
        address vault = shop.getLoan(id).vault;

        vm.warp(block.timestamp + 30 days + 3 days + 1);
        shop.startAuction(id);

        // The collection briefly reports another owner (revocation later reversed, upgrade, etc.).
        nft.seize(1, issuer);
        // Anyone can "buy" the auction for zero during that window; today this finalizes the sale.
        vm.prank(griefer);
        try shop.buyAuction(id, griefer) {} catch {}
        // Ownership is restored to the vault.
        nft.seize(1, vault);
        assertEq(nft.ownerOf(1), vault);

        // Expected: the seat is still saleable at the auction curve and the pool recovers principal.
        uint256 price = shop.auctionPrice(id); // currently reverts NotAuctioning: loan is already Sold
        assertGt(price, 0);
        vm.prank(buyer);
        shop.buyAuction{value: price}(id, buyer);
        assertEq(nft.ownerOf(1), buyer);
    }
}
```

### 4. Low: Ratcheted full-principal loss allowance is released in one step on sale, letting a same-block depositor capture the recovery from existing lenders

`src/LendingPool.sol:227`

```
        expectedAuctionLoss -= auctionLoss[id];
```

PawnShop.markAuctionLoss() is permissionless and marks loss = principal - auctionPrice(). If the collateral is momentarily unreported, auctionPrice() is 0 and the full principal is marked. LendingPool.markAuctionLoss() then forbids any decrease (line 220, `if (loss < auctionLoss[id]) revert`), so the over-marked allowance stays deducted from totalAssets() even after the seat is back and saleable. When the seat is later bought at a positive price, settleAuction() removes the whole allowance and adds the recovered ETH in the same transaction, so totalAssets() jumps up immediately instead of vesting like fees, donations and late recoveries do. Anyone can deposit just before buyAuction (or bundle deposit + buyAuction + redeem) and take part of the recovery that belongs to the lenders who bore the marked loss; lenders who exited while the allowance was overstated were also paid too little. In the normal path the curve only declines, so the marked loss never exceeds the realised loss; the jump needs the same transient misreport as the zero-price finding, hence low. Fix: in settleAuction compute the realised loss (principal - msg.value) and, when the released allowance exceeds it, route the difference through _vest() instead of releasing it at once; and/or allow markAuctionLoss to lower the allowance while holdsCollateral() is true so a transient zero reading cannot stick.

**Reproduction**

Same setup (bob 5 ETH, alice's 0.4 ETH loan, shortfallReserve 0 because protocol fees fill the bounty reserve first). After startAuction the collection briefly reports another owner; anyone calls shop.markAuctionLoss(1) -> expectedAuctionLoss = 0.4 ETH, totalAssets = 4.6102 ETH. Ownership returns to the vault. In one block a JIT account calls depositETH{4 ETH}, the buyer calls buyAuction at the curve price (1 ETH; pool recovers 0.4 ETH), totalAssets becomes 9.0102 ETH, and the JIT account redeems all its shares for 4.185826113214559475 ETH. Expected: <= 4 ETH (no same-block gain). Actual: +0.1858 ETH taken from bob. Reproduced with test/scratch/Proof_3d1b940e6a64.t.sol (fails: 4185826113214559475 > 4000000000000000000). Note for the fixer: this proof starts its auction 33 days after the last floor; if the stale-floor fix (fresh floor required by startAuction) is applied first, post a fresh floor before startAuction in the fixture, since the proof targets this finding's fix only.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {LaunchToken} from "src/LaunchToken.sol";
import {PawnShop} from "src/PawnShop.sol";
import {LendingPool} from "src/LendingPool.sol";
import {OracleAttestation} from "src/OracleAttestation.sol";

contract ZWETH is ERC20 {
    constructor() ERC20("Wrapped Ether", "WETH") {}

    function deposit() external payable {
        _mint(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external {
        _burn(msg.sender, amount);
        (bool ok,) = msg.sender.call{value: amount}("");
        require(ok);
    }
}

/// Seat collection whose issuer can temporarily reassign (e.g. a revocation later reversed).
contract ZSeat is ERC721 {
    constructor() ERC721("Seat", "SEAT") {}

    function mint(address to, uint256 id) external {
        _mint(to, id);
    }

    function seize(uint256 id, address to) external {
        _update(to, id, address(0));
    }
}

contract RatchetedLossReleaseTest is Test {
    uint256 internal constant KEY = 0xA11CE;
    bytes32 internal constant Q = keccak256("floor question");
    address internal owner = makeAddr("owner");
    address internal alice = makeAddr("alice");
    address internal bob = makeAddr("bob");
    address internal griefer = makeAddr("griefer");
    address internal buyer = makeAddr("buyer");
    address internal issuer = makeAddr("issuer");
    PawnShop internal shop;
    LendingPool internal pool;
    ZSeat internal nft;

    function setUp() public {
        vm.chainId(1);
        vm.warp(1_800_000_000);
        vm.deal(bob, 100 ether);
        vm.deal(buyer, 100 ether);
        LaunchToken token = new LaunchToken();
        ZWETH weth = new ZWETH();
        shop = new PawnShop(owner, address(token), address(weth), vm.addr(KEY));
        pool = shop.lendingPool();
        vm.etch(shop.IDENTITY_COLLECTION(), address(new ZSeat()).code);
        nft = ZSeat(shop.IDENTITY_COLLECTION());
        vm.prank(owner);
        shop.setQuestionHashOnce(address(nft), Q);
        OracleAttestation.Attestation memory a;
        a.requestId = keccak256("r1");
        a.chainId = 1;
        a.questionHash = Q;
        a.answerType = 3;
        a.answer = abi.encode(uint256(1 ether));
        a.panelSize = 5;
        a.quorum = 4;
        a.agreed = 4;
        a.issuedAt = uint64(block.timestamp);
        a.expiresAt = uint64(block.timestamp + 26 hours);
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(KEY, shop.attestationDigest(a));
        shop.submitFloor(address(nft), a, abi.encodePacked(r, s, v));
        vm.prank(owner);
        shop.setNewLoansPaused(false);
        vm.prank(bob);
        pool.depositETH{value: 5 ether}(bob);
    }

    function test_ratchetedFullLossReleasesUnvestedOnSale() public {
        nft.mint(alice, 1);
        vm.startPrank(alice);
        nft.approve(address(shop), 1);
        uint256 id = shop.pawn(address(nft), 1, 0);
        vm.stopPrank();
        address vault = shop.getLoan(id).vault;
        vm.warp(block.timestamp + 30 days + 3 days + 1);
        shop.startAuction(id);
        emit log_named_uint("reserve", pool.shortfallReserve());
        nft.seize(1, issuer);
        shop.markAuctionLoss(id); // full principal marked
        nft.seize(1, vault);
        emit log_named_uint("expectedLoss", pool.expectedAuctionLoss());
        emit log_named_uint("assetsBefore", pool.totalAssets());
        address jit = makeAddr("jit");
        vm.deal(jit, 4 ether);
        vm.prank(jit);
        uint256 shares = pool.depositETH{value: 4 ether}(jit);
        uint256 price = shop.auctionPrice(id);
        vm.prank(buyer);
        shop.buyAuction{value: price}(id, buyer);
        emit log_named_uint("assetsAfter", pool.totalAssets());
        uint256 out = pool.previewRedeem(shares);
        emit log_named_uint("jitRedeemable", out);
        vm.prank(jit);
        pool.redeemETH(shares, jit, jit);
        assertLe(out, 4 ether, "same-block depositor captured the released allowance");
    }
}
```

### 5. Low: Default losses are recognised only at startAuction, so a lender who watches the floor exits at par and leaves the whole loss to the remaining lenders

`src/PawnShop.sol:397`

```
        lendingPool.markAuctionLoss(id, loan.principal, auctionPrice(id));
```

LendingPool.totalAssets() carries every Active loan at full principal. The first impairment of a defaulted loan is booked here, inside startAuction, which anyone may call only strictly after due + 3 days (GRACE). Between a public floor collapse (submitFloor is permissionless and visible) and that call there is a window of at least three days, and the whole remaining term before it, in which the share price ignores a loss that is already certain from public data. Any lender who watches floors[collection] withdraws at par during that window (maxWithdraw is bounded only by idleAssets), and the entire loss lands on whoever is left. The same gap persists after an auction has started, because expectedAuctionLoss is refreshed only when someone calls markAuctionLoss, and extend() lets an underwater borrower keep a loan Active indefinitely for a weekly fee with no LTV recheck. The README documents that active loans remain at principal and that an earlier withdrawal may avoid a later loss, so this is a known limitation rather than a bypass, and is rated low. Fix (keeps grace, fees and the curve): add a permissionless markOverdue(id) usable from loan.due onward that books principal - min(principal, floors[collection].price / 2) through the existing markAuctionLoss path (keyed by loan id, non-decreasing), so the loss is visible as soon as the loan is late. A short withdrawal cooldown in LendingPool and an LTV check in extend() would close the rest but change lender/borrower UX and need a scope decision.

**Reproduction**

PawnTestBase: bob and buyer each deposit 5 ETH (pool 10 ETH). Floor 10 ETH; alice pawns token 1 at term 1 (principal 4 ETH). Floor 2 ETH is submitted. Warp to loan.due + 1 (overdue, inside GRACE). Observed in test/scratch/Judge.t.sol::test_lenderExitsAtParBeforeAuction: pool.totalAssets() = 10.034 ETH and pool.maxWithdraw(bob) = 5.016999999999999999 ETH; bob withdraws that at par. Warp to due + 3 days + 1 and startAuction: expectedAuctionLoss = 2 ETH and pool.maxWithdraw(buyer) = 1.017 ETH; after the sale at the 1 ETH terminal price buyer's shares are worth 2.017 ETH. Expected: the 3 ETH loss implied by public state is shared 1.5 / 1.5. Actual: bob 0, buyer 3 ETH.

### 6. Low: pawn() takes no minimum-principal or maximum-fee bound, so a floor update that lands first silently changes the loan the borrower committed to

`src/PawnShop.sol:326`

```
        uint256 principal = Math.mulDiv(floors[collection].price, ltv, 10000);
```

pawn(collection, tokenId, termId) carries no parameter binding the borrower to the valuation they saw. Principal and the non-refundable fee (1-10% of principal, taken out of the proceeds) are computed from whatever floors[collection].price is stored when the transaction mines. submitFloor is permissionless and any keeper holding a genuine, newer attestation (anyone can buy one for 0.5 IMD) can land it in front of a pending pawn. If the floor fell, the borrower gets a small loan and a locked seat they must repay to recover, forfeiting the fee and the vault-deployment gas; if the floor rose, they get a much larger loan whose fee is proportionally larger and is kept even if they repay next block. Merged from audit_flow and audit_permissions. Fix: add `uint256 minPrincipal` (and optionally `uint256 maxFee`) to pawn() and revert with a new error if `principal < minPrincipal || fee > maxFee`; or accept the `floorIssuedAt` the caller expects and revert if floors[collection].issuedAt differs. The frontend already reads the floor it displays and can pass it through. Every other rule is preserved.

**Reproduction**

PawnTestBase (floor 1 ETH, term 0 = 30 days / 300 bps). Alice approves the shop intending to borrow 0.4 ETH for a 0.012 ETH fee. Before her pawn mines, a keeper submits a valid attestation with price 10 ETH (issuedAt later than the stored one). Observed in test/scratch/Judge.t.sol::test_pawnNoPrincipalBound: alice's pawn(IDENTITY_COLLECTION, 1, 0) creates a loan with principal 4 ETH and fee 0.12 ETH (she is credited 3.88 ETH). Expected: the transaction reverts or honours a borrower-supplied bound. Actual: the loan opens; repaying it next block costs 4 ETH, so she is 0.12 ETH out of pocket instead of 0.012. The reverse case (0.5 ETH floor landing first) yields principal 0.2 ETH, fee 0.006 ETH, and a net loss of 0.006 ETH plus two transactions' gas to unwind.

### 7. Low: AUCTION_BOUNTY can exceed a small loan's fee, so a borrower profits from a self-default cycle and drains the shared bounty reserve

`src/PawnShop.sol:398`

```
        _payBounty(msg.sender, AUCTION_BOUNTY);
```

startAuction pays 0.002 ETH from bountyReserve to msg.sender with no relation to the loan's size or to who defaulted. The borrower may be that caller, and in buyAuction the surplus price - principal is credited back to the borrower, so a borrower who buys back their own seat pays net exactly principal, which they already received at origination. The cycle (pawn, claim, let it lapse, startAuction, buyAuction at any price, claim) nets AUCTION_BOUNTY - fee and leaves them with the seat. For term 1 (100 bps) that is positive whenever principal < 0.2 ETH (floor < 0.5 ETH), or principal < 0.4 ETH with 20M PAWN locked (50% discount); at MIN_LOAN the fee is 0.0001 ETH against a 0.002 ETH bounty. The reserve is protocol income (15% of fees) plus fundBounties donations and also pays the floor-update bounty, so repeated cycles across many seats or an owner-listed low-floor collection empty it and starve honest keepers. Not profitable today for the identity collection at a floor near 1.9 ETH, but it becomes so after a floor crash or for any collection with a floor under 0.5 ETH. Merged from audit_flow and audit_economics. Fix (keeps the bounty design): pay the bounty in startAuction only if msg.sender != loan.borrower and cap it at min(AUCTION_BOUNTY, principal / 100); or in buyAuction route min(AUCTION_BOUNTY, price - recovered) back into bountyReserve before crediting the borrower surplus so a self-buying defaulter refunds what startAuction paid.

**Reproduction**

PawnTestBase; shop.fundBounties{value: 0.2 ether}(); submit floor 0.025 ETH. alice: approve, pawn(nft, 1, 1) (principal 0.01 ETH, fee 0.0001 ETH), claim; warp to due + 3 days + 1; startAuction(id) from alice; buyAuction{value: auctionPrice(id)}(id, alice); claim. Observed in test/scratch/Judge.t.sol::test_bountyFarm: alice's ETH balance is 0.0019 ETH higher than before the cycle, nft.ownerOf(1) == alice, bountyReserve fell by 0.002 ETH. Expected: a defaulting borrower never ends a cycle with more ETH than they started with. Actual: +0.0019 ETH per cycle; about 100 cycles empty the reserve.

### 8. Low: submitFloor bounds the signature's age but not the answer's block window, so an attestation about an old window is accepted as a fresh floor

`src/PawnShop.sol:293`

```
                || block.timestamp - a.issuedAt > FLOOR_MAX_AGE || a.issuedAt <= floors[collection].issuedAt
```

Freshness is enforced only on a.issuedAt / a.expiresAt (when the oracle signed) and never on a.fromBlock / a.toBlock (what the answer is about). floorFresh() then treats the price as current for 26 hours. docs/review-notes.md item 2 states that the pinned questionHash commits to the resolved block window, so every attestation matching the pinned hash necessarily reports the floor as of that historical window; a freshly issued signature over an old window passes every check. Even with a relative-window question, a re-signed or late-delivered answer with toBlock thousands of blocks in the past is accepted. Lending and auction-start prices can then be based on a floor days or weeks old while the contract reports it as fresh; any oracle purchaser can submit it and the borrower side benefits when the stale price is above market. The docs already flag the window question as unresolved and advise keeping loans paused, so this is a hardening item rather than a bypass. Fix: add `|| a.fromBlock > a.toBlock || a.toBlock + MAX_BLOCK_AGE < block.number` (MAX_BLOCK_AGE about 26 hours of blocks, 7800 on mainnet) to the InvalidAttestation condition, and document that the pinned question must be a standing relative-window question so the hash does not freeze a window.

**Reproduction**

PawnTestBase at block 30,000,000: build _attestation(FLOOR_QUESTION, 10 ether) with a.fromBlock = 1, a.toBlock = 2, a.issuedAt = block.timestamp, a.expiresAt = issuedAt + 26 hours, sign with the shop's signer and call submitFloor. Observed in test/scratch/Judge.t.sol::test_oldWindowAccepted: it succeeds, floorFresh() returns true, and pawn() lends 4 ETH against it. Expected: an answer whose closing block is older than the freshness window is rejected.

### 9. Low: A shortfall reserve consumed at write-off is never restored when the collateral later sells; the protocol reserve leaks to current lenders

`src/LendingPool.sol:251`

```
    function receiveRecovery() external payable onlyShop nonReentrant {
```

writeOffAuction settles the full principal at zero and _settle covers the gap from shortfallReserve first. When the seat later sells, buyAuction routes min(price, principal) to receiveRecovery, which vests the money to lenders via _receiveIncome; nothing credits shortfallReserve back, even though the loss the reserve paid for has now been recovered in full. The reserve, built from the protocol's 15% fee share (the fee recipient's income), becomes permanent lender profit, the next fees are diverted again to refill it, and the pool is unprotected for the next default until then. The README sends recoveries to lenders by design, so this is an accounting inconsistency rather than a bypass. Fix: record reserveUsed[id] in settleAuction (the covered amount per loan), give receiveRecovery the loan id, and move min(msg.value, reserveUsed[id]) back into shortfallReserve before vesting the remainder.

**Reproduction**

PawnTestBase; the shop forwards 0.3 ETH to pool.addReserve (shortfallReserve = 0.3). alice pawns token 1 at term 1 (principal 0.4 ETH). Warp past due + 3 days, startAuction, warp 40 days, writeOffAuction. Observed in test/scratch/Judge.t.sol::test_reserveNotRestored: shortfallReserve = 0, cumulativeLoss = 0.1 ETH. buyAuction{value: 0.5 ether}: cumulativeRecoveries = 0.4 ETH, shortfallReserve still 0; after 7 days pool.totalAssets() = 5.3034 ETH versus 5 ETH deposited plus 0.0034 ETH fees, i.e. the 0.3 ETH reserve is now lender value. Expected: recovery first repays what the reserve covered (0.3 ETH), then 0.1 ETH vests to lenders.

### 10. Low: invariant_poolBookMatchesCashAndDebt underflows on write-off-then-sale sequences, so the Pawn invariant suite fails spuriously and cannot guard regressions

`test/PawnInvariant.t.sol:186`

```
                - handler.ghostWithdrawals() - pool.unvestedDonations() - pool.cumulativeLoss()
```

The expected-totalAssets expression subtracts unvestedDonations and cumulativeLoss before adding cumulativeRecoveries. After a loan is written off (cumulativeLoss += principal) and then sold (cumulativeRecoveries += principal, which is also unvested for seven days), the running value goes below zero and the checked subtraction panics even though the pool's book is right. forge test on this tree fails: 104 passed, 1 failed. A red invariant test gives no regression protection for the accounting it is meant to pin, and the suite cannot be used as a gate. Fix: reorder so all additions come first: 5 ether + deposits + donations + fees + pool.cumulativeRecoveries() - withdrawals - unvested - cumulativeLoss - (expectedAuctionLoss > reserve ? ... : 0).

**Reproduction**

Run `forge test --match-contract PawnInvariantTest` (default config, fail_on_revert = true). Observed on this tree: invariant_poolBookMatchesCashAndDebt reports `panic: arithmetic underflow or overflow (0x11)` with a shrunk sequence advanceAndPublish, pawn, pawn, advanceAndPublish, repayOrAuction(..., true, ...), repayOrAuction(..., true, ...) (a write-off followed by a sale); the other two invariants pass. Expected: the formula evaluates and equals pool.totalAssets().

### 11. Low: MilestoneBurn fires its irreversible one-shot burn on a single FDV reading up to 26 hours old

`src/MilestoneBurn.sol:53`

```
                || a.agreed > a.panelSize || a.issuedAt > block.timestamp || block.timestamp - a.issuedAt > 26 hours
```

burn() accepts any valid attestation with answer >= 1e24 issued up to 26 hours earlier and consumes the entire vault balance permanently. The configured question (web/src/oracle.ts CAP_QUESTION, docs/SETUP-AND-KEEPER.md) prices FDV from the Uniswap v4 pool's spot price at answer time, so one momentary reading is enough: push the thin PAWN/ETH pool for the block the oracle reads, buy an answer, and submit it any time in the next 26 hours, even after the price has fallen back. The floor feed uses the same window, but there a stale value is replaced the next day; here the action cannot be undone. Fix: shorten the accepted age for burn (e.g. <= 1 hour) and pin a question that uses a time-weighted price, or require two consumed answers separated by a minimum interval that both meet the milestone.

**Reproduction**

At T a signed FDV answer of 1_000_000e18 is issued (issuedAt = T, expiresAt = T + 26h, valid panel) and the vault holds 100 PAWN. At T + 25h 59m burn(a, sig) is called. Observed in test/scratch/Judge.t.sol::test_burnAcceptsOldAttestation: the burn succeeds and moves the whole balance to 0x...dEaD. Expected: the milestone requires a current FDV >= $1M, not a day-old single reading.

### 12. Low: LendingPool.executeDepositCap has no execution window and no cancel, unlike every PawnShop change

`src/LendingPool.sol:330`

```
        if (pendingCapAt == 0 || block.timestamp < pendingCapAt) revert TimelockPending();
```

PawnShop._execute refuses a queued change after queuedAt + EXECUTION_WINDOW (7 days) so a stale payload must be re-queued and re-announced, and the owner can cancel. The pool's cap raise only checks the lower bound and has no cancel, so a cap queued once can be executed by anyone at any later time, long after lenders stopped watching the queue. Cap increases are the pool owner's intended power and only raise the limit, so this is a consistency gap in the delay story rather than a bypass. Merged from audit_flow and audit_economics. Fix: mirror the shop: `if (block.timestamp > pendingCapAt + EXECUTION_WINDOW) revert TimelockPending();` with EXECUTION_WINDOW = 7 days, plus an onlyOwner cancelDepositCap().

**Reproduction**

Owner calls queueDepositCap(1000 ether) at T. Nobody executes. At T + 730 days anyone calls executeDepositCap(). Observed in test/scratch/Judge.t.sol::test_capNoWindow: depositCap becomes 1000 ether. Expected (by analogy with PawnShop.executeTerm, which reverts TimelockPending after T + 48h + 7d): revert.

### 13. Info: CollateralVault.isValidSignature reverts instead of returning 0xffffffff once the seat no longer exists

`src/CollateralVault.sol:123`

```
                || IERC721(collection).ownerOf(tokenId) != address(this)
```

ERC-1271 expects isValidSignature to return the failure value for an invalid signature. The vault calls IERC721(collection).ownerOf(tokenId) unguarded, so once the token is burned or nonexistent the call reverts with ERC721NonexistentToken rather than answering. OpenZeppelin's SignatureChecker treats a revert as invalid, but other ERC-1271 clients (including an off-chain pairing service doing an eth_call) see an error, not a refusal. The vault already has holdsCollateral() with the try/catch for exactly this. The authorisation scope itself is correct: only the single registered WorkerAuthorization digest for this vault and token, while the loan is active and the seat is held, returns the magic value. Merged from audit_flow and audit_permissions. Fix: replace the unguarded ownerOf comparison with `!holdsCollateral()` in isValidSignature.

**Reproduction**

PawnTestBase: alice pawns token 1 (term 0), calls vault.authorizeWorker with wallet = vault, tokenId = 1, a 1-day expiry; vault.isValidSignature(digest, "") returns 0x1626ba7e. Then the collection burns token 1 (nft.seize(1, address(0))). Observed in test/scratch/Judge.t.sol::test_isValidSignatureRevertsAfterBurn: a staticcall to isValidSignature fails with revert data 0x7e273289...0001 (ERC721NonexistentToken(1)). Expected: it returns 0xffffffff.

### 14. Info: buyAuction accepts the loan's own vault as receiver, stranding the seat with no recovery path

`src/PawnShop.sol:443`

```
        if (receiver == address(0)) revert InvalidRecipient();
```

The only receiver validation is non-zero. If a buyer passes the vault address, CollateralVault.release performs transferFrom(vault, vault, tokenId), marks released = true and the loan becomes Sold. After that nothing can move the seat: callFor requires an active loan, release is one-shot, the shop has no rescue function and the vault never approves anyone. The same happens with receiver = collection for most ERC-721s. Self-inflicted (the buyer loses what they paid), so informational, but the guard is one line and the loss is permanent. Fix: `if (receiver == address(0) || receiver == loan.vault) revert InvalidRecipient();` (optionally also `receiver == loan.collection`).

**Reproduction**

PawnTestBase: alice pawns token 1 (term 1); warp to due + 3 days + 1; startAuction(id); buyer calls buyAuction{value: auctionPrice(id)}(id, loan.vault). Observed in test/scratch/Judge.t.sol::test_buyAuctionReceiverVault: succeeds; nft.ownerOf(1) == vault, vault.released() == true, loan status Sold. Expected: revert InvalidRecipient.

### 15. Info: Owner powers and delays (trust assumptions): the one-shot question hash is immediate and can size a single loan to the pool's entire idle ETH; all other valuation levers wait 48 h

`src/PawnShop.sol:240`

```
        c.questionHash = hash;
```

Recorded as the actor and preconditions, not as a bypass; no path was found that changes a timelocked setting without its delay. Immediate owner powers: setNewLoansPaused, disableCollection (also cancels that collection's queued change), cancelChange, and setQuestionHashOnce for a collection whose hash is still zero (the identity collection at launch, enabled in the constructor with 40% LTV and a 100% share limit). The question hash is the single input that prices all collateral; submitFloor accepts any attestation signed by the configured signer (after the FloorRelay switch, any zero-consumer IMD attestation) whose questionHash matches. The owner can therefore pin a question whose genuine uint256 answer is about 2.5x the pool's totalAssets, submit the matching attestation, pawn any seat and borrow the entire idle balance in the same hour, before lenders can react. 48-hour, 7-day-window powers: terms (bounded 7-90 days, 50-1000 bps), collection config including LTV (<= 4000), share, seat flag and hash rotation (rotation zeroes floor expiry so lending pauses until a new matching floor), attester (any address including an owner-controlled ERC-1271 contract; MilestoneBurn mirrors it), fee recipient, discount module. Vault control is limited to the borrower and the immutable shop. The README documents all of this ('initial question selection has no delay'). Merged from audit_flow and audit_economics. Hardening that preserves the design, if the requester wants the delay to cover the first hash: route it through _queue (the keccak256(abi.encode("collection", collection)) kind, which executeCollection already supports) or keep newLoansPaused forced true for DELAY after any hash write; both change the agreed one-shot design and need a scope decision.

**Reproduction**

State: fresh PawnShop, pool holds 10 ETH idle, collections[IDENTITY].questionHash == 0. Owner calls setQuestionHashOnce(IDENTITY, H) and setNewLoansPaused(false) in one block; anyone submits an attestation for H answering 25e18 (chain 1, panel 5, quorum 4, agreed 4, 26 h lifetime). Owner pawns one seat with term 1. Observed in test/scratch/Judge.t.sol::test_oneShotHashSizesLoanToIdle: principal = 25e18 * 4000 / 10000 = 10 ETH, borrow(10 ETH) succeeds, pool.idleAssets() == 0, owner is credited 9.9 ETH. Expected by lenders: a 48-hour window to exit before a valuation change. Actual: none for the first hash.

### 16. Info: Trust gap: every terminal path hard-depends on the loan's discount module not reverting in release()

`src/PawnShop.sol:437`

```
        IDiscountModule(loan.module).release(id);
```

repay (line 363), buyAuction on a non-written-off loan (line 454) and writeOffAuction (line 437) all make an unguarded external call to loan.module.release(id). The module is chosen by the owner through a 48-hour timelock and _validateModule only checks two view functions, so a module whose release() reverts (or consumes all gas) makes every loan opened under it impossible to repay, sell or write off: the seat stays in its vault with released == false, totalBorrowed and collectionDebt never decrease, and only markAuctionLoss still works. The README states 'a malicious discount module can still block its own release call', so this is a documented trust assumption rather than a permission bypass, and the stock LockDiscount cannot revert here (each loan's commitment is released exactly once). Reported because the mitigation is cheap and preserves the design: wrap release in `try IDiscountModule(loan.module).release(id) {} catch {}` on the three terminal paths; a stuck commitment only over-locks that borrower's PAWN, far less harmful than a stuck seat and unrecoverable pool principal.

**Reproduction**

Owner queues and, after 48 h, executes a module whose release(uint256) reverts (commit returns the base fee). alice then pawns seat #1 under it (principal 0.4 ETH). Observed in test/scratch/Judge.t.sol::test_revertingModuleBlocksTerminalPaths: repay{value: 0.4 ether}(id) reverts inside release; after due + 3 days startAuction succeeds, but buyAuction reverts for every buyer and writeOffAuction reverts after 40 days. Expected: alice can always get her seat back by paying principal and the pool can always resolve the loan after default. Actual: seat and principal are stranded permanently.

---

Judge's submission `fdee41842a28306e6933b04d016c4282b2848b6b103a318a21b5ab07cb4e9129`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
