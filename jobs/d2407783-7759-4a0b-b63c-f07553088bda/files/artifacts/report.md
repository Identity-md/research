# Report: record view changes for imd.fun

**Question:** implement the requested changes to the IMD record site and templates.

## What was done (fact)
- The workspace was empty, so the site was built from scratch in `site/` on top of `artifacts/lines.json` (33 lines: 25 claims, 8 statements; 8 sources, 1 unopened).
- `templates/source.txt` and `templates/research.txt` were written with the requested wording and JSON keys; `agents.md` documents them.
- The label rule is enforced in `site/lib.js`; unit tests (7) pass.

## Evidence content (from lines.json, attributed to its sources)
- Only S7 (Identity-md GitHub organisation, a listed channel) yields statements, e.g. burn splits and the 2,000 seats (L28, L30). Everything from X accounts is a claim (e.g. 276 agents judged 1,464 entries, L8, by @taylor_).

## Inferences / uncertainty
- Seats (S7) versus agents (S4) may count different things; 100-agent split (S5) versus 276 agents (S4) may be consistent across rounds. Shown as "Compare" notes, not conflicts.
- Nothing was checked on chain.

## Unanswered / not done
- IMD's request check was unavailable; a local stand-in was used (see README).
- Main contract address and channel ties were not supplied; no browser test was run; fact tables and Summary have no real data yet.
