**+6.1996704634 over IB, SE 0.0448608322, on 1,664 fresh engine seeds.** The best measured contract is **T1ArbTell (T1)**. Its measured afterSwap peak is **208,330 gas**; all **18,033,745** submission afterSwap calls succeeded, with **0 OutOfGas and 0 reverts**, and all reported validation checks passed. Its Solidity source SHA-256 is `6ee77c053e29d23a89b926c33b13e32365bdd09d880cac5557ce06c043dcf1ac`; its code-bearing result ID is [`6b308b7219a0cf0bab1e5168e2f2b94b68bc6c118ae09a6d5ca30ea0173638ff`][t1]. That result's declared `code_sha256` is `70b4efee30b245afbfe6e277c802bfbd7d2f3289f4aeba850d9203c6f59ff267`, hashing the base64 text. These figures combine the 128-seed pilot and six disjoint 256-seed confirmation results, checked here against their recorded rows and gas counters. [Pilot][pilot], [E1][e1], [E2][e2], [E3][e3], [E4][e4], [E5][e5], [E6][e6].

The five worst T1-minus-IB pairs are:

| Engine seed | Paired gain |
|---:|---:|
| 12011003 | +1.7639315976611556 |
| 12013317 | +1.8181306018170744 |
| 12013239 | +1.9297408804256406 |
| 12009988 | +1.9570113826996476 |
| 12013797 | +2.2600429370430106 |

T1 exceeds the **+2.7 mean-gain threshold by 3.499670**, but **does not complete its required 4,000-seed test**: 2,336 observations are missing. Its point estimate is **0.200330 below +6.4**; a normal-approximation 95% interval is [6.111743, 6.287598]. **First place was not established, and this goal entered nothing.** The strongest contract that completed the earlier 4,000-seed milestone is **M09**, at **+3.8055818877, SE 0.0225973589, n=4,352**, afterSwap peak **219,533**, zero reported faults. T1 also has a material parity qualification: it passes an independently checked applied-WAD numerical comparison, but fails equality with autonomous ideal-double trajectories. Details appear below. [R4][r4], [R5][r5], [R6][r6], [Audit 1][au1], [Audit 2][au2]; goal notes, episodes 9–10.

This is an evidence synthesis, dated 2026-11-10. No new simulation, compilation, board fetch, or submission was performed for this report. Arithmetic recomputation and static inspection of existing artifacts are distinguished from workers' experimental measurements. All gains are edge differences, not basis points; basis points below measure fee or price error. Paired engine gains do not establish board scores or ranks.

**Track B: ranked ledger of the ideas tried**

The main ledger ranks complete **2,048-seed holdouts on replica seeds 10000..12047** by gain over `ref/lattice_qm.json`. Parentheses contain paired SE. “Increment” identifies the appropriate fresh control, so inherited gains are not credited to a new idea. `thr09` means the lattice policy with its phase/rival arb-call threshold changed to 0.9; its complete-holdout advantage is **+0.3228919198 (0.0106915999)**. `TG` means TellGauss. Misread is the percentage of first own trades classified incorrectly; price error is callback-weighted RMS log-price error in bps. A changed threshold changes the meaning of the classification diagnostic: thr09 earns more despite about 29% misreads versus the original lattice's 16.22%.

Every gas figure in the B ledger is **an unmeasured incremental estimate or operation count**, unless explicitly identified as a later A measurement. An estimate of zero means no additional algorithmic operation, not measured equal EVM gas. `NR` means the handed evidence does not retain the requested number; it does not mean zero. Duplicate implementations on the same seeds are shown together and never add statistical observations. Sources in each row identify the root merge and original item, or the directly handed JSON.

