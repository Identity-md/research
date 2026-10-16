# Audit report

> Focused review of HookJobRequester.sol at commit 0d9d440063465654f39ef7f3939b1b4d9c90c5f6. Re-run the four actionable findings and proofs from audit ef1f6915-b9df-441d-b2e5-db5e9d9e9b35. Check both callback/expiry transaction orders, owner-confirmed expiry, conflicting or reused UUIDs, receipt discard, cross-request binding, replay, and the 200k-gas one-shot callback with ERC-1271. Report any material blocker and the unresolved live-Intake/owner-trust assumptions. Do not deploy. Unchanged hook, listing and ad contracts are not the focus.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1811-build-technical-foundation-hooks.git |
| Commit | `0d9d440063465654f39ef7f3939b1b4d9c90c5f6` |
| Job | `6b607200-d29f-4c7a-8476-0dca8091f48f` |
| Judged | 2026-10-16 07:02 UTC |
| Findings | 6 low · 5 info |

Four agents audited the code as it is at `0d9d440`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: expireJob can front-run the Intake's late one-shot failure/completion, so the requester's tx order decides Failed vs Expired and makes a refused job reviewable

`src/imd/HookJobRequester.sol:352`

```
            (job.status != JobStatus.Delivered && job.status != JobStatus.Expired)
```

Merged from audit_permissions and audit_flow. expireJob (line 330-337) checks only status==Open, requester and deadline; onJobFailure/onJobResult revert UnknownOrSettled unless the job is still Open; requestReview (line 351-354) accepts Delivered or Expired but not Failed. After the job deadline a requester who sees the Intake's onJobFailure (status 1 refused / 2 no result) in the mempool can send expireJob first. The Intake's single attempt then reverts inside its try and is lost: the job records Expired with failureStatus/failureReason 0 (or no resultHash for a late completion), and the requester can buy a review the Failed state would forbid. Impact is bounded (the oracle still signs the verdict and the shipped question defines a missing review as false; the requester pays the extra fee), but the Intake's authenticated terminal status never reaches chain or the static page and the Failed/Expired eligibility split is bypassable by timing. Untested before this review. Fix that keeps the design: let onJobResult/onJobFailure also land on an Expired job (Expired -> Delivered/Failed, recording the evidence), or treat Failed and Expired the same in requestReview.

**Reproduction**

Reproduced in a scratch Foundry test on HookJobRequesterFixture + MockIntake at 0d9d440 (test/scratch/Judge.t.sol::testExpireJobFrontRunsLateFailure / testControlFailedJobNotReviewable, passes on current code demonstrating the behaviour). State: id = creator openJob(SPEC_HASH, brief); warp deadline+1. Tx1 creator expireJob(id) -> Expired. Tx2 intake.fail(id,1,'body_invalid',0,0) returns false (callback reverted UnknownOrSettled), getJob(id).failureStatus == 0. Tx3 creator requestReview(id) succeeds, reviewOf(ask)==id. Control: with Tx2 first the job is Failed and requestReview reverts NotReviewable(id). Expected: recorded outcome and review eligibility independent of who wins the race. Actual: ordering decides both.

### 2. Low: A pre-bound ask whose genuine callback differs in any context field (e.g. the plane-resolved window) loses the one-shot answer with no receipt, and the binding cannot be corrected

`src/imd/HookJobRequester.sol:550`

```
        ) revert ReviewAttestationMismatch(requestId);
```

From audit_economics. bindReview may run before delivery. The review template uses a relative window ('window':{'hours':1}) resolved by the plane after payment, so a pre-binding of fromBlock/toBlock/questionHash is a guess. In the bound branch any mismatch reverts ReviewAttestationMismatch inside the Intake's single 200k try: no receipt is stored (unlike the unbound branch, which retains a verified answer), the UUID is not consumed, the ask stays Pending and bound, and ask.oracleRequestId is immutable (line 393) so the owner cannot rebind. The verified answer and the fee are lost; recovery needs requester expireReview after the deadline, owner confirmReviewExpiry, owner releaseReservation and a second paid ask. Fix that keeps the design: in the bound branch, retain a verified-but-mismatching callback as a receipt (same write as the unbound path, already measured within the stipend) for owner resolution, or operationally never bind before a receipt exists (require a receipt in bindReview, a scope decision).

