# Audit report

> Scope is the msft95-contracts-audit-v4/ folder only. The README’s “look hardest at” section already covers this round’s changes.

| | |
|---|---|
| Repository | https://github.com/DrTatum/MSFT95.git |
| Commit | `6aa52313d9d8210fb296d8d97eaa2c0ffa6b62f9` |
| Job | `6af15c5b-019c-497a-9f24-e7b15366601d` |
| Judged | 2026-10-24 08:11 UTC |
| Findings | 1 medium · 4 low · 2 info |

Four agents audited the code as it is at `6aa5231`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Launch split skips the 200,000,000 MSFT95 liquidity transfer when LP_WALLET and TREASURY resolve to the same address (the mainnet default), leaving 20% of supply on the deployer key

`msft95-contracts-audit-v4/scripts/mainnet/lib.js:256`

```
      if (parts.liquidity[0].toLowerCase() !== me.toLowerCase() && !(await has(parts.liquidity[0], parts.liquidity[1]))) await send(m.transfer(parts.liquidity[0], parts.liquidity[1]));
```

Merged from audit_permissions and audit_flow (same root cause, same fix). The review-5 idempotency fix (AUDIT-5 L-4) decides whether each part of the supply split has already been paid by checking whether the destination already holds at least that part: `has(who, amt) = balanceOf(who) >= amt` (line 253). That is only sound when every destination is a distinct wallet holding nothing else. `config()` (line 57) defaults TREASURY, LP_WALLET, TEAM and OPS to SAFE, and docs/MAINNET.md section 0 explicitly allows the wallets to be 'separate addresses or the Safe'. With the defaults the treasury transfer on line 255 sends 250,000,000 MSFT95 to the Safe, and the liquidity check on line 256 then sees the Safe holding 250,000,000 >= 200,000,000 and skips the transfer. The step records itself as done (rec.steps.split) and prints the normal summary with liquidity: {to: SAFE, amount: 200000000.0}, so a re-run does not repair it; handover() only transfers ownership. Result: the Safe receives 250,000,000 instead of 450,000,000 and the deployer EOA keeps 200,000,000 MSFT95 (20% of supply, the whole launch-liquidity allocation) after handover, contradicting README 'The deployer ends up owning nothing' and leaving the Safe unable to add the launch position until someone moves the tokens by hand with the deployer key. The same mis-skip fires for any two parts that share a wallet, or for any destination that already holds MSFT95 for another reason. rehearse.js uses five distinct wallets (line 42), so its check on line 76 never exercises the default. Fix: record each transfer as its own sub-step (or by tx hash) in the launch record instead of inferring it from balances, or compute the expected balance per destination as the sum of all parts routed to that address; and assert at the end of split() that the deployer holds exactly AGENT_STAKE.

**Reproduction**

Reproduced by replaying lines 244-256 with the defaults (TREASURY and LP_WALLET unset, so both equal SAFE) and the deployer holding 950,000,000 after the vesting step: economy 250,032,300 -> vault; treasury 250,000,000 -> SAFE; then has(SAFE, 200,000,000) is true, so the liquidity transfer is skipped. Expected after split: balanceOf(SAFE) = 450,000,000e18, balanceOf(deployer) = 249,967,700e18. Actual: balanceOf(SAFE) = 250,000,000e18, balanceOf(deployer) = 449,967,700e18; after agentStakes and handover the deployer still holds 200,000,000e18 MSFT95 while steps.split is recorded as done. Minimal live reproduction: in rehearse.js set LP_WALLET: treasury.address (or run launch.js with SAFE set and TREASURY/LP_WALLET unset); the check 'liquidity: 200,000,000 to the LP wallet' (rehearse.js line 76) and 'the deployer keeps nothing' (line 78) fail.

### 2. Low: Launch `vesting` step cannot be resumed once VEST_DELAY has elapsed: MSFT95Vesting.fund() reverts AfterStart and the recorded address is never replaced, so the 5% allocation stays on the deployer

`msft95-contracts-audit-v4/scripts/mainnet/lib.js:209`

```
      if (have < amt) { await send(m.approve(v.target, amt - have)); await send(v.fund(amt - have)); }
```

