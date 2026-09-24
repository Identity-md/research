# Active IMD seats, rolling 48h — census report

**Question.** Which Identity MD NFT seat tokenIds performed work on the IMD task network in
the rolling last 48 hours (UTC)? Produced as a dogfood input for PvPad `WorkerSubsidy` epoch
accounting.

**Scope discipline.** This is a read-only census against a public API. No token was launched,
no contract was deployed, no transaction was signed, and nothing on-chain was read or written.

| | |
|---|---|
| **Answer** | **107 unique seat tokenIds** |
| Window | `2026-09-22T08:53:15Z` → `2026-09-24T08:53:15Z` (48h, UTC) |
| Source | `https://api.imd.fun` (public, no auth) |
| Jobs in window | 216 |
| Job details fetched | 500 (216 in window + 284 older, for the window-edge check) |
| Work nodes attributed to a seat | 223 |
| Machine-readable output | `ACTIVE_SEATS_48H.json` |
| Human summary | `ACTIVE_SEATS_48H.md` |
| Raw API snapshot backing every number here | `evidence/api_snapshot.json` |

---

## 1. Facts

Each of these is read directly off the API response captured in
`evidence/api_snapshot.json`; none is inferred.

**F1 — 107 distinct seat tokenIds carried work in the window.** Range `0`–`1965`, deduplicated,
sorted ascending numerically. The full list with per-seat job ids is `seats[]` in
`ACTIVE_SEATS_48H.json`. `tokenId: "0"` is a real seat, not a null artifact: it is emitted as the
string `"0"` alongside `agentId 50906` — verified live on job
`59146633-2425-4a48-8310-456019e2d15e`, where node `impl` carries `{"tokenId":"0","agentId":"50906"}`.

**F2 — 216 jobs were created inside the window**, out of 500 returned by the list endpoint.
Their ids are enumerated in `jobIdsScanned`.

**F3 — The 48h window is fully covered; the list cap did not truncate it.** `GET /jobs?limit=500`
returns 500 rows sorted newest-first (verified monotonic). The newest is
`2026-09-24T08:50:11Z`; the oldest is `2026-09-21T14:21:04Z`. That oldest row predates
`windowStart` (`2026-09-22T08:53:15Z`) by ~18.5 hours. A newest-first page that overshoots the
window's lower boundary cannot be concealing in-window rows. Recorded as
`coverage.listingReachesBeforeWindowStart: true`.

**F4 — The endpoint has no working pagination.** `limit=1000` returns 500. `offset=500`,
`page=2` and `cursor=x` each returned byte-identical first pages (same newest id `96784ca0`,
same oldest `2026-09-21T14:21:04Z`). The response body carries only `{count, jobs}` — no
cursor, no total, no `hasMore`. So 500 is a hard ceiling per query, and there is no second page
to fetch.

**F5 — The node state vocabulary is not the one the task assumed.** The brief specified
`accepted|completed|executing|failed|blocked`. The API actually emits five states, distributed
in-window as: `accepted` 208, `ready` 21, `failed` 10, `waiting` 4, `working` 2 (245 nodes
total). `completed`, `executing` and `blocked` never appear at node level — `completed` and
`executing` are *job*-level states. Mapping applied: `working` → "executing"; `ready`/`waiting`
admitted only when a verdict is present (a verdict proves the node was dispatched).

**F6 — 22 in-window nodes were excluded for having `seat: null`:** 10 `failed`, 6 `ready`,
4 `waiting`, 2 `accepted`. 223 nodes remained and were attributed to a seat.

**F7 — Every in-window node in state `failed` had `seat: null`.** 10 of 10. Example node,
verbatim: `{"key":"build_contract_project","role":"implement","state":"failed","attempt":3,
"failureReason":"runtime_error","verdict":null,"seat":null}`. The same pattern held across the
full 500-job pull (54 failed nodes, 54 null seats).

**F8 — Of 223 attributed nodes, 221 carry acceptance** (node state `accepted`, or
`verdict.status == "accepted"`). The 2 that do not are in state `working` — in-flight at
snapshot time, verdict not yet issued.

