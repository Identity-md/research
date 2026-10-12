# Audit report

> Audit BMC Illuminati PASS Candidate V3 for Ethereum Mainnet readiness.
>
> Primary target: src/experimental/BMCIlluminatiPassCandidateV3.sol
>
> Review Chainlink VRF v2.5 integration, single-request randomness liveness, permanent reveal-stall risk, irreversible BMC burns, NFT rarity fairness, 30-day sale deadline, Genesis IPFS metadata, access control and deployment configuration.
>
> The project previously passed 80 Foundry tests and a V3 deployment simulation.
>
> Identify vulnerabilities by severity, reproduce findings where possible and recommend precise fixes. Clearly distinguish Candidate V3 from older experimental contracts.
>
> Audit only. No modifications or deployment. Perform a comprehensive, read-only smart contract security audit of BMC Illuminati PASS Candidate V3.
>
> Repository: https://github.com/0xSt3w/launch-1356-project-bmc-illuminati-pass
>
> Commit: bf2a63c04d0e73a1a1b9c65a785d921526ec39b0
>
> Contract: src/experimental/BMCIlluminatiPassCandidateV3.sol
>
> Review Chainlink VRF v2.5 randomness, permanent reveal-stall risks, BMC token burns, NFT rarity fairness, sale deadlines, metadata integrity, permissions and deployment configuration.
>
> Verify the existing Foundry tests and report any critical, high, medium or low severity vulnerabilities.
>
> Deliver a written security report with recommended fixes and a Mainnet readiness verdict.
>
> AUDIT ONLY. Do not deploy, broadcast transactions, modify contracts or launch additional paid jobs.

| | |
|---|---|
| Repository | https://github.com/0xSt3w/launch-1356-project-bmc-illuminati-pass.git |
| Commit | `bf2a63c04d0e73a1a1b9c65a785d921526ec39b0` |
| Job | `92daebdf-60c5-433a-851e-a2ff409d92a3` |
| Judged | 2026-10-12 15:12 UTC |
| Findings | 1 high · 2 medium · 4 low · 2 info |

Four agents audited the code as it is at `bf2a63c`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: Single, permissionless, non-retryable VRF seed request: one unfulfilled or expired request permanently stalls every mystery reveal after irreversible BMC burns

`src/experimental/BMCIlluminatiPassCandidateV3.sol:255`

```
        require(seedRequestId == 0, "seed already requested");
```

Candidate V3 (unlike the production src/BMCIlluminatiPass.sol, which requests per mint, and Candidate V2, which allows a timed retry) issues exactly one VRF request for the whole collection. requestSeed() is callable by anyone the moment the sale is sold out or block.timestamp >= saleDeadline, and once seedRequestId is non-zero it can never be called again (line 255). rawFulfillRandomWords accepts only that id, the coordinator, subscription id and key hash are fixed at construction, and there is no timeout, re-request, owner recovery or fallback. The VRF v2.5 coordinator does not check the subscription balance when a request is made; Chainlink's subscription documentation states 'If your balance is below the minimum, your requests remain pending for up to 24 hours before they expire' (the README's claim that an unfunded request is held and fulfilled after funding is wrong beyond that window). So a request fired while the subscription is below the lane minimum and not topped up within 24 hours, a request whose fulfilment transaction fails, or a coordinator or node outage longer than the window leaves seedRequestId != 0 and seedReceived == false forever: finalizeReveals reverts 'seed pending', and every mystery token (ids 41..totalMinted, up to 460 tokens bought with up to 161,000,000 BMC destroyed via burnFrom) stays Tier.Pending with the 'Pending Reveal' metadata permanently. Because the request is permissionless, an outsider rather than the operator decides when the only request is made, for example in the block the deadline passes and before the subscription is funded. The dry-run configuration makes this realistic: on mainnet at block 26177145 the configured subscription holds 0.02 ETH native, 0 LINK and no consumers, while the 500 gwei lane with a 500,000 callback gas limit needs a minimum balance on the order of 0.4 ETH (see the deployment-configuration finding). The contract header acknowledges the stall but does not mitigate it, and test_OnlyOneSeedRequestEvenAfterSevenDays asserts it as intended behaviour. Fix (preserves single-seed fairness, because minting is closed before any request and no participant can act on a request's outcome): record seedRequestedAt and let requestSeed() run again while !seedReceived once block.timestamp >= seedRequestedAt + RETRY_DELAY with RETRY_DELAY longer than 24h (48h to 7 days); either overwrite seedRequestId so a late delivery of a superseded id is rejected by the existing id check, or record every issued id and accept the first word delivered for any of them (Candidate V2's issuedSeedRequests shape; the first delivered word is permanent either way). Defence in depth: before requesting, read VRF_COORDINATOR.getSubscription(subId) (part of the vendored IVRFCoordinatorV2Plus) and revert unless the balance in the asset selected by nativePayment exceeds a configured minimum, so a third party cannot consume the request while it is unpayable; and lower callbackGasLimit (the callback uses under 60k gas) to cut the lane minimum. Re-measure against the 984-byte EIP-170 margin.

