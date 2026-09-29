# CreatorOVault + CreatorOVaultWrapper + CreatorShareOFT: accounting-system review

Date: 2026-09-29. Scope: source snapshot only. Nothing was deployed, no transactions were sent, and no production source was changed.

## 0. Answer in brief

- **Local accounting holds (verified by tests).** In the wrapper, `totalLocked == totalMinted*1000 + totalUserDustShares`. With the modelled bridge, hub supply plus remote supply equals `totalMinted`. Vault shares are conserved. The wrapper never keeps creator coin. Small, cooled synchronous exits stayed live. These held across 16,384 stateful calls by 4 users plus a seeder. The calls covered deposit/withdraw, direct wrap/unwrap, transfers, bridge out/in, async request/claim, recognised profit and a modelled idle loss.
- **No unprivileged theft of principal was found.** Coverage has limits; see §6.
- **Confirmed weaknesses (executable, real contracts):**
  - **F-1 (Low, needs a privileged role).** The H-06 mint-backing guard in ShareOFT counts only hub-local supply. Once holders bridge out, an additional minter can mint unbacked ShareOFT equal to the bridged amount. That supply drains other users' backing, and the last holder to exit is left short.
  - **F-2 (Low, griefing, unprivileged).** Anyone can deposit into the vault with `receiver = wrapper` for at least 1% of the wrapper's shares. That stamps the pooled wrapper's cooldown and blocks every user's wrapper exit for `withdrawDelayBlocks`.
  - **F-3 (Medium if misconfigured, depends on deployment).** If the wrapper is not registered with `setTrustedAdapter`, any user's deposit (even 1 token) blocks all other users' wrapper exits in that block.
- **Independent review was NOT achieved.** See §7. Every finding below comes from a single seat (this agent) and has not been independently confirmed.

## 1. Provenance and integrity (facts)

| Item | Value |
|---|---|
| Package source | `https://raw.githubusercontent.com/4626fun/4626/1596618d1793ff86cd73f81e6540826358899ae8/` (the task pin). IMD_CREATOR_JOB.json names `1d539958d0029596398f370d70d90abfa5f08c68`. I downloaded the archive, bootstrap and foundry.toml from both commits and they are **byte-identical**. |
| `IMD_CREATOR_VAULTS_ARCHIVE.b64` sha256 | `95af4e17342ec15324b7739db26255ce5dbcb4715e21d73c525317b4127e0ede` (569,205 B) |
| Decoded ZIP sha256 | `5fe22f0051ea176b88f0d36147efd60890e39b211ed9aab83783cdf476d8fa2e`, which **matches** the required hash |
| `IMD_CREATOR_BOOTSTRAP.sh` sha256 | `be8945f06b0a70c8e8bc0a2daa10d04bfbbcc2e578932d97e77aa88288c267e6`. I inspected it before running: hash check, zip extract, `npm ci --ignore-scripts`, forge-std checkout. |
| root `foundry.toml` sha256 | `f6f9aae0a734d0f77d00f54e04fa4050c39d06c0263e14eb82412220af393f2c` |
| `IMD_CREATOR_VAULTS_REVIEW.md` sha256 | `f57e629c81610c24292437fd7a266bfc8dd9b8a556951adac7c2f8244921d03a` |
| Upstream (per manifest, not independently fetched) | `wenakita/4626@2a9e1334d5b9a13a555c6672e0ec0e735da24bf4` |
| Manifest | `python3 verify_manifest.py` returned exit 0, "Verified 109 upstream files; no mismatches". I ran it after bootstrap, again after all testing, and again on the copy committed to the repo. |
| Toolchain | forge 1.7.1 (`4072e487…`, from pinned npm `@foundry-rs/forge-linux-amd64`), solc 0.8.30, via-IR, cancun, forge-std `7117c90c…`. Linux x86-64, Node v24.21.0. |

Primary source sha256 (identical before and after testing):

