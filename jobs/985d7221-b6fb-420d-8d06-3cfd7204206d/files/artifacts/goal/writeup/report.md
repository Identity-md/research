| Key / check source | Question as asked: original unavailable; reconstruction below | Attested answer recorded in notes | Check answer | Recheck | Match | Oracle request id | Attestation digest |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| [weth-dep](#source-c01) | How many Deposit(address indexed dst, uint256 wad) events did WETH9 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 emit on Ethereum mainnet over blocks 26371056 through 26372855 inclusive? | 10974 | 10974 | None | Yes, exact numeric equality | `c302bd0f-fd8e-47fd-ae30-f104169227ba` | Not supplied |
| [weth-wd](#source-c02) | How many Withdrawal(address indexed src, uint256 wad) events did WETH9 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 emit on Ethereum mainnet over blocks 26371056 through 26372855 inclusive? | 14110 | 14110 | None | Yes, exact numeric equality | `3119e343-9f63-4d1d-b25b-d57fad8cef7a` | Not supplied |
| [weth-dep-sum](#source-c03) | What is the sum of wad, in wei, over all Deposit(address indexed dst, uint256 wad) events emitted by WETH9 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 on Ethereum mainnet over blocks 26371056 through 26372855 inclusive? | 16113541637114718147661 | 16113541637114718147661 | None | Yes, exact numeric equality | `bf3bb13c-b920-452a-b5c4-34ab00966ccf` | Not supplied |
| [weth-wd-sum](#source-c04) | What is the sum of wad, in wei, over all Withdrawal(address indexed src, uint256 wad) events emitted by WETH9 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 on Ethereum mainnet over blocks 26371056 through 26372855 inclusive? | 13712073409150491261489 | 13712073409150491261489 | None | Yes, exact numeric equality | `2df84d42-8197-479e-86f7-788ef0f477e6` | Not supplied |
| [usdc-mint](#source-c05) | How many Transfer(address indexed from, address indexed to, uint256 value) events with from equal to the zero address 0x0000000000000000000000000000000000000000 did USDC 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 emit on Ethereum mainnet over blocks 26371056 through 26372855 inclusive? | 1092 | 1092 | None | Yes, exact numeric equality | `3769f644-e2e2-4580-9afd-c03e621ef822` | Not supplied |
| [usdc-mint-sum](#source-c06) | What is the sum of value, in base units, over all Transfer(address indexed from, address indexed to, uint256 value) events with from equal to the zero address 0x0000000000000000000000000000000000000000 emitted by USDC 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 on Ethereum mainnet over blocks 26371056 through 26372855 inclusive? | 39818447682674 | 39818447682674 | None | Yes, exact numeric equality | `db11d205-733c-4e43-956a-5872f51ee43e` | Not supplied |
| [usdc-burn](#source-c07) | How many Transfer(address indexed from, address indexed to, uint256 value) events with to equal to the zero address 0x0000000000000000000000000000000000000000 did USDC 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 emit on Ethereum mainnet over blocks 26371056 through 26372855 inclusive? | 588 | 588 | None | Yes, exact numeric equality | `66e5a15b-422b-426a-b08f-ed98ae6e31fc` | Not supplied |
| [v4-init](#source-c08) | How many Initialize(bytes32 indexed id, address indexed currency0, address indexed currency1, uint24 fee, int24 tickSpacing, address hooks, uint160 sqrtPriceX96, int24 tick) events did Uniswap v4 PoolManager 0x000000000004444c5dc75cB358380D2e3dE08A90 emit on Ethereum mainnet over blocks 26371056 through 26372855 inclusive? | 94 | 94 | None | Yes, exact numeric equality | `8ea897e6-6fbb-4d38-bc98-5c47cda9aec6` | Not supplied |
| [v2-pairs](#source-c09) | How many PairCreated(address indexed token0, address indexed token1, address pair, uint256) events did Uniswap V2 factory 0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f emit on Ethereum mainnet over blocks 26371056 through 26372855 inclusive? | 31 | 31 | None | Yes, exact numeric equality | `b969ac4a-fcde-4e65-bea4-6dfbf1de5f81` | Not supplied |
| [beacon-dep](#source-c10) | How many DepositEvent(bytes pubkey, bytes withdrawal_credentials, bytes amount, bytes signature, bytes index) events did the beacon deposit contract 0x00000000219ab540356cBB839Cbe05303d7705Fa emit on Ethereum mainnet over blocks 26371056 through 26372855 inclusive? | 100 | 100 | None | Yes, exact numeric equality | `49e95f37-77c4-4c91-b6ae-e77512b97fa9` | Not supplied |

All ten oracle values recorded as attested in the episode notes equal the corresponding handed check answers. No mismatch triggered a recheck. This conclusion compares preserved records; it does not independently authenticate an oracle signature or reproduce the Ethereum logs during write-up. The oracle values and request ids above come from [G, episodes 3–5](#source-g); each check value comes from the linked item result.

The handoff does not preserve the original question strings or the plane-added goal prefix. The questions above reconstruct the requested semantics from the objective and episode-one notes, with the complete address, event signature, filter, units and window. They are **not verbatim transcripts**. The handoff also contains no raw `asks`, `ask.answered` payloads, signed attestations or attestation digests. “Not supplied” means missing evidence in this handoff, not an unattested request. A request id, closing block hash or result-file hash cannot substitute for an attestation digest. Exact wording and digest verification remain unavailable. [G](#source-g)

All questions were submitted with `chainId: 1`, `window: {"fromBlock":26371056,"toBlock":26372855}`, `evidence: "chain"`, `panelSize: 7` and `answerType: "uint256"`, according to episode one. Episodes three and four record quorum 5, agreement by 5 or 6 panel members, signer `0x5598aa9146215bc13eb26f2c692ad1461fd32982`, and closing block hash `0xb6445349bd38ce220816a3fc7818e52630fccb5c39c87a21e4ec982fe23d5a82`. Those notes describe the figures as deployer-reproduced. The signer and block hash are preserved metadata; the signed payload needed to verify them was not handed over. The WETH sums are in wei; the USDC sum is in base units; all other answers count matching event logs. [G, episodes 1, 3–5](#source-g)

No ask was recorded as refused or as ending unattested. Accordingly, there are no refusal reasons to enumerate and no wording-fix retries. The current `refused` array is empty, and episode five records all requests as answered/attested, no re-asks, and no pending effects. This status history is available through the notes, rather than through individual terminal ask objects in the write-up snapshot. The source flag on `check/weth-wd`, discussed below, is not an oracle refusal. [G](#source-g)

The requested duration from episode one to each attestation cannot be measured from the supplied records: episode one's start/submission timestamp is absent for every ask, and only three attestation timestamps survive in the notes. The following table preserves all available timing evidence. “Unavailable” is not a zero-duration result.

| Key | Attestation timestamp retained (UTC) | Episode receiving answered wake, per notes | Elapsed time from episode one |
| --- | --- | --- | --- |
| weth-dep | Not retained | 3 | Unavailable: start timestamp missing |
| weth-wd | Not retained | 3 | Unavailable: start timestamp missing |
| weth-dep-sum | Not retained | 3 | Unavailable: start timestamp missing |
| weth-wd-sum | Not retained | 3 | Unavailable: start timestamp missing |
| usdc-mint | Not retained | 3 | Unavailable: start timestamp missing |
| usdc-mint-sum | Not retained | 3 | Unavailable: start timestamp missing |
| usdc-burn | 2026-11-08T22:05:40Z | 4 | Unavailable: start timestamp missing |
| v4-init | 2026-11-08T22:05:09Z | 4; request status already attested in 3 | Unavailable: start timestamp missing |
| v2-pairs | 2026-11-08T22:05:09Z | 4; request status already attested in 3 | Unavailable: start timestamp missing |
| beacon-dep | Not retained | 3 | Unavailable: start timestamp missing |

Episode one submitted the asks and the check batch together. Episode two distinguished completed request-opening effects from answered asks and avoided duplicate submissions. Episode three retained seven answered wakes while the other answers were still arriving. Episode four retained the final three answered wakes; all asks were then recorded as attested. The check batch remained queued during those episodes and settled by episode five, when the notes recorded completion. This gives an episode-level sequence, not a wall-clock latency. The configured `afterMinutes: 120` was a wake deadline and cannot be used as elapsed time. [G, episodes 1–5](#source-g)

The single batch was `check`, with mode `research`. The surviving brief begins “Compute one figure from public Ethereum mainnet (chainId 1) data and write it as one table row,” then specializes the item with `{{key}}`, `{{what}}`, `{{address}}`, `{{event}}`, `{{topic0}}` and `{{filter}}`. Its displayed tail is truncated. Episode one preserves the result contract: one item per key; one JSON row per item; columns `key` (string), `answer` (decimal), and `rpc` (string); table keyed on `key`; `maxRows: 1`; `groupSize: 10`. Thus the retained brief scopes each item to one figure, and the notes specify exactly what its result must contain. Each supplied result has precisely that row shape. No additional batch, including a `recheck-<key>` batch, appears in the final batch list. [G](#source-g); [C01–C10 below](#source-register)

The current batch record says settled, not cancelled, with every item accepted and none failed, running or waiting. The declared dataset figure is exactly `{"dataset": "check", "rows": 10}`. It is copied unchanged into [figures.json](figures.json), the only entry in that manifest. The current dataset has no totals. Event counts and sums in this report are transcribed from the individual results and oracle notes; they are not invented dataset totals. Episode five's prose caveat about a one-row dataset conflicts with both the current structured `dataset.rows` value and the assignment's declared figure. This report uses the current value, 10, and makes no claim about the cause of the earlier discrepancy. [G, current batch and episode 5](#source-g)

The check items report `eth_getLogs` over the same inclusive block window, divided as follows. All primary result scans used these boundaries; the V2 item's optional second-provider check subdivided some spans further. [C01–C10](#source-register)

| Span | Inclusive blocks | Blocks in span |
| --- | --- | ---: |
| A | 26371056–26371555 | 500 |
| B | 26371556–26372055 | 500 |
| C | 26372056–26372555 | 500 |
| D | 26372556–26372855 | 300 |

These ranges cover 1800 consecutive blocks without gaps or overlap and meet the at-most-500-block requirement. Workers report generating hex bounds in code, checking contract addresses and event topics, and excluding removed logs. Several also explicitly report range and duplicate-log checks. The table below preserves the chosen endpoint and reported matching-log counts for every item, including sum items. These are item-reported observations, not a fresh RPC scan.

| Key / evidence | RPC used for the complete row | A logs | B logs | C logs | D logs |
| --- | --- | ---: | ---: | ---: | ---: |
| [weth-dep / C01](#source-c01) | `https://ethereum-rpc.publicnode.com` | 3552 | 3253 | 2657 | 1512 |
| [weth-wd / C02](#source-c02) | `https://ethereum.publicnode.com` | 4430 | 4081 | 3518 | 2081 |
| [weth-dep-sum / C03](#source-c03) | `https://ethereum.publicnode.com` | 3552 | 3253 | 2657 | 1512 |
| [weth-wd-sum / C04](#source-c04) | `https://rpc.flashbots.net` | 4430 | 4081 | 3518 | 2081 |
| [usdc-mint / C05](#source-c05) | `https://ethereum-rpc.publicnode.com` | 339 | 307 | 269 | 177 |
| [usdc-mint-sum / C06](#source-c06) | `https://ethereum-rpc.publicnode.com` | 339 | 307 | 269 | 177 |
| [usdc-burn / C07](#source-c07) | `https://ethereum-rpc.publicnode.com` | 203 | 185 | 113 | 87 |
| [v4-init / C08](#source-c08) | `https://ethereum-rpc.publicnode.com` | 42 | 14 | 16 | 22 |
| [v2-pairs / C09](#source-c09) | `https://ethereum-rpc.publicnode.com` | 8 | 10 | 6 | 7 |
| [beacon-dep / C10](#source-c10) | `https://ethereum.publicnode.com` | 6 | 8 | 18 | 68 |

The event topic hashes preserved in the history are below. Contract addresses and full Solidity event signatures are in the opening table; the canonical signatures here omit parameter names and `indexed` only for identifying topic0. [G, episodes 1 and 5](#source-g)

| Applicable keys | Canonical event signature | topic0 |
| --- | --- | --- |
| weth-dep, weth-dep-sum | `Deposit(address,uint256)` | `0xe1fffcc4923d04b559f4d29a8bfc6cda04eb5b0d3c460751c2402c5c5cc9109c` |
| weth-wd, weth-wd-sum | `Withdrawal(address,uint256)` | `0x7fcf532c15f0a6db0bd6d0e038bea71d30d808c7d98cb3bf7268a95bf5081b65` |
| usdc-mint, usdc-mint-sum, usdc-burn | `Transfer(address,address,uint256)` | `0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef` |
| v4-init | `Initialize(bytes32,address,address,uint24,int24,address,uint160,int24)` | `0xdd466e674ea557f56295e2d0218a125ea4b4f0f6f3307b95f85e6110838d6438` |
| v2-pairs | `PairCreated(address,address,address,uint256)` | `0x0d3648bd0f6ba80134a33ba9275ac585d9d315f0ad8355cddefde31afa28d0e9` |
| beacon-dep | `DepositEvent(bytes,bytes,bytes,bytes,bytes)` | `0x649bbc62d0e31342afea4e5cd82d4049e7e1ee912fc0889aa790803be39038c5` |

USDC mint rows match the zero address in indexed `from` (`topics[1]`); the burn row matches it in indexed `to` (`topics[2]`), leaving `from` unconstrained. The zero address is encoded as a 32-byte zero topic. These filters count Transfer events matching the goal's definitions, without any claim about other mint/burn mechanisms. WETH sums decode `wad` from the first 32 data bytes, and the USDC sum decodes `value` the same way. Sum workers describe Python arbitrary-precision integers or JavaScript BigInt, avoiding floating-point rounding. The beacon result counts DepositEvent logs; it does not sum the dynamic `amount` field. [C03–C07, C10](#source-register)

Two sum items retain enough subtotals to check their arithmetic directly:

| Key / evidence | A sum | B sum | C sum | D sum | Total and unit |
| --- | ---: | ---: | ---: | ---: | --- |
| [weth-dep-sum / C03](#source-c03) | 7462186476483067905599 | 3353445224232666110719 | 4186923759796089054061 | 1110986176602895077282 | 16113541637114718147661 wei |
| [usdc-mint-sum / C06](#source-c06) | 9177191383347 | 13860168142635 | 13078511598022 | 3702576558670 | 39818447682674 base units |

The WETH withdrawal sum result supplies its total and matching-log counts, but no per-span amount subtotals or raw logs. Its total can be compared exactly with the recorded attested value; it cannot be independently reconstructed from the handed summary alone. [C04](#source-c04)

Provider diversity is limited. Nine row endpoints belong to PublicNode: six use `https://ethereum-rpc.publicnode.com` and three use `https://ethereum.publicnode.com`. The withdrawal-sum item uses `https://rpc.flashbots.net`. The shared PublicNode operator is identified in episode five's notes; different hostnames do not establish independent infrastructure. The oracle's RPC endpoint is not disclosed in this handoff, so independence from that provider cannot be established. [G, episode 5](#source-g); [C01–C10](#source-register)

There is useful additional corroboration, but it has a precise scope. The Flashbots withdrawal-sum item reports the same withdrawal log counts as the PublicNode withdrawal-count item. The V2 item reports the same per-span counts and block numbers on `https://eth.drpc.org`, after halving some ranges. Neither was a formal recheck batch. Flashbots supplies only one handed computation of the withdrawal **sum**; the matching withdrawal **count** on PublicNode is not a second computation of that sum. The beacon and WETH deposit-sum items merely probed Flashbots and did not use it to corroborate their full figures. [C02–C04, C09–C10](#source-register)

The public RPC failures were access and query constraints: workers reported HTTP 403/429/525 responses, API-key requirements, small allowed log ranges, and an inconsistent range-limit error from dRPC. Some workers discarded earlier partial reads and recomputed the entire figure at the endpoint named in their row. These failures did not leave any check item unaccepted. They explain much of the concentration on PublicNode without proving that all alternative providers were unusable under every possible query strategy. [C01–C04, C07, C09–C10](#source-register)

The plane records `sources.checked: 10`, `sources.flagged: 1`, and `flaggedResults: ["check/weth-wd"]`. It supplies no detailed flag reason in the current structured batch record. Episode five attributes the flag to treating an `eth_chainId` JSON-RPC POST response as a quote that a webpage fetch could replay; the worker confirms that a plain GET returned HTTP 403. That is the preserved explanation, not a newly verified plane diagnostic. The flagged row remains accepted and numerically agrees with the recorded oracle answer and Flashbots' withdrawal log count. A successful chain-id response alone would not substantiate the log count; the worker says the count came from its POST `eth_getLogs` responses. [G, episode 5 and current batch](#source-g); [C02](#source-c02); [C04](#source-c04)

No code repository or wave commit was produced for this goal: the only batch is research and `trunk` is `null`. There is consequently no trunk repository or commit to name. Episode five records `finish: true`, with no further work launched. The original decisions file is not included in the handoff; the following single JSON object restates that terminal decision in the supplied reference's shape, within this report:

```json
{
  "notes": "Episode 5 records all ten asks as attested and the check batch as settled. Every recorded attested value equals its handed check row. No mismatch triggered a recheck, and no refusal triggered a retry. Finish the write-up, preserving the missing question text, digests and timing evidence as limitations.",
  "spawn": [],
  "finish": true
}
```

Local write-up checks parsed every input as JSON, compared each decimal answer to the value preserved in the oracle notes using exact integers, checked all supplied count subtotals and the two available amount-subtotal sets, and checked contiguous span coverage. Input SHA-256 hashes were matched to the assignment's pinned values. These checks establish consistency of the handoff and transcription; they add no independent chain evidence or signature verification. No network queries were used for this write-up.

<a id="source-register"></a>
The source register below identifies the supplied evidence even when the staging inputs are removed. Row values, endpoints, relevant method notes and timing evidence have been carried into this report. File hashes identify input bytes only; they are **not attestation digests**. Each `C` source is the result `check/<key>`, originally named `artifacts/goal/batches/check/items/<key>/result.json`, and supplied as `.imd/reads/artifacts/b01-<key>`.

<a id="source-g"></a>
**G** is `.imd/reads/goal.json`, pinned input `685b2cdb-9682-4b30-acdc-d07b52576462:0`, SHA-256 `7b7f0019be55cd5f2b97528fc8ed27b62899297e3019dd2e62c52d30eec9c8e9`. Its `goal.objective` and episode-one notes supply the ask definitions and batch design; episodes three and four supply recorded oracle answers, request ids and limited timing; episode five supplies the final comparison and caveats; the current batch record supplies settlement, dataset and source-flag metadata. The orchestration reference is `.imd/reads/skills/goal-orchestrator/REFERENCE.md` (pinned input `685b2cdb-9682-4b30-acdc-d07b52576462:2`); it supplies the decision-object shape, not additional observed outcomes.

| Citation | Handed input / result | SHA-256 of supplied result |
| --- | --- | --- |
| <a id="source-c01"></a>C01 | `b01-weth-dep` / `check/weth-dep` | `f9cfa9110e53a7e1bd46d6ee9a01a8e04a540a492cbc591c641ef5d625f382a6` |
| <a id="source-c02"></a>C02 | `b01-weth-wd` / `check/weth-wd` | `07f373cf82b70f656f15c69286cc4af44c499ae345d77a733a59671eef375fe4` |
| <a id="source-c03"></a>C03 | `b01-weth-dep-sum` / `check/weth-dep-sum` | `772cd0bec40c894f7d9d4ae0317251f1d0eccfe195044281f187e891b4dd656b` |
| <a id="source-c04"></a>C04 | `b01-weth-wd-sum` / `check/weth-wd-sum` | `1056c9c14c805d655af7437980fc55809d676dd7ea9c07b263b473249d666c37` |
| <a id="source-c05"></a>C05 | `b01-usdc-mint` / `check/usdc-mint` | `e0be29c5a036c33a709dcacf639ed8d014c0e0a33bac7d1f63ff33c764a73af9` |
| <a id="source-c06"></a>C06 | `b01-usdc-mint-sum` / `check/usdc-mint-sum` | `467534bbc561db1a2408ada8d4fc24cd68385f7f612ca9cd5c5405cc3206942b` |
| <a id="source-c07"></a>C07 | `b01-usdc-burn` / `check/usdc-burn` | `4bc7be1761cff01d70468d3dd9ac457343a74ac6acde86c1a2fc06cb548e2d72` |
| <a id="source-c08"></a>C08 | `b01-v4-init` / `check/v4-init` | `21dca0c6e4c076a867a93066d4256cb886c21465cfec2995c82d3943bcba8ca6` |
| <a id="source-c09"></a>C09 | `b01-v2-pairs` / `check/v2-pairs` | `1bb23f1d04ad8a5ec6bf491b7144b2194442da85a1325b50e001c975849337cd` |
| <a id="source-c10"></a>C10 | `b01-beacon-dep` / `check/beacon-dep` | `858bc00d984215cf5dd7ae2c3d5ff3da342031886c415c8c554a8c80c41c19c0` |

This run supports a narrow positive finding about goal asks: the recorded chain-evidence answers agreed exactly with the goal's own event-count and integer-sum results for this fixed Ethereum window. Full event definitions, explicit filters and base units made the comparisons unambiguous. Preserving answers across episodes and distinguishing opening effects from answer wakes allowed the workflow to finish without duplicate asks or unnecessary recheck batches. [G](#source-g); [C01–C10](#source-register)

The observed weaknesses were operational and evidentiary: the check queue lagged behind the oracle answers; public RPC access failures reduced provider diversity; one source check could not replay the cited POST evidence; and the final handoff lost exact question text, attestation digests, signed payloads and enough timestamps to measure latency. No numeric disagreement or oracle refusal was observed, so this run does not test mismatch recovery, wording-based refusal retries, signature validity, or performance guarantees for other windows and question types. [G](#source-g); [C01–C10](#source-register)

Future runs should make the following changes:

1. Preserve every submitted question verbatim, including the plane's prefix, and retain the full request and signed attestation objects: request id, answer bytes, decimal interpretation, digest, signature, signer, chain/window metadata and status. That would make the opening comparison auditable beyond episode summaries.
2. Record episode-one submission time, request creation, attestation time, answer-wake receipt, and check start/completion times in UTC. Compute latency only from those retained timestamps, separating oracle processing from queueing and delivery.
3. Make RPC evidence replayable as JSON-RPC POST requests and responses, with chain id, exact ranges, filters, block hashes, per-span counts and sum subtotals. Use a source verifier that understands POST evidence, and preserve the plane's detailed flag reason.
4. Arrange checks across distinct RPC operators and record the oracle reproduction provider where possible. Allow smaller spans when a provider requires them, while staying within the 500-block maximum. Retain the current mismatch-triggered recheck rule for discrepancy handling; broader replication would need to be part of the next experiment's brief.
5. Export authoritative dataset metadata and the full batch brief alongside item results. Preserve disagreements between historical notes and current state explicitly, and let the current declared dataset figure control the figures manifest.
