# Relay training of the IB fee policy for paradigm.xyz/puzzles/amm: final report

Goal f04f2a47. Ten episodes, 45 batches, 193 of 200 items used. The goal built no code repository (`trunk` is null in goal.json); every result is a worker's JSON or a merge, content-addressed at `https://api.imd.fun/artifacts/<sha256 of its bytes>`.

Every performance figure below is a local measurement by the item named next to it, on the pinned engine (`github.com/benedictbrady/amm-challenge` at `6b6921f8d463314aa7c96234e1be25a25245f704`, wheel `aedb6828…`), each strategy alone against the 30 bps VanillaStrategy through `amm_sim_rs.run_batch(X, VanillaStrategy, configs, 8)` with configs per `MatchRunner._build_configs`, paired by seed. None is a leaderboard score. Do not add any delta to the board's 522.00.

## 1. The deliverable: k01

**File:** `https://api.imd.fun/artifacts/12606d82ec57ee9fe351945ec520b1ab8d79c8a472ff46b3bce6c5c0693b7b49` (result of item `t3-a/k01-s05-h45-p16`; fetched again while writing this report, the bytes hash to that id). Its `code_zb64` is the Solidity below, `params` holds the weights (also reproduced in §1.3), `port_zb64` its float port.

| field | value |
|---|---|
| Solidity SHA-256 (`Strategy.sol`, 27,710 bytes, 515 lines) | `9253b6f3a49eafc1ed21ad19d9e2c0761c2ff151a6a7aa81e16de83834ad6a1b` |
| port SHA-256 | `732c0fb615480020795039a111e4a49a46f851e6f29720b092665b247d79006b` |
| contract | `Strategy is AMMStrategyBase`, `getName()` = `censored_10`, `pragma solidity ^0.8.24` |
| design | T's fee engine (41 constants, searched) plus a 19-8-2 ReLU head on IA's 19 inputs; T03's Solidity with only numeric literals changed |
| parents | T03 (`cb6d9455…`, requester's sister-goal file) ← continue-g (IG, `e1ea8fcb…`) ← IA ← HA ← T |

### 1.1 Paired real-engine gain over IB on fresh seeds (confirmation batch `confirm-k01`, items k01-c1..c6)

Six independent items, each 512 fresh seeds (8174080..8177151, never used before), three arms each (IB, k01, T03), 64-seed commands, `gas_stats()` per arm. Pooled here from the items' `n`, `sum`, `sumsq` (sample variance; identical to the merge in root-1-07).

| comparison | n | mean_diff | se | per-block means |
|---|---|---|---|---|
| **k01 − IB** | **3,072** | **+0.8221** | **0.0163** | +0.757, +0.826, +0.816, +0.847, +0.841, +0.847 |
| k01 − T03 (same seeds) | 3,072 | +0.0678 | 0.0086 | +0.037, +0.057, +0.086, +0.077, +0.066, +0.085 |
| T03 − IB (same seeds) | 3,072 | +0.7543 | 0.0158 | +0.720, +0.769, +0.730, +0.770, +0.775, +0.762 |

k01 beats IB by about 50 se and T03 by about 8 se. This satisfies the requester's rule (> 2 se over IB on two fresh 1,024 blocks, >= +0.3 on >= 2,048 seeds), so k01 is the file the requester may submit.

Worst five and best five seeds of k01 − IB across the 3,072:

| worst5 | diff | best5 | diff |
|---|---|---|---|
| 8175538 | −3.055 | 8176213 | +11.460 |
| 8175543 | −2.835 | 8174145 | +10.692 |
| 8174161 | −2.534 | 8175552 | +6.742 |
| 8174340 | −2.495 | 8176731 | +6.351 |
| 8174709 | −2.482 | 8176476 | +6.284 |

Medians per block: +0.782, +0.764, +0.801, +0.818, +0.796, +0.813. In k01-c1, 429 of 512 seeds were positive.

By quartile of IB's retail volume (q1 quietest; pooled over the six items, 768 seeds each; se from the within-item se only):

| quartile | k01 − IB | se |
|---|---|---|
| q1 | +0.764 | 0.025 |
| q2 | +0.794 | 0.029 |
| q3 | +0.816 | 0.033 |
| q4 | +0.914 | 0.041 |

The gain is present in every quartile and largest in the busiest markets (requester note 2 had found IB weakest there).

**Retail/arb deltas.** The Rust result exposes edge, PnL and retail/arb volumes, not a retail/arb edge split, so every item reports volume deltas (Y units per market, k01 − IB): retail +340 / arb −67 (k01-c1), retail +320 se 15 / arb −73 se 10 (k01-c2). PnL delta +0.814 (c1). On the replica, which does split edge, k01's gain over IB is retail −0.385 / arb +1.219 (k01's holdout, n 8,192) and its gain over T03 is retail −0.148 / arb +0.214: the relay's gains since J5 came from arbitrage, retail flat or slightly negative.

**Gas and validity (every arm of every confirmation item):** 0 OOG, 0 reverts, 0 other halts, 0 tx errors, 0 bad returns, about 5.5 M afterSwap calls per arm per item. afterSwap peak of k01 per item: 237,594; 235,550; 235,423; 238,102; 235,739; 238,271 (IB on the same seeds 234,872..237,699; T03 235,417..238,289). Highest k01 peak 238,271, under the 245,000 limit by 6,729. afterInitialize peak 243,234. `valid` true in all six.

