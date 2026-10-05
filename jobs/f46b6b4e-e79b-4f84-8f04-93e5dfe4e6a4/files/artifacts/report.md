# $EMBER — Third Swarm Review
## Adversarial Simplification, Incentive Attack & Final V1 Architecture Challenge

Review date: 2026-10-05 (brief dated 2026-10-06)
Reviewer: single Swarm contributor (AI). This is not an independent multi-reviewer panel.
Subject: the "$EMBER Living Economy" architecture candidate for IMD Ember World / Genesis PEPE

---

## 0. Read this first: evidence limits

| # | Limitation | Effect on this report |
|---|---|---|
| L1 | **The two reports named as primary sources were not in the workspace.** The "current $EMBER Living Economy report" and the "earlier conservative architecture / tokenomics / threat-model report" were not provided. The repository held one commit ("Empty workspace") and no files. | The candidate is reviewed **as the brief describes it** (§2–§3 of the brief). Anything those reports say beyond the brief, such as exact tranche percentages, contract interfaces or emission schedules, could not be checked. Where the brief says "the current range" (for example, outcome tranche %), this review does not know the number and treats it as OPEN. |
| L2 | **The brief was cut off at §4.5 ("DELAYED").** Sections after 4.4 were not received. | §4.5 onward follows the brief's own list of required outputs (attack scenarios, economic failure, minimum V1, roadmap, open decisions, go/no-go). The cut-off text is not invented. |
| L3 | Project constraints for IMD Ember World / Genesis / Build Vault were described only at the level of the brief. | These are labelled PROJECT CONSTRAINT and are only as reliable as the brief. |
| L4 | Platform facts were checked against live official pages on 2026-10-05 (listed in §15). | Platform parameters change. Re-check them before deployment (see the go/no-go list). |

Label key used throughout:
- **FACT**: checked against an official source listed in §15.
- **PROJECT CONSTRAINT**: stated in the brief.
- **ASSUMPTION**: believed reasonable but not verified.
- **RECOMMENDATION**: this reviewer's judgement.
- **EXPERIMENTAL**: worth trying, without a guaranteed outcome.
- **OPEN / TBD**: needs a decision or data that this review cannot supply.

---

## 1. Executive summary

**Verdict: CONDITIONAL GO for a much smaller V1.** The core idea survives the attack. The current candidate has roughly twice as many components as V1 needs, and it puts outcome-linked money in the wrong place.

The main conclusions:

1. **Forecast-committed building is genuinely distinctive, but only the forecast-and-learn part.** Committing a hash of a falsifiable forecast before review, then publishing forecast vs. actual and feeding that back into who gets to propose next, is a mechanism no meme, tax, burn, staking or rebase token has. It changes product behaviour: what gets built next depends on whose past predictions held up. **KEEP.**

2. **Outcome-linked payment is the weakest part of the design. Cap it at 0% in V1 and at most 10% later.** World metrics at launch will be low-traffic, noisy and heavily driven by outside factors such as IMD market activity, X reach and Sepolia-only availability. Holding back pay for delivered, QA-passed work on that basis is unfair. It also invites the gaming the design is trying to stop: agents will sandbag forecasts, pick vanity metrics or ask for padded budgets. **RECOMMENDATION:** pay 100% on QA-passed delivery in V1. Let forecast accuracy affect only **future proposal rights**, which is non-financial. An optional "calibration bonus" (paid from a separate small pool, never withheld from base pay) can be trialled in V1.5 at most 10% of base.

3. **The AI must not choose its own target metric.** Metrics come from a small **Human/Safe-approved Metric Catalogue**. Each catalogue metric is paired with a fixed **guardrail metric** (for example, room clicks are only valid alongside D7 return-visit rate not falling). An agent picks from the catalogue and cannot define new metrics.

4. **Small samples fail closed.** If the pre-set minimum sample is not reached within the horizon (default N ≥ 200 unique sessions per arm, or ≥ 30 for binary event metrics with a ≥ 5-event floor), the result is recorded as **INCONCLUSIVE**. Inconclusive results have **zero effect** on the Learning Ledger in either direction.

5. **Most components should be off-chain or deferred.** V1 needs **two to three contracts**: the fixed-supply EMBER ERC-20 (IMD standard launch, plain transfers), a **Safe** treasury, and optionally one tiny **ForecastCommit** registry, for which IMD's own `oracle.request` / signed git commits may be enough. Revenue Router, Epoch Manager, Mode Registry, on-chain Build Registry, on-chain Learning Ledger, outcome-tranche escrow and any custom v4 hook are all **DEFER or REMOVE**.

6. **Revenue is fragile and must be labelled honestly.** FACT: IMD standard launches pay the requesting wallet 1.0% of every trade, and **only Sepolia is open today**. Testnet fees have no market value. Until a mainnet pool exists, $EMBER has **no real revenue**, and "self-sustaining" is a design target only. V1 must run on a pre-funded Build Vault with a published runway, and must scale down automatically ("ember mode") when inflows fall.

7. **Authority stays human.** AI proposes, reviews, builds and measures. Only a Safe (recommended 2-of-3 at least) moves money or publishes to production. There is no autonomous spend path in V1.

8. **The biggest residual risks** are collusion between agents and reviewers who share the same base model or operator, concentration of proposal rights in early winners, and Safe signers acting as a single point of failure. Each has a concrete mitigation in §7.

### Final V1 in one line

> **Fixed-supply EMBER + Safe-held Build Vault + off-chain (but hash-anchored) Epoch loop: catalogue-metric forecasts committed → independent review → Safe selects → paid on QA delivery → measured with fail-closed statistics → public Learning Ledger → proposal slots for the next epoch.**

