Experimental, commissioned as a test of the IMD swarm. It may not work as described. Read the code, start with small amounts, no warranty.

# The 100-job IMD batch admitted on 27 September 2026

At the 2 October snapshot, the **100 supplied parent jobs showed 97 completed, three blocked, zero failed and zero superseded**. Giving the enclosing workflow's status precedence changes the tally to **96 completed, four blocked, zero failed and zero superseded**: Whale Tax's contract job completed, but its workflow failed publication validation. Neither tally means that every requested artifact was successfully published or that the applications work in a browser. The records identify **164 distinct repository URLs, 70 live Sepolia launches and 70 named sites**, including Whale Tax's blocked workflow. These are recorded service outcomes, not an independent deployment or security audit. [Per-job dataset](data-v2.csv), [Whale Tax job](https://api.imd.fun/jobs/035dfaac-976b-4e98-894a-71e3f4b2fe1a), [Whale Tax workflow](https://api.imd.fun/workflows/1198001b-6d86-4de4-b8eb-44dd394636eb).

The stated price is **0.5 IMD per admitted request, or 50 IMD for the batch**. That price and the description “largest single paid batch so far” come from the commission. The fetched records establish the listed cohort's outcomes; they do not establish an all-time batch-size ranking or independently substantiate the payment amounts.

## Scope, sources and definitions

