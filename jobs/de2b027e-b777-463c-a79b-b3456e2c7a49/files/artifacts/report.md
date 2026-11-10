# What could explain the Simple AMM challenge’s 528 cluster?

Research date: 10 November 2026. Simulator fixed to `6b6921f8d463314aa7c96234e1be25a25245f704`. Edge is in units of Y per 10,000-step simulation, not basis points and not profit relative to the competing pool.

## 1. Verdict and strength of evidence

**The structural problem is partially observed, competitive market making with endogenous opportunities to update quotes.** The useful architecture is (i) infer fair price and the competing pool’s state, (ii) translate those beliefs into executable bid/ask quotes, and (iii) choose fees for the retail flow, arbitrage loss, and future observations those quotes induce. A larger fee predictor trained on the same imperfect state need not solve any of those missing decisions.

**That architecture is a hypothesis for the 528 cluster, not an identified description of the leaders.** The narrow 0.3-point cluster is consistent with convergent best-response designs and small parameter differences, but also with shared lineage or selection on a common evaluation set; the scores alone distinguish none of these. Neither the score cluster nor public repositories prove what those five entries do. In particular, there is no verified basis here for saying they share code, have perfect information, use a specific exploit, or have reached the theoretical maximum.

The supplied 528.1–528.4 cluster, 526.8/525 break, and T3 ≈523 are treated as the assignment’s leaderboard snapshot. Direct requests to the official [About page](https://www.paradigm.xyz/puzzles/amm/about) and leaderboard API returned HTTP 403 during this research. I could not independently refresh that snapshot or inspect the five leaders’ Solidity. The simulator, public strategy code, research papers, and a particular public T3 artifact were accessible.

A particularly important correction: **T3 already incorporates a censored-price approximation and rival-pool information.** I downloaded artifact `2333ecf2…5336`, verified its content hash, decompressed its Solidity, and verified code SHA-256 `cb6d945511e1e10af78baa64c2a6cb25806f0998403ce6440654bfc3c70092d9`. It has a 19-input, eight-unit, two-output learned head and jointly tuned base constants. Its own evaluation reports +0.819 edge over IB on 1,024 paired markets and no out-of-gas calls; those measurements were **not rerun here**. Its mean on that seed block is 526.705, which does not verify or contradict the supplied ≈523 board score. [T3 artifact](https://api.imd.fun/artifacts/2333ecf28d4356bd232b85c1e55842e94e1ada05e1cd067830b5625dfdbc5336), [IMD goal cc45e1a7](https://explorer.imd.fun/jobs/cc45e1a7-047f-45d9-a5df-0b65be9cc03c).

The quantitative conclusions are narrower than a claim to have reverse engineered first place:

- A five-point improvement needs only about **0.625 bp of additional net edge on 80,000 Y of captured flow**. A small systematic modeling error can explain the gap.
- A reproducible, explicitly simplified perfect-information benchmark gives approximately **651 edge**. It is a one-order reset-state optimum, **not a proven upper bound or an estimate precise enough to locate the actual legal optimum**.
- The exact simulator’s callback-constrained, perfect-state optimum remains uncomputed. An oracle that may change fees before arbitrage or before every retail order solves a different problem.

Throughout: **verified** means inspected source or checked arithmetic; **derived** means a consequence of the stated model; **hypothesis/estimate** means not experimentally established; **unverified** identifies missing evidence.

## 2. Exactly what the pinned simulator does

### Configuration and units

Both pools initialize with 100 X and 10,000 Y, initial fair price 100 Y/X, and constant product 1,000,000. Each simulation has 10,000 steps. Per simulation, the canonical Python match builder independently draws mean retail size `m ∈ [19,21]`, arrival rate `λ ∈ [0.6,1.0]`, and volatility `σ ∈ [0.000882,0.001008]`. Drift is zero, `dt=1`, buy probability is 1/2, and log-size standard deviation is 1.2. These draws remain fixed within a run. [Canonical configuration](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/amm_competition/competition/config.py).

For the CLI’s default match, simulation `i` uses NumPy `default_rng(i)` for those parameter draws, in size/rate/volatility order. Rust then uses PCG64 seeded by `i` for price and `i+1` for retail. The separate Rust `HyperparameterVariance.apply` implementation also exists, but uses a different parameter-draw generator; it must not silently replace the Python builder in a claimed seed-identical reproduction. [Match construction](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/amm_competition/competition/match.py), [Rust configuration](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/amm_sim_rs/src/types/config.rs).

### Step ordering — including when new fees take effect

For `t = 0,…,9999`, the executable engine does the following:

1. Move fair price: `p ← p exp(−σ²/2 + σZ)`.
2. Attempt **one** profit-maximizing arbitrage on the submission, then **one** on the normalizer. There is no iterative cross-pool arbitrage loop.
3. Draw the retail order list. Execute its orders sequentially, each split across both pools.
4. Capture end-of-step statistics.

Each successful pool trade changes reserves and immediately calls that pool’s `afterSwap`. Its returned fees apply to subsequent trades, including later retail orders in the same step. Updating fees after arbitrage does **not** trigger another arbitrage that step. A step with no own trade provides no callback. Initialization happens before the first price movement, not after seeing `p₀`’s first shock. [Engine](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/amm_sim_rs/src/simulation/engine.rs), [Trade execution](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/amm_sim_rs/src/amm/cfmm.rs).

Retail count is Poisson(λ). Each order’s Y-denominated size is `Q = exp(log m − 1.2²/2 + 1.2Z)`, followed by a separate random side draw. A retail buy spends Q Y; a retail sell supplies `Q/p` X. Price is fixed throughout that step. [Retail generator](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/amm_sim_rs/src/market/retail.rs), [Price process](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/amm_sim_rs/src/market/price_process.rs).

### Fee accounting and score

Use pretrade reserves `(x,y)`, `k=xy`, spot `s=y/x`, bid fee `b`, ask fee `a`, and `γ_b=1−b`, `γ_a=1−a`.

- AMM buys X: the trader supplies gross `u` X, receives `v=y−k/(x+γ_b u)` Y. Reserves become `(x+γ_b u,y−v)`; `b u` X is put in a separate fee bucket.
- AMM sells X: the trader receives `v` X and pays gross `u=[k/(x−v)−y]/γ_a` Y. Reserves become `(x−v,y+γ_a u)`; `a u` Y goes to its fee bucket.

Thus **fees do not compound liquidity**: k stays constant, apart from floating-point error. Edge for these trades is respectively `p u−v` and `u−p v`, using gross transfers. Fee income is already included; do not add it to edge again. Arbitrage contributes minus the arbitrageur’s profit. The reported objective is submission edge averaged across simulations, not submission-minus-normalizer edge. End-of-run marked PnL is a separate statistic. [CFMM implementation](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/amm_sim_rs/src/amm/cfmm.rs), [Scoring and PnL](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/amm_sim_rs/src/simulation/engine.rs).

### Arbitrage size on each pool

The source formulas are independently applied to each pool using its current reserves and fees:

| Condition | Trader action / `TradeInfo.isBuy` | Optimal size | Uncapped endpoint |
|---|---|---|---|
| `p > s/γ_a` | Buy X / false | X out `v*=x−√(k/(γ_a p))` | `s′=γ_a p`, hence `p=s′/γ_a` |
| `p < s γ_b` | Sell X / true | Gross X in `u*=[√(kγ_b/p)−x]/γ_b` | `s′=p/γ_b`, hence `p=s′γ_b` |
| `sγ_b ≤ p ≤ s/γ_a` | None | Zero | No observation |

For the buy-X case, the engine caps X out at `0.99x`; the endpoint equality can fail when that cap binds. There is no corresponding explicit gross-X cap on the sell-X branch. Both branches reject nonpositive quantities, quotes, and profits. The source first chooses a branch by `s<p` or `s>p`, then performs those checks. [Arbitrageur](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/amm_sim_rs/src/market/arbitrageur.rs).

**Derivation.** When buying X, the trader maximizes

`Π_a(v)=pv−[k/(x−v)−y]/γ_a`.

Setting `dΠ_a/dv=0` gives `p=k/[γ_a(x−v)²]`. When selling X, maximize

`Π_b(u)=y−k/(x+γ_bu)−pu`.

Its derivative gives `p=kγ_b/(x+γ_bu)²`. The respective uncapped maximum profits have useful exact forms:

`Π_a*=(√(px)−√(y/γ_a))²`,

`Π_b*=(√y−√(px/γ_b))²`.

These squared expressions apply only on their profitable branches, not throughout the no-arbitrage band. Near a band edge, loss is approximately `y e²/4`, with e the excess log mispricing beyond that edge and small fees; the ask expression has an additional `1/γ_a` factor. Squared error, not simply trade count, therefore matters for defensive quoting.

### Exact retail split

Let pool 1 be the submission and pool 2 the normalizer. For a buy with total gross Y input Q, use each ask-side γ and define

`r = √(x₁y₁γ₁ / (x₂y₂γ₂))`,

`z₁ = clip((r(y₂+γ₂Q)−y₁)/(γ₁+rγ₂), 0, Q)`, `z₂=Q−z₁`.

For a sell, total gross X is `U=Q/p`. Use bid-side γ and replace y by x in the allocation expression:

`u₁ = clip((r(x₂+γ₂U)−x₁)/(γ₁+rγ₂), 0, U)`, `u₂=U−u₁`.

The split is calculated **once before either leg executes**. Submission executes first, normalizer second. A leg executes only if its input is **strictly greater than 0.0001** in that input’s units; a skipped leg is not redistributed. The next order gets a new split with updated reserves and fees. [Router](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/amm_sim_rs/src/market/router.rs).

**Derivation and consequences.** For a buy, output is `F_i(z)=x_iγ_i z/(y_i+γ_i z)`. An interior optimum satisfies `F₁′(z₁)=F₂′(z₂)`; solving gives the expression above. Sell output has the same form with x and y interchanged. At an interior allocation the **fee-adjusted marginal prices** equalize; raw spots generally do not. Small orders can route completely to one pool, so a fee’s effect is state- and size-dependent. “One basis point lower wins all flow” and a constant 50/50 share are both incorrect generalizations.

## 3. What TradeInfo reveals, and what it cannot

The six fields are `isBuy`, `amountX`, `amountY`, `timestamp`, `reserveX`, `reserveY`. Amounts and reserves are WAD encoded; timestamp is the integer simulation step. `isBuy=true` means **the AMM bought X**, not the retail customer. Both amounts describe gross trader transfers; reserves exclude accumulated fees. There is no trader identity, arb label, fair price, rival state, retail order count, seed, or future-order information. [Solidity interface](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/contracts/src/IAMMStrategy.sol), [ABI encoding](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/amm_sim_rs/src/types/trade_info.rs).

The distinction between one record and record-plus-persistent-history is essential:

| Observable or inference | Exactly what is justified |
|---|---|
| Current own state | Posttrade reserves, spot, product, gross execution price `amountY/amountX`, trade direction and size. |
| Previous state, given remembered applied fee | If true: `x_pre=x_post−γ_b amountX`, `y_pre=y_post+amountY`. If false: `x_pre=x_post+amountX`, `y_pre=y_post−γ_a amountY`. This also recovers price impact and the fee bucket increment. |
| Applied fee from history | Remember the last successfully returned, clamped fees. A lone record does not generally identify both pretrade reserves and the fee. A known initial k or remembered pretrade reserves can supply additional equations. |
| First own print in a timestamp | Can be arb **or retail**. Arb, if present, is first; first does not imply arb. Initialization must distinguish “no print yet” from a print at timestamp 0. |
| Later own prints at that timestamp | Definitely retail in this engine. Fair price has not moved between those prints. Lowering fees then cannot provoke an additional same-step arb, but those fees may survive into the next step. |
| Fair price conditional on arb | Exactly the endpoint identities in §2, up to encoding/floating precision, unless the cap binds. The fee to use is the **old fee**, not the new callback return. Applying this inversion to retail gives a pseudo-observation, not an oracle. |
| Missing callbacks | A gap reveals that no successful own trade occurred at the intervening steps. With fixed reserves/fees and normal successful execution, each missing arb attempt implies `sγ_b≤p_j≤s/γ_a`. It also implies retail never allocated an executable leg to us. This is censored path information, not a complete price history. |
| First print known to be retail | No own arb occurred at that step’s start, so the **pretrade** spot and old fees constrain fair price to the no-arb band. Using the post-retail spot for that constraint is wrong. |
| Other pool conditional on interior retail routing | For own posttrade spot `s₁′`, rival posttrade spot is `s₂′=s₁′γ₂/γ₁` on retail buys, and `s₂′=s₁′γ₁/γ₂` on retail sells. Since rival k is known, reconstruct its endpoint reserves as `√(k₂/s₂′), √(k₂s₂′)`. These refer to its planned completed leg; during our callback its leg has not executed yet. |
| Whether the retail route was interior | **Not generally identifiable from our leg alone.** We do not see total order size or the other leg. A high own fee does not prove the rival received a positive leg: our spot may be sufficiently better. Use a mixture over interior and boundary routes. |
| Flow, size, volatility, and arb probability | Statistically estimable with a model of selection and timestamps; not exact state readouts. Own trade counts combine arb and routed retail, while completely diverted orders are invisible. |

The rival endpoint identity is an algebraic consequence of `γ₁/s₁′=γ₂/s₂′` for buys or `γ₁s₁′=γ₂s₂′` for sells. Inferring its **current fair price** from that endpoint requires another assumption; the rival’s post-retail spot can be displaced from fair price.

These are the economically relevant information channels, not a claim that every statistic of an arbitrary trade history has been enumerated. Multiple latent histories can produce the same record. No policy fed only these records can deterministically reconstruct the hidden RNG state, future GBM shocks, all competitor-only orders, or the exact current p on every callback.

## 4. Why coefficient tuning and learned corrections can stall

### The established public family

[YQ’s pinned Solidity](https://github.com/jiayaoqijia/amm-challenge-yq/blob/3e9dc7d5a6192c88b562a0f8d9c172ca566ec94d/contracts/src/Strategy.sol) uses 11 slots: prior fees/time, direction, activity, fair-price estimate, volatility, arrival/size estimates, toxicity, and within-step count. It blends band-inverted prices with weights 0.26 on first prints and 0.05 later, adds flow/activity/toxicity widening, then applies asymmetric stale-price protection. Its [README](https://github.com/jiayaoqijia/amm-challenge-yq/blob/3e9dc7d5a6192c88b562a0f8d9c172ca566ec94d/README.md) claims 523.21 on the official board; that is the author’s claim, not a score reproduced here.

[ChengHua926’s pinned strategy](https://github.com/ChengHua926/amm-challenge/blob/d34a5199c59a4c44d5336a25f1436b4ae1f21104/contracts/src/Strategy.sol) visibly retains that estimator/mapping structure with changed coefficients, update speeds, and tail treatment. [Dipankar’s SigmaAdaptive code](https://github.com/dipankar/amm-challenge/blob/c588ae6c47fc9af2063c9bb1f2efbeb0dd276dab/contracts/src/SigmaAdaptiveStrategy.sol) is another public adaptive implementation; its [README](https://github.com/dipankar/amm-challenge/blob/c588ae6c47fc9af2063c9bb1f2efbeb0dd276dab/README.md) claims 526.54 on 500 local simulations. Neither local claim establishes a 528 board mechanism, and neither is an independent oracle ceiling.

T3 goes beyond those basic EWMAs: it has a seven-node soft-band approximation, an arb/retail mixture, slow and fast price estimates, flow state, a per-run toxicity anchor, and the learned head. However, its inspected `_posterior` uses heuristic likelihoods and fixed variance increments; its later-retail normalizer observation is gated by `fee > 30 bps`, which does not prove interior routing. Its head adjusts fees produced by the inherited mapping. Its CMA-ES fitness already uses full-market edge, so it would be incorrect to describe T3 as optimizing only immediate revenue. A continuation-value approach changes representation and training efficiency, not the underlying scoring objective. These are concrete residual model restrictions; **their causal contribution to a five-point deficit is unmeasured**. [Hash-verified T3 source and recorded results](https://api.imd.fun/artifacts/2333ecf28d4356bd232b85c1e55842e94e1ada05e1cd067830b5625dfdbc5336).

### Structural failure modes — deductions, not leader attribution

1. **A biased pseudo-oracle cannot be repaired solely by a better fee fit.** On retail, the band-inverted endpoint is displaced by our own flow. Blending it as a noisy arb endpoint creates feedback: chosen fees affect the observation subsequently used to justify those fees.
2. **Observation selection depends on the policy.** A larger fee can hide retail orders and also suppress price-revealing arb. Own count/elapsed estimates are not the exogenous λ. Training can compensate within a familiar state distribution and still fail after a policy change.
3. **A point estimate loses asymmetric tail risk.** Expected arb loss is quadratic in excess mispricing. Two beliefs with the same mean and different variance generally require different protection. T3 addresses this approximately, so simply adding a variance feature is not sufficient novelty.
4. **Fees persist across an unknown boundary.** Later prints are retail, but the next event can be another same-step retail order or tomorrow’s arb. There is no callback at the end of retail. An aggressive “retail fee” can become an exposed opening quote.
5. **The competitor’s outside option matters.** Identical own spot, estimated p, and σ can warrant different fees if the normalizer is at a different spot. Rival reconstruction must accommodate hidden orders and boundary routing.
6. **Immediate edge and continuation value differ.** A retail fill earns spread/impact now, moves inventory, changes the next arb’s opportunity, and changes when information next arrives. Neither minimizing arb volume alone nor maximizing current retail edge alone is the objective.
7. **Local score noise and implementation limits can masquerade as a plateau.** Use paired seeds, separate simulations against Vanilla, and failure counters. A reverted/OOG `afterSwap` leaves old fees in effect in the pinned CFMM; it is not automatically a failed overall simulation. A score without failure instrumentation can conceal stale quotes.

Algebra’s first-person write-up provides independent qualitative support: it describes environment/rival estimation, asymmetric fees, and probabilistic use of first-trade ordering, rather than a disclosed leading formula. It also reports an earlier seed leak and leaderboard recomputation. That history makes seed memorization an unsupported explanation for today’s cluster. [Algebra, 27 March 2026](https://www.linkedin.com/pulse/amm-fee-challenge-notes-from-our-run-optimization-arena-qe3ff).

## 5. Perfect information: derivation, numerical estimate, and limits

### Three different oracle questions

- **Perfect current state, legal callbacks:** p and rival reserves are revealed only when the existing strategy is called. No new pre-arb or pre-retail hook; no future randomness. This is the most relevant upper-information benchmark for a legal strategy.
- **Event oracle:** may reprice before each event and knows its side/size. This removes execution latency as well as information uncertainty.
- **Clairvoyant path oracle:** knows the full future and can optimize its initial and subsequent callback actions against that path. This is a different, larger-information optimization again.

For a fixed action space and callback schedule, adding information cannot lower the optimum. But changing both information and market dynamics, such as resetting reserves between orders, does not produce a theorem ordering the resulting scores.

### The exact optimization that would settle the question

At a callback let full state include `(t, phase, x₁,y₁,x₂,y₂,p,σ,λ,m,processed-retail-count)`. A legal full-state oracle chooses a fee pair `f∈[0,0.1]²`, and the simulator advances **until the next own callback or termination**, including arbitrage and competitor-only activity. If R is our cumulative edge over that interval, its Bellman equation is

`V(S)=max_f E[R(S,f,ω)+V(S_next)]`, with `V(terminal)=0`.

The observation-limited problem replaces S with a posterior over hidden states. A full-future oracle instead conditions on the future path. **No source inspected supplies a certified solution of this Bellman problem. I did not solve it numerically here.** Therefore neither “528 is the ceiling” nor a precise actual-oracle maximum is established by this report.

A public oracle script even calls a heuristic an “absolute upper bound,” but its `_optimal_side_fee` uses an approximate share proportional to `√(kγ)` rather than the actual clipped router allocation. Its harness introduces `before_arb`/`before_retail` hooks and explicitly uses different RNG seeding. It is a useful experiment scaffold, not a proof of an optimum. [Public oracle policies](https://github.com/ChengHua926/amm-challenge/blob/d34a5199c59a4c44d5336a25f1436b4ae1f21104/scratch/oracles.py), [Public oracle harness](https://github.com/ChengHua926/amm-challenge/blob/d34a5199c59a4c44d5336a25f1436b4ae1f21104/scratch/py_oracle_sim.py).

### A tractable numerical perfect-information benchmark: about 651

To provide a number with an auditable derivation, consider **one retail order**, resetting both pools to fair-centered reserves before each order. Normalize fair price to 1 and both reserve coordinates to `D=10,000` monetary units. Competitor fee is `f₀=0.003`. The oracle knows Q and side before quoting; it chooses f, with no subsequent arb debit or carryover state.

Let `g=1−f`, `g₀=1−f₀`, `r=√(g/g₀)`. The exact buy allocation and immediate edge are

`z(f,Q)=clip([r(D+g₀Q)−D]/[g+rg₀],0,Q)`,

`E(f,Q)=z−Dgz/(D+gz)`.

Sell is symmetric in these monetary coordinates. The numerical target is

`B = 10,000 E[λ] E_m E_Q[max_{0≤f≤0.1} E(f,Q)]`.

For intuition, expand to second order in Q/D and small fees:

`z ≈ Q/2 + D(f₀−f)/4`, `E ≈ fz + z²/D`.

For an interior split, differentiation gives `f*≈f₀/3+2Q/(3D)`, `z*≈Q/3+Df₀/6`. Thus

`E*(Q)≈(Q+Df₀/2)²/(3D)` for `Q>Df₀/4=7.5`.

For smaller Q, the all-flow boundary gives `f*≈f₀−2Q/D` and `E*≈f₀Q−Q²/D`.

Here `E[Q²]=m²exp(1.44)`; at m=20 this is about 1,688.28, so large retail orders materially affect the result. Integrating the **exact** expressions over the lognormal distribution gives:

| Mean order size m | Exact edge for 8,000 reset orders | Second-order approximation |
|---|---:|---:|
| 19 | 599.674 | 610.042 |
| 20 | 650.424 | 662.411 |
| 21 | 703.229 | 716.992 |

Simpson integration over uniformly distributed m using these three points gives **650.77**, rounded to **about 651**. This last integration is an approximation; the per-size integrations use 2,000 normal-coordinate intervals, with a 1,000-interval cross-check. At fixed m=20, varying λ from 0.6 to 1.0 scales the number from 487.8 to 813.0. These are parameter sensitivities, not confidence intervals for the actual challenge optimum.

**Interpretation:** 651 is a calculated *reset-state, order-clairvoyant benchmark*. It demonstrates the scale of extractable spread plus impact under its assumptions. It is not “the challenge’s theoretical maximum,” and 651−528 is not a proven exploitable gap. Resetting own inventory removes intertemporal costs; resetting the competitor also changes the opportunity set and can remove favorable competitive dislocations. The event oracle knows Q before the fee is set, which a legal policy does not.

### What can be bounded without those assumptions?

A rigorous but loose pathwise bound is available. For a retail buy, own edge `z−pX_out ≤ z ≤ Q`. For a sell, own edge `pX_in−Y_out ≤ pX_in ≤ Q`, because own input is at most Q/p. Arbitrage adds nonpositive edge. Hence

`edge ≤ Σ_retail Q`, and `E[edge] ≤ 10,000 E[λm] = 160,000`.

This also covers a clairvoyant strategy and respects the actual callbacks; it is far too loose to distinguish 525 from 528. There is no finite deterministic bound uniform over all possible runs because the lognormal sizes have unbounded support; the expectation bound remains finite.

An additional scale check: for a causal strategy at zero drift, the expected stochastic inventory holding gain vanishes. Summing cash flows gives expected edge = expected change in marked reserve value + expected fees valued when collected. For a continuously fair-centered zero-fee pool, marked reserve value is `2√(kp)`, and Itô’s formula gives a local decay scale `yσ²/4` per step, approximately **22.36 Y per run** at initial depth averaged over the σ range. This is a scale estimate, not the arbitrage loss of a particular strategy and not a valid deduction that one can just add 22.36 to its score. Finite fees, inventory displacement, and terminal residual value matter.

**Plain answer about the maximum:** the defensible computed oracle reference is about 651 under the specified simplified model; the true legal perfect-state maximum is unanswered. A tight numerical estimate requires solving or bounding the callback Bellman problem, with held-out exact-engine evaluation of candidate oracle policies. It would be misleading to present either the board cluster or a heuristic oracle run as that solution.

## 6. Ranked mechanisms, expected gain, derivation, and implementation cost

These are **research priorities relative to a strong T3-like policy**, not measured improvements, predictions of leaderboard scores, or claims that public authors never tried them. The positive gain ranges below are subjective engineering expectations **conditional on the specified residual error being present and correctable**. Every candidate can lose edge, and the gains overlap substantially; do not sum them. No experiment in this assignment estimates their unconditional expected gain.

Useful common scales, derived from the canonical configuration:

`total retail notional ≈ 10,000×0.8×20 = 160,000 Y`.

At half-flow capture, `1 bp × 80,000 = 8 edge`. Around a 10,000-Y reserve, `10,000 arb opportunities × (10,000/4) × (1 bp)² = 0.25 edge`. Replace the opportunity count and reserve with measured values before relying on either sensitivity.

| Rank | Mechanism and conditional expected gain | Gain derivation / reason for ranking | Storage and total runtime gas design budget |
|---|---|---|---|
| 1 | **Distill the callback-to-callback edge value, including continuation**, about +1 to +4 | Recovering only 0.125–0.5 bp of effective net margin on 80k Y yields 1–4. It changes value representation and credit assignment rather than merely enlarging an inherited fee-correction head. Use exact routed fills and next-callback transitions; immediate fee revenue or one-step arb proxies are inadequate. | 8–12 slots; 100k–210k gas. Offline value/fee distillation; nine bounded online candidates evaluated with a small polynomial, not an online Monte Carlo search. |
| 2 | **Joint p/rival-state filter with interior/boundary route likelihoods**, about +0.5 to +2 | An illustrative reduction of excess mispricing RMS from 3 bp to 2 bp across 10k arb opportunities saves `0.25(3²−2²)=1.25`; small routing improvements can add tenths. Unlike simply adding a filter, this fixes selection and rival-observation assumptions remaining in inspected T3. | 12–20 slots; 130k–230k gas. Two compact mixture components and bounded quadrature; no stored history. Compress the head to make room. |
| 3 | **Phase- and survival-aware quote persistence**, about +0.3 to +1.5 | Correcting a 0.1 error in next-event mixing on a 20k-Y subset with a 3-bp action-margin difference is 0.6 edge. This explicitly prices whether a quote survives into a future arb attempt, conditional on unseen competitor-only flow. | 8–12 slots; 80k–160k gas. Small tabulated Poisson tail ratios and bounded elapsed propagation. |
| 4 | **Router-censored estimation of λ and order-size tail**, about +0.2 to +1 | A corrected net action margin of just 0.025–0.125 bp on captured flow gives 0.2–1. Lognormal `E[Q²]=m²e^1.44`, not `(E[Q])²`, drives routing/impact; own mean leg size estimates neither moment without selection correction. | 10–16 slots; 100k–190k gas. Accumulate likelihood scores for rate, mean, tail exposure; keep size sigma fixed unless evidence warrants estimating it. |
| 5 | **Exact multiplicative recentering of executable bid and ask**, about +0.1 to +0.6 | Given target quotes `B=p̂(1−h_b)`, `A=p̂(1+h_a)`, implement `b=clip(1−B/s)` and `a=clip(1−s/A)`. Additive fee-skew approximations omit cross terms of size mispricing×spread: 20 bp×30 bp = 0.06 bp, worth 0.48 edge at 80k Y if consistently harmful. Floors can dominate; this is not a guaranteed saving. | 4–8 slots; 55k–110k gas. A handful of WAD multiply/divides, learned widths, explicit zero/10% clipping. |
| 6 | **Explicit value-of-information quoting**, about 0 to +0.5 | Example: 5,000 later defensive decisions each improved by 2 bp² of excess-error variance are worth `5,000×2,500×2×10⁻⁸=0.25`, before probing losses and opportunity costs. A small price-revealing arb can be worth allowing; blocking every arb is not necessarily best. This needs a credible joint filter first. | 12–20 slots; 140k–235k gas. Add a bounded posterior-entropy/variance continuation term to an already compressed policy. |
| 7 | **Gas-aware distillation and failure removal**, 0 to +0.3 in ordinary operation; larger only if failures are frequent | Gain is `failure_count × incremental stale-quote loss`, which must be measured. Ten prevented failures costing 0.02 each give 0.2. Gas savings alone earn zero edge, but permit a better state/decision model. | Target 8–12 slots and <180k gas; ≤8 nonzero slots at initialization. Replaces, rather than appends to, T3’s head/filter. |

**Why not put more generic network training first?** In the same reset model as §5, withholding advance order size and optimizing a single fixed fee gives about **575.14**, at **25.35 bp**, versus 650.42 with advance size information at m=20. The difference is an explicit example of information the legal controller cannot obtain just by fitting a larger function. It is not a forecast that the true legal optimum is 575. Learning is still useful as the implementation of a better sufficient state and continuation objective.

### Cost assumptions and hard constraints

All gas ranges above are **uncompiled design estimates for complete replacement policies**, not incremental costs on top of T3 and not claims of passing validation. Use only `slots[0..31]`; arithmetic and bounded small-array loops are plain Solidity, with no assembly or external calls. Model coefficients should be constants in code, not hundreds of storage words. A large lookup table also risks the EVM deployed-code size limit. [Base contract](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/contracts/src/AMMStrategyBase.sol), [Validator](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/amm_competition/evm/validator.py), [EIP-170](https://eips.ethereum.org/EIPS/eip-170).

A rough transaction budget starts near 21k, with a cold zero-to-nonzero write about 22.1k, and a cold nonzero update about 5k under the relevant access-cost rules. Eight new nonzero slots already cost about 176.8k before call overhead/math; ten nearly exhaust 250k. Runtime accesses can be cheaper, but initializing every planned state variable eagerly is unsafe. Initialize a few priors, leave unused fields zero, and initialize other components lazily on distinct callbacks; check that no one callback initializes too many fields. [EIP-2929](https://eips.ethereum.org/EIPS/eip-2929), [EIP-2200](https://eips.ethereum.org/EIPS/eip-2200).

The actual wrapper gives **250,000 gas to both initialization and each swap callback**. T3’s artifact reports 243,234 at initialization and 235,575 peak afterSwap; appending a new nonzero storage initialization is therefore not a plausible implementation plan. All proposed designs need compiler/runtime measurements, including first-use writes, extreme elapsed gaps, and tail trades. [EVM wrapper](https://github.com/benedictbrady/amm-challenge/blob/6b6921f8d463314aa7c96234e1be25a25245f704/amm_sim_rs/src/evm/strategy.rs), [T3 recorded gas](https://api.imd.fun/artifacts/2333ecf28d4356bd232b85c1e55842e94e1ada05e1cd067830b5625dfdbc5336).

## 7. Pseudocode for the top three

These are implementable algorithm sketches, not submitted or gas-validated contracts. Every online input below must come from TradeInfo, initialization, or persistent beliefs. True prices, rival reserves, and future orders may be used only as offline training labels/simulator state.

### 1 — Distilled callback continuation value

```text
OFFLINE:
  Generate randomized exact-engine markets, preserving real callback timing.
  At own callbacks, save observable history state and a candidate belief summary.
  For each bounded candidate fee pair:
    advance from this callback UNTIL next own callback or termination
    collect all own edge R in that interval, including next-step arb
    preserve competitor-only orders and all steps with no own callback
  Fit Qvalue(belief, fees, time) <- E[R + max_f Qvalue(next_belief, f)]
  Validate against full-rollout edge; distill to a small fixed-point polynomial.
  Freeze coefficients; test fees and whole-market gains on fresh exact seeds.

ONLINE afterSwap(trade):
  oldFees = storedFees
  preState = invert_trade(trade, oldFees)
  belief = update_compact_belief(belief, preState, trade, oldFees)
  candidates = nine bounded pairs around a distilled fair/rival quote center
  best = argmax over candidates of distilled_Qvalue(belief, pair, timeRemaining)
  store sufficient statistics and best; return best
```

The interval stopping rule is essential. Training transitions that assume a free update next step systematically misprice protection. Offline distillation incurs no runtime simulation or network dependency.

### 2 — Joint censored-price and rival-state inference

```text
STATE:
  two weighted compact components for (log fair price, log rival spot)
  each stores mean, variance, covariance; old own spot/fees/time; print count

ONLINE afterSwap(trade):
  pre = invert_trade(trade, oldFees)
  first = no prior print at trade.timestamp
  gap = timestamps elapsed

  predict beliefs through elapsed GBM steps
  for fully silent steps:
    condition on own no-arb band AND no executable own retail leg
    approximate repeated killed-transition propagation with a bounded operator

  if first:
    arb branch:
      likelihood from endpoint inversion, observed direction and optimal size
      include no-arb-in-other-direction and 99%-cap case
      remember that rival's step arb is still AFTER our arb callback
    retail branch:
      constrain fair price by pre.spot and OLD own fees (no own arb)
      predict rival's completed step arb before this retail order
  else:
    retail branch only; fair price unchanged within this timestamp

  for each bounded quadrature state in retail branch:
    interior hypothesis:
      invert router allocation to infer total Q from our observed leg
      weight by lognormal density(Q) times the change-of-variable Jacobian
      reject impossible Q, wrong allocation, or a sub-threshold rival leg
      propagate rival to its planned post-leg endpoint
    boundary hypothesis:
      allow total Q equal to our leg with the rival at a routing boundary
      include threshold-skipped-leg mass; do not force marginal equality

  combine branch weights; moment-match to two components
  emit p mean/variance, rival mean/variance, arb probability to quote policy
  lazily persist compact state; no loops over trade history
```

For example, on a buy the interior inverse is

`Q = [z(γ₁+rγ₂)+y₁−r y₂]/(rγ₂)`.

The sell inverse uses pretrade x coordinates, then converts total X to Y with the candidate p. Interior endpoint reconstruction can be excellent information; treating all high-fee retail legs as interior can manufacture false certainty.

### 3 — Phase and continuation survival

```text
OFFLINE:
  Tabulate P(N>j | N>=j, lambda) for a small lambda/j grid.
  Fit hidden-order corrections from exact routing, including competitor-only orders.
  Distill two compact action values: later-retail and next-price/arb continuation.

ONLINE afterSwap(trade):
  update within-step own-print count and a belief over processed global retail count
  if later own print: arbProbabilityForThisPrint = 0
  else: use calibrated arb/retail mixture, never a hard first=arb label

  w = expected probability of further same-step executable own retail
      integrating Poisson remaining-count tails and router capture probability
  for each of a small fixed set of candidate fee pairs:
    score = w * laterRetailValue(belief, pair)
          + (1-w) * nextStepContinuationValue(belief, pair)
  return argmax score; store actual returned fees and sufficient state
```

If all retail orders were visible and j had already occurred, the Poisson continuation probability would be

`P(N>j | N≥j) = 1 − P(N=j)/P(N≥j)`.

At λ=0.8, after the first retail order it is about 0.347, not 0.8. Own print count is not global retail count, so the online algorithm must integrate hidden orders; the simple ratio alone is not the finished policy. In particular, a later retail callback does not authorize a timed fee reset before tomorrow’s arb.

## 8. What the two papers support — and do not

Baggiani, Herdegen, and Sánchez-Betancourt’s **Optimal Dynamic Fees in Automated Market Makers**, arXiv:2506.02869 (version 3, July 2026), studies dynamic fee control and finds regimes that deter arbitrage or encourage noise flow. Near-linear inventory/external-price rules can approximate their optimal policies. It supports searching for compact, interpretable control laws. Its finite inventory grid, controlled order intensities, fee conventions, and allowance for negative fees differ from this simulator; its optimum is not the challenge’s ceiling. [Paper, especially §§2–5](https://arxiv.org/html/2506.02869v3).

Their **Competition between DEXs through Dynamic Fees**, arXiv:2603.09669 (version 1, March 2026), extends control to interacting pools. The relevant switching reference combines the oracle and competitors’ exchange rates, supporting the rival-state component of the proposed architecture. Its Brownian reference-price model and exponential, quote-dependent arrival intensities differ from the pinned GBM, Poisson batches, and exact split router. Moreover, our competitor has fixed fees: this is best response to a fixed strategy, not a symmetric Nash-equilibrium problem. The paper supplies a structural analogy, not a formula that can be copied to guarantee 528. [Paper, especially §§2–4](https://arxiv.org/html/2603.09669v1).

## 9. Verification, unanswered questions, and a decisive experiment

**Completed locally:** read the pinned Rust engine, arb, router, CFMM, market generators, ABI, EVM wrapper, Python match/configuration, and public strategy sources described above. Checked T3 artifact and decoded-code hashes. Independently checked 3,000 randomized formula cases covering both arb endpoints/profits, pretrade reconstruction, and interior routing derivatives. Largest relative residual was below `9×10⁻¹⁶`. Numerically integrated the reset oracle, cross-checked quadrature resolution, and checked its scalar fee optimizer against a 10,001-point grid across 81 order sizes. Source-code inspection plus these checks is evidence for the mechanics and arithmetic, not independent certification of the economic hypotheses.

The offline calculator and recorded output are delivered as `analysis/check_math.py` and `analysis/math_results.json`; `analysis/source_manifest.json` records hashes and immutable URLs for inspected code. They use only the Python standard library. They deliberately do not pretend to reproduce Rust RNG or execute Solidity.

**Not verified:** current official leaderboard; leader source or common lineage; T3’s supplied board score/current-best status; any causal explanation for the top-five cluster; actual candidate gains; compiled gas of the proposed mechanisms; full exact-engine reproductions of the public score claims; a tight theoretical maximum. No 1,000-market strategy benchmark or Solidity gas validation was run in this assignment.

The most useful next experiment would distinguish **information limitation** from **decision limitation**, on identical held-out market paths:

1. Original T3, with callback failures counted.
2. Same fee decision mapping, replacing its price/rival beliefs with truth **only at the same existing callbacks**; separately reveal just p, just rival state, then both.
3. Same observable beliefs, replacing the inherited mapping/head with a distilled continuation policy.
4. Full-state continuation policy, still with legal callbacks.
5. A separately labeled event oracle with extra hooks, to measure the cost of the callback restriction itself.

Each policy runs alone against Vanilla on shared market seeds. Report paired differences and their standard errors, retail and arb **edge** separately, volumes, callback counts, failures, and peak gas. Volume deltas cannot substitute for edge decomposition. Hold out parameter/seed blocks from training; an absolute local score is not a board calibration.

If revealing truth adds little but a better continuation policy adds several points, the plateau is mainly decision design. If truth adds several points with the old map, it is mainly inference. If only extra hooks help, it is principally the information/update constraint. Until those comparisons or leader code are available, **“belief-based competitive continuation control” is a well-motivated research direction, not a proven explanation of the 528 cluster**.
