# 4626 governance and weekly voter rewards: IMD review

**Target:** `https://github.com/4626fun/4626` @ `f67e3733deba8196b68c7fdf7d8e8065bd07b3d4`, file `IMD_REVIEW_ARCHIVE.b64`. This is not the older contracts tree on public main.
**Archive SHA-256 (verified):** `b4c71c33cee9cb3974b74ba6815af30821cf3e0676cd013c895c0150ac334c15`. This matches the value in `IMD_REVIEW.md`.
**Upstream source per archive:** private `wenakita/4626` @ `df0a8791cde7101713ac0a4bc11a05ffc2ad8537` (PR #1727). I did not have access to the private repo. The provenance claim rests on the manifest, and all 28 files matched `SOURCE_MANIFEST.json` SHA-256 values (0 mismatches, checked before and after testing).
**Review date:** 2026-09-28. There was one reviewer (this agent). The separate "independent adversarial review of the added tests" step in BRIEF §4 was done as a self-review only. No second reviewer checked it.
**Nothing was deployed and no production Solidity, existing test, or configuration was modified.**

This review is not a certification. It covers only the scoped snapshot. Anything in the Governor, lottery execution, vaults, or deployment wiring is marked *requires wider context*.

---

## 1. Summary

| ID | Severity | Status | Title |
|----|----------|--------|-------|
| F-1 | Medium (governance; impact depends on the Governor, which is outside the snapshot) | **Confirmed by test** | `ve4626.getPastTotalSupply` is not decayed between lock mutations, so the historical total overstates the sum of `getPastVotes` (2× after 2 idle years in the PoC) |
| F-2 | Low | **Confirmed by test** | Bribes and partner-stream funds are accepted for surfaces that cannot receive votes. They cannot be claimed, have no refund or sweep path, and rollover only moves them into another unvotable epoch |
| F-3 | Low (only if the reward token charges transfer fees) | **Confirmed by test with a mock FoT token** | `ve4626VoterRewardsDistributor.notifyRewards` credits the nominal `amount`, not the amount actually received. With a fee-on-transfer token, the last claimants revert |
| I-1…I-9 | Informational / trusted-owner / by design | Mixed (see §4) | forfeitAll escrow UX, `getVotes`/delegation mismatch, owner-enabled utility transfers, checkpoint event gap, epoch-0 attribution, and others |

**Direct answer to the review question.** For the properties tested below, I found no exploitable break in:
- the simultaneous 100/100/100 rights model;
- vote, reset, and emergency-reset accounting;
- per-lane reward solvency for standard ERC-20s;
- the "earned bags never recycle" rule.

The confirmed problems are:
- **F-1:** an inconsistency in the historical-supply API that governance relies on;
- **F-2:** a stuck-funds path in the bribe and stream lanes that depends on configuration;
- **F-3:** a token-assumption gap in the fee lane.

---

## 2. Environment, commands and exit codes (facts)

| Item | Value |
|---|---|
| OS / Node | Linux 6.8, Node v24.21.0 |
| Forge | `node_modules/.bin/forge` 1.7.1 (commit 4072e48), from the npm pin. A system forge 1.8.3 was present but **not** used |
| solc | 0.8.30, via-IR, optimizer 200, Cancun (from `foundry.toml`) |
| OpenZeppelin | 5.4.0 (`node_modules/@openzeppelin/contracts/package.json`) |
| forge-std | `7117c90c8cf6c68e5acce4f09a6b24715cea4de6` (verified with `git rev-parse`) |
| Fuzz runs | 1,000 (from `foundry.toml`) |

| # | Command (run in `4626-imd-review/`) | Exit | Result |
|---|---|---|---|
| 1 | `base64 -d IMD_REVIEW_ARCHIVE.b64 > pkg.zip && sha256sum pkg.zip` | 0 | Hash matches |
| 2 | `unzip pkg.zip` | 127 | `unzip` not installed. I used `python3 -m zipfile -e pkg.zip .` instead (exit 0) |
| 3 | `npm ci --no-audit --no-fund` | 0 | npm warned that the `@foundry-rs/forge` postinstall script was not approved. The binary still ran as 1.7.1 |
| 4 | `git clone …forge-std lib/forge-std && git -C lib/forge-std checkout 7117c90…` | 0 | |
| 5 | `node_modules/.bin/forge test -vv` (baseline, before my tests) | 0 | **160 passed, 0 failed, 0 skipped, 11 suites.** Same as `validation/RESULTS.md`. Compile plus run took about 92 s wall clock |
| 6 | `node_modules/.bin/forge test -vv` (baseline plus `test/imd/`) | 0 | **183 passed, 0 failed, 0 skipped, 13 suites** |
| 7 | `node_modules/.bin/forge test --match-path 'test/imd/*' --fuzz-seed 0x4626` | 0 | 23 passed |

I found no differences from the supplied baseline.

**Added tests** (delivered in this repo at `4626-imd-review/test/imd/`, copied over the unpacked archive's `test/imd/`):

| File | SHA-256 |
|---|---|
| `IMDBase.sol` (real-contract fixture and mocks) | `1f7a824ae707a9d598ef4ddb6951ee6e1fdc0054e6a72c4a6c0a95bf563cab9d` |
| `IMDRights.t.sol` (10 tests) | `71ec774a94aac170f263933cf1a4c8639caf8ff0c93bebeadbca1caeda448d31` |
| `IMDRewards.t.sol` (13 tests) | `32c409a4b59fcb0fa9f1de554157349caf1c0aa175d7c4d6af6c77a2db93685a` |

To reproduce everything:

```sh
git clone https://github.com/4626fun/4626 && cd 4626 && git checkout f67e3733deba8196b68c7fdf7d8e8065bd07b3d4
base64 -d IMD_REVIEW_ARCHIVE.b64 > pkg.zip && python3 -m zipfile -e pkg.zip . && cd 4626-imd-review
npm ci && git clone https://github.com/foundry-rs/forge-std.git lib/forge-std \
  && git -C lib/forge-std checkout 7117c90c8cf6c68e5acce4f09a6b24715cea4de6
cp -r <this-delivery>/4626-imd-review/test/imd test/
node_modules/.bin/forge test -vv
```

Tests named `test_FINDING_*` **pass by asserting the vulnerable behavior**. A passing run means the defect was reproduced. It does not mean the behavior is safe.

---

## 3. Findings

### F-1: Historical total supply is not decayed (Medium, confirmed; governance impact requires wider context)

**Location:**
- `contracts/shared/governance/ve4626.sol:788-811` (`getPastTotalSupply`)
- the supply trail is written only on mutations at `:493-494` (`_checkpointUserSlope`), `:451` (`_checkpointGlobal`), and `:667-674` (`_update`)
- compare with the per-user `getPastVotes` at `:775-781`, which is decayed

**Fact:**
- `getPastVotes(account, t)` returns the power decayed to time `t`.
- `getPastTotalSupply(t)` returns the global bias *as of the last lock mutation at or before `t`*, with no decay to `t`.
- Live `getTotalVotingPower()` does decay, so the two historical APIs disagree with each other and with the live total.

**PoC:** `IMDRightsTest.test_FINDING_pastTotalSupplyStaleVsPastVotes`
- Two max locks of 100e18 each are created, then there are 2 years with no lock mutation.
- Logged results:
  - `sum getPastVotes = 99.452e18`
  - `getPastTotalSupply = 199.452e18`
  - `getTotalVotingPower = 99.452e18`

```sh
node_modules/.bin/forge test --match-test test_FINDING_pastTotalSupplyStaleVsPastVotes -vv   # exit 0
```

**Prerequisites:** none. Any period with no lock, extend, increase, or unlock activity makes the stored total go stale. Expired locks keep contributing until the next mutation.

**Impact (inference):**
- An OZ-style Governor derives `quorum(t)` from `token.getPastTotalSupply(t)`. With a stale total, quorum is overstated, up to 2× in the PoC.
- Any "share of voting power at a snapshot" computation is understated.
- The error is conservative in that quorum gets harder, not easier. It can still block proposals that should pass, which is a governance liveness and correctness failure.
- No Governor or quorum consumer is in the snapshot, so the real-world severity is unconfirmed (*requires wider context*).
- I also could not determine whether PR #1727 touched this code or whether it predates the PR.

**Minimal fix:**
- Store `(clockTime, bias, slope)` in each supply checkpoint.
- In `getPastTotalSupply(t)`, find the last checkpoint at or before `t` and project it forward to `t` with the same week walk as `_decayStateAt`, using `_slopeChanges`.
- Using the current `_slopeChanges` for this projection is sound. Later mutations only edit entries for weeks after their own timestamp, and any such mutation also creates a newer checkpoint, so weeks between a checkpoint and the query time are unchanged.

```solidity
struct SupplyCheckpoint { uint48 clockTime; uint208 bias; uint128 slope; }
function getPastTotalSupply(uint256 t) public view override returns (uint256) {
    // ...binary search -> cp ...
    return _projectBias(cp.bias, cp.slope, cp.clockTime, t); // same loop as _decayStateAt
}
```

---

### F-2: Bribe and stream funds get stuck on vote-ineligible surfaces (Low, confirmed)

**Location:**
- funding gates: `bribes/BribeDepot4626.sol:99` (`canReceiveBribes` only) and `rewards/RewardStream4626.sol:387` (`canReceiveStreams` only)
- the flags are independent: `ve4626GaugeVoting.sol:654-667` and `surfaces/GaugeSurfaceRegistry4626.sol:133-148`
- recycling paths: `BribeDepot4626.sol:158-181`, `:189-225` and `RewardStream4626.sol:454-508`
- there is no refund or sweep function in either contract

**Fact:**
- A surface can be `bribes=true`/`streams=true` with `votes=false`. It can also have votes removed or paused after it was funded.
- In either case, deposits for epoch E are accepted, but `vote()` reverts `VaultNotWhitelisted`, so the vault weight is 0 and every claim reverts `NoUserVotes`.
- The only exits are the zero-vote rollovers. They credit the *current* epoch of the same unvotable vault, so the bag cycles indefinitely.
- There is no path back to the briber or to a treasury.

**PoC:** `IMDRewardsTest.test_FINDING_bribesOnVoteIneligibleSurfaceAreStuck`
- The surface is registered as `(votes=false, bribes=true, streams=true)`.
- 100e18 is bribed and 50e18 is streamed.
- Five rollovers are performed, and the balances are still held and unclaimable in epoch 11.

```sh
node_modules/.bin/forge test --match-test test_FINDING_bribesOnVoteIneligibleSurfaceAreStuck -vv   # exit 0
```

**Prerequisites:**
- The surface-registry mode is on and a surface has mismatched flags, or
- a surface or vault is delisted or paused for votes after funding, before anyone votes. The same happens if `globalPaused` is set after deposits but before votes and then held.
- In local-whitelist mode the bribe and vote gates are the same predicate, so only the delist-after-funding variant applies there.

**Impact:**
- Third-party bribers and partners lose control of their funds.
- The funds become claimable again only if the owner later re-enables votes and someone votes in an epoch that holds the rolled bag.
- Nobody can steal the funds, so this is a lock-up, not theft.

**Minimal fix:**
1. In `bribe()` and `fund()`, also require `gaugeVoting.canReceiveVotes(vault)`. Add it to `Ive4626GaugeVotingForBribeDepot4626` and `IRewardWeightSource`.
2. Add an owner or briber recovery path for zero-vote bags whose vault is not vote-eligible after the grace period. For example, `recoverZeroVoteBag(epoch, token, to)`, which closes the epoch, is gated on `getVaultWeightAtEpoch == 0 && !canReceiveVotes(vault)`, and has an event.

---

### F-3: The fee lane credits the nominal amount (Low, conditional on the token)

**Location:** `ve4626VoterRewardsDistributor.sol:184` (transfer) and `:192` (`epochVaultRewards[epoch][vault] += amount`). By contrast, `BribeDepot4626.sol:102-109` and `RewardStream4626.sol:390-397` use balance deltas.

**Fact:**
- If the reward token delivers less than `amount`, gross obligations exceed holdings.
- The fee token is shared across all epochs, so early claimers from any epoch drain tokens that back other epochs, and the last claimants revert.

**PoC:** `IMDRewardsTest.test_FINDING_fee_feeOnTransferInsolvency`
- The mock burns 1% on each transfer.
- The distributor credits 1000e18 but holds 990e18.
- Bob's claim of about 750e18 succeeds. Alice's claim of about 250e18 then reverts.

```sh
node_modules/.bin/forge test --match-test test_FINDING_fee_feeOnTransferInsolvency -vv   # exit 0
```

**Prerequisites:** the per-vault ShareOFT, or a token recovered with `recoverVaultRewardToken`, has transfer fees, rebasing, or hooks that reduce the amount received. Whether production ShareOFTs do is **unknown** (*requires wider context*). With a standard ERC-20 this does not occur (see the solvency fuzz in §5).

**Minimal fix:** credit `received = balanceAfter - balanceBefore`, revert on 0, and emit `received`. This matches the other two lanes.

---

## 4. Informational, trusted-owner and design observations

| ID | Observation | Evidence | Classification |
|---|---|---|---|
| I-1 | `forfeitAll()` reverts entirely while a vote is live (`ve4626Utility.sol:238-239`), so it cannot drop veLottery alone. `forfeitVeLottery` still works. | `test_escrowRules` | UX. Fix: skip the ve33 part instead of reverting, or document it |
| I-2 | `getVotes` from `ERC20Votes` is not overridden. It returns 0 without self-delegation and the **undecayed** minted balance after `delegate`. `getPastVotes` (`ve4626.sol:775`) ignores delegation. `delegate` is therefore meaningless for `getPastVotes` consumers. | `test_OBS_getVotesInconsistentWithGetPastVotes` | Info, *requires wider context* (depends on which API the Governor or UI reads). Fix: override `getVotes` to return `votingPower(account)`, and disable or document `delegate` |
| I-3 | If the owner calls `ve4626UtilityToken.setTransfersEnabled(true)` (`:313`), token balances diverge from `userClaimed*`. Power stays with the sender, the receiver gets none, and the sender's `sync`/`forfeit` revert on the burn underflow (`ve4626Utility.sol:163,167,221`). | `test_OBS_ownerEnablingTransfersBreaksSync` | Trusted-owner hazard. Fix: remove the toggle or make it one-way disabled |
| I-4 | After more than 53 idle epochs, `checkpoint()` (`ve4626GaugeVoting.sol:430-443`) jumps `lastCheckpointedEpoch` past epochs that never emit `EpochCheckpointed`. In the test, epochs 1-16 were skipped. Events only; no accounting reads `_epochCheckpointed`. | `test_OBS_checkpointSkipsOldEpochs` | Info (indexers) |
| I-5 | Fee notifications made before genesis, during epoch 0, and during epoch 1 all credit epoch 0 while epoch-0 voting is still open, so voters can see the funding (the G-04 asymmetry only for epoch 0). | `test_OBS_epochZeroAttribution` | Documented "existing epoch-zero behavior" |
| I-6 | A lock that ends exactly at the epoch end projects 0 power and cannot vote in its final week (`vote()` → `NoVotingPower`), even though its live ve33 is greater than 0. | `test_finalWeekLockCannotVote` | Intended (projected epoch-end power) |
| I-7 | The owner's `emergencyResetAllVotes` (`:751-770`) zeroes current-epoch weights. Vaults whose voters do not re-vote become zero-vote and their fee bag becomes owner-sweepable after grace. Surface-flag edits can likewise block votes. | Code reading; the reset path itself is tested in `test_emergencyReset_rewardsConsistent` | Trusted-owner power |
| I-8 | `sweepStaleEpochRewards` and `BribeDepot/RewardStream.rolloverExpiredEpoch` are now zero-vote-only. They duplicate `sweepZeroVoteEpoch` and the permissionless `rolloverZeroVoteEpoch`, but with longer grace periods. | `test_bribe_doubleClaimAndEpochIsolation`, fee fuzz | Info (dead-weight compatibility selectors) |
| I-9 | `BribeDepot4626.claim` checks `InsufficientBribeBalance` against the whole contract balance, not per epoch (`:141-142`). With negative-rebasing tokens, claims for one epoch can consume another epoch's tokens. | Code reading only; **not tested** | Hypothesis. Rebasing tokens appear unsupported (the comment at `:79` says as much) |

**Non-finding (probe):** the global dual-decay total is at least the per-user sum, with a residual of a few wei. The probe measured 449,387 wei after an extend and 4.5e6 wei after all locks expired. This is negligible for 18-decimal amounts (`test_PROBE_totalResidualAfterExtendAndExpiry`).

---

## 5. Properties tested and holding (facts from passing tests)

| Property (from BRIEF / README) | Test(s) | Result |
|---|---|---|
| Capacity C allows C ve33 and C veLottery at the same time, and governance `getPastVotes` stays at C | `test_fullSimultaneousRights` | Holds. Epoch-end gauge weight is below the live C, as documented |
| Claiming or forfeiting one right never changes the other | `test_forfeitOneDoesNotTouchOther` | Holds |
| Decay clamps each right independently, and token balances equal storage after `sync` | `testFuzz_independentDecayClamp` (1,000 runs, 0 to 5 years) | Holds |
| ve33 escrow while voted; veLottery is not escrowed; reset releases the escrow | `test_escrowRules` | Holds (plus I-1) |
| A top-up re-seasons the lock (a vote reverts `LockTooRecent`) | `test_topUpReseasonsVoting` | Holds |
| Fee notification in E credits E-1; top-ups are claimable after an early claim; later epochs do not leak into E-1 | `test_fee_attributionAndTopUp` | Holds |
| Fee lane: paid ≤ gross, balance = gross − paid at every step, only 3 wei or less of dust remains, and nonzero-vote dust is unsweepable at epoch 200 | `testFuzz_fee_solvencyInterleaved` (1,000 runs, 3 voters, 4 random top-ups, random claim order) | Holds for a standard ERC-20 |
| A zero-vote sweep takes only its own epoch's amount of a shared token | `test_fee_zeroVoteSweepDoesNotTouchOtherEpoch` | Holds |
| Emergency reset: stale records are hidden, stale voters get 0 fee and bribe, and re-voters get the full denominator | `test_emergencyReset_rewardsConsistent` | Holds |
| Vault weight equals the sum of current-generation user weights after random vote, reset, and emergency-reset sequences | `testFuzz_denominatorEqualsSumOfUserWeights` (1,000 runs × 12 ops, 2 vaults, duplicate inputs) | Holds |
| Bribe: one claim per user/token/epoch, cross-epoch isolation, and nonzero-vote bags never roll at age 150 | `test_bribe_doubleClaimAndEpochIsolation` | Holds |
| Bribe zero-vote rollover moves only its own bag and closes the source | `test_bribe_zeroVoteRolloverIsolated` | Holds |
| Stream: claim once; a fund in E+1 is not claimable for E; dust claims are settled and the dust stays reserved | `test_stream_claimOncePerEpochAndLateFundIsNextEpoch`, `test_stream_dustSettledAndReserved` | Holds |

---

## 6. Coverage gaps and remaining assumptions

| Area | Status |
|---|---|
| Stateful invariant campaign (a handler across all lanes, multiple vaults and tokens, over many epochs) | **Not done.** Only property fuzzing within single tests |
| Governor / quorum consumer of `getPastTotalSupply` / `getVotes` | Outside the snapshot. F-1 and I-2 impact are unconfirmed |
| Lottery execution path consuming `calculateBoostForPosition` and `getVaultProbabilityBoostPPM` | Outside the snapshot. The boost math was read but its economics were not tested |
| Reentrant / ERC-777 / hook tokens | Not tested. All claim, fund, and notify functions are `nonReentrant` and follow CEI (code reading) |
| Rebasing and blocklisting tokens (for example, a USDC-style blocklist making a user's claim revert) | Not tested. Only the fee-on-transfer case is covered (F-3) |
| Utility or gauge rewiring (48 h timelocks) and migration of legacy reward sources | Not tested. Covered as operational work by `independent-rights-migration.md` |
| Live deployment, Base fork, deployed-bytecode equality | Not done (no deployment access, and out of scope by instruction) |
| The `_decayStateAt` 255-week walk limit | Code reading only. Max lock is 208 weeks, so the limit is not reachable with fresh locks. Legacy non-aligned locks are not covered |
| Front-end "repeat last week" and reward discovery | Out of scope |

**Assumptions:**
- Reward tokens are standard ERC-20s (except where F-3 notes otherwise).
- The owner is trusted and follows the documented bootstrap wiring: `gauge.setUtility`, `utility.setGaugeVoting`, and `boost.setUtility`.
- Epoch alignment: `ve4626._weekFloor` and gauge genesis are both Thursday 00:00 UTC, which the tests rely on and which I observed to hold.

## 7. Facts vs inferences vs open questions

- **Facts:**
  - archive hash and manifest integrity;
  - baseline 160/160 and full 183/183 results with exit 0;
  - the behaviors asserted by the named tests;
  - the file and line locations above.
- **Inferences:**
  - F-1's effect on a Governor's quorum;
  - the impact of F-2 on bribers;
  - the real-world relevance of F-3, which depends on the ShareOFT's transfer semantics;
  - the severity ratings.
- **Open questions:**
  1. Which contract consumes `getPastTotalSupply`, `getVotes`, or `delegate` in production?
  2. Do any production ShareOFTs charge fees or rebase on transfer?
  3. Is registering `votes=false, bribes/streams=true` surfaces an intended operating mode?
  4. Did PR #1727 change `getPastTotalSupply`, or does the issue predate the PR?