| Rank | Idea / result | Gain vs lattice (SE) | Increment / conclusion | Misread %; price RMS bps | Gas estimate / feasibility |
|---:|---|---:|---|---|---|
| 1 | Post-tell rival-only order propagation, frozen Q=1, NMAX=2; [rival-1][rival] | **+2.815168 (.022661)** | **+.118987 (.010619) vs TG**; positive, below +.3; not ported | .065011; 7.114822 | +15–30k average; roughly .8–1.6M at long gaps; no feasible worst-case port demonstrated |
| 2 | TellLattice, `b9-tell-latt/tl-1`; [R5][r5] | **+2.707278 (.020712)** | +.011098 (.004147) vs TG; lattice adds little after the tell | .051059; 7.160079 | O(1) tell plus 121 cells, 33-tap diffusion; numerical gas NR; direct lattice exceeds budget |
| 3 | Sigma learned causally from tell pins, K0=2000; [sigma-1][sigma] | **+2.700377 (.020864)** | +.001864 (.003499) vs its local TG; null | .064662; 7.203290 | Four state words, potentially two packed slots; source's 1–2k pin arithmetic estimate omits potentially larger storage cost |
| 4 | Fixed log-drift correction, −sigma²/2; [fresh-2][drift] | **+2.698152 (.020813)** | +.001971 (.002622) vs TG; null | .064336; 7.207132 | +3–300, at most 13 subtractions; zero new slots |
| 5 | **Reserve-grid tell, Gaussian**, `b9-tell-gauss/tg-1,tg-2`; [R5][r5] | **+2.696180 (.020862)** | +3.191081 (.022113) vs Gaussian/QM; −.025757 (.002724) vs true-flag diagnostic; transferred to T1 | .065249; 7.207864 | O(1), no dynamic state; tg-1 guessed +300–1,500, tg-2 declined a numerical EVM estimate; actual T1 gas is in A |
| 6 | Tell with information weight κ=3e-5, `kap-3e5`; [R6][r6] | **about +1.9845, derived; SE NR** | −.7117 (.0134) vs TG; tighter quotes buy pins at excessive cost | NR; 6.40 | Table-only change; structural extra operations zero, EVM unmeasured |
| 7 | Survivor-mass repair of RivalT, `b8-rival-mass/mass8-1`; [R5][r5] | **+.538062 (.014747)** | +.215170 (.011931) vs thr09; repair-alone holdout contrast unavailable | 28.058964; 13.017707 | Repair ≤54 adds and 12 rescalings/kernel; 222 is only an opcode subtotal, not total gas |
| 8 | Rival-only transition on joint K1, original accounting, `rival7-1`; [R5][r5] | **+.531304 (.014847)** | +.208412 (.012083) vs thr09; new transition vs K1 about +.128585, derived mean, SE NR; later accounting repair required | 28.036559; 13.011308 | About 200k/kernel, up to 31 kernels; unsuitable directly |
| 9 | Joint price/rival first-fill router likelihood, K=1, `joint-1`; [R4][r4] | **+.4027 (.0116)** | +.079828 (.008845) vs thr09; K=2/4/8 persistence added no useful gain | 27.82; 13.119 | +60–400k; unported |
| 10 | Empirical retail fill-law KDE, h=.2, `fresh5-2`; [R4][r4] | **+.3531 (.0104)** | +.0302 (.0057) vs thr09; below transfer bar | 28.83; 13.236 | −200 to +400 |
| 11 | Posterior-integrated rival-band projection, `fresh5-1`; [R4][r4] | **+.3407 (.0113)** | +.017789 (.005253) vs thr09; small | NR; NR | +130–650k |
| 12 | Commit quoting to a hypothesis, q=.9, `fresh6-1`; [R4][r4] | **+.3346 (.0115)** | +.0117 (.0063) vs thr09; null | 28.57; 13.288 | +15–45k |
| 13 | Separate ask/bid tail-risk SDs, strength .25, `tails7-1`; [R5][r5] | **+.331662 (.011111)** | +.008770 (.005523) vs thr09; null | 28.807108; 13.215200 | Lattice moment pass; hypothetical two-Gaussian reduction +15–60k, not implemented |
| 14 | Ambiguity-aware IG2 tables, `ig8-1,ig8-2`; [R5][r5] | **+.327467 (.011247)** | +.004575 (.006958) vs thr09; identical duplicate holdouts | 28.557021; 13.233911 | Offline table change; zero structural callback increment |
| 15 | Integer-cell recentering, `fresh7-2`; [R5][r5] | **+.324044 (.010633)** | +.001152 (.003015) vs thr09; null, finite-window clipping persists | 28.940211; 13.280236 | −2,000 to +100 per recenter; excludes lattice cost |
| 16 | Prior-SD-dependent call cut (.82/.90/.95), `cutfn-1`; [R3][r3] | **+.323112 (.010851)** | +.000220 (.003309) vs constant thr09; retain constant | 30.487617; 13.262648 | Numerical gas NR; comparisons only |
| 17 | **Cost-sensitive call threshold .9**, `fresh3-1`; [R3][r3] | **+.322892 (.010692)** | Replaces .5 only for phase/rival decision; transferred to A | 28.883401; 13.277153 | About zero: replace one comparison constant |
| 18 | Same-step retail-fill conditioning, strength .1, `same-step`; [R4][r4] | **+.3221 (.0107)** | −.000837 (.000719) vs thr09; null | NR; NR | About 4.3M in naive cost model |
| 19 | Silent-step no-fill weighting, k=1, `fresh8-2`; [R5][r5] | **+.320131 (.010882)** | −.002761 (.003350) vs thr09; null | 28.899641; 13.279331 | 1,500–3,000/cell/silent step; one packed reserve slot; several gaps exceed budget |
| 20 | Posterior third-moment quote-centre shift, α=−.025, `fresh4-2`; [R3][r3] | **+.3175 (.0111)** | −.0054 (.0056) vs thr09; no gain | 28.898325; 13.237383 | One extra pass over ≤121 cells; numerical gas NR |
| 21 | Matched-Gaussian action-value control, `values7-2`; [R5][r5] | **+.313647 (.010773)** | −.009245 (.003251) vs thr09; negative control for posterior integration | 28.883126; 13.266079 | Shared nine-action/five-node value machinery; no EVM measurement |
| 22 | Belief-mixture temperature T=.9, `fresh4-1`; [R3][r3] | **+.302433 (.011609)** | −.020459 (.007480) vs thr09; sharpening/softening failed | 28.384294; 13.335754 | Two powers per ambiguous callback; zero new slots; numerical gas NR |
| 23 | Fork-trained continuation-value fee residual, η=.25, cap 1 bp, `value-residual`; [R4][r4] | **+.2992 (.0115)** | −.0237 (.0076) vs thr09; negative | NR; NR | +2–4k |
| 24 | Reserve-depth impact-unit rescaling, `fresh8-1`; [R5][r5] | **+.273642 (.011737)** | −.049250 (.008900) vs thr09; rejects this scaling formula | 28.914065; 13.308119 | +15–45k; zero new slots |
| 25 | Threshold .9 on unbounded two-Gaussian policy, `thr-mix2`; [R3][r3] | **+.260476 (.011536)** | +.327522 (.010431) vs mix05; +.755376 vs Gaussian; transferred as M09 threshold | 29.089191; 13.367387 | About zero above mixture |
| 26 | Posterior-integrated nine-action shortlist, `values7-2`; [R5][r5] | **+.235256 (.012417)** | −.087636 (.007795) vs thr09; −.078391 (.007673) vs matched-Gaussian control | 29.051613; 13.081342 | +120k–2M illustrative; 527 MB value arrays; direct port infeasible |
| 27 | Lattice branch/rival log-quote blend, g=2, `blend-tune`; [R2][r2] | **+.2231 (.0112)** | Below +.3; rival blend increment about .03–.045 in tuning/confirmation | 16.02; 13.59 | +25–35k on ambiguous calls; zero new slots |
| 28 | Fresh branch blend, g=2, `b1-fresh/fresh-2`; [R1][r1] | **+.1834 (.0107)** | Below +.3; superseded by later blend tests | NR; NR | +20–30k on ambiguous calls |
| 29 | Fresh branch blend, q=π, `b1-fresh/fresh-1`; [R1][r1] | **+.1336 (.0118)** | Below +.3; gain from quotes, not improved classification | NR; NR | +15–25k on ambiguous calls |
| 30 | Later branch revision plus blend, g=1.5, `br-1`; [R3][r3] | **+.118168 (.011410)** | Below +.3; revised rival/phase not enough | 15.852914; 13.563984 | About +450k warm; 128 extra naive slots |
| 31 | RouterEvidence posterior update, `b1-fresh/fresh-3`; [R1][r1] | **+.08919 (.01041)** | Below +.3; expensive | 15.9388; 13.5467 | +.3–1.5M on first calls |
| 32 | Trained logistic correction, `idea-trained`; [R1][r1] | **+.0227 (.0080)** | No useful unexploited calibration in tested features | NR; NR | +4–6k on first calls |
| 33 | Per-run rho/sigma adaptation, `idea-perrun`; [R1][r1] | **+.022491 (.007481)** | Below +.3 | 16.1937; 13.6307 | Estimate mentioned, numerical value NR |
| 34 | Post-tell price-belief truncation by inferred rival band, [fresh-1][band] | **+.010113 (.024085)** | **−2.686067 (.016580) vs TG**; clear dead end despite positive reference total | .976414; 10.542810 | Extra truncated-normal update and second lookup; zero new slots; numerical gas NR |
| 35 | Finer .625-bps belief lattice, `fresh2-1,fresh2-2`; [R2][r2] | **+.001906 (.004042)** | Same selected policy/measurements, count once; no useful gain | 16.213741; 13.640884 | About +3M/diffusion naive; +360 cells |
| 36 | Persistent two-Gaussian belief, floor 1e-5, `mix2-1`; [R3][r3] | **−.0670 (.0089)** | **+.4279 (.0125) vs Gaussian/QM**; useful affordable substitute for lattice, transferred to A | 16.377757; 13.747042 | +20–60k and three extra slots estimated; bounded ports measured later |
| 37 | Gaussian threshold .85, `thr-gauss`; [R3][r3] | **−.104439 (.014045)** | +.390458 (.010481) vs fresh Gaussian; already subsumed by stronger mixture transfer | 27.216792; 14.023488 | One constant comparison; numerical gas NR |
| 38 | Gaussian blend plus threshold .9, `thr-blend`; [R3][r3] | **−.115364 (.013707)** | +.060250 (.006910) vs blend; overlaps existing gain | 30.0595; 14.2980 | About zero above blend |
| 39 | **Gaussian branch blend g=1.5**, `blend-gauss`; [R2][r2] | **−.175614, derived mean; SE NR** | **+.319286 (.010933) vs Gaussian/QM**, transferred to PB; did not beat lattice | 16.960624; 14.337321 | +15–35k on ambiguous callbacks; no new slots |
| 40 | Two-reading action-value search, `qm2h-1`; [R3][r3] | **−.2531 (.0139)** | +.2418 (.0110) vs Gaussian; failed its endpoint/table gate | 16.98; 14.12 | 260 MB values plus 2-D search; unported, numerical gas NR |
| 41 | Midpoint information probe, `probe-2`; [R4][r4] | **−.3451 (.0142)** | −.668020 (.010654) vs thr09; better RMS bought at excessive edge cost | Within reported 29.49–29.72%; about 12.84 | Numerical gas NR; naive lattice about 135 slots |
| 42 | Depth-3 information-seeking quote probe, `probe-1`; [R4][r4] | **−.3496 (.0136)** | −.672513 (.010320) vs thr09; negative | Within reported 29.49–29.72%; about 12.95 | Numerical gas NR; naive lattice about 135 slots |
| 43 | Whole-posterior reweight/search, `idea-posterior`; [R1][r1] | **−2.8664 (.0236)** | Worse; price error rose | Exact rate NR; exact RMS NR | About 48,400 posterior contributions/callback plus lattice; unsuitable |
| 44 | Tell with κ=1e-4 tables, `kap-1e4`; [R6][r6] | **about −7.4003, derived; SE NR** | −10.096526 (.042768) vs TG; much tighter quotes lose heavily | About .045; 4.29 | Table-only change; structural extra operations zero, EVM unmeasured |

