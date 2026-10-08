# Audit report

> Audit the HiveSeatVault contract in src/HiveSeatVault.sol: a non-upgradeable custody vault holding Project Hive's identity.md seat NFTs (ERC-721 collection 0x0000eC93127BAA929E58E97dd0095A2BFb38ec1D). The owner is a 48h OpenZeppelin TimelockController; a scoped seatOperator hot key may pair and run the seats but must never be able to move them. The ERC-1271 WorkerAuthorization pairing (authorizeWorker, revokeWorkerAuthorization, workerAuthorizationDigest, isValidSignature) is lifted verbatim from the audited IMDSeatStrategy so IMD accepts this contract as a seat's signer; the EIP-712 domain is 'IdentityMD Worker' version 2, bound to the seat collection. The security of the whole design rests on one property and it deserves the hardest look. (1) isValidSignature must return the ERC-1271 magic value ONLY for digests inserted by authorizeWorker, i.e. well-formed WorkerAuthorizations whose wallet equals address(this) and whose tokenId the vault owns. There must be NO path by which the seatOperator, a hot key that may be compromised, can cause isValidSignature to accept an arbitrary hash, in particular the hash of a Seaport order that would list or sell a seat. Confirm authorizeWorker only ever stores the EIP-712 digest it computes itself from a structured WorkerAuthorization, that an attacker-chosen digest cannot be inserted into the mapping, and that no Seaport or marketplace order hash can collide with a WorkerAuthorization digest. Then the custody invariants. (2) A seat NFT must leave the vault ONLY via withdrawSeat, which is onlyOwner (the Timelock): confirm there is no other path that transfers, approves (approve or setApprovalForAll), or lists a held seat, and that the vault never grants NFT approval to anyone. (3) The seatOperator's only powers are authorizeWorker, revokeWorkerAuthorization and registerAgent: confirm none of them can move value or a seat, and that a leaked operator key can at worst grief (stop pairing), never steal. (4) sweepEarnings must be unable to move a seat: it uses the ERC-20 interface, reverts if the token is the seat collection, and sends only to the fixed rewardSink. Confirm there is no caller-supplied destination and no way to reach the ERC-721 collection through it. (5) withdrawSeat, setSeatOperator, setRewardSink and setEnsName are all onlyOwner: confirm there is no privilege-escalation or reentrancy path around the Timelock, and that onERC721Received cannot be abused to brick the vault or spoof an approval. (6) The contract is non-upgradeable with no delegatecall and no selfdestruct: confirm the rules cannot change silently. Also assess reentrancy on registerAgent (external adapter call) and sweepEarnings (token transfers), and whether a hostile ERC-20 passed to sweepEarnings can do anything beyond reverting its own sweep. Report findings rather than fixing them. Do not propose changes to the 48h timelock design, the operator model, or the economics.

| | |
|---|---|
| Repository | https://github.com/ProjectHive-IMD/hive-seat-vault.git |
| Commit | `0a04c66441e9094a4800e52d5b49163e22df7fa0` |
| Job | `64e57ab9-b8f6-41c6-b384-89df340c91df` |
| Judged | 2026-10-08 18:49 UTC |
| Findings | 1 high · 3 low · 3 info |

Four agents audited the code as it is at `0a04c66`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: registerAgent is dead against the live IMD adapter: IImdAgentAdapter.register uses uint256 but the adapter's selector is register(uint8,...)

`src/HiveSeatVault.sol:14`

```
    function register(uint256 kind, address collection, uint256 tokenId, string calldata agentURI)
```

