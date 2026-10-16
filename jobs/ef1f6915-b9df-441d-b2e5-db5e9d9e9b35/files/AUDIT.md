# Audit report

> Audit commit cb6ca724441c9aebf9a38cb4d7426218e0712723 against report 1053af02-a430-49b3-a914-75620c17c801. Reproduce the prior verdict-shopping, swapped-receipt, UUID-reservation and 200k-gas findings against the new code. Adversarially check discardReviewReceipt and releaseReservation for fabricated mismatches, unauthorized use, cross-request verdicts and replay; verify receipt-first gas with a realistic ERC-1271 signer and one-attempt callback. Check listing/ad escrow regressions. State unresolved findings and live-Intake assumptions. Do not deploy.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1811-build-technical-foundation-hooks.git |
| Commit | `cb6ca724441c9aebf9a38cb4d7426218e0712723` |
| Job | `ef1f6915-b9df-441d-b2e5-db5e9d9e9b35` |
| Judged | 2026-10-16 06:01 UTC |
| Findings | 1 medium · 3 low · 1 info |

Four agents audited the code as it is at `cb6ca72`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Residual verdict shopping: requester front-runs a late NotPassed delivery with expireReview and re-asks

`src/imd/HookJobRequester.sol:609`

```
        if (_reviewReceipts[intakeRequestId].oracleRequestId != bytes32(0)) {
```

Merged from audit_economics/audit_math/audit_flow/audit_permissions. The 1053af02 fix only blocks expiry once a receipt is stored. After reviewDeadline, a requester who sees the Intake's pending callback carrying answer=false (calldata) calls expireReview first: reviewOf is deleted, the one-shot onReviewResult reverts UnknownOrSettled, no receipt is kept, job becomes Unanswered and requestReview is allowed again. The requester keeps Passed answers and discards NotPassed ones for one fee per attempt. Fix: keep accepting a late, validly signed callback for an expired-but-not-re-asked Intake ID as a receipt (job back to Pending), or make expiry two-step/owner-assisted, or add a grace period longer than attestation validity.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {HookJobRequester} from "src/imd/HookJobRequester.sol";
import {IIntake} from "src/imd/IIntake.sol";
import {OracleAttestation} from "src/imd/OracleAttestation.sol";

contract PocToken {
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
        if (allowance[from][msg.sender] != type(uint256).max) allowance[from][msg.sender] -= amount;
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        return true;
    }
}

/// @dev One-shot Intake stand-in: 200k gas callback, settled even when the callback reverts.
contract PocIntake is IIntake {
    struct Req {
        address target;
        bytes4 selector;
        bool settled;
        bytes body;
    }

    mapping(bytes32 => Req) public reqs;
    uint256 internal nonce;
    uint256 public price = 0.5 ether;

    function priceOf(bytes32, address) external view returns (uint256) {
        return price;
    }

    function request(bytes32, bytes calldata body, Callback calldata cb, address asset, uint256 amount)
        external
        payable
        returns (bytes32 id)
    {
        return _req(body, cb, asset, amount);
    }

    function requestWithFailure(bytes32, bytes calldata body, Callback calldata cb, bytes4, address asset, uint256 amount)
        external
        payable
        returns (bytes32 id)
    {
        return _req(body, cb, asset, amount);
    }

    function _req(bytes calldata body, Callback calldata cb, address asset, uint256 amount) internal returns (bytes32 id) {
        PocToken(asset).transferFrom(msg.sender, address(this), amount);
        id = keccak256(abi.encode(address(this), ++nonce));
        reqs[id] = Req(cb.target, cb.selector, false, body);
    }

    function bodyOf(bytes32 id) external view returns (bytes memory) {
        return reqs[id].body;
    }

    function complete(bytes32 id, bytes calldata args) external returns (bool called) {
        Req storage r = reqs[id];
        require(r.target != address(0) && !r.settled, "not pending");
        r.settled = true;
        (called,) = r.target.call{gas: 200_000}(bytes.concat(r.selector, args));
    }
}

