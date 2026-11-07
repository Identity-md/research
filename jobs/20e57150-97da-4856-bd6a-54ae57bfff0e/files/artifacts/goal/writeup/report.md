# Prediction Market challenge: from 3rd to 1st, the final strategy and its evidence

## 1. The strategy to submit

The best file is **T**, the `code` field of https://api.imd.fun/artifacts/79af781a0f1882f2a291e045f803714b52128f9938480d54fb43360417b381ac.

| | |
|---|---|
| code_sha256 (UTF-8 bytes of the file) | `9fba1eb5659d5b0ac9b7273a968a520ef9a95551c697be22020993005af70192` |
| size | 43,168 bytes, 896 lines |
| Paradigm standing (requester's note, 2026-11-07 02:05Z) | 1st at 110.87 (2nd 110.69, 3rd 109.59); the objective started from 3rd at 104.84 |
| paired gain over wave 3's combine-cash on seeds 900000..903999 | **+3.502 (standard error 0.336)**, n = 4000, 0 failures, run on this machine during the write-up (section 3.1) |
| paired gain over MA, its direct base | +1.227 (se 0.354) on T's own holdout 170000..170999, n = 1000; +0.66 on Paradigm's runs; a partial check here on 744 finalist seeds gave +0.185 (se 0.265), so this link is the least established (section 3.2) |
| check values (unmodified simulator b244530e, seeds 310000..310003, total_edge) | 17.899934, 24.258579, 2.433424, 259.215142 |
| runtime | about 1.35 s a simulation serial here, equal to its base MA (1.37 s); it passed Paradigm's sandbox, which stops a submission at about 270 s for 200 runs |

The file is submittable as is. Section 2 is the file in full; section 3 is its evidence on the finalist seeds; section 4 is the ranked promotion table; section 5 is what the next run should try.

**What T is.** T is goal 7be68b75's `x-plus-b`: the per-spread merge MA (`149883fe…`, itself a sibling goal's merge of four spread-specific blocks) with four changes that this goal found or measured, carried by hand and gated per competitor spread through one table on line 34:

```python
ON = dict(cancel=(2, 3, 4), cut=(1, 4), postjump=(1,), premium=(), deadband=(3,))
```

- `cancel` (spreads 2, 3, 4): this goal's retreat cancel (RC). When the rival's bid falls exactly one tick or its ask rises exactly one tick, cancel every own order on that side and place nothing there for one callback, clearing that side's probe and exposure bookkeeping. The one change that passed this goal's finalist gate (section 4).
- `cut` (spreads 1, 4): belief weight multiplied by 0.016 on the stale side after a one-tick rival retreat. The descendant of this goal's retreat-crossing family (runner-up in section 4).
- `postjump` (spread 1): the spread-1 jump-withhold wrapper plus its `qb_z = 4` bank condition.
- `premium` (off everywhere): the spread-4 ask risk premium change; measured negative and left off.
- `deadband` (spread 3): `keep_lo` replaced by 1 in `add_b` and `add_a`.

A run has one competitor spread, read from the rival's first quotes as `self.s` (ask minus bid equals 2s minus 1), so each entry acts on its spreads only and the entries compose.

**No code repository.** The goal ran research batches only; no code batch was spawned and `goal.json` names no trunk. Every candidate lives as the `code` field of a result artifact at `https://api.imd.fun/artifacts/<result SHA-256>`.

## 2. Full code of T

Save the block below as a `.py` file. Its UTF-8 SHA-256 must be `9fba1eb5659d5b0ac9b7273a968a520ef9a95551c697be22020993005af70192` (the file ends with a newline after the last line).