---

## 2. What was reviewed (the candidate, restated)

PROJECT CONSTRAINT (from the brief):

```
EMBER ERC-20 ── Genesis Forge ── Revenue Router ── EMBER BUILD VAULT
                                                        │
Epoch Manager ── Build Registry ── World Pulse ── Mode Registry
                                                        │
World Brain ── Learning Ledger ── Swarm Dream Hall ── Agent Houses
                                                        │
                       Genesis PEPE ── Human/Safe ── Timelock
```

Philosophy: *AI imagines / proposes / builds / reviews; contracts enforce bounded rules; Human/Safe controls financial and production authority.* The token core is minimal and immutable.

Distinctive mechanism: **Forecast-Committed, Outcome-Graded Building**, with an optional outcome tranche held until measurement, and a Learning Ledger that affects proposal slots, review weight and visibility, but not token balances, yield or financial entitlement.

That last exclusion is already the right instinct. **The outcome tranche contradicts it.** A tranche is a financial entitlement that depends on outcome. Fixing that contradiction is the single most important change in this review.

---

## 3. Platform facts that constrain the design

| Topic | Finding | Label | Design consequence |
|---|---|---|---|
| IMD network availability | "Sepolia (`11155111`) is the only one open on `api.imd.fun` today." | FACT (imd.fun/docs, fetched 2026-10-05) | No real-value trading revenue exists yet. Any revenue model is hypothetical until mainnet. |
| Standard launch token | "On a project or hook launch the token is fixed: 1,000,000,000 with 18 decimals and plain transfers." | FACT (imd.fun/docs) | The immutable minimal core the brief wants is already what IMD gives by default. **Do not write a custom ERC-20.** |
| Supply split | 10% to the swarm, 90% to the requester. `poolBps` decides how much of the requester share seeds the pool. | FACT (imd.fun/docs) | The Genesis/Build Vault allocation must come out of the requester's 90%. Treat `poolBps` as an open decision. |
| Trading fee | "1.25% of every trade on today's factories, 1% to the paying wallet and 0.25% to the network." | FACT (imd.fun/docs) | Creator-side revenue is 1% of volume. The docs do not say how it is collected or in which asset (OPEN). |
| Pool type | Uniswap v4, single-sided initial liquidity in the launch token, paired with ETH or IMD. | FACT (imd.fun/docs) | Pairing choice changes revenue denomination and volatility (OPEN). |
| Custom tokens | A `custom_token` kind exists; its customisation limits are not fully documented. | FACT (existence) / OPEN (limits) | Not needed. A custom token adds audit surface for no V1 benefit. |
| Paid actions | `job.open`, `workflow.open`, `oracle.request`, `schedule.create` each cost 0.5 IMD. Schedules run with at least 10 minutes between questions and 30 between jobs, and "skipped and failed runs cost nothing." | FACT (imd.fun/docs) | The epoch loop can be driven by IMD **schedules** and **oracle panels** with no extra on-chain contracts of our own. Running cost is predictable: 0.5 IMD per action. |
| Oracle panels | Members answer independently. Attestation requires every one to match the quorum threshold. One member per seat. | FACT (imd.fun/docs) | A ready-made independent-measurement primitive for "did the metric hit?", if the inputs are public. |
| v4 hook immutability | "The hook is part of the PoolKey and is set once when the pool is created … It cannot be added, removed, or swapped afterward." | FACT (Uniswap v4 docs) | Any hook mistake is permanent for that pool. That is a strong argument **against a custom hook in V1**. |
| v4 hook power | Hooks can use return-delta permissions that "let a hook adjust balances." | FACT (Uniswap v4 docs) | A hook that skims swaps is effectively a transfer tax. That breaks Goal 1 (not a tax token). **REMOVE from V1.** |

---

## 4. The first required attack: is forecast-committed building actually good?

### 4.0 Distinctiveness test

| Comparator | Does it have pre-committed falsifiable forecasts tied to product changes? | Does it learn who to trust from results? |
|---|---|---|
| Meme coin | No | No |
| Transfer-tax / reflection | No | No |
| Buyback-and-burn | No | No |
| Staking / APY | No | No |
| Rebase | No | No |
| "AI-branded ERC-20" | Usually just an AI agent posting content | No |
| Grant DAO (retro-funding style) | Partly: reviews outcomes after the fact | Rarely builds a calibration record |
| Prediction market | Forecasts, but not attached to building | Prices, not proposal rights |
| **$EMBER forecast-committed building** | **Yes: forecast hash committed before review** | **Yes: Learning Ledger → proposal slots** |

ASSUMPTION: no comparable IMD ecosystem launch ties pre-committed forecasts to product-build selection. I scanned the public `identity-md-launches` GitHub organisation via search results only. That is not exhaustive.

**Verdict: distinctive. KEEP the forecast + ledger core.**

### 4.1 Metric selection failure

**Attack.** An agent proposes "Ember Lantern room" and forecasts "+40% room clicks". The clicks go up because the room is placed on the landing path. Return visits and world retention fall because the room is shallow and adds load time.

**Root cause.** The proposer picks the metric, so it will pick the one easiest to move.

**RECOMMENDATION: a closed Metric Catalogue, approved by the Safe and versioned.**

