# Audit report

> PROJECT: BMC ILLUMINATI PASS — PRE-MAINNET SECURITY AUDIT
>
> Audit my existing Solidity ERC-721 collection before Ethereum mainnet deployment.
>
> Repository:
> https://github.com/0xSt3w/launch-1356-project-bmc-illuminati-pass
>
> Network: Ethereum Mainnet, chain ID 1.
>
> BMC token:
> 0x38224239f2BDae357D47cb864BC533d7f72dF961
>
> Chainlink VRF v2.5 coordinator:
> 0xD7f86b4b8Cae7D942340FF628F82735b7a20893a
>
> Genesis IPFS directory CID:
> bafybeihfihwwpev4gkqjuqawgtptsv3ynzsokclo6odsolvoa65aqaac2u
>
> AUDIT SCOPE
>
> Review all relevant Solidity contracts, deployment scripts, libraries, Foundry tests, VRF integrations and token interactions.
>
> 1. NFT SUPPLY AND MINTING
> - Exactly 500 ERC-721 tokens.
> - First 40 mints are sequential Genesis.
> - Genesis #1 goes to the first successful minter.
> - First 40 mints burn 1,000,000 BMC each.
> - Remaining 460 mystery mints burn 350,000 BMC each.
> - Exactly 37 additional Genesis and 423 Standard outcomes.
> - No duplicate artwork assignments.
> - No minting beyond 500 tokens.
>
> 2. BMC BURN SECURITY
> - Verify real BMC burnFrom compatibility.
> - Verify 18 decimals and allowance handling.
> - Confirm totalSupply and payer balance decrease correctly.
> - Test failures, reentrancy and unexpected token behavior.
> - Maximum total burn: 201,000,000 BMC.
>
> 3. CHAINLINK VRF SECURITY
> - Verify Ethereum mainnet coordinator address and ABI compatibility.
> - Verify VRF v2.5 subscription requirements.
> - Review callback gas limits and payment configuration.
> - Test concurrent requests and out-of-order fulfillment.
> - Confirm random allocation without replacement.
> - Investigate permanently pending reveals and coordinator failures.
> - Review the consequences of owner-controlled VRF configuration.
>
> 4. IPFS AND METADATA
> - Verify all 77 Genesis image paths.
> - Verify Genesis #1 points to genesis-01.png.
> - Confirm CID locking and metadata immutability.
> - Review Base64 JSON and on-chain Standard SVG rendering.
> - Check uniqueness of all 423 Standard combinations.
> - Confirm the artwork generator cannot accidentally overwrite the approved premium Genesis files.
>
> 5. OWNER PERMISSIONS
> - Review setGenesisImagesCID and setVRFConfig.
> - Review transferOwnership and renounceOwnership.
> - Confirm no free owner mint, hidden withdrawals or upgrades.
> - Identify any risks from privileged configuration.
>
> 6. DEPLOYMENT
> - Review script/Deploy.s.sol.
> - Verify owner, BMC and VRF coordinator parameters.
> - Verify foundry.toml and bytecode_hash = "none".
> - Check deployment size, gas estimates and Etherscan verification.
> - Review readiness for Ethereum mainnet.
>
> 7. TESTING
> - Independently execute forge build and forge test.
> - Review the 43 existing Foundry tests.
> - Execute tests on an Ethereum mainnet fork using the actual BMC contract.
> - Add tests for uncovered edge cases.
> - Review invariants, gas limits and failure recovery.
>
> DELIVERABLES
>
> Provide:
> - Security findings classified Critical, High, Medium, Low and Informational.
> - Reproduction steps and proof-of-concept tests for significant findings.
> - Specific Solidity fixes.
> - Updated Foundry tests.
> - GitHub audit report.
> - Clear list of unresolved risks.
> - Mainnet deployment readiness assessment.
>
> IMPORTANT
>
> Do not deploy any contracts.
> Do not execute real BMC burns or token approvals.
> Do not request private keys or seed phrases.
> Do not change mint prices, supply or artwork without authorization.
> Do not claim that automated checks constitute a complete independent security audit.
>
> Report any blockers before requesting payment.

| | |
|---|---|
| Repository | https://github.com/0xSt3w/launch-1356-project-bmc-illuminati-pass.git |
| Commit | `330019e65d576ffda91c565cbff473a507d27d34` |
| Job | `de963da7-456d-4f11-a8cf-3b6dac017133` |
| Judged | 2026-10-12 04:54 UTC |
| Findings | 1 high · 2 medium · 3 low · 5 info |

Four agents audited the code as it is at `330019e`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: One never-fulfilled VRF request freezes every later mystery reveal forever: strict in-order finalization with no re-request, skip or recovery path

`src/BMCIlluminatiPass.sol:321`

```
        while (done < maxCount && tokenId <= totalMinted && _revealStatus[tokenId] == RevealStatus.RandomnessStored) {
```

finalizeReveals() only ever inspects token GENESIS_PHASE_SUPPLY + revealedCount + 1 and stops at the first token that is not RandomnessStored (line 321). The callback itself only calls this.finalizeReveals, mintMystery stores exactly one requestId per token, and rawFulfillRandomWords accepts only that id. So a token whose request is never fulfilled stays AwaitingRandomness forever, and every later token stays Pending as well, even when its own random word has already been delivered and stored in _randomWord. No function can open a replacement request, skip the stuck token, or finalize a stored word out of order; the owner's setVRFConfig does not help because it only affects future requests.

