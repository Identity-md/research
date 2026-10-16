# Audit report

> Cross-chain settlement integrity, hardest first: (1) IMDRetroWall.ccipReceive: router, source chain selector and sender checks, winnerIndex = randomWord % ticketCount(epoch), claimable[winner] += prize, then pull-based claimReward(). (2) requestSettlement(epoch): exact-fee InsufficientFee revert, SETTLEMENT_RETRY_DELAY = 1 day, and the SettlementStatus Requested/Settled machine must prevent double settlement or re-request at the epoch boundary. (3) VrfCcipRelay on Base: ccipReceive validation, _deliver when the word is cached, rawFulfillRandomWords first-word-wins and the UnknownRequest guard, and permissionless deliver(epoch) must not send a stale/zero word or replay a delivered epoch. (4) ERC-165 supportsInterface for IAny2EVMMessageReceiver (0x85572ffb) must not revert for unknown ids or 0xffffffff, because the off-ramp silently downgrades such receivers to token-only no-ops. (5) Economic bounds: MAX_STAMPS_PER_EPOCH = 5, 500 burn / 500 pool, stranded funds (no sweep). Current pair: wall 0x9550E4F888d1C084CB1C8E74677Da54109723EE3 (Robinhood 4663), relay 0x887bbed753938087Ce61Ca768a358848177E6eaA (Base 8453). Audited commit a5c1af9.

| | |
|---|---|
| Repository | https://github.com/gimogo/NTTW.git |
| Commit | `a5c1af9fc13c8413b508b245a997fdfc2689fa81` |
| Job | `44df6543-f9d6-4f44-9d69-40e0f7223b0c` |
| Judged | 2026-10-16 07:04 UTC |
| Findings | 2 medium · 5 low · 2 info |

Four agents audited the code as it is at `a5c1af9`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Relay never re-sends a cached word once delivered[epoch] is set, so the wall's 1-day re-request cannot recover a sent-but-unexecuted delivery and only burns the caller's CCIP fee

`contracts/VrfCcipRelay.sol:169`

```
        if (delivered[epoch]) return bytes32(0);
```

VrfCcipRelay._deliver sets delivered[epoch]=true the moment the Base->Robinhood message is handed to the router (line 170) and returns bytes32(0) without sending on every later call. The retry branch of ccipReceive (lines 123-125) goes through the same _deliver, so the wall-initiated retry that IMDRetroWall.requestSettlement allows after SETTLEMENT_RETRY_DELAY (IMDRetroWall.sol:375-378), and that the wall NatSpec (lines 53-54, 139-141), the relay NatSpec (lines 19-20, 110-111) and README section 4/5 ('lost message -> re-request after 1 day', 'the epoch stays Requested and retryable') present as the recovery for a lost or stalled CCIP message, is a silent no-op in exactly the case it exists for: a reply that left Base (deliver() or an earlier retry) but was never executed on the wall. The wall still charges the full Robinhood->Base fee (msg.value >= fee enforced, only the excess refunded), bumps settlementRequestedAt so the next retry is another day away, and stays in Requested with epochPrize[epoch] locked (no sweep). deliver(epoch) is blocked by the same flag, so the contracts have no path left; only off-contract CCIP manual execution of the original reply can finish the epoch. Re-sending is safe because the wall rejects a duplicate with EpochAlreadySettled (IMDRetroWall.sol:426). Merged from two specialists (audit_flow e66a6230, audit_math 1977eb8c); both proofs fail on the current code for the stated reason. Minimal fix that keeps the design: in the ccipReceive retry branch re-send the cached word regardless of delivered[epoch] (e.g. a private _send(epoch) without the flag check, keeping deliver() idempotent for unsolicited callers), optionally emitting an event when a retry is dropped.

**Reproduction**

