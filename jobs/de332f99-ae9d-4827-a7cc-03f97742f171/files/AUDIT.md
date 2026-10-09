# Audit report

> Audit the HiveSeatVault contract in src/HiveSeatVault.sol: a non-upgradeable custody vault holding Project Hive's identity.md seat NFTs (ERC-721 collection 0x0000eC93127BAA929E58E97dd0095A2BFb38ec1D). The owner is a 48h OpenZeppelin TimelockController; a scoped seatOperator hot key may pair and run the seats but must never be able to move them. The ERC-1271 WorkerAuthorization pairing (authorizeWorker, revokeWorkerAuthorization, workerAuthorizationDigest, isValidSignature) is lifted verbatim from the audited IMDSeatStrategy so IMD accepts this contract as a seat's signer; the EIP-712 domain is 'IdentityMD Worker' version 2, bound to the seat collection. The security of the whole design rests on one property and it deserves the hardest look. (1) isValidSignature must return the ERC-1271 magic value ONLY for digests inserted by authorizeWorker, i.e. well-formed WorkerAuthorizations whose wallet equals address(this) and whose tokenId the vault owns. There must be NO path by which the seatOperator, a hot key that may be compromised, can cause isValidSignature to accept an arbitrary hash, in particular the hash of a Seaport order that would list or sell a seat. Confirm authorizeWorker only ever stores the EIP-712 digest it computes itself from a structured WorkerAuthorization, that an attacker-chosen digest cannot be inserted into the mapping, and that no Seaport or marketplace order hash can collide with a WorkerAuthorization digest. Then the custody invariants. (2) A seat NFT must leave the vault ONLY via withdrawSeat, which is onlyOwner (the Timelock): confirm there is no other path that transfers, approves (approve or setApprovalForAll), or lists a held seat, and that the vault never grants NFT approval to anyone. (3) The seatOperator's only powers are authorizeWorker, revokeWorkerAuthorization and registerAgent: confirm none of them can move value or a seat, and that a leaked operator key can at worst grief (stop pairing), never steal. (4) sweepEarnings must be unable to move a seat: it uses the ERC-20 interface, reverts if the token is the seat collection, and sends only to the fixed rewardSink. Confirm there is no caller-supplied destination and no way to reach the ERC-721 collection through it. (5) withdrawSeat, setSeatOperator, setRewardSink and setEnsName are all onlyOwner: confirm there is no privilege-escalation or reentrancy path around the Timelock, and that onERC721Received cannot be abused to brick the vault or spoof an approval. (6) The contract is non-upgradeable with no delegatecall and no selfdestruct: confirm the rules cannot change silently. Also assess reentrancy on registerAgent (external adapter call) and sweepEarnings (token transfers), and whether a hostile ERC-20 passed to sweepEarnings can do anything beyond reverting its own sweep. New since the last round (fix for audit 41fa0208): (7) routeERC20(token, to, amount) is an onlyOwner (= 48h Timelock) ERC-20 exit for launch tokens that refuse a plain sweep to rewardSink; confirm it is onlyOwner, reverts on the seat collection and on to == address(0), cannot reach a seat by any path, and does not weaken any invariant above. (8) script/DeployHiveSeatVault.s.sol now supports a cancel-only guardian (temporary deployer admin, renounced in the same broadcast); confirm the deployer and proposer end with no DEFAULT_ADMIN_ROLE, the guardian can only cancel, and the comment's description of TimelockController self-administration is accurate. Report findings rather than fixing them. Do not propose changes to the 48h timelock design, the operator model, or the economics.

| | |
|---|---|
| Repository | https://github.com/ProjectHive-IMD/hive-seat-vault.git |
| Commit | `c1081ba0325699192f8c1029b0524dde619ee0db` |
| Job | `de332f99-ae9d-4827-a7cc-03f97742f171` |
| Judged | 2026-10-09 15:23 UTC |
| Findings | 3 low · 7 info |

Four agents audited the code as it is at `c1081ba`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Deploy script accepts HIVE_TIMELOCK_PROPOSER = address(0) when a guardian is set, producing a timelock nobody can propose to and a vault whose seats can never leave

`script/DeployHiveSeatVault.s.sol:39`

```
        address proposer = vm.envAddress("HIVE_TIMELOCK_PROPOSER"); // team key / multisig that queues ops
```