The NatSpec (lines 36-39) and README (lines 61-67) assume this state cannot arise because 'Chainlink VRF v2.5 requests remain pending while the subscription is unfunded and are fulfilled once it is funded again'. That is only true for 24 hours: Chainlink's VRF v2.5 subscription documentation (docs.chain.link/vrf/v2-5/overview/subscription, fetched during this review) states 'If your balance is below the minimum, your requests remain pending for up to 24 hours before they expire' and that pending requests process after funding only 'as long as they have not expired'. The repository's own test test_UnfundedSubscriptionKeepsTokenPendingUntilFunded encodes the wrong assumption. Other ways a request is never fulfilled, all verified in this review: the mainnet coordinator accepts requests for an unregistered key hash and never fulfils them (see the separate medium finding; reproduced on a mainnet fork at block 26174090), a lane retired by Chainlink while requests are outstanding, or the v2.5 coordinator being decommissioned. An unprivileged buyer can also amplify the funding path: there is no rate limit, so burst-minting pushes the subscription below its minimum and every request in that window (other buyers' included) expires unless the operator tops up within 24 hours.

Impact: every buyer after the stuck token has irreversibly burned 350,000 BMC for an NFT that can never be revealed (worst case 459 tokens, 160,650,000 BMC), the 37 mystery Genesis outcomes are never assigned, and the stuck tokens trade as perpetual 'Pending Reveal'. The README describes the pending state as affecting only 'the affected token'; the actual blast radius is the whole remainder of the collection.

Fix (preserves in-order finalization and the no-reroll guarantee): record the request block per mystery token and add a permissionless rerequestRandomness(uint256 tokenId) that, for a token still AwaitingRandomness whose request is older than a fixed timeout (e.g. 14,400 blocks, ~2 days, longer than Chainlink's 24h expiry so no legitimate fulfilment can still be in flight), opens a new VRF request with the current config and maps the new request id to the token while keeping the old mapping. The existing status check in rawFulfillRandomWords (line 298) already makes the first delivery win and later ones no-ops, so nobody gains a reroll. A reference implementation of exactly this (requestBlockOf mapping, 14,400-block timeout, same request parameters, nonReentrant) was applied during this review: the attached test passed and the runtime size was 24,277 bytes, 299 bytes under EIP-170. An alternative that also makes the attached test pass is finalizing in randomness-delivery order (a storage queue of delivered token ids) or a timeout-gated skip of a stuck head token; both change the 'mint order' property documented in F-1, so the re-request is the smaller design change. Whatever is chosen, correct the NatSpec at lines 36-39, README lines 61-67 and docs/SECURITY-REVIEW.md F-2/F-10, and replace test_UnfundedSubscriptionKeepsTokenPendingUntilFunded with a test that models expiry. Consider also the mint-time subscription balance check from the separate medium finding so requests are not opened against an unfundable subscription in the first place.

**Reproduction**

State: phase 1 complete (40 Genesis minted), CID and VRF config set. 1) alice approves 350_000e18 BMC and calls mintMystery() -> token 41, request A. 2) bob -> token 42, request B. 3) carol -> token 43, request C. 4) The coordinator delivers B and C: revealStatusOf(42) == revealStatusOf(43) == RandomnessStored (2), tierOf == Pending. 5) Request A is never delivered (expired after 24h underfunded, unregistered key hash, retired lane). Warp 30 days, roll 216,000 blocks. 6) Anyone calls finalizeReveals(type(uint256).max); the owner calls setVRFConfig with a fresh subscription and lane; anyone calls a hypothetical rerequestRandomness(41). Expected: a path exists for 42 and 43 (and eventually 41) to be revealed. Actual: finalizeReveals returns 0, the rerequest selector does not exist, revealStatusOf(42) and (43) stay 2 forever, pendingReveals() == 3, and no function in the contract can change this. Run: forge test --match-path test/scratch/HeadOfLineBlocking.t.sol -> FAIL 'token 42 has stored randomness but is frozen forever behind never-fulfilled token 41: 2 != 3'. The same test passes with a timeout-gated permissionless rerequestRandomness(uint256) added (verified on a patched copy), or with delivery-order / skip-after-timeout finalization.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {BMCIlluminatiPass} from "src/BMCIlluminatiPass.sol";

/// @dev Minimal 18-decimal token with OpenZeppelin ERC20Burnable-style burnFrom (spend allowance, destroy).
contract PocBMC {
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function decimals() external pure returns (uint8) {
        return 18;
    }

    function mint(address to, uint256 amount) external {
        balanceOf[to] += amount;
        totalSupply += amount;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }

    function burnFrom(address account, uint256 amount) external {
        uint256 a = allowance[account][msg.sender];
        require(a >= amount, "insufficient allowance");
        allowance[account][msg.sender] = a - amount;
        require(balanceOf[account] >= amount, "insufficient balance");
        balanceOf[account] -= amount;
        totalSupply -= amount;
    }
}

interface IRawFulfill {
    function rawFulfillRandomWords(uint256 requestId, uint256[] calldata randomWords) external;
}

/// @dev VRF v2.5 coordinator stand-in: same requestRandomWords((bytes32,uint256,uint16,uint32,uint32,bytes))
///      selector as the real coordinator; the test decides which request ids are ever delivered.
contract PocCoordinator {
    struct RandomWordsRequest {
        bytes32 keyHash;
        uint256 subId;
        uint16 requestConfirmations;
        uint32 callbackGasLimit;
        uint32 numWords;
        bytes extraArgs;
    }

    uint256 public lastRequestId = 1000;
    mapping(uint256 => address) public consumerOf;
    mapping(uint256 => uint32) public gasOf;
    mapping(uint256 => bool) public delivered;

    function requestRandomWords(RandomWordsRequest calldata req) external returns (uint256 id) {
        id = ++lastRequestId;
        consumerOf[id] = msg.sender;
        gasOf[id] = req.callbackGasLimit;
    }

    /// @dev Deliver one word with the request's own callback gas limit, like the real coordinator.
    function deliver(uint256 requestId, uint256 word) external returns (bool ok) {
        require(consumerOf[requestId] != address(0), "unknown request");
        require(!delivered[requestId], "already delivered");
        delivered[requestId] = true;
        uint256[] memory words = new uint256[](1);
        words[0] = word;
        (ok,) = consumerOf[requestId].call{gas: gasOf[requestId]}(
            abi.encodeCall(IRawFulfill.rawFulfillRandomWords, (requestId, words))
        );
    }
}

