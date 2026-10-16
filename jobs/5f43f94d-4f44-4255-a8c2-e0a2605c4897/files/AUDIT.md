# Audit report

> Re-review the fixes for audit d9970905 at commit 684c3da344f8f9f3a34ed810e55c243eec485090. Test exact oracle-attestation binding, replay/expiry, two-step ownership, EIP-7702/ERC-1271 signatures, and ad cancellation after listing transfer. Check for regressions in escrow accounting. Examine whether the new owner-per-review binding can be completed before the Intake's one-shot callback; distinguish proven local safety from unverified live compatibility.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1811-build-technical-foundation-hooks.git |
| Commit | `684c3da344f8f9f3a34ed810e55c243eec485090` |
| Job | `5f43f94d-4f44-4255-a8c2-e0a2605c4897` |
| Judged | 2026-10-16 04:04 UTC |
| Findings | 1 high · 2 low · 1 info |

Four agents audited the code as it is at `684c3da`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: Per-ask owner binding must land before the Intake's one-shot review callback; an honest, correctly signed answer to the contract's own ask delivered first is refused (ReviewNotBound), never retried, a

`src/imd/HookJobRequester.sol:366`

```
        if (ask.oracleRequestId == bytes32(0)) revert ReviewNotBound(requestId);
```

Merged from four specialist reports (audit_math a6cba18e, audit_economics 15e6096e, audit_permissions fd1246b3, audit_flow 2d584062): same mechanism, same line, one fix. The d9970905 remedy for 'attestation can settle another ask' makes every verdict depend on the owner having already called bindReview(intakeId, bodyHash, oracleRequestId, questionHash, questionChainId, fromBlock, toBlock) with the exact values the oracle will sign. onReviewResult (onlyIntake) reverts ReviewNotBound for an unbound ask, and bindReview afterwards still succeeds but nothing can then apply the already-signed answer: the Intake's writer attempts the callback exactly once inside a try, records a revert as not delivered and does not retry (oracle-consumer reference, 'The callback'), and no other function of this contract accepts an attestation. The values the owner must pin do not exist when the ask is paid for: a.requestId is the oracle request UUID the plane assigns, which the reference says differs from the Intake id on purpose; and with the shipped review template's relative window ({"hours":1} in test/helpers/ImdTemplates.sol and docs/IMD_INTEGRATION.md) the reference states the resolved fromBlock/toBlock and therefore questionHash 'cannot be computed in advance'. The reference names no pre-dispatch mapping endpoint ('the pairing of an answer to the intake request is the writer's'), and docs/AUDIT_D9970905.md lines 43-47 and docs/IMD_INTEGRATION.md lines 77-83 concede this. So under the documented configuration the sequence is deterministic: requestReview spends 0.5 IMD (no refund), the single delivery reverts, the job's review stays Pending until reviewDeadline (1 day default, 1 hour minimum), the requester calls expireReview and gets Unanswered, and a retry costs another 0.5 IMD and faces the same ordering. There is also no rebind path, so a binding typo strands the ask the same way. Proven locally: the fail-closed property holds (ReviewBinding.t.sol: unbound, mismatched, swapped, replayed and late answers never settle, and no oracle id is consumed), and the attached scratch test shows the burn against a mock Intake with the reference's semantics (one attempt, 200k gas, no retry). Unverified live: whether an operator can obtain the UUID and canonical question hash from the plane in the minutes between the plane reading the ask and the writer's callback; the reference gives no such facility and the repository's own docs call review delivery not production-ready. The contract itself does not enforce that: requestReview is open to every requester and charges them. Note the fixture hides the race: HookJobRequesterFixture._bind derives a synthetic UUID and hash locally and binds in the same step as the ask, which a live owner cannot do. Fix that preserves the agreed design (owner may still pin, and a pinned ask must match exactly): either (a) accept, for a pending ask this contract created (reviewOf) when it is unbound, a signature in this contract's domain with the snapshotted panel minimums, issuedAt/deadline checks and _consume(a.requestId), as the reference's same-chain consumer does, keeping bindReview as an optional stricter pre-pin; or (b) on an unbound delivery verify and store the attestation's requestId/questionHash/chainId/fromBlock/toBlock/answer/panel under the Intake id as 'delivered, awaiting confirmation' without consuming, and have bindReview with identical fields consume the oracle id and set Passed/NotPassed. The attached proof passes under either shape. If neither is acceptable, do not let requesters pay until the binding can be satisfied (an owner switch that disables requestReview, or an absolute-window template plus an owner-registered expected questionHash per template).

**Reproduction**

State: HookJobRequester deployed with a mock Intake that pulls the price and calls the callback once under 200,000 gas inside a try (test/scratch/EarlyCallbackBurnsAsk.t.sol, ScratchIntake); owner set the job template and a review template whose suffix contains "window":{"hours":1}; creator approved IMD. Steps: (1) creator.openJob(keccak256("spec"), "a hook"); intake.complete(jobId, abi.encode(jobId, "ipfs://result")) -> Delivered. (2) creator.requestReview(jobId) -> askId; creator's balance drops by 0.5 IMD; getReviewAsk(askId).oracleRequestId == 0. (3) vm.warp(+5 minutes); build Attestation{requestId = bytes16 UUID, chainId 31337, questionHash = keccak256("canonical question document with the resolved window"), answerType 0, answer abi.encode(true), fromBlock 1000, toBlock 1300, panelSize 7, quorum 5, agreed 6, issuedAt now, expiresAt now+1h}, sign requester.attestationDigest(a) with the configured signer key, and call intake.complete(askId, abi.encode(askId, a, sig)). Expected: the Intake's single attempt does not revert, and the review becomes Passed (directly, or after the owner's bindReview with the identical fields) with consumed[a.requestId] == true. Actual: complete returns false (ReviewNotBound(askId) inside the try); getJob(jobId).review == Pending; consumed[a.requestId] == false; a subsequent owner bindReview(askId, bodyHash, a.requestId, a.questionHash, 31337, 1000, 1300) succeeds but intake.complete reverts 'not pending' and onReviewResult from any non-Intake caller reverts NotTheIntake (test/scratch/JudgeChecks.t.sol testBindAfterEarlyCallbackCannotRecoverTheAnswer); after reviewDeadline the creator can only expireReview -> Unanswered; the 0.5 IMD is gone. forge test --match-path test/scratch/EarlyCallbackBurnsAsk.t.sol fails on 684c3da with 'the Intake's single callback reverted (ReviewNotBound) and is never retried'; it passes with a minimal patch that skips the ReviewNotBound/mismatch checks for an unbound own ask (verified locally, patch reverted). The specialist's attached proof .imd/reads/proofs/Proof_a6cba18e4cad.t.sol fails for the same reason.

### 2. Low: issuedAt must be >= askedAt with zero backward tolerance while the base contract allows five minutes of forward drift; attester clock behind the ask block's timestamp loses the one-shot answer

`src/imd/HookJobRequester.sol:371`

```
        if (a.issuedAt < ask.askedAt) revert AttestationPredatesAsk(a.issuedAt, ask.askedAt);
```

Merged from audit_math 62854f0f and audit_flow f4327605 (same check, same fix). askedAt is the block timestamp of the requestReview transaction; a.issuedAt is the attester's wall clock. OracleAttestationConsumer._verifyAttestation already tolerates issuedAt up to ISSUED_AT_TOLERANCE (300 s) ahead of the delivery block, but the new per-ask check tolerates nothing in the other direction. Because the Intake attempts the callback once, a refusal here is unrecoverable: the ask stays Pending until expireReview and the 0.5 IMD is spent. The check adds no replay protection beyond what the binding already gives (a.requestId, questionHash and window are pinned per ask and _consume keys on the oracle id), so it only trades liveness for clock ordering. docs/IMD_INTEGRATION.md line 66 calls the strictness deliberate and defers it to the pilot; the asymmetry with the existing forward tolerance has no stated reason. Honest caveat on likelihood: the attester stamps issuedAt when the panel answers, minutes after the ask, so hitting this needs the attester's clock to lag the chain by more than the panel latency, or an issuedAt stamped at an earlier plane step; the reference does not say which. Fix: tolerate a.issuedAt + ISSUED_AT_TOLERANCE >= ask.askedAt (or a dedicated backward tolerance), keeping expiresAt and the ask deadline as they are.

**Reproduction**

State: a bound pending ask with askedAt = T (test/scratch/JudgeChecks.t.sol, _boundAsk). Input: at T + 3 min the Intake delivers an attestation matching the binding exactly, panel 7/5/6, signed by the configured signer, with issuedAt = T - 1 and expiresAt = T + 1 h. Expected: accepted, as the same attestation with issuedAt = T + 3 min + 300 s is. Actual: onReviewResult reverts AttestationPredatesAsk(T-1, T) from the Intake; the subsequent issuedAt = now + 300 s delivery is accepted (Passed). testOneSecondBackwardSkewRefusedWhileFiveMinutesForwardAccepted passes on 684c3da, i.e. it asserts the current refusal; test/ReviewBinding.t.sol line 171 asserts the same revert at askedAt - 1.

### 3. Low: A bound, matching, unexpired verdict delivered after reviewTimeout is refused in the Intake's single attempt, so a slow panel costs the requester the price

`src/imd/HookJobRequester.sol:365`

```
        if (block.timestamp > ask.deadline) revert ReviewDeadlinePassed(ask.deadline);
```

From audit_permissions 4d21f524, reproduced. onReviewResult refuses delivery once block.timestamp exceeds the ask's deadline even though the ask is still Pending (expireReview not yet called), the owner's binding matches and the attestation is inside its own signed [issuedAt, expiresAt] window. The reference asks consumers to keep a deadline so the requester can clear an unanswered request; it does not ask them to refuse a late but valid answer, and its same-chain consumer accepts any answer for a pending id. Since the Intake never retries, an answer that lands between reviewDeadline and expireReview is lost and the requester must pay 0.5 IMD again. The owner may set reviewTimeout as low as MIN_TIMEOUT (1 hour) while the review body carries validForSeconds 3600 and the attestation its own expiresAt, so the contract-side cut-off duplicates a freshness bound the signature already enforces. With the 1-day default and panels answering in minutes this rarely bites, hence low. Fix: drop the deadline comparison in onReviewResult (keep it as the expireReview gate), or bound answer age by a.issuedAt <= ask.askedAt + reviewTimeout rather than by the delivery block's timestamp; bindReview may keep its deadline check.

**Reproduction**

State: owner.setTimeouts(7 days, 1 hours); creator opened a job, it was delivered, creator.requestReview(jobId) -> askId at time T; owner bound the ask with the correct UUID/hash/chain/window (test/scratch/JudgeChecks.t.sol testBoundValidAnswerAfterReviewTimeoutIsLost). Step: at T + 1 h + 60 s the Intake calls onReviewResult(askId, a, sig) where a matches the binding exactly, issuedAt = now, expiresAt = now + 1 h, panel 7/5/6, valid signature. Expected: the verdict settles. Actual: revert ReviewDeadlinePassed(T + 1 h); intake.complete returns false and marks the request settled; getJob(jobId).review stays Pending; consumed[a.requestId] == false; creator.expireReview -> Unanswered and must pay again. The scratch test passes on 684c3da because it asserts the current refusal.

### 4. Info: The documented review template uses a relative window, which the protocol reference says cannot be pinned in advance, while bindReview requires pinning the resolved window and questionHash before the

`test/helpers/ImdTemplates.sol:14`

```
        ' on this chain finish its adversarial review step with the review recorded as passed?","chainId":31337,"window":{"hours":1},"answerType":"bool","evidence":"panel","panelSize":7,"quorum":5,"validForSeconds":3600,"definitions":{"passed":"The job page shows the adversarial review step completed and the reviewer accepted the delivered code with no unresolved finding. Missing, pending or failed review means false."}}';
```

From audit_flow 955fc8c6; kept separate from the high finding because it lives in the shipped template rather than the contract and has its own fix. The template documented in docs/IMD_INTEGRATION.md and used by every local test asks with "window":{"hours":1}. The oracle-consumer reference states that questionHash covers the resolved block window, that a contract cannot compute it in advance when the window is relative, and that a consumer which pins its question uses absolute windows. bindReview requires the exact questionHash, fromBlock and toBlock, so with this template the owner can only learn the values to pin from the plane after it has resolved them, which is also when the writer dispatches the answer. The local fixture sidesteps this by deriving a synthetic hash from the body and fixed blocks 1..2 (HookJobRequester.t.sol lines 69-77, marked 'NOT the protocol canonical hash algorithm'), so no test exercises the live ordering. Fix: with the current contract design, ship an absolute-window template ({"fromBlock","toBlock"} chosen at ask time) whose questionHash the owner can compute with the protocol package's oracleQuestionHash, or apply the store-then-confirm/accept-own-ask fix from the high finding so the window may stay relative.

**Reproduction**

State: owner calls setReviewTemplate with REVIEW_PREFIX/REVIEW_SUFFIX as documented; creator calls requestReview -> ReviewRequested(jobId, askId, price, body) where body contains "window":{"hours":1}. Input: the owner attempts bindReview immediately after the event. Expected: the owner can compute questionHash, fromBlock and toBlock to pin from the paid body. Actual: they depend on the plane's resolution of the relative window at answer time, so the owner has nothing to pin until the answer exists; any guess that differs from the signed values makes onReviewResult revert ReviewAttestationMismatch (ReviewBinding.t.sol testSignedWrongQuestionIdChainOrWindowCannotSettle shows fromBlock+1 / toBlock+1 refused) and, with no rebind path, the paid answer is lost the same way as in the high finding.

---

Judge's submission `348cdca17c9cfebc6a80fe2d14c9f7e358b40291e2ee17c0997caaef0a9aaf50`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