Rows marked “derived” use same-seed differences of reported means only. For Gaussian blend, Gaussian minus lattice is −.4949005408, giving .3192861667−.4949005408=−.1756143741. The κ totals similarly add the inherited TG mean; their direct lattice paired SE was not retained in R6. SEs cannot be added or subtracted without paired covariance. Rankings within a few hundredths are descriptive, not significance claims. Sigma's local TG control differs by about .00233 from the other TG implementations; its incremental gain remains null. The worker attributes this to its Python build without establishing the cause. [R2][r2], [R5][r5], [R6][r6], [sigma-1][sigma].

The distinction between total and incremental gains changes the conclusions. The best post-tell B candidate, TellRival, gains only **+.118987** over TG; adding it to T1 was never measured. The large gains transferred earlier were Gaussian blend, persistent mixture, the cost-sensitive threshold, and finally the tell. The first two crossed +.3 against their Gaussian controls while still underperforming the lattice reference. M09 retains a bounded mixture and threshold, rather than stacking blend and mixture; blend on the mixture was worse in tuning. After TG, no completed new idea cleared +.3 incrementally. [R2][r2], [R3][r3], [R5][r5], [rival-1][rival].

**Partial, failed, diagnostic, and infrastructure B work**

These entries are outside the complete-holdout ranking. Missing runs are not filled, and overlapping copies are not pooled.

| Item / idea | What was actually measured | Misread / price error / gas | Disposition |
|---|---|---|---|
| `idea-router`, router-conditioned likelihood; [R1][r1] | n=512, +.000151 (.000179) vs lattice; selected α=0, preserving base; nonzero strength harmed an eight-seed probe | Candidate diagnostics and gas value NR | Remaining 1,536 holdout seeds unmeasured; no new policy gain |
| `b2-revise/revise-1`, retain/revise branch states; [R2][r2] | n=256, 10000..10255: +.0792 (.0228) vs lattice; 64 tuning and 64 confirmation seeds | Retrospective labels 13.02%, first-callback error unchanged 16.11%; RMS 13.61 on training diagnostic; +40–60k estimate | 1,792 holdout seeds absent; retrospective accuracy is not online accuracy |
| `b5-conditioning/silent-step`; [R4][r4] | n=128, 10000..10127: +.0066 (.0204) vs fresh thr09; +.3293 (.0414) vs lattice | Rate, RMS, gas NR | 1,920 holdout seeds absent; null |
| `b6-learned/history-price`; [R4][r4] | n=768, 10000..10767: −.0019 (.0087) vs thr09; +.3104 (.0177) vs lattice | Rate/RMS NR; +3–12k, worst about 80k estimate | 1,280 holdout seeds absent; confirmation also negative |
| `fresh6-2`, extra trade-size likelihood; [R4][r4] | n=256, 10000..10255: −.0405 (.0215) vs thr09; +.2929 (.0327) vs lattice | Rate/RMS/gas NR | 1,792 holdout seeds absent; negative |
| `fresh7-1`, uniform-cell arb density; [R5][r5] | n=512, 10000..10511: −.012841 (.011877) vs thr09; +.309315 (.021976) vs lattice | 28.809402%; RMS 13.273536; −300 to +200 estimated | 1,536 holdout seeds absent; null |
| `mass8-2`, second survivor-mass repair; [R5][r5] | n=1,536, 10000..11535: +.217756 (.013975) vs thr09; +.538281 (.017191) vs lattice | 28.053871%; RMS 13.014572; +500–3,000/kernel estimate | Overlaps full mass8-1; 512 missing, no extra N |
| `values7-1`, 25-action posterior shortlist; [R5][r5] | Only 64 tuning seeds 64000..64063: −.107411 (.060269) vs base, Gaussian ablation −.032770 (.050719) | Training 28.732041%; RMS 13.177927; up to 2,000 value reads, about .5 GB arrays | No confirmation or holdout; not a zero-return candidate |
| `b6-action-values/values-1`; [R4][r4] | Active candidate not scored: off-grid fee agreement max 6.909 bps failed its then-required .01 gate | Active diagnostics NR; naive gas about 10.8M | Reported zero increment/+ .3229 vs lattice belongs to α=0 fallback, not the candidate; excluded from ranking |
| `b9-kappa-flag/kap-0`; [R6][r6] | Full solve killed for memory; alternate memmap reached 13 of about 110 sweeps | No policy score, misread, price error or gas measurement | No κ=0 holdout. Separate kap-3e5 auxiliary tuning: κ=0 −.160 (.031), κ=3e-6 −.098 (.026) vs TG; not holdout evidence |
| `b9-float-forensics/ff-1`; [R6][r6] | Exact floating/WAD round-trip test, 64 tuning seeds: +.024 (.015) vs older tolerance on replica; +.048 (.018) on worker's Rust-arithmetic transcription | Replica 0/245,221 arbs missed; 220/206,330 retail first trades falsely flagged; price RMS/gas NR | No 10000..12047 result or port. The transcription was not checked against Rust execution |
| `a9-tell-wad/wad-1`; [R6][r6] | 32 tuning seeds; relative coefficient 199 plus absolute input-WAD allowance: 0/123,573 arbs missed, 653/227,917 retail callbacks falsely flagged | No closed-loop score/RMS; +1–4k estimate; 120 synthetic crossings, no natural crossings | Detector/spec work, not a holdout-winning policy; exact round-trip variant reduced false flags to 296 |
| `b1-ideas/idea-twohyp` | No result in handed record; failed/attempts exhausted, batch cancelled in goal state | All requested measurements absent | Later branch/probe items tested related mechanisms; no success attributed to this item |
| `b10-finer-table`, 2.5-bps DP refinement | One failed item; no accepted result in goal state | Score, misread, price error, table size, gas all absent | No finer-table gain demonstrated; cause of failure not supplied |
| Second `b10-tell-sigma` and `b10-tell-rival` copies | Each batch has one failed copy and one accepted result | No measurements from failed copies | Do not count as replications |

The three early **Numba acceleration** items report the twelve reference gates and agreement with their own Python reference on 64 seeds to ≤2.7393e-10; speedups ranged 55.7–99.5× under different timing conditions. The selected `b1-numba/numba-3` is described in episode-2 notes as a whole replica/lattice/RNG port, result [`1134b0f83ff44cf484f8dc780a5c7f0e5d08d2cbbfad3d4ee2d3578ae6fa1ac6`][numba]. It reported identity to local Python on 2,048 seeds but 34 differences above 1e-6 from the shipped lattice reference, maximum .074, attributed to libm without proof. These are acceleration results, not new fee-policy gains; numerical EVM gas is inapplicable. R2's later statement that no complete acceleration deliverable was established is weaker than the earlier recorded claim: this report retains the claim and its limits, without asserting a fresh reproduction or bundled offline dependencies. [R1][r1], [R2][r2]; goal notes, episode 2.

