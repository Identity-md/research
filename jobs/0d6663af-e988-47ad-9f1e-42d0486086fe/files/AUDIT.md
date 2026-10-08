# Audit report

> Audit the HiveSeatVault contract in src/HiveSeatVault.sol: a non-upgradeable custody vault holding Project Hive's identity.md seat NFTs (ERC-721 collection 0x0000eC93127BAA929E58E97dd0095A2BFb38ec1D). The owner is a 48h OpenZeppelin TimelockController; a scoped seatOperator hot key may pair and run the seats but must never be able to move them. The ERC-1271 WorkerAuthorization pairing (authorizeWorker, revokeWorkerAuthorization, workerAuthorizationDigest, isValidSignature) is lifted verbatim from the audited IMDSeatStrategy so IMD accepts this contract as a seat's signer; the EIP-712 domain is 'IdentityMD Worker' version 2, bound to the seat collection. The security of the whole design rests on one property and it deserves the hardest look. (1) isValidSignature must return the ERC-1271 magic value ONLY for digests inserted by authorizeWorker, i.e. well-formed WorkerAuthorizations whose wallet equals address(this) and whose tokenId the vault owns. There must be NO path by which the seatOperator, a hot key that may be compromised, can cause isValidSignature to accept an arbitrary hash, in particular the hash of a Seaport order that would list or sell a seat. Confirm authorizeWorker only ever stores the EIP-712 digest it computes itself from a structured WorkerAuthorization, that an attacker-chosen digest cannot be inserted into the mapping, and that no Seaport or marketplace order hash can collide with a WorkerAuthorization digest. Then the custody invariants. (2) A seat NFT must leave the vault ONLY via withdrawSeat, which is onlyOwner (the Timelock): confirm there is no other path that transfers, approves (approve or setApprovalForAll), or lists a held seat, and that the vault never grants NFT approval to anyone. (3) The seatOperator's only powers are authorizeWorker, revokeWorkerAuthorization and registerAgent: confirm none of them can move value or a seat, and that a leaked operator key can at worst grief (stop pairing), never steal. (4) sweepEarnings must be unable to move a seat: it uses the ERC-20 interface, reverts if the token is the seat collection, and sends only to the fixed rewardSink. Confirm there is no caller-supplied destination and no way to reach the ERC-721 collection through it. (5) withdrawSeat, setSeatOperator, setRewardSink and setEnsName are all onlyOwner: confirm there is no privilege-escalation or reentrancy path around the Timelock, and that onERC721Received cannot be abused to brick the vault or spoof an approval. (6) The contract is non-upgradeable with no delegatecall and no selfdestruct: confirm the rules cannot change silently. Also assess reentrancy on registerAgent (external adapter call) and sweepEarnings (token transfers), and whether a hostile ERC-20 passed to sweepEarnings can do anything beyond reverting its own sweep. Report findings rather than fixing them. Do not propose changes to the 48h timelock design, the operator model, or the economics.

| | |
|---|---|
| Repository | https://github.com/ProjectHive-IMD/hive-seat-vault.git |
| Commit | `e0f79b7c4c8f018767a385fb05cb3c652bd5178b` |
| Job | `0d6663af-e988-47ad-9f1e-42d0486086fe` |
| Judged | 2026-10-08 20:18 UTC |
| Findings | 2 low · 5 info |

Four agents audited the code as it is at `e0f79b7`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: registerAgent/setAgentURI key one agentId per seat: the owner's documented remedies orphan a poisoned agent and cannot reach pre-deposit registrations

`src/HiveSeatVault.sol:222`

```
        agentIdOf[tokenId] = agentId;
```

