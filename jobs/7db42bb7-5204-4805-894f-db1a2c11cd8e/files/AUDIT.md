# Audit report

> Audit commit 357201be804e18ab48567172fb6c8b07acb30a2c. Focus on changes since 205fa11271ab17a26630154815fae4c390aac624 addressing https://explorer.imd.fun/jobs/2218802d-0828-4f00-81cf-487b51c12aac.
> Verify late-build reserve refresh and requester-only renewal without extra payment/cancelled revival/NotPassed shopping; skew-tolerant signed validity and delayed true/false callbacks; trigger-time signer/epoch snapshots, bounded retired-key trust, pending/finalized emergency revocation and ERC1271 caller context; Delivered-only immutable commitments; codec body/pin/consumer equivalence. Preserve exact ArtifactV2 deployment authorization, escrow/refunds, native eight-block windows and recovery/replay controls.
> Check updated SDK/UI and per-chain block-age assumptions. Independently rerun regressions, 24576-byte runtime and isolated 200000-gas callbacks on Ethereum and mocked Robinhood. Distinguish owner/registry trust and live-integration gaps from code findings. No deployment or paid requests.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1811-build-technical-foundation-hooks.git |
| Commit | `357201be804e18ab48567172fb6c8b07acb30a2c` |
| Job | `7db42bb7-5204-4805-894f-db1a2c11cd8e` |
| Judged | 2026-10-19 02:58 UTC |
| Findings | 1 medium · 3 low · 2 info |

Four agents audited the code as it is at `357201b`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Chain-independent maxWindowAgeBlocks default (7200 native blocks) is about 13 minutes on Robinhood and 24 hours on Ethereum, while the same callback accepts signed answers for up to two days; a valid

`src/imd/automatic/AutoHookJobRequester.sol:61`

```
    uint64 public maxWindowAgeBlocks = 7200;
```

Merged from audit_math, audit_flow, audit_economics and the audit_permissions trust note. requestVerdict copies maxWindowAgeBlocks into windowAge[askId]; onReviewResult (line 346) reverts InvalidWindow when head() - att.toBlock > windowAge[askId]. Every other bound in that callback is in seconds and was widened in this commit: issuedAt <= deadline + 300 s and delivery until expiresAt <= issuedAt + 86400 s, and the oracle body the contract emits asks for validForSeconds 86400. The block bound is a chain-independent native count. On Robinhood (4663) head() is ArbSys.arbBlockNumber(); I measured the public RPC during this review: 189 native blocks in 21 s (about 0.11 s/block), so 7200 blocks is about 13 minutes. On Ethereum at 12 s/block the bound closes at about 24 h after trigger, before the issuance bound (deadline + 300 s) and about a day before the delivery bound. When the bound bites, the Intake's one 200k-gas callback reverts, review stays Pending with the reserve already spent, and the requester cannot renew, retry or cancel (intakeId set, review Pending). Only the owner's confirmReviewExpiry after ask.deadline unblocks it, and the requester then pays a second reserve via retryVerdict. The 7200 default ships in code, in deployment/automatic.draft.json defaultPanel (ownerCalls is empty), and script/preflight_automatic.py line 48 accepts it on any chain. docs/AUTOMATIC_BINDING.md records the sizing as an operator duty and says no Robinhood cadence was measured; the measurement above shows the shipped default rejects practically every real panel answer on the primary target chain, so this is a code/configuration default defect, not only a live-integration gap. The owner can mitigate with setPanel, which is an owner trust assumption to record. Fix preserving the design: derive the default from the codec's chain clock (for example codec-provided defaultWindowAge: about 1,731,008 for 4663 and 14,433 for 1 and 11155111 to cover 173,100 s, or at minimum 8 + ceil(86,700 s / cadence)), and/or make openJob refuse to take payment on 4663 until setPanel has set an age bound at least that large; add a regression at the deadline boundary on both clocks.

**Reproduction**

