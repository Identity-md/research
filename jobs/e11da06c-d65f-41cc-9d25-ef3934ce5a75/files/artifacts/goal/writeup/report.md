# PEPE RUN — goal write-up

**RUN. SURVIVE. WIN.** · Ethereum Mainnet (chain 1) · written 2026-11-28

**Status: not delivered as specified.** The goal asked to build, audit and deploy PEPE RUN at peperun.imd.site with 2 smart contracts, 1 website and 6 media assets. What exists is source code, tests, research and partial audits. Nothing is deployed on chain 1, nothing is published at peperun.imd.site, and paid play cannot be switched on under the stated economics. This report says exactly what landed, what did not, and what the requester has to decide before the rest can be built.

Evidence is cited as `[batch/item]`; section 15 lists every result with its SHA-256. "Re-run for this write-up" means I ran the trunk's own suites in a scratch clone while writing; those runs are mine and are not an independent audit.

---

## 1. Summary

| Deliverable the goal names | State | Evidence |
|---|---|---|
| Smart contract 1: `RunVerifier` (signed admissions and two-signature scores) | **Source + tests on trunk. Not deployed, not verified on an explorer.** Independently reviewed at v1 and v2: no critical or high finding in the verifier itself. | `[foundation/score-verifier]`, `[core-services-e2/protocol]`, `[foundation-review-e4/score-signatures]`, `[protocol-audit-e5/verifier]` |
| Smart contract 2: `RunArcade` (purchases, inventory, weekly jackpot) | **Source + tests on trunk. Not deployed. Not independently audited. Every purchase reverts on mainnet by design** (section 2). | `[core-services-e2/ledger]`, `[imd-mechanics-e2/burn-and-units]` |
| Website at peperun.imd.site | **Not published.** `https://peperun.imd.site/` answered HTTP 404, "Nothing is published as peperun.imd.site", when checked on 2026-11-28 at about 05:00 UTC. The trunk holds a free-practice client only; an independent review failed it as a release candidate. | section 9, `[foundation/practice]`, `[evidence-review-e2/foundation-audit]` |
| 6 media assets | **Six source packs on trunk** (logo, characters, obstacles, backgrounds, music, sound effects), each with editable source. Of the six bought media jobs, my last notes record three completed (logo, backgrounds, music), one still executing (characters), one blocked (obstacles) and one ordered but unconfirmed (sound effects). No child result file was handed to this write-up, so none is certified here. | section 8 |
| Audit | **Partial.** Verifier audited twice; engine, practice build, Royal mechanic, IMD token, swap route and eligibility reviewed. The ledger, the backend services and the system as a whole were never independently audited. | sections 5–7, 10–11 |
| Deploy | **Not done, deliberately.** Both bought deployments are unspent (section 12). | — |

Three blockers, each sufficient on its own:

1. **IMD cannot be burned.** The token has no `burn`/`burnFrom`, rejects transfers to the zero address, and its only internal burn path is a bridge send that re-mints on another chain. "25% permanent burn" has no implementation that reduces `totalSupply`. An immutable contract cannot be corrected after deployment, so this needs the requester's decision first.
2. **Eligibility is not validated.** The goal itself requires security and legal eligibility to be validated before paid play. No operator, markets, counsel opinion, privacy assessment or rights to the Pepe character have been supplied. Both eligibility reviews conclude *hold*.
3. **The system is incomplete.** Only two of the ten core-service targets (protocol, ledger) were recorded as landed when the goal was written up. The runtime and admission targets were on the trunk but still being checked; the chain indexer and settler was in progress; the independent replay verifier, projections, public API, integration tests and release handoff never started. There is no hosted backend, database, RPC, signer or payout automation.

---

## 2. The decision only the requester can make

**IMD on Ethereum has no burn function. What should happen to the 25% leg?**

Facts, pinned to chain 1 block 26,511,351 (hash `0x2036083ecd4b553db43d76dfbe48363f74a3e47d6fd4402da647b64ff3388689`) `[imd-mechanics-e2/burn-and-units]`:

- IMD `0xD34a99Bc0f67aE1bbd63C660e6d0b0dd03E263B7` is `Identity.md` / `IMD`, **18 decimals**, Sourcify exact match for `BridgedFP` (a LayerZero OFT on OpenZeppelin ERC20 v5.4.0), not a proxy, runtime code hash `0x79a1ae149d27d4aae006d4dd75cb834222c9623799bbf34359428aaf66fec3bf`. `totalSupply` at the block: 4,215,874.631149 IMD.
- Transfers are exact: no fee, no rebase, no pause, no blacklist.
- `burn(uint256)` and `burnFrom(address,uint256)` are absent from the bytecode and revert. `transfer(address(0), x)` reverts with `ERC20InvalidReceiver`.
- The only `_burn` path is the OFT `send`, which burns on Ethereum and mints the same amount on a peer chain (Arbitrum and Base peers were set), and needs a LayerZero fee. That is a move, not destruction.
- On a fork, a transfer to `0x…dEaD` completed for 1, 5 and 10 IMD and **left `totalSupply` unchanged**.
- The token owner is a single EOA that can rename the token and configure bridge peers; Ethereum supply is one chain's share of a multi-chain supply and is not fixed.
- The gate the batch was asked to report is `gates.token = fail`.

The ledger target reached the same conclusion independently at block 26,511,406 and wrote `RunArcade` to call `IMD.burn` and require an exact supply drop, so on mainnet every purchase reverts and nothing moves `[core-services-e2/ledger]`. No sink, lock, bridge, new token or changed split was substituted, because none was authorized and the goal forbids hidden changes.

Options, for the requester to choose:

| Option | What the player is told | Effect on the contract |
|---|---|---|
| (a) Irrecoverable sink | "25% is sent to an address nobody controls. Circulating supply falls; `totalSupply` does not." | Replace the burn call with a transfer to a fixed sink; the burn tracker reports sink balance growth, not supply reduction. |
| (b) Locked in the game contract | "25% stays in the contract forever; no function can move it." | Keep it out of every pot and payout path; same disclosure as (a). |
| (c) Change the allocation | New split stated by the requester. | Re-specify, re-test, re-audit. |
| (d) A token-side burn | Only possible if the IMD owner adds or exposes a real burn; outside this goal's control. | None until the token changes. |

Until one is chosen the three purchases, their approval prompts and their admissions stay unavailable.

**Also needed from the requester before any paid surface:** the operating entity and target markets; counsel's written view on the paid, participant-funded contest and on Royal's paid advantage; rights to the Pepe name and character and to the six assets; the operators of the two independent score signers; where the backend, database and RPC run. None of these can be invented by workers, and none was (section 11).

---

## 3. What exists: the trunk

- Repository: `https://github.com/identity-md-launches/goal-3502-build-audit-deploy-pepe.git`
- Commit the goal's waves reached: **`6083f1b5db4c14344351876ca9d2d057b768ad85`** (99 files; no submodules; no root README or LICENSE; no CI workflow).

| Commit | Wave | What it added |
|---|---|---|
| `c37a47850e3f6605a39c8b6259248c9424a4e47a` | foundation (10 items, all accepted) | `game/` engine, `web/` practice client, `backend/store`, `src/RunVerifier.sol` v1, six `media/` packs |
| `bddb39f58e88db884565d1c0c6ee9106f536a2f4` | core-services-e2 / protocol | `backend/protocol`, store migration 002, `RunVerifier` v2, `docs/protocol.md`, `docs/verification.md` |
| `6d74522030f0ad8eb71189153379a35b7afb5ba4` | core-services-e2 / ledger | `src/RunArcade.sol`, `src/arcade/IArcadeToken.sol`, `test/arcade/RunArcade.t.sol`, `docs/arcade.md` |
| `91d16563b91f479e1bbaaa66c7b9d19314cd9547` | core-services-e2 / runtime | `backend/runtime` |
| `6083f1b5db4c14344351876ca9d2d057b768ad85` | core-services-e2 / admission | `backend/admission` |

At the snapshot handed to this write-up the plane counted two targets landed (protocol, ledger) and three items accepted; `runtime` was still "working" after its re-check on another machine exited 1 (reason withheld by the plane), `admission` was "checking", `chain` was "working", and `replay`, `projections`, `api`, `integration` and `handoff` had never started. The runtime and admission files are on the trunk, but their acceptance was not final. No result for `runtime` was handed to me.

### Components

| Path | What it is | Reported checks |
|---|---|---|
| `game/engine.mjs`, `game/ENGINE.md` | Deterministic integer physics at a fixed 60 ticks per second, rules version `peperun-physics/1`; course generation from a uint32 seed; replay, state hash, input encoding. | 31/31 tests; a re-implementation written from the spec alone reproduced all 7 fixtures `[foundation/physics]` |
| `web/` | Static free-practice client: HUD (metres, m/s, time, personal best), keyboard and touch controls, local top-10 practice ranking, disabled paid panel. | 21 pass + 1 skipped before merge `[foundation/practice]`; 22/22 on the merged tree `[evidence-review-e2/foundation-audit]` |
| `backend/store` | Durable paid-session store on `node:sqlite` (WAL, synchronous FULL): single-use entry claims, ordered inputs, checkpoints, one bounded reconnect, reorg quarantine. | 15/15 `[foundation/session-store]`, 18/18 after migration 002 `[core-services-e2/protocol]` |
| `backend/protocol` | Hashing, EIP-712 v2, seed commit and derive, weekly schedule, JSON schemas, signer adapters, vectors. Vendored `@noble/hashes` 1.8.0 (MIT). | 11/11 `[core-services-e2/protocol]` |
| `backend/runtime` | Server-authoritative 60 Hz runtime for paid runs (section 6). | Its own `check.mjs`; no accepted result handed |
| `backend/admission` | Wallet-bound admission gate: EIP-4361 sign-in, EIP-712 v2 quotes, owner-provisioned policy with no fallback, external age/location/sanctions evidence. | 5/5 `[core-services-e2/admission]` |
| `src/RunVerifier.sol` | Stateless EIP-712 verifier (section 5). | 10/10 (v1), 12/12 (v2) |
| `src/RunArcade.sol` | Purchase, inventory and weekly jackpot ledger (section 5). | 26/26 with a stand-in burnable token `[core-services-e2/ledger]` |
| `media/*` | Six source packs (section 8). | per-pack checks |
| `docs/` | `protocol.md`, `verification.md`, `arcade.md`. | — |

### Re-run for this write-up at `6083f1b`

Fresh clone, Node 24, Foundry with solc 0.8.26, offline, no environment variables for forge:

| Command | Result |
|---|---|
| `node --test "game/test/**/*.test.mjs"` | 31 pass, 0 fail |
| `node --test web/tests/practice.test.mjs` | 22 pass, 0 fail |
| `node --test backend/store/test/store.test.mjs backend/store/test/migration.test.mjs` | 18 pass, 0 fail |
| `node --test backend/protocol/test/protocol.test.mjs` | 11 pass, 0 fail |
| `node --test backend/admission/test/admission.test.mjs` | 5 pass, 0 fail |
| `node backend/runtime/check.mjs` | 10/10 steps passed |
| `forge test --offline` | 38 pass, 0 fail: `RunVerifier` 12, `RunArcadeTest` 25, `RunArcadeForkTest` 1 (returns early offline, so it proves nothing about mainnet in this run) |
| `forge build --offline --sizes` | `RunArcade` 9,394 B runtime, `RunVerifier` 2,729 B runtime |
| `node media/characters/check.mjs` | 22/22 checks |
| `python3 media/backgrounds/check_atlas.py` | exit 0, 0 seam mismatches |
| `node media/sfx/check.js` | **exit 1**: `require is not defined in ES module scope` (audit finding F-4 is still present at this commit) |

