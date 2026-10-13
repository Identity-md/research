# Audit report

> Pre-token audit of BLACKOUT at commit 1e4490923f20a389ecb6be136121f4eea65db3b1. L1 (SwarmDesk + EndowmentEscrow) is already deployed on Robinhood Chain (4663) from this commit as launch 1593. After L1 every creation-code pin is frozen: SwarmDesk pins GameRegistry, which pins all 14 module creation codes, and V4Market pins the registry too. Any later source change to any module means a new L1 and, after L2, a new token. So we need every finding NOW, before L2.
>
> Goal: act exactly like the IMD launch panel (flow, permissions, economics, math, judge) for the three remaining launches and report everything it would raise:
> - L2: platform token + V4Market hook (univ4_hook, pairWith eth, poolBps 7000, remainderTo the escrow).
> - L3 (job A): Params, GameRegistry, RewardPool, FarmRewards, FarmCore, FarmItems, PackSale, StarterClaim, then the binder-only Desk.bind.
> - L4 (job B): FeeRouter, GridOperator, Season, FarmEngine, Economy, Enhancement, Civic, Billboards, then permissionless wiring (register roles, bindFeeRouter, escrow forward, fundEndowment).
> Read these contracts in full, with priority on everything except SwarmDesk and EndowmentEscrow, which have already been reviewed twice.
>
> Already known and accepted (do not re-report unless you find a new impact): the binder trust and liveness, M-2 matching twin, stream-0 answers before role 1, Economy._insert 33-tie lock griefing, Festival band dead code, PackSale.buyPacksFor gifting, one-shot escrow, Season.rollover before finalize, FeeRouter.executeSells sweep rollback, FarmRewards same-epoch vintage back-dating, future-block randomness, exact-input swaps only, spot() bounds, fixed oracle endpoints, reserved Params keys, RewardPool shortfall repair by plain transfer, and the farmDaily basis (fixed: sticky, decays 1/96 per epoch).
>
> Deliver for every finding: severity, contract and line, a runnable Foundry reproduction, whether a launch judge would block it, and for medium or higher the minimal fix plus which creation-code pins it changes. If nothing blocks, say so explicitly per launch (L2, L3, L4). Do not change source.

| | |
|---|---|
| Repository | https://github.com/identity-md-launches/launch-1593-blackout-v3-16-l1-robinhood.git |
| Commit | `1e4490923f20a389ecb6be136121f4eea65db3b1` |
| Job | `339b6b19-3df3-4420-8cfc-dcf78059d7c0` |
| Judged | 2026-10-13 17:37 UTC |
| Findings | 1 medium · 3 low · 4 info |

Four agents audited the code as it is at `1e44909`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: Enhancement: the player can throw away failed or burning draws by letting the 256-block window lapse and re-arming

`src/Enhancement.sol:98`

```
        if (h == bytes32(0)) {
```

L4, role 11. resolve() is a pure function of blockhash(target), and that hash is public as soon as the target block is mined. capture() turns an expired window (more than 256 blocks) into a re-arm with a new target instead of a final outcome. The attempting player can therefore read the outcome off-chain, call resolve() only on a success, and otherwise wait about 256 blocks (roughly a minute on an Arbitrum-Orbit chain) and re-arm. Repeated, every enhancement succeeds and none burns, which removes the item sink that the 50-90% burn chances at levels 8-16 provide. Unlike PackSale, StarterClaim and GridOperator, Enhancement.capture pays no EntropyBounty (FeeRouter.payWork only admits roles 4, 5, 7 and 8), so the only thing that closes the window is the project's own keeper (keeper.mjs 'enhancement capture'). This is a new, specific impact of the accepted future-block-randomness line: here the re-roll is fully player-selectable and decides the outcome. A launch judge would likely not block L4 (same entropy class as the accepted line) but should record it as an economics risk. Minimal fix (changes only the Enhancement creation code, role 11, so it changes ModuleCode/GameRegistry and therefore the frozen L1 pin): when the window has expired, resolve the attempt as a forced failure without burn (or at least without success) instead of re-arming. Alternative: pay an EntropyBounty from capture(), which also changes the FeeRouter pin (role 6), because payWork's caller list must admit module 11.

**Reproduction**

