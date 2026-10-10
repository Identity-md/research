# Audit report

> Audit the SvoStaking contract system in this repository (Solidity 0.8.26, Foundry). Primary target: src/SvoStaking.sol. Also in scope: script/DeployStaking.s.sol (run() deploys; fund() is a separate step). Read for context: src/SovrnToken.sol (the staked SVO token), src/Interfaces.sol (reentrancy Guard), STAKING.md (design notes, trust assumptions, prior audit notes), test/SvoStaking.t.sol, test/DeployStaking.t.sol. Out of scope: src/LifeForceVault.sol, src/SovrnHook.sol and the launch contracts (separately audited). Build/test: forge build && forge test --match-contract "SvoStaking|DeployStaking". Optional real-chain test: FORK_4663_RPC=https://rpc.mainnet.chain.robinhood.com forge test --match-contract StakingForkTest. Write nothing to the repository; deliver report.md with a machine-readable JSON appendix. Tone: factual and plain; no claims of safety beyond the evidence; do not call the contracts audited or secure; no investment language.
>
> DEPLOYMENT CONTEXT. Robinhood Chain, id 4663. SVO = 0x7f7e9b8e9f754c3076e514852552019cb571461b (plain 18-decimal ERC-20, fixed 1B supply, no hooks). Reward token IMD = 0x5F7Bb59365ce557C26dbcAa4EE9d39A4b95B7127 (an ERC-20 with its own single-key owner, blocklist, transfer gate and LayerZero bridge: treat as untrusted). The funder is a Safe v1.5.0 at 0x589A639529220f66a2661A41753e3fd432f48DA0 on 4663 (2-of-3, no modules, no guard; owners 0xa71Fb297aa443aDfc22Ff74981D8C067ec3475Cb, 0x217C05f5D1D1E595BBae94534540B803bfC4563B, 0xb1eC9d1C36974d05eb9889eBf8A150b05791E559). It holds the 100,000,000 SVO founder allocation, will be the immutable funder, will call approve + fund() as a batch and, after 365 days, may call reclaim(). The IMD rewards come from a different Safe (the immutable LifeForceVault's refuel Safe 0xEb57c52272B90F989C41B739e2ccc5f00bF7697C, 2-of-3).
>
> WHAT IT DOES. Stakers stake SVO and earn IMD. IMD is not minted: the refuel Safe sends Solomon's surplus IMD here and anyone calls notify(), which streams all IMD not yet accounted over 7 days, per second, pro rata by stake (Synthetix StakingRewards style). While a stream is running notify() accepts new IMD only if it is at least a tenth of what remains (otherwise it reverts and the IMD waits). Emission while nothing is staked rolls into the next stream. The funder deposits SVO once via fund() as a burn-match pool: matchBurn() is permissionless and burns the same amount again for SVO burned elsewhere (read from the token's totalBurned), limited to a linear 365-day vest, with unmatched burns carried forward. After 365 days the funder may reclaim() the unmatched remainder once (waiting burns are matched first), which closes the pool. unstake() moves only SVO, so a misbehaving IMD can block claim() but never principal. hasAccess(addr) = at least 1,000,000 SVO staked for at least 1 day (a top-up resets the age); an off-chain app uses it to grant 30-minute voice sessions instead of 10. No owner, no pause, no upgradeability; the funder is fixed at deploy.
>
> AUDIT SCOPE. (1) SECURITY: reward accounting (rewardsReserved vs the real balance, rounding and dust, undistributed/leftover double counting, lastUpdate before the first stream and after periodFinish, first/last-staker and zero-staker cases); theft, lock-up or griefing of staked SVO or earned IMD, including third-party donations and notify() timing, sandwiching and stream manipulation, and whether the tenth-of-remaining rule can itself be abused; burnSnapshot arithmetic (underflow, own-burn handling, forced over-matching, front-running reclaim, vesting boundaries); reentrancy and hostile reward-token behaviour (callbacks, fee-on-transfer, false-returning, reverting or blocklisting IMD, destroyed contract, rebasing), confirming staked SVO can never be blocked by IMD; access-tier gaming; funder-only functions including a Safe as funder; any path that moves SVO or IMD other than unstake, claim, matchBurn and reclaim; the deploy script (wrong-chain and wrong-token guards, funder handling, anything that could fund the wrong contract or amount). (2) COMPLIANCE: do code, comments and STAKING.md match behaviour; list every claim the code does not enforce (for example the contract cannot pull the surplus out of the vault, so the refuel Safe sending it is a trust assumption); the launch README (outside this scope) says SVO holders receive no payouts, rewards or returns and this contract changes that for stakers, so say what disclosures a project in this position usually needs (observations, not legal advice); flag centralisation powers (funder reclaim, refuel Safe discretion, IMD owner powers). (3) CODE QUALITY: NatSpec and event accuracy, custom errors, naming, dead code, gas, unchecked or low-level calls, and test gaps with the tests you would add.
>
> STANDARDS. SWC Registry; Consensys Smart Contract Best Practices; Solidity Style Guide; OWASP Smart Contract Top 10; ERC-20 (EIP-20) behaviour including non-standard tokens, compared with OpenZeppelin SafeERC20 conventions; Synthetix StakingRewards / Uniswap staker reward semantics as the reference design (list each intentional deviation and judge whether it is safe).
>
> FIXED SINCE EARLIER REVIEWS (verify the fixes and try to break them). notify() could be called for free to stretch a running stream (now needs new IMD of at least a tenth of what is left). claim() now reverts if the reward token has no code. reclaim() has its own AlreadyReclaimed error and unmatchedBurns() is 0 after reclaim. The constructor rejects rewardToken == token. DeployStaking requires an explicit STAKING_FUNDER (no default) and fund() checks the chain, that the staking contract's token is SVO_TOKEN and that its reward token is IMD. STAKING.md now lists the trust assumptions. A prior external review of commit 8a3222d found no critical or high issues; its low findings were: fund() trusting STAKING_CONTRACT, two funded matchers matching each other's burns, the IMD owner freezing claims, rewardToken == token, stretching a stream for a tenth of the remainder, and weak token identity checks in the script.
>
> KNOWN AND ACCEPTED (do not report as new, but dispute them if you disagree). A burn made just before reclaim() forces the pool to match it, at a cost to the burner equal to the matched amount. With nobody else staked, a staker of any size earns the whole stream. Rewards assume an 18-decimal IMD (per-update rounding is at most totalStaked/1e18 wei and accumulates across updates). The same SVO can rotate across accounts to rent the access tier, about one new account per day. SVO or IMD sent by plain transfer (not stake, fund or notify) is stranded. Small notify() deposits during a running stream wait until the stream ends or the threshold is met. Restarting a running stream costs the donor a tenth of the remainder in real IMD and only delays rewards.
>
> REPORT FORMAT. 1) Summary: overall risk rating, finding counts by severity, top 3 issues. 2) Findings table sorted most severe first: ID | Severity (Critical/High/Medium/Low/Info) | Category (Security/Compliance/Quality) | Location (file:line) | Title. 3) Per finding: description, a concrete exploit or failure scenario with numbers or a call sequence (a failing Foundry test is ideal), impact, a suggested fix, and confidence (Confirmed / Likely / Possible). 4) 'Checked and found fine': the properties verified. 5) Assumptions and out-of-scope items relied on. 6) Machine-readable appendix: findings as JSON [{id, severity, category, file, line, title, status}]. No generic advice. If you ran code, include the commands or test files.

