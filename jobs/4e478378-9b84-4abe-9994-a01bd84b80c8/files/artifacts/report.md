**BLACKOUT launch research — Robinhood Chain 4663**

Research date: **13 October 2026 (UTC)**. BLACKOUT source inspected: `8cd615252481e025cca0b225437056467ddf5405`, the published result of job **2f166600-ba14-4659-9409-a70218d2e97e**. Scope: public documentation, public plane responses, historical transactions, read-only RPC calls, and local fork tests. No payment, launch submission, signature, deployment or transaction was sent to a public chain. The free `/requests/check` calls created no paid order or job. [Published rehearsal job][JREHEARSAL], [pinned runbook][RUNBOOK].

**Findings that change launch planning**

- **FACT: ETH-paired hook launches are supported today, and one already succeeded.** KING launch **832**, job **0d76ba8d-53ca-4516-955a-de72bc596ae9**, used native ETH through the specified LaunchFactory. Its successful transaction is `0x296e1cc73b3b899128f22c7b92f20cbebeaec216a4d01ce01f5d9a353f012544`. The premise that all recorded 4663 hooks were IMD-paired is incorrect. [Launch 832][L832], [transaction][TX832].
- **FACT: the current BLACKOUT repository is rejected before admission.** A live imported-launch check returned `bytecode_hash`: the repository must add `bytecode_hash = "none"` to `foundry.toml` and publish the change; the launch adapter cannot edit that configuration. The file currently selects `via_ir = true` and omits `bytecode_hash`. Objective prose cannot repair this. [Pinned configuration][CONFIG], [captured final preflight](../evidence/preflight/imported-final.json).
- **FACT: a medium judge finding can block deployment.** Sherwood launch **1355** was parked for an unresolved medium after two fix rounds; low findings remained in successful launch **1389**. Accepted job/review status does not mean the launch is admissible. [1355][L1355], [1389][L1389], [judge submissions][S1355].
- **FACT: M4 should use named backward references**, such as `$contract:Params` and `$contract:GameRegistry`, rather than `$contract[0]`. Eight manifest contracts are supported; the request body's separate `contracts` selector is limited to four entries. [Current manifest schema][WORKER], [contracts launch reference][CONTRACTSREF].
- **MEASURED: one-contract launches took a median 63.3 minutes from posting to inclusion**, across 17 successful deployments in the rolling week defined below. **No eight-contract `evm_contracts` deployment was recorded in that cohort**, so there is no defensible empirical eight-contract “typical time.” [Launch index][INDEX], [timing data](../evidence/timing.json).

