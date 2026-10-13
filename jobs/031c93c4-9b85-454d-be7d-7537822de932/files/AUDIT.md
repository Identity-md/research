# Audit report

> Control audit of BLACKOUT v3.14 before its four contract launches on Robinhood Chain (4663). Source: identity-md-launches/launch-1544-blackout-swarmdesk-bootstrap-robinhood at commit 210eafe, built with the repo foundry.toml (solc 0.8.26, optimizer 200, cancun, viaIR false, bytecode_hash none). Read-only: no deploy, no broadcast, no source changes.
>
> v3.14 fixed the previous pre-launch audit (job a8730286): V4Market quotes now include the 1.25% LP fee; SwarmDesk.bind checks the hook's desk, token and game hash; FeeRouter.executeSells, FarmCore.retire, SwarmDesk._regulate key range, FarmRewards vintage timestamp, Season.claimLottery via PackSale receipts, Economy bounded lock insertion; all IMD protocol addresses moved from constructor arguments into src/lib/Robinhood.sol constants (the IMD manifest gate refuses protocol addresses as constructor words); SwarmDesk and EndowmentEscrow now deploy together in one launch.
>
> Goal: confirm the launch audit panel (flow, permissions, economics, math, judge) would raise no medium, high or critical finding in any of the four launches described in launch-v39.md (L1 SwarmDesk + EndowmentEscrow, L2 token + V4Market hook, L3 job A, L4 job B), and that each v3.14 fix is correct and introduced no regression. Also check every constructor in launch-v39.md against the deploy gate (no IMD protocol address as a constructor word; only $poolManager, $token, $factory and $contract:Name placeholders).
>
> Accepted by the requester, report only a worse variant: the eight items in docs/accepted-v314.md.
>
> Deliver: every finding with severity, contract and line, reproduction, and whether the launch judge would block; for each medium or higher the minimal fix and which creation-code pins it changes. If nothing blocks, say so explicitly per launch.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1544-blackout-swarmdesk-bootstrap-robinhood.git |
| Commit | `210eafe33ecc3a083e14a2b2c77b3b2584eaaa43` |
| Job | `031c93c4-9b85-454d-be7d-7537822de932` |
| Judged | 2026-10-13 13:25 UTC |
| Findings | 1 medium · 3 low · 2 info |

Four agents audited the code as it is at `210eafe`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: SwarmDesk.bind accepts any contract echoing desk/token/gameConfigHash as the registry market: a twin with attacker-written market captures the escrowed endowment and permanently freezes the real hook

`src/SwarmDesk.sol:207`

```
        if (h.desk() != address(this) || h.token() != r.token() || h.gameConfigHash() != binding.gameConfigHash) {
```

Launch L1 (SwarmDesk). The v3.14 hook check reads only three view values from registry.market(): desk(), token() and gameConfigHash(). Nothing proves the market is the LaunchFactory-initialized V4Market hook: no manager()/launcher() check, no hook flag check, no PoolManager pool state, no LaunchFactory record (none is exposed in this tree). A plain contract that returns the three expected values passes. Accepted item M-2 (docs/accepted-v314.md, docs/m2-trust-assumption.md) covers a byte-identical twin that runs the pinned game with the real hook as its market, rated griefing under the pinned game rules and mitigated by checking Desk.registry() before forwarding. This variant breaks both premises. (1) The twin registry market is attacker code, so everything the pinned modules read through registry.market() is attacker-chosen: GameRegistry.launchTime() (FarmRewards epochs, Season weeks, PackSale.opensAt), ILaunchHook(market).fees(), and IMarket.buy/quote/quoteSell/maxSellBatch/sell used by FeeRouter.executeBuys/executePotBuys/executeSells and zapBuy. The twin game is not the pinned game; the attacker is effectively its only player and harvests the 200,000,000e18 endowment emission under their own market. (2) EndowmentEscrow.forward (src/EndowmentEscrow.sol:61-89) is permissionless and authenticates only Desk.registry()==registry plus pinned code and factory coordinates, so the attacker forwards the whole escrow balance to the twin pool themselves; the runbook step 5 check cannot prevent it. (3) The real L2 hook can never bind a FeeRouter afterwards: V4Market.bindFeeRouter (src/V4Market.sol:139-150) requires _routerMarketValid(r.market()) i.e. r.market()==hook and _canonical(r) i.e. Desk.registry()==r, which no registry satisfies once the Desk is bound to a registry whose market is not the hook. flushFees then reverts NotConfigured forever and heldBase/heldSellTax/heldLaunchTax (1% of all swap volume plus sell surcharges and launch tax) are stuck in the hook; reward buys never run. In the accepted matching-twin case the twin FeeRouter can still bind to the real hook, so this impact is new. Preconditions are the same as accepted M-2: knowledge of the private roots (public once L3 executes, or earlier at the platform) and a platform-admitted ProjectFactory launch (Params, GameRegistry, RewardPool) landing before the keeper bind-desk transaction. Launch judge: medium on L1; it would be raised. Minimal fix (changes only the L1 SwarmDesk creation-code pin 0x2573ebbe...135e and its launch-v39.md row; EndowmentEscrow, V4Market, Params, GameRegistry and the 14 module pins embed the Desk address, not its code, and are unchanged): in bind, after the three equalities, prove the market is the genuine launch hook. If the LaunchFactory exposes the launch record that claimFees(N_TOKEN) keys on, require it to name h for r.token(). Otherwise require IBoundHook(h).launcher()==Robinhood.LAUNCH_FACTORY, h.manager()==Robinhood.POOL_MANAGER, h.initializedAt()!=0, uint160(address(h)) & 0x3fff == 0x10cc, and a non-zero sqrtPriceX96 read from the pinned PoolManager via extsload(keccak256(abi.encode(keccak256(abi.encode(PoolKey(address(0), r.token(), 12500, 60, h))), 6))); that forces the twin market to be an initialized flagged hook on the real PoolManager for the registry token, which the ProjectFactory salt scheme cannot mine, and leaves only a separately initialized pool at a self-mined address as residual. Per-launch verdict for the rest: L2 (token + V4Market), L3 (job A) and L4 (job B) carry no medium or higher finding; every v3.14 fix listed in the task was re-read and introduces no regression beyond the low/info items below.

