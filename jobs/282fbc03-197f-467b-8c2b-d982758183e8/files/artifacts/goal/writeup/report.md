# Wide-parameter search on fast replicas vs T (paradigm.xyz/puzzles/amm) — write-up of goal results

## Result

**Yes, on the real engine, but by far less than the top 10 needs, and only as the item workers reported it.** Each item's worker states that every real-engine number below was measured on the pinned `amm_sim_rs` engine (each strategy alone against VanillaStrategy, `run_batch(..., 8)`, paired on the same held seeds). This write-up re-checks those numbers for internal consistency and checks the hashes. It could **not** re-run the engine (see "Verifiability").

| item | design | real gain over T (held seeds) | valid? |
|---|---|---|---|
| **head-a** | 8-unit ReLU net on top of T's fee, 130 params searched | **+1.2573, se 0.0620, n = 512** | yes: 0 OOG, afterSwap peak 231,381 |
| retune-b | CMA-ES retune of 79 of T's named constants | +0.6661, se 0.0487, n = 512 | yes: 0 OOG, peak 226,188 |
| head-b | 12-unit net searched, cut to 6 units | +0.7135, se 0.0313, n = 512 | **no**: afterSwap peak 245,690 > 245,000 |
| head-c | 16-unit net on top of T | +0.4803, se 0.0323, n = 512 | yes: 0 OOG, peak 235,199 |
| retune-a | CMA-ES retune of 41 T constants, 20 generations | −0.1693, se 0.0807, n = 192 (partial) | gas ok, but no gain and the run is incomplete |

- Best valid candidate: **head-a**, +1.257 over T (about 20 se above zero). That is roughly 29% of the ~+4.3 over T that the brief says the top 10 needs. No item gets near the top 10. Even head-a's chunk means (0.96 to 1.54) are all far below 4.3.
- Sources: the item records listed under "Inputs" (field `real` for gains, `gas` for gas). The T baseline (+0.271 se 0.013 over RS2, board 520.05, 27th, 4,000 seeds, 0 OutOfGas, afterSwap peak 226k), the 250,000 limit, the 245,000 gate and the ~+4.3 target are the goal brief's figures, quoted as given.
- Held seed sets are **different per item** (6000000.., 6010000.., 6020000.., 6030000.., 6040000..). So gains are paired *within* an item (candidate vs T on the same seeds) but not *across* items. Comparing head-a with retune-b treats the two as independent: difference 0.591, combined se ≈ 0.079.

## Verifiability (answers review finding 0536f5b4…)

The reviewer reported that the item result records behind these numbers were missing from the delivered tree. **That holds:** the records are inputs given to this write-up step and are not in Git. The step may only write `artifacts/goal/writeup/report.md`, so it cannot ship them. This section therefore puts everything the records contain about the real-engine runs into the report, says exactly what the records do *not* contain, and states how far the headline is verified.

**Inputs (the item result records, `application/json`, read as data):**

| item | record path given to this step | SHA-256 of record |
|---|---|---|
| retune-a | `artifacts/goal/items/retune-a/result.json` (= `.imd/reads/artifacts/item-retune-a`) | `8ee7000ab7ea7bb9fde702d8cecdd2499855479c7a9aeb551251e3e0d3aed9e7` |
| retune-b | `artifacts/goal/items/retune-b/result.json` (= `.imd/reads/artifacts/item-retune-b`) | `0bb3c4ff4fdfb98f452e5720bd5d4d7c30f673eb2bf7f945fd9a46432f104f36` |
| head-a | `artifacts/goal/items/head-a/result.json` (= `.imd/reads/artifacts/item-head-a`) | `2801efc8190e86318dd922d4a7179f63684d77a226047fc2f3c78232963eb690` |
| head-b | `artifacts/goal/items/head-b/result.json` (= `.imd/reads/artifacts/item-head-b`) | `afeee2a8fa538e4887ef36a48c5a1585a4eb9d1a591d1958c5ce7c9632a38981` |
| head-c | `artifacts/goal/items/head-c/result.json` (= `.imd/reads/artifacts/item-head-c`) | `af64c628de665247d7470b726d48f7396b99aba741ff1c0b88f43ceeff4ccc68` |

I recomputed all five SHA-256 values on this machine and they match the hashes the task gave.

**What the records contain and what they don't.** None of the five records includes per-seed paired deltas, per-seed retail/arb splits, or per-call gas logs. On the real engine they hold only: n, mean, se, the 5 worst seeds, mean retail/arb deltas, seed ranges and gas maxima. head-a and retune-a also include raw gas counters per callback, and head-a includes 8 chunk means. So **nobody can recompute the 512 per-seed deltas behind head-a's se from the delivered material, and they were never recorded in what was handed over.** Read the se values as each worker's own report.