**Reproduction**

Reproduced in a scratch Foundry test on HookJobRequesterFixture + MockIntake at 0d9d440 (test/scratch/Judge.t.sol::testPreboundMismatchLosesOneShotAndOwnerCannotClose, passes on current code demonstrating the behaviour). State: job delivered; askId = creator requestReview(jobId); owner bindReview(askId, bodyHash, X, Q, 31337, 1, 2). Input: Intake complete(askId, ...) with a correctly signed fresh NotPassed attestation {requestId X, questionHash Q, chainId 31337, fromBlock 1, toBlock 3}. Expected: verified answer retained (as an unbound ask would). Actual: complete returns false; getReviewReceipt(askId).oracleRequestId == 0; consumed[X] == false; review Pending; intakeReviewOfOracle[X] == askId.

### 3. Low: Only the requester can start closure of a receipt-less pending ask, so an absent requester leaves a bound ask Pending and its oracle UUID reserved forever

`src/imd/HookJobRequester.sol:625`

```
        if (msg.sender != job.requester) revert NotRequester();
```

From audit_economics. Closure of a pending review needs onReviewFailure, discardReviewReceipt (requires a receipt) or confirmReviewExpiry, which requires reviewExpiryRequested, a flag only the job's requester can set here. releaseReservation also requires reviewOf[holder]==0. If a bound ask's one-shot callback is lost (previous finding, over-budget signer, wrong ABI) and the requester never returns, neither the owner nor the Intake can move the job out of Pending or release the reserved UUID. If the protocol later reuses that UUID for another ask, that ask's receipt can't be bound (DuplicateRequestId) and must be discarded as 'receipt UUID conflict', costing that requester a second fee. Fix that keeps the design: let the owner also set the expiry request after the snapshotted deadline (closure still needs confirmReviewExpiry and the no-receipt check).

**Reproduction**

Reproduced in a scratch Foundry test on HookJobRequesterFixture + MockIntake at 0d9d440 (test/scratch/Judge.t.sol::testPreboundMismatchLosesOneShotAndOwnerCannotClose, passes on current code demonstrating the behaviour). State: as above, bound ask with lost callback; warp reviewDeadline+1. Owner calls expireReview(jobId) -> NotRequester; confirmReviewExpiry(askId) -> ReviewExpiryNotRequested(askId); releaseReservation(X) -> ReservationNotReleasable(X). Expected: an owner path to close a deadline-passed, receipt-less ask. Actual: review stays Pending and intakeReviewOfOracle[X] == askId until the requester acts.

### 4. Low: A retained receipt that matches the ask's true context but must not be finalized (e.g. signer later found compromised) has no honest closure path; the job is stuck Pending and cannot be retried

`src/imd/HookJobRequester.sol:465`

```
            if (!consumed[oracleRequestId] && (holder == bytes32(0) || holder == intakeRequestId)) {
```

From audit_flow. With a receipt present: discardReviewReceipt on the same UUID reverts ReviewReceiptMatches unless the UUID is consumed or reserved elsewhere; expireReview and confirmReviewExpiry revert ReviewAlreadyReceived; onReviewFailure reverts ReviewAlreadyReceived; requestReview reverts NotReviewable. The owner's only moves are bindReview (finalizing the untrusted verdict) or a different-UUID 'misdelivered receipt' discard with a fabricated UUID, which the docs forbid. Recorded in docs/IMD_INTEGRATION.md as a retained design choice; reported because the resulting state is unrecoverable without a dishonest call. Fix needs a scope decision, e.g. an owner-only void for receipts verified under a signer that has since been rotated out, or explicit acceptance of the stuck state as policy.

**Reproduction**