The vault's IImdAgentAdapter interface declares register(uint256,address,uint256,string), selector 0x1f354cc5. The live IMD adapter read from IMDSeatStrategy.IMD_AGENT_ADAPTER() (proxy 0xde152AfB7db5373F34876E1499fbD893A82dD336, EIP-1967 implementation 0xa6d23f27d3b1780b12488482a008cb3c3787135f, Sourcify-verified Adapter8004.sol line 104) declares register(TokenStandard standard, address tokenContract, uint256 tokenId, string agentURI); TokenStandard is an enum, ABI type uint8, so the real selector is 0xb68ca002. The implementation bytecode contains 0xb68ca002 once and 0x1f354cc5 nowhere, and the adapter has no fallback, so every HiveSeatVault.registerAgent call reverts with empty return data. Because agentAdapter is immutable and the ABI is compiled into the bytecode, this deployment can never register an agent: one of the operator's three documented powers (invariant I3, 'needed once for a never-registered seat') does not exist, and a never-registered seat deposited into the vault cannot be registered until it is withdrawn through the 48h timelock, registered elsewhere, and redeposited. Neither the unit MockAdapter (which implements the vault's wrong signature) nor the fork suite (which never calls registerAgent) can catch it. No seat or token is at risk. Fix: declare the first parameter as uint8 (the reference IMDSeatStrategy's IIMDAgentAdapter does); the call site already passes the literal 0. Merged from audit_math (high) and audit_flow (medium).

**Reproduction**

Mainnet fork at block ~26149550 (test/scratch/JudgeFork.t.sol): deploy the vault with agentAdapter = IMDSeatStrategy(0x0000198C940D8cD70Cb9ACeC5E3af8216ac57d2F).IMD_AGENT_ADAPTER() = 0xde152AfB7db5373F34876E1499fbD893A82dD336, move seat 1343 from the treasury 0x84b31CB3D205EfD2d20F29eA7ccaB1bc34326DdB into the vault, set seatOperator. Input: operator calls vault.registerAgent(1343, "ipfs://agent"). Expected: returns a new agentId and emits AgentRegistered. Actual: the call returns ok=false with empty revert data. From the vault's own address, a raw call with signature register(uint8,address,uint256,string) and the same arguments succeeds and returns agentId 52468 (0xccf4); a raw call with register(uint256,address,uint256,string) reverts empty. `cast sig 'register(uint256,address,uint256,string)'` = 0x1f354cc5, `cast sig 'register(uint8,address,uint256,string)'` = 0xb68ca002; `cast code 0xa6d23f27d3b1780b12488482a008cb3c3787135f` contains b68ca002 and not 1f354cc5. Offline proof below: a mock exposing the live ABI; `forge test --match-path test/scratch/Proof_74c584344c3b.t.sol` fails with EvmError: Revert on the current code and passes after changing `uint256 kind` to `uint8 kind` on line 14 (verified both ways).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {Test} from "forge-std/Test.sol";
import {HiveSeatVault, IImdAgentAdapter, IEnsReverseRegistrar} from "src/HiveSeatVault.sol";
import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract MockSeat is ERC721 {
    constructor() ERC721("identity.md", "IDMD") {}
    function mint(address to, uint256 id) external { _mint(to, id); }
}

/// @dev Mirrors the ABI of IMD's live Adapter8004 (proxy 0xde152AfB7db5373F34876E1499fbD893A82dD336,
///      impl 0xa6d23f27d3b1780b12488482a008cb3c3787135f) and of the reference IMDSeatStrategy's
///      IIMDAgentAdapter: `register(uint8 standard, address tokenContract, uint256 tokenId, string agentURI)`.
///      TokenStandard is an enum, so the first parameter is ABI type uint8 and the selector is 0xb68ca002.
///      Like the live contract it has no fallback, so an unknown selector reverts.
contract RealAbiAdapter {
    uint256 public last;
    function register(uint8 standard, address tokenContract, uint256 tokenId, string calldata)
        external
        returns (uint256 agentId)
    {
        require(standard == 0, "standard");
        require(IERC721(tokenContract).ownerOf(tokenId) == msg.sender, "not controller");
        agentId = ++last;
    }
}

