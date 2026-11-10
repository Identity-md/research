# Third test of owner actions (mode 0) on Ethereum mainnet: top-up

## Outcome

The goal finished on its own stopping condition: one action reached state `ready`.

| Action | Intents batch | Mandate | Quorum | Last reported state | Hash |
| --- | --- | --- | --- | --- | --- |
| `top-up-1` | `top-up` | `0x384901bddda3b10173014f3d939ecf84f64afcad95786d955f62b4ed3736a9f2` | 3 | `ready` | `0x89c2567a2df0da62ba7ce9bd4cb2528dabdba7dc27fd001719fabf3abbbd0595` |

- Refusals: none. `goal.json.refused` was empty in every episode.
- `top-up-2` was never spawned and never acted on, because no refusal occurred.
- No ETH transfer is established as sent or confirmed. The mandate is mode 0, so the owner `0x047f606fd5b2baa5f5c6c4ab8958e45cb6b054b7` must send the compiled action from their own wallet. The last state the plane reported is `ready`, with the detail "simulated within what it declares: waiting for its owner".
- The goal built no code. `trunk` is null in `goal.json`, so there is no repository or commit to name.

## What was asked

The objective asked for exactly one intent batch named `top-up`, run on five independent machines reading Ethereum mainnet (chain 1) at one pinned block, followed by exactly one action under the owner's mandate once that batch settled. Each machine was to read the native ETH balance of three accounts at the pinned block and write one `asset-intent@1` of kind `treasury.rebalance`, adding a move of 500000000000000 wei (0.0005 ETH) to each account whose balance was below 10000000000000000 wei (0.01 ETH), in the listed order, and skipping the rest.

The allowed recipients, per the objective, are:

1. `0xb7a832db45f240f876432bf8b222bff30b4be8ff`
2. `0xbe11d80c27863c950485d269992dc086e9f397a9`
3. `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2`

## What happened, episode by episode

The goal ran 5 of its 14 allowed episodes and used 1 of its 12 items. Every statement below comes from the orchestrator's notes and the batch, withheld, refused and action records in `.imd/reads/goal.json`.

### Episode 1: spawn

The decision spawned the batch `top-up` with the objective's settings and nothing else:

- `intents: true`, `replicas: {size: 5, quorum: 4}`, exactly 1 item
- `chain: {chainId: 1, pin: "head", accounts: [the three addresses above, in order]}`
- The item brief copied word for word from the objective (quoted in full below)
- No action, no read, no child, no ask, no watch

### Episode 2: chain read complete, item running

The plane's chain read for `top-up` finished. Every replica of the item was handed the same snapshot:

| Field | Value |
| --- | --- |
| Chain | Ethereum mainnet, chainId 1 |
| Pinned block | 26381929 |
| Block hash | `0x6e659ea5b9a6b74d4bd2c61629b21033a6b0a5a3c32a1802a58641023d00d042` |

The item was running with 0 accepted, 0 failed, 0 waiting. The wake received was an `effect.snapshot` completion, not a batch settlement, so the episode kept waiting on the same batch and did not count the wait against the six mandate waits.

The mandate `0x384901bddda3b10173014f3d939ecf84f64afcad95786d955f62b4ed3736a9f2` was listed in `goal.json.mandates` as `active` from this episode on: chain 1, mode 0, quorum 3, `expiresAt` 2026-12-10T03:51:49.000Z. Its visible scope summary listed only the IMD launch factory `0x12c63b581d07093f6126bc02263c58f7eadaa96f` with `claimFees(uint64)`. The orchestrator reference says a mandate's recipients, allowances and argument rules are not shown in `goal.json`, so the ETH recipient scope the objective describes could not be confirmed from the summary and was left to the plane to enforce at compile time. It did compile, which is consistent with the scope the objective describes.

### Episode 3: batch settled, action requested once

`top-up` settled: 1 item total, 1 accepted, 0 failed, 0 running, 0 waiting. `goal.json` listed it under `withheld` with `settled: true`, so its intent files were never handed to the orchestrator, as the objective anticipated. The mandate was still active. The decision requested exactly one action:

```json
{"name":"top-up-1","intents":"top-up","mandate":"0x384901bddda3b10173014f3d939ecf84f64afcad95786d955f62b4ed3736a9f2","quorum":3}
```

### Episode 4: simulating

`goal.json.actions` listed `top-up-1`: lane `owner`, kinds `["treasury.rebalance"]`, state `simulating`, hash `0x89c2567a2df0da62ba7ce9bd4cb2528dabdba7dc27fd001719fabf3abbbd0595`, detail "waiting for the simulator". An `effect.action` wake at 2026-11-10T03:57:25.786Z reported the same. Simulating is not a finishing state, so the episode waited with a 10-minute fallback and requested nothing.

### Episode 5: ready, finish

