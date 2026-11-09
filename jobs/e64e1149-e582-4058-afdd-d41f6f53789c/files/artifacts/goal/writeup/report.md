# AMM fee challenge: goal write-up (STACK to top 10)

**Outcome.** The goal is not met. The best confirmed file, T (toxicity run-anchor on RS2), measures **+0.590 paired over STACK on 4,000 fresh seeds (se 0.014, 0 OutOfGas)**; the top 10 needs about +5.0. Ten episodes and 124 items produced four confirmed, stacked steps (V10, RS1, RS2, T), each worth tenths of a point, and nothing near the gap. T passes the requester's standing submission bar (at least +0.1 over RS2 on 4,000 fresh seeds, more than 2 se, 0 OOG) and is the file to submit. The goal built no code trunk (`trunk` is null in goal.json); every artifact is a result file under `artifacts/goal/batches/<batch>/items/<key>/result.json`, fetchable at `https://api.imd.fun/artifacts/<sha256 of the result file>`.

Board figures are the requester's (never refetched here): STACK 519.71 (29th), V10 519.8458 (28th), RS2 520.0536 (27th), 26th about +0.22 above RS2, 10th 524.66, 1st 528.40. Local gains reached the board at 1.0x (V10: local +0.136, board +0.136) and 1.27x (RS2: local +0.163, board +0.208). No board rank is claimed from local figures.

## 1. Best Strategy.sol: T

| Field | Value |
| --- | --- |
| SHA-256 of the source below | `ebd9de9bf6af6e55d5e308fd15dbb88edec11fd684891d02a30aec185acd19b3` |
| Origin | e07-run-anchor/tox-a (result id `6ac5e013b7b1fb4c5e7bdcdfec0aba28b16824e18ccf39500f258533879faffe`); generator applied to RS2 with k_linear 0.7126960148076509, k_quadratic 1.2952407538263107, N 674 |
| Base | RS2, `f24b6ca198b744c380842c3a17964a6dc21f311bb04984b26733afa3fee8eaf2` (result id `19f2ec857df536e8ab62ab1da89ec6623332521ce46849f15bccff402c63e1e5`), the network's own file now on the board |
| Confirmations | e09-confirm-tox/a (b43-a, result id `f0f9c213c29909def060f273358f517337e73bf3ee082deacd1cba25121dd3a8`), seeds 5116000..5117999; e09-confirm-tox/b (b43-b, id `cedcd5df5201048f2b679cddc6c44379f88db484e9c4c7ee6e3a72be7d1787e6`), seeds 5118000..5119999. Both: source frozen and hash-verified before any fresh seed, CH on seeds 0..999 = 525.5258821780834 exactly, each arm alone vs VanillaStrategy, no tuning, no retries, no seed dropped |
| Gas | afterSwap max 226,178 (block a), 225,591 (block b) of the 250,000 limit; afterInitialize 243,115; OOG 0; reverts/other halts 0 in every arm (candidate, RS2, STACK, both roles) |
| Licence | MIT SPDX header; no third-party code. T is a generator on RS2, which descends from the network's own V10/STACK line (V2/CH/YQ ancestry, credited by the requester in submitted headers) |

### Paired gain on fresh seeds (candidate minus reference, each arm alone vs Vanilla)

| Comparison | Block | n | mean | se | retail edge delta | arb edge delta |
| --- | --- | --- | --- | --- | --- | --- |
| T vs STACK | 5116000..5117999 | 2000 | +0.6292 | 0.0196 | -0.3281 | +0.9572 |
| T vs STACK | 5118000..5119999 | 2000 | +0.5513 | 0.0209 | -0.4003 | +0.9516 |
| **T vs STACK, pooled** | both | **4000** | **+0.5903** | **0.0143** | -0.3642 | +0.9544 |
| T vs RS2 | 5116000..5117999 | 2000 | +0.3099 | 0.0177 | -0.6942 | +1.0041 |
| T vs RS2 | 5118000..5119999 | 2000 | +0.2325 | 0.0194 | -0.7607 | +0.9932 |
| **T vs RS2, pooled** | both | **4000** | **+0.2712** | **0.0132** | -0.7275 | +0.9986 |

Pooling is over one hash from the reported sum_d and sum_d2 (sample variance includes the between-block means). The two blocks differ by 0.077 vs RS2, 2.9 se of the difference, so both are shown. Reconciliation retail + arb = total holds to 1.1e-13 in every arm. Arm means: block a T 528.115, RS2 527.806, STACK 527.486; block b T 525.492, RS2 525.259, STACK 524.940.

