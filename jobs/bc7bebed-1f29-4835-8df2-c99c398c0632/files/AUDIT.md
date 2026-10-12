# Audit report

> SECURITY AUDIT — BMC ILLUMINATI PASS V3
>
> Repository:
> https://github.com/0xSt3w/launch-1356-project-bmc-illuminati-pass
>
> Branch: security/vrf-recovery
>
> Primary contract:
> src/experimental/BMCIlluminatiPassCandidateV3.sol
>
> Tests:
> test/BMCIlluminatiPassCandidateV3.t.sol
>
> Deployment simulation:
> script/DeployBMCIlluminatiPassV3DryRun.s.sol
>
> Perform an adversarial, read-only security audit of Candidate V3 before Ethereum Mainnet deployment.
>
> Review:
> 1. Chainlink VRF v2.5 integration, gas lane, subscription configuration and coordinator compatibility.
> 2. Single-request randomness design and permanent reveal-stall risks.
> 3. BMC burnFrom accounting, irreversible token burns and reentrancy.
> 4. Genesis and Standard NFT rarity distribution and inventory uniqueness.
> 5. Sale deadlines, early closure and unsold NFTs.
> 6. Genesis IPFS metadata integrity and immutability.
> 7. Constructor permissions, deployment safety and potential denial of service.
>
> Run Foundry tests, adversarial tests and Ethereum Mainnet fork checks where possible.
>
> Produce a security report with severity-ranked findings, exact source locations, reproduction steps, recommended fixes and a clear Mainnet readiness verdict.
>
> IMPORTANT: Audit only. Do not modify files, deploy contracts, broadcast transactions, sign messages or initiate additional paid jobs. Do not claim independent certification.
>
> The existing tests report 80 passed, 0 failed. Verify these results independently.

| | |
|---|---|
| Repository | https://github.com/0xSt3w/launch-1356-project-bmc-illuminati-pass.git |
| Commit | `17aa38676fce6025a2d18cc705542e8a88c1157f` |
| Job | `bc7bebed-1f29-4835-8df2-c99c398c0632` |
| Judged | 2026-10-12 14:28 UTC |
| Findings | 2 high · 2 medium · 7 low · 3 info |

Four agents audited the code as it is at `17aa386`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: V3: the sole VRF seed request is permissionless and non-retryable; an expired or never-fulfilled request leaves every mystery token Pending forever

`src/experimental/BMCIlluminatiPassCandidateV3.sol:255`

```
        require(seedRequestId == 0, "seed already requested");
```

