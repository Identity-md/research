# Audit report

> Audit the assembled Hooks Store contracts at commit 50a73539a8619881cb1e0644e1d9d12df7f6c5e4, especially HookListingRegistry, FeaturedPlacements and HookJobRequester. Test ad-deposit accounting, refunds, settlement, withdrawals, reentrancy, recipient changes, listing ownership and metadata revisions, false audit claims, admin powers, and Intake/oracle callback forgery or replay. Reproduce material findings with Foundry tests. Distinguish local mock tests from unverified live IMD integration; nothing has been deployed.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1811-build-technical-foundation-hooks.git |
| Commit | `50a73539a8619881cb1e0644e1d9d12df7f6c5e4` |
| Job | `d9970905-4ad2-4107-a50e-bccd5a1cff0d` |
| Judged | 2026-10-16 02:33 UTC |
| Findings | 1 medium · 2 low · 2 info |

Four agents audited the code as it is at `50a7353`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: onReviewResult never binds the signed attestation to the ask it settles: a verdict signed for one review ask is accepted as another job's verdict

`src/imd/HookJobRequester.sol:284`

```
        _verifyAttestation(a, signature);
```

onReviewResult(requestId, a, signature) looks up the pending ask with the Intake-supplied callback argument requestId (reviewOf[requestId]), checks the panel minimums, verifies the EIP-712 signature over `a` in this contract's domain and consumes a.requestId as a replay key. It never checks that the attestation answers the ask being settled: a.requestId is not compared with requestId, a.questionHash is only emitted (the contract stores no hash of the review body it sent, unlike job.bodyHash for jobs), and a.chainId is unchecked. Every attestation the oracle genuinely signs for this consumer is therefore interchangeable across all of this consumer's pending asks. Whoever drives the Intake's completion path (the Intake operator, its upgrade admin, or a routing bug in it) can deliver the oracle's honest 'passed' answer for job B's ask as job A's verdict: job A becomes ReviewStatus.Passed with B's panel size, agreement and panelJobId, reviewOf[askA] is cleared, and because consumed[askB] is now true the genuine delivery for job B later reverts AlreadyConsumed so the job that was actually reviewed can never record that verdict. The same gap lets a still-valid attestation issued for an earlier, expired ask of the same job settle its re-ask, and lets an answer to a different question template settle a current ask. This contradicts the contract header (lines 14-17), docs/IMD_INTEGRATION.md step 5 ('it answers this contract's own pending ask') and docs/THREAT_MODEL.md row 'Forged IMD result, review verdict or replay', all of which state the verdict does not depend on the Intake. The existing suite signs every attestation with requestId keccak256('oracle uuid'), unrelated to any ask id, so it exercises the gap rather than catching it. Rated medium: not reachable by a stranger (onlyIntake holds), but defending the Passed badge against exactly this party is the stated purpose of the signature, and the Passed status is what the static site shows as the IMD oracle panel attestation. Reported by four specialists (audit_flow, audit_math, audit_economics, audit_permissions); merged here. Fix: before _verifyAttestation, `if (a.requestId != requestId) revert UnknownOrSettled(requestId);` (confirm in the pilot that the live Intake's bytes32 id equals the attestation's left-aligned UUID; if the encodings differ, record the mapping at requestReview and compare the canonical form). Additionally store keccak256(body) at requestReview and require a.questionHash to match if the pilot shows the oracle hashes the body as sent, and consider checking a.chainId against the template's chain. Update the existing tests to sign the real ask id.

**Reproduction**