```python
"""Crossing-cover base with isolated, untuned per-spread overrides stacked: each acts only in runs of its own competitor spread."""
import math
from orderbook_pm_challenge.strategy import BaseStrategy
from orderbook_pm_challenge.types import CancelOrder, PlaceOrder, Side

P = dict(lam_r=0.25, m=5.0, sig_n=1.2, lam_j=0.0019, sig_j=0.35, sig=0.02,
         qmax=3000.0, rmin=2, kA=0.7, kL=0.15, pL=0.05,
         ammo=1.0, ydem=0.4, W=200.0, fy=0.6, ammo_q=60.0, ammo_pmax=0.05, ammo_maxpay=0.02,
         fb=0.9, fu=0.7, xu=0.1, sticky=1.0, min_ahead=2.0, keep_hi=1.5, keep_lo=0.7, Hu=300.0, bins=8.0, filt=1.0, uni=0.01, jumpinfo=1.0, dmin=0.0, kLb=0.08, kLf=0.08, pinf=1.0, pre=0.0, H1=100.0,
         ydf=0.6, Wf=2000.0, g_hi=0.15, g_lo=0.15, qf=400.0, pmaxf=0.05, pre_gap=1.0,
         ydf1=0.6, g1=5.0, f1=0.6, a1=100.0, nb1=0.0, gs=1.0, p1t=1.0, m1=1.0, zd=1.0, pfl=0.0005)
SQ2 = math.sqrt(2.0)
SQ2PI = math.sqrt(2.0 * math.pi)
def cdf(x): return 0.5 * (1.0 + math.erf(x / SQ2))
def pdf(x): return math.exp(-0.5 * x * x) / SQ2PI
def inv(p):
    p = min(max(p, 1e-9), 1 - 1e-9)
    t = math.sqrt(-2.0 * math.log(min(p, 1 - p)))
    x = t - (2.515517 + 0.802853 * t + 0.010328 * t * t) / (1 + 1.432788 * t + 0.189269 * t * t + 0.001308 * t ** 3)
    x = -x if p < 0.5 else x
    for _ in range(2):
        d = pdf(x)
        if d < 1e-12:
            break
        x -= (cdf(x) - p) / d
    return x
def lpm(k):
    return pdf(k) + k * cdf(k)
def fl(q):
    return math.floor(q * 100 + 1e-9) / 100

NODES = [(-2.2, .06), (-1.3, .17), (-0.6, .27), (0.6, .27), (1.3, .17), (2.2, .06)]
PROBE = 0.01
ON = dict(cancel=(2, 3, 4), cut=(1, 4), postjump=(1,), premium=(), deadband=(3,))

F_AH = 1
F_FL = 1
F_QB = 1

# s1-flow: conditional likelihood of partial fills and zeros. Fully exhausted quotes
# can be either retail or arbitrage; neither is treated as a zero or a
# complete retail order. Truncation normalization corrects the selection.
FLOW_CAPS = (0.03125, 0.0625, 0.125, 0.25, 0.5, 1., 2., 4., 8., 16., 32., 64., 128., 256.)
FLOW_GRID = []
FLOW_PRIORS=[]
for _rn,_rw in ((-math.sqrt(0.6),5/18),(0.,4/9),(math.sqrt(0.6),5/18)):
    _r=0.1265+0.0495*_rn
    for _mn,_mw in ((-0.906179845938664,0.118463442528095),(-0.538469310105683,0.239314335249683),(0.,0.284444444444444),(0.538469310105683,0.239314335249683),(0.906179845938664,0.118463442528095)):
        _m=4.488+1.848*_mn
        _parts=[]
        for _n in (1,2,3):
            _v=math.log(1+(math.exp(1.44)-1)/_n)
            _sg=math.sqrt(_v)
            _mu=math.log(_n*_m)-_v/2
            _w=_r**_n/math.factorial(_n)
            _parts.append((_mu,_sg,_w))
        _norm=[]
        for _c in FLOW_CAPS:
            _prob=sum(w*(cdf((math.log(_c)-mu)/sg)-cdf((math.log(0.03)-mu)/sg)) for mu,sg,w in _parts)
            _norm.append(math.log1p(_prob))
        _tails=[]
        for _c in FLOW_CAPS:
            _cdf=1+sum(w*cdf((math.log(_c)-mu)/sg) for mu,sg,w in _parts)
            _tails.append(math.log(max(1e-100,1-math.exp(-_r)*_cdf)))
        FLOW_GRID.append((_r,_m,_parts,_norm,_tails))
        FLOW_PRIORS.append(math.log(_rw*_mw))


class Strategy(BaseStrategy):
    def __init__(self):
        self.n = 0
        self.ahead = set()     # main orders placed strictly ahead of any competitor order at their tick
        self.res = {}          # order id -> uncovered quantity at placement
        self.bc = None         # belief: sub-tick grid centres (ticks)
        self.bw = None         # belief: weights
        self.st = 0.5          # last one-step sd in ticks
        self.pcb = self.pca = None
        self.pb = set()
        self.pa = set()
        self.tb = 0
        self.s = None          # competitor spread parameter
        self.flow_notional = 0.0
        self.flow_exposure = 0
        self.last_ask_tick = None
        self.last_quote_exposed = False
        self.last_flow_ca = None
        self.last_flow_cap = 0.0
        self.last_flow_correction = 1.0
        self.params = P.copy()
        self.s2_mb = set()
        self.s2_ma = set()
        self.s2_lb = self.s2_la = -99
        self.fl_obs = ()
        self.fl_scores = FLOW_PRIORS.copy()
        self.fl_bins = [0]*len(FLOW_CAPS)
        self.fl_rate = 0.568734
        self.fl_r = 0.1265
        self.fl_m = 4.488
        self.fl_buy_sum = self.fl_sell_sum = 0.0
        self.fl_buy_exp = self.fl_sell_exp = 0.0
        self.fl_exp = 0
        self.fl_dirty=False
        self.fl_ahead=set()
        self.fl_safe_n=0
        self.fl_sbins=[0]*len(FLOW_CAPS)

    def _oid(self, tag):
        self.n += 1
        return tag + str(self.n)

    def on_step(self, state):
        H = max(1, state.steps_remaining)
        cb = state.competitor_best_bid_ticks or 0
        ca = state.competitor_best_ask_ticks or 100
        if self.s is None:
            self.s = max(1, (ca - cb + 1) // 2)
            if self.s == 4:
                # Use the existing low-price risk penalty on bids too; inventory
                # cover orders already provide the separate stocking mechanism.
                self.params['kLb'] = self.params['kLf'] = self.params['kL']
                # Censored compound-Poisson flow likelihood, using only our fills.
                self.f4_exposure = [0, 0]
                self.f4_events = [0, 0]
                self.f4_weights = [[0.0] * 9, [0.0] * 9]
                self.f4_means = [2.64 + i * (6.336 - 2.64) / 8 for i in range(9)]
                # Positive aggregate flow is approximately lognormal; +0.065
                # accounts for the occasional second arrival in a timestep.
                self.f4_mu = [math.log(m) - 0.72 + 0.065 for m in self.f4_means]
                self.f4_last = [None, None]
                self.f4_rate = 0.1265
                self.f4_mean = 4.488
                self.f4_flow = self.f4_rate * self.f4_mean
                self.f4_extreme = inv(1 - 1e-6)
            if self.s == 2:
                self.params.update(dict(flow_prior=200, flow_level=0.6, flow_strength=1.0, flow_safety=2.0, flow_exposure_min=5.0))
                self.params.update({'kLf': 0.16})
            if self.s == 1:
                self.params.update({'dmin': 0.3, 'pfl': 1e-06})
                if 1 in ON['postjump']:
                    self.params['qb_z'] = 4.0
            if self.s == 3:
                self.params.update({'flow_prior': 200, 'flow_level': 0.6, 'flow_strength': 1.0, 'flow_safety': 2.0, 'flow_exposure_min': 5.0})
        P = self.params
        s1 = self.s == 1
        AH = s1 and F_AH
        FL = s1 and F_FL
        QB = s1 and F_QB
        if self.s == 4:
            for side, filled, bound in ((0, state.sell_filled_quantity, ca), (1, state.buy_filled_quantity, cb)):
                last = self.f4_last[side]
                if last is None:
                    continue
                tick, conv, cap, old_bound, ids = last
                if (side == 0 and bound > old_bound + 1) or (side == 1 and bound < old_bound - 1):
                    continue
                # Track only the main quote, excluding probes and stock orders.
                remaining = sum(o.remaining_quantity for o in state.own_orders if o.order_id in ids)
                value = max(0.0, cap - remaining * conv)
                self.f4_exposure[side] += 1
                if value > 0.01:
                    self.f4_events[side] += 1
                    censored = remaining < 0.011
                    logv = math.log(max(value, 0.01))
                    weights = self.f4_weights[side]
                    for i, mu4 in enumerate(self.f4_mu):
                        z4 = (logv - mu4) / 1.2
                        weights[i] += math.log(max(1e-12, 1.0 - cdf(z4))) if censored else -0.5 * z4 * z4
            if state.step % 25 == 0:
                exposure = sum(self.f4_exposure)
                events = sum(self.f4_events)
                event_probability = (events + 80.0 * (1.0 - math.exp(-0.1265))) / (exposure + 80.0)
                self.f4_rate = max(0.077, min(0.176, -math.log(max(1e-6, 1.0 - event_probability))))
                weights = [a + b for a, b in zip(*self.f4_weights)]
                peak = max(weights)
                weights = [math.exp(w - peak) for w in weights]
                self.f4_mean = sum(m * w for m, w in zip(self.f4_means, weights)) / sum(weights)
                self.f4_flow = self.f4_rate * self.f4_mean
        if self.s in (2, 3) and self.last_quote_exposed and ca <= self.last_flow_ca + 1:
            self.flow_exposure += 1
            self.flow_notional += min(self.last_flow_cap, state.sell_filled_quantity * self.last_ask_tick / 100.0) * self.last_flow_correction
        lo, hi = cb, ca
        for o in state.own_orders:
            if o.side is Side.BUY:
                lo = max(lo, o.price_ticks)
            else:
                hi = min(hi, o.price_ticks)
        if P['pinf'] > 0:
            sb = {o.price_ticks for o in state.own_orders if o.side is Side.BUY and o.remaining_quantity <= PROBE + 1e-9}
            sa = {o.price_ticks for o in state.own_orders if o.side is Side.SELL and o.remaining_quantity <= PROBE + 1e-9}
            ea = self.pa - sa
            eb = self.pb - sb
            if sa and ea:
                lo = max(lo, min(max(ea), hi))
            if eb and (sb or min(eb) <= P['p1t']):
                hi = min(hi, max(min(eb), lo))
        retreat_ask = retreat_bid = False
        if P['jumpinfo'] > 0 and self.pcb is not None:
            if self.s in ON['cut']:
                retreat_ask = ca == self.pca + 1
                retreat_bid = cb == self.pcb - 1
            if ca > self.pca + 1:
                lo = max(lo, ca - 1)
            if cb < self.pcb - 1:
                hi = min(hi, cb + 1)
        hitB = hitA = shB = shA = False
        if self.s == 2:
            ids = {o.order_id for o in state.own_orders}
            hitB = bool(self.s2_mb) and not (self.s2_mb & ids)
            hitA = bool(self.s2_ma) and not (self.s2_ma & ids)
            if hitB:
                self.s2_lb = state.step
            if hitA:
                self.s2_la = state.step
            hitB = state.step - self.s2_lb < 1
            hitA = state.step - self.s2_la < 1
            if self.pcb is not None:
                shB = cb < self.pcb - 1
                shA = ca > self.pca + 1
        self.pcb, self.pca = cb, ca
        if lo > hi:
            lo, hi = hi, lo
        # sub-tick belief over p_(t-1): predict with one-step noise, truncate to [lo, hi]
        wid = max(hi - lo, 1e-6)
        nb = max(2, min(48, int(round(wid * P['bins']))))
        cs = [lo + (i + 0.5) * wid / nb for i in range(nb)]
        if self.bc is None or P['filt'] <= 0:
            ws = [1.0 / nb] * nb
        else:
            sg = max(self.st, 0.6 * wid / nb)
            k = -0.5 / (sg * sg)
            ws = []
            uni = P['uni'] * sg
            if self.s == 4:
                exp = math.exp
                if self.bc == cs and 1.0 <= wid <= 6.0 and nb == 8 * wid:
                    # On this stationary grid, spacing is exactly 1/8 tick.
                    # Equal index distances therefore have bit-identical d*d*k.
                    # Reuse exp values while retaining the original sum order.
                    kernel = []
                    c0 = cs[0]
                    for ci in self.bc:
                        d = c0 - ci
                        d2 = d * d * k
                        kernel.append(exp(d2) if d2 > -12.5 else 0.0)
                    kernel = kernel[:0:-1] + kernel
                    for i in range(nb):
                        t = uni
                        start = nb - 1 - i
                        for wi, e in zip(self.bw, kernel[start:start + nb]):
                            if e:
                                t += wi * e
                        ws.append(t)
                else:
                    previous = tuple(zip(self.bc, self.bw))
                    for c in cs:
                        t = uni
                        for ci, wi in previous:
                            d = c - ci
                            d2 = d * d * k
                            if d2 > -12.5:
                                t += wi * exp(d2)
                        ws.append(t)
            else:
                for c in cs:
                    t = uni
                    for ci, wi in zip(self.bc, self.bw):
                        d = c - ci
                        d2 = d * d * k
                        if d2 > -12.5:
                            t += wi * math.exp(d2)
                    ws.append(t)
            tot = sum(ws)
            ws = [w / tot for w in ws]
        if retreat_ask or retreat_bid:
            ws = [weight * (0.016 if retreat_ask and c < ca - 1 else 1.0)
                  * (0.016 if retreat_bid and c > cb + 1 else 1.0)
                  for c, weight in zip(cs, ws)]
            tot = sum(ws)
            ws = [weight / tot for weight in ws]
        self.bc, self.bw = cs, ws
        mean_t = sum(c * w for c, w in zip(cs, ws))
        var_t = max(sum(c * c * w for c, w in zip(cs, ws)) - mean_t * mean_t, 0.0)
        phat = min(max(mean_t / 100.0, 0.002), 0.998)
        var = P['sig'] ** 2 + P['lam_j'] * P['sig_j'] ** 2
        sd = math.sqrt(H * var)
        self.tb = self.tb + 1 if hi <= 1 else 0
        if self.tb > 0 and P['zd'] > 0:
            # below the last tick there is no probe: the score keeps walking away from it
            phat = min(phat, max(P['pfl'], cdf(inv(0.01) - P['zd'] * 0.02 * math.sqrt(self.tb) / sd)))
        z = inv(phat)
        Z = z * sd
        sp = pdf(z) / sd * P['sig']
        self.st = sp * 100.0
        if FL:
            remaining={o.order_id:o.remaining_quantity for o in state.own_orders} if self.fl_obs else {}
            for px, ci, buying, previous, tick in self.fl_obs:
                qty=max(0.0,sum(q-remaining.get(oid,0.0) for oid,q in previous))
                x=qty*px
                cap=FLOW_CAPS[ci]
                gap=tick/100.0-phat if buying else phat-tick/100.0
                safe=gap>max(0.005,2.0*math.sqrt(var_t)/100.0)
                if 0<x<0.03:
                    continue
                if x>=cap:
                    if safe:
                        self.fl_sbins[ci]+=1
                        self.fl_exp+=1
                        self.fl_dirty=True
                    continue
                if safe:
                    self.fl_safe_n+=1
                else:
                    self.fl_bins[ci]+=1
                self.fl_exp+=1
                self.fl_dirty=True
                if buying:
                    self.fl_buy_exp+=1
                else:
                    self.fl_sell_exp+=1
                if x>0:
                    lx=math.log(x)
                    for i,(r,m,parts,norm,tails) in enumerate(FLOW_GRID):
                        density=sum(w*pdf((lx-mu)/sg)/sg for mu,sg,w in parts)
                        self.fl_scores[i]+=math.log(max(density,1e-100))
            if state.step % 100 == 0 and (self.fl_dirty or state.step==0):
                bins=[(i,n) for i,n in enumerate(self.fl_bins) if n]
                sbins=[(i,n) for i,n in enumerate(self.fl_sbins) if n]
                logs=[score-sum(n*g[3][i] for i,n in bins)-g[0]*self.fl_safe_n+sum(n*g[4][i] for i,n in sbins) for score,g in zip(self.fl_scores,FLOW_GRID)]
                mx=max(logs)
                weights=[math.exp(v-mx) for v in logs]
                den=sum(weights)
                self.fl_dirty=False
                self.fl_rate=sum(w*g[0]*g[1] for w,g in zip(weights,FLOW_GRID))/den
                self.fl_r=sum(w*g[0] for w,g in zip(weights,FLOW_GRID))/den
                self.fl_m=sum(w*g[1] for w,g in zip(weights,FLOW_GRID))/den

        s = math.sqrt(sp * sp + var_t / 1e4 + 1e-8)
        sd1 = math.sqrt(max(1.0, H - 1.0) * var)
        jp = [(cdf((Z + n * P['sig_j']) / sd1), w) for n, w in NODES]
        lj = P['lam_j']

        def AB(x):
            k = (x - phat) / s
            a = s * lpm(k)
            b = a - (x - phat)
            if self.s == 4:
                ja = jb = 0.0
                for p, w in jp:
                    if x > p:
                        ja += w * (x - p)
                    else:
                        jb += w * (p - x)
            else:
                ja = sum(w * max(0.0, x - p) for p, w in jp)
                jb = sum(w * max(0.0, p - x) for p, w in jp)
            return (1 - lj) * a + lj * ja, (1 - lj) * b + lj * jb

        if H == 1:
            def AB(x):
                return (1 - phat) * x, phat * (1 - x)
        rho = P['lam_r'] * 0.5
        mu = math.log(P['m']) - 0.5 * P['sig_n'] ** 2
        kA = P['kL'] if phat < P['pL'] else P['kA']

        def qsize(loss, gain, px, flow=False, cap=None):
            loss *= kA
            if gain <= 0:
                return 0.0
            rr = (0.125+0.5*(self.fl_r-0.125)) if flow and FL else rho
            mm = math.log(5.0+0.5*(self.fl_m-5.0))-0.5*P['sig_n']**2 if flow and FL else mu
            tail = loss / (rr * gain)
            if tail >= 1.0:
                return 0.0
            if self.s == 4 and tail <= 1e-6:
                return min(P['qmax'], math.exp(mu + P['sig_n'] * self.f4_extreme) / px)
            return min((cap if cap is not None else P['qmax']), math.exp(mm + P['sig_n'] * inv(1 - max(tail, 1e-6))) / px)

        ptk = phat * 100
        def qbid(t):
            if not 1 <= t <= 99:
                return 0.0
            if self.s == 4 and phat * 100 - t < P['dmin']:
                return 0.0
            a, b = AB(t / 100.0)
            if phat * 100 - t < P['dmin']:
                return 0.0
            if P['nb1'] > 0 and self.s == 1 and t == 1 and ptk < 1.0:
                return 0.0
            if phat < P['pL']:
                ytg = P['ydem'] * min(H, P['W']) / max(ca - 1, ptk + 1) * 100.0
                a *= (P['kLb'] if state.yes_inventory < ytg else P['kLf']) / P['kL']
                if self.s == 3:
                    # Subsidize cover only while more stock is needed for remaining retail.
                    # Once the whole horizon is covered, use the ordinary bid risk weight.
                    flow = (self.flow_notional + P['flow_prior'] * P['flow_level']) / (P['flow_prior'] + self.flow_exposure)
                    if state.yes_inventory >= flow * H / max(ca - 1, ptk + 1) * 100.0:
                        a *= P['kA'] / P['kLf']
            return qsize(a, b, max(phat, 0.05))

        def qask(t):
            if not 1 <= t <= 99:
                return 0.0
            if self.s == 4 and t - phat * 100 < P['dmin']:
                return 0.0
            a, b = AB(t / 100.0)
            if t - phat * 100 < P['dmin']:
                return 0.0
            if self.s == 4:
                if 4 not in ON['premium'] and P['pL'] <= phat <= 0.95:
                    b *= 1.4
                tail = b * kA / max(self.f4_rate * a, 1e-30)
                if a <= 0 or tail >= 1.0:
                    return 0.0
                return min(P['qmax'], math.exp(math.log(self.f4_mean) - 0.72 + 1.2 * (self.f4_extreme if tail <= 1e-6 else inv(1 - tail))) / (t / 100.0))
            return qsize(b, a, t / 100.0, flow=True, cap=(15000 if AH and t == 2 and phat < 0.01 else None))

        bids = [o for o in state.own_orders if o.side is Side.BUY and o.remaining_quantity > PROBE + 1e-9]
        asks = [o for o in state.own_orders if o.side is Side.SELL and o.remaining_quantity > PROBE + 1e-9]
        sticky = P['sticky'] > 0
        def top(orders, comp, step):
            threshold = P['min_ahead']
            if self.s == 3 and step == -1 and 1 <= comp <= 5:
                threshold = max(P['min_ahead'], 20 * 100.0 / comp)
            elif QB and step == 1:
                threshold = PROBE + 0.01
            elif self.s == 2:
                # spread 2: a front order that one ordinary retail buy would use up is not worth holding the quote at the rival's tick
                threshold = max(P['min_ahead'], 400.0 / max(comp, 1))
            elif self.s == 4 and step < 0 and phat < 0.05:
                threshold = 50.0
            if sticky and sum(o.remaining_quantity for o in orders if o.price_ticks == comp and o.order_id in self.ahead) >= threshold:
                return comp
            return comp + step
        bid_t = top(bids, cb, 1)
        ask_t = top(asks, ca, -1)
        qb = qbid(bid_t)
        qa = qask(ask_t)
        s2f = self.s == 2 and bid_t == cb and qb > 0 and cb / 100.0 < phat
        if self.s == 4 and phat < 0.05 and bid_t >= 2:
            qb *= 0.5
        if self.s == 1 and ask_t == 2 and ask_t < ca and phat < 0.01:
            qa *= 5

        Y = state.yes_inventory
        if ask_t == 1 and H > P['H1'] and P['pre'] > 0:
            qa = qa if Y >= P['a1'] > 0 else 0.0          # let the competitor's 2-tick ask erode instead of fronting it for nothing
        # ammunition: hold YES so that low asks are covered
        ptick = phat * 100
        amt = 0
        qam = 0.0
        fs1 = max(0.4,min(1.9,1.0+0.5*(self.fl_rate/0.568734-1))) if FL else 1.0
        if P['ammo'] > 0 and ask_t >= 2 and phat < max(P['ammo_pmax'], P['pmaxf']):
            wealth = state.cash + Y * phat
            x = max(ask_t, ptick + 1) / 100.0
            capw = P['fy'] * wealth / max(phat, 0.005)
            flow_scale = self.f4_flow / 0.6 if self.s == 4 else fs1
            target = min(flow_scale * P['ydem'] * min(H, P['W']) / x, capw)
            if self.s == 3:
                # Buy routine cover only for the current front ask's desired size.
                target = min(target, qa)
            if self.s == 4:
                # Pay above fair value only for the current retail quote's cover.
                target = min(target, qa)
            full = min(flow_scale * P['ydf'] * min(H, P['Wf']) / x, capw) if phat < P['pmaxf'] else 0.0
            t = max(1, min(99, int(math.ceil(ptick + 1e-9))))
            g = t - ptick
            if self.s != 3 and Y < full and g <= P['g_hi'] and bid_t <= t < ask_t:
                amt, qam = t, min(P['qf'], full - Y)     # a tick p has just crossed: nearly free
            elif (self.s != 2 or t == 1) and Y < target and phat < P['ammo_pmax'] and bid_t <= t < ask_t and t / 100.0 - phat < P['ammo_maxpay']:
                if self.s == 1:
                    passive_t = t - 1
                    if passive_t >= max(1, bid_t):
                        amt, qam = passive_t, min(P['ammo_q'], target - Y)
                else:
                    amt, qam = t, min(P['ammo_q'], target - Y)
            elif Y < full and t >= 2 and 1.0 - g <= P['g_lo']:
                amt, qam = t - 1, min(P['qf'], full - Y)  # rest just under p: filled only on the crossing, or by retail

        if P['pre'] > 0 and ca == 2 and phat < 0.01 and H > P['H1'] and Y < P['pre'] and not qam and 1.0 - ptick < P['pre_gap']:
            amt, qam = 1, min(P['ammo_q'], P['pre'] - Y)
        q1 = 0.0
        if P['ydf1'] > 0 and P['m1'] < ptick < P['g1'] + 1.0 and amt != 1:
            stock_rate = fs1 * P['ydf1']
            if self.s == 4:
                stock_rate *= self.f4_flow / 0.6
            if self.s in (2, 3):
                flow = (self.flow_notional + P['flow_prior'] * P['flow_level']) / (P['flow_prior'] + self.flow_exposure)
                scale = max(0.5, min(2.0, flow / P['flow_level']))
                stock_rate *= 1.0 + P['flow_strength'] * (scale - 1.0)
            q1 = max(0.0, stock_rate * min(H, P['Wf']) / (self.s / 100.0) - Y)

        # Bridge expected retail demand until another tick crossing is available.
        if 0.02 < phat < 0.1:
            ct = max(2, min(99, int(math.floor(ptick))))
            wealth = state.cash + Y * phat
            goal = min(fs1 * qa, 0.3 * max(wealth, 0.0) / phat)
            if Y < goal and ct < ask_t:
                amt, qam = ct, min(3000.0, goal - Y)
        if self.s == 2:
            if hitB:
                qb = 0.0
                qam = 0.0
                q1 = 0.0
            if hitA:
                qa = 0.0
        # order management
        actions = []
        free = state.free_cash - 2.0
        keep_ask = 0.0
        new_b = []
        new_a = []
        def cancel(o):
            nonlocal free
            actions.append(CancelOrder(o.order_id))
            x = o.price_ticks / 100.0
            if o.side is Side.BUY:
                free += x * o.remaining_quantity
            else:
                free += (1 - x) * min(self.res.get(o.order_id, 0.0), o.remaining_quantity)
            self.ahead.discard(o.order_id)
            self.res.pop(o.order_id, None)
        for o in state.own_orders:
            if o.remaining_quantity <= PROBE + 1e-9:
                cancel(o)
        kept_ids = set()
        def manage(orders, t, q, comp):
            kept = 0.0
            if self.s == 2:
                buy = comp == cb
                held = {}
                for o in orders:
                    x = o.price_ticks
                    gain = ptk - x if buy else x - ptk
                    # under 10 cents a front order is kept whole for its life: resizing it would give up its place to the rival
                    if x == t and q > 0 and (kept + o.remaining_quantity <= max(q * P['keep_hi'], 1.0) or (x == comp and o.order_id in self.ahead and ptk <= 10.0 and gain >= 0.0)):
                        kept += o.remaining_quantity
                        kept_ids.add(o.order_id)
                        continue
                    # a small front remainder stays behind the new inside quote: it still fills ahead of the rival on a large retail order
                    if x == comp and x != t and o.order_id in self.ahead and gain >= 1.0:
                        if x not in held:
                            held[x] = [0.0, qbid(x) if buy else qask(x)]
                        h = held[x]
                        if h[0] + o.remaining_quantity <= max(h[1], 1.0) and h[1] > 0:
                            h[0] += o.remaining_quantity
                            kept_ids.add(o.order_id)
                            continue
                    cancel(o)
                return kept
            banked = {}
            bound_t, bound_q = t, q
            for o in orders:
                ah = o.order_id in self.ahead
                if AH and ah and o.remaining_quantity >= P['min_ahead'] and o.price_ticks != t:
                    if (o.side is Side.SELL and o.price_ticks > t) or (o.side is Side.BUY and o.price_ticks < t):
                        enough = bound_q > 0 and (
                            o.remaining_quantity <= bound_q if o.side is Side.BUY else
                            o.remaining_quantity * o.price_ticks <= min(bound_q, P['qmax']) * bound_t)
                        if enough:
                            kept_ids.add(o.order_id)
                            continue
                        if o.price_ticks == bound_t:
                            capacity = bound_q
                        else:
                            capacity = qask(o.price_ticks) if o.side is Side.SELL else qbid(o.price_ticks)
                            bound_t, bound_q = o.price_ticks, capacity
                        if capacity > 0 and o.remaining_quantity <= max(capacity, 1.0):
                            kept_ids.add(o.order_id)
                            continue
                if QB and ah and o.side is Side.BUY and o.price_ticks < t and ('qb_z' not in P or ptk - o.price_ticks >= P['qb_z'] * 100.0 * s) and banked.get(o.price_ticks, 0.0) + o.remaining_quantity <= P['keep_hi'] * qbid(o.price_ticks):
                    banked[o.price_ticks] = banked.get(o.price_ticks, 0.0) + o.remaining_quantity
                    kept_ids.add(o.order_id)
                    continue
                khi = 10.0 if (AH and ah) else (3.0 if (self.s == 4 and o.side is Side.SELL and ah and o.price_ticks == comp) else P['keep_hi'])
                if o.price_ticks == t and q > 0 and (kept + o.remaining_quantity <= max(q * khi, 1.0)
                        or (s1 and ah and (o.side is Side.SELL) and o.price_ticks <= 2)
                                        or (QB and ah and o.side is Side.BUY and o.price_ticks == comp)):
                    kept += o.remaining_quantity
                    kept_ids.add(o.order_id)
                else:
                    cancel(o)
            return kept
        if s2f and 1:
            kb = 0.0
            for o in bids:
                if o.price_ticks == bid_t and o.order_id in self.ahead:
                    kb += o.remaining_quantity
                    kept_ids.add(o.order_id)
                else:
                    cancel(o)
        elif self.s == 2 and 1 and bid_t == cb + 1:
            qf = qbid(cb) if 1 else 1.0
            fr = [o for o in bids if o.price_ticks == cb and o.order_id in self.ahead and cb / 100.0 < phat - 0.0 and qf > 0]
            for o in fr:
                kept_ids.add(o.order_id)
            kb = manage([o for o in bids if o not in fr], bid_t, qb, cb)
        else:
            kb = manage(bids, bid_t, qb, cb)
        ka = manage(asks, ask_t, qa, ca)
        dbk = 1.0 if self.s in ON['deadband'] else P['keep_lo']
        add_b = (qb - kb) if (kb < qb * dbk and bid_t != cb) else 0.0
        add_a = (qa - ka) if (ka < qa * dbk and ask_t != ca) else 0.0

        budget = P['fb'] * max(free, 0.0)
        cost = add_b * bid_t / 100.0 + qam * amt / 100.0
        if cost > budget:
            f = budget / cost
            add_b *= f
            qam *= f
            cost = budget
        out = []
        q1 = min(q1, P['f1'] * max(budget - cost, 0.0) * 100.0)
        if q1 >= 0.01:
            out.append(PlaceOrder(side=Side.BUY, price_ticks=1, quantity=fl(q1)))
            free -= fl(q1) / 100.0 + 1e-6
        if amt and qam >= 0.01:
            q = fl(qam)
            if QB:
                oid = self._oid('m')
                out.append(PlaceOrder(side=Side.BUY, price_ticks=amt, quantity=q, client_order_id=oid))
                if amt > cb:
                    self.ahead.add(oid)
            else:
                out.append(PlaceOrder(side=Side.BUY, price_ticks=amt, quantity=q))
            free -= q * amt / 100.0 + 1e-6
        if bid_t >= 1 and add_b >= 0.01:
            q = fl(add_b)
            total_q = q
            if self.s == 4 and ca <= 99 and bid_t > cb and bid_t == ca - 4 and q >= 4.0 and q * bid_t / 100 >= 4 * P['m']:
                head = fl(q / 2)
                oid = self._oid('b')
                out.append(PlaceOrder(side=Side.BUY, price_ticks=bid_t, quantity=head, client_order_id=oid))
                self.ahead.add(oid)
                q = fl(q - head)
            oid = self._oid('b')
            out.append(PlaceOrder(side=Side.BUY, price_ticks=bid_t, quantity=q, client_order_id=oid))
            free -= total_q * bid_t / 100.0 + 1e-6
            if bid_t > cb:
                self.ahead.add(oid)
        if ask_t <= 99 and add_a >= 0.01:
            x = ask_t / 100.0
            covk = sum(o.remaining_quantity - min(self.res.get(o.order_id, 0.0), o.remaining_quantity)
                       for o in asks if o.order_id in kept_ids)
            cov = max(0.0, Y - covk - 0.1)
            unc = max(0.0, add_a - cov)
            if unc > 0:
                ub = max(0.0, free - (1 - P['fu']) * max(state.cash, 0.0)) if x >= P['xu'] else 0.0
                if H < P['Hu'] and phat < 0.05:
                    ub = max(0.0, free * (1 - H / P['Hu']))
                unc = min(unc, ub / (1 - x))
            q = fl(min(add_a, cov + unc))
            if q >= 0.01:
                oid = self._oid('a')
                out.append(PlaceOrder(side=Side.SELL, price_ticks=ask_t, quantity=q, client_order_id=oid))
                r = max(0.0, q - cov)
                self.res[oid] = r
                free -= r * (1 - x) + 1e-6
                if ask_t < ca:
                    self.ahead.add(oid)

        # probes: tiny orders that the arbitrageur removes when p crosses them
        f = int(math.floor(ptick + 1e-9))
        r = max(int(P['rmin']), int(math.ceil(2.0 * s * 100)))
        self.pb = set()
        self.pa = set()
        if free > 1.0:
            for t in range(f, f + r + 1):
                if cb < t < ca and 1 <= t <= 99:
                    out.append(PlaceOrder(side=Side.BUY, price_ticks=t, quantity=PROBE))
                    self.pb.add(t)
            for t in range(f + 1 - r, f + 2):
                if cb < t < ca and 1 <= t <= 99:
                    out.append(PlaceOrder(side=Side.SELL, price_ticks=t, quantity=PROBE))
                    self.pa.add(t)
        if self.s in (2, 3):
            self.last_ask_tick = ask_t
            self.last_flow_ca = ca
            exposed_qty = ka + sum(o.quantity for o in out if o.side is Side.SELL and o.price_ticks == ask_t and o.quantity > PROBE)
            self.last_flow_cap = exposed_qty * ask_t / 100.0
            self.last_quote_exposed = ask_t / 100.0 > phat + max(0.005, P['flow_safety'] * self.st / 100.0) and self.last_flow_cap >= P['flow_exposure_min']
            if self.last_quote_exposed:
                logcap = math.log(self.last_flow_cap)
                mu_flow = math.log(P['m']) - 0.5 * P['sig_n'] ** 2
                clipped = P['m'] * cdf((logcap - mu_flow - P['sig_n'] ** 2) / P['sig_n']) + self.last_flow_cap * (1.0 - cdf((logcap - mu_flow) / P['sig_n']))
                self.last_flow_correction = min(3.0, P['m'] / max(clipped, 0.01))
        if self.s == 1:
            split_out = []
            for order in out:
                oid = order.client_order_id
                if (order.side is Side.SELL and oid is not None and oid.startswith('a')
                        and order.price_ticks >= 3 and order.price_ticks < 99):
                    back = fl(order.quantity * 0.5)
                    front = fl(order.quantity - back)
                    reserve = self.res.pop(oid, 0.0)
                    front_reserve = max(0.0, reserve - back)
                    if front >= 0.01:
                        split_out.append(PlaceOrder(side=Side.SELL, price_ticks=order.price_ticks, quantity=front, client_order_id=oid))
                        self.res[oid] = front_reserve
                    if back >= 0.01:
                        back_id = self._oid('a')
                        split_out.append(PlaceOrder(side=Side.SELL, price_ticks=order.price_ticks + 1, quantity=back, client_order_id=back_id))
                        self.res[back_id] = max(0.0, reserve-front_reserve)
                else:
                    split_out.append(order)
            out = split_out
        if FL:
            if not kept_ids and not any(o.quantity>PROBE for o in out):
                self.fl_obs=()
                self.fl_ahead.clear()
                return actions+out
            # Give stock orders explicit ids so per-order remaining quantities
            # separate their fills from other bid levels and tiny probes.
            for i,o in enumerate(out):
                if o.client_order_id is None and o.quantity>PROBE:
                    out[i]=PlaceOrder(side=o.side,price_ticks=o.price_ticks,quantity=o.quantity,client_order_id=self._oid('f'))
            live=[]
            oldids={o.order_id for o in state.own_orders if o.order_id in kept_ids}
            self.fl_ahead.intersection_update(oldids)
            for o in state.own_orders:
                if o.order_id in kept_ids and o.remaining_quantity>PROBE:
                    live.append((o.side,o.price_ticks,o.remaining_quantity,o.order_id))
            for o in out:
                if o.quantity>PROBE:
                    live.append((o.side,o.price_ticks,o.quantity,o.client_order_id))
                    if (o.side is Side.SELL and o.price_ticks<ca) or (o.side is Side.BUY and o.price_ticks>cb):
                        self.fl_ahead.add(o.client_order_id)
            obs=[]
            for buying,side,comp in ((True,Side.SELL,ca),(False,Side.BUY,cb)):
                orders=[o for o in live if o[0] is side]
                if not orders:
                    continue
                tick=min(o[1] for o in orders) if buying else max(o[1] for o in orders)
                orders=[o for o in orders if o[1]==tick]
                if not all(o[3] in self.fl_ahead for o in orders):
                    continue
                if (buying and tick>comp) or (not buying and tick<comp):
                    continue
                px=tick/100.0 if buying else max(phat,0.05)
                cap=sum(o[2] for o in orders)*px
                if cap<0.04:
                    continue
                ci=0
                while ci+1<len(FLOW_CAPS) and FLOW_CAPS[ci+1]<cap-0.01:
                    ci+=1
                obs.append((px,ci,buying,[(o[3],o[2]) for o in orders],tick))
            self.fl_obs=obs
        if self.s == 4:
            self.f4_last = [None, None]
            # Eligibility is decided before observing fills, so depleted quotes
            # remain in the sample as right-censored observations.
            for side, tick, bound, conv, distance in (
                (0, ask_t, ca, ask_t / 100.0, ask_t / 100.0 - phat),
                (1, bid_t, cb, max(phat, 0.05), phat - bid_t / 100.0)):
                if distance < max(0.01, 3.0 * self.st / 100.0):
                    continue
                if side == 0:
                    if not (ask_t < ca or any(o.price_ticks == ask_t and o.order_id in self.ahead for o in asks)):
                        continue
                    orders = asks
                    order_side = Side.SELL
                else:
                    if not (bid_t > cb or any(o.price_ticks == bid_t and o.order_id in self.ahead for o in bids)):
                        continue
                    if (qam > 0 and amt >= bid_t) or (q1 > 0 and bid_t <= 1):
                        continue
                    orders = bids
                    order_side = Side.BUY
                tracked = {o.order_id: o.remaining_quantity for o in orders if o.order_id in kept_ids and o.price_ticks == tick}
                tracked.update({o.client_order_id: o.quantity for o in out if o.side is order_side and o.price_ticks == tick and o.client_order_id is not None})
                cap = sum(tracked.values()) * conv
                if cap >= 0.5:
                    self.f4_last[side] = (tick, conv, cap, bound, tracked)
        if self.s == 2:
            self.s2_mb = {o.order_id for o in bids if o.order_id in kept_ids} | {o.client_order_id for o in out if o.side is Side.BUY and o.client_order_id}
            self.s2_ma = {o.order_id for o in asks if o.order_id in kept_ids} | {o.client_order_id for o in out if o.side is Side.SELL and o.client_order_id}
        return actions + out


_IncumbentStrategy = Strategy

class Strategy(_IncumbentStrategy):
    """cancel: for one callback after the rival's bid falls (ask rises) exactly one tick, cancel that side and place nothing there."""
    def __init__(self):
        super().__init__()
        self._retreat_previous = (None, None)
        self._retreat_left = {Side.BUY: 0, Side.SELL: 0}

    def on_step(self, state):
        bid = state.competitor_best_bid_ticks
        ask = state.competitor_best_ask_ticks
        old_bid, old_ask = self._retreat_previous
        self._retreat_previous = (bid, ask)
        actions = super().on_step(state)
        if self.s not in ON['cancel']:
            return actions
        for side, retreat in (
            (Side.BUY, bid is not None and old_bid is not None and bid == old_bid - 1),
            (Side.SELL, ask is not None and old_ask is not None and ask == old_ask + 1),
        ):
            if retreat:
                self._retreat_left[side] = 1
        blocked = {side for side, left in self._retreat_left.items() if left > 0}
        for side in blocked:
            self._retreat_left[side] -= 1
        if not blocked:
            return actions
        out = []
        for action in actions:
            if isinstance(action, PlaceOrder) and action.side in blocked:
                self.ahead.discard(action.client_order_id)
                self.res.pop(action.client_order_id, None)
            else:
                out.append(action)
        canceled = {a.order_id for a in out if isinstance(a, CancelOrder)}
        out.extend(CancelOrder(o.order_id) for o in state.own_orders
                   if o.side in blocked and o.order_id not in canceled)
        # Forget everything held about the withheld side, so our own cancels are not read as fills or hits.
        if Side.BUY in blocked:
            self.pb.clear()
            self.s2_mb = set()
            self.fl_obs = tuple(x for x in self.fl_obs if x[2])
            if self.s == 4:
                self.f4_last[1] = None
        if Side.SELL in blocked:
            self.pa.clear()
            self.s2_ma = set()
            self.last_quote_exposed = False
            self.fl_obs = tuple(x for x in self.fl_obs if not x[2])
            if self.s == 4:
                self.f4_last[0] = None
        return out


_N = Strategy


class Strategy(BaseStrategy):
    """postjump (spread 1): after a likely jump in the rival's quotes, withhold quotes on the side the jump runs toward for a few callbacks."""
    M = 4
    JUMP = 2.0

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._n = _N(*a, **k)
        self.s = None
        self._s = None
        self._pm = None
        self._dis = 0
        self._lo = 0
        self._hi = 0
        self._dir = 0
        self._pd = 0.05

    def on_step(self, state):
        acts = self._n.on_step(state)
        b, a = state.competitor_best_bid_ticks, state.competitor_best_ask_ticks
        self.s = self._n.s
        self._s = self.s
        if self._s not in ON['postjump'] or b is None or a is None:
            return acts
        mid = (a + b) / 2.0
        pm = self._pm
        self._pm = mid
        if pm is None:
            return acts
        mv = mid - pm
        fb, fs = state.buy_filled_quantity, state.sell_filled_quantity
        ev = abs(mv) / self.JUMP + (0.5 if (fs > 0 and mv > 0) or (fb > 0 and mv < 0) else 0.0)
        p = self._pd
        lr = 2.718281828 ** (3.0 * (ev - 1.0))
        p = p * lr / (p * lr + (1 - p))
        self._pd = min(0.95, max(0.01, 0.9 * p + 0.01))
        if p > 0.5 and abs(mv) >= 1:
            self._dis = self.M
            self._dir = 1 if mv > 0 else -1
            self._lo = min(pm, mid)
            self._hi = max(pm, mid)
        elif self._dis > 0:
            if abs(mv) >= 1 and (mv > 0) == (self._dir > 0):
                self._lo = min(self._lo, mid)
                self._hi = max(self._hi, mid)
                self._dis = self.M
            else:
                self._dis -= 1
        if self._dis <= 0:
            return acts
        out = []
        for x in acts:
            if isinstance(x, PlaceOrder):
                pr = x.price_ticks
                if self._dir > 0 and x.side == Side.SELL and pr <= self._hi + self._s:
                    continue
                if self._dir < 0 and x.side == Side.BUY and pr >= self._lo - self._s:
                    continue
            out.append(x)
        return out
```

