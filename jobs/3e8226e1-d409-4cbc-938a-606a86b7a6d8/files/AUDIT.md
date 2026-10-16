# Audit report

> Audit commit 575e8a8f74da581298a8527f493e9eab8a45901f, focusing on changes since eb1333775e60fe191acfa5a420e9256feeb4a2b0. Read the original report: https://api.imd.fun/jobs/648ba2e5-46a0-4759-8439-73a6c9d81af6/report.md — not just the remediation summary. Reproduce and verify the same-UUID context-mismatch recovery, corrected quorum checks and assembled-body step-marker validation. Test unauthorized discard, fabricated owner context, genuine NotPassed verdict shopping, replay, retries and retained receipt history. Clearly distinguish enforced protections from owner-trust assumptions. Reproduce finding #4 exactly: Intake takes payment and invokes a callback inside request/requestWithFailure before returning, swallowing a callback revert. The new pre-payment revert test does not cover this. State whether it remains a live-compatibility blocker and what evidence would resolve it. Rerun the full regression suite, check payment caps/accounting and listing/ad escrow, remeasure worst-case callbacks against 200k gas, and verify deployed bytecode size against the contract-size limit. Separate material code blockers, documented owner powers and unverified live-protocol assumptions. No deployment, paid Intake request or fund movement.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1811-build-technical-foundation-hooks.git |
| Commit | `575e8a8f74da581298a8527f493e9eab8a45901f` |
| Job | `3e8226e1-d409-4cbc-938a-606a86b7a6d8` |
| Judged | 2026-10-16 19:39 UTC |
| Findings | 2 low · 6 info |

Four agents audited the code as it is at `575e8a8`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Report 648ba2e5 finding #4 still reproduces: a post-payment callback delivered inside request/requestWithFailure is rejected UnknownOrSettled and burned with the fee; the new pre-payment refusal test

`src/imd/HookJobRequester.sol:986`

```
            requestId = intake.requestWithFailure(action, body, callback, onFailure, asset, price);
```

Merged from audit_flow 7d1abbcb, audit_economics fb0a644d, audit_math cd1f98bb and audit_permissions 7759e8c7; all four proofs were run and fail on this commit for the stated reason. openJob (lines 310-313) and requestReview (lines 392-395) call _ask, which calls intake.requestWithFailure/request, and only after it returns run _recordIntakeId and write jobs[requestId] (or reviewOf[intakeRequestId]). The four callbacks carry onlyIntake but not nonReentrant, so an Intake that pulls the price, assigns id R and invokes onJobFailure/onJobResult/onReviewResult/onReviewFailure before returning reaches them while job.status == None (reviewOf == 0); they revert UnknownOrSettled(R), the Intake's try swallows it, the outer call returns normally and the contract records the job as Open (ask as Pending) with the fee spent and no failure/result/receipt record. The job can only be expired by its requester after jobTimeout (7 days); an ask needs owner confirmReviewExpiry after reviewTimeout; a synchronously delivered signed verdict (including a NotPassed) is lost with no receipt. What commit 575e8a8 added is MockIntake.setRefusal, which reverts BEFORE transferFrom; testFuzzSynchronousIntakeRefusalRevertsTheWholeAskWithoutDebit therefore exercises whole-ask rollback, and testAsynchronousRefusalAfterPaymentClosesWithoutRefund calls back in a later transaction. Neither delivers a callback while the request call is on the stack, so the shape finding #4 describes (payment taken, callback inside the request, revert swallowed) is untested; MockIntake cannot reach it. docs/IMD_INTEGRATION.md line 380 now states 'A synchronous callback during payment is unsupported', so the project treats this as a pilot requirement rather than a code fix. Classification: not a permission bypass and no funds beyond the spent fee are at risk; it is an unverified live-protocol assumption that nothing in the repository proves. It remains a live-compatibility blocker until resolved by evidence. Evidence that would resolve it: (a) the Intake v2 source or verified bytecode on the launch chain showing request/requestWithFailure never calls the callback target or failure function before returning, or an authoritative protocol statement to that effect; or (b) one paid pilot request per path (requestWithFailure with a body refused AFTER payment, not an unsold action which reverts pre-payment, and a plain request) whose trace shows no internal call into this contract before the request returns and whose failure/result arrives in a later transaction with the job recorded Failed/Delivered. Minimal fix preserving the design if the pilot shows synchronous delivery: set a transient 'asking' marker in _ask and let the callbacks, when the id is unknown and the marker is set, buffer (id, status, reason/resultHash or the retained receipt) instead of reverting, then have openJob/requestReview apply the buffered notice to the returned id (reverting the whole ask if the ids differ); or write provisional job/ask state before the external call and move it to the returned id. Note the runtime is 24,081 bytes with 495 bytes of margin, so the change must be small.

