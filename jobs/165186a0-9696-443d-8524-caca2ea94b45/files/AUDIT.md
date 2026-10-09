# Audit report

> Audit the SOVRN.ONE / SVO launch contracts in this repository (Solidity 0.8.26, Foundry, Uniswap v4 vendored in lib/). Scope: src/SovrnHook.sol, src/LifeForceVault.sol, src/SovrnToken.sol, src/HookFlags.sol, src/Interfaces.sol, script/PrepareLaunch.s.sol, launch.json, README.md. Tests in test/ (175 tests, run in both currency orders, plus test/Fork4663.t.sol which runs against the real chain when FORK_4663_RPC is set) are evidence to check, not the object of the audit. Intended deployment: Robinhood Chain (chain id 4663), a Uniswap v4 pool of {IMD, SVO} where IMD is the ERC-20 at 0x5F7Bb59365ce557C26dbcAa4EE9d39A4b95B7127 and SVO is a plain fixed-supply token; every trading fee is paid in IMD to an immutable LifeForceVault that only accounts for it; a fixed Safe (0xEb57c52272B90F989C41B739e2ccc5f00bF7697C) withdraws by hand. Write nothing to the repository; deliver report.md. Tone: factual and plain; no claims of safety beyond the evidence; do not call the contracts audited or secure; no investment language.
>
> CONTEXT. This code was adapted from an accepted ETH-paired version (the first commits of the branch, where the fee was native ETH): the fee currency became IMD, the hook now handles IMD as either currency0 or currency1 (decided by address order, `imdIsCurrency0`), and the vault now derives its reserves from IMD.balanceOf. Review that diff with particular care: the ETH-to-IMD generalisation is where new defects are most likely.
>
> HARD QUESTIONS (answer each with a verdict and evidence, and a reproducible Foundry test where possible):
> 1. Currency order. For both orders and for all four exact-input/exact-output modes, is `buy = (zeroForOne == imdIsCurrency0)` and `specifiedIMD = (buy == (amountSpecified < 0))` correct, are the IMD leg (amount0 vs amount1) and every sign in beforeSwap/afterSwap and their return deltas right, and does the fee always equal the stated percentage of the actual IMD leg? Can any price limit, tiny amount or rounding produce a fee that differs from the spec, a revert on a valid swap, or a fee larger than the amount?
> 2. Quote mechanism. The hook measures the real IMD delta with a self-call that always reverts, then requires the real swap to match (QuoteMismatch). Can that be broken or griefed (reentrancy, the busy flag, transient state, protocol fees, an LP-fee override, a hook-less path, concurrent unlocks)? Can the quote leave state behind?
> 3. ERC-20 fee path. Fees are taken with PoolManager.take(IMD, vault, fee), or minted as ERC-6909 claims (id uint160(IMD)) when the manager holds less IMD than the fee, then redeemed by the permissionless redeemFees(). Is the manager-balance check right, can claims be stranded or double-spent, can redeemFees be reentered, and what exactly happens if IMD reverts, returns false, takes a transfer fee, or calls back (ERC-777 style) during take or transfer?
> 4. Vault accounting. The vault has no receive hook for an ERC-20, so _reserves() derives reserves from IMD.balanceOf with a checkpoint model, floor(x*3000/10000) to buyback, a clamp so reserves never exceed the real balance (shortfall reduces buyback first), sync(), and Safe-only withdrawals paid with a low-level call. Can the Safe withdraw more than it should, can anyone grief or steal, can reserves ever exceed the balance or underflow, are rounding and dust handled, is nonReentrant correct, and is the low-level transfer return handling safe for non-standard ERC-20s? What does a malicious or upgraded IMD change?
> 5. Initialisation and addresses. beforeInitialize binds one pool: factory-only, exact currencies in address order, fee 12500, hooks == this, tickSpacing > 0. Is that complete? Hook flags 8396: does PrepareLaunch mine a valid address, can a hook with the wrong flags or a pre-initialised address slip through, does the constructor guard (block.chainid == 4663, IMD has code, token != IMD) hold, and is anything wrong with deploying the vault inside the hook constructor?
> 6. Opening-price and launch risks. What can an attacker do between pool initialisation and liquidity seeding (empty pool zero-delta swap, price manipulation, sandwiching the first-hour decaying buy fee, block.timestamp use)? Is anything in the README wrong or missing about this?
> 7. Trust and operational assumptions. IMD has an owner and unknown transfer rules; the pool manager has a protocol-fee controller; one Safe has custody of every withdrawal. State precisely what each can and cannot do to funds and trading, and whether the code or README understate any of it. In particular: what happens to trading if IMD blocks transfers to the vault?
> 8. Token. Confirm SovrnToken is plain (no owner, mint, tax, pause, blacklist), name() is exactly "SOVRN.ONE" and symbol() exactly "SVO", supply 10^27, and burn() on the vault sends only to DEAD and only SVO.
> 9. Tests and docs. Does the test suite genuinely cover the risks above in both orders (incl. mocks that misbehave), what is missing, and does every claim in README.md and launch.json match the code exactly (numbers, addresses, privileges, wording rules)?
>
> METHOD: use the Pashov methodology and specialties. Reproduce every finding against the code; discard unreproducible claims. Rate each finding by severity and likelihood, give a concrete fix, and separate real defects from documented design trade-offs. Do not claim this review substitutes for an independent human audit.
>
> RE-AUDIT. An earlier audit of commit a939314 (job 26cf0d3a-2bd3-4602-8cb8-58ba9beb5c8a) found 6 low and 3 informational issues. This commit changes: (1) LifeForceVault checkpoints are only ever raised by sync() and the withdrawals, never written down on a shortfall, and withdrawals are bounded by the clamped view; (2) SovrnHook.afterSwap reads the manager's IMD balance only when fee != 0; (3) dead ETH code removed from Guard and the unreachable clamp line removed from the vault; (4) README and launch.json now describe the IMD owner's transfer gate, the 1-of-3 Safe, pay-first router ordering, the liquidity-operations fee bypass and the vault's balanceOf dependency. Verify that each change fixes what it claims, look for new defects introduced by the diff a939314..255cafb, and re-check the nine questions above against the new code.