**Reproduction**

Proof (forge test --match-path test/scratch/V3SeedLiveness.t.sol): mint 40 Genesis and 460 mystery tokens (201,000,000 BMC burned, minter balance 0); any address calls requestSeed() and gets id R = seedRequestId; the coordinator never delivers R (expired after 24h under-funded, or the fulfilment failed); vm.warp(+31 days); finalizeReveals(1) reverts 'seed pending'; requestSeed() reverts 'seed already requested'. Expected: a fresh request can be issued once the first is clearly dead and reveals proceed. Actual: no code path can ever produce a seed; all 460 tokens stay Tier.Pending. Verified: the specialist proofs Proof_f47f1ecdd235 and Proof_d7c20c60ac57 both fail on bf2a63c with 'seed already requested'; Proof_548cec8ac53c fails because requestSeed() succeeds against a subscription holding 0 of the configured payment asset ('next call did not revert as expected'); scratch test test_A_SecondRequestImpossibleForever shows the same after 365 days with totalBurned == 201,000,000e18 and pendingReveals() == 460. Mainnet reads (cast call on 0xD7f86b4b8Cae7D942340FF628F82735b7a20893a at block 26177145): s_provingKeys(0x3fd2fec1...f10b) = (true, 500 gwei); getSubscription(2785245948...9562985) = (0 LINK, 20000000000000000 wei native, 0 requests, owner 0x83027AD9d0D5374335086c539dADD1db983441B0, consumers []).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {BMCIlluminatiPassCandidateV3} from "src/experimental/BMCIlluminatiPassCandidateV3.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC20Burnable} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import {VRFV2PlusClient} from "@chainlink/contracts/src/v0.8/vrf/dev/libraries/VRFV2PlusClient.sol";

contract ProofBMC is ERC20, ERC20Burnable {
    constructor() ERC20("BMC Illuminati", "BMC") {}

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

/// @dev Coordinator stand-in. Request ids are accepted and recorded, but the first request is
///      never fulfilled: this models a VRF v2.5 request that expired off-chain (Chainlink keeps an
///      unfunded request pending for at most 24 hours, then drops it) or whose callback failed.
contract ProofCoordinator {
    bytes32 public constant KEY = keccak256("lane");
    uint256 public nextId = 1000;
    mapping(uint256 => address) public consumerOf;

    function s_provingKeys(bytes32 key) external pure returns (bool exists, uint64 maxGas) {
        return (key == KEY, uint64(500 gwei));
    }

    function requestRandomWords(VRFV2PlusClient.RandomWordsRequest calldata) external returns (uint256 id) {
        id = nextId++;
        consumerOf[id] = msg.sender;
    }

    function fulfill(uint256 id, uint256 word) external returns (bool ok) {
        uint256[] memory words = new uint256[](1);
        words[0] = word;
        (ok,) = consumerOf[id].call{gas: 500_000}(
            abi.encodeWithSignature("rawFulfillRandomWords(uint256,uint256[])", id, words)
        );
    }
}

/// @title Proof: a single unfulfilled seed request stalls every mystery reveal forever.
/// @notice Fails on the current code: after the only VRF request has gone unfulfilled for a month,
///         `requestSeed()` still reverts "seed already requested", so no seed can ever arrive and
///         `finalizeReveals` reverts "seed pending" for all 460 mystery tokens (161,000,000 BMC
///         already burned). Passes once the contract allows a timed re-request (e.g. `requestSeed()`
///         callable again after a retry delay while `seedReceived` is false, accepting the first
///         word delivered for any request id it issued).
contract V3SeedLivenessProofTest is Test {
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
            address(this), address(bmc), address(coord), deadline, 123, coord.KEY(), 500_000, 3, true, "bafycid"
        );
        bmc.mint(alice, 201_000_000 ether);
        vm.startPrank(alice);
        bmc.approve(address(pass), type(uint256).max);
        for (uint256 i; i < 40; ++i) pass.mintGenesis();
        for (uint256 i; i < 460; ++i) pass.mintMystery();
        vm.stopPrank();
        assertEq(pass.totalMinted(), 500);
        assertEq(bmc.balanceOf(alice), 0); // 201,000,000 BMC burned irreversibly
    }

    function test_SeedCanBeRequestedAgainAfterTheOnlyRequestIsNeverFulfilled() public {
        // Anyone can request the seed the moment the sale is sold out.
        address griefer = makeAddr("griefer");
        vm.prank(griefer);
        uint256 first = pass.requestSeed();
        assertEq(pass.seedRequestId(), first);

        // The request is never fulfilled (expired off-chain after 24h, or callback failed).
        vm.warp(block.timestamp + 31 days);
        assertFalse(pass.seedReceived());
        vm.expectRevert(bytes("seed pending"));
        pass.finalizeReveals(1);

        // Liveness requirement: a new request must be possible once the old one is clearly dead.
        uint256 second = pass.requestSeed();
        assertTrue(second != 0 && second != first, "a fresh request id must be issued");

        // And the fresh request must be able to deliver the seed and unblock reveals.
        assertTrue(coord.fulfill(second, 0xBEEF));
        assertTrue(pass.seedReceived());
        assertEq(pass.finalizeReveals(460), 460);
        assertEq(pass.revealedCount(), 460);
    }
}
```

### 2. Medium: VRF subscription id and key hash are fixed at construction without validation and without any recovery path: a wrong lane, a cancelled subscription or a lost subscription-owner key stalls reveals befo

`src/experimental/BMCIlluminatiPassCandidateV3.sol:204`

```
        vrfConfig = VRFConfig(subscriptionId, keyHash, callbackGasLimit, requestConfirmations, nativePayment, true);
