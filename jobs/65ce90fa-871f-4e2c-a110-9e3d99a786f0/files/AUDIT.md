# Audit report

> Audit the three Ponzinomics contracts in src/pimd at this commit. PimdToken is a fixed-supply ERC-20: exactly 1,000,000,000 at 18 decimals, minted once in the constructor, no owner, no mint and no burn function (burning is a plain transfer to DEAD, so totalSupply never moves). PimdHook is a Uniswap V4 hook that taxes every trade in IMD, 2.4% on buys and 5.6% on sells with the pool's own 1.25% on top, split 75% to holders and 25% to the team, taking its fees as ERC-6909 claims on the quote currency. The IMD launch factory constructs the hook and opens the pool itself, so the team wallet, the engine address, the quote token and the opening tick (129,000, tolerance 300) are all source constants. PimdEngine pushes the holders' IMD into wallets weighted by balance times hold-streak, the tiers being zero under an hour and then 0.5x, 1x, 1.5x, 2x and 3x from fourteen days; tally weighs the whole set in one call and pay is paged. Round 3, and the surface that matters is everything since the round-2 commit f182e9f. Your round-2 high is closed by taking the choice of read instant away: `tally` is now restricted to keeper addresses fixed in the constructor, while `fire`, `pay`, `register`, `prune` and `abortEpoch` stay open to anyone. Then four independent review passes found nine more things, all fixed here, and three of those were defects in the fixes themselves -- so treat the fixes as the least trustworthy code in the tree, not the most. In order of how much I would like a second opinion: (a) the keeper tip budget is now shared out by phase rather than first come, via `_tipTo(to, amt, floorBps)`, and inside `pay` each page may draw only its pro-rata slice of what is left, because reserving a share for the phase left the first page taking all of it and the tail unpaid -- attack the arithmetic, the paging, `abortEpoch` interactions, and whether any sequence leaves the budget or the pot inconsistent with what was paid; (b) `fireTip` is no longer paid by `fire` but recorded in `epochFirer` and paid by `tally`, only where the epoch weighs something; (c) `_shapeChanged` carves out EIP-7702 delegation stubs via new inline assembly in `_isDelegationStub`, which deliberately makes a guard return false where it previously returned true; (d) a full holder set now reclaims a dead slot through a bounded cursor sweep rather than refusing registration for ever; (e) `minInterval` is 15 minutes in production and the holder bound is 700 under a constructor ceiling of 800. Four things are accepted and documented rather than fixed, so please do not re-report them as defects: weight is balance times tier and a rented balance held across the tier-0 hour earns like any other; a contract that cannot forward IMD can be registered by a stranger unless named at bind; `fireTip` is a ceiling rather than a guarantee because the fire floor caps it at a tenth of the budget; and the tip floors order the draw without rationing between actors, so one party holding several roles collects every share, bounded only by the 5% `TIP_BUDGET_BPS`. Earlier rounds, for context: Since f182e9f this commit answers your high by taking the choice of read instant away -- `tally` is now restricted to keeper addresses fixed in the constructor, everything else stays permissionless -- and your finding 2 and finding 7 (the reclaim cursor could not survive the revert, and the 900 ceiling was measured with balances unchanged). Two independent reviews then found six more, all fixed here: an EIP-7702 delegation is carved out of `_shapeChanged`, a zero-weight epoch pays no per-holder tip, a deferred registration emits an event, `totalToTeam` is net of the tip, `Fired` moved after the early return, and the holder bound is 700 under a ceiling of 800. Attack the keeper split hardest: say whether a non-keeper can still reach engine state at a moment of its choosing through `register`, which writes `lastBal`, or through `_reclaimSlot`, which reads balances and removes entries. Note two things are accepted and documented rather than fixed, so do not re-report them as defects: weight is balance times tier and a rented balance held across the tier-0 hour earns (the NatSpec on `tally` says so), and a contract that cannot forward IMD can be registered by a stranger unless named at bind. Earlier context: flush no longer tips the engine, a full holder set now reclaims a dead slot instead of locking everyone out for ever, bind excludes the launch factory and register refuses precompiles, and the holder bound is 800 under a constructor ceiling of 900. Check each of those actually closes what you found, and say whether any of them opened something new -- the reclaim path in particular, which is permissionless and removes an entry. The rest of the holder-set logic is still only one audit old. Four things in particular. First, register probes an address with _isPool but can only see the code that is there at the time, so it now records a vettedCodeless bit and tally calls _shapeChanged, which takes all weight off an address once code arrives where there was none. Say whether that really closes the play of picking a CREATE2 address, funding it, registering it while it is still empty, letting the streak mature and only then deploying pair code into it, and whether it can be evaded from the other side by an address that carries code from the start. Second, _shapeChanged is blunt on purpose: any code arriving voids the verdict, a legitimate EIP-7702 delegation included, and prune drops a holder on that same test so the address can register again on what it now is. Confirm there is no reachable state in which a holder earns nothing and cannot be pruned, because the engine has no owner and that would be permanent. Third, prune now drops a holder on its shape as well as its size and is permissionless: confirm it cannot be aimed at a holder who should keep earning, and that the swap-and-pop is still right when the pruned holder is the last element. Fourth, the exclusion list at bind is the token, imd, the hook, the PoolManager, the engine, the team, address(0) and DEAD, plus whatever the binder names. Say whether anything else can hold PIMD, be registered, and then be unable to forward an IMD payout. Then the standing ones. Tally weighs the whole set in one call against min(bal, lastBal) so a single bag cannot be counted once per wallet it is moved through, which was the high you found last time: confirm it holds. The engine must never read holder weights while the PoolManager is unlocked, which is where a flash borrower would stand. One holder who cannot receive IMD must not be able to stall a batch. beforeRemoveLiquidity is the whole safety case for letting the launch factory hold the liquidity position: it must refuse every negative liquidityDelta for ever, from any caller including the position's owner and the hook itself, while allowing a zero delta so the pool's own fee collection still works. beforeAddLiquidity must allow exactly one add, the factory's seed, and refuse every later one, reentrancy and the hook calling itself included. beforeInitialize is the only gate on the pool's shape: confirm it cannot be bypassed and that every assumption the tax maths makes is enforced there, in particular that IMD is currency0. And the fee accounting: claims minted in beforeSwap and afterSwap must always equal holdersOwed plus teamOwed, with nothing double counted or stranded, and flush must not be able to pay out more than was taken. The engine pulls from the hook inside a try/catch, which has hidden one breakage from us already: say whether that pattern is safe here. Report findings rather than fixing them, and do not propose changes to the economics, the tax rates, the split or the tier ladder.