State (local mock Intake, nothing deployed): one requester, two jobs A and B opened by the same creator, both reported delivered by the Intake, creator calls requestReview for each, giving pending asks askA != askB. The oracle signer key signs attestation aB = {requestId: askB, questionHash: keccak256(B's review body), answerType: BOOL, answer: abi.encode(true), panelSize 7, quorum 5, agreed 6, issuedAt now, expiresAt now+1h} over requester.attestationDigest(aB). Input: the Intake calls onReviewResult(askA, aB, sig). Expected: revert (aB names askB, not askA); job A stays Pending, reviewOf(askA) == A, consumed(askB) == false. Actual: the call succeeds, getJob(A).review == Passed with aB's panel data, reviewOf(askA) deleted, consumed(askB) == true; a later onReviewResult(askB, aB, sig) reverts AlreadyConsumed. Verified: `forge test --match-path test/scratch/Proof_a67604f0c4be.t.sol` fails on this commit with 'next call did not revert as expected' (as do the two other specialists' equivalent proofs); with the one-line `if (a.requestId != requestId) revert UnknownOrSettled(requestId);` inserted before _verifyAttestation the same tests pass.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {HookJobRequester} from "src/imd/HookJobRequester.sol";
import {OracleAttestation} from "src/imd/OracleAttestation.sol";
import {IIntake} from "src/imd/IIntake.sol";

/// @dev Minimal ERC-20 for the proof: returns true, no hooks.
contract ProofToken {
    uint8 public constant decimals = 18;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function mint(address to, uint256 amount) external {
        balanceOf[to] += amount;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        allowance[from][msg.sender] -= amount;
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        return true;
    }
}

/// @dev Minimal Intake v2 stand-in: sells two actions, pulls exactly the price, hands out fresh ids.
contract ProofIntake is IIntake {
    uint256 public price;
    address public asset;
    uint256 internal nonce;

    constructor(address asset_, uint256 price_) {
        asset = asset_;
        price = price_;
    }

    function priceOf(bytes32, address asset_) external view returns (uint256) {
        return asset_ == asset ? price : 0;
    }

    function request(bytes32, bytes calldata, Callback calldata, address, uint256 amount)
        external
        payable
        returns (bytes32)
    {
        return _pull(amount);
    }

    function requestWithFailure(bytes32, bytes calldata, Callback calldata, bytes4, address, uint256 amount)
        external
        payable
        returns (bytes32)
    {
        return _pull(amount);
    }

    function _pull(uint256 amount) internal returns (bytes32 id) {
        require(amount == price, "wrong amount");
        require(ProofToken(asset).transferFrom(msg.sender, address(this), amount), "pull failed");
        // UUID-shaped ids, as the live plane issues them: sixteen bytes, left-aligned.
        id = bytes32(uint256(++nonce) << 128);
    }
}

/// @title A signed verdict for one review ask must not settle another pending ask
/// @notice Fails on the current code: `onReviewResult(requestId, a, sig)` checks only that
/// `requestId` is a pending ask of this contract and that `a` is signed by the oracle for this
/// contract. It never compares `a.requestId` (or `a.questionHash`) with the ask it settles, so the
/// honest "passed" answer to job B's question is accepted as job A's verdict.
contract ReviewAttestationBindingTest is Test {
    bytes32 internal constant JOB_ACTION = "job.open@test";
    bytes32 internal constant ORACLE_ACTION = "oracle.request@oracle-1";
    uint256 internal constant PRICE = 0.5 ether;

    ProofToken internal imd;
    ProofIntake internal intake;
    HookJobRequester internal requester;
    address internal owner = makeAddr("owner");
    address internal creator = makeAddr("creator");
    uint256 internal signerKey = uint256(keccak256("local test oracle key"));

    function setUp() public {
        vm.chainId(31337);
        vm.warp(1_800_000_000);
        imd = new ProofToken();
        intake = new ProofIntake(address(imd), PRICE);
        requester = new HookJobRequester(owner, address(intake), address(imd), vm.addr(signerKey), PRICE);
        vm.startPrank(owner);
        requester.setJobTemplate(
            JOB_ACTION, "forge build, forge test, adversarial review. spec ", " brief <brief>", "</brief>"
        );
        requester.setReviewTemplate(ORACLE_ACTION, "Did job ", " pass its adversarial review?", 5, 4);
        vm.stopPrank();
        imd.mint(creator, 10 ether);
        vm.prank(creator);
        imd.approve(address(requester), type(uint256).max);
    }

    function _deliveredJob(bytes32 specHash) internal returns (bytes32 jobId) {
        vm.prank(creator);
        jobId = requester.openJob(specHash, "a hook");
        vm.prank(address(intake));
        requester.onJobResult(jobId, "ipfs://result");
    }

    function _reviewPending(bytes32 specHash) internal returns (bytes32 jobId, bytes32 oracleId) {
        jobId = _deliveredJob(specHash);
        vm.prank(creator);
        oracleId = requester.requestReview(jobId);
    }

    /// @dev The oracle's honest answer to one specific ask: it names that ask's request id and
    /// the hash of that ask's question body.
    function _honestAnswer(bytes32 oracleId, bytes32 jobId, bool passed)
        internal
        view
        returns (OracleAttestation.Attestation memory a)
    {
        bytes memory question = bytes.concat("Did job ", bytes(vm.toString(jobId)), " pass its adversarial review?");
        a = OracleAttestation.Attestation({
            requestId: oracleId,
            chainId: 31337,
            questionHash: keccak256(question),
            answerType: OracleAttestation.ANSWER_BOOL,
            answer: abi.encode(passed),
            figure: 0,
            fromBlock: 1,
            toBlock: 2,
            blockHash: bytes32(uint256(3)),
            panelJobId: keccak256("panel job"),
            panelSize: 7,
            quorum: 5,
            agreed: 6,
            issuedAt: uint64(block.timestamp),
            expiresAt: uint64(block.timestamp + 1 hours)
        });
    }

    function _sign(OracleAttestation.Attestation memory a) internal view returns (bytes memory) {
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(signerKey, requester.attestationDigest(a));
        return abi.encodePacked(r, s, v);
    }

    function testAnswerForAnotherAskCannotSettleThisOne() public {
        // Job A: the one whose review should NOT pass (no verdict was ever signed for it).
        (bytes32 jobA, bytes32 askA) = _reviewPending(keccak256("spec A"));
        // Job B: the oracle honestly signs "passed" for B's ask, naming B's request id and question.
        (bytes32 jobB, bytes32 askB) = _reviewPending(keccak256("spec B"));
        assertTrue(askA != askB, "distinct asks");
        OracleAttestation.Attestation memory answerForB = _honestAnswer(askB, jobB, true);
        bytes memory sig = _sign(answerForB);

        // The relay delivers B's signed answer under A's ask. The attestation says requestId = askB
        // and questionHash = hash(B's question); the callback says askA. Expected: refused.
        vm.prank(address(intake));
        vm.expectRevert();
        requester.onReviewResult(askA, answerForB, sig);

        assertEq(uint8(requester.getJob(jobA).review), uint8(HookJobRequester.ReviewStatus.Pending), "A unsettled");
        assertEq(requester.reviewOf(askA), jobA, "A's ask still pending");
        assertFalse(requester.consumed(askB), "B's answer not consumed by A");

        // Delivered under its own ask, the same answer settles B as Passed.
        vm.prank(address(intake));
        requester.onReviewResult(askB, answerForB, sig);
        assertEq(uint8(requester.getJob(jobB).review), uint8(HookJobRequester.ReviewStatus.Passed));
        assertEq(uint8(requester.getJob(jobA).review), uint8(HookJobRequester.ReviewStatus.Pending));
    }
}
```

### 2. Low: HookJobRequester ownership is single-step with no zero-address check (solmate Owned), unlike the store's two-step StoreAdmin; one wrong transferOwnership permanently removes signer and Intake rotation

`src/imd/HookJobRequester.sol:21`

```
contract HookJobRequester is OracleAttestationConsumer, Owned {
```

HookJobRequester inherits solmate's Owned, whose transferOwnership(newOwner) writes `owner = newOwner` immediately with no zero-address check and no acceptance step (lib/solmate/src/auth/Owned.sol). The constructor rejects owner_ == address(0) but the running contract does not. FeaturedPlacements deliberately uses StoreAdmin's two-step propose/accept that refuses address(0) and address(this). The requester's owner is the only party able to rotate the oracle signer (setOracleSigner, needed for the documented IdentityMD signer rotation), move to a new Intake (setIntake), raise maxPrice after a published price move (setPayment), change templates, timeouts and the failure hook, and recover stuck tokens (sweep). A zero or mistyped argument makes all of these unreachable forever; after the next signer rotation every onReviewResult reverts BadSignature and each paid review ask ends Unanswered. docs/IMD_INTEGRATION.md tells operators to put ownership behind a multisig but not that the handover is one-step. This is a hardening of the intended owner role, not a change to it. Reported by three specialists; merged. Fix: give HookJobRequester the same two-step, zero-checked rotation as StoreAdmin (reuse StoreAdmin in place of Owned, or override transferOwnership to require a nonzero pending owner who accepts).

**Reproduction**

State: HookJobRequester deployed with owner O. Input: O calls transferOwnership(address(0)). Expected: revert, or a pending proposal that O can cancel and O keeps control. Actual: the call succeeds, owner() == address(0), and setOracleSigner, setIntake, setPayment, setJobTemplate, setReviewTemplate, setTimeouts, setFailureHook and sweep revert 'UNAUTHORIZED' for every caller from then on. Verified: `forge test --match-path test/scratch/Proof_ce672e6dacae.t.sol` fails on this commit with 'ownership must not be lost in one step'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {HookJobRequester} from "src/imd/HookJobRequester.sol";

contract Dummy {
    function priceOf(bytes32, address) external pure returns (uint256) {
        return 1;
    }
}

/// @title HookJobRequester ownership can be handed to the zero address in one step
/// @notice `HookJobRequester` inherits solmate `Owned`, whose `transferOwnership` is single-step and
/// has no zero-address check, unlike `StoreAdmin` used by `FeaturedPlacements`. A mistyped or
/// zero argument permanently removes the only authority that can rotate the oracle signer, the
/// intake, templates, the price ceiling or sweep stuck tokens.
contract OneStepOwnershipToZeroTest is Test {
    HookJobRequester internal requester;
    address internal owner = makeAddr("owner");

    function setUp() public {
        Dummy intake = new Dummy();
        Dummy asset = new Dummy();
        requester = new HookJobRequester(owner, address(intake), address(asset), makeAddr("signer"), 1 ether);
    }

    function testOwnershipCannotBeHandedToZeroInOneStep() public {
        vm.prank(owner);
        (bool ok,) = address(requester).call(abi.encodeWithSignature("transferOwnership(address)", address(0)));
        // Expected: the transfer is refused (reverts) or stays pending until accepted; the current
        // owner keeps control. Actual: the call succeeds and `owner` becomes address(0).
        assertTrue(!ok || requester.owner() == owner, "ownership must not be lost in one step");
        vm.prank(owner);
        requester.setOracleSigner(makeAddr("rotated signer"));
    }
}
```

### 3. Low: Signature verification switches to ERC-1271 only as soon as the oracle signer address has code, so an EIP-7702 delegation by the signer EOA makes every verdict fail BadSignature

`src/imd/OracleAttestation.sol:162`

```
        if (!SignatureChecker.isValidSignatureNowCalldata(oracleSigner, attestationDigest(a), signature)) {
```

The vendored OpenZeppelin SignatureChecker.isValidSignatureNowCalldata branches on signer.code.length: with code present it never attempts ECDSA recovery and only staticcalls isValidSignature on the signer address. The documented oracle signer (0x5598aa91...2982) is a plain key and the target chains support EIP-7702, under which an EOA that signs one delegation carries a 23-byte 0xef0100 designator while still producing ordinary ECDSA signatures. If the IdentityMD signer key ever delegates (wallet batching features, or a delegation to a contract without ERC-1271 support for the raw key), every attestation it signs for this consumer fails with BadSignature inside the Intake's try; reviews sit Pending until expireReview, each paid 0.5 IMD review ask ends Unanswered, and the only remedy is the owner pointing oracleSigner elsewhere. The project's tests run on evm_version cancun and never exercise a signer with code. Reported by audit_permissions; reproduced. Fix: attempt ECDSA recovery against oracleSigner first and fall back to ERC-1271 only when recovery does not yield it (OpenZeppelin's own EIP-7702 guidance), or document that the signer key must never delegate and point oracleSigner at an ERC-1271 registry from the start.

**Reproduction**

State: a pending review ask; attestation a = {requestId: ask, BOOL, answer true, panelSize 7, quorum 5, agreed 6, valid 1h} signed by the configured signer key (sanity: delivered as-is it settles the ask as Passed). Then the signer address acquires a 7702-shaped designator (locally vm.etch(signer, 0xef0100 ++ 20-byte delegate with no ERC-1271); on chain a 7702 delegation by the key). Input: the Intake calls onReviewResult(ask, a, sig). Expected: an ECDSA signature by the configured key is accepted. Actual: revert BadSignature(); review stays Pending. Verified by test/scratch/JudgeChecks.t.sol::testSignerWithCodeRejectsEcdsa (passes, i.e. asserts the behaviour described).

### 4. Info: Owner powers are understated in docs: setIntake plus setOracleSigner let the owner settle or forge verdicts for asks already pending and deliveries for jobs already open, not only 'jobs opened afterwa

`src/imd/HookJobRequester.sol:339`

```
    function setIntake(address to) external onlyOwner {
```

docs/IMD_INTEGRATION.md line 63 says a malicious owner 'could point the intake or signer at a contract they control and forge review verdicts for jobs opened afterwards'. onlyIntake and _verifyAttestation read the current intake and oracleSigner, and neither jobs nor reviewOf record which intake or signer was configured when the ask was made. The owner can therefore, in one transaction, set intake to itself and the signer to its own key, call onReviewResult for any already-Pending ask (or onJobResult / onJobFailure for any already-Open job) with a self-signed attestation, and restore the real values; the Passed badge the static site shows for an existing job is then owner-forged, distinguishable only by the surrounding IntakeSet/OracleSignerSet events. This is the documented trust assumption (multisig owner), not a permission bypass; the defect is that the documented scope of the power is wrong and there is no timelock or per-ask pinning. Reported by audit_permissions; reproduced. Minimal fix: correct the doc. Optionally record the intake and signer at requestReview/openJob and check the callbacks against them so a rotation cannot retroactively settle earlier asks.

**Reproduction**

State: job J delivered, review ask pending with the real intake and signer configured. Input: owner calls setIntake(owner), setOracleSigner(vm.addr(ownerKey)), then onReviewResult(ask, a, sig) with a signed by ownerKey in this contract's domain, then restores intake and signer. Expected per the docs: not possible for a job already open/pending. Actual: getJob(J).review == Passed. Verified by test/scratch/JudgeChecks.t.sol::testOwnerCanForgeVerdictForAlreadyPendingAsk (passes, i.e. asserts the behaviour described).

### 5. Info: After a listing transfer, the seller's live placement blocks the buyer from advertising for up to 7 days, keeps rendering the seller's revision and payer, and only the seller can cancel it

`src/store/FeaturedPlacements.sol:159`

```
        if (previous.status == Status.Open && block.timestamp < previous.endsAt) revert AlreadyFeatured();
```

purchase() admits only the current listing owner but refuses a second live placement per listing regardless of who paid it (AlreadyFeatured), while cancel() admits only the original payer (NotPayer). Combined with HookListingRegistry's two-step transfer, a seller can buy a 7-day ad (pinning the seller's revision and payer) right before the buyer accepts; the buyer can then neither cancel it nor advertise the listing until endsAt, while the seller keeps the right to cancel at any time and collect the pro-rata refund. No funds are at risk (the escrow refunds only the payer) and docs/LISTINGS_AND_ADS.md documents each rule individually ('A later owner cannot cancel', 'At most one live placement per listing'), so this is a design consequence to surface to buyers rather than a permission bypass. Reported by three specialists; merged. If unwanted, the minimal change preserving the economics is to let the current listing owner cancel a placement whose payer is no longer the owner, with the refund still credited to the original payer (or to let the new owner's purchase supersede such a placement the same way).

**Reproduction**

State: Alice creates listing L (revision 1), deposits 0.1 IMD, purchases placement P for L; Alice proposes Bob; Bob accepts and deposits 0.1 IMD. Inputs: Bob calls purchase(L, 1, treasury, now) -> reverts AlreadyFeatured; Bob calls cancel(P) -> reverts NotPayer. One day later Alice calls cancel(P) -> succeeds, refund = 0.1 IMD - floor(0.1 IMD * 1 day / 7 days) credited to Alice's available balance, after which Bob's purchase succeeds. Expected (buyer's view): Bob can clear or replace the ad on the listing he now owns. Verified by test/scratch/JudgeChecks.t.sol::testPreviousOwnersPlacementBlocksNewOwner (passes, i.e. asserts the behaviour described).

---

Judge's submission `cbad25df33185ebd13018dce7ceaf1601191ec7d4598f18d2b3c70af6afbb4ab`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