```
ac06c7dce93076a64dc54eb8bc7c6cf981c377d9715f806f60461506d1a41edf  contracts/creator/vault/CreatorOVault.sol
b892208d1ae3e069d558b70d1f194fa849669f43dff67a11c49b663f81ac3938  contracts/creator/vault/CreatorOVaultWrapper.sol
bbd30551a5963638b89661ce47a304dbd0552bc1f2fdc2180f91b732586b9f65  contracts/creator/vault/CreatorShareOFT.sol
14dda6885654d1bcd93e3180d2473cf0efa8792beeeb14cda33ec271e068f220  contracts/creator/vault/modules/CreatorOVaultCoreModule.sol
e6263d4d1457246afa9af852c82be8beb058ef10825e99109a31d666c500b4f1  contracts/shared/vault/modules/OVaultAdminModule.sol
2b5f99b0c016be34555e99aafebee336457f4ffc02155d67e89042c9ae22d9e9  contracts/shared/vault/modules/OVaultStrategiesModule.sol
2c5f9cefa2dec535105b47d989d7ed1145651dd9fea7ddb8d416ba80b8b38d99  contracts/shared/lottery/venue/ShareOFTSpokeModule.sol
```

I did not review the older root `contracts/` tree of the public repo. Only the extracted `imd-creator-vaults/` was used.

## 2. Commands and exit codes (facts)

All commands ran from `imd-creator-vaults/`, with `F=node_modules/@foundry-rs/forge-linux-amd64/bin/forge`.

| # | Command | Exit | Result |
|---|---|---|---|
| 1 | `bash IMD_CREATOR_BOOTSTRAP.sh` (repo root) | 0 | 109 files verified |
| 2 | `$F test --summary` (**baseline**, unmodified, rebalance suites included) | 0 | 538 `[PASS]`, 0 fail, 0 skip. Cold via-IR compile plus run took 10m38s. This matches the stated baseline of 538 executions. |
| 3 | `$F test --match-path 'test/imd/*' -vv` (config defaults: fuzz runs 64, seed `0x46264626`, invariant runs 32 / depth 32) | 0 | 14/14 regression, 8/8 invariants (1,024 calls each) |
| 4 | `FOUNDRY_INVARIANT_RUNS=256 FOUNDRY_INVARIANT_DEPTH=64 FOUNDRY_FUZZ_RUNS=1024 $F test --match-path 'test/imd/*' -vv` | 0 | 14/14 (fuzz 1,024 runs); 8/8 invariants (256 runs × 64 depth = 16,384 calls, 0 reverts) |
| 5 | `$F test --summary` (baseline **plus** new tests) | 0 | 560 `[PASS]` (538 + 22 new), 0 `[FAIL]` |
| 6 | `python3 verify_manifest.py` (after all testing) | 0 | no mismatches |

Earlier development runs failed and I repaired the tests; none of these failures came from production code:
- The real ShareOFT needs holder allowance for wrapper burns.
- `block.number` is cached under via-IR across `vm.roll`, so I switched to an explicit block cursor.
- Vault-share approval was missing for `wrap()`.
- A 1-wei `withdraw` reverts with `ZeroAmount` (see O-4).

I did not weaken any assertion to make it pass. The one bound change is withdraw ≥ 1e9 ShareOFT-wei. It is documented in the handler, and those tiny amounts are still exercised through `unwrap`.

## 3. Findings

`test_VULN_*` tests **pass when the weakness is present** because they assert the vulnerable behaviour. File: `imd-creator-vaults/test/imd/ImdCrossContract.t.sol`.

### F-1: ShareOFT H-06 mint-backing guard ignores remote supply (Low; needs a privileged role)
- **Code:** `CreatorShareOFT.sol:511-532`. `mint` → `_assertMintBacking` requires `totalSupply()*1000 <= vault.balanceOf(wrapper)`. `totalSupply()` is **hub-local**. The OFT `send` path burns on the hub (`_debit`), but the wrapper's backing (`totalLocked`) and `totalMinted` stay the same.
- **Prerequisites:** the owner grants `setMinter(x, true)` to some address other than the wrapper, or an existing minter is compromised, and holders have bridged ShareOFT off the hub. Unprivileged users cannot trigger this.
- **Reproduction:** `test_VULN_F1_localMintBackingGuardIgnoresRemoteSupply`.
  1. Alice deposits 10,000 coin and bridges her 10,000e18 ShareOFT out.
  2. The owner grants a rogue minter, which mints 10,000e18 on the hub. **Expected:** revert `UnbackedShareMint`. **Actual:** succeeds.
  3. The rogue calls `wrapper.withdraw` and receives about 10,000 coin.
  4. Alice bridges back and also exits, using other users' backing.
  5. The seeder, the last holder, can no longer exit in full. `requestAsyncExit(seederBal)` reverts, and `totalMinted == seederBal - 10,000e18`.