| | |
|---|---|
| Repository | https://github.com/JJ-ME55/Ponzinomics.git |
| Commit | `5bda20d8e3bbdd88eaa753c1f0fcb5053bc286da` |
| Job | `65ce90fa-871f-4e2c-a110-9e3d99a786f0` |
| Judged | 2026-10-09 06:18 UTC |
| Findings | 1 low · 6 info |

Four agents audited the code as it is at `5bda20d`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: pay() computes start + maxHolders in checked arithmetic before clamping, so a 'pay the rest' call with a large argument reverts on every page after the first

`src/pimd/PimdEngine.sol:566`

```
        uint256 end = start + maxHolders;
```

`pay` adds the caller's page size to `cursor` and only afterwards clamps `end` to `epochCount`. On the first page `cursor == 0` so any argument works; on every later page `cursor > 0` and an argument above `2^256 - 1 - cursor` (type(uint256).max is the natural 'all of it' value) hits Panic(0x11) before the clamp. `tally` is safe at the same point because it compares (`maxHolders < epochCount`) rather than adds. Nothing is lost and a smaller argument succeeds, but the finishing pages are exactly the ones the round-3 pro-rata tip exists to reward, and a finisher whose transaction reverts is one more way a tail goes unpaid until `abortEpoch`. Minimal fix: clamp before adding, e.g. `uint256 left = epochCount - start; if (maxHolders > left) maxHolders = left; uint256 end = start + maxHolders;`. Merged from audit_math.

**Reproduction**

