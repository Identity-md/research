# Investigation: Fren Pet training camps not starting for pets 83633, 83632, 83608, and 83626

**Investigation time:** 27 September 2026, 23:10–23:14 UTC  
**Networks/services checked:** Fren Pet production indexer/API, Fren Pet AI production API/UI, Base mainnet  
**Operator contract:** [`0x065bf5a7AF15c52C91353990CC8F3d97A1595CE7`](https://basescan.org/address/0x065bf5a7AF15c52C91353990CC8F3d97A1595CE7)

## Executive conclusion

All four pets have the same class of failure.

The Fren Pet game believes each pet is eligible to begin both an attack and a defense camp. Each has hundreds of wins, no camp level, no active camp, and `trainingCanStartAtk: true`. Meanwhile, Fren Pet AI is continuing to execute other actions successfully for the same pets. Its public operation feed contains recent successful bonks (and a successful wheel reveal for every pet), but no `startTrainAttack`, `stopTrainAttack`, `startTrainDefense`, or `stopTrainDefense` operation for any of the four.

The **proven proximal cause** is therefore in Fren Pet AI's training scheduling/configuration path, before a training transaction is submitted: eligible pets are not being selected/enqueued for `startTrainAttack`. This is not a failure of the win prerequisite, a pet-specific game-state lock, an exhausted gas account, a stopped agent, or a reverted on-chain start transaction.

The available public evidence does **not** expose the authenticated stored configuration or server source, so it does not prove the exact faulty line. The two leading internal root causes are (1) the scheduler is reading these pets' stored `training` value as disabled/stale/missing even though the UI reported “Only ATK”, or (2) the training eligibility predicate/action builder is dropping these records. Logging the scheduler decision for these four IDs will distinguish them immediately. Treating a successful configuration response as sufficient proof that the worker consumed the configuration is an underlying observability/design defect.

## Results by pet

The snapshot below is from a single GraphQL response from [`https://api.pet.game`](https://api.pet.game), indexed through Base block **51,880,646** (block timestamp **1790550639**, 27 September 2026 23:10:39 UTC).

| Pet | Wins | ATK / DEF | ATK camp level | DEF camp level | Camp active | API says ATK can start | Recent Fren Pet AI evidence | Assessment |
|---|---:|---:|---:|---:|---|---|---|---|
| 83633 | 382 | 22 / 24 | 0 | 0 | false | true | successful bonk at 1790550727; wheel at 1790538843 | scheduler omission |
| 83632 | 203 | 21 / 21 | 0 | 0 | false | true | successful wheel at 1790538843; recent game attack at 1790535301 | scheduler omission; lower bonk frequency is not a camp blocker |
| 83608 | 344 | 21 / 21 | 0 | 0 | false | true | successful bonk at 1790548087; wheel at 1790538843 | scheduler omission |
| 83626 | 230 | 15 / 20 | 0 | 0 | false | true | successful bonk at 1790550127; wheel at 1790538843 | scheduler omission |

There is no evidence that one pet has a different training problem. Pet 83632 is less recently active in battle than the others, but its automation performed a wheel action, its game status is the same (`status: 2`), it is not training, and the game independently returns `trainingCanStartAtk: true`. That difference does not explain failure to start a camp.

## Evidence and reasoning

### 1. Every game-side prerequisite represented by the API is satisfied (fact)

For all four records, the production game API returned:

- `trainingAtk: 0` and `trainingAtkUntil: 0`;
- `trainingDef: 0` and `trainingDefUntil: 0`;
- `trainingActive: false`;
- `trainingCanStartAtk: true` and `trainingCanStartDef: true`;
- a live/active common `status` value of 2; and
- the same owner, `0x2978E6219D540e8E8Cff994bf88Ad68782333Eb2`.

The documented camp progression requires 10 wins for level 1, then 20 more for level 2, 30 more for level 3, and so on ([Fren Pet gameplay documentation](https://fren-pet-docs.vercel.app/gameplay#2-training-camp)). The cumulative wins required through level *n* are therefore `5 × n × (n + 1)`. Even without relying on the API's explicit booleans, the listed win totals permit at least levels 8, 5, 7, and 6 respectively. The claimed prerequisite is not merely met once; it is met repeatedly.

This is primary production-state evidence. The documentation supplies the rule; the API supplies the authoritative indexed state.

### 2. The agents and operator are functioning for these pets (fact)

The public Fren Pet AI endpoint
[`/api/operations?afterTimestamp=0&ids=83633,83632,83608,83626`](https://frenpet.ai/api/operations?afterTimestamp=0&ids=83633%2C83632%2C83608%2C83626)
returned recent operations with `state: "success"` for the pets. Examples include:

- pets 83633, 83608, and 83626: multiple successful `bonkReveal` operations;
- all four pets: `wheelReveal` in transaction [`0x090e…83a4`](https://basescan.org/tx/0x090e2332551c7b17deb42af1b8be9e4d224dadc86e4de440f5c28d0d0bbb83a4);
- pet 83626: a successful bonk in [`0x1078…e03`](https://basescan.org/tx/0x10787f8ead3273dbd8b0af16cdfd1c35e2679030c6f2a0adedab5deeae248e03).

Thus registration, ownership/authorization, operator execution, and at least some gas funding are working. A system-wide worker outage is contradicted by the operation stream.

### 3. No training action is being submitted (fact, within the public feed's retention window)

The same operation response contains no training action for any target pet. Fren Pet AI's deployed client recognizes the action names `startTrainAttack`, `stopTrainAttack`, `startTrainDefense`, and `stopTrainDefense` and renders them in its live activity view. This can be inspected in the deployed `/pets` JavaScript referenced by [`https://frenpet.ai/pets`](https://frenpet.ai/pets). The client also exposes the persisted configuration choices as `disabled`, `atk`, `def`, `weakest`, and `fastest`, displaying `atk` as **Only ATK**.

This absence matters because a reverted attempt should still have an attempted/failed operation or transaction to inspect. Instead, other actions are present and successful while training is absent. The strongest supported interpretation is “not scheduled,” rather than “scheduled and rejected by the game.”

**Limit:** the public operations endpoint returned the most recent 25 matching operations and exposes no documented backward-pagination parameter. Absence is therefore established for that returned window, not for all historical database rows. The zero on-chain/indexed camp state proves that no historical start ever successfully took effect.

### 4. Configuration cannot be independently verified anonymously (fact)

`GET https://frenpet.ai/api/user/config/{petId}` returned HTTP JSON `{"error":"Unauthorized"}` for every target ID. Consequently this investigation accepts the task owner's statement that all four were configured as attack training, but cannot independently read the stored server-side values.

The deployed client has a noteworthy failure-masking behavior: if fetching configuration fails, it catches the error and substitutes a default whose `training` field is `"disabled"`. This affects what the UI can show and can conceal a read/auth/data failure. It does not by itself prove that the backend worker uses the same fallback, but it is a concrete underlying factor and a likely route by which intended `atk` configuration and effective configuration can diverge.

## Root-cause statement

### Established

1. **Immediate failure:** Fren Pet AI does not dispatch `startTrainAttack` for these eligible pets.
2. **Failure boundary:** the defect is upstream of the Fren Pet Diamond training call, inside effective configuration retrieval, eligibility selection, or action construction/enqueueing.
3. **Commonality:** the same boundary and symptom apply to all four pets. There is no evidence of a separate issue for one of them.
4. **Contributing design issue:** neither the UI nor public operation history exposes “evaluated but skipped” decisions, and the UI silently falls back to `training: "disabled"` on config-read failure. This makes a persisted/effective config mismatch look like successful configuration.

### Strong inference, not yet proven

The most likely exact defect is an effective-config mismatch: the UI wrote or displayed `atk`, while the worker sees `disabled`, missing, stale, or an unrecognized value. This parsimoniously explains four pets under one owner failing identically while unrelated actions continue. A shared bug in the worker's training predicate is the other plausible explanation.

There is no evidence here for an ID-width overflow. All four IDs exceed 65,535, but successful wheel/bonk processing of those same IDs shows the platform and operator generally handle them; only an inspection of training-specific casts could establish such a narrower bug.

### Unanswered

- What exact configuration row/value/version does the worker load for each ID?
- Does a scheduler trace say `training_disabled`, `not_eligible`, `already_training`, or an exception?
- Was the configuration POST committed to the same database/environment read by the worker?
- Does the worker compare against `"attack"` while the current UI stores `"atk"`, or otherwise use an outdated enum/schema?
- Are failed scheduler evaluations retained anywhere outside the public operation endpoint?

## Recommended repair

1. **Immediate recovery:** authenticated staff should read the four raw configuration rows and normalize each `training` value to the worker's canonical attack enum (the current deployed UI writes `atk`). Re-save them, invalidate worker/config caches, and manually enqueue one `startTrainAttack` for each pet. Confirm the game API changes to `trainingActive: true` and records a nonzero attack-training end time.
2. **Fix the worker contract:** validate configuration against one shared enum/schema at write and read time. Reject unknown/missing values instead of coercing them to disabled. Add a migration for legacy values such as `attack`/`Only ATK` if they exist.
3. **Instrument selection:** for every eligible registered pet, record a decision with pet ID, config revision, game snapshot/block, `canStartTrainingAtk`, chosen action, or an explicit skip reason. Alert when `training=atk && canStartTrainingAtk=true && trainingActive=false` persists through two scheduler cycles.
4. **Remove silent UI fallback:** show configuration fetch/auth failure as an error. Do not render or save `disabled` as if it were the existing setting when the read failed.
5. **Regression test:** seed four pets with IDs above 65,535, zero training levels, and wins around each threshold; set `training=atk`; run a scheduler cycle; assert one start is enqueued per pet, then no duplicate while active, and a stop is enqueued at expiry. Include a mixed batch where other actions continue.

If the raw rows already contain canonical `atk` and the worker trace confirms it read them, move directly to the eligibility predicate: compare the worker's input fields with the current game fields (`trainingCanStartAtk` in the indexer versus `canStartTrainingAtk` in the Diamond's full-info tuple). A stale field-name/schema mapping would yield exactly this “game says true, worker never submits” behavior.

## Reproduction details

Game-state query used (POST to `https://api.pet.game`, `Content-Type: application/json`):

```graphql
query {
  p83633: pet(id: 83633) { id name status owner winQty petWins attackPoints defensePoints trainingAtk trainingAtkUntil trainingDef trainingDefUntil trainingCanStartAtk trainingCanStartDef trainingActive createdAt lastAttacked }
  p83632: pet(id: 83632) { id name status owner winQty petWins attackPoints defensePoints trainingAtk trainingAtkUntil trainingDef trainingDefUntil trainingCanStartAtk trainingCanStartDef trainingActive createdAt lastAttacked }
  p83608: pet(id: 83608) { id name status owner winQty petWins attackPoints defensePoints trainingAtk trainingAtkUntil trainingDef trainingDefUntil trainingCanStartAtk trainingCanStartDef trainingActive createdAt lastAttacked }
  p83626: pet(id: 83626) { id name status owner winQty petWins attackPoints defensePoints trainingAtk trainingAtkUntil trainingDef trainingDefUntil trainingCanStartAtk trainingCanStartDef trainingActive createdAt lastAttacked }
  _meta { status }
}
```

The API is a GraphQL POST service, so its root link opens the GraphQL playground rather than a durable per-query page. The query above makes the reported snapshot independently reproducible. Values are time-sensitive and may change after remediation; the block number anchors the observation.

## Confidence

- **High:** eligibility, zero camps, common symptom, ongoing non-training automation, and localization to pre-submission scheduling.
- **Moderate:** effective configuration mismatch as the most likely exact internal defect.
- **Not established from public access:** the precise server-side line or whether config storage versus the training predicate is the final fault.