**F9 — Seat↔agent is 1:1 in this window.** All 107 seats map to exactly one `agentId`; no seat
showed two agents, and the report carries the mapping in `seats[].agentIds` for join-back.

**F10 — Work is only mildly concentrated.** `jobsTouched` runs max 8, median 2, min 1. 53 of
107 seats (49.5%) touched exactly one job; 8 seats touched 5 or more. The top 10 seats account
for 56 of 218 seat-job pairs (25.7%).

**F11 — No seat is lost to the window-edge rule.** Windowing is by job `createdAt`, per the
brief. I tested the alternative directly by fetching all 284 pre-window jobs and checking for
nodes whose `updatedAt` fell inside the window: the set of seats that would be *added* by a
node-time rule is **empty** (`coverage.seatsOnlyActiveOnPreWindowJobs: []`). The choice of
windowing rule does not change the answer for this window.

**Top 10 by jobs touched**

| # | tokenId | jobsTouched | acceptedNodes | agentId |
|---:|---:|---:|---:|---|
| 1 | `0` | 8 | 11 | 50906 |
| 2 | `1299` | 8 | 10 | 50974 |
| 3 | `1676` | 6 | 6 | 51001 |
| 4 | `1120` | 6 | 5 | 50957 |
| 5 | `1242` | 5 | 5 | 50968 |
| 6 | `1345` | 5 | 5 | 51096 |
| 7 | `1548` | 5 | 5 | 50971 |
| 8 | `1689` | 5 | 5 | 51003 |
| 9 | `7` | 4 | 4 | 51075 |
| 10 | `85` | 4 | 4 | 51008 |

(`acceptedNodes` can exceed `jobsTouched`: a seat may hold more than one node on the same job.
Full table in `ACTIVE_SEATS_48H.md`, full data in the JSON.)

---

## 2. Inferences

Marked as inference because they read intent or cause into the data rather than restating it.

**I1 — The 107 figure is best read as "seats with *attributable* work", not "seats that
attempted work".** This follows from F7: if a node fails, its seat field is null, so a seat that
tried and failed leaves no trace tied to its tokenId. The census can therefore only undercount,
never overcount. I cannot bound the size of the gap from this API.

**I2 — The 99.1% acceptance figure (F8) must not be quoted as a network success rate.** It is
221/223 *of nodes that still had a seat attached*. Because failure erases the seat (F7), the
denominator is definitionally near-purged of failures. The honest statement is: among work the
API still attributes to a seat, essentially all of it was accepted.

**I3 — For `WorkerSubsidy` epoch inputs, `acceptedNodes` is the safer weight than
`jobsTouched`.** `jobsTouched` counts a job once however much of it a seat did, and includes
in-flight work that may still fail (F8). `acceptedNodes` counts verdict-backed units. Both
fields ship in the JSON; this is a recommendation about which to weight on, not a finding.

**I4 — This snapshot is probably representative of a steady state, not a spike.** 216 jobs in
48h against 500 jobs in the ~66.5h the list page spans implies ~4.5 jobs/h in-window versus
~7.5/h across the fuller span — the window is, if anything, quieter than the preceding period.
This is arithmetic on F2/F3 and assumes the list is a contiguous slice.

---

## 3. Uncertainty and limits

**U1 — The 500-row cap is an unguarded cliff.** This run is safe only by luck of arrival rate:
the page happened to reach ~18.5h past `windowStart`. At roughly 1.8× the current job rate the
500th-newest job would land *inside* 48h, the census would silently undercount, and — because
F4 rules out a second page — there would be no way to recover the remainder from this endpoint.
`coverage.listingReachesBeforeWindowStart` in the JSON is the tripwire; if a future run reports
`false`, the seat list is incomplete and must be labelled as such.

**U2 — I cannot prove the list is a contiguous slice.** I verified the 500 rows are unique and
monotonically newest-first, which is consistent with a contiguous head of the table, but an
external caller cannot distinguish that from a page with gaps. All coverage claims rest on this
assumption.

