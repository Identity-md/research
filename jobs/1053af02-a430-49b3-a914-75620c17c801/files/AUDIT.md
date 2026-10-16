# Audit report

> Re-audit commit 64e40684 after the 5f43f94d fixes. Check the receipt-first one-shot callback, exact owner confirmation, cross-request answer misbinding, replay/expiry, 200k-gas callback limit, and listing/ad escrow regressions. Identify any remaining unsafe or unworkable assumptions; do not deploy.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1811-build-technical-foundation-hooks.git |
| Commit | `64e40684e68c84c21e770bca63206ec9d292f063` |
| Job | `1053af02-a430-49b3-a914-75620c17c801` |
| Judged | 2026-10-16 05:03 UTC |
| Findings | 1 medium · 3 low · 2 info |

Four agents audited the code as it is at `64e4068`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Requester can discard a retained, signature-verified NotPassed answer via expireReview and buy a new ask (verdict shopping)

`src/imd/HookJobRequester.sol:496`

```
        if (job.review != ReviewStatus.Pending) revert UnknownOrSettled(jobRequestId);
```

Merged from three specialists (audit_economics, audit_permissions, audit_math). In the receipt-first order the 5f43f94d fix recommends, onReviewResult stores a verified answer as a ReviewReceipt (lines 442-453) and leaves job.review Pending until the owner's bindReview. expireReview (lines 494-504) checks only review == Pending, msg.sender == requester and block.timestamp > reviewDeadline; it never consults _reviewReceipts[job.reviewRequestId]. The receipt's bool is public through getReviewReceipt, and reviewDeadline is askedAt + reviewTimeout (default 1 day, minimum 1 hour) measured from the ask, not from the receipt. So the party being judged can read a negative answer, wait out (or mempool-front-run) the owner's confirmation, erase it to Unanswered and pay 0.5 IMD for a fresh ask. Passed receipts get confirmed; NotPassed receipts get discarded. The docs present abandonment of a retained answer as allowed, but the asymmetry means a NotPassed verdict is only durable when the owner happens to confirm first, which defeats the terminal-NotPassed rule at line 315 and the property tested by testReviewNotPassedIsStoredNotReverted. Reproduced with both supplied proofs (Proof_f3885f4fc792 and Proof_20286c6ea28b fail on this commit for the stated reason). Minimal fix preserving the design: in expireReview revert when _reviewReceipts[job.reviewRequestId].oracleRequestId != 0 (or finalize the receipt instead of discarding it), and let only the owner close a receipt-bearing ask whose independently verified mapping shows the receipt belongs to another ask; alternatively start the abandonment clock at receivedAt. The attached proof passes under either variant.

**Reproduction**

Job Delivered; creator calls requestReview -> askId (owner has not bound). Intake delivers a correctly signed attestation with answer=abi.encode(false), panel 3/2/3 (or 7/5/6), issuedAt=now, expiresAt=now+1h: onReviewResult stores the receipt, getReviewReceipt(askId).passed == false, job.review == Pending. vm.warp(getJob(jobId).reviewDeadline + 1); as creator call expireReview(jobId). Expected: revert (a verified answer is retained) or finalization to NotPassed. Actual: succeeds, review == Unanswered (4), reviewOf[askId] == 0, owner's bindReview(askId, bodyHash, uuid, questionHash, chainId, 1, 2) now reverts UnknownOrSettled(askId), and requestReview(jobId) is accepted again for another 0.5 IMD. Run: forge test --match-path test/scratch/Proof_f3885f4fc792.t.sol -> FAIL 'verdict shopping: NotPassed answer discarded and a new ask opened'; test/scratch/Proof_20286c6ea28b.t.sol -> FAIL 'next call did not revert as expected'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import "forge-std/Test.sol";
import {HookJobRequester} from "src/imd/HookJobRequester.sol";
import {IIntake} from "src/imd/IIntake.sol";
import {OracleAttestation} from "src/imd/OracleAttestation.sol";

