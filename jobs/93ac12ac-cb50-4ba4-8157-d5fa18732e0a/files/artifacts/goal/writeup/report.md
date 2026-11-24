**INCOMPLETE — Bitcoin Puzzle #140 was not solved by this order, and no confirmed prize payment to the designated recipient was established.** No real-target search, recovered private key, production search checkpoint, or mainnet broadcast by the order is evidenced. The delivered code supports public verification, generated search tests, and a reproduced regtest claim workflow. It is not a validated, integrated production recovery-and-payment package. Nothing in this report substitutes a benchmark, component PASS, or report for the requested solution.

The latest handed mainnet observation ended **2026-11-24T11:03:36.975Z**: Blockstream and mempool.space agreed on **seven confirmed unspent outputs totaling 1,400,002,880 satoshis (14.00002880 BTC), before fees**, and neither observed a pending prize spend. This is a dated observation, not a current spendability guarantee. The final payment verdict was “no payment observed”; public evidence cannot establish who may know the private key. [b15-challenge-and-prize]

**Delivered source and scope.** The goal repository is [identity-md-launches/goal-3375-objective-solve-public-bitcoin](https://github.com/identity-md-launches/goal-3375-objective-solve-public-bitcoin.git), at final trunk commit [`45adea724172d45c2c8f18d69ff44df9acc26161`](https://github.com/identity-md-launches/goal-3375-objective-solve-public-bitcoin/tree/45adea724172d45c2c8f18d69ff44df9acc26161). This is the revision replayed by the final independent worker. Earlier merged revisions were `aebd9183af6a4b1643ddd1e71277f0e8166f3eda`, `0992632e39cd0624c0ead76e9e4ab6f176fb07c5`, and `65995c0a126daa60e498acca1ff0e408bf842048`; findings below retain their original revision scope. The final read-only wave had nothing to merge. `goal.json`; [b14-offline-replay]

This assignment delivers only this Markdown report. The implementation and bundled dependencies remain in the named repository; they are not embedded in this report or newly packaged as an offline archive. The original reports are identified by their supplied content hashes at the end, and the material findings and replay commands are preserved here because the handed input directory is temporary.

The write-up independently checked all 28 handed SHA-256 pins, parsed all 26 JSON results, recomputed public identity/checksum and interval arithmetic, and reconciled both recorded seven-output inventories. Public reads of the final pinned repository confirmed the relevant replay entry points and the two regtest fixture hashes. These were source/data checks, not a new solver, regtest, or mainnet execution. All execution results below are attributed to the workers that produced them. No machine inventory or configuration inspection was performed for this write-up; no private key or credential is included.

**Completion criteria and remaining gaps.**

| Requirement | Evidence and disposition |
| --- | --- |
| Verify public challenge, revealed key/address, declared interval, recipient | Public provenance and repeated independent derivations passed; checksum and arithmetic also recomputed during this write-up. Unknown-secret membership in the published interval remains unproven. |
| Determine available prize | Repeated two-provider dated observations, raw parent transaction checks, and historical Merkle proofs exist. Fresh validating-node inventory is still required before a real run and claim. |
| Use available orchestration resources | All 50 item allocations and all five planning rounds used; this does not mean 50 concurrent machines, 50 successful components, or any GPUs. |
| Review/pin implementations and licenses | RCKangaroo and JeanLucPons/Kangaroo reviewed and pinned; implementation limits and unresolved RCK defects remain. |
| Test small known-answer instances; measure work | Generated secp256k1, finite-field toy, signature, and regtest tests reported. CPU process work/timing/memory available; no measured GPU performance or comparable device inventory. |
| Coordinated real search with checkpoints | Not run. Coordinator missing; integrated launcher and release audit never ran. No real checkpoint exists to resume. |
| Establish private recovery/signing path | Standalone private interfaces exist and regtest signing passed. Entrant custody and integrated private verifier-to-signer relay have not been demonstrated. |
| Recover and independently verify real key | Not achieved. Synthetic acceptance cannot establish this. |
| Confirm exclusive-recipient mainnet payment | Not achieved. No candidate prize spend was observed in the final snapshot. |
| Respect 5 IMD ceiling | Existing allocation only; zero external spending authorized, and no paid service/rental reported. Aggregate platform billing was not supplied, so an actual total at or below 5 IMD cannot be independently certified. |

**Public challenge and fixed destination.**

| Field | Verified public value |
| --- | --- |
| Challenge | Bitcoin Puzzle #140 |
| Source address | `1QKBaU6WAeycb3DbKbLBkX7vJiaS8r42Xo` |
| Compressed public key | `031f6a332d3c5c4f2de2378c012f429cd109ba07d69690c6c701b6bb87860d6640` |
| Source HASH160 | `ffbb35a7bb9bbe16c1aa2534f7ff11d59c8e3d1a` |
| Source scriptPubKey | `76a914ffbb35a7bb9bbe16c1aa2534f7ff11d59c8e3d1a88ac` |
| Inclusive private-key interval | `[2^139, 2^140 − 1]` |
| Number of candidates | `696898287454081973172991196020261297061888` = `2^139` |
| Sole recipient | `bc1pg6luxm9s4qq65lge4l6ual7xwdw5v85eh675cmrl5we0ht3vpfhswxu0cx` |
| Sole recipient scriptPubKey | `512046bfc36cb0a801aa7d19aff5ceffc6735d461e99bebd4c6c7fa3b2fbae2c0a6f` |

The permitted output is one payment to its fixed script, less Bitcoin network fees, without change, operator fees, donations, or pool shares. Checksum validity establishes encoding/network consistency, not recipient ownership.

The original funding transaction [`08389f34c98c606322740c0be6a7125d9860bb8d5cb182c02f98461e5fa6cd15`](https://blockstream.info/api/tx/08389f34c98c606322740c0be6a7125d9860bb8d5cb182c02f98461e5fa6cd15), output 139, paid 14,000,000 sats at height 339085. The public key is exposed in zero-based input 15 of [`17e4e323cfbc68d7f0071cad09364e8193eedf8fefbcbd8a21b4b65717a4b3d3`](https://blockstream.info/api/tx/17e4e323cfbc68d7f0071cad09364e8193eedf8fefbcbd8a21b4b65717a4b3d3), confirmed at height 578732. That input spent a separate 1,000-sat deposit, `7c432398c7631600af01695c9767eff109cbfae4f7ecccaff388043a474d4f1e:16`; it did not spend the seven-output prize inventory below. Its destination differs from the required recipient. [root-1-01]; [b09-challenge-and-prize]; [b15-challenge-and-prize]

The key decompresses to an on-curve secp256k1 point with odd Y. HASH160 plus mainnet Base58Check version `00` produces the stated source address; the checksum bytes are `72d9d7c6`. The requested recipient decodes as HRP `bc`, witness version 1, a 32-byte program, and Bech32m residue `0x2bc830a3`. Its program is `46bfc36cb0a801aa7d19aff5ceffc6735d461e99bebd4c6c7fa3b2fbae2c0a6f`. These public derivations were recomputed without a secret during the write-up. [b09-challenge-and-prize]; [b10-boundary-audit]

The challenge worker recorded [btcpuzzle.info/puzzles](https://btcpuzzle.info/puzzles) at 2026-11-24T10:13:54.506934Z, response SHA-256 `73212ce4ab6121dc0516c22de0a7883dab01b6645ee53d22197295d9fb1f08c1`. Its exact endpoint excerpts were `Range start</small><b class="hex">080000000000000000000000000000000000` and `Range end</small><b class="hex">0FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF`. Parsing those hexadecimal numbers reproduces the stated bounds. They establish the published puzzle convention; a revealed public point and funding output do not prove where its unknown discrete logarithm lies. [b09-challenge-and-prize]

**Dated prize inventory and payment evidence.** The final common tip was height **977356**, hash `00000000000000000000980f8ec935f2d897b142f93e578cf7e5c0bd89ef1d86`. Blockstream's bracket was 11:03:35.711Z–11:03:36.975Z; mempool.space's was 11:03:35.712Z–11:03:36.677Z, on November 24, 2026. Both returned the same tip before and after, the following outpoints and amounts, no pending address activity, and `spent:false` for every listed outpoint. [b15-challenge-and-prize]

| Funding transaction | vout | Satoshis |
| --- | ---: | ---: |
| `08389f34c98c606322740c0be6a7125d9860bb8d5cb182c02f98461e5fa6cd15` | 139 | 14,000,000 |
| `12f34b58b04dfb0233ce889f674781c0e0c7ba95482cca469125af41a78d13b3` | 64 | 1,260,000,000 |
| `2b4f5f05b1377845ff0f8c1552dc901172ee2da9508b08d5c951366f74fbbf63` | 0 | 640 |
| `5d45587cfd1d5b0fb826805541da7d94c61fe432259e68ee26f4a04544384164` | 88 | 126,000,000 |
| `918c913baad2ae7a3b444350e047559434a4441041b5ba5050d09b8b54ef68b7` | 0 | 640 |
| `d8c38d06fe7ea6adf44c5cc2cbf50083ec9cd8a3fc6c537e8d39db30639e8a77` | 0 | 1,000 |
| `dd23b1079095ec6821f003b5a1acd5942152f478411157d717c8bddf8f67fb94` | 0 | 600 |
| **Total** | **7 outputs** | **1,400,002,880** |

The underlying read endpoints are [Blockstream UTXOs](https://blockstream.info/api/address/1QKBaU6WAeycb3DbKbLBkX7vJiaS8r42Xo/utxo) and [mempool.space UTXOs](https://mempool.space/api/address/1QKBaU6WAeycb3DbKbLBkX7vJiaS8r42Xo/utxo), with each provider's `/tx/{txid}/outspend/{vout}`, raw parent transaction, tip, and address history endpoints. The linked live endpoints may have changed since the recorded observations; the hashed result preserves the observation times and responses. [b15-challenge-and-prize]

| Earlier corroboration | Anchor and result |
| --- | --- |
| E3, ended 10:13:59.215167Z | Height 977354, hash `00000000000000000000511422470fe101bd955fff49df9144ca8dafd92df1fa`; same seven outputs and sum, no observed pending spend. |
| E4, ended 10:52:57.696154Z | Height 977356, same hash as the final observation; identical inventory. Seven distinct parent txids, values, source scripts, Merkle roots, and containing headers checked. |
| E5, ended 11:03:36.975Z | Both prior anchor hashes still reported active; no added, removed, or revalued outpoints, and no candidate prize spend. |

All times in that table are UTC on 2026-11-24. E4 obtained Merkle branches from Blockstream only, while raw transactions, headers, and block hashes at heights were cross-checked against both providers. A Merkle branch proves historical inclusion, not unspentness or independent most-work-chain validation. Public API reads are non-atomic, can be cached, and omit unpropagated/private transactions. No independent mainnet validating node was run for these observations. [b09-challenge-and-prize]; [b12-challenge-and-prize]; [b15-challenge-and-prize]

Historical funded total `1,400,003,880` minus the separate spent `1,000` equals the observed `1,400,002,880` sats. The final result contains no candidate transaction to check for a prize sweep: transaction coverage, fees, recipient exclusivity, and confirmation were therefore **not applicable**, not passed. No payment txid or real solution attribution is supplied. [b15-challenge-and-prize]

**Orchestration and budget record.** The supplied goal state records `items.max=50`, `items.used=50`, `workers=50`, `maxEpisodes=5`, and final episode 5. Allocations by planning round were 14, 16, 12, 6, and 2. All 15 batches settled; no pending work or additional spending is proposed. The E3 target board is more informative than its aggregate acceptance counter: six targets landed, coordinator and RCK sink were stuck after two attempts each, and the dependent private launcher and release audit had zero runs. “Settled” does not mean every requested component was completed. `goal.json`

The following is a record of each batch's single-item contract, not a new dispatch. The exported goal state truncates several briefs with an ellipsis and omits per-item substitutions; those missing suffixes are not reconstructed as quotations. Visible openings consistently scope one assertion, provider snapshot, component, review, or verdict per item. Result expectations below are drawn from the visible contracts and handed results.

| Batch | Allocations | One item's work and required result |
| --- | ---: | --- |
| `public-checks` | 3 | Independently check one public assertion; JSON assertion/status, expected/observed values, method, evidence URLs, limitations. |
| `prize-snapshots` | 2 | Measure one provider's inventory; dated bracketed tip, unique valued outpoints/scripts and pending-spend evidence in JSON. |
| `prize-crosscheck` | 1 | Reconcile the two inventories; common anchor, agreed outpoints, total and explanations for differences. |
| `method-evidence` | 3 | Review one implementation or work estimate; immutable references, method, observations, caveats, sources and attributed performance units. |
| `verification-tools` | 5 | Build one standalone verification/test component; source, deterministic tests, README, exact commands, observed results and blockers. |
| `e2-runner-components` | 14 | Deliver one component or read-only check within its scope; offline reproduction, dependency pins/licenses and honest test/blocker reporting. |
| `e2-focused-reviews` | 2 | Resolve one theory or private-boundary evidence gap; question/status, pinned sources, reproduced evidence, limitations and acceptance checks. |
| `e3-private-runner` | 10 | Implement/check one dependency-ordered component; scoped code, named executable gate, synthetic/regtest evidence and no public secret state. Six landed; two stuck; two never ran. |
| `e3-public-state` | 1 | Refresh one challenge/prize record; published identity/range evidence, derivations, dated inventory and limitations. |
| `e3-private-path-audit` | 1 | Audit the pinned recovery-to-claim boundary; prioritized findings, source locations, reproductions and repair prerequisites. |
| `e4-evidence-tools` | 4 | Complete one assigned evidence tool/reproduction; JSON component, base commit, changed paths, checks, measurements, evidence, limitations, replay and objective status. |
| `e4-funding-evidence` | 1 | Verify one seven-output historical funding set; recomputed txids/values/scripts, Merkle/header evidence and separately dated spend status. |
| `e4-source-inventory` | 1 | Inventory the pinned optional backends; licenses, immutable pins, source/binary classification, prerequisites and audit disposition. |
| `e5-merged-evidence` | 1 | Return one offline compatibility verdict on the final commit; actual command exits, fixture hashes, regtest/toy accounting and diagnostics. |
| `e5-payment-state` | 1 | Determine one dated public payment status; both providers' tip brackets, inventory movement, pending activity, candidate spends and attribution limits. |

No external paid services, rented compute, pools, child orders, or new purchases were authorized in the planning notes. Workers reported local zero external spend. Actual platform charges are absent, so this report does not manufacture a 5-IMD reconciliation. The worker cap is an allocation limit and supplies no GPU entitlement or indefinite runtime.

The reference's decisions schema requires a JSON object with `notes`; `finish` is optional and means that the evidence is ready to write up. No separate decisions file is supplied or named for creation in this report-only assignment, and none was found in the final public source tree. The earlier decisions file's existence/shape therefore cannot be independently certified here. To preserve the disposition without violating “write nothing else,” the reference-shaped record is embedded below; it is **not** represented as a separately delivered decisions file or a successful solution:

```json
{
  "notes": "INCOMPLETE. All 50 item allocations and five planning rounds are consumed. Public identity and dated prize evidence, synthetic search tests, and regtest claim/evidence replay are available at trunk 45adea724172d45c2c8f18d69ff44df9acc26161. There is no verified real key, real checkpoint, mainnet broadcast by this order, or confirmed designated-recipient prize payment. Coordinator, integrated private launcher, and release audit remain incomplete; RCK verification conflicts and range/parser defects remain unresolved. Preserve the pinned source and reported checks. Any future production execution requires entrant-controlled private custody, repaired and tested integration, and fresh validating-node inventory. Aggregate platform billing is unavailable; no new spending or work is dispatched.",
  "finish": true
}
```

**Implementation and license evidence.**

| Component | Pin/license | Delivered capability and limit |
| --- | --- | --- |
| RCKangaroo | [RetiredC/RCKangaroo at `618473acd7f5e696be5ec4f8377c18cc55c1361c`](https://github.com/RetiredC/RCKangaroo/tree/618473acd7f5e696be5ec4f8377c18cc55c1361c), GPLv3; license retained at `rckangaroo/upstream/LICENSE.TXT` | Vendored source, private-output patch and adapter. No built CUDA binary or verified GPU known-answer run. Upstream plaintext recovery sinks needed patching. Tame precomputation is not full wild-walk resume. |
| Native CPU comparator | [JeanLucPons/Kangaroo at `37576c82d198c20fca65b14da74138ae6153a446`](https://github.com/JeanLucPons/Kangaroo/tree/37576c82d198c20fca65b14da74138ae6153a446), GPLv3; `kangaroo-cpu/upstream/LICENSE.txt` | Patched source and static Linux x86_64 binary; synthetic endpoint, threading, checkpoint/resume and rejection checks passed. Packed distance fields limit the supported interval width to 125 bits. The wrapper rejects #140 and oversized widths. |
| Python private search | Goal trunk pin; `private-search/LICENSE` and `SOURCES.md` | Standalone standard-library CPU implementation, generated secp256k1 tests, private output/checkpoint interfaces. No production walk. Storage ceiling and missing coordinator prevent a complete distributed package. |
| Independent secp256k1 oracle | Worker reports v0.6.0 at [`0cdc758a56360bf58a851fe91085a327ec97685a`](https://github.com/bitcoin-core/secp256k1/tree/0cdc758a56360bf58a851fe91085a327ec97685a), MIT | Vendored source subset and per-file hash manifest, native C compiler needed. Inventory audit did not find the commit pin inside the repository; do not confuse the worker's provenance claim with an in-tree Git pin. |
| Bitcoin Core regtest runtime | Version 28.1, source commit `32efe850438ef22e2de39e562af557872a402c31`, MIT; `regtest-payment/runtime/COPYING` | Compressed Linux x86_64 executables and provenance files, available offline after checkout. Other architectures are not covered by the bundled binaries. |

The upstream [Core archive](https://bitcoincore.org/bin/bitcoin-core-28.1/bitcoin-28.1-x86_64-linux-gnu.tar.gz) pin is `07f77afd326639145b9ba9562912b2ad2ccec47b8a305bd075b4f4cb127b7ed7`. The native comparator binary pin is `781464cc2414527421bd88dd2604118aa9ab4fae5199a25acc8ab7ddc4d942a8`. The secp oracle's `vendor.sha256` file hashes to `71c8f041114e962c7baf36377a880c44a6b9f2a6c1712be4c91deca67ab55adb`, confirmed by this write-up's final-revision read. Its published point fixtures retain BSD-2-Clause attribution; generated baseline signature fixtures use CC0-1.0. [b06-regtest-offline]; [b06-secp-oracle]; [b13-boundary-audit]

RCK's reviewed commit differs from its v4.0 tag `a93695a799944d4a5f00ebccc42130353b4f98be`; the review reports a Makefile deletion. Opaque upstream turbo cubins were excluded from the package. The vendored assembly is not consumed by the CMake CUDA build and requires a separate upstream assembler. Upstream claims of K=1.15 and 14.5/19.3 billion jumps per second were not measured by this order; they are not evidence of available hardware or a completion time. [root-1-01]; [b13-boundary-audit]

**Search methods and measured results.** For the supplied interval, `N=2^139`, so `sqrt(N)=2^69.5`, approximately `8.348043408213×10^20`. This is an operation-count scale, not a measured rate or a guaranteed amount of work. A basic baby-step giant-step table with `ceil(sqrt(N))=834804340821298061591` entries would require `27548543247102836032503` bytes for illustrative 33-byte point payloads alone, before indices and table overhead. These values were recomputed with integer arithmetic. Kangaroo trades retained distinguished points against detection delay and stochastic work; repeated walks do not certify exhaustive key coverage.

The earlier `method-evidence/work-estimate` and `e2-focused-reviews/theory-recheck` each have a source flag in the goal state. Reasons are not present there; the latter report also lacked both requested paper PDF byte streams and direct access to the earlier estimate. Consequently the detailed literature constants and parallel-scaling claims are not promoted to independently verified results. No previously solved key pattern was used to predict this key. [b04-work-estimate]; [b07-theory-recheck]; `goal.json`

All measurements in the following table are worker-reported generated workloads. The memory entries are task-process lifetime high-water measurements, not machine RAM inventories or isolated algorithm allocations. Device identity is not established for a reproducible cross-device comparison.

| Workload | Measured work/time | Memory and interpretation |
| --- | --- | --- |
| Python secp256k1, width `2^20`, seed `compare-v1`, DP bits 0 | 8,278 walk steps in 0.317569892 s; 26,066.70 steps/s; 8,279 retained records | 29,954,048 bytes process peak RSS. Single synthetic worker; setup and final delivery separate. |
| Same width/seed, DP bits 4 | 8,310 steps in 0.291184689 s; 28,538.59 steps/s; 534 retained records | 20,615,168 bytes process peak RSS. Demonstrates this fixture's storage/detection trade-off. |
| Python secp256k1, width `2^24`, seed `large-synthetic-v1`, DP bits 8 | 13,956 steps in 0.490172395 s; 28,471.62 steps/s; 63 retained records | 19,832,832 bytes process peak RSS; total wall time 0.508524507 s. |
| Native comparator, generated 40-bit interval, two threads | 3,489,163 group additions in 0.915 s of walk time; reported 3,813,293 additions/s; 0.955 s total | 23,664 KiB task-process peak RSS, with possible inherited parent-process floor. This supported-range comparator refuses #140. |
| ECDSA verifier, 128 generated vectors | 128 timed verifications in 6.27491 s; 20.399 verifications/s | 20,864 KiB process peak RSS; 1,308 bytes measured Python allocation peak in a separate tracing phase. Signature verification is not interval search. |
| Finite-field toy replay, seven fixtures | BSGS 612 group operations = 7 setup + 605 search; kangaroo 2,948 = 1,456 setup + 1,492 search | Final replay suite 1.374 s. This is the order-65,393 subgroup of a small finite field, not secp256k1. |

The measurement records are [b06-private-search], [b08-native-comparator], [b08-ecdsa-regressions], [b11-toy-trial-restart], and [b14-offline-replay].

The original Python search component reported 41 tests, 56 endpoint/interior known-answer cases, nine of nine timed synthetic solves, and deterministic interrupted/resumed-state comparisons. E3 added five integration tests, native-generated oracle fixtures and an optional live libsecp256k1 comparison. Full-width initialization used a synthetic point with a mocked manifest validator; it is not a production solve. The pinned integration report distinguishes the optional live native-oracle run (35.097 s, 28,664 KiB) from the mandatory pinned-fixture run (41.150 s, 28,544 KiB). Neither measures a real-target search rate. [b06-private-search]; [b08-search-engine]; [final integration report](https://github.com/identity-md-launches/goal-3375-objective-solve-public-bitcoin/blob/45adea724172d45c2c8f18d69ff44df9acc26161/private-search/integration-report.json)

The independent candidate checker reported 40 tests, two separate scalar multipliers, exact 32-byte framing, interval endpoints, malformed candidates, wrong-endian input, and secret-sentinel error-path tests. Its production all-true path cannot be exercised without the unknown real key. The native oracle reported 559 strict assertions, including agreement with 128 baseline points/signatures/verifications; 172 assertions were available in its standalone mode. Later ECDSA regression checks covered 14 test methods, six RFC6979 nonce vectors, 23 retained Wycheproof cases, and 134 pinned independent oracle answers. A compiler-free fixture comparison is explicitly distinct from running a native oracle. [b06-candidate-check]; [b06-secp-oracle]; [b08-ecdsa-regressions]

Toy regressions repaired silent acceptance of malformed intervals/non-subgroup targets, made checks survive Python optimization, separated setup/search counts and traced/untraced timing, and tested 201 consecutive possible toy answers with no misses in either method. The earlier “width 4096” represented endpoint difference: that inclusive fixture has 4,097 candidates. Its table storage is order sqrt(width), not evidence of constant-memory production search. [b08-toy-regressions]

**Security and integration findings, with disposition.** The order did not have an entrant-private execution or custody channel. A private directory, inherited descriptor, or mode 0600 cannot protect a scalar from the operator of the execution host. Production checkpoints, wild distinguished points, and collision records can be key-equivalent; they must remain private along with candidates. This explains the use of synthetic/regtest worker runs and the entrant-controlled fallback, but does not satisfy the missing real execution. [b07-private-path-review]; [b10-boundary-audit]

| Finding | Evidence, repair, and remaining limit |
| --- | --- |
| Missing distributed coordinator | Both E3 attempts failed before tests: `walk-coordinator/check.py` was absent, exit 2. The final pinned public tree still has no such entry point. No collision-merging, deduplication, scheduling, or real-walk checkpoint result exists for this component. |
| Integrated private launcher/release audit | Both had zero runs because of target dependencies. The standalone `private-search/launch.py` does exist; it is not the unexecuted integrated launcher. No end-to-end production release acceptance occurred. |
| RCK 73-pass claim versus independent failures | Worker `b08-rck-sink` reported 73 CPU/private-I/O passes. The platform recorded two independent exit-1 checks and marked the target stuck. Diagnostics truncate before the failing assertion. Cause remains unresolved; local self-report does not override the target board. CUDA build and GPU known-answer execution remain unverified. |
| BA-01: confirmed partial sweep | Older `private-claim verify` inferred the selected inventory from the spend itself. E4/E5 regtest inventory tooling now distinguishes complete coverage from confirmation, including a confirmed partial sweep that omitted four outputs. No evidence establishes that a production success gate automatically composes all these checks. |
| BA-02: evidence export | Earlier aggregate claim summaries were insufficient for the raw-byte auditor. E3 added a regtest exporter with raw funding/spend bytes, valued pre-spend inventory and separate chain evidence; E4/E5 reproduced it. Mainnet evidence export and independent historical inventory remain untested. |
| BA-03: wrong RCK range width | Audit found `-range 140` despite `2^139` candidates. The write-up re-read the final manifest and adapter: they still set/pass 140. Required translation is 139 with start `2^139`; endpoint/outside-range GPU tests are absent. This is an unresolved source defect, not a measured slowdown. |
| BA-04: truncated tame-data acceptance | The older audit reproduced acceptance of a header-only file by the original CPU parser, which ignored short reads. The final `utils.cpp` SHA-256 remains `b659548681e3f3091a13d8f7106c72aa9ab39de739bd469582fdb4c0921f3562`, matching that audited code. No corrected loader or runtime revalidation is evidenced. |
| BA-05: fee-policy mismatch | E4 added a caller-supplied inclusive `--max-fee-sats` cap to the auditor; default remains 100,000 sats. E5 accepts equality at 2,164 and rejects a 2,163 cap. Receipt-supplied policy overrides are rejected; the integrator still must pass the same independently authorized cap to signer and auditor. |
| Core 28.1 compatibility and recipient | `getdescriptoractivity` was unavailable. Claim code was changed to reconstruct mempool activity with Core 28.1 methods, and the regtest destination was corrected to the exact mainnet recipient's witness program with regtest encoding. The actual CLI then passed live regtest signing/admission/broadcast/confirmation tests. |
| Candidate FD replay and identity binding | The verifier consumes/closes its stream. Duplicating a pipe does not duplicate its data; duplicated file descriptors share an offset. A private relay must provide the same verified bytes independently to the signer and bind decoded target/recipient fields and component hashes. Search and candidate manifests are not identical. |
| CPU capacity/resume | E3 added sparse-DP planning and preserves the pending point when capacity saturates. Increasing capacity can resume a saturated state, up to 100,000 records and the checkpoint size cap. At that ceiling the engine stops; a validated lossless external store/coordinator is still absent. |

These dispositions reconcile the target board in `goal.json` with [b08-coordinator], [b08-search-engine], [b08-claim-core], [b08-receipt-integration], [b08-rck-sink], [b10-boundary-audit], [b11-fee-policy], [b11-inventory-verdict], [b13-boundary-audit], and [b14-offline-replay].

The final-revision RCK source inspection is reproducible at [manifest_140.json](https://github.com/identity-md-launches/goal-3375-objective-solve-public-bitcoin/blob/45adea724172d45c2c8f18d69ff44df9acc26161/rckangaroo/adapter/manifest_140.json), [rck_adapter.py](https://github.com/identity-md-launches/goal-3375-objective-solve-public-bitcoin/blob/45adea724172d45c2c8f18d69ff44df9acc26161/rckangaroo/adapter/rck_adapter.py), and [utils.cpp](https://github.com/identity-md-launches/goal-3375-objective-solve-public-bitcoin/blob/45adea724172d45c2c8f18d69ff44df9acc26161/rckangaroo/upstream/utils.cpp). Manifest SHA-256 is `9057d510ca1ed66ff144c893462d18facb98ed3dd233253d3c7dd12bb06de4d9`; adapter SHA-256 is `07419f3809087f1bbb7fdc496d64dd21aaf847b7965c7bc8993198067e0be54c`. This static check does not diagnose the two failed independent RCK tests.

Earlier reports also found unsafe byte-auditor acceptance of caller-authenticated fictitious prevouts, network-label confusion, and excessive fees. Raw transaction parsing, txid/value/script checks, exact input-set equality, explicit network mode and fee policy replaced those behaviors. Later regtest coverage is stronger than the initial mock-only claim tests. It still leaves the distinction between authentic inventory, byte correctness, consensus validity, and active-chain confirmation intact. [b06-receipt-hardening]; [b08-receipt-integration]; [b11-fee-policy]

**Reproduced regtest payment, not a prize payment.** Final independent replay returned `COMPATIBLE` and `objectiveStatus: INCOMPLETE` at the final trunk pin. It used bundled Core 28.1 and offline fixtures, with no network or paid service. Its main integration command passed the 21-test receipt suite, 10-test payment suite, and 21-test private-claim suite, alongside real disposable-node signing/admission/broadcast/mining/verification. Reported elapsed time was 17.985 seconds. [b14-offline-replay]

| Published synthetic fixture field | Value |
| --- | --- |
| Network | Bitcoin regtest |
| Inputs | 7 |
| Input sum | 350,000,000 sats |
| Sole output | 349,997,836 sats to the fixed recipient witness program, encoded for regtest |
| Network fee | 2,164 sats |
| Signed virtual size | 1,082 vbytes |
| Fee / signed vsize | 2 sats/vbyte |
| Recorded active-chain depth | 2, on the disposable regtest chain |
| Synthetic txid | `2146972b61367c67fe7bc7a5638a1d86bb1b1e65ca38a867f219734fe321ad32` |
| Receipt file | `regtest-payment/claim_receipt.json` |
| Receipt SHA-256 | `7b1580efd82a5b80af28f30f16e860b94bb5c00c8e0e20df143059031c9b9694` |
| Separate evidence file | `regtest-payment/claim_evidence.json` |
| Evidence SHA-256 | `62ac64bc1fecd46fbdbfb9fc367c2ff0a73f1e18a77957e3b6b0566aa8b8a7a8` |

Both hashes were confirmed against public raw files at the final revision during this write-up. The earlier independent E4 reproduction also generated a fresh seven-input transaction with the same amounts, fee, size and depth, but different receipt/transaction hashes. Disposable wallets and blocks change between runs; stable accounting is not evidence that a newly generated transaction must match the published txid. [b11-regtest-reproduction]; [b14-offline-replay]

The byte auditor's PASS explicitly leaves `unspent_status` and `confirmation` **NOT ESTABLISHED**. The separate regtest evidence supplies the observed depth. The new inventory experiment uses a different fixture total, **350,000,021 sats**; it must not be mixed with the 350,000,000-sat payment fixture. [b11-inventory-verdict]; [b14-offline-replay]

| Inventory scenario | Final replay result |
| --- | --- |
| Complete confirmed sweep | 350,000,021 sats inventoried and spent; 349,997,021 paid, 3,000 fee, depth 2; coverage passes. |
| Confirmed partial sweep | Only 150,000,003 input sats; 149,997,003 paid, 3,000 fee. Confirmation passes while coverage is false: four omitted outpoints total 200,000,018 sats. |
| Later deposit | Does not change coverage of the earlier anchored inventory. |
| Payment-block rollback | Payment inactive, depth 0, in mempool; byte integrity survives while confirmation fails. |
| Snapshot rollback | Inventory anchor inactive; historical completeness cannot be accepted. |
| Missing snapshot | Inventory coverage unknown; inventory sum and anchor/match fields null. |

Runtime integrity checks validate compressed and unpacked binary hashes. The E4/E5 integration replay did not repeat the optional OpenPGP signature verification; the earlier packaging worker reported checking an upstream signer. This report does not equate a local manifest hash match with a fresh independent release-signature check. [b06-regtest-offline]; [b11-regtest-reproduction]; [b14-offline-replay]

**Checkpoints and exact offline replay.** There is no production checkpoint, production DP archive, verified real candidate, or real progress counter to resume. Synthetic private-search checkpoints were tested in disposable scratch and were not included as private state in public results. The source can regenerate them. The public toy replay checkpoints track completed benchmark fixtures only; they do not preserve #140 walks. [b06-private-search]; [b11-toy-trial-restart]

Toy fixture digest: `88d5ecc0c85266a579055e3f9dcedc6ac5a45ce7ac380136654c95ddb946b65b`. After an interrupted atomic update, four completed trials accounted for 346 BSGS operations and 1,699 kangaroo operations. Resume recovered the seven-trial totals of 612 and 2,948, matching a clean run. The resumed shard reused one completed trial and ran three; replay ignored five duplicate records without inflating totals. Missing shards and a mismatched fixture digest were detected; the digest-mismatch exit 2 is an intentional negative test. [b11-toy-trial-restart]; [b14-offline-replay]

Acquire the exact source revision before going offline. These are entrant/reviewer reproduction instructions, not commands executed by this write-up:

```sh
git clone --no-recurse-submodules https://github.com/identity-md-launches/goal-3375-objective-solve-public-bitcoin.git puzzle140
git -C puzzle140 checkout --detach 45adea724172d45c2c8f18d69ff44df9acc26161
cd puzzle140
```

Use Python 3 and the bundled Linux x86_64 Core runtime for the final replay. Run from that checkout root. Native oracle compilation additionally needs a local C compiler; no GPU is required for the following evidence checks. The final independent worker ran every command in this table successfully in its expected sense:

| Command | Expected exit and meaning |
| --- | --- |
| `python3 -I -B regtest-payment/check_claim.py` | 0: real Core regtest integration, fixture integrity and negative mutations pass. |
| `python3 -I -B regtest-inventory/check.py` | 0: completeness, partial-sweep, later-deposit and rollback verdicts pass. |
| `python3 -I -B toy-trial-replay/check.py` | 0: deterministic toy run, interruption, resume and negative fixtures pass. |
| `python3 -I -B receipt-check/audit.py --mode regtest --max-fee-sats 2164 regtest-payment/claim_receipt.json` | 0: byte audit accepts inclusive fee-cap equality. |
| `python3 -I -B receipt-check/audit.py --mode regtest --max-fee-sats 2163 regtest-payment/claim_receipt.json` | 1: expected rejection, actual fee 2,164 exceeds cap. |
| `python3 -I -B receipt-check/audit.py regtest-payment/claim_receipt.json` | 1: expected rejection because default audit mode is mainnet. |
| `python3 -I -B -m unittest discover -s receipt-check/tests -v` | 0: 21 tests. |

The exact expected exits and observations are recorded in [b14-offline-replay].

Additional component replay commands, reported in earlier results, are `python3 -I -B private-search/check_integration.py`, `python3 -I -B private-claim/check_core.py`, `python3 -I -B kangaroo-cpu/check_offline.py`, `python3 -I -B toy-comparison/check.py`, and `sh secp-oracle/check.sh --require-baseline`. They are not all replays performed by the final E5 worker. The native comparator's timing gates can be sensitive to scheduling; failure must retain the actual diagnostic rather than be silently skipped. [b08-search-engine]; [b08-claim-core]; [b08-native-comparator]; [b08-toy-regressions]; [b06-secp-oracle]

For an explicit toy trial restart, the following creates/reuses local generated-fixture checkpoints and then compares both shards:

```sh
python3 -I -B toy-trial-replay/replay.py run test/scratch/toy-state 0
python3 -I -B toy-trial-replay/replay.py run test/scratch/toy-state 1
python3 -I -B toy-trial-replay/replay.py run test/scratch/toy-state 0
python3 -I -B toy-trial-replay/replay.py check test/scratch/toy-state/shard-0.json test/scratch/toy-state/shard-1.json
```

Re-running a shard reuses completed trials under the same digest. These commands exercise generated fixtures, not the public puzzle. [b11-toy-trial-restart]

**Exact remaining entrant actions and private interfaces.** The unresolved production work is substantive: provide entrant-controlled custody; repair and verify the integrated candidate relay, coordinator and release gate; resolve any selected backend's outstanding defects; and capture a fresh authenticated inventory. No integrated production command or checkpoint can honestly be labeled validated. The standalone CPU runner and private claim component nevertheless have concrete interfaces that can be rehearsed and integrated without disclosing a scalar.

1. Obtain the pinned source, preserve its licenses, and reproduce the offline gates above. If selecting RCK, first repair the 139-bit range translation and strict precomputation loading, resolve the two failed output checks, build from reviewed inputs on entrant-controlled compatible hardware, and pass generated GPU known-answer tests. The native comparator cannot be converted into a full-width solver by simply removing its guard.
2. Establish a private process boundary before any real-key execution. Keep candidates, full DP records, collisions and checkpoints outside the checkout and out of public logs/backups. Bind target, interval, recipient and exact component/build identity. Validate common jump/DP namespaces, unique assignments, point equations, collisions and replay. Test the same private verifier-to-signer relay with generated cases; never assume a duplicated descriptor replays consumed bytes.
3. Re-verify the public challenge and current spendable inventory using an entrant-controlled, fully synced validating Bitcoin node, before real execution and again before signing. Historical API snapshots in this report are insufficient. The claim component documents Core 28.1, a complete transaction index and access to raw funding transactions.
4. Run only an appropriately bounded, privately controlled backend. Use preserved private state for resumption and report only safe counters/digests. Real execution has not been tested by this order. Stop at a storage limit without silently discarding collision evidence; implement and independently test lossless continuation before claiming distributed readiness.
5. If a real candidate is recovered, independently verify exact framing, scalar validity, inclusive range, `kG=Q`, compressed source address, and fixed payout identity. Preserve an authenticated, valued, pre-spend inventory bound to a named active tip and mempool view. Build/sign one output exclusively to the required recipient with an explicit total network-fee cap, then test node admission and recheck inputs/state.
6. Use the already authorized broadcast only after those checks. Preserve public raw funding/spend bytes and separate inclusion/active-chain evidence, then independently verify complete inventory coverage, fee, sole recipient and confirmation depth at a recorded tip. `prepared`, `broadcast_pending`, byte PASS, a balance reduction, or another party's spend is insufficient. No additional operator fee or substituted address is permitted.

The standalone CPU README provides the following bounded start/resume interface. Set `task_checkout` and `task_private` yourself to actual absolute paths; the private parent must exist and the state must be outside the physical checkout. These are future entrant-only commands, **not evidence that they ran**, and they do not integrate signing or coordination:

```sh
python3 -I -B "${task_checkout:?set actual checkout path}/private-search/launch.py" --mode real --entrant-controlled --private-dir "${task_private:?set actual private state path}" --seed entrant-v1 --worker-id cpu-001 --generation 0 --dp-bits 61 --max-records 10000 --max-steps 100000 --max-seconds 60 --checkpoint-steps 1000 --export-dp

python3 -I -B "${task_checkout:?set actual checkout path}/private-search/launch.py" --mode real --entrant-controlled --private-dir "${task_private:?set actual private state path}" --seed entrant-v1 --worker-id cpu-001 --generation 0 --dp-bits 61 --max-records 10000 --max-steps 100000 --max-seconds 60 --checkpoint-steps 1000 --export-dp --resume
```

Preserve manifest, seed, worker/generation identity and DP settings across resume. The 61-bit density is a sizing heuristic, not a success estimate; 100,000 steps/60 seconds is a finite invocation budget, not a claim that #140 is feasible in that time. [Pinned standalone runner README](https://github.com/identity-md-launches/goal-3375-objective-solve-public-bitcoin/blob/45adea724172d45c2c8f18d69ff44df9acc26161/private-search/README.md)

For the claim component, the private candidate is exactly 32 big-endian bytes followed by EOF; RPC authentication is a separate entrant-supplied stream. The following templates require actual private files, an entrant-selected fee cap/target and an explicit loopback RPC URL. No credential, key, fee choice or txid is invented. Run the checker before preparing a claim, using a separately opened stream for each consumer:

```sh
python3 -I -B candidate-check/candidate_check.py --candidate-fd 4 \
  4< "${task_candidate_file:?set verified private candidate file}"

python3 -B private-claim/claim.py --rpc-url "${task_rpc_url:?set entrant loopback RPC URL}" \
  --rpc-auth-fd 3 --max-fee-sats "${task_cap_sats:?set authorized total fee cap}" \
  claim --candidate-fd 4 --fee-target "${task_fee_target:?set target blocks}" \
  3< "${task_auth_file:?set entrant private RPC auth file}" \
  4< "${task_candidate_file:?set verified private candidate file}"
```

Require checker exit 0 and its fixed production-verification result plus pinned identity/build checks; the command sequence is not an automatic integrated gate. Keep the candidate file unchanged between independent opens. A successful preparation still lacks the independent completeness proof discussed under BA-01. After all production prerequisites pass, the claim CLI's explicit `--broadcast` flag on the `claim` subcommand rebuilds/rechecks and submits. Use the resulting actual broadcast txid for confirmation, not a preparation txid:

```sh
python3 -B private-claim/claim.py --rpc-url "${task_rpc_url:?set entrant loopback RPC URL}" \
  --rpc-auth-fd 3 --max-fee-sats "${task_cap_sats:?set authorized total fee cap}" \
  verify --txid "${task_payment_txid:?set actual broadcast txid}" \
  --confirmations "${task_confirmation_depth:?set required depth}" \
  3< "${task_auth_file:?set entrant private RPC auth file}"
```

The claim API receives the secret during local signing, so its node/process boundary must be trusted. An acknowledged broadcast is not confirmation; after an uncertain send, check the announced txid before attempting another send. The `confirmed` result establishes only the checks that command performs, and must be combined with authenticated pre-spend coverage and independent active-chain verification. The integrated production relay and public mainnet evidence export remain missing. [b06-candidate-check]; [b10-boundary-audit]; [pinned claim README](https://github.com/identity-md-launches/goal-3375-objective-solve-public-bitcoin/blob/45adea724172d45c2c8f18d69ff44df9acc26161/private-claim/README.md)

**Evidence checks and reporting limits.** This write-up's public source reads completed at 2026-11-24T11:32:47Z. The browsing interface initially returned “Failed to fetch restricted URL” for the GitHub tree; the immediate required browser-user-agent curl retry returned HTTP 200, as did the Git tree API and selected raw files. This was a client limitation, not evidence that the repository was unavailable. No fresh mainnet snapshot was taken during the write-up; 11:03:36.975Z remains the latest supplied payment observation.

The source/data checks confirmed the final commit's replay files and published fixture hashes, the missing coordinator entry point, and the unresolved RCK manifest/adapter mapping. They do not certify solver behavior, secret custody, Linux portability, actual hardware, total billing, or mainnet payment. Earlier Git staging failures reported by component workers did not prove missing integration: the final merged commit and E5 replay provide the later evidence for landed components. Conversely, an artifact's presence or a worker's `done` label cannot overrule the explicitly stuck target board.

This report is the only newly written deliverable. Its validation checks enforce UTF-8 Markdown, a nonempty file below 64,000 bytes, the exact target/recipient and pinned revision, internally consistent integer totals and evidence references, and an untracked output path. The report-only bundle is below 8 MiB. The checked files do not turn an incomplete objective into a successful one. The missing real solution, real checkpoint, validated integrated private path, and confirmed exclusive-recipient payment are explicit; no success, payment, key, hardware capacity, or charge was fabricated.

**Handed evidence register.** IDs used above resolve to the original content-addressed worker results below. Each displayed SHA-256 was recomputed and matched the assignment pin. The two root merges summarize earlier overlapping results; they are not extra independent executions. `goal.json` refers to the supplied final orchestration state; its essential allocation, revision, failure and planning facts are preserved in this report. Exact hashes are integrity identifiers, not proof that a result's claims are true.

| Result ID | Original batch/item or merge | SHA-256 |
| --- | --- | --- |
| [root-1-01] | `root merge 1-01` | `85eda1327e8963416db3a023678672896fd26e87a8bb445115ad3e8dbbb0898c` |
| [root-1-02] | `root merge 1-02` | `12bd6a9297450631e207d039ffd55fb2fbaa4fe05b2a4fd4d6ae9b5cff266b1d` |
| [b14-offline-replay] | `e5-merged-evidence/offline-replay` | `a159fc1c3358538f3145585d614f8133d7a77400cff100abe742612a49811b97` |
| [b15-challenge-and-prize] | `e5-payment-state/challenge-and-prize` | `d9525190eb2ec5687fe747b091ac4db1e8a48fc29b7ea3ca465d1fe839240d5c` |
| [b11-inventory-verdict] | `e4-evidence-tools/inventory-verdict` | `d67784377301ca2034dab23ca839479c3352d81c1bcc70339776238d91f114cc` |
| [b11-fee-policy] | `e4-evidence-tools/fee-policy` | `29aa135a4a2a60d5771bd55643d5089c7035526153e0ad34c2b5e46a133519d7` |
| [b11-toy-trial-restart] | `e4-evidence-tools/toy-trial-restart` | `02ed9bda6b5652095adea0fc3435e3c9b6e92c891ba51952c6e803fbbab5e84d` |
| [b11-regtest-reproduction] | `e4-evidence-tools/regtest-reproduction` | `9851e9553b9f66ce0438495c3a18b93ec0af136ebf6393d11b6a25b8e36e4fbf` |
| [b12-challenge-and-prize] | `e4-funding-evidence/challenge-and-prize` | `6e09a62a9e302c039ce1733951a501367bb81af8297d2a574016127e7c1629c2` |
| [b13-boundary-audit] | `e4-source-inventory/boundary-audit` | `597d32fe7f5a53f7ea319d4e2b57b7aaed9f5e7183bdc25f5cce052132ba01cc` |
| [b09-challenge-and-prize] | `e3-public-state/challenge-and-prize` | `69c5e9a026691b5eac276bc76d0e41881497fcc729c01f2b223e82e6800015f4` |
| [b10-boundary-audit] | `e3-private-path-audit/boundary-audit` | `88889f6747e50fe9dcc0d93e593ce3d42e7dd53e354cc0037fa0d97eefb51953` |
| [b08-receipt-integration] | `e3-private-runner/receipt-integration` | `5f4125a23ed911917750012596dd55690872da54734666f41ab31b2921709f13` |
| [b08-claim-core] | `e3-private-runner/claim-core` | `16a34d1e597a2c9569188a972c43ae5e4d48345b1d8e3ba2d72f61668ab671f8` |
| [b08-search-engine] | `e3-private-runner/search-engine` | `fa3c8b1ba5a463d8dcae0f961e9c64c433307ec7da7add3237a48f27990b77ec` |
| [b08-coordinator] | `e3-private-runner/coordinator` | `19391104f851510d351a7b5557a5a6947db17e5666b81c054f4d32ffd8f068f7` |
| [b08-rck-sink] | `e3-private-runner/rck-sink` | `6e10c41f67ae1bf3a587de5580791adbeeede1a262f86656268518aaab5207ff` |
| [b08-native-comparator] | `e3-private-runner/native-comparator` | `518b5d86ce51a747c20e173baac9ee451225bd540768beb79047e412d5897ab0` |
| [b08-toy-regressions] | `e3-private-runner/toy-regressions` | `4b9ffb3a09b3e9c8de50e7edb27251b9dc34367c7fc76032859893bebbc2f56d` |
| [b08-ecdsa-regressions] | `e3-private-runner/ecdsa-regressions` | `8980f4c6e9d5098f60e6da3b014df0d03fdf03c3d356841971970515f9b2ccb2` |
| [b06-private-search] | `e2-runner-components/private-search` | `1d491988e975b5d77b4c81a5d168f6939f7a8809f6f3812e7434a592835f33e3` |
| [b06-regtest-offline] | `e2-runner-components/regtest-offline` | `ac9224b87dc5fd2c2964eee8be35ecb2184a968285f1cc455f64beb5a493f864` |
| [b06-receipt-hardening] | `e2-runner-components/receipt-hardening` | `dc8eefc1dd51512d2b73af6467ade962f8e2871bde818af920a0a9d20a683eeb` |
| [b06-secp-oracle] | `e2-runner-components/secp-oracle` | `1c0fd9c0e5a6413ec7f12122405569e1364e5a596f2aa372371f2b3f0ad0ffed` |
| [b06-candidate-check] | `e2-runner-components/candidate-check` | `3b0aadbb1397eb6513b6bbe40cbc73d5b3cf44d97d6e116a9cc0c7fdd15ef7f2` |
| [b07-private-path-review] | `e2-focused-reviews/private-path-review` | `798d6dbead22c8e76f140183cf06d987e037ca1848fea9e73045da3b0450301b` |
| [b07-theory-recheck] | `e2-focused-reviews/theory-recheck` | `ed20c79667140dfba0fc329d9c761135f55741210af385bd18c8c4513790ca4b` |
| [b04-work-estimate] | `method-evidence/work-estimate` | `75da15f63c247e47969190c09dfcedd305041a66ca7012d080b16bdf7b1e34cc` |

[root-1-01]: https://api.imd.fun/artifacts/85eda1327e8963416db3a023678672896fd26e87a8bb445115ad3e8dbbb0898c
[root-1-02]: https://api.imd.fun/artifacts/12bd6a9297450631e207d039ffd55fb2fbaa4fe05b2a4fd4d6ae9b5cff266b1d
[b14-offline-replay]: https://api.imd.fun/artifacts/a159fc1c3358538f3145585d614f8133d7a77400cff100abe742612a49811b97
[b15-challenge-and-prize]: https://api.imd.fun/artifacts/d9525190eb2ec5687fe747b091ac4db1e8a48fc29b7ea3ca465d1fe839240d5c
[b11-inventory-verdict]: https://api.imd.fun/artifacts/d67784377301ca2034dab23ca839479c3352d81c1bcc70339776238d91f114cc
[b11-fee-policy]: https://api.imd.fun/artifacts/29aa135a4a2a60d5771bd55643d5089c7035526153e0ad34c2b5e46a133519d7
[b11-toy-trial-restart]: https://api.imd.fun/artifacts/02ed9bda6b5652095adea0fc3435e3c9b6e92c891ba51952c6e803fbbab5e84d
[b11-regtest-reproduction]: https://api.imd.fun/artifacts/9851e9553b9f66ce0438495c3a18b93ec0af136ebf6393d11b6a25b8e36e4fbf
[b12-challenge-and-prize]: https://api.imd.fun/artifacts/6e09a62a9e302c039ce1733951a501367bb81af8297d2a574016127e7c1629c2
[b13-boundary-audit]: https://api.imd.fun/artifacts/597d32fe7f5a53f7ea319d4e2b57b7aaed9f5e7183bdc25f5cce052132ba01cc
[b09-challenge-and-prize]: https://api.imd.fun/artifacts/69c5e9a026691b5eac276bc76d0e41881497fcc729c01f2b223e82e6800015f4
[b10-boundary-audit]: https://api.imd.fun/artifacts/88889f6747e50fe9dcc0d93e593ce3d42e7dd53e354cc0037fa0d97eefb51953
[b08-receipt-integration]: https://api.imd.fun/artifacts/5f4125a23ed911917750012596dd55690872da54734666f41ab31b2921709f13
[b08-claim-core]: https://api.imd.fun/artifacts/16a34d1e597a2c9569188a972c43ae5e4d48345b1d8e3ba2d72f61668ab671f8
[b08-search-engine]: https://api.imd.fun/artifacts/fa3c8b1ba5a463d8dcae0f961e9c64c433307ec7da7add3237a48f27990b77ec
[b08-coordinator]: https://api.imd.fun/artifacts/19391104f851510d351a7b5557a5a6947db17e5666b81c054f4d32ffd8f068f7
[b08-rck-sink]: https://api.imd.fun/artifacts/6e10c41f67ae1bf3a587de5580791adbeeede1a262f86656268518aaab5207ff
[b08-native-comparator]: https://api.imd.fun/artifacts/518b5d86ce51a747c20e173baac9ee451225bd540768beb79047e412d5897ab0
[b08-toy-regressions]: https://api.imd.fun/artifacts/4b9ffb3a09b3e9c8de50e7edb27251b9dc34367c7fc76032859893bebbc2f56d
[b08-ecdsa-regressions]: https://api.imd.fun/artifacts/8980f4c6e9d5098f60e6da3b014df0d03fdf03c3d356841971970515f9b2ccb2
[b06-private-search]: https://api.imd.fun/artifacts/1d491988e975b5d77b4c81a5d168f6939f7a8809f6f3812e7434a592835f33e3
[b06-regtest-offline]: https://api.imd.fun/artifacts/ac9224b87dc5fd2c2964eee8be35ecb2184a968285f1cc455f64beb5a493f864
[b06-receipt-hardening]: https://api.imd.fun/artifacts/dc8eefc1dd51512d2b73af6467ade962f8e2871bde818af920a0a9d20a683eeb
[b06-secp-oracle]: https://api.imd.fun/artifacts/1c0fd9c0e5a6413ec7f12122405569e1364e5a596f2aa372371f2b3f0ad0ffed
[b06-candidate-check]: https://api.imd.fun/artifacts/3b0aadbb1397eb6513b6bbe40cbc73d5b3cf44d97d6e116a9cc0c7fdd15ef7f2
[b07-private-path-review]: https://api.imd.fun/artifacts/798d6dbead22c8e76f140183cf06d987e037ca1848fea9e73045da3b0450301b
[b07-theory-recheck]: https://api.imd.fun/artifacts/ed20c79667140dfba0fc329d9c761135f55741210af385bd18c8c4513790ca4b
[b04-work-estimate]: https://api.imd.fun/artifacts/75da15f63c247e47969190c09dfcedd305041a66ca7012d080b16bdf7b1e34cc
