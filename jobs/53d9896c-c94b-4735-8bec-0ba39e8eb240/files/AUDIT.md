# Audit report

> Audit the HiveSeatVault contract in src/HiveSeatVault.sol: a non-upgradeable custody vault holding Project Hive's identity.md seat NFTs (ERC-721 collection 0x0000eC93127BAA929E58E97dd0095A2BFb38ec1D). The owner is a 48h OpenZeppelin TimelockController; a scoped seatOperator hot key may pair and run the seats but must never be able to move them. The ERC-1271 WorkerAuthorization pairing (authorizeWorker, revokeWorkerAuthorization, workerAuthorizationDigest, isValidSignature) is lifted verbatim from the audited IMDSeatStrategy so IMD accepts this contract as a seat's signer; the EIP-712 domain is 'IdentityMD Worker' version 2, bound to the seat collection. The security of the whole design rests on one property and it deserves the hardest look. (1) isValidSignature must return the ERC-1271 magic value ONLY for digests inserted by authorizeWorker, i.e. well-formed WorkerAuthorizations whose wallet equals address(this) and whose tokenId the vault owns. There must be NO path by which the seatOperator, a hot key that may be compromised, can cause isValidSignature to accept an arbitrary hash, in particular the hash of a Seaport order that would list or sell a seat. Confirm authorizeWorker only ever stores the EIP-712 digest it computes itself from a structured WorkerAuthorization, that an attacker-chosen digest cannot be inserted into the mapping, and that no Seaport or marketplace order hash can collide with a WorkerAuthorization digest. Then the custody invariants. (2) A seat NFT must leave the vault ONLY via withdrawSeat, which is onlyOwner (the Timelock): confirm there is no other path that transfers, approves (approve or setApprovalForAll), or lists a held seat, and that the vault never grants NFT approval to anyone. (3) The seatOperator's only powers are authorizeWorker, revokeWorkerAuthorization and registerAgent: confirm none of them can move value or a seat, and that a leaked operator key can at worst grief (stop pairing), never steal. (4) sweepEarnings must be unable to move a seat: it uses the ERC-20 interface, reverts if the token is the seat collection, and sends only to the fixed rewardSink. Confirm there is no caller-supplied destination and no way to reach the ERC-721 collection through it. (5) withdrawSeat, setSeatOperator, setRewardSink and setEnsName are all onlyOwner: confirm there is no privilege-escalation or reentrancy path around the Timelock, and that onERC721Received cannot be abused to brick the vault or spoof an approval. (6) The contract is non-upgradeable with no delegatecall and no selfdestruct: confirm the rules cannot change silently. Also assess reentrancy on registerAgent (external adapter call) and sweepEarnings (token transfers), and whether a hostile ERC-20 passed to sweepEarnings can do anything beyond reverting its own sweep. Report findings rather than fixing them. Do not propose changes to the 48h timelock design, the operator model, or the economics.

| | |
|---|---|
| Repository | https://github.com/ProjectHive-IMD/hive-seat-vault.git |
| Commit | `c8ea8b8e7916bd4182662ac0ba38914b6bd970cc` |
| Job | `53d9896c-c94b-4735-8bec-0ba39e8eb240` |
| Judged | 2026-10-08 19:40 UTC |
| Findings | 3 low · 6 info |

Four agents audited the code as it is at `c8ea8b8`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: registerAgent has no once-per-seat guard: a leaked operator key can bind unlimited ERC-8004 agents with attacker-chosen agentURI to a custodied seat, and the vault has no path to correct them

`src/HiveSeatVault.sol:207`

```
        agentId = agentAdapter.register(0, address(seatCollection), tokenId, agentURI);
```

