# A new fee rule for the AMM fee challenge entry: result of the goal

## 0. Status in one paragraph

The goal did not reach its target. No fee rule tried moves the entry toward the top 10 (+5.0 over V2) or 1st (+8.7). The best file found, called STACK below, is V2 with three small caps on its fee mapping. It measured +0.043 over V2 on 4,000 fresh seeds (se 0.003) with 0 OutOfGas halts of its own. **That measurement is not an accepted confirmation under the objective's rule.** The objective says "any OOG call invalidates a result", and the comparator V2 itself halted OutOfGas 86 times on those 4,000 seeds (39 in shard A on 23 seeds, 47 in shard B on 20 seeds). The same is true of every paired measurement against exact V2 made in this goal: exact V2 at the challenge's 250,000-gas cap halts about twice per million afterSwap calls, so a 2,000-seed block (about 20.6 million calls) has never been OOG-free. This is a protocol blocker, described in section 3, not a defect in STACK's code. All figures in this report are therefore retained in full as diagnostics, with no seeds dropped, and this report makes no submission recommendation. The requester's goal-record notes of 02:28Z and 02:36Z relaxed the rule to "candidate OOG no higher than V2's on the same seeds", and the workers measured under that relaxed rule; the decision whether to act on a measurement that is valid only under that relaxation rests with the requester, not with this report.

The goal built no repository: `trunk` in the goal record is null. Every item returned its code and measurements as a result artifact, fetchable at `https://api.imd.fun/artifacts/<sha256>`; section 10 lists the ones this report rests on.

## 1. The best Strategy.sol: STACK