```

The constructor (lines 192-204) only range-checks the VRF parameters; it does not ask the coordinator whether keyHash is a registered proving key or whether subscriptionId exists, and V3 removed setVRFConfig (present in the production contract and still documented in the README). Ownable is inherited but no function is owner-gated, so nothing can ever change vrfConfig. The s_provingKeys probe in requestSeed() (lines 259-262) runs only after the sale closes, and the VRF v2.5 coordinator accepts requests for unknown key hashes without fulfilling them, which is why the probe exists. Three pre-request failures of the fixed configuration are therefore unrecoverable after up to 201,000,000 BMC has been burned: (a) a typo in the 77-digit subscription id or in the key hash at deployment (for example the VRF v2.0 mainnet lane 0xff8dedfb...4f92 instead of the v2.5 lane 0x3fd2fec1...f10b) passes the constructor and the fork dry run, which never calls requestSeed, and surfaces only as 'unregistered gas lane' or InvalidSubscription after the deadline; (b) the subscription owner on the coordinator (mainnet: EOA 0x83027AD9d0D5374335086c539dADD1db983441B0, distinct from the pass contract and outside its stated trust model) calls cancelSubscription during the sale, which the coordinator allows while no request is pending, i.e. during the whole 30-day sale; v2.5 subscription ids are hash-derived, so a replacement can never match the immutable id; (c) that key is lost, so the pass is never added as a consumer (the configured subscription currently has none) and nobody else can add it. Consumer removal or a missing consumer is recoverable, but only by that same key. This is distinct from the single-request stall: here requestSeed() never succeeds, seedRequestId stays 0, and retry logic would not help. Fix: (1) fail fast in the constructor by making the same s_provingKeys staticcall and calling VRF_COORDINATOR.getSubscription(subscriptionId) (reverts InvalidSubscription when it does not exist), reverting InvalidVRFConfig otherwise, and assert both in DeployBMCIlluminatiPassV3DryRun.run(); (2) add a recovery path that cannot bias outcomes because the sale is closed before any request: either an owner-only setVRFConfig callable only while seedRequestId == 0 (emitting the already-declared VRFConfigSet) documented as a trust assumption, or have the contract create and own its subscription in the constructor (createSubscription plus addConsumer(address(this)); anyone can fund it). Option 2 changes the 'VRF config fixed in the constructor' statement in the contract header and needs the requester's decision.

**Reproduction**

Proof (forge test --match-path test/scratch/V3UnregisteredKeyHash.t.sol): deploy V3 against a coordinator whose s_provingKeys reports the v2.0 lane 0xff8dedfbfa60af186cf3c830acbc32c05aae823045ae5ea7da1e45fbfaba4f92 as unregistered. Expected: the constructor reverts. Actual: deployment succeeds ('next call did not revert as expected'); mints then burn BMC for 30 days and every requestSeed() reverts 'unregistered gas lane' (the repository's own test_UnknownGasLaneCannotRequestSeed shows that dead end). Scratch test test_B_CancelledSubscriptionStallsForever against Chainlink's VRFCoordinatorV2_5Mock extended with s_provingKeys: createSubscription, addConsumer(pass), fund 100 LINK, mint 40 Genesis + 5 mystery (41,750,000 BMC burned), the subscription owner calls cancelSubscription(subId, to) before the deadline; at the deadline and 365 days later requestSeed() reverts inside requestRandomWords; seedRequestId() == 0, pendingReveals() == 5, vrfConfig() still returns the dead subscription id and no function can change it. Scratch test test_B_RemovedConsumerIsRecoverableOnlyBySubscriptionOwner: without addConsumer, requestSeed() reverts InvalidConsumer(subId, pass) and succeeds only after the subscription owner adds the consumer.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {BMCIlluminatiPassCandidateV3} from "src/experimental/BMCIlluminatiPassCandidateV3.sol";
import {VRFV2PlusClient} from "@chainlink/contracts/src/v0.8/vrf/dev/libraries/VRFV2PlusClient.sol";

/// @dev Stand-in for the mainnet VRF v2.5 coordinator: like the real one, `requestRandomWords`
///      does not validate the key hash, and `s_provingKeys` reports whether a lane is registered.
contract KeyAwareCoordinator {
    bytes32 public constant REGISTERED = 0x3fd2fec10d06ee8f65e7f2e95f5c56511359ece3f33960ad8a866ae24a8ff10b;
    uint256 public nextRequestId = 1000;

    function s_provingKeys(bytes32 key) external pure returns (bool exists, uint64 maxGas) {
        return (key == REGISTERED, key == REGISTERED ? uint64(500 gwei) : 0);
    }

    function requestRandomWords(VRFV2PlusClient.RandomWordsRequest calldata) external returns (uint256 id) {
        id = nextRequestId++;
    }
}

/// @notice Finding: an unregistered gas lane is accepted by the constructor and only rejected by
///         `requestSeed()` after the sale has closed, when BMC has already been burned and the VRF
///         config can no longer be changed. The constructor must reject a key hash the coordinator
///         does not know, so the misconfiguration fails before any mint instead of after the sale.
contract V3UnregisteredKeyHashTest is Test {
    KeyAwareCoordinator coord;

    // VRF v2 (not v2.5) 500 gwei mainnet lane: a realistic copy-paste mistake.
    bytes32 constant V2_KEY_HASH = 0xff8dedfbfa60af186cf3c830acbc32c05aae823045ae5ea7da1e45fbfaba4f92;

    function setUp() public {
        vm.warp(1_800_000_000);
        coord = new KeyAwareCoordinator();
    }

    function _deploy(bytes32 key) internal returns (BMCIlluminatiPassCandidateV3) {
        return new BMCIlluminatiPassCandidateV3(
            address(this),
            address(0xB0C),
            address(coord),
            uint64(block.timestamp + 30 days),
            123,
            key,
            500_000,
            3,
            true,
            "bafybeihfihwwpev4gkqjuqawgtptsv3ynzsokclo6odsolvoa65aqaac2u"
        );
    }

    function test_RegisteredKeyHashDeploys() public {
        BMCIlluminatiPassCandidateV3 pass = _deploy(coord.REGISTERED());
        (, bytes32 keyHash,,,, bool configured) = pass.vrfConfig();
        assertEq(keyHash, coord.REGISTERED());
        assertTrue(configured);
    }

    /// @dev Fails on the current code: the constructor accepts any non-zero key hash, so the
    ///      deployment succeeds and the lane error surfaces only in `requestSeed()` post-sale.
    function test_UnregisteredKeyHashIsRejectedAtDeployment() public {
        vm.expectRevert();
        _deploy(V2_KEY_HASH);
    }
}
```

