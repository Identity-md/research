# IMD Viral Wars — revised feasibility assessment and specification (v2)

**Revision date:** 6 October 2026, about 23:30 UTC.
**Supersedes:** [report v1](https://github.com/Identity-md/research/blob/main/jobs/898e7e39-1bab-4e6d-ad27-50bae407d6aa/files/artifacts/report.md). An archived copy is in `evidence/original-report-v1.md`, SHA-256 `a5e9276f…e98745`.
**IMD control plane observed:** commit `7471272e37c4fbd51b40f02c0659da1d2cf5aa35` (`GET https://api.imd.fun/version`). The raw responses this report relies on are archived under `evidence/` with `SHA256SUMS`.

Every substantive statement carries one of these labels:

- **[Fact]** — stated by a cited primary source, or observed directly in a live API response on the revision date.
- **[Inference]** — my reasoning from facts.
- **[Assumption]** — a planning input that has not been tested. Change it freely.
- **[Proposal]** — a design choice.
- **[Unknown]** — an open question that has to be resolved before the dependent step.

Prices, volumes and audience numbers are illustrations, not forecasts.

---

## 0. Correction log (concise)

| # | v1 statement | Finding | v2 correction | Basis |
|---|---|---|---|---|
| 1 | Break-even `V = 1,950 / (30 × 0.002) = $325,000/day`. Sensitivity: $650,000/day at 0.5% and $162,500/day at 2%. | Arithmetic error by a factor of 10. `30 × 0.01 × 0.20 = 0.06`, and `1,950 / 0.06 = 32,500`. | **$32,500/day** at 1%, **$65,000/day** at 0.5%, **$16,250/day** at 2%. The v1 scenario table and the $6,500/day all-tax figure were correct. Cash, IMD fees and liquidity are now separate budgets (§4). | Recalculated (§4.3) |
| 2 | “One 30-run schedule = 15 IMD” **plus** “30 daily oracle requests … ≈16.5 IMD”, total 31.5 IMD. Only 2 production jobs. | (a) A schedule's runs are prepaid at 0.5 IMD per run, and each run *is* the job or question it opens. Adding a schedule to the same 30 openings counts them twice. (b) The 60 video jobs were left out of the IMD budget entirely. (c) Nothing supported the $15 per video. | The budget is rebuilt from a 109-action inventory: **54.5 IMD**, reserves included. One video equals one job. A schedule appears only as an *alternative* to per-day jobs, never in addition to them. The $15 is broken down and labelled as an assumption (§4.1–4.2). | `schedule.create` dry-run: 30 runs = 15 IMD, “only a run that opens a question or a job spends one” [Fact] |
| 3 | “Days 15–30 — run 27 competitive rounds.” | Days 15–30 are 16 days. With 48-hour windows plus attestation and disputes, they hold at most 13 fully settled rounds. | Setup (14 days, including 3 calibration rounds) is now separate from a 30-day season. The season has **27 rounds, published on season days 1–27**, and the last dispute closes on day 30 (§3). | Calendar arithmetic |
| 4 | Closing snapshot at 12:00 “then repeated at 12:30 and 13:00 if the API is stale.” Hashes treated as evidence of the count. | A read taken after the cutoff cannot recover the value at the cutoff, because the counter is mutable. A hash proves the bytes are intact. It does not prove where they came from or that they are true. | Exact cutoff, a ±15-minute tolerance, a same-request pair rule, two collectors, fallbacks that never reconstruct a value from a later read, and an explicit statement of what hashes do and do not prove (§2). | YouTube `videos`/`batchGetStats` docs [Fact] |
| 5 | TikTok is unsuitable because of “substantial data lag” (citing the Research API FAQ). | The 48-hour and 10-day lag in the FAQ is specific to the Research API's archived dataset. The same FAQ contrasts it with a per-user API that serves online data. The authorized-account Display API `/v2/video/query/` is a different endpoint. | TikTok is reassessed on the Display API. Its freshness is an **[Unknown]** to be measured, not assumed. The real blockers are the Direct Post audit and the lack of a documented freshness guarantee (§5). | TikTok Display API and Research FAQ [Fact] |
| 6 | “1% buy and 1% sell transfer tax only when the recipient is a recognized pool.” | A recipient-is-pool condition taxes only sells. On Uniswap v4 a pool is not an address: every pool's tokens sit in the singleton `PoolManager`. IMD project and hook launches mint tokens with **plain transfers only**. A fee-on-transfer token also conflicts with v4 `settle()` accounting. | Use the IMD-native `univ4_hook` launch fee. It is 1.25% of **every trade**, buys and sells alike, with 1% to the paying wallet (the treasury). An optional extra hook fee can be added only after review. A transfer tax is not recommended (§6). | IMD launch dry-run; v4-core source [Fact] |
| 7 | “One-wallet-one-vote … capped at 10 votes per address.” | The two rules contradict each other. One-wallet-one-vote can be defeated by splitting holdings across wallets. | Simulation: one verified account, one vote, labelled as not Sybil-resistant. Token pilot: **linear weight by minimum balance over 7 daily snapshots**, a rule that gives no advantage for splitting. The trade-off with large holders is stated openly (§7). | Design analysis [Inference] |
| 8 | “Simulated burn” pilot; real burns “after data gates”. Gates were partly qualitative. | v1 did not say what a simulation can and cannot validate, and its gates did not cover token economics. | Four phases with measurable gates (§8). The product stays intact: RED/IMD and BLUE/IMD, community-directed videos, and a shared fund that buys and burns the winner's token. | — |
| 9 | Attestation expiry of 24 hours plus a 24-hour dispute window. | An attestation would expire at the moment the dispute window closes, leaving no time to execute. | `validForSeconds = 172,800` (48 hours). Settlement executes only after the dispute window closes (§2.6). | IMD oracle body limits [Fact] |
| 10 | Equal-sided “$2,000 IMD liquidity per pool”. | IMD launches seed the pool **single-sided in the launch token** and open at a policy market cap of 2,500 IMD for IMD pairs. | No IMD inventory is needed to open the pools. The new risk is very thin depth at opening (§4.4). | Launch dry-run and policy v29 [Fact] |
| 11 | `videos.insert` costs “one unit”. YouTube Analytics is usable for scoring. | Google's quota pages contradict each other (1,600 points vs. 1 call in a 100/day bucket). Analytics data arrives 48–72 hours late. | Quota is treated as an **[Unknown]** to confirm in the Cloud console. Analytics is used only for a delayed audit, never for scoring (§2.2). | YouTube docs [Fact] |

---

## 1. Executive recommendation (updated)

**Proceed with an off-chain, YouTube-first simulation season now. Make a token-enabled pilot conditional on measurable gates. Do not present the treasury as self-funding.**

1. **The product concept is buildable with IMD today.** **[Fact]** `create-video` is in the live skill catalog. Its record shows 57 accepted runs out of 65 attempts. 672 of 715 connected workers advertise it. A sample job delivered a 10.2 MB MP4 in about 10 minutes for one 0.5 IMD job (`evidence/imd-create-video-job-result-sample.json`). Oracle panels with EIP-712 attestations and paid schedules are live.
2. **Two IMD-paired team tokens with a fee on both buys and sells are available natively.** **[Fact]** A free `POST /requests/check` for a `univ4_hook` launch on Ethereum mainnet paired with IMD returned no chain blocker. It reported a fixed 1B-supply token with plain transfers, a pool paired with IMD that opens at a 2,500 IMD market cap, and “1.25% of every trade: 1% to you, 0.25% to IMD”. That fee replaces v1's transfer tax.
3. **Self-funding is unlikely at launch scale.** **[Inference]** Funding the $1,950 cash budget from a 20% operating share of a 1% fee takes **$32,500/day** of combined volume. Including the season's IMD fees at the 6 October quote, it takes about $38,700/day. Each pool opens at a 2,500 IMD market cap, about $22,900 at ≈$9.14/IMD (DexScreener, 6 Oct 2026, secondary source). That threshold is more than each token's whole opening valuation traded every day. Plan for external funding and treat fee income as upside.
4. **Measurement is the binding constraint, not video production.** The score is a delta in a mutable, autoplay-inclusive platform counter, captured at exact cutoffs by two collectors (§2). Agreement among oracle panel members certifies their review of the archived evidence. It does not certify organic viewers.
5. **Budget (planning envelope, setup plus one 30-day season):**
   - **54.5 IMD** in IMD fees, including reserves. At the 6 October quote that is about $500, but price it at the live quote.
   - **$1,950 assumed cash budget**, unchanged from v1 and now itemised and labelled.
   - **No liquidity inventory**, because launches are single-sided.
   - **1 IMD** later, for two token launches (plus 1 IMD for Sepolia rehearsals), only if Gate C passes.

---

## 2. Measurement specification (exact cutoff)

### 2.1 Metric

- **[Fact]** YouTube `videos.statistics.viewCount` is a public counter. From **24 August 2026** it counts a view “the moment a video begins to play (includes autoplay, hold the pointer over, and click/tap to play)” ([videos resource](https://developers.google.com/youtube/v3/docs/videos), [revision history, 27 Aug 2026](https://developers.google.com/youtube/v3/revision_history)). Since 31 March 2025, Shorts views have counted replays with no minimum watch time.
- **[Fact]** `videos.batchGetStats` (added 3 June 2026) returns `viewCount` for a comma-separated list of IDs in one response. It needs no OAuth for public videos and costs 1 unit from its own 10,000/day bucket ([reference](https://developers.google.com/youtube/v3/docs/videos/batchGetStats)).
- **[Proposal]** The score is `S = viewCount(close) − viewCount(open)` per video, label “reported YouTube plays”. It is not reported as unique viewers or organic attention. **[Inference]** The autoplay-inclusive definition makes the counter easier to inflate than v1 assumed.
- **[Fact]** YouTube Analytics `engagedViews` keeps the older methodology. Analytics data, however, “typically introduces a latency of 48 to 72 hours” ([data model](https://developers.google.com/youtube/analytics/data_model)). **[Proposal]** Use it only for an audit report published after the round, never for settlement.

### 2.2 Equal start: scheduled publishing

- **[Proposal]** Both videos are uploaded `private` with `status.publishAt = T_open`. **[Fact]** `publishAt` can be set only when the video is private ([videos resource](https://developers.google.com/youtube/v3/docs/videos)). The goal is that both counters start near zero at the same instant, so the opening snapshot is a check rather than a correction.
- **[Fact]** API uploads from unverified projects created after 28 July 2020 are locked private until a compliance audit ([videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert)). **[Proposal]** Fallback: the channel owner uploads and schedules the video in YouTube Studio. Collectors need only an API key, because reads of public videos do not depend on the audit.
- **[Unknown]** How precisely YouTube flips `publishAt` to public. Measure this during calibration.
- **[Unknown]** Upload quota. Google's [quota page](https://developers.google.com/youtube/v3/determine_quota_cost) states both 1,600 points per `videos.insert` and a separate 100-calls/day bucket at 1 per call. Either way, 2 uploads a day fits. Confirm in the Cloud console.

### 2.3 Timeline of one round (all times UTC, publication day `d`)

| Event | Time | Rule |
|---|---|---|
| Prompt and script frozen | d−1 12:00 | The approved script's hash is published. Video jobs open. |
| Upload complete (private, scheduled) | ≤ d 10:00 | Missed → the team's pre-produced reserve video is used. Still missed by d 11:30 → forfeit rules apply. |
| **T_open** | **d 12:00:00** | Scheduled publication. |
| Opening snapshot | T_open + 15 min | One `batchGetStats` request containing **both** IDs. Both must be `public`. Opening counts are recorded (expected ≈0). |
| Public-status grace | ≤ T_open + 15 min | A video still not public: platform-side → no contest. Team-side → forfeit, exhibition only, no burn. |
| **T_close** | **d+2 12:00:00** | End of the 48-hour window. |
| Closing reads | Every 5 min from T_close − 30 min to T_close + 30 min | Both collectors run independently. Every read is one request for both IDs. |
| Evidence commit | ≤ T_close + 45 min | Hashes posted to the dashboard log, then embedded in the oracle question (§2.6). |
| Oracle opened | ≤ T_close + 60 min | One `oracle.request` per round. |
| Attestation deadline | T_close + 6 h (d+2 18:00) | Missed → “unverifiable, no settlement”. |
| Dispute window | 24 h after attestation is published (closes ≤ d+3 18:00) | — |
| Settlement (simulated or real) | After dispute close, ≤ d+3 20:00 | Attestation must still be valid. |

### 2.4 Canonical closing value and fallbacks

1. **Primary.** Use the first read by collector A whose response `Date` header lies in **[T_close, T_close + 15 min]**. Both IDs must be in the same response.
2. **Fallback 1.** If A has no such read, use the first read by collector B in the same interval, under the same rule.
3. **Fallback 2.** If neither collector has a read after the cutoff in that interval, use the **last read in [T_close − 15 min, T_close)** from A, then from B, still with both IDs in one response. Both teams are measured at the same instant, so the window shortens by up to 15 minutes for both teams equally.
4. **Otherwise:** “unverifiable — no settlement.” **No value at T_close is ever inferred from a later read.** **[Inference]** Counters can fall when spam views are filtered out, and they normally rise, so a later read is neither an upper nor a lower bound on the earlier value.
5. **Cross-check.** If A and B both have reads in the primary interval, their implied winners must match. Their totals must also agree within 2% plus 50 plays **[Assumption: tolerance to calibrate]**. A mismatch sends the round to dispute.
6. **Ineligible outcomes:** a negative delta, a video deleted or made private before T_close, or a change of channel ownership.
7. **Draw:** |S_red − S_blue| ≤ max(1% of the larger score, 100). A draw means no burn.

### 2.5 Evidence provenance, and what hashes prove

Each read stores:
- the raw response bytes,
- the request URL with the key redacted,
- request and response timestamps,
- the HTTP `Date` header,
- the response `etag`,
- the collector ID, host and code commit,
- the video IDs, `snippet.publishTime` and `summary.failedVideoIds`.

Each read's SHA-256 is appended to a public, hash-chained log as soon as the read happens. The per-round Merkle root goes into the oracle question.

| A hash of the raw response **proves** | It does **not** prove |
|---|---|
| The archived bytes have not changed since the hash was published. | That the bytes came from Google's servers. A collector can fabricate a response and hash it. |
| Combined with a third-party timestamp, the bytes existed no later than that time. Third-party timestamps here: the oracle request's IMD `createdAt` [Inference], or an on-chain commit if one is used. | That the read happened at the stated time. The stated time comes from the collector. Only the publish time sets an upper bound. |
| A panel member can recompute the score from exactly the same bytes. | That the count is correct, organic, free of bots, or final. YouTube may revise it. |
| | Anything about an earlier moment, if the read was taken later. |

**[Proposal]** Provenance therefore rests on four things:
- two independently operated collectors (different operators and infrastructure),
- immediate publication of hashes,
- a live sanity read by panel members at attestation time (the current count should not be far *below* the claimed closing count),
- an option to add TLS-notarised reads (for example TLSNotary or zkTLS). **[Unknown, untested]**

### 2.6 Oracle request per round

- **[Fact]** These capabilities are documented ([IMD docs, Oracle body](https://imd.fun/docs/)):
  - `evidence: "panel"` for off-chain sources;
  - `guards.sources` and `minSources` to restrict where evidence may come from;
  - panel size 5 to 100, with a quorum of matching answers;
  - `validForSeconds` from 60 to 2,592,000;
  - answer types `bool`, `address`, `bytes32`, `uint256`, `address[]` and `bytes32[]`.
- **[Fact]** Payment buys the question, not an answer. A panel that disagrees produces no answer.

**[Proposal]** One request per round:
- `answerType: "uint256"`, encoded 0 = draw, 1 = RED, 2 = BLUE, 3 = no contest.
- `panelSize 5`, `quorum 4`, `validForSeconds 172800`.
- `guards.sources`: the evidence archive prefix plus `https://www.googleapis.com/youtube/v3/`, with `minSources 2`.
- `definitions` pin the rules hash, both video IDs, both channel IDs, T_open, T_close, the evidence Merkle root and the §2.4 algorithm.
- The consumer contract also requires `agreed ≥ quorum`.

**[Inference]** Panel members can verify the hashes, IDs, ownership, publication times and the arithmetic, and run the live sanity read. They cannot independently re-observe the past counter.

---

## 3. Calendar (setup separated from competition)

### 3.1 Setup — days S1–S14 (no competition)

| Days | Work | Exit |
|---|---|---|
| S1–S5 | Create channels with equal starting conditions and disclosed baselines. Set up the Google Cloud project, apply for the audit, write the moderation policy and freeze the evidence schema. | Upload path chosen: API, or Studio as the fallback. |
| S3–S8 | IMD build jobs (§4.1, rows A1–A4): research panel, round registry and attestation consumer (**source and tests only, not deployed**), collector/publisher, dashboard and vote site. | Code delivered and an independent review passed. |
| S9, S10, S11 | **Calibration rounds C1–C3** published at 12:00. | — |
| S11, S12, S13 | C1–C3 closing windows end at 12:00 and attestations follow by 18:00. A deliberate negative-test oracle request is also run. | — |
| S12–S14 18:00 | C1–C3 dispute windows close. | **Gate A** review on S14 evening (§8). |

### 3.2 Competition season — days D1–D30 (D1 = S15)

- Rounds R1–R27 are published on D1–D27. Round R*n* closes on D(*n*+2) at 12:00 and its dispute closes on D(*n*+3) at 18:00.
- **R27 is published on D27, closes on D29 and finalises on D30.** This is the maximum number of rounds whose dispute windows close inside 30 days.
- D28–D30 have no scored publications. Unscored exhibition content is optional and not budgeted.
- **[Inference]** In steady state, up to three rounds are open at once: two observation windows and one dispute. Back-to-back seasons would overlap rather than pause.
- Weekly vote **[Proposal]**:
  - Mon 00:00 – Wed 00:00: proposals.
  - Wed: moderation, with published reasons.
  - Thu 00:00 – Sat 12:00: voting.
  - The winning prompt drives the following Mon–Sun rounds. Daily scripts are derived from it and frozen at d−1 12:00.
- **Total program:** 44 calendar days. The v1 framing of “30 days containing setup, calibration and 27 rounds” is withdrawn.

---

## 4. Economics

### 4.1 IMD job inventory

**[Fact]** Every paid action costs 0.5 IMD. A schedule costs 0.5 IMD per run, paid up front, and each run spends one prepaid unit when it opens its job or question. Skipped or failed runs cost nothing, and unused runs are not refunded (capabilities `pricedPer`; schedule dry-run, `evidence/imd-check-schedule-30-runs.json`).

| ID | Item | Action | Count | IMD |
|---|---|---|---:|---:|
| A1 | Research panel: YouTube audit/publication and TikTok Display API terms | `job.open` (template `research`) | 1 | 0.5 |
| A2 | Round registry and attestation consumer: source, tests and independent review in one job (`build-contract-project` → `adversarial-review`) | `job.open` | 1 | 0.5 |
| A3 | Collector A/B and publisher adapter with replay fixtures | `job.open` | 1 | 0.5 |
| A4 | Dashboard, evidence browser and vote site (`build-website`, IPFS) | `job.open` | 1 | 0.5 |
| A5 | Fix-up continuations after review | `job.continue` | 2 | 1.0 |
| C1 | Calibration videos (3 rounds × 2 teams) | `job.open` (`create-video`) | 6 | 3.0 |
| C2 | Calibration oracle requests | `oracle.request` | 3 | 1.5 |
| C3 | Negative test: deliberately mismatched evidence must not attest | `oracle.request` | 1 | 0.5 |
| **Setup subtotal** | | | **16** | **8.0** |
| S1 | Season videos (27 rounds × 2 teams) | `job.open` (`create-video`) | 54 | 27.0 |
| S2 | Season oracle requests (1 per round, covering both videos) | `oracle.request` | 27 | 13.5 |
| **Season subtotal** | | | **81** | **40.5** |
| R1 | Video retries and reserve videos (≈10% of 60) **[Assumption]** | `job.open` | 6 | 3.0 |
| R2 | Oracle re-asks after disagreement or a missed deadline (≈20% of 30) **[Assumption]** | `oracle.request` | 6 | 3.0 |
| **Total** | | | **109** | **54.5** |

- **No schedules in the baseline.** **[Fact]** A schedule's input is “checked once and frozen”, and `continue` restarts from the schedule's own last job rather than from new external input. **[Inference]** A frozen schedule cannot carry each day's voted script or each round's video IDs. If a schedule is used anyway, for example a frozen job input that tells the worker to fetch “today's approved script from URL X” (**[Unknown]**, and it weakens reproducibility), then 2 schedules × 27 runs = 27 IMD **replace** row S1. They are never added to it.
- **One video per job.** **[Fact]** A job may declare up to 32 named outputs and up to 6 steps, and the price does not depend on output count. Grouping both teams' videos in one job would therefore save 13.5 IMD per season. **[Proposal]** Keep them separate anyway:
  - each team's production is independent and attributable;
  - one failure does not void both entries;
  - the per-team budgets stay identical and auditable.
- **Liquidity.** None is bought in IMD. Pools are seeded single-sided (§4.4).
- **Phase C/D only:** 2 Sepolia rehearsal launches (1 IMD) and 2 mainnet launches (1 IMD). A custom hook adds build and audit risk but no extra listed fee beyond `launch.open`. **[Unknown]**

### 4.2 Assumed cash budget (USD, separate from IMD)

| Line | v1 | v2 | What it buys | Status |
|---|---:|---:|---|---|
| Per-video human costs: 60 scored videos × $15 | $900 | $900 | **Not generation**, which the 0.5 IMD job already covers. It buys about 15 minutes of human review, approval and scheduling at $40/h ($10), plus a $5 allowance for licensed audio, fonts or stock and caption fixes. | **[Assumption]** v1 gave no basis. It is $0 with volunteer operators and only generated assets, and too low if human editing is needed. |
| Moderation and community | $300 | $300 | Weekly shortlist moderation, published reasons, dispute handling | [Assumption] |
| Integration operations | $250 | $250 | Hosting collectors A and B on separate infrastructure, OAuth setup, incident time. The code itself is IMD jobs A2–A4. | [Assumption] |
| Storage and monitoring | $75 | $75 | Evidence archive and uptime alerts | [Assumption] |
| Gas reserve | $100 | $100 | Not needed in simulation. Covers Sepolia and mainnet executor transactions in Phase C/D. | [Assumption] |
| Contingency 20% | $325 | $325 | — | — |
| **Total cash** | **$1,950** | **$1,950** | | |

IMD fees (54.5 IMD) are **in addition** to this cash. **[Fact, time-sensitive]** At ≈$9.14/IMD on 6 October 2026 ([DexScreener](https://dexscreener.com/ethereum), a secondary aggregator), 54.5 IMD is about $498 and the season-only 40.5 IMD is about $370. Each round costs 1.5 IMD, about $13.70, in IMD fees.

### 4.3 Recalculated sustainability model

Definitions:
- `V` = combined daily volume across both pools.
- `f` = fee share paid to the treasury.
- `o` = operating share.
- Over 30 days: income `30·f·V`; operations `30·f·o·V`; burn `30·f·(1−o)·V`.

Base case `f = 1%`, which is the paying-wallet share of IMD's native 1.25% fee (§6), and `o = 20%`.

| Scenario | V/day | 30-day volume | Treasury fee | Ops (20%) | Burn (80%) | Gap vs $1,950 cash |
|---|---:|---:|---:|---:|---:|---:|
| Low | $2,000 | $60,000 | $600 | $120 | $480 | −$1,830 |
| Medium | $20,000 | $600,000 | $6,000 | $1,200 | $4,800 | −$750 |
| **Break-even** | **$32,500** | $975,000 | $9,750 | $1,950 | $7,800 | $0 |
| High | $100,000 | $3,000,000 | $30,000 | $6,000 | $24,000 | +$4,050 |

Break-even calculations:

- **Cash only:** `V* = 1,950 / (30 × 0.01 × 0.20) = $32,500/day`. v1's $325,000 is corrected.
- **Sensitivity on `f`:**
  - 0.5% → `1,950 / (30 × 0.005 × 0.2) = $65,000/day`.
  - 2% → `$16,250/day`.
  - Under IMD's native launch, `f` is fixed at 1%. Raising it requires an extra hook fee (§6), which raises the trader's total cost to 1.25% plus the hook fee.
- **All fees to operations first:** `1,950 / (30 × 0.01) = $6,500/day`. This was correct in v1, but it would leave nothing for burns at that volume.
- **Cash plus season IMD fees** (40.5 IMD × $9.14 ≈ $370): `(1,950 + 370) / 0.06 ≈ $38,670/day`. Including setup and reserves (54.5 IMD): ≈ $40,800/day. **[Fact for arithmetic; Assumption for price]**
- **[Fact]** Fee income tracks volume linearly. A losing streak does not change total receipts, but it changes which token is bought.
- **[Inference]** A wash trader pays 1.25% per trade, of which 1% goes to the treasury and later to burns. Wash trading is therefore costly, but a large holder of a team's token could find it worthwhile if the burns it funds are worth more than the fees. Volume is not evidence of audience.

### 4.4 Liquidity and buyback limits

- **[Fact]** IMD launches seed a single-sided pool in the launch token at an IMD-denominated opening market cap of 2,500 IMD for IMD pairs (policy v29, mainnet `univ4_hook`; dry-run fact `token_pool`). 80% of supply goes to the pool by default, 10% to the swarm, and the rest to the paying wallet.
- **[Inference]** The IMD side of each pool starts near zero. Early buybacks therefore move price sharply, and the first sellers face no IMD depth until buyers arrive.
- **[Proposal]** Buyback rules:
  - cap each round's buyback at the smaller of the round's allocated budget and the trade size that moves the winner's spot price by ≤2%. Spot price can be measured with IMD's `univ4-spot` oracle recipe, a median over up to 61 blocks [Fact: recipe exists];
  - split the buyback into ≥4 orders spread over ≥1 hour;
  - carry any excess forward;
  - publish the fills.

### 4.5 Fees received in team tokens

- **[Unknown]** The currency of the 1% paying-wallet fee (input currency, IMD only, or both) and its claim path. Verify this on Sepolia.
- **[Proposal]** If fees arrive partly in RED or BLUE:
  - fees in the winner's own token are burned directly;
  - fees in the loser's token are held in escrow and burned when that team next wins;
  - fees in IMD fund operations (20%) and the winner's buyback (80%).
- This honours “all remaining funds buy-and-burn the winner” without selling the loser's token into its own pool.

---

## 5. TikTok reassessed (authorized-account API)

**Facts:**
- The **Display API** `/v2/video/query/` (scope `video.list`) takes an authorized user's token and up to 20 video IDs. It verifies that the videos belong to that user and returns fields including `view_count` (int64) and `create_time` ([Query Videos](https://developers.tiktok.com/doc/tiktok-api-v2-video-query), [Video Object](https://developers.tiktok.com/doc/tiktok-api-v2-video-object), both updated 24 Aug 2026). The default rate limit is 600 requests per minute ([rate limits](https://developers.tiktok.com/doc/tiktok-api-v2-rate-limit)).
- The **Research API** lag of “up to 48 hours” for new videos and “up to 10 days” for statistics is explained by TikTok as the research video query using **archived** data. The same FAQ contrasts this with a per-user endpoint that uses **online** data ([Research FAQ](https://developers.tiktok.com/doc/research-api-faq), updated 1 Sep 2026). Research access is also restricted to approved researchers and excludes creators and commercial users.
- **Direct Post:** “All content posted by unaudited clients will be restricted to private viewing mode” until an audit. Error codes include a per-user daily post cap and an active-publisher cap ([Direct Post](https://developers.tiktok.com/doc/content-posting-api-reference-direct-post)).

**Inference:** v1 applied the Research API's lag to a different API. No primary source documents how fresh Display API `view_count` is, in either direction.

**Status:**
- **[Unknown]** Display API freshness.
- **[Unknown]** Whether the Display API app needs TikTok app review before production use. This was not confirmed in the pages fetched.
- **[Unknown]** Whether Direct Post supports a scheduled publish time equivalent to YouTube's `publishAt`.

**[Proposal]** TikTok becomes a **separate league** after a 14-day freshness test, with no cross-platform sum. The test reads Display API `view_count` every 5 minutes for test videos and compares it with in-app counts at fixed times. TikTok passes if, at T_close, the Display API value is within 2% of the in-app value on ≥95% of reads. Posting can be manual by the creator until the Direct Post audit is granted.

---

## 6. Fee (“tax”) specification, corrected

**Why v1's rule fails:**
- **Direction.** A rule of “tax when recipient is a pool” taxes only transfers *into* the pool, which are sells. Buys are transfers *out of* the pool. **[Inference]**
- **What a pool is on v4.** **[Fact]** Uniswap v4 uses a singleton `PoolManager`. Pool state lives inside it, and no per-pool contract exists ([PoolManager](https://docs.uniswap.org/contracts/v4/concepts/PoolManager)). A rule keyed on the `PoolManager` address would hit every v4 interaction with the token, including liquidity adds and other pairs, not just “the RED/IMD pool”.
- **Settlement.** **[Fact]** `PoolManager._settle` credits `balanceAfter − balanceBefore` for the synced currency, and `unlock` reverts with `CurrencyNotSettled` if any delta stays open ([v4-core `PoolManager.sol` @ 46c6834](https://github.com/Uniswap/v4-core/blob/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/src/PoolManager.sol)). **[Inference]** A fee-on-transfer token underpays its settlement unless a custom router compensates, so standard routers revert.
- **IMD policy.** **[Fact]** On project and hook launches the token is fixed: “1,000,000,000 with 18 decimals and plain transfers”. The dry-run reports “Transfers: plain, with no fees, limits, pausing or minting” ([IMD docs, Job body: What a launch is](https://imd.fun/docs/); `evidence/imd-check-univ4hook-mainnet-imd.json`). A `custom_token` request describing a 1% buy/sell fee was not refused at the free check. Its only blocker was a required independent review step (`evidence/imd-check-custom-token-fee.json`). Admission after build and audit is **[Unknown]**.

**Corrected specification [Proposal]:**
1. Launch **RED** and **BLUE** as two `launch.open` requests with `onchain: "univ4_hook"`, `pairWith: "imd"` and `chainId: 1`. Both are paid from the **treasury multisig** so that it is the “paying wallet”. **[Unknown]** Whether x402/Permit2 payment works from a smart-contract (EIP-1271) wallet. Test on Sepolia first.
2. The fee is the pool's own: **1.25% on every swap, buy or sell; 1% to the treasury, 0.25% to IMD** [Fact: check output]. The tokens keep plain transfers, so wallet-to-wallet transfers are untaxed. That is the intended behaviour.
3. **Optional:** a hook fee on top, applied in `beforeSwap` with `beforeSwapReturnDelta`, which is direction-agnostic ([custom accounting](https://docs.uniswap.org/contracts/v4/guides/custom-accounting)). If used: a hard cap of 1%, a timelocked parameter, and the swarm's audit panel plus an outside review. **[Proposal: omit in the first pilot]**
4. Treasury split: 20% operations, 80% the winner's buyback and burn (§4.5). The executor accepts only a valid attestation whose dispute window has closed.

---

## 7. Voting rule, resolved

v1's two rules cannot both apply. The resolution differs by phase.

| Phase | Eligibility | Weight | Why |
|---|---|---|---|
| Simulation (no tokens) | One account per verified login (OAuth or email) and captcha, with a 7-day account age before the vote | 1 per account | Measures participation. Labelled **not Sybil-resistant** and suitable only because nothing financial depends on it. |
| Token pilot | A wallet holding the team's token. Excluded: `PoolManager`, LP positions, the treasury, the swarm distributor, the launch wallet and known contracts. A wallet holding both tokens may vote in both, each at that team's balance. | **Linear in `min(balance)` over 7 daily snapshot blocks** (the first block after 00:00 UTC on each of the 7 days before voting closes) | Splitting one balance across *k* wallets gives exactly the same total weight, so splitting gains nothing. The 7-day minimum makes flash loans and last-minute buying useless. |

Trade-offs and controls:
- **[Inference]** Any wallet-based rule that is concave or per-wallet, including one-wallet-one-vote, per-address caps and quadratic voting, rewards splitting. Resisting splitting under those rules needs proof of personhood, which is out of scope. Linear weighting resists splitting but gives large holders proportional control.
- **[Proposal]** Mitigations for large holders:
  - moderators shortlist the 3 candidates;
  - the safety and rights veto stays human;
  - concentration is published (the top-10 wallets' share of the vote).
- A per-wallet cap is deliberately **not** used, because a large holder can defeat it by splitting.

---

## 8. Simulation vs. token pilot, and gates

| Validated by the **simulation** (Phases A–B) | Requires a **token-enabled pilot** (Phases C–D) |
|---|---|
| Video production reliability, cost per video, moderation load | Real trading volume and fee income |
| Measurement path: cutoffs, collectors, evidence, disputes | Fee currency, claim path, buyback execution and slippage |
| Oracle panel agreement and attestation latency | Wash trading, front-running of predictable buybacks, MEV |
| Settlement logic against a simulated ledger | Holder behaviour, token-weighted vote capture, losing-team morale |
| Audience response and returning voters | Legal and regulatory treatment of buybacks and team tokens |

**Phases and measurable gates:**

- **Gate A (setup → simulation season), all required:**
  - 3/3 calibration rounds have both collectors reading within ±15 min of T_close;
  - 0 hash mismatches;
  - attestation within 6 hours on 3/3;
  - the negative test does not attest;
  - an outside reviewer reconstructs each round's result from archived evidence alone;
  - an upload path (API audited, or Studio fallback) is proven on both channels.
- **Gate B (simulation → Sepolia shadow), across 27 rounds:**
  - ≥24 rounds settle (win or draw, not no-contest);
  - ≥25 canonical closes come from the primary interval;
  - ≥90% of attestations are delivered within 6 hours;
  - 0 unresolved disputes;
  - actual cash per video ≤ $15 and IMD per round ≤ 1.75;
  - median 48-hour plays per video in the last 14 rounds ≥ **1,000** **[Assumption: sponsor sets this]**;
  - ≥50 eligible voters per weekly vote, with ≥25% returning the next week.
- **Gate C (Sepolia shadow → mainnet token pilot):**
  - contracts independently reviewed, with 0 open critical or high findings;
  - a 14-day Sepolia shadow in which the executor consumes real round attestations with 0 incorrect executions;
  - wrong signer, expired, replayed and pre-dispute settlements are all rejected;
  - free `/requests/check` shows no blockers for both launches;
  - the fee currency and claim path are confirmed on Sepolia;
  - multisig payment of `launch.open` is confirmed;
  - written legal review.
- **Gate D (continue real burns), stop conditions:**
  - 2 consecutive unverifiable rounds;
  - any evidence mismatch;
  - a platform warning or suspension;
  - a compromised key;
  - any buyback exceeding the price-impact cap;
  - ops share below 50% of run-rate costs for 14 days, unless the sponsor continues to fund externally.

---

## 9. Risks (re-ranked)

1. **The counter is not organic attention.** The autoplay-inclusive definition makes this worse than v1 assumed. Keep the language “reported plays”, use two collectors, and default to no burn.
2. **Collector honesty and provenance** (§2.5). Hashes do not prove where data came from.
3. **Thin opening liquidity** at a 2,500 IMD opening cap (§4.4).
4. **Platform access:** the YouTube upload audit, the TikTok Direct Post audit, and the unknown freshness of TikTok's Display API.
5. **Contract and key risk:** consumer, executor and multisig.
6. **Channel baseline advantage, rights takedowns and voter capture.**
7. **Live policy drift.** The IMD launch policy changed between 5 and 6 October: mainnet hook fee tiers went from `[500, 3000, 10000]` (v19) to `[12500]` (v29). Pin the policy version at quote time.
8. **Documentation inconsistencies.** The IMD docs prose says Sepolia is “the only one open … today” for launches, but live capabilities and the dry-run accept mainnet. Google's quota page contradicts itself on `videos.insert`. Treat live responses and dry-runs as authoritative, and re-check them before paying.

## 10. Unanswered questions

- Currency of the 1% paying-wallet fee, and its claim mechanics.
- Whether the treasury can pay over x402/Permit2 from a smart-contract wallet.
- Admission of a custom hook fee.
- Precision of YouTube `publishAt` and the true `videos.insert` quota.
- Display API freshness and whether app review is required.
- Whether a frozen schedule may read external daily scripts.
- Whether failed paid jobs consume their 0.5 IMD.
- Legal status of treasury buybacks.

## 11. Next IMD swarm tasks (ordered)

1. A1 research panel (§4.1).
2. A2 registry and consumer source with adversarial review, with no deployment.
3. A3 dual collectors with replay fixtures.
4. A4 dashboard and vote site.
5. Run calibration and Gate A.
6. Run the 27-round simulation season and Gate B.
7. Sepolia launch rehearsal and 14-day shadow, then Gate C.
8. Decide whether to run the mainnet token pilot.

## Primary sources (accessed 6 Oct 2026)

**IMD:**
- [API docs](https://imd.fun/docs/)
- [`/requests/capabilities`](https://api.imd.fun/requests/capabilities)
- [`/launch/policies`](https://api.imd.fun/launch/policies) (v29 univ4_hook mainnet; v17/v26 custom_token)
- [`/skills`](https://api.imd.fun/skills)
- `POST /requests/check` dry-runs (archived in `evidence/`)
- [sample create-video job](https://api.imd.fun/jobs/470bd512-e366-46ba-8bec-87efb7cdba7f/result)

**YouTube:**
- [videos resource](https://developers.google.com/youtube/v3/docs/videos) (updated 16 Sep 2026)
- [videos.batchGetStats](https://developers.google.com/youtube/v3/docs/videos/batchGetStats)
- [videos.insert](https://developers.google.com/youtube/v3/docs/videos/insert)
- [quota costs](https://developers.google.com/youtube/v3/determine_quota_cost)
- [quota and audits](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits)
- [Data API revision history](https://developers.google.com/youtube/v3/revision_history)
- [Analytics data model](https://developers.google.com/youtube/analytics/data_model)
- [Analytics revision history](https://developers.google.com/youtube/analytics/revision_history)

**TikTok:**
- [Display API overview](https://developers.tiktok.com/doc/display-api-overview)
- [Query Videos](https://developers.tiktok.com/doc/tiktok-api-v2-video-query)
- [Video Object](https://developers.tiktok.com/doc/tiktok-api-v2-video-object)
- [Rate limits](https://developers.tiktok.com/doc/tiktok-api-v2-rate-limit)
- [Research FAQ](https://developers.tiktok.com/doc/research-api-faq)
- [Direct Post reference](https://developers.tiktok.com/doc/content-posting-api-reference-direct-post)

**Uniswap:**
- [PoolManager concept](https://docs.uniswap.org/contracts/v4/concepts/PoolManager)
- [Flash accounting](https://docs.uniswap.org/contracts/v4/concepts/flash-accounting)
- [Custom accounting / hook fees](https://docs.uniswap.org/contracts/v4/guides/custom-accounting)
- [v4-core `PoolManager.sol` @ 46c6834](https://github.com/Uniswap/v4-core/blob/46c6834698c48bc4a463a86d8420f4eb1d7f3b75/src/PoolManager.sol)

**Market (secondary, time-sensitive):** DexScreener IMD pairs, ≈$9.14 on 6 Oct 2026.

*Limits: this is a desk review by a single contributor. No video was produced, no API credential was used, nothing was paid for or deployed, and no independent reviewer checked this revision.*