agentIdOf[tokenId] is a single slot that registerAgent (line 222) unconditionally overwrites and that setAgentURI (line 229) is the only reader of. The NatSpec at lines 210-211 and 226-227 gives the Timelock two remedies against a leaked operator key that registered a seat with a poison URI: 'force a re-registration' or 'correct the URI via setAgentURI'. The live Adapter8004 (proxy 0xde152AfB7db5373F34876E1499fbD893A82dD336) accepts a second register() for the same (collection, tokenId) and mints a second ERC-8004 agent bound to the same seat, and its setAgentURI is gated only on collection.ownerOf(tokenId) == msg.sender, i.e. the vault is the one account allowed to edit ANY agent bound to a custodied seat. Consequences: (A) if the owner takes the re-register remedy, agentIdOf now points at the new agent and the earlier agent keeps the operator's poison URI in the public registry, bound to a Hive seat, with no vault function able to reach it even though the adapter would permit the call; (B) a seat whose previous holder registered it before depositing has agentIdOf == 0, so setAgentURI reverts NotRegistered for the pre-existing agent while the operator's once-per-seat registerAgent mints a duplicate agent for it instead of reusing the first. Neither case moves a seat or any value; the harm is a persistent attacker-chosen agentURI attributed to a vaulted seat, repairable only by withdrawing the seat through the 48h Timelock. Merged from three specialist reports (audit_math, audit_flow, audit_economics) describing the same slot design. Minimal fix that keeps the design and the existing ABI: record every agentId the vault registers per seat (e.g. mapping(uint256 => uint256[])) and have the owner-only setAgentURI(tokenId, uri) update all of them, or have the owner's forced re-register first correct/retire the previous agent; an alternative is an owner-only setAgentURI(agentId, uri) that defers authorization to the adapter's holder check, which already restricts it to the vault.

**Reproduction**

Unit (mock mirrors the live adapter: duplicates allowed, setAgentURI gated on seat holder): vault holds seat 1343, operator = leaked key. (1) vm.prank(operator); registerAgent(1343, 'ipfs://poison') -> agent A, agentIdOf[1343] = A. (2) vm.prank(timelock); registerAgent(1343, 'ipfs://owner') -> agent B, agentIdOf[1343] = B. (3) vm.prank(timelock); setAgentURI(1343, 'ipfs://good'). Expected: every agent the vault created for seat 1343 carries the corrected URI. Actual: adapter.uriOf(B) == 'ipfs://good' but adapter.uriOf(A) == 'ipfs://poison' and no vault function can change A, while a direct adapter.setAgentURI(A, ...) with msg.sender == vault succeeds. Variant: treasury registers seat 2000 itself (agent A), deposits it; vm.prank(timelock); setAgentURI(2000, ...) reverts NotRegistered(); vm.prank(operator); registerAgent(2000, 'ipfs://poison') succeeds and binds a duplicate agent C != A. Live confirmation on a mainnet fork at 2026-10-08: registering seat 1343 twice through the vault against the real adapter returned agentIds 52475 then 52476; the vault (as holder) could call adapter.setAgentURI(52475, ...) directly, a stranger's call reverted, and vault.setAgentURI(1343, ...) only reached 52476. The attached proof fails on the current code with 'first agent still carries the poison URI and is unreachable: ipfs://poison != ipfs://good'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {HiveSeatVault, IImdAgentAdapter, IEnsReverseRegistrar} from "src/HiveSeatVault.sol";
import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SeatMock is ERC721 {
    constructor() ERC721("identity.md", "IDMD") {}
    function mint(address to, uint256 id) external { _mint(to, id); }
}

/// Mirrors the live Adapter8004: duplicate registrations for the same seat are allowed (verified on a
/// mainnet fork: ids 52474 and 52475 were both created for seat 1343), setAgentURI is gated on the seat owner.
contract AdapterMock is IImdAgentAdapter {
    IERC721 public immutable seat;
    uint256 public n = 52473;
    mapping(uint256 => string) public uriOf;
    mapping(uint256 => uint256) public seatOf;
    constructor(IERC721 s) { seat = s; }
    function register(uint8, address, uint256 tokenId, string calldata uri) external returns (uint256) {
        require(seat.ownerOf(tokenId) == msg.sender, "not seat owner");
        uriOf[++n] = uri;
        seatOf[n] = tokenId;
        return n;
    }
    function setAgentURI(uint256 agentId, string calldata uri) external {
        require(seat.ownerOf(seatOf[agentId]) == msg.sender, "not seat owner");
        uriOf[agentId] = uri;
    }
}