### 3. Medium: Deployment configuration: 500,000 callback gas for a one-SSTORE callback inflates the lane minimum to about 0.4 ETH while the hard-coded mainnet subscription holds 0.02 ETH, 0 LINK and no consumers, a

`script/DeployBMCIlluminatiPassV3DryRun.s.sol:37`

```
            500_000,
            3,
            true,
```

The dry-run script fixes callbackGasLimit = 500,000, requestConfirmations = 3 and nativePayment = true for the 500 gwei lane 0x3fd2fec1...f10b and subscription 2785245948...9562985. V3's callback only stores one word (measured at 36,577 gas inside the coordinator's call in a scratch run); the batch-finalization constants that justified 500,000 in the production contract are unused in V3, so the limit is roughly 9x the need. Chainlink computes the minimum subscription balance from the lane's maximum gas price times (200,000 verification gas + callbackGasLimit) plus the premium: 500 gwei x 700,000 = 0.35 ETH before the native premium, about 0.43 ETH with it, against about 0.22 ETH at the contract's 150,000 minimum. Read-only mainnet calls at block 26177145 show the subscription holds 0 LINK and 0.02 ETH native, has 0 requests, is owned by EOA 0x83027AD9d0D5374335086c539dADD1db983441B0 and has no consumers. As configured, the pass is not a consumer (requestSeed would revert InvalidConsumer until that owner adds it), and once added the single request would sit below the minimum and expire after 24 hours with no retry (see the single-request finding); the correct operational order is to fund above the lane minimum first and add the consumer last. The dry run, and the CI job that runs it, only checks owner, deadline and CID equality: it never asserts s_provingKeys(KEY_HASH).exists, never reads getSubscription(SUBSCRIPTION_ID) for balance and consumers, and never calls requestSeed, so the 'V3 deployment simulation' cannot catch any of this. The Genesis CID bafybeihfihww...aac2u could not be verified from this environment. Fix: set callbackGasLimit to the contract minimum (150,000, or lower MIN_CALLBACK_GAS_LIMIT to about 100,000 with headroom) unless the callback is changed to finalize a batch; make the dry run assert the lane is registered, read getSubscription and require nativeBalance (nativePayment=true) above the computed lane minimum with margin, and prank the subscription owner to addConsumer and call requestSeed on the fork; and document the fund-then-add-consumer order in the launch checklist.

