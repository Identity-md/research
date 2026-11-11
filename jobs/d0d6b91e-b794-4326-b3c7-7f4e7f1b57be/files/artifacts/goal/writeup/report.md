# Paradigm AMM goal: final write-up (revised against the live board, 2026-11-11)

**Credit.** Every contract and figure here builds on Taylor (gtmcknight)'s solved policy, `github.com/gtmcknight/amm-sim@4812a6382311624e1506aca131ca35c378f930d9`, `research/solved`: the policy, Gaussian filter, qm tables, replica, tell research and `gates.py`. LEAN, TML, AGE and QLX5 are small network additions on top of his work; both embedded files carry his credit lines.

Units: "engine" = benedictbrady/amm-challenge@6b6921f8, each arm alone against the 30 bps VanillaStrategy, paired by seed, se = sd/sqrt(n). "replica" = Taylor's Python replica. "board" = paradigm.xyz's own 1,000 simulations. Links are at the foot; `A/` = `https://api.imd.fun/artifacts/`.

## 1. Result

**The goal is not met.** No contract of this goal reaches #1, none completed the gate chain P-Q-T-F-G-E, and this goal submitted nothing. The goal's trunk is null in goal.json: no repository was built, all code is in the content-addressed artifacts linked below.

**Best gated contract: AGE** (LEAN plus an age-weighted rival pull). Source sha256 `8cb006fa6376b0f5b2ac1c80627ce55f6b52ceef19d22a80687a87247431b135`, complete in section 9.

| AGE minus | engine gain | se | n | seeds positive |
|---|---:|---:|---:|---:|
| lb-4 (`a243bb35...`) | +0.223992 | 0.018531 | 512 | 362 |
| qt1 (`c68887cf...`) | +3.446088 | 0.045178 | 512 | 512 |
| LEAN (`a6dfc3ba...`, engine twin of TML) | +0.032246 | 0.008395 | 512 | 302 |

Fresh engine seeds 10016072..10016583, none burnt; afterSwap peak 199,567 gas; 0 out-of-gas and 0 failed callbacks in every arm; 21,507 runtime bytes; 44,616 source characters [AGE-E]. I recomputed the four differences from the artifact's raw rows and they match to nine decimals. In the same run LEAN - lb-4 is +0.191747 se 0.016892, so six sevenths of AGE's gain over lb-4 is the base's, not AGE's.

**Equal-sized alternative: QLX5** (LEAN plus a drift-tolerant split test, the gas-cheap rival tracker of lever 1). Source sha256 `e183e5bc3fb794b7067703b10a7da9920267aa5f4caa968e16ca101b02338f40`, complete in section 10. QLX5 - LEAN = +0.030494 se 0.005098 on 1,024 fresh engine seeds 10010000..10011023 (618 positive); peak 208,366; 0 OOG; 22,440 runtime bytes; 47,230 characters [QLX-A] [QLX-B]. It was never paired against lb-4 or qt1 on the engine.

AGE leads this report only because it is the one contract with a gate-E run against both required controls. Over LEAN the two are tied (difference 0.0018, far inside either se). Neither clears the requester's own bar of +0.05 over LEAN on 512+ engine seeds.

**Where that leaves the board (section 2).** The network's live entry is submission 1993d46e at 528.3333, 4th. First is 528.4520, so 0.1187 is needed. The live entry already scores +0.0308 over TML on the board, and its fingerprint matches QLX5, so one of the two measured gains is very probably already banked. What is left that was measured is at most AGE's +0.032 on top (never measured as a stack), which would not reach third place (528.3993), let alone first.

## 2. The board today, and what the live entry is

Fetched 2026-11-11T02:29Z from `GET https://www.paradigm.xyz/puzzles/api/v1/leaderboard` (no auth) [BOARD]:

| rank | submission | author / name | created (UTC) | avgEdge |
|---:|---|---|---|---:|
| 1 | fc68b4e4 | @HedgeEconomist / thecitadel.com | 2026-11-11 01:48:53 | 528.451996 |
| 2 | fb90e39e | @Ponxter / Tide v10 | 2026-11-10 00:47:33 | 528.415235 |
| 3 | 52df1e42 | @0xMai / Curvance.com | 2026-11-06 15:28:23 | 528.399264 |
| **4** | **1993d46e-e4db-43eb-9b13-3fd206d42990** | **@builtbyimd / imd.fun swarm (seat #29)** | **2026-11-10 23:03:18** | **528.333297** |
| 5 | 98a599e6 | @ultrapara / Parallax | 2026-11-10 15:35:27 | 528.291319 |
| 6 | fd732788 | @0xAron / FereAI | 2026-11-10 18:31:46 | 528.275821 |
| 7 | e9362d90 | @KaihuaQIN / MixZ11 | 2026-09-28 08:20:13 | 528.257594 |

The goal's target of 528.4152 (Tide v10) is now second: thecitadel.com, third at 528.3479 in the requester's note of 2026-11-10 17:21Z, entered 528.4520 on 2026-11-11, so the target rose by 0.0368 while this goal ran. `GET .../submissions` lists 15 @builtbyimd submissions; the last three are TML 9b220625 (TellMinLookup, 2026-11-10 14:39:46, 528.302452), lb-4 a103fe49 (seat #39, 14:46:39, 528.108759) and 1993d46e (23:03:18, 528.333297).

| gap from | to #1 528.451996 | to #2 528.415235 | to #3 528.399264 |
|---|---:|---:|---:|
| live entry 1993d46e, 528.333297 | 0.118699 | 0.081938 | 0.065967 |
| TML 9b220625, 528.302452 | 0.149544 | 0.112783 | 0.096812 |

The live entry leads fifth place by 0.041978. The earlier version of this report gave TML at 528.3025 as the entry, 528.4152 as first and 0.1127 as the gap; those were the requester's notes of 2026-11-10 and were stale on the day it shipped. They are replaced by the table above.

**Paired on the board's own 1,000 simulations** (`GET .../submissions/<id>` returns 1,000 `matches` in the same order for each submission; correlation of `submissionEdge` between any two is above 0.99999):

| difference | mean | se | positive of 1,000 |
|---|---:|---:|---:|
| 1993d46e - TML | +0.030845 | 0.005484 | 587 |
| TML - lb-4 | +0.193692 | 0.011748 | 712 |
| 1993d46e - lb-4 | +0.224538 | 0.012616 | 737 |

The board therefore confirms the engine: TML/LEAN over lb-4 is +0.19 (engine +0.1917 and +0.1637), and the live entry adds +0.031 over TML, the size of either AGE (+0.0322) or QLX5 (+0.0305) over LEAN.

**Which source is 1993d46e?** This goal's records do not say. The orchestrator spawned no submission step, goal.json and the handed results contain no mention of 1993d46e or of seat #29, and the board does not publish sources. The submission was made from the network's account 1.5 hours after the requester's note of 21:31Z, which calls QLX5 "confirmed on the engine". Edge alone cannot separate AGE from QLX5, so for this revision I ran a fingerprint: the board also publishes each run's average bid and ask fee, arbitrage and retail volume and the 30 bps baseline's edge, and the two rules move those differently. I ran LEAN, AGE and QLX5 (the exact sources embedded below) on engine seeds 0..127 with the kit at 45e7563d and the block driver's own compile and config functions [DRIVER], and compared each candidate's shift over LEAN with the live entry's shift over TML on the board. (TML and LEAN give bit-equal edges on 1,008 engine seeds [R2] [R3] and on 32 of 32 here, so LEAN stands in for TML.) z is the difference from the board in combined standard errors.

| per-run mean of | board: 1993d46e - TML (n 1,000) | QLX5 - LEAN (n 128) | z | AGE - LEAN (n 128) | z |
|---|---:|---:|---:|---:|---:|
| submission edge | +0.0308 (se 0.0055) | +0.0433 (0.0142) | +0.8 | +0.0319 (0.0131) | +0.1 |
| baseline (30 bps) edge | -0.3205 (0.0050) | -0.3326 (0.0122) | -0.9 | -0.1736 (0.0119) | +11.4 |
| arbitrage volume, Y | +50.36 (0.98) | +51.70 (2.67) | +0.5 | +37.99 (2.65) | -4.4 |
| retail volume, Y | +72.48 (1.15) | +74.13 (2.76) | +0.6 | +37.97 (2.60) | -12.1 |
| average bid fee, bps | -0.0692 (0.0022) | -0.0609 (0.0063) | +1.2 | -0.0319 (0.0063) | +5.6 |
| average ask fee, bps | -0.0674 (0.0024) | -0.0748 (0.0063) | -1.1 | -0.0499 (0.0059) | +2.7 |

QLX5 matches the live entry on all six statistics within 1.2 standard errors; AGE is 11 to 12 standard errors away on two of them. **So 1993d46e is not AGE, and it behaves like QLX5 (`e183e5bc...`).** Limits of this evidence: it is a statistical fingerprint, not an identification. The board's seeds are hidden (none of the 32 local TML edges equals any board simulation), a close variant such as QLX3 (`4345e3ea...`) would be expected to look nearly the same and was not run, the QLX5+AGE stack was not run here (its source is not among the handed results), and a contract from outside this goal is not excluded. The requester holds the file that was submitted: `sha256sum` on it settles the question against `e183e5bc...` (QLX5), `8cb006fa...` (AGE), `c25a9996...` (stack), `4345e3ea...` (QLX3). Seeds 0..127 are a diagnostic below the gate-E range: they are not gate E and took nothing from the lease ledger. Peaks there: LEAN 197,868, AGE 198,199, QLX5 207,690, 0 OOG.

**Consequences.** If 1993d46e is QLX5, then (a) it went to the board with gates Q, G and E against lb-4/qt1 never run (section 3), though the board result itself now stands in for E: +0.2245 se 0.0126 over lb-4 on 1,000 board simulations; (b) QLX5's gain is banked and must not be counted as upside again; (c) the earlier report's "retain TML as the entry" is void: the entry to retain and to measure against is 1993d46e. If the hash shows another source, AGE and QLX5 are both unbanked and each must be paired against that source before any further submission.

## 3. Gate ledger

| gate | AGE `8cb006fa...` | QLX5 `e183e5bc...` |
|---|---|---|
| P | **Not run on AGE** [AGE-S]. | Pass in both certificates: kit `gatep.py` ran Taylor's `gates.py` unmodified [CERT-A] [CERT-B]. |
| Q | **Missing.** No replica choose/report run of the production policy against lb-4's policy and qt1. | **Missing.** The QLX reference's old Q figures used full qm tables, a different fee policy from the contract, and do not carry over [CERT-A]. |
| T | Pass: replica seeds 74200..74249, 549,505 callbacks, 352,817 first trades with 0 label mismatches, 0 rule mismatches [AGE-S]. | Pass against a repaired reference: 549,802 callbacks, 0 mismatches in arb, tested, verdict, offset and lean label; 317,544 split hits [CERT-A]; second copy 0 mismatches on 549,733 and 549,802 callbacks [CERT-B]. |
| F | Pass, worst 7.48e-11 bps on 100,000 callbacks, **with a limit**: the reference tables were decoded from the contract under test by a decoder written for that item from the contract's `surf()`/`record()` code, because lookup-u1's `qpl.py` could not be fetched; its `q_u1.json` is sha256 `7068c7e5...`, not LEAN's `d5645b6d...`, which was not reproduced [AGE-S]. So F shows that filter, tell, pull and fee conversion agree given those tables; it does not show the tables are the intended U1 tables. | Pass, worst 1.80e-10 bps on 100,000 callbacks [CERT-A], 5.27e-08 on fixed inputs [CERT-B], with the same limit (tables read back from the contract; `q_u1.json` `62a0e859...`) and one more: it holds only with the contract's previous quotes fed back to the reference. A reference left on its own fees diverges on 542,700 of 549,802 callbacks [CERT-A]. |
| G | Pass on 8 engine seeds 10009056..10009063: 21,507 bytes, 44,616 characters (Python `len`, not counted on paradigm.xyz), peak 197,103, 0 OOG [AGE-S]; 199,567 on the 512 E seeds. | **No ordered G.** Sizes 22,440 / 47,230 and peak 208,366 with 0 OOG come from the ungated engine runs [QLX-A] [QLX-B]. |
| E | Done once: 512 seeds, table in section 1 [AGE-E]. Run before P and Q existed, so not "in order". | **Missing against lb-4 and qt1.** Engine data are against LEAN only. |

What mitigates the table limit: I decoded the `QPL` constant from four sources for this revision (LEAN, TML, AGE, QLX5) and it is the same 10,160 bytes in all four, sha256 `830868f9b3e5ad162c4f2070e6faed0782c7b4cc308ab69044b2cf7306f68099`. TML is the contract the previous goal gated and the board scored, so the tables are the ones already on the board; what F leaves unshown is only that an independent decoder reads them the same way.

Both certificates' items, and both AGE items, are among the results whose machines found at least one cited source not holding on re-read [R3]. Their gate counts are their own measurements; nobody has re-run them.

## 4. Each lever

| lever (goal's number) | measured in this goal | status |
|---|---|---|
| (1) rival tracking, gas-cheap form | rival64 on the new base: +0.0423 se 0.0059 replica, 198 storage words, no port [R1]. Few-point tracker: +0.048 replica, contract failed G (peak 248,120; 94,550 of 94,578 callbacks out of gas) [R1]. q-lite split test: +0.0386 se 0.0036 replica, but +0.0036 se 0.0037 on 512 engine seeds, because the engine recomputes k from rounded reserves and the exact test fires on 10% of tries against 78% on the replica [R2]. **QLX5** (tracked denominator offset, 89% hits): **+0.0305 se 0.0051 engine, n 1,024**, about +12k mean gas [QLX-A] [QLX-B]. **AGE** pull: +0.0197 se 0.0041 replica [R1], **+0.0322 se 0.0084 engine, n 512** [AGE-E]. Carrying the rival between hits: -1.39 to -1.43 [R3]. | Two small gains, each about a fifth of rival64's +0.145. Ceiling still open: the true rival spot is worth +0.105 to +0.110 over the split test on the replica [R2] [R3]; no live rule reaches it. |
| (2) recover the 0.111 of table compression | On the LEAN base the full kappa 1e-5 tables beat the U1 (QPL1) tables by +0.00254 (se 0.00701, n 768), +0.00079 (0.00606, n 1,024), +0.00239 (0.00643, n 896) and +0.00618 (0.00411, n 2,048), all replica [R1]. | Nothing left to recover on this base. See the note below on what this does and does not show. |
| (3) refit tables | Visit-weighted refit -0.0047 (se 0.0040) and -0.0023 (0.0038); ridge refit -0.0017 (0.0020) against U1, replica [R1]. The brief's rp-3 "+0.05 on the engine" was not reproduced: the supplied rp-3 item is a Python refit with no engine run [R1]. | Closed, negative. |
| (4) price between pins | Lattice filter +0.0101 se 0.0090 (n 256) at an estimated 175k+ gas; lb-4's two-component filter +0.0074 se 0.0048 (n 512); rival-pin band -137; per-run sigma/rate/size oracle +0.0049 se 0.0027; four learned fee heads between -0.0204 and +0.0058 on the 2,048-seed holdout (se 0.0044 to 0.0056) [R2]. | Closed at what was tried. The +1.19 of the true price is untouched. |
| base change (not a listed lever) | LEAN/TML over lb-4: +0.1917 se 0.0169 [AGE-E] and +0.1637 se 0.0161 [R2] on the engine, +0.1937 se 0.0117 on the board. LEAN's lean arb test cuts the peak from about 209k to about 199k gas at bit-equal edges on 1,008 seeds [R2] [R3]. | Banked since TML was submitted. |

**Lever (2), sources.** The claim that U1 already recovers most of the compression loss rests on a figure this goal did not measure: U1 minus the previous contract's lookup = +0.0971 se 0.0085 on 1,024 engine seeds. Its source is the previous goal's write-up [PRIOR] ("u1 - min-lookup = +0.0971045321712632, se 0.00847332349129484, n=1,024"), which itself says those pools were reconstructed from its root reports and that the raw files were not handed to it; the requester repeated the figure in the note of 2026-11-10 14:50Z. None of the artifacts linked here contains it. Two cautions follow. First, that comparison is U1 against the previous goal's min-lookup contract, not against lb-4's own blob; [R1] states that the brief's +0.111 and this goal's near-zero ceilings concern different encodings and baselines, that nobody ran lb-4's blob, and that the +0.111 was not reproduced. Second, the ceilings above are replica figures on choose/report windows, not engine runs. What this goal can stand behind is narrower: on the base now on the board, full tables are worth at most about +0.006 on the replica, so lever (2) has nothing left for the next contract, whatever share of lb-4's 0.111 U1 took.

Gains do not add: baselines, windows and overlapping rules differ, and the one stack built (QLX5+AGE, sha256 `c25a999646859d187f9a03655b4c7b3009a41b9cb20b4a7b56a19d612242ebc4`, 47,599 characters, 22,525 bytes, P and a 4-seed smoke only [R3]) was cancelled before any Q, T, F, G or E on the requester's instruction to do two other things only.

## 5. Distance to #1 and what is missing

- **To first: 0.118699** from the live entry (0.149544 from TML). To second 0.081938, to third 0.065967.
- **Measured and possibly still unbanked: one gain of about +0.03.** If the live entry is QLX5, that is AGE's +0.032 on top, and it is unmeasured as a stack: a split hit sets the rival estimate where AGE would otherwise pull, so the overlap may be large. Taken at full value it gives about 528.365: 0.034 short of third and 0.087 short of first. Added blindly, AGE + QLX5 over TML is +0.063, still under the 0.1187 needed; nothing in this goal's measurements reaches first, second or third.
- **Not submittable as they stand.** AGE lacks P and Q. QLX5 lacks Q, an ordered G and E against lb-4 and qt1. The stack has P only. The requester asks the user before any submission; this goal authorised none.
- **The next step that is worth its seats:** confirm the hash of 1993d46e; then run the frozen stack `c25a9996...` through Q, T, F, G and a 1,024-seed E with arms stack, QLX5, AGE, LEAN, lb-4 and qt1 from seed 10023000. Expect at most +0.03 over the live entry.
- **What would actually be needed for first:** a rule that captures a good part of the rival-spot ceiling (+0.105 to +0.110 on the replica, with no implementable form found: trackers cost 200 words or run out of gas, carry is strongly negative) or of the true-price ceiling (+1.19, where about a dozen belief ideas returned nothing). Both remain research, with no measurement that supports a promise. The target also moves: first place rose 0.037 in the last day.
- **Not done in this goal:** gate Q on any production policy; the structural search over LEAN+QLX5 constants asked for in the note of 21:31Z (goal.json counts for the last round: e07-qlx-cert 2 of 2 accepted; e07-struct-search 3 of 3 failed, none accepted; the three port stages and three engine stages behind it, 15 items, never ran); a 4,096-seed confirmation of anything; independent re-runs of AGE's or QLX5's gates.

## 6. Engine seed ledger (so that "never reused" stays true)

Source: the orchestrator's lease ledger in the goal's own notes (goal.json, episodes 1 to 7). It is not a public link, so it is reproduced here in full. The linked artifacts evidence only the ranges marked "ran"; every other range was reserved and is retired unused, which is the safe direction.

| range | lease | state |
|---|---|---|
| 10000000..10000319 | e01 gates | never run |
| 10000320..10000519 | e02 base, gas paths, lean and tracker gates | 10000320..10000383 ran [DRIVER]; the rest was leased to those items: treat as used |
| 10001000..10001079 | e03 G gates | 10001064..10001079 ran [R2] |
| 10002000..10003023 | e03-tab-eng | never run |
| 10003024..10004559 | e03-cheap-eng | 10003536..10004047 ran [R2]; rest retired |
| 10005000..10005031, 10006000..10008047 | e04 head G and E | never run |
| 10005100..10005227 | e04-split-engine | ran [R2] |
| 10009000..10009063 | e05 G gates | 10009056..10009063 ran [AGE-S] |
| 10010000..10011023 | e05-engine qlx-a, qlx-b | ran [QLX-A] [QLX-B] |
| 10011024..10012559 | e05-engine tml-a, tml-b | 768 ran; then 240 ran, 192 burnt, 336 untouched [R2] [R3] |
| 10013000..10016071 | e05 head and qlx E | never run |
| 10016072..10016583 | e05-age-eng | ran [AGE-E] |
| 10017000..10017007, 10018000..10019023 | e06 stack G and E | cancelled, never run |
| 10020000..10020023, 10021000..10022535 | e07 search G and E | stages never ran |

**Retire everything through 10022535. Next free: 10023000.** Other goals used 9.70M, 9.978M, 9.995M and 13.99M..14.01M. This revision's diagnostic used engine seeds 0..127, outside the gate-E range.

## 7. Where each kind of figure comes from

- Linked artifacts: every engine and replica figure tagged with a bracket. AGE and QLX5 rows were recomputed here from `rows_zb64`; both sources were decoded here and their hashes and sizes checked.
- The board: fetched for this revision from the two public endpoints named in section 2.
- This revision's own run: the fingerprint table in section 2 (engine seeds 0..127).
- Goal state only, not linked: the seed ledger above; six-decimal values for the learned heads (the linked [R2] gives four decimals: lin +0.0058 se 0.0046, lin-wide -0.0204 se 0.0055 after 141 generations, h4x4 -0.0009 se 0.0044, h8x4 -0.0010 se 0.0056; "100 generations" for the other three is the requester's note, not in [R2]); batch counts.
- Requester's notes: the lever-(2) history and, in the earlier version, the board snapshot.

## 8. Reading the two embedded sources

The files below are byte-exact and frozen: the sha256 is the identity that the gates, the engine and (for QLX5, probably) the board measured, so nothing in them was edited for this report. **Some of their comments are wrong and must not be trusted:**

| file, line | comment says | fact (checked by decoding the constant) |
|---|---|---|
| AGE 7, 80-81; QLX5 7, 79-80 | "qm-spline", "QMS1 blob sha256 3ac7cb88..., 10,167 B", "5 cubic tensor B-splines", "Coefficients int16 (1/8 bps) as PUSH32 immediates" | The table is `bytes constant QPL`: 10,160 bytes beginning `QPL1`, sha256 `830868f9b3e5ad162c4f2070e6faed0782c7b4cc308ab69044b2cf7306f68099` (the U1 tables). `record()`/`surf()` read int16 anchors plus int8 deltas and combine them with `lerp()`. No spline is evaluated. |
| QLX5 15, 226, 377-378 | "qlite-a ... cap24+GATE", "one candidate" | `afterSwap` (line 203) calls `TellMath.qHitX(..., m0, 5)`: the tracked-offset test over five candidates m0, m0+1, m0-1, m0+2, m0-2. |

The stale comments come from the files these were generated from. Removing them would save characters against the 50,000 limit but makes a new source hash (and, with the compiler's default metadata, new runtime bytes), so a cleaned file needs its gates re-run. Both files are ASCII, so bytes equal characters. Compile as measured: solc 0.8.24, optimizer 200 runs, viaIR, EVM paris.

To extract and check: take the lines strictly between the code fence that follows `<!-- BEGIN AGE Strategy.sol -->` and the fence that precedes `<!-- END AGE Strategy.sol -->` (same for QLX5), for example `awk '/^<!-- BEGIN AGE /{f=1;next} /^<!-- END AGE /{f=0} f && !/^```/' report.md | sha256sum`.

## 9. AGE Strategy.sol

sha256 `8cb006fa6376b0f5b2ac1c80627ce55f6b52ceef19d22a80687a87247431b135`, 44,616 bytes, 380 lines, 21,507 runtime bytes. From `code_zb64` of [AGE-S]. Policy, filter and tables: Taylor (gtmcknight).

<!-- BEGIN AGE Strategy.sol -->
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import {AMMStrategyBase} from "./AMMStrategyBase.sol";
import {TradeInfo} from "./IAMMStrategy.sol";
// Solved AMM policy by Taylor (gtmcknight), amm-sim 4812a638 research/solved: Gaussian filter + qm tables (qm_k1e-5.json),
// fee rule of real.py's qm variant (sd level, phase, synced flag). All credit for the policy, filter and tables: Taylor.
// Original tables compressed by qm-spline (cubic B-splines, QMS1 blob sha256 3ac7cb88...); filter, 3-slot state, math and fee conversion
// from trim-2 (port-3's filter); synced flag stored in bit 255 of slot 2.
// lookup-headroom: C0 (sha256 c68887cf...) with coefficient words loaded once per callback into memory and the
// second knot-span search of each axis walking forward from the first; same arithmetic, same fees.
// give-u1: lookup-u1 (Strategy.sol sha256 69c361ef...) plus one rule, the constant rival pull of GivePolicy (give.py sha256 8d871a6b...).
// lean-sol: give-u1 (Strategy.sol sha256 99d031f4...) with the exact-arithmetic isArb replaced by lb-4's LEAN TELL (bounded
// sell_one_division / buy_grid, budget 4): a first own trade is read as arbitrage iff the lean label is positive; negative, over
// budget and unsupported are misses; chance, filter, tables, pull, fee guard and storage slots unchanged (LEANBASE variant A).
// age-sol: lean-sol (Strategy.sol sha256 a6dfc3ba...) with one rule changed, the AGE pull of e03-cheap-ref/age-thr (frozen pick AGE):
// a bound that does not bind pulls ln r by 0.7*age/(age+1) instead of 0.35, age = steps since the last binding router bound, whose
// timestamp rt is kept in bits 224..252 of slot 2; bits 253..254 record what the rule did in the last callback (k: 0 read as arb,
// rule not run; 1 binding bound; 2 pull; 3 neither). Filter, tell, tables, fee guard and slots 0..5 are otherwise LEAN's.
// Credit: Taylor (gtmcknight), github.com/gtmcknight/amm-sim@4812a6382311624e1506aca131ca35c378f930d9 research/solved.
// Taylor source: https://github.com/gtmcknight/amm-sim/tree/4812a6382311624e1506aca131ca35c378f930d9/research/solved
contract Strategy is AMMStrategyBase {
    int256 constant U=1e18;
    int256 constant LN2=693147180559945309;
    uint256 constant M64=0xffffffffffffffff;
    // slots[0] = m (int128) | v (int128)<<128 ; slots[1] = sp (int128) | r (int128)<<128 ; slots[2] = fb | fa<<64 | t<<128 | cnt<<192 | rt<<224 | k<<253 | syn<<255
    function getName() external pure override returns(string memory) { unchecked {return "TellMinLookup";} }
    function mul(int256 a,int256 b) internal pure returns(int256){ unchecked {return a*b/U;} }
    function divi(int256 a,int256 b) internal pure returns(int256){ unchecked {return a*U/b;} }
    function ab(int256 x) internal pure returns(int256){ unchecked {return x<0?-x:x;} }
    function clip(int256 x,int256 a,int256 b) internal pure returns(int256){ unchecked {return x<a?a:(x>b?b:x);} }
    function ln(int256 x) internal pure returns(int256 z){ unchecked {
        require(x>0); int256 k;
        while(x< U){x*=2;k--;}
        while(x>=2*U){x/=2;k++;}
        int256 y=divi(x-U,x+U); int256 y2=mul(y,y); int256 q=y; z=y;
        for(int256 n=3;n<=29;n+=2){q=mul(q,y2);z+=q/n;}
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
        if(x<=0)return 0; uint256 n=uint256(x)*1e18;uint256 z=n;uint256 r=1;
        if(z>>128>0){z>>=128;r<<=64;} if(z>>64>0){z>>=64;r<<=32;}
        if(z>>32>0){z>>=32;r<<=16;} if(z>>16>0){z>>=16;r<<=8;}
        if(z>>8>0){z>>=8;r<<=4;} if(z>>4>0){z>>=4;r<<=2;} if(z>>2>0){r<<=1;}
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
        int256 tail=mul(mul(density,2506628274631000200),divi(n,d));return x>0?U-tail:tail;
    } }
    function trunc(int256 m,int256 v,int256 lo,int256 hi) internal pure returns(int256 Z,int256 mt,int256 vt){ unchecked {
        if(v<=0)return (lo<=m&&m<=hi?U:int256(0),m,0);
        int256 sd=root(v);int256 a=divi(lo-m,sd);int256 b=divi(hi-m,sd);
        int256 pa=pdf(a);int256 pb=pdf(b);
        Z=cdf(b,pb)-cdf(a,pa);
        if(Z<1e6)return(Z,m<lo?lo:hi,v/4);
        int256 r=divi(pa-pb,Z);
        mt=m+mul(sd,r);vt=mul(v,U+divi(mul(a,pa)-mul(b,pb),Z)-mul(r,r));if(vt<0)vt=0;
    } }
    // ---- qm-spline lookup (QMS1 blob sha256 3ac7cb88..., 10,167 B): 5 cubic tensor B-splines over (row, column, sd level),
    // ask side only; bid = point mirror. Coefficients int16 (1/8 bps) as PUSH32 immediates, 16 lanes of (c+32768) per word.
    // coefficient words of table tb (16 lanes of c+32768 each, word 0 = the table's first 16 coefficients), stored once per callback
    bytes constant QPL=hex"51504c314101a00005080004080c10141a223160ff7eff9cffb0ffc4ffceffd8ffe2ffe7ffecffeffff2fff4fff5fff6fff7fff8fff9fffafffbfffcfffdfffeffffff00000100020003000400050006000700080009000a000b000c000e001100140019001e00280032003c00500064008200a0000605fe02180b0007000055007000720078007b007c008100840089008d009000920094009500960097009c009d00a300a700aa00ab00400100010305060708090a0b0cff032b1e000307000052006b0077007c00800082008500870088008b008c008f0090009100920093009400960098009a009c009e009f00a100a200a400a500a600a700a800a900aa00ab00ac00ad00af00b200b500b900bd00ca00400100090c0f101112131415161718191a1b1c1d1e1f20222425262728292a30ff041c0d0002030700004a006900830084008500870088008a008b008d008e008f0090009200940097009c009d009e00a100a400a500a700a800a900ab00400100121315161718191a1b1c1e300003241a0003070000510073007d00870089008b008e008f009100920093009500970099009b009e009f00a100a300a500a600a700a800a900aa00ab00ac00ae00b000b200b600b800bc00bf004001000b101112131415161718191b1c1d1e20222425262728292a30ff03110a00030700005b00780088008a008b008d008f009000920095009b00a400a800ab00ad0040010012151618191a1b1e301e0c020403020101010101008305030404020202020102027203030606030303020301ff4c0303060703030302fcff7ad802030708030404000f7f019f02030808050402ff7f000f8c0203080807fefa72130d0a2d0204090d01105d0b0d0c09f401050b09164d0b120d0a0a9701070c263e0a120d0c0a09500107154413140d0d0c0a091c0108213e100e0f0c0d0d0bfe000925370c0f0e0f0f0a07e50009232d0e0f100e0b0b08dd00061f2b0d100e0e0c0a08d0000b162a0c100f0d0c0b07ca0000211a11100d0d0d0a0793000ee5290b100e0c0c0a08a000f5fb001511100c0b0b034a00eff3fa130a0f0f0b0a0c04000efcecf1140d0d0e0c0b0600ecf8e026fbf8d734120e0000000000000000000000000000000000000000000000000a0c030908030302020101017d05060a0a050404030202008103060e0d070706060504045d03060e0f070807070708d9ef02070f110809080b09d90ab902071011090a0b0ed61200a702071013080c0fe60505004d020911130e09ee0a050402180209121807f40c06060401bf010a1512fa0d08090604027a010916080b080a09060504490108110b0b0c09090703022501080f0f0d0b0a080605040c01010c130b0b0a08080604f500090d120a0b0a09080605fa00f60c0f0c0b0b09080605e100fb0d17090a0b0a0807057f00061b0d0b0b0909090806520014280f090b0a0909080c28000807fd080a0c0b0b0e002100e4fe030002060a0c060ebdff3609f503fcf5f91111d70000000000000000000000000000000000000000000000000106fe06020100010100000100010000010000ff0100000100ff010305fe02d102030102010002000101000100010001000001000001000102fffbf708ffdc0102020201000200010101010001010000000001ff0102fef605151e012d6701030102010101010101010101000000ff0000ff0200fa0b49151e02f2fb360104010201010101020101010000ffff01ff0002fa063933fcfef7010a051001040101010102020101010100ffff00ff05fdfb1168faf3050307fe0004fd000400020102010201020001ff0000ff02e70d3443f40403020101010304df00060101010102020102000000ff00fefb51140ff2070102020202010104c900080201010103010201000000ff00ff4b13010204020302010202010203bf00090200010202020201000000fffb540704040303030202020102010203a0000c0201010103020101000000024e01060404030203030102020201020495000e02ff0301030201010000fa480807060503040203020202010201020378000f030101020202020201ff3f040706060404030203030102020201020371000d0401010103020202002e0b09070606040403020303010301020201046a000c0501010102020202002e0b080706060404030204020202020201020362000d05010101020202021e0f0a080706060503030303020202020201020455001306020001020203041a0e0a07070705050402030302020202020202034f000f0a0301010102030b130b09080607050503030303020203020201020535001809070003030406090b0a08080607050504030204020202020202020521001a0d040302020608090808080706060605030402030303020203020204130014100505fe08000a09070807070606050505030203040202020501040afbff1b0f0a0108fd0cfc0b08060806070605040503020501040503040202ecb5ff4d1409000d0c0003fc080606070705050504040304090504030405057fccff2b180419fb12fb03f905070508060705050303040d0704030408115556c7ff39e4370a0ffbf904f602060507070605060406040c09061512283630f10000a668180201fe03fb00f804060507070605050707060a061626282a1cfff5ff0b1dfe04fffd03fa02f8ff0405060807050604050b070f0f242832130098ff75050403fdfe03fb02fafe0105050708050804040b050f102428311300a1ff6b000600fdff03fc00fdfbfb0a05060708050705070a0b1c1827311300cfff37020400fe02fefefe01f9000007050707060704090b091d172e2913000000f70b05f90600fa00000000000000000a07070605070c0a1c172e29120000000000000000000000000000000000000009070507080a091c172e2812000000000000000000000000000000000000000007050709090f16162e2812000000000000000000000000000000000000000000000a0a071016162e281100000000000000000000000000000000000000000000000b0d0a16152e281100000000000000000000000000000000000000000000fb070e0b141c26271200000000000000000000000000000000000000000000fbf40d12151428290e00000000000000000000000000000000000000000000000000e5201926270d0000000000000000000000000000000000000000000000000000f50c26270b010000000000000000000000000000000000000000000000000000fc05280aff000000000000000000000000000000000000000000000000000000fd04070300000000000000000000000000000000000000000000000000000000f0af8000000000000000000000000000000000000000000000000000000000000000ff0508fd040001010001010001000100010000010000010000000100010203ce02050203010100010101010101010100010001000100010002010101fd02da010304020101020001010201010301010101000100040101fdfd0907151a6701020402010201010102020203ff020002fe020101fefc051429190704fe37010303020202010002020303010201fffd0100fdf70c332103ffff02020712010302020202020002030302020103f903fefc0b2c2cf203010304030304000102030202020101010403030003ff0003022a1b02fe0404040203010304df0008010302020102010402030101090c35ff03fb04060201040203020304c9000b00050103010103030502000b12190dfe050404040301040400020304be000d00040202030002050404fff93b02070604030304020304010302030395001c000302020102030505030442e8080606050402050302020103020304820026010004030101050405051a090a08060405040304030104010203030360002c04fe0502020205060810090b0907060604030304030202030301030461002206fe030301020608090b0d09080806050404020502020302020303045b002007ff0103010206090d070c090807060505030205030203020202030457001c0701000202020709070c0b09080607050403030403020302030203044b00220702ff010302060a060b0b09070706050404030403020302020204043e00290801010002030505090b0a09080606050404030403020402020203052d00260e04000300030405080909080707060504040304030302030302030518002d0b04030102020505070808080707050604040304040203030302030608002a0e0404ff04000505070809080607060504040305040304020401040bf4ff2e0d0701040003010507070809070607040704040504040402050206fb98ff7b0c060006fd05ff07060707090807060705050409050405050606097fc2ff460f06fe05fe07030207060807080905070405050908050a050a075751d9ff1a140204ff0cfc05ff07070608080807050804050708070c0e222a52f5e7ffd23112080109fe07fc07070608070808050705040906080b0c2f3832fdeeff08fffdfb150008fd06f906060707070807050507070704130f352a36f1dcff0c11020804fefffe01fe010807060708060607040909060e11302e2ff8e1ff1bfb0b0002ff00fe0101de091f060608070605050907080c172c2d2afef0ff0eff05fffb06ff02fbff030000070607070605050909090f112a3524fd0000fa05fd04feff0300000000000000000b070606050b06090f14283327f9000000000000000000000000000000000000090606060908080f142b2f22ff0000000000000000000000000000000000000008050509080b1017282b22fe0000000000000000000000000000000000000000000a090a081017272e20fc000000000000000000000000000000000000000000000d07090f17272d1ffe000000000000000000000000000000000000000000fa080b0c0f14292720fd00000000000000000000000000000000000000000000f10f081116252b1700000000000000000000000000000000000000000000000000f011142728140000000000000000000000000000000000000000000000000000fefa28271202000000000000000000000000000000000000000000000000000000fc2612fd00000000000000000000000000000000000000000000000000000000fe090500000000000000000000000000000000000000000000000000000000ffac8000000000000000000000000000000000000000000000000000000000000000d105fb1b070302030202020202010101010101000101010101010201010204b202fd0e0b0303030302030302020202010102010001020201010102010406cf0102fe0f020304030403030303030202030102020102010203040100ff01600109f70f030404040404030404030504010203fe00020402fff7fe02050a35010af70b0404040504040404060505020001fd010902f4fa010705030407150107f908040405040504050506070a0108fe16fcdaf70805050204020508040107fa06050404060404050509060c060ff1f7e2050c0005030304030508e5000dfc020504050604050508030ffeffec04fd0c01000502040204030508c9001901fb0603050506040505060402f7ff070402ff020304030405010509c1001903f806040406050406050a07eb0a0302000401030103050501030508a0002006f8030305060505050e0bda180004050103040102040501040305099b001f02fb010405050505060af405050403050204010503030302030405097f001d0b00fa0204050505040101020504070505020405020105060301050a6f00240dfefd0004050405040200040306070505020502040107030303060a6a00210a00ffff03050504020300040705060604050404030404010403060b65001c0c02ff000004040505ff01040806050704040406040204010504060b6400131100ffff01030404050003040409050605040406040403010604060b59001c09fd04ff0201040505ff05020508070604050406050105050701070b3f0030040101fffe020202020700050707070506050407050404050603080d3000290d0400fffffb05020204030408070607050505080605060505050a0f1f002e09fe02ff0304fa030304060607070607050605080606060608080a130f002b0a0301fffffffb070305050907070d010905030d060608070a080f1e0300270b01010003fe08f5030608050906070bfd0d05060d0b0b070c0e1718eaff3a080304ff06f8fefc0505070609050a070b02030e020c09130e0ffc50e0ff3405080afff105fd08f90407090609070600050d0b060b0103120b4540d2ff3c18fbfdfdfafd0111f0050608070905070a000e010d08091200193c39a8ff5afdf617e00ffaf80618fd050808080a030a08fb130c0b0003fc2e3f3b0000fd0503f2fc02ff07fc07ff08070907080805010617fd090d06fd274435000000f700fb0702fd06fdfd12fdfd0807080404070515030513f90528462e000000f207ff08f302f7140000000002090704040f06090112ff061510512a0000fefe040000000000000000000000000a08070506020c10020c0c24461c000000000000000000000000000000000000090606ff150a07000f17134f1500000000000000000000000000000000000000040405110cff11f81e1e461a000000000000000000000000000000000000000013f90c010613fb1d223f190000000000000000000000000000000000000000000009140707f91e23421100000000000000000000000000000000000000000000fd15ff160513253d0d00000000000000000000000000000000000000000000db171a04052b193a04000000000000000000000000000000000000000000000000e5111a0a2b32020000000000000000000000000000000000000000000000000000f311292eff000000000000000000000000000000000000000000000000000000e82b1c0400000000000000000000000000000000000000000000000000000000e52af9000000000000000000000000000000000000000000000000000000000080bf0000000000000000000000000000000000000000000000000000000000000009060001010000010000010000002903000101010000010001000100f801000002010002000100010000fd00000202020000ffff00ff01fff5000001030100ff00ff00f0630eeb00000203000000ff00020067eed80001010301ff0000fff84f18ffcf0000020300000001e766070900bd0000020201ff00f44518050900b4000002020000fe1933070609ffa20000020300fff25aff07050900990000020301fa40080707060800900000020400f8420907060608008700010204f9360a09070705080078000102031a150a0807060608ff6e0000020b170c090706060608ff5b000104100a090808060606080038000105100705050606060509003100010df71107060707050609003d0003fb07fc07050806060608003100fefbfefc06050607070708ff19000402fbf8fe05050607060d001400fe04fbfcfe02060407080d000b0000fffd02f6f40d0705090bff070000f9000000000000000b0d000000000000000000000000010fff0000000000000000000000ec1200000000000000000000000000ee1008060001010001000100010000002703010101010101000100010000f701000202ff0103010000000102fd00010303010200ff00ff0000fff5000102040002ff0000fffa5508ec000103020102ff00fff3560a03d90001040200020000ff36180603d000010401010300f83c10070704be00010401010400231809070704b500010302020306330507060803a4000004030305230d0a080507039b000105020412180b080806070392000203030715130b08070607038a000105010c180d0a08070507037b0002fb120f0e0b090806060703700002040a0b0c0a090707050703600001010c0909080807060606033d00fd03090707080807050607043300ff0306090707080707050901210010fe060607070808060509012200f801000507070608080608071100f908fff9040606060709080608000afb00fbff050605070809060a00fe00f901ec060c0706070b050200fe00000000000000000b0b040000000000000000000000000e070000000000000000000000f50705000000000000000000000000804c0d06fd02010100010100000001002c03fe0202010101000101000100f90100030201020101010100ff06fe00030505030402ffffffffff06f60003050604040102fb270a09efed0003050704040203150d0909f8db000305070505030e0e0a0808fdd1000406070504070e0c0a0709fdc00003060805060a0d0b090708ffb70003060807060c0c0a080609ffa60003060a06080c0b09080608029e0002070908080b0c0808060801950004050a080a0b090a060608028d0003060a080a0b0a08070608027e0003040c090a090a070706070472000305030c0a0a090806060704610003000b0708070807060607043b00020205070708090706060809300009fd0507070808080706080926000bfe04060708080807050908110007010006060708070807080bfaff070701fc070607070708090addff28e41c01e81c060707070a0aa9ff2de03dfff10e0f0607060b0a00000000000000000000e9220b090000000000000000000000010c0b0000000000000000000000f7fc170000000000000000000000008080d7051b0603020101000100000100000319080402020101010102ff01df01120b05030202020100fb07030401040b0804030405050a1beee00001010b070404050505f0f6f91bf900000a0804040503fdfbfcf615ea00fe0a0804040401fffa02fb0be300fd090804050301fffc01fc09d400fc080804040301fd0003ff04cd00fb070805030301fc0205fe04bf00fa0508040402000101040200b800fa0408040302ff0105030200b200f80308040402ff0106040101ab00f90108040304fe01050601019e00f9fe070403010006040503018d00fcfb090304fd0305070403047900f903fe0602020206050408075800fdf5ff0304050808060804045300f102fe0103040708060708034c00f0fcfc0703080408040807093800e509fff70607080608070b031b00fbe6ff13fb05080707020b112300cf25dbfd25f2060906070e06050009fb0400fdfdf80505070c110000000000000000000008010b1300000000000000000000000011100000000000000000000000ea1d0000000000000000000000000080800103ff0300000000000100000000000000000000000100000000006e0100020000010000000000010000000100000000000000000101c700010101000001000001000000000000ff01000100ff0000fffc97000101010001000001000000ff00000001fefeff01ff040210216700020100010001000000000000000101fb080a0efb1f0b08fef25c00030101010001000000000001fc00fd2a17f90400fe01ff0003530003010101000100000000fffc111d0706fd0200000200010100420007000101010000000000fc2d0bfe00010201000101000100013d00070101010001000000ff0a28fc03020201000101000100010135000701010001000100000127010402020201010001000100010131000801010001000000001f04070203010201010101000100010128000e010100000000fd1c050407030202020101000101000100011e00100400010101020b0705040603020202010101000101000101100016040001030405050504040603020202010101000101000101090015040101020505040503040603020202010101010100010101faff1c050102010306040304040603020202010100010101010102e4ff260405fe070201040303040603020202020203010201000201eaff1b07020bfe04fc0403030307020302030601020200ff00011f6eff7f230203fe02fc0103030307020303050303030307100a222adfff2f05fefe04fc02fa01030208030304030403010907231e0bf902000702ffff02fd01fdff010306040403050302050514131d0afffcff0b01ff02fffe0000fdfd0505040403050304040513141c0bfecaff3b00ff02ffffff00fd000006040304050206030414141b0bfef6ff0dfd0003fd03fd0000000000060304040503030d0b1b140bfe0000000000000000000000000000000503060403030d0b1a1509ff0000000000000000000000000000000004060403060a0b191509ff000000000000000000000000000000000006030506090b19140aff00000000000000000000000000000000ff01070305091014140aff0000000000000000000000000000000000fa0207060b0c121509ff000000000000000000000000000000000000fd00040a0b151407000000000000000000000000000000000000000000fe050c12140700000000000000000000000000000000000000000000f704141306000000000000000000000000000000000000000000000000061305000000000000000000000000000000000000000000000000ef170400000000000000000000000000000000000000000000000000f40700000000000000000000000000000000000000000000000000000000ff0204ff01010000000100000000000100000000000000000100006c0102020100000100000100000100000001000000000001000002c6000202010001000100010100000001ff0001000100000100ffff97000102010101000101010001fd000002fffffdfb02010303081c67000301010201010101ff0100feff00fc05030d1505020a0305fb5e00030102010101010200fffeff05ff1715fe06fffe01ff0001035500030102010101010100fd0512120002020101010201010001024400070102010102000202060b15fa0302030201000100010101023d000a00020102020102030610050303020301010002000101010231000e010101020202010416fb09030202030201000101010101012c00100101010102020409050508020302030200010101010101012c000d01000102020307030605080203020301010101000200010220001303ff010102030405050507030202030201000200010101011400170301000202030305040407030302030101010101010100020f001403010101020303050404070302020302010101010101010106001504ff02010202040404050703020203020201010002000102f3ff1c03020002ff04030404040803040204040101020102010203f2ff190203fd03000404030404090203040502020302020300fb1cf0ff110301030003000403040408040303040303010305060b31220100e6140402fe050101040304070503020602040203020c1d2c05f2ff0c04fffe03fe02fb0404030704040305030303020412152a06faff06010001fffd0300ee0411070403030504020306010f1c2604efff12ffff020000fe00010000070304030505010305050f142c01e4ff180401fa05fb05000000fff90e0303060402040405141525000000000000000000000000000000000504050304040308121e19010000000000000000000000000000000004050403040408121c190200000000000000000000000000000000000505030306061418190200000000000000000000000000000000ff010604030508111a19ff00000000000000000000000000000000fffeff070407081215140100000000000000000000000000000000000000fd020908131510fe000000000000000000000000000000000000000000ff0815130eff000000000000000000000000000000000000000000fbfe11120dff000000000000000000000000000000000000000000000000140a000000000000000000000000000000000000000000000000fe030900000000000000000000000000000000000000000000000000fefd00000000000000000000000000000000000000000000000000000000e602050dff010101010001000100000100000100000001000100025c01020b0002010101010101010100000100010001000100010002c300000602020102020102010102010001000001000100010101039900010104020202010301020202ffff000101010200000100fffe690008ff030203030202020302030100fd00fe01fb0101010101065c000eff02020301030204030206ff01f9f9fb080102020102020353000eff030202020204040605f6fc03ff02fd0301010201010203440012ff0102030301020402fc010401ff010002010102010102033e0015ff0003020301020202fc060101010200000201010101020438001101ff020303030203f5080403010202fe03000203ff01020436000f01000103020302fc0302040302000400000102010201020332000e03ff01020302fd03020205020301030001010102010202032d000fff000100010201020202050303020303ff0003010201020426000f0201ff0001010000030305040203030301010201020103041d001103fd01fe0301010202020603030305030102010202010305140013fe03ff03fb030102030407050302040402010301030203050d000c0302fd0003fc02020403070306010703040303030303060a0a000b020008fb04f801030303090503000406040005040305080802000c05ff03fdfc01ff0204040801010806040204050103ff011cf1ff1dfcfd01fc0005fe01020508040405000703040402feff0b26e8ff1afbff00fdfdf81af6040407050203070801030603f7001427fbff010100ff0204fcff09fefe080401030c0104020306fbff1427f9ff020104fb01fb09000000fd0903050405ff07070102000016230000fd00fa09000000000000fd0601050402050cfe0401f90d12230000000000000000000000000000000501040a04fd0703fb0a191d0000000000000000000000000000000002080604000305f70c1c1b0000000000000000000000000000000000070103030800fd051f2300000000000000000000000000000000fe020a010203030707161e0000000000000000000000000000000000f0100404000404092213000000000000000000000000000000000000fffd05fb0a080821120000000000000000000000000000000000000000fff01301111d0f00000000000000000000000000000000000000000000cb29141b070000000000000000000000000000000000000000000000ec151a04000000000000000000000000000000000000000000000000f9100100000000000000000000000000000000000000000000000000fb0000000000000000000000000000000000000000000000000000000005060101ff0100000000017d020101010100010001fe63010102010100ff00ffffcb00010300ff00ff01fffeb9000103000000fff52516b000010300fffffafc72039e0001030000f805600bfa8c00010300fefa520d0c028400010303f45108070d0075000101f7371b07070b006700ff061629fb08070bff3700031e04070d06040dfe2800e3ff030b04040c10fe03000cfc04da0f080019ffe4fffa09fa1f0000e916fc000000000000000000ed0e00000000000000000000000906fd03000100010000008002fe040002010100010065010105020101feff0003ce000309fb02ff00ff0102bd000306fc05fd02090a12b4000308fa0207f54016e9a2000403ff041530000a009100040300093500070ffe89000403e952fb08070e007b00000017220108070e026c000210060d0b07070d033e0003070a100908070e05f6ff0506010f080709100b0300fdfbea0a090605130bf9fff30d07000000e7180b0000000000000000fa07f600000000000000008cbe80d1051b08000101000000005902170e000301000102005a010d130006020201fffedd00001306090302fefefbd000fd140509060531bb04c800fd12070a0513e5e711bb00fb12050b03e40dfb07ad00fa100609f30404fb05a600fa0e0ff106fe0600029900f90c00010401060201810000ff0706fc060607025d00fafe01090604070b061b00f4f708ff0a09051502fffff30f02fcfe0203180afeff02fdfe050000d0390a0000000000000000ef0d05000000000000000080807f";
    struct QT {uint256 lk;uint256 r0;uint256 r1;uint256 r2;uint256 ck;uint256 nl;uint256 nr;uint256 nc;uint256 off;int256 scale;}
    function qt(uint256 tb) internal pure returns(QT memory t) {
if(tb==0) t=QT(0x70000,0x960095009400920090008d008900840081007c007b00780072007000550000,0x14000ab00aa00a700a3009d009c0097,0x0,0xc0b0a0908070605030100,2,24,11,540,250000000000000000);
else if(tb==1) t=QT(0x700030000,0x9200910090008f008c008b00880087008500820080007c0077006b00520000,0xa900a800a700a600a500a400a200a1009f009e009c009a0098009600940093,0x14000ca00bd00b900b500b200af00ad00ac00ab00aa,0x302a29282726252422201f1e1d1c1b1a191817161514131211100f0c0900,3,43,30,1116,500000000000000000);
else if(tb==2) t=QT(0x7000300020000,0x9400920090008f008e008d008b008a008800870085008400830069004a0000,0x14000ab00a900a800a700a500a400a1009e009d009c0097,0x0,0x301e1c1b1a1918171615131200,4,28,13,5115,500000000000000000);
else if(tb==3) t=QT(0x700030000,0x9b009900970095009300920091008f008e008b00890087007d007300510000,0xb600b200b000ae00ac00ab00aa00a900a800a700a600a500a300a1009f009e,0x14000bf00bc00b8,0x302a29282726252422201e1d1c1b191817161514131211100b00,3,36,26,6683,1000000000000000000);
else if(tb==4) t=QT(0x700030000,0xad00ab00a800a4009b009500920090008f008d008b008a00880078005b0000,0x140,0x0,0x301e1b1a191816151200,3,17,10,9599,500000000000000000);
    }
    function rk(QT memory t,uint256 i) internal pure returns(uint256){unchecked{return ((i<16?t.r0:(i<32?t.r1:t.r2))>>(16*(i%16)))&65535;}}
    function spanR(QT memory t,uint256 x) internal pure returns(uint256 a){unchecked{
        uint256 hi=t.nr-1;while(hi-a>1){uint256 m=(a+hi)/2;if(rk(t,m)<=x)a=m;else hi=m;}
    }}
    function spanC(QT memory t,uint256 x) internal pure returns(uint256 a){unchecked{
        uint256 hi=t.nc-1;while(hi-a>1){uint256 m=(a+hi)/2;if(((t.ck>>(8*m))&255)<=x)a=m;else hi=m;}
    }}
    function record(bytes memory b,QT memory t,uint256 l,uint256 r,uint256 c) internal pure returns(int256 v,int256 vn){unchecked{
        uint256 o=t.off+(l*t.nr+r)*(t.nc+1);
        v=int256(int16(uint16(uint8(b[o]))|(uint16(uint8(b[o+1]))<<8)));
        for(uint256 n=0;n<c;n++)v+=int256(int8(uint8(b[o+2+n])));
        vn=v+int256(int8(uint8(b[o+2+c])));v*=t.scale;vn*=t.scale;
    }}
    function lerp(int256 a,int256 b,int256 f) internal pure returns(int256){unchecked{return a+mul(b-a,f);}}
    function surf(QT memory t,bytes memory b,int256 pw,int256 p2,uint256 k,int256 tt,uint256 jm) internal pure returns(int256){unchecked{
        uint256 i=uint256(pw/U);if(i>319)i=319;int256 f=pw-int256(i)*U;
        uint256 j=uint256(p2/U);if(j>jm)j=jm;int256 g=p2-int256(j)*U;
        uint256 a;while(a<t.nl-2&&((t.lk>>(16*(a+1)))&65535)<=k)a++;
        uint256 r=spanR(t,i);uint256 c=spanC(t,j);
        int256[8] memory v;
        for(uint256 l=0;l<2;l++)for(uint256 row=0;row<2;row++)(v[l*4+row*2],v[l*4+row*2+1])=record(b,t,a+l,r+row,c);
        int256[2] memory lr;lr[0]=int256((t.lk>>(16*a))&65535);lr[1]=int256((t.lk>>(16*(a+1)))&65535);
        int256 rlo=int256(rk(t,r));int256 rd=int256(rk(t,r+1))-rlo;
        int256 clo=int256((t.ck>>(8*c))&255);int256 cd=int256((t.ck>>(8*(c+1)))&255)-clo;
        int256[2] memory levels;
        for(uint256 l=0;l<2;l++){
            int256 u=(int256(k+l)-lr[0])*U/(lr[1]-lr[0]);int256[4] memory q;
            for(uint256 z=0;z<4;z++)q[z]=lerp(v[z],v[z+4],u);
            int256[4] memory nodes;
            for(uint256 row=0;row<2;row++){
                int256 rf=(int256(i+row)-rlo)*U/rd;
                int256 x0=lerp(q[0],q[2],rf);int256 x1=lerp(q[1],q[3],rf);
                for(uint256 col=0;col<2;col++){
                    int256 cf=(int256(j+col)-clo)*U/cd;
                    int256 n=lerp(x0,x1,cf);nodes[row*2+col]=n>0?n:int256(0);
                }
            }
            levels[l]=lerp(lerp(nodes[0],nodes[2],f),lerp(nodes[1],nodes[3],f),g);
        }
        return lerp(levels[0],levels[1],tt);
    }}
    function w2l(uint256 L) internal pure returns(int256){ unchecked {
        uint256 K=L<16?0x7ff77ff67ff57ff47ff27fef7fec7fe77fe27fd87fce7fc47fb07f9c7f7e7f60:(L<32?0x800780068005800480038002800180007fff7ffe7ffd7ffc7ffb7ffa7ff97ff8:(L<48?0x808280648050803c80328028801e801980148011800e800c800b800a80098008:0x00000000000000000000000000000000000000000000000000000000000080a0));
        return int256((K>>(16*(L&15)))&0xffff)-32768;
    } }
    // real.py/evalpol _pos2 over pol_mid's W2L (grid units of 5 bps), WAD in and out
    function pos2(int256 v) internal pure returns(int256){ unchecked {
        if(v<=-160*U)return 0; if(v>=160*U)return 48*U;
        uint256 lo=0;uint256 hi=48;
        while(hi-lo>1){uint256 md=(lo+hi)>>1;if(w2l(md)*U<=v)lo=md;else hi=md;}
        int256 a=w2l(lo);return int256(lo)*U+(v-a*U)/(w2l(hi)-a);
    } }
    function sdl(uint256 k) internal pure returns(int256){ unchecked { return int256((0x221a14100c080400>>(8*k))&0xff); } }
    // qm fee rule: w, w2 offsets (WAD bps), phase, synced flag, belief variance v (WAD, ln-price^2)
    function fees(int256 w,int256 w2,uint256 ph,bool syn,int256 v) internal pure returns(int256 fb,int256 fa){ unchecked {
        int256 sd=root(v)*10000;uint256 k;
        while(k<6&&sd>=sdl(k+1)*U)k++;
        int256 tt=clip((sd-sdl(k)*U)/(sdl(k+1)-sdl(k)),0,U);
        int256 pw=clip(w/5+160*U,0,320*U);int256 wq=(pw-160*U)*5;
        uint256 tb;int256 p2;int256 nc1;
        if(ph==0){tb=0;p2=clip(w2/5,-6*U,6*U)+6*U;nc1=12;}
        else{tb=(ph==1?1:3)+(syn?0:1);p2=pos2(w2/5);nc1=48;}
        QT memory t=qt(tb);bytes memory b=QPL;
        int256 xa=surf(t,b,pw,p2,k,tt,uint256(nc1)-1)+wq-w;
        int256 xb=surf(t,b,320*U-pw,nc1*U-p2,k,tt,uint256(nc1)-1)+w-wq;
        fb=xb>0?U-exp(-xb/10000):int256(0);fa=xa>0?U-exp(-xa/10000):int256(0);
        fb=clip(fb,0,U/10);fa=clip(fa,0,U/10);
    } }
    function afterInitialize(uint256 x,uint256 y) external override returns(uint256,uint256){ unchecked {
        int256 sp=int256(y*1e18/x);
        slots[0]=uint256(uint128(int128(ln(sp))));
        slots[1]=uint256(uint128(int128(sp)))*(1+(uint256(1)<<128));
        slots[3]=x;slots[4]=y;slots[5]=0;
        slots[2]=2823606104386589*(1+(uint256(1)<<64));
        return(2823606104386589,2823606104386589);
    } }
    // filter update over a gap of dt steps; returns new m, v, rival spot r and the arb flag
    function update(int256 m,int256 v,int256 fb,int256 fa,int256 sp,int256 r,int256 s,bool buy,uint256 dt,bool hit,int256 chance) internal pure returns(int256,int256,int256,bool arb){ unchecked {
        int256 lo=ln(mul(sp,U-fb));int256 hi=ln(divi(sp,U-fa));
        uint256 n=dt-1;if(n>12)n=12;
        for(uint256 i=0;i<n;i++){v+=893025000000;(,m,v)=trunc(m,v,lo,hi);}
        v+=893025000000;
        int256 lp=ln(buy?mul(s,U-fb):divi(s,U-fa));
        int256 sd=root(v);int256 la=divi(pdf(divi(lp-m,sd)),sd);
        (int256 Z,int256 mt,int256 vt)=trunc(m,v,lo,hi);
        int256 d=ab(ln(divi(s,sp)));if(d<1e9)d=1e9;
        int256 pi=pdf(divi(ln(d)+6801595083153746944,1176000000000000000));
        int256 lr=divi(mul(mul(Z,260000000000000000),pi),mul(d,1176000000000000000));
        lr=mul(lr,chance);
        pi=hit&&la+lr>0?divi(la,la+lr):int256(0);arb=pi>U/2;
        if(pi>5e15&&pi<995e15){
            m=mul(pi,lp)+mul(U-pi,mt);
            v=mul(pi,mul(lp-m,lp-m))+mul(U-pi,vt+mul(mt-m,mt-m));
        }else if(arb){m=lp;v=0;}else{m=mt;v=vt;}
        int256 pe=exp(m);r=clip(r,mul(pe,997e15),divi(pe,997e15));
        return(m,v,r,arb);
    } }
    // AGE pull weight (WAD): 0.7*age/(age+1), age = steps since the last binding router bound; 0 on the step of a binding bound
    function pullW(uint256 age) public pure returns(int256){ unchecked {return int256(7e17*age/(age+1));} }
    function afterSwap(TradeInfo calldata t) external override returns(uint256,uint256){ unchecked {
        uint256 s0=slots[0];uint256 s1=slots[1];uint256 s2=slots[2];
        int256 m=int256(int128(uint128(s0)));int256 v=int256(int128(uint128(s0>>128)));
        int256 sp=int256(int128(uint128(s1)));int256 r=int256(int128(uint128(s1>>128)));
        int256 fb=int256(s2&M64);int256 fa=int256(s2>>64&M64);uint256 cnt=s2>>192&0xffffffff;bool syn=s2>>255==1;
        uint256 rt=s2>>224&0x1fffffff;uint256 k;
        int256 s=int256(t.reserveY*1e18/t.reserveX);bool arb;
        if(t.timestamp>(s2>>128&M64)){
            bool hit=TellMath.ltTell(slots[3],slots[4],uint256(t.isBuy?fb:fa),t.amountX,t.amountY,t.reserveY,t.isBuy)==1;
            int256 chance=hit?int256(TellMath.ulpOverGridWad(t.isBuy?t.amountX:t.amountY,t.isBuy?slots[3]:slots[4],t.isBuy?t.reserveX:t.reserveY)):int256(0);
            (m,v,r,arb)=update(m,v,fb,fa,sp,r,s,t.isBuy,t.timestamp-(s2>>128&M64),hit,chance);cnt=0;syn=false;
        }
        slots[3]=t.reserveX;slots[4]=t.reserveY;
        uint256 ph;
        if(!arb){
            int256 c=t.isBuy?divi(mul(s,U-fb),997e15):divi(mul(s,997e15),U-fa);
            // binding router bound: r = c and its timestamp rt is kept (age 0)
            if(t.isBuy?c<r:c>r){r=c;syn=true;rt=t.timestamp&0x1fffffff;k=1;}
            // AGE: bound did not bind -> pull ln r alpha of the way to ln c, alpha = 0.7*age/(age+1), age = t - rt (LEAN: alpha 0.35)
            else if(c!=r){int256 al=pullW(t.timestamp-rt);if(al>0){int256 lr=ln(r);r=exp(lr+mul(al,ln(c)-lr));}syn=true;k=2;}
            else k=3;
            cnt++;ph=cnt==1?1:2;
        }
        int256 w=(ln(s)-m)*10000;int256 rr=(ln(r)-m)*10000;
        (fb,fa)=fees(w,rr,ph,syn,v);
        fb=guardFee(fb);fa=guardFee(fa);
        slots[0]=uint256(uint128(int128(m)))|uint256(uint128(int128(v)))<<128;
        slots[1]=uint256(uint128(int128(s)))|uint256(uint128(int128(r)))<<128;
        slots[2]=uint256(fb)|uint256(fa)<<64|t.timestamp<<128|cnt<<192|rt<<224|k<<253|(syn?uint256(1)<<255:0);
        return(uint256(fb),uint256(fa));
    } }

    // Complete integer preimage of Vanilla gamma under IEEE binary64 conversion.
    // Closest integer outside that interval; ties select the lower fee.
    function guardFee(int256 f) internal returns(int256) {
        if(f>=2999999999999948&&f<=3000000000000057){slots[5]++;return f-2999999999999947<=3000000000000058-f?int256(2999999999999947):int256(3000000000000058);}return f;
    }
    function guardShifts() external view returns(uint256) {return slots[5];}
    // lean label of a trade: 0 unsupported, 1 positive, 2 negative, 3 over budget; isArb = (label == 1). x (reserveX) is not used.
    function leanLabel(bool b,uint256 ax,uint256 ay,uint256,uint256 y,uint256 px,uint256 py,uint256 fb,uint256 fa) public pure returns(uint256) {return TellMath.ltTell(px,py,b?fb:fa,ax,ay,y,b);}
    function isArb(bool b,uint256 ax,uint256 ay,uint256 x,uint256 y,uint256 px,uint256 py,uint256 fb,uint256 fa) external pure returns(bool) {return leanLabel(b,ax,ay,x,y,px,py,fb,fa)==1;}
}
library TellMath {
    uint256 internal constant WAD = 1e18;
    uint256 internal constant TWO53 = 1 << 53;
    uint256 internal constant TWO52 = 1 << 52;
    uint256 internal constant LIM = 1 << 128;

    /// floor(log2(x)) + 1, 0 for x = 0, by binary normalization.
    function bitLen(uint256 x) internal pure returns (uint256 n) {
        unchecked {
            if (x >= 1 << 128) { x >>= 128; n += 128; }
            if (x >= 1 << 64) { x >>= 64; n += 64; }
            if (x >= 1 << 32) { x >>= 32; n += 32; }
            if (x >= 1 << 16) { x >>= 16; n += 16; }
            if (x >= 1 << 8) { x >>= 8; n += 8; }
            if (x >= 1 << 4) { x >>= 4; n += 4; }
            if (x >= 1 << 2) { x >>= 2; n += 2; }
            if (x >= 1 << 1) { x >>= 1; n += 1; }
            if (x != 0) n += 1;
        }
    }

    /// num/den (both > 0) rounded to nearest-even double m*2^e, 2^52 <= m < 2^53.
    /// One division: the bit-length estimate is off by at most one binade, fixed by a shift.
    function rn(uint256 num, uint256 den) internal pure returns (uint256 q, int256 e) {
        e = int256(bitLen(num)) - int256(bitLen(den)) - 53;
        uint256 sn; uint256 sd;
        if (e < 0) { sn = num << uint256(-e); sd = den; } else { sn = num; sd = den << uint256(e); }
        q = sn / sd;
        // estimate gives q in [2^52, 2^54): at most one step down in precision
        if (q >= TWO53) {
            e += 1;
            if (e <= 0) { sn = num << uint256(-e); } else { sn = num; sd = den << uint256(e); }
            q = sn / sd;
        }
        uint256 r = sn - q * sd;
        uint256 twice = 2 * r;
        if (twice > sd || (twice == sd && (q & 1) == 1)) {
            q += 1;
            if (q == TWO53) { q = TWO52; e += 1; }
        }
    }

    /// e with 2^e * 1e18 <= w < 2^(e+1) * 1e18 (w > 0).
    function binade(uint256 w) internal pure returns (int256 e) {
        e = int256(bitLen(w)) - 60; // bitLen(1e18) = 60
        if (!_atLeast(w, e)) e -= 1;
        else if (_atLeast(w, e + 1)) e += 1;
    }

    function _atLeast(uint256 w, int256 e) private pure returns (bool) {
        return e >= 0 ? (WAD << uint256(e)) <= w : WAD <= (w << uint256(-e));
    }

    function _min(int256 a, int256 b) private pure returns (int256) { return a < b ? a : b; }

    /// log2 of the grid: min(binade(before), binade(after)) - 52.
    function gridExp(uint256 beforeW, uint256 afterW) internal pure returns (int256) {
        return _min(binade(beforeW), binade(afterW)) - 52;
    }

    /// min(1, ulp(paid)/grid) scaled by 1e18, paid = fl(paidW/1e18) (the double behind paidW).
    /// Returns 0 for out-of-bounds inputs. 1e18 means the paid amount is no finer than the grid.
    function ulpOverGridWad(uint256 paidW, uint256 beforeW, uint256 afterW) internal pure returns (uint256) {
        if (paidW == 0 || paidW >= LIM || beforeW == 0 || beforeW >= LIM || afterW == 0 || afterW >= LIM) return 0;
        (, int256 pe) = rn(paidW, WAD);
        int256 d = gridExp(beforeW, afterW) - pe;
        if (d <= 0) return WAD;
        if (d > 64) return 0;
        return WAD >> uint256(d);
    }

    // ---- LEAN TELL of result lb-4 (scratch/LeanTell.sol, functions verbatim): buy-grid's bounded sell_one_division / buy_grid tests,
    // budget 4, in exact integer binary64 (round-to-nearest-even) arithmetic. A double is m*2^e with 2^52 <= m <= 2^53; 1e18 = LT_C*2^7.
    // ltTell returns 0 unsupported, 1 positive, 2 negative, 3 over budget. Mirrors lean_tell.py bit for bit. Credit Taylor (gtmcknight).
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
```
<!-- END AGE Strategy.sol -->

## 10. QLX5 Strategy.sol

sha256 `e183e5bc3fb794b7067703b10a7da9920267aa5f4caa968e16ca101b02338f40`, 47,230 bytes, 415 lines, 22,440 runtime bytes. From `code_zb64` of [QLX-S]; identical bytes in [QLX-A] and [QLX-B]. Policy, filter and tables: Taylor (gtmcknight).

<!-- BEGIN QLX5 Strategy.sol -->
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import {AMMStrategyBase} from "./AMMStrategyBase.sol";
import {TradeInfo} from "./IAMMStrategy.sol";
// Solved AMM policy by Taylor (gtmcknight), amm-sim 4812a638 research/solved: Gaussian filter + qm tables (qm_k1e-5.json),
// fee rule of real.py's qm variant (sd level, phase, synced flag). All credit for the policy, filter and tables: Taylor.
// Original tables compressed by qm-spline (cubic B-splines, QMS1 blob sha256 3ac7cb88...); filter, 3-slot state, math and fee conversion
// from trim-2 (port-3's filter); synced flag stored in bit 255 of slot 2.
// lookup-headroom: C0 (sha256 c68887cf...) with coefficient words loaded once per callback into memory and the
// second knot-span search of each axis walking forward from the first; same arithmetic, same fees.
// give-u1: lookup-u1 (Strategy.sol sha256 69c361ef...) plus one rule, the constant rival pull of GivePolicy (give.py sha256 8d871a6b...).
// lean-sol: give-u1 (Strategy.sol sha256 99d031f4...) with the exact-arithmetic isArb replaced by lb-4's LEAN TELL (bounded
// sell_one_division / buy_grid, budget 4): a first own trade is read as arbitrage iff the lean label is positive; negative, over
// budget and unsupported are misses; chance, filter, tables, pull, fee guard and storage slots unchanged (LEANBASE variant A).
// qlite-a: LEAN (sha256 a6dfc3ba...) plus the frozen qlgate rule cap24+GATE (qlgate.py sha256 0823f2d2..., qlite_int.capped_int cap 24):
// on a callback not read as arbitrage and at most 6 steps after the previous own callback, the capped router-quotient split test;
// a hit sets the rival spot to the marginal-price candidate, synced, and skips the 0.35 pull; a miss leaves LEAN unchanged.
// Credit: Taylor (gtmcknight), github.com/gtmcknight/amm-sim@4812a6382311624e1506aca131ca35c378f930d9 research/solved.
// Taylor source: https://github.com/gtmcknight/amm-sim/tree/4812a6382311624e1506aca131ca35c378f930d9/research/solved
contract Strategy is AMMStrategyBase {
    int256 constant U=1e18;
    int256 constant LN2=693147180559945309;
    uint256 constant M64=0xffffffffffffffff;
    // slots[0] = m (int128) | v (int128)<<128 ; slots[1] = sp (int128) | r (int128)<<128 ; slots[2] = fb | fa<<64 | t<<128 | cnt<<192
    function getName() external pure override returns(string memory) { unchecked {return "TellMinLookup";} }
    function mul(int256 a,int256 b) internal pure returns(int256){ unchecked {return a*b/U;} }
    function divi(int256 a,int256 b) internal pure returns(int256){ unchecked {return a*U/b;} }
    function ab(int256 x) internal pure returns(int256){ unchecked {return x<0?-x:x;} }
    function clip(int256 x,int256 a,int256 b) internal pure returns(int256){ unchecked {return x<a?a:(x>b?b:x);} }
    function ln(int256 x) internal pure returns(int256 z){ unchecked {
        require(x>0); int256 k;
        while(x< U){x*=2;k--;}
        while(x>=2*U){x/=2;k++;}
        int256 y=divi(x-U,x+U); int256 y2=mul(y,y); int256 q=y; z=y;
        for(int256 n=3;n<=29;n+=2){q=mul(q,y2);z+=q/n;}
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
        if(x<=0)return 0; uint256 n=uint256(x)*1e18;uint256 z=n;uint256 r=1;
        if(z>>128>0){z>>=128;r<<=64;} if(z>>64>0){z>>=64;r<<=32;}
        if(z>>32>0){z>>=32;r<<=16;} if(z>>16>0){z>>=16;r<<=8;}
        if(z>>8>0){z>>=8;r<<=4;} if(z>>4>0){z>>=4;r<<=2;} if(z>>2>0){r<<=1;}
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
        int256 tail=mul(mul(density,2506628274631000200),divi(n,d));return x>0?U-tail:tail;
    } }
    function trunc(int256 m,int256 v,int256 lo,int256 hi) internal pure returns(int256 Z,int256 mt,int256 vt){ unchecked {
        if(v<=0)return (lo<=m&&m<=hi?U:int256(0),m,0);
        int256 sd=root(v);int256 a=divi(lo-m,sd);int256 b=divi(hi-m,sd);
        int256 pa=pdf(a);int256 pb=pdf(b);
        Z=cdf(b,pb)-cdf(a,pa);
        if(Z<1e6)return(Z,m<lo?lo:hi,v/4);
        int256 r=divi(pa-pb,Z);
        mt=m+mul(sd,r);vt=mul(v,U+divi(mul(a,pa)-mul(b,pb),Z)-mul(r,r));if(vt<0)vt=0;
    } }
    // ---- qm-spline lookup (QMS1 blob sha256 3ac7cb88..., 10,167 B): 5 cubic tensor B-splines over (row, column, sd level),
    // ask side only; bid = point mirror. Coefficients int16 (1/8 bps) as PUSH32 immediates, 16 lanes of (c+32768) per word.
    // coefficient words of table tb (16 lanes of c+32768 each, word 0 = the table's first 16 coefficients), stored once per callback
    bytes constant QPL=hex"51504c314101a00005080004080c10141a223160ff7eff9cffb0ffc4ffceffd8ffe2ffe7ffecffeffff2fff4fff5fff6fff7fff8fff9fffafffbfffcfffdfffeffffff00000100020003000400050006000700080009000a000b000c000e001100140019001e00280032003c00500064008200a0000605fe02180b0007000055007000720078007b007c008100840089008d009000920094009500960097009c009d00a300a700aa00ab00400100010305060708090a0b0cff032b1e000307000052006b0077007c00800082008500870088008b008c008f0090009100920093009400960098009a009c009e009f00a100a200a400a500a600a700a800a900aa00ab00ac00ad00af00b200b500b900bd00ca00400100090c0f101112131415161718191a1b1c1d1e1f20222425262728292a30ff041c0d0002030700004a006900830084008500870088008a008b008d008e008f0090009200940097009c009d009e00a100a400a500a700a800a900ab00400100121315161718191a1b1c1e300003241a0003070000510073007d00870089008b008e008f009100920093009500970099009b009e009f00a100a300a500a600a700a800a900aa00ab00ac00ae00b000b200b600b800bc00bf004001000b101112131415161718191b1c1d1e20222425262728292a30ff03110a00030700005b00780088008a008b008d008f009000920095009b00a400a800ab00ad0040010012151618191a1b1e301e0c020403020101010101008305030404020202020102027203030606030303020301ff4c0303060703030302fcff7ad802030708030404000f7f019f02030808050402ff7f000f8c0203080807fefa72130d0a2d0204090d01105d0b0d0c09f401050b09164d0b120d0a0a9701070c263e0a120d0c0a09500107154413140d0d0c0a091c0108213e100e0f0c0d0d0bfe000925370c0f0e0f0f0a07e50009232d0e0f100e0b0b08dd00061f2b0d100e0e0c0a08d0000b162a0c100f0d0c0b07ca0000211a11100d0d0d0a0793000ee5290b100e0c0c0a08a000f5fb001511100c0b0b034a00eff3fa130a0f0f0b0a0c04000efcecf1140d0d0e0c0b0600ecf8e026fbf8d734120e0000000000000000000000000000000000000000000000000a0c030908030302020101017d05060a0a050404030202008103060e0d070706060504045d03060e0f070807070708d9ef02070f110809080b09d90ab902071011090a0b0ed61200a702071013080c0fe60505004d020911130e09ee0a050402180209121807f40c06060401bf010a1512fa0d08090604027a010916080b080a09060504490108110b0b0c09090703022501080f0f0d0b0a080605040c01010c130b0b0a08080604f500090d120a0b0a09080605fa00f60c0f0c0b0b09080605e100fb0d17090a0b0a0807057f00061b0d0b0b0909090806520014280f090b0a0909080c28000807fd080a0c0b0b0e002100e4fe030002060a0c060ebdff3609f503fcf5f91111d70000000000000000000000000000000000000000000000000106fe06020100010100000100010000010000ff0100000100ff010305fe02d102030102010002000101000100010001000001000001000102fffbf708ffdc0102020201000200010101010001010000000001ff0102fef605151e012d6701030102010101010101010101000000ff0000ff0200fa0b49151e02f2fb360104010201010101020101010000ffff01ff0002fa063933fcfef7010a051001040101010102020101010100ffff00ff05fdfb1168faf3050307fe0004fd000400020102010201020001ff0000ff02e70d3443f40403020101010304df00060101010102020102000000ff00fefb51140ff2070102020202010104c900080201010103010201000000ff00ff4b13010204020302010202010203bf00090200010202020201000000fffb540704040303030202020102010203a0000c0201010103020101000000024e01060404030203030102020201020495000e02ff0301030201010000fa480807060503040203020202010201020378000f030101020202020201ff3f040706060404030203030102020201020371000d0401010103020202002e0b09070606040403020303010301020201046a000c0501010102020202002e0b080706060404030204020202020201020362000d05010101020202021e0f0a080706060503030303020202020201020455001306020001020203041a0e0a07070705050402030302020202020202034f000f0a0301010102030b130b09080607050503030303020203020201020535001809070003030406090b0a08080607050504030204020202020202020521001a0d040302020608090808080706060605030402030303020203020204130014100505fe08000a09070807070606050505030203040202020501040afbff1b0f0a0108fd0cfc0b08060806070605040503020501040503040202ecb5ff4d1409000d0c0003fc080606070705050504040304090504030405057fccff2b180419fb12fb03f905070508060705050303040d0704030408115556c7ff39e4370a0ffbf904f602060507070605060406040c09061512283630f10000a668180201fe03fb00f804060507070605050707060a061626282a1cfff5ff0b1dfe04fffd03fa02f8ff0405060807050604050b070f0f242832130098ff75050403fdfe03fb02fafe0105050708050804040b050f102428311300a1ff6b000600fdff03fc00fdfbfb0a05060708050705070a0b1c1827311300cfff37020400fe02fefefe01f9000007050707060704090b091d172e2913000000f70b05f90600fa00000000000000000a07070605070c0a1c172e29120000000000000000000000000000000000000009070507080a091c172e2812000000000000000000000000000000000000000007050709090f16162e2812000000000000000000000000000000000000000000000a0a071016162e281100000000000000000000000000000000000000000000000b0d0a16152e281100000000000000000000000000000000000000000000fb070e0b141c26271200000000000000000000000000000000000000000000fbf40d12151428290e00000000000000000000000000000000000000000000000000e5201926270d0000000000000000000000000000000000000000000000000000f50c26270b010000000000000000000000000000000000000000000000000000fc05280aff000000000000000000000000000000000000000000000000000000fd04070300000000000000000000000000000000000000000000000000000000f0af8000000000000000000000000000000000000000000000000000000000000000ff0508fd040001010001010001000100010000010000010000000100010203ce02050203010100010101010101010100010001000100010002010101fd02da010304020101020001010201010301010101000100040101fdfd0907151a6701020402010201010102020203ff020002fe020101fefc051429190704fe37010303020202010002020303010201fffd0100fdf70c332103ffff02020712010302020202020002030302020103f903fefc0b2c2cf203010304030304000102030202020101010403030003ff0003022a1b02fe0404040203010304df0008010302020102010402030101090c35ff03fb04060201040203020304c9000b00050103010103030502000b12190dfe050404040301040400020304be000d00040202030002050404fff93b02070604030304020304010302030395001c000302020102030505030442e8080606050402050302020103020304820026010004030101050405051a090a08060405040304030104010203030360002c04fe0502020205060810090b0907060604030304030202030301030461002206fe030301020608090b0d09080806050404020502020302020303045b002007ff0103010206090d070c090807060505030205030203020202030457001c0701000202020709070c0b09080607050403030403020302030203044b00220702ff010302060a060b0b09070706050404030403020302020204043e00290801010002030505090b0a09080606050404030403020402020203052d00260e04000300030405080909080707060504040304030302030302030518002d0b04030102020505070808080707050604040304040203030302030608002a0e0404ff04000505070809080607060504040305040304020401040bf4ff2e0d0701040003010507070809070607040704040504040402050206fb98ff7b0c060006fd05ff07060707090807060705050409050405050606097fc2ff460f06fe05fe07030207060807080905070405050908050a050a075751d9ff1a140204ff0cfc05ff07070608080807050804050708070c0e222a52f5e7ffd23112080109fe07fc07070608070808050705040906080b0c2f3832fdeeff08fffdfb150008fd06f906060707070807050507070704130f352a36f1dcff0c11020804fefffe01fe010807060708060607040909060e11302e2ff8e1ff1bfb0b0002ff00fe0101de091f060608070605050907080c172c2d2afef0ff0eff05fffb06ff02fbff030000070607070605050909090f112a3524fd0000fa05fd04feff0300000000000000000b070606050b06090f14283327f9000000000000000000000000000000000000090606060908080f142b2f22ff0000000000000000000000000000000000000008050509080b1017282b22fe0000000000000000000000000000000000000000000a090a081017272e20fc000000000000000000000000000000000000000000000d07090f17272d1ffe000000000000000000000000000000000000000000fa080b0c0f14292720fd00000000000000000000000000000000000000000000f10f081116252b1700000000000000000000000000000000000000000000000000f011142728140000000000000000000000000000000000000000000000000000fefa28271202000000000000000000000000000000000000000000000000000000fc2612fd00000000000000000000000000000000000000000000000000000000fe090500000000000000000000000000000000000000000000000000000000ffac8000000000000000000000000000000000000000000000000000000000000000d105fb1b070302030202020202010101010101000101010101010201010204b202fd0e0b0303030302030302020202010102010001020201010102010406cf0102fe0f020304030403030303030202030102020102010203040100ff01600109f70f030404040404030404030504010203fe00020402fff7fe02050a35010af70b0404040504040404060505020001fd010902f4fa010705030407150107f908040405040504050506070a0108fe16fcdaf70805050204020508040107fa06050404060404050509060c060ff1f7e2050c0005030304030508e5000dfc020504050604050508030ffeffec04fd0c01000502040204030508c9001901fb0603050506040505060402f7ff070402ff020304030405010509c1001903f806040406050406050a07eb0a0302000401030103050501030508a0002006f8030305060505050e0bda180004050103040102040501040305099b001f02fb010405050505060af405050403050204010503030302030405097f001d0b00fa0204050505040101020504070505020405020105060301050a6f00240dfefd0004050405040200040306070505020502040107030303060a6a00210a00ffff03050504020300040705060604050404030404010403060b65001c0c02ff000004040505ff01040806050704040406040204010504060b6400131100ffff01030404050003040409050605040406040403010604060b59001c09fd04ff0201040505ff05020508070604050406050105050701070b3f0030040101fffe020202020700050707070506050407050404050603080d3000290d0400fffffb05020204030408070607050505080605060505050a0f1f002e09fe02ff0304fa030304060607070607050605080606060608080a130f002b0a0301fffffffb070305050907070d010905030d060608070a080f1e0300270b01010003fe08f5030608050906070bfd0d05060d0b0b070c0e1718eaff3a080304ff06f8fefc0505070609050a070b02030e020c09130e0ffc50e0ff3405080afff105fd08f90407090609070600050d0b060b0103120b4540d2ff3c18fbfdfdfafd0111f0050608070905070a000e010d08091200193c39a8ff5afdf617e00ffaf80618fd050808080a030a08fb130c0b0003fc2e3f3b0000fd0503f2fc02ff07fc07ff08070907080805010617fd090d06fd274435000000f700fb0702fd06fdfd12fdfd0807080404070515030513f90528462e000000f207ff08f302f7140000000002090704040f06090112ff061510512a0000fefe040000000000000000000000000a08070506020c10020c0c24461c000000000000000000000000000000000000090606ff150a07000f17134f1500000000000000000000000000000000000000040405110cff11f81e1e461a000000000000000000000000000000000000000013f90c010613fb1d223f190000000000000000000000000000000000000000000009140707f91e23421100000000000000000000000000000000000000000000fd15ff160513253d0d00000000000000000000000000000000000000000000db171a04052b193a04000000000000000000000000000000000000000000000000e5111a0a2b32020000000000000000000000000000000000000000000000000000f311292eff000000000000000000000000000000000000000000000000000000e82b1c0400000000000000000000000000000000000000000000000000000000e52af9000000000000000000000000000000000000000000000000000000000080bf0000000000000000000000000000000000000000000000000000000000000009060001010000010000010000002903000101010000010001000100f801000002010002000100010000fd00000202020000ffff00ff01fff5000001030100ff00ff00f0630eeb00000203000000ff00020067eed80001010301ff0000fff84f18ffcf0000020300000001e766070900bd0000020201ff00f44518050900b4000002020000fe1933070609ffa20000020300fff25aff07050900990000020301fa40080707060800900000020400f8420907060608008700010204f9360a09070705080078000102031a150a0807060608ff6e0000020b170c090706060608ff5b000104100a090808060606080038000105100705050606060509003100010df71107060707050609003d0003fb07fc07050806060608003100fefbfefc06050607070708ff19000402fbf8fe05050607060d001400fe04fbfcfe02060407080d000b0000fffd02f6f40d0705090bff070000f9000000000000000b0d000000000000000000000000010fff0000000000000000000000ec1200000000000000000000000000ee1008060001010001000100010000002703010101010101000100010000f701000202ff0103010000000102fd00010303010200ff00ff0000fff5000102040002ff0000fffa5508ec000103020102ff00fff3560a03d90001040200020000ff36180603d000010401010300f83c10070704be00010401010400231809070704b500010302020306330507060803a4000004030305230d0a080507039b000105020412180b080806070392000203030715130b08070607038a000105010c180d0a08070507037b0002fb120f0e0b090806060703700002040a0b0c0a090707050703600001010c0909080807060606033d00fd03090707080807050607043300ff0306090707080707050901210010fe060607070808060509012200f801000507070608080608071100f908fff9040606060709080608000afb00fbff050605070809060a00fe00f901ec060c0706070b050200fe00000000000000000b0b040000000000000000000000000e070000000000000000000000f50705000000000000000000000000804c0d06fd02010100010100000001002c03fe0202010101000101000100f90100030201020101010100ff06fe00030505030402ffffffffff06f60003050604040102fb270a09efed0003050704040203150d0909f8db000305070505030e0e0a0808fdd1000406070504070e0c0a0709fdc00003060805060a0d0b090708ffb70003060807060c0c0a080609ffa60003060a06080c0b09080608029e0002070908080b0c0808060801950004050a080a0b090a060608028d0003060a080a0b0a08070608027e0003040c090a090a070706070472000305030c0a0a090806060704610003000b0708070807060607043b00020205070708090706060809300009fd0507070808080706080926000bfe04060708080807050908110007010006060708070807080bfaff070701fc070607070708090addff28e41c01e81c060707070a0aa9ff2de03dfff10e0f0607060b0a00000000000000000000e9220b090000000000000000000000010c0b0000000000000000000000f7fc170000000000000000000000008080d7051b0603020101000100000100000319080402020101010102ff01df01120b05030202020100fb07030401040b0804030405050a1beee00001010b070404050505f0f6f91bf900000a0804040503fdfbfcf615ea00fe0a0804040401fffa02fb0be300fd090804050301fffc01fc09d400fc080804040301fd0003ff04cd00fb070805030301fc0205fe04bf00fa0508040402000101040200b800fa0408040302ff0105030200b200f80308040402ff0106040101ab00f90108040304fe01050601019e00f9fe070403010006040503018d00fcfb090304fd0305070403047900f903fe0602020206050408075800fdf5ff0304050808060804045300f102fe0103040708060708034c00f0fcfc0703080408040807093800e509fff70607080608070b031b00fbe6ff13fb05080707020b112300cf25dbfd25f2060906070e06050009fb0400fdfdf80505070c110000000000000000000008010b1300000000000000000000000011100000000000000000000000ea1d0000000000000000000000000080800103ff0300000000000100000000000000000000000100000000006e0100020000010000000000010000000100000000000000000101c700010101000001000001000000000000ff01000100ff0000fffc97000101010001000001000000ff00000001fefeff01ff040210216700020100010001000000000000000101fb080a0efb1f0b08fef25c00030101010001000000000001fc00fd2a17f90400fe01ff0003530003010101000100000000fffc111d0706fd0200000200010100420007000101010000000000fc2d0bfe00010201000101000100013d00070101010001000000ff0a28fc03020201000101000100010135000701010001000100000127010402020201010001000100010131000801010001000000001f04070203010201010101000100010128000e010100000000fd1c050407030202020101000101000100011e00100400010101020b0705040603020202010101000101000101100016040001030405050504040603020202010101000101000101090015040101020505040503040603020202010101010100010101faff1c050102010306040304040603020202010100010101010102e4ff260405fe070201040303040603020202020203010201000201eaff1b07020bfe04fc0403030307020302030601020200ff00011f6eff7f230203fe02fc0103030307020303050303030307100a222adfff2f05fefe04fc02fa01030208030304030403010907231e0bf902000702ffff02fd01fdff010306040403050302050514131d0afffcff0b01ff02fffe0000fdfd0505040403050304040513141c0bfecaff3b00ff02ffffff00fd000006040304050206030414141b0bfef6ff0dfd0003fd03fd0000000000060304040503030d0b1b140bfe0000000000000000000000000000000503060403030d0b1a1509ff0000000000000000000000000000000004060403060a0b191509ff000000000000000000000000000000000006030506090b19140aff00000000000000000000000000000000ff01070305091014140aff0000000000000000000000000000000000fa0207060b0c121509ff000000000000000000000000000000000000fd00040a0b151407000000000000000000000000000000000000000000fe050c12140700000000000000000000000000000000000000000000f704141306000000000000000000000000000000000000000000000000061305000000000000000000000000000000000000000000000000ef170400000000000000000000000000000000000000000000000000f40700000000000000000000000000000000000000000000000000000000ff0204ff01010000000100000000000100000000000000000100006c0102020100000100000100000100000001000000000001000002c6000202010001000100010100000001ff0001000100000100ffff97000102010101000101010001fd000002fffffdfb02010303081c67000301010201010101ff0100feff00fc05030d1505020a0305fb5e00030102010101010200fffeff05ff1715fe06fffe01ff0001035500030102010101010100fd0512120002020101010201010001024400070102010102000202060b15fa0302030201000100010101023d000a00020102020102030610050303020301010002000101010231000e010101020202010416fb09030202030201000101010101012c00100101010102020409050508020302030200010101010101012c000d01000102020307030605080203020301010101000200010220001303ff010102030405050507030202030201000200010101011400170301000202030305040407030302030101010101010100020f001403010101020303050404070302020302010101010101010106001504ff02010202040404050703020203020201010002000102f3ff1c03020002ff04030404040803040204040101020102010203f2ff190203fd03000404030404090203040502020302020300fb1cf0ff110301030003000403040408040303040303010305060b31220100e6140402fe050101040304070503020602040203020c1d2c05f2ff0c04fffe03fe02fb0404030704040305030303020412152a06faff06010001fffd0300ee0411070403030504020306010f1c2604efff12ffff020000fe00010000070304030505010305050f142c01e4ff180401fa05fb05000000fff90e0303060402040405141525000000000000000000000000000000000504050304040308121e19010000000000000000000000000000000004050403040408121c190200000000000000000000000000000000000505030306061418190200000000000000000000000000000000ff010604030508111a19ff00000000000000000000000000000000fffeff070407081215140100000000000000000000000000000000000000fd020908131510fe000000000000000000000000000000000000000000ff0815130eff000000000000000000000000000000000000000000fbfe11120dff000000000000000000000000000000000000000000000000140a000000000000000000000000000000000000000000000000fe030900000000000000000000000000000000000000000000000000fefd00000000000000000000000000000000000000000000000000000000e602050dff010101010001000100000100000100000001000100025c01020b0002010101010101010100000100010001000100010002c300000602020102020102010102010001000001000100010101039900010104020202010301020202ffff000101010200000100fffe690008ff030203030202020302030100fd00fe01fb0101010101065c000eff02020301030204030206ff01f9f9fb080102020102020353000eff030202020204040605f6fc03ff02fd0301010201010203440012ff0102030301020402fc010401ff010002010102010102033e0015ff0003020301020202fc060101010200000201010101020438001101ff020303030203f5080403010202fe03000203ff01020436000f01000103020302fc0302040302000400000102010201020332000e03ff01020302fd03020205020301030001010102010202032d000fff000100010201020202050303020303ff0003010201020426000f0201ff0001010000030305040203030301010201020103041d001103fd01fe0301010202020603030305030102010202010305140013fe03ff03fb030102030407050302040402010301030203050d000c0302fd0003fc02020403070306010703040303030303060a0a000b020008fb04f801030303090503000406040005040305080802000c05ff03fdfc01ff0204040801010806040204050103ff011cf1ff1dfcfd01fc0005fe01020508040405000703040402feff0b26e8ff1afbff00fdfdf81af6040407050203070801030603f7001427fbff010100ff0204fcff09fefe080401030c0104020306fbff1427f9ff020104fb01fb09000000fd0903050405ff07070102000016230000fd00fa09000000000000fd0601050402050cfe0401f90d12230000000000000000000000000000000501040a04fd0703fb0a191d0000000000000000000000000000000002080604000305f70c1c1b0000000000000000000000000000000000070103030800fd051f2300000000000000000000000000000000fe020a010203030707161e0000000000000000000000000000000000f0100404000404092213000000000000000000000000000000000000fffd05fb0a080821120000000000000000000000000000000000000000fff01301111d0f00000000000000000000000000000000000000000000cb29141b070000000000000000000000000000000000000000000000ec151a04000000000000000000000000000000000000000000000000f9100100000000000000000000000000000000000000000000000000fb0000000000000000000000000000000000000000000000000000000005060101ff0100000000017d020101010100010001fe63010102010100ff00ffffcb00010300ff00ff01fffeb9000103000000fff52516b000010300fffffafc72039e0001030000f805600bfa8c00010300fefa520d0c028400010303f45108070d0075000101f7371b07070b006700ff061629fb08070bff3700031e04070d06040dfe2800e3ff030b04040c10fe03000cfc04da0f080019ffe4fffa09fa1f0000e916fc000000000000000000ed0e00000000000000000000000906fd03000100010000008002fe040002010100010065010105020101feff0003ce000309fb02ff00ff0102bd000306fc05fd02090a12b4000308fa0207f54016e9a2000403ff041530000a009100040300093500070ffe89000403e952fb08070e007b00000017220108070e026c000210060d0b07070d033e0003070a100908070e05f6ff0506010f080709100b0300fdfbea0a090605130bf9fff30d07000000e7180b0000000000000000fa07f600000000000000008cbe80d1051b08000101000000005902170e000301000102005a010d130006020201fffedd00001306090302fefefbd000fd140509060531bb04c800fd12070a0513e5e711bb00fb12050b03e40dfb07ad00fa100609f30404fb05a600fa0e0ff106fe0600029900f90c00010401060201810000ff0706fc060607025d00fafe01090604070b061b00f4f708ff0a09051502fffff30f02fcfe0203180afeff02fdfe050000d0390a0000000000000000ef0d05000000000000000080807f";
    struct QT {uint256 lk;uint256 r0;uint256 r1;uint256 r2;uint256 ck;uint256 nl;uint256 nr;uint256 nc;uint256 off;int256 scale;}
    function qt(uint256 tb) internal pure returns(QT memory t) {
if(tb==0) t=QT(0x70000,0x960095009400920090008d008900840081007c007b00780072007000550000,0x14000ab00aa00a700a3009d009c0097,0x0,0xc0b0a0908070605030100,2,24,11,540,250000000000000000);
else if(tb==1) t=QT(0x700030000,0x9200910090008f008c008b00880087008500820080007c0077006b00520000,0xa900a800a700a600a500a400a200a1009f009e009c009a0098009600940093,0x14000ca00bd00b900b500b200af00ad00ac00ab00aa,0x302a29282726252422201f1e1d1c1b1a191817161514131211100f0c0900,3,43,30,1116,500000000000000000);
else if(tb==2) t=QT(0x7000300020000,0x9400920090008f008e008d008b008a008800870085008400830069004a0000,0x14000ab00a900a800a700a500a400a1009e009d009c0097,0x0,0x301e1c1b1a1918171615131200,4,28,13,5115,500000000000000000);
else if(tb==3) t=QT(0x700030000,0x9b009900970095009300920091008f008e008b00890087007d007300510000,0xb600b200b000ae00ac00ab00aa00a900a800a700a600a500a300a1009f009e,0x14000bf00bc00b8,0x302a29282726252422201e1d1c1b191817161514131211100b00,3,36,26,6683,1000000000000000000);
else if(tb==4) t=QT(0x700030000,0xad00ab00a800a4009b009500920090008f008d008b008a00880078005b0000,0x140,0x0,0x301e1b1a191816151200,3,17,10,9599,500000000000000000);
    }
    function rk(QT memory t,uint256 i) internal pure returns(uint256){unchecked{return ((i<16?t.r0:(i<32?t.r1:t.r2))>>(16*(i%16)))&65535;}}
    function spanR(QT memory t,uint256 x) internal pure returns(uint256 a){unchecked{
        uint256 hi=t.nr-1;while(hi-a>1){uint256 m=(a+hi)/2;if(rk(t,m)<=x)a=m;else hi=m;}
    }}
    function spanC(QT memory t,uint256 x) internal pure returns(uint256 a){unchecked{
        uint256 hi=t.nc-1;while(hi-a>1){uint256 m=(a+hi)/2;if(((t.ck>>(8*m))&255)<=x)a=m;else hi=m;}
    }}
    function record(bytes memory b,QT memory t,uint256 l,uint256 r,uint256 c) internal pure returns(int256 v,int256 vn){unchecked{
        uint256 o=t.off+(l*t.nr+r)*(t.nc+1);
        v=int256(int16(uint16(uint8(b[o]))|(uint16(uint8(b[o+1]))<<8)));
        for(uint256 n=0;n<c;n++)v+=int256(int8(uint8(b[o+2+n])));
        vn=v+int256(int8(uint8(b[o+2+c])));v*=t.scale;vn*=t.scale;
    }}
    function lerp(int256 a,int256 b,int256 f) internal pure returns(int256){unchecked{return a+mul(b-a,f);}}
    function surf(QT memory t,bytes memory b,int256 pw,int256 p2,uint256 k,int256 tt,uint256 jm) internal pure returns(int256){unchecked{
        uint256 i=uint256(pw/U);if(i>319)i=319;int256 f=pw-int256(i)*U;
        uint256 j=uint256(p2/U);if(j>jm)j=jm;int256 g=p2-int256(j)*U;
        uint256 a;while(a<t.nl-2&&((t.lk>>(16*(a+1)))&65535)<=k)a++;
        uint256 r=spanR(t,i);uint256 c=spanC(t,j);
        int256[8] memory v;
        for(uint256 l=0;l<2;l++)for(uint256 row=0;row<2;row++)(v[l*4+row*2],v[l*4+row*2+1])=record(b,t,a+l,r+row,c);
        int256[2] memory lr;lr[0]=int256((t.lk>>(16*a))&65535);lr[1]=int256((t.lk>>(16*(a+1)))&65535);
        int256 rlo=int256(rk(t,r));int256 rd=int256(rk(t,r+1))-rlo;
        int256 clo=int256((t.ck>>(8*c))&255);int256 cd=int256((t.ck>>(8*(c+1)))&255)-clo;
        int256[2] memory levels;
        for(uint256 l=0;l<2;l++){
            int256 u=(int256(k+l)-lr[0])*U/(lr[1]-lr[0]);int256[4] memory q;
            for(uint256 z=0;z<4;z++)q[z]=lerp(v[z],v[z+4],u);
            int256[4] memory nodes;
            for(uint256 row=0;row<2;row++){
                int256 rf=(int256(i+row)-rlo)*U/rd;
                int256 x0=lerp(q[0],q[2],rf);int256 x1=lerp(q[1],q[3],rf);
                for(uint256 col=0;col<2;col++){
                    int256 cf=(int256(j+col)-clo)*U/cd;
                    int256 n=lerp(x0,x1,cf);nodes[row*2+col]=n>0?n:int256(0);
                }
            }
            levels[l]=lerp(lerp(nodes[0],nodes[2],f),lerp(nodes[1],nodes[3],f),g);
        }
        return lerp(levels[0],levels[1],tt);
    }}
    function w2l(uint256 L) internal pure returns(int256){ unchecked {
        uint256 K=L<16?0x7ff77ff67ff57ff47ff27fef7fec7fe77fe27fd87fce7fc47fb07f9c7f7e7f60:(L<32?0x800780068005800480038002800180007fff7ffe7ffd7ffc7ffb7ffa7ff97ff8:(L<48?0x808280648050803c80328028801e801980148011800e800c800b800a80098008:0x00000000000000000000000000000000000000000000000000000000000080a0));
        return int256((K>>(16*(L&15)))&0xffff)-32768;
    } }
    // real.py/evalpol _pos2 over pol_mid's W2L (grid units of 5 bps), WAD in and out
    function pos2(int256 v) internal pure returns(int256){ unchecked {
        if(v<=-160*U)return 0; if(v>=160*U)return 48*U;
        uint256 lo=0;uint256 hi=48;
        while(hi-lo>1){uint256 md=(lo+hi)>>1;if(w2l(md)*U<=v)lo=md;else hi=md;}
        int256 a=w2l(lo);return int256(lo)*U+(v-a*U)/(w2l(hi)-a);
    } }
    function sdl(uint256 k) internal pure returns(int256){ unchecked { return int256((0x221a14100c080400>>(8*k))&0xff); } }
    // qm fee rule: w, w2 offsets (WAD bps), phase, synced flag, belief variance v (WAD, ln-price^2)
    function fees(int256 w,int256 w2,uint256 ph,bool syn,int256 v) internal pure returns(int256 fb,int256 fa){ unchecked {
        int256 sd=root(v)*10000;uint256 k;
        while(k<6&&sd>=sdl(k+1)*U)k++;
        int256 tt=clip((sd-sdl(k)*U)/(sdl(k+1)-sdl(k)),0,U);
        int256 pw=clip(w/5+160*U,0,320*U);int256 wq=(pw-160*U)*5;
        uint256 tb;int256 p2;int256 nc1;
        if(ph==0){tb=0;p2=clip(w2/5,-6*U,6*U)+6*U;nc1=12;}
        else{tb=(ph==1?1:3)+(syn?0:1);p2=pos2(w2/5);nc1=48;}
        QT memory t=qt(tb);bytes memory b=QPL;
        int256 xa=surf(t,b,pw,p2,k,tt,uint256(nc1)-1)+wq-w;
        int256 xb=surf(t,b,320*U-pw,nc1*U-p2,k,tt,uint256(nc1)-1)+w-wq;
        fb=xb>0?U-exp(-xb/10000):int256(0);fa=xa>0?U-exp(-xa/10000):int256(0);
        fb=clip(fb,0,U/10);fa=clip(fa,0,U/10);
    } }
    function afterInitialize(uint256 x,uint256 y) external override returns(uint256,uint256){ unchecked {
        int256 sp=int256(y*1e18/x);
        slots[0]=uint256(uint128(int128(ln(sp))));
        slots[1]=uint256(uint128(int128(sp)))*(1+(uint256(1)<<128));
        slots[3]=x;slots[4]=y;slots[5]=0;
        slots[2]=2823606104386589*(1+(uint256(1)<<64));
        return(2823606104386589,2823606104386589);
    } }
    // filter update over a gap of dt steps; returns new m, v, rival spot r and the arb flag
    function update(int256 m,int256 v,int256 fb,int256 fa,int256 sp,int256 r,int256 s,bool buy,uint256 dt,bool hit,int256 chance) internal pure returns(int256,int256,int256,bool arb){ unchecked {
        int256 lo=ln(mul(sp,U-fb));int256 hi=ln(divi(sp,U-fa));
        uint256 n=dt-1;if(n>12)n=12;
        for(uint256 i=0;i<n;i++){v+=893025000000;(,m,v)=trunc(m,v,lo,hi);}
        v+=893025000000;
        int256 lp=ln(buy?mul(s,U-fb):divi(s,U-fa));
        int256 sd=root(v);int256 la=divi(pdf(divi(lp-m,sd)),sd);
        (int256 Z,int256 mt,int256 vt)=trunc(m,v,lo,hi);
        int256 d=ab(ln(divi(s,sp)));if(d<1e9)d=1e9;
        int256 pi=pdf(divi(ln(d)+6801595083153746944,1176000000000000000));
        int256 lr=divi(mul(mul(Z,260000000000000000),pi),mul(d,1176000000000000000));
        lr=mul(lr,chance);
        pi=hit&&la+lr>0?divi(la,la+lr):int256(0);arb=pi>U/2;
        if(pi>5e15&&pi<995e15){
            m=mul(pi,lp)+mul(U-pi,mt);
            v=mul(pi,mul(lp-m,lp-m))+mul(U-pi,vt+mul(mt-m,mt-m));
        }else if(arb){m=lp;v=0;}else{m=mt;v=vt;}
        int256 pe=exp(m);r=clip(r,mul(pe,997e15),divi(pe,997e15));
        return(m,v,r,arb);
    } }
    function afterSwap(TradeInfo calldata t) external override returns(uint256,uint256){ unchecked {
        uint256 s0=slots[0];uint256 s1=slots[1];uint256 s2=slots[2];
        int256 m=int256(int128(uint128(s0)));int256 v=int256(int128(uint128(s0>>128)));
        int256 sp=int256(int128(uint128(s1)));int256 r=int256(int128(uint128(s1>>128)));
        int256 fb=int256(s2&M64);int256 fa=int256(s2>>64&M64);uint256 cnt=s2>>192&0xffffffff;bool syn=s2>>255==1;
        int256 s=int256(t.reserveY*1e18/t.reserveX);bool arb;
        if(t.timestamp>(s2>>128&M64)){
            bool hit=TellMath.ltTell(slots[3],slots[4],uint256(t.isBuy?fb:fa),t.amountX,t.amountY,t.reserveY,t.isBuy)==1;
            int256 chance=hit?int256(TellMath.ulpOverGridWad(t.isBuy?t.amountX:t.amountY,t.isBuy?slots[3]:slots[4],t.isBuy?t.reserveX:t.reserveY)):int256(0);
            (m,v,r,arb)=update(m,v,fb,fa,sp,r,s,t.isBuy,t.timestamp-(s2>>128&M64),hit,chance);cnt=0;syn=false;
        }
        uint256 ph;
        if(!arb){
            int256 c=t.isBuy?divi(mul(s,U-fb),997e15):divi(mul(s,997e15),U-fa);
            // counting variant qlx5 (copy-b, e04-split-engine): tracked-offset split test (see copy-b result). Credit Taylor (gtmcknight).
            bool qx;if(t.timestamp<(s2>>128&M64)+7){int256 m0=int256(slots[6]);int256 mm;(qx,mm)=TellMath.qHitX(t.isBuy?t.amountX:t.amountY,slots[3],slots[4],uint256(t.isBuy?fb:fa),t.isBuy,m0,5);if(mm!=m0)slots[6]=uint256(mm);}if(qx||(t.isBuy?c<r:c>r)){r=c;syn=true;}
            // give: bound did not bind -> pull ln r 0.35 of the way to ln c (GivePolicy, alpha=alpha2=0.35)
            else if(c!=r){int256 lr=ln(r);r=exp(lr+mul(35e16,ln(c)-lr));syn=true;}
            cnt++;ph=cnt==1?1:2;
        }
        slots[3]=t.reserveX;slots[4]=t.reserveY;
        int256 w=(ln(s)-m)*10000;int256 rr=(ln(r)-m)*10000;
        (fb,fa)=fees(w,rr,ph,syn,v);
        fb=guardFee(fb);fa=guardFee(fa);
        slots[0]=uint256(uint128(int128(m)))|uint256(uint128(int128(v)))<<128;
        slots[1]=uint256(uint128(int128(s)))|uint256(uint128(int128(r)))<<128;
        slots[2]=uint256(fb)|uint256(fa)<<64|t.timestamp<<128|cnt<<192|(syn?uint256(1)<<255:0);
        return(uint256(fb),uint256(fa));
    } }

    // Complete integer preimage of Vanilla gamma under IEEE binary64 conversion.
    // Closest integer outside that interval; ties select the lower fee.
    function guardFee(int256 f) internal returns(int256) {
        if(f>=2999999999999948&&f<=3000000000000057){slots[5]++;return f-2999999999999947<=3000000000000058-f?int256(2999999999999947):int256(3000000000000058);}return f;
    }
    function guardShifts() external view returns(uint256) {return slots[5];}
    // lean label of a trade: 0 unsupported, 1 positive, 2 negative, 3 over budget; isArb = (label == 1). x (reserveX) is not used.
    function leanLabel(bool b,uint256 ax,uint256 ay,uint256,uint256 y,uint256 px,uint256 py,uint256 fb,uint256 fa) public pure returns(uint256) {return TellMath.ltTell(px,py,b?fb:fa,ax,ay,y,b);}
    // qlite-a decision as afterSwap takes it: p paid wad, px/py previous reserves, f fee wad of the paid side, dt steps since the previous own callback
    
    function isArb(bool b,uint256 ax,uint256 ay,uint256 x,uint256 y,uint256 px,uint256 py,uint256 fb,uint256 fa) external pure returns(bool) {return leanLabel(b,ax,ay,x,y,px,py,fb,fa)==1;}
}
library TellMath {
    uint256 internal constant WAD = 1e18;
    uint256 internal constant TWO53 = 1 << 53;
    uint256 internal constant TWO52 = 1 << 52;
    uint256 internal constant LIM = 1 << 128;

    /// floor(log2(x)) + 1, 0 for x = 0, by binary normalization.
    function bitLen(uint256 x) internal pure returns (uint256 n) {
        unchecked {
            if (x >= 1 << 128) { x >>= 128; n += 128; }
            if (x >= 1 << 64) { x >>= 64; n += 64; }
            if (x >= 1 << 32) { x >>= 32; n += 32; }
            if (x >= 1 << 16) { x >>= 16; n += 16; }
            if (x >= 1 << 8) { x >>= 8; n += 8; }
            if (x >= 1 << 4) { x >>= 4; n += 4; }
            if (x >= 1 << 2) { x >>= 2; n += 2; }
            if (x >= 1 << 1) { x >>= 1; n += 1; }
            if (x != 0) n += 1;
        }
    }

    /// num/den (both > 0) rounded to nearest-even double m*2^e, 2^52 <= m < 2^53.
    /// One division: the bit-length estimate is off by at most one binade, fixed by a shift.
    function rn(uint256 num, uint256 den) internal pure returns (uint256 q, int256 e) {
        e = int256(bitLen(num)) - int256(bitLen(den)) - 53;
        uint256 sn; uint256 sd;
        if (e < 0) { sn = num << uint256(-e); sd = den; } else { sn = num; sd = den << uint256(e); }
        q = sn / sd;
        // estimate gives q in [2^52, 2^54): at most one step down in precision
        if (q >= TWO53) {
            e += 1;
            if (e <= 0) { sn = num << uint256(-e); } else { sn = num; sd = den << uint256(e); }
            q = sn / sd;
        }
        uint256 r = sn - q * sd;
        uint256 twice = 2 * r;
        if (twice > sd || (twice == sd && (q & 1) == 1)) {
            q += 1;
            if (q == TWO53) { q = TWO52; e += 1; }
        }
    }

    /// e with 2^e * 1e18 <= w < 2^(e+1) * 1e18 (w > 0).
    function binade(uint256 w) internal pure returns (int256 e) {
        e = int256(bitLen(w)) - 60; // bitLen(1e18) = 60
        if (!_atLeast(w, e)) e -= 1;
        else if (_atLeast(w, e + 1)) e += 1;
    }

    function _atLeast(uint256 w, int256 e) private pure returns (bool) {
        return e >= 0 ? (WAD << uint256(e)) <= w : WAD <= (w << uint256(-e));
    }

    function _min(int256 a, int256 b) private pure returns (int256) { return a < b ? a : b; }

    /// log2 of the grid: min(binade(before), binade(after)) - 52.
    function gridExp(uint256 beforeW, uint256 afterW) internal pure returns (int256) {
        return _min(binade(beforeW), binade(afterW)) - 52;
    }

    /// min(1, ulp(paid)/grid) scaled by 1e18, paid = fl(paidW/1e18) (the double behind paidW).
    /// Returns 0 for out-of-bounds inputs. 1e18 means the paid amount is no finer than the grid.
    function ulpOverGridWad(uint256 paidW, uint256 beforeW, uint256 afterW) internal pure returns (uint256) {
        if (paidW == 0 || paidW >= LIM || beforeW == 0 || beforeW >= LIM || afterW == 0 || afterW >= LIM) return 0;
        (, int256 pe) = rn(paidW, WAD);
        int256 d = gridExp(beforeW, afterW) - pe;
        if (d <= 0) return WAD;
        if (d > 64) return 0;
        return WAD >> uint256(d);
    }

    // ---- LEAN TELL of result lb-4 (scratch/LeanTell.sol, functions verbatim): buy-grid's bounded sell_one_division / buy_grid tests,
    // budget 4, in exact integer binary64 (round-to-nearest-even) arithmetic. A double is m*2^e with 2^52 <= m <= 2^53; 1e18 = LT_C*2^7.
    // ltTell returns 0 unsupported, 1 positive, 2 negative, 3 over budget. Mirrors lean_tell.py bit for bit. Credit Taylor (gtmcknight).
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
    // ---- qlite-a split test: qlgate.py cap24+GATE = qlite_int.capped_int(cap=24) in exact integer binary64 (round-to-nearest-even)
    // arithmetic, one candidate (preimage pair (0,0), z = r, k = n). Credit Taylor (gtmcknight), amm-sim 4812a638 research/solved.
    uint256 constant QG=8980177656976769;int256 constant QGE=-53; // 0.997
    uint256 constant QK=8782888972198741;int256 constant QKE=-43; // sqrt(1e6*0.997)
    // n > 0 to the nearest double m*2^s, 2^52 <= m < 2^53.
    function qR(uint256 n) internal pure returns(uint256 m,int256 s){unchecked{
        uint256 h=ltMsb(n);
        if(h<53)return(n<<(52-h),int256(h)-52);
        s=int256(h)-52;m=ltRound(n,uint256(s));if(m>>53!=0){m>>=1;s++;}
    }}
    // RN(a/b), a and b of 53 bits: m*2^s.
    function qD(uint256 a,uint256 b) internal pure returns(uint256 m,int256 s){unchecked{
        uint256 n=(a<<110)/b;if(n*b!=a<<110)n|=1;
        (m,s)=qR(n);s-=110;
    }}
    // RN(RN(w)/1e18), w > 0: float(w)/1e18.
    function qW(uint256 w) internal pure returns(uint256 m,int256 e){unchecked{
        int256 s;(m,e)=qR(w);(m,s)=qD(m,LT_C);e+=s-7;
    }}
    // pw: wad paid; rx, ry: previous callback's reserve wads; fee: fee wad returned then for the paid side; buy: the pool bought X.
    // Outside pw in (0, 2^128), rx, ry in [2^40, 2^128) the answer is a miss.
    function qHitX(uint256 pw,uint256 rx,uint256 ry,uint256 fee,bool buy,int256 m0,uint256 nc) internal pure returns(bool,int256){unchecked{
        if(pw==0||pw>>128!=0||rx>>40==0||rx>>128!=0||ry>>40==0||ry>>128!=0)return(false,m0);
        uint256 G=ltGamma(fee>1e17?1e17:fee); // gamma = G*2^-53
        (uint256 pm,int256 pe)=qW(pw);
        (uint256 am,int256 ae)=qW(buy?ry:rx);(uint256 vm,int256 ve)=qW(buy?rx:ry); // v: paid-side reserve, grid = ulp(v) = 2^ve
        int256 s;
        (am,s)=qR(am*G);ae+=s-53;(am,s)=qR(am*vm);ae+=s+ve; // a = (u*gamma)*v
        s=((ae-57)&1)!=0?int256(58):int256(57);
        uint256 M=am<<uint256(s);ae=(ae-s)/2-1;
        uint256 q=1<<56;while(true){uint256 y=(q+M/q)>>1;if(y>=q)break;q=y;} // floor sqrt
        (am,s)=qR(q<<1|(q*q!=M?1:0));ae+=s; // sqrt(a)
        (am,s)=qD(am,QK);ae+=s-QKE; // r
        (am,s)=qR(am*QG);ae+=s+QGE; // r*0.997
        s=ae<-53?ae:-53;
        (uint256 dm,int256 de)=qR((G<<uint256(-53-s))+(am<<uint256(ae-s)));de+=s; // d = gamma + r*0.997
        for(uint256 i;i<nc;++i){int256 m=m0+(i==0?int256(0):i==1?int256(1):i==2?int256(-1):i==3?int256(2):int256(-2));uint256 dc=uint256(int256(dm)+m);(uint256 nm,int256 ns)=qR(pm*dc);ns+=pe+de-ve;if(ns<0){if(ns<-54)continue;nm=ltRound(nm,uint256(-ns));if(nm==0)continue;ns=0;}if(ltDivWad(nm,ns+ve-de-53,dc)==pw)return(true,m);}return(false,m0); // trunc(((n*grid)/d)*1e18) == paid wad
    }}
}
```
<!-- END QLX5 Strategy.sol -->

## Links

[R1]: https://api.imd.fun/artifacts/6e49ac8603cf53f5ad5f5cd15171566ee820fa707140592b70992360eb1c1799
[R2]: https://api.imd.fun/artifacts/7ee5203bc3dd1ce86a3c50e9310a0bb4d909eb95ec89de5fbe7ae55bca7132fa
[R3]: https://api.imd.fun/artifacts/9607fe6b57cca321e4fcc8005371a94d9d2964b3d7e87adbba3c69ceebba00bf
[CERT-A]: https://api.imd.fun/artifacts/0e7b77ee3947fe43bedef9f98e24715c61b35338a9f30d581ee084334d44e0a9
[CERT-B]: https://api.imd.fun/artifacts/d73c1749574cce67042552e9278be2ba20c8fedf9720bdee71c27d4019f21f02
[AGE-S]: https://api.imd.fun/artifacts/0343e8049294da6680c2ee1ad413fa5dc95843b1893e96c3b173df49b850b3e1
[AGE-E]: https://api.imd.fun/artifacts/87dfbac60f00625d53477537621d5d15b2b95529011ed061eab3bb64452d677c
[QLX-S]: https://api.imd.fun/artifacts/84a14d5edf847f83dfdd8f6a9c3e034a97004dcae6c069c11b4f6a2ffa7c517c
[QLX-A]: https://api.imd.fun/artifacts/8f25be1e7a92585f01095429712ee5b25435abb73a2756bc6d5b47ac58421e4a
[QLX-B]: https://api.imd.fun/artifacts/1ef80bfb6d6791b877b1f4048a5e63cf2ae54153e6e8763ae3f8ab13132dfb15
[LB4]: https://api.imd.fun/artifacts/93cc15561f172c49c8bce174143333ede904fdbfcf51276cbbeb514d4f5b614e
[TML]: https://api.imd.fun/artifacts/fd2f147e94f3523e4c4f91e43dc98b88e9ce8ef1060d2939367445711154a16a
[LEAN]: https://api.imd.fun/artifacts/a79a3606add967bb8f8ec2af8ef3d61bafb597419c488133597c8af5b9d34505
[DRIVER]: https://api.imd.fun/artifacts/764c9461a9f3bab6e277178f4bb48553d1b97c6cca33bed016f7c9bfd611cc42
[PRIOR]: https://github.com/Identity-md/research/blob/main/jobs/361fbb0e-7902-475b-bccf-67100e1c5fe6/files/artifacts/goal/writeup/report.md
[BOARD]: https://www.paradigm.xyz/puzzles/api/v1/leaderboard

Sources by role: lb-4 [LB4] (`a243bb35...`, 22,946 bytes, 49,905 characters, board 528.108759); TML [TML] (`99d031f4...`, 21,055 bytes, 40,615 characters, board 528.302452); LEAN [LEAN] (`a6dfc3ba...`, 21,368 bytes, 43,563 characters). Kit: `identity-md-launches/goal-3178-build-shared-evaluation-kit@45e7563d1a29ffca9d608fdf60c90bf2624d2d01`.
