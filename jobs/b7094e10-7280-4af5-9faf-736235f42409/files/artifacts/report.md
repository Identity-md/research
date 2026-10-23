# Judge decision: test LP Desk before issuing a token

## 1. Question restated

Which of the four reports’ ideas should IMD or CLAUS build first, which moonshot deserves further research, and, if no launch is ready, what single experiment should resolve the next decision within fourteen days?

**Inference — read 2026-10-24:** None is ready for a public launch. Commission one **LP Desk consent-to-fee experiment**, derived from Open Lane, with a fork implementation and independent LP buying decision. Keep **Agent First Opening’s private, portable agent credential** as the research moonshot. Do not order a deployment from this judgment.

### Evidence convention and scope

All observations and judgments in this report have **read date 2026-10-24 UTC**. **Record** means directly retrieved content, API fields or inspected source; it does not certify the publisher’s economics or honesty. **Claim** means an assertion by a report, operator or project not independently demonstrated here. **Inference** covers scores, calculations, design choices and decision thresholds. A paragraph/table label applies to every figure in it. Section numbers, citation identifiers and ordering numbers are navigation, not measurements. Historical dates are distinguished from this review’s read date.

The reports were retrieved in full from their supplied URLs. References: [R1 Fee to Jobs](https://github.com/Identity-md/research/blob/main/jobs/dd378ca2-5133-464f-8e44-3e44bf8a5ba7/files/artifacts/report.md), [R2 Agent First Opening](https://github.com/Identity-md/research/blob/main/jobs/59734b38-c408-49f9-9354-a0bf6f304991/files/artifacts/report.md), [R3 Claus Crew](https://github.com/Identity-md/research/blob/main/jobs/aaeb3958-5818-4350-b441-a03bd8d28c80/files/artifacts/report.md), [R4 Open Lane](https://github.com/Identity-md/research/blob/main/jobs/f85fdd08-1c07-4c3f-a5e3-98b52847e411/files/artifacts/report.md). Their earlier observations are not silently promoted to current chain facts.

**Record:** This assignment retrieved sources and inspected code; it placed no paid orders, deployed no contracts, and broadcast no transactions. It did not reproduce the reports’ trading-volume census, signatures, worker payouts or fork tests. The accompanying [SPEC](SPEC.md) specifies future work, not completed software. Source-access failures limit this judgment; the local document checks are not independent research certification.

## 2. Random citation audit

**Record:** Before evaluating citation outcomes, the review sampled distinct inline Markdown citation URLs, preserving first-appearance order, using Python `random.Random(seed).sample` without replacement within each report. The recorded random seed is `041e38506d15455199d905f277797101`. Population sizes were **56, 46, 43 and 39** URLs respectively; each sample has **5** URLs. Repeated citations have one chance per report; therefore this is a URL-level sample, not a random sample of every factual claim. No failures were replaced. The [audit manifest](../evidence/citation-audit.json) retains populations, indices, report SHA-256 hashes, fetch outcomes and scoped findings for reproduction.

**Inference — classification rule:** **Confirmed** means the source supports the specified narrow assertion; for marketing material, that can establish only that the publisher makes the claim. **Wrong** means the cited content contradicts that assertion. **Unreachable** means access prevented checking it, not that the assertion is false. A successful HTTP response alone never counts as confirmation. Neither a confirmed README nor a verified source listing establishes adoption or safe deployed behavior.

All entries below are **Record of the citation check**; underlying publisher claims are explicitly identified.

### Fee to Jobs

| Sample | Citation / assertion checked | Result | Evidence and limit |
|---|---|---|---|
| F1 | [Robinhood RPC](https://rpc.mainnet.chain.robinhood.com): historical block-window anchor in §6 | **Unreachable** | GET returned HTTP 400; correctly formed read-only JSON-RPC POST returned HTTP 403. No historical blocks or volume confirmed. |
| F2 | [Dongle pinned tree](https://github.com/identity-md-launches/launch-2474-dongle/tree/de317a1501fcc8032672f55430028a74cdfeccf5): source provenance in §13 | **Confirmed** | Tree resolves; [commit API](https://api.github.com/repos/identity-md-launches/launch-2474-dongle/commits/de317a1501fcc8032672f55430028a74cdfeccf5) returns that SHA and committer date 2026-10-22. No deployment/volume inference. |
| F3 | [IMDirector launch](https://api.imd.fun/launches/5992ada2-68e1-4af2-ad6d-47d67e09f703): launch reward record in §5 | **Confirmed** | Launch 2418, chain 4663, live status, source commit and accepted-work roles appear in `rewardSnapshot`. Operator record; not proof of per-job wages or separate beneficial owners. |
| F4 | [YOLO launch](https://api.imd.fun/launches/a3cf5033-4522-4a83-bd9c-584be10351fc): pool/source provenance used in §6 | **Confirmed** | Launch 2364, chain 1, source commit and seeded factory position match its source directory. The sampled-day swaps and fee estimates were not remeasured. |
| F5 | [Verified project factory](https://sourcify.dev/server/v2/contract/1/0xff03410d0fe5fa8f7f59f743de35e333d9857120?fields=all): collection/split rule in §6 | **Confirmed** | Sourcify runtime match; `PoolFees` collects a seeded position and `LaunchFees.REQUESTER_BPS` is 8000. The share is of that position’s collected fees, not all fees paid anywhere in the pool. |

### Agent First Opening

| Sample | Citation / assertion checked | Result | Evidence and limit |
|---|---|---|---|
| A1 | [Reputation batch receipt](https://etherscan.io/tx/0x0d6a5212b354fc5e0195e5d7d3bc97cf8da670b49588f4b216331d9a14bd97ca): landed feedback in §5 | **Unreachable** | Direct HTTP 403; browser retrieval also inaccessible. Emitter, status and block not confirmed. |
| A2 | [Flaunch API](https://docs.flaunch.gg/references/api): currently offered temporary wallet cap in §2/§3 | **Wrong** | The page says fair launch and sniper protection are paused; enabling inputs are rejected. It describes a 0.25%-of-supply cap **when active**. Correct comparison: documented capability, currently unavailable through this API; no conclusion about every other Flaunch route. |
| A3 | [First same-owner registration receipt](https://etherscan.io/tx/0xfd6965a3e4d1f1d092f86ef509bcac50bf9141850154b1c10f71457069b7895b) in §5 | **Unreachable** | Direct HTTP 403 and inaccessible browser retrieval. Neither registration nor owner confirmed. |
| A4 | [Third same-owner registration receipt](https://etherscan.io/tx/0xa6adbcb75e3543b695ae95b88afb92d091b72ac78691c8a2bf5ca276ec12fd3e) in §5 | **Unreachable** | Same failures. The report’s ownership concentration measurements remain its claims in this judgment. |
| A5 | [IMD capabilities](https://api.imd.fun/requests/capabilities): prices, cadence and test target | **Confirmed** | Advertises 0.5 IMD per job/launch; oracle/job interval floors 10/30 minutes; Sepolia hook-launch target. Configuration is not fulfillment or admission of this hook. |

### Claus Crew

| Sample | Citation / assertion checked | Result | Evidence and limit |
|---|---|---|---|
| C1 | [Pinned IHooks](https://github.com/Uniswap/v4-core/blob/bea7f6d1c11cd5dc4f0d5151ffa37a1c239feee6/src/interfaces/IHooks.sol): callback interface in §4 | **Confirmed** | Named swap/liquidity callbacks and caller `sender` exist. Paired [Hooks library](https://github.com/Uniswap/v4-core/blob/bea7f6d1c11cd5dc4f0d5151ffa37a1c239feee6/src/libraries/Hooks.sol) defines permission bits. Not a verification of CLAUS’s deployed callback behavior. |
| C2 | [Official registry README](https://github.com/erc-8004/erc-8004-contracts/blob/b9e466c250744a7e06b13dff9d3c2844ed64f825/README.md): deployment list in §7 | **Confirmed** | Ethereum/Robinhood identity and reputation entries exist; no ValidationRegistry address appears in its deployment section. Validation source concepts elsewhere do not provide a deployment address. No fresh live registry-code check performed. |
| C3 | [Compute collector source](https://sourcify.dev/server/v2/contract/1/0xa25ca2d2521aa47b6cc84b28be66e8fc7a1b768e?fields=all): fixed-recipient claim in §5 | **Confirmed** | Exact-match source makes `active` immutable; `claimActive` redeems existing manager claims and `unlockCallback` sends to `active`. A deterministic keeper can invoke it. |
| C4 | [POD pinned README](https://github.com/nel349/pod/blob/a9ed4f75f7ee44417e90754d584f340423a8b749/README.md): testnet acceptance/refusal pattern in §3 | **Confirmed** | Publisher describes Monad testnet and later poster acceptance/refusal. Confirmed as a claim; no independent payout/controller or production check. |
| C5 | [IMD capabilities](https://api.imd.fun/requests/capabilities): unit costs/cadence in §6 | **Confirmed** | Same advertised price and interval fields as A5. Not evidence of worker compensation or capacity. |

### Open Lane

| Sample | Citation / assertion checked | Result | Evidence and limit |
|---|---|---|---|
| O1 | [Obelisk pinned README](https://github.com/ObeliskMoney/Obelisk/blob/07d27bb8119e6b3951cb33889475853b72734d9f/README.md): signed agent execution/policy proofs in §3 | **Confirmed** | Publisher describes signatures and SP1 proofs; also labels beta, unaudited and a simulator. Confirms design claim, not production security. |
| O2 | [CLAUS about.json](https://claus.si/about.json): frozen core and independent pools in §7 | **Confirmed** | `chainControl` describes unavailable core upgrades; `transferPolicy` permits independent pools. Published description, not fresh ownership or module-delay proof. |
| O3 | [Hindsight pinned README](https://github.com/OoJae/hindsight-hook/blob/63efd09c79f903c50ceefcb935501915d9b8261b/README.md): ex-post settlement/testnet in §3 | **Confirmed** | Describes markout settlement and Unichain Sepolia. Publisher claim, not independently verified returns. |
| O4 | [Hindsight commit](https://github.com/OoJae/hindsight-hook/commit/63efd09c79f903c50ceefcb935501915d9b8261b): dated precedent in §8 | **Confirmed** | [Commit API](https://api.github.com/repos/OoJae/hindsight-hook/commits/63efd09c79f903c50ceefcb935501915d9b8261b) returns the exact SHA and committer date 2026-09-03. This does not establish latest activity. |
| O5 | [Tab pinned README](https://github.com/EmadQureshiKhi/Tab/blob/f4cdd36d97f69802477e59ff722b7aa54beeb26d/README.md): postpaid agent billing in §3 | **Confirmed** | Publisher describes Monad mainnet/testnet and payment after service delivery. Architecture/status claim confirmed as present; usage not independently verified. |

**Record:** The sample produced **15 confirmed, 1 wrong and 4 unreachable** citations. These counts are audit outcomes, not a report accuracy percentage: confirmations have different scopes and some validate only attributed claims.

### Additional checks material to the decision

**Record:** Open Lane says the factory source/fee ABI was not verified. This review found Sourcify runtime matches for both the [Robinhood hook factory](https://sourcify.dev/server/v2/contract/4663/0xa25b02a1e93903b790e6aaf7da1b8b8d50294645?fields=all) and [Ethereum hook factory](https://sourcify.dev/server/v2/contract/1/0x12c63b581d07093f6126bc02263c58f7eadaa96f?fields=all). Their `PoolFees` exposes `setRequester(uint64,address)`, `claimFees(uint64)` and retryable `withdraw(address,Currency)`. Failed recipient transfers restore amounts owed. This resolves source/ABI availability; it does **not** establish that LP Desk’s launch can hand off the requester before trading or safely collect either currency.

**Record:** [Ethereum Intake source](https://sourcify.dev/server/v2/contract/1/0xa43e6f75ee006411f79ac1c84120606c2330de82?fields=all) collects payment in `_request`; `complete` attempts a later callback. A callback is not acceptance escrow. [CLAUS governance source](https://sourcify.dev/server/v2/contract/1/0x180eae784dee739fbab432b06f78bf9a98aae334?fields=all) permits operator module changes and founder operator replacement without an enforced delay. Source properties are verified here; current ownership/roles were not independently reread.

**Claim:** The fetched [CLAUS fee feed](https://claus.si/fee-state.json) reports **23,000 ppm = 2.3%** total hook fees and automatic provider payments disabled. Its embedded observation is **2026-10-23T20:30:08.949Z**, block **26257727**: this is stale relative to this review’s read date, not current revenue. No balance is treated as an approved crew budget.

## 3. Scores and comparison

**Inference:** Scores use an ordinal **0–5** scale: **0** means absent/blocked, **3** means plausible but materially unproved, **5** means strongly supported and executable. Higher safety means safer. “Agent depth” asks whether useful judgment survives a deterministic baseline; “hook necessity” asks whether removing the hook loses the core product rather than just a funding source. “Revenue” means an evidenced external payer, not token issuance, a sponsor recycling fees or a balance. Equal-weight totals aid comparison, not launch approval. All cells below are Inference, read 2026-10-24; no score estimates returns or probability.

| Idea | Real gap | Speed to MVP | Agent depth | Hook necessity | IMD/CLAUS fit | Day-one revenue | Safety | Total /35 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Fee to Jobs | 2 | 3 | 4 | 2 | 4 | 1 | 2 | 18 |
| Agent First Opening | 3 | 2 | 4 | 4 | 3 | 1 | 2 | 19 |
| Claus Crew | 2 | 2 | 5 | 1 | 2 | 1 | 1 | 14 |
| Open Lane — LP Desk | 3 | 3 | 4 | 3 | 4 | 2 | 3 | **22** |
| Open Lane — Catalyst Reserve | 2 | 3 | 4 | 1 | 4 | 1 | 2 | 17 |
| Open Lane — Fee Stream Underwriter | 2 | 3 | 4 | 1 | 4 | 2 | 2 | 18 |

**Inference — Fee to Jobs:** Much of the mechanism exists in [OCTO source](https://github.com/RobertKodes/octo/blob/3c5d13b8bad5941a2de90079069016c0cd1e9cf4/src/OctoDAO.sol); new investigations can require agents, but a treasury can buy them directly. Upfront Intake settlement and unresolved retirement semantics add risk. R1’s thin-activity cohort is an attributed warning, not a reverified market statistic. No committed buyer is demonstrated. [R1](https://github.com/Identity-md/research/blob/main/jobs/dd378ca2-5133-464f-8e44-3e44bf8a5ba7/files/artifacts/report.md).

**Inference — Agent First Opening:** Pool-level admission gives the hook a meaningful job, but agent identity issuance, farming resistance and router recipient semantics determine whether it creates fairness. The [ERC-8004 specification](https://eips.ethereum.org/EIPS/eip-8004) explicitly acknowledges Sybil risk. [Uniswap CCA](https://github.com/Uniswap/continuous-clearing-auction/blob/ce78b4d94cdf94fd41f20afb6f6e495b8b83a234/README.md) is a simpler auction baseline. Flaunch’s pause does not solve this idea’s identity problem. [R2](https://github.com/Identity-md/research/blob/main/jobs/59734b38-c408-49f9-9354-a0bf6f304991/files/artifacts/report.md).

**Inference — Claus Crew:** Novel-interface recovery could demand substantial synthesis, hence its high agent-depth score is a hypothesis about the proposed work, not demonstrated capability. The verified claim chore needs ordinary code, and the source-level governance bypass remains. A second seat network and swap hook do not establish a customer. [R3](https://github.com/Identity-md/research/blob/main/jobs/aaeb3958-5818-4350-b441-a03bd8d28c80/files/artifacts/report.md).

**Inference — LP Desk:** A consenting LP is a clear buyer and execution is measurable. A bounded vault can protect principal better than open-ended recovery authority. Its safety score is relative: LP losses and advice quality remain unproved. Hook callbacks can register externally visible execution, but a vault-only service is a credible simpler competitor. The experiment must test whether the hook adds value rather than assume it. [R4](https://github.com/Identity-md/research/blob/main/jobs/f85fdd08-1c07-4c3f-a5e3-98b52847e411/files/artifacts/report.md), O1/O3/O5.

**Inference — Catalyst Reserve:** Reading disclosures can need judgment, but a panel signature remains trusted and can be stale or ambiguous. A reserve distributor can consume that answer without coupling the answer to swaps; payer and demand remain unidentified. **Inference — Underwriter:** Real bidder capital would evidence willingness to pay, but no competing bids are shown; future fee rights invite adverse selection, and [Tenet’s pinned proposal](https://github.com/tenet-agents/tenet-agents/blob/ce941f5b1cf29b19793a44881c5e664828504aaa/README.md) reduces novelty. Both inherit opening/accounting complexity without needing a hook for their central market. [R4](https://github.com/Identity-md/research/blob/main/jobs/f85fdd08-1c07-4c3f-a5e3-98b52847e411/files/artifacts/report.md).

## 4. Picks, each in five lines

### First action: none ready; run the LP Desk experiment

1. **Inference:** Build a fork-only consent-to-fee vertical slice; the public-launch answer is **none ready**, even though LP Desk ranks first.
2. **Inference:** Within **14 days**, ask **one independently controlled LP** to choose between **two sourced agent plans** and a passive plan under identical disclosed payment terms.
3. **Inference:** Require its signed, positive-priced service commitment from its own budget, without reimbursement, plus a reproduced trace from requester handoff through executed liquidity and collected-fee credits in both currencies; simulation is not revenue.
4. **Inference:** Pass only if all accounting/exit tests pass and the LP accepts a plan and its separately priced service on their merits without a sponsor rebate; missing consent, route failure or a safety counterexample means stop.
5. **Inference:** The sponsor funds bounded implementation/review; publish the negative result or a separately gated launch proposal, with no token, deployment or alpha promise required. See [SPEC](SPEC.md).

### Research moonshot: private, portable Agent First credentials

1. **Inference:** Retain R2’s private credential/nullifier opening as the moonshot: it could make agent participation portable without publishing the registry-to-buying-wallet link.
2. **Record:** [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004) supplies identity/reputation signals and warns of Sybil attacks; it does not certify independent beneficial control.
3. **Inference:** Research credential issuance first: an adversary obtaining multiple valid identities defeats a perfect nullifier circuit, so cryptography cannot be the first proof of readiness.
4. **Inference:** Require independent issuance review, duplicate-control attacks, revocation/transfer rules and recipient-safe router integration before spending on a production proof system.
5. **Inference:** Kill this direction if issuance is easily farmed or if [CCA](https://github.com/Uniswap/continuous-clearing-auction/blob/ce78b4d94cdf94fd41f20afb6f6e495b8b83a234/README.md) meets the actual buyers’ fairness need at lower complexity; no ZK launch is approved.

## 6. What IMD or CLAUS must still confirm before shipping

All items below are **Inference — launch gates**, read 2026-10-24. Missing facts are not presumed favorable.

| Responsible party | Confirmation / evidence required |
|---|---|
| IMD | Admission of the exact LP Desk bytecode/permission mask, constructor-created companions, plain token terms, PoolKey and opening restrictions; source availability is not admission. Confirm source/compiler/runtime match at the actual deployment block. |
| IMD | Contract-payer/requester identity, launch-result schema, initialization/seed order and timely `setRequester` handoff. Demonstrate collection and failed-payment retry in both currencies, including native currency, without consuming LP principal. |
| IMD | Current fees, supply allocation, gas/creation limits, quote support and refusal policy. Explain upfront procurement payment and callbacks honestly; no implied refund or acceptance-gated base fee. |
| Sponsor + LP + agents | Real sponsor budget, independently controlled LP and agent payout identities, signed deposit/exposure limits, informed acceptance of losses, custody terms and absence of rebates/wash trading. Their addresses and capital limits must be supplied and verified before any launch quote; none is invented here. |
| Independent reviewer | Reproduce fork snapshots, code hashes, permission bits, principal/fee separation, activation/exit checkpoints, signatures, auction refunds and retained factory debts. No unresolved path may trap principal or pay from nonexistent receipts. |
| IMD governance | Scope every external authority, including network-fee recipient changes. Distinguish immutable project rules from platform controls; if a universal delay is required, evidence every bypass is delayed or disabled. |
| CLAUS, only if later selected | Current owner/operator/founder/host roles and every replacement/recovery path; enforce the required delay across all of them, authorize a budget/allocation and demonstrate compatible LP lifecycle observations. Frozen proxy admins alone do not satisfy this. |
| IMD/CLAUS operations | Artifact retention, signer rotation, job refusal/liveness and disclosure of trusted service dependencies. A hash is not guaranteed hosting; distinct wallet addresses are not proof of independent operators. |

**Inference:** The LP Desk decision remains a single experiment, not a commitment to an entire product family. Fee to Jobs would additionally need acceptance/payment and actual retirement proofs; Claus Crew needs a customer-valued task beating a keeper; Agent First needs issuance economics. A future launch cannot bypass those missing facts by adopting the moonshot label.