**Gain over HA.** No item of this goal ran HA. The chain is: k01 − IB = +0.822 se 0.016 (n 3,072, above) and IB − HA = +0.5916 se 0.030 (n 512, seeds 7132768..7133279, measured in the IB file `afd5183e…`, the requester's sister goal). Chained, k01 is about **+1.41 over HA** (combined se about 0.034), but the two legs are on different seeds, so it is not one paired figure. IB's file also gives IB − T = +1.749 se 0.040 on the same 512 seeds, so k01 is about +2.57 over T.

**Gates on k01 (from its own result):** gate A (port vs Solidity in the EVM, 50 × 2,000 callbacks) 3.7e-5 bps; gate B (replica T03 − IB on seeds 8588000..8589023, n 1,024) +0.769 se 0.027 against the real +0.819, error 0.050; gate C (frozen Solidity vs frozen port) 4.5e-5 bps. Later legs that started from k01 replayed recorded replica callbacks (seeds 9200000..9200049) against this Solidity at 6.0e-5 bps.

### 1.2 Strategy.sol (complete; SHA-256 `9253b6f3a49eafc1ed21ad19d9e2c0761c2ff151a6a7aa81e16de83834ad6a1b`)

The file imports `AMMStrategyBase.sol` and `IAMMStrategy.sol` from the pinned amm-challenge checkout (`contracts/src/`), as every entry in this lineage does.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {AMMStrategyBase} from "./AMMStrategyBase.sol";
import {TradeInfo} from "./IAMMStrategy.sol";

contract Strategy is AMMStrategyBase {
    uint256 constant ELAPSED_CAP = 7;
    uint256 constant SIGNAL_THRESHOLD = 1160146365492428;
    uint256 constant DIR_DECAY = 742579053110605312;
    uint256 constant ACT_DECAY = 362712919377395584;
    uint256 constant SIZE_DECAY = 514571880561315392;
    uint256 constant TOX_DECAY = 931334186146359040;
    uint256 constant SIGMA_DECAY = 735879907203958144;
    uint256 constant LAMBDA_DECAY = 992016217861851008;
    uint256 constant SIZE_BLEND_DECAY = 838916715724297856;
    uint256 constant TOX_BLEND_DECAY = 265113898351673984;
    uint256 constant ACT_BLEND_DECAY = 987130525530773888;
    uint256 constant PHAT_ALPHA = 250673916396877568;
    uint256 constant PHAT_ALPHA_RETAIL = 52025768623387664;
    uint256 constant PHAT_ALPHA_SAME = 143281931423379616;
    uint256 constant REVERT_U = 0;
    uint256 constant DIR_IMPACT_MULT = 4;
    uint256 constant GATE_SIGMA_MULT = 6396576222177718272;
    uint256 constant MIN_GATE = 29155056358021496;
    uint256 constant TRADE_TOX_BOOST = 287294577866444352;
    uint256 constant STALE_ATTRACT_FRAC = 692135649965966080;
    uint256 constant RET_CAP = 20704982534600448;
    uint256 constant TOX_CAP = 205698869865359840;
    uint256 constant TRADE_RATIO_CAP = 187708703942247328;
    uint256 constant LAMBDA_CAP = 1052565576926734336;
    uint256 constant STEP_COUNT_CAP = 64;
    uint256 constant BASE_FEE = 377247866990593;
    uint256 constant SIGMA_COEF = 205181214702057184;
    uint256 constant LAMBDA_COEF = 1292768640037444;
    uint256 constant FLOW_SIZE_COEF = 537269336057038656;
    uint256 constant TOX_COEF = 30724614186944084;
    uint256 constant TOX_QUAD_COEF = 1585589899856466432;
    uint256 constant ACT_COEF = 8367736522524027904;
    uint256 constant DIR_COEF = 1911778676094586;
    uint256 constant DIR_TOX_COEF = 8207843377267543;
    uint256 constant STALE_DIR_COEF = 754499253378701312;
    uint256 constant SIGMA_TOX_COEF = 59198091468550328;
    uint256 constant TAIL_KNEE = 56230542131989352;
    uint256 constant TAIL_SLOPE_PROTECT = 836628982188679936;
    uint256 constant TAIL_SLOPE_ATTRACT = 841263793374813952;

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
            if (sampleCount < 713) sampleCount++;
            if (toxEma >= runMean) runMean += (toxEma-runMean)/sampleCount;
            else runMean -= (runMean-toxEma)/sampleCount;
            slots[16] = runMean | (sampleCount << 64);
            toxLinear = _anchorBlend(runMean, toxEma, 648060424979456256);
            toxQuadratic = _anchorBlend(runMean, toxEma, 1102036062554150528);
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
            b = 1560235000000; a = 2820259000000;
            int256 z;
            z = 2258205 + ((-176997 * x[0]) + (759913 * x[1]) + (-607316 * x[2]) + (3064729 * x[3]) + (-2397445 * x[4]) + (490413 * x[5]) + (-1463102 * x[6]) + (2532234 * x[7]) + (-5334064 * x[8]) + (-1922200 * x[9]) + (-694299 * x[10]) + (-511010 * x[11]) + (409336 * x[12]) + (-2319113 * x[13]) + (-616024 * x[14]) + (-560712 * x[15]) + (-1108771 * x[16]) + (-76860 * x[17]) + (1689767 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (53395 * z); a += (493688 * z);
            z = -1688267 + ((749403 * x[0]) + (927639 * x[1]) + (1920145 * x[2]) + (2598310 * x[3]) + (-154325 * x[4]) + (-185428 * x[5]) + (-413339 * x[6]) + (430805 * x[7]) + (-345349 * x[8]) + (119308 * x[9]) + (-59679 * x[10]) + (-1768258 * x[11]) + (56022 * x[12]) + (-182701 * x[13]) + (-173974 * x[14]) + (894270 * x[15]) + (260072 * x[16]) + (67068 * x[17]) + (977048 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-2047954 * z); a += (-1938963 * z);
            z = -4067462 + ((877318 * x[0]) + (3793499 * x[1]) + (-1312105 * x[2]) + (843833 * x[3]) + (937328 * x[4]) + (2120865 * x[5]) + (-1612858 * x[6]) + (934500 * x[7]) + (1403904 * x[8]) + (-774995 * x[9]) + (583354 * x[10]) + (108677 * x[11]) + (-87352 * x[12]) + (323193 * x[13]) + (161516 * x[14]) + (1065185 * x[15]) + (-2552558 * x[16]) + (-437531 * x[17]) + (-2551197 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (1103189 * z); a += (-1782929 * z);
            z = -877852 + ((247895 * x[0]) + (-1520508 * x[1]) + (992764 * x[2]) + (-226949 * x[3]) + (-1169068 * x[4]) + (-552887 * x[5]) + (137885 * x[6]) + (-124757 * x[7]) + (636913 * x[8]) + (156567 * x[9]) + (198623 * x[10]) + (-1581699 * x[11]) + (-390313 * x[12]) + (359219 * x[13]) + (168015 * x[14]) + (-1109885 * x[15]) + (1018385 * x[16]) + (-243261 * x[17]) + (-965612 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-600331 * z); a += (3655466 * z);
            z = -1168667 + ((1045192 * x[0]) + (674658 * x[1]) + (4754701 * x[2]) + (-124304 * x[3]) + (-2206268 * x[4]) + (-1296372 * x[5]) + (-1005856 * x[6]) + (-726684 * x[7]) + (-409844 * x[8]) + (609799 * x[9]) + (25742 * x[10]) + (-2346546 * x[11]) + (-161326 * x[12]) + (-1195896 * x[13]) + (343508 * x[14]) + (-750284 * x[15]) + (2256378 * x[16]) + (-26349 * x[17]) + (625686 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-3128621 * z); a += (340409 * z);
            z = -2427504 + ((1361898 * x[0]) + (-2076545 * x[1]) + (167834 * x[2]) + (-1482120 * x[3]) + (3964198 * x[4]) + (1373475 * x[5]) + (3837027 * x[6]) + (649171 * x[7]) + (-484219 * x[8]) + (-56199 * x[9]) + (-8882 * x[10]) + (3387515 * x[11]) + (688338 * x[12]) + (-1078445 * x[13]) + (176220 * x[14]) + (328940 * x[15]) + (-1789160 * x[16]) + (-302653 * x[17]) + (-1568467 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-763904 * z); a += (-1896285 * z);
            z = -725963 + ((-673286 * x[0]) + (1149198 * x[1]) + (124468 * x[2]) + (-739598 * x[3]) + (2688452 * x[4]) + (822718 * x[5]) + (-1301634 * x[6]) + (2340034 * x[7]) + (1372744 * x[8]) + (-1535532 * x[9]) + (1149279 * x[10]) + (1021293 * x[11]) + (1539016 * x[12]) + (-970707 * x[13]) + (-924040 * x[14]) + (-1580181 * x[15]) + (666772 * x[16]) + (-764222 * x[17]) + (2839311 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (-831052 * z); a += (955570 * z);
            z = 200219 + ((-2515823 * x[0]) + (-2942958 * x[1]) + (3462455 * x[2]) + (3773968 * x[3]) + (-9852 * x[4]) + (-1002908 * x[5]) + (-1521680 * x[6]) + (2533901 * x[7]) + (364276 * x[8]) + (-1060362 * x[9]) + (2573698 * x[10]) + (-2046107 * x[11]) + (1401962 * x[12]) + (18048 * x[13]) + (413046 * x[14]) + (939239 * x[15]) + (-272336 * x[16]) + (-1950012 * x[17]) + (1164793 * x[18]))/1000000;
            if(z<0) z=0; else if(z>4000000) z=4000000;
            b += (684382 * z); a += (-320510 * z);
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

### 1.3 The weights (`params` of the k01 file)

W1 is 8 × 19 (row = hidden unit, column = input in `scaling.feature_order`), b1 8, W2 2 × 8 (bid, ask), b2 2; the 41 constants are T's, searched jointly; `scaling` is IA's input scaling, unchanged since continue-g. In the Solidity the head weights are integer literals at 1e-6 in `_head` (for example b1[0] = 2258205 and W1[0][0] = -176997 on line 348) and the constants are the WAD `uint256 constant` literals at the top (`constants_wad` in the file).

```json
{
 "W1": [
  [
   -0.176997,
   0.759913,
   -0.607316,
   3.064729,
   -2.397445,
   0.490413,
   -1.463102,
   2.532234,
   -5.334064,
   -1.9222,
   -0.694299,
   -0.51101,
   0.409336,
   -2.319113,
   -0.616024,
   -0.560712,
   -1.108771,
   -0.07686,
   1.689767
  ],
  [
   0.749403,
   0.927639,
   1.920145,
   2.59831,
   -0.154325,
   -0.185428,
   -0.413339,
   0.430805,
   -0.345349,
   0.119308,
   -0.059679,
   -1.768258,
   0.056022,
   -0.182701,
   -0.173974,
   0.89427,
   0.260072,
   0.067068,
   0.977048
  ],
  [
   0.877318,
   3.793499,
   -1.312105,
   0.843833,
   0.937328,
   2.120865,
   -1.612858,
   0.9345,
   1.403904,
   -0.774995,
   0.583354,
   0.108677,
   -0.087352,
   0.323193,
   0.161516,
   1.065185,
   -2.552558,
   -0.437531,
   -2.551197
  ],
  [
   0.247895,
   -1.520508,
   0.992764,
   -0.226949,
   -1.169068,
   -0.552887,
   0.137885,
   -0.124757,
   0.636913,
   0.156567,
   0.198623,
   -1.581699,
   -0.390313,
   0.359219,
   0.168015,
   -1.109885,
   1.018385,
   -0.243261,
   -0.965612
  ],
  [
   1.045192,
   0.674658,
   4.754701,
   -0.124304,
   -2.206268,
   -1.296372,
   -1.005856,
   -0.726684,
   -0.409844,
   0.609799,
   0.025742,
   -2.346546,
   -0.161326,
   -1.195896,
   0.343508,
   -0.750284,
   2.256378,
   -0.026349,
   0.625686
  ],
  [
   1.361898,
   -2.076545,
   0.167834,
   -1.48212,
   3.964198,
   1.373475,
   3.837027,
   0.649171,
   -0.484219,
   -0.056199,
   -0.008882,
   3.387515,
   0.688338,
   -1.078445,
   0.17622,
   0.32894,
   -1.78916,
   -0.302653,
   -1.568467
  ],
  [
   -0.673286,
   1.149198,
   0.124468,
   -0.739598,
   2.688452,
   0.822718,
   -1.301634,
   2.340034,
   1.372744,
   -1.535532,
   1.149279,
   1.021293,
   1.539016,
   -0.970707,
   -0.92404,
   -1.580181,
   0.666772,
   -0.764222,
   2.839311
  ],
  [
   -2.515823,
   -2.942958,
   3.462455,
   3.773968,
   -0.009852,
   -1.002908,
   -1.52168,
   2.533901,
   0.364276,
   -1.060362,
   2.573698,
   -2.046107,
   1.401962,
   0.018048,
   0.413046,
   0.939239,
   -0.272336,
   -1.950012,
   1.164793
  ]
 ],
 "b1": [
  2.258205,
  -1.688267,
  -4.067462,
  -0.877852,
  -1.168667,
  -2.427504,
  -0.725963,
  0.200219
 ],
 "W2": [
  [
   0.053395,
   -2.047954,
   1.103189,
   -0.600331,
   -3.128621,
   -0.763904,
   -0.831052,
   0.684382
  ],
  [
   0.493688,
   -1.938963,
   -1.782929,
   3.655466,
   0.340409,
   -1.896285,
   0.95557,
   -0.32051
  ]
 ],
 "b2": [
  1.560235,
  2.820259
 ],
 "constants": {
  "ELAPSED_CAP": 7,
  "SIGNAL_THRESHOLD": 0.001160146365492428,
  "DIR_DECAY": 0.7425790531106053,
  "ACT_DECAY": 0.3627129193773956,
  "SIZE_DECAY": 0.5145718805613154,
  "TOX_DECAY": 0.931334186146359,
  "SIGMA_DECAY": 0.7358799072039581,
  "LAMBDA_DECAY": 0.992016217861851,
  "SIZE_BLEND_DECAY": 0.8389167157242978,
  "TOX_BLEND_DECAY": 0.265113898351674,
  "ACT_BLEND_DECAY": 0.9871305255307739,
  "PHAT_ALPHA": 0.2506739163968776,
  "PHAT_ALPHA_RETAIL": 0.05202576862338766,
  "PHAT_ALPHA_SAME": 0.1432819314233796,
  "DIR_IMPACT_MULT": 4,
  "GATE_SIGMA_MULT": 6.3965762221777185,
  "MIN_GATE": 0.029155056358021497,
  "TRADE_TOX_BOOST": 0.28729457786644436,
  "STALE_ATTRACT_FRAC": 0.6921356499659661,
  "RET_CAP": 0.020704982534600447,
  "TOX_CAP": 0.20569886986535985,
  "TRADE_RATIO_CAP": 0.18770870394224734,
  "LAMBDA_CAP": 1.0525655769267344,
  "STEP_COUNT_CAP": 64,
  "BASE_FEE": 0.000377247866990593,
  "SIGMA_COEF": 0.2051812147020572,
  "LAMBDA_COEF": 0.001292768640037444,
  "FLOW_SIZE_COEF": 0.5372693360570386,
  "TOX_COEF": 0.030724614186944083,
  "TOX_QUAD_COEF": 1.5855898998564664,
  "ACT_COEF": 8.367736522524028,
  "DIR_COEF": 0.001911778676094586,
  "DIR_TOX_COEF": 0.008207843377267543,
  "STALE_DIR_COEF": 0.7544992533787013,
  "SIGMA_TOX_COEF": 0.059198091468550325,
  "TAIL_KNEE": 0.05623054213198935,
  "TAIL_SLOPE_PROTECT": 0.83662898218868,
  "TAIL_SLOPE_ATTRACT": 0.8412637933748139,
  "ANCHOR_COUNT_CAP": 713,
  "ANCHOR_LINEAR_K": 0.6480604249794563,
  "ANCHOR_QUADRATIC_K": 1.1020360625541505
 },
 "scaling": {
  "feature_order": [
   "sigmaHat",
   "lambdaHat",
   "sizeHat",
   "toxEma",
   "actEma",
   "direction",
   "(spot-staleHat)/staleHat",
   "signed_trade_ratio",
   "arb_probability",
   "first_in_step",
   "uncertainty",
   "min(silent,8)/8",
   "anchor_mean",
   "raw_size",
   "step_trade_count",
   "prev_bid_fee",
   "prev_ask_fee",
   "steps_since_arb_like_print",
   "router_implied_vanilla_spot_dev"
  ],
  "feature_multipliers": [
   1000.0,
   2.0,
   500.0,
   500.0,
   500.0,
   1.0,
   500.0,
   500.0,
   2.0,
   2.0,
   1000000.0,
   1.0,
   500.0,
   647.054817,
   1.395287,
   220.617911,
   228.148131,
   0.412565,
   274.335453
  ],
  "feature_offsets": [
   -1.0,
   -1.0,
   -1.0,
   -1.0,
   -1.0,
   -1.0,
   0.0,
   0.0,
   -1.0,
   -1.0,
   -1.0,
   0.0,
   -1.0,
   -0.618293,
   -2.037262,
   -0.803057,
   -0.808615,
   -0.823811,
   0.001772
  ],
  "weight_fixed_point_scale": 1000000,
  "input_clip": [
   -4,
   4
  ],
  "hidden_relu_clip": [
   0,
   4
  ],
  "output_unit_fee": 0.0001,
  "note": "unchanged from CG"
 }
}
```

## 2. The best trained file of the last round: q22 (confirmed on 512 real seeds only)

`t6-e/q22-k06-s03-h60-p16`, `https://api.imd.fun/artifacts/8cbbcd23417da9dc12595527212316c61f922c56d60bbfbdfe7b65d61488c91a` (handed as b45-q22-k06-s03-h60-p16; 39,853 bytes; code SHA-256 `97e538c7302a6d5af28db53408595358ce4fb1085714232110c295c032e2c993`, port `4c2c3549cba6539a3a1b89baf76e107d0da57a713c8c8e3eeabcf35b50503f36`; `params`, `code_zb64`, `port_zb64` inside). START = k06 (`e7b20742…`, code `ef01fb90…`), a sibling of k01 from T03.

- Search: 32 CPUs, 3,557 replica markets/s, 1,371 generations in 66.6 minutes, population 16, sigma0 0.3 capped at 0.3·0.5^(min/60), weights = start + 0.05·rms(block)·z, constants = start·2^(0.03 z) with every `*_DECAY` and `PHAT_ALPHA*` capped at 0.999 (TOX_DECAY and LAMBDA_DECAY sit at the cap), M 512 fresh markets per generation (train seeds 268000000..268701951, ES seed 20261622). Monitor over START (seeds 30000000..30002047): −0.017 at 5 min, +0.003 at 15, +0.029 at 35, +0.043 at 45, +0.061 at gen 1,358 (65 min), still rising when it stopped 35-40 minutes before the time limit.
- Gates: A 6.2e-5 bps and C 6.7e-5 bps on recorded replica callbacks; B replica k06 − IB +0.846 against the real +0.792 (error 0.054).
- Replica holdout 41090000..41098191 (n 8,192, once): +0.0498 se 0.0048 over k06 (retail −0.614 / arb +0.663), **+0.895 se 0.010 over IB** (highest of all 22 round-5 legs on this shared holdout; k01 sits at +0.848, k07 +0.841, k06 +0.845 on the same seeds).
- Real engine, seeds 8199680..8200191 (n 512): **+0.911 se 0.043 over IB** (quartiles +0.80 / +0.94 / +0.91 / +0.99; worst5 8199971 −2.02, 8200084 −1.25, 8200060 −0.86, 8199933 −0.76, 8200102 −0.74), +0.059 se 0.023 over k06 (2.6 se); k06 − IB +0.852 on the same seeds. Mean edges: IB 529.45, k06 530.30, q22 530.36. Volume deltas q22 − IB: retail +249, arb −125 Y.
- Gas: afterSwap peak 237,613 (IB 237,052, k06 237,608), 0 OOG, 0 reverts in 5.57 M calls; valid.

q22 was never paired with k01 on the real engine. On the shared holdout it is +0.047 ahead of k01 (0.895 vs 0.848, se about 0.005 for the paired difference against the same IB arm, though the two policies were not differenced seed by seed in one item). Recommendation: confirm q22 against IB **and k01** on 2,048 fresh seeds from 8200704 (never used) before submitting it; until then k01 is the confirmed deliverable.

Other round-5 legs that beat their START (all valid, 0 OOG, peaks 235k..238k, holdout 41090000..+8191 shared):

| leg (START) | id | gens, speed | holdout vs START | holdout vs IB | real vs IB (n 512) | real vs START |
|---|---|---|---|---|---|---|
| q04 (k01), macOS replica-only | `5922e652…` | 1,114, 1,887/s | +0.045 se 0.005 | +0.893 | not run (no Solidity, no EVM, no gas) | — |
| q14 (k01) | `c05bc26a…`, code `7bc0171f…` | 573, 1,304/s, pop 24 | +0.042 se 0.005 | +0.890 | +0.866 se 0.037 (8191488..) | +0.029 se 0.022 |
| q21 (k06) | `711657aa…`, code `c4805881…` | 397, 347/s | +0.032 se 0.004 | +0.878 | +0.889 se 0.039 (8198656..) | START arm not run |
| q13 (k01) | `89d4f522…`, code `08ec8003…` | 300, 431/s | +0.026 se 0.005 | +0.874 | +0.899 se 0.034 (8190464..) | +0.037 se 0.019 |
| q01 (k01) | root-1-07 | 322, 550/s | +0.021 se 0.004 | +0.869 | +0.800 | −0.006 se 0.016 |
| q10 (k01) | root-1-08 | 142, 202/s | −0.002 | +0.846 | +0.844 (n 256) | −0.039 se 0.020: do not use |

The other 15 round-5 legs returned START unchanged (nothing beat it on the monitor) after 68..322 generations on seats at 0..590 markets/s; their START arms add fresh START − IB blocks: k01 +0.74..+0.92 (pooled over q01..q15 START arms n 3,584: +0.855 se 0.014 per root-1-08; with the confirmation, +0.821 se 0.012 on 5,440 seeds per root-1-07), k07 +0.77..+0.90, k06 +0.77..+0.82.

A second confirmed file: **k07** (`t3-b/k07-s03-h60-p16`, id `9212fa7fbc3dae90d9d0eda9cb22972790431d4128339db1cc55754ddbfc73c3`, code `039fa1a3fcab7d33a03457284bdb8858beea581eaddcd904631e8c0d91855608`, port `cdf8c0f8…`): confirm-k01 items k07-c1, k07-c2 on 8177152..8178175, n 1,024: +0.884 se 0.049 over IB (block c2 holds one +43.5 seed, 8177832; its se is 0.091), +0.073 se 0.015 over T03; T03 − IB +0.810 on the same seeds; peaks 237,455 / 237,691, 0 OOG. k07 and k01 were never paired; their gains over T03 (+0.073 vs +0.068) are indistinguishable. k01 has the larger confirmation.

## 3. How the relay worked

- **One leg = one item**, about 75 minutes of search on whatever seat the network gave it (2 to 32 CPUs, 44 to 3,557 replica markets/s). A leg fetched START (a content-addressed JSON with `code_zb64`, `params`, `port_zb64`), checked hashes, ran gates A and B and a speed test, searched, froze the best monitored point into START's Solidity by replacing literals only, ran gate C, scored the frozen file once on a replica holdout shared by the round (frozen, START and IB arms), and once on the real engine on a fresh 512-seed block (IB and frozen, START when time remained, 64-seed commands, gas per arm). Its result JSON was shaped like START so the next round could start from it by URL (a brief holds 3,000 characters, never the weights).
- **Search:** CMA-ES (pycma), population 16 (24 in a few legs), fitness = mean edge on the same M fresh replica markets per generation (512 at >= 300 markets/s, 256 below), seeds never reused (ledger in §8), the ES mean scored every 5 minutes on monitor seeds 30000000..30002047 (reused on purpose, selection only), best monitored point kept, sigma capped at sigma0·0.5^(minutes/half-life). From round 3 on, every search was **joint**: 219 coordinates, the 178 head weights (start + c·rms(block)·z) plus 41 of T's constants (start·2^(k z), integers rounded), as requester note 4 asked; c, k were 0.05, 0.03 in round 3 (J5 and IG legs), 0.03, 0.02 in round 4 (k01, k06, k07) and 0.05, 0.03 in rounds 5 and 6.
- **Promotion:** the requester's rule, confirm the best leg against IB on two fresh 1,024-seed blocks, promote at > 2 se, continue from the promoted weights plus the next two best; frozen `params` only, never an ES-state vector.
- **Seats:** results came back on Linux x86_64 seats of every size and on macOS arm64 seats (where the Linux wheel cannot run). Seats under 100 markets/s ran confirmations instead of searching (requester note 3); macOS seats ran the search replica-only from note 6 on (q04), earlier they blocked.

## 4. Lineage round by round

Batons given by the requester (sister goal cc45e1a7), with the gains they arrived with; the rounds of this goal follow. "Real" is paired on the real engine; "holdout" is the replica once after freezing. Minutes are search minutes.

### 4.0 Starting files (requester's measurements, sister goal)

| file | id (code sha) | what | gain |
|---|---|---|---|
| IB (board entry 522.00, 20th) | `afd5183e…` (`30194182…`) | T + 19-8-2 head on HA's 13 inputs plus 6 newer; 910 CMA gens in 20.8 min on 22 processes | +0.592 se 0.030 over HA, +1.749 over T (n 512, 7132768..); afterSwap 234,849 |
| IA | `df0ddfdf…` | inputs-a design, 200 gens | +0.335 over HA, about 0.26 behind IB |
| IC = continue-h | `a97fa964…` (`01e3b53a…`) | IA continued 507 gens | +0.378 se 0.024 over IA; our confirm-ic: +0.061 se 0.021 and +0.076 se 0.021 over IB (n 1,024 each) |
| IG = continue-g | `ebbd90c6…` (`e1ea8fcb…`) | IA continued 1,030 gens at 892 markets/s | +0.507 se 0.024 over IA; +0.19 over IB on 5,120 seeds (note 5); our ig-joint START arms: +0.13..+0.19 per 512-seed block, holdout +0.183 se 0.008 |
| J5 | `fe2320b5…` (`dd53db1f…`) | IA's head + 41 of T's constants jointly, 1,496 gens in 41 min on 32 processes | +0.876 over IA, +0.55 se 0.01 over IB on 5,120 seeds (note 5); our j09: +0.562 se 0.030 (n 1,024) |
| T03 | `2333ecf2…` (`cb6d9455…`); as a START with port: `3d001532…` (k09's result) | IG's head + 41 constants jointly, 1,598 gens in 55 min on 30 processes, sigma still 0.27 at its cap | +0.819 se 0.060 over IB (n 1,024, 8588000..) |

### 4.1 Round 1 (episodes 2-3; batches ib-long, fa-long, scale, kit-ib, ic-long, slope, confirm-ic; results in root-1-01, root-1-02)

Head-only continuations of IB, FA and IC and the KIT-B width probes, about 75 minutes of search where the seat allowed it. Seven of the first eleven results stopped at the objective's 300 markets/s rule on 2-CPU seats before training anything (the requester lifted it to 100 in note 3).

| leg (START) | minutes, gens, speed | holdout vs START | real vs START | real vs IB |
|---|---|---|---|---|
| ib-long/ib-s30-h80-p32 (IB) | 76 min, **1,774** gens, 4,792/s, pop 32, sigma0 0.03 | +0.196 se 0.006 | = vs IB | **+0.246 se 0.020** (n 512) |
| ib-re/ib-s20 (IB) | 1,568 gens | — | — | +0.134 se 0.022 |
| ib-re/ib-s30 (IB) | 314 gens | — | — | +0.115 se 0.016 |
| ib-long/ib-s20-h80-p16 (IB) | 77 min, 260 gens, 423/s | +0.049 | — | +0.067 se 0.015 |
| ib-long/ib-s50-h40-p16 (IB) | 75 min, 291 gens | +0.043 | — | +0.062 se 0.019 |
| fa-long/fa-s50-h80-p16 (FA) | 72 min, 541 gens, 1,089/s | +0.167 over FA | +0.155 se 0.022 | +0.051 se 0.030 |
| fa-long/fa-s30-h80-p32 (FA) | 78 min, 74 gens | +0.045 over FA | +0.047 | −0.043 |
| ic-long/ic-s50-h30-p32 (IC) | 78 min, 240 gens, 865/s | — | +0.069 se 0.017 | +0.161 se 0.028 |
| ic-long/ic-s20-h60-p16, ic-s50-h30-p16 (IC) | 249 / 311 gens | — | +0.037 / +0.048 | +0.105 / +0.100 |
| slope/slope-c10-p32 (IC + volume-regime input, 190 vars) | 80 min, 199 gens | — | +0.073 se 0.024 | +0.233 se 0.031 |
| slope/slope-c05-p16 | 83 min, 423 gens | — | +0.036 | +0.149 |
| confirm-ic (IC vs IB, 2 × 1,024) | — | — | — | IC − IB +0.061 se 0.021 (ic-block-a) and +0.076 se 0.021 (ic-block-b); ic-s30 START arm +0.092 se 0.028 (n 480) |

Lesson of round 1: IB's own head kept climbing when given generations (1,774 gens: +0.25 over IB; 260-300 gens: +0.05..+0.07), confirming the sister goal's "still rising". But the requester's joint files (J5, T03) were 0.3..0.6 further ahead, so from episode 5 the head-only lines (IB, FA, IC, IG) were closed.

**Width probes (batches scale, kit-ib, wide-ig; KIT-B on the gas diet, from IA's or IG's weights).** The only legs that changed the network size:

| leg | width | result |
|---|---|---|
| scale/u16-gated-a (IA, two 19-16-2 nets, 708 weights) | 16 gated | 1,083 gens, 77 min: +0.219 se 0.006 over IA on holdout; real +0.191 over IAD but **−0.078 se 0.037 vs IB**; afterSwap 135,784 |
| scale/u24-gated (IA, 1,060 weights) | 24 gated | 110 gens: monitor +0.161 over IA; real +0.176 over IAD, **−0.098 vs IB**; unrolled emitter hit the 24,576-byte code limit, packed int32 head needed |
| scale/u24-single → fell back to 16 (speed) | 16 single | 118 gens: real +0.131 over IAD, **−0.118 vs IB** |
| scale/u16-single-a, u32-single | 16 / 32 | blocked at the old speed rule; 16-unit gas probe 132,923 (IAD 131,239), bytecode 15,330 |
| kit-ib-a, kit-ib-b | IB on the diet (IBD) | identical to IB per seed on real seeds 0..99 and 512 fresh (max diff 0.0); afterSwap 131,239 / 131,559 vs IB 237,021; 16-unit probe 132,040 / 132,328; kit speed 381 and 226 markets/s |
| wide-ig (w16-s30-p16, w16-s20-p32, w12-s30-p16; from IG) | 12 / 16 | small or absent gains over IG (root-1-03); cancelled in episode 5 with the other head-only lines |

So: widening to 16 or 24 units gained +0.13..+0.22 over the 8-unit IA/IAD it started from, at about 1,000 gas per doubling on the diet, but every widened net stayed 0.08..0.12 behind IB on the real engine because it started 0.26 behind, and no widened net was ever started from J5 or T03. The 8-unit joint line kept climbing instead (§5).

### 4.2 Round 2 (episode 4; ig-a/b/c, slope-ig, wide-ig, ib-re, fa-re, confirm-ig; root-1-02, root-1-03)

Head-only legs from IG under note 3's 100 markets/s rule. Best: ig-a/g02 +0.042 se 0.017 over IG, +0.276 se 0.029 over IB (n 512). All within +0.01..+0.06 of their START, 0.5 below T03; cancelled in episode 5 (running items still finished).

### 4.3 Round 3 (episode 5; j5-a..d from J5, ig-joint from IG; root-1-03, root-1-04)

First joint legs (note 4's parameterization: 0.05·rms, 2^(0.03 z); sigma0 0.3..0.7 in z; half-lives 30..60).

| leg (START) | minutes, gens, speed | holdout vs START | real vs START | real vs IB (n 512) |
|---|---|---|---|---|
| j5-c/j11-s05-h30-p16 (J5), id `cd8559ed…` | 62 min, 492 gens, 1,100/s | +0.065 se 0.005 | +0.091 se 0.018 | +0.595 se 0.039 |
| j5-b/j07-s07-h45-p16 (J5) | — | +0.077 se 0.006 | +0.035 se 0.020 | +0.669 se 0.038 |
| j5-c/j15-s04-h40-p16 (J5) | 80 min, 227 gens, 210/s | +0.038 | +0.024 | +0.679 se 0.035 |
| j5-d/j18-s03-h60-p16 (J5) | 81 min, 313 gens, 453/s | +0.048 | +0.047 se 0.024 | +0.661 se 0.047 |
| j5-d/j19, j20, j16 (J5) | 229 / 186 / 280 gens | +0.022 / +0.030 / +0.002 | +0.031 / +0.034 / −0.015 | +0.616 / +0.591 / +0.479 |
| ig-joint/gj04-s07-h45-p24 (IG) | 80 min, 305 gens, 342/s | **+0.396 se 0.009** | +0.381 se 0.028 | +0.568 se 0.033 |
| ig-joint/gj01-s10-h30-p16 (IG) | 79 min, 447 gens, 554/s | +0.332 | +0.339 se 0.030 | +0.491 |
| ig-joint/gj02, gj05, gj03 (IG) | 213 / 88 / 109 gens | +0.286 / +0.205 / +0.079 | +0.283 / +0.226 / +0.124 | +0.417 / +0.394 / +0.297 |

The joint search from IG gained +0.3..+0.4 in one 80-minute leg where head-only legs from the same IG gained +0.04: T's constants carried the gain (as J5 and T03 had shown in the sister goal). J5's children gained +0.02..+0.09 each; j11's sigma hit its cap after 10 minutes and its monitor was flat after 40 (cap too fast). Requester note 5 then delivered T03 (+0.82 over IB), 0.15 ahead of the best J5 child, and the J5 line was parked.

### 4.4 Round 4 (episodes 6-7; t3-a..d from T03, j11-a from J11, confirm-t03, then t4-a..e from T03 and dz-t03; root-1-04, root-1-05, root-1-06)

T03 legs: parameterization 0.03·rms, 2^(0.02 z) (decays via 1−d), sigma0 0.3..0.7, half-lives 45..90, holdout 41030000..41038191 shared.

| leg (START = T03) | minutes, gens, speed | holdout vs T03 (se 0.004-0.005) | holdout vs IB | real vs T03 | real vs IB (n 512) |
|---|---|---|---|---|---|
| **t3-a/k01-s05-h45-p16** | 76 min, 470 gens, 877/s (24 CPUs), sigma0 0.5, half 45 | **+0.066** | **+0.834 se 0.010** | **+0.071 se 0.019** | +0.793 se 0.037 |
| t3-b/k07-s03-h60-p16 | 79 min, 522 gens, 950/s, sigma0 0.3, half 60 | +0.055 | +0.822 | +0.035 se 0.018 | +0.836 se 0.041 |
| t3-b/k06-s04-h60-p16 | 80 min, 473 gens, 761/s, sigma0 0.4, half 60 | +0.051 | +0.819 | +0.047 se 0.017 | +0.792 se 0.038 |
| t3-c/k13-s05-h90-p16 | 79 min, 689 gens, 1,195/s, half 90 | +0.026 | +0.794 | +0.023 se 0.019 | +0.760 |
| t3-d/k16, k19, k20 (k20 id `b4669de3…`) | 196 gens (k20, 216/s) | +0.025 / +0.025 / +0.021 | +0.789 (k20) | +0.022 se 0.021 (k20, n 256) | +0.797 (k20) |
| t3-b/k10-s04-h45-p16 | 80 min, 251 gens, 444/s | +0.023 | +0.791 | −0.001 se 0.016 | +0.803 |
| t3-c/k11, k14; t3-a/k05, k04; t3-b/k08 | 377 / 252 / 131 / 85 / 127 gens | +0.014 / +0.010 / +0.010 / +0.002 / +0.004 | — | −0.011 / +0.010 / −0.024 / +0.025 / +0.001 | — |
| t3-a/k03, t3-b/k09, t3-c/k12 | blocked at the synthetic gate A (§6) | — | — | — | — |
| t3-a/k02, t3-c/k15 | blocked: macOS arm64, Linux wheel | — | — | — | — |
| j11-a/jc01..jc03 (J11) | jc01 44/s no search | jc03 +0.628, jc02 +0.617 vs IB | — | jc03 slightly negative | 0.2 behind T03: line closed |

k01's monitor curve (gain over T03 of the ES mean): +0.004 at 5 min, +0.022 at 18, +0.032 at 31, +0.047 at 44, +0.053 at 59, +0.061 at 72, +0.066 at 76 (sigma 0.5 → 0.155), still rising when it stopped. Gain tracked generations up to about 500 with a 45-60 minute half-life; the 90-minute half-life legs (k13, and m02 in t4 with 359 gens and nothing beating START) gained least.

confirm-t03: t03-block-a +0.800 se 0.026 (n 1,024, 8700000..8701023, on a native macOS build of the same engine source, reproducing published per-seed diffs to 1e-10; quartiles +0.89/+0.78/+0.75/+0.78), t03-block-b +0.7725 se 0.024 (8701024..8702047; quartiles +0.76/+0.78/+0.77/+0.78). With T03's own block: +0.797 on 3,072 seeds; the eleven START arms of t3/t4 legs agree; on confirm-k01's 3,072 seeds T03 − IB is +0.754 se 0.016; root-1-06 pools 19 results on 8,672 fresh seeds at +0.774 se 0.010. T03 is confirmed >= +0.3 over IB (code `cb6d9455…`).

t4-a..e (25 legs from T03 with EP7's capped synthetic gate A): 0 of the first 5 results trained; later ones mostly blocked at gate A (m06 panic at a 15 % cap, m19 and m21 0.195 / 0.251 bps drift near the spot bounds) or returned START (m17 139 gens, m22 485 gens with its own numba replica, m25 143 gens, m16 +0.001 holdout after 128 gens). m09 (85 markets/s) ran T03 vs IB on 384 seeds: +0.754 se 0.042. dz-t03 diagnosed the panic (§6).

### 4.5 Round 5 (episode 8; t5-a..e: n01..n15 from T03, n16..n25 from k20; root-1-06, root-1-07 and the nine t5 results handed to this write-up)

Parameterization 0.05·rms, 2^(0.03 z) (note 4's), recorded-callback gates, holdout 41070000..41078191. **No leg beat its START by a resolved margin.** The handed t5 results, read for this report:

| leg (START) | speed, gens, minutes | outcome | real START − IB |
|---|---|---|---|
| n11-s07-h45-p16 (T03) | 646/s, 128 gens, 28 min (stopped early for the real engine) | monitors −0.11..−0.30, START returned | +0.776 se 0.035 (n 512) |
| n12-s04-h60-p16 (T03) | 108 gens, 62 min, M 256 | START returned; first frozen 64-seed block lost (KIT decomposition assumed a 4 bps initial fee), valid false | +0.760 se 0.047 (n 256) |
| n13-s05-h75-p16 (T03) | **1,840/s, 956 gens, 82 min** | START returned | +0.784 se 0.034 |
| n14-s06-h45-p16 (T03) | 869/s, 514 gens, 78 min | START returned | +0.779 se 0.037 |
| n15-s03-h90-p16 (T03) | 105/s, 87 gens, 61 min | START returned; one block lost, valid false | +0.840 se 0.060 (n 192) |
| n16-s03-h60-p16 (k20) | 454/s, 161 gens, 78 min | START returned | +0.755 se 0.034 |
| n17-s04-h60-p16 (k20) | 463/s, 327 gens, 80 min | START returned (final monitor −0.083) | +0.771 se 0.039 |
| n18-s05-h45-p16 (k20) | 228/s, 116 gens, 46 min | START returned | +0.865 se 0.044 (n 256) |
| n19-s03-h90-p16 (k20) | 218 gens, 63 min, M 256 | START returned; one IB block lost, valid false | +0.818 se 0.067 (n 192) |

Root-1-06 and root-1-07 cover the rest: of 17 t5 searches, 13 returned START; n25 (k20, pop 24) +0.008 se 0.004 holdout and +0.046 se 0.022 real (n 256); n04 (T03) +0.003 holdout, −0.010 real; n02 400 gens, n03 457, n05 286, n06 270 all START. Pooled START − IB: T03 +0.774 se 0.010 (n 8,672, root-1-06); k20 +0.809 se 0.015 (n 3,008, root-1-07). The round's 4,000+ generations gained nothing: the ES mean drifted below START in the first 5-20 minutes in most legs and never recovered. The round-6 legs that did gain (q22, q21 phase 2, q04) all capped or re-mapped the decay constants (§5), and q21 phase 1 showed why: plain start·2^(0.03 z) on TOX_DECAY and LAMBDA_DECAY (0.99 and up) moves 1−d by large factors and cost −0.13 by minute 20.

### 4.6 Round 6 (episode 9; confirm-k01 and t6-a..e: q01..q15 from k01, q16..q18 from k07, q19..q22 from k06; root-1-07, root-1-08 and §2)

k01 confirmed (§1.1). Of 22 legs, 5 beat their START (q22, q04, q14, q21, q13; §2), q01 and q10 did not hold on the real engine, 15 returned START. Round-5 and round-6 legs together: gain over START tracked generations (1,371 gens +0.050; 1,114 +0.045; 573 +0.042; 397 +0.032; 300 +0.026; under about 280, nothing), that is the seat's speed; sigma0 0.2..0.3 with 45-60 minute half-lives gained, sigma0 0.4 with M 256 (q12, q18) drifted furthest below START (−0.09, −0.18).

### 4.7 The curve (real paired gain over IB)

| step | gain over IB | n | who |
|---|---|---|---|
| IB | 0 | — | board 522.00 |
| IG | +0.19 | 5,120 | requester note 5 |
| J5 | +0.55 se 0.01 | 5,120 | requester note 5; our j09 +0.562 (1,024) |
| J11 (our J5 child) | +0.595 se 0.039 | 512 | j5-c/j11 |
| T03 | +0.797 (own + confirm-t03); +0.754 se 0.016 on confirm-k01's seeds | 3,072 / 3,072 | confirm-t03, confirm-k01 |
| **k01 (our T03 child)** | **+0.822 se 0.016** | **3,072** | **confirm-k01** |
| k07 (our T03 child) | +0.884 se 0.049 | 1,024 | confirm-k01 |
| q22 (our k06 grandchild) | +0.911 se 0.043 | 512 | t6-e/q22, unconfirmed |

Each confirmed relay step in this goal added +0.05..+0.07 over its START per 70-80 minute leg at 500-1,000 markets/s; q22 added +0.05..+0.06 at 3,557 markets/s. Head-only continuations added +0.01..+0.06 (except the 1,774-generation IB leg, +0.25). Across the whole goal, about two thirds of trained legs came back with START unchanged.

## 5. What kept climbing, and what did not

- **Network size.** Only 8 hidden units ever climbed: every confirmed step (J5 → T03 → k01/k06/k07 → q22) is a 19-8-2 head with T's 41 constants searched jointly. The 12/16/24/32-unit variants (scale, wide-ig) were started from IA or IG on the gas diet, gained over their own start but never reached IB, and were not carried forward after the joint batons arrived. The diet itself works (IBD = IB per seed at 131k gas; 16 units at 132k), so a wide net from the T03 lineage is open but untried; J5 and T03 at 235k-238k have no room to widen without the diet.
- **Search dimensions.** 219 (178 weights + 41 constants) beat 178 (weights only) by an order of magnitude per leg (ig-joint +0.3..+0.4 vs ig-a/b/c +0.04 from the same IG).
- **Generations and speed.** Gain over START rose with generations in every round where the parameterization was sound (round 4: +0.066 at 470 gens, +0.025 at about 200, nothing under 130; round 6: +0.050 at 1,371, +0.042 at 573, +0.026 at 300, nothing under about 280). Seats under about 400 markets/s rarely produced a gain; the 1,774-generation head-only leg on a 4,792 markets/s seat produced the largest single-leg gain of the goal.
- **Sigma schedule.** sigma0 0.3..0.5 in z with a 45-60 minute half-life worked (k01 0.5/45, k06 0.4/60, k07 0.3/60, q22 0.3/60, q14 0.3/60); 90-minute half-lives (k13, m02, n15, n19) and sigma0 0.4+ with 256-market generations (q12, q18, n17) did not. Population 16 sufficed; 24 gained in q14 and n25 but not elsewhere.
- **Decay constants.** With 0.05/0.03 the plain multiplicative map on decays near 1 wrecked searches (round 5, q21 phase 1); capping decays and alphas at 0.999..0.9995 (q22, q04, q06) or mapping 1−(1−d)·2^(0.03 z) (q21 phase 2, q17, n25) let the search gain again. q22 and q04 both sit at the 0.999 cap on TOX_DECAY and LAMBDA_DECAY, so the cap binds.
- **Where the edge comes from.** Since J5 the gains are arbitrage edge (replica split: k01 − IB retail −0.38 / arb +1.22; q22 − k06 retail −0.61 / arb +0.66), while q13 and q14 moved the other way (retail +0.35..+0.50, arb −0.31..−0.47) and gained less. Retail volume rises +250..+480 Y per market against IB in every lineage; arb volume falls in k01/k07 and rises in k06.

## 6. The gate A finding (division by zero on synthetic stress)

T03 and every descendant (k01, k06, k07, q22 share its Solidity with only literals changed) revert with `Panic(0x12)` on a synthetic stress path of the EVM-against-port harness (reserves 100/10000, lognormal X amounts up to 15 % of the reserve, no restoring arbitrage): sequence 42, callback 1,223, reserve X drained to 0.0666 and Y 15,007,537, spot about 2.25e8. dz-t03/dz-b traced it to `_band`'s `acc[0]` (the sum of seven quadrature-node likelihoods, T03.sol line 462) being zero when every node z exceeds about 5e8; on 512 canonical replica markets its minimum is 4.5e-4. It never fired in any real-engine run of the goal (0 reverts in tens of millions of afterSwap calls across every arm). J5's Solidity passed the same harness (j01), so the division came with T03's constants. Three t3 legs (k03, k09, k12) and several t4 legs (m06, m19, m21 among those read) were lost to this gate, and the rest of t4 trained little. Two guards were built, each identical to T03 per seed on 256 real seeds (dz-a on 8146432.., peak 235,406; dz-b on 8147456.., peak 235,575; gate C 0.0003 bps): dz-b's `if (acc[0] == 0) return (mu, v);` (code `26c960d885b46eec181dd12edf56c6bd0a6696e41f81a163028029481c005e85`, result `badeca3a082ac0c48f60c71720189012bf824b0b22d474aeac0f2b967e420cb8`), which both items saw hit `Panic(0x11)` further along the same stress path (seed 440145, callback 1,825, reserve X 4.4e-8), and dz-a's clamp `if (acc[0] == 0) acc[0] = 1;` (code `df126b49435e97278a089d0db532986accb45722c5c13fe0e467752dcce3674b`, no revert through 2,000 callbacks per stress sequence but about 1,000 bps of port drift on that drained path). Per requester note 7, T03's code (and so k01's) ships unchanged; the guard is the requester's to adopt. From round 5 on, gates A and C replayed callbacks recorded from replica markets (seeds 9200000..9200049 and 9200100..9200149, 50 × 2,000) and every leg passed at under 1e-4 bps.

## 7. Seats, failures and tooling defects (so the next run can avoid them)

- Seat mix 2..32 CPUs, 44..3,557 replica markets/s; the real engine runs at about 1-3 markets/s per seat, so a 512-seed three-arm confirmation takes 10-20 minutes and slow seats lost their real arms to the 8-minute command limit (k05, m01, m24, jc01). macOS arm64 seats cannot run the Linux wheel (k02, k15, ic-s30-h40-p32, slope-c15, seven t03 batons in t4) and from note 6 ran replica-only (q04, n24).
- KIT-B's edge decomposition assumes a 4 bps initial fee; T03's BASE_FEE is 0.000394715, which tripped an assertion and lost one 64-seed real block in seven round-5 items (n12, n15, n19 among the handed ones) and in k05; the arms were not rerun (seeds never reused), so those items are `valid: false` for coverage, not for gas.
- Network: j17, m20, n10 could not reach api.imd.fun or github.com and measured nothing.
- Many legs searched below the goal's 300 markets/s rule under the requester's 100 markets/s override (six of round 5's, nine of 17 in t5-d/t5-e and t6-a/t6-b, four of 15 in t6-b..e); none of them produced a kept gain, so no promoted weights depend on one. k07's first IB chunk was rerun once after a reconstruction discrepancy (its confirmation items k07-c1/c2 ran clean).
- The merges' source checks flag 1-3 "sources that did not hold on re-read" on nearly every result; the result JSONs carry no URL lists, so the flag cannot be tied to a claim. Every performance figure here is a local engine measurement, not a quotation; the provenance claims (that a file at a URL is "the" IB/T03) rest on hashes that agree across dozens of independent items and on my own re-fetch of `12606d82…` and `afd5183e…` while writing this.

## 8. Seeds used (never reuse)

Real engine: every block below 8200704 (8000000..8200703), plus 8588000..8589023 (T03's own) and 8700000..8702047 (confirm-t03). **Next free real seed: 8200704.** Replica training: 100000000..275999999, 500000000..516000000, 600000000..800000000, 900000000..1360000000 (the sister goal uses 1400000000 up); next free 276000000. Monitor 30000000..30002047 reused on purpose. Holdouts used once each: 41010000, 41030000, 41050000, 41070000, 41090000 (+8191 each); next 41110000. Gate recordings 9200000..9200149. ES seeds up to 20261622.

## 9. What the next run should try

1. **Start from q22** (`8cbbcd23…`), after one item pairs q22, k01 and IB on 2,048 fresh seeds from 8200704 (three arms, 64-seed commands, sum/sumsq, quartiles, gas). If q22 holds its +0.05 over k01, it is the baton; otherwise k01. Also freeze q04's params (`5922e652…`, port 732c0fb6) into k01's Solidity on a Linux seat and confirm them: +0.045 on the holdout, never run in the EVM.
2. **Keep the joint 219-dimensional search, 8 units, population 16, 512 fresh markets a generation, sigma0 0.3 with a 60-minute half-life (0.2 on a slow seat), and the decay map 1 − (1−d)·2^(0.03 z) with d capped at 0.9995** (or raise the cap and let the search say): the 0.999 cap binds in q22 and q04.
3. **Spend the items on fast seats.** A leg under about 400 replica markets/s almost never beat its START; q22's 1,371 generations in 67 minutes did. Give slow seats the confirmations. Let a leg search for the full time: q22 stopped 35-40 minutes early with its monitor still rising.
4. **Chain legs through weights, as the requester asked, but hand over the ES state too** (mean z, sigma, next train seed; q21 and others return it) so a fast seat can resume rather than restart at z = 0 with a fresh covariance: round 5 showed that a restart from a converged point drifts below START for 5-20 minutes before it can gain.
5. **Try width on the diet from this lineage.** kit-ib proved IB on the diet is IB per seed at 131k gas and 16 units cost about 1,000 more; the j5-diet item (J5's 41 constants in KIT-B, J5D equal to J5 per seed, the kit's `train` extended to the joint search) was refused on a brief wording and never ran. A 16-unit net expanded from q22 (new output weights 0, identity proven first, gas probed) on a 1,000+ markets/s seat is the one untried direction with evidence behind it (+0.13..+0.22 over its own 8-unit start in round 1).
6. **Ship T03G's guard only if the requester wants it:** it is identical per seed on 512 real seeds and removes the only known revert.

## 10. What is missing or was not checked

- No leaderboard run of any file; the gains are paired engine measurements against IB, not board scores.
- No HA arm in this goal: the gain over HA is chained through IB's own file (§1.1).
- q22, q14, q21, q13 confirmed on 512 real seeds each only; q04 never frozen to Solidity; q22 and k01 never paired on the real engine; k07 and k01 never paired.
- The real engine exposes no retail/arb edge split; only volume deltas (engine) and replica edge splits are reported. Some legs reconstruct arb edge with KIT-B's decomposer; two of those (k07, k13) relaxed a reconstruction check.
- The t5 results were not read by any orchestration episode; nine of them were read for this report (§4.5) and the rest through root-1-06 and root-1-07.
- The sister goal's figures (J5 +0.55 on 5,120 seeds, IG +0.19, T03 +0.819 on its own block, IB +0.592 over HA) are the requester's measurements, not re-run here except where a START arm of our legs measured the same file (they agree within noise).
- The source-check flags on the results (§7) could not be resolved to specific claims.

## 11. Results this report rests on

Handed to this write-up: root merges root-1-01..08; confirm-k01 items k01-c1..c6 (b40-k01-c1..c6) and k07-c1, k07-c2; round-6 legs t6-e/q22 (b45-q22-k06-s03-h60-p16), t6-c/q14 (b43-q14-k01-s03-h60-p24), t6-e/q21 (b45-q21-k06-s04-h45-p16), t6-c/q13 (b43-q13-k01-s02-h45-p16), t6-a/q04 (b41-q04-k01-s03-h30-p16); round-5 legs t5-c/n11..n15 (b37-…) and t5-d/n16..n19 (b38-…). Fetched again for this report: the k01 file `12606d82…` (hash equal; its `code_zb64` hashes to `9253b6f3…`, reproduced in §1.2) and the IB file `afd5183e…` (hash equal; code `30194182…`). Earlier rounds' figures come from the root merges (which cite each item's result path under `artifacts/goal/batches/<batch>/items/<item>/result.json` and its SHA-256) and from the orchestrator's episode notes in goal.json, which name every id used above (T03 as a START `3d001532…`, k06 `e7b20742…`, k07 `9212fa7f…`, k20 `b4669de3…`, J11 `cd8559ed…`, T03G `badeca3a…`, kit-ib `b0acc9f9…` and `8c09856c…`).
