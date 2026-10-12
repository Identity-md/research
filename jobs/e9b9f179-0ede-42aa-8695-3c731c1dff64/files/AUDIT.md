# Audit report

> Adversarial review, ROUND 2, of the Regen rail in github.com/ToknWrks/imdo at the given commit (branch regen-rail, PR #1): src/regen/ and its tests, script/DeployRegenRail.s.sol, and the OffsetsForwarder seat in script/DeployImdo.s.sol. Foundry; Solidity 0.8.26, evm_version cancun, via_ir, optimizer_runs 44444444, bytecode_hash = "none"; vendored lib/. The rest of the tree was reviewed by IMD swarm job 37ac5d94-da10-4a27-84d9-246c17a2c3f7 and is NOT in scope except where the rail touches it (ImdoTreasury.payOffsets/offsetsSafe, DeployImdo's forwarder prediction).
>
> Round 1 was IMD swarm job 9091d583-d490-481f-8015-08f9d4df9009 at commit 43935b0 (1 high, 2 medium, 7 low, 4 info). All were answered in commits a245307 and ac40001. The point of this round is to BREAK THE FIXES and find what round 1 missed, not to restate it. The fixes:
> - High (no floor on the USDC -> kVCM leg; the aggregator prices kVCM at the spot of Aerodrome USDC/kVCM pool 0x5C0D76fab1822bDeb47308eD6028231761ED723E, ~15.8k USDC): RegenRouter now plans every credit's offer (_offer: aggregator quote for the dollars floored to TONNE_STEP 1e12, then the USDC the aggregator asks for those tonnes via quoteRetireCreditViaKlima.retirementPrice, one step less if that overshoots) and holds the tonnes to minTonnesBps (9700) of referenceTonnes = the aggregator's kVCM-input quote for kvcmPool.quote(USDC, spend, twapGranularity 4) (Pool.quote is Aerodrome's time-weighted price, observations >= 30 min apart, fee-exclusive). Planned BEFORE the ETH leg with minUsdcOut(ethIn - bounty, price) + usdcOf[project] (Skipped("priceOff") or Skipped("classEmpty"), nothing spent) and again AFTER it with the real held (revert NothingRetired undoes the swap).
> - Medium: retireCreditViaKlima is in try/catch; the first credit (A, B, C order) that plans and retires wins, a reverting one is passed over; none -> revert.
> - Medium: USDC is kept PER PROJECT (usdcOf[projectId] = held - spent) and only spent on that project's batches; partial absorption allowed; donated USDC belongs to nobody.
> - Low: remainders under minBatch (and forfeited bounties) are processed by anyone with NO bounty (balance 0 -> NothingToProcess); registry names unique on nameKey (ASCII lower-cased, runs of spaces collapsed; stored as registered); regen address BIP-173 bech32 checksum verified on chain (hrp "regen"); OffsetsForwarder refuses a treasury/bridge with no code (NoCode) and bounds minGasLimit to 100000..1000000 (BadGasLimit); DeployImdo takes exactly one of offsetsSafe / receiverOnBase and for the latter predicts the forwarder at computeCreateAddress(deployer, nonce+1) just before new ImdoTreasury, creates it right after and checks treasury.offsetsSafe() == forwarder; DeployRegenRail deploys Base in one broadcast (registry, venue, router, factory, register must return id 1, deploy(1) must equal predict(1)).
> - Info: a future updatedAt skips; an ETH/USD answer on the aggregator's min/max clamp (read via the proxy's aggregator(), revert tolerated) is stale; with Config.sequencerUptime set (Chainlink L2 uptime feed 0xBCF85224fc0756B9Fa45aA7892530B47e10b6433) a batch skips while the sequencer is down or back for under SEQUENCER_GRACE (1 hour); UniswapV3Venue pins its output token (constructor(router, weth, token, fee)).
>
> Config (19 fields): registry, aggregator, usdc, kvcm, kvcmPool, classVault, creditA/B/C, venue, ethUsd, sequencerUptime (optional), maxFeedAge, minBatch, maxBatch, bountyBps, minOutBps, twapGranularity, minTonnesBps. Intended Base values: 0.001 / 0.05 ether, bounty 50 bps, minOut 9700, maxFeedAge 3600, granularity 4, minTonnes 9700. Public views: minUsdcOut, referenceTonnes(credit, amount), plan(amount) -> Plan{credit, tonnes, spend, reason}, message (grammar v1, unchanged). Everything else (registry, receivers/factory, forwarder, events, errors) is as the round-1 brief described, read the source.
>
> Review questions (each needs a concrete answer):
> - The time-weighted bar. Can Pool.quote(USDC, amount, granularity) be moved within one transaction or block on Aerodrome's Pool (Velodrome v2; observations written in _update after periodSize 1800s)? What does holding the pool off its average for the whole window cost, and what is the most that extracts per batch and in total given the bounty? What if the pool has fewer observations than granularity, or has been idle so the last observations are hours old (an old bar: exploitable, or only a skip)? Does routing the reference through the aggregator's kVCM-input quote (Klima's kVCM-per-tonne curve, moved by retirements) give the caller a second lever, at what cost? Is the fee-exclusive quote on the right side of the bar?
> - Plan before vs after. Can the divergence between the pre-swap estimate and the real held be forced so the first plan always passes and the second always reverts (the batch never retires, each caller burns ~4M gas)? Can it under-retire within the bar?
> - Per-project dollars. Can USDC move between projects, be spent under another name, or become unspendable? What does a partial absorption leave and when is it spent? Is one step of slack enough against the live aggregator's round-up (quoteRetireCreditViaKlima.retirementPrice vs what retireCreditViaKlima pulls)?
> - Fall-through. Can the (upgradeable) aggregator revert in a way that eats the forwarded gas (63/64) and derail the loop; can a callback during the retirement re-enter deposit() or defeat the approve-to-zero; any standing allowance; can a credit retire fewer tonnes than planned without reverting?
> - Remainders. With sub-minBatch balances processable for no bounty: 1-wei griefing (what does SwapRouter02 do with 1 wei, who pays), and any path where a remainder is processed at the project's loss rather than the caller's.
> - Feeds. Sequencer answer/startedAt semantics on Base, the clamp read (int192, proxy phases, a proxy that reverts), future updatedAt; anything that skips forever.
> - Registry. Is nameKey the right normalisation (digits/punctuation look-alikes still register, by design) and does it break any grammar v1 guarantee? Verify the bech32 polymod against independent vectors; is a valid-but-wrong address still the trap round 1 described?
> - Forwarder and deploy. Do the gas bounds match the real OP portal and L2 relay needs; is the nonce prediction safe against everything DeployImdo does between the two creations (HookMiner.find is pure); can DeployRegenRail leave a half-deployed rail (register reverting, id != 1 on a reused registry); is receiver-before-forwarder enforced or only documented?
> - Anything from round 1 not actually fixed, and anything new.
>
> Rules: read-only review; do not modify src/, script/, foundry.toml, lib/ or test/ outside test/scratch/. Scratch tests only under test/scratch/. Every finding needs a severity, exact file:line, a concrete reproduction and, where possible, a Foundry proof that fails on this code. Run forge test (193 tests in the default profile, including test/invariant/RegenRouter.invariant.t.sol) and forge fmt --check, and report the result. Fork tests (7) run with FOUNDRY_PROFILE=fork: test/fork/RegenRouterBaseFork.t.sol forks Base at block 52335751 (env BASE_RPC_URL, default https://mainnet.base.org), test/fork/OffsetsForwarderMainnetFork.t.sol forks Ethereum latest (env ETH_RPC_URL, default https://ethereum-rpc.publicnode.com); skip and say so if no RPC is reachable. Do not claim an audit; this is a review by the IMD swarm. Wording in any report: "regenerative contribution" and "retired credits", never "carbon offset" or "net zero".

| | |
|---|---|
| Repository | https://github.com/ToknWrks/imdo.git |
| Commit | `ac40001aabe679656db3019e27ab267a154e6b86` |
| Job | `e9b9f179-0ede-42aa-8695-3c731c1dff64` |
| Judged | 2026-10-12 02:23 UTC |
| Findings | 1 high · 1 medium · 6 low · 3 info |

Four agents audited the code as it is at `ac40001`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. High: Time-weighted bar follows a price held for one window: four free sync() calls 1801 s apart make a pumped Aerodrome pool the reference, every pending batch is then retired at the pumped price and the m

`src/regen/RegenRouter.sol:353`

```
            if (tonnes < bar * minTonnesBps / BPS) return p;
```

The credit-leg floor (round 1's high) compares the tonnes the aggregator offers at the Aerodrome spot with minTonnesBps of referenceTonnes(credit, spend), i.e. Pool.quote(USDC, spend, 4): the equal-weight mean of the last four COMPLETED observation intervals of pool 0x5C0D76fab1822bDeb47308eD6028231761ED723E. Verified on a Base fork at block 52335751: (a) a swap cannot move quote() inside its own transaction (an 8,000 USDC pump is refused with Skipped("priceOff"), so the intra-transaction part of the round-1 fix holds); (b) observations are written by ANY Pool._update more than periodSize (1800 s) after the previous one, and sync() is public and free, so the mover decides when intervals close; (c) after the pump and five sync() calls 1801 s apart (observations 6805 -> 6810, 2 h 30 min) quote() equals the pumped reserves and the bar is met at the pumped price. The bar is relative, so once the average has followed, ANY level passes; nothing bounds the loss to (10000 - minTonnesBps) as the NatSpec at lines 44-46 and docs/REGEN_RAIL.md claim. Nothing rate-limits process(): every pending (project, depositor) balance can be processed against the held price in one transaction (nonReentrant only blocks nesting), each batch moving the spot only ~0.5% off the held average, so 3-5 batches pass per hold; the mover then sells its kVCM back into the router's own buys (a classic sandwich) and collects bountyBps on each full batch. Measured on the fork (intended Base config: minBatch 0.001, maxBatch 0.05, bounty 50, minOut 9700, granularity 4, minTonnes 9700; 0.25 ETH pending): fair plan 6.114145 t per batch; after an 8,000 USDC pump and the hold, plan() returns C02-004 at 2.666217 t with an empty reason; 3 of 5 process() calls go through, 8.017516 t retired where 18.342435 t were fair (43.7%); after unwinding the attacker holds 8,173.78 USDC (started with 8,000, i.e. +173.78 after both 30 bps fees) plus 0.00075 ETH of bounties. The economics specialist's fork probe shows the trade is already profitable from a 500 USDC pump (1 batch at 93.9% of fair, +4.79 USDC). Cost of the hold: two pool fees (~48 USDC on 8,000) and two hours of inventory risk in a ~31k USDC pool whose observations are 45 min to 3 h apart (a few trades a day), with kVCM's only venue being this pool. The quote is also interval-weighted, not time-weighted: a 30-minute interval the mover closes with sync() weighs the same as a 3-hour quiet one. An idle pool (old observations) is not exploitable on its own (the spot has not moved either) and fewer observations than granularity+1 makes quote() revert and the batch skip. Fix (a design decision for the requester): the bar must not be satisfiable by a price the mover can write in ~2 hours. Options that compose: a much longer window (twapGranularity 48 or more, ~24 h at this pool's cadence, so the hold ties capital for a day in front of every kVCM holder), a second reference that cannot be moved from this pool (Klima's own kVCM pricing), a sanity bound of the spot against a long average in both directions, and a per-project rate limit of one process() per periodSize so a hold pays for one batch at most. Correct the NatSpec and docs either way. Duplicate of audit_permissions 35882b7c, audit_economics 47039cf4, audit_math 259a3f00 and audit_flow dabf1e7f, merged; the math specialist's variant (an honest downward move since the last observation, which the caller then meets by pumping up to the stale bar) is the same lag of the completed-interval average with no capital held and is covered by the same fix.

**Reproduction**

Fork Base at block 52335751 (test/scratch/ForkProbe.t.sol::test_heldPump). Deploy RegenRegistry + RegenRouter with the fork test's addresses and the intended Base config (bounty 50, granularity 4, minTonnes 9700, maxFeedAge 86400). pot deposits 0.25 ether for project 1. router.plan(124_375_000).tonnes == 6_114_145_000_000_000_000 (fair). Attacker: deal(USDC, attacker, 8_000e6); transfer to the pool; swap(getAmountOut(8_000e6, USDC), 0, attacker, ''). plan() -> reason priceOff (intra-tx pump refused). Then five times: clock += 1801; vm.warp(clock); pool.sync() (observationLength 6805 -> 6810; note: use a local clock, the optimizer hoists block.timestamp out of a loop). plan(124_375_000) -> credit C02-004, tonnes 2_666_217_000_000_000_000, reason ''. Five vm.prank(attacker) router.process(1, pot): 3 accepted (retiredOf 8_017_516_000_000_000_000), 2 skipped priceOff. Attacker sells all kVCM back: USDC balance 8_173_782_569, attacker.balance 0.00075 ether. Expected (NatSpec lines 44-46): accepted batches retire at least 97% of the fair tonnes (17_792_161_950_000_000_000) and the hold costs the mover; actual: 43.7% of fair and the mover is up 173.78 USDC plus three bounties. Offline proof test/scratch/HeldPumpProof.t.sol (miniature Velodrome v2 pool with the same reserves, fee, periodSize, observation and quote logic): FAIL, 3 batches, 8.354828 t of 19.35459 t, attacker +170.91 USDC; the same test with twapGranularity 48 passes (0 batches accepted, attacker down 39.8 USDC in fees).

### 2. Medium: Live aggregator quotes the full curve regardless of the class vault's remaining credit: at depletion every full batch reverts NothingRetired after ~14M gas and the balance is stuck until Klima refills

`src/regen/RegenRouter.sol:422`

```
        revert NothingRetired();
```

The round-1 answer 'partial absorption allowed' (NatSpec step 6, the usdcOf remainder, test_aPartialAbsorptionStaysWithTheProject) rests on the aggregator's USDC-input quote returning fewer tonnes when a credit cannot absorb the batch; the project's MockAggregator encodes exactly that (test/unit/RegenRouter.t.sol:238, tonnes capped at supply). The real aggregator does not: on a Base fork at block 52335751 quoteRetireCreditForInputTokenInViaKlima(C004, 0, 100e6, USDC, VAULT, 0) returns 4.923018 t with 2,089 t in the vault and the same 4.923018 t with 2 t in the vault, and router.plan(125e6) still returns 6.144642 t. The plan passes, the ETH leg is swapped, retireCreditViaKlima reverts for lack of credit, the credit is passed over, and when all three credits hold fewer tonnes than the batch needs (about 6.1 t for a 0.05 ETH batch today) _retire reverts NothingRetired, undoing the swap. The batch is min(balance, maxBatch) and cannot be shrunk by the caller, so any balance whose tonnes exceed the remaining credit of every class member can never be retired until Klima refills the vault, and each attempt burns ~14.3M gas on the real diamond (three full quote + retire rounds), well above the ~4M the round-1 brief assumed. Nothing is lost, but the liveness property the fix relied on does not exist on chain, and the three fixed credits are the only outlets. Fix: cap the offer at what the vault can deliver (IERC20(credit).balanceOf(classVault), or retry with the vault's balance when it is below the plan) so a credit absorbs what it has and the remainder carries as usdcOf; see the saturation finding before doing so, because a capped offer must not cap the reference too. Also document that keepers should call plan() first and not process() when the plan is empty. Duplicate of audit_permissions 37b0baad.

**Reproduction**

test/scratch/ForkProbe.t.sol::test_depletion on a Base fork at block 52335751: IERC20(C004).balanceOf(VAULT) == 2_089_267_617_052_719_475_227; quote for 100e6 USDC == 4_923_018_451_979_376_994 t; deal(C004, VAULT, 2e18); deal(C003, VAULT, 2e18); deal(C006, VAULT, 2e18); the same quote still returns 4_923_018_451_979_376_994 t and router.plan(125e6).tonnes == 6_144_642_000_000_000_000 (expected: at most 2 t, or an empty plan). pot deposits 0.05 ether; process(1, pot) reverts with 0x6cfdfba7 (NothingRetired) after 14_268_106 gas; balanceOf(1, pot) stays 0.05 ether on every later call until the vault is refilled.

### 3. Low: Bar bypass whenever the aggregator's input quote saturates: both sides of the comparison cap at the same tonnes, so a pumped pool passes and the project pays the pumped price for the whole remainder

`src/regen/RegenRouter.sol:276`

```
            aggregator.quoteRetireCreditForInputTokenInViaKlima(credit, 0, kvcmRef, address(kvcm), classVault, 0);
```

_offer compares `tonnes` (the USDC-input quote, floored) against referenceTonnes(credit, spend), which routes the time-weighted kVCM amount through the same aggregator quote. If that quote saturates at S tonnes (a credit's remaining supply in the router's own model, a daily forward-balance limit, or any cap the upgradeable diamond applies), both sides saturate at S: a pumped spot makes `spend` for S tonnes larger (up to the whole amount), the reference for that spend is still S, and tonnes (S) >= 0.97 * S passes. The bar is void exactly in the partial-absorption state the router's NatSpec (step 6) and tests describe, and the loss per batch is bounded only by `held`. On the live aggregator at block 52335751 the input quote does not saturate at the vault balance (previous finding), so this path is latent there today; it becomes live the moment the quote caps (a diamond upgrade, a rate limit that caps instead of reverting), and it is exactly what the natural fix for the depletion finding (capping tonnes at the vault's balance inside the router) would introduce. Fix: compare kVCM amounts, not tonnes that pass through a saturating curve: bar = kvcmPool.quote(USDC, spend, granularity) against the kVCM the aggregator needs for `tonnes` (quoteRetireCreditViaKlima(credit, 0, tonnes, kvcm, ...).retirementPrice), requiring kvcmNeeded >= bar * minTonnesBps / BPS. Duplicate of audit_permissions 9d6ea511; rated low rather than medium because it is not reachable on the live aggregator today.

**Reproduction**

test/scratch/Judge.t.sol::test_saturationBypass with the project's unit mocks (22 kVCM per tonne): agg.setCredit(creditA, 0.5e18), B and C 0; pool.setTwap(1e18); pool.setSpot(0.5e18) (a dollar buys half the kVCM); depositor deposits 0.01 ether. router.plan(24_875_000) -> credit creditA, tonnes 500_000_000_000_000_000, spend 22_000_000 (expected: credit 0 with reason priceOff, as the identical pump with ample supply gets in test_aPumpedKvcmPoolIsSkippedBeforeAnythingIsSpent). process(1, depositor) retires 0.5 t for 22 USDC where the honest price is 11 USDC.

### 4. Low: _retire lets the aggregator pull up to `held`, not the planned `spend`: the time-weighted bar protects the quote, not the execution

`src/regen/RegenRouter.sol:414`

```
                offer.credit, 0, 0, offer.tonnes, address(usdc), classVault, held, 0, details
```

The bar is enforced on offer.spend (quoteRetireCreditViaKlima.retirementPrice), but retireCreditViaKlima is called with maxInputTokenIn = held and an allowance of held (line 412), and whatever the diamond pulls up to held is recorded as spent. Any divergence between the quote path and the execution path (a facet upgrade, a fee applied only on execution, a different swap route on retire) is paid by the project up to the whole batch plus its carried remainder while the plan says the price was fine. On the fork at block 52335751 quote and pull agree to within 1-18 micro-USDC across six batch sizes (economics specialist's probe), so this is defence in depth against the upgradeable aggregator the NatSpec at line 53 names as the residual trust, whose bound ('one batch's USDC allowance per call') is wider than the bar. Fix: pass maxInputTokenIn = spend plus one step's price (a few micro-USDC) and approve the same, so an over-pull reverts SlippageExceeded and the credit is passed over; or check spent <= spend + slack after the call. Duplicate of audit_permissions e2b2b528 and audit_economics f1f00084.

**Reproduction**

test/scratch/Judge.t.sol::test_overPull: a wrapper aggregator that forwards both quotes to the project's honest MockAggregator but on retire pulls maxIn from the router. creditA supply 1 t, 0.01 ether deposited (held = 24.875 USDC). router.plan(24_875_000).spend == 22_000_000 (the bar passed on 22 USDC for 1 t). process(1, depositor) succeeds and the aggregator takes 24_875_000; usdcOf(1) == 0 where 2_875_000 was expected to remain. Expected: the retirement is refused when it would cost more than the planned spend plus a step of slack.

### 5. Low: validRegenAddress indexes the 128-byte charset table with any byte: a byte >= 0x80 after "regen1" panics (0x32) instead of returning false, and register() panics instead of BadRegenAddress

`src/regen/RegenRegistry.sol:129`

```
            uint8 v = uint8(CHARSET_VALUE[uint8(s[i])]);
```

CHARSET_VALUE is 128 bytes (indices 0x00..0x7F; 0x7F maps to 0xff and answers false correctly) but the index is the raw byte, up to 0xFF. A 44-byte string that starts with 'regen1' and carries any byte >= 0x80 in positions 6..43 (a UTF-8 lead or continuation byte: a Unicode look-alike pasted into an address) hits an out-of-bounds read and the public pure view reverts with Panic(0x32). Its contract, and its use as a predicate by front ends and deploy preflights, is to answer false; register() is documented to revert BadRegenAddress for a mistyped address. The existing test covers only the multi-byte case where the length check fires first ('ö' makes the string 45 bytes). No funds at risk; the input is still rejected. The polymod, generator constants, hrp expansion and the table were cross-checked by the math and permissions specialists against independently encoded vectors (regen1qqqq...vptr3e, regen1zg69v...st7gy, BIP-173 'a12uel5l') and agree; the valid-but-wrong-address trap round 1 described remains by design. Fix: `if (uint8(s[i]) >= 0x80) return false;` before the table lookup, or a 256-byte table. Duplicate of audit_permissions 173e2a6d, audit_math 8acf3dc4 and audit_flow 222753ab.

**Reproduction**

test/scratch/Judge.t.sol::test_bechHighBytePanics: bytes memory m = bytes('regen183ht37fsp2fhnq3gneyjycp08c3ju4xnvxnvan'); m[10] = 0x7F -> validRegenAddress(m) == false (fine); m[10] = 0xC3 -> validRegenAddress(m) reverts Panic(0x32) (expected false); reg.register('Other', string(m), 0xBEEF) reverts Panic(0x32) (expected BadRegenAddress()).

### 6. Low: DeployRegenRail's 'same transaction sequence so nobody can take the name or the id first' is not atomic: registry creation and register() are separate broadcast transactions and the id-1 check runs on

`script/DeployRegenRail.s.sol:95`

```
        if (d.projectId != 1) revert InvalidConfiguration();
```

Under vm.startBroadcast each `new` and each call is its own transaction: registry (tx1), venue, router, factory, register (tx5), deploy(1) (tx6). Forge simulates the script, where projectId == 1 holds trivially on a fresh registry, then sends the six transactions with fixed calldata; the checks at lines 95 and 98 are not re-evaluated on chain. The registry is ownerless and first-come, and its address is predictable from the deployer's nonce. If any register() lands between tx1 and tx5 (a watcher of fresh RegenRegistry creations, a delayed signer, or the operator's own retry after a partially sent run) then: a squatter taking another name owns id 1, the operator's project becomes id 2 without any revert, and tx6 literally runs deploy(1), i.e. deploys the CREATE2 receiver for the squatter's project; the script's Deployment reports projectId 1 and that receiver, and if the operator carries it into DeployImdo as receiverOnBase every bridged leg is retired under the squatter's name, regen address and beneficiary, immutably. A squatter taking the name itself makes tx5 revert NameTaken and leaves four contracts half deployed. Likelihood is low on Base's private sequencer; the consequence is permanent and the NatSpec (lines 14-16, RegenRegistry.sol:15-16) promises atomicity it does not have. Fix: make registry creation and the first registration one transaction (a RegenRegistry constructor that registers the first project, or a one-shot deployer contract that creates registry + registers + deploys the receiver in its constructor), and have the script assert the on-chain project(1) fields and idByName(nameKey(projectName)) == 1 after the broadcast before the receiver address is handed to DeployImdo. Duplicate of audit_permissions 344c5a53, audit_economics 37af7197, audit_math 51e3ad27 and audit_flow 4c01afde.

**Reproduction**

test/scratch/Judge.t.sol::test_deployInterleave simulates the on-chain order: new RegenRegistry(); a factory built on a router over it; attacker.register('Other', <valid regen address>, attacker); operator register('IMDO', ...) returns 2 (no revert); factory.deploy(1) succeeds and RegenReceiver(rec).projectId() == 1 whose project(1).beneficiary == attacker. On a real broadcast of DeployRegenRail.run(c) the identical interleaving between the receipt of tx1 and tx5 yields count == 2, the broadcast's register returning 2 unchecked, and Deployment.receiver == predict(1) forwarding for the squatter's project. Expected: the run registers the operator's project as id 1 or fails as a whole.

### 7. Low: A 1-wei deposit lets anyone retire a project's carried USDC (bought with other depositors' ETH) under their own `src`: provenance in the retirement message is forgeable

`src/regen/RegenRouter.sol:222`

```
        Plan memory ahead = _plan(minUsdcOut(ethIn - bounty, price) + carried);
```

usdcOf[projectId] is per project, but the retirement message names the depositor of the CURRENT batch (src:8453:<depositor>, grammar v1) and the Processed event attributes the whole spend to that depositor. deposit() only requires msg.value != 0, so any address deposits 1 wei and calls process(projectId, self): ethIn = 1, bounty = 0 (under minBatch), minUsdcOut(1, price) = 0, the ahead plan is made on `carried` alone, the 1-wei swap returns 0 USDC against a required 0 (SwapRouter02 accepts amountOutMinimum 0; the V3 pool takes a 1-wei exact input and pays 0; the caller pays the gas, nothing is lost), then _retire spends the project's carried dollars, which after a partial absorption can be most of a batch bought by the Safe or the bridge receiver. Those dollars are retired with a message naming the 1-wei depositor. Tonnes still go to the right project, so this is an attribution defect in the one field the NatSpec (line 23-24) says `src` exists for, not a loss; the ETH-side 1-wei griefing the brief asked about does not exist (the caller pays, no bounty, no revert). Fix: keep the remainder per (project, depositor), or spend carried dollars only within a batch of at least minBatch, or omit carried dollars when the batch's own dollars are below a step. Duplicate of audit_math 760f0821.

**Reproduction**

test/scratch/Judge.t.sol::test_oneWeiAttribution with the project's unit mocks: creditA/B/C supply 0.5 t each; depositor deposits 0.01 ether; process(1, depositor) retires 0.5 t from A for 11 USDC and leaves usdcOf(1) == 13_875_000. attacker: deposit{value: 1}(1); process(1, attacker) succeeds: creditB retires 0.5 t for 11 USDC of the depositor's dollars and the aggregator's RetireDetails.retirementMessage equals router.message(1, project, attacker), i.e. ends 'src:8453:0x9df0c6b0066d5317aa5b38b36850548dacca6b4e' (the attacker). Expected: the depositor's dollars are retired naming the depositor, or not by a 1-wei batch.

### 8. Low: DeployRegenRail does not check that a WETH/USDC Uniswap V3 pool exists for v3Fee: a wrong tier deploys an ownerless rail whose every process() reverts and whose ETH has no exit

`script/DeployRegenRail.s.sol:69`

```
        d.venue = new UniswapV3Venue(ISwapRouter02(c.swapRouter02), c.weth, c.usdc, c.v3Fee);
```

preflight() checks code at swapRouter02 and weth and the kVCM pool's token pair, but v3Fee goes straight into UniswapV3Venue's immutable. SwapRouter02.exactInputSingle derives the pool address from (WETH, USDC, fee) and calls it; for a tier with no pool the call hits an address with no code and reverts. The router then passes the ahead plan and reverts inside _swap on every batch: deposits are accepted (deposit() needs only the registry) but nothing can ever be retired, and router, venue and the forwarder seat are immutable with no withdrawal path. The dry run does not exercise a swap, so the mistake is visible only after the Ethereum side has bound the forwarder to this receiver. Fix: in preflight, require IUniswapV3Factory(ISwapRouter02(c.swapRouter02).factory()).getPool(c.weth, c.usdc, c.v3Fee) != address(0) (optionally a non-zero liquidity read), as the pair check already does for the kVCM pool; or have the dry run quote a swap. Duplicate of audit_flow 067440f5.

**Reproduction**

test/scratch/ForkProbe.t.sol::test_wrongV3Fee on a Base fork at block 52335751: new UniswapV3Venue(SWAP_ROUTER02 0x2626664c2603336E57B271c5C0b26F421741e481, WETH, USDC, 1234) deploys (preflight would pass: all addresses have code); swapEthToToken{value: 0.01 ether}(USDC, 0, this) reverts. With that venue in the router, process() on any deposit reverts in _swap forever.

### 9. Info: Fee-exclusive reference: the effective tolerance is minTonnesBps minus the pool fee (2.7% today); an Aerodrome custom fee at or near its 3% maximum skips every batch for good

`src/regen/RegenRouter.sol:274`

```
        uint256 kvcmRef = kvcmPool.quote(address(usdc), amount, twapGranularity);
```

Pool.quote prices on averaged reserves without the swap fee, while the aggregator's execution (getAmountOut) pays it: at block 52335751 tonnes/bar at rest is 9972 bps (fee 30 bps). The bar is therefore on the safe side (it never flatters a pump), but the honest room is 3% minus the fee, not 3%, and the fee is set per pool by Aerodrome's PoolFactory fee manager (custom fees up to MAX_FEE 300 bps). At a fee of about 270 bps or more every batch is Skipped("priceOff") forever: minTonnesBps is immutable and the ETH has no exit. The NatSpec at lines 51-52 accepts that for the aggregator; the pool fee is a second, independent switch worth naming in docs/REGEN_RAIL.md, or netting out (pool.quote * (10000 - fee) / 10000 with the fee read from the factory). Duplicate of audit_permissions b56b120b, audit_economics 89d9f03c and audit_flow 67d96950.

**Reproduction**

test/scratch/Judge.t.sol::test_feeTolerance models a 3% fee with the project's mocks: pool.setSpot(0.969e18), pool.setTwap(1e18), 0.01 ether deposited; process(1, depositor) emits Skipped(1, depositor, "priceOff") at a perfectly centred price (1.095678 t offered < 0.97 * 1.130681 t). On the fork: IPoolFactory(pool.factory()).getFee(pool, false) == 30; plan(125e6) 6.144642 t against referenceTonnes 6.161818 t, ratio 9972 bps.

### 10. Info: try/catch in _onClamp does not cover return-data decoding: a proxy whose aggregator() returns an address with no code makes process() revert instead of skip

`src/regen/RegenRouter.sol:308`

```
            try agg.minAnswer() returns (int192 lo) {
```

Solidity's try/catch only catches reverts inside the callee. Since 0.8.10 the compiler skips the extcodesize check for calls that expect return data, so a call to an address with no code succeeds with empty returndata and the ABI decoding of minAnswer()'s int192 reverts in the router, outside the catch. The same holds for any of the aggregator's quote views returning data that does not decode. On Base today the ETH/USD proxy's phase aggregator exposes both clamps (minAnswer 1, maxAnswer ~2^175) and the Klima views decode, so this is a robustness note for the 'skip, never strand' design: a low-level staticcall with a returndata length check would make the skip unconditional. Duplicate of audit_economics bf854242.

**Reproduction**

test/scratch/Judge.t.sol::test_decodeFailureReverts: a feed whose latestRoundData is fresh and whose aggregator() returns 0xE0A0 (no code); 0.01 ether deposited; process(1, depositor) reverts (expected: Skipped("feedStale") or the clamp ignored).

### 11. Info: Retirement fall-through forwards 63/64 of the gas: a credit whose retire consumes it leaves nothing for the next credit's quotes, so the batch reverts out of gas instead of falling through

`src/regen/RegenRouter.sol:413`

```
            try aggregator.retireCreditViaKlima(
```

The try forwards all but 1/64 of the remaining gas. A retire path that burns everything it is given (a loop over a large class, or a deliberate upgrade) leaves ~1/64 for forceApprove(0) plus the next credit's three quote views, which cost several hundred thousand gas on the live diamond; the loop then runs out of gas and process() reverts, so B and C are never tried and the caller burns the full gas. This sits inside the documented aggregator trust assumption and no funds move; a per-call gas cap on the retire ({gas: ...} sized from the fork's ~1.5M per retirement) would keep the fall-through alive against an expensive-but-honest credit. Duplicate of audit_economics 0fe58a36.

**Reproduction**

test/scratch/Judge.t.sol::test_gasEaterDerailsFallThrough: a wrapper aggregator whose retireCreditViaKlima loops forever for creditA and forwards to the honest mock for B and C; all three credits have supply. address(router).call{gas: 2_000_000}(process(1, depositor)) returns ok == false with empty revert data (out of gas) and agg.retirements() == 0 (expected: creditB retires).

---

Judge's submission `a379f1c3ad9cc03949299566c21a05637bef4fc9e5f912b0c64d5b9b9f993a1a`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