`web/`, `media/` and `game/` are byte-for-byte unchanged since the foundation commit, so the practice-build findings F-1 to F-4 (section 9) still apply at the trunk's newest commit.

---

## 4. The goal, clause by clause

**Source** = code on trunk with passing tests. **None** = nothing built. Nothing in this table is live.

| Goal clause | State | Notes |
|---|---|---|
| Auto-run, jump, duck, distance in metres, speed, death score, personal best | Source | Engine and practice HUD. |
| Rapid difficulty increase | Source | Speed `min(18000, 7000 + floor(d/80))` mm/s: 7 m/s rising to an 18 m/s cap at 880 m. Seven difficulty levels, one per 150 m; minimum gap shrinks from 72 to 46 ticks. |
| Fair obstacles | Source, engine level | 1,500 seeds × 3 km: every gap at least the level minimum; every obstacle spawns off screen and is visible at least 30 ticks before contact; a reference player survives 2.4 km on 200 seeds; minimum clearing jump window 22–27 ticks `[foundation/physics]`. The *drawn* obstacles do not match the collision rectangles (F-2). |
| 60 FPS | **Unmeasured** | Simulation is fixed at 60 Hz. No real browser, phone or tablet frame timing was ever measured; the only figures are simulated timestamps. |
| Desktop and mobile controls | Source, untested on devices | Keyboard and multi-touch pads in unit tests only. |
| Evolving worlds | Art exists, wiring wrong | Three worlds (Lily Marsh 0 m, Neon Rooftops 400 m, Ruined Observatory 1,000 m); the renderer switches every 500 m and wraps (F-3). |
| Pixel art, smooth animation | Art exists, wiring wrong | 22 skins × 8 frames; the renderer draws Classic only and ignores the art anchor (F-1). |
| Prices 1 / 5 / 10 IMD; 50/25/25 on all purchases; atomic; immutable | Source; **unusable on mainnet** | `RunArcade` implements it with exact balance and supply checks and no owner. The burn leg cannot execute against real IMD. |
| Verify decimals and burn | **Done, result negative** | 18 decimals confirmed; burn impossible (section 2). |
| No NFTs, new token or hidden fees | Source | Inventory is a per-wallet bitmask; no token is created; the price is read from the ledger, not signed. |
| Weekly cycle, Sunday 20:00 UTC, auto-renewal, permissionless settlement, tie rule, deadlines, rollover | Source | Section 5. Countdown UI: none. Timing windows not validated against real finality (section 6). |
| Winner paid the entire jackpot directly | Source | `settle()` transfers the whole pot to the winning entry's wallet. |
| Classic free + 20 premium animated skins incl. Ninja, Cyber, Illuminati, Dragon | Art + contract source | Rows 1–4 are Ninja, Cyber, Illuminati, Dragon; rows 5–20 Pirate, Astronaut, Viking, Wizard, Punk, Zombie, Pharaoh, Knight, Robot, Skater, Magma, Frost, Phantom, Diamond, Tycoon, Samurai. No shop or inventory UI. |
| Permanent, non-transferable, on-chain wallet ownership | Source | `skinMask[wallet]`; no transfer function exists. |
| Identical physics and hitboxes, no advantages | Source, verified | `playerHitbox` is identical for ids 0–20; independently confirmed `[protocol-audit-e5/royal-advantage]`. |
| Royal: crown and cape, one extra life, distance preserved, no stacking, weekly expiry | Source + art | Section 7. |
| Disclose Royal advantage, expiry and leaderboard status | Written here (section 7) | Not on any live page. |
| Site: black / neon green / gold arcade design | Source, practice page only | |
| Free practice with separate rankings | Source | Browser-local top 10, never mixed with paid ranking. |
| Skin shop, inventory, live jackpot, leaderboard, Hall of Fame, achievements, profiles, shareable scores, burn tracker, FAQ | **None** | Not in `web/` at the trunk commit. |
| Verified IMD swap | Evidence only | A first-party route was verified at a pinned block (section 10); no link is built. |
| Wallets: MetaMask/Rabby EIP-6963, balances, network switching, exact approvals, confirmations | **None** | No wallet code in `web/`. The contract requires an exact approval of the price. |
| Server-authoritative physics | Source | `backend/runtime`; not hosted. |
| Fair seeds | Source | Commit before payment, derive from the finalized hash of `entryBlock+2`; no reroll (section 6). |
| Single-use sessions | Source | One session per entry in the store, runtime and ledger. |
| Replay validation, independent signed score verification | **Contract side only** | The on-chain two-signature check exists. The independent replay-verifier service never started; no score has ever been signed end to end. |
| Bot detection | Minimal | Objective anomaly counters kept as evidence; more than 8 impossible inputs end a run. No classifier, no review process. |
| Fair disconnect handling | Source | One 15 s grace window; earned distance kept (section 6). |
| No browser-trusted scores, backdoors, admin withdrawals, arbitrary winners | Source | Ledger has no owner, upgrade, withdrawal, winner choice or veto; tested by `testNoAdminSurface`. Not independently audited. |
| Persistent backend/database, RPC, secure hosting | **None hosted** | Libraries only. No HTTP or WebSocket API. |
| Automated payouts | **None** | `settle()` is permissionless; no caller runs. |
| Gas optimization | Measured, stand-in token only | Purchase median 152,172 / max 343,182; `submitScore` median 70,981 / max 105,175; `settle` max 91,516. Not mainnet costs. |
| Tests | Yes | Section 3. |
| Independent audits | **Partial** | Section 1. |
| Verified contracts | **None** | Nothing deployed. |
| Source code and documentation | Yes | Public repository; three protocol documents and per-module READMEs. No root README or licence file. |
| Validate security/legal eligibility before paid play | **Validated as not met** | Section 11. |
| No fake data, mockups or manipulative spending | Held | The practice page shows no jackpot figure, asks for no wallet and labels paid play unavailable. No invented address, key, policy or figure was written anywhere. |