State: epoch 1 has 1 ticket (alice). Step 1: warp past epoch 1; retrier calls wall.requestSettlement{value: fee}(1); the relay requests VRF, VRF fulfils word 12345, relay.deliver(1) sends the reply (delivered[1]=true) but the reply is not executed on the wall; wall.settlementStatus(1)==Requested. Step 2: warp +SETTLEMENT_RETRY_DELAY (1 day); retrier calls wall.requestSettlement{value: fee}(1) again (accepted, fee taken). Step 3: the retry message executes on the relay (relay.ccipReceive with data abi.encode(1)). Expected: a new relay->wall ccipSend carrying (1, 12345) and RandomnessDelivered, after which the wall settles with claimable[alice]=500e18. Actual: _deliver hits `if (delivered[epoch]) return bytes32(0);`, no message is sent, no event, the retrier's fee is gone, the epoch stays Requested. Reproduced with forge: test/scratch/RetryNoop.t.sol fails with 'retry must re-send the cached word to the wall: 3 != 4' and test/scratch/RelayRetryNoRedeliver.t.sol (the other specialist's proof) fails with 'epoch 1 must be Settled after the retry: 1 != 2'.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import {IMDRetroWall} from "contracts/IMDRetroWall.sol";
import {VrfCcipRelay} from "contracts/VrfCcipRelay.sol";
import {Client, IRouterClient, IAny2EVMMessageReceiver} from "contracts/interfaces/ChainlinkCCIP.sol";
import {VRFV2PlusClient, IVRFCoordinatorV2Plus, IVRFConsumerV2Plus} from "contracts/interfaces/ChainlinkVRF.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/// @dev Plain 18-decimal ERC-20 standing in for NOTES.
contract Notes is ERC20 {
    constructor() ERC20("NOTES", "NOTES") {
        _mint(msg.sender, 1_000_000e18);
    }
}

/// @dev Router test double that QUEUES messages instead of delivering them, so a
///      test can leave one CCIP leg "stalled" and execute the others by hand.
///      One instance plays the router on both chains.
contract QueueRouter is IRouterClient {
    struct Queued {
        address receiver;
        uint64 sourceSelector;
        address sender;
        bytes data;
    }

    uint256 public constant FEE = 0.001 ether;
    mapping(address => uint64) public selectorOf;
    Queued[] public queue;

    function setSelector(address who, uint64 selector) external {
        selectorOf[who] = selector;
    }

    function count() external view returns (uint256) {
        return queue.length;
    }

    function getFee(uint64, Client.EVM2AnyMessage memory) external pure returns (uint256) {
        return FEE;
    }

    function ccipSend(uint64, Client.EVM2AnyMessage calldata message) external payable returns (bytes32) {
        require(msg.value >= FEE, "fee");
        address receiver = abi.decode(message.receiver, (address));
        queue.push(Queued(receiver, selectorOf[msg.sender], msg.sender, message.data));
        return bytes32(queue.length);
    }

    /// @dev Execute queued message `i` on its receiver (the off-ramp's job).
    function exec(uint256 i) external {
        Queued memory q = queue[i];
        IAny2EVMMessageReceiver(q.receiver).ccipReceive(
            Client.Any2EVMMessage({
                messageId: bytes32(i + 1),
                sourceChainSelector: q.sourceSelector,
                sender: abi.encode(q.sender),
                data: q.data,
                destTokenAmounts: new Client.EVMTokenAmount[](0)
            })
        );
    }
}

contract QueueVRF is IVRFCoordinatorV2Plus {
    uint256 public next = 1;
    mapping(uint256 => address) public consumerOf;

    function requestRandomWords(VRFV2PlusClient.RandomWordsRequest calldata) external returns (uint256 id) {
        id = next++;
        consumerOf[id] = msg.sender;
    }

    function fulfill(uint256 id, uint256 word) external {
        uint256[] memory w = new uint256[](1);
        w[0] = word;
        IVRFConsumerV2Plus(consumerOf[id]).rawFulfillRandomWords(id, w);
    }
}