**Reproduction**

cast call 0xD7f86b4b8Cae7D942340FF628F82735b7a20893a 's_provingKeys(bytes32)(bool,uint64)' 0x3fd2fec10d06ee8f65e7f2e95f5c56511359ece3f33960ad8a866ae24a8ff10b -> (true, 500000000000); cast call 0xD7f86b4b8Cae7D942340FF628F82735b7a20893a 'getSubscription(uint256)(uint96,uint96,uint64,address,address[])' 27852459484169864437638942739291618120641810244677084392617474192083559562985 -> (0, 20000000000000000, 0, 0x83027AD9d0D5374335086c539dADD1db983441B0, []) at block 26177145. Scratch test test_B_RemovedConsumerIsRecoverableOnlyBySubscriptionOwner: V3 deployed against Chainlink's VRFCoordinatorV2_5Mock with the pass not yet a consumer -> requestSeed() reverts InvalidConsumer(subId, pass). Scratch test test_C_OutcomePredictableBeforeFinalize logs 'callback gas used 36577' for rawFulfillRandomWords. Reading script lines 43-49: the only assertions are owner, deadline, CID locked and CID equality. Expected: the dry run proves the request can be made and paid with the committed constants. Actual: it proves only that the constructor runs, and the live subscription state would make the only request unpayable.

### 4. Low: Every mystery outcome is publicly computable from globalSeed before finalizeReveals runs, while tierOf, tokenURI and revealStatusOf still report Pending and the callback finalizes nothing

`src/experimental/BMCIlluminatiPassCandidateV3.sol:306`

```
        if (seedReceived) return;
        seedReceived = true;
        globalSeed = randomWords[0];
```

rawFulfillRandomWords (lines 302-310) only stores globalSeed; unlike the production contract it finalizes nothing, although CALLBACK_REVEAL_BATCH, GAS_PER_REVEAL and CALLBACK_GAS_RESERVE are still declared and 500,000 callback gas is paid for. Every pending token's outcome is then a pure function of (globalSeed, tokenId) through the in-order virtual Fisher-Yates (r = keccak256(abi.encode(seed, tokenId)) % remaining), so anyone reading globalSeed() or watching the fulfilment transaction in the mempool knows which pending tokens will be Genesis (37 of 460, the 1,000,000-BMC tier) before holders and marketplaces do, while tierOf() returns Pending, artworkIdOf() returns 0, tokenURI() returns the 'Pending Reveal' JSON and revealStatusOf() keeps returning AwaitingRandomness (RevealStatus.RandomnessStored is never written in V3). The window lasts until someone pays for finalizeReveals(), which nobody is obliged to call and an informed buyer is incentivised not to; no ERC-4906 metadata event is emitted either. The pending JSON discloses that rarity can be calculated early, which keeps this Low, but the contract creates the window and leaves it open indefinitely. Fix: after storing the seed, finalize a gas-bounded batch inside the callback as src/BMCIlluminatiPass.sol does (batch from gasleft(), try this.finalizeReveals(batch) {} catch {}); derive revealStatusOf as RandomnessStored whenever seedReceived and the token is not yet finalized; optionally expose a view that computes a pending token's outcome from globalSeed so the information is symmetric; emit ERC-4906 BatchMetadataUpdate on seed receipt and MetadataUpdate on each reveal so marketplaces refresh.

**Reproduction**

