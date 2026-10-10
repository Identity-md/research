# Audit report

> Audit the SvoStaking contract system in this repository (Solidity 0.8.26, Foundry). Primary target: src/SvoStaking.sol. Also in scope: script/DeployStaking.s.sol (run() deploys; fund() is a separate step; the chain, SVO, IMD and the funder Safe are pinned as constants). This is the FINAL audit round: verify the fixes from the previous swarm audit and look for anything those changes introduced. Read for context: src/SovrnToken.sol (the staked SVO token), src/Interfaces.sol (reentrancy Guard), STAKING.md (design notes, trust assumptions, prior audit notes), test/SvoStaking.t.sol, test/DeployStaking.t.sol. Out of scope: src/LifeForceVault.sol, src/SovrnHook.sol and the launch contracts (separately audited). Build/test: forge build && forge test --match-contract "SvoStaking|DeployStaking". Optional fork test: FORK_4663_RPC=https://rpc.mainnet.chain.robinhood.com forge test --match-contract StakingForkTest. Write nothing to the repository; deliver report.md with a machine-readable JSON appendix. Tone: factual; no claims of safety beyond the evidence; no investment language.
>
> DEPLOYMENT CONTEXT. Robinhood Chain, id 4663. SVO = 0x7f7e9b8e9f754c3076e514852552019cb571461b (plain 18-decimal ERC-20, fixed 1B supply, no hooks). Reward token IMD = 0x5F7Bb59365ce557C26dbcAa4EE9d39A4b95B7127 (an ERC-20 with its own single-key owner, blocklist, transfer gate and LayerZero bridge: treat as untrusted). The funder is a Safe v1.5.0 at 0x589A639529220f66a2661A41753e3fd432f48DA0 on 4663 (2-of-3, no modules, no guard). It holds the 100,000,000 SVO founder allocation, will be the immutable funder, will call approve + fund() as a batch and, after 365 days, may call reclaim(). The IMD rewards come from a different Safe (the immutable LifeForceVault's refuel Safe 0xEb57c52272B90F989C41B739e2ccc5f00bF7697C, 2-of-3).
>
> WHAT IT DOES. Stakers stake SVO and earn IMD. IMD is not minted: the refuel Safe sends Solomon's surplus IMD here and anyone calls notify(), which streams all IMD not yet accounted over 7 days, per second, pro rata by stake (Synthetix StakingRewards style). While a stream is running notify() accepts new IMD only if it is at least a tenth of what remains (otherwise it reverts and the IMD waits). Emission while nothing is staked rolls into the next stream. The funder deposits SVO once via fund() as a burn-match pool: matchBurn() is permissionless and burns the same amount again for SVO burned elsewhere (read from the token's totalBurned), limited to a linear 365-day vest, with unmatched burns carried forward. fund() accepts only MIN_FUND (1,000,000 SVO) up to a tenth of the supply, and notify() rejects a stream above MAX_STREAM (1e40 wei). After 365 days the funder may reclaim() the unmatched remainder once (waiting burns are matched first), which closes the pool. unstake() moves only SVO, so a misbehaving IMD can block claim() but never principal. hasAccess(addr) = at least 1,000,000 SVO staked for at least 1 day (a top-up resets the age); an off-chain app uses it to grant 30-minute voice sessions instead of 10. No owner, no pause, no upgradeability; the funder is fixed at deploy.
>
> AUDIT SCOPE. (1) SECURITY: reward accounting (rewardsReserved vs the real balance, rounding and dust, undistributed/leftover double counting, lastUpdate before the first stream and after periodFinish, first/last-staker and zero-staker cases); theft, lock-up or griefing of staked SVO or earned IMD, including third-party donations and notify() timing, sandwiching and the tenth-of-remaining restart rule; burnSnapshot arithmetic (underflow, own-burn handling, forced over-matching, front-running reclaim, vesting boundaries); reentrancy and hostile reward-token behaviour (callbacks, fee-on-transfer, false-returning, blocklisting, destroyed contract, rebasing), confirming staked SVO can never be blocked by IMD; access-tier gaming; funder-only functions including a Safe as funder; any path that moves SVO or IMD other than unstake, claim, matchBurn and reclaim; the deploy script (guards, funder handling, anything that could fund the wrong contract or amount). (2) COMPLIANCE: do code, comments and STAKING.md match behaviour; list every claim the code does not enforce; the launch README (out of scope) says SVO holders receive no payouts and this contract changes that for stakers (the app's stake page and STAKING.md now carry a disclosure: say if it is sufficient; observations, not legal advice); flag centralisation powers (funder reclaim, refuel Safe discretion, IMD owner powers). (3) CODE QUALITY: NatSpec and event accuracy, dead code, unchecked or low-level calls, test gaps.
>
> STANDARDS. SWC Registry; Consensys Smart Contract Best Practices; OWASP Smart Contract Top 10; ERC-20 behaviour including non-standard tokens (compare OpenZeppelin SafeERC20); Synthetix StakingRewards as the reference design (list each deviation and judge it).
>
> FIXED SINCE THE PREVIOUS SWARM AUDIT (job 27aae9c4-e0db-4a83-b551-903d307b3205, commit 6a980ca: no critical, high or medium findings; 3 low, 7 info). Please verify each fix and try to break it, and review the new code for regressions: (1) notify() now rejects total > MAX_STREAM so a reward token reporting an absurd balance cannot overflow the reward math and lock unstake (previous finding 1). (2) fund() now requires MIN_FUND <= amount <= totalSupply/10 so a wrong-unit amount cannot spend the one-time deposit on dust (previous findings 3 and 9). (3) DeployStaking pins CHAIN_ID 4663, SVO, IMD and FOUNDER_SAFE as constants; STAKING_FUNDER must equal FOUNDER_SAFE unless ALLOW_OTHER_FUNDER=true; fund() checks the chain, that the staking contract's token is SVO and its reward token is IMD, and refuses FUND_AMOUNT below MIN_FUND (previous findings 2 and 3). (4) NatSpec now says reclaim() withdraws and notify() restarts; RewardAdded.streamed now reports rate * REWARD_PERIOD; Staked/Unstaked use accountTotal (previous findings 5 to 8). (5) STAKING.md documents the restart cost wording, the funding bounds and the trust assumptions (previous findings 4, 9, 10). Earlier fixes still in place: notify() needs new IMD of at least a tenth of what is left to restart a running stream; claim() reverts if the reward token has no code; reclaim() has AlreadyReclaimed; the constructor rejects rewardToken == token.
>
> KNOWN AND ACCEPTED (do not report as new, but dispute them if you disagree). A burn made just before reclaim() forces the pool to match it, at a cost to the burner equal to the matched amount. With nobody else staked, a staker of any size earns the whole stream. Rewards assume an 18-decimal IMD (per-update rounding is at most totalStaked/1e18 wei and accumulates across updates). The same SVO can rotate across accounts to rent the access tier, about one new account per day. SVO or IMD sent by plain transfer (not stake, fund or notify) is stranded. Small notify() deposits during a running stream wait until the stream ends or the threshold is met. A mid-stream restart is paid for by whoever's IMD is waiting (the threshold is on the whole unaccounted balance) and can be triggered by anyone once it is met; it only delays rewards, nothing is lost. The refuel Safe is trusted to send the surplus, and IMD's single-key owner can blocklist and freeze claims (principal is unaffected).
>
> REPORT FORMAT. Summary with overall risk rating and counts by severity; findings table (ID, severity, category, file:line, title) most severe first; per finding a concrete exploit or failing Foundry test, impact, fix and confidence; what was checked and found fine; assumptions; JSON appendix [{id, severity, category, file, line, title, status}]. No generic advice.

| | |
|---|---|
| Repository | https://github.com/SovrnOne/sovrn-contracts.git |
| Commit | `cfd73aebd3059ae31b8fc252e34bda2ccf6b485f` |
| Job | `36b2abd5-7aa4-4924-9236-59ea60642f13` |
| Judged | 2026-10-10 18:09 UTC |
| Findings | 1 low · 7 info |

Four agents audited the code as it is at `cfd73ae`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: DeployStaking.fund() accepts any FUND_AMOUNT inside the contract bounds without an explicit override, so an in-bounds typo fixes the one-time burn-match pool at the wrong size

`script/DeployStaking.s.sol:60`

```
        uint256 amount = vm.envOr("FUND_AMOUNT", DEFAULT_FUND);
```

The swarm-audit fix pinned the chain, SVO, IMD and the funder, and made fund() refuse amounts below MIN_FUND, but the amount itself is still free: any FUND_AMOUNT between MIN_FUND (1e24) and totalSupply/10 (1e26) passes the script's only amount check at line 65 and the contract's bounds at src/SvoStaking.sol:165. fund() is one-time (matchStart != 0 reverts AlreadyFunded), so an amount that is wrong but in bounds, for example 1e25 (one zero short of the intended 100,000,000 SVO), permanently sizes the pool at a tenth of the founder allocation; the remaining SVO can never be added and stays as plain SVO with the funder. DEFAULT_FUND (line 33) exists but only fills in when the variable is unset; it does not pin the value the way FOUNDER_SAFE pins the funder. The NatSpec at lines 16-17 tells the operator to check matchTotal() afterwards, which is after the irreversible step. The production path (a Safe batch of approve + fund) bypasses the script and has only the contract bounds, so the Safe instructions carry the same residual risk. Merged from audit_flow. Confidence: high (reproduced). Fix: require(amount == DEFAULT_FUND || vm.envOr("ALLOW_OTHER_AMOUNT", false), "FUND_AMOUNT is not 100,000,000 SVO") in the script, and in the Safe-batch NatSpec state the exact calldata fund(100000000000000000000000000) and that a Safe simulation should assert matchTotal() == 1e26 before signing. Pinning 1e26 in the contract itself would change the agreed design (the bounds were chosen deliberately) and is not proposed.

**Reproduction**

test/scratch/Judge.t.sol JudgeScriptTest.test_staleAllowOtherFunderAndTypoAmount (passes on the current code, demonstrating the behaviour): chain id 4663, stand-in SVO/IMD at the pinned addresses, STAKING_CONTRACT = a fresh SvoStaking with funder = DEFAULT_SENDER, FUND_AMOUNT=10000000000000000000000000 (1e25); script.fund() succeeds and s.matchTotal() == 1e25; a second fund() with FUND_AMOUNT=9e25 reverts 'already funded'. Contract level: JudgeTest.test_fundAcceptsTypoAmountAndCannotBeToppedUp: s.fund(1e25) succeeds, s.fund(9e25) reverts AlreadyFunded. Expected (by analogy with the funder pin): refusal of an amount other than 100,000,000 SVO unless explicitly overridden. Actual: accepted and irreversible.

### 2. Info: A stale ALLOW_OTHER_FUNDER=true in the shell silently disables the pinned founder-Safe check in run(); the funder is immutable

`script/DeployStaking.s.sol:44`

```
        require(funder == FOUNDER_SAFE || vm.envOr("ALLOW_OTHER_FUNDER", false), "funder is not the founder Safe");
```

The founder-Safe pin has a boolean escape hatch read with vm.envOr, so it needs no value on the command line and survives from an earlier rehearsal in the same shell (test/DeployStaking.t.sol:60 sets exactly this). With it set, run() deploys SvoStaking with whatever STAKING_FUNDER says as the immutable funder that holds reclaim() of the 100M SVO pool. Impact is bounded: the mis-deployed contract is unfunded, the Safe's fund() would revert Unauthorized (msg.sender != funder), and the deployer can redeploy; the cost is a wasted deployment and an address that must not be published to the app. Merged from audit_permissions. Confidence: high (reproduced). Fix: make the override name the address it permits, e.g. require(funder == FOUNDER_SAFE || vm.envOr("ALLOW_OTHER_FUNDER", address(0)) == funder, ...), so a leftover value cannot apply to a different funder, and log a prominent warning when the override is used.

**Reproduction**

test/scratch/Judge.t.sol JudgeScriptTest.test_staleAllowOtherFunderAndTypoAmount: vm.setEnv("ALLOW_OTHER_FUNDER","true") and STAKING_FUNDER = DEFAULT_SENDER (an EOA); script.run() succeeds and s.funder() == DEFAULT_SENDER != FOUNDER_SAFE. Expected per the pin's stated intent (NatSpec lines 9-10: a wrong env var cannot point a deployment at another funder): refusal. Actual: deployed with the EOA as permanent funder. test/DeployStaking.t.sol:60-63 shows the same acceptance.

### 3. Info: NatSpec and STAKING.md say the stake-age reset stops stake-wait-unstake rental of the tier; the code permits exactly that pattern

`src/SvoStaking.sol:28`

```
///      MIN_STAKE_AGE old. Adding to a stake restarts the age, which stops stake-wait-unstake rental of the tier.
```

hasAccess(a) is staked[a] >= MIN_STAKE && block.timestamp >= stakedSince[a] + MIN_STAKE_AGE and unstake() has no delay or cooldown. Resetting stakedSince on every stake() only prevents pre-staging a dust stake and topping it up for instant access. A plain stake-wait-unstake cycle (stake 1,000,000 SVO, wait one day, use the tier, unstake the same second, move the SVO to another account and repeat) is allowed, and STAKING.md:69-71 itself accepts that rotation. The header comment at line 28 and STAKING.md:85 ('Adding to a stake restarts its age (stops stake-wait-unstake rental of the tier)') therefore describe a protection the code does not provide; they should describe the one it does. Compliance item (a claim the code does not enforce), no funds affected. Merged from audit_flow. Confidence: high (reproduced). Fix: reword both to 'Adding to a stake restarts its age, so a pre-staged dust stake cannot be topped up for instant access; the tier can be held by any account that keeps MIN_STAKE staked for a day and released at once.' If rental is actually meant to be stopped, an unstake delay would be needed, which is a design change.

**Reproduction**

test/scratch/Judge.t.sol JudgeTest.test_stakeWaitUnstakeRentalIsPermitted (passes): alice.stake(1_000_000 ether); hasAccess false; skip(1 days); hasAccess true; alice.unstake(1_000_000 ether) succeeds in the same block, balance restored, hasAccess false; alice transfers the same 1,000,000 SVO to bob; bob.stake; skip(1 days); hasAccess(bob) true. Expected per line 28: the stake-wait-unstake rental is stopped. Actual: permitted, with the only cost a one-day lock.

### 4. Info: Error names misdescribe two failure paths: a failed balanceOf query reverts TransferFailed and bad constructor arguments revert Unauthorized

`src/SvoStaking.sol:278`

```
        if (!ok || data.length < 32) revert TransferFailed();
```

_rewardBalance() (used by notify() and the unnotified() view) reverts with TransferFailed when the reward token's balanceOf staticcall fails or returns fewer than 32 bytes, although no transfer was attempted. The constructor (lines 86 and 89) reverts with Unauthorized for a token or reward token without code, a zero funder, or rewardToken == token, although no authorization is involved. Off-chain tooling and the app decoding the custom error will attribute the wrong cause (a 'failed transfer' while diagnosing a reward token that lost its code or reverts on balanceOf). Code quality only; no funds affected. The vault (out of scope) uses the same TransferFailed-for-balanceOf convention, so if it is kept on purpose a one-line NatSpec note would do. Merged from audit_flow. Confidence: high (reproduced). Fix: add error BalanceQueryFailed() for line 278 and error InvalidArgument() for lines 86 and 89, or document the reuse.

**Reproduction**

test/scratch/Judge.t.sol JudgeTest.test_balanceQueryFailureRevertsTransferFailed: deploy with a working stand-in IMD, vm.etch(address(imd), "") (a destroyed reward token), then s.notify() and s.unnotified() both revert TransferFailed(). JudgeTest.test_badConstructorArgsRevertUnauthorized: new SvoStaking(svo, address(svo), funder) and new SvoStaking(svo, imd, address(0)) both revert Unauthorized(). Expected: an error naming the balance query / invalid argument. Actual: TransferFailed / Unauthorized.

### 5. Info: STAKING.md does not say that a blocklisted staker's earned IMD stays reserved in the contract with no exit, or that blocking the contract freezes every later deposit while notify() keeps succeeding

`STAKING.md:45`

```
  `setBlocked(address,bool)`. If that key blocks this contract or a staker, `claim()` reverts for them. Staked SVO is
```

Trust-assumption precision, not a code defect; the design has no owner and no sweep by choice, and the on-chain IMD owner can indeed call setBlocked (checked by eth_call on chain 4663: a call from the owner succeeds, from another address reverts OwnableUnauthorizedAccount). STAKING.md:45 says claim() 'reverts for them'. It does not say what then happens to the IMD: a blocked staker's earned[] balance remains counted in rewardsReserved indefinitely, is never redistributed to other stakers, cannot be reclaimed by the funder or the refuel Safe, and leaves only if the block is lifted. If the IMD owner blocks the staking contract itself, every later Safe deposit that notify() accounts is likewise frozen while notify() keeps succeeding (balanceOf still answers), so the refuel Safe would keep sending surplus into a frozen contract unless it checks blocked(staking) first. The Safe-timing point raised by audit_permissions (the Safe decides when the surplus is sent, and the staker set at that moment earns it) is already covered by the accepted 'Safe decides when' and 'sole staker earns the whole stream' items and is not repeated. Merged from audit_permissions. Confidence: high (reproduced). Fix: add to the IMD-owner bullet: 'IMD earned by a blocked staker stays in the contract, counted as reserved, until the block is lifted; it is not redistributed and no one can withdraw it. If the contract itself is blocked, the Safe should stop sending surplus until the block is lifted.'

**Reproduction**

test/scratch/Judge.t.sol JudgeTest.test_blockedStakerRewardsStayReservedForever (passes): alice and bob each stake 1,000,000 SVO, 700 IMD streamed over a week with a blocklisting stand-in IMD; owner blocks bob; bob.claim() reverts TransferFailed; alice.claim() succeeds; pendingRewards(bob) is about 350 IMD, rewardsReserved equals it (plus dust) and equals the contract's IMD balance; notify() reverts InvalidAmount (nothing new to stream); bob.unstake() returns principal; 3650 days later rewardsReserved and pendingRewards(bob) are unchanged. Expected per STAKING.md: claim reverts for them (true). Actual in addition: the IMD is stranded for as long as the block lasts, which the document does not state.

### 6. Info: README's 'SVO holders receive no payouts, rewards or returns' is unqualified and has no pointer to STAKING.md, so the staking disclosure only reaches readers who open STAKING.md or the app's stake pag

`README.md:3`

```
Trading fees from the launch's SVO/IMD pool fund the inference of a voice AI. All hook fees, collected only in IMD (an ERC-20), go to one immutable LifeForceVault: 70% is earmarked for inference and 30% for manually buying SVO to burn. The vault never swaps; the REFUEL_SAFE withdraws each reserve and the operators act by hand. SVO holders receive no payouts, rewards or returns.
```

Observation on the disclosure the brief asked about, not legal advice. STAKING.md:3-6 and its 'Known properties' and 'Trust assumptions' sections disclose clearly that SVO stakers earn IMD from Solomon's overflow, that rewards can be zero, that no audit is claimed, and the IMD-owner, refuel-Safe and funder powers; that is sufficient for anyone who reads STAKING.md (the app's stake page is outside this repository and was not reviewed). README.md:3 states 'SVO holders receive no payouts, rewards or returns' with no qualifier, README.md contains no occurrence of 'staking', 'stake' or 'STAKING.md' (the only 'stak' hit is unrelated, line 67), and README.md is hashed by launch-attestation.json (line 53), so it cannot be amended without changing the attestation. A reader who only sees the README, the document the launch attestation points to, is not told that a separate deployed contract pays IMD to SVO holders who stake. The README is out of scope as code; the point is the reach of the disclosure. Merged from audit_flow and audit_permissions (duplicates). Confidence: high (reproduced). Fix: where the attestation allows, add a one-line pointer to STAKING.md in the launch-facing page that is not hashed (the app's /tokenomics or stake page), and keep STAKING.md's wording that the README statement applies to the launch contracts only; if the README is ever re-attested, qualify the sentence there.

**Reproduction**

grep -n -i 'stak' README.md returns only line 67 (unrelated to staking); README.md:3 ends 'SVO holders receive no payouts, rewards or returns.'; grep -n README launch-attestation.json shows README.md hashed at line 53. Expected: the only distribution to SVO holders is disclosed wherever the no-payout statement is made, or that statement points to where the exception is described. Actual: the exception is documented only in STAKING.md.

### 7. Info: Test gaps: zero-staker mid-stream with re-staking, reclaim with nothing left, false-returning and re-entering reward token, partial unstake keeping access, run() token-identity guards and burn-match f

`test/SvoStaking.t.sol:138`

```
    function test_brokenIMDBlocksClaimButNeverPrincipal() public {
```

test/SvoStaking.t.sol (29 tests) and test/DeployStaking.t.sol cover the happy paths, every previous audit fix and a reverting IMD, but not: (a) every staker unstaking mid-stream and someone staking again before periodFinish, i.e. the totalStaked == 0 branch of _updateGlobal() taken in the middle of a stream and the undistributed amount re-streamed by the next notify(); (b) reclaim() when the pool is fully matched (returned == 0, the pool still closes); (c) a reward token whose transfer returns false or returns no data (the abi.decode branch at src/SvoStaking.sol:126); (d) a reward token that re-enters stake/unstake/claim/notify from transfer() during claim() (the Guard is the only defence and claim's state is written before the call); (e) hasAccess() surviving a partial unstake above MIN_STAKE and failing once the stake drops below it; (f) DeployStaking.run() refusing an SVO with the wrong totalSupply or symbol (script lines 39-40; the test only etches the SVO code away); (g) any fuzzing of the burn-match arithmetic (burnSnapshot += 2 * matched and the vesting cap) across two burn/match rounds. All of these behave correctly: the scratch file in this review exercises (a)-(e) and (g) and they pass, so no defect is claimed; a regression in any of them would pass CI. The audit_permissions claim that fund()/reclaim() are never called from a contract account is dropped: the test contract itself is the funder in test/SvoStaking.t.sol, which is the same msg.sender shape as a Safe's execTransaction. Merged from audit_flow and audit_permissions (duplicates). Confidence: high. Fix: add the listed tests (test/scratch/Judge.t.sol in this review can be adopted under test/).

**Reproduction**

forge test --match-contract SvoStakingTest --list and reading test/SvoStaking.t.sol: no test calls unstake() for every staker while block.timestamp < periodFinish and then stake() again before periodFinish; no test asserts reclaim() == 0; BrokenIMD only reverts and HugeBalanceIMD only returns true, none returns false, void or calls back; no test unstakes part of a stake above MIN_STAKE and reads hasAccess; DeployStakingTest never changes SVO's totalSupply() or symbol(); no fuzz test funds the pool. test/scratch/Judge.t.sol test_gap_* and testFuzz_burnMatchNeverOverMatches pass on the current code (2000 fuzz runs for the burn-match invariant: matchUsed <= external burns, matchUsed <= vested, matchUsed + unmatchedBurns == external burns, contract SVO == matchTotal - matchUsed).

### 8. Info: Documentation accuracy: STAKING.md cites 222 tests (236 are listed) and names only one of the two staking test files; the matchAvailable overflow comment cites a 1e27 bound that fund() now caps at 1e2

`STAKING.md:79`

```
  now reports what is actually streamed; `Staked`/`Unstaked` use `accountTotal`. **These last fixes were tested (222 tests,
```

Three code-and-doc mismatches, none affecting behaviour. (1) STAKING.md:79 says the swarm fixes 'were tested (222 tests, plus a dry run against the live chain)'; forge test --list at cfd73ae enumerates 236 tests, so the number is stale or counted differently. (2) STAKING.md:89 lists test/SvoStaking.t.sol only; test/DeployStaking.t.sol holds the offline deploy-and-fund script test and the StakingForkTest against the real IMD (the task's optional fork test), which a reader assessing coverage would want to know about. (3) src/SvoStaking.sol:221 justifies no overflow with 'matchTotal <= 1e27'; after the fund() bound at line 165 matchTotal is at most totalSupply/10 = 1e26, so the comment is true but no longer states the enforced bound. Merged from audit_permissions. Confidence: high (reproduced). Fix: replace the fixed test count with the command that produces it (or update to 236), list both test files, and change the comment to 'matchTotal <= totalSupply/10 = 1e26'.

**Reproduction**

forge test --list | grep -cE '^\s+test' at cfd73ae prints 236 (STAKING.md:79 says 222). STAKING.md:89 reads '- Tests: `test/SvoStaking.t.sol` (unit, a misbehaving-IMD case, fuzz solvency).' with no mention of test/DeployStaking.t.sol. src/SvoStaking.sol:165 enforces amount <= token.totalSupply() / 10 = 1e26 while line 221's comment says matchTotal <= 1e27.

---

Judge's submission `13e6387f90b3cfbb27a77b0030681d49ce52e15775ad8e05943b5790de8a64d1`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
