**No improved contract qualified for delivery.** Gain over QLX5 on fresh engine seeds is **unmeasured, n = 0**; there is no corrected contract with measured SE, peak gas, OOG, deployed bytes or source characters. The best correction selected for the prescribed replica report set, `ALL_x0.5`, gained **+0.010583737226753931**, **SE 0.004345614410903885**, on **2,048 seeds, 10000–12047**. Its `advance` is `false`: it missed the +0.03 replica promotion threshold. Solidity, T/F, G and all four fresh-engine items were consequently cancelled before execution. This goal did not establish a new leaderboard score. [t4-join/c, b07-c](https://api.imd.fun/artifacts/850d80bb480592688dfb6906456e51b84f31315944e9976e595bb300b0e0adc3)

| Evidence | Gain over QLX5 | SE | n and seed role | Engine afterSwap peak | OOG | Deployed bytes | Source characters |
|---|---:|---:|---|---:|---:|---:|---:|
| Unchanged QLX5 control | 0 by identity | 0 by identity | 128 screening seeds, 9700000–9700127 | 205,887 | 0 | 22,440 | 47,230 |
| Selected correction, `ALL_x0.5` | +0.010583737226753931 | 0.004345614410903885 | 2,048 replica report seeds | Unmeasured | Unmeasured | Uncompiled | No corrected source produced |
| Selected correction, fresh engine validation | Unmeasured | Unmeasured | 0 | Unmeasured | Unmeasured | Uncompiled | No corrected source produced |

The control figures are the measurements reported by [t2-kit/k, b01-k](https://api.imd.fun/artifacts/fc3bd54c8c987c0ab81c6861e1a6e91c5c3fca757b0f7c114e13a110470c0cde). Its zero gain and zero SE are definitions for the unchanged baseline, not a paired improvement experiment. They cannot be transferred to a corrected contract. The goal history marks this accepted result as source-flagged, without supplying the reason; the figures are therefore identified here as reported control evidence, not independently certified measurements.

**There is no qualifying complete `Strategy.sol` to include.** The objective permits bringing back a contract only after at least +0.04 over QLX5 on 1,024 or more fresh engine seeds, within the gas and size limits. No candidate reached that stage. Supplying an unvalidated corrected contract would bypass that condition. The original QLX5 remains available as `code_zb64.QLX5`, decoded as base64 then zlib, in the [pinned baseline artifact](https://api.imd.fun/artifacts/1ef80bfb6d6791b877b1f4048a5e63cf2ae54153e6e8763ae3f8ab13132dfb15). Its source SHA-256 is `e183e5bc3fb794b7067703b10a7da9920267aa5f4caa968e16ca101b02338f40`. This is the baseline hash carried by the research results, **not the hash of a newly compiled strategy**.

Credit throughout this work belongs to **Taylor (gtmcknight)** for the solved policy in [gtmcknight/amm-sim, research/solved](https://github.com/gtmcknight/amm-sim/tree/4812a6382311624e1506aca131ca35c378f930d9/research/solved), commit `4812a6382311624e1506aca131ca35c378f930d9`. QLX5 adds the exact-arithmetic arb/retail tell, U1 compressed tables and drift-tolerant rival split test specified in the objective. This report covers the new table-value search only. The earlier scalar, rule, compression/refit, belief, residual, rival-tracker and kappa work is not counted as a result of this goal.

The supplied goal history has **`trunk: null`**. All recorded batches were research batches; no code-wave repository or merged trunk commit exists to name. The checking kit is a separate input repository, [identity-md-launches/goal-3178-build-shared-evaluation-kit](https://github.com/identity-md-launches/goal-3178-build-shared-evaluation-kit/tree/45e7563d1a29ffca9d608fdf60c90bf2624d2d01), pinned at `45e7563d1a29ffca9d608fdf60c90bf2624d2d01`. It is not this goal's trunk.

**The surviving edge is small and concentrated in synced retail quotes.** Profiling first located the active tables; finite-difference probes then measured sensitivity, and evolution strategies searched their values. Each node supplies an ask quote in bps, with the bid using the mirrored lookup. Rows represent own mispricing relative to the price belief, on the policy's 5-bps grid with centre 160; columns index the rival-position grid. Stored level indices select uncertainty knots. For tables 1 and 3, indices 0, 1 and 2 correspond to sd 0, 12 and 34 bps; table 0 stores sd 0 and 34 bps. A stored row or column index is distinct from its knot coordinate.

The original QPL1 blob contains **9,172 nodes in 10,160 bytes**. Each stored row has an int16 first value and int8 successive column differences. Its table-specific quantization is part of the feasibility constraint: a continuous search improvement must survive rounding to the existing lattice and the column-difference bounds. The supplied harness validates this layout and supplies the table-use measurements below. [t3-harness/h, b02-h](https://api.imd.fun/artifacts/9ad960e6c7e11509b81f2852f7f34d395425adc226141b0bc828ed6f5f344663)

| Table | Phase | Stored shape, levels × rows × columns | Nodes | Lattice, bps | Lookups on 64000–64127 | Absolute interpolation-weight share by stored level |
|---|---|---|---:|---:|---:|---|
| 0 | Arbitrage | 2 × 24 × 11 | 528 | 0.25 | 977,024 | 99.78%, 0.22% |
| 1 | First retail, synced | 3 × 43 × 30 | 3,870 | 0.5 | 1,286,194 | 39.72%, 59.05%, 1.23% |
| 2 | First retail, unsynced | 4 × 28 × 13 | 1,456 | 0.5 | 0 | No observed weight |
| 3 | Later retail, synced | 3 × 36 × 26 | 2,808 | 1.0 | 522,558 | 40.34%, 58.52%, 1.15% |
| 4 | Later retail, unsynced | 3 × 17 × 10 | 510 | 0.5 | 0 | No observed weight |

The percentages are derived from the harness's absolute weights and rounded independently. These weights measure interpolation participation through active positive clamps; they exclude integer-truncation derivatives and do not measure causal contribution to profit. Tables 2 and 4 were unused on this 128-seed profile, which justified concentrating the search on tables 0, 1 and 3. That observation does not prove they are unreachable on every seed. The active tables contain 7,206 nodes.

The five regional maps covered **162 nonzero-weight groups and 324 signed ±1-bps probes**. Groups were frozen using profile weights before scoring. Probes began at seed 64000, stopped after 128 or 256 seeds when `mean + 2 SE < 0`, or completed 512 seeds through 64511. Derivatives used only the prefix evaluated for both signs. The following are each item's selected diagnostic probe figures, not independent estimates of achievable improvement:

| Map and evidence | Table and stored levels | Groups | Selected probe gain | SE | n |
|---|---|---:|---:|---:|---:|
| [b03-t0](https://api.imd.fun/artifacts/6abcb665394777d6358694762dc54e771cd39eb6c6df3e8a7d25a296149c2fa9) | 0; levels 0, 1 | 20 | +0.00620121374 | 0.00225921834 | 512 |
| [b03-t1a](https://api.imd.fun/artifacts/76220fbfcfea4d93155bb284a0594af40d97f380c0cecdfcb5b32e4797a99952) | 1; levels 0, 1 | 36 | +0.009956 | 0.00518 | 512 |
| [b03-t1b](https://api.imd.fun/artifacts/2b24ff281d6e24d598e91cca66fd33b005ad787037d3bd1d96573baaa1ca727b) | 1; level 2 | 36 | +0.00879878 | 0.00609404 | 512 |
| [b03-t3a](https://api.imd.fun/artifacts/5920796517650e557189a6ddb0dace8e9e0e5017ce9d6146cf420b3f08729a6e) | 3; levels 0, 1 | 36 | +0.009444338311400347 | 0.005068086497079471 | 512 |
| [b03-t3b](https://api.imd.fun/artifacts/043061d7099aa441af5a291d60f8cedeabec97e62e1ab6f4de676234b86667a8) | 3; level 2 | 34 | +0.010079834185175551 | 0.004651306909499757 | 512 |

None reached +0.03. Selection among dozens of probes biases these maxima upward. The strongest effects included losses from raising arbitrage quotes: in table 0, level 0, stored rows 15–23 and column 10, +1 bps gave **−0.182941883, SE 0.0123131016, n = 128** and stopped. The −1-bps direction also lost, **−0.0123906598, SE 0.00488218543, n = 512**. Thus a large finite-difference slope in that corner did not establish a profitable opposite move. Noisy quadratic extrapolations and sums of predicted group gains were not promoted as measured results. [b03-t0](https://api.imd.fun/artifacts/6abcb665394777d6358694762dc54e771cd39eb6c6df3e8a7d25a296149c2fa9)

The history also records exploratory replication checks on 100000–104095: 18 promising band moves failed to yield a robust gain, and a wider set of probes suggested a cusp near QLX5 rather than a smooth quadratic optimum. Those are orchestrator notes, without a separately handed per-seed dataset, so the conclusions here rest on the worker results. The notes' estimate that this encoding might hold only +0.01 to +0.02 is a local-search hypothesis, not a proven upper bound.

**Evolution strategies retained two nonzero parts.** Five items searched additive corrections from six row bands and five column bands per selected level. Training used slices within 200000–263999; realised, lattice-rounded candidates were selected on VALID 300000–304095. A nonzero candidate needed VALID mean minus one SE above zero. The retained correction was then evaluated on CHOOSE 64000–65023. Training schedules differed by item; they were finite searches, and the table-3 level-0 item completed 12 generations and 36,416 total simulations, below the approximately 100,000 suggested simulations. No ES item evaluated the report set.

| Part and evidence | Search scope | Retained correction | VALID gain; SE, n = 4,096 | CHOOSE gain; SE, n = 1,024 |
|---|---|---|---|---|
| [e0, b04-e0](https://api.imd.fun/artifacts/725e2ab18c208bf050e531c803097ce2e529d5cbc8d7a9e34f5a3c0f97c81cbc) | Table 0, levels 0, 1 | Zero | 0; 0, identity | 0; 0, identity |
| [e1, b04-e1](https://api.imd.fun/artifacts/3ac01b67d17cc28bddb3e9cda0c1228ab18cc379beaa5223104bf5d7a7ff0d7a) | Table 1, level 0 | Zero | 0; 0, identity | 0; 0, identity |
| [e2, b04-e2](https://api.imd.fun/artifacts/cd6d422ff7bdc14aeb730ff108e994dc641a86c66f769605fd3973d29cca0809) | Table 1, levels 1, 2 | ES mean × 1.5; 1,037 nodes | +0.010857; 0.003099 | +0.009264; 0.006311 |
| [e3, b04-e3](https://api.imd.fun/artifacts/0d356ac9e057e6a6c2f99ad4cc1d9e17743612796cc7311b28145a710c9974b5) | Table 3, level 0 | Zero | 0; 0, identity | 0; 0, identity |
| [e4, b04-e4](https://api.imd.fun/artifacts/88eb6d452ae55eb2dc1eb7c162933834f97b734b8481c99c5080b28398426686) | Table 3, levels 1, 2 | ES mean; 356 nodes | +0.007227; 0.002336 | −0.000248; 0.004883 |

The zero rows mean the selection retained unchanged QLX5; they do not establish zero attainable gain in those regions. In particular, e0 and e3 recorded identity results without additional redundant CHOOSE simulations. VALID selected among multiple candidates, so its displayed gains are optimistic. CHOOSE was subsequently used again by the join, so it is also selection data for the final candidate. The ES `advance: true` fields indicate completed work and controls, not passage of the +0.03 promotion bar.

The join considered ALL, GOOD, STRONG, individual nonzero parts, and applicable half-scale variants. GOOD and e2 had identical realised tables and shared one evaluation; STRONG was the unchanged baseline. Seven named candidates represented six distinct QPL1 blobs. On all 1,024 CHOOSE seeds, selecting by mean minus one SE chose **`ALL_x0.5`**, combining e2 and e4. Its CHOOSE gain was **+0.015848864107881888, SE 0.006185333863149532**. The full-scale ALL combination gave +0.014463191691167332, SE 0.006851785636583938. These alternatives were not separately run on REPORT. [b07-c](https://api.imd.fun/artifacts/850d80bb480592688dfb6906456e51b84f31315944e9976e595bb300b0e0adc3)

The selected correction changes **1,393 nodes**, all in table 1 or 3 at stored level 1 or 2. The half-scale operation rounds to the existing lattice, with exact half ties away from zero; it therefore does not halve every realised node change. After rounding, the full selected delta has this distribution:

| Table | Stored level and sd | Realised node correction | Nodes changed |
|---|---|---:|---:|
| 1 | 1; 12 bps | +0.5 bps | 806 |
| 1 | 1; 12 bps | −0.5 bps | 32 |
| 1 | 2; 34 bps | +0.5 bps | 104 |
| 1 | 2; 34 bps | −0.5 bps | 95 |
| 3 | 1; 12 bps | +1.0 bps | 188 |
| 3 | 2; 34 bps | +1.0 bps | 57 |
| 3 | 2; 34 bps | −1.0 bps | 111 |

These counts were independently decoded from the supplied delta for this write-up. They locate the changes, not an ablation-based allocation of the joint gain. In particular, e4 alone was indistinguishable from zero on CHOOSE, and no report-set ablation separates the two parts. Most profile weight lies at the middle sd knot; the changes at the highest sd knot are weakly identified.

The complete research correction remains in `delta_zb64` of [b07-c](https://api.imd.fun/artifacts/850d80bb480592688dfb6906456e51b84f31315944e9976e595bb300b0e0adc3). Its reproducible identities are:

| Object | SHA-256 |
|---|---|
| Exact decoded selected delta bytes, including Taylor credit line | `e78bd0551ad7275d4ab59735c02a692dd61626e6975d52d68533b221b44dc7d8` |
| Corrected 10,160-byte QPL1 blob | `b5fe4ab5049eb177c7a07cd4716cef7b936135c1ef7c55578328b673dd6f26ae` |
| Original QPL1 blob | `830868f9b3e5ad162c4f2070e6faed0782c7b4cc308ab69044b2cf7306f68099` |

The delta decodes as UTF-8 lines `table level row column millibps`, with indices into stored knots and a leading attribution comment. This write-up independently applied the nonzero records to the original nodes, checked lattice divisibility and index uniqueness, re-encoded int16 row starts and int8 column differences, and obtained the supplied corrected QPL1 hash. That verifies the research payload's encoding; it is not gate T on a Solidity source file.

On REPORT, the selected candidate's upper two-SE value is **0.0192749660485617**, below +0.03. The lower two-SE value is **0.001892508404946161**. These describe the paired sample uncertainty; they do not certify engine behavior. All 2,048 prescribed report seeds were completed. The result's `bar_check.early_stop: true` records the stop-rule outcome after that full evaluation, not a partial-window report. Only one candidate was evaluated on REPORT, and `report_looks` is 1. [b07-c](https://api.imd.fun/artifacts/850d80bb480592688dfb6906456e51b84f31315944e9976e595bb300b0e0adc3)

**Independent shape scans point to similar retail regions, but gains do not add.** These items used SCAN 400000–402047 and CONFIRM 410000–418191. A direction needed SCAN mean minus one SE above zero to receive all 8,192 CONFIRM seeds; a confirmed step needed CONFIRM mean minus two SE above zero. The same CONFIRM set selected components and evaluated their sum, so the sums are not fresh holdout results and the thresholds are unadjusted for multiple comparisons.

| Shape item and evidence | Signed SCAN steps | Steps evaluated on CONFIRM | Steps passing confirmation | Reported selected sum or outcome |
|---|---:|---:|---:|---|
| [g0, b05-g0](https://api.imd.fun/artifacts/07ab8a91d49490ad5c8d1981cdfd851ecf9a48c8243be507ac2d1024e11b8152) | 28 | 2 | 0 | No selected correction; top-level n = 0 is a sentinel |
| [g1, b05-g1](https://api.imd.fun/artifacts/1dafaba90a3fec5cca9a93542ff4e9168ce84682a84d4e0bbb8bb92d3cd26479) | 40 | 6 | 3 | +0.009470, SE 0.002293, n = 8,192 |
| [g3, b05-g3](https://api.imd.fun/artifacts/2c1d4cad4f607023e888459e413e7acaa633ddb6c39d79a6d39b269fe175b166) | 40 | 8 | 3 | −0.0037246891742434077, SE 0.0024793991244888842, n = 8,192 |

In **table 1 at sd 12 bps**, adding **+0.5 bps to rows with knot coordinate below 160** gave **+0.008361, SE 0.001769** on CONFIRM. Adding +0.5 bps to the lower contiguous column half, stored columns 0–10, gave **+0.006895, SE 0.001738**. A small row shift, explicitly `new(x) = old(x − 0.05)`, gave **+0.002453, SE 0.001137**. Their overlapping sum yielded only +0.009470, not the sum of the three individual gains. [b05-g1](https://api.imd.fun/artifacts/1dafaba90a3fec5cca9a93542ff4e9168ce84682a84d4e0bbb8bb92d3cd26479)

In **table 3 at sd 12 bps**, a +1-bps move on the lower-row half gave **+0.007595005668813076, SE 0.0018718072937946018**; the lower-column-half move gave **+0.0055403389695311556, SE 0.0017468496345722155**. The row shift defined by that item as `new(x) = old(x − 0.1)` gave **+0.003084743520298333, SE 0.0012230989681779481**. Despite all three passing individual confirmation, their sum lost −0.0037246891742434077. The worker's shift sign convention differs from g1's parameter convention; the formulas here state the actual transformation. [b05-g3](https://api.imd.fun/artifacts/2c1d4cad4f607023e888459e413e7acaa633ddb6c39d79a6d39b269fe175b166)

These findings support modest upward corrections to some middle-uncertainty retail quotes. They also directly demonstrate why separately positive moves cannot be added as independent gains. The scans cover a finite set of offsets, halves, scales, shifts and tilts. Some diagnostic scale moves failed the int8 column-difference constraint and were explicitly marked unencodable; their replica scores are not deployable candidates. Neither the shape results nor their “bound” labels prove a bound on all possible table corrections.

**Single-node scans found no confirmed improvement within the completed coverage.** Each item ranked 24 nodes by profile weight, then tested ± one lattice unit. Retained signed steps received 2,048 SCAN seeds, 500000–502047, and qualifying signs received 8,192 CONFIRM seeds, 510000–518191. Time limits reduced the coverage as shown:

| Node item and evidence | Lattice step | Nodes fully retained / planned | Signed SCAN steps retained | CONFIRM evaluations | Confirmed improving steps |
|---|---:|---:|---:|---:|---:|
| [n0, b06-n0](https://api.imd.fun/artifacts/a1a32621ba913dea97cb5cfeb6eb549727a15f818b9ae3ac7ac3f34fcab430ef) | 0.25 bps | 20 / 24 | 40 | 8 | 0 |
| [n1, b06-n1](https://api.imd.fun/artifacts/5151a34236014e75caf064179614c4611c6370d9bf0e182fc0ac097cbfa034ae) | 0.5 bps | 20 / 24 | 40 | 11 | 0 |
| [n3, b06-n3](https://api.imd.fun/artifacts/cce76a9ed02c9ca13e024a59956817534d4bfcf9f7c9d97044911e107a47a769) | 1.0 bps | 4 / 24 | 8 | 1 | 0 |

Ranks 21–24 were dropped in n0 and n1; ranks 5–24 were dropped in n3. Thus **44 of the planned 72 nodes** have the completed retained protocol, not all 72. Zero top-level gain, SE and n in these items are no-selection sentinels, not measured exact zero effects and not absence of all underlying evaluations. Table 1's best CONFIRM single-node result was only +0.000918, SE 0.000955. Table 3 included a reproducible −8.472212749756068 paired outlier on one SCAN seed; it remained in the statistics. These scans leave unsampled nodes and coordinated node moves unresolved. [b06-n1](https://api.imd.fun/artifacts/5151a34236014e75caf064179614c4611c6370d9bf0e182fc0ac097cbfa034ae), [b06-n3](https://api.imd.fun/artifacts/cce76a9ed02c9ca13e024a59956817534d4bfcf9f7c9d97044911e107a47a769)

**The validation pipeline was gated off, not passed.** The objective named T, F and G without defining them; the orchestrator supplied the operational definitions below in the goal notes. They are recorded as that interpretation, not as additional requester-supplied definitions.

| Stage | Required evidence | Actual outcome |
|---|---|---|
| Replica promotion | Gain ≥ +0.03 on all 2,048 REPORT seeds | Failed: +0.010583737226753931; `advance=false` |
| Solidity and T | Fit corrected tables in existing encoding; all 9,172 decoded nodes equal base plus correction; only QPL literal and one comment line change | `t4-sol/c` cancelled; no corrected source |
| T/F against Python | Independent table decode; every callback's two fees equal the Python reference on 9700000–9700003, with unchanged QLX5 control | `t4-tf/c` cancelled; no candidate replay |
| G | Engine screening 9700000–9700127: source ≤ 50,000 characters, runtime ≤ 24,576 bytes, afterSwap peak ≤ 245,000, zero OOG and failed callbacks | `t4-gas/c` cancelled; no candidate gas or size measurements |
| Fresh engine | Four disjoint 256-seed blocks against QLX5; stop checks after 128 when mean + 2 SE < +0.04 | Four `t4-engine` items cancelled; zero fresh seeds consumed |
| Return a contract | Pooled gain ≥ +0.04 on ≥ 1,024 actually completed fresh engine seeds, limits satisfied | Not reached; notes also required pooled mean − 2 SE > 0 |

The supplied history records **19 accepted research items** and **7 downstream items cancelled by dependencies**: one Solidity, one T/F, one G and four engine items. Every recorded batch contains at most five items and specifies `platform: [linux-x64]`, `minCpus: 8`. Mapping and the candidate validation stages have checks on `advance=true`; the join waits for the ES batch to settle. Early proposed pipelines in episodes 1 and 2 were refused and never executed, apart from the separately accepted kit work. Their projected item counts and reserved seeds must not be counted as completed experiments.

Each available batch brief excerpt starts with one item's bounded task. The supplied history truncates each brief to an excerpt, so it cannot support a fresh certification of every original output-schema clause, filled-template length or full hash in those briefs. No orchestration decisions file was supplied for this final write-up, and this assignment names only `report.md` as an output. The state and result fields, rather than invented replacement decisions, are the basis of the stage audit above.

The harness's numerical controls are useful but narrower than candidate validation. Its archived-engine comparison covered **512 seeds, 10010512–10011023**, with mean error **−1.7222758774693148e−09** and maximum absolute error **4.994752202946984e−07**, within the archived rows' six-decimal precision. Zero deltas preserved scores and instrumentation was neutral; QPL1 roundtripped byte-for-byte. This does not establish callback bit identity for every candidate. Earlier episode notes reported floating-point sensitivity in another build, further supporting the requirement for candidate-specific F and engine checks. [b02-h](https://api.imd.fun/artifacts/9ad960e6c7e11509b81f2852f7f34d395425adc226141b0bc828ed6f5f344663)

The baseline kit reported **43,721 callbacks across four replay seeds**, with zero fee mismatches and failed calls, and port edge equal to engine edge on those four seeds. Its 128 screening seeds reported zero OOG or failures and 1,377,819 Submission afterSwap calls. The compiler configuration was solc 0.8.24, optimizer 200, viaIR, Paris; QLX5 runtime SHA-256 was `903a0cf860910022916e7c16aa1ffcfb94b0db9e25074665947d786615a44ae8`. These are baseline controls only. The source-flag caveat noted above remains. [b01-k](https://api.imd.fun/artifacts/fc3bd54c8c987c0ab81c6861e1a6e91c5c3fca757b0f7c114e13a110470c0cde)

There was one payload defect that did not affect the selected nonzero correction: e0, e1 and e3 declared `nonzero=false`, but their compressed delta fields fail zlib decoding with an incomplete-stream error. The join excluded them and did not invent substitute deltas. The e2, e4 and joined deltas decode successfully and match their declared hashes. That distinction was reproduced during this write-up. The broken zero payloads would need repair if reusing those records as executable inputs. [b07-c input audit](https://api.imd.fun/artifacts/850d80bb480592688dfb6906456e51b84f31315944e9976e595bb300b0e0adc3)

**Seed accounting preserves the difference between search, report and engine evidence.** Gains are paired candidate-minus-QLX5 differences on identical seeds. SE means the sample standard deviation of those differences divided by √n; it is not the standard error of unpaired strategy levels. Repeated selection and correlated probes are not additional independent confirmations.

| Seed range, inclusive | Purpose and use |
|---|---|
| 64000–64127 | Baseline visit profile; reused within CHOOSE |
| 64000–64511 | Regional-map probes, including shorter stopped prefixes |
| 64000–65023 | Final CHOOSE set for ES parts and joined alternatives; selection data |
| 10000–12047 | One complete REPORT evaluation of `ALL_x0.5`; 2,048 seeds, one look |
| 100000–104095 | Exploratory checks recorded in episode-4 notes; no new run in this write-up |
| Within 200000–263999 | ES training pools; individual schedules used subsets, not the entire 64,000-seed pool |
| 300000–304095 | ES VALID selection, 4,096 seeds per evaluated candidate |
| 400000–402047 / 410000–418191 | Shape SCAN / CONFIRM; sum evaluation reused CONFIRM |
| 500000–502047 / 510000–518191 | Node SCAN / CONFIRM for retained nodes and selected signs |
| 9700000–9700127 | Unchanged QLX5 engine screening; first four also used for replay; not fresh gain validation |
| 10010512–10011023 | Archived-engine parity fixture; no new engine runs by the harness |
| 10400000–10400255 | Planned fresh engine block 0; unused |
| 10400256–10400511 | Planned fresh engine block 1; unused |
| 10400512–10400767 | Planned fresh engine block 2; unused |
| 10400768–10401023 | Planned fresh engine block 3; unused |

The next unspent fresh-engine allocation therefore still begins at **10,400,000**. The one-used REPORT set should be labelled as such in any later work. A later candidate selected in response to this report would make any reuse an additional look, not an untouched holdout.

**What remains between this work and #1 is at least the unclosed pinned score gap and the entire candidate engine proof.** The objective pins QLX5 at 528.3333 and the target at 528.452, a difference of **0.1187**. Those are assignment-time figures, not a live leaderboard check. This goal established no board gain, so its evidenced board gap remains 0.1187; exceeding the named leader would require slightly more, subject to displayed-score rounding.

For scale only, if the replica point estimate transferred unchanged to the board, adding +0.010583737226753931 would give about **528.343884**, still **0.10811626277324607** short of the pinned target. This is arithmetic, not a validated score prediction: the exact engine-to-board transfer premise applies to engine gains, and this correction has no engine gain measurement. It also sits **0.01941626277324607 below the replica promotion bar**, before the separate +0.04 fresh-engine requirement.

The supported conclusion is that the completed direct-value search found a small gain, centred on middle-uncertainty synced retail regions, and did not meet the objective. It did not exhaust all table-value possibilities. Finer row-column interactions, coordinated lattice moves and the omitted node coverage remain unresolved; the failed sums caution against simply combining individually positive changes. Any continuation within the permitted line should freeze a newly encodable candidate using selection data, disclose additional report looks, and meet the same replica gate before Solidity, T/F, G and four fresh engine blocks. The previously spent scalar, rule, belief, residual, rival and kappa lines remain outside this goal. No submission was made; the requester must ask the user before any future leaderboard submission.

**Write-up checks and reproducibility.** All 19 supplied result files matched the full SHA-256 identifiers in the assignment; the result links in this report use those identifiers. Each contained the required common fields and the original QLX5 source hash. The baseline result contained engine gas and OOG fields. The harness's decoded implementation, dependency and archived-row payload hashes were verified; its implementation hash is `4d4894474104eac9148e52b18d679b994ce73c6a889bafa18169c8dacca22855` and dependency hash is `a992fd6855d568b6fbb163423e9dd6ea7c4709b7475d343079c667edeceb9c00`. The credited source assets are retained inside [b02-h](https://api.imd.fun/artifacts/9ad960e6c7e11509b81f2852f7f34d395425adc226141b0bc828ed6f5f344663), with their README and codec API.

For this report, the public baseline artifact was also fetched and its artifact hash, decoded QLX5 source hash, 47,230-character length and original QPL1 hash independently verified. An independent decoder checked the original QPL1 roundtrip, the two nonzero ES deltas and the selected joined blob. Arithmetic checks verified the stop threshold, CHOOSE selection, node counts, map group counts, the baseline's 128 contiguous rows and recorded peak, and the seven cancelled stages. No new simulation, compiler run, Solidity replay, gas test or leaderboard action was performed. The handed join record has aggregate report statistics and the full delta, but no report per-seed rows; its reported gain and SE were not independently recomputed. Local hash, encoding, arithmetic and Markdown/size checks support faithful reporting, and do not independently certify strategy behavior.