Scratch test test_C_OutcomePredictableBeforeFinalize: mint 40 Genesis + 10 mystery, warp to saleDeadline, requestSeed(), the coordinator delivers word 0xC0FFEE. Before any finalizeReveals call: revealStatusOf(41) == AwaitingRandomness (1), tierOf(41) == Pending (0), tokenURI(41) is byte-identical to the pre-seed pending JSON, revealedCount() == 0. Replaying the Fisher-Yates in memory from globalSeed() for tokens 41..50 predicts tier and artwork; finalizeReveals(10) then returns exactly those predictions for all 10 tokens. Expected: views and metadata reflect the outcome once it is determined, or the first batch is revealed atomically with the seed. Actual: outcomes are public and fixed while the contract still reports pending.

### 5. Low: requestSeed() spends the single paid VRF request even when no mystery token exists; a Genesis shortfall at the deadline freezes the collection and mintMystery reports SoldOut

`src/experimental/BMCIlluminatiPassCandidateV3.sol:252`

```
    function requestSeed() external returns (uint256 requestId) {
        if (!saleClosed) closeSale();
```

requestSeed() only requires that the sale can be closed (sold out or block.timestamp >= saleDeadline) and then sends the single paid VRF request. mintMystery() requires totalMinted >= 40, so if the 30-day deadline passes before all 40 Genesis tokens (1,000,000 BMC each, 40,000,000 BMC in total) have sold, no mystery token exists and pendingReveals() == 0, yet anyone can still trigger a request billed to the subscription at 500 gwei lane prices, and finalizeReveals() loops zero times. The same path exposes a design consequence that is nowhere documented or tested: a Genesis shortfall freezes the collection at the sold size forever, the 460 mystery positions are never offered while remainingMysteryMints() still reports 460, and after the deadline mintMystery() reverts SoldOut() rather than a deadline error (with 41 tokens sold it reports SoldOut while 459 remain). Fix: require(totalMinted > GENESIS_PHASE_SUPPLY, 'nothing to reveal') in requestSeed() (closeSale() can stay callable); add a SaleEnded error for the deadline branch of both mint functions; return 0 from remainingMysteryMints() once the sale is closed; and document, or consciously change, the rule that the mystery phase never opens without a Genesis sell-out.

**Reproduction**

Scratch test test_D_RequestSeedWithNothingToReveal: 39 x mintGenesis(), warp to saleDeadline; mintGenesis() reverts GenesisPhaseOver, mintMystery() reverts GenesisPhaseNotOver before and after the deadline, pendingReveals() == 0, remainingMysteryMints() == 460. A random EOA calls requestSeed(): the coordinator's request counter increments (request created and billable on fulfilment), saleClosed() == true, and after fulfilment finalizeReveals(100) returns 0. Expected: revert because nothing needs randomness. Actual: a paid request is spent. Scratch test test_D_SoldOutErrorNameAfterDeadline: 40 Genesis + 1 mystery, warp to the deadline, mintMystery() reverts SoldOut() while remainingSupply() == 459.

### 6. Low: Fixed metadata claims ('One of 77 Genesis pieces in a 500-piece collection', 'One of 423 Standard pieces') and the remaining-pool views are false whenever the 30-day sale ends before sell-out

`src/experimental/BMCIlluminatiPassCandidateV3.sol:459`

```
                : "A Genesis BMC Illuminati Pass. A mysterious cartoon frog in a black hooded cloak with premium gold-and-black styling, a glowing golden third eye and a floating golden eye-in-triangle. One of 77 Genesis pieces in a 500-piece collection minted by permanently burning BMC.",
```

The sale closes permanently at saleDeadline (mint guards at lines 214 and 233, closeSale at line 245), and draws without replacement happen only for tokens actually sold, so after a partial sale most of the 37 mystery Genesis artworks and 423 Standard artworks never exist. The on-chain metadata is constant text: every Genesis token says 'One of 77 Genesis pieces in a 500-piece collection' (line 459), every Standard token 'One of 423 Standard pieces in a 500-piece collection' (line 485) and the Legendary token 'the rarest piece of the 500-piece collection' (line 458); phase-1 tokens 1..40 carry the same sentence. After a partial sale these claims misstate the supply and rarity the collection's value rests on, and remainingMysteryGenesis() and remainingMysteryStandard() keep reporting undrawn outcomes as 'still inside the random pool' after the sale is over. This is V3-specific: the production contract has no deadline, so there the counts become true at mint-out. Fix: build the counts from state once saleClosed (for example 'One of <GENESIS_PHASE_SUPPLY + mysteryGenesisRevealed> Genesis pieces in a <totalMinted>-piece collection' after all sold tokens are finalized) or drop the fixed numbers; return 0 from the remaining* views once saleClosed and expose the final supply after close.

**Reproduction**

