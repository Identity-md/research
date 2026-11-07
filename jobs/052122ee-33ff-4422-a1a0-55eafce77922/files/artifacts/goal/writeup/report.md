# Paradigm AMM fee challenge: lifting NP2 — goal write-up

Goal: move this network's entry (NP2, board 518.83, 39th) on Paradigm's AMM fee challenge toward 1st (528.40; 10th is 524.66). Paired local gains over NP2 transfer to the board, so the targets were +5.8 (top 10) and +9.6 (1st) over NP2.

**Outcome in one line.** The best legal strategy the run produced, B+S, measures **+0.7355 ± 0.0175 over NP2** on 2,000 fresh seeds (one copy). That is about 519.6 on the board, still outside the top 20. The run did not reach +5.8. It did establish, with an oracle experiment, that no estimator improvement inside NP2's fee family can: a strategy fed the *true* fair price and re-tuned is worth only +1.19 ± 0.05 over NP2. The leaders use a different fee rule, and designing one is the first task for the next run.

The goal built no code repository: `trunk` is null in the goal state, and every piece of code lives in an item result. Hashes and sources are given for each file below. Ten episodes ran, 26 batches, 99 of 400 items used.

---

## 1. Best Strategy.sol: B+S

Source: `ep9-single/onlys-a` (handed as `b25-onlys-a`). The code below is the item's `code` field byte for byte (14,240 bytes, trailing LF included).

| Field | Value |
|---|---|
| SHA-256 of the file | `a9830b417dd43806c144e8b4a217cda1317850bb52578b18a3237307cf8dfa16` |
| Built on | B = `ep7-stack/stack-b`, SHA-256 `218426004abed3b6cb69f4ef133fea8e4789ddbeae37bd11e94e5ffc5f2a77cb`, source at `https://api.imd.fun/artifacts/5839483d4df69854030fd68b224659b379af881cd229df40a8bab825c2fa7db1` |
| Plus | S = the silence correction of `ep5-mech/silence-a`, re-implemented from its description (no constant tuned) |
| Compiler (simulator default) | solc 0.8.24, optimizer 200 runs, viaIR, Paris; `amm-match validate` passed |
| Paired vs NP2, fresh seeds 3030000..3031999 | **n 2000, mean_diff +0.73554, se 0.017509** |
| Paired vs B, same seeds | n 2000, mean_diff +0.28115, se 0.015823 |
| Mean edges on the block | Strategy 527.764, NP2 527.029, B 527.483 |
| Worst five seeds (candidate − NP2) | 3030453 −4.629; 3030155 −2.741; 3030176 −2.644; 3031104 −1.682; 3031289 −1.681 |
| Second copy | `onlys-b` was blocked at setup (its host refused the toolchain install), so B+S has **one** valid fresh-seed measurement |

Measurement (every number in this report unless marked otherwise): each strategy runs **separately** against the simulator's compiled 30 bps `VanillaStrategy` on identical seed configs (`default_rng(seed)` draws size U(19,21), rate U(0.6,1.0), sigma U(0.000882,0.001008); `build_config(seed=seed, …)`; price seed = seed, retail seed = seed+1; 20 seeds per `run_batch` call, 8 workers); d = edge(candidate) − edge(NP2) per seed; se = sd(ddof=1)/√n. Calibration: CH (ChengHua926/amm-challenge `Strategy.sol` @ d34a5199) = 525.5258821780834 and NP2 = 526.1155722459862 on seeds 0..999, reproduced by every valid item. Simulator: benedictbrady/amm-challenge @ 6b6921f8d463314aa7c96234e1be25a25245f704.

What the file does, in words:

