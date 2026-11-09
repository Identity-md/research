# Owner-action test (mode 0), Sepolia: claimFees(551) on the IMD launch factory

## Outcome in one paragraph

The test did not produce a transaction. The intent batch `fee-claim` ran and settled with all three items accepted, and the owner's mandate was active at every check, but every one of the three permitted action attempts (`claim-551`, `claim-551-b`, `claim-551-c`) was refused by the plane before compilation with the same reason, word for word:

> item_b01_0001's intent has 0 of the 2 distinct holders it needs (1 replicas, 0 counted)

No action was ever simulated, ready, sent or confirmed. No transaction hash exists for any attempt. No call to `claimFees(551)` was broadcast, so nothing moved on chain and nothing left the owner's account. The goal finished after the third refusal, as the objective instructed.

## What the goal asked

| Field | Value |
| --- | --- |
| Chain | Sepolia, chainId 11155111 |
| Owner | 0x047f606fd5b2baa5f5c6c4ab8958e45cb6b054b7 |
| Asset | Launch 551 on the IMD launch factory 0x1721d7ae9c2bba9be52a316578c91295605c00fc (univ4_hook launch, one pool) |
| Mandate | 0xc0ca84c41d2e67866dec18175e0fa7f61c884ce9bde887ab23022fa5a3eb1f9c |
| Mandate mode | 0 (the owner sends from their own wallet) |
| Mandate quorum | 2 |
| Mandate expiry | 2026-12-09T21:59:56.000Z |
| Mandate scope | target 0x1721d7ae9c2bba9be52a316578c91295605c00fc, function `claimFees(uint64)` |
| Permitted call | exactly one: `claimFees(551)` on that factory |

The objective's steps were: spawn one intent batch named `fee-claim` with three items, each writing a single `asset-intent@1` of kind `fees.claim` for launch 551; once it settled and the mandate was active, act once as `claim-551` with quorum 2; on refusal, retry under `claim-551-b` and then `claim-551-c`, three attempts at most; wait ten minutes and recheck if the mandate was not yet active, at most six times; open no children, ask no oracle, set no watches, spawn no other batch; finish once an action was simulated, ready, sent or confirmed, or after the third refusal or the sixth wait.

## What happened, episode by episode

The goal ran five orchestration episodes. The record below is taken from the orchestrator's notes in the goal record and from the goal record's batch, mandate, refusal and wake fields as each episode saw them.

### Episode 1: spawn the intent batch

The goal record showed no batches, no handed results, no mandates and no actions. The orchestrator spawned the only batch the objective permits:

- Name: `fee-claim`
- Mode: research, with `"intents": true`
- Items: 3
- Brief (as recorded in the goal record): "Produce one independent fee-claim intent for launch 551 on Sepolia, chain 11155111, at factory 0x1721d7ae9c2bba9be52a316578c91295605c00fc. Your entire result must be exactly one JSON object with these six fields: {"schema":"asset-intent@1","chainId":11155111,"kind":"fees.claim","factory":"0x1721d7ae9c2bba9be52a316578c91295605c00fc","launchNumber":551,"rationale":"<one or two sentences on why claiming now is sensible>"}. Replace only the rationale placeholder with your own one or two sentences. …" (the record truncates the brief after this point)

The episode set a wake on the batch settling. No action, child, ask or watch was requested.

### Episode 2: batch settled, mandate active, first action

`fee-claim` had settled and was listed under `withheld`: 3 items total, 3 accepted, 0 failed. Its sources check showed 3 checked and 0 flagged. Its item files were, by design, never handed to the orchestrator and never requested.

The mandate 0xc0ca84c41d2e67866dec18175e0fa7f61c884ce9bde887ab23022fa5a3eb1f9c was listed as `active` on chain 11155111, mode 0, quorum 2, with the scope above. Because the mandate was already active, no ten-minute wait was needed.

The orchestrator requested the first action exactly as the objective specified:

```json
{"name":"claim-551","intents":"fee-claim","mandate":"0xc0ca84c41d2e67866dec18175e0fa7f61c884ce9bde887ab23022fa5a3eb1f9c","quorum":2}
```

### Episode 3: first refusal, second action

The plane refused `claim-551`. The refusal arrived as an `effect.action` wake at 2026-11-09T22:01:56.880Z and was listed under `refused` in the goal record. The goal record's `actions` list stayed empty, so the action never entered a simulating, ready, sent or confirmed state and no hash was ever assigned.

The orchestrator requested the second attempt, `claim-551-b`, with the same intents, mandate and quorum.

### Episode 4: second refusal, third action

The plane refused `claim-551-b` with the identical reason. The refusal arrived as an `effect.action` wake at 2026-11-09T22:03:31.783Z. `actions` remained empty; `effects.pending` was 0.

The orchestrator requested the third and final permitted attempt, `claim-551-c`, with the same intents, mandate and quorum.

### Episode 5: third refusal, finish

The plane refused `claim-551-c` with the identical reason. The refusal arrived as an `effect.action` wake at 2026-11-09T22:05:36.975Z and was listed in the goal record under `refused` as the decision "action claim-551-c". That was the third refusal, so the orchestrator set `finish` to true and requested nothing else.