Scratch test test_E_PartialSaleMetadata: mint 40 Genesis + 1 mystery, warp to saleDeadline, requestSeed(), fulfil with seed 5 (keccak256(abi.encode(5, 41)) % 460 < 37), finalizeReveals(1). totalMinted() == totalSupply() == 41 (all Genesis), remainingMysteryGenesis() == 36, remainingMysteryStandard() == 423, remainingMysteryMints() == 459. Decoded tokenURI(41): {"name":"BMC Illuminati Pass #41 - Genesis","description":"... One of 77 Genesis pieces in a 500-piece collection minted by permanently burning BMC.","image":"ipfs://bafycid/genesis-59.png", ...}; tokenURI(2) carries the same sentence. Expected: metadata that reflects the final 41-piece supply or makes no fixed-count claim. Actual: 77 of 500 is claimed for a 41-piece collection.

### 7. Low: V3 tests run only on a hand-written mock, encode the permanent stall and an 8-day fulfilment as expected behaviour, and cannot run against Chainlink's official VRFCoordinatorV2_5Mock; the '80 passing

`test/BMCIlluminatiPassCandidateV3.t.sol:87`

```
        vm.warp(block.timestamp + 8 days);
        vm.expectRevert(bytes("seed already requested"));
```

The nine V3 tests run only against V3RegisteredCoordinator, a hand-written mock that implements s_provingKeys but models neither billing, consumer registration nor request expiry. test_OnlyOneSeedRequestEvenAfterSevenDays (lines 82-94) asserts the permanent single-request stall as intended behaviour and then fulfils the request 8 days after it was sent, which the live network does not do (requests below the minimum balance expire after 24 hours). The repository's integration suites against Chainlink's official VRFCoordinatorV2_5Mock (ChainlinkMockIntegration, VRFRecovery*, VRFSafetyProperties) and the mainnet fork test target src/BMCIlluminatiPass.sol only; the official mock has no s_provingKeys getter, so V3's requestSeed() cannot execute against it at all. Untested for V3: an unfulfilled or expired request, an unfunded or LINK-only subscription with nativePayment=true, a cancelled subscription or missing consumer, the Genesis shortfall and partial-sale finalization, the pending-to-revealed metadata transition, redelivery of the seed, a callback delivered with exactly callbackGasLimit, and the gas profile of finalizing 460 tokens in batches. forge test --offline at bf2a63c reports 80 passed and 1 failed (test_RealBMCGenesisMint: 'Ethereum mainnet fork required', aimed at the production contract); CI excludes that contract and runs the fork test and the V3 dry run only when a MAINNET_RPC_URL secret exists. The claimed 80 passing tests therefore give little assurance about the property V3 hinges on. Fix: add a V3 suite on VRFCoordinatorV2_5Mock through a thin subclass exposing s_provingKeys (or vm.mockCall), cover the cases above, replace the 8-day fulfilment with the retry expectation once the liveness fix lands, and add a V3 fork test that deploys with the dry-run parameters, adds the consumer as the subscription owner and calls requestSeed against the real coordinator.

**Reproduction**

forge test --offline at bf2a63c: '80 tests passed, 1 failed' with '[FAIL: Ethereum mainnet fork required] test_RealBMCGenesisMint()'. Scratch test test_I_OfficialMockRejectsRequestSeed: deploy V3 with address(new VRFCoordinatorV2_5Mock(0.1 ether, 1e9, 4e15)), createSubscription, addConsumer, fundSubscription(100 ether), warp to the deadline, requestSeed(). Expected (per the README's claim of a run against Chainlink's official mock): a request id. Actual: revert 'unregistered gas lane'. grep shows no test deploys BMCIlluminatiPassCandidateV3 against VRFCoordinatorV2_5Mock or a chain-id-1 fork, and lines 87-88 of the V3 test assert the stall and fulfil 8 days later.

### 8. Info: Dead state, constants, events and errors inherited from the per-mint design, an inert Ownable and a misleading status machine make V3's public surface wrong for integrators; runtime is 984 bytes under

`src/experimental/BMCIlluminatiPassCandidateV3.sol:88`

```
    uint256 public constant CALLBACK_REVEAL_BATCH = 4;
```