The **misread investigations** used 60000..60511 for training and 61000..61255 for diagnostics, never the official holdout. Amount features changed CART error from 16.1034% to 16.0028%, without a closed-loop fee-policy test. Size/timing logistic features left AUC near .922 and error near 16.2%. Hindsight features cut retrospective logistic error to 11.772%, but the current price estimate did not improve: three-callback soft retrospective RMS was 11.846 bps, while current RMS stayed about 13.887 versus 13.867 for the base. Two additional 121-cell beliefs are not a viable direct contract implementation; a Gaussian approximation would need additional moments. These diagnostics supply no paired holdout gain or measured EVM gas. [R2][r2], `misread-amounts`, `misread-size`, `misread-hindsight`.

The **oracle ablations** also remain outside the blind ranking. On 512 tuning seeds, true flag alone added +2.715303 (.041883) over lattice; true price given flag added +1.482968 (.026741); rival and global phase together after flag/price added +.198392 (.015320). They overlap and cannot be summed arbitrarily. The separate flag-split experiment assigned +2.3425 to flag-informed belief alone, +.2193 to phase alone, and −.7898 to rival alone under a still-wrong belief; all three together added +2.7152. Oracle price has zero error by construction and is unavailable to a deployable policy. These experiments explain why simply minimizing misreads or price RMS was not enough. [R2][r2], `gap-1`; [R3][r3], `split-1`.

The float-forensics item also investigated four additional clues: split-versus-whole fills, reconstructing rival reserves after a split, price information from retail-sell amounts, and replaying alternate arithmetic code paths. It reported no usable new gain beyond the exact round-trip tell: the first two mostly recovered already-tracked state, retail-sell price information was extremely weak, and code-path replay added about zero on its training diagnostic. None received a separate full holdout, price-RMS result or EVM gas measurement. [R6][r6], `ff-1`.

Historical failures supplied as starting context were overlap-zone masking, more aggressive pin buying, quote-aware fill likelihood, and a classifier restricted to existing filter features. The later ledger separately tests larger κ, probes, fuller posteriors and router variants; it does not count those historical attempts as new goal measurements. [R1][r1], [R2][r2].

**What the tell found, and what it did not prove**

The breakthrough exploits the simulator's floating-point arithmetic. On the replica, an arb's net input is a reserve difference and often lies exactly on the reserve's binary64 spacing. A retail fill can hit that grid by chance, increasingly often for larger fills. The observable test uses the fee already in force and the six afterSwap inputs. If `v` is net input, `z` the input-side post-trade reserve, and `g=min(ulp(z),ulp(z-v))`, the double test checks distance of `v` to `g` times an integer against `C*2.220446e-16*v`. Its chance factor is `r=min(1,2*tol/g)` on a hit. **Off-grid forces π=0; on-grid uses π=L_arb/(L_arb+r*L_ret).** It does not hard-pin every grid hit. One root summary incorrectly says off-grid zeroes retail likelihood; the formula and frozen implementation instead force retail. [R5][r5], TG implementation description; [T1][t1], `tell_spec`.

TellGauss's two copies agree on the principal full holdout: 9,364 misreads / 14,351,249 first trades, versus about 2.32 million for the lattice reference. The remaining −.025757 edge gap to the true-flag diagnostic is small. The orchestrator's earlier hard-pin experiment lost about 5.1 edge on 32 tuning seeds, because a false pin is costly; C=.5 missed arbs, and exactly 30-bps fees produced a degenerate high false-hit rate in that diagnostic. These are limited training observations, not extra holdout samples. [R5][r5]; goal notes, episode 9.

T1 uses a wider **integer WAD** envelope plus an absolute truncation allowance, and stores the exact returned fee WADs. It inherits M09's bounded Gaussian mixture and compressed tables, not the full-table TG implementation. The method is an artifact of this simulator's observable numerical inputs, not a general ability to identify real-market arbitrage. Empirical engine performance supports transfer to the pinned engine build; universality across floating-point implementations, market mechanisms, or future engines was not established. [T1][t1], [Audit 1][au1], [Audit 2][au2], [E1][e1]–[E6][e6].

**Track A: compression ledger**

Compression cost must compare the same policy/filter with compressed and full tables. A positive combined policy change is not a compression measurement. Table payload bytes, JSON size and compiled runtime bytes are distinct. The inherited table family is `pol_mid.json` for plain quotes and `qm_k1e-5.json` for uncertainty-aware quotes. The full QM set has 321 own-price rows, eight SD levels and separate rival modes. [R1][r1], [R2][r2].

| Table experiment / port | Representation and bytes | Replica difference against full tables | Qualification |
|---|---|---|---|
| SD-level reduction, `compress-sdlevels`; [R1][r1] | Retain SD 4/20: 268,356 cells; add 34: 402,534 cells. Serialized/packed bytes NR | Full holdout: −.0098 (.0102), or −.0059 (.0101), vs Gaussian/QM | Good isolated dimension reduction, far too many cells alone; one level lost about .59 or more in tuning |
| Merge rival modes, `compress-rivalmode`; [R1][r1] | One mode, 13-knot “s” choice; bytes NR | −.2716 (.0103) holdout; averaged modes −.2939 | Fails −.2 loss target |
| Fit `k13_c15_c7_l4`; [R1][r1] | 6,968 cells, **7,007 bytes** one-byte payload including knot metadata | −.1306 (.0102), n=2048 | Within −.2 target; standalone compression, no final callback parity |
| Fit `k17_c15_c7_l5`; [R1][r1] | 11,390 cells, **11,434 bytes** | −.0653 (.0105), n=2048 | Lower loss, larger payload |
| Larger fitted candidate; [R1][r1] | About **30.8 kB** reported | −.051 on holdout; SE NR | Too large for direct contract use; multiple candidates tested on holdout weakens single-freeze interpretation |
| P1 plain port; [R1][r1] | 45 own-price knots, .01-bps residual resolution; payload bytes NR; runtime **24,132** | Separate edge compression cost NR; full-grid fee difference reached 58.1094 bps | Full-table parity failed despite close same-compressed-table arithmetic |
| **P2 plain port**; [R1][r1], [P2][p2] | 71 own-price knots, all 13/49 rival columns, mirrored bid, int16 .005-bps residuals; runtime **22,567**; distinct payload byte count NR | **−.00803 (.00899), n=256**, vs full plain tables, 60000..60255 | Within compression target for plain policy; full holdout compression cost not measured here |
| QM-1; [R2][r2] | 33 w knots, five SD levels, seven band/35 rival columns, s-only, mirrored bid; **12,705** byte cells, 398 words (**12,736 padded bytes**, derived); runtime **23,879** | **−.110174 (.025161), n=256**, 60000..60255, vs full Gaussian/QM | Qualifying alternative; no engine comparison |
| **QM-2 / Q2**; [R2][r2], [Q2][q2] | 33 w knots; SD 0/4/12/20/34; seven band/41 rival columns; retain s/c; phase 2 shares phase 1; mirrored bid; 1-bps unsigned residuals. **14,685 byte cells**, 459 words (**14,688 padded bytes**, derived); runtime **23,729** | **−.0377002762 (.0124479105), n=1024**, 60000..61023; 256-seed estimate −.062551 (.026640) | Selected common table set; loss is Gaussian-policy-specific |
| PB-1 / PB-2; [R2][r2], [R3][r3] | Same Q2 cells; XOR encoding/lookup changes; runtimes **21,915 / 22,118** | Combined blend+compression **+.264374 (.016250), n=1024**, vs full Gaussian/QM; not isolated compression | No additional Q2 table levels/columns dropped |
| MIX-1 / MIX-2 / M09; [R3][r3], [R4][r4] | Same Q2 cells; runtimes **22,073 / 21,984 / 21,984** | Combined changes vs full Gaussian/QM: **+.384582 (.018234)**, **+.387873 (.018380)**, **+.722985 (.019959)**, each n=1024 | Same-filter full-table mixture ablation not reported; do not assign Q2's −.0377 to them |
| **T1**; [T1][t1] | Same Q2/M09 tables; runtime **22,832**; expanded QM SHA `d035dfd049ab4d9b7cd69ed4588a87e15980732d3c5fe9d0a831ac9a64e1206e` | Exact WAD twin **+3.1112655590 (.0312996746)** vs full Gaussian/QM; ideal-double twin +3.1188887447; all n=1024, 60000..61023 | Combined tell/filter/compression effects; **isolated post-tell compression cost unmeasured** |
| `a10-tell-compress`, two copies | Both items failed; no accepted table set or byte count | No score or full-table ablation | Planned resolution reallocation is not a delivered improvement |

