**+3.34989051506659 over C0 on 4,096 fresh, paired engine seeds; standard error 0.0161103258436819.** The best confirmed contract is **u1-give, copy-b**, named `TellMinLookup`. Its confirmation afterSwap peak is **209,159 gas**, with **0 reported OutOfGas**, revert, other-halt, transaction-error or bad-return events in either arm. The worst five paired differences are **−3.957261118551, −3.153132520576, −0.159818110846, +0.174811064851 and +0.261021539747**; their seeds and arm scores appear below. These figures pool saved results; this write-up ran no new simulation.

The contract's source SHA-256 is `99d031f41074ea872c78fa7dec5db33d9f20f3251e29bdbb4682c92791334b72`. Its result ID is `e04-a-u1-give/copy-b`, supplied as [b14-copy-b], with content-addressed result digest `fd2f147e94f3523e4c4f91e43dc98b88e9ce8ef1060d2939367445711154a16a`. Runtime is **21,055 bytes**, SHA-256 `b6f3c2c2a78f7f5676d16fa8f78ee9ea43fda4e16f957aa3e1eed2bfe15b1d05`, leaving **3,521 bytes** below 24,576. Across the earlier selection runs of this same source, the larger observed afterSwap peak was **209,315 gas**. [b14-copy-b] [b17-g7]

Adding the measured gain to the request-pinned C0 score, **524.94 + 3.34989051506659 = 528.2898905150666**. This is **0.1898905150666 above the pinned fifth-place score, 528.10**, and **0.1301094849334 below the pinned first-place score, 528.42**. A normal approximation gives a local paired-gain 95% interval of **3.318314276413–3.381466753720**, or **528.258314276413–528.321466753720** after that addition. This interval covers sampling error in the local paired experiment only; it does not quantify transfer to the board's own seeds. **First place was not demonstrated. Nothing was entered, deployed or submitted, and the leaderboard was not fetched.** The targets are the assignment's snapshot, not a statement of the current board.

| Fresh-confirmation seed | Candidate − C0 | Candidate edge | C0 edge |
|---:|---:|---:|---:|
| 14005601 | -3.957261118551 | 544.753726619650 | 548.710987738202 |
| 14006041 | -3.153132520576 | 514.441935072790 | 517.595067593366 |
| 14005461 | -0.159818110846 | 721.139539179323 | 721.299357290169 |
| 14007655 | 0.174811064851 | 670.312032766205 | 670.137221701354 |
| 14006578 | 0.261021539747 | 685.993489024232 | 685.732467484486 |

The negative tails remain in the primary result. Sources for these five rows are [b19-c04], [b20-c06], [b21-c12] and [b20-c08].

**The real-engine probe detected 29,091 of 29,091 arbitrage trades at 30 bps, while reading 2,015 of 70,503 retail trades as arbitrage.** At 35 bps, the control detected **24,806 of 24,807 arbitrage trades**, and read **75 of 60,502 retail trades** as arbitrage. Each fee setting covered eight runs, using seeds **14000000–14000007**. The 35-bps control reused those seeds; it is not another eight independent fresh runs. The detailed result records **one false negative at 35 bps**, contrary to the broader “every arbitrage trade” wording in the requester summary and final orchestration notes. The count table is retained as the more precise evidence. [probe-result], as preserved in [root-1-01]

| Seed | 30 bps: arbitrage read / total | 30 bps: retail read as arb / total | 35 bps: arbitrage read / total | 35 bps: retail read as arb / total |
|---:|---:|---:|---:|---:|
| 14000000 | 3616 / 3616 | 337 / 8688 | 3083 / 3083 | 6 / 7406 |
| 14000001 | 3362 / 3362 | 148 / 6991 | 2896 / 2897 | 7 / 6081 |
| 14000002 | 3606 / 3606 | 362 / 8203 | 3062 / 3062 | 7 / 6995 |
| 14000003 | 3754 / 3754 | 47 / 9793 | 3238 / 3238 | 12 / 8404 |
| 14000004 | 3705 / 3705 | 579 / 9793 | 3137 / 3137 | 15 / 8317 |
| 14000005 | 3586 / 3586 | 115 / 8909 | 3034 / 3034 | 11 / 7672 |
| 14000006 | 3686 / 3686 | 235 / 9438 | 3134 / 3134 | 10 / 8050 |
| 14000007 | 3776 / 3776 | 192 / 8688 | 3222 / 3222 | 7 / 7577 |
| **Total** | **29091 / 29091** | **2015 / 70503** | **24806 / 24807** | **75 / 60502** |

The retail false-positive fractions are **2.8580344% at 30 bps** and **0.1239628% at 35 bps**. The 30-bps first-callback confusion counts are TP **29,091**, FN **0**, FP **861**, TN **28,868**. Thus the “one in 500” premise is not an engine-wide specificity guarantee, especially when the strategy's fee equals Vanilla's. The reported 35-bps miss was at seed **14000001**, step **7561**, with a very small inferred arbitrage margin, about **1.3e-8** relative; its cause was not established.

The probe used the **unpatched engine** and a Solidity telemetry strategy, keeping previous handed reserves and returned fees. It encoded step, callback and classifier counters in tiny fee perturbations. The harness decoded those counters and inferred arbitrage opportunities from returned fair price, prior pool spot and fees in force; it did not obtain hidden trade labels inside the contract. The result reports **4,096 distinct telemetry codes**, no collisions, maximum perturbation **4,095 wei = 4.095e-11 bps**, and no unreadable steps, saturation, stale aliases, ambiguous boundaries or missing inferred arbitrage callbacks. The strategy validated, had **3,699 runtime bytes**, and matched the vector corpus. At 30/35 bps respectively, afterSwap calls were **99,594 / 85,309**, peaks **99,374 / 100,064 gas**, and gas sums **7,749,619,451 / 6,650,400,915**, with zero recorded execution failures. The second, independent probe item blocked on its harness before producing engine evidence. These are one completed probe implementation plus its fee control, not two independent confirmations. [root-1-01]

**Track A produced an exact integer detector and a smaller, faster table representation, then confirmed the combined contract.** The frozen candidate adds the bounded-bitmath detector and posterior-odds rule to C0, uses the lookup optimization and frozen QPL1 u1 tables, and adds a constant **0.35** rival-price pull on retail callbacks where the existing one-sided bound does not bind. The pull moves log rival spot 35% toward the marginal-price candidate and marks the rival estimate synced. Its code keeps exact preceding callback reserves and returned fees in slots 0–5 of the inherited 32-slot array. No inline assembly is present. [b14-copy-b]

