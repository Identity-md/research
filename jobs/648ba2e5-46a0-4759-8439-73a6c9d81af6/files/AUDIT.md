# Audit report

> Audit commit eb1333775e60fe191acfa5a420e9256feeb4a2b0 against all six findings in report 6b607200-d29f-4c7a-8476-0dca8091f48f. Reproduce the expiry race, wrong pre-binding, abandoned ask, compromised-signer recovery, partial Intake spending, and price-change cases. Adversarially check the new owner reset/revocation powers, negative-verdict shopping, replay, exact IMD accounting and listing/ad escrow regressions. Re-measure the one-shot callback under 200k gas, especially the new mismatched pre-binding path. Identify material blockers and unverified live-Intake assumptions. Do not deploy.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1811-build-technical-foundation-hooks.git |
| Commit | `eb1333775e60fe191acfa5a420e9256feeb4a2b0` |
| Job | `648ba2e5-46a0-4759-8439-73a6c9d81af6` |
| Judged | 2026-10-16 14:51 UTC |
| Findings | 5 low · 5 info |

Four agents audited the code as it is at `eb13337`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Owner can void a genuine NotPassed receipt and unlock a paid retry through discard; the ReviewReceiptMatches guard is not a boundary (documented owner trust, incl. the new reset route)

`src/imd/HookJobRequester.sol:557`

```
            if (!consumed[oracleRequestId] && (holder == bytes32(0) || holder == intakeRequestId)) {
```

Merged from audit_math 1e90eece, audit_economics 79235e6e, audit_flow 81930d31 and audit_permissions 5c1d4f94. A requester cannot shop a verdict: a retained NotPassed blocks expireReview, confirmReviewExpiry and requestReview, and a bound matching callback finalizes atomically. The owner, however, can close any retained negative as Unanswered and the requester may then buy a new ask, by four routes that all reproduce on this commit: (1) discardReviewReceipt's misdelivery branch accepts ANY unconsumed, unreserved bytes32 as the 'true' UUID; no mapping proof is checked, so one call suffices; (2) pre-bind a wrong UUID W, let the real answer be retained, resetReviewBinding (W is released), then discard with W; (3) the 'borrowed conflict': bind an unrelated pending ask B to the receipt's own UUID X, discard A under the same-UUID branch with reason 'receipt UUID conflict' (the guard at line 557 counts a reservation that resetReviewBinding can remove), then reset B so no onchain inconsistency remains; (4) confirmReviewExpiry after the deadline before a late callback lands, which then reverts UnknownOrSettled and is lost. Route (3) is the only one that was impossible before this commit (a reservation used to be permanent), and it is the one the AUDIT_6B607200.md guarantee 'a field typo, negative value or elapsed time alone cannot justify discard' is meant to exclude. Because route (1) is a strictly cheaper, sanctioned equivalent for the same actor, this is not a permission bypass but an owner trust assumption: a Passed/NotPassed badge is only as trustworthy as the owner key, and ReviewReceiptDiscarded, ReviewBindingReset and ReviewUnanswered events on the same ask are the audit trail. Consistency fix that keeps the reset feature: in the same-UUID branch count only permanent conflicts (consumed[oracleRequestId]) or make resetReviewBinding/releaseReservation refuse a reservation that was used as conflict evidence; and document that the misdelivery branch is an unverified owner assertion. The attached proof encodes route (3) and fails on this code.

**Reproduction**