## 3. Evidence on the finalist seeds 900000..903999

All figures are paired differences per run: the candidate's `total_edge` minus the comparator's on the same seed, unmodified simulator at commit b244530ee2a6247b5f930830eeca9dd950da0e7e, default `ChallengeConfig` and `ParameterVariance`, 2,000 steps, serial engine calls, no `--sandbox`. Pooling of blocks uses mean = S/n and se = sqrt((Q − S²/n)/(n − 1)/n) from each block's n, sum of d and sum of d².

### 3.1 T against wave 3's combine-cash (the objective's start), all 4,000 finalist seeds

Run on this machine during the write-up because no handed batch measured T against combine-cash (the goal's comparisons moved with the base, section 3.2). Both files were hashed before the run (`9fba1eb5…` and `baef955e…`); combine-cash reproduces N's published check value 17.116002 on seed 310000. Six single-process workers, each on its own contiguous block, one fresh strategy instance per run.

| scope | n | T minus combine-cash | se | gain / se | retail | arb | combine-cash mean | T mean |
|---|---|---|---|---|---|---|---|---|
| **all seeds** | **4000** | **+3.502** | **0.336** | 10.4 | +1.599 | +1.903 | 102.52 | 106.02 |
| spread 1 | 991 | +6.117 | 0.827 | 7.4 | +0.913 | +5.204 | 45.50 | 51.62 |
| spread 2 | 1017 | +3.160 | 0.678 | 4.7 | +2.242 | +0.918 | 92.18 | 95.34 |
| spread 3 | 961 | +2.261 | 0.627 | 3.6 | +3.013 | -0.752 | 124.82 | 127.08 |
| spread 4 | 1031 | +2.481 | 0.525 | 4.7 | +0.305 | +2.176 | 146.73 | 149.21 |

| block | seeds | n | T minus combine-cash | se | retail | arb |
|---|---|---|---|---|---|---|
| 1 | 900000..900499 | 500 | +3.103 | 0.809 | +1.376 | +1.727 |
| 2 | 900500..900999 | 500 | +2.477 | 0.657 | +1.310 | +1.167 |
| 3 | 901000..901499 | 500 | +5.003 | 1.313 | +3.284 | +1.718 |
| 4 | 901500..901999 | 500 | +2.673 | 0.731 | +1.241 | +1.432 |
| 5 | 902000..902499 | 500 | +4.813 | 1.063 | +1.895 | +2.918 |
| 6 | 902500..902999 | 500 | +2.200 | 0.780 | +0.653 | +1.547 |
| 7 | 903000..903499 | 500 | +3.578 | 0.758 | +1.741 | +1.837 |
| 8 | 903500..903999 | 500 | +4.164 | 1.260 | +1.288 | +2.876 |

All 4,000 seeds complete, one record per seed, no failures in either file.

T beats combine-cash on 2928 seeds and loses on 1072; the rest are ties. Worst five seeds (seed, spread, d): 902511 (4, -272.2), 900327 (4, -224.2), 901136 (3, -155.8), 902361 (3, -135.7), 903352 (3, -120.8). Best five: 903835 (2, +519.8), 901130 (3, +386.7), 902357 (1, +273.0), 902256 (1, +260.8), 901023 (1, +248.3).

Mean wall seconds a simulation under six-way load: T 2.18, combine-cash 2.04 (serial and idle on this machine: T 0.9, combine-cash 0.8 on the check seeds).

### 3.2 The chain of bases, each link on the finalist seeds where it was measured

The incumbent changed three times on the requester's notes as sibling goals submitted stronger files. The links measured by this goal on seeds 900000..903999 are complete; the links measured elsewhere are quoted from the requester's notes or the file's own artifact.

| link | seeds | n | gain | se | retail | arb | per spread (gain / se) | source |
|---|---|---|---|---|---|---|---|---|
| combine-cash → N (adopted 11-06) | not on F | | | | | | N's artifact: +1.45 se 0.16 over the 108.47 file on 130000..133999 (s1 +1.64, s2 +1.73, s3 +0.49, s4 +1.87) | requester note 18:55Z |
| N → MA (adopted 11-07 00:30Z) | 900000..903999 | 4000 | **+1.258** | 0.252 | −0.435 | +1.693 | s1 +1.147/0.307 (n 991); s2 +2.784/0.934 (1017); s3 +0.568/0.117 (961); s4 +0.504/0.082 (1031) | r6-base-f merges 01 and 02 (handed) |
| N → RC (this goal's promotion) | 900000..903999 | 4000 | **+0.537** | 0.048 | −0.152 | +0.689 | s1 0 (991); s2 +1.080/0.145 (1017); s3 +1.093/0.123 (961); s4 0 (1031) | r5-final cancel-f1..f8 (handed) |
| MB → B_RC (= MB + RC's wrapper) | 700000..709999, blocks of 500 | | +0.40 | 0.04 | | | | goal 75dd8e1e, requester note 01:30Z; +0.34 on Paradigm (110.09 → 110.43) |
| MA → T | 170000..170999 | 1000 | +1.227 | 0.354 | −0.312 | +1.539 | s1 +1.40/0.75 (259); s2 +0.63/0.18 (225); s3 +1.13/0.51 (260); s4 +1.68/1.02 (256) | T's own artifact; +0.66 on Paradigm (110.21 → 110.87) |
| MA → T (partial check here) | 744 of 900000..900958 | 744 | +0.185 | 0.265 | −0.305 | +0.490 | s1 −0.02/0.70 (165); s2 +0.57/0.31 (193); s3 −0.06/0.70 (173); s4 +0.19/0.40 (213) | write-up's run, section 3.2 note below |
| combine-cash → T | 900000..903999 | 4000 | **+3.502** | 0.336 | +1.599 | +1.903 | s1 +6.117/0.827 (n 991); s2 +3.160/0.678 (n 1017); s3 +2.261/0.627 (n 961); s4 +2.481/0.525 (n 1031) | section 3.1 |

Notes on the N → MA link: one seed, 903835 (spread 2), has d = +904.35 and carries most of the second half's variance; without it the pooled gain is +1.032 se 0.112 over 3,999 seeds. The gain is arbitrage loss avoided (+1.69 per run) less retail (−0.43). N's mean on the finalist seeds is 104.14; MA's about 105.40.

T against MA on the finalist seeds was planned as batch r8-t-f (8 blocks of 500) in the last episode, but a finishing episode may spawn nothing, so that link rests on T's own 1,000-seed holdout and the board move. A partial check was run on this machine in the write-up's remaining minutes: T against MA, paired, on 744 finalist seeds (the leading seeds of six 167-seed blocks spanning 900000..900958; a partial run, not a contiguous block), 0 failures: **+0.185 se 0.265** (retail −0.305, arb +0.490); per spread s1 −0.019/0.701 (n 165), s2 +0.574/0.313 (n 193), s3 −0.056/0.703 (n 173), s4 +0.186/0.400 (n 213); worst seeds 900421 (3, −57.4), 900542 (1, −51.5), 900056 (3, −50.5). This is consistent both with zero and with T's own +1.23 se 0.35, so the MA → T link is the least established in the chain: T's standing over MA rests on its 1,000-seed holdout and the board move (110.21 → 110.87), and the full 4,000-seed measurement is the next run's first job (section 5).

### 3.3 The promotion's evidence in full: RC over N, seeds 900000..903999

RC is N's text plus a wrapper subclass appended at the end (`_IncumbentStrategy = Strategy` … ; 1,948 bytes, SHA-256 `accbde6a21b3b86b3bb95db393a74b6c9f20fde939f031db29d7d00dda13ca19`), the same text that makes B_RC from MB and T's `cancel` entry. Candidate `3c07bdcd221ac25729c3ebc92b21ac9e2014510ecb85816c4391ed81e933291f` (`code` of https://api.imd.fun/artifacts/2d4b30bbc6bffbc500b37ce5e8a1ac821d6513c52a6a2377b4be3c11d97717fb); comparator N `bf0d179f3e47d28819f6fa7e0d25548c2ced43374c216d36460b00a26a26ffae`. Every block verified both hashes and N's four check values before running; every block is complete with no failures; the rival's first quote width was checked equal to 2s − 1 on every seed.

| block | seeds | n | mean d | se | retail | arb | N's mean | worst seed (spread, d) |
|---|---|---|---|---|---|---|---|---|
| cancel-f1 | 900000..900499 | 500 | +0.467 | 0.111 | −0.196 | +0.664 | 93.96 | 900138 (2, −24.20) |
| cancel-f2 | 900500..900999 | 500 | +0.556 | 0.158 | −0.130 | +0.686 | 101.51 | 900902 (2, −20.88) |
| cancel-f3 | 901000..901499 | 500 | +0.470 | 0.162 | −0.316 | +0.786 | 114.61 | 901130 (3, −25.39) |
| cancel-f4 | 901500..901999 | 500 | +0.560 | 0.118 | −0.218 | +0.778 | 101.49 | 901980 (2, −15.61) |
| cancel-f5 | 902000..902499 | 500 | +0.630 | 0.104 | −0.049 | +0.679 | 110.32 | 902247 (2, −5.36) |
| cancel-f6 | 902500..902999 | 500 | +0.349 | 0.145 | −0.136 | +0.484 | 100.19 | 902828 (2, −45.05) |
| cancel-f7 | 903000..903499 | 500 | +0.716 | 0.143 | −0.046 | +0.762 | 100.10 | 903148 (2, −11.68) |
| cancel-f8 | 903500..903999 | 500 | +0.549 | 0.135 | −0.124 | +0.673 | 110.93 | 903956 (3, −22.64) |
| **pooled** | 900000..903999 | **4000** | **+0.537** | **0.048** | −0.152 | +0.689 | 104.14 | 902828 (2, −45.05) |

Per spread, pooled: spread 1 n 991 d = 0 on every seed; spread 2 n 1017 **+1.080 se 0.145** (retail −0.304, arb +1.384); spread 3 n 961 **+1.093 se 0.123** (retail −0.311, arb +1.404); spread 4 n 1031 d = 0 on every seed. d is non-zero on 1,978 seeds (1,451 positive, 527 negative); the five best seeds are +51.5, +34.4, +33.7, +31.8, +30.4. Overall, spread 2 and spread 3 each clear the gate (gain above twice its standard error) by a wide margin: 11.2, 7.5 and 8.9 standard errors. The plane flagged a source of cancel-f7; its numbers agree with the other seven blocks and the pool without it is +0.511 se 0.050.

RC's development evidence, in order: tuning on 320000..320199 (n 200) +0.518 se 0.151, two variants, the one-callback variant chosen; screen on 430000..430499 (n 500) +0.562 se 0.108 (s2 +1.114 se 0.357, s3 +1.109 se 0.233), 5 standard errors on a shared screen; then the finalist seeds above. The gain is arbitrage loss avoided: a one-tick rival retreat precedes a same-side sweep, and the diagnostics on N put same-side arbitrage loss after such a retreat at 2.40, 1.93, 1.81 and 1.04 per run for spreads 1 to 4.

### 3.4 Where T's gain comes from, per entry (T's own measurement, 60 runs a spread from seed 150000, halves of 30)

| entry | spread | kept | gain | se | retail | arb | halves |
|---|---|---|---|---|---|---|---|
| cancel | 1 | no | +0.91 | 1.05 | −1.73 | +2.65 | +1.85 / −0.03 |
| cancel | 2 | yes | +1.72 | 0.85 | +1.03 | +0.69 | +1.72 / +1.73 |
| cancel | 3 | yes | +1.16 | 0.30 | −0.05 | +1.21 | +1.35 / +0.98 |
| cancel | 4 | yes | +0.66 | 0.22 | −0.03 | +0.69 | +1.02 / +0.31 |
| cut | 1 | yes | +0.91 | 0.43 | −0.51 | +1.42 | +0.29 / +1.54 |
| cut | 2 | no | −1.30 | 2.68 | +1.90 | −3.19 | −0.42 / −2.17 |
| cut | 3 | no | −0.23 | 0.39 | +0.53 | −0.76 | −0.32 / −0.14 |
| cut | 4 | yes | +0.59 | 0.63 | +0.73 | −0.14 | +0.93 / +0.25 |
| postjump | 1 | yes | +0.13 | 0.07 | −0.01 | +0.15 | +0.12 / +0.15 |
| premium | 4 | no | −0.36 | 0.56 | +0.97 | −1.33 | −0.47 / −0.24 |
| deadband | 1 | no | +0.05 | 0.51 | +0.62 | −0.57 | −0.04 / +0.14 |
| deadband | 3 | yes | +0.95 | 0.50 | +1.39 | −0.44 | +1.70 / +0.20 |
| deadband | 4 | no | +1.54 | 0.93 | +2.83 | −1.29 | −0.68 / +3.76 |

These keep decisions rest on 60 runs each, so only cancel on spreads 3 and 4 and cut on spread 1 are clearly positive; the rest are within noise. Re-deciding them on thousands of seeds is the first item of section 5.

## 4. Ranked table of every promotion

The gate: a candidate replaces the incumbent for a spread when its paired gain on that spread on seeds 900000..903999 exceeds twice its standard error, with all 4,000 seeds complete, no failures and the frozen hashes verified. One candidate passed it. The base itself moved three times by adoption on the requester's notes; those are listed separately because they did not pass through this gate.

### 4.1 Promotions through the gate

| rank | round | spreads | old → new (code SHA-256) | code | F n | gain | se | per spread | retail | arb | worst seed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 4 | 2, 3 | N `bf0d179f…` → RC `3c07bdcd221ac25729c3ebc92b21ac9e2014510ecb85816c4391ed81e933291f` | https://api.imd.fun/artifacts/2d4b30bbc6bffbc500b37ce5e8a1ac821d6513c52a6a2377b4be3c11d97717fb | 4000 | **+0.537** | 0.048 | s2 +1.080/0.145; s3 +1.093/0.123; s1, s4 exactly 0 | −0.152 | +0.689 | 902828 (−45.1) |

RC's wrapper is what carried the live board from 110.21 (MB) to 110.43 (B_RC) on 2026-11-07 01:13Z, and it is T's `cancel` entry on spreads 2, 3 and 4.

**Runner-up, not promoted.** retreat-crossing `b5158a963a479a0919146dc0d56a347b68ddc2d66dd7c467b48473baef8997cf` (`code` of https://api.imd.fun/artifacts/459d3ec15ee1323593c23f1933500cb42ac662c51e5e2aa89f9b1befee3640d1; spread 3 belief reweight on a one-tick rival retreat) against N on 3,948 of the finalist seeds: overall +0.108 se 0.043, spread 3 +0.45 se 0.18. It clears the gate on spread 3 but RC gains twice as much there, and their combination on top of RC screened −0.18 se 0.18, so RC holds spread 3. T's `cut` entry is this family's descendant.

### 4.2 Adoptions of the base (requester's notes, not through the gate)

| when (2026) | base | code SHA-256 | evidence quoted at adoption | board |
|---|---|---|---|---|
| start | combine-cash (wave 3) | `baef955ec10728839f7c3357016ec9eb0550e7ec689bbd5171b1cdd5c9e37273` | +2.08 se 0.41 over the old base on 30000..30599 | 104.84, 3rd |
| 11-06 18:55Z | N (goal 253f3b6a, per-spread merge of four blocks) | `bf0d179f3e47d28819f6fa7e0d25548c2ced43374c216d36460b00a26a26ffae` | +1.45 se 0.16 over the 108.47 file | 109.79, 2nd |
| 11-07 00:30Z | MA (m-plus-a, N's blocks plus fixes) | `5d1bd5272884f513b19f0e66a7c235f6c188a08e4f7787ac9346f1614dda3ed3` | +2.43 se 0.22 over the 108.47 file; this goal: +1.258 se 0.252 over N on all 4,000 finalist seeds | 110.21, 2nd |
| 11-07 01:30Z | B_RC (MB + RC's wrapper) | `02696ea6fd0922f64167a1153748f6a38bf2fd5d87c7a4ac6cb974bb9482f57c` | +0.40 se 0.04 over MB (goal 75dd8e1e) | 110.43, 2nd |
| 11-07 02:05Z | T (MA + cancel, cut, postjump, deadband per spread) | `9fba1eb5659d5b0ac9b7273a968a520ef9a95551c697be22020993005af70192` | +1.227 se 0.354 over MA on 170000..170999 | **110.87, 1st** |

### 4.3 What was measured and did not promote (scoreboard, best rows)

Every row is candidate minus the base named, on the seeds named, complete unless said. Screens share one holdout across a round's items, so their ranking is selected; only the finalist rows above are unselected.

| round | candidate (code SHA-256 prefix) | base | seeds, n | target spread gain / se | overall gain / se | verdict |
|---|---|---|---|---|---|---|
| 1–2 | side-jump-budget `3b7236c9` | combine-cash | 254000..257999, 4000 | | +0.519 / 0.235 | 2.2 se, but −0.43 se 0.23 when ported to N; dead |
| 1–2 | stock-entry-gate `a709c7e8` | combine-cash | 250000..253999, 4000 | | −0.214 / 0.155 | dead |
| 1–2 | flow-cover `3df87ccd` | combine-cash | 220000..223999, 4000 | | +0.002 / 0.003 | no effect |
| 1–2 | simplify (independent alternative) `bd69d748` | combine-cash | 224000..225499, 1500 | | −1.902 / 0.523 | dead as a whole (retail −4.8, arb +2.9) |
| 1–2 | remove-premium-cover `4eb683ab` | combine-cash | 200000..201999, 2000 | | −0.903 / 0.177 | the immediate-cover branch stays |
| 3 | retreat-crossing `b5158a96` | N | F, 3948 | s3 +0.45 / 0.18 | +0.108 / 0.043 | runner-up (4.1) |
| 3 | s3-flow-transfer `e7891178` | N | 410500..411999, 1500 | s3 +0.26 / 0.13 | | extension faded |
| 3 | 30 blind overlays (f-…) | N | 410000..410499, 500 | all ≤ 0 on target | | none gained |
| 4 | **RC** `3c07bdcd` | N | F, 4000 | s2 +1.080 / 0.145; s3 +1.093 / 0.123 | +0.537 / 0.048 | **promoted** |
| 4 | d-s1-retreat-crossing-port `bed6def9` | N | 430000..430499 | s1 +0.85 / 0.40 | | dead on extension (1500 seeds) |
| 4 | c-s1-queue-postjump `64209895` | N | 430000..430499 | s1 +0.50 / 0.26 | | dead on extension; the idea lives on as T's `postjump` |
| 4 | d-s3-mid-size-up `1317a49c` | N | 430500..431999, 1500 | s3 +0.32 / 0.14 | | ported to MA (below) |
| 4 | remove-s4-ask-risk-premium `324acde8` | N | 430500..431999, 1500 | s4 −0.68 / 0.28 | | the premium stays (T leaves `premium` off) |
| 4 | every own-fill pullback (7 items) | N | 430000..430499 | −5 to −36 | | harmful: never pull after an own fill |
| 4 | 26 blind overlays | N | 430000..430499 | all ≤ 0 | | none gained |
| 5 | 32 cancel variants and combines on RC; 11 blind overlays | RC | 440000..440499 | best d5-s4-cancel-port s4 +0.36 / 0.26 | | nothing positive; cancelled when the base moved to MA |
| 6 | d6-s2-retreat-posterior `58daa7d8` | MA | 450000..450999, 1000 (s2 n 270) | **s2 +1.958 / 0.382** (retail +2.20, arb −0.24) | +0.529 / 0.107 | best open screen; port to T (section 5) |
| 6 | p6-s3-retreat-strength `d79cf349` | MA | 450000..450999 (s3 n 252) | s3 +0.689 / 0.209 | +0.174 / 0.053 | port to T; overlaps `cut` |
| 6 | p6-s3-mid-size-up `d2daff28` | MA | 450000..450999 (s3 n 252) | s3 +0.217 / 0.089 | +0.055 / 0.023 | port to T |
| 6 | p6-s3-retreat-crossing `b4a16d6c` | MA | 450000..450999 (s3) | s3 +0.379 / 0.213 | +0.095 / 0.054 | same family as strength |
| 6 | c6-s4-cancel-norisk `e37648a8` | MA | 450000..450999 (s4 n 251) | s4 +0.546 / 0.414 | +0.137 / 0.104 | within noise |
| 6 | p6-s2-lowp-early-bids `a99aded5` | MA | 450000..450999 (s2) | s2 +0.123 / 0.091 | +0.033 / 0.025 | within noise |
| 6 | p6-s3-flow-transfer `cc046a2f` | MA | 450000..450999 (s3) | s3 +0.176 / 0.190 | +0.044 / 0.048 | within noise |
| 6 | 7 blind overlays (f6-…) | MA | 450000..450499 | all ≤ 0 | | 74 blind overlays over five rounds, none gained |
| 7 | P (MA on s1, B_RC on s2–4) `44f64ab1` | B_RC | audit only | | | compose-p: equal to MA on 44 spread-1 seeds and to B_RC on 156 others of 460000..460199, timing equal; its F measurement was cancelled when T superseded B_RC |

The round-6 merge for the five spread-1 ports and two spread-4 ports (r6-port/merge-01) was still waiting on one item when the goal finished and was not handed; r7-dev (13 screens on MA and B_RC) and r7-remove (6 deletions of the wrapper's parts) were in their canaries. Their results, when they land, are public at `https://api.imd.fun/artifacts/<result SHA-256>`.

## 5. What the next run should try

1. **Re-decide T's ON table on thousands of seeds.** T's keep decisions rest on 60 runs a spread. Four variants of T, each line 34 changed and nothing else, were prepared and smoke-tested at T's speed in the last episode (batch r8-t-ablate, 4 variants × 8 blocks of 500 on fresh seeds 940000..943999; refused only because a finishing episode may spawn nothing): V-cancel `90b340f87fe2db61623bb201f21460d38e9d07f2be9a8845b585be017cc1146a` with `cancel=(1,)`, V-cut (`92504562…`) with `cut=(2, 3)`, V-pjpr (`3df90643…`) with `postjump=(), premium=(4,)`, V-dead (`81302517…`) with `deadband=(1, 2, 4)`. One variant's per-spread d tests one entry per spread; an entry flips when the pooled d on its spread exceeds twice its standard error in the direction of the change, about 1,000 runs a spread. The likeliest flips from T's own halves: cancel on spread 1 (first half +1.85), deadband on spread 4 (second half +3.76), cut on spread 4 (+0.59 se 0.63).
2. **Port the round-6 winners onto T as new ON entries, scoped to their spread.** d6-s2-retreat-posterior first (+1.96 se 0.38 on spread 2, retail gain, the only candidate that gains retail rather than arbitrage), then p6-s3-retreat-strength (+0.69 se 0.21) and p6-s3-mid-size-up (+0.22 se 0.09; +0.32 se 0.14 on N over 1,500 seeds). Strength and `cut` are the same family (retreat-triggered belief reweight); test strength as a replacement for `cut` on spread 3 where `cut` was dropped, not on top of it. Planned as r8-t-port (5 items, 1,000 fresh seeds each from 950000) with the same refusal.
3. **Measure T against MA on all 4,000 finalist seeds first** (r8-t-f, 8 × 500). T's own holdout is 1,000 seeds at +1.23 se 0.35, but the write-up's partial check on 744 finalist seeds gave only +0.19 se 0.27 (section 3.2). If the full measurement does not clear twice its standard error, T's entries should be re-decided one by one (item 1) before anything is built on top of it; MA itself is +1.26 se 0.25 over N on the same seeds and remains the fallback base.
4. **Spread 1 is the weakest and the noisiest.** T's spread-1 gain over MA is +1.40 se 0.75; MA over N on spread 1 is +1.15 se 0.31 with single seeds at −98.5 and −93.9. Diagnostics on N: after a rival inward move or a both-quote shift the next-step move rate is 22–29% against 14–15% at rest, and same-side arbitrage loss after a one-tick retreat is 2.40 per run on spread 1 (untreated by `cancel`, which T leaves off there). Ideas prepared for r7-dev: bid cancel on rival ask-down, ask cancel on bid-up, and a both-shift pause, each spread-1 only.
5. **Keep the arbitrage lever in view.** An oracle that cancels orders about to be swept only on a ≥3-tick next move gains +3.2, +7.6, +9.0 and +17.1 per run on spreads 1 to 4 (all arbitrage), while cancelling every swept order loses 27–59: the value is in predicting the large move, not in withdrawing. One step after an own fill the sweep rate on that side is 0.77–0.85 against 0.36, yet every own-fill pullback tried lost 5 to 36 per run, because the fills that precede sweeps are also the profitable retail fills.
6. **Do not spend on blind overlays.** 74 blind single-mechanism overlays over five rounds gained nothing; every gain came from reading the rival's quote changes (retreat cancel, retreat posterior, retreat strength) or from porting a sibling goal's spread block.
7. **Respect the time limit.** Paradigm stops a submission near 270 s for 200 runs; B_RC took 215 s and passed, MA plus RC's wrapper failed twice at about 270 s, T passed. Report seconds per simulation next to T's on the same machine for every candidate and drop anything over about 15% slower.

## 6. Method and limits

- **Pairing.** Every comparison runs candidate and comparator on the same seed (`sample_config` and the engine's process and retail streams are seed-derived), reports d per seed, and pools blocks by sum and sum of squares. A single 200-run mean has a standard error near 12; paired differences over 500 seeds have standard errors of 0.05 to 0.5, which is why only paired differences rank candidates.
- **Seeds.** Tuning seeds never overlapped a holdout: tuning 310000..350149 by round, holdouts 410000..411999, 430000..431999, 440000..440499, 450000..460699, diagnostics 420000..421999, 500000..502499, 510000..510499; everything below 300000 was exposed by rounds 1–2. Seeds 900000..903999 were run only by finalist measure batches: RC (complete), retreat-crossing (3,948), MA against N (complete), the cancelled P and B_RC4 finals, and the write-up's T against combine-cash. Seeds 700000..709999 (goal 75dd8e1e) and 150000..150999, 170000..170999 (T's own) were never used here.
- **Limits to weigh.** The finalist seeds were reused across rounds and by several finalists, so the 2-se gate on them is weaker than on untouched seeds. Each round's screen shares one holdout across its items, so screen rankings are selected and inflated by about one standard error for the best of many. N, MA, B_RC and T were adopted from sibling goals on the requester's notes, not promoted through this gate; the gate promoted one change (RC), which those files then carried. Local paired gains are not a leaderboard result; the standings quoted are the requester's, not checked live. `--sandbox` was never run; the 270 s limit is known from the requester and worker timing only. The write-up's own run (3.1) was made under six-way CPU load, so its per-simulation seconds are not comparable with the serial timings quoted elsewhere.
- **Rounds.** Ten episodes, 480 of 600 items used by the plane's count, 35 batches. Rounds 1–2 (pilot and wide development on combine-cash, 100 items), round 3 (105 on N), round 4 (117 on N), round 5 (49 on RC, cancelled when the base moved), round 6 (29 on MA), round 7 (61: P and B_RC4 finals and 19 screens, cancelled or unread when T superseded B_RC), and the last episode's 45 requested items against T, refused because the goal was finishing. Each round split about 40% combine and deepen, 30% fresh mechanisms, 15% removals, 15% measurement; the fresh lane was closed after round 4's results and its width went to measurement.

## 7. Inputs this write-up rests on

Handed results, read as data:

| input | result | SHA-256 | used for |
|---|---|---|---|
| b21-cancel-f1..f8 | r5-final/cancel-f1..f8 | 643cfa86…, 4cd6273c…, 44691263…, dbdaec5e…, f4115794…, 3c834b42…, 66a0748c…, 39abfcd8… | RC over N on 900000..903999 (3.3, 4.1) |
| b28-merge-01, b28-merge-02 | r6-base-f/merge-01, merge-02 | f8ad8d6c…, bf253342… | MA over N on 900000..903999 (3.2) |
| b26-merge-02 | r6-port/merge-02 | d22ee626… | round-6 screens on MA (4.3, 5) |
| b29-compose-p | r7-compose/compose-p | 27916dc9… | P's equality audit and timing (4.3) |

Artifacts fetched and hash-checked during the write-up: T (`79af781a…`, code `9fba1eb5…`), combine-cash (`ecbc9087…`, code `baef955e…`), RC (`2d4b30bb…`, code `3c07bdcd…`), MA (`149883fe…`, code `5d1bd527…`), N (`db22aff7…`, code `bf0d179f…`). The orchestrator's notes in `goal.json` supply the figures of rounds 1–5 whose results were not handed to this step; each is public at `https://api.imd.fun/artifacts/<result SHA-256>` under the batch and key named. Wave 3's report: https://github.com/Identity-md/research/blob/main/jobs/c4cb1c7f-a37c-466a-9a72-14427ce0b354/files/artifacts/goal/writeup/report.md. Simulator: https://github.com/danrobinson/prediction-market-challenge at b244530ee2a6247b5f930830eeca9dd950da0e7e.