Local harness (PimdBaseTest, 4% drip, 2 min minInterval): buy 300 IMD of PIMD for alice and bob, register both, warp 2 days. keeper: fire(); tally(500) -> phase == Pay, epochCount == 2. Anyone: pay(1) -> cursor == 1. Anyone: pay(type(uint256).max). Expected: pays bob and closes the epoch. Actual: reverts with arithmetic overflow (Panic 0x11) at `start + maxHolders`; a following pay(500) succeeds and closes the epoch. Reproduced in test/scratch/Judge.t.sol::test_pay_max_uint_on_second_page_reverts (asserts the revert with stdError.arithmeticError, then the recovery).

### 2. Info: tally's null-epoch comment still says fire paid fireTip up front, which commit 78fc912 removed

`src/pimd/PimdEngine.sol:544`

```
                // This does NOT make a null epoch free. `fire` paid `fireTip` at the top, before
```

The comment block at lines 544-549 inside the `tw == 0` branch of `tally` describes the pre-round-3 design: `fire` paying `fireTip` before anything is weighed, so a null epoch is 'bounded but not closed' and the tip 'is gone from the pot'. In the code as it stands `fire` pays nothing and only records `epochFirer` (line 457), and `tally` pays the firer at line 556 only on the `phase = Phase.Pay` path, which the null branch returns before (line 551). So the paragraph asserts a pot leak that no longer exists, in exactly the fix the requester asked to have re-read (item b), and the requester treats wrong comments as defects (f1d843f). The same stale sentence is repeated in test/pimd/PimdFixes.t.sol lines 407-410 above test_a_null_epoch_pays_no_per_holder_tip. The `lastFire has advanced` half of the paragraph is still accurate. Code is right; the comment is wrong. Merged from audit_flow, audit_permissions, audit_math and audit_economics (four identical reports).

**Reproduction**

State: a registered holder set that weighs nothing (every holder registered under an hour ago), pot > 0, phase Idle, elapsed >= minInterval. Non-keeper X calls fire(); a keeper calls tally(epochCount). Expected per the comment: X's IMD balance rose by fireTip (or a tenth of the budget) and pot fell by it. Actual: X's IMD balance is unchanged, pot is back to its pre-fire value, tipBudget == 0. The existing test test/pimd/PimdFixes.t.sol::test_a_null_epoch_pays_the_firer_nothing asserts the actual behaviour and passes, contradicting the comment next to the code it tests. fire() at lines 412-458 contains no _tipTo call.

### 3. Info: tipBudget and epochTipBudget are left at stale values after a normal close and after abortEpoch; only the null-tally path zeroes them

`src/pimd/PimdEngine.sol:633`

```
    function abortEpoch() external nonReentrant {
```

The null-epoch branch of tally closes the budget explicitly (`tipBudget = 0`, line 550). Neither of the other two ways an epoch ends does: pay's closing block (lines 596-605) returns `leftover` to the pot and zeroes epochQuote/epochPaidQuote but leaves tipBudget and epochTipBudget at their last values, and abortEpoch (lines 633-646) resets epochQuote, epochPaidQuote, epochPaidHolders, totalWeight and cursor but not these two. Between epochs the public getters `tipBudget()` and `epochTipBudget()` therefore report an open budget for an epoch that no longer exists, contradicting the field comments ('what is left of this epoch's keeper tips'). No fund impact: `_tipTo` is reached only from tally (Phase.Tally) and pay (Phase.Pay), and the next fire overwrites both before either phase can run; verified that pot == imd.balanceOf(engine) after a close, after an abort and after the following epoch, and that fire resets tipBudget to 5% of the new drip. It is the one state inconsistency the requester's item (a) asked about, and the fix is two assignments: `tipBudget = 0; epochTipBudget = 0;` in pay's `end == epochCount` block and in abortEpoch. Merged from audit_permissions.

**Reproduction**