Merged from four specialists (economics, flow, math, permissions). The NatSpec says registration is 'needed once for a never-registered seat' and invariant I3/I8 bound a leaked hot key to 'stop pairing' grief that rotation 'fully neutralises'. Neither holds for registration. The vault stores no per-seat agentId and rejects nothing; the live Adapter8004 proxy (0xde152AfB7db5373F34876E1499fbD893A82dD336) has no dedup either: every call mints a fresh ERC-8004 agent in the IdentityRegistry (0x8004A169FB4a3325136EB29fA0ceB6D2e539a432), owned by the adapter, permanently bound to (collection, tokenId), with the operator-supplied agentURI written verbatim. Every adapter correction path (setAgentURI, setMetadata, setAgentWallet) requires msg.sender == collection.ownerOf(tokenId), which is the vault, and the vault exposes no pass-through, so neither the Timelock nor a rotated operator can ever edit or retire a poisoned registration; only another duplicate can be appended. This also means a seat's legitimate pre-existing agent record cannot be updated for the whole custody period. No seat, ERC-20 or ETH moves (verified: ownerOf(1343) == vault after every call; the adapter gets no approval; registerAgent is nonReentrant), so this is persistent identity/reputation griefing that outlives key rotation, wider than the documented leaked-key blast radius. Fixing it without changing the operator model: record agentId per tokenId and reject a second registerAgent for a registered seat (optionally owner-overridable), and/or add an onlyOwner pass-through to Adapter8004.setAgentURI so the Timelock can correct a hostile URI.

**Reproduction**

Unit (test/scratch/Repro.t.sol::test_register_twice_same_seat, repo MockAdapter): vault holds seat 1343; prank(operator) registerAgent(1343, 'ipfs://one') returns 52001; registerAgent(1343, 'ipfs://two') returns 52002. Expected per NatSpec: second call rejected or same id; actual: both succeed. Mainnet fork at block 26149810 (test/scratch/ForkRepro.t.sol::test_fork_register_twice_and_no_correction_path, live collection + live adapter, seat 1343 deposited from treasury 0x84b31CB3D205EfD2d20F29eA7ccaB1bc34326DdB): the two calls return agentIds 52472 and 52473; IdentityRegistry.ownerOf(52473) == adapter, tokenURI(52473) == 'ipfs://two'. Adapter8004.setAgentURI(52473, ...) reverts from the operator and from the timelock; it succeeds only with msg.sender == vault, and HiveSeatVault has no function that issues that call. Seat 1343 remains owned by the vault throughout.

### 2. Low: setSeatOperator retires every live pairing, including the Timelock's own and on a same-address re-set, contrary to the line comment and I8

`src/HiveSeatVault.sol:303`

```
        unchecked { ++authEpoch; } // rotating (or disabling) the hot key retires every pairing it made (I8)
```

From the flow specialist, reproduced. authEpoch is global and authorizeWorker stamps the current epoch on every pairing regardless of who made it (the owner passes onlySeatOperator too). The comment on this line and the I8 header say rotating the hot key retires 'every pairing it made', i.e. the replaced key's pairings. In fact every setSeatOperator call invalidates every pairing in the vault: pairings the Timelock itself created (the normal bootstrap order is deploy, deposit, owner pairs, later assign a hot key), and all pairings when the Timelock re-sets the same address. Every such call is a publicly queued 48h operation, but nothing in code or docs warns that the first assignment of an operator or an unchanged re-set takes every seat's ERC-1271 signer status offline in one block, after which IMD has to re-pair each seat. Over-revocation is safe-side (never under-revocation), hence low. Fixing it: either store the authorizing key in Pairing and only retire pairings made by the key being replaced, or keep the global epoch and correct the NatSpec/I8/README so operators expect the full reset.

**Reproduction**

test/scratch/Repro.t.sol::test_owner_pairing_dies_on_first_operator_set: fresh vault, seatOperator == address(0); prank(timelock) authorizeWorker(auth for held seat 1343) -> digest d; isValidSignature(d, '') == 0x1626ba7e. prank(timelock) setSeatOperator(operator) (first-ever assignment, no key rotated). Expected per the line comment: owner-made pairing untouched. Actual: isValidSignature(d, '') == 0xffffffff. test_same_operator_reset_retires_pairings: operator pairs seat 1343 -> VALID; timelock calls setSeatOperator(operator) with the same address; actual: INVALID.

### 3. Low: Constructor validates only rewardSink_: a zero seatCollection_ or agentAdapter_ deploys an immutable vault that can never accept a seat or register an agent

`src/HiveSeatVault.sol:146`

```
        if (rewardSink_ == address(0)) revert ZeroAddress();
```