An `action.ready` wake at 2026-11-10T03:57:42.843Z carried payload name `top-up-1`, state `ready`, same hash. `goal.json.actions` agreed: state `ready`, detail "simulated within what it declares: waiting for its owner". The objective says to finish once an action is simulated, ready, sent or confirmed, so the decision set `finish: true` and requested nothing else.

## Mandate waits, refusals and other limits

| Limit from the objective | Used |
| --- | --- |
| Mandate waits (10 minutes each, at most 6) | 0 of 6: the mandate was active before the batch settled |
| Act refusals (finish on the second) | 0 |
| `top-up-2` (only after a too-few-holders refusal) | not spawned |
| Children, oracle asks, watches, other batches | none |
| Items | 1 of 12 |
| Episodes | 5 of 14 |

Every refusal word for word: there were none to quote.

## The item brief, word for word

The batch `top-up` carried this brief, copied from the objective:

> Read the native ETH balance of each of these accounts at the block .imd/reads/chain.json pins (its accounts give them; or eth_getBalance at exactly that block, never latest): 0xb7a832db45f240f876432bf8b222bff30b4be8ff, 0xbe11d80c27863c950485d269992dc086e9f397a9, 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2. For each account, in exactly that order, whose balance is below 10000000000000000 wei (0.01 ETH), add one move {"asset":"native","to":"<that account>","amount":"500000000000000"}. Skip every account at or above it. Write, as your whole result, one asset-intent@1 and nothing else:
> {"schema":"asset-intent@1","chainId":1,"kind":"treasury.rebalance","moves":[<the moves>],"approvals":[],"rationale":"<each account's balance in wei at the pinned block, and which you topped up>"}
> Addresses in lowercase, amounts as decimal strings of wei, the moves in the order the accounts are listed above.

The brief asks one item for one piece of work and says exactly what its result must contain. `goal.json` shows the brief truncated after "Skip every ac…"; the full text above is the objective's, which the episode 1 decision copied unchanged.

## What the withheld intent should contain: an independent check

The five replicas' intent files were withheld throughout and never handed to the orchestrator, so their moves and rationales cannot be quoted. To let a reader judge what the ready action most likely carries, I re-read Ethereum mainnet at the batch's pinned block with an archive `eth_getBlockByNumber` and three `eth_getBalance` calls at block 26381929 exactly. This is my own check, made while writing the report, not a goal result.

The block hash returned, `0x6e659ea5b9a6b74d4bd2c61629b21033a6b0a5a3c32a1802a58641023d00d042`, matches the batch's snapshot. Its timestamp is 2026-11-10T03:50:35Z.

| Account | Balance at block 26381929 (wei) | Below 0.01 ETH? | Expected move |
| --- | --- | --- | --- |
| `0xb7a832db45f240f876432bf8b222bff30b4be8ff` | 1634690350554818 | yes (about 0.0016 ETH) | 500000000000000 wei to this account |
| `0xbe11d80c27863c950485d269992dc086e9f397a9` | 706349479506548120 | no (about 0.706 ETH) | skip |
| `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2` | 2113238420561957318780456 | no (about 2,113,238 ETH, the WETH contract) | skip |

If the five machines followed the brief, each wrote an intent with exactly one move: 0.0005 ETH native to `0xb7a832db45f240f876432bf8b222bff30b4be8ff`. That is within the mandate's 0.002 ETH daily allowance and goes to one of its three listed recipients, which is consistent with the action compiling and simulating under the mandate and reaching `ready`. The plane's own compile, not this check, is what the action rests on.

## What is missing

- The intent files of `top-up` were withheld, so the exact moves and rationales the five holders wrote are not quoted here. The check above shows what the brief required at that block.
- The counted-holder total behind `top-up-1` is not shown in `goal.json`. The action compiled with quorum 3 under a batch of 5 replicas and quorum 4, and no refusal about counted holders occurred.
- `sent` and `confirmed` were not reached while the goal ran. Whether the owner has since sent the transaction is outside this record. Any later state change would wake the goal, and the episode 5 notes instruct any later episode to record the new state and hash verbatim and finish again without new actions or batches.

## Sources

- `.imd/reads/goal.json`: objective, notes for episodes 1 to 5, `batches[top-up]` (chain snapshot, items, replicas, withheld, settled), `withheld`, `refused` (empty), `trunk` (null), `goal.items` (1 of 12).
- The orchestrator's episode 4 and 5 notes, which record `goal.json.actions` for `top-up-1` (states `simulating` and `ready`, hash, details) and the `effect.action` and `action.ready` wakes at 2026-11-10T03:57:25.786Z and 2026-11-10T03:57:42.843Z.
- The orchestrator's episode 2 to 5 notes, which record `goal.json.mandates` for `0x384901bddda3b10173014f3d939ecf84f64afcad95786d955f62b4ed3736a9f2` (active, chain 1, mode 0, quorum 3, expiresAt 2026-12-10T03:51:49.000Z).
- My own archive reads of Ethereum mainnet at block 26381929, described above.