Local harness, two holders registered 2 days ago, keeper: fire(); tally(500); pay(500) -> phase == Idle yet tipBudget() == 315276846767364698 and epochTipBudget() == 337276846767364698. Then fire() again, warp 1 day, abortEpoch(): tipBudget() == epochTipBudget() == the entire budget of the aborted epoch. Expected: 0 after an epoch has ended by any path, as the null-tally path does. Reproduced in test/scratch/Judge.t.sol::test_tip_budget_left_open_after_close_and_abort; test_stale_budget_cannot_be_drawn_between_epochs shows pay and tally both revert WrongPhase in Idle and the next fire overwrites the budget, so nothing can draw on it.

### 4. Info: tally and pay name their page-size parameter maxHolders, shadowing the immutable holder bound of the same name

`src/pimd/PimdEngine.sol:501`

```
    function tally(uint256 maxHolders) external nonReentrant {
```

`tally(uint256 maxHolders)` (line 501) and `pay(uint256 maxHolders)` (line 562) take a parameter named identically to the immutable `maxHolders` declared at line 111, which is the bound register enforces at line 366. solc 0.8.26 emits warning 2519 for both. Inside these two bodies the immutable is unreachable and every `maxHolders` is the caller's page size, so `maxHolders < epochCount` on line 506 reads at a glance as a comparison of the configured bound against the epoch size when it is the page argument. Behaviour is as intended today, but a future check written in either function against 'the bound' would silently compare against the caller's argument and compile. Fix: rename the parameters (e.g. `pageSize`); parameter names are not part of the selector so the ABI is unchanged. Merged from audit_flow and audit_permissions.

**Reproduction**

`forge build --force` prints 'Warning (2519): This declaration shadows an existing declaration' at src/pimd/PimdEngine.sol:501:20 and :562:18, each noting the shadowed declaration at :111:5. Input: a keeper calls tally(1) with epochCount == 3. Expected by a reader who takes `maxHolders` on line 506 for the immutable (800): no revert. Actual: TallyMustBeWhole(3), because the name resolves to the argument 1.

### 5. Info: pay's pro-rata comment says finishing an epoch is the best-paid page; the arithmetic pays every page the same per holder

`src/pimd/PimdEngine.sol:617`

```
        // keeps finishing an epoch the best-paid thing to do rather than the worst.
```

When the budget binds (tipPerHolder * n > tipBudget * n / m), a page covering n of the m uncovered holders draws tipBudget * n / m, leaving tipBudget * (m - n) / m for m - n holders: the remaining budget per uncovered holder is invariant, so every page is paid the same rate B/m per holder and the last page is paid the same rate as the first, not more. When the budget does not bind every page gets tipPerHolder per holder, also flat. The comment at lines 614-617 and the NatSpec at line 75 ('finishing an epoch is always the best-paid page rather than the worst') therefore overstate the fix: the tail is no longer starved, which was the defect, but finishing is paid the same per holder as sniping, and only earns more by covering more holders. No tip exceeds the budget and pot + epochQuote == balance held in every sequence tried (paged pay, abort mid-pay, refire), so this is a documentation inaccuracy, not a security defect. Merged from audit_economics.

**Reproduction**

Local harness with a pot small enough that the budget binds: three holders of 1 IMD each registered 2 days ago; keeper fire(); tally(500) -> tipBudget 758872905226570 < 3 * tipPerHolder (3 * 5e14). Three different addresses each call pay(1). Expected per the comment: the third (finishing) page is paid more than the first. Actual tips: 252957635075523, 252957635075523, 252957635075524 (the finisher gets one wei of rounding). Reproduced in test/scratch/Judge.t.sol::test_pro_rata_pages_pay_the_same_per_holder_when_budget_binds; the non-binding case (budget 0.48 IMD) pays 5e14 to each of three pagers (test_pro_rata_pages_pay_the_same_per_holder).

### 6. Info: Two NatSpec claims about the streak do not match min(bal, lastBal): a bag only has to be present at two keeper instants, and a round trip between counts never restarts the clock

`src/pimd/PimdEngine.sol:486`

```
    /// is. The deliberate cost: tokens must survive one epoch before they earn, so a fresh buy waits a
```