Merged from three specialists (economics, math, permissions). rewardSink_ is zero-checked and owner_ is checked by Ownable, but the two immutables the whole design hangs on are stored unchecked (ensReverseRegistrar is documented as optionally zero; these two are not). With seatCollection_ == address(0): onERC721Received demands msg.sender == address(0), which no caller can satisfy, so every safeTransferFrom of a real seat reverts with NotSeatCollection; withdrawSeat, authorizeWorker, registerAgent and isValidSignature (once a pairing exists) revert on the call to an address without code. With agentAdapter_ == address(0), registerAgent always reverts (empty returndata cannot be decoded as uint256). The immutables cannot be corrected after deployment; the only recovery is a redeploy and a new Timelock ownership handover. Deploy-time misconfiguration only, no funds at risk because nothing can be deposited (a seat pushed in via unsafe transferFrom is recoverable through rescueERC721 since the real collection differs from the stored zero). Fix: one ZeroAddress check per immutable.

**Reproduction**

test/scratch/Repro.t.sol::test_zero_collection_deploys_and_rejects_every_deposit. Input: new HiveSeatVault(timelock, IERC721(address(0)), IImdAgentAdapter(address(0)), IEnsReverseRegistrar(address(0)), sink). Expected: constructor reverts ZeroAddress as it does for rewardSink_. Actual: deploys, seatCollection() == address(0); seat.safeTransferFrom(holder, vault, 2) reverts NotSeatCollection; prank(timelock) withdrawSeat(2, to) reverts; prank(timelock) registerAgent(2, 'x') reverts.

### 4. Info: Leaked operator key window: on-chain pairing expiry is operator-chosen and uncapped, so a compromised hot key keeps pair/revoke/register power until the 48h Timelock executes setSeatOperator

`src/HiveSeatVault.sol:179`

```
        if (auth.expiresAt <= block.timestamp) revert AuthorizationExpired();
```

Merged from three specialists (economics, math, permissions); trust assumption on the hot key, no change to the operator model proposed. Property (3) is confirmed: the operator cannot move a seat, ERC-20 or ETH. But I8's three freshness conditions are not equal: expiresAt is a field of the operator-supplied struct, checked only to be in the future and stored verbatim, so a compromised key pairs its own deviceKey/relayOrigin to every held seat with expiresAt = type(uint64).max (IMD's own pairing page uses now+900s), and can delete every legitimate pairing via revokeWorkerAuthorization (digests are public in WorkerAuthorized events), including ones the owner made. Rotation is onlyOwner behind the 48h Timelock, so the earliest neutralisation is schedule + minDelay; during that window the attacker runs Project Hive's seats as its own workers (on-chain, rewards landing in the vault still only reach rewardSink). The attacker cannot extend the window: authEpoch is bumped atomically when the rotation executes. Recorded so the I8 wording 'VALID only while fresh' is not read as an on-chain bound independent of the operator: the effective neutraliser is setSeatOperator, and any lifetime bound must come from the IMD relay's own validation of expiresAt.

**Reproduction**

test/scratch/Repro.t.sol::test_expiresAt_uncapped: prank(operator) authorizeWorker with expiresAt = 18446744073709551615 -> digest d; vm.warp(+100 years); isValidSignature(d, '') still == 0x1626ba7e. Expected if expiry bounded the hot key: INVALID at some point. Actual: VALID until prank(timelock) setSeatOperator(k2), after which it is 0xffffffff. test_operator_revokes_owner_pairing: owner-made pairing; prank(operator) revokeWorkerAuthorization(d) succeeds and the digest is INVALID.

### 5. Info: Trust assumption: nothing pins the owner to a TimelockController; one queued transferOwnership plus acceptOwnership makes withdrawSeat instant from then on

`src/HiveSeatVault.sol:315`

```
    ///         handed to a NEW Timelock via transferOwnership + acceptOwnership (two-step).
```