The proposer is read with vm.envAddress and never checked for zero. The only incidental guard is `require(guardian != proposer)` on line 43, which rejects a zero proposer only when no guardian is configured; with HIVE_TIMELOCK_GUARDIAN set (the recommended configuration) a zero proposer passes. OpenZeppelin's TimelockController constructor then grants PROPOSER_ROLE and CANCELLER_ROLE to address(0). schedule/scheduleBatch are onlyRole(PROPOSER_ROLE) (not onlyRoleOrOpenRole), and no transaction can originate from address(0), so no operation can ever be queued. The timelock's only DEFAULT_ADMIN_ROLE holder is itself, so the role cannot be repaired without a queued self-call, which is impossible. Every post-deploy require in the script passes (owner is the timelock, delay is 48h, deployer/proposer are not admin, guardian is canceller and not proposer), so the script logs success. Because the vault's owner is this dead timelock and renounceOwnership is disabled, every seat later deposited is stranded: withdrawSeat, setSeatOperator, routeERC20, transferOwnership are unreachable forever. Fix: `require(proposer != address(0), "proposer required")` before constructing the timelock, plus a post-deploy `require(timelock.hasRole(timelock.PROPOSER_ROLE(), proposer))`. Severity is low because it needs an explicitly zero env value, but the outcome is irreversible and the script's stated job is to fail on exactly this kind of misconfiguration. (Merged from audit_economics 25eb398c; the sibling guardian==executor gap is reported separately.)

**Reproduction**

Inputs: HIVE_REWARD_SINK=<non-zero>, HIVE_TIMELOCK_PROPOSER=0x0000000000000000000000000000000000000000, HIVE_TIMELOCK_GUARDIAN=<non-zero>. Call DeployHiveSeatVault.run(). Expected: revert before deploying. Actual: run() completes and logs success; timelock.hasRole(PROPOSER_ROLE, address(0)) == true; vm.prank(guardian); timelock.schedule(vault, 0, withdrawSeat(1, holder), 0, 0, 48h) reverts with AccessControlUnauthorizedAccount; no address can ever schedule. Reproduced with the attached test/scratch/Proof_25eb398c696c.t.sol: `forge test --match-path test/scratch/Proof_25eb398c696c.t.sol` fails both tests on the current script ('next call did not revert as expected' and 'script accepted a zero proposer'), and passes once run() rejects a zero proposer.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {TimelockController} from "@openzeppelin/contracts/governance/TimelockController.sol";
import {DeployHiveSeatVault} from "script/DeployHiveSeatVault.s.sol";
import {HiveSeatVault} from "src/HiveSeatVault.sol";

/// The deploy script must refuse HIVE_TIMELOCK_PROPOSER = address(0): with a guardian set the
/// `guardian != proposer` check passes, the timelock is created with PROPOSER_ROLE held only by
/// address(0), nobody can ever schedule an operation, and every seat deposited is stranded forever.
contract DeployZeroProposerTest is Test {
    function test_script_rejects_zero_proposer() public {
        vm.setEnv("HIVE_REWARD_SINK", vm.toString(makeAddr("sink")));
        vm.setEnv("HIVE_TIMELOCK_PROPOSER", vm.toString(address(0)));
        vm.setEnv("HIVE_TIMELOCK_GUARDIAN", vm.toString(makeAddr("guardian")));

        DeployHiveSeatVault script = new DeployHiveSeatVault();
        vm.expectRevert(); // expected: the script refuses a zero proposer
        script.run(); // actual (current code): it deploys a timelock nobody can propose to
    }

    function test_zero_proposer_timelock_strands_everything() public {
        vm.setEnv("HIVE_REWARD_SINK", vm.toString(makeAddr("sink")));
        vm.setEnv("HIVE_TIMELOCK_PROPOSER", vm.toString(address(0)));
        vm.setEnv("HIVE_TIMELOCK_GUARDIAN", vm.toString(makeAddr("guardian")));
        DeployHiveSeatVault script = new DeployHiveSeatVault();
        (bool ok, bytes memory ret) = address(script).call(abi.encodeCall(script.run, ()));
        if (!ok) return; // once the script validates the proposer, this test is moot and passes
        (TimelockController tl, HiveSeatVault vault) = abi.decode(ret, (TimelockController, HiveSeatVault));
        assertEq(vault.owner(), address(tl));
        bytes memory data = abi.encodeCall(HiveSeatVault.withdrawSeat, (1, makeAddr("holder")));
        // the only PROPOSER_ROLE holder is address(0): no EOA or contract can ever queue a withdrawal
        vm.prank(makeAddr("guardian"));
        vm.expectRevert();
        tl.schedule(address(vault), 0, data, bytes32(0), bytes32(0), 48 hours);
        assertTrue(tl.hasRole(tl.PROPOSER_ROLE(), address(0)));
        assertFalse(tl.hasRole(tl.PROPOSER_ROLE(), makeAddr("guardian")));
        // expected: a deploy that can never withdraw a seat must not succeed
        fail("script accepted a zero proposer: the vault owner is a timelock nobody can ever propose to");
    }
}
```

### 2. Low: Deploy script comment says the guardian 'cannot queue or execute anything'; with the default open executor it can execute any READY op, and the script never rejects guardian == executor

`script/DeployHiveSeatVault.s.sol:28`

```
 *           but cannot queue or execute anything. Without it, the proposer is the only canceller.