- **SHA-256 of the file:** `2eaafc7960e520b8a7fd322ec8afaff8fa677c730228a961efb509cc30b25719` (15,465 bytes).
- **Base:** G, a behaviour-preserving gas trim of V2 (sha `610c1905e7dd5559b84e40a3b2d6f8e0b53a7b0ac7574ae33b6c1770a28367cb`, the `code` of artifact `206a4888de6fa1bda53cd2c9bad1632ccdbb63d32e7f09b6a332746b7a3ac3c3`). G differs from V2 only in gas: it drops the zero writes in afterInitialize, packs the prior spot above the timestamp in slot 2, uses a floor Newton square root, and removes an unused pHat write. It matches V2 bit-exactly on every seed where V2 does not halt, and on 10000..10511 measures +0.0015 se 0.0014 against V2 (the difference is V2's own halts).
- **Comparator for every figure below:** exact V2, sha `28417e116f57f1029fdd1803832e852574902c1ae7253c05657f317db76da4ab`, built from the `code` of artifact `1f4f14f040b309e004904672ec6e2bb051f97b8d1195602d36b35a54c05d6c0f` with the two substitutions named in the objective.
- **Where the code comes from:** the `code` field of result artifacts `c33720874aa1285e9dc766540b8a90410118a8e8b840d949ea0dcc211bdb27c1` (e09-stack-confirm-a/a1) and `1f0e583c525721db0e8ebaf4f001668a3f7773bf506d1c98b7ac887be116a001` (e09-stack-confirm-b/b1). Both were re-fetched for this revision; both digests match their URLs, both `code` fields are byte-identical, and both hash to the SHA-256 above. All six confirm copies and e09-stack-tune/t1 carried the same bytes.

The full file:

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
        slots[13] = 902500000000; slots[14] = slots[5]; 
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

        {
            uint256 ret = fastHat > 0 ? wdiv(absDiff(pImplied, fastHat), fastHat) : 0;
            uint256 alpha;
            if (firstInStep) {
                uint256 processSigma = sigmaForFast;
                uint256 obsVar = uncertainty + wmul(processSigma, processSigma);
                uint256 probArb;
                uint256 z2 = wdiv(wmul(ret, ret), obsVar);
                uint256 density = _powWad(wdiv(WAD, WAD + z2 / 16), 8);
                uint256 sigmaObs = _isqrt(obsVar * WAD);
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

    function getName() external pure override returns (string memory) { return "no_cubic"; }
}
```

To reproduce the SHA-256 above from this listing, save it exactly as shown with a single trailing newline after the closing brace (15,465 bytes); the fenced block drops that final newline.

The three lines that make STACK differ from G are the `tradeBoost` cap (the line `if (!firstInStep && tradeBoost > 16 * BPS) ...`), the `if (firstInStep)` block that caps the lower of the two fees at 30 bps on a step's first print, and the two lines after it that cap the lower side at 36 bps on every call. Everything else is V2's estimators and V2's mapping, as trimmed in G.

## 2. Paired measurement of STACK against V2 on fresh seeds (diagnostic, not an accepted confirmation)

Method, every run: simulator commit `6b6921f8d463314aa7c96234e1be25a25245f704`, 10,000 steps, 250,000-gas callback cap, each strategy alone against the 30 bps Vanilla pool with `run_batch(X, VanillaStrategy, configs, 8)`, configs as `MatchRunner._build_configs` (size, rate, sigma from `default_rng(seed)`; price seed = seed, retail seed = seed + 1), paired per seed as candidate edge minus V2 edge, se = sample sd / sqrt(n). The harness is the strengthened one from artifact `206a4888...` (per-seed counters equal to global counters, retail + arb reconciled to total within 1.3e-11, all self-tests passing). Seeds 4380000..4381999 and 4390000..4391999 were allocated in episode 9, used once, never tuned on.

### 2.1 Shards

| | Shard A (e09-stack-confirm-a/a1) | Shard B (e09-stack-confirm-b/b1) |
|---|---|---|
| Result artifact | `c33720874aa1285e9dc766540b8a90410118a8e8b840d949ea0dcc211bdb27c1` | `1f0e583c525721db0e8ebaf4f001668a3f7773bf506d1c98b7ac887be116a001` |
| Seeds (half-open) | 4380000..4382000 | 4390000..4392000 |
| n | 2000 | 2000 |
| mean_diff (STACK minus V2) | +0.043224891299790416 | +0.04314031929182184 |
| se | 0.003943530703625499 | 0.0046822435465596 |
| sd | 0.17636005449328385 | 0.20939629714633934 |
| Worst 5 seeds (diff) | 4380438 (-0.9886), 4380970 (-0.9526), 4381653 (-0.8596), 4380519 (-0.5986), 4381375 (-0.5609) | 4390943 (-2.0785), 4391993 (-1.3430), 4390052 (-0.9530), 4391664 (-0.9113), 4390231 (-0.7130) |
| Retail edge delta | +0.04446 se 0.00399 | +0.04212 se 0.00424 |
| Arb edge delta | -0.00124 se 0.00146 | +0.00102 se 0.00265 |
| STACK afterSwap max_ok gas | 213,581 | 214,017 |
| STACK afterInitialize gas | 220,962 | 220,962 |
| STACK afterSwap calls / OOG | 20,695,584 / **0** | 20,629,954 / **0** |
| STACK other errors | 0 | 0 |
| V2 afterSwap max_ok gas | 244,105 | 244,370 |
| V2 afterInitialize gas | 236,377 | 236,377 |
| V2 afterSwap calls / OOG | 20,681,259 / **39** on 23 seeds | 20,615,934 / **47** on 20 seeds |
| V2 other errors | 0 | 0 |
| Vanilla failures (both runs) | 0 | 0 |
| Copies on the same shard | a1, a2, a3 bit-identical (mean, se, worst list) | b1, b2, b3 bit-identical |

V2's halted seeds, with halt counts, are listed in each artifact under `runs[0].v2_gas.oog_seeds`. Shard A: 4380041 (2), 4380082, 4380230, 4380275 (2), 4380281 (2), 4380538 (2), 4380553 (2), 4380644 (2), 4380710, 4380879 (2), 4380925 (2), 4381054 (2), 4381084, 4381179 (2), 4381392, 4381412 (2), 4381511, 4381522 (2), 4381544, 4381577 (2), 4381581, 4381673 (2), 4381977 (3). Shard B: 4390064, 4390453, 4390503 (2), 4390519 (2), 4390550 (2), 4390559, 4390579 (3), 4390699 (2), 4390712 (6), 4390722 (2), 4390783, 4390801, 4391252 (2), 4391344 (8), 4391428 (4), 4391481 (2), 4391518, 4391595 (2), 4391902 (2), 4391974 (2). No seed was dropped from any figure in this report; the per-seed differences on these 43 seeds are included in the means above. The simulator swallows an afterSwap error and keeps the previous fees, so a V2 halt leaves V2 quoting a stale fee for one trade.

Shard A's worker hit a 10-minute per-command limit and ran the unmodified harness on five consecutive 400-seed sub-ranges, then pooled with the harness's own functions; per-seed results do not depend on chunking. Chunk means were +0.0392, +0.0465, +0.0378, +0.0561, +0.0365.

### 2.2 Pooled over the two shards (4,000 disjoint seeds)

Pooled as planned in episode 9, with pooled variance rather than averaged standard errors: mean = (sum of all 4,000 differences) / 4000; se = sqrt(((1999 sd_A^2 + 1999 sd_B^2) / 3998) / 4000). Recomputed for this revision from the two artifacts.

| Pooled STACK vs V2 | |
|---|---|
| n | 4000 |
| mean_diff | +0.04318260529580613 |
| se | 0.0030608348142188288 (mean / se = 14.1) |
| worst seed | 4390943, -2.0785489651929083 |
| STACK OOG | 0 of 41,325,538 afterSwap calls |
| V2 OOG | 86 of 41,297,193 afterSwap calls, on 43 seeds |

**Validity.** Under the objective's rule ("any OOG call invalidates a result") this pooled comparison is invalid, because the V2 run contains 86 OOG calls; so is each shard on its own. It is therefore reported as a diagnostic, and this report accepts no confirmation and recommends no submission. Under the requester's amended rule in the goal record (02:28Z and 02:36Z notes: valid when the candidate's OOG count is no higher than V2's on the same seeds), the workers' harness marked both shards valid, and the requester's 05:42Z bar (pooled gain at least +0.04, more than 2 se, candidate OOG 0 on all 4,000 seeds) would be met on these figures. Which rule governs a submission is the requester's decision; this report only records that the two rules give different answers and why.

### 2.3 Replication of the same hash on five more fresh blocks (diagnostics, same caveat)

Every episode-9 LOO and tune item also ran STACK against V2 on its own fresh block. Each has candidate OOG 0 and V2 OOG above 0, so each is a diagnostic under the objective's rule.

| Block | Item | n | STACK minus V2 | se |
|---|---|---|---|---|
| 4400000..4400999 | e09-stack-loo/nof | 1000 | +0.04276 | 0.00558 |
| 4410000.. (partial) | e09-stack-loo/nos | 700 | +0.04918 | 0.00969 |
| 4430000..4430999 | e09-stack-tune/t1 | 1000 | +0.03986 | 0.00575 |
| 4440000..4440999 | e09-stack-tune/t2 | 1000 | +0.04111 | 0.00761 |
| 4450000..4450999 | e09-stack-tune/t3 | 1000 | +0.05225 | 0.00754 |

Seven fresh blocks, 7,700 seeds, every block positive and within about one se of +0.043. The gain is stable across blocks; it is also tiny: under 1% of the +5.0 gap to 10th place.

## 3. The protocol blocker: exact V2 cannot be an OOG-free comparator at 250,000 gas

Every paired measurement in this goal compared a candidate with exact V2, as the objective requires. Exact V2's afterSwap peaks at 243,554 to 244,370 gas, within 6,500 of the cap, and halts OutOfGas on rare states. The observed rate is stable across machines and seed ranges:

| Seeds | afterSwap calls (approx.) | V2 OOG | Source |
|---|---|---|---|
| 10000..10063 | 650k | 4 | e01 pilots (phase, routing, corridor), e01-metering |
| 10000..10127 | 1.3M | 4 | e01-metering/v2-audit (identical in two runs) |
| 10000..10255 | 2.6M | 7 | e04-harness-repair/control, e08-quote-audit |
| 10000..10511 | 5.3M | 13 | e02-gas-room/slim |
| 10000..10999 | 10.3M | 19 on 12 seeds | e02-decomp-local |
| 0..999 | 10.3M | 18 | requester's calibration, reproduced by e06-g-base/verify |
| 4380000..4381999 | 20.68M | 39 on 23 seeds | shard A |
| 4390000..4391999 | 20.62M | 47 on 20 seeds | shard B |
| other 2,000-seed holdouts | 20.6M each | 20 to 54 | e03, e05, e06, e07 items (see section 6) |

About two halts per million calls, deterministic per seed (two independent runs of V2 on the same seeds give the same halts), so a 2,000-seed block expects roughly 40 halts and a 0-OOG block of that size is not going to occur. Consequences:

1. No result of this goal is valid under the objective's literal rule. Every candidate built on G had 0 OOG of its own, and every comparator run had V2 OOG above 0. Candidates built directly on V2 (phase, threshold, position p2, pos-scale, the early pilots) inherited V2's halts themselves as well.
2. The rule, applied to the comparator, is the blocker, not any candidate's code. STACK peaks at 214,017 gas in afterSwap and 220,962 in afterInitialize, with about 36,000 of headroom and 0 halts in 41.3 million calls plus the 7,700 replication seeds.
3. The goal record shows the requester relaxed the rule for exactly this reason at 02:28Z, after the first four pilots stopped at the strict gate without measuring anything. The workers measured under the relaxed rule. The objective text itself was not amended, and this deliverable is judged against the objective, so this report classes the measurements as diagnostics and leaves the policy question to the requester.
4. A strictly valid confirmation is possible and was not run: compare STACK against G instead of V2. G has 0 OOG (peak 211,186 in afterSwap on 10000..10511, 0 halts on every block where it was run), is bit-identical to V2 on every seed where V2 does not halt, and differs from V2 by +0.0015 se 0.0014 overall (n 512) because of V2's halted seeds only. STACK vs G on fresh seeds would have 0 OOG in both runs. It was not measured; the expected value is about +0.042, but that is an inference, not a result. Section 9 puts this first.

## 4. The fee rule STACK uses and why it gains

STACK keeps V2's estimators (pHat and fastHat price filters, sigmaHat, lambdaHat, sizeHat, actEma, toxEma, dirState) and V2's mapping (fBase plus toxicity and activity terms into fMid, directional skew, stale-price shift, aligned-trade boost, compressed tails), and adds three caps that only lower fees:

1. **Later-print boost cap (K = 16 bps).** V2 adds `TRADE_TOX_BOOST * tradeRatio` (3500 bps times the trade's share of reserves) to the fee on the side a large aligned trade just hit. On a step's first print that trade may be an arb and the boost protects the next print. On later prints the trade cannot be the step's arb (the simulator runs one arb at most per step, first), so the boost mostly taxes retail; STACK caps it at 16 bps on later prints and leaves first prints alone. Measured alone (e08-boost-cap/later, n 512 training seeds 22000..22511): +0.02484 se 0.00545, retail +0.0265, arb -0.0017.
2. **First-print lower-side cap (30 bps).** On a step's first print, the lower of bid and ask is capped at 30 bps (ties untouched). The lower side is the attracting side, the one the stale-price shift has already pulled down because the pool believes the price moved the other way; the arb, if it comes, hits the higher side. Capping the attracting side at the Vanilla pool's 30 bps keeps the router share of same-step retail from collapsing when V2's flow terms have pushed both sides high. Measured alone (e07-hyb-afterfirst f1/f2/f3 with caps 32/29/30, n 2000 each on fresh blocks): +0.01182 se 0.00212, +0.01275 se 0.00376, +0.01487 se 0.00320; f1's split was retail +0.0176, arb -0.0058. Cuts of 2 or 4 bps instead of caps lost.
3. **Every-call lower-side cap (36 bps).** On every print, the lower side is capped at 36 bps. Measured alone (e07-hyb-floor s1/s2/s3 with caps 36/35/36, n 2000 each): +0.00805 se 0.00254, +0.0141 se 0.0024, +0.01314 se 0.00224.

The quote audit (e08-quote-audit, 256 training seeds, trace parity with V2 checked) explains why the gains are small: of 1.73 million first-print lower-side quotes, only 17 thousand exceeded 30 bps and 3.4 thousand exceeded 36 bps. The caps act on about 1% of prints. They cannot move the mean fee by the 1.3 to 2.4 bps that separate V2 from the leaders, and they do not.

**Attribution by leave-one-out** (same seeds, piece worth = STACK minus the stack without it):

| Piece removed | Block | n | Worth of the piece | LOO file sha |
|---|---|---|---|---|
| First-print 30 bps cap | 4400000..4400999 | 1000 | +0.00923 se 0.00389 | `94e4747a7666d0b92d3db7cb6d81d9cc0478c6e0d55e80472a8e6b5aa2d7f23a` |
| Every-call 36 bps cap | 4410000.. (partial) | 500 | +0.00216 se 0.00422 (not distinguishable from zero) | `54ae8c358696cb964acbb6525b901b7f1ede2908d460e298ce8183fcbd307a79` |
| Later boost cap | 4420000.. | 0 | not run (host was Darwin arm64); inferred by difference about +0.03, consistent with +0.02484 se 0.00545 measured alone | `1a2f14a74005f5beea29a59456f5c67525d862eb0b2b25d032b449335ee9e679` |

The pieces are not proven additive. The 30 and 36 bps caps overlap on first prints, and the 36 bps cap's own contribution inside the stack is within its noise.

**Retail and arb edge, and the board rungs.** The requester's board decomposition (e02-decomp-board, artifact `0213d3489bd92a4b4ae8ffb8e97fd7e444ce296d89c647243298a182823feb97`) gives the targets by tercile of V2's retail volume, and the local decomposition (e02-decomp-local, artifact `27b38b4fd30bae05991e8f1925f83d2fe75ec097a7a93d3ac0af270cce06d5ad`, 1,000 seeds 10000..10999) gives V2's own retail/arb split. STACK's gain by tercile, from the two shards:

| Tercile of V2 retail volume | V2 local edge (retail / arb / total) | V2 mean fee, bps | Gap to 10th on the board | Gap to 1st on the board | STACK gain, shard A | STACK gain, shard B |
|---|---|---|---|---|---|---|
| low | 457.36 / -24.01 / 433.36 | 34.93 | +4.164 | +7.293 | +0.0313 se 0.0048 | +0.0340 se 0.0057 |
| mid | 552.46 / -27.65 / 524.81 | 36.93 | +5.015 | +8.718 | +0.0419 se 0.0066 | +0.0471 se 0.0073 |
| high | 656.19 / -32.61 / 623.58 | 38.88 | +5.750 | +10.142 | +0.0565 se 0.0085 | +0.0483 se 0.0106 |

STACK's gain is retail (+0.044 and +0.042 on the two shards) with arb flat (-0.001 and +0.001). It grows with retail volume, as the board rungs do, but at about 0.5% of their size. The board rungs, from the requester's decomposition: the step from V2's class to 10th is a retail rung (about +1,430 retail Y per run at the same mean fee, arb about +440), and the step from 10th to 1st is an arb rung (arb about -824 Y at a mean fee only 0.12 bps higher). Every rule tried in this goal that moved retail by more than a few hundredths did so by cutting fees broadly and lost far more on both retail and arb (section 6). Nothing tried touched the arb rung without losing. The board API publishes total edge and volumes, not a retail/arb split, so the board rungs are the requester's proxy decomposition and the local split is the only measured one.

**Why the +5 to +8.7 was not found.** The leaders' fee is 1.3 bps below V2's on average and 2.2 to 2.4 bps below in busy runs, with a per-run fee sd of 1.6 vs V2's 1.97 and a fee slope of about 1.1 bps per 10k retail Y vs V2's 1.83. Every attempt to reproduce those symptoms by damping or capping V2's flow terms (flowcap c1/c2/c3), flooring or fixing the attracting side (floor and small-floor families), or quoting lower on later prints by a Poisson or threshold rule (position, pos-scale both-side, threshold) lost between 0.2 and 40 points, and every rule written from scratch lost 14 to 176 points. Flat fees at 30 to 40 bps lose 166 to 181, so V2's dynamics are worth about 170 of its 520 local edge. A lower mean fee is a symptom of the leaders' rule, not its mechanism, and the mechanism was not identified.

## 5. Harness, base and controls the figures rest on

- **e01-metering/v2-audit** (artifact `02c134d9ed51858f06d02b6dec25e6922016490f11e3a8174af512a6a77b6569`): V2 reproduces bit-exactly over two independent runs on 128 seeds; per-call counters for oog, revert, other_halt, tx_error, bad_return and max_ok gas; the engine swallows afterSwap errors and keeps the old fees. Its harness exited on any OOG and allocated configs for every seed below the range; both were repaired later.
- **e04-harness-repair/control** (artifact `db62deadd0a3ec885ad69bd3917fee793a924ead522776d73cc09110923e1e86`): corrected harness (requested seeds only, never exits on OOG, retail/arb attribution), forced-error diagnostics detect injected OOG, revert and bad returns; V2 vs V2 on 10000..10255 gives all 256 differences exactly zero.
- **e02-gas-room/slim** (artifact `c5114d6f2f9230073d40f09e3a4bd09dad08ee3833d8dc9faa8779f6d7b0b132`): dropping afterInitialize's zero writes is an exact zero diff; packing the prior spot above the timestamp removes V2's halts and changes only the 9 formerly-halting seeds of 512 (+0.0015 se 0.0014, max abs 0.73); the floor sqrt preserves edges exactly.
- **e06-g-base/verify** (artifact `206a4888de6fa1bda53cd2c9bad1632ccdbb63d32e7f09b6a332746b7a3ac3c3`): G's sha verified; the requester's calibration (exact V2 on seeds 0..999, mean 526.9433475904315, 18 OOG) reproduced bit-identically; G vs V2 at a diagnostic 1,000,000-gas cap equal on 128 seeds; 20,727 sqrt cases and packing bounds pass; harness gates counter agreement and reconciliation. Its bundle (setup.sh with the Rust fallback, instrumentation.patch, harness.py, tests.py, V2.sol) was used by every later item.
- **e08-quote-audit**: G vs V2 on 10000..10255 +0.0029 se 0.0029 (G OOG 0, V2 OOG 7), the control calibration 523.2153137188661 reproduced exactly, fee-use tables cited in section 4.
- **e05-flat-control**: flat bid = ask = F for F in 30..40 bps vs V2 on 10000..10255: -181.1 to -166.4; 75 bps still about -145.5. Agrees with the routing item's flat-33-bps variant (-175.8 se 2.7), so the two harnesses agree on the value of V2's dynamics.

Local absolute V2 means (524.1 on shard A, 522.5 on shard B, 527.2 on 10000..10999, 526.9 on 0..999) differ from the board's 519.68 because the seeds differ; only paired differences are used anywhere in this report.

## 6. Ranked table of every fee rule tried

Mean difference is candidate minus exact V2, paired on the same seeds. n is 2000 on a fresh block from 4000000 up unless marked "train" (seeds in 10000..99999, used for screening) or "partial". "OOG c/V" is candidate halts / V2 halts on those seeds. Under the objective's literal rule every row with V2 halts above 0 is a diagnostic (section 3); under the requester's amended rule, rows with c <= V are valid. Items built directly on V2 inherit V2's halts (c = V). Rows are ranked by measured mean difference; blocked items that never measured a candidate follow the table.

| Rank | Rule | Batch / item | Seeds | n | Mean diff | se | OOG c/V | Code sha (prefix) |
|---|---|---|---|---|---|---|---|---|
| 1 | STACK: later boost cap 16 + first-print lower cap 30 + every-call lower cap 36, on G | e09-stack-confirm a1 + b1 | 4380000.., 4390000.. | 4000 | +0.04318 | 0.00306 | 0/86 | 2eaafc79 |
| 2 | Later-print boost cap K16 alone, on G | e08-boost-cap/later | 22000..22511 | 512 train | +0.02484 | 0.00545 | 0/n.r. | fdcc291e |
| 3 | First-print lower-side cap 30, on G | e07-hyb-afterfirst/f3 | 4310000.. | 2000 | +0.01487 | 0.00320 | 0/33 | e98d8a0f |
| 4 | Every-call lower-side cap 35, on G (shortened screen) | e07-hyb-floor/s2 | 4360000.. | 2000 | +0.0141 | 0.0024 | 0/20 | n.r. |
| 5 | First-print boost cap K16 alone, on G | e08-boost-cap/first | 12000..12511 | 512 train | +0.01346 | 0.00570 | 0/n.r. | ab4a2640 |
| 6 | Every-call lower-side cap 36, on G | e07-hyb-floor/s3 | 4370000.. | 2000 | +0.01314 | 0.00224 | 0/31 | 306923bb |
| 7 | First-print lower-side cap 29, on G | e07-hyb-afterfirst/f2 | 4300000.. | 2000 | +0.01275 | 0.00376 | 0/32 | n.r. |
| 8 | First-print lower-side cap 32, on G | e07-hyb-afterfirst/f1 | 4290000.. | 2000 | +0.01182 | 0.00212 | 0/23 | n.r. |
| 9 | Pos-scale: blend V2's fee toward a constant weighted by P(next is retail), attracting side only, on V2 | e03-pos-scale/s1 | 4160000.. | 2000 | +0.00913 | 0.00197 | 0/50 | n.r. |
| 10 | Every-call lower-side cap 36, on G | e07-hyb-floor/s1 | 4350000.. | 2000 | +0.00805 | 0.00254 | 0/31 | n.r. |
| 11 | G alone (gas trim, no fee change) | e06-g-base/verify; e08-quote-audit | 10000..10511; 10000..10255 | 512; 256 train | +0.0015; +0.0029 | 0.0014; 0.0029 | 0/13; 0/7 | 610c1905 |
| 12 | STACK with R2 = 34 instead of 36 | e09-stack-tune/t2 | 4440000.. | 1000 | +0.04089 (vs V2); -0.0002 vs STACK | 0.00775 | 0/n.r. | 8fac06b4 |
| 13 | STACK with K = 12 | e09-stack-tune/t3 | 60000..60255 | 256 train | +0.0011 vs STACK | 0.0039 | 0/n.r. | n.r. |
| 14 | STACK with R1 in 26/28/32/34 | e09-stack-tune/t1 | 40000..40255 | 256 train | -0.011 / -0.002 / 0.000 / +0.006 vs STACK | 0.008 to 0.010 | 0/n.r. | n.r. |
| 15 | Next-mix (Poisson mix of the next retail quote), on G (requester's goal 5ec6cdb2) | requester note 03:00Z | 3300000..3301999 | 2000 | -0.0474 | 0.0246 | 0/n.r. | c0e7362b (GN) |
| 16 | Zero directional skew, on GN | requester note 03:00Z | same | 2000 | -0.0678 (additional) | 0.0084 | n.r. | n.r. |
| 17 | Gated small floor of the lower G fee, F = 1 bp, later prints | e08-small-floor/later | 22000..22511 | 512 train | -0.1985 | 0.0062 | 0/n.r. | e7f7111d |
| 18 | Small floor F = 1 bp, all prints (loss about -0.5 per bp of floor) | e08-small-floor/all | 32000..32511 | 512 train | -0.480 | 0.009 | 0/n.r. | n.r. |
| 19 | Continuation table, horizon 8, offset hybrid, on G | e06-continuation/h8 | 4280000.. | 2000 | -0.5057 | 0.0093 | 0/34 | n.r. |
| 20 | Flow-term scale 0.75 on the non-exposed side, on G | e07-hyb-flowcap/c1 | 4320000.. | 2000 | -0.6552 | 0.0130 | 0/44 | n.r. |
| 21 | Flow-term scale 0.70, on G | e07-hyb-flowcap/c3 | 4340000.. | 2000 | -0.9264 | 0.0131 | 0/39 | n.r. |
| 22 | Flow-term scale 0.60, on G | e07-hyb-flowcap/c2 | 4330000.. | 2000 | -1.477 | 0.015 | 0/n.r. | n.r. |
| 23 | Position blend p2: fR from router share, fA = max(F0, c sigmaHat sqrt(steps)), on V2 | e05-position-rerun/p2 | 4210000.. | 2000 | -2.0771 | 0.0352 | 0/31 | n.r. |
| 24 | Threshold t1: first print R + k sizeHat, later V2 | e05-threshold-rerun/t1 | 4230000.. | 450 partial | -4.3858 | 0.0854 | 20/20 | n.r. |
| 25 | Phase: unknown-next-event mixture, on V2 | e03-pilot-rerun/phase | 4080000.. | 2000 | -5.8763 | 0.0395 | 37/37 | 55da2430 |
| 26 | Protect hinge (stale addition slope change beyond a gap), first / later / all | e08-protect-hinge | 12000.., 22000.., 30000.. | 512 / 512 / 256 train | -6.20 / -6.39 / -6.93 | 0.13 / 0.23 / n.r. | 0/n.r. | n.r. |
| 27 | Observed-print threshold rule (reconstruction), best of six screens | e04-position-recovery/a1 | 10000..10255 | 256 train | -6.645 | 0.125 | n.r. | 68cc95b3 |
| 28 | Threshold t2: constant R first print, V2 fMid later | e05-threshold-rerun/t2 | 4240000.. | 2000 | -8.4260 | 0.0686 | 41/41 | n.r. |
| 29 | Interaction: six sparse hinge rules replacing the mapping | e01-fee-rule-pilot/interaction | 11000..11255 | 256 train | -13.67 | 0.40 | 0/n.r. | n.r. |
| 30 | Pos-scale both sides | e05-pos-scale-copy/s2 | 4250000.. | 2000 | -18.2016 | 0.1782 | 27/27 | n.r. |
| 31 | Continuation table, horizon 2 | e06-continuation/h2 | 4260000.. | 2000 | -21.66 | 0.145 | n.r. | n.r. |
| 32 | Continuation table, horizon 4 (H1 ablation identical) | e06-continuation/h4 | 4270000.. | 2000 | -23.6803 | 0.0986 | 0/45 | n.r. |
| 33 | Position blend a3 (fR 30..34, rescaled V2 fA) | e03-design-a-position/a3 | 4130000.. | 256 partial | -33.43 | 0.93 | n.r. | n.r. |
| 34 | Position blend p1 (constant fR 26..36) | e05-position-rerun/p1 | 4200000.. | 256 partial | -39.82 | 0.80 | n.r. | n.r. |
| 35 | Expected-edge per-side optimiser, linear router share | e02-design-b-edge/b2 | 4070000..4070399 | 400 partial | -43.975 | 0.481 | 0/5 | 42938ca2 |
| 36 | Closed-form expected-edge hinge | e03-design-b-edge/b2 | 4200000.. (seed-protocol deviation) | 2000 | -60.8203 | 0.2381 | 0/26 | n.r. |
| 37 | Routing table R0 (gap by sigma, 0 bps on the attracting side at negative gap) | e03-pilot-rerun/routing | 4090000.. | 2000 | -61.87 | 0.557 | 0/54 | 9e65b5a2 |
| 38 | Exact-router utility lookup table | e04-edge-table/table | 4190000.. | 2000 | -83.43 | 0.69 | 37/37 | 6ca9da36 |
| 39 | Flat bid = ask = F, F in 30..40 bps | e05-flat-control/flat; routing R11 | 10000..10255; 60000..60255 | 256 train | -166.4 to -181.1; -175.8 | n.r.; 2.7 | 0/7 | n.r. |

"n.r." means not recorded in the goal's notes; the figure is in the item's artifact. The e03-design-b-edge/b2 row ran on 4200000..4201999, a block the orchestrator had allocated to e05-position-rerun/p1, after aborting on its own block; it is a seed-protocol deviation and is recorded as such, with no promotion at issue since it lost.

**Never measured (blocked before any candidate ran; not tried ideas):** corridor (multiplicative quote widths; its first run stopped at the strict OOG gate, its rerun ran for six episodes and was cancelled in episode 9), e02 position a1/a2 (strict gate), e03-design-b-edge/b1, e05-position-rerun/p3, e04-position-recovery/a2 and e08-small-floor/first (host without /proc, Rust installer failed), e08-boost-cap/all and e09-stack-loo/nok (macOS arm64 hosts). The phase, routing and corridor pilots' first runs and e02-design-b-edge/b1 stopped at the strict gate too; phase and routing were rerun and measured (rows 25 and 37).

## 7. Seed ledger

Confirmation blocks are never reused for a new code hash. Blocks 4000000..4459999 are allocated or retired. Used for STACK: 4380000..4381999 and 4390000..4391999 (shards A and B), 4400000..4400999, 4410000..4410699 (partial), 4430000..4430999, 4440000..4440999, 4450000..4450999. The next free block for any file with a new hash is 4460000. Training was confined to 10000..99999 throughout; the quote audit and flat control used 10000..10255; the requester's calibration used 0..999 (neither tuning nor holdout). One worker (e03-design-b-edge/b2) chose its own replacement block; no other item deviated.

## 8. Limitations

- **No accepted confirmation.** Under the objective's rule, the comparator's 86 OOG halts make the 4,000-seed comparison invalid, and the same applies to every other paired result in this goal (section 3). The figures are complete diagnostics; nothing was dropped or re-selected.
- **The target was not reached.** +0.043 is under 1% of the gap to 10th. No rule tried identifies the leaders' mechanism.
- **Attribution is incomplete.** The boost cap's worth inside the stack is inferred (nok never ran); the 36 bps cap's worth is within noise on 500 seeds; the pieces overlap.
- **Board transfer is the requester's observation**, not measured here: paired local gains transferred to the board within 1 se twice before. The +0.04 bar is the requester's estimate of what passes 28th place. No board rank is claimed.
- **Board decomposition is a proxy.** The board API publishes total edge and volumes only; the retail/arb rungs are the requester's decomposition with fee times volume as a proxy, and the local split in section 4 is the only measured one.
- **Shard A was chunked** into five 400-seed commands because of a per-command time limit; per-seed results are independent of chunking and all three copies agree bit-exactly.
- **Hosts failed often**: eight items returned blocked at setup (no /proc for the Rust installer, or a macOS host). They are listed as never measured, not as losses.

## 9. What the next run should try

1. **A strictly valid confirmation of STACK with a zero-OOG comparator.** Run STACK against G (sha `610c1905...`) on 4460000..4463999 as two 2,000-seed shards on two machines, with G's halts and STACK's halts both required to be 0, and report the same fields as section 2. G equals V2 on every non-halting seed, so this is the comparison the objective's rule allows. Also report STACK against exact V2 on the same seeds as a diagnostic, so the two can be reconciled. Expect about +0.042 but measure it.
2. **Decide the OOG policy in the objective text, not in notes.** If the requester wants exact V2 as the comparator, the objective should say how the comparator's own halts are treated; if the requester wants the strict rule, the comparator must be G or another 0-OOG build. Until one of these is done, no confirmation against V2 can be accepted under the objective.
3. **Stop tuning the caps.** t1/t2/t3 found no constant better than 30/36/16 within noise, and the quote audit shows the caps act on about 1% of prints. More items here buy hundredths at most.
4. **Target the arb rung directly, with the local retail/arb split as the metric.** Everything that gained was retail. The 10th-to-1st rung is arb (about -824 Y arb loss at a mean fee only 0.12 bps higher). The local split shows V2 losing about 28 per run to arbs, 98% of it at gap 1, and 63% of arb loss on the 19% of steps where pHat is more than 30 bps off. Rules that widened protection by gap (protect hinges) lost 6 to 7 because the exposed side rose on steps with no arb. A next design should condition protection on something that distinguishes an impending arb from a stale estimate without raising the fee on quiet steps; the quote audit's trace tooling (e08-quote-audit) gives per-print exposure and realised edge to fit against, on training seeds only.
5. **Do not repeat the retired families**: written-from-scratch mappings (routing, edge tables, expected-edge optimisers, interaction hinges, continuation tables), flow damping, floors of the attracting side, Poisson or threshold position blends, both-side pos-scale, next-mix, zero skew, protect hinges and flat fees. Each has a measured loss in section 6.
6. **Use the b19 bundle** (artifact `206a4888...`) for setup, instrumentation and harness, and give every design three copies while hosts fail at setup as often as they did here; a host without /proc or a macOS host returns blocked, not a result.
7. **Whatever the requester submits, post the board score back as a note.** At +0.04 the transfer claim (local paired gain to board score within 1 se) would be tested at a scale an order of magnitude smaller than before.

## 10. Results this report rests on

All at `https://api.imd.fun/artifacts/<sha256>`. Re-fetched and digest-checked for this revision: the two confirmation shards (first two rows).

| Artifact sha256 | What it is |
|---|---|
| `c33720874aa1285e9dc766540b8a90410118a8e8b840d949ea0dcc211bdb27c1` | e09-stack-confirm-a/a1: STACK code and shard A |
| `1f0e583c525721db0e8ebaf4f001668a3f7773bf506d1c98b7ac887be116a001` | e09-stack-confirm-b/b1: STACK code and shard B, harness self-tests |
| `206a4888de6fa1bda53cd2c9bad1632ccdbb63d32e7f09b6a332746b7a3ac3c3` | e06-g-base/verify: G source, calibration, strengthened harness bundle |
| `f09f39f5092e5b1e56f156df10f397e5df0e194afa630ab24fc699adfd980d31` | requester's goal 5ec6cdb2 gn-a: GN source from which G was derived, next-mix and zero-skew measurements |
| `1f4f14f040b309e004904672ec6e2bb051f97b8d1195602d36b35a54c05d6c0f` | V2 source before the two substitutions named in the objective |
| `02c134d9ed51858f06d02b6dec25e6922016490f11e3a8174af512a6a77b6569` | e01-metering/v2-audit |
| `db62deadd0a3ec885ad69bd3917fee793a924ead522776d73cc09110923e1e86` | e04-harness-repair/control |
| `c5114d6f2f9230073d40f09e3a4bd09dad08ee3833d8dc9faa8779f6d7b0b132` | e02-gas-room/slim |
| `0213d3489bd92a4b4ae8ffb8e97fd7e444ce296d89c647243298a182823feb97` | e02-decomp-board/board: board per-run decomposition and tercile targets |
| `27b38b4fd30bae05991e8f1925f83d2fe75ec097a7a93d3ac0af270cce06d5ad` | e02-decomp-local/local: V2 retail/arb split by tercile |
| `9e7b66123809118f02298d3f6e0be318fbb32b2074c7fce724a8e41e0b6bdd35` | e07-hyb-afterfirst/f3 result (code e98d8a0f...) |
| `483c7c8541535ef703a0661f2d1cc8c235f21a0d149a60cf394f0d984d886d8f` | e07-hyb-floor/s3 result (code 306923bb...) |
| `22903683526e3817ce2cb099f097578ce78fa53121bac16c898e3bda0095560a` | e02-design-b-edge/b2 result |
| `372e7282ee336f557b6861ecc8ef6730b4e65b637c6f8018c1d3127c1ecabc9f` | e02-design-a-position/a1 (blocked at strict gate; source kept) |
| `bf4c55da9c1f3f7fdf3d3e28c8dc95b77acb63ac4cbc8e1e07bd2073e56aec9e` | e02-design-a-position/a2 (blocked) |
| `3114b7dc7d9fdf46e39f8ec85571819a5ac788e3871948a75f6c74d669a9a9fb` | e02-design-b-edge/b1 (blocked; prototype gas finding) |
| `f1e1fdd3c44b9ed1e4349a32828ef2ed1564cc8c9a0610f1017dca88a9a5f7a6` | e04-position-recovery/a2 (blocked at setup; reconstruction) |
| `f5de2d1e4002e37761d90e15463ba72b437ee3a948eb8d142f18f0f7740d92a1` | goal 052122ee write-up (prior estimation ceiling +1.19) |
| `ddbbaac58282566e0505d895c83daf348487cc322e8c482e61d4d87e6e4628de` | simulator rules JSON (step order, arb rule, router share, fee semantics) |

The remaining rows of section 6 come from the goal record's episode notes, which quote each item's returned figures; their artifacts are in the goal's batch records under the item names given.