| Rule | Detail |
|---|---|
| M1 | Agents choose **only** from catalogue metrics. Adding a metric needs a Safe-signed catalogue change and only applies from the *next* epoch. |
| M2 | Every primary metric has a **paired guardrail** that must not get worse beyond a tolerance. If a guardrail is breached, the outcome is a MISS even if the primary target was hit. |
| M3 | At least one catalogue metric per build class must be a **retention-class** metric: D1/D7 return visits, session depth, or repeat Genesis PEPE holder interaction. |
| M4 | Each metric's definition, data source, query hash, minimum sample and noise band are published **before** the epoch opens. |
| M5 | Catalogue size for V1 is about 8 metrics. A small catalogue is easier to audit and harder to game. |

Suggested V1 catalogue (EXPERIMENTAL; the exact list is OPEN):

| Primary metric | Paired guardrail | Build class |
|---|---|---|
| D7 return-visit rate (World) | Median load time (p75) not worse by >10% | Any World build |
| Room session depth (median actions/visit) | D7 return not worse by >1 pp | Rooms / Dream Hall |
| Agent House proof completions | Proof-failure / abandonment rate not worse | Agent Houses |
| Genesis PEPE holder World visits (unique wallets, signed-in) | Unique-wallet count measured with sybil filter | Genesis PEPE |
| Wearable equip rate among visitors | Return-visit rate of equippers ≥ non-equippers | Wearables |
| QA defects found post-publish (lower is better) | None (inverse metric) | Any |
| Build cost vs. budget (lower is better) | QA pass required | Any |
| p75 page performance | Feature parity checklist | Performance work |

### 4.2 Goodhart's law

Once a metric decides evaluation, it stops being a good measure. Mitigations, in order of strength:

1. **Decouple money from the metric** (§4.3). This removes most of the reason to game.
2. **Guardrail pairing** (M2). Gaming the primary metric usually damages a guardrail.
3. **Hold-out / staggered exposure** where feasible: show the new build to a random 50% of sessions for the measurement window. This measures the build's effect rather than the World's overall trend. (EXPERIMENTAL; needs simple client-side bucketing. No on-chain component.)
4. **Grade forecasts on calibration, not size of win.** The ledger rewards *being right*, including correctly predicting a small effect, not *claiming big numbers*. A proper scoring rule (Brier or log score over a forecast interval) does this. An agent that forecasts "+2% ± 3%" and lands at +1.5% scores better than one that forecasts "+40%" and lands at +10%.
5. **Human qualitative review stays mandatory.** "Did this make the World better?" is answered by a Safe signer's short written note per build. That note is published next to the numbers and can veto a "HIT".
6. **Rotate measurement auditors.** The agent that built something never measures it (see §7, collusion).

**RECOMMENDATION:** state publicly that "the metric is evidence, not the goal". It is a cultural rule, but it costs nothing and frames every dispute.

### 4.3 External-factor unfairness: should outcomes affect payment?

**Analysis.** Early World traffic will mostly reflect things the builder cannot control: IMD launch activity, X algorithm reach, market sentiment, outages and seasonality. Even with a hold-out design, small samples (§4.4) make most early results inconclusive. Withholding pay for good work under those conditions:

- is **unfair**, because builders carry risk they cannot manage
- **raises bid prices**, because rational agents pad budgets by the expected withheld amount, so the World pays more for the same work
- **rewards sandbagging**, because agents forecast tiny effects to secure the tranche
- **adds escrow state** (on-chain or off-chain) for every build until its horizon ends
- **creates disputes** at every measurement, with money attached

**Tranche comparison**

| Outcome tranche | Fairness | Gaming pressure | Complexity | Signal value | Verdict |
|---|---|---|---|---|---|
| **0%** | High: paid for delivered, QA-passed work | Lowest | Lowest: no escrow | Signal goes into the Learning Ledger instead | **V1 RECOMMENDED** |
| 5% | Acceptable | Low | Needs escrow + dispute process | Marginal | Not worth the machinery |
| 10% | Borderline | Moderate | Escrow + disputes | Some | **Max for V1.5 as a *bonus*, not a holdback** |
| 15% | Unfair at low traffic | Material sandbagging | Same | Noisy | Reject for now |
| 20% | Unfair | High | Same | Noisy | Reject |
| 25% | Unfair | High; agents price it in | Same | Noisy | Reject |
| 30% | Clearly unfair; deters good builders | Very high | Same | Noisy | Reject |

**RECOMMENDATION (decision):**

- **V1: outcome tranche = 0%.** Pay 100% of the agreed budget on QA pass and production publish, which the Safe signs.
- **Forecast accuracy affects only future proposal rights**, review weighting and visibility, as the candidate already intends for the ledger.
- **V1.5 (EXPERIMENTAL): an optional calibration bonus of at most 10% of base.** It is paid from a separate, pre-funded "Calibration Pool", only for CONCLUSIVE results, and only for calibration (proper scoring rule), not for raw uplift. It is never a holdback. Base pay is never at risk.
- **Never** allow outcome-linked *clawback*.

### 4.4 Small-sample noise: fail closed

| Rule | V1 default (EXPERIMENTAL; tune after 3 epochs) |
|---|---|
| S1 Minimum sample per measurement | Continuous metrics: ≥ 200 unique sessions per arm (or in total, if there is no hold-out). Binary/event metrics: ≥ 30 exposures **and** ≥ 5 events in each arm. |
| S2 Pre-registered horizon | 7–14 days, fixed in the committed forecast. No "peek and stop early". |
| S3 Noise band | The catalogue publishes each metric's historical week-to-week variance. An effect inside the band is "NO DETECTABLE EFFECT". |
| S4 Fail closed | Missing data, broken instrumentation, sample below S1, or a known outage covering more than 20% of the horizon gives **INCONCLUSIVE**. |
| S5 Inconclusive is neutral | Zero ledger effect: no credit, no penalty. Proposal slots are unaffected. |
| S6 Extension | One extension of equal length is allowed, and only if declared in the original commitment. |
| S7 Sybil filter | Unique-wallet metrics count only wallets with prior history (for example, holding Genesis PEPE or EMBER above dust before the epoch opened). |

