# Ethereum rollups above 500 M USD TVS: trust-minimisation snapshot, 2026-10-27

Snapshot taken 2026-10-27, 14:20 to 14:40 UTC, from L2BEAT's summary API and page, each project's L2BEAT page, the project's own docs and code, and GitHub release pages. Every fact carries a bracketed source tag resolving to a URL in the reference list at the end; L2BEAT tags (S-, L-, G-) come first in every cell, project docs, code and releases (D-, R-) second. Where sources disagree, both figures are kept; where nothing was found, the cell says NOT FOUND. Only the ranking in section 3 is the author's analysis.

Six-month window used throughout: 2026-04-27 to 2026-10-27. TVS figures move daily; the ones here are the single API observation of 2026-10-27 14:20 UTC [S-api].

## 1. Selection: which rollups qualify

Rule applied: L2BEAT category "Optimistic Rollup" or "ZK Rollup" (the summary page's Rollups tab) and `tvs.breakdown.total` strictly above 500,000,000 USD in the API [S-api] [S-sum].

| # | Rollup | Category (L2BEAT) | Stage badge | TVS, USD (API) | Page display |
|---|---|---|---|---|---|
| 1 | Base Chain | Optimistic Rollup | Stage 1 | 15,058,117,632 | $15.05 B |
| 2 | Arbitrum One | Optimistic Rollup | Stage 1 | 9,832,005,632 | $9.83 B |
| 3 | OP Mainnet | Optimistic Rollup | Stage 1 | 1,717,252,352 | $1.71 B |
| 4 | Mantle | ZK Rollup | Stage 0 | 1,301,224,448 | $1.30 B |
| 5 | Lighter | ZK Rollup | Stage 0 (Appchain) | 1,057,181,312 | $1.05 B |

Source for every row: [S-api] [S-sum].

**Above 500 M but not rollups per L2BEAT**, so excluded from the ranking:

- Hyperliquid, "Other", 6,569,551,872 USD, L3 on Arbitrum One: "The proof system isn't fully functional", "There is no data availability bridge" [S-api] [S-hl] [S-others].
- Polygon PoS, "Other", 3,831,951,104 USD: "The proof system isn't fully functional" [S-api] [S-pos] [S-others].
- Robinhood Chain, "Other", 2,294,226,432 USD: "Closed proofs", "less than 5 external actors that can submit challenges" [S-api] [S-rh] [S-others]. Profiled in section 7 because it has a stage checklist and rollup-like risks, but never ranked.

Below the cutoff and not profiled: World Chain 401,126,016 (Other), Starknet 371,292,320, Ink 365,203,936, Linea 335,396,256 [S-api].

L2BEAT: "the Stages Framework only discusses the maturity of a rollup in terms of decentralization, and not in terms of security" [S-stages]. On 2026-04-30 the Stage 1 minimum challenge period dropped from 7 d to 5 d; no chain in this set was promoted by it (section 6) [S-forum].

## 2. Ranked table: the six points per rollup

Ranked most to least trust-minimised (method in section 3). Points 1 to 3 in table A, 4 to 6 in table B. "SC" = Security Council.

### Table A: stage, proof system, exit window and upgraders

| Rank | Rollup | (1) L2BEAT stage and L2BEAT's reasons | (2) Proof system; permissionless? | (3) Exit window; who upgrades; council and threshold |
|---|---|---|---|---|
| 1 | **Arbitrum One** | **Stage 1.** Passes walkaway test. Stage 2 met: fraud proof submission open to everyone. Stage 2 unmet: "Upgrades unrelated to onchain provable bugs provide less than 30d to exit"; "The Security Council's actions are not confined to onchain provable bugs" [L-arb-stage]. | **Optimistic, "Fraud proofs (INT)"**, interactive BoLD, live and **permissionless** (`validatorWhitelistDisabled: true`); 3,600 ETH bond; 6 d 8 h challenge + 2 d execution delay; permissionless since 2025-02-15 [L-arb-risk] [L-arb-sv] [L-arb-perm]. Docs: anyone can propose and challenge subject to bond; BoLD executed 2025-02-12 [D-arb-bold] [D-arb-chain] [D-arb-upg]. | **Exit window: "10d (regular upgrade path)", "None (emergency upgrade path)"** [L-arb-risk]. Upgraders: ArbitrumDAO plus **Arbitrum Security Council 9/12**; regular route L2Timelock 8 d + Outbox 6 d 8 h + L1Timelock 3 d = 17 d 8 h; emergency council path instant [L-arb-gov] [L-arb-perm]. Docs: Constitution confirms 9-of-12 and the no-delay emergency path [D-arb-const]. |
| 2 | **OP Mainnet** | **Stage 1.** Passes walkaway test. Stage 2 met: "Fraud proof submission is open to everyone." Unmet: same two items as Arbitrum [L-op-stage]. | **Optimistic, "Fraud proofs (INT)"**, live and **permissionless**: "proposed and challenged by anyone who has sufficient funds"; 0.08 ETH bond; 3 d 12 h challenge + 3 d 12 h execution delay; game type 9 SUPER_CANNON_KONA since 2026-09-24, "Proposing and challenging remain permissionless"; a permissioned fallback game type exists [L-op-risk] [L-op-sv] [L-op-upd]. Docs: permissionless since 2024-06-10; Karst promoted CANNON_KONA 2026-07-08; the Guardian can switch to a permissioned game [D-op-fp] [D-op-karst] [D-op-sec]. | **Exit window: "None"**: upgrades "initiated by the Security Council with instant upgrade power and without proper notice" [L-op-risk]. Upgrader: SuperchainProxyAdminOwner **2/2** = OpFoundationUpgradeSafe **5/7** + **Optimism Security Council 10/13**, "Can upgrade with no delay"; LivenessModule hands control to the Foundation Safe if members fall below 8 [L-op-gov] [L-op-perm]. Docs: same thresholds, upgrades "without upgrade delays" [D-op-roles] [D-op-sec]. |
| 3 | **Base Chain** | **Stage 1.** Passes walkaway test. Stage 2 met: "Fraud proof submission is open to everyone." Unmet: same two items [L-base-stage]. | **Optimistic, "Fraud proofs (1R, ZK)"**: Azul multi-proof (TEE + SP1 ZK), 0.05 ETH bond; **challenge permissionless**, **TEE proposer path allowlisted** in `TEEProverRegistry` by the Coordinator Multisig; "Self propose"; 5 d single / 1 d dual finality [L-base-risk] [L-base-sv] [L-base-perm]. Docs: "The TEE path is permissioned… The ZK path is permissionless"; Azul mainnet 2026-05-28; Beryl 2026-06-25 [D-base-azul] [D-base-pc] [D-base-beryl]. | **Exit window: "None"**, "contracts are instantly upgradable" [L-base-risk]. Upgrader: Base Governance Multisig **2/2** = Base Coordinator Multisig **3/6** (Coinbase) + **Base Security Council 8/11**, counted as 9 of 12 entities, no timelock [L-base-gov] [L-base-perm]. Base Multisig 1 (3/12) can pause withdrawals up to 3 months 1 day [L-base-perm]. Docs: same thresholds; no timelock found [D-base-sc]. |
| 4 | **Lighter** | **Stage 0 (Appchain).** 5 Stage 0 items met. Stage 1 "4 issues need fixing": the ≥75 % SC principle; "Users' withdrawals can be censored by the permissioned operators"; upgrades by actors more centralised than a SC give <7 d to exit; "The Security Council is not properly set up." Met: trusted setup, prover source published, verifier reproducible. Stage 2: 2 issues [L-lit-stage]. | **Validity, "Validity proofs (SN)"**, no execution delay, live; custom Plonky2 circuits wrapped in PLONK (Ignition setup) [L-lit-risk] [L-lit-op]. **Permissioned**: "Only the centralized operators can submit batches and verify them"; validators EOA 1, 4, 5 set by Lighter Multisig 2 (3/5) [L-lit-op] [L-lit-perm]. Code: `commitBatch`/`verifyBatch` require `isActiveValidator`; governor-only `setValidator` [D-lit-code]. | **Exit window: "None"** [L-lit-risk]. Regular upgrades by Lighter Multisig 2 **3/5** with 21 d UpgradeGatekeeper delay; **Lighter Multisig 4/7** (the "security council") can cut the delay to zero and "every upgrade so far has been fast-tracked"; L2BEAT: this council "does not currently satisfy the Stage 1 requirements" [L-lit-gov] [L-lit-perm] [L-lit-ugk]. Code: 3-week notice, council can cut it; deployed thresholds not in docs [D-lit-um]. |
| 5 | **Mantle** | **Stage 0.** 5 Stage 0 items met. Stage 1 "3 issues need fixing": the ≥75 % SC principle; "Users' withdrawals can be censored by the permissioned operators"; upgrades give <7 d to exit. Met: prover source published, program hashes reproducible. Stage 2: 2 issues [L-man-stage]. | **Validity, "Validity proofs (ST, SN)"**, 12 h execution delay, live; OP Succinct / SP1 Hypercube [L-man-risk] [L-man-sv]. **Permissioned**: proposer EOA 2 whitelisted, set by MantleSecurityMultisig; MantleEngineeringMultisig 3/7 is `challenger`, can delete roots and enable proof-less optimistic mode; "Cannot withdraw" on proposer failure [L-man-perm] [L-man-risk]. Docs: proposer nodes "not open"; ZK live since 2025-09-16 [D-man-roles] [D-man-zk] [D-man-oracle]. | **Exit window: "None"**, "contracts are instantly upgradable" [L-man-risk]. Upgrader: **MantleSecurityMultisig 6/14**, "Can upgrade with no delay" on the oracle, SystemConfig, messenger, bridge and portal; L2 Safe 6/14 no delay; 1 d timelock only for the MNT token; **no separately named Security Council** [L-man-perm] [L-man-contracts]. Docs: `ProxyAdmin` owner is "Mantle Security Msig"; threshold, members and timelock NOT FOUND in docs [D-man-l1] [D-man-v1]. |

### Table B: data availability, sequencer and forced inclusion, newest release

| Rank | Rollup | (4) Data availability | (5) Sequencer; can users force a transaction in? | (6) Newest release of main node / prover software, date |
|---|---|---|---|---|
| 1 | **Arbitrum One** | **"Onchain"**, Ethereum blobs or calldata, badge "Ethereum with blobs"; no DAC [L-arb-da]. Docs: Rollup mode posts all data to L1 as blobs when economical, else calldata [D-arb-da] [D-arb-nitro]. | Single centralised sequencer; three batch-poster EOAs; operator NOT FOUND on L2BEAT [L-arb-seq] [L-arb-perm]. **"Self sequence"**: Delayed Inbox, then anyone calls `forceInclusion` after min(1 d, delay buffer), floor 30 min [L-arb-risk] [L-arb-seq]. Docs: maintained by Offchain Labs (FAQ) or the Arbitrum Foundation (another page); `delayBlocks = 7200` ≈ 24 h; owner can pause or allowlist the Inbox [D-arb-faq] [D-arb-prog] [D-arb-forced]. | **Nitro `v3.12.2`, published 2026-10-27T13:27:32Z**, not pre-release, API-confirmed; includes the `prover` and `nitro-val` binaries [R-nitro-3122] [D-arb-bin]. An earlier read the same day saw `v3.12.1` [R-nitro-3121]; docs still pin `v3.12.1-70fa99a` [D-arb-start]. |
| 2 | **OP Mainnet** | **"Onchain"**, blobs or calldata, badge "Ethereum with blobs"; no DAC [L-op-da]. Docs: primarily blobs; registry `eth-da`; switched to calldata during 2024-06-20 fee spike then back [D-op-blog] [D-op-reg] [D-op-inc]. | **"Centralized, Raft HA"**; batcher EOA 1; operator NOT FOUND on L2BEAT and in docs [L-op-seq] [L-op-perm] [D-op-reg]. **"Self sequence"**: one L1 tx to `OptimismPortal`, "up to a 12h delay" (3,600 L1 blocks); "Self propose" [L-op-risk] [L-op-seq]. Docs: `depositTransaction`; `seq_window_size = 3600` [D-op-forced] [D-op-reg]. | **`op-node/v1.19.11`** 2026-10-22T02:51:39Z and **`op-reth/v2.6.1`** 2026-10-22T02:51:23Z (node pair); **`op-challenger/v1.11.0`** 2026-10-26T19:49:27Z, **`kona-client/v1.9.0`** 2026-10-23T21:05:25Z (fault-proof software); none pre-release [R-opnode] [R-opreth] [R-opchal] [R-kona]. Deployed absolute prestate is `v1.7.0-rc.2` per L2BEAT; release ≠ deployment [L-op-sv]. |
| 3 | **Base Chain** | **"Onchain"**, blobs or calldata, badge "Ethereum with blobs", blobs since 2024-03-14; no DAC [L-base-da] [L-base-ms]. Docs: EIP-4844 blobs primary; "Alt-DA not supported" [D-base-batcher] [D-base-cfg]. | "Centralized 5-instance Raft HA"; operator named only as "Base" on L2BEAT [L-base-seq] [L-base-perm]. **"Self sequence"** via `OptimismPortal`, up to 12 h / 3,600 L1 blocks; "Self propose" [L-base-risk] [L-base-seq]. Docs: single active sequencer; deposits "must be included" after the 12 h window; Coinbase builds Base [D-base-rel] [D-base-llms]. | **`base/base` `v1.5.1`, published 2026-10-22T17:47:20Z**, not pre-release; the repository holds base-consensus, base-reth-node and the TEE/ZK proof services, so node and prover share the release [R-base-151]. Newer `v1.5.2-rc.5` is a tag only; upstream SP1 `v6.10.0` (2026-10-23) is the ZK engine [R-sp1]. |
| 4 | **Lighter** | **"Onchain (SD)"**: state diffs in Ethereum blobs, badge "Ethereum with blobs"; no DAC; L2BEAT reproduced the state snapshot root from blobs [L-lit-risk] [L-lit-wd]. Code: `commitBatch` accepts only `PubDataMode.Blob` [D-lit-code]. | "Centralized operators"; validators EOA 1, 4, 5 [L-lit-op] [L-lit-perm]. **"Force via L1"**: deposits, withdrawals, orders, cancels and share burns can be forced through L1; if not processed within **14 d** anyone can trigger desert mode and users exit by ZK proof of balance ("Use escape hatch") [L-lit-risk] [L-lit-op] [L-lit-wd]. Code: `PRIORITY_EXPIRATION` 14 days; `activateDesertMode()` ungated [D-lit-code] [D-lit-prio]. | **Main node/sequencer: NOT FOUND**: no such repository among the 19 public `elliottech` repos; closed source not proven [R-lit-org]. Prover `lighter-prover`: **no releases, no tags**; last commit 2026-10-12T20:30:56Z [R-lit-prover]. Component: `gnark-plonky2-verifier` `v0.1.0`, 2026-10-08T09:18:05Z [R-lit-gnark]. No node-operator docs [R-lit-docs]. |
| 5 | **Mantle** | **"Onchain"**, blobs or calldata, badge "Ethereum with blobs"; EigenDA removed at Arsia, "Mantle reclassified as a rollup" 2026-04-16; no DAC [L-man-risk] [L-man-da] [L-man-ms]. Docs: `op-batcher` posts EIP-4844 blobs; Arsia activation 2026-04-22; several docs pages still describe EigenDA [D-man-arch] [D-man-mc] [D-man-mig]. | "Centralized operator", batcher EOA 1; operator entity NOT FOUND [L-man-op] [L-man-perm]. **"Self sequence"** via `OptimismPortal.depositTransaction`, up to 12 h [L-man-risk] [L-man-op]. But **"Cannot withdraw"** on proposer failure: forced inclusion gives ordering, not settlement [L-man-risk]. Docs: 24 h guide vs `seq_window_size = 3600` blocks = 12 h in config [D-man-forced] [D-man-rollup]. | **`mantle-v2` `v1.6.3` "1.6.3 Elysium", published 2026-09-21T03:38:19Z**; `op-geth` `v1.6.3` 2026-09-21T03:25:25Z; prover fork **`mantle-xyz/op-succinct` `mantle-v1.6.1`, 2026-09-16T12:28:26Z**; none pre-release [R-man-v2] [R-man-geth] [R-man-succ]. L2BEAT recorded mainnet keys updated to mantle-v1.6.1 on 2026-09-17 [L-man-upd]; mainnet docs still pin `v1.5.4` [R-man-docs]. |

## 3. Ranking method and reasons (author's analysis)

Criteria in order: L2BEAT stage; permissionless proposing and challenging; forced inclusion and exit without the operator; exit window; upgrade control (who, threshold, delay); data availability, which does not separate them since all five post to Ethereum. L2BEAT's caveat applies: stages measure decentralisation, not security [S-stages].

1. **Arbitrum One.** Only chain with a non-zero exit window on any upgrade path (10 d regular); proving fully permissionless with no allowlisted arm; the DAO sits above the 9/12 council for ordinary changes [L-arb-risk] [L-arb-sv] [L-arb-gov]. Against: the 3,600 ETH bond, the instant emergency path, and the owner's power to pause the Inbox [L-arb-sv] [D-arb-forced].
2. **OP Mainnet.** Permissionless proving with the cheapest bond (0.08 ETH) and the widest council (10/13) [L-op-sv] [L-op-perm]. Below Arbitrum because every upgrade is instant, the Guardian can switch to a permissioned game, and a liveness module can hand the council's seat to the Foundation Safe [L-op-risk] [L-op-perm] [D-op-sec].
3. **Base Chain.** Same checklist as OP Mainnet, but the common proof path (TEE proposals) is allowlisted by a Coinbase-controlled 3/6 multisig, the council is the smallest (8/11), upgrades are instant, and a 3/12 multisig can pause withdrawals for three months [L-base-sv] [L-base-perm] [L-base-gov]. The open ZK challenge path keeps it at Stage 1 and close to OP Mainnet [L-base-stage].
4. **Lighter.** Stage 0: proving permissioned to three EOAs, upgrades effectively instant because the 4/7 multisig zeroes the 21 d notice, council below Stage 1 [L-lit-op] [L-lit-ugk] [L-lit-gov]. Above Mantle because users can force transactions through L1 and, after 14 d, anyone can freeze the system and users exit by ZK proof without the operator [L-lit-risk] [L-lit-wd].
5. **Mantle.** Stage 0 with the weakest user position: proposing is whitelisted and proposer failure means "Cannot withdraw"; a 3/7 engineering multisig can turn proofs off (optimistic mode) and delete roots; a 6/14 multisig upgrades core contracts instantly; there is no named council [L-man-risk] [L-man-perm] [L-man-stage].

The three Stage 1 chains are close; a reader who weights bond cost or council size differently could swap positions 1 to 3. The Stage 0 pair is separated mainly by the escape hatch.

## 4. The three most trust-minimised

**Arbitrum One.** L2BEAT: permissionless BoLD, 3,600 ETH bond, 6 d 8 h + 2 d; "Self sequence", "Self propose"; exit window 10 d regular / None emergency (risk-panel value; other figures on the page in section 8) [L-arb-risk] [L-arb-sv] [L-arb-other]. The DAO route takes 17 d 8 h across three timelocks; the Security Council (9/12) and its L2 emergency twin can upgrade immediately [L-arb-gov] [L-arb-perm]. Docs confirm 12 members, 9-of-12 emergency with no delay, and the ordinary 8 d + challenge period + 3 d route [D-arb-const]. Forced inclusion: Delayed Inbox then `forceInclusion` (no caller restriction in code), ≈24 h in the docs, 1 d on L2BEAT; worst-case self-exit 15 d 18 h [D-arb-forced] [D-arb-code] [L-arb-seq]. Stage history: 15 config revisions in the window, criteria identical to the 2026-04-22 baseline [L-arb-hist] [G-rename].

**OP Mainnet.** L2BEAT: permissionless interactive fraud proofs, 0.08 ETH bond, 3 d 12 h + 3 d 12 h; game type 0→8 (2026-06-30, "Trust model is unchanged") and 8→9 SUPER_CANNON_KONA (2026-09-24) [L-op-sv] [L-op-upd] [G-op-8] [G-op-9]. Exit window "None"; 2/2 of Foundation Upgrade Safe 5/7 and Security Council 10/13 "Can upgrade with no delay"; policy adds review and a 7-day veto for regular upgrades, not for emergencies [L-op-gov] [L-op-perm]. The Guardian (the council) can pause, blacklist games and set the respected game type [L-op-perm]. Docs agree on the thresholds and "without upgrade delays" [D-op-roles] [D-op-sec]. Forced inclusion via `OptimismPortal`, 12 h; worst-case exit 21 d 3 h [L-op-seq]. Stage history: Stage 1 since 2024-06-10; 10 project, 31 template and 44 directory revisions in the window, no rating change [L-op-ms] [L-op-hist].

**Base Chain.** L2BEAT: "Fraud proofs (1R, ZK)"; proposals carry 0.05 ETH and a TEE attestation or ZK proof; any party with a valid ZK proof can challenge; 5 d single / 1 d dual finality [L-base-sv]. The TEE arm is allowlisted in `TEEProverRegistry`, administered by the Coordinator Multisig [L-base-perm]. Exit window "None"; Governance Multisig 2/2 of Coordinator 3/6 and Council 8/11, no timelock; it can also pause withdrawals as Guardian, blacklist games, change the respected game type and freeze SP1 verifier routes [L-base-gov] [L-base-perm]. Docs: Azul mainnet 2026-05-28, Beryl 2026-06-25, council since April 2025, no timelock found [D-base-azul] [D-base-beryl] [D-base-sc]. Forced inclusion via `OptimismPortal`, 12 h [L-base-seq] [D-base-rel]. Stage history: Stage 1 since 2025-04-29; 17 config commits in the window, Stage 2 fields unchanged [L-base-ms] [L-base-hist].

## 5. The three least trust-minimised

With five rollups the bottom three overlap the top three at Base, which is covered above; its weakest points are the allowlisted TEE proposer path, the 8/11 council with instant upgrades and the 3/12 pause power [L-base-perm] [L-base-gov].

**Lighter.** L2BEAT: "Stage 0 Appchain ZK Rollup"; Stage 1 blocked by censorable withdrawals, <7 d exit on upgrades, no proper council and the 75 % principle [L-lit-stage]. "Validity proofs (SN)", no execution delay; "Only the centralized operators can submit batches and verify them with a ZK proof" [L-lit-risk] [L-lit-op]. Upgrades: 3/5 governor via a 21 d gatekeeper, 4/7 council zeroes the delay, every upgrade so far fast-tracked [L-lit-perm] [L-lit-ugk]. Guardians EOA 2 and EOA 3 can pause for up to 72 h or 24 h; neither blocks desert mode; L2 paused 2 h on 2026-10-17 [L-lit-perm] [L-lit-wd] [L-lit-para]. Exit without operator: forced L1 requests, 14 d expiry, then desert mode; the desert circuit and a state snapshot at batch #166859 are public and L2BEAT reproduced the root [L-lit-wd]. Code confirms the validator gate, the 3-week notice, the council cut, blob-only DA and ungated `activateDesertMode()` [D-lit-code] [D-lit-um]. Stage history: Stage 0 at the 2026-04-24 baseline and at every checkpoint (Wayback 04-22, 05-12, 09-14, 10-12, live 10-27); two checklist edits inside Stage 0, see section 6 [L-lit-hist].

**Mantle.** L2BEAT: Stage 0 ZK Rollup; Stage 1 blocked by the principle, censorable withdrawals and <7 d exit [L-man-stage]. Only whitelisted proposer EOA 2 may post roots; MantleEngineeringMultisig 3/7 "can delete proposed state roots, enable/disable the optimistic (proof-less) mode and change the finalization period"; SP1VerifierGatewayMultisig 2/3 can add or freeze verifier routes [L-man-sv] [L-man-perm]. Warnings: "Funds can be stolen if optimistic mode is enabled and no challenger checks the published state", and funds frozen if the validator goes down (CRITICAL) [L-man-sv] [L-man-risksum]. Exit window "None"; MantleSecurityMultisig 6/14 upgrades the core L1 contracts with no delay; no named Security Council [L-man-perm] [L-man-contracts]. Forced inclusion through `OptimismPortal` (12 h) exists but proposer failure is "Cannot withdraw" [L-man-risk]. Docs: `ProxyAdmin` owner "Mantle Security Msig", threshold NOT FOUND [D-man-l1]. DA: Ethereum blobs since Arsia (L2BEAT 2026-04-16, project 2026-04-22) [L-man-ms] [D-man-mc]. Stage history: 12 config and 37 directory commits in the window, no `stage` override; template logic keeps the Stage 1 principle false while proofs are permissioned [L-man-hist].

## 6. Stage changes in the last six months (2026-04-27 to 2026-10-27)

**None of the five rollups changed its numbered L2BEAT stage in the window.** Robinhood Chain (excluded) did not either. Evidence: each project's L2BEAT config history against its last pre-window revision, each page's Milestones, and for Lighter the shared stage evaluator and Wayback captures [L-base-hist] [L-arb-hist] [L-op-hist] [L-man-hist] [L-lit-hist] [L-rh-hist].

Dated events near or inside the window that are **not** stage changes:

| Date | Chain | Event | Stage before → after |
|---|---|---|---|
| 2026-04-16 | Mantle | Arsia: EigenDA removed, "Mantle reclassified as a rollup" (before the window) [L-man-ms]. | Stage 0 → Stage 0 |
| 2026-04-30 | framework | Stage 1 minimum challenge period 7 d → 5 d [S-forum]. | no chain promoted |
| 2026-05-06 | all | L2BEAT renamed `getStage` → `getRollupStage`; no criteria changed [G-rename]. | unchanged |
| 2026-05-19 | Lighter | `verifierContractsReproducible` false → true; proposer failure CANNOT_WITHDRAW → USE_ESCAPE_HATCH_ZK; desert-mode warning removed [G-lit-519]. | Stage 0 → Stage 0 |
| 2026-05-23 | Lighter | node-source item 'UnderReview' → true; "under review" notice removed [G-lit-523]. Deploy date NOT FOUND (no archive between 05-12 and 09-14) [L-lit-hist]. | Stage 0 → Stage 0 |
| 2026-05-28 | Base | Azul multi-proof mainnet (L2BEAT milestone 2026-05-26) [L-base-ms] [D-base-azul]. | Stage 1 → Stage 1 |
| 2026-06-25 | Base | Beryl: single-proof window 7 d → 5 d [D-base-beryl]. | Stage 1 → Stage 1 |
| 2026-06-30 / 07-01 | OP Mainnet | Game type 0 → 8; "Trust model is unchanged" [G-op-8] [L-op-upd]. | Stage 1 → Stage 1 |
| 2026-07-01 / 07-03 | Robinhood | Mainnet launch; full L2BEAT config added (first stub 2026-02-17) [L-rh-ms] [G-rh-full] [G-rh-first]. | Other, see below |
| 2026-09-24 | OP Mainnet | Game type 8 → 9 SUPER_CANNON_KONA; "Proposing and challenging remain permissionless" [G-op-9] [L-op-upd]. | Stage 1 → Stage 1 |

Dates of the last numbered promotions, all before the window: OP Mainnet Stage 1 2024-06-10 [L-op-ms]; Arbitrum One BoLD permissionless 2025-02-15 [L-arb-ms]; Base Stage 1 2025-04-29 [L-base-ms]; Mantle and Lighter have never been above Stage 0 [L-man-hist] [L-lit-hist].

## 7. Robinhood Chain (above 500 M, category "Other", not ranked)

L2BEAT shows two stage readings at once: the API entry and the Others-tab filter say `"stage":"Stage 0"`, while the project page headline says "Robinhood Chain is not even a Stage 0 project" with the warning "The requirement for available node software is under review", and the page header and summary-row data hold `"stage":"NotApplicable"` [S-api] [L-rh-stage] [L-rh-md] [S-others]. The config leaves `isNodeAvailable` unset, which the Orbit template defaults to 'UnderReview' [G-rh-cfg] [G-orbit]. Stage 0 checklist: 4 met, node source under review, "Fraud proof submission is not sufficiently decentralized" unmet [L-rh-stage]. Proofs: BoLD "Fraud proofs (INT)" that "only allow 2 WHITELISTED actors", 6 d 8 h + 2 d [L-rh-risk] [L-rh-perm]; docs name Offchain Labs and Alchemy as the validators, allowlisted with a 1 WETH bond [D-rh-gov] [D-rh-node]. Exit window "None": Robinhood Multisig 1 (7/8) upgrades with no delay, Multisig 2 (6/8) with a 7 d timelock [L-rh-risk] [L-rh-perm]; docs: eight-seat Security Council, 6-of-8 routine with 7-day timelock, 7-of-8 emergency without [D-rh-gov]. DA "Onchain", blobs [L-rh-risk]. Sequencer centralised with compliance screening; **Sequencer failure "No mechanism"**: `forceInclusion` exists but an authorised filterer can make a force-included transaction fail "without delay"; "Self propose (28d delay)" [L-rh-risk] [L-rh-seq] [D-rh-diff]. Software: Nitro v3.12.2 (2026-10-27) [R-nitro-3122]; docs pin older images, see section 8 [D-rh-node] [D-rh-status]. No stage change in the window; mainnet 2026-07-01 [L-rh-ms] [L-rh-hist].

## 8. Source disagreements and what was not found

- **Arbitrum**: forced-inclusion delay 1 d (L2BEAT) vs 7200 blocks ≈ 24 h or `delayBlocks: 5760` (two docs pages) [L-arb-seq] [D-arb-forced] [D-arb-addl]; sequencer operator Offchain Labs (FAQ) vs Arbitrum Foundation [D-arb-faq] [D-arb-prog]; L2BEAT's own exit figures disagree (10 d, ≈17.4 d, 2 d / 11 d 8 h) [L-arb-risk] [L-arb-gov] [L-arb-other]; Nitro v3.12.1 was read before and v3.12.2 after its 2026-10-27 13:27 UTC publication [R-nitro-3121] [R-nitro-3122].
- **OP Mainnet**: no upgrade delay (docs) vs 14 d non-emergency (blog), unverified onchain [D-op-sec] [D-op-blog]; Operations Safe vs Upgrade Safe naming on L2BEAT [L-op-gov] [L-op-perm]; sequencer drift 30 min (guide) vs 600 (registry) [D-op-forced] [D-op-reg]; operator entity NOT FOUND [L-op-seq] [D-op-reg].
- **Base**: whether a non-allowlisted address can create a ZK-only game is not stated [D-base-pc]; two docs pages give different L1 ProxyAdmin Owner addresses [D-base-contracts] [D-base-cfg]; upgrade timelock NOT FOUND in docs [D-base-sc]; Azul spec page still says 7 d [D-base-azul].
- **Mantle**: forced inclusion 12 h (L2BEAT, config) vs 24 h (guide) [L-man-risk] [D-man-forced] [D-man-rollup]; multisig threshold and any council NOT FOUND in docs [D-man-l1]; several docs pages still describe EigenDA [D-man-mig] [D-man-faq]; mainnet docs pin v1.5.4 [R-man-docs]; reclassification 2026-04-16 vs Arsia 2026-04-22 [L-man-ms] [D-man-mc]; live permissionless-proposer flag NOT FOUND [D-man-oracle].
- **Lighter**: node/sequencer release NOT FOUND, closed source not proven [R-lit-org]; prover has no tags or releases [R-lit-prover]; deployed thresholds come from L2BEAT only [L-lit-perm] [D-lit-um]; deploy dates of the May checklist changes NOT FOUND [L-lit-hist]; an earlier summarised read reported zeroed guardians, superseded by the verbatim page [L-lit-para] [L-lit-perm]; docs say the escape hatch triggers "automatically", code requires a call to `activateDesertMode()` [D-lit-code].
- **Robinhood**: Stage 0 (API) vs "not even a Stage 0 project" (page) vs NotApplicable (row data) [S-api] [L-rh-md] [S-others]; node image v3.11.2 (guide) vs v3.11.4 (notice) vs v3.12.2 (status) [D-rh-node] [D-rh-notices] [D-rh-status]; own forced-inclusion parameters NOT FOUND [D-rh-msg].
- **General**: newest release ≠ deployed version for every chain; no legal sequencer operator named by L2BEAT for any of the five; L2BEAT's glossary has no "Other" entry and the summary page no methodology link [S-gloss] [S-sum].

## 9. Results this report rests on

Batch results under `artifacts/goal/batches/`: `scope/l2beat-list`; `l2beat/<chain>` (points 1 to 5), `docs/<chain>`, `release/<chain>` (point 6) for base, arbitrum, optimism, mantle, lighter, robinhood; `lighter-verbatim/lighter` (supersedes `l2beat/lighter` where they differ); `robinhood-stage/robinhood`; `lighter-stage-history/lighter`. No code was built; there is no trunk repository.

## References

Selection and framework
[S-api]: https://l2beat.com/api/scaling/summary
[S-sum]: https://l2beat.com/layer2s/summary
[S-others]: https://l2beat.com/layer2s/summary?tab=others
[S-stages]: https://l2beat.com/stages
[S-gloss]: https://l2beat.com/glossary
[S-forum]: https://forum.l2beat.com/t/the-stages-framework/291
[S-hl]: https://l2beat.com/layer2s/projects/hyperliquid
[S-pos]: https://l2beat.com/layer2s/projects/polygon-pos
[S-rh]: https://l2beat.com/layer2s/projects/robinhood

Base, L2BEAT
[L-base-stage]: https://l2beat.com/layer2s/projects/base#stage
[L-base-risk]: https://l2beat.com/layer2s/projects/base#risk-analysis
[L-base-sv]: https://l2beat.com/layer2s/projects/base#state-validation
[L-base-perm]: https://l2beat.com/layer2s/projects/base#permissions
[L-base-gov]: https://l2beat.com/layer2s/projects/base#upgrades-and-governance
[L-base-da]: https://l2beat.com/layer2s/projects/base#da-layer
[L-base-seq]: https://l2beat.com/layer2s/projects/base#sequencing
[L-base-ms]: https://l2beat.com/layer2s/projects/base#milestones-and-incidents
[L-base-hist]: https://github.com/l2beat/l2beat/commits/main/packages/config/src/projects/base/base.ts?since=2026-04-27&until=2026-10-27

Base, docs and releases
[D-base-azul]: https://docs.base.org/upgrades/azul/proofs
[D-base-pc]: https://docs.base.org/specifications/base-protocol/proofs/proof-contracts
[D-base-beryl]: https://docs.base.org/upgrades/beryl/reducing-canonical-withdrawal-delay
[D-base-sc]: https://docs.base.org/specifications/security/security-council-for-base
[D-base-contracts]: https://docs.base.org/specifications/reference/base-contracts
[D-base-cfg]: https://docs.base.org/specifications/reference/configuration
[D-base-batcher]: https://docs.base.org/specifications/base-protocol/batcher
[D-base-rel]: https://docs.base.org/specifications/security/reliability-and-liveness
[D-base-llms]: https://docs.base.org/llms.txt
[R-base-151]: https://github.com/base/base/releases/tag/v1.5.1
[R-sp1]: https://github.com/succinctlabs/sp1/releases/tag/v6.10.0

Arbitrum One, L2BEAT
[L-arb-stage]: https://l2beat.com/layer2s/projects/arbitrum#stage
[L-arb-risk]: https://l2beat.com/layer2s/projects/arbitrum#risk-analysis
[L-arb-sv]: https://l2beat.com/layer2s/projects/arbitrum#state-validation
[L-arb-perm]: https://l2beat.com/layer2s/projects/arbitrum#permissions
[L-arb-gov]: https://l2beat.com/layer2s/projects/arbitrum#upgrades-and-governance
[L-arb-other]: https://l2beat.com/layer2s/projects/arbitrum#other-considerations
[L-arb-da]: https://l2beat.com/layer2s/projects/arbitrum#data-availability
[L-arb-seq]: https://l2beat.com/layer2s/projects/arbitrum#sequencing
[L-arb-ms]: https://l2beat.com/layer2s/projects/arbitrum#milestones
[L-arb-hist]: https://github.com/l2beat/l2beat/commits/main/packages/config/src/projects/arbitrum/arbitrum.ts?since=2026-04-27&until=2026-10-27

Arbitrum One, docs and releases
[D-arb-bold]: https://docs.arbitrum.io/how-arbitrum-works/bold/gentle-introduction
[D-arb-chain]: https://docs.arbitrum.io/chain-info#chain-parameters
[D-arb-upg]: https://docs.arbitrum.foundation/network-upgrades#network-activation-statuses
[D-arb-const]: https://docs.arbitrum.foundation/dao-constitution
[D-arb-prog]: https://docs.arbitrum.foundation/state-of-progressive-decentralization
[D-arb-faq]: https://docs.arbitrum.io/get-started/faq
[D-arb-da]: https://docs.arbitrum.io/run-a-node/data-availability
[D-arb-nitro]: https://docs.arbitrum.io/how-arbitrum-works/inside-arbitrum-nitro
[D-arb-forced]: https://docs.arbitrum.io/how-arbitrum-works/deep-dives/forced-transactions
[D-arb-addl]: https://docs.arbitrum.io/launch-arbitrum-chain/chain-config/additional-configuration-parameters
[D-arb-code]: https://github.com/OffchainLabs/nitro-contracts/blob/main/src/bridge/SequencerInbox.sol
[D-arb-bin]: https://docs.arbitrum.io/run-a-node/nitro/docker-and-cli-binaries
[D-arb-start]: https://docs.arbitrum.io/run-a-node/start-here
[R-nitro-3122]: https://github.com/OffchainLabs/nitro/releases/tag/v3.12.2
[R-nitro-3121]: https://github.com/OffchainLabs/nitro/releases/tag/v3.12.1

OP Mainnet, L2BEAT
[L-op-stage]: https://l2beat.com/layer2s/projects/op-mainnet#stage
[L-op-risk]: https://l2beat.com/layer2s/projects/op-mainnet#risk-analysis
[L-op-sv]: https://l2beat.com/layer2s/projects/op-mainnet#state-validation
[L-op-upd]: https://l2beat.com/layer2s/projects/op-mainnet#637b2364
[L-op-perm]: https://l2beat.com/layer2s/projects/op-mainnet#permissions
[L-op-gov]: https://l2beat.com/layer2s/projects/op-mainnet#upgrades-and-governance
[L-op-da]: https://l2beat.com/layer2s/projects/op-mainnet#data-availability
[L-op-seq]: https://l2beat.com/layer2s/projects/op-mainnet#sequencing
[L-op-ms]: https://l2beat.com/layer2s/projects/op-mainnet#milestones-and-incidents
[L-op-hist]: https://github.com/l2beat/l2beat/commits/main/packages/config/src/projects/optimism?since=2026-04-27&until=2026-10-27
[G-op-8]: https://github.com/l2beat/l2beat/commit/cfafbf3de953d9f519656c89c622fe51a04d547a
[G-op-9]: https://github.com/l2beat/l2beat/commit/da23cf33e845a8531717703d705f14a554436f89

OP Mainnet, docs and releases
[D-op-fp]: https://docs.optimism.io/op-stack/fault-proofs/explainer
[D-op-karst]: https://docs.optimism.io/op-stack/protocol/hardforks/karst
[D-op-sec]: https://docs.optimism.io/op-stack/security/faq-sec-model
[D-op-roles]: https://docs.optimism.io/op-stack/protocol/privileged-roles
[D-op-blog]: https://optimism.io/blog/institutional-defi-fortune-500-enterprises
[D-op-reg]: https://github.com/ethereum-optimism/superchain-registry/blob/main/superchain/configs/mainnet/op.toml
[D-op-inc]: https://status.optimism.io/clxnipyv759364bhmsk2dwifoa
[D-op-forced]: https://docs.optimism.io/op-stack/transactions/forced-transaction
[R-opnode]: https://github.com/ethereum-optimism/optimism/releases/tag/op-node%2Fv1.19.11
[R-opreth]: https://github.com/ethereum-optimism/optimism/releases/tag/op-reth%2Fv2.6.1
[R-opchal]: https://github.com/ethereum-optimism/optimism/releases/tag/op-challenger%2Fv1.11.0
[R-kona]: https://github.com/ethereum-optimism/optimism/releases/tag/kona-client%2Fv1.9.0

Mantle, L2BEAT
[L-man-stage]: https://l2beat.com/layer2s/projects/mantle#stage
[L-man-risk]: https://l2beat.com/layer2s/projects/mantle#risk-analysis
[L-man-risksum]: https://l2beat.com/layer2s/projects/mantle#risk-summary
[L-man-sv]: https://l2beat.com/layer2s/projects/mantle#state-validation
[L-man-perm]: https://l2beat.com/layer2s/projects/mantle#permissions
[L-man-contracts]: https://l2beat.com/layer2s/projects/mantle#contracts
[L-man-da]: https://l2beat.com/layer2s/projects/mantle#da-layer
[L-man-op]: https://l2beat.com/layer2s/projects/mantle#operator
[L-man-ms]: https://l2beat.com/layer2s/projects/mantle#milestones-and-incidents
[L-man-upd]: https://l2beat.com/layer2s/projects/mantle?update=706bc529
[L-man-hist]: https://github.com/l2beat/l2beat/commits/main/packages/config/src/projects/mantle/mantle.ts?since=2026-04-27&until=2026-10-27

Mantle, docs and releases
[D-man-zk]: https://docs.mantle.xyz/network/system-information/risk-management/zk-validity-proof.md
[D-man-roles]: https://docs.mantle.xyz/network/for-node-operators/network-roles.md
[D-man-oracle]: https://github.com/mantle-xyz/op-succinct/blob/8d280ded13f3fcba3d85fb6babedaf75cab5e9c0/contracts/src/validity/OPSuccinctL2OutputOracle.sol
[D-man-l1]: https://docs.mantle.xyz/network/system-information/on-chain-system/key-l1-contract-address.md
[D-man-v1]: https://docs.mantle.xyz/network/network/introduction/security-model-and-roles.md
[D-man-arch]: https://docs.mantle.xyz/network/system-information/architecture.md
[D-man-mc]: https://github.com/mantle-xyz/op-succinct/blob/8d280ded13f3fcba3d85fb6babedaf75cab5e9c0/MANTLE_CHANGES.md
[D-man-mig]: https://docs.mantle.xyz/network/introduction/updated-notices/migration-of-data-availability-to-ethereum-blobs.md
[D-man-faq]: https://docs.mantle.xyz/network/more/faqs.md
[D-man-forced]: https://docs.mantle.xyz/network/system-information/risk-management/forced-transaction-inclusion.md
[D-man-rollup]: https://github.com/mantle-xyz/networks/blob/f6e0f07ce813bd2f9965fceb7c32756b2f55d383/mainnet/rollup.json
[R-man-v2]: https://github.com/mantle-xyz/mantle-v2/releases/tag/v1.6.3
[R-man-geth]: https://github.com/mantle-xyz/op-geth/releases/tag/v1.6.3
[R-man-succ]: https://github.com/mantle-xyz/op-succinct/releases/tag/mantle-v1.6.1
[R-man-docs]: https://docs.mantle.xyz/network/for-node-operators/deployment-guides/mainnet-v1.5.4

Lighter, L2BEAT
[L-lit-stage]: https://l2beat.com/layer2s/projects/lighter#stage
[L-lit-risk]: https://l2beat.com/layer2s/projects/lighter#risk-analysis
[L-lit-op]: https://l2beat.com/layer2s/projects/lighter#operator
[L-lit-perm]: https://l2beat.com/layer2s/projects/lighter#permissions
[L-lit-gov]: https://l2beat.com/layer2s/projects/lighter#upgrades-and-governance
[L-lit-ugk]: https://l2beat.com/layer2s/projects/lighter#contracts-eth:0x94da8A995D0D82Ef0fE7E509C6D76c22603B6f67
[L-lit-wd]: https://l2beat.com/layer2s/projects/lighter#withdrawals
[L-lit-para]: https://l2beat.com/scaling/projects/lighter
[L-lit-hist]: https://github.com/l2beat/l2beat/blob/b3346aafa392488900d7a556a206cfabc7acf611/packages/config/src/projects/lighter/lighter.ts
[G-lit-519]: https://github.com/l2beat/l2beat/commit/307f5c3dfdab6a4f88448861a0bb75f0043b762b
[G-lit-523]: https://github.com/l2beat/l2beat/commit/abff564c9d5cf273d1708b3509cfd10eb11a791e
[G-rename]: https://github.com/l2beat/l2beat/commit/995eebbdd8d1f4c660341c19a27cbde34be98b24

Lighter, docs, code and releases
[D-lit-code]: https://github.com/elliottech/lighter-contracts/blob/5896c8f1425d56bc96675b76eeb142611ceca9a7/contracts/ZkLighter.sol
[D-lit-um]: https://github.com/elliottech/lighter-contracts/blob/5896c8f1425d56bc96675b76eeb142611ceca9a7/contracts/UpgradeableMaster.sol
[D-lit-prio]: https://docs.lighter.xyz/developers/reference/priority-transactions.md
[R-lit-org]: https://api.github.com/orgs/elliottech/repos
[R-lit-prover]: https://github.com/elliottech/lighter-prover/releases
[R-lit-gnark]: https://github.com/elliottech/gnark-plonky2-verifier/releases/tag/v0.1.0
[R-lit-docs]: https://docs.lighter.xyz/sitemap-pages.xml

Robinhood Chain
[L-rh-stage]: https://l2beat.com/layer2s/projects/robinhood#stage
[L-rh-md]: https://l2beat.com/layer2s/projects/robinhood.md
[L-rh-risk]: https://l2beat.com/layer2s/projects/robinhood#risk-analysis
[L-rh-perm]: https://l2beat.com/layer2s/projects/robinhood#permissions
[L-rh-seq]: https://l2beat.com/layer2s/projects/robinhood#sequencing
[L-rh-ms]: https://l2beat.com/layer2s/projects/robinhood#milestones-and-incidents
[L-rh-hist]: https://github.com/l2beat/l2beat/commits/main/packages/config/src/projects/robinhood/robinhood.ts?since=2026-04-27&until=2026-10-27
[G-rh-cfg]: https://github.com/l2beat/l2beat/blob/main/packages/config/src/projects/robinhood/robinhood.ts
[G-orbit]: https://github.com/l2beat/l2beat/blob/main/packages/config/src/templates/orbitStack.ts
[G-rh-first]: https://github.com/l2beat/l2beat/commit/32bba0a061f4995dc6d376ebc22e68d643812466
[G-rh-full]: https://github.com/l2beat/l2beat/commit/167aafe84eb65da4d711e3031b6a4df3d5d23fb8
[D-rh-gov]: https://docs.robinhood.com/chain/governance
[D-rh-node]: https://docs.robinhood.com/chain/run-a-full-node
[D-rh-diff]: https://docs.robinhood.com/chain/differences-from-ethereum
[D-rh-msg]: https://docs.robinhood.com/chain/cross-chain-messaging
[D-rh-notices]: https://docs.robinhood.com/chain/notices-and-upgrades
[D-rh-status]: https://status.robinhoodchain.offchain.io/