contract OrphanProofTest is Test {
    HiveSeatVault vault;
    SeatMock seat;
    AdapterMock adapter;
    address timelock = makeAddr("timelock");
    address operator = makeAddr("operator");
    uint256 constant SEAT_ID = 1343;

    function setUp() public {
        vm.warp(1_700_000_000);
        seat = new SeatMock();
        adapter = new AdapterMock(IERC721(address(seat)));
        vault = new HiveSeatVault(timelock, IERC721(address(seat)), adapter, IEnsReverseRegistrar(address(0)), makeAddr("sink"));
        vm.prank(timelock);
        vault.setSeatOperator(operator);
        seat.mint(address(vault), SEAT_ID);
    }

    /// A leaked operator key registers agent #52474 with a poison URI. The owner (Timelock) uses the documented
    /// remedy "force a re-registration", which creates #52475 and overwrites agentIdOf. The owner's only URI
    /// correction path, setAgentURI(tokenId, ...), now reaches #52475 only. #52474 stays bound to the seat in
    /// the registry with the poison URI, and the vault (the seat's owner, the only account the adapter accepts)
    /// has no function that can reach it. Expected: the owner can correct every agent the vault created for the
    /// seat. Actual: the first one is unreachable.
    function test_owner_can_correct_every_agent_the_vault_created() public {
        vm.prank(operator);
        uint256 id1 = vault.registerAgent(SEAT_ID, "ipfs://poison");
        vm.prank(timelock);
        uint256 id2 = vault.registerAgent(SEAT_ID, "ipfs://owner");
        assertEq(vault.agentIdOf(SEAT_ID), id2);
        vm.prank(timelock);
        vault.setAgentURI(SEAT_ID, "ipfs://good");
        assertEq(adapter.uriOf(id2), "ipfs://good");
        assertEq(adapter.uriOf(id1), "ipfs://good", "first agent still carries the poison URI and is unreachable");
    }
}
```

### 2. Low: Pairings inserted by a previous owner survive transferOwnership/acceptOwnership (authEpoch only bumps on an operator change)

`src/HiveSeatVault.sol:144`

```
        if (msg.sender != seatOperator && msg.sender != owner()) revert NotSeatOperator();
```

onlySeatOperator admits owner() as a second pairing key, so the Timelock can call authorizeWorker. The clean-slate mechanism (authEpoch, line 328) fires only inside setSeatOperator when the operator address changes. The inherited Ownable2Step transferOwnership/acceptOwnership path never touches authEpoch, so every pairing the OLD owner inserted stays VALID under the NEW owner for as long as its operator-chosen expiresAt (up to type(uint64).max). I8 describes a key change as retiring every live pairing; an owner handover is a key change that does not. This is a documentation/invariant gap, not a theft path: a pairing can never move a seat. Correction to the specialist's text: the new owner is NOT limited to rotating the operator to retire them; revokeWorkerAuthorization(digest) is available to the owner per digest (digests are emitted in WorkerAuthorized), so the gap is that the retirement is manual rather than automatic. Minimal fix if wanted: bump authEpoch in an override of _transferOwnership (or acceptOwnership), or document that owner-made pairings are not retired by an ownership handover.

**Reproduction**

State: owner = timelockA, vault holds seat 1343. (1) vm.prank(timelockA); authorizeWorker({wallet: vault, tokenId: 1343, expiresAt: type(uint64).max, ...}) -> digest D; isValidSignature(D, '') == 0x1626ba7e. (2) vm.prank(timelockA); transferOwnership(timelockB); vm.prank(timelockB); acceptOwnership(); owner() == timelockB. (3) isValidSignature(D, '') is still 0x1626ba7e (authEpoch unchanged, custodyEpoch unchanged, seat still held). Expected per I8's clean-slate wording: a change of a pairing key retires the pairings it made. Actual: D stays valid until timelockB calls revokeWorkerAuthorization(D) (verified to return 0xffffffff afterwards) or setSeatOperator with a new address. Reproduced in a scratch test (test_owner_pairings_survive_ownership_transfer).

### 3. Info: Nothing in the code binds owner_ to a 48h TimelockController: every custody delay is a deployment-time assumption

`src/HiveSeatVault.sol:149`

```
        address owner_, // the TimelockController