contract RegisterAgentAbiTest is Test {
    HiveSeatVault vault;
    MockSeat seat;
    RealAbiAdapter adapter;
    address timelock = makeAddr("timelock");
    address operator = makeAddr("operator");
    address sink = makeAddr("sink");
    address treasury = makeAddr("treasury");
    uint256 constant SEAT_ID = 1343;

    function setUp() public {
        vm.warp(1_700_000_000);
        seat = new MockSeat();
        adapter = new RealAbiAdapter();
        vault = new HiveSeatVault(
            timelock, IERC721(address(seat)), IImdAgentAdapter(address(adapter)), IEnsReverseRegistrar(address(0)), sink
        );
        vm.prank(timelock);
        vault.setSeatOperator(operator);
        seat.mint(treasury, SEAT_ID);
        vm.prank(treasury);
        seat.safeTransferFrom(treasury, address(vault), SEAT_ID);
    }

    /// The vault encodes register(uint256,address,uint256,string) = 0x1f354cc5; the adapter only
    /// implements register(uint8,address,uint256,string) = 0xb68ca002. The call reverts, so the
    /// operator's registerAgent power is unusable against the real adapter.
    function test_registerAgent_matches_live_adapter_abi() public {
        assertEq(
            bytes4(keccak256("register(uint8,address,uint256,string)")), bytes4(0xb68ca002), "live selector"
        );
        vm.prank(operator);
        uint256 agentId = vault.registerAgent(SEAT_ID, "ipfs://agent");
        assertEq(agentId, 1, "agent registered through the live ABI");
        assertEq(adapter.last(), 1);
    }
}
```

### 2. Low: Worker pairings never expire on-chain and survive operator rotation, withdrawSeat and redeposit: a leaked operator key's pairings outlive the documented recovery

`src/HiveSeatVault.sol:212`

```
        if (seatCollection.ownerOf(tokenIdPlusOne - 1) != address(this)) return ERC1271_INVALID;
