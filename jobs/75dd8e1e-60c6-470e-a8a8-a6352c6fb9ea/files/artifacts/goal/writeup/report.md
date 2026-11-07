# Retreat-cancel on m-plus-a and m-plus-b

**Recommendation: submit m-plus-b plus retreat-cancel as the next entry.** Both bases show a positive average gain from the wrapper after completing the missing measurements. I prefer the wrapped B file because its measured incremental downside is smaller and its gain is estimated more precisely. This is a choice based on the wrapper's measured benefit and risk, **not proof that B has the best absolute score**: A and B were measured on different seed sets, and neither merge identifies which base produced swarm #1042. The evidence below supports adding the wrapper to either base; it does not resolve that identity. Sources: [merge-01][M1], [merge-02][M2], original A/B inputs linked in the block tables, and [B10 completion](#completion).

The goal supplied the historical context: 2nd at **110.21** (imd.fun swarm **#1042**), 1st at **110.69**; the earlier m-all wrapper result was **+0.37**, **se 0.12**, **1,000** fresh seeds, worst single run **−57.8**. These are the requester's figures, also recorded in [the public goal][G], not newly verified board standings. The new gains are simulation edge per seed; adding them to a board score would not predict a new board result.

## Results and coverage

Let d = wrapped strategy total_edge − base strategy total_edge for the **same seed and sampled configuration**. Positive d means adding retreat-cancel helped. All means weight seeds equally. Sources: original item `notes`, `per_seed`, `overall`, `by_spread`; [pinned simulator runner][RUNNER]; [completion](#completion).

| Base | Completed paired seeds | Pooled gain | Standard error | Gain / SE | Incomplete blocks now | Blocks reporting failed pairs now |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| m-plus-a | 5,000 | +0.329660 | 0.069407 | 4.75 | 0 | 0 |
| m-plus-b | 5,000 | +0.398317 | 0.039061 | 10.20 | 0 | 0 |

Source: pool the block moments below; all original `failures` lists are empty and the completion checks both engine failure flags. A covers **700000–704999**; B covers **705000–709999** exactly once per base. The [embedded datasets](#data) contain every recorded seed difference and spread, including zeros. Coverage is checked from the rows rather than inferred from block endpoints.

Both pooled gains exceed twice their SE. A normal approximation mean ± 1.96 SE gives A [0.193623, 0.465698] and B [0.321757, 0.474878]. These intervals describe uncertainty in the sampled mean; they do not bound a single run or guarantee performance on board seeds. Calculated from the same pooled moments.

**Original completeness versus repaired completeness:** A originally had 10 complete blocks and 0 incomplete/failed blocks. B originally had 9 complete blocks, **1 incomplete block (B10)** and 0 blocks reporting failed pairs: 4,787 pairs, 213 unmeasured seeds. This revision adds exactly those 213 pairs, so both final experiments have ten blocks of 500. An empty failure list alone was never evidence that B10 was complete. Sources: [M1][M1], [M2][M2], all original item `n`, `complete`, `failures`, and [completion](#completion).

For comparison with merge-02, its original partial B pool is reproduced: gain **+0.400306**, SE **0.040331**, n = 4,787. Its nine complete blocks alone give **+0.419027**, SE **0.037308**, n = 4,500. Those historical summaries are retained as sensitivity checks, not substituted for the completed experiment. Sources: B01–B10 original moments below and [M2][M2].

## Gains by competitor spread

Means below condition on that spread; counts are the actual sampled counts, not forced equal weights across spreads. Sources: original A01–A10/B01–B10 `by_spread`, supplemented by the new B10 seed rows.

| Base | Spread | Pairs | Sum d | Sum d² | Mean gain | SE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| m-plus-a | 1 | 1261 | 0 | 0 | +0.000000 | 0.000000 |
| m-plus-a | 2 | 1269 | 509.9459533699 | 74186.6329558942 | +0.401849 | 0.214423 |
| m-plus-a | 3 | 1263 | 1138.3555800754 | 46766.0052621321 | +0.901311 | 0.169401 |
| m-plus-a | 4 | 1207 | 0 | 0 | +0.000000 | 0.000000 |
| m-plus-b | 1 | 1200 | 0 | 0 | +0.000000 | 0.000000 |
| m-plus-b | 2 | 1285 | 1073.7252785205 | 25286.8361567104 | +0.835584 | 0.121582 |
| m-plus-b | 3 | 1234 | 917.862015266099 | 13643.7836527669 | +0.743810 | 0.092296 |
| m-plus-b | 4 | 1281 | 0 | 0 | +0.000000 | 0.000000 |

Spreads 1 and 4 have zero measured effect. The inspected wrapper returns its incumbent actions unchanged outside spreads 2 and 3; it cancels and suppresses placement on a side for one callback when the rival retreats one tick on that side. [RC artifact][RC], exact suffix after [N][N]. A's spread-2 gain does not exceed 2 SE; A's spread-3 gain does. B's spread-2 and spread-3 gains each exceed 2 SE. These comparisons use the table above and describe this fixed wrapper, without selecting or modifying spread behavior after measurement.

## Worst five runs for each base

Ranked by the smallest paired **d**, including the newly measured B10 seeds. These are losses from adding the wrapper, not either strategy's absolute outcome. Values retain the source rows' six decimal places. Sources are linked per row; the complete rankings can be regenerated from the embedded datasets.

| Base | Rank | Seed | Spread | Wrapper minus base | Block/source |
| --- | ---: | ---: | ---: | ---: | --- |
| m-plus-a | 1 | 702116 | 2 | -197.439735 | [A05](https://api.imd.fun/artifacts/df9ee1bfa282422174e98acfcc73b7c834f49d19856c0a0fb5371ad7a8ae3697) |
| m-plus-a | 2 | 702325 | 3 | -144.452526 | [A05](https://api.imd.fun/artifacts/df9ee1bfa282422174e98acfcc73b7c834f49d19856c0a0fb5371ad7a8ae3697) |
| m-plus-a | 3 | 700179 | 2 | -65.330784 | [A01](https://api.imd.fun/artifacts/b96498828bedc0567619f288a3a2b2f4bbf1ccbabb82201a662d856c9f1f7e0f) |
| m-plus-a | 4 | 703795 | 2 | -63.604819 | [A08](https://api.imd.fun/artifacts/0b5f5623c80fc3d035551b4076d59f3f36fdbf4c16483569e1952d57cc69e9a4) |
| m-plus-a | 5 | 703512 | 2 | -36.449454 | [A08](https://api.imd.fun/artifacts/0b5f5623c80fc3d035551b4076d59f3f36fdbf4c16483569e1952d57cc69e9a4) |
| m-plus-b | 1 | 709790 | 2 | -90.875201 | [B10](https://api.imd.fun/artifacts/516d5cf7baf748ffd1f544312606942ee035f0ba65eba8d0951d39f86c36506c) |
| m-plus-b | 2 | 708875 | 3 | -55.473471 | [B08](https://api.imd.fun/artifacts/fe607b701c06e502ee0c166ab61bb64f012f200ddce209e76d2b73eb59e7040a) |
| m-plus-b | 3 | 707780 | 3 | -38.644767 | [B06](https://api.imd.fun/artifacts/b277dafb95843e7357b4f20bfe94fbe5d9f9b3ae8f27ef3fc39adc423eff3c5e) |
| m-plus-b | 4 | 705337 | 3 | -27.088252 | [B01](https://api.imd.fun/artifacts/1fb3f6456c9118ecceb6a66eafdd0fbbcf3b3e53b7f2e12e25724752ceef4a22) |
| m-plus-b | 5 | 705899 | 3 | -20.236248 | [B02](https://api.imd.fun/artifacts/6933986c635778830f6579341c839867ff53a1037a0e0ba9bc22fd8dc3b7b12f) |

Both wrappers can cause large losses on individual runs despite a positive pooled average. The earlier m-all worst run (−57.8, requester's historical figure) came from a smaller experiment on a different base; it is not a loss limit for these files. B's better observed incremental tail is one reason for the recommendation, not a guarantee that its future worst loss will be smaller.

## Block moments and pooling

For a pool, N = sum(n), S = sum(sum_d), Q = sum(sum_d2). Compute **mean = S/N** and **SE = sqrt((Q − S²/N)/(N(N−1)))**, equivalent to the sample standard deviation of d divided by sqrt(N). Block SEs are not averaged. All seeds, including the worst runs and the formerly missing B10 seeds, remain in the headline results. Sources: original item statistics and their stated sample-SE convention; arithmetic is independently recomputed here.

### m-plus-a

| Block | Seeds (inclusive) | Pairs | Sum d | Sum d² | Mean gain | SE |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| [A01](https://api.imd.fun/artifacts/b96498828bedc0567619f288a3a2b2f4bbf1ccbabb82201a662d856c9f1f7e0f) | 700000–700499 | 500 | 170.5421106717 | 11257.0105734431 | +0.341084 | 0.211861 |
| [A02](https://api.imd.fun/artifacts/1e265044d9fe6f4bac495442338f135b61f9af49bfd316f20b1fb2d6b63bdccc) | 700500–700999 | 500 | 274.32808 | 11398.252679 | +0.548656 | 0.212323 |
| [A03](https://api.imd.fun/artifacts/e64aba96fca95ecde4fb4a13bf6ec0e79fffd3fc55591f36ca14e5d1ad3f7618) | 701000–701499 | 500 | 201.7862779676 | 5585.70257061752 | +0.403573 | 0.148530 |
| [A04](https://api.imd.fun/artifacts/b6abf01484c1f4eb4670d6518ef2c0b1ab7bf0d0bea219f6b3440d81acd244d5) | 701500–701999 | 500 | 243.9907570433 | 3383.27039894778 | +0.487982 | 0.114381 |
| [A05](https://api.imd.fun/artifacts/df9ee1bfa282422174e98acfcc73b7c834f49d19856c0a0fb5371ad7a8ae3697) | 702000–702499 | 500 | -157.242862 | 63554.255819 | -0.314486 | 0.504508 |
| [A06](https://api.imd.fun/artifacts/74aa13178078172b575082bf064ded078803b60b74cb973dd9f015f58424839b) | 702500–702999 | 500 | 196.5232864688 | 4697.26018472806 | +0.393047 | 0.136078 |
| [A07](https://api.imd.fun/artifacts/60e9de2df432c291f19c196ea97a92b13e69cef01bbb8096d607af96378ecd36) | 703000–703499 | 500 | 257.353795 | 4315.410292 | +0.514708 | 0.129481 |
| [A08](https://api.imd.fun/artifacts/0b5f5623c80fc3d035551b4076d59f3f36fdbf4c16483569e1952d57cc69e9a4) | 703500–703999 | 500 | 94.6205647809002 | 11361.2860938169 | +0.189241 | 0.213224 |
| [A09](https://api.imd.fun/artifacts/760c087384b9826ec86a2487ac28ead78ee0f8dfd57f61165e18c8885c095e82) | 704000–704499 | 500 | 119.0147454569 | 3819.03917837119 | +0.238029 | 0.123261 |
| [A10](https://api.imd.fun/artifacts/ad03c7b6649949346f63defa0e00128291130d2da56672a854f2c4afcc862b91) | 704500–704999 | 500 | 247.3847780561 | 1581.15042810185 | +0.494770 | 0.076464 |

Pooled moments: N = 5000, S = 1648.3015334453, Q = 120952.638218026. [M1][M1] flags a source quotation in A02 as uncorroborated. Its recovered measurement rows are internally consistent; excluding the entire block still gives gain **+0.305327**, SE **0.073421**, n = 4,500. A02 is retained. This write-up does not certify its originally cited quotation.

### m-plus-b

| Block | Seeds (inclusive) | Pairs | Sum d | Sum d² | Mean gain | SE |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| [B01](https://api.imd.fun/artifacts/1fb3f6456c9118ecceb6a66eafdd0fbbcf3b3e53b7f2e12e25724752ceef4a22) | 705000–705499 | 500 | 172.3663163325 | 3755.21441104799 | +0.344733 | 0.121708 |
| [B02](https://api.imd.fun/artifacts/6933986c635778830f6579341c839867ff53a1037a0e0ba9bc22fd8dc3b7b12f) | 705500–705999 | 500 | 259.7378386064 | 3212.75811810848 | +0.519476 | 0.111068 |
| [B03](https://api.imd.fun/artifacts/3c599834ca300a92963465d462cfbafd320e2bc9f072003e282094463c07dcf5) | 706000–706499 | 500 | 249.1665836051 | 2348.85204334104 | +0.498333 | 0.094428 |
| [B04](https://api.imd.fun/artifacts/4e0e3a4e05a9549ac20768bec49fcb3b4019f8e5cae426a2efaa154937ebc8ed) | 706500–706999 | 500 | 198.472254086 | 3236.7663891201 | +0.396945 | 0.112504 |
| [B05](https://api.imd.fun/artifacts/ad8b48d0549c780285910d62aded1161e483e19476c83bb79c6241176a45663b) | 707000–707499 | 500 | 163.414003 | 2308.010095 | +0.326828 | 0.095060 |
| [B06](https://api.imd.fun/artifacts/b277dafb95843e7357b4f20bfe94fbe5d9f9b3ae8f27ef3fc39adc423eff3c5e) | 707500–707999 | 500 | 123.8299972813 | 3185.85822358157 | +0.247660 | 0.112455 |
| [B07](https://api.imd.fun/artifacts/3e3cfc0f4c04b23af7cd9f733fc9af83ad7ed42c419ef3e074cbd9b8b25dd9e3) | 708000–708499 | 500 | 242.351745 | 2316.898419 | +0.484703 | 0.093890 |
| [B08](https://api.imd.fun/artifacts/fe607b701c06e502ee0c166ab61bb64f012f200ddce209e76d2b73eb59e7040a) | 708500–708999 | 500 | 226.409778118999 | 6370.22475835438 | +0.452820 | 0.158496 |
| [B09](https://api.imd.fun/artifacts/241739e7ad50c5baa17c8f85050bf24ecfb6f58ec379554a344bb40a3afffef6) | 709000–709499 | 500 | 249.8729811801 | 2234.64783230942 | +0.499746 | 0.091957 |
| [B10](https://api.imd.fun/artifacts/516d5cf7baf748ffd1f544312606942ee035f0ba65eba8d0951d39f86c36506c) + [completion](#completion) | 709500–709999 | 500 | 105.9657965762 | 9961.38952061429 | +0.211932 | 0.199588 |

Pooled completed moments: N = 5000, S = 1991.5872937866, Q = 38930.6198104773. B10 originally had n = 287, S = 30.6415247093, Q = 9064.43483120505; adding the independently measured n = 213, S = 75.3242718668997, Q = 896.954689409241 gives the completed B10 row. Source: [B10](https://api.imd.fun/artifacts/516d5cf7baf748ffd1f544312606942ee035f0ba65eba8d0951d39f86c36506c) and [completion](#completion).

Rounding is retained rather than forced into agreement: B07's spread-specific Q values sum to 2316.898418 while its overall Q is 2316.898419. Overall and spread pools each use their own source moments; this 0.000001 discrepancy does not affect the displayed gains or SEs. [B07](https://api.imd.fun/artifacts/3e3cfc0f4c04b23af7cd9f733fc9af83ad7ed42c419ef3e074cbd9b8b25dd9e3), [M2][M2].

## What was recovered, checked, and corrected

The reviewer correctly identified the evidence gap in the prior report: aggregate moments and five deltas cannot stand in for every seed, and B10 was unfinished. This revision recovered all twenty original item JSON files using the public job's [accepted-file manifest][MANIFEST], verified their bytes against its SHA-256 identifiers, and retained all seed rows below. The supplied merge files themselves also match their assigned SHA-256 identifiers ([M1][M1], [M2][M2]); the original sources are now linked directly rather than through unavailable local paths.

For each original item, checks covered count, unique seed IDs, assigned-range membership, spread counts, smallest-five rankings, strategy hashes, and moments against six-decimal seed rows within rounding error. Spread labels for every seed were independently compared with `sample_config` at the pinned commit. The original A dataset has 5,000 unique rows; original B has 4,787, with exactly the gap listed below. No seed rows were inferred from aggregate statistics. Sources: twenty linked input files and the embedded data.

The A merge has two contradictory prose statements: it calls spread 3 positive in every block while listing a negative A05 spread-3 mean, and calls all five worst runs spread 2 while identifying the second-worst as spread 3. Recovered rows and the merge's tables agree: A05 spread 3 is negative, and seed 702325 is spread 3. The report uses those rows rather than the contradictory prose. [M1][M1], [A05](https://api.imd.fun/artifacts/df9ee1bfa282422174e98acfcc73b7c834f49d19856c0a0fb5371ad7a8ae3697).

The item notes report varying Python versions and some concurrent execution/restarts. The current completion uses Python 3.12.3, serial in-process execution, no simulator sandbox or workers, and a newly loaded strategy factory for each run. Prior provenance is retained as reported, not presented as a fresh rerun of every original simulation. [M1][M1], [M2][M2], original item `notes`.

<a id="completion"></a>

## B10 completion and strategy identity

Original B10 lacks these inclusive ranges: **709508–709562 (55), 709830–709877 (48), 709884–709940 (57), 709947–709999 (53)**, totaling **213**. Those exact seeds were run; no replacement seeds were chosen. Source: original [B10](https://api.imd.fun/artifacts/516d5cf7baf748ffd1f544312606942ee035f0ba65eba8d0951d39f86c36506c) `per_seed`, verified by set difference. The embedded completion data retain each new seed's BASE and CANDIDATE total edges so the subtraction can be inspected independently.

The exact base code is available in [m-plus-a][BASEA] and [m-plus-b][BASEB]. N and RC were recovered from their named artifacts, `RC.startswith(N)` was checked, and each candidate was built as **BASE + RC[len(N):]**, with no strategy changes. The wrapper suffix is **1,950 UTF-8 bytes**. These recovered code hashes exactly match every original item:

| File | SHA-256 of UTF-8 strategy code |
| --- | --- |
| m-plus-a | `5d1bd5272884f513b19f0e66a7c235f6c188a08e4f7787ac9346f1614dda3ed3` |
| m-plus-a + retreat-cancel | `0d627e80d1c3ecb98da2ccddf7406e301c76e59ab86c4ee068e508b6074f76ac` |
| m-plus-b | `4f9167dddd457f394e988bf9c9e2576dd6120834bfb8d93573ce9451fd587598` |
| m-plus-b + retreat-cancel | `02696ea6fd0922f64167a1153748f6a38bf2fd5d87c7a4ac6cb974bb9482f57c` |

Simulator: [danrobinson/prediction-market-challenge at b244530ee2a6247b5f930830eeca9dd950da0e7e][SIM], checked out at that commit with no tracked modifications. For each new seed s: `cfg = sample_config(ChallengeConfig(), ParameterVariance(), seed=s)`; run BASE first and CANDIDATE second using `SimulationEngine(cfg, load_strategy_factory(path), seed=s).run()`, reloading each factory. Both engine failure flags were false for every new pair. Sources: [runner][RUNNER], [loader][LOADER], new paired totals below.

Before filling gaps, ten existing pairs were rerun: B seeds 709500, 709501, 709502, 709503, 709790, 708875; A seeds 700000, 700001, 702116, 702325. Every spread and six-decimal d matched; available first-four BASE check values also matched within 1e−8. This corroborates strategy identity and execution on those seeds, including the largest reported losses; it is not a rerun of all original pairs. Sources: original item `check_values`/`per_seed`; the retained check totals below.

| Base | Check seed | Spread | BASE total edge | CANDIDATE total edge | d |
| --- | ---: | ---: | ---: | ---: | ---: |
| b | 709500 | 3 | 15.0068604734 | 15.6055028825 | +0.598642 |
| b | 709501 | 1 | -0.1291820085 | -0.1291820085 | +0.000000 |
| b | 709502 | 1 | -0.1586217964 | -0.1586217964 | +0.000000 |
| b | 709503 | 1 | -28.0093101371 | -28.0093101371 | +0.000000 |
| b | 709790 | 2 | 79.0897077735 | -11.7854935248 | -90.875201 |
| b | 708875 | 3 | 248.6909789193 | 193.2175079264 | -55.473471 |
| a | 700000 | 3 | 109.8256742104 | 111.1986577075 | +1.372983 |
| a | 700001 | 3 | 592.3142193551 | 595.0711372413 | +2.756918 |
| a | 702116 | 2 | 110.8187283084 | -86.6210067737 | -197.439735 |
| a | 702325 | 3 | -451.9518723482 | -596.4043988212 | -144.452526 |

## Limits on choosing a submission

The wrapper's gains are measured relative to each base, not between the two bases. B minus A in estimated wrapper gain is +0.068657; treating the disjoint seed pools as independent gives SE 0.079644 for that difference. That is not strong evidence of a larger wrapper effect on B, much less a test of the files' absolute scores. Comparing their unpaired absolute edge means would confound strategy differences with sampled market conditions. The recommendation favors B's more precisely estimated gain and smaller observed incremental worst losses; it does not claim statistical superiority over A plus RC. Sources: pooled moments and worst-run table above; calculation assumes independent seed draws.

Which base was #1042, the private board seeds, and a current board score for either candidate could not be established from the goal or these artifacts. No board submission was performed. The completed measurement is sufficient to assess the fixed wrapper's average gain and observed downside on both assigned seed sets. It cannot guarantee overtaking 110.69. Sources: goal [G][G], [M1][M1], [M2][M2]; no new board result is asserted.

<a id="data"></a>

## Offline evidence: every seed

To fit the single-file byte limit, both complete datasets are embedded as losslessly compressed data. **Nothing must be downloaded or installed to inspect them.** Copy the Python decoder below to a file and run `python3 decoder.py artifacts/goal/writeup/report.md`; it prints all 10,000 seed records as CSV, and recomputes overall/per-spread means, sample SEs and worst-five lists to stderr. It checks payload hashes, contiguous seed coverage, spreads, counts and new-pair subtraction.

Encoding: Base64 of zlib-compressed bytes. A/B raw records use little-endian `struct` format `<Bi` (one unsigned spread byte, one signed 32-bit integer d × 1,000,000). Seed IDs are exactly 700000 + row index for A and 705000 + row index for B; each has 5,000 records in increasing seed order. Thus every zero is retained and seed coverage is explicit. Source d values were already rounded to six decimals; this encoding preserves them exactly, including newly measured d rounded by the same rule. The completion payload uses `<Idd`: unsigned 32-bit seed, BASE total_edge double, CANDIDATE total_edge double, ordered by seed. It has 213 records and retains unrounded engine totals. Raw payload SHA-256:

| Payload | Raw bytes | SHA-256 |
| --- | ---: | --- |
| a | 25000 | `44d4896441dfedfdffa704f2cf033ac36d52ce7f675e747da4fac63263ce738a` |
| b | 25000 | `862f879e5e73a27a76de26ba4c431c4246e3367451d6e2d23b61829d80128f33` |
| completion | 4260 | `45988f0148eaee5065030ce377d73430c438ec02efc8d128188113968f3a9044` |

The moment tables use source aggregates computed before per-seed rounding, plus full-precision new differences. Recomputing from the embedded six-decimal d values changes only later digits; headline gains and SEs agree to six decimal places. The original records do not give absolute BASE/CANDIDATE edges for every seed, so those cannot be supplied for the old pairs. The complete paired differences, spreads, coverage and tail rankings are supplied; new pairs additionally retain both absolute totals.

```python
import base64, csv, hashlib, math, re, statistics, struct, sys, zlib
from pathlib import Path
report = Path(sys.argv[1]).read_text()
def unpack(tag, fmt, expected_hash):
    pattern = r"<!-- DATA:" + tag + r" -->\s*```text\n(.*?)\n```"
    encoded = re.search(pattern, report, re.S).group(1)
    raw = zlib.decompress(base64.b64decode(encoded))
    assert hashlib.sha256(raw).hexdigest() == expected_hash
    return list(struct.iter_unpack(fmt, raw))
def summary(label, rows):
    ds = [r[2] for r in rows]
    print(label, "n", len(ds), "mean", statistics.mean(ds),
          "se", statistics.stdev(ds)/math.sqrt(len(ds)), file=sys.stderr)
writer = csv.writer(sys.stdout)
writer.writerow(["base", "seed", "spread", "candidate_minus_base"])
datasets = {}
specs = [
    ("a", 700000, "44d4896441dfedfdffa704f2cf033ac36d52ce7f675e747da4fac63263ce738a"),
    ("b", 705000, "862f879e5e73a27a76de26ba4c431c4246e3367451d6e2d23b61829d80128f33"),
]
for base, start, digest in specs:
    packed = unpack(base, "<Bi", digest)
    assert len(packed) == 5000
    rows = [(start+i, spread, di/1_000_000) for i,(spread,di) in enumerate(packed)]
    assert len({r[0] for r in rows}) == 5000
    assert all(1 <= r[1] <= 4 for r in rows)
    assert all(r[2] == 0 for r in rows if r[1] in (1,4))
    datasets[base] = {r[0]:r for r in rows}
    for seed, spread, d in rows:
        writer.writerow(["m-plus-"+base, seed, spread, f"{d:.6f}"])
    summary(base, rows)
    for spread in range(1,5):
        summary(base+" spread "+str(spread), [r for r in rows if r[1]==spread])
    print(base, "worst five", sorted(rows,key=lambda r:(r[2],r[0]))[:5],file=sys.stderr)
pairs = unpack("completion", "<Idd", "45988f0148eaee5065030ce377d73430c438ec02efc8d128188113968f3a9044")
expected = set()
for first,last in [(709508,709562),(709830,709877),(709884,709940),(709947,709999)]:
    expected.update(range(first,last+1))
assert len(pairs) == 213 and {r[0] for r in pairs} == expected
assert len({r[0] for r in pairs}) == 213
for seed, base_edge, candidate_edge in pairs:
    assert math.isfinite(base_edge) and math.isfinite(candidate_edge)
    assert abs(round(candidate_edge-base_edge,6)-datasets["b"][seed][2]) < 1e-12
print("Verified all 213 new pairs; complete A and B coverage.", file=sys.stderr)
```

<!-- DATA:a -->
```text
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
```

<!-- DATA:b -->
```text
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
/nyh2cGK9cDQvlobY8xuthJx2FdIuPkzVdbwkoNTlR2ONj78VICTj0Qvp07R+IBXy9H9o8d8I6PIDTCFpEVclR0ma/e76/bzkEir
aAzNPMdSIo0qKtqeADfxyBWWFxUC2ph097tMUy7zXirKjhJpufGnJibxdm6qcdGB5TrzrQBDxCRWjzuyxmcdud6vLFVPIr7TNESd
BFro9FfPum4D3j8uq6rTOgnSRmOL/BKrU0fumCXTUk25Dbbe64/o2Gw/+/OfnWX0KgONP4qocuSCZJk2uqStJV5l9FOmY8vzZOaO
HCeJZD7H8qxfD5tpYwU7WrqcVwO9bc/ZUrflwKbelfhYjJXCuzWteB2ZLXep5M1HVbGg9Vtricys3VGVFY8Q40ZyudEIiVRJ0eR8
ydhxHPkrj6lTeA6ArmwMs19aezRT/mA7G/2G2M+wrPiYZzkxk08i+nCO+XwX1PumK49TGjiBJ/Z9qJyQ2UX1q/z8jbTwAj3ytYYL
35m6sk8mY1cGS8T/jkj9yIhnQPmFcZb/UoeyaQe8+Ou2h3IZUf9RVSKublypnynFQfMUcjKu7yms4IK68JzKoRL7FozS0T3hK8Xp
7youJgLIpSe8iHLzSNVGeEJ16MaSQfAGpzOhUv7RAyTiGaDacgm8DN1dkfUdAZtyOOvrSAvg1S/Y4Dorllqj73cZFFJDVYLXXlqZ
wIhPXPwh07AS/BjAomXci//dDchQuV4aYJ2LjjxtAi66rxMea3oZgwxoyx+Ly+W+ImUaYquEhhh9nd74YftBlWe6s1UVi7eL3wt+
pVPtlo7t7CnRcq8xo3M7HUWBXQ3UrBYNmwcKkVCNP1t5BqRxI6e4RJIfg2B4DqoCwvcKPDvqMYb7RAnOYoc/g2ORocCzrblTfzFb
ZIzkUqV3Mnm8gW/V/tWfr/m9lkqNdX++1+H+MVMmh2DxxP+gfl9BoycZ6q20ozMeQSevnrNSeY0ZCOLKTmknTtpVhsQfqeoxSbuZ
AOnJp0019la8JaIYv0Rt3NPKH4ppYzOE/Tl63wqmJVUgCbpGpv9R6Jrf/RnlDJGbBMc8fDwmXTMRyj+1EShYwDhWMkJCh6K/58+U
cvxl/JyDRVfEnFsP8Yz/2/lDZTpmuZiipv1qZ2o8mN2DfmyQf0hcJ3u/MSz87IPw7JZHPE840VOTgyeW6635Luhezs2C4sFVnPs0
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
```

<!-- DATA:completion -->
```text
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
```

## Sources and provenance

All original item links in the block tables are direct immutable artifact URLs; the URL's 64 hex digits are the SHA-256 of the downloaded input bytes. Their `per_seed` rows are preserved in the embedded A/B datasets. All new measurements are identified as this revision's B10 completion, with the actual paired totals embedded above. A report source is evidence about measurements, not an independent certification of every simulation.

- [Merge-01][M1]: supplied m-plus-a merge, SHA-256 `c6a261938b1185ebf70f67b9e21bdc4c46b4c258350ad32bd45e06af8856dc09`.
- [Merge-02][M2]: supplied m-plus-b merge, SHA-256 `9b621a92e8566c1eb5276bbe037a5d6f622b1fdad1cd500d6e02c114c0306a45`.
- [Accepted-file manifest][MANIFEST]: locates the original twenty item datasets; their exact links are in the block tables, including the partial original B10. No claim of original B10 completion is made.
- [m-plus-a artifact][BASEA] and [m-plus-b artifact][BASEB]: exact base strategy code, checked against the code hashes above. These are available artifact IDs, unlike the code hashes that the merges had tried as artifact IDs.
- [N][N] and [RC][RC]: exact prefix and wrapped code; checked prefix and hashes. N code SHA-256 `bf0d179f3e47d28819f6fa7e0d25548c2ced43374c216d36460b00a26a26ffae`; RC code SHA-256 `3c07bdcd221ac25729c3ebc92b21ac9e2014510ecb85816c4391ed81e933291f`.
- [Pinned simulator][SIM], especially [sampling][RUNNER] and [factory loading][LOADER]: new measurements used this code unmodified.
- [Goal][G]: historical standings, previous m-all measurement, and assigned experiment. [Paradigm challenge page](https://www.paradigm.xyz/puzzles/prediction-market-challenge) is the submission destination named by the requester; no numerical claim here relies on a current reading of that page.

[M1]: https://api.imd.fun/artifacts/c6a261938b1185ebf70f67b9e21bdc4c46b4c258350ad32bd45e06af8856dc09
[M2]: https://api.imd.fun/artifacts/9b621a92e8566c1eb5276bbe037a5d6f622b1fdad1cd500d6e02c114c0306a45
[G]: https://api.imd.fun/jobs/75dd8e1e-60c6-470e-a8a8-a6352c6fb9ea
[MANIFEST]: https://api.imd.fun/jobs/75dd8e1e-60c6-470e-a8a8-a6352c6fb9ea/result
[BASEA]: https://api.imd.fun/artifacts/149883fee797ad95a91e535b7a74453587a3eb19ca87ab95f7d8585db160a8f4
[BASEB]: https://api.imd.fun/artifacts/6b40ef6fdf9512700501e6b92fb5c920955a97b29111faada6d411074173b7cd
[N]: https://api.imd.fun/artifacts/db22aff7167a4798251ed3d20432509f30e511e4958799aba5b17b41bb39b4b6
[RC]: https://api.imd.fun/artifacts/2d4b30bbc6bffbc500b37ce5e8a1ac821d6513c52a6a2377b4be3c11d97717fb
[SIM]: https://github.com/danrobinson/prediction-market-challenge/tree/b244530ee2a6247b5f930830eeca9dd950da0e7e
[RUNNER]: https://github.com/danrobinson/prediction-market-challenge/blob/b244530ee2a6247b5f930830eeca9dd950da0e7e/orderbook_pm_challenge/runner.py
[LOADER]: https://github.com/danrobinson/prediction-market-challenge/blob/b244530ee2a6247b5f930830eeca9dd950da0e7e/orderbook_pm_challenge/loader.py