Only the first own callback of a new step runs isArb and the price-belief update. An off-grid observation makes the arbitrage probability zero; an on-grid observation discounts retail likelihood by the integer-derived ulp/grid chance before applying the posterior rule. **A hit alone never pins the price.** Later retail callbacks can update the rival estimate and fees. The fee guard excludes the complete integer interval **2999999999999948–3000000000000057**, which converts to Vanilla's binary64 gamma 0.997, and chooses the nearest allowed neighbor, lower on a tie. It therefore addresses equal-gamma collisions rather than merely avoiding the single integer for 30 bps. Guard tests passed in the minimal ports; no guard shifts occurred in their closed-loop calibration. The engine API does not return storage counters, so the live engine guard-shift count was not measured. [min-1] [min-lookup] [b14-copy-b]

The standalone detector ports both matched **11,856/11,856 expected vector answers**, with zero mismatches. The expected-positive set contains **4,661 arbitrage vectors and 9 retail vectors**: matching the reference is distinct from recovering the hidden truth perfectly. Both used solc 0.8.24, optimizer 200, viaIR and Paris. [root-1-01]

| Detector port | Vector and extra checks | Gas per call, with measurement boundary | Bytes and validation scope |
|---|---|---|---|
| [bounded-bitmath] | 11,856/11,856; another 6,892 edge vectors and 1,262 helper boundary checks passed | Inline corpus min/mean/p95/max **14,316 / 17,163.9 / 18,998 / 20,193**. Corpus plus edges max **20,859**. External-wrapper corpus mean/max **37,295 / 42,375** | Source 5,670 B; harness runtime **2,949**, creation 2,977. Standalone harness compiled/tested; whole-strategy validation belongs to the integrations below |
| [literal-rational] | 11,856/11,856; 31,378 synthetic classifier cases, 1,032 rounding cases, 3,000 chance checks, exponent/rejection checks; six Forge tests passed | Warm-harness STATICCALL min/mean/p95/max **25,837 / 31,421.1937 / 34,736 / 36,904**; includes harness encoding/decoding, excludes outer meter call | Source 6,938 B; harness runtime **3,092**, creation 3,120. Backup implementation; no integrated engine scoring |
| Detector inside frozen [b14-copy-b] | 11,856/11,856; per-vector array has exactly 11,856 entries, decoded and checked in this write-up | Execution gas min/mean/max **14,352 / 17,064.486926 / 20,242**; excludes 21,000 transaction base and calldata intrinsic gas. Transaction min/mean/max **37,256 / 40,000.532473 / 43,166** | Integrated contract runtime **21,055**; full gate ledger below |

These gas measurements have different call boundaries and must not be ranked as if identical. The bounded port supports paid-side amounts/reserves below 2^128 and returns false on unsupported values or fees outside the supported cap; the literal port uses a narrower 2^120 domain and can revert on rejected inputs. Vector agreement does not prove equivalence outside those domains.

The port-parity gate changed during the goal. The original native-double TellPolicy gate failed for min-1, min-3 and min-lookup: across **90,554** closed-loop callbacks, maximum clamped bid/ask discrepancies were about **25.961659 / 15.324826 bps**, with 14 first-trade classifier disagreements. Adjacent paid doubles **9.557781723314566** and **9.557781723314564** both map to the handed integer **9557781723314565120**, while the float test distinguishes them. The requester corrected the reference on **2026-11-10 at 04:17:51Z**: use tellref.is_arb on the exact handed integers and the chance from those integers' binades, synchronize the shadow's fees to each contract return, and retain the corresponding policy/tables. The same minimal candidates then matched within **4.84e-7 bps**, far below **0.01 bps**. The old literal gate failure remains a measured failure of that reference comparison; it is not silently renamed a pass. [root-1-01]; requester notes in supplied goal.json

The following ledger uses that corrected integer-observation reference. For QPL1 and give ports, fee parity is against the candidate's own frozen tables and rule, with the engine fee cap applied. It is not a claim of 0.01-bps agreement with the uncompressed qm tables or with unavailable raw-double observations.

| Integrated port or optimization | Vector / fee-parity evidence | Runtime bytes | Largest reported strategy afterSwap engine peak | Validation and disposition |
|---|---|---:|---:|---|
| C0 lookup-headroom, source prefix 85ba1c4b | No detector added. Exact equality on 23,166 fee cases, 132,369 surface cases and 218,129 ordered callbacks | **20,128**, down 477 from C0 | No new engine peak in this item; warm Forge replay peak **164,365**, formerly 176,065 | Behavior-preserving harness evidence; no standalone strategy validation/engine score reported in this item; used as lookup base. [lookup-headroom] |
| Original c0-tell-soft1 attempt | No completed vectors or parity | Not measured | Not measured | Blocked by a 404 for imports under contracts/; later corrected to contracts/src/. [root-1-01] |
| min-1, source prefix 644bdfad | 11,856/11,856; corrected shadow max **4.84e-7 bps**, 90,554 callbacks | **23,337** | **237,653** over its later paired runs; smoke 224,063 | Validate passed; zero reported failures; retired after 512 pairs. [min-1] [root-1-01] |
| min-2 | No candidate or gates | Not measured | Not measured | Fetch failed with curl 56 / proxy CONNECT aborted. [root-1-01] |
| min-3, source prefix c522fcfa | 11,856/11,856; integer diagnostic within **4.84e-7 bps**; original float gate failed | **23,519** | **228,387**, one candidate-only gas seed | Validate passed; zero reported failures; no paired score, retired. [min-3] |
| min-lookup, source prefix 3a799de0 | 11,856/11,856; corrected shadow max **4.84e-7 bps**, 90,554 callbacks | **22,499** | **228,745**, including later reference-arm runs | Validate passed; zero reported failures; preferred to min-1 for gas/size headroom, then superseded by u1. Source flag remains. [min-lookup] [root-1-01] [root-1-02] |
| lookup-u1, source 69c361ef… | 11,856/11,856; decoder max **5.0000003e-7 bps** on 65,632 boundary + 20,000 random points; closed-loop max **4.5800971e-7 bps**, 90,448 callbacks | **20,977** | **205,358** including later reference arms; initial gas smoke 202,190 | Validate, no-assembly and six-slot checks passed; zero reported failures. Raw-cap exception and source flag remain. [lookup-u1] [root-1-02] |
| u1-give copy-a, source prefix 6fd86a65 | 11,856/11,856; corrected closed-loop max about **4.58e-7 bps**, 90,802 callbacks; rule-off sanity passed | **21,077** | **207,455**, eight gas-only runs | Validate passed; six slots, no assembly, zero reported failures. Different source from copy-b; no paired scoring of copy-a. [give-copy-a] [root-1-02] |
| **u1-give copy-b**, source 99d031f4… | **11,856/11,856**; corrected closed-loop bid/ask max **4.4848741e-7 / 4.5801182e-7 bps**, **90,802 callbacks** | **21,055** | **209,159 fresh confirmation; 209,315 selection; 207,569 initial smoke** | **Validate passed; six slots; no assembly; zero reported failures. Frozen best contract.** [b14-copy-b] [b21-c09] [b17-g7] |

