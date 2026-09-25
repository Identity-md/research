# Worker health report

- **asOf (UTC, fetch time):** `2026-09-25T05:50:24Z`
- **Source:** `GET https://api.imd.fun/workers` — raw response saved at `data/workers-snapshot.json` (HTTP 200, server `date: Fri, 25 Sep 2026 05:50:24 GMT`, 384031 bytes)
- **Caveat:** GET /workers is a live point-in-time snapshot of currently registered daemons, not a historical archive; seats that are disconnected may be absent entirely rather than listed as stale.
- Structured twin: `WORKER_HEALTH.json` (every number below is copied from it).

## Totals

| Metric | Value |
|---|---|
| Unique seats (deduped by tokenId) | **342** |
| Online seats | **342** |
| Stale seats (heartbeat > 2h old or missing) | **0** |
| Distinct daemon versions | **9** |
| Mode (majority) daemon version | `0.1.0+5bfa8261` (313 seats) |
| Seats not on the mode version | **29** |

**Online rule used:** online = working is truthy (the API returns an integer; treated as working when > 0) OR lastHeartbeatAt is within the 15 minutes before asOf (asOf - 15m <= lastHeartbeatAt, future timestamps also count as fresh).  
Breakdown: 1 seat(s) have `working > 0`; 342 seat(s) have a heartbeat inside the 15-minute window.  
**Stale rule used:** stale = lastHeartbeatAt missing/unparseable OR lastHeartbeatAt < asOf - 2h.

## daemonVersion histogram (unique seats)

| daemonVersion | Seats | Share |
|---|---:|---:|
| `0.1.0+5bfa8261` | 313 | 91.5% |
| `0.1.0+79f4f4d5` | 6 | 1.8% |
| `0.1.0+ff3932db` | 5 | 1.5% |
| `0.1.0+8f011f3d` | 4 | 1.2% |
| `0.1.0+cff23c39` | 4 | 1.2% |
| `0.1.0+61d04d62` | 3 | 0.9% |
| `0.1.0+852666b2` | 3 | 0.9% |
| `0.1.0+50bb666f` | 2 | 0.6% |
| `0.1.0+aa8ff6ee` | 2 | 0.6% |
| **Total** | **342** | 100% |

## Stale seats

None. Oldest heartbeat in the snapshot is `2026-09-25T05:50:05Z`, newest `2026-09-25T05:50:24Z` — all within seconds of asOf.

## Seats not on the mode version `0.1.0+5bfa8261` (29)

| tokenId | daemonVersion |
|---:|---|
| 1032 | `0.1.0+50bb666f` |
| 1175 | `0.1.0+50bb666f` |
| 1120 | `0.1.0+61d04d62` |
| 1602 | `0.1.0+61d04d62` |
| 1886 | `0.1.0+61d04d62` |
| 165 | `0.1.0+79f4f4d5` |
| 263 | `0.1.0+79f4f4d5` |
| 605 | `0.1.0+79f4f4d5` |
| 708 | `0.1.0+79f4f4d5` |
| 1469 | `0.1.0+79f4f4d5` |
| 1756 | `0.1.0+79f4f4d5` |
| 334 | `0.1.0+852666b2` |
| 1116 | `0.1.0+852666b2` |
| 1310 | `0.1.0+852666b2` |
| 166 | `0.1.0+8f011f3d` |
| 1431 | `0.1.0+8f011f3d` |
| 1572 | `0.1.0+8f011f3d` |
| 1731 | `0.1.0+8f011f3d` |
| 8 | `0.1.0+aa8ff6ee` |
| 1427 | `0.1.0+aa8ff6ee` |
| 7 | `0.1.0+cff23c39` |
| 420 | `0.1.0+cff23c39` |
| 1613 | `0.1.0+cff23c39` |
| 1735 | `0.1.0+cff23c39` |
| 1080 | `0.1.0+ff3932db` |
| 1219 | `0.1.0+ff3932db` |
| 1248 | `0.1.0+ff3932db` |
| 1561 | `0.1.0+ff3932db` |
| 1676 | `0.1.0+ff3932db` |

## Facts, inferences, uncertainty

**Facts (read directly from the snapshot):**

- The response had `count: 342` and 342 worker records; 0 lacked a tokenId and 0 repeated an already-seen tokenId, giving 342 unique seats.
- Seat(s) with `working > 0`: `1943`.
- Heartbeats range from `2026-09-25T05:50:05Z` to `2026-09-25T05:50:24Z`.

**Inferences (not stated by the API):**

- `working` is returned as an integer (0/1 in this snapshot), not a boolean; it is read as "currently running a job" and treated as true when > 0.
- Every record reports `connectedHere: true` and a heartbeat seconds old, which suggests the endpoint lists only currently connected daemons. If so, the stale list is structurally near-empty: a seat that went offline is dropped rather than shown with an old heartbeat, and offline seats cannot be counted from this endpoint.
- The earliest `connectedAt` in the snapshot is `2026-09-25T04:46:29Z`, so the connection set may have been reset (e.g. server restart) around then; the snapshot says nothing about earlier periods.
- The "mode build" is the single most common `daemonVersion` string; the build suffix (e.g. `+5bfa8261`) looks like a git short hash, but whether it is newer or older than the other builds cannot be determined from this data.

**Uncertainty / unanswered questions:**

- This is one point-in-time read; numbers will differ on the next fetch. No history or trend is available.
- The total number of seats that exist (including offline ones) is not answerable from `/workers`.
- Server-side semantics of `lastHeartbeatAt`, `working`, and `connectedHere` are undocumented here; the rules above are this report's definitions.

Regenerate from the saved snapshot: `python3 scripts/worker_health.py --as-of 2026-09-25T05:50:24Z`.