Attached proof, run with forge test --match-path test/scratch/RobinhoodAgeDefault.t.sol: vm.chainId(4663), ArbSys mock etched at address(100), requester deployed with defaults, openJob/deliver/commitArtifact, advance 8 native blocks, outsider requestVerdict (reserve 0.5 ether spent). Warp +13 minutes and advance the native counter by 7800 (13 min at the measured cadence); block.timestamp is still inside ask.deadline. Intake delivers a correctly signed true attestation (exact window, issuedAt = now, expiresAt = now + 1 day, panel 7/5/5, trigger-time key). Expected: accepted, review Passed. Actual: onReviewResult reverts InvalidWindow because 7808 > 7200, intake.complete returns false, review stays Pending. Fails now with 'valid answer 13 minutes after trigger rejected under the 4663 default age bound'. Ethereum variant (test/scratch/Probe.t.sol::testEthereumDefaultAgeRejectsAnswerIssuedInsideDeadline, passes, asserting the defect): chainId 1, attestation issuedAt = ask.deadline (inside the issuance bound), delivered at block toBlock + 7201 and deadline + 12 s: callback returns false and review stays Pending. Live cadence check: eth_getBlockByNumber latest on https://rpc.mainnet.chain.robinhood.com returned block 92280132 at 1792378481 and block 92280321 at 1792378502.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {AutoHookJobRequester} from "src/imd/automatic/AutoHookJobRequester.sol";
import {HookRequestCodec} from "src/imd/automatic/HookRequestCodec.sol";
import {HookJobRequester} from "src/imd/HookJobRequester.sol";
import {IIntake} from "src/imd/IIntake.sol";
import {GatedHookDeployer} from "src/deployment/GatedHookDeployer.sol";
import {OracleAttestation} from "src/imd/OracleAttestation.sol";
import {HookSpec, HookSpecLib} from "src/HookSpec.sol";