For copy-b, the closed-loop gate exercised **7,470 pull moves** and **52,340 binding-bound cases**. Rule-off parity also passed on **90,448 callbacks**. Comparing the new contract with an alpha=0 shadow deliberately failed by **18.8757 / 39.2707 bps** on seed 60000, demonstrating that the gate detects the new rule. The raw, uncapped shadow bid comparison still differed by **458.6046549 bps** for copy-b, and **458.8627140 bps** for lookup-u1, where the shadow exceeded the unchanged 10% fee cap. Both executable outputs clamp to 0.1. These are **engine-clamped parity passes**, with an explicit raw-output exception. Table approximation to full qm is separately much larger: lookup-u1's shared-callback max bid/ask discrepancies were **7.0757 / 16.4904 bps**. [b14-copy-b] [root-1-01]

The initial u1 gas smoke reused its eight gas seeds after a harness called gas_stats on the wrong object. Copy-b's smoke used configuration draws seeded by indices 0–7 with simulation seeds 14002592–14002599, rather than tying both to the actual simulation seed. Those runs are calibration evidence only and supply no paired score. The subsequent selection and confirmation studies use the prescribed actual-seed configuration rule. [root-1-01] [b14-copy-b]

The table work recovered a measured portion of compression loss. Sparse spline residuals used **576 corrections**, a **2,055-byte** payload, and gained **+0.050943, se 0.004653** over the C0-compressed TellPolicy replica; the standalone Solidity lookup matched Python on **465 windows**, but an integrated detector-plus-residual candidate was not built. Estimated extra runtime cost was about **2,980 bytes**, with no measured whole-strategy gate. QPL1 u1 used a **10,160-byte** frozen payload, gained **+0.101708, se 0.006165** over that compressed replica baseline, and remained **−0.010338, se 0.004251** versus published tell_qm. The local compressed baseline was **−0.112046** versus tell_qm, so this experiment does not substantiate the assignment's historical “about 0.24” as the same comparison. [adaptive-grid] [sparse-residual] [root-1-01]

On the engine, the four three-arm u1 studies isolated **u1 − min-lookup = +0.0971045321712632, se 0.00847332349129484, n=1,024**. Their exact aggregate sum/sumsq were **99.43504094337351 / 84.86690509727319**. This is the measured recovery attributable to changing the tables in an otherwise matched contract, with runtime falling **1,522 bytes** from min-lookup. The same studies gave u1 − C0 **+3.24402671906749, se 0.0311645558612802**. Min-lookup's own 1,536 valid pairs, including those reference arms, pooled to **+3.18894060939983, se 0.0254867331000542**. These historical pools are reconstructed from the root reports and episode-5 aggregates; the individual p1–p4 raw files were not handed to this write-up. [root-1-01] [root-1-02]; goal.json episode 5

The seven completed give-selection studies isolated **u1-give − u1 = +0.0868430850264622, se 0.00711317935938385, n=1,792**, sum **155.6228083674202**, sumsq **175.90544851586614**. This justified carrying copy-b into fresh confirmation. The following rows are **selection evidence**, kept outside the primary 4,096:

| Selection result | Seeds, inclusive | Candidate − C0 | SE | Candidate afterSwap peak |
|---|---|---:|---:|---:|
| [b16-g1] | 14002600–14002855 | 3.414506 | 0.065039 | 208638 |
| [b16-g3] | 14003112–14003367 | 3.356967 | 0.060375 | 208942 |
| [b16-g4] | 14003368–14003623 | 3.326833 | 0.061154 | 208976 |
| [b17-g5] | 14003624–14003879 | 3.230223 | 0.065003 | 208150 |
| [b17-g6] | 14003880–14004135 | 3.361582 | 0.077405 | 209086 |
| [b17-g7] | 14004136–14004391 | 3.440780 | 0.064121 | 209315 |
| [b17-g8] | 14004392–14004647 | 3.344131 | 0.061610 | 208344 |

The selection pool's worst five differences were **−7.049983320971** (14003953), **−0.204693681653** (14004016), **+0.094598962954** (14003918), **+0.345321772577** (14004012), and **+0.482251011172** (14003663). The −7.05 tail is retained, even though it is outside the independently designated confirmation cohort. The missing g2 result was accepted administratively but marked invalid: only the first candidate/C0 64-seed block had an aggregate, no reference arm, empty decoded rows, no C0 runtime hash and an incorrect reference size. It contributes nothing to any pool. Its allocation was retired. [root-1-02]; goal.json episode 6

**The primary confirmation consists of sixteen complete, valid, 256-seed items of the same frozen source.** Episode 7 predeclared inclusion of every complete valid c01–c16 and r1–r4 item, regardless of its value. The completed set is c01–c09, c11–c13 and r1–r4. Every decoded row supplies both arms, all 4,096 seeds are distinct, and none overlaps the selection cohort. Each arm ran **alone against VanillaStrategy**, on matching configuration draws; candidate and C0 were not opposing pools in one match.

The protocol was **amm_sim_rs.run_batch(X, VanillaStrategy, configs, 8)**, **10,000 steps**, configuration draws in MatchRunner._build_configs order with **numpy.default_rng(actual_seed)**, and one checkpointing driver progressing through four **64-seed blocks** per arm. The scored field was **edges['submission']**, lower case. The pinned engine repository was **https://github.com/benedictbrady/amm-challenge**, commit **6b6921f8d463314aa7c96234e1be25a25245f704**. The reported unpatched wheel SHA-256 was **aedb68280aca34c110968f00148387c95885207913fb2cf19a1ab4c5cfd6887a**. The setup script SHA-256, where supplied, was **dc7fa6a1e59f5b043d3954cf68d538318b7affaf5c0db3ca69a1822680f300d4**; **c08 omits that digest**, naming the script and engine commit instead. All sixteen results, including metadata in c11's bundle, identify the same candidate/C0 source and runtime hashes. This is a record-consistency check, not an independent engine execution.

