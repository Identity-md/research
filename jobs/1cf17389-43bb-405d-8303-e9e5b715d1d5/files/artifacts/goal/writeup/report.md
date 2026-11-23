# Bitcoin Puzzle #71 — consolidated investigation

**No solution was found.** All 50 workstreams are represented in the three supplied merges. The address remained publicly unclaimed at the latest read, at Bitcoin mainnet height **977171** on **2026-11-23**. The workstreams report small candidate checks against the real target, successful recoveries of generated test instances, and no demonstrated shortcut for the real input. No funds were moved, no transaction was broadcast, and there was no paid compute. Any future verified solution would require a separate secure claiming process.

## Evidence and target

**Source convention.** M1/I05 means item 05 as reported in [merge-01](../../../.imd/reads/artifacts/merge-01), M2 covers I21–I40 in [merge-02](../../../.imd/reads/artifacts/merge-02), and M3 covers I41–I50 in [merge-03](../../../.imd/reads/artifacts/merge-03). These are the supplied inputs, which may travel separately from this report. Their SHA-256 fingerprints are at the end. “Reported” attributes execution to a workstream, “merge replay” to M3, “write-up replay” to execution for this report, and “estimate” to a calculation under stated assumptions.

| Field | Finding |
|---|---|
| Target | `1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU`, mainnet P2PKH. Base58Check version byte `00`, checksum `a22a3aab` (M2/I37). |
| Target commitment | HASH160 `f6f5431d25bbf7b12e8add9af5e3475c44a0a5b8`, script `76a914f6f5431d25bbf7b12e8add9af5e3475c44a0a5b888ac` (M1/I03–06, M2/I24/I37, M3/I43). |
| Published bounds | Inclusive `0x400000000000000000` through `0x7fffffffffffffffff`, exactly `[2^70, 2^71−1]`. Width **1,180,591,620,717,411,303,424**. The catalog agrees with the brief. The script commits to a hash, so the interval comes from the published construction convention. [Puzzle catalog](https://coinables.github.io/puzzle/) |
| Designated reward recipient | `bc1pg6luxm9s4qq65lge4l6ual7xwdw5v85eh675cmrl5we0ht3vpfhswxu0cx`, 62 characters, mainnet HRP `bc`, witness version 1, four zero padding bits, 32-byte Taproot program and Bech32m polymod `0x2bc830a3`. Encoding was reproduced by I43/I49/I50. This is the designated destination only, and its control remains unverified. [BIP 350](https://bips.dev/350/) |
| Recipient program | `46bfc36cb0a801aa7d19aff5ceffc6735d461e99bebd4c6c7fa3b2fbae2c0a6f`. Output script is `5120` followed by those bytes. I50 replay rejected all **1,829** single-symbol substitutions at the 59 data/checksum positions (31 alternatives each). |

M1/I12 decoded a 63-character copy with a 33-byte program and polymod `0x2acd85f6`. Replaying the exact brief string resolves the validity dispute. A transcription difference is plausible. The altered string was unavailable for comparison. M1/I04 also exercised targeted wrong-network, version, padding, length and checksum variants. M2/I38's reported 58 mutations describe a smaller test suite. (M1/I04/I12, M2/I38, M3/I46/I50.)

### Chain observations

For the write-up, the mempool.space and Blockstream address and UTXO requests were bracketed by tip-hash reads from **08:07:22.625846 through 08:07:24.192525 UTC on 2026-11-23**. Both brackets held at height **977171**, hash `00000000000000000001e0f89a9668808158e7d2a7fc7de8f3a25bee82da533e`, header time **07:55:32 UTC** (1795420532). Each returned **73 confirmed UTXOs totaling 710,196,696 sat (7.10196696 BTC)**, 73 confirmed address transactions, zero spent outputs and zero address-specific mempool transactions, funding or spending. These public index reads establish the observed unclaimed status at the snapshot. A privately known key or unobserved off-chain disclosure remains possible. [mempool.space stats](https://mempool.space/api/address/1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU) · [mempool.space UTXOs](https://mempool.space/api/address/1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU/utxo) · [Blockstream stats](https://blockstream.info/api/address/1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU) · [Blockstream UTXOs](https://blockstream.info/api/address/1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU/utxo) · [snapshot block](https://mempool.space/api/block/00000000000000000001e0f89a9668808158e7d2a7fc7de8f3a25bee82da533e)

| Principal funding outpoint | Height | Header time (UTC) | Satoshis | Source |
|---|---:|---|---:|---|
| `08389f34c98c606322740c0be6a7125d9860bb8d5cb182c02f98461e5fa6cd15:70` | 339085 | 2015-01-15 18:07:14 | 7,100,000 | [Original funding](https://mempool.space/api/tx/08389f34c98c606322740c0be6a7125d9860bb8d5cb182c02f98461e5fa6cd15) |
| `5d45587cfd1d5b0fb826805541da7d94c61fe432259e68ee26f4a04544384164:19` | 475240 | 2017-07-11 05:00:53 | 63,900,000 | [2017 redistribution](https://mempool.space/api/tx/5d45587cfd1d5b0fb826805541da7d94c61fe432259e68ee26f4a04544384164) |
| `12f34b58b04dfb0233ce889f674781c0e0c7ba95482cca469125af41a78d13b3:5` | 785620 | 2023-04-16 06:29:48 | 639,000,000 | [2023 top-up](https://mempool.space/api/tx/12f34b58b04dfb0233ce889f674781c0e0c7ba95482cca469125af41a78d13b3) |

The original transaction had 256 outputs totaling 32.896 BTC. The three large outputs total 710,000,000 sat and the other 70 total 196,696 sat (M1/I03–06/I10/I14/I20, M3/I43/I46/I50). The original timestamp follows directly from 1421345234. I12's 14:07:14 and I44's 12:07:14 are inconsistent with that conversion. M1/I07/I19's 7.10182686 BTC was a stale balance. Earlier reads at heights 977165–977167 (roughly 07:33–07:38 UTC) and M3's bracketed dual-provider read at 977168 (07:42:36–07:42:38 UTC, header 07:37:47 UTC) show the same 73 UTXOs and balance. I41 hit a Blockstream 429 and used one provider. I49 observed a moving Blockstream tip. I28/I48 lacked contemporaneous chain snapshots of their own. M3 reports different historical inventory hashes for different sort/serialization conventions, including whether the final LF, block hash and time entered the digest. The raw historical lists were unavailable for a canonical digest comparison. [Block 977165](https://mempool.space/api/block/000000000000000000014641e7b8d308b6a5eaec5772d150ceed4a4f3720e600) · [Block 977166](https://blockstream.info/api/block/00000000000000000001eb8dbe3d5f56627ee265efd5d61d48cc1929cbd4c9ec) · [Block 977168](https://mempool.space/api/block/00000000000000000000f85af08c4764ef543e9b5a44e5cf7e56b2661b09817e)

### Public invitation and its limits

M1/I03 reports public discussion by amaclin on 2015-01-23 and a proposed increasing-bit-length rule. The located public prize invitation is Bulista's thread, displayed **2015-12-28 16:12:47**, framing the discovery as a roughly 32 BTC prize. A post by `saatoshi_rising`, displayed **2017-04-27 06:41:08**, claims authorship and describes “consecutive keys from a deterministic wallet” masked to set the difficulty. The write-up re-read that post, resolving the uncertainty about whether this wording appeared outside trackers. Forum display timezones and the pseudonymous author's identity remain unauthenticated. The July transaction had 97 inputs, including all 96 original vouts 160–255, corroborating the proposed redistribution. The sources yielded no contemporaneous signed invitation from the January funder or authenticated prize terms. Catalogs may describe a random constrained model or repeat the masked-wallet account. Neither supplies a seed, derivation rule or verified probability distribution for #71. [Prize thread](https://bitcointalk.org/index.php?topic=1306983.0) · [Claimed creator post](https://bitcointalk.org/index.php?topic=1306983.msg18765941) · [Redistribution transaction](https://mempool.space/api/tx/5d45587cfd1d5b0fb826805541da7d94c61fe432259e68ee26f4a04544384164)

## What was tested and what the input permits

**Point-dependent methods.** The verified target input is HASH160 of a serialized point. BSGS and kangaroo need the actual curve point, while full-group Pollard rho would also require that point and scale at about `2^128` group steps. I21 checked scripts and witnesses associated with the 73 funding transactions and found 160 distinct valid points, with no match. This is a bounded source check. I05/I06 report the June 2019 reveal (height **578732**, **2019-06-01 02:07:26 UTC**, tx `17e4e323…b3d3`) exposed points for 20 siblings at five-puzzle steps from #65 through #160, all compressed. They found no #71 input. I05 also reproduced #70's point and address against the public solved record. I17 used the #1 address and I35 checked 40/40 solved-address fixtures. Those observations support compressed search priority. As I39 showed, the same point has two legacy address encodings, and an exhaustive claim for both predicates requires checking both. I06 reported a 9–14% overhead for both encodings on its Python stepper. (M1/I05/I06/I17, M2/I21/I35/I39.) [Bitcoin transaction guide](https://developer.bitcoin.org/devguide/transactions.html) · [SEC 1 point encoding](https://www.secg.org/sec1-v2.pdf) · [SEC 2 curve parameters](https://www.secg.org/sec2-v2.pdf)

With a verified point, the interval square root is **`2^35`**, correcting the `2^35.5` used in M1/M2 and some M3 estimates. A classic two-kangaroo constant of about two gives `2^36` expected group steps under the paper's model. I22 measured 26/26 toy recoveries, roughly 2.3–2.8√N for its Python solver, and 2.7–4.2 million group steps/s with a CPU implementation on toy ranges of size `2^48`–`2^56`. Its ~5.3-hour estimate used ~3.9 million steps/s and a tool estimate of `2^36.11` steps. I23 measured a simpler implementation at ~5.4√N. I21's BSGS memory scenario used ~`2^35` entries and ~1.19 TiB. At I43's separate assumption of 42 bytes per entry it is 1.3125 TiB before indexes. In I46's ten toy trials, both enumeration and BSGS recovered 10/10. The address scan took 19,185 checks and 1.321115 s, while BSGS took .065296 s with 64 entries per puzzle and 295 giant-step advances. The lower-endpoint enumeration was faster in that trial. These comparisons use different inputs and count different operations. The conditional speed estimates establish no target recovery time. [Kangaroo analysis](https://arxiv.org/abs/0812.0789) · [Interval methods](https://eprint.iacr.org/2010/617) · [Implementation documentation](https://raw.githubusercontent.com/JeanLucPons/Kangaroo/master/README.md) (M2/I21–23/I30, M3/I43/I46.)

**Hash-only enumeration and tradeoffs.** No reviewed method reduces the real hash-only workload below generic trial search with the available evidence. I24's 8,192-row synthetic inventory tested a time-memory tradeoff, with no established single-target gain after precomputation and coverage costs. I25 verified the GLV relation and tested 3,000 in-range scalars, with zero endomorphism images remaining in the window. I26 found negation maps scalars outside the interval while batch arithmetic can still reuse denominators. I29's AVX2 RIPEMD160 pipeline helped on its tested CPU, while naive 10×26-bit AVX2 field multiplication on the non-IFMA CPU lost to scalar arithmetic. I30/I32 found that software with an address-search mode fits the input, subject to build and correctness checks. I31 found no verified FPGA end-to-end rate for this problem. A binary Koblitz known-point result and a disputed ASIC forum rate supply no usable Bitcoin rate. No GPU or FPGA search was measured. (M2/I24–33.)

**Real-target work reported.** I44 reports 6,000 distinct compressed candidate checks from the lower endpoint, no match. Three batches of 2,000 took **2.409212, 2.496557 and 2.283185 s**, or **834.61/s** over **7.188954 s** combined. Its local toy key was recovered at check **3,809** in `[8192,16383]`. The planned C increment benchmark failed because the compiler command was unavailable for I44. Its Python benchmark depends on an unbundled cryptography package and was not replayed. M2's executive summary labels its searches toy-only, yet its individual index reports I38's **8,339** in-range scalars with zero matches and I39's **1,024** scalars in both encodings with zero matches. The merge does not give enough target/predicate/coordinate evidence to reconcile those counts with the executive summary or with I44's slice. No combined distinct real coverage is claimed. I44's 6,000 checks alone amount to **5.08×10⁻¹⁸** of the scalar interval. The write-up ran zero real-target candidate checks. (M2/I38/I39, M3/I44.)

### Recorded performance

Rates below describe local experiments with different arithmetic, comparisons and bookkeeping. Group steps, digest blocks and full checks are separate units.

| Source | Measured workload and result |
|---|---|
| M1/I02/I05/I06 | Pure JS address mode ~4,000 checks/s. Python toy brute force 22,722/s with recovery at check 254,237. Compressed stepper ~28,900/s. |
| M1/I12/I17 | Node 85–90k additions/s and BSGS 107,887 ops/s, 10/10 on 28-bit toys. I17 full multiply plus hash ~248/s. |
| M1/I18–20 | Random multiply 366/s vs sequential point stepping 35,438/s. I19's Python path 156–680/s. I20 trace-writing SQLite path ~1,112/s. |
| M2/I21–23 | I21 ~63,800 cand/s in its synthetic hash scan. I22 Python kangaroo 10–25.6k steps/s and Python address scan 12,389 checks/s. I23 toy kangaroo ~66k steps/s. |
| M2/I26–27 | C incremental point arithmetic 40–57× over naive affine, up to 1.5M EC steps/s. Whole C batch path 349–528k checks/s. Python simultaneous inversion 31–36× over per-add inversion, leveling off near batches of 1,024–2,048. |
| M2/I28–29 | SHA256 38.95M blocks/s and RIPEMD160 7.39M blocks/s on I28's measured path, ~5.3× gap. The compressed hash uses one block each after padding. I29 measured AVX2 HASH160 7.32M/s vs 1.27M/s scalar, and 2.5–2.68M end-to-end checks/s/core. |
| M2/I33–36 | I33 OpenSSL SHA256 ~8.4M/s, P-256 signatures ~52,190/s (proxy only). I34 four Node workers 11,309 checks/s, 3.63× one worker. I35 incremental Python ~28.5k/s and kangaroo toy n=44 exceeded a 300 s cap. I36 incremental Python ~79,900/s on one worker and ~186k/s across four. |
| M2/I37–40 | Independent Node/OpenSSL and Python/Libgcrypt paths agree on 256 positives and reject 768 negatives. I38 mixed boundary suite ~5,396 comparisons/s. I39 dual-library/encoding ~443 candidates/s. I40 crash/restart test recovered a planted toy key and overlap detection had zero false positives and zero false negatives over 4,000 randomized trials. |
| M3/I43–47 | I43 recovered three generated secrets exactly once each, scanning 16,384 positions per run. Runs 1.126149/.995384/1.094960 s, median 14,963.10/s (write-up replay below). I44's full multiply path 834.61/s. I45 reports ~33,700 pubkey-create+serialize operations/s/core and ~368,000 separate hashes/s, with no measured composite rate. I46/I47 toy tests are summarized above and under disclosure. |

I33 found third-party rates varied in what they count. Its audited README claims include ~4M/s keyhunt, 51.21/159M/s Cyclone AVX2/AVX512, and 35.91–120M/s VanitySearch. Even assuming 10,000 lanes at the highest claimed rate with ideal disjoint scaling, exhaustive time is ~23.5 years. I45's C fragment varies only two scalar bytes and lacks executable setup, dependency pins and enough context to check zero-scalar handling and return values. Its 200,000 operations in 5.9 s are an attributed measurement. The 135,000/s four-core figure is a projection from one stage. Serially combining the measured stage rates gives ~30,900/s before other overhead. (M2/I30–33, M3/I45.)

### Runtime and energy models

Assume one matching scalar in a fixed predicate, uniform location, no duplicate checks and sustained rate R. Exact mean checks for disjoint search are `(N+1)/2`, full coverage takes N, and after q distinct checks success probability is `q/N` for `0≤q≤N`. For draws with replacement the mean is N and the CDF is `1−(1−1/N)^q`, with p99 about 4.61N. M1/I18 found ~37% repeat draws at N attempts and ~68% duplicate work at 95% coverage, plus much slower random EC access on its implementation. A shard permutation can distribute work while retaining incremental stepping within shards. These formulas correct the mean/median conflation in M1/I07. For a prior with 90% mass in the first 10%, uniform separately within that region and the other 90%, scanning the favored region first gives mean .10N, a 5× gain. No workstream demonstrated that prior. (M1/I07/I12/I18/I19, M3/I44/I48.)

| Rate scenario | Mean years | Full years |
|---|---:|---:|
| 834.61/s, I44 measurement extrapolated | 22.41 billion | 44.82 billion |
| 79,900/s, I36 one-worker measurement extrapolated | 234 million | 468 million |
| 2.5–2.68M/s, I29 test extrapolated | 6.98–7.48 million | 14.0–15.0 million |
| Assumed 1–1.5G/s | 12,470–18,706 | 24,940–37,411 |
| Assumed 5G/s | 3,741 | 7,482 |
| Assumed 1T/s | 18.7 | 37.4 |
| I45's reported pool display 123.5G/s, if sustained with disjoint coverage | 152 | 303 |

Years use 31,557,600 seconds. In M2 the ~4.7×10⁸-year Python figure corresponds to **full** coverage at 79,900/s. Its GPU range also mixes mean and full horizons. The ~422-year pool estimate and I45's ~303-year estimate use separate unverified telemetry. M1/I07 had five flagged sources behind figures including 57.3G/s, 290,012 of 2²⁵ ranges (0.864%), and 324/647-year figures. The merges supply neither the verified progress ledger nor a comparable device benchmark. I17's ~1.05% progress claim is a dated tracker figure. These numbers receive no coverage credit. M2/I21 reports 403s on some forum/dev-guide/ePrint sources, I24's tracker and time-memory constants require separate corroboration, and I30's commercial/community GPU rate anecdotes were unverified. M3 flags two unspecified source failures for I47. That warning remains open even where newer public references were available. (M1/I07/I10/I17, M2/I21/I24/I30, M3/I45/I47/I48.)

I45 divides the [pool display](https://btcpuzzle.info/puzzle/71) by about 49 reported workers to assume 2.52G checks/s per worker. This does not identify devices or demonstrate coverage. With assumed wall power 550 W, tariff $0.1487/kWh and uniform position, energy is `(N/2)×550/(2.52e9×3.6e6)` kWh, about **35.8 GWh** or **$5.32M**. Full coverage doubles those figures to about 71.6 GWh and $10.6M. The same model implies ~6.5×10⁷ device-hours for the mean, ~$23M at the illustrative $0.35/device-hour, and ~13,000 tonnes CO₂ at 0.37 kg/kWh. The report's ~$436k reward scenario at $61,402/BTC gives break-even electricity around **1.79×10⁻⁸ J/check**. At 5×10⁻⁸ to 5×10⁻⁷ J/check, mean electricity spans ~8.2–82 GWh, or ~$1.22M–$12.2M at that tariff. No power, tariff, price, emissions, pool uniqueness or sustained GPU rate in this scenario was independently measured. Host-inclusive wall measurement and device-only telemetry answer different questions. (M3/I45.)

## Statistical tests and rejected hypotheses

M2/I21–40 mainly assessed algorithms and engineering. Its statement that no statistical shortcut was tested applies to that merge's scope. M1 and M3 include several such tests. Some use the same public solved record, so agreement across items need not mean independent datasets. Solved puzzles are a selected sample. Mild, localized or generator-specific effects remain possible.

| Study | Executed finding or limitation |
|---|---|
| M1/I08 and M3/I48, 83 solved rows | Mean normalized position .5136, KS D=.0678. I48 reports p=.827, variance .0774 and upper-half count 42/83. I48's partial parser, raw data and unspecified 20-test family do not support a full offline replay of those claims. The endpoint-normalization convention needs separate handling for width-one intervals. [Public solved record](https://raw.githubusercontent.com/roadhero/Bitcoin-Puzzle-Info/main/BTC-Solved-Unsolved.txt) |
| M1/I12, 69 positions from #2–70 | Mean .5267, KS D=.0892 (p=.61). Bottom-1% excess 3 vs .69 expected (raw p=.032) failed Holm. The in-sample preferred quartile had holdout p=.56. Null calibration gave 6.1% false positives over 1,000 simulated sets. |
| M1/I13, 65 solved rows | Smallest raw p=.0127 across 57 bit tests, adjusted .725. Hamming-weight p=.35 and held-out bit accuracy .5034. [OEIS A369920](https://oeis.org/A369920) |
| M1/I09/I15, generator hypotheses | Data fit the forced top bit and gave no support to tested common-master/slice interpretations. Consecutive outputs of a deterministic wallet do not imply consecutive scalar integers. Missing seed/xpub/derivation makes a specific wallet hypothesis unidentifiable. Nonce/lattice methods require signatures. Randstorm was assessed as a poor structural fit. No validated seed inference was supplied. |
| M1/I11/I14, synthetic holdout | Selection can make apparent patterns look predictive. I11 reports 57.6% passing discovery under the null, holdout hit rate near the 6.25% baseline, and corrected holdout passes 2/1,000 under null vs 991/1,000 with planted signal. I14 independently explored selection effects on synthetic data. |
| M1/I16 and M3/I48, prefix tests | I16's three preregistered tests failed Bonferroni α=.0167 and detected a leaky positive control. I12 reported prefix/position rank ρ=−.13. I48's reported 2,000 consecutive compressed test points gave correlations .018 (HASH160) and .003 (lexicographic address). Its 197-target first-byte distance ratio .957±.254 is reported with unspecified uncertainty definition and unavailable complete source. |
| M3/I49, synthetic prefix-distance | 4,096 trials per fold using salted SHA256, 10,000 paired sign permutations per endpoint. Development hits 272 and 14 for 4 and 8 bits, corrected p=.4488 and 1. Held-out hits 256 and 18, corrected p=1 for both. Small eight-bit hit counts limit power. Replayed below. |
| M3/I50, synthetic nearby/control | 4,096 development and 16,384 holdout trials. For 4/6/8 bits, held-out counts 1018/1009, 253/236 and 74/54, with Holm p=.467555/.467555/.139035. Eight-bit raw p=.046345 looked promising in isolation. Its +.122 percentage-point lift missed the .5-point floor as well. Replayed below. |

No tested predictor demonstrated reliable out-of-sample pruning for #71. The failed prefix hypotheses give no reason to use address ordering as a scalar-distance estimate. The limited sample sizes, the selection of previously solved keys and the simplified toy hash distributions constrain what can be inferred about the generator. M1/I10 re-derived 10/10 solved addresses and found inconsistencies in tracker balances, generation narratives, counts and GPU estimates. Its 256-original vs ~160-active distinction reflects the redistribution history. A dataset linter should derive addresses and bounds from disclosed records and check chain claims separately. (M1/I08–16, M3/I48–50.)

## Coverage, storage and disclosure

**Coverage evidence.** I19's deterministic integer partitions tiled the interval at 1/50/1,000/2²⁰ workers. I38 also tested a 50-way partition and caught injected off-by-one, gap, overlap, 64-bit narrowing and floating-point rounding bugs. I20's SQLite tests showed that an atomic cursor-and-result commit survived pre/post-commit kills, with one replayed batch in the first case and zero in the second. A faulty early cursor silently skipped the planted solution. I40's partial checkpoint replay recovered its toy key. Use a half-open cursor denoting the next untested scalar, exact integer coordinates, and an immutable manifest binding the predicate and build. Count unique intervals with an exact union. Treat assignment, reported completion and independently replayed coverage as distinct states. Leases with epochs, durable transitions and idempotent retries help detect stale or duplicate completions. A signed receipt identifies a signer and a commitment freezes bytes. Neither demonstrates that an unchecked range was evaluated. (M1/I18–20, M2/I38/I40, M3/I41/I42.)

I41 used 65,539 synthetic records in 65 shards with a three-record tail. Full reference plus replay took 131,078 evaluations per run and detected the injected last-shard false negative. Sampling eight shards detected it 1,290/10,000 times. Those seeded repeats share one Monte Carlo sequence. I42 covered 32,768 synthetic positions in 256 blocks, caught a one-position union gap and rejected four invalid ranges. A complete manifest still passed with incomplete receipts. Sampling 16 blocks detected honest/16-bad/1-bad cases in 0/3,295/348 of 5,000 trials each. For B total, C fixed corrupt blocks and k uniformly sampled without replacement, miss probability is `choose(B−C,k)/choose(B,k)`. A single bad block is detected with probability k/B. For 95% single-defect detection these workloads would need 62/65 and 244/256 sampled blocks respectively. Full replay and independent implementation checks address failure modes that agreeing receipts can share. No adversarial multiprocess network test was supplied. (M3/I41/I42.)

**Storage measured and modeled.** I43 tracked 16,384 generated candidates. Its packed rows took 524,288 bytes (408,173 zlib), JSONL 1,687,552 (476,448), raw hashes 327,680 (327,786), and the serialized in-memory SQLite table/index 1,171,456. A 64-byte progress record versus a 167-byte JSON checkpoint illustrates the value of sparse metadata. Sixty-four completions used 4,096 bytes. One duplicate delivery repeated 256 checks. Four logical workers were simulated in one process. Full-space extrapolations are 128 EiB for a candidate bitmap, 20 ZiB for raw HASH160s, 32 ZiB for 32-byte packed rows. A 64-byte ledger with 2³²/2⁴⁰/2⁴⁸ candidates per chunk would use 16 TiB/64 GiB/256 MiB respectively. Lazy leases and coalesced ranges cut metadata. At the assumed 50×100M checks/s, 2³² candidates per chunk, 256-byte completions and one 256-byte heartbeat/minute/worker, payload is ~511 B/s before transport or replay. Sending a 32-byte row per check at the same aggregate rate would cost 160 GB/s. No sustained bandwidth, disk or fsync performance was measured. (M3/I43.)

**Public reporting and claiming.** A legacy P2PKH spend reveals the serialized source point, including when the destination is Taproot. The public record verifies #69 spending in blocks 894620–894881 (first spend 2025-04-30 14:45:54 UTC, M1/I05). I08's reports of front-running for #66/#69 and private submission for #67/#68 are historical accounts. They do not establish who controlled the competing spends or how any specific relay would behave. A confirmed solve or spend is a stop condition for target-specific work. A matching point disclosed off-chain while the prize remains unclaimed would change the algorithm assessment only after its source and HASH160 were verified. A read-only status monitor proposed in M1 has value as a stop signal. No target spend watcher or claim workflow was executed here. [Bitcoin transaction guide](https://developer.bitcoin.org/devguide/transactions.html) (M1/I05/I08/I17, M3/I46/I47/I50.)

I47's toy precomputed-point experiment recovered all 11 samples in each of three scans. It measured medians of 9.455 ms for HASH160, .347 ms for a disclosed point and 2.731 ms for a scalar SHA256, excluding 173.074 ms of point table creation. OpenSSL cross-checked 2/2 endpoints. These results show why even an unblinded digest, an offset, recoverable signature or exported transaction fields merit care. Any candidate verification would take place privately, check inclusive bounds and exact serialized HASH160 with independent implementations, and export only a fixed status and allowlisted public facts. A local verified status would be an attestation. I47's zero-knowledge idea to hide both witness and point while binding the public puzzle context was analysis only, with no circuit, prover or audit supplied. Prize terms, donation provenance, recipient control and legal entitlement remain unverified. Private submission would still introduce a trust relationship. No private key, seed or spendable transaction is included. (M3/I46/I47.)

## Best next experiment

**Run a bounded correctness and throughput trial on generated 20-bit puzzles using up to four available CPU processes.** This combines M3/I41–44's coverage tests with M1/I20 and M2/I37–40's verifier and checkpoint work. Use fixed known answers, endpoint fixtures, 2¹⁰-candidate subchunks, an exact interval ledger and a separately implemented reference. Include compressed and uncompressed fixtures. Inject crashes before and after a durable commit, duplicate receipts, stale epochs, a missing boundary and two agreeing false negatives. Require exact recovery, no undetected omissions or duplicate coverage credit after restart, and independent replay to reject the false negatives. Record distinct full checks/s with setup and replay costs separate, wall time, memory, journal bytes and fsync/restart overhead. Stop after the fixed toy workload or a declared time cap and report partial counts if capped. The five replays below validate components. This integrated multiprocess experiment remains proposed.

Before any further target-specific experiment, refresh the public bounds/provenance and bracketed dual-explorer check. Stop for a confirmed solve/spend or unresolved parameter conflict. The next performance experiment after the correctness gate would measure batched point stepping and RIPEMD160 on the same toy workload, with the same predicate and fixtures. Hardware benchmarking is contingent on devices already available. For a proposed statistical predictor, preregister its entire hypothesis family, holdout and practical effect floor. I50's suggested blind control uses 16,384 trials per arm and injects an 8-bit match on 2% of trials in one arm to check power. A disclosure test with dummy secrets in logs and structured fields is a lower-cost check than implementing public proofs. These experiments address measurable gaps. None demonstrates a path to full-scale recovery within the authorized resources. (M1/I09/I11/I18–20, M2/I26–29/I35–40, M3/I41–50.)

## Reproducibility

Five complete offline programs from M3 are embedded below so the experiments survive delivery without the merge files. Each fenced Python block is independent. Run one at a time with Python 3. I43 needs Python's RIPEMD160 support and the standard SQLite and zlib modules. The programs evaluate synthetic inputs only and use the public addresses for decoding checks where relevant. No install or network is required to replay these five. The write-up ran them sequentially on **2026-11-23 at approximately 08:07:35–08:07:41 UTC**. All exited zero. Wall times are observations, with no expected timing equality across replays.

| Test | Write-up replay | Earlier M3 merge replay |
|---|---|---|
| I41 | Process .2664 s. 65 shards, tail 3, 131,078 evaluations and 1,290/10,000 audit hits. | Process .3895 s, same counts. |
| I42 | Process .2072 s. 0/3,295/348 detections out of 5,000 per case. Full reference .036128 s, uncached 16-block replay .002151 s. | Process .3324 s, same assertions and counts. |
| I43 | Process 3.3968 s. Three recoveries, byte counts reproduced. Median scan .690175 s, 23,738.91 checks/s. | Process 5.1585 s, median 14,452.71/s. |
| I49 | Process 1.0186 s. All hit counts and p-values reproduced. | Process 1.9794 s. |
| I50 | Process .4101 s. Rejected 1,829 checksum mutations, reproduced counts and p-values. Address .126 s, development .031 s, holdout .207 s. | Process .8333 s. |

M3 also replayed I46 (process 1.6260 s, 10/10 each for enumeration and BSGS, 1,829 mutations rejected) and I47 (process .5234 s, 11/11 each for three scan types, OpenSSL 2/2 and exporter checks). Those complete scripts were omitted in M3. This report therefore carries their methods and attributed results. M1/M2 refer to other item-level scripts such as I35's synthetic fixture generator, but do not supply the full scripts in the three merged inputs. I48's data and complete scripts and I45's executable benchmark were missing. No replacement raw logs, secrets, rates or results were fabricated.

**Input fingerprints** (SHA-256, matched to the brief)

- M1, workstreams 01–20 — `14d254db73e19a2e8fd2ba29736db3c6736b45965b0ea38856ae84a3234c8fb0`
- M2, workstreams 21–40 — `cb9729a4e1fa0268e592924953a5a2a0c79c033ce32b3a578cc83f57c9d56ff9`
- M3, workstreams 41–50 — `1bb79abbe8b32112de9007a0a3ba788528f4003e9fa6bbe11b308cf1de5bf0df`

### I41 — replayed source

```python
from hashlib import sha256
from random import Random
from time import perf_counter

start = perf_counter()
n, size = 65539, 1024
shards = [range(lo, min(n, lo + size)) for lo in range(0, n, size)]
assert [i for shard in shards for i in shard] == list(range(n))

def score(i):
    return sha256(b"item41-report-fixture:" + i.to_bytes(4, "big")).digest()

target = score(n - 1)

def replay(shard):
    return tuple(i for i in shard if score(i) == target)

baseline = [replay(shard) for shard in shards]
assert sum(baseline, ()) == (n - 1,)
reports = baseline.copy()
reports[-1] = ()
assert [j for j, shard in enumerate(shards)
        if reports[j] != replay(shard)] == [64]
print(len(shards), len(shards[-1]), "evaluations", 2 * n,
      "wall", perf_counter() - start)

start = perf_counter()
rng = Random(4181)
hits = sum(64 in rng.sample(range(len(shards)), 8) for _ in range(10000))
print("audit hits", hits, "wall", perf_counter() - start)
```

### I42 — replayed source

```python
from hashlib import sha256
from random import Random
from math import comb, sqrt
from time import perf_counter


def claimed_size(intervals, lo, hi):
    end = lo
    size = 0
    for a, b in sorted(intervals):
        if not lo <= a < b <= hi:
            raise ValueError("invalid interval")
        size += max(0, b - max(a, end))
        end = max(end, b)
    return size


BLOCK = 128
COUNT = 256


def receipt(block, start, stop):
    digest = sha256(b"coverage-demo-v1" + block.to_bytes(2, "big"))
    for i in range(block * BLOCK + start, block * BLOCK + stop):
        digest.update(sha256(i.to_bytes(4, "big")).digest())
    return digest.digest()


def main():
    start = perf_counter()
    n = BLOCK * COUNT
    ledger = [(0, n // 2), (n // 2 - 8, n - 1), (0, n // 2)]
    assert claimed_size(ledger, 0, n) == n - 1
    assert claimed_size(ledger + [(n - 1, n)], 0, n) == n
    for invalid in [(-1, 8), (0, n + 1), (8, 8), (9, 8)]:
        try:
            claimed_size([invalid], 0, n)
        except ValueError:
            continue
        raise AssertionError(invalid)
    assert claimed_size([(0, 5), (8, 13)], 0, 13) == 10
    assert claimed_size([], 0, n) == 0

    replay_start = perf_counter()
    ref = tuple(receipt(j, 0, BLOCK) for j in range(COUNT))
    print(f"full reference: {n} synthetic positions, {perf_counter()-replay_start:.6f}s")

    corrupt = Random(42).sample(range(COUNT), 16)
    bad = list(ref)
    for j in corrupt:
        bad[j] = receipt(j, 1, BLOCK)
    bad = tuple(bad)
    one = list(ref)
    one[corrupt[0]] = bad[corrupt[0]]
    one = tuple(one)
    assert sum(a != b for a, b in zip(ref, bad)) == 16
    assert sum(a != b for a, b in zip(ref, one)) == 1

    rng = Random(7142)
    k, trials = 16, 5000
    sets = [rng.sample(range(COUNT), k) for _ in range(trials)]
    # Independent replay once per block, cached across the simulated audits.
    check = tuple(receipt(j, 0, BLOCK) for j in range(COUNT))
    assert check == ref
    for name, claims, errors in [("honest", ref, 0), ("16 bad", bad, 16), ("1 bad", one, 1)]:
        detected = sum(any(claims[j] != check[j] for j in s) for s in sets)
        expected = 1 - comb(COUNT - errors, k) / comb(COUNT, k)
        assert abs(detected / trials - expected) < 5 * sqrt(expected * (1 - expected) / trials) + 1 / trials
        print(f"{name}: {detected}/{trials}; expected {expected:.6f}")
    replay_start = perf_counter()
    assert all(receipt(j, 0, BLOCK) == ref[j] for j in sets[0])
    print(f"uncached 16-block replay: {perf_counter()-replay_start:.6f}s")
    print(f"total: {perf_counter()-start:.6f}s")


if __name__ == "__main__":
    main()
```

### I43 — replayed source

```python
import sys, platform, time, hashlib as H, zlib, json, sqlite3, statistics
from datetime import datetime, timezone
print("UTC", datetime.now(timezone.utc).isoformat())
print("runtime", sys.version.split()[0], platform.machine(), "SQLite",sqlite3.sqlite_version,"zlib",zlib.ZLIB_VERSION)
recipient="bc1pg6luxm9s4qq65lge4l6ual7xwdw5v85eh675cmrl5we0ht3vpfhswxu0cx"
abc="qpzry9x8gf2tvdw0s3jn54khce6mua7l"
def validate(s):
    assert s==s.lower() and len(s)<=90
    hrp,tail=s.rsplit("1",1)
    v=[abc.index(c) for c in tail]; c=1
    for d in [ord(x)>>5 for x in hrp]+[0]+[ord(x)&31 for x in hrp]+v:
        top=c>>25; c=((c&0x1ffffff)<<5)^d
        for j,g in enumerate([0x3b6a57b2,0x26508e6d,0x1ea119fa,0x3d4233dd,0x2a1462b3]):
            if (top>>j)&1: c^=g
    assert hrp=="bc" and v[0]==1 and c==0x2bc830a3
    bits="".join(format(d,"05b") for d in v[1:-6])
    n=len(bits)//8; pad=bits[8*n:]
    assert n==32 and len(pad)<5 and set(pad)<=set("0")
    return c,n
print("recipient",validate(recipient))
try:
    validate(recipient[:-1]+"q")
    raise RuntimeError("mutation accepted")
except AssertionError: print("recipient mutation rejected")
target="1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU"
n=0
for ch in target: n=n*58+"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz".index(ch)
raw=b"\0"*(len(target)-len(target.lstrip("1")))+n.to_bytes((n.bit_length()+7)//8,"big")
assert len(raw)==25 and raw[0]==0 and H.sha256(H.sha256(raw[:-4]).digest()).digest()[:4]==raw[-4:]
print("target hash160",raw[1:-4].hex())
p=2**256-2**32-977
G=(int("79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798",16),
   int("483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8",16))
def add(a,b):
    if a is None:return b
    if b is None:return a
    x,y=a; X,Y=b
    if x==X and (y+Y)%p==0:return None
    m=((3*x*x)*pow(2*y,-1,p) if a==b else (Y-y)*pow(X-x,-1,p))%p
    z=(m*m-x-X)%p
    return z,(m*(x-z)-y)%p
def mul(k):
    a=None; b=G
    while k:
        if k&1:a=add(a,b)
        b=add(b,b);k>>=1
    return a
def h160(q):
    x,y=q
    return H.new("ripemd160",H.sha256(bytes([2+(y&1)])+x.to_bytes(32,"big")).digest()).digest()
assert (G[1]*G[1]-G[0]**3-7)%p==0
assert h160(G).hex()=="751e76e8199196d454941c45d1b3a323f1433bd6"
N=2**14; chunk=256; times=[]
for trial in range(3):
    secret=N+int.from_bytes(H.sha256(("local43:"+str(trial)).encode()).digest(),"big")%N
    goal=h160(mul(secret)); q=mul(N); rows=[]; matches=0; t=time.perf_counter()
    for i in range(N):
        d=h160(q)
        matches+=d==goal
        rows.append(d+i.to_bytes(9,"big")+(i//chunk%4).to_bytes(2,"big")+b"\0")
        q=add(q,G)
    elapsed=time.perf_counter()-t;times.append(elapsed)
    assert matches==1 and q==mul(2*N)
    packed=b"".join(rows)
    texts=b"".join((json.dumps({"hash":r[:20].hex(),"offset":r[20:29].hex(),
                              "worker":int.from_bytes(r[29:31],"big"),"flags":0},
                             separators=(",",":"))+"\n").encode() for r in rows)
    if trial==0:
        db=sqlite3.connect(":memory:")
        db.execute("create table records(h blob primary key, off blob, worker integer, flags integer)")
        t=time.perf_counter()
        db.executemany("insert into records values (?,?,?,?)",[(r[:20],r[20:29],int.from_bytes(r[29:31],"big"),0) for r in rows])
        db.commit();print("sqlite",len(db.serialize()),"insert_s",round(time.perf_counter()-t,6))
        for name,data in [("packed",packed),("jsonl",texts),("hashes",b"".join(r[:20] for r in rows))]:
            t=time.perf_counter();z=zlib.compress(data,6);dt=time.perf_counter()-t
            assert zlib.decompress(z)==data
            print(name,"bytes",len(data),"zlib_bytes",len(z),"compress_s",round(dt,6))
    print("trial",trial,"scanned",N,"matches",matches,"scan_s",round(elapsed,6))
# Model four logical workers, all 64 chunks complete, one duplicated delivery.
jobs=list(range(N//chunk)); arrivals=jobs+[7]; committed=set()
for j in arrivals:committed.add(j)
assert len(committed)*chunk==N and len(arrivals)*chunk-N==256
# 64-byte checkpoint: job id16, start9, end-exclusive9, next9, worker2,
# epoch4, status1, reserved14. Not a complete authenticated protocol.
checkpoint=bytes(16)+N.to_bytes(9,"big")+(N+256).to_bytes(9,"big")+(N+128).to_bytes(9,"big")+bytes(2+4+1+14)
assert len(checkpoint)==64
print("checkpoint_bytes",len(checkpoint),"completion_payload",len(jobs)*64,"duplicate_work",256)
print("median_scan_s",round(statistics.median(times),6),"median_keys_s",round(N/statistics.median(times),2))
# Synthetic incompressible baseline: fixed seed, not wallet data.
t=time.perf_counter()
baseline=b"".join(H.sha256(b"storage43"+i.to_bytes(4,"big")).digest() for i in range(2**18))
z=zlib.compress(baseline,6)
assert zlib.decompress(z)==baseline
print("synthetic_baseline",len(baseline),len(z),"generate_compress_check_s",round(time.perf_counter()-t,6))
print("checkpoint_json_bytes",len(json.dumps({"job":"00"*16,"start":format(2**70,"018x"),"end":format(2**70+2**32,"018x"),"next":format(2**70+2**31,"018x"),"worker":49,"epoch":1,"status":"running"},separators=(",",":")).encode()))
```

### I49 — replayed source

```python
import hashlib, random, time, platform
from statistics import mean

start = time.perf_counter()
address = 'bc1pg6luxm9s4qq65lge4l6ual7xwdw5v85eh675cmrl5we0ht3vpfhswxu0cx'
alphabet = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
generators = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
def decode(s):
    hrp, data = s.rsplit('1', 1)
    assert hrp == 'bc' and s == s.lower()
    words = [alphabet.index(c) for c in data]
    check = 1
    for word in [ord(c)>>5 for c in hrp] + [0] + [ord(c)&31 for c in hrp] + words:
        top = check >> 25
        check = ((check & 0x1ffffff) << 5) ^ word
        for i, g in enumerate(generators):
            if (top >> i) & 1:
                check ^= g
    bits = ''.join(format(word, '05b') for word in words[1:-6])
    assert check == 0x2bc830a3 and words[0] == 1
    assert len(bits) == 260 and bits[-4:] == '0000'
    return hex(check), words[0], len(bits[:-4]) // 8
print(decode(address))
try:
    decode(address[:-1]+'q')
except AssertionError:
    print('mutated checksum rejected')
else:
    raise RuntimeError('mutated checksum accepted')

# Independently salted synthetic domains. No Bitcoin keys or addresses.
for fold in (0, 1):
    rng = random.Random(4900 + fold)
    groups = [([], []) for _ in (4, 8)]
    for trial in range(4096):
        salt = (fold * 4096 + trial).to_bytes(2, 'big')
        x, y = rng.sample(range(4096), 2)
        h = lambda i: hashlib.sha256(salt + i.to_bytes(2, 'big')).digest()[0]
        diff = h(x) ^ h(y)
        for width, (hits, controls) in zip((4, 8), groups):
            if diff >> (8 - width) == 0:
                hits.append(abs(x-y)/4095)
                a, b = rng.sample(range(4096), 2)
                controls.append(abs(a-b)/4095)
    for width, (hits, controls) in zip((4, 8), groups):
        observed = mean(h-c for h,c in zip(hits, controls))
        null = random.Random(9100 + 10*fold + width)
        differences = [h-c for h,c in zip(hits,controls)]
        extreme = sum(abs(sum(d if null.getrandbits(1) else -d for d in differences)
                          / len(differences)) >= abs(observed) for _ in range(10000))
        p = (extreme+1)/10001
        print(fold, width, len(hits), mean(hits), mean(controls), p, min(1, 4*p))
print(platform.python_version(), platform.machine(), time.perf_counter()-start)
```

### I50 — replayed source

```python
from hashlib import sha256
from math import comb
from random import Random
from time import perf_counter

ALPHABET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
GENERATORS = (0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3)
RECIPIENT = "bc1pg6luxm9s4qq65lge4l6ual7xwdw5v85eh675cmrl5we0ht3vpfhswxu0cx"


def decode(address):
    if address not in (address.lower(), address.upper()) or len(address) > 90:
        raise ValueError("case or length")
    hrp, payload = address.lower().rsplit("1", 1)
    if hrp != "bc" or len(payload) < 7:
        raise ValueError("mainnet prefix or length")
    values = [ALPHABET.index(c) for c in payload]
    check = 1
    for value in [ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp] + values:
        top = check >> 25
        check = ((check & 0x1ffffff) << 5) ^ value
        for bit, generator in enumerate(GENERATORS):
            if (top >> bit) & 1:
                check ^= generator
    version, *words = values[:-6]
    if version != 1 or check != 0x2bc830a3:
        raise ValueError("version or checksum")
    stream = 0
    for word in words:
        stream = (stream << 5) | word
    bits = len(words) * 5
    pad = bits % 8
    if bits // 8 != 32 or pad >= 5 or stream & ((1 << pad) - 1):
        raise ValueError("program length or padding")
    return hrp, version, bits // 8, hex(check)


def address_checks():
    assert decode(RECIPIENT) == decode(RECIPIENT.upper())
    payload_start = RECIPIENT.index("1") + 1
    rejected = 0
    for index in range(payload_start, len(RECIPIENT)):
        for symbol in ALPHABET:
            if symbol == RECIPIENT[index]:
                continue
            mutation = RECIPIENT[:index] + symbol + RECIPIENT[index + 1:]
            try:
                decode(mutation)
            except ValueError:
                rejected += 1
            else:
                raise AssertionError("accepted a one-symbol mutation")
    assert rejected == 31 * (len(RECIPIENT) - payload_start)
    print("recipient", decode(RECIPIENT), "mutations rejected", rejected)


def toy_batch(label, seed, count):
    rng = Random(seed)
    widths = (4, 6, 8)
    near_hits = dict.fromkeys(widths, 0)
    random_hits = dict.fromkeys(widths, 0)
    near_only = dict.fromkeys(widths, 0)
    random_only = dict.fromkeys(widths, 0)
    for trial in range(count):
        secret = rng.randrange(1, 4095)
        near = secret + rng.choice((-1, 1))
        distant = (secret + rng.randrange(1024, 3073)) % 4096
        assert abs(distant - secret) >= 1024
        domain = b"toy50/" + label + trial.to_bytes(4, "big")
        expected, neighbor, baseline = (
            sha256(domain + value.to_bytes(2, "big")).digest()[0]
            for value in (secret, near, distant)
        )
        for width in widths:
            near_match = (expected ^ neighbor) >> (8 - width) == 0
            random_match = (expected ^ baseline) >> (8 - width) == 0
            near_hits[width] += near_match
            random_hits[width] += random_match
            near_only[width] += near_match and not random_match
            random_only[width] += random_match and not near_match
    p_values = {}
    for width in widths:
        discordant = near_only[width] + random_only[width]
        p = sum(comb(discordant, k) for k in range(near_only[width], discordant + 1))
        p_values[width] = p / (1 << discordant)
    adjusted = 0.0
    for rank, width in enumerate(sorted(widths, key=p_values.get)):
        adjusted = max(adjusted, min(1.0, (len(widths) - rank) * p_values[width]))
        difference = (near_hits[width] - random_hits[width]) / count
        print(label.decode(), width, near_hits[width], random_hits[width],
              near_only[width], random_only[width], f"{p_values[width]:.6f}",
              f"{adjusted:.6f}", "pass", adjusted < 0.05 and difference >= 0.005)


start = perf_counter()
address_checks()
print(f"address wall seconds {perf_counter() - start:.3f}")
for label, seed, count in [(b"dev", 500, 4096), (b"holdout", 501, 16384)]:
    start = perf_counter()
    toy_batch(label, seed, count)
    print(f"{label.decode()} wall seconds {perf_counter() - start:.3f}")
```
