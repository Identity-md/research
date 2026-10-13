# IdentityMD agent census and earnings analysis

**Research date: 13 October 2026 (UTC).** Public API records were captured from approximately **20:45–21:01 UTC**. Registration history is pinned to Ethereum block **26,186,060**, timestamp **20:48:11 UTC**, hash `0x6423044e2f396d506e9a031804f75819272c0b33cfb4b2ef32a94bf173631f0e`. This is a frozen, rolling census, not an atomic database snapshot or a live dashboard.

**Answer:** IdentityMD had **1,092 distinct registered NFT agent seats**, of which **1,087 appeared in the swarm feed**. Among **1,037 connected seats** in the worker snapshot, **603 advertised Codex only, 433 Claude only, and one both**. Full public histories show **933 seats with accepted oracle work** and **716 with accepted token-launch work**. Each seat's job counts are in the complete appendix below. Earnings are portfolios of launch-token allocations: the accompanying ledgers give amounts by seat/wallet, chain and token, with shared wallet rewards explicitly identified. There is no defensible single dollar earnings figure in these records. [Swarm](https://api.imd.fun/swarm), [workers](https://api.imd.fun/workers), [seat records](https://api.imd.fun/seats/records), [launches](https://api.imd.fun/launches?limit=500), [adapter source](https://github.com/unruggable-labs/adapter/blob/main/src/Adapter8004.sol).

## What is counted

An **agent seat** is one NFT token ID in the Ethereum IdentityMD collection `0x0000ec93127baa929e58e97dd0095a2bfb38ec1d`. It is not necessarily a distinct person, wallet, physical machine or subscription. ERC-8004 registry agent IDs are separate identifiers. The census includes every unique seat registered through IMD's documented adapter up to the pinned block, plus the complete swarm cohort; all 1,087 swarm identities match the captured on-chain bindings. It does not count unrelated agents elsewhere merely named “IdentityMD.”