/// @title Retry after a stalled reply leg must re-send the cached word
/// @notice Fails on the current code: once `delivered[epoch]` is true the relay's
///         `ccipReceive` retry path returns silently, so the wall's
///         SETTLEMENT_RETRY_DELAY retry pays a CCIP fee for a no-op and the epoch
///         stays `Requested` while the reply message is stuck.
contract RetryNoopTest is Test {
    uint64 constant WALL_SEL = 1;
    uint64 constant RELAY_SEL = 2;

    Notes token;
    QueueRouter router;
    QueueVRF vrf;
    IMDRetroWall wall;
    VrfCcipRelay relay;
    address alice = makeAddr("alice");
    address retrier = makeAddr("retrier");

    function setUp() public {
        token = new Notes();
        router = new QueueRouter();
        vrf = new QueueVRF();
        wall = new IMDRetroWall(token, address(router), RELAY_SEL);
        relay = new VrfCcipRelay(address(vrf), 1, bytes32(uint256(1)), address(router), WALL_SEL, address(wall));
        wall.setRelay(address(relay));
        router.setSelector(address(wall), WALL_SEL);
        router.setSelector(address(relay), RELAY_SEL);
        vm.deal(address(relay), 1 ether);
        vm.deal(retrier, 1 ether);

        token.transfer(alice, 10_000e18);
        vm.startPrank(alice);
        token.approve(address(wall), type(uint256).max);
        wall.stampNote("hello", "#ff0000", 1, 1, 0);
        vm.stopPrank();
    }

    function test_retryAfterStalledReplyLegResendsWord() public {
        // Epoch 1 ends; request its settlement.
        vm.warp(block.timestamp + wall.EPOCH_DURATION());
        vm.prank(retrier);
        wall.requestSettlement{value: router.FEE()}(1);
        assertEq(router.count(), 1); // msg0: wall -> relay

        // Execute the request on the relay and fulfil VRF.
        router.exec(0);
        vrf.fulfill(1, 12345);
        assertTrue(relay.randomnessReady(1));

        // Relay sends the word back (msg1: relay -> wall) ... and that leg stalls:
        // we never execute msg1 on the wall.
        relay.deliver(1);
        assertEq(router.count(), 2);
        assertTrue(relay.delivered(1));
        assertEq(uint8(wall.settlementStatus(1)), uint8(IMDRetroWall.SettlementStatus.Requested));

        // After SETTLEMENT_RETRY_DELAY the wall allows a retry, and the retrier pays the fee.
        vm.warp(block.timestamp + wall.SETTLEMENT_RETRY_DELAY());
        vm.prank(retrier);
        wall.requestSettlement{value: router.FEE()}(1);
        assertEq(router.count(), 3); // msg2: wall -> relay (the retry)

        // Execute the retry on the relay. Expected: the relay re-sends the cached
        // word (a new relay -> wall message). Actual on current code: silent no-op.
        router.exec(2);
        assertEq(router.count(), 4, "retry must re-send the cached word to the wall");

        // Executing the re-sent message settles the epoch and pays alice.
        router.exec(3);
        assertEq(uint8(wall.settlementStatus(1)), uint8(IMDRetroWall.SettlementStatus.Settled));
        assertEq(wall.claimable(alice), 500e18);
    }
}
```

### 2. Medium: Settlement liveness depends on an externally owned VRF subscription and immutable Chainlink parameters with no fallback, so one off-contract action strands every future prize pool while stamping keeps

`contracts/VrfCcipRelay.sol:42`

```
    uint256 public immutable SUBSCRIPTION_ID;