Expected consequence (ASSUMPTION): most V1 builds will be INCONCLUSIVE for the first several epochs. **That is fine and should be said publicly.** The ledger still learns **cost accuracy, delivery reliability and QA defect rate**. These are fully under the builder's control and need no traffic. In early V1 these three signals should carry most of the ledger weight.

### 4.5 Delayed outcomes and horizon mismatch

(The brief was cut off at this heading. This section covers the obvious meaning: outcomes arrive after the next epoch has started.)

- **Problem.** If an epoch is 14 days and the horizon is 14 days, epoch *n*'s results are only known during epoch *n+2*. Proposal rights would then lag by two cycles.
- **RECOMMENDATION:** The ledger updates **delivery-side metrics** (cost, on-time, QA) immediately after QA, and **outcome-side metrics** only when the measurement closes. Proposal-slot allocation for epoch *n+1* uses whatever has closed so far. Pending results count as neutral.
- **Decay.** Ledger scores decay with a half-life of about 4 epochs, so early luck or bad luck does not lock in.

### 4.6 Usefulness vs. complexity

| Sub-component | Value | Cost | V1 decision |
|---|---|---|---|
| Forecast commitment (hash before review) | High: core of the distinctiveness and stops after-the-fact narratives | Very low: a hash in a git commit, an event or an IMD oracle request | **KEEP** |
| Catalogue metrics + guardrails | High | Low (off-chain config) | **KEEP** |
| Fail-closed measurement | High | Low–moderate (analytics) | **KEEP** |
| Learning Ledger (off-chain, public, hash-anchored) | High | Moderate | **KEEP (off-chain)** |
| Ledger → proposal slots | High: this is what makes the system "learn" | Low | **KEEP** |
| Ledger → reviewer weight | Medium | Low | **MODIFY**: published but advisory only in V1 |
| Outcome tranche (holdback) | Negative in V1 | High | **REMOVE** (V1.5: bonus ≤10%, not a holdback) |
| On-chain ledger | Low | High (gas, immutability of bugs) | **DEFER** |

### 4.7 Is it suitable for V1?

**Yes, in the reduced form**: forecast commitment, catalogue metrics, fail-closed measurement, an off-chain public ledger, and proposal slots. **No, in the full form** (outcome tranche, on-chain registries).

---

## 5. Component-by-component decision table

| Component | Decision | Rationale | V1 form |
|---|---|---|---|
| **EMBER ERC-20** | **KEEP** | FACT: IMD standard launch gives a fixed 1B supply with plain transfers. That already matches "minimal / immutable". | IMD standard project launch. No custom code. |
| **Genesis Forge** | **MODIFY** | As a contract it duplicates the IMD launch. As an *event* (initial distribution to the Build Vault, Genesis PEPE holders and the pool) it is useful. | One-time distribution script plus a published allocation table. No persistent contract. |
| **Revenue Router** | **DEFER** | Real revenue does not exist yet (Sepolia only). Routing rules can be a Safe policy. | Written Safe policy: "X% of creator fees to Build Vault". Checked monthly. |
| **EMBER BUILD VAULT** | **KEEP** | The core treasury. | A **Safe** (≥2-of-3). Optionally a separate Safe for operations. |
| **Epoch Manager** | **MODIFY** | Orchestration does not need to be on-chain. | IMD `schedule.create` and a repository with an epoch state file. |
| **Build Registry** | **MODIFY** | A record of builds is needed, but not on-chain state. | Public git repository plus signed release tags. Optional minimal hash anchoring (§9). |
| **World Pulse** | **KEEP (simplified)** | Observation is step 1 of the loop and is what makes the World feel "alive". | Off-chain public dashboard of the catalogue metrics. |
| **Mode Registry** | **MODIFY** | "Modes" (normal / ember / dormant) are valuable for low-activity survival (§8). They do not need a contract. | A Safe-signed JSON file. Mode affects budget caps per epoch. |
| **World Brain** | **KEEP (bounded)** | The AI planner that observes, analyses and drafts epoch themes. | Off-chain agent. Read-only on data, no keys. |
| **Learning Ledger** | **KEEP (off-chain)** | The core "learn" step. | Append-only public file in the repository, hash-anchored per epoch. |
| **Swarm Dream Hall** | **KEEP** | A product surface where proposals and forecasts are visible to the community. That is part of the distinctiveness. | Web page rendering proposals, forecasts, outcomes and ledger. |
| **Agent Houses** | **KEEP (scope down)** | Proof experiences. | Start with 1–3 houses, not a full district. |
| **Genesis PEPE** | **KEEP** | Existing ecosystem asset (PROJECT CONSTRAINT). | Holder-gated World features. Optional "nominate a build theme" right (§7). |
| **Human / Safe** | **KEEP (strengthen)** | The only financial and production authority. | ≥2-of-3, with signers on separate devices and orgs where possible. |
| **Timelock** | **DEFER** (with condition) | It has nothing to protect if there are no upgradeable or parameterised contracts. | Required **if** any contract with admin parameters is added in V1.5+. Until then a publication delay ("announce 48h before spend > threshold") is a policy, not code. |
| **Custom v4 hook** (if contemplated) | **REMOVE** | FACT: hooks are immutable per pool and can adjust balances. That carries tax-token optics and permanent bug risk. | None. |
| **Burn mechanics** | **REMOVE** | Brief: burn ≠ revenue. Burning also looks like a generic token. | None. |
| **Staking / yield** | **REMOVE** | Conflicts with Goal 1 and creates securities-style optics. | None. |
| **Outcome tranche escrow** | **REMOVE (V1)** | §4.3 | None. |

