# Learned fee policies for Paradigm's AMM fee challenge: goal write-up

Goal 42a76c8f (orchestrator seat), 10 episodes, 371 of 400 items spent across 29 batches. This document is written from the orchestrator's episode notes in `goal.json` and the five root merges handed for the write-up (`root-1-01` to `root-1-05`, SHA-256 in the Sources section). Every figure below is a worker's own local measurement as relayed by those merges, or a pooled figure recomputed here from the workers' `n`, `sum` and `sumsq`. Nothing was re-run for this write-up except hashing: the winning artifact was downloaded again from `api.imd.fun`, its file hash equals its id, and its `code_zb64` decodes to the SHA-256 stated below. The goal built no code repository: `trunk` in `goal.json` is empty, so there is no commit to name. Each candidate lives in its item's result artifact.

## 1. Outcome in one paragraph

The top 10 was not reached. The entry moved from 27th (RS2, board 520.05) to 20th (file IB, board 522.0013, submitted by the requester during the goal), and the best file in hand, J24, is confirmed about +1.0 over IB on fresh real-engine seeds, which puts it at roughly 523.0 against 523.82 for 11th and 524.66 for 10th. The top 10 needs about +2.66 over IB; J24 is about 1.66 short of that, or about 1.5 short on the goal's "+3.1 over HA" scale. Every line that paid did so by training longer from saved weights, and the replica predicted real gains within 0.02 to 0.1 at every step, as the pilot said it would. What did not pay: more inputs beyond the first six, unions of input sets, wider heads, gated heads, weight averaging, and joint searches that freed more than 41 of T's constants.

## 2. Best Strategy.sol: J24

- Item: `r7-t03-joint/j024` (round 7, merge 03). Artifact: https://api.imd.fun/artifacts/829f927c66461935528f22de289983a23fc27b162375853e8f19161a0bb644d5 (the file's SHA-256 is its id; re-downloaded and checked for this write-up).
- Contract code SHA-256: `226d20b7c388c4e70e8fa0a2c057ed81240a4f0bbd55f1c8443be456c7ea7a25` (27,700 bytes, `contract Strategy`, `getName()` returns `censored_10`). The artifact's `code_zb64` and the `best` block of root merge 5 both decode to this hash.
- Design: T's RS2 fee path plus a per-run toxicity anchor, a 19-8-2 fee-correction head (19 inputs in 1e6 fixed point, 8 clipped-ReLU units, two outputs added to the bid and ask fee in units of 1 bps, then clamped to [0, MAX_FEE]), with the head's 178 weights and 41 of T's constants trained jointly. The 19 inputs are HA's 13 (sigmaHat, lambdaHat, sizeHat, toxEma, actEma, direction, (spot-staleHat)/staleHat, signed trade ratio, arb probability, first-in-step, uncertainty, min(silent,8)/8, anchor mean) plus the six IA added (raw size, step trade count, previous bid fee, previous ask fee, steps since the last arb-like print, router-implied Vanilla spot deviation). Scaling is unchanged from CG. The `params` field of the artifact holds W1 (8x19), b1, W2 (2x8), b2, the 41 constants and the scaling.
- Training: CMA-ES (pycma) over 219 coordinates from T3's frozen params, weight step 0.03 x block rms, constants moved as c0 x 2^(0.02 z) with the exponent clipped to [-1, 1] (decays as 1-(1-d0) x 2^(0.02 z)), population 16, 512 fresh replica markets per generation from seed 1976000000, sigma0 1.0 capped at 0.5^(minutes/40), ES seed 824. 889 generations in 45.28 minutes at 3,780 replica markets/s (32 processes). Frozen at the final CMA mean (weights rounded to 1e-6, constants to WAD integers).
- Gates (all passed): A, T3 port vs T3 EVM fees on 50 recorded sequences of 2,000 callbacks (seeds 310000..310049), max 5.7e-5 bps; B, replica CG minus T on 7232768..7233279 = +1.920 se 0.044 against real +2.00 (within 0.15; this is the inherited CG calibration, see section 8); C, frozen Solidity vs frozen port, max 6.4e-5 bps.

### 2.1 Real-engine results for J24

Protocol: each strategy alone against the 30 bps VanillaStrategy, `amm_sim_rs.run_batch(X, VanillaStrategy, configs, 8)` in 64-seed chunks, configs per `MatchRunner._build_configs`, paired by seed.

| Pair | Seeds | n | mean diff | se | wins | worst 5 seeds (diff) |
|---|---|---|---|---|---|---|
| J24 minus T3, block 1 | 8792000..8793023 | 1,024 | +0.1849 | 0.0149 | 679 | 8792657 (-1.69), 8792456 (-1.40), 8792083 (-1.37), 8792216 (-1.26), 8792200 (-1.25) |
| J24 minus T3, block 2 | 8794000..8795023 | 1,024 | +0.1972 | 0.0150 | 692 | 8794465 (-2.20), 8794444 (-1.66), 8794219 (-1.44), 8794578 (-1.43), 8794664 (-1.35) |
| J24 minus T3, pooled | both | 2,048 | **+0.1910** | **0.0106** | 1,371 | as above |