The full QM source SHA is `5ff53e42ca87390e5f65d1caa3f7a480e67a8212fb0670274dfd562b05ba1afd`; plain source SHA is `efbb5ee102db4d312f64565d9bf7232b6becbe02b624164f744a402bbbf2983b`. Q2's 1-bps cell quantization is compatible with much tighter arithmetic parity against a Python twin using those same quantized tables; it does not imply ≤.01-bps approximation of every original full-table action. Mirror asymmetry in one original table, separate SD-level experiments, and differing grids make the compression ablations nonadditive. Early “knots” and “mirror” items yielded no accepted results after cancellation; their absence is not zero compression loss. [R1][r1], [R2][r2]; goal state and notes.

**Port parity, gas and validation ledger**

The reference gate outputs were reported reproduced by independent early workers and later checks. They are recorded measurements, not rerun here:

| Replica seed | Perfect information | Gaussian/plain | Gaussian/QM | Lattice/QM |
|---:|---:|---:|---:|---:|
| 10000 | 448.261189 | 443.455598 | 443.522608 | 443.663520 |
| 10001 | 576.779199 | 571.463409 | 571.623551 | 571.977293 |
| 10002 | 531.886497 | 525.168028 | 525.865859 | 526.411631 |

Sources: [R1][r1], gate copies; [Audit 1][au1], `validation.reference_gates`. The pinned [solved README][readme] describes these reference checks and the separate compression and engine gates.

Every completed port below reports Solidity 0.8.24, viaIR, optimizer 200, Paris; runtime ceiling 24,576 bytes and 32 storage slots. Normal fee parity uses callbacks from 20 real replica runs, ordinarily 10000..10019. Stress results are separate sampled checks. Gas shown as pyrevm is not substituted for live engine gas. “0/0” means reported OOG/reverts on the stated tests, not a proof over arbitrary inputs.

| Port / source | 20-run fee parity, max error bps | afterSwap peak gas: pyrevm / stress / engine | Faults; validate; status |
|---|---|---|---|
| P1, `a1-port-full/port-1`; [R1][r1] | **FAIL** against full tables: 58.1094; 138,037/212,446 over .01; same compressed tables about .00225 | 193,882 / 213,782 / not run | Stress no reverts; validate pass; not qualified as full-table port |
| **P2**, `port-2`; [R1][r1], [R2][r2] | 3.35019e-9; 212,490 callbacks, none over .01; compressed plain reference | 145,062 / 144,288 / **193,866** | 0/0; pass; plain policy below +2.7 on measured engine sample |
| QM-1; [R2][r2] | 8.5021e-10; 214,731 callbacks | 165,011 / 163,949 / not run | 0/0; pass; alternative compression |
| **Q2**; [R2][r2], goal ep7 | 6.79479e-9; 214,310 callbacks | 155,745 / 158,473 / **206,021** | 0/0; pass; completed ≥4,000-pair bar |
| **PB-1**, measured engine PB; [R2][r2], [R5][r5] | 2.84168e-9; 215,003 callbacks | 167,214 / 157,232 / **215,849** | 0/0; pass; completed ≥4,000-pair bar |
| PB-2, separate source; [R3][r3] | 2.84172e-9; 215,003 callbacks | 172,801 / 160,948 / not run | 0/0; pass; do not attach PB-1 engine scores |
| MIX-1, merge after first silent cut; [R3][r3] | THR .5: 1.183585e-8 on 213,160; THR .9: 1.264243e-8 on 216,440 | 178,071 / reported forced maximum 162,965 / not run | 0/0; pass; separate candidate |
| MIX-2, merge after second silent cut; [R3][r3] | THR .5: 1.448608e-8 on 213,257; THR .9: 2.72139e-9 on 216,453 | 146,477 / 159,900; forced 147,222 / no standalone .5 engine test | 0/0; pass; parent of M09 |
| **M09**, MIX-2 with THR=.9; [R4][r4], [R5][r5] | 2.72139e-9 on 216,453, independently reproduced by both qualifiers | 146,477 / 159,900 / **219,533** | 0/0; pass; source identical across qualifier copies |
| Tell port `tp-1`; [R6][r6] | **FAIL original-double replay**: 479.784; 213,544/213,683 over .01. Conditional WAD diagnostic about 1.42e-8 | Separate tests ≤176,739 / no accepted engine pilot | 0/0 reported; pass; intended pilot cancelled |
| **T1 / tp-2**; [T1][t1] | Applied-WAD double-filter error **1.442564e-8**, 213,640; integer-model/EVM fees bit-exact | 147,038 / 163,384 / **208,330** | 0/0; pass; original-double trajectory equality not achieved |
| T1 independent audits; [Audit 1][au1], [Audit 2][au2] | Same frozen source, **218,199 callbacks on 67512..67531**, zero integer/EVM fee mismatches; conditional-double max **2.4638416307e-8** | 148,733; mean 62,018.2 / separate edge-case tests / audits ran no engine seeds | 0/0; pass under applied-WAD scope; cannot broaden this to ideal-double parity |

The original Q30 math components and table harnesses were useful spares, not full policy ports. `math-1` reported 19 tests and 5,437 runtime bytes, with a sampled truncNormal call around 147,201 gas including external harness overhead; `math-2` reported 35 tests, 4,161 bytes and sampled scalar/truncation costs 817–18,467 with different internal accounting. `tables-1` reported 106 tests, 13,566-byte runtime and 19,433-gas lookup; `tables-2` six tests, 8,351 bytes and 42,108-gas external lookup. Neither table harness established full-table compression quality plus callback parity; their coordinate units differ. These component tests were not added together into a contract gas claim. [R1][r1].

The two direct lattice efforts failed feasibility. The first exact filter reached **4,545,807** gas with a twelve-silent-step cap; matching the original thirty-step cap reached **9,040,497**. Coarser/truncated variants broke accuracy. SWAR reduced an exact implementation to **2,421,322**; its accuracy-qualified hybrid still peaked **1,487,686**, including **402,544** at dt=1. These were filter-only tests, so quote work would add cost. A 12,555-gas word-parallel microbenchmark and suggested 110–150k full design were not complete measured callbacks. [R2][r2], `latt-gas-1`; [R3][r3], `swar-1`.

**T1's parity qualification and reconciled audit findings**

The independently written Python integer model generates its own applied fees and replica callback tape before EVM execution. The frozen contract receives only the six callback fields, and its output is compared rather than fed back. A double filter runs on those common callback WADs, receiving the integer model's exact applied fees only for the discontinuous tell. The audits add an independent rational detector and a separate diagnostic getter; zero mismatches on the sampled callbacks support the numerical implementation. This is a useful test of the deployed integer policy. It is **not the original “same autonomous real.py trajectory” gate**. [Audit 1][au1], `method`; [Audit 2][au2], `int_model_twin_audit`.