**Reproduction**

State: fresh SwarmDesk with gameConfigHash H deployed through the factory; EndowmentEscrow(desk) holds 200000000e18 of the token T; the honest registry is not yet bound. Attacker deploys FakeMarket{desk()=Desk, token()=T, gameConfigHash()=H} as an ordinary contract, then through the ProjectFactory Params(Desk,200,1e18) at (41,0), GameRegistry(T, params, fakeMarket, starterRoot, freeRoot, snapshotBlock, 200000000e18) at (41,1), RewardPool(registry) at (41,2), and registry.register(0,41,2,poolCode). Attacker calls desk.bind(registry, registryCode, paramsCode, 41,1,41,0). Expected: revert InvalidProof (market is not the launch hook). Actual: succeeds, Desk.registry()==twin. Attacker calls escrow.forward(twin,41,1,registryCode,41,2,poolCode). Expected: impossible. Actual: succeeds, token.balanceOf(twinPool)==200000000e18, escrow balance 0, forwarded()==true. Afterwards V4Market.bindFeeRouter(anyRouter, ...) reverts InvalidValue (r.market()!=hook) or InvalidProof (_canonical) for every registry, so flushFees reverts NotConfigured forever. Run: forge test --match-path test/scratch/TwinFakeMarket.t.sol -> on 210eafe both tests fail: "bind accepted a registry whose market is attacker code" and "endowment captured by twin pool: 200000000000000000000000000 != 0".

### 2. Low: GameRegistry.register lets any admitted factory launch pre-fill a role with a byte-identical module copy, orphaning the recorded L3/L4 contract for that role

`src/GameRegistry.sol:95`

```
        deployed = factory.predictContract(launchNumber, index, bytes.concat(creationCode, abi.encode(address(this))));
```

Launch L3/L4 (GameRegistry pin). register() is permissionless and accepts any (launchNumber, index) whose ProjectFactory CREATE2 result for pinned creation code ++ abi.encode(registry) has code. Nothing ties a role to the launch numbers the runbook records (N_A for roles 0-5, N_B for roles 6-13). A third party who pays for their own ProjectFactory launch of the same pinned creation code with the canonical registry as the constructor word can register their copy first; modules[role] is then set permanently and the honest register reverts AlreadyDone. Because code and constructor word are identical, the registered copy behaves exactly like the honest one, so funds and game rules are unaffected. The harm is operational: runbook steps 3/4 (verify all fourteen modules against the recorded L3/L4 addresses) fail with no recovery path, the recorded contract for that role is dead weight, and the keeper wiring and EndowmentEscrow.forward coordinates (poolLaunch/poolIndex for role 0) must be re-pointed at the third party coordinates. Different mechanism from accepted M-2: it happens after a correct bind, needs no private preimage, and binding immediately does not prevent it. Launch judge: would not block. Minimal fix if wanted: none that keeps the pinned registry; operationally read module addresses from GameRegistry.module(role) and the Registered events instead of the launch records. A source fix (register pinning roles to the registry own launch number via the factory record) changes the GameRegistry pin and therefore SwarmCode, SwarmDesk, EndowmentEscrow and V4Market pins.

**Reproduction**