- **Contrast:** `test_OK_F1_guardWorksWhenAllSupplyIsLocal` shows the same mint is rejected when there is no remote supply. The guard works only in the single-chain case.
- **Severity rationale:** the impact is full loss of the minted amount, pushed onto the last holders to exit. Likelihood needs an owner misconfiguration or key compromise, and the NatSpec at `CreatorShareOFT.sol:506-510` presents H-06 as the guard for exactly that case. So the defence is weaker than documented: Low.
- **Proposed fix (not applied):**
  - Bind the guard to global accounting: require `IWrapper(wrapper).totalMinted()` to have increased by `_amount` during the call, or allow only `wrapper` to mint on the hub.
  - Or track `netBridgedOut` in `_debit`/`_credit` overrides and check `(totalSupply()+netBridgedOut)*1000 <= held`.

### F-2: an unprivileged third party can freeze all wrapper exits by stamping the pooled wrapper's cooldown (Low; griefing)
- **Code:**
  - `CreatorOVaultCoreModule.sol:435-439` and `515-524`: third-party inflows stamp `lastDepositBlock[receiver]` when `shares*100 >= receiverSharesBefore`. Trusted adapters are exempt only for **self**-deposits.
  - `CreatorOVaultCoreModule.sol:551-552`: `WithdrawTooSoon` in redeem.
  - `CreatorOVault.sol:1914-1920`: `TransferTooSoon` on share transfers out of the wrapper.
- **Reproduction:** `test_VULN_F2_thirdPartyInflowStampsPooledWrapperCooldown`.
  1. Carol calls `vault.deposit(≈1% of wrapper value + 1e18, wrapper)`.
  2. In the same block, a cooled user's `wrapper.withdraw` and `wrapper.unwrap` both revert. **Expected:** cooled users can exit. **Actual:** everyone is blocked.
  3. Exits succeed again one block later.
- **Contrast:** `test_OK_F2_smallInflowDoesNotStamp`. A deposit below 1% does not stamp.
- **Impact and severity:** this is a liveness denial for all wrapper users for `withdrawDelayBlocks` (default 1, admin max 100 per `OVaultAdminModule.sol:779`). It can be repeated. The griefer donates ≥1% of the wrapper's value each time; that value becomes wrapper surplus that only the owner can recover through `emergencyWithdraw`. The cost is high and no funds are lost, so: Low.
- **Inference, not tested:** the same stamp probably also blocks fee-bearing `wrap` (the fee transfer out of the wrapper) and `requestAsyncExit`.
- **Proposed fix:** in `_shouldStampInflowCooldown`, return `false` when `isTrustedAdapter[receiver]`. Adapters enforce per-user cooldowns themselves, which is the stated rationale at lines 504-514.

### F-3: an unregistered wrapper lets any depositor block everyone's exits (Medium if misconfigured; depends on deployment)
- **Code:** same stamp logic. If `isTrustedAdapter[wrapper]` is false, every `wrapper.deposit` self-stamps the wrapper.
- **Reproduction:** `test_VULN_F3_untrustedWrapperDepositBlocksAllExits`. Bob deposits 1 coin and Alice's cooled `withdraw` reverts in the same block.
- **Rationale:** this denial of service is cheap and repeatable every block, but it exists only when `setTrustedAdapter(wrapper,true)` was skipped. The wrapper's `supportsShareOFTAsyncExit()` already reads that flag. I have no deployment inventory, so I cannot say whether production is affected.
- **Proposed fix:** add a deploy-time or `setShareOFT` check that the wrapper is a trusted adapter, or apply the F-2 fix together with an explicit registration check.