Fixture: test/HookJobRequester.t.sol HookJobRequesterFixture (owner, creator, MockIntake, PRICE 0.5e18). Route 1: creator openJob + intake.complete + requestReview -> unbound ask A; Intake delivers a valid attestation (UUID X, answer false) -> retained, review Pending. Owner: discardReviewReceipt(A, bodyHashA, keccak256('any unused uuid'), a.questionHash, 31337, 1, 2) -> succeeds, reason 'misdelivered receipt'; getJob(J).review == Unanswered; consumed[X] == false; creator.requestReview(J, 0.5e18) succeeds (test/scratch/JudgeProbe.t.sol testOwnerDiscardsGenuineNegativeWithAnyUnusedUuid). Route 3: same retained A; second user's unbound ask B; owner bindReview(B, bodyHashB, X, qA, 31337, 1, 2); discardReviewReceipt(A, bodyHashA, X, qA, 31337, 1, 2). Expected per the documented guard: revert ReviewReceiptMatches(A). Actual: succeeds with reason 'receipt UUID conflict'; owner resetReviewBinding(B, bodyHashB) leaves intakeReviewOfOracle[X] == 0 and consumed[X] == false; creator.requestReview(J, 0.5e18) opens a new Pending ask. The attached proof fails on this commit with 'genuine NotPassed discarded through a resettable, borrowed reservation'. Route 2: testResetThenDiscardWithReleasedUuid; route 4: testOwnerExpiryBurnsLateCallback (late intake.complete returns false, retry succeeds).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {HookJobRequester} from "src/imd/HookJobRequester.sol";
import {IIntake} from "src/imd/IIntake.sol";
import {OracleAttestation} from "src/imd/OracleAttestation.sol";

contract ScratchToken {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function decimals() external pure returns (uint8) {
        return 18;
    }

    function mint(address to, uint256 a) external {
        balanceOf[to] += a;
    }

    function approve(address s, uint256 a) external returns (bool) {
        allowance[msg.sender][s] = a;
        return true;
    }

    function transfer(address to, uint256 a) external returns (bool) {
        balanceOf[msg.sender] -= a;
        balanceOf[to] += a;
        return true;
    }

    function transferFrom(address f, address to, uint256 a) external returns (bool) {
        allowance[f][msg.sender] -= a;
        balanceOf[f] -= a;
        balanceOf[to] += a;
        return true;
    }
}

/// @dev Asynchronous one-shot Intake: pulls exactly the price, later calls back once with 200k gas.
contract ScratchIntake {
    mapping(bytes32 => mapping(address => uint256)) public priceOf;
    mapping(bytes32 => address) public target;
    mapping(bytes32 => bytes4) public sel;
    mapping(bytes32 => bytes) public bodyOf;
    uint256 nonce;

    function setPrice(bytes32 action, address asset, uint256 p) external {
        priceOf[action][asset] = p;
    }

    function requestWithFailure(
        bytes32 action,
        bytes calldata body,
        IIntake.Callback calldata cb,
        bytes4,
        address asset,
        uint256 amount
    ) external returns (bytes32 id) {
        require(amount == priceOf[action][asset]);
        ScratchToken(asset).transferFrom(msg.sender, address(this), amount);
        id = keccak256(abi.encode(++nonce));
        target[id] = cb.target;
        sel[id] = cb.selector;
        bodyOf[id] = body;
    }

    function complete(bytes32 id, bytes calldata args) external returns (bool ok) {
        (ok,) = target[id].call{gas: 200_000}(bytes.concat(sel[id], args));
    }
}