State: canonical GameRegistry r deployed via the factory, role 9 unregistered. Third party deploys FarmEngine via the ProjectFactory at launch 999 index 0 with initCode = FarmEngine creationCode ++ abi.encode(address(r)) and calls r.register(9, 999, 0, creationCode). Expected (runbook): only the recorded L4 contract (N_B, index 3) can fill role 9. Actual: the call succeeds and registeredModule(9) is the third-party copy; the keeper later deploys at (1000,3) and r.register(9, 1000, 3, creationCode) reverts AlreadyDone. Reproduced with test/scratch/Lows.t.sol testRegisterPrefillByThirdPartyLaunch (factory etched at Robinhood.PROJECT_FACTORY, salt keccak256(abi.encode(launch,index))): passes on 210eafe, showing the behaviour.

### 3. Low: Season.rollover does not require the week to be finalized, so a late finalize produces winners whose pot claims always revert

`src/Season.sol:81`

```
        if (rolled[w] || block.timestamp < claimDeadline(w)) revert TooEarly();
```

Launch L4 (Season pin, role 8). rollover(w) is permissionless once block.timestamp >= claimDeadline(w) (launchTime + (w+1)*7d + 7d grace + 4 weeks) and checks only rolled[w]; it moves potRemaining[w] into the current week. prepare(w)/finalize(w) have no upper time bound, so if no keeper finalizes week w within five weeks of its end, anyone can roll the pot first and the week can still be prepared and finalized afterwards. finalize then awards the best-farm prize through FarmRewards (that part works) and marks lottery winners and the winning district, but claimBest/claimDistrict/claimLottery all route through _payPot (line 67), which reverts TooEarly because rolled[w] is true, so those winners can never collect and the 40%/30%/30% token pot for the week is silently redistributed to a later week. Needs a keeper absence of five weeks; not a permission bypass. Launch judge: would not block. Minimal fix: in rollover require seasons[w].finalized (or allow rolling an unfinalized week only once it can no longer be prepared), or make finalize refuse a rolled week. Changes the Season pin (role 8, launch-v39.md L4 row) only.

**Reproduction**

State: week 0 has pot[0] = 100e18 (depositPot from the FeeRouter) and nobody calls prepare(0). Warp to claimDeadline(0). Call rollover(0): succeeds, potRemaining[0] = 0, rolled[0] = true, pot moved to the current week. Then advance epochs until seasonReady(0), call prepare(0, 1), advance 3 blocks, finalize(0): succeeds, result(0).finalized == true while rolled[0] == true. Any address with lotteryWon[0] or seasons[0].best calling claimLottery(0)/claimBest(0) hits _payPot which reverts TooEarly() because rolled[0]. Expected: either rollover refuses an unfinalized week or finalize refuses a rolled week. Reproduced with test/scratch/Lows.t.sol testRolloverBeforeFinalizeThenFinalizeSucceeds (passes on 210eafe, asserting finalized && rolled for the same week).

### 4. Low: FeeRouter.executeSells: the capped-heartbeat token sweep is rolled back whenever nothing sellable remains after it

`src/FeeRouter.sol:205`

```
        if (amount == 0) revert InvalidValue();
```

Launch L4 (FeeRouter pin, role 6). executeSells first moves the whole heartbeatTokens balance to the RewardPool when heartbeatBalance has reached HEARTBEAT_CAP (lines 195-200), then computes amount = min(teamTokens + heartbeatTokens, maxSellBatch()) and reverts InvalidValue when amount == 0 (line 205). Since heartbeatTokens was just zeroed, amount is zero exactly when teamTokens == 0 or the market reports maxSellBatch() == 0, and the revert undoes the sweep. The heartbeat tokens stay parked in the FeeRouter (excluded from RewardPool.available() and epoch budgets) until team tokens accrue through a later routeTokens, and the keeper sees an unexplained revert. Reachable magnitude is small: routeTokens always credits teamTokens 10% alongside the heartbeat share and sells are proportional, so teamTokens == 0 with heartbeatTokens != 0 arises only from rounding dust in partial batches (or a market whose safe batch is zero). No funds are lost and nobody gains. Launch judge: would not block. Minimal fix: return early after the sweep when total == 0 instead of reverting, e.g. if (total == 0) { if (swept) return 0; revert InvalidValue(); }. Changes the FeeRouter pin (role 6, launch-v39.md L4 row) only.

**Reproduction**