The stricter comparison fails: ideal-double replay on the integer tape has **218,080/218,199** callbacks above .01 bps, maximum **466.346948 bps**; autonomous paths diverge in the first one to three callbacks. Even the initial double fees differ by two wei. Such tiny differences matter to a floating-grid test. The T1 port separately reports exact-WAD minus ideal-double edge **−.0076231857 (SE .0042938648), n=1024**, on training-range replicas. That small economic cost does not turn a failed equality gate into a pass, and the audit's different autonomous comparisons have different comparator definitions. No full ideal-double parity pass is claimed. [T1][t1], `wad_twin_cost`; [Audit 1][au1], `ideal_double_scope`; [Audit 2][au2], same field.

Two apparent identity problems in R6 can be resolved without another simulation:

* **IB identity verified here:** fetching the task's original IB artifact and decoding its `code_zb64` yields raw Solidity, SHA-256 `301941829a44bb60977bb28181a5e4bfa6544f3696763f987054789b2611d686`. This exactly matches IB in all seven T1 engine records. The original compressed object is raw source, not a tar. The fetched result bytes also match its content ID. [Original IB][ib], [Pilot][pilot].
* **No inline-assembly contradiction:** the frozen T1 source and its bundled base files contain no `assembly` keyword. Audit-2's archived `aggregate.py` line 50 defines its field as `'assembly': st['assembly_occurrences'] == 0`; therefore `true` means the no-assembly check passed. Audit-1's `false` means assembly is absent. The field names are inconsistent; the source is consistent. This corrects R6's unresolved-conflict statement. [T1][t1], [Audit 1][au1], [Audit 2][au2].

The audits' one-count retail tell discrepancy remains explicit: Audit 1 gives 353 positive retail tells among 64,820 first retail trades, Audit 2 gives 352. Both give 75,662/75,662 arbs with positive tells and no missed arb. The posterior classifier is a separate metric: 139 arbs classified retail plus 81 retail classified arb, **220/140,482 = about .1566%**. A positive tell is not automatically a positive arb classification. Both audits find zero nonzero posteriors on zero-tell first callbacks. Their exact positive-tell disagreement was not reconciled here. [Audit 1][au1], [Audit 2][au2].

Actual fee retention matters: reconstructing a capped fee from its log multiplier can give `99999999999999999` instead of `100000000000000000`, changing one detector result. T1 stores the exact WAD fees above bit 64 in slots 4/5 and remains within twelve slots. Independent mutation tests detect stale fees, wrong side, removal of absolute allowance and one-wei amount/fee perturbations. They are sampled sensitivity tests, not formal overflow or universal no-revert proofs. [Audit 1][au1], [Audit 2][au2].

**Track A: engine evidence and seed accounting**

All counted T1 blocks run each candidate **alone against VanillaStrategy**, using the same configurations for T1, M09 and IB. They use `amm_sim_rs.run_batch(X, VanillaStrategy, configs, 8)` and extract `edges["submission"]`. Reports check MatchRunner configuration construction, absolute-seed RNG, draw order mean size/arrival rate/sigma, and the frozen source, creation/runtime and wheel hashes. These are paired differences between separate matches, not T1 playing directly against IB. All seven original row sets, their pair statistics, nonoverlapping bounds, identities and per-command gas counters were checked for this write-up. [Pilot][pilot], [E1][e1]–[E6][e6].

| Source | Inclusive seed range | n | T1−IB mean (SE) | Paired sum | Paired sumsq | T1 afterSwap peak |
|---|---|---:|---:|---:|---:|---:|
| [Pilot / a9-tell-pilot/tp-2][pilot] | 12009984..12010111 | 128 | 6.314846 (.144242) | 808.3002913942055 | 5442.510110200317 | 198389 |
| [E1 / eng-12010112][e1] | 12010112..12010367 | 256 | 6.239486 (.113885) | 1597.308434844172 | 10813.050605319815 | 208330 |
| [E2 / eng-12010880][e2] | 12010880..12011135 | 256 | 6.125354 (.136722) | 1568.0905275311995 | 10825.382369350085 | 202637 |
| [E3 / eng-12012672][e3] | 12012672..12012927 | 256 | 6.228100 (.105713) | 1594.393581006647 | 10659.56240963919 | 195036 |
| [E4 / eng-12012928][e4] | 12012928..12013183 | 256 | 6.480936 (.117428) | 1659.11957613996 | 11652.815385806842 | 196517 |
| [E5 / eng-12013184][e5] | 12013184..12013439 | 256 | 6.063285 (.103334) | 1552.2010773097484 | 10108.498795356189 | 198337 |
| [E6 / eng-12013696][e6] | 12013696..12013951 | 256 | 6.003274 (.110599) | 1536.8381628781626 | 10024.57950506316 | 197613 |
| **Pooled, computed here** | Seven disjoint ranges | **1664** | **6.199670 (.044861)** | **10316.251651104096** | **69526.39918073559** | **208330** |

For reproducibility, pooling uses `N=sum(n)`, `S=sum(paired_sum)`, `Q=sum(paired_sumsq)`, `mean=S/N`, and `SE=sqrt((Q-S*S/N)/(N*(N-1)))`. Standard errors are never averaged. The worst-five union was checked against the raw paired rows. Excluding the expansion-triggering pilot gives confirmation-only **n=1,536, mean=6.1900724998, SE=.0470932569, S=9507.95135970989, Q=64083.88907053528**. The pilot inclusion does not create the gain.

On the same 1,664 seeds, **T1−M09 = +2.3831401103 (SE .0216904447)**, S=3965.545143603261, Q=10752.364248896203; **M09−IB = +3.8165303531 (SE .0385356834)**, S=6350.706507500834, Q=28347.000612618547. T1−M09 has negative individual seeds, worst −.6041287217 at 12010344. T1−IB is positive on every recorded seed. The training-replica exact-WAD increment over M09 was +2.3881759147 (.0283933033), close to the engine increment. The earlier calibration prediction 3.769+3.111265559−.59=6.290265559 differs from measured T1−IB by −.0905951, inside the goal's .2 diagnostic tolerance; this comparison is not a board forecast. [T1][t1], [Pilot][pilot], [E1][e1]–[E6][e6].

Live gas, calculated from all **78 commands (26 per arm), each 64 seeds**:

| Submission arm | afterSwap calls = successes | Gas sum | Call-weighted mean | afterSwap peak | afterInitialize peak | OOG / revert / other fault counts |
|---|---:|---:|---:|---:|---:|---|
| T1 | 18,033,745 | 1,938,263,609,970 | 107,479.8169 | 208,330 | 229,429 | All zero |
| M09 | 18,283,500 | 2,041,120,755,784 | 111,637.3099 | 202,326 | 229,594 | All zero |
| IB | 17,941,549 | 2,425,838,454,391 | 135,207.8605 | 237,694 | 243,227 | All zero |

Each command reports empty gas counters after reset, a snapshot after scoring, and elapsed time below eight minutes. Counts equal successes; OOG, revert, bad_return, other_halt and tx_error are zero for both roles. T1 has **36,670 gas** of measured afterSwap headroom to 245,000. Historical M09 peak 219,533 remains its overall maximum even though the T1-control sample peaks lower. Completion of a match alone would not establish this: the earlier audit noted that a callback failure can leave prior fees in effect. [R3][r3], [R5][r5], [Pilot][pilot], [E1][e1]–[E6][e6].

The goal state resolves R6's uncertainty about missing confirmation blocks. The sixteen allocated a10 blocks held 4,096 seeds, but only **six items were accepted and ten failed**: a10-a 2/4 accepted, a10-b 0/4, a10-c 2/4, a10-d 2/4. No results are supplied for failed ranges **12010368..12010879**, **12011136..12012671**, **12013440..12013695**, and **12013952..12014207**. They contribute zero observations, and their failure causes are absent from the snapshot. The cancelled tp-1 pilot allocation **12009856..12009983** was retired. The next unreserved seed in the final notes is **12014208**. No allocation was reused to manufacture missing coverage in this write-up.

