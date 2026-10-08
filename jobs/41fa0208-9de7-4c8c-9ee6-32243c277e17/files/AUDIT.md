# Audit report

> Audit the HiveSeatVault contract in src/HiveSeatVault.sol: a non-upgradeable custody vault holding Project Hive's identity.md seat NFTs (ERC-721 collection 0x0000eC93127BAA929E58E97dd0095A2BFb38ec1D). The owner is a 48h OpenZeppelin TimelockController; a scoped seatOperator hot key may pair and run the seats but must never be able to move them. The ERC-1271 WorkerAuthorization pairing (authorizeWorker, revokeWorkerAuthorization, workerAuthorizationDigest, isValidSignature) is lifted verbatim from the audited IMDSeatStrategy so IMD accepts this contract as a seat's signer; the EIP-712 domain is 'IdentityMD Worker' version 2, bound to the seat collection. The security of the whole design rests on one property and it deserves the hardest look. (1) isValidSignature must return the ERC-1271 magic value ONLY for digests inserted by authorizeWorker, i.e. well-formed WorkerAuthorizations whose wallet equals address(this) and whose tokenId the vault owns. There must be NO path by which the seatOperator, a hot key that may be compromised, can cause isValidSignature to accept an arbitrary hash, in particular the hash of a Seaport order that would list or sell a seat. Confirm authorizeWorker only ever stores the EIP-712 digest it computes itself from a structured WorkerAuthorization, that an attacker-chosen digest cannot be inserted into the mapping, and that no Seaport or marketplace order hash can collide with a WorkerAuthorization digest. Then the custody invariants. (2) A seat NFT must leave the vault ONLY via withdrawSeat, which is onlyOwner (the Timelock): confirm there is no other path that transfers, approves (approve or setApprovalForAll), or lists a held seat, and that the vault never grants NFT approval to anyone. (3) The seatOperator's only powers are authorizeWorker, revokeWorkerAuthorization and registerAgent: confirm none of them can move value or a seat, and that a leaked operator key can at worst grief (stop pairing), never steal. (4) sweepEarnings must be unable to move a seat: it uses the ERC-20 interface, reverts if the token is the seat collection, and sends only to the fixed rewardSink. Confirm there is no caller-supplied destination and no way to reach the ERC-721 collection through it. (5) withdrawSeat, setSeatOperator, setRewardSink and setEnsName are all onlyOwner: confirm there is no privilege-escalation or reentrancy path around the Timelock, and that onERC721Received cannot be abused to brick the vault or spoof an approval. (6) The contract is non-upgradeable with no delegatecall and no selfdestruct: confirm the rules cannot change silently. Also assess reentrancy on registerAgent (external adapter call) and sweepEarnings (token transfers), and whether a hostile ERC-20 passed to sweepEarnings can do anything beyond reverting its own sweep. Report findings rather than fixing them. Do not propose changes to the 48h timelock design, the operator model, or the economics.

| | |
|---|---|
| Repository | https://github.com/ProjectHive-IMD/hive-seat-vault.git |
| Commit | `c00246ba84db8289a4b18fa1c047b6fd926899dd` |
| Job | `41fa0208-9de7-4c8c-9ee6-32243c277e17` |
| Judged | 2026-10-08 20:45 UTC |
| Findings | 1 medium · 1 low · 5 info |

Four agents audited the code as it is at `c00246b`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: sweepEarnings cannot move IMD launch tokens (BaseStrategy ERC-20s revert InvalidTransfer on a plain transfer to rewardSink), so launch-token earnings are stuck in the vault

`src/HiveSeatVault.sol:305`

```
IERC20(token).safeTransfer(sink, bal);
```

The NatSpec (line 296) says sweepEarnings pushes 'IMD + launch tokens' to rewardSink. The live launch token (IMDSeatStrategy proxy 0x0000198C940D8cD70Cb9ACeC5E3af8216ac57d2F) only allows transfers that involve the v4 poolManager or a registered distributor/router, and reverts with InvalidTransfer() (0x2f352531) on any other transfer. A sweep to a treasury, multisig or EOA sink therefore always reverts for the whole balance. The vault has no partial sweep, no way to route through a distributor, and no owner-level ERC-20 exit. Pointing setRewardSink at a third-party router is the only address-level workaround, and it would hand the tokens to that router. So any launch-token balance a distributor pays to the vault is stranded. The mainnet IMD token (0xD34a99Bc0f67aE1bbd63C660e6d0b0dd03E263B7) is not restricted and sweeps correctly, so only launch tokens are affected. Fixing it is a scope decision for the requester, for example a timelocked owner-only ERC-20 exit that can route to a distributor, or routing launch-token sweeps through a whitelisted distributor. Merged from audit_math.