contract Tok {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

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

contract Intake {
    uint256 private n;
    mapping(bytes32 => address) public target;
    mapping(bytes32 => bytes4) public sel;

    function priceOf(bytes32, address) external pure returns (uint256) {
        return 0.5 ether;
    }

    function requestWithFailure(bytes32, bytes calldata, IIntake.Callback calldata cb, bytes4, address asset, uint256 amount)
        external
        returns (bytes32 id)
    {
        Tok(asset).transferFrom(msg.sender, address(this), amount);
        id = keccak256(abi.encode(address(this), ++n));
        target[id] = cb.target;
        sel[id] = cb.selector;
    }

    /// One-shot, 200k stipend, like the live Intake.
    function complete(bytes32 id, bytes calldata args) external returns (bool ok) {
        (ok,) = target[id].call{gas: 200_000}(bytes.concat(sel[id], args));
    }
}

contract ArbSysMock {
    uint256 public h;

    function setHead(uint256 v) external {
        h = v;
    }

    function arbBlockNumber() external view returns (uint256) {
        return h;
    }
}

/// Robinhood 4663, unchanged deployment defaults. The native counter advances ~10 blocks per
/// second (public RPC measurement 2026-10-19: blocks 92267521..92274721 spanned 741 s), so the
/// chain-independent 7200-block age bound is ~12 minutes while the signed validity the requester
/// itself asks for (validForSeconds 86400) and the ask deadline are 24 hours.
contract RobinhoodAgeDefaultTest is Test {
    AutoHookJobRequester auto_;
    GatedHookDeployer gated;
    Intake intake;
    Tok tok;
    HookSpec spec;
    address creator = makeAddr("creator");
    address outsider = makeAddr("outsider");
    uint256 pk = 0xB0B;

    function setUp() public {
        vm.chainId(4663);
        vm.warp(1_800_000_000);
        vm.roll(1000);
        vm.etch(address(100), type(ArbSysMock).runtimeCode);
        ArbSysMock(address(100)).setHead(92_000_000);
        intake = new Intake();
        tok = new Tok();
        HookRequestCodec codec = new HookRequestCodec();
        auto_ = new AutoHookJobRequester(address(this), address(intake), address(tok), vm.addr(pk), 1 ether, codec);
        gated = new GatedHookDeployer(address(this), HookJobRequester(address(auto_)));
        spec = HookSpec({
            schemaVersion: 1,
            templateId: HookSpecLib.TEMPLATE_ID,
            chainId: 4663,
            poolManager: address(0xBEEF),
            poolManagerCodeHash: keccak256("manager runtime"),
            permissions: HookSpecLib.PERMISSIONS,
            maxSpecifiedAmount: 1_000_000
        });
        tok.mint(creator, 10 ether);
        vm.prank(creator);
        tok.approve(address(auto_), 10 ether);
    }

    function _advance(uint64 count) internal {
        ArbSysMock(address(100)).setHead(auto_.head() + count);
    }

    function _artifact(bytes32 id) internal view returns (GatedHookDeployer.Artifact memory a) {
        a = GatedHookDeployer.Artifact({
            jobRequestId: id,
            sourceHash: sha256("src"),
            sourceSubmissionHash: sha256("source submission"),
            reviewSubmissionHash: sha256("review submission"),
            evidenceHash: bytes32(0),
            buildHash: keccak256("build"),
            creationCodeHash: keccak256("creation"),
            constructorArgsHash: keccak256("args"),
            runtimeCodeHash: keccak256("runtime"),
            chainId: block.chainid,
            deployer: address(gated),
            poolManager: spec.poolManager,
            poolManagerCodeHash: spec.poolManagerCodeHash,
            permissions: spec.permissions
        });
        a.evidenceHash = sha256(gated.evidenceDocument(a));
    }

    function _signed(bytes32 vid, bytes32 askId) internal view returns (bytes memory) {
        AutoHookJobRequester.Ask memory ctx = auto_.getAsk(askId);
        OracleAttestation.Attestation memory t = OracleAttestation.Attestation({
            requestId: keccak256("uuid"),
            chainId: block.chainid,
            questionHash: auto_.expectedQuestionHash(askId, ctx.fromBlock, ctx.toBlock),
            answerType: 0,
            answer: abi.encode(true),
            figure: 0,
            fromBlock: ctx.fromBlock,
            toBlock: ctx.toBlock,
            blockHash: bytes32(uint256(1)),
            panelJobId: keccak256("panel"),
            panelSize: 7,
            quorum: 5,
            agreed: 5,
            issuedAt: uint64(block.timestamp),
            expiresAt: uint64(block.timestamp) + 1 days
        });
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(pk, auto_.attestationDigest(t));
        return abi.encode(vid, t, abi.encodePacked(r, s, v));
    }

    function testDefaultAgeBoundOnRobinhoodCoversTheSignedValidityItRequests() public {
        vm.prank(creator);
        (bytes32 jobId, bytes32 askId) = auto_.openJob(spec, address(gated), "hook", 0.5 ether, 0.5 ether);
        assertTrue(intake.complete(jobId, abi.encode(jobId, keccak256("completion"), "ipfs://r")));
        GatedHookDeployer.Artifact memory a = _artifact(jobId);
        vm.prank(creator);
        auto_.commitArtifact(jobId, a, bytes20(keccak256("commit")));
        _advance(8);
        vm.prank(outsider);
        bytes32 vid = auto_.requestVerdict(askId);
        assertEq(tok.balanceOf(address(intake)), 1 ether, "reserve spent at trigger");

        // Panel answers 13 minutes later: 7800 native blocks at the measured cadence, well inside
        // the 24 hour ask deadline and the 24 hour signed validity.
        vm.warp(block.timestamp + 13 minutes);
        _advance(7800);
        assertLt(block.timestamp, auto_.getAsk(askId).deadline);
        bool accepted = intake.complete(vid, _signed(vid, askId));
        assertTrue(accepted, "valid answer 13 minutes after trigger rejected under the 4663 default age bound");
        assertEq(uint8(auto_.getJob(jobId).review), uint8(HookJobRequester.ReviewStatus.Passed));
    }
}
```

### 2. Low: Preflight's new native-window-age check only requires maxWindowAgeBlocks >= 8, which setPanel and the constructor already guarantee, so an unsized 7200 default on Robinhood passes preflight

`script/preflight_automatic.py:48`

```
    require('native window age permits confirmed depth',age_blocks >= depth)
```

From audit_flow. docs/AUTOMATIC_BINDING.md makes per-chain sizing of maxWindowAgeBlocks a launch gate and this read-only preflight is the only automated check of it. The check compares age_blocks with WINDOW_DEPTH (8). The constructor default is 7200 and setPanel reverts below 8, so the check cannot fail on any deployed requester and never relates the age bound to the signed-validity window at the chain's cadence. A Robinhood deployment left at the default (deployment/automatic.draft.json defaultPanel, ownerCalls empty) passes every preflight check and then loses verdicts as in the medium finding. Fix: require a per-chain minimum (for 4663 refuse the untouched 7200 and require at least 8 + ceil(86,700 / measured cadence), or take the measured cadence as an input and print the implied seconds), and record the chosen policy value in the output.

**Reproduction**

Call preflight(rpc, requester, deployer, spec) against a requester whose maxWindowAgeBlocks() returns 7200 and WINDOW_DEPTH() returns 8 on chainId 4663 (constructor defaults). Expected: the native window age check fails or warns because 7200 native blocks is about 13 minutes against a two-day acceptance window. Actual: require('native window age permits confirmed depth', 7200 >= 8) passes and the report lists maxWindowAgeBlocks: 7200 with all checks true. The same arithmetic on chainId 1 (7200 >= 8) also passes. Static inspection: the only comparison on line 48 is age_blocks >= depth; test/test_automatic.py exercises no failing case for it.

### 3. Low: Owner trust gap: confirmReviewExpiry is allowed from ask.deadline + 1 s while the callback still accepts answers issued until deadline + 300 s and delivered until their 24 h expiry, so a still-valid s

`src/imd/automatic/AutoHookJobRequester.sol:605`

```
        if (block.timestamp <= a.deadline) revert DeadlineNotReached();
```

Merged from audit_math, audit_permissions and audit_economics. The widened bounds at lines 347-349 accept an attestation with issuedAt <= deadline + ISSUED_AT_TOLERANCE and block.timestamp <= expiresAt <= issuedAt + REVIEW_TIMEOUT, so a conforming answer can land up to about 86,700 s after ask.deadline (subject to the block-age bound). confirmReviewExpiry only requires block.timestamp > a.deadline. In that overlap the owner can delete reviewOf[intakeId] and set Unanswered; the late answer then reverts UnknownOrSettled in the one-shot callback and the requester may retryVerdict for the same candidate, so a signed NotPassed that was in flight never lands. This needs the owner, and docs/IMD_INTEGRATION.md already tells the owner to establish non-delivery first, so it is an owner trust assumption rather than a bypass; it is reported because the contract's own acceptance bound and expiry bound disagree and the NatSpec 'cannot erase any verified true or false answer' covers only answers already received. Minimal fix keeping the recovery power: require block.timestamp > uint256(a.deadline) + ISSUED_AT_TOLERANCE + REVIEW_TIMEOUT (the last instant a conforming answer can still verify), or document the pre-emption window explicitly.

**Reproduction**

test/scratch/Probe.t.sol::testOwnerExpiryPrecedesAcceptanceWindow (passes, asserting the behaviour) on the AutomaticBinding fixture: _ready(); ctx = getAsk(askId); warp to ctx.deadline + 1; build a NotPassed attestation with issuedAt = ctx.deadline, expiresAt = ctx.deadline + 1 days, signed by the trigger-time key. Control: intake.complete(verdictId, ...) returns true and review becomes NotPassed. Same state, owner calls confirmReviewExpiry(verdictId) first: succeeds, review Unanswered; the identical delivery then returns false (UnknownOrSettled); creator's retryVerdict(jobId, FEE) succeeds with a fresh askId. Expected per the documented acceptance of delayed answers: the still-valid answer is terminal; actual: it is discarded and the verdict re-requested.

### 4. Low: An Intake review-price rise above the prepaid reserve strands a Delivered, committed candidate: readiness still reports ready, the trigger reverts PriceExceeded, renewVerdict adds no funds, retryVerdi

`src/imd/automatic/AutoHookJobRequester.sol:466`

```
        if (j.review != HookJobRequester.ReviewStatus.Unanswered) revert NotReady();
```

Merged from audit_permissions and audit_economics. requestVerdict quotes the live price capped at p.reserve (line 251) and reverts PriceExceeded when the Intake has raised the review price above the reserve chosen at openJob. No path adds funds to an unspent ask: retryVerdict is the only funding entry and is gated on Unanswered, which an untriggered ask never reaches; renewVerdict deliberately moves no tokens; commitArtifact is one-shot. verdictReadiness does not consult the quote, so the SDK and UI readiness gates keep offering a trigger that always reverts (the NatSpec on line 293 acknowledges 'fee changes may still prevent a ready ask'). Until reserveDeadline the requester cannot cancel; after it, cancelReserve returns the reserve but sets cancelled permanently, so even if the price later drops the delivered, committed build can never be reviewed and the build fee is sunk. The precondition is an Intake price change, a trusted external action, so this is partly a live-integration dependency; the code gap is the missing re-funding path. Fix: allow retryVerdict (or a topUpReserve) when review == None, candidateDigest != 0, asks[jobAsk[jobId]].intakeId == 0 and !cancelled, adding the pulled amount to p.reserve and reserved[asset] and refreshing the window; and/or have verdictReadiness (or SDK/UI) compare the live quote with p.reserve.

**Reproduction**

test/scratch/Probe.t.sol::testPriceRiseStrandsDeliveredCandidate (passes, asserting the lock-in) on the AutomaticBinding fixture: _open() with reserve 0.5 ether; _deliver; _commit; roll +8; intake.setPrice(reviewAction, imd, 0.5 ether + 1). verdictReadiness(askId).ready == true; requestVerdict(askId) reverts PriceExceeded(0.5e18+1, 0.5e18); creator retryVerdict(jobId, FEE+1) reverts NotReady; renewVerdict reverts DeadlineNotReached; after warping past reserveDeadline renewVerdict succeeds but reserveOf(jobId).amount is still 0.5 ether; after the next deadline cancelReserve succeeds; price lowered back to 0.5 ether: renewVerdict and retryVerdict both revert NotReady, approvedArtifact(jobId) == 0 and the Intake still holds the 0.5 ether build fee. Expected: some requester path to fund or trigger the verdict, or readiness false; actual: none.

### 5. Info: Design note: clock-skew tolerance is one-sided; issuedAt one second before the trigger block's timestamp is rejected while 300 s of forward skew is accepted

`src/imd/automatic/AutoHookJobRequester.sol:347`

```
                || att.issuedAt < a.askedAt || att.issuedAt > uint256(a.deadline) + ISSUED_AT_TOLERANCE
```

From audit_permissions and the audit_flow trust note. The remediation added ISSUED_AT_TOLERANCE on the forward side only; the lower bound att.issuedAt < a.askedAt has no tolerance. a.askedAt is the trigger block's timestamp, set by the block producer or sequencer; the attester stamps with its own clock. An attester whose clock lags the trigger block by more than the panel's answering time would lose the one-shot callback (review Pending, owner recovery, second payment). The author tests this bound deliberately (test/Audit2218802d.t.sol testIssuanceMustNotPrecedeAsk) and a real panel answer takes far longer than any plausible clock lag, so this is a design choice with very limited exposure, recorded for completeness and not counted as a defect. If symmetric tolerance is wanted: accept issuedAt + ISSUED_AT_TOLERANCE >= a.askedAt.

**Reproduction**

test/scratch/Probe.t.sol::testBackwardSkewAtAskBoundaryRejected (passes, asserting the behaviour): _ready(); warp +600 s; attestation with issuedAt = askedAt - 1, expiresAt = issuedAt + 1 days, otherwise exact and signed by the trigger-time key; vm.prank(intake); onReviewResult reverts InvalidWindow. Same attestation with issuedAt = askedAt is accepted and review becomes Passed.

### 6. Info: Owner/registry trust assumptions and live-integration gaps kept separate from code findings: bounded retired-key trust, two-transaction emergency revocation, owner recovery powers, mutable registry me

`src/imd/automatic/AutoHookJobRequester.sol:256`

```
        a.verification = (uint256(uint160(oracleSigner)) << 96) | (uint256(oracleSignerEpoch) << 64);
```

Merged from the audit_permissions and audit_flow info items; none is a permission bypass. (1) Retired-key trust is bounded but long: after an ordinary setOracleSigner the previous EOA or registry stays authoritative for every ask triggered before rotation until issuedAt > deadline + 300 s or now > expiresAt, about two days after trigger, subject to the block-age bound; only revokeSignerEpoch cuts it off, which also kills the pending answer and forces a paid retry. (2) Emergency revocation of the current epoch needs two owner transactions (setOracleSigner then revokeSignerEpoch(old)) because revokeSignerEpoch rejects epoch >= oracleSignerEpoch; an answer by the compromised key landing between them is recorded but approvedArtifact returns 0 once the epoch is revoked and closeRevokedVerdict lets the requester retry, so the window is bounded and recoverable. (3) With an ERC-1271 registry as signer only the registry address is snapshotted; key membership inside it stays mutable under the registry's own trust model. ERC-1271 is evaluated with the requester as caller and ECDSA is tried first, so a registry address cannot be impersonated by a raw signature; confirmed by test/Audit2218802d.t.sol ERC1271/EOA-with-code tests. (4) requestVerdict is permissionless, so whoever triggers chooses the trigger block whose signer, epoch and maxWindowAgeBlocks are snapshotted; at worst this pins an about-to-be-rotated signer and costs a retry after owner revocation. (5) The ArbSys clock, the Intake's one-shot 200k callback and the registry are exercised only with mocks. Independently re-measured with forge test --isolate: cold EOA / 5-of-7 / 22-cold-read ERC-1271 onReviewResult minimum forwarded gas 126,557 / 171,617 / 188,699 on the Ethereum clock and 132,223 / 177,283 / 194,365 on the mocked Robinhood clock, leaving 5,635 gas of margin for the heaviest mocked registry; any heavier live registry breaks the one-shot callback. (6) forge build --sizes: AutoHookJobRequester 24,258 bytes (318 of margin under EIP-170), HookRequestCodec 15,292, GatedHookDeployer 20,967; the codec codehash pin in openJob must match the deployed codec exactly. (7) All 640 Foundry tests, the 10 Python SDK tests in test/test_automatic.py and the 10 Node UI tests pass locally; no deployment or paid request was made. The SDK/UI gate commitArtifact on Delivered and on an uncancelled reserve, and the renew path moves no funds, matching the contract.

**Reproduction**

Retired-key window: test/scratch/Probe.t.sol::testRetiredKeyWindowAfterRotation (passes): _ready(); owner setOracleSigner(new); attestation by the old key with issuedAt = deadline + 300, expiresAt = issuedAt + 1 days; warp to expiresAt; intake.complete succeeds and approvedArtifact(jobId) equals the candidate digest. Emergency revocation and ERC-1271 context: test/Audit2218802d.t.sol testFuzzRevokedPendingSignerFailsAndRecoveryIsGuarded, testFuzzFinalizedRevocationPreservesHistoryAndAllowsOnlyOwnerRecovery, testERC1271IsVerifiedInRequesterContextAfterRotation, testEOAWithCodeUsesECDSAFirstAfterRotation all pass. Gas and sizes: forge test --isolate --match-contract 'AutomaticGasTest|ReviewReceiptGasTest' -vv and forge build --sizes, figures above. These describe designed behaviour and operational responsibilities, not failures of the stated requirements.

---

Judge's submission `f0731fedf4fa705ba3de4faa5052d5e67cad3699b8d62c5dff7b796cddd9d709`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
