# IMD swarm digest — 2 October 2026

**Observed 2026-10-02T18:58:59.158967+00:00 UTC; previous run 2026-10-02T07:04:13.606Z (~11.9 hours earlier).** Baseline is the latest pre-existing repository snapshot. Evidence: [current responses](current-snapshot.json), [previous responses](previous-snapshot.json). Live primary sources: [health](https://api.imd.fun/health) and [contributors](https://api.imd.fun/contributors).

**API-reported facts.** Health was computed at 2026-10-02T18:58:56.296Z (previous: 2026-10-02T07:04:01.619Z). Counts below describe API observations, not independently verified activity.

| Figure / health field | Previous | Current | Change |
|---|---:|---:|---|
| Seats online* (`connectedDaemons`) | 549 | 547 | -2 |
| Seats enrolled* (`activeEnrollments`) | 571 | 570 | -1 |
| Tasks accepted, rolling 24 h (`acceptedLastDay`) | 60,011 | 59,826 | -185 |
| Paid orders (`payments.orders.paid`) | 530 | 567 | +37 |
| Last paid (`payments.lastPaidAt`, UTC) | 2026-10-02T01:53:06.000Z | 2026-10-02T18:54:40.000Z | advanced |

**Five leading NFT seats by accepted work.** Sum `contributors[].accepted` across rows sharing `tokenId`; sort descending, breaking ties by ascending NFT number. These are endpoint totals, not the rolling 24-hour metric above.

| NFT | Rank: previous → current | Previous accepted | Current accepted | Change |
|---|---:|---:|---:|---:|
| #355 | 1 → 1 | 3,174 | 3,174 | unchanged (0) |
| #475 | 2 → 2 | 3,068 | 3,068 | unchanged (0) |
| #527 | 3 → 3 | 3,055 | 3,055 | unchanged (0) |
| #1207 | 4 → 4 | 3,042 | 3,042 | unchanged (0) |
| #1763 | 5 → 5 | 3,006 | 3,006 | unchanged (0) |

**What changed (derived).** Online daemons changed by -2, active enrollments by -1, and rolling daily acceptances by -185. Paid-order count changed by +37; the latest payment timestamp advanced. The top five retain the same NFT membership and order.

**Interpretation, uncertainty and unanswered questions.** *“Seats online” maps to `connectedDaemons`, and “enrolled” to `activeEnrollments`; these are field-name interpretations, not proof of distinct NFT seats online. A falling rolling count does not imply negative work: older acceptances leave the window. Contributors returned cache status `hit` and cache-control `public, max-age=30`; fetches are not atomic and underlying contributor freshness is unknown. The responses do not establish the historical start of contributor/payment totals, the acceptance rules, or whether device totals can overlap. Summing assumes additive rows. The previous snapshot is supplied repository evidence, not a historical response independently re-fetched today. No on-chain verification or independent review was performed.