/// @title One never-fulfilled VRF request freezes every later reveal forever
/// @notice finalizeReveals only ever inspects token 40 + revealedCount + 1 and stops when it is not
///         RandomnessStored. If that token's request is never fulfilled (expired after 24h on an
///         underfunded subscription, unregistered key hash, retired lane), every later token whose word
///         IS stored stays pending forever, and no function can re-request or skip. This test fails on
///         the current code. It passes with any of the fixes that give the collection a way forward:
///         a timeout-gated permissionless rerequestRandomness(uint256) for the stuck token, a
///         timeout-gated skip of the stuck head token, or finalization in randomness-delivery order.
contract HeadOfLineBlockingTest is Test {
    PocBMC bmc;
    PocCoordinator vrf;
    BMCIlluminatiPass pass;

    address owner = makeAddr("owner");
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");
    address carol = makeAddr("carol");

    uint256 constant GENESIS_PRICE = 1_000_000e18;
    uint256 constant MYSTERY_PRICE = 350_000e18;

    function setUp() public {
        bmc = new PocBMC();
        vrf = new PocCoordinator();
        pass = new BMCIlluminatiPass(owner, address(bmc), address(vrf));
        vm.startPrank(owner);
        pass.setGenesisImagesCID("bafybeihfihwwpev4gkqjuqawgtptsv3ynzsokclo6odsolvoa65aqaac2u");
        pass.setVRFConfig(1, keccak256("lane"), 500_000, 3, false);
        vm.stopPrank();
        for (uint256 i = 0; i < 40; i++) {
            address who = address(uint160(0x1000 + i));
            bmc.mint(who, GENESIS_PRICE);
            vm.startPrank(who);
            bmc.approve(address(pass), GENESIS_PRICE);
            pass.mintGenesis();
            vm.stopPrank();
        }
    }

    function _mintMystery(address who) internal returns (uint256 id, uint256 req) {
        bmc.mint(who, MYSTERY_PRICE);
        vm.startPrank(who);
        bmc.approve(address(pass), MYSTERY_PRICE);
        (id, req) = pass.mintMystery();
        vm.stopPrank();
    }

    function test_StuckRequestMustNotFreezeLaterRevealsForever() public {
        (uint256 a, uint256 reqA) = _mintMystery(alice); // token 41: its request is never delivered
        (uint256 b, uint256 reqB) = _mintMystery(bob); // token 42
        (uint256 c, uint256 reqC) = _mintMystery(carol); // token 43
        assertEq(a, 41);
        assertEq(b, 42);
        assertEq(c, 43);

        // The coordinator delivers 42 and 43 (callbacks succeed, words stored). 41's request never completes.
        assertTrue(vrf.deliver(reqB, uint256(keccak256("word-42"))));
        assertTrue(vrf.deliver(reqC, uint256(keccak256("word-43"))));
        assertEq(uint8(pass.revealStatusOf(b)), uint8(BMCIlluminatiPass.RevealStatus.RandomnessStored));
        assertEq(uint8(pass.revealStatusOf(c)), uint8(BMCIlluminatiPass.RevealStatus.RandomnessStored));

        // A long time passes: far beyond Chainlink's 24h expiry and any reasonable recovery timeout.
        vm.warp(block.timestamp + 30 days);
        vm.roll(block.number + 216_000);

        // Every path the fixed contract might offer is exercised:
        // (1) permissionless finalization (delivery-order or skip-after-timeout fixes);
        pass.finalizeReveals(type(uint256).max);
        // (2) a permissionless re-request for the stuck token (re-request fix); if the contract opens a
        //     fresh request, the coordinator delivers it and finalization is retried.
        (bool rerequested,) = address(pass).call(abi.encodeWithSignature("rerequestRandomness(uint256)", a));
        if (rerequested) {
            uint256 fresh = vrf.lastRequestId();
            assertTrue(fresh != reqA, "re-request must open a new VRF request");
            assertTrue(vrf.deliver(fresh, uint256(keccak256("word-41-again"))));
            pass.finalizeReveals(type(uint256).max);
        }

        // Bob and Carol each burned 350,000 BMC and their randomness is on-chain: their tokens must be revealable.
        assertEq(
            uint8(pass.revealStatusOf(b)),
            uint8(BMCIlluminatiPass.RevealStatus.Revealed),
            "token 42 has stored randomness but is frozen forever behind never-fulfilled token 41"
        );
        assertEq(
            uint8(pass.revealStatusOf(c)),
            uint8(BMCIlluminatiPass.RevealStatus.Revealed),
            "token 43 has stored randomness but is frozen forever behind never-fulfilled token 41"
        );
        assertTrue(pass.tierOf(b) != BMCIlluminatiPass.Tier.Pending, "token 42 has no tier");
        assertTrue(pass.tierOf(c) != BMCIlluminatiPass.Tier.Pending, "token 43 has no tier");
        // Without-replacement accounting must still hold: every finalized token consumed exactly one slot.
        assertEq(pass.revealedCount(), rerequested ? 3 : 2);
    }
}
```

### 2. Medium: setVRFConfig accepts any non-zero key hash; the mainnet coordinator accepts and never fulfils requests for unregistered lanes, so a wrong lane burns 350,000 BMC per mint instead of failing closed

`src/BMCIlluminatiPass.sol:204`

```
            subscriptionId == 0 || keyHash == bytes32(0) || callbackGasLimit < MIN_CALLBACK_GAS_LIMIT