Merged from two specialists (math, permissions). Properties (5) and (6) hold as written: withdrawSeat, setSeatOperator, setRewardSink, setEnsName, rescueERC721 and transferOwnership are onlyOwner, renounceOwnership reverts, there is no delegatecall or selfdestruct in reachable code (the only 0xf4 byte in the compiled runtime sits at offset 7075, inside the 51-byte CBOR metadata that starts at 7063), and no reentrancy path reaches an onlyOwner function. The only non-owner writer of ownership is Ownable2Step.acceptOwnership, which requires msg.sender == pendingOwner, a value only a timelocked transferOwnership can set, so there is no bypass of the delay. The residual is that the 48h delay is one-shot and a property of whoever the owner is: the constructor accepts any owner_ and the contract never checks that a transfer target is a Timelock, so once transferOwnership(x) has sat in the queue for 48h and x has accepted, x withdraws every seat with no further delay. Watchers of the Timelock queue must treat a transferOwnership whose target is not a known Timelock as equivalent to an immediate withdrawal of every seat. Inherent to the chosen design; no change proposed.

**Reproduction**

test/scratch/Repro.t.sol::test_owner_handoff_to_eoa_then_instant_withdraw. State: owner = timelock, vault holds 1343. prank(timelock) transferOwnership(eoa); prank(eoa) acceptOwnership(); prank(eoa) withdrawSeat(1343, eoa) in the same block. Expected under 'every seat exit is queued publicly >=48h ahead': the withdrawal itself is delayed. Actual: seat.ownerOf(1343) == eoa immediately after acceptance.

### 6. Info: Trust assumption: agentAdapter is a third-party-owned upgradeable proxy, so registerAgent's behaviour is not fixed even though the vault is non-upgradeable (no path to a seat found)

`src/HiveSeatVault.sol:83`

```
    IImdAgentAdapter public immutable agentAdapter; // ERC-8004 registration
```

Merged from two specialists (math, permissions). Invariant I7 holds for the vault itself (no proxy, no delegatecall, no selfdestruct, every configuration behind the Timelock). Its two external dependencies differ: the identity.md collection at 0x0000eC93127BAA929E58E97dd0095A2BFb38ec1D is not a proxy (EIP-1967 implementation slot is zero) and exposes no burn, but the adapter the fork tests resolve from IMDSeatStrategy.IMD_AGENT_ADAPTER() (0xde152AfB7db5373F34876E1499fbD893A82dD336) is an EIP-1967 proxy whose implementation slot holds 0xa6D23f27D3b1780B12488482a008cB3c3787135f and whose owner() is 0x03302Df40186D9B85faEA4fbb6cC5da028B23149, which can replace what registerAgent does at any time without a Timelock delay and can repoint the identity registry. Traced what a hostile implementation could do with the vault's call: it receives no value and no approval; registerAgent holds the nonReentrant lock so re-entering sweepEarnings/sweepETH/registerAgent reverts; authorizeWorker/revokeWorkerAuthorization require the operator or owner; withdrawSeat/rescueERC721/setters are onlyOwner; onERC721Received requires msg.sender == seatCollection; isValidSignature is a view lookup. Worst case is that registration reverts, burns gas, or registers somewhere other than the canonical registry. Dependency trust assumption, not a vault defect.

**Reproduction**

cast storage 0xde152AfB7db5373F34876E1499fbD893A82dD336 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc (mainnet, block 26149810) returns 0x...a6d23f27d3b1780b12488482a008cb3c3787135f; the same slot on 0x0000eC93127BAA929E58E97dd0095A2BFb38ec1D returns zero; cast call ...dD336 'owner()(address)' returns 0x03302Df40186D9B85faEA4fbb6cC5da028B23149. Expected for an 'immutable rules' claim: a non-upgradeable dependency. Actual: upgradeable by a third-party address. In test/scratch/ForkRepro.t.sol the seat stays owned by the vault after every registerAgent call.

### 7. Info: Deposits are open and untracked: onERC721Received only emits an event, unsafe transferFrom deposits emit nothing, and a third party's seat is pairable and sweepable but only returnable by a Timelock p

`src/HiveSeatVault.sol:163`

```
        emit SeatDeposited(tokenId, from);
```