| Confirmation result | Seeds, inclusive (n=256 each) | Mean d | SE | Sum d | Sum d² | Candidate / C0 afterSwap peak |
|---|---|---:|---:|---:|---:|---:|
| [b19-c01] | 14004648–14004903 | 3.330558 | 0.063471 | 852.622892374057 | 3102.694753873266 | 208474 / 209132 |
| [b19-c02] | 14004904–14005159 | 3.333810 | 0.068220 | 853.455381339407 | 3149.066553787528 | 208527 / 209206 |
| [b19-c03] | 14005160–14005415 | 3.385783 | 0.069630 | 866.760339009437 | 3251.165751648659 | 208713 / 209276 |
| [b19-c04] | 14005416–14005671 | 3.231871 | 0.069482 | 827.358966674567 | 2989.071170097405 | 208524 / 209453 |
| [b20-c05] | 14005672–14005927 | 3.447529 | 0.060232 | 882.567486200322 | 3279.502220796348 | 208820 / 209360 |
| [b20-c06] | 14005928–14006183 | 3.347500 | 0.066953 | 856.960060367403 | 3161.303793728019 | 208890 / 208693 |
| [b20-c07] | 14006184–14006439 | 3.282404 | 0.066376 | 840.295509482361 | 3045.800695071216 | 208672 / 209652 |
| [b20-c08] | 14006440–14006695 | 3.331932 | 0.064469 | 852.974492004923 | 3113.374650327100 | 208437 / 208971 |
| [b21-c09] | 14006696–14006951 | 3.279649 | 0.063043 | 839.590047704984 | 3013.009632533438 | 209159 / 208999 |
| [b21-c11] | 14007208–14007463 | 3.318093 | 0.059905 | 849.431800268893 | 3052.754968753303 | 208835 / 209078 |
| [b21-c12] | 14007464–14007719 | 3.290092 | 0.062679 | 842.263456466697 | 3027.588926540641 | 208610 / 209100 |
| [b22-c13] | 14007720–14007975 | 3.368498 | 0.065073 | 862.335480065866 | 3181.200512619375 | 208897 / 208723 |
| [b24-r1] | 14008744–14008999 | 3.433102 | 0.066086 | 878.874127705171 | 3302.368300972847 | 208262 / 208974 |
| [b24-r2] | 14009000–14009255 | 3.394910 | 0.060482 | 869.097075384614 | 3189.308824998258 | 208666 / 208782 |
| [b24-r3] | 14009256–14009511 | 3.379951 | 0.065064 | 865.267571071347 | 3200.910783481570 | 208459 / 209677 |
| [b24-r4] | 14009512–14009767 | 3.442566 | 0.058663 | 881.296863592703 | 3258.573047554956 | 208338 / 209028 |

The labels map to goal batches as follows: b19 = e06-a-fresh-confirm-1; b20 = -2; b21 = -3; b22 = -4; b24 = e07-a-confirm-fill. Each row links the exact supplied result bytes by content digest.

Across the primary cohort, candidate Submission afterSwap **calls = ok = 44,597,387**, and C0 **calls = ok = 44,683,221**. The candidate peak **209,159** occurs in c09; C0's peak **209,677** occurs in r3. Candidate peak headroom is **35,841 gas** against the **245,000** gate. All supplied failure counters are zero. The r1–r3 artifacts retain call counts, successes, maxima and failure summaries but **omit total gas sums and full per-block gas_stats**; consequently a full-cohort mean gas cost cannot be reconstructed. No missing sum is filled with zero. For the fully specified r4 item alone, candidate/C0 gas sums are **369,641,790,915 / 390,281,739,971** over **2,828,354 / 2,831,631** calls, respectively, about **130.7k / 137.8k** per call. [b24-r1] [b24-r2] [b24-r3] [b24-r4]

Every primary paired statistic was recomputed from the supplied base64/zlib JSON rows, including all replacement items that episode 8 had only checked through reported aggregates. With d = candidate edge − C0 edge, the formulas are mean = sum(d)/n and SE = sqrt((sum(d²) − sum(d)²/n)/((n−1)n)). Item means, sums, sumsq and standard errors agree with the submitted values to floating-point rounding. Stable summation across all rows gives:

```json
{
  "n": 4096,
  "mean_diff": 3.3498905150665905,
  "se": 0.016110325843681945,
  "sum": 13721.151549712755,
  "sumsq": 50317.69458678393,
  "worst5": [
    {
      "seed": 14005601,
      "diff": -3.957261118551287
    },
    {
      "seed": 14006041,
      "diff": -3.1531325205758094
    },
    {
      "seed": 14005461,
      "diff": -0.1598181108464587
    },
    {
      "seed": 14007655,
      "diff": 0.1748110648511556
    },
    {
      "seed": 14006578,
      "diff": 0.26102153974682096
    }
  ]
}
```

The last few binary rounding digits differ from episode 8's sum-of-item-summaries result; the reported conclusion is unchanged. No standard errors were averaged, no different contract versions were combined, and no loss-making seed was trimmed.

Source-reread warnings remain on **c06 and r1**. Their raw rows and contract hashes are consistent with the other items, but that does not clear the plane's warnings; no failed source or passage was identified in the handoff. The following sensitivity pools make their effect visible. Selection-inclusive pools are secondary, since those observations helped choose the contract.

| Pool | n | Mean candidate − C0 | SE |
|---|---:|---:|---:|
| Primary, all 16 complete valid items | 4096 | 3.349890515 | 0.016110326 |
| Primary excluding source-flagged c06 and r1 | 3584 | 3.344117567 | 0.017142611 |
| Primary plus 96 completed pairs from partial c14 | 4192 | 3.351755414 | 0.015843526 |
| Selection cohort alone (g1, g3–g8) | 1792 | 3.353574602 | 0.024638897 |
| Primary plus selection (contains selection evidence) | 5888 | 3.351011759 | 0.013483405 |
| Primary plus selection, excluding c06/r1/g3/g6 | 4864 | 3.346006259 | 0.014673704 |

The c14 result is **valid but incomplete**: **96 paired rows, seeds 14007976–14008071**, mean **+3.431324420322**, SE **0.078416**; it also contains eight candidate-only rows, **14008072–14008079**, with null C0 scores. Its paired sum/sumsq are **329.40714435088034 / 1186.3826633765639**. It ran smaller chunks after timeouts and repeated unsaved attempts. Its candidate/C0 observed peaks are **208,002 / 208,876**, but the candidate totals cover 104 runs and the C0 totals 96. It is excluded from the primary complete-item pool; only its 96 genuinely paired rows enter the named sensitivity pool. [b22-c14]

