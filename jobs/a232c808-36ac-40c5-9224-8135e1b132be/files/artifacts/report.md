# $EMBER: architecture, tokenomics, and threat-model report

**Status:** design proposal; no Mainnet token deployment is proposed by this report.  
**Target / prototype:** Ethereum Mainnet / Sepolia.  
**Asset:** Ember (`EMBER`).  
**Decision posture:** contracts enforce bounded economic rules; Swarm agents propose, create, and independently review; a human-controlled Safe approves spending and production publishing in V1.

## 1. Evidence, labels, and limits

### Evidence labels

* **Fact (source)** is an externally verifiable technical fact, linked to a primary source.
* **Constraint (brief)** is a confirmed instruction supplied for this design.
* **Recommendation / inference** is a proposed design conclusion, not a fact or promise.
* **TBD** needs a governance, legal, commercial, or launch decision before deployment.

### Relevant technical facts

* **Fact:** ERC-20 defines `transfer`, `approve`, `allowance`, and `transferFrom`; `transferFrom` is specifically the delegated-spend workflow. It also cautions UIs about changing a nonzero allowance directly. [EIP-20](https://eips.ethereum.org/EIPS/eip-20).
* **Fact:** OpenZeppelin’s current ERC-20 implementation treats a supply mechanism as a derived-contract choice; its documented extensions include burnable and capped variants, and `SafeERC20` wraps ERC-20 interactions. [OpenZeppelin ERC-20 API](https://docs.openzeppelin.com/contracts/5.x/api/token/erc20).
* **Fact:** A Uniswap v4 hook is optional, is fixed in the pool key at initialization, and cannot later be added, removed, or exchanged. Hooks can run before/after swaps; their callable permissions are encoded in the hook address. [Uniswap v4 hooks](https://developers.uniswap.org/docs/protocols/v4/concepts/hooks).
* **Fact:** A v4 hook does not itself cause routing/liquidity to arrive; Uniswap documents that hook developers must not assume front-end routing. [Uniswap v4 hooks FAQ](https://developers.uniswap.org/docs/protocols/v4/concepts/hooks).

**Limits:** Neither market volume, IMD price, demand, legal classification, launch-platform availability, nor the precise meaning/transferability of IMD is established in this assignment. Dollar examples below are sensitivity illustrations, not forecasts. A security audit, tax/accounting review, sanctions/privacy policy, and counsel review remain required.

## 2. Executive design

### Proposed V1

1. Deploy an **immutable, fixed-supply, plain ERC-20** named Ember / `EMBER`, 18 decimals. Mint exactly the approved `TOTAL_SUPPLY` once in the constructor to a disclosed distribution executor; expose no post-deployment mint, pause, blacklist, confiscation, transfer-tax, reflection, rebase, or fee-exemption code.
2. Use a **separate Build Vault** whose assets are approved protocol revenue (initially preferably a stable settlement asset or WETH converted through an auditable policy), not an invisible deduction from user EMBER balances.
3. Run funding in **World Build Epochs**. A constrained on-chain state machine reserves a bounded job budget; off-chain Identity.md work produces artifacts; independent review and a human Safe approval are required before payment/publishing is finalized; an immutable registry publishes provenance hashes and a public World Pulse reflects only non-financial progress.
4. Deploy the **Genesis Forge** separately. A paid Genesis mint transfers an exact EMBER amount from the user and burns it in the same transaction before minting the Genesis PEPE. Qualified Active IMD Seats use a separate, one-time, entitlement route; there is no general-public free mint.
5. Start on **Sepolia** with production-like addresses, role procedures, event indexing, failure tests, and a public dashboard. Mainnet only follows independent audit, parameter freeze, legal review, and a public deployment manifest.

This is AI-native because the economic release condition is an attestable chain of *Swarm proposal → creation → independent review → human acceptance → published world artifact*, rather than a volume-triggered token reward. AI does useful work, but receives neither autonomous spending authority nor token-holder revenue rights.

### Why it is not a generic fee / burn token

The principal economic output is a verified published world build and its permanent provenance record. Revenue is released to fund approved IMD work; users can inspect the build/job/manifest linkage. Any later burn is a small, optional consequence of an accepted public artifact, never the system’s objective and never a charge against a holder. The system functions with Build-to-Burn off.

## 3. Architecture and roles

```text
Protocol revenue ──> Revenue Router ──> EMBER BUILD VAULT ──> Epoch budget
                                                     │              │
                                             Safe approves     Swarm job escrow
                                                                    │
User EMBER ──> Genesis Forge ──> ERC-20 burn ──> Genesis PEPE      │
                                                                    v
Swarm proposal → creator evidence → independent review → human acceptance
                                                        → Registry + publish → World Pulse
```

| Module | V1 responsibility | Must not do |
|---|---|---|
| `EmberToken` | fixed ERC-20 ledger, optional `burn` / `burnFrom` | mint later, tax transfers, blacklist, freeze, seize |
| `GenesisForge` | atomic paid forge and one-time seat-entitlement forge | custody residual EMBER, partial mint, arbitrary free mints |
| `BuildVault` | receive approved revenue; reserve/release epoch and job amounts | yield/dividend distribution, agent self-payment, unlimited withdrawal |
| `EpochManager` | create bounded epochs, budgets and build states | decide artistic quality or publish automatically |
| `BuildRegistry` | append hashes/IDs/timestamps and accepted state | hold IP ownership, create revenue rights, change token balance |
| `WorldPulse` | derived public counters/status for clients | affect balances, mint rights, exemptions, or rewards |
| optional `BurnReserve` | custody a pre-funded EMBER balance and burn only after accepted publication | pull user balances or finance operating expenses |

### Epoch state machine

`Draft → Funded → JobsApproved → Created → IndependentlyReviewed → HumanAccepted → Published → Closed`.

Only a Safe 2-of-3 may open/close an epoch, approve a job cap, release a payment, accept a build, or record the publication attestation in V1. A creator cannot be the reviewer. The registry rejects duplicate `(epochId, jobIdHash)` and records:

`buildId, epochId, jobIdHash, creatorAgentIdHash, reviewerAgentIdHash, imdCost, artifactManifestHash, contentIdHash, approvedAt, publishedAt, status`.

`artifactManifestHash` should commit to a versioned manifest containing artifact CIDs, source revision(s), tool/model disclosures as policy permits, test/render evidence, reviewer findings, and human approver reference. Hash only sensitive agent/job identifiers; publish a separately governed redaction policy. An indexer/UI may make the evidence usable, but contract events and content-addressed artifacts are the canonical proof trail.

### AI-native release gate: Proof-of-Build Escrow

**Recommendation:** reserve a job budget when the Safe approves a scoped job; release it only after all four attestations are recorded: creator submission, different reviewer approval, human acceptance, and publication hash. The Safe may reject/cancel an uncompleted job and return *unspent Vault funds* to the epoch—not take assets from an agent or holder.

This is deliberately a proof-of-*process and publication*, not a claim that a hash proves artistic quality. Human approval remains the quality and financial authority. Public metrics should measure published builds, review latency, accepted/rejected jobs, and budget committed/released—not “AI output tokens” or financial return.

## 4. Token supply and allocation

**Constraint:** fixed or strictly capped supply, minimal immutable core, no arbitrary mint.  
**Recommendation:** fixed supply is safer than a cap: `TOTAL_SUPPLY` minted exactly once at deployment; the token has no role and no external mint entrypoint. Burns reduce `totalSupply`; no mechanism replenishes them.

`TOTAL_SUPPLY`, `POOL_SHARE`, `INITIAL_TREASURY`, and allocation recipients remain **TBD**. Before any deploy, publish a one-page allocation table where every allocation sums exactly to 100%, includes recipient/vesting/custody, and calls out the liquidity inventory. Treasury EMBER is an asset controlled under disclosed Safe policy; it is not a promise of buyback or market support. Lock/vesting mechanics must be independently audited and disclosed.

Do not allocate “daily emissions,” staking APY, reflections, holder dividends, or fee-sharing: each conflicts with a confirmed constraint and dilutes the build-oriented design.

## 5. Two economic engines

### A. User utility: irreversible forging

Paid Genesis flow:

```text
user approve (or permit, if implemented) → Forge.forge(qty, maxCost)
→ calculate quoted fixed/scheduled price → transfer exact EMBER → burn
→ mint exactly qty Genesis PEPE → emit Forge event; otherwise revert all
```

Use `SafeERC20.safeTransferFrom` and immediately invoke token `burn` from Forge’s own received balance. This works with a conventional burnable token and gives a true burn: a `Transfer(forge, address(0), amount)` and lower `totalSupply`. An alternative immutable sink (sending to an unrecoverable address) is **not** a true ERC-20 burn: `totalSupply` remains unchanged and the sink’s key-loss assumption cannot be proven. Prefer real burn.

The paid method must require post-transfer `balanceAfter - balanceBefore == cost`; otherwise revert. EMBER V1 should have no transfer fee, so exact-received is straightforward and future fee-on-transfer modifications are impossible. `burnFrom(user, amount)` is viable but combines allowance spending/burning in token code; the transfer-then-burn Forge pattern keeps the token core broadly interoperable. A single transaction is atomic: a failure in transfer, exact amount, burn, supply limit, or NFT mint reverts the whole call.

Require `qty > 0`, checked multiplication/no overflow, `maxCost` slippage protection, a global paid-mint supply cap, optional per-wallet cap only if it is publicly fixed and does not block sale, and `nonReentrant`. Multi-mint must charge exactly `qty × unitPrice` and mint all or none. The seat entitlement path should verify an immutable/Merkle entitlement of `(seat, recipient, allocation=1, claimed=false)` and mark it claimed atomically; it must not bypass paid inventory controls beyond its explicitly disclosed allocation.

### B. Protocol utility: work becomes visible world growth

Revenue from disclosed protocol products/services, Forge-adjacent primary offerings where applicable, sponsorships, or a bounded trading mechanism funds the Vault. The Vault purchases/holds the settlement asset needed for approved work, then pays against accepted deliverables. EMBER holders receive no entitlement to Vault assets, agent output, protocol revenue, or future profits. The registry’s role is transparency only.

**Important accounting inference:** EMBER burned in Forge is no longer available to pay a Vault. Therefore Forge burn is user utility/deflation, not revenue. If a product wants to fund work, it must separately route payment to the Vault or use a disclosed primary-sale/revenue stream. Do not describe a burn as “Vault funding.”

## 6. Fee models (decision analysis)

These models describe a separately visible **protocol trade levy** only if a v4 hook is ultimately adopted; they are not a token transfer tax. “Total trading fee” = normal LP swap fee + protocol levy. Allocation applies only to the levy. For comparable sensitivity, monthly eligible one-sided EMBER pool volume `V = $1,000,000`, assumes the levy is collected successfully, and assumes an average accepted-job all-in budget `J = $2,500`. Actual revenue is `V × levy`; jobs are `floor(BuildVaultRevenue / J)`. These are arithmetic examples, not forecasts; volume could be zero.

| Model | LP fee + levy = total | Levy routing (Vault / ops-liquidity / burn reserve) | Vault per $1m eligible volume | Illustrative jobs | Trade-off |
|---|---:|---|---:|---:|---|
| Low-fee | 0.30% + 0.10% = **0.40%** | 70% / 30% / 0% | $700 | 0 | Best execution; weak direct funding and job granularity |
| Balanced | 0.30% + 0.35% = **0.65%** | 70% / 20% / 10% | $2,450 | 0 (near one) | Measurable build funding; still adds routing/MEV/audit burden |
| World-growth-heavy | 0.30% + 0.80% = **1.10%** | 75% / 15% / 10% | $6,000 | 2 | More visible job cadence; likely worse price competitiveness and avoidance/routing risk |

`ops-liquidity` means disclosed operational funding or liquidity-support inventory under Safe policy, **not** owner withdrawal from LP positions. A burn reserve accrues EMBER only after a transparent, externally executed conversion/purchase policy; it must have a separate per-epoch cap. No model may use the user’s transfer itself as a hidden tax.

**Recommendation:** do **not** activate a protocol levy in V1. Launch the plain ERC-20/Forge/Vault architecture and fund the Vault with direct disclosed protocol revenue. If Sepolia measurement and audit later demonstrate a need, the **Balanced** model is the maximum starting candidate, with levy immutable at 35 bps (or a contract-wide irreversible downward-only setting), 35 bps hard ceiling, 0% hook fee on paths/pools not explicitly configured at deployment, and no discretionary increase. It is less destructive than the heavy model but has enough signal to fund a whole job at roughly $1.02m illustrated eligible volume. This recommendation does not assume volume exists.

## 7. Pair decision: EMBER/IMD vs EMBER/WETH

| Question | EMBER/IMD | EMBER/WETH |
|---|---|---|
| Liquidity depth / price discovery | Depends entirely on IMD liquidity and reliable price; a correlated/thin asset can obscure EMBER’s price | Usually easier to route/quote against Ethereum’s base asset; still needs adequate EMBER depth |
| UX and gas | Potentially thematic for existing IMD users; third-party routes may need an extra hop | Familiar wallet/DEX flow; ETH/WETH wrapping and gas still apply |
| Routing / slippage | Can compound slippage when a user starts/ends in ETH or stable assets | Often fewer hops for Ethereum-native flow; concentrated-liquidity price impact still applies |
| Vault access to IMD | Direct acquisition is convenient *if* jobs truly settle in IMD | Vault must swap/hold IMD separately if IMD is needed, adding policy/execution risk |
| MEV / operations | Thin pair and multi-hop routes increase manipulation/quote risk | Large WETH routing ecosystem helps, but no pool is immune to MEV or shallow-liquidity manipulation |
| Genesis | Technically equivalent: Forge calls EMBER, not the pool | Technically equivalent |
| Narrative | Strong internal-loop story, but not evidence of safer market structure | Less thematic, more legible and practical for external discovery |

**Recommendation:** primary EMBER/WETH pool; do not make EMBER/IMD the canonical price pair without independently verified IMD liquidity, ERC-20 behavior, oracle requirements, and actual job settlement needs. The Vault may maintain an approved, auditable conversion route to IMD if payments require it. An EMBER/IMD secondary pool can be reconsidered after liquidity and routing evidence. Never use a manipulable pool spot price to price Forge mints or release Vault payments.

## 8. Uniswap v4 hook decision

**Recommendation: no hook in V1.** A standard pool requires no hook, and v4 hooks are immutable components of a pool key, so adding one prematurely permanently couples launch liquidity to novel custom code. A hook cannot solve insufficient liquidity or manufacture routing. Use a simple pool and direct revenue routing first.

### If a later hook is approved: smallest useful design

Deploy a new, explicitly labelled pool with an immutable **`EpochFeeHook`** only after audit. It implements `afterSwap` only (no return-delta permission) and has a deployment-time immutable pool key, settlement token, fixed levy `<=35 bps`, Vault address, and optional BurnReserve address. It has no owner, proxy, upgrader, whitelist, or mutable fee. The hook receives/accounting-credits the bounded levy under the v4 accounting design, emits `LevyAccrued(poolId, token, amount, split)`, and makes accumulated balances claimable only by the immutable Vault/BurnReserve addresses. Exact implementation must follow the audited v4 core/periphery version; do not improvise callback settlement.

* **`beforeSwap`:** not implemented. Therefore it cannot inspect sender to block sells, discriminate wallets, or alter a user’s requested swap.
* **`afterSwap`:** records/settles only the predetermined levy. It must not change swap deltas, call arbitrary external contracts, swap tokens, or depend on price/oracles during the callback.
* **Fee accounting:** account separately per currency and pool; never assume that the input is EMBER. Vault-side conversion happens later via a Safe-approved, slippage-bounded route and public event, never inside a swap callback. Do not double-count LP fee, hook levy, and protocol revenue.
* **Reentrancy:** callback functions are callable only by the canonical PoolManager and use a reentrancy guard around any post-callback claim/transfer function. Follow checks-effects-interactions; ERC-20 transfers occur outside the hook callback if the accounting architecture allows. A full audit must model PoolManager lock/settlement behavior.
* **Controls:** no upgradeability. If a critical defect appears, communicate and migrate liquidity voluntarily to a newly audited pool; no one may confiscate LP positions or force migration. A 2-of-3 Safe may operate the Vault, but cannot mutate hook behavior. If any emergency pause exists in surrounding Vault withdrawals, it requires a disclosed timelock and must not pause EMBER transfers, Forge exits, or pool swaps.

This design excludes arbitrary sell blocking, honeypots, blacklists, arbitrary balance changes, hidden tax changes, fee escalation, and owner extraction of LP liquidity. It should be rejected if a business requirement needs any of those powers.

## 9. Optional Build-to-Burn

**Verdict: later, disabled in V1.** It is narratively coherent but increases accounting, conversion, and “burn theatre” risk before the proof-of-build system is trusted.

If activated after audit and public vote/approval procedure, the reserve must be a separate contract holding only EMBER already transferred into it. `executeBuildBurn(buildId, amount)` is callable only once for a registry build in `Published` status and requires: (1) an immutable registry address; (2) a predefined epoch budget; (3) `amount <= perBuildMax`; (4) cumulative epoch burn `<= epochMax`; (5) reserve balance sufficiency. It burns its own balance using `burn(amount)` and emits build/epoch/amount. It cannot `transferFrom` a user, pull from Forge, or receive a changing cap.

“True burn” reduces `totalSupply`; a permanent sink only makes tokens inaccessible by convention. Public dashboards must label the choice precisely. The protocol must remain economically and operationally sound with zero reserve and disabled burn.

## 10. World Pulse: public, non-financial state

`WorldPulse` is a read model/event stream populated from Registry accepted/published transitions:

* `worldBuildCount`, `currentEpoch`, `epochFundingProgress`, `lastPublishedBuildId`, `dreamRoomsPublished`, and timestamps/status.
* Clients may map it to Agent House light levels, Dream Hall boards, celebrations, weather, and progress effects.

It must never determine ERC-20 balances, ownership, mint eligibility, entitlement allocation, fee exemption, token reward, exchange rate, or payment. World clients should tolerate stale/missing indexer data and display on-chain event links. This preserves free Web2 exploration: looking at the world requires no wallet or gas.

## 11. Threat model and controls

| Threat / failure | Consequence | Required control / test |
|---|---|---|
| Token admin key or upgrade bug | mint, freeze, tax, or seize risk | no token roles/proxy; constructor-only fixed mint; source/bytecode verification; independent audit |
| Malicious/buggy Forge | user pays without Genesis or price changes | atomic transfer/burn/mint; exact-received check; immutable price schedule/caps; `maxCost`; reentrancy tests; pause only before public launch if possible |
| Allowance phishing/race | unwanted delegated transfer | clear spender/chain UI, permit domain verification if used, recommend zero-then-set for changing allowances per EIP-20, exact Forge address verification |
| Fake EMBER / wrong chain | assets sent to impostor contract | publish chain ID, addresses, bytecode hash, verified source, deployment manifest; Forge hardcodes real Mainnet EMBER only after address verification |
| Vault Safe compromise/collusion | misdirected spending | Safe 2-of-3 with independent signers/hardware custody, timelock for non-urgent policy changes, per-epoch/job caps, events, reconciliation, no agent signer |
| Agent self-review / fabricated work | bad work paid; trust loss | creator/reviewer identity inequality, job hash binding, artifact evidence, human acceptance, sampled independent audit, rejection/correction workflow |
| Human approval capture | subjective or improper publication/payment | documented acceptance rubric, dual-sign review policy, public rationale/manifest hash, budget caps; acknowledge V1 remains trust-bearing |
| CID/link rot or sensitive data leak | unverifiable or privacy-harming proof | content pinning/redundant archive, hashed IDs, redaction policy, do not put PII/secrets on-chain |
| Oracle/spot-price manipulation | unfair Forge price or Vault conversion | no AMM spot price for Forge/payment decisions; fixed schedule or robust oracle with bounds, TWAP and independent execution checks if later required |
| Hook callback/settlement bug | stuck swaps/funds, reentrancy | V1 no hook; if later, minimal afterSwap-only immutable code, canonical caller check, no external calls in callback, fuzz/invariant testing and audit |
| Fee escalation / stealth tax | honeypot perception and user harm | fee-free token; any later hook levy immutable or hard-capped at deployment, code/address disclosures |
| LP withdrawal / thin liquidity | slippage, price instability | disclose LP ownership/lock policy; no protocol ability to extract user LP positions; staged liquidity and monitoring, not price promises |
| MEV / sandwiching | poor trade execution | user-facing slippage warnings, aggregators/private routing where appropriate, no hook-dependent price actions; no claims of MEV elimination |
| Burn reserve abuse | arbitrary deflation theatre / wrong build linkage | zero-by-default, own-balance-only burn, immutable caps, registry published-state proof, once-per-build guard |
| Indexer/UI lies | misleading World Pulse/proof | verify signed/on-chain events and content hashes; UI labels indexed data; reproducible registry export |
| Regulatory/consumer confusion | legal and reputation exposure | no yield/revenue/ownership language, clear risk disclosures, counsel review in relevant jurisdictions, no performance claims |

## 12. Governance, controls, and operations

* **V1 authority:** Mainnet Build Vault/Epoch/Registry administration sits in a disclosed Safe 2-of-3. Signers are public roles/identities subject to an operating policy; agents have zero signing authority.
* **Timelock:** changes that can redirect future Vault revenue or modify Registry/Epoch policy use a public timelock. The immutable token and immutable Forge configuration should not be upgradeable. Emergency powers, if any, may stop *new Vault job release only*, are narrowly timed, and cannot seize, blacklist, pause EMBER, or block pool sells.
* **Separation:** Safe proposes/authorizes money and publication; agents make/review artifacts; human reviewers approve value; an indexer presents evidence. No single actor should author, review, accept, and pay the same job.
* **Transparency:** publish addresses, roles, thresholds, token supply/allocation, parameter hashes, epoch/job events, manifests, released/remaining budget, and a monthly reconciliation. Public dashboards must not imply token-holder claim rights.

## 13. Sepolia prototype and Mainnet gates

### Sepolia scope

Deploy test-only equivalents of Token, Forge, Vault, EpochManager, Registry, Pulse, and optionally a disabled BurnReserve. Exercise: normal paid forge; free-seat claim; duplicate claim; insufficient allowance; wrong token; NFT mint failure rollback; duplicate job; creator=reviewer; rejected build; late publication; epoch cap; Safe-only calls; zero/reserve/cap burn cases; event/indexer reconstruction. If experimenting with a v4 hook, use a separate experimental pool and test callback/reentrancy/invariant cases; it does not become a Mainnet commitment.

### Mainnet go/no-go checklist

1. Final supply/allocation/vesting, Forge price/caps, pair, revenue sources, and Build-to-Burn choice are public and internally consistent.
2. Real Mainnet EMBER address is hardcoded/verified by the final Genesis contract; no test token, mock, proxy swap, or symbolic address is accepted.
3. Independent audit covers every deployed module and deployment configuration; critical/high findings are remediated and published with scope/commit hash.
4. Safe signers, threshold, recovery/runbook, timelock, Vault job caps, and emergency boundaries are published and rehearsed.
5. Forge/Registry/Vault event schemas, dashboard, manifest retention, reconciliation, and incident disclosure process work on Sepolia.
6. Legal, tax, privacy, consumer-disclosure, IP/licensing, and sanctions reviews are completed for intended jurisdictions.
7. No claim is made that EMBER yields income, pays dividends, confers ownership, ensures liquidity, or guarantees world output.

## 14. Decisions required before implementation

| TBD | Decision owner / evidence needed |
|---|---|
| `TOTAL_SUPPLY`, allocation, pool share, treasury and vesting | accountable issuer/governance; allocation model and custody disclosures |
| Initial primary pair and LP ownership/lock policy | launch lead; independently checked liquidity/routing and risk review |
| Is IMD a real Mainnet ERC-20 and what asset pays jobs? | technical/operations lead; contract address, decimals, transfer behavior, liquidity, accounting/legal review |
| Exact revenue sources and settlement asset | product/finance/legal; no conflation of burn with revenue |
| Genesis inventory, paid price formula, seat snapshot/entitlement and anti-sybil policy | product/legal; privacy-preserving claim data and supply math |
| Vault payment currency and agent/vendor terms | operations/legal; tax, IP, contractor and payout compliance |
| Build acceptance rubric, identity/reviewer independence and dispute process | product/Swarm governance; publicly versioned policy |
| Launch platform / distribution restrictions | launch/legal; platform due diligence and geographic/consumer disclosures |
| Buyback | recommendation: disabled/none at launch; if reconsidered, obtain legal, accounting, market-abuse, execution and public-policy review |
| Build-to-Burn | recommendation: disabled V1; later only with immutable caps, audit, and a demonstrated proof-of-build cadence |

## 15. Recommended decision record

Adopt the fee-free, fixed-supply EMBER core; atomic true-burn Genesis Forge; WETH-primary plain pool; direct-revenue Build Vault; proof-of-build escrow/registry; human/Safe V1 controls; and World Pulse limited to display. Build-to-Burn and all v4-hook trade levies remain disabled/deferred. This preserves the decisive loop—**the economy funds the Swarm; the Swarm grows the world**—while refusing to make market trading or automated AI authority the center of the system.

