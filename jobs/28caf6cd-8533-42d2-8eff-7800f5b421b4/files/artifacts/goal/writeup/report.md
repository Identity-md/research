# imd.fun: reaching a price quote

**Evidence-backed pass rate: 97/100 attempts (97%).** A pass means the saved attempt reports acceptance of its request by a quote API, a quoted order, and a payment amount. A price copied from documentation or a free check alone does not count. The five merges report 19, 19, 20, 20, and 19 such quotes, respectively. Their agents saved response fields or summaries; these are not independently authenticated HTTP transcripts. The original user asks are not separately preserved, so the four ask groups below are reconstructed from submitted requests and replies. Exact fidelity to an absent original ask cannot be established. [M1][M1] [M2][M2] [M3][M3] [M4][M4] [M5][M5]

| Reconstructed ask | Evidenced quotes / attempts | Explicitly read `skill.md` | Quotes after read | Quotes without a recorded successful read |
|---|---:|---:|---:|---:|
| Research the five biggest tokens on Robinhood Chain | 24/25 (96%) | 15/25 | 15/15 | 9/10 |
| Build a one-page bakery website | 24/25 (96%) | 12/25 | 12/12 | 12/13 |
| Find the current CryptoPunks floor price | 25/25 (100%) | 10/25 | 10/10 | 15/15 |
| Give one quick BTC trade call for today | 24/25 (96%) | 15/25 | 15/15 | 9/10 |
| **Overall** | **97/100 (97%)** | **52/100** | **52/52 (100%)** | **45/48 (93.75%)** |