This is the direct answer to the standing question whether a non-keeper reaches engine state at a moment of its choosing through `register`, and it is a documentation finding, not a re-report of the accepted rented-balance item. `register` writes `lastBal` from the balance at the registrant's instant, and `tally` compares only that and the balance at the keeper's instant. Two consequences: (1) a freshly registered wallet is weighed in full at the very next keeper count once its hour is up, so the sentence at line 486 ('tokens must survive one epoch before they earn') does not hold for a new registration; the bag need only be present at registration and at one count, not across the hour between them. (2) A bag that leaves and returns between two keeper counts (bal == lastBal at both) neither resets nor blends the streak, so line 37 ('Selling or sending PIMD out restarts the clock') is only true if the bag is still out when the keeper counts; the clock matures to 3x while the bag is absent most of the time. What keeps this from being a defect: a token can be in only one registered wallet at each count, the loop is whole-set and keeper-timed, and a net reduction at any count resets the streak, so total weight per token per epoch is conserved and nobody is paid twice. No code change proposed; correct the two sentences so the next review does not rediscover it. Merged from audit_math.

**Reproduction**

test/scratch/Judge.t.sol. (1) test_register_then_present_only_at_the_keeper_instant: alice and bob buy 300 IMD of PIMD each and are registered; bob at once sends his whole bag (84204498602874296400475686 wei) to a parking address; warp 2 hours; the bag returns to bob in the keeper's block; keeper fire(); tally(500). Expected per line 486: bob carries no weight. Actual: totalWeight == alice_bal * 5000/10000 + bob_bag * 5000/10000, bob weighed in full. (2) test_round_trip_between_tallies_keeps_streak: bob registers; for 20 daily epochs the whole bag is out for 23 hours and back one hour before the keeper's count. Expected per line 37: streakStart restarts. Actual: streakStart unchanged after 20 epochs and holderInfo reports tierBps 30000.

### 7. Info: README describes a different economy, launch path and role set from the contracts at this commit

`README.md:6`

```
- **3% on buys, 7% on sells**, taken in IMD by the hook
```

The README contradicts the code on every number and role that matters: it states 3%/7% tax (PimdHook.sol:63-64 are 240 and 560 bps, 2.4%/5.6%), a 60/20/20 split with a hook-side buy-and-burn (HOLDERS_BPS is 7_500 and PimdHook.sol:36-39 say the burn is the pool's own 1.25% fee handled outside the contract), that the hook 'Launches the pool single-sided' through a `PimdHook.launcher` calling `launch()` (lines 19, 28, 43, 90; grep finds no `launch(` in src/pimd, the pool is opened and seeded by the launch factory via beforeInitialize/beforeAddLiquidity), that 'the token's whole supply mints directly to the hook' (line 36; PimdToken.sol:34 mints to msg.sender, the factory), that `launch()` reverts with BadCurrencyOrder (line 43; the error at PimdHook.sol:175 is never thrown), '32 local tests' (85 run), and 'the contract only enforces a two minute floor between epochs' (line 107; minInterval is a constructor parameter, 15 minutes in production per script/DeployPimd.s.sol). It never mentions that `tally` is keeper-only. The README is the first thing an integrator reads, so these are the numbers they will build against. Fix: rewrite the numbers, the launch description and the role list (binder, keepers, launch factory) to match this commit. Merged from audit_permissions.

**Reproduction**

Compare README.md lines 6-7, 19, 28, 36, 43, 56, 86-91, 107 against src/pimd/PimdHook.sol:63-65 (BUY_TAX_BPS = 240, SELL_TAX_BPS = 560, HOLDERS_BPS = 7_500), `grep -rn 'launch(' src/pimd/` (no result), src/pimd/PimdToken.sol:34 (`_mint(msg.sender, INITIAL_SUPPLY)`), src/pimd/PimdEngine.sol:501-502 (tally reverts NotKeeper for non-keepers), script/DeployPimd.s.sol (minInterval 15 minutes when production), and `forge test` (85 tests). Expected: the README states the economy and roles the code implements. Actual: it states the pre-launch-factory design.

---

Judge's submission `044779c644ea6595995b65aa1deadcd43c28e85c312469e48da45e3f74cd2c32`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
