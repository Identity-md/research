# Paradigm AMM fee challenge: goal write-up

Goal: take this network to 1st on Paradigm's AMM fee challenge (https://www.paradigm.xyz/puzzles/amm), simulator `benedictbrady/amm-challenge` at commit `6b6921f8d463314aa7c96234e1be25a25245f704`.

**Outcome in one line.** The best file is "NP": the public ChengHua926 strategy plus a nine-line normalizer-spot observation written by this network. It beats the 50 bps starter by about +156 edge, the previous best (CH) by +0.46 edge (29 standard errors), and scores 526.03 on seeds 0..999 locally. That maps to roughly 10th on the board, not 1st. First place (528.40 on the board) needs about +3.5 more edge locally, and no measured candidate in rounds 3 and 4 came close. The goal ran ten episodes, 124 of 600 items, three promotions, and ended because the last episode was reached. Round 4 (31 items) and the requester's priority combination (NP2 = NP + two-print) never produced a measurement, for toolchain reasons described in section 8.

---

## 1. The best Strategy.sol (NP), ready to submit

- **SHA-256:** `f1ea5b95c853ef28399a0b22ec222773525dba18c92282c04993170c97b57c83` (9,870 bytes, trailing newline; recomputed from the result's `code` field while writing this report and equal to the item's `code_sha256`).
- **Source item:** `r3-f1/norm-phat` (result `.imd/reads/artifacts/b19-norm-phat`, SHA-256 `da313379…`).
- **Base:** CH = `ChengHua926/amm-challenge` commit `d34a5199c59a4c44d5336a25f1436b4ae1f21104`, `contracts/src/Strategy.sol`, SHA-256 `6dd68f77a70900319460215374143dbd5d924198450a46d9f5f91f6b1e3d35c3`. NP is CH with the block at lines 98–105 below inserted immediately before `uint256 tradeRatio = ...`; nothing else differs.
- **Checks reported by the item:** `amm-match validate` passed ("Strategy 'no_cubic' validated successfully!"); storage slots 0..10 only; no new loops (the only loop is CH's exponentiation by squaring with the exponent capped at 8); 3,000 synthetic swaps all succeeded under the 250,000 gas limit (initialization 185,532 gas; max afterSwap 94,268 gas measured by pyrevm).
- **Name:** `getName()` still returns `"no_cubic"`, inherited from CH. Renaming it changes the SHA-256 but not the behaviour or the score.
- **Rebuild check:** a file rebuilt from CH's raw URL plus the inserted block is NP if it scores exactly `526.0337302497852` on seeds 0..999 with the default config (runs are bit-reproducible across machines, see section 6). Its SHA-256 matches only if the formatting is identical; r4-m1/calib-b's never-compiled rebuild hashed `95d21646…` because of whitespace alone.

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
        slots[9] = 0; slots[10] = 0;
        return (BASE_FEE, BASE_FEE);
    }

    function afterSwap(TradeInfo calldata trade) external override returns (uint256, uint256) {
        uint256 prevBidFee = slots[0]; uint256 prevAskFee = slots[1]; uint256 lastTs = slots[2];
        uint256 dirState = slots[3]; uint256 actEma = slots[4]; uint256 pHat = slots[5];
        uint256 sigmaHat = slots[6]; uint256 lambdaHat = slots[7]; uint256 sizeHat = slots[8];
        uint256 toxEma = slots[9]; uint256 stepTradeCount = slots[10];

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

        {
            uint256 ret = pHat > 0 ? wdiv(absDiff(pImplied, pHat), pHat) : 0;
            uint256 alpha = firstInStep ? PHAT_ALPHA : PHAT_ALPHA_RETAIL;
            uint256 adaptiveGate = wmul(sigmaHat, GATE_SIGMA_MULT);
            if (adaptiveGate < MIN_GATE) adaptiveGate = MIN_GATE;
            if (ret <= adaptiveGate) { pHat = wmul(pHat, WAD - alpha) + wmul(pImplied, alpha); }
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
            uint256 staleShift = wmul(STALE_DIR_COEF, toxSignal);
            uint256 attractShift = wmul(staleShift, STALE_ATTRACT_FRAC);
            if (spot >= pHat) {
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

### What the inserted block does

Every retail order is split by the simulator's router between our pool and the fixed 30 bps normalizer so that fee-adjusted marginal prices equalise. A print that is not the first in its step cannot be the step's arbitrage trade, so our post-trade spot `s` and the fee used, `g = 1 − feeUsed`, give the normalizer's post-trade spot: `n = s·g/0.997` when we bought X, `n = s·0.997/g` when we sold X. That is a second, noisy observation of the fair price (clipped splits and retail that moved the normalizer off its band make it noisy), so it is blended into `pHat` with weight 0.1 rather than used as a clamp. The item verified the inversion numerically on 16,936 random interior splits (max relative error 1.1e−15). On tuning seeds 10000..10499 (n 500) the alternatives lost: blend 0.3 −0.83 (se 0.08), blend 0.5 −6.03 (se 0.20), hard clamp of `pHat` into the normalizer's band −23.5 (se 0.93); blend 0.1 won at +0.42 (se 0.03) and was frozen before the holdout.

## 2. Paired gains of NP

All paired numbers are candidate minus reference on identical seeds (same per-seed parameter draws and same price and retail RNG streams), each strategy simulated separately against the fixed 30 bps normalizer, never against each other. se = sample standard deviation of the per-seed differences / sqrt(n).

| Comparison | Seeds | n | Mean diff | se | diff / se | 5 worst runs (seed: diff) | Source |
|---|---|---|---|---|---|---|---|
| NP vs CH (previous best) | 600000..601999 | 2000 | **+0.4645** | 0.0159 | 29.3 | 601271: −4.58; 601909: −3.01; 601666: −2.37; 601072: −2.26; 600393: −2.15 | r3-f1/norm-phat |
| CH vs StarterStrategy (50 bps) | 600000..601999 | 2000 | +155.80 | 0.909 | 171 | 600945: +76.97; 601402: +78.67; 600215: +79.02; 601394: +80.15; 600250: +80.32 | r3-d2/tune-tox `paired_vs_starter` |
| **NP vs StarterStrategy, same seeds (sum of the two rows above)** | 600000..601999 | 2000 | **+156.26** | 0.91 (bounds 0.89–0.93) | ~172 | not computable per seed from the handed results; every per-seed CH−starter difference is ≥ +76.97 and every NP−CH difference ≥ −4.58, so every one of the 2,000 NP−starter differences is ≥ +72.4 | derived |
| NP vs StarterStrategy, chain across blocks | mixed | — | +156.12 | 0.947 | — | — | YQ +154.69 (se 0.946, 100000..101999) + CH +0.962 (se 0.0212, 400000..401999) + NP +0.4645 (se 0.0159, 600000..601999); se = root of summed squares |
| NP vs YQ (promotion 1), chain | mixed | — | +1.43 | 0.027 | — | — | +0.962 + 0.4645 |

The per-seed NP−starter differences on 600000..601999 are exact sums of two measured per-seed series, so the mean +156.26 is exact; only the standard error of the sum needs the covariance, which the handed results do not carry, hence the bounds (se between 0.909 − 0.016 and 0.909 + 0.016). The direct measurement that would have replaced the derivation, r4-m1/replicate (NP vs CH, YQ and starter on 800000..801999), was still running at the last episode and was not handed.

Absolute scores of NP (unpaired, default config):

| Seeds | n | Mean edge | se |
|---|---|---|---|
| 0..999 (the `amm-match run --simulations 1000` set) | 1000 | 526.0337302497852 | 2.79 |
| 900000..909999 (requester's calibration set) | — | not measured: r4-m1/calib-a never landed, calib-b blocked at setup, r5-pri/combo-calib-a blocked at setup | — |

## 3. Ranked table of every promotion

Three promotions were made, each on a fresh block that no tuning had used, each clearing twice its standard error. Ranked by order of promotion (which is also the order of absolute score):

| # | Episode | File | SHA-256 | Reference | Fresh block | n | Paired gain | se | Worst run | Score 0..999 | Calibration 900000..909999 (n 10000) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 4 | **YQ** = `jiayaoqijia/amm-challenge-yq` `3e9dc7d5a6192c88b562a0f8d9c172ca566ec94d` `contracts/src/Strategy.sol` (byte-identical replica, r1/public-replica) | `00fae418c49cd681ad0879c6f96ebed0163fab5a660b38030f11e6947a39afd4` | StarterStrategy 50 bps (`8f2cea337f6736105f58c6758da6c3ebf002951d34492bcd5b7101bef2d1e7f3`) | 100000..101999 | 2000 | **+154.69** | 0.946 | 101573: +74.78 | 524.6271111458843 (se 2.78) | 522.5203 (se 0.917) |
| 2 | 6 | **CH** = `ChengHua926/amm-challenge` `d34a5199c59a4c44d5336a25f1436b4ae1f21104` `contracts/src/Strategy.sol` (r2-measure/pub-chenghua) | `6dd68f77a70900319460215374143dbd5d924198450a46d9f5f91f6b1e3d35c3` | YQ | 400000..401999 | 2000 | **+0.962** | 0.0212 | 401412: −4.28 | 525.525882178 (se 2.79) | not handed (r3-m1/ch-calib still running) |
| 3 | 8 | **NP** = CH + normalizer-spot observation (r3-f1/norm-phat; this network's change) | `f1ea5b95c853ef28399a0b22ec222773525dba18c92282c04993170c97b57c83` | CH | 600000..601999 | 2000 | **+0.4645** | 0.0159 | 601271: −4.58 | 526.0337302497852 (se 2.79) | not measured (see section 2) |

Replications: YQ vs starter was re-measured by a different worker on 500000..501999 at +154.95 (se 0.940, r2b-a/tune-asym `best_paired_starter`); CH vs starter directly at +155.80 (se 0.909) on 600000..601999 (r3-d2/tune-tox). CH's own score on 0..999 was reproduced to the last digit by six separate items (pub-chenghua, norm-phat, two-print, ablate, gate-grid, tune-tox). CH is YQ retuned without the cubic toxicity term (faster decays ACT/SIZE 0.53, DIR 0.75, SIGMA 0.69; `PHAT_ALPHA` 0.27/0.06; gate 7.2 sigma with a 3 % floor; `BASE_FEE` 4 bps; `TRADE_TOX_BOOST` 3500 bps; `STALE_ATTRACT_FRAC` 1.05). ChengHua's own "params_cubic_2" variant measured −0.021 (se 0.012) against the no-cubic file, so the cubic term is dead weight.

## 4. Where NP stands against the board

- Board on 2026-11-07 (official API, 743 entries, 1000 simulations each, r1 notes and m5-map/board-map): 1st 528.399 (0xMai), 2nd 528.323, 3rd 528.258, 4th 528.206, 5th 528.099; 10th 524.658.
- Board-to-local map (m5-map/board-map, medium confidence): the pinned commit equals upstream `main` (zero later commits), the About page's parameters match the pinned config (sigma displayed rounded), and three fixed-fee anchors on the board score 338.60 (30 bps; local 342.26), 367.18 (starter 50 bps; local 367.92) and 378.94 (75 bps; local 380.1). YQ's README claims 523.21 on the board against 524.63 local. So **board ≈ local(0..999) − 0.7 to −3.7**. The README's "30 bps = 522.13" is that author's local cross-seed mean of their own entry's row, not a board score of a fixed 30 bps strategy; it does not indicate a simulator mismatch.
- NP at 526.03 local therefore maps to about 522.3–525.3 on the board: around 10th place (524.66) at best. **First place needs about 529.5–530 local, +3.5 over NP. Not reached.**
- The requester's own submit rules were not met either: "+0.8 over CH on 4,000 fresh seeds" (NP is +0.46; NP2 was never measured) and "+2 over YQ with a change of ours" (NP is +1.43). The requester's calibration marks of 525, 527 and 528 on seeds 900000..909999 were not reached by any file measured there (YQ 522.52; CH and NP were not measured there).
- The leaderboard and per-submission API endpoints return different `avgEdge` for the same submission id (starter 367.18 vs 364.06; the cause is undisclosed); this report quotes the leaderboard field.

## 5. Candidate scoreboard

Every candidate that was measured, with its paired difference against the best of its round. Items with n = 0 (toolchain blocked) are listed in section 8, not here; the requester ruled that an unmeasured item is never ranked.

### 5.1 Deltas on CH (fresh block 600000..601999 unless noted; tuning on 10000..11999)

| Item | Change | SHA-256 (prefix) | n | Mean diff vs CH | se | Verdict |
|---|---|---|---|---|---|---|
| r3-f1/norm-phat | normalizer-spot blend 0.1 into pHat on later-in-step prints | f1ea5b95 | 2000 | **+0.4645** | 0.0159 | promoted (NP) |
| r3-f1/two-print | later print in the same step moving pHat the same way as the first uses alpha 0.12 instead of 0.06 (slots 11–12) | 6f23c204 | 2000 | **+0.248** | 0.0128 | clears 2 se; never combined with NP in a measured file (NP2 blocked) |
| r3-d3/fees-used | first-in-step alpha 0.20 instead of 0.27 when the implied return exceeds 2·sigmaHat | d6666c0c | **300** | +0.299 | 0.038 | promising but n below the 2000 rule (single-core machine); 0..999 unpaired 525.80 |
| r3-s1/ablate | CH minus the `SIGMA_TOX_COEF` term | 362d6ac9 | 2000 | +0.0014 | 0.0014 | free simplification, no score gain |
| r3-d1/gate-grid | gate multiplier 7.2 → 5 (best of 25 cells, in-sample +0.044) | ca996acf | 2000 | −0.014 | 0.015 | in-sample gain vanished out of sample; gate is at a local optimum |
| r3-d1/highfee | cap fMid at 250 bps | 61d76ecd | 300 | −0.025 | 0.012 | loses; high fees are protective |
| r3-d1/kalman-gate | variance-tracked innovation gate (R1 6, R2 25, G 5) | eec01c7d | 2000 | −0.211 | 0.015 | loses on CH although the same idea gained +0.196 on YQ |
| r3-d3/sigma-elapsed | elapsed-normalised variance estimator for sigma | 3d8dfb6a | 2000 | −0.287 | 0.018 | loses |
| r3-d2/tune-tox | coordinate search over six toxicity constants at ±10 %/±25 %, 500 seeds per cell, two passes | b34fe8bc (= CH with the power loop unrolled) | 2000 | 0.000 | 0 | no step cleared 2 se; the frozen endpoint is CH |
| r3-d2/tune-base (ep10 notes) | five base constants at ±25 %, n 500 per cell | — | — | every direction negative (LAMBDA_COEF −25 %: −2.11; SIGMA_COEF ±25 %: −0.54; BASE_FEE −25 %: −0.20) | — | CH returned unchanged |
| r3-d2/tune-est, cma-residual (ep10 notes) | estimator constants; CMA-ES over 33 constants on a 1-CPU machine | — | 30 / 6 per cell | nothing clears; every CMA candidate 0.4 to 10 below CH | — | CH sits in a sharp basin |

### 5.2 Public files measured against CH (r3-m1/pub-scan, 13 files; r2-measure/pub-chenghua)

| Repo and commit | SHA-256 (prefix) | Seeds | n | Mean diff vs CH | se |
|---|---|---|---|---|---|
| houseofjiao/amm-challenge 4f41eb91 | 07d5510d | 600000.. | 2000 | −0.006 | 0.024 |
| ChengHua926 params_cubic_2 (derived) | d957a8ed | 400000.. | 2000 | −0.021 | 0.012 |
| 0xniki/amm-challenge 56ca9d16 | 74229c65 | 600000.. | 2000 | −1.317 | 0.033 |
| The-CTra1n/amm-challenge cd1bf7bc | 08add619 | 600000.. | 2000 | −2.913 | 0.043 |
| atvinicius/amm-challenge 78752c17 | c6a81364 | 0.. | 200 | −5.81 | 0.12 |
| solosage1/amm-challenge 99dc1cfd (TmpFinal.sol) | aebe13d0 | 0.. | 200 | −14.60 | 0.20 |
| eliizabethzhang/market-making-challenge 7156ff03 | acd9e80d | 600000.. | 2000 | −17.73 | 0.37 |
| alexanderzliu/amm-challenge e15b10d2 | 72e777f2 | 0.. | 200 | −35.75 | 0.50 |
| VictorQian03/amm-challenge d0398512 | 4c39e3c2 | 0.. | 200 | −125.3 | 1.6 |
| 0xpranav62/amm-challenge 4e24ad7e | 6baac9c7 | 0.. | 200 | −143.6 | 2.4 |
| lumen-dev-a11y/amm-challenge-lab 4eae7bd9 (fixed 55 bps) | 9af0bc49 | 0.. | 200 | −154.2 | 2.7 |
| kmadorin/amm-challenge ec151d5a (fixed 30 bps) | f0999aff | 0.. | 200 | −185.4 | 3.3 |
| giorgoschionas/amm-challenge 61ba5df1 (fixed 25 bps) | 6fd32f2c | 0.. | 200 | about −207 | — |

No public file beats CH. houseofjiao is a CH twin within noise.

### 5.3 Deltas on YQ (round 2; fresh blocks 400000..401999 or 500000..501999)

| Item | Change | n | Mean diff vs YQ | se |
|---|---|---|---|---|
| r2-measure/pub-chenghua (CH) | public retune without cubic tox | 2000 | **+0.962** | 0.021 |
| r2-fresh-a/kalman | Kalman innovation gate | 2000 | +0.196 | 0.014 |
| r2-deep-b/tune-decay | DIR 0.7 / ACT 0.6 / SIZE 0.6, toxEma capped after a gap | 1200 | +0.182 | 0.017 |
| r2-deep-b/retail-alpha | gate multiplier 10 → 5 | 300 | +0.237 | 0.037 |
| r2-simplify/ablate | YQ minus cubic tox, dir skew, sigma·tox | 2000 | +0.019 | 0.007 |
| r2b-a/tune-asym | six asymmetry constants retuned by coordinate search (36 trials) | 2000 | −0.010 | 0.0066 |
| r2-fresh-b/vol-redo (hybrid) | online sigma replacing YQ's | 2000 | −0.061 | 0.007 |
| r2-measure/pub-shl0k28 (9c4be0b6) | public file claiming 525.08 | 2000 | −0.177 | 0.298 (blow-up seeds −334, −310, −308) |
| r2-deep-a/lambda-fix | retail intensity from non-first prints | — | −1.27 | — |
| r2b-b/freeze-est | sigma frozen at the midpoint | — | −2.51 | — |
| r2-fresh-b/linear-cma | 8-coefficient linear policy, CMA-ES | — | −3.16 | — |
| dipankar SigmaAdaptive (84da373d) | public, README claims 526.54 | 2000 | −5.05 | 0.041 |
| r2-deep-a/alpha-first | PHAT_ALPHA 0.5 / 0.75 / 1.0 | — | −12.4 / −53 / −120 | — |
| r2b-b/yq-lite | 6-slot simplification | — | −17.5 | 0.08 |
| r2-fresh-a/phase | tight after first print, wide after later ones | 30 | −25 | — |
| th-a/th-local | standalone per-side local expected-edge maximiser | — | −134.6 | — |
| dipankar WinningV5 (dc8dff68) | public | 2000 | −232.9 | 1.18 |
| r2-fresh-a/arb-class | arb label by band-edge consistency | — | −305 | — |

YQ ablation costs (r2-simplify/ablate, removal alone): stale shift −115.6, lambda term −39.8, activity −1.86, flow-size −1.04, trade boost −0.42, tail −0.13; cubic tox, dir skew and sigma·tox are free. CH's ablation (r3-s1/ablate, n 1000 on 10000..10999): lambda −38.4, ACT −1.70, TOX_QUAD −1.29, trade boost −0.71, flow-size −0.70, tail −0.33, dir skew −0.018, sigma·tox −0.002.

### 5.4 Round 1: standalone mechanisms against the starter (fresh block 100000..101999, or 300000..301999 for r1x)

| Item | Mean diff vs starter | se | Score 0..999 |
|---|---|---|---|
| r1/public-replica (YQ) | **+154.69** | 0.95 | 524.63 |
| r1/router-optimal (router-marginal pricing + arb-loss term + inferred normalizer spot) | +149.46 | 0.92 | 519.29 |
| r1x/edge-max (closed-form expected-edge table) | +147.19 | 0.84 | 517.53 |
| r1/flow-estimate | +124.42 | 0.86 | — (its adaptive lambda/size table added 0.000 ± 0.06 over a constant control) |
| r1/size-toxicity | +115.20 | — | — |
| r1/inventory | +104.49 | — | — |
| r1/fair-centered | +66.84 | — | — |
| r1/example-tuned | +65.71 | — | — |
| r1/band-state | +10.78 | — | — |
| r1x/param-lookup | +10.73 | — | — |
| r1x/arb-vol | +10.66 | — | — |
| r1/static-grid best fixed pair 75/75 (5837798b) | +10.61 | 0.16 | 380.14 (75 vs 80: +0.106, se 0.026) |
| r1/bandit | +9.91 | — | — |
| r1x/one-sided | +3.13 | — | — |
| r1/interval-tracker | 524.13 on 0..999, below YQ; its "+6.40 vs YQ" was a head-to-head market, not our paired measure | — | 524.13 |
| r1/vol-estimate | n 0 (no toolchain); the rerun as vol-redo is in 5.3 | — | — |

Lesson from rounds 1 and 2: every standalone mechanism landed 5 to 150 edge below the YQ family, so from round 3 on only deltas on the best were built. theory/fees gives the reason the fixed-fee optimum is broad (74–82 bps, driven by retail displacement, not sigma) and the post-arb local optimum (after a bid-side arb at a 30 bps band: bid 58.6 / ask 16.2 bps, relaxing to 26/26 over about 32 silent steps), which the YQ family's stale shift and attract discount approximate.

## 6. Method

- **Simulator and seeds.** Pinned commit `6b6921f8`, Rust engine `amm_sim_rs` built with maturin, solc 0.8.24 via py-solc-x, pyrevm; 10,000 steps per simulation; per-simulation parameters drawn by `numpy.default_rng(seed)` in the order retail mean size U(19,21), arrival rate U(0.6,1.0), sigma U(0.000882,0.001008) (`MatchRunner._build_configs`); the Rust engine seeds the price path with `seed` and retail with `seed+1`. `amm-match run --simulations N` is therefore seeds 0..N−1, and explicit seed ranges were run through `amm_sim_rs.run_batch`. Several items checked their config builder field by field against `MatchRunner._build_configs`.
- **Reproducibility.** Two independent machines scored VanillaStrategy and StarterStrategy on seeds 900000..909999 and agreed to every printed digit (vanilla 342.26191722896806 se 0.5176; starter 367.91606344584477 se 0.5900), and CH's 525.525882178 on 0..999 was reproduced by six items. Local runs are bit-reproducible across machines, so paired comparisons made by different items on the same seeds are valid.
- **Pairing and the promotion rule.** Each candidate and its reference were run separately against the fixed 30 bps normalizer on identical seeds; the per-seed difference is the statistic. Tuning used only seeds 0..99999 (round 3 on 10000.., round 4 on 30000..). Each episode had its own fresh confirmation block (e·100000 .. e·100000+1999) that no tuning touched; a candidate was promoted only when its paired mean difference on that block was at least twice its standard error with n ≥ 2000. The requester's calibration set 900000..909999 was never used to choose.
- **Scoreboard.** Kept in the orchestrator's notes each episode (file SHA-256, score, every candidate's paired difference); the tables in section 5 are that scoreboard.
- **Costs.** 0.02–0.2 s per simulation on 8–32 workers; 0.6–0.8 s on single-core machines, which is why three items (fees-used, highfee, tune-est) report n far below 2000.

## 7. Repository

The goal's trunk is `https://github.com/identity-md-launches/goal-3094-take-network-1st-paradigm-s`, commit `5527a7f080e1e5c10f4a3a454e61a1a107052259` (wave r1 merged: layout, 13 round-1 candidates under `candidates/<key>/`, `tools/pair.py`, `tools/README.md`, the starter as `best/Strategy.sol`). The code wave `r4-trunk`, whose single item was to write NP into `best/Strategy.sol` and `best/SCOREBOARD.md`, was still running at the last episode and was not merged, so **the trunk does not hold NP**; the authoritative copy of NP is the source in section 1 and the `code` field of `r3-f1/norm-phat`. The r1 wave took most of the goal's wall clock to merge, so rounds 2–5 ran as research batches whose results carry the full `.sol` in JSON; the best file travelled between items as "CH raw URL + the exact edit".

## 8. What is missing and why

1. **First place.** Not reached; NP is about +3.5 local edge short. The requester's submission thresholds (+0.8 over CH on 4,000 fresh seeds; +2 over YQ) were not met.
2. **Round 4 (31 NP deltas, batches r4-d1/d2/d3, r4-f1/f2, r4-s1, r4-m1) produced no measurement.** The ten results handed back (np-two, np-sigma, np-lambda, np-first, np-nhat, np-clip, fill-rate, exact-stale, phase2, lite9) and r4-m1/calib-b were all blocked at the setup script with n 0: eight at `tar: Cannot change ownership to uid 1001: Invalid argument` while extracting the uv archive on machines that run tar as root in a container (fixed by the requester on 05:19Z with `tar --no-same-owner`, after the briefs had been sent); np-lambda because micromamba's archive needs `bzip2`, absent; fill-rate because rustup needs procfs; np-first because the machine was a Mac. The other 20 items were still running at the end.
3. **NP2 = CH + norm-phat + two-print (the requester's 04:55Z priority, batch r5-pri at 4,000 fresh seeds plus calibration)** was never measured: the one handed item (combo-calib-a) blocked at the same tar step, the other three were cancelled in the last episode with no episode left to read them. The two edits touch the same pHat update, so whether their gains add (+0.46 and +0.25 on the same block, worst seeds partly shared: 601909 and 601072 appear in both lists) is unknown.
4. **Calibration of CH and NP on 900000..909999** (r3-m1/ch-calib, r4-m1/calib-a) did not land; the requester's 525/527/528 marks could only be checked for YQ (522.52).
5. **r4-m1/replicate** (NP directly against the starter and YQ on 800000..801999) did not land; the starter gain in section 2 is derived from two same-seed measurements.
6. **Blocking rate.** About 40 % of all build items never ran the simulator. Causes in order: no pip/rustc/maturin on the machine (round 2), the uv installer writing outside the workspace and TMPDIR not surviving between commands (round 3), Python 3.14 above PyO3 0.22's limit, Linux arm64 having no solc binary, no C compiler, no /proc, and finally the tar ownership error (round 4). Deviation to state: the briefs carried a compressed same-step version of the requester's 04:44Z setup script (uv release binary, micromamba gcc or ziglang cc when `cc` is missing, rustup minimal into `scratch/`, `uv venv --python 3.12`, Linux x86_64 only) because the full script plus a task did not fit the 3,000-character brief; that version lacked the `--no-same-owner` flag.
7. **One episode (7) carried nothing out:** its two batches were refused because the brief used a `{{key}}` placeholder the items' vars did not define.

## 9. What the next run should try

In order of expected value per item, all as deltas on NP, measured paired on ≥ 2,000 fresh seeds with the fixed setup script (`tar --no-same-owner -xz` for uv and `-xj` for micromamba, python `tarfile` as the bzip2 fallback, an early stop on machines without `/proc/self/exe`, `uv venv --python 3.12`, block at once on Linux arm64 and on macOS):

1. **NP2 = NP + two-print**, measured on 4,000 fresh seeds (1000000..1003999) by two items with identical SHA-256, plus its calibration on 900000..909999 in two halves. Expected +0.2 to +0.7 over NP if the edits add; this alone decides whether the requester submits.
2. **fees-used on NP** (first-in-step alpha 0.20 when the implied return exceeds 2·sigmaHat): confirm on the untouched 1,700 seeds 600300..601999, then grid alpha in {0.10, 0.15, 0.20, 0.24} × K in {1.5, 2, 3} on ≥ 2,000 tuning seeds per cell.
3. **Normalizer-spot refinements** (the only new mechanism that paid): blend weight 0.05–0.2 on ≥ 2,000 seeds per cell; apply the observation to the third and later prints with a smaller weight; use the inferred normalizer spot to set the attract-side discount directly (undercut the 30 bps pool by the amount the router needs, r1/router-optimal's idea) instead of CH's fixed `STALE_ATTRACT_FRAC`; feed the normalizer band `[n·0.997, n/0.997]` as a soft prior into the gate rather than as a clamp (the hard clamp lost 23.5).
4. **Rerun the 20 unmeasured round-4 ideas** with the fixed script: np-weight, np-size, np-lowfee, np-alpha, np-move, np-attract, np-silence, np-arbreset, side-asym (bid/ask-specific stale constants from the fixed-X versus fixed-Y router asymmetry that theory/fees derived), uncensor, regress, th-killed (killed-kernel relaxation of pHat in silence, theory/fees section 3), edge-base, warmup, recenter, strip, tail-one, replicate, calib-a; and the blocked ones np-two, np-sigma, np-lambda, np-first, np-nhat, np-clip, fill-rate, exact-stale, phase2, lite9.
5. **Stop spending items on CH's constants.** tune-tox, tune-base, tune-est, gate-grid, tune-asym and cma-residual all show the YQ/CH constants at a sharp local optimum; in-sample gains of +0.04 over 25 cells vanished out of sample. Constant tuning needs ≥ 4,000 seeds per cell and a second tuning split before freezing, and even then is worth at most tenths.
6. **First place needs a new mechanism, not tuning.** The +3.5 gap is seven times the largest delta found. Candidates not implemented anywhere public (writeups batch): a censored Bayesian fair-price posterior that uses silence (no arb at a step means p stayed inside our band, a killed-kernel relaxation with variance saturating at W²(1/4 − 2/π²)); router-censored joint inference of lambda and size from our fill share (fill-rate); closed-form expected-edge maximisation per side including next-step arb cost (theory/fees' objective J, which th-local implemented standalone at −134.6 but which was never tried as a delta on the YQ family's estimators); and a heavy-tail-aware paired estimator for selection, since holdout losses concentrate in a few seeds (601728: −19.2 in gate-grid, 600845: −16.2 in sigma-elapsed).
7. **Give every important idea two items under different keys** on different machines, and read `blocked` before counting an idea as tried.

## 10. Sources

Results this report rests on (all under `.imd/reads/artifacts/`, SHA-256 prefixes): b19-norm-phat (da313379), b19-two-print (528a6da7), b18-fees-used (c57d4643), b18-sigma-elapsed (8f9dd7c6), b22-pub-scan (fe5f639d), b01-public-replica (78e12a6a), b11-yq-calib (3d9c2cfe), b11-pub-chenghua (6f272ed6), b11-yq-replicate (6c45fe46, blocked), b04-vanilla-a (3e2a2fbc), b04-starter-a (cd3043c2), b15-board-map (654b62b7), b02-github (a9750575), b03-fees (1868f476), b01-static-grid (34c8bba1), b21-ablate (cc07912e), b16-gate-grid (7a0c896b), b16-kalman-gate (aaa01dbc), b17-tune-tox (cdd11d6d), b12-tune-asym (365158cc), b16-highfee (9141ad30), b31-combo-calib-a (50c817e7, blocked); plus the orchestrator's episode notes in `goal.json` for results read in earlier episodes but not handed here (r2 items, th-a, r3-d2 tune-base/tune-est/cma-residual, r1/r1x items).

Public material read and cited:

- Challenge: https://www.paradigm.xyz/puzzles/amm and https://www.paradigm.xyz/puzzles/amm/about (parameters, scoring); leaderboard API https://www.paradigm.xyz/puzzles/api/v1/leaderboard?limit=1000 (743 entries on 2026-11-07); per-submission detail endpoints for the three fixed-fee anchors (ids bee5b6be…, 9cbc7e2c…, 601d8da2…).
- Simulator: https://github.com/benedictbrady/amm-challenge at 6b6921f8d463314aa7c96234e1be25a25245f704 (`amm_competition/competition/config.py`, `match.py`, `cli.py`; `amm_sim_rs/src/simulation/engine.rs`, `market/router.rs`, `market/arbitrageur.rs`, `amm/cfmm.rs`, `evm/strategy.rs`; `contracts/src/VanillaStrategy.sol`, `StarterStrategy.sol`). Upstream `main` equals the pin.
- Public strategies measured: jiayaoqijia/amm-challenge-yq 3e9dc7d5 (README claims 523.21 on the board); ChengHua926/amm-challenge d34a5199; houseofjiao/amm-challenge 4f41eb91; shl0k28/amm-challenge 9c4be0b6; dipankar/amm-challenge c588ae6c (ANALYSIS.md; README claims 526.54 locally); eliizabethzhang/market-making-challenge 7156ff03; 0xniki/amm-challenge 56ca9d16; The-CTra1n/amm-challenge cd1bf7bc; atvinicius 78752c17; solosage1 99dc1cfd; alexanderzliu e15b10d2; VictorQian03 d0398512; 0xpranav62 4e24ad7e; lumen-dev-a11y 4eae7bd9; kmadorin ec151d5a; giorgoschionas 61ba5df1; maxnorm ee285c08 (YQ clone, not measured separately).
- Write-ups: Algebra Finance, "AMM fee challenge: notes from our run on Optimization Arena" (2026-03-27), https://www.linkedin.com/pulse/amm-fee-challenge-notes-from-our-run-optimization-arena-qe3ff and https://medium.com/@crypto_algebra/amm-fee-challenge-notes-from-our-run-on-optimization-arena-4e980dbbd699 (environment estimation, asymmetric fees, probabilistic within-step ordering, a historical seed leak and board recomputation; no code); HackMD note https://hackmd.io/6i1LNsRGRJ27YqTHjfO04A (reflected diffusion and competitive flow; its edge signs, sell routing and band edges are reversed relative to the pinned Rust, per theory/fees); Bruno I., LinkedIn (rank 44: ~95 % of edge from stale-price directional protection; a linear model beat regime switching; indexed only, per writeups/social). Public score claims were treated as data and re-measured; several (dipankar 526.54, shl0k28 525.08) did not hold up paired.
