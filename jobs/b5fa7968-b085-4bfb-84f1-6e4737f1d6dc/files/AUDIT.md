# Audit report

> Adversarial review, ROUND 3, of the Regen rail in github.com/ToknWrks/imdo at the given commit (branch regen-rail, PR #1): src/regen/ and its tests, script/DeployRegenRail.s.sol, and the OffsetsForwarder seat in script/DeployImdo.s.sol. Foundry; Solidity 0.8.26, evm_version cancun, via_ir, optimizer_runs 44444444, bytecode_hash = "none"; vendored lib/. The rest of the tree was reviewed by IMD swarm job 37ac5d94-da10-4a27-84d9-246c17a2c3f7 and is NOT in scope except where the rail touches it.
>
> Rounds 1 and 2 were IMD swarm jobs 9091d583-d490-481f-8015-08f9d4df9009 (commit 43935b0) and e9b9f179-0ede-42aa-8695-3c731c1dff64 (commit ac40001; 1 high, 1 medium, 6 low, 3 info). All round-2 findings were answered in the commit under review. The point of this round is to BREAK THE ROUND-2 FIXES and find what both rounds missed, not to restate them. The round-2 fixes:
> - High (the time-weighted bar followed a price HELD across the window: Aerodrome writes an observation on any state change, sync() is public): three things now stack. (1) twapGranularity is intended to be 48 completed intervals (>= 24 h) and the reference takes the pool's fee off (IAerodromeFactory.getFee(pool, stable) via pool.factory(); fee >= 10000 reverts referenceTonnes, which the plan treats as priceOff). (2) processInterval (intended 7200 s): one retirement per (project, depositor) per interval, revert TooSoon(nextAt); lastRetiredAt is set only on a retirement, not on a skip. (3) maxUsdcPerTonne (intended 45e6 USDC per 1e18 t): an ABSOLUTE ceiling checked in _offer as spend * 1e18 > maxUsdcPerTonne * tonnes -> priceOff. The fork test holds an 8,000 USDC pump for 25 h with sync() every 1801 s: the relative bar follows exactly and the ceiling refuses at $48.5/t. The NatSpec and docs/REGEN_RAIL.md state the residual: a mover who holds the pool off its average for a full window under the ceiling can take, per depositor, (24h / processInterval) x maxBatch x (1 - market / maxUsdcPerTonne) a day (about $790 at the intended values, against ~$15k of capital in the pool for a day).
> - Medium (the live aggregator quotes its curve regardless of the class vault, so a depleted class reverted every full batch after ~14M gas): _offer caps tonnes at IERC20(credit).balanceOf(classVault) before flooring; the rest of the batch's dollars carry.
> - Low: retireCreditViaKlima gets maxInputTokenIn = min(held, spend + spend*10/10000 + 100) and the same allowance (an execution that pulls more reverts SlippageExceeded and the credit is passed over); dollar remainders are per (project, depositor) (usdcOf[projectId][depositor]; a 1-wei depositor plans on its own zero carry and skips classEmpty); RegenRegistry's constructor(name, regenAddress, beneficiary) registers the first project in the registry's own creation (empty name = none) and DeployRegenRail uses it, then checks count()==1 and project(1).beneficiary; validRegenAddress returns false for any byte >= 0x80; DeployRegenRail preflight requires IUniswapV3Factory(ISwapRouter02(swapRouter02).factory()).getPool(weth, usdc, v3Fee) != 0 and a non-empty projectName.
> - Info: _onClamp reads ethUsd.aggregator(), minAnswer() and maxAnswer() with raw staticcalls and exact 32-byte return checks; a proxy without aggregator(), an aggregator with no code, or a malformed answer means "no clamp", never a revert.
>
> Config now has 21 fields: registry, aggregator, usdc, kvcm, kvcmPool, classVault, creditA/B/C, venue, ethUsd, sequencerUptime (optional), maxFeedAge, minBatch, maxBatch, bountyBps, minOutBps, twapGranularity, minTonnesBps, maxUsdcPerTonne, processInterval. Intended Base values: 0.001 / 0.05 ether, bounty 50 bps, minOut 9700, maxFeedAge 3600, granularity 48, minTonnes 9500, ceiling 45e6, interval 7200. Everything else is as the round-1 and round-2 briefs described; read the source.
>
> Review questions (each needs a concrete answer):
> - The ceiling and the interval. With the relative bar assumed beaten (a full-window hold), is the stated residual right, and is there a cheaper path: many depositors for one project (anyone can deposit under any address; does the per-depositor interval let a mover process its OWN deposits faster, and does that matter when the loss is the project's?), a pump that sits just under the ceiling, a ceiling-tolerant partial hold, or exploiting the fee-exclusive/inclusive difference? Can lastRetiredAt be reset or bypassed (a skip, a revert, a forfeited bounty, a receiver redeploy)? Is the interval a liveness problem for the bridge receiver (one batch per 2 h = 0.6 ETH/day per depositor)?
> - The vault cap. IERC20(credit).balanceOf(classVault) is read as "retirable supply": is that what the live Klima aggregator actually retires from (LibRetire / the class vault contract at 0xf4699531e0a5F6e9351a36De3753Deaad329Bf45), can the vault hold credit it will not release (locked, pending, another class), and can a mover change that balance within a transaction to shape the offer (donate credit to the vault, or make the vault's balance read revert)? Does capping tonnes at the vault re-open the round-2 "saturation bypass" (both sides of the comparison capped) now that the ceiling exists?
> - Spend-bounded pulls. Is spend + 0.1% + 100 enough slack for the live aggregator's round-up on every batch size (round 2 measured 1-18 micro-USDC); can the aggregator legitimately need more (its DiscountedForwardBalanceContext / rate limiter) so honest batches are passed over forever?
> - Per-depositor dollars. Verify the accounting invariants (USDC balance == sum of usdcOf; nothing moves between depositors); is a remainder that can never be spent possible (a depositor whose ETH is gone and whose carry is under a tonne step, with every batch too small)?
> - The registry constructor. Does registering in the constructor change msg.sender semantics or events in a way an indexer would misread; can the deploy still be front-run (the registry creation itself is one transaction; is there any window left between it and the receiver's deployment that matters)?
> - The clamp read. Is the raw staticcall decode safe against a proxy that returns more than 32 bytes, or an int192 encoded differently; could it ever read a clamp from the wrong phase aggregator?
> - Fee read. Can Aerodrome's factory fee for this pool be changed, by whom, and what does each value do to the rail (0, 30, 300, custom)?
> - Everything else: anything from rounds 1-2 not actually fixed, and anything new.
>
> Rules: read-only review; do not modify src/, script/, foundry.toml, lib/ or test/ outside test/scratch/. Scratch tests only under test/scratch/. Every finding needs a severity, exact file:line, a concrete reproduction and, where possible, a Foundry proof that fails on this code. Run forge test (201 tests in the default profile, including test/invariant/RegenRouter.invariant.t.sol) and forge fmt --check, and report the result. Fork tests (10) run with FOUNDRY_PROFILE=fork: test/fork/RegenRouterBaseFork.t.sol forks Base at blocks 52335751 and 52487479 (env BASE_RPC_URL, default https://mainnet.base.org; note that on a fork vm.warp(block.timestamp + x) only takes once, drive the clock from a local), test/fork/OffsetsForwarderMainnetFork.t.sol forks Ethereum latest (env ETH_RPC_URL, default https://ethereum-rpc.publicnode.com); skip and say so if no RPC is reachable. Do not claim an audit; this is a review by the IMD swarm. Wording in any report: "regenerative contribution" and "retired credits", never "carbon offset" or "net zero".

| | |
|---|---|
| Repository | https://github.com/ToknWrks/imdo.git |
| Commit | `aaa9f66b2754e7c3f43ec3447ef9408ae1a66d32` |
| Job | `b5fa7968-b085-4bfb-84f1-6e4737f1d6dc` |
| Judged | 2026-10-12 04:02 UTC |
| Findings | 1 medium · 3 low · 4 info |

Four agents audited the code as it is at `aaa9f66`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Medium: First-fit plan + vault cap: one step of the first credit in the class vault captures a whole batch (dust retired, full bounty paid, interval slot spent, dollars parked as an unbounded carry)

`src/regen/RegenRouter.sol:366`

```
            if (offer.credit != address(0)) return offer;
```

_plan returns the FIRST credit whose _offer is non-empty, and since the round-2 vault cap (line 379-380) an offer of any size >= TONNE_STEP is valid. When the class vault holds a little of creditA and creditB/C are deep, every batch retires only creditA's dust: process() still takes ethIn = maxBatch, swaps it, pays the caller bountyBps of ethIn (line 241, not of what was retired), sets lastRetiredAt (line 261) and parks the rest in usdcOf (line 260). Anyone who can put dust of creditA in the vault before each interval and call process() themselves is paid for doing it. It also breaks the round-2 residual: usdcOf has no bound tied to maxBatch and is spent in full on the next plan (held = carried + bought), so a mover who parks N batches this way and then holds the pool for one window prices all N batches at the held price in a single retirement. The documented bound of 12 x maxBatch x (1 - market/ceiling) per day assumes at most one maxBatch of dollars per interval. On the live system the aggregator refuses a single 1e12 step, but specialists measured on a Base fork at 52487479 that 0.01 t of C004 left in the vault captures a 0.05 ETH batch (retires 1e16, parks 125.88 USDC, pays 0.00025 ETH). A griefer needs free-floating credit, and today every credit's totalSupply equals the vault's balance. The same capture happens without any attacker whenever Klima's own retirements leave a sliver of creditA. Fix: do not stop at the first non-empty offer. Prefer the credit that spends the most of `amount`, or fall through when a vault-capped offer spends under a set share of `amount` while a later credit offers more. Pay the bounty pro rata to dollars spent, and bound the carry spent per batch to one maxBatch's worth.

**Reproduction**

Mocks with the intended Base values (22 USDC/t, oracle 2500, spot == twap). The vault holds 1e12 creditA and 1000 t each of creditB/C. The depositor deposits 0.05 ETH and the keeper calls process(1, depositor). Expected: ~5.6 t retired from creditB and a carry under 1 USDC. Actual: lastTonnes == 1e12 (creditA), usdcOf == 124,374,978, keeper paid 0.00025 ETH, and lastRetiredAt is set. Continuation (test/scratch/Explore.t.sol test_dust): 9 more intervals each seeded with 1e12 creditA bring the carry to 1,243.75 USDC. Then with spot and twap both held at 0.5 kVCM/USDC (44 USDC/t, under the 45 ceiling), one process() retires 28.39 t for ~1,368 USDC, about 11 batches of dollars at twice the market in a single batch. The proof fails with 'a full batch retired one micro-tonne: 1000000000000 < 1e18'.

### 2. Low: Relative bar is void when the class's liquid supply is below one batch: the live quoter caps both the spot quote and the TWAP reference at that supply, so a same-transaction pump goes through up to th

`src/regen/RegenRouter.sol:393`

```
            if (tonnes < bar * minTonnesBps / BPS) return p;
```

referenceTonnes asks the aggregator what the TWAP kVCM for `spend` retires. The live class quoter caps a budget quote at the class's liquid supply. Verified on Base: quoteRetireCreditForInputTokenInViaKlima(C004, 0, 1e25 kVCM, kVCM, vault, 0) returns exactly 6164.218432695479423223 t == vault.getLiquidTonnes(). _tonnesFor and the router's vault cap are both bounded by the same supply. So once the liquid tonnes L are below what a batch buys (about 5.8 t for 0.05 ETH today), tonnes = L and bar = L, and the 95% bar never refuses. A mover pumps the kVCM pool in the same transaction, with no hold and no capital tied up across the window, to just under maxUsdcPerTonne and calls process(). The batch then buys the class's last tonnes at up to 45 USDC/t against a ~21.4 USDC/t average. This is the round-2 'saturation bypass' re-opened by the aggregator's cap rather than the router's. The loss is bounded by (ceiling - market) x L per depletion, about $140 today. It recurs each time the class runs down after a refill. Fix: compare dollars, not capped tonnes. Require the TWAP kVCM for `spend` (fee off) to be at least minTonnesBps of the kVCM the aggregator needs for `tonnes` (quoteRetireCreditViaKlima with kVCM input). Alternatively, refuse when the reference equals getLiquidTonnes().

**Reproduction**

Mock aggregator with the live cap (budget quotes capped at the vault's total credit balance). The class holds 2 t of creditA. Spot is moved to 0.5 kVCM/USDC in the same transaction and twap is unchanged. plan(121e6) returns creditA, 2e18 t, spend 88e6 (44 USDC/t, 2x the average), and process() retires it. Control: with 1000 t in the vault the same pump returns priceOff. The proof fails with 'the plan accepted a 2x same-tx pump with no hold'.

### 3. Low: IERC20(credit).balanceOf(classVault) is unguarded: one credit whose balanceOf reverts halts every batch of every project instead of being passed over

`src/regen/RegenRouter.sol:379`

```
        uint256 inVault = IERC20(credit).balanceOf(classVault);
```

Every other dependency view in _offer is wrapped in try/catch so that a revert 'counts against the credit' (NatSpec 374-375) and _plan falls through to the next credit. The round-2 vault-cap read is a direct call and runs first for creditA on every plan. If creditA is paused or upgraded, or its balanceOf reverts for any reason, _plan, plan() and process() revert for every depositor and project, even though creditB and creditC are funded. No Skipped reason is emitted, and nothing in the ownerless rail can be changed. No ETH is lost, but the three-credit fall-through is dead. Fix: read the balance with a staticcall and an exact 32-byte return check, as _onClamp does, and treat a failure as 0 (classEmpty for that credit).

**Reproduction**

creditB/C each hold 1000 t. vm.mockCallRevert(creditA, balanceOf(vault), 'paused'). Deposit 0.05 ETH and call process(1, depositor). Expected: a retirement from creditB, the same as when creditA's quote reverts. Actual: revert 'paused'. The proof fails with 'paused'.

### 4. Low: A depositor's USDC carry is unreachable once its ETH balance is zero: process() reverts NothingToProcess before looking at usdcOf

`src/regen/RegenRouter.sol:237`

```
        if (balance == 0) revert NothingToProcess();
```

With the vault cap a batch can leave most of its dollars in usdcOf[project][depositor]. Those dollars are spent only by a later process() of the same pair, and process() refuses when balanceOf is zero. deposit() credits msg.sender only, so nobody else can unlock the carry, and a 1-wei stranger plans on its own zero carry. A one-off direct depositor (a Safe) therefore has its dollars stranded for good: there is no owner and no sweep. The NatSpec's 'so nothing is stranded' (line 28) does not hold. Fix: allow process() when balance == 0 && usdcOf != 0, with ethIn = 0, no swap and no bounty, planning on the carry alone (processInterval still applies).

**Reproduction**

The class holds 1 t of creditA. The depositor deposits 0.05 ETH and the keeper processes: 1 t is retired, balanceOf == 0, usdcOf == 102.375e6. Refill creditB to 1000 t and wait 7200 s. Expected: process() retires ~4.65 t with the carry. Actual: revert NothingToProcess() from any caller. The proof fails with NothingToProcess().

### 5. Info: _onClamp: abi.decode(ret, (address)) reverts on a 32-byte word with non-zero upper bits, so a malformed aggregator() reverts process() instead of meaning 'no clamp'

`src/regen/RegenRouter.sol:343`

```
        address agg = abi.decode(ret, (address));
```

The NatSpec (338-339) promises that a malformed answer means no clamp. ret.length == 32 is checked, but Solidity's ABI decoder validates the address range and reverts on dirty upper bits, so _ethUsd() and every process() revert. The int192 reads are fine: an int192 is sign-extended in the ABI, and decoding it as int256 is exact. Both aggregator() and latestRoundData() go through the proxy's current phase, so the clamp is never read from the wrong phase. The live Base proxy returns a clean address, so this is a robustness gap only. Fix: address(uint160(uint256(bytes32(ret)))) or return false when the top 12 bytes are not zero.

**Reproduction**

The feed's aggregator() returns abi.encode((1<<160) | 0x1234). Deposit 0.05 ETH and call process(1, depositor). Expected: the batch is processed with no clamp. Actual: EvmError: Revert (test/scratch/Explore.t.sol test_clamp).

### 6. Info: processInterval caps the project's bridge receiver (one depositor) at 12 x maxBatch = 0.6 ETH/day; an Offsets leg above that builds an unbounded backlog

`src/regen/RegenRouter.sol:239`

```
        if (block.timestamp < nextAt) revert TooSoon(nextAt);
```

All of a project's bridged ETH arrives under its RegenReceiver, so the per-depositor interval throttles the whole leg to (86400/7200) x 0.05 = 0.6 ETH/day. A slot spent on a dust retirement (finding 1) or lost to a skip lowers this further. ImdoTreasury sends 25% of net fees to the forwarder, so above ~2.4 ETH/day of net fees balanceOf[1][receiver] grows without bound. Nothing is lost, but the backlog keeps every one of the 12 daily slots full for a held-pump mover, and the ETH waits unhedged. This is a design trade and should be stated in docs/REGEN_RAIL.md, or maxBatch/processInterval sized for the expected leg. The interval cannot be reset or bypassed: lastRetiredAt is written only on a successful retirement, a revert rolls back, a forfeited bounty does not touch it, and the receiver's CREATE2 address cannot be redeployed. Extra depositors only give a mover more slots on its own deposits, not on the receiver's.

**Reproduction**

The depositor holds 1.2 ETH. Call process(1, depositor) as often as possible for 24 h. Every call inside 7200 s of the last retirement reverts TooSoon(nextAt), so exactly 12 batches (0.6 ETH) leave and 0.6 ETH waits.

### 7. Info: DeployRegenRail: factory.deploy(1) is permissionless, so a third party can land the receiver between the factory's creation and the script's call and make the run revert AlreadyDeployed

`script/DeployRegenRail.s.sol:111`

```
        d.receiver = d.factory.deploy(d.projectId);
```

The registry constructor closes the round-2 registration window: project 1 and its beneficiary are fixed in the registry's own creation, and ProjectRegistered carries the broadcaster as msg.sender in the creation receipt. Under broadcast, the factory's creation and deploy(1) are separate transactions, and RegenReceiverFactory.deploy reverts AlreadyDeployed(predicted) when code already exists (RegenReceiver.sol:66). The front-run receiver is identical (CREATE2, salt = id, fixed init code), so nothing is redirected. But the script reverts and d.receiver is never returned. Fix: skip deploy when predict(1).code.length != 0 and take the predicted address.

**Reproduction**

After the factory creation is mined, anyone calls factory.deploy(1). The script's next transaction reverts AlreadyDeployed(predict(1)) although the rail is fully and correctly deployed.

### 8. Info: DeployRegenRail preflight never exercises the credit leg (pool quote at twapGranularity, factory fee, aggregator quotes): a misconfigured, immutable rail deploys and skips 'priceOff' forever

`script/DeployRegenRail.s.sol:136`

```
        if (!((t0 == c.usdc && t1 == c.kvcm) || (t0 == c.kvcm && t1 == c.usdc))) revert InvalidConfiguration();
```

Round 2 added an ETH-leg preflight because 'an ownerless router whose swap always reverts has no exit'. The credit leg has the same property and is not checked. referenceTonnes runs inside try/catch (RegenRouter.sol:392-396), so a granularity beyond the pool's observation count, a factory without getFee, or an unquotable credit does not revert at deployment. Instead every plan returns priceOff or classEmpty for the life of the rail. Fix: in preflight, call kvcmPool.quote(usdc, 1e6, twapGranularity), check factory.getFee(pool, stable) < 10000, and check that each credit quotes a non-zero amount, reverting InvalidConfiguration otherwise.

**Reproduction**

By reading preflight (lines 115-137): no call reaches kvcmPool.quote, the factory fee or the aggregator. With twapGranularity larger than the live pool's observations length, Aerodrome's quote reverts, referenceTonnes reverts, and _offer's catch returns priceOff. plan() then returns credit 0 / 'priceOff' on every batch, while preflight and the five creations succeed.

---

Judge's submission `b392ea682d8720b1342cb9460049e321bdbf6b5dc18f2f9e644b256f832b1a94`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