test/scratch/Review.t.sol::testEnhancementRearmGrind, run with the BaseTest fixture (all features enabled). veteran(alice) at level 10, item at overclock 7 (level 8: chance 30, burn 50), alice commits. Each round rolls to target+1 and sets the target hash. The first two hashes are forced to be failing draws. On a failing draw alice rolls to target+257 and calls capture(id), which re-arms the attempt (EnhancementRearmed, still pending). On the first successful draw she calls resolve(id). Expected: the first unfavourable draw resolves as a failure, with a 50% burn chance. Actual: 6 draws discarded, and the test asserts overclock == 8 with alice still the holder. PASS on this tree.

### 2. Low: GridOperator: a submitted swarm plan is silently dropped and the epoch falls back to a seed known in advance if resolve(e) misses the 256-block window

`src/GridOperator.sol:200`

```
            ? keccak256(abi.encode(address(this), e, "fixed fallback"))
```

shift(e) sets target = number()+1. If nobody calls resolve(e) within 256 blocks (about one minute of Orbit blocks on chain 4663), _resolve takes h == 0. It then ignores the submitted Plan (kind := fallbackKind(e), severity := 10000 even when the swarm attested 3000-7000) and uses seed = keccak256(grid, e, 'fixed fallback'), which can be computed before the epoch starts. The district draw, per-farm outage/surge/theft rolls and supply drops for that epoch are then known ahead of time, and the L1 SwarmDesk plan pipeline has no effect for it. This goes beyond the accepted 'future-block randomness' line: the plan is discarded, and the fallback is fully deterministic rather than merely weak. A launch judge would not block L4, but the runbook should make 'resolve(e) within about 60 s of advanceEpoch' a hard keeper duty. Fix (GridOperator pin, role 7): re-arm the target while a plan is submitted, as PackSale and StarterClaim do, or derive the fallback seed from a later block.

**Reproduction**

test/scratch/Review.t.sol::testSubmittedPlanDiscardedAfterHashWindow. Swarm submitPlan(e, Fire, 5000, ...); advanceEpoch() (shift(e)); vm.roll(+300); grid.resolve(e). Expected: the attested Fire event at severity 5000, seeded from the block hash. Actual: eventAt(e) has severity 10000, seed == keccak256(abi.encode(grid, e, 'fixed fallback')) and kind != Fire. PASS on this tree.

### 3. Low: Economy.unlock reverts while the epoch is stale (live() false), contrary to 'Unlock is never gated'

`src/Economy.sol:156`

```
        IEconomyCore(registry.module(2)).syncFor(msg.sender);
```

unlock() calls FarmCore.syncFor -> _prepare, which reverts TooEarly when !rewards().live() and CatchUpRequired when the locker is more than 8 epochs behind. Between the end of an epoch's window and the next advanceEpoch call, a matured lock cannot be withdrawn, and if epochs stop advancing the principal stays in Economy. No funds are lost, because anyone can advanceEpoch and the full amount is then paid. This is a liveness gap and contradicts the NatSpec. A launch judge would not block. Fix (Economy pin, role 10): skip the weight resync when !live(); boostAt already reads the deleted lock, so the next owner action re-syncs.

**Reproduction**

test/scratch/Review.t.sol::testUnlockBlockedWhileEpochStale. alice places an item, locks lockQuote(alice,7) for 7 days, warp +8 days with nobody advancing (live() == false), unlock(). Expected: the principal is returned. Actual: revert TooEarly(). PASS on this tree.

### 4. Low: FarmCore.process removes a Surge-destroyed item from the loadout without resyncing; FarmRewards.claim then re-commits the stale weight for 12 more epochs

`src/FarmCore.sol:547`

```
            if (id != 0 && items().data(id).holder == address(0)) _remove(f, id);
```

When FarmEngine._damage destroys an item (2% Surge roll, rarity < 3), FarmCore.process removes it from loadout/active but never calls _sync, and it cannot, because setWeight requires a caught-up account. FarmRewards.claim (line 538) re-commits a.nextWeight verbatim for IDLE_EPOCHS. The global denominator (nextTotalHash and the district hash) therefore keeps the destroyed item's hash. That dilutes every other farm's reward per hash and inflates districtActiveHash for wars until the owner places, unplaces or syncs. The farm itself does not gain (gross is bounded by its real productive hash). A launch judge would not block. Fix: in FarmRewards.claim, re-commit a weight recomputed from the loadout (FarmRewards pin, role 1), or have FarmCore flag the farm for a resync on its next action (FarmCore pin, role 2).

**Reproduction**