---

## 5. The two contracts

### RunVerifier (`src/RunVerifier.sol`, 124 lines)

Stateless `view` contract. EIP-712 domain `RunVerifier` / version `2`, `chainId = block.chainid`, `verifyingContract = msg.sender` (the calling ledger). It checks one admission signature, or two score signatures over the same digest from two distinct non-zero addresses.

- `Admission`: wallet, action, sku, epoch, nonce, expiry, rulesHash, termsHash, policyHash, seedCommitment.
- `Score`: wallet, sessionId, epoch, distanceMeters, royal, seedCommitment, rulesHash, replayHash, expiry.
- Rejects high-s, wrong `v`, wrong length, zero `r`/`s`, `r ≥ n`. Also exposes `seedCommitment()` and `deriveSeed()`.

Independent review of v1 at `c37a478` `[foundation-review-e4/score-signatures]`: 10/10 tests with 1,024 fuzz runs; no material defect in the stateless checks; role authorization, session matching, weekly deadlines and single use are the ledger's job and were unevidenced there.

Independent review of v2 at `bddb39f` `[protocol-audit-e5/verifier]`: 12 repository tests plus 13 adversarial tests written by the reviewer, 25/25; all five published digest vectors reproduced with `cast`; all 11 selectors match the documentation. **No critical or high finding in the verifier.** Findings:

| Id | Severity | Finding | Where it stands at `6083f1b` (my reading of the source, not an audit) |
|---|---|---|---|
| M-1 | Medium | A Score does not carry termsHash or policyHash; its link to the paid entry exists only through ledger state. | `submitScore` loads the entry by `uint256(sessionId)` and requires wallet, epoch, royal, seedCommitment and rulesHash to match, unscored. termsHash and policyHash are emitted in `AdmissionConsumed` but not stored per entry. |
| M-2 | Medium | Roles are caller-supplied; the verifier grants no authority by itself. | The ledger passes its own immutables `ADMISSION_AUTHORITY` and `REPLAY_VERIFIER`. |
| L-1 | Low | Signatures replayable until expiry at the verifier. | Ledger consumes the nonce per wallet and scores each entry once. |
| L-2 | Low | No week window in the verifier. | Ledger enforces current epoch, the 19:30 cutoff and `timestamp < epochEnd`. |
| L-3 | Low | The engine seed is 32 bits (collisions expected after about 77,000 entries); the proposer of `entryBlock+2` can withhold a block. | **Open.** Unchanged. |
| L-4 | Low | EOA signers only; no rotation. | **Open by design.** Roles are immutable, so a compromised signer key cannot be rotated or paused without redeploying, and there is no pause. |
| L-5 | Info | One key signs admissions and is also the first score signer. | Unchanged; a score still needs the second, distinct key. |

That review ran before the ledger existed, so its 14-point ledger checklist (C1–C14) was "unknown" in the report. Reading `RunArcade` at `6083f1b`, I find C1–C7, C9 and C11–C14 addressed in source and tests; **C8 partly** (terms and policy hashes are not stored per entry) and **C10 not** (`distanceMeters` has no upper bound or sanity check; the ledger trusts the two signers). This mapping is my own reading and needs an independent audit.

### RunArcade (`src/RunArcade.sol`, 316 lines)

`constructor(RunVerifier verifier, address admissionAuthority, address replayVerifier)`: roles must be non-zero, distinct and not the developer address; `UNIT = 10 ** IMD.decimals()`. Constants: IMD `0xD34a99Bc0f67aE1bbd63C660e6d0b0dd03E263B7`, developer `0x83027AD9d0D5374335086c539dADD1db983441B0`.

- `purchase(admission, signature)`: caller must be the admitted wallet; epoch must be current; single-use nonce; action 1 game entry (sku 0 or an owned skin; Royal state snapshotted), action 2 permanent skin (sku 1–20, once per wallet), action 3 Royal (sku 21, once per week). Pulls exactly the price, keeps half in the week's pot, calls `IMD.burn(price/4)` and requires `totalSupply` and its own balance to fall by exactly that, then transfers the remainder to the developer with an exact balance check. Any fee, rebase, no-op burn, false return or revert undoes the whole purchase.
- `submitScore(score, authoritySig, replaySig)`: anyone may relay; checks described under M-1; strictly before the week ends; highest metres wins, a tie goes to the lower entry id.
- `settle()`: permissionless; settles the oldest unsettled closed week in O(1); pays the entire pot to the winner's wallet or, with no verified score, rolls the entire pot into the next week; missed weeks are caught up one call each.
- `absorbDonations()`: IMD sent directly to the contract is credited to the current pot.
- No owner, upgrade, withdrawal, winner selection or payout veto.

Tests (26, with a burnable stand-in token placed at the IMD address): exact split at all three prices, fee/no-op/rebase/missing-burn/false-return reverts, reentrancy, signature mutation and replay through the real `RunVerifier`, cutoff and strict close, duplicate and out-of-range skins, Royal weekly/no-stack/snapshot, ties in both submission orders, multi-week rollover without loss, donations, fuzzed conservation, no admin selectors `[core-services-e2/ledger]`.

Things a reader should know that the tests accept as intended, noted from my reading:

- A verified score of 0 m wins an otherwise empty week (`testZeroMeterScoreStillWins`).
- An entry that is paid but never scored simply does not rank; there is no refund path.
- Skins stay purchasable until 20:00, so a skin bought after 19:30 still funds the closing week's pot.
- Settlement is strictly sequential. A payout transfer that could never succeed would block that week and every later one, and there is no override. With IMD as verified today (not a proxy, no blacklist, no pause) a transfer to a winner's wallet cannot be refused; an auditor should confirm that and rule on the missing escape path.
- **Not independently audited. Not deployed.**

### Units

| Purchase | Price (base units) | Jackpot 50% | Burn 25% | Developer 25% |
|---|---|---|---|---|
| Game, 1 IMD | 1000000000000000000 | 500000000000000000 | 250000000000000000 | 250000000000000000 |
| Permanent skin, 5 IMD | 5000000000000000000 | 2500000000000000000 | 1250000000000000000 | 1250000000000000000 |
| Royal, 10 IMD | 10000000000000000000 | 5000000000000000000 | 2500000000000000000 | 2500000000000000000 |

Each row sums to its price with no remainder `[imd-mechanics-e2/burn-and-units]`.

---

## 6. Fair play: seeds, sessions, deadlines, disconnects

**Weekly schedule (UTC), as implemented.** Week *n* is `[331200 + n·604800, 331200 + (n+1)·604800)`: Sunday 20:00 to the next Sunday 20:00. New weeks open by time alone.

| Moment | Rule | Enforced by |
|---|---|---|
| Sunday 19:30 | Game entries and Royal purchases close for the week | `RunArcade` (on chain) |
| Sunday 19:55 | Live runs are stopped and keep the distance earned | `backend/runtime` |
| Before Sunday 20:00 | The score transaction must be in a block with `timestamp < 20:00`, carrying both signatures | `RunArcade` (strict) |
| Sunday 20:00 | Week closes; Royal expires; anyone may call `settle()` | `RunArcade` |
| Ranking | Highest whole metres; equal distances go to the lower entry id | `RunArcade` |
| No verified score | The entire pot rolls into the next week, once per missed week | `RunArcade` |

**These windows are not validated.** The seed needs block `entryBlock+2` to be *finalized*, which on Ethereum normally takes roughly 13 to 19 minutes after inclusion (general protocol behaviour, not measured in this goal). An entry bought just before 19:30 may therefore get only a few minutes of play, or none, before the 19:55 stop. The admission service refuses a quote whose finality and play windows do not fit, but a direct contract call is bound only by 19:30. The item meant to measure this (`protocol-audit-e5/schedule`) was still running at write-up; its result is not in this report.

**Seeds.** The server draws a 32-byte secret, commits to it inside the signed admission before payment, and derives the seed after `entryBlock+2` is final from the secret, the entry id and that block hash. One seed per entry; a reorg invalidates the run and never re-seeds it. The browser gets redacted render state only `[core-services-e2/protocol]`. Residual risks: L-3 above.

**Sessions and inputs** (`backend/runtime`, from its documentation and my run of its check): wall-clock-driven ticks the client cannot pause or slow; inputs accepted only in a window of 12 ticks late to 6 early; contiguous sequence numbers; exact duplicates return the original acknowledgement; inputs are persisted before the tick that uses them; at most 16 events per message and 20 per second; 2-hour maximum run.

**Disconnects.** Three seconds without a client message counts as a disconnect. One bounded grace window (15 s by default) pauses the run and restores the same tick, state and input prefix on reconnect. A second disconnect, or missing the deadline, ends the run with the last acknowledged distance. After a server crash, recovery restores the last checkpoint and every persisted input, including the Royal life. **Open policy point:** the store's eligibility predicate admits only `finished` runs, so whether a run ended by disconnect may rank has not been decided.

**Capacity** (single process, SQLite with full sync, measured by the check on a build machine): about 50 concurrent paid runs recommended. This is server throughput, unrelated to browser frame rate.

**Not built:** the independent replay-verifier service, the signing flow that would turn a validated replay into the two signatures, the finalized-chain indexer and settler, the network transport, seed-custody encryption, multi-provider RPC.

---

## 7. Royal

**Disclosure text for players (the product rule as built):**

> Royal costs 10 IMD and lasts until the current week ends on Sunday 20:00 UTC. It must be bought again each week, cannot be bought after Sunday 19:30 UTC, and cannot be stacked. It applies to paid games you enter after buying it. In each such game it saves you once: the first collision that would end your run is ignored, the obstacle is removed and your distance is kept; the next collision ends the run. **This is a paid competitive advantage.** Royal runs are ranked in the same weekly paid leaderboard as every other run, compete for the same jackpot, and are labelled Royal. Royal changes nothing else: speed, obstacles and hitbox are the same as Classic. Royal has no effect in free practice.

The contract implements weekly expiry (`royalEpochPlusOne`), no stacking, and a snapshot at entry that the score must match. The Royal label on a leaderboard does not exist yet because no leaderboard does.

**Measured effect.** Two reviews agree on direction and disagree on size:

- `[foundation-review-e4/royal-distance]`, 32 seeds, paired runs. Idle input: Royal farther in 32/32, median +13 m. A course-aware player with deterministic missed inputs: Royal farther in all 21 pairs where both runs died, median +643 m; 11 further pairs hit the 10,800-tick cap (2,759 m) with a runner still alive, so their final gaps are unknown. At all 61 first contacts Classic died and Royal continued on the same tick with identical distance.
- `[protocol-audit-e5/royal-advantage]` (flagged by the plane's source check), 2,000 seeds for each of three scripted skill profiles. Royal finished farther in 2,000/2,000 for each; mean gain +26.9 m (+62.1%), +25.4 m (+60.6%), +23.3 m (+58.2%); the best of 100 Royal runs beat the best of 100 non-Royal runs in 20/20 cohorts for each profile. **Caveat I add:** its "expert" profile has a median of 30.057 m without Royal, which is exactly the distance at which an idle runner dies on the first obstacle. Its controllers therefore fail early in at least half of all seeds, and its absolute distances are not representative of competent play, whose reference player survives 2.4 km `[foundation/physics]`.

Conclusion: in every paired run where both runners died, Royal went farther. The size of the advantage for real players is unknown; no human play data exists. The eligibility review ranks the same-ranking paid advantage as a high-severity classification question for counsel (section 11).

---

## 8. Media: six assets

**Source packs on the trunk** (made by the foundation wave; original procedural work with editable sources):

| Asset | Path | What it is | Check reported |
|---|---|---|---|
| Logo | `media/logo/logo.png` + SVG master | 512×512 RGB icon, 32 px circular preview | all 262,144 px opaque `[foundation/logo]` |
| Characters | `media/characters/characters.png`, `.json`, `source/` | 512×1408 atlas, 22 rows × 8 frames of 64×64; Classic, 20 premium, Royal with crown and cape; PNG sha256 `2e449de9…f4cf5` | 22/22 checks, 176 frames, identical body silhouette across skins `[foundation/characters]` |
| Obstacles | `media/obstacles/obstacles.png`, `.json`, `build_obstacles.py` | 256×128 atlas: one ground hazard and one overhead gate, 4 frames each | ad hoc checks only `[foundation/obstacles]` |
| Backgrounds | `media/backgrounds/backgrounds.png`, `.json`, `atlas_source.py` | 960×384 atlas, three worlds × three parallax layers; sha256 `d24147ee…a23a69` | seam check 0 mismatches `[foundation/backgrounds]` |
| Music | `media/music/run.ogg`, `run-score.mjs` | 150 BPM A-minor chiptune loop, 38.400 s, stereo Ogg Vorbis, peak −6.15 dBFS; sha256 `bfbfd1d9…7b4fc` | decoded with tools installed only in scratch `[foundation/music]` |
| Sound effects | `media/sfx/cues.wav`, `cues.json`, `synthesize.js` | 44.1 kHz mono PCM16 sprite, 2,880 ms, seven cues (menu, jump, duck, landing, milestone, revive, death), 80 ms silent guards | validator passes only when run as CommonJS `[foundation/sound-effects]`, F-4 |

Known defects `[evidence-review-e2/foundation-audit]`: only two obstacle drawings exist for four engine obstacle shapes; the character art declares per-animation boxes that differ from the engine's 32×44 standing and 32×24 ducking boxes (the engine's boxes are the rule and must not be changed to fit art); the music cannot be rebuilt or decoded offline because its encoder and decoder are not in the repository; the sound-effect scripts do not run as documented. Nobody has listened to the audio. Provenance notes are not rights clearance (F-5).

**Bought media jobs.** The goal bought seven off-chain deliverables. The snapshot handed to this write-up has no children section and no child result file, so the following is from my episode 6 notes and is unverified here:

| Job | Last recorded state | Route on the plane |
|---|---|---|
| Logo | completed | `/jobs/b46d4b32-f528-477c-865b-9df7fd7a1b48/result` |
| Backgrounds | completed | `/jobs/8d432742-6d5b-4b4b-a977-e3b66fe324a3/result` |
| Music | completed | `/jobs/04ee3159-9e64-4d01-bf0c-0cb280e0d7a1/result` |
| Characters | executing | `/jobs/16ded40b-e21e-4b37-aeba-3049166e43dd/result` |
| Obstacles | **blocked**, reason not supplied | `/jobs/3eff63b4-ac65-42a0-af2c-1e96d2124a99/result` |
| Sound effects | ordered in episode 5; opening never confirmed | — |

I could not read those routes from my seat, so no asset URL, hash or quality is confirmed for any child. "Completed" is a job state, not a checked asset.

---

## 9. Website

**Not published.** `https://peperun.imd.site/` returned HTTP 404 with the body "Nothing is published as peperun.imd.site" on 2026-11-28 at about 05:00 UTC. In episode 5 I ordered a website job for a free-practice build (engine and media from the trunk, findings F-1 to F-4 corrected, wallet discovery and balance reading only, every paid surface shown as not live with its reason, no transaction or approval request). Its opening was never confirmed to me and nothing is live.

What the trunk's `web/` is: one static page with the headline, the slogan, the canvas, a four-cell HUD, touch pads, a browser-local top-10 practice ranking and a disabled panel stating that paid runs, skins and Royal are not available and that nothing asks for a wallet or payment.

Independent verdict on it at the foundation commit, unchanged since: **fail as a release candidate; pass for the engine and asset validators** `[evidence-review-e2/foundation-audit]`.

| Id | Finding | Repair |
|---|---|---|
| F-1 | Renderer ignores the character anchor (32,60), placing the sprite 12 px left and 4 px up; always draws Classic. | Load `characters.json`, select the row by entitlement, place from the anchor; keep engine boxes. |
| F-2 | Obstacle cells are stretched over the collision rectangle; atlas bounds and animation unused; the overhead gate's drawn bar does not match what collides. | Map each engine obstacle kind to art that fills its rectangle, or show an explicit collision cue. |
| F-3 | Worlds change every 500 m and wrap; metadata says 0 / 400 / 1,000 m and keep the last. | Read the map; pick the last world whose start is ≤ distance. |
| F-4 | Audio scripts fail under ESM; music dependencies missing; `start`, `best`, `pause`, `resume` cues unmapped while `menu`, `landing`, `revive` are unused; no Ogg fallback. | Rename or convert scripts, commit dependencies, reconcile cue names. |
| F-5 | Provenance is not clearance. | Owner-approved asset manifest and a legal decision on the name and mascot. |