contract ResetConflictShoppingTest is Test {
    bytes32 constant JOB = "job.open@test";
    bytes32 constant ORACLE = "oracle.request@test";
    uint256 constant PRICE = 0.5 ether;
    ScratchToken imd;
    ScratchIntake intake;
    HookJobRequester req;
    address owner = makeAddr("owner");
    address creator = makeAddr("creator");
    address other = makeAddr("other");
    uint256 key = 0xA11CE;

    function setUp() public {
        vm.warp(1_800_000_000);
        imd = new ScratchToken();
        intake = new ScratchIntake();
        intake.setPrice(JOB, address(imd), PRICE);
        intake.setPrice(ORACLE, address(imd), PRICE);
        req = new HookJobRequester(owner, address(intake), address(imd), vm.addr(key), PRICE);
        vm.startPrank(owner);
        req.setJobTemplate(JOB, "steps: forge build, forge test, adversarial review. spec ", " brief <", ">");
        req.setReviewTemplate(ORACLE, "Did the adversarial review of job ", " pass?", 5, 4);
        vm.stopPrank();
        for (uint256 i; i < 2; ++i) {
            address u = i == 0 ? creator : other;
            imd.mint(u, 10 ether);
            vm.prank(u);
            imd.approve(address(req), type(uint256).max);
        }
    }

    function _deliveredReview(address who) internal returns (bytes32 jobId, bytes32 askId) {
        vm.prank(who);
        jobId = req.openJob(keccak256("spec"), "my hook", PRICE);
        assertTrue(intake.complete(jobId, abi.encode(jobId, bytes("ipfs://result"))));
        vm.prank(who);
        askId = req.requestReview(jobId, PRICE);
    }

    function _att(bytes32 uuid, bytes32 q, bool passed) internal view returns (OracleAttestation.Attestation memory a) {
        a = OracleAttestation.Attestation({
            requestId: uuid,
            chainId: 31337,
            questionHash: q,
            answerType: 0,
            answer: abi.encode(passed),
            figure: 0,
            fromBlock: 1,
            toBlock: 2,
            blockHash: bytes32(uint256(3)),
            panelJobId: keccak256("panel"),
            panelSize: 7,
            quorum: 5,
            agreed: 6,
            issuedAt: uint64(block.timestamp),
            expiresAt: uint64(block.timestamp + 1 hours)
        });
    }

    function _deliver(bytes32 askId, OracleAttestation.Attestation memory a) internal {
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(key, req.attestationDigest(a));
        assertTrue(intake.complete(askId, abi.encode(askId, a, abi.encodePacked(r, s, v))));
    }

    /// A genuine, exactly-authenticated NotPassed receipt must not be discardable by borrowing a
    /// temporary reservation on an unrelated ask and then resetting it.
    function testGenuineNegativeReceiptCannotBeDiscardedViaTemporaryConflict() public {
        (bytes32 jobA, bytes32 askA) = _deliveredReview(creator);
        bytes32 uuid = bytes32(bytes16(keccak256("uuid A")));
        bytes32 qA = keccak256(intake.bodyOf(askA));
        // The real answer for ask A arrives first (normal order) and is retained: NotPassed.
        _deliver(askA, _att(uuid, qA, false));
        assertEq(uint8(req.getJob(jobA).review), uint8(HookJobRequester.ReviewStatus.Pending));

        // Ask A's correct binding would finalize NotPassed. Instead, the owner borrows ask B.
        (, bytes32 askB) = _deliveredReview(other);
        bytes32 bodyB = keccak256(intake.bodyOf(askB));
        vm.startPrank(owner);
        req.bindReview(askB, bodyB, uuid, qA, 31337, 1, 2);
        // Expected: a matching, genuine receipt cannot be discarded (ReviewReceiptMatches guard).
        // Actual: the temporary reservation on B counts as a "conflict" and the discard succeeds.
        bytes32 bodyA = keccak256(intake.bodyOf(askA));
        try req.discardReviewReceipt(askA, bodyA, uuid, qA, 31337, 1, 2) {
            req.resetReviewBinding(askB, bodyB); // conflict evidence vanishes
            vm.stopPrank();
            // The requester now buys a fresh ask for the same job: verdict shopping.
            vm.prank(creator);
            req.requestReview(jobA, PRICE);
            assertEq(uint8(req.getJob(jobA).review), uint8(HookJobRequester.ReviewStatus.Pending));
            assertEq(req.intakeReviewOfOracle(uuid), bytes32(0));
            assertFalse(req.consumed(uuid));
            revert("genuine NotPassed discarded through a resettable, borrowed reservation");
        } catch {
            vm.stopPrank();
        }
    }
}
```

### 2. Low: Retained receipt carrying the ask's true UUID but a different signed questionHash/chain/window has no honest closure path; the ask stays Pending with the fee locked

`src/imd/HookJobRequester.sol:554`

```
            if (!_receiptMatches(receipt, oracleRequestId, questionHash, questionChainId, fromBlock, toBlock)) {
```

Merged from audit_math 458b7df1, audit_economics ef557e0e and audit_flow 85ebd968. The new mismatch-retention path keeps a verified attestation whose requestId equals the authenticated UUID X but whose questionHash (or chainId/window) differs from the value the owner computes independently, which the docs admit is possible because the canonical question algorithm is not known locally. Once retained, no function closes the ask honestly: bindReview with the owner's values reverts ReviewAttestationMismatch; discardReviewReceipt with the owner's values reverts ReviewAttestationMismatch (same-UUID branch requires every field to match) and with the receipt's own values reverts ReviewReceiptMatches (no conflict); confirmReviewExpiry and expireReview revert ReviewAlreadyReceived; closeRevokedReviewReceipt reverts SignerEpochNotRevoked; requestReview reverts NotReviewable. The remaining exits are to finalize under the oracle's fields (which the docs forbid without independent authentication), to rotate the signer and revoke the whole epoch (freezing every other genuine receipt of that epoch), or the dishonest misdelivery/borrowed-conflict discards from the previous finding. The requester's review fee is spent and the job can never show a verdict. The same dead end occurs for a pre-bound ask after resetReviewBinding. Fix: let discardReviewReceipt close a same-UUID receipt whose signed question/chain/window differs from the owner-authenticated context as 'wrong-question receipt', leaving X unconsumed and unreserved and recording the owner-supplied context in the event, as the misdelivery branch already does.

**Reproduction**

HookJobRequesterFixture. Unbound pending ask A for job J; Intake delivers a valid signed attestation with requestId X = fixture UUID, questionHash = keccak256('oracle canonicalized differently'), chainId 31337, fromBlock 1, toBlock 2, answer true -> retained, getJob(J).review == Pending. Owner (ownerQ = fixture canonical hash): bindReview(A, bodyHash, X, ownerQ, 31337, 1, 2) -> ReviewAttestationMismatch(A); discardReviewReceipt(A, bodyHash, X, ownerQ, 31337, 1, 2) -> ReviewAttestationMismatch(A); discardReviewReceipt(A, bodyHash, X, receiptQ, 31337, 1, 2) -> ReviewReceiptMatches(A); closeRevokedReviewReceipt(A) -> SignerEpochNotRevoked(1); after warp past deadline confirmReviewExpiry(A) -> ReviewAlreadyReceived(A). Creator: expireReview(J) -> ReviewAlreadyReceived(A); requestReview(J, 0.5e18) -> NotReviewable(J). Expected: an owner path that closes the ask Unanswered with history retained. Actual: review stays Pending indefinitely. Pre-bound variant: owner binds (X, Q); attestation (X, Q') is retained; after resetReviewBinding the same reverts occur. test/scratch/JudgeProbe.t.sol testSameUuidFieldMismatchDeadEndUnbound and testSameUuidFieldMismatchDeadEndPrebound pass on this code, demonstrating each revert.

### 3. Low: Quorum clause rejects an answer stronger than the configured agreement when the protocol's settlement quorum is below minAgreed, burning the one-shot callback and the fee

`src/imd/HookJobRequester.sol:645`

```
            a.panelSize < ask.minPanelSize || a.quorum < ask.minAgreed || a.agreed < ask.minAgreed
```

From audit_flow 8d8d9214, reproduced. onReviewResult requires a.quorum >= ask.minAgreed in addition to a.agreed >= ask.minAgreed and a.agreed >= a.quorum. The quorum is the protocol's settlement threshold for the action, which this contract cannot read and which no pilot has confirmed. If the protocol settles oracle.request panels at a quorum below the owner's minAgreed, every signed answer, including a unanimous one that satisfies both configured minimums, reverts PanelTooWeak inside the Intake's single try: the fee is spent, no receipt is stored, the ask stays Pending until owner-confirmed expiry, and a paid retry fails identically until the owner lowers minAgreed. IMD_INTEGRATION.md documents minAgreed <= quorum <= agreed <= panelSize as intended, so this is a design choice with an operational failure mode rather than a logic error: agreed >= minAgreed and agreed >= quorum already bound the panel's strength. Fix options preserving the design: drop the a.quorum < ask.minAgreed clause, or add to the pilot checklist that the action's quorum must be confirmed to be at least minAgreed before setReviewTemplate, and document that a lower protocol quorum burns fees.

**Reproduction**

HookJobRequesterFixture (setReviewTemplate minPanelSize 5, minAgreed 4). Delivered job with a bound pending ask A. Intake delivers an attestation signed by the configured signer with panelSize 5, quorum 3, agreed 5, answer false, fresh issuedAt/expiresAt. Expected: a 5-of-5 unanimous answer meeting panelSize >= 5 and agreed >= 4 is accepted. Actual: intake.complete returns false (callback reverted PanelTooWeak(5,3,5)), getReviewReceipt(A).oracleRequestId == 0, review stays Pending, a second complete reverts 'not pending'; a direct call as the intake reverts PanelTooWeak(5,3,5). test/scratch/JudgeProbe.t.sol testUnanimousAnswerBelowConfiguredQuorumBurnsOneShot.

### 4. Low: A synchronous Intake callback issued inside request/requestWithFailure is rejected as UnknownOrSettled and burned, because the job/ask is recorded only after the Intake call returns

`src/imd/HookJobRequester.sol:899`

```
            requestId = intake.requestWithFailure(action, body, callback, onFailure, asset, price);
```

From audit_permissions e0dac640 (also noted inside audit_math 495eb395), reproduced. openJob and requestReview call the Intake first and only then run _recordIntakeId and write jobs[requestId] / reviewOf[intakeRequestId]. If the live Intake ever delivers a result or failure synchronously inside requestWithFailure (an immediate refusal, status 1, for a mis-shaped body or paused action is the natural case), onJobFailure/onJobResult/onReviewFailure see job.status == None / reviewOf == 0 and revert UnknownOrSettled. The Intake's try swallows the revert and its one-shot is spent: the fee is pulled, the job stays Open (or the ask Pending) with no failure record, and the requester can only expireJob after jobTimeout (7 days), or needs owner confirmReviewExpiry for an ask. MockIntake only calls back in a later transaction, so no existing test exercises this, and the docs' live-Intake assumption list does not mention it. This is an unverified live-Intake assumption; funds are not at risk beyond the spent fee. Fix: either record the job/ask before the external call (write provisional state keyed by a precomputed nonce and move it to the returned id), or make the pilot confirm that the Intake never calls back synchronously and document it.

**Reproduction**

Deploy HookJobRequester (fixture) and setIntake to an Intake whose requestWithFailure pulls amount, assigns requestId R and immediately calls onFailure(R, 1, 'refused', 0, 0, '') on the callback target inside a try (test/scratch/JudgeProbe.t.sol SyncRefusingIntake). Creator calls openJob(SPEC_HASH, 'brief', 0.5e18). Expected: job R recorded Failed with reason 'refused', or the transaction reverts and the fee stays with the creator. Actual: the inner call fails with selector UnknownOrSettled(R), openJob succeeds, getJob(R).status == Open, creator balance drops by 0.5 IMD, expireJob(R) reverts DeadlineNotReached until 7 days pass (testSynchronousRefusalIsBurned).

### 5. Low: setJobTemplate validates step markers on the concatenated template, so a marker split across segments passes but never appears in any job body

`src/imd/HookJobRequester.sol:827`

```
        bytes memory all = bytes.concat(prefix, middle, suffix);
```

From audit_permissions 9aeeda52, reproduced. The documented guarantee is that every job.open body names the three steps. The guard checks prefix ++ middle ++ suffix, but every real body is prefix ++ '0x<specHash>' ++ middle ++ brief ++ suffix (openJob line 307), so a marker straddling the prefix/middle or middle/suffix boundary passes the check while the 66-byte hex and the brief are always inserted exactly there. Only the owner can set templates, so this is a misconfiguration the guard was meant to catch rather than a permission bypass. Fix: check each marker inside each individual segment, or validate a sample body built with a placeholder hash and a one-byte brief.

**Reproduction**

HookJobRequesterFixture. Owner calls setJobTemplate(JOB_ACTION, '{"steps":"forge bu', 'ild forge te', 'st adversarial review"}'). Expected: revert TemplateMissingStep('forge build'). Actual: accepted. Creator openJob(SPEC_HASH, 'brief', 0.5e18) succeeds and the stored body (intake.bodyOf(lastRequestId)) contains neither 'forge build' nor 'forge test' (test/scratch/JudgeProbe.t.sol testStepMarkerStraddlingSegmentsPasses).

### 6. Info: Owner trust: revokeSignerEpoch freezes every retained receipt of the epoch, genuine ones included, and the current epoch cannot be revoked without a rotation first

`src/imd/HookJobRequester.sol:505`

```
        revokedSignerEpochs[epoch] = incidentHash;
```

From audit_math 9f415c1d (also listed in audit_permissions 5c1d4f94), reproduced. Revocation is per epoch, not per receipt or time range. One revocation makes every receipt verified in that epoch unbindable (bindReview reverts SignerEpochRevoked) and lets the owner close each as Unanswered via closeRevokedReviewReceipt, which also permits paid retries on genuine NotPassed answers. Because epoch >= oracleSignerEpoch is rejected, the owner must rotate first; rotating to the same compromised registry makes the new epoch equally compromised and unrevocable until another rotation. Finalized verdicts and consumed UUIDs are untouched. This matches the documented incident workflow and is recorded so the coarse blast radius is an explicit trust assumption; no code change is required.

**Reproduction**

HookJobRequesterFixture. Two unbound asks A and B receive valid retained answers in epoch 1 (A passed=false, B passed=true). Owner: revokeSignerEpoch(1, keccak256('incident')) -> InvalidSignerEpoch(1) while epoch 1 is current; setOracleSigner(safe) (epoch 2); revokeSignerEpoch(1, keccak256('incident')) succeeds. bindReview(A, ...) and bindReview(B, ...) both revert SignerEpochRevoked(1). closeRevokedReviewReceipt(A) -> getJob(jobA).review == Unanswered; creator requestReview(jobA, 0.5e18) succeeds (test/scratch/JudgeProbe.t.sol testRevocationCoarse).

### 7. Info: Unverified live-Intake assumptions: callbacks must originate from the Intake address itself and must use the onJobResult(bytes32,bytes), onReviewResult(bytes32,Attestation,bytes) and failure(bytes32,u

`src/imd/HookJobRequester.sol:287`

```
        if (msg.sender != address(intake)) revert NotTheIntake();
```

Merged from audit_flow 93e07d09, audit_math fa1c634a and audit_flow f9e1ee59. All four callbacks are gated on msg.sender == intake, and the job.open completion ABI is an assumption not covered by any protocol vector in the repository (only the oracle.request EIP-712 digest is). If the production Intake v2 dispatches results through a separate executor or settlement contract, or encodes the completion differently, every callback reverts (NotTheIntake, selector mismatch or UnknownOrSettled) inside the dispatcher's single try: fees are spent, jobs stay Open until the 7-day local expiry, asks need owner-confirmed expiry, and the site never shows Delivered. There is no setter for the callback selectors or a separate callback-sender address, so a mismatch is a full outage until redeploy. Funds beyond spent fees are not at risk. These are material launch blockers that cannot be verified locally (MockIntake calls back from its own address with these exact shapes by construction). Pilot items: confirm the exact callback sender and ABI on the target chain with one paid request before any wallet approves funds; if the sender differs, add an owner-set, logged callback-sender address distinct from the request target; the constructor addresses listed in IMD_INTEGRATION.md were not checked with cast code.

**Reproduction**

Local evidence only. Sender: test/HookJobRequester.t.sol testResultAcceptedOnceFromIntakeOnly shows a non-intake sender reverting NotTheIntake with the job left Open. ABI: MockIntake.complete(id, hex'deadbeef') returns false and the job stays Open until expireJob after the deadline (testCallbackWithUnexpectedAbiFailsSafeAndJobCanExpire). Expected on a live chain: a result callback from executor E != I, or with another ABI, marks the job Delivered. Actual: revert; one-shot consumed; fee not refunded. The live sender and ABI are not known from this repository.

### 8. Info: Unverified live-Intake assumption: the Intake must debit exactly priceOf(action, asset) in the same call, or both paid entry points revert InexactIntakeSpend permanently with no owner tolerance knob

`src/imd/HookJobRequester.sol:904`

```
        if (ExactStoreToken.balance(asset, address(this)) != beforeBalance - price) revert InexactIntakeSpend();
```

Merged from audit_math 495eb395, audit_flow 9f2152e0 and audit_permissions 5c196727. The partial-Intake-spending fix is correct and atomic: a quote/spend discrepancy rolls back the pull, approval, Intake request and all local state, nothing becomes sweepable, and donations stay separate (RequesterMvpPaymentTest fuzz and donation tests, re-run green). The cost is liveness: if the live Intake rounds, splits a protocol fee, refunds dust, bills later, or reads priceOf at a different moment, openJob and requestReview revert for every caller and the deployment cannot take a single order until the owner points at another Intake or redeploys. The behaviour is the documented fail-closed design, so no code change is proposed; it is a pilot blocker: confirm with one real paid request on both requestWithFailure and request paths that the debit equals priceOf to the wei.

**Reproduction**

HookJobRequesterFixture with intake.setUnspent(1) (Intake debits price-1). Creator openJob(SPEC_HASH, 'brief', 0.5e18) and requestReview(jobId, 0.5e18) both revert InexactIntakeSpend; creator balance, allowance, jobCount and intake.lastRequestId unchanged; requester contract balance 0 (test/scratch/JudgeProbe.t.sol testPartialSpendRollsBack; RequesterMvpPaymentTest testFuzzUnderspendingIntakeRollsBackAllStateAndLeavesNothingSweepable). Price-change cases also re-verified: a quote above userMaxPrice reverts PriceAboveUserMaximum without debit, a lower quote pulls only that quote and leaves zero allowance (testPriceChangeCases).

### 9. Info: Unverified live-Intake assumption: if the Intake derives or recycles request ids for a byte-identical retry body, every review retry reverts DuplicateRequestId

`src/imd/HookJobRequester.sol:878`

```
        if (requestId == bytes32(0) || usedIntakeRequestIds[requestId]) revert DuplicateRequestId(requestId);
```

From audit_math cd29a94a, reproduced. A retry ask for the same job sends a byte-identical body (prefix ++ hex(jobId) ++ suffix) to the same action. If the live Intake derives request ids deterministically from (caller, action, body) or recycles ids after settlement, _recordIntakeId reverts after the Intake call, rolling back payment and the request. The Unanswered -> requestReview retry path that the owner recovery powers rely on would then be unusable. The fee is not lost, and no owner setting can tolerate id reuse. Pilot item: confirm the live id derivation before relying on retries.

**Reproduction**

HookJobRequesterFixture. Unbound ask A closed Unanswered by intake.fail(A, 2, 'no_agreement', 0, 0). intake.setReuseIds(true). Creator requestReview(jobId, 0.5e18) -> reverts DuplicateRequestId(A); creator balance unchanged (test/scratch/JudgeProbe.t.sol testReusedIntakeIdBlocksRetry).

### 10. Info: Re-measured one-shot callback gas: worst tested path 192,598 of 200,000 (mismatched pre-binding, 22-cold-read registry); production signer not modelled, 7.4k headroom

`src/imd/HookJobRequester.sol:658`

```
            _reviewReceipts[requestId] = StoredReviewReceipt({
```

Merged from audit_math 4bffb8c5, audit_permissions 54261bc6 and audit_flow f9e1ee59. Re-running test/ReviewReceiptGas.t.sol at this commit (solc 0.8.26, Cancun, optimizer 200, cold consumer and signer per trial) reproduces AUDIT_6B607200.md exactly: cold EOA receipt 125,296; 5-of-7 ERC-1271 receipt 170,389 (identical after an expiry request and with a reserved retry UUID); 5-of-7 bound 132,865; 22-read registry receipt 187,543 and bound 150,038; mismatched pre-binding 175,435 (5-of-7) and 192,598 (22-read). The mismatch path is the heaviest because all five binding slots are read cold before the retain branch writes four zero-to-nonzero words plus the packed details word. The claim holds locally but rests on pilot-only assumptions: the stipend is exactly 200,000 and forwarded in full after EIP-150; the production signer (a Safe-style wallet with proxy, singleton, fallback handler and owner lookups is not represented by the toy 5-of-7) verifies in under about 67k cold with signatures no larger than 325 bytes; and the retained-receipt path, not only the bound path, is what the live oracle hits first. A live signer costing more than roughly 7k above the 22-read fixture on this path loses the one-shot answer with no receipt, no verdict and no refund. Not a code defect; a signer qualification item before deployment.

**Reproduction**

forge test --match-path test/ReviewReceiptGas.t.sol -vv prints the numbers above (8 tests pass). Failing input for the budget: oracleSigner = ColdReadReceiptSigner(signer, 64) on the mismatched pre-binding ask -> intake.complete returns false, getReviewReceipt(ask).oracleRequestId == 0, review stays Pending, fee spent (testOverBudgetSignerStillFailsClosedAndLosesSingleAttemptWithoutPartialReceipt).

---

Judge's submission `5e9a10271670a9083a9f70d55ccf02ff4a6eea62886152219e17be581795cf43`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