```

The only validation of keyHash is `keyHash != bytes32(0)`. The Ethereum mainnet VRFCoordinatorV2_5 (0xD7f86b4b8Cae7D942340FF628F82735b7a20893a, verified source read from Sourcify during this review) says in requestRandomWords: 'Note we do not check whether the keyHash is valid to save gas. The consequence for users is that they can send requests for invalid keyHashes which will simply not be fulfilled.' So a mistyped lane, a VRF v2 or Sepolia key hash pasted on mainnet, a retired lane, or a placeholder such as the keccak256('500 gwei lane') / keccak256('lane') values used throughout the repository's tests does not make mintMystery revert. Every mystery mint under such a config succeeds, burns 350,000 BMC, mints a Pending NFT and opens a request no VRF node will ever serve. The subscription cannot even be cancelled while that request is outstanding (cancelSubscription reverts with PendingRequestExists). README line 74 states 'A bad config only blocks new mystery mints until corrected': that is true for a wrong subscription id or a non-consumer (the request reverts and the burn rolls back, test_NotAConsumerReverts) but false for the key hash, and combined with strict in-order finalization (high finding) one such mint freezes all later reveals even after the owner corrects the config. This is an owner-trust power the brief asked to be reviewed; the defect is that the contract and documentation promise a fail-closed behaviour the code does not have, and the owner cannot tell from the chain that the lane is dead until the first reveal never arrives.

Registered mainnet lanes at review time (s_provingKeyHashes(0..2), read live at block 26174082): 0xc6bf2e7b88e5cfbb4946ff23af846494ae1f3c65270b79ee7876c9aa99d3d45f, 0x8077df514608a09f83e4e8d300645594e5d7234665448ba83f51a50f842bd3d9, 0x3fd2fec10d06ee8f65e7f2e95f5c56511359ece3f33960ad8a866ae24a8ff10b; s_provingKeys(keccak256('500 gwei lane')) and s_provingKeys(0x787d74caea10b2b357790d5b5247c2f63d1d91572a9846f780606e4d953677ae) both return (false, 0).

Fix: in setVRFConfig, staticcall `s_provingKeys(bytes32)` on the coordinator through a small interface (`(bool exists,) = IVRFProvingKeys(address(VRF_COORDINATOR)).s_provingKeys(keyHash); if (!exists) revert InvalidVRFConfig();`), or iterate s_provingKeyHashes(i) until it reverts and require a match. Add the recovery path from the high finding so that a lane retired after configuration is not permanent either, replace the placeholder lane wording in README step 4 with an instruction to read the lane from the coordinator, and fix README line 74.

**Reproduction**

Mainnet fork reproduction (block 26174090, --fork-url on an Ethereum mainnet RPC, test/scratch/ForkKeyHash.t.sol): deploy BMCIlluminatiPass(owner, 0x38224239f2BDae357D47cb864BC533d7f72dF961, 0xD7f86b4b8Cae7D942340FF628F82735b7a20893a); as subOwner createSubscription(), addConsumer(subId, pass), fundSubscriptionWithNative{value: 5 ether}(subId); owner setGenesisImagesCID(cid) and setVRFConfig(subId, keccak256('500 gwei lane'), 500000, 3, true) -> accepted; mint the 40 Genesis with deal()'d BMC; alice approves 350_000e18 and calls mintMystery(). Expected (README line 74): revert, nothing burned. Actual: returns (41, 26456405297011878279983700180394513608970340370262199527078277608063898672485), BMC.balanceOf(alice) == 0, BMC.totalSupply() dropped by 350_000e18, revealStatusOf(41) == AwaitingRandomness, coordinator.pendingRequestExists(subId) == true, and cancelSubscription(subId, subOwner) reverts. Local proof (no fork): forge test --match-path test/scratch/KeyHashNotValidated.t.sol -> FAIL 'setVRFConfig accepted a key hash the coordinator does not serve' after showing the 350,000 BMC burn; passes once setVRFConfig checks s_provingKeys(keyHash).exists on the coordinator.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {BMCIlluminatiPass} from "src/BMCIlluminatiPass.sol";

/// @dev Minimal 18-decimal token with OpenZeppelin ERC20Burnable-style burnFrom (spend allowance, destroy).
contract PocBMC {
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function decimals() external pure returns (uint8) {
        return 18;
    }

    function mint(address to, uint256 amount) external {
        balanceOf[to] += amount;
        totalSupply += amount;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }

    function burnFrom(address account, uint256 amount) external {
        uint256 a = allowance[account][msg.sender];
        require(a >= amount, "insufficient allowance");
        allowance[account][msg.sender] = a - amount;
        require(balanceOf[account] >= amount, "insufficient balance");
        balanceOf[account] -= amount;
        totalSupply -= amount;
    }
}

/// @dev Models the Ethereum mainnet VRFCoordinatorV2_5 (0xD7f86b4b8Cae7D942340FF628F82735b7a20893a):
///      `s_provingKeys(bytes32)` returns (exists, maxGas) and `requestRandomWords` deliberately does NOT
///      check the key hash ("requests for invalid keyHashes which will simply not be fulfilled").
contract PocCoordinator {
    struct RandomWordsRequest {
        bytes32 keyHash;
        uint256 subId;
        uint16 requestConfirmations;
        uint32 callbackGasLimit;
        uint32 numWords;
        bytes extraArgs;
    }

    struct ProvingKey {
        bool exists;
        uint64 maxGas;
    }

    mapping(bytes32 => ProvingKey) public s_provingKeys;
    bytes32[] public s_provingKeyHashes;
    uint256 public lastRequestId = 1000;
    mapping(uint256 => bytes32) public keyHashOfRequest;

    constructor() {
        bytes32 lane = 0xc6bf2e7b88e5cfbb4946ff23af846494ae1f3c65270b79ee7876c9aa99d3d45f;
        s_provingKeys[lane] = ProvingKey({exists: true, maxGas: 1e12});
        s_provingKeyHashes.push(lane);
    }

    function requestRandomWords(RandomWordsRequest calldata req) external returns (uint256 id) {
        id = ++lastRequestId;
        keyHashOfRequest[id] = req.keyHash;
    }
}

/// @title setVRFConfig accepts a key hash the coordinator will never fulfil
/// @notice The only check is `keyHash != 0`. The mainnet coordinator accepts requests for unregistered
///         key hashes and never fulfils them, so every mystery mint under such a config burns 350,000 BMC
///         for a token that stays pending forever. The README promises "A bad config only blocks new
///         mystery mints until corrected", which this shows to be false for the key hash.
///         Fails on the current code; passes once setVRFConfig verifies the key hash against the
///         coordinator (s_provingKeys(keyHash).exists, or a scan of s_provingKeyHashes) and reverts
///         InvalidVRFConfig otherwise.
contract KeyHashNotValidatedTest is Test {
    PocBMC bmc;
    PocCoordinator vrf;
    BMCIlluminatiPass pass;
    address owner = makeAddr("owner");
    address alice = makeAddr("alice");

    function setUp() public {
        bmc = new PocBMC();
        vrf = new PocCoordinator();
        pass = new BMCIlluminatiPass(owner, address(bmc), address(vrf));
        vm.prank(owner);
        pass.setGenesisImagesCID("bafybeihfihwwpev4gkqjuqawgtptsv3ynzsokclo6odsolvoa65aqaac2u");
        for (uint256 i = 0; i < 40; i++) {
            address who = address(uint160(0x1000 + i));
            bmc.mint(who, 1_000_000e18);
            vm.startPrank(who);
            bmc.approve(address(pass), 1_000_000e18);
            pass.mintGenesis();
            vm.stopPrank();
        }
    }

    function test_UnregisteredKeyHashIsRejectedBeforeAnyBMCIsBurned() public {
        bytes32 badKey = keccak256("500 gwei lane"); // the placeholder lane used across the repo's tests
        (bool exists,) = vrf.s_provingKeys(badKey);
        assertFalse(exists);

        vm.prank(owner);
        (bool accepted,) = address(pass).call(
            abi.encodeCall(pass.setVRFConfig, (1, badKey, 500_000, 3, false))
        );

        if (accepted) {
            // Current behaviour: the config is live and the next mystery mint burns BMC for a request
            // that no VRF node will ever fulfil.
            bmc.mint(alice, 350_000e18);
            vm.startPrank(alice);
            bmc.approve(address(pass), 350_000e18);
            (uint256 id, uint256 req) = pass.mintMystery();
            vm.stopPrank();
            assertEq(id, 41);
            assertEq(bmc.balanceOf(alice), 0, "350,000 BMC burned");
            assertEq(vrf.keyHashOfRequest(req), badKey, "request opened for a key hash no node serves");
        }
        assertFalse(accepted, "setVRFConfig accepted a key hash the coordinator does not serve");

        // A registered lane must still be accepted.
        bytes32 goodKey = vrf.s_provingKeyHashes(0);
        vm.prank(owner);
        pass.setVRFConfig(1, goodKey, 500_000, 3, false);
        (,, uint32 gasLimit,,, bool configured) = pass.vrfConfig();
        assertTrue(configured);
        assertEq(gasLimit, 500_000);
    }
}
```