```

isValidSignature honours any digest present in _authorizedDigest as long as the vault currently owns the token. authorizeWorker checks expiresAt only at insertion (line 158) and does not store it; setSeatOperator does not invalidate digests the previous key inserted; withdrawSeat does not clear digests for the seat that leaves; the mapping is only ever cleared by revokeWorkerAuthorization, one digest at a time. Consequences for a leaked seatOperator key: (a) attacker-chosen device pairings (expiresAt up to type(uint64).max) stay VALID after the Timelock rotates the key, until the new operator enumerates every WorkerAuthorized event and revokes each digest individually; (b) a digest whose own expiresAt has passed still returns 0x1626ba7e; (c) when a seat is withdrawn and later redeposited (deposits are open, including by a buyer who resells to Hive), every old digest for that tokenId is VALID again with no new authorizeWorker call, so the unit test test_signature_invalid_after_seat_leaves does not mean withdrawal retires pairings. No seat or token can be moved this way (I1/I2 hold) and the behaviour is inherited from the reference IMDSeatStrategy, whose NatSpec relies on IMD enforcing expiresAt off-chain, so impact is bounded to who can run a seat (the brief's 'grief' class). It is recorded because the brief asks what a leaked key can do at worst: it can establish persistent pairings that 'rotate the operator' does not undo. Minimal fixes that keep the operator model: fold an epoch bumped by setSeatOperator and/or withdrawSeat into the stored value and reject stale epochs in isValidSignature, and/or store expiresAt alongside the tokenId and check it in isValidSignature. Merged from audit_math (two findings), audit_economics, audit_flow and audit_permissions.

**Reproduction**

State: vault holds seat 1343, seatOperator = K (leaked). 1) prank K: authorizeWorker({deviceKey: keccak256('attacker-device'), wallet: vault, tokenId: 1343, nonce: keccak256('attacker-nonce'), expiresAt: now+1h, relayOrigin: 'https://attacker.example'}) -> digest D; isValidSignature(D,'') == 0x1626ba7e. 2) prank Timelock: setSeatOperator(newKey); vm.warp(+365 days) so D's expiresAt is long past. Expected: 0xffffffff (key rotated out, authorization expired). Actual: 0x1626ba7e. 3) prank Timelock: withdrawSeat(1343, treasury) -> isValidSignature(D) == 0xffffffff; treasury calls seat.safeTransferFrom(treasury, vault, 1343) with no authorizeWorker by newKey. Expected: 0xffffffff for a fresh custody period. Actual: 0x1626ba7e. `forge test --match-path test/scratch/JudgePairing.t.sol` fails both assertions on the current code (0x1626ba7e != 0xffffffff). The specialists' Proof_58ea7af18ccb.t.sol fails for the same reason, but its AdapterMock implements IImdAgentAdapter with the uint256 signature and stops compiling once finding 1 is fixed; the proof below uses a plain stub instead.

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

/// @dev Not used by these tests; any address with code is enough for the constructor.
contract AdapterStub {
    fallback() external { revert("unused"); }
}

/// Pairings inserted by a (leaked) operator key outlive the key: they survive setSeatOperator rotation,
/// never expire on-chain, and silently come back when a withdrawn seat is re-deposited.
contract PairingLifecycleTest is Test {
    HiveSeatVault vault;
    SeatMock seat;

    address timelock = makeAddr("timelock");
    address leakedOperator = makeAddr("leakedOperator");
    address newOperator = makeAddr("newOperator");
    address treasury = makeAddr("treasury");
    uint256 constant SEAT_ID = 1343;

    function setUp() public {
        vm.warp(1_700_000_000);
        seat = new SeatMock();
        vault = new HiveSeatVault(
            timelock,
            IERC721(address(seat)),
            IImdAgentAdapter(address(new AdapterStub())),
            IEnsReverseRegistrar(address(0)),
            treasury
        );
        vm.prank(timelock);
        vault.setSeatOperator(leakedOperator);
        seat.mint(treasury, SEAT_ID);
        vm.prank(treasury);
        seat.safeTransferFrom(treasury, address(vault), SEAT_ID);
    }

    function _attackerAuth() internal view returns (HiveSeatVault.WorkerAuthorization memory a) {
        a.deviceKey = keccak256("attacker-device");
        a.wallet = address(vault);
        a.tokenId = SEAT_ID;
        a.nonce = keccak256("attacker-nonce");
        a.expiresAt = uint64(block.timestamp + 1 hours);
        a.relayOrigin = "https://attacker.example";
    }

    /// Rotating the operator key is the documented response to a leak, but it does not touch the
    /// digests the leaked key inserted: the attacker's device stays paired, even past expiresAt.
    function test_rotatingOperatorDoesNotInvalidateLeakedPairings() public {
        vm.prank(leakedOperator);
        bytes32 digest = vault.authorizeWorker(_attackerAuth());
        assertEq(vault.isValidSignature(digest, ""), bytes4(0x1626ba7e));

        // Timelock rotates the hot key (after its 48h delay) and the authorization's own expiry passes.
        vm.prank(timelock);
        vault.setSeatOperator(newOperator);
        vm.warp(block.timestamp + 365 days);

        // Expected: the leaked key's pairings are no longer honoured. Actual: still VALID.
        assertEq(
            vault.isValidSignature(digest, ""),
            bytes4(0xffffffff),
            "pairing inserted by the leaked operator key survives rotation and expiry"
        );
    }

    /// Withdrawing a seat makes its digests INVALID only while it is away; re-depositing the same
    /// seat silently re-arms every old pairing, including ones from a since-rotated operator.
    function test_redepositRearmsOldPairings() public {
        vm.prank(leakedOperator);
        bytes32 digest = vault.authorizeWorker(_attackerAuth());

        vm.prank(timelock);
        vault.setSeatOperator(newOperator);
        vm.prank(timelock);
        vault.withdrawSeat(SEAT_ID, treasury);
        assertEq(vault.isValidSignature(digest, ""), bytes4(0xffffffff));

        vm.prank(treasury);
        seat.safeTransferFrom(treasury, address(vault), SEAT_ID);

        // Expected: a fresh custody period starts with no pairings. Actual: the old digest is VALID again.
        assertEq(
            vault.isValidSignature(digest, ""),
            bytes4(0xffffffff),
            "old pairing re-armed by re-deposit without any authorizeWorker call"
        );
    }
}
```

### 3. Low: Inherited renounceOwnership can strand every custodied seat forever; transferOwnership removes the 48h delay for future exits

`src/HiveSeatVault.sol:47`

```
contract HiveSeatVault is Ownable2Step, ReentrancyGuard, IERC721Receiver {
```