Worst seeds, T minus STACK, across both blocks: 5118349 -6.27, 5119425 -6.24, 5119386 -6.18, 5116111 -5.79, 5117889 -5.55. Worst seeds, T minus RS2: 5119638 -8.39, 5118349 -6.99, 5119386 -6.56, 5117889 -6.32, 5118922 -5.93. The tail is heavier than RS2's own tail vs STACK (worst about -2.2 to -3.1): T's larger quadratic response occasionally overcharges a run.

Before confirmation, T measured +0.2335 se 0.0373 over RS2 on 512 held-out tuning seeds 954000..954511 (worst -8.72) and +0.270 se 0.051 on its 256-seed recheck; its independent sibling tox-b (different constants 0.473 / 1.266 / N 403, hash `c7df70f2...`) gave +0.227 se 0.029 on 959000..959511, so the family replicated on two machines before either block was opened.

### Source (complete, 20,627 bytes; imports the challenge's `AMMStrategyBase.sol` and `IAMMStrategy.sol` at commit 6b6921f8d463314aa7c96234e1be25a25245f704)

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

        slots[0] = bidFee; slots[1] = askFee; slots[2] = (spot << 64) | trade.timestamp;
        slots[3] = dirState; slots[4] = actEma; slots[5] = pHat;
        slots[6] = sigmaHat; slots[7] = lambdaHat; slots[8] = sizeHat;
        slots[9] = toxEma; slots[10] = stepTradeCount;

        return (bidFee, askFee);
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

## 2. The mechanism and why it gains