Earlier candidate milestones remain separate:

| Candidate | Qualified historical n | Mean over IB | SE | Paired sum | Paired sumsq | Overall engine afterSwap peak |
|---|---:|---:|---:|---:|---:|---:|
| P2 | 1024 | 2.2063503167 | .0497388461 | 2259.302724257228 | 7576.407493516774 | 193866 |
| Q2 | 4232 | 3.0212595955 | .0228327295 | 12785.970608252373 | 47964.52196328807 | 206021 |
| PB-1 | 4488 | 3.3643532801 | .0215266357 | 15099.217521313143 | 60130.81212553013 | 215849 |
| **M09 milestone** | **4352** | **3.8055818877** | **.0225973589** | **16561.89237517556** | **72696.89983294165** | **219533** |

Sources: [R2][r2]–[R5][r5] and goal notes, episodes 7–10. Later controls add 1,664 distinct M09 pairs: including them gives **n=6,016, mean=3.8086101866, SE=.0195134055, S=22912.598882676393, Q=101043.9004455602**, computed from the milestone and T1 records. They do not count toward T1's 4,000 requirement. Q2/PB/M09 meet the empirical +2.7/n≥4,000 milestone under the historical qualified-cohort rule; only M09 is the strongest completed fallback.

Historical exclusions and protocol deviations are retained:

* **12003072..12003327:** plausible scores but validation gas was substituted for live engine gas; excluded from qualified pools.
* **12003328..12003583:** unexplained IB mean 182.6913 and anomalous cross-contract gaps; quarantined, no cause inferred.
* **12004864..12005119:** different source-built engine/Cargo.lock, no released-wheel equivalence evidence; separate cohort, excluded.
* **12003840..12004095:** only common seeds 12003840..12003847 count, eight pairs; unmatched IB runs and remainder excluded/retired.
* **12007168..12007423:** no network access, no engine seeds started; later goal notes retire the allocation despite R4's suggestion it could be reused. Count zero.
* Early P2 work reran IB on the 768 baseline seeds already scored in episode 1; a Q2 item repeated its two-seed probe at 12001280..12001281; source-built work also repeated an IB block. Those are literal never-reuse deviations, even where only one observation per seed entered statistics. Therefore the historical Q2 milestone is not an unqualified certificate of perfect once-only execution. The seven T1 blocks report no repeats and have disjoint observed ranges.
* The default-seed diagnostic ran 500..511 outside bs-0's allocation and again in bs-500. Those duplicate diagnostic executions are excluded and never enter fresh-engine pools.

Sources: [R1][r1]–[R6][r6]; goal notes, episodes 2, 5, 7, 10. Good later runs cannot retroactively supply missing gas or explain a quarantined result.

**Reproducible identities and repository status**

The goal's **`trunk` is null**. All 72 recorded batches are research batches; no goal repository or merged wave commit was delivered. Code traveled in result archives. The upstream engine repository is [`benedictbrady/amm-challenge` at `6b6921f8d463314aa7c96234e1be25a25245f704`][engine], and solved reference inputs are [`gtmcknight/amm-sim`, commit `e65314f88de945f6d055bfc2aab01c482ab6570e`, `research/solved`][readme]. These are dependencies, not a goal-owned code trunk.

| Artifact | Exact identity / retrieval |
|---|---|
| T1 result | [`6b308b7219a0cf0bab1e5168e2f2b94b68bc6c118ae09a6d5ca30ea0173638ff`][t1]; `code_zb64` is base64(zlib(tar)); source member `t1/Strategy.sol` |
| T1 source | SHA-256 `6ee77c053e29d23a89b926c33b13e32365bdd09d880cac5557ce06c043dcf1ac` |
| T1 runtime | SHA-256 `8e10f67ca334ce8959f19520245254f7d9f2f47ab5299b2a62cd08ae49844208`; 22,832 bytes |
| T1 archive | Uncompressed tar SHA-256 `55c4b1e135e6bbd5f17f9d964107d8744a3ce7518650ef830da5d7f5a3192fef`; declared `code_sha256` **`70b4efee30b245afbfe6e277c802bfbd7d2f3289f4aeba850d9203c6f59ff267` hashes base64 text** |
| M09 result | [`063270cb0315aaded47d5cb3f437297bf8e9aac55e179fc4d26534a6d0e269d3`][m09]; member `m09-2/Strategy.sol`; source SHA `a44cca4b0155ca3953f27ccb6b43ac8ee74b1cdc4f27022ee5fc51d8ab67ed5f` |
| M09 runtime | `e95f44d13169747859490d2f5fb627a55b4a9cb3c84dae0c95a6b37e0023e281`; 21,984 bytes |
| IB | [Original result][ib]; decoded source SHA `301941829a44bb60977bb28181a5e4bfa6544f3696763f987054789b2611d686`; runtime `a4f70330df778c7a4c916170f1b3036522789028ae2dfd8f715b93ff7f24ab2d`, 14,528 bytes |
| Q2 | [QM-2 result][q2], nested `qm-2`; source SHA `2c471f0132b0f06aae83b7b2c8622083c9d8cb7b3d5e75719dd362f5b36bb259` |
| Measured PB | [PB-1 result][pb]; source SHA `5123bb39594add4ad9a32f376ff7aa89c13428b82ea324ae4d80c474e3162d95`; PB-2 is a different implementation |
| Canonical earlier source bundle | [Audit bundle][sources]: IB.sol, Q2.sol, PB.lines.json and restore_pb.py; source hashes, not ambiguous archive hashes, identify measured contracts |
| Frozen engine wheel | SHA-256 `aedb68280aca34c110968f00148387c95885207913fb2cf19a1ab4c5cfd6887a` |
| Native extension | SHA-256 `ff88b6353c2aad7342f0a26194f7347e78b9c3b38d683a7449006d423978cd14` |
| Vanilla source | SHA-256 `62d40ccef0de99a385e332a36ddf9cbd1da73eda06bd7954492a9880cb91a572`; runtime 640 bytes |

The T1 and original-IB result hashes, T1 tar/base64/source hashes and absence of assembly were checked here by decoding in memory, without executing embedded code. Other historical identities are attributed to the cited records. Hash domains are deliberately explicit: previous results sometimes hashed base64 text, compressed bytes, raw source or tar bytes under the same `code_sha256` name. Matching a hash identifies bytes; it does not certify their behavior or supply external dependencies. This report is the only new delivered file; archive links preserve the goal's code provenance and do not claim an offline build was rerun.

**Fleet execution, limits of the evidence, and closure**

The goal ran both tracks from episode 1 and generally used small batches, spare copies, segmented simulations, checkpointed solvers and no speed threshold. Early work exposed the fleet problems anticipated in the brief: platform wording blocked one IB item, raw-output requests refused fixture work, a no-network seat produced no M09 observations, slow seats returned partial B holdouts, and κ=0 solving exhausted memory. Later audits required real gas snapshots and exact source/config/wheel identity before expanding engine samples. These are observed limitations, not questions the requester needs to answer now. [R1][r1]–[R6][r6]; goal notes.

The final snapshot says **166/240 items used**, episode **10/20**, while the 72 batch item totals sum to **167**, with **148 accepted, 19 failed, zero running/waiting**, and all batches settled. The batch list includes the cancelled staged tp-1 pilot; no remaining-budget inference is drawn from the differing counters. They are not evidence of performance completion. “Accepted” includes partial or negative results, and never substitutes for the gates. Full batch briefs/vars and episode decisions files are not handed over: `goal.json` retains truncated brief excerpts. The notes record one named item per experiment/block and required result fields, but retrospective compliance of every filled brief or decisions JSON cannot be certified from excerpts. This write-up issues no new batch briefs or orchestration decisions; the requested sole output is `report.md`.