/// @notice Audit finding: a requester who sees a late NotPassed answer coming (Intake completion in
/// the mempool, or the public panel result) front-runs it with `expireReview`, so the one-shot
/// callback reverts, the negative verdict is never recorded, and the requester re-asks.
contract ExpiryFrontRunShoppingTest is Test {
    PocToken internal imd;
    PocIntake internal intake;
    HookJobRequester internal requester;
    address internal owner = makeAddr("owner");
    address internal creator = makeAddr("creator");
    uint256 internal signerKey = uint256(keccak256("poc oracle key"));

    function setUp() public {
        vm.warp(1_800_000_000);
        imd = new PocToken();
        intake = new PocIntake();
        requester = new HookJobRequester(owner, address(intake), address(imd), vm.addr(signerKey), 0.5 ether);
        vm.startPrank(owner);
        requester.setJobTemplate("job", '{"steps":"forge build, forge test, adversarial review","spec":"', '","b":"', '"}');
        requester.setReviewTemplate("review", '{"q":"did job ', ' pass?"}', 5, 4);
        vm.stopPrank();
        imd.mint(creator, 10 ether);
        vm.prank(creator);
        imd.approve(address(requester), type(uint256).max);
    }

    function _attestation(bytes32 askId, bool passed) internal view returns (OracleAttestation.Attestation memory) {
        return OracleAttestation.Attestation({
            requestId: bytes32(bytes16(keccak256(abi.encode("uuid", askId)))),
            chainId: 31337,
            questionHash: keccak256(intake.bodyOf(askId)),
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

    function _signed(bytes32 askId, OracleAttestation.Attestation memory a) internal view returns (bytes memory) {
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(signerKey, requester.attestationDigest(a));
        return abi.encode(askId, a, abi.encodePacked(r, s, v));
    }

    function testRequesterFrontRunsLateNotPassedWithExpiryAndReasks() public {
        vm.prank(creator);
        bytes32 jobId = requester.openJob(keccak256("spec"), "hook brief");
        assertTrue(intake.complete(jobId, abi.encode(jobId, bytes("ipfs://result"))));
        vm.prank(creator);
        bytes32 askId = requester.requestReview(jobId);

        // The oracle's answer is produced after the 1-day local deadline. It is a valid, fresh,
        // correctly signed NotPassed for this exact ask; the Intake's completion tx is pending.
        vm.warp(block.timestamp + 1 days + 1);
        bytes memory pendingDelivery = _signed(askId, _attestation(askId, false));

        // Requester sees `answer = false` in the pending calldata and front-runs with expiry.
        vm.prank(creator);
        (bool expired,) = address(requester).call(abi.encodeCall(HookJobRequester.expireReview, (jobId)));
        expired; // ignored: a fix may refuse this

        // The Intake's one attempt: the genuine negative answer must be retained or recorded.
        bool delivered = intake.complete(askId, pendingDelivery);
        assertTrue(delivered, "genuine NotPassed was discarded by requester-chosen expiry");
        HookJobRequester.ReviewStatus status = requester.getJob(jobId).review;
        assertTrue(status != HookJobRequester.ReviewStatus.Unanswered, "requester may re-ask after seeing NotPassed");
    }
}
```

### 2. Low: Receipt whose UUID was consumed/reserved through another ask can never be finalized or closed; job stuck Pending

`src/imd/HookJobRequester.sol:450`

```
        if (_receiptMatches(receipt, oracleRequestId, questionHash, questionChainId, fromBlock, toBlock)) {
```

Merged (audit_math, audit_flow, audit_economics wedge note). If an unbound ask's true-context receipt has UUID X and X is consumed (or reserved) by another ask, bindReview reverts DuplicateRequestId (line 390), discardReviewReceipt reverts ReviewReceiptMatches, releaseReservation reverts, expireReview reverts ReviewAlreadyReceived and requestReview reverts NotReviewable. The honest owner has no path; only a fabricated mismatch closes it. Fix: allow discard when consumed[receipt.oracleRequestId] or the UUID is reserved by a different ask.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {HookJobRequester} from "src/imd/HookJobRequester.sol";
import {IIntake} from "src/imd/IIntake.sol";
import {OracleAttestation} from "src/imd/OracleAttestation.sol";

/// @dev Minimal ERC-20 for the proof: returns true, no callbacks.
contract ProofToken {
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
        if (allowance[from][msg.sender] != type(uint256).max) allowance[from][msg.sender] -= amount;
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        return true;
    }
}

/// @dev Minimal Intake v2 stand-in: pulls the price, calls back once under the 200k stipend.
contract ProofIntake is IIntake {
    struct Req {
        address target;
        bytes4 selector;
        bool settled;
    }

    uint256 public price;
    uint256 internal nonce;
    mapping(bytes32 => Req) public reqs;

    constructor(uint256 price_) {
        price = price_;
    }

    function priceOf(bytes32, address) external view returns (uint256) {
        return price;
    }

    function request(bytes32, bytes calldata, Callback calldata callback, address asset, uint256 amount)
        external
        payable
        returns (bytes32 id)
    {
        return _request(callback, asset, amount);
    }

    function requestWithFailure(bytes32, bytes calldata, Callback calldata callback, bytes4, address asset, uint256 amount)
        external
        payable
        returns (bytes32 id)
    {
        return _request(callback, asset, amount);
    }

    function _request(Callback calldata callback, address asset, uint256 amount) internal returns (bytes32 id) {
        require(amount == price, "wrong amount");
        require(ProofToken(asset).transferFrom(msg.sender, address(this), amount), "pull failed");
        id = keccak256(abi.encode(address(this), ++nonce));
        reqs[id] = Req(callback.target, callback.selector, false);
    }

    function complete(bytes32 id, bytes calldata args) external returns (bool called) {
        Req storage r = reqs[id];
        require(r.target != address(0) && !r.settled, "not pending");
        r.settled = true;
        (called,) = r.target.call{gas: 200_000}(bytes.concat(r.selector, args));
    }
}

/// @notice Fails on the current code: an unbound receipt whose true context matches but whose UUID
/// was consumed through another ask has no recovery path. Passes once the owner can close it.
contract StuckReceiptProofTest is Test {
    bytes32 internal constant JOB_ACTION = "job.open@test";
    bytes32 internal constant ORACLE_ACTION = "oracle.request@oracle-1";
    uint256 internal constant PRICE = 0.5 ether;

    ProofToken internal imd;
    ProofIntake internal intake;
    HookJobRequester internal requester;
    address internal owner = makeAddr("owner");
    address internal creator = makeAddr("creator");
    uint256 internal signerKey = uint256(keccak256("proof oracle key"));

    function setUp() public {
        vm.chainId(31337);
        vm.warp(1_800_000_000);
        imd = new ProofToken();
        intake = new ProofIntake(PRICE);
        requester = new HookJobRequester(owner, address(intake), address(imd), vm.addr(signerKey), PRICE);
        vm.startPrank(owner);
        requester.setJobTemplate(
            JOB_ACTION,
            '{"steps":["forge build","forge test","adversarial review"],"specHash":"',
            '","request":"<brief>',
            '</brief>"}'
        );
        requester.setReviewTemplate(ORACLE_ACTION, '{"question":"', '"}', 5, 4);
        vm.stopPrank();
        imd.mint(creator, 10 ether);
        vm.prank(creator);
        imd.approve(address(requester), type(uint256).max);
    }

    function _unboundAsk() internal returns (bytes32 jobId, bytes32 askId) {
        vm.prank(creator);
        jobId = requester.openJob(keccak256("spec"), "A swap cap hook");
        assertTrue(intake.complete(jobId, abi.encode(jobId, bytes("ipfs://result"))));
        vm.prank(creator);
        askId = requester.requestReview(jobId);
    }

    function _attestation(bytes32 askId, bytes32 uuid, bool passed)
        internal
        view
        returns (OracleAttestation.Attestation memory a)
    {
        a = OracleAttestation.Attestation({
            requestId: uuid,
            chainId: 31337,
            questionHash: keccak256(abi.encode("question", askId)),
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

    function _deliver(bytes32 askId, OracleAttestation.Attestation memory a) internal returns (bool) {
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(signerKey, requester.attestationDigest(a));
        return intake.complete(askId, abi.encode(askId, a, abi.encodePacked(r, s, v)));
    }

    function testOwnerCanCloseReceiptWhoseUuidWasConsumedElsewhere() public {
        (, bytes32 askA) = _unboundAsk();
        (bytes32 jobB, bytes32 askB) = _unboundAsk();
        bytes32 uuid = bytes32(bytes16(keccak256("shared protocol UUID")));
        OracleAttestation.Attestation memory a = _attestation(askA, uuid, true);
        OracleAttestation.Attestation memory b = _attestation(askB, uuid, false);
        assertTrue(_deliver(askA, a), "receipt A retained");
        assertTrue(_deliver(askB, b), "receipt B retained");

        // Owner authenticates A's context and finalizes it, consuming the shared UUID.
        bytes32 bodyA = requester.getReviewAsk(askA).bodyHash;
        vm.prank(owner);
        requester.bindReview(askA, bodyA, uuid, a.questionHash, a.chainId, a.fromBlock, a.toBlock);
        assertTrue(requester.consumed(uuid));

        // B's receipt matches B's true context but its UUID is gone: bind is impossible by design.
        bytes32 bodyB = requester.getReviewAsk(askB).bodyHash;
        vm.prank(owner);
        vm.expectRevert(abi.encodeWithSelector(HookJobRequester.DuplicateRequestId.selector, uuid));
        requester.bindReview(askB, bodyB, uuid, b.questionHash, b.chainId, b.fromBlock, b.toBlock);

        // The requester has no path either.
        vm.warp(requester.getReviewAsk(askB).deadline + 1);
        vm.prank(creator);
        vm.expectRevert(abi.encodeWithSelector(HookJobRequester.ReviewAlreadyReceived.selector, askB));
        requester.expireReview(jobB);

        // Expected: the owner can close the dead receipt so the requester may retry.
        // Actual on current code: ReviewReceiptMatches, and jobB is Pending forever.
        vm.prank(owner);
        requester.discardReviewReceipt(askB, bodyB, uuid, b.questionHash, b.chainId, b.fromBlock, b.toBlock);
        assertEq(uint8(requester.getJob(jobB).review), uint8(HookJobRequester.ReviewStatus.Unanswered));
        vm.prank(creator);
        requester.requestReview(jobB);
    }
}
```

### 3. Low: Stale reservation of a terminal ask rejects the retry's one-shot callback before the owner can release it

`src/imd/HookJobRequester.sol:548`

```
        if (reservedFor != bytes32(0) && reservedFor != requestId) revert DuplicateRequestId(a.requestId);
```

Merged (economics, math, permissions). After a bound ask expires/fails, its UUID stays reserved until owner releaseReservation. The requester can re-ask immediately; if the protocol reuses the UUID, the retry's unbound receipt-first callback reverts here although releaseReservation's predicate already holds (holder terminal, no receipt, unconsumed). The single attempt and fee are lost. Fix: on the unbound path skip the reservation check, or treat a reservation as non-blocking when reviewOf[holder]==0, no receipt and unconsumed.

### 4. Low: discardReviewReceipt accepts a 'true context' with the receipt's own UUID or a consumed UUID, so an owner typo irreversibly erases a genuine verdict

`src/imd/HookJobRequester.sol:450`

```
        if (_receiptMatches(receipt, oracleRequestId, questionHash, questionChainId, fromBlock, toBlock)) {
```

Merged with the owner-trust notes from all specialists. Discard only requires a well-formed context that differs in any field. It does not refuse oracleRequestId == receipt UUID (a same-request field mismatch is not a misdelivery) nor UUIDs consumed/reserved elsewhere (which bindReview at line 390 refuses). A toBlock+1 typo (or deliberate owner choice) closes a genuine NotPassed and lets the requester re-ask. Deliberate abuse is a documented owner-trust assumption; the missing consistency checks are the defect. Fix: revert when oracleRequestId == receipt.oracleRequestId, or when it is consumed/reserved by another ask (keep the stuck-receipt exception above).

### 5. Info: Verification notes: gas, authorization, escrow, live-Intake assumptions

`src/imd/HookJobRequester.sol:548`

```
        if (reservedFor != bytes32(0) && reservedFor != requestId) revert DuplicateRequestId(a.requestId);
```

Not re-measured by this judge (time): specialists report receipt-first gas ~170.6k with a Safe-shaped 5-of-7 ERC-1271 signer under the 200k one-attempt call, ~29k headroom; signers over ~74k cold still lose the answer and fee. discard/release are onlyOwner; after discard reviewOf is deleted so replay reverts. No src/store changes since the audited commit per specialists. Unverified live assumptions: Intake callback ABI and single 200k delivery, authenticated UUID/context source for owner binding, UUID uniqueness, issuedAt/expiry windows, honest and available owner.

---

Judge's submission `a61567f73e825cb7860f0c1e4ded20775157bf9a9b0586a95324861b2aebc454`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