Tree note: this file exists only on branch security/vrf-recovery (commit bf2a63c), the branch the audit was commissioned for; the pinned checkout (17aa386, main) has no src/experimental/. Line 255 and the snippet were re-verified against the branch blob on 2026-10-12 (git show origin/security/vrf-recovery:src/experimental/BMCIlluminatiPassCandidateV3.sol). The attached proof compiles and fails only on that branch ('seed already requested'); on the pinned main tree it cannot compile because the import target is absent, so it cannot drive a revision here. The in-tree counterpart of this defect class (no retry for an unfulfilled VRF request in src/BMCIlluminatiPass.sol) is reported separately as the production-contract finding at src/BMCIlluminatiPass.sol:321. Scope note: the pinned checkout (17aa386, main) does not contain src/experimental/* or the V3 tests; this finding refers to branch security/vrf-recovery at commit bf2a63c, reproduced in a separate worktree of that commit. requestSeed() succeeds exactly once: after seedRequestId is set, line 255 reverts 'seed already requested' for the life of the contract, and rawFulfillRandomWords() only accepts that one id. finalizeReveals() requires seedReceived, so all sold mystery tokens (up to 460, 161,000,000 BMC burned irreversibly through burnFrom) depend on one external fulfilment. Chainlink VRF v2.5 does not keep requests alive indefinitely: the subscription docs (docs.chain.link/vrf/v2-5/overview/subscription, fetched 2026-10-12) state 'If your balance is below the minimum, your requests remain pending for up to 24 hours before they expire.' The coordinator does not check the balance at request time: on a mainnet fork at block 26176938, once the subscription owner adds the pass as consumer, requestRandomWords succeeds although subscription 2785...2985 holds 0 LINK and 0.02 ETH native (minimum for the 500 gwei lane at 500k callback gas is ~0.434 ETH). Because requestSeed is callable by anyone the moment block.timestamp >= saleDeadline (or by the 500th minter from inside onERC721Received), the operator cannot sequence 'fund, then request'; a griefer or eager holder can fire the request into an underfunded subscription, or during a gas spike above the lane cap lasting more than 24h, and the request expires. The coordinator then keeps the pending commitment (cancelSubscription reverts PendingRequestExists, verified on the fork), so the subscription cannot even be recycled. The header comment acknowledges the risk ('A permanently unfulfilled request may permanently prevent reveals') and test_OnlyOneSeedRequestEvenAfterSevenDays enshrines it as expected behaviour, so relaxing the single-request rule is a scope decision; but shipping it to mainnet means a single missed 24h window destroys the reveal for every buyer. Merged from audit_math (2be12ea3), audit_flow (b7224882) and audit_permissions (0840ae1c); the two attached proofs both fail on this code with 'seed already requested'. Fix (keeps first-delivered-word-is-permanent): store seedRequestedAt; allow requestSeed() again when !seedReceived && block.timestamp >= seedRequestedAt + TIMEOUT (e.g. 2-7 days); record every issued id in mapping(uint256 => bool) issued and accept delivery for any issued id, keeping the first word (the seedReceived guard already does this). Optionally restrict the first request window to the owner so funding can be verified before the request is made.

**Reproduction**

State: 40 Genesis + 5 mystery minted (1,750,000 BMC burned for ids 41-45), block.timestamp >= saleDeadline. 1) anyone calls requestSeed() -> seedRequestId = R. 2) the subscription is below Chainlink's minimum; the node never fulfils R and drops it after 24h. 3) 7 days later anyone calls requestSeed(). Expected: a fresh request can be opened (or any recovery path exists) so tokens 41-45 can be revealed. Actual: revert 'seed already requested'; finalizeReveals(10) reverts 'seed pending'; tierOf(41..45) == Pending and revealStatusOf == AwaitingRandomness forever. Run: forge test --match-path test/scratch/V3SeedRequestStall.t.sol on branch security/vrf-recovery -> FAIL 'seed already requested'. Re-run 2026-10-12 in a worktree of bf2a63c: Proof_0840ae1c8a6c and Proof_b72248823b93 both FAIL 'seed already requested'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC20Burnable} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import {VRFV2PlusClient} from "@chainlink/contracts/src/v0.8/vrf/dev/libraries/VRFV2PlusClient.sol";
import {BMCIlluminatiPassCandidateV3} from "src/experimental/BMCIlluminatiPassCandidateV3.sol";

/// @dev Self-contained BMC stand-in: 18 decimals, OpenZeppelin burnFrom semantics.
contract ProofBMC is ERC20, ERC20Burnable {
    constructor() ERC20("BMC Illuminati", "BMC") {}

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

/// @dev Minimal VRF v2.5 coordinator stand-in with a registered proving key and request expiry.
///      `expire` models the Chainlink node dropping a request that stayed unpaid for 24 hours
///      (docs.chain.link, VRF v2.5 subscription overview: "requests remain pending for up to
///      24 hours before they expire"). An expired request is never delivered.
contract ProofCoordinator {
    bytes32 public constant VALID_KEY = keccak256("registered-key");

    struct Req {
        address consumer;
        uint32 callbackGasLimit;
        bool fulfilled;
        bool expired;
    }

    uint256 public nextRequestId = 1000;
    mapping(uint256 => Req) public requests;

    function s_provingKeys(bytes32 key) external pure returns (bool exists, uint64 maxGas) {
        return (key == VALID_KEY, key == VALID_KEY ? uint64(500 gwei) : uint64(0));
    }


    function getSubscription(uint256)
        external
        view
        returns (uint96 balance, uint96 nativeBalance, uint64 reqCount, address owner, address[] memory consumers)
    {
        return (0, 1 ether, 0, address(this), new address[](0));
    }

    function requestRandomWords(VRFV2PlusClient.RandomWordsRequest calldata req) external returns (uint256 id) {
        id = nextRequestId++;
        requests[id] = Req({consumer: msg.sender, callbackGasLimit: req.callbackGasLimit, fulfilled: false, expired: false});
    }

    function expire(uint256 requestId) external {
        requests[requestId].expired = true;
    }

    function fulfill(uint256 requestId, uint256 word) external returns (bool ok) {
        Req storage r = requests[requestId];
        require(r.consumer != address(0), "unknown request");
        require(!r.fulfilled && !r.expired, "cannot fulfil");
        r.fulfilled = true;
        uint256[] memory words = new uint256[](1);
        words[0] = word;
        (ok,) = r.consumer.call{gas: r.callbackGasLimit}(
            abi.encodeWithSignature("rawFulfillRandomWords(uint256,uint256[])", requestId, words)
        );
    }
}

/// @title Proof: the sole seed request has no recovery path once the Chainlink node drops it.
/// @notice Fails on the current code: after the only request expires unfulfilled, every one of the
///         sold mystery tokens stays pending forever and `requestSeed()` reverts with
///         "seed already requested". Passes once the contract allows a fresh request for an
///         unfulfilled seed after a liveness timeout (first delivered word still permanent).
contract V3SeedRequestStallProof is Test {
    uint256 internal constant REREQUEST_TIMEOUT = 7 days;

    ProofBMC bmc;
    ProofCoordinator coord;
    BMCIlluminatiPassCandidateV3 pass;
    address alice = makeAddr("alice");
    uint64 deadline;

    function setUp() public {
        vm.warp(1_800_000_000);
        deadline = uint64(block.timestamp + 30 days);
        bmc = new ProofBMC();
        coord = new ProofCoordinator();
        pass = new BMCIlluminatiPassCandidateV3(
            address(this), address(bmc), address(coord), deadline, 123, coord.VALID_KEY(), 500_000, 3, true, "bafyTestCID"
        );
        bmc.mint(alice, 201_000_000 ether);
        vm.startPrank(alice);
        bmc.approve(address(pass), type(uint256).max);
        for (uint256 i; i < 40; ++i) pass.mintGenesis();
        for (uint256 i; i < 5; ++i) pass.mintMystery();
        vm.stopPrank();
    }

    function test_ExpiredSoleSeedRequestCanBeReplaced() public {
        vm.warp(deadline);
        uint256 first = pass.requestSeed();
        assertEq(pass.seedRequestId(), first);

        // The subscription was not funded in time; the node drops the request after 24h.
        coord.expire(first);
        vm.warp(block.timestamp + REREQUEST_TIMEOUT + 1);
        assertFalse(pass.seedReceived());
        assertEq(pass.revealedCount(), 0);

        // Expected: a liveness path exists and a second request can be opened.
        // Actual (current code): revert "seed already requested"; tokens 41..45 are pending forever.
        uint256 second = pass.requestSeed();
        assertTrue(second != 0 && second != first, "a fresh request must be opened");

        // The replacement request is delivered and finalization proceeds.
        assertTrue(coord.fulfill(second, 777));
        assertTrue(pass.seedReceived());
        pass.finalizeReveals(10);
        assertEq(pass.revealedCount(), 5);
        assertEq(uint256(pass.revealStatusOf(41)), uint256(BMCIlluminatiPassCandidateV3.RevealStatus.Revealed));
    }
}
```

### 3. High: Production contract: strict in-order finalization lets one unfulfillable per-token VRF request permanently block every later reveal; NatSpec wrongly claims requests never expire

`src/BMCIlluminatiPass.sol:321`

```
        while (done < maxCount && tokenId <= totalMinted && _revealStatus[tokenId] == RevealStatus.RandomnessStored) {
```

This is the contract in the pinned checkout (17aa386) and the fallback if V3 is not deployed. Each mystery mint opens its own VRF request (mintMystery, line 253) and finalizeReveals() advances only in strict mint order, stopping at the first token whose status is not RandomnessStored (line 321). There is no re-request, timeout or skip, so one request the coordinator never fulfils freezes that token and every token minted after it, even when their own words have already been delivered. Ways a request becomes permanently unfulfillable, none recoverable on-chain: (a) setVRFConfig accepts any non-zero keyHash and VRFCoordinatorV2_5.requestRandomWords deliberately does not validate the key hash ('requests for invalid keyHashes will simply not be fulfilled'), so a mint under a mistyped or retired lane commits a dead request; correcting the config afterwards only affects future requests; (b) the subscription runs dry for more than 24 hours during the 460-request sale: Chainlink's VRF v2.5 docs state 'If your balance is below the minimum, your requests remain pending for up to 24 hours before they expire', which directly contradicts the contract NatSpec at lines 38-39 and README line 64-65 ('requests remain pending while the subscription is unfunded and are fulfilled once it is funded again'); (c) Chainlink deregisters the lane's proving key while requests are pending. Impact: up to 460 pending NFTs (161,000,000 BMC burned) stay 'Pending Reveal' forever; the owner has no power to unblock them. Merged from audit_economics (ce5fcafa, with proof) and audit_permissions (d9951611). The attached proof fails on this code with 'token 42 stuck behind token 41: 2 != 3'. Fix (preserves in-order fairness): record the request timestamp per token; after a bounded window (e.g. 7 days) allow a permissionless retryRequest(tokenId) that issues a fresh request under the current config and maps the new id to the token, accepting only the newest id in rawFulfillRandomWords; or let finalizeReveals skip a token whose request has been stale for the window so delivered successors can finalize. Validate keyHash via s_provingKeys in setVRFConfig (as V3 does at request time) and correct the NatSpec and README.

**Reproduction**

State: Genesis phase complete (tokens 1-40), owner set VRF config with keyHash K1 that the coordinator will never fulfil. 1) alice mints token 41 -> request R1 under K1, 350,000 BMC burned. 2) owner calls setVRFConfig(.., K2 registered, ..). 3) alice mints tokens 42..50 -> R2..R10 under K2. 4) coordinator fulfils R2..R10 -> revealStatusOf(42..50) == RandomnessStored; R1 can never be fulfilled. 5) 30 days later anyone calls finalizeReveals(100). Expected: tokens 42..50 are Revealed, or some path exists to re-request randomness for token 41. Actual: finalizeReveals returns 0, revealedCount stays 0, revealStatusOf(42) == RandomnessStored, and no owner or public function can change that. Run: forge test --match-path test/scratch/ProofMainInOrderStall.t.sol on 17aa386 -> FAIL 'token 42 stuck behind token 41: 2 != 3'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC20Burnable} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import {VRFV2PlusClient} from "@chainlink/contracts/src/v0.8/vrf/dev/libraries/VRFV2PlusClient.sol";
import {BMCIlluminatiPass} from "src/BMCIlluminatiPass.sol";

/// @dev Plain 18-decimal ERC20Burnable, same semantics as mainnet BMC.
contract ProofBMC is ERC20, ERC20Burnable {
    constructor() ERC20("BMC Illuminati", "BMC") {}

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

interface IProofConsumer {
    function rawFulfillRandomWords(uint256 requestId, uint256[] calldata randomWords) external;
}

/// @dev Minimal VRF v2.5 coordinator stand-in. Like the real VRFCoordinatorV2_5, requestRandomWords
///      does NOT validate the key hash ("requests for invalid keyHashes will simply not be fulfilled").
///      Fulfilment is only possible for requests made under the registered lane; a request made under
///      any other key hash (typo, retired gas lane, deregistered proving key) stays pending forever.
contract ProofCoordinator {
    bytes32 public constant REGISTERED_LANE = keccak256("registered lane");
    uint256 public nextRequestId = 1000;
    mapping(uint256 => address) public consumerOf;
    mapping(uint256 => bytes32) public laneOf;

    function requestRandomWords(VRFV2PlusClient.RandomWordsRequest calldata req) external returns (uint256 id) {
        id = nextRequestId++;
        consumerOf[id] = msg.sender;
        laneOf[id] = req.keyHash;
    }

    function fulfill(uint256 requestId, uint256 word) external returns (bool ok) {
        require(laneOf[requestId] == REGISTERED_LANE, "NoSuchProvingKey");
        uint256[] memory words = new uint256[](1);
        words[0] = word;
        (ok,) = consumerOf[requestId].call{gas: 500_000}(
            abi.encodeCall(IProofConsumer.rawFulfillRandomWords, (requestId, words))
        );
    }
}

/// @title Proof: one unfulfillable VRF request permanently stalls every later mystery reveal.
/// @notice Fails on the current code: token 41's request was made under a key hash the coordinator
///         never fulfils; tokens 42..50 have their random words stored, yet finalizeReveals() reveals
///         none of them because it only advances in strict mint order and there is no re-request or
///         timeout for the stuck token. Passes once a token whose own randomness has been delivered
///         can be finalized after its predecessor's request has stayed unfulfilled for a bounded time.
contract ProofRevealStallTest is Test {
    ProofBMC bmc;
    ProofCoordinator coord;
    BMCIlluminatiPass pass;
    address alice = makeAddr("alice");

    function setUp() public {
        vm.warp(1_800_000_000);
        bmc = new ProofBMC();
        coord = new ProofCoordinator();
        pass = new BMCIlluminatiPass(address(this), address(bmc), address(coord));
        pass.setGenesisImagesCID("bafyProofCID");
        // Key hash that the coordinator accepts at request time but will never fulfil.
        pass.setVRFConfig(1, keccak256("retired lane"), 500_000, 3, true);

        bmc.mint(alice, 201_000_000 ether);
        vm.startPrank(alice);
        bmc.approve(address(pass), type(uint256).max);
        for (uint256 i; i < 40; ++i) pass.mintGenesis();
        vm.stopPrank();
    }

    function test_DeliveredTokensRevealDespiteOneStuckRequest() public {
        // Token 41: request committed under the unfulfillable lane (owner typo / lane retired later).
        vm.prank(alice);
        (uint256 stuckToken, uint256 stuckRequest) = pass.mintMystery();
        assertEq(stuckToken, 41);

        // Owner corrects the lane. setVRFConfig only affects future requests (contract doc, line 195).
        pass.setVRFConfig(1, coord.REGISTERED_LANE(), 500_000, 3, true);

        // Tokens 42..50: requests under the registered lane, all fulfilled by the coordinator.
        uint256[9] memory ids;
        for (uint256 i; i < 9; ++i) {
            vm.prank(alice);
            (, ids[i]) = pass.mintMystery();
        }
        for (uint256 i; i < 9; ++i) {
            assertTrue(coord.fulfill(ids[i], uint256(keccak256(abi.encode(i))) ));
        }
        for (uint256 t = 42; t <= 50; ++t) {
            assertEq(uint256(pass.revealStatusOf(t)), uint256(BMCIlluminatiPass.RevealStatus.RandomnessStored));
        }

        // The stuck request can never be fulfilled by the coordinator.
        vm.expectRevert(bytes("NoSuchProvingKey"));
        coord.fulfill(stuckRequest, 1);

        // Thirty days later, anyone tries to finalize. Expected: the nine tokens whose randomness was
        // delivered are revealed. Actual (current code): zero reveals; 3,150,000 BMC burned for tokens
        // 42..50 (and every later mystery mint) stay "Pending Reveal" forever.
        vm.warp(block.timestamp + 30 days);
        pass.finalizeReveals(100);
        assertEq(uint256(pass.revealStatusOf(42)), uint256(BMCIlluminatiPass.RevealStatus.Revealed), "token 42 stuck behind token 41");
        assertEq(pass.revealedCount(), 9, "delivered tokens must be revealable");
    }
}
```

### 2. Medium: VRF key hash and subscription id are accepted without any check against the coordinator: setVRFConfig takes an unregistered lane and mystery mints then burn BMC into requests no node will ever fulfil

`src/BMCIlluminatiPass.sol:204`

```
            subscriptionId == 0 || keyHash == bytes32(0) || callbackGasLimit < MIN_CALLBACK_GAS_LIMIT
```

In the production contract setVRFConfig (lines 196-217) only range-checks its inputs: line 204 rejects subscriptionId == 0 and keyHash == bytes32(0) and bounds the gas and confirmation values, then stores whatever else was passed with configured = true. Nothing asks the coordinator whether keyHash is a registered proving key (VRFCoordinatorV2_5 exposes s_provingKeys(bytes32) for exactly this) or whether subscriptionId exists and lists this contract as a consumer. mintMystery (lines 241-262) likewise burns 350,000 BMC (irreversible burnFrom) and only then calls requestRandomWords. The real coordinator does not validate the key hash at request time ('requests for invalid keyHashes will simply not be fulfilled'), so a mistyped or retired lane produces a request that is accepted, paid for by the buyer's burn, and never served; with an unknown subscription id the request reverts InvalidSubscription so no mint is possible until the owner fixes the config, which is the benign case. The harmful case is the accepted-but-unfulfillable lane: every token minted under it is stuck forever (no re-request exists), and through the strict in-order finalization reported at src/BMCIlluminatiPass.sol:321 it also blocks every later token, so a single owner typo or a lane retired by Chainlink between two mints permanently destroys the reveal for the rest of the collection. The owner can re-point setVRFConfig for future mints but cannot rescue the stuck tokens. The trigger is a privileged misconfiguration rather than an attacker, hence medium; the NatSpec claim that requests simply 'remain pending while the subscription is unfunded' (lines 36-39) understates it. Candidate V3 on branch security/vrf-recovery (bf2a63c, src/experimental/BMCIlluminatiPassCandidateV3.sol line 204, not in the pinned tree) carries the same defect in a worse form: the constructor performs the identical range check, freezes subscriptionId and keyHash with no setter, and the first contact with the coordinator is requestSeed() after the sale has closed and up to 201,000,000 BMC has been burned. Any of (a) unregistered keyHash -> 'unregistered gas lane', (b) unknown subscriptionId -> InvalidSubscription(), (c) the subscription owner (0x83027AD9d0D5374335086c539dADD1db983441B0 on mainnet, an EOA distinct from the contract owner) never calling addConsumer -> InvalidConsumer(subId, pass), or (d) removeConsumer / cancelSubscription before requestSeed (allowed while no request is pending) makes requestSeed revert on every call forever with no remedy for any party. Verified on a mainnet fork (block 26176938) with the exact DryRun constants: deploy, 40 Genesis + 1 mystery (40,350,000 BMC burned) succeed, then requestSeed() reverts InvalidConsumer because the live subscription has 0 consumers; a second fork test where the subscription owner cancels before the deadline ends in a permanent InvalidSubscription(). The branch test test_UnknownGasLaneCannotRequestSeed treats that permanent revert as correct behaviour. Merged from audit_permissions (3a7cd7c7, 430299f3, d9951611 key-hash part) and audit_economics (d80bb015). Fix, production contract: in setVRFConfig staticcall s_provingKeys(keyHash) on VRF_COORDINATOR and revert InvalidVRFConfig unless exists (the attached proof passes with exactly this two-line check); optionally also call getSubscription(subscriptionId) and require address(this) among the consumers so a mint can never burn into a request the coordinator will reject. Fix, V3 (keeps immutability): perform the same s_provingKeys and getSubscription checks in the constructor, and in mintMystery() or requestSeed() require that address(this) is a registered consumer with a non-zero balance before burning; name the subscription owner as a trusted party in the README, or let the contract create and own its subscription (createSubscription + addConsumer(address(this)), fundable by anyone).

**Reproduction**

Production contract, in tree: owner calls setGenesisImagesCID, then setVRFConfig(1, keccak256('typo'), 500000, 3, true) against a coordinator whose s_provingKeys(keccak256('typo')) returns (false, 0). Expected: setVRFConfig reverts (or at least the next mintMystery refuses to burn). Actual: setVRFConfig succeeds; after 40 Genesis mints a buyer's mintMystery() burns 350,000 BMC (totalBurned grows by 350000e18), token 41 is AwaitingRandomness, and the emitted request carries the unregistered key, so no node will ever fulfil it and tokens 42+ are blocked behind it. Run: forge test --match-path test/scratch/ProofMainUnvalidatedKeyHash.t.sol -> FAIL 'mintMystery burned BMC into a VRF request under an unregistered key hash'; with a s_provingKeys check added to setVRFConfig the same test passes (verified in a throwaway worktree). V3, branch only: deploy with keyHash = keccak256('typo-key-hash') or subscriptionId = 999. Expected: deployment reverts. Actual: deployment succeeds; after the sale closes requestSeed() reverts 'unregistered gas lane' (resp. InvalidSubscription()) on every call. Fork: deploy with the DryRun constants, mint 40 Genesis + 1 mystery, warp 30 days, requestSeed() -> InvalidConsumer(27852459...562985, pass). Proof_3a7cd7c7b5f2 re-run on a worktree of bf2a63c on 2026-10-12: two tests FAIL 'next call did not revert as expected'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC20Burnable} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import {VRFV2PlusClient} from "@chainlink/contracts/src/v0.8/vrf/dev/libraries/VRFV2PlusClient.sol";
import {BMCIlluminatiPass} from "src/BMCIlluminatiPass.sol";

/// @dev Plain 18-decimal ERC20Burnable, same semantics as mainnet BMC.
contract ProofBMC is ERC20, ERC20Burnable {
    constructor() ERC20("BMC Illuminati", "BMC") {}

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

/// @dev Minimal VRF v2.5 coordinator stand-in. Like the real VRFCoordinatorV2_5 it exposes the
///      registered proving keys through `s_provingKeys(bytes32)` and does NOT validate the key hash
///      in requestRandomWords ("requests for invalid keyHashes will simply not be fulfilled").
///      A request made under an unregistered key can never be fulfilled.
contract ProofCoordinator {
    bytes32 public constant REGISTERED_LANE = keccak256("registered lane");
    uint256 public nextRequestId = 1000;
    mapping(uint256 => bytes32) public laneOf;

    function s_provingKeys(bytes32 key) external pure returns (bool exists, uint64 maxGas) {
        return (key == REGISTERED_LANE, key == REGISTERED_LANE ? uint64(500 gwei) : uint64(0));
    }

    function requestRandomWords(VRFV2PlusClient.RandomWordsRequest calldata req) external returns (uint256 id) {
        id = nextRequestId++;
        laneOf[id] = req.keyHash;
    }

    function canEverFulfill(uint256 requestId) external view returns (bool) {
        return laneOf[requestId] == REGISTERED_LANE;
    }
}

/// @title Proof: setVRFConfig accepts a key hash the coordinator does not know, so mystery mints burn
///        BMC into VRF requests that can never be fulfilled.
/// @notice Fails on the current code: setVRFConfig(1, keccak256("typo"), ...) succeeds although the
///         coordinator reports the key as unregistered, and the next mintMystery() burns 350,000 BMC
///         and commits a request under that key. Passes once the contract checks the key hash against
///         the coordinator's s_provingKeys (at configuration time, or at the latest before burning in
///         mintMystery) so that no BMC can be burned for an unfulfillable request.
contract ProofUnvalidatedKeyHashTest is Test {
    ProofBMC bmc;
    ProofCoordinator coord;
    BMCIlluminatiPass pass;
    address alice = makeAddr("alice");

    function setUp() public {
        vm.warp(1_800_000_000);
        bmc = new ProofBMC();
        coord = new ProofCoordinator();
        pass = new BMCIlluminatiPass(address(this), address(bmc), address(coord));
        pass.setGenesisImagesCID("bafyProofCID");

        bmc.mint(alice, 201_000_000 ether);
        vm.startPrank(alice);
        bmc.approve(address(pass), type(uint256).max);
        for (uint256 i; i < 40; ++i) pass.mintGenesis();
        vm.stopPrank();
    }

    function test_UnregisteredKeyHashCannotBurnBMCIntoUnfulfillableRequest() public {
        bytes32 typo = keccak256("typo");
        (bool exists,) = coord.s_provingKeys(typo);
        assertFalse(exists, "precondition: coordinator does not know this key");

        // Expected (fixed code): the owner cannot configure a lane the coordinator does not serve.
        try pass.setVRFConfig(1, typo, 500_000, 3, true) {}
        catch {
            return; // rejected at configuration time: nothing can be burned under the bad key
        }

        // Actual (current code): the configuration is accepted. The next mystery mint must then be
        // refused, otherwise 350,000 BMC is burned for a request no node will ever fulfil.
        uint256 burnedBefore = pass.totalBurned();
        vm.prank(alice);
        try pass.mintMystery() returns (uint256 tokenId, uint256 requestId) {
            assertEq(tokenId, 41);
            assertFalse(coord.canEverFulfill(requestId), "request was made under the unregistered key");
            assertEq(pass.totalBurned() - burnedBefore, 350_000 ether, "350,000 BMC burned for it");
            assertEq(uint256(pass.revealStatusOf(41)), uint256(BMCIlluminatiPass.RevealStatus.AwaitingRandomness));
            assertTrue(false, "mintMystery burned BMC into a VRF request under an unregistered key hash");
        } catch {
            // fixed code: the mint refuses to burn under an unregistered key
        }
    }
}
```

### 4. Medium: Dry-run deployment hard-codes a mainnet subscription that has no consumers, 0 LINK and 0.02 ETH, and validates none of it; CI would pass while reveals are impossible

`script/DeployBMCIlluminatiPassV3DryRun.s.sol:25`

```
        require(BMC.code.length > 0 && COORDINATOR.code.length > 0, "missing mainnet contract code");
```

Scope note: the pinned checkout (17aa386, main) does not contain src/experimental/* or the V3 tests; this finding refers to branch security/vrf-recovery at commit bf2a63c, reproduced in a separate worktree of that commit. The only mainnet checks in the script are that the two addresses have code (line 25) and that owner/deadline/CID round-trip. It never reads getSubscription(SUBSCRIPTION_ID) or s_provingKeys(KEY_HASH). Live mainnet state read on 2026-10-12 at block 26176938 via cast on coordinator 0xD7f86b4b8Cae7D942340FF628F82735b7a20893a: getSubscription(27852459...562985) = (balance 0 LINK, nativeBalance 20000000000000000 = 0.02 ETH, reqCount 0, owner 0x83027AD9d0D5374335086c539dADD1db983441B0, consumers []); s_provingKeys(0x3fd2fec1...ff10b) = (true, 500 gwei) so the configured lane is the 500 gwei lane; s_config shows native premium 24%. With nativePayment = true only the native balance counts; Chainlink's documented minimum before a node fulfils is lane max gas x (200,000 verification + callbackGasLimit) x 1.24 = 500 gwei x 700,000 x 1.24 = 0.434 ETH, so the subscription holds 4.6% of what the single fulfilment needs. A V3 deployed with these constants today cannot request randomness at all (InvalidConsumer, see the high finding on validation), and after addConsumer the request would sit pending and expire after 24h (see the high finding on the single request). Running the script against the fork still prints 'Script ran successfully', so the CI step gives no assurance that the deployment can ever reveal. Merged from audit_flow (c492b0c4) and audit_economics (5a85ec2c). Fix: before deploying, fund the subscription with >= 0.5 ETH native (or LINK with nativePayment=false) and add the pass as consumer; extend the script to read getSubscription and s_provingKeys and require owner == expected signer, key exists, and nativeBalance >= laneMaxGas x (200000 + callbackGasLimit) x 124/100, printing the computed minimum.

**Reproduction**

OWNER=0x83027AD9d0D5374335086c539dADD1db983441B0 forge script script/DeployBMCIlluminatiPassV3DryRun.s.sol:DeployBMCIlluminatiPassV3DryRun --fork-url <mainnet> -> 'Script ran successfully'. In the same block: cast call 0xD7f86b4b8Cae7D942340FF628F82735b7a20893a 'getSubscription(uint256)(uint96,uint96,uint64,address,address[])' 27852459484169864437638942739291618120641810244677084392617474192083559562985 -> 0, 20000000000000000, 0, 0x83027AD9d0D5374335086c539dADD1db983441B0, []. Expected: the dry run fails or warns that the subscription has no consumer and 0.02 ETH against a 0.434 ETH minimum. Actual: passes. Fork test: deploy with the script constants, mint 40 Genesis + 1 mystery, warp to the deadline, requestSeed() -> InvalidConsumer; after vm.prank(subscription owner) addConsumer, requestSeed() returns a request id despite the 0.02 ETH balance.

### 5. Low: callbackGasLimit of 500,000 is about nine times the measured V3 callback cost and doubles the subscription balance Chainlink requires before fulfilling

`script/DeployBMCIlluminatiPassV3DryRun.s.sol:37`

```
            500_000,
```

Scope note: the pinned checkout (17aa386, main) does not contain src/experimental/* or the V3 tests; this finding refers to branch security/vrf-recovery at commit bf2a63c, reproduced in a separate worktree of that commit. V3's rawFulfillRandomWords only writes seedReceived and globalSeed and emits one event. Measured with the branch mock: 53,566 gas (a 60,000-gas delivery succeeds). The 500,000 value and the README note that 500k lets each callback finalize up to 4 reveals come from the per-mint design of src/BMCIlluminatiPass.sol and no longer apply. Chainlink reserves laneMaxGas x (200,000 + callbackGasLimit) x 1.24 before a node will fulfil: 0.434 ETH at 500 gwei with 500,000, versus 0.217 ETH with 150,000 (the contract's own MIN_CALLBACK_GAS_LIMIT). The oversized reserve doubles the funding the subscription must hold at close and widens the window in which the single request can expire unfunded. Merged from audit_flow (c492b0c4) and audit_economics (73f12892). Fix: set callbackGasLimit to 150,000 in the script (consider lowering MIN_CALLBACK_GAS_LIMIT toward ~120,000 and the 200 gwei lane 0x8077df51..., also registered on mainnet).

**Reproduction**

Deploy V3, mint 40 Genesis + 460 mystery, requestSeed(), then vm.prank(coordinator) and call rawFulfillRandomWords(req, [777]) measuring gasleft() before/after: 53,566 gas used; coord.fulfillWithGas(req, 5, 60_000) returns true and seedReceived() == true. Required minimum balance with 500,000: 500e9 x 700,000 x 124/100 = 434,000,000,000,000,000 wei; with 150,000: 217,000,000,000,000,000 wei. Expected: callback limit sized to the callback. Actual: 9x oversized.

### 6. Low: Every mystery outcome is publicly computable from globalSeed before finalizeReveals, while tokens still show Pending and trade; V3 dropped V1's inline callback batch

`src/experimental/BMCIlluminatiPassCandidateV3.sol:313`

```
    function finalizeReveals(uint256 maxCount) external returns (uint256 done) {
```

Scope note: the pinned checkout (17aa386, main) does not contain src/experimental/* or the V3 tests; this finding refers to branch security/vrf-recovery at commit bf2a63c, reproduced in a separate worktree of that commit. Once rawFulfillRandomWords stores globalSeed, the tier of every sold mystery token is a pure function of public state (keccak256(abi.encode(globalSeed, tokenId)) % remaining walked in token-id order over the virtual Fisher-Yates), but tierOf()/tokenURI() keep reporting Pending until someone pays for finalizeReveals(): measured 85,300 gas per token, about 39M gas for 460 tokens, so several transactions by an unincentivised caller. In that window an informed buyer who replays _finalize off-chain (or eth_calls finalizeReveals) can buy exactly the 37 future Genesis tokens from holders or marketplace listings priced as mysteries. No outcome can be changed, and the pending metadata warns that 'rarity can be calculated before this metadata is finalized', so this is an information-asymmetry/UX defect rather than a randomness defect. The main-branch contract mitigates it with a gas-aware try this.finalizeReveals(batch) inside the callback; V3 kept CALLBACK_REVEAL_BATCH, GAS_PER_REVEAL and CALLBACK_GAS_RESERVE but no longer uses them. Merged from audit_flow (2e476099), audit_economics (26c15c58) and audit_permissions (58088692). Fix: after storing the seed in rawFulfillRandomWords run the same gas-bounded try this.finalizeReveals(batch) {} catch {} as src/BMCIlluminatiPass.sol lines 307-312, have the deployer finalize the rest in the fulfilment block via a bundle, and/or make tierOf/tokenURI derive the outcome from globalSeed for tokens whose draw is already determined.

**Reproduction**

State: 500 minted, requestSeed() done, coordinator delivers word 0xC0FFEE. Compute r = keccak256(abi.encode(globalSeed, 41)) % 460 off-chain; expected tier = r < 37 ? Genesis : Standard. Observe tierOf(41) == Pending, revealStatusOf(41) == AwaitingRandomness, and transferFrom(alice, 0xBEEF, 41) succeeds. Then finalizeReveals(1): tierOf(41) equals the precomputed tier. Expected: outcomes are reflected on-chain in the delivery transaction (at least a first batch) or not knowable before they are on-chain. Actual: all 460 tokens stay Pending and transferable until a third party pays ~39M gas.

### 7. Low: requestSeed() closes the sale and fires a paid VRF request even when no mystery token exists

`src/experimental/BMCIlluminatiPassCandidateV3.sol:252`

```
    function requestSeed() external returns (uint256 requestId) {
        if (!saleClosed) closeSale();
        require(!seedReceived, "seed already received");
        require(seedRequestId == 0, "seed already requested");
```

Scope note: the pinned checkout (17aa386, main) does not contain src/experimental/* or the V3 tests; this finding refers to branch security/vrf-recovery at commit bf2a63c, reproduced in a separate worktree of that commit. If the deadline passes with totalMinted <= 40 (Genesis phase incomplete or nothing sold), the mystery phase never opened and there is nothing to reveal, yet any address can call requestSeed(): it closes the sale, passes the s_provingKeys check and sends a real requestRandomWords, charging the subscription the fulfilment cost (gas x 1.24 premium, up to ~0.17 ETH at the 500 gwei lane cap) for a word finalizeReveals() will never use (the loop body never runs because tokenId 41 > totalMinted). The one-shot request slot is consumed and the coordinator keeps a pending commitment that blocks cancelSubscription until fulfilled. Merged from audit_flow (cd0fac2c), audit_economics (e5bca14a) and audit_permissions (c3087eba). Fix: require(totalMinted > GENESIS_PHASE_SUPPLY, 'nothing to reveal') in requestSeed().

**Reproduction**

Deploy with a 30-day deadline; mint 10 Genesis; warp to the deadline; anyone calls requestSeed(). Expected: revert, no request. Actual: coordinator.nextRequestId increments (request made and billed at fulfilment), saleClosed == true, seedRequestId set; after fulfilment finalizeReveals(100) returns 0 and pendingReveals() == 0.

### 8. Low: Supply and inventory views ignore sale closure: unsold positions and undrawn outcomes are reported as available after the sale has ended

`src/experimental/BMCIlluminatiPassCandidateV3.sol:393`

```
        return totalMinted < GENESIS_PHASE_SUPPLY ? MYSTERY_SUPPLY : MAX_SUPPLY - totalMinted;
```

Scope note: the pinned checkout (17aa386, main) does not contain src/experimental/* or the V3 tests; this finding refers to branch security/vrf-recovery at commit bf2a63c, reproduced in a separate worktree of that commit. remainingSupply() (line 384), remainingMysteryMints() (line 393), remainingMysteryGenesis() (line 403) and remainingMysteryStandard() (line 407) check only totalMinted/revealedCount, while currentPrice() and genesisPhaseActive() also check saleClosed and saleDeadline. After the deadline or closeSale() these views report inventory that can never be minted and outcomes that can never be drawn. website/app.js reads remainingSupply, remainingMysteryGenesis and remainingMysteryStandard to display supply and remaining-inventory odds, so a closed sale shows live inventory to buyers and integrators. Merged from audit_math (2d6eca3b), audit_flow (68c7b089) and audit_permissions (28a7f101). Fix: return 0 from remainingSupply/remainingMysteryMints when saleClosed || block.timestamp >= saleDeadline, and either document that remainingMysteryGenesis/Standard count undrawn outcomes or return 0 once the sale is closed and all sold tokens are finalized.

**Reproduction**

Mint 40 Genesis + 46 mystery (ids 41-86), warp to the deadline, requestSeed(), fulfil with word 42, finalizeReveals(100) -> 46 finalized, mysteryGenesisRevealed == 3. Expected: remainingSupply() == 0 and remainingMysteryMints() == 0 (sale is over), consistent with currentPrice() == 0 and mintMystery() reverting SoldOut. Actual: remainingSupply() == 414, remainingMysteryMints() == 414, remainingMysteryGenesis() == 34, remainingMysteryStandard() == 380 forever. Also: 39 Genesis minted and warp past the deadline -> remainingMysteryMints() == 460, remainingSupply() == 461 while currentPrice() == 0.

### 9. Low: Partial sell-through: the reveal draws from the full 460-slot pool, so the fixed metadata claim of 77 Genesis / 423 Standard is false whenever the sale closes short

`src/experimental/BMCIlluminatiPassCandidateV3.sol:459`

```
                : "A Genesis BMC Illuminati Pass. A mysterious cartoon frog in a black hooded cloak with premium gold-and-black styling, a glowing golden third eye and a floating golden eye-in-triangle. One of 77 Genesis pieces in a 500-piece collection minted by permanently burning BMC.",
```

Scope note: the pinned checkout (17aa386, main) does not contain src/experimental/* or the V3 tests; this finding refers to branch security/vrf-recovery at commit bf2a63c, reproduced in a separate worktree of that commit. _finalize always draws from remaining = 460 - revealedCount regardless of how many mystery tokens were sold. When the sale closes at the deadline with N < 460 mystery mints, the Genesis outcomes left in the 460 - N unsold slots are never minted, so the number of mystery Genesis that exist is hypergeometric(460, 37, N) rather than 37, and Standard likewise. Yet the permanent on-chain metadata states for every Genesis 'One of 77 Genesis pieces in a 500-piece collection' (line 459) and for every Standard 'One of 423 Standard pieces in a 500-piece collection' (line 485). Each individual draw stays fair at 37/460, so this concerns the supply and rarity claims, not the fairness of the draw. From audit_math (75edb3bf). Fix: either keep the design and make the metadata and views supply-dependent (e.g. 'Genesis supply = 40 + mysteryGenesisRevealed' once reveals finish), or, as an explicit scope decision, shrink the pool to the sold count with a guaranteed Genesis quota (this changes the economics).

**Reproduction**

Mock VRF, seed 42: mint 40 Genesis, then 46 mystery tokens (ids 41-86). Warp to the deadline, requestSeed(), fulfil with word 42, finalizeReveals(100). Expected per the metadata and constants: 77 Genesis in a 500-piece collection. Actual: mysteryGenesisRevealed == 3, so 43 Genesis exist out of totalSupply() 86; tokenURI(2) still decodes to a description containing 'One of 77 Genesis pieces in a 500-piece collection' and a revealed Standard token's description contains 'One of 423 Standard pieces in a 500-piece collection'.

### 10. Low: Mystery phase opens only when all 40 Genesis sell under the same immutable deadline: 39 Genesis sold by the deadline makes all 460 mystery positions permanently unsellable

`src/experimental/BMCIlluminatiPassCandidateV3.sol:232`

```
        if (totalMinted < GENESIS_PHASE_SUPPLY) revert GenesisPhaseNotOver();
```

Scope note: the pinned checkout (17aa386, main) does not contain src/experimental/* or the V3 tests; this finding refers to branch security/vrf-recovery at commit bf2a63c, reproduced in a separate worktree of that commit. mintMystery() requires totalMinted >= 40 (line 232) and Phase 1 shares the single immutable saleDeadline with Phase 2. Nothing extends the deadline or opens Phase 2 early. If Genesis demand stops one short before the deadline, Phase 2 never opens: after the deadline mintGenesis reverts GenesisPhaseOver, mintMystery reverts GenesisPhaseNotOver, closeSale freezes the collection at 39 tokens, and Genesis artworks 40-77 plus all 423 Standard pieces are never minted. From audit_math (4508868c). Fix, preserving the two phases: give Phase 1 its own deadline after which Phase 2 opens (dropping or re-pooling unsold Genesis ids explicitly), or let mintMystery open once block.timestamp >= genesisPhaseDeadline.

**Reproduction**

Deploy with deadline = now + 30 days. Mint 39 Genesis. mintMystery() reverts GenesisPhaseNotOver. Warp 30 days: mintGenesis() reverts GenesisPhaseOver and mintMystery() reverts GenesisPhaseNotOver; closeSale() succeeds with totalMinted == 39. Expected: the mystery phase becomes sellable or the 460 positions are clearly closed. Actual: zero mystery sales are possible while remainingMysteryMints() still returns 460.

### 11. Low: Genesis CID is frozen without format validation; a scheme-prefixed or slash-terminated CID yields permanently broken image URIs for all 77 Genesis tokens

`src/experimental/BMCIlluminatiPassCandidateV3.sol:197`

```
        if (bytes(initialGenesisCID).length == 0) revert EmptyCID();
```

Scope note: the pinned checkout (17aa386, main) does not contain src/experimental/* or the V3 tests; this finding refers to branch security/vrf-recovery at commit bf2a63c, reproduced in a separate worktree of that commit. The constructor rejects only an empty string. tokenURI concatenates 'ipfs://' + genesisImagesCID + '/' + file, so a deployer who passes 'ipfs://<cid>' or '<cid>/' (both common copy-paste forms) locks 'ipfs://ipfs://<cid>//genesis-NN.png' into every Genesis token with no setter to repair it. The CID binds content so pinned bytes cannot be swapped, but availability still depends on off-chain pinning (trust assumption). From audit_permissions (cfc39c83). Fix: reject CIDs containing ':' or '/' and require a plausible prefix/length (bafy... or Qm...), and keep the dry-run assertion that the CID equals the pinned one.

**Reproduction**

Deploy with initialGenesisCID = 'ipfs://bafybeihfihwwpev4gkqjuqawgtptsv3ynzsokclo6odsolvoa65aqaac2u/'; mintGenesis(); base64-decode tokenURI(1): the image field is 'ipfs://ipfs://bafybeihf...aac2u//genesis-01.png' (double scheme, double slash). Expected: constructor reverts. Actual: deployment succeeds and the broken URI is permanent.

### 12. Info: Constructor accepts any closingTime in the future: a far-future or mis-scaled deadline makes a partially sold collection impossible to close, so reveals never start

`src/experimental/BMCIlluminatiPassCandidateV3.sol:191`

```
        require(closingTime > block.timestamp, "deadline must be future");
```

Scope note: the pinned checkout (17aa386, main) does not contain src/experimental/* or the V3 tests; this finding refers to branch security/vrf-recovery at commit bf2a63c, reproduced in a separate worktree of that commit. The deadline is validated only as strictly in the future. closeSale requires totalMinted == MAX_SUPPLY || block.timestamp >= saleDeadline, and requestSeed/finalizeReveals depend on it. A deadline such as type(uint64).max or a value mistakenly given in milliseconds means a sale that does not reach 500 can never close, and every mystery buyer's BMC is burned for a token that stays Pending forever; closingTime = now + 1 gives a sale already over. The dry-run script uses 30 days, but the contract has no guard and the owner has no setters. From audit_math (72b23f38). Fix: bound the deadline in the constructor, e.g. closingTime >= block.timestamp + 1 days && closingTime <= block.timestamp + 365 days.

**Reproduction**

Deploy with closingTime = type(uint64).max. Mint 40 Genesis and 1 mystery, warp 3650 days. requestSeed() reverts 'not closed yet' and finalizeReveals(1) reverts 'seed pending'. Expected: the sale closes and token 41 can be revealed. Actual: token 41 stays Pending after 350,000 BMC was burned.

### 13. Info: Leftover per-mint VRF scaffolding, misleading events and an owner role with no powers; README and website document the V1 API

`src/experimental/BMCIlluminatiPassCandidateV3.sol:237`

```
        emit MysteryMinted(msg.sender, tokenId, 0, MYSTERY_PRICE);
```

Scope note: the pinned checkout (17aa386, main) does not contain src/experimental/* or the V3 tests; this finding refers to branch security/vrf-recovery at commit bf2a63c, reproduced in a separate worktree of that commit. V3 moved to a single post-sale request but kept the per-token scaffolding: requestIdOf, tokenIdOfRequest and _randomWord are never written (public getters always return 0; delete _randomWord[tokenId] in _finalize is a no-op SSTORE on every reveal); RevealStatus.RandomnessStored, event RandomnessStored, event VRFConfigSet, errors GenesisCIDAlreadySet and VRFNotConfigured (configured is always true) and constants CALLBACK_REVEAL_BATCH, GAS_PER_REVEAL, CALLBACK_GAS_RESERVE are unused. MysteryMinted always emits requestId = 0 so indexers keyed on it break, and revealStatusOf reports AwaitingRandomness for tokens minted before any request exists. Ownable is inherited but no function is onlyOwner, so the owner can only transfer/renounce a role with no effect; the README 'Privileged powers' table (setGenesisImagesCID, setVRFConfig) and its claim that VRF keeps unfunded requests pending describe V1, not V3. The real privileged party is the VRF subscription owner (see the high finding on validation). Merged from audit_flow (96d291c1), audit_economics (ec44146c, 1b37b5b6). Fix: remove or document the dead members, drop the requestId field from MysteryMinted, add a status value for 'sale open, no request yet', and state in the trust model that the owner has no powers and that the subscription owner is trusted.

**Reproduction**

Mint 40 Genesis then mintMystery(): the MysteryMinted event carries requestId 0; requestIdOf(41) == 0 and tokenIdOfRequest(x) == 0 for the life of the contract; revealStatusOf(41) == AwaitingRandomness while seedRequestId() == 0. grep onlyOwner src/experimental/BMCIlluminatiPassCandidateV3.sol returns nothing.

### 14. Info: Test results verified: 80 passed is the CI figure excluding the fork test; V3 tests assert the stall and the unregistered lane as expected behaviour and never run against Chainlink's official mock or

`test/BMCIlluminatiPassCandidateV3.t.sol:82`

```
    function test_OnlyOneSeedRequestEvenAfterSevenDays() public {
```

Scope note: the pinned checkout (17aa386, main) does not contain src/experimental/* or the V3 tests; this finding refers to branch security/vrf-recovery at commit bf2a63c, reproduced in a separate worktree of that commit. Independent run (forge 1.8.3, solc 0.8.26): on branch security/vrf-recovery plain forge test reports 81 tests, 80 passed, 1 failed; the failure is test/BMCMainnetFork.t.sol which requires chainid 1 and passes with --fork-url (verified against mainnet). On the pinned checkout 17aa386 the figure is 44 tests, 43 passed, 1 failed (same fork test). The '80 passed, 0 failed' claim therefore matches CI's --no-match-contract BMCMainnetForkTest run, not a plain run. Only 9 tests target V3 and none covers the paths where the design fails: test_OnlyOneSeedRequestEvenAfterSevenDays (line 82) asserts that a second request after 8 days reverts and then fulfils the first, i.e. the stall is tested as intended; test_UnknownGasLaneCannotRequestSeed treats a permanent revert as correct. Untested: an expired/never-fulfilled request, a sale closed by deadline with fewer than 460 mystery tokens followed by reveal, requestSeed with zero mystery tokens, views after early close, callback gas, and V3 on a mainnet fork or against Chainlink's own VRFCoordinatorV2_5Mock, which has no s_provingKeys getter (grep count 0), so V3.requestSeed() reverts 'unregistered gas lane' against it; all official-mock tests target src/BMCIlluminatiPass.sol. docs/TEST-RESULTS.md records the 43 V1 tests only. Merged from audit_flow (9a9a6478), audit_economics (151d1201) and audit_permissions (e1775253). Verdict for the requester: V3 is not mainnet-ready while the two high V3 findings stand; the file header itself says NOT FOR DEPLOYMENT.

**Reproduction**

On branch security/vrf-recovery run forge test without an RPC: 'Ran 12 test suites: 80 tests passed, 1 failed (81 total)'; forge test --match-contract BMCMainnetForkTest --fork-url <mainnet> passes. On 17aa386: '43 tests passed, 1 failed (44 total)'. forge test --match-path test/BMCIlluminatiPassCandidateV3.t.sol lists 9 tests; none warps past an unfulfilled request and asserts recovery, none mints fewer than 460 mystery tokens before reveal, none deploys V3 on a fork.

---

Judge's submission `220bdc28adc69b626868313e90323c8fe56a3789d142c30220fe8023857d6083`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