State (test/scratch/Lows.t.sol testSweepRolledBackWhenNoTeamTokens, passes on 210eafe): FeeRouter f with a MockMarket, routeTokens(50) gives teamTokens 5, heartbeatTokens 1; market depth set so maxSellBatch() == 5; executeSells(5, quote*9850/10000) sells 5 with h = 5*1/6 = 0, leaving teamTokens 0 and heartbeatTokens 1; market deposits 50 ether sell tax so heartbeatBalance == 1 ether == HEARTBEAT_CAP; warp 5 minutes. Call executeSells(1, 1). Expected: the 1 heartbeat token is transferred to the RewardPool and recordInflow runs (lines 195-200), sell step skipped. Actual: revert InvalidValue() at line 205; heartbeatTokens is still 1 and the transfer at line 198 is rolled back.

### 5. Info: FarmRewards._credit: a same-epoch scrap/award credit back-dates the maturity of the later settlement credit for that epoch by up to one epoch

`src/FarmRewards.sol:486`

```
        if (v.amount == 0 || at < v.at) v.at = uint64(at);
```

Launch L3 (FarmRewards pin, role 1). The v3.14 vintage-timestamp rule keeps, per 32-slot vintage, the earliest at of all credits for the same epoch (line 486). Settlement credits pass at = e.end (lines 418, 423), but scrap (line 561) and award (line 575) credit the current epoch with at = block.timestamp, which is earlier than e.end. When a player scraps during epoch N and N is settled later, the settlement credit merges into the same slot and inherits the scrap timestamp, so its 7-day tax age starts up to 6 hours early. taxBps falls 1500 bps over 7 days, so the mispricing is at most about 54 bps of the settlement credit, in the player favour and self-triggered; reserved accounting is unchanged (pending == matured + sum(vintages) still holds). test/AuditV314.t.sol testLaterSameEpochCreditKeepsEarlierTaxVintage shows the earliest-timestamp merge is intended for two awards in one epoch; this note only records that it also lets a current-epoch scrap/award pull a later settlement credit age forward. Launch judge: would not block. Fix if wanted: pass epochs[epoch].end as at for scrap and award credits. Changes the FarmRewards pin (role 1) only.

**Reproduction**

State: epoch N open (start S, end S+6h), player p has committed weight and an unequipped item. At t = S+10min p calls FarmCore.scrap(id, 0) with scrapAllowance > 0: _credit(p, x, N, S+10min) sets vintages[N%32] = {epoch N, at S+10min, amount x}. After N closes and p settles N at S+6h+1min, _reward credits y via _credit(p, y, N, S+6h): at (S+6h) is not < v.at (S+10min), so v.at stays S+10min and v.amount = x+y. At a claim at S+10min+7d exactly, _consume sweeps the slot as fully matured (block.timestamp >= at + 7 days) and taxes y at 500 bps; with at = S+6h the age would be 7d - 5h50m and taxBps = 2000 - 1500*(7d-5h50m)/7d = about 552 bps. Verified by code reading of lines 418, 423, 486, 561, 575.

### 6. Info: Runbook says the deploy-gate tool accepts launch documents, but the tool only JSON.parses its arguments and crashes on launch-v39.md

`tools/check_deploy_gate.mjs:45`

```
    const count = checkDeployGate(JSON.parse(readFileSync(file,'utf8')));
```

launch-v39.md line 9 says: "The deploy-gate tool also accepts paths to generated launch documents and checks every constructor in each." The tool JSON.parses every argument, so passing the runbook itself throws before any check runs. The manual check of all 19 constructors in launch-v39.md finds no IMD protocol address (none of the eight src/lib/Robinhood.sol constants appears anywhere in the file; SwarmDesk takes 7 non-address words, EndowmentEscrow $contract:SwarmDesk, V4Market $poolManager,$token,12500,60,$factory,<L1_SWARM_DESK>,hash, Params <L1_SWARM_DESK>,200,1e18, GameRegistry <L2_TOKEN>,$contract:Params,<L2_V4MARKET>,roots,snapshot,endowment, all modules $contract:GameRegistry or <L3_GAME_REGISTRY>), and the tool passes on docs/launch-v314-plan.json (19 constructors). Risk is only operational: an operator following the runbook literally gets a crash instead of a PASS/FAIL. Launch judge: would not block. Fix: drop the sentence from the runbook or teach the tool to extract the [i] Name [...] lines from markdown. No creation-code pin changes.

**Reproduction**

Run node tools/check_deploy_gate.mjs launch-v39.md at 210eafe. Expected (per launch-v39.md line 9): a PASS/FAIL verdict over the 19 runbook constructors. Actual: SyntaxError: Unexpected token "#", "# BLACKOUT"... is not valid JSON thrown from JSON.parse at tools/check_deploy_gate.mjs:45; no constructor is checked. node tools/check_deploy_gate.mjs docs/launch-v314-plan.json prints "PASS — 19 constructors contain no literal IMD protocol addresses".

---

Judge's submission `da2e0df6bd3efb314a42fd5a2b406781b44869f24f47579d55a9192a0f386f56`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