Merged from audit_permissions, audit_flow and audit_economics (one mechanism). The step deploys MSFT95Vesting with start = latest.timestamp + VEST_DELAY (default 3600 s, line 203), saves the address at once (line 205) and on every run tops up amt - total() through v.fund(). MSFT95Vesting.fund() refuses any deposit once block.timestamp >= start (v4/MSFT95Vesting.sol line 60) and the contract has no owner or other funding path. If the run stops between the deploy and the fund transaction (RPC error, out of gas, operator interruption, sequencer pause) and is resumed more than an hour later, every retry reverts, rec.steps.vesting is never set, and because A().vesting is pinned the script never deploys a fresh schedule. The launch cannot continue past step 2 without hand-editing deployments/<net>Launch.json, which is the manual intervention the resume logic (AUDIT-5 L-4) was meant to remove; meanwhile 50,000,000 MSFT95 sit on the deployer key. agentStakes resume has no such time bound. Fix (keeps the design): when A().vesting is recorded, total() < amt and block.timestamp >= v.start(), log the stale address and deploy a fresh MSFT95Vesting instead of calling fund(); or fund in the same transaction as the deploy via a small deployer contract; or pick a VEST_DELAY long enough for any plausible resume and assert it up front.

**Reproduction**

Foundry test test/scratch/VestingResume.t.sol (passes, demonstrating the revert): deploy MSFT95Staking and MSFT95Vesting(token, staking, ops, start = block.timestamp + 3600, 365 days) with total() == 0; warp 3660 s (a resume 61 minutes later); replay line 208-209: have = total() = 0, approve 50,000,000e18, v.fund(50,000,000e18). Expected (what the resume assumes): total() == 50,000,000e18. Actual: fund reverts with AfterStart(), total() stays 0, and no later call can ever fund this contract; the step throws identically on every rerun.

### 3. Low: Launch `route` step crashes instead of skipping when ALLOW_NO_FEED=1 and a live USDG/MSFT pool exists: routeProblem() builds the feed contract from an empty MSFT_FEED

`msft95-contracts-audit-v4/scripts/mainnet/lib.js:351`

```
  const feed = new ethers.Contract(cfg.MSFT_FEED, ["function latestRoundData() view returns (uint80,int256,uint256,uint256,uint80)", "function decimals() view returns (uint8)"], signer);
```

audit_flow. config() allows a mainnet launch with no Chainlink feed when ALLOW_NO_FEED=1 (MSFT_FEED is then '', line 61) and the `feed` step handles that case by logging and skipping (line 180). The `route` step does not: with no ROUTE given, findRoute() (line 168) finds the deepest live USDG/MSFT v4 pool (anyone can create one), and line 170 calls routeProblem(), which unconditionally constructs new ethers.Contract(cfg.MSFT_FEED, ...) with the empty string and calls latestRoundData(). ethers v6 treats a non-address string target as an ENS name; the call rejects with UNCONFIGURED_NAME, so the step throws after the token, hook and pool have been created and while the deployer still owns the token and hook. Every resume hits the same throw until the operator sets ROUTE explicitly, which the message on line 172 never gets to print. Fix: in routeProblem(), when cfg.MSFT_FEED is empty, return a reason such as 'no MSFT feed to check the price against: set ROUTE explicitly' so the route is skipped and the fees wait for the Safe, instead of building the feed contract.

**Reproduction**

Reproduced the throwing call: with ethers 6.13.4 (the pinned version) against a local anvil chain with chain id 4663 and a signer runner, new ethers.Contract('', [latestRoundData ABI], signer).latestRoundData() rejects with code UNCONFIGURED_NAME: 'an ENS name used for a contract target must be correctly configured'. Trigger state: mainnet launch (dry = false) with ALLOW_NO_FEED=1, MSFT_FEED unset, ROUTE unset, and at least one initialised USDG/MSFT pool with liquidity (findRoute returns it, so line 170 calls routeProblem). Expected: the route is accepted or skipped with a logged reason and the launch continues. Actual: step('route') throws from line 351-352, nothing is recorded, and the launch aborts on every resume with the deployer still owning the token and hook.