- **NP2's slow estimator and fee mapping are untouched.** pHat (EMA of fee-implied post-trade spot, alpha 0.27 first print / 0.06 later / 0.12 same-direction second), sigmaHat, lambdaHat, sizeHat, actEma, toxEma, dirState skew, aligned-trade boost, tail compression and the NP 90/10 normalizer blend are exactly NP2's.
- **B adds a fast second estimate (slots 13–15) used only for the stale shift.** On a step's first print it computes a heuristic P(arb) from the innovation relative to a variance state (grown by sigmaHat²·elapsed through silence, capped), the 1.22σ flag, trade ratio and silence, and updates with alpha = P·0.6 + (1−P)·0.08; later prints update it only in the first print's direction (0.06, and a 0.1 normalizer observation when feeUsed > 30 bps). The stale/attract shift is computed from staleHat = 0.7·pHat + 0.3·fastHat instead of pHat.
- **S adds the silence correction to the slow pHat (slot 16).** Slot 16 stores our post-trade spot. On the first print after g = min(elapsed−1, 4) ≥ 1 silent steps, the price must have stayed inside the no-arb band [s(1−bid), s/(1−ask)] quoted after the last print, so pHat moves toward that band's centre by w = 1 − 0.925^g before the slow innovation, and that print's slow alpha and gate are scaled by 1 − 0.30w. The fast estimator is not touched. (Writing slot 16 in `afterInitialize` ran the 250k init gas out; it is left zero and falls back to pHat until the first trade.)

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
        slots[0] = BASE_FEE; slots[1] = BASE_FEE; slots[2] = 0; slots[3] = WAD; slots[4] = 0;
        slots[5] = initialX > 0 ? wdiv(initialY, initialX) : 100 * WAD;
        slots[6] = 950000000000000; slots[7] = 800000000000000000; slots[8] = 2000000000000000;
        slots[13] = 902500000000; slots[14] = slots[5]; slots[15] = 0; slots[9] = 0; slots[10] = 0; slots[11] = 0; slots[12] = 0;
        return (BASE_FEE, BASE_FEE);
    }

    function afterSwap(TradeInfo calldata trade) external override returns (uint256, uint256) {
        uint256 prevBidFee = slots[0]; uint256 prevAskFee = slots[1]; uint256 lastTs = slots[2];
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
            uncertainty += wmul(sigmaForFast, sigmaForFast) * elapsedRaw;
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
            if (g > 4) g = 4;
            uint256 w = WAD - _powWad(925000000000000000, g);
            uint256 s = slots[16];
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
            if (firstInStep) { slots[11] = pHat; slots[12] = pImplied >= pHat ? 1 : 2; }
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

        {
            uint256 ret = fastHat > 0 ? wdiv(absDiff(pImplied, fastHat), fastHat) : 0;
            uint256 alpha;
            if (firstInStep) {
                uint256 processSigma = sigmaForFast;
                uint256 obsVar = uncertainty + wmul(processSigma, processSigma);
                uint256 probArb;
                uint256 z2 = wdiv(wmul(ret, ret), obsVar);
                uint256 density = _powWad(wdiv(WAD, WAD + z2 / 16), 8);
                uint256 sigmaObs = sqrt(obsVar * WAD);
                uint256 odds = wmul(density, wdiv(6700000000000000, sigmaObs));
                bool arbFlag = ret <= wmul(sigmaForFast, 1220000000000000000);
                uint256 prior = arbFlag ? 650000000000000000 : 400000000000000000;
                uint256 tr = trade.reserveY > 0 ? wdiv(trade.amountY, trade.reserveY) : 0;
                if (tr > 3000000000000000) prior = wmul(prior, 6 * WAD / 10);
                if (silent > 1) prior = wmul(prior, 8 * WAD / 10);
                odds = wmul(odds, wdiv(prior, WAD - prior));
                probArb = wdiv(odds, WAD + odds);
                alpha = wmul(probArb, 600000000000000000) + wmul(WAD - probArb, 80000000000000000);
                slots[15] = pImplied >= fastHat ? 1 : 2;
                uncertainty = wmul(uncertainty, WAD - alpha);
            } else {
                if ((slots[15] == 1) == (pImplied >= fastHat)) alpha = PHAT_ALPHA_RETAIL;
            }
            uint256 gate = wmul(sigmaHat, GATE_SIGMA_MULT);
            if (gate < MIN_GATE) gate = MIN_GATE;
            if (ret <= gate) fastHat = wmul(fastHat, WAD - alpha) + wmul(pImplied, alpha);
            slots[13] = uncertainty;
        }

        if (!firstInStep && feeUsed > 30 * BPS && gamma > 0) {
            uint256 normalObs = trade.isBuy
                ? wdiv(wmul(spot, gamma), WAD - 30 * BPS)
                : wdiv(wmul(spot, WAD - 30 * BPS), gamma);
            if ((slots[15] == 1) == (normalObs >= fastHat)) {
                fastHat = wmul(fastHat, 9 * WAD / 10) + wmul(normalObs, WAD / 10);
            }
        }
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

        stepTradeCount = stepTradeCount + 1;
        if (stepTradeCount > STEP_COUNT_CAP) stepTradeCount = STEP_COUNT_CAP;

        uint256 flowSize = wmul(lambdaHat, sizeHat);
        uint256 fBase = BASE_FEE + wmul(SIGMA_COEF, sigmaHat) + wmul(LAMBDA_COEF, lambdaHat) + wmul(FLOW_SIZE_COEF, flowSize);
        uint256 fMid = fBase + wmul(TOX_COEF, toxSignal) + wmul(TOX_QUAD_COEF, wmul(toxSignal, toxSignal)) + wmul(ACT_COEF, actEma);
        fMid = fMid + wmul(SIGMA_TOX_COEF, wmul(sigmaHat, toxSignal));

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

        slots[0] = bidFee; slots[1] = askFee; slots[2] = trade.timestamp;
        slots[3] = dirState; slots[4] = actEma; slots[5] = pHat;
        slots[6] = sigmaHat; slots[7] = lambdaHat; slots[8] = sizeHat;
        slots[16] = spot;
        slots[9] = toxEma; slots[10] = stepTradeCount;

        return (bidFee, askFee);
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

    function getName() external pure override returns (string memory) { return "no_cubic"; }
}
```

### 1.1 Runner-up, confirmed twice on 4,000 seeds: B+S+L

L = slow-path `PHAT_ALPHA_RETAIL` 0.06 → 0.03 (the one semantic change of `ep7-late/later-b`; the fast estimator keeps 0.06). Two independent machines, two seed blocks, same semantics (their byte texts differ, so two hashes):

| Item | Seeds | n | vs NP2 | vs B | Worst seed | SHA-256 |
|---|---|---:|---:|---:|---:|---|
| `ep9-loo/non-a` | 2950000..2953999 | 4000 | **+0.6426 ± 0.0140** | +0.1524 ± 0.0113 | 2953238 −10.52 | `9e2f512a93955eff9c32d8434bb94d5238e312995e257d1fca8c90f31cdc5788` |
| `ep9-loo/non-b` | 2960000..2963999 | 4000 | **+0.6325 ± 0.0145** | +0.1917 ± 0.0270 | 2961301 −4.24 | `508ae3f24d0f042dd621ed7a8f7e90ba35457b1d3c252d980b91a6467648bbec` |

The two copies agree within one combined se. B+S+L is about 0.1 below B+S because L, which gains +0.105 on NP2, loses on B (see §4). If the requester wants a file with two independent 4,000-seed confirmations, this is it; if they want the highest point estimate, B+S is, with one 2,000-seed copy.

### 1.2 Against the requester's own bar

The requester (19:15Z note) submits a file that is ≥ +0.8 over NP2 on 4,000 fresh seeds. B+S is +0.74 on 2,000 seeds; B+S+L is +0.64 on 2×4,000. Neither clears the bar. Recommendation: re-measure B+S's exact file (hash above) on a fresh 4,000-seed block from 3070000 up (every block from 2000000 to 3061999 and 2900000..2909999 has been used; 3070000 up is unused) before any submission. Expected board effect of +0.74 is 518.83 → ~519.6: rank barely moves.

---

## 2. What the leaders' per-run board data says they do differently

Source: `ep2-board/top20-regimes` and `ep2-board/top20-families` (public per-run files, GET `www.paradigm.xyz/puzzles/api/v1/submissions/<id>`, 1,000 runs per entry; the requester confirmed 16:46Z that runs are the same 1,000 seeds in the same order for every entry, so the positional difference d is a true paired difference). Board snapshot 2026-11-07.

| Rank | Board | d vs NP2 | se | worst d | runs lost | retail Y | arb Y | bid bps | ask bps | bid−ask |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 528.399 | +9.570 | 0.063 | +3.59 | 0 | 77,878 | 23,665 | 35.35 | 35.48 | −0.13 |
| 2 | 528.362 | +9.532 | 0.063 | +3.44 | 0 | 77,894 | 23,709 | 35.36 | 35.38 | −0.02 |
| 5 | 528.099 | +9.270 | 0.062 | −5.73 | 1 | 78,057 | 23,717 | 35.22 | 35.27 | −0.05 |
| 10 | 524.658 | +5.829 | 0.049 | +1.42 | 0 | 77,928 | 24,489 | 35.19 | 35.40 | −0.21 |
| 20 | 521.978 | +3.149 | 0.047 | −3.54 | 11 | 79,262 | 25,783 | 34.28 | 33.71 | +0.57 |
| 39 NP2 | 518.829 | 0 | – | – | – | 76,498 | 24,049 | 36.26 | 35.24 | **+1.02** |

What the data shows:

1. **#1 beats NP2 on every one of the 1,000 runs** (minimum +3.59). This is not a tail effect or a regime bet.
2. **The gap scales with retail flow, and is flat as a share of NP2's edge.** By NP2-retail tercile #1's d is 8.13 / 9.54 / 11.04; as a fraction of NP2's own edge it is 1.92% / 1.85% / 1.79%. On a flow-free cut (NP2 arb volume after regressing out retail) d is flat at 9.53 / 9.59 / 9.59. No volatility or arb regime carries it.
3. **The ladder has two separate rungs.** NP2 → #10 is a **retail** rung: +1,430 retail Y, arb +440 Y, d +5.83. #10 → #1 is an **arb** rung: retail −50, arb −824 Y (−3.4%) at a mean mid fee only +0.12 bps higher, d +3.74. Across the top 20, d correlates −0.53 with arb change and +0.20 with retail change. Of #1's +9.57, about 7.1 is taken from the normalizer pool and 2.5 is new edge.
4. **Volume explains less than a third of the gap.** OLS across runs: d(#1) = 6.52 + 0.00187·ΔRetail − 0.00124·ΔArb, R² 0.43: about 2.6 from retail and 0.5 from arb volume, leaving a 6.5 intercept. The leaders earn more per unit of flow, not just more flow.
5. **NP2's fee shape stands out twice, and both are symptoms, not dials.** (a) Its step-end mid fee rises 1.755 bps per 10k retail Y (33.71 / 35.74 / 37.79 by tercile) vs #1's 1.096 (34.12 / 35.45 / 36.68) and #10's 1.013; fee sd 1.97 vs 1.61 bps; correlation with baseline edge 0.92 vs 0.76. (b) A persistent bid-over-ask lean of +1.02 bps (top-5 range −0.13..−0.02), present in every tercile, with per-run skew correlating 0.85 with #1's at the same sd, so the path response is right and the offset is the fault. In busy runs NP2 overprices and loses retail (T3: #1 +2,695 retail); in quiet runs its ask is too cheap and arbs take more (T1: #1 arb −1,278). **Every direct edit of these symptoms lost** (flattening the flow slope −0.09 to −6.5, zeroing the lean −0.035/−0.041, capping bid−ask −47; see §4), which is what tells us they are consequences of a different fee rule.
6. **Tails.** Run 476: d +18.41 with NP2 bid−ask 18.9 bps vs #1's 3.3; run 808: +14.83, 17.0 vs 3.8. NP2 has 90 runs with mean bid > 40 bps vs #1's 39 (max 52.95 vs 43.33).
7. **Families.** Ward clustering on fee statistics puts NP2 and #12 alone in a "high baseline coupling" family; the whole top 10 is one low-variability family. The leaders' code is not public (`houseofjiao`'s public repo is ~3.9 below his board entry).

How this reads with the simulator facts (`ep1-rules/rules`, `ep3-base/decomp`, `ep5-err/err-b`): each step the price moves, exactly one arb attempt hits our pool (and lands the spot exactly at the band edge, revealing the fair price), then all retail orders are routed by a **smooth** share rule against the 30 bps normalizer (at equal reserves: 20 bps → 62.6% of input, 30 → 50%, 40 → 37.4%; no cliff at 30). Fees we return after a print apply to the *next* trade, whatever it is. 98.1% of NP2's arb loss is at gap 1 (a print every step); displacement > 200 bps is 4.7% of arb prints and 35.6% of arb loss. Steps with > 30 bps pre-step pHat error are 19.4% of steps and 63.3% of arb loss. The leaders cut arb by 3.4% at the same mean fee, consistent with quoting by position within the step (the quote left at step end serves the next arb; the quote after a first print serves same-step retail) and with per-side fees set from an expected-edge rule rather than NP2's gap-proportional shift. These are the untested hypotheses of §6.

---

## 3. The ceiling: why estimation cannot close the gap

All measured separately vs Vanilla; oracle items used a patched simulator that appends the true fair price as a seventh calldata word (not submittable).

| Item | Design | n | vs NP2 | arb edge Δ | retail edge Δ |
|---|---|---:|---:|---:|---:|
| `ep3-oracle/oracle-price` | NP2 with pHat := true price, mapping unchanged | 2000 | **−5.39 ± 0.057** | +15.57 | −20.96 |
| `ep2-oracle/oracle-price` | true gap only in tox/side tests, TOX_SCALE 0.9 | 2500 | −2.11 ± 0.04 | +9.39 | −11.50 |
| `ep6-oracle/ceil-b` | true price **plus coordinate re-tune** of STALE_DIR_COEF ×0.75, TOX_COEF ×2, TOX_QUAD_COEF ×3 (grid edge), TOX_BLEND_DECAY ×2 | 2000 | **+1.19 ± 0.051** | +5.98 | −4.79 |
| `ep6-oracle/ev-a` / `ev-b` | true price, affine per-side fees (exposed = a·gap + b, other = c − d·gap) | 2000 | −5.13 ± 0.060 / −5.26 ± 0.065 | −0.34 | −4.79 |
| `ep3-oracle/oracle-full` | fee per side = gap to fair + g (25/25 bps), arb never trades | 10000 | −33.48 ± 0.071 | +28.0 | −61.5 |

Reading: knowing the price exactly saves +9 to +16 of arb loss, more than the whole gap to 1st, but NP2's stale/attract shift (0.685 × gap, both sides) is tuned to a laggy pHat and over-shifts with a correct gap, giving back more retail. Re-tuning the mapping jointly with the true price recovers only **+1.19**. Inside the NP2/CH fee family a *perfect* estimator is worth about +1.2, while 10th needs +5.8. B+S at +0.74 already takes about 60% of that ceiling. The affine and gap+g forms show that a fee rule that blocks arbs loses far more retail than it saves: arbs re-centre the pool, and the exposed side must stay below the gap. The leaders' +9.6 therefore comes from a fee rule NP2 does not have, not from tracking.

---

## 4. Ranked table of every promotion

"Promotion" = a candidate that was measured paired vs NP2 (or vs B) on a fresh block. Ranked by the best valid fresh-seed result. Status: **FINAL** shipped; **CONFIRMED** gain ≥ 2 se on a fresh block; **MARGINAL** < 2 se; **LOST**; **INVALID** (out of gas, or measured head-to-head in one market before the 17:45Z method correction). Head-to-head numbers (both-b +35.0, flat-a +13.0, flat-b +24.6, lean-b +0.385, cap-a) are discarded and listed only as invalid.

| # | Candidate | Base | Item(s) | n | Fresh paired gain | se | Status |
|---:|---|---|---|---:|---:|---:|---|
| 1 | **B+S** (silence correction on stack-b) | B | `ep9-single/onlys-a` | 2000 | **+0.7355** vs NP2; +0.2811 vs B | 0.0175 / 0.0158 | FINAL, one copy (onlys-b blocked) |
| 2 | B+S+L | B | `ep9-loo/non-a`, `non-b` | 4000, 4000 | +0.6426, +0.6325 vs NP2; +0.152, +0.192 vs B | 0.014 / 0.015 | CONFIRMED twice |
| 3 | **B** = stack-b: two-estimator design, fast estimate feeds only the stale shift | NP2 | `ep7-stack/stack-b`; re-measured by `ep9-tune/tune-a`, `tune-b`, `ep9-loo/non-b`, `nol-b`, `ep9-stack/full-b` | 2000; 2000; 2000; 4000; 2000; 660 | +0.4770; +0.4955; +0.4575; +0.4408; +0.4983; +0.4895 | 0.017–0.031 | CONFIRMED on six blocks (pooled ≈ +0.47); arb +3.96, retail −3.49 |
| 4 | B+L | B | `ep9-pair/onlyl-a`, `onlyl-b` | 4000, 4000 | +0.3492, +0.3382 vs NP2; **−0.1314, −0.1433 vs B** | 0.014 / 0.007 | L LOSES on B: drop from B-based files |
| 5 | S alone = silence-a (g ≤ 4, w = 1 − 0.925^g, alpha/gate × (1 − 0.30w)) | NP2 | `ep5-mech/silence-a` | 2000 | +0.2187 | 0.0108 | CONFIRMED on NP2; +0.28 on B |
| 6 | N = next-mix-a (exposed side blended with break-even fee by Poisson P(next trade retail), MIX_M 0.625, MIX_E 1/8) | NP2 | `ep3-mech/next-mix-a` | 4000 | +0.1700 | 0.0074 | CONFIRMED on NP2; **INVALID on B** (gas, see row 15) |
| 7 | L = later-b (slow PHAT_ALPHA_RETAIL 0.06 → 0.03) | NP2 | `ep7-late/later-b`; sweep `ep8-sweep-f27/r03` cell (0.03, 0.27, 0.12) | 2000; 2000 | +0.1051; +0.1031 | 0.0096; 0.0127 | CONFIRMED on NP2 (arb +1.42, retail −1.32); loses on B |
| 8 | stack-a (single-estimator variant of the same ideas) | NP2 | `ep7-stack/stack-a` | 2000 | +0.100 | 0.024 | CONFIRMED but dominated by stack-b |
| 9 | PHAT_ALPHA_RETAIL 0.02 (SAME 0.12 / 0.09) | NP2 | `ep8-sweep-f27/r02` | 2000 (tuning seeds) | +0.0607 / +0.0587 | 0.014 / 0.015 | tuning-seed result; 0.03 is better |
| 10 | skew-off (DIR_COEF = DIR_TOX_COEF = 0) | NP2 | `ep4-lean/lean-b` ablation | 200 | +0.061 | 0.012 | MARGINAL, unconfirmed; candidate gas diet (§6) |
| 11 | prespot-a (blend 95/5 toward pre-trade reserve price on prints with amountY/reserveY ≥ 1%) | NP2 | `ep5-mech/prespot-a` | 2000 | +0.025 | 0.0145 | MARGINAL (t 1.7) |
| 12 | B first-print wR 0.12 (wA 0.6) | B | `ep9-tune/tune-b` | 1024 (tuning) | +0.0200 vs B | 0.0123 | MARGINAL (1.6 se); wR 0.04 −0.081, wA 0.5 −0.048, wA 0.7 −0.003 |
| 13 | B stale blend fast weight 0.2 / 0.4 / 0.1 / 0.5 (B is 0.3) | B | `ep9-tune/tune-a` | 1024 (tuning) | −0.044 / −0.075 / −0.201 / −0.270 vs B | 0.013–0.019 | LOST: B's 0.3 is the optimum |
| 14 | B+S+N+L (full stack) | B | `ep9-stack/full-b` | 660 | +0.311 vs NP2; −0.178 vs B | 0.108 / 0.105 | INVALID/LOST: slow machine; seed 2920436 collapses 309 vs 376 only when S and N are together (ablation: noS 375.7, noN 376.3, noL 309.4) |
| 15 | Any N on B (B+N+L, B+N, B+S+N, B+S+N+L) | B | `ep9-stack/nos-a` −85.9 (n 4000), `nos-b` −48.7 (n 100), `ep9-pair/onlyn-a` −87.8, `onlyn-b` −84.6, `ep9-loo/nol-b` −92.4 (n 2000), `ep9-stack/full-a` −466 | | | **INVALID: out of gas.** B peaks at 242,638 of the 250,000 afterSwap gas (NP2 196,097); N's 24-term Poisson series, square roots and atanh push it over; the engine keeps old fees and reverts the hook's writes on OOG (nol-b counted 6,377,412 OOG calls over 2,000 sims; cand 431.5 vs NP2 523.9). Not a loss of the mechanism: untested on B |
| 16 | sitshift-a / -b (class-specific stale/attract/boost after arb-like vs retail-like prints) | NP2 | `ep6-mech/sitshift-a`, `-b` | 2000 | −0.003 / −0.017 | 0.009 / 0.007 | LOST (flat) |
| 17 | lean-a / lean-b (zero the +1 bps bid-over-ask lean) | NP2 | `ep4-lean/lean-a`, `lean-b` | 2000 / 1024 | −0.035 / −0.041 | 0.003 / 0.006 | LOST (lean-b's +0.385 confirm was head-to-head, invalid) |
| 18 | flat-a / flat-b (damp the flow slope to ~1.1 bps per 10k retail Y) | NP2 | `ep4-flow/flat-a`, `flat-b` | 1024 / – | −0.093 / −0.075 | 0.014 / 0.03 | LOST (their +13.0 / +24.6 confirms were head-to-head, invalid) |
| 19 | arbfirst-a (P(arb)-weighted first-print alpha on the slow path) | NP2 | `ep5-mech/arbfirst-a` | 2000 | −0.14 | 0.017 | LOST |
| 20 | mix-a / mix-b (first-print arb/retail mixture on the slow path, empirical P(arb) table, shift re-tuned) | NP2 | `ep7-mix/mix-a`, `mix-b` | 2000 | −0.305 / −1.25 | 0.027 / 0.032 | LOST (arb +3.43, retail −3.74) |
| 21 | both-a (flatten + zero lean) | NP2 | `ep4-flow/both-a` | 2000 | −1.87 | 0.048 | LOST (both-b's +35.0 was head-to-head) |
| 22 | hard-a / hard-b (hard 1.22σ-type cutoff, wA 0.5) | NP2 | `ep7-mix/hard-a`, `hard-b` | 2000 | −2.44 / −2.62 | 0.033 / 0.038 | LOST (arb +2.0, retail −4.6) |
| 23 | kalman-a (log-price Kalman filter replacing the alphas) | NP2 | `ep5-mech/kalman-a` | 2000 | −3.22 | 0.038 | LOST |
| 24 | unc-a / unc-b (variance grown through silence, Kalman gain on the slow path) | NP2 | `ep7-late/unc-a`, `unc-b` | 2000 | −4.44 / −4.55 | 0.046 / 0.068 | LOST |
| 25 | ev-a / ev-b (affine gap fees with the TRUE price) | oracle | `ep6-oracle/ev-a`, `ev-b` | 2000 | −5.13 / −5.26 | 0.060 / 0.065 | LOST (not a ceiling) |
| 26 | oracle-price (true price as pHat, mapping unchanged) | oracle | `ep3-oracle/oracle-price` | 2000 | −5.39 | 0.057 | LOST (arb +15.6, retail −21.0) |
| 27 | shrink-a / shrink-b (noise-shrunk gap, K·sigmaHat·√(1+elapsed)) | NP2 | `ep6-mech/shrink-a`, `-b` | tuning | −23 and worse for every K > 0 | | LOST |
| 28 | router-a (undercut the normalizer on the favourable side after an arb print) | NP2 | `ep3-mech/router-a` | | −26.7 | | LOST |
| 29 | oracle-full (gap + g fees, arbs blocked) | oracle | `ep3-oracle/oracle-full` | 10000 | −33.48 | 0.071 | LOST (retail −61.5) |
| 30 | cap-a / cap-b (12 bps bid−ask cap with stuck-side pull) | NP2 | `ep4-lean/cap-a`, `cap-b` | | −47 (grid −48..−57 at every cap; pull-only −218) | | LOST |
| 31 | ceil-b (true price + re-tuned mapping) | oracle | `ep6-oracle/ceil-b` | 2000 | **+1.19** | 0.051 | not submittable (needs the oracle feed and inline assembly); the ceiling figure |

Not in the table because their results were not handed or not recorded in the goal's notes: `ep5-mech/evfee-a/-b`, `nextmix-a/-b` (ep5 copies), `arbfirst-b`, `silence-b`, `kalman-b`, `prespot-b`; `ep5-err/err-a`; `ep6-oracle/ceil-a`; `ep7-late/later-a`; `ep8-sweep-f27/r0`, `r01`, `r04` (r04 blocked, no network; r0/r01 summarized in the notes as RETAIL 0 −0.116/−0.120 and 0.01 −0.007/−0.011); the cancelled `ep1-mech`, `ep3-mech` (except next-mix-a and router-a), `ep8-sweep-f22/-f32`, `ep8-stack`.

### 4.1 Structure of the gains

- **Each confirmed gain is a small change to NP2's own gains, or a second estimator that touches only one output.** stack-b's own ablations (n 80, tuning seeds): removing the first-print classifier costs 0.37, removing the later fast updates 0.28, removing variance growth 0.09; the "slow only" control is NP2 exactly.
- **Every rewrite of the slow estimator lost by 0.1 to 5** (kalman, unc, mixture, hard cutoff, shrink, arbfirst), even with the stale/attract shift re-tuned, because NP2's sigma, toxicity, activity and flow signals are all computed from the slow pHat and are tuned to its lag. `ep5-err/err-b` explains the paradox: an arb print reveals the true price exactly (RMS 1e-12 bps), yet raising the first-print alpha from 0.27 loses, because 45% of first prints are retail (67 bps RMS noise) and the fee mapping needs the lag.
- **Gains do not add on B.** S adds +0.28 on B (vs +0.22 on NP2), but L flips from +0.105 on NP2 to −0.14 on B (B's stale shift already uses a fast estimate, so slowing the slow path's later update now hurts), and N cannot be tested on B until something is removed for gas.
- **Where the gains come from:** every confirmed gain trades retail for arb (stack-b arb +3.96 / retail −3.49; later-b +1.42 / −1.32; next-mix arb volume −2.8%, retail −0.6%). The board's #10 rung is a *retail* rung (+1,430 Y retail). Nothing the run built takes more retail.

---

## 5. Method notes the judge should know

- **Head-to-head era (ep3, ep4).** The first briefs said "pair via run_batch" and workers ran `run_batch(candidate, NP2)` in one market, which measures flow stealing, not the board score (both-b showed +35.0 that way and −2.6 vs Vanilla). The requester corrected the method at 17:45Z; every later brief carried the separate-vs-Vanilla recipe, and every number above was checked for it. `ep3-base/harness-a` calibrates the method: a +5 bps BASE_FEE change is −2.68 ± 0.023 on 4,000 seeds and two 2,000-seed blocks agree within 1.2 combined se; per-seed diff sd for small edits is ~0.47, so se on 2,000 seeds is 0.01–0.03.
- **Setup script.** The objective's setup script was refused by the first workers as host inspection (its `uname -sm` / `/proc/self/exe` gate line). From ep3 on, every brief carried the requester's no-gate variant word for word; it worked on every x86_64 Linux host with network. Blocked items (`onlys-b`, `harness-b`, `r04`, the ep1/ep2 items) were host failures, not brief failures.
- **Seed hygiene.** Tuning on 10000..99999; each confirmation on its own never-reused block (10,000 per item) from 2000000 up; used: 2000000..3061999 and 2900000..2909999. Next free block: **3070000**.
- **Gas.** The afterSwap gas limit is 250,000. NP2 peaks at 196,097, B at 242,638, B+S at 236,395 (max successful; `nol-b`'s counter). Any further addition to B needs headroom first.

---

## 6. What the next run should try

In order of expected value.

1. **Design a new fee rule, not a better estimator.** The oracle ceiling (§3) caps NP2's fee family at about +1.2 with a perfect price. The board data (§2) gives the target: +5.8 to #10 is a retail rung at the same mean fee (+1,430 retail Y with arb +440), and #10 → #1 is an arb rung (−824 arb Y at +0.12 bps). Concrete, untested designs: (a) **quote by position within the step** — arb trades first, so the fee returned after a first print serves same-step retail (price it from the smooth router share, which has no cliff at 30 bps), and the fee left at step end serves the next step's arb (price it from sigmaHat and the expected gap); NP2 uses one formula for both; (b) **expected-edge per side** — f maximising f·share(f)·E[flow] − P(arb next)·E[arb loss | gap], with the exact router share from `ep1-rules/rules` and the Poisson P(next is retail) that next-mix-a already computes; (c) **take retail in busy runs** — the leaders' mid fee rises 1.1 bps per 10k retail Y vs NP2's 1.76 and they win T3 by +2,695 retail; flattening the slope *within NP2's mapping* lost, so this has to come from (a)/(b), not from damping the flow terms. Fit any new rule on tuning seeds and judge it only by the fresh-block paired gain; the two board rungs give it a per-tercile target to hit.
2. **Gas diet, then N on B.** B has 7k gas of headroom. Remove dead code first: the dirState skew (DIR_COEF/DIR_TOX_COEF, +0.06 to remove on 200 seeds), `REVERT_U` (constant 0), redundant zero writes in `afterInitialize`; pack slot 16 into slot 2 above the timestamp as `full-b` did; replace the base `sqrt` with the cheaper Newton `_isqrt` `nol-b` verified bit-identical. Then re-test B+S+N on fresh seeds. Expected if additive: about +0.9; but `full-b` saw one seed collapse (309 vs 376) only when S and N are together, so inspect seed 2920436 with the new build before trusting the mean.
3. **A second 4,000-seed copy of B+S** on 3070000..3073999, two machines. Also re-tune S *on B* (S's 0.075 / cap 4 / 0.30 were tuned on NP2) and try separate silence curves for the alpha and the gate (silence-a's own `next`).
4. **B's first-print retail weight wR 0.12..0.16** (+0.020 at 1.6 se at 0.12; 0.04 and wA changes lose). Small, cheap, needs ≥ 2,000 tuning seeds per cell.
5. **Look at the tails.** L's worst seeds under NP2 are −8 to −13 (10870, 10846 recur across every sweep cell); B+S+L's worst is −10.5 (2953238). A mechanism that loses 10 on 1 seed in 1,000 costs 0.01 of mean; finding why may expose where the slow pHat gets stuck.
6. **Do not retry:** every slow-estimator rewrite (Kalman, variance growth, mixture, hard cutoff, noise shrink, class shifts), flow-slope flattening, lean zeroing, bid−ask caps, router undercutting, affine or gap+g oracle fee forms.

---

## 7. What is missing

- A second fresh-seed copy of the FINAL file (B+S): `onlys-b` was blocked at setup. One 2,000-seed measurement is the only evidence for +0.74; the parts are each confirmed separately (B on six blocks, S on NP2 and on B+L twice).
- The requester's submission bar (≥ +0.8 on 4,000 fresh seeds) is not met by any file.
- The top-10 target (+5.8) and the 1st-place target (+9.6) are not met and, per §3, cannot be met inside NP2's fee family. The run did not get to designing a new fee rule.
- N (next-mix-a, +0.17 on NP2) is unmeasured on B for gas reasons.
- Results never handed: ep5-mech's second copies and evfee items, ep6-oracle/ceil-a, ep7-late/later-a, ep5-err/err-a.

## 8. Results this write-up rests on

Hashes of the handed result files are those listed in the task; cited by batch/item: `ep1-rules/rules` (simulator rules), `ep2-board/top20-regimes`, `ep2-board/top20-families` (board data), `ep3-base/decomp`, `ep3-base/harness-a` (edge decomposition, method calibration), `ep3-oracle/oracle-price`, `ep3-oracle/oracle-full`, `ep6-oracle/ceil-b`, `ep6-oracle/ev-a` (ceilings), `ep3-mech/next-mix-a`, `ep5-mech/silence-a`, `ep5-mech/kalman-a`, `ep7-late/later-b`, `ep7-mix/mix-a`, `ep7-stack/stack-b`, `ep4-flow/flat-a`, `ep4-lean/lean-b` (mechanisms), `ep5-err/err-b` (pHat error diagnosis), `ep8-sweep-f27/r02`, `r03` (alpha sweep), `ep9-stack/full-b`, `nos-a`, `ep9-loo/non-a`, `non-b`, `nol-b`, `ep9-pair/onlyl-a`, `onlyl-b`, `ep9-single/onlys-a`, `ep9-tune/tune-a`, `tune-b` (final stacks). Other figures (stack-a, hard-a/b, unc-a/b, arbfirst-a, prespot-a, sitshift, shrink, router-a, cap, both-a, lean-a, ev-b, the ep2 oracle-price, onlyn-a/b, full-a, nos-b) come from the orchestrator's episode notes in the goal state, which recorded them when those items were handed in earlier episodes.

Key hashes: NP2 `51f1c1a9d4999ee460eb8bbc66880da8074b173399a4f5d71f96671482e18ac0` (TWO + NP's interior-routing block, 526.1155722459862 on 0..999); CH `6dd68f77a70900319460215374143dbd5d924198450a46d9f5f91f6b1e3d35c3` (525.5258821780834); stack-b `218426004abed3b6cb69f4ef133fea8e4789ddbeae37bd11e94e5ffc5f2a77cb`; later-b `91fe9cb4553c4781f1c6e1ac3d5a036e5c0ebe09bd4ed67a2f4c059647e54fcc`; next-mix-a `1e8a7601c5c0622e870e80308f2ab7aa5a58361358e7926f96735c31f6321a5b`; B+L `d052c0a7dcbcd931aa683eaa7f109c39980f4f8664022b35d27a5cad5978785a`; B+S (FINAL) `a9830b417dd43806c144e8b4a217cda1317850bb52578b18a3237307cf8dfa16`; B+S+L `9e2f512a93955eff9c32d8434bb94d5238e312995e257d1fca8c90f31cdc5788` / `508ae3f24d0f042dd621ed7a8f7e90ba35457b1d3c252d980b91a6467648bbec`.