contract Tok {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    function mint(address to, uint256 a) external { balanceOf[to] += a; }
    function approve(address s, uint256 a) external returns (bool) { allowance[msg.sender][s] = a; return true; }
    function transferFrom(address f, address t, uint256 a) external returns (bool) {
        allowance[f][msg.sender] -= a; balanceOf[f] -= a; balanceOf[t] += a; return true;
    }
    function transfer(address t, uint256 a) external returns (bool) { balanceOf[msg.sender] -= a; balanceOf[t] += a; return true; }
}

contract Intake {
    uint256 n;
    function priceOf(bytes32, address) external pure returns (uint256) { return 1e18; }
    function _take(address asset, uint256 amount) internal returns (bytes32) {
        Tok(asset).transferFrom(msg.sender, address(this), amount);
        return keccak256(abi.encode(++n));
    }
    function request(bytes32, bytes calldata, IIntake.Callback calldata, address asset, uint256 amount)
        external payable returns (bytes32) { return _take(asset, amount); }
    function requestWithFailure(bytes32, bytes calldata, IIntake.Callback calldata, bytes4, address asset, uint256 amount)
        external payable returns (bytes32) { return _take(asset, amount); }
}

contract VerdictShoppingTest is Test {
    HookJobRequester r;
    Intake intake;
    Tok tok;
    address owner = makeAddr("owner");
    address creator = makeAddr("creator");
    uint256 key = 0xA11CE;
    address signer;

    function setUp() public {
        vm.warp(1_000_000);
        signer = vm.addr(key);
        intake = new Intake();
        tok = new Tok();
        r = new HookJobRequester(owner, address(intake), address(tok), signer, 1e18);
        vm.startPrank(owner);
        r.setJobTemplate("job.open", "forge build forge test adversarial review ", " ", " ");
        r.setReviewTemplate("oracle.request", "{\"job\":\"", "\"}", 3, 2);
        vm.stopPrank();
        tok.mint(creator, 10e18);
        vm.prank(creator);
        tok.approve(address(r), type(uint256).max);
    }

    function _att(bytes32 uuid, bool passed) internal view returns (OracleAttestation.Attestation memory a) {
        a.requestId = uuid;
        a.chainId = 31337;
        a.questionHash = keccak256("q");
        a.answerType = 0;
        a.answer = abi.encode(passed);
        a.fromBlock = 1;
        a.toBlock = 2;
        a.panelJobId = keccak256("panel");
        a.panelSize = 3;
        a.quorum = 2;
        a.agreed = 3;
        a.issuedAt = uint64(block.timestamp);
        a.expiresAt = uint64(block.timestamp + 3600);
    }

    function _sig(OracleAttestation.Attestation memory a) internal view returns (bytes memory) {
        (uint8 v, bytes32 rr, bytes32 s) = vm.sign(key, this.digest(a));
        return abi.encodePacked(rr, s, v);
    }

    function digest(OracleAttestation.Attestation calldata a) external view returns (bytes32) {
        return r.attestationDigest(a);
    }

    /// A retained, signature-verified NotPassed answer must not be erasable by the requester
    /// so they can buy a fresh ask and shop for a Passed verdict.
    function testRequesterCannotDiscardRetainedNotPassedAnswer() public {
        vm.prank(creator);
        bytes32 jobId = r.openJob(bytes32(uint256(1)), "hook");
        vm.prank(address(intake));
        r.onJobResult(jobId, "code");
        vm.prank(creator);
        bytes32 askId = r.requestReview(jobId);

        OracleAttestation.Attestation memory a = _att(keccak256("uuid-1"), false);
        bytes memory sig = _sig(a);
        vm.prank(address(intake));
        r.onReviewResult(askId, a, sig);
        assertFalse(r.getReviewReceipt(askId).passed, "verified NotPassed answer retained");

        // Owner is still authenticating the mapping off-chain; the 1-day deadline passes.
        vm.warp(r.getReviewAsk(askId).deadline + 1);
        vm.prank(creator);
        (bool expired,) = address(r).call(abi.encodeCall(r.expireReview, (jobId)));
        if (expired) {
            // Requester now buys a fresh ask and the job is reviewable again.
            vm.prank(creator);
            (bool reasked,) = address(r).call(abi.encodeCall(r.requestReview, (jobId)));
            assertFalse(reasked, "verdict shopping: NotPassed answer discarded and a new ask opened");
        }
        assertTrue(
            uint8(r.getJob(jobId).review) != uint8(HookJobRequester.ReviewStatus.Unanswered),
            "retained answer erased to Unanswered"
        );
    }
}
```

### 2. Low: Receipt-first callback leaves about 42k gas of the 200k stipend for a production ERC-1271 registry; an over-budget callback loses the one-shot answer and the fee

`src/imd/HookJobRequester.sol:442`

```
            _reviewReceipts[requestId] = ReviewReceipt({
```

Merged from audit_flow, audit_economics and audit_math. The unbound path of onReviewResult writes a five-slot ReviewReceipt (five cold SSTOREs, ~110k) on top of signature verification, decoding and a second full EIP-712 hash for the ReviewReceived event (attestationDigest(a) at line 454 recomputes what _verifyAttestation already hashed). Measured on this commit from a contract acting as the Intake, forwarding an exact gas cap, with vm.cool on the requester, signer and registry (binary search): receipt path 145,701 gas with a bare ECDSA key; 157,472 with a minimal ERC-1271 registry (one ecrecover, two cold SLOADs); +10 extra cold SLOADs in the registry 180,374; +16: 194,120; +18: 198,702 (fits); +22: 207,866 (exceeds 200,000). The bound path for the same cases costs 89,994 / 101,768 / 152,162, so a registry that works on a pre-bound ask fails on the receipt-first path the docs now recommend. The audit_flow figure of 179k/189k did not reproduce under this method; the other two specialists' numbers match mine. When the callback runs out of gas inside the Intake's try, no receipt is stored, the Intake records its single attempt, the ask fee is kept, and the only recovery is expireReview after the deadline plus a new paid ask. The existing tests pass only because OracleRegistryMock is minimal; the docs say live registry gas 'still needs verification' but state no budget. Not a code defect by itself; it is an unverified live assumption with a concrete, measurable failure mode. Suggested: document a registry budget (isValidSignature <= ~40k on a cold account), add a test with a registry burning ~40k, and recover headroom by emitting the digest already computed in _verifyAttestation instead of rehashing, and/or dropping receivedAt (never read on chain) from the packed slot.

**Reproduction**

test/scratch/Judge.t.sol::testHeavyRegistryLosesOneShotReceipt: deploy Registry(signer, 22) whose isValidSignature sums 22 cold mapping slots then ecrecover-compares; owner setOracleSigner(registry). Job delivered, requestReview -> askA (unbound). vm.cool(requester), vm.cool(registry); Intake delivers a valid bool attestation with call{gas: 200000}. Expected (fix's claim): receipt stored, ReviewReceived emitted. Actual: complete() returns false, getReviewReceipt(askA).oracleRequestId == 0, a second complete() reverts 'not pending', fee spent. The same registry on a pre-bound ask (askB) delivers successfully and sets Passed. testGasReceiptPathEcdsa / testGasReceiptPathRegistry print the minimum forwarded gas figures above (145,701 ECDSA receipt; 89,994 ECDSA bound; registry+18 cold reads 198,702; +22 207,866).

### 3. Low: A misdelivered (swapped) receipt permanently blocks the ask's true binding and can be confirmed into the other question's verdict; there is no owner path to discard it

`src/imd/HookJobRequester.sol:370`

```
        ) revert ReviewAttestationMismatch(intakeRequestId);
```

From audit_flow. Once an unbound ask holds any receipt, bindReview accepts only a binding whose five context fields equal the receipt's (lines 362-370), and the receipt is immutable (onReviewResult reverts ReviewAlreadyReceived at line 411; onReviewFailure likewise at 486). The receipt carries no on-chain tie to the ask; the docs say exactly that the Intake-id-to-UUID pairing cannot be assumed and name 'wrong delivery pairing' as a residual that may lose a paid answer. The consequence the docs do not state: after a swap the owner's independently authenticated true mapping is the one binding the contract refuses forever (ReviewAttestationMismatch), while confirming the swapped fields is accepted and records the other job's answer (Passed/NotPassed, panelJobId, panel counts) as this job's verdict. Confirming the swapped fields also reserves and consumes that UUID, so the other job's genuine ask can then never bind its own UUID (DuplicateRequestId). The only non-owner-error recovery is requester expireReview plus a new paid ask, the fee loss the fix set out to remove. The 'cannot finalize under their independently correct bindings' claim in THREAT_MODEL.md is true but incomplete. Fix preserving the design: an owner-only, event-emitting discard of an unconfirmed receipt (receipt stays readable as history), so the ask can be closed by the owner rather than relying on the requester to expire and repay; or let the owner close such an ask as Unanswered without a fee.

**Reproduction**

test/scratch/Judge.t.sol::testSwappedReceiptStrandsTrueMappingAndFinalizesOtherAnswer: two delivered jobs A and B, requestReview on both -> askA, askB. Intake delivers B's correctly signed attestation (UUID_B, answer=true) under askA. bindReview(askA, bodyHashA, UUID_A, qhA, 31337, 1, 2) as owner -> reverts ReviewAttestationMismatch(askA) (A's genuine answer was NotPassed). A second complete(askA) reverts 'not pending' (one shot). bindReview(askA, bodyHashA, UUID_B, qhB, 31337, 1, 2) succeeds: getJob(A).review == Passed. Then bindReview(askB, bodyHashB, UUID_B, ...) reverts DuplicateRequestId(UUID_B). Expected: the owner can pin A's authenticated mapping or discard the misdelivered receipt without a new fee; actual: true mapping permanently refused, swapped fields finalize, B stranded too.

### 4. Low: Owner pre-binding reserves an oracle UUID permanently even when nothing is ever delivered; a protocol-side UUID repeat on a paid retry makes the retry unfinalizable

`src/imd/HookJobRequester.sol:359`

```
        if (intakeReviewOfOracle[oracleRequestId] != bytes32(0) || consumed[oracleRequestId]) {
```

From audit_flow. bindReview reserves intakeReviewOfOracle[oracleRequestId] (line 376) and nothing clears it: not expiry, not failure, not the owner. If the ask expires undelivered and the requester pays for a retry, and the protocol reuses the same UUID for the retried question (IMD_INTEGRATION.md lists UUID repetition across retries as an unverified pilot item), both routes for the retry's genuine signed answer revert DuplicateRequestId: onReviewResult at line 438 (reservedFor != requestId) and bindReview at line 359. consumed[UUID] stays false and no receipt exists, so the reservation is provably unused, yet the retry can never finalize and its fee is lost. Precondition is unverified but not excluded, which is why this is low. Fix preserving the design: an owner-only releaseReservation(oracleRequestId) allowed only when consumed[oracleRequestId] == false and the holder ask is terminal (reviewOf[holder] == 0 and no receipt), with an event; consumed UUIDs stay untouchable.

**Reproduction**

test/scratch/Judge.t.sol::testReservationOfUndeliveredUuidBlocksRetry: job delivered; askA = requestReview; owner bindReview(askA, bodyHash, X, qh, 31337, 1, 2); no delivery. vm.warp(reviewDeadline+1); creator expireReview(job); askA2 = requestReview(job). Intake delivers a valid attestation carrying X to askA2: onReviewResult reverts DuplicateRequestId(X). Owner bindReview(askA2, bodyHash2, X, ...) reverts DuplicateRequestId(X). consumed(X) == false, getReviewReceipt(askA2).oracleRequestId == 0. Expected: an undelivered reservation on a terminal ask can be released; actual: permanent refusal.

### 5. Info: Signer rotation or ERC-1271 revocation does not stop a retained receipt from being confirmed into a verdict (documented, but incident-response relevant)

`src/imd/HookJobRequester.sol:387`

```
        if (receipt.oracleRequestId != bytes32(0)) {
```

From audit_flow. The receipt branch of bindReview (lines 387-398) consumes the UUID and finalizes using only the stored receipt; no signer, freshness or current-authority check runs at confirmation. A receipt taken before setOracleSigner (including a rotation made because the key was compromised) still mints Passed/NotPassed afterwards, whereas an undelivered answer for a pre-bound ask fails BadSignature after the same rotation. AUDIT_5F43F94D.md, THREAT_MODEL.md and IMD_INTEGRATION.md all state this as deliberate historical-answer behavior, so it is reported as a trust assumption with concrete state rather than a code defect: an operator rotating a compromised signer to freeze in-flight verdicts will not freeze retained receipts. If that matters operationally, an owner-only revokeReceipt(intakeRequestId) (event + history kept) would close the gap without changing the normal flow.

**Reproduction**

test/scratch/Judge.t.sol::testReceiptFinalizesAfterSignerRotation: deliver a valid receipt for askA (unbound); owner setOracleSigner(newSigner); owner bindReview(askA, receipt fields) succeeds and getJob(A).review == Passed. Contrast: askB pre-bound to its UUID, then the same rotation, then delivery of a valid attestation signed by the old key: complete() returns false (BadSignature inside the Intake's try) and B stays Pending.

### 6. Info: NotPassed is terminal while the shipped review question defines 'missing or pending review' as false, so a timing-induced honest false can never be corrected

`src/imd/HookJobRequester.sol:315`

```
                || (job.review != ReviewStatus.None && job.review != ReviewStatus.Unanswered)
```

From audit_economics. requestReview is allowed once a job is Delivered or Expired and refused forever once review is Passed or NotPassed. The template in test/helpers/ImdTemplates.sol (documented in IMD_INTEGRATION.md) defines the bool as 'Missing, pending or failed review means false'. An Expired job (completion notice lost, or the unconfirmed onJobResult(bytes32,bytes) ABI reverting inside the Intake's try, both named live assumptions) that is asked before the IMD-side review concludes receives an honest signed false, recorded as NotPassed permanently; onJobResult is refused for Expired jobs and requestReview reverts NotReviewable. The requester has paid for the job and the ask and the static site shows 'did not pass' for the life of the contract. Terminal NotPassed is the agreed economic rule (it is what prevents verdict shopping), so this is reported as a design caveat, not a defect: changing it (allowing a new paid ask after NotPassed with history kept, or dropping the 'pending means false' definition in favour of the existing onReviewFailure/Unanswered path) is a scope decision for the requester. Note the interaction with the medium finding: today the only way around a timing-induced NotPassed is the receipt-first expiry race, which is the wrong incentive.

**Reproduction**

test/scratch/Judge.t.sol::testExpiredJobFalseVerdictIsTerminal: openJob -> J Open; vm.warp(+7 days + 1); creator expireJob(J) -> Expired. requestReview(J) accepted (0.5 IMD pulled). Intake delivers a valid attestation with answer=false; owner bindReview -> review == NotPassed. requestReview(J) reverts NotReviewable(J); onJobResult(J, ...) from the Intake reverts UnknownOrSettled(J). Expected per the requester: a corrected verdict is purchasable once the review completes; actual: permanent NotPassed.

---

Judge's submission `a995d069fca086f5df294fe22808164c9cc8498b64835a170e7d0300dd370d5c`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