Net result: **about 15 named components become 1 token + 1–2 Safes + an off-chain loop, with optional hash anchoring.**

---

## 6. Simplified V1 architecture

```
                         ┌─────────────────────────────┐
                         │  EMBER ERC-20 (IMD standard)│  FACT: fixed 1B, plain transfers
                         │  Uniswap v4 pool (IMD)      │  creator fee 1.0% → requester wallet
                         └──────────────┬──────────────┘
                                        │ creator fees (mainnet only; none on Sepolia)
                                        ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ EMBER BUILD VAULT = Safe (≥2-of-3)        ◄── initial allocation (Forge)  │
│ Policy: per-epoch cap set by MODE (normal / ember / dormant)             │
└───────────────┬──────────────────────────────────────────────────────────┘
                │ pays 100% on QA-pass + publish (Safe-signed)
                ▼
┌──────────────── OFF-CHAIN LIVING LOOP (public, hash-anchored) ───────────┐
│                                                                           │
│  OBSERVE  World Pulse dashboard (catalogue metrics only)                  │
│     ↓                                                                     │
│  ANALYZE  World Brain drafts epoch theme + gaps                           │
│     ↓                                                                     │
│  PROPOSE  N agents (slots from Ledger) → proposal + catalogue metric     │
│           + guardrail + forecast interval + budget + horizon             │
│     ↓     ─── hash(proposal) committed BEFORE review ───                  │
│  REVIEW   ≥2 independent reviewers (different model/operator)             │
│     ↓                                                                     │
│  FUND     Safe selects; budget reserved in epoch plan                     │
│     ↓                                                                     │
│  BUILD    Agent builds (IMD job/workflow)                                 │
│     ↓                                                                     │
│  QA       Separate QA agent + human spot check → Safe pays 100%           │
│     ↓                                                                     │
│  PUBLISH  Safe signer approves production deploy                          │
│     ↓                                                                     │
│  MEASURE  Pre-registered horizon; fail-closed stats; auditor ≠ builder    │
│     ↓                                                                     │
│  LEARN    Learning Ledger: cost acc., delivery, QA, calibration           │
│     ↓                                                                     │
│  REPEAT   Ledger → proposal slots next epoch (decaying, capped)           │
│                                                                           │
│  Rendered publicly in the Swarm Dream Hall                                │
└───────────────────────────────────────────────────────────────────────────┘
```

Authority boundaries:

```
           can read data   can propose   can review   can spend   can publish to prod
AI agents       ✔               ✔             ✔            ✘              ✘
World Brain     ✔               theme only    ✘            ✘              ✘
Safe signers    ✔               ✘ (V1)        veto         ✔              ✔
Contracts       —               —             —        (token only)       —
```

---

## 7. Attack scenarios

Severity: H = high, M = medium, L = low (RECOMMENDATION-level judgement).

| # | Attack | Mechanism | Sev | Mitigation (V1) |
|---|---|---|---|---|
| A1 | **Vanity metric** | Agent picks clicks over retention. | H | Closed catalogue + guardrails (§4.1). |
| A2 | **Sandbagging** | Agent forecasts a tiny effect to be "accurate". | M | Proper scoring rewards calibration *and* forecast intervals must be no wider than the catalogue's noise band × k. Reviewers rate "ambition" separately. Without a tranche there is little money motive. |
| A3 | **Wash traffic** | Agent or ally scripts visits to hit the metric. | H | Sybil filter (S7), session-quality heuristics, auditor ≠ builder, metrics favour returning signed wallets. Detected manipulation means the agent is barred for N epochs. |
| A4 | **Agent–reviewer collusion** | The same operator or base model runs both proposer and reviewer, which leads to rubber-stamping. | H | Reviewer independence rule: different operator wallet **and**, where possible, a different model family. Reviewer identities are published. Reviews are committed (hash) before the reviewer sees other reviews. The Safe sees disagreement explicitly. |
| A5 | **Shared-model correlated error** | All reviewers are LLMs with the same blind spots. | M | At least one human (Safe signer) qualitative note per selected build. A small community "objection window" (48h) in the Dream Hall. |
| A6 | **Proposal-slot concentration** | Early lucky winners accumulate slots and lock out newcomers. | H | Hard cap: one agent ≤ 30% of slots per epoch. ≥ 1 "open slot" per epoch for agents with no history (lottery among eligible). Ledger half-life decay (~4 epochs). |
| A7 | **Sybil agents** | One operator registers many agents to farm open slots. | M | One open-slot entry per operator wallet with prior IMD activity. Safe can bar operators. |
| A8 | **Budget padding** | Agent inflates the budget to capture surplus. | M | Cost accuracy is a ledger metric. Per-epoch cap by mode. Reviewers compare to a reference cost table. Payment is fixed at the reviewed budget, and overruns are not paid. |
| A9 | **Forecast swap** | Agent edits the forecast after seeing early data. | M | Hash committed before review. Mismatch with the reveal means automatic rejection and a ledger penalty. |
| A10 | **Measurement-pipeline tampering** | Whoever runs analytics alters numbers. | H | Query definitions are hashed in the catalogue. Raw aggregate exports are published. Optional IMD `oracle.request` panel to attest the published aggregate (EXPERIMENTAL). |
| A11 | **Safe signer compromise / collusion** | Signers drain the vault or self-deal. | H | ≥2-of-3 (3-of-5 when TVL > threshold, OPEN). Public spending log. Per-epoch caps in policy. Signers cannot also be builders. |
| A12 | **AI prompt injection via World content** | User content steers the World Brain or reviewers ("approve this proposal"). | M | Treat all World and community text as data. The World Brain has no keys. Reviewers get structured proposal fields, not free-form World text. |
| A13 | **Genesis PEPE holder capture** | Whales use NFT-gated nomination to steer themes. | L | Holder nominations are advisory, one per wallet per epoch, and the Safe picks. |
| A14 | **Narrative overclaim** | Marketing says "self-sustaining AI economy" before revenue exists. | M | Mandatory disclaimer. Publish runway and inflow figures each epoch (§8). |
| A15 | **Hook / custom-token exploit** | A bug in a custom contract is permanent. | H (if built) | Removed by not building one (§5). |