```

All custody guarantees (I1, I5, I6, I8's rotation remedy) reduce to 'onlyOwner is a 48h public delay', but the constructor only requires owner_ to be non-zero (Ownable). It does not check that owner_ has code, is a TimelockController, has getMinDelay() >= 48h, or that the timelock's admin role has been renounced (an un-renounced admin can call updateDelay(0) and then schedule+execute withdrawSeat in one block). The repository ships no deployment script, no post-deploy assertion and no test exercising a real TimelockController: every test pranks an EOA named 'timelock'. The same applies to the two-step hand-off: transferOwnership + acceptOwnership can move ownership to any address the current timelock approves, after which all owner powers are instant. Not a code defect and not a request to change the timelock design; recorded as an open deployment item and trust assumption. Suggested closure: a deploy script that deploys TimelockController(minDelay = 48h, proposers, executors, admin = address(0)) and passes it as owner_, plus an integration test asserting schedule -> execute(withdrawSeat) reverts before 48h and succeeds after.

**Reproduction**

new HiveSeatVault(owner_ = any EOA, seatCollection, adapter, ens, sink); deposit seat 1343. Expected per README/I1: a seat exit is queued publicly >= 48h ahead. Actual: vm.prank(owner_); vault.withdrawSeat(1343, anywhere) succeeds in the same block and seat.ownerOf(1343) == anywhere (scratch test test_eoa_owner_withdraws_instantly; the shipped test_owner_withdraws does the same with an EOA).

### 4. Info: agentAdapter is an IMD-owned UUPS proxy: its rules can change without the Timelock, bounded to reverting/junk registrations, never a seat

`src/HiveSeatVault.sol:88`

```
    IImdAgentAdapter public immutable agentAdapter; // ERC-8004 registration
```

The vault itself is non-upgradeable (I7 verified: no delegatecall, no selfdestruct, no proxy, immutables only), but the live Adapter8004 it binds to (0xde152AfB7db5373F34876E1499fbD893A82dD336, from IMDSeatStrategy.IMD_AGENT_ADAPTER()) is an ERC-1967 proxy whose implementation slot holds 0xa6d23f27d3b1780b12488482a008cb3c3787135f; that implementation exposes upgradeToAndCall (0x4f1ef286) and proxiableUUID (0x52d1902d) and owner() returns 0x03302Df40186D9B85faEA4fbb6cC5da028B23149. An implementation change by IMD alters what registerAgent and setAgentURI do without any Timelock action. Verified damage bound: the adapter is called with msg.sender == vault only from registerAgent (nonReentrant) and setAgentURI (onlyOwner); a hostile implementation can revert, burn gas, register junk, or call back into the vault, but every state-changing re-entry target is onlyOwner, onlySeatOperator, gated by the shared ReentrancyGuard (sweepEarnings, sweepETH, registerAgent), or restricted to msg.sender == seatCollection (onERC721Received). The vault never grants ERC-721 approval to the adapter (isApprovedForAll(vault, adapter) == false and getApproved(seat) == 0 after a live registration), so no upgrade can transfer, approve or list a seat or insert a pairing digest. Merged from audit_flow and audit_permissions. Trust assumption, no change to the vault required.

**Reproduction**

On mainnet: cast storage 0xde152AfB7db5373F34876E1499fbD893A82dD336 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc -> 0x...a6d23f27d3b1780b12488482a008cb3c3787135f (non-zero: upgradeable proxy); the implementation bytecode contains selectors 4f1ef286 and 52d1902d. Expected per I7 wording ('the rules cannot change silently'): every code path the vault depends on is frozen; actual: the registration path is upgradeable by IMD. Bound confirmed by a scratch test in which a hostile callee attempts, during a vault call, sweepEarnings, sweepETH, registerAgent, withdrawSeat, setSeatOperator, onERC721Received, authorizeWorker and seat.transferFrom(vault, ...): all 8 revert and seat.ownerOf(1343) stays the vault with no approval set.

### 5. Info: sweepEarnings emits Swept for any caller-supplied contract that answers balanceOf/transfer, so the event can be forged; a hostile token can do nothing else

`src/HiveSeatVault.sol:295`

```
                emit Swept(token, bal, sink);