```

Trust assumption, not a permission bypass, reported because it is material and contradicts the stated trust model. The relay has no owner, but VRF_COORDINATOR, KEY_HASH and SUBSCRIPTION_ID are immutable with no setter, the wall's relay is one-shot (IMDRetroWall.sol:298-304) and both routers are immutable. The production subscription (id 51441836222580451052993458818119349024779142164800689033215217746100047214776 per FACTS/RUNBOOK) is owned by the deployer EOA 0x380fbF99A903253E14b9EB797807B4B92cd4b019; that owner can call cancelSubscription or removeConsumer(relay) on the Base coordinator at any time, after which VRF_COORDINATOR.requestRandomWords at line 128 reverts for every epoch, every wall->relay CCIP message lands FAILED on Base, and every 1-day retry repeats the failure at the retrier's cost. The same terminal state follows if Chainlink retires the coordinator, key hash or lane, or never fulfils. The wall's state machine has only two exits from Requested, a delivery (now impossible) or a retry of the same doomed request; there is no sweep, no roll-over of epochPrize, no pro-rata refund and no way to re-point the wall or the relay, yet stampNote keeps taking 1000 NOTES per ticket and adding 500 to pools that can never be paid. README sections 1 and 5 ('no owner, no pause', a stalled CCIP/VRF leg 'delays (never destroys) a prize') and the relay NatSpec trust-model section (lines 22-27) do not mention this liveness role. Merged from three specialists (audit_flow c4bcccc4, audit_economics 9ab0bad5, audit_permissions 289f39e4). Fix options are a design decision for the requester: document the subscription owner as a trusted liveness role and move the subscription to a multisig or non-cancelling contract; and/or add a permissionless wall-side escape hatch that preserves the one-winner design (e.g. after a long timeout in Requested, roll the pool into the next open epoch or let ticket holders reclaim their 500-NOTES share pro rata).

**Reproduction**

State: production pair as deployed. Input: the subscription owner sends removeConsumer(subId, 0x887bbed753938087Ce61Ca768a358848177E6eaA) or cancelSubscription(subId, to) on the Base coordinator 0xd5D517aBE5cF79B7e95eC98dB0f0277788aFF634. Then anyone calls wall.requestSettlement{value: fee}(E) for an ended epoch E with tickets. Expected per README section 5: the stall only delays the prize. Actual: the wall marks E Requested and takes the fee; relay.ccipReceive reverts inside requestRandomWords; the CCIP message is FAILED; every retry after 1 day fails identically; epochPrize[E] stays in the wall forever and no function on either contract can move it or change the subscription, coordinator or relay. Reproduced locally in test/scratch/Guards.t.sol::test_dead_subscription_strands_pool: with a coordinator that reverts InvalidSubscription, the router-delivered request to relay.ccipReceive reverts, relay.deliver(1) reverts NotReady(1), and the wall has no other path out of Requested.

### 3. Low: CCIP_GAS_LIMIT = 300_000 leaves the relay's cached-word retry path (ccipReceive -> _deliver -> getFee + ccipSend) only ~4.7k gas (1.6%) of headroom on the live Base lane

`contracts/IMDRetroWall.sol:145`

```
    uint256 public constant CCIP_GAS_LIMIT = 300_000;
```

The wall fixes the gas the Base off-ramp grants relay.ccipReceive via EVMExtraArgsV2{gasLimit: CCIP_GAS_LIMIT} (line 394). The fresh-request branch is cheap, but the retry branch performs a full CCIP_ROUTER.getFee + CCIP_ROUTER.ccipSend on the production Base router. Two specialists disagreed: audit_flow fc97fcee claimed (from an eth_estimateGas of a cold call from the router) that the branch needs ~313k and always reverts, while audit_economics cc27ad46 claimed it fits with 295,318 gas. I re-ran the faithful simulation (Router.routeMessage from the lane's off-ramp, which is how the message is really executed): the branch succeeds at a 300,000 gas limit using 295,318 gas and fails at 290,000, so the 'always out of gas' claim does not reproduce and its proof (a router double hard-coded to burn 285k) proves nothing about the real router; it is dropped. What remains is that both constants are immutable on the deployed pair and the recovery mechanism the NatSpec and README section 4 rely on has no safety margin against any increase in Chainlink's on-ramp/fee-quoter cost (a lane upgrade, an extra registry read, colder storage for a new sender). When that happens, every wall re-request for an epoch whose word is cached runs out of gas inside the off-ramp: the message is marked FAILED, delivered[epoch] stays false, the wall stays Requested and the re-requester's fee is lost. Nothing is stranded because deliver(epoch) is permissionless and CCIP manual execution with a gas override exists. Fix (needs a redeploy because the value is a constant): size the wall->relay gas limit for the delivery branch with margin (e.g. 500_000; the fee impact is a small fraction of a ~0.000045 ETH message), or make the relay's retry branch only mark/emit and leave sending to deliver().

**Reproduction**

Read-only, reproducible by anyone against Base mainnet with cast: `cast call --rpc-url https://mainnet.base.org --from 0xf09AFe78d3c7d359b334d7cB88995751F7eC5E13 --override-balance 0x887bbed753938087Ce61Ca768a358848177E6eaA:1000000000000000000 --override-state-diff 0x887bbed753938087Ce61Ca768a358848177E6eaA:0xcc69885fda6bcc1a4ace058b4a62bf5e179ea78fd58a1ccd71c22cc9b688792f:0x01,0x887bbed753938087Ce61Ca768a358848177E6eaA:0xe90b7bceb6e7df5418fb78d8ee546e97c83a08bbccc01a0644d599ccd2a7c2e0:0x3039 0x881e3A65B4d4a04dD529061dd0071cf975F58bCD 'routeMessage((bytes32,uint64,bytes,bytes,(address,uint256)[]),uint16,uint256,address)(bool,bytes,uint256)' '(0x11..11,6180753054346818345,<abi.encode(wall)>,<abi.encode(1)>,[])' 5000 <gasLimit> 0x887bbed753938087Ce61Ca768a358848177E6eaA` (the two slots are randomnessReady[1] and randomnessOf[1]; 0xf09A...5E13 is confirmed by router.isOffRamp(6180753054346818345, addr) == true). Results on 2026-10-16: gasLimit 300000 -> success=true, gasUsed=295318; gasLimit 290000 -> success=false, gasUsed=286358; gasLimit 280000 -> success=false. Expected: a documented recovery path should fit its fixed gas budget with margin. Actual: it fits with 4,682 gas to spare, and any increase of the router/on-ramp cost beyond that turns every cached-word retry into a FAILED message with the fee consumed.