```

Item (8) asks whether the comment's description is accurate. The self-administration part (lines 19-25) is accurate against the vendored OpenZeppelin TimelockController: the constructor always grants DEFAULT_ADMIN_ROLE to address(this); updateDelay reverts unless msg.sender == address(this); grantRole/revokeRole need DEFAULT_ADMIN_ROLE, which only the timelock holds after the deployer renounces; so any rule change is itself a queued 48h self-call. The guardian sentence on line 28 is not accurate: the script defaults HIVE_TIMELOCK_EXECUTOR to address(0), which the constructor turns into an open EXECUTOR_ROLE (onlyRoleOrOpenRole passes for every caller when hasRole(EXECUTOR_ROLE, address(0))). The guardian can therefore execute any READY operation, exactly like every other address. Queuing is correctly impossible (no PROPOSER_ROLE, asserted on line 80). In addition, the only separation the script enforces is guardian != proposer (line 43); HIVE_TIMELOCK_EXECUTOR is read independently (line 41) and never compared with the guardian, and the post-deploy asserts (lines 76-81) never check EXECUTOR_ROLE, so a deployment with a dedicated executor equal to the guardian passes every require and leaves a 'cancel-only' guardian that is also the sole executor. Impact is documentation plus a missing self-check: the guardian gains nothing a random EOA lacks under the default, and an executor cannot create operations. Fix: reword line 28 to 'cannot queue anything (with executor = address(0) execution of READY ops is open to everyone, the guardian included)', and add `require(guardian != executor)` or `require(!timelock.hasRole(timelock.EXECUTOR_ROLE(), guardian))` next to the existing guardian checks. (Merged from audit_permissions 4128e80d, audit_economics 3ad17528, audit_flow e184ccca.)

**Reproduction**

(a) Wire exactly as the script does with guardian G and no executor: new TimelockController(48h, [P], [address(0)], deployer); grantRole(CANCELLER_ROLE, G); renounceRole(DEFAULT_ADMIN_ROLE, deployer). P schedules withdrawSeat(1, holder); warp +48h; vm.prank(G); timelock.execute(...). Expected per the comment: revert. Actual: hasRole(EXECUTOR_ROLE, G) == false yet execute succeeds and seat 1 moves to holder (test/scratch/JudgeRepro.t.sol::test_guardian_executes_under_open_executor). (b) Set HIVE_TIMELOCK_PROPOSER=0xP, HIVE_TIMELOCK_GUARDIAN=0xG, HIVE_TIMELOCK_EXECUTOR=0xG and call run(). Expected per the header's 'cancel-only' promise: revert. Actual: run() completes; hasRole(EXECUTOR_ROLE, G) and hasRole(CANCELLER_ROLE, G) are both true (JudgeRepro.t.sol::test_script_accepts_guardian_equal_executor).

### 3. Low: Deploy script hardcodes mainnet collection/adapter addresses but never checks the chain id or that they have code

`script/DeployHiveSeatVault.s.sol:33`

```
    address constant SEAT_COLLECTION = 0x0000eC93127BAA929E58E97dd0095A2BFb38ec1D;