Never measured: real 60 FPS, touch behaviour on a device, audio playback.

Not built at all: wallet connection (EIP-6963, balances, network switch, exact approvals, confirmations), skin shop, inventory, live jackpot and countdown, paid leaderboard, Hall of Fame, achievements, profiles, shareable scores, burn tracker, swap link, FAQ.

---

## 10. IMD swap route

Two results; the second supersedes the first.

- `[release-evidence/swap-route]` at block 26,511,194 found no V2 pair and zero liquidity in the V3 1% WETH pool, and did not check V4. Its "not verified" conclusion was correct for what it checked and must not be read as "IMD has no liquidity".
- `[evidence-review-e2/swap]` at block 26,511,366 (hash `0x6a6bc8eb606c148074c9ad2cedb05f349982fd82d11b787cbfb98bedf70b94bf`, 2026-11-28 04:35:23 UTC): **pass for an external link** to the first-party page `https://pool4.imd.fun/swap`, subject to a fresh quote at click time. IdentityMD's token documentation says the market moved to Uniswap v4, and its project index lists that origin. The pool is Uniswap V4 id `0x415829f72e9f54531c26eae76f107618540e898a45d6ae35959e143f5faca704` (native ETH / IMD, 1% fee, tick spacing 60, hook `0xc6c965bd164c483e87d0b550671798e9a3602840`) with active liquidity. Exact-output quotes from the official V4 Quoter at that block:

| IMD wanted | ETH needed (wei) | ETH |
|---|---|---|
| 1 | 1006507376225399 | 0.001006507376225399 |
| 5 | 5035653817289618 | 0.005035653817289618 |
| 10 | 10079110842437904 | 0.010079110842437904 |

  A read-only Universal Router simulation of a 0.0011 ETH buy returned without revert. No transaction was sent.

Limits: these are one block's figures and must never be shown as live prices. The page quotes ETH in, so a buyer must check the IMD out. The hook owner can close the market. Other pools exist (a deeper hookless ETH/IMD V4 pool, V3 stablecoin pools at very different rates), so the project's "one pool" statement is not a chain fact. The page's wallet behaviour and the sell path were not tested. A site should show the link only after a current executable quote succeeds, and otherwise say the swap is temporarily unavailable.

---

## 11. Eligibility and rights

**Not legal advice, and no clearance exists.** Two reviews:

- `[release-evidence/paid-eligibility]` (flagged by the plane's source check): a launch-gate matrix. It is internally inconsistent: it says practice can launch now but also holds the whole public launch on branding, and it proposes discretionary payout holds that contradict the immutable direct payout the goal specifies. I treated it as an inventory of open issues, not as an instruction, and added no payout veto.
- `[evidence-review-e2/eligibility]` (flagged; its checkout was empty, so it reviewed the brief's facts against public primary sources): **hold all three purchases, public Pepe branding and public practice** until evidence exists.

What it establishes:

- A fair seed and a skill element do not by themselves take a paid, participant-funded prize contest outside gambling or lottery rules; the tests differ by jurisdiction (it cites Great Britain's Gambling Act ss. 6 and 14, UIGEA, New York Penal Law § 225.00 as examples, not as a market perimeter).
- Royal is a purchasable advantage in the same paid ranking; counsel must classify it.
- Cosmetic skins also fund the pot (2.5 of every 5 IMD), so calling them cosmetic does not remove them from the analysis.
- Pepe is identified by the original publisher as a Matt Furie character with a documented enforcement history. No licence or clearance was supplied. Pixel-art redrawing does not supply rights. The foundation character pack calls its frog an original drawing and flags the name for review; that is an assertion, not clearance.
- Free practice with wallet addresses, IPs and replays still needs a privacy and children's assessment.
- **A conflict the requester should know about:** an immutable, permissionless, full direct payout cannot be stopped if a valid winner later becomes legally blocked (sanctions, court order, withholding duty). Screening before entry reduces but does not remove this. If the applicable law requires an intervention the contract cannot perform, the affected scope must stay closed or the specification must change.

The admission service is built to match: it has no default policy, and it issues nothing until an owner-provisioned policy, approved terms and privacy hashes, rights and security approvals, a Royal disclosure and an external age/location/sanctions evidence provider are all present `[core-services-e2/admission]`.

---

## 12. What ran, what it cost, what is unspent

Items: 32 of 50 used. Six episodes (five ordinary, one for the unspent budget).

| Batch | Kind | Outcome |
|---|---|---|
| `foundation` | code wave, 10 items | 10 accepted, merged at `c37a478` |
| `release-evidence` | research, 2 | 2 accepted; `paid-eligibility` source-flagged |
| `core-services-e2` | code targets, 10 | protocol and ledger landed; runtime and admission on trunk, not finally accepted; chain working; replay, projections, api, integration, handoff never started. Not settled. |
| `imd-mechanics-e2` | research with chain pin, 1 | accepted; `gates.token = fail` |
| `evidence-review-e2` | research, 3 | 3 accepted; `eligibility` source-flagged |
| `foundation-review-e4` | research, 2 | 2 accepted |
| `protocol-audit-e5` | research, 4 | `verifier` and `royal-advantage` accepted (the latter source-flagged); `schedule` and `swap-route` still running, **not in this report** |

Two decisions of mine were refused by the plane and cost time: a first `imd-mechanics` batch (chain context needed an account) and `independent-audit-e3` (a second code wave cannot queue behind a running one). The second is why the ledger and services never got their independent audit.

Bought children: 2 on-chain deployments, 7 off-chain deliverables.

- **On-chain: 0 of 2 used, deliberately.** Deploying would have published either an immutable ledger whose every purchase reverts, or one with a burn substitute nobody authorized. The other reasons are in section 1. A launch written from words alone would not have matched the trunk's protocol.
- **Off-chain: 5 opened for media; sound effects and the website ordered in episode 5 with no confirmation handed to me.** If either did not open, that unit is also unspent and that deliverable unordered.

---

## 13. What is missing, in the order to do it

1. **Requester decides the 25% leg** (section 2) and supplies operator, markets, counsel's position, rights, signer operators and hosting.
2. Change `RunArcade` to the chosen mechanism; decide the open rules: a bound on `distanceMeters`, storing terms and policy hashes per entry, whether disconnect-ended runs rank, the seed width, signer-compromise procedure for an ownerless contract.
3. Finish the service targets: independent replay verifier and signing flow, chain indexer with reorg recovery, settler, projections, API and transport, integration tests.
4. **Independent audit of the ledger and of the integrated system**, with fixes and retest. Measure the Sunday windows against real finality.
5. Repair the client (F-1 to F-4), then build wallets (EIP-6963, exact approvals), shop, inventory, jackpot and countdown, leaderboard with Royal labels, Hall of Fame, achievements, profiles, share cards, burn tracker (reporting what the chosen mechanism really does), swap link gated on a live quote, FAQ. Measure frame rate and touch on real devices; listen to the audio.
6. Collect each media job's result with URL, hash and licence; resolve the blocked obstacles job; reconcile the art with the engine's rectangles.
7. Only then: deploy both contracts together from the trunk, verify source and bytecode, provision real roles, publish the site against the live addresses, run a settlement caller, and confirm each on chain and on the live site before calling anything delivered.

---

## 14. Limits of this report

- No child job result, and no result for the `runtime`, `chain`, `schedule` or second `swap-route` items, was available to me.
- Test counts from workers are their reports; the ones I re-ran are in section 3 and are not an audit.
- The fork test that checks RunArcade against real IMD ran on the ledger worker's machine with a public RPC; in my offline run it returns early.
- Chain facts are pinned to blocks 26,511,194, 26,511,351, 26,511,366 and 26,511,406 on 2026-11-28 and can change, especially liquidity and the token owner's bridge configuration.
- The site check is one request at one moment.

---

## 15. Results this report rests on

| Result | SHA-256 |
|---|---|
| `foundation/physics` | `298636324c5ea717da6750b5139caf8c21c02986283253f8e43b535dce3b3041` |
| `foundation/practice` | `972c1e42dfd76865e605b0344fae6ee29f1e6e413d3b1077d7f21a16db2a2a9f` |
| `foundation/score-verifier` | `ae6c5de69deaaed42605bcdd6afd30ea5fe3aa5699aaa3b386445d2d2d25a48a` |
| `foundation/session-store` | `174103d212a2e091176356ccfece2bc632508fa583b52520106d89888e1ac1ff` |
| `foundation/logo` | `6a4f8aaa596f4b892054dc9107e71d93e1312c46ac8773af308b8e0d8a5defd7` |
| `foundation/characters` | `352f3afbeaa43350dac7901b006b938d537794511156647001532a8ea4f4c038` |
| `foundation/obstacles` | `4a88f0fa67d8c3ff8607c68e532f8525ca4b555d3c4fb5c9298737f5e6cf03ca` |
| `foundation/backgrounds` | `e2f6a11da1bbdecadf46f00534ea07d653ceb35c95b954bb8a86eaac21e3a84d` |
| `foundation/music` | `758bc227db634ec01320d7e066491c987323ea24f8fbede2dfde4717ee35d0db` |
| `foundation/sound-effects` | `867ce5d79902c284c730d6c4376313e07a55ecddf31126b17de220a76716237d` |
| `release-evidence/swap-route` | `13f6beae749039421360105e374a7de9f868ff80f3d8ccaaa5be51f76ade4a0c` |
| `release-evidence/paid-eligibility` | `97727fbe1ba02a68e0681945f7c8aecb4864b4a5d9c354c069dc21bc1f6b1a2f` |
| `core-services-e2/protocol` | `16467f1987d3ebed9b4df3ec77896b1d1959d2b3e0c6f2b084b6d88e9ab1cff0` |
| `core-services-e2/ledger` | `1107c93a5ebeba5054a3fff2d3d18e904b6ece3a2e730615757b9e450f98aada` |
| `core-services-e2/admission` | `1d2191faabce1a16c38609412e1bc3841ac47865be01248e287338e6bab91f19` |
| `imd-mechanics-e2/burn-and-units` | `e60e4064122810135acf3828b055049b3a03a76380f3efead7d787ff80ec09b8` |
| `evidence-review-e2/eligibility` | `12679460382c928efacd0738ee839ab4ababe132332eb4cb5e7f92828c9ce5fe` |
| `evidence-review-e2/swap` | `401f0083113c88cc97e48640f534adf7c6663c1b9aeb821ff4de07fcb9d73481` |
| `evidence-review-e2/foundation-audit` | `46332c0b3bb0a32c2f0d59e9c3a246c27213ebfd46cf78609ec9e74eeb660313` |
| `foundation-review-e4/score-signatures` | `1bf910bdfb56063d5fc838c1bb5d4ab0b7f3ae1732f725e3dd8d75fad8117333` |
| `foundation-review-e4/royal-distance` | `4a13355f7c88e9e6b5d87a1aceace5d4948f25910fb422d91937ed6460c640a5` |
| `protocol-audit-e5/verifier` | `4a32cddd6f01ceae2e01974312240e05a7a9a3ce0b9ffaf90fb7959e37f91392` |
| `protocol-audit-e5/royal-advantage` | `48cc32da830814d43a4ab33e0b37f6e6bac328e305f574f9ca74854e882c65bc` |

Trunk: `https://github.com/identity-md-launches/goal-3502-build-audit-deploy-pepe.git` at `6083f1b5db4c14344351876ca9d2d057b768ad85`.