**Reproduction**

Mainnet fork (https://ethereum-rpc.publicnode.com, 2026-10-08). Deploy HiveSeatVault(owner, 0x0000eC93127BAA929E58E97dd0095A2BFb38ec1D, 0xde152AfB7db5373F34876E1499fbD893A82dD336, address(0), sink=makeAddr("sink")). deal(0x0000198C...d2F, vault, 1000e18) and deal(IMD 0xD34a...B7, vault, 1000e18). sweepEarnings([IMD]) succeeds and the sink receives 1000e18. Expected: sweepEarnings([0x0000198C...d2F]) moves 1000e18 to the sink. Actual: it reverts with 0x2f352531 (InvalidTransfer) and the vault still holds 1000e18. A plain EOA-to-EOA transfer of the same token also reverts, so the restriction is the token's, and the vault offers no route around it. Run as test/scratch/Fork.t.sol.

### 2. Low: Deploy script claims nobody can shorten the timelock delay or re-grant roles; the OZ TimelockController administers itself, so the proposer can set the delay to 0 after one 48h wait and then withdraw

`script/DeployHiveSeatVault.s.sol:18`

```
 *         - admin = address(0): no one can shorten the delay or re-grant roles after deploy.
```

OpenZeppelin v5 TimelockController's constructor always grants DEFAULT_ADMIN_ROLE to address(this), whatever admin is passed. updateDelay only requires msg.sender == address(this). So the proposer can schedule a self-call updateDelay(0) or grantRole(...), execute it once 48h have passed, and then schedule and execute withdrawSeat for every seat in the same block. The guarantee that every exit is visible 48h ahead becomes: only the first hostile operation is visible 48h ahead. This is documentation and trust-assumption only, with no timelock design change proposed. The fix is to correct the comment and to monitor any scheduled operation that targets the timelock itself as an exit signal. Related trust assumption: OZ grants CANCELLER_ROLE only to proposers, so with the script's single proposer, admin=0 and open execution, that one key is also the only account that can cancel. If it leaks, nobody else can stop a queued withdrawSeat. This merges the duplicate canceller findings from audit_economics and audit_flow.

**Reproduction**

Local test test/scratch/Local.t.sol::test_delay_can_be_zeroed. Build the timelock exactly as the script does: new TimelockController(48h, [P], [address(0)], address(0)). The vault is owned by it and holds seat 1343. P schedules (tl, updateDelay(0)), the test warps 48h, and anyone executes. Expected per the comment: impossible. Actual: getMinDelay()==0. P then schedules withdrawSeat(1343, P) with delay 0 and it executes in the same block: seat.ownerOf(1343)==P. The seat operator calling tl.cancel reverts, and hasRole(CANCELLER_ROLE, operator)==false. The test passes on the current code.

### 3. Info: Anyone can make the vault emit a fabricated Swept(token, amount, rewardSink) event using a fake ERC-20; this is the only effect a hostile token has

`src/HiveSeatVault.sol:306`

```
emit Swept(token, bal, sink);
```

The token list is supplied by the caller, and the vault trusts the token's own balanceOf and transfer return values. A contract that reports any balance and returns true from transfer() makes the vault emit Swept(fake, N, rewardSink) while nothing moves. Any indexer that treats Swept as an earnings ledger without filtering token addresses can be polluted. Nothing else is reachable. The destination is fixed. The seat collection is rejected before any call is made. Re-entry into sweepEarnings, sweepETH or registerAgent hits the shared nonReentrant guard, every other mutator is gated by onlyOwner or onlySeatOperator, and the vault holds no approvals. No contract change is needed; indexers should filter by known tokens. Merged from audit_math, audit_flow and audit_permissions.

**Reproduction**

test/scratch/Local.t.sol::test_swept_spoof. Fake{balanceOf->1e30; transfer->true}. vm.prank(0xBAD); vault.sweepEarnings([fake]). Expected: no earnings event. Actual: the vault emits Swept(fake, 1e30, sink) and no tokens move.

### 4. Info: Trust assumption: the 48h delay belongs to the owner, not the vault; after a handover to a non-timelock owner, withdrawSeat is instant

`src/HiveSeatVault.sol:359`

```
function _transferOwnership(address newOwner) internal override {
```

Nothing in the vault pins owner() to a timelock. The deploy script's require only checks the state at deployment. The timelock can schedule transferOwnership(newOwner); after the single 48h delay and acceptOwnership(), every onlyOwner function, including withdrawSeat, can be called with no further delay. This is the documented design (lines 350-351), and the handover itself is a public 48h operation, so the timelock is not bypassed. Reported as a trust assumption only. From audit_economics.

**Reproduction**

The timelock queues vault.transferOwnership(EOA); after 48h it executes, and the EOA calls acceptOwnership(). The EOA then calls withdrawSeat(1343, EOA) in the same block and seat.ownerOf(1343)==EOA. This follows directly from Ownable2Step plus onlyOwner on line 329.

### 5. Info: Trust assumption: the agent adapter is a UUPS proxy upgradeable by a third-party key, so what registerAgent and setAgentURI actually do is not frozen by the vault's own non-upgradeability

`src/HiveSeatVault.sol:223`

```
agentId = agentAdapter.register(0, address(seatCollection), tokenId, agentURI);
```

I7 holds for the vault itself: grep finds no delegatecall, selfdestruct, approve or setApprovalForAll calls. The immutable adapter 0xde152AfB... is an ERC-1967 proxy, though, and its owner 0x03302Df40186D9B85faEA4fbb6cC5da028B23149 is a 345-byte contract outside Hive's control. The damage is bounded. The vault never approves the adapter. registerAgent is nonReentrant. The adapter is neither owner nor operator. So a hostile upgrade can only make registration revert (a denial of service on the operator's third power) or return a bogus agentId. If it returns 0, agentIdOf stays 0 and the once-per-seat guard never engages. List this next to the timelock and operator as a dependency assumption. Merged from audit_flow and audit_permissions.

