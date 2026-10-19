# Hamster Hour v2: design, security and token economics review

**Review date: 19 October 2026. Decision: revise the design before building; launch the game before activating loss mining.** The pari-mutuel game can remain solvent if liabilities are segregated, but the proposed token incentives make manufactured losses cheap. An address limit does not limit a player. Neither vesting nor an NFT bonus fixes that problem.

This is a design review, not a bytecode audit or a certification of v1. **[Brief]** denotes facts supplied by the requester, **[Observed]** public evidence read during this review, **[Derived]** arithmetic or a consequence of specified behavior, **[Recommendation]** a proposed change, and **[Unknown]** information still needed. Severity measures economic impact and launch relevance, not an assertion that unbuilt code contains a bug.

## 1. Evidence and limits

- **[Brief]** v1 addresses are HamsterHour `0xc5217f129da200a8e86229de4eabf3686eef64b1` and OracleVerifier `0xdcd7a7dee31d589f9df8113780050c18e7ea1f7d`; no users and redeployment planned. **[Observed]** the public [IMD project record](https://explorer.imd.fun/jobs/51bec67e-efec-4e88-bb68-297892343ce0) lists those addresses and a source repository. This does not independently establish present balances, users or deployed-bytecode equivalence.
- **[Observed]** [hamsterhour.fun](https://hamsterhour.fun) was accessible by HTTP, although the browser research tool could not render it. Its served JavaScript at [index-BcGdBZPn.js](https://hamsterhour.fun/assets/index-BcGdBZPn.js) embeds the above addresses, source `https://sepolia.squeekchain.com`, and an old genesis constant `1791847800`. **[Recommendation]** remove that 600-second offset everywhere in v2, including frontend projections and oracle questions. The brief's `1791847200` is **2026-10-12 23:20:00 UTC**, not a whole UTC hour. Define window alignment explicitly rather than silently rounding to the hour.
- **[Brief, not independently replicated]** 162-hour telemetry: 77% zero-work hours; activity mostly 21:00–06:00 UTC; active-hour p10/median/p90 ≈1090/2100/3060 and observed max 3194. Direct access to the Squeekchain site returned HTTP 403; no raw 162-hour series or documented API schema was supplied. The quantiles cannot determine a probability density, serial dependence, the frequency of work 1–99, or a robust maximum. All probability estimates below are labeled models, not measured hit rates.
- **[Observed]** [IMD documentation](https://imd.fun/docs/#the-attestation) specifies version-2 EIP-712 oracle attestations with typed answers, question hashes, timing and panel agreement fields. Its [public capabilities endpoint](https://api.imd.fun/requests/capabilities), fetched on the review date and saved in `research/imd-capabilities-2026-10-19.json`, quoted `oracle.request` at **0.5 IMD**, minimum panel size 5. No paid request or production settlement was performed. Price and delivery latency can change.
- **[Observed]** the [v1 oracle integration document](https://github.com/identity-md-launches/launch-1951-workflow-contract-stage-context/blob/main/docs/ORACLE.md) describes caller-scoped verification and rejecting attestations issued before the window end. It is a useful compatibility reference, not proof that v2 works. No chain-state validation or complete v1 source audit was performed.

The previous attempt's reported failure was an upload HTTP 502, not a substantive review finding. Its files were unavailable; this report was produced anew. Research, calculations and local checks here are author checks with no independent assurance.

## 2. Findings ranked by severity

| ID | Severity | Finding | Required response |
|---|---|---|---|
| E1 | Critical economic, if mining activates | Opposing Sybil bets manufacture rewarded losses for 2–18% of nominal losses in modeled cases; potentially less with other rebates | Do not activate the proposed mining schedule; publish and test a bounded alternative |
| O1 | Critical trust exposure | A valid but false oracle answer can redirect all window pools and the available jackpot; timeout only handles absence | Specify source finality, signer trust, complete data, and exposure limits |
| J1 | High | A shared rolling jackpot has no defined chronology for concurrent/unsettled windows; caller-selected order can redirect value | Serialize jackpot finalization and snapshot liabilities |
| L1 | High | “Last 12 settled awake windows, ordered by index” still depends on selective settlement and creation timing | Deterministic historical cutoff and finalized-prefix rule |
| M1 | High | `lossOf` alone cannot assign deterministic retroactive halvings; ambiguous loss definitions allow double rewards | Freeze entitlement data and cumulative loss intervals at chronological finalization |
| S1 | High | Settlement-time staking and immediately staked vesting rewards enable fee capture and accounting dilution | Define time-based eligibility, vesting custody and one-shot staking adapter |
| T1 | High | Revised 750M base allocation cannot fund the original 800M asymptotic schedule; hook economics may conflict with launch policy | Reconcile supply and obtain a concrete launch quote before token build |
| B1 | High | Current `ownerOf` plus per-window uniqueness does not establish historical ownership; retroactive claims and short rentals drain boosts | Pre-window registration/escrow and immutable per-NFT usage/caps |
| R1 | Medium–high liveness | 1% oracle funding fails at low volume and reimbursement can be front-run or drained | Prefund operations and bind one bounded payment per useful settlement |
| P1 | Medium | Predictable sleep hours, one-sided refunds, fuzzy SLEEP meaning and 9% take impair pricing/retention | Clear market definitions, pre-start close, live payout information |
| H1 | Medium–high token launch | 98% anti-snipe tax, optional-pool bypass and unfunded perpetual drip assumptions | Remove launch tax; audit any retained hook in every swap mode |

### E1 — Manufactured losses and reflexive staking

**[Derived]** Let binary fees be `f=0.09`, losing-side stake `L`, winning-side stake `W`, and assume the attacker owns every bet in that market. Total returned as winnings is `0.91(L+W)`. The controlled wallets together lose `0.09(L+W)` even though the losing wallet reports loss `L`. There is no need to predict the outcome with equal stakes. External bettors, gas, capital lockup and rounding change the result; none provide a protocol-level defense.

**Balanced example:** wallet A and wallet B each bet 100 IMD on opposite sides. One receives 182 IMD and the other zero. Combined cost is 18 IMD; the losing wallet mines **2M HAMSTER** at the initial rate. If the coalition owns fraction `s` of eligible staking weight, it recovers `10s` IMD of the 10 IMD staking fee, so cost becomes `18−10s`. It can also recover jackpot allocations through future tickets, but that is not immediate or guaranteed.

**Predictable-outcome variant:** put `L` on the likely loser and only `ε` on the likely winner. If correct, cost approaches `0.09L`, while the loser still mines `R·L`. The attacker owns all winnings despite tiny winning stake. If wrong, the large stake returns almost the whole pool; under a net-loss definition even that winning wallet can qualify for its roughly 9% fee loss, alongside the small losing wallet. Mining is reduced, but the attacker does not lose the whole large stake. Repetition in a reliably sleeping SLEEP market makes this particularly accessible. The one-sided refund rule is defeated by the second wallet. Minimum stakes raise `ε`; they do not fix the mechanism.

If `s` of the staking fee is recaptured and `j` of jackpot contributions eventually recaptured, effective coalition cost before oracle reimbursement is

`C = [0.09 − 0.05s − 0.02j]·(L+W) + gas + capital cost`.

An eventual full staking+jackpot recapture leaves 2% of turnover (team and oracle), before considering oracle payment offsets. Treat `s=j=1` as an aggressive scenario, **not** an unconditional lower bound or a promised achievable cost. A coalition that also receives referral/team rebates or owns liquidity has a different cost again. Other players' fees and speculative token prices can make the whole strategy profitable. The system cannot identify common ownership from addresses.

#### Two-wallet cost at every halving

Costs below are **IMD per HAMSTER**, excluding gas, price impact, timing risk and capital lockup. `R_h=20,000/2^h` per IMD loss; each loss band is 20,000 IMD. “Stake recapture” assumes all staking fees returned to the coalition, without jackpot recovery.

| Epoch h; cumulative loss band (IMD) | R_h | Balanced, no recapture: .18/R | Balanced, full stake recapture: .08/R | Tiny winning side, no recapture: .09/R | Tiny side, full stake recapture: .04/R |
|---|---:|---:|---:|---:|---:|
| 0; 0–20k | 20,000 | .000009 | .000004 | .0000045 | .000002 |
| 1; 20k–40k | 10,000 | .000018 | .000008 | .000009 | .000004 |
| 2; 40k–60k | 5,000 | .000036 | .000016 | .000018 | .000008 |
| 3; 60k–80k | 2,500 | .000072 | .000032 | .000036 | .000016 |
| 4; 80k–100k | 1,250 | .000144 | .000064 | .000072 | .000032 |
| 5; 100k–120k | 625 | .000288 | .000128 | .000144 | .000064 |
| 6; 120k–140k | 312.5 | .000576 | .000256 | .000288 | .000128 |
| 7; 140k–160k | 156.25 | .001152 | .000512 | .000576 | .000256 |
| General h; 20k·h to 20k·(h+1) | 20,000/2^h | .000009·2^h | .000004·2^h | .0000045·2^h | .000002·2^h |

With eventual full jackpot recovery too, costs are `.04/R` balanced and `.02/R` tiny-side: initially **.000002** and **.000001** IMD/HAMSTER. A fully available +50% NFT bonus divides cost per total HAMSTER by **1.5** until its cap/pool binds. A 2× wake-up multiplier halves it again; stacking both gives 3× tokens and one-third cost. Vesting defers liquidity but does not remove this arithmetic; letting unvested rewards earn IMD actually helps recapture fees.

A sale tax of 1.6% would require a pre-tax realizable sale price above `cost/.984`, before LP fees, gas and price impact. For balanced initial farming with no recapture, that is about `.000009146` IMD/HAMSTER. There is no known token price or IMD pool depth from which to conclude realized profit. If the 100M pool tokens were all valued at price `p`, their simple notional is `100M·p`, **not necessarily pool backing**. Concentrated/single-sided liquidity requires its actual range and funding to evaluate realizable exits.

**[Recommendation]** 20,000/IMD is not defensible as a safe launch rate. Do not advertise nominal lost IMD as money that left the coalition. Keep mining inactive at game launch, retain historical accounting, and disclose that no future reward is guaranteed. If later activating a bounded experiment, a much smaller **1,000/IMD** is a starting scenario, not a security guarantee: tiny-side full stake+jackpot recovery still costs only `.00002` IMD/HAMSTER, or `.00001333` with full boost. A positive market price can always exceed that. No per-wallet cap, cooldown or line rule makes positive-rate permissionless lose-to-earn Sybil-proof.

Prefer a fixed daily emission budget distributed against **eligible net losses capped by fees attributable to that account**, rather than uncapped nominal losses. Count only binary markets initially; exclude EXACT, all refunds, referrals and boosts from the base metric. The fee cap reduces the amplification but still allows paid farming and concentration. Set a hard emission budget, publish worst-case farming yields and treat the distribution as a paid promotion. A low-variance participation reward funded independently of amount lost is another option; it still needs a Sybil budget. Do not automatically price rewards from a manipulable HAMSTER/IMD spot quote.

### O1 — Oracle truth, completeness and settlement boundaries

**[Observed]** [EIP-712](https://eips.ethereum.org/EIPS/eip-712) includes chain and verifying-contract domain fields and explicitly does not itself implement replay protection. **[Derived]** signature verification establishes who signed a statement, not that the hamster ran. A panel reading one API still shares that API's sensor, operator, availability and correction risks. Someone able to influence the physical wheel or data publisher may be an informed bettor; cannot be fixed by a larger panel alone.

**[Recommendation]** bind the exact six source rounds, source chain/network, dataset identity, units, genesis and indexing convention, consumer chain ID/address, answer schema, and question version. Use the project's canonical question hash, verified typed `uint256` answer of exact length, authorized signer, minimum panel 5 with at least 4 agreeing **and** `agreed >= quorum`, valid issue/expiry interval, consumer-scoped request replay protection and a single terminal status per game window. Domain separation between v1 and v2 is mandatory. Validate current production attester and domain using a real public attestation before deployment; do not guess an address.

Betting must close **before the first measured round starts**, never at window end. Accept results only after all six rounds are final and published. `issuedAt >= windowEnd` is necessary but insufficient: a post-end signer can still have read stale data. Missing rounds, resets, duplicates or zero-valued unavailable responses must be unanswerable, never “sleep.” Pin dataset evidence (round IDs, source block/hash or finalization marker and evidence link), and document how corrections are handled. First valid attestation wins makes contradictory valid answers a race; a delayed challenge path would change the architecture and require new trust rules. For the ownerless design, require final-source data first and acknowledge that a dishonest accepted answer is irreversible.

Use `end <= now < end+48h` for settle, `now >= end+48h` for timeout; specify equality exactly. No pre-end timestamp tolerance. Timeout is a permissionless terminal transition, not a competing second outcome. Freeze fees until valid settlement, reserve all refund liabilities, and keep pre-existing jackpot capital outside a timed-out window's refunds. Do not assume a “max 3194” cap: it is an observation, not a physical/protocol bound. Bad answer magnitude must not create unbounded gas or arithmetic overflow.

No pause/upgrade means an accepted oracle bug cannot be repaired in place. Prefer an immutable **per-window funded-liability limit** calibrated to oracle assurance and a small initial jackpot, not an assertion that the oracle is trustless. A safe numeric exposure limit cannot be inferred without IMD value and oracle security assumptions. Prelaunch operations must monitor contradictions, stop frontend promotion/new operator-created markets when needed, publish incident notices, and allow contractual timeouts; this does not give anyone power to freeze others' contracts.

### J1 — Jackpot chronology, rollover and the coverage attack

**[Derived]** if windows k and k+1 are both pending, paying 80% of the live global jackpot to whichever settles first gives two callers control over different payouts. Even if payouts conserve total funds, ordering changes who wins. A “refund everything” timeout is also incompatible with prematurely feeing tickets and spending their contributions in another window.

**[Recommendation]** finalize jackpot accounting in increasing window index, with bounded permissionless advancement through settled/expired/empty windows. Store each window's ticket escrow separately. On valid finalization: add its 93% ticket contribution and **that window's** 2% non-refunded binary fees to its incoming seed, determine winners, reserve 80% as immutable claim liabilities if any win, and carry exactly the remaining 20%. With no winners or sleep, carry the entire available amount. On timeout refund its tickets in full, collect no ticket/binary fees, and carry prior seed unchanged. A sleeping window rolls the net 93% ticket contribution; it does **not** also roll the 7% already assigned to other recipients. If the intended promise is literally 100% ticket rollover on sleep, remove those fees on sleep and reprice the plan.

Track hook donations in separate pending buckets assigned deterministically to the earliest eligible **not-yet-started** window at receipt. They must not change a window's already-fixed prize, or become withdrawable as someone else's timeout refund. Never use total ERC-20 balance as the jackpot: it contains refunds, staker fees, oracle credits and unclaimed winnings. Resolve a missed predecessor by timeout, not by indefinite blocking. Pre-start publication of the usable jackpot also lets players assess entry value.

At a known awake result near 2100, ±1% covers roughly **42 integer-scale work units**; ±0.25% covers roughly 10–11. Geometrically spaced guesses cover a multiplicative result range efficiently. Covering 1090–3060 requires about

`ceil[ ln(3060/1090) / ln((1+t)/(1−t)) ]`

nonoverlapping relative-tolerance tickets: **52 at 1%** (260 IMD) or **207 at .25%** (1,035 IMD), ignoring integer endpoints and safety overlap. This targets only the central 80% of the supplied awake distribution, not all possible work. One ticket per address merely adds wallets and gas. The observed max must not bound valid results.

If an attacker covers the winning range and owns all winning tickets, entering n tickets with old seed J returns `.8(J+4.65n)`. Its net ticket cost is `5n−.8(J+4.65n)=1.28n−.8J`, before gas and fee recapture. With certain coverage and no other winners it profits when **J > 1.6n IMD**: about **83.2 IMD for 52 tickets**, or **331.2 IMD for 207**. These are conditional illustrations, not actual expected-value thresholds. With win probability q and complete payout ownership when it hits, one-window expected net is `.8q(J+4.65n)−5n`; threshold `J > 6.25n/q−4.65n`. Other winners dilute payout; sleep, tails and gas lower q/profit. Retained seed is not a refund to the current player. Tighter tolerance raises coverage cost but cannot prevent attacks on a sufficiently large rollover.

**[Recommendation]** retain 5 IMD tickets and 80/20 initially, use **±0.25%** if empirical density supports it, publish aggregate odds/coverage economics, and explicitly allow that jackpot hunting is part of the game. No free tickets against a material carry pot. A fully enforceable anti-coverage claim would require a different identity/trust model. Consider an absolute ±5-unit band for simpler bounded winner counting, but backtest its varying relative difficulty before choosing it.

#### Jackpot hit probability by ticket count

**[Derived model, not empirical odds]** for independent randomized tickets with single-ticket success probability p in an awake window, `P(any hit | awake)=1−(1−p)^n`. It does not apply to copied guesses as independent trials: identical guesses have the same hit event regardless of n. Strategic spacing uses union coverage; n times p is an upper bound when each band has mass at most p, not an independence formula.

For a reproducible sensitivity illustration, assume results **conditional on the central p10–p90 interval** are uniform over a continuous 1970-unit span, tickets sampled independently in that span, and approximate each band by its width at 2100: p=42/1970 or 10.5/1970. Ignore boundary clipping and discrete rounding. The “all hours” columns below are only the modeled **central-interval contribution**, multiplying by `.23 × .80 = .184`; unmodeled tail hits may add to it. Treating work 1–99 as sleep could lower the true awake fraction below .23.

| Paid tickets n; cost | ±1% hit conditional on central awake result | All-hour central contribution | ±.25% hit conditional on central awake result | All-hour central contribution |
|---|---:|---:|---:|---:|
| 1; 5 IMD | 2.13% | .39% | .53% | .10% |
| 5; 25 IMD | 10.21% | 1.88% | 2.64% | .49% |
| 10; 50 IMD | 19.39% | 3.57% | 5.20% | .96% |
| 25; 125 IMD | 41.65% | 7.66% | 12.51% | 2.30% |
| 50; 250 IMD | 65.96% | 12.14% | 23.45% | 4.31% |
| 100; 500 IMD | 88.41% | 16.27% | 41.40% | 7.62% |

For strategically nonoverlapping equal-width bands, modeled central coverage is approximately `min(1,n·width/1970)`: 25 tickets give 53.3% at 1% and 13.3% at .25%; 50 give approximately 100% versus 26.6%. Relative-width spacing gives the more accurate 52/207 coverage counts above. Concentrated modes can make a well-chosen single guess much better than uniform guessing. Nighttime-conditional awake probability can be much higher than 23%. Raw time series plus actual guesses are needed for honest hourly odds and backtests. There is no credible exact probability table recoverable from three quantiles.

### L1/P1 — Sleep, line selection and information timing

**[Recommendation]** define sleeping as `result < 100`, awake as `result >= 100`. Rename SLEEP to **“Snooze: fewer than 100 work units?”** The phrase “did it run at all?” means `result == 0` and is inconsistent with threshold 100. The 100 proposal is reasonable for ignoring tiny motion only provisionally: it is 9.2% of awake p10 and 4.8% of median, but no data supplied shows what fraction of valid nonzero hours it excludes. Compare thresholds **1, 25, 50, 100** against labeled motion/noise and source errors before freezing 100. Missing telemetry never maps to zero. Test 0/99/100 explicitly.

Predictable sleep is public information, not itself a fund-draining exploit in a pari-mutuel pool. A 77% sleep prior makes naive 50/50 SLEEP stakes poor for the awake side. For sleep probability p, winning-side gross return per IMD is `.91·T/S`; expected break-even requires `S/T <= .91p`. At p=.77, a SLEEP bettor needs sleep-side stake at most **70.07%** of the pool, holding that probability fixed; actual probabilities depend on hour and conditions. Pool balance is not a probability oracle. Show payouts and the 9% take, especially when both sides are nearly balanced.

On sleep, OU refunds fully and earns no fees/mining. EXACT is deliberately unfavorable in daytime: paid tickets roll while there is no chance of winning. Show a prominent sleep/rollover explanation. Do not subsidize a weak side to make a market appear active. One-sided refunds permit free directional optionality when nobody takes the other side; that is acceptable if clearly disclosed and fees/mining are zero.

**[Derived]** sorting the last 12 **settled** awake windows by index is insufficient. Suppose recent awake k−1 is high and older k−13 is low. A caller who creates k before settling k−1 obtains a different set than a caller who first settles k−1. A different order changes the membership even if sorting within either set is correct. Attackers can also pre-create far-future windows and freeze today's line. Betting on both sides can keep selectively chosen windows economically alive. A 12-awake median needs roughly **52.2 wall-clock hours** at 23% activity; the 162-hour sample contains only about 37 awake observations, so evidence for that estimator is thin. Circadian effects and serial correlation make the effective sample smaller.

**[Recommendation]** retain bootstrap **2100** and median of **12 awake windows**, but change the data rule. Permit opening only the next scheduled window during the preceding hour. Assign window k a fixed historical cutoff: include indices **i <= k−50**, allowing all included windows' 48h deadlines to pass before k's opening slot begins. Maintain a chronological finalized prefix; process valid results or timeout states in order and settle useful historical data even when no bets exist. Require this prefix to reach k−50 before opening, with permissionless bounded catch-up; genesis-short histories simply use what exists. Select the 12 latest awake observations in that prefix; bootstrap until there are 12. Once those 12 are selected, use floor of the average of the sixth and seventh sorted work values as the median. An exactly equal result is UNDER (`OVER iff result > line`). Snapshot at opening, same for every bettor.

This adds roughly two days of estimator lag on top of the lookback, an explicit price for deterministic finality. It also costs data publication for empty windows. If that operational cost is unacceptable, launch with a fixed **2100** instead of claiming a timing-independent dynamic line. Oracle withholding until timeout can still censor observations; a signing/data availability problem remains. A fixed wall-clock cutoff does not cure a dishonest source. Do not use only bet-funded windows as the sample. Keep max future creation at one window and no post-creation configuration changes.

### M1/T1 — Retroactivity, halvings and finite supply

**[Derived]** with rate R and halving band H, continuous cumulative emission is

`F(C)= sum over h of (R/2^h)·clamp(C−hH,0,H)`.

At R=20,000 and H=20,000, the total approaches **800M**. Each complete band emits 400M, 200M, 100M, 50M, 25M… With 50M removed for boosts, base vault 750M is fully allocated at **80,000 eligible cumulative IMD losses**, after epochs 0–3. Epochs ≥4 in the cost table describe the promised mathematical schedule, **not available funded rewards** under that allocation. With an 800M base vault the schedule approaches its cap asymptotically; finite-precision rates eventually reach zero and dust rules matter. Replenishing with an unactivated boost pool restores capacity but must not restart halvings.

A standalone pull `lossOf(k,a)` cannot reveal which cumulative-loss band applied historically. Using the counter at claim time lets late claimants choose timing, or lets early claimants consume a disproportionate pool. Using bet settlement order instead of index lets callers reorder emissions. Awarding an entire boundary-crossing loss at one rate is wrong.

**[Recommendation]** game stores, when chronologically finalizing each window, immutable `totalEligibleLoss[k]`, `cumulativeLossBefore[k]` and `cumulativeLossAfter[k]`, excluding void/refunded losses. Compute that window's base budget as `F(after)−F(before)` across all crossed halvings. Allocate pro rata among accounts' eligible losses, rounded down; do not give the last claimant the remainder. This deliberately makes all losses in a window share a blended rate and removes within-window claim ordering. Define a deterministic dust bucket. No claim mutates C. Add a checked total committed-emission counter, not merely a vault token balance check.

Before token launch the game must already expose this history (or enough immutable information to reproduce it). Retroactivity means retroactive **base entitlement**, not retroactive staking yield or NFT ownership. If mining is introduced as a later separate program, publish its activation/history policy before accepting any promoted mining bets. A pure view cannot notify a not-yet-deployed vault of historical events; immutable state and an independently reconstructible index are required. Never truncate an entitlement only because another claimant got there first.

If the original 20k rate is retained against advice, reduce H to **18,750** to make the asymptotic base commitment 750M, and separately budget boosts. That fixes funding only. The lower-rate alternative **R=1,000, H=375,000** also has a 750M ceiling and spreads issuance; it still does not establish profitability safety. Returning an unactivated 50M must be accounted as surplus, not an excuse to retroactively change the emission curve.

### S1 — `lossOf` and vesting integration contract

**[Recommendation]** the loss API should return **net principal lost**, consistently aggregated across the account's binary positions in the window:

`lossOf(k,a)=max(0, binaryStakePaid − binaryRefundEntitlement − binaryPayoutEntitlement)`.

Use immutable entitlements, not amounts already claimed. The amount must be identical before and after game claims and must include both sides of both binary markets when netting; otherwise the same wallet can self-hedge and still report a gross losing side. Do not add EXACT ticket cost to mining in v2: rollover would become both a jackpot subsidy and an emission path. If a future version includes it, explicitly decide whether jackpot returns offset losses; those contingent liabilities make the integration harder. Staker income is not a betting payout, so the API cannot net coalition staking rebates or identify two wallets as one. Document this limitation.

Expose terminal status separately: unresolved should revert or return status+zero, never an indistinguishable provisional result. Timeout and one-sided refunds produce zero loss; sleeping OU produces zero while settled SLEEP losses can qualify. Per-account net losses are not generally the market's total losing-side stake: a winner can still have net loss after fees. `totalEligibleLoss` must equal the sum of the exact same per-account rule. Maintaining this without an unbounded settlement loop needs design work: update per-account position categories while betting and maintain bounded aggregate categories, or use a reviewed proof-based accounting scheme. Do not promise O(1) aggregate loss computation merely because each user's view is O(1). A fee-capped reward metric should be a separate `miningLossOf` so economic terminology stays honest.

The vault keys replay protection by `(gameAddress, windowIndex, beneficiary)`; verification uses a pinned game, then marks claimed before creating a funded vesting grant. Permissionless claim-for can be supported only if payment/credit always goes to that beneficiary. Distinct base and boost claim bits prevent replay or a failed optional boost from blocking base rewards. Batch claims must be bounded. Unclaimed IMD game payouts remain claimable independently of HAMSTER mining.

**[Derived]** “MiningVault is the game's single staking token holder” is ambiguous. If the game accepts HAMSTER directly, every holder could stake unless explicitly restricted. If the vault escrows the entire 750M reserve and stakes its own `balanceOf`, undistributed tokens capture fees and dilute users. If only vested tokens are deposited, unvested “staked” balances receive no game-level weight. None matches the intended plan automatically.

**[Recommendation]** set the game's one-time staking token to a **nontransferable, non-mintable-by-TEAM accounting receipt**, minted/burned only by the immutable MiningVault to reflect users' eligible stake, held/staked only by that vault. Alternatively hardwire an equivalent vault-only stake adapter; specify which before build. The game can accrue fees to a vault escrow while the vault's own IMD accumulator distributes them by users' eligible weight. Exclude all undistributed reserves, boost reserves and unclaimed grants from weight. Do not distribute the 5% over “whatever token balance the vault holds.”

A seven-day linear grant is fully backed and nontransferable; its full remaining locked principal may count as stake if that is intentional. Moving vested principal from locked to liquid-staked must not change total weight; withdrawal does. At an unstake request, checkpoint accrued IMD and remove requested eligible weight immediately. Release vested principal after 24h. Unvested principal cannot be withdrawn before its vesting time and must not gain immediate liquidity via an unstake request. Define partial requests, cancellations, multiple grants and re-staking so a token never earns twice or bypasses either delay.

If rewards accrue by stake at settlement, an attacker stakes just before a delayed profitable settlement, settles many windows, then exits; a 24h exit delay alone does not prevent it. Stream eligible fees across time and use a **24h stake warm-up**, no historical income for retroactive grants, and an accumulator checkpoint before every weight change. Pre-staking fees should stay in escrow and stream over **30 days of wall-clock time**, not 30 caller-triggered settlements. If eligible supply is zero, retain the undistributed amount for the next scheduled stream interval; never let the first depositor instantly receive the backlog. Use bounded grant accounting (e.g. daily coalesced buckets with exact stated rounding), reentrancy protection, and separate HAMSTER principal from IMD income.

The 48h TEAM selection is a real trust power: a malicious receipt/vault could direct the 5% share to TEAM. Review and publish immutable vault/receipt bytecode, authorization, supply constraints and configuration before the timelock; permit execution only of the exact reviewed pair. No token choice should enable upgrades, arbitrary share minting, vault withdrawals or bypass staking exclusivity. “No owner” is not a substitute for documenting this one-time choice.

### R1 — Oracle reserve runway and reimbursement attacks

Let B be daily **non-refunded fee-paying binary** IMD volume, E daily paid EXACT gross IMD volume in validly settled windows, V hooked IMD-leg swap volume, N paid attestations/day and K actual all-in cost per attestation (IMD). Donations D are not recurring revenue. The proposed reserve change is

`Δreserve = .01(B+E) + .001V + D − N·K`.

No fees arise from one-sided binary refunds, sleep OU refunds or timeout refunds. Sleep EXACT can fund the reserve if its 7% fee is retained as recommended. Hook fees are collected only on actual trades through that hook. Do not count LP liquidity or token inventory as oracle money.

**[Observed]** the fetched live quote is 0.5 IMD per oracle request; **[Unknown]** keeper mainnet gas in IMD, retries, failed requests, finality and latency. At request price alone, one paid hourly settlement needs **50 IMD/hour** of fee-paying bets or **500 IMD/hour** of hooked trading. These are alternative funding amounts; do not double count. Always-on 24 settlements/day cost **12 IMD/day**, not just the approximately 5.52 awake hours/day. Sleeping results still require an oracle to settle SLEEP and roll EXACT.

| Illustrative daily activity; 24 requests/day, K=.5 | Reserve revenue/day | Burn/day | 100 IMD reserve runway |
|---|---:|---:|---:|
| No bets/trades | 0 | 12 | 8.33 days |
| B+E=100; V=0 | 1 | 11 | 9.09 days |
| B+E=500; V=0 | 5 | 7 | 14.29 days |
| B+E=1,200; V=0 | 12 | 0 | Break-even for requests only |
| B+E=100; V=5,000 | 6 | 6 | 16.67 days |

For an actual reserve R0, runway is `R0 / max(NK−revenue,0)` when burn is positive, not a promise of uninterrupted service. At K=1 IMD and 24 requests/day, request+keeper budget requires 2,400 IMD/day of bets with no swaps. A 30-day request-only prefund is **360 IMD**; recommend **720 IMD** as an illustrative 30-day budget at K=1, then replace K with measured costs before launch. Maintain a public seven-day coverage alert. If 720 IMD cannot be committed, fund fewer paid windows and use a fixed line or a separately funded historical data feed; do not imply an unfunded cadence will run itself.

**[Derived]** reimbursing “the first settler” rewards the fastest copier of a published/mempool attestation, not necessarily the wallet that paid for it. A fixed bounty above cost can also incentivize minimum-size self-bet windows or even empty-window reserve draining. A reserve below reimbursement cannot be allowed to make a valid settlement revert.

**[Recommendation]** reimburse only one canonical paid request per window, to its cryptographically bound payer/beneficiary, capped by a predeclared supported request price; verify that payer binding is actually available in the oracle protocol. Otherwise use an operator-funded service or explicitly label the payment an open settlement bounty and budget copier risk. A small gas bounty, if any, is a separate bounded budget. Never reimburse arbitrary `tx.gasprice`, caller-supplied invoices, failed attempts or arbitrary duplicate empty windows. Account for any unpaid operator cost outside bettor funds. Depleted reserve must not impair settlement, timeout, refunds or user claims. Empty-history publication for the dynamic line is an explicitly funded operation, not unlimited access to a user-funded reimbursement faucet.

### H1/T1 — Hook, launch policy and drip

**[Observed]** Uniswap v4 hooks belong to particular pools, and the [PoolManager documentation](https://developers.uniswap.org/docs/protocols/v4/concepts/poolmanager) describes pool creation including an optional hook. **[Derived]** a hook cannot tax plain HAMSTER transfers or other unhooked venues; “1.6% on every swap” must mean **every supported swap in the designated pool(s)**. Arbitrage migrates activity where total execution cost is lower. Revenue and anti-snipe protection are not universal guarantees.

[Uniswap's custom accounting guide](https://developers.uniswap.org/docs/protocols/v4/guides/custom-accounting) distinguishes custom hook fees from LP fees and explains using actual swap deltas for partial fills. **[Recommendation]** charge 160 bps against the **absolute actual IMD leg**, on buy input or sell output, once per actual pool swap. Handle exact-input/exact-output, both currency orderings, multi-hop, partial fills, price limits, rounding and zero amounts. No spot-price conversion is needed for an IMD pair. Authenticate PoolManager and the intended PoolKey. Accrue recipient credits and let them pull; external jackpot/oracle distribution must not execute arbitrary game settlement during a swap. Bound callbacks and reentrancy. The [swap hook guide](https://developers.uniswap.org/docs/protocols/v4/guides/hooks/swap-hooks) notes the callback sender is typically a router; do not infer the actual buyer or referral identity from it.

**[Observed]** [IMD's current launch documentation](https://imd.fun/docs/#launch-fields) states a standard **1.25% trading fee**, split 1% payer and .25% network, and single-sided launch-token pool seeding. **[Unknown]** whether this applies in addition to or can be replaced by this custom hook. If additive, a 1.6% hook starts near **2.85% total stated fee rates** before any separate LP fee; exact realized cost depends on bases and fee ordering. Obtain a concrete launch-policy quote supporting the desired allocation, pool share, receipt/vault addresses and tax design. The 100M pool allocation must specify tick range, initial price and IMD funding/source; “vs IMD” does not prove that IMD is deposited at launch.

**[Recommendation]** remove the 98% anti-snipe tax. It deters ordinary early buyers, creates a predictable tax-decay timing game, and raises complex exact-output and disclosure risks. If retained against advice, specify percentage points (98,96,…,2,0 at minutes 0…49), immutable start tied to the intended pool's funded launch, and whether additive or sequential with other fees. At 98% plus 1.6% plus a 1.25% launch fee, naive addition exceeds 100%. A buyer's nominal input is not the post-tax purchase amount. Prevent premature initialization starting the clock, fee bypass through hook self-calls or alternate authorized paths, and any rearming power. Test at every boundary; refund/partial-fill accounting must use actual fills.

For the drip, `P_d=P0·.99^d`; after 7/30/365 days roughly **6.8%/26.0%/97.4%** has been released, half-life **68.97 days**. “Perpetual” means an asymptotic tail, not permanent meaningful yield. Implement elapsed-time decay, e.g. `exp(ln(.99)·seconds/86400)`, with fixed-point rounding and explicit dust behavior. A caller must not earn repeatedly by poking a daily 1% branch. Separate top-ups, vested release, zero-staker periods and pending IMD credits. An attacker can pay tax while holding most stake to recover 80% over time; not instant arbitrage, but the payment is not all external economic cost. Do not promote wash volume or promise sustainable APY from a finite launch pot.

## 3. Squeek Boost Pool review

**[Brief]** allocation becomes 100M swarm + 100M pool + 750M base vault + 50M boost = **1B**. Bonus is +50% of mined base rewards, not 50% more loss or a faster halving counter. Boosts do not advance base cumulative losses, do not recurse, and should share the same seven-day vesting.

[ERC-721](https://eips.ethereum.org/EIPS/eip-721) defines `ownerOf` as the **current** owner lookup; it does not provide historical ownership. **[Derived]** ownership checked only at reward claim lets someone borrow an NFT after the outcome and boost past losses. One NFT per wallet/window does not prevent transferring it between windows, boosting many old windows in one transaction, or exhausting a daily claim-time cap with backlog. A cap keyed only by wallet is bypassable; a cap reset at claim time gives the caller control over day selection.

**[Recommendation]** leave the pool dormant until the exact reviewed canonical collection exists on Ethereum mainnet. Define immutable game/collection/vault/pool bindings via a one-shot, publicly timelocked activation, with no arbitrary post-activation collection replacement. Merely detecting ERC-721 functions is insufficient provenance. The NFT address is presently **unknown** and must be verified when supplied; no guessed or placeholder launch address is appropriate.

Use a separate pre-window boost registration: check `ownerOf(tokenId)==registrant`, and bind `(tokenId,k)` to exactly one wallet before betting closes. One wallet may register at most one Squeek per window; one base claim gets at most one boost. For meaningful anti-flash protection, require **24h custody in an immutable escrow before registration** and lock withdrawal through that window's finalization/timeout. The escrow checks ownership on deposit and records the depositor as beneficiary; explicitly amend the simple direct-`ownerOf` plan to this custody model. The pool accepts only pre-registered, post-activation windows; no boost on historical pre-activation losses. If escrow is rejected, a signed pre-window registration plus a 24h delay only makes atomic abuse harder: an unescrowed NFT can be transferred, and a current-owner check cannot prove continuous holding. Say so rather than claiming flash-loan protection.

Even with escrow, a 24h or week-long rental is economically real and cannot be distinguished from ownership. Caps limit extraction; they do not prove fandom. Multiple rented Squeeks scale caps linearly. Legitimate transferred NFTs should carry their already-consumed cap and registration history with the token ID. Safe-transfer callbacks, withdrawal-to-contract paths and cancellation rules need reentrancy tests and must not lock NFTs forever on a timeout.

Recommend an initial **10,000 HAMSTER maximum bonus per token ID per UTC day**, attributed to the **window's start day**, not claim date, and a **100,000 HAMSTER global bonus budget per UTC day**. These are promotional budget choices, not telemetry-derived constants. The latter bounds a fully used 50M pool to at least **500 funded daily budgets**. Individual cap is full bonus on at most 20,000 base HAMSTER/day, equivalent to only **1 IMD nominal losses/day at the proposed original rate**, or 20 at 1,000/IMD. This sharply limits the original plan's boost value; disclose that before soliciting NFT buyers.

To avoid first-claim capture, finalize each day's eligible bonus amounts chronologically from immutable mining entitlements and registrations; cap each NFT's daily sum first, then pro-rate across NFTs if the global daily budget binds. Within an NFT's day, pro-rate across registered windows. Reserve that day's funded amount even for later claimants. This needs bounded or proven aggregation, not an unbounded loop over every NFT. If that complexity is excessive, omit the global daily cap and clearly disclose a maximum **10,000×eligible-NFT-count/day** drain instead. Never use “until empty” first-claimer allocation against already-earned promises. Current NFT supply and ownership concentration are unknown, so do not claim the per-NFT cap alone protects runway.

Set activation deadline to **boost deployment timestamp + 365 days**. Activation valid strictly before it; if still inactive at/after it, anyone can transfer the entire remaining 50M to the immutable MiningVault exactly once and permanently mark the pool swept. Activation and sweep must be mutually exclusive, including at the boundary. The destination has **no team rescue/withdrawal route**, and the vault must accept the transfer without minting claimant entitlement or restarting the curve. After activation there is no sweep path under the proposed promise; unused balance remains solely for earned bonuses. Specify whether unsolicited extra HAMSTER follows the same restrictions. Token/NFT custody liabilities are separate; escrowed NFTs remain withdrawable under their rules.

### If mainnet NFTs are delayed

1. **Preferred:** stay inactive and apply the 365-day public sweep rule. A frontend badge or free off-chain competition can recognize holders without allocating claimable mainnet bonuses.
2. **Trust-minimized but substantial work:** a canonical lock-and-mint NFT bridge with source-chain finality verification and one canonical mainnet representation. Prevent simultaneous origin/wrapper eligibility, replay and double minting; bind origin chain, collection, token ID and destination. Review bridge custody and withdrawal failures independently. A generic mainnet `ownerOf` on a random wrapper is not equivalent to canonical ownership.
3. **Explicit trusted alternative, only after a new review:** finalized source ownership snapshots relayed by a specified committee/light client, domain-separated and bound to window, wallet, token ID, nonce and source block. Include challenge/finality delays, cap total exposure, and reject stale or conflicting roots. A Merkle proof authenticates membership in a root, **not the honesty of its publisher**. A single HTTP API response or relayer signature cannot safely substitute for mainnet ownership under the current promise. Do not quietly activate this option with the simple `ownerOf` contract; it changes the trust model.

## 4. Recommended final parameters and decisions

These are explicit build recommendations; conditional items are launch gates, not invented measurements.

| Parameter | Recommendation | Reason / condition |
|---|---|---|
| Chain/genesis/window | Ethereum; **1791847200**; six 600s rounds; half-open intervals | Correct alignment; verify source's zero-vs-one-based round labels with real examples |
| Bet close/open horizon | Close strictly at first-round start; only next window opens during preceding hour | Prevent in-window information betting and far-future line pinning |
| Sleep | **result <100**, subject to raw-data noise validation; rename SLEEP wording | Prevent semantic ambiguity; never classify missing data as sleep |
| OU line | Bootstrap **2100**; last **12 awake** in finalized prefix through **k−50**; require 12 else bootstrap | Deterministic historical membership; accept lag or use fixed 2100 initially |
| OU equality | UNDER for `result <= line` | Binary market has no undefined equality case |
| Binary splits | Keep **91/5/2/1/1** winners/stakers/jackpot/oracle/team initially | Conservation; all void/one-sided/sleep-OU pools refund 100%, no fees |
| EXACT | **5 IMD**, tolerance **25 bps of result**, 80% payout/20% carry; 93/5/1/1 jackpot/stakers/team/oracle | Raises coverage cost ~4× vs 1%; one-address rule is UX only |
| Winner calculation | `abs(guess−result)*10000 <= result*25`, safely evaluated; no winner on sleep | Explicit integer boundary; use overflow-safe math |
| Jackpot order | Chronological finalization; fixed prize liabilities; timeout skips with full local refunds | Remove settlement-order extraction |
| Oracle | Current domain v2, ≥5 panel, ≥4 agreeing and ≥quorum; issued after all six final records | Signed truth remains trusted; source finality is still required |
| Oracle timeout | **48h after window end**, exclusive settle/inclusive void boundary | Disjoint terminal paths; paid service should finish well before it |
| Oracle funding | **720 IMD illustrative initial reserve**, measured K=1 budget; alert below seven days | Reprice after mainnet delivery/gas test; minimum request-only 30-day funding is 360 |
| Reimbursement | One supported paid request/window to authenticated payer; reserve-only | No copied-attestation windfall or unlimited empty-window bounty |
| Staking | Immutable vault-only receipt/adapter; **24h warm-up**, immediate weight stop on exit request, **24h exit**, seven-day funded vesting | Prevent instantaneous settlement capture and vesting escape |
| Pre-staking IMD | Stream over **30 wall-clock days**, checkpointed; no instant first-staker payout | Removes settlement-count manipulation |
| Supply | **100M swarm / 100M pool / 750M base / 50M boost** | Sum 1B; immutable commitments tracked separately |
| Mining at initial game launch | **Inactive**, loss history only, no guaranteed retroactive rewards | No price/liquidity or justified anti-farming budget yet |
| Conditional later mining | Prefer bounded daily promotion; if rate-halving design is chosen, **R=1,000, H=375,000**, capped by allocated 750M | Scenario to review, not farm-proof. Original R=20k would need H=18,750 for funding only |
| Boost | **+50%**, seven-day vesting, **10k/NFT/start-UTC-day**, **100k global/day** with deterministic allocation | Bounds promotional drain; no retroactive ownership windfall |
| Boost eligibility/expiry | Mainnet canonical collection only; 24h escrow before registration; inactive sweep at **365 days** to vault | Blocks atomic loans; term rentals remain possible |
| Hook | **160 bps on actual IMD leg**, proposed 100/50/10 bps team/jackpot/oracle | Conditional on factory policy; quote all additional LP/network charges |
| Anti-snipe tax | **0%**; remove 98→0 schedule | Avoid launch timing trap and additive-tax failure |
| Pool/liability limits | Fix only after source/security and price/liquidity review | No defensible numeric cap from current evidence; must be set before launch |

Tolerance implementation must not loop over every ticket/address at settlement. A relative band can contain many integers for a large valid answer. Use a bounded-depth range-count structure over a documented numeric domain (with explicit overflow/out-of-domain invalidity behavior), or a reviewed proof/counting protocol with enforceable availability. Individual claims verify that ticket's guess against an immutable winner count. A permissionless settlement that requires an off-chain winner list with no completeness proof is unsafe. A ticket cap per wallet does not bound aggregate settlement gas.

## 5. Retention and virality features: verdicts

These eight ideas preserve the hamster theme; rewards are evaluated as economic liabilities, not merely marketing.

| Feature | Exploit/economic risk and concrete guard | Must be on-chain in v2? | Verdict |
|---|---|---|---|
| **Weekly “Wheel of Misfortune” biggest loser** | Whales self-hedge across wallets and chase a bonus bigger than their fee cost; punishes genuine small players. Even wallet-net losses do not solve it. Use a cosmetic badge and opt-in funny recap, no HAMSTER prize | No; later off-chain verified results | **Yes as cosmetic; reject monetary leaderboard** |
| **Daily free EXACT for qualifying stakers** | Splitting stake at the threshold creates many free claims on paid jackpot capital; flash stakes and recycled principal worsen it. Funding the ticket from team fees is still a finite subsidy with adverse selection | Not in v2; any real voucher requires immutable eligibility/redemption and a separate budget | **Reject against shared jackpot.** Try a free separate prediction badge league |
| **2× mining “wake-up hour”** | Doubles manufactured-loss reward exactly when activity is predictable; “first awake” can be chosen by delayed settlement or day-boundary ambiguity. Requires canonical night definition and chronological results | Financial multiplier would require mining/oracle logic; cosmetic night streak can be off-chain later | **Reject multiplier; approve “First Squeek” badge** |
| **Daily wake-up-time market** | First qualifying hour, no wake-up, source gaps, two bursts and 21:00–06:00 crossing midnight all need outcomes. Coarse time buckets lower settlement cost. Insiders can influence timing | New escrow/settlement module; cannot safely append liabilities to immutable v2 later | **Later pilot** with separate pari-mutuel buckets, explicit “no wake-up” and timeout, no mining |
| **“Bring a wheelmate” referral: .5% of referred bets** | Self-referrals and Sybil loops recover half the 1% team fee. Recalculate farming costs with residual fee smaller. Never pay on refunded bets or from winner principal | If promised for immutable game fees, fund a separate distributor or build the routing/accounting now | **Conditional yes later**, team-funded only, hard campaign budget, no extra bettor charge, nonmonetary default |
| **HAMSTER drop / Squeek Boost Pool** | Snapshot trading, rentals, replay and double source-chain ownership; an uncapped extra drop silently spends vault promises | Separate reviewed pool can activate later; immutable funding and sweep terms must be established when funded | **Use capped 50M boost instead of an additional drop**, with the eligibility rules above |
| **Hourly X/Telegram “Wheel Report” bot** | Reports can misstate pending answers or create fake urgency; no bot keys should control funds. Show terminal/refund status, UTC interval, payout and evidence links; opt-in alerts | No; later, read-only bot using finalized events | **Strong yes**: shareable result cards, sleepy/awake art, no reward for posting or fake volume |
| **“Snooze Passport” streaks and squad prediction cards** | Wallet spam is harmless if prizes are cosmetic; avoid publicly ranking financial losses or rewarding deposit count. Streaks based on opted-in predictions, not loss amount; no effect on payouts | No; off-chain signed predictions or indexed settled events | **Strong yes**: weekly reset, collective badges, no financial multiplier |

No recommendation requires posting to social accounts during this assignment. The highest-value launch features are readable payout odds, honest sleep/rollover messaging, a shareable finalized result, and a low-pressure cosmetic streak. They do not need a new subsidy loop.

## 6. Required changes before build and safe-launch gaps

**Short build gate:**

1. Freeze round numbering/genesis, market wording, equality/tolerance rules and **pre-start** betting close; obtain raw six-round examples and the 162-hour export.
2. Replace order-sensitive line/jackpot behavior with chronological accounting and deterministic cutoffs; specify empty, timeout and concurrent-window processing with bounded gas.
3. Specify `lossOf`, aggregate eligible losses, immutable cumulative emission intervals and netting; remove the 800M/750M inconsistency. Keep mining inactive until the distribution budget and farming tradeoff are accepted.
4. Specify the immutable staking receipt/adapter, time-based income, funded vesting and exit accounting. Fully review the one-time TEAM selection and all pre-token fees.
5. Bind oracle source completeness/finality and reimbursement recipient, segregate every IMD liability, and fund a measured operations budget. Set exposure limits before accepting funds.
6. Specify boost registration/custody, cap allocation, chain/collection identity, activation and 365-day sweep; reconcile the desired hook with an actual IMD launch policy. Remove the launch tax.

**Still missing for safe launch [Unknown unless supplied]:** source round zero/one convention; raw/API completeness and finalization semantics; labeled tiny-work data; authority over wheel/sensor/feed and trading restrictions for informed operators; attester identity/rotation policy compatible with no upgrades; conflicting-attestation policy; real mainnet request latency and keeper gas; IMD price/liquidity and oracle exposure limit; exact pool price/range/funding and factory fee layering; token/receipt/vault deployment sequence; NFT collection/provenance, supply and concentration; and enforceable funded cap allocation for delayed claims. A report need not invent these to recommend a design, but deployment cannot leave them implicit.

Before launch require independent contract/economic review and adversarial tests for: two-wallet and many-wallet farming; fee recapture; cross-market netting; line creation/settlement permutations; empty windows; genesis and UTC-day boundaries; result 0/99/100/line-equal; exact tolerance endpoints and extreme inputs; all refund paths; duplicate/conflicting/expired/replayed attestations; copied settlements; reserve depletion; jackpot liabilities across 48h backlog; threshold-crossing emissions; claimed/unclaimed entitlement equality; vault weight and vesting conservation; all Uniswap swap modes; NFT transfer/rental/flash-loan sequences; and activation/sweep races.

Critical invariants: **IMD assets ≥ all principal/refund/winner/staker/team/oracle/jackpot liabilities**, with no category counted twice; **committed base rewards ≤ allocated base HAMSTER**; **committed boost rewards ≤ allocated boost HAMSTER**; **custodied HAMSTER covers vested+unvested+withdrawal principal**; no claim-order-dependent entitlement; and no unbounded-user settlement loop. Ownerlessness makes these checks more important because a bug is not patchable after deployment.

## 7. Reproduction and attribution notes

The tables and emission/runway examples are reproducible offline with `python3 research/calculations.py`; its checks validate arithmetic assumptions, not hamster probabilities or deployed contracts. `README.md` states scope and limitations. The public capabilities snapshot records the price observed on the review date. No software build was requested or performed.

Primary technical references used: [EIP-712](https://eips.ethereum.org/EIPS/eip-712), [ERC-721](https://eips.ethereum.org/EIPS/eip-721), [IMD docs](https://imd.fun/docs/), [v1 integration reference](https://github.com/identity-md-launches/launch-1951-workflow-contract-stage-context/blob/main/docs/ORACLE.md), [Uniswap PoolManager](https://developers.uniswap.org/docs/protocols/v4/concepts/poolmanager), [custom accounting](https://developers.uniswap.org/docs/protocols/v4/guides/custom-accounting), and [swap callbacks](https://developers.uniswap.org/docs/protocols/v4/guides/hooks/swap-hooks). Source-based facts are linked where used; attacks, formulas and recommended values are this review's derivations or judgments. No unavailable telemetry or failed explorer fetch is presented as verified evidence.