The plane identified its deployed source as `bdb0621d1a92b9ce4f1edda1001f0679200b0409` (protocol 1). The final imported-source preflight capture is timestamped **2026-10-13T05:56:45.045597+00:00**. [Plane version](https://api.imd.fun/version), [captured preflight](../evidence/preflight/imported-final.json).

Labels below distinguish **FACT** (observed primary-source evidence), **MEASURED** (local computation/test), **INFERENCE** (interpretation or advice), and **UNKNOWN** (not established). A local fork pass is not an IMD admission verdict or an independent security audit.

**1. ETH pairing, exact fields, valuation and ticks**

**FACT — three independent layers support ETH.** Current [IMD delivery documentation][DOCDELIVERY] permits `pairWith: "eth"`; [live capabilities][CAPS] list chain 4663, `univ4_hook`, and an ETH pairing whose currency is `0x0000000000000000000000000000000000000000`. A free live check of an explicitly ETH-paired hook request returned `judged: true`, `blockers: []`, and the fixed fact “Pool: paired with ETH, opening at a 10 ETH market cap.” Its fee-destination suggestion was advisory. The exact request and response are saved in [the preflight capture](../evidence/preflight/eth.json).

The third layer is an actual factory launch. **FACT:** transaction [0x296e…2544][TX832] has receipt status `0x1`, destination **`0xa25b02a1e93903b790e6aaf7da1b8b8d50294645`**, launch number **832**, and native-ETH `pairCurrency`. It was included in block **81870116**, **2026-10-06 19:16:01 UTC**, using **7,325,403 gas**. The [plane attestation][L832] separately records the ETH manifest and seven passed admission gates. These are stronger evidence than absence/presence in a small example list.

**FACT:** among the eleven live 4663 `univ4_hook` records in the inspected ledger, **832 is ETH-paired**; **784, 1015, 1033, 1194, 1205, 1300, 1316, 1327, 1330 and 1439 are IMD-paired**. The ledger covers dates back to 21 September, before the 4663 hook policy was introduced on 5 October. The runbook's three-launch sample omitted KING. This enumeration concerns the retrieved ledger, not every pool made outside IMD. [Index][INDEX], [saved launch attestations](../evidence/launches/).

**FACT — the current factories exist and answer their getters.** At Robinhood RPC block **87279516**, LaunchFactory and ProjectFactory both reported deployer `0xcecc29b037f5064fcdf45a5c318f132ef76aa551` and PoolManager `0x8366a39cc670b4001a1121b8f6a443a643e40951`. ProjectFactory's registry was `0xf52bbe066b7ad2d28c2195d066ea08dcbca88406`; LaunchFactory's distinct registry was `0x842e9bcff1e68566d45697a84f5b38c1c7766edb`. Use ProjectFactory's registry for BLACKOUT application proofs. Both runtimes were nonempty. [RPC capture](../evidence/rpc-factory.json), [IMD address documentation][DOCADDR].

**The request fields**

The transport action is **`launch.open`**. Its `input` must explicitly contain **`onchain: "univ4_hook"`, `chainId: 4663`, `pairWith: "eth"`**. A quote adds a fresh `requestKey` UUID outside `input`. The public preflight instead takes just `{action, input}`. The source-binding fields are `repoUrl` and `baseCommit` together; the commit must be 40 lowercase hex characters. `github: true` publishes the accepted source. For BLACKOUT M3, use **`economics: {poolBps: 7000, remainderTo: "<actual deployed escrow>"}`** outside the manifest. State the requester-approved token name and symbol explicitly in `objective`. [OpenAPI][OPENAPI], [job body][DOCBODY], [live check capture](../evidence/preflight/eth.json).

This is a field template, **not a submission-ready request**. The production escrow, approved name/symbol, and prepared commit must be supplied from the actual earlier steps; no address or identifier is invented here:

```json
{
  "action": "launch.open",
  "input": {
    "objective": "<approved M3 objective, with explicit token name and symbol>",
    "repoUrl": "https://github.com/identity-md-launches/launch-1269-reports-v1-job-b9e37680-814c-4f17-b4bc-6",
    "baseCommit": "<prepared, published 40-hex commit>",
    "shape": "chain",
    "steps": [
      {"skill": "audit-imported-code"},
      {"skill": "adapt-contract-project"},
      {"skill": "adversarial-review"}
    ],
    "onchain": "univ4_hook",
    "chainId": 4663,
    "pairWith": "eth",
    "economics": {"poolBps": 7000, "remainderTo": "<actual M2 escrow address>"},
    "github": true
  }
}
```

**FACT:** do not set `owner` on this hook request; that request field is restricted to `evm_project`/`evm_contracts`. A hook constructor's `$owner`, if used, resolves through the launch context, but BLACKOUT's V4Market has no owner parameter. Do not put `initialMarketCapWei` into hook economics: hook/project economics accept only pool share and remainder destination. Custom-token cap ranges in capabilities are **not** hook cap customization. [Delivery docs][DOCDELIVERY], [policy 30][POLICIES], [constructor validation code][WORKER].

**FACT — BLACKOUT's hook manifest should name** `V4Market` with constructor arguments, in order:

```text
$poolManager, $token, "12500", "60", $factory,
"0x9c9d2fcb75c2c132c0ac0c42df3819a42347265e",
<actual SwarmDesk address>, <approved GAME_CONFIG_HASH>
```

`$factory` here is **LaunchFactory**, the pool initializer; the literal ProjectFactory is separately needed for application proofs. The hook's callback permissions are **afterInitialize, beforeSwap, afterSwap, beforeSwapReturnDelta, afterSwapReturnDelta**, address bits **`0x10cc`**. The pool manifest currency is the native-ETH zero address, fee **12500**, spacing **60**. The zero address is the real V4 currency identifier, not a substituted owner or recipient. [V4Market source][MARKET], [fork fixture][FORK], [constructor validation][WORKER].

**FACT — policy and currency ordering explain the difference from IMD.** The newest 4663 hook policy is **version 30**, dated 6 October. It allows both currencies and maps their opening total-supply valuation to **10 ETH** or **2,500 IMD**. The supply is `1000000000000000000000000000` units (one billion, 18 decimals). The policy fee is **1.25%**, separate from the hook's application fee; **1% goes to the paying wallet and 0.25% to the network**. BLACKOUT's own post-launch 1% reward fee is additional. [Policy records][POLICIES], [live preflight](../evidence/preflight/eth.json), [runbook M3][RUNBOOK].

| Parameter | Native ETH pair | IMD pair |
| --- | --- | --- |
| Pair currency | Native ETH, address zero | `0x5f7bb59365ce557c26dbcaa4ee9d39a4b95b7127` |
| Opening total-supply market cap | **10 ETH**, `10000000000000000000` wei | **2,500 IMD**, `2500000000000000000000` minor units |
| Initial project-token price, calculated | `0.00000001 ETH` per token | `0.0000025 IMD` per token |
| Fee / spacing | **12500 / 60** | **12500 / 60** under current policy |
| Order | ETH is always currency0; project token is currency1 | Sorted by token address; project token can be currency0 or currency1 |
| Initial `sqrtPriceX96`, project token as currency1 | **792281625142643375935439503360000** (`10000 × 2^96`) | **50108289675009586237282760313922**, observed in 1316/1439 |
| Single-sided ticks, project token as currency1 | **−887220 to 184200**, observed in 832 | **−887220 to 128940**, observed in 1316/1439 |
| Single-sided ticks, project token as currency0 | Not applicable | **−128940 to 887220**, observed in 1330; its `sqrtPriceX96` is **125270724187523965593206900** |

Sources for policy rows: [policy 30][POLICIES]. Actual tick/price rows come from decoded **factory transaction calldata**, not the placeholder `pool.initialPrice` in many manifests: [832][TX832], [1316][TX1316], [1330][TX1330], [1439][TX1439]; [saved decodes](../evidence/decoded/). The recovered `launch(...)` ABI selector matches all these transactions: **`0xa7dd6d57`**. Factory source verification was not available; the ABI interpretation is supported by matching historical calldata and successful fork execution.

**MEASURED:** the ETH price corresponds to `log(100000000)/log(1.0001) ≈ 184216.02`, with the liquidity boundary rounded to spacing 60 at **184200**. The rehearsal comment's approximate tick “184206” is inaccurate, although its encoded price and range are correct. IMD with project token as currency1 gives approximately **128998.65**, boundary **128940**. Address-order inversion reverses the range. These are one-sided ranges around the launch price, not a symmetric full-range position. The deploy service chooses liquidity from the admitted pool share; callers should not copy the rehearsal's illustrative liquidity number. BLACKOUT's `poolBps: 7000` targets 70% of total supply in liquidity, with 10% reserved for swarm distribution and the 20% remainder plus unused liquidity dust sent to the actual escrow. The successful local factory test checked an escrow balance at least equal to the 200-million-token endowment.

**FACT/MEASURED — today’s BLACKOUT factory compatibility.** Locally rerunning the pinned repository's `RehearsalV311.t.sol` against RPC block **87279516**, with `FOUNDRY_VIA_IR=false FOUNDRY_BYTECODE_HASH=none`, passed **5 tests, 0 failures, 0 skips**. It exercised real factory bytecode for Desk, escrow, ETH token/hook, both eight-contract batches, code proofs, binding, escrow forwarding, endowment funding, oracle relay, fees and packs. [Original fixture][FORK], [local log](../evidence/rehearsal-current.log).

**Limit:** this impersonated the platform deployer on a local fork and used the fixture's public test configuration, test attester and mocked entropy clock. It did not run the paid plane, produce a production attestation, or broadcast. Its console “fork block” is Solidity `block.number` (an L1-number value on this Arbitrum chain); the independently selected RPC/L2 fork height is **87279516**. ETH acceptance is well evidenced; the actual BLACKOUT launch remains conditional on its source preparation, audit, manifest and deploy simulation.

**2. Admission, audit panel, manifest and deployment gates**

**FACT — the imported-contract path.** A launch from an existing Foundry repository starts with an **audit of the pinned imported code**, followed by **adaptation**, then independent tests, manifest generation, four specialist reviews and a judge. In recent imported Sherwood job **55bfb5c6-093b-4ab4-83ef-5ddb1a4c1cf3**, `audit_imported_code` preceded `adapt_contract_project`; tests, manifest and all four specialists depended on the adapter; the judge depended on **all seven** of those downstream/source nodes. New-source launches replace the import/adapter pair with the builder. A generic current contracts preflight displays the same tests/manifest/four-specialists/judge structure before deploy. [Sherwood job][J1389], [current contracts preflight](../evidence/preflight/contracts.json), [import audit reference][IMPORTREF].

| Stage / role | What is checked and how it participates | Blocking and retry meaning |
| --- | --- | --- |
| Public check / quote admission | Launch kind, chain/pair policy, complete request, public pinned source, required import-audit step, supported plan and build configuration | A `blockers` entry refuses admission independently of audit severity. Suggestions are advisory. Repair the request/source and check again before quoting. A check reserves no price. |
| Imported-code reviewer | Existing code's state-changing entry points, access, custody, accounting, arithmetic, external dependencies and platform incompatibilities | Its findings go to the adapter. Forbidden capabilities and incompatible deployment forms are reported, including medium findings. Import review acceptance is not clearance of those findings. |
| Builder / adapter | Factory-compatible nonpayable static constructors, exact ownership assignment, committed dependencies, buildable source and tests; adapter fixes reproduced import findings and records changes | Build/test/format/scope rejection needs a corrected attempt. These are pass/fail checks, not “low” or “medium” annotations. Configuration in an imported project is protected from adapter edits. |
| Independent tester | Unit/fuzz/invariant behavior, failure paths, privilege and custody guarantees; actual constructor/factory behavior | Tests can pass while the tester reports a defect. Tester findings are given to the judge just like specialist findings. Revised-source tests run again during fixes. |
| Manifest contributor (`integrate`) | Exact `launch.json` artifact selection, order, arguments, references and notes against accepted build | A malformed/incompatible manifest is a hard failure. This stage only writes `launch.json`; it does not repair source or send setup calls. |
| `audit_flow` specialist | Call sequence, state transitions, external-call order, reentrancy, terminal states and deployability | Read-only finding/coverage submission. The specialist does not itself decide final reopening. |
| `audit_permissions` specialist | Every authority, constructor privilege, caller authentication, custody/beneficiary access and external trust | Same mechanism. “Ownerless” still requires reviewing the contracts that hold authority. |
| `audit_economics` specialist | Distribution, pricing, incentives, exploit profitability, solvency and who can claim/lose funds | Same mechanism. This audit is distinct from the deploy gate named `economics`. |
| `audit_math` specialist | Accounting identities, rounding, overflow, bounds and proportional/time-dependent allocations | Same mechanism. Role scopes are reflected in the published findings; the supplied specialist reference requires concrete reproductions and coverage. |
| `audit_judge` | Reproduce specialists' and testers' claims; drop unproved claims; merge duplicates; recalibrate impact; independently review uncovered entry points and source/tests/manifest | **The judge's unresolved blocking findings control reopening and final launch clearance.** The observed launch threshold blocks **medium, high and critical**; **low/info annotate**. A deployment-model impossibility remains blocking until code is fixed, regardless of an author's answer. |

Sources: [current specialist reference][SPECIALISTREF], [judge reference][JUDGEREF], [adapter reference][ADAPTREF], [contracts recipe][CONTRACTSREF], [Sherwood published nodes][J1389], [BIC submissions][S1497]. Descriptions of specialist subject matter summarize their roles and observed reports; they are not claims that a finite panel proves every property.

**FACT — checks and analyzer reports are different evidence.** Accepted builder/test/manifest verdicts in BIC use profile `foundry`, evaluation `checks`, and report passing checks. The panel also considered static-analysis leads: its judge rejected an Aderyn reentrancy lead after tracing a STATICCALL plus a reentrancy guard. The specialist reference treats analyzer output as leads and requires matching source citations and concrete reproductions; an unmatched citation remains a note. The public records do not establish an additional universal formal-proof gate beyond the seven named admission gates. [BIC submissions][S1497], [specialist reference][SPECIALISTREF].

**FACT — constructors and the manifest.** `evm_contracts` has **1–8 unique application entries**, deployed **in order, atomically, in one factory transaction**. No platform token, distributor, pool or contributor-token reward is created. The current strict manifest has exactly:

```json
{
  "kind": "evm_contracts",
  "contracts": [
    {"contract": "<bare Solidity identifier>", "constructorArgs": ["<static words or supported references>"]}
  ],
  "notes": "<argument provenance, roles, behavior and limits>"
}
```

This schema illustration is not executable. Contract names are at most **32 ASCII identifier characters**; `MerkleDistributor` is reserved; notes are at most **4,000 characters**. Each contract has at most **16 constructor words**. The current recipe additionally supports signed integer words and flattened structs: `address`, sized `uint`/`int`, `bool` encoded `0/1`, `bytes32`, and structs of these flattened in declaration order. Negative integers use 32-byte two's complement. Dynamic bytes/string/array arguments and payable constructors are unsupported. This is more specific than the short public-doc summary of unsigned/static arguments. [Schema and ABI validator][WORKER], [current contracts reference][CONTRACTSREF].

Supported contracts-only references are **`$owner`** and **`$contract:EarlierName`**, resolving only address slots and only earlier manifest contracts. There is **no `$token`**, `$poolManager` or `$factory` placeholder in this manifest kind; external known addresses are literal constructor words. `$owner` uses the explicit request owner, otherwise the payer. It is unnecessary in an ownerless contract. The factory is `msg.sender` during construction; deriving owner from it traps control. Literal zero/burn/low/all-ones party addresses and IMD launch-wallet addresses are refused, with a native `Currency(0)` exception for real ETH. [Validator][WORKER], [contracts reference][CONTRACTSREF].

**FACT:** protected constructor rehearsal runs on an **empty chain**: external addresses are passed but have no code. Constructors must store/check their words without external calls or code-presence requirements; validate real dependencies on use. The factory sends **zero ETH** and executes **no post-deployment setup calls**. Runtime must be at most **24,576 bytes**, creation code **including constructor words** at most **49,152 bytes**. Proxies and runtime `DELEGATECALL`, `CALLCODE`, `SELFDESTRUCT` are prohibited. [Contracts reference][CONTRACTSREF], [judge deployability reference][JUDGEREF].

**The seven deploy admission gates**

**FACT:** all seven appear in BIC job **2d95a791-c71a-48e0-b7c4-68a6fda3273c**'s launch **1497**. That is an `evm_project`, so its token tests and reward allocation must not be mistaken for the contracts-only floor. The same gate names appear in `evm_contracts` launch **1389** and **1271**, with different protected-test/economics details. [BIC launch][L1497], [1389][L1389], [1271][L1271].

| Gate | Observed checks | What blocks; what medium/low means |
| --- | --- | --- |
| `provenance` | Accepted nodes and published source commit underpin the artifact being admitted; 1497 reports 8 accepted nodes at `8221822a`, 1389 reports 9 at `bd9dc1dd` | Missing/unaccepted provenance is a failed gate. No severity exception is evidenced. The public response does not expose every internal signature-validation branch. |
| `findings` | Accepted submissions have no unresolved blocking findings; final judge adjudication matters | **Unresolved medium/high/critical findings block in the observed launches. Low/info do not.** A specialist medium later downgraded/dropped by the judge is not an outstanding medium. An accepted final review can still contain a blocker and park the launch. |
| `independent_review` | A qualifying independent review is present; 1497/1389 each report 1; other published jobs report 5 | Missing independence/review clearance fails. Do not count the builder's self-review as this gate. Low/info findings can coexist with clearance; medium findings require adjudication/resolution as above. |
| `bytecode` | Signed/rebuilt artifact evidence is clean and reproducible; attestation records build settings, code/ABI hashes, byte lengths and forbidden-opcode flags | Nonreproducible/oversize/forbidden-bytecode failure is hard blocking, not a severity annotation. The contracts counted can include compiled dependencies beyond the one manifested deployment. |
| `manifest` | Manifest kind, artifact names/order, supported arguments/references, and policy-compatible configuration; hook launches also permission bits/pool parameters | Malformation, unsupported constructor or policy mismatch blocks regardless of a low prose finding. The 1497 detail names 1 project contract; 1389 names 1 application contract with no protocol token/pool. |
| `protected_invariants` | Platform-owned constructor/dependency/runtime/opcode floor, distinct from project tests. Contracts-only examples report **1** protected test; BIC/hook examples report **7** | Any failed protected test parks deployment irrespective of audit severity. Launch **867** passed other gates but failed `setUp(): application constructor failed`. BLACKOUT’s fork suite is not this protected harness. |
| `economics` | For contracts-only: policy explicitly selects **no on-chain contributor rewards**. For BIC: allocations and Merkle root were calculated | Missing/mismatched policy allocation blocks. No token share, pairing or liquidity obligation applies to `evm_contracts`. Economic application defects are judged by the audit panel, not waived by this gate's no-rewards result. |

Direct failure evidence: [867 constructor failure][L867], [1355 unresolved medium][L1355], [1423 factory-initialization failure][L1423]. The last is a hook example: protected initialization rejects a hook that refuses the factory's actual token/pair/fee/spacing. These are hard deployment checks even if an audit report has no high finding.

**FACT — after these gates, deployment still needs service clearance.** Current contracts documentation describes checking signed bytes/policy, **simulating the full factory transaction**, and enforcing the policy gas ceiling. Robinhood contracts-only policy **28** selects ProjectFactory `0x9c9d…265e`, no contributor rewards, and **`10000000000000000` wei (0.01 ETH)** maximum gas cost. The factory accepts only its configured deployer. Source publication, accepted job state, manifest acceptance, launch admission and successful on-chain inclusion are separate states. [Policy 28][POLICIES], [contracts reference][CONTRACTSREF], [factory RPC](../evidence/rpc-factory.json).

**Severity and retry evidence**

1. **Medium reopened and fixed:** ownerless MemecoinCemetery job **1d091aae-6d4d-4c64-959b-344d3865252c**, launch **876**. Its first judge reproduced a medium defect in capped holder reads, marked `blocking: true`, and was not accepted. The builder fixed it, tester/manifest ran again, and the judge settled it; launch then succeeded. Specialists retained their earlier reports. [Job][J876], [attempts][S876], [launch][L876].
2. **Medium annotated only after recalibration:** BIC specialist economics reported a **medium, blocking** collection-issuer dependency. Its judge verified the live dependency and judged the literal requested behavior a **low trust assumption** instead. The final judge had two lows and two infos, all nonblocking, and BIC deployed. This does **not** show unresolved medium findings are allowed. [BIC attempts][S1497], [launch][L1497].
3. **Two fix revisions, then parked:** Sherwood **1355** has `revisions: 2`, `judgeRevisions: 2` on adapter, tester, manifest and judge. Earlier judges were unaccepted with high defects; the final judge was accepted with a newly reproduced **medium, blocking** King-share defect. The job says `completed`, but launch says `parked`. A later separate corrected job **55bfb5c6…**, launch **1389**, deployed with five low and one info finding. [1355 job][J1355], [judge sequence][S1355], [1389 judge][S1389].
4. **Machine retry is a different counter:** BIC's manifest attempt 1 failed `internal_error`, `failureClass: machine`, summary “fetch failed”; attempt 2 was accepted, with **zero** fix/judge revisions. A machine retry did not require changing the economic design. [BIC submissions][S1497], [job][J1497].

**FACT:** the current judge reference says fix rounds rerun the author, tests and judge against changed code; **the four specialists do not rerun**. The judge confirms answers, rechecks changed lines and can discover new blockers. Deployment-model findings cannot be dismissed with a promise that the service will mine a salt or initialize later. [Judge reference][JUDGEREF].

**UNKNOWN:** the public endpoints inspected do not expose the complete server retry policy, universal maximum revision count, queue backoff, operator retry controls or deploy-transaction resubmission schedule. Two revisions are an observed exhausted case, not proof of a permanent global limit. The worker task schema limits an individual task's `attempt` field to 1–3, while published revision rounds can reset that counter. Do not equate it with three total audit rounds or promise automatic recovery of a parked launch. [Worker schema][WORKER], [1355 job][J1355]. A new source/payer-authorized launch request is evidenced by 1389; an ordinary project continuation is not an automatic redeployment instruction.

**3. Applying the pipeline to launch-v39.md M1, M2, M4 and M7**

**FACT — prepare the source before any of these paid launches.** The imported-source check without an explicit suitable plan initially returned `bad_path_count` for `impl` and `tests`. An explicit adapter step with additional `paths` returned `unplannable_steps` because that skill declares its own budget. Removing `paths` exposed the required initial import audit and the missing metadata setting. Adding `audit-imported-code` left **only the `bytecode_hash` blocker**. [Recorded preflight progression](../evidence/preflight/).

**INFERENCE — the concrete preparation needed:** publish a source-preparation commit with `bytecode_hash = "none"` and **`via_ir = false`** in the root Foundry profile, keeping solc **0.8.26**, Cancun and optimizer **200**. Build all contracts and tests under those settings and recheck every embedded pin. The latter compiler choice is necessary for the runbook's existing `*_LAUNCH` pins, not a universal current IMD rule: successful current attestations show both `viaIR: true` and `false`, and even different optimizer runs. [Current BLACKOUT config][CONFIG], [launch pins][PINS], [1316 attestation][L1316], [1439 attestation][L1439]. Asking the launch adapter to fix `foundry.toml` conflicts with the live check.

**MEASURED:** our override build reproduced **all fourteen `ModuleCode.launchHash` values**, plus:

| Artifact | Raw creation-code Keccak hash |
| --- | --- |
| GameRegistry | `0xee08039e9860c09d55aefe5cd2d9ffd5993f3fe60a1d606549902f56188418cb` |
| Params | `0x26c9f36af040b02eba9644f52daeed84fae4e42eab9bdb23277d0bb28c6dc6c0` |
| SwarmDesk | `0x9e0cf571a687b4e79948f2af5fd2095058226c11bd002342955d6022ddeda214` |
| EndowmentEscrow | `0xeeb7a2c17455a83fd04d6ab155c2c580720bd0d3c02d95a6bc0e9cd213491610` |
| V4Market | `0x758e2ab5a6db72b6c5192702ecb0fcb291101c599f91e1bbee1cc36091e3a974` |

[Build measurements](../evidence/blackout-build-summary.json), [SwarmCode pins][SWARMPINS], [ModuleCode pins][PINS]. These hash **creation bytecode without constructor words**. CREATE2 proofs additionally hash **creation bytecode plus encoded arguments**. Use the attestation's compiled-contract hashes for the former check; do not substitute an artifact/initcode hash or deployed-runtime hash. All 19 measured artifacts fit the individual creation/runtime size limits; this does not waive transaction simulation or protect against later adaptation changing bytes.

| Runbook item | Likely review/check issue | Assessment and action |
| --- | --- | --- |
| Ownerless contracts in all four jobs | Reviewer may look for trapped ownership or assume an owner is missing | **Not inherently blocked:** ownerless 876 and CharterClaim in 1497 deployed. Explicitly identify absence of owner/admin/upgrade/withdraw authority. Do not insert `$owner`, factory-as-owner, `tx.origin`, or a dummy owner. |
| M1 oracle-only SwarmDesk | Signer/endpoint trust, domain/question/window/quorum checks, replay/expiry, deferred execution and governance reach | **Review risk:** immutability is not absence of trust. Name the actual attester and immutable oracle configuration, bounded governance effects, signer-failure/liveness assumption and no recovery/rotation. No swarm EOA is needed; Desk is the authority contract. |
| M1 twelve constructor words | Treating the structs as ABI tuples/dynamic arrays, adding obsolete launch coordinates, passing thirteen or more values under a “twelve-word” claim | **Hard schema/constructor risk:** use exactly the encoder's ordered twelve static strings, with packed policy word and zero top 16 bits. The manifest maximum is 16, but exact ABI count/widths still apply. Binding coordinates are provided later, not constructor address stand-ins. |
| M2 escrow forward | Calling `forward` in deployment; accepting a predicted unfunded destination; confusing the two platform registries; twin-registry capture | **Hard deploy issue** if setup is required in the transaction; **security review risk** for twin capture. Constructor only stores the three actual addresses. Deployment must finish with `forwarded == false`; forwarding is a separate permissionless, authenticated operational call. |
| Pins in M1/M2/M4/M7 | Compiler/source changes make raw creation-code pins or CREATE2 proofs fail; same runtime does not establish the same constructor state | **Can permanently break wiring.** Freeze/reproduce the accepted source and compiler profile before bootstrap, check admitted hashes at each step, and stop on any mismatch. All hook/registry/Params/modules must use one matching build family. |
| M4 same-job dependencies | `$contract[0]` / `$contract[1]` are unsupported spellings | **Avoidable hard manifest failure:** write `$contract:Params`, `$contract:GameRegistry`. Named backward references are supported today; no reason to split Params merely for reference support. If a split is deliberately chosen, update every later recorded launch/index proof. |
| M4 and M7 eight contracts | Off-by-one index, ninth contract, top-level four-selector limit, single-transaction gas and bytecode size | **Eight is accepted by schema.** Omit the top-level `contracts` selector for eight entries; list exact names/order in objective and manifest. Distinguish manifest indices from game role numbers. Check every artifact and the full factory transaction. |
| M4 roots/snapshot and M1 game hash | Wrong chain for snapshot, wrong ABI hash, different roots at bootstrap and registry deployment, or guessed values | **Hard binding failure:** use actual approved roots and an Ethereum snapshot block; compute `keccak256(abi.encode(starterRoot, freeRoot, snapshotBlock, endowment))` consistently. No production values were supplied to this research; templates remain explicitly unfilled. |
| M4 → M5 secrecy mitigation | Public job objective reveals roots before Desk.bind | **Open medium/security risk:** the existing review documents a canonical-code twin front-run. A sentence asking for secrecy does not establish private transport or atomic binding. Immediate bind and checking Desk.registry before forwarding limit damage but do not eliminate the race. |
| M7 oracle-governed modules | “No admin” interpreted as “no restricted functions”; a builder substitutes an EOA or changes governance to obtain clearance | **Review risk:** restricted calls must remain authenticated to the actual Desk or registered modules. Explain oracle-derived, bounded game governance. Game asset issuance/permissions are application behavior, not creation of a second platform launch token. |

Primary BLACKOUT sources: [SwarmDesk][DESK], [escrow][ESCROW], [registry][REGISTRY], [Params][PARAMS], [GameModule constructor][GAMEMODULE], [independent v3.10 review][REVIEW], [runbook][RUNBOOK]. Severity predictions in this table are **inferences**; no new paid BLACKOUT audit verdict was generated.

**FACT — the twin issue cannot honestly be described as “closed.”** The published independent review rates it **medium, open by design**: a second canonical factory registry with the same token/hook/configuration can bind the Desk first, causing the escrow and hook to follow the twin. It expressly includes residual platform visibility of the job objective. The current public job API exposes full objectives; M4's own objective reveals the roots and snapshot before M5. The runbook's stop-before-forward check is necessary, but “keep private until bind” does not supply an on-chain discriminator for the honest job. [Review M-2][REVIEW], [public job schema][DOCJOBS]. **INFERENCE:** a judge could treat an explicitly accepted canonical-factory/platform trust assumption as advisory (BIC shows such recalibration), or keep this medium blocking. Neither wording nor an older contributor review guarantees acceptance. Removing the risk needs a reviewed design change or an evidenced private/atomic launch-and-bind facility; neither is established here.

**FACT/MEASURED — eight-contract gas headroom exists, but keep the service simulation.** Our fork reproduced factory-call gas **21,411,808** for job A and **19,523,888** for job B. At the pinned block base fee **20,038,000 wei/gas**, those call-only costs are approximately **0.00042905 ETH** and **0.00039122 ETH**. These calculations omit whole-transaction overhead; the local log records gas × base fee for each call. The live ArbGasInfo `getMaxTxGasLimit()` and `getMaxBlockGasLimit()` both returned **32,000,000**; `arbOSVersion()` returned **116**. [Local log](../evidence/rehearsal-current.log), [live limit reads](../evidence/rpc-gas-limits.json), [primary interface][ARBGAS]. **INFERENCE:** the measured call gas is below that ceiling and the 0.01 ETH policy cost ceiling at the observed low fee. Whole-transaction gas includes overhead/calldata and service margin; a Forge internal call is not the launch service's estimate. Do not turn this into a promise that eight-contract deployment can never be parked.

**Recommended objective text, after source preparation**

These are **recommendations**, not bypasses of audit or executable requests. Replace angle-bracket fields with actual requester-approved values and addresses returned by prior launch records. Use `action: launch.open`, `onchain: evm_contracts`, `chainId: 4663`, `repoUrl` and the prepared `baseCommit` for **each** job. Use the import-audit → adapter → independent-review steps above **without adding `paths` to skills that declare their own budget**. Omit `pairWith` and token economics for contracts-only jobs. The corrected current preflight still blocks the unprepared source, so no first-pass guarantee is claimed.

Common paragraph to include in each objective:

> Deploy only the named BLACKOUT application artifacts from <PREPARED_COMMIT>. Preserve the accepted contract behavior and its creation-code pins; do not silently substitute a different implementation to obtain admission. Compile with solc 0.8.26, optimizer 200, Cancun, viaIR false, bytecode_hash none. No new protocol token, distributor or pool. All deployment constructors are nonpayable static configuration, make no external calls, and need no dependency code on the empty-chain rehearsal. No privileged initializer, proxy, upgrade, factory ownership or broadcast by a contributor. The manifest contributor writes only launch.json. Publish the admitted source/toolchain/creation-code hashes and return the confirmed launch number, ordered artifact names/indices, addresses, transaction hash and block. If adaptation changes any pinned creation code or defeats a proof, stop for source correction and repeat validation before deploy.

**M1 — SwarmDesk**

> Deploy exactly one SwarmDesk. It has no owner, admin EOA, arbitrary-call path, withdrawal or upgrade. Its only governance authority derives from authenticated IMD oracle answers, with immutable endpoints/attester and bounded execution. Use the twelve static constructor strings in this exact order: intake, delivery, signer, asset, action, packed policyWord, eventQuestion, regulatorQuestion, eventBody, regulatorBody, ProjectFactory, GAME_CONFIG_HASH. Attach the output of tools/swarm_constructor_args.mjs from docs/oracle-v37/oracle-config.json and the approved binding data; do not reconstruct a tuple or append launch coordinates. GAME_CONFIG_HASH is <APPROVED_HASH>, heartbeat 200 bps, fixed cap 1e18. Deploy unbound. Review the EIP-712 domain, question/body commitments, expiry/quorum/replay checks, failure callback and deferred execution. Document immutable-signer availability risk and the existing same-config twin-binding risk. Permissionless authenticated bind is a later operational action; no owner setter or recovery key may be added. Return oracleConfig(), bindingConfig() and registry() checks.

The exact words are enumerated in source/encoder, not an inferred flattening. `policyWord` packs questionChain bits 0–31, fromBlock 32–79, toBlock 80–127, maxPrice 128–223 and heartbeatBps 224–239. Top 16 bits must be zero. The runbook's binding-file zero coordinates are **unused uint fields**, not zero owner addresses. [Encoder][ENCODER], [Desk constructor][DESK].

**M2 — EndowmentEscrow**

> Deploy exactly one EndowmentEscrow with constructorArgs ["0x9c9d2fcb75c2c132c0ac0c42df3819a42347265e", "0xf52bbe066b7ad2d28c2195d066ea08dcbca88406", "<CONFIRMED_M1_DESK>"]. This ownerless immutable escrow has no beneficiary setter, caller payout or discretionary withdrawal. Its one-time permissionless forward proves the Desk-bound registry and RewardPool through recorded factory launches, exact pinned creation code plus constructor words, and CREATE2 predictions; it sets forwarded before transferring the entire canonical-token balance. It is the future token launch's remainderTo, not a guessed CREATE2 address. Do not forward, fund or initialize in this deployment. Return factory(), records(), desk(), and forwarded()==false. Preserve/document the same-config twin risk; later forwarding must be withheld unless Desk.registry() equals the recorded job A registry.

**M4 — job A, exactly eight contracts**

> Deploy these eight artifacts in this exact order: [0] Params(<CONFIRMED_DESK>, "200", "1000000000000000000"); [1] GameRegistry(<CONFIRMED_TOKEN>, $contract:Params, <CONFIRMED_HOOK>, <APPROVED_STARTER_ROOT>, <APPROVED_FREE_ROOT>, <APPROVED_ETHEREUM_SNAPSHOT_BLOCK>, "200000000000000000000000000", "0x9c9d2fcb75c2c132c0ac0c42df3819a42347265e"); [2] RewardPool($contract:GameRegistry); [3] FarmRewards($contract:GameRegistry); [4] FarmCore($contract:GameRegistry); [5] FarmItems($contract:GameRegistry); [6] PackSale($contract:GameRegistry); [7] StarterClaim($contract:GameRegistry). Use named backward references exactly; no $contract[index], $token placeholder, extra token, owner or ninth artifact. Roots/snapshot/endowment must reproduce M1's configuration hash. Preserve Desk-only bounded governance and the game's specified asset permissions. Verify raw creation hashes against SwarmCode.REGISTRY_LAUNCH, PARAMS_LAUNCH and ModuleCode.launchHash(0..5). Record manifest indices separately from module roles. Binding and role registration are later permissionless proof calls; do not claim the game is fully wired at deployment. Expose the twin-binding trust assumption to the judge and return checks needed to verify immediate bind before any escrow forwarding.

**M7 — job B, exactly eight contracts**

> Deploy [0] FeeRouter, [1] GridOperator, [2] Season, [3] FarmEngine, [4] Economy, [5] Enhancement, [6] Civic, [7] Billboards, each with exactly one constructorArg "<CONFIRMED_JOB_A_REGISTRY>". This is an actual recorded GameRegistry address, not a prediction or placeholder to resolve after deployment. No new protocol token, owner, upgrade or ninth artifact. Preserve registered-module access and oracle-only, bounded Desk governance; no swarm EOA or arbitrary privileged initializer. Verify raw creation hashes against ModuleCode.launchHash(6..13) and simulate the whole eight-contract factory transaction under the current chain gas and 0.01 ETH policy ceilings. Return launch number, every artifact index/address/hash and the registry checks. Register roles 6–13 and bind FeeRouter later through their existing permissionless proofs; do not perform those operations in this deployment.

If M7 is combined with a website workflow, its contracts draft must retain `evm_contracts` and chain 4663; build the website from the confirmed handoff only after deployment. This research does not recommend conflating the later forwarding/funding/wiring calls with factory construction. [Workflow docs][DOCWORKFLOW], [contracts reference][CONTRACTSREF].

**4. Last-week wall time: posting → deployed**

**Method:** fix the rolling window to **2026-10-06 05:43:42.371 UTC through 2026-10-13 05:43:42.371 UTC** (the research job's posting instant). Filter recorded 4663 `evm_contracts` launches whose deployment was included during that week. Count **manifest application entries**, not every contract created inside a wrapper constructor or every compiled contract in the attestation. Start at the associated job's **`createdAt`**; end at the **successful receipt's block timestamp**. Do not start at launch-record `createdAt` (which usually occurs after building/auditing/publication), or end at explorer verification. The inspected 500-record ledger extends back to 21 September, so it covers the whole window. All 18 successful cohort receipts were retrieved, matched to block hashes and had status `0x1`. [Index][INDEX], [job snapshots](../evidence/jobs/), [RPC receipts/blocks](../evidence/chain/).

| Cohort | Observed result |
| --- | --- |
| **1 manifested application contract** | **n = 17**; median **63.3 min**; mean **79.0 min**; middle 50% **49.9–103.0 min**; range **28.4–213.4 min** |
| **8 manifested application contracts** | **n = 0**; typical wall time **unanswered** |
| Other multi-contract evidence | One **3-contract** launch, Swarmopoly **895**, took **101.8 min**; it is not an eight-contract sample |
| Source-publication/launch-record creation → inclusion, 1-contract cohort | Median **43.3 seconds**, range **12.6–158.5 seconds**; this is only the final service interval, not the user wait |

The quantile convention is inclusive linear interpolation. Statistics include successful jobs that needed repairs; they exclude three parked launches (**867, 1003, 1355**) with no deployment. This introduces survivor bias and is not a service SLA. Failed paid jobs that never reached a launch record are also not a deployment-time sample. **INFERENCE:** a one-contract launch should be budgeted in roughly hour-scale wall time with meaningful tail risk; there is no evidence to multiply that median by eight or assume an eight-contract job finishes equally quickly. The fresh BLACKOUT fork's elapsed seconds measure test execution, not contributor queue/build/audit latency.

Each row below links the full job ID and full transaction hash. Full timestamps and recomputable values are in [timing.json](../evidence/timing.json).

| Launch / applications | Posted UTC | Included UTC | Wall minutes | Job | Transaction |
| --- | --- | --- | --- | --- | --- |
| [782](https://api.imd.fun/launches/9be02b21-38b2-40b4-ae03-acefa2b11a75) / 1 | 10-06 05:20:39 | 10-06 05:50:55 | 30.3 | [05e49fa8](https://api.imd.fun/jobs/05e49fa8-b419-4c89-a9da-2b496a4dce9b) | [0x2d0d9251…](https://robin.etherscan.io/tx/0x2d0d92518cd6f258640dd64481979b11b35dc1079a6b7af1cc6ae6ecb99032eb) |
| [865](https://api.imd.fun/launches/f07b819d-429e-42c4-9226-eb7d20598e88) / 1 | 10-07 01:46:17 | 10-07 02:42:27 | 56.2 | [75b59a69](https://api.imd.fun/jobs/75b59a69-3f1b-40be-a42a-1343aa91d720) | [0x1c22d2cf…](https://robin.etherscan.io/tx/0x1c22d2cf5eda9956290e78eaa66431de7a99943a1be1ffe0115ef76031de2fc2) |
| [871](https://api.imd.fun/launches/01f59db4-993d-4a9d-866b-0440bd4a8a57) / 1 | 10-07 03:14:49 | 10-07 04:03:41 | 48.9 | [7b2d14d8](https://api.imd.fun/jobs/7b2d14d8-1923-4948-8a33-c8d85b741b2b) | [0xcdaf34c7…](https://robin.etherscan.io/tx/0xcdaf34c74db78e5104257bae26b928b2faf9c431235bb52d424cbabbd9d9d844) |
| [876](https://api.imd.fun/launches/d8c63be3-7e5f-449c-8dcd-466c099a97ea) / 1 | 10-07 05:11:33 | 10-07 06:14:52 | 63.3 | [1d091aae](https://api.imd.fun/jobs/1d091aae-6d4d-4c64-959b-344d3865252c) | [0x3377d54a…](https://robin.etherscan.io/tx/0x3377d54a841b93c78fa0f5a1e5f0cfd1f564739a3782145508d6c0cbe327a977) |
| [877](https://api.imd.fun/launches/10aca822-5003-4a53-89b2-f15f770befcb) / 1 | 10-07 05:16:08 | 10-07 06:23:31 | 67.4 | [9d7bffba](https://api.imd.fun/jobs/9d7bffba-141b-4e33-be9c-1bfa450d9384) | [0xfa90aa2b…](https://robin.etherscan.io/tx/0xfa90aa2b987ccb79374dbe1d07281be3377e8ad953de5183dceceeb759b8e90e) |
| [895](https://api.imd.fun/launches/40d9a21c-58b4-47c8-9e1c-3c761c2df5d5) / 3 | 10-07 10:15:31 | 10-07 11:57:18 | 101.8 | [ee10bd28](https://api.imd.fun/jobs/ee10bd28-8e70-4175-89b2-445a5e137bb3) | [0x5a419eb4…](https://robin.etherscan.io/tx/0x5a419eb4f115d8d127699683b406e9110f74f2579a8ee87d41ee9d9b0f715aa9) |
| [929](https://api.imd.fun/launches/2e9599ee-8024-49a7-8b56-e4086d608660) / 1 | 10-07 17:30:06 | 10-07 19:10:44 | 100.6 | [c7efa792](https://api.imd.fun/jobs/c7efa792-d9f8-403d-9157-d7d1660f2b24) | [0xb9f5d0d4…](https://robin.etherscan.io/tx/0xb9f5d0d499083dea6d7ba21252942974117962793eb938e9365b634fe2a59422) |
| [976](https://api.imd.fun/launches/658f7cfd-362d-4538-bf33-66b861fda7b0) / 1 | 10-08 02:14:17 | 10-08 02:42:39 | 28.4 | [17cab89e](https://api.imd.fun/jobs/17cab89e-bd76-4a9c-8661-e60b73815177) | [0x720bdb86…](https://robin.etherscan.io/tx/0x720bdb86f1a7605b00f3d2922f4369f38c269947a7d400606f830cbcaba10c85) |
| [978](https://api.imd.fun/launches/ab6fcb3d-8ce1-4a37-a4b4-8e773faefc28) / 1 | 10-08 02:26:49 | 10-08 06:00:14 | 213.4 | [5a737f9c](https://api.imd.fun/jobs/5a737f9c-132f-4bbd-a556-4510d4dcce14) | [0x659bb9d3…](https://robin.etherscan.io/tx/0x659bb9d371f8e17202954966c3dcf013de92450c6a421bbc62290b8b037a037c) |
| [985](https://api.imd.fun/launches/9a99a61b-ab97-426f-a272-213f779caa66) / 1 | 10-08 02:49:21 | 10-08 04:44:51 | 115.5 | [8a4b3bd0](https://api.imd.fun/jobs/8a4b3bd0-acf4-422f-9f68-d02d4d7978ae) | [0x35226356…](https://robin.etherscan.io/tx/0x35226356614019413bf16a034133fe4835c7dc0d73686ae18860719d5e402e1f) |
| [1020](https://api.imd.fun/launches/82ce62fe-faaf-4b79-a83f-942e180f7869) / 1 | 10-08 06:54:34 | 10-08 08:50:52 | 116.3 | [b8fd4c2b](https://api.imd.fun/jobs/b8fd4c2b-e0a5-48bd-951f-222b3f3a342c) | [0xf5de5142…](https://robin.etherscan.io/tx/0xf5de51420b6f784fcd81d4591e6ada052f280b3d142990dba5651cf8fd7da69e) |
| [1026](https://api.imd.fun/launches/d4b2fa5c-e280-46a6-96bc-7ff761b705d4) / 1 | 10-08 08:11:42 | 10-08 09:08:40 | 57.0 | [f0191de7](https://api.imd.fun/jobs/f0191de7-47dd-4658-8578-1f6f236538e4) | [0x392fc261…](https://robin.etherscan.io/tx/0x392fc26145b0a21f343f7b8c5cbf758f6bb04bec0459cdbb71dda38877264d06) |
| [1053](https://api.imd.fun/launches/e32a4dc9-053a-4c9f-ae3e-9feb138f72bc) / 1 | 10-08 14:16:03 | 10-08 14:55:27 | 39.4 | [3bfde4f8](https://api.imd.fun/jobs/3bfde4f8-74f7-4afd-b9c0-a0bdba9bac42) | [0xc99f49bb…](https://robin.etherscan.io/tx/0xc99f49bbc8c99169f4f15f47a52ee8d4acf888a913bd37bce941f907d452ba6c) |
| [1103](https://api.imd.fun/launches/e61c8e5f-a0ec-45a9-a426-bf7653dd71c6) / 1 | 10-08 22:50:15 | 10-08 23:40:08 | 49.9 | [c20f9b8b](https://api.imd.fun/jobs/c20f9b8b-afa2-45f5-abc8-bba3f87f5c47) | [0x2f6a9982…](https://robin.etherscan.io/tx/0x2f6a9982fcc38953a61a63e3101ff8dffcc4eb987989d7cb10e686fd0cdc0119) |
| [1109](https://api.imd.fun/launches/20da95ee-f66e-48ad-9eca-45ada790f19f) / 1 | 10-08 23:41:52 | 10-09 00:37:40 | 55.8 | [c0881060](https://api.imd.fun/jobs/c0881060-b5e0-4c0d-8dfb-dab81470c3e8) | [0x8739c5d3…](https://robin.etherscan.io/tx/0x8739c5d39491290adfbb6dd47451954d850b620d5070a45d08c1427f216df190) |
| [1110](https://api.imd.fun/launches/4715417b-5084-4050-8fb7-1d23050581ce) / 1 | 10-08 23:46:54 | 10-09 00:56:30 | 69.6 | [4ff210c0](https://api.imd.fun/jobs/4ff210c0-6868-42fb-b90e-23a06e676b0f) | [0xb5d76fd1…](https://robin.etherscan.io/tx/0xb5d76fd12eda0829ffc4c73b68a390e44945a176e21b8325b436e374b87c8fca) |
| [1271](https://api.imd.fun/launches/848ec41a-4641-42bc-b2e8-0c1426b49d8e) / 1 | 10-10 21:06:16 | 10-10 22:49:18 | 103.0 | [e63e94be](https://api.imd.fun/jobs/e63e94be-2e3d-4e5a-bf03-30d4c4c3cf03) | [0xcc510b0b…](https://robin.etherscan.io/tx/0xcc510b0b420b4968c06a85fb079da76fb416dfeaf51a68a6679bacdac4bdfaeb) |
| [1389](https://api.imd.fun/launches/50787239-e9b1-4891-b169-e0f0d38a850e) / 1 | 10-12 08:40:27 | 10-12 10:48:33 | 128.1 | [55bfb5c6](https://api.imd.fun/jobs/55bfb5c6-093b-4ab4-83ef-5ddb1a4c1cf3) | [0x8e328a10…](https://robin.etherscan.io/tx/0x8e328a10fb218f689e89d4f207c43700243b223fd733382e27b3ca0575da1d1b) |

**5. What remains uncertain, and verification limits**

- **Production source readiness:** the pinned BLACKOUT tree is demonstrably blocked by the metadata configuration today. A prepared published commit and its new admitted hashes do not yet exist in this report. Changing compiler settings must be followed by pin and test checks before bootstrap; changing actual contract behavior requires reviewing the entire binding chain.
- **Twin capture acceptance:** the medium design issue remains open. Public objective exposure weakens the secrecy mitigation. No private admission channel or atomic deploy-and-bind service was established. The final panel may keep it blocking; a promise of “first time pass” would be unsupported.
- **Eight-contract timing:** no completed eight-entry `evm_contracts` launch on 4663 was found in the last-week cohort. A successful local eight-contract fork test is deployment compatibility evidence, not an observed production latency sample.
- **Admission internals:** public gate details and published reports establish observed behavior. The plane's complete private implementation, exhaustive severity exceptions, retry/backoff policy and all signature-verification branches were not available. This report does not invent them.
- **Oracle-only liveness:** no owner key is missing from this design, but immutable attester/endpoints and off-chain schedules remain trust/availability dependencies. No fresh audit of their production service guarantees was performed.
- **Factory source verification:** explorer retrieval was unavailable for factory source; bytecode/getters, matching recovered selectors, historical receipts and fork execution support the claims. This is not a full audit of the factory.
- **Branding/site:** the supplied X account and `playblackout.xyz` identify the requested project. The site could not be retrieved through the web reader; no claim about current site functionality, project control of an address, or complete BLACKOUT deployment is inferred from its branding. A separate recorded custom-token launch **1338** exists, but it is not evidence that this runbook's Desk/escrow/modules were deployed or that a new `univ4_hook` job reuses that token. [1338 record][L1338].

**Local validation performed:** primary response capture; factory transaction selector and static-field decoding; successful receipt/block/chain matching; offline duration/statistic recalculation; creation-code/size/constructor measurement; all sixteen embedded launch pins checked; and the five-test current-state fork rehearsal. The delivered evidence manifest records hashes and whether each file is an excerpt or derived result. `python3 verify_report.py` validates the saved evidence and calculations offline. These checks are this contributor's own work, carry no independent review authority, and do not certify the truth of every upstream claim or grant deployment approval.

[CAPS]: https://api.imd.fun/requests/capabilities
[POLICIES]: https://api.imd.fun/launch/policies
[OPENAPI]: https://api.imd.fun/openapi.json
[INDEX]: https://api.imd.fun/launches?limit=500
[DOCDELIVERY]: https://imd.fun/docs/#delivery
[DOCBODY]: https://imd.fun/docs/#job-body
[DOCADDR]: https://imd.fun/docs/#contract-addresses
[DOCJOBS]: https://imd.fun/docs/#jobs
[DOCWORKFLOW]: https://imd.fun/docs/#workflow-body
[WORKER]: https://github.com/Identity-md/worker/blob/aeb60bd233ccd47ea1cba32babed8fcf7681fefd/dist/cli.js
[CONTRACTSREF]: https://api.imd.fun/reads/skill/evm-contracts-launch
[IMPORTREF]: https://api.imd.fun/reads/skill/audit-imported-code
[ADAPTREF]: https://api.imd.fun/reads/skill/adapt-contract-project
[SPECIALISTREF]: https://api.imd.fun/reads/skill/audit-specialist
[JUDGEREF]: https://api.imd.fun/reads/skill/audit-judge
[ARBGAS]: https://github.com/OffchainLabs/nitro-precompile-interfaces/blob/main/ArbGasInfo.sol
[JREHEARSAL]: https://api.imd.fun/jobs/2f166600-ba14-4659-9409-a70218d2e97e
[J1497]: https://api.imd.fun/jobs/2d95a791-c71a-48e0-b7c4-68a6fda3273c
[J1389]: https://api.imd.fun/jobs/55bfb5c6-093b-4ab4-83ef-5ddb1a4c1cf3
[J1355]: https://api.imd.fun/jobs/0f874eef-fadd-41fd-aab5-bf3ff4c420d4
[J876]: https://api.imd.fun/jobs/1d091aae-6d4d-4c64-959b-344d3865252c
[S1497]: https://api.imd.fun/jobs/2d95a791-c71a-48e0-b7c4-68a6fda3273c/submissions
[S1355]: https://api.imd.fun/jobs/0f874eef-fadd-41fd-aab5-bf3ff4c420d4/submissions
[S1389]: https://api.imd.fun/jobs/55bfb5c6-093b-4ab4-83ef-5ddb1a4c1cf3/submissions
[S876]: https://api.imd.fun/jobs/1d091aae-6d4d-4c64-959b-344d3865252c/submissions
[L832]: https://api.imd.fun/launches/4154320f-384b-46d9-b178-81b32f838dbb
[L876]: https://api.imd.fun/launches/d8c63be3-7e5f-449c-8dcd-466c099a97ea
[L867]: https://api.imd.fun/launches/43144ec9-c383-41b7-baf4-dbb5e3a2ed91
[L1271]: https://api.imd.fun/launches/848ec41a-4641-42bc-b2e8-0c1426b49d8e
[L1316]: https://api.imd.fun/launches/1ed280f5-02e0-4d77-83a2-1917bad1a061
[L1338]: https://api.imd.fun/launches/e614678d-8ac3-49f8-9922-cd662be4120f
[L1355]: https://api.imd.fun/launches/fcaf211f-83b5-4e3c-aede-7cd3941658b0
[L1389]: https://api.imd.fun/launches/50787239-e9b1-4891-b169-e0f0d38a850e
[L1423]: https://api.imd.fun/launches/bbfc7d94-12bf-4c12-8063-06e35c2d721d
[L1439]: https://api.imd.fun/launches/625e2dfc-895d-4af4-b987-85670c4509cc
[L1497]: https://api.imd.fun/launches/056c617a-2c6b-457d-8fb1-9e0d8a4c9469
[TX832]: https://robin.etherscan.io/tx/0x296e1cc73b3b899128f22c7b92f20cbebeaec216a4d01ce01f5d9a353f012544
[TX1316]: https://robin.etherscan.io/tx/0x22206fe6de8ae281bbf9f4e51ade224365cbfff770cb1ff57fa5159098a76c53
[TX1330]: https://robin.etherscan.io/tx/0x1fc60dcc43a3f0418578716e2cd09eb52bdf93061bc2c6a15231ff950b165ef6
[TX1439]: https://robin.etherscan.io/tx/0xe636c70a1405e486adb8cec2cafe4eaa1c809a63eafe0bb5ce2d738690129cd6
[RUNBOOK]: https://github.com/identity-md-launches/launch-1269-reports-v1-job-b9e37680-814c-4f17-b4bc-6/blob/8cd615252481e025cca0b225437056467ddf5405/launch-v39.md
[CONFIG]: https://github.com/identity-md-launches/launch-1269-reports-v1-job-b9e37680-814c-4f17-b4bc-6/blob/8cd615252481e025cca0b225437056467ddf5405/foundry.toml
[PINS]: https://github.com/identity-md-launches/launch-1269-reports-v1-job-b9e37680-814c-4f17-b4bc-6/blob/8cd615252481e025cca0b225437056467ddf5405/src/lib/ModuleCode.sol
[SWARMPINS]: https://github.com/identity-md-launches/launch-1269-reports-v1-job-b9e37680-814c-4f17-b4bc-6/blob/8cd615252481e025cca0b225437056467ddf5405/src/lib/SwarmCode.sol
[DESK]: https://github.com/identity-md-launches/launch-1269-reports-v1-job-b9e37680-814c-4f17-b4bc-6/blob/8cd615252481e025cca0b225437056467ddf5405/src/SwarmDesk.sol
[ESCROW]: https://github.com/identity-md-launches/launch-1269-reports-v1-job-b9e37680-814c-4f17-b4bc-6/blob/8cd615252481e025cca0b225437056467ddf5405/src/EndowmentEscrow.sol
[REGISTRY]: https://github.com/identity-md-launches/launch-1269-reports-v1-job-b9e37680-814c-4f17-b4bc-6/blob/8cd615252481e025cca0b225437056467ddf5405/src/GameRegistry.sol
[PARAMS]: https://github.com/identity-md-launches/launch-1269-reports-v1-job-b9e37680-814c-4f17-b4bc-6/blob/8cd615252481e025cca0b225437056467ddf5405/src/Params.sol
[GAMEMODULE]: https://github.com/identity-md-launches/launch-1269-reports-v1-job-b9e37680-814c-4f17-b4bc-6/blob/8cd615252481e025cca0b225437056467ddf5405/src/lib/GameModule.sol
[MARKET]: https://github.com/identity-md-launches/launch-1269-reports-v1-job-b9e37680-814c-4f17-b4bc-6/blob/8cd615252481e025cca0b225437056467ddf5405/src/V4Market.sol
[ENCODER]: https://github.com/identity-md-launches/launch-1269-reports-v1-job-b9e37680-814c-4f17-b4bc-6/blob/8cd615252481e025cca0b225437056467ddf5405/tools/swarm_constructor_args.mjs
[FORK]: https://github.com/identity-md-launches/launch-1269-reports-v1-job-b9e37680-814c-4f17-b4bc-6/blob/8cd615252481e025cca0b225437056467ddf5405/test/fork/RehearsalV311.t.sol
[REVIEW]: https://github.com/identity-md-launches/launch-1269-reports-v1-job-b9e37680-814c-4f17-b4bc-6/blob/8cd615252481e025cca0b225437056467ddf5405/docs/review-v39-independent.md
