| Rank by measured mean | Headroom source and evidence | Measured “ceiling” gain | SE | n | Actual report seeds, inclusive | `advance` | Best realisable capture measured here |
| --- | --- | ---: | ---: | ---: | --- | --- | --- |
| 1 | [Next retail order's side and size][NT] — future-order oracle; restricted fee adapter | +55.741962 | 0.239707 | 2,048 | 10000..12047 | true numerically | None measured. Foresight is unavailable to a strategy; requester excluded this from round two. |
| 2 | [Full callback-time engine information][FI] — achieved search **lower bound**, optimum unresolved | +23.838254 | 0.275076 | 2,048 | 10000..12047 | true numerically | None measured. Winning policy needs private price, rival state and the already-generated order queue. |
| 3 | [True current fair price][FP] — fixed-QLX5 posterior replacement | +1.456614 | 0.013306 | 2,048 | 10000..12047 | true | [Particle filter, arm A][PF]: +0.021165, SE 0.016351, n=128, seeds 10000..10127; **1.4530%** of this reference. Approximate, stopped; exact inferable fraction unresolved. |
| 4 | [True run volatility][VOL] — process-variance substitution | +0.028547 | 0.012706 | 128 | 10000..10127 | false; early stop | Not commissioned: this substitution did not advance. |
| 5 | [Engine behaviours: terminal fee oracle][AUDIT] — one decision on the final step | +0.003894 | 0.001105 | 128 | 10000..10127 | false; early stop | Not commissioned. Broader terminal relaxation: +0.026440 cap, SE 0.006966, same n/seeds; scope below. |
| 6 | [True retail arrival/size law][LAW] — selected likelihood-parameter mapping | +0.000569 | 0.007191 | 128 | 10000..10127 | false; early stop | Not commissioned: this mapping did not advance. |

All gains are paired changes in own-pool quote-asset edge per complete 10,000-step replica run. The ranking orders the reported means; the information sets, policy searches and kinds of bound differ. In particular, these six numbers are neither universal ceilings nor an additive explanation of the standings gap. “Realisable” here means using callback-visible information; contract cost has not been established.

**Is 528.45 reachable from QLX5? There is no demonstrated route in these results, and no justified contract design to build next. Reachability remains unresolved.** The supplied standings imply +0.1167 to reach 528.45, or +0.1187 to match #1 at 528.452 from 528.3333. The best measured callback-only candidate here is approximately +0.0212 with SE 0.0164 and a two-SE range spanning zero. It does not support a +0.12 forecast. These paired replica gains cannot be added to the supplied leaderboard score as a prediction.

Fair-price truth is the only advancing source pursued for realisable capture. It offers a large sensitivity, but both follow-up implementations explicitly failed to establish the requested exact posterior. Their small gains therefore do **not** prove that the remaining information is irreducible. The conditional contract sketch was not run because its gate failed. This closes the allocation with partial scientific findings, not an impossibility result. [Fair-price result][FP], [particle result][PF], [grid result][GRID].

Credit: **Taylor (gtmcknight)**, whose [solved policy in `gtmcknight/amm-sim` at commit `4812a6382311624e1506aca131ca35c378f930d9`][TAYLOR] underlies QLX5. QLX5's network extensions and the supplied replica retain their contributors' credits. The baseline is the supplied `code_zb64.QLX5`, source SHA-256 `e183e5bc3fb794b7067703b10a7da9920267aa5f4caa968e16ca101b02338f40`, from the [pinned baseline artifact][BASE]. This report concerns the supplied standings and pinned research, not a fresh leaderboard check.

**What the measurements establish**

For seed i, the measured delta is candidate edge minus unchanged QLX5 edge on the same exogenous path. Reported SE is the sample standard deviation of those deltas divided by sqrt(n), with the n−1 sample-variance denominator. The rival remains the fixed 30-bps policy. A policy can change routing, inventories and subsequent callback opportunities; preservation of exogenous draws does not imply preservation of fills.

The prescribed report bank was 10000..12047, with score.py checks at n=128, 256, 512, 1,024 and 2,048. Workers stopped when mean + 2 SE < +0.08. A positive advance required the lower endpoint to reach +0.08; the recorded protocol also required all 2,048 report seeds and passing execution controls. The completed advancing results have lower endpoints +55.262548 for next retail order, +23.288101 for full information, and +1.430001 for fair price. The stopped round-one probes have upper endpoints +0.053960 for volatility, +0.014951 for retail law and +0.006104 for the terminal fee oracle. All stopping figures were recomputed from the supplied deltas for this write-up.

These repeated two-SE checks implement the requested screening rule. They are not an anytime-valid confidence sequence or a guarantee against selection error. SE across seeds also does not measure approximation bias in a filter. Unrun report seeds have no results assigned to them.

Selection remained inside the permitted choose bank, but several items used only prefixes:

| Item | Actual choose/diagnostic use | Selection scope |
| --- | --- | --- |
| Fair price | 64000..65023, n=1,024 | One prescribed posterior replacement; no fitted fee parameters. Choose gain +1.492901, SE 0.019280. |
| Volatility | 64000..65023, n=1,024 | One sigma-squared substitution. Choose gain −0.001319, SE 0.003926. |
| Retail law | 64000..65023, n=1,024 | Three fixed parameter mappings; selected the highest choose mean. |
| Next retail order | Screening 64000..64127; final comparison 64000..65023 | 55 arm evaluations, including repeats/controls, in groups of at most five; final selected mean +55.923961, SE 0.342372. |
| Full information | Search 64000..64031, refined to 64000..64063; off-controls through 64127 | Three policy families; selected mean +22.590409, SE 1.178813 on 64 seeds. |
| Engine behaviours | Terminal probe/cap 64000..65023; rounding/dust diagnostics 64000..64127 | One primary terminal mechanism. Diagnostic caps use unchanged choose trajectories. |
| Particle | 64000..64031, n=32 | Compared 512 and 2,048 particles; used 2,048 on report. |
| Grid | Four complete runs, 64000..64003; refinements on seed 64000 for 2,000 steps | Selected 8-bps spacing and eight joint parameter nodes; fine-resolution checks were short traces. |

Sources: [FP], [VOL], [LAW], [NT], [FI], [AUDIT], [PF], [GRID]. Each reports freezing its implementation before report evaluation. The prefixes and short refinement traces are limitations, particularly for posterior convergence; they are not the full planned choose bank.

**Fair price: large truth sensitivity, small approximate capture**

The fair-price intervention resets QLX5's log-price posterior mean to ln(current true price) and its current posterior variance to zero at each successful own callback, before the existing rival-price clipping and fee selection. It occurs after the triggering fill, so it cannot change that fill. Initialization and the fixed process variance remain unchanged; no callbacks are added during silent intervals. No true event label, run parameter, rival reserve or future order is supplied. The measured effect therefore includes the coupled mean-and-uncertainty reset and its later consequences. It is not the effect of changing the mean alone. [FP]

Its gain is +1.4566139111071181, SE 0.013306207949579568, n=2,048. The baseline and oracle means on this bank are 533.2560040516776 and 534.7126179627846. Those sample means also illustrate why this result is not a direct forecast from the leaderboard's 528.3333. It is a sensitivity of the existing QLX5 policy to truth; the optimal price-informed policy was not solved. [FP]

The requester's later note narrowed round two to a single deciding question: how much of that reference can be recovered by an exact posterior using everything available at own callbacks? Particle and grid methods were commissioned as two attempts at that measurement. Arm A infers run parameters from their laws and callback history; arm B additionally receives the actual run volatility and retail parameters as an oracle sensitivity. Arm B is not a callback-only capture.

| Filter and arm | Gain vs QLX5 | SE | n / report seeds | Mean + 2 SE | Fraction of +1.4566139111071181 | Outcome |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| Particle A: callback-only inputs | +0.021165036359 | 0.016351362073 | 128 / 10000..10127 | +0.053867760504 | 1.453030% | First-look stop; `advance=false`; sketch gate failed. |
| Grid A: callback-only inputs | +0.020141961941 | 0.015283153832 | 128 / 10000..10127 | +0.050708269605 | 1.382793% | First-look stop; `advance=false`; sketch gate failed. |
| Particle B: true run parameters added | +0.021280721692 | 0.015620277501 | 128 / 10000..10127 | +0.052521276695 | 1.460972% | First-look stop; parameter-truth sensitivity only. |
| Grid B: true run parameters added | +0.017761660423 | 0.014961759813 | 128 / 10000..10127 | +0.047685180050 | 1.219380% | First-look stop; parameter-truth sensitivity only. |

Sources: [particle][PF], [grid][GRID]. Percentages divide each reported point estimate by the full-bank fair-price reference. The denominator uses 2,048 seeds while the numerators use 128; these are descriptive capture ratios, without a joint ratio-confidence claim. As a scale comparison only, +0.1187 is 8.1490% of the truth reference, whereas the best measured A-arm point estimate captures 1.4530%. Neither percentage predicts leaderboard movement.

The A arms used callback side/amounts, own reserves, timestamps, own fees and the known process laws; they report excluding seed IDs, market RNG state, true prices, true labels, true rival reserves, drawn run parameters and future orders. The particle filter uses its own independent random stream. The grid tracks price, rival state, parameter uncertainty and hidden retail counts, with analytic inversion of continuous router relations. Both replace QLX5's belief through the supplied hook, preserving its other policy equations and tables. [PF], [GRID]

The two A-arm outcomes agree on these seeds: particle minus grid is +0.001023074418, paired SE 0.012656452720, n=128, recomputed from their common-seed deltas. They must not be pooled as independent evidence or added together. Agreement also does not exclude shared approximation bias.

Both report recovering the same fair-price control on seeds 10000..10127: +1.472416081754699, SE 0.05109604665169002. This exactly matches the first 128 deltas of the original fair-price result. Hook-off/passive parity and exogenous-stream checks support the mechanics of the experiment, but do not establish the likelihood's exactness. Those execution claims were not rerun during this write-up. [FP], [PF], [GRID]

**Where the filters improve price error**

The following are passive measurements on unchanged QLX5 trajectories. They compare both beliefs against true contemporaneous price at the same callbacks. True prices and event labels are used for diagnostics after inference, not as A-arm inputs.

| Method and callback class | QLX5 RMSE, bps | Approximate posterior RMSE, bps | Callbacks | Passive seeds |
| --- | ---: | ---: | ---: | --- |
| Particle: all | 7.086835 | 7.054083 | 1,386,726 | 10000..10127, n=128 |
| Particle: arbitrage | 0.602288 | 0.305614 | 486,154 | Same 128 seeds |
| Particle: retail | 8.782899 | 8.750518 | 900,572 | Same 128 seeds |
| Grid: all | 7.111594 | 7.088328 | 348,145 | 10000..10031, n=32 |
| Grid: arbitrage | 0.503472 | 0.130631 | 121,537 | Same 32 seeds |
| Grid: retail | 8.807023 | 8.785379 | 226,608 | Same 32 seeds |

Particle error is 10,000 × RMS log-price error. Grid error is RMS of 10,000 × (estimated price / true price − 1), where estimated price is the exponential of the filter's log-price mean. Different definitions and samples prevent a direct cross-method RMSE ranking. The grid scoring experiment still used 128 seeds; only its passive audit used 32. [PF], [GRID]

Within each method, arbitrage error falls substantially, while retail error changes little and remains much larger. This is consistent with the small measured fee-score gains. It does not quantify how much of the remaining retail error is fundamentally unobservable. Passive nominal-95% interval coverage was 97.8574% for particle and 98.4969% for grid; conservative coverage and posterior atoms do not certify an exact posterior. [PF], [GRID]

The exact-posterior requirement remains open for specific reasons:

- Both methods use continuous observation densities and Taylor's tell/lattice approximations instead of integrating the complete binary64/WAD rounding preimages of the joint callback observation. Some available low-bit router evidence is omitted, and the extreme 99%-reserve arbitrage cap is not separately integrated in the likelihood.
- The particle result uses 2,048 particles, resampling, finite path histories and parameter rejuvenation. Its 512-versus-2,048 comparison on 32 choose seeds supplies no convergence certificate or bias bound.
- The grid result uses 8-bps price/rival grids, two prior quadrature nodes per run parameter, eight joint parameter states, truncated hidden-order integration and an idealized constant-product rival. Finer grids and three-node parameter checks cover only one 2,000-step choose trace, not complete-run score convergence.

The particle result explicitly records `exact_posterior_established=false`; its `controls.passed=true` applies to mechanical controls. The grid records `controls.passed=false`, `execution_controls_passed=true` and `exact_posterior_requirement_passed=false`. Administrative acceptance of these reports does not change those scientific qualifications. Consequently, the requester's “otherwise irreducible” conclusion cannot be supported by these approximate measurements. [PF], [GRID]

**What the other oracle sources mean**

The next-trade item actually reveals the next distinct **retail order**, before routing, rather than the next own fill or an arbitrage-inclusive next event. Its size is quote notional; a future sell's native-X size is not supplied. The next order may be in a later timestamp, with unobserved arbitrage in between. The replica copies the retail RNG to peek without consuming the live stream. The intervention also changes the fee returned at initialization, in addition to own swap callbacks. This initialization exposure and narrower event definition should be retained as differences from a strict swap-callback-only reading of the requested probe. [NT]

The selected adapter computes z = clamp(next size / (0.002 × own Y reserve) − 1, −1, 4), adds 5 + 17z bps on the predicted side and subtracts 11 bps on the opposite side, preserving the fee cap and gamma guard. Its +55.741962 is an achieved gain from a restricted three-coefficient search with future knowledge. It is neither a universal upper bound nor evidence that order prediction from callback history is possible. No estimator or capture fraction was measured for this source; an absent measurement is not zero. [NT]

The full-information item searched fee policies, rather than only injecting truth into QLX5. Its winning rule acts at a retail callback with another already-generated order in the same timestamp. It accounts for the pending rival fill, searches the next order's fee over 0..1,000 bps in 50-bps coarse steps, then applies 15 golden-search refinements around the best point. It keeps the other QLX5 fee and falls back to QLX5 when no eligible next order exists. Current true price, rival state and the private queue are used; no next-timestamp draws are used. [FI]

This achieves +23.838253663028897, SE 0.27507639991996496, over 2,048 report seeds. It is a lower bound on the value attainable with that engine-private information. The local one-order optimization ignores later value and has no global optimality guarantee across routing discontinuities. The smaller gain than the next-retail oracle is not a certified optimization gap: the latter sees across timestamps and acts at initialization, and the searched policy families differ. [FI], [NT]

The full-information report also supplies a very loose pathwise upper envelope: each retail order's positive own edge is at most its quote-notional input, arbitrage contributes nonpositive edge, so total edge is bounded by the sum of retail notionals, with a 0.001 numerical allowance per run. On report paths, its mean bound minus QLX5 is +159,185.816529, SE 523.669587, n=2,048, seeds 10000..12047; the reported mean upper-minus-achieved gap is 159,161.978275. The report calls this bound certified, but this write-up has not independently certified its numerical allowance. Even taken at face value, it does not locate the full-information ceiling anywhere near the precision needed here. [FI]

The volatility probe replaces only QLX5's process-variance slot with the true run sigma squared after each own fill. It leaves initialization, tables, posterior state and the silent-step handling unchanged. Its first-look upper endpoint +0.053960 fails the +0.08 continuation screen. This closes that substitution, not every possible volatility-conditioned policy. [VOL]

The retail-law probe supplies the exact Poisson rate and full-order lognormal parameters, but QLX5's fitted likelihood concerns the first own fill after routing and selection. The worker compared three midpoint-preserving maps on choose seeds; the selected map scales QLX5's rate weight by lambda/0.8, shifts its log-mean by the change in the true full-order log-mean, and preserves the existing shape because the run's log standard deviation is fixed at 1.2. Its +0.000569, upper endpoint +0.014951, closes this approximate transport. It does not bound a freshly solved routing-conditioned likelihood or reoptimized tables. [LAW]

**Engine scoring and routing audit: quick ceilings and exclusions**

The audit read `amm_sim_rs` and the competition caller in [benedictbrady/amm-challenge at commit `6b6921f8d463314aa7c96234e1be25a25245f704`][ENGINE]. It reports checking formula/order alignment with the supplied replica and the core's pinned provenance. This is a separate engine-source pin from Taylor's strategy repository. The supplied 512-seed printed-precision parity was inherited, not rerun. Neither public source nor inherited parity independently proves the live leaderboard binary/configuration. All entries below are from the [engine-behaviours result][AUDIT]. File/line references are at that engine pin.

| Behaviour and source locus | Quick ceiling or exclusion | Scope and decision |
| --- | --- | --- |
| Final-step fee opportunity; `simulation/engine.rs:136–180`, `market/router.rs:181–249` | Fee oracle +0.003893548970, SE 0.001105287207, n=128, 10000..10127. Broader relaxed cap +0.026439950457, SE 0.006966149108, same seeds; upper two-SE +0.040372248673. | At first own callback of t=9999, search 43×43 fee pairs using true price, rival reserves and remaining orders. Later fees follow QLX5. The cap allows arbitrary later fee choices from that callback but uses ideal CFMM arithmetic plus a numerical allowance. It excludes earlier anticipatory policies and is not interval-certified. No advance. |
| Terminal inventory/PnL; `simulation/engine.rs:141–164,183–216`, `competition/match.py:168–188` | Exactly 0 direct score improvement from changing terminal valuation alone. | The competition sums trade edges; terminal mark-to-market PnL is separate. Holding fills fixed, there is no liquidation or final-price scoring bonus to recover. |
| Retail output WAD roundtrip; `types/wad.rs:30–40`, `market/router.rs:198–244` | Mean direct-error cap 7.03789336238333e−11, SE 8.757230069646189e−13, n=128, choose 64000..64127. | Bound sums conservative rounding envelopes on unchanged baseline fills. It excludes routing/classification/path changes and assumes finite nonsaturating arithmetic. Too small as a direct scoring effect. |
| Side-asymmetric router dust; `market/router.rs:188–244` | Mean gross-input cap 0.004508218487429125, SE 0.0004440842175567628, n=128, choose 64000..64127. | Legs execute only for input >0.0001, in the input token, and dropped allocations are not reassigned. Cap covers positive baseline own allocations that were skipped, valued even with free output. A fee-changing policy's dynamic dust ceiling is **unmeasured**. |
| Continuous splitting and fee aliases; `market/router.rs:40–118`, `amm/cfmm.rs:119–196` | 0 extra pricing action from aliases mapping to the same binary64 fee/gamma. | Routing continuously splits; ties do not award the entire order to the first pool. QLX5 already uses split arithmetic and guards the vanilla-gamma preimage. This is not a zero bound on all floating-point path effects. |
| Own-first callbacks and frozen allocations; `simulation/engine.rs:120,136–163`, `market/router.rs:196–280` | 0 ability to reprice the triggering fill or its already-computed rival allocation. | Callback fees affect subsequent orders. There is one arbitrage attempt per pool per step and no second arbitrage pass after retail. Subsequent-order benefits belong to other probes. |
| Separate fee buckets, reserve arithmetic and arb cap; `amm/cfmm.rs:119–284`, `market/arbitrageur.rs:54–138` | 0 direct gain from counting/compounding fee buckets again for fixed fills. | Existing QLX5 tells already use these operations. The 99%-X-output arb cap is outside ordinary near-price states; no universal extreme-state dynamic cap is established. |
| Revert fallback, legal-fee decoding and gas; `amm/cfmm.rs:293–298`, `types/trade_info.rs:116–134`, `evm/strategy.rs:31–34,179–188` | 0 extra fee action from deliberately reverting; 0 direct edge from gas savings with fixed fills. | A failed callback retains prior fees, an action already available by returning them. Malformed or >10% fees are rejected. Replica omits EVM gas/rollback behaviour, so no engine-exploit conclusion is claimed. |
| Configuration and RNG paths; `competition/config.py:26–47`, `competition/match.py:99–138`, `simulation/engine.rs:51–70` | No separate measured ceiling. | Active Python configuration sampling matches the replica; a different Rust helper is not on that caller path. Price and retail streams are separate. Hidden-law and next-order effects are delegated to their round-one probes. |

The terminal oracle, its relaxation, dust and rounding figures must not be summed. They are overlapping mechanisms measured under different restrictions. No engine behaviour supplied a qualifying new lead; dynamic dust and extreme-state policy effects remain unmeasured rather than ruled out globally.

**Build decision and remaining evidence**

Keep QLX5 as the implementation baseline. No contract change in this allocation has a supported expected gain sufficient to reach 528.45. The best measured callback-only point estimate is the finite particle filter's +0.021165, with substantial sampling uncertainty, unresolved numerical bias and no contract-cost validation. The grid offers essentially the same measured scale. True-parameter arm B does not improve that conclusion.

If the question is reopened, the deciding research remains the one the requester specified: complete the exact observation likelihood, including rounding preimages and hidden rival/arrival state; establish full-run numerical convergence; then evaluate the frozen posterior-to-QLX5 replacement with the stated seed split and controls. Only a validated posterior result of at least +0.15 on the full report bank would justify the conditional cheapest-approximation sketch. That sketch would need a measured capture and evidence for ≤50,000 source characters and ≤245,000 peak `afterSwap` gas. No such capture, size or gas estimate exists in these results, so none is invented here.

Two scientific deliverables remain unresolved: the exact callback-inferable price fraction, and a tight optimized full-information ceiling. The next-retail measurement also differs from a literal next-event, swap-callback-only experiment as disclosed above. These gaps prevent declaring 528.45 impossible, declaring fair-price headroom irreducible, or claiming that every source has been tightly bounded. They do support withholding a new build recommendation.

The objective's settled scalar, rule/table, label/split, residual-head, prior belief, rival-tracker and kappa work was treated as prior evidence and not rerun. No joint estimator/rule combination was measured in this allocation; earlier small gains cannot be stacked with these figures.

**Batch and closeout record**

The goal record shows eight accepted research results across the first three batches, and one conditional sketch item cancelled as `not_run`. All four batches specify `requires={"platform":["linux-x64"],"minCpus":8}` and have at most five items. The notes/brief previews require caches under `test/scratch/`, Taylor credit, replica-only work, no Solidity, no engine runs and no submissions. Full original briefs are not present: `goal.json` contains shortened previews. The following records the per-item work and expected evidence from the objective, notes and results; it does not invent missing verbatim briefs or launch another batch.

| Batch | One item's piece of work | Required result content | Recorded outcome |
| --- | --- | --- | --- |
| `r1-oracle-ceilings`, 5 items | Each item handles exactly one of fair price, run volatility, retail law, next trade, or full information. The full-information item searches/solves a fee policy. | `result.json` with gain, SE, n, seeds, source hash, advance, exposure/timing, selection, controls, stop history and scope of ceiling. | Five accepted reports. Three numerical advances; substantial bound limitations disclosed above. |
| `r1-routing-audit`, 1 item | One item reads engine scoring/routing behaviour and assigns each finding a quick ceiling, with a primary replica probe. | Same numerical fields for the primary probe; source loci, per-behaviour caps/exclusions, assumptions and unmeasured effects. | Accepted; primary probe stopped at 128 report seeds. |
| `r2-exact-posterior`, 2 items | Each item attempts one posterior method, particle or grid, with A/B arms and passive error diagnostics. | Standard numerical fields, fraction of the fair-price reference, RMSE by callback type, information isolation, truth/off controls, approximation/convergence disclosure and `gates.posterior_ge_015`. | Both reports accepted as measurements; neither established exactness; both gates failed. |
| `r2-contract-sketch`, 1 conditional item | One item, paired to particle, sketches the cheapest contract-feasible approximation only after `gates.posterior_ge_015 == "pass"`. | Capture vs posterior and truth reference, size/gas estimates with estimation method and limit assessment. | Gate-cancelled, `not_run`; no sketch evidence exists. |

All batches are settled. `trunk` is null in the supplied goal record: this research goal has no produced code repository or merged wave commit to name. Taylor's repository/commit and the audit's engine repository/commit above are source provenance, not a new goal build. Worker research implementations are carried in their result artifacts. This deliverable is only `report.md`.

For the closeout record, the decision is one JSON object in the reference's shape, embedded here to preserve the requested single-file output:

```json
{
  "notes": "Credit Taylor (gtmcknight), amm-sim research/solved at 4812a6382311624e1506aca131ca35c378f930d9, and QLX5 network extensions. Close this allocation with eight research results. No measured callback-only route to the supplied 0.1187 gap; exact posterior inferability and a tight full-information ceiling remain unresolved. The conditional contract sketch did not run. No new batches or build recommendation.",
  "spawn": [],
  "finish": true
}
```

**Evidence identity and checks on this write-up**

Every supplied result's raw bytes were checked against the requester-pinned SHA-256. The embedded paired data were decoded as data, their supplied payload hashes verified, and all eight headline means, SEs and n values recomputed. Both B arms, all five checkpoints of each full-bank oracle, the A-arm paired comparison and the capture ratios were also checked. Reproduction source/patch bundle hashes were verified in memory; no embedded commands, simulation, engine, Solidity build or submission were executed for this write-up. These checks establish internal consistency, not independent experimental replication.

The plane flags sources for fair price, volatility, retail law and engine behaviours without giving reasons. Those flags are disclosed, not explained away. The unflagged results are not independent method certification either. Mechanical controls, source alignment and inherited engine parity remain worker-reported evidence except for the artifact/statistical checks just described.

Result hashes identify the input JSON bytes. `source_sha256` identifies each worker's measured implementation under its declared hash scope; it is distinct from both the result hash and the common QLX5 baseline hash.

| Input / citation | Result JSON SHA-256 | Measured `source_sha256` and scope |
| --- | --- | --- |
| `b01-fair-price` / [FP] | `c9ac833b4a6837bf0bd56fc2c4b931ef58d34dc98a000278ee4cec091fb216ee` | `bd90489648c1112a14767bd0befbefc9687cd32f68ae647860cf8929ed5f966d`; sorted runtime filenames and bytes with NUL separators. |
| `b01-run-volatility` / [VOL] | `9f16f7d816edaff1d23de863f4f2149b1823b2842856cb8a0b41f986442226b0` | `2092df4f2801811a7c17a658ca0a601ae4416b0ffd212fdc40f6333faf9c9310`; measured `core.hpp`. |
| `b01-retail-law` / [LAW] | `ef182bcb6b8d517b486b508ecf6969451bc7fa7da9ccced5fb76033d19f2117a` | `c72de3145ffb1d049dc254397533c72efe8ceb01bbf82c1c0a44f3535c7babcc`; probe `policy.hpp`. |
| `b01-next-trade` / [NT] | `19a9830766394638451d952df2f20e3a66d25059305d112fe0dd0ec47b7701f1` | `7adb2807e9e6e48ac41d449c5840016a761f96f73e79374c7598297b5b65ee0c`; probe `core.hpp`. |
| `b01-full-information` / [FI] | `7aef6cf758ba6716bcfcbfa89a011cfc40a1bcadaae5fd3548e572ff96f1e50a` | `56cde84d17fef731c3608ba3a564ddbc0074060247c27b4f51418add6b173e80`; `oracle/oraclepolicy.py`. |
| `b02-engine-behaviours` / [AUDIT] | `5b2315dfcf16f8f0040df6f5db14b27f68e24ebae38b6b15350ee85425d016c0` | `498b799e13b2543f9117420ccc2a37f94c418bdc6657257d2ef7280b0c8742ce`; decoded compact JSON source map. |
| `b03-particle` / [PF] | `3310b67bbc4b909c06e9623fe6e0fdc7d4d8fac21093abe25467f5400d61c5a9` | `eb43f176d444c38407937639655ed965e67386c15d48889e68e61fb1eb79575c`; sorted compiled runtime filenames and bytes with NUL separators. |
| `b03-grid` / [GRID] | `d9475f9a38366c72168c33423e2fbe84754883cb7312d9a47d22887c151511e7` | `8110ed30d87ab08fa381b58cf35fb218f61d1d7162dcb52ca2c6d66edb963165`; sorted runtime filenames and bytes with NUL separators. |

The source corpus is the [baseline][BASE], [engine-faithful replica][REPLICA], [core][CORE], [faster-build metadata][FAST], [table/scoring harness][HARNESS], and the two [oracle-probe][PROBE1] [examples][PROBE2]. The exact scoring script hash recorded by the results is `38856d193fa9f8e8a7ca0e43b62778f5d9f7b8a6bc7bf67168843ca1e03c6958`. The result links below retain the full 64-character artifact identities, so the findings and their limitations remain traceable after temporary read inputs are removed.

[FP]: https://api.imd.fun/artifacts/c9ac833b4a6837bf0bd56fc2c4b931ef58d34dc98a000278ee4cec091fb216ee
[VOL]: https://api.imd.fun/artifacts/9f16f7d816edaff1d23de863f4f2149b1823b2842856cb8a0b41f986442226b0
[LAW]: https://api.imd.fun/artifacts/ef182bcb6b8d517b486b508ecf6969451bc7fa7da9ccced5fb76033d19f2117a
[NT]: https://api.imd.fun/artifacts/19a9830766394638451d952df2f20e3a66d25059305d112fe0dd0ec47b7701f1
[FI]: https://api.imd.fun/artifacts/7aef6cf758ba6716bcfcbfa89a011cfc40a1bcadaae5fd3548e572ff96f1e50a
[AUDIT]: https://api.imd.fun/artifacts/5b2315dfcf16f8f0040df6f5db14b27f68e24ebae38b6b15350ee85425d016c0
[PF]: https://api.imd.fun/artifacts/3310b67bbc4b909c06e9623fe6e0fdc7d4d8fac21093abe25467f5400d61c5a9
[GRID]: https://api.imd.fun/artifacts/d9475f9a38366c72168c33423e2fbe84754883cb7312d9a47d22887c151511e7
[TAYLOR]: https://github.com/gtmcknight/amm-sim/tree/4812a6382311624e1506aca131ca35c378f930d9/research/solved
[ENGINE]: https://github.com/benedictbrady/amm-challenge/tree/6b6921f8d463314aa7c96234e1be25a25245f704
[BASE]: https://api.imd.fun/artifacts/1ef80bfb6d6791b877b1f4048a5e63cf2ae54153e6e8763ae3f8ab13132dfb15
[REPLICA]: https://api.imd.fun/artifacts/a1eef2f3dbbcbc7a1de9d15a2b22d1d25ac6d316a72efde67275b5d5a16ab16b
[CORE]: https://api.imd.fun/artifacts/2ad2abf45223c729557e83e77d22de54c5db7da2be0599658144906b91dbf0f7
[FAST]: https://api.imd.fun/artifacts/72b58a1407966f0223f06ab7c6ddd979a24fb4593f1a9b3dc43508a7f133d00b
[HARNESS]: https://api.imd.fun/artifacts/9ad960e6c7e11509b81f2852f7f34d395425adc226141b0bc828ed6f5f344663
[PROBE1]: https://api.imd.fun/artifacts/6c23d23d4a21a37a502bf47a69d9f87b4c7ac84f614f2097e2488c6d5e6dd164
[PROBE2]: https://api.imd.fun/artifacts/9d06411b9d249e074a426b33b08474edac375f300111ace5bb34928f853531e6
