**Taylor (gtmcknight) AMM research: final policy and evidence**

**The strongest delivered contract, R (LEAN tell plus refitted coefficients), gains +3.206713 over qt1 on report seeds 10000–12047: n=2,048, paired SE=0.022401.** Its fresh release-engine result is **+3.161202, SE=0.035513, n=768**. The complete, unchanged `Strategy.sol` and its two imports are embedded below. The goal did **not** establish #1, and no leaderboard submission was made. R passes the measured label, fee, size and gas checks, but its 768 engine pairs are **256 short of requester note 7's two × 512 requirement**. The larger LEAN sample cannot fill that gap for a different contract. [rq-1][b33-rq-1], [rq-2][b33-rq-2], [rq-3][b33-rq-3], [rq-4][b33-rq-4], [rp-1][b32-rp-1], [rp-2][b32-rp-2], [rp-3][b32-rp-3].

Taylor authored the replica, Gaussian/lattice filters, solved dynamic program and qm tables. This work builds on his [pinned solved research and README](https://github.com/gtmcknight/amm-sim/tree/4812a6382311624e1506aca131ca35c378f930d9/research/solved), commit `4812a6382311624e1506aca131ca35c378f930d9`, and IdentityMD's qt1/QMRef, TwoComp/TC-A and COMBO extensions. The delivered improvement comes chiefly from identifying the simulator's floating-point trade path, then retaining a small retail hypothesis when that identification is positive. A coefficient refit contributes a further **+0.046805 on the replica** and **+0.050019 on the engine**, paired against unchanged LEAN.

| Delivered R identity / measurement | Value |
|---|---|
| Complete source | [Embedded Strategy.sol](#strategy-source); called `scratch/StrategyR.sol` in each rp bundle; Solidity contract remains `Strategy` |
| Source bytes / SHA-256 | 49,905 / `c54d8d48d4a62ac655024ffa8b0e808e45d9809c9612fb614895aab10aee3491` |
| Deployed runtime bytes / SHA-256 | 22,953 / `23f8715372e4edf06692c342e082521ef1e601575616f1042b458eb6118e954e` |
| Compiler settings | solc 0.8.24; viaIR; optimizer enabled, 200 runs; EVM `paris`; source key `Strategy.sol`; default metadata settings retained |
| Maximum observed engine afterSwap gas | 222,787; 22,213 below the 245,000 limit |
| Size margin | 1,623 bytes below 24,576 |
| Engine safety sample | 8,578,549 R callbacks over 792 distinct seeds, including 24 pilot seeds; zero OOG and zero reported other failures |
| Scored engine sample | 768 distinct non-pilot seeds; R−qt1 +3.161202 (SE 0.035513); R−LEAN +0.050019 (SE 0.005857) |
| Refit blob SHA-256 | `ca5a606d074224ccc72fb4999c1d01a677ba00440ba39df2f99eba4913a72e1d` |
| Build agreement | rp-1, rp-2 and rp-3 contain byte-identical source; same engine runtime identity reported |

These gas maxima are measurements on the stated samples, not universal bounds. Source identity and statistics were checked again for this write-up; compilation and simulations were not rerun here. The artifact's header still mentions the **old** blob hash `3ac7cb88…`, and `getName()` still returns `TaylorTCALeanTell`. Both are preserved so the delivered source has the tested hash. The actual decoded coefficients have the new hash above. [rp-1][b32-rp-1], [rp-2][b32-rp-2], [rp-3][b32-rp-3].

There is **no goal trunk repository or merged commit** to name: the supplied `goal.json` has `trunk: null`, and all 36 batches are research batches. The contract is delivered through the content-addressed item bundles and the source in this report. The execution repository is [benedictbrady/amm-challenge at 6b6921f8d463314aa7c96234e1be25a25245f704](https://github.com/benedictbrady/amm-challenge/tree/6b6921f8d463314aa7c96234e1be25a25245f704); that is an upstream pin, not a commit reached by this goal. Notes also reference an external goal's TC-A ancestor in `identity-md-launches/goal-3170-beat-network-s-amm-entry` at `4eb3e985fd31e3cd17832501b95b6d2491aca73d`; it is not this goal's trunk or final R source.

**Taylor-derived measurement conventions and gate evidence**

“qt1” throughout means the compressed **QMRef** Python reference and the qt1 Solidity artifact, not Taylor's uncompressed Gaussian+qm gate column. “LEAN” means lb-4's TC-A two-component filter with bounded rounding tell and original QMS1 coefficients. “R” changes only those coefficients to the visit-refit blob. “COMBO” is TwoComp plus weighted-average branch quoting, an earlier base. A gain against COMBO includes neither a gain against LEAN nor an independently measured stack.

Replica figures are total own-pool edge per 10,000-step run, in the simulator's Y units; **they are not fee bps or board scores**. For each seed, `d = candidate_edge − reference_edge`; mean is the arithmetic mean of d and SE is sample SD(d)/sqrt(n). “Worst5” means five lowest individual seed differences, ordered by difference then seed. Engine evaluations run each strategy **separately against the 30 bps VanillaStrategy**, using `amm_sim_rs.run_batch(X, VanillaStrategy, configs, 8)` with `MatchRunner._build_configs` configurations. Candidate and qt1 share seed/configuration; they are not matched directly against each other. F compares fees in bps, a separate unit. [lb-4][b27-lb-4], [rp-3][b32-rp-3], [cf-2][b31-cf-2].

The tell's replica evaluations use Taylor's random streams through the engine-order Python port, so callback WAD arithmetic follows the engine. Unmodified `replica2` alone does not provide the required rounded callback stream. P and base-port comparisons are therefore separate checks. The release wheel has SHA-256 `aedb68280aca34c110968f00148387c95885207913fb2cf19a1ab4c5cfd6887a`; workers report checking that pinned wheel and completing the prescribed setup. Source-built diagnostic engine runs from the earlier tell experiments are not mixed into the release-wheel performance sample.

| Gate | R evidence | Qualification |
|---|---|---|
| P: unchanged Taylor baseline | All three rp and four rq items report the original gates.py values below before changes | Reported worker runs; independently reading source/hash is not a new P run |
| Q: choose and report | Four 256-seed choose blocks cover 64000–65023; four 512-seed report blocks cover 10000–12047, paired against LEAN and qt1 | R selected on choose; prior research had already exposed portions of these common windows, as disclosed below |
| Q numerical thresholds | R−qt1 +3.206713; worst −1.311917; three negative seeds, none below −2 | Exceeds both original +0.5 contract eligibility and later +2.0 tell threshold |
| T: label parity | 350,950 first trades on replica seeds 74200–74249; zero Solidity/reference mismatches in each rp item | All three repeat the same seed stream; do not count this as 1,052,850 unique labels |
| F: fee parity | 50 × 2,000 = 100,000 callbacks; maximum error 4.839644136833687e−7 bps; zero over 0.01 bps | Same test seeds repeated by three builders; F is numerical fidelity, separate from engine gas |
| G: size and gas | Runtime 22,953 bytes; engine peak 222,787; zero failures across the 792-seed sample | Fits both numeric caps on observed runs |
| E: fresh paired engine | Three disjoint 256-seed windows, n=768, all with R/LEAN/qt1 arms | Strong measured gain; original two × 512 quota remains incomplete for R |

Sources: [rp-1][b32-rp-1], [rp-2][b32-rp-2], [rp-3][b32-rp-3], [rq-1][b33-rq-1], [rq-2][b33-rq-2], [rq-3][b33-rq-3], [rq-4][b33-rq-4]. In rp-3, a negative control ran unchanged LEAN against the R reference and failed F at about **4.23 bps**, demonstrating that the parity test distinguishes the coefficient sets. rp-2 ran G before Q; rp-3 repaired a test-harness NameError and restarted F. Those procedural departures do not alter the frozen source, but prevent claiming perfect gate-order compliance across every item.

The P reference, corroborated by the pinned [Taylor README](https://raw.githubusercontent.com/gtmcknight/amm-sim/4812a6382311624e1506aca131ca35c378f930d9/research/solved/README.md), is:

| Seed | Perfect information | Gaussian/plain | Gaussian/qm | Lattice/qm |
|---|---:|---:|---:|---:|
| 10000 | 448.261189 | 443.455598 | 443.522608 | 443.663520 |
| 10001 | 576.779199 | 571.463409 | 571.623551 | 571.977293 |
| 10002 | 531.886497 | 525.168028 | 525.865859 | 526.411631 |

Actual qt1/QMRef on those three seeds is approximately **443.101741 / 571.454483 / 525.908441**. The full original report-window reference gives qt1−HA **+3.705396 (SE 0.038086)**, TwoComp−qt1 **+0.424803 (0.012202)** and COMBO−qt1 **+0.597391 (0.013388)**. COMBO with true first-trade flag gives **+3.167510 over qt1 (0.022386)**, or **+2.570119 over COMBO (0.020763)**. That frozen-base intervention is an oracle diagnostic, not a global upper bound on policies. [Root 1][root-1-01].

**Taylor-derived R selection, paired report and tails**

Each rq item used the predeclared rule “R if mean(R−LEAN) > 2 SE on its choose block; otherwise LEAN,” and recorded the choice before its own report block. All four chose R. No policy was selected in this write-up.

| Item | Choose seeds | Choose R−LEAN (SE) | Report seeds | Report R−LEAN (SE) | Report R−qt1 (SE) |
|---|---|---:|---|---:|---:|
| [rq-1][b33-rq-1] | 64000–64255 | +0.052353 (0.010491) | 10000–10511 | +0.044785 (0.006685) | +3.172116 (0.045955) |
| [rq-2][b33-rq-2] | 64256–64511 | +0.036939 (0.009592) | 10512–11023 | +0.041670 (0.007600) | +3.199706 (0.044021) |
| [rq-3][b33-rq-3] | 64512–64767 | +0.059771 (0.010058) | 11024–11535 | +0.041595 (0.007030) | +3.173857 (0.043250) |
| [rq-4][b33-rq-4] | 64768–65023 | +0.061482 (0.009678) | 11536–12047 | +0.059167 (0.007465) | +3.281175 (0.045880) |
| Pooled | 64000–65023, n=1024 | **+0.052636 (0.004982)** | 10000–12047, n=2048 | **+0.046805 (0.003603)** | **+3.206713 (0.022401)** |

The pooled report result was recomputed from all 2,048 supplied per-seed rows, with every seed present exactly once. Some rows are rounded to six decimals; six-decimal displayed pooled statistics are appropriate. LEAN−qt1 on the identical rows is **+3.159909 (SE 0.022227)**. R improves the mean while losing to LEAN on **770/2,048 seeds**; it is not a pointwise improvement.

| Paired report comparison | Worst five `(seed, difference)` |
|---|---|
| R−qt1 | (11062, −1.311917), (11519, −0.059604), (11376, −0.018040), (10642, +0.229206), (10141, +0.288098) |
| R−LEAN | (10843, −1.587869), (10852, −1.103122), (11675, −0.822112), (11998, −0.771508), (10357, −0.659034) |
| LEAN−qt1 | (11062, −1.359683), (11376, +0.012547), (11519, +0.161653), (10642, +0.225519), (10146, +0.257514) |

The coefficient fit used 64000–64511 visits and selected regularization on 64512–65023 under a different TwoComp+Bayes-tell BASE. Those validation seeds overlap rq-3/rq-4 choose blocks; upstream work also scored the common report window before these confirmations. rq results establish fixed-policy replication and no within-item report tuning, not a newly untouched holdout after the whole research program. The original refit's cap rule changed from one-SE to two-SE after its choose grid; its selected regularization values were weakly separated. These are selection qualifications, not reasons to silently discard the measurements. Fresh engine blocks provide additional evidence on a different seed population. [visit-refit][b25-visit-refit], [rq-3][b33-rq-3], [rq-4][b33-rq-4].

**Taylor-derived release-engine result and fallback**

R's engine seed windows are disjoint. Its score pool excludes the three eight-seed G pilots; its gas accounting includes them. Each item built the same source and paired all three strategies on the same seeds.

| Item | E seeds, inclusive | n | R−qt1 (SE) | R−LEAN (SE) | LEAN−qt1 (SE) | R peak gas |
|---|---|---:|---:|---:|---:|---:|
| [rp-1][b32-rp-1] | 9993100–9993355 | 256 | +3.129248 (0.059045) | +0.052317 (0.009531) | +3.076931 (0.060051) | 221,453 |
| [rp-2][b32-rp-2] | 9994100–9994355 | 256 | +3.226191 (0.062077) | +0.048429 (0.010329) | +3.177762 (0.061187) | 222,476 |
| [rp-3][b32-rp-3] | 9995100–9995355 | 256 | +3.128167 (0.063368) | +0.049312 (0.010585) | +3.078855 (0.062720) | 222,787 |
| Pooled | Three windows above | **768** | **+3.161202 (0.035513)** | **+0.050019 (0.005857)** | **+3.111183 (0.035403)** | **222,787** |

R−qt1 engine **worst5**: **(9995148, −0.387974), (9993174, +0.162958), (9995355, +0.626613), (9995311, +0.785173), (9995268, +0.804769)**. R−LEAN worst5: (9995204, −0.662688), (9993246, −0.578798), (9994129, −0.512531), (9993244, −0.500469), (9993197, −0.390608). These are retained rather than excluding losing seeds. R safety counts are 2,842,643 + 2,876,593 + 2,859,313 callbacks = **8,578,549**, over pilots 9993000–9993007, 9994000–9994007, 9995000–9995007 plus the 768 E seeds.

The fallback is lb-4's original LEAN `Strategy.sol`, SHA-256 **`a243bb3570545fb614d8995ced61e811db8e075af68e636add20eaf8fbaeebfb`**, runtime **22,946 bytes**, runtime SHA-256 **`dab7d69ddb7a172624b37828021941904406326442fb11f750a727e16707d017`**. Four confirmation items rebuilt it unchanged and reported matching source/runtime identities. This fallback is confirmed on substantially more fresh seeds than R; the direct R−LEAN comparisons, rather than unrelated engine means, support the coefficient upgrade. [lb-4][b27-lb-4], [cf-1][b31-cf-1], [cf-2][b31-cf-2], [cf-3][b31-cf-3], [cf-4][b31-cf-4].

| LEAN engine evidence | Seeds, inclusive | n | LEAN−qt1 (SE) | Peak afterSwap |
|---|---|---:|---:|---:|
| lb-4 window 1 | 9978100–9978355 | 256 | +3.225709 (0.062389) | 221,835 |
| lb-4 window 2 | 9978400–9978655 | 256 | +3.099814 (0.058114) | 224,481 |
| cf-1 | 9990000–9990511 | 512 | +3.213144 (0.043373) | 225,355 |
| cf-2 | 9990512–9991023 | 512 | +3.194663 (0.039750) | 223,146 |
| cf-3 | 9991024–9991343 | **320** | +3.130325 (0.053718) | 222,652 |
| cf-4 | 9991536–9992047 | 512 | +3.222989 (0.043896) | 224,693 |
| cf confirmations only | Four cf windows | 1856 | +3.196483 (0.022261) | 225,355 |
| lb-4 + cf | Six windows | 2368 | +3.189192 (0.019736) | 225,355 |
| All LEAN E pairs, also rp controls | Above plus the 768 rp seeds | **3136** | **+3.170087 (0.017249)** | **225,355** |

All final-LEAN runs above report zero OOG and other callback failures. Including its 32 pilot seeds, the total is **3,168 seeds / 34,419,397 callbacks**, not 3,168 independent E pairs. Across the full 3,136 E pairs, worst5 are (9991691, −0.552468), (9995148, −0.515803), (9991141, −0.387310), (9993174, +0.137388), (9991276, +0.345017). cf-3 omitted **9991344–9991535 (192 seeds)** because of its stated runtime allowance; they contribute neither zeros nor observations.

Independent LEAN T checks on 74300–74499 cover **1,396,492 first trades with zero mismatches**; four F checks cover **400,000 callbacks**, maximum fee error **4.820135496253972e−7 bps**. These are distinct from lb-4's original T/F seeds and R's repeated T/F stream. The early “tell costs at most 9,800 gas” statement was only lb-4's sample maximum: later probes reached 12,811 for LEAN and 13,055 for R. Whole-callback engine maxima, not isolated tell microbenchmarks, govern the limit. [cf-1][b31-cf-1], [cf-2][b31-cf-2], [cf-3][b31-cf-3], [cf-4][b31-cf-4], [rp-2][b32-rp-2].

The reserved/consumed engine regions in goal notes are 9900000–9900015; 9950000–9950031; 9960000–9963095; 9970000–9983655; 9990000–9992047; and 9993000–9995355. These broad reservations include unused gaps and failed/superseded experiments; they are not counts of successful evaluations. **9996000 is the next fresh region recorded by the goal.** An additional R confirmation would need new seeds; no unused or uncertain reservation should be recycled.

**Taylor-derived classifier result: ordinary observables versus arithmetic tell**

The brief's approximately 16% error describes the filter problem. Actual measured qt1/QMRef error is **17.3073%** and COMBO error **16.1186%** on their full report trajectories. Conventional observable models reduced that error modestly. The rounding tell changed it by orders of magnitude on measured streams.

| Classifier / diagnostic | Population | Error achieved | Interpretation |
|---|---|---:|---|
| qt1/QMRef | Report, 14,374,445 first own callbacks | 2,487,830 errors = **17.3073%** | Correct baseline identity matters |
| COMBO | Report, 14,382,447 first own callbacks | 2,318,251 = **16.1186%** | About 16%, as in the research premise |
| data-b GBT, 41 features | 64 held-out seeds, 450,628 rows | **15.9639%**, versus 16.1639% | −0.2000 percentage points; offline, no live fee-policy gain measured |
| data-c GBT, 52 features | 64 held-out seeds, 450,109 rows | **15.8719%**, versus 16.1723% | −0.3004 points; distinct dataset/model |
| routing teacher / compact guarded net | Held-out training dataset / live report | Teacher held-out **15.651%**; compact live diagnostic about **15.685%** | Best conventional classifier line; live score mattered more than hard-error rank |
| o1-a public-WAD tell | 8 replica-port seeds, 54,543 first trades | **32/54,543 = 0.0587%** | Corrected 8,818 of 8,821 COMBO errors on that stream |
| o1-b public-WAD tell | Different 8 port seeds, 57,783 first trades | **31/57,783 = 0.0536%** | Corrected 8,926 of 8,930 COMBO errors |
| LEAN diagnostic A0 | go-1, 64000–64511, 3,590,733 first trades | **993/3,590,733 = 0.0277%** | Closed-loop LEAN sample; not an independently logged error census for R's full report window |
| R Solidity T | 50-seed R reference stream | **0 implementation-label disagreements / 350,950** | Parity with Python, **not** zero mistakes versus true trade type |

Sources: [Root 1][root-1-01] for conventional classifiers; [Root 2][root-1-02] for o1-a/b; [go-1][b34-go-1] for LEAN; [rp-3][b32-rp-3] for R parity. The classifier populations differ and must not be pooled. The final rq records count tell outputs but do not supply a full R truth-error census, so no exact all-report R accuracy is claimed. Early notes called the ordinary-feature error an “information limit”; these experiments do not prove a Bayes limit, and the arithmetic tell demonstrates additional observable information outside those feature sets.

The final LEAN/R tell examines WAD amounts, previous own reserve WADs and the fee actually returned. On pool sells (`isBuy=false`), arbitrage and retail compute their amounts through different binary64 paths; on pool buys, the useful distinction lies in the upstream arbitrage sizing grid, despite a shared execution function. The contract implements bounded round-to-nearest-even arithmetic, including WAD conversions, and tests compatibility with the arb grid. A positive is not certainty: retail can collide with it. Positive evidence updates `pi` by Bayes with retail likelihood **15/13131 on sells** or **16/12889 on buys**, caps it at **0.9999**, and retains the retail component. Negative evidence sets pi to zero; unsupported or over-budget results preserve the original filter probability. Candidate budget is four. [lb-4][b27-lb-4].

This uncertainty is essential. o1-b's hard 0/1 version lost as much as **−158.769603 versus COMBO on seed 10146** despite low classification error. Its Bayesian version gained +2.543263 (SE 0.057067) over COMBO on a 256-seed report subset, within +0.010823 of that subset's flag oracle; that early subset was not full Q. Later LEAN full-window Q and release-engine pairings supplied the stronger evidence. In go-1/go-2, replacing LEAN's call with the true flag adds only **+0.006648 (0.005648)** and **+0.005805 (0.006060)** on their respective 512-seed choose blocks. Those interventions include timestamp-zero handling and are not a pure error-count-to-return conversion. [Root 2][root-1-02], [go-1][b34-go-1], [go-2][b34-go-2].

The tell uses the simulator's numerical implementation. Its success on the pinned release wheel supports that implementation only; it establishes neither equivalence with a different leaderboard-server binary nor organizer acceptance of the technique. The requester approved testing and then gated building in notes 6–7, while reserving submission for a later user decision. Nothing in this report changes that status.

**Taylor-derived results of every research line**

The following ledger retains successes, negative results, incomplete work and controls. Unless a row names another range, “full report” means n=2,048 on 10000–12047. Parenthetical values are paired SEs. Rows grouped by family remain separate experiments; their gains are not summed. Root merges preserve the older items' original identifiers, source digests, tails and detailed limitations.

| Batch / item(s) | Result and disposition |
|---|---|
| e02-baselines / references | Cancelled without an accepted result. qt1/TwoComp/COMBO baselines were instead corroborated by data and flag items. |
| e02-observable-data / data-a, data-b, data-c | data-a cancelled without result. data-b/data-c offline errors 15.9639%/15.8719%; conventional observable signal modest, not a proof of an information bound. [Root 1][root-1-01] |
| e02-classifier / filter-only | Compact table: +0.008647 (0.006813) over COMBO, +0.606015 (0.013571) over qt1, full report. Weak incremental result; multiple upstream source-recheck flags. [Root 1][root-1-01] |
| e02-classifier / history | Selected half-strength compact: +0.037480 (0.007527) over COMBO, +0.634871 (0.013728) over qt1. Full-strength/teacher report increments +0.015654/+0.045281; selection on choose, not lower Brier alone. [Root 1][root-1-01] |
| e02-classifier / routing | Guarded compact +0.078039 (0.009144) over COMBO; +0.675430 (0.014250) over qt1. Teacher +0.119282 (0.009579) over COMBO; +0.716673 over qt1. Unguarded net had roughly −30 seed losses. No contract. [Root 1][root-1-01] |
| e02-classifier / all-observables | Compact +0.028164 (0.008299) over COMBO; +0.625421 (0.013546) over qt1. No gas measurement; source qualification retained. [Root 1][root-1-01] |
| e02-residual-head / eight-output | Six small-sigma generations: +0.076499 (0.008473) over COMBO; +0.673867 (0.013783) over qt1. Exact original frozen-weight file absent; later reconstruction used rounded weights. [Root 1][root-1-01] |
| e02-residual-head / sixteen-output | Two tested perturbations lost; selected zero head = COMBO. Report qt1 comparison reused published baseline rows with spot checks; no learned improvement or complete fresh Q. [Root 1][root-1-01] |
| e02-residual-head / eight-joint; sixteen-symmetric | Full-report increments over COMBO +0.032444 (0.007277) / +0.017715 (0.007374); over qt1 +0.629835 / +0.615106. Small replica gains only. [Root 1][root-1-01] |
| e02-probability-tables / pi-five; other pending item | pi-five DP regeneration timed out at 470 s before integrated policy/Q; useful common-action expectation formulation, no measured improvement. Other item cancelled without result. [Root 1][root-1-01] |
| e02-flag-localization / qt1-strata | Oracle flag on small-trade bucket: +2.169006 (0.019531) over qt1; phase-1 bucket +2.267638 (0.019481); full flag +3.167510. Buckets overlap and are not additive. [Root 1][root-1-01] |
| e02-flag-localization / combo-strata | Two stale-pin/small-fill oracle buckets +0.490970 (0.010976) and +0.362310 (0.009597) over COMBO. Descriptive error anatomy, not deployable classification. [Root 1][root-1-01] |
| e02-flag-ceilings / combo-flag; other pending item | Full COMBO flag +2.570119 over COMBO, +3.167510 over qt1; other item cancelled. Fixed-base oracle, not attainable-policy certification. [Root 1][root-1-01] |
| e03-finer-solve / finer-a, finer-b | Fine 2.5 bps tables: +0.097021 (0.007661) / +0.093105 (0.007779) over COMBO, +0.694412 / +0.690496 over qt1. About +0.05 is grid refinement and +0.043 is compression removal. Under true flag, fine-over-full-coarse gain only +0.006754/+0.005157, statistically weak. Large arrays, differing convergence controls; no contract. [Root 1][root-1-01] |
| e03-full-posterior / posterior-a | Expected value before common-action argmax: +0.421303 (0.012069) over COMBO, +1.018694 (0.014377) over qt1; true-flag version +3.272681 over qt1. Best early conventional-policy result, but expensive lattice/action search, numerical and source qualifications, report-overlap debugging; no contract. [Root 1][root-1-01] |
| e03-full-posterior / posterior-b | Different implementation lost −121.953 (7.768) over 30 choose seeds, then timed out; no report. Unresolved implementation failure, not a refutation or replication of posterior-a. [Root 1][root-1-01] |
| e03-smoothing / smoothing-a, smoothing-b | a cancelled; b blocked on source-download connection resets before P. No performance result. [Root 1][root-1-01] |
| e03-information / information-a, information-b | Selected ambiguity-aware kappa=1e−5 gives −0.016225 (0.009022) / −0.016066 (0.009024) over COMBO. Larger kappa cuts error but sharply hurts return (about −16.87 at 1e−4). Flagged increment about +0.102716 over Flag, mostly a different table comparison. [Root 1][root-1-01] |
| e04-residual-a / res-a | −0.171475 (0.022841) over COMBO, +0.430912 over qt1 on only 384 report seeds; incomplete Q. [Root 1][root-1-01] |
| e04-residual-a / res-b | 51 short-horizon generations selected zero head; full choose/report exactly COMBO. No learned gain. [Root 1][root-1-01] |
| e04-residual-a / res-c | Reduced training protocol; selected nonzero head lost −0.385188 (0.090586) over COMBO on only 32 report seeds. Zero control omitted in selection; incomplete Q. [Root 1][root-1-01] |
| e04-residual-b / res-d | Specified run selected zero. Output-only sensitivity +0.008144 (0.006705) over COMBO, +0.605571 over qt1; unresolved incremental signal, protocol departure. [Root 1][root-1-01] |
| e04-residual-b / res-e, res-f | Full-report increments −0.184300 (0.010696) / −1.339070 (0.017958) over COMBO; qt1 differences +0.412956 / −0.741679. More generations alone did not fix short-horizon/scale problems. [Root 2][root-1-02] |
| e04-belief-solve / bs-a | −7.162411 (0.040675) over COMBO; collapsed control already −7.230291. Extra axes recovered only +0.067880 inside a broken/unconverged pipeline. Not evidence that belief-state solving cannot help. [Root 2][root-1-02] |
| e04-belief-solve / bs-b | Transition census and baseline reproduction only; no RVI solve, candidate or Q. [Root 2][root-1-02] |
| e04-price-loss / loss-a | True-price diagnostic +4.316378 (0.025937) over qt1, +3.718987 over COMBO, +8.021774 over HA. Uses compressed tables; not the README's +8.50 row. Loss buckets are descriptive, not causal ceilings. [Root 2][root-1-02] |
| e04-smoothing-b2 / smoothing-b2 | +0.040699 (0.006635) over COMBO, +0.638090 over qt1; first-call error 16.0368%. With true flag, exactly zero gain over ComboFlag. [Root 2][root-1-02] |
| e05-fast-sim / numba-tape; numba-rng | tape delivered no implementation/measurement. rng passed 384/384 baseline parity rows, max 1.19e−11, and 128 head rows, max 1.53e−11. COMBO 12.41 runs/s/core, roughly 20–25× acceleration, below 50/s target. Planned large later head-training line did not run. [Root 2][root-1-02] |
| e05-head-cost / cost8 | Rounded HEAD8 arithmetic added peak 51,564 gas; harness peak 246,963 and two OOG at 245k. Fee fidelity passed at a larger diagnostic cap; deployment feasibility did not. Unchanged G4 engine control n=16 gained +0.507088 (0.175472), not a head result. [Root 2][root-1-02] |
| e06-tell-port / o1-a, o1-b | Public-WAD path/grid classification roughly 0.05–0.06% error; o1-b Bayesian partial-window gain +2.543263 over COMBO, hard-label catastrophic tails. No contract in these measurement items. [Root 2][root-1-02] |
| e06-tell-engine / o2-a, o2-b, o2-c | a/c source-engine replays: 84,954/91,299 callbacks, zero actual-path bit/WAD mismatches; sell discrimination confirmed. b blocked at setup. a/c's no-buy-tell statement tested shared execution only, not upstream sizing grid. [Root 2][root-1-02] |
| e06-side-flag / combo, qt1 | COMBO sell/buy/all flag gains +1.622094/+1.601987/+2.570198 over COMBO. qt1 gains +2.037043/+2.018623/+3.167510 over qt1. Full report; one-side effects are nonadditive. [Root 2][root-1-02] |
| e06-stack / net-head | Guarded NET + rounded HEAD: +0.148967 (0.010412) over COMBO, +0.746358 (0.014554) over qt1; interaction −0.005679 (0.010402), consistent with small near-additive gains on that base. Worst vs COMBO −4.416473 at seed 10632. No tell stack or engine qualification. [Root 2][root-1-02] |
| e07-buy-grid-check / buy-grid | 93,187 source-engine callbacks; zero replay mismatches. First buys: 16,441 arb grid matches, 19/13,128 retail collisions. First sells: 15,100 arb matches, 20/13,338 retail collisions. Budget-4 standalone predicates had no sample fallbacks. [Root 2][root-1-02] |
| e07-tell-tables / visit-refit | On its own BASE: +0.049063 (0.003681), total +3.205537 over qt1. 1,599/4,896 int16 coefficients changed; blob remains 10,167 bytes. Later rq/rp directly measured transfer to LEAN, rather than adding this number to LEAN. [visit-refit][b25-visit-refit] |
| e08-refit-stack / refit | Cancelled without an accepted result; later rq/rp work supplies the composition measurements. |
| e08-lattice-tell / lat-a, lat-b | a: +0.107 (0.013) over tca-path TellPolicy on 512 report seeds; full-table control +0.099, leaving lattice shape +0.008 (0.008). b: +0.123 (0.017) on 320 seeds, without that control. No contract; lattice gas estimates only. [lat-a][b30-lat-a], [Root 3][root-1-03] |
| e09-gap-oracles / go-1, go-2 | True flag adds only about +0.006 to LEAN; true price about +1.18/+1.19. go-1 rival timing is invalid as a ceiling; corrected go-2 post-event rival adds +0.212675. Details below. [go-1][b34-go-1], [go-2][b34-go-2] |
| e09-rival-cut / rc-band | Rival-band cut loses −177.527080 (2.169463) over LEAN on 10000–10511; +40 bps/step was merely least bad among active settings. Reject. [rc-band][b35-rc-band] |
| e09-rival-cut / rc-scale | All live settings lost on choose, best −0.004138 (0.009559). Disabled control selected; exactly zero over LEAN on 10512–11023. [rc-scale][b35-rc-scale] |
| e09-rival-cut / rc-joint | 64-particle rival-only estimate: +0.145192 (0.014521) over LEAN and +3.277454 (0.044521) over qt1 on 11024–11535. Better rival estimate, not improved price estimate. No full 2048 Q or contract; large state/arithmetic requirements. [rc-joint][b35-rc-joint] |
| e09-kappa-tell / kt-high | Choose rejects 2e−5 and 4e−5 versus full 1e−5 by −0.218768/−1.454390. Selected original full 1e−5 tables: +0.111298 (0.011764) over compressed LEAN, +3.269334 over qt1 on 10512–11023. A table-fidelity control, no contract. [kt-high][b36-kt-high] |
| e09-kappa-tell / kt-low | Required unmodified DP solve timed out at 475 s (exit 124); 0 and 5e−6 were not scored. No low-kappa conclusion. [kt-low][b36-kt-low] |

The remaining batches were the contract progression and confirmations, accounted for below and in the Q/E tables: e07-tell-build (3), e08-lean-a (5), e08-lean-b (5), e08-same-label (4), e09-confirm (4), e09-refit-port (3), e09-refit-q (4). The supplied snapshot records **87 allocated items of 200, 81 accepted results and six cancelled-but-still-marked-running entries**, across 36 batches. “Accepted” includes honest blocks, partial results and failed candidates; it does not mean 81 successful policies. The six without accepted output are references, data-a, one probability-table item, one flag-ceiling item, smoothing-a and refit. 113 items remained unspent when the ten-episode limit was reached.

**Taylor-derived contract progression and rejected builds**

| Item | Report / final engine result against qt1 | Final runtime / observed peak gas | Disposition |
|---|---|---|---|
| tca-path | Q +3.133460 (0.022264), n=2048; pilot −1.497195, n=8 | 24,552 B; replay 298,073; 2,579 engine OOG | T/F pass, gas fails; E not run. [tca-path][b23-tca-path] |
| tca-short | Q +3.157779 (0.022523), n=2048; minimum −2.383452 | No contract | Tail condition fails; no Solidity/E. [Root 2][root-1-02] |
| qtr2-path | Q +3.149894 (0.022363), n=2048 | 25,564 B | 988 bytes too large; integrated T/F/G/E incomplete. [Root 2][root-1-02] |
| la-1 | Q +3.159895; final E +3.143933 (0.046044), n=448 | 24,383 B / 232,160 | Passing final sample. Historical n=512 statistic mixes 64 fee-identical earlier-build seeds; excluded here. [la-1][b26-la-1] |
| la-2 | Q +3.159895; final E +3.190869 (0.045594), n=448 | 23,960 B / 239,497 | Passing final sample; superseded 64 seeds peaked at 246,180 and are excluded. [la-2][b26-la-2] |
| la-3 | P only; setup could not execute required binary | No candidate | Blocked; no policy/engine evidence. [Root 2][root-1-02] |
| la-4 | Partial Q n=540; E +3.062, n=64 | 24,108 B / 249,025; one OOG | Fails gas, irrespective of pilot pass. [Root 3][root-1-03] |
| la-5 | Q full; E +3.183 (0.043), n=512 | 24,504 B / **249,087** | Fails task peak cap despite status saying pass and zero E OOG. [Root 3][root-1-03] |
| lb-1 | Q full; final E +3.2627 (0.0619), n=256 | 24,283 B / 232,871 | Final sample passes; earlier E peaked at 245,210, excluded. [Root 3][root-1-03] |
| lb-2 | Q n=512; final E +3.172 (0.117), n=64 | 24,076 B / 244,313 | Very small E sample, 687 gas margin. Failed earlier build excluded. [Root 3][root-1-03] |
| lb-3 | Q n=1024; final E +3.185 (0.044), n=448 | 24,202 B / 240,384 | Partial Q/E; 64 interrupted earlier-build seeds excluded; E initially launched before failed G was read. [lb-3][b27-lb-3] |
| lb-4 / LEAN | Q +3.159909; own E +3.162762 (0.042680), n=512 | 22,946 B / own 224,481; later 225,355 | Preferred base by complete evidence and gas/size margin; four independent confirmations above. [lb-4][b27-lb-4] |
| lb-5 | Q n=1280; final E +3.217 (0.060), n=352 | 24,574 B / 240,264 | Only two bytes of size margin; mixed earlier gas-only revisions excluded. [Root 3][root-1-03] |
| sl-1 | Inherits tca-path Q; label check passes | 26,016 B | Deployment refused for size; integrated F/E absent. [Root 3][root-1-03] |
| sl-2 | Inherits tca-path Q; E +3.128 (0.058), n=256 | 24,479 B / 232,387 | Second E window missing. [Root 3][root-1-03] |
| sl-3 | Inherits tca-path Q; E +3.0981 (0.0423), n=512 | 24,521 B / 227,577 | Passing same-label rewrite; little byte margin. [sl-3][b28-sl-3] |
| sl-4 | Inherits tca-path Q; final secondary E +3.2053 (0.0664), n=256 | 24,572 B / final-source 242,332 | Four bytes of margin; primary E incomplete/superseded. [Root 3][root-1-03] |
| rp-1 / rp-2 / rp-3 | R: full Q assembled by rq; each E n=256, pooled +3.161202 | Same 22,953 B source; pooled peak 222,787 | Measured numeric checks pass; R's original 1024-pair E quota remains incomplete. |

No performance-ranking inference is made from, for example, lb-1's +3.263 versus R's +3.161: different engine seeds and samples can move the means. The direct same-seed R−LEAN result is the relevant evidence for that upgrade. Likewise, fee-equality tests on a superseded implementation do not turn its gas observations into final-build observations.

**Taylor-derived remaining gap to #1**

The latest supplied board observation is requester note 2: qt1 **524.9403**, then ninth, leader **528.415**, a gap of **3.4747 board points**; fifth was **528.099**. These are historical requester observations, not a live ranking check. Adding R's local engine mean to qt1 would give 528.1015, still 0.3135 below that historical leader, but **that addition is only illustrative arithmetic**. The requester's roughly 0.97 replica/board ratio is also a planning heuristic, not a calibrated score conversion. Neither justifies claiming a new rank. The remaining research target is approximately **+0.3 to +0.4 beyond the delivered result**, subject to the board's actual scoring.

The useful late measurements are:

| LEAN intervention | go-1: 64000–64511, n=512, gain (SE) | go-2: 64512–65023, n=512, gain (SE) | Meaning |
|---|---:|---:|---|
| A1: true first-own trade flag | +0.006648 (0.005648) | +0.005805 (0.006060) | Little remaining value in perfecting this call on this base |
| A2: supplied true rival state | −7.512657 (0.083105) | **+0.212675 (0.018003)** | go-1 used pre-rival-leg state; go-2 aligns post-event state, the relevant diagnostic |
| A3: A2 plus rival-band cut | −8.657714 (0.088785) | −0.627194 (0.027765) | Particular projection is harmful; not an upper bound on all uses of bounds |
| A4: true own price | **+1.183373 (0.029621)** | **+1.193111 (0.030145)** | Large information headroom, not an observable policy |
| A5: true price plus rival | −5.278717 (0.070987) | +1.531476 (0.031897) | Corrected rival adds +0.338365 beyond true price in go-2 |

Sources: [go-1][b34-go-1], [go-2][b34-go-2]. go-1's A2/A3/A5 cannot bound rival-estimation value because their information is timed incorrectly; A3 also has one-ULP boundary sensitivity. go-2 repaired a per-callback rather than per-step band update and invalidated its first partial run before its complete corrected block. It discloses that the strict global once-only condition was not met. None of these hidden-truth arms is eligible for deployment.

The price-oracle gain is not all predictable. Its advantage includes quotes already in force when the next arbitrage trade arrives; the next price innovation is unavailable to a causal policy. Pin-age and phase decompositions are descriptive comparisons of diverging trajectories, not guaranteed recoverable components. The loss-a claim that fixing classification buys “at most a quarter” is inconsistent with the separately measured flag interventions and is not retained as a causal bound.

Three concrete directions remain, with clear limits:

1. **Compress a better rival estimate.** `rival64` obtains +0.145192 over LEAN on 512 report seeds, using only permitted observables; the corrected true-rival diagnostic suggests value of about +0.21 on its own separate block. But 64 particles require 192 state values, roughly 64 packed slots before other state, versus the challenge base's 32 slots. The worker did not compile or measure this implementation. A few-point or analytic substitute is a plausible next experiment, not a demonstrated gas-feasible improvement. Taking the particle price moments instead hurt choose return (price32 −0.082718). [rc-joint][b35-rc-joint], [go-2][b34-go-2], [pinned base interface](https://raw.githubusercontent.com/benedictbrady/amm-challenge/6b6921f8d463314aa7c96234e1be25a25245f704/contracts/src/AMMStrategyBase.sol).
2. **Recover more table fidelity at fixed code cost.** Full original 1e−5 lookup gains +0.111298 over LEAN on 10512–11023. R gains +0.041670 over LEAN on those same seeds, so their reported mean difference is about **+0.069628 in favor of full tables**; no paired SE for full-versus-R or compiled full-table contract was supplied. Refit-on-LEAN visits or improved knots/compression could investigate that gap. It is not a global +0.07 ceiling, and cannot simply be added to the rival gain. [kt-high][b36-kt-high], [rq-2][b33-rq-2].
3. **Improve causal price/posterior quoting between observations.** The +1.19 true-price diagnostic motivates the question but does not solve it. Earlier full-posterior work helped COMBO; after the tell, lattice shape alone added only +0.008 (SE 0.008), and fine-grid-over-full-coarse gains under the flag were similarly small. A profitable compact residual or posterior correction needs a new paired experiment on R, not addition of older COMBO gains. The measured 51.5k head overhead exceeds R's observed 22.2k gas headroom; optimizing a different head remains unmeasured. [lat-a][b30-lat-a], [Root 1][root-1-01], [Root 2][root-1-02].

No measured combination closes the remaining gap inside both limits. More aggressive information weights, the implemented rival-band cut and run-scale adaptation did not do so. Completing the missing R engine quota would strengthen confidence in the delivered policy, but would not by itself improve its score. Any future candidate should be frozen on choose seeds, evaluated on the full stated report window with its exact base, pass T/F/size/gas, then use genuinely fresh engine seeds before any separately authorized leaderboard submission.

**Taylor-derived provenance, reconstruction and checks**

This write-up checked all **30 supplied result files** against the task's SHA-256 values. It decoded selected archives in memory, checked their compressed/archive manifests and listed source hashes, verified byte identity of the three R sources, and verified that R and LEAN differ only in **242 coefficient-assignment lines out of 720**. No input file was modified or treated as an instruction. The 1,599 changed coefficients leave the 375-byte QMS1 header/knots and total 10,167-byte layout unchanged. The source's decoded R blob was compared to visit-refit's delivered bytes. The Markdown source fences were checked byte-for-byte against those bundle files.

For statistics, this write-up rejoined the four rq report blocks and checked exact seed coverage; recomputed means, sample SEs, negative counts and worst-five tails; and recomputed rp/cf/LEAN pools from disjoint block sufficient statistics, cross-checking available per-seed rows. For summary-only blocks, pooling uses `N=sum(n_i)`, `m=sum(n_i*m_i)/N`, and `SE²=sum((n_i−1)*n_i*SE_i²+n_i*(m_i−m)²)/(N*(N−1))`. It does not average SEs or count duplicate replica runs as fresh observations. These checks verify consistency of supplied evidence, not independent truth of the simulations.

Some early root inputs have explicit source-recheck flags, including data-b, filter-only, all-observables, combo-strata, finer-a, posterior-a, information-a/b, res-c/d, cost8, o1-a/b, o2-a/c, net-head, buy-grid, la-3, lat-b and kt-low. The root registers document them. Their direct numerical records are retained as attributed worker reports; their unverified source citations are not independent corroboration. The final lb-4/rq/rp/cf chain has raw handed results and later validation, rather than resting only on those early source assertions.

Where merge prose conflicts with raw results, this report uses the raw results. In particular, Root 4's closing statement that none of its policies exceeds +0.5 over qt1 is incorrect: `rival64` and full-table LEAN both exceed that numerical eligibility threshold on their partial report blocks; what they lack is full-window/contract qualification. Root 4 also says joint and full-table results use the same report block; joint actually uses **11024–11535**, full-table **10512–11023**. Root 3's claim that paired means are unaffected by platform math is too strong: lat-a measured single-seed sensitivity to one-ULP changes, and no universal invariance was proved. These corrections prevent promoting a merge sentence above its underlying evidence.

The archived reconstruction chain is [tca-path][b23-tca-path] → [lb-4][b27-lb-4] → [rp-3][b32-rp-3]. tca-path's `source_bundle.data` is base85(tar.xz), compressed SHA-256 `546b440855726c3cd2231e4879e0002dda182dc609ee9c5155c04e4790ca6fdb`. lb-4's `bundle.data` is base64(tar.xz), compressed SHA-256 `f368c459fec21abaa30e179ffbf03cfbe1c7b194f1ad8b07de3637892d06e9f1`. rp-3's `bundle.data` is base64(tar.xz), compressed SHA-256 `e5ec0bd4106e11191751a1cdd042865b6514c94d2dab884fb2008bba08a212ff`. Overlay only their ordinary relative-path files in a fresh task checkout, checking the manifests; do not execute arbitrary result text. lb-4 removes `scratch/ref/tca_tell.py`, `scratch/TellCore.sol`, `scratch/test_tell.py` and `scratch/test_policy.py`. Its `materialize.py` restores the old blob; rp-3's `materialize_r.py` restores R's blob from StrategyR. Keep LEAN and R reference blobs separate when pairing.

For the delivered contract alone, the three complete source fences below are sufficient source inputs to solc. Save their contents exactly, with their final LF, as `Strategy.sol`, `AMMStrategyBase.sol` and `IAMMStrategy.sol`; use the compiler settings above and standard-JSON source key `Strategy.sol`. Registering the same contents under `StrategyR.sol` instead changes metadata and thus the bytecode hash. The two imports are also pinned at [AMMStrategyBase.sol](https://raw.githubusercontent.com/benedictbrady/amm-challenge/6b6921f8d463314aa7c96234e1be25a25245f704/contracts/src/AMMStrategyBase.sol) and [IAMMStrategy.sol](https://raw.githubusercontent.com/benedictbrady/amm-challenge/6b6921f8d463314aa7c96234e1be25a25245f704/contracts/src/IAMMStrategy.sol); their exact archived bytes are included, not placeholders.

The engine/reproduction tools are in the content-addressed bundles, not a separately shipped runnable checkout. Reproduction of P/Q/T/F/E requires those Python sources, the pinned challenge checkout and the prescribed setup/dependencies. This Markdown does not contain the wheel, compiler, every training dataset or every trace, and is not an offline environment installation. The build settings above intentionally match the tested challenge compiler, rather than a new Foundry configuration. No setup, new contract build, engine run, publication or submission was performed in this bounded write-up task.

Credit also belongs to qt1's authors; TC-A seat #770; o1-a #541 and o1-b #1497; tca-path #1351; buy-grid #781; visit-refit #307; lb-4 #39; la-1 #330, la-2 #1631, lb-1 #1269, sl-3 #475 and sl-4 #1137; the other builders and research items recorded above; and the independent cf, rq and rp contributors. Taylor's attribution remains in the original contract header. The administrative handoff provides truncated 501-character batch-brief previews, not full original briefs or decisions files; this final report does not certify their complete schema/content from those previews. This task names only `artifacts/goal/writeup/report.md`, so no new orchestration decisions file is created.

**Taylor-derived source register: verified supplied artifacts**

The public links below identify the exact supplied bytes; SHA-256 verification here used the local handed copies. Earlier results not individually handed here are cited through the four root registers.

| Input / result | Bytes | SHA-256 |
|---|---:|---|
| [root-1-01][root-1-01] — root merge 1-01 | 62,779 | `3aa4e810dcdc7455a4bb38f1af1c11679350a85df2efd4c6d104c9bc47831b59` |
| [root-1-02][root-1-02] — root merge 1-02 | 60,107 | `062fde000000f45785411117d59eef4ba2fd93112d352b49bf2ec7edbada616d` |
| [root-1-03][root-1-03] — root merge 1-03 | 24,834 | `53483618a1e01cef60f6c48d36566f2a97887b45056d0ef428a8f006c536ede8` |
| [root-1-04][root-1-04] — root merge 1-04 | 12,986 | `7fd7a37171ce6c3205aeae12b7dbcd46ad39fc522009eb821e63cae2229f358d` |
| [b32-rp-1][b32-rp-1] — e09-refit-port/rp-1 | 50,894 | `cd212d2fca2f1d860bc3e2c45b19878e95e0ac36c9d96b53c7378d648282741c` |
| [b32-rp-2][b32-rp-2] — e09-refit-port/rp-2 | 50,158 | `bc2db6dbb85b1da53dcaddf8dc478f65d599ff79a65dd43f30ff3417cd8fbf76` |
| [b32-rp-3][b32-rp-3] — e09-refit-port/rp-3 | 57,307 | `31c415ffbbcdc36d91a30d4f4a8817406d3ab96b34df29d08ac28ad3e41432ba` |
| [b27-lb-4][b27-lb-4] — e08-lean-b/lb-4 | 53,722 | `93cc15561f172c49c8bce174143333ede904fdbfcf51276cbbeb514d4f5b614e` |
| [b31-cf-1][b31-cf-1] — e09-confirm/cf-1 | 56,028 | `94b493f4b4cf6b4ee6857b026f5845b9b5d5ba4fff9fc3a3d0c0cf7004269234` |
| [b31-cf-2][b31-cf-2] — e09-confirm/cf-2 | 60,850 | `8f87928cd398da5670bad08415db61fdca223a074816814dd0a55eee2ba23f0a` |
| [b31-cf-3][b31-cf-3] — e09-confirm/cf-3 | 27,113 | `255b2dd284d90672c1a22b0dcb70a74d7cf49bd0528faa9cf0ab0be77a49631a` |
| [b31-cf-4][b31-cf-4] — e09-confirm/cf-4 | 61,036 | `3a027cd578b8c4a9bc4c1eda72d8f4e019600b1897134ee196f3d14346e9cf66` |
| [b33-rq-1][b33-rq-1] — e09-refit-q/rq-1 | 28,273 | `92038c6919b4a84c228543015b4a585bcd8b0b0646efca5ca6351081d258357b` |
| [b33-rq-2][b33-rq-2] — e09-refit-q/rq-2 | 43,578 | `9d0badbdcdb3322b933255cfcb4d9f401a8dbe1a602ece691d0c2dc5077fbb50` |
| [b33-rq-3][b33-rq-3] — e09-refit-q/rq-3 | 42,082 | `df13d6faec27afa3cf5c22067878e3b577c03c4a04590a76980b1729fac1f500` |
| [b33-rq-4][b33-rq-4] — e09-refit-q/rq-4 | 38,633 | `2c2f1209c46a7e9775cca9c82d9dc4a975aac81a8f1526616ec39d13682aa444` |
| [b25-visit-refit][b25-visit-refit] — e07-tell-tables/visit-refit | 54,017 | `5893446c82f8bc1473468bba6b156ec2a96ce3df5ddfc897c05c63cf545e1162` |
| [b23-tca-path][b23-tca-path] — e07-tell-build/tca-path | 63,997 | `dc359635b5851de9f5b3ecf81dc2107d46acd5dbe67e0be234bcfbe0c8a488e7` |
| [b34-go-1][b34-go-1] — e09-gap-oracles/go-1 | 63,060 | `89aeb3a86be7d43f7ac3003050a7316ffe5d2eae4dc1017d9164e8c9c69e8cf7` |
| [b34-go-2][b34-go-2] — e09-gap-oracles/go-2 | 62,283 | `3dc2d521ec738b3659160a4b5ce04b04022a7ba85d9937fbfaafb544cc9d7a2f` |
| [b35-rc-joint][b35-rc-joint] — e09-rival-cut/rc-joint | 31,477 | `19bf5534225de5b3d201baaf0e35f9f2a8671120380295ea7726bf6379caedc1` |
| [b35-rc-band][b35-rc-band] — e09-rival-cut/rc-band | 63,934 | `91b47b26b5d927fd438ee899888651ecb2332488e51b21142b5d70f21021b78e` |
| [b35-rc-scale][b35-rc-scale] — e09-rival-cut/rc-scale | 60,956 | `a896b880fdbdd179e5b8a2944e795cca49b258f8f9dfca354471df4e32ca1f0e` |
| [b36-kt-high][b36-kt-high] — e09-kappa-tell/kt-high | 14,078 | `4a41a90c67cf9add7e0c4f382e60c411bbf8ed340874aead14be76f4d09951f7` |
| [b36-kt-low][b36-kt-low] — e09-kappa-tell/kt-low | 7,456 | `0eba8c0b9ea0ae453dede3025d640f64f8f5a1dc51335d25404e2a05ce487dcb` |
| [b26-la-1][b26-la-1] — e08-lean-a/la-1 | 60,786 | `1f399ab09bf68c0f88d9849a12eafd611176253dd98a27c05057f8df58e817ed` |
| [b26-la-2][b26-la-2] — e08-lean-a/la-2 | 63,662 | `b27ba5d1ec7d2a8ffb80fd39c02b63fa1e282fcb793906fe5f81861de5749f3c` |
| [b28-sl-3][b28-sl-3] — e08-same-label/sl-3 | 45,906 | `2e4efd13173e9747efbce3887c4bad0205ca2db4c92a127208f2e6b4a68a0b75` |
| [b27-lb-3][b27-lb-3] — e08-lean-b/lb-3 | 63,830 | `1fb0fbe958600ac4f836dcf2a7c45904b1209f7620176917a461ec73aa423b94` |
| [b30-lat-a][b30-lat-a] — e08-lattice-tell/lat-a | 61,945 | `b256af971792a884c3b1c39051d7516660f05e10c69c1bcaa9ff6d2483cb315a` |

[root-1-01]: https://api.imd.fun/artifacts/3aa4e810dcdc7455a4bb38f1af1c11679350a85df2efd4c6d104c9bc47831b59
[root-1-02]: https://api.imd.fun/artifacts/062fde000000f45785411117d59eef4ba2fd93112d352b49bf2ec7edbada616d
[root-1-03]: https://api.imd.fun/artifacts/53483618a1e01cef60f6c48d36566f2a97887b45056d0ef428a8f006c536ede8
[root-1-04]: https://api.imd.fun/artifacts/7fd7a37171ce6c3205aeae12b7dbcd46ad39fc522009eb821e63cae2229f358d
[b32-rp-1]: https://api.imd.fun/artifacts/cd212d2fca2f1d860bc3e2c45b19878e95e0ac36c9d96b53c7378d648282741c
[b32-rp-2]: https://api.imd.fun/artifacts/bc2db6dbb85b1da53dcaddf8dc478f65d599ff79a65dd43f30ff3417cd8fbf76
[b32-rp-3]: https://api.imd.fun/artifacts/31c415ffbbcdc36d91a30d4f4a8817406d3ab96b34df29d08ac28ad3e41432ba
[b27-lb-4]: https://api.imd.fun/artifacts/93cc15561f172c49c8bce174143333ede904fdbfcf51276cbbeb514d4f5b614e
[b31-cf-1]: https://api.imd.fun/artifacts/94b493f4b4cf6b4ee6857b026f5845b9b5d5ba4fff9fc3a3d0c0cf7004269234
[b31-cf-2]: https://api.imd.fun/artifacts/8f87928cd398da5670bad08415db61fdca223a074816814dd0a55eee2ba23f0a
[b31-cf-3]: https://api.imd.fun/artifacts/255b2dd284d90672c1a22b0dcb70a74d7cf49bd0528faa9cf0ab0be77a49631a
[b31-cf-4]: https://api.imd.fun/artifacts/3a027cd578b8c4a9bc4c1eda72d8f4e019600b1897134ee196f3d14346e9cf66
[b33-rq-1]: https://api.imd.fun/artifacts/92038c6919b4a84c228543015b4a585bcd8b0b0646efca5ca6351081d258357b
[b33-rq-2]: https://api.imd.fun/artifacts/9d0badbdcdb3322b933255cfcb4d9f401a8dbe1a602ece691d0c2dc5077fbb50
[b33-rq-3]: https://api.imd.fun/artifacts/df13d6faec27afa3cf5c22067878e3b577c03c4a04590a76980b1729fac1f500
[b33-rq-4]: https://api.imd.fun/artifacts/2c2f1209c46a7e9775cca9c82d9dc4a975aac81a8f1526616ec39d13682aa444
[b25-visit-refit]: https://api.imd.fun/artifacts/5893446c82f8bc1473468bba6b156ec2a96ce3df5ddfc897c05c63cf545e1162
[b23-tca-path]: https://api.imd.fun/artifacts/dc359635b5851de9f5b3ecf81dc2107d46acd5dbe67e0be234bcfbe0c8a488e7
[b34-go-1]: https://api.imd.fun/artifacts/89aeb3a86be7d43f7ac3003050a7316ffe5d2eae4dc1017d9164e8c9c69e8cf7
[b34-go-2]: https://api.imd.fun/artifacts/3dc2d521ec738b3659160a4b5ce04b04022a7ba85d9937fbfaafb544cc9d7a2f
[b35-rc-joint]: https://api.imd.fun/artifacts/19bf5534225de5b3d201baaf0e35f9f2a8671120380295ea7726bf6379caedc1
[b35-rc-band]: https://api.imd.fun/artifacts/91b47b26b5d927fd438ee899888651ecb2332488e51b21142b5d70f21021b78e
[b35-rc-scale]: https://api.imd.fun/artifacts/a896b880fdbdd179e5b8a2944e795cca49b258f8f9dfca354471df4e32ca1f0e
[b36-kt-high]: https://api.imd.fun/artifacts/4a41a90c67cf9add7e0c4f382e60c411bbf8ed340874aead14be76f4d09951f7
[b36-kt-low]: https://api.imd.fun/artifacts/0eba8c0b9ea0ae453dede3025d640f64f8f5a1dc51335d25404e2a05ce487dcb
[b26-la-1]: https://api.imd.fun/artifacts/1f399ab09bf68c0f88d9849a12eafd611176253dd98a27c05057f8df58e817ed
[b26-la-2]: https://api.imd.fun/artifacts/b27ba5d1ec7d2a8ffb80fd39c02b63fa1e282fcb793906fe5f81861de5749f3c
[b28-sl-3]: https://api.imd.fun/artifacts/2e4efd13173e9747efbce3887c4bad0205ca2db4c92a127208f2e6b4a68a0b75
[b27-lb-3]: https://api.imd.fun/artifacts/1fb0fbe958600ac4f836dcf2a7c45904b1209f7620176917a461ec73aa423b94
[b30-lat-a]: https://api.imd.fun/artifacts/b256af971792a884c3b1c39051d7516660f05e10c69c1bcaa9ff6d2483cb315a


<a id="strategy-source"></a>

**Taylor-derived complete Strategy.sol: exact tested R source**

The following code is copied byte-for-byte from all three rp bundles, including its original credit and the stale metadata comments disclosed above. It is not an excerpt or a patch.

File `Strategy.sol` — 49,905 bytes; SHA-256 `c54d8d48d4a62ac655024ffa8b0e808e45d9809c9612fb614895aab10aee3491`.

<!-- file: Strategy.sol -->
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import {AMMStrategyBase} from "./AMMStrategyBase.sol";
import {TradeInfo} from "./IAMMStrategy.sol";
// Two-component posterior port (TC-A #770) + LEAN TELL (lb-4); credit Taylor (gtmcknight) for policy, filter, tables and replica.
// Policy: Taylor's (gtmcknight) solved game, amm-sim 4812a638, research/solved: Gaussian filter (real.py) + qm tables
// (qm_k1e-5.json, +3.77 vs HA on Taylor's replica). Filter, state and timing from trim-1 / port-3.
// Fees: real.py RealPolicy.lookup over the qm-spline decoded tables (QMS1 blob sha256 3ac7cb88..., 10,167 B):
// per table one 3-D cubic B-spline (row, column, sd level), clamped knots, coefficients int16 in 1/8 bps.
// The contract evaluates the spline at the 8 surrounding grid nodes (2 rows x 2 columns x 2 sd levels) with
// Cox-de Boor bases computed at runtime, clamps each node fee at 0, then interpolates bilinearly and linearly in sd
// exactly as real.py reads the decoded JSON. Bid side = point mirror of the ask surface (row 320-i, column last-j).
// Coefficient words are PUSH32 immediates written to memory: 4 lanes x 64 bits per word, lane = 4 int16 sd coefficients.
// Gas trim: scalar node sums, shared mirrored knot geometry, and four packed state words.
// Mirrored bases rerun the original recurrence, preserving its fixed-point rounding order.
// Knot words: interior knots as uint16 in 1/64 grid units (W[0..1] rows, W[2] columns).
// Taylor source: https://github.com/gtmcknight/amm-sim/tree/4812a6382311624e1506aca131ca35c378f930d9/research/solved
// Credit Taylor (gtmcknight): replica, Gaussian filter, qm tables (github.com/gtmcknight/amm-sim
// @4812a6382311624e1506aca131ca35c378f930d9, research/solved); seats qt1, TC-A #770, o1-a #541,
// o1-b #1497, tca-path, buy-grid.
// LEAN TELL = buy-grid's bounded sell_one_division / buy_grid tests, budget 4, in exact integer
// binary64 (round-to-nearest-even) arithmetic. A double is m*2^e with 2^52 <= m <= 2^53; 1e18 = LT_C*2^7.
// Returns 0 unsupported, 1 positive, 2 negative, 3 over budget. Mirrors scratch/ref/lean_tell.py bit for bit.
abstract contract LeanTell {
    uint256 constant LT_C=7812500000000000;
    function ltMsb(uint256 x) internal pure returns(uint256 r){unchecked{
        if(x>>128!=0){x>>=128;r=128;}if(x>>64!=0){x>>=64;r+=64;}if(x>>32!=0){x>>=32;r+=32;}if(x>>16!=0){x>>=16;r+=16;}
        if(x>>8!=0){x>>=8;r+=8;}if(x>>4!=0){x>>=4;r+=4;}if(x>>2!=0){x>>=2;r+=2;}if(x>>1!=0)r++;
    }}
    // n / 2^s to nearest, ties to even; s >= 1.
    function ltRound(uint256 n,uint256 s) internal pure returns(uint256 q){unchecked{
        q=n>>s;uint256 rem=n&((uint256(1)<<s)-1);uint256 half=uint256(1)<<(s-1);
        if(rem>half||(rem==half&&(q&1)!=0))q++;
    }}
    // Wad::from_f64 of the double m*2^e: trunc(RN(m*2^e * 1e18)).
    function ltWad(uint256 m,int256 e) internal pure returns(uint256){unchecked{
        uint256 n=m*LT_C;uint256 s=n>>105!=0?53:52;uint256 p=ltRound(n,s);int256 t=e+7+int256(s);
        if(t>=0)return t>128?type(uint256).max:p<<uint256(t);
        return t<-64?0:p>>uint256(-t);
    }}
    // Wad of RN(d*2^e / g), g = G*2^-53, 0 < d < 2^53 exact.
    function ltDivWad(uint256 d,int256 e,uint256 G) internal pure returns(uint256){unchecked{
        uint256 n=(d<<110)/G;if(n*G!=d<<110)n|=1;
        uint256 s=ltMsb(n)-52;return ltWad(ltRound(n,s),e+int256(s)-57);
    }}
    // G = 2^53 * RN(1 - RN(RN(fee)/1e18)), fee <= 1e17.
    function ltGamma(uint256 f) internal pure returns(uint256){unchecked{
        if(f==0)return 1<<53;
        uint256 sf=ltMsb(f);
        if(sf>52){sf-=52;f=ltRound(f,sf);}else sf=0;
        uint256 n=(f<<110)/LT_C;if(n*LT_C!=f<<110)n|=1;
        uint256 s=ltMsb(n)-52;uint256 r=64-s-sf;
        return ltRound((uint256(1)<<(53+r))-ltRound(n,s),r);
    }}
    // Every double whose wad is w (2^60 <= w < 2^120): mantissas a, b (0 = absent), exponent e.
    function ltPre(uint256 w) internal pure returns(uint256 a,uint256 b,int256 e){unchecked{
        uint256 n=(w<<64)/1e18;uint256 h=ltMsb(n);uint256 m=n>>(h-52);e=int256(h)-116;
        if(ltWad(m,e)==w)a=m;
        if(ltWad(m+1,e)==w)b=m+1;
    }}
    // Virtual reserves xv = (m+k)*2^e > rx whose amount wad is ax.
    function ltGrid(uint256 m,int256 e,uint256 k0,uint256 G,uint256 ax) internal pure returns(uint256 hits){unchecked{
        if(m==0)return 0;
        uint256 lo=k0;uint256 hi=k0+1;if(k0>>48!=0){lo--;hi++;}
        if(lo==0)lo=1;
        for(uint256 k=lo;k<=hi;k++){
            uint256 t=m+k;if(t>>53!=0&&(t&1)!=0)continue;
            if(ltDivWad(k,e,G)==ax)hits++;
        }
    }}
    // px, py: previous callback's reserve wads; fee: the fee wad returned then for this side
    // (bid when the pool buys X); ax, ay, cy: this trade's amountX, amountY, reserveY.
    function ltTell(uint256 px,uint256 py,uint256 fee,uint256 ax,uint256 ay,uint256 cy,bool buy) internal pure returns(uint256){unchecked{
        if(fee>1e17)return 0;
        uint256 G=ltGamma(fee);
        if(buy){
            if(px>>60==0||px>>120!=0||ax==0||ax>px>>1)return 0;
            (uint256 a,uint256 b,int256 e)=ltPre(px);
            if((a|b)==0)return 0;
            uint256 k0=ax*G/(uint256(1e18)<<uint256(e+53));
            uint256 hits=ltGrid(a,e,k0,G,ax)+ltGrid(b,e,k0,G,ax);
            if((a!=0?1:0)+(b!=0?1:0)+hits>4)return 3;
            return hits!=0?1:2;
        }
        if(py>>60==0||py>>120!=0||cy>>60==0||cy>>120!=0||ay==0||ay>>120!=0)return 0;
        (uint256 y0,uint256 y1,int256 ey)=ltPre(py);(uint256 z0,uint256 z1,int256 ez)=ltPre(cy);
        if((y0|y1)==0||(z0|z1)==0)return 0;
        int256 de=ez-ey;if(de>1||de<-1)return 0;
        if(de==1){z0<<=1;z1<<=1;}else if(de==-1){y0<<=1;y1<<=1;ey=ez;}
        for(uint256 i=0;i<4;i++){
            uint256 y=i<2?y0:y1;uint256 z=(i&1)==0?z0:z1;
            if(y==0||z<=y)continue;
            z-=y;if(z>>53!=0)return 0;
            if(ltDivWad(z,ey,G)==ay)return 1;
        }
        return 2;
    }}
}

contract Strategy is AMMStrategyBase, LeanTell {
    int256 constant U=1e18;
    int256 constant LN2=693147180559945309;
    struct Belief { int256 m; int256 v; int256 fb; int256 fa; int256 sp; int256 r; uint256 t; uint256 cnt; bool sy; int256 pi; int256 lp; int256 mt; int256 vt; }
    function getName() external pure override returns(string memory) { unchecked {return "TaylorTCALeanTell";} }
    function mul(int256 a,int256 b) internal pure returns(int256){ unchecked {return a*b/U;} }
    function divi(int256 a,int256 b) internal pure returns(int256){ unchecked {return a*U/b;} }
    function ab(int256 x) internal pure returns(int256){ unchecked {return x<0?-x:x;} }
    function clip(int256 x,int256 a,int256 b) internal pure returns(int256){ unchecked {return x<a?a:(x>b?b:x);} }
    function ln(int256 x) internal pure returns(int256 z){ unchecked {
        require(x>0); int256 k;
        while(x< U){x*=2;k--;}
        while(x>=2*U){x/=2;k++;}
        // Reduce to [1/sqrt(2),sqrt(2)]; |y| <= 0.171573.
        if(x>1414213562373095048){x/=2;k++;}
        int256 y=divi(x-U,x+U); int256 y2=mul(y,y); int256 q=y; z=y;
        q=mul(q,y2);z+=q/3;
        q=mul(q,y2);z+=q/5;
        q=mul(q,y2);z+=q/7;
        q=mul(q,y2);z+=q/9;
        q=mul(q,y2);z+=q/11;
        q=mul(q,y2);z+=q/13;
        q=mul(q,y2);z+=q/15;
        q=mul(q,y2);z+=q/17;
        q=mul(q,y2);z+=q/19;
        return 2*z+k*LN2;
    } }
    function exp(int256 x) internal pure returns(int256){ unchecked {
        if(x< -42*U)return 0; require(x<60*U);
        int256 k=(x>=0?x+LN2/2:x-LN2/2)/LN2; int256 r=x-k*LN2;
        int256 r2=mul(r,r);
        int256 even=665280*U+mul(r2,75600*U+mul(r2,840*U+r2));
        int256 odd=mul(r,332640*U+mul(r2,10080*U+mul(r2,42*U)));
        int256 s=divi(even+odd,even-odd);
        return k>=0?s*int256(uint256(1)<<uint256(k)):s/int256(uint256(1)<<uint256(-k));
    } }
    function root(int256 x) internal pure returns(int256){ unchecked {
        if(x<=0)return 0; uint256 n=uint256(x)*1e18;uint256 r=uint256(1)<<(ltMsb(n)/2);
        for(uint256 i=0;i<7;i++)r=(r+n/r)/2;
        return int256(r<n/r?r:n/r);
    } }
    function pdf(int256 x) internal pure returns(int256){ unchecked {if(ab(x)>10*U)return 0;return divi(exp(-mul(x,x)/2),2506628274631000200);} }
    // Hart rational normal tail approximation; erf(x)=2*Phi(x*sqrt(2))-1.
    function cdf(int256 x,int256 density) internal pure returns(int256){ unchecked {
        int256 y=ab(x);if(y>8*U)return x>0?U:int256(0);
        int256 n=35262496599891000;
        n=mul(n,y)+700383064443688000;n=mul(n,y)+6373962203531650000;
        n=mul(n,y)+33912866078383000000;n=mul(n,y)+112079291497871000000;
        n=mul(n,y)+221213596169931000000;n=mul(n,y)+220206867912376000000;
        int256 d=88388347648318400;
        d=mul(d,y)+1755667163182640000;d=mul(d,y)+16064177579207000000;
        d=mul(d,y)+86780732202946100000;d=mul(d,y)+296564248779674000000;
        d=mul(d,y)+637333633378831000000;d=mul(d,y)+793826512519948000000;
        d=mul(d,y)+440413735824752000000;
        int256 tail=(density*2506628274631000200/U)*n/d;return x>0?U-tail:tail;
    } }
    function trunc(int256 m,int256 v,int256 lo,int256 hi) internal pure returns(int256,int256,int256){
        return truncSD(m,v,lo,hi,root(v));
    }
    function truncSD(int256 m,int256 v,int256 lo,int256 hi,int256 sd) internal pure returns(int256 Z,int256 mt,int256 vt){ unchecked {
        if(v<=0)return (lo<=m&&m<=hi?U:int256(0),m,0);
        int256 a=divi(lo-m,sd);int256 b=divi(hi-m,sd);
        int256 pa=pdf(a);int256 pb=pdf(b);
        Z=cdf(b,pb)-cdf(a,pa);
        if(Z<1e6)return(Z,m<lo?lo:hi,v/4);
        int256 r=divi(pa-pb,Z);
        mt=m+mul(sd,r);vt=mul(v,U+divi(mul(a,pa)-mul(b,pb),Z)-mul(r,r));if(vt<0)vt=0;
    } }
    uint256 constant K64=15625000000000000; // U/64: knots are stored in 1/64 grid units
    uint256 constant SL=0x221a14100c080400;    // S levels 0,4,8,12,16,20,26,34 bps, byte k
    uint256 constant W2=0xa08264503c32281e1914110e0c0b0a090807060504030201;  // |W2L[i]| for i<24 (grid units), byte 23-i
    function S(uint256 k) internal pure returns(int256){ unchecked {return int256((SL>>(8*k))&0xff)*U;} }
    function w2l(uint256 idx) internal pure returns(int256){ unchecked {
        if(idx==24)return 0; bool neg=idx<24; if(!neg)idx=48-idx;
        int256 v=int256((W2>>(8*(23-idx)))&0xff)*U; return neg?-v:v;
    } }
    function pos2(int256 l2) internal pure returns(int256){ unchecked {
        if(l2<= -160*U)return 0; if(l2>=160*U)return 48*U;
        uint256 lo;uint256 hi=48;
        while(hi-lo>1){uint256 mid=(lo+hi)>>1;if(w2l(mid)<=l2)lo=mid;else hi=mid;}
        int256 wl=w2l(lo);return int256(lo)*U+(l2-wl)*U/(w2l(hi)-wl);
    } }
    function kn(uint256 w0,uint256 w1,uint256 ni,int256 lastU,uint256 idx) internal pure returns(int256){ unchecked {
        if(idx<4)return 0;if(idx>=4+ni)return lastU;idx-=4;
        return int256(((idx<16?w0:w1)>>((idx&15)<<4))&0xffff)*int256(K64);
    } }
    // Clamped cubic B-spline at integer x: span m (coefficients m-3..m) and the 4 nonzero bases N (WAD), Cox-de Boor.
    function basis(uint256[87] memory W,uint256 base,uint256 ni,uint256 last,uint256 x,int256[4] memory N) internal pure returns(uint256 m){ unchecked {
        int256 xu=int256(x)*U;int256 lastU=int256(last)*U;uint256 w0=W[base];uint256 w1=W[base+1];
        uint256 q;
        while(q<ni&&int256(((q<16?w0:w1)>>((q&15)<<4))&0xffff)*int256(K64)<=xu)q++;
        m=3+q;
        int256 l1=xu-kn(w0,w1,ni,lastU,m);int256 r1=kn(w0,w1,ni,lastU,m+1)-xu;
        int256 l2=xu-kn(w0,w1,ni,lastU,m-1);int256 r2=kn(w0,w1,ni,lastU,m+2)-xu;
        int256 l3=xu-kn(w0,w1,ni,lastU,m-2);int256 r3=kn(w0,w1,ni,lastU,m+3)-xu;
        evalBasis(l1,r1,l2,r2,l3,r3,N);
    } }
    function basisPair(uint256[87] memory W,uint256 base,uint256 ni,uint256 last,uint256 x,int256[4] memory N,int256[4] memory M) internal pure returns(uint256 m){ unchecked {
        int256 xu=int256(x)*U;int256 lastU=int256(last)*U;uint256 w0=W[base];uint256 w1=W[base+1];
        uint256 q;
        while(q<ni&&int256(((q<16?w0:w1)>>((q&15)<<4))&0xffff)*int256(K64)<=xu)q++;
        m=3+q;
        int256 l1=xu-kn(w0,w1,ni,lastU,m);int256 r1=kn(w0,w1,ni,lastU,m+1)-xu;
        int256 l2=xu-kn(w0,w1,ni,lastU,m-1);int256 r2=kn(w0,w1,ni,lastU,m+2)-xu;
        int256 l3=xu-kn(w0,w1,ni,lastU,m-2);int256 r3=kn(w0,w1,ni,lastU,m+3)-xu;
        evalBasis(l1,r1,l2,r2,l3,r3,N);
        evalBasis(r1,l1,r2,l2,r3,l3,M);
    } }
    function evalBasis(int256 l1,int256 r1,int256 l2,int256 r2,int256 l3,int256 r3,int256[4] memory N) internal pure {unchecked {
        int256 d=r1+l1;int256 n0=r1*U/d;int256 n1=l1*U/d;int256 n2;
        int256 tmp=n0*U/(r1+l2);n0=r1*tmp/U;int256 sv=l2*tmp/U;
        tmp=n1*U/(r2+l1);n1=sv+r2*tmp/U;n2=l1*tmp/U;
        tmp=n0*U/(r1+l3);n0=r1*tmp/U;sv=l3*tmp/U;
        tmp=n1*U/(r2+l2);n1=sv+r2*tmp/U;sv=l2*tmp/U;
        tmp=n2*U/(r3+l1);n2=sv+r3*tmp/U;N[3]=l1*tmp/U;
        N[0]=n0;N[1]=n1;N[2]=n2;
    }}
    // sd axis has no interior knots: Bernstein cubics in u=k/7.
    function bern(uint256 k,int256[4] memory B) internal pure { unchecked {
        int256 a=int256(k);int256 c=7-a;
        B[0]=c*c*c*U/343;B[1]=3*a*c*c*U/343;B[2]=3*a*a*c*U/343;B[3]=a*a*a*U/343;
    } }
    // Node sums carry U^3/8 scale: divide, clamp each grid node at 0 (as the decoder), then bilinear in (f,g).
    function bl(int256 n00,int256 n10,int256 n01,int256 n11,int256 f,int256 g) internal pure returns(int256){ unchecked {
        int256 D=8*U*U;n00/=D;n10/=D;n01/=D;n11/=D;
        if(n00<0)n00=0;if(n10<0)n10=0;if(n01<0)n01=0;if(n11<0)n11=0;
        return ((n00*(U-f)+n10*f)/U*(U-g)+(n01*(U-f)+n11*f)/U*g)/U;
    } }
    struct Ctx { uint256 nr; uint256 nc; uint256 last; int256[4] B0; int256[4] B1; int256 tt; }
    // Fee surface interpolated at rows i,i+1 (weight f), columns j,j+1 (weight g), sd levels k,k+1 (weight tt).
    struct Patch {int256[4] Nr0;int256[4] Nr1;int256[4] Nc0;int256[4] Nc1;uint256 mr0;uint256 dr;uint256 mc0;uint256 dc;}
    function patches(uint256[87] memory W,Ctx memory X,uint256 i,uint256 j) internal pure returns(Patch memory P,Patch memory M){unchecked {
        P.mr0=basisPair(W,0,X.nr-4,320,i,P.Nr0,M.Nr1);
        uint256 mr1=basisPair(W,0,X.nr-4,320,i+1,P.Nr1,M.Nr0);
        P.dr=mr1-P.mr0;M.mr0=X.nr+2-mr1;M.dr=P.dr;
        // 0c column knots are asymmetric; 1c contains exact integer interior knots.
        if(X.last==12||X.nc==12){
            P.mc0=basis(W,2,X.nc-4,X.last,j,P.Nc0);P.dc=basis(W,2,X.nc-4,X.last,j+1,P.Nc1)-P.mc0;
            M.mc0=basis(W,2,X.nc-4,X.last,X.last-1-j,M.Nc0);M.dc=basis(W,2,X.nc-4,X.last,X.last-j,M.Nc1)-M.mc0;
        }else{
            P.mc0=basisPair(W,2,X.nc-4,X.last,j,P.Nc0,M.Nc1);
            uint256 mc1=basisPair(W,2,X.nc-4,X.last,j+1,P.Nc1,M.Nc0);
            P.dc=mc1-P.mc0;M.mc0=X.nc+2-mc1;M.dc=P.dc;
        }
    }}
    function interp(uint256[87] memory W,Ctx memory X,Patch memory P,int256 f,int256 g) internal pure returns(int256){ unchecked {
        int256[4] memory Nr0=P.Nr0;int256[4] memory Nr1=P.Nr1;int256[4] memory Nc0=P.Nc0;int256[4] memory Nc1=P.Nc1;
        uint256 mr0=P.mr0;uint256 dr=P.dr;uint256 mc0=P.mc0;uint256 dc=P.dc;
        int256 A0;int256 A1;int256 A2;int256 A3;int256 A4;int256 A5;int256 A6;int256 A7;
        uint256 nc=X.nc;bool two=X.tt!=0;
        int256 b00=X.B0[0];int256 b01=X.B0[1];int256 b02=X.B0[2];int256 b03=X.B0[3];
        int256 b10=X.B1[0];int256 b11=X.B1[1];int256 b12=X.B1[2];int256 b13=X.B1[3];
        for(uint256 bb=0;bb<=dr+3;bb++){
            int256 s0;int256 s1;int256 s2;int256 s3;
            uint256 Li=(mr0-3+bb)*nc+mc0-3;
            for(uint256 cc=0;cc<=dc+3;cc++){
                uint256 lane=W[3+(Li>>2)]>>((Li&3)<<6);Li++;
                int256 c0=int256(int16(uint16(lane)));int256 c1=int256(int16(uint16(lane>>16)));int256 c2=int256(int16(uint16(lane>>32)));int256 c3=int256(int16(uint16(lane>>48)));
                int256 wc0=cc<4?Nc0[cc]:int256(0);int256 wc1=cc>=dc?Nc1[cc-dc]:int256(0);
                int256 d=b00*c0+b01*c1+b02*c2+b03*c3;s0+=wc0*d;s1+=wc1*d;
                if(two){d=b10*c0+b11*c1+b12*c2+b13*c3;s2+=wc0*d;s3+=wc1*d;}
            }
            int256 wr0=bb<4?Nr0[bb]:int256(0);int256 wr1=bb>=dr?Nr1[bb-dr]:int256(0);
            A0+=wr0*s0;A1+=wr1*s0;A2+=wr0*s1;A3+=wr1*s1;
            if(two){A4+=wr0*s2;A5+=wr1*s2;A6+=wr0*s3;A7+=wr1*s3;}
        }
        int256 v0=bl(A0,A1,A2,A3,f,g);
        if(!two)return v0;
        return (v0*(U-X.tt)+bl(A4,A5,A6,A7,f,g)*X.tt)/U;
    } }
    function table(uint256 ph,bool sy) internal pure returns(uint256[87] memory W,uint256 nr,uint256 nc){ unchecked {
        if(ph==0){T0c(W);return(W,24,10);}
        if(ph==1){if(sy){T1s(W);return(W,24,14);}T1c(W);return(W,18,12);}
        if(sy){T2s(W);return(W,24,14);}T2c(W);return(W,12,8);
    } }
    // real.py RealPolicy.lookup: w, r, sd in WAD bps; returns (bid fee, ask fee) in WAD.
    function fees(int256 w,int256 r,uint256 ph,bool sy,int256 sd) internal pure returns(int256 fb,int256 fa){ unchecked {
        uint256 k;while(k<6&&sd>=S(k+1))k++;
        int256 tt=(sd-S(k))*U/(S(k+1)-S(k));if(tt<0)tt=0;if(tt>U)tt=U;
        int256 pw=w/5+160*U;if(pw<0)pw=0;if(pw>320*U)pw=320*U;
        int256 p2;uint256 last;
        if(ph==0){int256 l2=r/5;if(l2< -6*U)l2=-6*U;if(l2>6*U)l2=6*U;p2=l2+6*U;last=12;}else{p2=pos2(r/5);last=48;}
        uint256 i=uint256(pw/U);uint256 j=uint256(p2/U);if(i>319)i=319;if(j>last-1)j=last-1;
        int256 f=pw-int256(i)*U;int256 g=p2-int256(j)*U;
        Ctx memory X;(uint256[87] memory W,uint256 nr,uint256 nc)=table(ph,sy);X.nr=nr;X.nc=nc;X.last=last;X.tt=tt;bern(k,X.B0);bern(k+1,X.B1);
        (Patch memory P,Patch memory M)=patches(W,X,i,j);
        int256 Fa=interp(W,X,P,f,g);
        int256 Fb=interp(W,X,M,U-f,U-g);
        int256 base=(pw-160*U)*5;
        int256 aw=base-w+Fa;int256 bw=w-base+Fb;
        fa=aw>0?U-exp(-aw/10000):int256(0);fb=bw>0?U-exp(-bw/10000):int256(0);
        fb=clip(fb,0,U/10);fa=clip(fa,0,U/10);
    } }
    function T0c(uint256[87] memory W) internal pure { unchecked {
        W[0]=0x2b762af92aaf2a6729f0290226fe2610259925512507248a23b422211e0711d1;
        W[1]=0x0000000000000000000000000000000000000000000000003e2f31f92ddf2c4c;
        W[2]=0x000000000000000000000000000000000000000002f002e0024800b8001b000b;
        W[3]=0x1813181b1873184817ef18cf17c618390000000000000000180018521836183e;
        W[4]=0x183218f917db18521850184518ac187f185417c919441861180c191d17ab1846;
        W[5]=0x0000000000000000144c14ad148214891849187d185a18620000000000000000;
        W[6]=0x143e17811158146314c512ff164c14cb143a158113b2147914801389158914aa;
        W[7]=0x14721595144a14a4000000000000000014a214b6152614f414591622136e141b;
        W[8]=0x0e500d880f2f0e770dd60ff00ce00e2000000000000000000e1e0e600e470e50;
        W[9]=0x0e560ed60e090e100ebd0cf8101f0f5c0eb20be612080ece0dde10c20c330e16;
        W[10]=0x0000000000000000074f075e074407460e9d0dbc0f050e980000000000000000;
        W[11]=0x077d0928059c072207d20630085d0794073b07fe06d507320783068907e3076a;
        W[12]=0x077c08ef06b90738000000000000000007a40882070b07ae0767092f0651068b;
        W[13]=0x042a03e803eb03da03fe044d0379039d0000000000000000041203fa03bb03ba;
        W[14]=0x047604cc053b054104db03cc0632060c044d04da04d00418042804d9036a03b5;
        W[15]=0x000000000000000002c802ed028702810492047205be05d40000000000000000;
        W[16]=0x03af02c30427052f03200309030d026f02c00331027602a602f202a702a6026e;
        W[17]=0x038803ee03ae032f000000000000000003a5038e041103ec032d0488032002e9;
        W[18]=0x0266025d023701d60232029c01da02540000000000000000026a024b020d0201;
        W[19]=0x033d022d048e06c7031202e90390035402c5031e037c025502b2026f02510324;
        W[20]=0x0000000000000000022e021201d901cd0305031f033f059b0000000000000000;
        W[21]=0x028e02a002f403a5028401e8026c021401fe024801c701f3027201a201fe01b4;
        W[22]=0x02d20301033a01d9000000000000000002800392032300ac02e202f702b30355;
        W[23]=0x0238018801e70195018a02b7016f01eb0000000000000000022d01ca01be01b4;
        W[24]=0x03070232039f03aa025702c602ab02f802b60225033d01cc01e8025901c60292;
        W[25]=0x000000000000000001ed01cb01c0019302ab02860340035d0000000000000000;
        W[26]=0x0203028702690308024a014a020c01b4019e022d016d01c502ac00a00218017a;
        W[27]=0x027902ed020303130000000000000000026d02660255033102ac0276031f026f;
        W[28]=0x0233009701db013200ff034f00650175000000000000000001d70165013b0171;
        W[29]=0x026d026703a5017301d9025e016b02a202a0016902a401c201140270012b0200;
        W[30]=0x0000000000000000014100fb010400f5024601ed037401bf0000000000000000;
        W[31]=0x00e302de006901ed01aefef60226009500f50236ffb3012b0233fdca036d0208;
        W[32]=0x01a201d801a501d20000000000000000015a0255008c029701f100fa02a90182;
        W[33]=0x0121fe760220017eff9404e5fad9fe17000000000000000000b7ffc200400175;
        W[34]=0x01400044023700c5008f019c003800ea0134ff34022400e2fff001e6fe96ffab;
        W[35]=0x0000000000000000000b00b6ffddfd2c00f601000109010f0000000000000000;
        W[36]=0xff960187fea6ffcf00b2fc7e02c8001effd102a8fc0e002d00eaf6730df70125;
        W[37]=0x0063005c00780076000000000000000000120121ff570086008effaf011b006d;
        W[38]=0x005df6c704e8ffd6fe5514b4eccbff0300000000000000000010fbd9023801ea;
        W[39]=0x0089fea501270025ffb40140ff6800000055fc9b00c3ffdfff3305d9fe12ffaf;
        W[40]=0x0000000000000000ffb2017efecafdb2000d004a000700320000000000000000;
        W[41]=0xffe20183ff6a00140043fd5c010cfff4ff9b0354fd6b000a00a2f92d0672000e;
        W[42]=0xffe0ffc1ff98fffe0000000000000000ffe900cbff0d0004000bff290070ffe3;
        W[43]=0x002efe7b007c0008ff8a0351fdc5ffc300000000000000000008ff64005a004d;
        W[44]=0xffddffc6005c0000fffe0062ffce00050010ff230047fffdffd70130ffa6fffb;
        W[45]=0x0000000000000000fffa0016ffebffc2000100200021fffa0000000000000000;
        W[46]=0x00000038ffe800020006ffb0001ffffefff4004fffda00010010ff5e005ffffb;
        W[47]=0x0005ffc3ffe800010000000000000000001dffcaffcf0000fffbffe50012fffc;
        W[48]=0x0002ffe100090000fffd0037ffe900000000000000000000fffffffe00020001;
        W[49]=0xffe10028000f000000040006fff90001fffeffe6000affffffff001efff60000;
        W[50]=0x000000000000000000000001ffff0000fffb00160004fffe0000000000000000;
        W[51]=0x0004000efff90000fffcfff0000700000002000efffa0000fffcffe9000b0000;
        W[52]=0x0005ffd2fffd000000000000000000000018ffaafff20000fffafffd00050000;
        W[53]=0xffffffea0008000000030024fff2000000000000000000000000ffff00010000;
        W[54]=0xffda003d002900000004fffefff70000fffeffe5000c00000001001bfff50000;
        W[55]=0x000000000000000000000001ffff0000fff8002c0006ffff0000000000000000;
        W[56]=0x00000025ffea00000001ffda00120000ffff001afff300000001ffd500160000;
        W[57]=0x0008ff96ffe60001000000000000000000170009ff4f0000fffdfff300160000;
        W[58]=0x0001ffee00090000ffff001dfff1000000000000000000000000ffff00010000;
        W[59]=0xfff4ffe7006e00000001000cffec00000001ffe500110000ffff0019fff30000;
        W[60]=0x00000000000000000000000000000000fff7003c0013fffe0000000000000000;
        W[61]=0x00000008fffa00000001fff800040000ffff0005fffd00000001fff800050000;
        W[62]=0x0001ffd3fffa0000000000000000000000010014ffc40000fffffffb00050000;
    } }
    function T1s(uint256[87] memory W) internal pure { unchecked {
        W[0]=0x2a892a072989291128a0283427cc276026ef267725f9257724df23f420d812c5;
        W[1]=0x0000000000000000000000000000000000000000000000003d3b2f282c0c2b21;
        W[2]=0x000000000000000000000000091007a906f6068d063005d00573050a045702f0;
        W[3]=0x17d8189617bc18221739180117d6180a16ed186b17d91806173b181917fb1806;
        W[4]=0x1841176019bd186017c318c217e6181017d018f91766182e17cd18371856182c;
        W[5]=0x181b18b917a517de181418c517b61891182c179a193e1874182f17171a30184e;
        W[6]=0x131a150f13a114351349140e142e141a185218bc17c1182b185d1875182d1809;
        W[7]=0x148d12be161214721404147513c8142c1405139314e7146113571439149d141b;
        W[8]=0x13f515fd12b2124213df173a10131344136517ce0f0c13b414a9139c148714c9;
        W[9]=0x1481145715ad14b0145a158713bb15c0145d140f155b1566144f13fc14ed1395;
        W[10]=0x0d3e0e610c400d3b0c620dfd0c5a0d6c0c710c900dcd0d310c810dcf0d030d5a;
        W[11]=0x0eae086515670e300c490f810c600cdd0cae0f8b0b3d0d440d000dcf0dde0d90;
        W[12]=0x0d6e0e7f0be80c020d660ee40c430f140dec0ad6112f0fe40dc00a4313220f13;
        W[13]=0x05f4065f05e905fd058f05e005c605ef0db00ed20a900d020dfd0cba0df30abb;
        W[14]=0x06e305380722063b064405ff05a906000610059706f5062a0558059705ea05e2;
        W[15]=0x0646085d0341049b0646086502ea050a05a20950019e05b1074604d306ef0682;
        W[16]=0x06e8069b08f4079706ad081c06d2098906d00601074e06b806a60634060404c8;
        W[17]=0x028e0267022b0252034502dc0287028502600250021902410290020e02930261;
        W[18]=0x03a5028c04a102f1028104aa01fb024a02a703c7022e027e0310034002a702a3;
        W[19]=0x038e0450047e04ac03750454046304cf0394035304d6043d0363035e044a03a2;
        W[20]=0x014b00a40151017a0169018effbc01330417049b04990477042d04e5049b0429;
        W[21]=0x0257023b025c01ef01fa022e01d301c7021001dc01b701bc0256022001cf01a1;
        W[22]=0x02c4031802e4031402b102bd02cd0328027802b7026f031b02c901c302f10319;
        W[23]=0x03bc03b50379039203c703c103bd03ec031e03a4032b033c0310031403770310;
        W[24]=0x01f001a60182019e01b201ae01dc012f017d01ebffdd01430165ffcf02e700f1;
        W[25]=0x0240022202980233022b01db024b021601f801fb01b7022801d101c401bd019e;
        W[26]=0x02c703490306032c02af02fd02f8032a027e028b02eb02c8025c024302ce027e;
        W[27]=0x00fa00a90052ffde00c50021ffff0194038a037b0387034203ae035b0390033d;
        W[28]=0x01d7018801d101b301b4017b0176018501b401890142010a01d7016401220184;
        W[29]=0x0242025902730277022a0204024c025401fb01e20218023e01e901b901e80208;
        W[30]=0x0385034e0276031403a303460311033f02bd02ee02b602b20291029102bf0296;
        W[31]=0x01a10113012901010116012500fa00dd0113011a000d002000b3ff38ff850112;
        W[32]=0x01c401c301e501da01c2015701cf019b017c017c0150019b0177012c0128013d;
        W[33]=0x029c02b9027e0293024c02790267026e020d02200237023301db01f6020501f3;
        W[34]=0x006a00caff3dfff70066fe3403be0044039302d103e502b4038c030e02e202b6;
        W[35]=0x015a00fa01480136015a00cc012800f7013f012800ae00de0150008500f90085;
        W[36]=0x01d501df01f901e101a301c201b601ca01a3015101b4018f015201660141017f;
        W[37]=0x03a2035c00df029403af033b02a903190282024c026b02020211027e01fd0231;
        W[38]=0x0121008b012b005f00ba0113ff4700ca002effdf0233feb300080479ee7800d2;
        W[39]=0x013f01420144015a014100e5013b012300fd00ee00e70107011d00d30058011a;
        W[40]=0x021502ef01ac024601d901f3024701c2017b01e7017301b30176015e01a4016f;
        W[41]=0x000702c8fb4cffd90020f7aa0ba9fe3903d4034d05c201b103fe025a02e20247;
        W[42]=0x00fd005d00e5008c00eb0079007d012000e300e5ffb400a700cdff4401f8ffc6;
        W[43]=0x01580149019d016c013e013601490145011800dd0124010000e100e200d30105;
        W[44]=0x03e5061105a80a3a042504f701ad023301a3019a028d022101bc0216017201a3;
        W[45]=0x005300610036011b010f00c2ff57fdc0ff40fcaf025e032aff58057af7c1fb4b;
        W[46]=0x00ce00c400d300c600cf006800ba00d800830083005c008200da003f00400095;
        W[47]=0x01b80234018600d40165016101b601b1011c0150013b010300f800f300f4011a;
        W[48]=0x0099fad90478fd14ff6400eeff4502650468072203a0073b0418019d04460684;
        W[49]=0x00890004000b009900850003005f00a800d8ff58ffcf00c1ffdc0197fe7300ae;
        W[50]=0x00e300ea012900b200ce008000f700dd0091009600700090007d002500bf0032;
        W[51]=0x047e03330a8e044703f2007c056f068a01af01f0012e008f013201480132018e;
        W[52]=0x0024ffd5ffe1005a00d8fbf0020c007dfde208bbfaebff95007cfcf2011afefd;
        W[53]=0x006a0020008700650045fffa0031005600490032ffee00240085fee901040056;
        W[54]=0x014200d901c6000000ed013200ee017b00ae00be00cd0081006b009e00430070;
        W[55]=0x015bf8220412000bff60025dff0afed7040e0775085f051d03100528016206e1;
        W[56]=0x008ffd94010a0051ffd00098ff8f003d0043fdcc0157003eff510426fd850042;
        W[57]=0x00630076006f006b005fffff0089005a0022000efffc0005fff5ffdaffe6ffcc;
        W[58]=0x03e5061f0832030702fa016602fe05e60151014d012d007200ab00ca00c200e0;
        W[59]=0xffc50114ff49002b00b4fd57017effd8fecd0471fdcbffdf0043fe6d0080002a;
        W[60]=0xff8afff2001bffe70010fffcff6c0014ff58016fff83ffea002eff490076ffe5;
        W[61]=0x003401a0ffdcff57009d003a00dc00e50021006c00130023ffc4ffdeffaeffc7;
        W[62]=0x006bfda50136fffdffd00091ffb0fff2030e08a0093803be04450119045506f6;
        W[63]=0x002dff3c0011fffbfff2005affbf000b0013ff6a0065ffd6ff990167ff2a0018;
        W[64]=0xffbcff9fffb9ffb20052ff760065000effd900a9ff88fff6001dffb8006bfff2;
        W[65]=0x030102ca0d0300d3027f014201b204dd00c0fff201200005002c00960028004d;
        W[66]=0xfffa001bffe700050016ffae003cffffffde0089ff9dfff70007ffd800120003;
        W[67]=0x002eff21003bffeeffe0004fffd60006ffe60022fffafff90006fff00012ffff;
        W[68]=0xff7a009cffc8ff33fffeffadffc80013ffd0ffcd0050ffe4ffa600b2ffad000e;
        W[69]=0x000dffcbffe8fff9fffa000cfffc0002029f0379141302fc03c402fb02850568;
        W[70]=0x0010ffdcffb8fff6fff7000d000a00050006fff2ffecfff7ffee0027000d0008;
        W[71]=0xffebfe79feccffbc0006ffda00cb0014000c0067fec7ffe1fffbffe300610009;
        W[72]=0x01d7fd0904e7011e019005e1032902fbfed3fae3fe49fea000a501f9012b0071;
        W[73]=0x0003ffed000500090002fffa0009fff6fffc0014fffb00080002fff90004fffc;
        W[74]=0x00b7fd3b00780021ff7b0121ffc4fff0000dffae001a000cfff5001a000afff8;
        W[75]=0x0229fd7700a7fd5ffba60869ff8eff95013ffb7201050039fe9402bdff6effd6;
        W[76]=0x0004ffe20024fff7fffe000afff20003fe3501dc0198fc1dfe2afdf5fa900026;
        W[77]=0xfff1004c006dffee0008fffeff850009fffc000a0025fff2fffd0015ffbf000c;
        W[78]=0xfe5506300444ffa00130fdd0fb850032ff3202db023affcc0078fef4fe5f0013;
        W[79]=0x00fdfc2d00a3010c020f04e5fe6e01defceb01b217e303ba03fff3e1eddd0070;
        W[80]=0x0003fff9ffdc00080001fff50030fff9fffe0010ffe300050001fffb0009fffe;
        W[81]=0x008afe3afca50019ffa400aa0172fff6000cffccff6e0009fffa00030056fffb;
        W[82]=0x025c029fdd65fb5bfd2f05641178ffe70122fca6f7c30029ff22013904a9ffe7;
        W[83]=0x0001fff9000cfffeffff0002fffc0000ff860198ffcd0006fe63fb0901c7fcd7;
        W[84]=0xfffc000e0028fffd00010001ffd30002ffff0000000ffffcffff0006ffea0003;
        W[85]=0xffab01540169ffed0021ff9dfe2d0007ffd9008400c4fff6000fffb6ff600003;
        W[86]=0x000fffa10005ffe6002d009effe1009aff7d009f065e00660074fd27f94a0011;
    } }
    function T1c(uint256[87] memory W) internal pure { unchecked {
        W[0]=0x0000000037dd2d9b2af42a2d298e28f7285527ab2709267225d3250c22651823;
        W[2]=0x000000000000000000000000000000000781074006bc064505bb054404c0047f;
        W[3]=0x17db180d18151829179c1808183f181e172018b817cf183617631852180e1826;
        W[4]=0x18a614971b5b185c1855182718171844180717731927182a17b0185e1807182b;
        W[5]=0x17e618e917c9185c185b168319b217e1174a1b82163618aa18a6163a18d3184c;
        W[6]=0x12f913f0131d1326128c135912d5131a1245131b133513281275137812f41328;
        W[7]=0x119d19ad0e6e129711ac16c10f5b12e2127a17640ec3134613a5128a14101339;
        W[8]=0x1336127e13bd12f21202186c0f1c13a514ce0c561768129c113e1887119112cd;
        W[9]=0x0b960b900be30bfd0b950af30c9b0bee0ae40d7b0b190c1b0b3c0bec0c010bf4;
        W[10]=0x0d8407230faa0ce10dad07c310440c7f0c4209690f200be60aaf0c5f0b980bf3;
        W[11]=0x0bb60d7c0b1c0c930d0506ee11a60b7a09fc13c005f20d340dd007fb0e0e0ca2;
        W[12]=0x051004910484047903f1059d03f7045a048b039c04c00481046504be04510473;
        W[13]=0x04650705030003e6041c071c0269043404b405c00368049805b4048004860488;
        W[14]=0x050d04d8048a041404d9071c015204f2055602e606fb039204b4064d036b040a;
        W[15]=0x0210029a01d001e202170095021a01b002fa034a01450264025d01c7020701a8;
        W[16]=0x02e60275041f038b030d01f10451027b025a02e702c801d401c702f801f201ed;
        W[17]=0x02ba034c03eb047c035b011806c50233024204ce0224060202e102ab046d0404;
        W[18]=0x01df01750195019d01f30215015700d601d10098040b020401da01f8008b0148;
        W[19]=0x023f021902ef012101ee02d6004704b701c90264009903e0020b017b01f80171;
        W[20]=0x027f026d02bf01ed021d0353005903e802c901f6043a00c7024a025e028b01f3;
        W[21]=0x01ab012f014800f301a7014100e601e7019dffbc0202005101ad01c000e0016c;
        W[22]=0x01e6020301fa02a001dd0188028d0129020600d00304ff9c016d0175012401e2;
        W[23]=0x02160275026102bc0281012903a401a601d703700180037b020e0214025c027b;
        W[24]=0x015700ed00c30171015201cb00f4fde401bcfebf01140388012e01be0107fffb;
        W[25]=0x01b7016d026501040167018f0151018d015401560062034a013900de014e0033;
        W[26]=0x021501f3020701d900d3032a00d701c602f20143031c01e80190020001c501c6;
        W[27]=0x011300c7005c00a200d8ff9201e5024700f7042efd38ffdb0129ff7600ee015b;
        W[28]=0x011c01a2011c0196015100db013601a300e400e0014dffc70141002c00e00134;
        W[29]=0x016b01e3020701870215012700aa0209011f027c020601730178013d01ec0139;
        W[30]=0x00a3007c002900b401b3ff7fff2f016f0006fee5038f000d00ed009aff7600e5;
        W[31]=0x011000a001b2006600be00ce007f010600bd003b00b200d800c8002e004a002b;
        W[32]=0x01800144013b01340047020a0160013a025300ac023a010b00e5015e00f3016e;
        W[33]=0x008e0009ffde0125ff910142fdd2ff56015dff5e012f012d0051ffd0ffe4003d;
        W[34]=0x007b00e3002201050095001500cf00560065fff90085ff950087ffefffbd011e;
        W[35]=0x00d600fe00eb012c016500c0014800020093020a001f01fb00c200b4010e0099;
        W[36]=0x0003ffccfeed016e00e7fdeb04a7ffa0ff92ff1bfd850073004eff4101160040;
        W[37]=0x007fffd2011fffc8fff10043ffc700310039ff2d004dffbc005aff61001100b7;
        W[38]=0x00d7004800e700aa002c0215ff8b00990130007b01ac00c700610077005a00b2;
        W[39]=0x0012ffda0069ff8fff560154fe22ff040069ff5f012100ceffd20042ff98ffaf;
        W[40]=0xfff4ffcbff360010fff6ffc2000dffec00020036ffae0029ffcd003bffedffc8;
        W[41]=0x008d0038ff400079ffe500ce02c0ff0900f60068ff7400e4ffcf00770026fff0;
        W[42]=0xfff7fff70004ffff0047ffa600620006ffba0045ffadfff1000effed00150000;
        W[43]=0xff5000de0032fffa0047fff5ffbd0007ffd100050034fff2002affd4ffec0006;
        W[44]=0xffa70067006bffc700a6fd2cfe2b004cfed00331ff9effa20085fdaa002cfff2;
        W[45]=0x000e0009fff60000ffa10067ff92ffff0048ffb600560004ffe9001affe50000;
        W[46]=0x010cfd8fffe10008ff66002d0050fff90054ffe9ffc10006ffb7004a0008fffd;
        W[47]=0x0038fe8dfff50018fedc05fdffc5ffca0182f7b701360036ff1003c2ffa30003;
        W[48]=0xffddffd90022ffff0069ffcb00570001ffac0031ffacfffb0013ffef0017ffff;
        W[49]=0xfdb2044400c9ffee00fa001cfef9000aff4500330091fff5008bff17ffed0005;
        W[50]=0xff9c01a0fffeffdc01a1f64f0068005cfd830e01fe79ff95019bf5c6008a0001;
        W[51]=0x0010004cffba0001ffc1ffedffee00000031ffff00230002fff30005fff40000;
        W[52]=0x017dfcf7fe15000cff53fecd018cfff800710059ff090007ff8b0090003bfffc;
        W[53]=0x0039fedefffe0016fed50650ffbfffbc01d9f68800b20048fe76073d0013fff4;
        W[54]=0xfffaffd400170000000d001cfffdfffffff4fff3fffa00000001000000020000;
        W[55]=0xff5b01770059fffc002fffbcff9b0002ffd80036001efffd0017ff8500000001;
        W[56]=0xffe4004afff5fff80056fd3e0032000fff700411ffeaffed004dfc34ff4c0002;
    } }
    function T2s(uint256[87] memory W) internal pure { unchecked {
        W[0]=0x2a992a092989291328a2283627ca275e26ed267725f7256724b42395204c12b7;
        W[1]=0x0000000000000000000000000000000000000000000000003d492fb42c6b2b4c;
        W[2]=0x000000000000000000000000094507e30720069d063305cd056304e0041d02bb;
        W[3]=0x17bb187d17b4180d172818051806180f1704187817c91803172f182817f51806;
        W[4]=0x17a4196a170a17f817b918be176f182c17dc1844181b181f17a5184618281821;
        W[5]=0x17cd196f1686196717f717f1193f183e17e0183e18f4183e17d7181818db1828;
        W[6]=0x133214c813e014351358141414201425180618a117ec1870182217ea19301795;
        W[7]=0x13f1148913f7143713f1146c13b4143013f2139315011457130f145e13f9141a;
        W[8]=0x14211496121f13a5141c151212231423149a11f8164f1515143b134e15cc1429;
        W[9]=0x1442144c144413ee140a1591122c151a14761245172311de13f0159c112213c6;
        W[10]=0x0d510e2b0c4b0d5f0c7a0e5d0d330d780cbd0cc70da00d640ca00e190d240d6c;
        W[11]=0x0c69118d09f80c8c0cdd0fa10b060d930d7c0d540dbf0d9d0ce10dfa0e020d8b;
        W[12]=0x0cf010d20a9a10000dae0c3912260ed20d420db011030e400d330d2d10760da2;
        W[13]=0x05e806d705ec062905af05c4062c06290d880e400ddc0e110dd80cf90f800dd4;
        W[14]=0x064b0694060e062e068d05f20601063506040629069e0648059c057b06370618;
        W[15]=0x06e105f5045a05c806c7069604830658076203c0088206e806d00569079d0641;
        W[16]=0x06e1068105b605b50688081103cc0607073e03f7083704410665082701e40561;
        W[17]=0x02cb02b202790291032702f502a002a702d602960277028902c2023d02a1028a;
        W[18]=0x02ee05680137022f0306045501be02c1034b032a02c502cd0318035b02bb02b7;
        W[19]=0x02a206d303a40513040601c005990397030c050b03a6032b036f03ca03630294;
        W[20]=0x01980133012a01810183006700fd017603a004d8054a0543046502140673051d;
        W[21]=0x021d02ef01a301b4020f021a01d301d1022801e701b601bd0261020d01d901bb;
        W[22]=0x02fb02a3039f03db0261034102f503af032b0140044e030e020e02d1029701b4;
        W[23]=0x035d037c03530302031e04dc02df03420353029e03b20360027c0457032a03d4;
        W[24]=0x01f601a60198018801b101a301bd0174014201e2009100dc01ac01590192017e;
        W[25]=0x01f602d001d40274028e014c025c02d8020501c0020401a801d301c901a401a0;
        W[26]=0x026003be02c1031302b10289032d02d2026702d202db028d028701fc02fd0256;
        W[27]=0x0171017eff53004a00f5ff0301a4012602fa036f034503820365026204350381;
        W[28]=0x01bb01bd017701dd01b6016c016e014b01b90178012f011601bd014d0144013f;
        W[29]=0x023f026b027602b402190220025b0279020e019f026b022601e9019b021401b5;
        W[30]=0x030302f802b7029c03000364029f02d4029702b002bb02ad025e02d802ab02cd;
        W[31]=0x017f0128012500f0015500c000e800ef008d01d800be0007011c0074ff3800b3;
        W[32]=0x01b301da01d701e001c6015a01a601c8017a0155015c016c019700ff0130010a;
        W[33]=0x0266029502a1026502510279024a0256020a0213026c022401e601e7020501f5;
        W[34]=0x0110012dff52ff570086feda01e200c002f7029802f40293030e0307026f02ff;
        W[35]=0x015300f701250140014800e800d900f9014a00fa00bd00a1011c00b000cb00e4;
        W[36]=0x01de021501d30207019d01e401c901cf01aa013001c50196015a014f01560157;
        W[37]=0x02ea02b70216025d02fa02d602b70211027f02610207023a020002770226022b;
        W[38]=0x00dd00e1009f009a0158000300590028ff8d015900fefff300f00056fb34ff66;
        W[39]=0x0147013a01520157013600ed012d0137010300de00be00fd0142007f00d90097;
        W[40]=0x02340225022b01c901c4027201ea01db017701c601d601a7016f0187018d0182;
        W[41]=0x0148ff420045fd81fff0fef100e000dc0334024a0292020e0303031e0253030f;
        W[42]=0x010e002300f400a700b10110ffa40123012afff200cfffdc0031012fff790125;
        W[43]=0x013c01ca014e018701450120017d0145011d00de011d011200e300df00cd00e8;
        W[44]=0x028902db01cd01be04260331018900e7011f02d701c1027c0203015c02320193;
        W[45]=0xffce017efeed008801f7fd9e02c0fe86fe1d03abfad302430112fdb00297fe0c;
        W[46]=0x00d100c500db00c800ce004b00c700ce00810093002a00620104ffd8008800c0;
        W[47]=0x023501b1013a0119013001db017401c10136013a0183011d00fd010300f80112;
        W[48]=0x01a1f6720aaafdb1fe7204d0f9a10133033a048d0819092201c101d7053704b3;
        W[49]=0x008ffff70013009e00ceffd8000d00a000cbff24003200daff5f0383faff009c;
        W[50]=0x00cf012800fc010300d60093010600d300990085007a00a30086001c00a5003b;
        W[51]=0x020d051d0797021a0556fc7605620670011b02b8013b00c3015f013201530166;
        W[52]=0x009cfed100000039002efde302eb0073ff25069bf7d100970088fca50412fea3;
        W[53]=0x006d002b007a00690043ffef00370043007dffccffef002b0058fed900fe0056;
        W[54]=0x01b800100276000f00c8018c00b9017500cc00ae010800ae0076009b005d0062;
        W[55]=0x00b3f944042effeeff7c027bfd9a00a4033305d906c3037600a20759fdb206f5;
        W[56]=0x0074fe0d00d10067ffd000cfff9d001f0053fe4c0103007dffc40246fe69ffea;
        W[57]=0x0068008b007d0073004c0033007a006a0026ffdc00230004fff9ffefffd3ffd8;
        W[58]=0x0293032c047a05ca03defdb004400601012201f400c8005a00c100cc00d300fd;
        W[59]=0xfff800c0ffc4ffb6ffcdfeb30061008dff9403d4fe4afef70027fe000129ffcf;
        W[60]=0xffc20019ffefffe5ffcbffe0ff670017ffb30125ffccffcf0010ff3d00280018;
        W[61]=0x00660143003aff750091007d00a101090033005b0064003cfff8ffdeffa7ffc8;
        W[62]=0xfffffe7700de0047ffee006fffadfff10239091f0852022f029200e8041f06ef;
        W[63]=0x0021ff570032000bfffb0053ffcdfff9fffcff9f003f0010001a009fff93ffd2;
        W[64]=0xffd6fff3ffa1ffbfffb7ff5a000ffffc00370051003200020002ffdd001ffff7;
        W[65]=0x028fff2b04cf013702fbff8b0209056b00bb00cb00a7ffff0032004f00520049;
        W[66]=0xfff70029ffcafff5fffdffc800520013fff3007fff61ffe00003ffdd00180003;
        W[67]=0xff9aff54ff84ffea001800250016000affd10046ffbbfff2000affdf00260006;
        W[68]=0xff900078ff1fff05ffddffd3fff6001fffd4ffc1001cffd5005d00a000070012;
        W[69]=0x0006ffc800190006fffd000dfff6ffff01de08ff0ee70202034a0124052f062d;
        W[70]=0x0024ffb6fff4fffcfff20022fff700010007ffd9000a0000fff9002bffeffffc;
        W[71]=0xffaafe73fee2ffc6ff81fff50083001600530031ff8effe9ffd9fffd002c0005;
        W[72]=0x01a2ff0d02e30057005a030001f60292ff16fd26feedfec100c8010800a60056;
        W[73]=0xfffa000dfff7ffff0004ffef000f0005fffc0019ffeffff90001fff700070001;
        W[74]=0xffb4fe81005a000a000300a7ffb9fffeffe3ffff000200010007fff9000c0000;
        W[75]=0x00fe03f4001bfec9fef0ff99fe5affe6ff43ff1b01c7001a007301a8ff3fffee;
        W[76]=0x0002ffed0019000affff0007fff7fffdfe15045fffbafed3ffbbfb33fdabff2c;
        W[77]=0x00080039003f0005fffefff2ffc3fffc0002fffe00180004ffff0004ffdffff7;
        W[78]=0xffd0047fff2e0020ffe8fc28fdcfffdfffec02ce00db000c0019fe91ff7fffee;
        W[79]=0x00d6faef012c00010156056efec70124fd7dfd4c0c1103d4017dfdebfafafee4;
        W[80]=0x0000fff9ffeafffc000000050017000800000004fff0fff80000fffd00050002;
        W[81]=0x0025fda3fe65ffdeffe30113009600140001ffb6ffaefff6ffff0013002c0005;
        W[82]=0x01eafff3ec85fadcfecd02a506b6012c005ffb78fdedffb9ffdb030c0265002b;
        W[83]=0x0000ffff0005000200000001fffeffffffb90199ffc40024fea3fd6e0174fe79;
        W[84]=0xfffd001b001100010001fff3ffeffffeffff0004000600010001fffcfff9fffd;
        W[85]=0xffbf0187001c000e001bfe71ff3cfff1ffe600ca00470006000aff71ffd2fffa;
        W[86]=0xfff5ffc10000fff2006a007fffe3004eff2d00ac031700ad0056feeefdb4ffa7;
    } }
    function T2c(uint256[87] memory W) internal pure { unchecked {
        W[0]=0x00000000000000000000000000000000314e2bc82a0228c4273c25fe24381eb2;
        W[2]=0x00000000000000000000000000000000000000000000000007710685057b048f;
        W[3]=0x180a17541d97180d182116671596181a16911a8818541808176717b8180b1828;
        W[4]=0x17e1185a15eb180b17b518161fe3183a17681b230e2b180b19d9120a16bd1844;
        W[5]=0x112b0fd90c0211d20fea176c13f8119f12160c3012b711b210d813d810d911c9;
        W[6]=0x114513c814691238125c0d1c0722118f121a10f822cd121f0bcb23f50f0a1161;
        W[7]=0x0b6409120cca0a2809ba0b24093c0a3e08b80c3307990a60094409630b3e0a1d;
        W[8]=0x09e00a4d08b309bf0a9b0a730fb70a44086c0f9afc0f09f60e65010f0d000aa9;
        W[9]=0x029e03ec01f802aa02f6016b02a7026402a001e8046e02950314034401a40292;
        W[10]=0x03b5029302d102d602280547014e031f0474ff8308e402b8028105e40148025f;
        W[11]=0x01d201a501ea010a01ae011d014a0202039602b8ff93fc78012400d002480357;
        W[12]=0x016c051f039b058904a9fae8064cfc82010b06d4fde9092c029e00a7046e029d;
        W[13]=0x00c80194ff5e04190211ff510199fba1febe05ff07b806a60212ff34fd4bfea0;
        W[14]=0x0261fe10033c0025ffec0b95fb03047a0275004204eeff440133021200cb010f;
        W[15]=0x00cdff220120fe7f002b018dfebd02b800c0f659fe67fe0700c102d200ea01b7;
        W[16]=0x00be04a4013e01f201e3f9c1028effcf010102a40071031a00d9001e01a3007a;
        W[17]=0xffd8ff8100100012ffd2fffaff9a0028004cff920340003bff7bff29fedcff89;
        W[18]=0x0068fe9e017fff9500040371fbfa00ef00af00ff01efffbcff9f0015fecb0003;
        W[19]=0x004c0022ffbefff9ffd4003c009bffea0036fde1fd87000fffe000470068fffa;
        W[20]=0xff99fdd4ff3f001b004d06060165ff6ffe92f7f0003f0019ffeb00ac007bfff9;
        W[21]=0xfdd7fed2012c0008015600c3fdcb0019ff0d00a80437fff60018ffe8fed0ffff;
        W[22]=0xff9e049500beffaa0192e88ffe550104fedb160a009fffc7005ffcf0fdf10006;
        W[23]=0x0194057afd1bfff6ff42fc2a039bffeb006101b0fb5f0009fff7ffa800f90002;
        W[24]=0x003dfb8fff24003bfee610d4046fff1600cfee1cfb4b002fff2901c70382fffb;
        W[25]=0xff24f9c902090002003a03e2fe230000fff2fde40180fff6fff10058ff6bffff;
        W[26]=0xffd3005e0074ffec006cfc70fc6c0020ff88017a0463fff6fffc00f8fc56ffff;
    } }
    // Four words: arb point/weight, retail mean/variance, spots, fees/time/count.
    function save(Belief memory b) internal { unchecked {
        slots[0]=uint256(uint128(int128(b.lp)))|(uint256(b.pi)<<128);
        slots[1]=uint256(uint128(int128(b.mt)))|(uint256(b.vt)<<128);
        slots[2]=uint256(b.sp)|(uint256(b.r)<<128);
        slots[3]=uint256(b.fb)|(uint256(b.fa)<<64)|(b.t<<128)|(b.cnt<<192)|(b.sy?uint256(1)<<255:0);
    } }
    function moments(int256 p,int256 m0,int256 v0,int256 m1,int256 v1) internal pure returns(int256 m,int256 v){ unchecked {
        m=mul(p,m0)+mul(U-p,m1);
        v=mul(p,v0+mul(m0-m,m0-m))+mul(U-p,v1+mul(m1-m,m1-m));
        if(v<0)v=0;
    } }
    function afterInitialize(uint256 x,uint256 y) external override returns(uint256,uint256){ unchecked {
        slots[4]=x|(y<<128);Belief memory b; b.sp=int256(y*1e18/x);b.r=b.sp;b.lp=ln(b.sp);b.pi=U;
        b.fb=2823606104386589;b.fa=2823606104386589;save(b);return(uint256(b.fb),uint256(b.fa));
    } }
    struct Mix {int256 p; int256 m0; int256 v0; int256 m1; int256 v1;}
    // Reweight by the no-arbitrage likelihood, preserving both components for two cuts.
    function cut(Mix memory c,int256 lo,int256 hi) internal pure { unchecked {
        int256 z0;int256 z1;
        (z0,c.m0,c.v0)=trunc(c.m0,c.v0+893025000000,lo,hi);
        if(c.p==U)return;
        (z1,c.m1,c.v1)=trunc(c.m1,c.v1+893025000000,lo,hi);
        int256 w0=mul(c.p,z0);int256 w1=mul(U-c.p,z1);int256 total=w0+w1;
        if(total>0){c.p=divi(w0,total);}
        else {if(c.p<U/2){c.m0=c.m1;c.v0=c.v1;}c.p=U;}
        if(c.p==0){c.m0=c.m1;c.v0=c.v1;c.p=U;}
    } }
    function update(Belief memory b,int256 s,bool buy,uint256 dt,uint256 tell) internal pure returns(bool arb){ unchecked {
        int256 lo=ln(mul(b.sp,U-b.fb));int256 hi=ln(divi(b.sp,U-b.fa));
        Mix memory c=Mix(b.pi,b.lp,0,b.mt,b.vt);
        if(c.p==0){c.p=U;c.m0=c.m1;c.v0=c.v1;}
        uint256 n=dt-1;if(n>12)n=12;
        for(uint256 i=0;i<n;i++){
            if(i==2&&c.p<U){(c.m0,c.v0)=moments(c.p,c.m0,c.v0,c.m1,c.v1);c.p=U;}
            cut(c,lo,hi);
        }
        c.v0+=893025000000;c.v1+=893025000000;
        int256 lp=ln(buy?mul(s,U-b.fb):divi(s,U-b.fa));
        int256 sd=root(c.v0);int256 la=mul(c.p,divi(pdf(divi(lp-c.m0,sd)),sd));
        int256 z0;int256 z1;
        (z0,c.m0,c.v0)=truncSD(c.m0,c.v0,lo,hi,sd);
        if(c.p<U){
            sd=root(c.v1);la+=mul(U-c.p,divi(pdf(divi(lp-c.m1,sd)),sd));
            (z1,c.m1,c.v1)=truncSD(c.m1,c.v1,lo,hi,sd);
        }
        int256 w0=mul(c.p,z0);int256 w1=mul(U-c.p,z1);int256 Z=w0+w1;
        int256 mt;int256 vt;
        if(c.p==U){mt=c.m0;vt=c.v0;}
        else if(Z>0){(mt,vt)=moments(divi(w0,Z),c.m0,c.v0,c.m1,c.v1);}
        else if(c.p>=U/2){mt=c.m0;vt=c.v0;}else{mt=c.m1;vt=c.v1;}
        int256 d=ab(ln(divi(s,b.sp)));if(d<1e9)d=1e9;
        int256 pi=pdf(divi(ln(d)+6801595083153746944,1176000000000000000));
        int256 lr=divi(mul(mul(Z,260000000000000000),pi),mul(d,1176000000000000000));
        pi=la+lr>0?divi(la,la+lr):int256(0);
        // Lean tell: negative -> retail; positive -> Bayes with L = 16/12889 (buy), 15/13131 (sell); else unchanged.
        if(tell==2)pi=0;
        else if(tell==1){int256 a=pi*(buy?int256(12889):int256(13131));int256 z=a+(U-pi)*(buy?int256(16):int256(15));if(z>0)pi=a*U/z;}
        bool keep=tell==1&&pi>U/2;
        if(keep&&pi>9999e14)pi=9999e14;
        arb=pi>U/2;
        if((pi>5e15&&pi<995e15)||keep){
            b.pi=pi;b.lp=lp;b.mt=mt;b.vt=vt;
            (b.m,b.v)=moments(pi,lp,0,mt,vt);
        }else {
            b.pi=U;b.lp=arb?lp:mt;b.mt=0;b.vt=0;
            // Single retail Gaussian is represented by weight zero on the point.
            if(!arb){b.pi=0;b.mt=mt;b.vt=vt;b.m=mt;b.v=vt;}
            else {b.m=lp;b.v=0;}
        }
        int256 pe=exp(b.m);b.r=clip(b.r,mul(pe,997e15),divi(pe,997e15));b.cnt=0;b.sy=false;
    } }
    function afterSwap(TradeInfo calldata t) external override returns(uint256,uint256){ unchecked {
        uint256 p0=slots[0];uint256 p1=slots[1];uint256 p2=slots[2];uint256 p3=slots[3];
        Belief memory b;
        b.lp=int256(int128(uint128(p0)));b.pi=int256(p0>>128);
        b.mt=int256(int128(uint128(p1)));b.vt=int256(p1>>128);
        b.sp=int256(uint256(uint128(p2)));b.r=int256(p2>>128);
        b.fb=int256(uint256(uint64(p3)));b.fa=int256(uint256(uint64(p3>>64)));
        b.t=uint64(p3>>128);b.cnt=(p3>>192)&((uint256(1)<<63)-1);b.sy=p3>>255==1;
        (b.m,b.v)=moments(b.pi,b.lp,0,b.mt,b.vt);
        int256 s=int256(t.reserveY*1e18/t.reserveX);bool arb;
        if(t.timestamp>b.t){
            uint256 pr=slots[4];
            uint256 tell=ltTell(uint256(uint128(pr)),pr>>128,uint256(t.isBuy?b.fb:b.fa),t.amountX,t.amountY,t.reserveY,t.isBuy);
            arb=update(b,s,t.isBuy,t.timestamp-b.t,tell);
        }
        slots[4]=(t.reserveX|t.reserveY)>>128==0?t.reserveX|(t.reserveY<<128):0;
        uint256 ph;
        if(!arb){
            int256 c=t.isBuy?divi(mul(s,U-b.fb),997e15):divi(mul(s,997e15),U-b.fa);
            if(t.isBuy?c<b.r:c>b.r){b.r=c;b.sy=true;}
            b.cnt++;ph=b.cnt==1?1:2;
        }
        int256 w=(ln(s)-b.m)*10000;int256 r=(ln(b.r)-b.m)*10000;
        (b.fb,b.fa)=fees(w,r,ph,b.sy,root(b.v)*10000);b.sp=s;b.t=t.timestamp;save(b);
        return(uint256(b.fb),uint256(b.fa));
    } }
}
```

**Taylor-derived strategy dependency: pinned challenge AMMStrategyBase.sol**

File `AMMStrategyBase.sol` — 4,506 bytes; SHA-256 `3f4154a6c4bb8f1223c7fc0bde1f9cd9dba10cef502e300d0f6d229f610b8869`.

<!-- file: AMMStrategyBase.sol -->
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IAMMStrategy, TradeInfo} from "./IAMMStrategy.sol";

/// @title AMM Strategy Base Contract
/// @notice Base contract that all user strategies must inherit from
/// @dev Provides fixed storage slots, helper functions, and fee clamping
abstract contract AMMStrategyBase is IAMMStrategy {
    /*//////////////////////////////////////////////////////////////
                               CONSTANTS
    //////////////////////////////////////////////////////////////*/

    /// @notice 1e18 - represents 100% in WAD precision
    uint256 public constant WAD = 1e18;

    /// @notice Maximum allowed fee: 10% (1e17)
    uint256 public constant MAX_FEE = WAD / 10;

    /// @notice Minimum allowed fee: 0
    uint256 public constant MIN_FEE = 0;

    /// @notice 1 basis point in WAD (0.01% = 0.0001 = 1e14)
    uint256 public constant BPS = 1e14;

    /*//////////////////////////////////////////////////////////////
                            STORAGE SLOTS
    //////////////////////////////////////////////////////////////*/

    /// @notice Fixed storage array - strategies can only use these 32 slots
    /// @dev This provides 1KB of persistent storage per strategy
    /// @dev Slot access is validated at the EVM level (array bounds)
    uint256[32] public slots;

    /*//////////////////////////////////////////////////////////////
                            HELPER FUNCTIONS
    //////////////////////////////////////////////////////////////*/

    /// @notice Multiply two WAD values
    /// @param x First value (WAD)
    /// @param y Second value (WAD)
    /// @return Result in WAD precision
    function wmul(uint256 x, uint256 y) internal pure returns (uint256) {
        return (x * y) / WAD;
    }

    /// @notice Divide two WAD values
    /// @param x Numerator (WAD)
    /// @param y Denominator (WAD)
    /// @return Result in WAD precision
    function wdiv(uint256 x, uint256 y) internal pure returns (uint256) {
        return (x * WAD) / y;
    }

    /// @notice Clamp a value between min and max
    /// @param value Value to clamp
    /// @param minVal Minimum value
    /// @param maxVal Maximum value
    /// @return Clamped value
    function clamp(uint256 value, uint256 minVal, uint256 maxVal) internal pure returns (uint256) {
        if (value < minVal) return minVal;
        if (value > maxVal) return maxVal;
        return value;
    }

    /// @notice Convert basis points to WAD
    /// @param bps Basis points (1 bps = 0.01%)
    /// @return WAD value
    function bpsToWad(uint256 bps) internal pure returns (uint256) {
        return bps * BPS;
    }

    /// @notice Convert WAD to basis points
    /// @param wadValue WAD value
    /// @return Basis points
    function wadToBps(uint256 wadValue) internal pure returns (uint256) {
        return wadValue / BPS;
    }

    /// @notice Clamp fee to valid range [0, MAX_FEE]
    /// @param fee Fee value to clamp
    /// @return Clamped fee value
    function clampFee(uint256 fee) internal pure returns (uint256) {
        return clamp(fee, MIN_FEE, MAX_FEE);
    }

    /// @notice Calculate absolute difference between two values
    /// @param a First value
    /// @param b Second value
    /// @return Absolute difference
    function absDiff(uint256 a, uint256 b) internal pure returns (uint256) {
        return a > b ? a - b : b - a;
    }

    /// @notice Simple integer square root (Babylonian method)
    /// @param x Value to take sqrt of
    /// @return y Square root
    function sqrt(uint256 x) internal pure returns (uint256 y) {
        if (x == 0) return 0;
        uint256 z = (x + 1) / 2;
        y = x;
        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }
    }

    /*//////////////////////////////////////////////////////////////
                          SLOT HELPERS
    //////////////////////////////////////////////////////////////*/

    /// @notice Read a slot value
    /// @param index Slot index (0-31)
    /// @return Value stored in the slot
    function readSlot(uint256 index) internal view returns (uint256) {
        require(index < 32, "Slot index out of bounds");
        return slots[index];
    }

    /// @notice Write a value to a slot
    /// @param index Slot index (0-31)
    /// @param value Value to store
    function writeSlot(uint256 index, uint256 value) internal {
        require(index < 32, "Slot index out of bounds");
        slots[index] = value;
    }
}
```

**Taylor-derived strategy dependency: pinned challenge IAMMStrategy.sol**

File `IAMMStrategy.sol` — 1,791 bytes; SHA-256 `85b2a0fce484b1c4f70c5bebe6c06042293b2099983f0b641c4a6656c7ea15ff`.

<!-- file: IAMMStrategy.sol -->
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title Trade information passed to AMM strategies
/// @notice Contains all data about an executed trade that strategies can use to adjust fees
struct TradeInfo {
    bool isBuy;          // true if AMM bought X (trader sold X)
    uint256 amountX;     // Amount of X traded (WAD precision, 1e18)
    uint256 amountY;     // Amount of Y traded (WAD precision, 1e18)
    uint256 timestamp;   // Simulation step number
    uint256 reserveX;    // Post-trade X reserves (WAD precision)
    uint256 reserveY;    // Post-trade Y reserves (WAD precision)
}

/// @title AMM Strategy Interface
/// @notice Interface that all AMM fee strategies must implement
/// @dev Fees are returned as WAD values (1e18 = 100%, 1e15 = 0.1% = 10bps)
interface IAMMStrategy {
    /// @notice Initialize the strategy with starting reserves
    /// @param initialX Starting X reserve amount (WAD precision)
    /// @param initialY Starting Y reserve amount (WAD precision)
    /// @return bidFee Fee when AMM buys X (WAD precision, e.g., 30e14 = 30bps)
    /// @return askFee Fee when AMM sells X (WAD precision, e.g., 30e14 = 30bps)
    function afterInitialize(uint256 initialX, uint256 initialY) external returns (uint256 bidFee, uint256 askFee);

    /// @notice Called after each trade to update fees
    /// @param trade Information about the just-executed trade
    /// @return bidFee Updated fee when AMM buys X (WAD precision)
    /// @return askFee Updated fee when AMM sells X (WAD precision)
    function afterSwap(TradeInfo calldata trade) external returns (uint256 bidFee, uint256 askFee);

    /// @notice Get the strategy name for display
    /// @return Strategy name string
    function getName() external view returns (string memory);
}
```