| | |
|---|---|
| Repository | https://github.com/SovrnOne/sovrn-contracts.git |
| Commit | `6a980ca8ba27066464df586a9298b8e3e025d319` |
| Job | `27aae9c4-e0db-4a83-b551-903d307b3205` |
| Judged | 2026-10-10 16:32 UTC |
| Findings | 3 low · 7 info |

Four agents audited the code as it is at `6a980ca`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Hostile reward-token balance overflows _updateGlobal and permanently locks unstake(), contradicting the 'never principal' guarantee

`src/SvoStaking.sol:256`

```
        else rewardPerTokenStored += emitted * PRECISION / totalStaked;
```

notify() sets rewardsReserved and rewardRate from whatever rewardToken.balanceOf(this) returns, with no upper bound (lines 131-143). stake(), unstake() and claim() all run _update() -> _updateGlobal(), which computes emitted * PRECISION in checked arithmetic. If the reported balance makes emitted between two updates exceed about 1.16e59 wei, every _updateGlobal reverts with panic 0x11. lastUpdate never advances and after periodFinish emitted is fixed at (periodFinish - lastUpdate) * rewardRate, so the state cannot recover: unstake() reverts forever and all staked SVO is locked. This contradicts SvoStaking.sol:16-17 and STAKING.md:29 ('an IMD that misbehaves can block claim but never stakers' principal'): the guarantee rests on the reward token's supply bound, not on the code. Reachability with the deployed IMD (0x5F7B...7127, checked with cast against rpc.mainnet.chain.robinhood.com): totalSupply 5.47e22, decimals 18, no EIP-1967 implementation slot, no mint(address,uint256)/mint(uint256) selector in the bytecode, LayerZero OFT credits are bounded by uint64 shared-decimal units (~1.8e31 wei). The threshold cannot realistically be reached with this IMD, so severity is Low. Merged from audit_permissions (26b99a63) and audit_flow (5f75fe26); both attached proofs fail on this code with panic 0x11.

**Reproduction**

Reward token whose balanceOf(staking) returns 1e66 (or 1e61). alice stakes 5,000,000 SVO; anyone calls notify() (rewardRate = 1e66 / 604800 ~= 1.65e60 per second); warp 1 second; alice.unstake(5_000_000e18). Expected: alice receives 5,000,000 SVO (unstake moves only SVO). Actual: revert panic(0x11) in _updateGlobal at line 256, and at every later timestamp. Reproduced: forge test --match-path test/scratch/Proof_5f75fe261cb5.t.sol -> [FAIL: panic: arithmetic underflow or overflow (0x11)]. Fix: in notify() revert if total > type(uint256).max / PRECISION / REWARD_PERIOD (or a much tighter cap such as 1e40), and/or give unstake() a path that does not depend on reward math (e.g. an exit that forfeits accrual when _update would revert).

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;
import {Test} from "forge-std/Test.sol";
import {SovrnToken} from "src/SovrnToken.sol";
import {SvoStaking} from "src/SvoStaking.sol";

/// A reward token whose balanceOf can be made to report an absurd balance (hostile, compromised, or buggy IMD).
contract HostileIMD {
    uint256 public fake;
    function setFake(uint256 f) external { fake = f; }
    function balanceOf(address) external view returns (uint256) { return fake; }
    function transfer(address, uint256) external pure returns (bool) { return true; }
}

contract HostileBalanceTest is Test {
    SovrnToken svo;
    HostileIMD imd;
    SvoStaking s;
    address alice = address(0xA11CE);

    function setUp() public {
        svo = new SovrnToken();
        imd = new HostileIMD();
        s = new SvoStaking(svo, address(imd), address(this));
        svo.transfer(alice, 10_000_000 ether);
        vm.startPrank(alice);
        svo.approve(address(s), type(uint256).max);
        s.stake(5_000_000 ether);
        vm.stopPrank();
    }

    /// STAKING.md / NatSpec: "an IMD that misbehaves can block claim but never stakers' principal".
    function test_hostileRewardBalanceMustNotLockPrincipal() public {
        imd.setFake(1e66);              // reported balance only; no real tokens needed
        try s.notify() {} catch {}       // permissionless: rewardRate = 1e66 / 604800 ~= 1.65e60 per second (a fix may reject this)
        vm.warp(block.timestamp + 1);    // emitted * 1e18 ~= 1.65e78 > 2^256 -> checked overflow in _updateGlobal
        uint256 before = svo.balanceOf(alice);
        vm.prank(alice);
        s.unstake(5_000_000 ether);      // currently reverts with panic 0x11, forever
        assertEq(svo.balanceOf(alice) - before, 5_000_000 ether);
    }
}
```

### 2. Low: DeployStaking pins IMD but not SVO: any SovrnToken clone passes run(), fund() checks against the same env var, and EXPECT_CHAIN_ID disables the chain guard

`script/DeployStaking.s.sol:34`

```
        require(SovrnToken(svo).totalSupply() == 1_000_000_000 ether, "SVO_TOKEN is not SVO");
```

run() identifies SVO only by totalSupply == 1e27 and symbol == 'SVO' (lines 34-35). Both are compile-time constants of SovrnToken, so every SovrnToken deployment passes (the repository's own test/DeployStaking.t.sol deploys a fresh SovrnToken and runs the script). The canonical SVO 0x7f7e9b8e9f754c3076e514852552019cb571461b is never compared, although IMD is pinned as a constant on line 26. fund() (line 58) only compares staking.token() with the same SVO_TOKEN env var, so a wrong SVO_TOKEN is self-consistent across both steps and nothing catches it. The chain guard (lines 30 and 52) compares against vm.envOr('EXPECT_CHAIN_ID', 4663), so a leftover EXPECT_CHAIN_ID turns it off; IMD is a LayerZero OFT and may have code at the same address on other chains, so the IMD code check does not pin the chain either. STAKING_FUNDER is not compared with the intended Safe 0x589A...8DA0. Impact: an immutable staking contract bound to the wrong token, chain or funder can be deployed and published to the app without any guard firing; real SVO is not taken, but stakers of the wrong token are. Merged from audit_permissions (2071ea37), audit_math (3687bb79), audit_flow (67ea3f89) and audit_economics (8dbaaa5b).

**Reproduction**

chainid 4663, SVO_TOKEN=<address of a freshly deployed SovrnToken>, STAKING_FUNDER=<any address>: script.run() succeeds and staking.token() == the impostor (expected: revert 'SVO_TOKEN is not SVO'); with STAKING_CONTRACT set to it, script.fund() also succeeds with matchTotal == 100_000_000e18 of the impostor. chainid 1 with EXPECT_CHAIN_ID=1 and code at the IMD address: script.run() deploys (expected: revert 'wrong chain'). Reproduced: forge test --match-path test/scratch/DeployGuards.t.sol (test_deployScriptGuards passes, demonstrating both). Fix: add constants SVO = 0x7f7e9b8e9f754c3076e514852552019cb571461b, CHAIN_ID = 4663 and FUNDER = 0x589A639529220f66a2661A41753e3fd432f48DA0; require svo == SVO in run() and staking.token() == SVO in fund(); drop the EXPECT_CHAIN_ID override or allow it only together with an explicit test-only flag.

### 3. Low: FUND_AMOUNT in whole units (1e8 wei) passes the script and the contract floor; the one-shot fund() slot is then spent on a dust pool

`script/DeployStaking.s.sol:54`

```
        uint256 amount = vm.envOr("FUND_AMOUNT", DEFAULT_FUND);
```

The script reads FUND_AMOUNT as a raw uint with no plausibility floor, and the contract's only floor (src/SvoStaking.sol:156, amount < MATCH_DURATION) is 31,536,000 wei, chosen so the pool vests at least 1 wei per second. An operator who sets FUND_AMOUNT=100000000 (whole SVO instead of wei) passes every script check (chain, token, reward token, funder, balance) and the contract check, and funds the burn-match pool with 100,000,000 wei = 1e-10 SVO. fund() is one-shot (matchStart != 0 reverts AlreadyFunded), so the real 100,000,000 SVO allocation can never be deposited into that deployment; STAKING_CONTRACT must be redeployed and re-pinned in the app. The same wrong-unit value is what a Safe batch would carry if the amount is typed in whole units in the Safe UI, and the Safe path (approve + fund batch, as the script comments recommend) bypasses the script checks entirely. No value is lost (the funder keeps its SVO; the dust is reclaimable after 365 days), but the deployment is unrecoverable. STAKING.md:14 'up to 10% of supply' is not enforced in either direction. Merged from audit_math (9fe986dd) and audit_economics (10550100).

**Reproduction**

Env: SVO_TOKEN=<SovrnToken>, STAKING_FUNDER=<broadcaster>, STAKING_CONTRACT=<deployed SvoStaking>, FUND_AMOUNT=100000000. Expected: refused as implausible (default is 100000000000000000000000000). Actual: fund() succeeds, staking.matchTotal() == 100000000 (wei), svo.balanceOf(staking) == 100000000, and a following staking.fund(100_000_000 ether) from the funder reverts AlreadyFunded(). Contract boundary: fund(31_535_999) reverts InvalidAmount, fund(31_536_000) succeeds. Reproduced: forge test --match-path test/scratch/DeployGuards.t.sol (test_deployScriptGuards). Fix: in the script require amount == DEFAULT_FUND unless an explicit override env is set, or require amount >= 1 ether && amount % 1 ether == 0 and print the amount in whole SVO; optionally raise the contract floor in fund() (e.g. 1 ether) since 31,536,000 wei only guarantees 1 wei/s vesting.

### 4. Info: Tenth-of-remaining rule counts IMD already waiting, so a third party can restart a running stream for the shortfall or for free

`src/SvoStaking.sol:140`

```
        if (leftover != 0 && (added == 0 || added < leftover / 10)) revert InvalidAmount();
```

Disputes the wording of an accepted item. `added` is the whole unaccounted balance, not the caller's own transfer. STAKING.md:13 and the audit notes say restarting a running stream 'costs the donor a tenth of the remainder in real IMD'; in practice the cost is borne by whoever's IMD is already waiting (normally a sub-threshold refuel-Safe deposit), and the restart is then triggered by any address either for the shortfall only or for nothing once leftover has decayed to ten times the waiting amount. Nothing is lost (the same restart would happen on the Safe's next deposit), but it is a timing lever any third party holds whenever a deposit is waiting: the remainder is re-spread over a fresh 7 days and the per-second rate drops. Merged from audit_math (e94afd98) and audit_economics (84f0cde1).

**Reproduction**

alice stakes 1,000,000 SVO; 7000 IMD notified (1000/day). At day 6 leftover ~= 1000 IMD; the Safe sends 99 IMD: notify() reverts (99 < 100). mallory sends 1 IMD and calls notify(): succeeds, added = 100, periodFinish = now + 7 days, rewardRate = 1100/7 days; alice's next-day accrual is ~157 IMD instead of ~1000. Restart cost to mallory: 1 IMD (0.1% of the remainder). Zero-cost variant: 2000 IMD stream, Safe sends 100 at t0 (waits), at t0 + 3.5 days leftover = 1000 and notify() from 0xBAD succeeds, rate falls 45%. Reproduced: forge test --match-path test/scratch/Boundaries.t.sol (test_waitingDepositLetsThirdPartyRestartForTheShortfall, test_waitingDepositLetsAnyoneRestartForFree). Fix (design choice): reword STAKING.md ('costs whoever's IMD is waiting; anyone may trigger it once the threshold is met'), or measure the threshold against IMD sent since the last successful notify by a recorded source, or restrict mid-stream restarts to the refuel Safe.

### 5. Info: Contract NatSpec says 'no withdraw of the pools' but reclaim() withdraws the unmatched match pool to the funder

`src/SvoStaking.sol:9`

```
/// @dev No owner, no upgrade path, no withdraw of the pools.
```

The contract-level summary contradicts reclaim() (lines 174-185), which sends matchTotal - matchUsed SVO to the funder once, 365 days after fund(); with no burns that is the full 100,000,000 SVO. Lines 22-24 of the same comment and STAKING.md describe reclaim correctly; a reader of the summary line or verified source gets a stronger guarantee than the contract enforces and misses the funder's main power. Merged from audit_permissions (1f26c4ce), audit_math (92244a63), audit_economics (4d6f9ece) and audit_flow (33716e9d).

**Reproduction**

fund(100_000_000e18); warp 365 days; no burns; funder calls reclaim(). Expected per line 9: no path moves pool SVO to anyone but DEAD. Actual: reclaim() returns 100,000,000 SVO to the funder (test/SvoStaking.t.sol::test_reclaimOnlyFunderOnlyAfterAYearOnlyOnce and test/scratch/Boundaries.t.sol::test_reclaimWithdrawsWholePoolToFunder). Fix: 'No owner, no upgrade path; the only withdrawal is the funder's one-time reclaim() of the unmatched match pool after MATCH_DURATION.'

### 6. Info: notify() NatSpec says 'extend' but a successful mid-stream notify restarts the stream and lowers the current rate

`src/SvoStaking.sol:125`

```
    /// @notice Start (or extend) the stream with IMD that has arrived since the last call. Anyone may call.
```

notify() sets periodFinish = now + 7 days and rewardRate = (added + leftover + undistributed) / 7 days. The leftover is re-spread over a fresh period, so the per-second rate can fall sharply rather than merely be extended. The test name test_secondOverflowExtendsStreamWithoutLosingLeftover repeats the wording. From audit_economics (93b593c1) and audit_flow (33716e9d, second part).

**Reproduction**

alice stakes 1,000,000 SVO; 7000 IMD stream (1000/day). At day 6 (leftover 1000) notify with 100 new IMD: rewardRate becomes 1100e18 / 604800 ~= 157/day for 7 days, less than a sixth of the previous rate. A reader of 'extend' expects 1000/day to continue plus more. Reproduced: forge test --match-path test/scratch/Boundaries.t.sol (test_notifyRestartsAtLowerRate). Fix: 'Start (or restart over a new REWARD_PERIOD, with what is left plus the new IMD) the stream ...'.

### 7. Info: RewardAdded.streamed reports `total`, which includes rounding dust that is not streamed this period

`src/SvoStaking.sol:147`

```
        emit RewardAdded(added, total, rewardRate, periodFinish);
```

notify() computes rewardRate = total / REWARD_PERIOD and carries the remainder (up to 604,799 wei) in `undistributed` for the next stream, but the event's `streamed` field is `total`, so every RewardAdded over-reports what the period emits by the dust, and the dust is reported again in the next RewardAdded. Off-chain sums of `streamed` drift from rewardRate * REWARD_PERIOD sums and from totalNotified. No on-chain effect. Merged from audit_permissions (a6638d28) and audit_math (c01414e7).

**Reproduction**

One staker; send 700e18 IMD and call notify(). rewardRate = 700e18 / 604800 = 1157407407407407; rewardRate * 604800 = 699999999999999753600; the event emits streamed = 700000000000000000000 (246,400 wei more than is streamed) and undistributed() == 246400 afterwards. Reproduced: forge test --match-path test/scratch/Boundaries.t.sol (test_rewardAddedStreamedIncludesUnstreamedDust). Fix: emit rewardRate * REWARD_PERIOD as streamed (and optionally the carried dust), or rename the field to `total`.

### 8. Info: Staked/Unstaked event field 'total' is the account's stake, not totalStaked

`src/SvoStaking.sol:63`

```
    event Staked(address indexed account, uint256 amount, uint256 total);
```

stake() and unstake() emit staked[msg.sender] in a field named 'total' (lines 97 and 107). The contract also exposes a public totalStaked, so an indexer that reads 'total' as the pool total gets wrong numbers. From audit_flow (0a1e9a92).

**Reproduction**

alice stakes 1,000,000e18, then bob stakes 2,000,000e18. Bob's Staked event has total = 2,000,000e18 while totalStaked = 3,000,000e18. Reproduced: forge test --match-path test/scratch/Boundaries.t.sol (test_stakedEventTotalIsAccountStake). Fix: rename the field to accountTotal (or emit totalStaked as well).

### 9. Info: STAKING.md says the pool is 'up to 10% of supply'; fund() enforces only amount >= 365 days in wei

`STAKING.md:14`

```
| Burn-match pool | `fund(amount)`, once, only by the `funder` set at deploy (the founder's SVO, up to 10% of supply); vests linearly over `MATCH_DURATION` (365 days) |
```

fund() (src/SvoStaking.sol:156) checks only amount >= MATCH_DURATION (31,536,000 wei). The 10% bound and the 100,000,000 SVO figure are funder commitments, not contract properties; the matching rate per second and what reclaim() returns both scale with whatever is funded. From audit_permissions (e2a9ae7a).

**Reproduction**

A funder holding 200,000,000 SVO calls fund(200_000_000e18): succeeds, matchTotal == 200_000_000e18 (20% of supply); a fresh contract accepts fund(31_536_000) as a 365-wei-per-day pool. Expected per the doc: at most 100,000,000 SVO. Reproduced: forge test --match-path test/scratch/Boundaries.t.sol (test_fundAcceptsMoreThanTenPercentAndDust). Fix: enforce a bound (amount <= token.totalSupply() / 10) or state in STAKING.md that the amount is chosen by the funder and is verifiable only from the Funded event / matchTotal.

### 10. Info: Compliance observation: staking changes the README's 'no payouts, rewards or returns' position for SVO holders and the disclosures around it are partial

`STAKING.md:4`

```
covered by `README.md`, whose statement that the *launch contracts* pay SVO holders nothing stays true of the token, hook and
```

Observation, not legal advice. README.md:3 states 'SVO holders receive no payouts, rewards or returns' and does not mention this contract; STAKING.md only says the README statement covers the launch contracts. With SvoStaking, staking SVO yields IMD pro rata from a project-controlled Safe's discretionary transfers, and the founder pool burns SVO. Projects in this position usually disclose, where users actually read: that rewards are discretionary and may be zero indefinitely (the Safe is not obliged on chain); the IMD owner's blocklist and transfer-gate powers over claims; the funder's one-time reclaim of up to the whole pool after a year; that burn-matching is not a value or price commitment; and a pointer from the README to STAKING.md so the two statements are reconciled. From audit_economics (eb5e1726).

**Reproduction**

State: a user reads README.md:3 ('SVO holders receive no payouts, rewards or returns'), stakes 1,000,000 SVO, the Safe sends IMD and anyone calls notify(); after 7 days the user's claim() pays IMD (test/SvoStaking.t.sol::test_overflowStreamsToStakersOverAWeek). The README contains no reference to SvoStaking or STAKING.md (grep -n 'staking' README.md returns nothing). Fix: add a linked disclosure section to README.md and the app's staking page covering the points above.

---

Judge's submission `7ed4f1eadc66759030d4cae1058ce92ed0ce512cd4a8ef56bb81f6ec03470634`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