### 4. Low: Every wall re-request before the VRF word has arrived issues another paid VRF request for the same epoch; only the first word is used, the rest drain the subscription

`contracts/VrfCcipRelay.sol:128`

```
        uint256 requestId = VRF_COORDINATOR.requestRandomWords(
```

ccipReceive only short-circuits when randomnessReady[epoch] is already true; it has no notion of a request already in flight for the epoch. The wall lets anyone re-request a Requested epoch every SETTLEMENT_RETRY_DELAY (IMDRetroWall.sol:375-378). While fulfilment is pending (README section 6 and RUNBOOK record multi-hour Chainlink fulfiller stalls on the test pairs) each retry costs the caller only the Robinhood->Base CCIP fee but charges the relay's native subscription a full VRF v2.5 request (premium plus up to CALLBACK_GAS_LIMIT callback gas). rawFulfillRandomWords keeps the first word and discards every later one at line 152, so correctness holds, but the subscription (0.0008 ETH funded at the time of writing) pays for each discarded word; once it runs dry requestRandomWords reverts InsufficientBalance, every wall->relay message fails on Base and the epoch stays Requested until someone tops up via the coordinator. Bounded (one extra request per day per pending epoch) and recoverable, so low. Merged from three specialists (audit_flow 747910de, audit_economics d53c62d7, audit_permissions d05350d7). Fix: track a pending request per epoch (e.g. mapping(uint256 => uint256) pendingRequestOf) and return early in ccipReceive when one is outstanding, optionally allowing a fresh request only after a relay-side timeout.

**Reproduction**

State: epoch 1 has one ticket, the epoch has ended, relay and subscription funded. Input: wall.requestSettlement{value: fee}(1) at T (relay emits RandomnessRequested(1, idA)); VRF does not fulfil; wall.requestSettlement{value: fee}(1) again at T+1 day. Expected: no second VRF charge for the same epoch. Actual: relay emits RandomnessRequested(1, idB) and the subscription pays for both; when both are fulfilled the second word is dropped. Reproduced in test/scratch/Guards.t.sol::test_retry_spawns_additional_vrf_requests with MockVRFCoordinator: nextRequestId goes 2 -> 3 after the retry; fulfilling request 2 with 42 then request 1 with 43 leaves randomnessOf(1) == 42.

### 5. Low: Wall ccipReceive accepts a word for an epoch in state None, so a relay-side fault can settle a running epoch and strand every later stamp's pool share

`contracts/IMDRetroWall.sol:426`

```
        if (settlementStatus[epoch] == SettlementStatus.Settled) revert EpochAlreadySettled(epoch);
```

The settlement machine is documented as None -> Requested -> Settled and requestSettlement enforces epoch < currentEpoch() before anything is sent, but ccipReceive only rejects Settled and accepts None, including the current epoch. Today the relay is trusted and only echoes epochs the wall asked for, so this is defence in depth, but the consequence of a relay-side fault (bug, misconfigured pair, replayed message with different data) is permanent: a word for the running epoch k sets Settled, credits the prize accumulated so far and zeroes epochPrize[k]; every stampNote after that in epoch k still adds 500 NOTES to epochPrize[k] and a ticket, yet requestSettlement(k) and ccipReceive(k) both revert EpochAlreadySettled, so those pool shares are stranded forever (no sweep). From audit_math f3aae7d1. Minimal fix: in ccipReceive require settlementStatus[epoch] == SettlementStatus.Requested; Requested is the only state in which a word is legitimately expected, so retries and duplicate deliveries keep working.