Reproduced in a scratch Foundry test on HookJobRequesterFixture + MockIntake at 0d9d440 (test/scratch/Judge.t.sol::testExactContextReceiptHasNoHonestClosure, passes on current code demonstrating the behaviour). State: askId unbound; Intake delivers validly signed Passed for (UUID U, Q, 31337, 1, 2) -> receipt stored. Owner setOracleSigner(rotated). Owner discardReviewReceipt(askId, bodyHash, U, Q, 31337, 1, 2) -> ReviewReceiptMatches(askId). After deadline creator expireReview(jobId) -> ReviewAlreadyReceived(askId); creator requestReview(jobId) -> NotReviewable(jobId). Expected: an honest owner can close the ask as Unanswered. Actual: review stays Pending indefinitely.

### 5. Low: Requester is charged the quoted price even if the Intake pulls less; the surplus is stranded and owner-sweepable

`src/imd/HookJobRequester.sol:804`

```
        _approve(address(intake), 0);
```

From audit_math. _pull transfers intake.priceOf(...) from the caller and approves that amount; _ask resets the allowance to zero but never checks how much the Intake actually took. The documented invariant 'pulls exactly that price ... and holds nothing between calls' therefore rests on unverified live-Intake behaviour. If the Intake pulls less, the requester has overpaid and only the owner's sweep can move the difference (to any address). Fix: after _ask, refund asset.balanceOf(this) surplus to msg.sender, or revert if nonzero.

**Reproduction**

Reproduced in a scratch Foundry test on HookJobRequesterFixture + MockIntake at 0d9d440 (test/scratch/Judge.t.sol::testIntakePullsLessStrandsSurplus, passes on current code demonstrating the behaviour). State: owner setIntake(LessIntake) whose priceOf is 0.5e18 but whose requestWithFailure transferFroms amount-0.1e18. Input: creator openJob(SPEC_HASH, brief). Expected: creator pays what the Intake charged, or revert. Actual: creator -0.5e18, Intake +0.4e18, HookJobRequester holds 0.1e18 with allowance 0.

### 6. Low: openJob/requestReview have no caller-supplied price limit: the price read at execution is pulled up to the owner's contract-wide ceiling

`src/imd/HookJobRequester.sol:788`

```
        if (price > maxPrice) revert PriceAboveCeiling(price, maxPrice);
```

From audit_economics. The only bound is maxPrice, which the owner raises ahead of announced price changes. Between signing and inclusion the Intake's priceOf can rise and a user with a standing allowance pays the new price, non-refundably. Fix that keeps the design: add a caller maxPrice argument (revert if price > min(callerMax, maxPrice)); the static site already shows the current price. Changing the external signatures is an ABI change for the site and SDK.

**Reproduction**

Reproduced in a scratch Foundry test on HookJobRequesterFixture + MockIntake at 0d9d440 (test/scratch/Judge.t.sol::testPriceRaiseUpToCeilingChargesUser, passes on current code demonstrating the behaviour). State: creator approved max; owner setPayment(imd, 5e18); intake price raised from 0.5e18 to 5e18 before inclusion. Input: creator openJob(SPEC_HASH, brief) expecting 0.5 IMD. Expected: 0.5 IMD charged or revert. Actual: 5e18 pulled from creator.

### 7. Info: Live-Intake assumption: a callback delivered synchronously inside request/requestWithFailure is dropped, because job/ask state is written after the call returns

`src/imd/HookJobRequester.sol:282`

```
        requestId = _ask(jobAction, body, this.onJobResult.selector, this.onJobFailure.selector, price);
```

Merged from audit_math, audit_permissions, audit_flow and audit_economics (item b). openJob/requestReview learn the Intake ID only from the return value and record usedIntakeRequestIds, jobs[id] and reviewOf[id] afterwards, so an in-call onJobFailure/onJobResult/onReviewFailure/onReviewResult reverts UnknownOrSettled, the one-shot is consumed and the fee spent; the job stays Open for jobTimeout (requester expiry) or the review stays Pending (requester expiry + owner confirmation). docs/IMD_INTEGRATION.md lists asynchronous delivery as an unverified pilot assumption; MockIntake cannot exercise this order. Pilot blocker to confirm, not a local code change.

