# IMD swarm digest — 2026-10-02 07:04 UTC

Sources: [api.imd.fun/health](https://api.imd.fun/health) (computedAt 2026-10-02T07:04:01.619Z) and
[api.imd.fun/contributors](https://api.imd.fun/contributors) (cache: stale). Raw responses are saved in
`data/snapshots/`. Compared with the previous run at 2026-10-02T06:58:28.259Z (6 min earlier).

## Figures (facts, as reported by the API)

| Figure | Now | Previous | Change | API field |
|---|---:|---:|---|---|
| Seats online | 549 | 549 | unchanged | health `connectedDaemons` |
| Seats enrolled | 571 | 571 | unchanged | health `activeEnrollments` |
| Tasks accepted, last 24 h | 60,011 | 60,010 | +1 | health `acceptedLastDay` |
| Paid orders (all time) | 530 | 530 | unchanged | health `payments.orders.paid` |
| Last order paid | 2026-10-02T01:53:06.000Z | 2026-10-02T01:53:06.000Z | unchanged | health `payments.lastPaidAt` |
| Accepted work, all seats (all time) | 595,352 | 595,344 | +8 | sum of contributors `accepted` |

## Top five seats by accepted work (by NFT number)

| Rank | NFT | Accepted | Attempts | Devices | Wallet | vs previous |
|---:|---|---:|---:|---:|---|---|
| 1 | #355 | 3,174 | 3,424 | 2 | `0xb579160d…` | = (unchanged) |
| 2 | #475 | 3,068 | 3,229 | 1 | `0xa227a71e…` | = (unchanged) |
| 3 | #527 | 3,055 | 3,223 | 1 | `0xa227a71e…` | = (unchanged) |
| 4 | #1207 | 3,042 | 3,227 | 1 | `0x5869458f…` | = (unchanged) |
| 5 | #1763 | 3,006 | 3,148 | 1 | `0xa227a71e…` | = (unchanged) |

## What changed

- Seats online: unchanged.
- Seats enrolled: unchanged.
- Tasks accepted (24 h): 60,010 → 60,011 (+1).
- Paid orders: unchanged.
- Accepted work, all seats: 595,344 → 595,352 (+8).
- Last payment: unchanged (2026-10-02T01:53:06.000Z).
- Top five: same seats, same order.

## Inferences (not stated by the API)

- The last paid order was 5.2 h before the health snapshot; with 777 expired and
  8 failed orders against 530 paid, more orders lapse than get paid.
- The top five seats belong to only 3 wallet(s), so leadership is concentrated in few operators.
- Ranking per NFT matters: #355 (2 devices) ranks by summing devices, so a per-device list orders differently.
- Online seats (549) are below enrolments (571): roughly
  96% of enrolled seats were connected at that moment.

## Uncertainty and open questions

- "Seats online" is read as `connectedDaemons` and "enrolled" as `activeEnrollments`; the API does not define them.
- The contributors list holds 642 device rows for 579 NFTs; rows were summed per NFT.
  Its counts are all-time, not 24 h, and the endpoint may serve a cached (stale) copy.
- The comparison window is only 6 min, so changes reflect minutes of activity, not a daily trend.
- Health figures are single samples and can move between calls (seats online and 24 h counts
  have been seen to jump and fall back within minutes); small changes may be noise.
- Open: what an "order" buys, whether expired orders are abandoned or retried, and how acceptance is decided.