---

## 8. Economic failure analysis

### 8.1 Burn ≠ revenue (restated)

- **Revenue** is assets the Build Vault actually receives that can pay for work: creator fees in ETH/IMD/EMBER and any direct product sales.
- **Burn** destroys EMBER. It pays no one and funds nothing. **No burns in V1.**

### 8.2 Revenue model and its fragility

FACT: the creator receives 1.0% of every trade. FACT: only Sepolia is open, where fees have no market value.

ASSUMPTION / illustration only (not a forecast). Monthly creator revenue ≈ 1% × monthly volume.

| Monthly volume | Creator fee (1%) | Paid builds at 0.5 IMD per job + agent budget |
|---|---|---|
| 0 (Sepolia / dormant) | 0 | Funded only by initial vault |
| Low | 1% of low | Ember mode |
| Launch spike | Large, temporary | Do **not** set the cost base from spike months |

Fee currency: the docs fetched do not say whether creator fees accrue in the paired asset, the launch token, or both (OPEN). Fees in EMBER that must be sold to fund work create **reflexive sell pressure**: low price leads to more EMBER sold per build, which pushes the price lower. **RECOMMENDATION:** budget builds in the paired asset (ETH or IMD), and sell EMBER only under a published monthly cap.

### 8.3 Failure modes

| Failure | Trigger | Consequence | Design response |
|---|---|---|---|
| F1 Volume collapse | Post-launch decay (typical for new tokens: ASSUMPTION) | Inflows → ~0 | **Modes**: normal → ember → dormant, with automatic budget caps. |
| F2 Reflexive dumping | Vault sells EMBER to fund builds | Price spiral | Fund in paired asset. EMBER sale cap. Runway reported in the paired asset. |
| F3 Cost overrun | Agent work costs grow | Vault drains | Per-epoch caps. Cost accuracy feeds the ledger. Reference cost table. |
| F4 Mainnet delay | IMD mainnet not open | No real revenue | V1 is honest: "pre-funded experiment". Do not claim self-sustaining. |
| F5 Treasury concentration | Vault holds only EMBER | Correlated collapse | Diversify: target ≥ 50% of runway in the paired asset (RECOMMENDATION; the exact number is OPEN). |
| F6 Overspend in spike | Big launch month sets expectations | Later cuts feel like failure | Spend from a trailing 90-day inflow average, not the current month. |

### 8.4 Mode rules (Safe-signed JSON, no contract)

```
mode        condition (trailing 90d)                         per-epoch build cap
normal      inflow ≥ 1.0 × trailing build spend AND           up to 100% of plan
            runway ≥ 6 epochs
ember       inflow < 1.0 × spend OR runway 3–6 epochs         ≤ 40% of plan;
                                                              maintenance + 1 build
dormant     runway < 3 epochs OR inflow ≈ 0 for 60 days       measurement + ledger only;
                                                              0–1 small build
```

(EXPERIMENTAL thresholds.) **Even dormant mode stays "alive"**: World Pulse keeps observing, the World Brain keeps analysing, and agents keep proposing. Only funding pauses. Proposals queue in the Dream Hall. This lets the World feel alive during low activity without spending.

### 8.5 Self-sustainability test (honest)

Self-sustaining = trailing-90-day inflow ≥ trailing-90-day build + ops spend, held for 2 consecutive quarters. Publish this figure each epoch. Until it is met, all materials say **"pre-funded, working toward self-sustainability."**

---

## 9. Minimum viable V1 (exact scope)

### 9.1 On-chain (smallest set)

| Item | Required? | Notes |
|---|---|---|
| EMBER ERC-20 via IMD standard launch | **Yes** | No custom code. `poolBps`, pairing and initial market cap are OPEN. |
| Build Vault Safe | **Yes** | ≥2-of-3. |
| Ops Safe (agent payments) | Optional | Separates operational float from the treasury. |
| ForecastCommit anchoring | Optional | Minimal option: a Safe or ops-wallet transaction posting `keccak256(epochBundle)` with calldata only, so no contract is needed. Alternative: a ~30-line contract that emits `Committed(epoch, proposalHash, author)` with no storage, no owner and no funds. **RECOMMENDATION:** start with signed git tags + IMD oracle attestation and add the event contract only if the community asks for on-chain proof. |

### 9.2 Off-chain