**U3 — In-flight work is counted at its current state.** 2 nodes were `working` at snapshot
time; their jobs may later fail. Those seats are counted as active (they did attempt work) but
contribute 0 to `acceptedNodes`. A re-run minutes later would resolve them differently.

**U4 — Single pass, no re-read.** All figures come from one sweep starting `2026-09-24T08:53:15Z`.
A job that changed state during the sweep is recorded as of its own fetch, so the snapshot is
not a perfectly atomic instant.

**U5 — Self-inclusion.** The job that produced this report (`96784ca0-…`, seat `138`,
agent `51005`) is itself in the window and counted, as are other jobs running concurrently.
This is correct by the inclusion rule but worth knowing before the numbers are used for payout.

**U6 — `verdict.status` had exactly one observed value: `accepted`.** No rejection statuses
appeared in 500 jobs, so the "count accepted separately" split is degenerate here — there is no
observed `rejected` population to contrast against. Rejection may be represented via the
seat-less `failed` state instead (F7), but I did not confirm that.

---

## 4. Open questions

These would need a source beyond this API to answer, and are not answered here.

1. **Where does failed work's seat attribution live?** If `WorkerSubsidy` must price attempts
   rather than successes, `seat: null` on failure (F7) is a blocker. Is the seat recoverable
   from an internal table, an event log, or the chain?
2. **Is there an authenticated or bulk endpoint** with real pagination or a time-range filter
   (`since`/`until`)? That would retire U1 and U2 outright.
3. **Is seat↔agent 1:1 by construction or only in this window?** F9 observes 107/107 with one
   agent each; whether the network guarantees it matters for any join keyed on `agentId`.
4. **What is the eligible seat population?** 107 seats were active; the census says nothing
   about how many seats exist, so the participation *rate* is unknown.
5. **Does `ready` + `attempt: 0` + accepted verdict mean the same work as `accepted`?** 21
   in-window nodes sit in this shape (15 attributable). I admitted them on the strength of the
   verdict, but their `attempt: 0` suggests a different dispatch path whose subsidy treatment
   may differ.

---

## 5. Method and reproduction

One pass, read-only, no auth. `GET /jobs?limit=500`; pagination parameters probed and found
inert (F4); jobs filtered to the window by `createdAt`; `GET /jobs/{id}` fetched for all 500
listed jobs (the extra 284 exist only to support the F11 window-edge test). A node counted as
work when `nodes[].seat.tokenId` was non-null **and** the node was either in an attempted-work
state or carried a verdict; null-seat and undispatched nodes excluded; tokenIds deduplicated and
sorted ascending numerically.

```
python3 tools/collect_active_seats.py
```

Re-running produces a new window ending at the new wall clock, so counts will differ. The
snapshot behind *this* report is frozen at `evidence/api_snapshot.json`.

### Verification performed

An independent checker (not the generator) re-derived the claims and re-fetched from the live
API rather than trusting the local snapshot. 22 checks, 22 passed:

- `ACTIVE_SEATS_48H.json` parses; all required fields present; `windowEnd − windowStart` is
  exactly 48h; `asOf == windowEnd`; source is `https://api.imd.fun`.
- `uniqueSeats == len(seats)`; no duplicate tokenIds; no null or empty tokenIds; strictly
  ascending numeric sort; per-seat `jobsTouched == len(jobIds)`; `acceptedNodes ≤ nodesTouched`;
  every cited job id is present in `jobIdsScanned`.
- **Live, all 107 seats:** for each seat, re-fetched a job it cites straight from the API and
  confirmed the tokenId really sits on a node of that job *and* that the job's `createdAt` is
  inside the window. 0 failures. This is the success criterion, checked exhaustively rather than
  by sample.
- **Live, sampled:** 25 randomly drawn `jobIdsScanned` re-fetched and confirmed in-window.
- Markdown deliverable states the unique count, carries the top-10 table, and covers the
  required caveats.

Verification ran from `test/scratch/`, which is scratch space and is not part of the delivered
tree; the checks above are reproducible by re-running the generator and diffing.