```

SEAT_COLLECTION and AGENT_ADAPTER are mainnet constants and the post-conditions only check timelock/owner wiring. Nothing asserts block.chainid == 1 or SEAT_COLLECTION.code.length > 0 / AGENT_ADAPTER.code.length > 0 before vm.startBroadcast, and the vault constructor only rejects address(0). Pointed at any other RPC (testnet, L2, wrong fork) the script broadcasts a 48h timelock and a vault whose immutable seatCollection has no code. authorizeWorker, registerAgent and isValidSignature all call seatCollection.ownerOf, which reverts on a code-less address (extcodesize check / empty return data), and the vault cannot be re-pointed (immutable, non-upgradeable). No funds are at risk; the broadcast is wasted, and a stale constant would ship silently if the collection ever migrated. Fix: `require(block.chainid == 1 && SEAT_COLLECTION.code.length > 0 && AGENT_ADAPTER.code.length > 0, "wrong chain")` before the broadcast. (From audit_flow 1b2a9499.)

**Reproduction**

In a Foundry test (chainid 31337, 0x0000eC93...1D has no code) set HIVE_REWARD_SINK, HIVE_TIMELOCK_PROPOSER, HIVE_TIMELOCK_GUARDIAN and call DeployHiveSeatVault.run(). Expected: refuse to deploy against a chain where the collection has no code. Actual: run() succeeds and returns a vault with seatCollection == 0x0000eC93...1D; vault.authorizeWorker({wallet: vault, tokenId: 1343, expiresAt: now+1h, ...}) from the owner then reverts inside seatCollection.ownerOf. Reproduced in test/scratch/JudgeRepro.t.sol::test_script_deploys_against_codeless_collection.

### 4. Info: Trust assumption not stated in the timelock header: a leaked proposer key can never be rotated out on-chain, only held in a stalemate by the guardian

`script/DeployHiveSeatVault.s.sol:27`

```
 *           cancel a queued operation (e.g. a hostile withdrawSeat or updateDelay from a leaked proposer key)
```

The header presents the guardian as the containment for a leaked proposer key. What it omits: the TimelockController constructor grants every proposer CANCELLER_ROLE as well, the script wires exactly one proposer, and every role change on the timelock (revokeRole/grantRole on PROPOSER_ROLE) and every vault ownership handover (transferOwnership to a fresh timelock) must be scheduled by that same proposer and survive 48h. Whoever holds the leaked key can cancel the team's rotation at any point in the window, while the guardian cancels the attacker's hostile operations. Seats are not stolen, but custody and configuration are frozen indefinitely: no withdrawSeat, no setSeatOperator (so a simultaneously leaked operator key cannot be retired), no setRewardSink, no handover, with no recovery that does not depend on the attacker stopping. This is a documentation/trust-assumption note, not a code defect, and the 48h design is out of scope. Suggested wording for the header: the proposer is also a canceller and the sole scheduler, so a leaked proposer key is unrecoverable on-chain and the guardian can only hold a stalemate; the proposer must be a multisig/HSM, never a hot key. (From audit_permissions be7cce03.)

**Reproduction**

State: TimelockController(48h, [P], [0], deployer); grantRole(CANCELLER_ROLE, G); renounce admin (the script's path). Team (as P) schedules target=timelock, data=revokeRole(PROPOSER_ROLE, P), salt='rot'. Attacker (as P, which holds CANCELLER_ROLE) calls cancel(id) before 48h. After warp +48h execute(...) reverts (TimelockUnexpectedOperationState) and hasRole(PROPOSER_ROLE, P) is still true; G calling schedule(...) reverts with AccessControlUnauthorizedAccount. Reproduced in test/scratch/JudgeRepro.t.sol::test_proposer_rotation_cancellable_by_leaked_key.

### 5. Info: Deploy script's post-deploy requires run only in simulation; an interrupted broadcast can leave the deployer with DEFAULT_ADMIN_ROLE on-chain

`script/DeployHiveSeatVault.s.sol:56`

```
            timelock.renounceRole(timelock.DEFAULT_ADMIN_ROLE(), deployer);
```

Item (8) asks to confirm the deployer ends with no DEFAULT_ADMIN_ROLE. In the simulated run that is true and asserted on line 76. On-chain, however, `forge script --broadcast` sends the constructor, grantRole, renounceRole and vault-creation as four separate transactions after a single simulation; the require statements are never re-evaluated against chain state. If the broadcast stops after grantRole (RPC failure, nonce gap, out-of-gas on a later tx) the deployer keeps DEFAULT_ADMIN_ROLE and can grant PROPOSER_ROLE/EXECUTOR_ROLE or change role admins instantly, with no 48h delay, until it renounces. No vault actor can exploit this without the deployer key, and resuming the broadcast completes the renounce, so it is an operational note: verify `hasRole(DEFAULT_ADMIN_ROLE, deployer) == false` from an independent read after the broadcast is confirmed, and treat the deployer key as privileged until then.

**Reproduction**

Execute the script's first two on-chain steps and stop: new TimelockController(48h, [P], [0], deployer); grantRole(CANCELLER_ROLE, G). Expected per the header ('No outside admin is left behind'): deployer has no admin. Actual: hasRole(DEFAULT_ADMIN_ROLE, deployer) == true and deployer.grantRole(PROPOSER_ROLE, anyone) succeeds with no delay. Reproduced in test/scratch/JudgeRepro.t.sol::test_interrupted_broadcast_leaves_deployer_admin.

### 6. Info: isValidSignature reverts instead of returning 0xffffffff when a paired seat no longer exists in the collection

`src/HiveSeatVault.sol:281`

```
        if (seatCollection.ownerOf(p.tokenId) != address(this)) return ERC1271_INVALID; // not held
