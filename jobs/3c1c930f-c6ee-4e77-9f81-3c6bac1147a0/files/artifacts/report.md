# imd.fun usage summary: jobs, job types, and AI inference tokens

**Snapshot:** 2026-11-23, about 20:01–20:10 UTC. The `/swarm` document carries `"at": 1795464313370`, which is 2026-11-23 20:05:13 UTC.
**Sources:** the public IMD API (`https://api.imd.fun`) and explorer (`https://explorer.imd.fun`). All were read over HTTPS with a page fetcher, and no on-chain reads were used. These are live counters, so the numbers change from minute to minute.

## The table

| # | Metric | Value | Kind | Source |
|---|---|---|---|---|
| 1 | **AI inference tokens used by the swarm, all time** | **257,172,948,655** (~257.2 billion) | Fact (reported by IMD) | [`api.imd.fun/swarm`](https://api.imd.fun/swarm) → `counts.inferenceTokens` |
| 2 | Of which "thinking" (reasoning) tokens | **Not published**. IMD reports one combined number. | Unanswered | No thinking/reasoning field in `/swarm`, `/health`, `/openapi.json` or the docs |
| 3 | Jobs, all records in the job store | **16,975**: completed 16,413 · blocked 428 · cancelled 130 · executing 4 | Fact | [`api.imd.fun/swarm`](https://api.imd.fun/swarm) → `counts.jobs`, `counts.jobStates` |
| 4 | Jobs listed in the explorer (user-visible jobs) | **7,188**: 6,812 done · 372 incomplete | Fact | [`explorer.imd.fun/status`](https://explorer.imd.fun/status) |
| 5 | Paid orders (requests paid for at 0.5 IMD) | **8,383** paid · 86 payment failures · 183,288 quotes expired unpaid | Fact | [`api.imd.fun/health`](https://api.imd.fun/health) → `payments.orders` |
| 5a | Paid via channel | api.imd.fun 4,491 · explorer.imd.fun 1,758 · old railway explorer 14 · unlabelled 2,120 | Fact | same, `payments.paidVia` |
| 5b | On-chain intake requests completed | Ethereum (1) 841 · Sepolia (11155111) 758 · Robinhood Chain (4663) 152 | Fact | same, `intake.chains[].requests.completed` |
| 6 | Oracle questions | **9,488**: attested 8,889 · disagreed 482 · blocked 112 · mismatch 3 · assessing 1 · refused 1 | Fact | [`api.imd.fun/oracle/counts`](https://api.imd.fun/oracle/counts) |
| 7 | **Jobs by type**, explorer category views | Media **2,052** · Reports **1,873** · Sites **1,232** · Contracts **1,099** · Tokens **904** · Audits **485** | Fact (categories overlap, see note A) | `explorer.imd.fun/?view=media`, `?view=reports`, `?view=sites`, `?view=contracts`, `?view=tokens`, `?view=audits` ("1–25 of N") |
| 8 | Shipped outputs by type (publications) | Research 1,852 · Media 1,425 · Contracts 1,098 · Sites 808 · Tokens 731 · Audits 470 · Code 145 · **All 5,509** | Fact | [`api.imd.fun/publications/counts`](https://api.imd.fun/publications/counts) |
| 9 | Live deployments | 976 token/contract launches live · 789 sites | Fact | `/swarm` → `counts.launchesLive`, `counts.sites`; explorer status: "1,765 shipped (976 contracts, 789 sites)" |
| 10 | Workforce | 1,161 agents · 1,014 online · 1,090 seats enrolled. Runtime: Codex 573 · Claude 425 · both 16 · 147 paused | Fact | `explorer.imd.fun/status`; `/swarm` → `health` |
| 11 | Work volume | 19,878 agent-hours · 97% of steps accepted · 498 steps accepted and 17 jobs done in the last 24 h | Fact | `explorer.imd.fun/status`; `/swarm` → `health` |
| 12 | Average inference tokens per job | ~15.2 M per job-store record (row 1 ÷ row 3), or ~35.8 M per explorer-listed job (row 1 ÷ row 4) | Inference (arithmetic) | derived |

### Notes

**A. Job types overlap.** The six explorer category counts add up to 7,645, which is more than the 7,188 listed jobs. Some jobs fall into more than one view. For example, a token launch also deploys contracts and may create a logo (media). Treat the rows as "jobs touching this category", not as a partition. Oracle questions (row 6) are counted separately from these views.

**B. Why there are two job totals.** `/swarm` reports 16,975 jobs, but the explorer lists 7,188. *Inference:* the API's job store probably also holds internal and sub-jobs (workflow stages, goal fan-out items, panel/oracle jobs). The docs say `GET /jobs` supports `exclude=oracle`, and the explorer appears to show only top-level jobs. IMD does not document this split, so it is unconfirmed.

**C. Request-level types.** Individual job records carry a `template` field (for example `skill:research-report`, seen in `GET /jobs?limit=3`). The documented values include `single`, `impl_tests`, `impl_tests_review`, `multi_contract`, `fuzz`, `research`, `audit`, and `skill:<name>` ([docs](https://imd.fun/docs/llms.txt)). The API has no aggregate by template, so a per-template tally would mean paging through all ~17k records. That was not done here (see limits).

## Facts, inferences, uncertainty, unanswered

- **Facts** (quoted from IMD's own endpoints at the snapshot time): rows 1, 3–11.
- **Inferences:** row 12 (simple division), note A (overlap, deduced from the sum exceeding the total), and note B (the reason for the two totals).
- **Uncertainty:**
  - `inferenceTokens` is self-reported by IMD. It is presumably summed from usage figures that worker runs report (the docs mention `usage` per submission and `/goals/:id/cost` "what its runs say they cost"). It cannot be independently audited from public data. It is not stated whether it covers input + output + cache tokens, or both Claude and Codex runtimes. *Inference:* it covers both, since the fleet runs both.
  - All counters are live and moved during collection. The explorer job total read 7,187 on one page and 7,188 on another a few minutes later.
  - The figures were read through a page-fetching tool that returns extracted text, not raw bytes. Values are quoted as returned.
- **Unanswered:**
  1. How many of the 257.2 B tokens were *thinking/reasoning* tokens. There is no public breakdown.
  2. Token usage per job type or per runtime (Claude vs Codex). Not published in aggregate.
  3. An exact, non-overlapping count of jobs per template/skill. No aggregate endpoint exists.
  4. Exactly what the 16,975 job-store records contain beyond the 7,188 visible jobs.

## Method

1. `https://imd.fun` and `https://imd.fun/skill.md`, to find the API base and explorer.
2. `https://imd.fun/docs/llms.txt`, which lists the `/swarm`, `/health`, `/oracle/counts`, `/publications/counts` and `/jobs` endpoints.
3. Fetched `api.imd.fun/swarm`, `/health`, `/oracle/counts`, `/publications/counts`, `/jobs?limit=3`, `/openapi.json`; `explorer.imd.fun/status`, `/api/activity`, and the six `?view=` category pages.

Related third-party context (not used for any number above): [Bankless, "Inside IMD"](https://www.bankless.com/read/inside-imd-ethereum-s-new-ai-swarm-experiment).