**Reproduction**

cast storage 0xde152AfB7db5373F34876E1499fbD893A82dD336 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc returns implementation 0xa6d23f27d3b1780b12488482a008cb3c3787135f, and cast call owner() returns 0x03302Df4...3149, which has 345 bytes of code (checked 2026-10-08). If that owner upgrades to an implementation whose register() reverts, vault.registerAgent(1343, uri) reverts for both operator and owner.

### 6. Info: Custodied seats and agents lose owner-gated controls the vault does not pass through (adapter setAgentWallet/setMetadata, collection setIdentityHash)

`src/HiveSeatVault.sol:20`

```
function setAgentURI(uint256 agentId, string calldata agentURI) external;
```

For held seats the vault is the ERC-721 owner and the adapter controller, but it only passes through register and setAgentURI. Nobody, including the timelock, can call the adapter's setAgentWallet or setMetadata, or the collection's setIdentityHash, for a custodied seat. The identity-hash part is latent today: identityAllowed()==false on mainnet, so the call reverts for everyone. No seat or value is at risk. This is a functional gap; adding owner-only passthroughs is a scope decision. Downgraded from low because no material impact was shown. From audit_permissions.

**Reproduction**

The source has no function that calls setAgentWallet, setMetadata or setIdentityHash. Every external call on the adapter is at lines 223, 233 and 242 (register and setAgentURI). cast call 0x0000eC93...1D identityAllowed() returns false (2026-10-08).

### 7. Info: Seats deposited with plain transferFrom emit no SeatDeposited event

`src/HiveSeatVault.sol:171`

```
function onERC721Received(address, address from, uint256 tokenId, bytes calldata)
```

SeatDeposited is emitted only from the safeTransfer hook. A seat sent with transferFrom is fully custodied: it can be paired and withdrawn, and the custody invariants are unaffected. But off-chain tooling that rebuilds the custody set from SeatDeposited will miss it. This is an observability gap only. From audit_economics.

**Reproduction**

test/scratch/Local.t.sol::test_transferFrom_no_event. A holder calls seat.transferFrom(holder, vault, 7) with vm.recordLogs. Expected: a SeatDeposited log. Actual: no log has topic0 == SeatDeposited.selector, and ownerOf(7)==vault.

---

Judge's submission `f188b9eadcba8d194c5b7460c610e47634d4566465433ba7bdcd88f835e8299c`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