**Reproduction**

Reproduced in a scratch Foundry test on HookJobRequesterFixture + MockIntake at 0d9d440 (test/scratch/Judge.t.sol::testSynchronousRefusalDropped, passes on current code demonstrating the behaviour). State: owner setIntake(SyncIntake) whose requestWithFailure pulls 0.5e18, derives id and calls onFailure(id,1,'refused',0,0,'') under 200k before returning. Input: creator openJob. Expected: job Failed status 1. Actual: inner call returned false, job status Open, 0.5e18 held by the Intake.

### 8. Info: After owner-confirmed expiry and a retry, a re-delivered answer issued during the earlier ask is rejected by AttestationPredatesAsk, burning the retry's one-shot

`src/imd/HookJobRequester.sol:555`

```
        if (uint256(a.issuedAt) + ISSUED_AT_TOLERANCE < ask.askedAt) {
```

From audit_math. onReviewResult rejects issuedAt more than 5 minutes before askedAt. If, on a retry, the protocol re-delivers the original signed answer (same UUID, issuedAt from the first ask, still before expiresAt) instead of re-signing, the retry's single attempt reverts and the requester has paid twice with no receipt. The anti-pre-signing intent is sound; whether the oracle re-signs on retry is an unverified protocol behaviour (UUID reuse/timestamp windows listed as unverified). Pilot item: confirm re-signing on retry, or anchor a retry's askedAt to the original by a design decision.

**Reproduction**

Reproduced in a scratch Foundry test on HookJobRequesterFixture + MockIntake at 0d9d440 (test/scratch/Judge.t.sol::testRetryRedeliveryPredatesAsk, passes on current code demonstrating the behaviour). State: ask1 at T; attestation for ask1 issuedAt T+1h, expiresAt T+1h+3d. At T+1d+1 creator expireReview, owner confirmReviewExpiry(ask1), creator requestReview -> ask2 (same body). Input: Intake delivers that signed attestation to onReviewResult(ask2). Expected per retry design: receipt retained. Actual: revert AttestationPredatesAsk(T+1h, T+1d+1); complete returns false; no receipt.

### 9. Info: 200,000-gas one-shot callback: ERC-1271 signer headroom is about 77k cold receipt-first; the production signer is unmeasured and an over-budget signer loses the answer and fee

`src/imd/HookJobRequester.sol:564`

```
        bytes32 digest = _verifyAttestation(a, signature);
```

Merged from audit_math, audit_permissions, audit_flow and audit_economics (item e). _verifyAttestation forwards all remaining gas to isValidSignature. Re-measured at 0d9d440 with test/ReviewReceiptGas.t.sol: cold EOA receipt 123,013; 5-of-7 ERC-1271 receipt 168,106 (also after an expiry request and on a reserved retry), bound 132,880; +22 cold-read registry receipt 185,260, bound 150,053. All fit under 200,000. The 64-cold-read fixture does not fit: the callback runs out of gas, the Intake marks the request settled, nothing is retained or consumed, and recovery is owner-assisted expiry plus a new fee. No code defect. Launch blocker until the real signer/proxy is measured cold on the target chain.

**Reproduction**

forge test --match-path test/ReviewReceiptGas.t.sol -vv prints the figures above; testOverBudgetSignerStillFailsClosedAndLosesSingleAttemptWithoutPartialReceipt passes (setOracleSigner(ColdReadReceiptSigner(signer,64)), complete under 200k returns false, receipt.oracleRequestId == 0, consumed false, review Pending). Expected for launch: the production isValidSignature at or under 60k cold and the whole callback under 200k; actual: only local fixtures measured.

### 10. Info: Unverified live-Intake assumptions that each fail closed into a lost one-shot plus spent fee: job callback ABI, attestation validity window, UUID mapping and uniqueness