c10 saved no block after an interruption; c15 compiled but had no time left for scoring; c16 failed checkpointing because its driver used the incorrect key “Submission”. Their allocations remained spent/retired, and fresh replacement allocations followed. r3 discloses **one retry of an unsaved C0 block, seeds 14009384–14009447**, allowed by the amended replacement brief. Thus “fresh” here means unused at allocation and distinct completed seed pairs, not that every unsuccessful execution attempt occurred only once. No saved primary block is reported as rerun. The 300-step driver proofs on seeds 13990000–13990001 are excluded. Final orchestration retired all engine allocations below **14009768**. [root-1-03] [b22-c15] [b24-r3] [b24-r4]; goal.json episodes 7–8

**Track C found no replica idea meeting the original +0.2 promotion threshold.** The ranking below covers every completed holdout idea, plus the two table studies assigned to A and the fixed u1-only control from the stack experiment. All listed holdout comparisons use **seeds 10000–12047, n=2,048**, against **tell_qm.json**. Entries retain the precision supplied by their sources. Tuning used separate seeds beginning at 60000; a frozen variant was scored once on holdout. Identical holdout seeds across ideas make comparisons paired, but do not make their gains additive or turn them into independent engine evidence.

“BASE” means the integer-observation stalerival policy with **a0 = ainf = 0.35**, full qm tables, soft=1: the rival-pull policy underlying the candidate, before its u1 compression. BASE − tell_qm is **+0.08860271361352773, SE 0.007079197151580293**. The corrected no-pull Gaussian control is a different baseline. Rank is by the final column's mean, not by statistical significance.

| Rank | Frozen idea / result | Increment over the stated local control | Paired gain over tell_qm (SE) |
|---:|---|---|---:|
| 1 | Quotient test on BASE, pull retained on misses, q=1/pull=1. [b25-quotient-on-base] | **+0.044300837 (0.003914150)** over BASE | **+0.132903551 (0.008267215)** |
| 2 | Retail router-quotient signal alone on TellPolicy, weight=1, ±2-ulp ratio radius. [quotient-alone] [root-1-01] | No BASE arm in this item | **+0.122855405 (0.006284516)** |
| 3 | Coarse lattice: 10-bps spacing, 31 cells, cap 12, constant pull. b18-coarse-lattice. [root-1-02] | +0.0191 (0.0049) over BASE | **+0.1077 (0.0077)** |
| 4 | Stale-rival pull: rise_fast, a0=0, ainf=0.7, tau=2. [stale-pull] [root-1-02] | +0.0121 (0.0039) over constant BASE, derived by the root merge from matching seed rows | **+0.1007 (0.0073)** |
| 5 | Retail-price likelihood: rival_sd=0.0002, strength=0.5. b23-retail-price-likelihood. [root-1-03] | +0.0058 (0.0028) over BASE | **+0.0944 (0.0072)** |
| 6 | Closed-form belief, smoothed box kappa=0.25. b18-closed-form-filter. [root-1-02] | +0.0034 (0.0029) over BASE | **+0.0920 (0.0073)** |
| 7 | Give-away: constant rival pull alpha=alpha2=0.35. [give-away] [root-1-01] | +0.093 (0.007) over its local float TellPolicy rerun | **+0.091 (0.0071)** |
| 8 | Offset residual: tuning selected [0,0,0], exactly BASE. b18-offset-residual. [root-1-02] | **0**, identical policy; all nonzero tuning offsets lost | **+0.0886 (0.0071)** |
| 9 | Rival-band evidence retry: noise_bps=5, strength=0.25. b23-band-evidence-retry. [root-1-03] | −0.00047 (0.0031) over BASE | **+0.0881 (0.0074)** |
| 10 | SD calibration: c0=−1, c1=1.1 on phases 1+2. b18-sd-calibration. [root-1-02] | −0.0010 (0.0025) over BASE | **+0.0876 (0.0071)** |
| 11 | Silent-retail/no-fill likelihood, strength=1. b23-silent-retail-evidence. [root-1-03] | −0.0012 (0.0021) over BASE | **+0.0874 (0.0071)** |
| 12 | Stack u1 tables + constant pull, frozen V1. [stack-u1-give] [root-1-02] | +0.090439 (0.007157) over V0; +0.0859 (0.0077) over corrected full-qm no-pull control | **+0.082079 (0.007715)** |
| 13 | Fine Bayes lattice, exactfast: 0.25-bps cells, no 0.995 collapse, silent steps retained. [exact-filter] [root-1-02] | +0.01022054 (0.00368330) over corrected no-pull Gaussian | **+0.00642766 (0.0036)** |
| 14 | Conditional rival pull by size/gap, alpha=1. [conditional-pull] [root-1-01] | Corrected alpha=0 holdout arm absent; the isolated effect is not measured | **−0.001694364 (0.003159986)** |
| 15 | Pin-volatility estimator: C=1, K0=500, prior 9.45 bps, bounds 8.5–10.5, DMAX=50. [pin-volatility] [root-1-01] | Corrected TellInt holdout arm absent; the isolated effect is not measured | **−0.005432120 (0.003325358)** |
| 16 | Fixed u1-only control V0 in the stack study. [stack-u1-give] [root-1-02] | −0.0046 (0.0043) versus its corrected full-qm control | **−0.0084 (0.0043)** |
| 17 | Adaptive linear-grid QPL1 u1 table recovery, frozen 10,160-byte payload. [adaptive-grid] [root-1-01] | **+0.101708 (0.006165)** versus C0-compressed TellPolicy | **−0.010338 (0.004251)** |
| 18 | Sparse spline residual SRS1 table recovery, 576 corrections. [sparse-residual] [root-1-01] | **+0.050943 (0.004653)** versus C0-compressed TellPolicy | **−0.061103 (0.005125)** |

The two small negative u1-versus-tell_qm entries come from different observation wrappers/reruns and are not duplicate measurements of an identical execution. The early table studies' local full-qm rerun differed from published tell_qm by **−0.002024, SE 0.001199**; the corrected integer Gaussian control in later studies differed by about **−0.0038, SE 0.0015**. The workers report sensitivity to binary64/libm rounding. Controls must therefore remain attached to each reported gain. Conditional-pull and pin-volatility totals also include their integer-wrapper/gamma-guard changes; without their corrected baseline holdout arms, they do not isolate those ideas' causal effects.

The following tried variants and unfinished ideas have **no additional comparable holdout score**. A blank measurement is not a zero result.