test/scratch/Review2.t.sol::testDestroyedItemWeightStale. alice places two items (weight W). Step one epoch, then the engine destroys item A. The test mocks FarmItems.maintain for A only, because the real Surge path zeroes the snapshot slot so maintain is never called on the destroyed id. Step: process _remove()s A. alice claims half her pending balance. Expected: committed weight drops to the one-item hash. Actual: configuredWeight(alice) == W and farmWeight(alice, epoch+1) == W, while a subsequent farm.sync() lowers it below W. PASS on this tree.

### 5. Info: Civic.claimWar floors each winner's share; the rounding remainder is stuck in Civic forever

`src/Civic.sol:212`

```
        amount = Math.mulDiv(w.payout, contribution[id][msg.sender], w.winningChest);
```

The per-winner payouts are floored, so their sum is below w.payout whenever the division is inexact. No path moves the remainder, and `escrow` permanently overstates claimable tokens by up to (winners - 1) wei per war. Accounting hygiene only. Fix (Civic pin, role 12): track the amount claimed per war and send the remainder to the pool once all claims are in.

**Reproduction**

test/scratch/Review2.t.sol::testWarDustStuck. Feature 0 enabled, startWar(0,1). District-0 wallets X and Y fund 1e18 and 2e18; district-1 wallet Z funds 1e18+1. Warp 48h, finishWar(): payout = 3.5e18. X and Y claim. Expected: escrow() == 0. Actual: escrow() == 1, with 1 wei left in Civic (assertion 'escrow dust left: 1 != 0').

### 6. Info: PackSale.openPack (and FarmCore.buyTokenPack) charge the curve price at execution with no maximum-cost bound

`src/PackSale.sol:163`

```
        return _buy(msg.sender, msg.sender, n, type(uint256).max, false);
```

openPack passes maxCost = type(uint256).max, and buyTokenPack charges price() at execution. Any purchases that land first raise the buyer's cost by 1% per pack above target, up to the ceiling, with no revert. buyPacksFor(msg.sender, n, maxCost) already offers the bound, so the UI can avoid the problem without a source change. Not a blocker. A contract fix would change the PackSale pin (role 4) and, for buyTokenPack, the FarmCore pin (role 2).

**Reproduction**

test/scratch/Review2.t.sol::testOpenPackNoCostBound. quote(1) = 15000e18. alice openPack(20), then bob openPack(1). Expected: bob pays the quoted 15000e18 or the call reverts. Actual: bob pays 18302.85e18 (+22%). PASS on this tree.

### 7. Info: Unused minter/caller permissions: FarmItems.mint admits Season (role 8) and Season.recordSpend admits GridOperator (role 7)

`src/FarmItems.sol:93`

```
            || msg.sender == season() || msg.sender == registry.module(12);
```

Season never calls FarmItems.mint (its prizes go through PackSale), and GridOperator never calls Season.recordSpend (src/Season.sol:153, `msg.sender != grid()`). Both are dead permissions that widen the trusted-caller set. They are harmless only because the module code is pinned. Trust-surface note only, not a blocker.

**Reproduction**

grep -n '\.mint(' src/Season.sol and grep -n recordSpend src/GridOperator.sol both return nothing, yet FarmItems.mint (line 92-93) admits registry.module(8) and Season.recordSpend (line 153) admits grid().

### 8. Info: Dead fields and constants: FarmEngine Snapshot.paid, PackSale Commit.expired, Season.BEST_SPEND_CAP

`src/FarmEngine.sol:71`

```
        f.paid = paid;
```

FarmEngine.allocationHash writes Snapshot.paid but nothing reads it, so the paid flag FarmCore passes has no effect. PackSale's Commit.expired is never set, so PackOpened always emits expired=false (src/PackSale.sol:291). Season.BEST_SPEND_CAP = 1 ether (src/Season.sol:98) is declared public but never used; the best-spender score is capped by farmDaily*7 instead. The requester should confirm that no intended paid/unpaid rule is missing. Cosmetic only; not a blocker.

**Reproduction**

grep -n '\.paid' src/FarmEngine.sol shows only the assignment at line 71. grep -n 'expired =' src/PackSale.sol returns nothing. grep -n BEST_SPEND_CAP src/*.sol shows only the declaration.

---

Judge's submission `d26870b9697956d37449760ef06e4a98a7cd662998460e6cfbd29f1d48291d4d`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