### 4. Low: MSFT95Staking.sync: unbounded `fresh * ACC` overflows and blocks stake/unstake/claim for every user until the owner switches the token off

`msft95-contracts-audit-v4/v4/MSFT95Staking.sol:155`

```
        uint256 add = fresh * ACC + back + d;
```

audit_math. sync() reads a reward token's balance with a guarded staticcall (handles a reverting token, AUDIT-2 H-2) but then scales the new amount by ACC = 1e36 with checked arithmetic and nothing bounds it. When a listed, switched-on reward token reports a balance for the staking contract above held + type(uint256).max / 1e36 (about 1.158e41 raw units), `fresh * ACC` panics with 0x11. stake(), unstake(), claim() and claimToken() all run _syncAll() first, so every one of them reverts for every user, including the Vesting and AgentStakes positions. The NatSpec promises 'Unstaking is instant and never blocked, not even by a broken reward token'. Recovery needs the owner (the timelocked Safe) to call setRewardOff(token, true), which only runs _accrue and so lets sync return before the multiplication. None of the six launch reward tokens can reach that balance honestly; the trigger is a token that misreports after an upgrade, or a token the owner later lists with a very large supply. Fix: treat an amount that would overflow like a failed read, e.g. `if (fresh > (type(uint256).max - back - d - left) / ACC) return;` (or clamp), so a bad reward token can never block unstake.

**Reproduction**

Ran the specialist's proof test/scratch/Proof_7371cd4786e1.t.sol with forge (solc 0.8.26, via-ir, as the project builds): deploy MSFT95Staking with stake token T and one plain ERC-20 reward token R; Alice stakes 10e18 T; R mints type(uint256).max / 1e36 + 1 to the staking contract; Alice calls unstake(10e18). Expected: she gets 10e18 T back. Actual: the call reverts with 'panic: arithmetic underflow or overflow (0x11)' at `fresh * ACC` in sync(), reached through _syncAll(). The same test passes against a copy of the contract where sync() returns early when fresh would overflow the multiplication.

**Proof**: a Foundry test that fails on this code and passes once it is fixed.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;
import "forge-std/Test.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {MSFT95Staking} from "msft95-contracts-audit-v4/v4/MSFT95Staking.sol";

contract Tok is ERC20 { constructor() ERC20("T","T") {} function mint(address a, uint256 v) external { _mint(a, v); } }