| Idea / item | What was tried or what failed | Holdout over tell_qm |
|---|---|---|
| Flag-aware fee tables, e01-c-replica/flag-aware-fee-table | Never landed; cancelled at closure. The later offset-residual experiment is only a limited proxy, not this requested table solve | **Not measured** |
| Between-pin filter, e01-c-replica/between-pin-filter | Duplicate relative path caused a file/open failure; active holdout interrupted | **No completed holdout** |
| Between-pin retry, e02-c-replica/between-pin | Still outstanding at closure; cancelled | **Not measured** |
| Rival-band-cut, e05-c-replica/rival-band-cut | Multiprocessing startup failed before any seed completed; the serial band-evidence retry is ranked above | **Not measured in original item** |
| Quotient-lite, e07-c-quotient/quotient-lite | Cheaper preimage/radius/numerator/time-gap settings were assigned; result never landed and was cancelled | **Not measured** |
| Config oracle, e07-c-quotient/config-oracle | Non-blind tuning bound using true sigma/rate/size; best of 30 coordinate trials **−0.0012, SE 0.0088** versus BASE on 65500–65755; failed its +0.04 bound and stopped before a blind variant | **Not run** |
| Truncated-normal belief alternatives within closed-form-filter | Tuning-only losses about **−1.46** on 32 seeds, **−0.71** on 16 seeds, then roughly **−0.37 / −0.30** for wider settings; misreads increased | **Not separately scored** |
| 2.5-bps latt.py lattice with tell and pull, within closed-form-filter | **−1.086, SE 0.355**, 32 tuning seeds; smears pins. This differs from the 0.25-bps fine lattice above | **Not separately scored** |
| Smaller coarse lattices, within coarse-lattice | 16 cells lost about **0.48**; 21 cells about **0.02–0.03** in tuning. A 121-cell candidate gained +0.0384 versus BASE in tuning but the predeclared one-SE rule chose 31 cells | **No separate holdout** |
| Alternative table allocations/residual budgets | QPL1 allocations starving columns lost **−0.1645 / −0.2392** versus local full tables in tuning; larger 11,475-byte payload bought no measured improvement. Sparse residual sweeps recovered less or cost more than the selected 576-entry format | **Only the frozen table variants were scored** |

These statuses and tuning values are from [root-1-01], [root-1-02], [root-1-03] and goal.json episodes 4–8. The config oracle is not blind evidence and not a rigorous bound on all possible policies. Likewise the fine-lattice “bound” experiment retained moment-based table decisions; its small gain is not a proof that all between-pin improvements are exhausted. Nothing measured recovers the brief's remaining **1.73** to true price.

The best remaining observable signal, quotient-on-base, tests whether a predicted-retail payment is consistent with an interior router split and updates rival spot toward marginal-price equality on a hit. It tested **14,591,188 callbacks**, hit **13,036,158** (**89.3427%**), and moved the rival estimate on **298,317**, or **2.2884% of hits**. The early quotient study also found **831 false hits among 13,823 synthetic full orders**, about 6%, so a hit is not proof of an interior fill. The combined holdout gain **+0.132903551** is much less than the naive **+0.122855405 + +0.088602714 ≈ +0.211458119**: the two policies exploit overlapping information. This write-up decoded all 2,048 quotient-on-base saved rows and reproduced its incremental mean and SE within the reported 1e-9 row-rounding precision. Its tell_qm total remains the item's full-precision reported comparison; the supplied pair rows contain only variant and BASE. [b25-quotient-on-base] [root-1-01]

The separate **Solidity split-test port**, e07-a-split-test/copy-b (b26-copy-b in [root-1-03]), matched **32,115/32,115** quotient vectors with zero reverts. This is a different classifier from isArb. Its full isSplit execution gas was **113,244–298,298 on hits** and **36,674–359,320 on misses**; mean hit/miss costs **140,330 / 141,573**. Runtime increment over the 2,070-byte TellMath baseline was **3,264 bytes**. isSplitLite cost **90,816–173,253 on hits**, **96,276–215,396 on misses**, added **2,562 bytes**, and made **eight errors: seven lost hits and one false hit**. No integrated strategy validation, combined callback peak or engine score exists for either.

The full split test's worst measured call alone exceeds the **245,000** callback budget. Lite also lacks exact vector parity and a combined-strategy gas proof. The two planned path-specific gas profiles both failed before measurements, so a selective later-callback or small-time-gap integration was never demonstrated to fit. The full test was not ported into the candidate. Its replica's **79.8226 average / 189 worst binary64 operations per tested callback** were operation counts, not gas predictions; the Solidity measurement supplied the actual cost evidence. No claimed recovery from an unbuilt selective version is added to the score. [b25-quotient-on-base] [root-1-03]

There was one explicit promotion-rule deviation. The requester directed the small QPL1 table recovery into A. Separately, episode 4 chose to port the **+0.091** constant rival pull as a side candidate, despite the original Track C **+0.2** threshold. It was then selected using the measured **+0.086843** engine gain over u1 and confirmed independently. This is a documented subthreshold experiment, not evidence that a C idea met +0.2. Later orchestration considered a lower quotient-port threshold, but its vector/gas conditions did not all pass and no quotient integration was made. No other C holdout gain is credited to the frozen contract.

There are further evidence qualifications. Band-evidence-retry read the first 350 bytes of tell_qm for schema validation before freezing and explicitly did not claim strict unopened-reference compliance. Retail-price-likelihood materialized the selected-parameter hash after holdout scoring began, although its driver hash and deterministic selection rule were recorded before. Silent-retail-evidence's quadrature introduced a stated **0.9423% flat-likelihood variance error at ±8 SD**, confounding attribution of its small effect. The early quotient ±2-ulp search interval is empirical, not a proof for every state. These qualifications accompany the rankings rather than being erased by positive means. [root-1-03] [root-1-01]

**The delivered code is identified by its result artifact; there is no goal code trunk or merged-wave commit to name.** The supplied goal.json has **trunk: null**, and all **27 batches** were research batches. Workers transported source and harness material in their result payloads. The engine repository/commit above is the experimental dependency, not a fabricated goal repository. For recovery, [b14-copy-b]'s **code_zb64** decodes as base64, then zlib, to **40,615 bytes of UTF-8 Strategy.sol**; this write-up verified the source hash stated at the start. Its **bundle_zb64** contains the changed replica gate, engine harness, give policy and README, with decoded SHA-256 **0b1b99501bc5753a63c303f91b67c58bae7cc40b940fcfba0a9f18198dec1377**. That is a delta harness bundle over [lookup-u1], whose own bundle and the pinned research/engine dependencies are needed for a rebuild. It is not a self-contained offline build bundled with this Markdown report.

