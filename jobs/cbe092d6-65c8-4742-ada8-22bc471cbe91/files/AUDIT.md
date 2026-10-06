# Audit report

> Project: PepesFamily launchpad v4, final check after 348884ab
> Repo: github.com/0xtenang/PepesFamily (commit 5d3fbb0)
> Scope: contracts/src/PepesFamily.sol, contracts/src/PadToken.sol, contracts/src/PepesFamilyEthRouter.sol
> Tests: contracts/test/PepesFamily.t.sol, contracts/test/Fork.t.sol
>
> Change: PepesBuyback is removed. PadToken.recycle(holder) now sends expired rewards to pad.feeRecipient(), read at call time. The team buys back and burns $PEPES manually (a trust assumption, documented). Expiry, activity rules (claim, buy via hook markActive, send, own pull, first receipt) and the ETH router hookData are unchanged from 2560653.
>
> Please check
>
> Is recycle still bounded to expired rewards only, and is the token always solvent?
> Any risk in reading feeRecipient from the pad at recycle time (owner changes it, zero address, reverts)?
> Did removing the buyback leave anything inconsistent: constructor, docs, tests?
> Any regression of earlier findings, or of v3 guarantees.

| | |
|---|---|
| Repository | https://github.com/0xtenang/PepesFamily.git |
| Commit | `5d3fbb0463752698899a21eab4d43fd16d0d60a8` |
| Job | `cbe092d6-65c8-4742-ada8-22bc471cbe91` |
| Judged | 2026-10-06 16:30 UTC |
| Findings | 2 low · 3 info |

Four agents audited the code as it is at `5d3fbb0`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: A gift received after a distribution shields another wallet's old rewards from expiry, contradicting the stated 'nobody can keep another wallet's rewards from expiring' guarantee

`contracts/src/PadToken.sol:311`

```
        uint256 recent = FullMath.mulDivRoundingUp(magnifiedDividendPerShare - magCut, balanceOf[holder], MAGNITUDE);
```