### 3. Medium: mintMystery burns 350,000 BMC and opens a VRF request even when the subscription has no balance to pay for fulfilment

`src/BMCIlluminatiPass.sol:248`

```
        _burnExact(msg.sender, MYSTERY_PRICE);
```

The buyer's irreversible payment is taken before the only external dependency is checked for solvency. mintMystery checks cfg.configured and then relies on VRF_COORDINATOR.requestRandomWords reverting to roll back the burn (test_MysteryBurnRevertsIfVRFRequestFails, test_NotAConsumerReverts). But Chainlink VRF v2.5 accepts a request from a registered consumer whose subscription holds zero LINK and zero native balance; payment is only attempted at fulfilment. Chainlink's official VRFCoordinatorV2_5Mock, vendored in lib/ and used by the repository's own test_UnfundedSubscriptionKeepsTokenPendingUntilFunded, behaves the same and that test shows the mint succeeding on an empty subscription. Chainlink's documentation states such requests expire after 24 hours ('If your balance is below the minimum, your requests remain pending for up to 24 hours before they expire'), and the contract has no re-request path, so a buyer who mints while the subscription is empty, a state the buyer cannot see from the mint UI and that is controlled by the subscription owner (a privileged role distinct from the contract owner), permanently loses 350,000 BMC for a token that can never be revealed. Because reveals are strictly ordered that token also freezes every later reveal (high finding). The README text 'Chainlink VRF v2.5 keeps a request pending while the subscription is unfunded and fulfils it after funding' is contradicted by Chainlink's 24h expiry.

Fix: before _burnExact, read `(uint96 balance, uint96 nativeBalance,,,) = VRF_COORDINATOR.getSubscription(cfg.subscriptionId)` (IVRFCoordinatorV2Plus already inherits IVRFSubscriptionV2Plus, so no interface change) and revert with a new SubscriptionUnfunded error when the balance matching cfg.nativePayment is zero, or below an owner-set minimum bounded to a sane range. This fails closed exactly like the existing VRFNotConfigured path and changes no price, supply or artwork. It is a mitigation, not a guarantee (a balance above zero can still be below Chainlink's per-request minimum), which is why the recovery path from the high finding is still required. The existing test test_UnfundedSubscriptionKeepsTokenPendingUntilFunded must be rewritten with the fix (verified: it fails with 'subscription unfunded' once the check is added). Also surface pendingReveals and the subscription balance on the website so buyers can see the sale is healthy.

**Reproduction**

State: Chainlink VRFCoordinatorV2_5Mock (lib/chainlink), subscription created by subOwner, pass added as consumer, balance 0 LINK / 0 native. Owner setVRFConfig(subId, lane, 500000, 3, false). Phase 1 complete. alice holds 350_000e18 BMC and approves the pass. alice calls mintMystery(). Expected: revert, alice's balance 350_000e18, totalMinted 40, nothing burned. Actual: call succeeds, 350_000e18 BMC destroyed (totalSupply drops), token 41 minted AwaitingRandomness, request accepted; coordinator.fulfillRandomWords then reverts InsufficientBalance (shown by the repository's own test) and per Chainlink's documentation the request expires after 24h with no way to re-request. Run: forge test --match-path test/scratch/UnfundedSubscriptionBurn.t.sol -> FAIL 'mintMystery accepted a burn although the VRF subscription has no balance'; passes once mintMystery checks the matching subscription balance before burning (verified on a patched copy).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {VRFCoordinatorV2_5Mock} from "@chainlink/contracts/src/v0.8/vrf/mocks/VRFCoordinatorV2_5Mock.sol";
import {BMCIlluminatiPass} from "src/BMCIlluminatiPass.sol";

/// @dev Minimal 18-decimal token with OpenZeppelin ERC20Burnable-style burnFrom (spend allowance, destroy).
contract PocBMC {
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function decimals() external pure returns (uint8) {
        return 18;
    }

    function mint(address to, uint256 amount) external {
        balanceOf[to] += amount;
        totalSupply += amount;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }

    function burnFrom(address account, uint256 amount) external {
        uint256 a = allowance[account][msg.sender];
        require(a >= amount, "insufficient allowance");
        allowance[account][msg.sender] = a - amount;
        require(balanceOf[account] >= amount, "insufficient balance");
        balanceOf[account] -= amount;
        totalSupply -= amount;
    }
}