C0 is [C0], source SHA-256 **c68887cff61180e12ba2b1ceb333edf76a830f91f63b5d775a8806fb9ec08aca**, runtime **20,605 bytes**, runtime SHA-256 **79c8d6c305ec6dfc29770b27cfb15b6cbd57b1fb01a23309cf8c131ca5c70189**. The source is the original artifact's first Solidity fence with its trailing newline, as recorded by the workers. The candidate and C0 were reported compiled with **solc 0.8.24, optimizer 200, viaIR, Paris**, importing AMMStrategyBase.sol and IAMMStrategy.sol from **contracts/src/** of the pinned engine checkout. No compilation, dependency installation or engine run was performed for this write-up.

The supplied roots cover successive subsets of the goal. Their statements that a probe or 4,096-seed carry was “missing” apply to their own inputs, not to the combined record: root 1 provides the probe and early ports, root 2 adds give-selection/gates, and the directly handed confirmation rows complete the primary cohort. Their headline pools overlap and were **not summed**. Root 3 also says individual means straddle +3.48, but every primary item's mean in the table above is below +3.48; this report uses the row-derived numbers. [root-1-01] [root-1-02] [root-1-03]

Source warnings were not resolved by this write-up. Beyond c06/r1, they affect **retail-quotient-signal, min-lookup, lookup-u1, g3, g6, coarse-lattice, sd-calibration and silent-retail-evidence**. The earlier root reports describe failed source rereads but do not supply the precise failed URL/passage for each. Content hashes and internal arithmetic establish identity/consistency, not the truth of an unavailable quotation or the correctness of an execution. The primary and selection sensitivity pools show the numerical effect of removing flagged engine items; they do not rehabilitate citations.

The following operational failures and missing work remain explicit:

| Work | Recorded outcome and what remains absent |
|---|---|
| Initial integration imports | HTTP 404 for contracts/AMMStrategyBase.sol; subsequent ports fixed the path to contracts/src/. The failed attempt itself produced no gate evidence |
| Initial shared gate/paired runner | Setup exited 133 with an execution-loader failure; later items supplied their own runners |
| Independent engine probe | Harness dependency/path error; no independent eight-run probe |
| min-2 | curl 56 / proxy CONNECT aborted; no contract |
| g2 selection | Invalid partial export and empty rows; excluded, no invented replacement statistics |
| c10 / c15 / c16 | Interrupted unsaved block / compilation consumed available time / incorrect edge key; no completed pairs; fresh replacement items supplied confirmation |
| c14 | Only 96 complete pairs, eight further candidate-only rows; primary exclusion and separate sensitivity treatment |
| Gas-profile copy-a / copy-b | Venv setup failed because ensurepip was unavailable / python3 unavailable; **no path-specific profile** |
| Split-test copy-a | Never landed; cancelled. Copy-b supplies detector-only evidence, not an integrated strategy |
| Flag-aware tables, between-pin retry, quotient-lite | Never landed; cancelled. No scores or behavioral claims substituted |
| Board performance and first place | No entry, current board fetch, board-speed check or measured rank change |
| Stronger correctness/gas claims | No universal worst-case gas proof, no proof of zero detector misses in all states, no strict original raw-float/full-qm parity pass |

Failure descriptions are reported worker outcomes, not inspection of this write-up's execution machine. No missing measurement, code repository, commitment, gas sum or leaderboard result was fabricated.

The closing snapshot used **77 of 160 item allocations**, leaving **83** unspent. Four batches had outstanding items and were marked cancelled at finish; an administratively accepted result may still be blocked or invalid, as g2 and the setup failures show. The supplied batch briefs are **truncated previews**, commonly ending in an ellipsis after their setup/source clauses. Their visible wording and episode notes describe one detector, port, paired seed allocation, probe or replica idea per item, with expected gates, paired fields or blocked outcome; this handoff cannot independently certify the complete output clauses of every historical brief. No new batch was issued during this write-up.

For the reference's decision-object shape, the closing decision is recorded below inside the sole authorized report output. It records the completed handoff and does not create or execute further orchestration:

```json
{
  "notes": "Finish the write-up from the supplied results. Retain frozen u1-give copy-b, source SHA-256 99d031f41074ea872c78fa7dec5db33d9f20f3251e29bdbb4682c92791334b72. Fresh confirmation: n=4096, mean gain over C0=3.3498905150665905, SE=0.016110325843681945; candidate afterSwap peak=209159 and reported OutOfGas=0. The implied score 528.2898905150666 is below the request-pinned first-place score by 0.1301094849334. No entry or new simulation. Preserve the one missed arbitrage in the 35-bps probe, source flags, missing gas/profile/unfinished-idea measurements, raw-cap parity exception and subthreshold promotion deviation. No goal trunk exists. Nothing was fabricated.",
  "finish": true
}
```

This write-up checked all **30 supplied input SHA-256 identities**, parsed the 27 JSON item results, decoded available paired rows, checked their statistics and seed uniqueness, checked the reported failure counters and role-specific peaks, verified the candidate source payload and available declared payload hashes, and decoded the candidate's per-vector gas array. The quotient incremental statistics were checked within stored row precision. No supplied executable was run. These checks establish document and arithmetic consistency only; they carry no independent authority over the reported simulations or contract behavior.

The links below resolve by immutable result digest. For results available only through a root merge, citations to that merge identify the supplied evidence; an original-result link is a recovery pointer, not a claim that its remote endpoint was re-fetched here.