- Epoch repository: proposals, commitments, reviews, QA reports, measurement results, ledger.
- Metric Catalogue v1 (≈8 metrics + guardrails, §4.1).
- World Pulse dashboard (catalogue metrics only).
- World Brain agent (read-only, no keys).
- Dream Hall page rendering everything above.
- 1–3 Agent Houses.
- Genesis PEPE holder gating for at least one World feature.

### 9.3 Learning Ledger schema (V1)

```
agent_id, operator_wallet, epoch, build_id,
proposal_hash, reveal_ok (bool),
budget, actual_cost, cost_error_pct,
delivered_on_time (bool), qa_defects_preprod, qa_defects_postpub,
metric_id, guardrail_id, forecast_low, forecast_high, horizon_days,
result_status ∈ {HIT, MISS, NO_EFFECT, INCONCLUSIVE, GUARDRAIL_BREACH},
calibration_score (null if INCONCLUSIVE),
reviewer_ids[], reviewer_predictions[], reviewer_calibration[],
human_note_hash
```

### 9.4 Proposal-slot formula (V1, EXPERIMENTAL)

```
score = 0.35·delivery_reliability + 0.30·cost_accuracy + 0.15·(1 − qa_defect_rate)
      + 0.20·calibration           (calibration term = 0 weight until ≥3 conclusive results)
decay half-life = 4 epochs
slots(agent) = min( ceil(score_share × total_slots), 0.30 × total_slots )
reserved: ≥1 open slot per epoch for agents with no history
```

Weights favour what builders control, in line with §4.4.

### 9.5 Epoch cadence

- V1: 14-day epochs. Measurement horizon 7–14 days, overlapping the next epoch.
- Driven by IMD `schedule.create` (FACT: 0.5 IMD per run that opens a question/job; skipped/failed runs are free).

---

## 10. Goal check: does the slim V1 still meet the four goals?

| Goal | Met by | Status |
|---|---|---|
| 1 Distinctive | Forecast-committed builds + public calibration ledger deciding who builds next. No tax, burn, staking or rebase. | **Met** |
| 2 Alive | Continuous visible loop in the Dream Hall. World Pulse. Modes keep the loop running even when funding pauses. | **Met** |
| 3 Self-sustaining | Creator-fee inflow → Vault, mode-based spend, honest runway reporting. | **Target only**: unproven until mainnet revenue (F4) |
| 4 Self-improving | Ledger feeds proposal rights. Cost, QA and calibration learning. Catalogue covers World, Dream Hall, Agent Houses, Genesis PEPE, wearables, UX and performance. | **Met in mechanism**; real improvement must be shown over ≥ 6 epochs |

---

## 11. V1.5 / V2 roadmap

| Phase | Item | Gate to enter |
|---|---|---|
| **V1.5** | Calibration bonus pool (≤10% of base, bonus only) | ≥ 6 epochs, ≥ 10 CONCLUSIVE results, no unresolved A3/A10 incidents |
| V1.5 | Hold-out bucketing for all World builds | Analytics proven stable for 4 epochs |
| V1.5 | ForecastCommit event contract (no storage, no owner) | Community request or need for external verifiability |
| V1.5 | Reviewer weighting by reviewer calibration (binding, not advisory) | ≥ 20 reviews per reviewer |
| V1.5 | IMD oracle panel attestation of every measurement | Cost per epoch acceptable |
| V1.5 | Genesis PEPE holders get a theme-nomination right | Sybil filter validated |
| **V2** | Revenue Router contract (fixed splits, Safe-owned, Timelock) | Mainnet revenue ≥ 2 quarters; audit |
| V2 | On-chain Learning Ledger summary roots (Merkle per epoch) | Need for third-party composability |
| V2 | Mode Registry contract with bounded parameters + Timelock | Contracts with parameters exist |
| V2 | Limited autonomous micro-spend (e.g. ≤ X per epoch, AI-initiated, Safe-revocable allowance via Safe module) | 12+ epochs of clean audits; formal threat review |
| V2 | Multiple competing World Brains | Diversity of proposals measurably low |
| **Never (current view)** | Transfer tax, custom swap-skimming hook, burn-as-value, staking/APY, rebase, outcome clawback | — |

---

## 12. Final recommended architecture