/// @notice mintMystery burns 350,000 BMC and opens a VRF request even when the configured subscription
///         holds no LINK and no native balance, so the request cannot be paid for. Chainlink's v2.5
///         coordinator accepts such requests (its official mock, used here, behaves the same) and, per
///         Chainlink's documentation, expires them after 24 hours if the subscription stays underfunded.
///         The contract has no re-request path, so the buyer's BMC is gone for a permanently pending token.
///         Expected: the mint fails closed (no burn), as it already does when the request itself reverts.
///         Actual: the burn succeeds and the pending token is minted.
///         This test fails on the current code and passes once mintMystery checks the subscription
///         balance that matches nativePayment (via VRF_COORDINATOR.getSubscription) before burning.
contract UnfundedSubscriptionBurnTest is Test {
    PocBMC bmc;
    VRFCoordinatorV2_5Mock coordinator;
    BMCIlluminatiPass pass;
    uint256 subId;

    address owner = makeAddr("owner");
    address subOwner = makeAddr("subscriptionOwner");
    address alice = makeAddr("alice");

    function setUp() public {
        bmc = new PocBMC();
        coordinator = new VRFCoordinatorV2_5Mock(0.1 ether, 1e9, 4e15);
        pass = new BMCIlluminatiPass(owner, address(bmc), address(coordinator));

        vm.startPrank(subOwner);
        subId = coordinator.createSubscription();
        coordinator.addConsumer(subId, address(pass));
        vm.stopPrank();
        // Subscription deliberately left with zero LINK and zero native balance.

        vm.startPrank(owner);
        pass.setGenesisImagesCID("bafytest");
        pass.setVRFConfig(subId, keccak256("lane"), 500_000, 3, false);
        vm.stopPrank();

        for (uint256 i = 0; i < 40; i++) {
            address who = address(uint160(0x7000 + i));
            bmc.mint(who, 1_000_000e18);
            vm.startPrank(who);
            bmc.approve(address(pass), 1_000_000e18);
            pass.mintGenesis();
            vm.stopPrank();
        }
    }

    function test_MysteryMintFailsClosedWhenSubscriptionCannotPayForFulfilment() public {
        (uint96 balance, uint96 nativeBalance,,,) = coordinator.getSubscription(subId);
        assertEq(balance, 0);
        assertEq(nativeBalance, 0);

        bmc.mint(alice, 350_000e18);
        uint256 supplyBefore = bmc.totalSupply();
        vm.startPrank(alice);
        bmc.approve(address(pass), 350_000e18);
        (bool ok,) = address(pass).call(abi.encodeCall(pass.mintMystery, ()));
        vm.stopPrank();

        assertFalse(ok, "mintMystery accepted a burn although the VRF subscription has no balance");
        assertEq(bmc.balanceOf(alice), 350_000e18, "buyer's BMC must be untouched");
        assertEq(bmc.totalSupply(), supplyBefore, "nothing may be burned");
        assertEq(pass.totalMinted(), 40, "no pending token may be minted");
    }
}
```

### 4. Low: Single-step Ownable: renounceOwnership or a mistyped transferOwnership before configuration permanently disables minting, and after it freezes a possibly-broken VRF config

`src/BMCIlluminatiPass.sol:40`

```
contract BMCIlluminatiPass is ERC721, Ownable, ReentrancyGuard {
```

The contract inherits OpenZeppelin's single-step Ownable, not Ownable2Step; transferOwnership(address) takes effect immediately and renounceOwnership() is available at any time. Both owner powers are prerequisites for minting: setGenesisImagesCID gates mintGenesis and mintMystery, setVRFConfig gates mintMystery, and setVRFConfig is load-bearing for the whole phase 2 because the subscription id and key hash depend on Chainlink-side state the contract does not control (three lanes exist on mainnet today; Chainlink has retired lanes before, and a subscription can be cancelled by its owner). If the owner key is lost (keystroke error in transferOwnership, compromised key renouncing, or the early renounce that README O-5 contemplates) before the CID is set, no token can ever be minted and the deployment is dead; if it happens before a working VRF config, or the configured lane or subscription later becomes invalid, requestRandomWords reverts inside every mintMystery (InvalidKeyHash / InvalidSubscription / InvalidConsumer) and phase 2 stops permanently short of 500 tokens with the remaining Genesis and Standard outcomes never minted. The README (line 76) only notes that renouncing 'freezes the VRF config forever' and does not spell out that the collection can then never complete. This is a documented trust assumption, reported because the brief asks for review of transferOwnership and renounceOwnership.

Fix preserving the design: inherit Ownable2Step (the pending owner must call acceptOwnership), and override renounceOwnership to revert unless genesisCIDLocked && vrfConfig.configured (or until totalMinted == MAX_SUPPLY), or disable it entirely. Using a multisig as owner (README O-5) is complementary.

**Reproduction**

1) Deploy BMCIlluminatiPass(owner, BMC, coordinator). 2) owner calls renounceOwnership() (or transferOwnership(0x000...dead), accepted in one step). 3) owner calls setGenesisImagesCID('bafy...') -> reverts OwnableUnauthorizedAccount. 4) mintGenesis() -> reverts GenesisCIDNotSet; mintMystery() -> reverts GenesisCIDNotSet. Expected: the configuration steps cannot be irrecoverably skipped by one call. Actual: the contract is permanently unusable and must be redeployed. Verified with test/scratch/Misc.t.sol::test_RenounceBeforeCID (passes on the current code, i.e. the lockout is real). Second input: totalMinted == 200, owner transfers to a mistyped address, Chainlink later retires the configured lane: every mintMystery reverts in requestRandomWords, setVRFConfig reverts OwnableUnauthorizedAccount, 300 tokens including all 37 mystery Genesis can never be minted.

### 5. Low: Documented verification commands fail: plain `forge test` fails on the fork test, `forge fmt --check` fails, and the recorded test count (43) is stale

`test/BMCMainnetFork.t.sol:27`

```
        require(block.chainid == 1, "Ethereum mainnet fork required");
```

README line 132 gives `forge build && forge test && forge fmt --check` as the test command, README line 19 and docs/TEST-RESULTS.md record 43 passing tests. The fork test hard-requires chain id 1 instead of skipping when no fork is configured, so plain `forge test` now reports 1 failing test out of 44, and the file is not formatted (leading blank line and a space before the SPDX header, wrapped constant declarations), so `forge fmt --check` exits 1. CI only passes because .github/workflows/main.yml excludes the contract with --no-match-contract and re-runs it with a secret RPC. A reviewer, or the contributor fixing any of the findings above, who follows the README sees a red suite unrelated to their change. The test itself is valuable: against a live mainnet fork it passes (verified in this review at block ~26174082: real BMC burnFrom destroys exactly 1,000,000e18 and totalSupply drops accordingly).

Fix: start the test with `string memory url = vm.envOr("MAINNET_RPC_URL", string("")); if (bytes(url).length == 0) { vm.skip(true); return; } vm.createSelectFork(url);` (or `if (block.chainid != 1) { vm.skip(true); return; }`), run `forge fmt`, and update README line 19 and docs/TEST-RESULTS.md to 44 tests with the fork test listed separately.

**Reproduction**

Fresh clone, no RPC: `forge test` -> 'Ran 3 test suites ... 43 tests passed, 1 failed, 0 skipped (44 total tests)' with '[FAIL: Ethereum mainnet fork required] test_RealBMCGenesisMint() (gas: 372)'. `forge fmt --check test/BMCMainnetFork.t.sol` -> exit code 1. `grep -c 'function test' test/*.sol` -> 39 + 1 + 4 = 44. Expected per README/TEST-RESULTS: all tests pass, formatting clean, 43 tests. With `--fork-url <mainnet RPC>` the test passes (verified).

### 6. Low: generate_genesis.py writes into the approved artwork/genesis directory by default and overwrites genesis-01.png .. genesis-77.png with no hash check; byte-identical regeneration depends on the Pillow

`artwork/tools/generate_genesis.py:196`

```
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "genesis")
```

Audit scope item 4 asks to confirm the generator cannot accidentally overwrite the approved premium Genesis files. It can: with no argument `out` resolves to artwork/genesis (line 196), os.makedirs(out, exist_ok=True) on line 197 accepts the existing directory, and img.save(...) on line 201 overwrites each of the 77 PNGs without an existence check, a hash comparison against the committed bytes, or a confirmation prompt. README line 133 even instructs running it against that directory. The 'byte-identical' claim depends on the installed Pillow release: the plate label is drawn with Pillow's default bitmap font (d.text with no font argument, line 191), GaussianBlur and the optimize=True PNG encoder have all changed output across Pillow versions, so a re-run on another machine can silently replace the approved artwork with visually similar but byte-different files. If the IPFS upload happens afterwards the directory CID changes, and setGenesisImagesCID locks whatever CID is uploaded forever. Determinism could not be verified in this environment (Pillow is not installed), so that part is reported as unverified; the unconditional overwrite is verified from the source.

Fix: default to a separate output directory (e.g. artwork/generated), refuse to write when a target file exists unless --force is passed, record the SHA-256 of the 77 approved files in the repository (e.g. artwork/genesis/SHA256SUMS; genesis-01.png today hashes to b35a60c9a4fb8227ca6dd4874dca5e9d3ef7948ac0ccdb7b770851e0ae11c406) and check the upload against them before setGenesisImagesCID, and pin the Pillow version in a requirements file.

**Reproduction**

State: artwork/genesis contains the 77 approved PNGs. Input: `python3 artwork/tools/generate_genesis.py` (no argument) with any Pillow version installed. Expected: the approved files are left untouched or the tool refuses. Actual: out == artwork/genesis, makedirs succeeds because exist_ok=True, and all 77 files are rewritten unconditionally by img.save on line 201; whether the bytes match the approved files depends on the installed Pillow release.

### 7. Info: README and NatSpec operational claims do not match measured behaviour: a 500k callback finalizes 3 reveals not 4, a 150k callback finalizes none, GAS_PER_REVEAL comment understates the cost, unfunded

`README.md:105`

```
   500k callback gas lets each callback finalize up to 4 reveals. `nativePayment=true` if funded with ETH.
```

Statements the operator will rely on do not match measured or documented behaviour. (1) README line 105: with callbackGasLimit 500,000 the callback has about 467k gas left after storing the word, batch = (467k - 30k) / 110k = 3, so at most 3 reveals run inline; 4 requires >= ~504k. (2) src line 94 says the per-reveal cost was 'measured ~85k'; a first permissionless finalizeReveals(1) measured in this review consumes 133,705 gas of execution (the ~85k figure appears to include end-of-transaction SSTORE refunds, which do not reduce gasleft()). At the minimum permitted MIN_CALLBACK_GAS_LIMIT = 150,000 the callback stores the word and finalizes nothing (batch == 0), so every reveal then depends on an unpaid finalizeReveals call. Nothing is lost on failure because the try/catch keeps the word, so this is informational, but the batch sizing margin in the 175k-250k band is under 10% against the 63/64 forwarding rule. (3) README lines 64-67 and NatSpec lines 38-39: Chainlink documents that requests on an underfunded subscription 'remain pending for up to 24 hours before they expire'; they are not fulfilled whenever funding arrives (this is the root of the high finding). (4) README line 19 and docs/TEST-RESULTS.md: the repository has 44 tests. Fix: recommend 550,000 callback gas (or re-measure and set GAS_PER_REVEAL to ~140k and raise MIN_CALLBACK_GAS_LIMIT so a callback can always store and finalize at least one token), correct the expiry wording, and refresh the counts.

**Reproduction**

Project MockVRFCoordinator (forwards exactly callbackGasLimit), phase 1 complete, setVRFConfig(1, lane, 500000, 3, false): mint tokens 41..46; deliver 46,45,44,43,42 with 95,000 gas (stored only, revealedCount == 0); deliver 41 with the request's own 500,000 gas. Expected per README: revealedCount() == 4. Actual: revealedCount() == 3 (test/scratch/Misc.t.sol::test_BatchAt500k prints 'revealed by 500k callback 3'). With callbackGasLimit 150,000: deliver 41 -> revealedCount() == 0; a fresh finalizeReveals(1) then costs 133,705 gas (test_BatchAt150k). `grep -c 'function test' test/*.sol` -> 44.

### 8. Info: Deploy script hard-codes mainnet addresses but never checks block.chainid == 1 or that the targets have code

`script/Deploy.s.sol:35`

```
        pass = deploy(mainnetConfig(owner));
```

run() always uses MAINNET_BMC and MAINNET_VRF_COORDINATOR and reads only OWNER from the environment; neither run() nor deploy() checks block.chainid or that cfg.bmc / cfg.vrfCoordinator have code. Run against any other RPC (a testnet rehearsal or a wrong --rpc-url), it deploys a contract pointing at addresses with no code there: setGenesisImagesCID succeeds, then every mintGenesis reverts inside BMC.decimals() (staticcall to an address without code returns no data and the ABI decoder reverts), so the deployment is useless while the deployer may believe the rehearsal represents mainnet. Fix: `require(block.chainid == 1, "mainnet only");` in run(), and in deploy() `require(cfg.bmc.code.length > 0 && cfg.vrfCoordinator.code.length > 0, "no code at dependency");`.

**Reproduction**

OWNER=<addr> forge script script/Deploy.s.sol:DeployBMCIlluminatiPass --rpc-url <any non-mainnet RPC> --broadcast: succeeds. On the resulting contract, after setGenesisImagesCID, mintGenesis() reverts with an empty revert from the decimals() staticcall to 0x38224239f2BDae357D47cb864BC533d7f72dF961 (no code on that chain). Expected: the script refuses to run off mainnet or against code-less dependencies.

### 9. Info: BurnMismatch reports the supply delta even when the payer-balance delta is the mismatching operand, and a supply or balance increase during burnFrom panics instead of reverting with BurnMismatch

`src/BMCIlluminatiPass.sol:280`

```
        if (supplyDelta != amount || balanceDelta != amount) revert BurnMismatch(amount, supplyDelta);
```

_burnExact checks two deltas but the error always carries supplyDelta. When the token destroys exactly `amount` of supply but not from `payer` (a burnFrom that burns from a treasury and only debits the payer a fee), supplyDelta == amount and balanceDelta != amount, so the revert data reads BurnMismatch(1000000e18, 1000000e18), which claims the burn matched. Separately, lines 278-279 compute supplyBefore - totalSupply() and balanceBefore - balanceOf(payer) with checked arithmetic; if either value grows during burnFrom (a token that mints a rebate or hooks a transfer back to the payer) the call reverts with Panic(0x11) rather than BurnMismatch. Both paths fail closed so there is no loss; the diagnostics are misleading, which matters because this error is the contract's sole on-chain evidence about an unexpected BMC behaviour. Fix: compare before/after values without subtraction that can underflow and report both deltas, e.g. `revert BurnMismatch(amount, supplyDelta, balanceDelta)`, or two distinct errors.

**Reproduction**

Deploy with a mock whose burnFrom(account, amount) does _spendAllowance(account, msg.sender, amount), _burn(treasury, amount) and _transfer(account, treasury, amount / 100). Fund payer with 1_000_000e18, approve, call mintGenesis(). Expected: a revert identifying the payer-balance mismatch (balance fell by 10_000e18 instead of 1_000_000e18). Actual: revert BurnMismatch(1000000000000000000000000, 1000000000000000000000000). Second input: a mock whose burnFrom mints amount*2 to account before burning amount; expected BurnMismatch, actual Panic(0x11) from line 279. Both verified by test/scratch/Misc.t.sol::test_BurnMismatchDiag (expectRevert with exactly those payloads passes on the current code).

### 10. Info: Immutable coordinator with no setCoordinator: subscription migrate() reverts for this consumer and a coordinator deprecation strands all future mystery mints (accepted trust dependency, undocumented c

`src/BMCIlluminatiPass.sol:99`

```
    IVRFCoordinatorV2Plus public immutable VRF_COORDINATOR;
```

The coordinator is immutable by design (docs/SECURITY-REVIEW.md F-3), which removes the owner's reroll-by-proxy power and is the right call. Two consequences should be stated as accepted risks. (1) The live VRFCoordinatorV2_5.migrate(subId, newCoordinator) (verified source read from Sourcify during this review) loops over the subscription's consumers and calls `IVRFMigratableConsumerV2Plus(consumers[i]).setCoordinator(newCoordinator)`; the pass has no such function and no fallback, so the subscription owner cannot migrate a subscription that lists the pass as a consumer (the call reverts) and must removeConsumer first, which itself requires no pending request. (2) If Chainlink retires the v2.5 coordinator or all its lanes during the sale, mintMystery either reverts (no consumer / no subscription) or keeps burning BMC for requests nobody fulfils (key-hash finding), and any request outstanding at that moment freezes all later reveals (high finding). The README mentions decommissioning only for 'affected tokens'. Recommendation: keep the immutable coordinator, document these outcomes, keep the sale window short relative to Chainlink's deprecation notice periods, and rely on the recovery path from the high finding.

**Reproduction**

On the verified mainnet coordinator source, migrate() contains `for (uint256 i = 0; i < consumers.length; ++i) { IVRFMigratableConsumerV2Plus(consumers[i]).setCoordinator(newCoordinator); }`. With the pass registered as a consumer, the external call hits a contract with neither a setCoordinator(address) selector nor a fallback, so migrate reverts. Expected by a subscription owner: migration proceeds; actual: revert until the pass is removed as consumer.

### 11. Info: Public without-replacement pool makes blocked and late mystery outcomes knowable before finalization

`src/BMCIlluminatiPass.sol:334`

```
        uint256 r = uint256(keccak256(abi.encode(word, tokenId))) % remaining;
```

Two information effects of the design, not permission bypasses, that affect who pays 350,000 BMC for what. (a) `remaining` depends only on revealedCount, so for a token whose word is stored but which is blocked behind an earlier AwaitingRandomness token, r is already fixed and _slotValue(r) is the outcome unless an earlier blocked draw lands on the same slot. The word is also emitted in RandomnessStored. Anyone reading the chain knows the near-certain tier of a 'Pending' token; a marketplace buyer who does not will overpay for a known-Standard token or be front-run on a known-Genesis one. (b) The inventory is public (remainingMysteryGenesis / remainingMysteryStandard). Once all 37 mystery Genesis are drawn, every remaining mystery mint is a guaranteed Standard at the same 350,000 BMC; conversely with one Genesis slot left and one mint left, the final mint is a guaranteed Genesis for 350,000 BMC versus the 1,000,000 BMC Genesis price, and the last mints become a gas auction. The website already shows provisional odds, so this is informational: document both effects for buyers, consider not emitting the raw word, and have the website refuse to show 'odds' once they are 0% or 100%.

**Reproduction**

(a) Phase 1 done; mint 41 (request never fulfilled) and 42; deliver 42's word w = keccak256('w42'). Compute r = uint256(keccak256(abi.encode(w, 42))) % 460 = 235 off-chain (test/scratch/Misc.t.sol::test_KnowableOutcome); r >= 37 so token 42 is Standard artwork 199 as soon as 41 is finalized, while tokenURI(42) still says 'Pending Reveal' and tierOf(42) == Pending. (b) State revealedCount == 459, mysteryGenesisRevealed == 36, totalMinted == 499: currentPrice() == 350_000e18 and the next mintMystery() is certain to draw the last Genesis (remaining == 1, the only slot left is < 37).

---

Judge's submission `bba3408249ecfbcc380e9ec156b5fd47764d26de344da792a3935f385a40bb39`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