[b17-g5]: https://api.imd.fun/artifacts/254cc414fbd891d2eea199bb4fa54b452a4e4fc6235ac54431a763d735da2f3c
[b25-quotient-on-base]: https://api.imd.fun/artifacts/88712dac0e4b048a0860ccb13d2f22e13d956161c102939cb480f53388f3b185
[b19-c03]: https://api.imd.fun/artifacts/cce670bfa15045fc42ff54cb693b50ccec66c2219f0ac4e57fb34858ef9f49a6
[b20-c05]: https://api.imd.fun/artifacts/113d6b87d70ab86de0bf17ae10cbd78feae7d01a3f915b31a1987155082542be
[b20-c08]: https://api.imd.fun/artifacts/551301e742356ba88d7a02a43146ba5e850e79cac9eb3cfd103aae68e7067455
[b19-c01]: https://api.imd.fun/artifacts/53579a588449b8aaf3da3f6533707f907510dd715757adbf85b6c91b7fbc8fac
[b21-c12]: https://api.imd.fun/artifacts/60fecd9e4635301f1b383eaa6b2eab405ea31a31a36a15cf97def134d6ffc15f
[root-1-01]: https://api.imd.fun/artifacts/c5ea99de2d3c7b9ed3dc6681c642a29e6e07e347c0f3a47fe9135f7fd9cbad11
[b16-g1]: https://api.imd.fun/artifacts/42ecdae1702175005b28b53640b7fe33150e1ad29e4d363b93f35c0ebaecfc8f
[b24-r2]: https://api.imd.fun/artifacts/dbc5f44ea18abd780024f9e166257e3a3e5e3216e04445b19a3d39c8e197e2f3
[b22-c13]: https://api.imd.fun/artifacts/9eaead7fc8a396f59edd1e12582de80eff4cc0b7f25223bdd6f2a04fce608d13
[root-1-03]: https://api.imd.fun/artifacts/2caa5518a6806b0b6b37ccb70e3b3fe16450e1b4c460771776e5a3966ab71287
[b21-c11]: https://api.imd.fun/artifacts/b5df1fcb0297b2927f225649d09cc272d571939fafe679fce17eb07bcf3f27f7
[root-1-02]: https://api.imd.fun/artifacts/80c068e857d2de60bfc4c707f18c977467303b3da986064daa50fdd846e6a796
[b14-copy-b]: https://api.imd.fun/artifacts/fd2f147e94f3523e4c4f91e43dc98b88e9ce8ef1060d2939367445711154a16a
[b20-c06]: https://api.imd.fun/artifacts/e641cf070046c696cfe148ab07c78b04a9f04aea16111e94d1dd741c19a0794b
[b21-c09]: https://api.imd.fun/artifacts/b4e6ded235289268c6779411548cb67dd4f38946dabfe8dd52a621c933c96aff
[b20-c07]: https://api.imd.fun/artifacts/b90a42ad1da2bf4f1febdfbd4eda24e25afdeaa16235d60d556c09c48732d41e
[b17-g6]: https://api.imd.fun/artifacts/2c2e3249a7e332a725dc867b4c7549c50a41636ca03fdfd145bc4345d00be207
[b16-g4]: https://api.imd.fun/artifacts/407a30d4c8a6d71cb390585cbdc38350447c0b1e9f1538842524f4c147a1c82a
[b22-c14]: https://api.imd.fun/artifacts/cb21620af6f8ec70b7740f27bdff59c554143094c1d0c6e5fb247a8dc36622ba
[b22-c15]: https://api.imd.fun/artifacts/297addf6bfc48f70f6a5da8ba096336257d38240cc797adc17a012e6edae4da9
[b24-r4]: https://api.imd.fun/artifacts/5d74385cf880d54c355c13a891c2b6278185b427c6f34bbd7eacb015cb73ec6a
[b24-r1]: https://api.imd.fun/artifacts/41fef3ac6c13e589b53470704fc04e413d4ae94ffd9051aea126efbdc9eb3671
[b19-c04]: https://api.imd.fun/artifacts/70cf6fbdef930116f46c63587abe36fb73b214b8ab89e56d4ca80f247b938978
[b19-c02]: https://api.imd.fun/artifacts/2e9a25f09f69155647ad158d886debe6655b163af2e9118598eab5565f34384a
[b16-g3]: https://api.imd.fun/artifacts/f9b272bcde4c784af316279a36a833b5a7ca66453fb19f9eb7d7c2cf5716f694
[b17-g7]: https://api.imd.fun/artifacts/13306c7aed7f0ccbb1379f5b8dcf41fa4992281cb782bf79c7666b3f54e62d54
[b17-g8]: https://api.imd.fun/artifacts/3c9962c4395652c0b9da8bb707730b5a9409ddda3501ac4b5328949b2bd9223c
[b24-r3]: https://api.imd.fun/artifacts/8d4cd55e0b4ed75c0d25bd92785dd986f0e4910f67a34100eb7177d2d2094c89
[probe-result]: https://api.imd.fun/artifacts/b0cb4b28e101ad902ec383c2d4142b6e9a9dd10d229f482b47ca81b273933495
[bounded-bitmath]: https://api.imd.fun/artifacts/22122152083d7c876b3475c321fd3c85be79de48419965491d117f095e3d1905
[literal-rational]: https://api.imd.fun/artifacts/122533c069dcbd6787c736a7578ab603ca092c90409e9bd6a344bddf94863a38
[lookup-headroom]: https://api.imd.fun/artifacts/9093159ef6d83b4f6f8c0368355cec5771548c9e9ab3cb9608885007afa43741
[min-1]: https://api.imd.fun/artifacts/6a27a64088c1f95bd06f5b7b2bb6570ecbaf96ea7323c8718b32e79224dc3a16
[min-3]: https://api.imd.fun/artifacts/4486cd24cc4728ae80c6c62be6afbd08ca1702f5ff38896911848f19fd43e849
[min-lookup]: https://api.imd.fun/artifacts/755f4fc0a7b028497ad9ddf23ea568071192341e192335cb7f31174d066d4df0
[lookup-u1]: https://api.imd.fun/artifacts/fd38823c16c850438759b77387cecd713241ff3f0b6d5280ef161c6717375ed8
[give-copy-a]: https://api.imd.fun/artifacts/72875662697bad4d0cb848934e20dca2e834fa4bce69dfd49a916dab6e27753b
[C0]: https://api.imd.fun/artifacts/8a6e303b662e1a5ea9bb47f31acedd3988ef65b3ddb66d074517aa59ad41ca40
[adaptive-grid]: https://api.imd.fun/artifacts/ce5b4e6f21a08070df1df5e784c374eaf555f1540405c1c33864a710683fe8d8
[sparse-residual]: https://api.imd.fun/artifacts/cc3998563369642f4867cdc5780ca2a7bcdbee80e66fc17e8cf3fbfa8afee701
[quotient-alone]: https://api.imd.fun/artifacts/bb1b85910e7628d6c716ee1328da911b4da42c0903cb6c96309cfda82a379abd
[give-away]: https://api.imd.fun/artifacts/e931451c8e4b3ace70dbcde4910728e086fb292489bccaab0bf9c5c3be72fe14
[conditional-pull]: https://api.imd.fun/artifacts/631a50b4823943d5614ffb901519d34f9dbbb3a6fdce025594edeb70f4abc663
[pin-volatility]: https://api.imd.fun/artifacts/751a83dfca0c3871042a18f326de6b6a7b21afd63fe40c74d705576c7837c809
[stack-u1-give]: https://api.imd.fun/artifacts/16a3c22200b8e134cf8af61ccde36fada98a5c98299a29c37a9ea8d3247a65b2
[exact-filter]: https://api.imd.fun/artifacts/4c0dc590134f3bb9eb0256435bb83825c6efb651035870380f53878f81d20c9b
[stale-pull]: https://api.imd.fun/artifacts/f5a140f51df99423d6ede60b618dbc6eabc37a3050ac439c80dc3824191e9f59