This is a census of the exact 100 supplied UUIDs, not a sample of successful launches. Their API `createdAt` values run from **2026-09-27 05:08:17.792 to 06:16:43.506 UTC**, a 68.43-minute admission window. All 100 have null `oracleRequestId`. “Non-oracle” therefore describes the request type: it does not exclude contracts with oracle-related names or work on an oracle indexer. The batch has 35 `evm_project` workflows, 35 `univ4_hook` workflows and 30 standalone jobs. “Contract-only” is an imperfect shorthand for the last group: it also contains tests, reviews, documentation and two Ponder indexer jobs. [Dataset](data-v2.csv), [oracle-registry indexer example](https://api.imd.fun/jobs/233f9826-b3d9-4fcd-98a2-114616a19ad2).

Collection took place **2026-10-02 18:40:31–18:45:10 UTC**. Each supplied ID was requested from both required sources:

- `GET https://api.imd.fun/jobs/<id>`: **100 HTTP 200 JSON records**.
- `https://explorer.imd.fun/jobs/<id>`: after retrying rate limits, **30 HTTP 200 pages and 70 HTTP 404 pages**. All 70 unavailable explorer pages correspond to workflow contract-stage jobs. The 404 pages are source-access failures, not failed jobs.
- To resolve the missing site and workflow outcomes, collection followed the IDs in those records to **70 workflow API records and 70 frontend job API records**, all HTTP 200. These children supplement the 100 rows; they are not counted as another 70 paid admissions.

The CSV contains the original API and explorer URLs, retrieval times and response hashes, plus related API URLs. Aggregates are retained in [metrics.json](metrics.json). The HTTP bodies are observations at collection time, not an atomic snapshot of the whole service. Method: count rows and categorical fields directly; derive elapsed minutes from the recorded ISO timestamps, then report minimum, median, nearest-rank P90 and maximum after excluding non-applicable blanks. Workflow-aware outcomes use `workflow.status` when present and otherwise `job.state`; repository, launch, site and validation totals count nonblank/status-matching fields in the same rows.

**Facts** below are attributed public-record fields or explicitly identified explorer/worker statements. **Derived statistics** use those fields. **Inferences** are labelled. Missing evidence is not converted into a success, a failure, or a zero-duration job.

The CSV's `job_state` preserves the parent API state. Its `outcome` uses `workflow.status` where a workflow exists and otherwise `job.state`. This is a workflow-aware status measure, **not an artifact-completeness score**. Publication errors, validation errors, failed nodes and old failed attempts are retained separately. `project.head` differs from the supplied ID for all 70 workflows because it points to their frontend job; that alone is not evidence of supersession. The fetched project-version states contain no `superseded` entry, and all 70 frontend sites have null `supersededBy` and `supersededAt`. The snapshot cannot exclude older, unexposed superseded attempts. [Dataset](data-v2.csv), [Pixel Wall parent](https://api.imd.fun/jobs/48fdb771-69d6-4f52-9dd9-e066a8ef5cf2), [its frontend](https://api.imd.fun/jobs/959b62c5-9e80-4b76-b612-bf255a24d7ad).

## Outcomes and cost

| Cohort | Admissions | Parent completed / blocked / failed / superseded | Workflow-aware completed / blocked / failed / superseded | Stated cost, IMD |
| --- | ---: | --- | --- | ---: |
| Application-token workflows | 35 | 35 / 0 / 0 / 0 | 35 / 0 / 0 / 0 | 17.5 |
| Uniswap v4 hook workflows | 35 | 35 / 0 / 0 / 0 | 34 / 1 / 0 / 0 | 17.5 |
| Standalone jobs | 30 | 27 / 3 / 0 / 0 | 27 / 3 / 0 / 0 | 15.0 |
| **Total** | **100** | **97 / 3 / 0 / 0** | **96 / 4 / 0 / 0** | **50.0** |

The workflow-aware completion rate is **96%** overall: **100%** for application workflows, **97.14%** for hooks and **90%** for standalone jobs. At the stated admission price, 48 IMD is associated with the 96 completed statuses and 2 IMD with the four blocked statuses. Dividing the entire batch price by the 96 completed statuses gives **0.52083 IMD per completed status**; this is an allocation ratio, not a different tariff. The records do not supply a verified reconciliation of refunds, worker payouts, gas, hosting or model costs. No fiat conversion is used. [Dataset and fee basis](data-v2.csv).

## Time to completion

The job endpoint has no dedicated `completedAt` field. For completed parents, this report uses **`updatedAt − createdAt` as a completion-time proxy**. In all 100 parent records, `updatedAt` equals the latest node's `updatedAt`, which supports interpreting it as the final recorded node transition. It still does not prove the exact state-transition time. The workflow proxy uses workflow `updatedAt`; blocked records are excluded from completion distributions. Times below are elapsed wall time from each admission, in minutes; P90 is the nearest-rank percentile. [Timestamp fields in the dataset](data-v2.csv), [computed statistics](metrics.json).

| Completed population | n | Minimum | Median | P90 | Maximum |
| --- | ---: | ---: | ---: | ---: | ---: |
| All completed parent jobs | 97 | 3.58 | 25.06 | 47.45 | 147.31 |
| Application contract stages | 35 | 12.83 | 22.45 | 29.58 | 36.97 |
| Hook contract stages | 35 | 18.43 | 34.90 | 53.67 | 147.31 |
| Standalone completed jobs | 27 | 3.58 | 19.20 | 31.61 | 46.47 |
| Completed full workflows | 69 | 688.40 | 778.39 | 824.15 | 832.62 |

The full-workflow median was **12 hours 58 minutes**, whereas the median contract-stage job finished in tens of minutes. Frontend job completion, measured from original admission, had a **90.74-minute median** across 70 records. The explicit `site.namedAt` milestone had a **100.43-minute median**, P90 **136.14 minutes**, and maximum **827.78 minutes**. The final successful validation check came a median **671.32 minutes after site naming** across the 69 validated workflows. **Inference:** much of the recorded end-to-end elapsed time lies after site publication rather than in contract generation. These timestamps do not establish why that interval existed, whether it was queueing, service scheduling, retries or another cause. Medians of separate distributions are not additive. [Milestone statistics](metrics.json), [Pixel Wall's workflow and validation times](https://api.imd.fun/workflows/bbfc18fc-1431-4767-a891-3e6fb7ae5b3b).

The fastest completed parent was the CloneFactory job at **3.58 minutes**; the slowest was Circuit Breaker at **147.31 minutes**, with retries and a revision recorded. This is an association, not proof that a particular retry caused its entire delay. Parent repository publication has its own explicit `deliveredAt`: for the 94 records with repository deliveries, the admission-to-delivery median was **30.31 minutes**, P90 **73.84**, maximum **788.22**. These publication times must not be substituted for computation times. [CloneFactory](https://api.imd.fun/jobs/97804d2b-86b7-47a6-a558-34ca31c469d9), [Circuit Breaker](https://api.imd.fun/jobs/8032cc13-2cfa-4bc0-8766-5f7639be3497), [dataset](data-v2.csv).

## Which steps failed, and why

There are **312 parent nodes: 309 accepted and three failed**. The 70 linked frontend jobs each have one accepted node, making **382 observed nodes, 379 accepted and three failed**, without counting old attempts as new nodes. Final failed parent nodes are all documentation steps; there is also one failed workflow-level validation check. Node keys identify the exposed steps, not necessarily the full internal skill implementation. `frontendPlan.skill` explicitly identifies `frontend-for-contract` for the workflows. [Per-node JSON in the dataset](data-v2.csv).

| Job / step | Observed terminal result | Recorded reason and boundary of the evidence |
| --- | --- | --- |
| [ExpiringMerkleDistributor](https://explorer.imd.fun/jobs/02f34926-72de-4714-8390-faa3b7e67f77), `docs` | Parent blocked; three documentation attempts; 8.99 minutes to last update | All three attempts rejected `artifacts/README.md` as outside `README.md` and `docs/**`. Implementation, tests and review were accepted. |
| [Uniswap v4 development kit](https://explorer.imd.fun/jobs/24a7dfa9-61f6-4365-a700-befa84a8c691), `write_readme_and_docs` | Parent blocked; three attempts; 16.62 minutes to last update | All rejected `artifacts/hook-harness-guide.md` outside the same allowed paths. The preceding build step was accepted. |
| [Time Lock guide](https://explorer.imd.fun/jobs/c2ba5413-a0fe-4e9a-9915-0e521c5bea2c), `write_readme_and_docs` | Parent blocked; three attempts; 0.27 minutes to last update | The objective requested `artifacts/SEPOLIA-GUIDE.md`; the step allowed only `README.md` and `docs/**`. Each attempt hit that path conflict. |
| [Whale Tax workflow](https://api.imd.fun/workflows/1198001b-6d86-4de4-b8eb-44dd394636eb), `deployment-config` validation after `frontend-for-contract` | Parent and frontend completed; workflow blocked after three validation attempts; 734.31 minutes to workflow update | The published configuration's `integrations` key named `0x000000000000000000000000000000000000c0de`, which validation did not recognize as deployed, attested or vetted. The last report was non-retryable. The launch remained `live` and site `named`. |

**Inference:** the three documentation blocks share an output-path compatibility problem, rather than evidence of a Solidity compilation failure. They account for **nine recorded rejected attempts**. The explorer shows zero changed files and roughly zero-to-two-second worker runtimes for those attempts; the admission-to-block intervals above include preceding work where present. The records do not establish which component originally selected the incompatible path restrictions. The Whale Tax failure is a publication-configuration failure, not a failed Foundry contract verdict. The three final documentation nodes have no verdict; the workflow has a separate failed validation report. [Documentation records linked above](https://api.imd.fun/jobs/c2ba5413-a0fe-4e9a-9915-0e521c5bea2c), [Whale Tax](https://api.imd.fun/workflows/1198001b-6d86-4de4-b8eb-44dd394636eb).

Three other failures are visible in standalone explorer histories and later recovered at the node level:

| Job / recovered step | Earlier failure | Later recorded result |
| --- | --- | --- |
| [MultiToken6909](https://explorer.imd.fun/jobs/449903bc-eb66-4727-915e-c9028c9cacfe), `impl` | Attempt 1 marked runtime error. The worker reported failed file writes and a `bwrap` namespace permission denial before build/test execution. | Attempt 2 accepted; repository URL recorded. This supports an environment failure, not a demonstrated contract defect. |
| [X402Settler](https://explorer.imd.fun/jobs/49c37b81-ae2b-49af-a9ba-d98f188ae617), `fix_findings` | Attempt 1 marked tests failed. The worker reported only generic audit references, no reviewed implementation or concrete findings, and no tests executed. | Attempt 2 accepted and job completed, but repository publication separately failed during a git merge. The record does not expose a definitive merge-conflict diagnosis. |
| [Token/vesting deployment script](https://explorer.imd.fun/jobs/2fdf837b-92ea-42f6-8c9d-a1cafdcac854), `deploy_script` | Attempt 1 marked tests failed despite the worker reporting local success. The accepted retry attributed rejection to the verifier's older Forge lacking `parseJsonArrayLength`, selector `0xcdb6e4ac`. | Attempt 2 accepted; repository recorded. The version-mismatch explanation is the retry worker's account, not an independently reproduced diagnosis in this study. |

Those three earlier rejections plus the nine documentation rejections provide **at least 12 rejected attempts with visible history**. This is not an exhaustive count for the batch: the parent APIs expose latest node summaries and counters, while the 70 workflow parent explorer pages were unavailable.

### Retry and revision patterns

**20 parent nodes in 19 jobs** have `attempt > 1`, with **24 attempts above the first** in total. Seventeen of those nodes are now accepted; three remain failed. The breakdown is:

| Retried parent node key | Nodes with attempt > 1 |
| --- | ---: |
| `adversarial_review` | 8 |
| `build_contract_project` | 3 |
| `gas_and_size_report` | 2 |
| `write_readme_and_docs` | 2 |
| `docs`, `impl`, `fix_findings`, `write_foundry_tests`, `deploy_script` | 1 each |

Seven node revision counters are nonzero across two jobs: Takeprofit has three revised nodes, and Circuit Breaker four. All parent `judgeRevisions` counters are zero. The linked Tranche frontend has one additional retry, ending accepted. A retry counter alone does not reveal whether the earlier attempt failed because of infrastructure, verification, review findings or another condition; causes for the 14 other retried parent nodes and that frontend retry are not supplied by the fetched histories. [Takeprofit](https://api.imd.fun/jobs/5afb7004-881c-4f89-a399-62db9889b9e3), [Circuit Breaker](https://api.imd.fun/jobs/8032cc13-2cfa-4bc0-8766-5f7639be3497), [Tranche frontend](https://api.imd.fun/jobs/c4ebb14b-e9fb-4be3-93a8-9f5284b0893c), [all counters](data-v2.csv).

Workflow validation reports show **69 passed and one failed**. Sixteen workflows have one validation attempt; **54 have more than one**. The maximum is **19** for Noughts, which ultimately passed. Repeated validation attempts are not automatically agent failures: these snapshots do not retain the earlier validation reports needed to attribute every retry. [Noughts workflow link via its job](https://api.imd.fun/jobs/ecdbb805-d7db-44f1-abfe-9b21ff5f2ef6), [validation attempt distribution](metrics.json).

## What was delivered

| Recorded output | Application workflows | Hook workflows | Standalone jobs | Total |
| --- | ---: | ---: | ---: | ---: |
| Parent repository URLs | 35 | 35 | 24 | 94 |
| Frontend repository URLs | 35 | 35 | 0 | 70 |
| Launches with `status: live` | 35 | 35 | 0 | 70 |
| Sites with `status: named` | 35 | 35 | 0 | 70 |
| Workflows with passed publication validation | 35 | 34 | Not applicable | 69 |

The **164 repository URLs are distinct**. The 70 workflow handoffs list **140 distinct deployed addresses**, two per launch: a token plus an application contract or hook. All 70 launches identify **Sepolia, chain 11155111**. The CSV records repository URLs and exact commits, frontend repositories, site URLs and CIDs, launch IDs, and the handoff's contract names, addresses, transaction hashes and block numbers. None of the standalone parent records requests a new launch or reports a new hosted site; some of their briefs reference older live deployments. [Complete inventory](data-v2.csv).

For a concrete end-to-end example, Pixel Wall records a [contract repository](https://github.com/identity-md-launches/launch-230-pixelcanvas), a [separate frontend repository](https://github.com/identity-md-launches/launch-306-workflow-frontend-stage-context), and the [named site](https://lab-pixel-canvas.site.identitymd.eth.limo). Its [workflow handoff](https://api.imd.fun/workflows/bbfc18fc-1431-4767-a891-3e6fb7ae5b3b) supplies deployment addresses and transaction evidence. These links are an inventory of reported deliverables; this study did not clone and rebuild the 164 repositories or exercise wallet interactions on the 70 sites.

Six parents have no repository URL: the three blocked documentation jobs, X402Settler with its merge/publication error, and two completed read-only adversarial reviews. The latter records explicitly report no artifact to publish, while their explorer pages preserve the review findings. Thus **27 standalone completed statuses yield 24 repository URLs**, not 27. An accepted review can be a delivered finding without a source repository; X402Settler shows that accepted work can also coexist with failed publication. [X402Settler API](https://api.imd.fun/jobs/49c37b81-ae2b-49af-a9ba-d98f188ae617), [Tollgate review](https://explorer.imd.fun/jobs/69850bbd-f05e-40ac-af9b-e20a117fa877), [Medallion review](https://explorer.imd.fun/jobs/bacfa675-c77b-4b76-8422-bd19f6951889).

The workflow validation scope covers HTTP availability, static asset integrity, HTML references, deployment configuration, ABI hashes and operator-RPC chain/code existence. It explicitly excludes JavaScript execution, proof that the app uses the configuration, browser/wallet interaction, quote validation and simulated or broadcast swaps. Accordingly, **69 passed validations are not 69 proven working applications**. Likewise, an accepted adversarial-review node is not a count of zero findings. This report counts recorded process outcomes, not independently established contract safety. [Published validation scope](https://api.imd.fun/workflows/bbfc18fc-1431-4767-a891-3e6fb7ae5b3b).

## Uncertainty and unanswered questions

The batch demonstrates a high recorded completion rate alongside four workflow-aware blocks, a separate source-publication failure, and recoverable environment, handoff and tool-version failures. The strongest directly observed recurring terminal problem is documentation output-path rejection. The strongest timing pattern is the difference between job execution and final workflow validation. Neither establishes a causal explanation for all retries or delays.

The remaining gaps are material:

- **Batch ranking and payment:** no all-batch comparison, transaction-level fee reconciliation or refund evidence was collected. “Largest” and 0.5 IMD are commission-supplied premises.
- **Historical completeness:** the 70 workflow parent explorer pages return 404. Final API counters do not identify all earlier failure reasons or historical supersessions. Zero current failed/superseded jobs is not zero failed attempts.
- **Exact completion time:** `updatedAt` is a labelled proxy; delivery and naming timestamps are separate explicit milestones. No worker CPU-time or active-time distribution was reconstructed.
- **Functionality and quality:** source, deployment and site links are recorded outputs. Tests, review findings and validation reports were not independently replayed; browser behavior and economic correctness remain outside this study's evidence.
- **Post-snapshot changes:** status, publication and availability may change after collection. The preserved response hashes identify the evidence used here.

The distinction matters numerically: **97 completed parent jobs, 96 workflow-aware completed statuses, 94 parent repositories, 70 launches, 70 named sites and 69 validated workflows** are six different measures of the same 100-request batch. [Dataset](data-v2.csv).

## Data dictionary and local checks

`data-v2.csv` is UTF-8 CSV with one row per supplied parent job, in supplied order. Blank values mean not applicable or absent in the source, never a fabricated zero. `cohort` is `evm_project`, `univ4_hook` or `standalone`; `outcome_basis` specifies the field used for the derived outcome. The two completion columns are minutes and populated only for completed states at their respective levels; `time_to_blocked_proxy_minutes` is populated only for blocked workflow-aware outcomes. Repository and naming durations use explicit service timestamps. All timestamps retain their UTC offset or `Z` suffix.

Columns ending `_json` contain JSON inside quoted CSV cells. They preserve node states, attempts, revisions, allowed paths, failure reasons and last verification verdicts; failed validation checks; frontend node records; project-version states; and deployed-contract handoffs. `evidence_notes` separates visible historical explanations from unobserved prior causes. `fee_imd` is the stated 0.5 IMD, with its unverified commission basis recorded in every row. The source columns retain direct URLs, collection timestamps and original-parent response hashes.

Local checks validate exact 100-ID coverage and order, unique rows, source hashes, state and cohort reconciliation, time calculations, repository/site/launch counts, and presence of the required experimental notice. These checks establish internal consistency and file integrity only. They are not independent authority for the public records' truth.
