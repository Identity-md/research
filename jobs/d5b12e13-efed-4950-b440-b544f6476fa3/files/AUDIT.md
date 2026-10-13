# Audit report

> Audit the contracts in sudeepb02/imdLend-contracts-public as they are.

| | |
|---|---|
| Repository | https://github.com/sudeepb02/imdLend-contracts-public.git |
| Commit | `a78fa7b3734f42803df5fe8dbaf3d2acca5f0387` |
| Job | `d5b12e13-efed-4950-b440-b544f6476fa3` |
| Judged | 2026-10-13 17:00 UTC |
| Findings | 2 low · 4 info |

Four agents audited the code as it is at `a78fa7b`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: releaseRewards lets the caller pick the split granularity, so small partial releases route the protocol fee and the owner share to the operator

`src/IMDLend.sol:453`

```
        feeAmount = amount * PROTOCOL_FEE / BPS_PRECISION;
        ownerAmount = (amount - feeAmount) * ownerBps / BPS_PRECISION;
        operatorAmount = amount - feeAmount - ownerAmount;
```

releaseRewards (src/IMDLend.sol:259-262) is permissionless and accepts any amount from 1 up to the balance. _calculateSplit rounds the protocol fee down, then rounds the owner share down, and gives the operator whatever remains. Each call loses at most one unit for the fee recipient and one for the owner, but the number of calls is unbounded and the caller chooses it, so the operator (or anyone acting for it) can release a balance in pieces for which the fee and the owner share truncate to zero: any release below 50 units pays no fee at all, and any release where (amount - fee) * ownerBps < 10000 pays the owner nothing. Nothing tracks the dust that was owed, so it is lost for good, and getAvailableRewards reports a split that a sequence of partial releases of the same balance does not pay. For 18-decimal tokens such as IMD the gain per call is 1e-18 of a token against roughly 45k gas, so it is uneconomic there; it matters for a low-decimal or high-unit-value reward token airdropped to the vault, which the contract explicitly supports splitting, and it breaks the documented rule that 2% of every reward goes to the fee recipient. Merged from four specialist reports (audit_flow, audit_economics, audit_permissions, audit_math) of the same mechanism. Minimal fix that keeps partial releases for capped or taxed tokens: in releaseRewards require amount to be either the whole balance or at least BPS_PRECISION units (so each share's rounding error is at most 1/10000 of the release), or compute each payee's share from cumulative released totals so repeated small releases cannot bias the rounding. Rounding the fee up alone is not a fix: with 1-unit releases it moves everything to the fee recipient instead.

**Reproduction**

Deploy the market with any NFT address and a 0-decimal ERC-20; vault = market.deployVault(owner, operator, 5000); mint 100 units of the token to the vault. getAvailableRewards(token) returns (2, 49, 49). As the operator call releaseRewards(token, 1) one hundred times. Expected: fee recipient 2, owner 49, operator 49, the split one releaseRewards(token, type(uint256).max) pays. Actual: fee recipient 0, owner 0, operator 100. Same with 18-decimal units: 1000 units released 1 at a time pay 0 / 0 / 1000 instead of 20 / 490 / 490, and twenty releases of 49 units out of 980 pay the fee recipient 0 instead of 19. Reproduced by running the attached test with forge test --match-path: it fails on this code with "fee recipient got its 2%: 0 != 2"; the two other specialist proofs fail on this code for the same reason ("fee recipient lost its fee: 0 < 19", "protocol fee never paid").

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";

import {IMDLendMarket} from "src/IMDLendMarket.sol";
import {IIMDLend} from "src/interfaces/IIMDLend.sol";

/// @dev Minimal ERC-20 with 0 decimals: one unit is the smallest transferable amount.
contract UnitToken {
    string public constant name = "Unit";
    string public constant symbol = "UNIT";
    uint8 public constant decimals = 0;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function mint(address to, uint256 amount) external {
        balanceOf[to] += amount;
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        return true;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        allowance[from][msg.sender] -= amount;
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        return true;
    }
}

/// @dev Placeholder NFT contract: only its address is needed for the market constructor.
contract DummyNft {
    function ownerOf(uint256) external pure returns (address) {
        return address(0);
    }
}

contract ReleaseRewardsDustTest is Test {
    IMDLendMarket market;
    IIMDLend vault;
    UnitToken token;

    address owner = makeAddr("owner");
    address operator = makeAddr("operator");
    address feeRecipient = makeAddr("feeRecipient");
    uint16 constant OWNER_BPS = 5000; // owner and operator split the post-fee rewards 50/50

    function setUp() public {
        DummyNft nft = new DummyNft();
        token = new UnitToken();
        market = new IMDLendMarket(block.chainid, IERC721(address(nft)), IERC20(address(token)), feeRecipient);
        vault = market.deployVault(owner, operator, OWNER_BPS);
    }

    /// @dev 100 units of rewards split at once: fee 2, owner 49, operator 49.
    /// Released one unit at a time by the operator on the current code: fee 0, owner 0, operator 100.
    function test_oneUnitReleasesRouteEverythingToOperator() public {
        token.mint(address(vault), 100);

        (uint256 feeExpected, uint256 ownerExpected, uint256 operatorExpected) =
            vault.getAvailableRewards(IERC20(address(token)));
        assertEq(feeExpected, 2);
        assertEq(ownerExpected, 49);
        assertEq(operatorExpected, 49);

        // Release one unit at a time. If the fix makes a 1-unit release revert (for example a
        // minimum release amount), fall back to releasing the whole balance, which must split correctly.
        vm.startPrank(operator);
        for (uint256 i = 0; i < 100 && token.balanceOf(address(vault)) > 0; i++) {
            try vault.releaseRewards(IERC20(address(token)), 1) {}
            catch {
                vault.releaseRewards(IERC20(address(token)), type(uint256).max);
            }
        }
        vm.stopPrank();

        assertEq(token.balanceOf(address(vault)), 0, "vault drained");
        // These assertions fail on the current code: the operator ends with all 100 units.
        assertEq(token.balanceOf(feeRecipient), feeExpected, "fee recipient got its 2%");
        assertEq(token.balanceOf(owner), ownerExpected, "owner got its share");
        assertEq(token.balanceOf(operator), operatorExpected, "operator got only its share");
    }
}
```

### 2. Low: A take at the listing's minimum duration parks the seat in the taker's vault: the owner's other open listings become takeable only by that operator, rewards keep splitting after the lending ends, and

`src/IMDLendMarket.sol:218`

```
        address holder = NFT_CONTRACT.ownerOf(listing.tokenId);
        if (holder == listing.owner) {
            NFT_CONTRACT.transferFrom(listing.owner, address(vault), listing.tokenId);
        } else if (holder != address(vault)) {
            revert LibError.NftNotAvailable(listing.tokenId, holder);
        }
```

The market's only floor on a lending is minDuration >= 1 second (src/IMDLendMarket.sol:139) and the upfront amount is pricePerDay * duration / 1 days (src/IMDLendMarket.sol:227), so a take at the shortest duration the owner leaves open is close to free. Once the take lands the seat moves into the vault for (owner, taker, ownerBps) and stays there after the lending is over: the vault splits every token it receives at the fixed terms whether or not a lending is running (src/IMDLend.sol:259-273, documented at src/IMDLend.sol:25-27), and takeListing accepts a seat already in place only for that vault's operator (src/IMDLendMarket.sol:217-223). Until the owner withdraws, three things follow from one cheap take: (1) every reward the network pays the seat's holder is split with the taker at (1 - ownerBps) after the 2% fee, though the taker paid for one second; (2) every other open listing of the owner for that seat reverts with NftNotAvailable for anyone but the taker, and listings with a different ownerBps or naming another operator are dead; (3) the taker can re-take any still-open listing with the same ownerBps in place, with no owner approval or action, for up to that listing's maxDuration, including racing the owner's withdrawNft at endsAt. The owner has an exit, cancelling the remaining listings and then calling withdrawNft (reproduced), and consented to the listed terms, so this is a trust-assumption gap on the owner keeping listings tidy rather than a permission bypass. Merged from audit_flow (1-second take) and audit_permissions (open listing re-taken in place), which describe the same mechanism. Minimal fix that preserves the documented in-place re-take for a named operator: in takeListing accept the in-place path (holder == vault) only when listing.operator == msg.sender, so an open listing created while the seat was in the owner's wallet can be taken only from the wallet; optionally also enforce a protocol floor on minDuration (for example 1 day) or require upfrontAmount > 0. Routing post-lending rewards to the owner would change the documented design and needs a scope decision.

**Reproduction**

test/scratch/Repro.t.sol, test_minDurationTakeParksSeatAndKeepsSplit (passes on this code, showing the behaviour): owner mints seat 5, approves the market, creates two open listings L1 and L2 with ownerBps 5000, pricePerDay 1e18, minDuration 1, maxDuration 30 days. Alice calls takeListing(L1, 1). Expected by the owner: a one-second lending worth 1 IMD per day. Actual: Alice pays 11574074074074 wei, seat 5 is owned by vault(owner, alice, 5000). Two seconds later isNftLent(5) is false but the seat is still in the vault; bob's takeListing(L2, 1 days) reverts NftNotAvailable(5, vault); 100e18 of a reward token sent to the vault and released pays alice 49e18, owner 49e18, fee 2e18; alice then calls takeListing(L2, 1) in place and re-locks the seat with no owner action. test_ownerExitAfterParkedSeat shows the owner's exit: cancelListing(L2) then withdrawNft(5) returns the seat.

### 3. Info: Pairing approval survives into a second lending that starts in the same second the previous one was ended early

`src/IMDLend.sol:358`

```
        if (approval.lendingStartedAt != _lendings[approval.tokenId].startedAt) return 0;
```

getPairingExpiry ties an approval to its lending by comparing the recorded lendingStartedAt with the current lending's startedAt, and the comment in authorizePairing (src/IMDLend.sol:210) says a lending that starts in a later second never revives the approval. A lending started at T, ended early by the operator at T (endLending sets endsAt = T, so isNftLent is false at T) and restarted at T through a second listing in the same block has startedAt == T again, so the earlier approval validates in the new lending. Both lendings are to the same operator, since the vault is per owner, operator and split, so no privilege crosses parties; it is a gap between the stated invariant (an approval belongs to exactly one lending) and the code. If the invariant is wanted, key approvals to a per-token lending counter incremented in startLending instead of to startedAt.

**Reproduction**

test/scratch/Repro.t.sol, test_pairingSurvivesSameSecondRestart: owner lists seat 5 twice for alice (L1, L2). In one block at time T alice takes L1 for 1 day (startedAt T), calls authorizePairing(D, 5, T + 10 min), calls endLending(5), then takes L2 for 1 day (startedAt T again). Expected per the authorizePairing comment: getPairingExpiry(D) == 0 in the new lending. Actual: getPairingExpiry(D) == T + 10 min, and at T + 1 isValidSignature(D, abi.encode(deviceKey, nonce, relayOrigin)) returns 0x1626ba7e.

### 4. Info: createListing does not bound pricePerDay, so a listing whose pricePerDay * duration overflows can never be taken

`src/IMDLendMarket.sol:227`

```
        uint256 upfrontAmount = listing.pricePerDay * duration / 1 days;
```

createListing validates the expiry, the durations and ownerBps but accepts any uint256 pricePerDay. takeListing multiplies pricePerDay by duration in checked arithmetic before dividing by 1 days, so for pricePerDay > type(uint256).max / duration the take reverts with Panic(0x11). The listing is created, emits ListingCreated and looks open, but no duration above the overflow bound is takeable; where pricePerDay * minDuration fits but pricePerDay * maxDuration does not, only the short end of the advertised range works. Only the listing's own owner is affected and the bound is about 3.7e69 wei per day for a 365-day take, so this is a boundary note. Fix: in createListing require pricePerDay <= type(uint256).max / maxDuration so an untakeable listing is rejected at creation.

**Reproduction**

test/scratch/Repro.t.sol, test_pricePerDayOverflowListingUntakeable: createListing(tokenId 5, ownerBps 5000, pricePerDay = type(uint256).max / 1 days + 1, minDuration 1 days, maxDuration 1 days, availableUntil now + 1 day, operator alice) succeeds. Alice calls takeListing(id, 1 days). Expected: the listing is rejected at creation or the take succeeds. Actual: takeListing reverts with Panic(0x11) at the multiplication on line 227.

### 5. Info: An IdentityMD seat pushed into a vault with plain transferFrom by a non-owner can only be recovered by the vault owner

`src/IMDLend.sol:286`

```
        if (msg.sender == address(NFT_CONTRACT)) revert LibError.UnexpectedNft(msg.sender, from, tokenId);
```

onERC721Received refuses IdentityMD seats so they arrive only through the market, but the market moves seats with plain transferFrom and so can anyone else: ERC-721 transferFrom never calls the receiver hook (the deployed IdentityMD contract is a plain Solady ERC-721 with no transfer hook). A seat a third party pushes into a vault (a mis-pasted vault address, or the vault for the wrong owner, operator or split) is not lent, so nothing locks it, but the only exit is withdrawNft, which is owner-only and always sends to OWNER(). The sender has no path to recover it; the vault owner receives it. This is a user-error surface rather than a permission bypass, reported because the receiver guard suggests a protection the plain-transfer path does not give. Minimal mitigation is documentation and a front-end warning; an on-chain owner-only returnNft(tokenId, to) for seats never lent in the vault changes the security-model table and needs a scope decision.

**Reproduction**

test/scratch/Repro.t.sol, test_thirdPartyPushOnlyOwnerRecovers: vault V = market.deployVault(owner, alice, 5000). Bob holds seat 2 and calls nft.transferFrom(bob, V, 2). Expected from the receiver guard's intent: the transfer is refused or bob can recover seat 2. Actual: the transfer succeeds, bob's withdrawNft(2) reverts NotOwner, and owner's withdrawNft(2) sends seat 2 to owner.

### 6. Info: Repository ships no test suite; the custody, lending, pairing and split edges in the security model are unexercised

`README.md:108`

```
Not audited. The vaults take custody of NFTs, so they need an independent audit before mainnet use.
```

The repository holds contract sources only, the build instructions stop at forge build and forge fmt, and there is no test directory, so none of the behaviours the README's security model promises is checked by a test: a lent seat cannot be withdrawn, the operator cannot move seats, isValidSignature validates only an approved WorkerAuthorization naming the vault within its lending and from the block after it starts, the three reward parts always sum to the amount, the market's approval can only move an owner's seat into that owner's own vault, the two-step fee recipient handover, the off-identity-chain behaviour (createListing and takeListing revert NotIdentityChain while deployVault works), and the boundary cases at endsAt, availableUntil and expiresAt. Merged from audit_flow and audit_permissions. Fix: add a Foundry suite covering those invariants and boundaries plus a fuzz test over _calculateSplit asserting fee + owner + operator == amount.

**Reproduction**

State: at the pinned commit `git ls-files test` prints nothing and `ls test` reports no such directory; `forge test` runs zero project tests. Expected for a custody contract before mainnet: a suite exercising the security-model table in README.md. Actual: none.

---

Judge's submission `f867c28a67f364cd1e912017dd1126508e17b0c9ad87cb5f6cf086ed1841376c`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