**Reproduction**

State: relay set, epoch 1 is the current epoch, alice has stamped once (epochPrize[1]=500e18, settlementStatus[1]=None). Input: the router executes a message with sourceChainSelector=RELAY_CHAIN_SELECTOR, sender=abi.encode(relay), data=abi.encode(1, 777). Expected: revert, epoch 1 was never requested and has not ended. Actual: settlementStatus[1]=Settled, claimable[alice]=500e18, epochPrize[1]=0. Then bob stamps in epoch 1: epochPrize[1]=500e18, ticketCount(1)=2; after the epoch ends requestSettlement(1) reverts EpochAlreadySettled(1) and a second ccipReceive(1) reverts the same way, so bob's 500e18 can never be paid or recovered. Reproduced in test/scratch/Guards.t.sol::test_none_state_epoch_can_be_settled_while_running.

### 6. Low: Production settlement script and README rely on an automatic word forward that the contracts do not perform; settle-prod.ts never calls relay.deliver()

`scripts/settle-prod.ts:168`

```
  console.error("[monitor] timeout without WinnerDrawn — the VRF word never arrived within 24 h; see runbook fallbacks.");
```

VrfCcipRelay.rawFulfillRandomWords (contracts/VrfCcipRelay.sol:145-157) only records the word. The only ways the word reaches the wall are a deliver(epoch) transaction on Base or a second wall requestSettlement(epoch) after SETTLEMENT_RETRY_DELAY. scripts/settle-prod.ts sends requestSettlement(1) and then only polls randomnessReady(1)/delivered(1) and the wall's WinnerDrawn log for 24 h (lines 145-169); it never sends a Base transaction and never re-requests, so delivered(1) cannot become true from the script and the run ends with exit code 3 even when VRF fulfilled within minutes. README section 6 (line 290) states 'the relay forwards the word automatically with its existing CCIP ETH balance and the wall settles', which the code does not do, and the runbook's contingency table has no row for ready=true, delivered=false other than waiting for the 1-day retry. The documented procedure therefore cannot complete epoch 1 inside its own window and costs a second CCIP fee if the retry is used instead of deliver(). From audit_economics 7bc1224b. Fix: once randomnessReady(1) is true have the script (or operator) send relay.deliver(1) on Base, and correct README section 6 and the runbook to say delivery is a separate, permissionless call.

**Reproduction**

Run scripts/settle-prod.ts after 2026-10-19 04:28:50 UTC with 1 ticket in epoch 1 and let VRF fulfil. Expected per README line 290: WinnerDrawn appears on the wall once VRF fulfils. Actual: relay.randomnessReady(1) turns true, relay.delivered(1) stays false (no code path in VrfCcipRelay sets it without a deliver() or wall re-request, and grep of the script shows 'deliver' only as a read at lines 137/146/165), the script prints 'ready=true delivered=false' every 30 s and exits with code 3 at line 168-169 after 24 h; wall.settlementStatus(1) stays Requested until someone calls relay.deliver(1) or pays a second requestSettlement(1) after settlementRequestedAt(1)+1 day.

### 7. Low: EPOCH_DURATION NatSpec, contract header, FACTS.md and the testnet copy say 7 days while the constant and the deployed wall are 3 days

`contracts/IMDRetroWall.sol:133`

```
    /// @notice One epoch lasts exactly 7 days.
```

Line 133 says 'One epoch lasts exactly 7 days' and the header at line 26 says 'per 7-day epoch', but line 134 is `uint256 public constant EPOCH_DURATION = 3 days;` and the production wall 0x9550E4F888d1C084CB1C8E74677Da54109723EE3 returns EPOCH_DURATION()=259200. FACTS.md line 107 ('EPOCH_DURATION = 7 days'), README line 3 and ENTRY.md line 4 ('weekly') and contracts/testnet/IMDRetroWallShortEpoch.sol line 3 ('instead of 7 days') repeat the 7-day figure, while README section 3, FACTS line 26 and the RUNBOOK correctly say 3 days. The epoch length fixes when a stamp stops counting toward a prize, when per-address caps reset and when requestSettlement becomes callable, so anyone reading the explorer-verified source or the docs will be off by four days. Merged from three specialists (audit_flow bbe08591, audit_economics cb59dae3, audit_math 8416c58b). Fix: correct the NatSpec, header and docs to 3 days (or, if 7 days was intended, note that the deployed contract cannot change and document the discrepancy).