Candidate V3 replaced per-mint requests with one global seed but kept the per-mint design's surface: RevealStatus.RandomnessStored is never written (revealStatusOf goes AwaitingRandomness -> Revealed), events RandomnessStored and VRFConfigSet are never emitted (the config is set in the constructor without an event, asymmetric with GenesisImagesCIDSet), requestIdOf and tokenIdOfRequest are public getters that always return 0, _randomWord is only ever deleted, MysteryMinted always carries requestId 0, CALLBACK_REVEAL_BATCH, GAS_PER_REVEAL and CALLBACK_GAS_RESERVE (lines 88-91) are unused, errors GenesisCIDAlreadySet, GenesisCIDNotSet and VRFNotConfigured guard conditions that are always false (genesisCIDLocked and configured are set true in the constructor), and Ownable is inherited although no function is onlyOwner, so owner(), transferOwnership and renounceOwnership have no effect while signalling a role to explorers. The pending artwork text 'REVEAL PENDING (Chainlink VRF)' also stays after the seed exists. Indexers and front ends built on the documented status machine (README: 'anyone can call finalizeReveals(n) if a callback left stored words') will misreport state. forge build --sizes reports the V3 runtime at 23,592 bytes, 984 bytes under the EIP-170 limit, so the fixes for the higher findings must be re-measured; removing the dead members recovers margin. Fix: delete the unused state, constants, events and errors; emit VRFConfigSet in the constructor; derive RandomnessStored from seedReceived; either drop Ownable or document that the V3 owner has no powers (and make it a multisig if the VRF-config recovery setter is added).

**Reproduction**

grep -n onlyOwner src/experimental/BMCIlluminatiPassCandidateV3.sol returns nothing; grep shows RandomnessStored, VRFConfigSet, requestIdOf, tokenIdOfRequest, CALLBACK_REVEAL_BATCH, GAS_PER_REVEAL and CALLBACK_GAS_RESERVE are declared but never assigned or emitted. Scratch test test_C_OutcomePredictableBeforeFinalize: after the coordinator delivers the seed, revealStatusOf(41) == 1 (AwaitingRandomness), never 2. The existing test_BurnAndMintDoNotRequestRandomness asserts requestIdOf(41) == 0 after a mystery mint. forge build --sizes --offline: 'BMCIlluminatiPassCandidateV3 | 23,592 | 25,449 | 984'. Expected: a surface that describes V3. Actual: getters, events and statuses that can never be observed.

### 9. Info: README and security review document the production contract, contradict Candidate V3 (which is marked NOT FOR DEPLOYMENT) and misstate Chainlink's handling of unfunded requests

`README.md:63`

```
A pending token stays pending until its original request is fulfilled. There is no reroll,
re-request or fallback. Chainlink VRF v2.5 keeps a request pending while the subscription is
unfunded and fulfils it after funding, which anyone can do. The owner changing `setVRFConfig`
```

README.md and docs/SECURITY-REVIEW.md describe the production contract src/BMCIlluminatiPass.sol: one VRF request per mystery mint (lines 46-47), a gas-aware batch of reveals in the callback (48-49), owner setters setGenesisImagesCID and setVRFConfig (73-74, 100-104), a three-argument constructor (83) and an 'unavailable randomness' model in which an unfunded request is kept pending and fulfilled after funding (63-65). Candidate V3 has none of these: one post-sale seed, a ten-argument constructor, no owner setters, an immutable 30-day deadline, and its own header says 'EXPERIMENTAL V3 CANDIDATE - NOT FOR DEPLOYMENT' (line 14) while the CI workflow simulates its deployment. The README's funding statement is also wrong for the network: Chainlink's VRF v2.5 subscription documentation states that requests below the minimum balance 'remain pending for up to 24 hours before they expire', which is exactly what turns V3's single request into a permanent stall. Anyone deploying or operating from the README would deploy the wrong contract or misconfigure V3, and marketplaces reading it would misstate the reveal mechanics. The older experimental contracts (Candidate, Candidate V2, BMCPassVRFPrototype, BMCPostSaleSeedController) are not distinguished from V3 anywhere in the docs. Fix: decide which contract is the deployment candidate; if V3, remove the header, rewrite the README's mint mechanics, privileged-powers and deployment sections for V3, correct the 24-hour expiry statement, and scope docs/SECURITY-REVIEW.md to V3; otherwise mark V3 experimental in the README and stop simulating its deployment in CI.

**Reproduction**

Read README.md lines 46-47, 63-65, 73-74, 83 and 100-104 and compare with src/experimental/BMCIlluminatiPassCandidateV3.sol lines 14, 178-189, 228-240 and 250-276: grep -n 'function set' on the V3 source returns nothing, while the README instructs the owner to call setGenesisImagesCID and setVRFConfig after launch. docs/SECURITY-REVIEW.md line 3 scopes the review to src/BMCIlluminatiPass.sol. The Chainlink subscription page (docs.chain.link/vrf/v2-5/overview/subscription) states the 24-hour expiry. Expected: documentation that matches the deployment candidate and Chainlink's expiry behaviour. Actual: it documents a different contract and an incorrect liveness assumption.

---

Judge's submission `c813c676da27eab8a3f583814725ae3f4e463f48cc996b569f209324ab048eea`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