Sources for every table row: [M1, attempts 001–020][M1]; [M2, 021–040][M2]; [M3, 041–060][M3]; [M4, 061–080][M4]; [M5, 081–100][M5]. “Read” means a successful opening or fetch of [imd.fun/skill.md](https://imd.fun/skill.md) explicitly recorded in `steps`, not merely seeing its link or mentioning it later. Attempt 029 tried to open it but the web tool could not access it, so it is in the “without a recorded successful read” column. All three quote misses are in that column. Lack of a recorded read is not proof that an agent never saw the file. The 52/52 versus 45/48 difference is descriptive, not evidence that reading the skill caused success. [M1][M1] [M2][M2] [M3][M3] [M4][M4] [M5][M5]

Attempt **059** is the one counting correction: its `reached_quote` flag is false and its `price` field is null, but its saved evidence reports HTTP 201, `status=quoted`, `oracle.request`, and `500000000000000000` atomic IMD at 18 decimals. Its reply also says the request was accepted and quoted. It lacked the *purchased floor-price answer*, which lies beyond this quote-only target; therefore it counts as a quote. Attempt 028's earlier quote for an accidentally overwritten, unrelated brief does **not** count; its later corrected BTC quote does. In 002, the recorded Explorer quote API returned HTTP 200 with `created=true`, quoted status and payment amount, and therefore meets the same acceptance standard. [M3, 059][M3] [M2, 028][M2] [M1, 002][M1]

All 97 evidenced quotes show a **0.5 IMD service price** (`500000000000000000` atomic units at 18 decimals); this is neither the CryptoPunks floor nor a delivered report, website or trade call. A quote admits a proposed job or oracle request and does not prove fulfillment. The saved attempts do not show payment, an agent signature, a wallet connection, or a finished result. These are observations of the supplied records, not a transaction audit. [M1][M1] [M2][M2] [M3][M3] [M4][M4] [M5][M5]

## What prevented a quote

**All three actual misses were access or transport failures before a quote response.** None is evidence that imd.fun rejected the subject of the ask. Each cause occurred once; the quotation is from the named attempt. [M1, 018][M1] [M2, 029][M2] [M5, 088][M5]

| Terminal cause | Count | Recorded excerpt and source |
|---|---:|---|
| Browser/web tool could not submit a POST for the bakery request | 1 | “The available web tool cannot send POST requests.” [M1, 018][M1] |
| Proxy failed before returning HTTP for the token research request | 1 | “Proxy CONNECT aborted due to timeout” [M2, 029][M2] |
| API access returned HTTP 403/error 1010 for the BTC request | 1 | “HTTP 403, error code 1010” [M5, 088][M5] |

This access problem also created substantial **recovered** friction: 36 *successful* attempts across the five batches recorded client/API access or response-reading trouble and then reached a quote (batch counts 6, 6, 10, 7, 7). The exact symptoms vary, including Python-client 403s and unreadable responses; the groups are not 36 additional failures. One representative recovery says, “Python HTTP client received 403; retry with curl received HTTP 200.” [M1, recovered obstacles][M1] [M2, 026 and recovered obstacles][M2] [M3, resolved friction][M3] [M4, recovered friction][M4] [M5, transient difficulties][M5]

Three other records—015, 059 and 095—describe the missing *paid oracle answer* after a successful quote. This is a boundary or reporting problem, not a quote failure. Attempt 059 says, “it did not provide the floor price without payment.” Oracle checks also produced recoverable wording or schema problems: for example, 055 first got `HTTP 422 ambiguous_question` before a revised panel-evidence request was accepted; 063 and 071 encountered unrecognized keys in a check payload before quoting. [M1, 015][M1] [M3, 055 and 059][M3] [M4, 063 and 071][M4] [M5, 095][M5]

### Source key

The five supplied merge files are transient inputs, so this report retains their batch counts, decisive exceptions and failure excerpts. The hashes identify the exact source bytes; each merge also contains per-attempt evidence and source identifiers. Links point to the read paths supplied for this job, not to a fresh imd.fun verification.

- [M1][M1]: `.imd/reads/artifacts/merge-01` (attempts 001–020; SHA-256 `ae2f69c19ee75872ed1e2dc64f18227f671c6a0d13d351c0697c09395106e278`).
- [M2][M2]: `.imd/reads/artifacts/merge-02` (021–040; `4604cf9798ba707825ec2583f038a4d680b0bd3cf33fefb18db261796c6dd4f8`).
- [M3][M3]: `.imd/reads/artifacts/merge-03` (041–060; `af1499bd7cbbda67c4805aa0a223f5649e841297c4139198e367b435f439e3d7`).
- [M4][M4]: `.imd/reads/artifacts/merge-04` (061–080; `81c716717b0a9cdba0c7ee0e17f10772dff5fde571ada6e4fa1ba47bc5237b8e`).
- [M5][M5]: `.imd/reads/artifacts/merge-05` (081–100; `270a2c601ffbb78b32196606ea3e5cd321ebf98c31256cde9cbe76f696c77460`).

## Fixes, in priority order

1. **Make quoting reachable from common agent environments.** Add a same-origin, browser-usable quote form on imd.fun and make the documented API work consistently for common HTTP clients, with a tested fallback route and clear 403/1010 and timeout diagnostics. The form would remove 018's POST-only tool barrier. Better client compatibility and an alternate route target the 088 denial and the 36 recovered access cases; an external proxy timeout such as 029 may still be outside imd.fun's control. [M1, 018 and recovered obstacles][M1] [M2, 029 and recovered obstacles][M2] [M3, resolved friction][M3] [M4, recovered friction][M4] [M5, 088 and transient difficulties][M5]
2. **Make `skill.md` easy to find and operational.** Link it prominently from the homepage; include one minimal request-to-quote example per action, a browser route, a curl fallback, and short recovery steps for 403/1010 and timeouts. The homepage was the first recorded imd.fun page in 96/100 attempts, while only 52/100 explicitly read the skill. This would make the recovery path visible to agents like 018 and 088 and reduce the repeated client retries; the record does not establish how many failures discovery alone would have prevented. [M1, navigation][M1] [M2, discovery][M2] [M3, first URL][M3] [M4, discovery][M4] [M5, first URLs][M5]
3. **Separate “quote accepted” from “answer delivered” in the UI and skill, and publish exact check-versus-quote schemas.** Show the service fee, quote status and next paid step separately from the requested output. Provide worked definitions for a time-sensitive CryptoPunks floor and examples of the accepted short oracle-check body versus the full quote body. This would prevent the false quote-failure classification in 059 and clarify 015/095; schema examples would remove the avoidable validation retries seen in 063, 071 and 091. [M1, 015][M1] [M3, 059][M3] [M4, 063 and 071][M4] [M5, 091 and 095][M5]

[M1]: ../../../.imd/reads/artifacts/merge-01
[M2]: ../../../.imd/reads/artifacts/merge-02
[M3]: ../../../.imd/reads/artifacts/merge-03
[M4]: ../../../.imd/reads/artifacts/merge-04
[M5]: ../../../.imd/reads/artifacts/merge-05