```

sweepEarnings is permissionless and takes an arbitrary token list; the only exclusion is the seat collection. For a hostile contract the vault reads balanceOf via STATICCALL (attacker-chosen return) and then calls transfer via SafeERC20, which only requires the call not to revert and to return true or nothing. The vault then emits Swept(token, bal, rewardSink) with the attacker-chosen amount although nothing moved; the amount is also the pre-transfer balance, so fee-on-transfer or rebasing tokens over-report. This answers the brief's 'hostile ERC-20' question: during its transfer callback the token cannot re-enter sweepEarnings/sweepETH/registerAgent (shared nonReentrant), cannot call authorizeWorker/revokeWorkerAuthorization/withdrawSeat/setSeatOperator (role-gated), cannot reach onERC721Received (msg.sender must be the seat collection), and cannot move the seat because its msg.sender toward the collection is the token, not the vault, and the vault holds no approvals. The seat collection cannot be reached through sweepEarnings (exact address check; the collection has no transfer(address,uint256)). Impact is limited to off-chain consumers that index Swept without an allow-list. Merged from audit_permissions and audit_math. Mitigation if desired: consumers verify Swept against the token's own Transfer event, or an owner-maintained token allow-list (a design change, not required).

**Reproduction**

Deploy EvilToken with balanceOf(address) returning 1e24 and transfer(address,uint256) returning true without moving anything. vm.prank(anyone); vault.sweepEarnings([evil]). Expected: no Swept event for a token that paid nothing. Actual: the vault emits Swept(evil, 1e24, rewardSink) (vm.expectEmit on the vault passes). In the same transaction the token's transfer attempts all 8 re-entries/seat moves listed above: all revert (counter == 8), seat.ownerOf(1343) == vault, getApproved(1343) == 0, isApprovedForAll(vault, evil) == false. Scratch test test_hostile_token_forges_Swept_but_nothing_else.

### 6. Info: Open deposits let the operator pair and register any third-party seat sent to the vault, with no self-service exit for the depositor

`src/HiveSeatVault.sol:173`

```
        if (msg.sender != address(seatCollection)) revert NotSeatCollection();
```

onERC721Received accepts every token of the collection from any sender, and authorizeWorker/registerAgent gate only on ownerOf(tokenId) == address(this), not on a per-seat allow-list. A seat that an unrelated holder sends to the vault (by mistake) is immediately pairable and registerable by the seatOperator hot key and can leave only through a 48h Timelock withdrawSeat naming the sender (rescueERC721 refuses the seat collection). The vault itself is unharmed and the seat is custodied under the same rules as Hive's own seats; the deposit requires the holder's own safeTransferFrom, so it cannot be forced on them. Listed because the brief asks what a leaked operator key can reach: 'run a stranger's mistakenly deposited seat until the Timelock returns it' is within its reach. Open deposits are a stated design choice; no change is required beyond documenting it for depositors. Downgraded from the specialist's low to info for that reason.

**Reproduction**

State: vault holds Hive seat 1343; seatOperator = op. (1) Unrelated holder X calls seatCollection.safeTransferFrom(X, vault, 777): accepted. (2) vm.prank(op); authorizeWorker({wallet: vault, tokenId: 777, expiresAt: now + 10 days, ...}) -> isValidSignature == 0x1626ba7e; vm.prank(op); registerAgent(777, 'ipfs://poison') succeeds. (3) vm.prank(X); withdrawSeat(777, X) reverts (onlyOwner); vm.prank(timelock); rescueERC721(seat, 777, X) reverts CannotRescueSeats; only vm.prank(timelock); withdrawSeat(777, X) returns it. Scratch test test_third_party_seat_pairable_by_operator.

### 7. Info: setEnsName reverts with empty revert data when ensReverseRegistrar was deployed as address(0)

`src/HiveSeatVault.sol:357`

```
        return ensReverseRegistrar.setName(name);
```

The constructor explicitly permits ensReverseRegistrar == address(0) ('may be address(0) off-mainnet', line 89), but setEnsName performs a high-level call expecting a bytes32 return. Since solc 0.8.10 the extcodesize check is skipped when return data is expected, so the call to the empty account returns no data and ABI decoding reverts with no reason. A Timelock proposal would fail after its 48h delay with an opaque revert. Cosmetic, owner-only, no security impact. Minimal fix: revert with a named error when address(ensReverseRegistrar) == address(0), or disallow zero in the constructor.

**Reproduction**

new HiveSeatVault(timelock, seat, adapter, IEnsReverseRegistrar(address(0)), sink); vm.prank(timelock); address(vault).call(abi.encodeWithSelector(vault.setEnsName.selector, 'hive.eth')). Expected: a clear revert (or no-op) when ENS is not configured. Actual: ok == false and returndata.length == 0 (scratch test test_setEnsName_zero_registrar_reverts_empty).

---

Judge's submission `a4234ea776329f76f27067f5b51a4fe198b7b6f21530fe8af46b549f32b4b355`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