Pooled from sum 391.254 and sumsq 542.144: 18 se above zero, confirmed on two fresh blocks of 1,024 (the requester's two confirmations, run on one machine). Retail and arb edge deltas are null in this item because `run_batch` exposes volumes, not an edge split; the replica holdout split is retail +0.149, arb +0.028 over T3. Volume deltas vs T3: retail -54 / -56 Y, arb -25 / -20 Y per market (blocks 1 / 2). Mean edges: candidate 533.49 vs T3 533.30 (block 1), 528.62 vs 528.42 (block 2).

Replica holdout (seeds 40000000..40008191, n 8,192, evaluated once after freezing): over T +2.710 se 0.0135; over T3 +0.177 se 0.0054. Monitor (30000000..30002047) over T: 2.585 at the start, 2.562 at 5 min, 2.604, 2.703, 2.702, 2.701, 2.748, 2.758, 2.762 at 45.3 min, still rising at the stop with sigma about 0.30.

Gas (`amm_sim_rs.gas_stats()`): afterSwap peak 235,471 (block 1) and **237,452** (block 2), limit 245,000; afterInitialize peak 243,234 (same as T3, unchanged code path); **0 OutOfGas**, 0 reverts, 0 other halts in 22.3 million candidate afterSwap calls.

### 2.2 J24 over HA and over T

J24 was never run on the same real seeds as HA or T; its item compared it with T3 only (the HA artifact returned HTTP 404 on that machine, which did not matter for its mode). The gains over HA and T are therefore chained across different fresh seed blocks, each link measured directly:

| Link | n (fresh real seeds) | mean | se | source |
|---|---|---|---|---|
| J24 minus T3 | 2,048 | +0.191 | 0.011 | r7-t03-joint/j024 |
| T3 minus IB | 3,776 | +0.805 | 0.014 | r7-t03-confirm c1..c4 (pooled here) |
| T3 minus HA | 3,776 | +1.448 | 0.016 | r7-t03-confirm c1..c4 (pooled here) |
| T3 minus HA | 85,288 | +1.420 | 0.003 | 88 real-only blocks of r7-t03-joint j021..j150 (pooled by root merge 5) |
| IB minus HA | 3,968 | +0.643 | 0.012 | r7-t03-confirm c1..c4 |
| IB minus HA | 9,216 | +0.652 | 0.007 | j5-a/b/c, j2-a/b, cf-a/b/c, ib-a (episode 9 pool) |
| HA minus T | 1,024 + 1,024 | +1.128, +1.120 | 0.026 | r2-confirm confirm-a/b; other fresh blocks 1.01 to 1.20 |
| HA minus T | 512 | +1.257 | 0.062 | goal statement (pilot block 6020000..6020511) |

So J24 is about **+1.61 to +1.64 over HA** (0.191 + 1.420 to 1.448) and about **+1.00 over IB**. Over T: about +2.75 to +2.90 on fresh real blocks (adding the measured HA minus T of 1.12 to 1.26), against the replica holdout's +2.710. These two chained figures are estimates, not paired measurements. Over T3 the worst seeds are listed above; over HA, T3's own worst seeds in the confirm items were single outliers of -8.6 to -36 (j029 8812677, j118 9168361) in blocks whose means stayed at +1.39 to +1.48.

### 2.3 Expected board place

Board as of the requester's note 6 (2026-11-09): IB 522.0013 (20th), 19th 522.05, 14th 522.40, 11th 523.82, 10th 524.66. Transfer from local gain to board score held within 0.05 for IB (local about +2.0 over RS2, board +1.95). Expected: T3 about 522.8 (12th to 14th), J24 about 523.0 (12th to 13th), about 0.8 below 11th and 1.66 below 10th. The requester's submission bar (confirmed >= +0.3 over IB on 2,048 fresh seeds) is met by J24 through T3 (J24 > T3 on 2,048, T3 > IB by +0.805 on 3,776) and directly by T3 and J5.

### 2.4 Fallback files

- **T3** = `r6-cg-joint-t/t03`, artifact https://api.imd.fun/artifacts/2333ecf28d4356bd232b85c1e55842e94e1ada05e1cd067830b5625dfdbc5336, code SHA-256 `cb6d945511e1e10af78baa64c2a6cb25806f0998403ce6440654bfc3c70092d9` (27,712 bytes): +0.805 se 0.014 over IB on 3,776 fresh seeds (blocks +0.784, +0.821, +0.820, +0.796) and +0.80 on 3,072 more (note 9), +1.448 over HA; afterSwap peak 237,689, init 243,234, 0 OOG in 41 million calls. T3 minus IB is even across retail-volume quartiles (+0.68 to +0.91); T3 minus HA rises with volume (Q1 about +1.2, Q4 about +1.6 to +1.8).
- **J5** = `r4-ib-joint/j5`, artifact `fe2320b5c091489337b3eb06bcbaea19bf4a8af09d959d67504ba63184f1dab6`, code `dd53db1fbe42628e040c6c7b7a82689867ab601263c5e740506299a3a186b38c`: +0.570 se 0.015 over IB on 3,072 fresh seeds, +1.222 over HA; peak 238,232, 0 OOG.
- **IB** (on the board) = `e2-ha-round1/inputs-b`, artifact `afd5183e9ff3235334e041c00b0cd19079599a2c6464db95f8c1586712105557`, code `301941829a44bb60977bb28181a5e4bfa6544f3696763f987054789b2611d686`.

### 2.5 The complete contract

Decoded from the artifact's `code_zb64`; SHA-256 of the text between the fences is `226d20b7c388c4e70e8fa0a2c057ed81240a4f0bbd55f1c8443be456c7ea7a25`. It imports the challenge repository's `AMMStrategyBase.sol` and `IAMMStrategy.sol` at commit `6b6921f8d463314aa7c96234e1be25a25245f704`.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {AMMStrategyBase} from "./AMMStrategyBase.sol";
import {TradeInfo} from "./IAMMStrategy.sol";

contract Strategy is AMMStrategyBase {
    uint256 constant ELAPSED_CAP = 7;
    uint256 constant SIGNAL_THRESHOLD = 1207883360604119;
    uint256 constant DIR_DECAY = 731359309089878272;
    uint256 constant ACT_DECAY = 414577356369668096;
    uint256 constant SIZE_DECAY = 529232927557566464;
    uint256 constant TOX_DECAY = 928709037506485248;
    uint256 constant SIGMA_DECAY = 703254383289366912;
    uint256 constant LAMBDA_DECAY = 992262990333512704;
    uint256 constant SIZE_BLEND_DECAY = 826367988226459520;
    uint256 constant TOX_BLEND_DECAY = 246917720219493312;
    uint256 constant ACT_BLEND_DECAY = 987953659006214272;
    uint256 constant PHAT_ALPHA = 248344316747393024;
    uint256 constant PHAT_ALPHA_RETAIL = 53200239248891392;
    uint256 constant PHAT_ALPHA_SAME = 136225884814527552;
    uint256 constant REVERT_U = 0;
    uint256 constant DIR_IMPACT_MULT = 4;
    uint256 constant GATE_SIGMA_MULT = 6323258321481004032;
    uint256 constant MIN_GATE = 29836286994856604;
    uint256 constant TRADE_TOX_BOOST = 237883143513038048;
    uint256 constant STALE_ATTRACT_FRAC = 712506613612537856;
    uint256 constant RET_CAP = 20836850395478756;
    uint256 constant TOX_CAP = 218399766296251552;
    uint256 constant TRADE_RATIO_CAP = 163221858095291424;
    uint256 constant LAMBDA_CAP = 1120951150619335040;
    uint256 constant STEP_COUNT_CAP = 66;
    uint256 constant BASE_FEE = 364519583294980;
    uint256 constant SIGMA_COEF = 200595304912634752;
    uint256 constant LAMBDA_COEF = 1325819502431104;
    uint256 constant FLOW_SIZE_COEF = 465459061821990656;
    uint256 constant TOX_COEF = 31585249424377932;
    uint256 constant TOX_QUAD_COEF = 1687069465601069312;
    uint256 constant ACT_COEF = 8930758579064809472;
    uint256 constant DIR_COEF = 2055106615282290;
    uint256 constant DIR_TOX_COEF = 7003657154136395;
    uint256 constant STALE_DIR_COEF = 746228901977979264;
    uint256 constant SIGMA_TOX_COEF = 60808045096652952;
    uint256 constant TAIL_KNEE = 61405344140246432;
    uint256 constant TAIL_SLOPE_PROTECT = 849716177499675648;
    uint256 constant TAIL_SLOPE_ATTRACT = 824873345164924672;

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
            if (sampleCount < 756) sampleCount++;
            if (toxEma >= runMean) runMean += (toxEma-runMean)/sampleCount;
            else runMean -= (runMean-toxEma)/sampleCount;
            slots[16] = runMean | (sampleCount << 64);
            toxLinear = _anchorBlend(runMean, toxEma, 773297010117480960);
            toxQuadratic = _anchorBlend(runMean, toxEma, 1039779796564214144);
        }


        stepTradeCount = stepTradeCount + 1;
        if (stepTradeCount > STEP_COUNT_CAP) stepTradeCount = STEP_COUNT_CAP;

        uint256 originalLambda = lambdaHat; uint256 originalSize = sizeHat;
        int256[19] memory nx;

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
            {
                uint256 la = packedFlow >> 240;
                uint256 sn = trade.timestamp - la; if (sn > 32) sn = 32;
                nx[17] = int256(sn * WAD);
                if (firstInStep && arbProbability > 500000000000000000) la = trade.timestamp;
                slots[15]=rate | (count << 80) | (meanSize << 160) | (la << 240);
            }
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
                nx[13] = trade.reserveY > 0 ? int256(wdiv(trade.amountY, trade.reserveY)) : int256(0);
                nx[14] = int256(stepTradeCount * WAD);
                nx[15] = int256(prevBidFee);
                nx[16] = int256(prevAskFee);
                nx[18] = (int256(trade.isBuy ? wdiv(wmul(spot, gamma), WAD - 30 * BPS) : wdiv(wmul(spot, WAD - 30 * BPS), gamma)) - int256(nh)) * 1e18 / int256(nh);
                nx[13] = nx[13] * 647054817 / 1e18 + (-618293);
                nx[14] = nx[14] * 1395287 / 1e18 + (-2037262);
                nx[15] = nx[15] * 220617911 / 1e18 + (-803057);
                nx[16] = nx[16] * 228148131 / 1e18 + (-808615);
                nx[17] = nx[17] * 412565 / 1e18 + (-823811);
                nx[18] = nx[18] * 274335453 / 1e18 + (1772);
                for (uint256 ni=0;ni<19;ni++) {
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



    function _head(int256[19] memory x) internal pure returns (int256 b,int256 a) {
        unchecked {
            b = 1287868000000; a = 2979361000000;
            int256 z;
            z = 1984133 + ((249826 * x[0]) + (323701 * x[1]) + (-332967 * x[2]) + (2762324 * x[3]) + (-2353991 * x[4]) + (424153 * x[5]) + (-1328463 * x[6]) + (2533555 * x[7]) + (-5024596 * x[8]) + (-1551135 * x[9]) + (-911372 * x[10]) + (440517 * x[11]) + (505858 * x[12]) + (-2238548 * x[13]) + (-217040 * x[14]) + (-814892 * x[15]) + (-1338393 * x[16]) + (-361956 * x[17]) + (1475329 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (301525 * z); a += (691969 * z);
            z = -1437820 + ((803786 * x[0]) + (957388 * x[1]) + (2093172 * x[2]) + (2748433 * x[3]) + (-133784 * x[4]) + (-187525 * x[5]) + (-340574 * x[6]) + (241472 * x[7]) + (-247469 * x[8]) + (36611 * x[9]) + (-70689 * x[10]) + (-1272845 * x[11]) + (-69697 * x[12]) + (30097 * x[13]) + (-223803 * x[14]) + (715967 * x[15]) + (221316 * x[16]) + (-12580 * x[17]) + (857289 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-1950288 * z); a += (-1534645 * z);
            z = -3525094 + ((420422 * x[0]) + (3958800 * x[1]) + (-1288583 * x[2]) + (530511 * x[3]) + (1201236 * x[4]) + (2347051 * x[5]) + (-1286586 * x[6]) + (883741 * x[7]) + (556815 * x[8]) + (-341257 * x[9]) + (325027 * x[10]) + (-30235 * x[11]) + (183590 * x[12]) + (580943 * x[13]) + (139585 * x[14]) + (836732 * x[15]) + (-3090374 * x[16]) + (-132328 * x[17]) + (-2965527 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (1487011 * z); a += (-1791242 * z);
            z = -201381 + ((226500 * x[0]) + (-1010257 * x[1]) + (1053765 * x[2]) + (-452356 * x[3]) + (-477484 * x[4]) + (493809 * x[5]) + (743164 * x[6]) + (-428776 * x[7]) + (695613 * x[8]) + (-247334 * x[9]) + (16302 * x[10]) + (-2335395 * x[11]) + (250796 * x[12]) + (731134 * x[13]) + (105307 * x[14]) + (-1608775 * x[15]) + (1208568 * x[16]) + (-411687 * x[17]) + (-1323658 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-765540 * z); a += (3280020 * z);
            z = -2203571 + ((1312964 * x[0]) + (565926 * x[1]) + (4394728 * x[2]) + (9190 * x[3]) + (-2179355 * x[4]) + (-915025 * x[5]) + (-1330540 * x[6]) + (-417759 * x[7]) + (-367499 * x[8]) + (416126 * x[9]) + (-152720 * x[10]) + (-2589276 * x[11]) + (223496 * x[12]) + (-934374 * x[13]) + (183449 * x[14]) + (-892020 * x[15]) + (2277461 * x[16]) + (32989 * x[17]) + (514387 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-2697103 * z); a += (-162077 * z);
            z = -2699666 + ((1490975 * x[0]) + (-1966124 * x[1]) + (568637 * x[2]) + (-1222799 * x[3]) + (3553697 * x[4]) + (1431720 * x[5]) + (3671675 * x[6]) + (1007801 * x[7]) + (-449369 * x[8]) + (2309 * x[9]) + (71799 * x[10]) + (3971645 * x[11]) + (673235 * x[12]) + (-1382863 * x[13]) + (320984 * x[14]) + (109350 * x[15]) + (-1302385 * x[16]) + (-486331 * x[17]) + (-1399253 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-743049 * z); a += (-2096325 * z);
            z = -490161 + ((-528427 * x[0]) + (1587087 * x[1]) + (590052 * x[2]) + (-515887 * x[3]) + (2638251 * x[4]) + (907594 * x[5]) + (-785145 * x[6]) + (2794075 * x[7]) + (1380856 * x[8]) + (-1776323 * x[9]) + (1152475 * x[10]) + (1441066 * x[11]) + (1228102 * x[12]) + (-964254 * x[13]) + (-1253082 * x[14]) + (-1657448 * x[15]) + (910916 * x[16]) + (-682301 * x[17]) + (2443875 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-1217138 * z); a += (855714 * z);
            z = -39825 + ((-2329801 * x[0]) + (-2768515 * x[1]) + (3971862 * x[2]) + (3753315 * x[3]) + (-65711 * x[4]) + (-638795 * x[5]) + (-1736210 * x[6]) + (2981103 * x[7]) + (355119 * x[8]) + (-893119 * x[9]) + (2569282 * x[10]) + (-1688518 * x[11]) + (1493543 * x[12]) + (277654 * x[13]) + (620367 * x[14]) + (1388380 * x[15]) + (4897 * x[16]) + (-1492740 * x[17]) + (793315 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (823607 * z); a += (-182773 * z);
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

## 3. Lineage of files

All gains are paired real-engine differences on fresh seeds unless marked holdout (replica, seeds 40000000..40008191, n 8,192). "Over base" is over the file each was trained from.

| File | Item | Code SHA-256 | What changed | Real gain | Holdout over T |
|---|---|---|---|---|---|
| T | pilot | `ebd9de9b...19b3` | RS2 + toxicity anchor | board 520.05 (RS2) | 0 |
| HA | pilot head-a | `99e3a2ec...90fe` | + 13-8-2 head | +1.257 se 0.062 over T (512); fresh blocks 1.01 to 1.20 | 1.117 |
| IA | e2-ha-round1/inputs-a | `956566e9...cf2` | 19 inputs (+6), 210 gens | +0.359 se 0.013 over HA (2,048) | 1.482 |
| FA | leg1/feat-a | `aa2c4a56...728` | 19 inputs (T's own fees, prev fees, (spot-pHat)/pHat, retail flow rate), 512 gens | +0.572 se 0.016 over HA (2,048) | 1.681 |
| IB | e2-ha-round1/inputs-b | `30194182...686` | IA's six inputs, own scaling, 910 gens at 6,000 markets/s | +0.643 to +0.652 over HA (3,968 / 9,216); board 522.00, 20th | 1.769 |
| CG | r2-continue-x/continue-g | `e1ea8fcb...04b` | IA's head continued, pop 32, 1,039 gens, 77 min | +0.180 se 0.012 over IB (3,072); +0.827 over HA | 1.952 |
| J2 | r4-ib-joint/j2 | `4da9e3ae...964` | IB's head + 41 T constants jointly, 327 gens | +0.501 se 0.017 over IB (1,984) | 2.275 |
| J5 | r4-ib-joint/j5 | `dd53db1f...38c` | IA's head + 41 T constants jointly, 1,496 gens at 5,264 markets/s | +0.570 se 0.015 over IB (3,072); +1.222 over HA | 2.308 |
| T3 | r6-cg-joint-t/t03 | `cb6d9455...2d9` | CG's head + 41 T constants from T's values, 1,598 gens, 55 min | +0.805 se 0.014 over IB (3,776); +1.448 over HA | 2.533 |
| J24 | r7-t03-joint/j024 | `226d20b7...a25` | T3 continued jointly, 889 gens, 45 min at 3,780 markets/s | +0.191 se 0.011 over T3 (2,048) | 2.710 |

One holdout scale ties them together: over IB = over T - 1.769 = over HA - 0.652 (HA minus T 1.117 and IB minus T 1.769 on the holdout, identical in every port).

## 4. Each line: training curves and real results

### 4.1 Weights-only continuation of HA's 13-input head

- leg1/net8-a: 231 generations in 54 min; monitor 1.231 to 1.258 over T in the last 30 min, "near a plateau" (sigma 0.029). Real +0.096 se 0.019 over HA; holdout +0.104.
- e2-ha-round1/continue-a: 424 gens in 45 min: +0.194 se 0.021 over HA; holdout +0.185. Peak 231,484.
- leg1/th-a: HA's 130 weights plus 38 T constants and the anchor, 265 gens in 70 min at 326 markets/s: +0.370 se 0.031 over HA (retail -0.58, arb +0.95), still rising. First evidence that constants add on the arbitrage side.
- Verdict: the 13-input head saturates near +0.1 to +0.2 over HA; constants on top of it gave +0.37.

### 4.2 Added inputs (the first big step)

- IA (inputs-a): +0.335 se 0.025 over HA on 512 seeds after only 21 min and 210 gens, still rising; confirmed +0.394 se 0.019 and +0.325 se 0.018 on two blocks of 1,024 (pooled +0.359 se 0.013; 787 and 759 wins of 1,024); peaks 235,490 and 237,631, 0 OOG. Retail +0.6, arb -0.23.
- IB (inputs-b): same six inputs, own scaling, 910 gens in 21 min at about 6,000 markets/s (22 processes): +0.592 se 0.030 over HA (512), holdout +0.652; confirmed at +0.628 se 0.023 (ib-a, 1,024), +0.655 (c1, 2,592), +0.626 (c4, 512), and +0.643 se 0.012 on 3,968 in round 7. Monitor still rising at generation 890 of 910 (1.810 over T, sigma 0.022). Submitted: board 522.0013, 20th. Training compute was the lever: IB's 7.45 million market evaluations against IA's 0.5 million gave +0.26 more.
- FA (feat-a): six different added inputs, 512 gens in 56 min at 925 markets/s: +0.569 se 0.029 over HA (512), monitor 1.15 -> 1.44 (25 min) -> 1.70 (46) -> 1.73 (51), rising. Confirmed +0.569 se 0.024 and +0.575 se 0.020 on two blocks of 1,024 (pooled +0.572 se 0.016). Retail +0.49, arb +0.08. Per evaluation FA's inputs did slightly better than IB's; on the holdout IB is 0.088 above FA.
- One more input family on IA (r2-inputs2, 512 seeds, over IA): flow +0.322 se 0.031 (holdout +0.341, best of them, mostly arb +0.52), cross-products +0.238, fees +0.156, path +0.119 (peak 243,585, too close to the limit), clock not run. Flow and cross came close to a plain long continuation of IA (continue-g +0.507) but no better.
- Unions (23 inputs: IB's 19 + FA's four, or FA's 19 + IA's four): fu-b +0.112 se 0.017 over FA (holdout +0.076), fu-c -0.013 (gate C unfinished, invalid), u1 +0.060 se 0.016 over IB, u3 +0.005, u4 +0.051 (holdout +0.024 to +0.056). Dead: the four extra columns earned small weights and no gain over continuing the base.
- Verdict: the first six added inputs bought +0.36 to +0.65 over HA; the next six bought nothing beyond long training.

### 4.3 Long weights-only training of the 19-input head

Round 2 continuations of IA (512 seeds, over IA; holdout in brackets): continue-g pop 32, 1,039 gens, 77 min: +0.507 se 0.024 [+0.470], retail +0.17, arb +0.33, monitor still rising (0.81 at gen 780, 0.85 at 990); continue-h pop 32 diagonal, 507 gens: +0.378 [+0.384]; continue-a 750 gens: +0.319 [+0.332], plateau from gen 490; continue-f 590 gens: +0.247 [+0.272]; continue-d 210 gens: +0.223 [+0.220]; continue-c (Darwin, no real run) 3,520 gens of pop 16: [+0.420], flat from about gen 2,300 at sigma 0.031. Population 32 beat 16 at equal wall-clock.

Round 4 continuations of IB (over IB): c3 pop 32, 868 gens in 45 min at 5,400 markets/s: +0.209 se 0.023 [+0.192], monitor 1.810 -> 1.992 over T, fluctuating late; c2 (1,024 markets/gen, 62 gens): +0.011 [+0.010]; r4-ib-wide w01 (605 gens) [+0.106], real +0.087; w17 (299 gens, 1,024 markets/gen) [+0.112], real +0.102; w16 [+0.074], real +0.091; the other 16 wide items trained 66 to 367 generations or not at all and gained +0.03 to +0.06 or nothing. c5 (224 gens at 363 markets/s) never recovered its start and returned IB.

FA continuations (over FA): f2 513 gens at 1,373 markets/s: +0.136 se 0.022 [+0.170], monitor 1.729 -> 1.897; f5 211 gens: +0.060; f4 68 gens: +0.028.

Round 5 continuations of CG (over CG): k01 pop 32, 1,276 gens in 42 min at 2,246 markets/s: +0.115 se 0.018 [+0.110]; k26 1,762 gens in 58 min: +0.093 se 0.016 [+0.077], "still trending up"; k24 501 gens: +0.046; everything else +0.00 to +0.02, with k11 flat after gen 730 and k27 noting "CG looks close to a local optimum". Model soups of CG with its sisters (r5-cg-soup m1): every mixing point negative (CG+S1 at t=1: -0.025), then 331 gens of CMA: +0.011 se 0.008.

Verdict: weights alone give +0.2 to +0.5 per round from a fresh head and +0.05 to +0.1 per round once the head has been trained for about 1,000 generations. The gain tracks generations: nothing under 500 generations moved more than +0.06.

### 4.4 Structural changes (none paid)

- Width: wide-a 16 units from HA, 16 min: +0.073; gas-a's 12-unit head on the diet (191 gens): +0.016 se 0.022; on IA's diet 12 units (r2 wide-a) +0.157, 16 units (wide-b, wide-c) +0.088 and +0.129 over IA, each below plain continuation at equal compute. The diets themselves (gas-a: 16 live storage words to 8; kit-b IAD; kit-c IBD) reproduced the base fees exactly on 100 regression seeds and 256 to 512 fresh seeds and cut the afterSwap peak from about 237k to 131k to 132k (init 243k to 177k), so gas stopped binding; width still did not pay. No trained candidate was shipped on a diet.
- Gating (two heads chosen by first-in-step or by side): gated-a +0.192 over HA (leg 1), +0.170, +0.101, +0.066 over IA (round 2; gated-c plateaued after gen 140 and has a -27.6 tail seed). Below plain continuation.
- Pilot head-b (12 units without a diet) ran out of gas (62 OOG calls); its 6-unit fallback peaked 245,690: the hard limit is real for the undieted shell.

### 4.5 T's constants trained jointly with the head (the second big step)

- Constants alone: const-a (33 constants in log scale, IA's head fixed, 348 gens): +0.231 se 0.034 over IA [+0.238], retail -0.78, arb +1.01; r5-cg-joint q10 (33 constants, CG head fixed, 374 gens): +0.171 se 0.030 over CG [+0.176]; q04 +0.163, q03 +0.149, q02 +0.167, q08 +0.135. A line scan from CG's constants toward const-a's peaks at t = 0.75 with +0.109 on the monitor.
- Joint with too many degrees of freedom fails: joint-a (167 dims from HA) never beat HA on the monitor (-0.8 to -4.5); j1, j3, j4 (81 to 83 TH entries from IB, structural ones included) fell to -0.8, -6.0 and -3.4 over T at once and returned IB unchanged. Searching exactly the 41 declared constants of `params.constants` works.
- J2 (IB's head + 41 constants, pop 32, 327 gens in 56 min at 1,565 markets/s): monitor 1.810 -> 2.310 over T, still rising at the stop; +0.578 se 0.055 over IB (512) [+0.505]; confirmed +0.499 and +0.504 on two blocks (pooled +0.501 se 0.017, n 1,984); +1.18 over HA. Retail volume down, arb up.
- J5 (IA's head + 41 constants, pop 16, 1,496 gens in 41 min at 5,264 markets/s): monitor 1.540 -> 2.357 over T, rising; +0.876 se 0.035 over IA (512) [+0.826]; confirmed +0.559, +0.551, +0.600 over IB on three blocks of 1,024 (pooled +0.570 se 0.015), +1.213 to +1.235 over HA; arb +0.96, retail -0.08. Peak 238,232.
- Both J2 and J5 moved TOX_BLEND_DECAY from 0.051 to 0.25 to 0.29; J24 has it at 0.247.
- T3 (CG's head + 41 constants started at T's values, pop 16, 512 markets/gen, 1,598 gens in 55 min at 1,358 markets/s): monitor rose at every 5-minute check, 2.002 -> 2.150 (5 min) -> 2.327 (20) -> 2.430 (30) -> 2.530 (45) -> 2.585 (55), sigma 1.0 -> 0.27; holdout +0.581 se 0.008 over CG, 2.533 over T; real +0.819 se 0.060 over IB (one seed at +55.7; +0.765 se 0.026 without it), then +0.805 on 3,776 and +0.80 on 3,072. Its batch mates t02 (92 gens) and t07 (248 gens) reached +0.24 and +0.25 over CG on the holdout, so the gain tracked generations here too.
- Continuing a joint-trained point: from J5 (r6-j5-joint, 50 items), k15 at 1,225 gens in 75 min: +0.116 over J5 on the holdout, +0.668 se 0.025 over IB real, curve still rising; everything under 300 gens +0.02 to +0.03. From J2 (r6-j2-joint, 20 items): +0.016 to +0.027 on the holdout, real indistinguishable from J2 (p04 +0.003 se 0.016 vs J2 directly). From T3 (r7-t03-joint, 150 items): see 4.6.

### 4.6 Round 7: continuing T3 (150 items)

Of 150 items, 41 searched (replica at or above 500 markets/s), 104 ran real-only T3-versus-HA blocks (slow machines), 5 were blocked at setup (Darwin arm64 or a proxy). 37 searches were valid. Candidate minus T3, real pooled on two fresh blocks of 1,024 unless noted (holdout over T3 in brackets):

| Item | markets/s | gens | min | real over T3 (se) | peak | code SHA-256 |
|---|---|---|---|---|---|---|
| j024 | 3,780 | 889 | 45.3 | **+0.191 (0.011)** [+0.177] | 237,452 | `226d20b7...a25` |
| j116 | 4,791 | 1,585 | 45.0 | +0.149 (0.011) [+0.146] | 238,255 | `a4a71517cdea07042fa2b79387280832d21c3e0a36ae6c574e8d88bd5fdc88b1` |
| j003 | 1,430 | 708 | 56.0 | +0.150 (0.011) [+0.128] | 237,620 | `9386b3d1b0e09fc376db314a9105a8facdf8646b5c19723702635fbb8408266d` |
| j008 | 2,601 | 1,581 | 48.5 | +0.145 (0.011) [+0.122] | 238,108 | `1d97c3cabc56293ad49459c3513a5739dacce604de2270952517c5aabfb365ff` |
| j002 | 1,510 | 634 | 55.1 | +0.116 (0.010) [+0.128] | 238,228 | `5758f1fbbdc71c8f56469d89d9ea183f282b83456c805382f6ab7a2f63c89d8c` |
| j030 | 981 | 895 | 45.1 | +0.123 (0.016), one block [+0.152] | 237,433 | `5a6bfdd94cdbc7cc4ff704f3a82aa099220a369a7cc2663061a1e415801b6257` |
| j021 | 675 | 507 | 51.3 | +0.093 (0.010) [+0.078] | 237,709 | `1d779c09e46e8cd9564de9ac8533901329e230382b2326e31296a47c449e96cd` |
| j107 | 946 | 319 | 52.2 | +0.062 (0.015) [+0.028] | 238,094 | |
| j011 | 984 | 479 | 57.2 | +0.052 (0.008) [+0.052] | 237,733 | `67f6e1a239b0896dafc9ff26415c7677b1c53de3f4d97e4d321fc7291afb63bf` |
| j041, j063, j136, j061, j082, j111, j147 | 635 to 1,500 | 158 to 379 | 45 to 56 | +0.034 to +0.047 | 237,464 to 238,338 | |
| 19 more valid searches | 509 to 1,491 | 15 to 295 | 27 to 56 | +0.003 to +0.029 | all under 238,500 | |

The gain is a function of generations: about +0.15 to +0.19 per 900 to 1,600 generations from T3, +0.05 to +0.09 per 500, and under +0.05 below 400. Items at 512 to 1,024 markets per generation on machines under about 1,500 markets/s report flat curves; j116 (pop 32, 256 markets/gen, 24-process pool) was "still rising" at 45 min (2.585 -> 2.730 on the monitor) and j024's best monitored point was its last. j050 (holdout +0.026, real -0.374 se 0.007) ran a simulator built from source on macOS rather than the pinned wheel and must not be used; j022 and j145 failed gate C (2.3 and 1.1 bps at a fee-routing threshold); j095 returned T3 unchanged; j036 lost 256 observations. Every candidate had 0 OOG. Candidates traded slightly less volume than T3; j116 slightly more.

The 104 real-only items gave T3 minus HA on 85,288 paired fresh seeds: +1.420 se 0.003 (Cochran's Q 94.5 on 87 df, so the blocks agree); full blocks range +1.354 to +1.500. Reconstructed splits: T3 over HA retail about +0.74 to +0.83, arb about +0.64 to +0.68; T3 over IB retail -0.16 to -0.23, arb +0.98 to +1.03; IB over HA retail +0.96 to +1.02, arb -0.34.

## 5. Which designs kept climbing

| Line | Curve at the stop | Real gain per round |
|---|---|---|
| 13-input head, weights only | plateau by 230 to 420 gens (net8-a, continue-a) | +0.1 to +0.2 over HA, once |
| 19-input head, weights only, fresh | rising through 1,000 gens with pop 32 (continue-g, c3); flat after 2,300 gens with pop 16 (continue-c) | +0.2 to +0.5 over the base |
| 19-input head, weights only, already trained | flat or +0.05 to +0.1 per 1,200 to 1,800 gens (k01, k26); soup nothing | +0.05 to +0.1 |
| Constants only (33 to 41) | rising, saturating near +0.17 to +0.24 | +0.17 to +0.24 |
| Head + 41 constants, first time | rising at every check (J2, J5, T3); T3 +0.58 over CG at 1,598 gens | +0.5 to +0.8 |
| Head + 41 constants, continued | rising on the fast long runs (j024, j116, k15), flat on short or slow ones | +0.1 to +0.19 per 900 to 1,600 gens |
| Head + 82 constants or more | collapses at once | nothing |
| More inputs, unions, width, gating | below plain continuation at equal compute | 0 to +0.1 |

Every step that mattered came from training longer on a fast machine from the best frozen params: IB over IA (910 vs 210 gens), CG over its sisters (pop 32, 1,039 gens), J5 and T3 (1,500 to 1,600 gens), J24 and j116 (900 to 1,600 gens at 3,800 to 4,800 markets/s). About a third of the network's machines reach 500 replica markets/s and one in ten 1,300 or more; the one machine at 6,000 markets/s produced IB.

## 6. Replica versus real agreement

Holdout prediction (n 8,192) against the real paired gain over the same base on fresh seeds:

| Candidate | base | replica | real | gap |
|---|---|---|---|---|
| IA | HA | +0.365 | +0.335 / +0.359 (2,048) | 0.01 to 0.03 |
| IB | HA | +0.652 | +0.592 / +0.628 / +0.643 | 0.01 to 0.06 |
| FA | HA | +0.564 | +0.569 / +0.572 | 0.01 |
| continue-g, -h, -a, -d, -f, gated-a(r2) | IA | +0.470, +0.384, +0.332, +0.220, +0.272, +0.164 | +0.507, +0.378, +0.319, +0.223, +0.247, +0.170 | at most 0.04 |
| inputs-flow | IA | +0.341 | +0.322 | 0.02 |
| c3 | IB | +0.192 | +0.209 | 0.02 |
| J5 | IA | +0.826 | +0.876 | 0.05 |
| J2 | IB | +0.505 | +0.578 (512) / +0.501 (1,984) | 0.07 / 0.00 |
| CG | IB | +0.183 | +0.180 (3,072) | 0.00 |
| k26, k01 | CG | +0.077, +0.110 | +0.093, +0.115 | 0.02 |
| q10, q04 | CG | +0.176, +0.158 | +0.171, +0.163 | 0.01 |
| T3 | IB | +0.764 (via the holdout scale) | +0.805 (3,776) | 0.04 |
| J24, j116, j003, j008, j002, j011 | T3 | +0.177, +0.146, +0.128, +0.122, +0.128, +0.052 | +0.191, +0.149, +0.150, +0.145, +0.116, +0.052 | at most 0.03 |

The replica called every real gain within 0.01 to 0.07, inside the pilot's 0.1 and the gates' 0.15. The only large miss, j050 (+0.026 predicted, -0.374 real), used an unpinned engine. The base level HA minus T is the one place where the replica and the goal text disagree: fresh real blocks of 512 to 1,024 seeds gave 1.01 to 1.20 (large blocks 1.12 to 1.15), the replica gives 1.12 to 1.14, and the goal's 1.257 came from one favourable block, so the goal's "+3.1 over HA" target is anchored about 0.1 high.

## 7. Gas

All valid candidates: 0 OOG. afterSwap peaks: T about 223k to 226k, HA 228k to 234k, IA and IB 235k to 238.5k, CG 235.5k to 238.4k, J5 237.4k to 238.2k, T3 232.5k to 238.5k, J24 235.5k to 237.5k, the highest trained candidate anywhere k35 at 239,076 and inputs-path at 243,585. afterInitialize peaks 243,115 (T) to 243,327 (gated): under 245,000 but close, and the brief's limit names afterSwap. The diets leave about 110k of afterSwap headroom; no shipped candidate uses one. The only OOG in the goal's history is the pilot's undieted 12-unit head.

## 8. Caveats a judge should know

- **Gate B for T3 and its children is inherited.** Every T3-line item reports B as replica CG minus T on 7232768..7233279 (+1.920 vs real +2.00). No item ran a fresh real T3 minus T, so "the replica reproduces the start file's real gain over T within 0.15" was shown for CG, not for T3. The nearest evidence is the candidate-minus-T3 transfer (within 0.03) and the chained real T3 minus T of about 2.68 against the replica's 2.53 to 2.55, at the edge of 0.15 and built on the goal's HA figure.
- **J24 was never paired with HA, IB or T on real seeds.** Its gains over them are chained (section 2.2).
- **Division-by-zero panics under synthetic stress.** Many items found a Solidity Panic 0x12 in CG-, J2-, J5- and T3-family code under unbounded synthetic callback sequences (a recurring case is seed 310037, callback 1424, reserve_x about 0.118, a drained pool at spot about 2e8). None occurred on the real engine in about 100 million afterSwap calls, and none is an OOG. The requester's note 9 asked for gate A on recorded replica sequences for this reason. It is a robustness caveat for the submitted file.
- **T3's initial fee tripped the KIT decomposition.** T3 starts at BASE_FEE (394715277459523 wei-scaled), not 4 bps; c1 to c3 lost T3's first 64 seeds to an assertion and marked themselves invalid rather than re-run; c4 re-ran that chunk and marked itself valid. Edges were unaffected; only 3,776 of the planned 4,096 confirm pairs exist.
- **Retail and arb splits** are reconstructions (arb from the constant-product pre-arb state, retail = edge - arb; reconstruction error about 1e-4) where given, and Y-volume deltas where the item says so. The two must not be mixed.
- **Validity flags are inconsistent across items** for re-run or partial chunks (c4, j031, j056, j125 valid; c1 to c3, j023, j053, j060 invalid for the same kind of event). Nothing was selected on a re-run chunk.
- **Sources flags.** The plane's `sources` check flagged nearly every accepted result (for example 48 of 50 in r6-j5-joint, 17 of 20 in r4-ib-wide) without naming a page. The flagged claims are artifact provenance and quoted references (Gate B targets, the 1.769 holdout offset); the measured edges, paired statistics and gas are each item's own local runs and do not rest on a quoted page.
- **The requester's HA minus T of +1.257** sits above every fresh block measured in this goal (1.01 to 1.20).
- **Platform losses.** About one item in eight landed on a Darwin arm64 host where the pinned Linux wheel or the uv binary cannot run (fu-a, ib-b, f1, w10, k14, k34, k40, t05, t08, j025, j034, j089, j144, continue-c's real run among them); one item was denied downloads; one was a path_violation (r5-cg-continue/k10). No item failed for any other reason. Slow machines (under 200 or 500 markets/s by batch) ran confirmations instead of searches: 104 of 150 in round 7.
- **Seed ledger.** Fresh real seeds ran from 7000000 upward, one block per item, never reused for a decision: leg 1 7000000..7017511; round 1 7100000..7136863; round 2 7200000..7302399; round 3 7310000..7399999; round 4 7500000..7696511; CG confirms 7400000..7421023; round 5 8000000..8169023; round 6 7800000..7841023 and 8300000..8617023; round 7 8700000..9297023 and 9500000..9531023. Gas probes touched a few 16-seed ranges inside earlier blocks (noted by root merge 1); no confirmation figure used them. Monitor 30000000..30002047 and holdout 40000000..40008191 were never trained on but were shared by every item, so holdout ranks are selection, and real blocks are the evidence.

## 9. What the next run should try

1. **Continue J24 jointly on the fastest machines only.** The gain per round scales with generations: budget 2,000 to 4,000 generations per item (90 minutes at 3,000 markets/s or more, segmented under 8 minutes with CMA state saved), population 16 to 32, 256 to 512 markets per generation, sigma restarted at 0.5 to 1.0 in T3's coordinates with the 40-minute half-life. Give machines under 1,500 markets/s confirmations, not searches. Expect +0.15 to +0.2 per such round; 11th needs about +0.8 more over J24 and 10th about +1.66.
2. **Carry the CMA state, not only the mean.** Every continuation restarted from a frozen mean with a fresh covariance and lost the first 5 to 10 minutes re-widening (j024's monitor dipped at 5 min). Ship `scratch/` CMA pickles as an artifact field and resume from them.
3. **Measure J24 directly against IB and HA** on two fresh blocks of 1,024, plus a real T3 minus T calibration, so the ladder has paired links and gate B is fresh for the T3 line.
4. **Try the second joint step from a different head.** T3's +0.58 over CG came from training T's constants for the first time on a good head; J5 got +0.83 over IA the same way. j116 (IB-independent lineage within the T3 line) and k15 (J5 continued) are the other long-trained points; a joint continuation from k15's params at 2,000+ generations is the one untested comparison.
5. **Put a trained candidate on the diet** (kit-c's IBD emitter; general port and emitter for any input set) before trying anything that costs gas: learned memory (two values the head writes and reads back next trade) was never run because a new storage slot costs about 22k at first write against 7k to 10k of undieted headroom.
6. **Bound the drained-pool case** in the shell (guard the divisions that panic at reserve_x near zero) before submitting, and re-run gate C.
7. **Do not spend items on** more input families, unions, width, gating, weight soups, or joint searches over more than the 41 declared constants: twelve to twenty items each returned nothing beyond plain continuation.

## 10. What is missing

- No top-10 result. The best confirmed file is about 1.66 short over IB (about 1.5 over HA).
- No real-engine pairing of J24 with IB, HA or T; no fresh real T3 minus T.
- No retail/arb edge split for J24 on the real engine (volumes only); the replica split is retail +0.149, arb +0.028 over T3.
- No submission of T3, J5 or J24 by the goal itself; the requester submits. IB is the only file known to be on the board.
- A complete 4 x 1,024 confirmation of T3 does not exist (3,776 pairs).
- The r5-cg-continue, r6-j5-joint and r7-t03-joint items each returned only their own best; the weights of the runner-up continuations are in their artifacts (`rows[].result_sha256` in each merge) and were not pooled into a soup, which did nothing when tried on CG.

## 11. Sources

Handed root merges (file SHA-256 as given by the plane):
- root-1-01 `b6dd2e79264257329e8100877f31b583ae78924f55855697d1854cb0ccb9b7f6`: leg1, e2-ha-round1, r2-confirm, r2-continue, r2-continue-x, r2-gated/gated-a (25 results).
- root-1-02 `b68ec9212df0b291c5f85ce05c3abf1e0ea2fcf8f08839eaa7101093219fd010`: r2-gated, r2-diet-wide, r2-joint, r2-kit, r2-inputs2, r3-fa-union, r4-confirm, r4-ib-continue c1..c4 (25).
- root-1-03 `dd7d1e7548decea9ba069b0c82eaf492988cc531b10ad723d0876f11dbb6fbe9`: r4-ib-continue c5, r4-ib-wide merges 01..04, r4-ib-union, r4-ib-joint j1..j5, r4-fa-continue, r4-ib-kit, r5-cg-confirm, r5-cg-continue merges 01..02 (25).
- root-1-04 `71c52f6282a44cb0d11b8da1ef410d1c680c6f9439428cd8c0fbf6fea787b087`: r5-cg-continue merges 03..06, r5-cg-joint, r5-cg-soup, r6-confirm, r6-j5-joint, r6-j2-joint, r6-cg-joint-t, r7-t03-joint merges 01..02 (25).
- root-1-05 `c15748ad4d88b4d0522ae9e6f23cf8cf3158e59d0ed9e5be2f2790f49b4f467a`: r7-t03-joint merges 03..15 and r7-t03-confirm c1..c4 (17).

Artifacts named in this report (id = file SHA-256 at `https://api.imd.fun/artifacts/<id>`): HA `2801efc8190e86318dd922d4a7179f63684d77a226047fc2f3c78232963eb690`; T `6ac5e013b7b1fb4c5e7bdcdfec0aba28b16824e18ccf39500f258533879faffe`; replica `e8a7a2af9039c24b8bb2d3b5fa1c9113606cbf5a480ac07d02ca26750f1752ea` (`replica_source` `1e4c44b4...040c`); RS2 port `d845a4b94eab87f23956fd1939c0135d955df212d1f3037f2a761c178cef7a0e`; KIT `0d8194e9f6e0017dc4e515cdb04c048efc292935bb1d18e3336091fe81154786`; KB `48cd6a10f39fc22a79c5f12398474bd65282803d59314819acd586f187015808`; kit-c `71695e4eb1e3c194637eafe539ddf967f9e1a27f2f7f6690fb86a6e373f1d706`; IA `df0ddfdf122c88641513dd179980fce475f42a912a184f812d213f27db7c14df`; IB `afd5183e9ff3235334e041c00b0cd19079599a2c6464db95f8c1586712105557`; FA `d3bff2aae5d832c494baf42f463dd674ab63c084734a435ea6d204d0b6176e28`; CG `ebbd90c663c396598965b23341aea97a4501b4c971db183a8fe94a880f399979`; J2 `4d396adc0e3056c010e59ab8c3d413eb0380a14e8cefa6cd825e809fa2494999`; J5 `fe2320b5c091489337b3eb06bcbaea19bf4a8af09d959d67504ba63184f1dab6`; T3 `2333ecf28d4356bd232b85c1e55842e94e1ada05e1cd067830b5625dfdbc5336`; J24 `829f927c66461935528f22de289983a23fc27b162375853e8f19161a0bb644d5`; j116 `edb467cbe3b57f2a8c91d57d50729d98ee07a1f5b8adfe683916a1cc923f09b9`. Challenge repository commit `6b6921f8d463314aa7c96234e1be25a25245f704`; simulator wheel SHA-256 `aedb68280aca34c110968f00148387c95885207913fb2cf19a1ab4c5cfd6887a`.