Merged from two specialists (flow, permissions). Property (5)'s hook is confirmed safe: it writes no storage, cannot brick the vault and cannot grant or spoof an approval. Two consequences of the open-deposit design are recorded as trust assumptions. First, this emit is the only deposit record and ERC-721 transferFrom (OpenZeppelin and the live Solady collection alike) never calls the receiver hook, so a seat moved in with transferFrom is fully custodied, pairable, registrable and exits only via withdrawSeat, yet the vault emits nothing; tooling that enumerates custodied seats from SeatDeposited/SeatWithdrawn under-counts, and the 'stray NFTs are rejected' gate holds only for safe transfers (the repo's own test_rescue_foreign_nft_but_never_seats relies on this bypass). Second, the depositor is not stored and there is no self-service return, so an identity.md holder who sends a seat here by mistake depends entirely on the Timelock queuing withdrawSeat back to them, while the operator can immediately pair/register that seat and anyone can sweep its earnings to Hive's rewardSink. Fix for the first point is documentation (the collection's Transfer events with to == vault are the source of truth); the second is a design choice the brief reserves.

**Reproduction**

test/scratch/Repro.t.sol::test_unsafe_deposit_no_event: mint seat 2 to EOA; EOA calls seat.transferFrom(EOA, vault, 2); vm.recordLogs shows no log with emitter == vault (expected if the event were the deposit record: SeatDeposited(2, EOA)); then prank(operator) authorizeWorker(tokenId 2) succeeds and isValidSignature(digest, '') == 0x1626ba7e. test_third_party_seat_stuck_behind_owner: third party safeTransferFrom(seat 7) into the vault succeeds; prank(operator) authorizeWorker(auth for 7) succeeds; prank(third) withdrawSeat(7, third) reverts OwnableUnauthorizedAccount.

### 8. Info: sweepEarnings is contained against a hostile ERC-20, but such a token can make the vault emit a fabricated Swept event of any amount

`src/HiveSeatVault.sol:271`

```
                emit Swept(token, bal, sink);
```

From the math specialist, reproduced; answers the brief's hostile-ERC-20 question. Property (4) is confirmed: there is no caller-supplied destination, the seat collection is rejected by address before any call, and a hostile token runs with its own authority, so seatCollection.transferFrom(vault, ...) from inside its transfer reverts (no approval was ever granted), re-entering sweepEarnings/sweepETH/registerAgent reverts on ReentrancyGuard, a no-code address reverts in the balanceOf decode, and a reverting or false-returning token only aborts that caller's own sweep (SafeERC20 bubbles the revert). The one thing it can do beyond reverting its own sweep is lie: balanceOf returning 1e30 and transfer returning true without moving anything makes the vault emit Swept(token, 1e30, rewardSink). Impact is limited to off-chain consumers that trust Swept events without filtering on known token addresses.

**Reproduction**

test/scratch/Repro.t.sol::test_hostile_token_fake_swept_event_only. Input: anyone calls sweepEarnings([hostileToken]) where hostileToken.balanceOf returns 1e30 and transfer re-enters sweepEarnings and attempts seat.transferFrom(vault, token, 1343) before returning true. Expected: no event unless value moved. Actual: Swept(hostileToken, 1e30, sink) is emitted by the vault; the re-entry reverted; the seat move reverted; seat 1343 remains owned by the vault.

### 9. Info: sweepETH and sweepEarnings liveness depends on rewardSink accepting value; a sink without a payable receive, or a token that blacklists the sink, blocks sweeps until a 48h setRewardSink

`src/HiveSeatVault.sol:284`

```
            (bool ok,) = rewardSink.call{value: bal}("");
```

From the permissions specialist, reproduced. Both sweep paths are permissionless with a fixed sink, which is the intended design. The operational consequence is that if the sink itself refuses value (no receive()/fallback, or a USDC-style blacklist of the sink address) earnings are stuck in the vault until the Timelock executes setRewardSink, at least 48h later. No value is lost and nothing else is blocked (sweepEarnings processes tokens independently per call, so a caller can omit the blocked token). Reentrancy from the sink during sweepETH is contained: sweepEarnings/sweepETH/registerAgent share one ReentrancyGuard and every other state-changing entry is role-gated or msg.sender-gated to the collection.

**Reproduction**

test/scratch/Repro.t.sol::test_sink_without_receive_blocks_sweepETH. State: timelock sets rewardSink to a contract with no receive/fallback; vault.balance == 1 ether. Input: vault.sweepETH() from anyone. Expected: ETH reaches the sink. Actual: reverts ETHSweepFailed and keeps reverting for every caller until the owner's setRewardSink(newSink) executes.

---

Judge's submission `f48e2770ac824cc029334f0c3bc76e60c34bd5a57c182c3b50a12d7580b66faf`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