**Reproduction**

Deploy HookJobRequester against an Intake whose requestWithFailure transfers the price, assigns id R and immediately calls onFailure(R, 1, 'refused', 0, 0, '') on the callback target inside a low-level call (test/scratch/Proof_7759e8c794df.t.sol SyncCallbackIntake). Owner sets templates; creator approves and calls openJob(keccak256('spec'), 'my hook', 0.5e18). Expected: getJob(R).status == Failed (3) with reason 'refused', or the transaction reverts and the creator keeps 0.5 IMD. Actual: the inner call fails with revert selector == UnknownOrSettled.selector, openJob returns R, getJob(R).status == Open (1), creator balance drops by 0.5 IMD, expireJob(R) reverts DeadlineNotReached for 7 days. With failureHook off, the v1 request path delivering a synchronous onJobResult leaves status Open (1) instead of Delivered (2). forge test --match-path 'test/scratch/Proof_*' on this commit: all four specialist proofs fail ('synchronous post-payment refusal was swallowed: job left Open, fee spent, no failure record: 1 != 3'; '... result lost: 1 != 2'; audit_math's second test shows the same for onReviewResult with a validly signed NotPassed: getReviewReceipt(ask).oracleRequestId == 0, review Pending, fee spent).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {HookJobRequester} from "src/imd/HookJobRequester.sol";
import {IIntake} from "src/imd/IIntake.sol";

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

/// @dev An Intake that takes payment, assigns the request id and refuses the ask by invoking the
/// failure function (or the result callback) synchronously, inside request/requestWithFailure,
/// before returning. The callback revert is swallowed by its try, exactly as finding #4 describes.
contract SyncCallbackIntake {
    mapping(bytes32 => mapping(address => uint256)) public priceOf;
    uint256 nonce;
    bytes32 public lastId;
    bool public innerOk;
    bytes public innerRet;

    function setPrice(bytes32 action, address asset, uint256 p) external {
        priceOf[action][asset] = p;
    }

    function requestWithFailure(
        bytes32 action,
        bytes calldata,
        IIntake.Callback calldata cb,
        bytes4 onFailure,
        address asset,
        uint256 amount
    ) external payable returns (bytes32 id) {
        require(amount == priceOf[action][asset], "wrong amount");
        ScratchToken(asset).transferFrom(msg.sender, address(this), amount);
        id = keccak256(abi.encode(++nonce));
        lastId = id;
        (innerOk, innerRet) = cb.target.call{gas: 200_000}(
            abi.encodeWithSelector(onFailure, id, uint8(1), bytes32("refused"), uint16(0), uint16(0), bytes(""))
        );
    }

    function request(bytes32 action, bytes calldata, IIntake.Callback calldata cb, address asset, uint256 amount)
        external
        payable
        returns (bytes32 id)
    {
        require(amount == priceOf[action][asset], "wrong amount");
        ScratchToken(asset).transferFrom(msg.sender, address(this), amount);
        id = keccak256(abi.encode(++nonce));
        lastId = id;
        (innerOk, innerRet) = cb.target.call{gas: 200_000}(bytes.concat(cb.selector, abi.encode(id, bytes("done"))));
    }
}

contract SyncCallbackIntakeTest is Test {
    bytes32 constant JOB = "job.open@test";
    bytes32 constant ORACLE = "oracle.request@test";
    uint256 constant PRICE = 0.5 ether;
    ScratchToken imd;
    SyncCallbackIntake intake;
    HookJobRequester req;
    address owner = makeAddr("owner");
    address creator = makeAddr("creator");
    uint256 key = 0xA11CE;

    function setUp() public {
        vm.warp(1_800_000_000);
        imd = new ScratchToken();
        intake = new SyncCallbackIntake();
        intake.setPrice(JOB, address(imd), PRICE);
        intake.setPrice(ORACLE, address(imd), PRICE);
        req = new HookJobRequester(owner, address(intake), address(imd), vm.addr(key), PRICE);
        vm.startPrank(owner);
        req.setJobTemplate(JOB, "steps: forge build, forge test, adversarial review. spec ", " brief <", ">");
        req.setReviewTemplate(ORACLE, "Did the adversarial review of job ", " pass?", 5, 4);
        vm.stopPrank();
        imd.mint(creator, 10 ether);
        vm.prank(creator);
        imd.approve(address(req), type(uint256).max);
    }

    /// Finding #4: a synchronous refusal issued after payment, inside requestWithFailure, must
    /// either be recorded as a failure or leave the fee with the creator. On this code the inner
    /// callback reverts UnknownOrSettled(id) because the job is written only after the Intake
    /// returns; the fee is pulled, the job stays Open and the one-shot failure notice is lost.
    function testSynchronousPostPaymentRefusalIsRecordedOrRolledBack() public {
        uint256 before = imd.balanceOf(creator);
        vm.prank(creator);
        try req.openJob(keccak256("spec"), "my hook", PRICE) returns (bytes32 id) {
            assertEq(id, intake.lastId());
            // Evidence of the swallowed revert on the current code (informational on a fixed one).
            if (!intake.innerOk()) {
                bytes memory ret = intake.innerRet();
                bytes4 sel;
                assembly {
                    sel := mload(add(ret, 0x20))
                }
                emit log_named_bytes32("inner revert selector (UnknownOrSettled = 0x...)", bytes32(sel));
                assertEq(sel, HookJobRequester.UnknownOrSettled.selector, "inner callback reverted for another reason");
            }
            assertEq(
                uint8(req.getJob(id).status),
                uint8(HookJobRequester.JobStatus.Failed),
                "synchronous post-payment refusal was swallowed: job left Open, fee spent, no failure record"
            );
        } catch {
            assertEq(imd.balanceOf(creator), before, "refused ask must not keep the fee");
        }
    }

    /// Same shape with the failure hook off: the v1 `request` path delivering a synchronous
    /// result. The result must be recorded Delivered or the ask rolled back.
    function testSynchronousPostPaymentResultOnV1PathIsRecordedOrRolledBack() public {
        vm.prank(owner);
        req.setFailureHook(false);
        uint256 before = imd.balanceOf(creator);
        vm.prank(creator);
        try req.openJob(keccak256("spec"), "my hook", PRICE) returns (bytes32 id) {
            assertEq(
                uint8(req.getJob(id).status),
                uint8(HookJobRequester.JobStatus.Delivered),
                "synchronous post-payment result was swallowed: job left Open, fee spent, result lost"
            );
        } catch {
            assertEq(imd.balanceOf(creator), before, "refused ask must not keep the fee");
        }
    }
}
```

### 2. Low: Owner trust, not an enforced boundary: discardMismatchedReviewReceipt compares the receipt only with owner-supplied context, so one call with a fabricated question/chain/window sets aside a genuine No

`src/imd/HookJobRequester.sol:610`

```
        if (_receiptMatches(receipt, oracleRequestId, questionHash, questionChainId, fromBlock, toBlock)) {
```

Merged from audit_flow aa6e9e92, audit_economics 65126b77 (route A), audit_math 07265826 and audit_permissions 6e77982e; reproduced in test/scratch/JudgeProbe.t.sol testFabricatedContextDiscardsGenuineNotPassedAndRetryReplay. The new same-UUID recovery (lines 589-624) verifies the owner's context only through _validateReviewBinding (body hash, non-zero fields, fromBlock <= toBlock) and the public reviewReceiptHash acknowledgment; the ReviewReceiptMatches guard fires only when the owner repeats the receipt's own signed fields. Any single differing field (questionHash ^ 1, fromBlock 0, another chainId) closes a genuine, signer-verified NotPassed as Unanswered with reason 'receipt context mismatch', leaves its UUID X unconsumed and unreserved, and re-opens requestReview for the requester. Because the discard neither reserves nor consumes X, the owner can then bind the retry to (X, true context) and a fresh-signed copy of the same attestation settles the retry; alternatively a new Passed answer settles it, so the job shows Passed while the NotPassed receipt remains only in history. Enforced on this commit (verified): requester and stranger revert NotOwner on both discard functions, resetReviewBinding, releaseReservation and confirmReviewExpiry; a retained receipt blocks expireReview, confirmReviewExpiry (ReviewAlreadyReceived) and requestReview (NotReviewable); a second delivery reverts ReviewAlreadyReceived; a bound ask reverts ReviewAlreadyBound until reset; the true context reverts ReviewReceiptMatches; a wrong receiptHash reverts ReviewReceiptMismatch; the stale signed answer replayed into the retry reverts AttestationPredatesAsk, and a fresh-signed one delivered to the unbound retry is retained, not settled; the receipt with its verdict stays readable and discardedReviewReceipts[ask] == true; consumed UUIDs are refused for delivery (AlreadyConsumed) and binding (DuplicateRequestId). Not enforced (owner trust): the authenticity of the asserted context, the honesty of a mismatch closure, and re-binding a retry to a previously discarded UUID. IMD_INTEGRATION.md already discloses that 'an owner who asserts a different true question for a receipt carrying the ask's own UUID can also close a receipt as Unanswered', so this is a documented, logged owner power inside the existing trust boundary and not a permission bypass; it is the same power as the pre-existing misdelivery branch (report 648ba2e5 #1 route 1) with one fewer step. However README.md lines 118-121 and docs/AUDIT_648BA2E5.md ('a receipt matching the ask's true context can only be bound, so a genuine NotPassed cannot be discarded this way') read as an enforced protection; the contract can only enforce that a discard does not name the receipt's own context. Fix (documentation and observability, preserving the feature): state in README/AUDIT docs that the guard is a consistency check on owner-supplied data and that Passed/NotPassed badges are only as trustworthy as the owner key; emit the receipt's own signed questionHash/chainId/window beside the owner's context in ReviewReceiptDiscarded (today only the owner's context and the UUIDs are logged) so observers can see which field the owner claimed differed; keep the operator duty to publish the canonical question before any set-aside.

**Reproduction**

HookJobRequesterFixture (minPanelSize 5, minAgreed 4). Delivered job J; creator requestReview -> unbound ask A. Intake delivers a valid attestation (UUID X, questionHash Q, chainId 31337, window 1..2, answer false) -> retained, getJob(J).review == Pending. creator and stranger: discardMismatchedReviewReceipt / discardReviewReceipt -> NotOwner. Owner: discardMismatchedReviewReceipt(A, keccak256(bodyOf(A)), reviewReceiptHash(A), Q, 31337, 1, 2) -> ReviewReceiptMatches(A). Owner: same call with keccak256('owner asserts other question') -> succeeds. Expected per README wording: the genuine NotPassed cannot be set aside. Actual: getJob(J).review == Unanswered, consumed[X] == false, intakeReviewOfOracle[X] == 0, getReviewReceipt(A).passed == false still readable, discardedReviewReceipts[A] == true; creator.requestReview(J, 0.5e18) succeeds (Pending). Fresh-signed (X, Q, false) delivered to the unbound retry is retained; owner bindReview(retry, bodyR, X, Q, 31337, 1, 2) finalizes NotPassed and consumes X. test/scratch/JudgeProbe.t.sol testFabricatedContextDiscardsGenuineNotPassedAndRetryReplay passes on this commit, demonstrating each step.

### 3. Info: Report 648ba2e5 finding #1 route 3 (borrowed, resettable UUID conflict in discardReviewReceipt) is unchanged and still reproduces; now dominated by discardMismatchedReviewReceipt

`src/imd/HookJobRequester.sol:558`

```
            if (!consumed[oracleRequestId] && (holder == bytes32(0) || holder == intakeRequestId)) {
```

From audit_flow 8a5b4f57 and audit_economics 65126b77 (route B), also noted by audit_permissions 6e77982e; reproduced in test/scratch/JudgeProbe.t.sol testBorrowedConflictDiscardStillReproduces. The same-UUID branch of discardReviewReceipt accepts a reservation held by another pending ask as the 'onchain conflict' that justifies closing an exactly matching receipt, and resetReviewBinding can remove that reservation afterwards, leaving no inconsistency on chain. The remediation note scopes itself to findings #2, #3 and #5 and leaves this as it was; the docstring at lines 530-532 ('A field typo, negative value or elapsed time alone cannot justify discard') remains a statement about honest input, not a code property. With the new function the owner has a cheaper, logged route to the same outcome (previous finding), so this is an owner-trust consistency note rather than new risk. Minimal consistency fix, if wanted: in this branch count only consumed[oracleRequestId] as a conflict, or make resetReviewBinding/releaseReservation refuse a reservation that was cited as conflict evidence.

**Reproduction**

HookJobRequesterFixture. Ask A (creator) retains a genuine NotPassed with UUID X, question Q. Second user's unbound ask B. Owner: bindReview(B, bodyB, X, Q, 31337, 1, 2); discardReviewReceipt(A, bodyA, X, Q, 31337, 1, 2). Expected per the documented guard: revert ReviewReceiptMatches(A). Actual: succeeds with reason 'receipt UUID conflict'; owner resetReviewBinding(B, bodyB) leaves intakeReviewOfOracle[X] == 0 and consumed[X] == false; getJob(jobA).review == Unanswered; creator requestReview(jobA, 0.5e18) opens a new Pending ask. Test passes on this commit.

### 4. Info: Remediation note overstates coverage: 'compatible with both refusal shapes' omits the synchronous post-payment callback shape of finding #4, which no test exercises and which IMD_INTEGRATION.md labels

`docs/AUDIT_648BA2E5.md:30`

```
**Compatibility statement.** The contract is compatible with both refusal shapes. Which shape the
```

From audit_permissions 9bac974c, reproduced by reading. The two shapes the note tests are a pre-payment revert (whole ask rolls back; MockIntake.setRefusal reverts before transferFrom) and an asynchronous post-payment failure callback (fee spent, job Failed/ask Unanswered). The shape in report 648ba2e5 finding #4, a callback invoked inside request/requestWithFailure after the price is debited, is a third shape: the fee is spent AND no failure is recorded (first finding above). docs/IMD_INTEGRATION.md line 380 correctly labels it unsupported, so the two documents disagree on whether the refusal story is closed, and an operator reading only the remediation note would conclude finding #4 is resolved. Fix: name the unsupported shape in the compatibility statement, point to the pilot item, and either add a MockIntake mode that calls back inside _request so the suite covers the shape explicitly or state that it is deliberately untested.

**Reproduction**

Read docs/AUDIT_648BA2E5.md lines 21-34 against docs/IMD_INTEGRATION.md line 380 and test/helpers/MockIntake.sol _request (line 91: refusal reverts before any transfer). grep for a MockIntake path that invokes the callback target inside _request finds none; the specialist proofs in test/scratch/Proof_*.t.sol reach that path and the job is left Open with the fee spent.

### 5. Info: Relaxed panel check accepts a signed quorum of 0 and a minority share: agreed is compared with minAgreed as an absolute count, so 4-of-100 with quorum 0 settles as Passed

`src/imd/HookJobRequester.sol:720`

```
        if (a.panelSize < ask.minPanelSize || a.agreed < ask.minAgreed || a.agreed < a.quorum || a.agreed > a.panelSize)
```

From audit_math df2ad8ba, reproduced in test/scratch/JudgeProbe.t.sol testQuorumChecks. After 575e8a8 removed `a.quorum < ask.minAgreed`, the lower bounds on agreement are agreed >= minAgreed (absolute) and agreed >= a.quorum (oracle-signed, may be 0). minPanelSize is a floor, never a ceiling, so a larger panel dilutes the agreement share without limit. The same 4-of-100 input also settled before the change (with quorum 4), so this is not a regression; it is safe only if the oracle never signs a sub-majority answer, which is the oracle's documented quorum semantics. Boundary math is otherwise correct: quorum <= agreed <= panelSize on uint16, no casts; the original #3 reproduction (panel 5, quorum 3, agreed 5) now settles; agreed below minAgreed, below the signed quorum, or above panelSize still reverts PanelTooWeak inside the one-shot. If the intended guarantee is 'a majority of the panel agreed', add `2 * a.agreed > a.panelSize` or a configured ratio; otherwise document that panel strength beyond the absolute minimum is the oracle's signed quorum semantics.

**Reproduction**

HookJobRequesterFixture (minPanelSize 5, minAgreed 4), bound ask. Attestation panelSize 7, quorum 0, agreed 3 -> onReviewResult reverts PanelTooWeak(7,0,3) (minAgreed enforced). Attestation panelSize 100, quorum 0, agreed 4, answer true, validly signed -> intake.complete returns true, getJob(J).review == Passed, reviewPanelSize 100, reviewAgreed 4. Expected if 'panel agreed' means a majority: PanelTooWeak; actual: settled. Second bound ask: panelSize 5, quorum 3, agreed 5, answer false -> NotPassed (previous finding #3 input now accepted).

### 6. Info: Remediations verified on 575e8a8: same-UUID context-mismatch recovery, corrected quorum check and per-fragment step-marker validation behave as documented; payment caps, exact accounting, replay and l

`src/imd/HookJobRequester.sol:605`

```
        _validateReviewBinding(
```

From audit_economics 9ff12b9e, re-verified. forge test at this commit: 25 suites, 240 passed, 0 failed, including FeaturedInvariant and FeaturedTransferInvariant (listing/ad escrow, 256 runs each, 0 reverts) and RequesterMvpPaymentTest. Context mismatch (previous #2): a pre-bound ask whose receipt carries its UUID but another question reverts ReviewAlreadyBound from discardMismatchedReviewReceipt until resetReviewBinding, then closes Unanswered with the receipt retained; expireReview on the closed job reverts UnknownOrSettled; a late onReviewResult/onReviewFailure on the terminal id reverts UnknownOrSettled. Quorum (previous #3): see the quorum finding. Step markers (previous #5): a marker straddling prefix/middle or middle/suffix now reverts TemplateMissingStep; a marker whole in any fragment, including the suffix alone, is accepted. Payment: a retry quoted above maxPrice reverts PriceAboveCeiling and above userMaxPrice reverts PriceAboveUserMaximum with no debit, zero standing allowance and zero contract balance; a lower quote pulls exactly that quote. Replay: a consumed UUID reverts AlreadyConsumed on delivery to another ask and DuplicateRequestId on binding; a stale signed answer replayed to a retry reverts AttestationPredatesAsk. No defect found in the changed code beyond the items above.

**Reproduction**

test/scratch/JudgeProbe.t.sol: testPreboundMismatchNeedsResetThenCloses, testStepMarkers, testPaymentCapsAndAccounting, testConsumedUuidReplayRefused, testQuorumChecks all pass on this commit; forge test prints '240 tests passed, 0 failed'. Expected == actual in every case.

### 7. Info: Remeasured one-shot callback gas (worst tested path 192,286 of 200,000) and runtime size (24,081 bytes, 495 under EIP-170): both hold locally, production signer not modelled

`src/imd/HookJobRequester.sol:732`

```
            _reviewReceipts[requestId] = StoredReviewReceipt({
```

From audit_economics d7fa7018 (also audit_permissions), re-run. forge test --match-path test/ReviewReceiptGas.t.sol -vv at this commit: cold EOA receipt 124,984; 5-of-7 ERC-1271 receipt 170,077 (same after an expiry request and with a reserved retry UUID); 5-of-7 bound 132,553; 22-cold-read registry receipt 187,231 and bound 149,726; mismatched pre-binding 175,123 (5-of-7) and 192,286 (22-read). All about 300 gas below the previous report's numbers, matching the removed comparison. Headroom on the heaviest tested path is 7,714 gas. forge build --sizes: HookJobRequester runtime 24,081 bytes, margin 495 bytes; initcode 25,825 (margin 23,327); FeaturedPlacements 8,232; HookListingRegistry 9,035. Both rest on pilot-only assumptions: the stipend is exactly 200,000 forwarded in full; the production signer verifies in under roughly 67k cold with signatures no larger than the fixture's. A signer costing more than about 7.7k above the 22-read fixture on the mismatched pre-binding path loses the one-shot answer with no receipt, no verdict and no refund. Not a code defect; a signer qualification item, and any future addition to this contract must fit in 495 bytes of runtime or deployment fails.

**Reproduction**

forge test --match-path test/ReviewReceiptGas.t.sol -vv prints the numbers above (8 tests pass). Failing input for the budget: oracleSigner = ColdReadReceiptSigner(signer, 64) on a mismatched pre-binding ask -> intake.complete returns false, getReviewReceipt(ask).oracleRequestId == 0, review stays Pending, fee spent (testOverBudgetSignerStillFailsClosedAndLosesSingleAttemptWithoutPartialReceipt). forge build --sizes prints Runtime Margin 495 for HookJobRequester.

### 8. Info: Unverified live-protocol assumptions unchanged since report 648ba2e5: callback sender and ABI, exact priceOf debit, non-recycled Intake ids, asynchronous delivery; documented owner powers listed separ

`src/imd/HookJobRequester.sol:288`

```
        if (msg.sender != address(intake)) revert NotTheIntake();
```

From audit_economics 3a464e48, re-verified locally. Nothing in 575e8a8 changes these and none can be verified from this repository (MockIntake satisfies them by construction). (1) All four callbacks require msg.sender == intake and the exact selectors onJobResult(bytes32,bytes), onReviewResult(bytes32,Attestation,bytes) and the six-argument failure shape; a dispatcher/executor sender or other encoding reverts inside the Intake's try, fees spent, jobs Open until local expiry. (2) InexactIntakeSpend (line 991) requires the Intake to debit exactly priceOf in the same call; any rounding or fee split makes both paid entry points revert for every caller until setIntake/redeploy (fail-closed, fee not lost). (3) _recordIntakeId refuses a reused id, so deterministic or recycled ids for a byte-identical retry body make every review retry revert DuplicateRequestId (fee not lost). (4) Asynchronous delivery: first finding. Material code blockers: none found. Documented owner powers (all onlyOwner behind two-step ownership, logged): bindReview, resetReviewBinding, discardReviewReceipt, discardMismatchedReviewReceipt, confirmReviewExpiry, releaseReservation, revokeSignerEpoch, closeRevokedReviewReceipt, setIntake, setPayment, setFailureHook, setOracleSigner, setJobTemplate, setReviewTemplate, setTimeouts, sweep. Pilot items before any wallet approves funds: one paid request per path confirming sender, ABI, exact debit, a fresh id and asynchronous delivery.

**Reproduction**

Local evidence only: test/HookJobRequester.t.sol testResultAcceptedOnceFromIntakeOnly (non-intake sender -> NotTheIntake, job stays Open); testCallbackWithUnexpectedAbiFailsSafeAndJobCanExpire (MockIntake.complete(id, hex'deadbeef') -> false, job expires after the deadline); RequesterMvpPaymentTest (intake.setUnspent(1) -> openJob and requestReview revert InexactIntakeSpend, balances unchanged); intake.setReuseIds(true) after an Unanswered ask -> requestReview reverts DuplicateRequestId. Expected on a live chain: Delivered/Passed with a fresh id and an exact debit. Actual live behaviour is not known from this repository.

---

Judge's submission `9536f7ed63ef38ffa955f3c606d325e8babe0f47726f523a6276f8f013f8cb15`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