**Checks run for this write-up:**
1. Each record's `code` field hashes (SHA-256 of the UTF-8 text) to the `sha256` the record states. All five match.
2. head-a: the mean of its 8 chunk means equals its `mean_diff`. This was recomputed and gives 1.257317072552457, the same as the record.
3. Retail delta + arb delta = mean_diff for every item, to 4 decimals (e.g. head-a 4.1957 − 2.9384 = 1.2573; retune-a 2.4774 − 2.6468 = −0.1693).
4. head-a cites 5 upstream evidence artifacts. I re-fetched all five on this machine: each returned HTTP 200, each body's SHA-256 equals its content address, and the embedded sources hash to the input hashes the items report:
   - [T](https://api.imd.fun/artifacts/6ac5e013b7b1fb4c5e7bdcdfec0aba28b16824e18ccf39500f258533879faffe): `code` → `ebd9de9b…`
   - [RS2](https://api.imd.fun/artifacts/19f2ec857df536e8ab62ab1da89ec6623332521ce46849f15bccff402c63e1e5): `code` → `f24b6ca1…`
   - [replica](https://api.imd.fun/artifacts/e8a7a2af9039c24b8bb2d3b5fa1c9113606cbf5a480ac07d02ca26750f1752ea): `replica_source` → `1e4c44b4…`
   - [port](https://api.imd.fun/artifacts/d845a4b94eab87f23956fd1939c0135d955df212d1f3037f2a761c178cef7a0e): `port_source` → `9eac3553…`
   - [decomposition harness](https://api.imd.fun/artifacts/33f54e81f3372088e9eced52c0174f310ac348af98ef5727b73785c088679194)

   So head-a, head-c (which lists the same four hashes) and the others started from the agreed T, RS2, replica and port.
5. **Independent re-run attempted and failed.** I cloned `benedictbrady/amm-challenge` at `6b6921f8d463314aa7c96234e1be25a25245f704` and started the brief's setup script. Its GitHub release downloads (the `uv` tarball and the pinned `amm_sim_rs-0.1.0.post1` wheel from `github.com/gtmcknight/amm-sim/releases/download/sim-6b6921f8/`) failed. The release-asset redirect returned HTTP 504 on this machine: twice for `uv` and once for the wheel. Without the pinned wheel there is no real engine, so **none of the real-engine figures in this report was reproduced here.**

**How to reproduce the headline** with the pinned setup from the brief:
- Compile the head-a code below (sha256 `99e3a2ec…90fe`) and T (sha256 `ebd9de9b…19b3`, the `code` of the T artifact above).
- Run each alone against VanillaStrategy with `amm_sim_rs.run_batch(X, VanillaStrategy, configs, 8)` on seeds 6020000..6020511, with configs per `MatchRunner._build_configs`, in 64-seed chunks, one run per seed per arm.
- Take the per-seed edge difference.
- Expected chunk means: see the head-a table. Expected overall: 1.2573 (se 0.0620). Gas: candidate afterSwap max 231,381 over 5,439,483 calls, 0 OOG.

**Status of the conclusion:** the workers measured the "yes" on the real engine. This write-up has checked it for consistency and hashes but has **not independently verified** it.

## Weight of flagged sources

The task notes that some results cite sources that did not hold when re-read: retune-a 3, retune-b 2, head-a 4, head-b 1, head-c 3. The records I was handed don't say which sources those are. Only head-a lists URLs at all, and all five of those re-read correctly here (check 4 above). So the flagged ones must sit in sources lists that were not passed to this step. As a result:
- Every *measurement* in this report is a worker's local measurement, as its record states. head-a, for example, says "gates and confirmation are not copied from upstream artifacts".
- Anything that rests on outside sources is weighted down: setup provenance, the description of T and RS2, and the organizer's claims about leaders. That matters most for **head-a** (the headline, 4 flagged sources) and for **retune-a**, which also skipped the brief's CH check.
- Upstream inputs are checked by hash (check 4), not by quotation, so the flagged sources do not touch the identity of T, RS2, the replica or the port.

## Gates (shared definitions)

- **A:** the replica's T port matches EVM T's fees.
- **B:** the replica reproduces T − RS2 on 4,096 markets (31000000..31004095).
- **C:** the frozen candidate's port matches its Solidity fees.

Every item reports Gate A max fee difference 1.2216616607219066e-09 bps and Gate B 0.2420270811033297, se 0.01692058854320023. Those equal values across items come from the shared replica, T port and seeds. Gate B (+0.242) differs from the real-engine T − RS2 of +0.271 se 0.013 (brief) by 0.029, about 1.4 combined se. Head-a's own required interval was [0.17, 0.37] and head-b's target was 0.27 ± 0.10, and Gate B is inside both.

## Per-item results

All figures come from the item record named in each heading. "Gain" means candidate minus T in mean edge, paired on the same seeds. "Replica gain" is the monitor score on markets 30000000..30002047 (2,048 markets, paired against the T port), unless stated otherwise.

### retune-a: CMA-ES retune of T's declared constants (record `8ee7000a…`)

| field | value |
|---|---|
| design | 38 declared constants of T (`REVERT_U` excluded) plus the anchor N, k_lin and k_quad, so 41 dims. CMA-ES with sigma0 0.15 and 256-market blocks. Inline literals were **not** searched (a disclosed deviation). |
| gates A / B / C | pass (1.22e-9 bps) / pass (0.2420 se 0.0169, 4,096 mkts) / pass (2.48e-9 bps, 20 seq) |
| CH check | **not run**: the worker ran only 0..19 (mean 561.15) because a full run takes ~14 min on 1 CPU |
| replica speed | 101.8 markets/s (worker reports a 1-CPU cgroup limit) |
| search | 20 generations, 14.3 min |
| replica gain, end of curve | −0.0121 se 0.0230 (gen 20). Best monitor −0.0086 se 0.0246 (gen 10). Curve: 2 points, **flat, not rising**. Population means ran −1.9 to −12.2 per generation. |
| real gain over T | n = **192** (seeds 6000000..6000191, stopped by time before 512): **−0.1693, se 0.0807** |
| worst seeds | 6000120 −3.468; 6000062 −3.092; 6000081 −2.698; 6000021 −2.631; 6000029 −2.582 |
| retail / arb delta | +2.4774 (se 0.0826) / −2.6468 (se 0.0574) |
| gas | afterSwap peak 223,298, afterInitialize 243,115, 0 OOG, 0 other errors (1,995,345 afterSwap calls) |
| candidate sha256 | `d6cd642806e704f1b074c0145736b637c9c7a29a6b8d9b88348ac8f9758a3323` |

**Carry-over:** the replica said "no gain" (−0.009) and the real engine agrees: −0.17 ± 0.08, about 2 se below zero, which is consistent with no gain or a small loss. The search was too short and too narrow to say anything about the method itself.

### retune-b: CMA-ES retune of (almost) all named constants of T (record `0bb3c4ff…`)

| field | value |
|---|---|
| design | 79 dims, all of T's named constants except brief or structural exclusions. Two convex-weight pairs are tied: `ROUTE_NEW = 1−ROUTE_OLD` and `STALE_FAST = 1−STALE_SLOW`. Logit/log coordinates. CMA-ES seed 12, pop 16, sigma0 0.15, starting from T. 256 common-random-number markets per generation. |
| restart | A first run that left the pairs untied fell to −34.8 at gen 10. It was discarded and only the restart is reported (disclosed). |
| gates A / B / C | pass (1.22e-9) / pass (0.2420 se 0.0169) / pass (1.91e-9, 20 seq) |
| CH check | run: 525.5258821780834 on 0..999, as expected |
| replica speed | 478.4 markets/s |
| search | 190 generations, 30.3 min |
| replica gain, end of curve | **+0.6879 se 0.0216** (gen 190, the final monitor and a new high; earlier peak 0.656 at gen 150). **Noisy but still rising slowly** (sigma ≈ 0.073). |
| real gain over T | n = 512, seeds 6010000..6010511: **+0.6661, se 0.0487**. Candidate mean 530.976, T mean 530.309. 78.5% of seeds positive. |
| worst seeds | 6010056 −4.391; 6010167 −1.894; 6010267 −1.843; 6010098 −1.777; 6010380 −1.693 |
| retail / arb delta | +2.4045 (se 0.0541) / −1.7384 (se 0.0295). Replica: +2.4207 / −1.7328. |
| gas | afterSwap peak 226,188 (T on the same seeds 223,348), afterInitialize 243,115, 0 OOG, 0 reverts |
| candidate sha256 | `b9a6cfc6dea448a249d9ac9091814af535ee7c8d308d15173846815ffc39adc5` |

**Carry-over: yes, closely.** Replica +0.688 vs real +0.666, a gap of 0.02, well inside the se. The retail/arb split also matches to within about 0.02.

### head-a: 8-unit neural head on T (record `2801efc8…`), the best valid result

| field | value |
|---|---|
| design | fee = T fee + net output. 13 features, in order: sigmaHat, lambdaHat, sizeHat, toxEma, actEma, direction, (spot−staleHat)/staleHat, signed trade ratio, arb probability, first-in-step, uncertainty, min(silent,8)/8, anchor mean. Features are clipped to [−4, 4], go through an 8-unit ReLU layer clipped to [0, 4], and produce 2 outputs (bid/ask fee, unit 1e-4). That is 130 params, all searched. Weights use 1e6 fixed point. T's toxicity anchor is kept (cap 674, k_lin 0.7127, k_quad 1.2952 in WAD). W2 and the biases start at 0, so generation 0 equals T. |
| search | CMA-ES seed 21, pop 16, sigma0 0.2, 413 generations, 256 markets per generation from train seeds 22000000..22105727. Monitored every 10 generations; the frozen candidate is the monitor maximum. |
| gates A / B / C | pass (1.22e-9 bps, threshold 0.01) / pass (0.2420 se 0.0169, required [0.17, 0.37]) / pass (7.60e-5 bps, threshold 0.1, 20 seq × 2,000 callbacks) |
| CH check | run: 525.5258821780834 on 0..999, abs error 0.0 |
| replica speed | 759.1 markets/s for the T port (RS2 port 613.2). 4,096 markets of 10,000 steps, 8 processes. |
| search | 44.3 min |
| replica gain, end of curve | **+1.1515 se 0.0214** at gen 410, the final monitor and a new high. Curve: 0.31 (g10), 0.72 (g40), 1.04 (g220–280), 1.10 (g370), 1.15 (g410). **Still rising**, slowly, in steps. |
| real gain over T | n = 512, seeds 6020000..6020511, 64-seed chunks, run once in ascending order: **+1.2573, se 0.0620** |
| chunk means | 6020000: 1.1425 · 6020064: 1.2991 · 6020128: 1.5408 · 6020192: 0.9598 · 6020256: 1.2137 · 6020320: 1.1967 · 6020384: 1.3237 · 6020448: 1.3822 (all 8 positive; their mean is 1.2573) |
| worst seeds | 6020246 −2.179; 6020336 −2.022; 6020180 −1.645; 6020487 −1.279; 6020342 −1.267 |
| retail / arb delta | +4.1957 (se 0.0693) / −2.9384 (se 0.0257). Decomposition reconciles to 1.1e-13. |
| gas | **Candidate:** afterSwap peak **231,381** over 5,439,483 calls, 0 OOG, 0 other failures. afterInitialize 243,147 (512 calls), getName 21,654. **T on the same seeds:** afterSwap peak 223,251 over 5,280,593 calls, afterInitialize 243,115. **Vanilla:** afterSwap peak 22,592. |
| candidate sha256 | `99e3a2eceae0e5543d27473859e10b005d0ce0aa7067f2e1a24d1e0e4a7390fe` (code below) |

**Carry-over: yes.** The real gain (+1.257 ± 0.062) is slightly *above* the replica's +1.152 ± 0.021. The gap is 0.11, about 1.6 combined se. The candidate takes much more retail edge and gives back more to arbitrage than T does.

### head-b: 12-unit head searched, frozen as 6 units (record `afeee2a8…`)

| field | value |
|---|---|
| design | fee_side = clamp(T fee + h_side·1e-4, 0, MAX_FEE), with h = W2·clamp(W1·xn + b1, 0, 4) + b2 in bps. Same 13 features, normalized by constants from 48 T-port markets and clipped to ±4. 12 units searched (194 params). CMA-ES seed 22, pop 16, sigma0 0.3, 256 markets per generation. |
| gates A / B / C | pass (1.22e-9) / pass (0.2420 se 0.0169, target 0.27 ± 0.10) / pass (3.47e-9 for the frozen 6-unit; the 12-unit gave 7.8e-10) |
| CH check | worker notes it passed: 525.5258821780834 |
| replica speed | 455.1 markets/s without head (4 procs), about 311 markets/s with the 12-unit head |
| search | 137 generations, 33.4 min |
| replica gain, end of curve | best +0.8222 se 0.0183 at **gen 90**, then 0.796, 0.812, 0.784, 0.769 at gens 100–130: **plateaued or declining, not rising**. The frozen 6-unit version scored +0.7538 se 0.0179. The worker flags this as optimistic: the 6 units were chosen by \|W2\| and compared on the first 1,024 monitor markets. |
| real gain over T | n = 512, seeds 6030000..6030511: **+0.7135, se 0.0313**. Candidate mean 522.547, T mean 521.834. |
| worst seeds | 6030029 −2.131; 6030100 −1.871; 6030284 −1.709; 6030407 −1.559; 6030127 −1.257 |
| retail / arb delta | +3.1343 (se 0.0369) / −2.4209 (se 0.0213) |
| gas | afterSwap peak **245,690 > 245,000**, so **INVALID** under the brief, with 0 OOG (T on the same seeds 225,592). afterInitialize 243,121. The earlier 12-unit frozen candidate scored +0.793 ± 0.033 but had **62 afterSwap OOG calls** and was invalid. |
| seed reuse | The 6-unit run is a disclosed **second real run on the same 512 seeds**. The cut used \|W2\| rank, not the real results, but the held set is no longer clean. |
| candidate sha256 | `fab2b1966e8cd76d92608948c77285a8546335731901fbb3e9ebd36dbd274b22` |

**Carry-over: yes, approximately.** Replica +0.754 (6-unit) vs real +0.713, so the replica overstated by about 0.04. The candidate fails the gas rule. The worker estimates it needs about 700+ gas saved and a re-run before it could count.

### head-c: 16-unit head on T (record `af64c628…`)

| field | value |
|---|---|
| design | 13 scaled features (×1000 etc.), clipped to [−4, 4], feed 16 hidden units with min(4, max(0, z)) and 2 outputs in bps. Coefficients use 1e9 fixed point. All weights are optimized, the output starts at 0, and T's anchor is kept. CMA-ES seed 23, pop 16, sigma0 0.3, 211 generations, 256 markets per generation (train seeds 24000000..24054015). Monitored every 10 generations, with T itself (gain 0) as a candidate. |
| gates A / B / C | pass (1.22e-9) / pass (0.2420 se 0.0169; 348.8 markets/s) / pass (1.32e-8, 20 seq) |
| CH check | run: 525.5258821780834 on 0..999 (243.9 s) |
| replica speed | 348.8 markets/s |
| search | 43.1 min |
| replica gain, end of curve | best +0.4806 se 0.0171 at gen 160, flat through 200, then +0.389 at 210: **plateaued, not rising** |
| real gain over T | n = 512, seeds 6040000..6040511: **+0.4803, se 0.0323** |
| worst seeds (diff / retail / arb) | 6040170 −2.014 / −0.386 / −1.628; 6040026 −1.439 / +0.501 / −1.941; 6040388 −1.356 / +1.062 / −2.418; 6040338 −1.269 / +0.334 / −1.603; 6040061 −1.160 / −0.188 / −0.972 |
| retail / arb delta | +1.7237 / −1.2435 (no se in record). Decomposition reconciles to 1.1e-13. |
| gas | afterSwap peak 235,199 over 5,319,377 calls, 0 OOG, 0 revert/halt/tx-error/bad-return. afterInitialize 243,182. |
| candidate sha256 | `7efaaf440a3cf22ad2ac38a9f0ffc495ea4199c7f8b14342949fda322aef77c2` |

**Carry-over: yes, almost exactly.** Replica +0.4806 vs real +0.4803.

## Did replica gains carry over? (summary)

| item | replica (monitor) | real (held) | real − replica | curve at end |
|---|---|---|---|---|
| retune-a | −0.0086 ± 0.0246 | −0.169 ± 0.081 (n = 192) | −0.16 (≈2 se) | flat (2 points) |
| retune-b | +0.6879 ± 0.0216 | +0.666 ± 0.049 | −0.02 | slowly rising |
| head-a | +1.1515 ± 0.0214 | +1.257 ± 0.062 | +0.11 | rising |
| head-b | +0.7538 ± 0.0179 (6-unit) | +0.713 ± 0.031 | −0.04 | plateau after gen 90 |
| head-c | +0.4806 ± 0.0171 | +0.480 ± 0.032 | −0.00 | plateau after gen 160 |

All four items with a positive replica gain kept it on the real engine, to within 0.11. The monitor set is therefore a reliable predictor at the ±0.1 level. The replica's ability to *propose* is confirmed; it was not the bottleneck.

## Blocked and incomplete items

- **No item is blocked:** `blocked` is null in all five records.
- **retune-a is incomplete:** the real run covers 192 of 512 seeds, the CH check was not run, inline literals were not searched, and there were only 20 generations on a 1-CPU machine.
- **head-b is invalid on gas:** peak 245,690 > 245,000. Its 12-unit predecessor had 62 OOG calls. It also reuses its held seeds.

## Positive real gains: code and hashes

The brief asks for complete code of any file with a positive real gain. Four items qualify: head-a, retune-b, head-b (gas-invalid) and head-c. Their code is 25.5 kB, 21.4 kB, 27.0 kB and 32.2 kB, about 106 kB together, which does not fit the 64,000-byte cap of this report. So only the **recommended valid candidate, head-a**, is given in full below. For the others the sha256 values identify the exact file; the full text is in each record's `code` field (record hashes above), and I checked each against its stated sha256:

- retune-b `b9a6cfc6dea448a249d9ac9091814af535ee7c8d308d15173846815ffc39adc5` (record `0bb3c4ff…`)
- head-b `fab2b1966e8cd76d92608948c77285a8546335731901fbb3e9ebd36dbd274b22` (record `afeee2a8…`), not valid as is
- head-c `7efaaf440a3cf22ad2ac38a9f0ffc495ea4199c7f8b14342949fda322aef77c2` (record `af64c628…`)

### head-a `Strategy.sol` — sha256 `99e3a2eceae0e5543d27473859e10b005d0ce0aa7067f2e1a24d1e0e4a7390fe`

The hash is of the exact text between the fences, which ends with a single newline.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {AMMStrategyBase} from "./AMMStrategyBase.sol";
import {TradeInfo} from "./IAMMStrategy.sol";

contract Strategy is AMMStrategyBase {
    uint256 constant ELAPSED_CAP = 8;
    uint256 constant SIGNAL_THRESHOLD = WAD / 650;
    uint256 constant DIR_DECAY = 750000000000000000;
    uint256 constant ACT_DECAY = 530000000000000000;
    uint256 constant SIZE_DECAY = 530000000000000000;
    uint256 constant TOX_DECAY = 910000000000000000;
    uint256 constant SIGMA_DECAY = 690000000000000000;
    uint256 constant LAMBDA_DECAY = 990000000000000000;
    uint256 constant SIZE_BLEND_DECAY = 828000000000000000;
    uint256 constant TOX_BLEND_DECAY = 51000000000000000;
    uint256 constant ACT_BLEND_DECAY = 985000000000000000;
    uint256 constant PHAT_ALPHA = 270000000000000000;
    uint256 constant PHAT_ALPHA_RETAIL = 60000000000000000;
    uint256 constant PHAT_ALPHA_SAME = 120000000000000000;
    uint256 constant REVERT_U = 0;
    uint256 constant DIR_IMPACT_MULT = 4;
    uint256 constant GATE_SIGMA_MULT = 7200000000000000000;
    uint256 constant MIN_GATE = 30000000000000000;
    uint256 constant TRADE_TOX_BOOST = 3500 * BPS;
    uint256 constant STALE_ATTRACT_FRAC = 1050000000000000000;
    uint256 constant RET_CAP = WAD / 35;
    uint256 constant TOX_CAP = WAD / 5;
    uint256 constant TRADE_RATIO_CAP = WAD / 5;
    uint256 constant LAMBDA_CAP = 1820000000000000000;
    uint256 constant STEP_COUNT_CAP = 64;
    uint256 constant BASE_FEE = 4 * BPS;
    uint256 constant SIGMA_COEF = 200000000000000000;
    uint256 constant LAMBDA_COEF = 12 * BPS;
    uint256 constant FLOW_SIZE_COEF = 4842 * BPS;
    uint256 constant TOX_COEF = 300 * BPS;
    uint256 constant TOX_QUAD_COEF = 15000 * BPS;
    uint256 constant ACT_COEF = 91843 * BPS;
    uint256 constant DIR_COEF = 20 * BPS;
    uint256 constant DIR_TOX_COEF = 100 * BPS;
    uint256 constant STALE_DIR_COEF = 6850 * BPS;
    uint256 constant SIGMA_TOX_COEF = 500 * BPS;
    uint256 constant TAIL_KNEE = 600 * BPS;
    uint256 constant TAIL_SLOPE_PROTECT = 930000000000000000;
    uint256 constant TAIL_SLOPE_ATTRACT = 850000000000000000;

    function afterInitialize(uint256 initialX, uint256 initialY) external override returns (uint256, uint256) {
        slots[0] = BASE_FEE; slots[1] = BASE_FEE; slots[3] = WAD; 
        slots[5] = initialX > 0 ? wdiv(initialY, initialX) : 100 * WAD;
        slots[6] = 950000000000000; slots[7] = 800000000000000000; slots[8] = 2000000000000000;
        slots[15] = 400000000000000000 | (uint256(2000000000000000) << 160); slots[13] = 902500000000; slots[14] = slots[5]; 
        return (BASE_FEE, BASE_FEE);
    }

    function afterSwap(TradeInfo calldata trade) external override returns (uint256, uint256) {
        uint256 prevBidFee = slots[0]; uint256 prevAskFee = slots[1]; uint256 lastTs = uint64(slots[2]);
        uint256 dirState = slots[3]; uint256 actEma = slots[4]; uint256 pHat = slots[5];
        uint256 sigmaHat = slots[6]; uint256 lambdaHat = slots[7]; uint256 sizeHat = slots[8];
        uint256 toxEma = slots[9]; uint256 stepTradeCount = slots[10];

        uint256 sigmaForFast = sigmaHat;
        uint256 fastHat = slots[14];
        uint256 uncertainty = slots[13];
        uint256 silent = trade.timestamp > lastTs ? trade.timestamp - lastTs : 0;
        bool isNewStep = trade.timestamp > lastTs;
        if (isNewStep) {
            uint256 elapsedRaw = trade.timestamp - lastTs;
            uint256 elapsed = elapsedRaw > ELAPSED_CAP ? ELAPSED_CAP : elapsedRaw;
            dirState = _decayCentered(dirState, DIR_DECAY, elapsed);
            actEma = wmul(actEma, _powWad(ACT_DECAY, elapsed));
            sizeHat = wmul(sizeHat, _powWad(SIZE_DECAY, elapsed));
            toxEma = wmul(toxEma, _powWad(TOX_DECAY, elapsed));
            if (stepTradeCount > 0 && elapsedRaw > 0) {
                uint256 lambdaInst = (stepTradeCount * WAD) / elapsedRaw;
                if (lambdaInst > LAMBDA_CAP) lambdaInst = LAMBDA_CAP;
                lambdaHat = wmul(lambdaHat, LAMBDA_DECAY) + wmul(lambdaInst, WAD - LAMBDA_DECAY);
            }
            // Process variance is propagated inside the censored update.
            if (uncertainty > 100000000000000) uncertainty = 100000000000000;
            stepTradeCount = 0;
        }

        bool firstInStep = stepTradeCount == 0;
        uint256 spot = trade.reserveX > 0 ? wdiv(trade.reserveY, trade.reserveX) : pHat;
        if (pHat == 0) pHat = spot;

        uint256 feeUsed = trade.isBuy ? prevBidFee : prevAskFee;
        uint256 gamma = feeUsed < WAD ? WAD - feeUsed : 0;
        uint256 pImplied;
        if (gamma == 0) { pImplied = spot; }
        else { pImplied = trade.isBuy ? wmul(spot, gamma) : wdiv(spot, gamma); }

        // S: infer a no-trade interval center from the last post-trade spot.
        uint256 silenceScale = WAD;
        if (firstInStep && silent > 1) {
            uint256 g = silent - 1;
            if (g > 1) g = 1;
            uint256 w = WAD - _powWad(800000000000000000, g);
            uint256 s = slots[2] >> 64;
            if (s == 0) s = pHat;
            uint256 c = (wmul(s, WAD - prevBidFee) + wdiv(s, WAD - prevAskFee)) / 2;
            if (c >= pHat) pHat += wmul(w, c - pHat);
            else pHat -= wmul(w, pHat - c);
            silenceScale = WAD - wmul(300000000000000000, w);
        }

        {
            uint256 ret = pHat > 0 ? wdiv(absDiff(pImplied, pHat), pHat) : 0;
            uint256 alpha = firstInStep ? PHAT_ALPHA : PHAT_ALPHA_RETAIL;
            uint256 prePhat = pHat;
            bool secondPrint = !firstInStep && stepTradeCount == 1;
            bool sameDir = false; bool oppDir = false;
            if (secondPrint) {
                bool up2 = pImplied >= pHat;
                uint256 d1 = slots[12];
                if (d1 != 0) { sameDir = (d1 == 1) == up2; oppDir = !sameDir; }
                if (sameDir) alpha = PHAT_ALPHA_SAME;
            }
            if (firstInStep) { slots[12] = pImplied >= pHat ? 1 : 2; }
            uint256 adaptiveGate = wmul(sigmaHat, GATE_SIGMA_MULT);
            if (adaptiveGate < MIN_GATE) adaptiveGate = MIN_GATE;
            alpha = wmul(alpha, silenceScale);
            adaptiveGate = wmul(adaptiveGate, silenceScale);
            if (ret <= adaptiveGate) { pHat = wmul(pHat, WAD - alpha) + wmul(pImplied, alpha); }
            if (oppDir && REVERT_U > 0) {
                uint256 pre = slots[11];
                if (pre > pHat) pHat = pHat + wmul(pre - pHat, REVERT_U);
                else pHat = pHat - wmul(pHat - pre, REVERT_U);
            }
            if (firstInStep) {
                if (ret > RET_CAP) ret = RET_CAP;
                sigmaHat = wmul(sigmaHat, SIGMA_DECAY) + wmul(ret, WAD - SIGMA_DECAY);
            }
        }

        // Interior retail routing equalizes fee-adjusted marginal prices.
        // Subsequent trades in a step cannot be the initial arbitrage trade.
        if (!firstInStep && feeUsed > 30 * BPS && gamma > 0) {
            uint256 normalSpot = trade.isBuy
                ? wdiv(wmul(spot, gamma), WAD - 30 * BPS)
                : wdiv(wmul(spot, WAD - 30 * BPS), gamma);
            pHat = wmul(pHat, 90 * WAD / 100) + wmul(normalSpot, 10 * WAD / 100);
        }

        // Censored assumed-density posterior. No external or future inputs.
        uint256 arbProbability;
        (fastHat, uncertainty, arbProbability) = _posterior(PosteriorInput(
            fastHat, uncertainty, pImplied, spot, slots[2] >> 64,
            prevBidFee, prevAskFee, firstInStep, silent, trade.isBuy,
            trade.reserveY > 0 ? wdiv(trade.amountY, trade.reserveY) : 0
        ));
        slots[13] = uncertainty;
        slots[14] = fastHat;
        uint256 tradeRatio = trade.reserveY > 0 ? wdiv(trade.amountY, trade.reserveY) : 0;
        if (tradeRatio > TRADE_RATIO_CAP) tradeRatio = TRADE_RATIO_CAP;

        if (tradeRatio > SIGNAL_THRESHOLD) {
            uint256 push = tradeRatio * DIR_IMPACT_MULT;
            if (push > WAD / 4) push = WAD / 4;
            if (trade.isBuy) {
                dirState = dirState + push;
                if (dirState > 2 * WAD) dirState = 2 * WAD;
            } else {
                dirState = dirState > push ? dirState - push : 0;
            }
            actEma = wmul(actEma, ACT_BLEND_DECAY) + wmul(tradeRatio, WAD - ACT_BLEND_DECAY);
            sizeHat = wmul(sizeHat, SIZE_BLEND_DECAY) + wmul(tradeRatio, WAD - SIZE_BLEND_DECAY);
            if (sizeHat > WAD) sizeHat = WAD;
        }

        uint256 tox = pHat > 0 ? wdiv(absDiff(spot, pHat), pHat) : 0;
        if (tox > TOX_CAP) tox = TOX_CAP;
        toxEma = wmul(toxEma, TOX_BLEND_DECAY) + wmul(tox, WAD - TOX_BLEND_DECAY);
        uint256 toxSignal = toxEma;
        uint256 toxLinear;
        uint256 toxQuadratic;
        {
            uint256 packedAnchor = slots[16];
            uint256 runMean = uint64(packedAnchor);
            uint256 sampleCount = packedAnchor >> 64;
            if (sampleCount < 674) sampleCount++;
            if (toxEma >= runMean) runMean += (toxEma-runMean)/sampleCount;
            else runMean -= (runMean-toxEma)/sampleCount;
            slots[16] = runMean | (sampleCount << 64);
            toxLinear = _anchorBlend(runMean, toxEma, 712696014807650816);
            toxQuadratic = _anchorBlend(runMean, toxEma, 1295240753826310656);
        }


        stepTradeCount = stepTradeCount + 1;
        if (stepTradeCount > STEP_COUNT_CAP) stepTradeCount = STEP_COUNT_CAP;

        uint256 originalLambda = lambdaHat; uint256 originalSize = sizeHat;

        if (342406799193418304 > 0) {
            uint256 packedFlow = slots[15];
            uint256 rate = uint80(packedFlow);
            uint256 count = uint80(packedFlow >> 80);
            uint256 meanSize = uint80(packedFlow >> 160);
            if (rate == 0) rate = 400000000000000000;
            if (meanSize == 0) meanSize = 2000000000000000;
            if (isNewStep) {
                uint256 inst = count / silent;
                if (inst > 3 * WAD) inst = 3 * WAD;
                uint256 retention = _powWad(999000000000000000, silent > 64 ? 64 : silent);
                rate = wmul(rate, retention) + wmul(inst, WAD-retention);
                count = 0;
            }
            uint256 weight = firstInStep ? WAD-arbProbability : WAD;
            uint256 correctedWeight = weight;
            if (2 == 2) {
                uint256 missing = wmul(feeUsed, 196030880396139429888);
                if (missing > 333333333333333376) missing = 333333333333333376;
                correctedWeight = wdiv(weight, WAD-missing);
            }
            count += correctedWeight;
            uint256 learning = wmul(WAD-999000000000000000, weight);
            meanSize = _blend(meanSize, tradeRatio, learning);
            slots[15]=rate | (count << 80) | (meanSize << 160);
            uint256 retailRate = wmul(rate, 366383424913407168);
            uint256 retailSize = 2 == 0 ? sizeHat : wmul(meanSize,1883296158119298304);
            lambdaHat = _blend(lambdaHat,retailRate,342406799193418304);
            sizeHat = _blend(sizeHat,retailSize,342406799193418304);
        }
        uint256 flowSize = wmul(lambdaHat, sizeHat);
        uint256 fBase = BASE_FEE + wmul(SIGMA_COEF, sigmaHat) + wmul(LAMBDA_COEF, lambdaHat) + wmul(FLOW_SIZE_COEF, flowSize);
        uint256 fMid = fBase + wmul(TOX_COEF, toxLinear) + wmul(TOX_QUAD_COEF, wmul(toxQuadratic, toxQuadratic)) + wmul(ACT_COEF, actEma);
        fMid = fMid + wmul(SIGMA_TOX_COEF, wmul(sigmaHat, toxLinear));

        lambdaHat = originalLambda; sizeHat = originalSize;
        uint256 dirDev; bool sellPressure;
        if (dirState >= WAD) { dirDev = dirState - WAD; sellPressure = true; }
        else { dirDev = WAD - dirState; sellPressure = false; }

        uint256 skew = wmul(DIR_COEF, dirDev) + wmul(DIR_TOX_COEF, wmul(dirDev, toxSignal));
        uint256 bidFee; uint256 askFee;
        if (sellPressure) {
            bidFee = fMid + skew;
            askFee = fMid > skew ? fMid - skew : 0;
        } else {
            askFee = fMid + skew;
            bidFee = fMid > skew ? fMid - skew : 0;
        }

        {
            uint256 staleHat = wmul(pHat, 700000000000000000) + wmul(fastHat, 300000000000000000);
            uint256 staleTox = wdiv(absDiff(spot, staleHat), staleHat);
            if (staleTox > TOX_CAP) staleTox = TOX_CAP;
            uint256 staleShift = wmul(STALE_DIR_COEF, staleTox);
            uint256 attractShift = wmul(staleShift, STALE_ATTRACT_FRAC);
            if (spot >= staleHat) {
                bidFee = bidFee + staleShift;
                askFee = askFee > attractShift ? askFee - attractShift : 0;
            } else {
                askFee = askFee + staleShift;
                bidFee = bidFee > attractShift ? bidFee - attractShift : 0;
            }
        }

        {
            bool tradeAligned = (trade.isBuy && spot >= pHat) || (!trade.isBuy && spot < pHat);
            if (tradeAligned) {
                uint256 tradeBoost = wmul(TRADE_TOX_BOOST, tradeRatio);
                if (!firstInStep && tradeBoost > 16 * BPS) tradeBoost = 16 * BPS;
                if (trade.isBuy) { bidFee = bidFee + tradeBoost; }
                else { askFee = askFee + tradeBoost; }
            }
        }

        if (sellPressure) {
            bidFee = clampFee(_compressTailWithSlope(bidFee, TAIL_SLOPE_PROTECT));
            askFee = clampFee(_compressTailWithSlope(askFee, TAIL_SLOPE_ATTRACT));
        } else {
            askFee = clampFee(_compressTailWithSlope(askFee, TAIL_SLOPE_PROTECT));
            bidFee = clampFee(_compressTailWithSlope(bidFee, TAIL_SLOPE_ATTRACT));
        }

        if (firstInStep) {
            if (askFee > bidFee && bidFee > 30 * BPS) bidFee = 30 * BPS;
            else if (bidFee > askFee && askFee > 30 * BPS) askFee = 30 * BPS;
        }

        if (bidFee > askFee && askFee > 36 * BPS) askFee = 36 * BPS;
        else if (askFee > bidFee && bidFee > 36 * BPS) bidFee = 36 * BPS;

        {
            int256[13] memory nx;
            unchecked {
                nx[0] = int256(sigmaHat)*1000/1e12-1000000;
                nx[1] = int256(lambdaHat)*2/1e12-1000000;
                nx[2] = int256(sizeHat)*500/1e12-1000000;
                nx[3] = int256(toxEma)*500/1e12-1000000;
                nx[4] = int256(actEma)*500/1e12-1000000;
                nx[5] = int256(dirState)/1e12-1000000;
                uint256 nh = wmul(pHat,700000000000000000)+wmul(fastHat,300000000000000000);
                nx[6] = (int256(spot)-int256(nh))*500000000/int256(nh);
                nx[7] = int256(tradeRatio)*500/1e12;
                if (!trade.isBuy) nx[7] = -nx[7];
                nx[8] = int256(arbProbability)*2/1e12-1000000;
                nx[9] = firstInStep ? int256(1000000) : -int256(1000000);
                nx[10] = int256(uncertainty)/1e6-1000000;
                nx[11] = int256(silent>8 ? 8 : silent)*1000000/8;
                nx[12] = int256(uint256(uint64(slots[16])))*500/1e12-1000000;
                for (uint256 ni=0;ni<13;ni++) {
                    if(nx[ni]>4000000) nx[ni]=4000000;
                    if(nx[ni]<-4000000) nx[ni]=-4000000;
                }
                (int256 hb,int256 ha) = _head(nx);
                int256 nb = int256(bidFee)+hb*100000000;
                int256 na = int256(askFee)+ha*100000000;
                bidFee = nb<0 ? 0 : (nb>int256(MAX_FEE) ? MAX_FEE : uint256(nb));
                askFee = na<0 ? 0 : (na>int256(MAX_FEE) ? MAX_FEE : uint256(na));
            }
        }

        slots[0] = bidFee; slots[1] = askFee; slots[2] = (spot << 64) | trade.timestamp;
        slots[3] = dirState; slots[4] = actEma; slots[5] = pHat;
        slots[6] = sigmaHat; slots[7] = lambdaHat; slots[8] = sizeHat;
        slots[9] = toxEma; slots[10] = stepTradeCount;

        return (bidFee, askFee);
    }



    function _head(int256[13] memory x) internal pure returns (int256 b,int256 a) {
        unchecked {
            b = 654604000000; a = 1544139000000;
            int256 z;
            z = 1446428 + ((-42655 * x[0]) + (1389981 * x[1]) + (-435022 * x[2]) + (2131939 * x[3]) + (-2307678 * x[4]) + (-134711 * x[5]) + (-1563002 * x[6]) + (838218 * x[7]) + (-3867643 * x[8]) + (-287527 * x[9]) + (-14871 * x[10]) + (138925 * x[11]) + (547082 * x[12]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (532461 * z); a += (237721 * z);
            z = -2846664 + ((840878 * x[0]) + (1015656 * x[1]) + (1905167 * x[2]) + (4344855 * x[3]) + (1491520 * x[4]) + (813268 * x[5]) + (140392 * x[6]) + (-166508 * x[7]) + (-344279 * x[8]) + (280778 * x[9]) + (-262185 * x[10]) + (-623571 * x[11]) + (543047 * x[12]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-1789106 * z); a += (-1524133 * z);
            z = -3039159 + ((2339559 * x[0]) + (1927192 * x[1]) + (-1149669 * x[2]) + (419394 * x[3]) + (2422033 * x[4]) + (2797237 * x[5]) + (-184718 * x[6]) + (2200018 * x[7]) + (2191446 * x[8]) + (-1193034 * x[9]) + (-27589 * x[10]) + (-1571561 * x[11]) + (-1126364 * x[12]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-79941 * z); a += (-899179 * z);
            z = -668153 + ((-1436015 * x[0]) + (-245775 * x[1]) + (519839 * x[2]) + (840096 * x[3]) + (-1067680 * x[4]) + (941901 * x[5]) + (-447013 * x[6]) + (1415013 * x[7]) + (-1647625 * x[8]) + (825277 * x[9]) + (681432 * x[10]) + (-1416949 * x[11]) + (-1754078 * x[12]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-398251 * z); a += (243723 * z);
            z = -679680 + ((1014618 * x[0]) + (-1515656 * x[1]) + (3692017 * x[2]) + (-716903 * x[3]) + (-2472535 * x[4]) + (-750627 * x[5]) + (-1234693 * x[6]) + (-1457361 * x[7]) + (437293 * x[8]) + (64478 * x[9]) + (-154363 * x[10]) + (-3496125 * x[11]) + (238174 * x[12]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-3782992 * z); a += (796095 * z);
            z = -1681270 + ((1237463 * x[0]) + (-770777 * x[1]) + (793692 * x[2]) + (-1766367 * x[3]) + (2499688 * x[4]) + (1239927 * x[5]) + (842836 * x[6]) + (-357134 * x[7]) + (-2299169 * x[8]) + (131642 * x[9]) + (337489 * x[10]) + (3914560 * x[11]) + (554438 * x[12]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-373606 * z); a += (-493254 * z);
            z = -2093270 + ((-2559287 * x[0]) + (779086 * x[1]) + (-480982 * x[2]) + (-2426775 * x[3]) + (2235989 * x[4]) + (776522 * x[5]) + (-255200 * x[6]) + (-74918 * x[7]) + (1361255 * x[8]) + (-489339 * x[9]) + (456458 * x[10]) + (1516253 * x[11]) + (-226631 * x[12]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-1339628 * z); a += (-436366 * z);
            z = -152766 + ((-3164297 * x[0]) + (-1575901 * x[1]) + (2530196 * x[2]) + (3744943 * x[3]) + (-1077146 * x[4]) + (-1736719 * x[5]) + (-508633 * x[6]) + (1762971 * x[7]) + (752575 * x[8]) + (-725826 * x[9]) + (2462294 * x[10]) + (-2054677 * x[11]) + (1028772 * x[12]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (932635 * z); a += (913103 * z);
            b /= 1000000; a /= 1000000;
        }
    }

    function _anchorBlend(uint256 mean, uint256 value, uint256 k) internal pure returns (uint256) {
        if (k == WAD) return value;
        if (value >= mean) return mean + wmul(value-mean,k);
        uint256 delta = wmul(mean-value,k);
        return delta < mean ? mean-delta : 0;
    }

    struct PosteriorInput {
        uint256 mu; uint256 v; uint256 obs; uint256 spot; uint256 preSpot;
        uint256 bid; uint256 ask; bool first; uint256 silent; bool buy; uint256 size;
    }
    function _posterior(PosteriorInput memory x) internal pure returns (uint256, uint256, uint256) {
        if (x.mu == 0) x.mu = x.spot;
        if (x.v < 10000000000) x.v = 10000000000;
        uint256 lo = wmul(x.preSpot, WAD-x.bid);
        uint256 hi = wdiv(x.preSpot, WAD-x.ask);
        if (x.first) {
            if (x.silent>1 && x.preSpot>0) {
                uint256 elapsed=x.silent>8?8:x.silent;
                x.v += 902500000000*(elapsed-1);
                (x.mu,x.v)=_band(x.mu,x.v,lo,hi);
            }
            x.v+=902500000000;
        }
        uint256 mRetail = x.mu;
        uint256 vRetail = x.v;
        // A missing own-pool trade is a censored price observation.
        if (x.first && x.preSpot > 0) {
            (mRetail, vRetail) = _band(x.mu, x.v, lo, hi);
        }
        if (!x.first) {
            // A later print is retail. Only an interior route is an observation
            // of the other pool, with explicit observation uncertainty.
            uint256 fee = x.buy ? x.bid : x.ask;
            if (fee > 30 * BPS) {
                uint256 normal = x.buy ? wdiv(wmul(x.spot, WAD-fee), WAD-30*BPS)
                    : wdiv(wmul(x.spot, WAD-30*BPS), WAD-fee);
                uint256 residual = wdiv(absDiff(normal, x.mu),x.mu);
                uint256 noise = 9000000000000 + wmul(residual,residual);
                uint256 k = wdiv(x.v,x.v+noise);
                return (_blend(x.mu,normal,k),wmul(x.v,WAD-k),0);
            }
            return (x.mu,x.v,0);
        }
        uint256 e = wdiv(absDiff(x.obs,x.mu),x.mu);
        uint256 totalV = x.v + 22500000000;
        uint256 z = wdiv(wmul(e,e),totalV);
        uint256 density = _powWad(wdiv(WAD,WAD+z/8),4);
        uint256 odds = wmul(density,wdiv(4000000000000000,_isqrt(totalV*WAD)));
        if (x.size > 3000000000000000) odds = wmul(odds,4*WAD/10);
        if (x.silent > 1) odds = wmul(odds,8*WAD/10);
        uint256 sd = _isqrt(x.v*WAD);
        uint256 width = wdiv(hi-lo,x.mu);
        uint256 distance = x.mu<lo?lo-x.mu:(x.mu>hi?x.mu-hi:0);
        uint256 zBand = wdiv(wdiv(distance,x.mu),sd);
        uint256 mass = wmul(wdiv(width,width+2*sd),wdiv(WAD,WAD+wmul(zBand,zBand)));
        if (mass < WAD/100) mass = WAD/100;
        odds = wdiv(odds,mass);
        uint256 prob = wdiv(odds,WAD+odds);
        uint256 kArb = wdiv(x.v,totalV);
        uint256 mArb = _blend(x.mu,x.obs,kArb);
        uint256 mean = _blend(mRetail,mArb,prob);
        uint256 between = wdiv(absDiff(mArb,mRetail),x.mu);
        uint256 variance = wmul(prob,wmul(x.v,WAD-kArb)) + wmul(WAD-prob,vRetail)
            + wmul(wmul(prob,WAD-prob),wmul(between,between));
        if (variance > 100000000000000) variance = 100000000000000;
        return (mean,variance,prob);
    }
    function _blend(uint256 a,uint256 b,uint256 w) internal pure returns(uint256) {
        return b>=a ? a+wmul(b-a,w) : a-wmul(a-b,w);
    }
    function _band(uint256 mu,uint256 v,uint256 lo,uint256 hi) internal pure returns(uint256,uint256) {
        // Soft interval likelihood avoids discontinuities at quadrature nodes.
        uint256 sd=wmul(mu,_isqrt(v*WAD));
        uint256[3] memory acc;
        for(uint256 j=0;j<7;j++) {
            uint256 p=j<3 ? (mu>(3-j)*sd?mu-(3-j)*sd:1) : mu+(j-3)*sd;
            uint256 w=j==3?72:(j==2||j==4?45:(j==1||j==5?10:1));
            uint256 distance=p<lo?lo-p:(p>hi?p-hi:0);
            uint256 z=sd>0?wdiv(distance,sd):0;
            uint256 likelihood=wdiv(WAD,WAD+4*wmul(z,z));
            w=wmul(w*WAD,likelihood);
            acc[0]+=w;acc[1]+=wmul(w,p);
            uint256 d=wdiv(absDiff(p,mu),mu);
            acc[2]+=wmul(w,wmul(d,d));
        }
        uint256 m=wdiv(acc[1],acc[0]);
        uint256 d=wdiv(absDiff(m,mu),mu);
        uint256 second=wdiv(acc[2],acc[0]);
        return(m,second>wmul(d,d)?second-wmul(d,d):10000000000);
    }

    function _compressTailWithSlope(uint256 fee, uint256 slope) internal pure returns (uint256) {
        if (fee <= TAIL_KNEE) return fee;
        return TAIL_KNEE + wmul(fee - TAIL_KNEE, slope);
    }

    function _powWad(uint256 factor, uint256 exp) internal pure returns (uint256 result) {
        result = WAD;
        while (exp > 0) {
            if (exp & 1 == 1) result = wmul(result, factor);
            factor = wmul(factor, factor);
            exp >>= 1;
        }
    }

    function _decayCentered(uint256 centered, uint256 decayFactor, uint256 elapsed) internal pure returns (uint256) {
        uint256 mul = _powWad(decayFactor, elapsed);
        if (centered >= WAD) { return WAD + wmul(centered - WAD, mul); }
        uint256 below = wmul(WAD - centered, mul);
        return below < WAD ? WAD - below : 0;
    }

    // Floor square root: bit-length seed and seven Newton steps (all uint256).
    function _isqrt(uint256 x) internal pure returns (uint256 r) {
        if (x == 0) return 0;
        unchecked {
            uint256 y = x;
            r = 1;
            if (y >> 128 != 0) { y >>= 128; r <<= 64; }
            if (y >> 64 != 0) { y >>= 64; r <<= 32; }
            if (y >> 32 != 0) { y >>= 32; r <<= 16; }
            if (y >> 16 != 0) { y >>= 16; r <<= 8; }
            if (y >> 8 != 0) { y >>= 8; r <<= 4; }
            if (y >> 4 != 0) { y >>= 4; r <<= 2; }
            if (y >> 2 != 0) { r <<= 1; }
            r = (r + x / r) >> 1;
            r = (r + x / r) >> 1;
            r = (r + x / r) >> 1;
            r = (r + x / r) >> 1;
            r = (r + x / r) >> 1;
            r = (r + x / r) >> 1;
            r = (r + x / r) >> 1;
            uint256 t = x / r;
            return r < t ? r : t;
        }
    }

    function getName() external pure override returns (string memory) { return "censored_10"; }
}
```

## Recommendation on a wider search

**Design: head-a's**, an output-at-zero residual net on top of T, searched with CMA-ES on the replica and decided on the real engine. It gave the largest real gain (+1.257), it was the only design still rising when stopped, and the replica predicted it well (gap 0.11). The plain constant retune (retune-b, +0.666) also works and transfers, but gains less. retune-a shows what happens with too few generations.

**Compute.** head-a used 413 generations × 16 candidates × 256 markets in 44 min on 8 processes at ~759 markets/s. Its last ~190 generations added only ~+0.11 on the monitor (1.04 at g220 to 1.15 at g410).
- My judgment, not a measured result: simply running head-a 10× longer (≈ 4,000 generations, ≈ 7 hours of wall time on 8 processes at its rate) might plausibly add a few tenths, but **will not close the ~+3 gap to the top 10 at that slope.**
- So spend the compute on the changes below and keep a 10×-run budget per change.
- Size the real-engine confirmation from head-a's figure of ~5.2 min for 512 seeds, both arms: a 4,000-seed final check like T's is roughly 40 min.

**What to change:**
1. **Warm-start and widen the parameter set jointly.** Start from head-a's weights and add T's ~79 named constants (retune-b's coordinates, with the two convex pairs tied) to the same CMA-ES. retune-b and head-a each moved the retail/arb balance in the same direction (retail up, arb down), so whether their gains add is untested and must be measured, not assumed.
2. **Treat gas as a constraint inside the search.** head-a has ~13.6k afterSwap headroom (245,000 − 231,381). head-b's 12-unit net hit OOG, and the cut-down 6-unit version still breached 245,000. head-c fit 16 units at 235,199 by its encoding. Use head-c's encoding for wider nets, or penalize a gas estimate during the search, rather than cutting units after freezing.
3. **Reduce selection noise as steps shrink.** Grow from 256 to 512–1,024 markets per generation, or use more common-random-number blocks, once monitor steps fall to ~0.05. Keep the 2,048-market monitor for selection.
4. **Use more processes.** The two slow items (retune-a at 102 markets/s on 1 CPU; head-c at 349) show that throughput limited what each item could try within ~45 min.
5. **Keep the evidence auditable** (the lesson of this revision). Final confirmation should use fresh seeds never touched before (head-b's seed reuse is to be avoided). It should run on 4,000 seeds to match T's protocol. It should save **per-seed paired deltas, retail/arb splits and the raw `gas_stats()` counters** in the delivered item record, so a write-up can carry them and a reviewer can recompute the se.

**Bottom line:** head-a's +1.257 is a real-engine improvement over T as measured by its worker; it was not reproduced here. Even taken at face value, it would not reach the top 10. A wider search is worth running only with the design changes above, not as a longer run of the same setup.