### Observations (Informational, tested)
- **O-1: dust is keyed to the wrapping address.** `test_OK_O1_dustStrandedButRecoverable`. After moving all ShareOFT away, a user cannot unwrap to claim dust (`unwrap(0)` → `ZeroAmount`). The dust is not lost: re-depositing folds it in, and another holder's unwrap does not receive it.
- **O-2: same-block "hot" dust transfer grief is bounded.** `test_OK_O2_hotDustTransferIsBoundedGrief`. A victim's full exit waits one block, but `balance - hot` exits immediately. This refutes a stronger denial-of-service claim.
- **O-3 (model only): wrapper cooldown is not carried through OFT burn/mint.** `test_MODEL_O3_cooldownNotCarriedAcrossBridge`. In the model, a same-block round trip to a fresh address clears it. Real LayerZero delivery takes multiple blocks, so with `wrapperWithdrawDelayBlocks = 1` I judge it not exploitable (inference).
- **O-4: sub-wei asset exits revert.** `wrapper.withdraw` of about 1 ShareOFT-wei reverts with vault `ZeroAmount` (found by the invariant campaign). `unwrap` still works. This is expected.
- **N-1: integration and test gap.** The real ShareOFT `burn` requires the holder's ERC-20 allowance to the wrapper (`CreatorShareOFT.sol:538-553`, H-3). Every wrapper exit path (`withdraw`, `unwrap`, `requestAsyncExit`) therefore needs a prior `share.approve(wrapper, …)`. The existing wrapper suites use mock ShareOFTs that skip this, so they do not cover the real burn authorization. Front-ends must request this approval.
- **TRUST: transport trust assumption, not an application bug.** `test_TRUST_authenticatedPeerCreditHasNoHubBackingCheck` shows an authenticated peer message mints on the hub with no backing check. Hub backing therefore depends entirely on peer and DVN configuration. `test_OK_lzReceive_rejectsUnauthenticatedOrigins` confirms that a wrong peer, an unknown EID and a non-endpoint caller all revert.

### Code-reading notes (not tested; inferences)
- `CreatorShareOFT._sendFeesToGauge` reverts with `HubGaugeControllerUnset` when `gaugeController == 0` on the hub. While fees are enabled and a `SwapOnly` venue is configured, every fee-bearing "buy" transfer would revert. This is a configuration liveness risk.
- `ShareOFTSpokeModule.handleLz` rejects winner-callback replay by GUID (`usedReportIds`). Remote-lottery forwards that fail are stored for retry by GUID. I did not test the retry path.

## 4. Refuted or negative results (facts, with evidence)

- **Wrapper backing equation (I1):** holds by algebra and under invariants. On wrap, Δrequired = `afterFee`. On unwrap, Δrequired = `-beforeFee`. Fees in both directions go to `feeRecipient` in vault shares (`test_OK_feesConserveShares`).
- **Global supply conservation (I3):** hub supply plus the modelled remote ledger equals `totalMinted` across 16,384 calls. A holder on another chain can bridge back and redeem 1:1 (`test_OK_globalBacking_bridgeRoundTripToDifferentUserThenExit`).
- **Dust:** held below 1 unit per user and summed correctly (I4). A fuzz test with 1,024 runs and non-trivial PPS showed every vault share accounted for through wrap and unwrap.
- **Async exits:** entries are isolated per `(adapter, owner)`. The receiver cannot claim or cancel. Claiming before unlock reverts. Double claims revert. Cancel returns raw vault shares, not ShareOFT (`test_OK_asyncExit_claimAndCancelConserveBacking`). Large synchronous withdrawals are forced into the queue.
- **Authorization:** non-vault minters need allowance to burn ShareOFT. `propagateCooldownOnTransfer` can only be called by the ShareOFT. The cooldown hook runs in try/catch, so it cannot freeze transfers (`CreatorShareOFT.sol:651-667`, code reading).

## 5. Tests added (`imd-creator-vaults/test/imd/`; also in `artifacts/imd-tests.zip`)

| File | sha256 | Content |
|---|---|---|
| `ImdSystemBase.sol` | `877bf875…3b41` | Real vault, all three modules, real wrapper and real ShareOFT. Stub LZ endpoint and remote-supply ledger (MODEL). |
| `ImdCrossContract.t.sol` | `d9a7b449…f505` | 14 tests: 3 VULN, 1 TRUST, 1 MODEL, 9 OK/negative controls |
| `ImdSystemInvariant.t.sol` | `d0f8b003…ed63` | Handler with 12 actions and 4 actors; invariants I1–I8 |

`artifacts/imd-tests.zip` sha256 is `5e8777a3fbb2f51c2e7aea0552ac49220d95ab864d94054dde8059a49d8cea6d`. It contains a README and SHA256SUMS.