At the final episode the goal record showed: `fee-claim` settled and withheld (3 accepted, 0 failed); the mandate still active with expiry 2026-12-09T21:59:56.000Z; `actions` empty; `effects.pending` 0; `wakes.waiting` 0.

## Action record

Every attempt used the same intents batch (`fee-claim`), the same mandate (0xc0ca84c41d2e67866dec18175e0fa7f61c884ce9bde887ab23022fa5a3eb1f9c) and the same quorum (2), which is the mandate's own quorum and the least the plane accepts under it.

| # | Action name | State | Hash | Refused at (effect.action wake) | Refusal, word for word |
| --- | --- | --- | --- | --- | --- |
| 1 | `claim-551` | refused | none (no hash was ever reported) | 2026-11-09T22:01:56.880Z | item_b01_0001's intent has 0 of the 2 distinct holders it needs (1 replicas, 0 counted) |
| 2 | `claim-551-b` | refused | none (no hash was ever reported) | 2026-11-09T22:03:31.783Z | item_b01_0001's intent has 0 of the 2 distinct holders it needs (1 replicas, 0 counted) |
| 3 | `claim-551-c` | refused | none (no hash was ever reported) | 2026-11-09T22:05:36.975Z | item_b01_0001's intent has 0 of the 2 distinct holders it needs (1 replicas, 0 counted) |

No action reached `simulating`, `ready`, `flagged`, `approved`, `denied`, `sent`, `confirmed`, `failed` or `expired`. The refusals happened at the act stage, before any intent was compiled into a call, so there is no transaction, no simulation result and no on-chain footprint from this goal.

## Mandate waits

The objective allowed up to six ten-minute waits for the mandate to become active. None were used: the mandate was already `active` the first time it was checked (episode 2) and stayed active through the last episode.

| Waits allowed | Waits scheduled | Waits completed |
| --- | --- | --- |
| 6 | 0 | 0 |

## Why the actions were refused, as far as the record shows

All three refusals name the same cause: the plane counted zero distinct holders behind the intent of item `item_b01_0001` against the two the mandate's quorum requires, reporting "1 replicas, 0 counted". This is despite `fee-claim` accepting all three of its items.

The orchestrator skill's reference states that an intent no holder other than the orchestrator stands behind does not count, and nor does one that only the orchestrator's own seats wrote. The refusal text is consistent with that rule: the accepted intents appear to have been written by seats the plane does not count as distinct holders for quorum purposes. The orchestrator never saw the intents' files (they are withheld by design), so this reading rests on the refusal text and the reference, not on inspection of the items.

Within the objective's constraints there was no permitted way to change this outcome:

- The objective forbade spawning any other batch, so no new intents could be gathered from other holders.
- The quorum could not be lowered: the mandate's quorum is 2, and an act's quorum may never be under the mandate's.
- Children, oracle asks and watches were all forbidden.
- The only permitted move after a refusal was to act again under a new name, which the orchestrator did twice. Retrying under a new name does not change which holders stand behind the intents, so the same refusal recurred each time.

## Resources used

| Resource | Used | Allowed |
| --- | --- | --- |
| Items | 3 | 12 |
| Episodes | 5 | 12 |
| Batches spawned | 1 (`fee-claim`) | 1 permitted by the objective |
| Action attempts | 3 | 3 permitted by the objective |
| Mandate waits | 0 | 6 permitted by the objective |
| Children opened | 0 | 0 permitted |
| Oracle asks | 0 | 0 permitted |
| Watches set | 0 | 0 permitted |

The goal built no code. The goal record's `trunk` is null, so there is no repository or commit to name.

## What this report rests on

- The goal record (`.imd/reads/goal.json` as handed for the write-up): the objective, the `fee-claim` batch entry with its brief, item counts, `settled` and `withheld` flags and sources check, the `withheld` list, the empty `refused` list and absent `actions` at the final episode, and `items.used` 3 of 12 at episode 5 of 12.
- The orchestrator's notes for episodes 1 through 5 in that record, which preserved each action's name, state, absent hash, the timestamp of each `effect.action` wake and each refusal word for word as the episode that saw it recorded it. The final goal record no longer lists the three refusals under `refused` (that list is per-episode), so the refusal texts and wake timestamps above are taken from the notes written in episodes 3, 4 and 5, which copied them from the record of their own episode.
- The orchestrator skill reference (`.imd/reads/skills/goal-orchestrator/REFERENCE.md`) for the rules on action quorum, distinct holders and action states.

## What is missing

- No item results from `fee-claim` were ever handed to the orchestrator, by design of intent batches, so the three rationales the items wrote are not in this report.
- No action state beyond refusal, no hash, no simulation output and no transaction exist to report.
- The record does not say which seats or wallets wrote the three accepted intents, so the exact reason the plane counted zero distinct holders cannot be confirmed from the goal record alone; the reading given above is an inference from the refusal text and the skill reference.

## Recommendation for a repeat of this test

If the owner wants a claim to go through, the next goal should either allow the orchestrator to spawn a replacement intent batch sized so that at least two distinct holders other than the orchestrator write intents for the same item, or allow a `replicas` setting on the intent batch so each item is written by several holders. Until then, `claimFees(551)` remains callable by anyone directly on the factory and pays the launch's requester and the network, so no funds are blocked by this outcome.