`src/imd/HookJobRequester.sol:302`

```
    function onJobResult(bytes32 requestId, bytes calldata result) external onlyIntake {
```

Merged from audit_flow and audit_economics (items a, d, f, g). (1) The job.open callback shapes (bytes32,bytes) and (bytes32,uint8,bytes32,uint16,uint16,bytes) are assumed; a different live ABI reverts in the Intake's try and the job can only be expired after 7 days. (2) An answer delivered after expiresAt (template validForSeconds 3600) reverts AttestationExpired even unbound, so a delivery lag beyond one hour loses the answer. (3) Oracle UUID/questionHash/window are not derivable on chain; bindReview relies on an authenticated off-chain mapping source that doesn't exist yet. (4) Intake IDs are assumed unique and nonzero (_recordIntakeId reverts the whole paid ask otherwise). None is a local code defect; they are pilot acceptance conditions.

**Reproduction**

Reproduced in a scratch Foundry test on HookJobRequesterFixture + MockIntake at 0d9d440 (test/scratch/Judge.t.sol::testLateDeliveryAfterSignatureExpiryLost, passes on current code demonstrating the behaviour). for (2): unbound ask, attestation issuedAt=now, expiresAt=now+1h; warp now+1h+1; Intake complete returns false; no receipt. For (1): existing test/HookJobRequester.t.sol testCallbackWithUnexpectedAbiFailsSafeAndJobCanExpire (complete(id, hex'deadbeef') returns false, job stays Open).

### 11. Info: Owner-trust assumptions: misdelivery discard accepts any unused UUID, expiry confirmation needs no on-chain evidence, bindReview pairing is owner-asserted, and setIntake/setOracleSigner apply immediat

`src/imd/HookJobRequester.sol:699`

```
        intake = IIntake(to);
```

Merged from audit_permissions (3 findings), audit_flow and audit_economics. These are intentional, documented powers (docs/AUDIT_EF1F6915.md 'Expiry and owner trust', THREAT_MODEL 'Malicious requester owner'), not bypasses: (a) discardReviewReceipt's different-UUID branch (line 470) lets the owner close a genuine NotPassed as 'misdelivered receipt' with an invented UUID, after which a retry can be bound to Passed; (b) confirmReviewExpiry (line 642-652) checks only the requester flag and no receipt, so an early confirmation burns a later genuine answer and opens a paid retry; (c) bindReview's Intake-to-oracle pairing is unauthenticated on chain; (d) setIntake/setOracleSigner govern deliveries for asks paid earlier, so a rotated Intake+signer can settle any pending ask, and the old Intake's in-flight callbacks revert NotTheIntake; (e) owner unavailability blocks every receipt-first finalization and retry. Both ef1f6915 callback/expiry orders hold: an expiry request alone never blocks delivery or binding, and a receipt always blocks confirmation (AuditExpiryProof.t.sol, ReviewAuditRegression.t.sol pass). Mitigation is operational: requester-approved multisig owner, event monitoring, preserved evidence.

**Reproduction**

Reproduced in a scratch Foundry test on HookJobRequesterFixture + MockIntake at 0d9d440 (test/scratch/Judge.t.sol::testOwnerDiscardsGenuineNotPassedWithInventedUuid / testConfirmedExpiryBurnsLaterAnswer, passes on current code demonstrating the behaviour). (a) askA receives a signed NotPassed; owner discardReviewReceipt(askA, bodyHash, keccak256('invented'), Q, 31337, 1, 2) succeeds; creator re-asks askB, owner binds, Intake delivers Passed -> review Passed. (b) bound ask, deadline+1, creator expireReview, owner confirmReviewExpiry, Intake's genuine NotPassed returns false (UnknownOrSettled), creator requestReview succeeds. (d) existing ReviewBinding.t.sol::testOwnerRotationPowersApplyToAlreadyPendingRequestsAsDocumented passes.

---

Judge's submission `de62449b121100d34ceebbfd8b197c6da1dc9db719041aa89b853a220babc8b1`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