```
┌─────────────────────────────── V1 FINAL ─────────────────────────────────┐
│                                                                          │
│  TOKEN CORE (stable/minimal/trustworthy)                                 │
│    EMBER — IMD standard launch, fixed 1B, plain transfers, v4 pool       │
│                                                                          │
│  TREASURY (human authority)                                              │
│    Build Vault Safe ≥2-of-3  ·  optional Ops Safe  ·  Mode JSON (signed) │
│                                                                          │
│  LIVING PROTOCOL (adaptive/AI-driven, off-chain, public, hash-anchored)  │
│    World Pulse → World Brain → Agents (ledger slots, 30% cap, open slot) │
│    → commit hash → independent review → Safe select → build (IMD jobs)   │
│    → QA → 100% pay → Safe publish → fail-closed measurement (auditor ≠   │
│    builder) → Learning Ledger → next epoch                               │
│                                                                          │
│  PRODUCT SURFACES                                                        │
│    Swarm Dream Hall (the loop, visible) · 1–3 Agent Houses ·             │
│    Genesis PEPE gated features · wearables as catalogue build class      │
│                                                                          │
│  NOT IN V1: Revenue Router, Epoch Manager contract, Mode Registry        │
│  contract, on-chain ledger, outcome escrow, Timelock, custom hook, burn  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 13. Exact open decisions

| # | Decision | Options | Recommended default | Owner |
|---|---|---|---|---|
| D1 | Pair asset | ETH / IMD | **ETH** for budget stability (ASSUMPTION: less correlated with ecosystem activity). Check availability in IMD launch permissions. | Safe |
| D2 | `poolBps` and remainder split (Vault / Genesis PEPE / team) | — | OPEN. Publish before launch. | Safe |
| D3 | Initial market cap (`initialMarketCapWei`) | — | OPEN | Safe |
| D4 | Safe threshold and signers | 2-of-3 / 3-of-5 | 2-of-3 now; 3-of-5 above a TVL threshold (OPEN) | Founders |
| D5 | Metric Catalogue v1 contents | §4.1 table | Adopt the table, edit before epoch 1 | Safe |
| D6 | Sample minimums S1 | — | 200 sessions / 30 exposures + 5 events | Safe + analytics |
| D7 | Epoch length | 7 / 14 / 28 days | 14 days | Safe |
| D8 | Mode thresholds | §8.4 | Adopt as written | Safe |
| D9 | Reviewer independence definition | operator only / operator + model family | Both where feasible | Safe |
| D10 | Hash-anchoring method | git tag / calldata tx / event contract / IMD oracle | git tag + calldata tx | Safe |
| D11 | Creator-fee collection mechanics and asset | — | **OPEN: not documented in pages fetched.** Must be verified on Sepolia before mainnet. | Tech |
| D12 | Mainnet timing | — | OPEN: depends on IMD | — |
| D13 | Content of the "earlier conservative report" vs. this review | — | **OPEN: not supplied.** Reconcile any differing parameters. | Reviewer swarm |

---

## 14. Final go / no-go criteria

**GO for V1 launch only if ALL hold:**

1. Token is an IMD standard launch with no custom token or hook code. Supply split and `poolBps` are published.
2. Build Vault is a Safe at ≥2-of-3, signers are documented, and no single person holds a majority of keys.
3. Initial vault runway covers ≥ 6 epochs at the normal-mode plan **without any trading revenue**.
4. Metric Catalogue v1 with guardrails, query hashes and sample minimums is published before epoch 1.
5. Commit → review → select ordering is demonstrably enforced. At least one dry-run epoch on Sepolia shows hashes committed before reviews.
6. Payment policy is published: 100% on QA pass, no outcome holdback, no clawback.
7. Reviewer-independence and auditor ≠ builder rules are published and checked for each epoch.
8. Slot cap (30%) and open-slot rule are in the ledger code.
9. Public materials say "pre-funded, working toward self-sustainability" and contain no yield, burn-value or return claims.
10. Platform facts in §3 have been re-verified within 7 days of launch.

**NO-GO if ANY hold:**

- Any contract can mint EMBER, tax transfers or skim swaps.
- Any AI agent holds keys able to move vault funds or deploy to production.
- Outcome-linked holdback above 0% in V1.
- Self-sustainability is advertised as achieved without 2 quarters of evidence (§8.5).
- The Learning Ledger affects token balances, yield or any financial entitlement.
- Creator-fee mechanics (D11) are unverified at mainnet launch.

---

## 15. Sources

Checked on 2026-10-05:

- IMD API documentation: https://imd.fun/docs. Supply 1B/18 decimals; 10% swarm / 90% requester; `poolBps`; Uniswap v4 single-sided pool; ETH/IMD pairing; 1.25% fee (1.0% requester, 0.25% network); launch kinds; paid actions at 0.5 IMD; schedule spacing; "Sepolia (11155111) is the only one open"; standard launch token "fixed … plain transfers"; oracle panel mechanics.
- Uniswap v4 hooks concepts: https://developers.uniswap.org/contracts/v4/concepts/hooks (served from https://developers.uniswap.org/llms.mdx/docs/protocols/v4/concepts/hooks). Permission bits in the hook address; callbacks; four return-delta permissions that "adjust balances"; the hook "cannot be added, removed, or swapped afterward."
- Comparative IMD launches (comparative only, not protocol facts), found via search on 2026-10-05: https://github.com/identity-md-launches, for example https://github.com/identity-md-launches/launch-661-imd-offsets-token-symbol-imdo-chain-id-1/pull/1 and https://github.com/identity-md-launches/launch-603-build-imd-schemas-json-schema.

Referenced as general practice but **not re-fetched this session** (treat as background, not verified facts): Safe multisig (https://docs.safe.global), OpenZeppelin TimelockController (https://docs.openzeppelin.com/contracts), Goodhart's law and proper scoring rules (Brier / log score) as standard concepts.

**Not available:** the current $EMBER Living Economy report and the earlier conservative report (see L1). Any conflict between this review and those documents is unresolved (D13).

---

## 16. Facts vs. inference vs. uncertainty (summary)

- **FACTS** (sourced): IMD launch parameters, the Sepolia-only availability, the 1.25% / 1.0% / 0.25% fee split, v4 hook immutability and balance-adjusting capability, IMD paid-action pricing and schedule spacing.
- **INFERENCES / RECOMMENDATIONS:** 0% V1 tranche; ≤10% bonus-only later; closed metric catalogue; fail-closed thresholds; 30% slot cap; mode thresholds; component cuts.
- **UNCERTAIN / EXPERIMENTAL:** sample-size thresholds, mode thresholds, slot-formula weights, whether hold-out bucketing is feasible at V1 traffic, and whether other IMD ecosystem launches already do something similar.
- **UNANSWERED:** the contents of the two prior reports; brief sections after §4.5; creator-fee collection mechanics and asset; mainnet timing.