Merged from audit_economics 1fd9e673, audit_math 936fd392, audit_permissions a7dcd037 and case (a) of audit_flow 9e1b675b; all four reproduce. expiredRewardsOf() protects the 'recent' part as (magnifiedDividendPerShare - magAt(now - 7d - 1)) x balanceOf[holder], using the holder's balance NOW. Tokens a third party sends to an inactive wallet after a distribution inside the window are therefore counted as if they had earned that distribution for the recipient, although the sender keeps those rewards (transfers move only future rewards). Since b803125e a gift no longer resets lastActive, but the balance term still lets a large enough gift shrink, or zero, the amount recycle() can send to feeRecipient. The code comment at lines 307-309 acknowledges the over-estimate 'in the holder's favour', while the contract notice (line 21) and README 'Activity' promise an absolute guarantee that does not hold. Bounds verified: recycle() never moves more than expiredRewardsOf(), the token stays solvent, and the shield is temporary: once a full window has passed since the gift (no newer distributions), all of the old rewards expire (checked: at T0 + 13 days + 1 expiredRewardsOf(bob) equals bob's whole withdrawable). The gifter irrevocably parts with the tokens and the inactive wallet could have claimed anyway, so no profit path was found; the impact is a false documented guarantee and delayed/reduced recycle revenue. Fix is a design decision: (1) document the limitation in the PadToken notice and README ('a gift never resets the timer but tokens received without activity delay expiry of up to balance x per-share growth of the last 7 days'); or (2) change the estimate so rewards on gifted tokens count only from receipt. Caution on (2): the simplest variant, snapshotting activeBalance at each activity and using min(balanceOf, activeBalance) as proposed by audit_permissions, makes the attached proof and the 53 suite tests pass but breaks the other stated guarantee 'what it earned during those last 7 days never expires': under that patch my ground-truth fuzz (test/scratch/Probe.t.sol::testFuzz_recycleBoundedAndSolvent, run against a patched copy outside the repo) found recycle taking 5.518 IMD when only 0.560 IMD had been distributed before the cutoff, because rewards earned inside the window on tokens received as gifts were expired. A correct code fix needs per-receipt accounting (amount and magnifiedDividendPerShare at receipt for gifts since the last activity), which is a larger change. The attached proof pins option (2); if the requester chooses option (1) it should be dropped. Either way add a regression test: the suite's gift tests only exercise gifts with no distribution inside the window.

**Reproduction**

Commit 5d3fbb0, Foundry, mock IMD, start mcap 100 IMD (test/scratch/GiftShield.t.sol, the audit_permissions proof, re-run here). T0: bob buys 10 IMD, carol buys 50 IMD; bob (sole holder at flush time) is owed 1799999999999999999 wei. T0 + 6d: alice buys 200 IMD (6 IMD distributed over bob and carol); bob's real window earnings are 1430462255459255159 wei. Then carol transfers her whole balance to bob; t.lastActive(bob) is unchanged (T0). T0 + 7d + 1s: expected per the NatSpec, expiredRewardsOf(bob) ~= 1.8 IMD (everything earned before the window). Actual: expiredRewardsOf(bob) == 0 and recycle(bob) sends 0 to feeRecipient, because recent = (mag - magCut) x (bobBal + carolBal) ~= 6 IMD > 1.8 IMD withdrawable; carol still has her ~4.57 IMD withdrawable. `forge test --match-path test/scratch/GiftShield.t.sol -vv` fails with 'old rewards must expire despite the gift: 0 !~= 1799999999999999999'. Same shape with carol gifting half her bag (audit_economics: expired 599999999999999999 -> 0) and with a 45% gift (audit_math: 32.999 IMD -> 18.956 IMD).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/src/PoolManager.sol";
import {PepesFamily} from "src/PepesFamily.sol";
import {PepesFamilyRouter} from "src/PepesFamilyRouter.sol";
import {PadToken} from "src/PadToken.sol";
import {DeployLib} from "script/DeployLib.sol";

contract ScratchIMD {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    function mint(address to, uint256 amt) external {
        balanceOf[to] += amt;
    }

    function approve(address s, uint256 amt) external returns (bool) {
        allowance[msg.sender][s] = amt;
        return true;
    }

    function transfer(address to, uint256 amt) external returns (bool) {
        balanceOf[msg.sender] -= amt;
        balanceOf[to] += amt;
        return true;
    }

    function transferFrom(address f, address to, uint256 amt) external returns (bool) {
        if (allowance[f][msg.sender] != type(uint256).max) allowance[f][msg.sender] -= amt;
        balanceOf[f] -= amt;
        balanceOf[to] += amt;
        return true;
    }
}

/// A gift received after a distribution inflates the recipient's "recent" rewards and shields old rewards
/// from expiry, although the NatSpec says tokens someone else sends can't keep another wallet's rewards
/// from expiring.
contract GiftShieldTest is Test {
    address constant FEE_RECIPIENT = 0x3c8A4d94B3219F6633F2cC94094f4765b30c691C;
    PoolManager pm;
    PepesFamily pad;
    PepesFamilyRouter router;
    ScratchIMD imd;
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");
    address carol = makeAddr("carol");

    function setUp() public {
        vm.warp(1_800_000_000);
        pm = new PoolManager(address(this));
        imd = new ScratchIMD();
        bytes memory initCode = abi.encodePacked(
            type(PepesFamily).creationCode,
            abi.encode(
                pm,
                address(imd),
                address(this),
                FEE_RECIPIENT,
                DeployLib.startTickForMarketCap(100e18),
                PepesFamily.ImdEthPool(10_000, 100, address(0))
            )
        );
        (bytes32 salt, address expected) = DeployLib.mineSalt(address(this), uint160(0x28CC), initCode, 0);
        address deployed;
        assembly {
            deployed := create2(0, add(initCode, 0x20), mload(initCode), salt)
        }
        require(deployed == expected, "hook address");
        pad = PepesFamily(deployed);
        router = PepesFamilyRouter(payable(pad.router()));
        address[3] memory users = [alice, bob, carol];
        for (uint256 i; i < users.length; i++) {
            imd.mint(users[i], 1_000_000e18);
            vm.prank(users[i]);
            imd.approve(address(router), type(uint256).max);
        }
    }

    function _buy(address who, PadToken t, uint256 amt) internal returns (uint256) {
        vm.prank(who);
        return router.buy(address(t), amt, 0, block.timestamp);
    }

    function test_giftAfterDistributionShieldsOldRewardsFromExpiry() public {
        vm.prank(alice);
        PadToken t = PadToken(payable(pad.launch("Test", "TST", "", address(imd))));
        _buy(bob, t, 10e18);
        _buy(carol, t, 50e18); // day 0: bob (sole holder) earns 0.3 + 1.5 IMD
        uint256 oldRewards = t.withdrawableDividendOf(bob);
        assertApproxEqAbs(oldRewards, 1.8e18, 10);
        uint256 lastBob = t.lastActive(bob);

        vm.warp(block.timestamp + 6 days);
        _buy(alice, t, 200e18); // day 6: 6 IMD spread over bob and carol
        uint256 bobRecentReal = t.withdrawableDividendOf(bob) - oldRewards;

        // Day 6, after the distribution: carol gifts bob her whole balance. Not bob's activity.
        uint256 carolBal = t.balanceOf(carol);
        vm.prank(carol);
        t.transfer(bob, carolBal);
        assertEq(t.lastActive(bob), lastBob, "a gift is not bob's activity");
        uint256 carolKeeps = t.withdrawableDividendOf(carol);
        assertGt(carolKeeps, 0, "carol keeps what she earned on those tokens");

        vm.warp(lastBob + 7 days + 1); // bob inactive for more than 7 days
        // Expected: everything bob earned before day 6 (1.8 IMD) has expired; only `bobRecentReal` is protected.
        // Actual: the gifted tokens are counted as if they had earned for bob during the window, so the
        // protocol receives nothing at recycle.
        uint256 expired = t.expiredRewardsOf(bob);
        emit log_named_uint("old rewards (should expire)", oldRewards);
        emit log_named_uint("bob's real recent rewards  ", bobRecentReal);
        emit log_named_uint("expiredRewardsOf(bob)      ", expired);
        assertApproxEqAbs(expired, oldRewards, 1e6, "old rewards must expire despite the gift");
        uint256 got = t.recycle(bob);
        assertEq(got, expired);
        assertApproxEqAbs(imd.balanceOf(FEE_RECIPIENT), oldRewards, 1e6);
    }
}
```

### 2. Low: Expiry is lazy: claim() pays rewards that have already expired unless someone called recycle() first, so the protocol's share depends on an undocumented keeper

`contracts/src/PadToken.sol:286`

```
        amount = withdrawableDividendOf(msg.sender);
```

From audit_economics 368ce461; reproduced. The contract notice says 'Rewards of a wallet inactive for more than 7 days expire' and README says expired rewards go to the protocol address, but expiry only takes effect when an unprivileged caller runs recycle()/recycleMany(). claim() resets lastActive and then pays the full withdrawableDividendOf(), expired part included; nothing in the contracts or tests asserts what claim() does on a wallet whose expiredRewardsOf() > 0. Consequences: (1) the recyclable revenue exists only if the team runs a recycler bot, which is not stated anywhere in README, AUDIT.md or the NatSpec (the sibling $EARN web copy does say 'You can still claim it until someone recycles it', so lazy expiry looks intended); (2) a holder who notices can always claim first, deterministically on Robinhood Chain's sequencer. No user funds are at risk, so low. Fix: if lazy expiry is the design, document it in the PadToken notice and README together with the keeper assumption, and add a test for claim() on an expired wallet; if strict expiry is wanted, compute expiredRewardsOf(msg.sender) in claim() before the lastActive reset and route that part to feeRecipient with the same accounting as recycle(), which keeps the bound and solvency properties.

**Reproduction**

test/scratch/Probe.t.sol::test_claimIgnoresExpiry (passes on this code, showing the behaviour). Launch; bob buys 10 IMD, carol buys 10 IMD (bob owed 599999999999999999 wei); warp +60 days with no activity; expiredRewardsOf(bob) == 599999999999999999 (all of it). bob calls claim(). Expected under the stated rule: at most the recent part (0) is paid and 0.6 IMD goes to feeRecipient. Actual: claim() returns 599999999999999999 to bob, imd.balanceOf(feeRecipient) stays 0 and totalRecycled stays 0.

### 3. Info: AUDIT.md still describes v3: feeRecipient's role omits expired holder rewards, owner powers and invariant 4 do not mention recycle, scope and test count are stale

`AUDIT.md:83`

```
| `feeRecipient` | Receives protocol fees | Anything else |
```

Merged from audit_math da18616d, audit_flow b3538cf4, audit_permissions 3d2b9b67 and the AUDIT.md part of audit_economics 26910b3a; all verified by reading the file against the code. AUDIT.md is the brief handed to reviewers, and no v4 commit touched it. At 5d3fbb0 it is contradicted by the code in four places: (1) line 83 says feeRecipient receives protocol fees and 'Anything else' is impossible, while PadToken.recycle (contracts/src/PadToken.sol:325) now pays every v4 token's expired holder rewards to IPadFlush(pad).feeRecipient(), read at call time; (2) line 82 says the owner cannot touch holder rewards, but setFeeRecipient now chooses where expired holder rewards go, including (owner trust assumption, verified in test/scratch/Probe.t.sol::test_ownerCanRedirectExpiredRewardsToToken) to the token itself, where the next distribute() spreads them to current holders instead of the manual buyback; README 'Owner powers' (line 184) was updated, AUDIT.md was not; (3) invariant 4 'Reward solvency' (line 138) lists claims as the only outflow and does not mention totalRecycled, so it cannot be checked as written against v4 (the correct statement is accountedBalance = distributed - claimed - recycled <= quote.balanceOf(token), with recycle bounded by expiredRewardsOf); (4) line 18 says 'In scope: v3' and line 218 says '34 unit + attack tests' while forge test runs 111 (53 in PepesFamily.t.sol alone), and sections 5 and 9 have no entry for expiry/recycle/activity. Removing PepesBuyback left no code inconsistency: constructor arity, Deploy.s.sol, both fork tests and the unit suite match the new wiring (111 tests pass offline), no reference to PepesBuyback or poke remains in the launchpad sources, tests or script, and MockPepes/MockPepesRouter in test/Mocks.sol belong to the live $EARN tests. Fix: add a v4 section to AUDIT.md (actor: anyone; destination: feeRecipient only, read at call time; manual buyback as a trust assumption as README line 83 states; owner can redirect it with setFeeRecipient), extend the owner and feeRecipient rows and invariant 4, and refresh scope and test counts.

**Reproduction**

Read AUDIT.md line 83 ('feeRecipient | Receives protocol fees | Anything else'), line 82 (owner cannot touch holder rewards), line 138 (invariant 4) and line 218 ('34 unit + attack tests'). Then: launch a v4 token, bob buys 10 IMD, carol buys 10 IMD, warp +8 days, anyone calls t.recycle(bob): IMD owed to a holder leaves the token to pad.feeRecipient(); after the owner calls pad.setFeeRecipient(treasury) a second token's recycle pays treasury instead (existing test test_expiry_goesToCurrentFeeRecipient: e1 to FEE_RECIPIENT, e2 to treasury). With setFeeRecipient(address(t)) recycle(bob) returns the owed amount, imd.balanceOf(t) is unchanged, accountedBalance drops by it and t.distribute() returns that amount to current holders. `forge test` reports 111 passed, not 34.

### 4. Info: README build/deploy section describes the pre-v4 deployment: wrong output file name, an ETH_START_MCAP option the script never reads, stale test counts

`README.md:153`

```
The owner defaults to `0x3c8A…691C`, and any wallet can pay for the deployment (about 0.0003 ETH). The script mines the hook salt, deploys through the standard CREATE2 factory, and writes `deployments/robinhood.json`.
```

From the README part of audit_economics 26910b3a; verified against contracts/script/Deploy.s.sol. (a) README line 153 says the script writes deployments/robinhood.json and line 178 tells the website operator to copy pad/router/block from that file, but Deploy.s.sol line 68 writes deployments/robinhood-v4.json (robinhood.json in the tree is an older deployment record); (b) README line 161 lists ETH_START_MCAP (default 1.5e18) as a deploy option, but v4 is IMD-only and Deploy.s.sol reads only IMD_START_MCAP, OWNER and SALT_START (SALT_START is not listed); (c) README lines 138-139 say '34 unit + attack tests' and '+ 7 fork tests' while PepesFamily.t.sol alone has 53 tests and forge test runs 111 offline; (d) README line 188 says the owner cannot add quote assets 'other than ETH and IMD' while v4 launches are IMD-only. None of this affects on-chain behaviour; it can mislead whoever deploys v4 or wires the website to the deployment file. Fix: update the Deploy and Test sections for the v4 script (robinhood-v4.json, IMD_START_MCAP/OWNER/SALT_START, current counts).

**Reproduction**

grep -n ETH_START_MCAP contracts/script returns nothing (Deploy.s.sol lines 27-28 read only IMD_START_MCAP and OWNER, line 44 SALT_START); Deploy.s.sol line 68 is vm.writeJson(out, "./deployments/robinhood-v4.json"). Expected per README: the ETH start cap is applied and deployments/robinhood.json is (re)written. Actual: the variable is never read and a different file is written. `cd contracts && forge test` prints '111 tests passed', not 34.

### 5. Info: Expiry test coverage gap: no stateful ground-truth check that recycle only takes rewards older than 7 days; gift inside the window and zero-fee 1 wei buy untested

`contracts/test/PepesFamily.t.sol:853`

```
    function testFuzz_expirySolvent(uint96 a, uint96 b, uint32 gap1, uint32 gap2) public {
```

Merged from audit_math cdc5ec75 and audit_flow 9e1b675b; verified by reading the suite and by writing the missing checks as scratch tests (not kept). The central v4 guarantee, 'recycle can only ever move rewards that have expired', is pinned only by fixed sequences: testFuzz_expirySolvent runs buy(bob), warp, buy(carol), warp, buy(alice), one recycle(bob), two claims; it never recycles twice, never claims before a recycle, never sells, never gifts, never changes a holder's balance between the buys and the recycle, and never flushes third-party-router fees late. The hand-written cases (day 0/5/8/10/13) use a 1e6 wei tolerance. A regression that takes a few wei of recent rewards, or a change like the activeBalance patch discussed in the gift finding (which expires rewards earned inside the window on gifted tokens), would pass the suite unchanged: I confirmed the 53 tests still pass against such a patched copy while my ground-truth fuzz fails on it. Two behaviours the code relies on are also unexercised: (a) the 'recent over-estimate in the holder's favour' for a gift received during the window (PadToken.sol:307-309), and (b) an exact-in buy of 1 wei IMD through a third-party router, whose fee is 0 (1 * 400 / 10000; _chargeFee returns early) but which still calls markActive(tx.origin) in afterSwap, so the 'a buy of any size counts' rule is not pinned. Both behave as documented on the current code. Separately, 31 lines in this file compute vm.warp(block.timestamp + ...) or read block.timestamp after a warp; forge lint flags this under via_ir because the compiler may reuse an earlier block.timestamp read (my own probe captured a wrong t0 this way until switched to vm.getBlockTimestamp()). The suite currently passes, but a timing test can silently check the wrong instant after an unrelated edit. Suggested additions: a stateful fuzz that records, per holder and distribution, balance x delta(magnifiedDividendPerShare) with its timestamp and asserts on every recycle that expired <= sum of rewards at or before now - 7d - 1 net of withdrawals (+2 wei), withdrawable after == owed - expired, and solvency; a gift-in-window test asserting expired <= r1, withdrawable == owed - expired and solvency; a 1 wei external buy test asserting fee == 0 and lastActive updated; and vm.getBlockTimestamp() in the timing tests.

**Reproduction**

Current suite: `forge test --match-test testFuzz_expirySolvent` only runs the fixed 3-buy/1-recycle sequence above; grep shows no test that transfers tokens to a holder between a distribution and a recycle, none with amountSpecified = -1, and no per-distribution ground truth. Scratch evidence on 5d3fbb0: test/scratch/Probe.t.sol::testFuzz_recycleBoundedAndSolvent (random router buys, partial sells, gifts, external buys with tx.origin set, warps, flushes, claims, recycles over up to 40 actions; asserts recycle == expiredRewardsOf, recycle <= rewards distributed at or before now-7d-1 net of withdrawals + 2 wei, withdrawable after == owed - expired, imd.balanceOf(token) >= accountedBalance, sum of withdrawable <= accountedBalance) passes 2000 runs on the current code and fails within 11 runs on the activeBalance-patched copy ('only rewards older than 7 days: 5518562966114463113 > 560066326748174097'). test_oneWeiExternalBuyMarksActiveWithZeroFee: quote as currency0, bob (vm.prank(bob, bob)) swaps amountSpecified = -1 via PoolSwapTest 6 days after his buy: pendingProtocolFees and pendingHolderFees unchanged, lastActive(bob) == block.timestamp, expiredRewardsOf(bob) == 0 six days later.

---

Judge's submission `95e8b3a67c51edc7dd38badd661e7c161adcaabac0f75db76656bcf446b9d003`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