**Real versus mock (evidence classes):**
- **Real contracts:** CreatorOVault plus CreatorOVaultCoreModule, OVaultStrategiesModule and OVaultAdminModule through the real delegatecall; CreatorOVaultWrapper; CreatorShareOFT, including its OFT `_debit`/`_credit`, `lzReceive` peer checks and the real spoke module.
- **Mock or model:**
  - The LZ endpoint is etched code with `send` mocked.
  - Remote chains are a ledger.
  - The registry is minimal.
  - The coin is a plain ERC20.
  - "Loss" means removing idle coin plus `syncBalances()`. No strategy is attached in the new tests.
  - **There is no fork, no real LayerZero delivery and no real strategy evidence.**

**Handler coverage (deep campaign, forge table; all handler calls return, and inner reverts are caught and classified):** bridgeIn 1371, bridgeOut 1336, claimAsync 1382, deposit 1363, directDepositThenWrap 1399, loss 1322, profit 1393, requestAsync 1318, roll 1344, transferShare 1387, unwrap 1403, withdraw 1366. Reverts: 0.

Ghost success/skip counts for the final run (depth 64):

| Action | Success | Skip |
|---|---|---|
| deposit | 5 | 0 |
| withdraw | 3 | 1 |
| wrap | 9 | 0 |
| unwrap | 5 | 0 |
| transfer | 6 | 1 |
| bridgeOut | 6 | 1 |
| bridgeIn | 4 | 2 |
| requestAsync | 5 | 0 |
| claimAsync | 2 | 4 |
| profit | 2 | 0 |
| loss | 3 | 0 |
| roll | 5 | 0 |

Skips are no-balance or no-queue preconditions. Unexpected exit reverts are asserted to be 0 (I7).

**Limitation:** forge reports ghost counts only for the last run, so per-campaign success totals are not reported. An earlier attempt at a non-vacuity assertion in `afterInvariant` broke forge's shrinking replay, so I removed it.

## 6. Coverage gaps and unanswered questions

- **Strategies:** the new tests attach no strategies. Rebalance, valuation-revert, maxLoss and hostile-strategy behaviour rests on the **retained baseline suites** (all passing), not on new evidence.
- **Impairment and recovery:** ERC-1155 claims, epoch snapshots, `OVaultRecoveryEscrow` and the wrapper's `claimImpairmentRecovery` were **not newly tested**; only the baseline suites cover them. Open question: shares queued in the vault's own balance during an async exit (`_sharesUpdate(adapter, address(this))`) could be mis-attributed in impairment snapshots. I did not verify this.
- **OVaultHubComposer, the lottery queue and fee flush/sweep paths:** not tested.
- **Delegatecall storage layout and reentrancy across facade, modules and hooks:** not independently diffed or fuzzed. I relied on the baseline `ModuleIdentity` and `MigrateStrategyReentrancy` tests.
- **Management and performance fees, profit unlocking, report timing:** not newly tested.
- **Real LayerZero behaviour:** DVN configuration, ordered delivery, `lzReceive` retry and clear, in-flight supply and enforced options are not modelled. Replay protection is assumed to come from the endpoint nonce.
- **Deployment facts:** no deployment inventory or bytecode equivalence was available. F-3 and the gauge-unset note depend on deployment.

## 7. Independent review record

- **Test writer and analyst:** Claude (Opus 5.5) acting as a single IMD agent seat in this session.
- **Independent reviewer: NOT AVAILABLE and NOT ACHIEVED.** This session had no separate reviewer seat or subagent facility, and no second human or model reviewed the code, the tests or the findings. Self-review does not satisfy the requirement. Treat F-1 to F-3 as **single-seat, unconfirmed** until a different reviewer reproduces them with the commands in §2.

## 8. Remediation priorities

1. **F-2 and F-3:** exempt trusted adapters as inflow receivers from cooldown stamping, and assert wrapper registration at deploy time. This is a small change with a large liveness benefit.
2. **F-1:** make the ShareOFT mint guard use global or wrapper accounting, or restrict hub minting to the wrapper only.
3. **N-1:** add wrapper tests against the real ShareOFT, including allowance-based burns, and document the approval UX.
4. Close the §6 gaps, especially impairment snapshots versus queued shares, and a real-endpoint or fork test of hub/spoke supply.