| | |
|---|---|
| Repository | https://github.com/SovrnOne/sovrn-contracts.git |
| Commit | `255cafb8ac44f27895db086e7b3a6f06f4124451` |
| Job | `165186a0-9696-443d-8524-caca2ea94b45` |
| Judged | 2026-10-09 12:09 UTC |
| Findings | 2 low · 6 info |

Four agents audited the code as it is at `255cafb`, each in one area (math, permissions, economics, control flow),
and a judge reproduced, merged and ranked what they found, then read the code once more itself. Nothing in the repository was changed or deployed.

## Findings

### 1. Low: Vault: IMD arriving during a shortfall refills the stored checkpoints (inference first, then buyback) instead of the documented 70/30 split, and sync() never reports it

`src/LifeForceVault.sol:101`

```
        if (balance > tracked) {
```

Introduced by the a939314..255cafb change that made the checkpoints monotone. _checkpoint() only records IMD while balance > inference + buyback, and _reserves() (line 119-120) clamps the view inference-first whenever balance < tracked. The vault cannot distinguish IMD that 'returns' from IMD that is genuinely new (hook fees, voluntary funding), so after any loss that is not reversed (an IMD seizure, blocklist confiscation, a transfer fee, any outflow not made through the vault) every subsequent receipt is credited to the unbacked part of the stored inference checkpoint first, then to the unbacked buyback checkpoint, and only receipts beyond the old total are split 70/30 again. While the balance stays below the checkpoints _checkpoint() does nothing, so sync() emits no LifeForceFunded for those receipts and the fee stream is invisible on-chain. README line 73 ('whatever arrived since the last checkpoint is split floor(x*3000/10000) to buyback and the entire remainder to inference') and line 75 ('the withdrawals record new IMD, split 70/30 as a whole') do not hold during a shortfall; the README's own explanation ('IMD that later returns restores the original split') describes only the case where the lost IMD actually comes back. Both reserves pay the same Safe, so no IMD is lost or stolen and the Safe can never exceed the balance; the defect is that the stated 70/30 accounting rule is violated by a reproducible input, and that the documented 'inference keeps priority' property is transient. This is the direct consequence of the earlier audit's request never to write checkpoints down, so it is a design trade-off to decide, not an arithmetic bug. Fix options: (a) document in README 'Vault accounting' and launch.json that receipts during a shortfall backfill the checkpoints (inference first) and are not reported by sync(), so an unreversed loss is ultimately shared across both reserves out of future income; (b) add a Safe-only acknowledgement that writes the two checkpoints down to the clamped view once, deliberately, so later receipts split 70/30 again (sync() stays unable to write down); (c) have sync() also emit when the clamped view rises during a shortfall. (b) changes agreed accounting rules and needs the requester's decision. Merges the three specialist reports of the same mechanism (economics, flow, math); their differing attributions (buyback-first vs inference-first) are both correct for their respective starting states and are both covered by the reproduction.