Invariant I6 and the brief enumerate withdrawSeat, setSeatOperator, setRewardSink and setEnsName as the owner surface, but Ownable2Step also exposes renounceOwnership() (single call, no second step, inherited from Ownable 5.1) and transferOwnership()/acceptOwnership(). Nothing enforces that owner() is a TimelockController. If the Timelock executes renounceOwnership, owner() becomes address(0) and withdrawSeat, setSeatOperator, setRewardSink and setEnsName can never be called again: every held seat is frozen permanently while deposits remain open (I1 degenerates to 'never leaves'; sweepEarnings keeps working to whatever rewardSink was last set). If it transfers ownership to a non-timelock address that accepts, all later seat exits are instant, so the README guarantee 'every seat exit is queued publicly >=48h ahead' holds only while the owner remains the Timelock. Both actions are themselves queued through the Timelock, so they are public and delayed; this is a trust-assumption gap, not a permission bypass, and no change to the timelock design is proposed. If wanted, overriding renounceOwnership to revert is a one-line hardening that leaves the two-step handover to a new Timelock intact. Merged from audit_economics, audit_flow and audit_permissions.

**Reproduction**

State: vault holds seat 1343, owner = timelock. 1) prank timelock: vault.renounceOwnership(); vault.owner() == address(0). prank timelock: vault.withdrawSeat(1343, treasury). Expected under I1: the Timelock can always withdraw after the delay. Actual: reverts OwnableUnauthorizedAccount(timelock); seat.ownerOf(1343) == vault with no function able to move it. 2) prank timelock: transferOwnership(eoa); prank eoa: acceptOwnership(); prank eoa: withdrawSeat(1343, eoa) succeeds immediately. Both in test/scratch/JudgeProbe.t.sol (test_renounce_locks_seats_forever, test_transfer_ownership_to_eoa_removes_delay), passing on the current code.

### 4. Low: No ETH path and no rescue for non-seat NFTs: ETH payouts to the vault revert and ERC-721s pushed with transferFrom are stuck forever

`src/HiveSeatVault.sol:141`

```
        if (msg.sender != address(seatCollection)) revert NotSeatCollection();
```

The collection filter runs only inside onERC721Received, which is invoked only by safeTransferFrom/safeMint. A plain ERC-721 transferFrom from any other collection bypasses it, so the README's 'stray NFTs are rejected' holds only for the safe-transfer path. Once inside, such a token has no exit: withdrawSeat is hard-wired to seatCollection, and sweepEarnings calls the ERC-20 transfer(address,uint256) selector, which ERC-721s do not implement, so SafeERC20 reverts. The contract also has no receive/fallback and no ETH sweep: a payout that sends ETH to the seat's wallet address (the vault) with a plain call reverts at the sender, and ETH that arrives anyway (selfdestruct, coinbase) can never leave; the reference IMDSeatStrategy by contrast has an ETH path and a sweepToken. No seat and no earnings are at risk; this is a permanent lock of whatever a third party sends the wrong way, plus a possible revert in any ETH-paying integration. An owner-only rescue that excludes seatCollection (and an ETH path to rewardSink) would close it without touching the custody invariants. Merged from audit_math, audit_economics and audit_flow.

**Reproduction**

a) address(vault).call{value: 1 ether}('') returns false (verified on a mainnet fork and with mocks); after vm.deal(vault, 1 ether) no function can move the balance (sweepEarnings([address(0)]) reverts in SafeERC20). b) OtherNft other; other.mint(treasury, 7); prank treasury: other.transferFrom(treasury, vault, 7). Expected per README: rejected. Actual: other.ownerOf(7) == vault; sweepEarnings([other]) reverts (no transfer(address,uint256)); prank timelock: withdrawSeat(7, treasury) reverts (seatCollection.ownerOf(7) does not exist); token 7 stays in the vault. Both in test/scratch/JudgeProbe.t.sol (test_eth_cannot_be_received_or_swept, test_foreign_nft_unsafe_transfer_is_stuck), passing on the current code.

### 5. Info: Once registerAgent works, the vault cannot manage the ERC-8004 record it controls, and the operator can mint unlimited duplicate agents per seat

`src/HiveSeatVault.sol:179`

```
        agentId = agentAdapter.register(0, address(seatCollection), tokenId, agentURI);
```