```

The NatSpec on lines 273-274 and invariants I4/I8 describe isValidSignature as returning INVALID whenever the seat is not held. The custodyEpoch check on line 280 only covers a seat that left through withdrawSeat. If the token ceases to exist collection-side (burn, admin reclaim) while a live pairing exists, custodyEpoch is unchanged and control reaches line 281, where an OpenZeppelin-style ownerOf reverts with ERC721NonexistentToken, so the view reverts instead of returning the ERC-1271 failure value; authorizedTokenId (line 288) keeps reporting authorized == true for that digest. No custody or signing impact: a revert is never the magic value, and the seat is already gone. Whether the live identity.md collection has any burn/reclaim path could not be checked offline. Fix if desired: wrap the ownerOf read in try/catch (or staticcall + decode) and return ERC1271_INVALID on failure. (Merged from audit_permissions 19de3012 and audit_flow e8aae48b.)

**Reproduction**

Vault holds seat 1; operator calls authorizeWorker({wallet: vault, tokenId: 1, expiresAt: now+1h, ...}) -> digest d; isValidSignature(d, '') == 0x1626ba7e. The collection burns token 1 (no vault call). Expected: isValidSignature(d, '') returns 0xffffffff. Actual: reverts with ERC721NonexistentToken(1); authorizedTokenId(d) still returns (true, 1). Reproduced in test/scratch/JudgeRepro.t.sol::test_isValidSignature_reverts_when_burned with an OZ ERC721 mock exposing _burn.

### 7. Info: Trust assumptions: nothing in the vault pins the owner to a timelock, and the owner can route ERC-20s past rewardSink

`src/HiveSeatVault.sol:364`

```
    function _transferOwnership(address newOwner) internal override {
```

Documented as privileged powers, not bypasses; all are onlyOwner and so 48h-delayed and public while the owner is the TimelockController. (a) transferOwnership + acceptOwnership (Ownable2Step) can hand the vault to any address, including an EOA or a 0-delay timelock; from acceptance onward withdrawSeat, setSeatOperator, setRewardSink, routeERC20, rescueERC721 and setAgentURIById execute instantly. The deploy script asserts owner == timelock only at deployment (line 74); the vault itself has no check. (b) routeERC20 (line 380) sends any non-seat ERC-20 to a caller-supplied destination, so 'earnings go only to rewardSink' holds for permissionless callers only, not for the owner; I1 and I5 are preserved (the seat collection is rejected on line 381 and ERC-721 has no transfer(address,uint256)). (c) setRewardSink retargets all future sweeps; no in-flight value, so no retroactive loss. None is a defect under the stated model; they define the watch-list for queued timelock operations: transferOwnership(...) to a non-timelock target, routeERC20(...) to an unexpected destination, and any op whose target is the timelock itself. (From audit_permissions b2b27044.)

**Reproduction**

Owner = Timelock schedules vault.transferOwnership(0xEOA); after 48h it executes; 0xEOA calls acceptOwnership() (no delay). 0xEOA then calls withdrawSeat(1, 0xEOA) and the seat leaves in the same block with no queued operation. Likewise the owner's routeERC20(token, 0xAnyone, 100) moves 100 tokens to 0xAnyone instead of rewardSink. Reproduced in test/scratch/JudgeRepro.t.sol::test_owner_powers_trust_assumptions and by the existing test_ownership_handover_retires_pairings / test_routeERC20_partial_amount_and_event.

### 8. Info: Leaked operator key can create pairings with an unbounded expiresAt; only the 48h operator rotation retires them

`src/HiveSeatVault.sol:194`

```
        if (auth.expiresAt <= block.timestamp) revert AuthorizationExpired();
```

Trust-assumption note already acknowledged by the I8 comment, recorded because item (3) asks to confirm a leaked operator key 'can at worst grief'. The operator can pair attacker-chosen deviceKey values and expiresAt is only required to be in the future, so type(uint64).max is accepted; such a pairing stays VALID until the owner rotates the operator (setSeatOperator bumps authEpoch), which is itself a 48h-delayed operation. On-chain this moves nothing: wallet must equal the vault, the pairing only makes isValidSignature return the magic value for that one WorkerAuthorization digest, the vault never approves a seat, and no vault function lets a paired device transfer anything. Whether a paired worker can divert value at the IMD relay layer is outside the vault and should be confirmed with IMD; if it cannot, 'never steal' holds and the exposure is roughly 48h of an attacker running the seats. A vault-side cap (e.g. expiresAt <= block.timestamp + 30 days) would bound it without changing the operator model. (From audit_flow af16882a.)

**Reproduction**

Operator calls authorizeWorker({deviceKey: attackerKey, wallet: vault, tokenId: 1, nonce: n, expiresAt: type(uint64).max, relayOrigin: 'https://api.imd.fun'}). Expected under a bounded-grief model: the pairing lapses on its own. Actual: isValidSignature(digest, '') == 0x1626ba7e after warp +50 years, until the timelock executes setSeatOperator to a different address. Reproduced in test/scratch/JudgeRepro.t.sol::test_operator_pairing_never_expires.

### 9. Info: withdrawSeat has no to != address(0) guard and relies on the third-party collection to reject a zero recipient

`src/HiveSeatVault.sol:334`

```
    function withdrawSeat(uint256 tokenId, address to) external onlyOwner {
```

routeERC20 (line 382) and setRewardSink (line 350) revert on a zero destination, but withdrawSeat, the only seat exit, does not validate `to`. With an OpenZeppelin-style ERC-721 the collection reverts (ERC721InvalidReceiver(address(0))), so nothing is lost on the mocks; the live identity.md collection's transfer-to-zero behaviour is not exercised by any test here. If that collection treats a transfer to address(0) as a burn, a queued withdrawSeat(tokenId, address(0)) that nobody cancels within 48h destroys the seat. Owner-side mistake path, mitigated by the public 48h queue; recorded because the zero-check is applied asymmetrically. Fix: `if (to == address(0)) revert ZeroAddress();`. (From audit_flow a9099fe0.)

**Reproduction**

Owner calls vault.withdrawSeat(1, address(0)). Expected: ZeroAddress() from the vault, consistent with routeERC20/setRewardSink. Actual: the vault forwards seatCollection.safeTransferFrom(vault, address(0), 1) unguarded; on the OZ mock it reverts with ERC721InvalidReceiver(address(0)) (test/scratch/JudgeRepro.t.sol::test_withdrawSeat_zero_relies_on_collection); on the live collection the outcome depends on its implementation.

### 10. Info: Flow gap: the vault can only receive ERC-721 seats; ERC-1155 or safe-transferred non-seat ERC-721 rewards revert at the sender

`src/HiveSeatVault.sol:177`

```
        if (msg.sender != address(seatCollection)) revert NotSeatCollection();
```

Inbound value paths: ETH via receive, ERC-20 freely, seats via safeTransferFrom/transferFrom, non-seat ERC-721 only via unsafe transferFrom. Two inbound classes have no entry: ERC-1155 (no onERC1155Received, and ERC-1155 only has safe transfers) and any non-seat ERC-721 sent with safeTransferFrom (rejected on line 177). Rejecting stray ERC-721s is intentional per the NatSpec, and no inspected IMD flow pushes such assets to seat wallets today, so this is informational. It matters only if IMD or a launch later distributes rewards to seat holders as ERC-1155 or via safeMint/safeTransfer: that distribution transaction would revert for the vault's seats and the reward would be missed. If such a flow appears, add ERC1155Holder plus an owner-only rescue mirroring rescueERC721. (From audit_economics a941c16e.)

**Reproduction**

Any ERC-1155 calls safeTransferFrom(sender, vault, id, 1, '') -> reverts (ERC1155InvalidReceiver, no hook). Any non-seat ERC-721 calls safeTransferFrom(sender, vault, id) -> reverts with NotSeatCollection. Expected for a reward delivery: accepted and later sweepable/rescuable. Reproduced in test/scratch/JudgeRepro.t.sol::test_erc1155_and_foreign_safe721_rejected and the existing test_rejects_foreign_collection.

---

Judge's submission `3e3434159e8f21f82b51d603eb8d4885e2456354f9b308a63dd268d78a4250c9`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