**Reproduction**

test/scratch/VaultShortfall.t.sol, both currency orders, all pass on the current code (forge test --match-path test/scratch/VaultShortfall.t.sol). Full loss: transfer 100 IMD to the vault, sync(): views 70/30. vm.prank(vault); imd.transfer(BOB, 100e18): views 0/0, checkpoints stay 70/30. Transfer 50 IMD of new fees: expected by README line 73 inference 35 / buyback 15; actual inferenceReserve()==50e18, buybackReserve()==0. vm.recordLogs(); vault.sync(); getRecordedLogs().length==0 (no LifeForceFunded). Transfer 30 more (80 new in total): expected 56/24; actual 70/10. The Safe then withdrawInference(70e18) succeeds. Partial loss: 100 funded and synced, 30 removed: views 70/0; 30 new fees arrive: expected 91/9 and a LifeForceFunded(0, 30e18, 21e18, 9e18); actual views 70/30 and sync() emits nothing.

### 2. Low: README and launch.json say the IMD v4 gate blocks transfers 'out of' the manager; on the live token it blocks transfers into the manager too, so liquidity cannot be added and buys fail at settlement r

`README.md:42`

```
- The owner can call `setV4Config(poolManager, gate, bool)`. It is unset today. When set for the Uniswap v4 manager, every IMD transfer **out of** that manager reverts unless the gate contract approves it. That would stop this pool's buys (the fee take), sells (the trader's IMD output) and `redeemFees()`, **and it would stop liquidity providers withdrawing their IMD**. The vault's own withdrawals to the Safe are not manager transfers and would keep working.
```

The README (and launch.json notes: 'every IMD transfer out of the pool manager reverts, which stops swaps and also stops liquidity providers withdrawing IMD') describe the gate as a restriction on the manager's outgoing transfers and list the consequences accordingly. On a fork of chain 4663 the deployed IMD applies the check to any transfer whose sender OR recipient is the configured manager. Consequences the documents miss: (a) liquidity providers cannot ADD IMD either, so a launch or top-up that seeds IMD liquidity while the gate is on fails; (b) buys fail at the router's IMD settlement (the transferFrom into the manager) even when the hook takes no fee or falls back to ERC-6909 claims, so the claims fallback is not a 'trading continues' path under the gate; (c) sells and buys with a non-zero fee fail inside the hook's take as the README already says. Confirmed as the README states: the vault's own withdrawal to the Safe keeps working (it is not a manager transfer). The gate is called by the token on both directions; a gate contract that reverts and one that returns false both produce the token's own 'BridgedFP: v4 transfer not approved' revert. This is a documentation/trust-assumption accuracy issue, not a code defect. The specialist claim that the blocklist (blocked(address)) also stops the Safe's withdrawals could not be reproduced here: the token exposes no owner-callable blocklist setter under any common name, the only gate-restricted entry point (selector 0x059c9548, 'BridgedFP: not v4 gate') accepted (vault,true) from the gate role without setting blocked(vault), so that part remains unverified. Fix: in README.md line 42 and launch.json notes replace 'out of' with 'into or out of', state that liquidity cannot be added either and that buys stop regardless of the fee path, and keep the pre-launch instruction to obtain the IMD owner's gate approval; if the blocklist's effect on the vault/Safe matters, read the verified source or ask the IMD owner, and record what was and was not verified.