The live Adapter8004 binds each new agent to (collection, tokenId) and gates setAgentURI, setMetadata, setAgentWallet and unsetAgentWallet on IERC721(collection).ownerOf(tokenId) == msg.sender, i.e. on the vault. The vault exposes only registerAgent, so while a seat is custodied neither the Timelock nor the operator can correct an operator-supplied agentURI (the string is unvalidated); the only route is a 48h withdrawSeat, act, redeposit. The adapter also performs no deduplication: every register call mints another agent bound to the same seat, and the vault does not track prior registrations, so a leaked operator key can spam bindings for gas. The same applies to the collection's own owner-gated calls such as setIdentityHash. Nothing here moves value or a seat and the reference IMDSeatStrategy has the same limitation, so this is an operational note within the brief's 'grief, never steal' envelope. If wanted: an onlyOwner forwarder restricted to a fixed allowlist of adapter/collection selectors (never approve/transfer). Merged from audit_math, audit_flow and audit_permissions.

**Reproduction**

Mainnet fork (test/scratch/JudgeFork2.t.sol, test/scratch/JudgeFork.t.sol): vault holds seat 1343; from address(vault) call adapter 0xde152AfB7db5373F34876E1499fbD893A82dD336 register(uint8,address,uint256,string)(0, collection, 1343, 'ipfs://wrong') -> agentId 52468; a second identical call -> agentId 52469 (both bound to seat 1343). Then setAgentURI(52468, 'ipfs://fixed') from the timelock reverts NotController(timelock, 52468) (selector 0xa9d48768), from the operator reverts NotController(operator, 52468), and from address(vault) succeeds; HiveSeatVault has no function that makes that call.

### 6. Info: authorizedTokenId cannot distinguish an authorization for tokenId 0 (which exists on mainnet) from 'no authorization'

`src/HiveSeatVault.sol:219`

```
        return v == 0 ? 0 : v - 1;
```

The mapping stores tokenId + 1 so that token 0 is representable, but the view helper collapses it back: for a digest authorized for token 0 it returns 0, the documented 'none' sentinel. identity.md token 0 exists (ownerOf(0) = 0x200E710aCAA6A93bbc77146026328C40F1d60fB1 at block 26149550) and deposits are open, so the state is reachable. isValidSignature is unaffected; only keepers or tests relying on authorizedTokenId misread it. Returning (bool, uint256) or exposing the raw stored value would remove the ambiguity. From audit_math.

**Reproduction**

State: vault holds token 0. prank operator: authorizeWorker(auth with tokenId 0) -> d. isValidSignature(d,'') == 0x1626ba7e but authorizedTokenId(d) == 0 == authorizedTokenId(keccak256('unknown')). test_token0_ambiguous_in_view_helper in test/scratch/JudgeProbe.t.sol passes on the current code.

### 7. Info: Fork suite forks mainnet unconditionally, so plain `forge test` fails offline, and it never exercises registerAgent against the live adapter

`test/HiveSeatVaultFork.t.sol:36`

```
        vm.createSelectFork(vm.envOr("ETH_RPC_URL", string("https://ethereum-rpc.publicnode.com")));
```

setUp creates a mainnet fork with no guard, so any environment without network (including an offline verifier) reports the suite as failed, masking the 19 passing unit tests in a CI summary. With network, the three fork tests pass (digest equals the live IMDSeatStrategy's, a real seat pairs, operator cannot withdraw), but none calls registerAgent against the real adapter, which is why finding 1 went unnoticed; the unit MockAdapter implements the vault's own (wrong) interface and so cannot catch it either. Suggested: skip the suite when ETH_RPC_URL is unset or unreachable, and add a fork test that calls vault.registerAgent on the live adapter. Merged from audit_math and audit_economics.

**Reproduction**

ETH_RPC_URL=http://127.0.0.1:9 forge test --match-path test/HiveSeatVaultFork.t.sol -> 'Suite result: FAILED' with 'vm.createSelectFork: could not instantiate forked environment ... Connection refused' in setUp(). With network: grep shows no test in test/ calls vault.registerAgent against 0xde152AfB...; adding one (test/scratch/JudgeFork.t.sol) reverts as in finding 1.

---

Judge's submission `bcfbfdddd49334ca61ac78676d8a2b9f12b7ab3463afa10533c5ab4a13e317f0`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