The supplied merges carry source-recheck warnings on numerous worker results. Those warnings leave local measurements as attributed reports and reduce support for source-derived explanations; matching deterministic duplicate results is not independent statistical replication. R6's assertion that local measurements are “unaffected” is too strong to treat as certification. This report recomputed the seven T1 row sets, but did not independently reproduce the engine, audit experiments or B simulations. Small cross-runtime reference differences, subset-only diagnostics, model-derived gas estimates, and multiple ideas evaluated on a shared fixed holdout limit broad statistical claims. [R1][r1]–[R6][r6].

The only later board information used is the **historical supplied snapshot**, fetched by the earlier board item at about 15:22 UTC on 2026-11-10: first 528.4152345795, tenth about 525.38, and an existing external `@builtbyimd` TellMinLookup entry about 528.3025. It is not this goal's submission, and its relation to T1 is unproved. The pooled default-seed IB diagnostic gave **529.3520873175 (SE 2.7977255528), n=1000**, rather than historical IB 522.0013. Thus the board's seed/model equivalence was not reproduced; neither 522+6.19967 nor the source snapshot establishes a T1 rank. No board page or API was fetched for this report. [R6][r6]; goal notes, episode 10.

What remains unmeasured or unmet is specific: T1's remaining 2,336 pairs to reach 4,000; the original ideal-double parity gate; a same-filter post-tell full-table compression ablation; a completed finer-table result; a feasible, validated Solidity transfer of post-tell rival propagation; the missing B holdout portions and diagnostics marked NR; and any actual first-place board outcome. The delivered result is a substantial simulator-specific gain with a fully identified contract, a stronger completed M09 fallback, and a ledger of both gains and dead ends. The empirical first-place objective remains unachieved in the supplied evidence.

**Source register and write-up checks**

Root citations refer to immutable supplied merge results: [R1 / root-1-01][r1], [R2 / root-1-02][r2], [R3 / root-1-03][r3], [R4 / root-1-04][r4], [R5 / root-1-05][r5], [R6 / root-1-06][r6]. The named original item in each row locates its evidence within that merge. Direct audit, engine and final-B citations link the supplied JSON result IDs. The input goal record's SHA-256 is `0753a3f4183381cdf2154fa4f8753fddcfafe0fefdcd558950f492ae6a40f38d`; references to episode notes mean that fixed handoff, not an external mutable plan.

Local write-up verification checked all eighteen supplied artifact hashes against the assignment, parsed all direct JSON results, recomputed every T1 arm sum/sumsq and paired mean/SE/worst-five from the seven original row sets, checked unique seed ranges and common frozen identities, and reconciled 78 gas snapshots with successful-call totals and zero fault counters. No new simulation was used. File encoding, the 64,000-byte ceiling, Markdown links and write scope were checked separately. These checks establish consistency of the report with its evidence; they carry no independent behavioral authority.

[r1]: https://api.imd.fun/artifacts/e6e59f87d0cdc0172a94287f142a95a443f2a09b9d26398bb7c623e4d115fff4
[r2]: https://api.imd.fun/artifacts/304684a48223719e0cd912d39fe8bafd501debd710044df3e80e97b36f66a298
[r3]: https://api.imd.fun/artifacts/71835bcc2bcdd05ffc6288155d2bf9980d5dae3966e22604ad60d64d0a64ad5e
[r4]: https://api.imd.fun/artifacts/147a6af7a376561b3b652a2d7c8c5b8eaf12f154f32876203e6f141e98418193
[r5]: https://api.imd.fun/artifacts/be7f39bdd1d1dd4aa3de6c0c3c375e38d90b68e7ba2b711bc3b88d679e9afad4
[r6]: https://api.imd.fun/artifacts/1733b25b102d35b6c4fc4c0ed98d18122464297149a1c5acd5839e3b7453099c
[au1]: https://api.imd.fun/artifacts/dd606564acfea059712453ef8f6a15d0294516f741b2c25c88f15cbcb5d22fdb
[au2]: https://api.imd.fun/artifacts/4f33bdc52e056d9c1bd1682593cd4f81de1c95ea4ff44bd9f433b31d150dbaf1
[e1]: https://api.imd.fun/artifacts/9b2aafec709e1cd87331023dcd7c79d666ef951f15d5f195e1336ec19f4a5685
[e2]: https://api.imd.fun/artifacts/9b815f9bd2bdec62df8e8a87cc3e36bf6b944aabc5bf025702ce3d9355d2e2ad
[e3]: https://api.imd.fun/artifacts/fb652cad4d4fd58b2524b5fc27eb6113fd71310fa796c2dfe3c8c39f73b84d40
[e4]: https://api.imd.fun/artifacts/81a1be4805f4de0032885d84b73561594d9985304c2039b01e8e3b386929f97d
[e5]: https://api.imd.fun/artifacts/cad5f2b47515f8beaac5c4dd74f26f0319734704ce539a94aac6d8f54ae9ec60
[e6]: https://api.imd.fun/artifacts/942348d62eb067ed5cc7a08f421f8d0a817931ae21f77b373565ca9b9140f959
[sigma]: https://api.imd.fun/artifacts/088a66503709b08bf96bfad74da737afcc49941e42a718c8da6165049466012d
[rival]: https://api.imd.fun/artifacts/5bfd6685de1c72b0f3ba222dbf0d6231463e19e2fc99433c8bbdcc84b11641f9
[band]: https://api.imd.fun/artifacts/873d1eec966aacb43b6695cba932f69c0814de3bf850f4425ac70332833a56e2
[drift]: https://api.imd.fun/artifacts/ebeb0efc4494c5f311408a9b044746e7618bacc04c2a9bc9d323e641063f68b2
[t1]: https://api.imd.fun/artifacts/6b308b7219a0cf0bab1e5168e2f2b94b68bc6c118ae09a6d5ca30ea0173638ff
[pilot]: https://api.imd.fun/artifacts/4528695b3a181b79340bf6e476b94d7f8ec2ee0a36dd9cd896416026cb6a7ccf
[ib]: https://api.imd.fun/artifacts/afd5183e9ff3235334e041c00b0cd19079599a2c6464db95f8c1586712105557
[m09]: https://api.imd.fun/artifacts/063270cb0315aaded47d5cb3f437297bf8e9aac55e179fc4d26534a6d0e269d3
[p2]: https://api.imd.fun/artifacts/679e9ec3e69ce093fb9ba56944ad799079b2a311ad4bea0521c2f7b15aa626d6
[q2]: https://api.imd.fun/artifacts/f6f4c4cccbd3fd9b0d7a4c4c329011ba1c765a10cc192b1402434033bdd10402
[pb]: https://api.imd.fun/artifacts/2ade1a24f75836479efeeaff574e452ff3ef5c23fd856c50bd2c1a4a10d78463
[sources]: https://api.imd.fun/artifacts/db67c7a0e8fa98f87b069766df6e213890861b15f967695293f519ecc46eeeb6
[numba]: https://api.imd.fun/artifacts/1134b0f83ff44cf484f8dc780a5c7f0e5d08d2cbbfad3d4ee2d3578ae6fa1ac6
[readme]: https://raw.githubusercontent.com/gtmcknight/amm-sim/e65314f88de945f6d055bfc2aab01c482ab6570e/research/solved/README.md
[engine]: https://github.com/benedictbrady/amm-challenge/tree/6b6921f8d463314aa7c96234e1be25a25245f704