contract StakingOverflowTest is Test {
    function test_hugeRewardBalanceBlocksUnstake() public {
        Tok stakeT = new Tok();
        Tok rew = new Tok();
        address[] memory r = new address[](1); r[0] = address(rew);
        MSFT95Staking s = new MSFT95Staking(IERC20(address(stakeT)), address(this), r);
        address alice = address(0xA11CE);
        stakeT.mint(alice, 10e18);
        vm.startPrank(alice); stakeT.approve(address(s), 10e18); s.stake(10e18); vm.stopPrank();
        rew.mint(address(s), type(uint256).max / 1e36 + 1);
        vm.prank(alice);
        s.unstake(10e18);
        assertEq(stakeT.balanceOf(alice), 10e18);
    }
}
```

### 5. Low: MSFT dividends accrued to a contract holder without a claim path are unrecoverable; the in-scope MSFT95AgentFarm is such a holder and nothing in the package excludes it

`msft95-contracts-audit-v4/v4/MSFT95AgentFarm.sol:62`

```
///     freeze the keeper for their agent or leave. There is no way to sweep tokens out: nothing held here belongs to the admin.
```

Merged from audit_permissions (farm) and audit_economics (any non-claiming contract): one mechanism in MSFT95Token, with the farm as the in-scope instance. Every non-excluded address holding MSFT95 is credited balanceOf * perShare of MSFT at each distribute, and anyone can push it to the holder with claimFor (v4/MSFT95Token.sol line 102). MSFT95 is a listed farm token (the MSFT95/USDG OPEN pool in the tests and MAINNET.md), so agents' MSFT95 cash sits in the farm, which therefore earns MSFT. The farm's only outward transfers are withdraw (bounded by balanceOf[agentId][token], never credited for MSFT), payTreasury (treasuryOwed[MSFT], 0), and pool settlement of the pool's own token0/token1 (lines 235, 255, 543-561); there is no rescue, and `owed[MSFT]` is never increased by claimed dividends, so the MSFT above `owed` is unreachable by anyone, forever, and grows with every distribution. docs/MAINNET.md line 81-82 states 'only the pool manager, the hook, the token and the farm are excluded', but no script in this package performs that exclusion (lib.js excludes only the PoolManager in the constructor and the hook on line 154; the farm is deployed outside this package). setExcluded(farm, true) stops future accrual but freezes what was already earned as `credit`, which claimFor still pays into the farm where it is equally stuck. The same applies to any third-party contract that comes to hold MSFT95 and cannot call claim (a permissionless Uniswap v3 MSFT95 pool, a bridge escrow, a lending market): its share is removed from the dividend flow and, once excluded, stays frozen as credit with no way to return it to perShare. Note: the economics specialist's claim that a surplus in a MSFT-paired v3 pool is 'taken by the next swapper' does not hold (v3 measures balanceBefore after the surplus exists), so that part is dropped. Fix: exclude the farm in its deployment step and list it as a required Safe action; or give the farm a claimDividends path that credits MSFT pro rata or forwards it to the treasury; and consider letting the owner redistribute an excluded address's frozen credit back into perShare.

**Reproduction**

State: farm deployed, MSFT95/USDG listed as an OPEN pool (listedToken[MSFT95] = true), farm not in `excluded`. Agent 1's holder calls farm.deposit(1, MSFT95, 1e24): eligibleSupply includes the farm's 1e24. The hook keeper runs convert, which calls distribute(100e18) MSFT. Anyone calls MSFT95Token.claimFor(farm): MSFT.balanceOf(farm) rises by 100e18 * 1e24 / eligibleSupply. Expected: that MSFT reaches the agent or the treasury. Actual, by enumeration of every transfer in the farm (grep safeTransfer/take: lines 235, 255, 543, 546, 553, 554, 560, 561): farm.withdraw(1, MSFT, type(uint256).max, holder) transfers 0 because balanceOf[1][MSFT] == 0; farm.payTreasury(MSFT) transfers 0 because treasuryOwed[MSFT] == 0; the pool paths only move the pool's token0/token1 by the pool's deltas. No function moves the balance above owed[MSFT]. After setExcluded(farm, true), credit[farm] holds the accrued amount and claimFor(farm) still sends it into the farm.

### 6. Info: Hook fee on exact-output swaps naming USDG is charged on the amount named, not the amount filled: a price-limited partial fill pays more than 3% and can leave the swapper paying USDG as well

`msft95-contracts-audit-v4/v4/MSFT95RewardHook.sol:156`

```
        uint256 fee = _fee(amt, exactIn);
```

audit_economics. The NatSpec promises 'the fee is the same 3% of the gross USDG either way' and AUDIT-3 I-3 documents the deviation only for exact-input buys. The same gap exists for exact-output swaps whose specified currency is USDG (a sell for exact USDG out): beforeSwap computes fee = amt * 300 / 9700 on the requested output, takes it immediately with poolManager.take, and returns +fee as the specified delta, so v4-core (Hooks.beforeSwap line 275) asks the pool for amt + fee. If the swapper's sqrtPriceLimitX96 stops the swap early, the pool delivers only P < amt + fee; in Hooks.afterSwap (line 306-311) the caller's delta becomes swapDelta - hookDelta = P - fee, which is below amt and negative when P < fee, so the swapper pays MSFT95 and USDG in the same swap while the hook books a fee far above 3% of what traded. The MSFT95Router never sets a tight limit and only does exact input, so site users are unaffected; aggregators, bots or any direct PoolManager caller using exact output with a limit are. Fix: for exact-output swaps move the USDG fee to afterSwap where the realised specified delta is known (compute on the actual output), or document the limitation for exact output as I-3 does for exact input.

**Reproduction**

Trace against v4-core 1.0.2 and the hook (no Foundry pool harness built for this informational item). State: pool open at the launch price, feeBps 300. Input: a direct PoolManager swap selling MSFT95 for exact USDG out, amountSpecified = +1_000e6 with USDG the specified currency, sqrtPriceLimitX96 one tick away so the pool can only move about 20e6 USDG. beforeSwap (line 154-162): fee = 1_000e6 * 300 / 9_700 = 30_927_835 taken by the hook; amountToSwap = 1_030_927_835. The pool stops at the limit after delivering ~20e6 USDG. afterSwap in v4-core: hookDelta specified = +30_927_835, swapper USDG delta = 20_000_000 - 30_927_835 = -10_927_835. Expected: fee = 3% of the USDG that actually traded (~0.62 USDG) and the swapper receives USDG. Actual: the hook keeps 30.93 USDG (about 150% of the fill) and the swapper owes 10.93 USDG on top of the MSFT95 sold.

### 7. Info: Farm keeper loss bound is per swap, not per agent per day: with slipBps 150 and SWAPS_PER_DAY 8 a compromised keeper can move about 11% of an agent's cash to itself per day on ORACLE pools, and the da

`msft95-contracts-audit-v4/v4/MSFT95AgentFarm.sol:311`

```
            floor_ = _fairOut(p, zeroForOne, amountIn) * (10000 - p.slipBps) / 10000;