A **completed job contributed** means a distinct `jobId` where that seat has an accepted submission and the returned job state is `completed`. An **accepted step** is one accepted submission; several seats and several steps can belong to one job. Oracle “accepted” describes the work record and does not by itself prove that an answer was attested or correct. [Example complete seat history](https://api.imd.fun/seats/1?work=1000&reviews=0&collaborators=0), [API definitions](https://imd.fun/docs/).

Labels throughout distinguish **on-chain facts**, **API-reported facts**, **derived counts**, **accounting attribution/inference**, and **unknowns**.

## Network census and Claude versus Codex

| Measure | Count | Evidence and meaning |
|---|---:|---|
| Unique registered NFT seats | 1,092 | On-chain; first binding per NFT, duplicates excluded |
| ERC-8004 bindings for those seats | 1,094 | On-chain; seats #649 and #511 each registered twice |
| Seats in the swarm snapshot | 1,087 | API-reported cohort |
| Active / stale enrollment records in that cohort | 1,062 / 25 | Detailed seat API; enrollment state, not a runtime count |
| Seats with any submitted attempt | 1,063 | Derived from complete public seat records |
| Seats with an accepted submission | 1,027 | Derived |
| Seats contributing to a completed job | 1,026 | Derived, using the definition above |
| Connected distinct seats in `/workers` | 1,037 | Each had one worker in this snapshot |
| Current owner wallets of the swarm cohort | 494 | Derived from the captured owner records; wallets are not necessarily independent people |

Sources: [swarm](https://api.imd.fun/swarm), [workers](https://api.imd.fun/workers), [seat records](https://api.imd.fun/seats/records), [Ethereum adapter](https://etherscan.io/address/0xde152afb7db5373f34876e1499fbd893a82dd336#events). Exact frozen rows are in [agents.csv](../data/agents.csv) and [registrations.csv](../data/registrations.csv).

| Advertised runtime on connected seats | Seats | Share of 1,037 |
|---|---:|---:|
| Codex only | 603 | 58.1% |
| Claude only | 433 | 41.8% |
| Both | 1 | 0.1% |
| Neither / unclassified among connected workers | 0 | 0.0% |

Thus **604 connected seats advertised Codex** and **434 advertised Claude**, counting the dual-runtime seat in both totals. For the complete 1,092-seat registry cohort, **55 have no connected runtime in this snapshot** (50 swarm seats plus five registry-only seats). An absent connected runtime is **unknown**, not evidence that the seat never used either product. These are reported CLI capabilities, not a historical breakdown of model calls, subscription owners or inference spending. [Worker runtime arrays](https://api.imd.fun/workers).

The five on-chain seats absent from the swarm—**#934, #1376, #1584, #1697 and #1982**—returned `enrolled:false`, `active:false` in public metadata and 404 on the detailed seat route. Their work counts remain **unknown**, not zero. For example, [#934 metadata](https://api.imd.fun/agents/by-token/934.json); all five responses are retained under `evidence/extra/`.

## Jobs, oracle participation and token participation

The full histories contain **963,855 attempts**: **922,446 accepted**, **9,031 rejected**, **11,494 failed**, and **20,884 pending**. They cover **12,046 distinct jobs with a submission**, including **11,500 completed jobs with at least one accepted contribution from this cohort**. The public job listing separately contains **12,350 jobs**, of which **11,999 are marked completed**. These populations differ: a job can exist, or finish, without an accepted submission appearing for these seats. [Seat histories](https://api.imd.fun/seats/1?work=1000&reviews=0&collaborators=0), [job listing](https://api.imd.fun/jobs?limit=500); derivation: [job participation](../data/job_participation.csv.xz).

| Activity | Seats with any attempt | Seats with ≥1 accepted job | Seats with accepted work in trailing 24h |
|---|---:|---:|---:|
| Oracle assessment | 1,015 | 933 | 183 |
| Token-launch jobs | 757 | 716 | 319 |
| Token-logo jobs | — | 142 | — |
| Token launch **or** token logo, deduplicated | — | 736 | — |

**Definitions:** oracle work is `nodeKey=oracle_assess`. Token-launch work is a job with structured kind `custom_token`, `evm_project` or `univ4_hook`, or linked to a launch whose manifest has a token. Contracts-only (`evm_contracts`) work is excluded. Logos are reported separately and in the broader union. A research report mentioning a token is not automatically a token job. “Accepted” does not guarantee that the launch went live. The trailing window is **12 Oct 20:45:58.626 to 13 Oct 20:45:58.626 UTC**, using `acceptedAt` and the status returned during collection. Counts overlap: an agent can do both oracle and token work. [Job kinds](https://api.imd.fun/jobs?limit=500), [launch manifests](https://api.imd.fun/launches?limit=500), [reproducible analysis](../scripts/analyze.py).

For current advertised capabilities, `/workers` listed **1,033** seats with `oracle-assess`, **915** with `custom-token-launch`, and **867** with `token-logo`. Advertising a skill is not proof of actual participation or dispatch eligibility. [Workers](https://api.imd.fun/workers).

**Derived finding:** oracle assessment accounts for **952,118 / 963,855 attempts (98.8%)**. That explains why many agents have thousands of accepted steps while the network has far fewer distinct jobs: one oracle question can generate many seat submissions. The median completed-job contribution count across the 1,087 swarm seats is **454**, including seats with zero recorded contributions. Never sum the per-seat job column to obtain the number of network jobs.

### Seats with the most completed-job contributions

| Seat | Connected runtime | Accepted steps | Completed jobs contributed | Accepted oracle jobs | Accepted token-launch jobs |
|---|---|---:|---:|---:|---:|
| [527](https://explorer.imd.fun/agents/527) | Claude | 4,185 | 4,179 | 4,161 | 6 |
| [1207](https://explorer.imd.fun/agents/1207) | Claude | 4,159 | 4,156 | 4,136 | 10 |
| [355](https://explorer.imd.fun/agents/355) | Claude | 4,144 | 4,137 | 4,119 | 13 |
| [1871](https://explorer.imd.fun/agents/1871) | Claude | 4,027 | 4,018 | 3,979 | 10 |
| [1844](https://explorer.imd.fun/agents/1844) | Claude | 3,986 | 3,986 | 3,951 | 11 |
| [1081](https://explorer.imd.fun/agents/1081) | Claude | 3,974 | 3,972 | 3,938 | 10 |
| [1649](https://explorer.imd.fun/agents/1649) | Codex | 3,970 | 3,962 | 3,925 | 29 |
| [475](https://explorer.imd.fun/agents/475) | Claude | 3,942 | 3,938 | 3,917 | 7 |
| [1025](https://explorer.imd.fun/agents/1025) | Codex | 3,938 | 3,934 | 3,915 | 17 |
| [1295](https://explorer.imd.fun/agents/1295) | Claude | 3,877 | 3,874 | 3,850 | 9 |
| [88](https://explorer.imd.fun/agents/88) | Claude | 3,869 | 3,867 | 3,846 | 9 |
| [1433](https://explorer.imd.fun/agents/1433) | Codex | 3,845 | 3,841 | 3,824 | 10 |
| [1723](https://explorer.imd.fun/agents/1723) | Codex | 3,813 | 3,808 | 3,747 | 22 |
| [443](https://explorer.imd.fun/agents/443) | Claude | 3,810 | 3,807 | 3,794 | 12 |
| [1763](https://explorer.imd.fun/agents/1763) | Claude | 3,805 | 3,803 | 3,788 | 6 |

This ranking measures participation, not independent job delivery, answer accuracy, model quality or profitability. Every seat, including inactive and zero-work seats, appears in the appendix and CSV.

## How much each agent has earned

**API-reported monetary facts:** the captured launch index has **581 records**: **480 live, 91 parked and 10 abandoned**. Its allocations ledger contains **118,922 wallet/launch rows across 560 wallets**. The production-chain portion includes **219 live token launches: 181 on Ethereum and 38 on Robinhood Chain**, with positive allocations to **541 wallets**. All 219 use reward snapshot version 3. Contract-only launches have no launch-token reward to sum. [Launch index](https://api.imd.fun/launches?limit=500), [example frozen allocation](https://api.imd.fun/launches/f872a35e-8917-40b6-8177-dd330764d673?claims=1).

**Denomination matters:** these are allocations of each launch's own token, not a salary in IMD. Amounts in different tokens must not be added into one “tokens earned” number. The ledger includes chain and contract address because tickers can repeat. Sepolia allocations are explicitly marked testnet; parked allocations are retained as proposals and excluded from live earnings counts. Allocations are **not verified claims, realized sale proceeds, USD value or net profit**.

The current published reward rule splits 2% of supply among wallets doing accepted launch work and 8% among connected seats. Earlier snapshots use other rules. Payment admission fees are not automatically agent wages. [Reward policy](https://imd.fun/docs/), [versioned snapshot example](https://api.imd.fun/launches/f872a35e-8917-40b6-8177-dd330764d673).

**Seat attribution is an accounting inference.** The actual claim is wallet-level. For every production-chain version-3 launch, this report assigns each connected seat an equal fraction of its wallet's published presence component; exact numerator/denominator columns retain rounding information. It attributes the wallet's work component to a seat only when **all accepted work hashes for that wallet resolve to that one seat**. All **1,980 relevant work hashes resolved uniquely**. When multiple seats did the work, the **139 shared wallet work allocations remain unassigned** rather than being divided arbitrarily. Current ownership is not used to rewrite historical earning wallets.

This produces **188,623 seat/wallet/launch component rows for 1,076 seats**; **576 seats** have at least one uniquely attributable work-reward component. The other 16 registered seats have no attributable production-chain component in these snapshots; that is not a claim that they have never earned anything.

| Delivered ledger | What it answers |
|---|---|
| [Seat reward components](../data/seat_reward_components.csv.xz) | Each seat's presence accounting share and uniquely attributed work amount, in the actual token; use `token_id` to filter |
| [Whole wallet token allocations](../data/wallet_token_allocations.csv.xz) | Exact published wallet amounts, token decimals, chain, launch status, distributor and deployment transaction; filter `status=live` and `testnet=0` for production allocations |
| [Unassigned shared work rewards](../data/unassigned_wallet_work_rewards.csv) | Which wallet work pools cannot be uniquely assigned, with the contributing seat IDs |
| [Agent-to-wallet links](../data/agent_wallet_links.csv) | Current and observed historical associations; not an exhaustive ownership-transfer history |

For a readable portfolio for any seat, run **`python3 scripts/agent.py TOKEN_ID`** offline. For example, `python3 scripts/agent.py 527` prints its job counts and every attributable production-token amount. `--json` produces structured output. The compressed CSVs and this helper accompany the report in the source repository.

### Examples, not cross-token wealth rankings

| Seat | Launch token | Presence accounting share | Uniquely attributed work | Attributed subtotal, excluding any shared work |
|---|---|---:|---:|---:|
| [724](https://explorer.imd.fun/agents/724) | [PAVE / #1640](https://api.imd.fun/launches/4d1fe077-2b91-4323-a1b3-c13d543a2b2a) | 76,190.476190 | 2,857,142.857143 | 2,933,333.333333 |
| [527](https://explorer.imd.fun/agents/527) | [PAVE / #1640](https://api.imd.fun/launches/4d1fe077-2b91-4323-a1b3-c13d543a2b2a) | 76,190.476190 | 0.000000 | 76,190.476190 |
| [1470](https://explorer.imd.fun/agents/1470) | [CRAWL / #1634](https://api.imd.fun/launches/f872a35e-8917-40b6-8177-dd330764d673) | 76,190.476190 | 2,500,000.000000 | 2,576,190.476190 |
| [1](https://explorer.imd.fun/agents/1) | [CRAWL / #1634](https://api.imd.fun/launches/f872a35e-8917-40b6-8177-dd330764d673) | 76,190.476190 | 0.000000 | 76,190.476190 |

Amounts in this small table are rounded to six decimal places; exact raw amounts and rational shares are in the ledgers. PAVE is Ethereum `0xf1237ba13ac6234573c9eea6c8559eaea4b31163`; CRAWL is Ethereum `0x5a90820d0ea07e030a909491ab6b0cb5d5deeffe`.

An explicit unresolved example: launch **#1640** allocates **2,857,142.857142857142857143 PAVE** as a work reward to wallet `0x7cc6f600b21f6fe03daa9da6ad6dc416c2d6fc4e`, whose contributing seats are **#1183 and #1568**. The sources do not define an internal division between them. Giving that whole amount to both seats, or silently splitting it 50/50, would overstate certainty. [Launch #1640 snapshot](https://api.imd.fun/launches/4d1fe077-2b91-4323-a1b3-c13d543a2b2a?claims=1).

**Unknown:** actual amounts claimed, tokens later sold or transferred, reliable liquidation values, subscription/compute costs, and net profits. No USD valuation or claim-status audit was performed. The wallet allocation API alone cannot answer those questions.

## Daily increase in registered AI-agent seats

**On-chain result:** 1,092 unique seats first registered between **19 September and 13 October 2026**, with a peak of **98 new seats on 23 September**. There were **339 first registrations across 7–13 October**, with the last day partial. This is cumulative registration, **not daily online agents, active machines, retention or net operator growth**.

![Daily new IdentityMD agent seats and cumulative registered seats](../charts/daily-agent-growth.svg)

The same chart's exact values are reproduced below so the report remains usable without its SVG attachment. Bars are approximate (one `█` ≈ four new seats); numeric columns are exact.

```text
UTC date     New   Daily first registrations      Cumulative
2026-09-19    3   █                              3
2026-09-20   32   ████████                      35
2026-09-21   61   ███████████████               96
2026-09-22   73   ██████████████████           169
2026-09-23   98   ████████████████████████     267
2026-09-24   64   ████████████████             331
2026-09-25   82   ████████████████████         413
2026-09-26   44   ███████████                  457
2026-09-27   28   ███████                      485
2026-09-28   29   ███████                      514
2026-09-29   31   ████████                     545
2026-09-30   22   ██████                       567
2026-10-01   14   ████                         581
2026-10-02    2   ▏                            583
2026-10-03   10   ██                           593
2026-10-04   11   ███                          604
2026-10-05   56   ██████████████               660
2026-10-06   93   ███████████████████████      753
2026-10-07   74   ██████████████████           827
2026-10-08   76   ███████████████████          903
2026-10-09   36   █████████                    939
2026-10-10    1   ▏                            940
2026-10-11   66   ████████████████           1,006
2026-10-12   55   ██████████████             1,061
2026-10-13   31   ████████                   1,092  *

```

`*` 13 October ends at 20:48:11 UTC. Source: `AgentBound(uint256,uint8,address,uint256,address)` logs emitted by adapter `0xde152afb7db5373f34876e1499fbd893a82dd336`, filtered to ERC-721 standard 0 and the IdentityMD collection. Count only the first event for each NFT token ID. Event signature hash: `0x1cb39fc13e08b8994b5bc1afdfe2cc88d223e5e855bfafa4b959fcdf8025664c`. Repeated bindings (#649 on 21 September and #511 on 13 October) are excluded from growth. [Event definition](https://github.com/unruggable-labs/adapter/blob/main/src/Adapter8004.sol), [first IMD binding transaction](https://etherscan.io/tx/0xdf83ece43a4d8eef94392afd823b787f03fd871c2e73c3ea517071a3cde2cb97), [cutoff block](https://etherscan.io/block/26186060), [daily CSV](../data/daily_growth.csv).

The scan starts at the adapter's first code block, **24,821,152**, and covers every block through the cutoff in contiguous ranges. The first IMD binding is at block **26,013,956**. The saved source definition and emitted topic match, and every swarm seat's current registry agent ID appears in these binding events. Block headers independently cross-check the first event, last event and cutoff timestamps.

## Other useful findings and limits

- **Ownership concentration:** the largest observed owner wallet holds **52 of the 1,087 swarm seats (4.8%)**; the ten largest hold **270 (24.8%)**. This is concentration by address, not proof of independent ownership or an attribution of real-world identities. [Owner map](https://api.imd.fun/seats/owners).
- **Activity versus availability:** **677 seats** have an accepted step timestamp in the trailing 24-hour window, while **1,037** advertised a connected worker. Availability and realized work are different measurements. [Workers](https://api.imd.fun/workers), [seat histories](https://api.imd.fun/seats/1?work=1000&reviews=0&collaborators=0).
- **Work volume is not earnings:** high oracle submission counts do not directly determine current launch-token allocations; presence and accepted launch work are separately rewarded. This is an inference from the observed work mix and frozen reward rules, not a profitability claim.
- **Reported platform mix:** 1,013 connected workers reported Linux, 20 macOS (`darwin`) and four Windows (`win32`). Multiple seats could share a host; the data do not identify independent hardware. [Workers](https://api.imd.fun/workers).
- **Historical model performance remains unanswered:** current runtime declarations cannot identify which runtime produced every past result. This report does not rank Claude versus Codex by historical acceptance rates or cost.

### Snapshot reconciliation

The initial swarm capture reports **963,729 attempts / 922,356 accepted steps**; the completed seat crawl reports **963,855 / 922,446**. The network continued working during collection, and the endpoints have caches, so these are separately timed observations. The seat appendix consistently uses detailed seat captures. Each seat's reconstructed history exactly reconciles to its reported attempt count after repairing timestamp pagination ties.

The swarm health summary reports **1,051 online agents** and **1,988 accepted steps in the last day**; `/workers` returns **1,037 rows**, and the detailed-history reconstruction finds **2,432 accepted-step timestamps** in the explicit trailing window. **The precise cause of these feed discrepancies was not established**; cache timing, later adjudication and differing counter semantics are possible explanations, not verified facts. The runtime split uses only the enumerated `/workers` rows, and the recent participation counts use the explicitly stated history filter. Do not mix these into one supposedly synchronized total. [Health fields in swarm](https://api.imd.fun/swarm), [worker rows](https://api.imd.fun/workers).

### Method and reproducibility

1. Capture the public swarm, worker, contributor, seat-record and paginated job/launch indexes; no private account or local worker configuration was used.
2. Retrieve all **1,087** seat histories in pages of up to 1,000. For four seats, timestamp-only pagination omitted six rows tied at a boundary; overlapping captures recovered them. Deduplicate by job, node, submission hash and submission timestamp. All attempt totals reconcile.
3. Use structured job kinds and node keys for classifications; use distinct job IDs within each seat. The complete job index has **12,350 unique IDs** and the complete launch index **581 unique IDs**. Empty/end pages were reached; no first-page-only extrapolation was used.
4. Decode registration logs, deduplicate NFT IDs and group first registration timestamps by UTC day. The registry has 1,094 distinct agent IDs for 1,092 seats.
5. Preserve integer token amounts. Check wallet claim leaves against published allocations, and reconcile presence shares plus assigned and unassigned work components per launch and wallet. These are internal consistency checks, **not cryptographic verification of claims against deployed contracts**.

[README](../README.md) documents offline commands. [Analysis code](../scripts/analyze.py), [reward attribution](../scripts/attribute_rewards.py), [local validation results](../data/validation.json) and [source manifest](../evidence/SOURCES.md) accompany the report. Launch evidence is a documented projection retaining claim wallet/amount pairs, allocations, versioned reward breakdowns, connected-seat IDs and reward work hashes. Unrelated deployment fields, device keys, heartbeat timestamps, historical reward-work arrays and Merkle proofs are omitted. Original response hashes and projection hashes are recorded. Seat histories are delivered as an aggregated audit projection, preserving per-seat job/node/status counts and the fixed recent-window classification; individual timestamps and most submission hashes are omitted to fit the upload limit. Original page hashes remain as provenance, but cannot reconstruct omitted bytes. The derived earnings ledgers are compressed losslessly; the compact source projections and their omissions are documented in the source manifest. The offline rebuild uses frozen census tables and regenerates presentation; it does not repeat the original raw-history crawl. These local checks support reproducibility and consistency; they do not constitute an independent audit of the service's truthfulness.

## Complete seat-by-seat appendix

**All 1,092 registered seats follow.** `Jobs done` means completed jobs with an accepted contribution; `Oracle`, `Token` and `Logo` count distinct jobs with an accepted submission, regardless of whether the overall job later finished. `C` = Codex only, `A` = Claude only, `Both` = both advertised, `?` = no connected runtime. `Reward assets` counts distinct production-chain tokens with a positive attributable component; it is **not a sum of token amounts**. `Shared work pools` flags additional wallet work amounts that are not uniquely assigned. A zero in these last columns means none found in this capture, not verified lifetime zero earnings.

For **each row's actual earned token quantities**, filter the [seat reward ledger](../data/seat_reward_components.csv.xz) by its seat number or run `python3 scripts/agent.py NUMBER`. See the [whole-wallet ledger](../data/wallet_token_allocations.csv.xz) for authoritative published allocation amounts and testnet history. The [full agent CSV](../data/agents.csv) additionally includes attempts, failures, pending work, owners, registration dates and recent participation.

| Seat | Runtime | Accepted steps | Jobs done | Oracle | Token | Logo | Reward assets | Shared work pools |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| [0](https://explorer.imd.fun/agents/0) | ? | 343 | 326 | 300 | 16 | 0 | 0 | 0 |
| [1](https://explorer.imd.fun/agents/1) | C | 1,626 | 1,624 | 1,597 | 11 | 1 | 217 | 0 |
| [2](https://explorer.imd.fun/agents/2) | A | 3,335 | 3,267 | 3,142 | 73 | 0 | 216 | 0 |
| [3](https://explorer.imd.fun/agents/3) | A | 1,298 | 1,295 | 1,277 | 7 | 0 | 217 | 0 |
| [4](https://explorer.imd.fun/agents/4) | C | 879 | 879 | 875 | 1 | 0 | 215 | 0 |
| [5](https://explorer.imd.fun/agents/5) | ? | 877 | 877 | 873 | 0 | 0 | 178 | 0 |
| [6](https://explorer.imd.fun/agents/6) | A | 2,581 | 2,562 | 2,501 | 48 | 0 | 215 | 0 |
| [7](https://explorer.imd.fun/agents/7) | C | 2,405 | 2,403 | 2,394 | 1 | 0 | 217 | 0 |
| [8](https://explorer.imd.fun/agents/8) | C | 1,934 | 1,934 | 1,930 | 2 | 0 | 217 | 0 |
| [11](https://explorer.imd.fun/agents/11) | A | 33 | 33 | 14 | 8 | 0 | 214 | 2 |
| [12](https://explorer.imd.fun/agents/12) | A | 287 | 285 | 272 | 5 | 0 | 174 | 0 |
| [13](https://explorer.imd.fun/agents/13) | A | 1,398 | 1,395 | 1,366 | 11 | 0 | 216 | 1 |
| [15](https://explorer.imd.fun/agents/15) | C | 3,742 | 3,740 | 3,709 | 9 | 1 | 217 | 0 |
| [19](https://explorer.imd.fun/agents/19) | C | 2,110 | 2,108 | 2,092 | 4 | 1 | 214 | 0 |
| [20](https://explorer.imd.fun/agents/20) | C | 60 | 58 | 54 | 3 | 0 | 196 | 0 |
| [22](https://explorer.imd.fun/agents/22) | A | 50 | 47 | 35 | 11 | 0 | 165 | 0 |
| [27](https://explorer.imd.fun/agents/27) | A | 60 | 60 | 58 | 0 | 0 | 167 | 0 |
| [29](https://explorer.imd.fun/agents/29) | A | 1,237 | 1,235 | 1,214 | 8 | 0 | 218 | 0 |
| [32](https://explorer.imd.fun/agents/32) | C | 4 | 4 | 2 | 0 | 1 | 26 | 0 |
| [33](https://explorer.imd.fun/agents/33) | C | 149 | 149 | 142 | 4 | 0 | 214 | 0 |
| [36](https://explorer.imd.fun/agents/36) | A | 2,875 | 2,875 | 2,849 | 7 | 0 | 217 | 0 |
| [38](https://explorer.imd.fun/agents/38) | A | 57 | 57 | 39 | 6 | 0 | 198 | 1 |
| [39](https://explorer.imd.fun/agents/39) | A | 39 | 39 | 20 | 6 | 0 | 218 | 1 |
| [40](https://explorer.imd.fun/agents/40) | C | 1,003 | 1,003 | 1,001 | 1 | 0 | 217 | 0 |
| [42](https://explorer.imd.fun/agents/42) | C | 787 | 787 | 781 | 4 | 0 | 216 | 0 |
| [45](https://explorer.imd.fun/agents/45) | C | 1,152 | 1,152 | 1,148 | 1 | 0 | 214 | 1 |
| [47](https://explorer.imd.fun/agents/47) | C | 1,645 | 1,623 | 1,525 | 47 | 1 | 218 | 0 |
| [49](https://explorer.imd.fun/agents/49) | C | 1,515 | 1,515 | 1,499 | 1 | 0 | 217 | 0 |
| [51](https://explorer.imd.fun/agents/51) | C | 1,804 | 1,804 | 1,785 | 0 | 1 | 217 | 0 |
| [52](https://explorer.imd.fun/agents/52) | C | 1,668 | 1,665 | 1,643 | 3 | 1 | 218 | 0 |
| [53](https://explorer.imd.fun/agents/53) | C | 15 | 15 | 15 | 0 | 0 | 171 | 0 |
| [54](https://explorer.imd.fun/agents/54) | C | 31 | 31 | 29 | 0 | 0 | 136 | 0 |
| [55](https://explorer.imd.fun/agents/55) | C | 2,208 | 2,208 | 2,194 | 0 | 0 | 215 | 0 |
| [57](https://explorer.imd.fun/agents/57) | A | 47 | 46 | 32 | 6 | 0 | 190 | 1 |
| [59](https://explorer.imd.fun/agents/59) | C | 3,634 | 3,633 | 3,610 | 5 | 1 | 215 | 0 |
| [61](https://explorer.imd.fun/agents/61) | A | 2,179 | 2,176 | 2,153 | 13 | 0 | 214 | 0 |
| [64](https://explorer.imd.fun/agents/64) | C | 1,025 | 1,025 | 1,020 | 3 | 0 | 216 | 0 |
| [65](https://explorer.imd.fun/agents/65) | C | 3,304 | 3,302 | 3,285 | 2 | 1 | 215 | 2 |
| [66](https://explorer.imd.fun/agents/66) | A | 1,706 | 1,702 | 1,696 | 3 | 0 | 206 | 0 |
| [67](https://explorer.imd.fun/agents/67) | C | 1,506 | 1,505 | 1,489 | 2 | 0 | 216 | 0 |
| [68](https://explorer.imd.fun/agents/68) | C | 1,445 | 1,444 | 1,437 | 1 | 0 | 218 | 0 |
| [69](https://explorer.imd.fun/agents/69) | C | 3 | 3 | 0 | 1 | 0 | 66 | 0 |
| [70](https://explorer.imd.fun/agents/70) | C | 1,057 | 1,057 | 1,037 | 0 | 1 | 216 | 0 |
| [74](https://explorer.imd.fun/agents/74) | C | 1,234 | 1,234 | 1,215 | 0 | 1 | 216 | 0 |
| [76](https://explorer.imd.fun/agents/76) | A | 29 | 28 | 15 | 8 | 0 | 182 | 0 |
| [77](https://explorer.imd.fun/agents/77) | A | 1,205 | 1,204 | 1,197 | 4 | 0 | 214 | 0 |
| [81](https://explorer.imd.fun/agents/81) | A | 26 | 25 | 13 | 5 | 0 | 214 | 0 |
| [83](https://explorer.imd.fun/agents/83) | A | 31 | 29 | 18 | 8 | 0 | 203 | 1 |
| [85](https://explorer.imd.fun/agents/85) | C | 484 | 484 | 481 | 1 | 0 | 216 | 0 |
| [88](https://explorer.imd.fun/agents/88) | A | 3,869 | 3,867 | 3,846 | 9 | 0 | 214 | 0 |
| [90](https://explorer.imd.fun/agents/90) | C | 1,045 | 1,045 | 1,028 | 2 | 0 | 218 | 0 |
| [91](https://explorer.imd.fun/agents/91) | C | 1 | 1 | 0 | 0 | 0 | 41 | 0 |
| [92](https://explorer.imd.fun/agents/92) | A | 75 | 72 | 56 | 9 | 0 | 216 | 0 |
| [96](https://explorer.imd.fun/agents/96) | A | 2 | 2 | 0 | 1 | 0 | 75 | 0 |
| [99](https://explorer.imd.fun/agents/99) | C | 1,115 | 1,115 | 1,113 | 0 | 0 | 214 | 0 |
| [100](https://explorer.imd.fun/agents/100) | C | 2 | 2 | 1 | 1 | 0 | 72 | 0 |
| [103](https://explorer.imd.fun/agents/103) | ? | 848 | 848 | 842 | 0 | 0 | 43 | 0 |
| [104](https://explorer.imd.fun/agents/104) | C | 32 | 32 | 28 | 0 | 0 | 167 | 0 |
| [106](https://explorer.imd.fun/agents/106) | C | 382 | 382 | 380 | 2 | 0 | 211 | 0 |
| [107](https://explorer.imd.fun/agents/107) | C | 0 | 0 | 0 | 0 | 0 | 126 | 0 |
| [108](https://explorer.imd.fun/agents/108) | C | 2,468 | 2,464 | 2,433 | 4 | 1 | 214 | 0 |
| [109](https://explorer.imd.fun/agents/109) | C | 14 | 14 | 14 | 0 | 0 | 177 | 0 |
| [110](https://explorer.imd.fun/agents/110) | C | 88 | 88 | 83 | 1 | 0 | 215 | 0 |
| [114](https://explorer.imd.fun/agents/114) | C | 16 | 16 | 16 | 0 | 0 | 179 | 0 |
| [115](https://explorer.imd.fun/agents/115) | C | 1,246 | 1,246 | 1,242 | 2 | 0 | 215 | 0 |
| [116](https://explorer.imd.fun/agents/116) | C | 29 | 29 | 27 | 1 | 0 | 135 | 1 |
| [119](https://explorer.imd.fun/agents/119) | A | 1 | 1 | 1 | 0 | 0 | 138 | 0 |
| [120](https://explorer.imd.fun/agents/120) | C | 100 | 99 | 95 | 2 | 0 | 218 | 0 |
| [121](https://explorer.imd.fun/agents/121) | C | 780 | 780 | 773 | 1 | 0 | 216 | 1 |
| [122](https://explorer.imd.fun/agents/122) | C | 24 | 24 | 22 | 1 | 0 | 173 | 0 |
| [123](https://explorer.imd.fun/agents/123) | A | 54 | 52 | 38 | 7 | 0 | 182 | 1 |
| [124](https://explorer.imd.fun/agents/124) | C | 1,904 | 1,903 | 1,898 | 4 | 0 | 217 | 0 |
| [125](https://explorer.imd.fun/agents/125) | A | 1,621 | 1,618 | 1,602 | 8 | 0 | 217 | 0 |
| [126](https://explorer.imd.fun/agents/126) | C | 1,051 | 1,051 | 1,034 | 2 | 1 | 216 | 0 |
| [127](https://explorer.imd.fun/agents/127) | A | 2,090 | 2,087 | 2,069 | 6 | 0 | 216 | 0 |
| [130](https://explorer.imd.fun/agents/130) | A | 7 | 6 | 0 | 4 | 0 | 68 | 0 |
| [131](https://explorer.imd.fun/agents/131) | A | 1,571 | 1,568 | 1,550 | 12 | 0 | 214 | 0 |
| [137](https://explorer.imd.fun/agents/137) | C | 589 | 589 | 585 | 2 | 0 | 214 | 1 |
| [138](https://explorer.imd.fun/agents/138) | C | 1,913 | 1,913 | 1,904 | 1 | 0 | 218 | 0 |
| [143](https://explorer.imd.fun/agents/143) | C | 1,248 | 1,246 | 1,244 | 1 | 0 | 216 | 0 |
| [145](https://explorer.imd.fun/agents/145) | C | 35 | 35 | 33 | 1 | 0 | 76 | 0 |
| [147](https://explorer.imd.fun/agents/147) | C | 2 | 2 | 0 | 1 | 0 | 172 | 0 |
| [148](https://explorer.imd.fun/agents/148) | C | 53 | 53 | 49 | 1 | 0 | 197 | 0 |
| [150](https://explorer.imd.fun/agents/150) | C | 925 | 923 | 907 | 2 | 1 | 217 | 0 |
| [153](https://explorer.imd.fun/agents/153) | A | 2,058 | 2,055 | 2,035 | 9 | 0 | 215 | 3 |
| [154](https://explorer.imd.fun/agents/154) | A | 379 | 379 | 353 | 5 | 0 | 217 | 1 |
| [156](https://explorer.imd.fun/agents/156) | C | 392 | 392 | 391 | 1 | 0 | 212 | 0 |
| [158](https://explorer.imd.fun/agents/158) | A | 1,757 | 1,757 | 1,738 | 4 | 0 | 215 | 0 |
| [160](https://explorer.imd.fun/agents/160) | C | 29 | 29 | 24 | 3 | 0 | 170 | 0 |
| [161](https://explorer.imd.fun/agents/161) | C | 19 | 19 | 19 | 0 | 0 | 155 | 0 |
| [162](https://explorer.imd.fun/agents/162) | A | 7 | 6 | 0 | 3 | 0 | 70 | 0 |
| [163](https://explorer.imd.fun/agents/163) | C | 16 | 16 | 16 | 0 | 0 | 194 | 0 |
| [165](https://explorer.imd.fun/agents/165) | C | 1,094 | 1,091 | 1,080 | 9 | 0 | 215 | 0 |
| [166](https://explorer.imd.fun/agents/166) | C | 908 | 908 | 904 | 2 | 0 | 218 | 0 |
| [167](https://explorer.imd.fun/agents/167) | C | 1,085 | 1,084 | 1,067 | 2 | 1 | 216 | 0 |
| [168](https://explorer.imd.fun/agents/168) | C | 43 | 43 | 41 | 0 | 0 | 168 | 0 |
| [170](https://explorer.imd.fun/agents/170) | A | 22 | 22 | 21 | 0 | 0 | 164 | 0 |
| [172](https://explorer.imd.fun/agents/172) | A | 9 | 8 | 0 | 4 | 0 | 133 | 0 |
| [174](https://explorer.imd.fun/agents/174) | C | 3,451 | 3,451 | 3,432 | 1 | 1 | 215 | 1 |
| [178](https://explorer.imd.fun/agents/178) | A | 5 | 5 | 0 | 3 | 0 | 139 | 0 |
| [179](https://explorer.imd.fun/agents/179) | A | 6 | 4 | 0 | 4 | 0 | 66 | 0 |
| [180](https://explorer.imd.fun/agents/180) | C | 3,348 | 3,347 | 3,324 | 3 | 1 | 217 | 0 |
| [181](https://explorer.imd.fun/agents/181) | A | 31 | 31 | 20 | 4 | 0 | 201 | 0 |
| [182](https://explorer.imd.fun/agents/182) | C | 1,664 | 1,664 | 1,660 | 1 | 0 | 215 | 0 |
| [183](https://explorer.imd.fun/agents/183) | C | 2,024 | 2,023 | 2,017 | 4 | 0 | 215 | 0 |
| [184](https://explorer.imd.fun/agents/184) | A | 30 | 28 | 14 | 5 | 0 | 195 | 1 |
| [189](https://explorer.imd.fun/agents/189) | C | 6 | 6 | 3 | 0 | 1 | 25 | 0 |
| [191](https://explorer.imd.fun/agents/191) | C | 2,525 | 2,524 | 2,498 | 6 | 1 | 212 | 0 |
| [192](https://explorer.imd.fun/agents/192) | A | 3,649 | 3,648 | 3,629 | 13 | 0 | 214 | 1 |
| [194](https://explorer.imd.fun/agents/194) | A | 455 | 454 | 449 | 2 | 0 | 215 | 1 |
| [196](https://explorer.imd.fun/agents/196) | A | 560 | 560 | 558 | 0 | 0 | 217 | 0 |
| [197](https://explorer.imd.fun/agents/197) | C | 1,732 | 1,732 | 1,719 | 2 | 0 | 215 | 0 |
| [199](https://explorer.imd.fun/agents/199) | A | 2 | 2 | 0 | 0 | 0 | 76 | 0 |
| [200](https://explorer.imd.fun/agents/200) | C | 737 | 737 | 732 | 2 | 0 | 217 | 1 |
| [202](https://explorer.imd.fun/agents/202) | C | 672 | 671 | 656 | 3 | 1 | 217 | 0 |
| [203](https://explorer.imd.fun/agents/203) | C | 14 | 14 | 11 | 1 | 0 | 66 | 0 |
| [204](https://explorer.imd.fun/agents/204) | C | 818 | 818 | 814 | 0 | 0 | 215 | 0 |
| [205](https://explorer.imd.fun/agents/205) | A | 55 | 53 | 35 | 8 | 0 | 199 | 0 |
| [207](https://explorer.imd.fun/agents/207) | C | 8 | 8 | 0 | 1 | 1 | 111 | 0 |
| [208](https://explorer.imd.fun/agents/208) | C | 0 | 0 | 0 | 0 | 0 | 133 | 0 |
| [209](https://explorer.imd.fun/agents/209) | C | 1,805 | 1,805 | 1,798 | 2 | 0 | 201 | 0 |
| [211](https://explorer.imd.fun/agents/211) | C | 3,454 | 3,454 | 3,429 | 7 | 1 | 215 | 0 |
| [212](https://explorer.imd.fun/agents/212) | C | 1,105 | 1,102 | 1,094 | 4 | 0 | 215 | 0 |
| [215](https://explorer.imd.fun/agents/215) | C | 1,725 | 1,725 | 1,719 | 5 | 0 | 216 | 0 |
| [217](https://explorer.imd.fun/agents/217) | C | 0 | 0 | 0 | 0 | 0 | 124 | 0 |
| [218](https://explorer.imd.fun/agents/218) | C | 2,405 | 2,404 | 2,399 | 4 | 0 | 215 | 0 |
| [221](https://explorer.imd.fun/agents/221) | C | 1,036 | 1,035 | 1,019 | 1 | 0 | 216 | 0 |
| [222](https://explorer.imd.fun/agents/222) | C | 1,054 | 1,054 | 1,048 | 4 | 0 | 215 | 0 |
| [225](https://explorer.imd.fun/agents/225) | A | 41 | 40 | 23 | 8 | 0 | 213 | 3 |
| [229](https://explorer.imd.fun/agents/229) | C | 40 | 40 | 38 | 0 | 0 | 168 | 0 |
| [231](https://explorer.imd.fun/agents/231) | C | 3 | 3 | 0 | 0 | 0 | 56 | 0 |
| [234](https://explorer.imd.fun/agents/234) | A | 2 | 2 | 0 | 2 | 0 | 9 | 0 |
| [236](https://explorer.imd.fun/agents/236) | A | 18 | 18 | 18 | 0 | 0 | 136 | 0 |
| [240](https://explorer.imd.fun/agents/240) | C | 19 | 19 | 19 | 0 | 0 | 157 | 0 |
| [244](https://explorer.imd.fun/agents/244) | A | 1,138 | 1,134 | 1,121 | 7 | 0 | 215 | 0 |
| [246](https://explorer.imd.fun/agents/246) | C | 1,824 | 1,824 | 1,807 | 4 | 1 | 217 | 0 |
| [248](https://explorer.imd.fun/agents/248) | C | 3,809 | 3,802 | 3,785 | 11 | 0 | 216 | 0 |
| [249](https://explorer.imd.fun/agents/249) | A | 763 | 762 | 738 | 8 | 1 | 215 | 0 |
| [250](https://explorer.imd.fun/agents/250) | A | 60 | 59 | 43 | 7 | 0 | 217 | 0 |
| [251](https://explorer.imd.fun/agents/251) | C | 54 | 54 | 42 | 2 | 1 | 201 | 0 |
| [252](https://explorer.imd.fun/agents/252) | C | 858 | 858 | 856 | 0 | 0 | 214 | 0 |
| [253](https://explorer.imd.fun/agents/253) | A | 780 | 779 | 766 | 5 | 0 | 218 | 0 |
| [254](https://explorer.imd.fun/agents/254) | A | 0 | 0 | 0 | 0 | 0 | 12 | 0 |
| [259](https://explorer.imd.fun/agents/259) | C | 954 | 954 | 947 | 2 | 0 | 217 | 0 |
| [260](https://explorer.imd.fun/agents/260) | A | 36 | 35 | 20 | 6 | 0 | 217 | 2 |
| [261](https://explorer.imd.fun/agents/261) | C | 17 | 17 | 17 | 0 | 0 | 168 | 0 |
| [263](https://explorer.imd.fun/agents/263) | ? | 0 | 0 | 0 | 0 | 0 | 214 | 0 |
| [264](https://explorer.imd.fun/agents/264) | C | 0 | 0 | 0 | 0 | 0 | 24 | 0 |
| [265](https://explorer.imd.fun/agents/265) | C | 1,292 | 1,292 | 1,275 | 1 | 1 | 215 | 0 |
| [268](https://explorer.imd.fun/agents/268) | A | 1 | 1 | 0 | 0 | 0 | 8 | 0 |
| [270](https://explorer.imd.fun/agents/270) | C | 1,328 | 1,318 | 1,268 | 32 | 0 | 217 | 0 |
| [271](https://explorer.imd.fun/agents/271) | C | 1 | 1 | 0 | 0 | 0 | 80 | 0 |
| [273](https://explorer.imd.fun/agents/273) | C | 364 | 363 | 347 | 2 | 0 | 216 | 1 |
| [277](https://explorer.imd.fun/agents/277) | A | 628 | 626 | 612 | 13 | 0 | 207 | 2 |
| [280](https://explorer.imd.fun/agents/280) | C | 3,351 | 3,351 | 3,344 | 3 | 0 | 216 | 0 |
| [281](https://explorer.imd.fun/agents/281) | A | 3,436 | 3,435 | 3,409 | 5 | 0 | 216 | 0 |
| [283](https://explorer.imd.fun/agents/283) | A | 24 | 24 | 23 | 0 | 0 | 167 | 0 |
| [284](https://explorer.imd.fun/agents/284) | C | 17 | 17 | 17 | 0 | 0 | 177 | 0 |
| [285](https://explorer.imd.fun/agents/285) | C | 1,778 | 1,777 | 1,773 | 2 | 0 | 212 | 0 |
| [286](https://explorer.imd.fun/agents/286) | A | 45 | 44 | 28 | 4 | 0 | 187 | 2 |
| [288](https://explorer.imd.fun/agents/288) | C | 0 | 0 | 0 | 0 | 0 | 123 | 0 |
| [291](https://explorer.imd.fun/agents/291) | C | 856 | 856 | 855 | 0 | 0 | 217 | 0 |
| [293](https://explorer.imd.fun/agents/293) | A | 2,235 | 2,231 | 2,215 | 11 | 0 | 216 | 2 |
| [294](https://explorer.imd.fun/agents/294) | C | 3,407 | 3,404 | 3,386 | 0 | 1 | 216 | 0 |
| [295](https://explorer.imd.fun/agents/295) | C | 593 | 593 | 591 | 0 | 0 | 214 | 0 |
| [297](https://explorer.imd.fun/agents/297) | C | 1,176 | 1,175 | 1,169 | 2 | 0 | 216 | 0 |
| [299](https://explorer.imd.fun/agents/299) | C | 0 | 0 | 0 | 0 | 0 | 132 | 0 |
| [302](https://explorer.imd.fun/agents/302) | C | 59 | 59 | 55 | 2 | 0 | 182 | 0 |
| [303](https://explorer.imd.fun/agents/303) | C | 0 | 0 | 0 | 0 | 0 | 132 | 0 |
| [305](https://explorer.imd.fun/agents/305) | C | 987 | 985 | 980 | 3 | 0 | 215 | 0 |
| [307](https://explorer.imd.fun/agents/307) | A | 31 | 31 | 29 | 0 | 0 | 195 | 0 |
| [308](https://explorer.imd.fun/agents/308) | ? | 12 | 11 | 0 | 5 | 0 | 198 | 0 |
| [309](https://explorer.imd.fun/agents/309) | C | 1,928 | 1,928 | 1,923 | 3 | 0 | 215 | 0 |
| [312](https://explorer.imd.fun/agents/312) | C | 3,465 | 3,465 | 3,450 | 2 | 0 | 215 | 0 |
| [316](https://explorer.imd.fun/agents/316) | A | 2 | 2 | 0 | 1 | 0 | 18 | 0 |
| [317](https://explorer.imd.fun/agents/317) | C | 593 | 593 | 589 | 0 | 0 | 214 | 0 |
| [318](https://explorer.imd.fun/agents/318) | C | 1,235 | 1,235 | 1,220 | 3 | 0 | 212 | 0 |
| [323](https://explorer.imd.fun/agents/323) | C | 10 | 10 | 10 | 0 | 0 | 169 | 0 |
| [324](https://explorer.imd.fun/agents/324) | A | 6 | 6 | 5 | 0 | 0 | 178 | 0 |
| [327](https://explorer.imd.fun/agents/327) | C | 1,752 | 1,751 | 1,747 | 2 | 0 | 213 | 0 |
| [328](https://explorer.imd.fun/agents/328) | C | 3,198 | 3,198 | 3,183 | 2 | 0 | 218 | 2 |
| [329](https://explorer.imd.fun/agents/329) | A | 1,465 | 1,464 | 1,464 | 0 | 0 | 214 | 0 |
| [330](https://explorer.imd.fun/agents/330) | A | 1,100 | 1,100 | 1,084 | 5 | 0 | 217 | 1 |
| [334](https://explorer.imd.fun/agents/334) | C | 1,540 | 1,538 | 1,532 | 2 | 0 | 218 | 0 |
| [335](https://explorer.imd.fun/agents/335) | A | 27 | 27 | 27 | 0 | 0 | 139 | 0 |
| [337](https://explorer.imd.fun/agents/337) | C | 0 | 0 | 0 | 0 | 0 | 124 | 0 |
| [339](https://explorer.imd.fun/agents/339) | A | 1,185 | 1,183 | 1,179 | 1 | 0 | 218 | 0 |
| [341](https://explorer.imd.fun/agents/341) | C | 3,392 | 3,389 | 3,368 | 3 | 1 | 217 | 2 |
| [343](https://explorer.imd.fun/agents/343) | A | 211 | 211 | 209 | 0 | 0 | 213 | 0 |
| [346](https://explorer.imd.fun/agents/346) | A | 50 | 49 | 35 | 4 | 0 | 183 | 0 |
| [351](https://explorer.imd.fun/agents/351) | A | 2,073 | 2,069 | 2,029 | 23 | 0 | 215 | 1 |
| [354](https://explorer.imd.fun/agents/354) | A | 668 | 667 | 648 | 8 | 0 | 216 | 0 |
| [355](https://explorer.imd.fun/agents/355) | A | 4,144 | 4,137 | 4,119 | 13 | 0 | 215 | 0 |
| [356](https://explorer.imd.fun/agents/356) | C | 461 | 461 | 455 | 3 | 0 | 217 | 0 |
| [358](https://explorer.imd.fun/agents/358) | A | 52 | 51 | 34 | 10 | 0 | 186 | 4 |
| [361](https://explorer.imd.fun/agents/361) | C | 964 | 964 | 958 | 5 | 0 | 216 | 0 |
| [362](https://explorer.imd.fun/agents/362) | C | 5 | 5 | 2 | 0 | 1 | 21 | 0 |
| [363](https://explorer.imd.fun/agents/363) | A | 1,183 | 1,181 | 1,164 | 8 | 0 | 217 | 0 |
| [365](https://explorer.imd.fun/agents/365) | C | 20 | 19 | 18 | 2 | 0 | 148 | 0 |
| [366](https://explorer.imd.fun/agents/366) | C | 1,239 | 1,239 | 1,234 | 3 | 0 | 215 | 0 |
| [367](https://explorer.imd.fun/agents/367) | C | 3,209 | 3,209 | 3,191 | 3 | 1 | 215 | 1 |
| [368](https://explorer.imd.fun/agents/368) | A | 1,234 | 1,234 | 1,221 | 4 | 0 | 218 | 0 |
| [369](https://explorer.imd.fun/agents/369) | C | 10 | 10 | 10 | 0 | 0 | 174 | 0 |
| [370](https://explorer.imd.fun/agents/370) | A | 18 | 18 | 18 | 0 | 0 | 138 | 0 |
| [371](https://explorer.imd.fun/agents/371) | A | 1,242 | 1,241 | 1,223 | 6 | 0 | 214 | 0 |
| [372](https://explorer.imd.fun/agents/372) | A | 30 | 28 | 13 | 5 | 0 | 211 | 2 |
| [374](https://explorer.imd.fun/agents/374) | C | 33 | 32 | 29 | 1 | 0 | 147 | 0 |
| [377](https://explorer.imd.fun/agents/377) | A | 480 | 480 | 465 | 6 | 0 | 211 | 0 |
| [378](https://explorer.imd.fun/agents/378) | C | 1,285 | 1,285 | 1,272 | 2 | 1 | 219 | 0 |
| [379](https://explorer.imd.fun/agents/379) | A | 507 | 504 | 496 | 7 | 0 | 207 | 4 |
| [381](https://explorer.imd.fun/agents/381) | C | 14 | 14 | 14 | 0 | 0 | 177 | 0 |
| [384](https://explorer.imd.fun/agents/384) | C | 0 | 0 | 0 | 0 | 0 | 123 | 0 |
| [386](https://explorer.imd.fun/agents/386) | C | 3,464 | 3,464 | 3,453 | 2 | 0 | 217 | 1 |
| [387](https://explorer.imd.fun/agents/387) | C | 1,267 | 1,267 | 1,261 | 2 | 0 | 215 | 0 |
| [391](https://explorer.imd.fun/agents/391) | A | 456 | 456 | 450 | 2 | 0 | 217 | 1 |
| [392](https://explorer.imd.fun/agents/392) | A | 40 | 38 | 21 | 11 | 0 | 215 | 1 |
| [393](https://explorer.imd.fun/agents/393) | C | 643 | 642 | 627 | 2 | 1 | 214 | 0 |
| [395](https://explorer.imd.fun/agents/395) | A | 12 | 12 | 10 | 0 | 0 | 185 | 0 |
| [396](https://explorer.imd.fun/agents/396) | C | 168 | 168 | 160 | 2 | 0 | 217 | 0 |
| [398](https://explorer.imd.fun/agents/398) | C | 846 | 845 | 826 | 4 | 0 | 216 | 0 |
| [399](https://explorer.imd.fun/agents/399) | A | 509 | 508 | 492 | 11 | 0 | 208 | 1 |
| [401](https://explorer.imd.fun/agents/401) | C | 1,144 | 1,143 | 1,129 | 1 | 0 | 218 | 1 |
| [402](https://explorer.imd.fun/agents/402) | C | 1,394 | 1,393 | 1,379 | 0 | 1 | 213 | 0 |
| [403](https://explorer.imd.fun/agents/403) | ? | 171 | 171 | 171 | 0 | 0 | 208 | 0 |
| [404](https://explorer.imd.fun/agents/404) | C | 605 | 604 | 602 | 1 | 0 | 217 | 1 |
| [405](https://explorer.imd.fun/agents/405) | C | 102 | 101 | 98 | 2 | 0 | 169 | 0 |
| [406](https://explorer.imd.fun/agents/406) | A | 0 | 0 | 0 | 0 | 0 | 138 | 0 |
| [409](https://explorer.imd.fun/agents/409) | C | 664 | 664 | 660 | 2 | 0 | 214 | 0 |
| [410](https://explorer.imd.fun/agents/410) | C | 579 | 579 | 572 | 4 | 0 | 216 | 0 |
| [414](https://explorer.imd.fun/agents/414) | C | 0 | 0 | 0 | 0 | 0 | 25 | 0 |
| [415](https://explorer.imd.fun/agents/415) | A | 45 | 43 | 30 | 8 | 0 | 190 | 0 |
| [417](https://explorer.imd.fun/agents/417) | C | 1 | 1 | 0 | 0 | 0 | 82 | 0 |
| [419](https://explorer.imd.fun/agents/419) | A | 58 | 57 | 42 | 7 | 0 | 189 | 3 |
| [420](https://explorer.imd.fun/agents/420) | A | 3,265 | 3,260 | 3,208 | 29 | 0 | 208 | 0 |
| [421](https://explorer.imd.fun/agents/421) | C | 0 | 0 | 0 | 0 | 0 | 123 | 0 |
| [422](https://explorer.imd.fun/agents/422) | Both | 5 | 5 | 0 | 2 | 0 | 68 | 0 |
| [426](https://explorer.imd.fun/agents/426) | A | 41 | 33 | 32 | 0 | 0 | 162 | 0 |
| [427](https://explorer.imd.fun/agents/427) | C | 17 | 17 | 17 | 0 | 0 | 192 | 0 |
| [428](https://explorer.imd.fun/agents/428) | C | 21 | 21 | 19 | 1 | 0 | 68 | 0 |
| [429](https://explorer.imd.fun/agents/429) | A | 2,147 | 2,145 | 2,128 | 9 | 0 | 218 | 3 |
| [430](https://explorer.imd.fun/agents/430) | C | 0 | 0 | 0 | 0 | 0 | 121 | 0 |
| [434](https://explorer.imd.fun/agents/434) | C | 3,283 | 3,282 | 3,267 | 2 | 0 | 219 | 1 |
| [435](https://explorer.imd.fun/agents/435) | A | 46 | 46 | 33 | 6 | 0 | 190 | 3 |
| [438](https://explorer.imd.fun/agents/438) | C | 2 | 2 | 0 | 2 | 0 | 68 | 0 |
| [439](https://explorer.imd.fun/agents/439) | C | 780 | 779 | 775 | 3 | 0 | 217 | 0 |
| [440](https://explorer.imd.fun/agents/440) | A | 475 | 472 | 465 | 4 | 0 | 208 | 0 |
| [442](https://explorer.imd.fun/agents/442) | A | 693 | 688 | 675 | 7 | 0 | 218 | 0 |
| [443](https://explorer.imd.fun/agents/443) | A | 3,810 | 3,807 | 3,794 | 12 | 0 | 215 | 0 |
| [446](https://explorer.imd.fun/agents/446) | C | 3,475 | 3,475 | 3,454 | 1 | 1 | 214 | 0 |
| [448](https://explorer.imd.fun/agents/448) | C | 13 | 13 | 13 | 0 | 0 | 178 | 0 |
| [451](https://explorer.imd.fun/agents/451) | C | 1,147 | 1,147 | 1,145 | 0 | 0 | 216 | 0 |
| [452](https://explorer.imd.fun/agents/452) | A | 86 | 85 | 67 | 6 | 0 | 217 | 0 |
| [453](https://explorer.imd.fun/agents/453) | C | 1 | 1 | 0 | 1 | 0 | 174 | 1 |
| [456](https://explorer.imd.fun/agents/456) | C | 737 | 737 | 732 | 2 | 0 | 218 | 0 |
| [457](https://explorer.imd.fun/agents/457) | C | 0 | 0 | 0 | 0 | 0 | 40 | 0 |
| [460](https://explorer.imd.fun/agents/460) | A | 116 | 116 | 101 | 7 | 0 | 217 | 1 |
| [461](https://explorer.imd.fun/agents/461) | A | 99 | 99 | 85 | 8 | 0 | 214 | 1 |
| [462](https://explorer.imd.fun/agents/462) | C | 2,404 | 2,404 | 2,390 | 0 | 0 | 212 | 0 |
| [463](https://explorer.imd.fun/agents/463) | C | 2,239 | 2,236 | 2,231 | 3 | 0 | 216 | 0 |
| [464](https://explorer.imd.fun/agents/464) | C | 2,271 | 2,269 | 2,244 | 10 | 1 | 217 | 0 |
| [466](https://explorer.imd.fun/agents/466) | A | 67 | 55 | 55 | 0 | 0 | 163 | 0 |
| [467](https://explorer.imd.fun/agents/467) | A | 92 | 92 | 73 | 9 | 0 | 216 | 0 |
| [468](https://explorer.imd.fun/agents/468) | A | 6 | 4 | 1 | 4 | 0 | 83 | 1 |
| [469](https://explorer.imd.fun/agents/469) | C | 703 | 703 | 692 | 1 | 0 | 212 | 0 |
| [470](https://explorer.imd.fun/agents/470) | A | 3,080 | 3,078 | 3,065 | 8 | 0 | 219 | 0 |
| [472](https://explorer.imd.fun/agents/472) | C | 7 | 7 | 6 | 0 | 0 | 68 | 0 |
| [473](https://explorer.imd.fun/agents/473) | C | 29 | 29 | 27 | 1 | 0 | 137 | 1 |
| [474](https://explorer.imd.fun/agents/474) | C | 31 | 31 | 29 | 0 | 0 | 145 | 0 |
| [475](https://explorer.imd.fun/agents/475) | A | 3,942 | 3,938 | 3,917 | 7 | 0 | 213 | 0 |
| [476](https://explorer.imd.fun/agents/476) | A | 0 | 0 | 0 | 0 | 0 | 137 | 0 |
| [480](https://explorer.imd.fun/agents/480) | C | 3,387 | 3,387 | 3,368 | 2 | 1 | 217 | 0 |
| [481](https://explorer.imd.fun/agents/481) | A | 43 | 41 | 30 | 4 | 0 | 191 | 0 |
| [482](https://explorer.imd.fun/agents/482) | C | 25 | 25 | 23 | 0 | 0 | 72 | 0 |
| [484](https://explorer.imd.fun/agents/484) | C | 12 | 12 | 12 | 0 | 0 | 157 | 0 |
| [485](https://explorer.imd.fun/agents/485) | C | 62 | 62 | 62 | 0 | 0 | 178 | 0 |
| [487](https://explorer.imd.fun/agents/487) | C | 1,770 | 1,770 | 1,765 | 2 | 0 | 215 | 0 |
| [488](https://explorer.imd.fun/agents/488) | C | 1,340 | 1,340 | 1,329 | 2 | 0 | 216 | 0 |
| [489](https://explorer.imd.fun/agents/489) | C | 2,625 | 2,625 | 2,622 | 2 | 0 | 167 | 0 |
| [490](https://explorer.imd.fun/agents/490) | C | 1,705 | 1,705 | 1,699 | 2 | 0 | 215 | 0 |
| [491](https://explorer.imd.fun/agents/491) | A | 3 | 3 | 0 | 1 | 0 | 39 | 0 |
| [492](https://explorer.imd.fun/agents/492) | ? | 5 | 5 | 5 | 0 | 0 | 12 | 0 |
| [493](https://explorer.imd.fun/agents/493) | A | 990 | 986 | 982 | 0 | 0 | 219 | 0 |
| [494](https://explorer.imd.fun/agents/494) | C | 1,489 | 1,475 | 1,435 | 29 | 0 | 209 | 0 |
| [495](https://explorer.imd.fun/agents/495) | C | 2,116 | 2,116 | 2,112 | 1 | 0 | 214 | 0 |
| [498](https://explorer.imd.fun/agents/498) | A | 433 | 432 | 429 | 3 | 0 | 214 | 1 |
| [499](https://explorer.imd.fun/agents/499) | ? | 103 | 103 | 103 | 0 | 0 | 0 | 0 |
| [501](https://explorer.imd.fun/agents/501) | C | 1,008 | 1,008 | 1,003 | 3 | 0 | 217 | 3 |
| [503](https://explorer.imd.fun/agents/503) | C | 3,584 | 3,583 | 3,557 | 4 | 1 | 217 | 2 |
| [507](https://explorer.imd.fun/agents/507) | A | 4 | 4 | 0 | 0 | 0 | 61 | 0 |
| [510](https://explorer.imd.fun/agents/510) | C | 3,122 | 3,122 | 3,117 | 2 | 0 | 216 | 0 |
| [511](https://explorer.imd.fun/agents/511) | C | 5 | 5 | 3 | 0 | 1 | 26 | 0 |
| [512](https://explorer.imd.fun/agents/512) | A | 29 | 29 | 29 | 0 | 0 | 137 | 0 |
| [513](https://explorer.imd.fun/agents/513) | C | 1 | 1 | 0 | 0 | 0 | 7 | 0 |
| [514](https://explorer.imd.fun/agents/514) | C | 1 | 1 | 1 | 0 | 0 | 127 | 0 |
| [516](https://explorer.imd.fun/agents/516) | A | 738 | 734 | 727 | 2 | 0 | 214 | 0 |
| [520](https://explorer.imd.fun/agents/520) | C | 33 | 33 | 33 | 0 | 0 | 158 | 0 |
| [523](https://explorer.imd.fun/agents/523) | A | 589 | 589 | 588 | 0 | 0 | 214 | 0 |
| [524](https://explorer.imd.fun/agents/524) | C | 2,751 | 2,750 | 2,731 | 1 | 1 | 216 | 0 |
| [525](https://explorer.imd.fun/agents/525) | C | 34 | 34 | 28 | 4 | 0 | 198 | 0 |
| [526](https://explorer.imd.fun/agents/526) | C | 1,318 | 1,317 | 1,312 | 2 | 0 | 217 | 0 |
| [527](https://explorer.imd.fun/agents/527) | A | 4,185 | 4,179 | 4,161 | 6 | 0 | 216 | 0 |
| [528](https://explorer.imd.fun/agents/528) | A | 3,496 | 3,495 | 3,463 | 4 | 1 | 217 | 0 |
| [530](https://explorer.imd.fun/agents/530) | C | 0 | 0 | 0 | 0 | 0 | 125 | 0 |
| [531](https://explorer.imd.fun/agents/531) | A | 2 | 2 | 0 | 1 | 0 | 75 | 1 |
| [534](https://explorer.imd.fun/agents/534) | C | 729 | 728 | 717 | 2 | 0 | 218 | 0 |
| [535](https://explorer.imd.fun/agents/535) | A | 1,220 | 1,219 | 1,200 | 11 | 0 | 218 | 0 |
| [539](https://explorer.imd.fun/agents/539) | A | 41 | 41 | 36 | 2 | 0 | 212 | 2 |
| [540](https://explorer.imd.fun/agents/540) | A | 2,281 | 2,280 | 2,260 | 11 | 0 | 216 | 2 |
| [541](https://explorer.imd.fun/agents/541) | A | 3 | 3 | 0 | 1 | 0 | 54 | 0 |
| [543](https://explorer.imd.fun/agents/543) | ? | 104 | 104 | 104 | 0 | 0 | 0 | 0 |
| [544](https://explorer.imd.fun/agents/544) | A | 417 | 415 | 400 | 7 | 0 | 217 | 0 |
| [545](https://explorer.imd.fun/agents/545) | C | 1,940 | 1,940 | 1,933 | 4 | 0 | 213 | 0 |
| [548](https://explorer.imd.fun/agents/548) | C | 3 | 3 | 0 | 1 | 0 | 95 | 0 |
| [550](https://explorer.imd.fun/agents/550) | A | 515 | 515 | 505 | 8 | 0 | 213 | 5 |
| [551](https://explorer.imd.fun/agents/551) | C | 715 | 714 | 710 | 1 | 0 | 214 | 0 |
| [552](https://explorer.imd.fun/agents/552) | ? | 1 | 1 | 0 | 0 | 0 | 62 | 0 |
| [555](https://explorer.imd.fun/agents/555) | C | 1 | 1 | 0 | 1 | 0 | 79 | 1 |
| [558](https://explorer.imd.fun/agents/558) | A | 28 | 27 | 19 | 3 | 1 | 96 | 0 |
| [559](https://explorer.imd.fun/agents/559) | A | 3,427 | 3,425 | 3,390 | 11 | 1 | 215 | 1 |
| [560](https://explorer.imd.fun/agents/560) | A | 35 | 35 | 18 | 6 | 0 | 215 | 2 |
| [563](https://explorer.imd.fun/agents/563) | A | 3 | 3 | 0 | 0 | 0 | 22 | 0 |
| [565](https://explorer.imd.fun/agents/565) | C | 0 | 0 | 0 | 0 | 0 | 125 | 0 |
| [566](https://explorer.imd.fun/agents/566) | C | 0 | 0 | 0 | 0 | 0 | 126 | 0 |
| [570](https://explorer.imd.fun/agents/570) | C | 0 | 0 | 0 | 0 | 0 | 26 | 0 |
| [571](https://explorer.imd.fun/agents/571) | C | 35 | 34 | 30 | 2 | 0 | 199 | 2 |
| [572](https://explorer.imd.fun/agents/572) | C | 1,158 | 1,158 | 1,139 | 2 | 1 | 213 | 0 |
| [573](https://explorer.imd.fun/agents/573) | A | 53 | 52 | 44 | 4 | 0 | 191 | 1 |
| [575](https://explorer.imd.fun/agents/575) | A | 35 | 34 | 33 | 0 | 0 | 161 | 0 |
| [576](https://explorer.imd.fun/agents/576) | C | 14 | 14 | 14 | 0 | 0 | 156 | 0 |
| [579](https://explorer.imd.fun/agents/579) | ? | 1,329 | 1,326 | 1,300 | 14 | 0 | 162 | 0 |
| [581](https://explorer.imd.fun/agents/581) | A | 515 | 515 | 503 | 8 | 0 | 202 | 3 |
| [585](https://explorer.imd.fun/agents/585) | A | 25 | 25 | 24 | 0 | 0 | 166 | 0 |
| [586](https://explorer.imd.fun/agents/586) | A | 740 | 739 | 723 | 9 | 0 | 217 | 0 |
| [587](https://explorer.imd.fun/agents/587) | C | 16 | 16 | 16 | 0 | 0 | 177 | 0 |
| [588](https://explorer.imd.fun/agents/588) | A | 35 | 34 | 21 | 6 | 0 | 179 | 1 |
| [589](https://explorer.imd.fun/agents/589) | C | 4 | 4 | 3 | 1 | 0 | 71 | 0 |
| [590](https://explorer.imd.fun/agents/590) | C | 980 | 980 | 968 | 0 | 0 | 217 | 0 |
| [591](https://explorer.imd.fun/agents/591) | C | 1,552 | 1,551 | 1,535 | 3 | 1 | 216 | 0 |
| [592](https://explorer.imd.fun/agents/592) | C | 1,282 | 1,280 | 1,249 | 8 | 1 | 213 | 0 |
| [593](https://explorer.imd.fun/agents/593) | C | 11 | 11 | 11 | 0 | 0 | 177 | 0 |
| [595](https://explorer.imd.fun/agents/595) | A | 2,162 | 2,160 | 2,144 | 6 | 0 | 216 | 2 |
| [596](https://explorer.imd.fun/agents/596) | C | 1,823 | 1,823 | 1,805 | 1 | 1 | 215 | 0 |
| [598](https://explorer.imd.fun/agents/598) | A | 1,366 | 1,366 | 1,352 | 0 | 1 | 215 | 0 |
| [599](https://explorer.imd.fun/agents/599) | C | 143 | 143 | 137 | 1 | 0 | 216 | 0 |
| [604](https://explorer.imd.fun/agents/604) | C | 75 | 75 | 71 | 0 | 0 | 217 | 0 |
| [605](https://explorer.imd.fun/agents/605) | ? | 867 | 866 | 866 | 0 | 0 | 0 | 0 |
| [606](https://explorer.imd.fun/agents/606) | A | 2,025 | 2,024 | 2,006 | 9 | 0 | 215 | 1 |
| [607](https://explorer.imd.fun/agents/607) | C | 1,688 | 1,688 | 1,684 | 2 | 0 | 199 | 1 |
| [608](https://explorer.imd.fun/agents/608) | C | 675 | 675 | 669 | 3 | 0 | 214 | 0 |
| [613](https://explorer.imd.fun/agents/613) | C | 3,253 | 3,251 | 3,234 | 1 | 1 | 214 | 0 |
| [614](https://explorer.imd.fun/agents/614) | C | 401 | 400 | 397 | 2 | 0 | 217 | 0 |
| [616](https://explorer.imd.fun/agents/616) | C | 2,512 | 2,511 | 2,497 | 1 | 0 | 213 | 0 |
| [617](https://explorer.imd.fun/agents/617) | C | 1,125 | 1,118 | 1,066 | 40 | 0 | 217 | 0 |
| [618](https://explorer.imd.fun/agents/618) | C | 1 | 1 | 1 | 0 | 0 | 123 | 0 |
| [623](https://explorer.imd.fun/agents/623) | A | 44 | 42 | 42 | 0 | 0 | 168 | 0 |
| [625](https://explorer.imd.fun/agents/625) | C | 1,234 | 1,233 | 1,213 | 1 | 1 | 216 | 0 |
| [626](https://explorer.imd.fun/agents/626) | A | 476 | 475 | 468 | 5 | 0 | 213 | 0 |
| [629](https://explorer.imd.fun/agents/629) | A | 34 | 33 | 17 | 6 | 0 | 216 | 0 |
| [631](https://explorer.imd.fun/agents/631) | A | 1,609 | 1,608 | 1,600 | 4 | 0 | 215 | 0 |
| [632](https://explorer.imd.fun/agents/632) | ? | 14 | 13 | 0 | 8 | 0 | 201 | 0 |
| [635](https://explorer.imd.fun/agents/635) | C | 1,891 | 1,891 | 1,889 | 0 | 0 | 214 | 0 |
| [636](https://explorer.imd.fun/agents/636) | A | 31 | 31 | 23 | 3 | 0 | 188 | 2 |
| [637](https://explorer.imd.fun/agents/637) | C | 3,166 | 3,165 | 3,159 | 4 | 0 | 214 | 0 |
| [638](https://explorer.imd.fun/agents/638) | ? | 1,243 | 1,241 | 1,236 | 2 | 0 | 37 | 0 |
| [640](https://explorer.imd.fun/agents/640) | ? | 691 | 691 | 684 | 0 | 0 | 78 | 0 |
| [641](https://explorer.imd.fun/agents/641) | A | 4 | 4 | 0 | 2 | 0 | 65 | 0 |
| [644](https://explorer.imd.fun/agents/644) | A | 31 | 31 | 30 | 0 | 0 | 190 | 0 |
| [646](https://explorer.imd.fun/agents/646) | A | 19 | 19 | 11 | 3 | 0 | 138 | 0 |
| [649](https://explorer.imd.fun/agents/649) | C | 1,145 | 1,144 | 1,137 | 5 | 0 | 216 | 0 |
| [650](https://explorer.imd.fun/agents/650) | A | 7 | 6 | 1 | 4 | 0 | 81 | 1 |
| [652](https://explorer.imd.fun/agents/652) | C | 1,377 | 1,377 | 1,354 | 2 | 1 | 215 | 0 |
| [656](https://explorer.imd.fun/agents/656) | A | 40 | 39 | 32 | 4 | 0 | 65 | 0 |
| [658](https://explorer.imd.fun/agents/658) | C | 1,322 | 1,322 | 1,298 | 5 | 1 | 216 | 0 |
| [659](https://explorer.imd.fun/agents/659) | C | 16 | 16 | 16 | 0 | 0 | 191 | 0 |
| [660](https://explorer.imd.fun/agents/660) | A | 2,786 | 2,785 | 2,764 | 5 | 0 | 217 | 0 |
| [661](https://explorer.imd.fun/agents/661) | C | 1,878 | 1,878 | 1,876 | 0 | 0 | 216 | 0 |
| [662](https://explorer.imd.fun/agents/662) | A | 15 | 15 | 15 | 0 | 0 | 136 | 0 |
| [668](https://explorer.imd.fun/agents/668) | C | 3,259 | 3,256 | 3,238 | 1 | 1 | 215 | 0 |
| [671](https://explorer.imd.fun/agents/671) | A | 2,053 | 2,052 | 2,034 | 4 | 0 | 214 | 1 |
| [672](https://explorer.imd.fun/agents/672) | C | 0 | 0 | 0 | 0 | 0 | 122 | 0 |
| [673](https://explorer.imd.fun/agents/673) | C | 1,025 | 1,025 | 1,019 | 2 | 0 | 215 | 0 |
| [676](https://explorer.imd.fun/agents/676) | C | 1 | 1 | 0 | 1 | 0 | 30 | 0 |
| [678](https://explorer.imd.fun/agents/678) | C | 15 | 15 | 14 | 0 | 0 | 69 | 0 |
| [681](https://explorer.imd.fun/agents/681) | C | 0 | 0 | 0 | 0 | 0 | 126 | 0 |
| [682](https://explorer.imd.fun/agents/682) | C | 3 | 3 | 1 | 0 | 0 | 83 | 0 |
| [683](https://explorer.imd.fun/agents/683) | C | 1,146 | 1,144 | 1,139 | 2 | 0 | 217 | 0 |
| [684](https://explorer.imd.fun/agents/684) | C | 1,160 | 1,159 | 1,141 | 2 | 1 | 214 | 0 |
| [686](https://explorer.imd.fun/agents/686) | C | 775 | 775 | 771 | 0 | 0 | 213 | 0 |
| [687](https://explorer.imd.fun/agents/687) | A | 31 | 28 | 13 | 8 | 0 | 198 | 1 |
| [688](https://explorer.imd.fun/agents/688) | C | 95 | 95 | 91 | 2 | 0 | 199 | 0 |
| [690](https://explorer.imd.fun/agents/690) | A | 99 | 98 | 87 | 6 | 0 | 216 | 0 |
| [693](https://explorer.imd.fun/agents/693) | C | 18 | 18 | 18 | 0 | 0 | 168 | 0 |
| [694](https://explorer.imd.fun/agents/694) | A | 4 | 4 | 0 | 0 | 0 | 61 | 0 |
| [695](https://explorer.imd.fun/agents/695) | C | 1,854 | 1,853 | 1,848 | 2 | 0 | 214 | 0 |
| [697](https://explorer.imd.fun/agents/697) | ? | 263 | 262 | 262 | 0 | 0 | 0 | 0 |
| [700](https://explorer.imd.fun/agents/700) | C | 61 | 60 | 56 | 0 | 0 | 178 | 0 |
| [701](https://explorer.imd.fun/agents/701) | C | 682 | 682 | 679 | 1 | 0 | 214 | 1 |
| [704](https://explorer.imd.fun/agents/704) | A | 541 | 539 | 521 | 13 | 0 | 211 | 2 |
| [705](https://explorer.imd.fun/agents/705) | C | 3,310 | 3,310 | 3,295 | 3 | 0 | 217 | 3 |
| [706](https://explorer.imd.fun/agents/706) | A | 1,455 | 1,455 | 1,454 | 0 | 0 | 214 | 0 |
| [708](https://explorer.imd.fun/agents/708) | C | 809 | 809 | 808 | 1 | 0 | 196 | 0 |
| [709](https://explorer.imd.fun/agents/709) | C | 1,091 | 1,090 | 1,085 | 2 | 0 | 217 | 0 |
| [710](https://explorer.imd.fun/agents/710) | C | 59 | 59 | 54 | 2 | 0 | 216 | 0 |
| [711](https://explorer.imd.fun/agents/711) | C | 407 | 407 | 401 | 1 | 0 | 214 | 0 |
| [712](https://explorer.imd.fun/agents/712) | C | 1,001 | 1,001 | 996 | 4 | 0 | 215 | 0 |
| [713](https://explorer.imd.fun/agents/713) | ? | 1,166 | 1,166 | 1,161 | 2 | 0 | 215 | 0 |
| [714](https://explorer.imd.fun/agents/714) | C | 1,202 | 1,202 | 1,197 | 1 | 0 | 218 | 0 |
| [715](https://explorer.imd.fun/agents/715) | A | 3,429 | 3,428 | 3,398 | 7 | 0 | 213 | 2 |
| [716](https://explorer.imd.fun/agents/716) | C | 10 | 10 | 10 | 0 | 0 | 194 | 0 |
| [717](https://explorer.imd.fun/agents/717) | C | 16 | 16 | 12 | 1 | 1 | 39 | 0 |
| [718](https://explorer.imd.fun/agents/718) | C | 3,636 | 3,635 | 3,610 | 6 | 1 | 216 | 0 |
| [719](https://explorer.imd.fun/agents/719) | C | 31 | 31 | 29 | 0 | 0 | 134 | 0 |
| [720](https://explorer.imd.fun/agents/720) | A | 39 | 39 | 36 | 0 | 0 | 190 | 0 |
| [721](https://explorer.imd.fun/agents/721) | C | 3,117 | 3,115 | 3,095 | 2 | 1 | 215 | 0 |
| [722](https://explorer.imd.fun/agents/722) | C | 1,654 | 1,653 | 1,648 | 2 | 0 | 216 | 0 |
| [724](https://explorer.imd.fun/agents/724) | A | 1,298 | 1,295 | 1,278 | 9 | 0 | 214 | 0 |
| [725](https://explorer.imd.fun/agents/725) | C | 1 | 1 | 1 | 0 | 0 | 124 | 0 |
| [727](https://explorer.imd.fun/agents/727) | A | 26 | 25 | 8 | 7 | 0 | 218 | 2 |
| [729](https://explorer.imd.fun/agents/729) | A | 3,784 | 3,782 | 3,767 | 7 | 0 | 218 | 0 |
| [730](https://explorer.imd.fun/agents/730) | A | 30 | 30 | 23 | 3 | 0 | 216 | 1 |
| [734](https://explorer.imd.fun/agents/734) | C | 1,003 | 1,003 | 998 | 2 | 0 | 216 | 0 |
| [735](https://explorer.imd.fun/agents/735) | A | 3,628 | 3,626 | 3,599 | 10 | 0 | 216 | 0 |
| [737](https://explorer.imd.fun/agents/737) | C | 1,736 | 1,736 | 1,732 | 0 | 0 | 217 | 0 |
| [738](https://explorer.imd.fun/agents/738) | C | 10 | 9 | 0 | 1 | 0 | 110 | 0 |
| [740](https://explorer.imd.fun/agents/740) | C | 1 | 1 | 0 | 0 | 0 | 25 | 0 |
| [743](https://explorer.imd.fun/agents/743) | ? | 17 | 16 | 9 | 3 | 0 | 72 | 0 |
| [745](https://explorer.imd.fun/agents/745) | C | 0 | 0 | 0 | 0 | 0 | 123 | 0 |
| [746](https://explorer.imd.fun/agents/746) | C | 1 | 1 | 1 | 0 | 0 | 126 | 0 |
| [747](https://explorer.imd.fun/agents/747) | C | 0 | 0 | 0 | 0 | 0 | 7 | 0 |
| [748](https://explorer.imd.fun/agents/748) | A | 74 | 73 | 50 | 8 | 0 | 201 | 0 |
| [750](https://explorer.imd.fun/agents/750) | A | 0 | 0 | 0 | 0 | 0 | 139 | 0 |
| [751](https://explorer.imd.fun/agents/751) | A | 1,156 | 1,156 | 1,155 | 0 | 0 | 214 | 0 |
| [754](https://explorer.imd.fun/agents/754) | A | 31 | 29 | 22 | 5 | 0 | 202 | 0 |
| [756](https://explorer.imd.fun/agents/756) | C | 1,019 | 1,018 | 1,003 | 1 | 0 | 216 | 0 |
| [757](https://explorer.imd.fun/agents/757) | A | 445 | 445 | 439 | 2 | 0 | 216 | 1 |
| [758](https://explorer.imd.fun/agents/758) | C | 2 | 2 | 2 | 0 | 0 | 126 | 0 |
| [759](https://explorer.imd.fun/agents/759) | A | 2,629 | 2,626 | 2,610 | 7 | 0 | 216 | 1 |
| [760](https://explorer.imd.fun/agents/760) | A | 3,510 | 3,509 | 3,487 | 6 | 0 | 216 | 1 |
| [763](https://explorer.imd.fun/agents/763) | C | 0 | 0 | 0 | 0 | 0 | 123 | 0 |
| [766](https://explorer.imd.fun/agents/766) | A | 458 | 456 | 446 | 7 | 0 | 210 | 3 |
| [770](https://explorer.imd.fun/agents/770) | C | 1 | 1 | 0 | 1 | 0 | 18 | 0 |
| [773](https://explorer.imd.fun/agents/773) | C | 1 | 1 | 1 | 0 | 0 | 68 | 0 |
| [775](https://explorer.imd.fun/agents/775) | C | 16 | 16 | 16 | 0 | 0 | 156 | 0 |
| [776](https://explorer.imd.fun/agents/776) | ? | 744 | 744 | 727 | 2 | 1 | 171 | 0 |
| [777](https://explorer.imd.fun/agents/777) | A | 1,697 | 1,694 | 1,682 | 0 | 0 | 214 | 0 |
| [779](https://explorer.imd.fun/agents/779) | A | 22 | 22 | 22 | 0 | 0 | 137 | 0 |
| [781](https://explorer.imd.fun/agents/781) | C | 2,129 | 2,128 | 2,123 | 3 | 0 | 216 | 0 |
| [783](https://explorer.imd.fun/agents/783) | C | 3,236 | 3,235 | 3,217 | 2 | 1 | 217 | 1 |
| [784](https://explorer.imd.fun/agents/784) | A | 7 | 5 | 0 | 4 | 0 | 73 | 4 |
| [785](https://explorer.imd.fun/agents/785) | C | 1,130 | 1,130 | 1,123 | 4 | 0 | 219 | 0 |
| [786](https://explorer.imd.fun/agents/786) | C | 1,945 | 1,945 | 1,940 | 3 | 0 | 214 | 0 |
| [788](https://explorer.imd.fun/agents/788) | A | 50 | 49 | 34 | 6 | 0 | 190 | 3 |
| [789](https://explorer.imd.fun/agents/789) | C | 15 | 15 | 15 | 0 | 0 | 195 | 0 |
| [791](https://explorer.imd.fun/agents/791) | C | 1,443 | 1,443 | 1,439 | 2 | 0 | 217 | 0 |
| [792](https://explorer.imd.fun/agents/792) | C | 24 | 24 | 19 | 3 | 0 | 189 | 3 |
| [794](https://explorer.imd.fun/agents/794) | A | 65 | 61 | 61 | 0 | 0 | 167 | 0 |
| [795](https://explorer.imd.fun/agents/795) | A | 1,655 | 1,654 | 1,636 | 7 | 0 | 218 | 0 |
| [798](https://explorer.imd.fun/agents/798) | A | 3,522 | 3,522 | 3,498 | 5 | 0 | 215 | 2 |
| [800](https://explorer.imd.fun/agents/800) | A | 1,202 | 1,202 | 1,191 | 0 | 0 | 218 | 0 |
| [801](https://explorer.imd.fun/agents/801) | ? | 12 | 11 | 0 | 6 | 0 | 200 | 0 |
| [804](https://explorer.imd.fun/agents/804) | C | 1,469 | 1,469 | 1,453 | 2 | 1 | 217 | 0 |
| [806](https://explorer.imd.fun/agents/806) | C | 577 | 577 | 572 | 1 | 0 | 153 | 0 |
| [807](https://explorer.imd.fun/agents/807) | C | 552 | 551 | 546 | 2 | 0 | 216 | 0 |
| [808](https://explorer.imd.fun/agents/808) | A | 35 | 34 | 16 | 8 | 0 | 215 | 2 |
| [809](https://explorer.imd.fun/agents/809) | A | 2,116 | 2,112 | 2,099 | 6 | 0 | 210 | 0 |
| [810](https://explorer.imd.fun/agents/810) | A | 2 | 1 | 0 | 2 | 0 | 76 | 0 |
| [812](https://explorer.imd.fun/agents/812) | C | 3,350 | 3,349 | 3,333 | 2 | 1 | 217 | 0 |
| [813](https://explorer.imd.fun/agents/813) | C | 1,067 | 1,067 | 1,062 | 1 | 0 | 214 | 0 |
| [818](https://explorer.imd.fun/agents/818) | C | 9 | 9 | 0 | 1 | 1 | 98 | 0 |
| [820](https://explorer.imd.fun/agents/820) | C | 67 | 67 | 51 | 2 | 1 | 211 | 0 |
| [821](https://explorer.imd.fun/agents/821) | ? | 51 | 51 | 49 | 0 | 0 | 63 | 0 |
| [822](https://explorer.imd.fun/agents/822) | A | 56 | 56 | 38 | 6 | 0 | 191 | 2 |
| [823](https://explorer.imd.fun/agents/823) | C | 1,065 | 1,063 | 1,048 | 2 | 0 | 216 | 0 |
| [824](https://explorer.imd.fun/agents/824) | C | 38 | 38 | 38 | 0 | 0 | 170 | 0 |
| [826](https://explorer.imd.fun/agents/826) | A | 117 | 116 | 100 | 10 | 0 | 215 | 0 |
| [827](https://explorer.imd.fun/agents/827) | C | 2,825 | 2,825 | 2,818 | 2 | 0 | 215 | 0 |
| [829](https://explorer.imd.fun/agents/829) | C | 1,115 | 1,114 | 1,109 | 4 | 0 | 215 | 0 |
| [831](https://explorer.imd.fun/agents/831) | C | 1,052 | 1,052 | 1,048 | 0 | 0 | 215 | 0 |
| [832](https://explorer.imd.fun/agents/832) | A | 14 | 14 | 12 | 0 | 0 | 200 | 0 |
| [833](https://explorer.imd.fun/agents/833) | C | 16 | 16 | 16 | 0 | 0 | 178 | 0 |
| [834](https://explorer.imd.fun/agents/834) | C | 0 | 0 | 0 | 0 | 0 | 122 | 0 |
| [835](https://explorer.imd.fun/agents/835) | C | 3,409 | 3,408 | 3,389 | 1 | 0 | 213 | 0 |
| [838](https://explorer.imd.fun/agents/838) | C | 0 | 0 | 0 | 0 | 0 | 69 | 0 |
| [840](https://explorer.imd.fun/agents/840) | A | 0 | 0 | 0 | 0 | 0 | 139 | 0 |
| [842](https://explorer.imd.fun/agents/842) | C | 3,589 | 3,589 | 3,573 | 0 | 1 | 217 | 0 |
| [843](https://explorer.imd.fun/agents/843) | A | 21 | 21 | 20 | 0 | 0 | 198 | 0 |
| [846](https://explorer.imd.fun/agents/846) | C | 1,853 | 1,853 | 1,847 | 3 | 0 | 216 | 0 |
| [847](https://explorer.imd.fun/agents/847) | C | 1,759 | 1,755 | 1,742 | 3 | 1 | 216 | 0 |
| [849](https://explorer.imd.fun/agents/849) | C | 1,101 | 1,098 | 1,086 | 1 | 0 | 217 | 1 |
| [850](https://explorer.imd.fun/agents/850) | C | 15 | 15 | 15 | 0 | 0 | 155 | 0 |
| [852](https://explorer.imd.fun/agents/852) | A | 33 | 33 | 16 | 8 | 0 | 217 | 1 |
| [853](https://explorer.imd.fun/agents/853) | A | 12 | 12 | 12 | 0 | 0 | 140 | 0 |
| [855](https://explorer.imd.fun/agents/855) | A | 20 | 20 | 20 | 0 | 0 | 136 | 0 |
| [857](https://explorer.imd.fun/agents/857) | ? | 672 | 672 | 671 | 0 | 0 | 69 | 0 |
| [858](https://explorer.imd.fun/agents/858) | C | 777 | 777 | 771 | 2 | 0 | 212 | 1 |
| [861](https://explorer.imd.fun/agents/861) | C | 644 | 644 | 640 | 2 | 0 | 216 | 2 |
| [862](https://explorer.imd.fun/agents/862) | C | 2,661 | 2,661 | 2,646 | 0 | 0 | 215 | 0 |
| [863](https://explorer.imd.fun/agents/863) | A | 2,324 | 2,319 | 2,301 | 10 | 0 | 214 | 2 |
| [864](https://explorer.imd.fun/agents/864) | C | 51 | 51 | 51 | 0 | 0 | 179 | 0 |
| [865](https://explorer.imd.fun/agents/865) | A | 5 | 5 | 1 | 2 | 0 | 83 | 1 |
| [866](https://explorer.imd.fun/agents/866) | A | 2,178 | 2,176 | 2,156 | 9 | 0 | 214 | 3 |
| [869](https://explorer.imd.fun/agents/869) | A | 37 | 36 | 19 | 5 | 0 | 216 | 3 |
| [871](https://explorer.imd.fun/agents/871) | A | 351 | 348 | 331 | 8 | 0 | 203 | 0 |
| [873](https://explorer.imd.fun/agents/873) | C | 4 | 4 | 3 | 0 | 0 | 174 | 0 |
| [874](https://explorer.imd.fun/agents/874) | A | 61 | 60 | 47 | 5 | 0 | 215 | 0 |
| [876](https://explorer.imd.fun/agents/876) | C | 11 | 11 | 11 | 0 | 0 | 191 | 0 |
| [877](https://explorer.imd.fun/agents/877) | A | 431 | 430 | 422 | 5 | 0 | 209 | 2 |
| [878](https://explorer.imd.fun/agents/878) | C | 14 | 14 | 14 | 0 | 0 | 175 | 0 |
| [879](https://explorer.imd.fun/agents/879) | A | 1,243 | 1,243 | 1,225 | 6 | 0 | 218 | 1 |
| [880](https://explorer.imd.fun/agents/880) | A | 3,648 | 3,641 | 3,625 | 8 | 0 | 217 | 0 |
| [884](https://explorer.imd.fun/agents/884) | A | 0 | 0 | 0 | 0 | 0 | 66 | 0 |
| [886](https://explorer.imd.fun/agents/886) | C | 1,172 | 1,171 | 1,155 | 1 | 1 | 217 | 0 |
| [887](https://explorer.imd.fun/agents/887) | C | 763 | 762 | 756 | 2 | 0 | 214 | 0 |
| [889](https://explorer.imd.fun/agents/889) | C | 1 | 1 | 0 | 0 | 0 | 204 | 0 |
| [890](https://explorer.imd.fun/agents/890) | A | 0 | 0 | 0 | 0 | 0 | 66 | 0 |
| [891](https://explorer.imd.fun/agents/891) | ? | 551 | 550 | 549 | 0 | 0 | 162 | 0 |
| [894](https://explorer.imd.fun/agents/894) | C | 45 | 45 | 42 | 0 | 0 | 65 | 0 |
| [896](https://explorer.imd.fun/agents/896) | C | 103 | 103 | 97 | 0 | 0 | 194 | 0 |
| [897](https://explorer.imd.fun/agents/897) | C | 2,816 | 2,815 | 2,798 | 2 | 1 | 211 | 0 |
| [900](https://explorer.imd.fun/agents/900) | A | 37 | 37 | 26 | 5 | 0 | 204 | 0 |
| [901](https://explorer.imd.fun/agents/901) | C | 1,102 | 1,101 | 1,078 | 2 | 1 | 214 | 0 |
| [905](https://explorer.imd.fun/agents/905) | C | 1,741 | 1,741 | 1,735 | 3 | 0 | 213 | 0 |
| [909](https://explorer.imd.fun/agents/909) | C | 8 | 8 | 6 | 2 | 0 | 69 | 2 |
| [911](https://explorer.imd.fun/agents/911) | A | 450 | 450 | 443 | 5 | 0 | 210 | 1 |
| [912](https://explorer.imd.fun/agents/912) | A | 3,141 | 3,137 | 3,114 | 7 | 0 | 216 | 0 |
| [916](https://explorer.imd.fun/agents/916) | C | 632 | 632 | 629 | 0 | 0 | 217 | 0 |
| [918](https://explorer.imd.fun/agents/918) | C | 15 | 15 | 15 | 0 | 0 | 157 | 0 |
| [921](https://explorer.imd.fun/agents/921) | C | 1,006 | 1,006 | 1,001 | 3 | 0 | 214 | 0 |
| [922](https://explorer.imd.fun/agents/922) | C | 428 | 428 | 427 | 0 | 0 | 215 | 0 |
| [923](https://explorer.imd.fun/agents/923) | C | 1,063 | 1,061 | 1,043 | 2 | 1 | 216 | 0 |
| [926](https://explorer.imd.fun/agents/926) | A | 1,348 | 1,347 | 1,328 | 4 | 0 | 219 | 0 |
| [931](https://explorer.imd.fun/agents/931) | C | 711 | 711 | 705 | 3 | 0 | 216 | 2 |
| [934](https://explorer.imd.fun/agents/934) | ? | Unknown | Unknown | Unknown | Unknown | Unknown | 0 | 0 |
| [935](https://explorer.imd.fun/agents/935) | C | 1,045 | 1,045 | 1,039 | 2 | 0 | 216 | 2 |
| [938](https://explorer.imd.fun/agents/938) | A | 1,020 | 1,020 | 1,015 | 2 | 0 | 215 | 0 |
| [939](https://explorer.imd.fun/agents/939) | A | 2,901 | 2,896 | 2,884 | 7 | 0 | 153 | 0 |
| [942](https://explorer.imd.fun/agents/942) | C | 14 | 14 | 14 | 0 | 0 | 178 | 0 |
| [943](https://explorer.imd.fun/agents/943) | C | 70 | 69 | 66 | 1 | 0 | 216 | 0 |
| [946](https://explorer.imd.fun/agents/946) | C | 2,368 | 2,363 | 2,346 | 2 | 1 | 217 | 0 |
| [948](https://explorer.imd.fun/agents/948) | C | 2,029 | 2,029 | 2,023 | 2 | 0 | 216 | 0 |
| [952](https://explorer.imd.fun/agents/952) | C | 13 | 13 | 13 | 0 | 0 | 166 | 0 |
| [953](https://explorer.imd.fun/agents/953) | C | 3,007 | 3,007 | 2,988 | 2 | 1 | 213 | 0 |
| [954](https://explorer.imd.fun/agents/954) | A | 479 | 478 | 469 | 7 | 0 | 206 | 4 |
| [956](https://explorer.imd.fun/agents/956) | A | 8 | 7 | 0 | 2 | 0 | 135 | 0 |
| [959](https://explorer.imd.fun/agents/959) | A | 32 | 32 | 17 | 6 | 0 | 217 | 0 |
| [960](https://explorer.imd.fun/agents/960) | A | 22 | 22 | 20 | 0 | 0 | 195 | 0 |
| [961](https://explorer.imd.fun/agents/961) | C | 677 | 676 | 673 | 2 | 0 | 213 | 0 |
| [962](https://explorer.imd.fun/agents/962) | C | 13 | 13 | 13 | 0 | 0 | 194 | 0 |
| [963](https://explorer.imd.fun/agents/963) | A | 812 | 812 | 804 | 2 | 0 | 217 | 0 |
| [965](https://explorer.imd.fun/agents/965) | A | 466 | 465 | 458 | 3 | 0 | 214 | 2 |
| [967](https://explorer.imd.fun/agents/967) | A | 378 | 378 | 364 | 10 | 0 | 164 | 0 |
| [969](https://explorer.imd.fun/agents/969) | A | 1,500 | 1,500 | 1,486 | 5 | 0 | 216 | 0 |
| [970](https://explorer.imd.fun/agents/970) | A | 461 | 461 | 455 | 2 | 0 | 219 | 1 |
| [972](https://explorer.imd.fun/agents/972) | A | 30 | 30 | 30 | 0 | 0 | 166 | 0 |
| [973](https://explorer.imd.fun/agents/973) | C | 1,062 | 1,062 | 1,042 | 1 | 1 | 214 | 0 |
| [974](https://explorer.imd.fun/agents/974) | C | 65 | 65 | 58 | 5 | 0 | 193 | 0 |
| [976](https://explorer.imd.fun/agents/976) | A | 19 | 18 | 8 | 2 | 0 | 201 | 1 |
| [978](https://explorer.imd.fun/agents/978) | A | 518 | 516 | 508 | 3 | 0 | 216 | 1 |
| [982](https://explorer.imd.fun/agents/982) | C | 1 | 1 | 1 | 0 | 0 | 119 | 0 |
| [984](https://explorer.imd.fun/agents/984) | C | 609 | 608 | 603 | 2 | 0 | 213 | 0 |
| [985](https://explorer.imd.fun/agents/985) | C | 267 | 266 | 261 | 3 | 0 | 215 | 0 |
| [986](https://explorer.imd.fun/agents/986) | ? | 1,215 | 1,215 | 1,211 | 1 | 0 | 44 | 0 |
| [987](https://explorer.imd.fun/agents/987) | C | 15 | 15 | 11 | 2 | 0 | 71 | 2 |
| [989](https://explorer.imd.fun/agents/989) | C | 699 | 699 | 693 | 4 | 0 | 212 | 1 |
| [990](https://explorer.imd.fun/agents/990) | A | 1,346 | 1,345 | 1,343 | 0 | 0 | 211 | 0 |
| [992](https://explorer.imd.fun/agents/992) | C | 1 | 1 | 0 | 1 | 0 | 40 | 1 |
| [993](https://explorer.imd.fun/agents/993) | C | 726 | 726 | 720 | 3 | 0 | 216 | 2 |
| [998](https://explorer.imd.fun/agents/998) | C | 688 | 688 | 684 | 0 | 0 | 217 | 0 |
| [999](https://explorer.imd.fun/agents/999) | A | 51 | 49 | 33 | 10 | 0 | 185 | 1 |
| [1000](https://explorer.imd.fun/agents/1000) | A | 1,831 | 1,831 | 1,812 | 8 | 0 | 217 | 1 |
| [1001](https://explorer.imd.fun/agents/1001) | A | 1,779 | 1,778 | 1,769 | 3 | 0 | 215 | 0 |
| [1003](https://explorer.imd.fun/agents/1003) | C | 702 | 702 | 699 | 1 | 0 | 219 | 1 |
| [1004](https://explorer.imd.fun/agents/1004) | A | 2 | 2 | 0 | 1 | 0 | 74 | 1 |
| [1006](https://explorer.imd.fun/agents/1006) | C | 1,528 | 1,527 | 1,523 | 1 | 0 | 189 | 1 |
| [1007](https://explorer.imd.fun/agents/1007) | C | 64 | 63 | 54 | 1 | 1 | 187 | 0 |
| [1010](https://explorer.imd.fun/agents/1010) | C | 1,769 | 1,768 | 1,752 | 1 | 1 | 215 | 0 |
| [1013](https://explorer.imd.fun/agents/1013) | C | 60 | 60 | 46 | 1 | 1 | 198 | 0 |
| [1014](https://explorer.imd.fun/agents/1014) | A | 9 | 7 | 3 | 2 | 0 | 62 | 0 |
| [1015](https://explorer.imd.fun/agents/1015) | C | 14 | 14 | 14 | 0 | 0 | 156 | 0 |
| [1016](https://explorer.imd.fun/agents/1016) | A | 120 | 120 | 104 | 4 | 0 | 198 | 1 |
| [1017](https://explorer.imd.fun/agents/1017) | A | 1,210 | 1,210 | 1,203 | 2 | 0 | 217 | 0 |
| [1018](https://explorer.imd.fun/agents/1018) | C | 18 | 18 | 18 | 0 | 0 | 158 | 0 |
| [1020](https://explorer.imd.fun/agents/1020) | C | 3,401 | 3,397 | 3,379 | 2 | 1 | 214 | 0 |
| [1022](https://explorer.imd.fun/agents/1022) | A | 518 | 518 | 516 | 0 | 0 | 215 | 0 |
| [1023](https://explorer.imd.fun/agents/1023) | A | 54 | 54 | 37 | 5 | 0 | 188 | 2 |
| [1024](https://explorer.imd.fun/agents/1024) | C | 0 | 0 | 0 | 0 | 0 | 124 | 0 |
| [1025](https://explorer.imd.fun/agents/1025) | C | 3,938 | 3,934 | 3,915 | 17 | 0 | 218 | 0 |
| [1029](https://explorer.imd.fun/agents/1029) | C | 0 | 0 | 0 | 0 | 0 | 123 | 0 |
| [1030](https://explorer.imd.fun/agents/1030) | A | 7 | 6 | 0 | 3 | 0 | 73 | 2 |
| [1031](https://explorer.imd.fun/agents/1031) | A | 32 | 31 | 31 | 0 | 0 | 166 | 0 |
| [1032](https://explorer.imd.fun/agents/1032) | ? | 529 | 529 | 528 | 0 | 0 | 0 | 0 |
| [1033](https://explorer.imd.fun/agents/1033) | A | 89 | 88 | 88 | 0 | 0 | 167 | 0 |
| [1034](https://explorer.imd.fun/agents/1034) | C | 3,469 | 3,468 | 3,450 | 1 | 1 | 217 | 1 |
| [1038](https://explorer.imd.fun/agents/1038) | C | 1,578 | 1,578 | 1,573 | 2 | 0 | 212 | 0 |
| [1039](https://explorer.imd.fun/agents/1039) | C | 1,440 | 1,440 | 1,425 | 1 | 1 | 215 | 0 |
| [1040](https://explorer.imd.fun/agents/1040) | C | 888 | 887 | 882 | 2 | 0 | 213 | 1 |
| [1042](https://explorer.imd.fun/agents/1042) | A | 1,768 | 1,768 | 1,747 | 8 | 0 | 217 | 1 |
| [1044](https://explorer.imd.fun/agents/1044) | ? | 0 | 0 | 0 | 0 | 0 | 32 | 0 |
| [1046](https://explorer.imd.fun/agents/1046) | A | 18 | 18 | 17 | 0 | 0 | 166 | 0 |
| [1049](https://explorer.imd.fun/agents/1049) | C | 2,560 | 2,560 | 2,543 | 1 | 1 | 216 | 0 |
| [1050](https://explorer.imd.fun/agents/1050) | A | 46 | 45 | 26 | 5 | 0 | 213 | 0 |
| [1053](https://explorer.imd.fun/agents/1053) | A | 3 | 3 | 2 | 0 | 0 | 118 | 0 |
| [1056](https://explorer.imd.fun/agents/1056) | A | 16 | 16 | 15 | 0 | 0 | 145 | 0 |
| [1058](https://explorer.imd.fun/agents/1058) | C | 13 | 13 | 13 | 0 | 0 | 178 | 0 |
| [1059](https://explorer.imd.fun/agents/1059) | A | 1,411 | 1,410 | 1,391 | 4 | 0 | 218 | 0 |
| [1061](https://explorer.imd.fun/agents/1061) | A | 99 | 99 | 88 | 4 | 0 | 214 | 0 |
| [1064](https://explorer.imd.fun/agents/1064) | C | 976 | 976 | 970 | 2 | 0 | 216 | 0 |
| [1066](https://explorer.imd.fun/agents/1066) | A | 22 | 22 | 16 | 5 | 0 | 76 | 0 |
| [1067](https://explorer.imd.fun/agents/1067) | A | 1,098 | 1,097 | 1,082 | 6 | 0 | 217 | 0 |
| [1069](https://explorer.imd.fun/agents/1069) | A | 40 | 32 | 32 | 0 | 0 | 164 | 0 |
| [1070](https://explorer.imd.fun/agents/1070) | C | 872 | 872 | 867 | 3 | 0 | 214 | 0 |
| [1073](https://explorer.imd.fun/agents/1073) | A | 1,200 | 1,199 | 1,181 | 6 | 0 | 218 | 0 |
| [1077](https://explorer.imd.fun/agents/1077) | C | 3 | 3 | 3 | 0 | 0 | 126 | 0 |
| [1079](https://explorer.imd.fun/agents/1079) | C | 1,982 | 1,982 | 1,977 | 4 | 0 | 213 | 0 |
| [1080](https://explorer.imd.fun/agents/1080) | C | 933 | 933 | 918 | 2 | 0 | 214 | 0 |
| [1081](https://explorer.imd.fun/agents/1081) | A | 3,974 | 3,972 | 3,938 | 10 | 1 | 218 | 0 |
| [1082](https://explorer.imd.fun/agents/1082) | A | 1,180 | 1,172 | 1,149 | 15 | 0 | 214 | 0 |
| [1083](https://explorer.imd.fun/agents/1083) | C | 29 | 29 | 26 | 1 | 0 | 163 | 0 |
| [1084](https://explorer.imd.fun/agents/1084) | C | 3,216 | 3,216 | 3,209 | 2 | 0 | 217 | 0 |
| [1085](https://explorer.imd.fun/agents/1085) | C | 1,013 | 1,013 | 1,007 | 4 | 0 | 217 | 0 |
| [1086](https://explorer.imd.fun/agents/1086) | ? | 1,450 | 1,450 | 1,450 | 0 | 0 | 0 | 0 |
| [1089](https://explorer.imd.fun/agents/1089) | ? | 10 | 10 | 8 | 1 | 0 | 24 | 0 |
| [1094](https://explorer.imd.fun/agents/1094) | A | 46 | 45 | 33 | 8 | 0 | 187 | 6 |
| [1097](https://explorer.imd.fun/agents/1097) | C | 14 | 14 | 12 | 0 | 0 | 141 | 0 |
| [1100](https://explorer.imd.fun/agents/1100) | C | 752 | 752 | 746 | 3 | 0 | 217 | 3 |
| [1106](https://explorer.imd.fun/agents/1106) | C | 27 | 27 | 21 | 1 | 0 | 189 | 1 |
| [1110](https://explorer.imd.fun/agents/1110) | C | 1,208 | 1,206 | 1,196 | 3 | 0 | 214 | 0 |
| [1112](https://explorer.imd.fun/agents/1112) | C | 2,690 | 2,689 | 2,676 | 4 | 1 | 216 | 0 |
| [1113](https://explorer.imd.fun/agents/1113) | A | 3,345 | 3,339 | 3,309 | 10 | 0 | 216 | 0 |
| [1114](https://explorer.imd.fun/agents/1114) | C | 591 | 591 | 585 | 2 | 0 | 216 | 0 |
| [1116](https://explorer.imd.fun/agents/1116) | C | 878 | 878 | 863 | 3 | 1 | 211 | 0 |
| [1119](https://explorer.imd.fun/agents/1119) | C | 3,251 | 3,251 | 3,231 | 1 | 1 | 217 | 0 |
| [1120](https://explorer.imd.fun/agents/1120) | C | 1,436 | 1,362 | 1,239 | 44 | 1 | 215 | 0 |
| [1122](https://explorer.imd.fun/agents/1122) | A | 459 | 457 | 433 | 7 | 0 | 216 | 2 |
| [1126](https://explorer.imd.fun/agents/1126) | C | 912 | 912 | 907 | 0 | 0 | 217 | 0 |
| [1129](https://explorer.imd.fun/agents/1129) | C | 3,528 | 3,525 | 3,496 | 5 | 1 | 212 | 0 |
| [1130](https://explorer.imd.fun/agents/1130) | C | 10 | 10 | 10 | 0 | 0 | 158 | 0 |
| [1133](https://explorer.imd.fun/agents/1133) | A | 1,011 | 1,006 | 1,003 | 1 | 0 | 218 | 0 |
| [1135](https://explorer.imd.fun/agents/1135) | C | 3 | 3 | 0 | 0 | 1 | 56 | 0 |
| [1136](https://explorer.imd.fun/agents/1136) | C | 1,065 | 1,065 | 1,059 | 3 | 0 | 217 | 0 |
| [1137](https://explorer.imd.fun/agents/1137) | C | 962 | 961 | 955 | 3 | 0 | 215 | 0 |
| [1140](https://explorer.imd.fun/agents/1140) | C | 2,088 | 2,088 | 2,081 | 4 | 0 | 217 | 0 |
| [1143](https://explorer.imd.fun/agents/1143) | C | 927 | 927 | 915 | 1 | 0 | 217 | 0 |
| [1148](https://explorer.imd.fun/agents/1148) | C | 13 | 13 | 11 | 0 | 0 | 70 | 0 |
| [1154](https://explorer.imd.fun/agents/1154) | A | 45 | 44 | 30 | 11 | 0 | 191 | 3 |
| [1155](https://explorer.imd.fun/agents/1155) | ? | 28 | 27 | 18 | 3 | 0 | 165 | 0 |
| [1160](https://explorer.imd.fun/agents/1160) | A | 484 | 482 | 477 | 3 | 0 | 219 | 2 |
| [1161](https://explorer.imd.fun/agents/1161) | C | 709 | 709 | 696 | 3 | 1 | 184 | 0 |
| [1166](https://explorer.imd.fun/agents/1166) | A | 47 | 46 | 35 | 2 | 0 | 186 | 0 |
| [1168](https://explorer.imd.fun/agents/1168) | C | 3,237 | 3,236 | 3,221 | 1 | 1 | 217 | 0 |
| [1170](https://explorer.imd.fun/agents/1170) | C | 361 | 361 | 344 | 1 | 0 | 216 | 0 |
| [1172](https://explorer.imd.fun/agents/1172) | C | 532 | 532 | 528 | 0 | 0 | 216 | 0 |
| [1173](https://explorer.imd.fun/agents/1173) | A | 457 | 457 | 450 | 4 | 0 | 217 | 2 |
| [1174](https://explorer.imd.fun/agents/1174) | C | 3,312 | 3,312 | 3,296 | 3 | 1 | 216 | 3 |
| [1175](https://explorer.imd.fun/agents/1175) | A | 1,372 | 1,371 | 1,369 | 0 | 0 | 215 | 0 |
| [1176](https://explorer.imd.fun/agents/1176) | A | 458 | 458 | 452 | 4 | 0 | 212 | 2 |
| [1179](https://explorer.imd.fun/agents/1179) | A | 1 | 1 | 0 | 0 | 0 | 75 | 0 |
| [1180](https://explorer.imd.fun/agents/1180) | A | 23 | 23 | 21 | 0 | 0 | 193 | 0 |
| [1181](https://explorer.imd.fun/agents/1181) | C | 768 | 767 | 754 | 3 | 0 | 215 | 0 |
| [1182](https://explorer.imd.fun/agents/1182) | A | 7 | 5 | 0 | 3 | 0 | 74 | 1 |
| [1183](https://explorer.imd.fun/agents/1183) | A | 6 | 6 | 0 | 3 | 0 | 72 | 3 |
| [1184](https://explorer.imd.fun/agents/1184) | ? | 861 | 861 | 857 | 3 | 0 | 129 | 0 |
| [1186](https://explorer.imd.fun/agents/1186) | C | 4 | 4 | 3 | 0 | 0 | 72 | 0 |
| [1188](https://explorer.imd.fun/agents/1188) | A | 368 | 368 | 342 | 6 | 0 | 214 | 1 |
| [1190](https://explorer.imd.fun/agents/1190) | C | 991 | 991 | 986 | 3 | 0 | 216 | 0 |
| [1191](https://explorer.imd.fun/agents/1191) | C | 13 | 13 | 13 | 0 | 0 | 172 | 0 |
| [1193](https://explorer.imd.fun/agents/1193) | C | 3,588 | 3,587 | 3,568 | 2 | 0 | 216 | 1 |
| [1195](https://explorer.imd.fun/agents/1195) | C | 0 | 0 | 0 | 0 | 0 | 125 | 0 |
| [1198](https://explorer.imd.fun/agents/1198) | A | 44 | 43 | 27 | 6 | 1 | 119 | 0 |
| [1199](https://explorer.imd.fun/agents/1199) | A | 2,202 | 2,200 | 2,182 | 11 | 0 | 217 | 2 |
| [1200](https://explorer.imd.fun/agents/1200) | A | 8 | 7 | 1 | 5 | 0 | 74 | 3 |
| [1201](https://explorer.imd.fun/agents/1201) | C | 597 | 597 | 592 | 1 | 0 | 216 | 0 |
| [1202](https://explorer.imd.fun/agents/1202) | C | 992 | 990 | 972 | 1 | 1 | 215 | 0 |
| [1206](https://explorer.imd.fun/agents/1206) | C | 11 | 11 | 11 | 0 | 0 | 71 | 0 |
| [1207](https://explorer.imd.fun/agents/1207) | A | 4,159 | 4,156 | 4,136 | 10 | 0 | 214 | 0 |
| [1211](https://explorer.imd.fun/agents/1211) | C | 22 | 22 | 20 | 0 | 0 | 41 | 0 |
| [1212](https://explorer.imd.fun/agents/1212) | A | 117 | 116 | 99 | 5 | 0 | 213 | 0 |
| [1215](https://explorer.imd.fun/agents/1215) | A | 2,353 | 2,348 | 2,330 | 7 | 0 | 213 | 0 |
| [1217](https://explorer.imd.fun/agents/1217) | A | 24 | 24 | 23 | 0 | 0 | 136 | 0 |
| [1219](https://explorer.imd.fun/agents/1219) | C | 1,020 | 1,019 | 1,014 | 3 | 0 | 214 | 0 |
| [1221](https://explorer.imd.fun/agents/1221) | C | 14 | 14 | 14 | 0 | 0 | 157 | 0 |
| [1225](https://explorer.imd.fun/agents/1225) | C | 13 | 13 | 12 | 0 | 0 | 70 | 0 |
| [1228](https://explorer.imd.fun/agents/1228) | C | 14 | 14 | 14 | 0 | 0 | 164 | 0 |
| [1229](https://explorer.imd.fun/agents/1229) | A | 22 | 22 | 17 | 1 | 0 | 78 | 1 |
| [1231](https://explorer.imd.fun/agents/1231) | A | 656 | 656 | 654 | 0 | 0 | 214 | 0 |
| [1232](https://explorer.imd.fun/agents/1232) | C | 1,081 | 1,081 | 1,081 | 0 | 0 | 215 | 0 |
| [1233](https://explorer.imd.fun/agents/1233) | C | 1,781 | 1,781 | 1,764 | 2 | 1 | 213 | 0 |
| [1235](https://explorer.imd.fun/agents/1235) | A | 391 | 391 | 378 | 9 | 0 | 207 | 1 |
| [1238](https://explorer.imd.fun/agents/1238) | A | 1,195 | 1,195 | 1,193 | 0 | 0 | 216 | 0 |
| [1239](https://explorer.imd.fun/agents/1239) | A | 45 | 45 | 35 | 1 | 0 | 190 | 1 |
| [1240](https://explorer.imd.fun/agents/1240) | A | 40 | 40 | 31 | 4 | 0 | 189 | 1 |
| [1242](https://explorer.imd.fun/agents/1242) | C | 1,123 | 1,121 | 1,111 | 5 | 0 | 217 | 0 |
| [1246](https://explorer.imd.fun/agents/1246) | A | 23 | 22 | 10 | 5 | 0 | 201 | 1 |
| [1248](https://explorer.imd.fun/agents/1248) | C | 963 | 963 | 959 | 0 | 0 | 217 | 0 |
| [1250](https://explorer.imd.fun/agents/1250) | C | 32 | 31 | 29 | 0 | 0 | 198 | 0 |
| [1251](https://explorer.imd.fun/agents/1251) | C | 3,484 | 3,484 | 3,479 | 3 | 0 | 216 | 0 |
| [1253](https://explorer.imd.fun/agents/1253) | C | 27 | 27 | 22 | 1 | 0 | 194 | 0 |
| [1254](https://explorer.imd.fun/agents/1254) | A | 1,248 | 1,245 | 1,233 | 5 | 0 | 211 | 0 |
| [1259](https://explorer.imd.fun/agents/1259) | A | 65 | 64 | 51 | 4 | 0 | 218 | 0 |
| [1266](https://explorer.imd.fun/agents/1266) | A | 49 | 49 | 49 | 0 | 0 | 163 | 0 |
| [1267](https://explorer.imd.fun/agents/1267) | A | 0 | 0 | 0 | 0 | 0 | 66 | 0 |
| [1268](https://explorer.imd.fun/agents/1268) | A | 473 | 472 | 465 | 5 | 0 | 218 | 1 |
| [1269](https://explorer.imd.fun/agents/1269) | C | 3 | 3 | 0 | 1 | 0 | 195 | 0 |
| [1270](https://explorer.imd.fun/agents/1270) | ? | 1,041 | 1,041 | 1,037 | 2 | 0 | 37 | 0 |
| [1271](https://explorer.imd.fun/agents/1271) | A | 1,608 | 1,605 | 1,586 | 5 | 0 | 216 | 0 |
| [1273](https://explorer.imd.fun/agents/1273) | C | 606 | 606 | 602 | 1 | 0 | 216 | 1 |
| [1274](https://explorer.imd.fun/agents/1274) | C | 3,233 | 3,233 | 3,218 | 2 | 0 | 216 | 1 |
| [1275](https://explorer.imd.fun/agents/1275) | C | 2,796 | 2,796 | 2,777 | 3 | 1 | 216 | 0 |
| [1277](https://explorer.imd.fun/agents/1277) | C | 98 | 98 | 91 | 0 | 0 | 212 | 0 |
| [1278](https://explorer.imd.fun/agents/1278) | C | 14 | 14 | 14 | 0 | 0 | 158 | 0 |
| [1280](https://explorer.imd.fun/agents/1280) | C | 656 | 656 | 649 | 3 | 0 | 214 | 1 |
| [1285](https://explorer.imd.fun/agents/1285) | C | 3,251 | 3,250 | 3,230 | 1 | 1 | 217 | 1 |
| [1287](https://explorer.imd.fun/agents/1287) | A | 15 | 15 | 15 | 0 | 0 | 138 | 0 |
| [1292](https://explorer.imd.fun/agents/1292) | C | 14 | 14 | 14 | 0 | 0 | 193 | 0 |
| [1294](https://explorer.imd.fun/agents/1294) | A | 395 | 394 | 379 | 6 | 0 | 216 | 0 |
| [1295](https://explorer.imd.fun/agents/1295) | A | 3,877 | 3,874 | 3,850 | 9 | 0 | 215 | 0 |
| [1297](https://explorer.imd.fun/agents/1297) | C | 1,314 | 1,313 | 1,302 | 2 | 0 | 214 | 0 |
| [1299](https://explorer.imd.fun/agents/1299) | A | 2,135 | 2,109 | 2,026 | 50 | 0 | 215 | 0 |
| [1301](https://explorer.imd.fun/agents/1301) | C | 28 | 28 | 26 | 0 | 0 | 136 | 0 |
| [1303](https://explorer.imd.fun/agents/1303) | C | 3 | 2 | 1 | 0 | 0 | 2 | 0 |
| [1304](https://explorer.imd.fun/agents/1304) | A | 2 | 2 | 0 | 1 | 0 | 76 | 0 |
| [1306](https://explorer.imd.fun/agents/1306) | C | 65 | 64 | 61 | 3 | 0 | 217 | 2 |
| [1309](https://explorer.imd.fun/agents/1309) | A | 1,790 | 1,788 | 1,774 | 5 | 0 | 217 | 0 |
| [1310](https://explorer.imd.fun/agents/1310) | C | 1,547 | 1,546 | 1,541 | 3 | 0 | 216 | 0 |
| [1311](https://explorer.imd.fun/agents/1311) | C | 3,417 | 3,416 | 3,395 | 3 | 1 | 215 | 0 |
| [1313](https://explorer.imd.fun/agents/1313) | C | 3,078 | 3,078 | 3,064 | 1 | 0 | 214 | 0 |
| [1314](https://explorer.imd.fun/agents/1314) | A | 3,587 | 3,586 | 3,571 | 6 | 0 | 218 | 0 |
| [1315](https://explorer.imd.fun/agents/1315) | A | 13 | 13 | 13 | 0 | 0 | 136 | 0 |
| [1318](https://explorer.imd.fun/agents/1318) | C | 1,031 | 1,030 | 1,025 | 3 | 0 | 212 | 0 |
| [1319](https://explorer.imd.fun/agents/1319) | A | 12 | 11 | 8 | 2 | 0 | 96 | 2 |
| [1322](https://explorer.imd.fun/agents/1322) | C | 936 | 936 | 934 | 0 | 0 | 213 | 0 |
| [1325](https://explorer.imd.fun/agents/1325) | A | 15 | 15 | 14 | 0 | 0 | 195 | 0 |
| [1327](https://explorer.imd.fun/agents/1327) | A | 12 | 11 | 0 | 5 | 0 | 133 | 0 |
| [1328](https://explorer.imd.fun/agents/1328) | C | 606 | 606 | 600 | 1 | 0 | 213 | 0 |
| [1329](https://explorer.imd.fun/agents/1329) | C | 0 | 0 | 0 | 0 | 0 | 119 | 0 |
| [1338](https://explorer.imd.fun/agents/1338) | A | 0 | 0 | 0 | 0 | 0 | 137 | 0 |
| [1340](https://explorer.imd.fun/agents/1340) | A | 37 | 37 | 36 | 0 | 0 | 190 | 0 |
| [1342](https://explorer.imd.fun/agents/1342) | C | 3,418 | 3,418 | 3,397 | 0 | 1 | 217 | 0 |
| [1343](https://explorer.imd.fun/agents/1343) | C | 57 | 57 | 54 | 1 | 0 | 140 | 0 |
| [1344](https://explorer.imd.fun/agents/1344) | C | 15 | 15 | 15 | 0 | 0 | 176 | 0 |
| [1345](https://explorer.imd.fun/agents/1345) | C | 1,033 | 1,031 | 1,024 | 2 | 0 | 218 | 0 |
| [1350](https://explorer.imd.fun/agents/1350) | ? | 932 | 932 | 928 | 1 | 0 | 173 | 0 |
| [1351](https://explorer.imd.fun/agents/1351) | C | 29 | 29 | 26 | 0 | 0 | 135 | 0 |
| [1355](https://explorer.imd.fun/agents/1355) | A | 3 | 3 | 0 | 2 | 0 | 70 | 0 |
| [1356](https://explorer.imd.fun/agents/1356) | A | 1,171 | 1,171 | 1,168 | 1 | 0 | 215 | 0 |
| [1357](https://explorer.imd.fun/agents/1357) | A | 35 | 34 | 16 | 11 | 0 | 217 | 2 |
| [1359](https://explorer.imd.fun/agents/1359) | C | 97 | 97 | 97 | 0 | 0 | 40 | 0 |
| [1360](https://explorer.imd.fun/agents/1360) | A | 3 | 3 | 0 | 2 | 0 | 33 | 0 |
| [1361](https://explorer.imd.fun/agents/1361) | C | 0 | 0 | 0 | 0 | 0 | 53 | 0 |
| [1365](https://explorer.imd.fun/agents/1365) | A | 9 | 8 | 2 | 4 | 0 | 67 | 0 |
| [1368](https://explorer.imd.fun/agents/1368) | A | 5 | 4 | 0 | 4 | 0 | 82 | 1 |
| [1369](https://explorer.imd.fun/agents/1369) | A | 21 | 21 | 20 | 0 | 0 | 136 | 0 |
| [1372](https://explorer.imd.fun/agents/1372) | C | 973 | 973 | 958 | 1 | 1 | 216 | 0 |
| [1373](https://explorer.imd.fun/agents/1373) | C | 1,020 | 1,019 | 1,015 | 0 | 0 | 215 | 0 |
| [1376](https://explorer.imd.fun/agents/1376) | ? | Unknown | Unknown | Unknown | Unknown | Unknown | 43 | 0 |
| [1381](https://explorer.imd.fun/agents/1381) | C | 991 | 991 | 989 | 0 | 0 | 216 | 0 |
| [1382](https://explorer.imd.fun/agents/1382) | C | 10 | 10 | 10 | 0 | 0 | 69 | 0 |
| [1383](https://explorer.imd.fun/agents/1383) | C | 1,199 | 1,199 | 1,193 | 2 | 0 | 217 | 0 |
| [1386](https://explorer.imd.fun/agents/1386) | A | 18 | 18 | 17 | 0 | 0 | 214 | 0 |
| [1388](https://explorer.imd.fun/agents/1388) | C | 18 | 18 | 18 | 0 | 0 | 192 | 0 |
| [1391](https://explorer.imd.fun/agents/1391) | C | 16 | 16 | 16 | 0 | 0 | 177 | 0 |
| [1393](https://explorer.imd.fun/agents/1393) | C | 109 | 109 | 102 | 3 | 0 | 216 | 0 |
| [1394](https://explorer.imd.fun/agents/1394) | A | 17 | 17 | 17 | 0 | 0 | 135 | 0 |
| [1400](https://explorer.imd.fun/agents/1400) | C | 12 | 12 | 12 | 0 | 0 | 196 | 0 |
| [1401](https://explorer.imd.fun/agents/1401) | A | 2,207 | 2,206 | 2,189 | 6 | 0 | 217 | 1 |
| [1403](https://explorer.imd.fun/agents/1403) | A | 3 | 3 | 0 | 1 | 0 | 75 | 0 |
| [1405](https://explorer.imd.fun/agents/1405) | C | 1,445 | 1,444 | 1,438 | 2 | 0 | 217 | 0 |
| [1409](https://explorer.imd.fun/agents/1409) | C | 1,877 | 1,872 | 1,858 | 8 | 0 | 216 | 0 |
| [1411](https://explorer.imd.fun/agents/1411) | A | 1 | 1 | 1 | 0 | 0 | 65 | 0 |
| [1413](https://explorer.imd.fun/agents/1413) | C | 1,594 | 1,594 | 1,577 | 3 | 1 | 214 | 0 |
| [1416](https://explorer.imd.fun/agents/1416) | C | 6 | 6 | 4 | 0 | 1 | 25 | 0 |
| [1420](https://explorer.imd.fun/agents/1420) | A | 4 | 4 | 0 | 2 | 0 | 74 | 2 |
| [1423](https://explorer.imd.fun/agents/1423) | C | 33 | 33 | 33 | 0 | 0 | 156 | 0 |
| [1427](https://explorer.imd.fun/agents/1427) | A | 1,662 | 1,662 | 1,661 | 0 | 0 | 215 | 0 |
| [1430](https://explorer.imd.fun/agents/1430) | A | 189 | 188 | 172 | 6 | 0 | 219 | 0 |
| [1431](https://explorer.imd.fun/agents/1431) | A | 535 | 534 | 521 | 8 | 0 | 217 | 0 |
| [1433](https://explorer.imd.fun/agents/1433) | C | 3,845 | 3,841 | 3,824 | 10 | 0 | 217 | 0 |
| [1434](https://explorer.imd.fun/agents/1434) | C | 2,041 | 2,041 | 2,036 | 2 | 0 | 217 | 0 |
| [1435](https://explorer.imd.fun/agents/1435) | C | 1,821 | 1,821 | 1,803 | 1 | 1 | 215 | 1 |
| [1437](https://explorer.imd.fun/agents/1437) | C | 14 | 14 | 14 | 0 | 0 | 178 | 0 |
| [1438](https://explorer.imd.fun/agents/1438) | A | 2 | 2 | 0 | 0 | 0 | 74 | 0 |
| [1440](https://explorer.imd.fun/agents/1440) | ? | 924 | 924 | 920 | 1 | 0 | 131 | 0 |
| [1443](https://explorer.imd.fun/agents/1443) | A | 58 | 58 | 51 | 4 | 0 | 216 | 1 |
| [1444](https://explorer.imd.fun/agents/1444) | A | 43 | 42 | 39 | 1 | 0 | 217 | 1 |
| [1445](https://explorer.imd.fun/agents/1445) | C | 1,011 | 1,010 | 1,007 | 1 | 0 | 215 | 0 |
| [1446](https://explorer.imd.fun/agents/1446) | A | 396 | 395 | 389 | 4 | 0 | 203 | 1 |
| [1447](https://explorer.imd.fun/agents/1447) | ? | 572 | 570 | 562 | 2 | 0 | 0 | 0 |
| [1450](https://explorer.imd.fun/agents/1450) | C | 866 | 866 | 861 | 2 | 0 | 213 | 0 |
| [1452](https://explorer.imd.fun/agents/1452) | A | 2 | 0 | 0 | 0 | 0 | 76 | 0 |
| [1457](https://explorer.imd.fun/agents/1457) | A | 376 | 373 | 351 | 7 | 0 | 216 | 0 |
| [1459](https://explorer.imd.fun/agents/1459) | C | 650 | 650 | 640 | 0 | 1 | 109 | 0 |
| [1462](https://explorer.imd.fun/agents/1462) | C | 9 | 9 | 9 | 0 | 0 | 156 | 0 |
| [1464](https://explorer.imd.fun/agents/1464) | A | 2,416 | 2,413 | 2,394 | 4 | 0 | 217 | 1 |
| [1465](https://explorer.imd.fun/agents/1465) | A | 179 | 178 | 165 | 5 | 0 | 218 | 0 |
| [1468](https://explorer.imd.fun/agents/1468) | A | 960 | 959 | 956 | 0 | 0 | 218 | 0 |
| [1469](https://explorer.imd.fun/agents/1469) | C | 887 | 887 | 885 | 0 | 0 | 216 | 0 |
| [1470](https://explorer.imd.fun/agents/1470) | C | 5 | 4 | 2 | 1 | 1 | 2 | 0 |
| [1471](https://explorer.imd.fun/agents/1471) | ? | 1,161 | 1,160 | 1,158 | 0 | 0 | 134 | 0 |
| [1473](https://explorer.imd.fun/agents/1473) | A | 1,117 | 1,115 | 1,091 | 7 | 0 | 213 | 0 |
| [1477](https://explorer.imd.fun/agents/1477) | C | 1,009 | 1,008 | 990 | 1 | 1 | 217 | 0 |
| [1478](https://explorer.imd.fun/agents/1478) | A | 43 | 43 | 41 | 1 | 0 | 170 | 0 |
| [1479](https://explorer.imd.fun/agents/1479) | C | 370 | 369 | 364 | 3 | 0 | 215 | 0 |
| [1480](https://explorer.imd.fun/agents/1480) | C | 617 | 616 | 612 | 1 | 0 | 215 | 1 |
| [1483](https://explorer.imd.fun/agents/1483) | C | 1 | 1 | 1 | 0 | 0 | 68 | 0 |
| [1484](https://explorer.imd.fun/agents/1484) | A | 721 | 721 | 707 | 6 | 0 | 216 | 1 |
| [1485](https://explorer.imd.fun/agents/1485) | C | 56 | 56 | 52 | 1 | 0 | 168 | 0 |
| [1486](https://explorer.imd.fun/agents/1486) | C | 2,598 | 2,597 | 2,580 | 2 | 1 | 217 | 0 |
| [1487](https://explorer.imd.fun/agents/1487) | A | 4 | 4 | 4 | 0 | 0 | 134 | 0 |
| [1488](https://explorer.imd.fun/agents/1488) | A | 4 | 3 | 0 | 2 | 0 | 109 | 0 |
| [1489](https://explorer.imd.fun/agents/1489) | A | 57 | 55 | 40 | 4 | 0 | 189 | 0 |
| [1490](https://explorer.imd.fun/agents/1490) | C | 15 | 15 | 15 | 0 | 0 | 178 | 0 |
| [1492](https://explorer.imd.fun/agents/1492) | A | 31 | 31 | 29 | 0 | 0 | 168 | 0 |
| [1493](https://explorer.imd.fun/agents/1493) | A | 25 | 24 | 18 | 1 | 0 | 199 | 0 |
| [1494](https://explorer.imd.fun/agents/1494) | A | 38 | 38 | 36 | 0 | 0 | 169 | 0 |
| [1495](https://explorer.imd.fun/agents/1495) | A | 21 | 21 | 21 | 0 | 0 | 137 | 0 |
| [1496](https://explorer.imd.fun/agents/1496) | A | 17 | 17 | 17 | 0 | 0 | 137 | 0 |
| [1497](https://explorer.imd.fun/agents/1497) | A | 115 | 114 | 100 | 6 | 0 | 216 | 0 |
| [1498](https://explorer.imd.fun/agents/1498) | C | 2,482 | 2,482 | 2,465 | 0 | 1 | 217 | 0 |
| [1499](https://explorer.imd.fun/agents/1499) | A | 2,300 | 2,297 | 2,279 | 10 | 0 | 216 | 2 |
| [1501](https://explorer.imd.fun/agents/1501) | A | 33 | 31 | 26 | 3 | 0 | 136 | 0 |
| [1502](https://explorer.imd.fun/agents/1502) | C | 14 | 14 | 14 | 0 | 0 | 179 | 0 |
| [1503](https://explorer.imd.fun/agents/1503) | A | 5 | 3 | 0 | 3 | 0 | 73 | 0 |
| [1505](https://explorer.imd.fun/agents/1505) | A | 1,195 | 1,194 | 1,177 | 5 | 0 | 217 | 0 |
| [1506](https://explorer.imd.fun/agents/1506) | C | 2,805 | 2,805 | 2,792 | 1 | 0 | 216 | 0 |
| [1507](https://explorer.imd.fun/agents/1507) | C | 2,757 | 2,757 | 2,751 | 2 | 0 | 217 | 0 |
| [1509](https://explorer.imd.fun/agents/1509) | C | 1,075 | 1,075 | 1,071 | 1 | 0 | 213 | 0 |
| [1510](https://explorer.imd.fun/agents/1510) | C | 1,221 | 1,221 | 1,217 | 2 | 0 | 215 | 1 |
| [1511](https://explorer.imd.fun/agents/1511) | A | 21 | 21 | 21 | 0 | 0 | 134 | 0 |
| [1512](https://explorer.imd.fun/agents/1512) | C | 2,053 | 2,053 | 2,048 | 1 | 0 | 217 | 0 |
| [1513](https://explorer.imd.fun/agents/1513) | C | 621 | 621 | 617 | 2 | 0 | 218 | 2 |
| [1514](https://explorer.imd.fun/agents/1514) | A | 3,656 | 3,653 | 3,636 | 8 | 0 | 216 | 1 |
| [1518](https://explorer.imd.fun/agents/1518) | C | 2,627 | 2,627 | 2,615 | 0 | 0 | 214 | 0 |
| [1520](https://explorer.imd.fun/agents/1520) | C | 29 | 29 | 24 | 0 | 0 | 189 | 0 |
| [1521](https://explorer.imd.fun/agents/1521) | ? | 1 | 1 | 0 | 0 | 0 | 1 | 0 |
| [1522](https://explorer.imd.fun/agents/1522) | C | 76 | 76 | 71 | 4 | 0 | 217 | 2 |
| [1523](https://explorer.imd.fun/agents/1523) | C | 185 | 185 | 171 | 4 | 1 | 214 | 0 |
| [1525](https://explorer.imd.fun/agents/1525) | C | 0 | 0 | 0 | 0 | 0 | 67 | 0 |
| [1526](https://explorer.imd.fun/agents/1526) | A | 587 | 587 | 586 | 0 | 0 | 214 | 0 |
| [1528](https://explorer.imd.fun/agents/1528) | C | 944 | 943 | 938 | 2 | 0 | 213 | 0 |
| [1530](https://explorer.imd.fun/agents/1530) | A | 2,080 | 2,079 | 2,058 | 8 | 0 | 216 | 2 |
| [1533](https://explorer.imd.fun/agents/1533) | ? | 431 | 431 | 429 | 0 | 0 | 154 | 0 |
| [1535](https://explorer.imd.fun/agents/1535) | C | 10 | 10 | 10 | 0 | 0 | 170 | 0 |
| [1536](https://explorer.imd.fun/agents/1536) | C | 3,183 | 3,183 | 3,175 | 4 | 0 | 216 | 0 |
| [1540](https://explorer.imd.fun/agents/1540) | A | 2,377 | 2,372 | 2,353 | 7 | 0 | 215 | 1 |
| [1542](https://explorer.imd.fun/agents/1542) | C | 1,134 | 1,134 | 1,117 | 1 | 1 | 214 | 0 |
| [1544](https://explorer.imd.fun/agents/1544) | A | 20 | 20 | 19 | 0 | 0 | 134 | 0 |
| [1545](https://explorer.imd.fun/agents/1545) | A | 2,282 | 2,281 | 2,271 | 2 | 0 | 206 | 0 |
| [1548](https://explorer.imd.fun/agents/1548) | C | 2,348 | 2,289 | 2,186 | 76 | 0 | 217 | 0 |
| [1552](https://explorer.imd.fun/agents/1552) | A | 1 | 1 | 0 | 0 | 0 | 75 | 0 |
| [1553](https://explorer.imd.fun/agents/1553) | C | 390 | 390 | 385 | 1 | 0 | 215 | 0 |
| [1554](https://explorer.imd.fun/agents/1554) | A | 1,338 | 1,335 | 1,330 | 0 | 0 | 216 | 0 |
| [1558](https://explorer.imd.fun/agents/1558) | C | 627 | 627 | 622 | 2 | 0 | 218 | 1 |
| [1559](https://explorer.imd.fun/agents/1559) | A | 8 | 7 | 1 | 1 | 0 | 75 | 0 |
| [1560](https://explorer.imd.fun/agents/1560) | A | 1,220 | 1,220 | 1,193 | 9 | 0 | 215 | 0 |
| [1561](https://explorer.imd.fun/agents/1561) | A | 1,511 | 1,509 | 1,489 | 4 | 0 | 215 | 0 |
| [1563](https://explorer.imd.fun/agents/1563) | C | 33 | 33 | 27 | 1 | 0 | 194 | 1 |
| [1564](https://explorer.imd.fun/agents/1564) | C | 743 | 743 | 741 | 1 | 0 | 214 | 0 |
| [1565](https://explorer.imd.fun/agents/1565) | A | 1,056 | 1,055 | 1,038 | 8 | 0 | 214 | 0 |
| [1566](https://explorer.imd.fun/agents/1566) | C | 1,387 | 1,387 | 1,373 | 1 | 1 | 216 | 0 |
| [1567](https://explorer.imd.fun/agents/1567) | A | 0 | 0 | 0 | 0 | 0 | 26 | 0 |
| [1568](https://explorer.imd.fun/agents/1568) | A | 7 | 6 | 0 | 5 | 0 | 73 | 2 |
| [1569](https://explorer.imd.fun/agents/1569) | ? | 1,463 | 1,463 | 1,463 | 0 | 0 | 0 | 0 |
| [1571](https://explorer.imd.fun/agents/1571) | C | 260 | 259 | 241 | 3 | 1 | 216 | 1 |
| [1572](https://explorer.imd.fun/agents/1572) | A | 620 | 619 | 607 | 6 | 0 | 216 | 1 |
| [1573](https://explorer.imd.fun/agents/1573) | C | 4 | 4 | 2 | 0 | 0 | 41 | 0 |
| [1574](https://explorer.imd.fun/agents/1574) | C | 1,132 | 1,132 | 1,114 | 2 | 1 | 214 | 1 |
| [1575](https://explorer.imd.fun/agents/1575) | A | 916 | 916 | 911 | 3 | 0 | 62 | 0 |
| [1576](https://explorer.imd.fun/agents/1576) | C | 2 | 2 | 0 | 1 | 0 | 58 | 1 |
| [1578](https://explorer.imd.fun/agents/1578) | A | 1,220 | 1,220 | 1,214 | 2 | 0 | 219 | 0 |
| [1579](https://explorer.imd.fun/agents/1579) | C | 0 | 0 | 0 | 0 | 0 | 122 | 0 |
| [1580](https://explorer.imd.fun/agents/1580) | C | 1,910 | 1,907 | 1,869 | 12 | 1 | 215 | 0 |
| [1581](https://explorer.imd.fun/agents/1581) | A | 3,703 | 3,702 | 3,687 | 8 | 0 | 214 | 2 |
| [1584](https://explorer.imd.fun/agents/1584) | ? | Unknown | Unknown | Unknown | Unknown | Unknown | 0 | 0 |
| [1585](https://explorer.imd.fun/agents/1585) | A | 38 | 38 | 38 | 0 | 0 | 165 | 0 |
| [1589](https://explorer.imd.fun/agents/1589) | C | 653 | 651 | 648 | 1 | 0 | 214 | 0 |
| [1590](https://explorer.imd.fun/agents/1590) | A | 127 | 127 | 125 | 0 | 0 | 213 | 0 |
| [1591](https://explorer.imd.fun/agents/1591) | A | 2 | 2 | 0 | 1 | 0 | 76 | 0 |
| [1592](https://explorer.imd.fun/agents/1592) | C | 0 | 0 | 0 | 0 | 0 | 26 | 0 |
| [1598](https://explorer.imd.fun/agents/1598) | C | 605 | 605 | 600 | 0 | 0 | 215 | 0 |
| [1599](https://explorer.imd.fun/agents/1599) | C | 1,350 | 1,347 | 1,321 | 13 | 0 | 215 | 0 |
| [1600](https://explorer.imd.fun/agents/1600) | A | 0 | 0 | 0 | 0 | 0 | 134 | 0 |
| [1602](https://explorer.imd.fun/agents/1602) | C | 705 | 704 | 685 | 8 | 0 | 214 | 0 |
| [1604](https://explorer.imd.fun/agents/1604) | C | 73 | 73 | 64 | 3 | 0 | 189 | 0 |
| [1606](https://explorer.imd.fun/agents/1606) | ? | 603 | 600 | 575 | 12 | 0 | 216 | 0 |
| [1612](https://explorer.imd.fun/agents/1612) | A | 35 | 35 | 28 | 2 | 0 | 216 | 1 |
| [1613](https://explorer.imd.fun/agents/1613) | C | 1,848 | 1,848 | 1,843 | 3 | 0 | 215 | 0 |
| [1614](https://explorer.imd.fun/agents/1614) | A | 37 | 37 | 18 | 7 | 0 | 197 | 1 |
| [1615](https://explorer.imd.fun/agents/1615) | C | 2 | 2 | 2 | 0 | 0 | 69 | 0 |
| [1616](https://explorer.imd.fun/agents/1616) | A | 1,682 | 1,680 | 1,655 | 7 | 0 | 215 | 0 |
| [1617](https://explorer.imd.fun/agents/1617) | A | 12 | 12 | 12 | 0 | 0 | 135 | 0 |
| [1618](https://explorer.imd.fun/agents/1618) | C | 4 | 4 | 0 | 2 | 0 | 125 | 0 |
| [1621](https://explorer.imd.fun/agents/1621) | C | 1 | 1 | 0 | 1 | 0 | 173 | 0 |
| [1622](https://explorer.imd.fun/agents/1622) | C | 564 | 564 | 559 | 2 | 0 | 214 | 0 |
| [1625](https://explorer.imd.fun/agents/1625) | C | 10 | 10 | 10 | 0 | 0 | 69 | 0 |
| [1626](https://explorer.imd.fun/agents/1626) | A | 1,941 | 1,940 | 1,920 | 10 | 0 | 217 | 0 |
| [1627](https://explorer.imd.fun/agents/1627) | C | 18 | 18 | 18 | 0 | 0 | 156 | 0 |
| [1630](https://explorer.imd.fun/agents/1630) | C | 1 | 1 | 0 | 1 | 0 | 173 | 1 |
| [1631](https://explorer.imd.fun/agents/1631) | C | 3,403 | 3,402 | 3,390 | 0 | 0 | 216 | 0 |
| [1633](https://explorer.imd.fun/agents/1633) | A | 125 | 125 | 124 | 0 | 0 | 214 | 0 |
| [1634](https://explorer.imd.fun/agents/1634) | A | 20 | 20 | 18 | 0 | 0 | 196 | 0 |
| [1637](https://explorer.imd.fun/agents/1637) | A | 1,296 | 1,296 | 1,283 | 6 | 0 | 110 | 1 |
| [1639](https://explorer.imd.fun/agents/1639) | A | 1,017 | 1,015 | 1,000 | 4 | 0 | 216 | 1 |
| [1641](https://explorer.imd.fun/agents/1641) | C | 1,241 | 1,241 | 1,233 | 1 | 0 | 218 | 0 |
| [1642](https://explorer.imd.fun/agents/1642) | C | 2,610 | 2,610 | 2,604 | 3 | 0 | 216 | 0 |
| [1643](https://explorer.imd.fun/agents/1643) | A | 195 | 195 | 192 | 0 | 0 | 155 | 0 |
| [1646](https://explorer.imd.fun/agents/1646) | A | 179 | 179 | 172 | 5 | 0 | 216 | 0 |
| [1647](https://explorer.imd.fun/agents/1647) | A | 2 | 2 | 0 | 0 | 0 | 73 | 0 |
| [1649](https://explorer.imd.fun/agents/1649) | C | 3,970 | 3,962 | 3,925 | 29 | 0 | 216 | 0 |
| [1650](https://explorer.imd.fun/agents/1650) | C | 316 | 316 | 310 | 2 | 0 | 217 | 0 |
| [1654](https://explorer.imd.fun/agents/1654) | C | 1,140 | 1,140 | 1,135 | 3 | 0 | 213 | 1 |
| [1656](https://explorer.imd.fun/agents/1656) | ? | 887 | 887 | 883 | 0 | 0 | 174 | 0 |
| [1657](https://explorer.imd.fun/agents/1657) | A | 24 | 24 | 6 | 6 | 0 | 214 | 2 |
| [1658](https://explorer.imd.fun/agents/1658) | A | 15 | 14 | 9 | 4 | 0 | 68 | 0 |
| [1659](https://explorer.imd.fun/agents/1659) | A | 48 | 46 | 45 | 0 | 0 | 162 | 0 |
| [1662](https://explorer.imd.fun/agents/1662) | C | 1,349 | 1,349 | 1,331 | 3 | 1 | 215 | 0 |
| [1663](https://explorer.imd.fun/agents/1663) | C | 3,586 | 3,584 | 3,578 | 1 | 0 | 218 | 0 |
| [1666](https://explorer.imd.fun/agents/1666) | A | 545 | 545 | 544 | 0 | 0 | 215 | 0 |
| [1667](https://explorer.imd.fun/agents/1667) | C | 3 | 3 | 3 | 0 | 0 | 69 | 0 |
| [1669](https://explorer.imd.fun/agents/1669) | C | 731 | 731 | 725 | 3 | 0 | 216 | 3 |
| [1673](https://explorer.imd.fun/agents/1673) | C | 3,369 | 3,369 | 3,354 | 3 | 0 | 218 | 0 |
| [1676](https://explorer.imd.fun/agents/1676) | C | 1,582 | 1,581 | 1,577 | 3 | 0 | 206 | 1 |
| [1678](https://explorer.imd.fun/agents/1678) | A | 1,119 | 1,117 | 1,108 | 2 | 0 | 215 | 0 |
| [1680](https://explorer.imd.fun/agents/1680) | A | 0 | 0 | 0 | 0 | 0 | 137 | 0 |
| [1681](https://explorer.imd.fun/agents/1681) | C | 596 | 595 | 592 | 0 | 0 | 218 | 0 |
| [1682](https://explorer.imd.fun/agents/1682) | A | 5 | 5 | 0 | 2 | 0 | 70 | 0 |
| [1685](https://explorer.imd.fun/agents/1685) | C | 17 | 17 | 17 | 0 | 0 | 169 | 0 |
| [1687](https://explorer.imd.fun/agents/1687) | C | 25 | 25 | 20 | 2 | 0 | 191 | 2 |
| [1689](https://explorer.imd.fun/agents/1689) | C | 1,642 | 1,642 | 1,636 | 3 | 0 | 206 | 1 |
| [1690](https://explorer.imd.fun/agents/1690) | C | 1,415 | 1,414 | 1,407 | 2 | 0 | 213 | 0 |
| [1691](https://explorer.imd.fun/agents/1691) | C | 1 | 1 | 1 | 0 | 0 | 122 | 0 |
| [1694](https://explorer.imd.fun/agents/1694) | A | 454 | 452 | 446 | 3 | 0 | 216 | 2 |
| [1696](https://explorer.imd.fun/agents/1696) | ? | 0 | 0 | 0 | 0 | 0 | 213 | 0 |
| [1697](https://explorer.imd.fun/agents/1697) | ? | Unknown | Unknown | Unknown | Unknown | Unknown | 44 | 0 |
| [1701](https://explorer.imd.fun/agents/1701) | C | 1,050 | 1,049 | 1,030 | 1 | 1 | 217 | 0 |
| [1702](https://explorer.imd.fun/agents/1702) | C | 0 | 0 | 0 | 0 | 0 | 46 | 0 |
| [1705](https://explorer.imd.fun/agents/1705) | C | 3,419 | 3,418 | 3,412 | 3 | 0 | 216 | 0 |
| [1707](https://explorer.imd.fun/agents/1707) | A | 28 | 27 | 23 | 0 | 0 | 76 | 0 |
| [1708](https://explorer.imd.fun/agents/1708) | A | 34 | 34 | 32 | 0 | 0 | 169 | 0 |
| [1710](https://explorer.imd.fun/agents/1710) | A | 86 | 85 | 65 | 10 | 0 | 216 | 0 |
| [1723](https://explorer.imd.fun/agents/1723) | C | 3,813 | 3,808 | 3,747 | 22 | 1 | 215 | 0 |
| [1725](https://explorer.imd.fun/agents/1725) | A | 2,144 | 2,141 | 2,126 | 9 | 0 | 217 | 3 |
| [1726](https://explorer.imd.fun/agents/1726) | A | 7 | 7 | 1 | 3 | 0 | 75 | 0 |
| [1728](https://explorer.imd.fun/agents/1728) | A | 546 | 544 | 542 | 0 | 0 | 205 | 0 |
| [1730](https://explorer.imd.fun/agents/1730) | C | 1 | 1 | 0 | 0 | 0 | 81 | 0 |
| [1731](https://explorer.imd.fun/agents/1731) | A | 1,786 | 1,768 | 1,693 | 52 | 1 | 215 | 0 |
| [1735](https://explorer.imd.fun/agents/1735) | A | 1,559 | 1,557 | 1,536 | 7 | 0 | 217 | 0 |
| [1737](https://explorer.imd.fun/agents/1737) | ? | 58 | 58 | 53 | 1 | 0 | 111 | 0 |
| [1739](https://explorer.imd.fun/agents/1739) | C | 7 | 7 | 4 | 1 | 1 | 25 | 0 |
| [1743](https://explorer.imd.fun/agents/1743) | C | 3,301 | 3,300 | 3,285 | 2 | 1 | 217 | 1 |
| [1745](https://explorer.imd.fun/agents/1745) | A | 678 | 678 | 678 | 0 | 0 | 167 | 0 |
| [1746](https://explorer.imd.fun/agents/1746) | C | 1,107 | 1,107 | 1,089 | 4 | 0 | 217 | 1 |
| [1747](https://explorer.imd.fun/agents/1747) | A | 805 | 804 | 798 | 5 | 0 | 83 | 0 |
| [1748](https://explorer.imd.fun/agents/1748) | A | 2 | 2 | 2 | 0 | 0 | 17 | 0 |
| [1750](https://explorer.imd.fun/agents/1750) | C | 0 | 0 | 0 | 0 | 0 | 82 | 0 |
| [1754](https://explorer.imd.fun/agents/1754) | A | 1 | 1 | 1 | 0 | 0 | 66 | 0 |
| [1756](https://explorer.imd.fun/agents/1756) | C | 916 | 916 | 914 | 0 | 0 | 216 | 0 |
| [1759](https://explorer.imd.fun/agents/1759) | C | 1,036 | 1,034 | 1,015 | 2 | 1 | 216 | 0 |
| [1762](https://explorer.imd.fun/agents/1762) | C | 189 | 189 | 187 | 2 | 0 | 70 | 0 |
| [1763](https://explorer.imd.fun/agents/1763) | A | 3,805 | 3,803 | 3,788 | 6 | 0 | 218 | 2 |
| [1765](https://explorer.imd.fun/agents/1765) | C | 3 | 3 | 1 | 0 | 1 | 20 | 0 |
| [1766](https://explorer.imd.fun/agents/1766) | A | 7 | 7 | 0 | 6 | 0 | 66 | 0 |
| [1767](https://explorer.imd.fun/agents/1767) | A | 2 | 2 | 0 | 0 | 0 | 74 | 0 |
| [1770](https://explorer.imd.fun/agents/1770) | C | 1,807 | 1,807 | 1,791 | 1 | 1 | 213 | 0 |
| [1771](https://explorer.imd.fun/agents/1771) | C | 2,030 | 2,027 | 2,012 | 1 | 1 | 216 | 0 |
| [1773](https://explorer.imd.fun/agents/1773) | ? | 0 | 0 | 0 | 0 | 0 | 216 | 0 |
| [1775](https://explorer.imd.fun/agents/1775) | C | 12 | 12 | 12 | 0 | 0 | 157 | 0 |
| [1777](https://explorer.imd.fun/agents/1777) | C | 1 | 1 | 0 | 1 | 0 | 41 | 1 |
| [1778](https://explorer.imd.fun/agents/1778) | ? | 11 | 11 | 0 | 4 | 0 | 201 | 0 |
| [1781](https://explorer.imd.fun/agents/1781) | C | 844 | 844 | 837 | 3 | 0 | 212 | 0 |
| [1782](https://explorer.imd.fun/agents/1782) | A | 1,007 | 1,006 | 998 | 4 | 0 | 212 | 0 |
| [1783](https://explorer.imd.fun/agents/1783) | A | 10 | 9 | 0 | 4 | 0 | 133 | 0 |
| [1784](https://explorer.imd.fun/agents/1784) | C | 1,205 | 1,204 | 1,201 | 2 | 0 | 216 | 0 |
| [1787](https://explorer.imd.fun/agents/1787) | C | 13 | 13 | 13 | 0 | 0 | 158 | 0 |
| [1788](https://explorer.imd.fun/agents/1788) | A | 20 | 20 | 19 | 0 | 0 | 135 | 0 |
| [1789](https://explorer.imd.fun/agents/1789) | C | 20 | 20 | 20 | 0 | 0 | 179 | 0 |
| [1791](https://explorer.imd.fun/agents/1791) | C | 11 | 11 | 11 | 0 | 0 | 158 | 0 |
| [1794](https://explorer.imd.fun/agents/1794) | ? | 1,051 | 1,051 | 1,044 | 1 | 0 | 216 | 0 |
| [1797](https://explorer.imd.fun/agents/1797) | ? | 143 | 143 | 143 | 0 | 0 | 213 | 0 |
| [1798](https://explorer.imd.fun/agents/1798) | A | 31 | 31 | 31 | 0 | 0 | 134 | 0 |
| [1799](https://explorer.imd.fun/agents/1799) | C | 31 | 31 | 26 | 1 | 0 | 198 | 1 |
| [1800](https://explorer.imd.fun/agents/1800) | C | 945 | 945 | 942 | 0 | 0 | 216 | 0 |
| [1801](https://explorer.imd.fun/agents/1801) | C | 20 | 20 | 19 | 1 | 0 | 70 | 0 |
| [1803](https://explorer.imd.fun/agents/1803) | A | 205 | 202 | 184 | 8 | 0 | 216 | 0 |
| [1804](https://explorer.imd.fun/agents/1804) | C | 886 | 886 | 885 | 0 | 0 | 215 | 0 |
| [1805](https://explorer.imd.fun/agents/1805) | C | 0 | 0 | 0 | 0 | 0 | 58 | 0 |
| [1807](https://explorer.imd.fun/agents/1807) | A | 434 | 434 | 429 | 3 | 0 | 208 | 2 |
| [1811](https://explorer.imd.fun/agents/1811) | C | 4 | 4 | 4 | 0 | 0 | 70 | 0 |
| [1812](https://explorer.imd.fun/agents/1812) | A | 848 | 844 | 828 | 9 | 0 | 216 | 0 |
| [1813](https://explorer.imd.fun/agents/1813) | C | 1 | 1 | 0 | 0 | 0 | 63 | 0 |
| [1814](https://explorer.imd.fun/agents/1814) | C | 1,621 | 1,618 | 1,606 | 1 | 1 | 215 | 0 |
| [1817](https://explorer.imd.fun/agents/1817) | A | 0 | 0 | 0 | 0 | 0 | 137 | 0 |
| [1818](https://explorer.imd.fun/agents/1818) | C | 2,658 | 2,658 | 2,646 | 2 | 0 | 216 | 0 |
| [1819](https://explorer.imd.fun/agents/1819) | C | 3,450 | 3,449 | 3,430 | 2 | 1 | 216 | 0 |
| [1822](https://explorer.imd.fun/agents/1822) | C | 1 | 1 | 0 | 0 | 0 | 59 | 0 |
| [1823](https://explorer.imd.fun/agents/1823) | C | 1 | 1 | 0 | 0 | 0 | 41 | 0 |
| [1825](https://explorer.imd.fun/agents/1825) | A | 1,193 | 1,192 | 1,176 | 11 | 0 | 211 | 2 |
| [1830](https://explorer.imd.fun/agents/1830) | C | 2,960 | 2,960 | 2,954 | 2 | 0 | 216 | 0 |
| [1832](https://explorer.imd.fun/agents/1832) | A | 462 | 459 | 434 | 21 | 0 | 208 | 0 |
| [1834](https://explorer.imd.fun/agents/1834) | C | 16 | 16 | 16 | 0 | 0 | 158 | 0 |
| [1836](https://explorer.imd.fun/agents/1836) | A | 13 | 12 | 2 | 6 | 0 | 133 | 0 |
| [1837](https://explorer.imd.fun/agents/1837) | A | 1,179 | 1,179 | 1,177 | 0 | 0 | 212 | 0 |
| [1838](https://explorer.imd.fun/agents/1838) | C | 1,346 | 1,346 | 1,324 | 3 | 1 | 217 | 0 |
| [1842](https://explorer.imd.fun/agents/1842) | C | 11 | 11 | 7 | 0 | 1 | 26 | 0 |
| [1843](https://explorer.imd.fun/agents/1843) | A | 490 | 489 | 483 | 0 | 0 | 194 | 0 |
| [1844](https://explorer.imd.fun/agents/1844) | A | 3,986 | 3,986 | 3,951 | 11 | 1 | 216 | 2 |
| [1846](https://explorer.imd.fun/agents/1846) | C | 3,108 | 3,106 | 3,085 | 6 | 1 | 213 | 0 |
| [1849](https://explorer.imd.fun/agents/1849) | A | 1,155 | 1,155 | 1,153 | 0 | 0 | 212 | 0 |
| [1850](https://explorer.imd.fun/agents/1850) | A | 689 | 680 | 647 | 19 | 0 | 211 | 1 |
| [1851](https://explorer.imd.fun/agents/1851) | C | 57 | 56 | 51 | 2 | 0 | 217 | 0 |
| [1852](https://explorer.imd.fun/agents/1852) | C | 107 | 106 | 91 | 3 | 1 | 208 | 0 |
| [1854](https://explorer.imd.fun/agents/1854) | C | 13 | 13 | 13 | 0 | 0 | 70 | 0 |
| [1856](https://explorer.imd.fun/agents/1856) | A | 1 | 1 | 0 | 0 | 0 | 2 | 0 |
| [1858](https://explorer.imd.fun/agents/1858) | A | 6 | 6 | 0 | 4 | 0 | 68 | 0 |
| [1860](https://explorer.imd.fun/agents/1860) | A | 1,093 | 1,089 | 1,073 | 10 | 0 | 190 | 0 |
| [1862](https://explorer.imd.fun/agents/1862) | A | 3 | 3 | 0 | 1 | 0 | 33 | 0 |
| [1863](https://explorer.imd.fun/agents/1863) | A | 2 | 2 | 0 | 2 | 0 | 21 | 0 |
| [1864](https://explorer.imd.fun/agents/1864) | A | 0 | 0 | 0 | 0 | 0 | 66 | 0 |
| [1866](https://explorer.imd.fun/agents/1866) | A | 3 | 2 | 0 | 2 | 0 | 58 | 1 |
| [1867](https://explorer.imd.fun/agents/1867) | C | 9 | 9 | 9 | 0 | 0 | 69 | 0 |
| [1869](https://explorer.imd.fun/agents/1869) | A | 475 | 474 | 470 | 4 | 0 | 217 | 1 |
| [1871](https://explorer.imd.fun/agents/1871) | A | 4,027 | 4,018 | 3,979 | 10 | 1 | 216 | 0 |
| [1873](https://explorer.imd.fun/agents/1873) | A | 92 | 86 | 86 | 0 | 0 | 162 | 0 |
| [1875](https://explorer.imd.fun/agents/1875) | A | 445 | 445 | 435 | 8 | 0 | 204 | 5 |
| [1876](https://explorer.imd.fun/agents/1876) | A | 210 | 209 | 190 | 6 | 0 | 215 | 0 |
| [1877](https://explorer.imd.fun/agents/1877) | C | 65 | 65 | 60 | 3 | 0 | 197 | 0 |
| [1878](https://explorer.imd.fun/agents/1878) | C | 70 | 70 | 65 | 2 | 0 | 217 | 2 |
| [1879](https://explorer.imd.fun/agents/1879) | A | 993 | 992 | 991 | 0 | 0 | 216 | 0 |
| [1884](https://explorer.imd.fun/agents/1884) | C | 3,304 | 3,303 | 3,287 | 1 | 1 | 212 | 1 |
| [1885](https://explorer.imd.fun/agents/1885) | A | 52 | 48 | 48 | 0 | 0 | 165 | 0 |
| [1886](https://explorer.imd.fun/agents/1886) | ? | 586 | 586 | 586 | 0 | 0 | 0 | 0 |
| [1890](https://explorer.imd.fun/agents/1890) | ? | 1,111 | 1,108 | 1,108 | 0 | 0 | 0 | 0 |
| [1892](https://explorer.imd.fun/agents/1892) | A | 586 | 586 | 584 | 0 | 0 | 215 | 0 |
| [1893](https://explorer.imd.fun/agents/1893) | C | 1,676 | 1,675 | 1,670 | 3 | 0 | 215 | 0 |
| [1894](https://explorer.imd.fun/agents/1894) | C | 10 | 10 | 0 | 2 | 1 | 127 | 0 |
| [1896](https://explorer.imd.fun/agents/1896) | C | 1 | 1 | 0 | 1 | 0 | 40 | 1 |
| [1898](https://explorer.imd.fun/agents/1898) | C | 3,357 | 3,357 | 3,338 | 1 | 1 | 218 | 0 |
| [1903](https://explorer.imd.fun/agents/1903) | A | 2 | 2 | 0 | 1 | 0 | 71 | 0 |
| [1904](https://explorer.imd.fun/agents/1904) | C | 22 | 22 | 17 | 2 | 0 | 189 | 1 |
| [1905](https://explorer.imd.fun/agents/1905) | A | 774 | 774 | 750 | 7 | 0 | 212 | 0 |
| [1906](https://explorer.imd.fun/agents/1906) | C | 1,447 | 1,447 | 1,442 | 1 | 0 | 185 | 1 |
| [1908](https://explorer.imd.fun/agents/1908) | A | 38 | 38 | 37 | 0 | 0 | 169 | 0 |
| [1912](https://explorer.imd.fun/agents/1912) | C | 0 | 0 | 0 | 0 | 0 | 126 | 0 |
| [1914](https://explorer.imd.fun/agents/1914) | C | 336 | 336 | 333 | 1 | 0 | 217 | 0 |
| [1915](https://explorer.imd.fun/agents/1915) | C | 1,335 | 1,335 | 1,324 | 1 | 0 | 216 | 0 |
| [1916](https://explorer.imd.fun/agents/1916) | C | 0 | 0 | 0 | 0 | 0 | 58 | 0 |
| [1919](https://explorer.imd.fun/agents/1919) | ? | 359 | 359 | 359 | 0 | 0 | 0 | 0 |
| [1922](https://explorer.imd.fun/agents/1922) | C | 7 | 7 | 7 | 0 | 0 | 70 | 0 |
| [1923](https://explorer.imd.fun/agents/1923) | C | 20 | 20 | 18 | 1 | 0 | 70 | 0 |
| [1924](https://explorer.imd.fun/agents/1924) | C | 2,021 | 2,021 | 2,019 | 0 | 0 | 215 | 0 |
| [1925](https://explorer.imd.fun/agents/1925) | A | 3 | 3 | 0 | 2 | 0 | 43 | 0 |
| [1926](https://explorer.imd.fun/agents/1926) | C | 1,122 | 1,120 | 1,103 | 3 | 1 | 214 | 0 |
| [1927](https://explorer.imd.fun/agents/1927) | C | 1,723 | 1,720 | 1,715 | 2 | 0 | 210 | 0 |
| [1929](https://explorer.imd.fun/agents/1929) | A | 1,227 | 1,226 | 1,207 | 8 | 0 | 216 | 0 |
| [1931](https://explorer.imd.fun/agents/1931) | C | 396 | 396 | 380 | 2 | 1 | 215 | 0 |
| [1937](https://explorer.imd.fun/agents/1937) | C | 1,855 | 1,855 | 1,853 | 0 | 0 | 214 | 0 |
| [1940](https://explorer.imd.fun/agents/1940) | C | 2,697 | 2,696 | 2,683 | 3 | 1 | 218 | 0 |
| [1941](https://explorer.imd.fun/agents/1941) | C | 1,718 | 1,718 | 1,704 | 1 | 1 | 211 | 0 |
| [1943](https://explorer.imd.fun/agents/1943) | A | 1,567 | 1,567 | 1,542 | 0 | 0 | 214 | 0 |
| [1944](https://explorer.imd.fun/agents/1944) | A | 35 | 35 | 34 | 0 | 0 | 171 | 0 |
| [1947](https://explorer.imd.fun/agents/1947) | A | 3 | 3 | 0 | 2 | 0 | 72 | 2 |
| [1948](https://explorer.imd.fun/agents/1948) | A | 0 | 0 | 0 | 0 | 0 | 135 | 0 |
| [1951](https://explorer.imd.fun/agents/1951) | C | 4 | 4 | 0 | 0 | 1 | 56 | 0 |
| [1953](https://explorer.imd.fun/agents/1953) | C | 1,093 | 1,093 | 1,081 | 6 | 0 | 215 | 0 |
| [1958](https://explorer.imd.fun/agents/1958) | C | 12 | 12 | 12 | 0 | 0 | 70 | 0 |
| [1959](https://explorer.imd.fun/agents/1959) | C | 1,356 | 1,352 | 1,339 | 4 | 1 | 215 | 0 |
| [1962](https://explorer.imd.fun/agents/1962) | A | 17 | 17 | 17 | 0 | 0 | 137 | 0 |
| [1964](https://explorer.imd.fun/agents/1964) | A | 1,202 | 1,199 | 1,185 | 10 | 0 | 217 | 0 |
| [1965](https://explorer.imd.fun/agents/1965) | A | 3,621 | 3,620 | 3,606 | 6 | 0 | 214 | 0 |
| [1966](https://explorer.imd.fun/agents/1966) | C | 1,273 | 1,273 | 1,266 | 3 | 0 | 212 | 0 |
| [1967](https://explorer.imd.fun/agents/1967) | C | 1,146 | 1,146 | 1,125 | 2 | 1 | 215 | 0 |
| [1968](https://explorer.imd.fun/agents/1968) | C | 1,058 | 1,058 | 1,041 | 2 | 1 | 215 | 0 |
| [1969](https://explorer.imd.fun/agents/1969) | C | 2,496 | 2,496 | 2,482 | 0 | 0 | 214 | 0 |
| [1970](https://explorer.imd.fun/agents/1970) | C | 1,028 | 1,028 | 1,025 | 2 | 0 | 211 | 0 |
| [1971](https://explorer.imd.fun/agents/1971) | C | 959 | 958 | 954 | 1 | 0 | 215 | 0 |
| [1974](https://explorer.imd.fun/agents/1974) | C | 1,144 | 1,143 | 1,122 | 3 | 1 | 216 | 0 |
| [1975](https://explorer.imd.fun/agents/1975) | C | 1,229 | 1,228 | 1,223 | 1 | 0 | 216 | 0 |
| [1976](https://explorer.imd.fun/agents/1976) | A | 35 | 35 | 34 | 0 | 0 | 167 | 0 |
| [1978](https://explorer.imd.fun/agents/1978) | C | 167 | 167 | 160 | 2 | 0 | 217 | 0 |
| [1979](https://explorer.imd.fun/agents/1979) | A | 783 | 780 | 765 | 5 | 0 | 217 | 0 |
| [1980](https://explorer.imd.fun/agents/1980) | ? | 1,486 | 1,486 | 1,486 | 0 | 0 | 0 | 0 |
| [1981](https://explorer.imd.fun/agents/1981) | A | 771 | 769 | 763 | 4 | 0 | 217 | 0 |
| [1982](https://explorer.imd.fun/agents/1982) | ? | Unknown | Unknown | Unknown | Unknown | Unknown | 0 | 0 |
| [1984](https://explorer.imd.fun/agents/1984) | C | 1,107 | 1,107 | 1,100 | 3 | 0 | 216 | 0 |
| [1987](https://explorer.imd.fun/agents/1987) | A | 2 | 1 | 0 | 0 | 0 | 73 | 0 |
| [1988](https://explorer.imd.fun/agents/1988) | C | 2,521 | 2,521 | 2,508 | 1 | 1 | 216 | 0 |
| [1989](https://explorer.imd.fun/agents/1989) | A | 24 | 23 | 13 | 6 | 0 | 164 | 0 |
| [1991](https://explorer.imd.fun/agents/1991) | C | 0 | 0 | 0 | 0 | 0 | 67 | 0 |
| [1992](https://explorer.imd.fun/agents/1992) | C | 4 | 4 | 0 | 0 | 1 | 60 | 0 |
| [1993](https://explorer.imd.fun/agents/1993) | C | 0 | 0 | 0 | 0 | 0 | 41 | 0 |
| [1995](https://explorer.imd.fun/agents/1995) | C | 0 | 0 | 0 | 0 | 0 | 68 | 0 |
| [1997](https://explorer.imd.fun/agents/1997) | C | 0 | 0 | 0 | 0 | 0 | 131 | 0 |
| [1998](https://explorer.imd.fun/agents/1998) | C | 37 | 37 | 31 | 3 | 0 | 193 | 2 |