T differs from RS2 in three places (unified diff against RS2's exact code, 24 added lines, 3 changed):

1. **A run-level anchor for the toxicity signal.** Slot 16 packs a running mean of `toxEma` (low 64 bits) and a sample count (upper bits). The count climbs to 674 and then stays there, so the mean is a 1/674 incremental average over the whole run: it remembers the run's typical mispricing level, where RS2's `toxEma` (decay 0.91 a step, blend 0.051) forgets it in a few steps.
2. **Two blended toxicity inputs.** `toxLinear = mean + 0.7127 * (toxEma - mean)` feeds the linear toxicity term and the sigma-toxicity cross term; `toxQuadratic = mean + 1.2952 * (toxEma - mean)` feeds the quadratic term. The linear fee therefore moves less than RS2's with each print (deviations from the run norm shrunk to 71%), while the quadratic fee moves more (deviations amplified to 130%). The directional skew (`DIR_TOX_COEF`) and the stale-side shift keep the raw `toxEma`.
3. **No new initialisation write**: slot 16 is lazily populated, so afterInitialize gas stays at RS2's 243,115 and the only gas cost is about 23k in afterSwap (203k to 226k).

**Why it gains.** Against STACK, T wins +0.95 per run on the arbitrage side and gives back -0.36 on retail; against RS2, +1.00 arb and -0.73 retail. Toxicity is `|spot - pHat| / pHat`, the pool's own mispricing; when it spikes above the run's norm, the quadratic term now widens the fee faster, so the arbitrageur who arrives at the next step pays more or trades less (arb loss is about y*(dp/p)^2/2 per up-step while the spot sits at the band edge). When toxicity is near its norm, the linear term is steadier than RS2's, so ordinary retail prints see a calmer quote. The net is a convex response to mispricing anchored to the run: cheap in calm stretches, sharply dearer in toxic ones. This is the direction the board fit (e02-board-fit) pointed at: the leaders' mid fee rises more with volatility proxies (4.8 to 6.8 bps per unit of the arb-volume proxy vs STACK's 3.2) and less with retail flow (0.19 to 0.44 bps per 10k retail Y vs STACK's 1.42).

**Against the board rungs.** The requester's board analysis splits the gap into a retail rung (29th to 10th: about +1,430 retail Y per run at the same mean fee) and an arb rung (10th to 1st: about -824 arb Y). T attacks the arb rung and pays on the retail rung. The sigma anchor S (section 3) does the opposite (retail +0.30, arb -0.19); their fixed union U was not better than T alone on the 780 seeds that ran (+0.199 vs RS2, retail -1.17 / arb +1.37), so gains in this family do not add.

**Tercile breakdown: not measured.** The brief asked for T's retail and arb edge by retail-volume tercile. No handed result contains per-seed rows or retail volumes (the confirmation workers kept per-seed files under their scratch directories and returned only sums, worst-five lists and arm means), so that split cannot be computed from the delivered data and is not invented here. What the board data give, from e02-board-fit on the leaderboard's 1,000 runs (tercile cutpoints 69,854 and 81,019 retail Y per run): the top five are 0.21 to 0.63 bps cheaper than STACK in the low-retail tercile, 1.16 to 1.45 bps cheaper in the middle and 2.11 to 2.33 bps cheaper in the high tercile, almost all on the bid; 10th is 0.59 / 1.31 / 2.36 bps cheaper. T does not lower fees with retail volume; it sharpens the response to mispricing. The first measurement of the next run should be T's per-tercile retail and arb deltas on the two confirmation blocks (seeds 5116000..5119999 are already spent, so they can be re-run for diagnostics without touching fresh seeds).

## 3. Every mechanism tried, ranked by its fresh-seed result

Fresh means a block of seeds at or above 5,000,000 never used before, at least 2,000 seeds unless noted; held-out means 512 tuning seeds (10000..999999) unseen by the search, frozen before the run. Every arm ran alone vs Vanilla. "Base" is the file the mechanism was built on and paired against. Entries with no fresh row were never promoted (gate: held-out gain more than 2 se and at least +0.05 to +0.1). All listed arms had 0 OOG unless noted.

### 3a. Confirmed on fresh seeds (vs STACK where measured)

| Rank | Mechanism (base) | Code sha256 | Fresh vs STACK | Fresh vs base | retail / arb vs base | afterSwap max | Source results |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **T: toxicity run-anchor (RS2)** | `ebd9de9b...` | **+0.5903 se 0.0143, n 4000** | +0.2712 se 0.0132 vs RS2 | -0.73 / +1.00 | 226,178 | b43-a, b43-b |
| 2 | V: virtual Vanilla reserves steer the attracting fee, g .15 cap 8 bps margin 4 (RS2) | `f61c0f28...` | +0.5514 se 0.0138, n 2000 (block 5820000, no RS2 arm) | held-out only: +0.223 se 0.018 | +0.18 / +0.04 | 231,403 (tight) | b35-b |
| 3 | U: union T + A + S (RS2) | `64a233b9...` | +0.573 se 0.036, **n 780 only** (block 5120000 partial) | +0.199 se 0.037 vs RS2 | -1.17 / +1.37 | 228,697 | b44-a (b44-b ran no fresh seed) |
| 4 | vanilla-quote c, g .5 cap 3 margin 3 (RS2) | `ef486e30...` | +0.4614 se 0.0144, n 2000 (block 5830000) | held-out +0.107 se 0.018 | +0.04 / +0.07 | 229,745 | e08-vanilla-quote/c |
| 5 | S: sigma run-anchor, w .683 g 1.047 N 5377 (RS2) | `014ad7bd...` | +0.4366 se 0.0118, n 4000 | +0.1155 se 0.0091 vs RS2 | +0.30 / -0.19 | 205,159 | b41-a, b41-b |
| 6 | A: activity/flow run-anchor (RS2) | `0c3836cd...` | +0.4082 se 0.0097, n 4000 | +0.0853 se 0.0054 vs RS2 (under the +0.1 bar) | -0.51 / +0.60 | 204,576 | b42-a, b42-b |
| 7 | dual-anchor b: weak pull of the stale price into the inferred Vanilla band, w .02 k 8 (RS2) | `77854865...` | +0.3415 se 0.0138, n 2000 (block 5800000) | held-out +0.011 se 0.005 (null) | +0.06 / -0.05 | 205,326 | e08-dual-anchor/b |
| 8 | RS2: cleaned retail-size state, 7-param CMA (V10) | `f24b6ca1...` | +0.3233 se 0.0081, n 6000 (RS2 arms of b41-a, b42-a, b42-b) | +0.163 vs V10, +0.090 vs RS1, n 4000 | vs V10 +1.47 / -1.32 | 203,671 | e06-confirm-rs2/a,b; on the board at 520.0536 |
| 9 | arb-surge a: surcharge on arbitrage streaks (RS2) | `03f2991d...` | +0.3065 se 0.0140, n 2000 (block 5018000: **re-used**, it was e03-v10-blend/b's block) | held-out -0.037 se 0.012 (negative) | -0.23 / +0.20 | 225,494 | e08-arb-surge/a |
| 10 | RS1: posterior-weighted own-flow count and size (V10) | `df2817ba...` | +0.2138 se 0.0135, n 2000 | +0.085 se 0.008 and +0.072 se 0.009 vs V10 | +0.04 / +0.05 | 202,479 | e05-confirm-rs/a,b |
| 11 | V10: censored-price posterior on the fast estimate (STACK) | `cd9bdb45...` | +0.1362 se 0.0079, n 6000 | same | -1.14 / +1.27 | 194,882 | e01 censored-price, e03-confirm-v10/a,b; board 519.8458 |
| 12 | dual-anchor a, w .125 k 2 (RS2) | `9faa3bed...` | +0.0280 se 0.0169, n 2000 (block 6840000) | held-out -0.272 se 0.018 | +0.39 / -0.66 | 203,598 | e08-dual-anchor/a |
| 13 | value-policy floor fMid >= 0.3 sqrt(uncertainty) (STACK) | `5c367973...` | +0.0164 se 0.0015, n 2000 | same | not split | 214,561 | e01 value-policy |
| 14 | V10 + floor kappa .8 | `ebf9989a...` | +0.1824 (inherited V10) | +0.0002 se 0.0002 vs V10 | 0 / 0 | 196,935 | e03-v10-floor/b |
| 15 | V10 toxicity fast-weight .15 / .30 | `c46e2b14...` / `c8a4b226...` | +0.125 / +0.121 (inherited) | +0.001 se 0.004 / -0.005 se 0.006 vs V10 | b: -0.41 / +0.40 | 195,466 | e03-v10-blend/a,b |
| 16 | V10 cheaper attracting side (first-print cap 28 bps) | `6694d28a...` | +0.153 (inherited) | +0.002 se 0.003 vs V10 | +0.007 / -0.005 | 194,759 | e03-v10-retail/a,b |
| 17 | normalizer-state D: interval projection of the rival pool (STACK) | `ce7e02d2...` | -1.376 se 0.046, n 2000 | same | split unvalidated | 240,832 | e01 normalizer-state |

### 3b. Searched, held-out only, never promoted (vs the named base)

| Mechanism (base) | Held-out vs base, n 512 | retail / arb | Verdict | Source |
| --- | --- | --- | --- | --- |
| **K: arb-weighted direction skew**, push weighted by a+(1-a)p, cap k x cleaned size, DIR coefficients x32 (a .25, k 4) (RS2) | **+0.509 se 0.027** | +0.51 / 0.00 | Best unconfirmed lead; its confirmation batch (e10-confirm-skew) was refused because the episode finished | b37-a, `9f9c5b45...` |
| arb-skew b (a 0, k 8, gain 64) (RS2) | +0.305 se 0.034 | -1.89 / +2.19 | same family, different trade-off | b37-b, `8fd9c011...` |
| sticky deviation b (RS2) | +0.126 se 0.030; cubic toxicity term alone +0.108 se 0.029; peak-hold increment +0.018 se 0.011 | -0.24 / +0.36 | the gain is the added cubic term, not the peak-hold | b38-b, `d8501ff2...` |
| sticky deviation a (RS2) | +0.283 se 0.057, n 128 only | not split | incomplete | e08-sticky-dev/a |
| rs2-wide c (7-param family, retention at its .9999 bound) (RS2) | +0.019 se 0.009; a -0.004, d -0.021, e +0.010, f -0.020, b incomplete | c: -0.08 / +0.10 | family at its plateau, closed | e06-rs2-wide |
| lean-tail governors a / b (RS2) | +0.010 se 0.011 / +0.011 se 0.006 | a -0.45 / +0.46 | persistent lean tracks real mispricing; shrinking it loses | e07-lean-tail |
| arb-surge b (RS2) | -0.003 se 0.005 | -0.07 / +0.07 | null | e08-arb-surge/b |
| rs-post a / b: cleaned rate into first-print arb odds (RS2) | -0.102 se 0.023 / -0.011 se 0.015 | a -0.42 / +0.32 | retired | e06-rs-post |
| rs-side b: per-side lambda split (RS2) | -0.025 se 0.014 (a incomplete, n 24) | -0.59 / +0.56 | retired | e06-rs-side |
| vol-flow a / b: (1+a) on sigma terms, (1-b) on flow terms, minus c (RS2) | -0.037 se 0.018 / -5.35 se 0.067 | a -0.40 / +0.36 | retired | e07-vol-flow |
| learned fee heads a / b / c (RS2 state, 10-8-2 nets, ES at EVM speed) | -40.5 se 0.98 / -0.87 se 0.055 (n 128) / -19.0 se 0.69 | b -1.90 / +1.03 | a few dozen evaluations per item; not a test of the family | e09-learn-head |
| transition-policy a / b: continuation-gated residual quotes (V10) | -0.026 se 0.005 / +0.003 se 0.004 | b +0.03 / -0.02 | retired | e04-transition-policy |
| band-transport a / b: move both band endpoints with cumulative retail displacement (V10) | -0.187 se 0.051 / -0.041 se 0.020 | a +1.10 / -1.28 | retired; losses grow with the square of the move | e04-band-transport |
| continuation table / polynomial (V10) | -0.044 se 0.013 / -0.003 se 0.003 | a -0.49 / +0.44 | retired | e05-design-impl cont-a, cont-b |
| size-tail quote targets, DAR and Jensen (V10) | every active arm -0.13 to -30; identity frozen | | retired | e05-design-impl tail-a, tail-b |
| retail-state a, structure C (V10) | +0.033 se 0.072, n 64, incomplete | -1.45 / +1.48 | no information | e04-retail-state/a |
| router-share revenue-optimal attracting fee a / b (STACK) | -0.232 se 0.013 / -0.002 se 0.003 (collapsed to STACK) | a -0.21 / -0.03 | retired | e02-search-share |
| exposed-side surcharge from the arb sizing identity (STACK) | -0.024 se 0.007 (b: 2 evaluations) | -0.12 / +0.10 | retired | e02-search-arbside |
| 60-constant regime split a / b (STACK) | -0.576 se 0.046 / -0.836 se 0.040 (n 384) | not split | retired | e02-search-regime |
| RES-TABLE residual a / b (STACK) | -0.239 se 0.022 / -0.039 se 0.018; shuffled controls -0.52 / -0.75 | | retired | e03-restable |
| horizon-hazard fee b (STACK) | -0.046 se 0.016, n 128 (a blocked) | -0.07 / +0.02 | not retired, not pursued | e03-horizon |
| shadow-value objective a / b (STACK) | -0.024 se 0.010 / -0.045 se 0.013 | b -0.51 / +0.46 | retired | e03-shadow |
| event-hazard pilot | blocked at setup (non-x86 host), n 0 | | not a tried idea | e01 event-hazard |

### 3c. Public code measured against RS2 (common seeds 901000..901255, n 256; none used)

CH (ChengHua926 @d34a5199) -1.840 se 0.070; houseofjiao public head -1.838; solosage1 TmpDirectionalSkewMod_v16 -2.028; shl0k28 BandShield_ghost -2.165; lumen night_7 -2.720; YQ, wellimbharath godknows and maxnorm V34/V43 -2.73 (edge-identical totals); ylintern -2.757; 0xniki L9 -3.222; atvinicius -7.565; dipankar SigmaAdaptive -7.965; happybigmtn -20.1 and -32.9 (n 32); VictorQian03 finalists -65.8 to -87.6; dicethedev Noise gist -142.7. Many other screened fork files OOG and are invalid regardless of score. 74 forks were enumerated (28 pushed after upstream, all mined; 46 upstream-identical or inaccessible), plus write-ups and entrant pages for the top 30: only houseofjiao (14th) has published code, and the public file was not shown to be the ranked entry. Every public state-estimation file is the YQ architecture retuned. No third-party code entered any candidate.

### 3d. Pattern across 124 items

Every overlay that moves the quoted band trades retail for arb at about one for one and nets zero or less (band-transport, continuation, size-tail, surcharges, governors). The only mechanisms that net a gain replace a short-memory input with a long-memory or cleaned one: the censored posterior (V10), the cleaned flow size (RS1/RS2), and run-level anchors on sigma, activity and toxicity (S, A, T). K (arb-weighted skew) is the one lead that gains retail without paying arb, and it is unconfirmed.

## 4. Evidence quality and gaps

- Each confirmation above was run once per machine on a block never used before, with the candidate frozen and hash-checked first, CH calibration exact, and gas counters reset and read per 20-seed chunk for every arm and role. Every handed `code` field was re-hashed in episodes 4 to 10 and matched its claim; T's embedded source above re-hashes to `ebd9de9b...`.
- Retail and arb edges are reconstructed by the harness (arb = negative reconstructed arbitrageur profit, retail = total minus arb) and reconcile to 1e-13; they are not native labels.
- The two T blocks differ by 2.9 se of the difference. A third block would settle the size of the gain; it does not change the sign (both blocks are more than 11 se above zero).
- Off-ledger blocks: workers also used 5018000..5019999 (arb-surge/a; previously e03-v10-blend/b's block), 5800000..5801999, 5820000..5821999, 5830000..5831999 and 6840000..6841999. Treat [5000000,5148000), [5800000,5900000) and [6840000,6842000) as spent; the next free confirmation seed is 5148000.
- The union item b ran no fresh seed (5122000..5123999 untouched, still quarantined); union item a ran 780 of 2,000 seeds on a two-core machine.
- Source-recheck flags: the plane flagged unreadable or unsupported external sources on many items (public forks, the organiser's essay). Those flags qualify authorship, licence and mechanism attributions of public material; they do not touch the local measurements, which are the workers' own simulator runs with embedded reproduction scripts.
- The 0.65 transfer coefficient in the objective came from one earlier submission; the two submissions in this goal transferred at 1.0 and 1.27. If T transfers one for one it lands near 520.3, about 26th, and about 4.3 board points short of 10th.

## 5. What the next run should do

1. **Confirm K, KT and KV first.** K (`9f9c5b45...`, result id `82aa583bf73126cb5c1a4e934c3ee4021848b8b15938f7f9dfbbf129ea694c5c`) is +0.509 se 0.027 over RS2 on 512 held-out seeds with no arb cost and gas 202,817. KT is K's four text replacements applied to T's code (expected sha256 `072edba3d6b13c0c88560fd58b3ab31a0bf72a7cc095aab8406e03cad284be11`), KV the same on V (`b9cd1840a2d988399f72b3d78c6a11c26b138402fce90f21914f0b6afb6aa7ee`); neither has been compiled or run. Three machines each, 2,000 fresh seeds per machine from 5148000, candidate and RS2 and STACK arms, 32-seed gas preflight first. Episode 10 wrote these five batches but they were refused because a finishing decision runs no new batches.
2. **Measure T's gain by retail-volume tercile** on the spent blocks 5116000..5119999 (retail volume per run is in the simulator's result rows) so the retail and arb rungs can be attributed properly.
3. **Search in the replica, confirm in the simulator.** Five validated market replicas exist; the fastest, e08-replica/d (result id `e8a7a2af9039c24b8bb2d3b5fa1c9113606cbf5a480ac07d02ca26750f1752ea`), runs 3,721 markets a second against 1 to 5 in the EVM simulator, with CH's mean within 0.3 se of the real 525.53 and three perturbation deltas within 1 se of real. RS2 exists as an njit Python port with fee error under 4e-9 bps against the EVM (e08-rs2-port/a, id `1b8e8ca5d0da1f0071a9ae18505d6cbff902b88b2fbc34e523afbd212a9a26ce`, 102 constants in a TH array). The leaders' kind of rule (Solidity neural networks, 100+ constants, per the organiser's essay) needs thousands of evaluations an item; every search here got 15 to 180. Train the learned head and a joint search over RS2's constants in the replica, write back to Solidity, re-check on 256 real seeds, then confirm. The e10-replica-pilot brief (port a spliced into replica d, transfer check on two RS2 variants, 20-minute CMA over the 39 named constants) is written and ready to re-spawn.
4. **Stack the cubic toxicity term** (+0.108 se 0.029 alone on RS2) onto T and K, and test T's anchor with a larger quadratic gain and a cap on the per-run overcharge that produced the -8 worst seeds.
5. Keep the rules that held: briefs under 3,000 characters with the verbatim setup script; two items per idea on different machines; read `blocked` before counting an idea as tried; CH calibration in every confirmation; never pool different hashes; afterSwap under 235k and afterInitialize under 245k before confirmation; any OOG invalidates the hash.

## 6. Provenance of the figures in this report

Handed results read for this write-up: root merges 1 to 5 (`artifacts/goal/roots/1/01..05/result.md`), e09-confirm-tox/a,b, e09-confirm-sigma/a,b, e09-confirm-act/a,b, e09-combine-anchors/a, e08-arb-skew/a,b, e08-vanilla-quote/b, e08-sticky-dev/b, e09-learn-head/b, e08-replica/d, e08-rs2-port/a, plus the orchestrator notes of episodes 1 to 10 in goal.json. Pooled figures (T, S, A over two blocks; RS2 minus STACK over three) were computed here from the reported n, mean and se, and for T cross-checked against the reported sum_d and sum_d2 (identical to 1e-15). Nothing in this report is a new simulation or a board fetch.