```

audit_permissions; reported as a trust-assumption quantification, not a permission bypass (AUDIT-3 I-5 already accepts 'up to slipBps per swap, or the daily cap on OPEN pools' with no code change). The README asks reviewers to test that 'a compromised keeper can only cause bounded loss'. swap() is onlyRole(KEEPER_ROLE); on ORACLE pools its floor is the feed value less slipBps (line 311), on PEG pools 1:1 less slipBps (line 314), and the only per-agent limit is SWAPS_PER_DAY = 8 (line 304); each swap may be the agent's whole balance of the input token. A keeper that is also the counterparty pushes the pool price slipBps away from the feed (inside maxDevBps, so _checkPrice passes), swaps the agent's full balance, and unwinds, pocketing up to slipBps per swap; losses compound across the 8 swaps: with the values the tests use (slipBps 150, maxDevBps 200) 1 - 0.985^8 = 11.4% of each agent's cash per day, about 57% per week; at the admin maximum slipBps 2000, 83% per day. On OPEN pools (MSFT95/USDG) there is no oracle floor at all: only the keeper's own minOut > 0 (line 316) and the per-pool daily cap0/cap1 (line 317), so a stolen key can sell each agent's balance for 1 wei until the pool cap is used. The holder's only defence is setFrozen (line 246), which requires noticing. The comment on line 71 ('bounds what a compromised keeper could bleed') reads as a daily bound; the actual bound is per swap times eight. Fix preserving the design: add a per-agent daily value limit for swaps (cumulative amountIn per agent per day as a fraction of its balance, or in feed dollars), and for OPEN pools a per-agent daily cap in addition to the per-pool one.

**Reproduction**

Code trace (the farm needs live v3/v4 pools, so no Foundry harness was built for this informational item). State: pool idx listed ORACLE with slipBps 150, maxDevBps 200, feed fresh at $100; agent 1 has balanceOf[1][USDG] = 10,000e6, not frozen. Keeper bundle, 8 times in one UTC day: (1) sell stock into the pool so its price is $98.6 (gap 1.4% < 2%); (2) farm.swap(1, idx, usdgIsToken0, 10,000e6, 0): _checkPrice passes, floor = 10,000/100 * 0.985 = 98.5 stock (line 311), the pool returns ~101.4 stock, so the swap succeeds; (3) keeper buys the stock back, restoring the price; then swap the agent's stock back to USDG the same way. Expected per the comment on line 71: loss bounded to about slipBps of value per day. Actual: after 8 swaps the agent's USDG is about 8,860e6 (11.4% moved to the keeper); after 7 days about 4,300e6. On the OPEN MSFT95 pool with cap1 = 1,000e6 per day: farm.swap(1, iM, false, 1,000e6, 1) succeeds with out = 1 wei once the keeper has first drained that side of the pool, moving $1,000 per agent per day with no oracle check.

---

Judge's submission `973b40ad783b556f43501309881150125c0af2effa343dab663f402bd6b70d2f`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