**Reproduction**

Fork of chain 4663 (test/scratch/GateProbe.t.sol::test_gateDirections, RPC https://rpc.mainnet.chain.robinhood.com, run 2026-10-09). Steps: deploy the hook/vault/token on the fork with the real PoolManager 0x8366a39CC670B4001A1121B8F6A443A643e40951 and seed full-range liquidity; transfer 1 IMD to the vault; deploy a gate contract whose fallback reverts; vm.prank(IMD.owner()) IMD.setV4Config(manager, gate, true). Then: vm.prank(manager) IMD.transfer(other, 1e18) -> REVERT 'BridgedFP: v4 transfer not approved' (as README says); IMD.transfer(manager, 1e18) from an ordinary holder -> REVERT 'BridgedFP: v4 transfer not approved' (README says only 'out of'); IMD.transfer(SAFE, 1e18) -> OK; router.liquidity(key, full range +1e20) -> REVERT 'BridgedFP: v4 transfer not approved' (README says only withdrawing is stopped); buy exact-in 1 IMD and sell exact-in 1000 SVO -> both REVERT (wrapped hook error 0x90bfb865 carrying the same reason); vm.prank(SAFE) vault.withdrawInference(0.7e18) -> OK, 0.7 IMD paid. test_gateFalseReturn shows a gate returning false gives the same two reverts.

### 3. Info: README router-ordering note describes both the failing and the safe sequence with the same words; the real condition is that sync(IMD) must come after the swap, and no delivered test covers either ord

`README.md:69`

```
**Router ordering.** During `afterSwap` the hook takes the IMD fee out of the manager. A router that does `sync(IMD)`, transfers its IMD input, swaps and only then calls `settle()` is credited the input minus the fee and the swap reverts with `CurrencyNotSettled` on this pool, while it succeeds on a pool without the hook. Routers that call `sync()` immediately before the transfer and `settle()` after the swap (the Uniswap v4 router and the Universal Router) are unaffected, as are sells. An integration that pays first must add the fee to its payment.
```

The sentence 'Routers that call sync() immediately before the transfer and settle() after the swap ... are unaffected' is literally also true of the failing sequence it describes (sync, transfer, swap, settle). The property that matters is where the manager's IMD reserve snapshot is taken: PoolManager._settle computes paid = balanceOfSelf - reservesBefore, with reservesBefore taken at the last sync(IMD). Because afterSwap's take() (src/SovrnHook.sol line 226) lowers the manager's IMD balance between that snapshot and settle(), any router whose sync(IMD) precedes the swap is credited input minus fee and the unlock reverts with CurrencyNotSettled, whether its transfer happens before the swap (pay-first) or after it (sync, swap, transfer, settle). Routers that sync after the swap (Uniswap V4Router and Universal Router SETTLE_ALL) and all sells are unaffected. The claim is correct in substance and the trade-off is documented, but the wording covers both cases and the delivered suite contains no test for it (no test file mentions CurrencyNotSettled). Fix: reword to 'routers whose sync(IMD) and transfer come after the swap ... are unaffected; any router that syncs IMD before the swap must add the fee to its payment', and add a test with a pay-first router asserting CurrencyNotSettled with an exact payment and success with payment + fee. Optional code mitigation that keeps the fee rule: in afterSwap, read the manager's synced currency (TransientStateLibrary.getSyncedCurrency) and use the existing claims path when it equals IMD, so a pay-first router's settle() credits its full transfer and redeemFees() delivers the fee later; this is a design choice, not required. Merges the flow, math and permissions reports of the same mechanism.

**Reproduction**

test/scratch/RouterOrder.t.sol, both currency orders, passes on the current code at elapsed >= 3600 s (fee 3.5%). OrderRouter mode 1 (sync IMD; transferFrom payer->manager 1e18; swap buy exact-in -1e18; settle): REVERT IPoolManager.CurrencyNotSettled; the same router paying 1.035e18 succeeds and the vault gains exactly 0.035e18. Mode 2 (sync IMD; swap; transferFrom 1e18; settle), which satisfies the README sentence word for word: REVERT CurrencyNotSettled. Mode 0 (swap; sync; transferFrom; settle): succeeds, vault gains 0.035e18. grep -rn CurrencyNotSettled test/*.sol returns nothing.

### 4. Info: README understates a transfer-fee IMD: every buy on the hooked pool reverts for standard routers (CurrencyNotSettled); only sells keep working

`README.md:35`

```
- If IMD charges a transfer fee or confiscates balances, the vault's reserves shrink with its balance (see Vault accounting); withdrawals can never exceed what it actually holds.
```

For a transfer-fee IMD the README describes only the vault side (reserves shrink with the balance). Observed with the project's own MockIMD switched to a 10% fee: both buy modes revert for a router that pays exactly its debt, because afterSwap takes the full fee out of the manager while the router's transferFrom credits only the net amount, so settle() comes up short and the manager reverts CurrencyNotSettled. Sells succeed: the trader receives 90% of the net output and the vault 90% of the fee. This is a v4 settlement property, not a hook defect, and the real IMD moves exactly today (Fork4663 confirms), but the transfer-fee sentence should say that IMD-input swaps halt for standard routers, in the same way the gate and blocklist paragraphs do. Documentation only; no code change required.

**Reproduction**

test/scratch/RouterOrder.t.sol::test_feeOnTransferIMDBuysRevertSellsWork, both currency orders, passes on the current code. In the SystemBase fixture, warp 1 hour past opening, imd.setFeeBps(1000). _trade(true, -1 ether) -> REVERT IPoolManager.CurrencyNotSettled; _trade(true, 1000 ether) (buy exact-output) -> REVERT CurrencyNotSettled; an after-swap-settling custom router buying 1 IMD -> REVERT CurrencyNotSettled. _trade(false, -1000 ether) succeeds and the vault receives 31103178561117 wei, 90% of the fee the hook debited. Expected per README line 35: only the vault's reserves shrink; actual: buys are impossible until IMD stops charging the fee.

### 5. Info: IMD first checkpointed by a Safe withdrawal is never reported: LifeForceFunded is emitted only by sync(), and a later sync() finds nothing new

`src/LifeForceVault.sol:70`

```
        _checkpoint();
```

withdrawInference and withdrawBuyback call _checkpoint() to record IMD that arrived since the last checkpoint (split 70/30) but, unlike sync(), emit no LifeForceFunded for the amount they record. Because _checkpoint only raises the stored reserves, a subsequent sync() finds no new IMD and emits nothing either, so off-chain accounting that reconstructs funding from LifeForceFunded permanently under-reports every amount first checkpointed by a withdrawal. Reserve math is unaffected and README line 90 does say the event is 'emitted only by sync()', so this is observability only. Fix: emit LifeForceFunded(address(0), added, added - addedBuyback, addedBuyback) from _checkpoint (or from the two withdrawal callers) when added != 0, or state in the README that funding events are complete only if sync() is called before each withdrawal.

**Reproduction**

test/scratch/VaultShortfall.t.sol::test_withdrawalCheckpointEmitsNoFundingEvent, both currency orders, passes on the current code: imd.transfer(vault, 10e18) without sync; vm.prank(REFUEL_SAFE) vault.withdrawInference(1e18) emits only InferenceWithdrawn (zero LifeForceFunded logs); vault.sync() afterwards emits no log at all (getRecordedLogs().length == 0); the reserves sum to 9e18 as expected. Expected by an event-driven indexer: LifeForceFunded totalling 10e18; actual: none.

### 6. Info: Trust assumptions understated: IMD is a LayerZero OFT whose owner-set peers can mint IMD, and one externally owned key owns both the PoolManager and its protocol-fee controller

`README.md:43`

```
- IMD has a `blocked(address)` blocklist (false today for the manager and the Safe) and a LayerZero bridge whose peers the owner controls.
```

Read from Robinhood Chain on 2026-10-09. IMD (0x5F7B...7127) answers oftVersion() = (0x02e49c2c, 1) and exposes send, quoteSend, peers, setPeer, lzReceive, endpoint() = 0x6F475642a6e85809B1c36Fa62763669b1b48DD5B, plus updateName(string), updateSymbol(string), enableTransfers()/transfersEnabled() (true today) and the v4 gate config; it has no public mint selector. Under the LayerZero OFT standard a message from a configured peer credits (mints) the carried amount on this chain, and the owner (EOA 0x047F...54B7) can point a peer at a contract it controls, so the single owner key can in effect mint IMD without bound and sell it into this pool, diluting LP-held IMD and the IMD accumulated in the vault. The verified source was not available to this review, so the mint path is inferred from the standard the token declares, not read. Separately, the real PoolManager (0x8366...0951) has owner() = 0x2BAD8182C09F50c8318d769245beA52C32Be46CD (no code) and protocolFeeController() = 0x6d0009504D129CF5002Dba61D9Ae8575AA79314c whose owner() is the same key: that key can set a protocol fee on this pool at any time (bounded by the vendored v4-core to 0.1% of swap input per direction, taken before the LP fee, paid in IMD on buys and SVO on sells; it does not change the hook fee, see test/FeeDifferential.t.sol) and can replace the controller; it cannot pause the pool or move LP or vault funds. README line 43 names the bridge but not the minting consequence, and line 119 names the controller but not that one EOA controls it and the right to replace it, nor the fee bound. Fix: add to README 'IMD assumptions and risks' and launch.json notes that the IMD owner can mint IMD through the bridge configuration (or confirm from verified source that it cannot) and that the token has owner-controlled name/symbol updates; add to 'Validation and scope' the manager owner address and that its power is bounded to a 0.1% per-direction protocol fee with no pause or custody power.

**Reproduction**

cast call 0x5F7Bb59365ce557C26dbcAa4EE9d39A4b95B7127 'oftVersion()(bytes4,uint64)' --rpc-url https://rpc.mainnet.chain.robinhood.com -> 0x02e49c2c, 1; selectors 0x3400288b setPeer(uint32,bytes32), 0x13137d65 lzReceive, 0xc7c7f5b3 send(...), 0x537f5312 updateSymbol(string), 0x84da92a7 updateName(string), 0xaf35c6c7 enableTransfers() are present in its runtime bytecode and 0x40c10f19 mint(address,uint256) is not; cast call ... 'owner()(address)' -> 0x047F606fD5b2BaA5f5C6c4aB8958E45CB6B054B7 (no code). cast call 0x8366a39CC670B4001A1121B8F6A443A643e40951 'owner()(address)' -> 0x2BAD8182C09F50c8318d769245beA52C32Be46CD (cast code length 0); 'protocolFeeController()(address)' -> 0x6d0009504D129CF5002Dba61D9Ae8575AA79314c; cast call 0x6d00...314c 'owner()(address)' -> 0x2BAD...46CD. Not reproducible locally without the IMD source and a LayerZero endpoint; reported as understated trust assumptions, not a code defect.

### 7. Info: Plain ERC-20 IMD or SVO sent to the hook address is stranded; README covers only stray ERC-6909 claims

`README.md:65`

```
Anyone can call `redeemFees()` after settlement. It opens a manager unlock, burns all recorded claims and takes the IMD directly to the immutable vault. Failure reverts the counter reset and claim burn, permitting a later retry. The hook holds no IMD or SVO after any swap, and has no `receive()` or fallback: plain ETH sent to it reverts. Unsolicited ERC-6909 claims beyond `claimFees` sent to the hook have no forwarding or rescue function and do not divert recorded fees.
```

SovrnHook has no function that moves an ERC-20 balance it holds: redeemFees() burns ERC-6909 claims and takes from the manager, and there is no transfer, approve or rescue entry. An IMD or SVO transfer sent to the hook address by mistake (the address is public in the manifest and is where fees visibly flow) is permanently lost. README line 65 states the hook holds nothing after a swap and covers unsolicited claims, but not stray ERC-20 balances. Fee accounting is unaffected (the hook never reads its own IMD balance). Documentation note consistent with the no-admin design; a rescue function would add a privilege the design excludes.

**Reproduction**

In the SystemBase fixture: imd.transfer(address(hook), 1 ether); hook.redeemFees(); imd.balanceOf(address(hook)) is still 1e18. The SovrnHook ABI (out/SovrnHook.sol/SovrnHook.json) contains no transfer, approve, rescue or sweep function; test/Security.t.sol::test_noAdministrationEvenForFactoryOrSafe confirms there are no setters. test/RevisionBoundaries.t.sol::test_managerRoutedIMDAndUnsolicitedClaimsAreNotFeeDeposits already leaves 1 ether at the hook without a way to recover it.

### 8. Info: Test coverage: the misbehaving-IMD switches, the claims path under a protocol fee, router ordering and the first-hour liquidity-range bypass are not exercised in the delivered suite

`test/Vault.t.sol:307`

```
        imd.setFeeBps(1000);
```

MockIMD has four switches (refuses, returnFalse, feeBps, callbackTarget). refuses and returnFalse are driven through the hook and callbackTarget through the vault's withdrawals, but feeBps is used only here on a direct transfer into the vault: no test drives a transfer-fee IMD through a swap (take to the vault, router settlement) or through redeemFees(). No test makes IMD.balanceOf(manager) return less than the fee while the real balance suffices (the hook would mint claims on a funded manager; benign but untested), the claims path is never run with a non-zero protocol fee, no test exercises a router that syncs IMD before the swap (nothing in test/ references CurrencyNotSettled), and the README line 48 first-hour bypass through an IMD-only liquidity range on the hooked pool has no test (only the hookless-pool bypass does). None of these gaps hides a defect found in this review; they are listed so the suite's coverage claim in README 'Validation and scope' can be read precisely. Fix: add, in both currency orders, (a) imd.setFeeBps(1000) then _trade(true, -1 ether) expecting CurrencyNotSettled and _trade(false, -1000 ether) expecting the vault to receive 90% of the fee; (b) vm.mockCall(IMD_ADDR, balanceOf(manager), 0) on a funded pool asserting claimFees()==fee and that redeemFees() pays the vault after vm.clearMockedCalls(); (c) a FreshManagerTest with manager.setProtocolFee(key, 500 | (1000 << 12)) on the claims branch; (d) the pay-first router case from the router-ordering finding; (e) an IMD-only range one tick-spacing beyond the price at elapsed 0, a seller pushing through it, and the LP withdrawing SVO with no FeePaid event.

**Reproduction**

grep -rn setFeeBps test/*.t.sol -> only test/Vault.t.sol lines 307 and 309 (direct deposit); grep -rn CurrencyNotSettled test/*.sol -> no match; grep -n 'balanceOf(address)", address(manager)' test/*.t.sol -> only the mockCallRevert in test/Hook.t.sol line 43 (revert, not a low value); grep -n 'function test_' test/RevisionBoundaries.t.sol lists test_hooklessPoolBypassesTheHookFee and test_zeroLiquidityPriceMoveIsFree but no hooked-pool liquidity-range test. Scenario (a) is demonstrated by test/scratch/RouterOrder.t.sol::test_feeOnTransferIMDBuysRevertSellsWork and (d) by test_payFirstRevertsCurrencyNotSettled, both passing on the current code.

---

Judge's submission `8bcf724b8c60f095422abab9df0e991f8de833985816b4db337879979bd4daa5`, accepted on the IdentityMD network. Acceptance means the report met the job's checks;
it is not a guarantee that the code has no other defects.