**Reproduction**

Read contracts/IMDRetroWall.sol lines 26, 133 and 134 side by side: the comments say 7 days, the constant is 3 days. On the live wall GENESIS=1792124930 (2026-10-16 04:28:50 UTC) and EPOCH_DURATION()=259200, so epoch 1 ends 2026-10-19 04:28:50 UTC, whereas a reader of the NatSpec expects 2026-10-23 04:28:50 UTC; a user who stamps on 2026-10-20 expecting the epoch-1 pool is in epoch 2. Expected: comment, docs and constant agree. Actual: they disagree.

### 8. Info: stampNote accepts tickets and pool funds before setRelay, so the deployer selects the trusted randomness source after money is already at stake

`contracts/IMDRetroWall.sol:323`

```
    function stampNote(
```

stampNote (lines 323-359) has no relay != address(0) precondition; only requestSettlement checks RelayNotSet (line 370). setRelay (lines 298-304) lets DEPLOYER set any address on the Base selector as the sole accepted CCIP sender and ccipReceive then trusts whatever (epoch, randomWord) that sender ships. On a fresh deployment the deployer can wait until tickets and pools exist, then wire a contract they control instead of a VrfCcipRelay and send a chosen word, picking the winner deterministically (index = word % ticketCount). The deployer is already trusted during setup and users can read relay() before stamping, and for the live pair the window is closed (setRelay already points at the verified relay), so this is informational: a hardening gap in the 'ownerless' trust story for new deployments and redeploys. From audit_permissions 19c4afd6. Fix keeping the one-shot design: revert stampNote with RelayNotSet until relay is set, or pass a CREATE2-precomputed relay address to the constructor.

**Reproduction**

Fresh IMDRetroWall with relay unset. alice calls stampNote('hi','#aabbcc',1,1,0) paying 1000 NOTES: succeeds, ticketCount(1)=1, relay()=address(0). Deployer calls setRelay(bob) where bob is any address. After epoch 1 ends the router executes a message with sender=abi.encode(bob), data=abi.encode(1, 0). Expected: tickets are only sold once the randomness source is fixed, or the word must come from a VrfCcipRelay. Actual: ccipReceive accepts it (sender == relay), settles epoch 1 with winnerIndex 0 and credits claimable[alice]=500e18. Reproduced in test/scratch/Guards.t.sol::test_stamp_before_setRelay_then_deployer_chooses_relay.

### 9. Info: first-word-wins and the UnknownRequest guard in rawFulfillRandomWords are not exercised by the Hardhat suite

`contracts/VrfCcipRelay.sol:152`

```
        if (randomnessReady[epoch]) return;
```

test/IMDRetroWall.ts covers NotRouter, UnexpectedSourceChain, UnexpectedSender, NotCoordinator, NotReady, InsufficientBalance and the double-delivery no-op, but no test fulfils a second VRF request for an epoch that already has a word (line 152, the branch that makes a wall retry safe) and no test fulfils an unknown requestId (lines 147-148, UnknownRequest); grep for 'UnknownRequest' in the test file returns nothing and vrf.fulfill is called only once per epoch (lines 169, 371). Both branches behave as intended when exercised (test/scratch/Guards.t.sol::test_retry_spawns_additional_vrf_requests: a later word is dropped and randomnessOf keeps the first). Coverage gap only, no defect. From audit_permissions 8114ac96.

**Reproduction**

Mutation check: change line 152 to `if (false) return;` and run `npx hardhat test`; expected a failing test because a second fulfilment would overwrite the stored word; actual: no test fulfils the same epoch twice, so the suite passes. Likewise deleting `if (epoch == 0) revert UnknownRequest(requestId);` is not caught because no test fulfils an unknown requestId.

---

Judge's submission `af7b627b8b8b8b25863139cf51724fffe7ab8213daf27b563547580ea9f2fe5e`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
